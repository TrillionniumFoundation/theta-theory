#!/usr/bin/env python3
"""Fail-closed verifier for the global finite-Borel event current."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.global-borel-current-assembly.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_global_borel_current_assembly_cert.py"


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
    if result.get("maximal_row_manifest") != (
        "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
    ):
        errors.append("maximal-row manifest binding mismatch")
    if result.get("maximal_row_registry_sha256") != (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    ):
        errors.append("maximal-row registry digest mismatch")

    assembly = result.get("current_assembly", {})
    for key, expected in {
        "maximal_row_current_count": 64,
        "current_rows_sha256": "90b7e85dcea38b6b90e9ae57e7943030d7d205e0e5b3dce57721e3231953621d",
    }.items():
        if assembly.get(key) != expected:
            errors.append(f"current assembly mismatch: {key}")
    for key in (
        "positive_coarea_law_attached_to_every_row",
        "strict_hit_and_miss_trace_attached_to_every_row",
        "one_shared_plus_minus_mark_per_occurrence",
    ):
        if assembly.get(key) is not True:
            errors.append(f"missing current assembly flag: {key}")

    envelope = result.get("uniform_finite_measure_envelope", {})
    for key, expected in {
        "active_source_target_pair_count": 64,
        "maximum_relative_center_squared": "1362001/160000",
        "all_relative_center_distances_strictly_below": "6",
        "minimum_squared_circle_separation_margin": "36337/160000",
        "center_gap_lower_bound": "36337/1043200",
        "target_tangent_flight_squared_lower_bound": "36337/3260000",
        "target_tangent_flight_strict_lower_bound": "1/10",
        "unnormalized_coarea_density_upper_bound_wrt_dtheta": "18/5",
        "circle_length_upper_bound": "7",
        "per_row_positive_mass_upper_bound": "126/5",
        "global_positive_mass_upper_bound": "8064/5",
        "global_event_current_TV_upper_bound": "16128/5",
        "relative_center_bound_rows_sha256": "4655224b7880cac92fe22712cbb45917acc9c26ee0d268a9f3b182f55606a890",
    }.items():
        if envelope.get(key) != expected:
            errors.append(f"finite envelope mismatch: {key}")
    try:
        if Fraction(envelope["global_positive_mass_upper_bound"]) != (
            assembly["maximal_row_current_count"]
            * Fraction(envelope["per_row_positive_mass_upper_bound"])
        ):
            errors.append("global positive-mass identity mismatch")
        if Fraction(envelope["global_event_current_TV_upper_bound"]) != (
            2 * Fraction(envelope["global_positive_mass_upper_bound"])
        ):
            errors.append("global TV identity mismatch")
        if Fraction(envelope["target_tangent_flight_squared_lower_bound"]) <= Fraction(1, 100):
            errors.append("flight lower bound is insufficient")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid finite-envelope arithmetic")

    pairing = result.get("exact_Jx_scalar_pairing", {})
    for key, expected in {
        "exact_Jx_maximal_row_pair_count": 32,
        "global_signed_scalar_coarea_mass": "0",
        "constant_test_event_current_pairing": "0 rowwise by (+1,-1)",
        "Jx_pair_rows_sha256": "11ee023e90fa2be2c318ad28c1691f6407eadf6b9a901b7543e4fdbe33ee6abb",
    }.items():
        if pairing.get(key) != expected:
            errors.append(f"Jx pairing mismatch: {key}")
    for key in (
        "all_positive_coarea_laws_pair_by_exact_pushforward",
        "all_pair_polarities_are_opposite",
    ):
        if pairing.get(key) is not True:
            errors.append(f"missing Jx pairing flag: {key}")

    typing = result.get("endpoint_and_test_typing", {})
    for key, expected in {
        "extra_endpoint_atoms": 0,
        "global_current_type": "finite signed Borel measure on compactified collision space",
        "displayed_TV_constant": "16128/5",
    }.items():
        if typing.get(key) != expected:
            errors.append(f"test typing mismatch: {key}")
    if typing.get("arbitrary_bounded_Borel_test_pairing") is not True:
        errors.append("bounded-Borel test pairing missing")

    limits = result.get("scope_limits", {})
    for key in (
        "maximal_connected_event_rows_imported",
        "positive_coarea_law_attached_to_every_maximal_row",
        "global_finite_Borel_event_current_assembled",
        "arbitrary_bounded_Borel_test_pairing",
        "global_signed_scalar_coarea_matching",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "full_transfer_difference_quotient_convergence",
        "fixed_core_differentiability",
        "dynamic_C1_test_CM2_bound",
        "forward_reverse_standard_family_costs",
        "stopped_parent_recovery",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("global_finite_Borel_event_current") != "CERTIFIED":
        errors.append("global Borel current verdict mismatch")
    if verdict.get("global_signed_scalar_coarea_matching") != "CERTIFIED":
        errors.append("global scalar verdict mismatch")
    if verdict.get("full_transfer_DQ_and_CM2_norms") != "NOT_CERTIFIED":
        errors.append("full DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_global_borel_current_assembly_cert as cert
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
        print("GATE3_GLOBAL_BOREL_CURRENT_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["uniform_finite_measure_envelope"][
            "global_event_current_TV_upper_bound"
        ] = "0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (TV tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"][
            "full_transfer_difference_quotient_convergence"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported DQ completion accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  TV-envelope tamper rejected")
        print("  unsupported DQ completion rejected")
        return 0
    print("GATE3_GLOBAL_FINITE_BOREL_EVENT_CURRENT: CERTIFIED")
    print("GATE3_GLOBAL_SIGNED_SCALAR_COAREA_MATCHING: CERTIFIED")
    if args.integrity_only:
        print("GATE3_GLOBAL_BOREL_CURRENT_INTEGRITY: PASS")
        return 0
    print("GATE3_FULL_TRANSFER_DQ_AND_CM2_NORMS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
