#!/usr/bin/env python3
"""Fail-closed verifier for the Round-43 Eulerian/Duhamel frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round43_duhamel_eulerian_charge_frontier_cert as cert


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
        generator = result["one_step_area_eulerian_generator"]
        bounds = generator["cross_colour_pointwise_bounds"]
        if bounds["abs_X_r"] != "<=75/(4*c_target)":
            errors.append("Xr")
        if bounds["abs_X_p"] != "<=25/4":
            errors.append("Xp")
        if bounds["l1_generator"] != "abs_X_r+abs_X_p<=25*2^B":
            errors.append("X bound")
        if generator["generator_rank_exponent"] != 1:
            errors.append("rank exponent")
        if generator["cubic_second_jet_rank_exponent_used"] is not False:
            errors.append("cubic overclaim")
        moment = generator["physical_one_time_L3over2"]
        if Q(moment["strict_upper"]) != Q(16777216875, 64):
            errors.append("L3/2")
        if moment["status"] != "CERTIFIED":
            errors.append("one-time status")

        duhamel = result["arbitrary_path_Duhamel_current"]
        if duhamel["identity_status"] != (
            "CERTIFIED_ALGEBRAIC_ARBITRARY_FINITE_PATH"
        ):
            errors.append("Duhamel")
        if duhamel["same_ID_prefix_suffix_order_preserved"] is not True:
            errors.append("same ID")
        if duhamel["full_composed_second_parameter_jet_differentiated"] is not False:
            errors.append("second jet")
        if "sum_{j=1}^n" not in duhamel["finite_path_formula"]:
            errors.append("Duhamel sum")

        charge = result["physical_D1_dominated_eulerian_charge"]
        if charge["pointwise_same_ID_identity"] != (
            "c_X,n=(25/151)*c_D1,n<c_D1,n"
        ):
            errors.append("D1 dominance")
        if charge["global_L6over5_moment"]["K_rank"] != str(cert.K_RANK):
            errors.append("K rank")
        if charge["global_L6over5_moment"]["N_open_numeric"] is not False:
            errors.append("N_open scope")
        if charge["weighted_tail"]["inherited_block_exponent"] != "1/6":
            errors.append("tail exponent")
        if charge["arbitrary_Rn_same_ID_insertion_amplitude_ledger"] != "CERTIFIED":
            errors.append("amplitude ledger")

        frontier = result["F13_F16_operator_field_frontier"]
        if frontier["depth_one_occurrence_current"]["oriented_traces"] != 128:
            errors.append("traces")
        if frontier["arbitrary_Rn_F13_insertion_amplitude_charge"] != "CERTIFIED":
            errors.append("F13 amplitude")
        if frontier["arbitrary_Rn_F13_two_trace_operator_field"] != (
            "NOT_CERTIFIED"
        ):
            errors.append("F13 overclaim")
        if frontier["arbitrary_Rn_F16_pointwise_affine_flux_envelope"] != (
            "CERTIFIED"
        ):
            errors.append("F16 envelope")
        if frontier["arbitrary_Rn_F16_complete_operator_cost"] != (
            "NOT_CERTIFIED"
        ):
            errors.append("F16 overclaim")

        scope = result["strict_nonpromotion"]
        if scope["arbitrary_Rn_Duhamel_insertion_charge_ledger"] != "CERTIFIED":
            errors.append("ledger verdict")
        if scope["F13"] != "NOT_CERTIFIED":
            errors.append("F13 verdict")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
        if scope["Gate5"] != "NOT_CERTIFIED":
            errors.append("Gate5")
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
        ("one_step_area_eulerian_generator", "generator_rank_exponent", 3),
        ("one_step_area_eulerian_generator", "cubic_second_jet_rank_exponent_used", True),
        ("arbitrary_path_Duhamel_current", "identity_status", "OPEN"),
        ("arbitrary_path_Duhamel_current", "same_ID_prefix_suffix_order_preserved", False),
        ("arbitrary_path_Duhamel_current", "full_composed_second_parameter_jet_differentiated", True),
        ("physical_D1_dominated_eulerian_charge", "pointwise_same_ID_identity", "false"),
        ("physical_D1_dominated_eulerian_charge", "arbitrary_Rn_same_ID_insertion_amplitude_ledger", "OPEN"),
        ("F13_F16_operator_field_frontier", "arbitrary_Rn_F13_insertion_amplitude_charge", "OPEN"),
        ("F13_F16_operator_field_frontier", "arbitrary_Rn_F13_two_trace_operator_field", "CERTIFIED"),
        ("F13_F16_operator_field_frontier", "arbitrary_Rn_F16_complete_operator_cost", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["one_step_area_eulerian_generator"][
        "cross_colour_pointwise_bounds"
    ]["l1_generator"] = "<=2^(3B)"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["one_step_area_eulerian_generator"][
        "physical_one_time_L3over2"
    ]["strict_upper"] = "0"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["physical_D1_dominated_eulerian_charge"][
        "global_L6over5_moment"
    ]["N_open_numeric"] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["F13_F16_operator_field_frontier"][
        "depth_one_occurrence_current"
    ]["oriented_traces"] = 0
    mutations.append(mutation)
    for key, value in (
        ("arbitrary_Rn_Duhamel_insertion_charge_ledger", "OPEN"),
        ("arbitrary_Rn_F13_two_trace_operator_field", "CERTIFIED"),
        ("arbitrary_Rn_F16_complete_operator_cost", "CERTIFIED"),
        ("complete_all_face_F10_field", "CERTIFIED"),
        ("F12", "CERTIFIED"),
        ("F13", "CERTIFIED"),
        ("F14_through_F18", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
        ("dynamic_MT_DQ", "CERTIFIED"),
        ("Gate5_maturity", "8/18"),
        ("complete_18_field_operator_block_count", 1),
        ("Gate5", "CERTIFIED"),
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
