#!/usr/bin/env python3
"""Fail-closed verifier for the Round-44 all-face Borel F13 payload."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round44_all_face_suffix_two_trace_f13_cert as cert


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
        core = result["C24_core_boundary_flux"]
        if Q(core["axis_total_l1_perimeter_strict_upper"]) != Q(33013, 312500):
            errors.append("axis perimeter")
        if Q(core["diagonal_total_l1_perimeter_strict_upper"]) != Q(218213, 156250):
            errors.append("diagonal perimeter")
        if Q(core["C24_total_l1_perimeter_strict_upper"]) != Q(469439, 312500):
            errors.append("total perimeter")
        if Q(core["normalized_C24_boundary_l1_measure_strict_upper"]) != Q(
            469439, 1950000
        ):
            errors.append("normalized perimeter")
        if Q(core["two_trace_ratio_to_c_X_insertion"]) != Q(469439, 975000):
            errors.append("core/X ratio")
        if core["status"] != "CERTIFIED_EXACT_RATIONAL_BOUND":
            errors.append("core flux status")

        occurrence = result["occurrence_suffix_two_trace_transport"]
        if occurrence["depth_one_physical_rows"] != 64:
            errors.append("occurrence rows")
        if occurrence["depth_one_oriented_hit_miss_traces"] != 128:
            errors.append("occurrence traces")
        if Q(occurrence["occurrence_TV_ratio_to_c_X_insertion"]) != Q(63, 8000):
            errors.append("occurrence/X ratio")
        transport = occurrence["suffix_transport"]
        if transport["prefix_regular_branch_Linfinity_constant"] != "1":
            errors.append("prefix constant")
        if transport["suffix_positive_pushforward_mass_constant"] != "1":
            errors.append("suffix constant")
        if transport["constant_test_cancellation_preserved"] is not True:
            errors.append("constant cancellation")
        if occurrence["status"] != "CERTIFIED_ON_EVERY_FINITE_REGULAR_SUFFIX":
            errors.append("occurrence transport status")

        join = result["five_face_F13_Borel_join"]
        if join["face_kind_count"] != 5 or len(join["rows"]) != 5:
            errors.append("five-face count")
        if not join["all_five_physical_face_grammars_have_a_Borel_F13_payload"]:
            errors.append("five-face join")
        if join["status"] != "CERTIFIED_REGULAR_DENSITY_BOREL_LAYER":
            errors.append("F13 layer status")
        if digest_rows(join["rows"]) != join["rows_sha256"]:
            errors.append("face rows digest")

        charge = result["same_ID_physical_F13_trace_charge"]
        if Q(charge["exact_F13_over_X_ratio"]) != Q(3816937, 7800000):
            errors.append("F13/X ratio")
        if Q(charge["exact_F13_over_D1_ratio"]) != Q(3816937, 47112000):
            errors.append("F13/D1 ratio")
        if charge["physical_L6over5_moment"]["status"] != "CERTIFIED":
            errors.append("F13 moment")
        if charge["physical_weighted_tail"]["inherited_block_exponent"] != "1/6":
            errors.append("F13 tail exponent")
        if charge["physical_weighted_tail"]["collision_time_rate_numeric"] is not False:
            errors.append("collision rate overclaim")
        lazy = charge["lazy_symbolic_registry"]
        if lazy["candidate_occurrence_trace_pair_slots"] != 210366464:
            errors.append("trace pairs")
        if lazy["candidate_oriented_occurrence_trace_slots"] != 420732928:
            errors.append("oriented slots")
        if lazy["candidate_slot_count_claimed_as_nonempty_physical_count"] is not False:
            errors.append("slot overclaim")
        if charge["arbitrary_Rn_suffix_pushed_two_trace_TV_ledger"] != "CERTIFIED":
            errors.append("trace ledger")

        f16 = result["F16_frontier"]
        if f16["regular_density_C24_boundary_flux_TV_cost"] != "CERTIFIED_AS_F13_INPUT":
            errors.append("F16 input")
        if f16["all_face_standard_family_strong_flux_operator_cost"] != "NOT_CERTIFIED":
            errors.append("F16 overclaim")
        if f16["F16"] != "NOT_CERTIFIED":
            errors.append("F16 verdict")

        scope = result["strict_nonpromotion"]
        if scope["arbitrary_Rn_suffix_pushed_two_trace_TV_ledger"] != "CERTIFIED":
            errors.append("ledger verdict")
        if scope["all_five_face_regular_density_Borel_F13_payload"] != "CERTIFIED":
            errors.append("F13 verdict")
        if scope["complete_strong_F13_operator_intertwiner"] != "NOT_CERTIFIED":
            errors.append("strong F13 overclaim")
        if scope["F12_C1_trace_pullback"] != "NOT_CERTIFIED":
            errors.append("F12")
        if scope["F16"] != "NOT_CERTIFIED":
            errors.append("F16 scope")
        if scope["dynamic_MT_DQ"] != "NOT_CERTIFIED":
            errors.append("MT_DQ")
        if scope["Gate5_maturity"] != "8/18":
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


def digest_rows(rows: Any) -> str:
    return hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []
    edits = [
        ("C24_core_boundary_flux", "C24_total_l1_perimeter_strict_upper", "0"),
        ("C24_core_boundary_flux", "normalized_C24_boundary_l1_measure_strict_upper", "0"),
        ("C24_core_boundary_flux", "two_trace_ratio_to_c_X_insertion", "1"),
        ("C24_core_boundary_flux", "status", "OPEN"),
        ("occurrence_suffix_two_trace_transport", "depth_one_physical_rows", 0),
        ("occurrence_suffix_two_trace_transport", "depth_one_oriented_hit_miss_traces", 0),
        ("occurrence_suffix_two_trace_transport", "occurrence_TV_ratio_to_c_X_insertion", "1"),
        ("occurrence_suffix_two_trace_transport", "status", "OPEN"),
        ("five_face_F13_Borel_join", "face_kind_count", 0),
        ("five_face_F13_Borel_join", "all_five_physical_face_grammars_have_a_Borel_F13_payload", False),
        ("five_face_F13_Borel_join", "status", "OPEN"),
        ("same_ID_physical_F13_trace_charge", "exact_F13_over_X_ratio", "1"),
        ("same_ID_physical_F13_trace_charge", "exact_F13_over_D1_ratio", "1"),
        ("same_ID_physical_F13_trace_charge", "arbitrary_Rn_suffix_pushed_two_trace_TV_ledger", "OPEN"),
        ("F16_frontier", "all_face_standard_family_strong_flux_operator_cost", "CERTIFIED"),
        ("F16_frontier", "F16", "CERTIFIED"),
    ]
    for section, key, value in edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["occurrence_suffix_two_trace_transport"]["suffix_transport"][
        "suffix_positive_pushforward_mass_constant"
    ] = "2"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["same_ID_physical_F13_trace_charge"]["physical_weighted_tail"][
        "collision_time_rate_numeric"
    ] = True
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["same_ID_physical_F13_trace_charge"]["lazy_symbolic_registry"][
        "candidate_slot_count_claimed_as_nonempty_physical_count"
    ] = True
    mutations.append(mutation)
    for key, value in (
        ("arbitrary_Rn_suffix_pushed_two_trace_TV_ledger", "OPEN"),
        ("all_five_face_regular_density_Borel_F13_payload", "OPEN"),
        ("physical_F13_trace_charge_L6over5_and_tail", "OPEN"),
        ("complete_strong_F13_operator_intertwiner", "CERTIFIED"),
        ("F12_C1_trace_pullback", "CERTIFIED"),
        ("F16", "CERTIFIED"),
        ("complete_all_face_F10", "CERTIFIED"),
        ("F14_through_F18", "CERTIFIED"),
        ("strong_cemetery", "CERTIFIED"),
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
