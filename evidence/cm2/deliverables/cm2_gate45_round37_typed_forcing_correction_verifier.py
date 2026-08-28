#!/usr/bin/env python3
"""Fail-closed verifier for the round-37 typed-forcing correction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate45_round37_typed_forcing_correction_cert as cert


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
        typed = result["typed_forcing_correction"]
        if typed["correction_status"] != "CERTIFIED_APPEND_ONLY_TYPE_CORRECTION":
            errors.append("correction status")
        if typed["round36_decomposition_remains_a_typed_physical_bound"] is not False:
            errors.append("old decomposition nonpromotion")
        if len(typed["closed_map_terms_already_absorbed_in_a"]) != 3:
            errors.append("closed-map term count")
        if "F10,F13,F16" not in typed["moving_occurrence_role"]:
            errors.append("moving occurrence type")

        arithmetic = result["C24_complement_exact_arithmetic"]
        a = Q(360134800, 360493663)
        ratio = Q(2000, 1999)
        if arithmetic["one_retained_interval_then_step_coefficient"] != str(a * ratio):
            errors.append("one-component arithmetic")
        if arithmetic["two_complement_components_then_step_coefficient"] != str(
            a * 2 * ratio
        ):
            errors.append("two-component arithmetic")
        if arithmetic["one_retained_interval_is_contractive"] is not True:
            errors.append("one-component sign")
        if arithmetic["two_complement_component_bound_is_contractive"] is not False:
            errors.append("two-component sign")
        if not a * ratio < 1 < a * 2 * ratio:
            errors.append("independent sign")

        model = result["affine_two_survivor_countermodel"]
        if model["survivor_components"] != 2:
            errors.append("model components")
        if model["new_boundary_functional"] != (
            "Z_new=sum_i mass(W_i)/length(W_i)=1+1=2"
        ):
            errors.append("model functional")
        if model["local_face_data"] != {
            "F8_transversality": "1",
            "F9_curvature": "0",
            "F10_stationary_current_density_and_derivatives": "0",
        }:
            errors.append("model local fields")
        if model["uniform_finite_mass_additive_C_exists_from_local_F8_F10"] is not False:
            errors.append("mass-additive nonimplication")
        if model["physical_CM2_impossibility_claimed"] is not False:
            errors.append("model scope")

        frontier = result["corrected_shortest_frontier"]
        if not frontier["first_missing_base_Z_input"].startswith("hereditary C24"):
            errors.append("frontier")
        scope = result["strict_nonpromotion"]
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
        ("typed_forcing_correction", "correction_status", "NOT_CERTIFIED"),
        ("typed_forcing_correction", "round36_decomposition_remains_a_typed_physical_bound", True),
        ("C24_complement_exact_arithmetic", "one_retained_interval_then_step_coefficient", "1"),
        ("C24_complement_exact_arithmetic", "two_complement_components_then_step_coefficient", "1"),
        ("C24_complement_exact_arithmetic", "two_complement_component_bound_is_contractive", True),
        ("affine_two_survivor_countermodel", "survivor_components", 1),
        ("affine_two_survivor_countermodel", "uniform_finite_mass_additive_C_exists_from_local_F8_F10", True),
        ("affine_two_survivor_countermodel", "physical_CM2_impossibility_claimed", True),
        ("corrected_shortest_frontier", "first_missing_base_Z_input", "F10 only"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["typed_forcing_correction"][
        "closed_map_terms_already_absorbed_in_a"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["affine_two_survivor_countermodel"]["local_face_data"][
        "F9_curvature"
    ] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["hereditary_C24_open_Growth"] = "CERTIFIED"
    mutation["verdict"]["hereditary_C24_open_Growth"] = "CERTIFIED"
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
