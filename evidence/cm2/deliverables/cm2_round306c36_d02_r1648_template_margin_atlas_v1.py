#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c36.d02-r1648-template-margin-atlas.v1"
TEMPLATE_SCHEMA = "cm2.round306c36.r1648-template-margin-atlas-row.v1"
WORD_SCHEMA = "cm2.round306c36.r1648-word-stratum-margin-atlas-row.v1"
OCCURRENCE_SCHEMA = "cm2.round306c36.r1648-occurrence-margin-binding-row.v1"
OBLIGATION_SCHEMA = "cm2.round306c36.component-refinement-obligation-row.v1"

ROUND139 = DELIVERABLES / (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
EXPECTED_ROUND139_FILE = "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
EXPECTED_ROUND139_RESULT = "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C35_OBJECT = "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"
EXPECTED_C35_AUDIT_OBJECT = (
    "914b1440a311a922819e488e4ed4ef39cb87df74b884f2fe7821336f7cb8d33a"
)
EXPECTED_C35_STATUS = (
    "PASS_C35_R1648_TRANSITION_REGISTRY__137_GEOMETRY_TEMPLATES__"
    "197_OFFICIAL_WORD_VARIANTS__1648_OCCURRENCES__ZERO_D02_CREDIT"
)
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
    value: dict[str, Any], field: str, expected: str, label: str,
) -> None:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(recorded == expected == digest(semantic), f"object:{label}")


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    require(rows, f"manifest nonempty:{directory}")
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"manifest duplicate:{directory}:{name}")
        names.append(name)
        path = directory / name
        require(
            path.is_file() and file_sha256(path) == expected,
            f"manifest member:{path}",
        )
    require(names == sorted(names), f"manifest order:{directory}")


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


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> LedgerWriter:
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, mtime=0
        )
        return self

    def write(self, row: dict[str, Any]) -> None:
        require("row_sha256" not in row, "writer row open")
        row_sha = digest(row)
        self.stream.write(canonical({**row, "row_sha256": row_sha}) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


def load_authorities(
    c35: Path, c35_audit: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(file_sha256(ROUND139) == EXPECTED_ROUND139_FILE, "Round139 file pin")
    envelope = strict_json(ROUND139)
    require(
        envelope.get("result_sha256") == EXPECTED_ROUND139_RESULT
        and digest(envelope.get("result")) == EXPECTED_ROUND139_RESULT,
        "Round139 envelope",
    )
    validate_manifest(c35)
    c35_result = strict_json(c35 / "result.json")
    validate_object(c35_result, "object_sha256", EXPECTED_C35_OBJECT, "C35")
    require(c35_result.get("status") == EXPECTED_C35_STATUS, "C35 status")
    audit = strict_json(c35_audit)
    validate_object(
        audit, "object_sha256", EXPECTED_C35_AUDIT_OBJECT, "C35 audit"
    )
    require(
        audit.get("candidate_object_sha256") == EXPECTED_C35_OBJECT
        and audit.get("status")
        == "PASS_INDEPENDENT_C35_RECONSTRUCTION__10_OF_10_ATTACKS_FAIL_CLOSED",
        "C35 audit binding",
    )
    c34_path = ROOT / c35_result["C34_authority"]["path"]
    validate_manifest(c34_path)
    c34_result = strict_json(c34_path / "result.json")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")
    require(
        c34_result["round144_terminal_census"]
        ["UNRESOLVED_R1648_CONTINUATION"] == 1724,
        "C34 unresolved census",
    )
    return envelope["result"], c35_result, c34_result


def margin_vector(row: dict[str, Any]) -> dict[str, Any]:
    vector = {field: row[field] for field in MARGIN_FIELDS}
    require(
        all(value is None or type(value) is int for value in vector.values()),
        "margin value types",
    )
    crossing_count = row["official_wall_ordered_crossing_count"]
    require(
        (vector["official_wall_crossing_time_endpoint_margin_dyadic_depth"] is None)
        == (crossing_count == 0),
        "wall endpoint margin applicability",
    )
    require(
        (vector["official_wall_event_order_gap_dyadic_depth"] is None)
        == (crossing_count < 2),
        "wall order margin applicability",
    )
    require(
        vector["homogeneity_upper_margin_dyadic_depth"] is None,
        "H0 upper margin inapplicable",
    )
    return vector


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


def build_occurrence_rows(
    round139: dict[str, Any], c35: Path, c35_result: dict[str, Any],
) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]],
]:
    graph = round139["collision_rows"]
    cylinder = round139["positive_area_collision_rows"]
    require(
        len(graph) == len(cylinder) == RETURN_DEPTH
        and digest(graph) == round139["collision_rows_sha256"]
        and digest(cylinder) == round139["positive_area_collision_rows_sha256"],
        "Round139 rows",
    )
    summaries = (
        round139["local_first_return_summary"],
        round139["positive_area_first_return_summary"],
    )
    for summary in summaries:
        require(
            summary["all_official_words_whole_collar_strict"] is True
            and summary["all_other_owner_decisions_whole_collar_strict"] is True
            and summary["all_homogeneity_and_incidence_decisions_whole_collar_strict"]
            is True,
            "Round139 strict whole-collar summary",
        )
    geometry = read_ledger(
        c35, c35_result["ledgers"]["geometry_transition_templates"]
    )
    words = read_ledger(c35, c35_result["ledgers"]["official_word_variants"])
    occurrences = read_ledger(c35, c35_result["ledgers"]["path_occurrences"])
    require(
        len(geometry) == 137
        and len(words) == 197
        and len(occurrences) == RETURN_DEPTH,
        "C35 ledger census",
    )
    bindings: list[dict[str, Any]] = []
    for index, (left, right, source) in enumerate(
        zip(graph, cylinder, occurrences, strict=True), start=1
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
            all(left[field] == right[field] for field in semantic_fields),
            f"dual Round139 semantic projection:{index}",
        )
        require(
            source["collision_index"] == index
            and source["graph_row_sha256"] == left["row_sha256"]
            and source["positive_area_row_sha256"] == right["row_sha256"]
            and source["selected_absolute_owner_id"]
            == left["selected_absolute_owner_id"]
            and source["relative_frozen_target_id"]
            == left["relative_frozen_target_id"]
            and source["outgoing_chart"] == left["outgoing_chart"]
            and source["official_word_key_id"]
            == left["official_word_key"]["official_word_key_id"],
            f"C35 occurrence binding:{index}",
        )
        graph_vector = margin_vector(left)
        positive_area_vector = margin_vector(right)
        collar_vectors = {
            "exact_half_open_graph": graph_vector,
            "positive_area_rectangle": positive_area_vector,
        }
        bindings.append({
            "schema": OCCURRENCE_SCHEMA,
            "collision_index": index,
            "geometry_template_id": source["geometry_template_id"],
            "official_word_variant_id": source["official_word_variant_id"],
            "incoming_absolute_owner_id": source["incoming_absolute_owner_id"],
            "selected_absolute_owner_id": source["selected_absolute_owner_id"],
            "incoming_chart": source["incoming_chart"],
            "outgoing_chart": source["outgoing_chart"],
            "relative_frozen_target_id": source["relative_frozen_target_id"],
            "official_word_key_id": source["official_word_key_id"],
            "official_registry_row_sha256":
                left["official_word_key"]["registry_row_sha256"],
            "ordered_clean_wall_record_sha256":
                digest(left["ordered_clean_wall_record"]),
            "collar_candidate_census": {
                "exact_half_open_graph": {
                    "retained_candidate_count": left["retained_candidate_count"],
                    "full_radius4_candidate_count":
                        left["full_radius4_candidate_count"],
                    "official_wall_ordered_crossing_count":
                        left["official_wall_ordered_crossing_count"],
                },
                "positive_area_rectangle": {
                    "retained_candidate_count": right["retained_candidate_count"],
                    "full_radius4_candidate_count":
                        right["full_radius4_candidate_count"],
                    "official_wall_ordered_crossing_count":
                        right["official_wall_ordered_crossing_count"],
                },
            },
            "homogeneity_label": left["homogeneity_label"],
            "incidence_rank_B": left["incidence_rank_B"],
            "C24_classification": left["C24_classification"],
            "destination_core_id": left["destination_core_id"],
            "collar_margin_vectors": collar_vectors,
            "collar_margin_vectors_sha256": digest(collar_vectors),
            "dual_Round139_collar_semantic_projection_equal": True,
            "owner_discriminant_root_order_word_chart_core_map_status":
                "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    return geometry, words, bindings


def materialize_template_rows(
    geometry: list[dict[str, Any]], bindings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in bindings:
        grouped[row["geometry_template_id"]].append(row)
    result: list[dict[str, Any]] = []
    for source in geometry:
        template_id = source["geometry_template_id"]
        rows = sorted(grouped[template_id], key=lambda row: row["collision_index"])
        indices = [row["collision_index"] for row in rows]
        require(
            indices == source["occurrence_indices"]
            and len(rows) == source["occurrence_count"],
            f"geometry occurrences:{template_id}",
        )
        result.append({
            "schema": TEMPLATE_SCHEMA,
            "geometry_template_id": template_id,
            "source_obstacle": source["source_obstacle"],
            "incoming_chart": source["incoming_chart"],
            "relative_frozen_target_id": source["relative_frozen_target_id"],
            "target_obstacle": source["target_obstacle"],
            "outgoing_chart": source["outgoing_chart"],
            "occurrence_count": len(rows),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "official_word_variant_count": source["official_word_variant_count"],
            "official_word_variant_ids_sha256":
                source["official_word_variant_ids_sha256"],
            "contains_collision_2": source["contains_collision_2"],
            "occurrence_collar_margin_vector_sequence_sha256": digest(
                [row["collar_margin_vectors_sha256"] for row in rows]
            ),
            "margin_field_census_by_collar": {
                collar: summarize_margins(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            },
            "owner_candidate_discriminant_map_materialized": True,
            "near_root_order_map_materialized": True,
            "official_word_map_materialized": True,
            "outgoing_chart_map_materialized": True,
            "C24_core_map_materialized": True,
            "atlas_scope": "DUAL_R139_SEED_COLLARS_ONLY",
            "template_atlas_status": "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    require(len(result) == 137, "template atlas count")
    return result


def materialize_word_rows(
    words: list[dict[str, Any]], bindings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in bindings:
        grouped[row["official_word_variant_id"]].append(row)
    result: list[dict[str, Any]] = []
    for source in words:
        word_id = source["official_word_variant_id"]
        rows = sorted(grouped[word_id], key=lambda row: row["collision_index"])
        indices = [row["collision_index"] for row in rows]
        require(
            indices == source["occurrence_indices"]
            and len(rows) == source["occurrence_count"]
            and all(
                row["official_registry_row_sha256"]
                == source["official_registry_row_sha256"]
                for row in rows
            ),
            f"word occurrences:{word_id}",
        )
        result.append({
            "schema": WORD_SCHEMA,
            "official_word_variant_id": word_id,
            "geometry_template_id": source["geometry_template_id"],
            "source_obstacle": source["source_obstacle"],
            "incoming_chart": source["incoming_chart"],
            "relative_frozen_target_id": source["relative_frozen_target_id"],
            "outgoing_chart": source["outgoing_chart"],
            "official_registry_row": source["official_registry_row"],
            "official_registry_row_sha256":
                source["official_registry_row_sha256"],
            "occurrence_count": len(rows),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "occurrence_collar_margin_vector_sequence_sha256": digest(
                [row["collar_margin_vectors_sha256"] for row in rows]
            ),
            "margin_field_census_by_collar": {
                collar: summarize_margins(rows, collar)
                for collar in ("exact_half_open_graph", "positive_area_rectangle")
            },
            "official_word_endpoint_and_order_map_materialized": True,
            "word_stratum_scope": "DUAL_R139_SEED_COLLARS_ONLY",
            "word_stratum_status": "MATERIALIZED_ON_DUAL_R139_SEED_COLLARS",
            "C34_common_refinement_credit": 0,
            "D02_credit": 0,
        })
    require(len(result) == 197, "word atlas count")
    return result


def build_obligations(
    c34_path: Path, c34_result: dict[str, Any],
) -> list[dict[str, Any]]:
    components = read_ledger(
        c34_path, c34_result["ledgers"]["ordinary_components"]
    )
    require(
        len(components) == 26
        and sum(row["cell_count"] for row in components) == 1724,
        "C34 component obligations",
    )
    rows: list[dict[str, Any]] = []
    for source in components:
        cell_count = source["cell_count"]
        rows.append({
            "schema": OBLIGATION_SCHEMA,
            "component_id": source["component_id"],
            "component_index": source["component_index"],
            "contains_R1648_seed_coarse_cell":
                source["contains_R1648_seed_coarse_cell"],
            "cell_count": cell_count,
            "cell_ids_sha256": source["cell_ids_sha256"],
            "chart_census": source["chart_census"],
            "adjacent_typed_event_cell_count":
                source["adjacent_typed_event_cell_count"],
            "geometry_template_count": 137,
            "official_word_variant_count": 197,
            "R1648_occurrence_count": RETURN_DEPTH,
            "cell_occurrence_refinement_obligation_count":
                cell_count * RETURN_DEPTH,
            "cell_geometry_template_obligation_count": cell_count * 137,
            "cell_word_variant_obligation_count": cell_count * 197,
            "common_refinement_status": "NOT_MATERIALIZED",
            "terminal_typing_status": "UNRESOLVED_R1648_CONTINUATION",
            "D02_credit": 0,
        })
    return rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir() if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def build(output: Path, c35: Path, c35_audit: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        round139, c35_result, c34_result = load_authorities(
            c35.resolve(), c35_audit.resolve()
        )
        c34_path = (ROOT / c35_result["C34_authority"]["path"]).resolve()
        geometry, words, bindings = build_occurrence_rows(
            round139, c35.resolve(), c35_result
        )
        templates = materialize_template_rows(geometry, bindings)
        word_atlas = materialize_word_rows(words, bindings)
        obligations = build_obligations(c34_path, c34_result)

        template_writer = LedgerWriter(
            stage / "template_margin_atlas.jsonl.gz",
            "C35_GEOMETRY_TEMPLATE_LEDGER_ORDER",
        )
        with template_writer:
            for row in templates:
                template_writer.write(row)
        word_writer = LedgerWriter(
            stage / "word_stratum_margin_atlas.jsonl.gz",
            "C35_OFFICIAL_WORD_VARIANT_LEDGER_ORDER",
        )
        with word_writer:
            for row in word_atlas:
                word_writer.write(row)
        binding_writer = LedgerWriter(
            stage / "occurrence_margin_bindings.jsonl.gz",
            "COLLISION_INDEX_ASCENDING",
        )
        with binding_writer:
            for row in bindings:
                binding_writer.write(row)
        obligation_writer = LedgerWriter(
            stage / "component_refinement_obligations.jsonl.gz",
            "C34_ORDINARY_COMPONENT_LEDGER_ORDER",
        )
        with obligation_writer:
            for row in obligations:
                obligation_writer.write(row)

        (stage / "SEED_COLLAR_ONLY.lock").write_text(
            "C36 materializes all C35 transition-template and word-stratum margin maps only "
            "on the two pinned Round139 seed collars. It grants zero C34 common-refinement, "
            "D02, D03, D04, Gate5, or CM2 credit.\n",
            encoding="utf-8",
        )
        total_occurrence_obligations = sum(
            row["cell_occurrence_refinement_obligation_count"]
            for row in obligations
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C36_DUAL_SEED_COLLAR_TEMPLATE_MARGIN_ATLAS__"
                "137_OF_137_GEOMETRY_TEMPLATES__197_OF_197_WORD_STRATA__"
                "1648_OF_1648_OCCURRENCES__C34_COMMON_REFINEMENT_ZERO"
            ),
            "Round139_authority": {
                "path": str(ROUND139.relative_to(ROOT)),
                "file_sha256": EXPECTED_ROUND139_FILE,
                "result_sha256": EXPECTED_ROUND139_RESULT,
            },
            "C35_authority": {
                "path": str(c35.resolve().relative_to(ROOT)),
                "object_sha256": c35_result["object_sha256"],
                "independent_audit_path":
                    str(c35_audit.resolve().relative_to(ROOT)),
                "independent_audit_object_sha256": EXPECTED_C35_AUDIT_OBJECT,
            },
            "C34_authority": {
                "path": str(c34_path.relative_to(ROOT)),
                "object_sha256": c34_result["object_sha256"],
            },
            "atlas_census": {
                "geometry_templates_materialized_on_dual_seed_collars":
                    len(templates),
                "official_word_strata_materialized_on_dual_seed_collars":
                    len(word_atlas),
                "occurrence_margin_bindings": len(bindings),
                "ordinary_components_awaiting_common_refinement":
                    len(obligations),
                "ordinary_cells_awaiting_common_refinement":
                    sum(row["cell_count"] for row in obligations),
                "cell_occurrence_refinement_obligations":
                    total_occurrence_obligations,
                "cell_geometry_template_obligations": sum(
                    row["cell_geometry_template_obligation_count"]
                    for row in obligations
                ),
                "cell_word_variant_obligations": sum(
                    row["cell_word_variant_obligation_count"]
                    for row in obligations
                ),
            },
            "map_stage_census": {
                "owner_candidate_discriminant_maps": len(templates),
                "near_root_order_maps": len(templates),
                "official_word_maps": len(word_atlas),
                "outgoing_chart_maps": len(templates),
                "C24_core_maps": len(templates),
                "scope": "DUAL_R139_SEED_COLLARS_ONLY",
            },
            "ledgers": {
                "template_margin_atlas": template_writer.descriptor(),
                "word_stratum_margin_atlas": word_writer.descriptor(),
                "occurrence_margin_bindings": binding_writer.descriptor(),
                "component_refinement_obligations":
                    obligation_writer.descriptor(),
            },
            "round144_terminal_census": c34_result["round144_terminal_census"],
            "strict_nonpromotion": {
                "C34_common_refined_cell_count": 0,
                "C34_unresolved_R1648_continuations": 1724,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "common-refine all 26 C34 ordinary components and 1724 cells against the "
                "C36 137-template/197-word margin atlas; materialize every first event, "
                "component exit, seam, grazing, corner, and disconnected exterior sheet; "
                "require the four Round161 terminal classes to have unresolved=0"
            ),
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        stage.rename(output)
        return result
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--c35", type=Path)
    parser.add_argument("--c35-audit", type=Path)
    args = parser.parse_args()
    c35 = args.c35 or (
        RUNTIME / "candidates" / (RUNTIME / "c35-current-token").read_text().strip()
    )
    c35_audit = args.c35_audit or (
        RUNTIME / "audit" / (RUNTIME / "c35-current-audit-token").read_text().strip()
        / "independent_audit.json"
    )
    result = build(args.output.resolve(), c35.resolve(), c35_audit.resolve())
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
