#!/usr/bin/env python3
"""Independent replay verifier for the Round165 adaptive seam census.

The verifier does not import or execute the Round165 producer.  It rebuilds
the two pinned direct source-W atlases, reconstructs the 618 Round163 seam
parents, independently reruns the adaptive classifier, and requires canonical
equality with a fully reconstructed expected document.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge


ctx.prec = 192
HERE = Path(__file__).resolve().parent
PRODUCER = "cm2_round165_adaptive_typed_seam_census.py"
CERTIFICATE = (
    HERE / "cm2_round165_adaptive_typed_seam_census_certificate.json"
)
OUTPUT = (
    HERE / "cm2_round165_adaptive_typed_seam_census_verification.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round165.adaptive-typed-seam-census.prototype.v1"
)
SCHEMA = (
    "cm2.round165.adaptive-typed-seam-census.verification.prototype.v1"
)
FROZEN_OWNER = "W[1,0]"
SOURCE_CHARTS = ("W:E", "W:W", "W:N", "W:S")
DIRECT_CHARTS = ("W:E", "W:N")
MAX_EXTRA_DEPTH = 14
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270"
)
PINS = {
    PRODUCER:
        "95bdbe3fc8d1d26512d8469a0e9382a3e977d5606375ed2729877c9f1ac8e012",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
}
DEPENDENCY_PINS = {
    key: value for key, value in PINS.items() if key != PRODUCER
}
EXPECTED_CANDIDATE_DIGESTS = {
    "W:E": "ebeeae12ba192d7808031ebf4be3537fb49e73e17295404adcad371045e7c2e7",
    "W:N": "4719c19ccb8c63288e8815c4b8961f64d9d096dd4377641acafbec59c00769e5",
}
ROUND163_RESULT_SHA256 = (
    "d64b5fab6b599a8fb4d6665c8abb902d79f86afd0370610845a5f7558d848102"
)
ROUND163_VERIFICATION_RESULT_SHA256 = (
    "183b30155016229f27ba35293ad98d4b1b779af19c84dab5fec583862c8ef8a9"
)
ROUND164_RESULT_SHA256 = (
    "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
)
ROUND164_VERIFICATION_RESULT_SHA256 = (
    "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
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


def strict_load_raw(raw: bytes) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "encoding",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "duplicate key")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, "top object")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


def check_chain() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    require(
        Path(atlas.__file__).resolve()
        == (HERE / "cm2_gate3_eight_cell_symmetry_atlas_cert.py").resolve(),
        "atlas identity",
    )
    require(
        Path(base.__file__).resolve()
        == (HERE / "cm2_gate3_candidate_first_hit_cert.py").resolve(),
        "base identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    prior = strict_load(
        HERE / "cm2_round163_outgoing_chart_pruning_certificate.json"
    )
    prior_verification = strict_load(
        HERE / "cm2_round163_outgoing_chart_pruning_verification.json"
    )
    context = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
    )
    context_verification = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_verification.json"
    )
    ownership = strict_load(
        HERE / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
    )
    require(
        prior["result_sha256"] == ROUND163_RESULT_SHA256
        and prior_verification["result_sha256"]
        == ROUND163_VERIFICATION_RESULT_SHA256
        and prior_verification["result"]["status"] == "PASS"
        and prior_verification["result"]["certificate_result_sha256"]
        == prior["result_sha256"],
        "Round163 chain",
    )
    require(
        context["schema"]
        == "cm2.round164.dimension-safe-tangency-graph-typing.v2"
        and context["result_sha256"] == ROUND164_RESULT_SHA256
        and context["result"]["tangency_graph_typing"][
            "ambient_parent_leaf_count"
        ] == 32
        and context["result"]["ambient_frozen_prefix_census"][
            "new_full_dimensional_ambient_leaf_exclusion_count"
        ] == 0
        and context["result"]["ambient_frozen_prefix_census"][
            "remaining_ambient_unresolved_leaf_count"
        ] == 39348
        and context_verification["result_sha256"]
        == ROUND164_VERIFICATION_RESULT_SHA256
        and context_verification["result"]["status"] == "PASS"
        and context_verification["result"]["certificate_result_sha256"]
        == context["result_sha256"],
        "Round164-v2 chain",
    )
    require(
        ownership["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and ownership["verdict"]["rectangular_bulk_seam_quotient"]
        == "CERTIFIED"
        and ownership["result"]["scope_limits"][
            "ownership_rule_applies_to_analytic_strata"
        ] is True
        and ownership["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True
        and ownership["result"]["unique_half_open_owner_rule"][
            "diagonal_tie"
        ] == "E or W owns; N or S excludes",
        "analytic seam ownership",
    )
    return (
        prior,
        prior_verification,
        context,
        context_verification,
        ownership,
    )


TARGET_MAP = {target.target_id: target for target in base.TARGETS}


def root_from_geometry(
    geometry: tuple[arb, arb, arb, arb, arb, arb],
    target_id: str,
) -> atlas.RootRecord:
    qx, qy, ux, uy, s, _cp = geometry
    target = TARGET_MAP[target_id]
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return atlas.RootRecord(
            target_id, "no_real_intersection", ell, discriminant,
            None, None, transverse,
        )
    if not bool(discriminant > 0):
        return atlas.RootRecord(
            target_id, "unresolved_discriminant", ell, discriminant,
            None, None, transverse,
        )
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    classification = (
        "intersection_behind"
        if bool(far < 0)
        else (
            "strict_future_root"
            if bool(near > 0)
            else "unresolved_root_sign"
        )
    )
    return atlas.RootRecord(
        target_id, classification, ell, discriminant,
        near, far, transverse,
    )


def fast_build_atlas(chart_id: str) -> list[atlas.Leaf]:
    candidate_ids = tuple(base.candidate_ids(chart_id))
    require(
        digest(list(candidate_ids)) == EXPECTED_CANDIDATE_DIGESTS[chart_id],
        f"candidate digest:{chart_id}",
    )
    old_ids = base.candidate_ids
    old_target = base.target_by_id
    old_records = atlas.records

    def cached_ids(requested: str) -> tuple[str, ...]:
        require(requested == chart_id, "cached chart")
        return candidate_ids

    def cached_target(target_id: str) -> Any:
        return TARGET_MAP[target_id]

    def cached_records(
        requested: str, box: atlas.AtlasBox,
    ) -> list[atlas.RootRecord]:
        require(requested == chart_id, "records chart")
        geometry = atlas.geometry(requested, box)
        return [
            root_from_geometry(geometry, target_id)
            for target_id in candidate_ids
        ]

    base.candidate_ids = cached_ids  # type: ignore[assignment]
    base.target_by_id = cached_target  # type: ignore[assignment]
    atlas.records = cached_records  # type: ignore[assignment]
    try:
        return atlas.build_atlas(chart_id)
    finally:
        atlas.records = old_records  # type: ignore[assignment]
        base.target_by_id = old_target  # type: ignore[assignment]
        base.candidate_ids = old_ids  # type: ignore[assignment]


def build_atlases(workers: int) -> dict[str, list[atlas.Leaf]]:
    if workers == 1:
        direct = {
            chart_id: fast_build_atlas(chart_id)
            for chart_id in DIRECT_CHARTS
        }
    else:
        with ProcessPoolExecutor(max_workers=2) as pool:
            values = list(pool.map(fast_build_atlas, DIRECT_CHARTS))
        direct = dict(zip(DIRECT_CHARTS, values, strict=True))
    return {
        **direct,
        "W:W": [
            atlas.reflect_leaf("W:E", "vertical", leaf)
            for leaf in direct["W:E"]
        ],
        "W:S": [
            atlas.reflect_leaf("W:N", "horizontal", leaf)
            for leaf in direct["W:N"]
        ],
    }


def box_row(box: atlas.AtlasBox) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
    }


def box_volume(box: atlas.AtlasBox) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def row_volume(row: dict[str, Any]) -> Q:
    box = row["box"]
    return (
        (Q(box["t"][1]) - Q(box["t"][0]))
        * (Q(box["p"][1]) - Q(box["p"][0]))
        * (Q(box["s"][1]) - Q(box["s"][0]))
    )


def source_frame(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[arb, arb, arb, arb, arb, arb, arb, arb]:
    _source, cell = chart_id.split(":")
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    rt = ge.sqrt_one_minus_square(box.t0, box.t1)
    rp = ge.sqrt_one_minus_square(box.p0, box.p1)
    require(bool(rt > 0), "source radical")
    if cell == "E":
        nx, ny, dnx, dny = rt, t, -t / rt, arb(1)
    elif cell == "W":
        nx, ny, dnx, dny = -rt, t, t / rt, arb(1)
    elif cell == "N":
        nx, ny, dnx, dny = t, rt, arb(1), -t / rt
    elif cell == "S":
        nx, ny, dnx, dny = t, -rt, arb(1), t / rt
    else:  # pragma: no cover
        raise ValueError(cell)
    ux = rp * nx - p * ny
    uy = rp * ny + p * nx
    dux = rp * dnx - p * dny
    duy = rp * dny + p * dnx
    return nx, ny, dnx, dny, ux, uy, dux, duy


def subbox(
    box: atlas.AtlasBox,
    t_value: Q | None = None,
    p_value: Q | None = None,
) -> atlas.AtlasBox:
    t0, t1 = (
        (box.t0, box.t1)
        if t_value is None
        else (t_value, t_value)
    )
    p0, p1 = (
        (box.p0, box.p1)
        if p_value is None
        else (p_value, p_value)
    )
    return atlas.AtlasBox(
        t0, t1, p0, p1, box.s0, box.s1, box.depth, box.path
    )


def round163_contact(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[str | None, arb, arb, arb, arb]:
    geometry = atlas.geometry(chart_id, box)
    qx, qy, ux, uy, s, _cp = geometry
    record = root_from_geometry(geometry, FROZEN_OWNER)
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        "Round163 owner root",
    )
    target = TARGET_MAP[FROZEN_OWNER]
    cx, cy = base.target_center(target, s)
    radius = base.arbq(base.RADIUS["W"])
    nx = (qx + record.near * ux - cx) / radius
    ny = (qy + record.near * uy - cy) / radius
    tests = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, nx, ny, first, second
    return None, nx, ny, nx, ny


def tight_contact(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[str | None, arb, arb, arb, arb, arb, arb]:
    nx0, ny0, _a, _b, ux, uy, _c, _d = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    dx, dy = arb(1) - radius * nx0, -radius * ny0
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    discriminant = radius * radius - transverse * transverse
    require(bool(discriminant > 0), "tight discriminant")
    radical = discriminant.sqrt()
    near = ell - radical
    require(bool(near > 0), "tight near root")
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    tests = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return cell, nx, ny, first, second, near, discriminant
    return None, nx, ny, nx, ny, near, discriminant


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


SEAMS = {
    "NW": {
        "signs": (-1, 1),
        "adjacent": "N",
        "margin": lambda nx, ny: nx + ny,
        "other": lambda nx, ny: nx - ny,
    },
    "SW": {
        "signs": (-1, -1),
        "adjacent": "S",
        "margin": lambda nx, ny: nx - ny,
        "other": lambda nx, ny: nx + ny,
    },
}


def seam_quantities(
    chart_id: str, box: atlas.AtlasBox, seam_id: str,
) -> dict[str, arb]:
    data = SEAMS[seam_id]
    a = base.arbq(Q(1, 2)).sqrt()
    mx = data["signs"][0] * a
    my = data["signs"][1] * a
    nx, ny, dnx, dny, ux, uy, dux, duy = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    dx = arb(1) + radius * mx - radius * nx
    dy = radius * my - radius * ny
    ddx, ddy = -radius * dnx, -radius * dny
    forward = ux * dx + uy * dy
    rp = ge.sqrt_one_minus_square(box.p0, box.p1)
    return {
        "H": ux * dy - uy * dx,
        "forward": forward,
        "inward": -(ux * mx + uy * my),
        "dp": -forward / rp,
        "dt": dux * dy - duy * dx + ux * ddy - uy * ddx,
    }


def corner_H(
    chart_id: str, box: atlas.AtlasBox, seam_id: str,
) -> list[arb]:
    return [
        seam_quantities(
            chart_id,
            subbox(box, t_value=t_value, p_value=p_value),
            seam_id,
        )["H"]
        for t_value in (box.t0, box.t1)
        for p_value in (box.p0, box.p1)
    ]


def typed_seam(
    chart_id: str, box: atlas.AtlasBox, nx: arb, ny: arb,
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for seam_id, data in SEAMS.items():
        margin = data["margin"](nx, ny)
        other = data["other"](nx, ny)
        if strict_sign(margin) != 0 or not bool(other < 0):
            continue
        q = seam_quantities(chart_id, box, seam_id)
        if not (
            bool(q["forward"] > 0)
            and bool(q["inward"] > 0)
            and bool(q["dp"] < 0)
        ):
            continue
        lower = seam_quantities(
            chart_id, subbox(box, p_value=box.p0), seam_id
        )["H"]
        upper = seam_quantities(
            chart_id, subbox(box, p_value=box.p1), seam_id
        )["H"]
        corners = corner_H(chart_id, box, seam_id)
        signs = [strict_sign(value) for value in corners]
        full = bool(lower > 0) and bool(upper < 0)
        dt_sign = strict_sign(q["dt"])
        clipped = dt_sign != 0 and 1 in signs and -1 in signs
        if not (full or clipped):
            continue
        predicate = (
            "n_x+n_y" if seam_id == "NW" else "n_x-n_y"
        )
        candidates.append({
            "seam_id": seam_id,
            "adjacent_outgoing_chart": data["adjacent"],
            "graph_kind":
                "FULL_P_GRAPH" if full else "MONOTONE_CLIPPED_GRAPH",
            "normal_equation": predicate + "=0",
            "target_normal": (
                "(-1,+1)/sqrt(2)"
                if seam_id == "NW"
                else "(-1,-1)/sqrt(2)"
            ),
            "W_open_side": predicate + "<0",
            "mismatch_open_side": (
                "n_x+n_y>0 -> N"
                if seam_id == "NW"
                else "n_x-n_y>0 -> S"
            ),
            "diagonal_half_open_owner": "W",
            "ambient_parameter_dimension": 3,
            "graph_dimension": 2,
            "whole_parent_leaf_excluded": False,
            "three_stratum_partition_materialized": True,
            "strata": [
                {
                    "stratum": "W_OPEN_SIDE",
                    "dimension": 3,
                    "predicate": predicate + "<0",
                    "outgoing_chart": "W",
                    "frozen_prefix_disposition":
                        "PREFIX_STAGE_ONE_MATCH_OPEN_REGION",
                },
                {
                    "stratum": "ADJACENT_OPEN_SIDE",
                    "dimension": 3,
                    "predicate": predicate + ">0",
                    "outgoing_chart": data["adjacent"],
                    "frozen_prefix_disposition":
                        "OUTGOING_CHART_MISMATCH_OPEN_REGION",
                },
                {
                    "stratum": "DIAGONAL_GRAPH",
                    "dimension": 2,
                    "predicate": predicate + "=0",
                    "outgoing_chart": "W",
                    "frozen_prefix_disposition":
                        "PREFIX_STAGE_ONE_MATCH_HALF_OPEN_SEAM",
                },
            ],
            "H_lower_p_face_arb": str(lower),
            "H_upper_p_face_arb": str(upper),
            "H_lower_p_face_sign": (
                "POSITIVE"
                if strict_sign(lower) > 0
                else (
                    "NEGATIVE"
                    if strict_sign(lower) < 0
                    else "UNRESOLVED"
                )
            ),
            "H_upper_p_face_sign": (
                "POSITIVE"
                if strict_sign(upper) > 0
                else (
                    "NEGATIVE"
                    if strict_sign(upper) < 0
                    else "UNRESOLVED"
                )
            ),
            "H_corner_signs": signs,
            "H_derivative_p_arb": str(q["dp"]),
            "H_derivative_t_arb": str(q["dt"]),
            "H_derivative_p_sign": "NEGATIVE",
            "H_derivative_t_sign": (
                "POSITIVE"
                if dt_sign > 0
                else (
                    "NEGATIVE"
                    if dt_sign < 0
                    else "UNUSED_OR_UNRESOLVED"
                )
            ),
            "forward_margin_arb": str(q["forward"]),
            "incoming_margin_arb": str(q["inward"]),
            "other_diagonal_margin_arb": str(other),
            "forward_margin_sign": "POSITIVE",
            "incoming_margin_sign": "POSITIVE",
            "other_diagonal_margin_sign": "NEGATIVE",
            "arb_display_outers_are_not_sign_witnesses": True,
        })
    return candidates[0] if len(candidates) == 1 else None


def H_separated(
    chart_id: str, box: atlas.AtlasBox, nx: arb, ny: arb,
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for seam_id, data in SEAMS.items():
        margin = data["margin"](nx, ny)
        other = data["other"](nx, ny)
        if strict_sign(margin) != 0 or not bool(other < 0):
            continue
        q = seam_quantities(chart_id, box, seam_id)
        dt_sign = strict_sign(q["dt"])
        if not (
            bool(q["forward"] > 0)
            and bool(q["inward"] > 0)
            and bool(q["dp"] < 0)
            and dt_sign != 0
        ):
            continue
        corners = corner_H(chart_id, box, seam_id)
        signs = [strict_sign(value) for value in corners]
        if not (
            all(sign == 1 for sign in signs)
            or all(sign == -1 for sign in signs)
        ):
            continue
        H_sign = signs[0]
        outgoing = (
            ("W" if H_sign > 0 else "N")
            if seam_id == "NW"
            else ("W" if H_sign < 0 else "S")
        )
        candidates.append({
            "seam_id": seam_id,
            "outgoing_chart": outgoing,
            "H_sign": H_sign,
            "H_corner_signs": signs,
            "H_corner_values_arb": [str(value) for value in corners],
            "H_derivative_p_arb": str(q["dp"]),
            "H_derivative_t_arb": str(q["dt"]),
            "H_derivative_p_sign": "NEGATIVE",
            "H_derivative_t_sign":
                "POSITIVE" if dt_sign > 0 else "NEGATIVE",
            "forward_margin_arb": str(q["forward"]),
            "incoming_margin_arb": str(q["inward"]),
            "other_diagonal_margin_arb": str(other),
            "forward_margin_sign": "POSITIVE",
            "incoming_margin_sign": "POSITIVE",
            "other_diagonal_margin_sign": "NEGATIVE",
            "arb_display_outers_are_not_sign_witnesses": True,
            "sign_transfer_identity": (
                "sign(n_x+n_y)=-sign(H_NW)"
                if seam_id == "NW"
                else "sign(n_x-n_y)=sign(H_SW)"
            ),
        })
    return candidates[0] if len(candidates) == 1 else None


def split_box(box: atlas.AtlasBox) -> tuple[atlas.AtlasBox, atlas.AtlasBox]:
    tw = (box.t1 - box.t0) / (atlas.T_UPPER - atlas.T_LOWER)
    pw = (box.p1 - box.p0) / (atlas.P_UPPER - atlas.P_LOWER)
    depth = box.depth + 1
    if tw >= pw:
        middle = (box.t0 + box.t1) / 2
        return (
            atlas.AtlasBox(
                box.t0, middle, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "t0",
            ),
            atlas.AtlasBox(
                middle, box.t1, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "t1",
            ),
        )
    middle = (box.p0 + box.p1) / 2
    return (
        atlas.AtlasBox(
            box.t0, box.t1, box.p0, middle, box.s0, box.s1,
            depth, box.path + "p0",
        ),
        atlas.AtlasBox(
            box.t0, box.t1, middle, box.p1, box.s0, box.s1,
            depth, box.path + "p1",
        ),
    )


def terminal(
    parent_key: str,
    chart_id: str,
    box: atlas.AtlasBox,
    extra_depth: int,
) -> dict[str, Any] | None:
    cell, nx, ny, first, second, near, discriminant = tight_contact(
        chart_id, box
    )
    common = {
        "parent_leaf_key": parent_key,
        "leaf_key": f"{chart_id}:{box.path}",
        "chart_id": chart_id,
        "extra_depth": extra_depth,
        "box": box_row(box),
    }
    if cell is not None:
        return {
            **common,
            "classification": (
                "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
                if cell == "W"
                else "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
            ),
            "outgoing_chart": cell,
            "strict_margin_one_arb": str(first),
            "strict_margin_two_arb": str(second),
        }
    separated = H_separated(chart_id, box, nx, ny)
    if separated is not None:
        cell = separated["outgoing_chart"]
        return {
            **common,
            "classification": (
                "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
                if cell == "W"
                else "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
            ),
            "outgoing_chart": cell,
            "monotone_H_separator": separated,
        }
    seam = typed_seam(chart_id, box, nx, ny)
    if seam is not None:
        return {
            **common,
            "classification": "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES",
            "outgoing_chart": None,
            "owner_root_arb": str(near),
            "owner_discriminant_arb": str(discriminant),
            "typed_seam": seam,
        }
    return None


def refine(
    chart_id: str,
    parent: atlas.Leaf,
) -> list[dict[str, Any]]:
    parent_key = f"{chart_id}:{parent.box.path}"
    pending = [(parent.box, 0)]
    rows: list[dict[str, Any]] = []
    while pending:
        box, extra_depth = pending.pop()
        row = terminal(parent_key, chart_id, box, extra_depth)
        if row is not None:
            rows.append(row)
        elif extra_depth >= MAX_EXTRA_DEPTH:
            (
                _cell, nx, ny, _first, _second, near, discriminant,
            ) = tight_contact(chart_id, box)
            rows.append({
                "parent_leaf_key": parent_key,
                "leaf_key": f"{chart_id}:{box.path}",
                "chart_id": chart_id,
                "extra_depth": extra_depth,
                "box": box_row(box),
                "classification": "ADAPTIVE_DEPTH_LIMIT_UNRESOLVED",
                "outgoing_chart": None,
                "normal_x_arb": str(nx),
                "normal_y_arb": str(ny),
                "owner_root_arb": str(near),
                "owner_discriminant_arb": str(discriminant),
            })
        else:
            left, right = split_box(box)
            pending.append((right, extra_depth + 1))
            pending.append((left, extra_depth + 1))
    return sorted(rows, key=lambda row: row["leaf_key"])


def round163_row(chart_id: str, leaf: atlas.Leaf) -> dict[str, Any]:
    cell, nx, ny, first, second = round163_contact(chart_id, leaf.box)
    if cell is None:
        disposition = "OUTGOING_CHART_SEAM_UNRESOLVED"
        first, second = nx, ny
    elif cell == "W":
        disposition = "PREFIX_STAGE_ONE_MATCH"
    else:
        disposition = "EARLIEST_PREFIX_EXCLUDED_OUTGOING_CHART_MISMATCH"
    return {
        "leaf_key": f"{chart_id}:{leaf.box.path}",
        "owner": FROZEN_OWNER,
        "outgoing_chart": cell,
        "disposition": disposition,
        "strict_margin_one_arb": str(first),
        "strict_margin_two_arb": str(second),
    }


def reconstruct_inputs(
    prior: dict[str, Any],
    atlases: dict[str, list[atlas.Leaf]],
) -> tuple[
    dict[str, list[atlas.Leaf]],
    list[dict[str, Any]],
]:
    prior_charts = {
        row["chart_id"]: row
        for row in prior["result"]["outgoing_chart_pruning"]["charts"]
    }
    inputs: dict[str, list[atlas.Leaf]] = {}
    replay_rows: list[dict[str, Any]] = []
    for chart_id in SOURCE_CHARTS:
        owner_leaves = [
            leaf for leaf in atlases[chart_id]
            if leaf.classification == "unique_first"
            and leaf.owner_target == FROZEN_OWNER
        ]
        require(
            len(owner_leaves)
            == prior_charts[chart_id]["owner_match_leaf_count"],
            f"owner replay:{chart_id}",
        )
        rows = [
            round163_row(chart_id, leaf)
            for leaf in sorted(owner_leaves, key=lambda item: item.box.path)
        ]
        require(
            digest(rows)
            == prior_charts[chart_id]["disposition_rows_sha256"],
            f"Round163 chart digest:{chart_id}",
        )
        replay_rows.extend(rows)
        unresolved = {
            row["leaf_key"]
            for row in rows
            if row["disposition"] == "OUTGOING_CHART_SEAM_UNRESOLVED"
        }
        inputs[chart_id] = [
            leaf for leaf in owner_leaves
            if f"{chart_id}:{leaf.box.path}" in unresolved
        ]
    require(
        len(replay_rows) == 1176
        and digest(replay_rows)
        == prior["result"]["outgoing_chart_pruning"][
            "all_disposition_rows_sha256"
        ],
        "Round163 all-row digest",
    )
    return inputs, replay_rows


def build_expected(workers: int) -> dict[str, Any]:
    (
        prior,
        prior_verification,
        context,
        context_verification,
        ownership,
    ) = check_chain()
    atlases = build_atlases(workers)
    inputs, replay_rows = reconstruct_inputs(prior, atlases)
    input_leaves = [
        (chart_id, leaf)
        for chart_id in SOURCE_CHARTS
        for leaf in inputs[chart_id]
    ]
    require(len(input_leaves) == 618, "input count")
    input_rows = [
        {
            "leaf_key": f"{chart_id}:{leaf.box.path}",
            "chart_id": chart_id,
            "box": box_row(leaf.box),
        }
        for chart_id, leaf in input_leaves
    ]
    terminal_rows = [
        row
        for chart_id, leaf in input_leaves
        for row in refine(chart_id, leaf)
    ]
    terminal_rows.sort(key=lambda row: row["leaf_key"])

    counts: dict[str, int] = {}
    volumes: dict[str, Q] = {}
    charts: dict[str, dict[str, int]] = {
        chart_id: {} for chart_id in SOURCE_CHARTS
    }
    for row in terminal_rows:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1
        volumes[classification] = (
            volumes.get(classification, Q(0)) + row_volume(row)
        )
        chart_counts = charts[row["chart_id"]]
        chart_counts[classification] = (
            chart_counts.get(classification, 0) + 1
        )
    input_volume = sum(
        (box_volume(leaf.box) for _chart, leaf in input_leaves), Q(0)
    )
    require(sum(volumes.values(), Q(0)) == input_volume, "volume")

    typed_rows = [
        row for row in terminal_rows
        if row["classification"] == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
    ]
    typed_by_seam: dict[str, int] = {}
    typed_by_kind: dict[str, int] = {}
    for row in typed_rows:
        seam_id = row["typed_seam"]["seam_id"]
        kind = row["typed_seam"]["graph_kind"]
        typed_by_seam[seam_id] = typed_by_seam.get(seam_id, 0) + 1
        typed_by_kind[kind] = typed_by_kind.get(kind, 0) + 1

    rows_by_parent: dict[str, list[dict[str, Any]]] = {}
    for row in terminal_rows:
        rows_by_parent.setdefault(row["parent_leaf_key"], []).append(row)
    require(len(rows_by_parent) == 618, "parent registry")
    parent_counts = {
        "WHOLE_PARENT_OUTGOING_CHART_MISMATCH": 0,
        "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH": 0,
        "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION": 0,
        "PARENT_WITH_DEPTH_LIMIT_RESIDUAL": 0,
    }
    for rows in rows_by_parent.values():
        classes = {row["classification"] for row in rows}
        if "ADAPTIVE_DEPTH_LIMIT_UNRESOLVED" in classes:
            key = "PARENT_WITH_DEPTH_LIMIT_RESIDUAL"
        elif "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES" in classes:
            key = "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION"
        elif all(row["outgoing_chart"] == "W" for row in rows):
            key = "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH"
        else:
            require(
                all(
                    row["outgoing_chart"] in {"E", "N", "S"}
                    for row in rows
                ),
                "mixed parent",
            )
            key = "WHOLE_PARENT_OUTGOING_CHART_MISMATCH"
        parent_counts[key] += 1
    require(sum(parent_counts.values()) == 618, "parent counts")

    mismatch = sum(
        counts.get(key, 0)
        for key in (
            "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
            "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
        )
    )
    match = sum(
        counts.get(key, 0)
        for key in (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
        )
    )
    typed = len(typed_rows)
    unresolved = counts.get("ADAPTIVE_DEPTH_LIMIT_UNRESOLVED", 0)
    prior_combined = prior["result"]["combined_frozen_prefix_census"]
    require(
        prior_combined["combined_recordwise_excluded_leaf_count"] == 37480
        and prior_combined["remaining_leaf_count"] == 39348,
        "Round163 baseline",
    )
    untouched = prior_combined["remaining_leaf_count"] - 618
    refined_total = 76828 - 618 + len(terminal_rows)
    refined_excluded = 37480 + mismatch
    refined_live = untouched + match + typed + unresolved
    require(refined_excluded + refined_live == refined_total, "ledger")

    result = {
        "status": (
            "ROUND165_ADAPTIVE_TYPED_SEAM_PROTOTYPE__"
            + (
                "ALL_618_INPUTS_RECTANGULAR_OR_TYPED_GRAPH_RESOLVED"
                if unresolved == 0
                else "DEPTH_LIMIT_RESIDUAL_REMAINS"
            )
        ),
        "frozen_prefix": {
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": "W",
        },
        "mathematical_classifier": {
            "same_colour_relative_centre": ["1", "0"],
            "same_colour_translation_parameter_cancels_exactly": True,
            "seam_function":
                "H_m=cross(u,(1,0)+R_W*m-R_W*n_source)",
            "seam_equivalence":
                "H_m=0 iff the forward incoming near-contact normal equals m",
            "strict_p_derivative_identity":
                "partial_p H_m=-dot(u,D_m)/sqrt(1-p^2)<0",
            "monotone_no_zero_separator":
                "fixed-sign partials and four same strict corner signs",
            "seam_to_normal_sign_transfer": {
                "NW": "sign(n_x+n_y)=-sign(H_NW)",
                "SW": "sign(n_x-n_y)=sign(H_SW)",
            },
            "accepted_graph_kinds": [
                "FULL_P_GRAPH",
                "MONOTONE_CLIPPED_GRAPH",
            ],
            "typed_collar_is_not_a_whole_leaf_exclusion": True,
            "arb_display_outers_are_not_used_as_sign_witnesses": True,
            "typed_collar_partition":
                "{diagonal margin<0} union {=0} union {>0}",
            "diagonal_half_open_owner": "W",
            "diagonal_half_open_owner_source":
                "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json",
            "pinned_rule_applies_to_analytic_strata": ownership[
                "result"
            ]["scope_limits"]["ownership_rule_applies_to_analytic_strata"],
        },
        "adaptive_seam_census": {
            "input_parent_leaf_count": len(input_leaves),
            "input_by_chart": {
                chart_id: len(inputs[chart_id])
                for chart_id in SOURCE_CHARTS
            },
            "input_rows_sha256": digest(input_rows),
            "input_rational_volume": str(input_volume),
            "maximum_extra_depth_allowed": MAX_EXTRA_DEPTH,
            "maximum_extra_depth_used": max(
                row["extra_depth"] for row in terminal_rows
            ),
            "terminal_record_count": len(terminal_rows),
            "terminal_classification_counts": counts,
            "terminal_classification_rational_volumes": {
                key: str(value) for key, value in sorted(volumes.items())
            },
            "terminal_counts_by_source_chart": charts,
            "input_parent_resolution_counts": parent_counts,
            "typed_graph_count_by_seam": typed_by_seam,
            "typed_graph_count_by_kind": typed_by_kind,
            "strict_mismatch_rectangle_count": mismatch,
            "strict_match_rectangle_count": match,
            "typed_graph_collar_count": typed,
            "typed_full_dimensional_W_open_side_count": typed,
            "typed_full_dimensional_mismatch_open_side_count": typed,
            "typed_codimension_one_half_open_W_graph_count": typed,
            "typed_collar_whole_leaf_exclusion_count": 0,
            "adaptive_depth_limit_unresolved_count": unresolved,
            "all_618_inputs_semantically_chart_typed": unresolved == 0,
            "terminal_rows_sha256": digest(terminal_rows),
            "terminal_rows": terminal_rows,
        },
        "refined_recordwise_census": {
            "round163_total_source_W_records": 76828,
            "round163_seam_parent_records_replaced": 618,
            "round163_excluded_record_baseline": 37480,
            "round163_remaining_record_baseline": 39348,
            "untouched_remaining_parent_records": untouched,
            "new_strict_mismatch_child_rectangles": mismatch,
            "typed_collars_not_counted_as_whole_record_exclusions": typed,
            "typed_analytic_strata_not_added_to_rectangular_record_count":
                True,
            "refined_live_records_is_conservative_rectangle_or_collar_count":
                True,
            "refined_total_records": refined_total,
            "refined_excluded_records": refined_excluded,
            "refined_live_records": refined_live,
        },
        "round164_noninheritance": {
            "dimension_safe_schema": context["schema"],
            "dimension_safe_certificate_result_sha256":
                context["result_sha256"],
            "dimension_safe_verification_result_sha256":
                context_verification["result_sha256"],
            "tangency_parent_leaf_count": context["result"][
                "tangency_graph_typing"
            ]["ambient_parent_leaf_count"],
            "whole_tangency_parent_leaf_exclusions_inherited": 0,
            "reason":
                "typing a tangency graph does not classify its off-graph bulk",
            "combined_exclusion_baseline_remains": 37480,
            "combined_remaining_baseline_before_Round165_refinement": 39348,
        },
        "provenance": {
            "dependency_sha256": DEPENDENCY_PINS,
            "round163_result_sha256": prior["result_sha256"],
            "round163_verification_result_sha256":
                prior_verification["result_sha256"],
            "round163_all_1176_rows_replayed": True,
            "round163_all_rows_sha256": digest(replay_rows),
            "direct_source_W_atlases_replayed_at_192_bits": True,
            "candidate_registry_digests_checked_before_local_cache":
                EXPECTED_CANDIDATE_DIGESTS,
            "local_cache_changes_no_dependency_file": True,
            "analytic_seam_owner_manifest_verdict": {
                "eight_chart_seam_ownership": ownership["verdict"][
                    "eight_chart_seam_ownership"
                ],
                "rectangular_bulk_seam_quotient": ownership["verdict"][
                    "rectangular_bulk_seam_quotient"
                ],
            },
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "recut any Round165 depth-limit seam residual; resolve the "
            "off-graph bulk of all 32 Round164 tangency parents; then "
            "subdivide the 38,180 outside-W:W multi-candidate leaves"
        ),
    }
    return {
        "schema": CERTIFICATE_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def exact_key_tree(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type:{path}")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"keys:{path}")
        for key in expected:
            exact_key_tree(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"list length:{path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            exact_key_tree(left, right, f"{path}[{index}]")


def validate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    exact_key_tree(document, expected)
    require(document["schema"] == CERTIFICATE_SCHEMA, "schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "result digest",
    )
    require(
        document["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "frozen result digest",
    )
    require(canonical(document) == canonical(expected), "expected document")


def resigned(
    document: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    mutate(candidate)
    candidate["result_sha256"] = digest(candidate["result"])
    return candidate


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    rows = document["result"]["adaptive_seam_census"]["terminal_rows"]
    typed_index = next(
        index for index, row in enumerate(rows)
        if row["classification"] == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
    )
    monotone_index = next(
        index for index, row in enumerate(rows)
        if row["classification"].startswith("MONOTONE_H_")
    )
    attacks: dict[str, Callable[[dict[str, Any]], None]] = {
        "schema":
            lambda value: value.__setitem__("schema", "mutated"),
        "status":
            lambda value: value["result"].__setitem__("status", "PASS"),
        "frozen owner":
            lambda value: value["result"]["frozen_prefix"].__setitem__(
                "required_owner", "G[1,0]"
            ),
        "required chart":
            lambda value: value["result"]["frozen_prefix"].__setitem__(
                "required_outgoing_chart", "N"
            ),
        "seam owner":
            lambda value: value["result"]["mathematical_classifier"].__setitem__(
                "diagonal_half_open_owner", "N"
            ),
        "seam owner source":
            lambda value: value["result"]["mathematical_classifier"].__setitem__(
                "diagonal_half_open_owner_source", "untrusted.json"
            ),
        "analytic ownership":
            lambda value: value["result"]["mathematical_classifier"].__setitem__(
                "pinned_rule_applies_to_analytic_strata", False
            ),
        "display outers":
            lambda value: value["result"]["mathematical_classifier"].__setitem__(
                "arb_display_outers_are_not_used_as_sign_witnesses", False
            ),
        "input parents":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "input_parent_leaf_count", 617
            ),
        "input chart ledger":
            lambda value: value["result"]["adaptive_seam_census"][
                "input_by_chart"
            ].__setitem__("W:E", 467),
        "input digest":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "input_rows_sha256", "0" * 64
            ),
        "depth ledger":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "maximum_extra_depth_used", 0
            ),
        "terminal count":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "terminal_record_count", 621
            ),
        "classification ledger":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_classification_counts"
            ].__setitem__("TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES", 279),
        "parent resolution ledger":
            lambda value: value["result"]["adaptive_seam_census"][
                "input_parent_resolution_counts"
            ].__setitem__("PARENT_WITH_DEPTH_LIMIT_RESIDUAL", 1),
        "typed seam ledger":
            lambda value: value["result"]["adaptive_seam_census"][
                "typed_graph_count_by_seam"
            ].__setitem__("NW", 139),
        "typed kind ledger":
            lambda value: value["result"]["adaptive_seam_census"][
                "typed_graph_count_by_kind"
            ].__setitem__("FULL_P_GRAPH", 9),
        "mismatch rectangles":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "strict_mismatch_rectangle_count", 117
            ),
        "W rectangles":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "strict_match_rectangle_count", 223
            ),
        "full dimensional side ledger":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "typed_full_dimensional_mismatch_open_side_count", 279
            ),
        "codimension one ledger":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "typed_codimension_one_half_open_W_graph_count", 279
            ),
        "fake collar exclusion":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "typed_collar_whole_leaf_exclusion_count", 280
            ),
        "fake zero resolution":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "adaptive_depth_limit_unresolved_count", 1
            ),
        "terminal row digest":
            lambda value: value["result"]["adaptive_seam_census"].__setitem__(
                "terminal_rows_sha256", "0" * 64
            ),
        "row classification":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index].__setitem__(
                "classification", "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            ),
        "typed owner label":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"].__setitem__(
                "diagonal_half_open_owner", "N"
            ),
        "typed derivative sign":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"].__setitem__(
                "H_derivative_p_sign", "POSITIVE"
            ),
        "typed forward sign":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"].__setitem__(
                "forward_margin_sign", "NEGATIVE"
            ),
        "typed graph dimension":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"].__setitem__("graph_dimension", 3),
        "typed whole parent credit":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"].__setitem__(
                "whole_parent_leaf_excluded", True
            ),
        "remove typed stratum":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"]["strata"].pop(),
        "typed stratum dimension":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"]["strata"][1].__setitem__(
                "dimension", 2
            ),
        "typed stratum disposition":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][typed_index]["typed_seam"]["strata"][1].__setitem__(
                "frozen_prefix_disposition",
                "PREFIX_STAGE_ONE_MATCH_OPEN_REGION",
            ),
        "monotone sign transfer":
            lambda value: value["result"]["adaptive_seam_census"][
                "terminal_rows"
            ][monotone_index]["monotone_H_separator"].__setitem__(
                "sign_transfer_identity", "reversed"
            ),
        "refined baseline":
            lambda value: value["result"]["refined_recordwise_census"].__setitem__(
                "round163_excluded_record_baseline", 37492
            ),
        "refined exclusion":
            lambda value: value["result"]["refined_recordwise_census"].__setitem__(
                "refined_excluded_records", 37599
            ),
        "dimension mixing":
            lambda value: value["result"]["refined_recordwise_census"].__setitem__(
                "typed_analytic_strata_not_added_to_rectangular_record_count",
                False,
            ),
        "Round164 inheritance":
            lambda value: value["result"]["round164_noninheritance"].__setitem__(
                "whole_tangency_parent_leaf_exclusions_inherited", 12
            ),
        "Round164 result":
            lambda value: value["result"]["round164_noninheritance"].__setitem__(
                "dimension_safe_certificate_result_sha256", "0" * 64
            ),
        "dependency pin":
            lambda value: value["result"]["provenance"][
                "dependency_sha256"
            ].__setitem__(
                "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json",
                "0" * 64,
            ),
        "candidate digest":
            lambda value: value["result"]["provenance"][
                "candidate_registry_digests_checked_before_local_cache"
            ].__setitem__("W:E", "0" * 64),
        "ownership verdict":
            lambda value: value["result"]["provenance"][
                "analytic_seam_owner_manifest_verdict"
            ].__setitem__("eight_chart_seam_ownership", "NOT_CERTIFIED"),
        "D02 promotion":
            lambda value: value["result"]["strict_nonpromotion"].__setitem__(
                "D02", "CLOSED"
            ),
        "CM2 promotion":
            lambda value: value["result"]["strict_nonpromotion"].__setitem__(
                "CM2", "GO"
            ),
        "next gate":
            lambda value: value["result"].__setitem__(
                "next_core_gate", "none"
            ),
        "extra key":
            lambda value: value["result"].__setitem__("extra", True),
    }
    rejected: list[str] = []
    for name, mutate in attacks.items():
        candidate = resigned(document, mutate)
        try:
            validate(candidate, expected)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"semantic attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "all_result_mutations_resigned": True,
        "rejected_attack_names": rejected,
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"x":1,"x":2}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'\xef\xbb\xbf{"x":1}',
        b'{"x":"\\u0000"}',
        b'{"x":"\\ud800"}',
        b'{"x":1}\x00',
    ]
    rejected = 0
    for raw in attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("strict JSON attack accepted")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_rejected": rejected == len(attacks),
    }


def build_verification(
    certificate: Path,
    workers: int,
) -> dict[str, Any]:
    document = strict_load(certificate)
    expected = build_expected(workers)
    validate(document, expected)
    semantic = semantic_attacks(document, expected)
    strict_json = strict_json_attacks()
    require(
        semantic["all_rejected"] and strict_json["all_rejected"],
        "attack suites",
    )
    result = {
        "status": "PASS",
        "certificate_schema": document["schema"],
        "certificate_result_sha256": document["result_sha256"],
        "round165_producer_imported_or_executed": False,
        "all_1176_Round163_rows_reconstructed": True,
        "all_618_seam_parents_reconstructed": True,
        "all_622_terminal_records_reconstructed": True,
        "all_terminal_sign_labels_recomputed": True,
        "all_280_three_stratum_partitions_recomputed": True,
        "dimension_safe_record_ledgers_recomputed": True,
        "analytic_half_open_W_ownership_recomputed_from_pinned_manifest": True,
        "all_certificate_fields_semantically_reconstructed": True,
        "full_document_exactly_matched": True,
        "recursive_exact_key_tree_matched": True,
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_json,
        "strict_nonpromotion_recomputed": True,
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--atlas-workers", type=int, choices=(1, 2), default=2
    )
    arguments = parser.parse_args()
    document = build_verification(
        arguments.certificate,
        arguments.atlas_workers,
    )
    arguments.output.write_text(canonical(document) + "\n")
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
