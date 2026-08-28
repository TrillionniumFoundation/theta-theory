#!/usr/bin/env python3
"""Higher-precision closed-schema verifier for the outward-port frontier."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_round85_rank3_outward_port_continuation_frontier_cert as certificate
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "cm2-round85-rank3-outward-port-continuation-frontier-2026-07-22.json"
TOP_KEYS = {"schema", "result", "result_sha256"}
RESULT_KEYS = {
    "fixed_parameter", "precision_bits", "input_registered_port_count", "input_source_boundary_port_count",
    "input_non_source_registered_port_count", "classified_non_source_port_count",
    "outward_cell_lookup_definition",
    "outward_cell_classification_histogram", "same_candidate_same_second_branch_seed_count",
    "preliminary_read_only_partition_2588_428_196_reproduced", "preliminary_partition_status",
    "same_candidate_different_second_branch_seed_count", "subgrid_exposed_edge_count",
    "root_on_physical_grid_line_count", "strict_grid_cut_test_count", "reverse_tangent_action_histogram",
    "signed_transverse_tangency_factor_histogram", "oriented_line_projective_chart_histogram",
    "continuation_frontier_rows", "continuation_frontier_rows_sha256", "strict_scope", "strict_nonclaims",
    "upstream_pins",
}
ROW_KEYS = {
    "continuation_frontier_id", "registered_port_id", "physical_root_component_id", "source_core_index",
    "second_selected_target_id", "second_outgoing_chart", "third_candidate_id", "boundary_axis",
    "fixed_coordinate", "inside_side", "fixed_grid_line_index", "root_grid_isolation", "outward_grid_cell",
    "outward_dyadic_path", "outward_cell_box", "outward_seed_count", "outward_seed_rows",
    "outward_seed_rows_sha256", "outward_cell_classification", "typed_physical_event_frontier",
    "next_certification_action", "reverse_tangent_continuation_input",
}
ISOLATION_KEYS = {
    "parameter_axis", "input_root_bracket", "isolated_root_bracket", "isolated_endpoint_signs",
    "parameter_grid_cell_index", "strict_grid_cut_test_count", "grid_cut_rows", "grid_cut_rows_sha256",
}
CUT_KEYS = {"cut_coordinate", "cut_sign"}
SEED_KEYS = {
    "dyadic_path", "source_box", "blocker", "carrier", "second_selected_target_id", "second_outgoing_chart",
}
REVERSE_KEYS = {
    "source_core_index", "second_selected_target_id", "second_outgoing_chart", "third_candidate_id",
    "source_coordinate_box", "signed_transverse_tangency_factor", "signed_transverse_sign",
    "oriented_line_projective_chart", "projective_chart_denominator",
    "projective_chart_denominator_strictly_positive",
}
SOURCE_BOX_KEYS = {"fixed_axis", "fixed_coordinate", "parameter_axis", "parameter_interval"}
PIN_KEYS = {
    "round85_registered_arc_port_manifest_sha256", "round82_sha256_ledger_sha256",
    "round80_sha256_ledger_sha256", "rank3_physical_patch_atlas_sha256",
    "rank3_cross_tube_joins_sha256", "time3_carrier_geometry_sha256",
}


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def keys(row: dict[str, Any], expected: set[str], label: str) -> None:
    if set(row) != expected:
        raise ValueError(f"non-closed {label} schema")


def closed_schema(document: dict[str, Any]) -> None:
    keys(document, TOP_KEYS, "top-level")
    if document["schema"] != "cm2.round85.rank3-outward-port-continuation-frontier.v1":
        raise ValueError("schema")
    result = document["result"]
    keys(result, RESULT_KEYS, "result")
    keys(result["upstream_pins"], PIN_KEYS, "upstream pin")
    if document["result_sha256"] != digest(result):
        raise ValueError("result digest")
    if result["continuation_frontier_rows_sha256"] != digest(result["continuation_frontier_rows"]):
        raise ValueError("frontier row digest")
    identifiers = set()
    ports = set()
    for row in result["continuation_frontier_rows"]:
        keys(row, ROW_KEYS, "frontier row")
        keys(row["root_grid_isolation"], ISOLATION_KEYS, "root-grid isolation")
        keys(row["outward_cell_box"], {"t", "p"}, "outward cell box")
        keys(row["reverse_tangent_continuation_input"], REVERSE_KEYS, "reverse input")
        keys(row["reverse_tangent_continuation_input"]["source_coordinate_box"], SOURCE_BOX_KEYS, "source coordinate box")
        isolation = row["root_grid_isolation"]
        if isolation["grid_cut_rows_sha256"] != digest(isolation["grid_cut_rows"]):
            raise ValueError("grid-cut row digest")
        for cut in isolation["grid_cut_rows"]:
            keys(cut, CUT_KEYS, "grid cut")
        if row["outward_seed_rows_sha256"] != digest(row["outward_seed_rows"]):
            raise ValueError("seed row digest")
        if row["outward_seed_count"] != len(row["outward_seed_rows"]):
            raise ValueError("seed row count")
        for seed in row["outward_seed_rows"]:
            keys(seed, SEED_KEYS, "seed evidence")
            keys(seed["source_box"], {"t", "p"}, "seed source box")
        if row["continuation_frontier_id"] in identifiers or row["registered_port_id"] in ports:
            raise ValueError("duplicate frontier or port identifier")
        identifiers.add(row["continuation_frontier_id"])
        ports.add(row["registered_port_id"])


def expected_document() -> dict[str, Any]:
    expected = certificate.build(precision_bits=768)
    expected["result"]["precision_bits"] = 384
    expected["result_sha256"] = digest(expected["result"])
    return expected


def validate(document: dict[str, Any], expected: dict[str, Any]) -> None:
    closed_schema(document)
    if document != expected:
        raise ValueError("candidate differs from the 768-bit recomputation")


def coordinated_digest(document: dict[str, Any]) -> None:
    result = document["result"]
    for row in result["continuation_frontier_rows"]:
        row["root_grid_isolation"]["grid_cut_rows_sha256"] = digest(row["root_grid_isolation"]["grid_cut_rows"])
        row["outward_seed_rows_sha256"] = digest(row["outward_seed_rows"])
    result["continuation_frontier_rows_sha256"] = digest(result["continuation_frontier_rows"])
    document["result_sha256"] = digest(result)


def hostile_audit(original: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    attacks = []
    document = copy.deepcopy(original)
    document["result"]["outward_cell_classification_histogram"]["NO_UNRESOLVED_SEED_REGISTERED"] -= 1
    coordinated_digest(document)
    attacks.append(("classification scalar", document))
    document = copy.deepcopy(original)
    document["result"]["continuation_frontier_rows"][0]["outward_grid_cell"][0] += 1
    coordinated_digest(document)
    attacks.append(("outward cell", document))
    document = copy.deepcopy(original)
    document["result"]["continuation_frontier_rows"][0]["next_certification_action"] = "CERTIFIED_ENDPOINT"
    coordinated_digest(document)
    attacks.append(("continuation action", document))
    document = copy.deepcopy(original)
    document["result"]["continuation_frontier_rows"][0]["reverse_tangent_continuation_input"]["signed_transverse_sign"] *= -1
    coordinated_digest(document)
    attacks.append(("tangency factor", document))
    document = copy.deepcopy(original)
    document["result"]["upstream_pins"]["round80_sha256_ledger_sha256"] = "0" * 64
    coordinated_digest(document)
    attacks.append(("Round-80 ledger pin", document))
    document = copy.deepcopy(original)
    document["result"]["strict_nonclaims"].append("1606 complete gaps")
    coordinated_digest(document)
    attacks.append(("gap-count claim injection", document))
    rejected = []
    for label, document in attacks:
        try:
            validate(document, expected)
        except Exception:
            rejected.append(label)
    if len(rejected) != len(attacks):
        raise ValueError("hostile mutation accepted")
    return {"attempted": len(attacks), "rejected": len(rejected), "rejected_labels": rejected}


def strict_json_audit(text: str) -> dict[str, Any]:
    attacks = {
        "duplicate_top_level": text.replace('"schema":', '"schema": "shadow", "schema":', 1),
        "duplicate_nested": text.replace('"fixed_parameter":', '"fixed_parameter": "shadow", "fixed_parameter":', 1),
        "nan": text.replace('"precision_bits": 384', '"precision_bits": NaN', 1),
        "infinity": text.replace('"precision_bits": 384', '"precision_bits": Infinity', 1),
    }
    rejected = []
    for label, payload in attacks.items():
        try:
            strict_load_text(payload)
        except Exception:
            rejected.append(label)
    if len(rejected) != len(attacks):
        raise ValueError("strict JSON attack accepted")
    return {"attempted": len(attacks), "rejected": len(rejected), "rejected_labels": rejected}


def main() -> int:
    text = CANDIDATE.read_text()
    document = strict_load_text(text)
    expected = expected_document()
    validate(document, expected)
    result = {
        "status": "PASS",
        "candidate_sha256": file_sha256(CANDIDATE),
        "candidate_result_sha256": document["result_sha256"],
        "producer_precision_bits": 384,
        "higher_precision_recomputation_bits": 768,
        "higher_precision_row_recomputation": "3212/3212_EXACT",
        "higher_precision_outward_partition": document["result"]["outward_cell_classification_histogram"],
        "higher_precision_tangency_factor_partition": document["result"]["signed_transverse_tangency_factor_histogram"],
        "semantic_hostile_mutation_audit": hostile_audit(document, expected),
        "strict_json_attack_audit": strict_json_audit(text),
        "strict_scope": "outward-cell and reverse-tangent-input frontier only; no port pairing, physical endpoint or gap count is certified",
    }
    audit = {"schema": "cm2.round85.rank3-outward-port-continuation-frontier-audit.v1", "result": result, "result_sha256": digest(result)}
    json.dump(audit, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
