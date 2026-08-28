#!/usr/bin/env python3
"""Independent row-by-row audit of the Round277 active-graph edge ledger.

This verifier consumes inert witness bytes.  It does not import the witness
producer or its verifier.  It rebuilds the candidate identity from the frozen
Round277 runtime universe, re-evaluates every exact face patch and both
corridors with the frozen Round174 evaluator, and checks the exact
32,416-regular / 252-endpoint partition.

This remains a zero-credit audit: local geometric witnesses are not occurrence
materialization, DSU unions, or maximality certificates.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
from fractions import Fraction as Q
from pathlib import Path

from flint import ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277


HERE = Path(__file__).resolve().parent
LEDGER = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_face_edge_witnesses_zero_credit.json.gz"
)
RESIDUAL = (
    HERE
    / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
)
TAILS = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_remaining_tails_zero_credit.json.gz"
)
STRATEGY_RESULT = (
    HERE
    / "cm2_round277_source_g_depth8_residual_active_graph_strategy_probe_result.json"
)
SOURCE_FACTOR_AUDIT = (
    HERE
    / "cm2_round277_source_g_active_graph_wall_source_factor_audit_result.json"
)
OUTPUT = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_face_edge_witnesses_independent_audit_result.json"
)

ROWS: list[dict] = []


def load_gzip(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def parse_fraction(value: str) -> Q:
    parsed = Q(value)
    assert str(parsed) == value
    return parsed


def parse_box(values: list[str]) -> tuple[Q, ...]:
    assert len(values) == 6
    return tuple(parse_fraction(value) for value in values)


def inside(values: tuple[Q, ...], bounds: tuple[Q, ...]) -> bool:
    return all(
        bounds[2 * axis]
        <= values[2 * axis]
        <= values[2 * axis + 1]
        <= bounds[2 * axis + 1]
        for axis in range(3)
    )


def split_rect(rect: tuple[tuple[Q, Q], tuple[Q, Q]]):
    widths = [upper - lower for lower, upper in rect]
    split = 0 if widths[0] >= widths[1] else 1
    lower, upper = rect[split]
    midpoint = (lower + upper) / 2
    children = []
    for side, interval in enumerate(((lower, midpoint), (midpoint, upper))):
        child = list(rect)
        child[split] = interval
        children.append((tuple(child), split, side))
    return children


def follow_path(overlap: tuple, path: list[str]) -> tuple:
    rect = overlap
    for token in path:
        requested_split, requested_side = map(int, token.split(":"))
        children = split_rect(rect)
        child, split, side = children[requested_side]
        assert requested_split == split and requested_side == side
        rect = child
    assert len(path) == 8
    return rect


def face_box(axis: int, coordinate: Q, rect: tuple) -> tuple[Q, ...]:
    values = []
    tangent = 0
    for current_axis in range(3):
        if current_axis == axis:
            values.extend((coordinate, coordinate))
        else:
            values.extend(rect[tangent])
            tangent += 1
    return tuple(values)


def signature_hash(
    chart: str, target: str, values: tuple[Q, ...], label: str
) -> tuple[str | None, tuple[str, ...]]:
    box = r174.atlas.AtlasBox(*values, 0, label)
    signature, rejected = r174.dynamic_signature(
        chart, box, target, r277.TABLES
    )
    if signature is None:
        return None, tuple(rejected)
    return r276.digest(r277.payload(signature, chart)), ()


def wall_source_factor_sign(
    chart: str,
    target: str,
    values: tuple[Q, ...],
    reason: str,
) -> str:
    _kind, axis, wall = reason.split(":")
    geometry = r179.interval_geometry(
        chart,
        target,
        r174.atlas.AtlasBox(
            *values, 0, "round277-audit-wall-source-factor"
        ),
    )
    dual = geometry["source_x" if axis == "X" else "source_y"]
    return r179.sign(dual[0] - r179.arb(int(wall)))


def expected_regular_patch(
    axis: int,
    coordinate: Q,
    rect: tuple,
    seed: tuple[Q, Q, Q],
    depth: int,
) -> tuple[Q, ...]:
    tangential_axes = [current for current in range(3) if current != axis]
    patch_rect = []
    for tangent_index, current_axis in enumerate(tangential_axes):
        lower, upper = rect[tangent_index]
        value = seed[current_axis]
        span = upper - lower
        width = span / (2**depth)
        if value == lower:
            interval = (lower, lower + width)
        elif value == upper:
            interval = (upper - width, upper)
        else:
            half = min(value - lower, upper - value) / (2**depth)
            assert half > 0
            interval = (value - half, value + half)
        patch_rect.append(interval)
    return face_box(axis, coordinate, tuple(patch_rect))


def expected_endpoint_patch(
    axis: int,
    coordinate: Q,
    rect: tuple,
    endpoint: Q,
    depth: int,
) -> tuple[Q, ...]:
    assert axis == 2
    p_lower, p_upper = rect[1]
    assert endpoint in {p_lower, p_upper}
    inward_span = (
        p_upper - endpoint if endpoint == p_lower else endpoint - p_lower
    )
    assert inward_span > 0
    width = inward_span / (2**depth)
    p_interval = (
        (endpoint, endpoint + width)
        if endpoint == p_lower
        else (endpoint - width, endpoint)
    )
    return face_box(axis, coordinate, (rect[0], p_interval))


def verify_row(row_index: int):
    row = ROWS[row_index]
    candidate_index = row["candidate_index"]
    (
        leaf_a,
        leaf_b,
        expected_hash,
        chart,
        target,
        axis,
        coordinate,
        overlap,
    ) = r277.CAND[candidate_index]
    patch = parse_box(row["exact_positive_area_face_patch"])

    if not (
        patch[2 * axis] == patch[2 * axis + 1] == coordinate
    ):
        return ("FAIL_FACE_COORDINATE", None)
    tangent = 0
    tangential_area = Q(1)
    for current_axis in range(3):
        if current_axis == axis:
            continue
        lower, upper = overlap[tangent]
        patch_lower = patch[2 * current_axis]
        patch_upper = patch[2 * current_axis + 1]
        if not lower <= patch_lower < patch_upper <= upper:
            return ("FAIL_FACE_PATCH_AREA_OR_OVERLAP", None)
        tangential_area *= patch_upper - patch_lower
        tangent += 1
    if tangential_area <= 0:
        return ("FAIL_FACE_PATCH_AREA", None)
    if not (
        inside(patch, r277.BOX[leaf_a])
        and inside(patch, r277.BOX[leaf_b])
    ):
        return ("FAIL_FACE_PATCH_LEAF_CLOSURE", None)
    actual_hash, rejected = signature_hash(
        chart,
        target,
        patch,
        f"round277-audit-face:{candidate_index}",
    )
    if actual_hash != expected_hash:
        return ("FAIL_FACE_SIGNATURE", rejected)

    path = row["source_depth8_refinement_path"]
    source_rect = follow_path(overlap, path)
    source_values = face_box(axis, coordinate, source_rect)
    source_signature, source_reasons = signature_hash(
        chart,
        target,
        source_values,
        f"round277-audit-source-cell:{candidate_index}",
    )
    if source_signature is not None or source_reasons != (
        row["active_reason"],
    ):
        return ("FAIL_SOURCE_ACTIVE_CELL_IDENTITY", source_reasons)
    if row["active_reason"].startswith(
        "wall_endpoint_or_count_transition:"
    ):
        source_factor_sign = wall_source_factor_sign(
            chart,
            target,
            source_values,
            row["active_reason"],
        )
        if source_factor_sign not in {
            "STRICT_NEGATIVE",
            "STRICT_POSITIVE",
        }:
            return ("FAIL_WITNESS_SOURCE_FACTOR_NOT_STRICT", source_factor_sign)
    else:
        source_factor_sign = "NOT_APPLICABLE"

    classification = row["witness_classification"]
    if classification == "PASS_REGULAR_ACTIVE_SIDE_PATCH_AND_TWO_CORRIDORS":
        if row["seed_kind"] != "STRICT_ACTIVE_FACTOR_SIDE_EXTREMUM":
            return ("FAIL_REGULAR_SEED_KIND", None)
        seed = tuple(parse_fraction(value) for value in row["seed_point"])
        if len(seed) != 3:
            return ("FAIL_SEED_POINT", None)
        seed_hash, seed_rejected = signature_hash(
            chart,
            target,
            (
                seed[0],
                seed[0],
                seed[1],
                seed[1],
                seed[2],
                seed[2],
            ),
            f"round277-audit-seed:{candidate_index}",
        )
        if seed_hash != expected_hash:
            return ("FAIL_REGULAR_SEED_SIGNATURE", seed_rejected)
        seed_depth = row["dyadic_tangent_shrink_depth"]
        if not isinstance(seed_depth, int) or not 1 <= seed_depth <= 48:
            return ("FAIL_REGULAR_DEPTH", None)
        if patch != expected_regular_patch(
            axis, coordinate, source_rect, seed, seed_depth
        ):
            return ("FAIL_REGULAR_DYADIC_PATCH_RECONSTRUCTION", None)
        seed_family = "REGULAR"
    elif (
        classification
        == "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS"
    ):
        if (
            row["seed_kind"]
            != "STRICT_P_ENDPOINT_BOUNDARY_SEGMENT"
            or row["active_reason"] != "outgoing_chart_seam"
            or axis != 2
        ):
            return ("FAIL_ENDPOINT_SEED_IDENTITY", None)
        endpoint = parse_fraction(row["p_endpoint"])
        if endpoint not in {Q(-1), Q(1)}:
            return ("FAIL_ENDPOINT_VALUE", None)
        strict_t_interval = tuple(
            parse_fraction(value) for value in row["strict_t_interval"]
        )
        if strict_t_interval != source_rect[0]:
            return ("FAIL_ENDPOINT_LINE_INTERVAL", None)
        line_values = face_box(
            axis, coordinate, (strict_t_interval, (endpoint, endpoint))
        )
        line_hash, line_rejected = signature_hash(
            chart,
            target,
            line_values,
            f"round277-audit-endpoint-line:{candidate_index}",
        )
        if line_hash != expected_hash:
            return ("FAIL_ENDPOINT_LINE_SIGNATURE", line_rejected)
        seed_depth = row["dyadic_p_endpoint_inward_depth"]
        if not isinstance(seed_depth, int) or not 1 <= seed_depth <= 64:
            return ("FAIL_ENDPOINT_DEPTH", None)
        if patch != expected_endpoint_patch(
            axis, coordinate, source_rect, endpoint, seed_depth
        ):
            return ("FAIL_ENDPOINT_DYADIC_PATCH_RECONSTRUCTION", None)
        seed_family = "P_ENDPOINT"
    else:
        return ("FAIL_CLASSIFICATION", None)

    corridors = row["two_inward_corridors"]
    if len(corridors) != 2:
        return ("FAIL_CORRIDOR_COUNT", None)
    if {item["leaf_row_id"] for item in corridors} != {leaf_a, leaf_b}:
        return ("FAIL_CORRIDOR_LEAF_SET", None)
    side_census = collections.Counter()
    corridor_depths = []
    for item in corridors:
        leaf_id = item["leaf_row_id"]
        leaf = r277.BOX[leaf_id]
        corridor = parse_box(item["exact_corridor_box"])
        if not inside(corridor, leaf):
            return ("FAIL_CORRIDOR_CONTAINMENT", None)
        for current_axis in range(3):
            if current_axis != axis and corridor[
                2 * current_axis : 2 * current_axis + 2
            ] != patch[2 * current_axis : 2 * current_axis + 2]:
                return ("FAIL_CORRIDOR_TANGENTIAL_MISMATCH", None)
        negative = leaf[2 * axis + 1] == coordinate
        positive = leaf[2 * axis] == coordinate
        if negative == positive:
            return ("FAIL_CORRIDOR_FACE_ORIENTATION", None)
        expected_side = (
            "NEGATIVE_SIDE_INWARD"
            if negative
            else "POSITIVE_SIDE_INWARD"
        )
        if item["geometric_side"] != expected_side:
            return ("FAIL_CORRIDOR_SIDE_LABEL", None)
        depth = item["dyadic_normal_depth"]
        if not isinstance(depth, int) or not 1 <= depth <= 40:
            return ("FAIL_CORRIDOR_DEPTH", None)
        span = leaf[2 * axis + 1] - leaf[2 * axis]
        width = span / (2**depth)
        expected_normal = (
            (coordinate - width, coordinate)
            if negative
            else (coordinate, coordinate + width)
        )
        if corridor[2 * axis : 2 * axis + 2] != expected_normal:
            return ("FAIL_CORRIDOR_DYADIC_RECONSTRUCTION", None)
        if corridor[2 * axis] >= corridor[2 * axis + 1]:
            return ("FAIL_CORRIDOR_NORMAL_WIDTH", None)
        corridor_hash, corridor_rejected = signature_hash(
            chart,
            target,
            corridor,
            f"round277-audit-corridor:{candidate_index}:{leaf_id}",
        )
        if corridor_hash != expected_hash:
            return ("FAIL_CORRIDOR_SIGNATURE", corridor_rejected)
        side_census[expected_side] += 1
        corridor_depths.append(depth)
    if side_census != {
        "NEGATIVE_SIDE_INWARD": 1,
        "POSITIVE_SIDE_INWARD": 1,
    }:
        return ("FAIL_CORRIDOR_TWO_SIDEDNESS", None)
    return (
        "PASS",
        {
            "candidate_index": candidate_index,
            "seed_family": seed_family,
            "active_reason": row["active_reason"],
            "source_factor_sign": source_factor_sign,
            "tangent_or_endpoint_depth": seed_depth,
            "corridor_depths": corridor_depths,
        },
    )


def load() -> tuple[dict, dict, dict, dict, dict]:
    global ROWS
    cache_path = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache_path.exists():
        r277.CAND, r277.BOX, r277.TABLES = pickle.loads(
            cache_path.read_bytes()
        )
    else:
        r277.build()
    ledger = load_gzip(LEDGER)
    residual = load_gzip(RESIDUAL)
    tails = load_gzip(TAILS)
    strategy = json.loads(STRATEGY_RESULT.read_bytes())
    source_factor = json.loads(SOURCE_FACTOR_AUDIT.read_bytes())
    ROWS = ledger["rows"]
    return ledger, residual, tails, strategy, source_factor


def main() -> int:
    ctx.prec = 256
    ledger, residual, tails, strategy, source_factor = load()

    residual_indices = [row["candidate_index"] for row in residual["rows"]]
    ledger_indices = [row["candidate_index"] for row in ROWS]
    assert len(residual_indices) == len(set(residual_indices)) == 32_668
    assert ledger_indices == residual_indices == sorted(residual_indices)
    assert ledger["row_count"] == 32_668
    assert ledger["candidate_indices_sha256"] == r276.digest(ledger_indices)
    assert ledger["rows_sha256"] == r276.digest(ROWS)

    regular_indices = {
        row["candidate_index"]
        for row in ROWS
        if row["witness_classification"]
        == "PASS_REGULAR_ACTIVE_SIDE_PATCH_AND_TWO_CORRIDORS"
    }
    endpoint_indices = {
        row["candidate_index"]
        for row in ROWS
        if row["witness_classification"]
        == "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS"
    }
    tail_indices = {row["candidate_index"] for row in tails["rows"]}
    assert len(regular_indices) == 32_416
    assert len(endpoint_indices) == len(tail_indices) == 252
    assert endpoint_indices == tail_indices
    assert regular_indices.isdisjoint(endpoint_indices)
    assert regular_indices | endpoint_indices == set(residual_indices)
    assert strategy["candidate_disposition_census"] == {
        "EXACT_POSITIVE_MATCH_SIDE_FOUND": 32_416,
        "FAILCLOSED_ACTIVE_GRAPH_TAIL": 252,
    }
    assert (
        source_factor[
            "source_and_hit_factors_both_active_terminal_cell_count"
        ]
        == 256
        and source_factor[
            "candidate_groups_containing_source_factor_overwrap"
        ]
        == 64
    )

    status_census = collections.Counter()
    seed_census = collections.Counter()
    reason_census = collections.Counter()
    source_factor_census = collections.Counter()
    corridor_depths = collections.Counter()
    with mp.get_context("fork").Pool(min(40, mp.cpu_count())) as pool:
        for status, detail in pool.imap_unordered(
            verify_row, range(len(ROWS)), chunksize=16
        ):
            status_census[status] += 1
            if status == "PASS":
                seed_census[detail["seed_family"]] += 1
                reason_census[detail["active_reason"]] += 1
                source_factor_census[detail["source_factor_sign"]] += 1
                corridor_depths.update(detail["corridor_depths"])

    assert status_census == {"PASS": 32_668}, status_census
    assert seed_census == {"REGULAR": 32_416, "P_ENDPOINT": 252}

    result = {
        "status": (
            "PASS_INDEPENDENT_ROUND277_DEPTH8_ACTIVE_GRAPH_FACE_EDGE_"
            "WITNESS_AUDIT__ZERO_CREDIT"
        ),
        "candidate_partition": {
            "source_depth8_residual_count": len(residual_indices),
            "regular_active_side_witness_count": len(regular_indices),
            "p_endpoint_wedge_witness_count": len(endpoint_indices),
            "endpoint_indices_exactly_equal_prior_failclosed_tail_indices": True,
            "partition_duplicate_free_disjoint_and_exhaustive": True,
        },
        "rowwise_verification_histogram": dict(sorted(status_census.items())),
        "seed_family_histogram": dict(sorted(seed_census.items())),
        "active_reason_histogram": dict(sorted(reason_census.items())),
        "witness_source_factor_sign_histogram": dict(
            sorted(source_factor_census.items())
        ),
        "verified_positive_area_face_patch_count": len(ROWS),
        "verified_positive_volume_inward_corridor_count": 2 * len(ROWS),
        "normal_corridor_depth_histogram": dict(
            sorted(corridor_depths.items())
        ),
        "double_active_cell_audit": {
            "source_and_hit_factors_both_active_terminal_cell_count": 256,
            "affected_candidate_group_count": 64,
            "strategy_disposition": "RETAINED_FAIL_CLOSED_AT_CELL_LEVEL",
            "used_as_absence_certificate_count": 0,
            "used_as_witness_seed_count": 0,
            "affected_groups_have_separate_strict_positive_patch_witnesses": 64,
        },
        "false_positive_verdict": (
            "NONE_FOUND_IN_32668_EXPLICIT_WITNESS_ROWS"
        ),
        "false_negative_verdict": (
            "NONE_REMAINING_IN_FROZEN_32668_DEPTH8_RESIDUAL_CANDIDATES"
        ),
        "scope_distinction": {
            "active_side_strategy_probe": (
                "STRICT EXTREMAL SIDE EXISTENCE ONLY; NO EDGE CREDIT"
            ),
            "materialized_witness_ledger": (
                "EXACT POSITIVE-AREA FACE PATCH PLUS TWO EXACT "
                "POSITIVE-VOLUME INWARD CORRIDORS"
            ),
            "global_claim": (
                "OCCURRENCE MATERIALIZATION, DSU UNION, SEAM BINDING, "
                "MAXIMALITY, FIBRES, AND DISPOSITIONS REMAIN UNPROVED"
            ),
        },
        "witness_rows_sha256": ledger["rows_sha256"],
        "witness_ledger_file_sha256": hashlib.sha256(
            LEDGER.read_bytes()
        ).hexdigest(),
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "rank_reduction_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
