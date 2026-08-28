#!/usr/bin/env python3
"""Read-only generalized exact-behind reduction over the frozen Round184 tail.

The outcome-blind input is exactly the 596 DELTA_H_OR_MULTI_NO_Q plus 54
COMPACT_Q_PRESENT origins in the pinned Round184 priority registry.  Every
Round180 depth-4 final row is rebuilt from pinned geometry.  Within a row,
unresolved candidates are considered in target-id order and deleted one at a
time only when the whole-box proof

    ell < 0 and distance^2 - R^2 = ell^2 - Delta > 0

holds.  After every deletion the remaining records are independently
reclassified and their terminal disposition, owner, and chart are recomputed.

Compact-q/source-grazing rows and physical source seams remain independent
strata and cannot receive credit from candidate deletion.  This probe has no
output path, performs no filesystem writes, reports progress on stderr,
prints one final JSON document on stdout, and mutates no formal ledger.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

from flint import ctx


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round197.source-w-generalized-exact-behind-reduction-probe.v1"
MAX_INPUT_BYTES = 8 * 1024 * 1024

ROUND194_NAME = "cm2_round194_source_w_exact_behind_target_removal_probe.py"
ROUND194_SHA256 = (
    "d4eb7ba9f2932083da2266a0ae67df7b4b941625472849fb9a52cbdc8e7c371f"
)
ROUND184_REGISTRY_ROWS_SHA256 = (
    "d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e"
)

DELTA_MULTI_CLASS = "DELTA_H_OR_MULTI_NO_Q"
COMPACT_CLASS = "COMPACT_Q_PRESENT"
SELECTED_CLASSES = (DELTA_MULTI_CLASS, COMPACT_CLASS)
EXPECTED_CLASS_ORIGIN_COUNT = {
    DELTA_MULTI_CLASS: 596,
    COMPACT_CLASS: 54,
}
EXPECTED_CLASS_ORIGIN_KEYS_SHA256 = {
    DELTA_MULTI_CLASS:
        "b6440ea91a3fd331cf55b1a5e7a530c3ca688d48a3e2ec0897f1981d05edbd1d",
    COMPACT_CLASS:
        "d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b",
}
EXPECTED_CLASS_CHILD_COUNT = {
    DELTA_MULTI_CLASS: 161442,
    COMPACT_CLASS: 21334,
}
EXPECTED_SELECTED_ORIGIN_COUNT = 650
EXPECTED_SELECTED_ORIGIN_KEYS_SHA256 = (
    "36c2f93e9252373ee95fd4574c84f8d8084b1d6cd2e4467ebb6e6670d48e7467"
)
EXPECTED_SELECTED_CHILD_COUNT = 182776

CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
FULL_P = "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
MULTI = "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
COMPACT_Q = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
TYPED_DOUBLE = "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
PAIR_SUPPORT = (CLIPPED, FULL_P)
EXPECTED_PAIR_ORIGIN_COUNT = 210
EXPECTED_PAIR_ORIGIN_KEYS_SHA256 = (
    "35041af235b0eb1e9793b636942446cb6dc6329c9193df1afbf0b4cbf33732b1"
)
EXPECTED_PAIR_CHILD_COUNT = 34816

UNRESOLVED_CLASSES = {
    "unresolved_discriminant",
    "unresolved_root_sign",
}
Q_HOLDOUT_REASON = "SOURCE_GRAZING_COMPACT_Q_INDEPENDENT_STRATUM"
NO_DELETION_REASON = "NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE"
REDUCED_UNRESOLVED_REASON = "REDUCED_REMAINING_RECORD_DISPOSITION_UNRESOLVED"
REDUCED_LIVE_REASON = "REDUCED_REMAINING_RECORD_DISPOSITION_LIVE"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[Any, Q]) -> dict[str, str]:
    return {
        str(key): str(item) for key, item in sorted(value.items())
    }


def nested_counter_map(
    value: dict[str, Counter[Any]],
) -> dict[str, dict[str, int]]:
    return {
        key: map_counter(counter)
        for key, counter in sorted(value.items())
    }


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def read_regular(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(stat.S_ISREG(status.st_mode), f"input regular:{absolute.name}")
    require(not absolute.is_symlink(), f"input symlink:{absolute.name}")
    require(status.st_nlink == 1, f"input hardlink:{absolute.name}")
    require(
        0 < status.st_size <= MAX_INPUT_BYTES,
        f"input size:{absolute.name}",
    )
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino),
            f"input race:{absolute.name}",
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"opened input type:{absolute.name}",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(chunk), f"short input:{absolute.name}")
            chunks.append(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    require(len(raw) == status.st_size, f"input byte count:{absolute.name}")
    return raw


def pin_round194() -> None:
    require(
        hashlib.sha256(read_regular(HERE / ROUND194_NAME)).hexdigest()
        == ROUND194_SHA256,
        "Round194 source pin",
    )


pin_round194()
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r194 = importlib.import_module(
    "cm2_round194_source_w_exact_behind_target_removal_probe"
)
pin_round194()
r193 = r194.r193
r190 = r194.r190
r187 = r194.r187
r180 = r194.r180
r176 = r194.r176


class ListDigest:
    def __init__(self) -> None:
        self._hasher = hashlib.sha256()
        self._hasher.update(b"[")
        self._count = 0

    def add(self, value: Any) -> None:
        if self._count:
            self._hasher.update(b",")
        self._hasher.update(canonical(value).encode())
        self._count += 1

    def finish(self) -> str:
        self._hasher.update(b"]")
        return self._hasher.hexdigest()

    @property
    def count(self) -> int:
        return self._count


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def check_chain_and_select() -> dict[str, Any]:
    require(
        Path(r194.__file__).resolve() == (HERE / ROUND194_NAME).resolve(),
        "Round194 module identity",
    )
    inputs = r194.check_chain()
    registry = inputs["result"]["priority_registry"]
    rows = registry["rows"]
    require(
        registry["row_count"] == 1444
        and registry["rows_sha256"] == ROUND184_REGISTRY_ROWS_SHA256
        and digest(rows) == ROUND184_REGISTRY_ROWS_SHA256,
        "Round184 frozen registry",
    )
    selected = [
        row for row in rows
        if row["priority_class"] in SELECTED_CLASSES
    ]
    require(
        all(
            row["selection_uses_new_closure_outcome"] is False
            and row["row_sha256"]
            == digest({
                key: value for key, value in row.items()
                if key != "row_sha256"
            })
            for row in selected
        ),
        "outcome-blind selected rows and self digests",
    )
    class_keys = {
        class_name: sorted(
            row["origin_key"]
            for row in selected
            if row["priority_class"] == class_name
        )
        for class_name in SELECTED_CLASSES
    }
    selected_keys = sorted(row["origin_key"] for row in selected)
    require(
        len(selected) == EXPECTED_SELECTED_ORIGIN_COUNT
        and digest(selected_keys) == EXPECTED_SELECTED_ORIGIN_KEYS_SHA256
        and sum(
            row["Round180_residual_child_count"] for row in selected
        ) == EXPECTED_SELECTED_CHILD_COUNT,
        "selected registry aggregate",
    )
    for class_name in SELECTED_CLASSES:
        require(
            len(class_keys[class_name])
            == EXPECTED_CLASS_ORIGIN_COUNT[class_name]
            and digest(class_keys[class_name])
            == EXPECTED_CLASS_ORIGIN_KEYS_SHA256[class_name]
            and sum(
                row["Round180_residual_child_count"]
                for row in selected
                if row["priority_class"] == class_name
            )
            == EXPECTED_CLASS_CHILD_COUNT[class_name],
            f"selected class aggregate:{class_name}",
        )
    pair_keys = sorted(
        row["origin_key"]
        for row in selected
        if tuple(row["Round180_residual_category_support"])
        == PAIR_SUPPORT
    )
    require(
        len(pair_keys) == EXPECTED_PAIR_ORIGIN_COUNT
        and digest(pair_keys) == EXPECTED_PAIR_ORIGIN_KEYS_SHA256
        and all(
            inputs["priority_by_origin"][key]["priority_class"]
            == DELTA_MULTI_CLASS
            for key in pair_keys
        )
        and sum(
            inputs["priority_by_origin"][key][
                "Round180_residual_child_count"
            ]
            for key in pair_keys
        ) == EXPECTED_PAIR_CHILD_COUNT,
        "clipped plus full-p pair cohort",
    )
    return {
        "inputs": inputs,
        "selected_rows": selected,
        "selected_keys": selected_keys,
        "class_keys": class_keys,
        "pair_keys": pair_keys,
    }


def outgoing_chart(row: Any, leaf: Any) -> str:
    if (
        leaf.classification != "unique_first"
        or leaf.owner_target != r176.FROZEN_OWNER
    ):
        return "NOT_APPLICABLE"
    chart, _margins = r176.outgoing_generic(row.chart_id, row.box)
    return chart if chart is not None else "OVERWRAP"


def candidate_evidence(row: Any, candidate: Any) -> dict[str, Any]:
    distance = r193.exact_distance_evidence(row, candidate)
    eligible = (
        distance["ell_negative"] and distance["distance_positive"]
    )
    failure = (
        "NONE__EXACT_BEHIND"
        if eligible
        else (
            "ELL_NOT_STRICT_NEGATIVE+DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
            if (
                not distance["ell_negative"]
                and not distance["distance_positive"]
            )
            else "ELL_NOT_STRICT_NEGATIVE"
            if not distance["ell_negative"]
            else "DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
        )
    )
    return {
        "target": candidate.target_id,
        "classification": candidate.classification,
        "ell_sign": distance["ell_sign"],
        "direct_distance_margin_sign": distance["direct_sign"],
        "identity_margin_sign": distance["identity_sign"],
        "direct_identity_interval_overlap":
            distance["interval_enclosures_overlap"],
        "eligible_exact_behind": eligible,
        "failure": failure,
    }


def analyze_cell(
    row: Any,
    category: str,
    priority_class: str,
) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    original_unresolved = sorted(
        (
            record
            for record in records
            if record.classification in UNRESOLVED_CLASSES
        ),
        key=lambda record: record.target_id,
    )
    evidence_by_target = {
        candidate.target_id: candidate_evidence(row, candidate)
        for candidate in original_unresolved
    }
    eligible_targets = sorted(
        target
        for target, evidence in evidence_by_target.items()
        if evidence["eligible_exact_behind"]
    )
    failed_candidate_reasons = Counter(
        evidence["failure"]
        for evidence in evidence_by_target.values()
        if not evidence["eligible_exact_behind"]
    )

    current_records = list(records)
    deletion_rounds: list[dict[str, Any]] = []
    for round_index, target in enumerate(eligible_targets, 1):
        require(
            any(
                record.target_id == target
                and record.classification in UNRESOLVED_CLASSES
                for record in current_records
            ),
            f"eligible candidate still present:{row.key}:{target}",
        )
        current_records = [
            record
            for record in current_records
            if record.target_id != target
        ]
        leaf = r176.classify_records(
            row.chart_id, row.box, current_records
        )
        disposition, _margins = r176.terminal_disposition(
            row.chart_id, leaf
        )
        deletion_rounds.append({
            "round": round_index,
            "deleted_target": target,
            "remaining_record_count": len(current_records),
            "remaining_leaf_classification": leaf.classification,
            "remaining_owner_target":
                leaf.owner_target if leaf.owner_target is not None else "NONE",
            "remaining_outgoing_chart": outgoing_chart(row, leaf),
            "remaining_disposition":
                disposition if disposition is not None else "UNRESOLVED",
        })

    final_leaf = r176.classify_records(
        row.chart_id, row.box, current_records
    )
    final_disposition, _margins = r176.terminal_disposition(
        row.chart_id, final_leaf
    )
    final_disposition_name = (
        final_disposition
        if final_disposition is not None
        else "UNRESOLVED"
    )
    final_excluded = (
        final_disposition is not None
        and final_disposition.startswith("EXCLUDED")
    )
    final_live = (
        final_disposition is not None
        and final_disposition.startswith("LIVE")
    )
    remaining_unresolved = [
        record
        for record in current_records
        if record.classification in UNRESOLVED_CLASSES
    ]
    closed_by_rule = bool(eligible_targets) and final_excluded
    q_holdout = (
        category == COMPACT_Q
        or row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR"
        or priority_class == COMPACT_CLASS
    )
    probe_admissible_closed = closed_by_rule and not q_holdout
    if q_holdout:
        residual_reason = Q_HOLDOUT_REASON
    elif not eligible_targets:
        residual_reason = NO_DELETION_REASON
    elif final_live:
        residual_reason = REDUCED_LIVE_REASON
    elif not final_excluded:
        residual_reason = REDUCED_UNRESOLVED_REASON
    else:
        residual_reason = "NONE__CLOSED"
    require(
        probe_admissible_closed
        == (residual_reason == "NONE__CLOSED"),
        f"cell outcome equivalence:{row.key}",
    )
    return {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "priority_class": priority_class,
        "original_failure_type": row.failure,
        "original_residual_category": category,
        "original_active_target_count": len(records),
        "original_unresolved_candidate_count":
            len(original_unresolved),
        "eligible_exact_behind_candidate_count":
            len(eligible_targets),
        "deleted_candidate_targets": eligible_targets,
        "failed_candidate_reason_count":
            map_counter(failed_candidate_reasons),
        "deletion_round_count": len(deletion_rounds),
        "deletion_rounds": deletion_rounds,
        "remaining_record_count": len(current_records),
        "remaining_unresolved_candidate_count":
            len(remaining_unresolved),
        "final_leaf_classification":
            final_leaf.classification,
        "final_owner_target":
            (
                final_leaf.owner_target
                if final_leaf.owner_target is not None
                else "NONE"
            ),
        "final_outgoing_chart": outgoing_chart(row, final_leaf),
        "final_disposition": final_disposition_name,
        "reduced_target_geometry_excluded": closed_by_rule,
        "compact_q_or_source_grazing_holdout": q_holdout,
        "probe_admissible_whole_cell_closed":
            probe_admissible_closed,
        "residual_reason": residual_reason,
    }


def rebuild_and_analyze(selection: dict[str, Any]) -> dict[str, Any]:
    selected_rows = selection["selected_rows"]
    selected_keys = set(selection["selected_keys"])
    pair_set = set(selection["pair_keys"])
    registry_by_origin = {
        row["origin_key"]: row for row in selected_rows
    }

    progress("replay Round180 frontier for frozen registry selection")
    replay = r176.replay_frontier()
    base_kinds: defaultdict[str, set[str]] = defaultdict(set)
    base_kinds.update({
        key: set(values)
        for key, values in replay["origin_kinds"].items()
        if key in selected_keys
    })
    base_closed_by_origin: Counter[str] = Counter()
    residual_roots: dict[str, list[Any]] = defaultdict(list)
    for row in replay["frontier"]:
        if row.origin_key not in selected_keys:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_roots[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key].add(kind)
            base_closed_by_origin[row.origin_key] += 1
    require(
        set(residual_roots) == selected_keys,
        "all selected origins have residual roots",
    )
    for rows in residual_roots.values():
        rows.sort(key=lambda row: row.key)

    input_cell_count: Counter[str] = Counter()
    input_volume: defaultdict[str, Q] = defaultdict(Q)
    category_count: Counter[str] = Counter()
    category_volume: defaultdict[str, Q] = defaultdict(Q)
    failure_type_count: Counter[str] = Counter()
    support_pattern_origins: Counter[str] = Counter()
    unresolved_cardinality: Counter[int] = Counter()
    eligible_cardinality: Counter[int] = Counter()
    deleted_cardinality: Counter[int] = Counter()
    remaining_unresolved_cardinality: Counter[int] = Counter()
    deletion_round_count: Counter[int] = Counter()
    deleted_target_count: Counter[str] = Counter()
    failed_candidate_reason_count: Counter[str] = Counter()
    final_leaf_count: Counter[str] = Counter()
    final_owner_count: Counter[str] = Counter()
    final_chart_count: Counter[str] = Counter()
    final_disposition_count: Counter[str] = Counter()
    reduced_geometric_closed_count: Counter[str] = Counter()
    reduced_geometric_closed_volume: defaultdict[str, Q] = defaultdict(Q)
    probe_closed_count: Counter[str] = Counter()
    probe_closed_volume: defaultdict[str, Q] = defaultdict(Q)
    residual_reason_count: Counter[str] = Counter()
    residual_reason_volume: defaultdict[str, Q] = defaultdict(Q)
    category_outcome: dict[str, Counter[str]] = defaultdict(Counter)
    class_residual_reason: dict[str, Counter[str]] = defaultdict(Counter)
    source_domain_count: Counter[str] = Counter()
    source_domain_by_class: dict[str, Counter[str]] = defaultdict(Counter)
    cell_digest = ListDigest()
    origin_rows: list[dict[str, Any]] = []
    closed_cell_keys: list[str] = []
    residual_cell_keys: list[str] = []

    geometrically_complete_origins: list[str] = []
    admissible_complete_origins: list[str] = []
    strict_interior_complete_origins: list[str] = []
    source_seam_geometric_holdouts: list[str] = []
    compact_origin_holdouts: list[str] = []
    residual_origins: list[str] = []
    pair_geometric_complete: list[str] = []
    pair_admissible_complete: list[str] = []

    total_selected = len(selected_rows)
    for index, registry in enumerate(selected_rows, 1):
        origin = registry["origin_key"]
        priority_class = registry["priority_class"]
        require(
            len(residual_roots[origin])
            == registry["Round176_residual_root_count"]
            and base_closed_by_origin[origin]
            == registry["Round176_preclosed_frontier_count"]
            and sorted(base_kinds[origin])
            == registry["Round176_preclosed_kinds"],
            f"Round176 registry reconstruction:{origin}",
        )
        refinement = r180.refine_origin(residual_roots[origin], 4)
        final_rows = refinement["final_residual_rows"]
        categories = Counter(
            r180.residual_category(row) for row in final_rows
        )
        initial_categories = Counter(
            r180.initial_category(row)
            for row in residual_roots[origin]
        )
        volume = sum(
            (box_volume(row.box) for row in final_rows), Q(0)
        )
        require(
            len(final_rows)
            == registry["Round180_residual_child_count"]
            and digest(sorted(row.key for row in final_rows))
            == registry["Round180_residual_child_keys_sha256"]
            and str(volume)
            == registry["Round180_residual_child_volume"]
            and map_counter(categories)
            == registry["Round180_residual_category_count"]
            and sorted(categories)
            == registry["Round180_residual_category_support"]
            and map_counter(initial_categories)
            == registry["initial_residual_category_count"],
            f"Round180 registry reconstruction:{origin}",
        )

        meta = replay["origins"][origin]
        source = r176.physical_domain(
            meta["chart_id"], meta["box"]
        )
        source_class = source["classification"]
        source_domain_count[source_class] += 1
        source_domain_by_class[priority_class][source_class] += 1
        support_pattern = "+".join(
            registry["Round180_residual_category_support"]
        )
        support_pattern_origins[support_pattern] += 1

        origin_geometric_closed = 0
        origin_probe_closed = 0
        origin_residual_reasons: Counter[str] = Counter()
        origin_deleted = 0
        origin_eligible = 0
        origin_input_volume = Q(0)
        origin_geometric_volume = Q(0)
        origin_probe_volume = Q(0)
        for row in final_rows:
            category = r180.residual_category(row)
            outcome = analyze_cell(
                row, category, priority_class
            )
            cell_digest.add(outcome)
            row_volume = box_volume(row.box)
            input_cell_count[priority_class] += 1
            input_volume[priority_class] += row_volume
            category_count[category] += 1
            category_volume[category] += row_volume
            failure_type_count[row.failure] += 1
            unresolved_cardinality[
                outcome["original_unresolved_candidate_count"]
            ] += 1
            eligible_cardinality[
                outcome["eligible_exact_behind_candidate_count"]
            ] += 1
            deleted_cardinality[
                len(outcome["deleted_candidate_targets"])
            ] += 1
            remaining_unresolved_cardinality[
                outcome["remaining_unresolved_candidate_count"]
            ] += 1
            deletion_round_count[
                outcome["deletion_round_count"]
            ] += 1
            deleted_target_count.update(
                outcome["deleted_candidate_targets"]
            )
            failed_candidate_reason_count.update(
                outcome["failed_candidate_reason_count"]
            )
            final_leaf_count[
                outcome["final_leaf_classification"]
            ] += 1
            final_owner_count[outcome["final_owner_target"]] += 1
            final_chart_count[outcome["final_outgoing_chart"]] += 1
            final_disposition_count[
                outcome["final_disposition"]
            ] += 1
            outcome_name = (
                "PROBE_CLOSED"
                if outcome["probe_admissible_whole_cell_closed"]
                else outcome["residual_reason"]
            )
            category_outcome[category][outcome_name] += 1
            origin_eligible += outcome[
                "eligible_exact_behind_candidate_count"
            ]
            origin_deleted += len(
                outcome["deleted_candidate_targets"]
            )
            origin_input_volume += row_volume
            if outcome["reduced_target_geometry_excluded"]:
                reduced_geometric_closed_count[priority_class] += 1
                reduced_geometric_closed_volume[priority_class] += row_volume
                origin_geometric_closed += 1
                origin_geometric_volume += row_volume
            if outcome["probe_admissible_whole_cell_closed"]:
                probe_closed_count[priority_class] += 1
                probe_closed_volume[priority_class] += row_volume
                origin_probe_closed += 1
                origin_probe_volume += row_volume
                closed_cell_keys.append(row.key)
            else:
                reason = outcome["residual_reason"]
                residual_reason_count[reason] += 1
                residual_reason_volume[reason] += row_volume
                class_residual_reason[priority_class][reason] += 1
                origin_residual_reasons[reason] += 1
                residual_cell_keys.append(row.key)

        require(
            origin_input_volume == volume
            and origin_geometric_volume <= origin_input_volume
            and origin_probe_volume <= origin_geometric_volume,
            f"origin exact-volume accounting:{origin}",
        )
        all_geometric = origin_geometric_closed == len(final_rows)
        all_probe = origin_probe_closed == len(final_rows)
        if all_geometric:
            geometrically_complete_origins.append(origin)
            if origin in pair_set:
                pair_geometric_complete.append(origin)
        if all_probe:
            admissible_complete_origins.append(origin)
            if origin in pair_set:
                pair_admissible_complete.append(origin)
        if (
            all_probe
            and priority_class != COMPACT_CLASS
            and source_class == r187.SOURCE_INTERIOR
        ):
            strict_interior_complete_origins.append(origin)
        elif all_geometric and source_class == r187.SOURCE_SEAM:
            source_seam_geometric_holdouts.append(origin)
        elif priority_class == COMPACT_CLASS:
            compact_origin_holdouts.append(origin)
        else:
            residual_origins.append(origin)

        origin_rows.append({
            "origin_key": origin,
            "priority_class": priority_class,
            "priority_ordinal": registry["priority_ordinal"],
            "source_domain_classification": source_class,
            "support_pattern": support_pattern,
            "input_cell_count": len(final_rows),
            "input_exact_volume": str(origin_input_volume),
            "eligible_exact_behind_candidate_count": origin_eligible,
            "deleted_candidate_count": origin_deleted,
            "reduced_geometry_closed_cell_count":
                origin_geometric_closed,
            "probe_admissible_closed_cell_count":
                origin_probe_closed,
            "probe_residual_reason_count":
                map_counter(origin_residual_reasons),
            "all_reduced_geometry_closed": all_geometric,
            "all_probe_cells_admissibly_closed": all_probe,
            "in_clipped_plus_full_p_210_cohort":
                origin in pair_set,
        })
        if index % 20 == 0 or index == total_selected:
            progress(
                f"generalized registry origins {index}/{total_selected}"
            )

    total_input_count = sum(input_cell_count.values())
    total_input_volume = sum(input_volume.values(), Q(0))
    total_probe_closed = sum(probe_closed_count.values())
    total_probe_closed_volume = sum(probe_closed_volume.values(), Q(0))
    total_residual = sum(residual_reason_count.values())
    total_residual_volume = sum(residual_reason_volume.values(), Q(0))
    require(
        total_input_count == EXPECTED_SELECTED_CHILD_COUNT
        and total_probe_closed + total_residual == total_input_count
        and total_probe_closed_volume + total_residual_volume
        == total_input_volume
        and cell_digest.count == total_input_count
        and len(origin_rows) == EXPECTED_SELECTED_ORIGIN_COUNT,
        "global selected count and volume conservation",
    )
    for class_name in SELECTED_CLASSES:
        require(
            input_cell_count[class_name]
            == EXPECTED_CLASS_CHILD_COUNT[class_name]
            and probe_closed_count[class_name]
            + sum(class_residual_reason[class_name].values())
            == input_cell_count[class_name],
            f"class count conservation:{class_name}",
        )

    key_lists = (
        geometrically_complete_origins,
        admissible_complete_origins,
        strict_interior_complete_origins,
        source_seam_geometric_holdouts,
        compact_origin_holdouts,
        residual_origins,
        pair_geometric_complete,
        pair_admissible_complete,
        closed_cell_keys,
        residual_cell_keys,
    )
    for values in key_lists:
        values.sort()
    origin_rows.sort(key=lambda row: row["priority_ordinal"])
    pair_input_cells = sum(
        registry_by_origin[key]["Round180_residual_child_count"]
        for key in pair_set
    )
    pair_input_volume = sum(
        (
            Q(registry_by_origin[key]["Round180_residual_child_volume"])
            for key in pair_set
        ),
        Q(0),
    )
    pair_closed_cells = sum(
        row["probe_admissible_closed_cell_count"]
        for row in origin_rows
        if row["in_clipped_plus_full_p_210_cohort"]
    )
    pair_residual_cells = pair_input_cells - pair_closed_cells
    pair_closed_volume = sum(
        (
            Q(row["input_exact_volume"])
            if row["all_probe_cells_admissibly_closed"]
            else Q(0)
            for row in origin_rows
            if row["in_clipped_plus_full_p_210_cohort"]
        ),
        Q(0),
    )
    # The whole-origin volume above is deliberately conservative; cell-level
    # volume is separately and exactly conserved globally.

    verdict = (
        "VALIDATED"
        if strict_interior_complete_origins
        else "PARTIAL"
        if total_probe_closed
        else "INVALIDATED"
    )
    return {
        "spike_verdict": verdict,
        "frozen_selection": {
            "selection_rule":
                "priority_class in {DELTA_H_OR_MULTI_NO_Q,"
                "COMPACT_Q_PRESENT}",
            "selection_uses_probe_outcome": False,
            "selected_origin_count": EXPECTED_SELECTED_ORIGIN_COUNT,
            "selected_origin_keys_sha256":
                EXPECTED_SELECTED_ORIGIN_KEYS_SHA256,
            "origin_count_by_priority_class":
                EXPECTED_CLASS_ORIGIN_COUNT,
            "origin_keys_sha256_by_priority_class":
                EXPECTED_CLASS_ORIGIN_KEYS_SHA256,
        },
        "input_reconstruction": {
            "cell_count_by_priority_class":
                map_counter(input_cell_count),
            "exact_volume_by_priority_class":
                fraction_map(input_volume),
            "total_cell_count": total_input_count,
            "total_exact_volume": str(total_input_volume),
            "residual_category_count":
                map_counter(category_count),
            "residual_category_exact_volume":
                fraction_map(category_volume),
            "original_failure_type_count":
                map_counter(failure_type_count),
            "support_pattern_origin_count":
                map_counter(support_pattern_origins),
            "source_domain_origin_count":
                map_counter(source_domain_count),
            "source_domain_origin_count_by_priority_class":
                nested_counter_map(source_domain_by_class),
            "all_registry_rows_reconstructed_exactly": True,
        },
        "iterative_exact_behind_reduction": {
            "original_unresolved_candidate_count_per_cell":
                map_counter(unresolved_cardinality),
            "eligible_exact_behind_candidate_count_per_cell":
                map_counter(eligible_cardinality),
            "deleted_candidate_count_per_cell":
                map_counter(deleted_cardinality),
            "remaining_unresolved_candidate_count_per_cell":
                map_counter(remaining_unresolved_cardinality),
            "deletion_round_count_per_cell":
                map_counter(deletion_round_count),
            "deleted_candidate_target_count":
                map_counter(deleted_target_count),
            "failed_candidate_reason_count":
                map_counter(failed_candidate_reason_count),
            "final_leaf_classification_count":
                map_counter(final_leaf_count),
            "final_owner_target_count":
                map_counter(final_owner_count),
            "final_outgoing_chart_count":
                map_counter(final_chart_count),
            "final_disposition_count":
                map_counter(final_disposition_count),
            "reduced_geometry_closed_cell_count_by_priority_class":
                map_counter(reduced_geometric_closed_count),
            "reduced_geometry_closed_exact_volume_by_priority_class":
                fraction_map(reduced_geometric_closed_volume),
            "probe_admissible_closed_cell_count_by_priority_class":
                map_counter(probe_closed_count),
            "probe_admissible_closed_exact_volume_by_priority_class":
                fraction_map(probe_closed_volume),
            "residual_reason_count":
                map_counter(residual_reason_count),
            "residual_reason_exact_volume":
                fraction_map(residual_reason_volume),
            "residual_reason_count_by_priority_class":
                nested_counter_map(class_residual_reason),
            "original_category_outcome_count":
                nested_counter_map(category_outcome),
            "total_probe_admissible_closed_cell_count":
                total_probe_closed,
            "total_probe_admissible_closed_exact_volume":
                str(total_probe_closed_volume),
            "total_residual_cell_count": total_residual,
            "total_residual_exact_volume":
                str(total_residual_volume),
            "closed_cell_keys_sha256":
                digest(closed_cell_keys),
            "residual_cell_keys_sha256":
                digest(residual_cell_keys),
            "per_cell_reduction_evidence_rows_sha256":
                cell_digest.finish(),
            "exact_count_and_volume_conservation": True,
        },
        "origin_outcome": {
            "geometrically_complete_origin_count":
                len(geometrically_complete_origins),
            "geometrically_complete_origin_keys":
                geometrically_complete_origins,
            "geometrically_complete_origin_keys_sha256":
                digest(geometrically_complete_origins),
            "all_probe_cells_admissibly_closed_origin_count":
                len(admissible_complete_origins),
            "all_probe_cells_admissibly_closed_origin_keys":
                admissible_complete_origins,
            "strict_physical_interior_noncompact_complete_origin_count":
                len(strict_interior_complete_origins),
            "strict_physical_interior_noncompact_complete_origin_keys":
                strict_interior_complete_origins,
            "strict_physical_interior_noncompact_complete_keys_sha256":
                digest(strict_interior_complete_origins),
            "source_seam_geometrically_complete_but_held_out_count":
                len(source_seam_geometric_holdouts),
            "source_seam_geometrically_complete_but_held_out_keys":
                source_seam_geometric_holdouts,
            "compact_q_origin_holdout_count":
                len(compact_origin_holdouts),
            "compact_q_origin_holdout_keys":
                compact_origin_holdouts,
            "other_residual_origin_count": len(residual_origins),
            "other_residual_origin_keys": residual_origins,
            "per_origin_rows_sha256": digest(origin_rows),
            "official_integer_credit": 0,
        },
        "clipped_plus_full_p_210_cohort": {
            "selection_rule":
                "frozen Round180 residual category support exactly "
                "{CLIPPED,FULL_P}",
            "selection_uses_probe_outcome": False,
            "origin_count": EXPECTED_PAIR_ORIGIN_COUNT,
            "origin_keys": sorted(pair_set),
            "origin_keys_sha256":
                EXPECTED_PAIR_ORIGIN_KEYS_SHA256,
            "input_cell_count": pair_input_cells,
            "input_exact_volume": str(pair_input_volume),
            "probe_closed_cell_count": pair_closed_cells,
            "probe_residual_cell_count": pair_residual_cells,
            "geometrically_complete_origin_count":
                len(pair_geometric_complete),
            "geometrically_complete_origin_keys":
                pair_geometric_complete,
            "admissibly_complete_origin_count":
                len(pair_admissible_complete),
            "admissibly_complete_origin_keys":
                pair_admissible_complete,
            "conservative_whole_complete_origin_volume":
                str(pair_closed_volume),
            "official_integer_credit": 0,
        },
        "stratum_nonpromotion": {
            "compact_q_rows_promoted_by_candidate_deletion": 0,
            "compact_q_origins_promoted_by_candidate_deletion": 0,
            "source_grazing_requires_independent_source_stratum": True,
            "physical_source_seam_requires_half_open_partition": True,
            "source_seam_integer_credit": 0,
            "compact_q_integer_credit": 0,
        },
    }


def build_probe() -> dict[str, Any]:
    selection = check_chain_and_select()
    analysis = rebuild_and_analyze(selection)
    result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_GENERALIZED_EXACT_BEHIND_REDUCTION",
        "spike_verdict": analysis["spike_verdict"],
        "question":
            "How much of the frozen 596 mixed plus 54 compact-q origin "
            "registry closes under iterative exact-behind candidate removal?",
        "parameters": {
            "arb_precision_bits": 192,
            "hash_seed_external": "197052",
            "Round180_extra_depth_reconstructed": 4,
            "candidate_deletion_order": "lexicographic target id",
            "delete_one_candidate_then_reclassify": True,
        },
        "input_chain": {
            "Round194_source_sha256": ROUND194_SHA256,
            "Round184_registry_rows_sha256":
                ROUND184_REGISTRY_ROWS_SHA256,
            "imported_rounds_used_only_as_probe_libraries": True,
        },
        "analysis": analysis,
        "mathematical_contract": {
            "candidate_rule":
                "Delta<0 gives no real root; Delta>=0 with ell<0 and "
                "distance^2-R^2=ell^2-Delta>0 gives far<0",
            "iteration_rule":
                "delete one eligible unresolved candidate, then rebuild "
                "remaining leaf, owner, chart, and disposition",
            "registry_selection_outcome_blind": True,
            "compact_q_and_source_grazing_independent": True,
            "source_seam_independent": True,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "filesystem_writes": 0,
            "official_ledger_mutated": False,
            "probe_counts_applied_to_official_ledger": False,
            "whole_origin_integer_credit_issued": 0,
            "D02": "UNCHANGED_BLOCKED",
            "D03_negative_oracle": "UNCHANGED_UNAUTHORIZED",
            "Gate5": "UNCHANGED_10_OF_18",
            "complete_18_field_blocks": 0,
            "CM2": "UNCHANGED_NO_GO",
            "required_before_any_ledger_use":
                "formal producer with full stratum ledgers plus independent "
                "non-importing verifier",
        },
    }
    return {
        "schema": SCHEMA,
        "probe_result": result,
        "probe_result_sha256": digest(result),
    }


def main() -> int:
    ctx.prec = 192
    document = build_probe()
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
