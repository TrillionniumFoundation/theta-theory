#!/usr/bin/env python3
"""Fail-closed verifier for the round-33 time-three depth-six ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate34_round33_time3_depth6_adaptive_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in rows:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


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
            errors.append("dependencies")
        if manifest.get("result") != cert.build_result():
            errors.append("result")
        ledger = manifest["result"]["time3_depth6_ledger"]
        if sum(ledger["terminal_depth_histogram"].values()) != ledger["terminal_leaf_count"]:
            errors.append("depth count")
        if sum(ledger["terminal_blocker_histogram"].values()) != ledger["terminal_unresolved_count"]:
            errors.append("blocker count")
        if ledger["terminal_Q3_inner_count"] - 244704 != ledger["Q3_gain_over_round31_depth4"]:
            errors.append("Q3 gain")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("terminal_Q3_inner_count", 965361),
        ("terminal_unresolved_count", 4260097),
        ("Q3_coordinate_base_mass", "43469814/163840000000"),
        ("unresolved_coordinate_base_mass", "24955950/32768000000"),
        ("depth6_over_depth4_unresolved_mass_ratio", "1"),
    ]
    for key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"]["time3_depth6_ledger"][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["time3_depth6_ledger"]["terminal_depth_histogram"]["6"] -= 1
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["time3_depth6_ledger"]["terminal_blocker_histogram"]["unresolved_competitor:unresolved_discriminant"] -= 1
    mutations.append(mutation)
    for gate in ("Gate3", "Gate4"):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][gate] = "CERTIFIED"
        mutation["verdict"][gate] = "CERTIFIED"
        mutations.append(mutation)
    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            target = Path(directory) / f"mutation-{index}.json"
            target.write_text(json.dumps(mutation), encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


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
    if args.replay:
        cert.replay(args.workers)
        print("VERIFY: PASS")
        return 0
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    print("VERIFY: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
