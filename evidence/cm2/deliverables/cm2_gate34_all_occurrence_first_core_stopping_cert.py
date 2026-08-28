#!/usr/bin/env python3
"""First-core stopping cylinders for all 128 charged occurrence sides.

The preceding all-occurrence certificate produced one positive all-scale
core-hit cylinder on each hit/miss side of every maximal reference
occurrence, but intentionally recorded only an entrance-time upper bound.
This replay closes the finite stopping prefix on exactly those cylinders.

For every source box it first rechecks the physical immutable-row label and
the global first-collision owners on both actual-parameter sides.  It then
replays every listed collision with Arb, classifies every intermediate state
against the complete frozen 24-core union, and requires every state before
the displayed terminal time to be strictly outside all 24 cores.  The final
state must be strictly inside exactly one core.

The result certifies first-core stopping times on the 128 labelled positive
cylinders.  It does not cover the whole germ domains, identify labelled
coordinate volume with collision-SRB mass, estimate a cemetery tail, or
construct a strong induced operator.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_all_occurrence_positive_core_hit_cert as all_charge
import cm2_gate34_dyadic_transverse_recovery_shell_cert as phase_shell
import cm2_gate34_parameter_dq_all_scale_shell_cert as parameter
import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 2048

DEPENDENCIES = {
    "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json": (
        "fa590ec6fbaeb08b6f5d9e38d45c2fdc3a06dc170451ded93892f7c531653b51"
    ),
    "cm2_gate34_all_occurrence_positive_core_hit_cert.py": (
        "98c7642856bac56a5309a0fcc6a362e971f25f08c3b52292aaa13eace7d2e76f"
    ),
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": (
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458"
    ),
    "cm2_gate34_dyadic_transverse_recovery_shell_cert.py": (
        "21c683c89881fa5b6acec98b905f0c5be7ff0b2b7c1e5c2309dcc51762dfb6db"
    ),
    "cm2_gate3_endpoint_identity_refinement_cert.py": (
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563"
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


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    manifest = json.loads(
        (
            HERE
            / "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    registry = manifest["result"]["all_occurrence_positive_core_hit_registry"]
    assert registry["charged_occurrence_count"] == 64
    assert registry["charged_oriented_branch_count"] == 128
    assert manifest["verdict"]["first_core_stopping_time"] == "NOT_CERTIFIED"


def core_payload(core: Any) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: Any) -> str:
    return "core:" + canonical_digest(core_payload(core))


def classify_core_state(
    target_id: str,
    normal_x: arb,
    normal_y: arb,
    ux: arb,
    uy: arb,
) -> dict[str, Any]:
    """Classify one entire Arb state as inside one core or outside all."""
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
    inside: list[str] = []
    ambiguous: list[str] = []
    for core in core_cert.physical_cores():
        if core.chart_id != chart_id:
            continue
        identifier = core_id(core)
        if (
            bool(t > charge.arbq(core.t0))
            and bool(t < charge.arbq(core.t1))
            and bool(p > charge.arbq(core.p0))
            and bool(p < charge.arbq(core.p1))
        ):
            inside.append(identifier)
            continue
        separated = (
            bool(t < charge.arbq(core.t0))
            or bool(t > charge.arbq(core.t1))
            or bool(p < charge.arbq(core.p0))
            or bool(p > charge.arbq(core.p1))
        )
        if not separated:
            ambiguous.append(identifier)
    assert not ambiguous
    assert len(inside) <= 1
    if inside:
        return {
            "status": "strict_inside_one_core",
            "core_id": inside[0],
            "chart_id": chart_id,
        }
    return {
        "status": "strict_outside_all_24_cores",
        "core_id": None,
        "chart_id": chart_id,
    }


def occurrence_specifications(
    maximal_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    specifications: dict[str, dict[str, Any]] = {}
    for occurrence_id, (
        chart_id,
        z_text,
        expected_time,
        radius_power,
    ) in sorted(all_charge.NEW_CHARGES.items()):
        proposal = all_charge.floating_proposal(
            by_id[occurrence_id], chart_id, z_text, expected_time
        )
        proposal["radius_power"] = radius_power
        proposal["origin"] = "new_62_binary64_proposal_Arb_admission"
        specifications[occurrence_id] = proposal
    for occurrence_id, old in sorted(charge.SELECTED.items()):
        row = by_id[occurrence_id]
        specifications[occurrence_id] = {
            "occurrence_id": occurrence_id,
            "source_chart": row["witness"]["chart_id"],
            "z": str(Q(row["witness"]["z"]) + Q(old["z_shift"])),
            "post_suffix_collision_count_to_core": 20,
            "suffix_and_future_targets": list(
                old["suffix_and_future_targets"]
            ),
            "destination_chart": old["destination_chart"],
            "radius_power": charge.WIDTH_POWER,
            "origin": "imported_2_frozen_proposal_Arb_readmission",
        }
    assert len(specifications) == 64
    assert set(specifications) == set(by_id)
    return specifications


def physical_row_and_owner_audit(
    original_row: dict[str, Any], specification: dict[str, Any]
) -> dict[str, Any]:
    """Recheck both global first-collision owners on the exact charged box."""
    radius_power = specification["radius_power"]
    radius = Q(1, 2**radius_power)
    row = dict(original_row)
    row["witness"] = dict(row["witness"])
    row["witness"]["chart_id"] = specification["source_chart"]
    row["witness"]["z"] = specification["z"]
    z = Q(specification["z"])
    box = bulk.Box(
        row["witness"]["chart_id"],
        row["target"],
        row["epsilon"],
        z - radius,
        z + radius,
        Q(0),
        Q(0),
        radius_power,
    )
    kind, data = endpoint.classify_box(box)
    assert kind == "physical_immutable_subrow"
    assert data is not None
    assert data["miss_target"] == row["miss_target"]
    assert data["polarity"] == row["parameter_coarea_polarity"]

    geometry = bulk.tangent_geometry(
        box.chart_id,
        box.z0,
        box.z1,
        box.s0,
        box.s1,
        box.target_id,
        box.epsilon,
    )
    assert geometry is not None
    _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, s = geometry
    source = row["source"]
    source_id = f"{source}[0,0]"
    direct_rows = phase_shell.centered_candidate_rows(
        qx, qy, ux, uy, s, 0, 0, source_id
    )
    tangent_radius = phase_shell.obstacle_radius(row["target"])
    direct_rows[row["target"]] = (
        ell_t,
        row["epsilon"] * tangent_radius,
        tangent_radius,
    )
    target = bulk.TARGET_BY_ID[row["target"]]
    post_rows = phase_shell.centered_candidate_rows(
        qx, qy, ux, uy, s, target.ix, target.iy, row["target"]
    )
    post_rows[row["target"]] = direct_rows[row["target"]]

    magnitude = bulk.arb_interval(Q(0), radius)
    polarity = row["parameter_coarea_polarity"]
    eta_target = parameter.eta(source, row["target"])
    positive_transversality = (
        polarity * row["epsilon"] * eta_target * uy
    )
    assert bool(positive_transversality > 0)

    miss_negative_discriminant_factor = (
        2 * tangent_radius * positive_transversality
        + uy * uy * magnitude
    )
    assert bool(miss_negative_discriminant_factor > 0)
    miss_rows = parameter.shifted_rows(
        direct_rows, source, ux, uy, -polarity * magnitude
    )
    # On the open miss side the tangent target has
    # Delta=-r*(2*R*c+u_y^2*r)<0, so only that target is removed.
    miss_rows.pop(row["target"])
    miss_state = phase_shell.direct_suffix_state(
        miss_rows, row["miss_target"], arb(0), ux, uy
    )

    square_root_power = (radius_power - 2) // 2
    parameter.SQRT_DISCRIMINANT_UPPER = Q(1, 2**square_root_power)
    hit_state = parameter.all_scale_hit_suffix_state(
        post_rows,
        source,
        row["target"],
        row["miss_target"],
        row["epsilon"],
        polarity,
        ux,
        uy,
        magnitude,
    )
    assert miss_state is not None
    assert hit_state is not None
    assert miss_state["cell"] == hit_state["cell"]
    suffix_chart = (
        f"{bulk.TARGET_BY_ID[row['miss_target']].obstacle}:"
        f"{miss_state['cell']}"
    )
    payload = {
        "occurrence_id": row["occurrence_id"],
        "source_box": box.key(),
        "radius_power": radius_power,
        "direct_candidate_count": len(direct_rows),
        "post_tangent_candidate_count": len(post_rows),
        "hit_first_target": row["target"],
        "hit_second_target": row["miss_target"],
        "miss_first_target": row["miss_target"],
        "hit_state": {key: str(value) for key, value in hit_state.items()},
        "miss_state": {key: str(value) for key, value in miss_state.items()},
    }
    return {
        "source_owner_audit_id": "source-owner:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "exact_charged_source_box": box.key(),
        "physical_immutable_subrow_label_rechecked": True,
        "miss_target_and_parameter_polarity_rechecked": True,
        "hit_tangent_target_is_global_first_collision": True,
        "hit_regular_suffix_target_is_global_second_collision": True,
        "miss_tangent_discriminant_strictly_negative_on_open_side": True,
        "miss_regular_suffix_target_is_global_first_collision": True,
        "two_parameter_sides_share_suffix_chart": True,
        "suffix_chart": suffix_chart,
        "candidate_universe_radius_in_lattice_cells": 4,
        "direct_candidate_count": len(direct_rows),
        "post_tangent_candidate_count": len(post_rows),
        "hit_square_root_upper_power": square_root_power,
        "parameter_magnitude_interval": ["0_open", str(radius)],
    }


def replay_first_stopping_branch(
    original_row: dict[str, Any],
    specification: dict[str, Any],
    side: str,
    owner_audit_id: str,
) -> dict[str, Any]:
    radius_power = specification["radius_power"]
    radius = Q(1, 2**radius_power)
    charge.BASE_HALF_WIDTH = radius
    charge.PARAMETER_RADIUS = radius
    charge.SQRT_DISCRIMINANT_UPPER = Q(
        1, 2 ** ((radius_power - 2) // 2)
    )
    row = dict(original_row)
    row["witness"] = dict(row["witness"])
    row["witness"]["chart_id"] = specification["source_chart"]
    row["witness"]["z"] = specification["z"]
    magnitude = charge.interval(Q(0), radius)
    if side == "hit":
        state = charge.hit_suffix_state(row, magnitude)
        displacement = row["parameter_coarea_polarity"] * magnitude
        source_collision_count = 2
    else:
        state = charge.direct_suffix_state(row, magnitude)
        displacement = -row["parameter_coarea_polarity"] * magnitude
        source_collision_count = 1
    qx, qy, ux, uy, normal_x, normal_y, suffix_record = state
    itinerary = specification["suffix_and_future_targets"]
    assert suffix_record["target"] == itinerary[0] == row["miss_target"]
    current_id = itinerary[0]
    classifications = [
        classify_core_state(current_id, normal_x, normal_y, ux, uy)
    ]
    step_records = [suffix_record]
    for expected_id in itinerary[1:]:
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, expected_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        current_id = expected_id
        step_records.append(record)
        classifications.append(
            classify_core_state(current_id, normal_x, normal_y, ux, uy)
        )
    first_time = specification["post_suffix_collision_count_to_core"]
    assert len(classifications) == first_time + 1
    assert all(
        item["status"] == "strict_outside_all_24_cores"
        for item in classifications[:-1]
    )
    terminal = classifications[-1]
    assert terminal["status"] == "strict_inside_one_core"
    assert terminal["chart_id"] == specification["destination_chart"]
    if "destination_core_id" in specification:
        assert terminal["core_id"] == specification["destination_core_id"]
    payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "source_owner_audit_id": owner_audit_id,
        "radius_power": radius_power,
        "itinerary": itinerary,
        "first_core_time": first_time,
        "destination_core_id": terminal["core_id"],
    }
    return {
        "first_stopping_branch_id": "first-core:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "source_owner_audit_id": owner_audit_id,
        "source_collision_count_to_regular_suffix": source_collision_count,
        "first_core_stopping_time_from_regular_suffix": first_time,
        "strict_outside_core_state_count_before_stop": first_time,
        "destination_core_id": terminal["core_id"],
        "destination_chart": terminal["chart_id"],
        "terminal_core_membership_strict_on_entire_cylinder": True,
        "every_preterminal_state_strictly_outside_all_24_cores": True,
        "all_listed_first_collision_decisions_unique_and_regular": True,
        "complete_itinerary_sha256": hashlib.sha256(
            "\n".join(itinerary).encode("utf-8")
        ).hexdigest(),
        "step_records_sha256": canonical_digest(step_records),
        "classification_records_sha256": canonical_digest(classifications),
    }


def first_stopping_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    assert len(by_id) == 64
    specifications = occurrence_specifications(maximal_rows)
    all_charge.refresh_arb_constants()
    assert ctx.prec == PRECISION_BITS

    owner_rows = []
    branch_rows = []
    for occurrence_id, specification in sorted(specifications.items()):
        owner = physical_row_and_owner_audit(
            by_id[occurrence_id], specification
        )
        owner_rows.append(owner)
        for side in ("hit", "miss"):
            branch_rows.append(
                replay_first_stopping_branch(
                    by_id[occurrence_id],
                    specification,
                    side,
                    owner["source_owner_audit_id"],
                )
            )
    owner_rows.sort(key=canonical_json)
    branch_rows.sort(key=canonical_json)
    assert len(owner_rows) == 64
    assert len(branch_rows) == 128
    assert len({row["source_owner_audit_id"] for row in owner_rows}) == 64
    assert len({row["first_stopping_branch_id"] for row in branch_rows}) == 128

    old_subset_count = 0
    for occurrence_id, selected in sorted(charge.SELECTED.items()):
        predecessor = parameter.certify_germ(by_id[occurrence_id])
        shifted_radius = Q(1, 2**charge.WIDTH_POWER)
        assert (
            abs(Q(selected["z_shift"])) + shifted_radius
            < Q(predecessor["base_half_width"])
        )
        assert shifted_radius < parameter.PARAMETER_RADIUS
        old_subset_count += 1
    assert old_subset_count == 2

    time_histogram = Counter(
        row["first_core_stopping_time_from_regular_suffix"]
        for row in branch_rows
    )
    expected_histogram = {
        "2": 44,
        "3": 20,
        "4": 16,
        "7": 16,
        "8": 8,
        "9": 8,
        "16": 4,
        "19": 8,
        "20": 4,
    }
    assert {str(key): value for key, value in sorted(time_histogram.items())} == (
        expected_histogram
    )
    outside_count = sum(
        row["strict_outside_core_state_count_before_stop"]
        for row in branch_rows
    )
    assert outside_count == 756
    destination_ids = {row["destination_core_id"] for row in branch_rows}
    assert len(destination_ids) == 14
    branch_key_mapping = [
        {
            "occurrence_id": row["occurrence_id"],
            "side": row["side"],
            "suffix_relative_first_core_time": row[
                "first_core_stopping_time_from_regular_suffix"
            ],
            "destination_core_id": row["destination_core_id"],
        }
        for row in branch_rows
    ]
    return {
        "maximal_reference_occurrence_count": 64,
        "charged_oriented_cylinder_count": 128,
        "exact_source_boxes_reclassified_as_physical_immutable_subrows": 64,
        "hit_global_first_owner_audits": 64,
        "miss_global_first_owner_audits": 64,
        "old_frozen_boxes_strictly_contained_in_predecessor_germs": 2,
        "all_hit_tangent_targets_are_global_first_collisions": True,
        "all_hit_regular_suffix_targets_are_global_second_collisions": True,
        "all_miss_regular_suffix_targets_are_global_first_collisions": True,
        "all_hit_miss_pairs_share_the_same_regular_suffix_chart": True,
        "first_core_stopping_cylinder_count": 128,
        "first_core_stopping_clock_origin": (
            "regular_suffix_state_at_time_0"
        ),
        "source_to_regular_suffix_collisions_are_not_in_stopping_clock": True,
        "first_core_stopping_time_histogram_by_oriented_cylinder": (
            expected_histogram
        ),
        "maximum_first_core_stopping_time_from_regular_suffix": 20,
        "strict_preterminal_outside_all_24_core_state_count": outside_count,
        "strict_terminal_inside_one_core_state_count": 128,
        "ambiguous_core_classification_count": 0,
        "distinct_destination_core_count": len(destination_ids),
        "all_128_displayed_entrance_words_are_first_core_stopping_words": True,
        "source_owner_audit_rows_sha256": canonical_digest(owner_rows),
        "first_stopping_branch_rows_sha256": canonical_digest(branch_rows),
        "branch_key_to_suffix_relative_first_time_and_core_sha256": (
            canonical_digest(branch_key_mapping)
        ),
        "destination_core_ids_sha256": canonical_digest(sorted(destination_ids)),
        "first_source_owner_audit_id": owner_rows[0]["source_owner_audit_id"],
        "last_source_owner_audit_id": owner_rows[-1]["source_owner_audit_id"],
        "first_stopping_branch_id": branch_rows[0]["first_stopping_branch_id"],
        "last_stopping_branch_id": branch_rows[-1]["first_stopping_branch_id"],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.all-occurrence-first-core-stopping.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "floating_search_role": "proposal_only",
            "admission_engine": "python-flint Arb",
            "precision_bits": PRECISION_BITS,
            "candidate_universe_radius_in_lattice_cells": 4,
        },
        "all_occurrence_first_core_stopping_registry": (
            first_stopping_registry()
        ),
        "strict_nonpromotion": {
            "positive_cylinders_cover_entire_maximal_rows": False,
            "labelled_coordinate_volume_is_collision_SRB_fraction": False,
            "whole_germ_domain_first_core_stopping": "NOT_CERTIFIED",
            "normalized_selected_core_hit_fraction": "NOT_CERTIFIED",
            "quantitative_cemetery_tail": "NOT_CERTIFIED",
            "post_core_first_return_operator": "NOT_CERTIFIED",
            "common_two_view_restriction": "NOT_CERTIFIED",
            "common_strong_space_DQ_MT_DQ_FACE_recovery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("CHARGED_FIRST_CORE_STOPPING_CYLINDERS_128: CERTIFIED")
    print("MAXIMUM_FIRST_CORE_STOPPING_TIME_20: CERTIFIED")
    print("GLOBAL_HIT_MISS_SOURCE_OWNER_AUDITS_64_64: CERTIFIED")
    print("WHOLE_GERM_FIRST_CORE_STOPPING: NOT_CERTIFIED")
    print("QUANTITATIVE_CEMETERY_TAIL: NOT_CERTIFIED")
    print("INDUCED_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
