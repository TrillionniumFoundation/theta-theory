#!/usr/bin/env python3
"""Read-only inventory and shard planner for the C43B0 zero-surface tranche.

C43B0 is deliberately narrower than a C43 producer.  It inventories exactly
the C41 residual primary outers which have no normalized surface obligations:

* 872 C1 outgoing-H1-factor outers;
* 2,482 collision-two wall-endpoint outers; and
* 89 collision-two evaluation-exception outers.

The resulting 3,443 sources have no pair-surface or surface-face incidence
work.  They are therefore the first adaptive closed-box tranche, modelled on
the already audited C42 P391 closure.  This program does not solve a source,
write a checkpoint, mint a candidate, or install an authority pointer.  It
only validates the frozen C41 bytes and emits a deterministic inventory or
pair-preserving shard plan on stdout.

The default shard-plan basis is the expected post-C42 work queue: the single
P391 source independently closed by C42 is omitted from execution, while the
raw C41 inventory remains reported as 3,443.  This is a planning overlay only;
it is not an authority claim and must not be used by a future formal producer
until the C42 candidate, audit, installation receipt, and commit seal have all
been independently validated.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import stat
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c43b0.d02-zero-surface-shard-plan.v1"
INVENTORY_SCHEMA = SCHEMA + ".inventory"
PLAN_SCHEMA = SCHEMA + ".plan"
SHARD_SCHEMA = SCHEMA + ".shard"
TASK_SCHEMA = SCHEMA + ".task"

C41_CANDIDATE = (
    RUNTIME
    / "candidates"
    / "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
)
C41_SCHEMA = "cm2.round306c41.d02-lower-strata-depth3-closure.v1"
C41_OBJECT = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C41_STATUS = (
    "PASS_C41_DEPTH3_STRICT_ROUTER_PARTIAL__91879_AMBIENT_LEAVES__"
    "572_WHOLE_CELLS_TERMINAL__1152_FORMAL_UNRESOLVED"
)
C41_MANIFEST_FILE_SHA256 = (
    "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
)

C42_OBJECT = "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
C42_AUDIT_OBJECT = (
    "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c"
)
C42_TARGET_OUTER_ID = (
    "c41-c2-outer:6711f208eef9b4a3e63d73649ffed9e296c0de107c5f92185489d287908fbad3"
)
C42_TARGET_OUTER_ROW_SHA256 = (
    "3e336912ccc519e429c98449138fcfd4b197c631a67029fe6271d88d1123f469"
)
C42_TARGET_AMBIENT_ID = (
    "c41-ambient:01bcc14671eacb7628822945582e307e70cf9fbeeff7f3f47adc6e9597f3ab38"
)
C42_TARGET_AMBIENT_ROW_SHA256 = (
    "49b986a5ba33c0fba075e854feb5316348815199e56e2b93e1ab224898c6c0e8"
)
C42_TARGET_PAIR_INDEX = 391

B0_CLASSES = {
    "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER": {
        "category": "C1_OUTGOING_H1_FACTOR",
        "ledger": "c1_h1_surface_outers",
        "id_field": "c1_h1_surface_outer_id",
        "expected_count": 872,
        "work_units": 6,
    },
    "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER": {
        "category": "C2_WALL_ENDPOINT",
        "ledger": "c2_surface_outers",
        "id_field": "c2_surface_outer_id",
        "expected_count": 2_482,
        "work_units": 4,
    },
    "UNRESOLVED_C41_COLLISION2_EVALUATION_EXCEPTION_OUTER": {
        "category": "C2_EVALUATION_EXCEPTION",
        "ledger": "c2_surface_outers",
        "id_field": "c2_surface_outer_id",
        "expected_count": 89,
        "work_units": 8,
    },
}
EXPECTED_B0_COUNT = 3_443
EXPECTED_B0_PAIR_COUNT = 248
EXPECTED_WHOLE_PAIR_GAIN_PAIR_COUNT = 12
EXPECTED_WHOLE_PAIR_GAIN_TASK_COUNT = 67
EXPECTED_SOLE_DEFICIT_PAIR_COUNT = 6
EXPECTED_WHOLE_PAIR_GAIN_HISTOGRAM = {
    "1": 6,
    "2": 1,
    "6": 1,
    "10": 2,
    "15": 1,
    "18": 1,
}
EXPECTED_SOLE_DEFICIT_PAIRS = [97, 211, 391, 592, 664, 715]

# A future producer should run whole-parent gain tasks first, then fail-closed
# evaluation replays, then the two regular zero-surface families.  Priority is
# a scheduling hint only and carries no mathematical credit.
PRIORITY_ORDER = {
    "WHOLE_PAIR_GAIN": 0,
    "C2_EVALUATION_EXCEPTION": 1,
    "C2_WALL_ENDPOINT": 2,
    "C1_OUTGOING_H1_FACTOR": 3,
}

HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class PlannerError(RuntimeError):
    """Fail-closed planner validation error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise PlannerError(label)


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


