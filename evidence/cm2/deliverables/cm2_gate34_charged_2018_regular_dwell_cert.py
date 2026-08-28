#!/usr/bin/env python3
"""Positive charged subcylinders with 2018 regular post-core collisions.

The positive core-hit charge contains four oriented parameter branches.  On
each branch this certificate selects an interior point at ``|h|=2^-300``,
replays its core entrance, and validates the next 2018 unique first
collisions with 8192-bit Arb.  Every collision is strictly non-grazing and
strictly earlier than every retained competitor.  Finiteness and continuity
therefore give a positive open subcylinder around each selected point with
the same complete regular itinerary.

This is a local physical no-collision-singularity dwell witness.  It does not
prove that the whole charged cylinder follows the itinerary, that every
selected branch reaches a core, that the fixed-core multiplier is preserved
at every step, or that one common strong-space operator realizes the
scheduled scalar dwell theorem.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


ctx.prec = 8192
Q = Fraction
HERE = Path(__file__).resolve().parent
POST_CORE_STEPS = 2018
POINT_PARAMETER_POWER = 300
POINT_PARAMETER_MAGNITUDE = Q(1, 2**POINT_PARAMETER_POWER)

DEPENDENCIES = {
    "cm2-gate34-positive-core-hit-charge-manifest-2026-07-17.json": (
        "961ba5598e0737bc70a4f1cc86f7ccec31ab40d6d2ec028f3b11d2d473165d37"
    ),
    "cm2_gate34_positive_core_hit_charge_cert.py": (
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
    "cm2_gate45_sparse_cut_dwell_contraction_frontier_cert.py": (
        "38f195eed430f9698c6a4b144198a6c042e868a1f8ad49397d878aa79f547b39"
    ),
}

EXPECTED_ITINERARY_DIGESTS = {
    ("occ:f2b4833eb8dccd403eec3485", "hit"): (
        "d8ca47c69c36c520e4201ee5410a65d747187b6ea4d1b7c56a61fe3baac53da5"
    ),
    ("occ:f2b4833eb8dccd403eec3485", "miss"): (
        "4c92545207710c4c41bdad872464c3e0f29bcad6f55195633c7b69fb0a84b998"
    ),
    ("occ:c5fde0378e6e76eec93a0ceb", "hit"): (
        "a39c479aa39d08e881a9a99db1a75f303eaf215a928946675ac52cb2b2e12694"
    ),
    ("occ:c5fde0378e6e76eec93a0ceb", "miss"): (
        "58441be1a936dfc5c75f6e45ea3de9eb04978d991300e51e2c4db352028ea6c6"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_high_precision_constants() -> None:
    bulk.INV_SQRT_TWO = (arb(1) / 2).sqrt()
    bulk.ARB_RADIUS = {
        obstacle: charge.arbq(radius) for obstacle, radius in bulk.R.items()
    }
    bulk.ARB_RADIUS_SQUARED = {
        obstacle: radius * radius
        for obstacle, radius in bulk.ARB_RADIUS.items()
    }
    charge.bulk.ARB_RADIUS = bulk.ARB_RADIUS


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    dwell_manifest = json.loads(
        (HERE / "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json")
        .read_text(encoding="utf-8")
    )
    shell = dwell_manifest["result"]["shell_scheduled_contraction"]
    assert shell["dwell_steps"] == POST_CORE_STEPS
    assert shell["cycle_coefficient_strict_upper"] == "45/64"
    assert dwell_manifest["verdict"]["native_physical_no_hidden_cut_dwell_schedule"] == (
        "NOT_CERTIFIED"
    )


def point_source_geometry(row: dict[str, Any]) -> tuple[arb, ...]:
    z = Q(row["witness"]["z"])
    geometry = bulk.tangent_geometry(
        row["witness"]["chart_id"],
        z,
        z,
        Q(0),
        Q(0),
        row["target"],
        row["epsilon"],
    )
    assert geometry is not None
    return geometry


def pilot_expected_target(
    qx: arb,
    qy: arb,
    ux: arb,
    uy: arb,
    current_id: str,
    displacement: arb,
) -> str:
    qx_float, qy_float = float(qx), float(qy)
    ux_float, uy_float = float(ux), float(uy)
    displacement_float = float(displacement)
    roots: list[tuple[float, str]] = []
    for target_id in charge.candidate_ids_around(current_id):
        obstacle, ix, iy = charge.parse_target(target_id)
        center_x = ix + (
            Q(1, 2) + displacement_float if obstacle == "W" else 0
        )
        center_y = iy + (Q(1, 2) if obstacle == "W" else 0)
        dx = float(center_x) - qx_float
        dy = float(center_y) - qy_float
        longitudinal = ux_float * dx + uy_float * dy
        transverse = -uy_float * dx + ux_float * dy
        radius = float(bulk.R[obstacle])
        discriminant = radius * radius - transverse * transverse
        if longitudinal <= 0 or discriminant <= 0:
            continue
        root = longitudinal - math.sqrt(discriminant)
        if 0 < root < 2:
            roots.append((root, target_id))
    assert roots
    roots.sort()
    return roots[0][1]


def enter_regular_suffix(
    row: dict[str, Any], side: str,
) -> tuple[arb, arb, arb, arb, arb, arb, str, arb]:
    _nx, _ny, qx, qy, ux, uy, *_rest = point_source_geometry(row)
    polarity = row["parameter_coarea_polarity"]
    signed_parameter = (
        polarity * POINT_PARAMETER_MAGNITUDE
        if side == "hit"
        else -polarity * POINT_PARAMETER_MAGNITUDE
    )
    displacement = charge.arbq(signed_parameter)
    qx, qy = charge.shifted_source_point(
        row["source"], qx, qy, displacement
    )
    current_id = f"{row['source']}[0,0]"
    if side == "hit":
        state = charge.step_expected(
            qx,
            qy,
            ux,
            uy,
            current_id,
            row["target"],
            displacement,
        )
        qx, qy, ux, uy, normal_x, normal_y, _record = state
        current_id = row["target"]
        ignored_competitors: tuple[str, ...] = ()
    else:
        ignored_competitors = (row["target"],)
    state = charge.step_expected(
        qx,
        qy,
        ux,
        uy,
        current_id,
        row["miss_target"],
        displacement,
        ignored_competitors,
    )
    qx, qy, ux, uy, normal_x, normal_y, _record = state
    return (
        qx,
        qy,
        ux,
        uy,
        normal_x,
        normal_y,
        row["miss_target"],
        displacement,
    )


def certify_branch(
    row: dict[str, Any], side: str, specification: dict[str, Any],
) -> dict[str, Any]:
    state = enter_regular_suffix(row, side)
    qx, qy, ux, uy, normal_x, normal_y, current_id, displacement = state
    itinerary = specification["suffix_and_future_targets"]
    assert current_id == itinerary[0]
    for target_id in itinerary[1:]:
        state = charge.step_expected(
            qx,
            qy,
            ux,
            uy,
            current_id,
            target_id,
            displacement,
        )
        qx, qy, ux, uy, normal_x, normal_y, _record = state
        current_id = target_id
    destination = charge.destination_core(
        specification["destination_chart"], normal_x, normal_y, ux, uy
    )

    charged_payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "base_half_width": str(charge.BASE_HALF_WIDTH),
        "parameter_radius": str(charge.PARAMETER_RADIUS),
        "itinerary": itinerary,
        "core_id": destination["core_id"],
    }
    charged_branch_id = "core-charge:" + canonical_digest(charged_payload)

    post_core_itinerary: list[str] = []
    for _step in range(POST_CORE_STEPS):
        target_id = pilot_expected_target(
            qx, qy, ux, uy, current_id, displacement
        )
        state = charge.step_expected(
            qx,
            qy,
            ux,
            uy,
            current_id,
            target_id,
            displacement,
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        assert bool(arb(record["cosine"]) > charge.arbq(Q(1, 1000)))
        post_core_itinerary.append(target_id)
        current_id = target_id

    itinerary_digest = hashlib.sha256(
        "\n".join(post_core_itinerary).encode("utf-8")
    ).hexdigest()
    assert itinerary_digest == EXPECTED_ITINERARY_DIGESTS[
        (row["occurrence_id"], side)
    ]
    payload = {
        "charged_branch_id": charged_branch_id,
        "point_parameter_magnitude": str(POINT_PARAMETER_MAGNITUDE),
        "post_core_steps": POST_CORE_STEPS,
        "itinerary_digest": itinerary_digest,
    }
    return {
        "charged_branch_id": charged_branch_id,
        "regular_dwell_witness_id": "regular-dwell:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "point_base_z": row["witness"]["z"],
        "point_parameter_magnitude": str(POINT_PARAMETER_MAGNITUDE),
        "point_parameter_sign": (
            row["parameter_coarea_polarity"]
            if side == "hit"
            else -row["parameter_coarea_polarity"]
        ),
        "destination_core_id": destination["core_id"],
        "post_core_regular_collision_count": POST_CORE_STEPS,
        "post_core_itinerary_sha256": itinerary_digest,
        "all_post_core_flights_strictly_between_0_and_2": True,
        "all_post_core_cosines_strictly_above_1_over_1000": True,
        "every_retained_competitor_strictly_later": True,
        "finite_strict_system_has_positive_open_parameter_subcylinder": True,
        "positive_subcylinder_radius_materialized": False,
    }


def charged_regular_dwell_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    records = []
    for occurrence_id, specification in charge.SELECTED.items():
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
    assert len({row["regular_dwell_witness_id"] for row in records}) == 4
    assert len({row["occurrence_id"] for row in records}) == 2
    assert all(
        row["finite_strict_system_has_positive_open_parameter_subcylinder"]
        for row in records
    )
    return {
        "charged_occurrence_count": 2,
        "charged_oriented_branch_count": 4,
        "point_parameter_magnitude_power": POINT_PARAMETER_POWER,
        "point_parameter_magnitude": str(POINT_PARAMETER_MAGNITUDE),
        "post_core_regular_collision_count_per_branch": POST_CORE_STEPS,
        "total_validated_post_core_regular_collisions": (
            len(records) * POST_CORE_STEPS
        ),
        "positive_open_no_singularity_subcylinder_count": 4,
        "all_four_points_lie_strictly_inside_the_existing_core_hit_charge": True,
        "all_8072_post_core_flights_strictly_between_0_and_2": True,
        "all_8072_post_core_cosines_strictly_above_1_over_1000": True,
        "all_8072_first_collision_decisions_unique": True,
        "finite_strict_analytic_itinerary_implies_positive_open_subcylinder": True,
        "branch_records_sha256": canonical_digest(records),
        "post_core_itinerary_digest_table": {
            f"{occurrence_id}:{side}": digest
            for (occurrence_id, side), digest in sorted(
                EXPECTED_ITINERARY_DIGESTS.items()
            )
        },
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    refresh_high_precision_constants()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.charged-2018-regular-dwell.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "precision_bits": ctx.prec,
            "floating_pilot_is_proposal_only": True,
            "every_pilot_target_is_independently_validated_by_Arb": True,
        },
        "charged_2018_regular_dwell_registry": (
            charged_regular_dwell_registry()
        ),
        "frozen_scalar_attachment": {
            "abstract_same_interval_shell_cycle_upper": "45/64",
            "abstract_shell_dwell_steps": POST_CORE_STEPS,
            "local_regular_dwell_witness_does_not_install_common_strong_operator": True,
        },
        "strict_nonpromotion": {
            "positive_open_subcylinder_radii": "EXIST_BUT_NOT_MATERIALIZED",
            "whole_four_branch_core_hit_charge_has_2018_common_itinerary": False,
            "all_128_selected_branches_have_positive_core_hit_charge": False,
            "post_core_12108_step_no_recut_dwell": "NOT_CERTIFIED",
            "fixed_core_multiplier_survival_for_all_2018_steps": "NOT_CERTIFIED",
            "same_interval_two_view_shell_identification": "NOT_CERTIFIED",
            "common_strong_space_recovery_operator": "NOT_CERTIFIED",
            "native_global_2018_dwell_schedule": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("POSITIVE_OPEN_2018_REGULAR_DWELL_SUBCYLINDERS_4: CERTIFIED")
    print("VALIDATED_POST_CORE_REGULAR_COLLISIONS_8072: CERTIFIED")
    print("NATIVE_GLOBAL_2018_DWELL_SCHEDULE: NOT_CERTIFIED")
    print("POST_CORE_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
