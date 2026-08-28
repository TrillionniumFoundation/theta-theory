#!/usr/bin/env python3
"""Outcome-blind monotone endpoint-edge root census for Round219.

For every terminal subface left UNRESOLVED by Round219, this read-only probe
identifies the one non-strict graph endpoint, restricts the active factor to
that endpoint edge, and checks strict endpoint signs plus the full transverse
derivative.  It grants no formal credit.
"""

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


HERE = Path(__file__).resolve().parent
R219_SOURCE_SHA256 = (
    "8b670ffbcabd5a9796fb67580cbb9e3318b8eb2ee1cd65c5e71f7f1f360b3019"
)
R219_CERTIFICATE_SHA256 = (
    "8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096"
)
R219_RESULT_SHA256 = (
    "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e"
)
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)
STRICT = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class ProbeError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_box(
    fixed_axis: str,
    graph_coordinate: Q,
    fixed_coordinate: Q,
    lower: Q,
    upper: Q,
    label: str,
) -> tuple[Any, int]:
    atlas = r186.r179.r174.atlas.AtlasBox
    if fixed_axis == "p":
        return (
            atlas(
                graph_coordinate,
                graph_coordinate,
                fixed_coordinate,
                fixed_coordinate,
                lower,
                upper,
                0,
                label,
            ),
            2,
        )
    require(fixed_axis == "s", "fixed p/s face")
    return (
        atlas(
            graph_coordinate,
            graph_coordinate,
            lower,
            upper,
            fixed_coordinate,
            fixed_coordinate,
            0,
            label,
        ),
        1,
    )


def selected_sign(
    chart: str,
    target: str,
    active: str,
    box: Any,
) -> str:
    direct = r186.r179.arb_sign(
        r186.factor_geometry(chart, target, box)[active][0]
    )
    if direct in STRICT:
        return direct
    return r186.r179.arb_sign(
        r186.centered_value(chart, target, box, active)
    )


def main() -> int:
    require(
        sha256(HERE / r219.__file__.split("/")[-1])
        == R219_SOURCE_SHA256,
        "Round219 source pin",
    )
    require(
        sha256(HERE / r186.__file__.split("/")[-1])
        == R186_SOURCE_SHA256,
        "Round186 source pin",
    )
    certificate_path = HERE / (
        "cm2_round219_source_g_partial_face_common_refinement_glue"
        "_certificate.json"
    )
    raw = certificate_path.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == R219_CERTIFICATE_SHA256,
        "Round219 certificate pin",
    )
    envelope = json.loads(raw)
    require(
        envelope["result_sha256"] == R219_RESULT_SHA256
        and r219.digest(envelope["result"]) == R219_RESULT_SHA256,
        "Round219 result closure",
    )
    unresolved = [
        row
        for row in envelope["result"][
            "formal_terminal_subface_ledger"
        ]["rows"]
        if row["classification"] == "UNRESOLVED"
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

    census = Counter()
    contact_classes: dict[str, list[str]] = {}
    started = time.perf_counter()
    for index, row in enumerate(unresolved, 1):
        frontier = frontier_by_id[row["Round217_frontier_row_id"]]
        signs = row["selected_lower_upper_derivative_signs"]
        require(
            signs[2] in STRICT
            and ((signs[0] in STRICT) ^ (signs[1] in STRICT)),
            "exactly one ambiguous graph endpoint and strict graph derivative",
        )
        endpoint = "LOWER" if signs[0] not in STRICT else "UPPER"
        graph_coordinate = Q(
            row["graph_interval"][0 if endpoint == "LOWER" else 1]
        )
        lower, upper = (
            Q(value) for value in row["transverse_interval"]
        )
        full_box, derivative_index = edge_box(
            row["fixed_axis"],
            graph_coordinate,
            Q(row["shared_coordinate"]),
            lower,
            upper,
            f"round221-edge-full:{row['terminal_subface_row_id']}",
        )
        lower_box, _ = edge_box(
            row["fixed_axis"],
            graph_coordinate,
            Q(row["shared_coordinate"]),
            lower,
            lower,
            f"round221-edge-lower:{row['terminal_subface_row_id']}",
        )
        upper_box, _ = edge_box(
            row["fixed_axis"],
            graph_coordinate,
            Q(row["shared_coordinate"]),
            upper,
            upper,
            f"round221-edge-upper:{row['terminal_subface_row_id']}",
        )
        chart = frontier["source_chart"]
        target = frontier["target_lift"]
        active = frontier["active_factor"]
        full = r186.factor_geometry(
            chart, target, full_box
        )[active]
        derivative = full[1][derivative_index]
        derivative_sign = (
            "DERIVATIVE_UNAVAILABLE"
            if derivative is None
            else r186.r179.arb_sign(derivative)
        )
        lower_sign = selected_sign(
            chart, target, active, lower_box
        )
        upper_sign = selected_sign(
            chart, target, active, upper_box
        )
        if (
            derivative_sign in STRICT
            and lower_sign in STRICT
            and upper_sign in STRICT
        ):
            edge_class = (
                "UNIQUE_INTERIOR_ROOT"
                if lower_sign != upper_sign
                else "STRICT_MONOTONE_ZERO_ABSENT"
            )
        else:
            edge_class = "UNRESOLVED"
        census[
            (
                row["fixed_axis"],
                endpoint,
                edge_class,
                lower_sign,
                upper_sign,
                derivative_sign,
            )
        ] += 1
        contact_classes.setdefault(
            row["contact_row_id"], []
        ).append(edge_class)
        if index % 1000 == 0:
            print(
                f"Round221 endpoint edges {index}/{len(unresolved)}",
                file=sys.stderr,
                flush=True,
            )

    edge_class_counts = Counter()
    for key, value in census.items():
        edge_class_counts[key[2]] += value
    contact_class_sets = Counter(
        tuple(sorted(classes))
        for classes in contact_classes.values()
    )
    output = {
        "status": "OUTCOME_BLIND_READ_ONLY_PROBE_NO_FORMAL_CREDIT",
        "Round219_source_sha256": R219_SOURCE_SHA256,
        "Round219_certificate_sha256": R219_CERTIFICATE_SHA256,
        "Round219_result_sha256": R219_RESULT_SHA256,
        "Round186_source_sha256": R186_SOURCE_SHA256,
        "effective_Arb_precision_bits": ctx.prec,
        "UNRESOLVED_terminal_subface_count": len(unresolved),
        "incomplete_contact_count": len(contact_classes),
        "edge_class_counts": dict(sorted(edge_class_counts.items())),
        "contact_edge_class_multiset_histogram": {
            "|".join(key): value
            for key, value in sorted(contact_class_sets.items())
        },
        "detailed_census": [
            {
                "fixed_axis": key[0],
                "graph_endpoint": key[1],
                "edge_class": key[2],
                "lower_transverse_endpoint_sign": key[3],
                "upper_transverse_endpoint_sign": key[4],
                "full_transverse_derivative_sign": key[5],
                "count": value,
            }
            for key, value in sorted(census.items())
        ],
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
