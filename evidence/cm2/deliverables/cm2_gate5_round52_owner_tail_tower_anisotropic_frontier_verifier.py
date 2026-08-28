#!/usr/bin/env python3
"""Fail-closed verifier for the Round-52 Gate-5 owner/tower/F17 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round52_owner_tail_tower_anisotropic_frontier_cert as cert


HERE = Path(__file__).resolve().parent
RHO = Q(111718729, 111718750) ** 9148
W_Z = (1 + 1 / RHO) / 2
KAPPA_THRESHOLD = 1 / W_Z


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        fixed = result["fixed_insertion_same_ID_owner_tail_transfer"]
        mass = Q(8064, 5)
        tail = Q(9158592, 6875)
        rank_l1 = (1 << 14) * mass + tail * Q(1, 1 << 13)
        forward = 68 * rank_l1
        reverse = 35 * rank_l1
        total = forward + reverse
        if rank_l1 != Q(23253221519103, 880000):
            errors.append("independent rank L1")
        if fixed["transferred_integral_2^B_strict_upper"] != str(rank_l1):
            errors.append("transferred rank L1")
        if fixed["transferred_forward_F10_L1_strict_upper"] != str(forward):
            errors.append("transferred forward")
        if fixed["transferred_reverse_F10_L1_strict_upper"] != str(reverse):
            errors.append("transferred reverse")
        if fixed["transferred_bidirectional_F10_L1_strict_upper"] != str(total):
            errors.append("transferred total")
        expected_operations = [
            {
                "operation": "restrict_to_regular_Rn_record",
                "measure_effect": "1_R*m_occ<=m_occ",
                "can_increase_positive_tail": False,
            },
            {
                "operation": "owner_minimization",
                "measure_effect": "owner set is a measurable subset of active representations",
                "can_increase_positive_tail": False,
            },
            {
                "operation": "sum_disjoint_owner_selected_source_pieces",
                "measure_effect": "marked source total and source-rank tail are <= those of m_occ",
                "can_increase_positive_tail": False,
            },
            {
                "operation": "finite_regular_suffix_pushforward",
                "measure_effect": (
                    "record total mass and retained source-rank mark are preserved; "
                    "common-target-set domination is not claimed"
                ),
                "can_increase_positive_tail": False,
            },
        ]
        if fixed["operations"] != expected_operations:
            errors.append("transfer operations")
        if fixed["operations_sha256"] != cert.digest(expected_operations):
            errors.append("transfer operations digest")
        if fixed["transfer_constant"] != "1":
            errors.append("transfer constant")
        if fixed["arbitrary_finite_regular_suffix_TV_scope"] is not True:
            errors.append("suffix scope")
        if fixed["target_Borel_set_domination_after_distinct_suffixes"] is not False:
            errors.append("target Borel domination overclaim")
        if fixed["uniform_in_j_bound_has_decay_in_j"] is not False:
            errors.append("time decay overclaim")
        if fixed["sums_over_insertion_times"] is not False:
            errors.append("insertion sum overclaim")
        if fixed["return_depth_face_tower_moment"] != "NOT_CERTIFIED":
            errors.append("fixed transfer tower promotion")
        if fixed["status"] != (
            "CERTIFIED_FIXED_INSERTION_SAME_ID_OWNER_TAIL_TRANSFER_ONLY"
        ):
            errors.append("fixed transfer status")

        tower = result["null_survivor_face_tower_countermodel"]
        rho = RHO
        w = W_Z
        threshold = KAPPA_THRESHOLD
        if not Q(0) < rho < 1:
            errors.append("rho range")
        if w * rho != (1 + rho) / 2 or not w * rho < 1:
            errors.append("forcing series")
        expected_tower_rows = []
        for p in (0, 1, 4, 16):
            expected_tower_rows.append(
                {
                    "block_index": p,
                    "collision_survivor_mass": "1" if p == 0 else f"rho^{p}",
                    "trace_survivor_mass": "1",
                    "constant_rank": 14,
                    "owner_ZB_charge": "16384",
                }
            )
        if tower["rows"] != expected_tower_rows:
            errors.append("tower rows")
        if tower["rows_sha256"] != cert.digest(expected_tower_rows):
            errors.append("tower digest")
        if tower["threshold_fraction_binary_sha256"] != cert.fraction_digest(
            threshold
        ):
            errors.append("tower threshold digest")
        if tower["owner_charge_sequence"] != "b_p=2^14 for every p":
            errors.append("tower charge")
        if tower["minimal_asymptotic_kappa_allowed_by_current_inputs"] != ">=1":
            errors.append("tower kappa")
        if tower["status"] != (
            "CERTIFIED_NULL_SURVIVOR_FACE_TOWER_NONIMPLICATION"
        ):
            errors.append("tower status")

        interp = result["fixed_weight_Lq_interpolation_audit"]
        fixed_threshold = 2 * rho / (1 + rho)
        if not fixed_threshold * fixed_threshold < rho:
            errors.append("AM-GM endpoint separation")
        expected_interp_rows = [
            {
                "q": "3/2",
                "Holder_decay_exponent": "1/3",
                "effective_kappa": "rho^(1/3)",
                "below_fixed_Round50_threshold": False,
            },
            {
                "q": "2 (even if endpoint were granted)",
                "Holder_decay_exponent": "1/2",
                "effective_kappa": "sqrt(rho)",
                "below_fixed_Round50_threshold": False,
            },
        ]
        if interp["rows"] != expected_interp_rows:
            errors.append("interpolation rows")
        if interp["rows_sha256"] != cert.digest(expected_interp_rows):
            errors.append("interpolation digest")
        if interp["all_q_at_most_two_fail_fixed_threshold"] is not True:
            errors.append("interpolation conclusion")
        if interp["weaker_weight_route_is_currently_certified"] is not False:
            errors.append("weaker weight overclaim")
        if interp["status"] != (
            "CERTIFIED_FIXED_WEIGHT_LQ_INTERPOLATION_OBSTRUCTION"
        ):
            errors.append("interpolation status")

        f17 = result["physical_anisotropic_F17_candidate_audit"]
        expected_f17_rows = []
        for scale in (1, 16, 256, 4096, 65536):
            expected_f17_rows.append(
                {
                    "L": scale,
                    "domain": f"[0,1/{scale}]x[0,1]",
                    "stable_direction": "e_2",
                    "test": f"phi_L(u,s)={scale}*u",
                    "stable_curve_test_norm": "1",
                    "vector_current": "K=e_1",
                    "source_L1_vector_mass": str(Q(1, scale)),
                    "divergence_pairing": "1",
                    "pairing_to_source_mass_ratio": str(scale),
                }
            )
        counter = f17["transverse_pairing_countermodel"]
        if counter["rows"] != expected_f17_rows:
            errors.append("F17 rows")
        if counter["rows_sha256"] != cert.digest(expected_f17_rows):
            errors.append("F17 digest")
        if f17["adding_uniform_full_gradient_repairs_source_pairing"] is not True:
            errors.append("F17 gradient repair")
        if f17["adding_uniform_full_gradient_preserves_suffix_multiplier"] is not False:
            errors.append("F17 suffix obstruction")
        if f17["official_source_supplies_required_vector_current_injection"] is not False:
            errors.append("F17 literature overclaim")
        if f17["unified_physical_anisotropic_CM2_F17_space"] != "NOT_CERTIFIED":
            errors.append("F17 space promotion")
        if f17["F17_dynamic_test_operator_cost"] != "NOT_CERTIFIED":
            errors.append("F17 promotion")
        if f17["status"] != (
            "CERTIFIED_STABLE_CURVE_CANDIDATE_TRANSVERSE_CURRENT_OBSTRUCTION"
        ):
            errors.append("F17 status")

        tech = result["latest_technology_audit"]
        if tech["official_version_checked_2026_07_20"] != "2606.10155v1":
            errors.append("technology version")
        if tech[
            "direct_same_ID_face_tower_or_vector_current_F17_upgrade_found"
        ] is not False:
            errors.append("technology overclaim")

        update = result["Gate5_maturity_update"]
        if update["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if update["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if update["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")

        strict = result["strict_nonpromotion"]
        required = {
            "fixed_insertion_same_ID_owner_tail_transfer": "CERTIFIED",
            "all_insertion_time_owner_tail_sum": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "owner_ZB_kappa_below_fixed_threshold": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "trace_nullity_of_never_return_cemetery": "NOT_CERTIFIED",
            "unified_physical_anisotropic_CM2_F17_space": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if set(strict) != set(required):
            errors.append("strict key set")
        for key, value in required.items():
            if strict.get(key) != value:
                errors.append(f"strict {key}")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"result structure: {exc}")
    return errors


def verify_object(manifest: dict[str, Any], replay: bool) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }
    if set(manifest) != expected_keys:
        errors.append("manifest keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency ledger")
    for name, expected in cert.DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe dependency {name}")
        elif sha(path) != expected:
            errors.append(f"dependency hash {name}")
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result root")
        return errors
    if result.get("schema") != cert.RESULT_SCHEMA:
        errors.append("result schema")
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal replay digest")
    errors.extend(direct_errors(result))
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict projection")
    if replay:
        try:
            expected_result = cert.build_result()
        except Exception as exc:
            errors.append(f"certificate replay: {exc}")
        else:
            if result != expected_result:
                errors.append("deterministic result replay")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def fast_integrity_errors(manifest: dict[str, Any]) -> list[str]:
    """Cheap mutation predicate used after one full baseline verification.

    Result mutations are cryptographically covered by the internal digest;
    the remaining top-level projections are compared directly.  The main
    verifier still performs dependency hashing, independent arithmetic and a
    deterministic producer replay before this hostile suite is entered.
    """

    errors: list[str] = []
    if set(manifest) != {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }:
        errors.append("manifest keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependencies")
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result")
        return errors
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal digest")
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict")
    return errors


def hostile_paths() -> list[tuple[str, ...]]:
    fixed = "fixed_insertion_same_ID_owner_tail_transfer"
    tower = "null_survivor_face_tower_countermodel"
    interp = "fixed_weight_Lq_interpolation_audit"
    f17 = "physical_anisotropic_F17_candidate_audit"
    tech = "latest_technology_audit"
    strict = "strict_nonpromotion"
    paths: list[tuple[str, ...]] = [
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "depth_scope"),
        ("result", "provenance", "claim_type"),
        ("result", fixed, "source_measure"),
        ("result", fixed, "fixed_index"),
        ("result", fixed, "same_ID_restriction_formula"),
        ("result", fixed, "positivity_and_disjointness_inequality"),
        ("result", fixed, "target_Borel_set_domination_after_distinct_suffixes"),
        ("result", fixed, "operations_sha256"),
        ("result", fixed, "transferred_rank_tail"),
        ("result", fixed, "transferred_integral_2^B_strict_upper"),
        ("result", fixed, "transferred_forward_F10_L1_strict_upper"),
        ("result", fixed, "transferred_reverse_F10_L1_strict_upper"),
        ("result", fixed, "transferred_bidirectional_F10_L1_strict_upper"),
        ("result", fixed, "transfer_constant"),
        ("result", fixed, "arbitrary_finite_regular_suffix_TV_scope"),
        ("result", fixed, "uniform_in_j_bound_has_decay_in_j"),
        ("result", fixed, "sums_over_insertion_times"),
        ("result", fixed, "return_depth_face_tower_moment"),
        ("result", fixed, "status"),
        ("result", tower, "space"),
        ("result", tower, "face"),
        ("result", tower, "survivors"),
        ("result", tower, "return_layers"),
        ("result", tower, "never_return_set"),
        ("result", tower, "collision_mass"),
        ("result", tower, "trace_mass"),
        ("result", tower, "rank"),
        ("result", tower, "fixed_time_raw_tail_and_all_q_moments"),
        ("result", tower, "same_ID_owner_restriction"),
        ("result", tower, "rows_sha256"),
        ("result", tower, "owner_charge_sequence"),
        ("result", tower, "ordinary_forcing_model"),
        ("result", tower, "weighted_forcing_sum"),
        ("result", tower, "weighted_owner_charge_sum"),
        ("result", tower, "recurrence_conclusion"),
        ("result", tower, "minimal_asymptotic_kappa_allowed_by_current_inputs"),
        ("result", tower, "Round50_threshold"),
        ("result", tower, "threshold_fraction_binary_sha256"),
        ("result", tower, "logical_scope"),
        ("result", tower, "new_missing_interface"),
        ("result", tower, "status"),
        ("result", interp, "hypothetical_extra_input"),
        ("result", interp, "Holder_bound"),
        ("result", interp, "effective_recurrence_factor"),
        ("result", interp, "available_raw_moment_range"),
        ("result", interp, "fixed_threshold"),
        ("result", interp, "exact_endpoint_separation"),
        ("result", interp, "all_q_at_most_two_fail_fixed_threshold"),
        ("result", interp, "rows_sha256"),
        ("result", interp, "required_for_fixed_weight_route"),
        ("result", interp, "weaker_weight_route"),
        ("result", interp, "weaker_weight_route_is_currently_certified"),
        ("result", interp, "status"),
        ("result", f17, "literature_candidate"),
        ("result", f17, "candidate_scalar_test_norm"),
        ("result", f17, "candidate_suffix_advantage"),
        ("result", f17, "full_Eulerian_current_pairing_needed"),
        ("result", f17, "transverse_pairing_countermodel", "rows_sha256"),
        ("result", f17, "transverse_pairing_countermodel", "conclusion"),
        ("result", f17, "physical_alignment_available"),
        ("result", f17, "adding_uniform_full_gradient_repairs_source_pairing"),
        ("result", f17, "adding_uniform_full_gradient_preserves_suffix_multiplier"),
        ("result", f17, "reason_full_gradient_fails"),
        ("result", f17, "required_vector_current_space"),
        ("result", f17, "official_source_checked"),
        ("result", f17, "official_source_supplies_required_vector_current_injection"),
        ("result", f17, "unified_physical_anisotropic_CM2_F17_space"),
        ("result", f17, "F17_dynamic_test_operator_cost"),
        ("result", f17, "status"),
        ("result", tech, "official_version_checked_2026_07_20"),
        ("result", tech, "relevant_mechanism"),
        ("result", tech, "direct_same_ID_face_tower_or_vector_current_F17_upgrade_found"),
        ("result", tech, "status"),
        ("result", "Gate5_maturity_update", "new_global_field_completed"),
        ("result", "Gate5_maturity_update", "current_global_maturity"),
        ("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"),
    ]
    for key in (
        "fixed_insertion_same_ID_owner_tail_transfer",
        "all_insertion_time_owner_tail_sum",
        "same_ID_full_ZB_one_step_recurrence",
        "owner_ZB_kappa_below_fixed_threshold",
        "unconditional_aggregate_ZB_resolvent",
        "return_depth_weighted_face_integrability",
        "trace_nullity_of_never_return_cemetery",
        "unified_physical_anisotropic_CM2_F17_space",
        "F17_bulk_dynamic_test",
        "complete_all_face_F10",
        "strong_F13",
        "F14_F15_F17_F18",
        "strong_cemetery",
        "Gate5",
        "Gate5_maturity",
        "complete_18_field_operator_block_count",
        "complete_composite_gates",
        "CM2",
    ):
        paths.append(("result", strict, key))
    return paths


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    failures = 0
    total = 0
    for path in hostile_paths():
        total += 1
        mutant = copy.deepcopy(manifest)
        current: Any = mutant
        for key in path:
            current = current[key]
        if isinstance(current, bool):
            replacement: Any = not current
        elif isinstance(current, int):
            replacement = current + 1
        elif current is None:
            replacement = "CERTIFIED"
        else:
            replacement = "HOSTILE_MUTATION"
        set_path(mutant, path, replacement)
        if not fast_integrity_errors(mutant):
            failures += 1

    for key, replacement in (
        ("schema", "bad.schema"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("verdict", {}),
    ):
        total += 1
        mutant = copy.deepcopy(manifest)
        mutant[key] = replacement
        if not fast_integrity_errors(mutant):
            failures += 1

    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not fast_integrity_errors(mutant):
        failures += 1

    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        total += 1
        try:
            json.loads(
                payload,
                object_pairs_hook=cert.strict_object,
                parse_constant=cert.reject_json_constant,
            )
        except ValueError:
            pass
        else:
            failures += 1
    return total - failures, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = strict_load(args.manifest.resolve())
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    replay = args.replay or args.self_test or not args.integrity_only
    errors = verify_object(manifest, replay=replay)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    if args.self_test:
        passed, total = self_test(manifest)
        print(f"HOSTILE_SELF_TEST: {passed}/{total}")
        if passed != total:
            return 1
    elif args.integrity_only:
        print("INTEGRITY_ONLY: PASS")
    elif args.replay:
        print("REPLAY: PASS")
    else:
        print("SAFE_MANIFEST: PASS")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
