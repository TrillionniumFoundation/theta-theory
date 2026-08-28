#!/usr/bin/env python3
"""Fail-closed verifier for Round-47 refined crossing/post-cut recovery."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round47_postcut_dyadic_recovery_cert as cert


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    crossing = result.get("refined_white_diagonal_crossing_minorisation", {})
    length = Q(66, 7)
    arc_fraction = Q(1, 25) / length
    r_ext = Q(400000000, 399794003)
    pair_hit = arc_fraction / r_ext
    threshold = Q(21, 111718750) / pair_hit
    if arc_fraction != Q(7, 1650):
        errors.append("adapted length fraction")
    if pair_hit != Q(2798558021, 660000000000):
        errors.append("pair hit arithmetic")
    if threshold != Q(230400, 5197322039):
        errors.append("beta threshold arithmetic")
    if crossing.get("one_crossing_bundle_hit_fraction_strict_lower") != str(pair_hit):
        errors.append("pair hit field")
    if crossing.get("sufficient_actual_crossing_family_weight") != f"beta_Wdiag>={threshold}":
        errors.append("beta threshold field")
    if not (Q(1, 22557) >= threshold and Q(1, 22558) < threshold):
        errors.append("reciprocal threshold")
    if Q(1, 22557) * pair_hit - Q(21, 111718750) != Q(
        1324673, 193539060000000000
    ):
        errors.append("safe beta excess")

    z1 = Q(2000, 1999) * 49 * Q(900337, 901685) + 2
    cp = Q(4 * 10**90 * 360493663, 358863)
    envelope = z1 * cp
    one_step = result.get("one_step_postcut_Z_envelope", {})
    if z1 != Q(18367592526, 360493663):
        errors.append("Z1 arithmetic")
    if envelope != Q(24490123368 * 10**90, 119621):
        errors.append("P arithmetic")
    if not 2**316 < envelope < 2**317:
        errors.append("P power bracket")
    if one_step.get("P_exact") != str(envelope):
        errors.append("P field")

    rows = []
    for k in (0, 1, 14, 64, 128):
        exponent = 318 + k
        rows.append(
            {
                "shell_k": k,
                "survivor_fraction": f"2^(-{k + 1})<x<=2^(-{k})",
                "normalized_Z_strict_upper": f"2^({exponent})",
                "closed_recovery_iterations": 1005 * exponent,
            }
        )
    dyadic = result.get("per_orientation_dyadic_postcut_return", {})
    if dyadic.get("sample_rows") != rows:
        errors.append("sample rows")
    if dyadic.get("sample_rows_sha256") != cert.digest(rows):
        errors.append("sample row digest")
    a = Q(360134800, 360493663)
    if a**1005 > Q(1, 2):
        errors.append("half block")
    if Q(1, 6030) * 1005 != Q(1, 6):
        errors.append("moment slope")
    if Q(1, 6030) * 319590 != 53:
        errors.append("moment base")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink():
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")

        result = source.get("result", {})
        errors.extend(independent_arithmetic(result))
        registry = result.get("corrected_adapted_source_cell_registry", {})
        if registry.get("status") != "CERTIFIED_CORRECTED_ADAPTED_SOURCE_CELL_SCHEMA":
            errors.append("adapted source registry")
        if registry.get("Round31_Euclidean_cell_bound_not_reused_as_adapted") is not True:
            errors.append("Round31 metric reuse")
        crossing = result.get("refined_white_diagonal_crossing_minorisation", {})
        if crossing.get("status") != "CERTIFIED_REFINED_CONDITIONAL_MINORISATION":
            errors.append("crossing status")
        if crossing.get("numeric_H_cover_or_actual_beta_Wdiag_inferred") is not False:
            errors.append("crossing overclaim")
        if "former Euclidean arc fraction cannot be multiplied" not in crossing.get(
            "round45_46_metric_correction", ""
        ):
            errors.append("metric correction")

        dyadic = result.get("per_orientation_dyadic_postcut_return", {})
        if dyadic.get("same_proper_class_return") != (
            "CERTIFIED_PER_ORIENTATION_DYADIC_FAMILYWISE"
        ):
            errors.append("per-orientation return")
        if dyadic.get("single_short_leaf_assumed_proper") is not False:
            errors.append("leaf properness overclaim")
        if dyadic.get("same_ID_forward_reverse_survivor_or_common_k_asserted") is not False:
            errors.append("same-ID overclaim")
        if dyadic.get("zero_survivor_policy") != (
            "mass(H)=0 is absorbed and is never normalized"
        ):
            errors.append("zero survivor")

        moment = result.get("per_orientation_postcut_shell_moment", {})
        if moment.get("status") != (
            "CERTIFIED_CONDITIONAL_FINITE_OR_COUNTABLE_FAMILY_SHELL_LEMMA"
        ):
            errors.append("per-orientation moment")
        if moment.get("standard_Borel_mass_kernel_or_disintegration_claimed") is not False:
            errors.append("Borel shell overclaim")
        if moment.get("same_ID_joint_moment_claimed") is not False:
            errors.append("joint moment overclaim")

        frontier = result.get("corrected_frontier", {})
        if frontier.get("numeric_H_cover") is not None:
            errors.append("H_cover overclaim")
        if frontier.get("numeric_actual_crossing_weight_beta_Wdiag") is not None:
            errors.append("actual beta overclaim")
        if frontier.get("same_ID_two_orientation_survivor_registry") != "NOT_CERTIFIED":
            errors.append("joint survivor overclaim")
        if frontier.get("standard_Borel_parent_survivor_mass_kernel") != "NOT_CERTIFIED":
            errors.append("Borel mass kernel overclaim")
        if frontier.get("strong_cemetery_current_envelope") != "NOT_CERTIFIED":
            errors.append("cemetery overclaim")

        strict = result.get("strict_nonpromotion", {})
        expected = {
            "refined_conditional_one_crossing_hit_and_beta_threshold": "CERTIFIED",
            "adapted_source_cell_metric_correction": "CERTIFIED",
            "one_orientation_post_C24_cut_same_proper_class_return": "CERTIFIED_DYADIC_FAMILYWISE",
            "per_orientation_postcut_exponential_shell_moment": "CERTIFIED_CONDITIONAL_FINITE_OR_COUNTABLE",
            "same_ID_two_orientation_postcut_return": "NOT_CERTIFIED",
            "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if strict != expected:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[str, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "parameter_scope"), "s=0"),
        (("result", "corrected_adapted_source_cell_registry", "adapted_cell_length_upper"), "2.5e-90"),
        (("result", "corrected_adapted_source_cell_registry", "same_parent_union"), False),
        (("result", "corrected_adapted_source_cell_registry", "Round31_Euclidean_cell_bound_not_reused_as_adapted"), False),
        (("result", "corrected_adapted_source_cell_registry", "status"), "NOT_CERTIFIED"),
        (("result", "refined_white_diagonal_crossing_minorisation", "selected_component"), "G"),
        (("result", "refined_white_diagonal_crossing_minorisation", "extended_parent_adapted_length_strict_upper"), "6"),
        (("result", "refined_white_diagonal_crossing_minorisation", "one_crossing_bundle_hit_fraction_strict_lower"), "0"),
        (("result", "refined_white_diagonal_crossing_minorisation", "sufficient_actual_crossing_family_weight"), "beta>=0"),
        (("result", "refined_white_diagonal_crossing_minorisation", "safe_reciprocal_beta"), "1/22558"),
        (("result", "refined_white_diagonal_crossing_minorisation", "first_failing_reciprocal_beta"), "1/22557"),
        (("result", "refined_white_diagonal_crossing_minorisation", "numeric_H_cover_or_actual_beta_Wdiag_inferred"), True),
        (("result", "refined_white_diagonal_crossing_minorisation", "round45_46_metric_correction"), "reuse Euclidean fraction"),
        (("result", "one_step_postcut_Z_envelope", "Z1"), "1"),
        (("result", "one_step_postcut_Z_envelope", "P_exact"), "1"),
        (("result", "one_step_postcut_Z_envelope", "P_power_bracket"), "false"),
        (("result", "one_step_postcut_Z_envelope", "large_9148_step_Z0_not_used"), False),
        (("result", "per_orientation_dyadic_postcut_return", "zero_survivor_policy"), "normalize zero"),
        (("result", "per_orientation_dyadic_postcut_return", "normalized_postcut_bound"), "uniform"),
        (("result", "per_orientation_dyadic_postcut_return", "per_orientation_postcut_clock"), "1005"),
        (("result", "per_orientation_dyadic_postcut_return", "same_proper_class_return"), "NOT_CERTIFIED"),
        (("result", "per_orientation_dyadic_postcut_return", "single_short_leaf_assumed_proper"), True),
        (("result", "per_orientation_dyadic_postcut_return", "same_ID_forward_reverse_survivor_or_common_k_asserted"), True),
        (("result", "per_orientation_dyadic_postcut_return", "sample_rows"), []),
        (("result", "per_orientation_dyadic_postcut_return", "sample_rows_sha256"), "0" * 64),
        (("result", "per_orientation_postcut_shell_moment", "clock_weight_eta"), "1"),
        (("result", "per_orientation_postcut_shell_moment", "geometric_ratio_upper"), "1"),
        (("result", "per_orientation_postcut_shell_moment", "same_ID_joint_moment_claimed"), True),
        (("result", "per_orientation_postcut_shell_moment", "standard_Borel_mass_kernel_or_disintegration_claimed"), True),
        (("result", "per_orientation_postcut_shell_moment", "status"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_crossing_weight_beta_Wdiag"), "1/22557"),
        (("result", "corrected_frontier", "same_ID_two_orientation_survivor_registry"), "CERTIFIED"),
        (("result", "corrected_frontier", "standard_Borel_parent_survivor_mass_kernel"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery_current_envelope"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "same_ID_two_orientation_postcut_return"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_cover_and_actual_beta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "numeric_collision_time_q"), "CERTIFIED"),
    ]
    mutations: list[tuple[str, str]] = []
    for index, (keys, replacement) in enumerate(changes):
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append((f"mutation-{index}.json", json.dumps(mutation)))
    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append((f"mutation-{len(mutations)}.json", json.dumps(mutation)))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    duplicate = duplicate[:-1] + ',"schema":"duplicate"}'
    mutations.append((f"mutation-{len(mutations)}.json", duplicate))

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for name, body in mutations:
            target = Path(directory) / name
            target.write_text(body, encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
