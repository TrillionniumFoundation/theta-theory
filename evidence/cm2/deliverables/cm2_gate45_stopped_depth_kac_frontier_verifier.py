#!/usr/bin/env python3
"""Fail-closed verifier for stopped-depth and Kac frontier data."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.stopped-depth-kac-frontier.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-stopped-depth-kac-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_stopped_depth_kac_frontier_cert.py"


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
    if result.get("schema") != "cm2.gate45.stopped-depth-kac-frontier.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "endpoint_rank_first_order_manifest": (
            "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
        ),
        "controlled_interval_algebra_manifest": (
            "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
        ),
        "corrected_kac_manifest": (
            "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    critical = result.get("critical_stopped_depth_countermodel", {})
    for key, expected in {
        "critical_depth_tail": "P(K>=k)=2^-k",
        "normalization_moment_at_cutoff_N": "E[2^K]=1+N/2",
        "required_depth_tail_exponent_base_two": "strictly greater than 1",
        "critical_tail_does_not_uniformly_control_2^K": True,
        "dyadic_atom_mass_scale_alone_is_not_a_stopping_depth_law": True,
        "finite_countermodel_rows_sha256": (
            "ebc5d0185491ce62c9dae9739d76045a07e391d1aebf25f9ded8b9c1f1c4295a"
        ),
    }.items():
        if critical.get(key) != expected:
            errors.append(f"critical-depth mismatch: {key}")
    family = critical.get("finite_countermodel_family")
    if not isinstance(family, list) or [row.get("E_2^K") for row in family] != [
        "3", "5", "9", "17", "33"
    ]:
        errors.append("critical countermodel family mismatch")

    sufficient = result.get("supercritical_depth_rank_sufficient_bridge", {})
    for key, expected in {
        "assumed_propagated_depth_tail": "q{K>=k}<=A*2^(-3k/2)",
        "depth_holder_moment": "E_q[2^(5K/4)]<=7A",
        "geometric_ratio_certificate": "2^(-1/4)<6/7",
        "holder_exponents": ["5/4", "5"],
        "endpoint_rank_factor": "2^(B/10)",
        "endpoint_holder_moment_required": "E_q[2^(B/2)]<infinity",
        "combined_moment": "E_q[2^K*2^(B/10)]<infinity",
        "conditional_recovery_clock": (
            "if R_fw+R_rev<=A0+A1*B, choose gamma=log(2)/(10*A1)"
        ),
        "conditional_target_moment": (
            "E_q[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "endpoint_exponent_is_inside_certified_first_order_q_window": True,
        "no_independence_of_K_and_B_required": True,
        "physical_supercritical_depth_tail_available": False,
        "physical_rank_recovery_clock_available": False,
    }.items():
        if sufficient.get(key) != expected:
            errors.append(f"supercritical bridge mismatch: {key}")

    rebind = result.get("first_order_64_occurrence_128_coordinate_kac_rebind", {})
    for key, expected in {
        "maximal_occurrence_count": 64,
        "singular_kac_coordinate_count": 128,
        "incorrect_per_coordinate_double_charge_count": 128,
        "one_first_order_charge_per_occurrence": True,
        "first_order_charge_formula": "q_e^(1)=151*2^B*m_e",
        "global_first_order_charge_mass_upper_before_Z_N_inverse": (
            "3511236449384553/880000"
        ),
        "global_first_order_current_TV_upper_before_Z_N_inverse": (
            "3511236449384553/440000"
        ),
        "finite_borel_kac_algebra_survives_first_order_reweighting": True,
        "global_signed_scalar_coarea_mass_before_reweighting": "0",
        "weighted_scalar_cancellation_not_claimed": True,
        "first_order_occurrence_rows_sha256": (
            "e6a0bfe0b1147566243d733c397f99840d79c5d9dbabc299fd81e8851e7ea72b"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
        "prior_corrected_occurrence_rows_sha256": (
            "dee3b15f6747e81a7c63ef7b3c5e3c9b2e3ed3fc61339c0113f0ec618c5cb30f"
        ),
    }.items():
        if rebind.get(key) != expected:
            errors.append(f"first-order Kac rebind mismatch: {key}")

    frontier = result.get("physical_completion_frontier", {})
    for key in (
        "controlled_dyadic_interval_algebra",
        "finite_raw_endpoint_rank_first_moment",
        "numeric_first_order_bidirectional_C1_subcosts",
    ):
        if frontier.get(key) is not True:
            errors.append(f"missing positive frontier flag: {key}")
    for key in (
        "stopped_depth_random_variable_on_physical_tree",
        "q_propagated_supercritical_depth_tail",
        "C2_curvature_and_log_density_costs",
        "boundary_Z_and_proper_family_recovery_clock",
        "full_numeric_C_fw_C_rev",
        "controlled_stopped_parent_recovery",
        "dynamic_MT_DQ",
        "CM2_norm_lifts",
    ):
        if frontier.get(key) is not False:
            errors.append(f"unsupported frontier completion: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "critical_depth_tail_obstruction_exact",
        "supercritical_depth_tail_sufficient_theorem_exact",
        "first_order_Kac_rebind_complete",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "physical_supercritical_depth_tail",
        "physical_recovery_clock",
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
        "137a226f0e808a2ca61a21dbe2dfa760185400f023746d3c920c684174419513"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    for key in (
        "critical_stopped_depth_tail_obstruction",
        "supercritical_depth_rank_sufficient_bridge",
        "first_order_64_row_128_coordinate_Kac_rebind",
    ):
        if verdict.get(key) != "CERTIFIED":
            errors.append(f"positive verdict mismatch: {key}")
    if verdict.get("physical_stopped_recovery_and_CM2_lifts") != "NOT_CERTIFIED":
        errors.append("physical recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_stopped_depth_kac_frontier_cert as cert
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
        print("GATE45_STOPPED_DEPTH_KAC_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["critical_stopped_depth_countermodel"][
            "normalization_moment_at_cutoff_N"
        ] = "bounded"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (critical-depth tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"][
            "controlled_stopped_parent_recovery"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  critical-depth tamper rejected")
        print("  unsupported stopped recovery rejected")
        return 0
    print("GATE45_CRITICAL_STOPPED_DEPTH_TAIL_OBSTRUCTION: CERTIFIED")
    print("GATE45_SUPERCRITICAL_DEPTH_RANK_SUFFICIENT_BRIDGE: CERTIFIED")
    print("GATE45_FIRST_ORDER_64_ROW_128_COORDINATE_KAC_REBIND: CERTIFIED")
    if args.integrity_only:
        print("GATE45_STOPPED_DEPTH_KAC_FRONTIER_INTEGRITY: PASS")
        return 0
    print("GATE45_PHYSICAL_STOPPED_RECOVERY_AND_CM2_LIFTS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
