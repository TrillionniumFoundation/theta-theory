#!/usr/bin/env python3
"""Fail-closed verifier for the Round-51 Gate-5 face/Z_B/F17 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round51_face_sparse_zb_dynamic_envelope_frontier_cert as cert


HERE = Path(__file__).resolve().parent


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
        faces = result["five_face_rank_localization"]
        expected_faces = [
            {
                "physical_face_kind": "source_core_clipping_face",
                "one_step_parameter_current": "zero in fixed common source coordinates",
                "rank_weight_role": "none",
                "available_route": "zero current",
                "full_theta_one_ZB_needed": False,
            },
            {
                "physical_face_kind": "intermediate_core_avoidance_preimage_face",
                "one_step_parameter_current": "affine C24 core-edge flux",
                "rank_weight_role": "rank-zero central C24 seed",
                "available_route": "fixed ordinary-Z insertion cost before suffix",
                "full_theta_one_ZB_needed": False,
            },
            {
                "physical_face_kind": "terminal_core_preimage_face",
                "one_step_parameter_current": "affine C24 core-edge flux",
                "rank_weight_role": "rank-zero central C24 seed",
                "available_route": "fixed ordinary-Z insertion cost before suffix",
                "full_theta_one_ZB_needed": False,
            },
            {
                "physical_face_kind": "collision_singularity_or_owner_change_face",
                "one_step_parameter_current": "seven frozen boundary-kind regular seeds",
                "rank_weight_role": "fixed tangency/corner costs; five zero-speed kinds vanish",
                "available_route": "fixed ordinary-Z insertion cost before suffix",
                "full_theta_one_ZB_needed": False,
            },
            {
                "physical_face_kind": "moving_occurrence_face",
                "one_step_parameter_current": "sigma*(tau_hit-tau_miss)",
                "rank_weight_role": "raw bidirectional seed cost <103*2^B",
                "available_route": "occurrence-only Z_B or a paired-current separation theorem",
                "full_theta_one_ZB_needed": True,
            },
        ]
        if faces["rows"] != expected_faces:
            errors.append("face rows")
        if faces["rows_sha256"] != cert.digest(expected_faces):
            errors.append("face rows digest")
        if faces["five_physical_face_kinds_exhausted"] is not True:
            errors.append("face exhaustion")
        if faces["only_full_rank_face_kind"] != "moving_occurrence_face":
            errors.append("full-rank face localization")
        if faces["status"] != "CERTIFIED_FACE_LOCAL_RANK_DECOMPOSITION":
            errors.append("face status")

        seed = result["raw_occurrence_seed_theta_one_bound"]
        mass = Q(8064, 5)
        tail = Q(9158592, 6875)
        rank_l1 = (1 << 14) * mass + tail * Q(1, 1 << 13)
        forward = 68 * rank_l1
        reverse = 35 * rank_l1
        total = forward + reverse
        if rank_l1 != Q(23253221519103, 880000):
            errors.append("rank L1 independent arithmetic")
        if seed["integral_2^B_dm_occ_strict_upper"] != str(rank_l1):
            errors.append("rank L1")
        if seed["forward_F10_L1_strict_upper"] != str(forward):
            errors.append("forward L1")
        if seed["reverse_F10_L1_strict_upper"] != str(reverse):
            errors.append("reverse L1")
        if seed["bidirectional_F10_L1_strict_upper"] != str(total):
            errors.append("bidirectional L1")
        if seed["full_theta_one_raw_seed_coarea_integrability"] != "CERTIFIED":
            errors.append("seed theta-one status")
        if seed["arbitrary_Rn_owner_leaf_law_is_this_measure"] is not False:
            errors.append("seed/owner measure typing")
        if seed["return_depth_weighted_owner_coarea_integrability"] != (
            "NOT_CERTIFIED"
        ):
            errors.append("seed return nonpromotion")

        obstruction = result["owner_scalar_cancellation_nonimplication"]
        model = obstruction["countermodel"]
        model_rows = []
        for count in (1, 16, 64, 256):
            model_rows.append(
                {
                    "active_strip_count": count,
                    "ordinary_positive_mass": str(
                        Q(count, 6121 * (6121 + count))
                    ),
                    "owner_event_count_per_parent": 1,
                    "signed_scalar_mass": "0",
                    "C1_test_response_strict_lower": str(count),
                }
            )
        if model["rows"] != model_rows:
            errors.append("nonimplication rows")
        if model["rows_sha256"] != cert.digest(model_rows):
            errors.append("nonimplication digest")
        if model["base_mass"] != (
            "a_k=1/(k*(k+1)); sum_(k>=6121)a_k=1/6121"
        ):
            errors.append("countermodel finite mass")
        if model["rank_response_lower"] != (
            "nu_k(phi)=a_k*2^Bbar(k)/2 >=(k+1)/k>1"
        ):
            errors.append("countermodel response")
        if obstruction["does_not_claim_actual_billiard_current_diverges"] is not True:
            errors.append("countermodel scope")
        if obstruction["global_Jx_reflection_supplies_same_target_small_separation"] is not False:
            errors.append("Jx separation scope")
        if obstruction["same_ID_full_ZB_one_step_recurrence"] != "NOT_CERTIFIED":
            errors.append("ZB recurrence nonpromotion")
        if obstruction["status"] != (
            "CERTIFIED_OWNER_AND_SCALAR_CANCELLATION_NONIMPLICATION"
        ):
            errors.append("obstruction status")

        aggregate = result["conditional_aggregate_ZB_update"]
        rho = Q(111718729, 111718750) ** 9148
        threshold = 2 * rho / (1 + rho)
        if not Q(99914, 100000) < threshold < Q(99915, 100000):
            errors.append("aggregate independent bracket")
        if aggregate["threshold_fraction_binary_sha256"] != cert.fraction_digest(
            threshold
        ):
            errors.append("aggregate threshold digest")
        if aggregate["finite_raw_seed_theta_one_injection_available"] is not True:
            errors.append("aggregate seed forcing")
        if aggregate["finite_raw_seed_injection_is_recurrence_contraction"] is not False:
            errors.append("aggregate forcing typing")
        if aggregate["owner_ZB_recurrence_coefficient_kappa_B"] is not None:
            errors.append("aggregate kappa overclaim")
        if aggregate["unconditional_aggregate_ZB_resolvent"] != "NOT_CERTIFIED":
            errors.append("aggregate nonpromotion")
        if aggregate["return_depth_face_tower_moment"] != "NOT_CERTIFIED":
            errors.append("face tower nonpromotion")

        dynamic = result["common_dynamic_suffix_envelope"]
        thresholds = dynamic["thresholds"]
        if thresholds["preserve_source_quarter"] != str(Q(7961063, 7800000)):
            errors.append("dynamic quarter threshold")
        if thresholds["preserve_subunit"] != str(Q(43295063, 7800000)):
            errors.append("dynamic unit threshold")
        if thresholds["quarter_multiplier_slack"] != str(Q(161063, 7800000)):
            errors.append("dynamic slack")
        if thresholds["unit_multiplier_passes_both"] is not True:
            errors.append("dynamic threshold pass")
        if dynamic["source_current_ratio"] != str(Q(11616937, 47112000)):
            errors.append("dynamic source ratio")
        if dynamic["common_envelope_suffix_multiplier"] != "C_dyn=1":
            errors.append("dynamic envelope multiplier")
        if dynamic["branch_uniform_embedding_on_T_env"] != "CERTIFIED":
            errors.append("dynamic envelope status")
        dynamic_rows = []
        for exponent in (0, 4, 8, 12, 16):
            scale = 1 << exponent
            dynamic_rows.append(
                {
                    "L": scale,
                    "branch": f"diag({scale},1/{scale})",
                    "determinant": "1",
                    "source_domain": f"[0,1/{scale}]x[0,1]",
                    "target_domain": f"[0,1]x[0,1/{scale}]",
                    "physical_test": "phi(y)=y_1/2",
                    "physical_C1_sum_norm": "<=1 on the unit chart",
                    "envelope_pullback_gradient_lower": str(Q(scale, 2)),
                }
            )
        compat = dynamic["physical_compatibility_obstruction"]
        if compat["rows"] != dynamic_rows:
            errors.append("dynamic rows")
        if compat["rows_sha256"] != cert.digest(dynamic_rows):
            errors.append("dynamic rows digest")
        if compat[
            "bounded_inclusion_C1_physical_into_T_env_from_current_inputs"
        ] is not False:
            errors.append("dynamic physical inclusion")
        if dynamic[
            "required_physical_CM2_test_algebra_contained_with_finite_constant"
        ] != "NOT_CERTIFIED":
            errors.append("dynamic CM2 nonpromotion")
        if dynamic["F17_dynamic_test_operator_cost"] != "NOT_CERTIFIED":
            errors.append("dynamic F17 nonpromotion")
        if dynamic["complete_strong_F13_operator_intertwiner"] != "NOT_CERTIFIED":
            errors.append("dynamic F13 nonpromotion")
        if dynamic["status"] != "CERTIFIED_COMMON_ENVELOPE_ONLY_NOT_PHYSICAL_F17":
            errors.append("dynamic scope status")

        tech = result["latest_technology_audit"]
        if tech["official_versions_checked_2026_07_20"] != [
            "2606.10155v1", "2604.19671v2", "2604.25881v1"
        ]:
            errors.append("technology versions")
        if tech["rows_sha256"] != cert.digest(tech["rows"]):
            errors.append("technology digest")
        if tech["direct_gate5_upgrade_found"] is not False:
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
            "five_face_full_rank_localization": "CERTIFIED_MOVING_OCCURRENCE_ONLY",
            "raw_occurrence_seed_theta_one_L1": "CERTIFIED",
            "arbitrary_Rn_owner_theta_one_recurrence": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "common_algebraic_suffix_envelope_Cdyn_one": "CERTIFIED",
            "branch_uniform_physical_dynamic_test_embedding": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
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


def hostile_paths() -> list[tuple[str, ...]]:
    faces = "five_face_rank_localization"
    seed = "raw_occurrence_seed_theta_one_bound"
    obs = "owner_scalar_cancellation_nonimplication"
    agg = "conditional_aggregate_ZB_update"
    dyn = "common_dynamic_suffix_envelope"
    tech = "latest_technology_audit"
    strict = "strict_nonpromotion"
    return [
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "depth_scope"),
        ("result", "provenance", "claim_type"),
        ("result", faces, "rows_sha256"),
        ("result", faces, "five_physical_face_kinds_exhausted"),
        ("result", faces, "only_full_rank_face_kind"),
        ("result", faces, "artificial_chart_or_homogeneity_faces"),
        ("result", faces, "scope"),
        ("result", faces, "status"),
        ("result", seed, "measure"),
        ("result", seed, "rank_scope"),
        ("result", seed, "integer_layer_cake"),
        ("result", seed, "integral_2^B_dm_occ_strict_upper"),
        ("result", seed, "forward_F10_L1_strict_upper"),
        ("result", seed, "reverse_F10_L1_strict_upper"),
        ("result", seed, "bidirectional_F10_L1_strict_upper"),
        ("result", seed, "full_theta_one_raw_seed_coarea_integrability"),
        ("result", seed, "arbitrary_Rn_owner_leaf_law_is_this_measure"),
        ("result", seed, "return_depth_weighted_owner_coarea_integrability"),
        ("result", seed, "logical_scope"),
        ("result", seed, "status"),
        ("result", obs, "countermodel", "parent_index"),
        ("result", obs, "countermodel", "base_mass"),
        ("result", obs, "countermodel", "rank"),
        ("result", obs, "countermodel", "owned_pair_current"),
        ("result", obs, "countermodel", "constant_test"),
        ("result", obs, "countermodel", "unit_C1_test"),
        ("result", obs, "countermodel", "rank_response_lower"),
        ("result", obs, "countermodel", "full_C1_partial_response"),
        ("result", obs, "countermodel", "rows_sha256"),
        ("result", obs, "logical_conclusion"),
        ("result", obs, "does_not_claim_actual_billiard_current_diverges"),
        ("result", obs, "missing_pair_interface"),
        ("result", obs, "sufficient_model_separation"),
        ("result", obs, "global_Jx_reflection_supplies_same_target_small_separation"),
        ("result", obs, "raw_seed_tail_transfer_needed"),
        ("result", obs, "same_ID_full_ZB_one_step_recurrence"),
        ("result", obs, "status"),
        ("result", agg, "sharp_requirement"),
        ("result", agg, "rho"),
        ("result", agg, "threshold_strict_bracket"),
        ("result", agg, "threshold_fraction_binary_sha256"),
        ("result", agg, "finite_raw_seed_theta_one_injection_available"),
        ("result", agg, "finite_raw_seed_injection_is_recurrence_contraction"),
        ("result", agg, "owner_ZB_recurrence_coefficient_kappa_B"),
        ("result", agg, "unconditional_aggregate_ZB_resolvent"),
        ("result", agg, "return_depth_face_tower_moment"),
        ("result", agg, "status"),
        ("result", dyn, "regular_suffix_registry"),
        ("result", dyn, "finite_norm_pre_space"),
        ("result", dyn, "common_test_space"),
        ("result", dyn, "branch_uniform_embedding"),
        ("result", dyn, "dual_pushforward"),
        ("result", dyn, "common_envelope_suffix_multiplier"),
        ("result", dyn, "branch_uniform_embedding_on_T_env"),
        ("result", dyn, "thresholds", "preserve_source_quarter"),
        ("result", dyn, "thresholds", "preserve_subunit"),
        ("result", dyn, "thresholds", "unit_multiplier_passes_both"),
        ("result", dyn, "thresholds", "quarter_multiplier_slack"),
        ("result", dyn, "source_current_ratio"),
        ("result", dyn, "physical_compatibility_obstruction", "claim"),
        ("result", dyn, "physical_compatibility_obstruction", "rows_sha256"),
        ("result", dyn, "physical_compatibility_obstruction", "bounded_inclusion_C1_physical_into_T_env_from_current_inputs"),
        ("result", dyn, "billiard_specific_possible_replacement"),
        ("result", dyn, "required_physical_CM2_test_algebra_contained_with_finite_constant"),
        ("result", dyn, "F17_dynamic_test_operator_cost"),
        ("result", dyn, "complete_strong_F13_operator_intertwiner"),
        ("result", dyn, "logical_scope"),
        ("result", dyn, "status"),
        ("result", tech, "rows_sha256"),
        ("result", tech, "official_versions_checked_2026_07_20"),
        ("result", tech, "direct_gate5_upgrade_found"),
        ("result", tech, "status"),
        ("result", "Gate5_maturity_update", "new_global_field_completed"),
        ("result", "Gate5_maturity_update", "current_global_maturity"),
        ("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"),
        ("result", strict, "five_face_full_rank_localization"),
        ("result", strict, "raw_occurrence_seed_theta_one_L1"),
        ("result", strict, "arbitrary_Rn_owner_theta_one_recurrence"),
        ("result", strict, "same_ID_full_ZB_one_step_recurrence"),
        ("result", strict, "unconditional_aggregate_ZB_resolvent"),
        ("result", strict, "return_depth_weighted_face_integrability"),
        ("result", strict, "common_algebraic_suffix_envelope_Cdyn_one"),
        ("result", strict, "branch_uniform_physical_dynamic_test_embedding"),
        ("result", strict, "complete_all_face_F10"),
        ("result", strict, "F17_bulk_dynamic_test"),
        ("result", strict, "strong_F13"),
        ("result", strict, "strong_cemetery"),
        ("result", strict, "Gate5_maturity"),
        ("result", strict, "complete_18_field_operator_block_count"),
        ("result", strict, "complete_composite_gates"),
        ("result", strict, "CM2"),
    ]


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
        if not verify_object(mutant, replay=True):
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
        if not verify_object(mutant, replay=True):
            failures += 1

    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not verify_object(mutant, replay=True):
        failures += 1

    total += 1
    try:
        json.loads(
            '{"x":1,"x":2}',
            object_pairs_hook=cert.strict_object,
            parse_constant=cert.reject_json_constant,
        )
    except ValueError:
        pass
    else:
        failures += 1

    total += 1
    try:
        json.loads(
            '{"x":NaN}',
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
