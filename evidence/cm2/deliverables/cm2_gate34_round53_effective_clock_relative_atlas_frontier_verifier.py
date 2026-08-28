#!/usr/bin/env python3
"""Fail-closed verifier for the Round-53 Gate-4 effective frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

import cm2_gate34_round53_effective_clock_relative_atlas_frontier_cert as cert


HERE = Path(__file__).resolve().parent
ALLOWED_TOP = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite constant: {token}")


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ValueError("unsafe manifest path")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def semantic_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    proper = result.get("numeric_SYZ_eventual_proper_return", {})
    if proper.get("numeric_n_p_upper") != 220632:
        errors.append("n_p")
    if proper.get("half_block") != 696:
        errors.append("half block")
    if Q(proper.get("a", "0")) != Q(360134800, 360493663):
        errors.append("growth a")
    if not (Q(proper.get("C_p_E", "0")) < 2**317):
        errors.append("C_p power upper")
    if proper.get("status") != (
        "CERTIFIED_NUMERIC_SYZ_PROPER_RETURN_UPPER_FOR_THE_FROZEN_PROJECT_CLASS"
    ):
        errors.append("proper status")

    gap = result.get("coupling_gap_five_row_decomposition", {})
    rows = gap.get("remaining_atomic_rows", [])
    if [row.get("id") for row in rows] != ["zeta0", "S", "R", "C", "lambda"]:
        errors.append("five row ids")
    if any(row.get("value", "missing") is not None for row in rows):
        errors.append("five row nonpromotion")
    expected_domains = [
        "0<zeta0<=1/2",
        "S is a nonnegative integer",
        "R is a nonnegative integer",
        "C>=1",
        "0<lambda<1",
    ]
    if [row.get("domain") for row in rows] != expected_domains:
        errors.append("five row domains")
    if gap.get("newly_numeric_component") != "n_p<=220632":
        errors.append("new numeric component")
    if gap.get("numeric_Delta_upper", "missing") is not None:
        errors.append("Delta overclaim")
    if gap.get("remaining_atomic_rows_sha256") != digest(rows):
        errors.append("five row digest")

    clocks = result.get("conditional_H_bump_H_out", {})
    samples = clocks.get("arithmetic_samples_not_physical_claims", {})
    bump = samples.get("H_bump_zeta_half_D_one", {})
    outer = samples.get("H_out_zeta_half_D_one", {})
    if (bump.get("minimal_safe_block_count_m"), bump.get("safe_time_H")) != (140, 280):
        errors.append("bump sample")
    if (outer.get("minimal_safe_block_count_m"), outer.get("safe_time_H")) != (104, 208):
        errors.append("outer sample")
    if clocks.get("numeric_H_bump", "missing") is not None:
        errors.append("H_bump overclaim")
    if clocks.get("numeric_H_out", "missing") is not None:
        errors.append("H_out overclaim")

    atlas = result.get("fixed_parameter_relative_crossing_atlas", {})
    steps = atlas.get("compact_open_thickening_steps", [])
    if len(steps) != 4 or [row.get("step") for row in steps] != [1, 2, 3, 4]:
        errors.append("thickening steps")
    if atlas.get("compact_open_thickening_steps_sha256") != digest(steps):
        errors.append("thickening digest")
    if atlas.get("fixed_sigma_eta_star_positive") is not True:
        errors.append("fixed adapted eta")
    if atlas.get("input_selection_metric") != "Euclidean |V|>=delta_rect":
        errors.append("Euclidean input selection")
    if "ell_*(U)/ell_*(V)" not in atlas.get("adapted_relative_width_definition", ""):
        errors.append("adapted relative width")
    if Q(
        atlas.get(
            "exact_eta_threshold_for_conditional_direct_C24_fraction",
            "0",
        )
    ) != Q(
        43008, 14285703575
    ):
        errors.append("conditional beta eta threshold")
    if Q(atlas.get("equivalent_eta_threshold_for_aggregate_hit_gap", "0")) != Q(
        43008, 14285703575
    ):
        errors.append("aggregate hit-gap eta threshold")
    if atlas.get("numeric_eta_sigma_star", "missing") is not None:
        errors.append("adapted eta overclaim")
    if atlas.get("numeric_H_cover", "missing") is not None:
        errors.append("H_cover overclaim")
    if atlas.get("numeric_beta", "missing") is not None:
        errors.append("beta overclaim")
    if atlas.get("uniform_parameter_window_eta_star_positive") != "NOT_CERTIFIED":
        errors.append("parameter overclaim")

    separators = result.get("strict_type_and_effectivity_separators", {})
    if separators.get("whole_family_hit_renamed_crossing") is not False:
        errors.append("whole family type")
    if separators.get("fixed_sigma_positive_eta_star_renamed_numeric_beta") is not False:
        errors.append("adapted eta numeric type")
    if separators.get("strict_inferable_uniform_numeric_eta_star_lower") != "0":
        errors.append("strict adapted eta lower")

    tech = result.get("latest_technology_audit", {})
    if tech.get("new_numeric_pilot_magnet_or_rectangle_atlas_found") is not False:
        errors.append("technology overclaim")
    tech_rows = tech.get("rows", [])
    if len(tech_rows) != 3 or tech.get("rows_sha256") != digest(tech_rows):
        errors.append("technology rows")

    frontier = result.get("corrected_frontier", {})
    expected_none = (
        "numeric_tilde_zeta_lower",
        "numeric_Delta_upper",
        "numeric_H_bump",
        "numeric_H_out",
        "numeric_eta_sigma_star",
        "numeric_H_cover",
        "numeric_beta",
    )
    if any(frontier.get(key, "missing") is not None for key in expected_none):
        errors.append("frontier numerical overclaim")
    if frontier.get("numeric_SYZ_n_p_upper") != 220632:
        errors.append("frontier n_p")

    strict = result.get("strict_nonpromotion", {})
    if strict.get("Gate4") != "NOT_CERTIFIED":
        errors.append("Gate4")
    if strict.get("CM2") != "NO-GO_FOR_CLAIM":
        errors.append("CM2")
    if strict.get("complete_composite_gates") != "0/5":
        errors.append("gate count")

    replay = copy.deepcopy(result)
    claimed_digest = replay.pop("internal_replay_digest", None)
    if claimed_digest != digest(replay):
        errors.append("internal replay digest")
    return errors


def manifest_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(manifest) != ALLOWED_TOP:
        errors.append("top-level keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("schema")
    cert_path = Path(cert.__file__).resolve()
    verifier_path = Path(__file__).resolve()
    if manifest.get("certificate_sha256") != sha(cert_path):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(verifier_path):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependencies")
    try:
        expected = cert.build_result()
    except Exception as exc:  # fail closed on any dependency failure
        errors.append(f"dependency replay: {exc}")
        return errors
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result root")
        return errors
    try:
        errors.extend(semantic_errors(result))
    except Exception as exc:
        errors.append(f"semantic parse: {exc}")
    if result != expected:
        errors.append("deterministic result replay")
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict projection")
    return errors


def leaf_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def get_at(value: Any, path: tuple[Any, ...]) -> Any:
    current = value
    for key in path:
        current = current[key]
    return current


def set_at(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    current = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def hostile_value(value: Any) -> Any:
    if value is None:
        return "CERTIFIED"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__MUTATED"
    raise TypeError(type(value))


def hostile_self_test(manifest: dict[str, Any], count: int = 104) -> tuple[int, int]:
    paths = list(leaf_paths(manifest["result"]))
    if len(paths) < count - 4:
        raise RuntimeError("insufficient hostile paths")
    cases: list[dict[str, Any]] = []
    for path in paths[: count - 4]:
        mutated = copy.deepcopy(manifest)
        set_at(mutated["result"], path, hostile_value(get_at(mutated["result"], path)))
        cases.append(mutated)
    for key, replacement in (
        ("schema", "wrong.schema"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "f" * 64),
        ("dependencies", {}),
    ):
        mutated = copy.deepcopy(manifest)
        mutated[key] = replacement
        cases.append(mutated)
    rejected = sum(bool(manifest_errors(case)) for case in cases)
    return rejected, len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.manifest and not args.self_test:
        print("FAIL_CLOSED: supply --manifest or --self-test")
        return 2
    path = args.manifest or cert.DEFAULT_MANIFEST
    try:
        manifest = load_manifest(path)
        errors = manifest_errors(manifest)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 2
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 2
    print("REPLAY: PASS")
    print("INTEGRITY: PASS")
    if args.self_test:
        rejected, total = hostile_self_test(manifest)
        print(f"HOSTILE_MUTATIONS: {rejected}/{total}")
        if rejected != total:
            return 2
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
