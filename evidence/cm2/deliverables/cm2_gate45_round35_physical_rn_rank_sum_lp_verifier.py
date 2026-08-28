#!/usr/bin/env python3
"""Fail-closed verifier for the physical R_n incidence-rank Lp certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate45_round35_physical_rn_rank_sum_lp_cert as cert


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


def independent_constants() -> tuple[Q, Q]:
    moment = Q(1 << 21) + Q(7, 64)
    epsilon = Q(21, 111718750)
    prefactor = Q(550000, 147)
    constant = Q(22801) * prefactor * moment * Q(250) / epsilon**3
    return moment, constant


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
        moment, constant = independent_constants()
        rank = result["physical_collision_incidence_rank"]
        if rank[
            "global_collision_SRB_integral_2^(3B_inc/2)_strict_upper"
        ] != str(moment):
            errors.append("rank moment")
        if rank["status"] != "CERTIFIED_PHYSICAL_GLOBAL_Q0_MOMENT":
            errors.append("rank status")
        charge = result["arbitrary_Rn_additive_rank_sum_charge"]
        if charge["physical_first_return_component_charge"] != "CERTIFIED":
            errors.append("physical charge")
        if charge["forward_reverse_policy"] != (
            "one common physical charge on the shared carrier, not one charge per view"
        ):
            errors.append("one charge")
        if charge["dominates_final_same_ID_q"] is not False:
            errors.append("q domination")
        level = result["levelwise_physical_L6over5_bound"]
        if level["p"] != "6/5" or level["q0"] != "3/2":
            errors.append("exponents")
        if level["p_over_q0"] != "4/5":
            errors.append("holder exponent")
        global_moment = result["global_physical_L6over5_moment"]
        if global_moment["M_rank"] != str(moment):
            errors.append("global rank moment")
        if global_moment["K_rank_exact"] != str(constant):
            errors.append("K rank")
        if global_moment["status"] != (
            "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT"
        ):
            errors.append("global moment status")
        tail = result["physical_rank_sum_weighted_tail"]
        if tail["uniform_exponential_tail"] != (
            "CERTIFIED_FOR_ADDITIVE_D1_RANK_SUM_CHARGE"
        ):
            errors.append("D1 tail")
        if tail["block_exponent"] != "1/6":
            errors.append("tail exponent")
        scope = result["strict_nonpromotion"]
        if scope["D1_tail_is_final_q_weighted_tail"] is not False:
            errors.append("tail promotion")
        if scope["final_same_ID_q"] != "NOT_CERTIFIED":
            errors.append("final q")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("physical_collision_incidence_rank", "status", "NOT_CERTIFIED"),
        (
            "physical_collision_incidence_rank",
            "global_collision_SRB_integral_2^(3B_inc/2)_strict_upper",
            "1",
        ),
        (
            "arbitrary_Rn_additive_rank_sum_charge",
            "physical_first_return_component_charge",
            "NOT_CERTIFIED",
        ),
        (
            "arbitrary_Rn_additive_rank_sum_charge",
            "forward_reverse_policy",
            "two charges",
        ),
        (
            "arbitrary_Rn_additive_rank_sum_charge",
            "dominates_final_same_ID_q",
            True,
        ),
        ("levelwise_physical_L6over5_bound", "p", "3/2"),
        ("levelwise_physical_L6over5_bound", "p_over_q0", "1"),
        ("global_physical_L6over5_moment", "K_rank_exact", "0"),
        (
            "global_physical_L6over5_moment",
            "status",
            "NOT_CERTIFIED",
        ),
        (
            "physical_rank_sum_weighted_tail",
            "uniform_exponential_tail",
            "NOT_CERTIFIED",
        ),
        ("physical_rank_sum_weighted_tail", "block_exponent", "1"),
        ("same_ID_interface_update", "final_same_ID_q", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["strict_nonpromotion"][
        "D1_tail_is_final_q_weighted_tail"
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
