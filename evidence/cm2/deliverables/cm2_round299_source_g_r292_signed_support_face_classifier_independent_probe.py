#!/usr/bin/env python3
"""Independent signed-support classifier for all Round292 box faces.

This zero-credit spike reconstructs the 11,852 exact Round292 refinement
cells, binds each cell to its formal Round294 occurrence endpoint, and
independently enumerates the 43,092 same-chart, same-physical-t-sign,
positive-area coordinate-face contacts.

Coordinate contact is not accepted by itself.  The classifier applies the
frozen Round287 signed-support semantics:

* FULL/FULL contacts receive an exact positive-area inner face patch and
  strict positive-volume corridors on both sides;
* a single active-graph constraint is replayed on the face and corridor;
* two graph constraints are split into same-factor/same-side,
  same-factor/opposite-side, and different-factor cases;
* accepted rows carry a strict patch and two corridors;
* rejected rows carry either an exact empty-face extrema certificate or the
  exact incompatibility ``{f > 0} intersect {f < 0} = empty``;
* any case lacking one of those certificates remains unresolved and makes
  the diagnostic fail closed.

This file does not import the parallel Round299 frontier producer and grants
no occurrence, component, rank, maximality, fibre, or disposition credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
from math import isqrt
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Iterable

from flint import ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274


PREFIX = (
    "cm2_round299_source_g_r292_signed_support_face_classifier_"
    "independent_probe"
)
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R174_PY = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization.py"
)
R179_PY = "cm2_round179_source_g_residual_tube_arrangement.py"
R274_PY = "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
R275 = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R287_PY = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe.py"
)
R287 = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "ledger.json.gz"
)
R292 = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "ledger.json.gz"
)
R294 = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_"
    "closure_physical_witness_incidence_binding_ledger.json.gz"
)
R296 = (
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
    "edge_ledger.json.gz"
)
R297 = (
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
    "edge_ledger.json.gz"
)

PINS = {
    R174_PY:
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R179_PY:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R274_PY:
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287_PY:
        "b39849e3aee21688ccf3eb5443984e9e0e8d7a88ed2d61e059ed3485d84c780d",
    R287:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R292:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R295A:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296:
        "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297:
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

SCHEMA = (
    "cm2.round299.source-g-r292-signed-support-face-classifier-"
    "independent-probe.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)

UNCOVERED_DISPOSITION = (
    "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
    "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
)
OCCUPIED_DISPOSITION = (
    "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__"
    "NO_NEW_OCCURRENCE_ID"
)
GRAPH = "REGULAR_GRAPH_CROSSING"
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
MAX_FACE_DEPTH = 32
MAX_CORRIDOR_DEPTH = 32
SQRT_CONSTRUCTION_BITS = 256
SQRT_REPLAY_BITS = 512
ARB_PRECISION_BITS = 512


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            state.update(chunk)
    return state.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_json(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], "pin:" + name)
    return json.loads(path.read_bytes())


def read_gzip(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], "pin:" + name)
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def verify_table(
    document: dict[str, Any],
    rows_key: str,
    count_key: str,
    digest_key: str,
) -> list[dict[str, Any]]:
    rows = document[rows_key]
    need(len(rows) == document[count_key], rows_key + ":count")
    need(digest(rows) == document[digest_key], rows_key + ":digest")
    return rows


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(row.get("row_sha256") == digest(payload), label + ":row_sha256")


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "row already closed")
    row = dict(payload)
    row["row_sha256"] = digest(row)
    return row


def qbox(values: Iterable[str]) -> tuple[Q, ...]:
    result = tuple(map(Q, values))
    need(
        len(result) == 6
        and all(
            result[2 * axis] < result[2 * axis + 1]
            for axis in range(3)
        ),
        "positive exact box",
    )
    return result


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else str(value)
    )


def qlist(values: Iterable[Q]) -> list[str]:
    return [qstr(value) for value in values]


def rational_square_root(value: Q) -> Q | None:
    need(value >= 0, "nonnegative square requested")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if (
        numerator * numerator == value.numerator
        and denominator * denominator == value.denominator
    ):
        return Q(numerator, denominator)
    return None


def sqrt_dyadic_bounds(value: Q, bits: int) -> tuple[Q, Q]:
    """Exact rational enclosure copied from the frozen Round273 method."""
    need(value >= 0 and bits > 0, "sqrt dyadic domain")
    scale = 1 << bits
    scaled_square_numerator = value.numerator * scale * scale
    quotient = scaled_square_numerator // value.denominator
    k = isqrt(quotient)
    while (
        (k + 1) * (k + 1) * value.denominator
        <= scaled_square_numerator
    ):
        k += 1
    while k * k * value.denominator > scaled_square_numerator:
        k -= 1
    lower = Q(k, scale)
    exact = (
        k * k * value.denominator == scaled_square_numerator
    )
    upper = lower if exact else Q(k + 1, scale)
    need(
        lower >= 0
        and lower * lower <= value <= upper * upper
        and (
            lower == upper
            or lower * lower < value < upper * upper
        ),
        "strict exact sqrt dyadic enclosure",
    )
    return lower, upper


def sqrt_enclosure_certificate(value: Q, bits: int) -> dict[str, Any]:
    lower, upper = sqrt_dyadic_bounds(value, bits)
    exact = rational_square_root(value)
    need(
        lower >= 0
        and lower * lower <= value <= upper * upper
        and (
            exact is not None
            or lower * lower < value < upper * upper
        ),
        "sqrt enclosure certificate inequalities",
    )
    payload = {
        "t_square": qstr(value),
        "sqrt_enclosure_bits": bits,
        "sqrt_lower": qstr(lower),
        "sqrt_upper": qstr(upper),
        "lower_square_le_t_square": True,
        "t_square_le_upper_square": True,
        "strict_when_not_rational_square": exact is None,
        "exact_rational_sqrt": None if exact is None else qstr(exact),
    }
    payload["certificate_sha256"] = digest(payload)
    return payload


def strict_rational_square_between(
    lower_square: Q,
    upper_square: Q,
) -> Q:
    """Choose rational t strictly between two algebraic sqrt endpoints."""
    need(
        0 <= lower_square < upper_square,
        "strict transformed interval for rational interior point",
    )
    bits = SQRT_CONSTRUCTION_BITS
    while True:
        lower_upper = sqrt_dyadic_bounds(lower_square, bits)[1]
        upper_lower = sqrt_dyadic_bounds(upper_square, bits)[0]
        if lower_upper < upper_lower:
            point = (lower_upper + upper_lower) / 2
            break
        bits *= 2
        need(bits <= 4_096, "sqrt enclosures did not separate")
    result = point * point
    need(
        lower_square < result < upper_square
        and rational_square_root(result) == point,
        "strict rational square interior point",
    )
    return result


def transformed_to_signed_physical_outer(
    box: tuple[Q, ...],
    physical_t_sign: int,
) -> tuple[tuple[Q, ...], list[dict[str, Any]]]:
    """Return a rational box containing the exact algebraic physical t box."""
    need(physical_t_sign in {-1, 1}, "physical t sign")
    lower_certificate = sqrt_enclosure_certificate(
        box[0], SQRT_REPLAY_BITS
    )
    upper_certificate = sqrt_enclosure_certificate(
        box[1], SQRT_REPLAY_BITS
    )
    lower_sqrt = Q(lower_certificate["sqrt_lower"])
    upper_sqrt = Q(upper_certificate["sqrt_upper"])
    if physical_t_sign > 0:
        t_lo, t_hi = lower_sqrt, upper_sqrt
    else:
        t_lo, t_hi = -upper_sqrt, -lower_sqrt
    result = (t_lo, t_hi, *box[2:])
    need(
        all(
            result[2 * axis] <= result[2 * axis + 1]
            for axis in range(3)
        ),
        "ordered outer signed physical box",
    )
    return result, [lower_certificate, upper_certificate]


def validate_transformed_t_boundaries(box: tuple[Q, ...]) -> None:
    for value in box[:2]:
        certificate = sqrt_enclosure_certificate(
            value, SQRT_CONSTRUCTION_BITS
        )
        need(
            Q(certificate["sqrt_lower"]) ** 2 <= value
            <= Q(certificate["sqrt_upper"]) ** 2,
            "transformed t boundary sqrt enclosure",
        )


def transformed_t_boundary_certificates(
    box: tuple[Q, ...],
) -> list[dict[str, Any]]:
    certificates = [
        sqrt_enclosure_certificate(value, SQRT_REPLAY_BITS)
        for value in box[:2]
    ]
    need(
        all(
            Q(item["sqrt_lower"]) ** 2
            <= Q(item["t_square"])
            <= Q(item["sqrt_upper"]) ** 2
            for item in certificates
        ),
        "transformed t certificate inequalities",
    )
    return certificates


def face_area(face: tuple[Q, ...], axis: int) -> Q:
    widths = [
        face[2 * other + 1] - face[2 * other]
        for other in range(3)
        if other != axis
    ]
    need(len(widths) == 2 and all(width > 0 for width in widths), "face area")
    return widths[0] * widths[1]


def volume(box: tuple[Q, ...]) -> Q:
    result = Q(1)
    for axis in range(3):
        width = box[2 * axis + 1] - box[2 * axis]
        need(width > 0, "positive corridor volume")
        result *= width
    return result


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself pair")
    return tuple(sorted((left, right)))


def load_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(
        wrapper["result_sha256"] == digest(wrapper["result"]),
        "R275 result digest",
    )
    result = wrapper["result"]
    rows = [
        row
        for table_name in ("strict_region_ledger", "arrangement_region_ledger")
        for row in verify_table(
            result[table_name], "rows", "row_count", "rows_sha256"
        )
    ]
    need(len(rows) == 13_788, "R275 region census")
    by_id = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(by_id) == len(rows), "R275 region ID injectivity")
    return by_id


def load_r287() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    document = read_gzip(R287)
    region_rows = verify_table(
        document, "region_rows", "region_row_count", "region_rows_sha256"
    )
    cell_rows = verify_table(
        document,
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
    )
    need(
        len(region_rows) == 13_788 and len(cell_rows) == 7_616,
        "R287 census",
    )
    return (
        {row["Round275_region_id"]: row for row in region_rows},
        {row["Round286_refinement_cell_id"]: row for row in cell_rows},
    )


def load_refined_occurrence_map() -> dict[str, str]:
    document = read_gzip(R294)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    need(len(rows) == 431_208, "R294 registry census")
    result = {
        row["source_row_id"]: row["registry_occurrence_id"]
        for row in rows
        if row["registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(
        len(result) == 9_404
        and len(set(result.values())) == len(result),
        "R294 refined occurrence mapping",
    )
    del document, rows
    gc.collect()
    return result


def inherited_support_mode(
    source_cell_id: str,
    region_id: str,
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
) -> str:
    if source_cell_id.startswith("WHOLE:"):
        need(source_cell_id == "WHOLE:" + region_id, "whole source cell")
        if regions[region_id].get("arrangement_classification") == GRAPH:
            return "ACTIVE_GRAPH_CONSTRAINED"
        need(
            r287_regions[region_id]["R275_region_kind"]
            in {"WHOLE_STRICT_SIGNATURE_CELL", "ZERO_SET_ABSENT"},
            "known whole support kind",
        )
        return "FULL_SIGNED_SUPPORT"

    source = r287_cells[source_cell_id]
    need(source["Round275_region_id"] == region_id, "R287 cell region")
    state = source["signed_region_cell_state"]
    if state == "FULL_DESIRED_SIDE_SUPPORT":
        return "FULL_SIGNED_SUPPORT"
    need(
        state == "CLIPPED_DESIRED_SIDE_SUPPORT"
        and regions[region_id].get("arrangement_classification") == GRAPH,
        "known graph-constrained refinement cell",
    )
    return "ACTIVE_GRAPH_CONSTRAINED"


def factor_descriptor(region: dict[str, Any]) -> dict[str, Any]:
    need(region.get("arrangement_classification") == GRAPH, "graph region")
    reason = region["active_reason"]
    if reason == "outgoing_chart_seam":
        expression = (
            "interval_geometry(adjacent_chart,owner_target)."
            "outgoing_equality[0]"
        )
    else:
        kind, axis, wall = reason.split(":")
        need(
            kind == "wall_endpoint_or_count_transition"
            and axis in {"X", "Y"},
            "known active wall factor",
        )
        expression = (
            "interval_geometry(adjacent_chart,owner_target)."
            + ("hit_x[0]" if axis == "X" else "hit_y[0]")
            + f"-arb({int(wall)})"
        )
    active_function_payload = {
        "adjacent_chart": region["adjacent_chart"],
        "owner_target": region["owner_target"],
        "active_reason": reason,
        "active_function_expression": expression,
        "active_function_evaluator_module_sha256": PINS[R274_PY],
        "interval_geometry_module_sha256": PINS[R179_PY],
    }
    provenance_payload = {
        "source_chart": region["source_chart"],
        "source_guard_row_id": region["source_guard_row_id"],
        "parent_id": region["parent_id"],
        "exact_coordinate_identity": region["exact_coordinate_identity"],
        "adjacent_cover_refinement_path":
            region["adjacent_cover_refinement_path"],
    }
    active_function_id = (
        "round299-active-function:" + digest(active_function_payload)
    )
    return {
        "active_function_id": active_function_id,
        "factor_id": active_function_id,
        "active_function_identity_payload": active_function_payload,
        "provenance_descriptor": provenance_payload,
        "source_chart": region["source_chart"],
        "adjacent_chart": region["adjacent_chart"],
        "owner_target": region["owner_target"],
        "active_reason": reason,
        "source_guard_row_id": region["source_guard_row_id"],
        "parent_id": region["parent_id"],
        "exact_coordinate_identity": region["exact_coordinate_identity"],
        "active_function_expression": expression,
        "desired_side_sign": region["active_factor_side_sign"],
        "strict_derivative_signs_t_p_s":
            region["strict_derivative_signs_t_p_s"],
    }


def load_cells(
    regions: dict[str, dict[str, Any]],
    r287_regions: dict[str, dict[str, Any]],
    r287_cells: dict[str, dict[str, Any]],
    refined_occurrence_map: dict[str, str],
) -> list[dict[str, Any]]:
    document = read_gzip(R292)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result = []
    for source in rows:
        disposition = source.get("disposition")
        if disposition not in {
            UNCOVERED_DISPOSITION,
            OCCUPIED_DISPOSITION,
        }:
            continue
        verify_closed_row(source, "R292 refinement")
        region_id = source["Round275_region_id"]
        source_cell_id = source["source_Round287_support_cell_id"]
        region = regions[region_id]
        physical_t_sign = r287_regions[region_id]["physical_t_sign"]
        need(physical_t_sign in {-1, 1}, "R287 physical t sign")
        support_mode = inherited_support_mode(
            source_cell_id,
            region_id,
            regions,
            r287_regions,
            r287_cells,
        )
        component_id = source["Round292_refined_new_support_component_id"]
        if disposition == UNCOVERED_DISPOSITION:
            need(
                source["existing_occurrence_ids"] == []
                and component_id in refined_occurrence_map,
                "uncovered refined occurrence endpoint",
            )
            endpoint_kind = "U"
            endpoint = refined_occurrence_map[component_id]
        else:
            need(
                source["existing_occurrence_occupancy_count"] == 1
                and len(source["existing_occurrence_ids"]) == 1
                and component_id is None,
                "occupied existing occurrence endpoint",
            )
            endpoint_kind = "O"
            endpoint = source["existing_occurrence_ids"][0]
        box = qbox(source["exact_transformed_open_cell"])
        validate_transformed_t_boundaries(box)
        need(
            source["source_chart"] == region["adjacent_chart"],
            "R292 transformed chart equals R275 adjacent chart",
        )
        result.append({
            "cell_id":
                source["Round292_R287_existing_overlap_refinement_cell_id"],
            "source_cell_id": source_cell_id,
            "support_union_id":
                source["Round287_potential_new_support_union_id"],
            "region_id": region_id,
            "source_chart": source["source_chart"],
            "physical_t_sign": physical_t_sign,
            "box": box,
            "endpoint_kind": endpoint_kind,
            "endpoint_occurrence_id": endpoint,
            "refined_component_id": component_id,
            "support_mode": support_mode,
            "factor": (
                factor_descriptor(region)
                if support_mode == "ACTIVE_GRAPH_CONSTRAINED"
                else None
            ),
        })
    del document, rows
    gc.collect()
    result.sort(key=lambda row: row["cell_id"])
    need(
        len(result) == 11_852
        and Counter(row["endpoint_kind"] for row in result)
        == {"U": 10_252, "O": 1_600}
        and len({row["cell_id"] for row in result}) == len(result),
        "R292 cell reconstruction census",
    )
    return result


def common_face(
    left: tuple[Q, ...],
    right: tuple[Q, ...],
    axis: int,
) -> tuple[Q, ...] | None:
    if left[2 * axis + 1] != right[2 * axis]:
        return None
    values = []
    for current in range(3):
        if current == axis:
            coordinate = left[2 * current + 1]
            values.extend((coordinate, coordinate))
        else:
            lower = max(left[2 * current], right[2 * current])
            upper = min(left[2 * current + 1], right[2 * current + 1])
            if not lower < upper:
                return None
            values.extend((lower, upper))
    return tuple(values)


def pair_kind(left: dict[str, Any], right: dict[str, Any]) -> str:
    return "".join(sorted((left["endpoint_kind"], right["endpoint_kind"])))


def contact_class(
    left: dict[str, Any],
    right: dict[str, Any],
) -> str:
    graphs = [
        row for row in (left, right)
        if row["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED"
    ]
    if not graphs:
        return "FULL_FULL"
    if len(graphs) == 1:
        return "SINGLE_GRAPH"
    left_factor = left["factor"]
    right_factor = right["factor"]
    if (
        left_factor["active_function_id"]
        != right_factor["active_function_id"]
    ):
        return "DOUBLE_GRAPH_DIFFERENT_FACTOR"
    if (
        left_factor["desired_side_sign"]
        == right_factor["desired_side_sign"]
    ):
        return "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE"
    return "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE"


def active_factor_replay(
    region_id: str,
    transformed_box: tuple[Q, ...],
    physical_t_sign: int,
    regions: dict[str, dict[str, Any]],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    key = (region_id, transformed_box, physical_t_sign)
    if key in cache:
        return cache[key]
    region = regions[region_id]
    need(region.get("arrangement_classification") == GRAPH, "factor replay graph")
    physical_box, sqrt_certificates = transformed_to_signed_physical_outer(
        transformed_box, physical_t_sign
    )
    atlas_box = r174.atlas.AtlasBox(
        *physical_box, "round299-independent-face-classifier", None
    )
    signs = []
    for want_maximum in (False, True):
        point = r274.extremal_point(
            atlas_box,
            region["strict_derivative_signs_t_p_s"],
            want_maximum,
        )
        active_value = r274.active_dual(
            r179.interval_geometry(
                region["adjacent_chart"],
                region["owner_target"],
                point,
            ),
            region["active_reason"],
        )[0]
        signs.append(r179.sign(active_value))
    descriptor = factor_descriptor(region)
    if not set(signs) <= STRICT_SIGNS:
        support_state = "UNRESOLVED_ACTIVE_FACTOR_OVERWRAP"
        raw_state = "ACTIVE_FACTOR_INTERVAL_OVERWRAP"
    elif signs[0] != signs[1]:
        support_state = "CLIPPED_DESIRED_SIDE_SUPPORT"
        raw_state = "ACTIVE_FACTOR_STRICT_SIGN_CHANGE"
    elif signs[0] == region["active_factor_side_sign"]:
        support_state = "FULL_DESIRED_SIDE_SUPPORT"
        raw_state = signs[0]
    else:
        support_state = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
        raw_state = signs[0]
    result = {
        "region_id": region_id,
        "active_function_id": descriptor["active_function_id"],
        "factor_id": descriptor["factor_id"],
        "desired_side_sign": region["active_factor_side_sign"],
        "active_factor_extremal_signs": signs,
        "active_factor_raw_state": raw_state,
        "signed_support_state": support_state,
        "outer_rational_signed_physical_box": qlist(physical_box),
        "outer_box_contains_exact_algebraic_sqrt_boundaries": True,
        "t_boundary_sqrt_enclosure_certificates": sqrt_certificates,
        "t_boundary_sqrt_enclosures_sha256":
            digest(sqrt_certificates),
    }
    cache[key] = result
    return result


def split_face(
    face: tuple[Q, ...],
    axis: int,
    physical_t_sign: int,
) -> list[tuple[Q, ...]]:
    need(physical_t_sign in {-1, 1}, "split physical t sign")
    tangent_axes = [current for current in range(3) if current != axis]
    result = []
    for first_half in (0, 1):
        for second_half in (0, 1):
            halves = dict(zip(tangent_axes, (first_half, second_half), strict=True))
            values = []
            for current in range(3):
                lower, upper = face[2 * current:2 * current + 2]
                if current == axis:
                    values.extend((lower, upper))
                    continue
                middle = (
                    strict_rational_square_between(lower, upper)
                    if current == 0
                    else (lower + upper) / 2
                )
                values.extend(
                    (lower, middle)
                    if halves[current] == 0
                    else (middle, upper)
                )
            child = tuple(values)
            validate_transformed_t_boundaries(child)
            result.append(child)
    return result


def inset_face(
    face: tuple[Q, ...],
    axis: int,
    physical_t_sign: int,
) -> tuple[Q, ...]:
    need(physical_t_sign in {-1, 1}, "inset physical t sign")
    values = []
    for current in range(3):
        lower, upper = face[2 * current:2 * current + 2]
        if current == axis:
            values.extend((lower, upper))
            continue
        width = upper - lower
        need(width > 0, "positive tangent width")
        if current == 0:
            middle = strict_rational_square_between(lower, upper)
            values.extend((
                strict_rational_square_between(lower, middle),
                strict_rational_square_between(middle, upper),
            ))
        else:
            values.extend((lower + width / 4, upper - width / 4))
    result = tuple(values)
    validate_transformed_t_boundaries(result)
    need(face_area(result, axis) > 0, "positive inset face patch")
    return result


def targeted_tangent_interval(
    lower: Q,
    upper: Q,
    *,
    direction: str,
    depth: int,
    transformed_t_axis: bool,
) -> tuple[Q, Q]:
    need(
        lower < upper
        and direction in {"LOWER", "UPPER", "CENTER"}
        and depth > 0,
        "targeted tangent interval inputs",
    )
    if not transformed_t_axis:
        width = upper - lower
        divisor = 1 << depth
        if direction == "LOWER":
            outer_lower = lower
            outer_upper = lower + width / divisor
        elif direction == "UPPER":
            outer_lower = upper - width / divisor
            outer_upper = upper
        else:
            middle = (lower + upper) / 2
            radius = width / (1 << (depth + 2))
            outer_lower, outer_upper = middle - radius, middle + radius
        outer_width = outer_upper - outer_lower
        result = (
            outer_lower + outer_width / 4,
            outer_upper - outer_width / 4,
        )
        need(lower < result[0] < result[1] < upper, "strict rational patch")
        return result

    outer_lower, outer_upper = lower, upper
    for _ in range(depth):
        middle = strict_rational_square_between(
            outer_lower, outer_upper
        )
        if direction == "LOWER":
            outer_upper = middle
        elif direction == "UPPER":
            outer_lower = middle
        else:
            outer_lower = strict_rational_square_between(
                outer_lower, middle
            )
            outer_upper = strict_rational_square_between(
                middle, outer_upper
            )
    middle = strict_rational_square_between(outer_lower, outer_upper)
    result = (
        strict_rational_square_between(outer_lower, middle),
        strict_rational_square_between(middle, outer_upper),
    )
    need(
        lower < result[0] < result[1] < upper
        and rational_square_root(result[0]) is not None
        and rational_square_root(result[1]) is not None,
        "strict physical-t-derived transformed patch",
    )
    return result


def targeted_face_patch(
    face: tuple[Q, ...],
    axis: int,
    seed_cell: dict[str, Any],
    regions: dict[str, dict[str, Any]],
    depth: int,
) -> tuple[Q, ...]:
    region = regions[seed_cell["region_id"]]
    desired = region["active_factor_side_sign"]
    derivatives = region["strict_derivative_signs_t_p_s"]
    values = []
    for current in range(3):
        lower, upper = face[2 * current:2 * current + 2]
        if current == axis:
            values.extend((lower, upper))
            continue
        derivative = derivatives[current]
        if derivative not in STRICT_SIGNS:
            direction = "CENTER"
        else:
            prefer_higher_physical_coordinate = (
                (desired == "STRICT_POSITIVE")
                == (derivative == "STRICT_POSITIVE")
            )
            if current == 0 and seed_cell["physical_t_sign"] < 0:
                prefer_higher_transformed_coordinate = (
                    not prefer_higher_physical_coordinate
                )
            else:
                prefer_higher_transformed_coordinate = (
                    prefer_higher_physical_coordinate
                )
            direction = (
                "UPPER" if prefer_higher_transformed_coordinate else "LOWER"
            )
        interval = targeted_tangent_interval(
            lower,
            upper,
            direction=direction,
            depth=depth,
            transformed_t_axis=current == 0,
        )
        values.extend(interval)
    result = tuple(values)
    validate_transformed_t_boundaries(result)
    need(face_area(result, axis) > 0, "targeted positive face patch")
    return result


def face_patch_search(
    face: tuple[Q, ...],
    axis: int,
    graph_cells: list[dict[str, Any]],
    regions: dict[str, dict[str, Any]],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    need(graph_cells, "graph-constrained face search")
    physical_t_sign = graph_cells[0]["physical_t_sign"]
    need(
        all(
            cell["physical_t_sign"] == physical_t_sign
            for cell in graph_cells
        ),
        "face search one physical t sign",
    )
    initial_replays = [
        active_factor_replay(
            cell["region_id"],
            face,
            cell["physical_t_sign"],
            regions,
            cache,
        )
        for cell in graph_cells
    ]
    if all(
        replay["signed_support_state"] == "FULL_DESIRED_SIDE_SUPPORT"
        for replay in initial_replays
    ):
        patch = inset_face(face, axis, physical_t_sign)
        patch_replays = [
            active_factor_replay(
                cell["region_id"],
                patch,
                cell["physical_t_sign"],
                regions,
                cache,
            )
            for cell in graph_cells
        ]
        need(
            all(
                replay["signed_support_state"]
                == "FULL_DESIRED_SIDE_SUPPORT"
                for replay in patch_replays
            ),
            "inset full face remains full desired support",
        )
        return {
            "status": "ACCEPT_STRICT_DYADIC_POSITIVE_AREA_FACE_PATCH",
            "face_refinement_depth": 0,
            "patch": patch,
            "initial_face_replays": initial_replays,
            "patch_replays": patch_replays,
            "targeted_patch_trace": [],
            "targeted_patch_trace_sha256": digest([]),
            "exclusion_cover_cell_count": 0,
            "exclusion_cover_sha256": digest([]),
        }

    empty = [
        replay
        for replay in initial_replays
        if replay["signed_support_state"]
        == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"
    ]
    if empty:
        exclusion = [{
            "exact_face": qlist(face),
            "empty_region_ids":
                sorted(replay["region_id"] for replay in empty),
            "strict_opposite_extremal_signs": [
                replay["active_factor_extremal_signs"]
                for replay in empty
            ],
        }]
        return {
            "status": "REJECT_EXACT_WHOLE_FACE_EMPTY_SUPPORT_EXTREMA",
            "face_refinement_depth": 0,
            "patch": None,
            "initial_face_replays": initial_replays,
            "patch_replays": [],
            "targeted_patch_trace": [],
            "targeted_patch_trace_sha256": digest([]),
            "exclusion_cover_cell_count": 1,
            "exclusion_cover_sha256": digest(exclusion),
        }

    trace = []
    for depth in range(1, MAX_FACE_DEPTH + 1):
        for seed_cell in graph_cells:
            candidate = targeted_face_patch(
                face, axis, seed_cell, regions, depth
            )
            replays = [
                active_factor_replay(
                    cell["region_id"],
                    candidate,
                    cell["physical_t_sign"],
                    regions,
                    cache,
                )
                for cell in graph_cells
            ]
            trace.append({
                "face_refinement_depth": depth,
                "seed_region_id": seed_cell["region_id"],
                "candidate_patch_sha256": digest(qlist(candidate)),
                "candidate_t_boundary_sqrt_enclosures_sha256": digest(
                    transformed_t_boundary_certificates(candidate)
                ),
                "signed_support_states": [
                    replay["signed_support_state"] for replay in replays
                ],
                "active_factor_extremal_signs": [
                    replay["active_factor_extremal_signs"]
                    for replay in replays
                ],
            })
            if all(
                replay["signed_support_state"]
                == "FULL_DESIRED_SIDE_SUPPORT"
                for replay in replays
            ):
                return {
                    "status":
                        "ACCEPT_TARGETED_MONOTONE_STRICT_FACE_PATCH",
                    "face_refinement_depth": depth,
                    "patch": candidate,
                    "initial_face_replays": initial_replays,
                    "patch_replays": replays,
                    "targeted_patch_trace": trace,
                    "targeted_patch_trace_sha256": digest(trace),
                    "exclusion_cover_cell_count": 0,
                    "exclusion_cover_sha256": digest([]),
                }
    return {
        "status": "UNRESOLVED_TARGETED_MONOTONE_FACE_DEPTH_EXHAUSTED",
        "face_refinement_depth": MAX_FACE_DEPTH,
        "patch": None,
        "initial_face_replays": initial_replays,
        "patch_replays": [],
        "targeted_patch_trace": trace,
        "targeted_patch_trace_sha256": digest(trace),
        "exclusion_cover_cell_count": 0,
        "exclusion_cover_sha256": digest([]),
        "remaining_mixed_face_cell_count": len(trace),
        "remaining_mixed_face_cells_sha256": digest(trace),
    }


def corridor_candidate(
    cell: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    is_left: bool,
    depth: int,
) -> tuple[Q, ...]:
    box = cell["box"]
    coordinate = patch[2 * axis]
    need(
        patch[2 * axis] == patch[2 * axis + 1],
        "degenerate patch normal coordinate",
    )
    values = list(patch)
    divisor = 1 << depth
    if is_left:
        need(box[2 * axis + 1] == coordinate, "left cell face")
        if axis == 0:
            lower = box[2 * axis]
            for _ in range(depth):
                lower = strict_rational_square_between(lower, coordinate)
        else:
            lower = coordinate - (coordinate - box[2 * axis]) / divisor
        values[2 * axis:2 * axis + 2] = [lower, coordinate]
    else:
        need(box[2 * axis] == coordinate, "right cell face")
        if axis == 0:
            upper = box[2 * axis + 1]
            for _ in range(depth):
                upper = strict_rational_square_between(coordinate, upper)
        else:
            upper = coordinate + (box[2 * axis + 1] - coordinate) / divisor
        values[2 * axis:2 * axis + 2] = [coordinate, upper]
    result = tuple(values)
    validate_transformed_t_boundaries(result)
    need(volume(result) > 0, "positive strict corridor")
    return result


def certify_corridor(
    cell: dict[str, Any],
    patch: tuple[Q, ...],
    axis: int,
    is_left: bool,
    regions: dict[str, dict[str, Any]],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any] | None:
    if cell["support_mode"] == "FULL_SIGNED_SUPPORT":
        box = corridor_candidate(cell, patch, axis, is_left, 1)
        certificates = transformed_t_boundary_certificates(box)
        trace = [{
            "corridor_depth": 1,
            "transformed_corridor_sha256": digest(qlist(box)),
            "signed_support_state": "INHERITED_FULL_SIGNED_SUPPORT",
            "t_boundary_sqrt_enclosures_sha256": digest(certificates),
        }]
        return {
            "corridor_depth": 1,
            "exact_positive_volume_transformed_corridor": qlist(box),
            "exact_transformed_corridor_volume": qstr(volume(box)),
            "t_boundary_sqrt_enclosure_certificates": certificates,
            "t_boundary_sqrt_enclosures_sha256": digest(certificates),
            "dyadic_inward_shrink_trace": trace,
            "dyadic_inward_shrink_trace_sha256": digest(trace),
            "signed_support_replay": None,
            "support_basis": "INHERITED_R287_FULL_SIGNED_SUPPORT",
        }
    trace = []
    for depth in range(1, MAX_CORRIDOR_DEPTH + 1):
        box = corridor_candidate(cell, patch, axis, is_left, depth)
        certificates = transformed_t_boundary_certificates(box)
        replay = active_factor_replay(
            cell["region_id"],
            box,
            cell["physical_t_sign"],
            regions,
            cache,
        )
        trace.append({
            "corridor_depth": depth,
            "transformed_corridor_sha256": digest(qlist(box)),
            "signed_support_state": replay["signed_support_state"],
            "active_factor_extremal_signs":
                replay["active_factor_extremal_signs"],
            "t_boundary_sqrt_enclosures_sha256": digest(certificates),
        })
        if (
            replay["signed_support_state"]
            == "FULL_DESIRED_SIDE_SUPPORT"
        ):
            return {
                "corridor_depth": depth,
                "exact_positive_volume_transformed_corridor": qlist(box),
                "exact_transformed_corridor_volume": qstr(volume(box)),
                "t_boundary_sqrt_enclosure_certificates": certificates,
                "t_boundary_sqrt_enclosures_sha256": digest(certificates),
                "dyadic_inward_shrink_trace": trace,
                "dyadic_inward_shrink_trace_sha256": digest(trace),
                "signed_support_replay": replay,
                "support_basis":
                    "R287_ACTIVE_FACTOR_STRICT_CORRIDOR_REPLAY",
            }
    return None


def classify_contact(
    left: dict[str, Any],
    right: dict[str, Any],
    axis: int,
    face: tuple[Q, ...],
    regions: dict[str, dict[str, Any]],
    cache: dict[tuple[str, tuple[Q, ...], int], dict[str, Any]],
) -> dict[str, Any]:
    classification = contact_class(left, right)
    graph_cells = [
        row for row in (left, right)
        if row["support_mode"] == "ACTIVE_GRAPH_CONSTRAINED"
    ]
    if classification == "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE":
        left_factor = left["factor"]
        right_factor = right["factor"]
        need(
            left_factor["active_function_id"]
            == right_factor["active_function_id"]
            and left_factor["desired_side_sign"]
            != right_factor["desired_side_sign"],
            "opposite-side factor classification",
        )
        return {
            "contact_class": classification,
            "decision": "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH",
            "decision_reason":
                "SAME_ACTIVE_FACTOR_OPPOSITE_STRICT_OPEN_SIDES",
            "face_replay": None,
            "accepted_patch": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": {
                "active_function_id":
                    left_factor["active_function_id"],
                "left_factor_provenance":
                    left_factor["provenance_descriptor"],
                "right_factor_provenance":
                    right_factor["provenance_descriptor"],
                "left_desired_side_sign":
                    left_factor["desired_side_sign"],
                "right_desired_side_sign":
                    right_factor["desired_side_sign"],
                "exact_set_identity":
                    "{f>0} INTERSECT {f<0} = EMPTY",
                "positive_area_common_strict_trace_possible": False,
            },
        }

    if classification == "FULL_FULL":
        patch = inset_face(face, axis, left["physical_t_sign"])
        search = {
            "status": "ACCEPT_DIRECT_FULL_FULL_INSET_FACE_PATCH",
            "face_refinement_depth": 0,
            "initial_face_replays": [],
            "patch_replays": [],
            "exclusion_cover_cell_count": 0,
            "exclusion_cover_sha256": digest([]),
        }
    else:
        search = face_patch_search(
            face, axis, graph_cells, regions, cache
        )
        patch = search["patch"]
    search_evidence = dict(search)
    if search_evidence.get("patch") is not None:
        search_evidence["patch"] = qlist(search_evidence["patch"])

    if search["status"].startswith("REJECT_"):
        return {
            "contact_class": classification,
            "decision": "REJECT_NO_COMMON_POSITIVE_AREA_SIGNED_FACE_PATCH",
            "decision_reason": search["status"],
            "face_replay": search_evidence,
            "accepted_patch": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": {
                "exclusion_cover_cell_count":
                    search["exclusion_cover_cell_count"],
                "exclusion_cover_sha256":
                    search["exclusion_cover_sha256"],
                "positive_area_common_strict_trace_possible": False,
            },
        }
    if not search["status"].startswith("ACCEPT_") or patch is None:
        return {
            "contact_class": classification,
            "decision": "UNRESOLVED_FAIL_CLOSED",
            "decision_reason": search["status"],
            "face_replay": search_evidence,
            "accepted_patch": None,
            "left_corridor": None,
            "right_corridor": None,
            "exclusion_evidence": None,
        }

    left_corridor = certify_corridor(
        left, patch, axis, True, regions, cache
    )
    right_corridor = certify_corridor(
        right, patch, axis, False, regions, cache
    )
    if left_corridor is None or right_corridor is None:
        return {
            "contact_class": classification,
            "decision": "UNRESOLVED_FAIL_CLOSED",
            "decision_reason":
                "STRICT_TWO_SIDED_CORRIDOR_DEPTH_EXHAUSTED",
            "face_replay": search_evidence,
            "accepted_patch": qlist(patch),
            "left_corridor": left_corridor,
            "right_corridor": right_corridor,
            "exclusion_evidence": None,
        }
    return {
        "contact_class": classification,
        "decision": "ACCEPT_STRICT_POSITIVE_AREA_FACE_PATCH_AND_TWO_SIDED_CORRIDOR",
        "decision_reason": search["status"],
        "face_replay": search_evidence,
        "accepted_patch": qlist(patch),
        "accepted_patch_area": qstr(face_area(patch, axis)),
        "accepted_patch_t_boundary_sqrt_enclosure_certificates":
            transformed_t_boundary_certificates(patch),
        "left_corridor": left_corridor,
        "right_corridor": right_corridor,
        "exclusion_evidence": None,
    }


def enumerate_and_classify(
    cells: list[dict[str, Any]],
    regions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    lower_index: dict[tuple[str, int, int, Q], list[int]] = defaultdict(list)
    for index, cell in enumerate(cells):
        for axis in range(3):
            lower_index[(
                cell["source_chart"],
                cell["physical_t_sign"],
                axis,
                cell["box"][2 * axis],
            )].append(index)

    cache: dict[
        tuple[str, tuple[Q, ...], int],
        dict[str, Any],
    ] = {}
    rows = []
    for left in cells:
        for axis in range(3):
            candidates = lower_index.get((
                left["source_chart"],
                left["physical_t_sign"],
                axis,
                left["box"][2 * axis + 1],
            ), [])
            for right_index in candidates:
                right = cells[right_index]
                face = common_face(left["box"], right["box"], axis)
                if face is None:
                    continue
                classification = classify_contact(
                    left, right, axis, face, regions, cache
                )
                same_endpoint = (
                    left["endpoint_occurrence_id"]
                    == right["endpoint_occurrence_id"]
                )
                endpoint_pair = (
                    None
                    if same_endpoint
                    else list(pair(
                        left["endpoint_occurrence_id"],
                        right["endpoint_occurrence_id"],
                    ))
                )
                face_t_certificates = (
                    transformed_t_boundary_certificates(face)
                )
                payload = {
                    "Round299_independent_signed_face_classification_row_id":
                        "round299-independent-signed-face:"
                        + digest([
                            left["cell_id"],
                            right["cell_id"],
                            axis,
                            qlist(face),
                        ]),
                    "left_Round292_refinement_cell_id": left["cell_id"],
                    "right_Round292_refinement_cell_id": right["cell_id"],
                    "left_Round287_support_union_id":
                        left["support_union_id"],
                    "right_Round287_support_union_id":
                        right["support_union_id"],
                    "left_Round275_region_id": left["region_id"],
                    "right_Round275_region_id": right["region_id"],
                    "source_chart": left["source_chart"],
                    "physical_t_sign": left["physical_t_sign"],
                    "common_face_axis": axis,
                    "exact_positive_area_transformed_coordinate_face":
                        qlist(face),
                    "exact_transformed_coordinate_face_area":
                        qstr(face_area(face, axis)),
                    "common_face_t_boundary_sqrt_enclosure_certificates":
                        face_t_certificates,
                    "common_face_t_boundary_sqrt_enclosures_sha256":
                        digest(face_t_certificates),
                    "endpoint_pair_kind": pair_kind(left, right),
                    "left_formal_occurrence_id":
                        left["endpoint_occurrence_id"],
                    "right_formal_occurrence_id":
                        right["endpoint_occurrence_id"],
                    "unordered_nonself_formal_occurrence_endpoint_pair":
                        endpoint_pair,
                    "same_formal_occurrence_endpoint": same_endpoint,
                    "same_Round287_support_union":
                        left["support_union_id"]
                        == right["support_union_id"],
                    "left_support_mode": left["support_mode"],
                    "right_support_mode": right["support_mode"],
                    "left_active_factor_descriptor": left["factor"],
                    "right_active_factor_descriptor": right["factor"],
                    **classification,
                    "diagnostic_nonself_component_edge_candidate":
                        int(
                            classification["decision"].startswith("ACCEPT_")
                            and not same_endpoint
                        ),
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                    "formal_fibre_credit": 0,
                    "formal_global_disposition_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(
        key=lambda row:
            row["Round299_independent_signed_face_classification_row_id"]
    )
    need(len(rows) == 43_092, "signed coordinate common-face census")
    return rows


def load_existing_channel_pairs() -> dict[str, set[tuple[str, str]]]:
    result = {}

    document = read_gzip(R297)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result["R297_ORDINARY"] = {
        tuple(row["exact_occurrence_endpoint_pair"]) for row in rows
    }
    need(len(result["R297_ORDINARY"]) == 330_724, "R297 pair census")
    del document, rows
    gc.collect()

    document = read_gzip(R296)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result["R296_TRUE_SEAM"] = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in rows
    }
    need(len(result["R296_TRUE_SEAM"]) == 15_316, "R296 pair census")
    del document, rows
    gc.collect()

    document = read_gzip(R295A)
    rows = verify_table(document, "rows", "row_count", "rows_sha256")
    result["R295A_LOWER"] = {
        tuple(sorted(row["target_Round294_registry_occurrence_ids"]))
        for row in rows
        if row["target_Round294_registry_reference_count"] == 2
    }
    need(len(result["R295A_LOWER"]) == 111_524, "R295A pair census")
    del document, rows
    gc.collect()
    return result


def census(
    rows: list[dict[str, Any]],
    channels: dict[str, set[tuple[str, str]]],
) -> dict[str, Any]:
    contact_classes = Counter(row["contact_class"] for row in rows)
    decisions = Counter(row["decision"] for row in rows)
    class_decisions = Counter(
        row["contact_class"] + "|" + row["decision"]
        for row in rows
    )
    scope_kind = Counter(
        (
            "SAME_UNION" if row["same_Round287_support_union"]
            else "CROSS_UNION"
        )
        + "|"
        + row["endpoint_pair_kind"]
        for row in rows
    )
    axes = Counter(str(row["common_face_axis"]) for row in rows)
    accepted_pairs = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in rows
        if row["decision"].startswith("ACCEPT_")
        and row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    rejected_pairs = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in rows
        if row["decision"].startswith("REJECT_")
        and row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    unresolved = sum(
        row["decision"] == "UNRESOLVED_FAIL_CLOSED" for row in rows
    )

    need(
        contact_classes == {
            "FULL_FULL": 16_828,
            "SINGLE_GRAPH": 9_576,
            "DOUBLE_GRAPH_SAME_FACTOR_SAME_SIDE": 8_344,
            "DOUBLE_GRAPH_SAME_FACTOR_OPPOSITE_SIDE": 8_344,
        },
        "independent graph contact-class census",
    )
    need(
        scope_kind == {
            "SAME_UNION|UU": 848,
            "SAME_UNION|OU": 464,
            "SAME_UNION|OO": 740,
            "CROSS_UNION|UU": 38_668,
            "CROSS_UNION|OU": 496,
            "CROSS_UNION|OO": 1_876,
        },
        "independent scope/kind census",
    )
    need(
        axes == {"0": 14_552, "1": 16_244, "2": 12_296},
        "independent axis census",
    )

    accepted_rows = [
        row for row in rows if row["decision"].startswith("ACCEPT_")
    ]
    rejected_rows = [
        row for row in rows if row["decision"].startswith("REJECT_")
    ]
    return {
        "input_exact_Round292_refinement_cell_count": 11_852,
        "raw_same_chart_same_physical_t_sign_box_face_contact_count":
            len(rows),
        "contact_class_histogram": dict(sorted(contact_classes.items())),
        "decision_histogram": dict(sorted(decisions.items())),
        "contact_class_decision_histogram":
            dict(sorted(class_decisions.items())),
        "scope_endpoint_kind_histogram": dict(sorted(scope_kind.items())),
        "axis_histogram": dict(sorted(axes.items())),
        "accepted_raw_physical_face_patch_count": len(accepted_rows),
        "accepted_self_endpoint_physical_patch_count": sum(
            row["same_formal_occurrence_endpoint"] for row in accepted_rows
        ),
        "accepted_nonself_raw_component_edge_candidate_count": sum(
            not row["same_formal_occurrence_endpoint"]
            for row in accepted_rows
        ),
        "accepted_distinct_nonself_occurrence_pair_count":
            len(accepted_pairs),
        "accepted_distinct_nonself_occurrence_pairs_sha256":
            digest([list(value) for value in sorted(accepted_pairs)]),
        "rejected_raw_face_contact_count": len(rejected_rows),
        "rejected_distinct_nonself_occurrence_pair_count":
            len(rejected_pairs),
        "rejected_distinct_nonself_occurrence_pairs_sha256":
            digest([list(value) for value in sorted(rejected_pairs)]),
        "unresolved_face_contact_count": unresolved,
        "accepted_pair_existing_channel_intersection_count": {
            name: len(accepted_pairs & pairs)
            for name, pairs in sorted(channels.items())
        },
        "accepted_pair_novel_against_all_three_existing_channels_count":
            len(accepted_pairs - set().union(*channels.values())),
        "all_accepted_rows_have_exact_positive_area_patch": all(
            Q(row["accepted_patch_area"]) > 0
            for row in accepted_rows
        ),
        "all_accepted_rows_have_two_exact_positive_volume_corridors": all(
            Q(row[side]["exact_transformed_corridor_volume"]) > 0
            for row in accepted_rows
            for side in ("left_corridor", "right_corridor")
        ),
        "all_rejected_rows_have_exclusion_evidence": all(
            row["exclusion_evidence"] is not None for row in rejected_rows
        ),
        "all_formal_credits_zero": all(
            row[field] == 0
            for row in rows
            for field in (
                "formal_occurrence_identity_collapse_credit",
                "formal_component_edge_credit",
                "formal_DSU_rank_reduction_credit",
                "formal_maximality_credit",
                "formal_fibre_credit",
                "formal_global_disposition_credit",
            )
        ),
    }


def deterministic_gzip_bytes(value: Any) -> bytes:
    target = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=target,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(canonical(value))
    return target.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    ctx.prec = ARB_PRECISION_BITS
    need(ctx.prec == ARB_PRECISION_BITS, "fixed Arb precision")
    regions = load_regions()
    r287_regions, r287_cells = load_r287()
    refined_occurrence_map = load_refined_occurrence_map()
    cells = load_cells(
        regions,
        r287_regions,
        r287_cells,
        refined_occurrence_map,
    )
    rows = enumerate_and_classify(cells, regions)
    channels = load_existing_channel_pairs()
    result_census = census(rows, channels)
    unresolved = result_census["unresolved_face_contact_count"]
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "PASS_ZERO_CREDIT__ALL_43092_SIGNED_FACE_CONTACTS_CLASSIFIED"
            if unresolved == 0
            else "FAIL_CLOSED__SIGNED_FACE_CONTACTS_REMAIN_UNRESOLVED"
        ),
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([
            row["Round299_independent_signed_face_classification_row_id"]
            for row in rows
        ]),
        "row_hashes_sha256":
            digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }
    result = {
        "schema": SCHEMA,
        "status": ledger["status"],
        "input_file_pins": dict(sorted(PINS.items())),
        "method_contract": {
            "independent_of_parallel_Round299_frontier_producer": True,
            "transformed_coordinate_system": "(t^2,p,s)",
            "same_physical_t_sign_required": True,
            "rational_square_root_reconstruction_exact": True,
            "Round287_active_factor_extrema_semantics_replayed": True,
            "FULL_FULL_requires_exact_two_sided_corridor": True,
            "single_graph_replayed_on_face_and_corridor": True,
            "double_graph_factor_and_side_relation_exhausted": True,
            "opposite_strict_sides_have_empty_common_strict_trace": True,
            "coordinate_box_face_alone_is_never_component_edge_proof": True,
            "python_flint_version": FLINT_VERSION,
            "Arb_precision_bits": ARB_PRECISION_BITS,
            "sqrt_construction_enclosure_bits": SQRT_CONSTRUCTION_BITS,
            "sqrt_replay_enclosure_bits": SQRT_REPLAY_BITS,
            "non_square_sqrt_enclosures_verified_by_rational_inequalities":
                True,
            "active_factor_interval_overwrap_is_unresolved": True,
        },
        "census": result_census,
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(rows),
            "rows_sha256": ledger["rows_sha256"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
        },
        "strict_nonpromotion": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "CM2": (
                "NO_GO_DIAGNOSTIC_ONLY__"
                "FORMAL_PRODUCER_AND_INDEPENDENT_VERIFIER_REQUIRED"
            ),
        },
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=299_103)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    arguments = parser.parse_args()
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(
        ledger_bytes
    ).hexdigest()
    result["result_sha256"] = digest(
        {
            key: value
            for key, value in result.items()
            if key != "result_sha256"
        }
    )
    atomic(arguments.ledger, ledger_bytes)
    atomic(arguments.result, canonical(result) + b"\n")
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print("result_sha256=" + result["result_sha256"])
    print("ledger_file_sha256=" + result["ledger"]["file_sha256"])


if __name__ == "__main__":
    main()
