#!/usr/bin/env python3
"""Fail-closed verifier for the Round-42 numerical C24 Growth block."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round42_numeric_c24_growth_block_cert as cert


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
        holder = result["physical_branch_length_pullback"]
        if holder["holder_constant_C_len"] != "5962448355/5191":
            errors.append("holder constant")
        if holder["abs_dDelta_dr_low_region_strict_lower"] != "36337/900000":
            errors.append("Delta lower")
        if holder["low_region_component_count_upper"] != 2:
            errors.append("low components")
        if holder["numeric_length_holder"] != "CERTIFIED":
            errors.append("length holder")

        scale = result["explicit_short_curve_schedule"]
        if scale["n"] != 9148:
            errors.append("scale n")
        if scale["recurrence"] != "delta_(j+1)=(delta_j/C_len)^2":
            errors.append("scale recurrence")
        if int(scale["delta_1_exponent_2_to_n_minus_1"]) != 1 << 9147:
            errors.append("delta exponent")
        if int(scale["C_len_exponent_2_to_n_minus_2"]) != (1 << 9148) - 2:
            errors.append("holder exponent")
        if scale["all_first_9147_forward_images_remain_below_delta_1"] is not True:
            errors.append("forward images")
        if scale["delta_open_strictly_below_10^-90"] is not True:
            errors.append("delta open")

        growth = result["numerical_C24_killed_Growth"]
        gamma = cert.gamma_value(9148)
        previous = cert.gamma_value(9147)
        if not gamma < Q(1, 2):
            errors.append("gamma contraction")
        if not previous >= Q(1, 2):
            errors.append("gamma minimality")
        if growth["gamma_exact_fraction_sha256"] != cert.gamma_digest(9148):
            errors.append("gamma digest")
        if growth["previous_gamma_exact_fraction_sha256"] != cert.gamma_digest(9147):
            errors.append("previous gamma digest")
        if growth["one_step_Z_multiplier_Z1"] != "18367592526/360493663":
            errors.append("Z1")
        if growth["numeric_n_star_Z0_Z1"] != "CERTIFIED_EXACT_SYMBOLIC":
            errors.append("numeric block")
        if growth["hereditary_under_positive_C24_killing"] is not True:
            errors.append("heredity")

        aggregate = result["aggregate_canonical_Z_resolvent"]
        rho = cert.SURVIVAL**9148
        weight = (1 + 1 / rho) / 2
        if not weight > 1 or not weight * rho < 1 or not weight * gamma < Q(3, 4):
            errors.append("aggregate weight")
        if aggregate["scheduled_projective_block_N_open"] is not None:
            errors.append("N open overclaim")
        if aggregate["block_index_weight_and_resolvent"] != (
            "CERTIFIED_EXACT_SYMBOLIC"
        ):
            errors.append("aggregate resolvent")
        if aggregate["collision_time_numeric_rate"] != (
            "NOT_CERTIFIED_WITHOUT_NUMERIC_N_open"
        ):
            errors.append("collision rate scope")

        scope = result["strict_nonpromotion"]
        if scope["numeric_n_star_Z0_Z1"] != "CERTIFIED_EXACT_SYMBOLIC":
            errors.append("numeric verdict")
        if scope["numeric_N_open"] != "NOT_CERTIFIED":
            errors.append("N open verdict")
        if scope["final_same_ID_q"] != "NOT_CERTIFIED":
            errors.append("q verdict")
        if scope["Gate4"] != "NOT_CERTIFIED":
            errors.append("Gate4")
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
        ("physical_branch_length_pullback", "holder_constant_C_len", "1"),
        ("physical_branch_length_pullback", "abs_dDelta_dr_low_region_strict_lower", "0"),
        ("physical_branch_length_pullback", "low_region_component_count_upper", 1),
        ("physical_branch_length_pullback", "numeric_length_holder", "OPEN"),
        ("explicit_short_curve_schedule", "n", 9147),
        ("explicit_short_curve_schedule", "recurrence", "delta_(j+1)=delta_j"),
        ("explicit_short_curve_schedule", "delta_open_strictly_below_10^-90", False),
        ("numerical_C24_killed_Growth", "block_depth_n_star", 9147),
        ("numerical_C24_killed_Growth", "gamma_exact_fraction_sha256", "0" * 64),
        ("numerical_C24_killed_Growth", "one_step_Z_multiplier_Z1", "1"),
        ("numerical_C24_killed_Growth", "hereditary_under_positive_C24_killing", False),
        ("aggregate_canonical_Z_resolvent", "scheduled_projective_block_N_open", 1),
        ("aggregate_canonical_Z_resolvent", "collision_time_numeric_rate", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    for key, value in (
        ("numeric_N_open", "CERTIFIED"),
        ("collision_time_numeric_q", "CERTIFIED"),
        ("complete_numeric_C_fw_C_rev", "CERTIFIED"),
        ("final_same_ID_q", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
        ("Gate4", "CERTIFIED"),
        ("complete_composite_gates", "1/5"),
        ("CM2", "GO"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = value
        mutation["verdict"][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["verifier_sha256"] = "0" * 64
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
