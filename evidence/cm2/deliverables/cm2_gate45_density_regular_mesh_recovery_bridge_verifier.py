#!/usr/bin/env python3
"""Fail-closed verifier for the density mesh and recovery bridge."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.density-regular-mesh-recovery-bridge.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_density_regular_mesh_recovery_bridge_cert.py"


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
    if result.get("schema") != "cm2.gate45.density-regular-mesh-recovery-bridge.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "curvature_log_density_manifest": (
            "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
        ),
        "product_stopped_depth_manifest": (
            "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
        ),
        "endpoint_rank_manifest": (
            "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    mesh = result.get("density_regular_endpoint_mesh", {})
    for key, expected in {
        "checked_shell_rank_range": [14, 64],
        "canonical_mesh": (
            "delta_b=2^-ceil(3(b+1)/2) in carrier arclength"
        ),
        "mesh_scale_contract": "delta_b^2<=2^-3(b+1)",
        "common_shell_carrier_length_upper": "8192*2^-b",
        "piece_count_upper": "32769*2^ceil(b/2)",
        "common_density_upper_on_zero_shell": "23*2^-b",
        "one_zero_endpoint_Z_numerator_series_upper": "753687/32",
        "one_zero_endpoint_Z_series_is_summable": True,
        "density_mesh_rows_sha256": (
            "53db99fcb31ccb266999259ddd2e48bdee1b5757b94cdb25c03a37f8dff83e40"
        ),
    }.items():
        if mesh.get(key) != expected:
            errors.append(f"density mesh mismatch: {key}")

    standard = result.get("oriented_standard_family_contract", {})
    for key, expected in {
        "density_zero_endpoint_counts": {
            "source_reverse_view": 48,
            "miss_forward_view": 48,
        },
        "uniform_log_Hoelder_constant_on_endpoint_mesh": "52",
        "uniform_carrier_C2_upper": "4949",
        "fixed_global_unstable_cone": (
            "25/9<dphi/dr<4108425/145348"
        ),
        "common_row_mass_strict_lower": "169/2147483648000",
        "orientation_specific_decompositions_allowed": True,
        "same_restricted_measure_and_same_K_j_record_in_both_views": True,
        "single_depth_K_atom_initial_standard_family_boundary": (
            "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K"
        ),
        "C_mesh_is_finite_and_table_dependent": True,
    }.items():
        if standard.get(key) != expected:
            errors.append(f"standard-family contract mismatch: {key}")

    recovery = result.get("closed_map_growth_lemma_recovery_bridge", {})
    for key, expected in {
        "imported_closed_map_theorem": (
            "Canestrari arXiv:2604.19671v2 Lemma 6.14 "
            "(Growth Lemma; based on Demers 2014 Lemma 8.4)"
        ),
        "growth_recurrence": (
            "Z(F^((p+1)n_*)G)<=theta*Z(F^(p n_*)G)+Z_0, 0<theta<1"
        ),
        "forward_and_reverse_use_time_reversibility": True,
        "closed_map_recovery_clock": "R_fw(K,j)+R_rev(K,j)<=A0+A1*K",
        "A0_A1_are_finite_table_dependent_constants": True,
        "controlled_s0_stopped_parent_recovery": True,
        "uniform_finite_s_moving_face_recovery_majorant": False,
        "hereditary_recovery_after_repeated_indicator_cuts": False,
    }.items():
        if recovery.get(key) != expected:
            errors.append(f"growth-lemma bridge mismatch: {key}")
    expected_hypotheses = [
        "unstable cone alignment",
        "uniform C2 carrier bound",
        "uniform one-third log-Hoelder density",
        "finite initial boundary Z<=C_mesh*2^K",
    ]
    if recovery.get("hypotheses_verified_for_each_oriented_stopped_atom") != expected_hypotheses:
        errors.append("growth-lemma hypothesis ledger mismatch")

    literature = result.get("latest_literature_boundary", {})
    if literature.get("latest_review") != (
        "Demers--Liverani, Recent Progress in the Application of "
        "Transfer Operators to Dispersing Billiards, arXiv:2606.10155v1"
    ):
        errors.append("latest review mismatch")
    if literature.get("review_date") != "2026-06-08":
        errors.append("latest review date mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "summable_density_regular_endpoint_mesh",
        "uniform_standard_pair_density_and_C2_constants",
        "normalized_atom_boundary_Z_at_most_exponential_in_K",
        "controlled_s0_stopped_parent_recovery",
        "finite_depth_plus_recovery_moment_for_some_gamma",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "uniform_finite_s_moving_face_recovery",
        "hereditary_recovery_under_repeated_arbitrary_indicators",
        "complete_numeric_C_fw_C_rev",
        "full_dynamic_MT_DQ",
        "CM2_norm_lifts",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if result.get("internal_replay_digest") != (
        "53db99fcb31ccb266999259ddd2e48bdee1b5757b94cdb25c03a37f8dff83e40"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("density_regular_endpoint_mesh") != "CERTIFIED":
        errors.append("density mesh verdict mismatch")
    if verdict.get("controlled_s0_stopped_parent_recovery") != "CERTIFIED":
        errors.append("s0 recovery verdict mismatch")
    if verdict.get("uniform_finite_s_recovery_and_full_MT_DQ") != "NOT_CERTIFIED":
        errors.append("finite-s recovery/MT_DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_density_regular_mesh_recovery_bridge_cert as cert
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
        print("GATE45_DENSITY_MESH_RECOVERY_BRIDGE_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["density_regular_endpoint_mesh"][
            "one_zero_endpoint_Z_series_is_summable"
        ] = False
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (Z-series tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"][
            "uniform_finite_s_moving_face_recovery"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported finite-s recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  Z-series tamper rejected")
        print("  unsupported finite-s recovery rejected")
        return 0
    print("GATE45_DENSITY_REGULAR_ENDPOINT_MESH: CERTIFIED")
    print("GATE45_CONTROLLED_S0_STOPPED_PARENT_RECOVERY: CERTIFIED")
    if args.integrity_only:
        print("GATE45_DENSITY_MESH_RECOVERY_BRIDGE_INTEGRITY: PASS")
        return 0
    print("GATE45_UNIFORM_FINITE_S_RECOVERY_AND_FULL_MT_DQ: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