def strict_pairs(label: str):
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, f"duplicate JSON key:{label}:{key}")
            result[key] = value
        return result

    return pairs


def reject_float(label: str):
    def reject(value: str) -> None:
        raise PlannerError(f"noninteger JSON number:{label}:{value}")

    return reject


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
            f"JSON encoding:{label}")
    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=strict_pairs(label),
        parse_float=reject_float(label),
        parse_constant=reject_float(label),
    )
    require(type(value) is dict, f"top-level JSON object:{label}")
    return value


def regular_single_link(path: Path, label: str) -> os.stat_result:
    value = path.lstat()
    require(
        stat.S_ISREG(value.st_mode)
        and not path.is_symlink()
        and value.st_nlink == 1,
        f"regular single-link file:{label}:{path}",
    )
    return value


def stable_read(path: Path, label: str) -> bytes:
    before = regular_single_link(path, label)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            chunks.append(block)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after = regular_single_link(path, label)
    identity_before = (
        before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns
    )
    identity_fd = (
        after_fd.st_dev, after_fd.st_ino, after_fd.st_size,
        after_fd.st_mtime_ns,
    )
    identity_after = (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns
    )
    require(identity_before == identity_fd == identity_after,
            f"stable file capture:{label}:{path}")
    raw = b"".join(chunks)
    require(len(raw) == before.st_size, f"stable file size:{label}:{path}")
    return raw


def strict_json_file(path: Path, label: str) -> dict[str, Any]:
    raw = stable_read(path, label)
    require(raw == raw.strip() + b"\n", f"canonical newline:{label}")
    value = strict_json_bytes(raw, label)
    require(canonical(value) + b"\n" == raw, f"canonical JSON:{label}")
    return value


def validate_self_object(
    value: dict[str, Any], expected: str, label: str
) -> None:
    semantic = dict(value)
    observed = semantic.pop("object_sha256", None)
    require(
        observed == expected
        and HEX64.fullmatch(expected) is not None
        and digest(semantic) == expected,
        f"self-hashed object:{label}",
    )


def validate_manifest(candidate: Path) -> dict[str, str]:
    manifest_path = candidate / "root_manifest.sha256"
    raw = stable_read(manifest_path, "C41 root manifest")
    require(
        hashlib.sha256(raw).hexdigest() == C41_MANIFEST_FILE_SHA256,
        "C41 root manifest file pin",
    )
    text = raw.decode("ascii", "strict")
    require(text.endswith("\n") and "\r" not in text,
            "C41 root manifest newline")
    rows: dict[str, str] = {}
    for ordinal, line in enumerate(text.splitlines()):
        require(line.count("  ") == 1,
                f"C41 manifest syntax:{ordinal}")
        expected, name = line.split("  ", 1)
        require(
            HEX64.fullmatch(expected) is not None
            and name not in rows
            and name != "root_manifest.sha256"
            and Path(name).name == name,
            f"C41 manifest row:{ordinal}",
        )
        rows[name] = expected
    observed_names = {
        path.name for path in candidate.iterdir()
        if path.name != "root_manifest.sha256"
    }
    require(set(rows) == observed_names, "C41 manifest exact inventory")
    for name, expected in rows.items():
        path = candidate / name
        regular_single_link(path, "C41 manifest payload")
        require(file_sha256(path) == expected,
                f"C41 manifest payload hash:{name}")
    return rows


