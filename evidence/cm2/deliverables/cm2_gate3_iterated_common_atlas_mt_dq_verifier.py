#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 iterated common-atlas frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.iterated-common-atlas-mt-dq.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.iterated-common-atlas-mt-dq.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate3-iterated-common-atlas-mt-dq-manifest-2026-07-16.json"
CERTIFICATE = HERE / "cm2_gate3_iterated_common_atlas_mt_dq_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


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
    if not isinstance(dependencies, dict) or len(dependencies) != 5:
        errors.append("dependency ledger mismatch")
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
    digest = result.get("internal_replay_digest")
    digest_payload = copy.deepcopy(result)
    digest_payload.pop("internal_replay_digest", None)
    if digest != canonical_digest(digest_payload):
        errors.append("internal replay digest mismatch")

    common = result.get("common_mass_coordinate_atlas", {})
    expected_common = {
        "depth_two_component_count": 256,
        "all_finite_cutoffs_component_indexed": True,
        "boundary_Z_exponent": "1",
        "uniform_total_positive_mass_upper": "8064/5",
        "uniform_graph_current_TV_upper": "16128/5",
    }
    for key, expected in expected_common.items():
        if common.get(key) != expected:
            errors.append(f"common mass-atlas mismatch: {key}")
    cutoff_rows = common.get("cutoff_rows")
    if not isinstance(cutoff_rows, list) or len(cutoff_rows) != 13:
        errors.append("cutoff row ledger mismatch")
    else:
        for level, row in enumerate(cutoff_rows):
            expected_coefficient = Fraction(32256, 5) * ((1 << level) + 1)
            if row.get("cutoff_level") != level:
                errors.append(f"cutoff level mismatch: {level}")
            if row.get("component_count") != 64 * (1 << level):
                errors.append(f"cutoff component count mismatch: {level}")
            if row.get("boundary_component_count") != 64 * ((1 << level) + 1):
                errors.append(f"cutoff boundary count mismatch: {level}")
            if row.get("graph_current_boundary_collar_linear_coefficient") != str(expected_coefficient):
                errors.append(f"cutoff collar arithmetic mismatch: {level}")
        if common.get("cutoff_rows_sha256") != canonical_digest(cutoff_rows):
            errors.append("cutoff rows digest mismatch")

    depth_two = result.get("genuine_depth_two_miss_trace_registry", {})
    for key, expected in {
        "row_count": 64,
        "parameter_value": "s=0",
        "endpoint_absolute_inward_angular_trim_each_side": "1/1048576",
        "endpoint_cemetery_positive_mass_upper": "9/20480",
        "endpoint_cemetery_graph_TV_upper": "9/10240",
        "this_is_not_the_formal_telescope": True,
    }.items():
        if depth_two.get(key) != expected:
            errors.append(f"depth-two registry mismatch: {key}")
    try:
        certified = Fraction(depth_two["certified_normalized_row_length"])
        unresolved = Fraction(depth_two["unresolved_normalized_row_length"])
        fraction = Fraction(depth_two["unresolved_fraction_of_64_row_domain"])
        if certified <= 0 or unresolved <= 0 or certified + unresolved != 64:
            errors.append("depth-two row-length partition mismatch")
        if fraction != unresolved / 64:
            errors.append("depth-two unresolved fraction mismatch")
        if depth_two.get("certified_leaf_count", 0) <= 0:
            errors.append("empty certified depth-two registry")
        if depth_two.get("unresolved_leaf_count", 0) <= 0:
            errors.append("missing fail-closed unresolved strips")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("invalid depth-two rational ledger")
    for key in ("certified_rows_sha256", "unresolved_rows_sha256"):
        value = depth_two.get(key)
        if not isinstance(value, str) or len(value) != 64:
            errors.append(f"depth-two digest malformed: {key}")
    reasons = depth_two.get("unresolved_reason_counts", {})
    if not isinstance(reasons, dict) or sum(reasons.values()) != depth_two.get("unresolved_leaf_count"):
        errors.append("unresolved reason ledger mismatch")
    for key in (
        "unresolved_box_union_is_finite_resolution_outer_cover",
        "no_positive_length_claim_for_actual_singularity_set",
    ):
        if depth_two.get(key) is not True:
            errors.append(f"missing outer-cover scope guard: {key}")

    analytic = result.get("analytic_s0_second_singularity_audit", {})
    for key, expected in {
        "parameter_value": "s=0",
        "candidate_discriminant_function_count": 4704,
        "witness_rows_sha256": "1902970049f2b68b5c1edbaa4109a1a2ab1b3e9b20e688a18b0b45200b9605c3",
        "per_occurrence_rows_sha256": "c3570fa6b8c3faa0e262b7b5e7a4ebff694f9d63281767d6f6ff7747fa87a6e5",
        "explicit_interval_registry_coverage": "128399/131072",
    }.items():
        if analytic.get(key) != expected:
            errors.append(f"analytic singularity audit mismatch: {key}")
    for key in (
        "every_candidate_discriminant_has_a_strict_nonzero_Arb_witness",
        "finite_zero_set_per_candidate_on_every_compact_subarc",
        "second_collision_singular_set_is_discrete_on_each_open_row",
        "second_collision_singular_set_is_at_most_countable_on_open_rows",
        "actual_second_singularity_set_has_zero_row_length",
        "actual_second_singularity_set_has_zero_coarea_mass",
        "outer_cover_is_not_the_actual_singular_set",
    ):
        if analytic.get(key) is not True:
            errors.append(f"missing analytic singularity flag: {key}")

    strong = result.get("strong_source_frontier", {})
    if strong.get("fixed_time_branch_record_MT_DQ") is not False:
        errors.append("strong-source frontier overclaimed")
    missing = strong.get("missing_hypotheses")
    if not isinstance(missing, list) or len(missing) != 4:
        errors.append("strong-source missing-hypothesis ledger mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "moving_dyadic_endpoints_registered_on_depth_one_DQ_common_atlas",
        "all_finite_dyadic_cutoffs_component_indexed",
        "exact_boundary_Z_tightness_for_dyadic_record_boundaries",
        "genuine_s0_depth_two_miss_trace_registry_on_certified_components",
        "s0_depth_two_full_measure_component_atlas_modulo_discrete_singular_points",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "finite_s_genuine_depth_two_registry",
        "complete_depth_two_physical_domain",
        "strong_source_invariance",
        "fixed_time_branch_record_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME",
        "gate3_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    blockers = result.get("exact_remaining_blockers")
    if not isinstance(blockers, list) or len(blockers) != 5:
        errors.append("remaining blocker ledger mismatch")

    expected_verdict = {
        "moving_dyadic_common_DQ_atlas": "CERTIFIED",
        "explicit_s0_depth_two_box_registry": "PARTIALLY_CERTIFIED",
        "genuine_s0_depth_two_full_measure_atlas": "CERTIFIED",
        "finite_s_depth_two_registry": "NOT_CERTIFIED",
        "fixed_time_branch_record_MT_DQ": "NOT_CERTIFIED",
        "physical_FACE_2CUT_and_FACE_TIME": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_iterated_common_atlas_mt_dq_cert as cert
        actual = cert.build_manifest()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    tampered = copy.deepcopy(data)
    tampered["result"]["common_mass_coordinate_atlas"]["depth_two_component_count"] = 255
    mutations.append(("depth-two dyadic count", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["common_mass_coordinate_atlas"]["cutoff_rows"][2][
        "graph_current_boundary_collar_linear_coefficient"
    ] = "1"
    mutations.append(("boundary-Z coefficient", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["genuine_depth_two_miss_trace_registry"][
        "unresolved_normalized_row_length"
    ] = "0"
    mutations.append(("unresolved strip deletion", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["genuine_depth_two_miss_trace_registry"][
        "endpoint_cemetery_graph_TV_upper"
    ] = "0"
    mutations.append(("endpoint cemetery deletion", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["analytic_s0_second_singularity_audit"][
        "actual_second_singularity_set_has_zero_coarea_mass"
    ] = False
    mutations.append(("analytic zero-mass deletion", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"]["finite_s_genuine_depth_two_registry"] = True
    mutations.append(("finite-s depth-two overclaim", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"]["strong_source_invariance"] = True
    mutations.append(("strong-source overclaim", tampered))

    tampered = copy.deepcopy(data)
    tampered["result"]["scope_limits"]["gate3_certified"] = True
    mutations.append(("Gate-3 overclaim", tampered))

    tampered = copy.deepcopy(data)
    tampered["verdict"]["fixed_time_branch_record_MT_DQ"] = "CERTIFIED"
    mutations.append(("MT_DQ verdict overclaim", tampered))

    failed = []
    for name, mutation in mutations:
        if not check_structure(mutation):
            failed.append(name)
    if failed:
        print("SELF_TEST_FAILED:", ", ".join(failed))
        return 1
    print(f"SELF_TEST: PASS ({len(mutations)} mutations rejected)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    path = Path(args.manifest)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"INVALID_MANIFEST: {exc}")
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("INVALID:")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    print("MOVING_DYADIC_COMMON_DQ_ATLAS: CERTIFIED")
    print("EXPLICIT_S0_DEPTH_TWO_BOX_REGISTRY: PARTIALLY_CERTIFIED")
    print("GENUINE_S0_DEPTH_TWO_FULL_MEASURE_ATLAS: CERTIFIED")
    print("FINITE_S_DEPTH_TWO_REGISTRY: NOT_CERTIFIED")
    print("FIXED_TIME_BRANCH_RECORD_MT_DQ: NOT_CERTIFIED")
    print("PHYSICAL_FACE_2CUT_AND_FACE_TIME: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
