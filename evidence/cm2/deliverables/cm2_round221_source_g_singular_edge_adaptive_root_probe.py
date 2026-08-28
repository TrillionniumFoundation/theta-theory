#!/usr/bin/env python3
"""Outcome-blind adaptive probe for the 252 derivative-unavailable edges."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Any

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round219_source_g_partial_face_common_refinement_glue as r219
import cm2_round221_source_g_endpoint_edge_root_census_probe as edge


HERE = Path(__file__).resolve().parent
R219_CERTIFICATE_SHA256 = (
    "8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096"
)
R219_RESULT_SHA256 = (
    "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e"
)
MAX_DEPTH = 8
STRICT = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class ProbeError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


def edge_class(
    row: dict[str, Any],
    frontier: dict[str, Any],
    interval: tuple[Q, Q],
    label: str,
) -> tuple[str, tuple[str, str, str]]:
    graph_signs = row["selected_lower_upper_derivative_signs"]
    endpoint = "LOWER" if graph_signs[0] not in STRICT else "UPPER"
    graph_coordinate = Q(
        row["graph_interval"][0 if endpoint == "LOWER" else 1]
    )
    lower, upper = interval
    full_box, derivative_index = edge.edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        lower,
        upper,
        label + ":full",
    )
    lower_box, _ = edge.edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        lower,
        lower,
        label + ":lower",
    )
    upper_box, _ = edge.edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        upper,
        upper,
        label + ":upper",
    )
    chart = frontier["source_chart"]
    target = frontier["target_lift"]
    active = frontier["active_factor"]
    full = r186.factor_geometry(chart, target, full_box)[active]
    full_value_sign = r186.r179.arb_sign(full[0])
    derivative = full[1][derivative_index]
    derivative_sign = (
        "DERIVATIVE_UNAVAILABLE"
        if derivative is None
        else r186.r179.arb_sign(derivative)
    )
    lower_sign = edge.selected_sign(
        chart, target, active, lower_box
    )
    upper_sign = edge.selected_sign(
        chart, target, active, upper_box
    )
    if full_value_sign in STRICT:
        classification = "STRICT_INTERVAL_ZERO_ABSENT"
    elif (
        derivative_sign in STRICT
        and lower_sign in STRICT
        and upper_sign in STRICT
    ):
        classification = (
            "UNIQUE_INTERIOR_ROOT"
            if lower_sign != upper_sign
            else "STRICT_MONOTONE_ZERO_ABSENT"
        )
    else:
        classification = "UNRESOLVED"
    return classification, (
        lower_sign,
        upper_sign,
        derivative_sign,
    )


def main() -> int:
    certificate = HERE / (
        "cm2_round219_source_g_partial_face_common_refinement_glue"
        "_certificate.json"
    )
    raw = certificate.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == R219_CERTIFICATE_SHA256,
        "Round219 certificate pin",
    )
    envelope = json.loads(raw)
    require(
        envelope["result_sha256"] == R219_RESULT_SHA256
        and r219.digest(envelope["result"]) == R219_RESULT_SHA256,
        "Round219 result pin",
    )
    unresolved = [
        row
        for row in envelope["result"][
            "formal_terminal_subface_ledger"
        ]["rows"]
        if row["classification"] == "UNRESOLVED"
        and row["fixed_axis"] == "s"
    ]
    (
        _result217,
        exact_frontier,
        _partial_frontier,
        _evaluators,
        _hashes,
    ) = r219.load_boundary()
    frontier_by_id = {
        row["frontier_row_id"]: row for row in exact_frontier
    }
    ctx.prec = 256

    # Select exactly the full intervals whose transverse derivative is absent.
    selected: list[
        tuple[str, dict[str, Any], dict[str, Any], str, tuple[Q, Q]]
    ] = []
    for row in unresolved:
        frontier = frontier_by_id[row["Round217_frontier_row_id"]]
        interval = tuple(
            Q(value) for value in row["transverse_interval"]
        )
        classification, signs = edge_class(
            row, frontier, interval, row["terminal_subface_row_id"]
        )
        if (
            classification == "UNRESOLVED"
            and signs[2] == "DERIVATIVE_UNAVAILABLE"
        ):
            selected.append(
                (
                    row["terminal_subface_row_id"],
                    row,
                    frontier,
                    "",
                    interval,
                )
            )
    require(len(selected) == 252, "252 singular-edge rows")

    active = selected
    finished_by_parent: dict[str, list[str]] = {
        item[0]: [] for item in selected
    }
    per_depth: list[dict[str, Any]] = []
    started = time.perf_counter()
    for depth in range(1, MAX_DEPTH + 1):
        following: list[
            tuple[
                str,
                dict[str, Any],
                dict[str, Any],
                str,
                tuple[Q, Q],
            ]
        ] = []
        counts = Counter()
        layer_started = time.perf_counter()
        for parent_id, row, frontier, path, (lower, upper) in active:
            midpoint = (lower + upper) / 2
            for suffix, interval in (
                ("L", (lower, midpoint)),
                ("R", (midpoint, upper)),
            ):
                child_path = path + suffix
                classification, _signs = edge_class(
                    row,
                    frontier,
                    interval,
                    f"{parent_id}:{child_path}",
                )
                counts[classification] += 1
                if classification == "UNRESOLVED":
                    following.append(
                        (
                            parent_id,
                            row,
                            frontier,
                            child_path,
                            interval,
                        )
                    )
                else:
                    finished_by_parent[parent_id].append(classification)
        remaining_parents = {item[0] for item in following}
        complete_parents = (
            len(finished_by_parent) - len(remaining_parents)
        )
        per_depth.append({
            "depth": depth,
            "evaluations": 2 * len(active),
            "classification_counts": dict(sorted(counts.items())),
            "remaining_UNRESOLVED_children": len(following),
            "complete_original_edge_rows": complete_parents,
            "remaining_original_edge_rows": len(remaining_parents),
            "elapsed_seconds": round(
                time.perf_counter() - layer_started, 6
            ),
        })
        print(
            json.dumps(per_depth[-1], sort_keys=True),
            file=sys.stderr,
            flush=True,
        )
        active = following
        if not active:
            break

    complete = set(finished_by_parent) - {item[0] for item in active}
    complete_histogram = Counter(
        tuple(sorted(finished_by_parent[parent_id]))
        for parent_id in complete
    )
    output = {
        "status": "OUTCOME_BLIND_READ_ONLY_PROBE_NO_FORMAL_CREDIT",
        "Round219_certificate_sha256": R219_CERTIFICATE_SHA256,
        "Round219_result_sha256": R219_RESULT_SHA256,
        "starting_derivative_unavailable_edge_rows": len(selected),
        "maximum_adaptive_depth": MAX_DEPTH,
        "per_depth": per_depth,
        "complete_original_edge_rows": len(complete),
        "remaining_original_edge_rows":
            len({item[0] for item in active}),
        "complete_terminal_class_multiset_histogram": {
            "|".join(key): value
            for key, value in sorted(complete_histogram.items())
        },
        "elapsed_seconds": round(
            time.perf_counter() - started, 6
        ),
        "formal_credit_granted": False,
        "component_or_global_credit_granted": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
