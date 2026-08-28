#!/usr/bin/env python3
"""Fail-closed verifier for the product stopped-depth kernel."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.product-stopped-depth-kernel.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_product_stopped_depth_kernel_cert.py"


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
    if result.get("schema") != "cm2.gate45.product-stopped-depth-kernel.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "controlled_interval_algebra_manifest": (
            "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
        ),
        "curvature_log_density_cost_manifest": (
            "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
        ),
        "maximal_occurrence_count": 64,
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    cutoff = result.get("finite_cutoff_replay", {})
    for key, expected in {
        "checked_cutoffs": [4, 8, 16, 32, 64],
        "all_finite_cutoff_mass_identities_exact": True,
        "finite_cutoff_rows_sha256": (
            "2b792c75c285fd0804416185f4625d18d0ab9fefaa829a22d4a33ecda82b82ab"
        ),
    }.items():
        if cutoff.get(key) != expected:
            errors.append(f"finite-cutoff replay mismatch: {key}")

    kernel = result.get("mass_preserving_product_stopped_kernel", {})
    for key, expected in {
        "depth_probability": "w_K=(3/4)*4^-K, K>=0",
        "depth_tail": "P(K>=k)=4^-k",
        "tail_exponent_base_two": "2",
        "depth_K_atom_count": "2^K",
        "one_depth_K_atom_joint_mass": (
            "w_K*2^-K*m_e=(3/4)*8^-K*m_e"
        ),
        "atom_index": "j=floor(2^K*u_e), 0<=j<2^K",
        "row_marginal_identity": (
            "sum_K sum_j (3/4)*8^-K*m_e|I(K,j)=m_e"
        ),
        "same_K_j_mark_in_forward_and_reverse_views": True,
        "K_sampled_before_orientation_time_mode_and_final_test": True,
        "K_independent_of_physical_row_point_under_product_kernel": True,
        "exact_normalization_moment": "E[2^K]=3/2",
        "holder_depth_moment": "E[2^(5K/4)]<15/8",
        "holder_bound_uses": "2^(1/4)<6/5",
    }.items():
        if kernel.get(key) != expected:
            errors.append(f"product kernel mismatch: {key}")

    frontier = result.get("recovery_moment_factorization_frontier", {})
    for key, expected in {
        "finite_q_product_extension": (
            "d qhat(e,u,K)=d q(e,u)*(3/4)*4^-K"
        ),
        "q_marginal_preserved_exactly": True,
        "depth_only_target": "E_qhat[2^K]=3/2",
        "remaining_endpoint_factor": "E_q[exp(gamma*A1*B)]",
        "critical_K_tail_obstruction_removed_in_declared_policy": True,
        "native_dynamical_stopping_antichain_constructed": False,
        "physical_recovery_clock_constructed": False,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"recovery frontier mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "query_independent_mass_preserving_depth_kernel",
        "exact_supercritical_depth_tail",
        "finite_expected_parent_normalization_cost",
        "same_stopped_mark_for_both_orientations",
        "critical_depth_tail_obstruction_removed_in_controlled_policy",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "native_physical_stopping_antichain",
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
        "2b792c75c285fd0804416185f4625d18d0ab9fefaa829a22d4a33ecda82b82ab"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("mass_preserving_product_stopped_depth_kernel") != "CERTIFIED":
        errors.append("product stopped-depth verdict mismatch")
    if verdict.get("supercritical_depth_tail_and_E_2K") != "CERTIFIED":
        errors.append("supercritical depth-tail verdict mismatch")
    if verdict.get("native_physical_stopped_recovery") != "NOT_CERTIFIED":
        errors.append("native physical recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_product_stopped_depth_kernel_cert as cert
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
        print("GATE45_PRODUCT_STOPPED_DEPTH_KERNEL_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["mass_preserving_product_stopped_kernel"][
            "exact_normalization_moment"
        ] = "1"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (normalization moment tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["physical_recovery_clock"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported recovery clock accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  normalization-moment tamper rejected")
        print("  unsupported physical recovery clock rejected")
        return 0
    print("GATE45_MASS_PRESERVING_PRODUCT_STOPPED_DEPTH_KERNEL: CERTIFIED")
    print("GATE45_SUPERCRITICAL_DEPTH_TAIL_AND_E_2K: CERTIFIED")
    if args.integrity_only:
        print("GATE45_PRODUCT_STOPPED_DEPTH_KERNEL_INTEGRITY: PASS")
        return 0
    print("GATE45_NATIVE_PHYSICAL_STOPPED_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
