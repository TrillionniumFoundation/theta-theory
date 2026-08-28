#!/usr/bin/env python3
"""Fail-closed verifier for the Round-54 Gate-4 numerical frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

import cm2_gate34_round54_numeric_growth_gap_rate_interval_atlas_frontier_cert as cert


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
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


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
    growth = result.get("new_numeric_growth_lemma", {})
    c_len = Q(5962448355, 5191)
    c_e = c_len**2
    a = Q(360134800, 360493663)
    density = Q(2000, 1999)
    delta = Q(1, 10**90)
    additive = 2 / delta
    endpoint_conversion = Q(27, 5) * Q(141, 2) * density
    euclidean_length_coefficient = (
        Q(141, 2) / delta
        + Q(141, 4) * additive / (1 - a)
    )
    c_gr = endpoint_conversion * euclidean_length_coefficient
    if Q(growth.get("C_len", "0")) != c_len:
        errors.append("C_len")
    if Q(growth.get("safe_frozen_fixed_map_C_e", "0")) != c_e or not c_e < 2**41:
        errors.append("C_e")
    if Q(growth.get("Growth_vartheta", "0")) != a:
        errors.append("Growth vartheta")
    if Q(growth.get("numeric_C_gr", "0")) != c_gr:
        errors.append("C_gr")
    if Q(growth.get("Euclidean_endpoint_conversion_prefactor", "0")) != endpoint_conversion:
        errors.append("endpoint conversion")
    if Q(growth.get("Euclidean_length_coefficient", "0")) != euclidean_length_coefficient:
        errors.append("length coefficient")
    rows = growth.get("proof_rows", [])
    if len(rows) != 5 or growth.get("proof_rows_sha256") != digest(rows):
        errors.append("Growth proof rows")
    if growth.get("status") != "CERTIFIED_NUMERIC_FROZEN_FIXED_MAP_GROWTH_LEMMA":
        errors.append("Growth status")
    if "not the full moving-configuration SYZ class" not in growth.get("scope", ""):
        errors.append("Growth scope")

    gap = result.get("conditional_numeric_gap_rate_candidate", {})
    lam = Q(9997, 10000)
    old = Q(2499, 2500)
    expansion = Q(180337, 144000)
    if gap.get("Growth_half_life") != 696:
        errors.append("half life")
    if gap.get("recovery_rank_slope") != 697:
        errors.append("rank slope")
    if Q(gap.get("conditional_candidate_lambda_bar", "0")) != lam:
        errors.append("conditional lambda candidate")
    if gap.get("official_Euclidean_SYZ_recurrence") != (
        "Z_n^E/mass<=(C_p^E/2)*(1+a^n*Z_0^E/mass)"
    ):
        errors.append("Euclidean SYZ recurrence")
    if gap.get("Euclidean_properness_test") != "a^N*(Z_0^E/mass)<1":
        errors.append("Euclidean properness test")
    if "apply the pinned Euclidean recurrence to checkrho|V" not in gap.get(
        "conditional_recovery_derivation", ""
    ):
        errors.append("Euclidean recurrence use")
    if gap.get("same_magnet_checkrho_density_join") != "NOT_CERTIFIED":
        errors.append("same-magnet density join overclaim")
    if gap.get("density_recovery_is_rank_independent_intercept") is not True:
        errors.append("density intercept typing")
    if not lam**697 > 1 / expansion:
        errors.append("lambda exact check")
    if not old**697 <= 1 / expansion:
        errors.append("predecessor check")
    if gap.get("official_lambda_equality_claimed") is not False:
        errors.append("official lambda overclaim")
    if gap.get("safe_replacement_rate_row_status") != (
        "CERTIFIED_CONDITIONAL_ON_SAME_MAGNET_DENSITY_JOIN"
    ):
        errors.append("safe rate status")
    if gap.get("official_five_row_lambda_status") != "NOT_CERTIFIED":
        errors.append("official lambda status")
    if gap.get("numeric_C_bar", "missing") is not None:
        errors.append("C bar overclaim")
    if gap.get("numeric_r", "missing") is not None:
        errors.append("r overclaim")
    sample = gap.get("arithmetic_sample_not_physical", {})
    expected_sample = cert.dyadic_gap_builder(1, 1, Q(1), Q(1, 4), 0, 0)
    if sample != expected_sample:
        errors.append("gap sample")

    atom = result.get("gap_prefactor_atomisation", {})
    h = Q(20, 3807)
    k_g = (
        density
        * (h + Q(11, 10))
        * c_gr
        * 69
        / (1 - 1 / expansion)
    )
    if Q(atom.get("fully_numeric_multiplier_K_g", "0")) != k_g:
        errors.append("K_g")
    if Q(
        atom.get("maximum_homogeneous_unstable_curve_length_L0_strict_upper", "0")
    ) != 68:
        errors.append("L0 upper")
    if atom.get("conditional_prefactor") != "C_g_double_prime<=K_g*T":
        errors.append("conditional prefactor")
    missing = atom.get("remaining_rows", [])
    if [row.get("id") for row in missing] != [
        "tildeC_stable_length",
        "c_g_rank_growth",
        "W_tilde_length",
        "same_magnet_density_join",
        "top_excess_recovery",
    ]:
        errors.append("prefactor rows")
    if any(row.get("value", "missing") is not None for row in missing):
        errors.append("prefactor row overclaim")
    if atom.get("remaining_rows_sha256") != digest(missing):
        errors.append("prefactor digest")
    if atom.get("numeric_C_g_double_prime", "missing") is not None:
        errors.append("C_gpp overclaim")

    atlas = result.get("rational_parameter_interval_atlas_builder", {})
    required = atlas.get("required_rows", [])
    if len(required) != 9 or atlas.get("required_rows_sha256") != digest(required):
        errors.append("atlas rows")
    if atlas.get("physical_rows_materialized") != 0:
        errors.append("atlas physical rows")
    if atlas.get("parameter_interval_rows_materialized") != 0:
        errors.append("atlas interval rows")
    if atlas.get("mixed_metric_rows_accepted") is not False:
        errors.append("mixed metric")
    if "20/3807" not in atlas.get("Euclidean_mode_formula", ""):
        errors.append("metric conversion")
    if "per-step derivative/distortion upper" not in atlas.get("J_j_semantics", ""):
        errors.append("J per-step semantics")
    if not any("per-step derivative/distortion upper J_j" in row for row in required):
        errors.append("J per-step row")
    if Q(atlas.get("safe_target", "0")) != Q(43008, 14285703575):
        errors.append("eta target")
    samples = atlas.get("arithmetic_samples_not_physical", {})
    threshold = Q(43008, 14285703575)
    if Q(samples.get("adapted_exact_threshold", "0")) != threshold:
        errors.append("adapted sample")
    if Q(samples.get("Euclidean_exact_threshold_after_conversion", "0")) != threshold:
        errors.append("Euclidean sample")
    for key in ("numeric_uniform_eta_sigma_star", "numeric_H_cover", "numeric_beta"):
        if atlas.get(key, "missing") is not None:
            errors.append(f"atlas overclaim {key}")

    tech = result.get("latest_technology_audit", {})
    tech_rows = tech.get("rows", [])
    if len(tech_rows) != 4 or tech.get("rows_sha256") != digest(tech_rows):
        errors.append("technology rows")
    if tech.get("new_direct_numeric_magnet_or_interval_atlas_theorem_found") is not False:
        errors.append("technology overclaim")
    hashes = tech.get("source_hashes", {})
    if hashes != cert.ARXIV_SOURCE_HASHES:
        errors.append("source hash scopes")

    frontier = result.get("corrected_round53_five_row_frontier", {})
    for key in (
        "zeta0",
        "S",
        "R",
        "C",
        "lambda",
        "numeric_Delta_upper",
        "numeric_H_bump",
        "numeric_H_out",
        "numeric_eta_sigma_star",
        "numeric_H_cover",
        "numeric_beta",
    ):
        if frontier.get(key, "missing") is not None:
            errors.append(f"frontier overclaim {key}")
    if Q(
        frontier.get(
            "lambda_conditional_candidate_if_same_magnet_density_join", "0"
        )
    ) != lam:
        errors.append("frontier conditional lambda candidate")

    separators = result.get("strict_type_separators", {})
    if any(value is not False for value in separators.values()):
        errors.append("type separators")
    strict = result.get("strict_nonpromotion", {})
    if strict.get("numeric_safe_gap_rate_base") != "NOT_CERTIFIED":
        errors.append("rate verdict")
    if strict.get("conditional_gap_rate_candidate") != (
        "CERTIFIED_CONDITIONAL_ON_SAME_MAGNET_DENSITY_JOIN"
    ):
        errors.append("conditional rate verdict")
    if strict.get("same_magnet_density_join") != "NOT_CERTIFIED":
        errors.append("density join verdict")
    if strict.get("Gate4") != "NOT_CERTIFIED":
        errors.append("Gate4")
    if strict.get("complete_composite_gates") != "0/5":
        errors.append("gate count")
    if strict.get("CM2") != "NO-GO_FOR_CLAIM":
        errors.append("CM2")

    replay = copy.deepcopy(result)
    claimed = replay.pop("internal_replay_digest", None)
    if claimed != digest(replay):
        errors.append("internal replay digest")
    return errors


def manifest_errors(
    manifest: dict[str, Any], expected: dict[str, Any] | None = None
) -> list[str]:
    errors: list[str] = []
    if set(manifest) != ALLOWED_TOP:
        errors.append("top-level keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependencies")
    if expected is None:
        try:
            expected = cert.build_result()
        except Exception as exc:
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
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "__MUTATED"
    raise TypeError(type(value))


def self_test(manifest: dict[str, Any]) -> tuple[bool, int]:
    expected = cert.build_result()
    count = 0
    for path in leaf_paths(manifest):
        mutated = copy.deepcopy(manifest)
        set_at(mutated, path, hostile_value(get_at(mutated, path)))
        if not manifest_errors(mutated, expected):
            print(f"HOSTILE ACCEPTED: {path}")
            return False, count
        count += 1

    # Parser and top-level hostile cases.
    duplicate = '{"schema":"x","schema":"y"}'
    try:
        json.loads(duplicate, object_pairs_hook=strict_object)
    except ValueError:
        count += 1
    else:
        return False, count
    try:
        json.loads('{"x":NaN}', parse_constant=reject_constant)
    except ValueError:
        count += 1
    else:
        return False, count
    unknown = copy.deepcopy(manifest)
    unknown["unknown"] = 1
    if manifest_errors(unknown, expected):
        count += 1
    else:
        return False, count
    return True, count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--self-test", type=Path)
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    if args.verify is not None:
        try:
            value = load_manifest(args.verify)
            errors = manifest_errors(value)
        except Exception as exc:
            print(f"VERIFY FAIL: {exc}")
            return 1
        if errors:
            print("VERIFY FAIL")
            for error in errors:
                print(f"- {error}")
            return 1
        print("VERIFY PASS")
        return 0
    if args.self_test is not None:
        try:
            value = load_manifest(args.self_test)
            if manifest_errors(value):
                print("SELF-TEST FAIL: baseline")
                return 1
            ok, count = self_test(value)
        except Exception as exc:
            print(f"SELF-TEST FAIL: {exc}")
            return 1
        if not ok:
            print("SELF-TEST FAIL")
            return 1
        print(f"SELF-TEST PASS: {count}/{count} hostile mutations rejected")
        return 0
    if args.reemit is not None:
        cert.write_manifest(args.reemit)
        print(f"REEMIT {args.reemit}")
        return 0
    print("ROUND54_GATE4_VERIFIER: FAIL-CLOSED")
    print("Use --verify, --self-test, or --reemit")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
