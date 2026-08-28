#!/usr/bin/env python3
"""Fail-closed verifier for the moving-test/telescope frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.moving-test-telescope-frontier.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-moving-test-telescope-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_moving_test_telescope_frontier_cert.py"


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
    if result.get("schema") != "cm2.gate3.moving-test-telescope-frontier.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "depth_one_DQ_manifest": (
            "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
        ),
        "density_mesh_recovery_manifest": (
            "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    moving = result.get("depth_one_strong_moving_test_upgrade", {})
    for key, expected in {
        "depth_one_norm_convergence": (
            "L_s(h)=(P_s-P_0)h/s converges to D_0 h in (C^{1,alpha})*"
        ),
        "moving_test_hypothesis": (
            "Phi_s->Phi_0 in C^{1,alpha} for one fixed C^1 source h"
        ),
        "uniform_boundedness_reason": (
            "norm convergence of L_s(h) implies sup_s ||L_s(h)||<infinity"
        ),
        "uncentered_depth_one_strong_moving_test_DQ": True,
        "centered_depth_one_strong_moving_test_DQ": True,
        "source_is_fixed_not_s_dependent": True,
    }.items():
        if moving.get(key) != expected:
            errors.append(f"moving-test upgrade mismatch: {key}")

    telescope = result.get("fixed_time_noncommutative_telescope", {})
    for key, expected in {
        "checked_fixed_depth_range": [1, 64],
        "exact_noncommutative_telescope": (
            "(P_s^n-P_0^n)/s=sum_(j=0)^(n-1) "
            "P_s^(n-1-j)*((P_s-P_0)/s)*P_0^j"
        ),
        "all_mixed_noncommutative_words_cancel": True,
        "telescope_rows_sha256": (
            "94577905a41c8acc5d68508dbb21cb34819b201fee3070062a2201701b6b1c7d"
        ),
    }.items():
        if telescope.get(key) != expected:
            errors.append(f"telescope mismatch: {key}")

    frontier = result.get("exact_MT_DQ_frontier", {})
    if frontier.get("fixed_time_telescope_algebra_complete") is not True:
        errors.append("fixed-time telescope frontier flag missing")
    if frontier.get("depth_one_strong_moving_tests_complete") is not True:
        errors.append("depth-one moving-test frontier flag missing")
    for key in (
        "fixed_time_dynamic_branch_record_MT_DQ",
        "full_three_space_MT_DQ",
        "CM2_time_decay_majorant",
    ):
        if frontier.get(key) is not False:
            errors.append(f"unsupported MT_DQ frontier flag: {key}")
    if len(frontier.get("still_missing", [])) != 5:
        errors.append("exact MT_DQ missing ledger mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "depth_one_strong_moving_test_DQ",
        "fixed_time_DQ_telescope_algebra",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "fixed_time_dynamic_branch_record_MT_DQ",
        "uniform_finite_s_moving_face_recovery",
        "full_three_space_MT_DQ",
        "CM2_time_decay_majorant",
        "CM2_norm_lifts",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if result.get("internal_replay_digest") != (
        "94577905a41c8acc5d68508dbb21cb34819b201fee3070062a2201701b6b1c7d"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("depth_one_strong_moving_test_DQ") != "CERTIFIED":
        errors.append("moving-test verdict mismatch")
    if verdict.get("fixed_time_noncommutative_DQ_telescope") != "CERTIFIED":
        errors.append("telescope verdict mismatch")
    if verdict.get("dynamic_branch_record_full_MT_DQ") != "NOT_CERTIFIED":
        errors.append("full MT_DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_moving_test_telescope_frontier_cert as cert
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
        print("GATE3_MOVING_TEST_TELESCOPE_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["fixed_time_noncommutative_telescope"][
            "all_mixed_noncommutative_words_cancel"
        ] = False
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (telescope tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["full_three_space_MT_DQ"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported full MT_DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  telescope tamper rejected")
        print("  unsupported full MT_DQ rejected")
        return 0
    print("GATE3_DEPTH_ONE_STRONG_MOVING_TEST_DQ: CERTIFIED")
    print("GATE3_FIXED_TIME_NONCOMMUTATIVE_DQ_TELESCOPE: CERTIFIED")
    if args.integrity_only:
        print("GATE3_MOVING_TEST_TELESCOPE_FRONTIER_INTEGRITY: PASS")
        return 0
    print("GATE3_DYNAMIC_BRANCH_RECORD_FULL_MT_DQ: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
