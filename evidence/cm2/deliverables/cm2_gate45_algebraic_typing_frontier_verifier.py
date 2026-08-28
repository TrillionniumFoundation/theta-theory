#!/usr/bin/env python3
"""Replay and fail-closed verifier for the Gate-4/5 algebraic frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate45_algebraic_typing_frontier_cert as cert


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "deliverables/cm2-gate45-algebraic-typing-frontier-2026-07-15.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify(data: dict[str, Any], *, require_physical: bool) -> None:
    assert data["schema"] == "cm2.gate45.algebraic-typing-frontier.v1"
    for item in data["provenance"]:
        path = ROOT / item["path"]
        assert path.is_file(), path
        assert sha256(path) == item["sha256"], path

    fresh = cert.certify()
    alignment = data["cross_gate_ledger_alignment"]
    fresh_alignment = fresh["cross_gate_ledger_alignment"]
    for key in (
        "gate3_gate4_raw_sheet_universes_identical",
        "global_signed_sheets",
        "parameter_active_signed_sheets",
        "parameter_inactive_signed_sheets",
        "all_sheet_symmetry_orbits",
        "active_sheet_symmetry_orbits",
        "active_target_target_endpoint_descriptors",
        "active_source_grazing_descriptors",
        "active_parameter_boundary_descriptors",
        "active_polarity_split_equations",
        "gate3_sheet_universe_sha256",
        "gate4_sheet_universe_sha256",
        "global_candidate_row_count",
        "global_scalar_roof_mass_cancellation",
        "corrected_forward_time_endpoint_audit",
        "component_local_physical_baseline",
    ):
        assert alignment[key] == fresh_alignment[key]

    algebra = data["global_algebraic_kac_layer"]
    fresh_algebra = fresh["global_algebraic_kac_layer"]
    for key in (
        "fixed_flux_mean_roof",
        "fixed_flux_mean_dot_roof",
        "phase_mean",
        "phase_mean_derivative",
        "four_term_centered_base_mean",
        "four_term_identity_exact",
        "finite_borel_endpoint_adjoint_exact",
        "finite_borel_kac_tower_pairing_exact",
        "finite_borel_prefix_suffix_pairing_exact",
        "singular_occurrence_structural_mark",
        "singular_coordinates_share_one_measure",
        "charged_occurrences",
        "coordinate_count",
        "charges_are_per_occurrence_not_per_coordinate",
        "constant_observable_rowwise_singular_centering",
        "sample_combined_occurrence_digest",
    ):
        assert algebra[key] == fresh_algebra[key]

    obstruction = data["exact_no_promotion_obstruction"]
    fresh_obstruction = fresh["exact_no_promotion_obstruction"]
    assert obstruction == fresh_obstruction
    assert obstruction["reflection_scalar_test_one_cancels_at_every_scale"]
    assert obstruction["unbounded_scale_family"]
    assert obstruction["abstract_height_two_countermodel_cycle_gcd"] == 2
    assert obstruction["actual_pilot_height_two_component_cycle_gcd"] == 1
    assert obstruction["actual_pilot_standard_N_component_cycle_gcd"] == 1
    assert obstruction["height_bound_alone_implies_aperiodicity"] is False
    assert obstruction[
        "actual_component_gcd_one_implies_operator_Dz_invertibility"
    ] is False

    assert data["completion"] == fresh["completion"]
    if require_physical:
        completion = data["completion"]
        for key in (
            "immutable_physical_event_rows",
            "all_row_physical_banach_typing",
            "global_stopped_parent_recovery",
            "global_single_charge_q_ledger",
            "physical_four_term_kac_typing",
            "phase_cm2_norm_lifts",
            "gate4_certified",
            "gate5_certified",
        ):
            assert completion[key] is True


def self_test(data: dict[str, Any]) -> None:
    verify(data, require_physical=False)

    bad = copy.deepcopy(data)
    bad["cross_gate_ledger_alignment"]["parameter_active_signed_sheets"] = 127
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("active-sheet tamper was accepted")

    bad = copy.deepcopy(data)
    bad["global_algebraic_kac_layer"]["charged_occurrences"] *= 2
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("double-charge tamper was accepted")

    bad = copy.deepcopy(data)
    bad["cross_gate_ledger_alignment"][
        "corrected_forward_time_endpoint_audit"
    ]["corrected_physical_transition_vertices"] = 16
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("retracted physical vertices were accepted")

    bad = copy.deepcopy(data)
    bad["exact_no_promotion_obstruction"]["unbounded_scale_family"] = False
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("norm-promotion tamper was accepted")
    print("MANIFEST_VERIFIER_SELF_TEST: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.self_test:
        self_test(data)
        return
    try:
        verify(data, require_physical=True)
    except AssertionError:
        verify(data, require_physical=False)
        print("GATE45_PHYSICAL_BANACH_COMPLETION: NOT_CERTIFIED")
        raise SystemExit(2)
    print("GATE45_PHYSICAL_BANACH_COMPLETION: CERTIFIED")


if __name__ == "__main__":
    main()
