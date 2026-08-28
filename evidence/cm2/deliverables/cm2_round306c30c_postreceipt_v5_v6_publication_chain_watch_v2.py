#!/usr/bin/env python3
"""Fresh-token C30c publication chain consuming the v5/v6 joint adapter."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import stat
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
RECEIPTS = WORKSPACE / ".cm2-runtime/receipts"
ADAPTER_PROGRAM = DELIVERABLES / "cm2_round306c30c_postreceipt_v5_v6_joint_attestation_consumer_adapter_v1.py"
VERIFIER = DELIVERABLES / "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_independent_verifier.py"
PYTHON = WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
CANDIDATE = WORKSPACE / ".cm2-runtime/candidates/c30c-v4-seed-30630071"
RESULT_NAME = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_result.json"
VERIFIER_SHA256 = "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377"
RESULT_OBJECT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"
C30B_MANIFEST = DELIVERABLES / "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256"
C30B_MANIFEST_SHA256 = "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
VERIFIER_STATUS = ("PASS_INDEPENDENT_CANDIDATE_C30C__80_DELTA_H_CELLS__"
                   "2_RESOLVED_MIXED__ZERO_FORMAL_CREDIT")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def closed(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body["object_sha256"] = hashlib.sha256(canonical(body)).hexdigest()
    return body


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in result, "unique key:" + label)
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def file_bytes(path: Path, maximum: int = 128 << 20) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        raw = os.read(descriptor, before.st_size + 1)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                              value.st_uid, value.st_gid, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns)
    need(len(raw) == before.st_size and identity(before) == identity(after),
         "stable capture:" + os.fspath(path))
    return raw


def sha(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "hash singleton:" + path.name)
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns),
         "stable hash:" + path.name)
    return state.hexdigest()


def validate_object(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    observed = body.pop("object_sha256", None)
    need(type(observed) is str and HEX64.fullmatch(observed) is not None
         and hashlib.sha256(canonical(body)).hexdigest() == observed, "object closure:" + label)


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


def verify_adapter(adapter: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    environment = {"HOME": os.environ.get("HOME", "/home/qian-qi"),
                   "LC_ALL": "C.UTF-8", "TZ": "UTC", "PATH": "/usr/bin:/bin",
                   "PYTHONDONTWRITEBYTECODE": "1",
                   "XDG_RUNTIME_DIR": os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000")}
    if "DBUS_SESSION_BUS_ADDRESS" in os.environ:
        environment["DBUS_SESSION_BUS_ADDRESS"] = os.environ["DBUS_SESSION_BUS_ADDRESS"]
    completed = subprocess.run(
        ["/usr/bin/python3", "-I", "-B", os.fspath(ADAPTER_PROGRAM),
         "--verify", "--adapter-dir", os.fspath(adapter)], cwd=WORKSPACE,
        env=environment,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"", "clean adapter verifier")
    verification = strict_object(completed.stdout, "adapter verification")
    validate_object(verification, "adapter verification")
    receipt = strict_object(file_bytes(adapter / "adapter_receipt.json"), "adapter receipt")
    validate_object(receipt, "adapter receipt")
    need(verification.get("status") == "PASS_ADAPTER_LIVE_REPLAY_AND_ALL_BINDINGS"
         and verification.get("adapter_receipt_object_sha256") == receipt.get("object_sha256")
         and receipt.get("publication_precondition_satisfied") is True
         and receipt.get("source_W_formal_remainder") == 80
         and receipt.get("source_W_transition_authorized") is False,
         "exact adapter publication precondition")
    return verification, receipt


def audited_dual_mathematics(bridge: Path) -> tuple[dict[str, Any], bytes]:
    need(sha(VERIFIER) == VERIFIER_SHA256 and sha(C30B_MANIFEST) == C30B_MANIFEST_SHA256,
         "pinned verifier and predecessor")
    first = file_bytes(bridge / "dual-seed-30630071/stdout.json")
    second = file_bytes(bridge / "dual-seed-30630929/stdout.json")
    need(first == second, "dual verifier byte identity")
    expected = strict_object(first, "dual verifier output")
    need(expected.get("status") == VERIFIER_STATUS
         and expected.get("candidate_result_sha256") == RESULT_OBJECT_SHA256
         and expected.get("proposed_source_W_remaining_transition") == "80->78"
         and expected.get("formal_credit") == 0 and expected.get("manifest_authorized") is False,
         "audited dual exact mathematical conclusion")
    result = strict_object(file_bytes(CANDIDATE / RESULT_NAME), "candidate result")
    body = dict(result); observed = body.pop("result_sha256", None)
    need(observed == RESULT_OBJECT_SHA256
         and hashlib.sha256(canonical(body)).hexdigest() == observed,
         "candidate result object closure")
    return expected, first


def evidence_sources(adapter: Path, bridge: Path) -> list[tuple[str, Path]]:
    sources: list[tuple[str, Path]] = []
    roots = (("adapter", adapter), ("bridge", bridge), ("candidate", CANDIDATE),
             ("transaction-run", AUDIT / RUN_NAME), ("transaction-receipt", RECEIPTS / RUN_NAME))
    for prefix, root in roots:
        need(root.is_dir() and not root.is_symlink(), "real evidence root:" + prefix)
        for path in sorted(root.rglob("*"), key=lambda value: value.relative_to(root).as_posix()):
            if path.is_file() and not path.is_symlink():
                sources.append((prefix + "/" + path.relative_to(root).as_posix(), path))
    sources.extend((("programs/adapter.py", ADAPTER_PROGRAM),
                    ("programs/publication_watcher.py", Path(__file__).resolve(strict=True)),
                    ("programs/independent_verifier.py", VERIFIER),
                    ("predecessor/manifest.sha256", C30B_MANIFEST)))
    names = [name for name, _ in sources]
    need(len(names) == len(set(names)) and len(names) >= 150, "complete unique evidence inventory")
    return sources


def deterministic_bundle(chain: Path, sources: list[tuple[str, Path]]) -> tuple[str, int]:
    temporary = tempfile.NamedTemporaryFile(prefix=".bundle-", dir=chain, delete=False)
    temporary_path = Path(temporary.name)
    try:
        with temporary:
            with gzip.GzipFile(filename="", mode="wb", fileobj=temporary, mtime=0) as zipper:
                with tarfile.open(fileobj=zipper, mode="w|") as archive:
                    for name, path in sources:
                        raw = file_bytes(path)
                        info = tarfile.TarInfo(name)
                        info.size = len(raw); info.mode = 0o400; info.uid = 0; info.gid = 0
                        info.uname = ""; info.gname = ""; info.mtime = 0
                        import io
                        archive.addfile(info, io.BytesIO(raw))
            os.fsync(temporary.fileno())
        target = chain / "c30c_v5_v6_joint_publication_evidence.tar.gz"
        os.link(temporary_path, target)
        os.unlink(temporary_path)
        return sha(target), target.stat().st_size
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def run(adapter: Path, chain: Path) -> dict[str, Any]:
    need(adapter.parent == AUDIT and chain.parent == AUDIT and not chain.exists()
         and chain.name.startswith("c30c-publication-v5-v6-chain-"), "fresh exact chain path")
    verification, adapter_receipt = verify_adapter(adapter)
    bridge = AUDIT / adapter_receipt["bridge_name"]
    fresh, fresh_raw = audited_dual_mathematics(bridge)
    sources = evidence_sources(adapter, bridge)
    before = {name: sha(path) for name, path in sources}
    chain.mkdir(mode=0o700)
    exclusive(chain / "adapter_verification.json", canonical(verification) + b"\n")
    outer = closed({
        "schema": "cm2.round306c30c.v5-v6-publication-outer-verification.v1",
        "status": "PASS_JOINT_ADAPTER_AND_AUDITED_DUAL_MATHEMATICS__CONDITIONAL_80_TO_78",
        "adapter_receipt_object_sha256": adapter_receipt["object_sha256"],
        "audited_dual_verifier_stdout_sha256": hashlib.sha256(fresh_raw).hexdigest(),
        "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "formal_credit": 0, "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False, "CM2": "NO-GO_FOR_CLAIM",
    })
    exclusive(chain / "outer_verification.json", canonical(outer) + b"\n")
    bundle_sha, bundle_size = deterministic_bundle(chain, sources)
    after = {name: sha(path) for name, path in sources}
    need(before == after, "all publication sources stable across bundle")
    evidence = closed({"schema": "cm2.round306c30c.v5-v6-publication-evidence-index.v1",
                       "status": "PASS_EXACT_SOURCE_INVENTORY_BUNDLED",
                       "entries": [{"name": name, "sha256": before[name]}
                                   for name in sorted(before)],
                       "entry_count": len(before), "bundle_sha256": bundle_sha,
                       "bundle_size": bundle_size})
    exclusive(chain / "evidence_index.json", canonical(evidence) + b"\n")
    payload_names = ("adapter_verification.json", "outer_verification.json",
                     "c30c_v5_v6_joint_publication_evidence.tar.gz", "evidence_index.json")
    payload = "".join(f"{sha(chain / name)}  {name}\n" for name in payload_names)
    exclusive(chain / "payload_manifest.sha256", payload.encode("ascii"))
    root = f"{sha(chain / 'payload_manifest.sha256')}  payload_manifest.sha256\n"
    exclusive(chain / "root_manifest.sha256", root.encode("ascii"))
    terminal = closed({
        "schema": "cm2.round306c30c.v5-v6-joint-publication-terminal-replay.v1",
        "status": "PASS_TERMINAL_REPLAY__FORMAL_SOURCE_W_80_TO_78",
        "adapter_receipt_object_sha256": adapter_receipt["object_sha256"],
        "joint_attestation_object_sha256": adapter_receipt["joint_attestation_object_sha256"],
        "outer_verification_object_sha256": outer["object_sha256"],
        "evidence_index_object_sha256": evidence["object_sha256"],
        "payload_manifest_sha256": sha(chain / "payload_manifest.sha256"),
        "root_manifest_sha256": sha(chain / "root_manifest.sha256"),
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "candidate_result_object_sha256": RESULT_OBJECT_SHA256,
        "source_W_transition": {"before": 80, "after": 78},
        "formal_credit": {"resolved_source_W_origin_dispositions": 2,
                          "resolved_nonexcluded": 2, "whole_source_W_origin_exclusions": 0},
        "source_W_formal_remainder": 78, "source_W_transition_authorized": True,
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
        "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
    })
    exclusive(chain / "terminal_replay.json", canonical(terminal) + b"\n")
    final = closed({
        "schema": "cm2.round306c30c.v5-v6-publication-chain-watch.v2",
        "status": "PASS_C30C_V5_V6_JOINT_PUBLICATION__FORMAL_SOURCE_W_80_TO_78",
        "chain_name": chain.name, "terminal_replay_object_sha256": terminal["object_sha256"],
        "terminal_replay_file_sha256": sha(chain / "terminal_replay.json"),
        "source_W_formal_remainder": 78, "source_W_transition_authorized": True,
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
        "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
    })
    exclusive(chain / "chain_status.json", canonical(final) + b"\n")
    exclusive(chain / "PUBLICATION_PASS.lock",
              b"PASS_C30C_V5_V6_JOINT_PUBLICATION__SOURCE_W_80_TO_78__CM2_NO_GO\n")
    return final


def self_test(adapter: Path) -> dict[str, Any]:
    verification, receipt = verify_adapter(adapter)
    bridge = AUDIT / receipt["bridge_name"]
    fresh, _ = audited_dual_mathematics(bridge)
    need(fresh.get("status") == VERIFIER_STATUS, "self-test mathematics")
    return closed({"schema": "cm2.round306c30c.v5-v6-publication-watch-selftest.v1",
                   "status": "PASS_ADAPTER_REPLAY_AND_AUDITED_DUAL_MATHEMATICS",
                   "adapter_verification_object_sha256": verification["object_sha256"],
                   "formal_credit": 0, "source_W_transition_authorized": False})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter-dir", required=True, type=Path)
    parser.add_argument("--chain-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        adapter = arguments.adapter_dir.resolve(strict=True)
        if arguments.self_test:
            need(arguments.chain_dir is None, "self-test creates no chain")
            output = self_test(adapter)
        else:
            need(arguments.chain_dir is not None, "chain path required")
            output = run(adapter, arguments.chain_dir.absolute())
    except (Blocked, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError,
            tarfile.TarError) as error:
        print(canonical({"schema": "cm2.round306c30c.v5-v6-publication-chain-watch.v2",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 2
    print(canonical(output).decode("ascii"))
    return 0


def held_entry(source_fd: int, source_state: os.stat_result, source_raw: bytes,
               expected_sha256: str, argv: list[str]) -> int:
    def verify_source() -> None:
        current = os.fstat(source_fd)
        identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                                  value.st_uid, value.st_gid, value.st_size,
                                  value.st_mtime_ns, value.st_ctime_ns)
        need(identity(current) == identity(source_state)
             and stat.S_ISREG(current.st_mode) and stat.S_IMODE(current.st_mode) == 0o444
             and current.st_nlink == 1 and current.st_uid == os.getuid()
             and current.st_gid == os.getgid() and len(source_raw) == current.st_size
             and HEX64.fullmatch(expected_sha256) is not None
             and hashlib.sha256(source_raw).hexdigest() == expected_sha256,
             "held publication watcher source")
    try:
        verify_source()
        result = main(argv)
        verify_source()
        return result
    finally:
        os.close(source_fd)


if __name__ == "__main__":
    raise SystemExit(main())
