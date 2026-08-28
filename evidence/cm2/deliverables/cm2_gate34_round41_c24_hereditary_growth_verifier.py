#!/usr/bin/env python3
"""Fail-closed verifier for Round-41 hereditary C24 Growth."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round41_c24_hereditary_growth_cert as cert


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
        correction = result["round40_operator_correction"]
        if correction["operator_correction_status"] != "CERTIFIED":
            errors.append("operator correction")
        if correction["normalization_needed_for_unnormalized_killed_Growth"] is not False:
            errors.append("normalization scope")

        interface = result["C24_Demers_H1_H2_match"]
        if interface["C24_H1"] != "B0=49 on each collision component":
            errors.append("H1")
        if interface["C24_implies_H2"] != (
            "1493*epsilon<=1493*epsilon^(1/2) for 0<epsilon<=1"
        ):
            errors.append("H2")
        if interface["general_hole_interface_status"] != "CERTIFIED_FOR_C24":
            errors.append("general hole match")
        if interface["unstable_time_reversed_geometry"]["piece_bound"] != 49:
            errors.append("unstable pieces")

        replay = result["exact_expansion_fragmentation_replay"]
        theta = Q(900337, 901685)
        n = replay["exact_bare_Jacobian_half_threshold"]
        if n != 9148:
            errors.append("bare threshold")
        if not 2 * (1 + 48 * n) * theta.numerator**n < theta.denominator**n:
            errors.append("threshold inequality")
        previous = n - 1
        if not 2 * (1 + 48 * previous) * theta.numerator**previous >= theta.denominator**previous:
            errors.append("threshold minimality")
        if replay["final_standard_family_block_is_9148"] is not False:
            errors.append("numeric block overclaim")

        growth = result["extra_cut_standard_family_Growth"]
        if growth["extra_cut_map_keeps_all_mass"] is not True:
            errors.append("extra-cut mass")
        if growth["chosen_reference_gamma"] != "1/2":
            errors.append("gamma")
        if growth["numeric_n_star"] is not None:
            errors.append("numeric n star")
        if growth["hat_family_Growth"] != "CERTIFIED_QUALITATIVE_UNIFORM":
            errors.append("hat Growth")

        killed = result["unnormalized_killed_subfamily_Growth"]
        if killed["same_ID_registry"] is not True:
            errors.append("same ID")
        if killed["conditional_survival_normalization_used"] is not False:
            errors.append("killed normalization")
        if killed["hereditary_C24_open_Growth"] != (
            "CERTIFIED_QUALITATIVE_UNIFORM"
        ):
            errors.append("killed Growth")

        aggregate = result["aggregate_canonical_Z_resolvent"]
        if aggregate["cellwise_2_to_retained_depth_moment_used"] is not False:
            errors.append("cellwise moment")
        if aggregate["canonical_trace_from_projective_norm_used"] is not False:
            errors.append("projective trace")
        if aggregate["physical_aggregate_Z_weighted_tail"] != (
            "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES"
        ):
            errors.append("aggregate tail")
        if aggregate["numeric_w_Z"] is not None:
            errors.append("numeric weight")

        scope = result["strict_nonpromotion"]
        if scope["numeric_n_star_Z0_Z1"] != "NOT_CERTIFIED":
            errors.append("numeric Growth scope")
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
        ("round40_operator_correction", "operator_correction_status", "OPEN"),
        ("round40_operator_correction", "normalization_needed_for_unnormalized_killed_Growth", True),
        ("C24_Demers_H1_H2_match", "C24_H1", "B0=3"),
        ("C24_Demers_H1_H2_match", "C24_implies_H2", "NOT_PROVED"),
        ("C24_Demers_H1_H2_match", "general_hole_interface_status", "NOT_CERTIFIED"),
        ("exact_expansion_fragmentation_replay", "exact_bare_Jacobian_half_threshold", 9147),
        ("exact_expansion_fragmentation_replay", "final_standard_family_block_is_9148", True),
        ("extra_cut_standard_family_Growth", "extra_cut_map_keeps_all_mass", False),
        ("extra_cut_standard_family_Growth", "numeric_n_star", 9148),
        ("extra_cut_standard_family_Growth", "hat_family_Growth", "NOT_CERTIFIED"),
        ("unnormalized_killed_subfamily_Growth", "same_ID_registry", False),
        ("unnormalized_killed_subfamily_Growth", "conditional_survival_normalization_used", True),
        ("unnormalized_killed_subfamily_Growth", "hereditary_C24_open_Growth", "NOT_CERTIFIED"),
        ("aggregate_canonical_Z_resolvent", "cellwise_2_to_retained_depth_moment_used", True),
        ("aggregate_canonical_Z_resolvent", "canonical_trace_from_projective_norm_used", True),
        ("aggregate_canonical_Z_resolvent", "numeric_w_Z", "2"),
        ("aggregate_canonical_Z_resolvent", "physical_aggregate_Z_weighted_tail", "NOT_CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["C24_Demers_H1_H2_match"]["unstable_time_reversed_geometry"]["piece_bound"] = 97
    mutations.append(mutation)
    for key, value in (
        ("numeric_n_star_Z0_Z1", "CERTIFIED"),
        ("complete_numeric_C_fw_C_rev", "CERTIFIED"),
        ("final_same_ID_q", "CERTIFIED"),
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
