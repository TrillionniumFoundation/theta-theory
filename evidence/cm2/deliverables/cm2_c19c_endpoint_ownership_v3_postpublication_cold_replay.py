#!/usr/bin/env python3
"""Cold post-publication replay for the sealed C19C endpoint v3 bundle.

This wrapper snapshots the sealed manifest, all fifteen manifest members, its
own source, and the exact Python executable before and after an isolated
independent-verifier replay.  It publishes evidence only after byte and inode
metadata identity, a clean numeric exit, empty stderr, and replay closure all
pass.  It never authorizes C27/C28/C29 or a Source-W transition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import stat
import subprocess
import time
from pathlib import Path
from typing import Any


BASE_MANIFEST = "cm2_c19c_endpoint_ownership_v3_manifest.sha256"
BASE_MANIFEST_SHA256 = "14643e303aee7a3bac27342204ee92f2420ae855a5df66916307680721c82929"
BASE_RESULT = "cm2_c19c_endpoint_ownership_v3_result.json"
BASE_RECEIPT = "cm2_c19c_endpoint_ownership_v3_terminal_receipt.json"
VERIFIER = "cm2_c19c_endpoint_ownership_v3_independent_verifier.py"
PUBLISHED_VERIFICATION = "cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_verification.json"
COLD_RECEIPT = "cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_receipt.json"
COLD_MANIFEST = "cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_manifest.sha256"
EXPECTED_MEMBERS = {
    "cm2_c19c_endpoint_ownership_v3_attack_harness.py",
    "cm2_c19c_endpoint_ownership_v3_attack_result.json",
    "cm2_c19c_endpoint_ownership_v3_authority.py",
    "cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_c19c_additive_replay_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_c25_additive_replay_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_c26_additive_replay_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_codimension1_in_face_junction_1d_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_codimension2_in_face_junction_0d_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_face_atom_ledger.jsonl.gz",
    "cm2_c19c_endpoint_ownership_v3_independent_verification.json",
    VERIFIER,
    "cm2_c19c_endpoint_ownership_v3_receipt_builder.py",
    BASE_RESULT,
    BASE_RECEIPT,
}


class Reject(RuntimeError):
    pass


def demand(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def filesha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def closed_json(path: Path, closure_key: str) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    demand(canonical(value) == raw, "canonical JSON:" + path.name)
    body = dict(value)
    claimed = body.pop(closure_key, None)
    demand(claimed == objsha(body), "JSON closure:" + path.name)
    return value


def stat_record(path: Path) -> dict[str, Any]:
    value = path.stat()
    return {
        "device": value.st_dev,
        "inode": value.st_ino,
        "mode": stat.S_IMODE(value.st_mode),
        "nlink": value.st_nlink,
        "size": value.st_size,
        "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def snapshot(items: list[tuple[str, Path]]) -> dict[str, Any]:
    return {
        "sha256": {label: filesha(path) for label, path in items},
        "stat": {label: stat_record(path) for label, path in items},
    }


def parse_manifest(bundle: Path) -> dict[str, str]:
    path = bundle / BASE_MANIFEST
    demand(filesha(path) == BASE_MANIFEST_SHA256, "base manifest pin")
    members: dict[str, str] = {}
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        demand(len(pieces) == 2, f"manifest syntax:{ordinal}")
        digest, name = pieces
        demand(len(digest) == 64 and all(ch in "0123456789abcdef" for ch in digest), f"manifest digest:{ordinal}")
        demand(name == Path(name).name and name not in members, f"manifest member name:{ordinal}")
        members[name] = digest
    demand(set(members) == EXPECTED_MEMBERS and len(members) == 15, "exact fifteen-member manifest")
    for name, digest in members.items():
        demand(filesha(bundle / name) == digest, "manifest member hash:" + name)
    return members


def publish_bytes(path: Path, content: bytes) -> None:
    if path.exists():
        demand(path.read_bytes() == content, "append-only publication conflict:" + path.name)
        return
    with path.open("xb") as stream:
        stream.write(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    demand(args.seed > 0, "positive seed")
    bundle = Path(args.bundle_dir).resolve()
    run_dir = Path(args.run_dir).resolve()
    python = Path(args.python).resolve()
    wrapper = Path(__file__).resolve()
    demand(bundle.is_dir() and python.is_file() and wrapper.parent == bundle, "resolved inputs")
    demand(not run_dir.exists(), "new cold run directory")
    for name in (PUBLISHED_VERIFICATION, COLD_RECEIPT, COLD_MANIFEST):
        demand(not (bundle / name).exists(), "new append-only output:" + name)
    run_dir.mkdir(parents=True, mode=0o700)

    members = parse_manifest(bundle)
    base_result = closed_json(bundle / BASE_RESULT, "result_sha256")
    base_receipt = closed_json(bundle / BASE_RECEIPT, "receipt_sha256")
    demand(base_receipt["status"] == "PASS_APPEND_ONLY_V3_AUTHORITY_DUAL_SEED_DUAL_VERIFIER_ATTACK_SEALED", "base receipt status")
    demand(base_receipt["formal_credit"] == 0 and base_receipt["C27_C28_C29"] == "UNAUTHORIZED_PENDING_REBUILD", "base receipt nonpromotion")
    demand(base_receipt["CM2"] == "NO-GO_FOR_CLAIM" and base_receipt["source_W_transition_authorized"] is False, "base global nonpromotion")

    observed: list[tuple[str, Path]] = [("bundle/" + BASE_MANIFEST, bundle / BASE_MANIFEST)]
    observed.extend(("bundle/" + name, bundle / name) for name in sorted(members))
    observed.extend((("runtime/python", python), ("runtime/wrapper", wrapper)))
    pre = snapshot(observed)

    replay_path = run_dir / "verification.json"
    environment = {
        "HOME": "/nonexistent",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "PYTHONHASHSEED": str(args.seed),
    }
    command = [
        str(python), "-S", "-B", str(bundle / VERIFIER),
        "--candidate-dir", str(bundle),
        "--seed", str(args.seed),
        "--output", str(replay_path),
    ]
    started = time.monotonic_ns()
    usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    process = subprocess.run(
        command,
        cwd=bundle.parent,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    ended = time.monotonic_ns()
    numeric_exit = process.returncode if process.returncode >= 0 else None
    signal_number = -process.returncode if process.returncode < 0 else None
    (run_dir / "stdout.json").write_bytes(process.stdout)
    (run_dir / "stderr.log").write_bytes(process.stderr)
    (run_dir / "exit.json").write_bytes(canonical({"numeric_exit": numeric_exit, "signal": signal_number}))

    demand(numeric_exit == 0 and signal_number is None, "clean replay exit")
    demand(process.stderr == b"", "empty replay stderr")
    stdout_value = json.loads(process.stdout)
    replay = closed_json(replay_path, "verification_sha256")
    demand(stdout_value == {"status": "PASS", "verification_sha256": replay["verification_sha256"]}, "stdout/replay binding")
    demand(replay["status"] == "PASS" and replay["verification_seed"] == args.seed, "replay status/seed")
    demand(replay["verified_result_sha256"] == base_result["result_sha256"], "replay/result binding")
    demand(replay["verified_ledgers"] == base_result["ledgers"], "replay/ledger binding")
    demand(replay["formal_credit"] == 0, "replay zero credit")

    post = snapshot(observed)
    demand(pre == post, "pre/post SHA+stat identity")

    published_verification = bundle / PUBLISHED_VERIFICATION
    publish_bytes(published_verification, replay_path.read_bytes())
    timing = {
        "wall_seconds": (ended - started) / 1_000_000_000,
        "user_seconds": usage_after.ru_utime - usage_before.ru_utime,
        "system_seconds": usage_after.ru_stime - usage_before.ru_stime,
        "maximum_resident_set_kib": usage_after.ru_maxrss,
    }
    semantic = {
        "schema": "cm2.c19c-endpoint-ownership-v3.postpublication-cold-replay-receipt.v1",
        "status": "PASS_COLD_POSTPUBLICATION_REPLAY_PRE_POST_SHA_STAT_IDENTICAL__ZERO_FORMAL_CREDIT",
        "base_manifest": {
            "filename": BASE_MANIFEST,
            "sha256": BASE_MANIFEST_SHA256,
            "member_count": len(members),
            "members": members,
        },
        "observed_pre_sha256": pre["sha256"],
        "observed_pre_stat": pre["stat"],
        "observed_post_sha256": post["sha256"],
        "observed_post_stat": post["stat"],
        "pre_post_sha256_identical": pre["sha256"] == post["sha256"],
        "pre_post_stat_identical": pre["stat"] == post["stat"],
        "isolated_replay": {
            "command": command,
            "environment": environment,
            "verification_seed": args.seed,
            "numeric_exit": numeric_exit,
            "signal": signal_number,
            "stderr_empty": process.stderr == b"",
            "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
            "timing": timing,
        },
        "replay_verification": {
            "filename": PUBLISHED_VERIFICATION,
            "file_sha256": filesha(published_verification),
            "verification_sha256": replay["verification_sha256"],
            "verified_result_sha256": replay["verified_result_sha256"],
            "census": replay["census"],
            "closure_valid": True,
        },
        "source_pins": {
            "python_executable_sha256": pre["sha256"]["runtime/python"],
            "wrapper_sha256": pre["sha256"]["runtime/wrapper"],
            "independent_verifier_sha256": members[VERIFIER],
        },
        "formal_credit": 0,
        "C27_C28_C29": "UNAUTHORIZED_PENDING_REBUILD",
        "CM2": "NO-GO_FOR_CLAIM",
        "source_W_transition_authorized": False,
        "required_next": "CONSUME_ONLY_IN_C27_INDEPENDENT_SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE",
    }
    receipt = {**semantic, "receipt_sha256": objsha(semantic)}
    receipt_path = bundle / COLD_RECEIPT
    publish_bytes(receipt_path, canonical(receipt))
    cold_manifest_members = [BASE_MANIFEST, wrapper.name, PUBLISHED_VERIFICATION, COLD_RECEIPT]
    manifest_bytes = b"".join(
        f"{filesha(bundle / name)}  {name}\n".encode("ascii")
        for name in sorted(cold_manifest_members)
    )
    publish_bytes(bundle / COLD_MANIFEST, manifest_bytes)
    print(canonical({
        "status": receipt["status"],
        "receipt_sha256": receipt["receipt_sha256"],
        "supplemental_manifest_sha256": filesha(bundle / COLD_MANIFEST),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
