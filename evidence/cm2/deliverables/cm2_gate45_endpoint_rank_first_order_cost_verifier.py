#!/usr/bin/env python3
"""Fail-closed verifier for endpoint-rank and first-order cost data."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.endpoint-rank-first-order-cost.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_endpoint_rank_first_order_cost_cert.py"


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
    if result.get("schema") != "cm2.gate45.endpoint-rank-first-order-cost.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "corrected_DQ_manifest": (
            "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
        ),
        "all_row_slope_manifest": (
            "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
        ),
        "controlled_interval_algebra_manifest": (
            "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    endpoint = result.get("all_endpoint_simple_germ_audit", {})
    endpoint_expected = {
        "maximal_row_count": 64,
        "endpoint_incidence_count": 128,
        "endpoint_counts_by_kind": {
            "parameter_polarity": 16,
            "physical_earlier_occlusion_boundary": 16,
            "physical_later_miss_switch_boundary": 64,
            "source_grazing": 32,
        },
        "minimum_row_arc_width_strict_lower": "1/10",
        "common_collar_width": "1/2048",
        "global_simple_germ_derivative_strict_lower": "3/80",
        "every_nonactive_collar_source_cp_strict_lower": "1/4096",
        "every_nonactive_collar_miss_cp_squared_strict_lower": "1/16384",
        "endpoint_rows_sha256": (
            "34316a4ddc301f1036e72aa089086bf392c1e28e11220943ac384621b3db626b"
        ),
        "row_width_rows_sha256": (
            "6c3dd32ff96babfdd55bf1160bb3681fb1eba5c85d38fe19575a7251bbf8c12f"
        ),
    }
    for key, expected in endpoint_expected.items():
        if endpoint.get(key) != expected:
            errors.append(f"endpoint audit mismatch: {key}")
    if endpoint.get("collars_are_pairwise_disjoint_on_each_row") is not True:
        errors.append("endpoint collar disjointness missing")

    core = result.get("compact_core_nondegeneracy_audit", {})
    core_expected = {
        "trimmed_core_row_count": 64,
        "common_endpoint_trim": "1/2048",
        "strict_core_source_cp_lower": "1/4096",
        "strict_core_absolute_uy_lower": "1/16384",
        "strict_core_miss_cp_squared_lower": "1/16384",
        "strict_core_transition_scale_squared_lower": "1/16384",
        "adaptive_core_leaf_count": 3206,
        "maximum_core_subdivision_depth": 14,
        "core_leaf_depth_counts": {
            "2": 2,
            "3": 92,
            "4": 464,
            "5": 390,
            "6": 372,
            "7": 334,
            "8": 316,
            "9": 332,
            "10": 332,
            "11": 252,
            "12": 192,
            "13": 96,
            "14": 32,
        },
        "core_leaf_rows_sha256": (
            "2990cbbfcb64dc464b509e4753c0e4f108e2abd8a0898bad56f633d7aadc8fab"
        ),
        "per_occurrence_core_rows_sha256": (
            "561bbaab426e31ac54579fb15f2b82574548c5177d9af3888fe033db34d4e274"
        ),
    }
    for key, expected in core_expected.items():
        if core.get(key) != expected:
            errors.append(f"compact core mismatch: {key}")

    cost = result.get("endpoint_rank_tail_and_first_order_cost", {})
    rank = cost.get("canonical_rank_definition", {})
    for key, expected in {
        "core_rank": 14,
        "endpoint_rank": "max(14,ceil(log2(1/scale))) on its collar",
        "source_grazing_scale": "cp_source",
        "parameter_polarity_scale": "abs(u_y)",
        "transition_scale": "sqrt(abs(Delta_transition))/R_transition",
        "only_one_endpoint_collar_active_per_row_point": True,
    }.items():
        if rank.get(key) != expected:
            errors.append(f"rank definition mismatch: {key}")

    tail = cost.get("endpoint_tail", {})
    for key, expected in {
        "valid_integer_threshold": "b>=14",
        "source_tail_constant_per_endpoint": "40/11",
        "polarity_tail_constant_per_endpoint": "20",
        "first_visibility_tail_constant_per_endpoint": "3888/625",
        "miss_switch_tail_constant_per_endpoint": "7776/625",
        "global_tail_constant": "9158592/6875",
        "tail_exponent_in_dyadic_rank": "2",
    }.items():
        if tail.get(key) != expected:
            errors.append(f"rank tail mismatch: {key}")

    moment = cost.get("raw_rank_moment", {})
    for key, expected in {
        "positive_coarea_mass_upper_before_Z_N_inverse": "8064/5",
        "integral_2^B_dm_upper_before_Z_N_inverse": "23253221519103/880000",
        "all_rank_moments_2^(chi*B)_finite_for": "0<=chi<2",
        "first_order_charge_rank_moments_2^(chi*B)_finite_for": "0<=chi<1",
        "finite_first_rank_moment": True,
        "chi_equals_2_not_inferred_from_tail_bound": True,
    }.items():
        if moment.get(key) != expected:
            errors.append(f"rank moment mismatch: {key}")
    try:
        if Fraction(moment["integral_2^B_dm_upper_before_Z_N_inverse"]) <= 0:
            errors.append("rank moment bound is not positive")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid rank moment arithmetic")

    derivative = cost.get("one_collision_birkhoff_derivative", {})
    for key, expected in {
        "tau_strict_upper": "3",
        "kappa_upper": "25/4",
        "infinity_norm_numerator_upper": "2391/16",
        "forward_derivative_bound": "||DF_e||_infinity<150/cp_miss",
        "reverse_derivative_bound": "||DF_e^-1||_infinity<150/cp_source",
        "rank_dominates_both_inverse_incidence_scales": True,
    }.items():
        if derivative.get(key) != expected:
            errors.append(f"collision derivative mismatch: {key}")

    charge = cost.get("first_order_bidirectional_subcharge", {})
    for key, expected in {
        "forward_C1_chart_test_subcost": "C_fw^(1)(a)=151*2^B(a)",
        "reverse_C1_chart_test_subcost": "C_rev^(1)(a)=151*2^B(a)",
        "one_common_first_order_charge": "q_e^(1)=151*2^B*m_e",
        "global_first_order_charge_mass_upper_before_Z_N_inverse": (
            "3511236449384553/880000"
        ),
        "global_first_order_current_TV_upper_before_Z_N_inverse": (
            "3511236449384553/440000"
        ),
        "one_collision_dynamic_C1_pullback_integrable": True,
        "first_order_charge_is_not_final_q": True,
    }.items():
        if charge.get(key) != expected:
            errors.append(f"first-order charge mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "all_128_endpoint_germs_simple",
        "global_endpoint_rank_tail_exponent_two",
        "finite_raw_first_rank_moment",
        "numeric_first_order_forward_reverse_C1_subcosts",
        "one_collision_dynamic_C1_pullback_integrable",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "homogeneity_weighted_C2_curvature_cost",
        "log_density_and_boundary_Z_cost",
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
        "8747bfdc48aeb8fb208cedd4110e7298eaccddf1e0075cc7ea97a7bc8c764438"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    for key in (
        "all_128_endpoint_simple_germs",
        "global_endpoint_rank_tail_exponent_two",
        "first_order_bidirectional_C1_costs",
    ):
        if verdict.get(key) != "CERTIFIED":
            errors.append(f"positive verdict mismatch: {key}")
    if verdict.get("complete_C_fw_C_rev_and_recovery") != "NOT_CERTIFIED":
        errors.append("complete cost/recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_endpoint_rank_first_order_cost_cert as cert
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
        print("GATE45_ENDPOINT_RANK_FIRST_ORDER_COST_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["endpoint_rank_tail_and_first_order_cost"][
            "endpoint_tail"
        ]["tail_exponent_in_dyadic_rank"] = "3"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (rank-tail tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["complete_numeric_C_fw_C_rev"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported complete costs accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  endpoint-rank tail tamper rejected")
        print("  unsupported complete C_fw/C_rev rejected")
        return 0
    print("GATE45_ALL_128_ENDPOINT_SIMPLE_GERMS: CERTIFIED")
    print("GATE45_GLOBAL_ENDPOINT_RANK_TAIL_EXPONENT_TWO: CERTIFIED")
    print("GATE45_FIRST_ORDER_BIDIRECTIONAL_C1_COSTS: CERTIFIED")
    if args.integrity_only:
        print("GATE45_ENDPOINT_RANK_FIRST_ORDER_COST_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
