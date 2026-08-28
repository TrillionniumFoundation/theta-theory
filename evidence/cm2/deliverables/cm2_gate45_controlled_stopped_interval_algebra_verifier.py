#!/usr/bin/env python3
"""Fail-closed verifier for the controlled stopped interval algebra."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.controlled-stopped-interval-algebra.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate45_controlled_stopped_interval_algebra_cert.py"


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
    if result.get("schema") != "cm2.gate45.controlled-stopped-interval-algebra.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "corrected_DQ_manifest": (
            "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
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

    algebra = result.get("dyadic_mass_coordinate_algebra", {})
    for key, expected in {
        "atom_mass_fraction": "2^-K",
        "finite_level_boolean_algebra": True,
        "countable_nested_union_boolean_algebra": True,
        "exhaustive_small_depth_rows_sha256": (
            "ac64385675bf7a58a1292d4db30b7c699ed2d7a45dc0452aa67544bfe09cd990"
        ),
    }.items():
        if algebra.get(key) != expected:
            errors.append(f"dyadic algebra mismatch: {key}")
    exhaustive = algebra.get("exhaustive_small_depth_rows")
    if not isinstance(exhaustive, list) or len(exhaustive) != 5:
        errors.append("small-depth exhaustive ledger mismatch")

    trim = result.get("exact_trim_and_cemetery_ledger", {})
    for key, expected in {
        "checked_depth_range": [2, 10],
        "trim_identity_row_count": 45,
        "all_trim_mass_identities_exact": True,
        "trim_rows_sha256": (
            "29fca89f1bd410e0a671a17188d1f24f2f13dc00e28d9afa0c80b5b69e148062"
        ),
    }.items():
        if trim.get(key) != expected:
            errors.append(f"trim ledger mismatch: {key}")

    rows = result.get("all_maximal_row_contracts", {})
    for key, expected in {
        "maximal_occurrence_count": 64,
        "canonical_mass_coordinate_count": 64,
        "row_contracts_sha256": (
            "788397f435056033454ae17fcfb0a671f021796cc43cdc6c48a96e59d3c3149a"
        ),
    }.items():
        if rows.get(key) != expected:
            errors.append(f"row contract mismatch: {key}")
    for key in (
        "one_corrected_m_and_one_q_expression_per_occurrence",
        "same_atom_transport_in_forward_and_reverse_views",
    ):
        if rows.get(key) is not True:
            errors.append(f"missing row contract flag: {key}")

    policy = result.get("controlled_stopped_policy", {})
    for key, expected in {
        "maximum_interval_components_per_row": "2^K",
        "minimum_nonzero_restricted_mass": "2^-K*m_e(row)",
        "maximum_parent_normalization_cost": "2^K",
        "two_sided_cemetery_mass": "2^(1-L)*m_e(row)",
        "fat_cantor_restrictions_admissible": False,
        "fat_cantor_obstruction_removed_inside_declared_policy": True,
    }.items():
        if policy.get(key) != expected:
            errors.append(f"controlled policy mismatch: {key}")
    sample = policy.get("sample_ledger", {})
    for key, expected in {
        "K": 8,
        "L": 4,
        "atoms_per_row": 256,
        "core_atoms_per_row": 224,
        "total_core_atoms_all_rows": 14336,
        "total_cemetery_mass_fraction_per_row": "1/8",
        "maximum_normalization_cost": 256,
    }.items():
        if sample.get(key) != expected:
            errors.append(f"sample policy mismatch: {key}")
    try:
        if Fraction(sample["total_cemetery_mass_fraction_per_row"]) != Fraction(1, 8):
            errors.append("sample cemetery arithmetic mismatch")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid sample policy arithmetic")

    boundary = result.get("recovery_boundary", {})
    if boundary.get("controlled_interval_algebra_is_not_recovery") is not True:
        errors.append("algebra/recovery distinction missing")
    if boundary.get("arbitrary_Borel_stopped_recovery") is not False:
        errors.append("arbitrary Borel recovery must remain false")
    if boundary.get("controlled_dyadic_stopped_recovery") is not False:
        errors.append("dyadic physical recovery must remain false")
    missing = boundary.get("still_missing")
    if not isinstance(missing, list) or len(missing) != 6:
        errors.append("remaining recovery ledger mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "corrected_row_laws_imported",
        "countable_nested_dyadic_interval_algebra",
        "finite_component_and_normalization_cost_at_declared_depth",
        "exact_trimmed_core_and_cemetery_mass",
        "same_restriction_transported_in_both_oriented_views",
        "fat_cantor_restrictions_excluded",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "numeric_forward_reverse_costs",
        "controlled_stopped_parent_recovery",
        "CM2_norm_lifts",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("controlled_dyadic_stopped_interval_algebra") != "CERTIFIED":
        errors.append("controlled algebra verdict mismatch")
    if verdict.get("fat_cantor_obstruction_inside_policy") != "REMOVED":
        errors.append("fat-Cantor policy verdict mismatch")
    if verdict.get("physical_stopped_recovery_and_CM2_norms") != "NOT_CERTIFIED":
        errors.append("physical recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_controlled_stopped_interval_algebra_cert as cert
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
        print("GATE45_CONTROLLED_STOPPED_INTERVAL_ALGEBRA_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["controlled_stopped_policy"][
            "maximum_parent_normalization_cost"
        ] = "1"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (normalization tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"][
            "controlled_stopped_parent_recovery"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  normalization-cost tamper rejected")
        print("  unsupported physical recovery rejected")
        return 0
    print("GATE45_CONTROLLED_DYADIC_STOPPED_INTERVAL_ALGEBRA: CERTIFIED")
    print("GATE45_FAT_CANTOR_RESTRICTION_OBSTRUCTION_IN_POLICY: REMOVED")
    if args.integrity_only:
        print("GATE45_CONTROLLED_STOPPED_INTERVAL_ALGEBRA_INTEGRITY: PASS")
        return 0
    print("GATE45_PHYSICAL_STOPPED_RECOVERY_AND_CM2_NORMS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
