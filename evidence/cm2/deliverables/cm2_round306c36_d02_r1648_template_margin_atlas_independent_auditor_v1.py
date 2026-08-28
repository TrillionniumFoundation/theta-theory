#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SCHEMA = "cm2.round306c36.d02-r1648-template-margin-atlas.v1"
AUDIT_SCHEMA = "cm2.round306c36.d02-r1648-template-margin-atlas-independent-audit.v1"
EXPECTED_STATUS = (
    "PASS_C36_DUAL_SEED_COLLAR_TEMPLATE_MARGIN_ATLAS__"
    "137_OF_137_GEOMETRY_TEMPLATES__197_OF_197_WORD_STRATA__"
    "1648_OF_1648_OCCURRENCES__C34_COMMON_REFINEMENT_ZERO"
)
EXPECTED_C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_ROUND139_FILE = "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
EXPECTED_ROUND139_RESULT = "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
RETURN_DEPTH = 1648
MARGIN_FIELDS = (
    "retained_candidate_minimum_decision_margin_dyadic_depth",
    "retained_candidate_minimum_winner_gap_dyadic_depth",
    "full_radius4_candidate_minimum_decision_margin_dyadic_depth",
    "full_radius4_candidate_minimum_winner_gap_dyadic_depth",
    "official_wall_crossing_time_endpoint_margin_dyadic_depth",
    "official_wall_endpoint_integer_margin_dyadic_depth",
    "official_wall_event_order_gap_dyadic_depth",
    "outgoing_chart_margin_dyadic_depth",
    "C24_minimum_inside_or_exclusion_margin_dyadic_depth",
    "homogeneity_lower_margin_dyadic_depth",
    "homogeneity_upper_margin_dyadic_depth",
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{path}:{key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda item: (_ for _ in ()).throw(ValueError(item)),
        parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)),
    )
    require(type(value) is dict, f"top object:{path}")
    return value


def validate_object(
    value: dict[str, Any], field: str, expected: str | None, label: str,
) -> str:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(type(recorded) is str and recorded == digest(semantic), f"object:{label}")
    if expected is not None:
        require(recorded == expected, f"expected object:{label}")
    return recorded


def validate_manifest(directory: Path, expected_names: set[str] | None = None) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"duplicate manifest member:{name}")
        names.append(name)
        require(
            (directory / name).is_file()
            and file_sha256(directory / name) == expected,
            f"manifest member:{name}",
        )
    require(names == sorted(names), "manifest order")
    if expected_names is not None:
        require(set(names) == expected_names, "manifest inventory")


