#!/usr/bin/env python3
"""Fail-closed verifier for the Round-40 C24 Growth frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round40_c24_standard_family_growth_frontier_cert as cert


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
        correction = result["round39_trace_claim_correction"]
        if correction["correction_status"] != (
            "CERTIFIED_SUPERSEDING_ONLY_THE_OVERTYPED_NECESSITY_CLAIM"
        ):
            errors.append("correction status")
        if correction["round39_nonpromotion_remains_valid"] is not True:
            errors.append("round39 nonpromotion")
        if correction["countermodel_correct_scope"] != (
            "moving inverse-branch face currents and other C0 transverse source terms"
        ):
            errors.append("countermodel scope")

        initial = result["previously_certified_initial_standard_family"]
        if initial["same_restricted_measure_and_depth_record"] is not True:
            errors.append("same measure")
        if initial["initial_boundary_Z"] != (
            "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K"
        ):
            errors.append("initial Z")
        if initial["repeated_C24_characteristic_restrictions"] != "NOT_COVERED":
            errors.append("initial scope")

        moment = result["canonical_boundary_inverse_length_moment"]
        if moment["strict_sufficient_condition"] != "alpha>1":
            errors.append("alpha condition")
        expected_examples = [("2", "4"), ("3", "8/3"), ("4", "16/7")]
        examples = moment["exact_rational_examples"]
        if len(examples) != len(expected_examples):
            errors.append("moment examples")
        for row, (alpha, multiplier) in zip(
            examples, expected_examples, strict=True
        ):
            if row["alpha"] != alpha or row["dyadic_inverse_length_multiplier"] != multiplier:
                errors.append("moment arithmetic")
        counter = moment["critical_alpha_one_countermodel"]
        if counter["inverse_length_moment"] != "infinite":
            errors.append("critical countermodel")
        rows = counter["finite_prefix_rows_at_M_1"]
        for row, prefix in zip(rows, (1, 2, 4, 8, 16), strict=True):
            if row["prefix_mass"] != str(1 - Q(1, 1 << prefix)):
                errors.append("counter mass")
            if row["prefix_inverse_length_moment"] != str(Q(prefix, 2)):
                errors.append("counter Z")
        if moment["round26_tube_alone_closes_boundary_Z"] is not False:
            errors.append("tube promotion")

        technology = result["latest_technology_geometry_match"]
        versions = technology["official_version_snapshot_checked_2026_07_19"]
        if versions["arXiv:2604.19671"] != "v2 revised 2026-05-21":
            errors.append("paper version")
        if technology["available_C24_precursors"]["physical_boundary_edges_total"] != 96:
            errors.append("C24 edges")
        if technology["direct_theorem_import_status"] != (
            "NOT_ALLOWED_WITHOUT_C24_EXPANSION_FRAGMENTATION_MATCH"
        ):
            errors.append("theorem scope")

        target = result["native_C24_standard_family_Growth_target"]
        crude = Q(137751561, 901685)
        if target["current_crude_one_step_Xi_upper"] != str(crude):
            errors.append("crude coefficient")
        if not crude > 1 or target["current_crude_one_step_is_contractive"] is not False:
            errors.append("crude contraction")
        if target["hereditary_C24_open_Growth"] != "NOT_CERTIFIED":
            errors.append("Growth promotion")
        if len(target["exact_missing_physical_payload"]) != 4:
            errors.append("missing payload")

        rate = result["retained_projective_rate_budget"]
        survival = Q(111718729, 111718750)
        weighted = Q(223437479, 223437500)
        if rate["hypothetical_norm_to_Z_root_loss_unweighted_upper"] != str(
            1 / survival
        ):
            errors.append("unweighted rate")
        if rate["hypothetical_norm_to_Z_root_loss_weighted_upper"] != str(
            1 / weighted
        ):
            errors.append("weighted rate")
        if rate["native_Growth_route_needs_projective_to_Z_trace"] is not False:
            errors.append("native trace scope")

        scope = result["strict_nonpromotion"]
        if scope["round39_C0_trace_necessity_for_positive_Z_initialization"] != (
            "SUPERSEDED"
        ):
            errors.append("supersession verdict")
        if scope["hereditary_C24_open_Growth"] != "NOT_CERTIFIED":
            errors.append("Growth verdict")
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
        ("round39_trace_claim_correction", "round39_nonpromotion_remains_valid", False),
        ("round39_trace_claim_correction", "correction_status", "UNCORRECTED"),
        (
            "previously_certified_initial_standard_family",
            "same_restricted_measure_and_depth_record",
            False,
        ),
        (
            "previously_certified_initial_standard_family",
            "initial_boundary_Z",
            "NOT_CERTIFIED",
        ),
        (
            "canonical_boundary_inverse_length_moment",
            "strict_sufficient_condition",
            "alpha>=1",
        ),
        (
            "canonical_boundary_inverse_length_moment",
            "round26_tube_alone_closes_boundary_Z",
            True,
        ),
        (
            "latest_technology_geometry_match",
            "direct_theorem_import_status",
            "CERTIFIED",
        ),
        (
            "native_C24_standard_family_Growth_target",
            "current_crude_one_step_Xi_upper",
            "1/2",
        ),
        (
            "native_C24_standard_family_Growth_target",
            "current_crude_one_step_is_contractive",
            True,
        ),
        (
            "native_C24_standard_family_Growth_target",
            "hereditary_C24_open_Growth",
            "CERTIFIED",
        ),
        (
            "retained_projective_rate_budget",
            "native_Growth_route_needs_projective_to_Z_trace",
            True,
        ),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["canonical_boundary_inverse_length_moment"][
        "exact_rational_examples"
    ][0]["dyadic_inverse_length_multiplier"] = "2"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["canonical_boundary_inverse_length_moment"][
        "critical_alpha_one_countermodel"
    ]["finite_prefix_rows_at_M_1"][3]["prefix_inverse_length_moment"] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["latest_technology_geometry_match"][
        "official_version_snapshot_checked_2026_07_19"
    ]["arXiv:2604.19671"] = "v1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["latest_technology_geometry_match"][
        "available_C24_precursors"
    ]["physical_boundary_edges_total"] = 48
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["native_C24_standard_family_Growth_target"][
        "exact_missing_physical_payload"
    ].pop()
    mutations.append(mutation)
    for key in (
        "hereditary_C24_open_Growth",
        "physical_aggregate_Z_uniform_or_weighted_bound",
        "Gate4",
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = "CERTIFIED"
        mutation["verdict"][key] = "CERTIFIED"
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"]["CM2"] = "GO"
    mutation["verdict"]["CM2"] = "GO"
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
