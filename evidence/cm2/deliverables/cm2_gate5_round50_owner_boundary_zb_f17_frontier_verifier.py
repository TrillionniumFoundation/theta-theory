#!/usr/bin/env python3
"""Fail-closed verifier for the Round-50 owner-Z_B/F17 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round50_owner_boundary_zb_f17_frontier_cert as cert


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        owner = result["global_owner_aware_boundary_ZB_kernel"]
        expected_rows = []
        for kind in (
            "source_core_clipping_face",
            "intermediate_core_avoidance_preimage_face",
            "terminal_core_preimage_face",
            "collision_singularity_or_owner_change_face",
            "moving_occurrence_face",
        ):
            for side in ("minus", "plus"):
                expected_rows.append(
                    {
                        "physical_face_kind": kind,
                        "side_label": side,
                        "connected_rank": 0,
                        "regular_root_multiplicity_on_one_parent_W": "0_or_1",
                    }
                )
        if owner["side_rows"] != expected_rows:
            errors.append("owner side rows")
        if owner["side_rows_sha256"] != cert.digest(expected_rows):
            errors.append("owner side digest")
        if owner["index_space_is_standard_Borel"] is not True:
            errors.append("owner index Borel")
        if owner["owner_sets_pairwise_disjoint"] is not True:
            errors.append("owner disjointness")
        if owner["different_physical_events_are_never_deduplicated"] is not True:
            errors.append("owner physical separation")
        if owner["corner_or_simultaneous_event_policy"] != (
            "cemetery, before owner minimization"
        ):
            errors.append("owner cemetery")
        if owner["finite_after_sum_over_all_depths"] != "NOT_CERTIFIED":
            errors.append("owner finiteness nonpromotion")
        if owner["status"] != (
            "CERTIFIED_GLOBAL_STANDARD_BOREL_OWNER_ZB_KERNEL_SCHEMA"
        ):
            errors.append("owner status")

        hom = result["full_ZB_homogeneity_majorant_frontier"]
        central = hom["central_child"]
        k0 = 6121
        cp_inv = 2 * k0 * k0
        rank = cert.ceil_log2_integer(cp_inv)
        coefficient = Q(2000, 1999) * Q(144000, 180337) * (1 << rank)
        if cp_inv != 74933282 or rank != 27:
            errors.append("central independent arithmetic")
        if central["cp_inverse_strict_upper"] != cp_inv:
            errors.append("central cp")
        if central["incidence_rank_upper"] != rank:
            errors.append("central rank")
        if central["full_2^B_density_weighted_inverse_majorant"] != str(
            coefficient
        ):
            errors.append("central coefficient")
        shell_rows = []
        for k in (6121, 8192, 16384, 32768):
            bbar = cert.ceil_log2_integer(2 * (k + 1) * (k + 1))
            term = Q(2 * 153 * 4 * (1 << bbar), k * k)
            shell_rows.append(
                {
                    "k": k,
                    "Bbar_k": bbar,
                    "full_weight_available_majorant_term": str(term),
                }
            )
        if hom["representative_shell_rows"] != shell_rows:
            errors.append("shell rows")
        if hom["representative_shell_rows_sha256"] != cert.digest(shell_rows):
            errors.append("shell digest")
        divergence = [
            {
                "number_of_high_strips": n,
                "partial_majorant_strict_lower": str(2448 * n),
            }
            for n in (1, 16, 64)
        ]
        if hom["divergence_rows"] != divergence:
            errors.append("divergence rows")
        if hom["divergence_rows_sha256"] != cert.digest(divergence):
            errors.append("divergence digest")
        if hom["full_theta_one_available_majorant"] != "INFINITE":
            errors.append("theta one frontier")
        if hom["soft_exponent_exact_threshold"] != (
            "M_theta<infinity iff 0<=theta<1/2"
        ):
            errors.append("theta threshold")
        if hom["same_ID_full_ZB_one_step_recurrence"] != "NOT_CERTIFIED":
            errors.append("ZB recurrence nonpromotion")

        aggregate = result["conditional_aggregate_ZB_resolvent"]
        rho = Q(111718729, 111718750) ** 9148
        w = (1 + 1 / rho) / 2
        threshold = 1 / w
        if not Q(99914, 100000) < threshold < Q(99915, 100000):
            errors.append("resolvent bracket independent")
        if aggregate["threshold_strict_bracket"] != (
            "99914/100000 < 2rho/(1+rho) < 99915/100000"
        ):
            errors.append("resolvent bracket")
        if aggregate["threshold_fraction_binary_sha256"] != cert.fraction_digest(
            threshold
        ):
            errors.append("resolvent threshold digest")
        if aggregate["owner_ZB_recurrence_coefficient_available"] is not False:
            errors.append("resolvent coefficient scope")
        if aggregate["numeric_collision_time_eta"] is not None:
            errors.append("numeric eta overclaim")
        if aggregate["unconditional_aggregate_ZB_resolvent"] != "NOT_CERTIFIED":
            errors.append("aggregate nonpromotion")
        if aggregate["return_depth_face_tower_moment"] != "NOT_CERTIFIED":
            errors.append("face tower nonpromotion")

        f17 = result["dynamic_anisotropic_F17_frontier"]
        source = Q(25, 151) + Q(3816937, 47112000)
        if source != Q(11616937, 47112000) or not source < Q(1, 4):
            errors.append("source independent arithmetic")
        if f17["source_bulk_plus_trace_ratio"] != str(source):
            errors.append("source ratio")
        thresholds = f17["required_physical_multiplier_thresholds"]
        if thresholds["preserve_less_than_one_quarter"] != str(
            Q(7961063, 7800000)
        ):
            errors.append("quarter threshold")
        if thresholds["preserve_less_than_one"] != str(
            Q(43295063, 7800000)
        ):
            errors.append("unit threshold")
        matrix_rows = []
        for exponent in (0, 4, 8, 12, 16):
            scale = 1 << exponent
            matrix_rows.append(
                {
                    "L": scale,
                    "matrix": f"diag({scale},1/{scale})",
                    "determinant": "1",
                    "Piola_normal_flux_multiplier": "1",
                    "C1_pullback_multiplier_for_phi_y1": scale,
                }
            )
        counter = f17["area_preserving_embedding_countermodel"]
        if counter["rows"] != matrix_rows:
            errors.append("dynamic rows")
        if counter["rows_sha256"] != cert.digest(matrix_rows):
            errors.append("dynamic rows digest")
        if f17["branch_adapted_suffix_multiplier"] != "C_dyn=1":
            errors.append("dynamic isometry multiplier")
        if f17["branch_dependent_dynamic_isometry"] != "CERTIFIED":
            errors.append("dynamic isometry status")
        if f17["branch_uniform_physical_dynamic_test_embedding"] != (
            "NOT_CERTIFIED"
        ):
            errors.append("dynamic embedding nonpromotion")
        if f17["F17_dynamic_test_operator_cost"] != "NOT_CERTIFIED":
            errors.append("F17 nonpromotion")

        update = result["Gate5_maturity_update"]
        if update["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if update["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if update["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")

        strict = result["strict_nonpromotion"]
        required = {
            "global_owner_aware_boundary_ZB_kernel_schema": "CERTIFIED",
            "global_owner_ZB_finiteness": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "branch_dependent_dynamic_isometry": "CERTIFIED",
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
    owner = "global_owner_aware_boundary_ZB_kernel"
    hom = "full_ZB_homogeneity_majorant_frontier"
    aggregate = "conditional_aggregate_ZB_resolvent"
    f17 = "dynamic_anisotropic_F17_frontier"
    strict = "strict_nonpromotion"
    return [
        ("result", owner, "parameter_scope"),
        ("result", owner, "global_index_space"),
        ("result", owner, "index_space_is_standard_Borel"),
        ("result", owner, "candidate_representation_token"),
        ("result", owner, "physical_event_signature"),
        ("result", owner, "active_regular_root_section"),
        ("result", owner, "owner_rule"),
        ("result", owner, "owner_sets_pairwise_disjoint"),
        ("result", owner, "owner_sets_cover_all_regular_active_representations"),
        ("result", owner, "different_physical_events_are_never_deduplicated"),
        ("result", owner, "corner_or_simultaneous_event_policy"),
        ("result", owner, "owner_marked_trace_kernel"),
        ("result", owner, "owner_boundary_ZB_functional"),
        ("result", owner, "extended_valued_functional_is_Borel"),
        ("result", owner, "finite_after_sum_over_all_depths"),
        ("result", owner, "global_owner_deduplication_requires_finite_enumeration"),
        ("result", owner, "status"),
        ("result", hom, "certified_unweighted_high_strip_input"),
        ("result", hom, "homogeneity_rank_contract"),
        ("result", hom, "central_child", "incidence_rank_upper"),
        ("result", hom, "central_child", "full_2^B_density_weighted_inverse_majorant"),
        ("result", hom, "central_child", "already_exceeds_one"),
        ("result", hom, "high_strip_available_theta_majorant"),
        ("result", hom, "full_theta_one_term_lower"),
        ("result", hom, "full_theta_one_available_majorant"),
        ("result", hom, "soft_exponent_exact_threshold"),
        ("result", hom, "logical_scope"),
        ("result", hom, "required_replacement"),
        ("result", hom, "same_ID_full_ZB_one_step_recurrence"),
        ("result", hom, "status"),
        ("result", aggregate, "block_mass_rate"),
        ("result", aggregate, "Round42_weight"),
        ("result", aggregate, "hypothetical_owner_ZB_recurrence"),
        ("result", aggregate, "exact_weighted_resolvent"),
        ("result", aggregate, "sharp_contraction_requirement"),
        ("result", aggregate, "threshold_strict_bracket"),
        ("result", aggregate, "threshold_fraction_binary_sha256"),
        ("result", aggregate, "owner_ZB_recurrence_coefficient_available"),
        ("result", aggregate, "current_positive_majorant_coefficient"),
        ("result", aggregate, "conditional_block_index_face_tower_moment"),
        ("result", aggregate, "numeric_collision_time_eta"),
        ("result", aggregate, "unconditional_aggregate_ZB_resolvent"),
        ("result", aggregate, "return_depth_face_tower_moment"),
        ("result", aggregate, "status"),
        ("result", f17, "branch_adapted_test_norm"),
        ("result", f17, "exact_dual_isometry"),
        ("result", f17, "branch_adapted_suffix_multiplier"),
        ("result", f17, "branch_adapted_multiplier_below_quarter_threshold"),
        ("result", f17, "source_bulk_plus_trace_ratio"),
        ("result", f17, "why_this_is_not_F17"),
        ("result", f17, "common_branch_norm_candidate"),
        ("result", f17, "logical_conclusion"),
        ("result", f17, "first_missing_interface"),
        ("result", f17, "branch_dependent_dynamic_isometry"),
        ("result", f17, "branch_uniform_physical_dynamic_test_embedding"),
        ("result", f17, "F17_dynamic_test_operator_cost"),
        ("result", f17, "status"),
        ("result", "Gate5_maturity_update", "new_global_field_completed"),
        ("result", "Gate5_maturity_update", "current_global_maturity"),
        ("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"),
        ("result", strict, "global_owner_aware_boundary_ZB_kernel_schema"),
        ("result", strict, "global_owner_ZB_finiteness"),
        ("result", strict, "same_ID_full_ZB_one_step_recurrence"),
        ("result", strict, "unconditional_aggregate_ZB_resolvent"),
        ("result", strict, "return_depth_weighted_face_integrability"),
        ("result", strict, "branch_dependent_dynamic_isometry"),
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
        json.loads('{"x":1,"x":2}', object_pairs_hook=cert.strict_object)
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
