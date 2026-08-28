#!/usr/bin/env python3
"""Fail-closed verifier for the round-33 safe F9/F10 subatlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round33_safe_f9_f10_subatlas_cert as cert


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
        matrix = manifest["result"]["five_face_kind_matrix"]
        if sum(row["F9"].startswith("CERTIFIED") for row in matrix.values()) != 1:
            errors.append("F9 matrix")
        if sum(row["F10"].startswith("CERTIFIED") for row in matrix.values()) != 2:
            errors.append("F10 matrix")
        if manifest["result"]["strict_nonpromotion"]["Gate5_maturity"] != "6/18_UNCHANGED":
            errors.append("maturity")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    paths = [
        ("stationary_source_core_subatlas", "physical_face_count", 95),
        ("stationary_source_core_subatlas", "F9_face_C2_atlas_bound", "4949"),
        ("stationary_source_core_subatlas", "collision_trace_measure_declared_zero", True),
        ("moving_occurrence_F10_subatlas", "positive_density_wrt_source_normal_angle_upper", "19/5"),
        ("moving_occurrence_F10_subatlas", "reverse_density_derivative_wrt_normal_angle", "<(4373/125)*2^B"),
        ("moving_occurrence_F10_subatlas", "F9_physical_face_C2_from_carrier_4949", "CERTIFIED"),
    ]
    for section, key, value in paths:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_matrix"]["terminal_core_preimage_face"]["F9"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["complete_F10_all_face_coarea_regular_atlas"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate5_maturity"] = "8/18"
    mutation["verdict"]["Gate5_maturity"] = "8/18"
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