def read_ledger(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    require(
        path.is_file()
        and path.stat().st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger bytes:{path}",
    )
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            semantic = dict(row)
            row_sha = semantic.pop("row_sha256", None)
            require(row_sha == digest(semantic), f"row closure:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(
        len(rows) == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor:{path}",
    )
    return rows


def round139_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    path = DELIVERABLES / (
        "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
        "2026-07-24.json"
    )
    require(file_sha256(path) == EXPECTED_ROUND139_FILE, "Round139 file pin")
    envelope = strict_json(path)
    require(
        envelope.get("result_sha256") == EXPECTED_ROUND139_RESULT
        and digest(envelope.get("result")) == EXPECTED_ROUND139_RESULT,
        "Round139 envelope",
    )
    result = envelope["result"]
    graph = result["collision_rows"]
    cylinder = result["positive_area_collision_rows"]
    require(
        len(graph) == len(cylinder) == RETURN_DEPTH
        and digest(graph) == result["collision_rows_sha256"]
        and digest(cylinder) == result["positive_area_collision_rows_sha256"],
        "Round139 dual rows",
    )
    return graph, cylinder


def margin_vector(row: dict[str, Any]) -> dict[str, Any]:
    return {field: row[field] for field in MARGIN_FIELDS}


def summarize_margins(
    rows: list[dict[str, Any]], collar: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in MARGIN_FIELDS:
        values = [row["collar_margin_vectors"][collar][field] for row in rows]
        finite = [value for value in values if value is not None]
        result[field] = {
            "finite_occurrence_count": len(finite),
            "null_inapplicable_occurrence_count": len(values) - len(finite),
            "minimum_dyadic_depth": min(finite) if finite else None,
            "maximum_dyadic_depth": max(finite) if finite else None,
        }
    return result


def validate_candidate(candidate: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    expected_names = {
        "SEED_COLLAR_ONLY.lock",
        "component_refinement_obligations.jsonl.gz",
        "occurrence_margin_bindings.jsonl.gz",
        "result.json",
        "template_margin_atlas.jsonl.gz",
        "word_stratum_margin_atlas.jsonl.gz",
    }
    validate_manifest(candidate, expected_names)
    result = strict_json(candidate / "result.json")
    object_sha = validate_object(result, "object_sha256", None, "C36")
    require(
        result.get("schema") == SCHEMA
        and result.get("status") == EXPECTED_STATUS,
        "C36 envelope",
    )
    lock = (candidate / "SEED_COLLAR_ONLY.lock").read_text(encoding="utf-8")
    require(
        "zero C34 common-refinement" in lock
        and "D02" in lock
        and "CM2" in lock,
        "C36 lock",
    )
    c35_path = ROOT / result["C35_authority"]["path"]
    validate_manifest(c35_path)
    c35_result = strict_json(c35_path / "result.json")
    validate_object(c35_result, "object_sha256", EXPECTED_C35_OBJECT, "C35")
    c34_path = ROOT / result["C34_authority"]["path"]
    validate_manifest(c34_path)
    c34_result = strict_json(c34_path / "result.json")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")

    c35_geometry = read_ledger(
        c35_path, c35_result["ledgers"]["geometry_transition_templates"]
    )
    c35_words = read_ledger(
        c35_path, c35_result["ledgers"]["official_word_variants"]
    )
    c35_occurrences = read_ledger(
        c35_path, c35_result["ledgers"]["path_occurrences"]
    )
    c34_components = read_ledger(
        c34_path, c34_result["ledgers"]["ordinary_components"]
    )
    templates = read_ledger(
        candidate, result["ledgers"]["template_margin_atlas"]
    )
    words = read_ledger(
        candidate, result["ledgers"]["word_stratum_margin_atlas"]
    )
    bindings = read_ledger(
        candidate, result["ledgers"]["occurrence_margin_bindings"]
    )
    obligations = read_ledger(
        candidate, result["ledgers"]["component_refinement_obligations"]
    )
    direct_graph, direct_positive_area = round139_rows()
    require(
        len(templates) == len(c35_geometry) == 137
        and len(words) == len(c35_words) == 197
        and len(bindings) == len(c35_occurrences)
        == len(direct_graph) == len(direct_positive_area) == RETURN_DEPTH
        and len(obligations) == len(c34_components) == 26,
        "ledger census",
    )

    by_template: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_word: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, (binding, source, graph_row, positive_area_row) in enumerate(
        zip(
            bindings,
            c35_occurrences,
            direct_graph,
            direct_positive_area,
            strict=True,
        ),
        start=1,
    ):
        semantic_fields = (
            "collision_index",
            "incoming_absolute_owner_id",
            "selected_absolute_owner_id",
            "relative_frozen_target_id",
            "official_word_key",
            "ordered_clean_wall_record",
            "outgoing_chart",
            "C24_classification",
            "destination_core_id",
            "homogeneity_label",
            "incidence_rank_B",
        )
        require(
            all(
                graph_row[field] == positive_area_row[field]
                for field in semantic_fields
            ),
            f"dual semantic projection:{index}",
        )
        expected_vectors = {
            "exact_half_open_graph": margin_vector(graph_row),
            "positive_area_rectangle": margin_vector(positive_area_row),
        }
        expected_candidate_census = {
            "exact_half_open_graph": {
                "retained_candidate_count": graph_row["retained_candidate_count"],
                "full_radius4_candidate_count":
                    graph_row["full_radius4_candidate_count"],
                "official_wall_ordered_crossing_count":
                    graph_row["official_wall_ordered_crossing_count"],
            },
            "positive_area_rectangle": {
                "retained_candidate_count":
                    positive_area_row["retained_candidate_count"],
                "full_radius4_candidate_count":
                    positive_area_row["full_radius4_candidate_count"],
                "official_wall_ordered_crossing_count":
                    positive_area_row["official_wall_ordered_crossing_count"],
            },
        }
        require(
            binding["collision_index"] == source["collision_index"] == index
            and binding["geometry_template_id"] == source["geometry_template_id"]
            and binding["official_word_variant_id"]
            == source["official_word_variant_id"]
            and binding["selected_absolute_owner_id"]
            == source["selected_absolute_owner_id"]
            and binding["official_word_key_id"]
            == graph_row["official_word_key"]["official_word_key_id"]
            and binding["official_registry_row_sha256"]
            == graph_row["official_word_key"]["registry_row_sha256"]
            and source["graph_row_sha256"] == graph_row["row_sha256"]
            and source["positive_area_row_sha256"]
            == positive_area_row["row_sha256"]
            and binding["collar_margin_vectors"] == expected_vectors
            and binding["collar_margin_vectors_sha256"] == digest(expected_vectors)
            and binding["collar_candidate_census"] == expected_candidate_census
            and binding["owner_discriminant_root_order_word_chart_core_map_status"]
            == "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS"
            and binding["C34_common_refinement_credit"] == 0
            and binding["D02_credit"] == 0,
            f"binding reconstruction:{index}",
        )
        by_template[binding["geometry_template_id"]].append(binding)
        by_word[binding["official_word_variant_id"]].append(binding)

    for atlas, source in zip(templates, c35_geometry, strict=True):
        rows = by_template[source["geometry_template_id"]]
        indices = [row["collision_index"] for row in rows]
        require(
            atlas["geometry_template_id"] == source["geometry_template_id"]
            and atlas["occurrence_count"] == source["occurrence_count"]
            and atlas["occurrence_indices"] == source["occurrence_indices"] == indices
            and atlas["margin_field_census_by_collar"] == {
                collar: summarize_margins(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            }
            and atlas["occurrence_collar_margin_vector_sequence_sha256"]
            == digest([row["collar_margin_vectors_sha256"] for row in rows])
            and all(
                atlas[field] is True
                for field in (
                    "owner_candidate_discriminant_map_materialized",
                    "near_root_order_map_materialized",
                    "official_word_map_materialized",
                    "outgoing_chart_map_materialized",
                    "C24_core_map_materialized",
                )
            )
            and atlas["atlas_scope"] == "DUAL_R139_SEED_COLLARS_ONLY"
            and atlas["C34_common_refinement_credit"] == 0
            and atlas["D02_credit"] == 0,
            f"template reconstruction:{atlas['geometry_template_id']}",
        )

    for atlas, source in zip(words, c35_words, strict=True):
        rows = by_word[source["official_word_variant_id"]]
        indices = [row["collision_index"] for row in rows]
        require(
            atlas["official_word_variant_id"]
            == source["official_word_variant_id"]
            and atlas["official_registry_row"] == source["official_registry_row"]
            and atlas["official_registry_row_sha256"]
            == source["official_registry_row_sha256"]
            and atlas["occurrence_indices"] == source["occurrence_indices"] == indices
            and atlas["margin_field_census_by_collar"] == {
                collar: summarize_margins(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            }
            and atlas["word_stratum_scope"] == "DUAL_R139_SEED_COLLARS_ONLY"
            and atlas["C34_common_refinement_credit"] == 0
            and atlas["D02_credit"] == 0,
            f"word reconstruction:{atlas['official_word_variant_id']}",
        )

    for obligation, source in zip(obligations, c34_components, strict=True):
        cells = source["cell_count"]
        require(
            obligation["component_id"] == source["component_id"]
            and obligation["cell_count"] == cells
            and obligation["cell_ids_sha256"] == source["cell_ids_sha256"]
            and obligation["geometry_template_count"] == 137
            and obligation["official_word_variant_count"] == 197
            and obligation["R1648_occurrence_count"] == RETURN_DEPTH
            and obligation["cell_occurrence_refinement_obligation_count"]
            == cells * RETURN_DEPTH
            and obligation["cell_geometry_template_obligation_count"]
            == cells * 137
            and obligation["cell_word_variant_obligation_count"]
            == cells * 197
            and obligation["common_refinement_status"] == "NOT_MATERIALIZED"
            and obligation["D02_credit"] == 0,
            f"component obligation:{source['component_id']}",
        )

    summary = {
        "templates": len(templates),
        "words": len(words),
        "occurrences": len(bindings),
        "components": len(obligations),
        "cells": sum(row["cell_count"] for row in obligations),
        "cell_occurrence_obligations": sum(
            row["cell_occurrence_refinement_obligation_count"]
            for row in obligations
        ),
        "cell_geometry_obligations": sum(
            row["cell_geometry_template_obligation_count"]
            for row in obligations
        ),
        "cell_word_obligations": sum(
            row["cell_word_variant_obligation_count"] for row in obligations
        ),
        "scope": result["map_stage_census"]["scope"],
        "common_refined": result["strict_nonpromotion"]
        ["C34_common_refined_cell_count"],
        "unresolved": result["strict_nonpromotion"]
        ["C34_unresolved_R1648_continuations"],
        "unresolved_zero": result["strict_nonpromotion"]
        ["four_class_terminal_census_unresolved_zero"],
        "D02": result["strict_nonpromotion"]["D02"],
    }
    validate_summary(summary)
    require(
        result["atlas_census"] == {
            "geometry_templates_materialized_on_dual_seed_collars": 137,
            "official_word_strata_materialized_on_dual_seed_collars": 197,
            "occurrence_margin_bindings": 1648,
            "ordinary_components_awaiting_common_refinement": 26,
            "ordinary_cells_awaiting_common_refinement": 1724,
            "cell_occurrence_refinement_obligations": 2841152,
            "cell_geometry_template_obligations": 236188,
            "cell_word_variant_obligations": 339628,
        },
        "result atlas census",
    )
    return result, {
        "candidate_object_sha256": object_sha,
        "summary": summary,
        "ledger_sha256": {
            key: value["sha256"] for key, value in result["ledgers"].items()
        },
    }


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["templates"] == 137, "summary templates")
    require(summary["words"] == 197, "summary words")
    require(summary["occurrences"] == 1648, "summary occurrences")
    require(summary["components"] == 26, "summary components")
    require(summary["cells"] == 1724, "summary cells")
    require(
        summary["cell_occurrence_obligations"] == 2841152,
        "summary occurrence obligations",
    )
    require(summary["cell_geometry_obligations"] == 236188, "summary geometry")
    require(summary["cell_word_obligations"] == 339628, "summary words obligations")
    require(summary["scope"] == "DUAL_R139_SEED_COLLARS_ONLY", "summary scope")
    require(summary["common_refined"] == 0, "summary common refinement")
    require(summary["unresolved"] == 1724, "summary unresolved")
    require(summary["unresolved_zero"] is False, "summary unresolved zero")
    require(
        summary["D02"] == "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
        "summary D02",
    )


def hostile_attacks(summary: dict[str, Any]) -> dict[str, str]:
    mutations = {
        "template_count_tamper": ("templates", 136),
        "word_count_tamper": ("words", 196),
        "occurrence_count_tamper": ("occurrences", 1647),
        "component_count_tamper": ("components", 25),
        "cell_count_tamper": ("cells", 1723),
        "occurrence_obligation_tamper": ("cell_occurrence_obligations", 2841151),
        "geometry_obligation_tamper": ("cell_geometry_obligations", 236187),
        "word_obligation_tamper": ("cell_word_obligations", 339627),
        "scope_expansion": ("scope", "ALL_C34_CELLS"),
        "false_common_refinement": ("common_refined", 1724),
        "false_unresolved_decrement": ("unresolved", 1723),
        "false_unresolved_zero": ("unresolved_zero", True),
        "illegal_D02_authorization": ("D02", "AUTHORIZED"),
        "illegal_D02_clearance": ("D02", "CLEARED"),
    }
    results: dict[str, str] = {}
    for name, (field, value) in mutations.items():
        mutated = copy.deepcopy(summary)
        mutated[field] = value
        try:
            validate_summary(mutated)
        except Exception:
            results[name] = "FAIL_CLOSED"
        else:
            raise RuntimeError(f"attack accepted:{name}")
    return results


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".stage-{os.getpid()}")
    temporary.write_bytes(canonical(value) + b"\n")
    temporary.replace(path)


def audit(candidate: Path, output: Path) -> dict[str, Any]:
    result, reconstruction = validate_candidate(candidate.resolve())
    attacks = hostile_attacks(reconstruction["summary"])
    require(len(attacks) == 14 and set(attacks.values()) == {"FAIL_CLOSED"}, "attacks")
    receipt: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "status": "PASS_INDEPENDENT_C36_RECONSTRUCTION__14_OF_14_ATTACKS_FAIL_CLOSED",
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": reconstruction["candidate_object_sha256"],
        "candidate_status": result["status"],
        "independently_reconstructed_summary": reconstruction["summary"],
        "candidate_ledger_sha256": reconstruction["ledger_sha256"],
        "hostile_attacks": attacks,
        "strict_nonpromotion": result["strict_nonpromotion"],
    }
    receipt["object_sha256"] = digest(receipt)
    write_json_atomic(output.resolve(), receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.candidate, args.output)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
