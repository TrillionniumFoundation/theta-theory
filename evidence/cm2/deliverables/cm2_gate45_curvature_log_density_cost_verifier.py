#!/usr/bin/env python3
"""Fail-closed verifier for curvature and log-density subcosts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.curvature-log-density-cost.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_curvature_log_density_cost_cert.py"


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
    if result.get("schema") != "cm2.gate45.curvature-log-density-cost.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "endpoint_rank_manifest": (
            "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
        ),
        "bidirectional_boundary_Z_manifest": (
            "cm2-gate45-bidirectional-boundary-z-cost-manifest-2026-07-16.json"
        ),
        "global_invariant_cone_manifest": (
            "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    audit = result.get("nonactive_parameter_velocity_collar_audit", {})
    for key, expected in {
        "endpoint_collar_count": 128,
        "parameter_polarity_active_collar_count": 16,
        "nonactive_parameter_velocity_collar_count": 112,
        "every_nonactive_collar_absolute_u_y_strict_lower": "1/32",
        "nonactive_u_y_collar_rows_sha256": (
            "71c77f3dac50f6525076545c0a6e859355b33650dcb78cfb88176cdad952c380"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
    }.items():
        if audit.get(key) != expected:
            errors.append(f"parameter-velocity audit mismatch: {key}")

    costs = result.get("curvature_log_density_and_partial_cost", {})
    rank = costs.get("rank_dominates_all_density_denominators", {})
    for key, expected in {
        "canonical_core_rank": 14,
        "source_cosine_inverse": "1/cp_source<=2^B",
        "parameter_velocity_inverse": "1/abs(u_y)<=2^B",
        "miss_cosine_inverse": "1/cp_miss<=2^B",
    }.items():
        if rank.get(key) != expected:
            errors.append(f"rank denominator mismatch: {key}")

    curvature = costs.get("bidirectional_carrier_C2_bounds", {})
    for key, expected in {
        "common_caustic_slope": "V=kappa+cp/d",
        "differentiated_bound": (
            "abs(dV/dr)<=kappa/d+2/d^2+R_caustic/d^3"
        ),
        "source_reverse_distance_strict_lower": "1/10",
        "source_reverse_curvature_exact_upper": "1245/2",
        "source_reverse_curvature_strict_upper": "623",
        "miss_forward_distance_strict_lower": "36337/800000",
        "miss_forward_curvature_exact_upper": (
            "237433247845000000/47978559724753"
        ),
        "miss_forward_curvature_strict_upper": "4949",
        "both_curvature_costs_absorbed_by_2^B": True,
    }.items():
        if curvature.get(key) != expected:
            errors.append(f"carrier curvature mismatch: {key}")

    log_cost = costs.get("bidirectional_log_density_bounds", {})
    for key, expected in {
        "reverse_density": "rho_rev=cp_source*abs(u_y)/ell_T",
        "forward_density": (
            "rho_fw=cp_miss*abs(u_y)/(t_miss-ell_T)"
        ),
        "reverse_log_derivative_coefficient_exact_upper": "215063/8192",
        "reverse_log_derivative_cost": (
            "abs(d log(rho_rev)/dr_source)<27*2^B"
        ),
        "forward_log_derivative_coefficient_exact_upper": (
            "4312088721189/84504164416"
        ),
        "forward_log_derivative_cost": (
            "abs(d log(rho_fw)/dr_miss)<52*2^B"
        ),
    }.items():
        if log_cost.get(key) != expected:
            errors.append(f"log-density mismatch: {key}")

    partial = costs.get("numeric_one_collision_geometric_subcosts", {})
    for key, expected in {
        "rank_coefficient_breakdown": (
            "151 first-order chart pullback + 52 log-density + 1 carrier-C2"
        ),
        "reverse_subcost": "C_rev^(geom,Z)=204*2^B+C_Z_rev",
        "forward_subcost": "C_fw^(geom,Z)=204*2^B+C_Z_fw",
        "one_common_partial_charge": (
            "q_e^(geom,Z)=max(C_fw^(geom,Z),C_rev^(geom,Z),2)*m_e"
        ),
        "global_partial_charge_mass_upper_before_Z_N_inverse": (
            "344740673672569503213/63953120000"
        ),
        "partial_charge_is_finite": True,
        "partial_charge_is_not_final_recovery_charge": True,
    }.items():
        if partial.get(key) != expected:
            errors.append(f"partial geometric cost mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "all_row_bidirectional_carrier_C2_bounds",
        "all_row_bidirectional_log_density_derivative_costs",
        "numeric_one_collision_geometric_forward_reverse_subcosts",
        "one_finite_partial_geometric_charge_per_occurrence",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "physical_stopped_recovery_clock",
        "complete_numeric_C_fw_C_rev",
        "controlled_stopped_parent_recovery",
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
        "71c77f3dac50f6525076545c0a6e859355b33650dcb78cfb88176cdad952c380"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("bidirectional_carrier_C2_costs") != "CERTIFIED":
        errors.append("carrier-C2 verdict mismatch")
    if verdict.get("bidirectional_log_density_costs") != "CERTIFIED":
        errors.append("log-density verdict mismatch")
    if verdict.get("complete_C_fw_C_rev_and_stopped_recovery") != "NOT_CERTIFIED":
        errors.append("complete costs/recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_curvature_log_density_cost_cert as cert
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
        print("GATE45_CURVATURE_LOG_DENSITY_COST_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["curvature_log_density_and_partial_cost"][
            "bidirectional_log_density_bounds"
        ]["forward_log_derivative_cost"] = "0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (log-density tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["physical_stopped_recovery_clock"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported stopped recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  log-density tamper rejected")
        print("  unsupported stopped recovery rejected")
        return 0
    print("GATE45_BIDIRECTIONAL_CARRIER_C2_COSTS: CERTIFIED")
    print("GATE45_BIDIRECTIONAL_LOG_DENSITY_COSTS: CERTIFIED")
    if args.integrity_only:
        print("GATE45_CURVATURE_LOG_DENSITY_COST_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_C_FW_C_REV_AND_STOPPED_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
