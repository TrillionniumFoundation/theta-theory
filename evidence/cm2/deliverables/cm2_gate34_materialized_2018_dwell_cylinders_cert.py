#!/usr/bin/env python3
"""Explicit dyadic radii for four charged 2018-step dwell cylinders.

The frozen point witnesses are expanded to two-dimensional source-coordinate
boxes.  Each box has half-width 2^-8000 in base z and in parameter magnitude,
is centered at the frozen base point and |h|=2^-300, and is validated at
8192-bit precision.  Every source-to-core collision, strict terminal core
membership, and all 2018 post-core collisions are checked on the entire box.

This materializes four local positive radii.  It does not extend 2018-step
dwell to the other 124 charged branches, prove 12108-step field-7 dwell,
preserve a fixed multiplier throughout the block, identify a common two-view
restriction, or install a strong-space recovery operator.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate34_charged_2018_regular_dwell_cert as frozen_dwell
import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 8192
RADIUS_POWER = 8000
RADIUS = Q(1, 2**RADIUS_POWER)

DEPENDENCIES = {
    "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json": (
        "fa590ec6fbaeb08b6f5d9e38d45c2fdc3a06dc170451ded93892f7c531653b51"
    ),
    "cm2_gate34_all_occurrence_positive_core_hit_cert.py": (
        "98c7642856bac56a5309a0fcc6a362e971f25f08c3b52292aaa13eace7d2e76f"
    ),
    "cm2-gate34-charged-2018-regular-dwell-manifest-2026-07-17.json": (
        "f85b12c32b867abd11a43cad8e2b8662afc5a5a296b2f6914425789e31b1ae03"
    ),
    "cm2_gate34_charged_2018_regular_dwell_cert.py": (
        "f2d629880621b2623d4a408ce9dfd4334b7728e8e26115a48461c2ccaf352f75"
    ),
    "cm2_gate34_positive_core_hit_charge_cert.py": (
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
    "cm2_gate3_global_physical_subrow_atlas_cert.py": (
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_constants() -> None:
    ctx.prec = PRECISION_BITS
    bulk.INV_SQRT_TWO = (arb(1) / 2).sqrt()
    bulk.ARB_RADIUS = {
        obstacle: charge.arbq(radius) for obstacle, radius in bulk.R.items()
    }
    bulk.ARB_RADIUS_SQUARED = {
        obstacle: radius * radius for obstacle, radius in bulk.ARB_RADIUS.items()
    }
    charge.bulk.ARB_RADIUS = bulk.ARB_RADIUS


def point_post_core_word(
    row: dict[str, Any], side: str, specification: dict[str, Any],
) -> tuple[list[str], str]:
    state = frozen_dwell.enter_regular_suffix(row, side)
    qx, qy, ux, uy, normal_x, normal_y, current_id, displacement = state
    entrance = specification["suffix_and_future_targets"]
    assert current_id == entrance[0]
    for target_id in entrance[1:]:
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, _record = state
        current_id = target_id
    destination = charge.destination_core(
        specification["destination_chart"], normal_x, normal_y, ux, uy
    )
    word = []
    for _step in range(frozen_dwell.POST_CORE_STEPS):
        target_id = frozen_dwell.pilot_expected_target(
            qx, qy, ux, uy, current_id, displacement
        )
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        assert bool(arb(record["cosine"]) > charge.arbq(Q(1, 1000)))
        current_id = target_id
        word.append(target_id)
    digest = hashlib.sha256("\n".join(word).encode("utf-8")).hexdigest()
    assert digest == frozen_dwell.EXPECTED_ITINERARY_DIGESTS[
        (row["occurrence_id"], side)
    ]
    return word, destination["core_id"]


def interval_suffix_state(
    row: dict[str, Any], side: str,
) -> tuple[arb, arb, arb, arb, arb, arb, str, arb]:
    z = Q(row["witness"]["z"])
    geometry = bulk.tangent_geometry(
        row["witness"]["chart_id"],
        z - RADIUS,
        z + RADIUS,
        Q(0),
        Q(0),
        row["target"],
        row["epsilon"],
    )
    assert geometry is not None
    _nx, _ny, qx, qy, ux, uy, *_rest = geometry
    magnitude = charge.interval(
        frozen_dwell.POINT_PARAMETER_MAGNITUDE - RADIUS,
        frozen_dwell.POINT_PARAMETER_MAGNITUDE + RADIUS,
    )
    assert bool(magnitude > 0)
    polarity = row["parameter_coarea_polarity"]
    displacement = (
        polarity * magnitude if side == "hit" else -polarity * magnitude
    )
    qx, qy = charge.shifted_source_point(
        row["source"], qx, qy, displacement
    )
    current_id = f"{row['source']}[0,0]"
    if side == "hit":
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, row["target"], displacement
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


def strict_outside_frozen_core_union(
    target_id: str, normal_x: arb, normal_y: arb, ux: arb, uy: arb,
) -> str:
    if bool(abs(normal_x) > abs(normal_y)):
        t = normal_y
        if bool(normal_x > 0):
            cell = "E"
        else:
            assert bool(normal_x < 0)
            cell = "W"
    else:
        assert bool(abs(normal_y) > abs(normal_x))
        t = normal_x
        if bool(normal_y > 0):
            cell = "N"
        else:
            assert bool(normal_y < 0)
            cell = "S"
    p = -ux * normal_y + uy * normal_x
    chart_id = f"{target_id[0]}:{cell}"
    matching_chart_cores = [
        core for core in core_cert.physical_cores()
        if core.chart_id == chart_id
    ]
    assert len(matching_chart_cores) == 3
    for core in matching_chart_cores:
        separated = (
            bool(t < charge.arbq(core.t0))
            or bool(t > charge.arbq(core.t1))
            or bool(p < charge.arbq(core.p0))
            or bool(p > charge.arbq(core.p1))
        )
        assert separated
    return chart_id


def materialize_branch(
    row: dict[str, Any], side: str, specification: dict[str, Any],
) -> dict[str, Any]:
    post_core_word, point_destination_core_id = point_post_core_word(
        row, side, specification
    )
    state = interval_suffix_state(row, side)
    qx, qy, ux, uy, normal_x, normal_y, current_id, displacement = state
    entrance = specification["suffix_and_future_targets"]
    assert current_id == entrance[0]
    for target_id in entrance[1:]:
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, _record = state
        current_id = target_id
    interval_destination = charge.destination_core(
        specification["destination_chart"], normal_x, normal_y, ux, uy
    )
    assert interval_destination["core_id"] == point_destination_core_id
    first_post_core_target = ""
    first_post_core_chart = ""
    for step, target_id in enumerate(post_core_word, start=1):
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        assert bool(arb(record["cosine"]) > charge.arbq(Q(1, 1000)))
        current_id = target_id
        if step == 1:
            first_post_core_target = target_id
            first_post_core_chart = strict_outside_frozen_core_union(
                target_id, normal_x, normal_y, ux, uy
            )
    assert first_post_core_target
    assert first_post_core_chart
    itinerary_digest = hashlib.sha256(
        "\n".join(post_core_word).encode("utf-8")
    ).hexdigest()
    payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "base_z": row["witness"]["z"],
        "parameter_magnitude": str(frozen_dwell.POINT_PARAMETER_MAGNITUDE),
        "radius": "2^-8000",
        "itinerary_digest": itinerary_digest,
        "destination_core_id": interval_destination["core_id"],
    }
    return {
        "materialized_dwell_cylinder_id": "dwell-cylinder:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "base_z_center": row["witness"]["z"],
        "parameter_magnitude_center": str(
            frozen_dwell.POINT_PARAMETER_MAGNITUDE
        ),
        "parameter_sign": (
            row["parameter_coarea_polarity"]
            if side == "hit" else -row["parameter_coarea_polarity"]
        ),
        "common_base_z_and_parameter_half_width_power": RADIUS_POWER,
        "common_base_z_and_parameter_half_width": "2^-8000",
        "source_to_core_word_length": len(entrance),
        "destination_core_id": interval_destination["core_id"],
        "terminal_core_membership_strict_on_entire_box": True,
        "post_core_regular_collision_count": frozen_dwell.POST_CORE_STEPS,
        "post_core_itinerary_sha256": itinerary_digest,
        "first_post_core_target": first_post_core_target,
        "first_post_core_chart": first_post_core_chart,
        "first_post_core_collision_strictly_outside_frozen_24_core": True,
        "all_post_core_first_collision_decisions_unique_on_entire_box": True,
        "all_post_core_flights_strictly_between_0_and_2_on_entire_box": True,
        "all_post_core_cosines_strictly_above_1_over_1000_on_entire_box": True,
    }


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    all_occurrence_manifest = json.loads(
        (
            HERE
            / "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    all_registry = all_occurrence_manifest["result"][
        "all_occurrence_positive_core_hit_registry"
    ]
    assert all_registry["charged_occurrence_count"] == 64
    assert all_registry["charged_oriented_branch_count"] == 128
    frozen_manifest = json.loads(
        (
            HERE / "cm2-gate34-charged-2018-regular-dwell-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    frozen_registry = frozen_manifest["result"][
        "charged_2018_regular_dwell_registry"
    ]
    assert frozen_registry["positive_open_no_singularity_subcylinder_count"] == 4
    assert frozen_manifest["result"]["strict_nonpromotion"][
        "positive_open_subcylinder_radii"
    ] == "EXIST_BUT_NOT_MATERIALIZED"


def materialized_dwell_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    records = []
    for occurrence_id, specification in sorted(charge.SELECTED.items()):
        row = dict(by_id[occurrence_id])
        row["witness"] = dict(row["witness"])
        row["witness"]["z"] = str(
            Q(row["witness"]["z"]) + Q(specification["z_shift"])
        )
        for side in ("hit", "miss"):
            records.append(materialize_branch(row, side, specification))
    records.sort(key=canonical_json)
    assert len(records) == 4
    assert len({row["materialized_dwell_cylinder_id"] for row in records}) == 4
    assert len({row["occurrence_id"] for row in records}) == 2
    assert RADIUS < frozen_dwell.POINT_PARAMETER_MAGNITUDE
    assert (
        frozen_dwell.POINT_PARAMETER_MAGNITUDE + RADIUS
        < charge.PARAMETER_RADIUS
    )
    coordinate_volume = 4 * (2 * RADIUS) * (2 * RADIUS)
    assert coordinate_volume == Q(1, 2**15996)
    return {
        "materialized_occurrence_count": 2,
        "materialized_oriented_branch_count": 4,
        "explicit_positive_dwell_cylinder_count": 4,
        "Arb_precision_bits": PRECISION_BITS,
        "common_base_z_and_parameter_half_width_power": RADIUS_POWER,
        "common_base_z_and_parameter_half_width": "2^-8000",
        "point_parameter_magnitude_power": frozen_dwell.POINT_PARAMETER_POWER,
        "point_parameter_magnitude": str(
            frozen_dwell.POINT_PARAMETER_MAGNITUDE
        ),
        "all_four_boxes_lie_strictly_inside_frozen_core_hit_charge": True,
        "all_four_source_to_core_words_unique_and_regular": True,
        "all_four_terminal_core_memberships_strict_on_entire_boxes": True,
        "post_core_regular_collision_count_per_branch": 2018,
        "total_interval_validated_post_core_regular_collisions": 8072,
        "all_8072_first_collision_decisions_unique_on_entire_boxes": True,
        "all_8072_flights_strictly_between_0_and_2_on_entire_boxes": True,
        "all_8072_cosines_strictly_above_1_over_1000_on_entire_boxes": True,
        "all_four_first_post_core_collisions_strictly_outside_frozen_24_core": True,
        "fixed_core_open_operator_survival_failure_post_core_time": 1,
        "direct_regular_dwell_identification_with_fixed_core_operator_power": (
            "REFUTED_ON_FOUR_MATERIALIZED_BOXES"
        ),
        "labelled_materialized_coordinate_volume": "2^-15996",
        "labelled_materialized_coordinate_volume_power": 15996,
        "materialized_branch_records_sha256": canonical_digest(records),
        "first_materialized_dwell_cylinder_id": records[0][
            "materialized_dwell_cylinder_id"
        ],
        "last_materialized_dwell_cylinder_id": records[-1][
            "materialized_dwell_cylinder_id"
        ],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    refresh_constants()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.materialized-2018-dwell-cylinders.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "precision_bits": PRECISION_BITS,
            "floating_pilot_is_proposal_only": True,
            "every_pilot_target_is_independently_validated_by_Arb": True,
            "rejected_common_radius_power_6000_not_promoted": True,
        },
        "materialized_2018_dwell_cylinder_registry": (
            materialized_dwell_registry()
        ),
        "strict_nonpromotion": {
            "all_128_charged_branches_have_2018_materialized_dwell": False,
            "post_core_12108_step_field7_dwell": "NOT_CERTIFIED",
            "fixed_core_multiplier_survival_for_all_2018_steps": (
                "REFUTED_ON_FOUR_MATERIALIZED_BOXES"
            ),
            "same_interval_two_view_shell_identification": "NOT_CERTIFIED",
            "common_strong_space_recovery_operator": "NOT_CERTIFIED",
            "native_global_2018_dwell_schedule": "NOT_CERTIFIED",
            "quantitative_cemetery_tail": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("EXPLICIT_POSITIVE_2018_DWELL_CYLINDERS_4: CERTIFIED")
    print("COMMON_DYADIC_HALF_WIDTH_2^-8000: CERTIFIED")
    print("INTERVAL_VALIDATED_POST_CORE_REGULAR_COLLISIONS_8072: CERTIFIED")
    print("DIRECT_FIXED_CORE_OPERATOR_POWER_ATTACHMENT_ON_4_BOXES: REFUTED")
    print("ALL_128_BRANCH_NATIVE_2018_DWELL: NOT_CERTIFIED")
    print("POST_CORE_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
