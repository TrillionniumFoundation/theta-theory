#!/usr/bin/env python3
"""Fail-closed verifier for the finite-s mesh and recovery certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.finite-s-common-mesh-recovery.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.finite-s-common-mesh-recovery.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_finite_s_common_mesh_recovery_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_exact(
    errors: list[str], section: dict[str, Any], expected: dict[str, Any], label: str
) -> None:
    for key, value in expected.items():
        if section.get(key) != value:
            errors.append(f"{label} mismatch: {key}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")

    check_exact(errors, result.get("provenance", {}), {
        "maximal_row_manifest": (
            "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
        ),
        "curvature_log_density_manifest": (
            "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
        ),
        "product_stopped_depth_manifest": (
            "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
        ),
        "s0_recovery_manifest": (
            "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
        ),
        "uniform_horizon_certificate": "cm2_standard_section_horizon_lift_cert.py",
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
    }, "provenance")

    endpoint = result.get("finite_s_endpoint_collar_audit", {})
    check_exact(errors, endpoint, {
        "parameter_window": ["-1/400", "1/400"],
        "common_inward_angular_collar": "1/48",
        "initial_angular_cells_per_endpoint": 32,
        "endpoint_incidence_count": 128,
        "endpoint_counts_by_kind": {
            "parameter_polarity": 16,
            "physical_earlier_occlusion_boundary": 16,
            "physical_later_miss_switch_boundary": 64,
            "source_grazing": 32,
        },
        "uniform_inward_derivative_strict_lowers": {
            "parameter_polarity": "1/6",
            "physical_earlier_occlusion_boundary": "1/16",
            "physical_later_miss_switch_boundary": "1/32",
            "source_grazing": "9/10",
        },
        "common_nonactive_scale_strict_lower": "1/1048576",
        "parameter_leaf_count": 20104,
        "maximum_parameter_subdivision_depth": 5,
        "endpoint_parameter_rows_sha256": (
            "09f59ea2a1b1381187245e0160287554d9f122b02e087fe63857f51c041319cf"
        ),
    }, "endpoint collar")

    core = result.get("finite_s_moving_core_audit", {})
    check_exact(errors, core, {
        "moving_core_definition": "inward angular interval [1/48,width_s-1/48]",
        "uniform_row_angular_width_strict_lower": "1/16",
        "common_core_scale_strict_lower": "1/1048576",
        "initial_normalized_angular_cells_per_row": 16,
        "uniform_parameter_cells_per_row": 64,
        "core_leaf_count": 110336,
        "maximum_core_subdivision_depth": 6,
        "core_leaf_rows_sha256": (
            "c34e6b0fedf0a9ca6303a72e4e06bbfaa65f8478965d6087d8519f67ec8a2a3f"
        ),
        "per_occurrence_rows_sha256": (
            "146e7246c6a006a9ba3d9ef2d566f7fb4745cad88d7082a7fd68930f81845278"
        ),
    }, "moving core")

    rank_cost = result.get("finite_s_rank_and_one_collision_cost", {})
    check_exact(errors, rank_cost.get("uniform_rank_tail", {}), {
        "valid_integer_threshold": "b>=20",
        "global_tail_constant": "4839232/3125",
        "integral_2^B_uniform_upper_before_Z_N_inverse": (
            "43293270343755613/25600000"
        ),
    }, "rank tail")
    check_exact(errors, rank_cost.get("finite_s_one_collision_cost", {}), {
        "uniform_reverse_subcost": "C_rev^(geom)(s,a)<=204*2^B_s(a)",
        "uniform_forward_subcost": "C_fw^(geom)(s,a)<=204*2^B_s(a)",
        "uniform_partial_charge_mass_upper_before_boundary_Z": (
            "2207956787531536263/6400000"
        ),
        "complete_propagated_numeric_C_fw_C_rev": False,
    }, "one-collision cost")

    mesh = result.get("finite_s_density_mesh_and_numeric_C_mesh", {})
    check_exact(errors, mesh, {
        "canonical_mesh": "delta_b=2^-ceil(3(b+1)/2), b>=20",
        "uniform_carrier_shell_length_upper": "2^17*2^-b",
        "uniform_density_upper_on_zero_shell": "23*2^-b",
        "one_zero_endpoint_Z_series_upper": "18522046487/524288",
        "one_zero_endpoint_Z_series_summable": True,
        "uniform_row_mass_strict_lower": "1/989560464998400",
        "explicit_initial_C_mesh": "69986663973833932800",
        "density_mesh_rows_sha256": (
            "f356adec6f4431e1d3bfe95e024b2595ea48ae532d99d236192f02f8b91a5d09"
        ),
    }, "density mesh")

    horizon = result.get("uniform_horizon_penetration_audit", {})
    check_exact(errors, horizon, {
        "replayed_leaf_count": 35024,
        "maximum_binary_depth": 14,
        "least_squared_penetration_slack_strict_lower": "1/524288",
        "uniform_incidence_sine_squared_strict_lower": "25/4718592",
        "explicit_SYZ_horizon": "(t,phi)=(3,1/512)",
        "every_open_length_3_segment_has_one_incidence_angle_gt_1_over_512": True,
        "horizon_leaf_rows_sha256": (
            "b34c66989be6bb2c738eb8185096a1903a96c108d316d768978cd7514d77d6c7"
        ),
    }, "uniform horizon")

    recovery = result.get("uniform_configuration_and_recovery", {})
    check_exact(errors, recovery.get("compact_configuration_path", {}), {
        "declared_SYZ_tau_bar_min": "1/25",
        "uniform_SYZ_horizon": "(3,1/512)",
        "one_compact_SYZ_configuration_class": True,
    }, "configuration path")
    check_exact(errors, recovery.get("one_time_atom_typing", {}), {
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
        "uniform_recovery_is_not_common_branch_record_MT_DQ": True,
    }, "atom typing")
    check_exact(errors, recovery.get("uniform_recovery_theorem", {}), {
        "source": (
            "Stenlund--Young--Zhang, Dispersing billiards with moving "
            "scatterers, arXiv:1210.0011v4"
        ),
        "growth_result": (
            "Lemma 12 (Growth lemma), uniform for all configuration sequences"
        ),
        "Z_result": (
            "Lemma 16: Z_n/mu <= C_p/2*(1+vartheta_p^n*Z_0/mu)"
        ),
        "constants_uniform_in_s_and_orientation": True,
        "controlled_one_time_finite_s_stopped_parent_recovery": True,
        "C_p_vartheta_p_numerically_evaluated": False,
        "hereditary_repeated_indicator_recovery": False,
    }, "recovery theorem")

    limits = result.get("scope_limits", {})
    for key in (
        "finite_s_common_moving_endpoint_collars",
        "finite_s_common_density_regular_mesh_rule",
        "mesh_endpoints_move_with_u_e_s",
        "explicit_numeric_initial_C_mesh",
        "uniform_one_time_finite_s_stopped_parent_recovery",
        "finite_s_depth_plus_recovery_moment_for_some_gamma",
        "uniform_one_collision_geometric_cost_coefficients",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas",
        "common_branch_record_MT_DQ",
        "theorem_recovery_constants_numeric",
        "complete_propagated_numeric_C_fw_C_rev_q",
        "native_dynamical_stopping_antichain",
        "hereditary_repeated_indicator_recovery",
        "physical_prefix_suffix_costs",
        "full_dynamic_MT_DQ",
        "CM2_norm_lifts",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if result.get("internal_replay_digest") != (
        "85692dbad0dcc08808c97da232a096d500800c105abf890e230c4c8c5f8e7448"
    ):
        errors.append("internal replay digest mismatch")

    check_exact(errors, data.get("verdict", {}), {
        "finite_s_common_endpoint_mesh": "CERTIFIED",
        "explicit_numeric_initial_C_mesh": "CERTIFIED",
        "uniform_one_time_finite_s_recovery": "CERTIFIED",
        "complete_propagated_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }, "verdict")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_finite_s_common_mesh_recovery_cert as cert
        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE45_FINITE_S_COMMON_MESH_RECOVERY_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        mutations = [
            (
                "endpoint leaf count",
                lambda value: value["result"]["finite_s_endpoint_collar_audit"].__setitem__(
                    "parameter_leaf_count", 20103
                ),
            ),
            (
                "core leaf count",
                lambda value: value["result"]["finite_s_moving_core_audit"].__setitem__(
                    "core_leaf_count", 110335
                ),
            ),
            (
                "rank tail",
                lambda value: value["result"]["finite_s_rank_and_one_collision_cost"][
                    "uniform_rank_tail"
                ].__setitem__("global_tail_constant", "0"),
            ),
            (
                "numeric C_mesh",
                lambda value: value["result"]["finite_s_density_mesh_and_numeric_C_mesh"].__setitem__(
                    "explicit_initial_C_mesh", "1"
                ),
            ),
            (
                "explicit horizon",
                lambda value: value["result"]["uniform_horizon_penetration_audit"].__setitem__(
                    "every_open_length_3_segment_has_one_incidence_angle_gt_1_over_512",
                    False,
                ),
            ),
            (
                "unsupported propagated costs",
                lambda value: value["result"]["scope_limits"].__setitem__(
                    "complete_propagated_numeric_C_fw_C_rev_q", True
                ),
            ),
        ]
        for label, mutate in mutations:
            tampered = copy.deepcopy(data)
            mutate(tampered)
            if not check_structure(tampered):
                print(f"SELF_TEST: FAIL ({label} tamper accepted)")
                return 1
        print("SELF_TEST: PASS")
        for label, _mutate in mutations:
            print(f"  {label} tamper rejected")
        return 0
    print("GATE45_FINITE_S_COMMON_ENDPOINT_MESH: CERTIFIED")
    print("GATE45_UNIFORM_ONE_TIME_FINITE_S_RECOVERY: CERTIFIED")
    print("GATE45_EXPLICIT_INITIAL_C_MESH: CERTIFIED")
    if args.integrity_only:
        print("GATE45_FINITE_S_COMMON_MESH_RECOVERY_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_PROPAGATED_NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
