#!/usr/bin/env python3
"""Certify per-trace reach for the eight repaired source-grazing traces.

The certified ambient models are the unwrapped/periodic source cylinder in
coordinates ``(r,c)`` and ``(r,p)``, where ``r=(9/25)*theta``.  The producer
does not turn either statement into an endpoint-inclusive two-sided collar in
the bounded physical phase space ``|p|<=1``.

The base portion is independently replayed with second-order Arb Jets through
the Round115 outer metric endpoint.  A path-only reverse replay continues
through the positive-width Round114/115 root/base overlap.  The root portion
replays the Round115 correlated affine implicit graph in the source cosine
``c0``.  On the overlap, fixed-path
reversibility and the unique affine implicit root identify both
representations with the same analytic physical state; hence the selected
splice has common first and second physical derivatives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from fractions import Fraction as Q
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round114_rank3_seam_root_stitch_gap_atlas as round114
import cm2_round115_rank3_selected_lift_nofold_atlas as round115
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json"
SCHEMA = "cm2.round119.rank3-eight-grazing-trace-extended-cylinder-reach.v1"

ROUND118 = HERE / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
ROUND118_PRODUCER = HERE / "cm2_round118_rank3_repaired_endpoint_source_cylinder_transfer_atlas.py"
ROUND115 = HERE / "cm2-round115-rank3-selected-lift-nofold-atlas-2026-07-23.json"
ROUND115_PRODUCER = HERE / "cm2_round115_rank3_selected_lift_nofold_atlas.py"
ROUND114 = HERE / "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json"
ROUND114_PRODUCER = HERE / "cm2_round114_rank3_seam_root_stitch_gap_atlas.py"

PINS = {
    ROUND118.name: "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f",
    ROUND118_PRODUCER.name: "bfd517d6dd71aa923ed89400719302bd022945db9cce38e4b74f163ed0fa45f4",
    ROUND115.name: "bcaa3612fe6369b7a6a55e51cd7d345d3a7e4817906dd5998ad544d945035263",
    ROUND115_PRODUCER.name: "2552bcd8ad4cf769b2d65665d43e661331fffd9a0e00330af4bb11283169db7b",
    ROUND114.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    ROUND114_PRODUCER.name: "47a231e32df2121058185a0fd82cbfb6c6105ace0d268a257103bc005b46ed02",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round93_rank3_full_source_chart_exit_cert.py": "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023",
    "cm2_round95_rank3_centered_reverse_interval_cert.py": "c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
}
SCHEMAS = {
    ROUND118.name: "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1",
    ROUND115.name: "cm2.round115.rank3-selected-lift-nofold-atlas.v1",
    ROUND114.name: "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1",
}

PRECISION_BITS = 768
BASE_INITIAL_PARTITION = 1024
BASE_MAX_DEPTH = 32
JOIN_PARTITION = 512
SOURCE_RADIUS = Q(9, 25)
EDGE_WIDTH = Q(1, 16384)

THETA_FIRST_LOWER = Q(2, 5)
THETA_FIRST_UPPER = Q(28)
THETA_SECOND_UPPER = Q(30_000_000)
MOMENTUM_ABS_LOWER = Q(1, 51)
MOMENTUM_SECOND_UPPER = Q(132_651)
R_SECOND_UPPER = Q(10_800_000)
GAMMA_SECOND_UPPER = Q(11_000_000)
SPEED_LOWER = Q(18, 125)
REACH_RADIUS = Q(1, 2_500_000_000)
THETA_SPAN_UPPER = Q(3, 2)

# Orthogonal local normal coordinates.  A determinant -1 row simply chooses
# the reflected angular orientation on that trace; the cylinder metric is
# unchanged.  In every row theta=2*atan(local_y/(1+local_x)).
LOCAL_NORMAL_MATRICES = (
    ((0, -1), (1, 0)),
    ((0, 1), (1, 0)),
    ((-1, 0), (0, 1)),
    ((1, 0), (0, 1)),
    ((-1, 0), (0, -1)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
    ((0, 1), (-1, 0)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    result = json.loads(
        path.read_text(),
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"JSON float forbidden: {token}")),
    )
    require(isinstance(result, dict), f"top-level object: {path.name}")
    return result


def load_closed(path: Path) -> dict[str, Any]:
    require(sha256(path) == PINS[path.name], f"pin mismatch: {path.name}")
    document = strict_json(path)
    require(set(document) == {"schema", "result", "result_sha256"}, f"closed document: {path.name}")
    require(document["schema"] == SCHEMAS[path.name], f"schema: {path.name}")
    require(document["result_sha256"] == digest(document["result"]), f"result digest: {path.name}")
    return document["result"]


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"helper pin mismatch: {name}")
    r118 = load_closed(ROUND118)
    r115 = load_closed(ROUND115)
    r114 = load_closed(ROUND114)
    # Replays all of Round114's own closed upstream/helper pins.
    documents = round114.load_documents()
    require(r118["repaired_endpoint_identity_count"] == 8, "Round118 repaired count")
    require(r115["certified_selected_lift_whole_trace_no_fold_atlas_count"] == 8, "Round115 trace count")
    require(r114["certified_selected_lift_root_edge_stitch_count"] == 8, "Round114 stitch count")
    return r118, r115, r114, documents


def arb_pair(value: arb) -> tuple[Q, Q]:
    return round114.arb_pair(value)


def positive_lower(value: arb, label: str) -> Q:
    require(strict_sign(value) == 1, f"non-strict positive: {label}")
    lower, _ = arb_pair(value)
    require(lower > 0, f"nonpositive lower endpoint: {label}")
    return lower


def require_positive(value: arb, label: str) -> None:
    """Check a directed interval sign without serializing its endpoints."""
    require(strict_sign(value) == 1, f"non-strict positive: {label}")


def require_negative(value: arb, label: str) -> None:
    """Check a directed interval sign without serializing its endpoints."""
    require(strict_sign(value) == -1, f"non-strict negative: {label}")


def negative_abs_lower(value: arb, label: str) -> Q:
    return positive_lower(-value, label)


def abs_upper(value: arb) -> Q:
    lower, upper = arb_pair(value)
    return max(abs(lower), abs(upper))


def contains_zero(value: arb) -> bool:
    return value.contains(0)


def add(a: tuple[Any, Any], b: tuple[Any, Any]) -> tuple[Any, Any]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[Any, Any], b: tuple[Any, Any]) -> tuple[Any, Any]:
    return a[0] - b[0], a[1] - b[1]


def scale(x: Any, a: tuple[Any, Any]) -> tuple[Any, Any]:
    return x * a[0], x * a[1]


def dot(a: tuple[Any, Any], b: tuple[Any, Any]) -> Any:
    return a[0] * b[0] + a[1] * b[1]


def cross(a: tuple[Any, Any], b: tuple[Any, Any]) -> Any:
    return a[0] * b[1] - a[1] * b[0]


def reflect(v: tuple[Any, Any], n: tuple[Any, Any]) -> tuple[Any, Any]:
    return sub(v, scale(2 * dot(v, n), n))


def object_center(identifier: str) -> tuple[Jet, Jet]:
    return center(identifier, Jet(arb(0)))


def radius(identifier: str) -> Jet:
    return aq(round112.radius(identifier))


def tangent(branch: tuple[Any, ...], q: Jet) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet]:
    ux = (1 - q * q) / (1 + q * q)
    uy = 2 * q / (1 + q * q)
    tangent_normal = (-uy, ux)
    direction = (tangent_normal[1], -tangent_normal[0])
    height = dot(tangent_normal, object_center(branch[2])) - branch[3] * radius(branch[2])
    return tangent_normal, direction, height


def line_hit(
    line_normal: tuple[Jet, Jet],
    direction: tuple[Jet, Jet],
    height: Jet,
    identifier: str,
    path_sign: int,
) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet]:
    target = object_center(identifier)
    object_radius = radius(identifier)
    distance = height - dot(line_normal, target)
    radicand = object_radius * object_radius - distance * distance
    require_positive(radicand.value, "line radicand")
    root = radicand.sqrt()
    foot = add(target, scale(distance, line_normal))
    hit = add(foot, scale(path_sign * root, direction))
    return hit, scale(1 / object_radius, sub(hit, target)), radicand


def ray_hit(
    point: tuple[Jet, Jet],
    direction: tuple[Jet, Jet],
    identifier: str,
    path_sign: int,
) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet, Jet]:
    target = object_center(identifier)
    object_radius = radius(identifier)
    delta = sub(target, point)
    longitudinal = dot(direction, delta)
    transverse = cross(direction, delta)
    radicand = object_radius * object_radius - transverse * transverse
    require_positive(radicand.value, "ray radicand")
    root = radicand.sqrt()
    flight = longitudinal + path_sign * root
    hit = add(point, scale(flight, direction))
    return hit, scale(1 / object_radius, sub(hit, target)), flight, radicand


def local_lift(
    normal_vector: tuple[Jet, Jet],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[Jet, Jet, Jet]:
    local_x = matrix[0][0] * normal_vector[0] + matrix[0][1] * normal_vector[1]
    local_y = matrix[1][0] * normal_vector[0] + matrix[1][1] * normal_vector[1]
    require_positive(local_x.value, "local_x")
    z = local_y / (1 + local_x)
    return local_x, local_y, z


def theta_derivatives_from_q(cosine: Jet, z: Jet) -> tuple[arb, arb]:
    c_q = cosine.gradient[0]
    c_qq = cosine.hessian[0][0]
    require(strict_sign(c_q) != 0, "base dc/dq")
    z_q = z.gradient[0]
    z_qq = z.hessian[0][0]
    z_c = z_q / c_q
    z_cc = (z_qq * c_q - z_q * c_qq) / (c_q * c_q * c_q)
    denominator = arb(1) + z.value * z.value
    theta_c = 2 * z_c / denominator
    theta_cc = 2 * z_cc / denominator - 4 * z.value * z_c * z_c / (denominator * denominator)
    return theta_c, theta_cc


def reverse_state_from_q(
    source: Any,
    branch: tuple[Any, ...],
    q: Jet,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
    compute_metric: bool = True,
) -> dict[str, Any]:
    require(path == (1, -1, -1), "fixed reverse path")
    tangent_normal, outgoing2, height = tangent(branch, q)
    hit2, normal2, line_radicand = line_hit(tangent_normal, outgoing2, height, branch[1], path[0])
    incoming2 = reflect(outgoing2, normal2)
    reverse1 = scale(-1, incoming2)
    hit1, normal1, flight1, ray1_radicand = ray_hit(hit2, reverse1, source.target_id, path[1])
    initial = reflect(incoming2, normal1)
    reverse0 = scale(-1, initial)
    hit0, normal0, flight0, ray0_radicand = ray_hit(
        hit1, reverse0, f"{source.source}[0,0]", path[2]
    )
    candidate_delta = sub(object_center(branch[2]), hit2)
    tangent_flight = dot(outgoing2, candidate_delta)
    third_transverse = cross(outgoing2, candidate_delta)
    candidate_radius = radius(branch[2])
    tangent_equation = candidate_radius * candidate_radius - third_transverse * third_transverse

    line_incidence = dot(outgoing2, normal2)
    ray1_incidence = dot(reverse1, normal1)
    ray0_incidence = dot(reverse0, normal0)
    require_positive(line_incidence.value, "line path incidence")
    require_negative(ray1_incidence.value, "ray1 path incidence")
    require_negative(ray0_incidence.value, "ray0 path incidence")
    require_positive(flight1.value, "flight1")
    require_positive(flight0.value, "flight0")
    require_positive(tangent_flight.value, "tangent flight")

    cosine = dot(initial, normal0)
    momentum = cross(normal0, initial)
    result = {
        "q": q,
        "hit0": hit0,
        "normal0": normal0,
        "initial": initial,
        "cosine": cosine,
        "momentum": momentum,
        "c_q": cosine.gradient[0],
        "line_radicand": line_radicand,
        "ray1_radicand": ray1_radicand,
        "ray0_radicand": ray0_radicand,
        "line_incidence": line_incidence,
        "ray1_incidence": ray1_incidence,
        "ray0_incidence": ray0_incidence,
        "flight1": flight1,
        "flight0": flight0,
        "tangent_flight": tangent_flight,
        "tangent_equation": tangent_equation,
    }
    if compute_metric:
        local_x, local_y, z = local_lift(normal0, matrix)
        theta_c, theta_cc = theta_derivatives_from_q(cosine, z)
        result.update(
            {
                "local_x": local_x,
                "local_y": local_y,
                "z": z,
                "theta_c": theta_c,
                "theta_cc": theta_cc,
            }
        )
    return result


def base_state(
    source: Any,
    branch: tuple[Any, ...],
    qa: Q,
    qb: Q,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> dict[str, Any]:
    q = Jet.variable(interval(min(qa, qb), max(qa, qb)), 0)
    return reverse_state_from_q(source, branch, q, path, matrix)


def reverse_prefix_from_q(
    source: Any,
    branch: tuple[Any, ...],
    q: Jet,
    path: tuple[int, int, int],
) -> dict[str, Any]:
    """Reverse through the two downstream collisions, stopping before G.

    This form is used in the correlated join.  It avoids recomputing the
    source-grazing square root from an interval expression; the known root
    source point is instead checked directly for collinearity, positive flight,
    and the exact incidence ``-c0``.
    """
    require(path == (1, -1, -1), "fixed reverse prefix path")
    tangent_normal, outgoing2, height = tangent(branch, q)
    hit2, normal2, line_radicand = line_hit(
        tangent_normal, outgoing2, height, branch[1], path[0]
    )
    incoming2 = reflect(outgoing2, normal2)
    reverse1 = scale(-1, incoming2)
    hit1, normal1, flight1, ray1_radicand = ray_hit(
        hit2, reverse1, source.target_id, path[1]
    )
    initial = reflect(incoming2, normal1)
    reverse0 = scale(-1, initial)
    candidate_delta = sub(object_center(branch[2]), hit2)
    tangent_flight = dot(outgoing2, candidate_delta)
    third_transverse = cross(outgoing2, candidate_delta)
    candidate_radius = radius(branch[2])
    tangent_equation = (
        candidate_radius * candidate_radius - third_transverse * third_transverse
    )
    require_positive(dot(outgoing2, normal2).value, "prefix line incidence")
    require_negative(dot(reverse1, normal1).value, "prefix ray1 incidence")
    require_positive(flight1.value, "prefix flight1")
    require_positive(tangent_flight.value, "prefix tangent flight")
    return {
        "hit1": hit1,
        "initial": initial,
        "reverse0": reverse0,
        "line_radicand": line_radicand,
        "ray1_radicand": ray1_radicand,
        "flight1": flight1,
        "tangent_flight": tangent_flight,
        "tangent_equation": tangent_equation,
    }


def source_chart_coordinate(normal0: tuple[Jet, Jet], chart_id: str) -> Jet:
    side = chart_id.split(":")[1]
    return normal0[1] if side in ("E", "W") else normal0[0]


def total_derivatives(value: Jet, error_first: arb, error_second: arb) -> tuple[arb, arb]:
    first = value.gradient[0] + value.gradient[1] * error_first
    second = (
        value.hessian[0][0]
        + 2 * value.hessian[0][1] * error_first
        + value.hessian[1][1] * error_first * error_first
        + value.gradient[1] * error_second
    )
    return first, second


def root_source_jet(
    root: dict[str, Any],
    c_lower: Q,
    c_upper: Q,
    error_lower: Q,
    error_upper: Q,
) -> tuple[tuple[Jet, Jet], Jet, Jet]:
    c0 = Jet.variable(interval(c_lower, c_upper), 0)
    error = Jet.variable(interval(error_lower, error_upper), 1)
    t = (
        Jet(aq(Q(root["affine_t_reference"])))
        + aq(Q(root["affine_slope"])) * (c0 - aq(Q(root["affine_center_c0"])))
        + error
    )
    return normal(root["source_chart"].split(":")[1], t), c0, t


def root_error_enclosure(
    source: Any,
    branch: tuple[Any, ...],
    root: dict[str, Any],
    c_lower: Q,
    c_upper: Q,
    full_values: dict[str, Jet],
) -> tuple[Q, Q]:
    zero_values = round115.affine_edge_jet(
        source,
        branch,
        root["source_grazing_sign_sigma0"],
        Q(root["affine_t_reference"]),
        Q(root["affine_slope"]),
        Q(root["affine_center_c0"]),
        c_lower,
        c_upper,
        Q(0),
        Q(0),
    )
    # For each fixed c, F(c,e*)=0 and the mean-value theorem gives
    # e*=-F(c,0)/F_e(c,xi).  The full Round115 tube contains xi.
    enclosure = -zero_values["equation"].value / full_values["equation"].gradient[1]
    lower, upper = arb_pair(enclosure)
    radius_bound = Q(root["affine_error_radius"])
    lower, upper = max(lower, -radius_bound), min(upper, radius_bound)
    require(lower < upper, "nonempty parameter-dependent root error enclosure")
    return lower, upper


def root_forward_diagnostics(
    source: Any,
    branch: tuple[Any, ...],
    root: dict[str, Any],
    c_lower: Q,
    c_upper: Q,
    error_lower: Q,
    error_upper: Q,
) -> dict[str, Jet]:
    normal0, c0, _t = root_source_jet(root, c_lower, c_upper, error_lower, error_upper)
    sigma0 = root["source_grazing_sign_sigma0"]
    momentum0 = sigma0 * (1 - c0 * c0).sqrt()
    velocity_x = c0 * normal0[0] - momentum0 * normal0[1]
    velocity_y = c0 * normal0[1] + momentum0 * normal0[0]
    zero = Jet(arb(0))
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    point_x = source_x + aq(round112.radius(source.source)) * normal0[0]
    point_y = source_y + aq(round112.radius(source.source)) * normal0[1]
    first_x, first_y = center(source.target_id, zero)
    first = round112.collision_diagnostic(
        point_x,
        point_y,
        velocity_x,
        velocity_y,
        first_x,
        first_y,
        round112.radius(source.target_id),
    )
    first_c_square = 1 - first["momentum"] * first["momentum"]
    first_c = first_c_square.sqrt()
    outgoing1_x = first_c * first["normal_x"] - first["momentum"] * first["normal_y"]
    outgoing1_y = first_c * first["normal_y"] + first["momentum"] * first["normal_x"]
    second_x, second_y = center(branch[1], zero)
    second = round112.collision_diagnostic(
        first["hit_x"],
        first["hit_y"],
        outgoing1_x,
        outgoing1_y,
        second_x,
        second_y,
        round112.radius(branch[1]),
    )
    second_c_square = 1 - second["momentum"] * second["momentum"]
    second_c = second_c_square.sqrt()
    outgoing2_x = second_c * second["normal_x"] - second["momentum"] * second["normal_y"]
    outgoing2_y = second_c * second["normal_y"] + second["momentum"] * second["normal_x"]
    candidate_x, candidate_y = center(branch[2], zero)
    dx, dy = candidate_x - second["hit_x"], candidate_y - second["hit_y"]
    third_longitudinal = outgoing2_x * dx + outgoing2_y * dy
    third_transverse = -outgoing2_y * dx + outgoing2_x * dy
    candidate_radius = aq(round112.radius(branch[2]))
    equation = candidate_radius * candidate_radius - third_transverse * third_transverse
    return {
        "normal0_x": normal0[0],
        "normal0_y": normal0[1],
        "c0": c0,
        "momentum0": momentum0,
        "source_reverse_radicand": aq(SOURCE_RADIUS * SOURCE_RADIUS) * c0 * c0,
        "source_reverse_incidence": -c0,
        "first_discriminant": first["discriminant"],
        "first_flight": first["flight"],
        "first_c_square": first_c_square,
        "second_discriminant": second["discriminant"],
        "second_flight": second["flight"],
        "second_c_square": second_c_square,
        "third_tangent_flight": third_longitudinal,
        "third_transverse": third_transverse,
        "third_tangency_equation": equation,
    }


def theta_derivatives_on_root(z: Jet, error_first: arb, error_second: arb) -> tuple[arb, arb]:
    z_c, z_cc = total_derivatives(z, error_first, error_second)
    denominator = arb(1) + z.value * z.value
    theta_c = 2 * z_c / denominator
    theta_cc = 2 * z_cc / denominator - 4 * z.value * z_c * z_c / (denominator * denominator)
    return theta_c, theta_cc


def new_extrema() -> dict[str, arb | None]:
    return {
        "theta_lower": None,
        "theta_upper": None,
        "theta_c_lower": None,
        "theta_c_upper": None,
        "theta_cc_abs_upper": None,
        "momentum_abs_lower": None,
        "r_cc_abs_upper": None,
        "local_x_lower": None,
        "cosine_lower": None,
        "cosine_upper": None,
    }


def update_min(stats: dict[str, Q | None], key: str, value: Q) -> None:
    stats[key] = value if stats[key] is None else min(stats[key], value)


def update_max(stats: dict[str, Q | None], key: str, value: Q) -> None:
    stats[key] = value if stats[key] is None else max(stats[key], value)


def update_hull(stats: dict[str, arb | None], key: str, value: arb) -> None:
    """Accumulate an Arb hull; rational endpoint extraction is deferred."""
    stats[key] = value if stats[key] is None else stats[key].union(value)


def certify_metric_leaf(
    stats: dict[str, arb | None],
    cosine: arb,
    momentum: arb,
    local_x: arb,
    z: arb,
    theta_c: arb,
    theta_cc: arb,
    sigma0: int,
    label: str,
    allow_zero_cosine: bool = False,
) -> None:
    if allow_zero_cosine:
        cosine_lower, cosine_upper = arb_pair(cosine)
        require(
            cosine_upper > 0 and (cosine_lower >= 0 or contains_zero(cosine)),
            f"{label} nonnegative cosine enclosure",
        )
    else:
        require_positive(cosine, f"{label} cosine")
    p_abs = sigma0 * momentum
    require(strict_sign(p_abs - aq(MOMENTUM_ABS_LOWER)) == 1, f"{label} momentum > 1/51")
    require(strict_sign(theta_c - aq(THETA_FIRST_LOWER)) == 1, f"{label} theta_c lower")
    require(strict_sign(aq(THETA_FIRST_UPPER) - theta_c) == 1, f"{label} theta_c upper")
    require(strict_sign(aq(THETA_SECOND_UPPER) - abs(theta_cc)) == 1, f"{label} theta_cc")
    require_positive(local_x, f"{label} local_x")

    # The source normal and initial velocity are exact unit vectors: circle
    # normalization, a unit stereographic tangent, and two orthogonal
    # reflections prove this algebraically.  The planar Lagrange identity
    # therefore gives c^2+p^2=1 exactly.  Since the fixed-sign branch obeys
    # |p|>1/51 on every leaf, differentiation with c as coordinate gives the
    # following exact analytic derivatives.  Dependency-prone interval
    # subtraction of two equivalent formulas is deliberately not an
    # acceptance predicate.
    # In particular |p_cc|=1/|p|^3<51^3=132651 exactly.  Together with
    # |r_cc|<R*30,000,000=10,800,000, the triangle inequality gives the
    # ambient acceleration bound 10,932,651<11,000,000.  Likewise
    # r_c>R*(2/5)=18/125 pays the speed lower bound without a dependency-prone
    # interval square root.
    r_cc = aq(SOURCE_RADIUS) * theta_cc
    require(strict_sign(aq(R_SECOND_UPPER) - abs(r_cc)) == 1, f"{label} r_cc")

    theta = 2 * z.atan()
    update_hull(stats, "theta_lower", theta)
    update_hull(stats, "theta_upper", theta)
    update_hull(stats, "theta_c_lower", theta_c)
    update_hull(stats, "theta_c_upper", theta_c)
    update_hull(stats, "theta_cc_abs_upper", abs(theta_cc))
    update_hull(stats, "momentum_abs_lower", p_abs)
    update_hull(stats, "r_cc_abs_upper", abs(r_cc))
    update_hull(stats, "local_x_lower", local_x)
    update_hull(stats, "cosine_lower", cosine)
    update_hull(stats, "cosine_upper", cosine)


EXTREMA_LOWER_KEYS = {
    "theta_lower",
    "theta_c_lower",
    "momentum_abs_lower",
    "local_x_lower",
    "cosine_lower",
}


def serialize_hulls(
    stats: dict[str, arb | None],
    lower_keys: set[str],
    *,
    clamp_cosine_lower_to_zero: bool = False,
) -> dict[str, str]:
    require(all(value is not None for value in stats.values()), "empty extrema")
    result: dict[str, str] = {}
    for key, value in stats.items():
        require(value is not None, f"missing hull: {key}")
        lower, upper = arb_pair(value)
        bound = lower if key in lower_keys else upper
        if clamp_cosine_lower_to_zero and key == "cosine_lower":
            bound = max(Q(0), bound)
        result[key] = str(bound)
    return result


def serialize_extrema(stats: dict[str, arb | None]) -> dict[str, str]:
    return serialize_hulls(
        stats,
        EXTREMA_LOWER_KEYS,
        clamp_cosine_lower_to_zero=True,
    )


def certify_base_trace(
    ray_index: int,
    source: Any,
    branch: tuple[Any, ...],
    q0: Q,
    projective_direction: int,
    cell_edge: Q,
    base_end: Q,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
    sigma0: int,
) -> dict[str, Any]:
    require(cell_edge < base_end, f"ray {ray_index} base parameter order")
    require(path == (1, -1, -1), f"ray {ray_index} reverse path")
    width = base_end - cell_edge
    pending = [(cell, 0, 0) for cell in range(BASE_INITIAL_PARTITION)]
    leaves: list[tuple[int, int, int]] = []
    failures: list[tuple[int, int, int, str]] = []
    stats = new_extrema()
    margins: dict[str, Q | None] = {
        "oriented_minus_dc_dq_lower": None,
        "line_radicand_lower": None,
        "ray1_radicand_lower": None,
        "ray0_radicand_lower": None,
        "line_incidence_lower": None,
        "ray1_incidence_abs_lower": None,
        "ray0_incidence_abs_lower": None,
        "flight1_lower": None,
        "flight0_lower": None,
        "tangent_flight_lower": None,
        "tangent_equation_residual_abs_upper": None,
    }
    while pending:
        cell, subcell, depth = pending.pop()
        denominator = BASE_INITIAL_PARTITION * (1 << depth)
        lower_index = cell * (1 << depth) + subcell
        parameter_lower = cell_edge + width * Q(lower_index, denominator)
        parameter_upper = cell_edge + width * Q(lower_index + 1, denominator)
        qa = q0 + projective_direction * parameter_lower
        qb = q0 + projective_direction * parameter_upper
        try:
            state = base_state(source, branch, qa, qb, path, matrix)
            oriented = -projective_direction * state["c_q"]
            require_positive(oriented, f"ray {ray_index} oriented -dc/dq")
            certify_metric_leaf(
                stats,
                state["cosine"].value,
                state["momentum"].value,
                state["local_x"].value,
                state["z"].value,
                state["theta_c"],
                state["theta_cc"],
                sigma0,
                f"ray {ray_index} base {cell}:{subcell}/{depth}",
            )
            tangent_residual = state["tangent_equation"].value
            require(contains_zero(tangent_residual), f"ray {ray_index} tangent equation")
            update_min(
                margins,
                "oriented_minus_dc_dq_lower",
                positive_lower(oriented, "oriented derivative"),
            )
            update_min(
                margins,
                "line_radicand_lower",
                positive_lower(state["line_radicand"].value, "line radicand"),
            )
            update_min(
                margins,
                "ray1_radicand_lower",
                positive_lower(state["ray1_radicand"].value, "ray1 radicand"),
            )
            update_min(
                margins,
                "ray0_radicand_lower",
                positive_lower(state["ray0_radicand"].value, "ray0 radicand"),
            )
            update_min(
                margins,
                "line_incidence_lower",
                positive_lower(state["line_incidence"].value, "line incidence"),
            )
            update_min(
                margins,
                "ray1_incidence_abs_lower",
                negative_abs_lower(state["ray1_incidence"].value, "ray1 incidence"),
            )
            update_min(
                margins,
                "ray0_incidence_abs_lower",
                negative_abs_lower(state["ray0_incidence"].value, "ray0 incidence"),
            )
            update_min(
                margins,
                "flight1_lower",
                positive_lower(state["flight1"].value, "flight1"),
            )
            update_min(
                margins,
                "flight0_lower",
                positive_lower(state["flight0"].value, "flight0"),
            )
            update_min(
                margins,
                "tangent_flight_lower",
                positive_lower(state["tangent_flight"].value, "tangent flight"),
            )
            update_max(
                margins, "tangent_equation_residual_abs_upper",
                abs_upper(tangent_residual),
            )
            leaves.append((cell, subcell, depth))
        except Exception as exc:
            if depth >= BASE_MAX_DEPTH:
                failures.append((cell, subcell, depth, f"{type(exc).__name__}: {exc}"))
                continue
            pending.append((cell, 2 * subcell + 1, depth + 1))
            pending.append((cell, 2 * subcell, depth + 1))
    require(not failures, f"ray {ray_index} base residuals: {failures[:3]}")
    require(leaves, f"ray {ray_index} empty base partition")
    leaves.sort(key=lambda item: (item[0], Q(item[1], 1 << item[2]), item[2]))
    require(all(value is not None for value in margins.values()), f"ray {ray_index} base margins")

    endpoint_q = q0 + projective_direction * cell_edge
    endpoint = base_state(source, branch, endpoint_q, endpoint_q, path, matrix)
    endpoint_c_lower = positive_lower(endpoint["cosine"].value, f"ray {ray_index} far endpoint c")
    return {
        "parameter_interval": [str(cell_edge), str(base_end)],
        "q_interval": [
            str(q0 + projective_direction * cell_edge),
            str(q0 + projective_direction * base_end),
        ],
        "initial_partition_count": BASE_INITIAL_PARTITION,
        "maximum_adaptive_depth_allowed": BASE_MAX_DEPTH,
        "achieved_maximum_adaptive_depth": max(item[2] for item in leaves),
        "accepted_leaf_count": len(leaves),
        "failed_leaf_count": 0,
        "accepted_leaf_partition_sha256": digest(leaves),
        "fixed_reverse_path": list(path),
        "far_endpoint_source_cosine_lower_bound": str(endpoint_c_lower),
        "extrema": serialize_extrema(stats),
        "path_and_equation_margins": {
            key: str(value) for key, value in margins.items()
        },
    }


def certify_root_trace(
    ray_index: int,
    source: Any,
    branch: tuple[Any, ...],
    root: dict[str, Any],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> dict[str, Any]:
    sigma0 = root["source_grazing_sign_sigma0"]
    power = root["dyadic_leaf_power"]
    leaf_count = 1 << power
    stats = new_extrema()
    evidence: list[tuple[int, int]] = []
    equation_error_margin: Q | None = None
    q_second_margin: Q | None = None
    path_margins: dict[str, Q | None] = {
        "first_discriminant_lower": None,
        "second_discriminant_lower": None,
        "first_incidence_square_lower": None,
        "second_incidence_square_lower": None,
        "source_to_first_flight_lower": None,
        "first_to_second_flight_lower": None,
        "second_to_tangent_flight_lower": None,
        "third_tangency_equation_residual_abs_upper": None,
        "root_error_enclosure_width_upper": None,
    }
    for leaf_index in range(leaf_count):
        c_lower = EDGE_WIDTH * leaf_index / leaf_count
        c_upper = EDGE_WIDTH * (leaf_index + 1) / leaf_count
        values = round115.affine_edge_jet(
            source,
            branch,
            sigma0,
            Q(root["affine_t_reference"]),
            Q(root["affine_slope"]),
            Q(root["affine_center_c0"]),
            c_lower,
            c_upper,
            -Q(root["affine_error_radius"]),
            Q(root["affine_error_radius"]),
        )
        equation_error = values["equation"].gradient[1]
        require(
            strict_sign(equation_error) == root["parameterized_root_tube_equation_error_derivative_sign"],
            f"ray {ray_index} root F_e sign",
        )
        equation_margin = positive_lower(
            root["parameterized_root_tube_equation_error_derivative_sign"] * equation_error,
            f"ray {ray_index} root F_e",
        )
        require(equation_margin > Q(7), f"ray {ray_index} root F_e margin")
        equation_error_margin = (
            equation_margin if equation_error_margin is None else min(equation_error_margin, equation_margin)
        )
        error_lower, error_upper = root_error_enclosure(
            source, branch, root, c_lower, c_upper, values
        )
        update_max(
            path_margins,
            "root_error_enclosure_width_upper",
            error_upper - error_lower,
        )
        tight_values = round115.affine_edge_jet(
            source,
            branch,
            sigma0,
            Q(root["affine_t_reference"]),
            Q(root["affine_slope"]),
            Q(root["affine_center_c0"]),
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        derivatives = round115.implicit_derivatives(tight_values)
        q_second_sign = strict_sign(derivatives["q_second"])
        require(q_second_sign == root["q_second_derivative_sign"], f"ray {ray_index} root q_second sign")
        q_margin = positive_lower(q_second_sign * derivatives["q_second"], f"ray {ray_index} root q_second")
        require(q_margin > Q(1, 1000), f"ray {ray_index} root q_second margin")
        q_second_margin = q_margin if q_second_margin is None else min(q_second_margin, q_margin)

        forward = root_forward_diagnostics(
            source,
            branch,
            root,
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        tangent_residual = forward["third_tangency_equation"].value
        require(contains_zero(tangent_residual), f"ray {ray_index} root tangent equation")
        update_min(
            path_margins, "first_discriminant_lower",
            positive_lower(forward["first_discriminant"].value, "root first discriminant"),
        )
        update_min(
            path_margins, "second_discriminant_lower",
            positive_lower(forward["second_discriminant"].value, "root second discriminant"),
        )
        update_min(
            path_margins, "first_incidence_square_lower",
            positive_lower(forward["first_c_square"].value, "root first incidence square"),
        )
        update_min(
            path_margins, "second_incidence_square_lower",
            positive_lower(forward["second_c_square"].value, "root second incidence square"),
        )
        update_min(
            path_margins, "source_to_first_flight_lower",
            positive_lower(forward["first_flight"].value, "root source-to-first flight"),
        )
        update_min(
            path_margins, "first_to_second_flight_lower",
            positive_lower(forward["second_flight"].value, "root first-to-second flight"),
        )
        update_min(
            path_margins, "second_to_tangent_flight_lower",
            positive_lower(forward["third_tangent_flight"].value, "root tangent flight"),
        )
        update_max(
            path_margins, "third_tangency_equation_residual_abs_upper",
            abs_upper(tangent_residual),
        )

        normal0, c0, _t = root_source_jet(
            root, c_lower, c_upper, error_lower, error_upper
        )
        local_x, _local_y, z = local_lift(normal0, matrix)
        theta_c, theta_cc = theta_derivatives_on_root(
            z, derivatives["error_prime"], derivatives["error_second"]
        )
        momentum = sigma0 * (1 - c0 * c0).sqrt()
        certify_metric_leaf(
            stats,
            c0.value,
            momentum.value,
            local_x.value,
            z.value,
            theta_c,
            theta_cc,
            sigma0,
            f"ray {ray_index} root {leaf_index}",
            allow_zero_cosine=True,
        )
        evidence.append((leaf_index, q_second_sign))
    require(
        equation_error_margin is not None
        and q_second_margin is not None
        and all(value is not None for value in path_margins.values()),
        "empty root partition",
    )
    return {
        "root_coordinate_interval": ["0", str(EDGE_WIDTH)],
        "dyadic_leaf_power": power,
        "dyadic_leaf_count": leaf_count,
        "failed_leaf_count": 0,
        "leaf_q_second_sign_sha256": digest(evidence),
        "equation_error_derivative_abs_lower_bound": str(equation_error_margin),
        "q_second_derivative_abs_lower_bound": str(q_second_margin),
        "exact_corner_identity": "q_prime(0)=0_BY_SOURCE_GRAZING_FLOW_SHIFT",
        "strict_positive_c_q_prime_sign": root["q_prime_sign_for_c0_positive"],
        "fixed_regular_reverse_path_for_c0_positive": [1, -1, -1],
        "root_tube_forward_path_margins": {
            key: str(value) for key, value in path_margins.items()
        },
        "source_reverse_radicand_exact_factorization": "(9/25)^2*c0^2",
        "source_reverse_incidence_exact_factorization": "-c0",
        "projective_q_prime_exact_endpoint_factorization": (
            "q_prime(c0)=c0*H(c0), with fixed nonzero H sign and |H|>1/1000 "
            "from the replayed q_second mean-value bound"
        ),
        "regular_open_root_source_radicand_and_incidence_strict_for_c0_positive": True,
        "endpoint_stratum": {
            "source_cosine": "0",
            "source_reverse_radicand": "0",
            "source_reverse_incidence": "0",
            "source_momentum": str(sigma0),
            "projective_q_prime": "0",
            "kept_in_singularity_ledger": True,
            "counted_as_regular_collision_owner": False,
        },
        "closed_root_downstream_radicands_incidences_and_three_flights_certified": True,
        "closed_root_source_grazing_quantity_falsely_claimed_strict": False,
        "extrema": serialize_extrema(stats),
    }


def chart_radial(normal0: tuple[Jet, Jet], chart_id: str) -> Jet:
    side = chart_id.split(":")[1]
    if side == "E":
        return normal0[0]
    if side == "W":
        return -normal0[0]
    if side == "N":
        return normal0[1]
    return -normal0[1]


def certify_join(
    ray_index: int,
    base_source: Any,
    root_source: Any,
    branch: tuple[Any, ...],
    q0: Q,
    projective_direction: int,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
    root: dict[str, Any],
) -> dict[str, Any]:
    del matrix  # metric derivatives are certified by the adjoining blocks
    outer_lower, outer_upper = map(Q, root["outer_parameter_enclosure"])
    tail_lower = Q(root["pre_root_tail_parameter_interval"][0])
    require(outer_upper < tail_lower, f"ray {ray_index} positive projective anchor")
    require(path == (1, -1, -1), f"ray {ray_index} fixed reverse path")
    c_lower_neighborhood = EDGE_WIDTH / 2
    c_upper_neighborhood = EDGE_WIDTH
    c_width = c_upper_neighborhood - c_lower_neighborhood

    minimum_root_fe: Q | None = None
    minimum_q_second: Q | None = None
    minimum_first_discriminant: Q | None = None
    minimum_second_discriminant: Q | None = None
    minimum_first_flight: Q | None = None
    minimum_second_flight: Q | None = None
    minimum_tangent_flight: Q | None = None
    minimum_projective_q_denominator: Q | None = None
    minimum_signed_tangent_side: Q | None = None
    maximum_equation_residual = Q(0)
    maximum_tangent_side_residual = Q(0)
    maximum_error_width = Q(0)
    evidence: list[int] = []
    for index in range(JOIN_PARTITION):
        c_lower = c_lower_neighborhood + c_width * Q(index, JOIN_PARTITION)
        c_upper = c_lower_neighborhood + c_width * Q(index + 1, JOIN_PARTITION)
        full_values = round115.affine_edge_jet(
            root_source,
            branch,
            root["source_grazing_sign_sigma0"],
            Q(root["affine_t_reference"]),
            Q(root["affine_slope"]),
            Q(root["affine_center_c0"]),
            c_lower,
            c_upper,
            -Q(root["affine_error_radius"]),
            Q(root["affine_error_radius"]),
        )
        error_lower, error_upper = root_error_enclosure(
            root_source, branch, root, c_lower, c_upper, full_values
        )
        maximum_error_width = max(maximum_error_width, error_upper - error_lower)
        tight_values = round115.affine_edge_jet(
            root_source,
            branch,
            root["source_grazing_sign_sigma0"],
            Q(root["affine_t_reference"]),
            Q(root["affine_slope"]),
            Q(root["affine_center_c0"]),
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        derivatives = round115.implicit_derivatives(tight_values)
        signed_fe = (
            root["parameterized_root_tube_equation_error_derivative_sign"]
            * tight_values["equation"].gradient[1]
        )
        fe_margin = positive_lower(signed_fe, f"ray {ray_index} join F_e")
        require(fe_margin > Q(7), f"ray {ray_index} join F_e margin")
        minimum_root_fe = fe_margin if minimum_root_fe is None else min(minimum_root_fe, fe_margin)
        q_second_margin = positive_lower(
            root["q_second_derivative_sign"] * derivatives["q_second"],
            f"ray {ray_index} join q_second",
        )
        require(q_second_margin > Q(1, 1000), f"ray {ray_index} join q_second margin")
        minimum_q_second = (
            q_second_margin
            if minimum_q_second is None
            else min(minimum_q_second, q_second_margin)
        )
        denominator_margin = positive_lower(
            tight_values["projective_q_denominator"].value,
            f"ray {ray_index} join projective denominator",
        )
        minimum_projective_q_denominator = (
            denominator_margin
            if minimum_projective_q_denominator is None
            else min(minimum_projective_q_denominator, denominator_margin)
        )

        forward = root_forward_diagnostics(
            root_source,
            branch,
            root,
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        first_discriminant = positive_lower(
            forward["first_discriminant"].value,
            f"ray {ray_index} join first discriminant",
        )
        second_discriminant = positive_lower(
            forward["second_discriminant"].value,
            f"ray {ray_index} join second discriminant",
        )
        first_flight = positive_lower(
            forward["first_flight"].value, f"ray {ray_index} join first flight"
        )
        second_flight = positive_lower(
            forward["second_flight"].value, f"ray {ray_index} join second flight"
        )
        tangent_flight = positive_lower(
            forward["third_tangent_flight"].value,
            f"ray {ray_index} join tangent flight",
        )
        candidate_radius = aq(round112.radius(branch[2]))
        signed_tangent_side = branch[3] * forward["third_transverse"].value
        signed_tangent_margin = positive_lower(
            signed_tangent_side, f"ray {ray_index} join signed tangent side"
        )
        require(
            strict_sign(signed_tangent_side - candidate_radius / 2) == 1,
            f"ray {ray_index} join tangent side margin",
        )
        minimum_signed_tangent_side = (
            signed_tangent_margin
            if minimum_signed_tangent_side is None
            else min(minimum_signed_tangent_side, signed_tangent_margin)
        )
        tangent_side_residual = (
            forward["third_transverse"].value - branch[3] * candidate_radius
        )
        require(
            contains_zero(tangent_side_residual),
            f"ray {ray_index} join tangent side identity",
        )
        maximum_tangent_side_residual = max(
            maximum_tangent_side_residual, abs_upper(tangent_side_residual)
        )
        minimum_first_discriminant = (
            first_discriminant
            if minimum_first_discriminant is None
            else min(minimum_first_discriminant, first_discriminant)
        )
        minimum_second_discriminant = (
            second_discriminant
            if minimum_second_discriminant is None
            else min(minimum_second_discriminant, second_discriminant)
        )
        minimum_first_flight = (
            first_flight
            if minimum_first_flight is None
            else min(minimum_first_flight, first_flight)
        )
        minimum_second_flight = (
            second_flight
            if minimum_second_flight is None
            else min(minimum_second_flight, second_flight)
        )
        minimum_tangent_flight = (
            tangent_flight
            if minimum_tangent_flight is None
            else min(minimum_tangent_flight, tangent_flight)
        )
        equation_residual = tight_values["equation"].value
        require(contains_zero(equation_residual), f"ray {ray_index} join F enclosure")
        maximum_equation_residual = max(maximum_equation_residual, abs_upper(equation_residual))
        evidence.append(index)

    require(
        all(
            value is not None
            for value in (
                minimum_root_fe,
                minimum_q_second,
                minimum_first_discriminant,
                minimum_second_discriminant,
                minimum_first_flight,
                minimum_second_flight,
                minimum_tangent_flight,
                minimum_projective_q_denominator,
                minimum_signed_tangent_side,
            )
        ),
        f"ray {ray_index} empty exact join replay",
    )

    # One strict interior q anchor confirms that the analytic identity
    # neighborhood lies on the base reverse branch.  The canonical c=edge q
    # value itself is the much tighter frozen Round114/115 enclosure.
    anchor_c = EDGE_WIDTH / 2
    anchor_full = round115.affine_edge_jet(
        root_source,
        branch,
        root["source_grazing_sign_sigma0"],
        Q(root["affine_t_reference"]),
        Q(root["affine_slope"]),
        Q(root["affine_center_c0"]),
        anchor_c,
        anchor_c,
        -Q(root["affine_error_radius"]),
        Q(root["affine_error_radius"]),
    )
    anchor_error_lower, anchor_error_upper = root_error_enclosure(
        root_source, branch, root, anchor_c, anchor_c, anchor_full
    )
    anchor_tight = round115.affine_edge_jet(
        root_source,
        branch,
        root["source_grazing_sign_sigma0"],
        Q(root["affine_t_reference"]),
        Q(root["affine_slope"]),
        Q(root["affine_center_c0"]),
        anchor_c,
        anchor_c,
        anchor_error_lower,
        anchor_error_upper,
    )
    anchor_parameter = (
        anchor_tight["projective_q"].value - aq(q0)
    ) / projective_direction
    anchor_parameter_lower, anchor_parameter_upper = arb_pair(anchor_parameter)
    require(
        outer_upper < anchor_parameter_lower
        and anchor_parameter_upper < tail_lower,
        f"ray {ray_index} strict interior q anchor",
    )
    derived_q_prime_lower = c_lower_neighborhood * Q(1, 1000)
    require(derived_q_prime_lower > 0, f"ray {ray_index} derived q prime")
    return {
        "join_mode": "EXACT_GEOMETRIC_INVOLUTION_PLUS_UNIQUE_IMPLICIT_ROOT",
        "canonical_splice_root_coordinate": str(EDGE_WIDTH),
        "canonical_splice_projective_parameter_enclosure": [
            str(outer_lower),
            str(outer_upper),
        ],
        "base_metric_cover_parameter_upper": str(outer_upper),
        "base_metric_cover_contains_splice_enclosure": True,
        "outer_upper_is_only_a_cover_bound_not_an_asserted_physical_point": True,
        "additional_projective_path_anchor_interval": [str(outer_upper), str(tail_lower)],
        "additional_projective_path_anchor_width": str(tail_lower - outer_upper),
        "strict_interior_projective_anchor_at_c_edge_over_2": [
            str(anchor_parameter_lower),
            str(anchor_parameter_upper),
        ],
        "correlated_positive_c_identity_neighborhood": [
            str(c_lower_neighborhood),
            str(c_upper_neighborhood),
        ],
        "correlated_positive_c_identity_neighborhood_certified": True,
        "correlated_partition_count": JOIN_PARTITION,
        "correlated_partition_sha256": digest(evidence),
        "fixed_reverse_path": list(path),
        "root_equation_error_derivative_abs_lower_bound": str(minimum_root_fe),
        "root_q_second_derivative_abs_lower_bound": str(minimum_q_second),
        "derived_root_q_prime_abs_lower_bound_on_identity_neighborhood": str(
            derived_q_prime_lower
        ),
        "derived_q_prime_proof": (
            "q_prime(0)=0 exactly and signed q_second>1/1000 on [0,edge], "
            "so |q_prime(c)|>c/1000>=edge/2000 throughout [edge/2,edge]"
        ),
        "first_discriminant_lower_bound": str(minimum_first_discriminant),
        "second_discriminant_lower_bound": str(minimum_second_discriminant),
        "source_to_first_flight_lower_bound": str(minimum_first_flight),
        "first_to_second_flight_lower_bound": str(minimum_second_flight),
        "second_to_tangent_flight_lower_bound": str(minimum_tangent_flight),
        "projective_q_denominator_lower_bound": str(
            minimum_projective_q_denominator
        ),
        "signed_tangent_side_lower_bound": str(minimum_signed_tangent_side),
        "tangent_side_identity": "third_transverse=branch_sign*R3",
        "tangent_side_residual_abs_upper": str(maximum_tangent_side_residual),
        "tangent_side_residual_width_used_as_acceptance_predicate": False,
        "correlated_root_error_enclosure_width_upper": str(maximum_error_width),
        "low_level_equation_residual_abs_upper": str(maximum_equation_residual),
        "raw_interval_state_composition_used_as_acceptance_predicate": False,
        "raw_whole_q_image_minmax_used_as_acceptance_predicate": False,
        "exact_identity_proof": (
            "F=0 and the projective-q definition put outgoing2 on the same signed tangent "
            "line. The two specular reflections are algebraic involutions. Fixed circle-root "
            "choices, incidence signs, and positive flights therefore make the reverse branch "
            "unique and return the root source state exactly"
        ),
        "unique_implicit_root_proof": (
            "the MVT error enclosure stays in the Round115 affine tube; F_e has fixed sign "
            "and the tube faces are opposite. Thus no second source state on this branch can "
            "share the same (c,q) data"
        ),
        "c2_splice_proof": (
            "the exact involution identity holds on the positive-width analytic neighborhood "
            "[edge/2,edge], where q_prime is nonzero. Hence theta,c,p and their first/second "
            "derivatives agree through the closure at the unique c=edge root. Base metric "
            "coverage contains its frozen q enclosure and root bounds begin at c=edge"
        ),
        "physical_state_c2_join_certified": True,
    }


def combine_extrema(base: dict[str, Any], root: dict[str, Any]) -> dict[str, str]:
    b = {key: Q(value) for key, value in base["extrema"].items()}
    r = {key: Q(value) for key, value in root["extrema"].items()}
    minimum_keys = {
        "theta_lower",
        "theta_c_lower",
        "momentum_abs_lower",
        "local_x_lower",
        "cosine_lower",
    }
    result: dict[str, str] = {}
    for key in b:
        result[key] = str(min(b[key], r[key]) if key in minimum_keys else max(b[key], r[key]))
    theta_span = Q(result["theta_upper"]) - Q(result["theta_lower"])
    require(theta_span < THETA_SPAN_UPPER, "whole trace theta span")
    result["theta_span_upper_bound"] = str(theta_span)
    return result


def reach_theorem() -> dict[str, Any]:
    m = SPEED_LOWER
    acceleration = GAMMA_SECOND_UPPER
    rho = REACH_RADIUS
    require(SOURCE_RADIUS * THETA_FIRST_LOWER == m, "metric monotonicity identity")
    require(SOURCE_RADIUS * THETA_SECOND_UPPER == R_SECOND_UPPER, "r second identity")
    require(R_SECOND_UPPER + MOMENTUM_SECOND_UPPER == Q(10_932_651), "acceleration sum")
    require(Q(10_932_651) < acceleration, "acceleration budget")
    require(m * m - acceleration * rho == Q(1021, 62500), "double minimizer margin")
    require(m * m - 4 * acceleration * rho == Q(49, 15625), "normal injectivity margin")
    require((m * m - acceleration * rho) / m == Q(1021, 9000), "normal determinant margin")
    # pi>3 proves rho < pi*R/4 from the following exact rational inequality.
    require(rho < 3 * SOURCE_RADIUS / 4, "periodic radius inequality")
    periodic_copy_separation = SOURCE_RADIUS * (Q(6) - THETA_SPAN_UPPER)
    require(periodic_copy_separation == Q(81, 50), "periodic copy separation")
    require(periodic_copy_separation > 2 * rho, "periodic copy offset separation")
    return {
        "common_monotone_coordinate": "r=(9/25)*theta",
        "ambient_models_paid_by_this_common_lemma": [
            "extended/periodic cosine master (r,c)",
            "extended/periodic momentum cylinder (r,p)",
        ],
        "strict_r_derivative_lower_bound": str(m),
        "common_acceleration_upper_bound": str(acceleration),
        "certified_radius": str(rho),
        "double_minimizer_exact_margin_m2_minus_A_rho": "1021/62500",
        "normal_map_exact_margin_m2_minus_4A_rho": "49/15625",
        "normal_map_determinant_lower_bound": "1021/9000",
        "double_minimizer_proof": (
            "if y has two nearest points gamma(c),gamma(d), c<d, h=d-c, "
            "w=y-gamma(c), Delta=gamma(d)-gamma(c), equal distance gives "
            "w dot Delta=|Delta|^2/2.  At the lower point, interior stationarity "
            "or the left-endpoint one-sided minimum gives w dot gamma'(c)<=0. "
            "Taylor gives Delta=h*gamma'(c)+E with |E|<=A*h^2/2, hence "
            "|Delta|^2/2<=rho*A*h^2/2, while r'>=m gives |Delta|>=m*h. "
            "This contradicts m^2-A*rho=1021/62500>0 and covers every "
            "interior/endpoint combination, including both endpoints"
        ),
        "normal_map_injectivity_proof": (
            "N'=J(I-TT^T)gamma''/|gamma'| gives |N'|<=A/m.  For h<=m/A, "
            "tangent projection gives at least m*h/2 while two normal offsets "
            "give less than rho*A*h/m<m*h/4.  For h>=m/A, monotone r separates "
            "centres by at least m^2/A>2*rho.  Same-parameter offsets are unique"
        ),
        "periodic_copy_proof": (
            "each lifted angular span is <3/2.  Since pi>3, distinct 2*pi "
            "copies of the centre trace are separated in r by more than "
            "(9/25)*(6-3/2)=81/50>2*rho; also rho<3R/4<pi*R/4"
        ),
        "compact_nearest_point_existence": True,
        "endpoint_cases_paid_inside_double_minimizer_argument": True,
        "periodic_cylinder_copy_separation_paid": True,
    }


def certify_trace_worker(payload: tuple[int, int]) -> dict[str, Any]:
    """Certify one trace in an independent Arb process context."""
    ray_index, precision_bits = payload
    require(type(ray_index) is int and 0 <= ray_index < 8, "worker ray index")
    require(type(precision_bits) is int, "worker precision type")
    require(precision_bits >= PRECISION_BITS, "worker precision floor")
    ctx.prec = precision_bits
    r118, r115_result, _r114_result, documents = load_inputs()
    roots = {row["ray_index"]: row for row in r115_result["root_edge_rows"]}
    repaired = {row["ray_index"]: row for row in r118["repaired_endpoint_rows"]}
    frozen_rows = {
        row["ray_index"]: row
        for row in documents["r111"]["ray_correction_rows"]
    }
    require(set(roots) == set(repaired) == set(frozen_rows) == set(range(8)), "eight ray indices")

    cores = core_cert.physical_cores()
    by_port = {
        row["registered_port_id"]: row for row in documents["r87"]["port_event_rows"]
    }
    physical = {
        port_id: by_port[port_id]
        for port_id in documents["r99"]["corrected_locally_physical_registered_port_ids"]
    }
    sheet_groups: dict[str, dict[str, dict[str, Any]]] = {}
    for row in documents["r112"]["sheet_rows"]:
        sheet_groups.setdefault(row["exterior_port_id"], {})[row["sheet_kind"]] = row

    frozen = frozen_rows[ray_index]
    root = roots[ray_index]
    repaired_row = repaired[ray_index]
    branch = tuple(frozen["branch_key"])
    port_id = frozen["exterior_port_id"]
    require(root["branch_key"] == repaired_row["branch_key"] == list(branch), f"ray {ray_index} branch")
    require(root["exterior_port_id"] == repaired_row["exterior_port_id"] == port_id, f"ray {ray_index} port")
    require(
        root["source_grazing_sign_sigma0"] == repaired_row["source_grazing_sign_sigma0"],
        f"ray {ray_index} source sign",
    )
    require(
        root["corner_stationary_identity"]
        == "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT",
        f"ray {ray_index} pinned Round115 stationary identity",
    )
    require(
        isinstance(root["corner_flow_shift_lemma"], str)
        and "free-flight-shift-invariant" in root["corner_flow_shift_lemma"],
        f"ray {ray_index} pinned Round115 flow-shift lemma",
    )
    require(
        type(root["corner_flow_shift_lambda_sign"]) is int
        and root["corner_flow_shift_lambda_sign"] in (-1, 1),
        f"ray {ray_index} flow-shift lambda sign",
    )
    require(
        root["root_coordinate_interval"] == ["0", str(EDGE_WIDTH)],
        f"ray {ray_index} root coordinate interval",
    )
    require(
        root["q_prime_closed_interval_avoids_zero"] is False,
        f"ray {ray_index} pinned endpoint q-prime degeneracy",
    )
    require(
        root["affine_tube_inside_round112_t_box"] is True,
        f"ray {ray_index} affine tube inside Round112",
    )
    require(
        root["parameterized_root_tube_theorem"]
        == "UNIFORM_OPPOSITE_FACES_PLUS_FIXED_F_e_SIGN_GIVES_ONE_ROOT_FOR_EVERY_c0",
        f"ray {ray_index} root tube theorem",
    )
    stored_fe_sign = root["parameterized_root_tube_equation_error_derivative_sign"]
    require(
        type(stored_fe_sign) is int and stored_fe_sign in (-1, 1),
        f"ray {ray_index} stored F_e sign",
    )
    require(
        root["parameterized_root_tube_lower_face_sign"] == -stored_fe_sign
        and root["parameterized_root_tube_upper_face_sign"] == stored_fe_sign,
        f"ray {ray_index} oriented opposite tube faces",
    )
    require(
        Q(root["parameterized_root_tube_lower_face_abs_margin"]) > 0
        and Q(root["parameterized_root_tube_upper_face_abs_margin"]) > 0,
        f"ray {ray_index} positive tube face margins",
    )
    require(
        Q(root["parameterized_root_tube_equation_error_derivative_abs_lower_bound"]) >= Q(7),
        f"ray {ray_index} stored F_e lower bound",
    )
    require(
        root["root_edge_q_injective"] is True
        and root["root_edge_to_base_chain_transition"]
        == "UNIQUE_MONOTONE_q_CROSSWALK_ON_ROUND114_OVERLAP"
        and root["root_edge_to_base_chain_transition_coordinate"]
        == "SAME_STEREOGRAPHIC_PROJECTIVE_q"
        and Q(root["root_edge_overlaps_certified_base_before_tail_margin"]) > 0,
        f"ray {ray_index} root/base overlap contract",
    )
    require(
        Q(root["outer_parameter_enclosure"][1])
        < Q(root["pre_root_tail_parameter_interval"][0]),
        f"ray {ray_index} root/base overlap order",
    )
    q0, projective_direction, cell_edge, _inner, _seam, event_kind, *_ = round93.isolate_event(
        branch, frozen["projective_end"], port_id, physical, cores
    )
    require(event_kind == "SOURCE_CHART_SEAM", f"ray {ray_index} event")
    base_end = Q(root["outer_parameter_enclosure"][1])
    require(
        base_end < Q(root["pre_root_tail_parameter_interval"][0]),
        f"ray {ray_index} overlap",
    )
    base_source = cores[branch[0]]
    path = round95.discover_path(
        base_source,
        branch,
        q0 + projective_direction * (cell_edge + base_end) / 2,
    )
    matrix = LOCAL_NORMAL_MATRICES[ray_index]
    print(f"Round119 ray {ray_index}: base", file=sys.stderr, flush=True)
    base = certify_base_trace(
        ray_index,
        base_source,
        branch,
        q0,
        projective_direction,
        cell_edge,
        base_end,
        path,
        matrix,
        root["source_grazing_sign_sigma0"],
    )

    hit = sheet_groups[port_id]["HIT"]
    require(hit["source_chart"] == root["source_chart"], f"ray {ray_index} root chart")
    root_source = replace(cores[branch[0]], chart_id=root["source_chart"])
    print(f"Round119 ray {ray_index}: root", file=sys.stderr, flush=True)
    root_certificate = certify_root_trace(ray_index, root_source, branch, root, matrix)
    print(f"Round119 ray {ray_index}: splice", file=sys.stderr, flush=True)
    join = certify_join(
        ray_index,
        base_source,
        root_source,
        branch,
        q0,
        projective_direction,
        path,
        matrix,
        root,
    )
    whole = combine_extrema(base, root_certificate)
    result = {
        "ray_index": ray_index,
        "repaired_endpoint_id": repaired_row["repaired_endpoint_id"],
        "exterior_port_id": port_id,
        "branch_key": list(branch),
        "projective_end": frozen["projective_end"],
        "source_component": "G",
        "source_radius": str(SOURCE_RADIUS),
        "source_grazing_sign_sigma0": root["source_grazing_sign_sigma0"],
        "local_normal_matrix": [list(matrix[0]), list(matrix[1])],
        "local_angular_lift": "theta=2*atan(local_y/(1+local_x))",
        "local_matrix_is_orthogonal": True,
        "local_matrix_orientation_may_be_reflected": True,
        "base_certificate": base,
        "root_certificate": root_certificate,
        "root_base_c2_splice_certificate": join,
        "whole_trace_extrema": whole,
        "whole_trace_theta_span_strictly_below_3_over_2": True,
        "ambient_extended_cosine_master_self_reach": str(REACH_RADIUS),
        "ambient_extended_momentum_cylinder_self_reach": str(REACH_RADIUS),
        "periodic_source_cylinder_copy_separation_certified": True,
        "unit_identity_geometric_proof_certified": True,
        "analytic_momentum_derivatives_from_exact_identity_certified": True,
        "cross_trace_union_reach_installed": False,
        "bounded_phase_space_two_sided_endpoint_collar_installed": False,
    }
    print(
        f"Round119 ray {ray_index}: leaves={base['accepted_leaf_count']} "
        f"depth={base['achieved_maximum_adaptive_depth']}",
        file=sys.stderr,
        flush=True,
    )
    return result


def certify_rows(
    precision_bits: int,
    workers: int,
    ray_indices: list[int],
) -> list[dict[str, Any]]:
    require(type(precision_bits) is int, "precision type")
    require(precision_bits >= PRECISION_BITS, f"precision must be at least {PRECISION_BITS}")
    require(type(workers) is int and 1 <= workers <= 8, "worker count")
    require(
        ray_indices
        and all(type(index) is int and 0 <= index < 8 for index in ray_indices)
        and len(set(ray_indices)) == len(ray_indices),
        "distinct worker ray indices",
    )
    ctx.prec = precision_bits
    r118, r115_result, _r114_result, documents = load_inputs()
    roots = {row["ray_index"] for row in r115_result["root_edge_rows"]}
    repaired = {row["ray_index"] for row in r118["repaired_endpoint_rows"]}
    frozen_rows = {row["ray_index"] for row in documents["r111"]["ray_correction_rows"]}
    require(roots == repaired == frozen_rows == set(range(8)), "eight ray indices")
    payloads = [(ray_index, precision_bits) for ray_index in ray_indices]
    if workers == 1:
        trace_rows = [certify_trace_worker(payload) for payload in payloads]
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=get_context("spawn"),
        ) as executor:
            trace_rows = list(executor.map(certify_trace_worker, payloads))
    trace_rows.sort(key=lambda row: row["ray_index"])
    return trace_rows


def build(precision_bits: int = PRECISION_BITS, workers: int = 1) -> dict[str, Any]:
    trace_rows = certify_rows(precision_bits, workers, list(range(8)))

    require(len(trace_rows) == 8, "trace count")
    total_base_leaves = sum(row["base_certificate"]["accepted_leaf_count"] for row in trace_rows)
    total_root_leaves = sum(row["root_certificate"]["dyadic_leaf_count"] for row in trace_rows)
    result = {
        "precision_bits": precision_bits,
        "arithmetic": (
            "768-bit-or-higher directed Arb interval arithmetic; exact rationals for all "
            "acceptance thresholds and reach inequalities"
        ),
        "input_repaired_source_grazing_trace_count": 8,
        "certified_whole_trace_c2_splice_count": 8,
        "certified_per_trace_ambient_extended_cosine_master_reach_count": 8,
        "certified_per_trace_ambient_extended_momentum_cylinder_reach_count": 8,
        "pinned_round115_corner_stationary_identity_replayed_count": 8,
        "pinned_round115_root_existence_uniqueness_contract_replayed_count": 8,
        "certified_periodic_copy_separation_count": 8,
        "cross_trace_union_reach_count": 0,
        "source_component": "G",
        "source_radius": str(SOURCE_RADIUS),
        "ambient_models": {
            "cosine_master": "S^1_(9/25) x R_c with metric dr^2+dc^2",
            "momentum_master": "S^1_(9/25) x R_p with metric dr^2+dp^2",
            "flattened_coordinate": "r=(9/25)*theta",
            "bounded_physical_phase_space": "S^1_(9/25) x [-1,1]_p",
        },
        "threshold_contract": {
            "theta_c_strict_lower_bound": str(THETA_FIRST_LOWER),
            "theta_c_strict_upper_bound": str(THETA_FIRST_UPPER),
            "theta_cc_abs_strict_upper_bound": str(THETA_SECOND_UPPER),
            "momentum_abs_strict_lower_bound": str(MOMENTUM_ABS_LOWER),
            "momentum_cc_abs_strict_upper_bound": str(MOMENTUM_SECOND_UPPER),
            "r_cc_abs_strict_upper_bound": str(R_SECOND_UPPER),
            "metric_speed_strict_lower_bound": str(SPEED_LOWER),
            "momentum_curve_acceleration_strict_upper_bound": str(GAMMA_SECOND_UPPER),
            "theta_span_strict_upper_bound": str(THETA_SPAN_UPPER),
            "reach_radius": str(REACH_RADIUS),
        },
        "unit_identity_geometric_proof": (
            "each circle normal is (hit-center)/R and the certified hit equation gives unit "
            "norm; the stereographic tangent direction is unit and reflection preserves norm, "
            "so both normal0 and initial are unit vectors.  The planar Lagrange "
            "identity (initial dot normal0)^2+(normal0 cross initial)^2="
            "|initial|^2|normal0|^2 gives c^2+p^2=1 exactly"
        ),
        "unit_identity_geometric_proof_certified": True,
        "exact_unit_identity_and_analytic_momentum_derivative_contract": {
            "definitions": "c=initial dot normal0; p=normal0 cross initial",
            "unit_chain": (
                "on the base, circle normalization and the certified hit equations make "
                "normal0 unit, while the stereographic tangent is unit and specular "
                "reflections are orthogonal, so initial is unit; planar Lagrange gives "
                "c^2+p^2=1 exactly. On the root, the source-chart normal is unit and "
                "p=sigma0*sqrt(1-c^2) by construction, giving the same identity directly"
            ),
            "splice_branch_identity": (
                "the exact geometric involution identifies the base and root states on the "
                "positive-width overlap with the same fixed sigma0 momentum branch"
            ),
            "fixed_momentum_branch_abs_lower_bound": str(MOMENTUM_ABS_LOWER),
            "first_derivative_exact": "p_c=-c/p",
            "second_derivative_exact": "p_cc=-1/p^3",
            "momentum_second_derivative_bound_derivation": (
                "|p|>1/51 implies |p_cc|=1/|p|^3<51^3=132651"
            ),
            "metric_speed_bound_derivation": (
                "r_c=(9/25)*theta_c>(9/25)*(2/5)=18/125, hence |gamma'|>18/125"
            ),
            "metric_acceleration_bound_derivation": (
                "|r_cc|<10800000 and |p_cc|<132651 imply "
                "|gamma''|<=|r_cc|+|p_cc|<10932651<11000000"
            ),
            "endpoint_values": "c=0 and p=sigma0 in {+1,-1}",
            "analytic_derivatives_used_for_speed_and_acceleration_bounds": True,
        },
        "interval_dependency_residual_width_used_as_acceptance_predicate": False,
        "root_base_global_regularization": (
            "the second-order base metric block covers the complete Round115 outer q enclosure. "
            "The canonical splice is the unique implicit root point c*=1/16384 whose q value lies "
            "in that enclosure; outer_upper is only the base-cover bound, not an asserted physical "
            "point. A correlated fixed-path replay on c in [1/32768,1/16384] identifies the "
            "reverse and implicit formulae as one analytic state, so their first/second derivatives "
            "agree at c* while the root bounds cover the remainder"
        ),
        "reach_theorem": reach_theorem(),
        "base_initial_partition_count_per_trace": BASE_INITIAL_PARTITION,
        "base_maximum_adaptive_depth": BASE_MAX_DEPTH,
        "base_total_accepted_leaf_count": total_base_leaves,
        "base_accepted_leaf_counts": [
            row["base_certificate"]["accepted_leaf_count"] for row in trace_rows
        ],
        "base_achieved_maximum_depths": [
            row["base_certificate"]["achieved_maximum_adaptive_depth"] for row in trace_rows
        ],
        "root_total_dyadic_leaf_count": total_root_leaves,
        "trace_rows": trace_rows,
        "trace_rows_sha256": digest(trace_rows),
        "physical_endpoint_obstruction": {
            "root_endpoint_source_cosine": "c=0",
            "root_endpoint_momentum": "p=sigma0=+1_or_-1",
            "distance_to_bounded_momentum_boundary": "1-|p|=0",
            "uniform_endpoint_inclusive_two_sided_physical_collar_impossible": True,
        },
        "strict_scope": (
            "eight individual repaired source-grazing traces; per-trace self-reach in the "
            "extended cosine and momentum source cylinders, including endpoint and periodic "
            "copy cases; no separation between different traces or other singular strata"
        ),
        "strict_nonclaims": [
            "the eight traces are certified separately; reach of their union is not installed",
            "no uniform separation from other collision singularities, wall corners, flight caps, or unrelated strata is installed",
            "at c=0 one has p=+1 or -1, so the bounded physical phase space admits no endpoint-inclusive two-sided momentum collar",
            "extended-cylinder/stratified-master reach is not a physical-owner collar and does not create a standard-curve child",
            "no complete 57-candidate collar ordering, homogeneity child, official word, or Gate5 field is installed",
        ],
        "physical_owner_whole_trace_atlas_installed": False,
        "bounded_phase_space_endpoint_inclusive_two_sided_collar_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "actual_standard_curve_child_count": 0,
        "canonical_curve_recut_instance_count": 0,
        "new_gate5_actual_child_field_count": 0,
        "gate5_child_field_counts": {f"F{i}": 0 for i in range(1, 7)},
        "gate5_global_maturity": "10/18",
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "upstream_and_helper_pins": dict(sorted(PINS.items())),
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=PRECISION_BITS)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--only-rays", nargs="+", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.only_rays is not None:
        rows = certify_rows(args.precision, args.workers, args.only_rays)
        print(
            json.dumps(
                {
                    "precision_bits": args.precision,
                    "ray_indices": [row["ray_index"] for row in rows],
                    "row_sha256": {
                        str(row["ray_index"]): digest(row) for row in rows
                    },
                    "base_leaf_counts": {
                        str(row["ray_index"]): row["base_certificate"][
                            "accepted_leaf_count"
                        ]
                        for row in rows
                    },
                },
                sort_keys=True,
            )
        )
        return 0
    document = build(args.precision, args.workers)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "schema": document["schema"],
                "result_sha256": document["result_sha256"],
                "base_leaf_counts": document["result"]["base_accepted_leaf_counts"],
                "cm2_verdict": document["result"]["cm2_verdict"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
