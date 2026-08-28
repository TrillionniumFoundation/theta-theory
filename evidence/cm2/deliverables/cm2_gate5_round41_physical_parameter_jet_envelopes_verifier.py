#!/usr/bin/env python3
"""Fail-closed verifier for Round-41 physical parameter jets."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round41_physical_parameter_jet_envelopes_cert as cert


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
        majorant = result["ray_circle_parameter_majorant"]
        if majorant["majorant_status"] != (
            "CERTIFIED_BY_EXACT_RATIONAL_RAY_CIRCLE_CALCULUS"
        ):
            errors.append("majorant status")
        geometry = majorant["geometry_bounds"]
        if geometry["one_state_derivative_of_transverse_offset_upper"] != "22":
            errors.append("transverse derivative")
        normal = majorant["target_normal_angle"]
        if normal["mixed_parameter_upper"] != "155625/(8*c^3)":
            errors.append("mixed bound")
        if normal["mixed_majorant_strictly_below_20000"] is not True:
            errors.append("mixed majorant")
        if normal["second_majorant_strictly_below_40"] is not True:
            errors.append("second majorant")

        jets = result["physical_rank_indexed_step_jets"]
        if jets["cross_colour_step_jets"] != [
            "U(B)=20*2^B",
            "V(B)=20000*2^(3B)",
            "W(B)=40*2^(3B)",
        ]:
            errors.append("rank jets")
        if jets["rank_exponents"] != {"U": 1, "V": 3, "W": 3}:
            errors.append("rank exponents")
        for key in (
            "physical_rank_indexed_U_B_materialized",
            "physical_rank_indexed_V_B_materialized",
            "physical_rank_indexed_W_B_materialized",
        ):
            if jets[key] is not True:
                errors.append(key)
        expected_samples = []
        for rank in (14, 16, 20):
            expected_samples.append(
                {
                    "B": rank,
                    "U": str(20 * (1 << rank)),
                    "V": str(20000 * (1 << (3 * rank))),
                    "W": str(40 * (1 << (3 * rank))),
                }
            )
        if jets["sample_rows"] != expected_samples:
            errors.append("sample rows")

        faces = result["all_face_base_parameter_jets"]
        tangent = faces["tangency_raw_level_exact_bounds"]
        if tangent != {
            "abs_G_s_strict_upper": "18/25",
            "abs_G_xs_strict_upper": "97/2",
            "abs_G_ss_upper": "2",
        }:
            errors.append("tangency jets")
        rows = faces["seven_boundary_kind_rows"]
        if len(rows) != 7 or len({row["type"] for row in rows}) != 7:
            errors.append("seven kinds")
        if faces["all_five_physical_face_base_parameter_jets"] != "CERTIFIED":
            errors.append("five faces")

        frontier = result["physical_summability_frontier"]
        model = frontier["logical_countermodel"]
        if model["law"] != "P(B=b0+2k)=(15/16)*16^-k, k>=0":
            errors.append("countermodel law")
        if model["2_to_3B_over_2_moment"] != (
            "finite geometric series with ratio 1/2"
        ):
            errors.append("finite moment")
        if model["2_to_3B_moment"] != (
            "divergent geometric series with ratio 4"
        ):
            errors.append("divergent moment")
        prefix = model["finite_prefix_rows"]
        if prefix[-1]["shell_prefix_count"] != 16:
            errors.append("countermodel prefix")
        if frontier["existing_rank_moment_implies_V_W_L1"] is not False:
            errors.append("moment overclaim")
        if frontier["same_law_full_path_moment"] != "NOT_CERTIFIED":
            errors.append("path moment")

        scope = result["strict_nonpromotion"]
        if scope["rank_indexed_physical_U_V_W"] != "CERTIFIED":
            errors.append("U V W verdict")
        if scope["all_five_face_base_parameter_jets"] != "CERTIFIED":
            errors.append("face verdict")
        if scope["arbitrary_Rn_pullback_F10_field"] != "NOT_CERTIFIED":
            errors.append("F10 scope")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
        if scope["Gate5"] != "NOT_CERTIFIED":
            errors.append("Gate5")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("ray_circle_parameter_majorant", "majorant_status", "NOT_CERTIFIED"),
        ("physical_rank_indexed_step_jets", "same_colour_step_jets", "NONZERO"),
        ("physical_rank_indexed_step_jets", "cross_colour_step_jets", ["U=1"]),
        ("physical_rank_indexed_step_jets", "rank_exponents", {"U": 1, "V": 2, "W": 2}),
        ("physical_rank_indexed_step_jets", "physical_rank_indexed_U_B_materialized", False),
        ("physical_rank_indexed_step_jets", "physical_rank_indexed_V_B_materialized", False),
        ("physical_rank_indexed_step_jets", "physical_rank_indexed_W_B_materialized", False),
        ("all_face_base_parameter_jets", "all_five_physical_face_base_parameter_jets", "NOT_CERTIFIED"),
        ("physical_summability_frontier", "existing_rank_moment_implies_V_W_L1", True),
        ("physical_summability_frontier", "existing_occurrence_seed_L3over2_propagates_through_paths", True),
        ("physical_summability_frontier", "same_law_full_path_moment", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["ray_circle_parameter_majorant"]["geometry_bounds"][
        "one_state_derivative_of_transverse_offset_upper"
    ] = "21"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["ray_circle_parameter_majorant"]["target_normal_angle"][
        "mixed_parameter_upper"
    ] = "100/c"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["physical_rank_indexed_step_jets"]["sample_rows"][0]["V"] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["all_face_base_parameter_jets"]["tangency_raw_level_exact_bounds"][
        "abs_G_xs_strict_upper"
    ] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["all_face_base_parameter_jets"]["seven_boundary_kind_rows"].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["physical_summability_frontier"]["logical_countermodel"][
        "2_to_3B_moment"
    ] = "finite"
    mutations.append(mutation)
    for key, value in (
        ("same_law_full_path_D_H_P_Q_S_moment", "CERTIFIED"),
        ("arbitrary_Rn_pullback_F10_field", "CERTIFIED"),
        ("complete_all_face_F10_field", "CERTIFIED"),
        ("Gate5_maturity", "8/18"),
        ("complete_18_field_operator_block_count", 1),
        ("Gate5", "CERTIFIED"),
        ("complete_composite_gates", "1/5"),
        ("CM2", "GO"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = value
        mutation["verdict"][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["verifier_sha256"] = "0" * 64
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
