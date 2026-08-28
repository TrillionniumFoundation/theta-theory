#!/usr/bin/env python3
"""Terminal root/payload replay for the scoped C26 zero-credit receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def replay_manifest(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="ascii").splitlines():
        claimed, relative = line.split("  ", 1)
        target = ROOT / relative
        need(target.is_file() and file_sha(target) == claimed, "manifest member:" + relative)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    seal = Path(args.seal_dir).resolve()
    output = Path(args.output_dir).resolve()
    need(not output.exists(), "new output dir")
    root = seal / "root_manifest.sha256"
    payload = seal / "payload_manifest.sha256"
    receipt_path = seal / "receipt.json"
    root_count = replay_manifest(root)
    payload_count = replay_manifest(payload)
    receipt = json.loads(receipt_path.read_bytes())
    body = dict(receipt)
    claimed = body.pop("receipt_sha256", None)
    need(claimed == digest(body), "receipt closure")
    need(receipt["status"].startswith("PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS"), "receipt status")
    need(receipt["authority_scope"]["fills_v5_C26_absence_slot"] is True and receipt["authority_scope"]["twenty_family_gate_closed_by_this_receipt"] is False, "scope boundary")
    need(receipt["formal_credit"] == 0 and receipt["manifest_authorized"] is False and receipt["source_W_transition_authorized"] is False, "zero credit")
    output.mkdir(parents=True)
    replay = {
        "schema": "cm2.c26-independent.no-new-geometry-from-c26-feature-rows-terminal-replay.v1",
        "status": "PASS_ROOT_PAYLOAD_AND_SCOPED_RECEIPT_REPLAY__V5_C26_ABSENCE_SLOT_CLOSED__TWENTY_FAMILY_GATE_OPEN__ZERO_CREDIT",
        "root_manifest_file_sha256": file_sha(root),
        "root_manifest_entry_count": root_count,
        "payload_manifest_file_sha256": file_sha(payload),
        "payload_manifest_entry_count": payload_count,
        "receipt_file_sha256": file_sha(receipt_path),
        "receipt_sha256": receipt["receipt_sha256"],
        "NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS": True,
        "twenty_family_gate_closed": False,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    replay["result_sha256"] = digest(replay)
    (output / "terminal_replay.json").write_bytes(canonical(replay) + b"\n")
    print(canonical({"status": replay["status"], "result_sha256": replay["result_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
