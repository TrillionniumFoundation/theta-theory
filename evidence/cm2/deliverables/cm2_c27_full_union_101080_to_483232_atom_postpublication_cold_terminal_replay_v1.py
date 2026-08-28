#!/usr/bin/env python3
"""Cold, manifest-first postpublication replay of the scoped atom seal."""
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

BASE_MANIFEST = "manifest.sha256"
BASE_MANIFEST_SHA256 = "5ec48d319fd02c6907abf06300d0668604da6ccd10f07f2023c02d099939a648"
BASE_RECEIPT = "terminal_zero_credit_receipt.json"
BASE_RECEIPT_FILE_SHA256 = "456d462da8f269112908caaed8bb30a9ff042d54760136c675d00abda28f0241"
VERIFIER_SHA256 = "87220d033900e50e3b831d79e85e985377fec035f72f056d9e6dd198a285b414"
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
PUBLISHED_VERIFICATION = "postpublication_cold_terminal_verification.json"
COLD_RECEIPT = "postpublication_cold_terminal_receipt.json"
COLD_MANIFEST = "postpublication_cold_terminal_manifest.sha256"


class Reject(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stat_record(path: Path) -> dict[str, Any]:
    value = path.stat()
    return {
        "device": value.st_dev,
        "inode": value.st_ino,
        "mode": stat.S_IMODE(value.st_mode),
        "uid": value.st_uid,
        "gid": value.st_gid,
        "size": value.st_size,
        "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def snapshot(paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "sha256": {label: file_sha(path) for label, path in sorted(paths.items())},
        "stat": {label: stat_record(path) for label, path in sorted(paths.items())},
    }


def parse_manifest(root: Path, bundle: Path) -> dict[str, str]:
    manifest = bundle / BASE_MANIFEST
    need(file_sha(manifest) == BASE_MANIFEST_SHA256, "manifest-first base pin")
    members: dict[str, str] = {}
    for ordinal, line in enumerate(manifest.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2, f"manifest syntax:{ordinal}")
        digest, relative = pieces
        need(relative not in members and not relative.startswith("/")
             and ".." not in Path(relative).parts, f"manifest path:{ordinal}")
        need(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
             f"manifest digest:{ordinal}")
        need(file_sha(root / relative) == digest, "manifest member:" + relative)
        members[relative] = digest
    need(len(members) == 25, "manifest member count")
    receipt_relative = str((bundle / BASE_RECEIPT).relative_to(root))
    need(members[receipt_relative] == BASE_RECEIPT_FILE_SHA256, "base receipt pin")
    return members


def closed(path: Path, key: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claimed = body.pop(key, None)
    need(claimed == object_sha(body), "closure:" + path.name)
    return value


def publish(path: Path, content: bytes) -> None:
    if path.exists():
        need(path.read_bytes() == content, "append-only conflict:" + path.name)
        return
    with path.open("xb") as stream:
        stream.write(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    try:
        need(args.seed > 0, "positive seed")
        root = Path(__file__).resolve().parent.parent
        wrapper = Path(__file__).resolve()
        verifier = root / "deliverables/cm2_c27_full_union_101080_to_483232_atom_terminal_manifest_verifier_v1.py"
        bundle = args.bundle_dir.resolve()
        run = args.run_dir.resolve()
        python = args.python.resolve()
        need(bundle.parent.parent == root and not run.exists(), "fresh resolved run")
        need(file_sha(verifier) == VERIFIER_SHA256 and file_sha(python) == PYTHON_SHA256,
             "runtime/source pins")
        for name in (PUBLISHED_VERIFICATION, COLD_RECEIPT, COLD_MANIFEST):
            need(not (bundle / name).exists(), "fresh append-only output:" + name)

        members = parse_manifest(root, bundle)
        run.mkdir(parents=True, mode=0o700)
        watched: dict[str, Path] = {
            "base_manifest": bundle / BASE_MANIFEST,
            "runtime/python": python,
            "runtime/verifier": verifier,
            "runtime/wrapper": wrapper,
        }
        watched.update({"member:" + relative: root / relative for relative in members})
        pre = snapshot(watched)

        output = run / "verification.json"
        command = [
            str(python), "-I", "-S", "-B", str(verifier),
            "--bundle-dir", str(bundle),
            "--output", str(output),
            "--seed", str(args.seed),
        ]
        environment = {
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "PYTHONHASHSEED": "0",
        }
        usage_before = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.monotonic_ns()
        process = subprocess.run(
            command, cwd=root, env=environment, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
        ended = time.monotonic_ns()
        usage_after = resource.getrusage(resource.RUSAGE_CHILDREN)
        numeric_exit = process.returncode if process.returncode >= 0 else None
        signal_number = -process.returncode if process.returncode < 0 else None
        (run / "stdout.log").write_bytes(process.stdout)
        (run / "stderr.log").write_bytes(process.stderr)
        (run / "command.json").write_bytes(canonical(command) + b"\n")
        (run / "exit.json").write_bytes(canonical({
            "numeric_exit": numeric_exit, "signal": signal_number,
        }) + b"\n")
        need(numeric_exit == 0 and signal_number is None, "clean numeric exit")
        need(process.stderr == b"", "empty stderr")

        verification = closed(output, "verification_sha256")
        stdout_value = json.loads(process.stdout)
        need(stdout_value == {
            "status": verification["status"],
            "verification_sha256": verification["verification_sha256"],
        }, "stdout/output binding")
        need(verification["status"].startswith("PASS_MANIFEST_FIRST_TERMINAL_REPLAY")
             and verification["verification_seed"] == args.seed
             and verification["base_manifest_sha256"] == BASE_MANIFEST_SHA256
             and verification["formal_credit"] == 0
             and verification["manifest_authorized"] is False
             and verification["C27_C28_C29"] == "FULL_REBUILD_REQUIRED"
             and verification["Source_W_formal_remainder"] == 80
             and verification["CM2"] == "NO-GO_FOR_CLAIM"
             and verification["source_W_transition_authorized"] is False,
             "verification nonpromotion")
        post = snapshot(watched)
        need(pre == post, "pre/post SHA+stat identity")
        need(parse_manifest(root, bundle) == members, "post manifest replay")

        published_verification = bundle / PUBLISHED_VERIFICATION
        publish(published_verification, output.read_bytes())
        timing = {
            "elapsed_monotonic_ns": ended - started,
            "user_seconds": usage_after.ru_utime - usage_before.ru_utime,
            "system_seconds": usage_after.ru_stime - usage_before.ru_stime,
            "maximum_resident_set_kib": usage_after.ru_maxrss,
        }
        semantic = {
            "schema": "cm2.c27-independent.full-union-atom.postpublication-cold-terminal-replay-receipt.v1",
            "status": "PASS_COLD_POSTPUBLICATION_MANIFEST_FIRST_TERMINAL_REPLAY__PRE_POST_SHA_STAT_IDENTICAL__ZERO_CREDIT",
            "base_manifest_sha256": BASE_MANIFEST_SHA256,
            "base_manifest_member_count": len(members),
            "base_receipt_file_sha256": BASE_RECEIPT_FILE_SHA256,
            "verification_seed": args.seed,
            "verification_sha256": verification["verification_sha256"],
            "verification_file_sha256": file_sha(published_verification),
            "manifest_first_terminal_replay": True,
            "numeric_exit": numeric_exit,
            "signal": signal_number,
            "stderr_empty": True,
            "stdout_bound_to_verification": True,
            "command": command,
            "environment": environment,
            "timing": timing,
            "observed_pre_sha256": pre["sha256"],
            "observed_pre_stat": pre["stat"],
            "observed_post_sha256": post["sha256"],
            "observed_post_stat": post["stat"],
            "pre_post_sha256_identical": True,
            "pre_post_stat_identical": True,
            "python_sha256": PYTHON_SHA256,
            "verifier_sha256": VERIFIER_SHA256,
            "wrapper_sha256": pre["sha256"]["runtime/wrapper"],
            "pair_routes": 101080,
            "primitive_atoms": 483232,
            "incident_atoms": 62768,
            "exact_complement_atoms": 420464,
            "expanded_atom_route_incidences": 206632,
            "coarse_positive_incidences_removed": 184,
            "coarse_positive_atoms_corrected": 144,
            "G2B_new_incident_atoms": 528,
            "coherent_attacks_rejected": 54,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_C28_C29": "FULL_REBUILD_REQUIRED",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
            "source_W_transition_authorized": False,
            "required_next": "CONSUME_WITH_REMAINING_PRIMITIVE_TERMINAL_SUBGATES_BEFORE_ANY_C27_REBUILD_AUTHORIZATION",
        }
        receipt = {**semantic, "receipt_sha256": object_sha(semantic)}
        receipt_path = bundle / COLD_RECEIPT
        publish(receipt_path, canonical(receipt) + b"\n")
        supplement_paths = {
            str((bundle / BASE_MANIFEST).relative_to(root)): bundle / BASE_MANIFEST,
            str((bundle / BASE_RECEIPT).relative_to(root)): bundle / BASE_RECEIPT,
            str(verifier.relative_to(root)): verifier,
            str(wrapper.relative_to(root)): wrapper,
            str(published_verification.relative_to(root)): published_verification,
            str(receipt_path.relative_to(root)): receipt_path,
        }
        manifest_bytes = b"".join(
            f"{file_sha(path)}  {relative}\n".encode("ascii")
            for relative, path in sorted(supplement_paths.items())
        )
        publish(bundle / COLD_MANIFEST, manifest_bytes)
        print(canonical({
            "status": receipt["status"],
            "receipt_sha256": receipt["receipt_sha256"],
            "receipt_file_sha256": file_sha(receipt_path),
            "supplemental_manifest_sha256": file_sha(bundle / COLD_MANIFEST),
        }).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError) as error:
        print("FAIL:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
