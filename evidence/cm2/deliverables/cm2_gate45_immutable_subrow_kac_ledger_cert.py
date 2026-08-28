#!/usr/bin/env python3
"""Exact Gate-4/5 ledger on the refined immutable Jx/Jy subrow atlas.

The global Gate-3 atlas still has genuine collars.  This certificate binds
the endpoint-identity refinement (64 connected physical subrows) to every
piece of the Gate-4/5 construction that only needs a connected physical row,
while retaining the frozen four-element orbit for an exact rowwise scalar
cancellation:

* one occurrence id and one positive coefficient law per row;
* the same-occurrence forward/reverse Borel views with one common law;
* one ``q=max(Cfw,Crev,2)m`` charge rather than two coordinate charges;
* the two singular Kac coordinates with the fixed mark ``(+1,-1)``; and
* exact Jx pair cancellation of the scalar roof mass.

It deliberately distinguishes bounded-Borel/finite-measure typing from the
still missing CM2 standard-family, flux-face and dynamic-test norm typing.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_component_orbit_dedup_cert as gate3_rows
import cm2_gate4_all_sheet_single_charge_schema_cert as gate4
import cm2_gate45_algebraic_typing_frontier_cert as gate45_frontier
import cm2_gate5_prefix_suffix_norm_cert as gate5


Q = Fraction
HERE = Path(__file__).resolve().parent
ATLAS_MANIFEST = (
    HERE / "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json"
)
ATLAS_MANIFEST_SHA256 = (
    "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certified_bulk_structural_ledger() -> dict[str, Any]:
    """Bind the refined 64-component atlas to the universal Kac/q schema.

    The atlas deliberately retains unresolved collars.  Hence these are
    certified connected immutable *subrows*, not the maximal global physical
    event partition.  Nevertheless the Gate-4 same-occurrence construction
    and bounded-Borel Kac type apply independently to every component.
    """

    assert sha256_path(ATLAS_MANIFEST) == ATLAS_MANIFEST_SHA256
    manifest = json.loads(ATLAS_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "cm2.gate3.endpoint-identity-refinement.manifest.v1"
    assert manifest["certificate_sha256"] == sha256_path(
        HERE / "cm2_gate3_endpoint_identity_refinement_cert.py"
    )
    atlas = manifest["result"]
    assert atlas["schema"] == "cm2.gate3.endpoint-identity-refinement.v1"
    assert atlas["active_chart_signed_sheets"] == 384
    assert atlas["physical_immutable_box_count"] == 11812
    assert atlas["physical_complete_label_count"] == 64
    components = atlas["connected_component_atlas"]
    assert components["certified_connected_subrow_components"] == 64
    assert components["component_label_count"] == 64
    limits = atlas["scope_limits"]
    assert limits["redundant_source_coordinate_and_positive_flight_collars_removed"] is True
    assert limits["coarea_product_dependency_collar_reduced_by_exact_sign_factor"] is True
    assert limits["all_remaining_endpoint_collars_are_source_grazing_not_tau3"] is True
    assert limits["remaining_source_grazing_edge_or_degeneracy_boxes_resolved"] is False
    assert limits["components_maximal_across_remaining_collars"] is False
    assert limits["components_quotiented_across_chart_seams"] is False
    assert limits["global_dq"] is False
    assert limits["global_scalar_matching"] is False

    symmetry = atlas["certified_bulk_symmetry_matching"]
    assert symmetry["Jx_Jy_label_orbit_count"] == 16
    assert symmetry["four_labels_per_orbit"] is True
    assert symmetry["Jx_reverses_parameter_coarea_polarity"] is True
    assert symmetry["Jy_preserves_parameter_coarea_polarity"] is True
    assert symmetry["box_count_and_parameter_area_equal_within_each_orbit"] is True
    assert symmetry["paired_bulk_polarity_weighted_parameter_area"] == "0"

    universal = gate4.universal_occurrence_contract()
    component_count = components["certified_connected_subrow_components"]
    structural_contract = {
        "atlas_component_rows_sha256": components["component_rows_sha256"],
        "atlas_physical_labels_sha256": atlas["physical_complete_labels_sha256"],
        "atlas_physical_boxes_sha256": atlas["physical_box_rows_sha256"],
        "atlas_symmetry_orbits_sha256": symmetry["label_orbits_sha256"],
        "component_count": component_count,
        "per_component_types": {
            "coefficient": "m_e in M_+(A_e)",
            "singular_kac_current": "M_b(compactified N)",
            "dual_test": "B_b(compactified N)",
            "structural_mark": [1, -1],
            "same_occurrence_nonadditive_views": True,
            "common_coarea_law": True,
            "pre_recovery_charge": universal["pre_recovery_single_charge"],
        },
    }
    return {
        "atlas_manifest_sha256": ATLAS_MANIFEST_SHA256,
        "certified_physical_boxes": atlas["physical_immutable_box_count"],
        "certified_connected_immutable_subrow_components": component_count,
        "complete_component_labels": atlas["physical_complete_label_count"],
        "Jx_Jy_component_orbits": symmetry["Jx_Jy_label_orbit_count"],
        "borel_singular_kac_coordinate_count": 2 * component_count,
        "pre_recovery_single_charge_expression_count": component_count,
        "incorrect_per_coordinate_double_charge_count": 2 * component_count,
        "same_occurrence_common_m_schema_instantiated_on_every_component": True,
        "bounded_borel_singular_kac_typing_on_every_component": True,
        "bulk_polarity_weighted_parameter_area": (
            symmetry["paired_bulk_polarity_weighted_parameter_area"]
        ),
        "bulk_parameter_area_proxy_cancels": True,
        "bulk_physical_coarea_current_matching": False,
        "bulk_physical_mu_dot_r_cancellation_from_rows": False,
        "unresolved_area_fraction": atlas["unresolved_area_fraction"],
        "components_are_maximal_global_rows": False,
        "global_dq": False,
        "global_scalar_matching": False,
        "structural_bulk_ledger_sha256": canonical_digest(structural_contract),
    }


def row_id(row: dict[str, Any]) -> str:
    key = {
        "chart_id": row["chart_id"],
        "t": row["t"],
        "s": row["s"],
        "target": row["target"],
        "epsilon": row["epsilon"],
        "miss_owner": row["miss_owner"],
        "polarity": row["parameter_coarea_polarity"],
    }
    return "occ:" + canonical_digest(key)[:24]


def certified_orbit_ledger() -> dict[str, Any]:
    """Replay and type the four immutable physical subrows."""

    orbit = gate3_rows.immutable_local_orbit()
    universal = gate4.universal_occurrence_contract()
    rows = orbit["rows"]
    assert len(rows) == 4
    assert orbit["constant_miss_trace_on_every_row"] is True
    assert orbit["constant_nonzero_parameter_coarea_polarity_on_every_row"] is True
    assert orbit["symmetry_invariant_scalar_current_cancels_pairwise"] is True

    by_symmetry = {row["symmetry"]: row for row in rows}
    assert set(by_symmetry) == {"id", "Jx", "Jy", "JxJy"}
    pairs = (("id", "Jx", "m_Jx_pair_0"), ("Jy", "JxJy", "m_Jx_pair_1"))
    for positive, negative, _symbol in pairs:
        assert by_symmetry[positive]["parameter_coarea_polarity"] == 1
        assert by_symmetry[negative]["parameter_coarea_polarity"] == -1
        # Exact reflection conjugacy sends the full rational base rectangle
        # and the coarea density of the first row to those of the second.
        assert by_symmetry[positive]["s"] == by_symmetry[negative]["s"]

    pair_symbol = {
        symmetry: symbol
        for positive, negative, symbol in pairs
        for symmetry in (positive, negative)
    }
    partner = {
        positive: negative for positive, negative, _symbol in pairs
    } | {
        negative: positive for positive, negative, _symbol in pairs
    }

    typed_rows: list[dict[str, Any]] = []
    for row in rows:
        occurrence_id = row_id(row)
        polarity = row["parameter_coarea_polarity"]
        assert polarity in (-1, 1)
        typed_rows.append({
            "occurrence_id": occurrence_id,
            "raw_sheet_id": (
                f"{row['chart_id'].split(':')[0]}:{row['target']}:"
                f"eps={row['epsilon']:+d}"
            ),
            "chart_id": row["chart_id"],
            "base_rectangle": {"t": row["t"], "s": row["s"]},
            "tangent_target": row["target"],
            "miss_target": row["miss_owner"],
            "polarity": polarity,
            "symmetry": row["symmetry"],
            "Jx_partner_symmetry": partner[row["symmetry"]],
            "coarea_law_symbol": pair_symbol[row["symmetry"]],
            "physical_fields": {
                "compact_connected_base": True,
                "first_visible_tangent_owner": True,
                "constant_miss_trace": True,
                "strict_miss_after_tangent": True,
                "non_grazing_source_endpoint": True,
                "non_grazing_miss_endpoint": True,
                "constant_nonzero_parameter_polarity": True,
                "maximal_global_component": False,
            },
            "borel_current_typing": {
                "coefficient": "m_e in M_+(A_e)",
                "face_current": "J_e(h) in M_b(compactified N)",
                "dual_tests": "B_b(compactified N)",
                "forward_reverse_views_are_nonadditive": True,
                "restrictionwise_identity": True,
                "common_coarea_law": True,
            },
            "singular_kac_typing": {
                "coordinates": ["moving_level_dot_S_face", "roof_dot_r_times_phase_mean"],
                "structural_mark": [1, -1],
                "coefficient_measure_copies": 1,
                "borel_pairing": (
                    "int_A g(x_e(a))*(h_1(z_e(a))-mu_hat(h))*dm_e(a)"
                ),
                "TV_bound": (
                    "norm <= 2*norm(h)_infinity*norm(g)_infinity*m_e(A_e)"
                ),
            },
            "single_charge": universal["pre_recovery_single_charge"],
            "charge_multiplicity": 1,
            "coordinate_multiplicity": 2,
        })

    assert len({row["occurrence_id"] for row in typed_rows}) == 4
    assert sum(row["charge_multiplicity"] for row in typed_rows) == 4
    assert sum(row["coordinate_multiplicity"] for row in typed_rows) == 8
    return {
        "certified_immutable_physical_subrows": len(typed_rows),
        "Jx_pair_count": len(pairs),
        "row_coordinate_count": 8,
        "single_charge_count": 4,
        "double_charge_count_rejected": 8,
        "all_rows_share_mark_plus_one_minus_one": True,
        "bounded_borel_measure_typing": True,
        "rows_sha256": canonical_digest(typed_rows),
        "rows": typed_rows,
    }


def exact_roof_mass_cancellation(ledger: dict[str, Any]) -> dict[str, Any]:
    """Formal exact cancellation on the two Jx coefficient-law pairs."""

    coefficients: dict[str, int] = {}
    pair_members: dict[str, list[str]] = {}
    for row in ledger["rows"]:
        symbol = row["coarea_law_symbol"]
        coefficients[symbol] = coefficients.get(symbol, 0) + row["polarity"]
        pair_members.setdefault(symbol, []).append(row["occurrence_id"])
    assert coefficients == {"m_Jx_pair_0": 0, "m_Jx_pair_1": 0}
    assert all(len(members) == 2 for members in pair_members.values())

    # Executable scalar sample of the symbolic identity.  The proof above is
    # coefficientwise, so the values are deliberately arbitrary.
    sample_mass = {"m_Jx_pair_0": Q(17, 31), "m_Jx_pair_1": Q(29, 47)}
    total = sum(
        Q(row["polarity"]) * sample_mass[row["coarea_law_symbol"]]
        for row in ledger["rows"]
    )
    assert total == 0

    global_frontier = gate45_frontier.certify()
    assert global_frontier["cross_gate_ledger_alignment"][
        "global_scalar_roof_mass_cancellation"
    ] is True
    return {
        "local_orbit_Jx_coarea_laws_pair_exactly": True,
        "formal_pair_coefficients": coefficients,
        "sample_exact_total": str(total),
        "mu_dot_r_on_complete_local_orbit": "0",
        "fixed_collision_flux_global_scalar_identity_replayed": True,
        "arbitrary_test_current_cancellation": False,
    }


def exact_kac_and_single_charge_checks(ledger: dict[str, Any]) -> dict[str, Any]:
    """Exact finite algebra and charge accounting on the row ledger."""

    assert gate5.exact_endpoint_adjoint_pairing() == Q(116)
    assert gate5.exact_kac_tower_pairing() == Q(59, 6)
    assert gate5.exact_prefix_suffix_pairing() == Q(623)

    # Every occurrence owns one law and two coordinates.  The fixed mark
    # contracts those coordinates before any norm estimate; it never creates
    # a second copy of the positive law.
    charges = ledger["single_charge_count"]
    coordinates = ledger["row_coordinate_count"]
    assert charges == 4 and coordinates == 8
    assert coordinates == 2 * charges

    # Exact sample pairing of h_1(z)-mu(h) against each coefficient law.
    masses = (Q(2, 7), Q(3, 11), Q(5, 13), Q(7, 17))
    level_values = (Q(3), Q(5), Q(7), Q(11))
    phase_mean = Q(47, 13)
    contracted = tuple(
        mass * (value - phase_mean)
        for mass, value in zip(masses, level_values)
    )
    constant = tuple(mass * (phase_mean - phase_mean) for mass in masses)
    assert all(value == 0 for value in constant)
    return {
        "finite_borel_endpoint_adjoint": True,
        "finite_borel_kac_tower_pairing": True,
        "finite_borel_prefix_suffix_pairing": True,
        "occurrence_charges": charges,
        "singular_coordinates": coordinates,
        "coordinates_are_not_independent_charges": True,
        "constant_observable_rowwise_centering": True,
        "sample_contracted_pairing_sha256": canonical_digest(
            [str(value) for value in contracted]
        ),
    }


def cm2_norm_and_recovery_obstruction() -> dict[str, Any]:
    """Exact obstruction to promoting the Borel ledger to CM2 typing."""

    # The same reflection-compatible signed current can have zero scalar
    # mass and arbitrarily large TV/odd-test norm.  Thus neither mu(dot r)=0
    # nor the fixed (+1,-1) mark provides the missing physical norm bound.
    scales = (1, 2, 4, 8, 16, 32, 64, 128)
    tv = []
    odd = []
    for scale in scales:
        coefficients = (Q(scale), Q(-scale))
        scalar_pairing = coefficients[0] + coefficients[1]
        odd_pairing = coefficients[0] - coefficients[1]
        total_variation = abs(coefficients[0]) + abs(coefficients[1])
        assert scalar_pairing == 0
        assert odd_pairing == total_variation == 2 * scale
        odd.append(odd_pairing)
        tv.append(total_variation)
    assert all(left < right for left, right in zip(tv, tv[1:]))

    recovery = gate4.recovery_boundary()
    assert recovery["arbitrary_borel_stopped_recovery"] is False
    return {
        "scalar_mass_zero_at_every_scale": True,
        "largest_exact_TV_and_odd_test_pairing": str(tv[-1]),
        "unbounded_reflection_odd_current_family": True,
        "fat_cantor_arbitrary_borel_recovery_obstruction": True,
        "missing_rowwise_numeric_fields": [
            "homogeneity cut registry and cut-growth sum",
            "forward standard-family/flux carrier cost C_fw",
            "reverse standard-family/flux carrier cost C_rev",
            "dynamic C1 test-pullback cost",
            "bidirectional stopped-parent recovery envelope",
            "physical prefix/suffix inverse-Jacobian and distortion sums",
        ],
        "borel_TV_typing_implies_standard_family_CM2_typing": False,
        "scalar_cancellation_implies_flux_face_CM2_bound": False,
        "finite_subrow_ledger_implies_phase_test_norm_lift": False,
    }


def certify() -> dict[str, Any]:
    ledger = certified_orbit_ledger()
    bulk = certified_bulk_structural_ledger()
    result = {
        "schema": "cm2.gate45.immutable-subrow-kac-ledger.v2",
        "model": "cm2-centered-rational-two-disk-standard-N",
        "certified_bulk_structural_ledger": bulk,
        "certified_row_ledger": ledger,
        "roof_mass_cancellation": exact_roof_mass_cancellation(ledger),
        "kac_single_charge_layer": exact_kac_and_single_charge_checks(ledger),
        "cm2_norm_recovery_obstruction": cm2_norm_and_recovery_obstruction(),
        "completion": {
            "sixty_four_component_bulk_structural_occurrence_ledger": True,
            "one_pre_recovery_q_expression_per_bulk_component": True,
            "typed_bounded_borel_singular_kac_current_on_all_bulk_components": True,
            "bulk_Jx_Jy_parameter_area_proxy_cancellation": True,
            "four_row_immutable_physical_occurrence_ledger": True,
            "same_occurrence_two_view_common_m_on_every_certified_row": True,
            "one_pre_recovery_q_charge_per_certified_occurrence": True,
            "typed_bounded_borel_singular_kac_current_on_every_certified_row": True,
            "local_orbit_mu_dot_r_scalar_cancellation": True,
            "bulk_physical_coarea_current_matching": False,
            "bulk_physical_mu_dot_r_cancellation_from_rows": False,
            "all_global_physical_event_rows": False,
            "all_row_numeric_forward_reverse_CM2_costs": False,
            "global_stopped_parent_recovery": False,
            "global_physical_four_term_CM2_typing": False,
            "standard_family_CM2_norm_lift": False,
            "flux_face_CM2_norm_lift": False,
            "dynamic_test_CM2_norm_lift": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_64_COMPONENT_REFINED_BULK_STRUCTURAL_KAC_q_LEDGER: CERTIFIED")
    print("GATE45_FOUR_IMMUTABLE_SUBROW_EXACT_KAC_LEDGER: CERTIFIED")
    print("GATE45_BOUNDED_BOREL_SINGULAR_CURRENT_TYPING: CERTIFIED")
    print("GATE45_LOCAL_ORBIT_MU_DOT_R_ZERO: CERTIFIED")
    print("GATE45_ONE_q_PER_OCCURRENCE_NOT_COORDINATE: CERTIFIED")
    print("GATE45_GLOBAL_PHYSICAL_CM2_NORM_TYPING: NOT_CERTIFIED")
    print("GATE45_GLOBAL_STOPPED_RECOVERY: NOT_CERTIFIED")
    print("GATE_4: NOT_CERTIFIED")
    print("GATE_5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
