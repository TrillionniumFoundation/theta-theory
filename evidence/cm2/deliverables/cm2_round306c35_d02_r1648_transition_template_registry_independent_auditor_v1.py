#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SCHEMA = "cm2.round306c35.d02-r1648-transition-template-registry.v1"
AUDIT_SCHEMA = "cm2.round306c35.d02-r1648-transition-template-registry-independent-audit.v1"
EXPECTED_STATUS = (
    "PASS_C35_R1648_TRANSITION_REGISTRY__137_GEOMETRY_TEMPLATES__"
    "197_OFFICIAL_WORD_VARIANTS__1648_OCCURRENCES__ZERO_D02_CREDIT"
)
EXPECTED_ROUND139_FILE = "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
EXPECTED_ROUND139_RESULT = "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
EXPECTED_C34_OBJECT = "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e"
EXPECTED_C34_AUDIT_OBJECT = (
    "6cf20bd4915731e41be5da6cc4f8599ec4a4dbed8243bc3e17c15497b980b9f8"
)
EXPECTED_WORD_SEQUENCE = "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
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


def validate_object(value: dict[str, Any], field: str, expected: str | None, label: str) -> str:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(type(recorded) is str and recorded == digest(semantic), f"object:{label}")
    if expected is not None:
        require(recorded == expected, f"expected object:{label}")
    return recorded


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(encoding="utf-8").splitlines()
    expected_names = {
        "REGISTRY_ONLY.lock",
        "geometry_transition_templates.jsonl.gz",
        "official_word_variants.jsonl.gz",
        "path_occurrences.jsonl.gz",
        "result.json",
    }
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"duplicate manifest member:{name}")
        names.append(name)
        require(
            (directory / name).is_file() and file_sha256(directory / name) == expected,
            f"manifest member:{name}",
        )
    require(names == sorted(names) and set(names) == expected_names, "manifest inventory")


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
            require(row_sha == digest(semantic), f"row hash:{path}")
            rows.append(row)
            sequence.update((row_sha + "\n").encode("ascii"))
    require(
        len(rows) == descriptor["row_count"]
        and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor:{path}",
    )
    return rows


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path = DELIVERABLES / (
        "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
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
        "Round139 row groups",
    )
    rows: list[dict[str, Any]] = []
    incoming_chart = "E"
    previous_owner = "W[0,0]"
    official_ids: list[str] = []
    for index, (left, right) in enumerate(zip(graph, cylinder, strict=True), start=1):
        for label, row in (("graph", left), ("cylinder", right)):
            semantic = dict(row)
            row_sha = semantic.pop("row_sha256", None)
            require(row_sha == digest(semantic), f"Round139 row:{label}:{index}")
        fields = (
            "collision_index", "incoming_absolute_owner_id", "selected_absolute_owner_id",
            "relative_frozen_target_id", "official_word_key", "ordered_clean_wall_record",
            "outgoing_chart", "C24_classification", "destination_core_id",
            "homogeneity_label", "incidence_rank_B",
        )
        require(all(left[field] == right[field] for field in fields), f"semantic duality:{index}")
        registry = left["official_word_key"]["registry_row"]
        require(
            left["collision_index"] == index
            and left["incoming_absolute_owner_id"] == previous_owner
            and registry[0] == f"{previous_owner[0]}:{incoming_chart}"
            and registry[1] == left["relative_frozen_target_id"]
            and registry[2] == left["ordered_clean_wall_record"]
            and left["official_word_key"]["registry_row_sha256"] == digest(registry),
            f"path recurrence:{index}",
        )
        geometry_key = [
            previous_owner[0], incoming_chart,
            left["relative_frozen_target_id"], left["outgoing_chart"],
        ]
        word_key = [*geometry_key, canonical(registry).decode("utf-8")]
        rows.append({
            "collision_index": index,
            "incoming_absolute_owner_id": previous_owner,
            "selected_absolute_owner_id": left["selected_absolute_owner_id"],
            "incoming_chart": incoming_chart,
            "outgoing_chart": left["outgoing_chart"],
            "relative_frozen_target_id": left["relative_frozen_target_id"],
            "geometry_template_id": "c35-r1648-geometry-template:" + digest(geometry_key),
            "official_word_variant_id": "c35-r1648-official-word-variant:" + digest(word_key),
            "official_word_key_id": left["official_word_key"]["official_word_key_id"],
            "graph_row_sha256": left["row_sha256"],
            "positive_area_row_sha256": right["row_sha256"],
            "C24_classification": left["C24_classification"],
            "destination_core_id": left["destination_core_id"],
            "registry": registry,
        })
        official_ids.append(left["official_word_key"]["official_word_key_id"])
        previous_owner = left["selected_absolute_owner_id"]
        incoming_chart = left["outgoing_chart"]
    require(digest(official_ids) == EXPECTED_WORD_SEQUENCE, "official sequence")
    geometry_counts = Counter(row["geometry_template_id"] for row in rows)
    word_counts = Counter(row["official_word_variant_id"] for row in rows)
    variants: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        variants[row["geometry_template_id"]].add(row["official_word_variant_id"])
    summary = {
        "geometry_transition_template_count": len(geometry_counts),
        "official_word_variant_count": len(word_counts),
        "path_occurrence_count": len(rows),
        "geometry_template_occurrence_total": sum(geometry_counts.values()),
        "official_word_variant_occurrence_total": sum(word_counts.values()),
        "geometry_templates_with_multiple_word_variants": sum(
            len(value) > 1 for value in variants.values()
        ),
        "maximum_word_variants_per_geometry_template": max(map(len, variants.values())),
    }
    require(summary == {
        "geometry_transition_template_count": 137,
        "official_word_variant_count": 197,
        "path_occurrence_count": 1648,
        "geometry_template_occurrence_total": 1648,
        "official_word_variant_occurrence_total": 1648,
        "geometry_templates_with_multiple_word_variants": 38,
        "maximum_word_variants_per_geometry_template": 4,
    }, "reconstructed census")
    return rows, summary


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["geometry"] == 137, "summary geometry")
    require(summary["words"] == 197, "summary words")
    require(summary["occurrences"] == 1648, "summary occurrences")
    require(summary["multi_geometry"] == 38, "summary multi geometry")
    require(summary["maximum_variants"] == 4, "summary maximum variants")
    require(summary["collision2"] == ["W", "W", "G[-1,1]", "E"], "summary collision2")
    require(summary["materialized_templates"] == 0, "summary materialized")
    require(summary["unresolved"] == 1724, "summary unresolved")
    require(summary["D02"] == "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS", "summary D02")


