#!/usr/bin/env python3
"""Fail-closed verifier for bidirectional boundary-Z subcosts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.bidirectional-boundary-z-cost.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-bidirectional-boundary-z-cost-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_bidirectional_boundary_z_cost_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
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
    if result.get("schema") != "cm2.gate45.bidirectional-boundary-z-cost.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "endpoint_rank_first_order_manifest": (
            "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
        ),
        "all_row_slope_manifest": (
            "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    zeros = result.get("orientation_specific_density_zero_ledger", {})
    for key, expected in {
        "maximal_occurrence_count": 64,
        "source_view_simple_zero_endpoint_count": 48,
        "miss_view_simple_zero_endpoint_count": 48,
        "selected_miss_tangent_endpoint_count": 32,
        "shared_parameter_polarity_zero_endpoint_count": 16,
        "source_regular_endpoint_count": 80,
        "miss_regular_endpoint_count": 80,
        "orientation_zero_rows_sha256": (
            "47362f121d2fde534c16047dd4be04d6d1742bae55dd93dbf17975c3549cc864"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
    }.items():
        if zeros.get(key) != expected:
            errors.append(f"orientation-zero ledger mismatch: {key}")

    exact = result.get("exact_density_and_boundary_Z_cost", {})
    source = exact.get("exact_source_density_derivation", {})
    for key, expected in {
        "source_arclength": "dr_source=R_source*dtheta",
        "coarea_law": "dm=R_source*cp_source*abs(u_y)/ell_T*dtheta",
        "density_wrt_dr_source": "rho_rev=cp_source*abs(u_y)/ell_T",
        "strict_density_upper": "10",
    }.items():
        if source.get(key) != expected:
            errors.append(f"source density mismatch: {key}")
    miss = exact.get("exact_miss_density_derivation", {})
    for key, expected in {
        "caustic_angle_variation": (
            "d beta/dtheta=-R_source*cp_source/ell_T"
        ),
        "miss_arclength_jacobian": (
            "abs(dr_miss/dtheta)=(t_miss-ell_T)*R_source*"
            "cp_source/(ell_T*cp_miss)"
        ),
        "density_wrt_dr_miss": (
            "rho_fw=cp_miss*abs(u_y)/(t_miss-ell_T)"
        ),
        "miss_gap_strict_lower": "36337/800000",
        "strict_density_upper": "800000/36337",
    }.items():
        if miss.get(key) != expected:
            errors.append(f"miss density mismatch: {key}")

    subdivision = exact.get("canonical_boundary_subdivision", {})
    for key, expected in {
        "core_rank": 14,
        "dyadic_zero_shell": "2^(-(b+1))<=scale<2^-b, b>=14",
        "sum_shell_scales": "1/8192",
        "source_shell_Z_contribution_per_zero": "<=10*2^-b",
        "miss_shell_Z_contribution_per_zero": (
            "<=(800000/36337)*2^-b"
        ),
        "one_core_component_per_occurrence_and_orientation": True,
    }.items():
        if subdivision.get(key) != expected:
            errors.append(f"boundary subdivision mismatch: {key}")

    costs = exact.get("numeric_boundary_Z_subcosts", {})
    for key, expected in {
        "global_reverse_source_Z_upper_before_Z_N_inverse": "163855/256",
        "global_forward_miss_Z_upper_before_Z_N_inverse": "102409375/72674",
        "global_partial_charge_mass_upper_by_sum_before_Z_N_inverse": (
            "255175728776567057847/63953120000"
        ),
        "partial_single_charge_formula": (
            "q_e^(1,Z)=max(151*2^B,C_Z_fw,C_Z_rev,2)*m_e"
        ),
        "both_raw_boundary_Z_sums_finite": True,
        "canonical_piecewise_boundary_costs_are_Borel": True,
        "partial_charge_is_not_final_q": True,
    }.items():
        if costs.get(key) != expected:
            errors.append(f"boundary-Z cost mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "exact_source_and_miss_arclength_densities",
        "numeric_bidirectional_raw_boundary_Z_subcosts",
        "one_partial_first_order_plus_Z_charge_per_occurrence",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "log_density_regularization_cost",
        "homogeneity_weighted_C2_curvature_cost",
        "proper_standard_family_recovery_clock",
        "complete_numeric_C_fw_C_rev",
        "controlled_stopped_parent_recovery",
        "full_dynamic_MT_DQ",
        "CM2_norm_lifts",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if result.get("internal_replay_digest") != (
        "47362f121d2fde534c16047dd4be04d6d1742bae55dd93dbf17975c3549cc864"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("exact_bidirectional_arclength_densities") != "CERTIFIED":
        errors.append("density verdict mismatch")
    if verdict.get("numeric_bidirectional_raw_boundary_Z_costs") != "CERTIFIED":
        errors.append("boundary-Z verdict mismatch")
    if verdict.get("complete_C_fw_C_rev_and_recovery") != "NOT_CERTIFIED":
        errors.append("complete cost/recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_bidirectional_boundary_z_cost_cert as cert
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
        print("GATE45_BIDIRECTIONAL_BOUNDARY_Z_COST_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["exact_density_and_boundary_Z_cost"][
            "numeric_boundary_Z_subcosts"
        ]["global_reverse_source_Z_upper_before_Z_N_inverse"] = "0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (boundary-Z tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["complete_numeric_C_fw_C_rev"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported complete costs accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  boundary-Z tamper rejected")
        print("  unsupported complete C_fw/C_rev rejected")
        return 0
    print("GATE45_EXACT_BIDIRECTIONAL_ARCLENGTH_DENSITIES: CERTIFIED")
    print("GATE45_NUMERIC_BIDIRECTIONAL_RAW_BOUNDARY_Z_COSTS: CERTIFIED")
    if args.integrity_only:
        print("GATE45_BIDIRECTIONAL_BOUNDARY_Z_COST_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
