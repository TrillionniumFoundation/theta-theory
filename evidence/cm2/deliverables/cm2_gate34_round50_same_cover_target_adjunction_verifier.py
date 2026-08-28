#!/usr/bin/env python3
"""Fail-closed verifier for the Round-50 enlarged-cover target adjunction."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round50_same_cover_target_adjunction_cert as cert


EXPECTED_MANIFEST_KEYS = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_checks(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    mass = Q(1999, 32000)
    fraction = Q(2688, 893303125)
    hit = Q(21, 111718750)
    if mass * fraction != hit:
        errors.append("direct threshold product")
    if not (Q(1, 332330) > fraction > Q(1, 332331)):
        errors.append("direct threshold reciprocal")

    rows = [
        {
            "paper": "Climenhaga--Day, arXiv:2604.25881v1",
            "official_source_sha256": cert.ARXIV_2604_SOURCE_SHA256,
            "source_anchor": "Proposition 3.19 and proof sketch, source lines 1568--1586",
            "frozen_fact": (
                "for one fixed finite-horizon Sinai billiard, the authors first choose a countable high-density Cantor cover; for every delta and target R0 in that cover, compactness gives finitely many proper-crossing source rectangles and Liouville mixing gives one finite iterate N for all admissible u-curves at that scale"
            ),
            "effectivity": "qualitative only",
        },
        {
            "paper": "Baladi--Demers, arXiv:1807.02330v4",
            "official_source_sha256": cert.ARXIV_1807_SOURCE_SHA256,
            "source_anchor": (
                "Definitions at source lines 2430--2468; cover construction 3914--3944; open-target rectangle 4067--4096"
            ),
            "frozen_fact": (
                "for a fixed billiard, a regular open set contains a positive Liouville Cantor rectangle whose solid hull stays in the open set; these lines do not assert that this target rectangle itself satisfies the global 0.9 cover condition"
            ),
            "effectivity": "qualitative only",
        },
        {
            "paper": "Baladi--Demers proof mechanism used by Proposition 3.19",
            "official_source_sha256": cert.ARXIV_1807_SOURCE_SHA256,
            "source_anchor": "source lines 2508--2533",
            "frozen_fact": (
                "inside a positive target rectangle, leafwise Lebesgue differentiation and absolute continuity select a separate positive uniformly-dense subset in the required orientation; for a finite proper-crossing source family, Liouville mixing then gives a common finite time and the crossing lemma extracts a target-crossing subcurve"
            ),
            "effectivity": "no numerical time or subcurve width",
        },
    ]
    audit = result.get("literature_audit", {})
    if audit.get("rows") != rows:
        errors.append("literature rows")
    if audit.get("rows_sha256") != cert.digest(rows):
        errors.append("literature digest")

    expected_steps = [
        {
            "step": 1,
            "claim": (
                "fix s and write T_s=A_s^{-1} hat_T_s A_s; compactness and the diffeomorphism property give m_s=inf_x sigma_min(DA_s(x))>0, so every reference admissible u-curve V with length at least delta_rect maps to a physical admissible u-curve A_s(V) with length at least hat_delta_s=m_s*delta_rect>0"
            ),
        },
        {
            "step": 2,
            "claim": (
                "map the closure-contained direct-C24 open core O_s to hat_O_s=A_s(O_s), and inside hat_O_s choose a positive locally maximal Cantor rectangle hat_R_* with D(hat_R_*) subset hat_O_s"
            ),
        },
        {
            "step": 3,
            "claim": (
                "inside hat_R_* select a separate positive uniformly-dense subset hat_P_* in the leaf orientation required by the forward unstable-curve crossing argument; no global 0.9 condition is claimed for hat_R_* itself"
            ),
        },
        {
            "step": 4,
            "claim": (
                "adjoin hat_R_* to the published physical countable cover and retain, at the positive scale hat_delta_s, the original finite proper-crossing source subcover; the enlarged cover remains countable and covers the physical regular set"
            ),
        },
        {
            "step": 5,
            "claim": (
                "Liouville mixing for the finitely many original-source/hat_P_* pairs gives one finite N_s; the published crossing argument gives, in every physical admissible u-curve of length at least hat_delta_s, a subcurve whose hat_T_s^N_s image crosses hat_R_*"
            ),
        },
        {
            "step": 6,
            "claim": (
                "pull the enlarged cover, target rectangle and crossing subcurve back by A_s^{-1}; crossing is preserved by conjugacy and D(A_s^{-1}hat_R_*) lies in O_s subset C24, yielding the fixed-s T_s target hit for every reference admissible u-curve of length at least delta_rect"
            ),
        },
    ]
    bridge = result.get("fixed_parameter_enlarged_cover_target_adjunction", {})
    if bridge.get("proof_steps") != expected_steps:
        errors.append("adjunction proof steps")
    if bridge.get("proof_steps_sha256") != cert.digest(expected_steps):
        errors.append("adjunction proof digest")

    missing_ids = [
        "K_rect",
        "m_conjugacy",
        "m_rect",
        "delta_density",
        "C_mix_theta_mix",
        "N_mix",
        "r_transverse",
        "J_branch",
        "omega_parameter",
    ]
    frontier = result.get("numerical_effectivity_frontier", {})
    missing = frontier.get("missing_numeric_constants", [])
    if not isinstance(missing, list) or [row.get("id") for row in missing] != missing_ids:
        errors.append("missing constant registry")
    elif any(row.get("published_value", "bad") is not None for row in missing):
        errors.append("missing constant overclaim")
    if frontier.get("missing_numeric_constants_sha256") != cert.digest(missing):
        errors.append("missing constant digest")
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
            digest_payload = dict(result)
            stored_digest = digest_payload.pop("internal_replay_digest", None)
            if stored_digest != cert.digest(digest_payload):
                errors.append("internal replay digest")
        else:
            errors.append("result root")
        errors.extend(independent_checks(result))

        audit = result.get("literature_audit", {})
        if audit.get("enlarged_cover_adjunction_is_a_derived_lemma") is not True:
            errors.append("derived lemma scope")
        if audit.get("not_a_verbatim_numbered_theorem") is not True:
            errors.append("literature overclaim")

        bridge = result.get("fixed_parameter_enlarged_cover_target_adjunction", {})
        if bridge.get("status") != (
            "CERTIFIED_FIXED_S_QUALITATIVE_ENLARGED_COVER_ADJUNCTION"
        ):
            errors.append("bridge status")
        if "one fixed parameter s" not in bridge.get("scope", ""):
            errors.append("bridge scope")
        if "A_s^{-1}(hat_V_s^u)" not in bridge.get("admissible_curve_scope", ""):
            errors.append("admissible u-curve scope")
        if bridge.get("pointwise_conjugacy_lower_length_factor_m_s_positive") is not True:
            errors.append("pointwise conjugacy factor")
        if bridge.get("physical_input_scale") != "hat_delta_s=m_s*delta_rect>0":
            errors.append("physical input scale")
        if bridge.get("numeric_m_s") is not None:
            errors.append("numeric m_s overclaim")
        if bridge.get("numeric_physical_input_scale") is not None:
            errors.append("numeric physical scale overclaim")
        if bridge.get("target_rectangle_itself_global_point9_claimed") is not False:
            errors.append("target rectangle 0.9 overclaim")
        if "separate positive hat_P_* subset" not in bridge.get(
            "uniformly_dense_target_subset", ""
        ):
            errors.append("separate target dense subset")
        if "enlarge/adjoin" not in bridge.get("cover_operation", ""):
            errors.append("enlarged-cover wording")
        if bridge.get("enlarged_cover_bridge_installed_fixed_s") is not True:
            errors.append("enlarged-cover bridge")
        if bridge.get("fixed_s_finite_target_hit_iterate_exists") is not True:
            errors.append("fixed-s finite hit")
        if bridge.get("target_crossing_implies_C24_entry") is not True:
            errors.append("C24 containment")
        for key in (
            "numeric_target_rectangle_coordinates",
            "numeric_finite_source_cover_rows",
            "numeric_N_s",
            "numeric_source_subcurve_fraction",
        ):
            if bridge.get(key) is not None:
                errors.append(f"bridge numerical overclaim: {key}")
        if bridge.get("physical_whole_family_join_installed") is not False:
            errors.append("whole-family overclaim")

        frontier = result.get("numerical_effectivity_frontier", {})
        if frontier.get("status") != (
            "CERTIFIED_EXACT_EFFECTIVITY_FRONTIER_NO_NUMERIC_PROMOTION"
        ):
            errors.append("effectivity status")
        if frontier.get("direct_C24_required_per_safe_leaf_source_fraction") != (
            "2688/893303125"
        ):
            errors.append("direct fraction field")
        if frontier.get("safe_reciprocal") != "1/332330":
            errors.append("safe reciprocal")
        if frontier.get("next_reciprocal_fails") != "1/332331":
            errors.append("failing reciprocal")
        if frontier.get("incidence_safe_family_mass") != "1999/32000":
            errors.append("safe family mass")
        if frontier.get("actual_source_fraction_from_theorem") is not None:
            errors.append("source fraction overclaim")
        if frontier.get("strict_inferable_uniform_source_fraction_lower") != "0":
            errors.append("source fraction lower")
        if frontier.get("numeric_uniform_H_cover") is not None:
            errors.append("numeric H overclaim")
        if frontier.get("numeric_actual_beta") is not None:
            errors.append("numeric beta overclaim")
        if frontier.get("strict_inferable_uniform_beta_lower") != "0":
            errors.append("uniform beta lower")

        parameter = result.get("parameter_window_frontier", {})
        if parameter.get("pointwise_fixed_s_enlarged_cover_bridge") != "CERTIFIED":
            errors.append("pointwise bridge")
        if parameter.get("published_theorem_quantifier") != (
            "one fixed physical billiard map hat_T_s"
        ):
            errors.append("published quantifier")
        if parameter.get("pointwise_conjugacy_factor_m_s_positive") is not True:
            errors.append("parameter pointwise conjugacy")
        if parameter.get("numeric_uniform_conjugacy_lower_factor") is not None:
            errors.append("uniform conjugacy numerical overclaim")
        for key in (
            "common_target_rectangle_registry_over_s",
            "common_finite_source_cover_rows_over_s",
            "branch_persistence_and_crossing_margin_over_s",
            "uniform_Liouville_mixing_constants_over_s",
        ):
            if parameter.get(key) != "NOT_CERTIFIED":
                errors.append(f"parameter promotion: {key}")
        if parameter.get("uniform_integer_N") is not None:
            errors.append("uniform integer overclaim")
        if parameter.get("compactness_of_parameter_interval_alone_is_sufficient") is not False:
            errors.append("compactness overclaim")

        corrected = result.get("corrected_frontier", {})
        if corrected.get("fixed_s_qualitative_C24_target_hit") != "CERTIFIED":
            errors.append("fixed-s target hit")
        if corrected.get("fixed_s_target_in_enlarged_sufficient_cover") != (
            "CERTIFIED_BY_ADJUNCTION"
        ):
            errors.append("fixed-s enlarged cover")
        if corrected.get("fixed_s_finite_H_exists_but_is_not_numerical") is not True:
            errors.append("fixed-s H existence")
        if corrected.get("numeric_H_cover") is not None:
            errors.append("corrected H overclaim")
        if corrected.get("numeric_actual_beta") is not None:
            errors.append("corrected beta overclaim")
        for key in (
            "uniform_parameter_window_numeric_rectangle_atlas",
            "physical_whole_family_grouping",
            "same_ID_two_orientation_cover",
            "complete_numeric_C_fw_C_rev_q",
            "strong_cemetery",
        ):
            if corrected.get(key) != "NOT_CERTIFIED":
                errors.append(f"corrected promotion: {key}")

        expected = {
            "fixed_s_qualitative_enlarged_cover_bridge": "CERTIFIED",
            "uniform_numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected:
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
        (("result", "provenance", "claim_type"), "numeric theorem"),
        (("result", "literature_audit", "rows_sha256"), "0" * 64),
        (("result", "literature_audit", "enlarged_cover_adjunction_is_a_derived_lemma"), False),
        (("result", "literature_audit", "not_a_verbatim_numbered_theorem"), False),
        (("result", "literature_audit", "rows", 0, "official_source_sha256"), "0" * 64),
        (("result", "literature_audit", "rows", 1, "frozen_fact"), "stronger"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "status"), "NUMERIC"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "scope"), "uniform all s"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "admissible_curve_scope"), "all curves"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "pointwise_conjugacy_lower_length_factor_m_s_positive"), False),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "physical_input_scale"), "delta_rect"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_m_s"), "1"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_physical_input_scale"), "1"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "target_rectangle_itself_global_point9_claimed"), True),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "uniformly_dense_target_subset"), "none"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "cover_operation"), "unchanged original cover"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "proof_steps_sha256"), "0" * 64),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "enlarged_cover_bridge_installed_fixed_s"), False),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "fixed_s_finite_target_hit_iterate_exists"), False),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "target_crossing_implies_C24_entry"), False),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_target_rectangle_coordinates"), [0, 1]),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_finite_source_cover_rows"), []),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_N_s"), 1),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "numeric_source_subcurve_fraction"), "1/2"),
        (("result", "fixed_parameter_enlarged_cover_target_adjunction", "physical_whole_family_join_installed"), True),
        (("result", "numerical_effectivity_frontier", "status"), "THEOREM"),
        (("result", "numerical_effectivity_frontier", "missing_numeric_constants_sha256"), "0" * 64),
        (("result", "numerical_effectivity_frontier", "missing_numeric_constants", 0, "published_value"), 1),
        (("result", "numerical_effectivity_frontier", "missing_numeric_constants", 5, "id"), "H"),
        (("result", "numerical_effectivity_frontier", "direct_C24_required_per_safe_leaf_source_fraction"), "0"),
        (("result", "numerical_effectivity_frontier", "safe_reciprocal"), "1/332331"),
        (("result", "numerical_effectivity_frontier", "next_reciprocal_fails"), "1/332330"),
        (("result", "numerical_effectivity_frontier", "incidence_safe_family_mass"), "1"),
        (("result", "numerical_effectivity_frontier", "actual_source_fraction_from_theorem"), "1/332330"),
        (("result", "numerical_effectivity_frontier", "strict_inferable_uniform_source_fraction_lower"), "1/332330"),
        (("result", "numerical_effectivity_frontier", "numeric_uniform_H_cover"), 1),
        (("result", "numerical_effectivity_frontier", "numeric_actual_beta"), "1/332330"),
        (("result", "numerical_effectivity_frontier", "strict_inferable_uniform_beta_lower"), "1/332330"),
        (("result", "parameter_window_frontier", "pointwise_fixed_s_enlarged_cover_bridge"), "NOT_CERTIFIED"),
        (("result", "parameter_window_frontier", "published_theorem_quantifier"), "uniform family"),
        (("result", "parameter_window_frontier", "pointwise_conjugacy_factor_m_s_positive"), False),
        (("result", "parameter_window_frontier", "numeric_uniform_conjugacy_lower_factor"), "1"),
        (("result", "parameter_window_frontier", "common_target_rectangle_registry_over_s"), "CERTIFIED"),
        (("result", "parameter_window_frontier", "common_finite_source_cover_rows_over_s"), "CERTIFIED"),
        (("result", "parameter_window_frontier", "branch_persistence_and_crossing_margin_over_s"), "CERTIFIED"),
        (("result", "parameter_window_frontier", "uniform_Liouville_mixing_constants_over_s"), "CERTIFIED"),
        (("result", "parameter_window_frontier", "uniform_integer_N"), 1),
        (("result", "parameter_window_frontier", "compactness_of_parameter_interval_alone_is_sufficient"), True),
        (("result", "corrected_frontier", "fixed_s_qualitative_C24_target_hit"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "fixed_s_target_in_enlarged_sufficient_cover"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "fixed_s_finite_H_exists_but_is_not_numerical"), False),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_beta"), "1/332330"),
        (("result", "corrected_frontier", "physical_whole_family_grouping"), "CERTIFIED"),
        (("result", "corrected_frontier", "same_ID_two_orientation_cover"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "fixed_s_qualitative_enlarged_cover_bridge"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    passed = 0
    bodies: list[str] = []
    for field_path, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, field_path, replacement)
        bodies.append(json.dumps(mutation, sort_keys=True) + "\n")
    bodies.append('{"schema":"x","schema":"y"}\n')
    extra_key = copy.deepcopy(source)
    extra_key["unexpected"] = 1
    bodies.append(json.dumps(extra_key, sort_keys=True) + "\n")
    valid_body = json.dumps(source, sort_keys=True)
    bodies.append(valid_body[:-1] + ',"unexpected":NaN}\n')
    for body in bodies:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r50-same-cover-hostile-",
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
