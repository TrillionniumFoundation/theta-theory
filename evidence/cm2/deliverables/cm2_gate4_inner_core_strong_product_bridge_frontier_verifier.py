#!/usr/bin/env python3
"""Verifier for the Gate-4 24-inner-core strong/product bridge frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import cm2_gate4_inner_core_strong_product_bridge_frontier_cert as cert


Q = Fraction
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
SCHEMA = "cm2.gate4.inner-core-strong-product-bridge-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.inner-core-strong-product-bridge-frontier.v1"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def expected_summary(result: dict[str, Any]) -> dict[str, Any]:
    strong = result["core_local_strong_multiplier"]
    growth = result["core_local_open_growth"]
    composition = result["product_composition_frontier"]
    obstruction = result["exact_physical_join_obstruction"]
    return {
        "inner_core_count": strong["inner_core_count"],
        "source_multiplier_norm_upper": strong[
            "core_union_characteristic_strong_operator_norm_upper"
        ],
        "restricted_contraction": strong[
            "core_restriction_then_physical_step_contraction"
        ],
        "restricted_margin": strong["core_restricted_contraction_margin"],
        "half_life_block": growth["half_life_block"],
        "abstract_terminal_composed_integral_upper": composition[
            "abstract_terminal_composed_integral_strict_upper_before_Z_N_inverse"
        ],
        "certified_core_to_occurrence_mapping_count": obstruction[
            "certified_core_to_64_occurrence_mapping_count"
        ],
        "normalized_core_clip_shape_supremum": obstruction[
            "sup_normalized_shape_cost_after_nonempty_core_clip"
        ],
        "complete_numeric_C_fw_C_rev": False,
        "final_q": False,
        "gate4_certified": False,
    }


def verify_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")

    strong = result.get("core_local_strong_multiplier", {})
    exact_strong = {
        "inner_core_count": 24,
        "cross_chart_and_within_chart_gap_audit": "CERTIFIED",
        "global_pairwise_source_normal_angle_gap_strict_lower": "1/100",
        "global_pairwise_source_r_gap_strict_lower": "1/625",
        "canonical_short_curve_meets_at_most_one_core": True,
        "retained_component_count_upper": 1,
        "new_endpoint_count_upper": 2,
        "core_union_characteristic_strong_operator_norm_upper": "2000/1999",
        "regularity_mark_type": (
            "the frozen scale-invariant log-density/dynamic regularity mark"
        ),
        "conditional_normalization_effect_on_regularity": (
            "normalizing rho restricted to I adds a carrierwise constant to "
            "log rho, so Reg_alpha is unchanged"
        ),
        "core_local_standard_family_source_multiplier": "CERTIFIED",
        "core_local_regular_density_restriction": "CERTIFIED",
        "core_restriction_then_physical_step_contraction": (
            "720269600000/720626832337"
        ),
        "core_restricted_contraction_margin": "357232337/720626832337",
        "core_local_open_Growth_contraction": "CERTIFIED",
    }
    for key, value in exact_strong.items():
        if strong.get(key) != value:
            errors.append(f"strong multiplier mismatch: {key}")

    ratio = Q(strong.get("core_union_characteristic_strong_operator_norm_upper", "0"))
    theta = Q(strong.get("physical_step_vartheta_p", "0"))
    restricted = Q(strong.get("core_restriction_then_physical_step_contraction", "0"))
    margin = Q(strong.get("core_restricted_contraction_margin", "0"))
    if ratio * theta != restricted or restricted >= 1 or 1 - restricted != margin:
        errors.append("restricted Growth rational arithmetic failed")

    growth = result.get("core_local_open_growth", {})
    if growth.get("substochastic_core_operator") != (
        "T_* o M_core: first clip the source by the fixed 24-core "
        "characteristic, then take one physical step"
    ):
        errors.append("core operator order mismatch")
    if growth.get("half_life_block") != 2018:
        errors.append("half-life block mismatch")
    if restricted**2018 >= Q(1, 2):
        errors.append("half-life inequality failed")
    if growth.get("uniform_normalized_shape_after_arbitrarily_small_clip") is not False:
        errors.append("normalized clip overclaim")
    expected_adapted_cp = (
        "2882507329348000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000/357232337"
    )
    expected_euclidean_cp = (
        "101608383359517000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000/357232337"
    )
    if growth.get("adapted_open_Growth_constant") != expected_adapted_cp:
        errors.append("adapted open Growth constant mismatch")
    if growth.get("euclidean_open_Growth_constant") != expected_euclidean_cp:
        errors.append("Euclidean open Growth constant mismatch")

    composition = result.get("product_composition_frontier", {})
    expected_integral = Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6707530956800,
    )
    expected_boundary = Q(209959991921501798400000, 1999)
    if Q(composition.get("abstract_terminal_composed_integral_strict_upper_before_Z_N_inverse", "0")) != expected_integral:
        errors.append("terminal composition integral mismatch")
    if Q(composition.get("abstract_terminal_composed_one_cut_boundary_upper", "0")) != expected_boundary:
        errors.append("terminal composition boundary mismatch")
    if composition.get("this_is_a_physical_core_to_occurrence_join") is not False:
        errors.append("physical composition overclaim")
    if composition.get("this_reuses_the_clock_after_a_pre_recovery_core_clip") is not False:
        errors.append("recovery-clock overclaim")

    obstruction = result.get("exact_physical_join_obstruction", {})
    exact_obstruction = {
        "certified_core_to_64_occurrence_mapping_count": 0,
        "immutable_same_restriction_forward_reverse_carrier_join": False,
        "sup_normalized_shape_cost_after_nonempty_core_clip": "infinity",
        "existing_K_only_recovery_clock_survives_pre_recovery_core_clip": False,
        "full_key_characteristic_Z": False,
        "Gate3_MT_DQ_physical_current_match": False,
        "complete_numeric_C_fw": False,
        "complete_numeric_C_rev": False,
        "final_same_occurrence_q": False,
        "gate4_certified": False,
        "audit_row_count": 24,
    }
    for key, value in exact_obstruction.items():
        if obstruction.get(key) != value:
            errors.append(f"join obstruction mismatch: {key}")

    core_manifest = json.loads(
        (HERE / "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json").read_text(encoding="utf-8")
    )
    rows = []
    for row in core_manifest["result"]["seeded_implicit_maximal_component_registry"]["rows"]:
        rows.append({
            "maximal_component_id": row["maximal_component_id"],
            "physical_key": row["definition"]["physical_key"],
            "certified_product_occurrence_id": None,
            "certified_forward_recovery_carrier_id": None,
            "certified_reverse_recovery_carrier_id": None,
        })
    rows.sort(key=canonical_json)
    if obstruction.get("audit_rows_sha256") != canonical_digest(rows):
        errors.append("audit-row digest mismatch")

    scope = result.get("scope_limits", {})
    expected_scope = {
        "core_local_standard_family_source_multiplier": True,
        "core_local_regular_density_restriction": True,
        "core_local_open_Growth_contraction": True,
        "abstract_post_recovery_product_composition_arithmetic": True,
        "physical_core_to_product_occurrence_join": False,
        "uniform_pre_recovery_core_clip_clock": False,
        "full_key_characteristic_Z": False,
        "complete_numeric_C_fw_C_rev": False,
        "final_same_occurrence_q": False,
        "gate4_certified": False,
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            errors.append(f"scope mismatch: {key}")
    return errors


def verify_manifest(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not MANIFEST.is_file():
        return ["manifest missing"]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema mismatch")
    if manifest.get("certificate_sha256") != sha256_path(
        HERE / "cm2_gate4_inner_core_strong_product_bridge_frontier_cert.py"
    ):
        errors.append("certificate SHA mismatch")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier SHA mismatch")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency map mismatch")
    for name, expected in cert.DEPENDENCIES.items():
        if sha256_path(HERE / name) != expected:
            errors.append(f"dependency SHA mismatch: {name}")
    if manifest.get("replay_summary") != expected_summary(result):
        errors.append("replay summary mismatch")
    verdict = manifest.get("verdict", {})
    expected_verdict = {
        "core_local_standard_family_source_multiplier": "CERTIFIED",
        "core_local_open_Growth_contraction": "CERTIFIED",
        "physical_core_to_product_occurrence_join": "NOT_CERTIFIED",
        "uniform_pre_recovery_core_clip_clock": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }
    if verdict != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def mutation_self_test() -> tuple[int, int]:
    base = cert.certify()
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def add(name: str, fn: Callable[[dict[str, Any]], None]) -> None:
        mutations.append((name, fn))

    add("core_count", lambda d: d["core_local_strong_multiplier"].__setitem__("inner_core_count", 25))
    add("cross_chart_gap", lambda d: d["core_local_strong_multiplier"].__setitem__("cross_chart_and_within_chart_gap_audit", "NOT_CERTIFIED"))
    add("multiplicity", lambda d: d["core_local_strong_multiplier"].__setitem__("retained_component_count_upper", 2))
    add("source_norm", lambda d: d["core_local_strong_multiplier"].__setitem__("core_union_characteristic_strong_operator_norm_upper", "1"))
    add("regularity_type", lambda d: d["core_local_strong_multiplier"].__setitem__("regularity_mark_type", "ordinary Holder density norm"))
    add("contraction", lambda d: d["core_local_strong_multiplier"].__setitem__("core_restriction_then_physical_step_contraction", "1"))
    add("operator_order", lambda d: d["core_local_open_growth"].__setitem__("substochastic_core_operator", "M_core o T_*"))
    add("half_life", lambda d: d["core_local_open_growth"].__setitem__("half_life_block", 1005))
    add("adapted_Cp", lambda d: d["core_local_open_growth"].__setitem__("adapted_open_Growth_constant", "1"))
    add("euclidean_Cp", lambda d: d["core_local_open_growth"].__setitem__("euclidean_open_Growth_constant", "1"))
    add("normalized_clip", lambda d: d["core_local_open_growth"].__setitem__("uniform_normalized_shape_after_arbitrarily_small_clip", True))
    add("integral", lambda d: d["product_composition_frontier"].__setitem__("abstract_terminal_composed_integral_strict_upper_before_Z_N_inverse", "1"))
    add("physical_join", lambda d: d["product_composition_frontier"].__setitem__("this_is_a_physical_core_to_occurrence_join", True))
    add("mapping", lambda d: d["exact_physical_join_obstruction"].__setitem__("certified_core_to_64_occurrence_mapping_count", 1))
    add("clock", lambda d: d["exact_physical_join_obstruction"].__setitem__("existing_K_only_recovery_clock_survives_pre_recovery_core_clip", True))
    add("digest", lambda d: d["exact_physical_join_obstruction"].__setitem__("audit_rows_sha256", "0" * 64))
    add("gate4", lambda d: d["scope_limits"].__setitem__("gate4_certified", True))

    rejected = 0
    for _, mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        if verify_result(candidate):
            rejected += 1
    return rejected, len(mutations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        rejected, total = mutation_self_test()
        print(f"MUTATION_SELF_TEST: {rejected}/{total} REJECTED")
        raise SystemExit(0 if rejected == total else 1)

    result = cert.certify()
    errors = verify_result(result) + verify_manifest(result)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("REPLAY_INTEGRITY: PASS")
    print("GATE4_24_CORE_LOCAL_STRONG_MULTIPLIER: CERTIFIED")
    print("GATE4_24_CORE_LOCAL_OPEN_GROWTH: CERTIFIED")
    print("GATE4_PHYSICAL_CORE_TO_PRODUCT_OCCURRENCE_JOIN: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    if args.replay or args.integrity_only:
        raise SystemExit(0)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
