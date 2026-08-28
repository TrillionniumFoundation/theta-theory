#!/usr/bin/env python3
"""Replay and fail-closed verifier for the Gate-4/5 subrow Kac ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import cm2_gate45_immutable_subrow_kac_ledger_cert as cert


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / (
    "deliverables/cm2-gate45-immutable-subrow-kac-ledger-"
    "manifest-2026-07-15.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@lru_cache(maxsize=1)
def fresh_summary() -> dict[str, Any]:
    result = cert.certify()
    return {
        "bulk": result["certified_bulk_structural_ledger"],
        "local": {
            key: value
            for key, value in result["certified_row_ledger"].items()
            if key != "rows"
        },
        "roof": result["roof_mass_cancellation"],
        "kac": result["kac_single_charge_layer"],
        "obstruction": result["cm2_norm_recovery_obstruction"],
        "completion": result["completion"],
    }


def verify(data: dict[str, Any], *, require_physical: bool) -> None:
    assert data["schema"] == "cm2.gate45.immutable-subrow-kac-ledger.manifest.v2"
    for item in data["provenance"]:
        path = ROOT / item["path"]
        assert path.is_file(), path
        assert sha256(path) == item["sha256"], path

    fresh = fresh_summary()
    for key in ("bulk", "local", "roof", "kac", "obstruction", "completion"):
        assert data[key] == fresh[key], key

    bulk = data["bulk"]
    assert bulk["certified_physical_boxes"] == 11812
    assert bulk["certified_connected_immutable_subrow_components"] == 64
    assert bulk["Jx_Jy_component_orbits"] == 16
    assert bulk["borel_singular_kac_coordinate_count"] == 128
    assert bulk["pre_recovery_single_charge_expression_count"] == 64
    assert bulk["incorrect_per_coordinate_double_charge_count"] == 128
    assert bulk["same_occurrence_common_m_schema_instantiated_on_every_component"]
    assert bulk["bounded_borel_singular_kac_typing_on_every_component"]
    assert bulk["bulk_parameter_area_proxy_cancels"]
    assert bulk["bulk_physical_coarea_current_matching"] is False
    assert bulk["bulk_physical_mu_dot_r_cancellation_from_rows"] is False

    local = data["local"]
    assert local["certified_immutable_physical_subrows"] == 4
    assert local["Jx_pair_count"] == 2
    assert local["single_charge_count"] == 4
    assert local["row_coordinate_count"] == 8
    assert data["roof"]["mu_dot_r_on_complete_local_orbit"] == "0"
    assert data["roof"]["arbitrary_test_current_cancellation"] is False

    obstruction = data["obstruction"]
    assert obstruction["unbounded_reflection_odd_current_family"]
    assert obstruction["fat_cantor_arbitrary_borel_recovery_obstruction"]
    assert obstruction["borel_TV_typing_implies_standard_family_CM2_typing"] is False
    assert obstruction["scalar_cancellation_implies_flux_face_CM2_bound"] is False

    if require_physical:
        completion = data["completion"]
        for key in (
            "bulk_physical_coarea_current_matching",
            "bulk_physical_mu_dot_r_cancellation_from_rows",
            "all_global_physical_event_rows",
            "all_row_numeric_forward_reverse_CM2_costs",
            "global_stopped_parent_recovery",
            "global_physical_four_term_CM2_typing",
            "standard_family_CM2_norm_lift",
            "flux_face_CM2_norm_lift",
            "dynamic_test_CM2_norm_lift",
            "gate4_certified",
            "gate5_certified",
        ):
            assert completion[key] is True, key


def self_test(data: dict[str, Any]) -> None:
    verify(data, require_physical=False)

    bad = copy.deepcopy(data)
    bad["bulk"]["certified_connected_immutable_subrow_components"] = 65
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("bulk component-count tamper accepted")

    bad = copy.deepcopy(data)
    bad["bulk"]["pre_recovery_single_charge_expression_count"] = 128
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("per-coordinate double-charge tamper accepted")

    bad = copy.deepcopy(data)
    bad["roof"]["mu_dot_r_on_complete_local_orbit"] = "1"
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("roof-mass cancellation tamper accepted")

    bad = copy.deepcopy(data)
    bad["completion"]["standard_family_CM2_norm_lift"] = True
    try:
        verify(bad, require_physical=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("uncertified CM2 norm lift tamper accepted")
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
        print("GATE45_GLOBAL_PHYSICAL_CM2_COMPLETION: NOT_CERTIFIED")
        raise SystemExit(2)
    print("GATE45_GLOBAL_PHYSICAL_CM2_COMPLETION: CERTIFIED")


if __name__ == "__main__":
    main()
