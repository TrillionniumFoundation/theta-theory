#!/usr/bin/env python3
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import cm2_round149_terminal_c24_two_sided_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round149-terminal-c24-two-sided-frontier-2026-07-24.json"
SCHEMA = "cm2.round149.terminal-c24-two-sided-frontier.v1"
PINS = {
    "cm2_round149_terminal_c24_two_sided_engine.py": "ffa02ee24969f7b9b4cbd0d81690ba209411a5a00f869a2d935135d1d2376aa8",
    "cm2-round148-atomic-future-input-admission-2026-07-24.json": "7ab3a83998b34811f6af38ea50630a94a3a32a3e43f889b75331e2db716800e3",
    "cm2-round148-atomic-future-input-admission-verification-2026-07-24.json": "dacaf48cb0ae968983ce28dd1006f11fc7ebfc1a24c2b2bd2589b72ffd4c6842",
}
SPECS = [
    {"role": "return_side", "x_power": 4304, "x_cell_index": 37400, "beta_power": 4304, "beta_cell_index": 0, "expected_terminal_classification": "RETURN_AT_3_INNER", "precision": 8192},
    {"role": "survive_side", "x_power": 4304, "x_cell_index": 37410, "beta_power": 4304, "beta_cell_index": 0, "expected_terminal_classification": "SURVIVE_THROUGH_3_INNER", "precision": 8192},
]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def check_pins():
    for name, expected in PINS.items():
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"pin mismatch:{name}")


def run_spec(spec):
    row = engine.audit_cell(spec)
    return {"role": spec["role"], **row}


def build_result():
    check_pins()
    with ProcessPoolExecutor(max_workers=2) as pool:
        cells = list(pool.map(run_spec, SPECS))
    cells.sort(key=lambda row: row["role"])
    by_role = {row["role"]: row for row in cells}
    return_cell = by_role["return_side"]
    survive_cell = by_role["survive_side"]
    if return_cell["terminal_classification"] != "RETURN_AT_3_INNER":
        raise RuntimeError("return side")
    if survive_cell["terminal_classification"] != "SURVIVE_THROUGH_3_INNER":
        raise RuntimeError("survive side")
    if return_cell["official_sequence_sha256"] != survive_cell["official_sequence_sha256"]:
        raise RuntimeError("official sequence")
    return {
        "status": "CERTIFIED_TWO_SIDED_TERMINAL_C24_CLASSIFICATION_FRONTIER",
        "physical_coordinate_scale": "h=2^-4296",
        "shared_beta_strip_in_h_units": ["-1/256", "1/256"],
        "return_side_abs_delta_x_in_h_units": ["37400/256", "37401/256"],
        "survive_side_abs_delta_x_in_h_units": ["37410/256", "37411/256"],
        "strict_unclassified_x_gap_in_h_units": "9/256",
        "audited_cell_rows": cells,
        "audited_cell_rows_sha256": digest(cells),
        "same_complete_R1648_owner_word_chart_homogeneity_incidence_path": True,
        "same_official_sequence_sha256": return_cell["official_sequence_sha256"],
        "full_radius4_candidate_tests_per_cell": 161 * 1648,
        "full_radius4_candidate_tests_total": 2 * 161 * 1648,
        "terminal_classification_census": {"RETURN_AT_3_INNER": 1, "SURVIVE_THROUGH_3_INNER": 1},
        "frontier_contract": {
            "event_kind": "COLLISION1648_TERMINAL_C24_RETURN_SURVIVE_BOUNDARY",
            "two_sided_full_cell_classification_certified": True,
            "a_boundary_between_the_two_closed_cells_is_forced_by_continuity_of_the_frozen_composition": True,
            "unique_global_graph_certified": False,
            "all_beta_fibres_bracketed": False,
            "all_other_event_families_exhausted": False,
        },
        "Round148_DAG_effect": {
            "D02_status_before": "BLOCKED",
            "D02_status_after": "BLOCKED",
            "new_local_frontier_type_added": "terminal C24 return/survive",
            "D03_least_rank_negative_oracle_authorized": False,
        },
        "strict_nonpromotion": {
            "component_v1_id": None,
            "parent_W_v1_id": None,
            "restriction_v1_id": None,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the two cells localize a terminal C24 frontier but do not certify a unique graph on every beta fibre",
            "the 9/256 h gap is intentionally unclassified",
            "the positive collision-three D0 frontier and every other outer-atlas event family remain to be joined",
            "Round144 D02 remains blocked and no versioned identifier is minted",
            "no global Gate5 field or CM2 claim is promoted",
        ],
        "upstream_sha256": {**PINS, **engine.PINS},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build_result()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    args.output.write_text(json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(canonical({"status": result["status"], "output": str(args.output), "result_sha256": document["result_sha256"]}))


if __name__ == "__main__":
    main()
