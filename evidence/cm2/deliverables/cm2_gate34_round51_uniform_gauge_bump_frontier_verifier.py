#!/usr/bin/env python3
"""Fail-closed verifier for the Round-51 uniform-gauge/bump frontier."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round51_uniform_gauge_bump_frontier_cert as cert


EXPECTED_MANIFEST_KEYS = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    hit = Q(21, 111718750)
    bump = Q(21, 55859375)
    safe_mass = Q(1999, 32000)
    direct = Q(2688, 893303125)
    if bump != 2 * hit:
        errors.append("bump/hit arithmetic")
    if safe_mass * direct != hit:
        errors.append("Round49 threshold product")
    if not (Q(1, 332330) > direct > Q(1, 332331)):
        errors.append("direct reciprocal bracket")

    t0, t1 = Q(11, 1000), Q(19, 1000)
    p0, p1 = -Q(3, 2000), Q(3, 2000)
    if not (Q(1, 100) < t0 < t1 < Q(1, 50)):
        errors.append("target t containment")
    if not (-Q(1, 500) < p0 < p1 < Q(1, 500)):
        errors.append("target p containment")
    raw = Q(9, 25) * (t1 - t0) * (p1 - p0)
    norm_upper = 4 * Q(22, 7) * (Q(9, 25) + Q(4, 25))
    normalized = raw / norm_upper
    if raw != Q(27, 3125000):
        errors.append("target raw mass")
    if norm_upper != Q(1144, 175):
        errors.append("target normalization")
    if normalized != Q(189, 143000000) or normalized != Q(225, 32) * hit:
        errors.append("target normalized mass")

    target = result.get("explicit_uniform_open_C24_target", {})
    if target.get("open_box_O_star") != {
        "t": ["11/1000", "19/1000"],
        "p": ["-3/2000", "3/2000"],
    }:
        errors.append("target coordinates")
    if target.get("normalized_collision_mass_strict_lower") != str(normalized):
        errors.append("target mass field")

    gauge_rows = [
        {
            "component": "G",
            "physical_motion": "fixed",
            "label_map": "A_s(G,r,phi)=(G,r,phi)",
            "coordinate_derivative": "I_2",
            "least_singular_value": "1",
        },
        {
            "component": "W",
            "physical_motion": "ambient translation by (s,0)",
            "label_map": "A_s(W,r,phi)=(W_s,r,phi) in intrinsic boundary-arclength/outgoing-angle labels",
            "coordinate_derivative": "I_2",
            "least_singular_value": "1",
        },
    ]
    gauge = result.get("instance_specific_fixed_gauge", {})
    if gauge.get("rows") != gauge_rows:
        errors.append("gauge rows")
    if gauge.get("rows_sha256") != cert.digest(gauge_rows):
        errors.append("gauge digest")

    missing_ids = [
        "R_Cantor",
        "K_rect",
        "delta_density",
        "C_mix_theta_mix",
        "N_mix",
        "r_transverse",
        "J_branch",
        "omega_parameter_dynamic",
    ]
    frontier = result.get("cover_effectivity_frontier", {})
    missing = frontier.get("original_cover_route_missing_numeric_rows", [])
    if [row.get("id") for row in missing] != missing_ids:
        errors.append("missing row ids")
    if any(row.get("value", "bad") is not None for row in missing):
        errors.append("missing row overclaim")
    if frontier.get("missing_rows_sha256") != cert.digest(missing):
        errors.append("missing row digest")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if (
            not path.is_file()
            or path.is_symlink()
            or path.resolve().parent != cert.HERE
        ):
            return ["unsafe manifest"]
        source = read(path)
        if set(source) != EXPECTED_MANIFEST_KEYS:
            errors.append("manifest keys")
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
        if isinstance(result, dict):
            payload = dict(result)
            stored = payload.pop("internal_replay_digest", None)
            if stored != cert.digest(payload):
                errors.append("internal replay digest")
        else:
            errors.append("result root")
            result = {}
        errors.extend(independent_arithmetic(result))

        audit = result.get("literature_quantifier_audit", {})
        if audit.get("rows") != cert.literature_rows():
            errors.append("literature rows")
        if audit.get("rows_sha256") != cert.digest(cert.literature_rows()):
            errors.append("literature digest")
        if audit.get("official_sources_publish_numeric_cover_or_mixing_constants") is not False:
            errors.append("literature numeric overclaim")

        gauge = result.get("instance_specific_fixed_gauge", {})
        if gauge.get("status") != "CERTIFIED_INSTANCE_SPECIFIC_UNIFORM_ISOMETRIC_GAUGE":
            errors.append("gauge status")
        if gauge.get("uniform_numeric_m_s") != "1":
            errors.append("m_s")
        if gauge.get("numeric_physical_delta_hat") != gauge.get("numeric_reference_delta_rect"):
            errors.append("delta preservation")
        if gauge.get("length_loss_under_pullback") != "1":
            errors.append("length loss")
        if gauge.get("generic_measure_trivializing_interface_used_for_numeric_bound") is not False:
            errors.append("generic interface overclaim")
        if "only from this fixed-radius translation pilot" not in gauge.get("generic_interface_warning", ""):
            errors.append("instance scope warning")

        target = result.get("explicit_uniform_open_C24_target", {})
        if target.get("status") != "CERTIFIED_NUMERIC_UNIFORM_OPEN_C24_TARGET_NOT_CANTOR_RECTANGLE":
            errors.append("target status")
        if target.get("closure_strictly_inside_C24") is not True:
            errors.append("target closure")
        if target.get("is_a_dynamical_Cantor_rectangle") is not False:
            errors.append("target type overclaim")
        if target.get("ratio_to_required_hit_gap") != "225/32":
            errors.append("target ratio")

        bump = result.get("uniform_standard_family_bump_minorisation", {})
        if bump.get("status") != "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_WITH_NUMERIC_HIT_FRACTION":
            errors.append("bump status")
        if bump.get("uniform_exponential_constants_exist") is not True:
            errors.append("uniform theorem join")
        dynamic = bump.get("uniform_SYZ_dynamic_density_bridge", {})
        if dynamic.get("status") != "CERTIFIED_SPATIAL_TO_SYZ_DYNAMIC_REGULARITY":
            errors.append("dynamic density bridge")
        if dynamic.get("global_adapted_u_curve_length_strict_upper") != "40":
            errors.append("dynamic global length")
        if dynamic.get("inverse_contraction_cube_root_strict_upper") != "93/100":
            errors.append("dynamic separation rate")
        if dynamic.get("uniform_dynamic_density_constant_upper") != "2000000000000000000000000000":
            errors.append("dynamic density constant")
        if "2e27*(93/100)^s(x,y)" not in dynamic.get("separation_time_conclusion", ""):
            errors.append("dynamic density conclusion")
        comparison = bump.get("comparison_probability_typing", {})
        if comparison.get("density_relative_to_common_collision_law") != "1":
            errors.append("comparison density")
        if comparison.get("log_density_constant") != "0":
            errors.append("comparison log density")
        if comparison.get("uniform_finite_Z_and_density_regularity") is not True:
            errors.append("comparison regularity")
        if bump.get("uniform_bump_theorem_norm") != "norm_infinity(g)+Lipschitz_1(g)<2724":
            errors.append("bump theorem norm")
        if bump.get("one_uniform_finite_integer_H_bump_exists") is not True:
            errors.append("uniform H existence")
        for key in ("numeric_C_bump", "numeric_theta_bump", "numeric_H_bump"):
            if bump.get(key) is not None:
                errors.append(f"bump numerical overclaim: {key}")
        if bump.get("actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump") != "21/111718750":
            errors.append("bump hit fraction")
        if bump.get("cover_crossing_source_fraction_per_retained_leaf") is not None:
            errors.append("cover source fraction overclaim")
        if bump.get("does_not_require_materialized_Cantor_source_cover") is not True:
            errors.append("bypass type")

        counter = result.get("numerical_non_effectivity_countermodel", {})
        if counter.get("logical_obstruction_certified") is not True:
            errors.append("non-effectivity countermodel")
        if "theta^H0>=1-H0/(2*(H0+1))>1/2" not in counter.get("for_each_proposed_integer_H0", ""):
            errors.append("countermodel inequality")

        frontier = result.get("cover_effectivity_frontier", {})
        if frontier.get("status") != "PARTIALLY_RESOLVED_GAUGE_AND_TARGET_NUMERIC_CLOCK_STILL_NONEFFECTIVE":
            errors.append("frontier status")
        if frontier.get("numeric_H_cover") is not None or frontier.get("numeric_H_bump") is not None:
            errors.append("frontier numerical H overclaim")
        if frontier.get("actual_cover_crossing_source_fraction") is not None:
            errors.append("frontier source fraction overclaim")
        if frontier.get("strict_inferable_uniform_cover_source_fraction_lower") != "0":
            errors.append("source fraction lower")
        registry = frontier.get("finite_registry_type_audit", {})
        if registry.get("twenty_four_C24_boxes_total_normalized_mass_strict_upper") != "1/2500":
            errors.append("registry mass")
        if registry.get("therefore_existing_finite_registries_do_not_supply_K_rect") is not True:
            errors.append("registry type")

        corrected = result.get("corrected_frontier", {})
        expected_corrected = {
            "uniform_numeric_conjugacy_factor_m_s": "CERTIFIED_EXACT_1",
            "uniform_numeric_open_C24_target": "CERTIFIED",
            "uniform_finite_bump_hit_time_exists_but_is_not_numerical": True,
            "numeric_whole_family_hit_fraction_at_existential_time": "21/111718750",
            "numeric_H_cover": None,
            "numeric_H_bump": None,
            "numeric_proper_crossing_source_atlas": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        }
        if corrected != expected_corrected:
            errors.append("corrected frontier")

        expected_verdict = {
            "instance_specific_uniform_m_s_equals_1": "CERTIFIED",
            "explicit_uniform_open_C24_target": "CERTIFIED",
            "uniform_existential_time_numeric_hit_fraction": "CERTIFIED",
            "uniform_numeric_H_cover": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected_verdict:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("dependencies",), {}),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "claim_type"), "numeric closure"),
        (("result", "literature_quantifier_audit", "rows_sha256"), "0" * 64),
        (("result", "literature_quantifier_audit", "official_sources_publish_numeric_cover_or_mixing_constants"), True),
        (("result", "literature_quantifier_audit", "rows", 0, "official_source_sha256"), "0" * 64),
        (("result", "literature_quantifier_audit", "rows", 1, "safe_quantifier"), "effective"),
        (("result", "literature_quantifier_audit", "rows", 2, "paper"), "wrong"),
        (("result", "instance_specific_fixed_gauge", "status"), "GENERIC"),
        (("result", "instance_specific_fixed_gauge", "parameter_window"), "fixed s"),
        (("result", "instance_specific_fixed_gauge", "physical_path"), "shape change"),
        (("result", "instance_specific_fixed_gauge", "collision_metric"), "adapted"),
        (("result", "instance_specific_fixed_gauge", "literature_metric_match"), "none"),
        (("result", "instance_specific_fixed_gauge", "rows_sha256"), "0" * 64),
        (("result", "instance_specific_fixed_gauge", "rows", 0, "coordinate_derivative"), "2I"),
        (("result", "instance_specific_fixed_gauge", "rows", 1, "least_singular_value"), "1/2"),
        (("result", "instance_specific_fixed_gauge", "generic_measure_trivializing_interface_used_for_numeric_bound"), True),
        (("result", "instance_specific_fixed_gauge", "generic_interface_warning"), "generic is numeric"),
        (("result", "instance_specific_fixed_gauge", "uniform_numeric_m_s"), "1/2"),
        (("result", "instance_specific_fixed_gauge", "numeric_reference_delta_rect"), "1"),
        (("result", "instance_specific_fixed_gauge", "numeric_physical_delta_hat"), "1"),
        (("result", "instance_specific_fixed_gauge", "length_loss_under_pullback"), "2"),
        (("result", "explicit_uniform_open_C24_target", "status"), "CANTOR"),
        (("result", "explicit_uniform_open_C24_target", "chart"), "G:N"),
        (("result", "explicit_uniform_open_C24_target", "ambient_C24_core", "t", 0), "0"),
        (("result", "explicit_uniform_open_C24_target", "open_box_O_star", "t", 0), "1/100"),
        (("result", "explicit_uniform_open_C24_target", "open_box_O_star", "p", 1), "1/500"),
        (("result", "explicit_uniform_open_C24_target", "closure_strictly_inside_C24"), False),
        (("result", "explicit_uniform_open_C24_target", "uniform_for_parameter_window"), "fixed s"),
        (("result", "explicit_uniform_open_C24_target", "unnormalized_mass_strict_lower"), "1"),
        (("result", "explicit_uniform_open_C24_target", "normalization_strict_upper_using_pi_lt_22_over_7"), "1"),
        (("result", "explicit_uniform_open_C24_target", "normalized_collision_mass_strict_lower"), "1"),
        (("result", "explicit_uniform_open_C24_target", "ratio_to_required_hit_gap"), "1"),
        (("result", "explicit_uniform_open_C24_target", "is_a_dynamical_Cantor_rectangle"), True),
        (("result", "uniform_standard_family_bump_minorisation", "status"), "NUMERIC_TIME"),
        (("result", "uniform_standard_family_bump_minorisation", "family_scope"), "one family"),
        (("result", "uniform_standard_family_bump_minorisation", "numeric_uniform_Z_envelope_C_p_E"), "0"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_bump_mass_strict_lower"), "0"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_bump_theorem_norm"), "1"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_SYZ_dynamic_density_bridge", "status"), "NOT_CERTIFIED"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_SYZ_dynamic_density_bridge", "global_adapted_u_curve_length_strict_upper"), "41"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_SYZ_dynamic_density_bridge", "inverse_contraction_cube_root_strict_upper"), "1"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_SYZ_dynamic_density_bridge", "uniform_dynamic_density_constant_upper"), "0"),
        (("result", "uniform_standard_family_bump_minorisation", "comparison_probability_typing", "density_relative_to_common_collision_law"), "2"),
        (("result", "uniform_standard_family_bump_minorisation", "comparison_probability_typing", "uniform_finite_Z_and_density_regularity"), False),
        (("result", "uniform_standard_family_bump_minorisation", "theorem_join"), "not joined"),
        (("result", "uniform_standard_family_bump_minorisation", "uniform_exponential_constants_exist"), False),
        (("result", "uniform_standard_family_bump_minorisation", "numeric_C_bump"), "1"),
        (("result", "uniform_standard_family_bump_minorisation", "numeric_theta_bump"), "1/2"),
        (("result", "uniform_standard_family_bump_minorisation", "safe_time_formula"), "H=1"),
        (("result", "uniform_standard_family_bump_minorisation", "one_uniform_finite_integer_H_bump_exists"), False),
        (("result", "uniform_standard_family_bump_minorisation", "numeric_H_bump"), 1),
        (("result", "uniform_standard_family_bump_minorisation", "conclusion"), "no hit"),
        (("result", "uniform_standard_family_bump_minorisation", "actual_whole_family_C24_hit_fraction_strict_lower_at_H_bump"), "0"),
        (("result", "uniform_standard_family_bump_minorisation", "cover_crossing_source_fraction_per_retained_leaf"), "1"),
        (("result", "uniform_standard_family_bump_minorisation", "does_not_require_materialized_Cantor_source_cover"), False),
        (("result", "numerical_non_effectivity_countermodel", "for_each_proposed_integer_H0"), "false"),
        (("result", "numerical_non_effectivity_countermodel", "resulting_error_majorant"), "small"),
        (("result", "numerical_non_effectivity_countermodel", "logical_obstruction_certified"), False),
        (("result", "cover_effectivity_frontier", "status"), "CLOSED"),
        (("result", "cover_effectivity_frontier", "missing_rows_sha256"), "0" * 64),
        (("result", "cover_effectivity_frontier", "original_cover_route_missing_numeric_rows", 0, "value"), "row"),
        (("result", "cover_effectivity_frontier", "original_cover_route_missing_numeric_rows", 1, "id"), "atlas"),
        (("result", "cover_effectivity_frontier", "resolved_rows", "uniform_conjugacy_length_factor"), "1/2"),
        (("result", "cover_effectivity_frontier", "resolved_rows", "uniform_finite_bump_hit_time_exists"), False),
        (("result", "cover_effectivity_frontier", "finite_registry_type_audit", "twenty_four_C24_boxes_total_normalized_mass_strict_upper"), "1"),
        (("result", "cover_effectivity_frontier", "finite_registry_type_audit", "twenty_four_boxes_are_target_coordinate_boxes_not_proper_Cantor_source_rectangles"), False),
        (("result", "cover_effectivity_frontier", "finite_registry_type_audit", "therefore_existing_finite_registries_do_not_supply_K_rect"), False),
        (("result", "cover_effectivity_frontier", "numeric_H_cover"), 1),
        (("result", "cover_effectivity_frontier", "numeric_H_bump"), 1),
        (("result", "cover_effectivity_frontier", "actual_cover_crossing_source_fraction"), "1"),
        (("result", "cover_effectivity_frontier", "strict_inferable_uniform_cover_source_fraction_lower"), "1/2"),
        (("result", "corrected_frontier", "uniform_numeric_conjugacy_factor_m_s"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_proper_crossing_source_atlas"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "instance_specific_uniform_m_s_equals_1"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "uniform_numeric_H_cover"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    bodies: list[str] = []
    for field_path, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, field_path, replacement)
        bodies.append(json.dumps(mutation, sort_keys=True) + "\n")
    bodies.append('{"schema":"x","schema":"y"}\n')
    extra = copy.deepcopy(source)
    extra["unexpected"] = 1
    bodies.append(json.dumps(extra, sort_keys=True) + "\n")
    valid = json.dumps(source, sort_keys=True)
    bodies.append(valid[:-1] + ',"unexpected":NaN}\n')

    passed = 0
    for body in bodies:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r51-cover-hostile-",
            suffix=".json",
            dir=cert.HERE,
            delete=False,
        )
        candidate = Path(handle.name)
        try:
            with handle:
                handle.write(body)
            errors = verify(candidate)
            if errors and errors != ["unsafe manifest"]:
                passed += 1
        finally:
            candidate.unlink(missing_ok=True)
    return passed, len(bodies)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.self_test:
        passed, total = self_test(args.manifest)
        print(f"SELF_TEST: {passed}/{total}")
        return 0 if passed == total else 1
    print("VERIFY: PASS")
    if args.integrity_only or args.replay:
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
