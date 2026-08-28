#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 product weak-Borel payload frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import cm2_gate4_product_borel_payload_frontier_cert as cert


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate4.product-borel-payload-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate4.product-borel-payload-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate4-product-borel-payload-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate4_product_borel_payload_frontier_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_summary() -> dict[str, Any]:
    return {
        "product_record_weak_Borel_payload": True,
        "corrected_current_Borel_Kac_payload": True,
        "height_nine_two_coordinate_coefficient": "36",
        "C_prod_dominates_weak_Borel_payload": True,
        "finite_s_physical_current_MT_DQ_match": False,
        "complete_CM2_strong_operator_ledger": False,
        "complete_numeric_C_fw_C_rev": False,
        "final_q": False,
        "gate4_certified": False,
    }


def expected_verdict() -> dict[str, str]:
    return {
        "product_record_weak_Borel_operator_test_payload": "CERTIFIED",
        "corrected_current_physical_Borel_Kac_payload": "CERTIFIED",
        "finite_s_physical_current_MT_DQ_match": "NOT_CERTIFIED",
        "complete_CM2_strong_operator_ledger": "NOT_CERTIFIED",
        "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
        "gate4": "NOT_CERTIFIED",
    }


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
    if data.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency ledger mismatch")
    else:
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    try:
        result = cert.certify()
    except Exception as exc:
        return errors + [f"certificate replay failed: {type(exc).__name__}: {exc}"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    if data.get("result_sha256") != cert.canonical_digest(result):
        errors.append("result digest mismatch")

    operator = result.get("weak_borel_operator_join", {})
    if operator.get("source_space") != (
        "M_b (finite signed Borel measures with total variation)"
    ):
        errors.append("weak source space mismatch")
    if operator.get("test_space") != "B_b (bounded Borel tests with sup norm)":
        errors.append("weak test space mismatch")
    for key in (
        "single_prefix_suffix_source_multiplier_upper",
        "single_prefix_suffix_test_multiplier_upper",
        "complete_disjoint_partition_source_multiplier_upper",
        "complete_disjoint_partition_test_multiplier_upper",
    ):
        if operator.get(key) != "1":
            errors.append(f"weak operator constant mismatch: {key}")
    if operator.get("tower_height_upper") != 9:
        errors.append("tower height mismatch")
    if operator.get("tower_source_or_test_multiplier_upper") != "9":
        errors.append("tower multiplier mismatch")
    if operator.get("product_record_weak_Borel_source_test_payload") != "CERTIFIED":
        errors.append("weak Borel payload verdict mismatch")
    if operator.get("physical_finite_s_current_or_MT_DQ_match") is not False:
        errors.append("finite-s current overclaim")

    kac = result.get("corrected_current_kac_join", {})
    expected_kac = {
        "occurrence_count": 64,
        "global_event_current_TV_upper": "16128/5",
        "global_two_coordinate_l1_TV_upper": "32256/5",
        "global_height_nine_lifted_pair_l1_TV_upper": "290304/5",
        "corrected_current_physical_Borel_Kac_payload": "CERTIFIED",
        "full_four_term_physical_CM2_Kac_output": False,
    }
    for key, value in expected_kac.items():
        if kac.get(key) != value:
            errors.append(f"corrected Kac join mismatch: {key}")

    payload = result.get("controlled_product_payload", {})
    if payload.get(
        "weak_Borel_height_nine_two_coordinate_coefficient_per_unit_occurrence_mass"
    ) != "36":
        errors.append("weak Borel payload coefficient mismatch")
    if payload.get("C_mesh") != "69986663973833932800":
        errors.append("C_mesh mismatch")
    if payload.get("payload_coefficient_strictly_below_C_mesh") is not True:
        errors.append("payload/C_mesh domination missing")
    if payload.get("clocked_depth_moment_strict_upper") != str(2 * 3**50):
        errors.append("clocked depth bound mismatch")
    if payload.get(
        "standalone_weak_Borel_payload_moment_strict_upper_per_unit_base_mass"
    ) != str(72 * 3**50):
        errors.append("standalone payload moment mismatch")
    if payload.get("existing_C_prod_envelope_already_dominates_coefficient_36") is not True:
        errors.append("C_prod domination mismatch")
    if payload.get("finite_s_product_record_weak_Borel_payload_envelope") != "CERTIFIED":
        errors.append("product weak payload verdict mismatch")
    if payload.get("physical_finite_s_signed_current_identification") != "NOT_CERTIFIED":
        errors.append("physical finite-s current scope mismatch")

    boundary = result.get("exact_nonpromotion_boundary", {})
    for key in (
        "TV_does_not_control_standard_family_Z",
        "TV_does_not_control_regular_density_variation",
        "Linf_does_not_control_dynamic_C1_inverse_pullback",
        "Borel_payload_does_not_supply_flux_face_atlas",
    ):
        if boundary.get(key) is not True:
            errors.append(f"nonpromotion guard missing: {key}")
    for key in (
        "Gate3_finite_s_common_branch_record_current_MT_DQ",
        "native_countable_time_zero_boundary_Z_finite",
        "arbitrary_or_unbounded_repeated_indicator_recovery",
        "complete_same_occurrence_CM2_strong_operator_ledger",
        "complete_C_fw",
        "complete_C_rev",
        "final_q_max_Cfw_Crev_2m",
        "gate4_certified",
    ):
        if boundary.get(key) is not False:
            errors.append(f"remaining-boundary overclaim: {key}")

    # Independent exact arithmetic for the joined constants.
    event = Q(16128, 5)
    if 2 * event != Q(32256, 5):
        errors.append("independent two-coordinate arithmetic failed")
    if 9 * 2 * event != Q(290304, 5):
        errors.append("independent height-nine arithmetic failed")
    if Q(36) >= Q(69986663973833932800):
        errors.append("independent C_mesh domination failed")
    if Q(36) * Q(2 * 3**50) != Q(payload.get(
        "standalone_weak_Borel_payload_moment_strict_upper_per_unit_base_mass",
        "0",
    )):
        errors.append("independent product payload moment failed")

    if data.get("replay_summary") != expected_summary():
        errors.append("replay summary mismatch")
    if data.get("replay_summary_sha256") != cert.canonical_digest(
        data.get("replay_summary", {})
    ):
        errors.append("replay summary digest mismatch")
    if data.get("verdict") != expected_verdict():
        errors.append("verdict mismatch")
    return errors


def mutation_self_test(baseline: dict[str, Any]) -> list[str]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        candidate["replay_summary_sha256"] = cert.canonical_digest(
            candidate.get("replay_summary", {})
        )
        cases.append((name, candidate))

    add("schema", lambda d: d.__setitem__("schema", "mutated"))
    add("certificate_hash", lambda d: d.__setitem__("certificate_sha256", "0" * 64))
    add("verifier_hash", lambda d: d.__setitem__("verifier_sha256", "0" * 64))
    add(
        "dependency_hash",
        lambda d: d["dependencies"].__setitem__(next(iter(d["dependencies"])), "0" * 64),
    )
    add("result_digest", lambda d: d.__setitem__("result_sha256", "0" * 64))
    add("weak_payload", lambda d: d["replay_summary"].__setitem__("product_record_weak_Borel_payload", False))
    add("kac_payload", lambda d: d["replay_summary"].__setitem__("corrected_current_Borel_Kac_payload", False))
    add("coefficient", lambda d: d["replay_summary"].__setitem__("height_nine_two_coordinate_coefficient", "18"))
    add("domination", lambda d: d["replay_summary"].__setitem__("C_prod_dominates_weak_Borel_payload", False))
    add("finite_s_overclaim", lambda d: d["replay_summary"].__setitem__("finite_s_physical_current_MT_DQ_match", True))
    add("strong_overclaim", lambda d: d["replay_summary"].__setitem__("complete_CM2_strong_operator_ledger", True))
    add("Cfw_overclaim", lambda d: d["replay_summary"].__setitem__("complete_numeric_C_fw_C_rev", True))
    add("q_overclaim", lambda d: d["replay_summary"].__setitem__("final_q", True))
    add("gate4_overclaim", lambda d: d["replay_summary"].__setitem__("gate4_certified", True))
    add("verdict_overclaim", lambda d: d["verdict"].__setitem__("gate4", "CERTIFIED"))
    add("strong_verdict", lambda d: d["verdict"].__setitem__("complete_CM2_strong_operator_ledger", "CERTIFIED"))
    return [name for name, candidate in cases if not check_structure(candidate)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"MANIFEST_READ: FAIL ({type(exc).__name__}: {exc})")
        raise SystemExit(1)
    errors = check_structure(data)
    if errors:
        for error in errors:
            print(f"VERIFY: FAIL: {error}")
        raise SystemExit(1)
    if args.self_test:
        failures = mutation_self_test(data)
        if failures:
            print("MUTATION_SELF_TEST: FAIL: " + ", ".join(failures))
            raise SystemExit(1)
        print("MUTATION_SELF_TEST: PASS (16/16 mutations rejected)")
        return
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return
    print("GATE4_PRODUCT_WEAK_BOREL_OPERATOR_TEST_PAYLOAD: CERTIFIED")
    print("GATE4_CORRECTED_CURRENT_BOREL_KAC_PAYLOAD: CERTIFIED")
    print("GATE4_FINITE_S_PHYSICAL_CURRENT_MT_DQ_MATCH: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
