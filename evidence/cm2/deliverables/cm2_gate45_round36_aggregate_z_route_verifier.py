#!/usr/bin/env python3
"""Fail-closed verifier for the round-36 aggregate-Z route certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate45_round36_aggregate_z_route_cert as cert


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


def independent_constants() -> tuple[Q, Q, Q, Q]:
    a = Q(360134800, 360493663)
    margin = 1 - a
    resolvent = 1 / margin
    weight = Q(a.denominator + a.numerator, 2 * a.numerator)
    return margin, resolvent, weight, weight * a


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
        recurrence = result["aggregate_Z_new_face_recurrence"]
        margin, resolvent, weight, weighted_ratio = independent_constants()
        if recurrence["contraction_margin"] != str(margin):
            errors.append("margin")
        if recurrence["exact_resolvent"] != str(resolvent):
            errors.append("resolvent")
        if recurrence["one_explicit_growth_compatible_weight"] != str(weight):
            errors.append("weight")
        if recurrence["weighted_growth_ratio"] != str(weighted_ratio):
            errors.append("weighted ratio")
        if recurrence["inverse_component_mass_used"] is not False:
            errors.append("inverse mass")
        if recurrence["abstract_aggregate_Z_transfer"] != "CERTIFIED":
            errors.append("aggregate transfer")

        interface = result["same_ID_new_face_injection_interface"]
        if interface["available"]["all_five_face_kind_F9_rank_path_C2"] != (
            "CERTIFIED_PARAMETERIZED"
        ):
            errors.append("F9 interface")
        if interface["uniform_J_upper"] != "NOT_CERTIFIED":
            errors.append("J nonpromotion")
        if len(interface["missing"]) != 9:
            errors.append("missing interface count")

        model = result["retained_depth_marginal_countermodel"]
        if model["exact_tail"] != "P(B>b)=4^-b for every integer b>=14":
            errors.append("countermodel tail")
        if model["perfect_time_correlation"] != "B_i=B for every i>=1":
            errors.append("correlation")
        if model["claims_physical_rank_process_has_perfect_correlation"] is not False:
            errors.append("countermodel scope")
        if "beta*n>=2" not in model["failure"]:
            errors.append("countermodel threshold")

        decision = result["round36_route_decision"]
        if not decision["aggregate_Z_route"].startswith("SELECTED_PRIMARY"):
            errors.append("route")
        if decision["naive_cellwise_F7_is_contraction"] is not False:
            errors.append("naive contraction")
        scope = result["strict_nonpromotion"]
        if scope["physical_aggregate_Z_uniform_bound"] != "NOT_CERTIFIED":
            errors.append("aggregate nonpromotion")
        if scope["D1_tail_dominates_image_recut_product"] is not False:
            errors.append("D1 nonpromotion")
        if scope["Gate5_maturity"] != "7/18":
            errors.append("maturity")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("aggregate_Z_new_face_recurrence", "a", "1"),
        ("aggregate_Z_new_face_recurrence", "exact_resolvent", "1"),
        ("aggregate_Z_new_face_recurrence", "inverse_component_mass_used", True),
        ("same_ID_new_face_injection_interface", "uniform_J_upper", "CERTIFIED"),
        ("retained_depth_marginal_countermodel", "exact_tail", "P(B>b)=0"),
        ("retained_depth_marginal_countermodel", "perfect_time_correlation", "independent"),
        ("round36_route_decision", "naive_cellwise_F7_is_contraction", True),
        ("round36_route_decision", "aggregate_Z_route", "REJECTED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["same_ID_new_face_injection_interface"]["missing"].pop(
        "all_pullback_F10_coarea_density_regular_bound"
    )
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["retained_depth_marginal_countermodel"][
        "claims_physical_rank_process_has_perfect_correlation"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "physical_aggregate_Z_uniform_bound"
    ] = "CERTIFIED"
    mutation["verdict"]["physical_aggregate_Z_uniform_bound"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "D1_tail_dominates_image_recut_product"
    ] = True
    mutation["verdict"]["D1_tail_dominates_image_recut_product"] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["Gate4"] = "CERTIFIED"
    mutation["verdict"]["Gate4"] = "CERTIFIED"
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
