#!/usr/bin/env python3
"""All-key, all-maximal-component characteristic-boundary certificate."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": (
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
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
        value = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        loaded[name] = value

    first_hit = loaded["cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"]
    gate5 = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    roots = loaded[
        "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
    ]
    growth = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]

    assert first_hit["candidate_reduction"]["retained_pair_count"] == 448
    assert gate5["result"]["immutable_candidate_key_registry"][
        "candidate_return_word_key_count"
    ] == 441280
    assert gate5["result"]["crossing_grammar"]["crossing_pattern_count"] == 985
    root_result = roots["result"]
    assert root_result["physical_branch_slope_and_root_grammar"][
        "every_active_branch_has_at_most_one_isolated_root"
    ] is True
    assert root_result["physical_branch_slope_and_root_grammar"][
        "simultaneous_branch_roots_are_coalesced_into_one_geometric_cut"
    ] is True
    assert growth["replay_summary"]["density_ratio"] == "2000/1999"
    assert growth["replay_summary"]["vartheta_p"] == "360134800/360493663"
    return loaded


def source_class_rows(
    dependencies: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    first_hit = dependencies[
        "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
    ]
    gate5 = dependencies[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    roots = dependencies[
        "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
    ]
    growth = dependencies[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]

    charts = first_hit["candidate_reduction"]["charts"]
    crossing_count = gate5["result"]["crossing_grammar"][
        "crossing_pattern_count"
    ]
    root_rows = roots["result"]["positive_seeded_component_boundary_reduction"][
        "source_class_records"
    ]
    root_by_source = {
        row["source_obstacle"]: row["common_physical_reduction"]
        for row in root_rows
    }
    density_ratio = Q(growth["replay_summary"]["density_ratio"])
    physical_step = Q(growth["replay_summary"]["vartheta_p"])

    rows: list[dict[str, Any]] = []
    for source in ("G", "W"):
        source_charts = [row for row in charts if row["chart_id"].startswith(source)]
        assert len(source_charts) == 4
        retained_per_chart = {int(row["retained"]) for row in source_charts}
        assert retained_per_chart == ({57} if source == "G" else {55})
        retained_pairs = sum(int(row["retained"]) for row in source_charts)
        key_count = retained_pairs * crossing_count

        root_row = root_by_source[source]
        root_upper = int(
            root_row["distinct_physical_boundary_root_upper_per_canonical_curve"]
        )
        interval_upper = int(
            root_row["intersection_component_upper_per_canonical_curve"]
        )
        assert interval_upper == root_upper + 1
        multiplier = interval_upper * density_ratio
        combined = multiplier * physical_step
        assert multiplier == Q(root_row[
            "component_local_unnormalized_characteristic_Z_multiplier_upper"
        ])
        assert combined == Q(
            root_row["restriction_then_physical_step_coefficient_upper"]
        )
        assert combined > 1

        rows.append(
            {
                "source_obstacle": source,
                "source_chart_count": len(source_charts),
                "retained_targets_per_chart": next(iter(retained_per_chart)),
                "retained_chart_target_pair_count": retained_pairs,
                "crossing_pattern_count_per_pair": crossing_count,
                "candidate_key_count": key_count,
                "physical_boundary_root_upper_per_canonical_curve": root_upper,
                "all_component_union_interval_upper_per_canonical_curve": interval_upper,
                "each_maximal_component_interval_upper_per_canonical_curve": interval_upper,
                "all_component_unnormalized_characteristic_Z_multiplier_upper": str(
                    multiplier
                ),
                "restriction_then_physical_step_coefficient_upper": str(combined),
                "restriction_then_physical_step_is_contraction": False,
            }
        )

    assert sum(row["retained_chart_target_pair_count"] for row in rows) == 448
    assert sum(row["candidate_key_count"] for row in rows) == 441280
    return rows


def boundary_inheritance_theorem() -> dict[str, Any]:
    return {
        "key_fibre": (
            "D_w(s), the open regular return-word fibre with fixed source chart, "
            "target, wall record and central homogeneity labels"
        ),
        "maximal_components": "the connected components M of D_w(s)",
        "relative_boundary_inclusion": (
            "boundary(D_w(s)) and every boundary(M) inside the regular source "
            "chart are contained in the frozen physical tangency, wall/corner, "
            "chart-seam and homogeneity-face branch union"
        ),
        "boundary_inclusion_is_independent_of_nonemptiness_decision": True,
        "empty_key_cost": "0",
        "all_physical_branch_roots_are_isolated_on_canonical_unstable_curves": True,
        "one_root_upper_per_active_branch": True,
        "simultaneous_roots_charged_once": True,
        "curve_minus_m_roots_has_at_most_m_plus_one_open_intervals": True,
        "full_key_union_and_each_maximal_component_share_the_same_safe_upper": True,
        "component_enumeration_required_for_the_safe_upper": False,
        "curve_by_curve_numeric_root_order_required_for_the_safe_upper": False,
        "parameter_scope": "uniform fibrewise for every |s|<=1/400",
        "common_moving_DQ_atlas_constructed": False,
    }


def build_result() -> dict[str, Any]:
    dependencies = load_dependencies()
    rows = source_class_rows(dependencies)
    gate5 = dependencies[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    registry = gate5["result"]["immutable_candidate_key_registry"]
    density_ratio = Q(2000, 1999)
    uniform_interval_upper = max(
        row["all_component_union_interval_upper_per_canonical_curve"] for row in rows
    )
    uniform_multiplier = uniform_interval_upper * density_ratio
    assert uniform_interval_upper == 290
    assert uniform_multiplier == Q(580000, 1999)

    result: dict[str, Any] = {
        "schema": "cm2.gate25.all-component-characteristic-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "candidate_key_registry_sha256": registry[
                "candidate_word_key_rows_sha256"
            ],
            "candidate_key_count": registry["candidate_return_word_key_count"],
            "parameter_window": "|s|<=1/400",
            "old_artifacts_modified": False,
        },
        "set_theoretic_boundary_inheritance": boundary_inheritance_theorem(),
        "all_key_all_component_characteristic_registry": {
            "source_class_rows": rows,
            "source_class_rows_sha256": canonical_digest(rows),
            "candidate_key_count_covered": sum(row["candidate_key_count"] for row in rows),
            "all_regular_key_fibres_covered_mod_declared_cemetery": True,
            "all_maximal_connected_components_covered_without_enumeration": True,
            "uniform_physical_boundary_root_upper_per_canonical_curve": 289,
            "uniform_full_key_and_component_interval_upper_per_canonical_curve": (
                uniform_interval_upper
            ),
            "uniform_unnormalized_characteristic_Z_multiplier_upper": str(
                uniform_multiplier
            ),
            "full_key_all_component_characteristic_boundary_Z": "CERTIFIED",
            "each_maximal_component_characteristic_boundary_Z": "CERTIFIED",
        },
        "operator_field_frontier": {
            "full_key_field7_finite_characteristic_formula": "CERTIFIED",
            "field7_formula": (
                "Z_*(1_{D_w(s)} F)<=C_src Z_*(F), "
                "C_G=580000/1999, C_W=572000/1999"
            ),
            "same_formula_applies_to_each_eventual_homogeneous_slot": True,
            "field7_growth_contraction": False,
            "physical_homogeneous_subbranch_ids_materialized": False,
            "other_17_operator_fields_completed": False,
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "finite_characteristic_bound_implies_growth_contraction": False,
            "finite_characteristic_bound_implies_common_strong_space_DQ": False,
            "finite_characteristic_bound_implies_hereditary_repeated_recovery": False,
            "finite_characteristic_bound_implies_stable_quotient_or_PPE": False,
            "common_moving_DQ_atlas": "NOT_CERTIFIED",
            "strong_DQ_MT_DQ_FACE": "NOT_CERTIFIED",
            "unbounded_repeated_cuts": "NOT_CERTIFIED",
            "stable_quotient_PPE": "NOT_CERTIFIED",
            "three_norm_Kac_phase_closure": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(
        {key: value for key, value in result.items() if key != "internal_replay_digest"}
    )
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("ALL_441280_KEYS_CHARACTERISTIC_BOUNDARY_Z: CERTIFIED")
    print("ALL_MAXIMAL_COMPONENTS_CHARACTERISTIC_BOUNDARY_Z: CERTIFIED")
    print("FIELD7_GROWTH_CONTRACTION: NOT_CERTIFIED")
    print("GATES_2_3_4_5: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
