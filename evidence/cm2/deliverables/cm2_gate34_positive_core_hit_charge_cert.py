#!/usr/bin/env python3
"""Positive all-scale core-hit charge on two selected occurrence rows.

Two reference suffix orbits enter frozen diagonal cores after twenty regular
collisions.  This certificate validates the complete prescribed itinerary
with 1024-bit Arb on positive source-row intervals and on both actual
parameter sides for every ``0<|h|<=2^-220``.  The hit side includes the
grazing square-root limit by an independent nonnegative enclosure; the miss
side is the direct regular continuation.  Both sides of each occurrence then
follow the same twenty-target word into one compact core.

The result supplies the first strictly positive selected-germ core-hit
charge.  It covers two of 64 occurrences and four of 128 oriented branches;
it does not give a global hit fraction, a cemetery tail, or the subsequent
2018/12108 no-recut dwell.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


ctx.prec = 1024
Q = Fraction
HERE = Path(__file__).resolve().parent
WIDTH_POWER = 220
BASE_HALF_WIDTH = Q(1, 2**WIDTH_POWER)
PARAMETER_RADIUS = Q(1, 2**WIDTH_POWER)
SQRT_DISCRIMINANT_UPPER = Q(1, 2**100)
TARGET_PATTERN = re.compile(r"([GW])\[(-?\d+),(-?\d+)\]")

DEPENDENCIES = {
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json": (
        "ae6c31fb385070bec1c85463d0d125a504089da6c035c8d34d892a768a6f8c2e"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
}


SELECTED = {
    "occ:f2b4833eb8dccd403eec3485": {
        "z_shift": "3/2251799813685248",
        "suffix_and_future_targets": [
            "G[0,-1]", "W[0,0]", "G[1,0]", "W[0,0]", "G[0,0]",
            "G[2,1]", "W[1,0]", "G[2,1]", "W[1,0]", "G[2,1]",
            "G[2,0]", "W[1,0]", "G[2,0]", "W[1,0]", "G[2,1]",
            "G[2,0]", "G[2,1]", "G[2,0]", "G[3,0]", "W[2,0]",
            "G[3,0]",
        ],
        "destination_chart": "G:W",
    },
    "occ:c5fde0378e6e76eec93a0ceb": {
        "z_shift": "1/4503599627370496",
        "suffix_and_future_targets": [
            "G[-1,0]", "W[0,0]", "G[0,1]", "W[0,0]", "G[0,0]",
            "G[1,2]", "W[0,1]", "G[1,2]", "W[0,1]", "G[1,2]",
            "G[0,2]", "W[0,1]", "G[0,2]", "W[0,1]", "G[1,2]",
            "G[0,2]", "G[1,2]", "G[0,2]", "G[0,3]", "W[0,2]",
            "G[0,3]",
        ],
        "destination_chart": "G:S",
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    return bulk.arb_interval(lower, upper)


def parse_target(target_id: str) -> tuple[str, int, int]:
    match = TARGET_PATTERN.fullmatch(target_id)
    assert match is not None
    return match.group(1), int(match.group(2)), int(match.group(3))


def target_center(target_id: str, displacement: arb) -> tuple[arb, arb]:
    obstacle, ix, iy = parse_target(target_id)
    return (
        arb(ix) + (arbq(Q(1, 2)) + displacement if obstacle == "W" else 0),
        arb(iy) + (arbq(Q(1, 2)) if obstacle == "W" else 0),
    )


def candidate_ids_around(current_id: str, radius: int = 4) -> Iterable[str]:
    _obstacle, ix0, iy0 = parse_target(current_id)
    for obstacle in ("G", "W"):
        for ix in range(ix0 - radius, ix0 + radius + 1):
            for iy in range(iy0 - radius, iy0 + radius + 1):
                target_id = f"{obstacle}[{ix},{iy}]"
                if target_id != current_id:
                    yield target_id


def root_data(
    qx: arb, qy: arb, ux: arb, uy: arb, target_id: str, displacement: arb,
) -> tuple[arb, arb, arb, arb, arb]:
    ax, ay = target_center(target_id, displacement)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    cross = -uy * dx + ux * dy
    radius = bulk.ARB_RADIUS[target_id[0]]
    discriminant = radius * radius - cross * cross
    return ell, cross, discriminant, ax, ay


def step_expected(
    qx: arb,
    qy: arb,
    ux: arb,
    uy: arb,
    current_id: str,
    expected_id: str,
    displacement: arb,
    ignored_competitors: tuple[str, ...] = (),
) -> tuple[arb, arb, arb, arb, arb, arb, dict[str, str]]:
    ell, cross, discriminant, ax, ay = root_data(
        qx, qy, ux, uy, expected_id, displacement
    )
    assert bool(ell > 0) and bool(discriminant > 0)
    radical = discriminant.sqrt()
    root = ell - radical
    assert bool(root > arbq(Q(1, 10**40)))
    assert bool(root < arbq(Q(2)))

    for candidate_id in candidate_ids_around(current_id):
        if candidate_id == expected_id or candidate_id in ignored_competitors:
            continue
        candidate_ell, _candidate_cross, candidate_delta, _ax, _ay = root_data(
            qx, qy, ux, uy, candidate_id, displacement
        )
        if bool(candidate_delta < 0) or bool(candidate_ell < 0):
            continue
        candidate_radius = bulk.ARB_RADIUS[candidate_id[0]]
        if bool(candidate_ell - candidate_radius > root):
            continue
        assert bool(candidate_delta > 0) and bool(candidate_ell > 0)
        candidate_root = candidate_ell - candidate_delta.sqrt()
        assert bool(candidate_root > root)

    radius = bulk.ARB_RADIUS[expected_id[0]]
    normal_x = (-radical * ux + cross * uy) / radius
    normal_y = (-radical * uy - cross * ux) / radius
    contact_x = ax + radius * normal_x
    contact_y = ay + radius * normal_y
    outgoing_x = (
        (1 - 2 * discriminant / (radius * radius)) * ux
        + 2 * radical * cross / (radius * radius) * uy
    )
    outgoing_y = (
        (1 - 2 * discriminant / (radius * radius)) * uy
        - 2 * radical * cross / (radius * radius) * ux
    )
    speed = outgoing_x * outgoing_x + outgoing_y * outgoing_y
    assert bool(speed > arbq(Q(999999, 1000000)))
    assert bool(speed < arbq(Q(1000001, 1000000)))
    return (
        contact_x, contact_y, outgoing_x, outgoing_y,
        normal_x, normal_y,
        {"target": expected_id, "root": str(root), "cosine": str(radical / radius)},
    )


def source_geometry(row: dict[str, Any]) -> tuple[arb, ...]:
    z = Q(row["witness"]["z"])
    geometry = bulk.tangent_geometry(
        row["witness"]["chart_id"],
        z - BASE_HALF_WIDTH,
        z + BASE_HALF_WIDTH,
        Q(0), Q(0), row["target"], row["epsilon"],
    )
    assert geometry is not None
    return geometry


def shifted_source_point(
    source: str, qx: arb, qy: arb, displacement: arb,
) -> tuple[arb, arb]:
    return qx + (displacement if source == "W" else 0), qy


def direct_suffix_state(
    row: dict[str, Any], magnitude: arb,
) -> tuple[arb, arb, arb, arb, arb, arb, dict[str, str]]:
    _nx, _ny, qx, qy, ux, uy, _ell, _cp, _p, _s = source_geometry(row)
    displacement = -row["parameter_coarea_polarity"] * magnitude
    qx, qy = shifted_source_point(row["source"], qx, qy, displacement)
    return step_expected(
        qx, qy, ux, uy,
        f"{row['source']}[0,0]", row["miss_target"], displacement,
        (row["target"],),
    )


def hit_suffix_state(
    row: dict[str, Any], magnitude: arb,
) -> tuple[arb, arb, arb, arb, arb, arb, dict[str, str]]:
    _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, _s = source_geometry(row)
    polarity = row["parameter_coarea_polarity"]
    displacement = polarity * magnitude
    qx, qy = shifted_source_point(row["source"], qx, qy, displacement)
    eta = int(row["target"][0] == "W") - int(row["source"] == "W")
    radius = bulk.ARB_RADIUS[row["target"][0]]
    projection = ell_t + eta * ux * displacement
    cross = row["epsilon"] * radius - eta * uy * displacement
    transversality = polarity * row["epsilon"] * eta * uy
    assert bool(transversality > 0)
    factor = 2 * radius * transversality - uy * uy * magnitude
    assert bool(factor > 0)
    assert SQRT_DISCRIMINANT_UPPER**2 > 2 * PARAMETER_RADIUS
    radical = interval(Q(0), SQRT_DISCRIMINANT_UPPER)
    root = projection - radical
    assert bool(root > 0) and bool(root < arbq(Q(2)))

    target_x, target_y = target_center(row["target"], displacement)
    normal_x = (-radical * ux + cross * uy) / radius
    normal_y = (-radical * uy - cross * ux) / radius
    contact_x = target_x + radius * normal_x
    contact_y = target_y + radius * normal_y
    discriminant = radical * radical
    outgoing_x = (
        (1 - 2 * discriminant / (radius * radius)) * ux
        + 2 * radical * cross / (radius * radius) * uy
    )
    outgoing_y = (
        (1 - 2 * discriminant / (radius * radius)) * uy
        - 2 * radical * cross / (radius * radius) * ux
    )
    suffix = step_expected(
        contact_x, contact_y, outgoing_x, outgoing_y,
        row["target"], row["miss_target"], displacement,
    )
    suffix[-1]["tangent_root"] = str(root)
    return suffix


def destination_core(
    chart_id: str, normal_x: arb, normal_y: arb, ux: arb, uy: arb,
) -> dict[str, Any]:
    source, cell = chart_id.split(":")
    assert source == "G"
    if cell in {"E", "W"}:
        t = normal_y
        assert bool(abs(normal_x) > abs(normal_y))
    else:
        t = normal_x
        assert bool(abs(normal_y) > abs(normal_x))
    p = -ux * normal_y + uy * normal_x
    matches = []
    for core in core_cert.physical_cores():
        if core.chart_id != chart_id:
            continue
        if (
            bool(t > arbq(core.t0)) and bool(t < arbq(core.t1))
            and bool(p > arbq(core.p0)) and bool(p < arbq(core.p1))
        ):
            matches.append(core)
    assert len(matches) == 1
    core = matches[0]
    payload = {
        "chart_id": core.chart_id,
        "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }
    return {
        "core_id": "core:" + canonical_digest(payload),
        "chart_id": chart_id,
        "final_t": str(t),
        "final_p": str(p),
        "strict_interior": True,
    }


def certify_branch(
    row: dict[str, Any], side: str, specification: dict[str, Any],
) -> dict[str, Any]:
    magnitude = interval(Q(0), PARAMETER_RADIUS)
    if side == "hit":
        state = hit_suffix_state(row, magnitude)
        displacement = row["parameter_coarea_polarity"] * magnitude
        suffix_collision_count = 2
    else:
        state = direct_suffix_state(row, magnitude)
        displacement = -row["parameter_coarea_polarity"] * magnitude
        suffix_collision_count = 1
    qx, qy, ux, uy, normal_x, normal_y, suffix_record = state
    itinerary = specification["suffix_and_future_targets"]
    assert suffix_record["target"] == itinerary[0] == row["miss_target"]
    step_records = [suffix_record]
    current_id = itinerary[0]
    for expected_id in itinerary[1:]:
        state = step_expected(
            qx, qy, ux, uy, current_id, expected_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        step_records.append(record)
        current_id = expected_id
    assert len(step_records) == 21
    core = destination_core(
        specification["destination_chart"], normal_x, normal_y, ux, uy
    )
    payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "base_half_width": str(BASE_HALF_WIDTH),
        "parameter_radius": str(PARAMETER_RADIUS),
        "itinerary": itinerary,
        "core_id": core["core_id"],
    }
    return {
        "charged_branch_id": "core-charge:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "source_chart": row["witness"]["chart_id"],
        "base_z_center": row["witness"]["z"],
        "base_z_half_width": str(BASE_HALF_WIDTH),
        "parameter_magnitude_interval": ["0_open", str(PARAMETER_RADIUS)],
        "parameter_sign": (
            row["parameter_coarea_polarity"]
            if side == "hit" else -row["parameter_coarea_polarity"]
        ),
        "collision_count_to_regular_suffix": suffix_collision_count,
        "regular_suffix_target": itinerary[0],
        "post_suffix_collision_count_to_core": 20,
        "total_collision_count_from_source_to_core": (
            suffix_collision_count + 20
        ),
        "destination": core,
        "complete_itinerary": itinerary,
        "all_flights_strictly_between_0_and_2": True,
        "no_intermediate_collision_singularity": True,
        "step_records_sha256": canonical_digest(step_records),
    }


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected


def positive_core_hit_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    records = []
    for occurrence_id, specification in SELECTED.items():
        row = dict(by_id[occurrence_id])
        row["witness"] = dict(row["witness"])
        row["witness"]["z"] = str(
            Q(row["witness"]["z"]) + Q(specification["z_shift"])
        )
        for side in ("hit", "miss"):
            records.append(certify_branch(row, side, specification))
    records.sort(key=canonical_json)
    assert len(records) == 4
    assert len({row["charged_branch_id"] for row in records}) == 4
    assert len({row["occurrence_id"] for row in records}) == 2
    assert len({row["destination"]["core_id"] for row in records}) == 2
    coordinate_volume = (
        2 * (2 * BASE_HALF_WIDTH) * (2 * PARAMETER_RADIUS)
    )
    assert coordinate_volume == Q(1, 2 ** (2 * WIDTH_POWER - 3))
    return {
        "charged_occurrence_count": 2,
        "charged_oriented_branch_count": 4,
        "all_four_branches_cover_every_scale_below_radius": True,
        "selected_reference_z_shifts": {
            occurrence_id: specification["z_shift"]
            for occurrence_id, specification in sorted(SELECTED.items())
        },
        "base_z_half_width_power": WIDTH_POWER,
        "base_z_half_width": str(BASE_HALF_WIDTH),
        "parameter_radius_power": WIDTH_POWER,
        "parameter_radius": str(PARAMETER_RADIUS),
        "post_suffix_collision_count_to_core": 20,
        "destination_core_count": 2,
        "all_84_suffix_and_post_suffix_flights_strictly_between_0_and_2": True,
        "all_four_words_avoid_intermediate_collision_singularities": True,
        "all_four_destinations_are_strict_core_interiors": True,
        "labelled_base_parameter_coordinate_volume_power": 437,
        "labelled_base_parameter_coordinate_volume": str(coordinate_volume),
        "charged_branch_rows_sha256": canonical_digest(records),
        "first_charged_branch_id": records[0]["charged_branch_id"],
        "last_charged_branch_id": records[-1]["charged_branch_id"],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.positive-core-hit-charge.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "precision_bits": ctx.prec,
        },
        "selected_positive_core_hit_charge_registry": (
            positive_core_hit_registry()
        ),
        "strict_nonpromotion": {
            "four_charged_branches_are_all_128_selected_branches": False,
            "positive_coordinate_volume_is_collision_SRB_fraction": False,
            "two_occurrences_imply_uniform_core_hit_fraction": False,
            "post_core_2018_step_no_recut_dwell": "NOT_CERTIFIED",
            "post_core_12108_step_no_recut_dwell": "NOT_CERTIFIED",
            "quantitative_cemetery_tail": "NOT_CERTIFIED",
            "common_strong_space_recovery_operator": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("POSITIVE_ALL_SCALE_CORE_HIT_OCCURRENCES_2: CERTIFIED")
    print("POSITIVE_ALL_SCALE_CORE_HIT_ORIENTED_BRANCHES_4: CERTIFIED")
    print("POST_SUFFIX_COLLISION_TIME_TO_CORE_20: CERTIFIED")
    print("GLOBAL_SELECTED_CORE_HIT_FRACTION: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
