#!/usr/bin/env python3
"""Fail-closed verifier for the round-35 arbitrary-Rn carrier registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate45_round35_arbitrary_rn_common_carrier_cert as cert


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
        registry = result["arbitrary_Rn_parent_W_Borel_registry"]
        if "depth_scope" in registry:
            errors.append("misplaced depth scope")
        if registry["registry_type"] != "standard-Borel parameterized actual curve registry":
            errors.append("registry type")
        if registry["finite_integer_curve_count_claimed"] is not False:
            errors.append("finite count")
        pair = result["common_forward_reverse_carrier_pair"]
        if pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
            errors.append("carrier pair")
        if pair["forward_and_reverse_are_two_views_not_two_charges"] is not True:
            errors.append("single charge")
        clock = result["per_carrier_numeric_recovery_clock"]
        if clock["A0"] != 301500 or clock["A1"] != 1005:
            errors.append("clock constants")
        rows = clock["sample_clock_rows"]
        if len(rows) != 7:
            errors.append("clock rows")
        for row in rows:
            depth = row["retained_mass_depth_D"]
            expected_one = 301500 + 1005 * depth
            if row["per_orientation_recovery_clock_upper"] != expected_one:
                errors.append("one clock")
            if row["two_orientation_recovery_clock_upper"] != 2 * expected_one:
                errors.append("two clock")
        scope = result["strict_nonpromotion"]
        if scope["complete_numeric_C_fw_C_rev"] != "NOT_CERTIFIED":
            errors.append("Cfw Crev")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("arbitrary_Rn_parent_W_Borel_registry", "inside_invariant_unstable_cone", False),
        ("arbitrary_Rn_parent_W_Borel_registry", "finite_integer_curve_count_claimed", True),
        ("collision_SRB_leaf_disintegration", "absolute_Jacobian", "1"),
        ("collision_SRB_leaf_disintegration", "positive_on_every_regular_rank_cell", False),
        ("common_forward_reverse_carrier_pair", "forward_and_reverse_share_identical_component_and_restriction", False),
        ("common_forward_reverse_carrier_pair", "forward_and_reverse_are_two_views_not_two_charges", False),
        ("common_forward_reverse_carrier_pair", "mu_s_A_equals_mu_s_B_equals_mu_s_I_B", False),
        ("per_carrier_numeric_recovery_clock", "same_D_on_both_views", False),
        ("per_carrier_numeric_recovery_clock", "physical_global_D_tail_or_moment", "CERTIFIED"),
        ("same_ID_interface_update", "numeric_componentwise_C_fw_C_rev_final_q", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["per_carrier_numeric_recovery_clock"]["sample_clock_rows"][3][
        "two_orientation_recovery_clock_upper"
    ] += 1
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "parameterized_schema_is_finite_component_enumeration"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["final_same_ID_q"] = "CERTIFIED"
    mutation["verdict"]["final_same_ID_q"] = "CERTIFIED"
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
