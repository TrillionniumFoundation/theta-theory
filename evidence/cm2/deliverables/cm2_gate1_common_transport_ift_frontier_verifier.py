#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 common-transport frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate1_common_transport_ift_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate1.common-transport-ift-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate1.common-transport-ift-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-common-transport-ift-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate1_common_transport_ift_frontier_cert.py"


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

    columns = result.get("exact_column_replay", {})
    for key in ("determinant_one_frame_at_x", "determinant_one_frame_at_y"):
        if columns.get(key) != "1":
            errors.append(f"columns {key}")
    if columns.get("stable_half_density_is_first_column_wedge") != "-1/2":
        errors.append("stable wedge")
    if columns.get("unstable_half_density_is_reversed_second_column_wedge") != "7/9":
        errors.append("unstable wedge")

    transport = result.get("common_transport_anchor_lemma_replay", {})
    expected_transport = {
        "plaque_point_count": 4,
        "common_transport_determinant": "1/3",
        "all_pair_wedges_scale_by_common_determinant": True,
        "two_noncollinear_anchor_images_reconstruct_unique_transport": True,
        "all_other_images_forced_by_anchor_wedge_data": True,
        "perturbed_nontransport_image_breaks_pair_equations": True,
    }
    for key, expected in expected_transport.items():
        if transport.get(key) != expected:
            errors.append(f"transport {key}")

    audit = result.get("small_amplitude_half_density_audit", {})
    if audit.get("exact_product_mismatch") != "-487/10000":
        errors.append("amplitude mismatch")
    if audit.get("first_epsilon_derivative_at_zero") != "0":
        errors.append("amplitude derivative")
    model = audit.get("amplitude_alone_does_not_change_decay_exponent_model", {})
    if model.get("theta_over_r") != "8":
        errors.append("amplification ratio")
    if model.get("diverges_for_every_nonzero_epsilon_when_theta_over_r_gt_1") is not True:
        errors.append("amplification conclusion")
    if audit.get("model_is_not_an_obstruction_for_every_possible_physical_gauge") is not True:
        errors.append("model scope")

    reduction = result.get("structural_reduction", {})
    if reduction.get("symmetric_unstable_anchor_lemma") is not True:
        errors.append("unstable anchor lemma")
    if len(reduction.get("new_unknowns_exposed", [])) != 4:
        errors.append("unknown list")

    literature = result.get("literature_and_ift_audit", {})
    if literature.get("direct_nonfiber_bunched_half_density_solver_found") is not False:
        errors.append("literature solver")
    if literature.get("plain_small_amplitude_ift_has_bounded_right_inverse_certified") is not False:
        errors.append("IFT inverse")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "small_amplitude_by_itself_closes_combined_class_H",
        "common_transport_reduction_supplies_physical_solution",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "uniform_big_cell_q_lower_bound",
        "coupled_half_density_groupoid_solution",
        "same_representative_class_H_plus_twisting",
        "Gate1",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "common_plaque_transport_reduction": "CERTIFIED",
        "plain_small_amplitude_ift_promotion": "REJECTED",
        "coupled_half_density_groupoid_solution": "NOT_CERTIFIED",
        "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
        "Gate1": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


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

    mutate(("result", "exact_column_replay", "determinant_one_frame_at_x"), "0")
    mutate(("result", "exact_column_replay", "stable_half_density_is_first_column_wedge"), "0")
    mutate(("result", "common_transport_anchor_lemma_replay", "plaque_point_count"), 3)
    mutate(("result", "common_transport_anchor_lemma_replay", "common_transport_determinant"), "1")
    mutate(("result", "common_transport_anchor_lemma_replay", "all_pair_wedges_scale_by_common_determinant"), False)
    mutate(("result", "common_transport_anchor_lemma_replay", "perturbed_nontransport_image_breaks_pair_equations"), False)
    mutate(("result", "small_amplitude_half_density_audit", "exact_product_mismatch"), "0")
    mutate(("result", "small_amplitude_half_density_audit", "first_epsilon_derivative_at_zero"), "1")
    mutate(("result", "small_amplitude_half_density_audit", "model_is_not_an_obstruction_for_every_possible_physical_gauge"), False)
    mutate(("result", "structural_reduction", "symmetric_unstable_anchor_lemma"), False)
    mutate(("result", "literature_and_ift_audit", "direct_nonfiber_bunched_half_density_solver_found"), True)
    mutate(("result", "literature_and_ift_audit", "plain_small_amplitude_ift_has_bounded_right_inverse_certified"), True)
    mutate(("result", "strict_nonpromotion", "small_amplitude_by_itself_closes_combined_class_H"), True)
    mutate(("result", "strict_nonpromotion", "coupled_half_density_groupoid_solution"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate1"), "CERTIFIED")
    mutate(("verdict", "plain_small_amplitude_ift_promotion"), "CERTIFIED")
    mutate(("verdict", "coupled_half_density_groupoid_solution"), "CERTIFIED")
    mutate(("verdict", "Gate1"), "CERTIFIED")
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
    print("COMMON_PLAQUE_TRANSPORT_REDUCTION: CERTIFIED")
    print("PLAIN_SMALL_AMPLITUDE_IFT_PROMOTION: REJECTED")
    print("COUPLED_HALF_DENSITY_SOLUTION: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
