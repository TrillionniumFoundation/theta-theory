#!/usr/bin/env python3
"""Local post-core first-return and finite-horizon tail ledger.

The four frozen 2^-8000 source-current boxes start at strict interiors of the
24-core union and have 2018 interval-validated post-core collisions.  This
certificate classifies every one of those 8072 whole-box states against all
24 frozen core rectangles.  It materializes the first positive return time
when a whole box re-enters a strict core interior and otherwise records an
unresolved excursion survivor through the horizon.

These boxes are labelled ``(z,h)`` source-current parameter boxes.  For a
fixed parameter they are one-dimensional source curves; they are not
two-dimensional collision-core rectangles.  Therefore the three finite
returns below are local return-current cylinders, not a complete induced
transfer operator.  The exact 3/4 return fraction and 1/4 survivor fraction
refer only to the equal labelled coordinate volumes of these four boxes and
are not collision-SRB probabilities.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate34_all_occurrence_first_core_stopping_cert as first_stopping
import cm2_gate34_charged_2018_regular_dwell_cert as frozen_dwell
import cm2_gate34_materialized_2018_dwell_cylinders_cert as materialized
import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate3_global_borel_current_assembly_cert as current


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 8192
HORIZON = 2018
SINGLE_BOX_VOLUME_POWER = 15998

DEPENDENCIES = {
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2_gate34_all_occurrence_first_core_stopping_cert.py": (
        "8a22c1a2483822b849562acb06775298a8e9d3a84d753e29ebe86229d35ad1fb"
    ),
    "cm2-gate34-materialized-2018-dwell-cylinders-manifest-2026-07-17.json": (
        "4c391b75e95b7b04bc377d23131dd6244410da3c75a33f39ade3df0648b31bce"
    ),
    "cm2_gate34_materialized_2018_dwell_cylinders_cert.py": (
        "e77e7cb6a174dc4f5fbe7b2890927596d8a87a98b17f66dfa3867f8a4a4bd4b1"
    ),
    "cm2_gate34_charged_2018_regular_dwell_cert.py": (
        "f2d629880621b2623d4a408ce9dfd4334b7728e8e26115a48461c2ccaf352f75"
    ),
    "cm2_gate34_positive_core_hit_charge_cert.py": (
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
}

EXPECTED_CORE_HIT_TIMES = {
    ("occ:c5fde0378e6e76eec93a0ceb", "hit"): [545, 1604],
    ("occ:c5fde0378e6e76eec93a0ceb", "miss"): [1531],
    ("occ:f2b4833eb8dccd403eec3485", "hit"): [],
    ("occ:f2b4833eb8dccd403eec3485", "miss"): [649],
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
    stopping_manifest = json.loads(
        (
            HERE
            / "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
        ).read_text(encoding="utf-8")
    )
    assert stopping_manifest["verdict"][
        "charged_first_core_stopping_cylinders_128"
    ] == "CERTIFIED"
    dwell_manifest = json.loads(
        (
            HERE
            / "cm2-gate34-materialized-2018-dwell-cylinders-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    registry = dwell_manifest["result"][
        "materialized_2018_dwell_cylinder_registry"
    ]
    assert registry["explicit_positive_dwell_cylinder_count"] == 4
    assert registry[
        "total_interval_validated_post_core_regular_collisions"
    ] == 8072
    assert dwell_manifest["verdict"]["direct_fixed_core_operator_power_attachment_on_4_boxes"] == "REFUTED"


def replay_return_box(
    row: dict[str, Any], side: str, specification: dict[str, Any]
) -> dict[str, Any]:
    point_word, point_destination_core_id = materialized.point_post_core_word(
        row, side, specification
    )
    assert len(point_word) == HORIZON
    state = materialized.interval_suffix_state(row, side)
    qx, qy, ux, uy, normal_x, normal_y, current_id, displacement = state
    entrance = specification["suffix_and_future_targets"]
    assert current_id == entrance[0]
    for target_id in entrance[1:]:
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, _record = state
        current_id = target_id
    initial = first_stopping.classify_core_state(
        current_id, normal_x, normal_y, ux, uy
    )
    assert initial["status"] == "strict_inside_one_core"
    assert initial["core_id"] == point_destination_core_id

    classifications = []
    core_hit_times = []
    core_hit_ids = []
    collision_records = []
    for time, target_id in enumerate(point_word, start=1):
        state = charge.step_expected(
            qx, qy, ux, uy, current_id, target_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        assert bool(arb(record["cosine"]) > charge.arbq(Q(1, 1000)))
        current_id = target_id
        classification = first_stopping.classify_core_state(
            current_id, normal_x, normal_y, ux, uy
        )
        classifications.append(classification)
        collision_records.append(record)
        if classification["status"] == "strict_inside_one_core":
            core_hit_times.append(time)
            core_hit_ids.append(classification["core_id"])
        else:
            assert classification["status"] == "strict_outside_all_24_cores"
    key = (row["occurrence_id"], side)
    assert core_hit_times == EXPECTED_CORE_HIT_TIMES[key]
    first_return_time = core_hit_times[0] if core_hit_times else None
    first_return_core_id = core_hit_ids[0] if core_hit_ids else None
    if first_return_time is None:
        assert all(
            item["status"] == "strict_outside_all_24_cores"
            for item in classifications
        )
        pre_first_outside_count = HORIZON
        outcome = "tau_core_plus_strictly_greater_than_2018"
    else:
        assert all(
            item["status"] == "strict_outside_all_24_cores"
            for item in classifications[: first_return_time - 1]
        )
        assert classifications[first_return_time - 1]["status"] == (
            "strict_inside_one_core"
        )
        pre_first_outside_count = first_return_time - 1
        outcome = "finite_first_return_current_cylinder"
    payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "initial_core_id": initial["core_id"],
        "core_hit_times": core_hit_times,
        "core_hit_ids": core_hit_ids,
        "post_core_itinerary_sha256": hashlib.sha256(
            "\n".join(point_word).encode("utf-8")
        ).hexdigest(),
    }
    return {
        "local_return_ledger_id": "local-return:" + canonical_digest(payload),
        "branch_key": f"{row['occurrence_id']}|{side}",
        "occurrence_id": row["occurrence_id"],
        "parameter_side": side,
        "source_object_type": "labelled_(z,h)_source-current_box",
        "fixed_parameter_source_dimension": 1,
        "box_is_full_two_dimensional_collision_core_rectangle": False,
        "initial_core_id": initial["core_id"],
        "post_core_first_return_clock": "tau_C_plus=inf{n>=1:T^n(x) in C_24}",
        "outcome": outcome,
        "first_return_time": (
            first_return_time if first_return_time is not None else ">2018"
        ),
        "first_return_core_id": first_return_core_id,
        "all_core_reentry_times_through_2018": core_hit_times,
        "all_core_reentry_ids_through_2018": core_hit_ids,
        "strict_outside_state_count_before_first_return_or_horizon": (
            pre_first_outside_count
        ),
        "strict_outside_state_count_through_2018": sum(
            item["status"] == "strict_outside_all_24_cores"
            for item in classifications
        ),
        "strict_core_reentry_state_count_through_2018": len(core_hit_times),
        "ambiguous_core_classification_count": 0,
        "all_2018_collisions_unique_and_regular_on_entire_box": True,
        "singular_cemetery_hit_through_2018": False,
        "single_labelled_coordinate_box_volume": "2^-15998",
        "post_core_itinerary_sha256": payload["post_core_itinerary_sha256"],
        "collision_records_sha256": canonical_digest(collision_records),
        "core_classification_records_sha256": canonical_digest(
            classifications
        ),
    }


def local_return_tail_registry() -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    materialized.refresh_constants()
    assert ctx.prec == PRECISION_BITS
    rows = []
    for occurrence_id, specification in sorted(charge.SELECTED.items()):
        row = dict(by_id[occurrence_id])
        row["witness"] = dict(row["witness"])
        row["witness"]["z"] = str(
            Q(row["witness"]["z"]) + Q(specification["z_shift"])
        )
        for side in ("hit", "miss"):
            rows.append(replay_return_box(row, side, specification))
    rows.sort(key=lambda item: item["branch_key"])
    assert len(rows) == 4
    assert len({row["branch_key"] for row in rows}) == 4
    assert len({row["local_return_ledger_id"] for row in rows}) == 4
    keyed_outcomes = {
        row["branch_key"]: {
            "first_return_time": row["first_return_time"],
            "first_return_core_id": row["first_return_core_id"],
            "all_core_reentry_times_through_2018": row[
                "all_core_reentry_times_through_2018"
            ],
        }
        for row in rows
    }
    expected_keyed_times = {
        "occ:c5fde0378e6e76eec93a0ceb|hit": 545,
        "occ:c5fde0378e6e76eec93a0ceb|miss": 1531,
        "occ:f2b4833eb8dccd403eec3485|hit": ">2018",
        "occ:f2b4833eb8dccd403eec3485|miss": 649,
    }
    assert {
        key: value["first_return_time"]
        for key, value in keyed_outcomes.items()
    } == expected_keyed_times
    finite_rows = [row for row in rows if isinstance(row["first_return_time"], int)]
    survivor_rows = [row for row in rows if row["first_return_time"] == ">2018"]
    assert len(finite_rows) == 3
    assert len(survivor_rows) == 1
    assert sum(row["strict_outside_state_count_through_2018"] for row in rows) == 8068
    assert sum(row["strict_core_reentry_state_count_through_2018"] for row in rows) == 4
    total_volume = Q(1, 2**15996)
    returning_volume = Q(3, 2**15998)
    survivor_volume = Q(1, 2**15998)
    assert returning_volume + survivor_volume == total_volume
    return {
        "materialized_source_current_box_count": 4,
        "Arb_precision_bits": PRECISION_BITS,
        "post_core_classification_horizon": HORIZON,
        "whole_box_core_classification_count": 8072,
        "ambiguous_core_classification_count": 0,
        "strict_outside_core_state_count": 8068,
        "strict_core_reentry_state_count": 4,
        "finite_first_return_current_cylinder_count": len(finite_rows),
        "unresolved_excursion_survivor_box_count_after_2018": len(
            survivor_rows
        ),
        "branch_key_to_return_outcome": keyed_outcomes,
        "first_return_time_multiset": [545, 649, 1531, ">2018"],
        "exact_labelled_coordinate_tail": [
            {"horizon_range": "0<=n<=544", "fraction_tau_C_plus_gt_n": "1"},
            {"horizon_range": "545<=n<=648", "fraction_tau_C_plus_gt_n": "3/4"},
            {"horizon_range": "649<=n<=1530", "fraction_tau_C_plus_gt_n": "1/2"},
            {"horizon_range": "1531<=n<=2018", "fraction_tau_C_plus_gt_n": "1/4"},
        ],
        "return_by_2018_labelled_coordinate_fraction": "3/4",
        "unresolved_after_2018_labelled_coordinate_fraction": "1/4",
        "singular_cemetery_labelled_coordinate_fraction_through_2018": "0",
        "total_labelled_coordinate_volume": "2^-15996",
        "finite_return_labelled_coordinate_volume": "3*2^-15998",
        "survivor_labelled_coordinate_volume": "2^-15998",
        "all_8072_collisions_unique_and_regular_on_entire_boxes": True,
        "all_8072_states_strictly_classified_against_all_24_cores": True,
        "local_return_ledger_rows_sha256": canonical_digest(rows),
        "branch_key_to_return_outcome_sha256": canonical_digest(keyed_outcomes),
        "first_local_return_ledger_id": rows[0]["local_return_ledger_id"],
        "last_local_return_ledger_id": rows[-1]["local_return_ledger_id"],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.local-core-return-tail.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "floating_pilot_role": "itinerary_proposal_only",
            "admission_engine": "python-flint Arb",
            "precision_bits": PRECISION_BITS,
        },
        "local_core_return_tail_registry": local_return_tail_registry(),
        "strict_nonpromotion": {
            "labelled_coordinate_fraction_is_collision_SRB_probability": False,
            "source_current_boxes_are_full_collision_core_rectangles": False,
            "three_local_returns_construct_the_24_core_induced_operator": False,
            "unresolved_survivor_is_nonreturning_cemetery": False,
            "quantitative_global_cemetery_tail": "NOT_CERTIFIED",
            "new_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
            "common_two_view_restriction": "NOT_CERTIFIED",
            "common_strong_space_induced_recovery_operator": "NOT_CERTIFIED",
            "native_global_2018_12108_dwell": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("LOCAL_FIRST_RETURN_CURRENT_CYLINDERS_3: CERTIFIED")
    print("LOCAL_TAU_CORE_PLUS_GREATER_THAN_2018_SURVIVOR_BOXES_1: CERTIFIED")
    print("LOCAL_LABELLED_RETURN_FRACTION_BY_2018_3_OVER_4: CERTIFIED")
    print("SINGULAR_CEMETERY_THROUGH_2018_ON_FOUR_BOXES_0: CERTIFIED")
    print("FULL_24_CORE_INDUCED_OPERATOR: NOT_CERTIFIED")
    print("GLOBAL_CEMETERY_TAIL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
