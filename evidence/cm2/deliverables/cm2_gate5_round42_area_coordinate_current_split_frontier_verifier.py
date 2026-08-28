#!/usr/bin/env python3
"""Fail-closed verifier for the Round-42 F10 area-coordinate frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round42_area_coordinate_current_split_frontier_cert as cert


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
        area = result["canonical_area_coordinate_split"]
        if area["collision_SRB_area_form"] != "R*cos(phi)*dr*dphi=R*dr*dp":
            errors.append("area form")
        if area["ray_circle_target_momentum"] != "p_1=w/R_1":
            errors.append("momentum coordinate")
        bounds = area["target_momentum_parameter_bounds"]
        if bounds != {
            "abs_partial_s_p1": "<=25/4",
            "partial_ss_p1": "0",
            "abs_partial_r_s_p1": "<=625/16",
            "abs_partial_phi_s_p1": "<=25/4",
            "dyadic_rank_exponent": 0,
        }:
            errors.append("momentum bounds")
        if area["full_F10_rank_exponent_reduced_to_zero"] is not False:
            errors.append("full exponent overclaim")
        if area["area_coordinate_split"] != "CERTIFIED":
            errors.append("area split")

        shell = result["physical_area_shell_summability_frontier"]
        if shell["exact_probability_law"] != (
            "P(B=2k)=(15/16)*16^-k, k>=0"
        ):
            errors.append("shell law")
        if shell["claim_about_actual_physical_path_divergence"] is not False:
            errors.append("physical divergence overclaim")
        if shell["coordinate_change_alone_closes_arbitrary_Rn_F10"] is not False:
            errors.append("coordinate closure overclaim")
        if shell["supercritical_obstruction"] != "CERTIFIED_NO_IMPLICATION":
            errors.append("obstruction")
        if shell["finite_prefix_rows"] != cert.shell_prefixes():
            errors.append("shell prefixes")
        if shell["finite_prefix_rows"][-1]["shell_prefix_count"] != 16:
            errors.append("shell prefix depth")

        split = result["area_preserving_current_decomposition"]
        if split["identity_status"] != "CERTIFIED_ALGEBRAIC":
            errors.append("current identity")
        if split["divergence_free_generator"] != "div_mu X_s=0 on each regular branch":
            errors.append("divergence free")
        typed = split["typed_terms"]
        if "F13" not in typed["dynamic_transport_current"]:
            errors.append("F13 typing")
        if "F16" not in typed["flux_operator_cost"]:
            errors.append("F16 typing")
        if split["F13_trace_bounds_on_arbitrary_Rn"] != "NOT_CERTIFIED":
            errors.append("F13 scope")
        if split["F16_flux_cost_on_arbitrary_Rn"] != "NOT_CERTIFIED":
            errors.append("F16 scope")

        technology = result["latest_technology_audit"]
        if technology["official_arXiv_snapshot"] != [
            "2104.06947v3",
            "2604.19671v2",
            "2606.10155v1",
        ]:
            errors.append("arXiv snapshot")
        if technology["new_direct_theorem_for_arbitrary_Rn_moving_face_F10"] is not False:
            errors.append("technology overclaim")

        scope = result["strict_nonpromotion"]
        if scope["target_momentum_parameter_rank_exponent_zero"] != "CERTIFIED":
            errors.append("momentum verdict")
        if scope["target_position_cubed_grazing_loss_removed"] is not False:
            errors.append("position verdict")
        if scope["arbitrary_Rn_pullback_F10_field"] != "NOT_CERTIFIED":
            errors.append("F10 verdict")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
        if scope["Gate5"] != "NOT_CERTIFIED":
            errors.append("Gate5")
        if scope["complete_composite_gates"] != "0/5":
            errors.append("gate count")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("canonical_area_coordinate_split", "collision_SRB_area_form", "wrong"),
        ("canonical_area_coordinate_split", "ray_circle_target_momentum", "p_1=tau"),
        ("canonical_area_coordinate_split", "full_F10_rank_exponent_reduced_to_zero", True),
        ("canonical_area_coordinate_split", "area_coordinate_split", "OPEN"),
        ("physical_area_shell_summability_frontier", "exact_probability_law", "finite support"),
        ("physical_area_shell_summability_frontier", "claim_about_actual_physical_path_divergence", True),
        ("physical_area_shell_summability_frontier", "coordinate_change_alone_closes_arbitrary_Rn_F10", True),
        ("physical_area_shell_summability_frontier", "supercritical_obstruction", "NONE"),
        ("area_preserving_current_decomposition", "identity_status", "NOT_CERTIFIED"),
        ("area_preserving_current_decomposition", "divergence_free_generator", "div X=1"),
        ("area_preserving_current_decomposition", "F13_trace_bounds_on_arbitrary_Rn", "CERTIFIED"),
        ("area_preserving_current_decomposition", "F16_flux_cost_on_arbitrary_Rn", "CERTIFIED"),
        ("latest_technology_audit", "new_direct_theorem_for_arbitrary_Rn_moving_face_F10", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["canonical_area_coordinate_split"][
        "target_momentum_parameter_bounds"
    ]["dyadic_rank_exponent"] = 3
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["physical_area_shell_summability_frontier"][
        "finite_prefix_rows"
    ][0]["2^(3B)_moment_prefix"] = "0"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["area_preserving_current_decomposition"]["typed_terms"][
        "dynamic_transport_current"
    ] = "F10"
    mutations.append(mutation)
    for key, value in (
        ("target_position_cubed_grazing_loss_removed", True),
        ("arbitrary_Rn_F13_trace_bounds", "CERTIFIED"),
        ("arbitrary_Rn_F16_flux_cost", "CERTIFIED"),
        ("arbitrary_Rn_pullback_F10_field", "CERTIFIED"),
        ("complete_all_face_F10_field", "CERTIFIED"),
        ("F13", "CERTIFIED"),
        ("F14_through_F18", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
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
