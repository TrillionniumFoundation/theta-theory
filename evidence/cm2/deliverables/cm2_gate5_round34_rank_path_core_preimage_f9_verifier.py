#!/usr/bin/env python3
"""Fail-closed verifier for the round-34 rank-path core-preimage F9 leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round34_rank_path_core_preimage_f9_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in rows:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_path_bounds(ranks: list[int]) -> tuple[int, int, int, Q]:
    derivative = 1
    inverse_derivative = 1
    hessian = 0
    for rank in ranks:
        if type(rank) is not int or rank < 14:
            raise ValueError("rank")
        one_derivative = 150 * (1 << rank)
        one_hessian = 42672 * (1 << (3 * rank))
        hessian = one_hessian * derivative * derivative + one_derivative * hessian
        derivative *= one_derivative
        inverse_derivative *= one_derivative
    return derivative, inverse_derivative, hessian, Q(3, 2) * inverse_derivative * hessian


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if set(manifest) != {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        }:
            errors.append("top-level keys")
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        expected = cert.build_result()
        if manifest.get("result") != expected:
            errors.append("result")
        if manifest.get("verdict") != expected["strict_nonpromotion"]:
            errors.append("verdict")

        result = manifest["result"]
        samples = result["arbitrary_time_composition_recurrence"][
            "sample_rank_path_replays"
        ]
        if len(samples) != 5:
            errors.append("sample count")
        for row in samples:
            derivative, inverse_derivative, hessian, curvature = independent_path_bounds(
                row["rank_path"]
            )
            if row["prefix_D_infinity_strict_upper"] != str(derivative):
                errors.append("sample derivative")
            if row["prefix_inverse_D_infinity_strict_upper"] != str(inverse_derivative):
                errors.append("sample inverse")
            if row["prefix_D2_infinity_strict_upper"] != str(hessian):
                errors.append("sample Hessian")
            if row["unit_speed_face_C2_seminorm_strict_upper"] != str(curvature):
                errors.append("sample curvature")
        matrix = result["five_face_kind_matrix"]
        if sum(row["F9"].startswith("CERTIFIED") for row in matrix.values()) != 3:
            errors.append("F9 matrix")
        if sum(row["F10"].startswith("CERTIFIED") for row in matrix.values()) != 2:
            errors.append("F10 matrix")
        scope = result["strict_nonpromotion"]
        if scope["rank_path_template_is_complete_instantiated_face_atlas"] is not False:
            errors.append("atlas nonpromotion")
        if scope["Gate5_maturity"] != "6/18_UNCHANGED":
            errors.append("maturity")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("stationary_C24_affine_level_functions", "stationary_core_face_count", 95),
        ("stationary_C24_affine_level_functions", "base_level_Hessian", "4949"),
        ("ranked_one_collision_C2_envelope", "D2_infinity_strict_upper", "M(B)=4949"),
        ("ranked_one_collision_C2_envelope", "valid_only_off_collision_singularities_and_owner_changes", False),
        ("arbitrary_time_composition_recurrence", "gradient_lower", "||dF_j||_1>1"),
        ("arbitrary_time_composition_recurrence", "unit_speed_C2_bound", "curvature<4949"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["arbitrary_time_composition_recurrence"][
        "sample_rank_path_replays"
    ][2]["prefix_D2_infinity_strict_upper"] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_matrix"][
        "collision_singularity_or_owner_change_face"
    ]["F9"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_matrix"]["moving_occurrence_face"][
        "F9"
    ] = "CERTIFIED_FROM_CARRIER_4949"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "rank_path_template_is_complete_instantiated_face_atlas"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "complete_F9_physical_face_C2_atlas"
    ] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate5_maturity"] = "7/18"
    mutation["verdict"]["Gate5_maturity"] = "7/18"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["dependencies"] = {}
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
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