def iter_ledger(
    candidate: Path,
    descriptor: dict[str, Any],
    ledger_name: str,
) -> Iterator[dict[str, Any]]:
    required = {
        "filename", "order", "row_count", "row_hash_line_sequence_sha256",
        "sha256", "size",
    }
    require(set(descriptor) == required, f"ledger descriptor keys:{ledger_name}")
    path = candidate / descriptor["filename"]
    before = regular_single_link(path, f"ledger:{ledger_name}")
    require(
        before.st_size == descriptor["size"]
        and file_sha256(path) == descriptor["sha256"],
        f"ledger descriptor bytes:{ledger_name}",
    )
    sequence = hashlib.sha256()
    count = 0
    with gzip.open(path, "rb") as stream:
        for raw in stream:
            label = f"{ledger_name}:{count}"
            require(raw.endswith(b"\n"), f"ledger newline:{label}")
            row = strict_json_bytes(raw, label)
            require(canonical(row) + b"\n" == raw,
                    f"canonical ledger row:{label}")
            semantic = dict(row)
            observed = semantic.pop("row_sha256", None)
            require(
                type(observed) is str
                and HEX64.fullmatch(observed) is not None
                and observed == digest(semantic),
                f"ledger row closure:{label}",
            )
            sequence.update((observed + "\n").encode("ascii"))
            count += 1
            yield row
    after = regular_single_link(path, f"ledger:{ledger_name}")
    require(
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
        f"stable ledger capture:{ledger_name}",
    )
    require(
        count == descriptor["row_count"]
        and sequence.hexdigest()
        == descriptor["row_hash_line_sequence_sha256"],
        f"ledger descriptor closure:{ledger_name}",
    )


def load_c41(candidate: Path) -> dict[str, Any]:
    candidate = candidate.resolve()
    require(candidate == C41_CANDIDATE.resolve(),
            "planner accepts only the pinned C41 candidate path")
    value = candidate.lstat()
    require(stat.S_ISDIR(value.st_mode) and not candidate.is_symlink(),
            "C41 candidate directory")
    validate_manifest(candidate)
    result = strict_json_file(candidate / "result.json", "C41 result")
    validate_self_object(result, C41_OBJECT, "C41 result")
    require(
        result.get("schema") == C41_SCHEMA
        and result.get("status") == C41_STATUS,
        "C41 schema/status pins",
    )
    required_ledgers = {
        "c1_h1_surface_outers",
        "c2_surface_outers",
        "routed_ambient_cells",
    }
    require(required_ledgers <= set(result.get("ledgers", {})),
            "C41 planner ledger inventory")
    return result


def base_task(
    row: dict[str, Any], ledger_name: str, id_field: str,
) -> dict[str, Any]:
    classification = row["residual_classification"]
    metadata = B0_CLASSES[classification]
    require(
        metadata["ledger"] == ledger_name
        and metadata["id_field"] == id_field
        and row["normalized_surface_count"] == 0
        and row["normalized_surfaces"] == []
        and row["carrier_existence_status"]
        == "UNRESOLVED_STRATIFIED_SURFACE_OUTER"
        and row["certified_carrier_dimension"] is None
        and row["candidate_intersection_rank_status"] is None
        and row["ambient_or_whole_parent_credit"] == 0
        and row["D02_gate_credit"] == 0,
        f"B0 exact zero-surface semantics:{row[id_field]}",
    )
    return {
        "schema": TASK_SCHEMA,
        "source_ledger": ledger_name,
        "source_outer_id": row[id_field],
        "source_outer_row_sha256": row["row_sha256"],
        "pair_index": row["pair_index"],
        "c40_source_leaf_id": row["c40_source_leaf_id"],
        "descendant_path": row["descendant_path"],
        "residual_classification": classification,
        "category": metadata["category"],
        "normalized_surface_count": 0,
        "pair_incidence_count": 0,
        "surface_face_incidence_count": 0,
        "base_work_units": metadata["work_units"],
    }


