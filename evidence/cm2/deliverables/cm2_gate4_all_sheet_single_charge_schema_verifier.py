#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-4 all-sheet schema manifest."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate4_all_sheet_single_charge_schema_cert as cert


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "deliverables/cm2-gate4-all-sheet-single-charge-schema-manifest-2026-07-15.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(data: dict[str, Any], *, require_global: bool) -> None:
    for item in data["provenance"]:
        path = ROOT / item["path"]
        assert path.is_file(), path
        assert sha256(path) == item["sha256"], path

    fresh = cert.certify()
    ledger = data["exact_raw_ledger"]
    assert ledger["global_raw_signed_sheets_after_chart_merge"] == fresh[
        "global_raw_signed_sheets_after_chart_merge"
    ]
    assert ledger["global_parameter_active_signed_sheets"] == fresh[
        "global_parameter_active_signed_sheets"
    ]
    assert ledger["global_identically_zero_parameter_sheets"] == fresh[
        "global_identically_zero_parameter_sheets"
    ]
    assert ledger["chart_parameter_active_signed_sheets_before_merge"] == sum(
        row["moving_signed_sheets"] for row in fresh["chart_ledger"].values()
    )
    assert ledger["raw_sheet_schema_sha256"] == fresh["raw_sheet_schema_sha256"]
    assert ledger["active_sheet_schema_sha256"] == fresh["active_sheet_schema_sha256"]

    endpoints = fresh["active_endpoint_registry"]
    frozen_endpoints = ledger["active_endpoint_descriptors"]
    assert frozen_endpoints == {
        "target_target_common_tangent": endpoints[
            "target_target_common_tangent_descriptors"
        ],
        "source_grazing": endpoints["source_grazing_descriptors"],
        "parameter_boundary": endpoints["parameter_boundary_descriptors"],
        "constant_polarity_split": endpoints["constant_polarity_split_equations"],
        "total": endpoints["total_raw_active_endpoint_descriptors"],
    }

    symmetry = data["symmetry"]
    fresh_symmetry = fresh["symmetry"]
    assert symmetry["active_sheet_orbits"] == fresh_symmetry[
        "active_sheet_orbit_count"
    ]
    assert symmetry["orbit_size"] == fresh_symmetry["orbit_size"]
    assert symmetry["two_plus_two_minus_per_orbit"] == fresh_symmetry[
        "two_plus_two_minus_per_orbit"
    ]
    assert symmetry["orbits_sha256"] == fresh_symmetry["orbits_sha256"]

    contract = data["universal_physical_row_contract"]
    fresh_contract = fresh["universal_occurrence_contract"]
    assert contract["restrictionwise_two_view_current"]
    assert contract["common_absolute_coarea"]
    assert contract["endpoint_views_nonadditive"] == fresh_contract[
        "endpoint_views_are_nonadditive"
    ]
    assert contract["pre_recovery_single_charge"] == fresh_contract[
        "pre_recovery_single_charge"
    ]
    assert contract["charged_occurrence_count"] == fresh_contract[
        "charged_occurrence_count"
    ]
    assert contract["raw_descriptor_receives_charge"] == fresh_contract[
        "raw_descriptor_receives_q_charge"
    ]
    assert contract["distinct_physical_rows_remain_additive"] == fresh_contract[
        "distinct_physical_rows_remain_additive"
    ]

    recovery = data["recovery_boundary"]
    fresh_recovery = fresh["recovery_boundary"]
    assert recovery["borel_change_of_variables_for_two_views"] == fresh_recovery[
        "borel_change_of_variables_for_two_views"
    ]
    assert recovery["arbitrary_borel_stopped_recovery"] == fresh_recovery[
        "arbitrary_borel_stopped_recovery"
    ]
    assert recovery["fat_cantor_obstruction"]
    assert recovery["pilot_two_map_energy_is_physical_full_mass_ppe"] is False

    assert data["completion"] == fresh["completion"]
    if require_global:
        completion = data["completion"]
        for key in (
            "connected_immutable_physical_event_rows",
            "all_row_forward_reverse_typing_and_costs",
            "controlled_stopped_restriction_algebra",
            "physical_bidirectional_recovery_moments",
            "global_single_charge_q_ledger",
            "gate4_certified",
        ):
            assert completion[key] is True


def self_test(data: dict[str, Any]) -> None:
    verify(data, require_global=False)
    bad = copy.deepcopy(data)
    bad["exact_raw_ledger"]["global_parameter_active_signed_sheets"] = 127
    try:
        verify(bad, require_global=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("active-sheet-count tamper was accepted")

    bad = copy.deepcopy(data)
    bad["universal_physical_row_contract"]["charged_occurrence_count"] = 2
    try:
        verify(bad, require_global=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("double-charge tamper was accepted")
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
        verify(data, require_global=True)
    except AssertionError:
        verify(data, require_global=False)
        print("GATE4_GLOBAL_SINGLE_CHARGE_COMPLETION: NOT_CERTIFIED")
        raise SystemExit(2)
    print("GATE4_GLOBAL_SINGLE_CHARGE_COMPLETION: CERTIFIED")


if __name__ == "__main__":
    main()
