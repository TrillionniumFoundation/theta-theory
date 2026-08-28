#!/usr/bin/env python3
"""Fail-closed verifier for the round-30 time-three depth-two ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round30_time3_depth2_adaptive_cert as cert


class DuplicateKeyError(ValueError):
    pass


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in rows:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependency ledger")
        cert.verify_dependencies()
        result = manifest.get("result")
        if result != cert.frozen_result():
            errors.append("frozen result")
        ledger = result["time3_depth2_ledger"]
        if sum(ledger["terminal_depth_histogram"].values()) != ledger["terminal_leaf_count"]:
            errors.append("depth count")
        if sum(ledger["terminal_blocker_histogram"].values()) != ledger["terminal_unresolved_count"]:
            errors.append("blocker count")
        if Q(ledger["Q3_coordinate_base_mass"]) + Q(ledger["R3_coordinate_base_mass"]) + Q(ledger["unresolved_coordinate_base_mass"]) != Q(ledger["total_Q2_coordinate_base_mass"]):
            errors.append("mass")
        if result["strict_nonpromotion"]["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2 fail-close")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> None:
    manifest = load(path)
    manifest["result"]["time3_depth2_ledger"]["terminal_Q3_inner_count"] += 1
    temporary = path.with_suffix(".mutation.json")
    temporary.write_text(json.dumps(manifest), encoding="utf-8")
    try:
        if not verify(temporary):
            raise RuntimeError("mutation accepted")
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        self_test(args.manifest)
    if args.replay:
        cert.replay(args.workers)
    print("VERIFY: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if (args.self_test or args.replay) else 2


if __name__ == "__main__":
    raise SystemExit(main())
