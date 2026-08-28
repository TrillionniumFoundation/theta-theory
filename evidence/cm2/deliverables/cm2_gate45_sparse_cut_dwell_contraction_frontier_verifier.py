#!/usr/bin/env python3
"""Fail-closed verifier for scheduled Gate-4/5 sparse-cut blocks."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate45_sparse_cut_dwell_contraction_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate45.sparse-cut-dwell-contraction-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.sparse-cut-dwell-contraction-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate45_sparse_cut_dwell_contraction_frontier_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest type"]
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if manifest.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency table")
    else:
        for name, expected in certificate.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency {name}")

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    core = result.get("core_block_sharpening", {})
    expected_core = {
        "b_core": "720269600000/720626832337",
        "block_length": 2018,
        "sharpened_exact_rational_upper": "3/8",
        "exact_statement": "b_core^2018<3/8<1/2",
        "comparison_replayed_with_exact_integer_arithmetic": True,
    }
    for key, expected in expected_core.items():
        if core.get(key) != expected:
            errors.append(f"core {key}")
    if not isinstance(core.get("exact_power_witness_sha256"), str):
        errors.append("core witness")

    ledger = result.get("abstract_scheduled_ledger", {})
    expected_ledger = {
        "arbitrary_registered_cut_count_h": True,
        "probabilistic_geometric_cut_count_tail_used": False,
        "deterministic_dwell_schedule_used": True,
        "weighted_forcing_summability_still_required_for_weighted_l1": True,
    }
    for key, expected in expected_ledger.items():
        if ledger.get(key) != expected:
            errors.append(f"ledger {key}")

    shell = result.get("shell_scheduled_contraction", {})
    expected_shell = {
        "cut_factor_strict_upper": "15/8",
        "dwell_steps": 2018,
        "cycle_coefficient_strict_upper": "45/64",
        "cycle_contraction": True,
        "pointwise_Green_resolvent_strict_upper": "64/19",
        "rational_exponential_cut_weight": "4/3",
        "weighted_cycle_coefficient_strict_upper": "15/16",
        "weighted_Green_resolvent_strict_upper": "16",
        "external_cut_count_tail_required_for_scheduled_scalar_ledger": False,
        "scheduled_shell_arbitrary_cut_count_contraction": "CERTIFIED_ABSTRACTLY",
    }
    for key, expected in expected_shell.items():
        if shell.get(key) != expected:
            errors.append(f"shell {key}")

    field7 = result.get("raw_field7_scheduled_contraction", {})
    expected_field7 = {
        "all_key_cut_factor_upper": "580000/1999",
        "covered_candidate_key_count": 441280,
        "core_block_count": 6,
        "dwell_steps": 12108,
        "five_coarse_blocks_do_not_contract": True,
        "six_coarse_blocks_are_first_contracting_count_for_the_3_over_8_bound": True,
        "cycle_coefficient_strict_upper": "13213125/16375808",
        "cycle_contraction": True,
        "pointwise_Green_resolvent_strict_upper": "16375808/3162683",
        "rational_exponential_cut_weight": "6/5",
        "weighted_cycle_coefficient_strict_upper": "7927875/8187904",
        "weighted_Green_resolvent_exact_upper": "8187904/260029",
        "weighted_Green_resolvent_simplified_strict_upper": "32",
        "external_cut_count_tail_required_for_scheduled_scalar_ledger": False,
        "scheduled_raw_field7_arbitrary_cut_count_contraction": (
            "CERTIFIED_ABSTRACTLY"
        ),
    }
    for key, expected in expected_field7.items():
        if field7.get(key) != expected:
            errors.append(f"field7 {key}")

    frontier = result.get("physical_installation_frontier", {})
    for key in (
        "transported_occurrence_to_24_core_incidence",
        "common_strong_space_DQ_MT_DQ_FACE",
        "strong_complement_cemetery_payload",
        "native_no_hidden_cut_dwell_schedule",
        "complete_18_field_operator_blocks",
    ):
        if frontier.get(key) != "NOT_CERTIFIED":
            errors.append(f"frontier {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "abstract_schedule_implies_native_recut_schedule",
        "scalar_block_product_implies_common_strong_operator_typing",
        "field7_block_contraction_implies_other_17_fields",
        "scheduled_ledger_implies_transport_incidence",
        "scheduled_ledger_implies_cemetery_payload",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "native_unbounded_repeated_cut_recovery",
        "stable_quotient_PPE",
        "three_norm_Kac_phase_closure",
        "Gate4",
        "Gate5",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "core_2018_step_upper_3_over_8": "CERTIFIED",
        "scheduled_shell_arbitrary_cut_contraction": "CERTIFIED_ABSTRACTLY",
        "scheduled_raw_field7_arbitrary_cut_contraction": "CERTIFIED_ABSTRACTLY",
        "native_physical_no_hidden_cut_dwell_schedule": "NOT_CERTIFIED",
        "transported_occurrence_to_24_core_incidence": "NOT_CERTIFIED",
        "common_strong_space_and_cemetery_payload": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    mutate(("result", "core_block_sharpening", "block_length"), 2017)
    mutate(("result", "core_block_sharpening", "sharpened_exact_rational_upper"), "1/2")
    mutate(("result", "abstract_scheduled_ledger", "probabilistic_geometric_cut_count_tail_used"), True)
    mutate(("result", "shell_scheduled_contraction", "dwell_steps"), 0)
    mutate(("result", "shell_scheduled_contraction", "cycle_coefficient_strict_upper"), "1")
    mutate(("result", "shell_scheduled_contraction", "weighted_cycle_coefficient_strict_upper"), "1")
    mutate(("result", "shell_scheduled_contraction", "scheduled_shell_arbitrary_cut_count_contraction"), "NOT_CERTIFIED")
    mutate(("result", "raw_field7_scheduled_contraction", "core_block_count"), 5)
    mutate(("result", "raw_field7_scheduled_contraction", "dwell_steps"), 2018)
    mutate(("result", "raw_field7_scheduled_contraction", "cycle_coefficient_strict_upper"), "1")
    mutate(("result", "raw_field7_scheduled_contraction", "weighted_Green_resolvent_simplified_strict_upper"), "infinity")
    mutate(("result", "physical_installation_frontier", "transported_occurrence_to_24_core_incidence"), "CERTIFIED")
    mutate(("result", "physical_installation_frontier", "common_strong_space_DQ_MT_DQ_FACE"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "abstract_schedule_implies_native_recut_schedule"), True)
    mutate(("result", "strict_nonpromotion", "native_unbounded_repeated_cut_recovery"), "CERTIFIED")
    mutate(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    mutate(("verdict", "native_physical_no_hidden_cut_dwell_schedule"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != manifest["result"]:
        print("ERROR: replay mismatch", file=sys.stderr)
        return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("SCHEDULED_SHELL_ARBITRARY_CUT_CONTRACTION: CERTIFIED_ABSTRACTLY")
    print("SCHEDULED_RAW_FIELD7_ARBITRARY_CUT_CONTRACTION: CERTIFIED_ABSTRACTLY")
    print("NATIVE_PHYSICAL_DWELL_SCHEDULE: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
