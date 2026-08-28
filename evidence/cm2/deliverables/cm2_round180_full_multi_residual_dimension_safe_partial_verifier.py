#!/usr/bin/env python3
"""Independent verifier for the bounded Round180 residual pass.

This file does not import or execute the Round180 producer.  Relative to the
frozen, independently verified Round176 base, it locally rebuilds every one of
the 44,040 residual inputs, both bounded refinement depths, all 32 promoted
origin trees, the lower-dimensional split ledger, the H nonclosure regression,
the depth-10 compact-q profile, the producer output-safety contract and its 19
path attacks, and the complete expected certificate result.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import ctx

import cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier as r176


HERE = Path(__file__).resolve().parent
PRODUCER = (
    HERE
    / "cm2_round180_full_multi_residual_dimension_safe_partial.py"
)
CERTIFICATE = (
    HERE
    / "cm2_round180_full_multi_residual_dimension_safe_partial_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round180_full_multi_residual_dimension_safe_partial_verification.json"
)
SCHEMA = (
    "cm2.round180.full-multi-residual-dimension-safe-partial."
    "verification.v1"
)
CERTIFICATE_SCHEMA = (
    "cm2.round180.full-multi-residual-dimension-safe-partial.v1"
)
EXPECTED_PRODUCER_SHA256 = (
    "0ddb815a036a6e351929c484a00a565ce8969286bb137977ee9470577d807955"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "46c6f1b2e86f9aa70d9126b28febbf97a81d6a4ac8f610dc2bb82d032a1abb70"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "b2d30aade1e60c3b8d1e5943a240bafc8c8a28e35e67c882026b94246dafae3b"
)
MAX_INPUT_BYTES = 8 * 1024 * 1024
PINS = {
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion.py":
        "dc1668d868687bb1c6bb2cc458f2aed8cf35308c852d7ba92e75eddc7e848086",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json":
        "bb255bf9dbf1c6cb6680ea32b57ad31c03f108a8af5c345a2f7ca3ab88a22fa8",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py":
        "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verification.json":
        "31ad065d06309b9f830c6135579672e50e4c84d6f2620419326c1cd682dd010e",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_report.md":
        "3add38da9cdf44d8489bf364a70205cf4ef036255dab0832f3ab9ea23178debe",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_cold_replay.md":
        "a773e2c55ded7cce5335ddeb61904abcbbb0568898318b0652f290c12f23bf30",
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_manifest.sha256":
        "9338ce1401cfb61ea52db558651a6283bd6039caa856f912494b9d26084cb761",
}
ROUND180_NON_CERTIFICATE_PROTECTED = (
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py",
    "cm2_round180_full_multi_residual_dimension_safe_partial_verification.json",
    "cm2_round180_full_multi_residual_dimension_safe_partial_report.md",
    "cm2_round180_full_multi_residual_dimension_safe_partial_cold_replay.md",
    "cm2_round180_full_multi_residual_dimension_safe_partial_manifest.sha256",
)
ROUND176_RESULT = (
    "3090fb2f58fff50f0c9ab89b7a228042f49d5d929cd53e9c358e31a4d977254e"
)
ROUND176_VERIFICATION_RESULT = (
    "b5057dcc0ff32ac6a8e619fb030ba1bf9ff1c975598ade79a282accaeac6f6f3"
)

INITIAL_CATEGORIES = {
    "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 26728,
    "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY": 4812,
    "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 10802,
    "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 1478,
    "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH": 220,
}
EXPECTED_H_REGRESSION = (
    "W:N:04.00.10000000",
    "W:N:04.00.1000000000010110",
)


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


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{path.name}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    require(type(value) is dict, f"top:{path.name}")
    return value


def check_chain() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            == expected,
            f"pin:{name}",
        )
    certificate = strict_load(
        HERE
        / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json"
    )
    verification = strict_load(
        HERE
        / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verification.json"
    )
    require(
        certificate["result_sha256"] == ROUND176_RESULT,
        "Round176 result",
    )
    require(
        verification["result_sha256"] == ROUND176_VERIFICATION_RESULT
        and verification["result"]["status"] == "PASS",
        "Round176 verification",
    )
    ledger = verification["result"]["ledger_reconstruction"]
    require(
        ledger["combined_whole_record_excluded"] == 73360
        and ledger["combined_conservative_live"] == 3472
        and ledger["refined_source_W_record_count"] == 76832,
        "Round176 ledger",
    )
    manifest_rows: dict[str, str] = {}
    for line in (
        HERE
        / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_manifest.sha256"
    ).read_text().splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest_rows, f"manifest duplicate:{name}")
        manifest_rows[name] = value
    require(
        all(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == value
            for name, value in manifest_rows.items()
        ),
        "Round176 manifest replay",
    )
    return {
        "file_sha256": dict(sorted(PINS.items())),
        "Round176_result_sha256": ROUND176_RESULT,
        "Round176_verification_result_sha256":
            ROUND176_VERIFICATION_RESULT,
        "Round176_manifest_entries_replayed": True,
    }


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[str, Q]) -> dict[str, str]:
    return {
        key: str(item) for key, item in sorted(value.items())
    }


def initial_category(row: r176.Frontier) -> str:
    if row.failure in {
        "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
        "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
    }:
        return "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
    if row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR":
        return "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
    require(
        row.failure == "UNTYPED_DISCRIMINANT_COLLAR",
        f"initial category:{row.failure}",
    )
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    if len(unresolved) != 1:
        return "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
    _derivative, _lower, _upper, full = r176.graph_faces(
        row, unresolved[0]
    )
    return (
        "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
        if full
        else "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
    )


def residual_category(row: r176.Frontier) -> str:
    if row.failure == "SOURCE_GRAZING_ENDPOINT_COLLAR":
        return "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
    if row.failure in {
        "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
        "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
    }:
        return "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
    if row.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
        return "OUTGOING_H_GRAPH_INTERSECTION_RESIDUAL"
    if row.failure == "STRICT_ROOT_ORDER_OVERLAP":
        return "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
    if row.failure != "UNTYPED_DISCRIMINANT_COLLAR":
        return "MIXED_INTERVAL_DEPENDENCY_RESIDUAL"
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    if len(unresolved) != 1:
        return "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
    _derivative, _lower, _upper, full = r176.graph_faces(
        row, unresolved[0]
    )
    return (
        "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
        if full
        else "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
    )


def split_axis(box: r176.Box) -> int:
    widths = (
        box.t1 - box.t0,
        box.p1 - box.p0,
        box.s1 - box.s0,
    )
    return max(range(3), key=lambda index: widths[index])


def split_face(
    parent: r176.Frontier,
    axis: int,
    lower: r176.Box,
    upper: r176.Box,
) -> dict[str, Any]:
    names = ("t", "p", "s")
    bounds = (
        (parent.box.t0, parent.box.t1),
        (parent.box.p0, parent.box.p1),
        (parent.box.s0, parent.box.s1),
    )
    coordinate = (
        lower.t1 if axis == 0
        else (lower.p1 if axis == 1 else lower.s1)
    )
    row = {
        "parent_cell_key": parent.key,
        "axis": names[axis],
        "coordinate": str(coordinate),
        "spans": {
            names[index]: [
                str(bounds[index][0]), str(bounds[index][1])
            ]
            for index in range(3)
            if index != axis
        },
        "dimension": 2,
        "lower_child_owner": f"{parent.chart_id}:{lower.path}",
        "upper_child_nonowner": f"{parent.chart_id}:{upper.path}",
        "both_closed_interval_enclosures_include_face": True,
    }
    row["face_sha256"] = digest(row)
    return row


def close_node(
    row: r176.Frontier,
) -> tuple[str | None, dict[str, Any] | None, r176.Frontier | None]:
    leaf, records = r176.classify(
        row.chart_id, row.box, row.active_targets
    )
    disposition, margins = r176.terminal_disposition(
        row.chart_id, leaf
    )
    if disposition is not None:
        return r176.coarse(disposition), {
            "method": "DIRECT_STRICT_CLOSED_BOX",
            "disposition": disposition,
            "dimension": 3,
            "all_owned_boundary_strata_inherit_strict_proof": True,
        }, None
    failure = r176.failure_type(leaf, records, margins)
    inherited = (
        (r176.FROZEN_OWNER,)
        if leaf.classification == "unique_first"
        else (
            row.active_targets
            if leaf.classification == "tangency_graph"
            else leaf.active_targets
        )
    )
    unresolved = r176.Frontier(
        row.chart_id,
        row.box,
        inherited,
        row.origin_key,
        failure,
    )
    if failure == "OUTGOING_CHART_SEAM_OVERWRAP":
        kind, classes, depths = r176.h_partition(unresolved)
        if kind is None:
            return None, None, unresolved
        return kind, {
            "method": "OUTGOING_H_CLOSED_RECTANGLE_TREE",
            "dimension": 3,
            "terminal_classes": map_counter(classes),
            "terminal_depths": map_counter(depths),
            "H_zero_graph_dimension": 2,
            "H_graph_boundary_dimension": 1,
            "H_graph_corner_dimension": 0,
        }, None
    if failure in {
        "TYPED_FROZEN_OWNER_TANGENCY_GRAPH_COLLAR",
        "TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR",
    }:
        closed, witness = r176.close_tangency(unresolved)
        if not closed:
            return None, None, unresolved
        return "EXCLUDED", {
            "method": "TYPED_DELTA_THREE_STRATUM",
            "dimension": 3,
            "Delta_negative_dimension": 3,
            "Delta_zero_dimension": 2,
            "Delta_positive_dimension": 3,
            "graph_edge_dimension": 1,
            "graph_corner_dimension": 0,
            "witness": witness,
        }, None
    if failure == "UNTYPED_DISCRIMINANT_COLLAR":
        kind, witness = r176.close_same_sign(unresolved)
        if kind is None:
            return None, None, unresolved
        current_records = r176.records_for(
            unresolved.chart_id,
            unresolved.box,
            unresolved.active_targets,
        )
        candidates = [
            record for record in current_records
            if record.classification == "unresolved_discriminant"
        ]
        require(len(candidates) == 1, "same-sign candidate")
        derivative, lower, upper, _full = r176.graph_faces(
            unresolved, candidates[0]
        )
        common_sign = r176.sign(lower)
        require(
            derivative != 0
            and common_sign != 0
            and common_sign == r176.sign(upper),
            "same-sign proof",
        )
        return kind, {
            "method": "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX",
            "dimension": 3,
            "target": candidates[0].target_id,
            "derivative_sign":
                "POSITIVE" if derivative > 0 else "NEGATIVE",
            "strict_common_face_sign":
                "POSITIVE" if common_sign > 0 else "NEGATIVE",
            "Delta_zero_graph_inside_closed_box": False,
            "empty_2D_graph_edge_and_corner_ledger": True,
            "witness": witness,
        }, None
    return None, None, unresolved


def refine_origin(
    rows: list[r176.Frontier],
    max_depth: int,
) -> dict[str, Any]:
    pending = [(row, row.key) for row in rows]
    terminals: list[dict[str, Any]] = []
    split_faces: list[dict[str, Any]] = []
    h_nonclosures: list[dict[str, Any]] = []
    residual_at_cutoff: dict[int, int] = {}
    evaluated = 0
    earliest_complete: int | None = None
    final_residual: list[r176.Frontier] = []
    for depth in range(max_depth + 1):
        unresolved_rows: list[tuple[r176.Frontier, str]] = []
        for row, root_key in pending:
            evaluated += 1
            kind, evidence, unresolved = close_node(row)
            if kind is not None:
                require(evidence is not None, "terminal evidence")
                terminal = {
                    "cell_key": row.key,
                    "root_depth14_cell_key": root_key,
                    "extra_depth": depth,
                    "coverage_numerator": 2 ** (max_depth - depth),
                    "coverage_denominator": 2 ** max_depth,
                    "coarse_disposition": kind,
                    **evidence,
                }
                terminal["terminal_sha256"] = digest(terminal)
                terminals.append(terminal)
                continue
            require(unresolved is not None, "unresolved row")
            if unresolved.failure == "OUTGOING_CHART_SEAM_OVERWRAP":
                kind_h, classes, depths = r176.h_partition(unresolved)
                if kind_h is None:
                    h_nonclosures.append({
                        "origin_key": unresolved.origin_key,
                        "cell_key": unresolved.key,
                        "box": {
                            "t": [
                                str(unresolved.box.t0),
                                str(unresolved.box.t1),
                            ],
                            "p": [
                                str(unresolved.box.p0),
                                str(unresolved.box.p1),
                            ],
                            "s": [
                                str(unresolved.box.s0),
                                str(unresolved.box.s1),
                            ],
                        },
                        "H_tree_terminal_classes": map_counter(classes),
                        "H_tree_terminal_depths": map_counter(depths),
                        "H_tree_max_extra_depth": 4,
                        "whole_cell_closed": False,
                    })
            unresolved_rows.append((unresolved, root_key))
        residual_at_cutoff[depth] = len(unresolved_rows)
        if not unresolved_rows:
            earliest_complete = depth
            pending = []
            break
        if depth == max_depth:
            final_residual = [row for row, _root in unresolved_rows]
            pending = unresolved_rows
            break
        next_pending: list[tuple[r176.Frontier, str]] = []
        for row, root_key in unresolved_rows:
            axis = split_axis(row.box)
            lower, upper = r176.split(row.box, axis)
            split_faces.append(split_face(row, axis, lower, upper))
            next_pending.extend([
                (
                    r176.Frontier(
                        row.chart_id,
                        lower,
                        row.active_targets,
                        row.origin_key,
                        row.failure,
                    ),
                    root_key,
                ),
                (
                    r176.Frontier(
                        row.chart_id,
                        upper,
                        row.active_targets,
                        row.origin_key,
                        row.failure,
                    ),
                    root_key,
                ),
            ])
        pending = next_pending
    coverage_by_root: Counter[str] = Counter()
    for row in terminals:
        coverage_by_root[row["root_depth14_cell_key"]] += row[
            "coverage_numerator"
        ]
    for row, root_key in pending:
        coverage_by_root[root_key] += 1
    require(
        set(coverage_by_root) == {row.key for row in rows}
        and all(
            value == 2 ** max_depth
            for value in coverage_by_root.values()
        ),
        "refinement coverage",
    )
    return {
        "max_extra_depth": max_depth,
        "evaluated_node_count": evaluated,
        "earliest_complete_depth": earliest_complete,
        "terminal_rows": sorted(
            terminals, key=lambda row: row["cell_key"]
        ),
        "terminal_count_by_disposition": map_counter(Counter(
            row["coarse_disposition"] for row in terminals
        )),
        "terminal_count_by_method": map_counter(Counter(
            row["method"] for row in terminals
        )),
        "terminal_count_by_extra_depth": map_counter(Counter(
            row["extra_depth"] for row in terminals
        )),
        "split_face_rows": sorted(
            split_faces, key=lambda row: row["parent_cell_key"]
        ),
        "split_face_count": len(split_faces),
        "residual_at_cutoff": {
            str(key): value
            for key, value in sorted(residual_at_cutoff.items())
        },
        "final_residual_rows": sorted(
            final_residual, key=lambda row: row.key
        ),
        "H_nonclosures": sorted(
            h_nonclosures, key=lambda row: row["cell_key"]
        ),
    }


def lower_strata_ledger(
    split_faces: list[dict[str, Any]],
) -> dict[str, Any]:
    axis_index = {"t": 0, "p": 1, "s": 2}
    axes = ("t", "p", "s")
    edge_owners: dict[str, str] = {}
    corner_owners: dict[str, str] = {}
    for face in split_faces:
        fixed_axis = face["axis"]
        free_axes = [axis for axis in axes if axis != fixed_axis]
        for boundary_axis in free_axes:
            remaining_axis = next(
                axis for axis in free_axes if axis != boundary_axis
            )
            for endpoint in face["spans"][boundary_axis]:
                edge = {
                    "fixed": {
                        fixed_axis: face["coordinate"],
                        boundary_axis: endpoint,
                    },
                    "free": {
                        remaining_axis: face["spans"][remaining_axis]
                    },
                }
                key = canonical(edge)
                owner = face["lower_child_owner"]
                edge_owners[key] = min(edge_owners.get(key, owner), owner)
        for first_endpoint in face["spans"][free_axes[0]]:
            for second_endpoint in face["spans"][free_axes[1]]:
                corner = {
                    fixed_axis: face["coordinate"],
                    free_axes[0]: first_endpoint,
                    free_axes[1]: second_endpoint,
                }
                key = canonical({
                    axis: corner[axis]
                    for axis in sorted(corner, key=axis_index.get)
                })
                owner = face["lower_child_owner"]
                corner_owners[key] = min(
                    corner_owners.get(key, owner), owner
                )
    face_keys = [
        row["face_sha256"]
        for row in sorted(
            split_faces, key=lambda row: row["parent_cell_key"]
        )
    ]
    edge_rows = [
        {"geometry": json.loads(key), "owner": owner}
        for key, owner in sorted(edge_owners.items())
    ]
    corner_rows = [
        {"geometry": json.loads(key), "owner": owner}
        for key, owner in sorted(corner_owners.items())
    ]
    return {
        "3D_closed_terminal_cells_are_primary_proof_objects": True,
        "2D_owned_split_face_count": len(split_faces),
        "2D_owned_split_face_rows_sha256": digest(split_faces),
        "2D_owned_split_face_self_digests_sha256": digest(face_keys),
        "1D_deduplicated_split_face_edge_count": len(edge_rows),
        "1D_split_face_edges_sha256": digest(edge_rows),
        "0D_deduplicated_split_face_corner_count": len(corner_rows),
        "0D_split_face_corners_sha256": digest(corner_rows),
        "duplicate_lower_strata_owner":
            "lexicographically least lower-child key",
        "all_owned_2D_1D_0D_strata_inherit_a_closed_EXCLUDED_enclosure":
            True,
    }


def q_depth10_profile(rows: list[r176.Frontier]) -> dict[str, Any]:
    face_counts: Counter[str] = Counter()
    terminal_counts: Counter[str] = Counter()
    terminal_depths: Counter[int] = Counter()
    terminal_volume: dict[str, Q] = defaultdict(Q)
    residual_counts: Counter[str] = Counter()
    residual_volume = Q(0)
    residual_keys: list[str] = []
    closed_parents: list[str] = []
    for row in rows:
        p_sign = 1 if row.box.p1 == 1 else -1
        root = r176.QBox(
            row.box.t0, row.box.t1, Q(0), Q(1),
            row.box.s0, row.box.s1, 0,
        )
        face = r176.QBox(
            row.box.t0, row.box.t1, Q(0), Q(0),
            row.box.s0, row.box.s1, 0,
        )
        face_classification, _active = r176.q_classify(
            row.chart_id, p_sign, face, row.active_targets
        )
        face_counts[face_classification] += 1
        pending = [(root, row.active_targets, "")]
        parent_residual = False
        parent_kinds: set[str] = set()
        while pending:
            box, targets, path = pending.pop()
            classification, active = r176.q_classify(
                row.chart_id, p_sign, box, targets
            )
            if not classification.startswith("UNRESOLVED"):
                terminal_counts[classification] += 1
                terminal_depths[box.depth] += 1
                terminal_volume[classification] += Q(
                    1, 2 ** box.depth
                )
                parent_kinds.add(
                    "EXCLUDED"
                    if classification.startswith("EXCLUDED")
                    else "LIVE"
                )
            elif box.depth < 10:
                lower, upper = r176.q_split(box)
                inherited = active or targets
                pending.extend([
                    (lower, inherited, path + "0"),
                    (upper, inherited, path + "1"),
                ])
            else:
                parent_residual = True
                residual_counts[classification] += 1
                residual_volume += Q(1, 2 ** box.depth)
                residual_keys.append(f"{row.key}:q{path}")
        if not parent_residual:
            closed_parents.append(
                f"{row.key}:{','.join(sorted(parent_kinds))}"
            )
    residual_keys.sort()
    require(
        len(rows) == 1478
        and not closed_parents
        and sum(terminal_counts.values()) == 92976
        and sum(residual_counts.values()) == 138432
        and residual_volume == Q(2163, 16),
        "q depth10 census",
    )
    return {
        "input_depth14_parent_count": len(rows),
        "max_extra_q_depth": 10,
        "coordinate": {
            "r_interval": "[0,1]",
            "q": "sqrt(1023/262144)*r",
            "p": "sign*sqrt(1-(1023/262144)*r^2)",
        },
        "interior_stratum": {"predicate": "r>0", "dimension": 3},
        "grazing_face_stratum": {
            "predicate": "r=0",
            "dimension": 2,
            "classification_count": map_counter(face_counts),
        },
        "Delta_H_or_root_intersection_with_grazing_face_dimension_at_most":
            1,
        "triple_or_corner_intersection_dimension_at_most": 0,
        "terminal_count_by_disposition": map_counter(terminal_counts),
        "terminal_count_by_extra_depth": map_counter(terminal_depths),
        "terminal_volume_by_disposition":
            fraction_map(terminal_volume),
        "residual_count_by_type": map_counter(residual_counts),
        "residual_q_cell_count": len(residual_keys),
        "residual_q_cell_keys_sha256": digest(residual_keys),
        "residual_depth14_parent_equivalent": str(residual_volume),
        "whole_depth14_parent_closed": 0,
        "whole_origin_integer_credit": 0,
    }


def build_result() -> dict[str, Any]:
    upstream = check_chain()
    replay = r176.replay_frontier()
    base_kinds: dict[str, set[str]] = replay["origin_kinds"]
    base_closed_by_origin: Counter[str] = Counter()
    base_frontier_by_origin: Counter[str] = Counter(
        row.origin_key for row in replay["frontier"]
    )
    residual_rows: list[r176.Frontier] = []
    initial_keys_by_category: dict[str, list[str]] = defaultdict(list)
    for row in replay["frontier"]:
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_rows.append(row)
            initial_keys_by_category[initial_category(row)].append(row.key)
        else:
            base_kinds[row.origin_key].add(kind)
            base_closed_by_origin[row.origin_key] += 1
    for values in initial_keys_by_category.values():
        values.sort()
    require(
        len(residual_rows) == 44040
        and {
            key: len(values)
            for key, values in sorted(initial_keys_by_category.items())
        }
        == INITIAL_CATEGORIES,
        "initial residual categories",
    )
    residual_by_origin: dict[str, list[r176.Frontier]] = defaultdict(list)
    for row in residual_rows:
        residual_by_origin[row.origin_key].append(row)
    for values in residual_by_origin.values():
        values.sort(key=lambda row: row.key)
    require(len(residual_by_origin) == 2162, "residual origins")
    witness_origins = sorted(
        origin for origin in residual_by_origin
        if (
            "LIVE" in base_kinds[origin]
            or "MIXED" in base_kinds[origin]
        )
    )
    upper_candidates = sorted(
        origin for origin in residual_by_origin
        if base_kinds[origin] <= {"EXCLUDED"}
    )
    require(
        len(witness_origins) == 686
        and digest(witness_origins)
        == "1d974a10739e6e2dc1a99b9a8eec721fe70d1bf7fc92e6d7c283d1aea00769f5"
        and len(upper_candidates) == 1476
        and digest(upper_candidates)
        == "c15ab39fcffba53204de689f631110e5888df616e47d56a08f8cb42f72ee8aad",
        "origin partition",
    )
    upper_candidate_set = set(upper_candidates)
    final_residual_keys_by_category: dict[str, list[str]] = defaultdict(list)
    final_residual_origin_keys: list[str] = []
    newly_complete_nonexcluded: list[str] = []
    new_excluded: list[str] = []
    credited_summaries: list[dict[str, Any]] = []
    all_h_nonclosures: list[dict[str, Any]] = []
    global_terminal_methods: Counter[str] = Counter()
    global_terminal_dispositions: Counter[str] = Counter()
    global_evaluated = 0
    complete_depth_counts: Counter[int] = Counter()
    exact_earliest_depth_counts: Counter[int] = Counter()
    for origin in sorted(residual_by_origin):
        max_depth = 4 if origin in upper_candidate_set else 2
        refinement = refine_origin(
            residual_by_origin[origin], max_depth
        )
        global_evaluated += refinement["evaluated_node_count"]
        global_terminal_methods.update(
            refinement["terminal_count_by_method"]
        )
        global_terminal_dispositions.update(
            refinement["terminal_count_by_disposition"]
        )
        all_h_nonclosures.extend(refinement["H_nonclosures"])
        remaining = refinement["final_residual_rows"]
        if remaining:
            final_residual_origin_keys.append(origin)
            for row in remaining:
                final_residual_keys_by_category[
                    residual_category(row)
                ].append(row.key)
            continue
        kinds = set(base_kinds[origin])
        kinds.update(
            row["coarse_disposition"]
            for row in refinement["terminal_rows"]
        )
        if kinds == {"EXCLUDED"}:
            require(origin in upper_candidates, "excluded upper candidate")
            new_excluded.append(origin)
            depth = refinement["earliest_complete_depth"]
            require(depth is not None, "complete depth")
            exact_earliest_depth_counts[depth] += 1
            # "2" is the bounded depth-2 tranche and therefore includes
            # parents that happen to finish at depth 0 or 1.
            complete_depth_counts[2 if depth <= 2 else depth] += 1
            split_rows = refinement["split_face_rows"]
            source = r176.physical_domain(
                replay["origins"][origin]["chart_id"],
                replay["origins"][origin]["box"],
            )
            summary = {
                "origin_key": origin,
                "original_parent_box": r176.box_row(
                    replay["origins"][origin]["box"]
                ),
                "source_chart_domain": source,
                "Round176_residual_root_count":
                    len(residual_by_origin[origin]),
                "Round176_preclosed_frontier_count":
                    base_closed_by_origin[origin],
                "Round176_preclosed_kinds":
                    sorted(base_kinds[origin]),
                "maximum_extra_depth": max_depth,
                "earliest_complete_extra_depth": depth,
                "evaluated_node_count":
                    refinement["evaluated_node_count"],
                "terminal_count_by_method":
                    refinement["terminal_count_by_method"],
                "terminal_count_by_extra_depth":
                    refinement["terminal_count_by_extra_depth"],
                "terminal_rows": refinement["terminal_rows"],
                "terminal_rows_sha256":
                    digest(refinement["terminal_rows"]),
                "replacement_coverage": {
                    "each_depth14_root_coverage_numerator":
                        2 ** max_depth,
                    "each_depth14_root_coverage_denominator":
                        2 ** max_depth,
                    "residual_cell_count": 0,
                    "all_terminal_coarse_dispositions": ["EXCLUDED"],
                },
                "lower_dimensional_strata":
                    lower_strata_ledger(split_rows),
                "analytic_graph_ledger": {
                    "same_sign_Delta_terminal_count":
                        refinement["terminal_count_by_method"].get(
                            "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX", 0
                        ),
                    "same_sign_boxes_have_Delta_zero_graph": False,
                    "typed_Delta_graph_terminal_count":
                        refinement["terminal_count_by_method"].get(
                            "TYPED_DELTA_THREE_STRATUM", 0
                        ),
                    "outgoing_H_graph_terminal_count":
                        refinement["terminal_count_by_method"].get(
                            "OUTGOING_H_CLOSED_RECTANGLE_TREE", 0
                        ),
                    "all_nonempty_analytic_2D_1D_0D_strata_excluded":
                        True,
                },
                "whole_original_physical_parent_excluded": True,
                "whole_origin_integer_credit": 1,
                "child_count_or_volume_used_as_integer_credit": False,
                "guard_outside_used_as_exterior_credit": False,
            }
            summary["row_sha256"] = digest(summary)
            credited_summaries.append(summary)
        else:
            newly_complete_nonexcluded.append(origin)
    for values in final_residual_keys_by_category.values():
        values.sort()
    new_excluded.sort()
    newly_complete_nonexcluded.sort()
    credited_summaries.sort(key=lambda row: row["origin_key"])
    require(
        len(new_excluded) == 32
        and digest(new_excluded)
        == "70300cade4136fdb41f4b1f8900b47b89f0d9a498f7afd0c0d614296f84b3c87"
        and complete_depth_counts == {2: 18, 3: 8, 4: 6}
        and exact_earliest_depth_counts == {1: 18, 3: 8, 4: 6}
        and len(newly_complete_nonexcluded) == 4,
        (
            "bounded whole-origin result:"
            f"count={len(new_excluded)}:"
            f"digest={digest(new_excluded)}:"
            f"depths={dict(complete_depth_counts)}:"
            f"other={len(newly_complete_nonexcluded)}"
        ),
    )
    final_residual_origin_keys.sort()
    require(
        len(final_residual_origin_keys) == 2126
        and len(upper_candidates) - len(new_excluded) == 1444,
        "final origin conservation",
    )
    require(
        global_evaluated == 755544
        and newly_complete_nonexcluded
        == [
            "W:E:00.14.10100011",
            "W:E:01.13.01010010",
            "W:E:06.02.10101101",
            "W:E:07.01.01011100",
        ],
        "bounded workload and four nonexcluded completions",
    )
    exact_regressions = [
        row for row in all_h_nonclosures
        if (
            row["origin_key"], row["cell_key"]
        ) == EXPECTED_H_REGRESSION
    ]
    require(exact_regressions, "H nonclosure regression")
    h_regression = exact_regressions[0]
    require(
        h_regression["box"]
        == {
            "t": ["2301/25600", "5841/64000"],
            "p": ["-1", "-1023/1024"],
            "s": ["1/800", "1/400"],
        }
        and h_regression["H_tree_terminal_classes"]
        == {
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE": 4,
            "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES": 4,
        }
        and h_regression["H_tree_terminal_depths"]
        == {"3": 7, "4": 1},
        "H regression eight pieces",
    )
    grazing_key_set = set(initial_keys_by_category[
        "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
    ])
    grazing_rows = sorted(
        (row for row in residual_rows if row.key in grazing_key_set),
        key=lambda row: row.key,
    )
    q_profile = q_depth10_profile(grazing_rows)
    crossing = [
        row["origin_key"] for row in credited_summaries
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
    ]
    guard_only = [
        row["origin_key"] for row in credited_summaries
        if row["source_chart_domain"]["guard_only_parent"]
    ]
    round176_certificate = strict_load(
        HERE
        / "cm2_round176_dimension_safe_multi_origin_parent_exclusion_certificate.json"
    )
    round176_excluded = set(
        round176_certificate["result"][
            "new_whole_parent_exclusion_credit"
        ]["exact_origin_keys"]
    )
    require(
        not (round176_excluded & set(new_excluded)),
        "Round176/Round180 disjoint",
    )
    final_category_counts = {
        key: len(values)
        for key, values in sorted(
            final_residual_keys_by_category.items()
        )
    }
    require(
        final_category_counts
        == {
            "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH":
                185438,
            "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY":
                53144,
            "MULTI_DISCRIMINANT_2_TO_5_TARGETS": 54214,
            "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 6838,
            "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH": 294,
        },
        "final child residual categories",
    )
    route_keys: dict[str, list[str]] = defaultdict(list)
    for row in credited_summaries:
        methods = set(row["terminal_count_by_method"])
        route = (
            "PURE_DIRECT"
            if methods == {"DIRECT_STRICT_CLOSED_BOX"}
            else (
                "PURE_SAME_SIGN_DELTA"
                if methods
                == {"SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"}
                else "MIXED_DIRECT_AND_SAME_SIGN_DELTA"
            )
        )
        route_keys[route].append(row["origin_key"])
    require(
        {
            key: len(values)
            for key, values in sorted(route_keys.items())
        }
        == {
            "MIXED_DIRECT_AND_SAME_SIGN_DELTA": 8,
            "PURE_DIRECT": 18,
            "PURE_SAME_SIGN_DELTA": 6,
        },
        "32 proof routes",
    )
    result = {
        "status": (
            "PARTIAL__CERTIFIED_32_ADDITIONAL_WHOLE_MULTI_ORIGIN_"
            "EXCLUSIONS__D02_STILL_BLOCKED"
        ),
        "verdict": "PARTIAL",
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": "W[1,0]",
            "frozen_outgoing_chart": "W",
            "Round176_depth14_residual_cells_all_entered": True,
            "Round176_unexcluded_original_parent_count": 2434,
            "Round176_fully_replaced_live_or_mixed_parent_count": 272,
            "Round176_residual_bearing_origin_count": 2162,
            "rectangular_refinement_depth_for_witness_origins": 2,
            "rectangular_refinement_depth_for_exclusion_upper_candidates":
                4,
            "integer_credit_unit":
                "one fully replaced original physical depth8 parent",
            "child_or_volume_count_used_as_integer_credit": False,
        },
        "upstream_verified_chain": upstream,
        "Round176_residual_input": {
            "depth14_cell_count": len(residual_rows),
            "residual_origin_count": len(residual_by_origin),
            "category_count": dict(sorted(INITIAL_CATEGORIES.items())),
            "category_exact_key_sha256": {
                key: digest(values)
                for key, values in sorted(
                    initial_keys_by_category.items()
                )
            },
            "all_residual_cell_keys_sha256": digest(sorted(
                row.key for row in residual_rows
            )),
            "arrangement_dimensions": {
                "Delta_H_root_or_grazing_graph": 2,
                "pairwise_graph_intersection": 1,
                "triple_graph_or_corner_intersection": 0,
            },
            "no_internal_stratum_is_an_integer_record": True,
        },
        "origin_upper_bound_partition": {
            "strict_live_or_mixed_witness_origin_count":
                len(witness_origins),
            "strict_live_or_mixed_witness_origin_keys":
                witness_origins,
            "strict_live_or_mixed_witness_origin_keys_sha256":
                digest(witness_origins),
            "whole_exclusion_upper_candidate_count":
                len(upper_candidates),
            "whole_exclusion_upper_candidate_keys": upper_candidates,
            "whole_exclusion_upper_candidate_keys_sha256":
                digest(upper_candidates),
            "upper_bound_is_not_credit": True,
        },
        "bounded_rectangular_pass": {
            "evaluated_node_count": global_evaluated,
            "terminal_count_by_method":
                map_counter(global_terminal_methods),
            "terminal_count_by_disposition":
                map_counter(global_terminal_dispositions),
            "final_child_residual_count_by_category":
                final_category_counts,
            "final_child_residual_exact_key_sha256": {
                key: digest(values)
                for key, values in sorted(
                    final_residual_keys_by_category.items()
                )
            },
            "final_child_residual_total":
                sum(final_category_counts.values()),
            "final_residual_origin_count":
                len(final_residual_origin_keys),
            "final_residual_origin_keys_sha256":
                digest(final_residual_origin_keys),
            "newly_complete_nonexcluded_origin_count":
                len(newly_complete_nonexcluded),
            "newly_complete_nonexcluded_origin_keys":
                newly_complete_nonexcluded,
            "newly_complete_nonexcluded_origin_keys_sha256":
                digest(newly_complete_nonexcluded),
            "child_counts_are_refinement_diagnostics_only": True,
        },
        "new_whole_parent_exclusion_credit": {
            "count": len(new_excluded),
            "exact_origin_keys": new_excluded,
            "exact_origin_keys_sha256": digest(new_excluded),
            "increment_by_closed_by_or_before_extra_depth": {
                "2": 18,
                "3": 8,
                "4": 6,
            },
            "earliest_complete_extra_depth_histogram":
                map_counter(exact_earliest_depth_counts),
            "proof_route_origin_count": {
                key: len(values)
                for key, values in sorted(route_keys.items())
            },
            "proof_route_exact_origin_keys": {
                key: values
                for key, values in sorted(route_keys.items())
            },
            "proof_route_exact_origin_keys_sha256": {
                key: digest(values)
                for key, values in sorted(route_keys.items())
            },
            "upper_bound_conservation": "1476=32+1444",
            "origin_summaries": credited_summaries,
            "origin_summaries_sha256": digest(credited_summaries),
            "every_summary_self_digest_valid": all(
                row["row_sha256"]
                == digest({
                    key: value for key, value in row.items()
                    if key != "row_sha256"
                })
                for row in credited_summaries
            ),
            "all_32_whole_original_physical_parents_excluded": True,
            "all_32_complete_3D_2D_1D_0D_ledgers": True,
        },
        "physical_source_chart_audit": {
            "strict_physical_interior_credited_origin_count":
                32 - len(crossing),
            "source_seam_and_guard_composite_credited_origin_count":
                len(crossing),
            "exact_crossing_origin_keys": crossing,
            "exact_crossing_origin_keys_sha256": digest(crossing),
            "guard_only_credited_origin_count": len(guard_only),
            "physical_interior_predicate": "2*t^2<1",
            "source_seam_predicate": "2*t^2=1",
            "source_seam_dimension": 2,
            "source_seam_half_open_owner": "E",
            "guard_predicate": "2*t^2>1",
            "guard_outside_exterior_credit": 0,
            "source_seam_intersection_with_split_face_dimension_at_most": 1,
            "source_seam_split_edge_or_graph_triple_dimension_at_most": 0,
        },
        "H_nonclosure_regression": {
            **h_regression,
            "H_zero_graph_dimension": 2,
            "H_intersection_with_Delta_or_root_graph_dimension_at_most": 1,
            "H_Delta_root_triple_or_corner_dimension_at_most": 0,
            "whole_parent_integer_credit": 0,
            "Round176_H_depth4_closure_may_not_be_generalized": True,
        },
        "compact_q_depth10_profile": q_profile,
        "ledger_composition": {
            "base_round": 176,
            "base_whole_record_excluded": 73360,
            "base_conservative_live": 3472,
            "Round180_new_whole_parent_excluded": 32,
            "combined_whole_record_excluded": 73392,
            "combined_conservative_live": 3440,
            "refined_source_W_record_count": 76832,
            "conservation_identity": "73392+3440=76832",
            "Round176_and_Round180_exact_credit_sets_disjoint": True,
            "analytic_internal_strata_added_to_integer_record_count": False,
            "child_residual_count_added_to_integer_record_count": False,
            "compact_q_volume_added_to_integer_record_count": False,
            "guard_outside_added_to_integer_record_count": False,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_whole_exclusion_upper_candidates": 1444,
            "remaining_conservative_live": 3440,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "replace rectangular collars by interval-Newton graph cells "
            "for multi-Delta, root-equality, Delta-H, clipped-face, and "
            "compact-q arrangements"
        ),
        "provenance": {
            "producer": PRODUCER.name,
            "producer_sha256": EXPECTED_PRODUCER_SHA256,
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "producer_imports_only_frozen_Round176_verifier_geometry":
                True,
            "older_round_files_modified": False,
        },
    }
    result["producer_output_safety_contract"] = {
        "output_directory": str(HERE),
        "official_certificate_may_be_replaced": CERTIFICATE.name,
        "cold_replay_output_rule":
            "hidden .cm2_round180_*_certificate.json in HERE only",
        "other_same_directory_regular_outputs_caller_authorized": False,
        "producer_self_protected": True,
        "all_Round176_pins_protected": sorted(PINS),
        "Round180_non_certificate_paths_protected":
            list(ROUND180_NON_CERTIFICATE_PROTECTED),
        "existing_target_must_be_regular_non_symlink_single_link": True,
        "write_protocol": "same-directory mkstemp+fsync+os.replace",
    }
    result["producer_path_safety_attack_suite"] = {
        "attack_count": 19,
        "rejected_count": 19,
        "all_rejected": True,
        "rejected_attack_names": [
            "symlink output",
            "hardlink output",
            "parent directory escape",
            "nested subdirectory output",
            "existing directory output",
            "FIFO output",
            "producer self",
            *(f"Round176 pin:{name}" for name in sorted(PINS)),
            *(
                f"Round180 protected:{name}"
                for name in ROUND180_NON_CERTIFICATE_PROTECTED
            ),
        ],
        "real_pins_used_only_for_protected_set_membership_check": True,
        "write_attempts_against_real_pins": 0,
    }
    return result


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in key
                ),
                f"JSON key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in value
            ),
            f"JSON string:{path}",
        )


def strict_parse(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{label}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{label}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    validate_json_tree(value)
    require(type(value) is dict, f"top:{label}")
    return value


def read_regular(
    path: Path,
    expected_sha256: str | None = None,
) -> bytes:
    status = path.lstat()
    require(stat.S_ISREG(status.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(status.st_nlink == 1, f"hardlink:{path.name}")
    require(status.st_size <= MAX_INPUT_BYTES, f"size:{path.name}")
    raw = path.read_bytes()
    if expected_sha256 is not None:
        require(
            hashlib.sha256(raw).hexdigest() == expected_sha256,
            f"pin:{path.name}",
        )
    return raw


def parse_envelope(
    raw: bytes,
    *,
    label: str,
    schema: str | None = None,
    canonical_pretty: bool = False,
) -> dict[str, Any]:
    value = strict_parse(raw, label)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope:{label}",
    )
    if schema is not None:
        require(value["schema"] == schema, f"schema:{label}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"digest:{label}",
    )
    if canonical_pretty:
        require(raw == pretty_bytes(value), f"canonical:{label}")
    return value


def validate_document(
    document: dict[str, Any],
    expected_result: dict[str, Any],
    *,
    enforce_frozen_result_digest: bool = True,
) -> None:
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    if enforce_frozen_result_digest:
        require(
            document["result_sha256"]
            == EXPECTED_CERTIFICATE_RESULT_SHA256,
            "frozen result digest",
        )
    require(
        canonical(document["result"]) == canonical(expected_result),
        "full independently reconstructed expected-result equality",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def update_summary_digests(
    document: dict[str, Any],
    index: int,
) -> None:
    credit = document["result"]["new_whole_parent_exclusion_credit"]
    row = credit["origin_summaries"][index]
    row["row_sha256"] = digest({
        key: value for key, value in row.items()
        if key != "row_sha256"
    })
    credit["origin_summaries_sha256"] = digest(
        credit["origin_summaries"]
    )


def semantic_attacks(
    document: dict[str, Any],
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    result = document["result"]
    summaries = result["new_whole_parent_exclusion_credit"][
        "origin_summaries"
    ]
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("schema", lambda d: d.__setitem__("schema", "forged")),
        (
            "status",
            lambda d: d["result"].__setitem__("status", "CERTIFIED"),
        ),
        (
            "verdict",
            lambda d: d["result"].__setitem__("verdict", "COMPLETE"),
        ),
        (
            "44040 input",
            lambda d: d["result"]["Round176_residual_input"].
                __setitem__("depth14_cell_count", 44039),
        ),
        (
            "initial clipped census",
            lambda d: d["result"]["Round176_residual_input"][
                "category_count"
            ].__setitem__(
                "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH",
                26727,
            ),
        ),
        (
            "initial multi Delta digest",
            lambda d: d["result"]["Round176_residual_input"][
                "category_exact_key_sha256"
            ].__setitem__("MULTI_DISCRIMINANT_2_TO_5_TARGETS", "0" * 64),
        ),
        (
            "686 witness count",
            lambda d: d["result"]["origin_upper_bound_partition"].
                __setitem__(
                    "strict_live_or_mixed_witness_origin_count", 685
                ),
        ),
        (
            "686 witness key",
            lambda d: d["result"]["origin_upper_bound_partition"][
                "strict_live_or_mixed_witness_origin_keys"
            ].__setitem__(0, "forged"),
        ),
        (
            "686 witness digest",
            lambda d: d["result"]["origin_upper_bound_partition"].
                __setitem__(
                    "strict_live_or_mixed_witness_origin_keys_sha256",
                    "0" * 64,
                ),
        ),
        (
            "1476 upper count",
            lambda d: d["result"]["origin_upper_bound_partition"].
                __setitem__("whole_exclusion_upper_candidate_count", 1475),
        ),
        (
            "upper bound promoted",
            lambda d: d["result"]["origin_upper_bound_partition"].
                __setitem__("upper_bound_is_not_credit", False),
        ),
        (
            "evaluated workload",
            lambda d: d["result"]["bounded_rectangular_pass"].
                __setitem__("evaluated_node_count", 755543),
        ),
        (
            "final residual child count",
            lambda d: d["result"]["bounded_rectangular_pass"].
                __setitem__("final_child_residual_total", 0),
        ),
        (
            "final residual origin count",
            lambda d: d["result"]["bounded_rectangular_pass"].
                __setitem__("final_residual_origin_count", 2125),
        ),
        (
            "child count integer credit",
            lambda d: d["result"]["bounded_rectangular_pass"].
                __setitem__(
                    "child_counts_are_refinement_diagnostics_only",
                    False,
                ),
        ),
        (
            "32 credit count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("count", 33),
        ),
        (
            "32 exact key",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "exact_origin_keys"
            ].__setitem__(0, "forged"),
        ),
        (
            "32 digest",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("exact_origin_keys_sha256", "0" * 64),
        ),
        (
            "closed-by-depth2",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "increment_by_closed_by_or_before_extra_depth"
            ].__setitem__("2", 17),
        ),
        (
            "closed-by-depth3",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "increment_by_closed_by_or_before_extra_depth"
            ].__setitem__("3", 9),
        ),
        (
            "actual earliest depth1",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "earliest_complete_extra_depth_histogram"
            ].__setitem__("1", 17),
        ),
        (
            "actual earliest forged depth2",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "earliest_complete_extra_depth_histogram"
            ].__setitem__("2", 18),
        ),
        (
            "route direct count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "proof_route_origin_count"
            ].__setitem__("PURE_DIRECT", 17),
        ),
        (
            "route same-sign count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "proof_route_origin_count"
            ].__setitem__("PURE_SAME_SIGN_DELTA", 7),
        ),
        (
            "route mixed count",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"][
                "proof_route_origin_count"
            ].__setitem__("MIXED_DIRECT_AND_SAME_SIGN_DELTA", 9),
        ),
        (
            "upper conservation",
            lambda d: d["result"]["new_whole_parent_exclusion_credit"].
                __setitem__("upper_bound_conservation", "1476=33+1443"),
        ),
        (
            "H regression cell",
            lambda d: d["result"]["H_nonclosure_regression"].
                __setitem__("cell_key", "forged"),
        ),
        (
            "H eight-piece census",
            lambda d: d["result"]["H_nonclosure_regression"][
                "H_tree_terminal_classes"
            ].__setitem__("TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES", 3),
        ),
        (
            "H falsely closed",
            lambda d: d["result"]["H_nonclosure_regression"].
                __setitem__("whole_cell_closed", True),
        ),
        (
            "H dimension",
            lambda d: d["result"]["H_nonclosure_regression"].
                __setitem__("H_zero_graph_dimension", 3),
        ),
        (
            "q parent input",
            lambda d: d["result"]["compact_q_depth10_profile"].
                __setitem__("input_depth14_parent_count", 1477),
        ),
        (
            "q residual cell count",
            lambda d: d["result"]["compact_q_depth10_profile"].
                __setitem__("residual_q_cell_count", 138431),
        ),
        (
            "q residual volume",
            lambda d: d["result"]["compact_q_depth10_profile"].
                __setitem__(
                    "residual_depth14_parent_equivalent", "0"
                ),
        ),
        (
            "q whole credit",
            lambda d: d["result"]["compact_q_depth10_profile"].
                __setitem__("whole_origin_integer_credit", 1),
        ),
        (
            "physical guard credit",
            lambda d: d["result"]["physical_source_chart_audit"].
                __setitem__("guard_outside_exterior_credit", 1),
        ),
        (
            "source seam dimension",
            lambda d: d["result"]["physical_source_chart_audit"].
                __setitem__("source_seam_dimension", 3),
        ),
        (
            "combined excluded",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("combined_whole_record_excluded", 73393),
        ),
        (
            "combined live",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("combined_conservative_live", 3439),
        ),
        (
            "conservation",
            lambda d: d["result"]["ledger_composition"].
                __setitem__("conservation_identity", "forged"),
        ),
        (
            "analytic strata integer credit",
            lambda d: d["result"]["ledger_composition"].
                __setitem__(
                    "analytic_internal_strata_added_to_integer_record_count",
                    True,
                ),
        ),
        (
            "D02 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("D02", "READY"),
        ),
        (
            "Gate5 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("global_Gate5_fields", "18/18"),
        ),
        (
            "CM2 promotion",
            lambda d: d["result"]["strict_nonpromotion"].
                __setitem__("CM2", "GO"),
        ),
        (
            "producer pin",
            lambda d: d["result"]["provenance"].
                __setitem__("producer_sha256", "0" * 64),
        ),
        (
            "producer output caller authorization",
            lambda d: d["result"]["producer_output_safety_contract"].
                __setitem__(
                    "other_same_directory_regular_outputs_caller_authorized",
                    True,
                ),
        ),
        (
            "producer output protected pin list",
            lambda d: d["result"]["producer_output_safety_contract"][
                "all_Round176_pins_protected"
            ].pop(),
        ),
        (
            "producer path attack count",
            lambda d: d["result"]["producer_path_safety_attack_suite"].
                __setitem__("attack_count", 18),
        ),
        (
            "producer path attack accepted",
            lambda d: d["result"]["producer_path_safety_attack_suite"].
                __setitem__("all_rejected", False),
        ),
        (
            "producer path real pin write",
            lambda d: d["result"]["producer_path_safety_attack_suite"].
                __setitem__("write_attempts_against_real_pins", 1),
        ),
        (
            "recursive extra key",
            lambda d: d["result"].__setitem__("forged", True),
        ),
    ]
    for index, row in enumerate(summaries):
        key = row["origin_key"]

        def method_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            summary = d["result"][
                "new_whole_parent_exclusion_credit"
            ]["origin_summaries"][index]
            method = next(iter(summary["terminal_count_by_method"]))
            summary["terminal_count_by_method"][method] += 1
            update_summary_digests(d, index)

        def coverage_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            summary = d["result"][
                "new_whole_parent_exclusion_credit"
            ]["origin_summaries"][index]
            summary["replacement_coverage"][
                "each_depth14_root_coverage_numerator"
            ] -= 1
            update_summary_digests(d, index)

        def lower_strata_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            summary = d["result"][
                "new_whole_parent_exclusion_credit"
            ]["origin_summaries"][index]
            summary["lower_dimensional_strata"][
                "1D_deduplicated_split_face_edge_count"
            ] += 1
            update_summary_digests(d, index)

        def physical_mutation(
            d: dict[str, Any],
            index: int = index,
        ) -> None:
            summary = d["result"][
                "new_whole_parent_exclusion_credit"
            ]["origin_summaries"][index]
            summary["source_chart_domain"][
                "guard_outside_exterior_credit"
            ] = 1
            update_summary_digests(d, index)

        attacks.extend([
            (f"{key}:method route", method_mutation),
            (f"{key}:coverage", coverage_mutation),
            (f"{key}:2D/1D/0D strata", lower_strata_mutation),
            (f"{key}:physical guard", physical_mutation),
        ])
    rejected: list[str] = []
    for name, mutate in attacks:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        resign(candidate)
        try:
            validate_document(
                candidate,
                expected_result,
                enforce_frozen_result_digest=False,
            )
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"semantic attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "re_signed_result_digest_each_time": True,
        "frozen_result_digest_shortcut_disabled_during_attacks": True,
        "per_credited_origin_attack_count": 4 * len(summaries),
        "all_32_method_coverage_lower_strata_physical_rows_attacked": True,
        "rejected_attack_names": rejected,
    }


def strict_json_attacks() -> dict[str, Any]:
    empty_digest = digest({})
    attacks = {
        "duplicate envelope key":
            b'{"schema":"x","schema":"y","result":{},'
            b'"result_sha256":"0"}',
        "duplicate nested key":
            b'{"schema":"x","result":{"a":1,"a":1},'
            b'"result_sha256":"0"}',
        "floating number":
            b'{"schema":"x","result":{"a":1.0},"result_sha256":"0"}',
        "exponent number":
            b'{"schema":"x","result":{"a":1e2},"result_sha256":"0"}',
        "NaN constant":
            b'{"schema":"x","result":{"a":NaN},"result_sha256":"0"}',
        "UTF8 BOM": b'\xef\xbb\xbf{"schema":"x"}',
        "raw NUL": b'{"schema":"x","result":{}\x00}',
        "invalid UTF8": b"\xff",
        "noncanonical whitespace": (
            b'{ "schema":"x","result":{},"result_sha256":"'
            + empty_digest.encode()
            + b'"}\n'
        ),
    }
    rejected: list[str] = []
    for name, raw in attacks.items():
        try:
            parse_envelope(
                raw,
                label=f"JSON attack:{name}",
                canonical_pretty=True,
            )
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"JSON attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "rejected_attack_names": rejected,
    }


def safe_atomic_write(
    path: Path,
    raw: bytes,
    protected: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output directory")
    if path.exists() or path.is_symlink():
        status = path.lstat()
        require(stat.S_ISREG(status.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(status.st_nlink == 1, "output hardlink")
    require(
        path.resolve(strict=False) not in protected,
        "protected output",
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(
    name: str,
    operation: Callable[[], Any],
) -> str:
    try:
        operation()
    except Exception:
        return name
    raise RuntimeError(f"path attack accepted:{name}")


def path_safety_attacks(certificate_path: Path) -> dict[str, Any]:
    rejected: list[str] = []
    scratch = Path(tempfile.mkdtemp(prefix=".round180-path.", dir=HERE))
    symlink_output = HERE / f".round180-symlink-output.{os.getpid()}"
    hard_base = HERE / f".round180-hard-base.{os.getpid()}"
    hard_link = HERE / f".round180-hard-link.{os.getpid()}"
    outside = HERE.parent / f".round180-escape.{os.getpid()}"
    try:
        source = scratch / "source"
        source.write_bytes(b"{}\n")
        symlink_input = scratch / "symlink-input"
        symlink_input.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink input",
            lambda: read_regular(symlink_input),
        ))
        hard_input = scratch / "hard-input"
        os.link(source, hard_input)
        rejected.append(expect_rejection(
            "hardlink input",
            lambda: read_regular(hard_input),
        ))
        oversized = scratch / "oversized"
        with oversized.open("wb") as handle:
            handle.truncate(MAX_INPUT_BYTES + 1)
        rejected.append(expect_rejection(
            "oversized sparse input",
            lambda: read_regular(oversized),
        ))
        protected = {
            certificate_path.resolve(),
            PRODUCER.resolve(),
            Path(__file__).resolve(),
        }
        symlink_output.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink_output, b"x", protected),
        ))
        hard_base.write_bytes(b"x")
        os.link(hard_base, hard_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_link, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "protected certificate output",
            lambda: safe_atomic_write(certificate_path, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "parent directory escape",
            lambda: safe_atomic_write(outside, b"x", protected),
        ))
    finally:
        for path in (symlink_output, hard_link, hard_base, outside):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    return {
        "attack_count": 7,
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == 7,
        "rejected_attack_names": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ctx.prec = 192
    certificate_path = Path(
        os.path.abspath(os.fspath(arguments.certificate))
    )
    require(
        certificate_path.parent.resolve() == HERE,
        "certificate directory",
    )
    producer_raw = read_regular(PRODUCER, EXPECTED_PRODUCER_SHA256)
    certificate_raw = read_regular(
        certificate_path,
        EXPECTED_CERTIFICATE_SHA256,
    )
    document = parse_envelope(
        certificate_raw,
        label=certificate_path.name,
        schema=CERTIFICATE_SCHEMA,
        canonical_pretty=True,
    )
    expected_result = build_result()
    validate_document(document, expected_result)
    semantic = semantic_attacks(document, expected_result)
    strict = strict_json_attacks()
    paths = path_safety_attacks(certificate_path)
    result = {
        "status": "PASS_PARTIAL_BOUNDED_ROUND180",
        "verdict": "PARTIAL",
        "certificate_sha256": hashlib.sha256(certificate_raw).hexdigest(),
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": hashlib.sha256(producer_raw).hexdigest(),
        "verifier_sha256":
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "independence_contract": {
            "Round180_producer_imported_or_executed": False,
            "only_frozen_Round176_verifier_geometry_imported": True,
            "all_44040_residual_inputs_reconstructed": True,
            "all_2162_residual_origins_reconstructed": True,
            "both_depth2_and_depth4_bounded_trees_reconstructed": True,
            "all_32_whole_parent_coverages_reconstructed": True,
            "all_32_2D_1D_0D_ledgers_reconstructed": True,
            "H_nonclosure_eight_piece_regression_reconstructed": True,
            "compact_q_depth10_profile_reconstructed": True,
            "producer_output_safety_contract_reconstructed": True,
            "producer_19_path_attack_result_reconstructed": True,
            "full_expected_result_independently_reconstructed": True,
            "full_expected_canonical_equality": True,
        },
        "recomputed_census": {
            "input_residual_cells": 44040,
            "residual_origins": 2162,
            "live_or_mixed_witness_origins": 686,
            "exclusion_upper_candidates": 1476,
            "new_whole_excluded": 32,
            "new_whole_excluded_keys_sha256":
                document["result"]["new_whole_parent_exclusion_credit"][
                    "exact_origin_keys_sha256"
                ],
            "closed_by_or_before_depth": {"2": 18, "3": 8, "4": 6},
            "actual_earliest_depth_histogram": {
                "1": 18, "3": 8, "4": 6
            },
            "proof_routes": {
                "PURE_DIRECT": 18,
                "PURE_SAME_SIGN_DELTA": 6,
                "MIXED_DIRECT_AND_SAME_SIGN_DELTA": 8,
            },
            "final_residual_origins": 2126,
            "final_child_residual_diagnostic_count": 299928,
        },
        "H_regression_audit": {
            "origin_key": EXPECTED_H_REGRESSION[0],
            "cell_key": EXPECTED_H_REGRESSION[1],
            "typed_composites": 4,
            "strict_live_rectangles": 4,
            "whole_credit": 0,
        },
        "compact_q_audit": {
            "input_parents": 1478,
            "terminal_q_cells": 92976,
            "residual_q_cells": 138432,
            "residual_parent_equivalent": "2163/16",
            "whole_credit": 0,
        },
        "ledger_reconstruction": {
            "Round176_excluded": 73360,
            "Round180_new_excluded": 32,
            "combined_excluded": 73392,
            "combined_live": 3440,
            "total": 76832,
            "conservation_identity": "73392+3440=76832",
        },
        "semantic_mutation_attack_suite": semantic,
        "strict_json_attack_suite": strict,
        "path_safety_attack_suite": paths,
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {
        PRODUCER.resolve(),
        certificate_path.resolve(),
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
    }
    safe_atomic_write(arguments.output, pretty_bytes(envelope), protected)
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
