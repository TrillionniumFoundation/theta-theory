#!/usr/bin/env python3
"""Build one fresh, persistently runnable C30c v3 receipt transaction."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
from pathlib import Path
from types import ModuleType
from typing import Any


WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
VALIDATOR = WORKSPACE / "deliverables/cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
VALIDATOR_SHA256 = "c68633b3cc996c344c737f1e6c71da382a81c8f6bf6c4318b233b6d9db34c97a"


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise BuildFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def file_sha256(path: Path) -> str:
    descriptor = os.open(
        os.fspath(path), os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                "regular singleton:" + os.fspath(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        identity = lambda item: (
            item.st_dev, item.st_ino, item.st_mode, item.st_nlink,
            item.st_size, item.st_mtime_ns, item.st_ctime_ns,
        )
        require(identity(before) == identity(after), "stable file:" + os.fspath(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def exclusive(path: Path, payload: bytes, mode: int) -> None:
    descriptor = os.open(
        os.fspath(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0), mode,
    )
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            require(written > 0, "complete exclusive write:" + os.fspath(path))
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def load_validator() -> ModuleType:
    require(file_sha256(VALIDATOR) == VALIDATOR_SHA256, "exact v3 validator bytes")
    specification = importlib.util.spec_from_file_location(
        "cm2_c30c_receipt_validator_v3_frozen", VALIDATOR,
    )
    require(specification is not None and specification.loader is not None,
            "validator import specification")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def launch_bytes(
    run: Path, control: Path, receipt: Path, pinset_sha256: str,
) -> bytes:
    return f'''#!/bin/bash
set -uo pipefail
set -C
umask 077

WORKSPACE={WORKSPACE}
RUN_DIR={run}
CONTROL_DIR={control}
RECEIPT_DIR={receipt}
PINSET="$CONTROL_DIR/pins.sha256"
RUNNER="$RUN_DIR/run.sh"
VALIDATOR={VALIDATOR}
EXPECTED_PINSET_SHA256={pinset_sha256}

cd "$WORKSPACE" || exit 125

for name in preflight-pin-check.log preflight.json preflight.stderr \\
    preflight.exit transaction-run.exit postrun-pin-check.log \\
    receipt.json receipt.stderr receipt.exit transaction-end-utc.txt; do
    if [[ -e "$RECEIPT_DIR/$name" ]]; then
        exit 124
    fi
done

OBSERVED_PINSET_SHA256=$(/usr/bin/sha256sum "$PINSET" | /usr/bin/cut -d' ' -f1)
if [[ "$OBSERVED_PINSET_SHA256" != "$EXPECTED_PINSET_SHA256" ]]; then
    exit 123
fi
/usr/bin/sha256sum --check --strict "$PINSET" \\
    > "$RECEIPT_DIR/preflight-pin-check.log" || exit 122

set +e
/usr/bin/python3 -I -B "$VALIDATOR" --self-test \\
    > "$RECEIPT_DIR/preflight.json" 2> "$RECEIPT_DIR/preflight.stderr"
PREFLIGHT_EXIT=$?
set -e
/usr/bin/printf '%s\n' "$PREFLIGHT_EXIT" > "$RECEIPT_DIR/preflight.exit"
if [[ "$PREFLIGHT_EXIT" -ne 0 || -s "$RECEIPT_DIR/preflight.stderr" ]]; then
    exit 121
fi

set +e
"$RUNNER"
RUN_EXIT=$?
set -e
/usr/bin/printf '%s\n' "$RUN_EXIT" > "$RECEIPT_DIR/transaction-run.exit"
if [[ "$RUN_EXIT" -ne 0 ]]; then
    exit "$RUN_EXIT"
fi

/usr/bin/sha256sum --check --strict "$PINSET" \\
    > "$RECEIPT_DIR/postrun-pin-check.log" || exit 120
set +e
/usr/bin/python3 -I -B "$VALIDATOR" "$RUN_DIR" \\
    > "$RECEIPT_DIR/receipt.json" 2> "$RECEIPT_DIR/receipt.stderr"
RECEIPT_EXIT=$?
set -e
/usr/bin/printf '%s\n' "$RECEIPT_EXIT" > "$RECEIPT_DIR/receipt.exit"
/usr/bin/date -u +'%Y-%m-%dT%H:%M:%SZ' \\
    > "$RECEIPT_DIR/transaction-end-utc.txt"
/usr/bin/sync -f "$RECEIPT_DIR"
if [[ "$RECEIPT_EXIT" -ne 0 || -s "$RECEIPT_DIR/receipt.stderr" ]]; then
    exit 119
fi
exit 0
'''.encode("ascii")


def build() -> dict[str, Any]:
    validator = load_validator()
    run: Path = validator.RUN
    control = WORKSPACE / ".cm2-runtime/control" / validator.RUN_NAME
    receipt = WORKSPACE / ".cm2-runtime/receipts" / validator.RUN_NAME
    require(not run.exists(), "fresh run directory")
    require(not control.exists(), "fresh control directory")
    require(not receipt.exists(), "fresh receipt directory")
    require(validator.self_test()["status"]
            == "PASS_FAIL_CLOSED_STATIC_AND_FIXTURE_PREFLIGHT",
            "builder static/fixture preflight")

    run.mkdir(parents=True, mode=0o700)
    control.mkdir(parents=True, mode=0o700)
    receipt.mkdir(parents=True, mode=0o700)
    command = validator.command_bytes()
    provenance = validator.provenance_bytes()
    runner = validator.runner_bytes()
    exclusive(run / "command.txt", command, 0o400)
    exclusive(run / "provenance.json", provenance, 0o400)
    exclusive(run / "run.sh", runner, 0o500)

    paths = [validator.PYTHON, validator.HARNESS, validator.VERIFIER, VALIDATOR]
    paths.extend((run / name) for name in ("command.txt", "provenance.json", "run.sh"))
    paths.extend(validator.CANDIDATE / name for name in sorted(validator.CANDIDATE_HASHES))
    hashes: dict[str, str] = {}
    for path in paths:
        if path == validator.PYTHON:
            value, _target, _link = validator.python_hash()
        else:
            value = file_sha256(path)
        hashes[os.fspath(path)] = value
    require(len(hashes) == 13, "exact 13 pin members")
    pinset = b"".join(
        f"{value}  {path}\n".encode("utf-8")
        for path, value in sorted(hashes.items())
    )
    exclusive(control / "pins.sha256", pinset, 0o400)
    pinset_sha = hashlib.sha256(pinset).hexdigest()
    launch = launch_bytes(run, control, receipt, pinset_sha)
    exclusive(control / "launch.sh", launch, 0o500)

    result = {
        "schema": "cm2.c30c.receipted-transaction-v3-build.v1",
        "status": "PASS_FRESH_FAIL_CLOSED_TRANSACTION_BUILT_NOT_YET_RUN",
        "run_name": validator.RUN_NAME,
        "run_directory": os.fspath(run.relative_to(WORKSPACE)),
        "control_directory": os.fspath(control.relative_to(WORKSPACE)),
        "receipt_directory": os.fspath(receipt.relative_to(WORKSPACE)),
        "validator_sha256": VALIDATOR_SHA256,
        "command_sha256": hashlib.sha256(command).hexdigest(),
        "provenance_sha256": hashlib.sha256(provenance).hexdigest(),
        "runner_sha256": hashlib.sha256(runner).hexdigest(),
        "pinset_sha256": pinset_sha,
        "launcher_sha256": hashlib.sha256(launch).hexdigest(),
        "pin_member_count": len(hashes),
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "downstream_publication_authorized": False,
    }
    exclusive(receipt / "build.json", canonical(result) + b"\n", 0o400)
    for path in (run, control, receipt):
        fsync_directory(path)
    return result


def main() -> int:
    try:
        result = build()
    except (BuildFailure, OSError, ValueError, KeyError, TypeError) as error:
        print("FAIL_C30C_TRANSACTION_V3_BUILD:" + str(error))
        return 2
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
