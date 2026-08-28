#!/usr/bin/env python3
"""Fail-closed verifier for the round-34 weighted-tail interface refresh."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate45_round34_weighted_tail_interface_refresh_cert as cert


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


def independent_lthreehalves_upper() -> tuple[Q, Q]:
    rank_moment = (1 << 21) * Q(8064, 5) + Q(7, 128) * Q(9158592, 6875)
    return rank_moment, 1963 * rank_moment


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
        baseline = result["corrected_C24_tail_baseline"]
        if baseline["recovered_cone_explicit_per_block_hit_gap"] != "21/111718750":
            errors.append("hit gap")
        if baseline["uniform_unweighted_exponential_return_tail"] != "CERTIFIED":
            errors.append("unweighted tail")
        if baseline["q_weighted_exponential_return_cemetery_tail"] != "NOT_CERTIFIED":
            errors.append("weighted tail")
        interface = result["post_round31_to_round34_interface_refresh"]
        if interface["required_interface_count"] != 6 or len(interface["rows"]) != 6:
            errors.append("interface rows")
        if interface["fully_completed_interface_count"] != 0:
            errors.append("interface completion")
        if interface["partially_advanced_interface_indices"] != [2, 4]:
            errors.append("partial interfaces")
        seed = result["one_collision_endpoint_coarea_L3over2_seed"]
        rank_moment, cost_moment = independent_lthreehalves_upper()
        if seed["integral_2^(3B/2)_dm_strict_upper"] != str(rank_moment):
            errors.append("rank moment")
        if seed["integral_(151*2^B)^(3/2)_dm_strict_upper"] != str(cost_moment):
            errors.append("cost moment")
        if seed["same_measure_as_fixed_s_first_return_component_mass"] is not False:
            errors.append("measure type")
        payload = result["current_F7_to_F10_payload"]
        if payload["F7_Q2_actual_parameterized_instance_slots"] != (
            "CERTIFIED_PARAMETERIZED_228012_BASE_RULES"
        ):
            errors.append("F7 slots")
        if payload["F7_arbitrary_depth_Rn_same_ID_numeric_charge"] != "NOT_CERTIFIED":
            errors.append("F7 Rn scope")
        if payload["global_Gate5_maturity"] != "6/18_UNCHANGED":
            errors.append("maturity")
        scope = result["strict_nonpromotion"]
        if scope["q_weighted_exponential_excursion_cemetery_tail"] != "NOT_CERTIFIED":
            errors.append("q nonpromotion")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("corrected_C24_tail_baseline", "round33_missing_hit_lower_label_was_stale", False),
        ("corrected_C24_tail_baseline", "recovered_cone_explicit_per_block_hit_gap", "0"),
        ("corrected_C24_tail_baseline", "uniform_unweighted_exponential_return_tail", "NOT_CERTIFIED"),
        ("corrected_C24_tail_baseline", "q_weighted_exponential_return_cemetery_tail", "CERTIFIED"),
        ("post_round31_to_round34_interface_refresh", "fully_completed_interface_count", 1),
        ("post_round31_to_round34_interface_refresh", "recovered_cone_hit_lower_is_first_missing_interface", True),
        ("current_F7_to_F10_payload", "F7_arbitrary_depth_Rn_same_ID_numeric_charge", "CERTIFIED"),
        ("current_F7_to_F10_payload", "global_Gate5_maturity", "10/18"),
        ("one_collision_endpoint_coarea_L3over2_seed", "same_measure_as_fixed_s_first_return_component_mass", True),
        ("one_collision_endpoint_coarea_L3over2_seed", "physical_first_return_Lp_transfer_hypothesis_filled", True),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["post_round31_to_round34_interface_refresh"]["rows"][2][
        "round34_state"
    ] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["latest_technology_audit"]["new_external_theorem_promoted"] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "one_collision_coarea_L3over2_seed_is_physical_Rn_Lp_envelope"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "q_weighted_exponential_excursion_cemetery_tail"
    ] = "CERTIFIED"
    mutation["verdict"]["q_weighted_exponential_excursion_cemetery_tail"] = "CERTIFIED"
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
