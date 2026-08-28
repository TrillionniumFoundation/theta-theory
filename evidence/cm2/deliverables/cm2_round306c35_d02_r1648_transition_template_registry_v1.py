#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
SCHEMA = "cm2.round306c35.d02-r1648-transition-template-registry.v1"
GEOMETRY_ROW_SCHEMA = "cm2.round306c35.r1648-geometry-transition-template-row.v1"
WORD_ROW_SCHEMA = "cm2.round306c35.r1648-official-word-variant-row.v1"
OCCURRENCE_ROW_SCHEMA = "cm2.round306c35.r1648-transition-occurrence-row.v1"

ROUND139 = DELIVERABLES / (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
ROUND139_VERIFICATION = DELIVERABLES / (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "verification-2026-07-24.json"
)
EXPECTED_ROUND139_FILE = "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
EXPECTED_ROUND139_RESULT = "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
EXPECTED_ROUND139_VERIFICATION_FILE = (
    "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f"
)
EXPECTED_ROUND139_VERIFICATION_RESULT = (
    "e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1"
)
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C34_AUDIT_OBJECT = (
    "6cf20bd4915731e41be5da6cc4f8599ec4a4dbed8243bc3e17c15497b980b9f8"
)
EXPECTED_WORD_SEQUENCE = "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
EXPECTED_PATH_TUPLE = "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
SOURCE_CORE = "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
DESTINATION_CORE = "core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2"
RETURN_DEPTH = 1648


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


def validate_object(value: dict[str, Any], field: str, expected: str, label: str) -> None:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(recorded == expected == digest(semantic), f"object:{label}")


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(encoding="utf-8").splitlines()
    require(rows, f"manifest nonempty:{directory}")
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"manifest duplicate:{directory}:{name}")
        names.append(name)
        path = directory / name
        require(path.is_file() and file_sha256(path) == expected, f"manifest member:{path}")
    require(names == sorted(names), f"manifest order:{directory}")


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    semantic = dict(row)
    recorded = semantic.pop("row_sha256", None)
    require(recorded == digest(semantic), f"row closure:{label}")


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
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
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


