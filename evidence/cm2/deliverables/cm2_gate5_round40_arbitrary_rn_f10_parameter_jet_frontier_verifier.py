#!/usr/bin/env python3
"""Fail-closed verifier for the Round-40 arbitrary-R_n F10 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round40_arbitrary_rn_f10_parameter_jet_frontier_cert as cert


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


def replay(ranks: list[int]) -> list[dict[str, Any]]:
    spatial_first = 1
    spatial_second = 0
    parameter_first = 0
    mixed = 0
    parameter_second = 0
    rows: list[dict[str, Any]] = []
    for depth, rank in enumerate(ranks, start=1):
        first = 150 * (1 << rank)
        second = 42672 * (1 << (3 * rank))
        synthetic_u = 1 << rank
        synthetic_v = 3 * (1 << (2 * rank))
        synthetic_w = 5 * (1 << (3 * rank))
        old_d = spatial_first
        old_h = spatial_second
        old_p = parameter_first
        old_q = mixed
        old_s = parameter_second
        spatial_first = first * old_d
        spatial_second = second * old_d**2 + first * old_h
        parameter_first = synthetic_u + first * old_p
        mixed = synthetic_v * old_d + second * old_p * old_d + first * old_q
        parameter_second = (
            synthetic_w
            + 2 * synthetic_v * old_p
            + second * old_p**2
            + first * old_s
        )
        rows.append(
            {
                "depth": depth,
                "B": rank,
                "synthetic_U": str(synthetic_u),
                "synthetic_V": str(synthetic_v),
                "synthetic_W": str(synthetic_w),
                "D": str(spatial_first),
                "H": str(spatial_second),
                "P": str(parameter_first),
                "Q": str(mixed),
                "S": str(parameter_second),
            }
        )
    return rows


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
        inventory = result["one_step_parameter_jet_inventory"]
        for key in (
            "physical_rank_indexed_U_B_materialized",
            "physical_rank_indexed_V_B_materialized",
            "physical_rank_indexed_W_B_materialized",
        ):
            if inventory[key] is not False:
                errors.append(key)
        if inventory["known_spatial_rank_envelopes"]["A_i"] != (
            "||D_x T_i||<=150*2^B_i"
        ):
            errors.append("A envelope")
        if inventory["known_spatial_rank_envelopes"]["B_i"] != (
            "||D_x^2 T_i||<=42672*2^(3B_i)"
        ):
            errors.append("B envelope")

        recurrence = result["arbitrary_path_mixed_jet_recurrence"]
        expected_recurrence = [
            "D_i<=A_i*D_(i-1)",
            "H_i<=B_i*D_(i-1)^2+A_i*H_(i-1)",
            "P_i<=U_i+A_i*P_(i-1)",
            "Q_i<=V_i*D_(i-1)+B_i*P_(i-1)*D_(i-1)+A_i*Q_(i-1)",
            "S_i<=W_i+2*V_i*P_(i-1)+B_i*P_(i-1)^2+A_i*S_(i-1)",
        ]
        if recurrence["exact_safe_recurrence"] != expected_recurrence:
            errors.append("recurrence")
        if recurrence["finite_for_every_fixed_finite_path_with_finite_step_jets"] is not True:
            errors.append("finite recurrence")
        if recurrence["recurrence_status"] != "CERTIFIED_BY_SECOND_ORDER_CHAIN_RULE":
            errors.append("recurrence status")

        synthetic = result["synthetic_integer_replay"]
        if synthetic["synthetic_values_are_physical_bounds"] is not False:
            errors.append("synthetic scope")
        expected_paths = [[14], [14, 15], [14, 16, 18]]
        blocks = synthetic["replay_blocks"]
        if len(blocks) != len(expected_paths):
            errors.append("replay block count")
        for block, ranks in zip(blocks, expected_paths, strict=True):
            rows = replay(ranks)
            if block["rank_path"] != ranks:
                errors.append("rank path")
            if block["rows"] != rows:
                errors.append("replay rows")
            if block["rows_sha256"] != cert.digest(rows):
                errors.append("replay digest")

        audit = result["pulled_back_level_F10_type_audit"]
        if len(audit["second_derivatives_needed_by_F10"]) != 3:
            errors.append("second derivative inventory")
        if audit["base_face_parameter_jets_required"] != ["G_s", "G_xs", "G_ss"]:
            errors.append("base jets")
        if audit["chain_rule_type_audit_status"] != "CERTIFIED":
            errors.append("type audit")

        local = result["compact_germ_constructive_status"]
        if local["new_parameter_jet_recurrence_can_be_evaluated_on_each_compact_germ"] is not True:
            errors.append("local recurrence")
        if local["materialized_arbitrary_Rn_U_V_W_rows"] != 0:
            errors.append("UVWs materialized")
        if local["materialized_arbitrary_Rn_global_F10_values"] != 0:
            errors.append("F10 materialized")
        if local["uniform_joint_parameter_component_atlas"] != "NOT_CERTIFIED":
            errors.append("joint atlas")

        frontier = result["global_physical_installation_frontier"]
        if frontier["seed_exponent_propagates_through_arbitrary_paths_automatically"] is not False:
            errors.append("seed propagation")
        if len(frontier["first_missing_numeric_payload"]) != 4:
            errors.append("missing payload")
        if frontier["arbitrary_Rn_all_face_F10"] != "NOT_CERTIFIED":
            errors.append("F10 promotion")

        scope = result["strict_nonpromotion"]
        if scope["arbitrary_path_mixed_parameter_jet_recurrence"] != "CERTIFIED":
            errors.append("recurrence verdict")
        if scope["rank_indexed_physical_U_V_W"] != "NOT_CERTIFIED":
            errors.append("UVW verdict")
        if scope["arbitrary_Rn_pullback_F10_field"] != "NOT_CERTIFIED":
            errors.append("Rn verdict")
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
        (
            "one_step_parameter_jet_inventory",
            "physical_rank_indexed_U_B_materialized",
            True,
        ),
        (
            "one_step_parameter_jet_inventory",
            "physical_rank_indexed_V_B_materialized",
            True,
        ),
        (
            "one_step_parameter_jet_inventory",
            "physical_rank_indexed_W_B_materialized",
            True,
        ),
        (
            "arbitrary_path_mixed_jet_recurrence",
            "finite_for_every_fixed_finite_path_with_finite_step_jets",
            False,
        ),
        (
            "arbitrary_path_mixed_jet_recurrence",
            "recurrence_status",
            "NOT_CERTIFIED",
        ),
        (
            "synthetic_integer_replay",
            "synthetic_values_are_physical_bounds",
            True,
        ),
        (
            "pulled_back_level_F10_type_audit",
            "chain_rule_type_audit_status",
            "NOT_CERTIFIED",
        ),
        (
            "compact_germ_constructive_status",
            "materialized_arbitrary_Rn_U_V_W_rows",
            1,
        ),
        (
            "compact_germ_constructive_status",
            "materialized_arbitrary_Rn_global_F10_values",
            1,
        ),
        (
            "compact_germ_constructive_status",
            "uniform_joint_parameter_component_atlas",
            "CERTIFIED",
        ),
        (
            "global_physical_installation_frontier",
            "seed_exponent_propagates_through_arbitrary_paths_automatically",
            True,
        ),
        (
            "global_physical_installation_frontier",
            "arbitrary_Rn_all_face_F10",
            "CERTIFIED",
        ),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["arbitrary_path_mixed_jet_recurrence"][
        "exact_safe_recurrence"
    ][3] = "Q_i<=A_i*Q_(i-1)"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["synthetic_integer_replay"]["replay_blocks"][1]["rows"][1][
        "Q"
    ] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["pulled_back_level_F10_type_audit"][
        "base_face_parameter_jets_required"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["global_physical_installation_frontier"][
        "first_missing_numeric_payload"
    ].pop()
    mutations.append(mutation)
    for key in (
        "rank_indexed_physical_U_V_W",
        "arbitrary_Rn_pullback_F10_field",
        "complete_all_face_F10_field",
        "Gate5",
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
