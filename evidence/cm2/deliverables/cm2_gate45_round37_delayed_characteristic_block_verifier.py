#!/usr/bin/env python3
"""Fail-closed verifier for the delayed-characteristic block certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import cm2_gate45_round37_delayed_characteristic_block_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in rows:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


@lru_cache(maxsize=None)
def independent_minimum(multiplier: Q) -> tuple[int, Q, Q]:
    a = Q(360134800, 360493663)
    lower = 0
    upper = 1
    while multiplier * a**upper >= 1:
        lower = upper
        upper *= 2
    while upper - lower > 1:
        midpoint = (lower + upper) // 2
        if multiplier * a**midpoint >= 1:
            lower = midpoint
        else:
            upper = midpoint
    coefficient = multiplier * a**upper
    return upper, coefficient, coefficient / a


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if set(manifest) != {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        }:
            errors.append("top-level keys")
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        expected = cert.build_result()
        if manifest.get("result") != expected:
            errors.append("result")
        if manifest.get("verdict") != expected["strict_nonpromotion"]:
            errors.append("verdict")

        result = manifest["result"]
        theorem = result["conditional_delayed_characteristic_theorem"]
        if theorem["conditional_scalar_bridge"] != "CERTIFIED":
            errors.append("conditional theorem")
        if theorem["inverse_component_mass_used"] is not False:
            errors.append("inverse mass")

        rows = [
            (
                result["two_component_exact_threshold"],
                Q(4000, 1999),
                697,
                Q(49973, 50000),
            ),
            (
                result["generic_F7_exact_threshold"],
                Q(580000, 1999),
                5694,
                Q(24983, 25000),
            ),
        ]
        for row, multiplier, expected_steps, upper in rows:
            steps, coefficient, previous = independent_minimum(multiplier)
            if steps != expected_steps or row[
                "least_closed_steps_for_inherited_Z_contraction"
            ] != expected_steps:
                errors.append("minimum block")
            if not previous >= 1 > coefficient:
                errors.append("minimum sign")
            if row["simple_strict_coefficient_upper"] != str(upper):
                errors.append("coefficient upper")
            weight = (1 + 1 / upper) / 2
            if row["one_rational_exponential_block_weight"] != str(weight):
                errors.append("weight")
            if row["weighted_coefficient_strict_upper"] != str(weight * upper):
                errors.append("weighted upper")

        frontier = result["physical_installation_frontier"]
        if frontier["uniform_or_subexponential_C_N_for_full_Q_N"] != "NOT_CERTIFIED":
            errors.append("CN nonpromotion")
        if frontier["nonnumeric_N_open_compared_to_697_or_5694"] is not False:
            errors.append("N_open scope")
        if frontier["weak_sparse_hit_tail_is_strong_characteristic_bound"] is not False:
            errors.append("weak/strong type")
        scope = result["strict_nonpromotion"]
        if scope["physical_killed_strong_block_contraction"] != "NOT_CERTIFIED":
            errors.append("physical block nonpromotion")
        if scope["hereditary_C24_open_Growth"] != "NOT_CERTIFIED":
            errors.append("Growth nonpromotion")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_composite_gates"] != "0/5":
            errors.append("gate count")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("conditional_delayed_characteristic_theorem", "conditional_scalar_bridge", "NOT_CERTIFIED"),
        ("conditional_delayed_characteristic_theorem", "inverse_component_mass_used", True),
        ("two_component_exact_threshold", "least_closed_steps_for_inherited_Z_contraction", 696),
        ("two_component_exact_threshold", "simple_strict_coefficient_upper", "1"),
        ("two_component_exact_threshold", "one_rational_exponential_block_weight", "1"),
        ("generic_F7_exact_threshold", "least_closed_steps_for_inherited_Z_contraction", 5693),
        ("generic_F7_exact_threshold", "simple_strict_coefficient_upper", "1"),
        ("physical_installation_frontier", "uniform_or_subexponential_C_N_for_full_Q_N", "CERTIFIED"),
        ("physical_installation_frontier", "nonnumeric_N_open_compared_to_697_or_5694", True),
        ("physical_installation_frontier", "weak_sparse_hit_tail_is_strong_characteristic_bound", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "physical_killed_strong_block_contraction"
    ] = "CERTIFIED"
    mutation["verdict"]["physical_killed_strong_block_contraction"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate4"] = "CERTIFIED"
    mutation["verdict"]["Gate4"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["CM2"] = "GO"
    mutation["verdict"]["CM2"] = "GO"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["dependencies"] = {}
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
