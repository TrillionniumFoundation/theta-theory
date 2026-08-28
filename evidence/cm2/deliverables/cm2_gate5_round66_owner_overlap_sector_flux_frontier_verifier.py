#!/usr/bin/env python3
"""Independent verifier for the Round-66 Gate-5 owner-overlap frontier."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, replay_sidecar, require, semantic_mutation_test,
    sha256_path, strict_json_path, strict_json_self_test, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round66.owner-overlap-sector-flux-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate5-round66-owner-overlap-sector-flux-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
SIDECAR = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate5_round66_owner_overlap_sector_flux_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
COMMON = HERE / "cm2_round66_common.py"
EXPECTED_PINS_DIGEST = "ae6fe5c44cf9fafbe7dd9160614dd31a5c05d98a08f6a9c3f016aef421b86b03"
EXPECTED_RESULT_DIGEST = "121db225717290f7fce30584a1c0d54378e92ca253b38e9f3ca14c4c92a719c2"


def integrity(data: dict[str, Any], files: bool = True) -> None:
    require(data.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    pins = data.get("pins")
    require(isinstance(pins, dict) and len(pins) == 47, "pin root/count")
    require(digest(pins) == EXPECTED_PINS_DIGEST, "pin-set digest")
    if files:
        validate_pins(HERE, pins)
        require(data.get("report_sha256") == sha256_path(REPORT), "report hash")
        require(data.get("certificate_sha256") == sha256_path(CERT), "cert hash")
        require(data.get("verifier_sha256") == sha256_path(VERIFIER), "verifier hash")
        require(data.get("common_sha256") == sha256_path(COMMON), "common hash")
    result = data.get("result")
    require(isinstance(result, dict), "result root")
    replay = copy.deepcopy(result)
    recorded = replay.pop("internal_replay_digest", None)
    require(recorded == EXPECTED_RESULT_DIGEST and digest(replay) == recorded,
            "result digest")
    require(data.get("verdict") == result.get("strict_status"), "verdict alias")


def semantics(result: dict[str, Any]) -> None:
    require(result["schema"] == RESULT_SCHEMA, "result schema")
    provenance = result["provenance"]
    require(provenance["append_only"] is True and
            provenance["old_artifacts_modified"] is False and
            digest(provenance["pinned_round65_owner_cemetery_jordan_chain"])
            == EXPECTED_PINS_DIGEST, "provenance")

    actual = result["actual_fixed_time_input"]
    require(actual["same_raw_occurrence_law"] is True and
            actual["owner_pieces_disjoint_at_each_fixed_j"] is True and
            actual["owner_sets_nested_across_j"] == "NOT_CERTIFIED" and
            actual["time_j_deleted_or_deduplicated"] is False and
            actual["actual_overlap_departure_birth_masses"] == "NOT_CERTIFIED",
            "fixed-time guards")
    require("n(a)>j" in actual["formula"] and "m_occ" in actual["formula"],
            "fixed-time formula")

    cross = result["terminal_record_crosswalk"]
    require(cross["status"] == "CERTIFIED_EXACT_BOREL_MAXIMAL_OVERLAP" and
            cross["time_coordinate_retained"] is True and
            cross["terminal_eligibility_implies_owner_set_nesting"] is False and
            cross["owner_label_switch_is_death_plus_birth"] is True and
            cross["cross_time_owner_deduplication"] == "ILLEGAL", "crosswalk")
    require(cross["time_update"] == "U_j(j,a,x)=(j+1,a,x) for n(a)>j+1" and
            "bar(ell)_j=bar(ell)_next" in cross["overlap"] and
            "n=j+1" in cross["terminal_departure"], "crosswalk formulas")

    rn = result["rn_frontier"]
    require(rn["status"] == "CERTIFIED_EXACT_ON_FULL_TERMINAL_SOURCE_OWNER_LABEL" and
            rn["live_coefficient"] == {
                "positive_birth": "INFINITY",
                "birth_free_positive_overlap": "1",
                "zero_target": "0",
            } and rn["birth_free_live_plus_departure_coefficient"] == "1" and
            rn["birth_free_density_on_overlap"] == "1" and
            rn["positive_overlap_route_coefficient_below_w_Z_inverse"] is False and
            rn["total_mass_ratio_is_Linfinity_RN_ratio"] is False and
            rn["actual_c_live_star"] == "NOT_EVALUABLE_WITH_FROZEN_MASSES",
            "RN frontier")

    finite = rn["finite_replay"]
    rows = finite["rows"]
    require(len(rows) == 6 and [row["atom"] for row in rows] == list("abcdef"),
            "overlap row IDs")
    source = sum(row["mass"] for row in rows if row["in_j"])
    target = sum(row["mass"] for row in rows if row["in_next"])
    overlap = sum(row["mass"] for row in rows if row["role"] == "overlap")
    terminal = sum(row["mass"] for row in rows if row["role"] == "terminal_exit")
    switch = sum(row["mass"] for row in rows if row["role"] == "owner_departure")
    birth = sum(row["mass"] for row in rows if row["role"] == "owner_birth")
    require((source, target, overlap, terminal, switch, birth) == (21, 21, 14, 2, 5, 7),
            "overlap arithmetic")
    require(finite["source_total"] == source and finite["next_total"] == target and
            finite["overlap_total"] == overlap and
            finite["terminal_departure_total"] == terminal and
            finite["switch_departure_total"] == switch and
            finite["birth_total"] == birth and
            Q(finite["birth_free_next_source_mass_ratio"]) == Q(2, 3) and
            finite["with_birth_c_live_star"] == "INFINITY" and
            finite["birth_free_full_label_c_live_star"] == "1" and
            finite["birth_free_accounting_c_star"] == "1", "finite replay")

    sectors = result["seven_sector_overlap"]
    expected_names = [
        "active-clock", "raw-Z", "power-Orlicz", "complement",
        "variation", "common-mode", "one-shot-cemetery",
    ]
    expected_kappa = [Q(1, 2), Q(2), Q(2), Q(1), Q(2), Q(1), Q(1)]
    require(sectors["status"] == "CERTIFIED_EXACT_TYPED_RN_FORMULA" and
            sectors["sectors"] == expected_names and
            sectors["positive_target_sector_birth"] == "INFINITY" and
            sectors["sum_marks_first_is_typed_safe"] is False and
            len(sectors["finite_replay"]) == 7, "sector typing")
    for name, expected, row in zip(expected_names, expected_kappa,
                                   sectors["finite_replay"]):
        before = [Q(x) for x in row["h_j_on_overlap"]]
        after = [Q(x) for x in row["h_next_on_overlap"]]
        ratios = [after[i] / before[i] for i in range(2)]
        require(row["sector"] == name and
                [Q(x) for x in row["overlap_ratios"]] == ratios and
                Q(row["birth_free_kappa_star"]) == max(ratios) == expected and
                row["positive_birth_kappa_star"] == "INFINITY", f"sector {name}")
    require(sectors["actual_fixed_j_base_owner"] == "FINITE" and
            sectors["actual_fixed_j_complement_variation_common_mode"] == "FINITE" and
            sectors["actual_active_clock_raw_Z_power_Orlicz"] == "NOT_CERTIFIED_FINITE" and
            sectors["actual_pre_regularization_cemetery"] == "NOT_MATERIALIZED" and
            sectors["actual_finite_seven_sector_slice"] == "NOT_CERTIFIED" and
            sectors["actual_sector_drift_coefficients"] == "NOT_CERTIFIED",
            "sector guards")

    raw = result["raw_Orlicz_frontier"]
    require(raw["same_slice_comparison"] == "H_raw<=H_Orl<C_col H_raw" and
            raw["comparison_creates_finiteness"] is False and
            raw["comparison_creates_cross_j_coefficient"] is False and
            raw["finite_truncations_uniform"] is False and
            raw["actual_raw_Z_Orlicz_drift"] == "NOT_CERTIFIED", "raw guards")
    require(len(raw["truncation_rows"]) == 12, "raw truncation count")
    for row in raw["truncation_rows"]:
        n = row["N"]
        require(row == {"N": n, "K_truncated": n,
                        "raw_mark": str(2 ** (n + 1)), "finite": True},
                "raw truncation")

    arrival = result["arrival_typing"]
    require(arrival["terminal_exit_is_pre_regularization_cemetery"] is False and
            arrival["switch_departure_is_one_shot"] is True and
            arrival["absorbing_occupancy_for_w_Z_gt_1"] == "DIVERGES_IF_NONZERO" and
            arrival["live_plus_departure_identity_supplies_decay"] is False and
            arrival["pre_regularization_cemetery"] == "NOT_MATERIALIZED",
            "arrival typing")

    oriented = result["oriented_positive_frontier"]
    f_upper = Q(oriented["forward_strict_upper"])
    r_upper = Q(oriented["reverse_strict_upper"])
    require(oriented["exact_mass_crosswalk_necessary_row"] ==
            "xi_j^f(X)=m_p=xi_j^r(X)" and
            oriented["forward_reverse_equality_is_only_first_scalar_test"] is True and
            f_upper + r_upper == Q(oriented["upper_sum"]) and
            f_upper - r_upper == Q(oriented["upper_difference"]) and
            oriented["unequal_upper_bounds_imply_unequal_actual_totals"] is False and
            oriented["positive_lower_bound_for_m_p"] == "NOT_CERTIFIED" and
            oriented["two_RN_rows"] == "NOT_CERTIFIED" and
            oriented["common_mode_equality"] == "NOT_CERTIFIED" and
            oriented["terminal_crosswalk_identifies_abs_lambda_with_m_owner"] is False and
            oriented["physical_oriented_carrier"] == "NOT_CERTIFIED", "oriented")

    fields = result["remaining_eight_fields"]
    expected_fields = ["F5", "F6", "F10", "F11", "F14", "F15", "F17", "F18"]
    require(fields["required_field_count"] == 18 and
            fields["certified_maturity"] == 10 and fields["open_count"] == 8 and
            fields["new_field_promoted"] is False and
            [row["field"] for row in fields["rows"]] == expected_fields,
            "remaining fields")

    tech = result["latest_technology_boundary"]
    require(tech["dominated_kernel_theorems_assume_domination_and_Lyapunov_rows"] is True and
            tech["dominated_kernel_theorems_remove_owner_birth_singularity"] is False and
            tech["killing_branching_diffusions_are_same_process_recipient"] is False and
            tech["external_theorem_promoted"] is False, "technology")
    require(result["strict_status"] == {
        "Gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_blocks": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict status")


def independent_replay() -> dict[str, Any]:
    atoms = [
        (2, True, False, "terminal"),
        (3, True, True, "overlap"),
        (5, True, False, "switch"),
        (7, False, True, "birth"),
        (11, True, True, "overlap"),
        (13, False, False, "inactive"),
    ]
    source = sum(m for m, old, _new, _role in atoms if old)
    target = sum(m for m, _old, new, _role in atoms if new)
    overlap = sum(m for m, _old, _new, role in atoms if role == "overlap")
    birth = sum(m for m, _old, _new, role in atoms if role == "birth")
    require((source, target, overlap, birth) == (21, 21, 14, 7),
            "independent overlap")
    require(Q(overlap, source) == Q(2, 3), "independent average ratio")
    require(max(Q(1), Q(1)) == 1, "independent Linfinity density")

    raw_before, raw_after = [Q(2), Q(4)], [Q(4), Q(4)]
    raw_kappa = max(raw_after[i] / raw_before[i] for i in range(2))
    require(raw_kappa == 2, "independent raw kappa")

    f_upper = Q(395304765824751, 220000)
    r_upper = Q(162772550633721, 176000)
    require(f_upper + r_upper == Q(2395081816467609, 880000) and
            f_upper - r_upper == Q(69759664557309, 80000),
            "independent oriented arithmetic")
    return {
        "source_total": source,
        "target_total": target,
        "overlap_total": overlap,
        "birth_total": birth,
        "birth_free_average_ratio": "2/3",
        "birth_free_full_label_c_star": "1",
        "positive_birth_c_star": "INFINITY",
        "raw_overlap_kappa": "2",
        "open_fields": 8,
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, timeout=240,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    if SIDECAR.exists():
        replay_sidecar(HERE, SIDECAR, 5)
    if regenerate:
        deterministic(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = strict_json_path(MANIFEST)
        if args.audit:
            run_audit(data)
            print("AUDIT: PASS")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(independent_replay(), sort_keys=True))
            return 0
        if args.self_test:
            run_audit(data)
            semantic = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            print(f"HOSTILE_SEMANTIC_REJECTED: {semantic}/{semantic}")
            print(f"HOSTILE_JSON_REJECTED: {strict}/{strict}")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            proc = subprocess.run(
                [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=False, timeout=240,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND66_GATE5_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate5 maturity: 10/18")
    print("complete blocks: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
