#!/usr/bin/env python3
"""Fail-closed verifier for the round-33 2026 small-hole audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate134_round33_2026_small_hole_interface_cert as cert


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
        matrix = manifest["result"]["exact_interface_matrix"]
        if not matrix["single_full_angle_boundary_strip_H_t"].startswith("MISMATCH"):
            errors.append("shape mismatch")
        if manifest["verdict"]["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("verdict")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations = []
    for gate in ("Gate1", "Gate2", "Gate3", "Gate4"):
        value = copy.deepcopy(source)
        value["result"]["strict_nonpromotion"][gate] = "CERTIFIED"
        value["verdict"][gate] = "CERTIFIED"
        mutations.append(value)
    value = copy.deepcopy(source)
    value["result"]["exact_interface_matrix"]["single_full_angle_boundary_strip_H_t"] = "MATCH"
    mutations.append(value)
    value = copy.deepcopy(source)
    value["result"]["exact_interface_matrix"]["unnormalized_recovered_cone_hit_lower"] = "CERTIFIED"
    mutations.append(value)
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
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    print("VERIFY: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
