#!/usr/bin/env python3
"""Bind every C32 compact cell to the final formal source-W disposition."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
sys.path.insert(0, str(DELIVERABLES))

import cm2_round165_adaptive_typed_seam_census as round165  # noqa: E402


SCHEMA = "cm2.round306c33.d02-source-w-row-level-disposition-crosswalk.v1"
ROW_SCHEMA = "cm2.round306c33.d02-source-w-row-level-disposition.v1"
FROZEN_OWNER = "W[1,0]"
EXPECTED_C32_STATUS = (
    "PASS_EXACT_FOUR_CHART_COMPACT_S0_CELL_ADJACENCY_SEAM_GRAZING_"
    "CORNER_AND_INHERITED_EVENT_LEDGER__D02_STILL_BLOCKED"
)
EXPECTED_FORMAL_OBJECT = (
    "34d485901b6458f7e0614361a220d3e475ee0827be64aa19e8955b29e09d1c97"
)
EXPECTED_ROUND201_FILE = (
    "72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536"
)
EXPECTED_ROUND201_KEYS = (
    "b0c171c0c27bf2e7ea4125dd8b1d46f47532d7d5227fcb3aa00377d2758b95fb"
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_loads(raw: str, label: str) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result

    def reject_float(value: str) -> None:
        raise RuntimeError(f"floating number:{label}:{value}")

    value = json.loads(
        raw, object_pairs_hook=pairs, parse_float=reject_float,
    )
    require(type(value) is dict, f"object:{label}")
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_loads(path.read_text(encoding="utf-8"), str(path))


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            row = strict_loads(line, f"{path}:{index + 1}")
            closed = dict(row)
            row_sha = closed.pop("row_sha256", None)
            require(row_sha == digest(closed), f"row self hash:{path}:{index + 1}")
            rows.append(row)
    return rows


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    return {**value, "row_sha256": digest(value)}


class LedgerWriter:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: io.BufferedWriter | None = None
        self.stream: gzip.GzipFile | None = None

    def __enter__(self) -> "LedgerWriter":
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, compresslevel=6, mtime=0,
        )
        return self

    def write(self, value: dict[str, Any]) -> None:
        require(self.stream is not None, "writer open")
        row = closed_row(value)
        self.stream.write(canonical_bytes(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: object) -> None:
        require(self.stream is not None and self.raw is not None, "writer close")
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


def validate_c32(directory: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = strict_json(directory / "result.json")
    result_copy = dict(result)
    object_sha = result_copy.pop("object_sha256", None)
    require(object_sha == digest(result_copy), "C32 result self hash")
    require(result.get("status") == EXPECTED_C32_STATUS, "C32 status")
    descriptor = result["ledgers"]["cells"]
    cell_path = directory / descriptor["filename"]
    require(file_sha256(cell_path) == descriptor["sha256"], "C32 cell file")
    cells = read_rows(cell_path)
    require(len(cells) == descriptor["row_count"] == 76832, "C32 cell count")
    require(
        [row["origin_key"] for row in cells]
        == sorted(row["origin_key"] for row in cells),
        "C32 cell order",
    )
    require(len({row["cell_id"] for row in cells}) == 76832, "C32 cell IDs")
    return result, cells


def add_stage(
    stages: dict[str, set[str]], name: str, keys: Iterable[str], count: int,
) -> None:
    values = set(keys)
    require(len(values) == count, f"stage count:{name}")
    stages[name] = values


def baseline_stages(cells: list[dict[str, Any]], workers: int) -> dict[str, set[str]]:
    stages: dict[str, set[str]] = {}
    add_stage(
        stages,
        "ROUND162_W_W_OPEN_CELL_EXCLUSION",
        (row["origin_key"] for row in cells if row["gate3_chart"] == "W:W"),
        18930,
    )
    add_stage(
        stages,
        "ROUND162_UNIQUE_FIRST_OWNER_MISMATCH",
        (
            row["origin_key"] for row in cells
            if row["gate3_chart"] != "W:W"
            and row["source_lineage"]["kind"] == "ROUND162_GATE3_BASE_LEAF"
            and row["source_lineage"]["classification"] == "unique_first"
            and row["source_lineage"]["owner_target"] != FROZEN_OWNER
        ),
        18510,
    )
    add_stage(
        stages,
        "ROUND165_REFINED_OUTGOING_CHART_MISMATCH",
        (
            row["origin_key"] for row in cells
            if row["source_lineage"]["kind"] == "ROUND165_REFINED_TERMINAL"
            and "OUTGOING_CHART_MISMATCH" in row["source_lineage"]["classification"]
        ),
        118,
    )
    add_stage(
        stages,
        "ROUND166_MULTI_CANDIDATE_FROZEN_OWNER_ABSENT",
        (
            row["origin_key"] for row in cells
            if row["gate3_chart"] != "W:W"
            and row["source_lineage"]["kind"] == "ROUND162_GATE3_BASE_LEAF"
            and row["source_lineage"]["classification"] == "multi_candidate"
            and FROZEN_OWNER not in row["source_lineage"]["active_candidates"]
        ),
        35564,
    )

    atlases = round165.build_atlases(workers)
    round163_keys: list[str] = []
    for chart in round165.SOURCE_CHARTS:
        for leaf in atlases[chart]:
            if leaf.classification != "unique_first" or leaf.owner_target != FROZEN_OWNER:
                continue
            replay = round165.round163_replay_row(chart, leaf)
            if replay["disposition"] == "EARLIEST_PREFIX_EXCLUDED_OUTGOING_CHART_MISMATCH":
                round163_keys.append(replay["leaf_key"])
    add_stage(stages, "ROUND163_OUTGOING_CHART_MISMATCH", round163_keys, 40)
    require(sum(len(values) for values in stages.values()) == 73162, "Round168 baseline")
    return stages


def keys_from(path: Path, selector: tuple[str, ...]) -> list[str]:
    value: Any = strict_json(path)["result"]
    for key in selector:
        value = value[key]
    require(type(value) is list and all(type(item) is str for item in value), f"key list:{path}")
    return value


def load_round201_keys(path: Path, certificate: Path) -> list[str]:
    require(file_sha256(certificate) == EXPECTED_ROUND201_FILE, "Round201 file pin")
    values = [
        line.strip() for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and line.strip() != "null"
    ]
    require(
        len(values) == len(set(values)) == 546
        and values == sorted(values)
        and digest(values) == EXPECTED_ROUND201_KEYS,
        "Round201 extracted key authority",
    )
    return values


def exclusion_stages(
    cells: list[dict[str, Any]], round201_keys: Path,
    c30a_ledger: Path, c30b_ledger: Path, q9_producer: Path,
    formal: dict[str, Any], workers: int,
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, Any]]:
    stages = baseline_stages(cells, workers)
    paths = {
        "r172": DELIVERABLES / "cm2_round172_dimension_safe_tangency_parent_frozen_owner_absence_pruning_certificate.json",
        "r175": DELIVERABLES / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json",
        "r176": DELIVERABLES / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json",
        "r180": DELIVERABLES / "cm2_round180_full_multi_residual_dimension_safe_partial_certificate.json",
        "r184": DELIVERABLES / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_certificate.json",
        "r201": DELIVERABLES / "cm2_round201_source_w_exact_behind_formal_promotion_certificate.json",
        "r212": DELIVERABLES / "cm2_round212_source_w_half_open_source_seam_promotion_certificate.json",
        "r215": DELIVERABLES / "cm2_round215_source_w_mixed_algebraic_formal_promotion_certificate.json",
    }
    add_stage(
        stages, "ROUND172_TANGENCY_PARENT_OWNER_ABSENCE",
        keys_from(paths["r172"], ("whole_parent_frozen_owner_absence_credit", "exact_excluded_parent_keys")), 10,
    )
    add_stage(
        stages, "ROUND175_TANGENCY_ARRANGEMENT",
        keys_from(paths["r175"], ("new_whole_parent_exclusion_credit", "exact_parent_keys")), 6,
    )
    add_stage(
        stages, "ROUND176_MULTI_ORIGIN_ANALYTIC_CLOSURE",
        keys_from(paths["r176"], ("new_whole_parent_exclusion_credit", "exact_origin_keys")), 182,
    )
    add_stage(
        stages, "ROUND180_FULL_MULTI_RESIDUAL",
        keys_from(paths["r180"], ("new_whole_parent_exclusion_credit", "exact_origin_keys")), 32,
    )
    add_stage(
        stages, "ROUND184_PURE_SINGLE_CLIPPED_DELTA",
        keys_from(paths["r184"], ("pure_single_clipped_Delta_tranche", "closed_exact_origin_keys")), 620,
    )
    add_stage(
        stages, "ROUND201_EXACT_BEHIND_FORMAL_PROMOTION",
        load_round201_keys(round201_keys, paths["r201"]), 546,
    )
    add_stage(
        stages, "ROUND212_HALF_OPEN_SOURCE_SEAM",
        keys_from(paths["r212"], ("whole_origin_ledger", "promoted_whole_origin_keys")), 24,
    )
    r215 = strict_json(paths["r215"])["result"]
    add_stage(
        stages, "ROUND215_MIXED_ALGEBRAIC_FORMAL_PROMOTION",
        (row["origin_key"] for row in r215["formal_promotion"]["promotion_rows"]), 2,
    )

    c30a_rows = read_rows(c30a_ledger)
    require(
        len(c30a_rows) == 160
        and all(row["whole_original_physical_origin_excluded"] is True for row in c30a_rows)
        and all(row["formal_credit"]["whole_source_W_origin_exclusion"] == 1 for row in c30a_rows),
        "C30a whole-origin ledger",
    )
    add_stage(stages, "C30A_REDUCED_CLIPPED_DELTA", (row["origin_key"] for row in c30a_rows), 160)

    c30b_rows = read_rows(c30b_ledger)
    require(len(c30b_rows) == 12, "C30b whole-origin ledger")
    c30b_excluded = [row["origin_key"] for row in c30b_rows if row["whole_origin_disposition"] == "EXCLUDED"]
    c30b_resolved = [row["origin_key"] for row in c30b_rows if row["whole_origin_disposition"] == "RESOLVED_MIXED"]
    add_stage(stages, "C30B_OUTGOING_H_EXCLUDED", c30b_excluded, 2)

    transitions = {row["round"]: row for row in formal["transitions"]}
    add_stage(stages, "C30D_MULTI_DELTA_EXCLUDED", transitions["C30d"]["origin_keys"], 20)
    add_stage(stages, "C30F_RETAINED_SOURCE_SEAMS_EXCLUDED", transitions["C30f"]["origin_keys"], 2)

    q9 = strict_json(q9_producer)
    require(q9.get("result_sha256") == digest(q9["result"]), "Q9 result self hash")
    q9_rows = q9["result"]["research_disposition_ledger"]
    q9_excluded = [row["origin_key"] for row in q9_rows if row["research_disposition"] == "EXCLUDED"]
    q9_resolved = [row["origin_key"] for row in q9_rows if row["research_disposition"] == "RESOLVED_MIXED"]
    add_stage(stages, "C30Q10_COMPACT_Q_EXCLUDED", q9_excluded, 44)

    resolved_late: dict[str, set[str]] = {}
    add_stage(resolved_late, "C30B_OUTGOING_H_RESOLVED_MIXED", c30b_resolved, 10)
    add_stage(resolved_late, "C30C_FULL_DELTA_RESOLVED_MIXED", transitions["C30c"]["origin_keys"], 2)
    add_stage(resolved_late, "C30E_REDUCED_LIVE_RESOLVED_MIXED", transitions["C30e"]["origin_keys"], 2)
    add_stage(resolved_late, "C30Q10_COMPACT_Q_RESOLVED_MIXED", q9_resolved, 10)
    provenance_paths = {**paths, "c30a": c30a_ledger, "c30b": c30b_ledger, "q9": q9_producer}
    return stages, resolved_late, {
        str(path.relative_to(ROOT)): file_sha256(path)
        for path in provenance_paths.values()
    }


def validate_formal(path: Path) -> dict[str, Any]:
    formal = strict_json(path)
    copy = dict(formal)
    object_sha = copy.pop("object_sha256", None)
    require(object_sha == EXPECTED_FORMAL_OBJECT == digest(copy), "formal object")
    require(
        formal["current_state"] == {
            "conservative_live": 2020,
            "excluded": 74812,
            "remaining": 0,
            "remaining_partition": {"compact_q": 0},
            "resolved_nonexcluded": 2020,
            "total": 76832,
        },
        "formal final state",
    )
    return formal


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical_bytes(value) + b"\n")


def build(
    output: Path, c32: Path, formal_path: Path, round201_keys: Path,
    c30a_ledger: Path, c30b_ledger: Path, q9_producer: Path, workers: int,
) -> dict[str, Any]:
    require(workers in {1, 2}, "workers")
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        c32_result, cells = validate_c32(c32.resolve())
        formal = validate_formal(formal_path.resolve())
        exclusion, resolved_late, provenance = exclusion_stages(
            cells, round201_keys.resolve(), c30a_ledger.resolve(),
            c30b_ledger.resolve(), q9_producer.resolve(), formal, workers,
        )
        origin_keys = {row["origin_key"] for row in cells}
        stage_by_key: dict[str, str] = {}
        cumulative: list[dict[str, Any]] = []
        excluded_total = 0
        for stage_name, keys in exclusion.items():
            require(keys <= origin_keys, f"stage subset:{stage_name}")
            overlap = set(stage_by_key) & keys
            require(not overlap, f"stage overlap:{stage_name}:{sorted(overlap)[:3]}")
            for key in keys:
                stage_by_key[key] = stage_name
            excluded_total += len(keys)
            cumulative.append({
                "stage": stage_name,
                "new_excluded": len(keys),
                "cumulative_excluded": excluded_total,
                "origin_keys_sha256": digest(sorted(keys)),
            })
        require(excluded_total == len(stage_by_key) == 74812, "formal exclusion total")
        resolved_keys = origin_keys - set(stage_by_key)
        require(len(resolved_keys) == 2020, "formal resolved complement")

        resolved_stage_by_key: dict[str, str] = {}
        for stage_name, keys in resolved_late.items():
            require(keys <= resolved_keys, f"resolved subset:{stage_name}")
            require(not (set(resolved_stage_by_key) & keys), f"resolved overlap:{stage_name}")
            for key in keys:
                resolved_stage_by_key[key] = stage_name
        inherited_resolved = resolved_keys - set(resolved_stage_by_key)
        require(len(inherited_resolved) == 1996, "pre-C30a resolved complement")
        for key in inherited_resolved:
            resolved_stage_by_key[key] = "INHERITED_RESOLVED_NONEXCLUDED_PRE_C30A"

        event_nonexcluded = 0
        disposition_counts: Counter[str] = Counter()
        terminal_counts: Counter[str] = Counter()
        writer = LedgerWriter(
            stage / "source_w_row_level_disposition_crosswalk.jsonl.gz",
            "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        )
        with writer:
            for cell in cells:
                origin = cell["origin_key"]
                if origin in stage_by_key:
                    disposition = "EXCLUDED"
                    disposition_stage = stage_by_key[origin]
                    terminal_class = "EARLIEST_PREFIX_EXCLUDED"
                    terminal_credit = 1
                else:
                    disposition = "RESOLVED_NONEXCLUDED"
                    disposition_stage = resolved_stage_by_key[origin]
                    terminal_class = "UNASSIGNED_COMPONENT_EVENT_OR_CEMETERY"
                    terminal_credit = 0
                    if cell["inherited_event_graph"] is not None:
                        event_nonexcluded += 1
                disposition_counts[disposition] += 1
                terminal_counts[terminal_class] += 1
                writer.write({
                    "schema": ROW_SCHEMA,
                    "origin_key": origin,
                    "cell_id": cell["cell_id"],
                    "compact_chart": cell["compact_chart"],
                    "formal_source_W_disposition": disposition,
                    "disposition_stage": disposition_stage,
                    "round144_terminal_class": terminal_class,
                    "round144_terminal_credit": terminal_credit,
                    "inherited_first_collision_event_graph": cell[
                        "inherited_event_graph"
                    ],
                    "scope_binding": {
                        "whole_original_source_W_origin": True,
                        "uniform_s_product_contains_s_zero_slice": True,
                        "compact_cell_geometry_from_C32": True,
                    },
                    "strict_nonpromotion": {
                        "component_connectivity_credit": 0,
                        "D02_credit": 0,
                        "D03_credit": 0,
                        "D04_credit": 0,
                        "Gate5_credit": 0,
                    },
                })
        require(disposition_counts == Counter({"EXCLUDED": 74812, "RESOLVED_NONEXCLUDED": 2020}), "crosswalk disposition")
        require(terminal_counts == Counter({"EARLIEST_PREFIX_EXCLUDED": 74812, "UNASSIGNED_COMPONENT_EVENT_OR_CEMETERY": 2020}), "terminal candidate")

        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                "PASS_76832_ROW_LEVEL_FORMAL_SOURCE_W_DISPOSITIONS__74812_"
                "EARLIEST_PREFIX_EXCLUDED__2020_COMPONENT_EVENT_OR_CEMETERY_"
                "UNRESOLVED__D02_STILL_BLOCKED"
            ),
            "C32_compact_atlas_authority": {
                "path": str(c32.resolve().relative_to(ROOT)),
                "result_object_sha256": c32_result["object_sha256"],
                "compact_cell_count": 76832,
            },
            "formal_source_W_authority": {
                "path": str(formal_path.resolve().relative_to(ROOT)),
                "object_sha256": formal["object_sha256"],
                "current_state": formal["current_state"],
            },
            "exclusion_chain": {
                "rows": cumulative,
                "rows_sha256": digest(cumulative),
                "stage_count": len(cumulative),
                "pairwise_disjoint": True,
                "all_keys_in_C32_cell_universe": True,
                "final_excluded": 74812,
            },
            "row_level_crosswalk": writer.descriptor(),
            "formal_disposition_census": dict(sorted(disposition_counts.items())),
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "TYPED_EVENT_GRAPH": 0,
                "EARLIEST_PREFIX_EXCLUDED": 74812,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "UNRESOLVED_COMPONENT_EVENT_OR_CEMETERY": 2020,
                "resolved_nonexcluded_with_inherited_first_collision_event_graph": event_nonexcluded,
                "formal_disposition_unresolved": 0,
                "terminal_unresolved": 2020,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "D02": "BLOCKED_BY_2020_NONEXCLUDED_COMPONENT_EVENT_OR_CEMETERY_ASSIGNMENTS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "required_next": (
                "partition the 2020 resolved-nonexcluded origins into connected-to-known, "
                "complete typed R1648 event graph, or source-grazing/cemetery classes; bind "
                "every connected class to the Round161 component-exit ledger"
            ),
            "provenance_file_sha256": {
                **provenance,
                str(round201_keys.resolve().relative_to(ROOT)): file_sha256(round201_keys.resolve()),
                str(c32.resolve().relative_to(ROOT) / "result.json"): file_sha256(c32.resolve() / "result.json"),
                str(formal_path.resolve().relative_to(ROOT)): file_sha256(formal_path.resolve()),
            },
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        manifest_members = sorted(stage.iterdir())
        (stage / "root_manifest.sha256").write_text(
            "".join(f"{file_sha256(path)}  {path.name}\n" for path in manifest_members),
            encoding="utf-8",
        )
        write_json(stage / "CROSSWALK_ONLY.lock", {
            "status": "PASS_CROSSWALK_ONLY__D02_NOT_PROMOTED",
            "result_object_sha256": result["object_sha256"],
            "root_manifest_sha256": file_sha256(stage / "root_manifest.sha256"),
        })
        os.replace(stage, output)
        return result
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--c32", type=Path, required=True)
    parser.add_argument("--formal-ledger", type=Path, required=True)
    parser.add_argument("--round201-keys", type=Path, required=True)
    parser.add_argument("--c30a-ledger", type=Path, required=True)
    parser.add_argument("--c30b-ledger", type=Path, required=True)
    parser.add_argument("--q9-producer", type=Path, required=True)
    parser.add_argument("--atlas-workers", type=int, default=2)
    args = parser.parse_args()
    result = build(
        args.output.resolve(), args.c32.resolve(), args.formal_ledger.resolve(),
        args.round201_keys.resolve(), args.c30a_ledger.resolve(),
        args.c30b_ledger.resolve(), args.q9_producer.resolve(), args.atlas_workers,
    )
    print(canonical_bytes({
        "status": result["status"],
        "object_sha256": result["object_sha256"],
        "output": str(args.output.resolve()),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
