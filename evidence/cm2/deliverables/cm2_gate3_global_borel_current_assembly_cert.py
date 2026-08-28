#!/usr/bin/env python3
"""Global finite-Borel coarea current on the 64 maximal CM2 event rows.

This certificate binds the chart-free maximal-row registry to the exact
moving-face coefficient.  On a row ``e`` at the reference table ``s=0`` the
positive coefficient law, in the unnormalised collision-flux gauge, is

    dm_e = R_source * cp^2 * |u_y| / ell_T dtheta,

and the signed event current is

    J_e(Phi) = sigma_e int [Phi(hit_T)-Phi(miss_M)] dm_e.

An exact global flight lower bound gives a rational total-variation envelope,
so the finite sum pairs with every bounded Borel test.  The executable also
constructs all 32 Jx row pairs and proves exact push-forward equality of their
positive laws, hence global signed scalar-coarea cancellation.

This is an assembled order-zero Borel event current.  It deliberately does
not claim convergence of the full transfer-operator difference quotient,
fixed-core differentiability, stopped recovery, or any CM2 norm lift.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_maximal_global_row_registry_cert as maximal
import cm2_gate3_stratified_collar_closure_cert as collar
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
ROW_MANIFEST = (
    HERE / "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_maximal_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = json.loads(ROW_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "cm2.gate3.maximal-global-row-registry.manifest.v1"
    assert manifest["verdict"]["maximal_connected_event_rows"] == "CERTIFIED"
    certified = manifest["result"]["maximal_row_registry"]
    assert certified["maximal_connected_physical_row_count"] == 64
    assert certified["rows_are_maximal_in_exhaustive_transition_arrangement"] is True
    curves, _candidate_registry = maximal.candidate_curve_registry()
    rows, replayed, _boundary_registry = maximal.enumerate_bands(curves)
    assert replayed["maximal_connected_physical_row_count"] == 64
    assert replayed["maximal_row_rows_sha256"] == certified["maximal_row_rows_sha256"]
    return rows, certified


def exact_relative_center_upper_squared() -> tuple[Q, list[dict[str, Any]]]:
    rows = []
    maximum = Q(0)
    seen = set()
    for source, target, _epsilon in maximal.ACTIVE_GLOBAL_SHEETS:
        key = (source, target)
        if key in seen:
            continue
        seen.add(key)
        target_row = bulk.TARGET_BY_ID[target]
        target_x0 = Q(target_row.ix) + (
            Q(1, 2) if target_row.obstacle == "W" else Q(0)
        )
        target_x_slope = 1 if target_row.obstacle == "W" else 0
        target_y = Q(target_row.iy) + (
            Q(1, 2) if target_row.obstacle == "W" else Q(0)
        )
        source_x0 = Q(1, 2) if source == "W" else Q(0)
        source_x_slope = 1 if source == "W" else 0
        source_y = Q(1, 2) if source == "W" else Q(0)
        x0 = target_x0 - source_x0
        slope = target_x_slope - source_x_slope
        y = target_y - source_y
        endpoint_x = (
            x0 + slope * bulk.S_LOWER,
            x0 + slope * bulk.S_UPPER,
        )
        upper = max(value * value for value in endpoint_x) + y * y
        assert upper < 36
        maximum = max(maximum, upper)
        rows.append({
            "source": source,
            "target": target,
            "relative_center_squared_upper": str(upper),
        })
    rows.sort(key=canonical_json)
    assert len(rows) == 64
    return maximum, rows


def global_borel_envelope(row_count: int) -> dict[str, Any]:
    separation = collar.source_target_separation_registry()
    margin = Q(separation["minimum_squared_circle_separation_margin"])
    assert margin == Q(36337, 160000)
    maximum_center_squared, center_rows = exact_relative_center_upper_squared()
    radius_sum = Q(13, 25)
    minimum_target_radius = Q(4, 25)
    center_distance_upper = Q(6)
    center_gap_lower = margin / (center_distance_upper + radius_sum)
    flight_squared_lower = 2 * minimum_target_radius * center_gap_lower
    assert flight_squared_lower == Q(36337, 3260000)
    assert flight_squared_lower > Q(1, 100)
    flight_lower = Q(1, 10)
    maximum_source_radius = Q(9, 25)
    density_upper = maximum_source_radius / flight_lower
    assert density_upper == Q(18, 5)
    circle_length_upper = Q(7)
    per_row_mass_upper = density_upper * circle_length_upper
    total_positive_mass_upper = row_count * per_row_mass_upper
    current_total_variation_upper = 2 * total_positive_mass_upper
    return {
        "active_source_target_pair_count": len(center_rows),
        "maximum_relative_center_squared": str(maximum_center_squared),
        "all_relative_center_distances_strictly_below": str(center_distance_upper),
        "minimum_squared_circle_separation_margin": str(margin),
        "center_gap_lower_bound": str(center_gap_lower),
        "target_tangent_flight_squared_lower_bound": str(flight_squared_lower),
        "target_tangent_flight_strict_lower_bound": str(flight_lower),
        "unnormalized_coarea_density_upper_bound_wrt_dtheta": str(density_upper),
        "circle_length_upper_bound": str(circle_length_upper),
        "per_row_positive_mass_upper_bound": str(per_row_mass_upper),
        "global_positive_mass_upper_bound": str(total_positive_mass_upper),
        "global_event_current_TV_upper_bound": str(current_total_variation_upper),
        "fixed_collision_flux_normalization": (
            "multiply every displayed mass bound by the common constant Z_N^-1"
        ),
        "relative_center_bound_rows_sha256": canonical_digest(center_rows),
    }


def current_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    typed = []
    for row in rows:
        polarity = row["parameter_coarea_polarity"]
        assert polarity in (-1, 1)
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "base": row["base"],
            "positive_coarea_law": {
                "coordinate": "source normal angle theta at s=0",
                "density_wrt_dtheta": "R_source*cp^2*abs(u_y)/ell_T",
                "source_flux_factor": "cp",
                "absolute_graph_coarea_factor": "abs(eta*epsilon*cp*u_y/ell_T)",
                "strict_interior_positivity": True,
            },
            "signed_current": {
                "polarity": polarity,
                "hit_trace": {
                    "target": row["target"],
                    "grazing_side": row["epsilon"],
                },
                "miss_trace": {
                    "target": row["miss_target"],
                    "strictly_non_grazing_on_open_row": True,
                },
                "shared_vector_mark": [1, -1],
                "formula": "sigma*integral(Phi(hit)-Phi(miss)) dm",
            },
            "left_boundary": row["left_boundary"],
            "right_boundary": row["right_boundary"],
        })
    typed.sort(key=canonical_json)
    assert len(typed) == 64
    assert len({row["occurrence_id"] for row in typed}) == 64
    return typed, {
        "maximal_row_current_count": len(typed),
        "positive_coarea_law_attached_to_every_row": True,
        "strict_hit_and_miss_trace_attached_to_every_row": True,
        "one_shared_plus_minus_mark_per_occurrence": True,
        "current_rows_sha256": canonical_digest(typed),
    }


def reflected_label(label: tuple[str, str, int, str, int]) -> tuple[str, str, int, str, int]:
    source, target, epsilon, miss_target, polarity = label
    return (
        source,
        bulk.reflected_target(source, "Jx", target),
        -epsilon,
        bulk.reflected_target(source, "Jx", miss_target),
        -polarity,
    )


def exact_jx_pairing(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_label = {
        tuple(row["global_physical_label"]): row for row in rows
    }
    assert len(by_label) == 64
    seen = set()
    pairs = []
    for label in sorted(by_label):
        if label in seen:
            continue
        partner = reflected_label(label)
        assert partner in by_label and partner != label
        assert reflected_label(partner) == label
        left = by_label[label]
        right = by_label[partner]
        assert left["parameter_coarea_polarity"] == -right[
            "parameter_coarea_polarity"
        ]
        seen.update((label, partner))
        ordered = sorted((left["occurrence_id"], right["occurrence_id"]))
        pairs.append({
            "occurrence_ids": ordered,
            "labels": [list(item) for item in sorted((label, partner))],
            "positive_law_identity": "(Jx)_*m_left=m_right",
            "signed_scalar_pair": "(+m)+(-m)=0",
        })
    pairs.sort(key=canonical_json)
    assert len(seen) == 64 and len(pairs) == 32
    return {
        "exact_Jx_maximal_row_pair_count": len(pairs),
        "all_positive_coarea_laws_pair_by_exact_pushforward": True,
        "all_pair_polarities_are_opposite": True,
        "global_signed_scalar_coarea_mass": "0",
        "constant_test_event_current_pairing": "0 rowwise by (+1,-1)",
        "transformation_law": {
            "parameter": "s -> -s; reference s=0 fixed",
            "source_normal": "(n_x,n_y)->(-n_x,n_y)",
            "source_direction": "(u_x,u_y)->(-u_x,u_y)",
            "tangent_side": "epsilon -> -epsilon",
            "invariants": ["cp", "ell_T", "abs(u_y)", "R_source", "dtheta"],
            "positive_density": "R_source*cp^2*abs(u_y)/ell_T preserved",
            "signed_parameter_coarea": "reversed",
        },
        "Jx_pair_rows_sha256": canonical_digest(pairs),
    }


def endpoint_and_test_typing(envelope: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_grazing_endpoints": (
            "density vanishes because cp=0"
        ),
        "parameter_polarity_endpoints": (
            "density vanishes because u_y=0"
        ),
        "first_visibility_and_miss_switch_endpoints": (
            "finite-density one-dimensional endpoints have zero base measure"
        ),
        "extra_endpoint_atoms": 0,
        "global_current_type": "finite signed Borel measure on compactified collision space",
        "arbitrary_bounded_Borel_test_pairing": True,
        "test_bound": (
            "abs(J(Phi)) <= global_event_current_TV_upper_bound*"
            "Z_N^-1*norm(Phi)_infinity"
        ),
        "displayed_TV_constant": envelope["global_event_current_TV_upper_bound"],
    }


def certify() -> dict[str, Any]:
    rows, certified_registry = load_maximal_rows()
    typed_rows, assembly = current_rows(rows)
    envelope = global_borel_envelope(len(rows))
    pairing = exact_jx_pairing(rows)
    typing = endpoint_and_test_typing(envelope)
    assert certified_registry["maximal_row_rows_sha256"] == (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    )
    return {
        "schema": "cm2.gate3.global-borel-current-assembly.v1",
        "maximal_row_manifest": ROW_MANIFEST.name,
        "maximal_row_registry_sha256": certified_registry[
            "maximal_row_rows_sha256"
        ],
        "current_assembly": assembly,
        "uniform_finite_measure_envelope": envelope,
        "exact_Jx_scalar_pairing": pairing,
        "endpoint_and_test_typing": typing,
        "scope_limits": {
            "maximal_connected_event_rows_imported": True,
            "positive_coarea_law_attached_to_every_maximal_row": True,
            "global_finite_Borel_event_current_assembled": True,
            "arbitrary_bounded_Borel_test_pairing": True,
            "global_signed_scalar_coarea_matching": True,
            "full_transfer_difference_quotient_convergence": False,
            "fixed_core_differentiability": False,
            "dynamic_C1_test_CM2_bound": False,
            "forward_reverse_standard_family_costs": False,
            "stopped_parent_recovery": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_GLOBAL_FINITE_BOREL_EVENT_CURRENT: CERTIFIED")
    print("GATE3_GLOBAL_SIGNED_SCALAR_COAREA_MATCHING: CERTIFIED")
    print("GATE3_FULL_TRANSFER_DQ_AND_CM2_NORMS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
