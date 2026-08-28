#!/usr/bin/env python3
"""Fail-closed verifier for actual-parameter all-scale recovery germs."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_parameter_dq_all_scale_shell_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.parameter-dq-all-scale-shell.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.parameter-dq-all-scale-shell.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_parameter_dq_all_scale_shell_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest type"]
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if manifest.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency table")
    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    jacobian = result.get("exact_parameter_angle_jacobian", {})
    expected_derivatives = {
        "partial_h_Delta_at_0": "2*eta*epsilon*R_T*u_y",
        "partial_alpha_Delta_at_0": "2*epsilon*R_T*ell_T",
        "clearance_matched_phase_angle_dalpha_dh": "eta*u_y/ell_T",
        "tangent_graph_dp_dh": "-eta*cp*u_y/ell_T",
        "signed_face_coarea": "eta*epsilon*cp*u_y/ell_T",
    }
    if jacobian.get("exact_first_derivatives") != expected_derivatives:
        errors.append("exact derivatives")
    if jacobian.get("global_on_all_64_open_maximal_occurrence_rows") is not True:
        errors.append("global Jacobian rows")
    if jacobian.get("corrected_positive_face_law") != (
        "R_source*cp*abs(u_y)/ell_T*dtheta"
    ):
        errors.append("corrected face law")
    if jacobian.get("superseded_extra_cp_not_used") is not True:
        errors.append("extra cp exclusion")

    registry = result.get("selected_parameter_dq_all_scale_germ_registry", {})
    expected = {
        "selected_occurrence_parameter_germ_count": 64,
        "oriented_actual_parameter_tube_germ_count": 128,
        "parameter_magnitude_interval": ["0_open", "1/65536"],
        "all_dyadic_scales_below_radius_included": True,
        "hit_parameter_sign_equals_corrected_coarea_polarity": True,
        "miss_parameter_sign_equals_negative_corrected_coarea_polarity": True,
        "base_half_width_power_histogram": {
            "10": 40, "11": 16, "12": 4, "14": 4,
        },
        "labelled_base_event_coordinate_area": "2833/16777216",
        "labelled_two_side_parameter_coordinate_volume": (
            "2833/549755813888"
        ),
        "all_hit_germs_first_hit_tangent_target": True,
        "all_hit_germs_next_hit_fixed_miss_target": True,
        "all_miss_germs_first_hit_fixed_miss_target": True,
        "all_two_side_successors_regular": True,
        "all_two_side_successors_share_one_suffix_chart_per_occurrence": True,
        "selected_face_time_collision_offset": 1,
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    expected_bounds = {
        "cosine_strict_lower": "1/20",
        "abs_p_strict_upper": "999/1000",
        "each_owner_flight_strict_upper": "2",
    }
    if registry.get("uniform_suffix_bounds") != expected_bounds:
        errors.append("suffix bounds")
    expected_suffix = {
        "G:E": 10, "G:N": 12, "G:S": 12, "G:W": 10,
        "W:E": 4, "W:N": 6, "W:S": 6, "W:W": 4,
    }
    if registry.get("suffix_regular_chart_histogram") != expected_suffix:
        errors.append("suffix histogram")
    universe = registry.get("complete_local_candidate_universe", {})
    if universe.get("candidate_count_after_exclusion") != 161:
        errors.append("candidate count")
    if universe.get("window_radius_4_exceeds_required_center_offset") is not True:
        errors.append("candidate completeness")
    for key in ("parameter_germ_rows_sha256", "imported_maximal_rows_sha256"):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "selected_germs_exhaust_every_point_of_every_maximal_row",
        "first_order_clearance_angle_identification_is_finite_conjugacy",
        "selected_face_time_is_common_strong_space_FACE_TIME",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "full_boundary_all_scale_tubular_atlas",
        "bounded_grazing_pushforward",
        "first_24_core_destination",
        "native_no_recut_dwell",
        "common_strong_space_restriction",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "parameter_angle_Jacobian_rows_64": "CERTIFIED",
        "selected_parameter_DQ_all_scale_germs_64": "CERTIFIED",
        "oriented_actual_parameter_tube_germs_128": "CERTIFIED",
        "full_boundary_all_scale_tubular_atlas": "NOT_CERTIFIED",
        "first_24_core_destination": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    base = ("result", "selected_parameter_dq_all_scale_germ_registry")
    mutate(base + ("selected_occurrence_parameter_germ_count",), 63)
    mutate(base + ("oriented_actual_parameter_tube_germ_count",), 126)
    mutate(base + ("parameter_magnitude_interval",), ["0", "0"])
    mutate(base + ("all_dyadic_scales_below_radius_included",), False)
    mutate(base + ("hit_parameter_sign_equals_corrected_coarea_polarity",), False)
    mutate(base + ("base_half_width_power_histogram", "10"), 39)
    mutate(base + ("all_hit_germs_first_hit_tangent_target",), False)
    mutate(base + ("all_hit_germs_next_hit_fixed_miss_target",), False)
    mutate(base + ("all_miss_germs_first_hit_fixed_miss_target",), False)
    mutate(base + ("selected_face_time_collision_offset",), 0)
    mutate(base + ("uniform_suffix_bounds", "cosine_strict_lower"), "0")
    mutate(base + ("complete_local_candidate_universe", "candidate_count_after_exclusion"), 160)
    jac = ("result", "exact_parameter_angle_jacobian")
    mutate(jac + ("superseded_extra_cp_not_used",), False)
    mutate(jac + ("global_on_all_64_open_maximal_occurrence_rows",), False)
    mutate(jac + ("corrected_positive_face_law",), "cp^2")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("selected_germs_exhaust_every_point_of_every_maximal_row",), True)
    mutate(scope + ("selected_face_time_is_common_strong_space_FACE_TIME",), True)
    mutate(scope + ("bounded_grazing_pushforward",), "CERTIFIED")
    mutate(scope + ("first_24_core_destination",), "CERTIFIED")
    mutate(scope + ("native_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("Gate3",), "CERTIFIED")
    mutate(("verdict", "full_boundary_all_scale_tubular_atlas"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != manifest["result"]:
        print("ERROR: replay mismatch", file=sys.stderr)
        return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("PARAMETER_ANGLE_JACOBIAN_ROWS_64: CERTIFIED")
    print("SELECTED_PARAMETER_DQ_ALL_SCALE_GERMS_64: CERTIFIED")
    print("ORIENTED_ACTUAL_PARAMETER_TUBE_GERMS_128: CERTIFIED")
    print("FULL_BOUNDARY_ALL_SCALE_TUBULAR_ATLAS: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
