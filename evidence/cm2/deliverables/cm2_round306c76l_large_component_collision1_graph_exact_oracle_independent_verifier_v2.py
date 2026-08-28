#!/usr/bin/env python3
"""C76-L independent no-producer verifier v2 with upstream provenance.

V2 is append-only and supersedes v1 verification *objects*.  It may reuse the
pin-checked v1 byte/ledger verifier as a library, but never imports or executes
the C76-L producer.  In addition to candidate-internal closure, it freshly
reads the pinned C68/C56/C41/C55B authorities and reconstructs every decision,
branch, handoff, and degree-one boundary lineage.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
sys.path.insert(0, str(OUT))
import cm2_round306c76l_large_component_collision1_graph_exact_oracle_independent_verifier_v1 as base  # noqa:E402


V1_SOURCE_SHA256 = "74bd2de3b133f0f6452bd8fbbc105ac8ca725ca8007b52ca74f16b5651a57789"

C41_DIR = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C32_DIR = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"

INPUTS: dict[str, tuple[Path, str]] = {
    "C68_RESULT": (OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json", "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37"),
    "C68_TASKS": (OUT / "cm2_round306c68l_blocker_crosswalk_large_current_task_replay_v1.jsonl.gz", "bc62868582ca26be996904fe8120422b0d67e8afc0080dfd4650512a041eaa2f"),
    "C56_RESULT": (OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json", "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601"),
    "C56_TASKS": (OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz", "6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a"),
    "C55B_RESULT": (OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json", "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93"),
    "C55B_CELLS": (OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz", "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce"),
    "C55B_COMPONENTS": (OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz", "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04"),
    "C41_RESULT": (C41_DIR / "result.json", "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f"),
    "C41_AMBIENT": (C41_DIR / "routed_ambient_cells.jsonl.gz", "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8"),
    "C41_C1": (C41_DIR / "c1_h1_surface_outers.jsonl.gz", "487fb8e9e9355dcb7094b302b70b6843a8fb6db0baf4f1e116496c9de9723294"),
    "C41_C2": (C41_DIR / "c2_surface_outers.jsonl.gz", "80bcf335780d61b12e181743699343a0dada51d320f7b1b4643a9c6432b7eee9"),
    "C41_ENDPOINTS": (C41_DIR / "endpoint_recharts.jsonl.gz", "e631af197d07e0dbbf0b67fcef92e2a981530f68e9bef84f1806f59ad8eb2219"),
    "C32_CELLS": (C32_DIR / "compact_cells.jsonl.gz", "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8"),
    "C35_PATH": (C35_DIR / "path_occurrences.jsonl.gz", "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66"),
    "C37_PATH": (C37_DIR / "reflected_r1648_occurrences.jsonl.gz", "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5"),
    "CHART_MANIFEST": (OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json", "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b"),
    "H1_CORE": (OUT / "cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py", "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8"),
}

CAPABILITIES: dict[str, tuple[Path, str]] = {
    "C71B_RESULT": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/cm2_round306c71b_child_h1_clipped_arrangement_successor_v3_result.json", "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246"),
    "C71B_VERIFY": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/independent_verification_v3_1.json", "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612"),
    "C71B_RECEIPT": (ROOT / ".cm2-runtime/c71b-v3-final-75c21279/dual_build_publication_completion_receipt_v3.json", "3a6cfa624fab8cd1b787d3facd139cf9e055a008236864d894d2633522fe9fbc"),
    "C72B2_RESULT": (ROOT / ".cm2-runtime/c72b2-build-a.v2-3eb4d9c9/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2_result.json", "0c8c56a86d3293dd08bc1fef95a72fe0aedc3a35edb20ff0ec9c6e19cd69d1f3"),
    "C72B2_VERIFY": (ROOT / ".cm2-runtime/c72b2-independent-a.v2-3212bb3d.json", "21988ad9b5d746495489e506fadfdf537848eeae6a788a64c6bca3b11c2c9252"),
    "C72B2_RECEIPT": (ROOT / ".cm2-runtime/c72b2-completion-outer-receipt.v2-a53e5319.json", "e0d6da2518d48278a42ffea5e6a676b11001d531e971fdc59da39f3b524dec62"),
    "C72O_RESULT": (ROOT / ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1_result.json", "fd9ca6489f5fedef85fb55de6906a62ecadc417c72d7eb938a6268e7f402302a"),
    "C72O_VERIFY": (ROOT / ".cm2-runtime/c72o-independent-verification-v2.json", "2d34c25b5fd9f2b3a1e8b30d184b40d8a93ffce8c192d193b75715e0d7a68ccb"),
    "C73_RESULT": (ROOT / ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2_result.json", "5de9d37c69ed4d13d972eff8845ed55ad695ab040d6c1beda01626c0c065c615"),
    "C73_VERIFY": (ROOT / ".cm2-runtime/c73v2-audit-a.W2AYpD/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verification_v2.json", "784505135d105fcdf05cc2d6e37779ea896f7d1bbe06e75dd1019b67ae951fe1"),
    "C74_RESULT": (ROOT / ".cm2-runtime/c74-final-a.AzIjhj/cm2_round306c74_exact_multi_graph_order_oracle_v1_result.json", "8d2372de67a5ed0d87a6699845778c9e4d05e183cd21b599a3fd6287032e27b1"),
    "C74_VERIFY": (ROOT / ".cm2-runtime/c74-audit-a.cazCPb/cm2_round306c74_exact_multi_graph_order_oracle_v1_independent_verification_v1.json", "eb4fbefba436ca827a6a60ceb9a3978c496fdbf9798a7eed29333e2067d256cb"),
    "C75_RESULT": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_result.json", "1d9d4b2f8b7a4bfb6133ce7b23c22765ef9097c133cc47dc199dd0479f478366"),
    "C75_VERIFY": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_independent_verification_v1.json", "8f620e4e7312828dcbcee23cf3f33280c8583bd414ded493b7996b2279131a4c"),
    "C75_RECEIPT": (ROOT / ".cm2-runtime/c75-build-a2.TG7bbZ/cm2_round306c75_first_tangency_exact_strata_oracle_v1_dual_completion_receipt_v1.json", "dbbad4ea8d807b6bcb8b7f121acc57f782925be7e00c9267b9edf011e3eba2b1"),
    "C74L_RESULT": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_v1_result.json", "53732dbd4d3be61f26a4aba74952c2aef40684c9d2fb23bd9bd6692917fc5b8d"),
    "C74L_VERIFY": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_v1_independent_verification_v1_1.json", "f0ee22df980db6886dd73e014796418512925d28dce37d1be0caf04d293310e5"),
    "C74L_RECEIPT": (ROOT / ".cm2-runtime/c74l-final-seed1.7LcQlt/cm2_round306c74l_source_seam_collision1_handoff_successor_dual_completion_receipt_v1.json", "1b9459e41a3de4ce5ab2f99b946ce6cb325c63934d87c641571c474f62ad7a3a"),
}

SELECTED = {
    "UNRESOLVED_C41_ALGEBRAIC_H0_SEAM_RECHART_OUTER": 29,
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER": 832,
    "UNRESOLVED_C41_C1_REGULAR_MULTI_GRAPH_OUTER": 11_917,
    "UNRESOLVED_C41_H1_GRAPH_OR_BOUNDARY_OUTER": 3_858,
    "UNRESOLVED_C41_SOURCE_RADICAL_STEREOGRAPHIC_ENDPOINT_OUTER": 247,
}


def expected_input_pins() -> dict[str, str]:
    return {key: pin for key, (_path, pin) in INPUTS.items()}


def expected_capability_pins() -> dict[str, dict[str, str]]:
    return {key: {"path": str(path.relative_to(ROOT)), "sha256": pin}
            for key, (path, pin) in CAPABILITIES.items()}


def read_map(path: Path, key: str, wanted: set[str] | None = None) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in base.row_stream(path, path.name):
        value = row[key]
        if wanted is None or value in wanted:
            base.need(value not in output, path.name + ":unique:" + value); output[value] = row
    return output


def validate_pins(result: Mapping[str, Any]) -> None:
    expected_inputs = expected_input_pins(); expected_caps = expected_capability_pins()
    base.need(result["input_file_sha256"] == expected_inputs, "result input pin projection")
    base.need(result["sealed_capability_pins"] == expected_caps, "result capability pin projection")
    for key, (path, pin) in INPUTS.items():
        base.need(base.sha_file(path) == pin, "actual input pin:" + key)
    for key, (path, pin) in CAPABILITIES.items():
        base.need(base.sha_file(path) == pin, "actual capability pin:" + key)


def cell_face_is_outer_boundary(cell: Mapping[str, Any], face: str,
                                spec: Mapping[str, Any]) -> bool:
    if spec["fixed_axis"] == "t":
        endpoints = tuple(Q(item["value"]) for item in cell["physical_t_interval"])
    else:
        endpoints = tuple(Q(item) for item in cell["physical_p_interval"])
    endpoint = 0 if face.lower().endswith("lower") or face.upper().endswith("LOW") else 1
    return Q(spec["fixed_value"]) == endpoints[endpoint]


def check_decision(row: Mapping[str, Any], cross: Mapping[str, Any], task: Mapping[str, Any],
                   ambient: Mapping[str, Any], cells: Mapping[str, Mapping[str, Any]]) -> None:
    equal = {
        "C68_large_task_row_sha256": cross["row_sha256"],
        "C56_task_row_sha256": task["row_sha256"],
        "C41_ambient_row_sha256": ambient["row_sha256"],
        "pair_index": cross["pair_index"], "path": cross["path"],
        "source_path": task["source_path"], "parent_volume_fraction": task["parent_volume_fraction"],
        "representative_cell_id": task["representative_cell_id"],
        "reflected_cell_id": task["reflected_cell_id"],
        "input_residual_classification": cross["residual_classification"],
        "input_raw_classification": ambient["raw_classification"],
        "input_witness": ambient["raw_witness"],
        "exact_representative_box": ambient["closed_representative_box"],
        "exact_reflected_box": ambient["closed_reflected_box"],
    }
    for key, value in equal.items():
        base.need(row.get(key) == value, "decision upstream field:" + key)
    base.need(cross["C56_task_row_sha256"] == task["row_sha256"] and
        cross["C41_routed_ambient_row_sha256"] == task["C41_routed_ambient_row_sha256"] == ambient["row_sha256"],
        "C68/C56/C41 foreign keys")
    for key in ("pair_index", "path", "residual_classification"):
        base.need(cross[key] == task[key] == ambient[key], "C68/C56/C41:" + key)
    for key in ("representative_cell_id", "reflected_cell_id", "source_path", "parent_volume_fraction"):
        base.need(task[key] == ambient[key], "C56/C41:" + key)
    rep, reflected = cells[task["representative_cell_id"]], cells[task["reflected_cell_id"]]
    base.need(rep["reflection_partner_cell_id"] == reflected["cell_id"] and
        reflected["reflection_partner_cell_id"] == rep["cell_id"] and
        rep["pair_index"] == reflected["pair_index"] == row["pair_index"], "C55B reflected pair")
    base.need(row["gate3_chart"] == rep["gate3_chart"] and row["parent_key"] == rep["origin_key"] and
        rep["component_index"] in {0, 1} and reflected["component_index"] in {0, 1}, "C55B decision cell")


def side_cell(decision: Mapping[str, Any], side: str,
              cells: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    base.need(side in {"REPRESENTATIVE", "REFLECTED"}, "physical side")
    return cells[decision["representative_cell_id"] if side == "REPRESENTATIVE" else
                 decision["reflected_cell_id"]]


def expected_side_box(decision: Mapping[str, Any], side: str) -> Any:
    return decision["exact_representative_box"] if side == "REPRESENTATIVE" else decision["exact_reflected_box"]


def check_branch(row: Mapping[str, Any], decision: Mapping[str, Any],
                 cells: Mapping[str, Mapping[str, Any]], registry_object: str) -> None:
    side = row["physical_side"]; cell = side_cell(decision, side, cells)
    expected_task_id = "c76l-task:" + base.digest({"C68_large_task_row_sha256": decision["C68_large_task_row_sha256"],
        "pair_index": decision["pair_index"], "path": decision["path"]})
    equal = {"source_task_id": expected_task_id,
        "source_C68_row_sha256": decision["C68_large_task_row_sha256"],
        "source_C41_row_sha256": decision["C41_ambient_row_sha256"],
        "pair_index": decision["pair_index"], "path": decision["path"],
        "component_index": cell["component_index"], "gate3_chart": cell["gate3_chart"],
        "closed_physical_box": expected_side_box(decision, side),
        "semialgebraic_registry_object_sha256": registry_object}
    for key, value in equal.items():
        base.need(row.get(key) == value, "branch lineage:" + key)


def check_handoff(row: Mapping[str, Any], decision: Mapping[str, Any],
                  cells: Mapping[str, Mapping[str, Any]], registry_object: str,
                  input_pin_set: str, capability_pin_set: str) -> None:
    side = row["physical_side"]; cell = side_cell(decision, side, cells)
    expected_task_id = "c76l-task:" + base.digest({"C68_large_task_row_sha256": decision["C68_large_task_row_sha256"],
        "pair_index": decision["pair_index"], "path": decision["path"]})
    equal = {"source_task_id": expected_task_id,
        "source_C68_row_sha256": decision["C68_large_task_row_sha256"],
        "source_C56_row_sha256": decision["C56_task_row_sha256"],
        "source_C41_row_sha256": decision["C41_ambient_row_sha256"],
        "pair_index": decision["pair_index"], "path": decision["path"],
        "component_index": cell["component_index"], "component_id": cell["component_id"],
        "gate3_chart": cell["gate3_chart"], "closed_physical_box": expected_side_box(decision, side),
        "semialgebraic_registry_object_sha256": registry_object,
        "input_pin_set_sha256": input_pin_set, "capability_pin_set_sha256": capability_pin_set,
        "physical_incidence_digest": base.digest(decision["physical_graph_endpoint_occurrences"])}
    for key, value in equal.items():
        base.need(row.get(key) == value, "handoff lineage:" + key)


def check_boundary(row: Mapping[str, Any], decisions: Mapping[str, Mapping[str, Any]],
                   cells: Mapping[str, Mapping[str, Any]], scope_sha: str) -> None:
    only = row["sole_occurrence"]; decision = decisions[only["C68_large_task_row_sha256"]]
    cell = cells[decision["representative_cell_id"]]
    outer = cell_face_is_outer_boundary(cell, only["face"], only["exact_physical_face"])
    source = "source" in only["equation"].lower() or "1-p^2" in only["equation"].lower()
    classification = ("FROZEN_SOURCE_GRAZING_BOUNDARY" if source else
        "FROZEN_COMPONENT_CELL_BOUNDARY" if outer else "FROZEN_SELECTED_C76L_SCOPE_BOUNDARY")
    base.need(row["representative_cell_id"] == cell["cell_id"] and
        row["component_index"] == cell["component_index"] and
        row["component_cell_boundary"] is outer and
        row["boundary_classification"] == classification and
        row["frozen_selected_scope_sha256"] == scope_sha, "upstream boundary derivation")


def expect_reject(callback: Any, label: str) -> None:
    try:
        callback()
    except (base.Reject, KeyError, TypeError, ValueError):
        return
    raise base.Reject("escaped provenance attack:" + label)


def verify_provenance(stage: Path) -> dict[str, Any]:
    result = base.strict_json(stage / base.RESULT, "v2 result")
    validate_pins(result)
    input_pin_set = base.digest(dict(sorted(expected_input_pins().items())))
    caps = expected_capability_pins(); capability_pin_set = base.digest(caps)

    all_c68_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []; all_c68 = 0; selected_census: Counter[str] = Counter()
    seen_c68: set[str] = set()
    for row in base.row_stream(INPUTS["C68_TASKS"][0], "v2 C68 tasks"):
        all_c68 += 1; base.need(row["row_sha256"] not in seen_c68, "C68 row unique"); seen_c68.add(row["row_sha256"])
        all_c68_rows.append(row)
        if row["residual_classification"] in SELECTED:
            selected_rows.append(row); selected_census[row["residual_classification"]] += 1
    base.need(all_c68 == 33_319 and len(selected_rows) == 16_883 and selected_census == Counter(SELECTED),
              "fresh selected C68 scope/order/class")
    selected_by_hash = {row["row_sha256"]: row for row in selected_rows}
    full_wanted_c56 = {row["C56_task_row_sha256"] for row in all_c68_rows}
    base.need(len(full_wanted_c56) == 33_319, "full C68 to C56 foreign-key uniqueness")
    all_tasks = read_map(INPUTS["C56_TASKS"][0], "row_sha256", full_wanted_c56)
    base.need(set(all_tasks) == full_wanted_c56 and len(all_tasks) == 33_319, "fresh full C56 universe join")
    wanted_c56 = {row["C56_task_row_sha256"] for row in selected_rows}
    tasks = {claim: all_tasks[claim] for claim in wanted_c56}
    base.need(set(tasks) == wanted_c56, "fresh C56 join")
    wanted_c41 = {row["C41_routed_ambient_row_sha256"] for row in selected_rows}
    ambient = read_map(INPUTS["C41_AMBIENT"][0], "row_sha256", wanted_c41)
    base.need(set(ambient) == wanted_c41, "fresh C41 join")
    full_representative_cells = {task["representative_cell_id"] for task in all_tasks.values()}
    full_reflected_cells = {task["reflected_cell_id"] for task in all_tasks.values()}
    selected_representative_cells = {task["representative_cell_id"] for task in tasks.values()}
    selected_reflected_cells = {task["reflected_cell_id"] for task in tasks.values()}
    base.need(len(full_representative_cells) == len(full_reflected_cells) == 562 and
        not (full_representative_cells & full_reflected_cells) and
        len(full_representative_cells | full_reflected_cells) == 1_124 and
        len(selected_representative_cells) == len(selected_reflected_cells) == 375 and
        not (selected_representative_cells & selected_reflected_cells) and
        len(selected_representative_cells | selected_reflected_cells) == 750 and
        selected_representative_cells < full_representative_cells and
        selected_reflected_cells < full_reflected_cells, "C1 selected cells strict subset of full large universe")
    full_public_cells = full_representative_cells | full_reflected_cells
    public_cells = read_map(INPUTS["C55B_CELLS"][0], "cell_id", full_public_cells)
    base.need(set(public_cells) == full_public_cells and len(public_cells) == 1_124,
              "fresh full 1124 public C55B two-side cell universe")
    wanted_cells = selected_representative_cells | selected_reflected_cells
    cells = read_map(INPUTS["C55B_CELLS"][0], "cell_id", wanted_cells)
    base.need(set(cells) == wanted_cells and len(cells) == 750, "fresh C1-only C55B cell join")

    decisions: dict[str, dict[str, Any]] = {}; first_decision: tuple[Any, ...] | None = None
    for ordinal, row in enumerate(base.row_stream(stage / base.DECISIONS, "v2 decisions")):
        cross = selected_rows[ordinal]; task = tasks[cross["C56_task_row_sha256"]]
        source = ambient[cross["C41_routed_ambient_row_sha256"]]
        check_decision(row, cross, task, source, cells)
        decisions[cross["row_sha256"]] = row
        if first_decision is None:
            first_decision = (row, cross, task, source)
    base.need(len(decisions) == 16_883 and set(decisions) == set(selected_by_hash), "decision provenance exhaustion")

    registry_object = result["semialgebraic_branch_registry"]["object_sha256"]
    branches: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict); first_branch: dict[str, Any] | None = None
    for row in base.row_stream(stage / base.BRANCHES, "v2 branches"):
        source = row["source_C68_row_sha256"]; base.need(source in decisions, "branch source decision")
        check_branch(row, decisions[source], cells, registry_object)
        side = row["physical_side"]; base.need(side not in branches[source], "branch source/side unique")
        branches[source][side] = row
        if first_branch is None:
            first_branch = row
    handoffs: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict); first_handoff: dict[str, Any] | None = None
    for row in base.row_stream(stage / base.HANDOFFS, "v2 handoffs"):
        source = row["source_C68_row_sha256"]; base.need(source in decisions, "handoff source decision")
        check_handoff(row, decisions[source], cells, registry_object, input_pin_set, capability_pin_set)
        side = row["physical_side"]; base.need(side not in handoffs[source], "handoff source/side unique")
        handoffs[source][side] = row
        if first_handoff is None:
            first_handoff = row
    for source, decision in decisions.items():
        if decision["task_disposition"] == "EXACT_PER_SIDE_MIXED_BRANCH_PARTITION":
            base.need(set(branches[source]) == {"REPRESENTATIVE", "REFLECTED"}, "two branch lineage rows")
            base.need(decision["exact_branch_partition_row_sha256"] ==
                [branches[source][side]["row_sha256"] for side in ("REPRESENTATIVE", "REFLECTED")],
                "ordered decision branch lineage")
            expected_handoff = [branches[source][side]["collision3_handoff_row_sha256"]
                                for side in ("REPRESENTATIVE", "REFLECTED")]
            expected_handoff = [item for item in expected_handoff if item is not None]
            base.need(decision["collision3_handoff_row_sha256"] == expected_handoff,
                      "ordered decision branch-to-handoff lineage")
            if expected_handoff:
                base.need(set(handoffs[source]) == {"REPRESENTATIVE", "REFLECTED"} and
                    expected_handoff == [handoffs[source][side]["row_sha256"] for side in
                                         ("REPRESENTATIVE", "REFLECTED")], "two handoff lineage rows")
            else:
                base.need(source not in handoffs, "no-C3 decision has no handoff")
        else:
            base.need(source not in branches and source not in handoffs, "strict decision has no branch/handoff")

    scope_sha = base.digest(sorted(decisions)); boundary_census: Counter[str] = Counter()
    first_boundary: dict[str, Any] | None = None
    for row in base.row_stream(stage / base.BOUNDARIES, "v2 boundaries"):
        check_boundary(row, decisions, cells, scope_sha)
        boundary_census[row["boundary_classification"]] += 1
        if first_boundary is None:
            first_boundary = row
    base.need(boundary_census == Counter({"FROZEN_COMPONENT_CELL_BOUNDARY": 808,
        "FROZEN_SELECTED_C76L_SCOPE_BOUNDARY": 154, "FROZEN_SOURCE_GRAZING_BOUNDARY": 375}),
        "upstream boundary category census")

    attacks: dict[str, str] = {}
    base.need(first_decision is not None and first_branch is not None and first_handoff is not None and
              first_boundary is not None, "attack exemplars")
    d0, x0, t0, a0 = first_decision
    for key in ("C68_large_task_row_sha256", "C56_task_row_sha256", "C41_ambient_row_sha256",
                "pair_index", "path", "source_path", "representative_cell_id", "reflected_cell_id",
                "input_residual_classification", "input_raw_classification", "input_witness"):
        mutant = copy.deepcopy(d0); value = mutant[key]
        mutant[key] = value + 1 if type(value) is int else str(value) + "__ATTACK"
        expect_reject(lambda m=mutant: check_decision(m, x0, t0, a0, cells), "decision:" + key)
        attacks["decision:" + key] = "FAIL_CLOSED"
    source = first_branch["source_C68_row_sha256"]
    for key in ("source_task_id", "source_C68_row_sha256", "source_C41_row_sha256", "pair_index",
                "path", "component_index", "gate3_chart", "closed_physical_box"):
        mutant = copy.deepcopy(first_branch); value = mutant[key]
        mutant[key] = value + 1 if type(value) is int else ({} if type(value) is dict else str(value) + "__ATTACK")
        expect_reject(lambda m=mutant: check_branch(m, decisions[source], cells, registry_object), "branch:" + key)
        attacks["branch:" + key] = "FAIL_CLOSED"
    source = first_handoff["source_C68_row_sha256"]
    for key in ("source_C56_row_sha256", "component_id", "input_pin_set_sha256",
                "capability_pin_set_sha256", "physical_incidence_digest"):
        mutant = copy.deepcopy(first_handoff); mutant[key] = str(mutant[key]) + "__ATTACK"
        expect_reject(lambda m=mutant: check_handoff(m, decisions[source], cells, registry_object,
            input_pin_set, capability_pin_set), "handoff:" + key)
        attacks["handoff:" + key] = "FAIL_CLOSED"
    for key in ("representative_cell_id", "boundary_classification", "frozen_selected_scope_sha256"):
        mutant = copy.deepcopy(first_boundary); mutant[key] = str(mutant[key]) + "__ATTACK"
        expect_reject(lambda m=mutant: check_boundary(m, decisions, cells, scope_sha), "boundary:" + key)
        attacks["boundary:" + key] = "FAIL_CLOSED"
    mutant_result = copy.deepcopy(result); mutant_result["input_file_sha256"]["C68_TASKS"] = "0" * 64
    expect_reject(lambda: validate_pins(mutant_result), "input pin"); attacks["result:input_pin"] = "FAIL_CLOSED"
    mutant_result = copy.deepcopy(result); mutant_result["sealed_capability_pins"]["C71B_RESULT"]["sha256"] = "0" * 64
    expect_reject(lambda: validate_pins(mutant_result), "capability pin"); attacks["result:capability_pin"] = "FAIL_CLOSED"

    return {"upstream_input_file_sha256": expected_input_pins(),
        "upstream_capability_pins": caps, "input_pin_set_sha256": input_pin_set,
        "capability_pin_set_sha256": capability_pin_set,
        "C68_total": all_c68, "selected_C1_count": len(selected_rows),
        "selected_C1_class_census": dict(sorted(selected_census.items())),
        "full_C56_universe_join_count": len(all_tasks),
        "full_representative_cell_count": len(full_representative_cells),
        "full_reflected_cell_count": len(full_reflected_cells),
        "full_public_two_side_cell_universe_count": len(full_public_cells),
        "selected_representative_cell_count": len(selected_representative_cells),
        "selected_reflected_cell_count": len(selected_reflected_cells),
        "selected_two_side_C55B_cell_join_count": len(cells),
        "C56_join_count": len(tasks), "C41_join_count": len(ambient),
        "decision_lineage_count": len(decisions), "branch_lineage_count": sum(map(len, branches.values())),
        "handoff_lineage_count": sum(map(len, handoffs.values())),
        "boundary_classification_census": dict(sorted(boundary_census.items())),
        "coherent_provenance_attacks": {"attack_count": len(attacks), "attacks": attacks,
            "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_UPSTREAM_PROVENANCE_ATTACKS_FAIL_CLOSED"}}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("candidate_a", type=Path)
    parser.add_argument("candidate_b", type=Path); parser.add_argument("output", type=Path)
    args = parser.parse_args(); base.need(not args.output.exists(), "fresh v2 output")
    base.need(base.sha_file(Path(base.__file__).resolve()) == V1_SOURCE_SHA256, "v1 verifier library pin")
    for name in base.ALL_FILES:
        base.need(base.byte_identical(args.candidate_a / name, args.candidate_b / name), "v2 dual bytes:" + name)
    internal = base.verify_stage(args.candidate_a)
    provenance = verify_provenance(args.candidate_a)
    output = base.close_object({"schema": base.SCHEMA + ".independent-no-producer-verification.v2",
        "status": "PASS_INDEPENDENT_C76L_V2__DUAL_BYTES__UPSTREAM_PROVENANCE__EXACT_INCIDENCE_BOUNDARY__ZERO_CREDIT",
        "dual_build_byte_identical": True, "producer_imported_or_executed": False,
        "v1_verifier_library_sha256": V1_SOURCE_SHA256,
        "candidate_internal_reconstruction": internal, "upstream_provenance_reconstruction": provenance,
        "terminal_byte_replay_after_outer_receipts": True,
        "verifier_v2_file_sha256": base.sha_file(Path(__file__).resolve()),
        "formal_credit": 0, "global_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0})
    base.exclusive(args.output, base.canonical(output) + b"\n")
    print(json.dumps({"output": str(args.output), "object_sha256": output["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
