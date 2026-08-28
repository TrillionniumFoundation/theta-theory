#!/usr/bin/env python3
"""Create the fresh canonical-provenance C30c 62-case run transaction."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T1325-canonical-v2"
RUN = ROOT / ".cm2-runtime/audit" / RUN_NAME
PYTHON = ROOT / ".cm2-runtime/python-flint-0.9.0/bin/python"
HARNESS = ROOT / "deliverables/cm2_round306c30c_source_w_full_delta_whole_origin_disposition_attack_harness.py"
VERIFIER = ROOT / "deliverables/cm2_round306c30c_source_w_full_delta_whole_origin_disposition_independent_verifier.py"
CANDIDATE = ROOT / ".cm2-runtime/candidates/c30c-v4-seed-30630071"
OLD_COMMAND = ROOT / ".cm2-runtime/audit/c30c-v5-toctou-robustness-rerun-20260807T1012-final/command.txt"
EXPECTED = {
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "harness": "9f0b72a81098333c3f0b76d7191f48855d608b0aa1e405bdf72cb10532e825c8",
    "verifier": "0fd82ce16053b69cbb04eddc423cb3f4b8cf8d11923219b50e6ff659f97b7377",
    "command": "7875414533ecafbd270a8bad128ebcfc30af28f6008e3ac85270ccf9f38137eb",
}
CANDIDATE_HASHES = {
    "cm2_round306c30b_python_flint_runtime_attestation.json": "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_combined_boundary_atomic_owner_join_ledger.jsonl.gz": "63f004bdb065d8674ecfde9eb957f3477ee6c3f806064ef8f151850cd391d251",
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_delta_h_cell_ledger.jsonl.gz": "acbd71e9155d81d17ae4b42eecd31f0fc9d4bb91ac36aa93a7ab7df08e3dee50",
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_inherited_h_cell_ledger.jsonl.gz": "d4142d7748e0546184542bea7b3b337c9f33e7312efa2e7c5271d2a9dba30abd",
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_result.json": "96c1e9f627bd6113fc56f7b6d35856581b57b4afde049e997b10eef3f8c706f1",
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_whole_origin_ledger.jsonl.gz": "48a3e612de84004ba746d93d492e8f3e9f587ebf6b3574615fa946dddf21a573",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def exclusive(path: Path, payload: bytes, mode: int = 0o600) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build() -> dict[str, Any]:
    need(not RUN.exists(), "fresh run directory")
    need(PYTHON.resolve(strict=True) == Path("/usr/bin/python3.12"),
         "controlled Python target")
    need(fsha(PYTHON) == EXPECTED["python"]
         and fsha(HARNESS) == EXPECTED["harness"]
         and fsha(VERIFIER) == EXPECTED["verifier"], "pinned executable inputs")
    command = OLD_COMMAND.read_bytes()
    need(command.endswith(b"\n") and sha256(command) == EXPECTED["command"],
         "pinned command bytes")
    observed = {name: fsha(CANDIDATE / name)
                for name in sorted(CANDIDATE_HASHES)}
    need(observed == CANDIDATE_HASHES
         and {entry.name for entry in os.scandir(CANDIDATE)}
             == set(CANDIDATE_HASHES), "exact pinned candidate six")
    provenance = {
        "candidate_directory": ".cm2-runtime/candidates/c30c-v4-seed-30630071",
        "candidate_file_sha256": CANDIDATE_HASHES,
        "command_bytes_without_final_newline_sha256":
            sha256(command.removesuffix(b"\n")),
        "formal_credit": 0,
        "harness_sha256": EXPECTED["harness"],
        "intended_start_utc": "2026-08-07T02:12:24Z",
        "purpose": "C30c candidate-only exact 62-case mathematical artifact integrity rerun",
        "python_executable_sha256": EXPECTED["python"],
        "schema": "cm2.c30c.robustness-rerun-provenance.v1",
        "verifier_sha256": EXPECTED["verifier"],
        "zero_credit_until_formal_prerequisites_exist": True,
    }
    provenance_raw = canonical(provenance) + b"\n"
    run_script = f'''#!/bin/bash
set -u

WORKSPACE={ROOT}
RUN_DIR="$WORKSPACE/.cm2-runtime/audit/{RUN_NAME}"
PYTHON="$WORKSPACE/.cm2-runtime/python-flint-0.9.0/bin/python"
HARNESS="$WORKSPACE/deliverables/cm2_round306c30c_source_w_full_delta_whole_origin_disposition_attack_harness.py"
VERIFIER="$WORKSPACE/deliverables/cm2_round306c30c_source_w_full_delta_whole_origin_disposition_independent_verifier.py"
CANDIDATE="$WORKSPACE/.cm2-runtime/candidates/c30c-v4-seed-30630071"

cd "$WORKSPACE" || exit 125
umask 077

for name in stdout.json stderr.log time.txt exit_code.txt end_utc.txt; do
    if [[ -e "$RUN_DIR/$name" ]]; then
        exit 124
    fi
done

/usr/bin/date -u +'%Y-%m-%dT%H:%M:%SZ' > "$RUN_DIR/start_utc.txt"
/usr/bin/printf '%s\n' "$$" > "$RUN_DIR/wrapper_pid.txt"
/usr/bin/sha256sum \
    "$PYTHON" "$HARNESS" "$VERIFIER" "$RUN_DIR/command.txt" \
    "$RUN_DIR/provenance.json" "$RUN_DIR/run.sh" \
    "$CANDIDATE"/* > "$RUN_DIR/pre.sha256"
/usr/bin/stat -c '%n|dev=%d|ino=%i|mode=%f|links=%h|size=%s|mtime=%Y|ctime=%Z' \
    "$PYTHON" "$HARNESS" "$VERIFIER" "$CANDIDATE" "$CANDIDATE"/* \
    > "$RUN_DIR/pre.stat"

/usr/bin/time --verbose --output="$RUN_DIR/time.txt" -- \
    /usr/bin/env -i HOME=/nonexistent LC_ALL=C.UTF-8 TZ=UTC \
    PYTHONHASHSEED=30630071 \
    "$PYTHON" -I -B "$HARNESS" "$CANDIDATE" \
    > "$RUN_DIR/stdout.json" 2> "$RUN_DIR/stderr.log" &
TIME_PID=$!
/usr/bin/printf '%s\n' "$TIME_PID" > "$RUN_DIR/time_pid.txt"

for _attempt in $(/usr/bin/seq 1 200); do
    if [[ -r "/proc/$TIME_PID/task/$TIME_PID/children" ]]; then
        read -r CHILDREN < "/proc/$TIME_PID/task/$TIME_PID/children" || true
        if [[ -n "${{CHILDREN:-}}" ]]; then
            /usr/bin/printf '%s\n' "$CHILDREN" > "$RUN_DIR/observed_child_pids.txt"
            break
        fi
    fi
    /usr/bin/sleep 0.05
done

wait "$TIME_PID"
RUN_EXIT=$?
/usr/bin/printf '%s\n' "$RUN_EXIT" > "$RUN_DIR/exit_code.txt"
/usr/bin/date -u +'%Y-%m-%dT%H:%M:%SZ' > "$RUN_DIR/end_utc.txt"
/usr/bin/sha256sum \
    "$PYTHON" "$HARNESS" "$VERIFIER" "$RUN_DIR/command.txt" \
    "$RUN_DIR/provenance.json" "$RUN_DIR/run.sh" \
    "$CANDIDATE"/* > "$RUN_DIR/post.sha256"
/usr/bin/stat -c '%n|dev=%d|ino=%i|mode=%f|links=%h|size=%s|mtime=%Y|ctime=%Z' \
    "$PYTHON" "$HARNESS" "$VERIFIER" "$CANDIDATE" "$CANDIDATE"/* \
    > "$RUN_DIR/post.stat"
/usr/bin/sync -f "$RUN_DIR"
exit "$RUN_EXIT"
'''.encode("ascii")
    RUN.mkdir(parents=True, mode=0o700)
    exclusive(RUN / "command.txt", command)
    exclusive(RUN / "provenance.json", provenance_raw)
    exclusive(RUN / "run.sh", run_script, 0o700)
    directory = os.open(RUN, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return {
        "schema": "cm2.c30c.canonical-receipted-run-v2-build.v1",
        "run_name": RUN_NAME,
        "command_sha256": sha256(command),
        "provenance_sha256": sha256(provenance_raw),
        "runner_sha256": sha256(run_script),
        "canonical_provenance": True,
        "formal_credit": 0,
    }


def main() -> int:
    try:
        result = build()
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
