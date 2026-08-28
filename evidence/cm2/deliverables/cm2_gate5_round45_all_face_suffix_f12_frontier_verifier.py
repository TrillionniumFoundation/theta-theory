#!/usr/bin/env python3
"""Fail-closed verifier for the Round-45 F12/F16 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round45_all_face_suffix_f12_frontier_cert as cert


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
        f12 = result["all_face_arbitrary_suffix_F12"]
        if f12["one_step_derivative_envelope"] != "L(B)=150*2^B, B>=14":
            errors.append("derivative envelope")
        if f12["suffix_derivative"] != "D_suffix=product_i L(B_i)":
            errors.append("suffix derivative")
        if len(f12["face_rows"]) != 5:
            errors.append("face rows")
        if not f12["all_five_physical_face_grammars_covered"]:
            errors.append("five face F12")
        if f12["global_rank_path_moment_required_for_F12_field"] is not False:
            errors.append("F12 moment typing")
        samples = f12["sample_replays"]
        if samples != [
            cert.suffix_c1_bound(()),
            cert.suffix_c1_bound((14,)),
            cert.suffix_c1_bound((14, 15)),
            cert.suffix_c1_bound((14, 16, 18)),
            cert.suffix_c1_bound((20, 14, 17, 15)),
        ]:
            errors.append("F12 samples")
        if f12["sample_replays_sha256"] != cert.digest(samples):
            errors.append("F12 sample digest")

        f16 = result["F16_frontier"]
        empty = f16["empty_suffix_subspace"]
        if empty["F12_multiplier"] != "1":
            errors.append("empty F12")
        if empty["physical_L6over5_moment"] != "CERTIFIED_BY_F13_DOMINATION":
            errors.append("empty F16 moment")
        if f16["nonempty_suffix_global_physical_moment"] != "NOT_CERTIFIED":
            errors.append("nonempty F16 overclaim")
        if f16["all_face_standard_family_strong_F16"] != "NOT_CERTIFIED":
            errors.append("strong F16 overclaim")
        counter = f16["moment_nonimplication"]
        if "not a physical billiard counterexample" not in counter["purpose"]:
            errors.append("countermodel scope")
        if counter["probability_sums_to_one"] is not True:
            errors.append("countermodel law")
        if counter["finite_available_moment_value"] != 33292288:
            errors.append("countermodel finite moment")
        if counter["divergent_required_product_moment"] != (
            "E[2^(2B)]=infinity"
        ):
            errors.append("countermodel divergence")

        maturity = result["Gate5_maturity_update"]
        if maturity != {
            "previous_global_maturity": "8/18",
            "newly_completed_parameterized_field": "F12 C1_face_trace_pullback_bound",
            "current_global_maturity": "9/18",
            "complete_18_field_operator_block_count": 0,
        }:
            errors.append("maturity")

        scope = result["strict_nonpromotion"]
        expected_scope = {
            "all_five_face_arbitrary_suffix_F12": "CERTIFIED",
            "terminal_empty_suffix_F16_sublayer": "CERTIFIED",
            "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
            "nonempty_suffix_strong_F16": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5_maturity": "9/18",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if scope != expected_scope:
            errors.append("strict scope")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("all_face_arbitrary_suffix_F12", "one_step_derivative_envelope", "L(B)=1"),
        ("all_face_arbitrary_suffix_F12", "suffix_derivative", "1"),
        ("all_face_arbitrary_suffix_F12", "all_five_physical_face_grammars_covered", False),
        ("all_face_arbitrary_suffix_F12", "global_rank_path_moment_required_for_F12_field", True),
        ("F16_frontier", "nonempty_suffix_global_physical_moment", "CERTIFIED"),
        ("F16_frontier", "all_face_standard_family_strong_F16", "CERTIFIED"),
        ("F16_frontier", "cemetery_compatible_F16", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    for key, value in (
        ("F12_multiplier", "2"),
        ("physical_L6over5_moment", "NOT_CERTIFIED"),
        ("physical_block_tail_exponent", "1"),
        ("status", "NOT_CERTIFIED"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["F16_frontier"]["empty_suffix_subspace"][key] = value
        mutations.append(mutation)
    for key, value in (
        ("probability_sums_to_one", False),
        ("finite_available_moment_value", 0),
        ("divergent_required_product_moment", "finite"),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["F16_frontier"]["moment_nonimplication"][key] = value
        mutations.append(mutation)
    for key, value in (
        ("previous_global_maturity", "9/18"),
        ("newly_completed_parameterized_field", "F16"),
        ("current_global_maturity", "10/18"),
        ("complete_18_field_operator_block_count", 1),
    ):
        mutation = copy.deepcopy(source)
        mutation["result"]["Gate5_maturity_update"][key] = value
        mutations.append(mutation)
    for key, value in (
        ("all_five_face_arbitrary_suffix_F12", "NOT_CERTIFIED"),
        ("terminal_empty_suffix_F16_sublayer", "NOT_CERTIFIED"),
        ("complete_strong_F13_intertwiner", "CERTIFIED"),
        ("nonempty_suffix_strong_F16", "CERTIFIED"),
        ("complete_all_face_F10", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
        ("F14_through_F18", "CERTIFIED"),
        ("dynamic_MT_DQ", "CERTIFIED"),
        ("Gate3", "CERTIFIED"),
        ("Gate5_maturity", "18/18"),
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
    mutation["result"]["all_face_arbitrary_suffix_F12"]["sample_replays"][1][
        "C1_trace_pullback_multiplier_strict_upper"
    ] = "1"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["all_face_arbitrary_suffix_F12"]["face_rows"].pop()
    mutations.append(mutation)
    for top, value in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[top] = value
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
