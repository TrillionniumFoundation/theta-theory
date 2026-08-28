#!/usr/bin/env python3
"""Round165 prototype: adaptive outgoing-chart seam subdivision and typing.

This block starts only from the 618 Round163 owner-matching leaves whose
outgoing dominant chart was interval-overwrapped.  It never treats a
rectangular seam collar as a whole-leaf exclusion.  A terminal collar is
accepted only after it is decomposed into

    {g < 0}, {g = 0}, {g > 0},

where ``g`` is the appropriate target-normal diagonal margin and ``g = 0``
is certified to be one connected monotone graph in the box.  The W side and
the adjacent N/S side are then exact semianalytic pieces; the diagonal itself
is owned by W under the pinned half-open dominant-chart rule.

For the same-colour flight W -> W[1,0], source and target translate together.
Consequently all geometry below is independent of s.  If ``m`` is one of the
two diagonal target normals adjacent to W, put

    D_m = (1,0) + R_W m - R_W n_source,
    H_m = cross(u, D_m).

Then, on a forward incoming intersection,

    H_m = 0  iff  the near-contact target normal is m,
    partial_p H_m = -dot(u,D_m)/sqrt(1-p^2) < 0.

The producer uses those identities plus strict Arb face signs.  It is a
recordwise frozen-prefix result, not an exterior-sheet or D02 closure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge


ctx.prec = 192
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round165_adaptive_typed_seam_census_certificate.json"
SCHEMA = "cm2.round165.adaptive-typed-seam-census.prototype.v1"
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING_CHART = "W"
SOURCE_CHARTS = ("W:E", "W:W", "W:N", "W:S")
DIRECT_CHARTS = ("W:E", "W:N")
DEFAULT_MAX_EXTRA_DEPTH = 14

PINS = {
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
    # Round164-v2 is dimension-safe context.  Its 32 tangency parents are not
    # subtracted: graph typing does not classify off-graph ambient bulk.
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
    "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json":
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
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
            require(key not in result, f"duplicate key:{path.name}")
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
                f"decoded string:{path.name}",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, f"top object:{path.name}")
    return value


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
    verification = strict_load(
        HERE / "cm2_round163_outgoing_chart_pruning_verification.json"
    )
    context = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_certificate.json"
    )
    context_verification = strict_load(
        HERE / "cm2_round164_tangency_strata_pruning_verification.json"
    )
    seam_ownership = strict_load(
        HERE / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
    )
    require(
        prior["result_sha256"] == ROUND163_RESULT_SHA256
        and verification["result_sha256"]
        == ROUND163_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
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
        seam_ownership["verdict"]["eight_chart_seam_ownership"]
        == "CERTIFIED"
        and seam_ownership["verdict"][
            "rectangular_bulk_seam_quotient"
        ] == "CERTIFIED"
        and seam_ownership["result"]["scope_limits"][
            "ownership_rule_applies_to_analytic_strata"
        ] is True
        and seam_ownership["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True
        and seam_ownership["result"]["unique_half_open_owner_rule"][
            "diagonal_tie"
        ] == "E or W owns; N or S excludes",
        "pinned analytic seam ownership",
    )
    return (
        prior,
        verification,
        context,
        context_verification,
        seam_ownership,
    )


TARGET_MAP = {target.target_id: target for target in base.TARGETS}


def root_from_geometry(
    geometry: tuple[arb, arb, arb, arb, arb, arb],
    target_id: str,
) -> atlas.RootRecord:
    """Bit-for-bit operation order of the pinned atlas root routine."""

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
            target_id,
            "no_real_intersection",
            ell,
            discriminant,
            None,
            None,
            transverse,
        )
    if not bool(discriminant > 0):
        return atlas.RootRecord(
            target_id,
            "unresolved_discriminant",
            ell,
            discriminant,
            None,
            None,
            transverse,
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
        target_id,
        classification,
        ell,
        discriminant,
        near,
        far,
        transverse,
    )


def _fast_build_atlas(chart_id: str) -> list[atlas.Leaf]:
    """Replay one pinned atlas with audited, process-local pure caches."""

    candidate_ids = tuple(base.candidate_ids(chart_id))
    require(
        digest(list(candidate_ids)) == EXPECTED_CANDIDATE_DIGESTS[chart_id],
        f"candidate digest:{chart_id}",
    )
    original_candidate_ids = base.candidate_ids
    original_target_by_id = base.target_by_id
    original_records = atlas.records

    def cached_candidate_ids(requested: str) -> tuple[str, ...]:
        require(requested == chart_id, f"unexpected chart cache:{requested}")
        return candidate_ids

    def cached_target_by_id(target_id: str) -> Any:
        return TARGET_MAP[target_id]

    def cached_records(
        requested: str, box: atlas.AtlasBox,
    ) -> list[atlas.RootRecord]:
        require(requested == chart_id, f"unexpected records chart:{requested}")
        geometry = atlas.geometry(requested, box)
        return [
            root_from_geometry(geometry, target_id)
            for target_id in candidate_ids
        ]

    base.candidate_ids = cached_candidate_ids  # type: ignore[assignment]
    base.target_by_id = cached_target_by_id  # type: ignore[assignment]
    atlas.records = cached_records  # type: ignore[assignment]
    try:
        return atlas.build_atlas(chart_id)
    finally:
        atlas.records = original_records  # type: ignore[assignment]
        base.target_by_id = original_target_by_id  # type: ignore[assignment]
        base.candidate_ids = original_candidate_ids  # type: ignore[assignment]


def build_atlases(workers: int) -> dict[str, list[atlas.Leaf]]:
    if workers == 1:
        direct = {
            chart_id: _fast_build_atlas(chart_id)
            for chart_id in DIRECT_CHARTS
        }
    else:
        require(workers == 2, "atlas workers")
        with ProcessPoolExecutor(max_workers=2) as pool:
            values = list(pool.map(_fast_build_atlas, DIRECT_CHARTS))
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


def round163_contact_data(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[str | None, arb, arb, arb, arb, arb, arb]:
    """Replay the deliberately dependency-heavy Round163 contact formula."""

    geometry = atlas.geometry(chart_id, box)
    qx, qy, ux, uy, s, _cp = geometry
    record = root_from_geometry(geometry, FROZEN_OWNER)
    require(
        record.classification == "strict_future_root"
        and record.near is not None,
        f"inherited owner root:{chart_id}:{box.path}",
    )
    target = TARGET_MAP[FROZEN_OWNER]
    center_x, center_y = base.target_center(target, s)
    radius = base.arbq(base.RADIUS[target.obstacle])
    normal_x = (qx + record.near * ux - center_x) / radius
    normal_y = (qy + record.near * uy - center_y) / radius
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return (
                cell,
                normal_x,
                normal_y,
                first,
                second,
                record.near,
                record.discriminant,
            )
    return (
        None,
        normal_x,
        normal_y,
        normal_x,
        normal_y,
        record.near,
        record.discriminant,
    )


def contact_data(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[str | None, arb, arb, arb, arb, arb, arb]:
    """Tight same-colour contact reconstruction with exact s cancellation.

    Writing the target-minus-source-centre vector as ``(1,0)`` before interval
    evaluation removes the duplicate source/target translation balls.  The
    normal formula is the orthonormal-frame identity used by the later exact
    collision engines; it does not form ``q + near*u - centre`` and therefore
    also avoids cancellation of the longitudinal component ``ell*u``.
    """

    nx, ny, _dnx, _dny, ux, uy, _dux, _duy = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    dx = arb(1) - radius * nx
    dy = -radius * ny
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    discriminant = radius * radius - transverse * transverse
    require(bool(discriminant > 0), f"tight owner discriminant:{box.path}")
    radical = discriminant.sqrt()
    near = ell - radical
    require(bool(near > 0), f"tight owner root:{box.path}")
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    tests = {
        "E": (normal_x - normal_y, normal_x + normal_y),
        "W": (-normal_x - normal_y, -normal_x + normal_y),
        "N": (normal_y - normal_x, normal_y + normal_x),
        "S": (-normal_y - normal_x, -normal_y + normal_x),
    }
    for cell in ("E", "W", "N", "S"):
        first, second = tests[cell]
        if bool(first > 0) and bool(second > 0):
            return (
                cell,
                normal_x,
                normal_y,
                first,
                second,
                near,
                discriminant,
            )
    return (
        None,
        normal_x,
        normal_y,
        normal_x,
        normal_y,
        near,
        discriminant,
    )


def source_frame(
    chart_id: str, box: atlas.AtlasBox,
) -> tuple[arb, arb, arb, arb, arb, arb, arb, arb]:
    """Return n, dn/dt, u and du/dt without the cancelling s coordinate."""

    _source, cell = chart_id.split(":")
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    radical_t = ge.sqrt_one_minus_square(box.t0, box.t1)
    radical_p = ge.sqrt_one_minus_square(box.p0, box.p1)
    require(bool(radical_t > 0), "source radical")
    if cell == "E":
        nx, ny = radical_t, t
        dnx, dny = -t / radical_t, arb(1)
    elif cell == "W":
        nx, ny = -radical_t, t
        dnx, dny = t / radical_t, arb(1)
    elif cell == "N":
        nx, ny = t, radical_t
        dnx, dny = arb(1), -t / radical_t
    elif cell == "S":
        nx, ny = t, -radical_t
        dnx, dny = arb(1), t / radical_t
    else:  # pragma: no cover
        raise ValueError(cell)
    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    dux = radical_p * dnx - p * dny
    duy = radical_p * dny + p * dnx
    return nx, ny, dnx, dny, ux, uy, dux, duy


def point_box(
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


SEAM_DATA = {
    "NW": {
        "signs": (-1, 1),
        "adjacent_chart": "N",
        "normal_margin": lambda nx, ny: nx + ny,
        "other_margin": lambda nx, ny: nx - ny,
    },
    "SW": {
        "signs": (-1, -1),
        "adjacent_chart": "S",
        "normal_margin": lambda nx, ny: nx - ny,
        "other_margin": lambda nx, ny: nx + ny,
    },
}


def seam_quantities(
    chart_id: str,
    box: atlas.AtlasBox,
    seam_id: str,
) -> dict[str, arb]:
    data = SEAM_DATA[seam_id]
    inv_sqrt_two = base.arbq(Q(1, 2)).sqrt()
    mx = data["signs"][0] * inv_sqrt_two
    my = data["signs"][1] * inv_sqrt_two
    nx, ny, dnx, dny, ux, uy, dux, duy = source_frame(
        chart_id, box
    )
    radius = base.arbq(base.RADIUS["W"])
    # Target centre minus source centre is exactly (1,0); s cancels.
    dx = arb(1) + radius * mx - radius * nx
    dy = radius * my - radius * ny
    ddx = -radius * dnx
    ddy = -radius * dny
    cross = ux * dy - uy * dx
    forward = ux * dx + uy * dy
    inward = -(ux * mx + uy * my)
    derivative_t = (
        dux * dy - duy * dx + ux * ddy - uy * ddx
    )
    radical_p = ge.sqrt_one_minus_square(box.p0, box.p1)
    derivative_p = -forward / radical_p
    return {
        "H": cross,
        "forward": forward,
        "inward": inward,
        "derivative_p": derivative_p,
        "derivative_t": derivative_t,
    }


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def typed_seam(
    chart_id: str,
    box: atlas.AtlasBox,
    normal_x: arb,
    normal_y: arb,
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for seam_id, data in SEAM_DATA.items():
        normal_margin = data["normal_margin"](normal_x, normal_y)
        other_margin = data["other_margin"](normal_x, normal_y)
        if strict_sign(normal_margin) != 0 or not bool(other_margin < 0):
            continue
        quantities = seam_quantities(chart_id, box, seam_id)
        if not (
            bool(quantities["forward"] > 0)
            and bool(quantities["inward"] > 0)
            and bool(quantities["derivative_p"] < 0)
        ):
            continue
        lower_p = seam_quantities(
            chart_id, point_box(box, p_value=box.p0), seam_id
        )["H"]
        upper_p = seam_quantities(
            chart_id, point_box(box, p_value=box.p1), seam_id
        )["H"]
        corner_values = [
            seam_quantities(
                chart_id,
                point_box(box, t_value=t_value, p_value=p_value),
                seam_id,
            )["H"]
            for t_value in (box.t0, box.t1)
            for p_value in (box.p0, box.p1)
        ]
        corner_signs = [strict_sign(value) for value in corner_values]
        full_p_graph = bool(lower_p > 0) and bool(upper_p < 0)
        derivative_t_sign = strict_sign(quantities["derivative_t"])
        monotone_clipped_graph = (
            derivative_t_sign != 0
            and 1 in corner_signs
            and -1 in corner_signs
        )
        if not (full_p_graph or monotone_clipped_graph):
            continue
        candidates.append({
            "seam_id": seam_id,
            "adjacent_outgoing_chart": data["adjacent_chart"],
            "graph_kind": (
                "FULL_P_GRAPH"
                if full_p_graph
                else "MONOTONE_CLIPPED_GRAPH"
            ),
            "normal_equation": (
                "n_x+n_y=0" if seam_id == "NW" else "n_x-n_y=0"
            ),
            "target_normal": (
                "(-1,+1)/sqrt(2)"
                if seam_id == "NW"
                else "(-1,-1)/sqrt(2)"
            ),
            "W_open_side": (
                "n_x+n_y<0" if seam_id == "NW" else "n_x-n_y<0"
            ),
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
                    "predicate": (
                        "n_x+n_y<0"
                        if seam_id == "NW"
                        else "n_x-n_y<0"
                    ),
                    "outgoing_chart": "W",
                    "frozen_prefix_disposition":
                        "PREFIX_STAGE_ONE_MATCH_OPEN_REGION",
                },
                {
                    "stratum": "ADJACENT_OPEN_SIDE",
                    "dimension": 3,
                    "predicate": (
                        "n_x+n_y>0"
                        if seam_id == "NW"
                        else "n_x-n_y>0"
                    ),
                    "outgoing_chart": data["adjacent_chart"],
                    "frozen_prefix_disposition":
                        "OUTGOING_CHART_MISMATCH_OPEN_REGION",
                },
                {
                    "stratum": "DIAGONAL_GRAPH",
                    "dimension": 2,
                    "predicate": (
                        "n_x+n_y=0"
                        if seam_id == "NW"
                        else "n_x-n_y=0"
                    ),
                    "outgoing_chart": "W",
                    "frozen_prefix_disposition":
                        "PREFIX_STAGE_ONE_MATCH_HALF_OPEN_SEAM",
                },
            ],
            "H_lower_p_face_arb": str(lower_p),
            "H_upper_p_face_arb": str(upper_p),
            "H_lower_p_face_sign": (
                "POSITIVE"
                if strict_sign(lower_p) > 0
                else (
                    "NEGATIVE"
                    if strict_sign(lower_p) < 0
                    else "UNRESOLVED"
                )
            ),
            "H_upper_p_face_sign": (
                "POSITIVE"
                if strict_sign(upper_p) > 0
                else (
                    "NEGATIVE"
                    if strict_sign(upper_p) < 0
                    else "UNRESOLVED"
                )
            ),
            "H_corner_signs": corner_signs,
            "H_derivative_p_arb": str(quantities["derivative_p"]),
            "H_derivative_t_arb": str(quantities["derivative_t"]),
            "H_derivative_p_sign": "NEGATIVE",
            "H_derivative_t_sign": (
                "POSITIVE"
                if derivative_t_sign > 0
                else (
                    "NEGATIVE"
                    if derivative_t_sign < 0
                    else "UNUSED_OR_UNRESOLVED"
                )
            ),
            "forward_margin_arb": str(quantities["forward"]),
            "incoming_margin_arb": str(quantities["inward"]),
            "other_diagonal_margin_arb": str(other_margin),
            "forward_margin_sign": "POSITIVE",
            "incoming_margin_sign": "POSITIVE",
            "other_diagonal_margin_sign": "NEGATIVE",
            "arb_display_outers_are_not_sign_witnesses": True,
        })
    return candidates[0] if len(candidates) == 1 else None


def monotone_H_separated_chart(
    chart_id: str,
    box: atlas.AtlasBox,
    normal_x: arb,
    normal_y: arb,
) -> dict[str, Any] | None:
    """Classify a no-seam rectangle when direct normal balls still overwrap.

    On the half circle selected by ``other_margin < 0``, the exact chord
    identity gives

        sign(n_x+n_y) = -sign(H_NW),
        sign(n_x-n_y) =  sign(H_SW).

    If both partial derivatives of H have fixed sign, its extrema on the
    rectangle occur at corners.  Four same strict corner signs therefore
    prove that the relevant seam is absent from the whole closed rectangle.
    """

    candidates: list[dict[str, Any]] = []
    for seam_id, data in SEAM_DATA.items():
        normal_margin = data["normal_margin"](normal_x, normal_y)
        other_margin = data["other_margin"](normal_x, normal_y)
        if strict_sign(normal_margin) != 0 or not bool(other_margin < 0):
            continue
        quantities = seam_quantities(chart_id, box, seam_id)
        derivative_t_sign = strict_sign(quantities["derivative_t"])
        if not (
            bool(quantities["forward"] > 0)
            and bool(quantities["inward"] > 0)
            and bool(quantities["derivative_p"] < 0)
            and derivative_t_sign != 0
        ):
            continue
        corner_values = [
            seam_quantities(
                chart_id,
                point_box(box, t_value=t_value, p_value=p_value),
                seam_id,
            )["H"]
            for t_value in (box.t0, box.t1)
            for p_value in (box.p0, box.p1)
        ]
        corner_signs = [strict_sign(value) for value in corner_values]
        if not (
            all(sign == 1 for sign in corner_signs)
            or all(sign == -1 for sign in corner_signs)
        ):
            continue
        H_sign = corner_signs[0]
        outgoing_chart = (
            ("W" if H_sign > 0 else "N")
            if seam_id == "NW"
            else ("W" if H_sign < 0 else "S")
        )
        candidates.append({
            "seam_id": seam_id,
            "outgoing_chart": outgoing_chart,
            "H_sign": H_sign,
            "H_corner_signs": corner_signs,
            "H_corner_values_arb": [
                str(value) for value in corner_values
            ],
            "H_derivative_p_arb": str(quantities["derivative_p"]),
            "H_derivative_t_arb": str(quantities["derivative_t"]),
            "H_derivative_p_sign": "NEGATIVE",
            "H_derivative_t_sign": (
                "POSITIVE" if derivative_t_sign > 0 else "NEGATIVE"
            ),
            "forward_margin_arb": str(quantities["forward"]),
            "incoming_margin_arb": str(quantities["inward"]),
            "other_diagonal_margin_arb": str(other_margin),
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
    """Bisect the larger normalized t/p width; s is exactly irrelevant."""

    t_width = (box.t1 - box.t0) / (atlas.T_UPPER - atlas.T_LOWER)
    p_width = (box.p1 - box.p0) / (atlas.P_UPPER - atlas.P_LOWER)
    depth = box.depth + 1
    if t_width >= p_width:
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


def terminal_row(
    parent_key: str,
    chart_id: str,
    box: atlas.AtlasBox,
    extra_depth: int,
) -> tuple[dict[str, Any] | None, str]:
    (
        cell, normal_x, normal_y, first, second, near, discriminant,
    ) = contact_data(chart_id, box)
    common = {
        "parent_leaf_key": parent_key,
        "leaf_key": f"{chart_id}:{box.path}",
        "chart_id": chart_id,
        "extra_depth": extra_depth,
        "box": box_row(box),
    }
    if cell is not None:
        disposition = (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if cell == FROZEN_OUTGOING_CHART
            else "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        return ({
            **common,
            "classification": disposition,
            "outgoing_chart": cell,
            "strict_margin_one_arb": str(first),
            "strict_margin_two_arb": str(second),
        }, "terminal")
    separated = monotone_H_separated_chart(
        chart_id, box, normal_x, normal_y
    )
    if separated is not None:
        cell = separated["outgoing_chart"]
        disposition = (
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE"
            if cell == FROZEN_OUTGOING_CHART
            else "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE"
        )
        return ({
            **common,
            "classification": disposition,
            "outgoing_chart": cell,
            "monotone_H_separator": separated,
        }, "terminal")
    seam = typed_seam(chart_id, box, normal_x, normal_y)
    if seam is not None:
        return ({
            **common,
            "classification": "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES",
            "outgoing_chart": None,
            "owner_root_arb": str(near),
            "owner_discriminant_arb": str(discriminant),
            "typed_seam": seam,
        }, "terminal")
    return None, "subdivide"


def refine_parent(
    chart_id: str,
    parent: atlas.Leaf,
    max_extra_depth: int,
) -> list[dict[str, Any]]:
    parent_key = f"{chart_id}:{parent.box.path}"
    pending = [(parent.box, 0)]
    rows: list[dict[str, Any]] = []
    while pending:
        box, extra_depth = pending.pop()
        row, status = terminal_row(
            parent_key, chart_id, box, extra_depth
        )
        if status == "terminal":
            assert row is not None
            rows.append(row)
        elif extra_depth >= max_extra_depth:
            (
                _cell, nx, ny, _first, _second, near, discriminant,
            ) = contact_data(chart_id, box)
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
    return sorted(rows, key=lambda item: item["leaf_key"])


def box_volume(box: atlas.AtlasBox) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def rational_volume_from_row(row: dict[str, Any]) -> Q:
    box = row["box"]
    return (
        (Q(box["t"][1]) - Q(box["t"][0]))
        * (Q(box["p"][1]) - Q(box["p"][0]))
        * (Q(box["s"][1]) - Q(box["s"][0]))
    )


def round163_replay_row(
    chart_id: str, leaf: atlas.Leaf,
) -> dict[str, Any]:
    (
        cell, nx, ny, first, second, _near, _discriminant,
    ) = round163_contact_data(chart_id, leaf.box)
    if cell is None:
        disposition = "OUTGOING_CHART_SEAM_UNRESOLVED"
        first, second = nx, ny
    elif cell == FROZEN_OUTGOING_CHART:
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


def build_result(
    max_extra_depth: int,
    atlas_workers: int,
) -> dict[str, Any]:
    (
        prior,
        verification,
        round164_context,
        round164_verification,
        seam_ownership,
    ) = check_chain()
    atlases = build_atlases(atlas_workers)
    prior_chart_rows = {
        row["chart_id"]: row
        for row in prior["result"]["outgoing_chart_pruning"]["charts"]
    }
    input_by_chart: dict[str, list[atlas.Leaf]] = {}
    replay_rows: list[dict[str, Any]] = []
    for chart_id in SOURCE_CHARTS:
        owner_leaves = [
            leaf for leaf in atlases[chart_id]
            if leaf.classification == "unique_first"
            and leaf.owner_target == FROZEN_OWNER
        ]
        require(
            len(owner_leaves)
            == prior_chart_rows[chart_id]["owner_match_leaf_count"],
            f"owner leaf replay:{chart_id}",
        )
        chart_replay = [
            round163_replay_row(chart_id, leaf)
            for leaf in sorted(owner_leaves, key=lambda item: item.box.path)
        ]
        require(
            digest(chart_replay)
            == prior_chart_rows[chart_id]["disposition_rows_sha256"],
            f"Round163 row digest:{chart_id}",
        )
        replay_rows.extend(chart_replay)
        unresolved_paths = {
            row["leaf_key"]
            for row in chart_replay
            if row["disposition"] == "OUTGOING_CHART_SEAM_UNRESOLVED"
        }
        input_by_chart[chart_id] = [
            leaf for leaf in owner_leaves
            if f"{chart_id}:{leaf.box.path}" in unresolved_paths
        ]
    require(
        len(replay_rows) == 1176
        and digest(replay_rows)
        == prior["result"]["outgoing_chart_pruning"][
            "all_disposition_rows_sha256"
        ],
        "Round163 all-row replay",
    )
    input_leaves = [
        (chart_id, leaf)
        for chart_id in SOURCE_CHARTS
        for leaf in input_by_chart[chart_id]
    ]
    require(len(input_leaves) == 618, "Round163 seam input")
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
        for row in refine_parent(chart_id, leaf, max_extra_depth)
    ]
    terminal_rows.sort(key=lambda item: item["leaf_key"])
    counts: dict[str, int] = {}
    volumes: dict[str, Q] = {}
    charts: dict[str, dict[str, int]] = {
        chart_id: {} for chart_id in SOURCE_CHARTS
    }
    for row in terminal_rows:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1
        volumes[classification] = (
            volumes.get(classification, Q(0))
            + rational_volume_from_row(row)
        )
        chart_counts = charts[row["chart_id"]]
        chart_counts[classification] = (
            chart_counts.get(classification, 0) + 1
        )
    input_volume = sum(
        (box_volume(leaf.box) for _chart, leaf in input_leaves), Q(0)
    )
    require(sum(volumes.values(), Q(0)) == input_volume, "refined volume")
    typed_rows = [
        row for row in terminal_rows
        if row["classification"] == "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES"
    ]
    typed_by_seam: dict[str, int] = {}
    typed_by_kind: dict[str, int] = {}
    maximum_extra_depth = max(
        row["extra_depth"] for row in terminal_rows
    )
    for row in typed_rows:
        seam_id = row["typed_seam"]["seam_id"]
        kind = row["typed_seam"]["graph_kind"]
        typed_by_seam[seam_id] = typed_by_seam.get(seam_id, 0) + 1
        typed_by_kind[kind] = typed_by_kind.get(kind, 0) + 1

    rows_by_parent: dict[str, list[dict[str, Any]]] = {}
    for row in terminal_rows:
        rows_by_parent.setdefault(row["parent_leaf_key"], []).append(row)
    require(len(rows_by_parent) == 618, "parent terminal registry")
    parent_resolution_counts = {
        "WHOLE_PARENT_OUTGOING_CHART_MISMATCH": 0,
        "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH": 0,
        "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION": 0,
        "PARENT_WITH_DEPTH_LIMIT_RESIDUAL": 0,
    }
    for rows in rows_by_parent.values():
        classifications = {
            row["classification"] for row in rows
        }
        if "ADAPTIVE_DEPTH_LIMIT_UNRESOLVED" in classifications:
            key = "PARENT_WITH_DEPTH_LIMIT_RESIDUAL"
        elif "TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES" in classifications:
            key = "PARENT_WITH_TYPED_SEAM_THREE_STRATUM_PARTITION"
        elif all(row["outgoing_chart"] == "W" for row in rows):
            key = "WHOLE_PARENT_PREFIX_STAGE_ONE_MATCH"
        else:
            require(
                all(
                    row["outgoing_chart"] in {"E", "N", "S"}
                    for row in rows
                ),
                "mixed untyped parent disposition",
            )
            key = "WHOLE_PARENT_OUTGOING_CHART_MISMATCH"
        parent_resolution_counts[key] += 1
    require(
        sum(parent_resolution_counts.values()) == 618,
        "parent resolution census",
    )

    mismatch_count = sum(
        counts.get(classification, 0)
        for classification in (
            "STRICT_OUTGOING_CHART_MISMATCH_RECTANGLE",
            "MONOTONE_H_OUTGOING_CHART_MISMATCH_RECTANGLE",
        )
    )
    match_count = sum(
        counts.get(classification, 0)
        for classification in (
            "STRICT_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
            "MONOTONE_H_PREFIX_STAGE_ONE_MATCH_RECTANGLE",
        )
    )
    typed_count = len(typed_rows)
    unresolved_count = counts.get(
        "ADAPTIVE_DEPTH_LIMIT_UNRESOLVED", 0
    )
    prior_combined = prior["result"]["combined_frozen_prefix_census"]
    require(
        prior_combined["combined_recordwise_excluded_leaf_count"] == 37480
        and prior_combined["remaining_leaf_count"] == 39348,
        "Round163 combined baseline",
    )
    untouched_remaining = prior_combined["remaining_leaf_count"] - 618
    refined_total_records = 76828 - 618 + len(terminal_rows)
    refined_excluded_records = (
        prior_combined["combined_recordwise_excluded_leaf_count"]
        + mismatch_count
    )
    refined_live_records = (
        untouched_remaining
        + match_count
        + typed_count
        + unresolved_count
    )
    require(
        refined_excluded_records + refined_live_records
        == refined_total_records,
        "refined record census",
    )
    return {
        "status": (
            "ROUND165_ADAPTIVE_TYPED_SEAM_PROTOTYPE__"
            + (
                "ALL_618_INPUTS_RECTANGULAR_OR_TYPED_GRAPH_RESOLVED"
                if unresolved_count == 0
                else "DEPTH_LIMIT_RESIDUAL_REMAINS"
            )
        ),
        "frozen_prefix": {
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": FROZEN_OUTGOING_CHART,
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
            "pinned_rule_applies_to_analytic_strata": seam_ownership[
                "result"
            ]["scope_limits"]["ownership_rule_applies_to_analytic_strata"],
        },
        "adaptive_seam_census": {
            "input_parent_leaf_count": len(input_leaves),
            "input_by_chart": {
                chart_id: len(input_by_chart[chart_id])
                for chart_id in SOURCE_CHARTS
            },
            "input_rows_sha256": digest(input_rows),
            "input_rational_volume": str(input_volume),
            "maximum_extra_depth_allowed": max_extra_depth,
            "maximum_extra_depth_used": maximum_extra_depth,
            "terminal_record_count": len(terminal_rows),
            "terminal_classification_counts": counts,
            "terminal_classification_rational_volumes": {
                key: str(value) for key, value in sorted(volumes.items())
            },
            "terminal_counts_by_source_chart": charts,
            "input_parent_resolution_counts": parent_resolution_counts,
            "typed_graph_count_by_seam": typed_by_seam,
            "typed_graph_count_by_kind": typed_by_kind,
            "strict_mismatch_rectangle_count": mismatch_count,
            "strict_match_rectangle_count": match_count,
            "typed_graph_collar_count": typed_count,
            "typed_full_dimensional_W_open_side_count": typed_count,
            "typed_full_dimensional_mismatch_open_side_count": typed_count,
            "typed_codimension_one_half_open_W_graph_count": typed_count,
            "typed_collar_whole_leaf_exclusion_count": 0,
            "adaptive_depth_limit_unresolved_count": unresolved_count,
            "all_618_inputs_semantically_chart_typed":
                unresolved_count == 0,
            "terminal_rows_sha256": digest(terminal_rows),
            "terminal_rows": terminal_rows,
        },
        "refined_recordwise_census": {
            "round163_total_source_W_records": 76828,
            "round163_seam_parent_records_replaced": 618,
            "round163_excluded_record_baseline": 37480,
            "round163_remaining_record_baseline": 39348,
            "untouched_remaining_parent_records": untouched_remaining,
            "new_strict_mismatch_child_rectangles": mismatch_count,
            "typed_collars_not_counted_as_whole_record_exclusions":
                typed_count,
            "typed_analytic_strata_not_added_to_rectangular_record_count":
                True,
            "refined_live_records_is_conservative_rectangle_or_collar_count":
                True,
            "refined_total_records": refined_total_records,
            "refined_excluded_records": refined_excluded_records,
            "refined_live_records": refined_live_records,
        },
        "round164_noninheritance": {
            "dimension_safe_schema": round164_context["schema"],
            "dimension_safe_certificate_result_sha256":
                round164_context["result_sha256"],
            "dimension_safe_verification_result_sha256":
                round164_verification["result_sha256"],
            "tangency_parent_leaf_count": round164_context["result"][
                "tangency_graph_typing"
            ]["ambient_parent_leaf_count"],
            "whole_tangency_parent_leaf_exclusions_inherited": 0,
            "reason":
                "typing a tangency graph does not classify its off-graph bulk",
            "combined_exclusion_baseline_remains": 37480,
            "combined_remaining_baseline_before_Round165_refinement": 39348,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "round163_result_sha256": prior["result_sha256"],
            "round163_verification_result_sha256":
                verification["result_sha256"],
            "round163_all_1176_rows_replayed": True,
            "round163_all_rows_sha256": digest(replay_rows),
            "direct_source_W_atlases_replayed_at_192_bits": True,
            "candidate_registry_digests_checked_before_local_cache":
                EXPECTED_CANDIDATE_DIGESTS,
            "local_cache_changes_no_dependency_file": True,
            "analytic_seam_owner_manifest_verdict": {
                "eight_chart_seam_ownership": seam_ownership["verdict"][
                    "eight_chart_seam_ownership"
                ],
                "rectangular_bulk_seam_quotient": seam_ownership[
                    "verdict"
                ]["rectangular_bulk_seam_quotient"],
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


def build(
    max_extra_depth: int,
    atlas_workers: int,
) -> dict[str, Any]:
    result = build_result(max_extra_depth, atlas_workers)
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--max-extra-depth", type=int, default=DEFAULT_MAX_EXTRA_DEPTH
    )
    parser.add_argument(
        "--atlas-workers", type=int, choices=(1, 2), default=2
    )
    arguments = parser.parse_args()
    require(
        0 <= arguments.max_extra_depth <= 24,
        "max extra depth range",
    )
    document = build(
        arguments.max_extra_depth,
        arguments.atlas_workers,
    )
    arguments.output.write_text(canonical(document) + "\n")
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
