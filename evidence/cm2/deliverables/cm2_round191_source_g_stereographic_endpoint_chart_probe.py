#!/usr/bin/env python3
"""Read-only stereographic endpoint-chart probe for the Round188 tail.

Round188 leaves 288 factor faces at ``p = +/-1`` because the square-root
coordinate ``rp = sqrt(1-p^2)`` has no usable full-face p derivative there.
Round189 shows that bounded p bisection only partially helps.  This spike
does not split p.  It instead uses the smooth rational circle chart

    p  = sigma * (1-u^2) / (1+u^2),
    rp =             2*u / (1+u^2),       u >= 0,

and reconstructs the factor geometry as a dual function of ``(u, s)`` on
each fixed t-face.

The accepted face normal forms are mutually exclusive: either a unique
two-boundary-endpoint factor curve, or a strict-monotone active factor whose
two graph-axis endpoint edges have one common strict C0 sign and hence no
zero.  This is diagnostic only: stdout is the sole result channel, stderr
carries progress, there is no output-path option, and no leaf/global credit
is issued.  Probe-only trust boundary: imported Round189/188/186 modules
execute before this module can pin them.  All imported sources and the
complete Round182 package are pinned immediately afterwards, but a formal
verifier must instead pin inert bytes before loading an independent evaluator.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from math import isqrt
import json
from pathlib import Path
import sys
from typing import Any

from flint import arb, ctx

import cm2_round189_source_g_endpoint_p_refinement_probe as r189


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round191.source-g-stereographic-endpoint-chart-probe.v1"

ROUND189_SOURCE = "cm2_round189_source_g_endpoint_p_refinement_probe.py"
ROUND189_SOURCE_SHA256 = (
    "118f0ec0333562026294ba4667cf7498403c4b6274378921afaa3819ef9323e4"
)
ROUND188_SOURCE = (
    "cm2_round188_source_g_factor_face_boundary_arrangement_probe.py"
)
ROUND188_SOURCE_SHA256 = (
    "11e033c726a51bab875f42c371682814a84f46871f1a45797d5c68aa3b3149de"
)
ROUND186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
ROUND186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

EXPECTED_ENDPOINT_FACES = 288
EXPECTED_ENDPOINT_LEAVES = 288
EXPECTED_ENDPOINT_ORIGINS = 8
EXPECTED_NEGATIVE_ENDPOINT_FACES = 144
EXPECTED_POSITIVE_ENDPOINT_FACES = 144
EXPECTED_ENDPOINT_FACES_ON_TWO_SIDED_U_LEAVES = 0
EXPECTED_TWO_SIDED_U_LEAVES = 88
EXPECTED_WALL_G_RESIDUAL_LEAVES = 64

EXPECTED_ROUND189_DEPTH2_REFINEMENT_SHA256 = (
    "52ad352756cd5a9dcdd800142145d771c01a5db5e7c5b9ac634c8e2e694f2b0f"
)
EXPECTED_ROUND189_DEPTH2_AUDIT_ROWS_SHA256 = (
    "a3e3c264699820d08d0e406b2692987a5c41aebc8a804ef9d7c3029526c99550"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
UNIQUE_ZERO = "UNIQUE_BRACKETED_ZERO"
ZERO_ABSENT = {
    "STRICT_C0_ZERO_ABSENT",
    "STRICT_MONOTONE_ZERO_ABSENT",
}


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


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def q_interval(lower: Q, upper: Q) -> arb:
    require(lower <= upper, "ordered rational interval")
    midpoint = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arb(arbq(midpoint), arbq(radius))


def strict_sign(value: arb) -> str:
    return r189.r188.r186.r179.arb_sign(value)


def rational_sqrt_upper(value: Q, bits: int = 192) -> Q:
    """Smallest bits-denominator dyadic whose square is at least value."""

    require(value > 0, "positive square-root radicand")
    denominator = 1 << bits
    scaled_numerator = value.numerator << (2 * bits)
    root = isqrt(scaled_numerator // value.denominator)
    while root * root * value.denominator < scaled_numerator:
        root += 1
    while (
        root
        and (root - 1) * (root - 1) * value.denominator
        >= scaled_numerator
    ):
        root -= 1
    result = Q(root, denominator)
    require(result * result >= value, "sqrt upper enclosure")
    if root:
        require(
            Q(root - 1, denominator) ** 2 < value,
            "sqrt upper is least selected dyadic",
        )
    return result


def dconstant(value: arb) -> tuple[arb, tuple[arb, arb]]:
    return value, (arb(0), arb(0))


def dadd(
    left: tuple[arb, tuple[arb, arb]],
    right: tuple[arb, tuple[arb, arb]],
) -> tuple[arb, tuple[arb, arb]]:
    return (
        left[0] + right[0],
        tuple(
            x + y
            for x, y in zip(left[1], right[1], strict=True)
        ),
    )


def dneg(
    value: tuple[arb, tuple[arb, arb]],
) -> tuple[arb, tuple[arb, arb]]:
    return -value[0], tuple(-derivative for derivative in value[1])


def dsub(
    left: tuple[arb, tuple[arb, arb]],
    right: tuple[arb, tuple[arb, arb]],
) -> tuple[arb, tuple[arb, arb]]:
    return dadd(left, dneg(right))


def dmul(
    left: tuple[arb, tuple[arb, arb]],
    right: tuple[arb, tuple[arb, arb]],
) -> tuple[arb, tuple[arb, arb]]:
    return (
        left[0] * right[0],
        tuple(
            x * right[0] + left[0] * y
            for x, y in zip(left[1], right[1], strict=True)
        ),
    )


def dscale(
    value: tuple[arb, tuple[arb, arb]],
    factor: arb | int,
) -> tuple[arb, tuple[arb, arb]]:
    return (
        value[0] * factor,
        tuple(derivative * factor for derivative in value[1]),
    )


def chart_geometry(
    chart: str,
    target_id: str,
    t_value: Q,
    sigma: int,
    u_value: arb,
    s_value: arb,
) -> dict[str, tuple[arb, tuple[arb, arb]]]:
    """Round186 outgoing-W geometry in the smooth (u,s) chart."""

    require(sigma in {-1, 1}, "stereographic endpoint sign")
    r186 = r189.r188.r186
    u = (u_value, (arb(1), arb(0)))
    s = (s_value, (arb(0), arb(1)))
    one = dconstant(arb(1))
    u_squared = dmul(u, u)
    denominator = dadd(one, u_squared)
    require(bool(denominator[0] > 0), "strict chart denominator")
    p = dscale(
        dmul(
            dsub(one, u_squared),
            (
                1 / denominator[0],
                tuple(
                    -derivative / (denominator[0] * denominator[0])
                    for derivative in denominator[1]
                ),
            ),
        ),
        sigma,
    )
    rp = dmul(dscale(u, 2), (
        1 / denominator[0],
        tuple(
            -derivative / (denominator[0] * denominator[0])
            for derivative in denominator[1]
        ),
    ))

    t = arbq(t_value)
    rt = r186.r179.r174.atlas.ge.sqrt_one_minus_square(t_value, t_value)
    constant_t = dconstant(t)
    constant_rt = dconstant(rt)
    cell = chart.split(":")[1]
    if cell == "E":
        nx, ny = constant_rt, constant_t
    elif cell == "W":
        nx, ny = dneg(constant_rt), constant_t
    elif cell == "N":
        nx, ny = constant_t, constant_rt
    elif cell == "S":
        nx, ny = constant_t, dneg(constant_rt)
    else:
        raise RuntimeError(f"unknown source-G chart cell:{cell}")

    ux = dsub(dmul(rp, nx), dmul(p, ny))
    uy = dadd(dmul(rp, ny), dmul(p, nx))
    source_x = dscale(nx, arb(9) / 25)
    source_y = dscale(ny, arb(9) / 25)
    target = r186.r179.r174.first_hit.target_by_id(target_id)
    require(target.obstacle == "W", "stereographic geometry requires W target")
    cx = dadd(
        dconstant(arb(target.ix) + arb(1) / 2),
        s,
    )
    cy = dconstant(arb(target.iy) + arb(1) / 2)
    dx = dsub(cx, source_x)
    dy = dsub(cy, source_y)
    transverse = dadd(dneg(dmul(uy, dx)), dmul(ux, dy))
    radius_q = r186.r179.r174.first_hit.RADIUS[target.obstacle]
    radius = arb(radius_q.numerator) / radius_q.denominator
    discriminant = dsub(
        dconstant(radius * radius),
        dmul(transverse, transverse),
    )
    require(bool(discriminant[0] > 0), "strict transformed discriminant")
    radical_value = discriminant[0].sqrt()
    radical = (
        radical_value,
        tuple(
            derivative / (2 * radical_value)
            for derivative in discriminant[1]
        ),
    )
    out_x = dscale(
        dadd(dneg(dmul(radical, ux)), dmul(transverse, uy)),
        1 / radius,
    )
    out_y = dscale(
        dsub(dneg(dmul(radical, uy)), dmul(transverse, ux)),
        1 / radius,
    )
    return {
        "HPLUS": dadd(out_x, out_y),
        "HMINUS": dsub(out_x, out_y),
        "NX": out_x,
        "NY": out_y,
        "P": p,
        "RP": rp,
    }


def centered_c0(
    chart: str,
    target_id: str,
    t_value: Q,
    sigma: int,
    u_range: arb,
    s_range: arb,
    u_center: arb,
    s_center: arb,
    kind: str,
) -> arb:
    point = chart_geometry(
        chart,
        target_id,
        t_value,
        sigma,
        u_center,
        s_center,
    )[kind][0]
    full = chart_geometry(
        chart,
        target_id,
        t_value,
        sigma,
        u_range,
        s_range,
    )[kind]
    return (
        point
        + full[1][0] * (u_range - u_center)
        + full[1][1] * (s_range - s_center)
    )


def c0_profile(
    chart: str,
    target_id: str,
    t_value: Q,
    sigma: int,
    u_range: arb,
    s_range: arb,
    u_center: arb,
    s_center: arb,
    kind: str,
) -> dict[str, str]:
    direct = chart_geometry(
        chart,
        target_id,
        t_value,
        sigma,
        u_range,
        s_range,
    )[kind][0]
    centered = centered_c0(
        chart,
        target_id,
        t_value,
        sigma,
        u_range,
        s_range,
        u_center,
        s_center,
        kind,
    )
    direct_sign = strict_sign(direct)
    centered_sign = strict_sign(centered)
    selected = (
        direct_sign if direct_sign in STRICT_SIGNS else centered_sign
    )
    return {
        "direct_sign": direct_sign,
        "centered_sign": centered_sign,
        "selected_sign": selected,
    }


def point_box(
    face: Any,
    p: Q,
    s: Q,
    label: str,
) -> Any:
    return r189.r188.r186.r179.r174.atlas.AtlasBox(
        face.t0,
        face.t1,
        p,
        p,
        s,
        s,
        face.depth,
        face.path + "." + label,
    )


def chart_audit(
    box: Any,
    endpoint: str,
) -> dict[str, Any]:
    if endpoint == "p=-1":
        sigma = -1
        p_inner = box.p1
        require(box.p0 == Q(-1), "negative endpoint face")
    elif endpoint == "p=+1":
        sigma = 1
        p_inner = box.p0
        require(box.p1 == Q(1), "positive endpoint face")
    else:
        raise RuntimeError(f"unknown endpoint:{endpoint}")

    denominator = 1 + sigma * p_inner
    numerator = 1 - sigma * p_inner
    require(denominator > 0 and numerator > 0, "positive endpoint chart ratio")
    u_max_squared = numerator / denominator
    require(
        sigma * (1 - u_max_squared) / (1 + u_max_squared)
        == p_inner,
        "exact p_inner inverse map",
    )
    require(sigma * Q(1) == Q(sigma), "exact p endpoint map")
    require(2 * Q(0) == 0, "exact rp endpoint map")

    # Exact numerator of p^2 + rp^2 - 1 as a polynomial in z=u^2.
    identity_coefficients = (
        sigma * sigma - 1,
        -2 * sigma * sigma + 4 - 2,
        sigma * sigma - 1,
    )
    require(
        identity_coefficients == (0, 0, 0),
        "exact rational unit-circle identity",
    )

    u_max = arbq(u_max_squared).sqrt()
    u_upper = rational_sqrt_upper(u_max_squared)
    u_range = q_interval(Q(0), u_upper)
    require(bool(u_range.contains(u_max)), "u range contains algebraic u_max")
    require(
        u_upper * u_upper >= u_max_squared,
        "dyadic u_max cover",
    )
    return {
        "sigma": sigma,
        "p_inner": p_inner,
        "u_max_squared": u_max_squared,
        "u_max": u_max,
        "u_upper": u_upper,
        "u_range": u_range,
        "symbolic_unit_identity_coefficients": identity_coefficients,
    }


def transformed_arrangement(item: dict[str, Any]) -> dict[str, Any]:
    r186 = r189.r188.r186
    row = item["leaf_row"]
    collar = item["collar"]
    box = item["box"]
    upper = item["upper"]
    side = item["side"]
    face = r186.r179.face_box(box, "t", upper)
    require(face.t0 == face.t1, "fixed t face")
    audit = chart_audit(box, item["endpoint"])
    sigma = audit["sigma"]
    p_inner = audit["p_inner"]
    u_max = audit["u_max"]
    u_upper = audit["u_upper"]
    u_range = audit["u_range"]
    s_range = q_interval(face.s0, face.s1)
    u_center = u_max / 2
    s_mid_q = (face.s0 + face.s1) / 2
    s_center = arbq(s_mid_q)

    initial = item["initial_arrangement"]
    active_kind = initial["active_factor"]
    inactive_kind = initial["inactive_factor"]
    require(
        {active_kind, inactive_kind} == {"HPLUS", "HMINUS"},
        "one active and one inactive factor",
    )

    full = chart_geometry(
        collar["chart"],
        collar["owner_target"],
        face.t0,
        sigma,
        u_range,
        s_range,
    )
    normal = full["NX"][0] * full["NX"][0] + full["NY"][0] * full["NY"][0]
    require(bool(normal > 0), "transformed normal zero excluded")
    inactive_c0 = c0_profile(
        collar["chart"],
        collar["owner_target"],
        face.t0,
        sigma,
        u_range,
        s_range,
        u_center,
        s_center,
        inactive_kind,
    )
    inactive_strict = inactive_c0["selected_sign"] in STRICT_SIGNS
    if inactive_strict:
        require(
            inactive_c0["selected_sign"]
            == initial["inactive_factor_sign"],
            "inactive factor sign agrees with Round188",
        )

    face_du_sign = strict_sign(full[active_kind][1][0])
    face_ds_sign = strict_sign(full[active_kind][1][1])
    graph_axis = (
        "u"
        if face_du_sign in STRICT_SIGNS
        else "s" if face_ds_sign in STRICT_SIGNS else None
    )

    corner_specs = {
        "SW": (arb(0), face.s0, Q(sigma)),
        "SE": (u_max, face.s0, p_inner),
        "NE": (u_max, face.s1, p_inner),
        "NW": (arb(0), face.s1, Q(sigma)),
    }
    corner_signs: dict[str, str] = {}
    corner_map_cross_checks: dict[str, bool] = {}
    for label, (u_value, s_value, p_value) in corner_specs.items():
        transformed = chart_geometry(
            collar["chart"],
            collar["owner_target"],
            face.t0,
            sigma,
            u_value,
            arbq(s_value),
        )
        corner_signs[label] = strict_sign(transformed[active_kind][0])
        original = r186.factor_geometry(
            collar["chart"],
            collar["owner_target"],
            point_box(face, p_value, s_value, label),
        )
        checks = [
            bool(transformed[kind][0].overlaps(original[kind][0]))
            for kind in ("HPLUS", "HMINUS", "NX", "NY")
        ]
        require(all(checks), f"corner map equivalence:{row['row_id']}:{side}:{label}")
        corner_map_cross_checks[label] = all(checks)

    edge_specs = {
        "S": {
            "corners": ("SW", "SE"),
            "u_range": u_range,
            "s_range": arbq(face.s0),
            "u_center": u_center,
            "s_center": arbq(face.s0),
            "tangent_index": 0,
        },
        "E": {
            "corners": ("SE", "NE"),
            "u_range": u_max,
            "s_range": s_range,
            "u_center": u_max,
            "s_center": s_center,
            "tangent_index": 1,
        },
        "N": {
            "corners": ("NW", "NE"),
            "u_range": u_range,
            "s_range": arbq(face.s1),
            "u_center": u_center,
            "s_center": arbq(face.s1),
            "tangent_index": 0,
        },
        "W": {
            "corners": ("SW", "NW"),
            "u_range": arb(0),
            "s_range": s_range,
            "u_center": arb(0),
            "s_center": s_center,
            "tangent_index": 1,
        },
    }
    edge_rows: dict[str, dict[str, Any]] = {}
    for edge, spec in edge_specs.items():
        c0 = c0_profile(
            collar["chart"],
            collar["owner_target"],
            face.t0,
            sigma,
            spec["u_range"],
            spec["s_range"],
            spec["u_center"],
            spec["s_center"],
            active_kind,
        )
        edge_dual = chart_geometry(
            collar["chart"],
            collar["owner_target"],
            face.t0,
            sigma,
            spec["u_range"],
            spec["s_range"],
        )[active_kind]
        tangent_sign = strict_sign(
            edge_dual[1][spec["tangent_index"]]
        )
        lower, upper_label = spec["corners"]
        endpoint_signs = {
            corner_signs[lower],
            corner_signs[upper_label],
        }
        if c0["selected_sign"] in STRICT_SIGNS:
            require(
                corner_signs[lower] == c0["selected_sign"]
                and corner_signs[upper_label] == c0["selected_sign"],
                f"edge C0/corner consistency:{row['row_id']}:{side}:{edge}",
            )
            disposition = "STRICT_C0_ZERO_ABSENT"
        elif (
            tangent_sign in STRICT_SIGNS
            and endpoint_signs == STRICT_SIGNS
        ):
            disposition = UNIQUE_ZERO
        elif (
            tangent_sign in STRICT_SIGNS
            and len(endpoint_signs) == 1
            and "OVERWRAP" not in endpoint_signs
        ):
            disposition = "STRICT_MONOTONE_ZERO_ABSENT"
        elif "OVERWRAP" in endpoint_signs:
            disposition = "EDGE_ENDPOINT_SIGN_RESIDUAL"
        else:
            disposition = "EDGE_ZERO_SET_UNRESOLVED"
        edge_rows[edge] = {
            **c0,
            "tangent_axis": "u" if spec["tangent_index"] == 0 else "s",
            "tangent_derivative_sign": tangent_sign,
            "endpoint_corner_pair": f"{lower}|{upper_label}",
            "endpoint_sign_pair":
                f"{corner_signs[lower]}|{corner_signs[upper_label]}",
            "disposition": disposition,
        }

    bracketed_edges = sorted(
        edge
        for edge, evidence in edge_rows.items()
        if evidence["disposition"] == UNIQUE_ZERO
    )
    unresolved_edges = sorted(
        edge
        for edge, evidence in edge_rows.items()
        if (
            evidence["disposition"] != UNIQUE_ZERO
            and evidence["disposition"] not in ZERO_ABSENT
        )
    )
    all_edges_resolved = not unresolved_edges
    exactly_two_endpoints = len(bracketed_edges) == 2
    curve_normal_form = (
        inactive_strict
        and graph_axis is not None
        and all(value in STRICT_SIGNS for value in corner_signs.values())
        and all_edges_resolved
        and exactly_two_endpoints
    )
    graph_endpoint_edges = (
        ("W", "E")
        if graph_axis == "u"
        else ("S", "N") if graph_axis == "s" else ()
    )
    graph_endpoint_C0_signs = (
        [
            edge_rows[edge]["selected_sign"]
            for edge in graph_endpoint_edges
        ]
        if graph_endpoint_edges
        else []
    )
    strict_monotone_absent_normal_form = (
        inactive_strict
        and graph_axis is not None
        and all(value in STRICT_SIGNS for value in corner_signs.values())
        and all_edges_resolved
        and not bracketed_edges
        and len(set(graph_endpoint_C0_signs)) == 1
        and graph_endpoint_C0_signs[0] in STRICT_SIGNS
        and all(
            value == graph_endpoint_C0_signs[0]
            for value in corner_signs.values()
        )
    )
    require(
        not (
            curve_normal_form
            and strict_monotone_absent_normal_form
        ),
        "curve and absent normal forms are mutually exclusive",
    )
    face_level_resolved = (
        curve_normal_form or strict_monotone_absent_normal_form
    )
    if curve_normal_form:
        status = "UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE"
        residual_reason = None
        normal_form = "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
    elif strict_monotone_absent_normal_form:
        status = "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"
        residual_reason = None
        normal_form = "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"
    elif not inactive_strict:
        status = "STEREOGRAPHIC_FACE_RESIDUAL"
        residual_reason = "INACTIVE_FACTOR_C0_NOT_STRICT"
        normal_form = None
    elif graph_axis is None:
        status = "STEREOGRAPHIC_FACE_RESIDUAL"
        residual_reason = "NO_FULL_FACE_STRICT_GRAPH_DERIVATIVE"
        normal_form = None
    elif any(
        value not in STRICT_SIGNS for value in corner_signs.values()
    ):
        status = "STEREOGRAPHIC_FACE_RESIDUAL"
        residual_reason = "CORNER_SIGN_OVERWRAP"
        normal_form = None
    elif unresolved_edges:
        status = "STEREOGRAPHIC_FACE_RESIDUAL"
        residual_reason = "UNRESOLVED_BOUNDARY_EDGE"
        normal_form = None
    else:
        status = "STEREOGRAPHIC_FACE_RESIDUAL"
        residual_reason = "NO_ACCEPTED_CURVE_OR_ABSENT_NORMAL_FORM"
        normal_form = None

    evidence = {
        "leaf_row_id": row["row_id"],
        "occurrence_row_id": row["occurrence_row_id"],
        "origin_row_id": collar["origin_row_id"],
        "side": side,
        "p_endpoint": item["endpoint"],
        "sigma": sigma,
        "p_inner": str(p_inner),
        "u_max_squared": str(audit["u_max_squared"]),
        "u_upper_dyadic": str(u_upper),
        "exact_endpoint_map_checked": True,
        "exact_unit_circle_identity_coefficients":
            list(audit["symbolic_unit_identity_coefficients"]),
        "active_factor": active_kind,
        "inactive_factor": inactive_kind,
        "inactive_factor_C0": inactive_c0,
        "face_du_sign": face_du_sign,
        "face_ds_sign": face_ds_sign,
        "graph_axis": graph_axis,
        "corner_signs": corner_signs,
        "corner_map_cross_checks": corner_map_cross_checks,
        "edges": edge_rows,
        "bracketed_edges": bracketed_edges,
        "edge_pair": "|".join(bracketed_edges),
        "unresolved_edges": unresolved_edges,
        "graph_axis_endpoint_edges": list(graph_endpoint_edges),
        "graph_axis_endpoint_C0_signs": graph_endpoint_C0_signs,
        "boundary_unique_endpoint_count": len(bracketed_edges),
        "all_edges_zero_absent_or_unique_bracket": all_edges_resolved,
        "curve_and_absent_normal_forms_mutually_exclusive": True,
        "normal_form": normal_form,
        "face_level_resolved": face_level_resolved,
        "status": status,
        "residual_reason": residual_reason,
    }
    return evidence


def check_inputs() -> dict[str, Any]:
    require(
        Path(r189.__file__).resolve() == (HERE / ROUND189_SOURCE).resolve(),
        "Round189 module identity",
    )
    require(
        Path(r189.r188.__file__).resolve()
        == (HERE / ROUND188_SOURCE).resolve(),
        "Round188 module identity",
    )
    require(
        Path(r189.r188.r186.__file__).resolve()
        == (HERE / ROUND186_SOURCE).resolve(),
        "Round186 module identity",
    )
    r189.pinned_sha256(HERE / ROUND189_SOURCE, ROUND189_SOURCE_SHA256)
    pins = r189.check_inputs()
    require(
        pins["Round188_probe_source_sha256"] == ROUND188_SOURCE_SHA256,
        "Round188 source pin through Round189",
    )
    require(
        pins["Round186_probe_source_sha256"] == ROUND186_SOURCE_SHA256,
        "Round186 source pin through Round189",
    )
    return {
        **pins,
        "Round189_probe_source_sha256": ROUND189_SOURCE_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def check_round189_depth2(
    endpoint_faces: list[dict[str, Any]],
) -> dict[str, Any]:
    refinement = r189.refine_endpoint_faces(endpoint_faces, 2)
    require(
        digest(refinement) == EXPECTED_ROUND189_DEPTH2_REFINEMENT_SHA256,
        "Round189 depth2 full refinement result pin",
    )
    require(refinement["verdict"] == "PARTIAL", "Round189 depth2 verdict")
    require(
        refinement["input_original_face_count"] == 288
        and refinement["resolved_original_face_count"] == 32
        and refinement["residual_original_face_count"] == 256,
        "Round189 depth2 original-face census",
    )
    require(
        refinement["original_face_audit_rows_sha256"]
        == EXPECTED_ROUND189_DEPTH2_AUDIT_ROWS_SHA256,
        "Round189 depth2 audit-row digest",
    )
    require(
        refinement["exact_p_s_area"] == {
            "input": "1/655360",
            "resolved": "1/819200",
            "residual": "1/3276800",
            "conserved": True,
            "per_original_face_conserved": True,
        },
        "Round189 depth2 exact face area",
    )
    return {
        "refinement_result_sha256":
            EXPECTED_ROUND189_DEPTH2_REFINEMENT_SHA256,
        "verdict": refinement["verdict"],
        "input_original_face_count":
            refinement["input_original_face_count"],
        "resolved_original_face_count":
            refinement["resolved_original_face_count"],
        "residual_original_face_count":
            refinement["residual_original_face_count"],
        "original_face_audit_rows_sha256":
            refinement["original_face_audit_rows_sha256"],
        "exact_p_s_area": refinement["exact_p_s_area"],
        "no_Round189_child_is_promoted_here": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Round191 stereographic endpoint-chart feasibility "
            "probe; no output-path option and zero promotion."
        )
    )
    parser.parse_args()
    ctx.prec = 256

    pins = check_inputs()
    outgoing, collar_by_occurrence, _source = r189.load_scope()
    endpoint_faces, reconstruction = r189.reconstruct_endpoint_cohort(
        outgoing,
        collar_by_occurrence,
    )
    require(
        reconstruction["endpoint_residual_face_count"]
        == EXPECTED_ENDPOINT_FACES,
        "endpoint face census",
    )
    require(
        reconstruction["endpoint_residual_distinct_leaf_count"]
        == EXPECTED_ENDPOINT_LEAVES,
        "endpoint leaf census",
    )
    require(
        reconstruction["endpoint_residual_distinct_origin_count"]
        == EXPECTED_ENDPOINT_ORIGINS,
        "endpoint origin census",
    )
    require(
        reconstruction["endpoint_residual_p_endpoint_count"]
        == {
            "p=+1": EXPECTED_POSITIVE_ENDPOINT_FACES,
            "p=-1": EXPECTED_NEGATIVE_ENDPOINT_FACES,
        },
        "balanced p endpoint census",
    )
    require(
        reconstruction[
            "endpoint_residual_faces_on_two_sided_U_leaves"
        ]
        == EXPECTED_ENDPOINT_FACES_ON_TWO_SIDED_U_LEAVES,
        "endpoint cohort excludes U|U leaves",
    )
    round189_depth2 = check_round189_depth2(endpoint_faces)

    status_counts: Counter[str] = Counter()
    residual_reasons: Counter[str] = Counter()
    active_factors: Counter[str] = Counter()
    endpoint_signs: Counter[str] = Counter()
    face_sides: Counter[str] = Counter()
    graph_axes: Counter[str] = Counter()
    edge_pairs: Counter[str] = Counter()
    corner_patterns: Counter[str] = Counter()
    face_derivative_pairs: Counter[str] = Counter()
    edge_dispositions: Counter[str] = Counter()
    edge_tangent_signs: Counter[str] = Counter()
    inactive_C0_signs: Counter[str] = Counter()
    identity_coefficients: Counter[str] = Counter()
    evidence_rows: list[dict[str, Any]] = []
    residual_samples: list[dict[str, Any]] = []

    for index, item in enumerate(endpoint_faces, 1):
        evidence = transformed_arrangement(item)
        evidence_rows.append(evidence)
        status_counts[evidence["status"]] += 1
        if evidence["residual_reason"] is not None:
            residual_reasons[evidence["residual_reason"]] += 1
            if len(residual_samples) < 16:
                residual_samples.append(evidence)
        active_factors[evidence["active_factor"]] += 1
        endpoint_signs[evidence["p_endpoint"]] += 1
        face_sides[evidence["side"]] += 1
        graph_axes[str(evidence["graph_axis"])] += 1
        edge_pairs[evidence["edge_pair"]] += 1
        corner_patterns[
            "|".join(
                evidence["corner_signs"][name]
                for name in ("SW", "SE", "NE", "NW")
            )
        ] += 1
        face_derivative_pairs[
            evidence["face_du_sign"] + "|" + evidence["face_ds_sign"]
        ] += 1
        inactive_C0_signs[
            evidence["inactive_factor_C0"]["selected_sign"]
        ] += 1
        identity_coefficients[
            "|".join(
                str(value)
                for value in evidence[
                    "exact_unit_circle_identity_coefficients"
                ]
            )
        ] += 1
        for edge, row in evidence["edges"].items():
            edge_dispositions[f"{edge}:{row['disposition']}"] += 1
            edge_tangent_signs[
                f"{edge}:{row['tangent_derivative_sign']}"
            ] += 1
        if index % 50 == 0 or index == len(endpoint_faces):
            print(
                f"stereographic-chart {index}/{len(endpoint_faces)}",
                file=sys.stderr,
                flush=True,
            )

    curve_count = status_counts[
        "UNIQUE_TWO_ENDPOINT_STEREOGRAPHIC_FACTOR_CURVE"
    ]
    absent_count = status_counts[
        "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"
    ]
    resolved_count = curve_count + absent_count
    residual_count = EXPECTED_ENDPOINT_FACES - resolved_count
    require(
        resolved_count + residual_count == EXPECTED_ENDPOINT_FACES,
        "stereographic face conservation",
    )
    require(
        sum(endpoint_signs.values()) == EXPECTED_ENDPOINT_FACES
        and endpoint_signs["p=-1"] == endpoint_signs["p=+1"] == 144,
        "stereographic endpoint conservation",
    )
    require(
        len({row["leaf_row_id"] for row in evidence_rows})
        == EXPECTED_ENDPOINT_LEAVES,
        "stereographic leaf conservation",
    )
    require(
        len({row["origin_row_id"] for row in evidence_rows})
        == EXPECTED_ENDPOINT_ORIGINS,
        "stereographic origin conservation",
    )
    require(
        identity_coefficients == {"0|0|0": EXPECTED_ENDPOINT_FACES},
        "all unit-circle symbolic identities exact",
    )

    if residual_count == 0:
        verdict = "VALIDATED"
        verdict_reason = (
            "the smooth rational endpoint chart resolves all 288 endpoint "
            "faces as either a unique two-endpoint factor curve or a strict "
            "monotone active-factor absence, without p bisection"
        )
    elif resolved_count:
        verdict = "PARTIAL"
        verdict_reason = (
            "the endpoint chart resolves only part of the 288-face cohort "
            "under the strict edge and graph criteria"
        )
    else:
        verdict = "INVALIDATED"
        verdict_reason = (
            "the endpoint chart resolves none of the 288-face cohort under "
            "the strict edge and graph criteria"
        )

    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_STEREOGRAPHIC_ENDPOINT_CHART_PROBE",
        "question":
            "Can the rational stereographic circle chart replace endpoint "
            "p bisection and give a complete strict curve-or-absence "
            "boundary arrangement for the 288 Round188 p=+/-1 faces?",
        "verdict": verdict,
        "verdict_scope": "288-face feasibility subquestion only",
        "verdict_reason": verdict_reason,
        "input_chain": pins,
        "cohort_reconstruction": reconstruction,
        "Round189_depth2_reconstruction": round189_depth2,
        "chart_contract": {
            "coordinate_domain": "u>=0",
            "p_formula": "sigma*(1-u^2)/(1+u^2)",
            "rp_formula": "2*u/(1+u^2)",
            "u_max_formula":
                "sqrt((1-sigma*p_inner)/(1+sigma*p_inner))",
            "sigma_values": [-1, 1],
            "exact_p_endpoint_and_p_inner_mapping_checked_per_face": True,
            "exact_p_squared_plus_rp_squared_identity_checked_per_face":
                True,
            "algebraic_u_max_covered_by_least_192_bit_dyadic_upper":
                True,
            "corner_equivalence_with_original_Round186_geometry":
                "HPLUS,HMINUS,NX,NY checked at all four corners",
            "p_bisection_used": False,
            "accepted_face_normal_forms": [
                "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE",
                "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT",
            ],
            "accepted_face_normal_forms_mutually_exclusive": True,
        },
        "stereographic_arrangement": {
            "input_face_count": EXPECTED_ENDPOINT_FACES,
            "resolved_face_count": resolved_count,
            "residual_face_count": residual_count,
            "unique_two_endpoint_curve_count": curve_count,
            "strict_monotone_active_factor_absent_count": absent_count,
            "status_count": dict(sorted(status_counts.items())),
            "residual_reason_count":
                dict(sorted(residual_reasons.items())),
            "active_factor_count": dict(sorted(active_factors.items())),
            "p_endpoint_count": dict(sorted(endpoint_signs.items())),
            "face_side_count": dict(sorted(face_sides.items())),
            "selected_graph_axis_count": dict(sorted(graph_axes.items())),
            "unique_endpoint_edge_pair_count":
                dict(sorted(edge_pairs.items())),
            "corner_sign_pattern_count":
                dict(sorted(corner_patterns.items())),
            "full_face_du_ds_sign_pair_count":
                dict(sorted(face_derivative_pairs.items())),
            "inactive_factor_selected_C0_sign_count":
                dict(sorted(inactive_C0_signs.items())),
            "edge_disposition_count":
                dict(sorted(edge_dispositions.items())),
            "edge_tangential_derivative_sign_count":
                dict(sorted(edge_tangent_signs.items())),
            "symbolic_unit_identity_coefficient_count":
                dict(sorted(identity_coefficients.items())),
            "evidence_row_count": len(evidence_rows),
            "evidence_rows_sha256": digest(evidence_rows),
            "all_curve_faces_have_exactly_two_unique_boundary_endpoints":
                all(
                    (
                        row["boundary_unique_endpoint_count"] == 2
                        and row[
                            "all_edges_zero_absent_or_unique_bracket"
                        ]
                        and row["graph_axis"] in {"u", "s"}
                    )
                    for row in evidence_rows
                    if row["normal_form"]
                    == "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
                ),
            "all_absent_faces_have_same_sign_graph_endpoint_edges":
                all(
                    (
                        row["boundary_unique_endpoint_count"] == 0
                        and len(
                            set(row["graph_axis_endpoint_C0_signs"])
                        )
                        == 1
                        and row["graph_axis_endpoint_C0_signs"][0]
                        in STRICT_SIGNS
                    )
                    for row in evidence_rows
                    if row["normal_form"]
                    == "STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT"
                ),
            "residual_samples": residual_samples,
            "residual_sample_limit": 16,
        },
        "uncovered_tail": {
            "Round188_two_sided_U_leaf_count":
                EXPECTED_TWO_SIDED_U_LEAVES,
            "endpoint_cohort_faces_on_two_sided_U_leaves": 0,
            "two_sided_U_cross_t_ordering_processed_here": False,
            "wall_G_residual_leaf_count":
                EXPECTED_WALL_G_RESIDUAL_LEAVES,
            "wall_G_processed_here": False,
            "formal_half_open_edge_ownership_materialized": False,
            "side_specific_return_signatures_materialized": False,
            "independent_verifier_built": False,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "evidence_rows_emitted_as_attachment": False,
            "whole_leaf_credit_issued": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
            "required_next":
                "formal producer with complete evidence rows, half-open "
                "boundary ownership, side-specific return signatures, U|U "
                "cross-t ordering, wall-G tail, and an independent verifier",
        },
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
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