def load_authorities(c34: Path, c34_audit: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    require(file_sha256(ROUND139) == EXPECTED_ROUND139_FILE, "Round139 file pin")
    require(
        file_sha256(ROUND139_VERIFICATION) == EXPECTED_ROUND139_VERIFICATION_FILE,
        "Round139 verification file pin",
    )
    round139 = strict_json(ROUND139)
    verification = strict_json(ROUND139_VERIFICATION)
    require(
        round139.get("result_sha256") == EXPECTED_ROUND139_RESULT
        and digest(round139.get("result")) == EXPECTED_ROUND139_RESULT,
        "Round139 envelope",
    )
    require(
        verification.get("result_sha256") == EXPECTED_ROUND139_VERIFICATION_RESULT
        and digest(verification.get("result")) == EXPECTED_ROUND139_VERIFICATION_RESULT
        and verification["result"].get("status") == "PASS"
        and verification["result"].get("certificate_result_sha256")
        == EXPECTED_ROUND139_RESULT,
        "Round139 verification",
    )

    validate_manifest(c34)
    c34_result = strict_json(c34 / "result.json")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")
    require(
        c34_result["round144_terminal_census"]["UNRESOLVED_R1648_CONTINUATION"] == 1724
        and c34_result["round144_terminal_census"]["unresolved_zero"] is False,
        "C34 unresolved frontier",
    )
    audit = strict_json(c34_audit)
    validate_object(audit, "object_sha256", EXPECTED_C34_AUDIT_OBJECT, "C34 audit")
    require(
        audit.get("candidate_object_sha256") == EXPECTED_C34_OBJECT
        and audit.get("status")
        == "PASS_INDEPENDENT_C34_RECONSTRUCTION__8_OF_8_ATTACKS_FAIL_CLOSED",
        "C34 audit binding",
    )
    return round139["result"], c34_result


SEMANTIC_FIELDS = (
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


def geometry_key(row: dict[str, Any], incoming_chart: str) -> tuple[str, str, str, str]:
    return (
        row["incoming_absolute_owner_id"][0],
        incoming_chart,
        row["relative_frozen_target_id"],
        row["outgoing_chart"],
    )


def word_key(row: dict[str, Any], incoming_chart: str) -> tuple[Any, ...]:
    return (*geometry_key(row, incoming_chart), canonical(row["official_word_key"]["registry_row"]).decode("utf-8"))


def validate_round139(result: dict[str, Any]) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[str], list[str]
]:
    graph = result["collision_rows"]
    cylinder = result["positive_area_collision_rows"]
    require(
        len(graph) == len(cylinder) == RETURN_DEPTH
        and digest(graph) == result["collision_rows_sha256"]
        and digest(cylinder) == result["positive_area_collision_rows_sha256"],
        "Round139 row groups",
    )
    incoming_charts: list[str] = []
    geometry_ids: list[str] = []
    previous_owner = "W[0,0]"
    incoming_chart = "E"
    official_ids: list[str] = []
    for index, (graph_row, cylinder_row) in enumerate(zip(graph, cylinder, strict=True), start=1):
        validate_closed_row(graph_row, f"graph:{index}")
        validate_closed_row(cylinder_row, f"cylinder:{index}")
        require(
            all(graph_row[field] == cylinder_row[field] for field in SEMANTIC_FIELDS),
            f"dual semantic projection:{index}",
        )
        require(
            graph_row["collision_index"] == index
            and graph_row["incoming_absolute_owner_id"] == previous_owner
            and graph_row["homogeneity_label"] == "H0_CENTRAL"
            and graph_row["incidence_rank_B"] == 14,
            f"path recurrence:{index}",
        )
        official = graph_row["official_word_key"]
        registry = official["registry_row"]
        require(
            registry[0] == f"{previous_owner[0]}:{incoming_chart}"
            and registry[1] == graph_row["relative_frozen_target_id"]
            and registry[2] == graph_row["ordered_clean_wall_record"]
            and official["registry_row_sha256"] == digest(registry)
            and official["official_word_key_id"]
            == (
                f"gate5-word:{official['ordinal_zero_based']:06d}:"
                f"{official['registry_row_sha256']}"
            ),
            f"official registry binding:{index}",
        )
        if index < RETURN_DEPTH:
            require(
                graph_row["C24_classification"] == "SURVIVE_THROUGH_3_INNER"
                and graph_row["destination_core_id"] is None,
                f"preterminal C24:{index}",
            )
        else:
            require(
                graph_row["C24_classification"] == "RETURN_AT_3_INNER"
                and graph_row["destination_core_id"] == DESTINATION_CORE,
                "terminal C24",
            )
        incoming_charts.append(incoming_chart)
        key = geometry_key(graph_row, incoming_chart)
        geometry_ids.append("c35-r1648-geometry-template:" + digest(list(key)))
        official_ids.append(official["official_word_key_id"])
        previous_owner = graph_row["selected_absolute_owner_id"]
        incoming_chart = graph_row["outgoing_chart"]
    require(
        digest(official_ids) == EXPECTED_WORD_SEQUENCE
        and digest([SOURCE_CORE, RETURN_DEPTH, official_ids]) == EXPECTED_PATH_TUPLE,
        "Round139 path identity",
    )
    return graph, cylinder, incoming_charts, geometry_ids


def build_rows(
    graph: list[dict[str, Any]], cylinder: list[dict[str, Any]],
    incoming_charts: list[str], geometry_ids: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    geometry_occurrences: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
    word_occurrences: dict[tuple[Any, ...], list[int]] = defaultdict(list)
    word_ids_by_geometry: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    occurrence_rows: list[dict[str, Any]] = []

    for index, (row, cylinder_row, incoming_chart, geometry_id) in enumerate(
        zip(graph, cylinder, incoming_charts, geometry_ids, strict=True), start=1,
    ):
        gkey = geometry_key(row, incoming_chart)
        wkey = word_key(row, incoming_chart)
        official_variant_id = "c35-r1648-official-word-variant:" + digest(list(wkey))
        geometry_occurrences[gkey].append(index)
        word_occurrences[wkey].append(index)
        word_ids_by_geometry[gkey].add(official_variant_id)
        occurrence_rows.append({
            "schema": OCCURRENCE_ROW_SCHEMA,
            "collision_index": index,
            "incoming_absolute_owner_id": row["incoming_absolute_owner_id"],
            "selected_absolute_owner_id": row["selected_absolute_owner_id"],
            "incoming_chart": incoming_chart,
            "outgoing_chart": row["outgoing_chart"],
            "relative_frozen_target_id": row["relative_frozen_target_id"],
            "geometry_template_id": geometry_id,
            "official_word_variant_id": official_variant_id,
            "official_word_key_id": row["official_word_key"]["official_word_key_id"],
            "graph_row_sha256": row["row_sha256"],
            "positive_area_row_sha256": cylinder_row["row_sha256"],
            "C24_classification": row["C24_classification"],
            "destination_core_id": row["destination_core_id"],
        })

    geometry_rows: list[dict[str, Any]] = []
    for key in sorted(geometry_occurrences):
        source, incoming_chart, relative_target, outgoing_chart = key
        indices = geometry_occurrences[key]
        geometry_id = "c35-r1648-geometry-template:" + digest(list(key))
        variant_ids = sorted(word_ids_by_geometry[key])
        geometry_rows.append({
            "schema": GEOMETRY_ROW_SCHEMA,
            "geometry_template_id": geometry_id,
            "source_obstacle": source,
            "incoming_chart": incoming_chart,
            "relative_frozen_target_id": relative_target,
            "target_obstacle": relative_target[0],
            "outgoing_chart": outgoing_chart,
            "occurrence_count": len(indices),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "official_word_variant_count": len(variant_ids),
            "official_word_variant_ids_sha256": digest(variant_ids),
            "contains_collision_2": 2 in indices,
            "required_template_atlas_status": "NOT_MATERIALIZED",
            "D02_credit": 0,
        })

    word_rows: list[dict[str, Any]] = []
    for key in sorted(word_occurrences, key=lambda item: canonical(list(item))):
        source, incoming_chart, relative_target, outgoing_chart, registry_json = key
        registry = json.loads(registry_json)
        indices = word_occurrences[key]
        gkey = (source, incoming_chart, relative_target, outgoing_chart)
        word_rows.append({
            "schema": WORD_ROW_SCHEMA,
            "official_word_variant_id": "c35-r1648-official-word-variant:" + digest(list(key)),
            "geometry_template_id": "c35-r1648-geometry-template:" + digest(list(gkey)),
            "source_obstacle": source,
            "incoming_chart": incoming_chart,
            "relative_frozen_target_id": relative_target,
            "outgoing_chart": outgoing_chart,
            "official_registry_row": registry,
            "official_registry_row_sha256": digest(registry),
            "occurrence_count": len(indices),
            "occurrence_indices": indices,
            "occurrence_indices_sha256": digest(indices),
            "required_word_stratum_status": "NOT_MATERIALIZED",
            "D02_credit": 0,
        })

    require(
        len(geometry_rows) == 137
        and len(word_rows) == 197
        and len(occurrence_rows) == RETURN_DEPTH
        and sum(row["occurrence_count"] for row in geometry_rows) == RETURN_DEPTH
        and sum(row["occurrence_count"] for row in word_rows) == RETURN_DEPTH,
        "template registry census",
    )
    collision2 = [row for row in geometry_rows if row["contains_collision_2"]]
    require(
        len(collision2) == 1
        and (
            collision2[0]["source_obstacle"],
            collision2[0]["incoming_chart"],
            collision2[0]["relative_frozen_target_id"],
            collision2[0]["outgoing_chart"],
        ) == ("W", "W", "G[-1,1]", "E"),
        "collision2 template",
    )
    return geometry_rows, word_rows, occurrence_rows


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def write_manifest(directory: Path) -> None:
    members = sorted(path for path in directory.iterdir() if path.name != "root_manifest.sha256")
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


def build(output: Path, c34: Path, c34_audit: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        round139, c34_result = load_authorities(c34.resolve(), c34_audit.resolve())
        graph, cylinder, incoming_charts, geometry_ids = validate_round139(round139)
        geometry_rows, word_rows, occurrence_rows = build_rows(
            graph, cylinder, incoming_charts, geometry_ids,
        )

        geometry_writer = LedgerWriter(
            stage / "geometry_transition_templates.jsonl.gz",
            "LEXICOGRAPHIC_GEOMETRY_TEMPLATE_KEY",
        )
        with geometry_writer:
            for row in geometry_rows:
                geometry_writer.write(row)
        word_writer = LedgerWriter(
            stage / "official_word_variants.jsonl.gz",
            "CANONICAL_OFFICIAL_WORD_VARIANT_KEY",
        )
        with word_writer:
            for row in word_rows:
                word_writer.write(row)
        occurrence_writer = LedgerWriter(
            stage / "path_occurrences.jsonl.gz",
            "COLLISION_INDEX_ASCENDING",
        )
        with occurrence_writer:
            for row in occurrence_rows:
                occurrence_writer.write(row)

        collision2_occurrence = occurrence_rows[1]
        (stage / "REGISTRY_ONLY.lock").write_text(
            "C35 registers transition obligations and does not authorize D02, D03, D04, Gate5, or CM2.\n",
            encoding="utf-8",
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_C35_R1648_TRANSITION_REGISTRY__137_GEOMETRY_TEMPLATES__"
                "197_OFFICIAL_WORD_VARIANTS__1648_OCCURRENCES__ZERO_D02_CREDIT"
            ),
            "Round139_authority": {
                "path": str(ROUND139.relative_to(ROOT)),
                "file_sha256": EXPECTED_ROUND139_FILE,
                "result_sha256": EXPECTED_ROUND139_RESULT,
                "verification_path": str(ROUND139_VERIFICATION.relative_to(ROOT)),
                "verification_file_sha256": EXPECTED_ROUND139_VERIFICATION_FILE,
                "verification_result_sha256": EXPECTED_ROUND139_VERIFICATION_RESULT,
            },
            "C34_authority": {
                "path": str(c34.resolve().relative_to(ROOT)),
                "object_sha256": c34_result["object_sha256"],
                "independent_audit_path": str(c34_audit.resolve().relative_to(ROOT)),
                "independent_audit_object_sha256": EXPECTED_C34_AUDIT_OBJECT,
            },
            "path_identity": {
                "source_core_id": SOURCE_CORE,
                "return_depth": RETURN_DEPTH,
                "official_word_key_sequence_sha256": EXPECTED_WORD_SEQUENCE,
                "Round27_path_tuple_sha256": EXPECTED_PATH_TUPLE,
                "dual_Round139_semantic_projection_equal": True,
            },
            "registry_census": {
                "geometry_transition_template_count": len(geometry_rows),
                "official_word_variant_count": len(word_rows),
                "path_occurrence_count": len(occurrence_rows),
                "geometry_template_occurrence_total": sum(
                    row["occurrence_count"] for row in geometry_rows
                ),
                "official_word_variant_occurrence_total": sum(
                    row["occurrence_count"] for row in word_rows
                ),
                "geometry_templates_with_multiple_word_variants": sum(
                    row["official_word_variant_count"] > 1 for row in geometry_rows
                ),
                "maximum_word_variants_per_geometry_template": max(
                    row["official_word_variant_count"] for row in geometry_rows
                ),
            },
            "collision2_anchor": {
                "collision_index": 2,
                "source_obstacle": "W",
                "incoming_chart": "W",
                "relative_frozen_target_id": "G[-1,1]",
                "selected_absolute_owner_id": "G[0,1]",
                "outgoing_chart": "E",
                "geometry_template_id": collision2_occurrence["geometry_template_id"],
                "official_word_variant_id": collision2_occurrence["official_word_variant_id"],
            },
            "ledgers": {
                "geometry_transition_templates": geometry_writer.descriptor(),
                "official_word_variants": word_writer.descriptor(),
                "path_occurrences": occurrence_writer.descriptor(),
            },
            "round144_terminal_census": c34_result["round144_terminal_census"],
            "strict_nonpromotion": {
                "template_atlases_materialized": 0,
                "word_strata_materialized": 0,
                "C34_unresolved_R1648_continuations": 1724,
                "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "materialize a certified owner/discriminant/root-order/word/chart/core map for "
                "each of the 137 geometry templates and all 197 official wall-word variants; "
                "then common-refine the C34 1724-cell continuation frontier and type every first "
                "event, component exit, grazing, corner, seam, and exterior sheet"
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
    parser.add_argument("--c34", type=Path)
    parser.add_argument("--c34-audit", type=Path)
    args = parser.parse_args()
    c34 = args.c34 or (
        RUNTIME / "candidates" / (RUNTIME / "c34-current-token").read_text().strip()
    )
    c34_audit = args.c34_audit or (
        RUNTIME / "audit" / (RUNTIME / "c34-current-audit-token").read_text().strip()
        / "independent_audit.json"
    )
    result = build(args.output.resolve(), c34.resolve(), c34_audit.resolve())
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
