#!/usr/bin/env python3
"""Verifier for the Round-46 extended-parent density certificate."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate34_round46_extended_parent_density_frontier_cert as cert


HERE = Path(__file__).resolve().parent


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
        registry = result.get("extended_pre_recut_parent_bundle_registry", {})
        if registry.get("status") != (
            "CERTIFIED_PARAMETERIZED_EXTENDED_PRE_RECUT_BUNDLE_REGISTRY"
        ):
            errors.append("extended registry")
        if registry.get("artificial_recut_preserves_measure") is not True:
            errors.append("recut measure")
        density = result.get("numeric_cross_cell_density_continuation", {})
        if density.get("extended_parent_density_ratio_strict_upper_R_ext") != (
            "400000000/399794003"
        ):
            errors.append("R_ext")
        if density.get("status") != (
            "CERTIFIED_NUMERIC_CROSS_CELL_DENSITY_AND_WEIGHT_CONTINUATION"
        ):
            errors.append("density continuation")
        frontier = result.get("C24_covering_frontier_after_R_ext", {})
        if frontier.get("one_crossing_extended_parent_hit_fraction_strict_lower") != (
            "399794003/1200000000000"
        ):
            errors.append("pair hit")
        if frontier.get("exact_sufficient_crossing_bundle_weight") != (
            "beta>4608000/8167220347"
        ):
            errors.append("beta threshold")
        if frontier.get("numeric_H_cover") is not None:
            errors.append("H_cover overclaim")
        if frontier.get("numeric_beta") is not None:
            errors.append("beta overclaim")
        strict = result.get("strict_nonpromotion", {})
        expected = {
            "extended_pre_recut_parent_bundle_registry": "CERTIFIED",
            "numeric_cross_cell_R_ext": "CERTIFIED",
            "numeric_H_cover_and_beta": "NOT_CERTIFIED",
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
        (("result", "provenance", "parameter_scope"), "one s"),
        (("result", "provenance", "path_scope"), "depth one"),
        (("result", "extended_pre_recut_parent_bundle_registry", "source_object"), "none"),
        (("result", "extended_pre_recut_parent_bundle_registry", "image_object"), "recut child"),
        (("result", "extended_pre_recut_parent_bundle_registry", "extended_parent_bundle_id_schema"), "bad"),
        (("result", "extended_pre_recut_parent_bundle_registry", "ordered_child_id_schema"), "bad"),
        (("result", "extended_pre_recut_parent_bundle_registry", "child_union"), "not exhaustive"),
        (("result", "extended_pre_recut_parent_bundle_registry", "artificial_recut_preserves_measure"), False),
        (("result", "extended_pre_recut_parent_bundle_registry", "child_weights"), "independent"),
        (("result", "extended_pre_recut_parent_bundle_registry", "same_ID_forward_reverse_compatibility"), False),
        (("result", "extended_pre_recut_parent_bundle_registry", "finite_integer_bundle_count_claimed"), True),
        (("result", "extended_pre_recut_parent_bundle_registry", "status"), "NOT_CERTIFIED"),
        (("result", "numeric_cross_cell_density_continuation", "source_cell_adapted_length_upper"), "1"),
        (("result", "numeric_cross_cell_density_continuation", "source_conditional_density_ratio_upper"), "2"),
        (("result", "numeric_cross_cell_density_continuation", "one_step_log_Jacobian_variation_strict_upper"), "1/100"),
        (("result", "numeric_cross_cell_density_continuation", "Jacobian_ratio_upper_via_exp_x_le_1_over_1_minus_x"), "1"),
        (("result", "numeric_cross_cell_density_continuation", "pushforward_density_formula"), "rho_image=rho_source"),
        (("result", "numeric_cross_cell_density_continuation", "extended_parent_density_ratio_strict_upper_R_ext"), "2000/1999"),
        (("result", "numeric_cross_cell_density_continuation", "cross_cell_weight_continuation"), "none"),
        (("result", "numeric_cross_cell_density_continuation", "independent_child_weight_model_excluded"), False),
        (("result", "numeric_cross_cell_density_continuation", "status"), "NOT_CERTIFIED"),
        (("result", "C24_covering_frontier_after_R_ext", "one_crossing_extended_parent_hit_fraction_strict_lower"), "0"),
        (("result", "C24_covering_frontier_after_R_ext", "family_hit_fraction"), "0"),
        (("result", "C24_covering_frontier_after_R_ext", "exact_sufficient_crossing_bundle_weight"), "beta>0"),
        (("result", "C24_covering_frontier_after_R_ext", "safe_reciprocal_beta"), "1/1773"),
        (("result", "C24_covering_frontier_after_R_ext", "next_reciprocal_fails"), "1/1772"),
        (("result", "C24_covering_frontier_after_R_ext", "numeric_R_ext"), None),
        (("result", "C24_covering_frontier_after_R_ext", "numeric_H_cover"), 1),
        (("result", "C24_covering_frontier_after_R_ext", "numeric_beta"), "1/1772"),
        (("result", "C24_covering_frontier_after_R_ext", "post_C24_cut_same_proper_class_return"), "CERTIFIED"),
        (("result", "C24_covering_frontier_after_R_ext", "numeric_proper_family_C24_minorization"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_cover_and_beta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "numeric_collision_time_q"), "CERTIFIED"),
    ]
    mutations: list[dict[str, Any]] = []
    for path_keys, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, path_keys, replacement)
        mutations.append(mutation)
    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append(mutation)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            target = Path(directory) / f"mutation-{index}.json"
            target.write_text(json.dumps(mutation), encoding="utf-8")
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

