#!/usr/bin/env python3
"""Terminal manifest replay for the sealed C27R2 actual-v5 truthful REJECT."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json")


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def manifest(path: Path, base: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        sha, rel = line.split("  ", 1)
        target = (base / rel).resolve()
        need(target.is_relative_to(base.resolve()) and target.is_file(),
             "manifest target:" + rel)
        need(fsha(target) == sha, "manifest hash:" + rel)
        count += 1
    return count


def write_new(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=False)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    seal = Path(args.seal_dir).resolve()
    try:
        need(seal.is_relative_to(WORKSPACE), "seal workspace-bound")
        need(not ACTUAL.exists(), "actual receipt appeared before reject terminal replay")
        payload_manifest = seal / "payload_manifest.sha256"
        root_manifest = seal / "root_manifest.sha256"
        receipt_path = seal / "receipt.json"
        payload_count = manifest(payload_manifest, WORKSPACE)
        root_count = manifest(root_manifest, seal)
        raw = receipt_path.read_bytes()
        need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single receipt")
        receipt = json.loads(raw[:-1])
        need(type(receipt) is dict and canonical(receipt) == raw[:-1], "canonical receipt")
        body = dict(receipt)
        claimed = body.pop("receipt_sha256", None)
        need(type(claimed) is str and claimed == digest(body), "receipt closure")
        need(receipt.get("status") ==
             "PASS_SEALED_TRUTHFUL_REJECT_LOCKED_ACTUAL_INTERFACE_VERIFIER_AND_41_ATTACKS__ZERO_CREDIT"
             and receipt.get("formal_credit") == 0
             and receipt.get("manifest_authorized") is False
             and receipt.get("fresh_C27R2_producer_may_start") is False,
             "receipt nonpromotion")
        need(receipt.get("preflight_execution") == {
            **receipt["preflight_execution"], "numeric_exit": 2, "signal": None,
            "stderr_empty": True, "truthful_reject": True,
        }, "truthful reject receipt")
        need(receipt.get("coherent_attacks", {}).get("attack_count") == 41
             and receipt["coherent_attacks"].get("accepted") == 0,
             "41 attacks")
        need(receipt.get("payload_manifest", {}).get("entry_count") == payload_count
             and receipt["payload_manifest"].get("file_sha256") == fsha(payload_manifest),
             "payload manifest receipt bind")
        need(root_count == 2, "root manifest count")
        result = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight-terminal-replay.v1",
            "status": "PASS_TERMINAL_REPLAY_TRUTHFUL_REJECT_MANIFESTS_AND_41_ATTACKS__ZERO_CREDIT",
            "seal_receipt_file_sha256": fsha(receipt_path),
            "seal_receipt_object_sha256": claimed,
            "payload_manifest_file_sha256": fsha(payload_manifest),
            "payload_manifest_entry_count": payload_count,
            "root_manifest_file_sha256": fsha(root_manifest),
            "root_manifest_entry_count": root_count,
            "actual_gate_receipt_still_absent": True,
            "fresh_C27R2_producer_may_start": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_transition_totality": "UNAUTHORIZED",
            "C28_pair_routing": "UNAUTHORIZED",
            "C29_physical_maximality": "UNAUTHORIZED",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result["terminal_replay_sha256"] = digest(result)
        write_new(Path(args.output), result)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "terminal_replay_sha256": result["terminal_replay_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