def hostile_attacks(summary: dict[str, Any]) -> dict[str, Any]:
    mutations = {
        "geometry_count_tamper": ("geometry", 136),
        "word_count_tamper": ("words", 196),
        "occurrence_count_tamper": ("occurrences", 1647),
        "multi_geometry_tamper": ("multi_geometry", 37),
        "maximum_variant_tamper": ("maximum_variants", 3),
        "collision2_source_swap": ("collision2", ["G", "W", "G[-1,1]", "E"]),
        "collision2_target_swap": ("collision2", ["W", "W", "G[1,-1]", "E"]),
        "false_template_materialization": ("materialized_templates", 137),
        "false_unresolved_zero": ("unresolved", 0),
        "illegal_D02_promotion": ("D02", "AUTHORIZED"),
    }
    passed: list[str] = []
    for label, (field, value) in mutations.items():
        candidate = copy.deepcopy(summary)
        candidate[field] = value
        try:
            validate_summary(candidate)
        except RuntimeError:
            passed.append(label)
        else:
            raise RuntimeError(f"attack accepted:{label}")
    return {"attack_count": len(mutations), "fail_closed_count": len(passed), "labels": passed}


def audit(candidate: Path) -> dict[str, Any]:
    validate_manifest(candidate)
    result = strict_json(candidate / "result.json")
    object_sha = validate_object(result, "object_sha256", None, "C35")
    require(result.get("schema") == SCHEMA and result.get("status") == EXPECTED_STATUS, "C35 identity")
    require(
        result["Round139_authority"]["file_sha256"] == EXPECTED_ROUND139_FILE
        and result["Round139_authority"]["result_sha256"] == EXPECTED_ROUND139_RESULT,
        "Round139 result binding",
    )
    c34 = ROOT / result["C34_authority"]["path"]
    c34_result = strict_json(c34 / "result.json")
    validate_object(c34_result, "object_sha256", EXPECTED_C34_OBJECT, "C34")
    c34_audit = ROOT / result["C34_authority"]["independent_audit_path"]
    c34_audit_result = strict_json(c34_audit)
    validate_object(c34_audit_result, "object_sha256", EXPECTED_C34_AUDIT_OBJECT, "C34 audit")
    require(c34_audit_result["candidate_object_sha256"] == EXPECTED_C34_OBJECT, "C34 audit candidate")

    reconstructed, census = reconstruct()
    geometry = read_ledger(candidate, result["ledgers"]["geometry_transition_templates"])
    words = read_ledger(candidate, result["ledgers"]["official_word_variants"])
    occurrences = read_ledger(candidate, result["ledgers"]["path_occurrences"])
    require(
        len(geometry) == census["geometry_transition_template_count"]
        and len(words) == census["official_word_variant_count"]
        and len(occurrences) == census["path_occurrence_count"]
        and result["registry_census"] == census,
        "candidate census",
    )
    geometry_by_id = {row["geometry_template_id"]: row for row in geometry}
    word_by_id = {row["official_word_variant_id"]: row for row in words}
    require(len(geometry_by_id) == 137 and len(word_by_id) == 197, "unique registry IDs")
    recorded_occurrences = Counter()
    recorded_words = Counter()
    variants: dict[str, set[str]] = defaultdict(set)
    for expected, row in zip(reconstructed, occurrences, strict=True):
        semantic = dict(row)
        semantic.pop("schema")
        semantic.pop("row_sha256")
        expected_semantic = dict(expected)
        expected_semantic.pop("registry")
        require(semantic == expected_semantic, f"occurrence semantics:{expected['collision_index']}")
        require(
            row["geometry_template_id"] in geometry_by_id
            and row["official_word_variant_id"] in word_by_id
            and word_by_id[row["official_word_variant_id"]]["geometry_template_id"]
            == row["geometry_template_id"],
            "occurrence registry binding",
        )
        recorded_occurrences[row["geometry_template_id"]] += 1
        recorded_words[row["official_word_variant_id"]] += 1
        variants[row["geometry_template_id"]].add(row["official_word_variant_id"])
    for template_id, row in geometry_by_id.items():
        indices = [
            item["collision_index"] for item in occurrences
            if item["geometry_template_id"] == template_id
        ]
        require(
            row["occurrence_count"] == recorded_occurrences[template_id]
            and row["occurrence_indices"] == indices
            and row["occurrence_indices_sha256"] == digest(indices)
            and row["official_word_variant_count"] == len(variants[template_id])
            and row["official_word_variant_ids_sha256"] == digest(sorted(variants[template_id]))
            and row["required_template_atlas_status"] == "NOT_MATERIALIZED"
            and row["D02_credit"] == 0,
            f"geometry row:{template_id}",
        )
    for variant_id, row in word_by_id.items():
        indices = [
            item["collision_index"] for item in occurrences
            if item["official_word_variant_id"] == variant_id
        ]
        require(
            row["occurrence_count"] == recorded_words[variant_id]
            and row["occurrence_indices"] == indices
            and row["occurrence_indices_sha256"] == digest(indices)
            and row["official_registry_row_sha256"] == digest(row["official_registry_row"])
            and row["required_word_stratum_status"] == "NOT_MATERIALIZED"
            and row["D02_credit"] == 0,
            f"word row:{variant_id}",
        )

    collision2 = occurrences[1]
    require(
        result["collision2_anchor"] == {
            "collision_index": 2,
            "source_obstacle": "W",
            "incoming_chart": "W",
            "relative_frozen_target_id": "G[-1,1]",
            "selected_absolute_owner_id": "G[0,1]",
            "outgoing_chart": "E",
            "geometry_template_id": collision2["geometry_template_id"],
            "official_word_variant_id": collision2["official_word_variant_id"],
        },
        "collision2 anchor",
    )
    require(
        result["strict_nonpromotion"] == {
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
        "strict nonpromotion",
    )
    summary = {
        "geometry": len(geometry),
        "words": len(words),
        "occurrences": len(occurrences),
        "multi_geometry": sum(len(value) > 1 for value in variants.values()),
        "maximum_variants": max(map(len, variants.values())),
        "collision2": [
            collision2["incoming_absolute_owner_id"][0],
            collision2["incoming_chart"],
            collision2["relative_frozen_target_id"],
            collision2["outgoing_chart"],
        ],
        "materialized_templates": result["strict_nonpromotion"]["template_atlases_materialized"],
        "unresolved": result["strict_nonpromotion"]["C34_unresolved_R1648_continuations"],
        "D02": result["strict_nonpromotion"]["D02"],
    }
    validate_summary(summary)
    attacks = hostile_attacks(summary)
    audit_result: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "status": "PASS_INDEPENDENT_C35_RECONSTRUCTION__10_OF_10_ATTACKS_FAIL_CLOSED",
        "candidate_path": str(candidate.resolve().relative_to(ROOT)),
        "candidate_object_sha256": object_sha,
        "candidate_root_manifest_sha256": file_sha256(candidate / "root_manifest.sha256"),
        "reconstructed_registry_census": census,
        "collision2_anchor": result["collision2_anchor"],
        "hostile_attacks": attacks,
        "strict_conclusion": {
            "materialized_template_atlas_count": 0,
            "C34_unresolved_R1648_continuations": 1724,
            "D02": "BLOCKED_BY_1724_COMPLETE_R1648_CONTINUATIONS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    audit_result["object_sha256"] = digest(audit_result)
    return audit_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.candidate.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.name + f".tmp-{os.getpid()}")
    require(not temporary.exists(), "temporary absent")
    temporary.write_bytes(canonical(result) + b"\n")
    temporary.rename(args.output)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