def scan_primary_outers(
    candidate: Path, result: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    class_counts: Counter[str] = Counter()
    for ledger_name, id_field in (
        ("c1_h1_surface_outers", "c1_h1_surface_outer_id"),
        ("c2_surface_outers", "c2_surface_outer_id"),
    ):
        for row in iter_ledger(
            candidate, result["ledgers"][ledger_name], ledger_name
        ):
            classification = row["residual_classification"]
            if classification not in B0_CLASSES:
                continue
            # WALL_ENDPOINT has another 180 rows carrying one or two
            # normalized surfaces.  Those belong to the later arrangement
            # tranche, not B0; the exact post-filter census below prevents a
            # silent widening or narrowing of this zero-surface selection.
            if row["normalized_surface_count"] != 0:
                continue
            task = base_task(row, ledger_name, id_field)
            outer_id = task["source_outer_id"]
            require(outer_id not in tasks, "B0 outer ID uniqueness")
            tasks[outer_id] = task
            class_counts[classification] += 1
    expected = {
        classification: metadata["expected_count"]
        for classification, metadata in B0_CLASSES.items()
    }
    require(
        len(tasks) == EXPECTED_B0_COUNT
        and dict(class_counts) == expected,
        "exact B0 primary-outer census",
    )
    return tasks


def attach_ambient_sources(
    candidate: Path,
    result: dict[str, Any],
    tasks: dict[str, dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    pairs: dict[int, dict[str, Any]] = defaultdict(lambda: {
        "all_nonterminal_count": 0,
        "collision3_ready_count": 0,
        "b0_task_ids": [],
        "unresolved_fraction": Q(0),
    })
    seen: set[str] = set()
    for row in iter_ledger(
        candidate,
        result["ledgers"]["routed_ambient_cells"],
        "routed_ambient_cells",
    ):
        pair_index = row["pair_index"]
        require(type(pair_index) is int and 0 <= pair_index < 862,
                "C41 ambient pair range")
        pair = pairs[pair_index]
        if row["disposition_family"] == "TERMINAL_EXCLUDED":
            continue
        pair["all_nonterminal_count"] += 1
        fraction = Q(row["parent_volume_fraction"])
        require(fraction > 0, "positive nonterminal parent fraction")
        pair["unresolved_fraction"] += fraction
        if row["disposition_family"] == "COLLISION3_READY":
            pair["collision3_ready_count"] += 1
            continue
        require(row["disposition_family"] == "RESIDUAL_OUTER",
                "C41 ambient disposition enum")
        obligations = row["obligation_ids"]
        require(type(obligations) is list and obligations,
                "C41 residual primary obligation")
        task = tasks.get(obligations[0])
        if task is None:
            continue
        outer_id = task["source_outer_id"]
        require(outer_id not in seen, "B0 ambient source uniqueness")
        require(
            task["pair_index"] == pair_index
            and task["c40_source_leaf_id"] == row["c40_source_leaf_id"]
            and task["descendant_path"] == row["path"]
            and task["residual_classification"]
            == row["residual_classification"]
            and row["local_round144_terminal_credit"] == 0
            and row["lower_dimensional_ambient_credit"] == 0
            and row["collision3_ready_credit"] == 0
            and row["D02_gate_credit"] == 0,
            f"B0 primary/ambient foreign-key closure:{outer_id}",
        )
        task.update({
            "source_ambient_id": row["c41_ambient_cell_id"],
            "source_ambient_row_sha256": row["row_sha256"],
            "source_parent_volume_fraction": row["parent_volume_fraction"],
            "closed_representative_box": row["closed_representative_box"],
            "closed_reflected_box": row["closed_reflected_box"],
            "representative_cell_id": row["representative_cell_id"],
            "reflected_cell_id": row["reflected_cell_id"],
        })
        pair["b0_task_ids"].append(outer_id)
        seen.add(outer_id)
    require(seen == set(tasks), "every B0 outer has exactly one ambient source")

    touched = {pair for pair, value in pairs.items() if value["b0_task_ids"]}
    require(len(touched) == EXPECTED_B0_PAIR_COUNT, "exact B0 pair census")
    whole_gain: list[int] = []
    histogram: Counter[str] = Counter()
    gain_task_count = 0
    for pair_index in sorted(touched):
        value = pairs[pair_index]
        value["b0_task_ids"].sort()
        b0_count = len(value["b0_task_ids"])
        whole = (
            value["all_nonterminal_count"] == b0_count
            and value["collision3_ready_count"] == 0
        )
        value["b0_closure_would_make_whole_pair"] = whole
        value["unresolved_fraction"] = qstr(value["unresolved_fraction"])
        if whole:
            whole_gain.append(pair_index)
            histogram[str(b0_count)] += 1
            gain_task_count += b0_count
    require(
        len(whole_gain) == EXPECTED_WHOLE_PAIR_GAIN_PAIR_COUNT
        and gain_task_count == EXPECTED_WHOLE_PAIR_GAIN_TASK_COUNT
        and dict(sorted(histogram.items()))
        == EXPECTED_WHOLE_PAIR_GAIN_HISTOGRAM,
        "exact B0 whole-pair gain frontier",
    )
    sole = [
        pair_index for pair_index in whole_gain
        if len(pairs[pair_index]["b0_task_ids"]) == 1
    ]
    require(
        sole == EXPECTED_SOLE_DEFICIT_PAIRS
        and len(sole) == EXPECTED_SOLE_DEFICIT_PAIR_COUNT,
        "exact B0 sole-deficit pairs",
    )
    return dict(pairs)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def finalize_tasks(
    tasks: dict[str, dict[str, Any]],
    pairs: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for outer_id in sorted(tasks):
        task = dict(tasks[outer_id])
        pair = pairs[task["pair_index"]]
        category = task["category"]
        priority = (
            "WHOLE_PAIR_GAIN"
            if pair["b0_closure_would_make_whole_pair"]
            else category
        )
        task.update({
            "priority_class": priority,
            "priority_rank": PRIORITY_ORDER[priority],
            "pair_all_nonterminal_count": pair["all_nonterminal_count"],
            "pair_b0_task_count": len(pair["b0_task_ids"]),
            "pair_collision3_ready_count": pair["collision3_ready_count"],
            "b0_closure_would_make_whole_pair": pair[
                "b0_closure_would_make_whole_pair"
            ],
            "already_closed_by_C42": outer_id == C42_TARGET_OUTER_ID,
            "planning_only": True,
            "D02_gate_credit": 0,
        })
        semantic = dict(task)
        task["task_id"] = "c43b0-task:" + digest(semantic)
        rows.append(task)
    rows.sort(key=lambda row: (
        row["priority_rank"], row["pair_index"], row["descendant_path"],
        row["source_outer_id"],
    ))
    require(
        len(rows) == EXPECTED_B0_COUNT
        and sum(row["already_closed_by_C42"] for row in rows) == 1,
        "final B0 task census and C42 overlay target",
    )
    target = next(row for row in rows if row["already_closed_by_C42"])
    require(
        target["pair_index"] == C42_TARGET_PAIR_INDEX
        and target["source_outer_row_sha256"]
        == C42_TARGET_OUTER_ROW_SHA256
        and target["source_ambient_id"] == C42_TARGET_AMBIENT_ID
        and target["source_ambient_row_sha256"]
        == C42_TARGET_AMBIENT_ROW_SHA256,
        "exact C42 planning overlay target",
    )
    return rows


def build_inventory(candidate: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = load_c41(candidate)
    task_index = scan_primary_outers(candidate, result)
    pair_index = attach_ambient_sources(candidate, result, task_index)
    tasks = finalize_tasks(task_index, pair_index)
    class_counts = Counter(row["residual_classification"] for row in tasks)
    category_counts = Counter(row["category"] for row in tasks)
    priority_counts = Counter(row["priority_class"] for row in tasks)
    whole_pairs = sorted({
        row["pair_index"] for row in tasks
        if row["b0_closure_would_make_whole_pair"]
    })
    sole_pairs = sorted({
        row["pair_index"] for row in tasks
        if row["b0_closure_would_make_whole_pair"]
        and row["pair_b0_task_count"] == 1
    })
    post_c42 = [row for row in tasks if not row["already_closed_by_C42"]]
    inventory: dict[str, Any] = {
        "schema": INVENTORY_SCHEMA,
        "status": "PASS_READ_ONLY_C43B0_EXACT_INVENTORY",
        "C41_input": {
            "candidate_path": str(candidate.resolve().relative_to(ROOT)),
            "candidate_object_sha256": result["object_sha256"],
            "candidate_status": result["status"],
            "root_manifest_file_sha256": C41_MANIFEST_FILE_SHA256,
        },
        "raw_C41_B0": {
            "task_count": len(tasks),
            "pair_count": len({row["pair_index"] for row in tasks}),
            "classification_census": dict(sorted(class_counts.items())),
            "category_census": dict(sorted(category_counts.items())),
            "priority_census": dict(sorted(priority_counts.items())),
            "zero_normalized_surface_count": len(tasks),
            "pair_incidence_count": 0,
            "surface_face_incidence_count": 0,
        },
        "whole_pair_gain_frontier": {
            "pair_count": len(whole_pairs),
            "task_count": sum(
                row["b0_closure_would_make_whole_pair"] for row in tasks
            ),
            "pair_indices": whole_pairs,
            "sole_deficit_pair_count": len(sole_pairs),
            "sole_deficit_pair_indices": sole_pairs,
        },
        "C42_planning_overlay": {
            "candidate_object_sha256": C42_OBJECT,
            "independent_audit_object_sha256": C42_AUDIT_OBJECT,
            "closed_source_outer_id": C42_TARGET_OUTER_ID,
            "closed_source_ambient_id": C42_TARGET_AMBIENT_ID,
            "closed_pair_index": C42_TARGET_PAIR_INDEX,
            "raw_task_count": len(tasks),
            "expected_post_C42_task_count": len(post_c42),
            "overlay_is_authority": False,
            "formal_use_requires_installed_C42_commit_seal": True,
        },
        "strict_nonpromotion": {
            "planner_writes_runtime_state": False,
            "planner_mints_candidate": False,
            "planner_installs_pointer": False,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    inventory["inventory_sha256"] = digest(inventory)
    return inventory, tasks


def task_projection(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in (
            "task_id", "source_ledger", "source_outer_id",
            "source_outer_row_sha256", "source_ambient_id",
            "source_ambient_row_sha256", "pair_index", "descendant_path",
            "source_parent_volume_fraction", "residual_classification",
            "category", "priority_class", "priority_rank",
            "base_work_units", "b0_closure_would_make_whole_pair",
            "already_closed_by_C42", "D02_gate_credit",
        )
    }


def assign_shards(
    tasks: list[dict[str, Any]], shard_count: int, basis: str,
) -> list[dict[str, Any]]:
    require(type(shard_count) is int and 1 <= shard_count <= 128,
            "shard count in [1,128]")
    if basis == "post-c42":
        selected = [row for row in tasks if not row["already_closed_by_C42"]]
    else:
        require(basis == "c41", "plan basis enum")
        selected = list(tasks)
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        grouped[row["pair_index"]].append(row)
    groups: list[tuple[int, int, int, list[dict[str, Any]]]] = []
    for pair_index, rows in grouped.items():
        rows.sort(key=lambda row: (
            row["priority_rank"], row["descendant_path"],
            row["source_outer_id"],
        ))
        priority = min(row["priority_rank"] for row in rows)
        work = sum(row["base_work_units"] for row in rows)
        groups.append((priority, -work, pair_index, rows))
    groups.sort(key=lambda item: (item[0], item[1], item[2]))

    buckets: list[list[dict[str, Any]]] = [[] for _ in range(shard_count)]
    loads = [0] * shard_count
    pair_sets: list[set[int]] = [set() for _ in range(shard_count)]
    for _priority, negative_work, pair_index, rows in groups:
        work = -negative_work
        shard = min(
            range(shard_count),
            key=lambda index: (loads[index], len(buckets[index]), index),
        )
        buckets[shard].extend(rows)
        pair_sets[shard].add(pair_index)
        loads[shard] += work

    observed_pairs: dict[int, int] = {}
    observed_tasks: set[str] = set()
    shards: list[dict[str, Any]] = []
    for shard_index, rows in enumerate(buckets):
        rows.sort(key=lambda row: (
            row["priority_rank"], row["pair_index"],
            row["descendant_path"], row["source_outer_id"],
        ))
        for row in rows:
            require(row["task_id"] not in observed_tasks,
                    "shard task uniqueness")
            observed_tasks.add(row["task_id"])
            prior = observed_pairs.setdefault(row["pair_index"], shard_index)
            require(prior == shard_index, "pair must not cross shards")
        projections = [task_projection(row) for row in rows]
        category = Counter(row["category"] for row in rows)
        priority = Counter(row["priority_class"] for row in rows)
        semantic: dict[str, Any] = {
            "schema": SHARD_SCHEMA,
            "shard_index": shard_index,
            "pair_count": len(pair_sets[shard_index]),
            "pair_indices": sorted(pair_sets[shard_index]),
            "task_count": len(rows),
            "estimated_work_units": loads[shard_index],
            "category_census": dict(sorted(category.items())),
            "priority_census": dict(sorted(priority.items())),
            "ordered_task_projection_sha256": digest(projections),
            "first_task_id": rows[0]["task_id"] if rows else None,
            "last_task_id": rows[-1]["task_id"] if rows else None,
        }
        semantic["shard_id"] = "c43b0-shard:" + digest(semantic)
        semantic["_tasks"] = projections
        shards.append(semantic)
    require(
        len(observed_tasks) == len(selected)
        and len(observed_pairs) == len(grouped)
        and sum(len(row["_tasks"]) for row in shards) == len(selected),
        "shard exact task/pair conservation",
    )
    return shards


def build_plan(
    inventory: dict[str, Any],
    tasks: list[dict[str, Any]],
    shard_count: int,
    basis: str,
    emit_tasks: bool,
) -> dict[str, Any]:
    shards = assign_shards(tasks, shard_count, basis)
    full_task_digest = digest([
        task
        for shard in shards
        for task in shard["_tasks"]
    ])
    public_shards: list[dict[str, Any]] = []
    for shard in shards:
        row = dict(shard)
        task_rows = row.pop("_tasks")
        if emit_tasks:
            row["tasks"] = task_rows
        public_shards.append(row)
    selected_count = EXPECTED_B0_COUNT - int(basis == "post-c42")
    plan: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "status": "PASS_READ_ONLY_C43B0_PAIR_PRESERVING_SHARD_PLAN",
        "basis": basis,
        "basis_semantics": (
            "RAW_AUDITED_C41_B0"
            if basis == "c41"
            else "EXPECTED_POST_C42_QUEUE__PLANNING_OVERLAY_NOT_AUTHORITY"
        ),
        "inventory_sha256": inventory["inventory_sha256"],
        "raw_C41_B0_task_count": EXPECTED_B0_COUNT,
        "planned_task_count": selected_count,
        "shard_count": shard_count,
        "nonempty_shard_count": sum(row["task_count"] > 0 for row in shards),
        "pair_preserving_partition": True,
        "ordered_full_task_projection_sha256": full_task_digest,
        "task_rows_embedded": emit_tasks,
        "shards": public_shards,
        "execution_contract": {
            "adaptive_depth_has_no_mathematical_fixed_cap": True,
            "budget_exhaustion_yields_checkpoint_not_candidate": True,
            "accepted_terminal_classes": [
                "EARLIEST_PREFIX_EXCLUDED",
                "COLLISION3_READY",
                "CONNECTED_TO_KNOWN",
                "SOURCE_GRAZING_OR_CEMETERY",
            ],
            "source_exit_requires_prefix_free_exact_fraction_conservation": True,
            "source_exit_requires_closed_face_corner_owner_census": True,
            "source_exit_requires_reflection_transport": True,
            "formal_run_requires_installed_C42_commit_seal": True,
        },
        "strict_nonpromotion": {
            "plan_is_authority": False,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    plan["plan_sha256"] = digest(plan)
    return plan


def synthetic_task(pair_index: int, ordinal: int, priority: int) -> dict[str, Any]:
    priority_class = next(
        key for key, value in PRIORITY_ORDER.items() if value == priority
    )
    source = f"synthetic:{pair_index}:{ordinal}"
    task = {
        "task_id": "c43b0-task:" + hashlib.sha256(source.encode()).hexdigest(),
        "source_ledger": "synthetic",
        "source_outer_id": source,
        "source_outer_row_sha256": hashlib.sha256((source + ":o").encode()).hexdigest(),
        "source_ambient_id": source + ":ambient",
        "source_ambient_row_sha256": hashlib.sha256((source + ":a").encode()).hexdigest(),
        "pair_index": pair_index,
        "descendant_path": format(ordinal, "b"),
        "source_parent_volume_fraction": "1/8",
        "residual_classification": "SYNTHETIC",
        "category": "C2_WALL_ENDPOINT",
        "priority_class": priority_class,
        "priority_rank": priority,
        "base_work_units": ordinal + 1,
        "b0_closure_would_make_whole_pair": priority == 0,
        "already_closed_by_C42": False,
        "D02_gate_credit": 0,
    }
    return task


def self_test() -> dict[str, Any]:
    require(sum(
        metadata["expected_count"] for metadata in B0_CLASSES.values()
    ) == EXPECTED_B0_COUNT, "B0 constant census")
    require(
        sorted(PRIORITY_ORDER.values()) == list(range(len(PRIORITY_ORDER))),
        "priority ranks contiguous",
    )
    require(
        all(HEX64.fullmatch(value) is not None for value in (
            C41_OBJECT, C41_MANIFEST_FILE_SHA256, C42_OBJECT,
            C42_AUDIT_OBJECT, C42_TARGET_OUTER_ROW_SHA256,
            C42_TARGET_AMBIENT_ROW_SHA256,
        )),
        "all authority constants are SHA256",
    )
    probe = {"z": ["1/2", 3], "a": {"x": True}}
    require(canonical(probe) == b'{"a":{"x":true},"z":["1/2",3]}',
            "canonical codec")
    require(digest(probe) == hashlib.sha256(canonical(probe)).hexdigest(),
            "canonical digest")
    require(Q("1/8") + Q("3/8") == Q("1/2"), "exact Fraction codec")

    synthetic = [
        synthetic_task(2, 0, 2),
        synthetic_task(2, 1, 2),
        synthetic_task(7, 0, 0),
        synthetic_task(11, 0, 1),
        synthetic_task(11, 1, 1),
        synthetic_task(19, 0, 3),
    ]
    first = assign_shards(synthetic, 3, "c41")
    second = assign_shards(list(reversed(synthetic)), 3, "c41")
    projection = lambda values: [
        {
            key: value for key, value in row.items() if key != "_tasks"
        } | {"tasks": row["_tasks"]}
        for row in values
    ]
    require(projection(first) == projection(second),
            "shard plan input-order independence")
    owner: dict[int, int] = {}
    for shard in first:
        for task in shard["_tasks"]:
            prior = owner.setdefault(task["pair_index"], shard["shard_index"])
            require(prior == shard["shard_index"], "synthetic pair preservation")
    require(sum(row["task_count"] for row in first) == len(synthetic),
            "synthetic task conservation")
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C43B0_READ_ONLY_PLANNER_SELF_TEST",
        "static_B0_task_count": EXPECTED_B0_COUNT,
        "static_B0_pair_count": EXPECTED_B0_PAIR_COUNT,
        "synthetic_task_count": len(synthetic),
        "synthetic_pair_count": len(owner),
        "synthetic_shard_count": len(first),
        "input_order_independent": True,
        "pair_preserving_partition": True,
        "filesystem_writes_performed": 0,
        "authority_claimed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only C43B0 inventory and pair-preserving shard planner"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inventory", action="store_true")
    mode.add_argument("--shard-plan", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate", type=Path, default=C41_CANDIDATE)
    parser.add_argument("--shards", type=int, default=32)
    parser.add_argument("--basis", choices=("c41", "post-c42"),
                        default="post-c42")
    parser.add_argument(
        "--emit-tasks",
        action="store_true",
        help="embed ordered task projections in each shard",
    )
    arguments = parser.parse_args()
    if arguments.self_test:
        require(not arguments.emit_tasks, "--emit-tasks requires --shard-plan")
        print(canonical(self_test()).decode("utf-8"))
        return 0
    inventory, tasks = build_inventory(arguments.candidate.resolve())
    if arguments.inventory:
        require(not arguments.emit_tasks, "--emit-tasks requires --shard-plan")
        print(canonical(inventory).decode("utf-8"))
        return 0
    plan = build_plan(
        inventory, tasks, arguments.shards, arguments.basis,
        arguments.emit_tasks,
    )
    print(canonical(plan).decode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PlannerError as error:
        print(
            canonical({
                "schema": SCHEMA + ".failure",
                "status": "FAIL_CLOSED_C43B0_PLANNER",
                "error": str(error),
                "authority_claimed": False,
            }).decode("utf-8"),
            file=os.sys.stderr,
        )
        raise SystemExit(1)
