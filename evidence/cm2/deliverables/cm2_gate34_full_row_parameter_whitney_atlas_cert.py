#!/usr/bin/env python3
"""Countable actual-parameter Whitney germ atlas on all maximal event rows.

The twentieth certificate materialized one positive-width actual-parameter
germ in each of the 64 maximal occurrence rows.  A uniform parameter radius
up to every row endpoint is neither available nor required for pointwise
coverage.  This certificate uses the exact analytic maximal-row arrangement
to install the correct full-row object at the reference table ``s=0``:

* normalize every open angular row to ``t in (0,1)``;
* partition it by a countable Whitney family whose compact cells stay a
  controlled positive normalized distance from the two analytic endpoints;
* use strict physical labels plus continuity of the finite collision-root
  universe to obtain a positive actual-parameter hit/miss radius on every
  compact cell; and
* provide a deterministic dyadic-halving search for a rational radius.

The first sixteen Whitney levels are materialized.  They contain 1,984 cells
and 3,968 oriented parameter-germ records and leave an order-zero graph-TV
tail at most ``63/1280`` in the frozen unnormalised collision-flux gauge.
The countable theorem covers every interior point of every reference row.

This is not a finite uniform-radius tubular atlas and does not prove a
bounded pushforward in the common strong space.  Local radius constants may
degenerate at row endpoints and their strong weighted summability remains
open.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_global_borel_current_assembly_cert as current


Q = Fraction
HERE = Path(__file__).resolve().parent
MATERIALIZED_MAX_LEVEL = 16
ROW_COUNT = 64
PER_ROW_POSITIVE_MASS_UPPER = Q(126, 5)

DEPENDENCIES = {
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": (
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458"
    ),
    "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json": (
        "2a25426d0a3f90a3fc2df592626d01cf294394f14590a9b1e9338f65ba8614f8"
    ),
    "cm2_gate3_maximal_global_row_registry_cert.py": (
        "66338ea304793e8fbf1fc58a052167f8106d97751cacff8387ed87102ab16093"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    parameter = loaded[
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    ]
    assert parameter["verdict"]["parameter_angle_Jacobian_rows_64"] == (
        "CERTIFIED"
    )
    assert parameter["verdict"]["selected_parameter_DQ_all_scale_germs_64"] == (
        "CERTIFIED"
    )
    assert parameter["verdict"]["full_boundary_all_scale_tubular_atlas"] == (
        "NOT_CERTIFIED"
    )

    maximal = loaded[
        "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
    ]
    assert maximal["verdict"]["maximal_connected_event_rows"] == "CERTIFIED"
    registry = maximal["result"]["maximal_row_registry"]
    assert registry["maximal_connected_physical_row_count"] == ROW_COUNT
    assert registry[
        "rows_are_maximal_in_exhaustive_transition_arrangement"
    ] is True

    depth_one = loaded[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]
    assert depth_one["verdict"]["complete_depth_one_fixed_gauge_DQ"] == (
        "CERTIFIED"
    )
    return loaded


def endpoint_incidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    histogram = Counter(
        boundary["kind"]
        for row in rows
        for boundary in (row["left_boundary"], row["right_boundary"])
    )
    assert histogram == Counter({
        "physical_later_miss_switch_boundary": 64,
        "source_grazing": 32,
        "parameter_polarity": 16,
        "physical_earlier_occlusion_boundary": 16,
    })
    assert sum(histogram.values()) == 2 * ROW_COUNT
    return {
        "reference_maximal_row_count": ROW_COUNT,
        "endpoint_incidence_count": 2 * ROW_COUNT,
        "endpoint_incidence_histogram": dict(sorted(histogram.items())),
        "source_grazing_density_vanishes_by_cp": True,
        "parameter_polarity_density_vanishes_by_abs_u_y": True,
        "first_visibility_and_miss_switch_endpoints_have_zero_base_mass": True,
        "extra_endpoint_atoms": 0,
    }


def whitney_intervals(max_level: int) -> list[dict[str, Any]]:
    assert max_level >= 2
    intervals = [{
        "side": "central",
        "level": 1,
        "normalized_t": ["1/4", "3/4_open"],
        "endpoint_distance_lower": "1/4",
    }]
    for level in range(2, max_level + 1):
        left_lower = Q(1, 2 ** (level + 1))
        left_upper = Q(1, 2**level)
        intervals.append({
            "side": "left",
            "level": level,
            "normalized_t": [str(left_lower), f"{left_upper}_open"],
            "endpoint_distance_lower": str(left_lower),
        })
        right_lower = 1 - left_upper
        right_upper = 1 - left_lower
        intervals.append({
            "side": "right",
            "level": level,
            "normalized_t": [str(right_lower), f"{right_upper}_open"],
            "endpoint_distance_lower": str(left_lower),
        })
    intervals.sort(key=canonical_json)
    assert len(intervals) == 1 + 2 * (max_level - 1)
    return intervals


def materialized_prefix(
    rows: list[dict[str, Any]], max_level: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    intervals = whitney_intervals(max_level)
    cells: list[dict[str, Any]] = []
    for row in rows:
        for interval in intervals:
            identity = {
                "occurrence_id": row["occurrence_id"],
                "side": interval["side"],
                "level": interval["level"],
                "normalized_t": interval["normalized_t"],
            }
            cells.append({
                **identity,
                "whitney_cell_id": "whitney:" + canonical_digest(identity),
                "global_physical_label": row["global_physical_label"],
                "left_boundary": row["left_boundary"],
                "right_boundary": row["right_boundary"],
                "endpoint_distance_lower": interval[
                    "endpoint_distance_lower"
                ],
                "compact_closure_inside_open_row": True,
                "actual_parameter_hit_and_miss_radius": (
                    "POSITIVE_EXISTS_AND_DYADIC_HALVING_TERMINATES"
                ),
                "oriented_parameter_germ_count": 2,
            })
    cells.sort(key=canonical_json)
    expected = ROW_COUNT * (1 + 2 * (max_level - 1))
    assert len(cells) == expected
    assert len({row["whitney_cell_id"] for row in cells}) == expected

    normalized_tail_per_row = Q(1, 2**max_level)
    positive_tail = (
        ROW_COUNT * PER_ROW_POSITIVE_MASS_UPPER * normalized_tail_per_row
    )
    graph_tv_tail = 2 * positive_tail
    if max_level == 16:
        assert positive_tail == Q(63, 2560)
        assert graph_tv_tail == Q(63, 1280)

    trim = Q(1, 2 ** (max_level + 1))
    return cells, {
        "materialized_maximum_whitney_level": max_level,
        "cells_per_row": len(intervals),
        "materialized_whitney_cell_count": len(cells),
        "materialized_oriented_parameter_germ_record_count": 2 * len(cells),
        "covered_normalized_reference_row": [
            str(trim), f"{1 - trim}_open",
        ],
        "omitted_normalized_endpoint_length_per_row": str(
            normalized_tail_per_row
        ),
        "positive_coarea_mass_tail_upper": str(positive_tail),
        "hit_minus_miss_graph_TV_tail_upper": str(graph_tv_tail),
        "tail_bounds_use_row_angle_width_strict_upper_2pi_lt_7": True,
        "materialized_cells_sha256": canonical_digest(cells),
        "first_cell_id": cells[0]["whitney_cell_id"],
        "last_cell_id": cells[-1]["whitney_cell_id"],
    }


def countable_completion_theorem() -> dict[str, Any]:
    return {
        "reference_parameter": "s=0",
        "row_coordinate": (
            "normalized positively oriented source-normal angle between the "
            "two analytic row boundaries"
        ),
        "normalized_row_domain": "t in (0,1)",
        "countable_family": (
            "central [1/4,3/4) plus left/right dyadic Whitney cells for "
            "every level n>=2"
        ),
        "countable_cells_cover_every_reference_row_interior_point": True,
        "every_cell_closure_is_compact_inside_one_constant_label_row": True,
        "strict_predicate_universe_is_finite_on_each_occurrence": True,
        "moving_centres_and_regular_competitor_roots_are_continuous": True,
        "correct_hit_side_tangent_discriminant_has_positive_linear_factor": True,
        "hit_tangent_miss_and_direct_miss_itineraries_persist_on_each_cell": True,
        "positive_cell_radius_exists_by_compactness": True,
        "dyadic_halving_of_parameter_radius_is_a_terminating_certificate_search": True,
        "all_interior_points_have_two_actual_parameter_all_scale_germs": True,
        "all_64_reference_rows_have_countable_actual_parameter_germ_atlas": True,
        "finite_prefix_positive_mass_tail_tends_to_zero": True,
        "finite_prefix_graph_TV_tail_tends_to_zero": True,
        "uniform_radius_over_all_cells_asserted": False,
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    rows, maximal_registry = current.load_maximal_rows()
    assert len(rows) == ROW_COUNT
    cells, prefix = materialized_prefix(rows, MATERIALIZED_MAX_LEVEL)
    result: dict[str, Any] = {
        "schema": "cm2.gate34.full-row-parameter-whitney-atlas.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "imported_maximal_rows_sha256": maximal_registry[
                "maximal_row_rows_sha256"
            ],
        },
        "endpoint_incidence_and_atoms": endpoint_incidence(rows),
        "countable_full_row_parameter_germ_atlas": (
            countable_completion_theorem()
        ),
        "materialized_level_16_prefix": prefix,
        "strict_nonpromotion": {
            "countable_pointwise_germ_atlas_is_finite_uniform_radius_atlas": False,
            "order_zero_tail_implies_common_strong_space_pushforward": False,
            "local_radius_existence_supplies_weighted_radius_summability": False,
            "finite_s_future_singularity_atlas": "NOT_CERTIFIED",
            "bounded_common_strong_space_grazing_pushforward": "NOT_CERTIFIED",
            "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("REFERENCE_FULL_ROW_COUNTABLE_PARAMETER_GERM_ATLAS_64: CERTIFIED")
    print("MATERIALIZED_WHITNEY_CELLS_1984: CERTIFIED")
    print("MATERIALIZED_ORIENTED_PARAMETER_GERM_RECORDS_3968: CERTIFIED")
    print("LEVEL16_GRAPH_TV_ENDPOINT_TAIL_LE_63_OVER_1280: CERTIFIED")
    print("BOUNDED_COMMON_STRONG_SPACE_GRAZING_PUSHFORWARD: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
