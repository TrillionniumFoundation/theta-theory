#!/usr/bin/env python3
"""Fail-closed verifier for the round-36 all-face F9 certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round36_all_face_rank_path_f9_cert as cert


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


def independent_pullback(
    ranks: list[int], gradient_upper: int, hessian_upper: int
) -> tuple[int, int, int, int, Q]:
    derivative = 1
    inverse_derivative = 1
    prefix_hessian = 0
    for rank in ranks:
        if type(rank) is not int or rank < 14:
            raise ValueError("rank")
        one_derivative = 150 * (1 << rank)
        one_hessian = 42672 * (1 << (3 * rank))
        prefix_hessian = (
            one_hessian * derivative * derivative
            + one_derivative * prefix_hessian
        )
        derivative *= one_derivative
        inverse_derivative *= one_derivative
    face_hessian = (
        hessian_upper * derivative * derivative
        + gradient_upper * prefix_hessian
    )
    curvature = Q(3, 2) * inverse_derivative * face_hessian
    return derivative, inverse_derivative, prefix_hessian, face_hessian, curvature


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
        base = result["base_physical_face_geometry"]
        if base["global_circle_tangency_face"]["graph_C2_strict_upper"] != "4949":
            errors.append("tangency C2")
        if base["selected_64_moving_occurrence_face"]["graph_C2_strict_upper"] != "623":
            errors.append("moving C2")
        if base["forward_integer_corner_face"]["graph_C2_strict_upper"] != "21":
            errors.append("corner C2")
        kinds = result["seven_one_step_boundary_kind_F9_join"]["rows"]
        if len(kinds) != 7 or len({row["type"] for row in kinds}) != 7:
            errors.append("seven kinds")
        if not all(
            row["arbitrary_regular_prefix_pullback_F9"]
            == "CERTIFIED_BY_RANK_PATH_CHAIN_RULE"
            for row in kinds
        ):
            errors.append("kind pullbacks")

        samples = result["general_base_face_rank_path_recurrence"]["sample_replays"]
        if len(samples) != 5:
            errors.append("sample count")
        for row in samples:
            values = independent_pullback(
                row["rank_path"],
                row["base_gradient_l1_upper"],
                row["base_Hessian_operator_upper"],
            )
            if row["prefix_D_infinity_strict_upper"] != str(values[0]):
                errors.append("sample D")
            if row["prefix_inverse_D_infinity_strict_upper"] != str(values[1]):
                errors.append("sample E")
            if row["prefix_D2_infinity_strict_upper"] != str(values[2]):
                errors.append("sample H")
            if row["pullback_Hessian_operator_strict_upper"] != str(values[3]):
                errors.append("sample face Hessian")
            if row["unit_speed_face_C2_seminorm_strict_upper"] != str(values[4]):
                errors.append("sample face C2")

        matrix = result["five_face_kind_matrix"]
        if sum(row["F9"].startswith("CERTIFIED") for row in matrix.values()) != 5:
            errors.append("F9 matrix")
        if sum(row["F10"].startswith("CERTIFIED") for row in matrix.values()) != 2:
            errors.append("F10 matrix")
        scope = result["strict_nonpromotion"]
        if scope["complete_F9_physical_face_C2_parameterized_atlas"] != "CERTIFIED":
            errors.append("F9 completion")
        if scope["rank_path_values_are_uniform_in_depth_or_rank"] is not False:
            errors.append("uniformity nonpromotion")
        if scope["complete_F10_all_face_coarea_regular_atlas"] != "NOT_CERTIFIED":
            errors.append("F10 nonpromotion")
        if scope["Gate5_maturity"] != "7/18":
            errors.append("maturity")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("base_physical_face_geometry", "global_distinct_disk_boundary_gap_strict_lower", "1"),
        ("Gate5_maturity_update", "current_global_maturity", "8/18"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    nested_edits = [
        ("global_circle_tangency_face", "graph_C2_strict_upper", "623"),
        ("selected_64_moving_occurrence_face", "graph_C2_strict_upper", "4949"),
        ("forward_integer_corner_face", "uniform_corner_ray_length_strict_lower", "0"),
        ("forward_integer_corner_face", "graph_C2_strict_upper", "4949"),
    ]
    for section, key, value in nested_edits:
        mutation = copy.deepcopy(source)
        mutation["result"]["base_physical_face_geometry"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["seven_one_step_boundary_kind_F9_join"]["rows"].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["seven_one_step_boundary_kind_F9_join"]["rows"][0][
        "base_Hessian_upper"
    ] = 0
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["general_base_face_rank_path_recurrence"]["sample_replays"][2][
        "pullback_Hessian_operator_strict_upper"
    ] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_matrix"][
        "collision_singularity_or_owner_change_face"
    ]["F9"] = "NOT_CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_matrix"]["moving_occurrence_face"][
        "F10"
    ] = "CERTIFIED_ALL_PULLBACKS"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "rank_path_values_are_uniform_in_depth_or_rank"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "complete_F10_all_face_coarea_regular_atlas"
    ] = "CERTIFIED"
    mutation["verdict"]["complete_F10_all_face_coarea_regular_atlas"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate5"] = "CERTIFIED"
    mutation["verdict"]["Gate5"] = "CERTIFIED"
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
