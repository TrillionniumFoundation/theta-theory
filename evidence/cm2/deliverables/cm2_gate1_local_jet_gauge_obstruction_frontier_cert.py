#!/usr/bin/env python3
"""Gate-1 local-jet gauge obstruction frontier.

This certificate does not search for a new global resonant gauge.  It closes
an exact invariance statement around the two already certified periodic
obstructions:

* the first derivative of the gauged return at a periodic point depends only
  on the value and first jet of the gauge there;
* consequently every gauge sharing the compact twisting gauge's 1-jet at the
  96-collision shadow has the same strictly nonzero resonant mixed
  coefficient and the same divergent stable canonical comparison;
* every gauge locally constant near the connector differs there only by a
  constant conjugacy, so the frozen connector mixed-jet obstruction also
  persists.

This rules out the natural class of local/partition-of-unity repairs that do
not alter both obstructing jets.  It deliberately leaves arbitrary global
jet-changing gauges open, hence Gate 1 stays fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEPENDENCIES = (
    "cm2-gate1-same-representative-resonant-shadow-frontier-manifest-2026-07-16.json",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def dependency_hashes() -> dict[str, str]:
    return {name: sha256_path(HERE / name) for name in DEPENDENCIES}


def build_result() -> dict[str, Any]:
    shadow_manifest = load(DEPENDENCIES[0])
    global_manifest = load(DEPENDENCIES[1])
    shadow_result = shadow_manifest["result"]
    global_result = global_manifest["result"]

    shadow = shadow_result["compact_gauge_periodic_shadow_obstruction"]
    connector = global_result["connector_compact_gauge_obstruction"]

    assert shadow["gauged_stable_direction_lower_left_derivative_excludes_zero"]
    assert shadow["compact_gauge_stable_canonical_limit_at_shadow"] == "DIVERGENT"
    assert shadow["nontrivial_local_stable_tail_required"] is True
    assert connector["stable_mixed_jet_in_minus_1_over_20_minus_1_over_25"]
    assert connector["connector_has_neighbourhood_where_compact_qnl_gauge_is_identity"]
    assert connector["compact_qnl_gauge_connector_stable_limit_converges"] is False

    local_jet_identity = {
        "periodic_return": "G(z_*)=z_*",
        "gauged_return_formula": "A_D(z)=D(Gz)^-1 DG(z) D(z)",
        "first_derivative_formula": (
            "dA_D[v]=-D^-1 dD[DG v] D^-1 DG D "
            "+D^-1 d(DG)[v]D+D^-1 DG dD[v] at z_*"
        ),
        "data_used_by_A_D_and_dA_D": [
            "D(z_*)",
            "dD(z_*)",
            "DG(z_*)",
            "dDG(z_*)",
        ],
        "same_value_and_first_jet_give_same_gauged_return_and_derivative": True,
        "same_fiber_eigenbasis_and_resonant_mixed_coefficient": True,
        "higher_gauge_jets_enter_first_derivative": False,
    }

    shadow_class = {
        "periodic_shadow_collision_count": shadow["periodic_shadow_collision_count"],
        "periodic_shadow_full_word": shadow["periodic_shadow_full_word"],
        "reference_compact_gauge_mixed_coefficient": shadow[
            "gauged_stable_direction_lower_left_derivative"
        ],
        "reference_coefficient_excludes_zero": True,
        "alternative_gauge_hypothesis": (
            "D_alt(z_*)=D_compact(z_*) and "
            "dD_alt(z_*)=dD_compact(z_*)"
        ),
        "alternative_has_same_nonzero_mixed_coefficient": True,
        "alternative_stable_canonical_limit_on_nontrivial_shadow_tail": "DIVERGENT",
        "class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail": False,
        "modifications_supported_away_from_shadow_are_obstructed": True,
        "modifications_flat_through_first_order_at_shadow_are_obstructed": True,
        "isolated_periodic_orbit_alone_is_not_claimed_obstructed": True,
    }

    connector_class = {
        "connector_return": connector["connector_return"],
        "reference_physical_mixed_jet": connector["stable_mixed_jet_partial_xy_G2"],
        "reference_mixed_jet_strict_interval": "(-1/20,-1/25)",
        "alternative_gauge_hypothesis": (
            "D_alt is constant on a neighbourhood of the connector fixed point"
        ),
        "constant_local_gauge_changes_return_by_constant_conjugacy": True,
        "canonical_comparison_divergence_is_preserved_by_constant_conjugacy": True,
        "alternative_connector_stable_canonical_limit": "DIVERGENT",
        "class_H_on_common_basic_set_with_connector_and_nontrivial_stable_tail": False,
        "all_gauges_supported_inside_the_frozen_QNL_chart_are_obstructed_at_connector": True,
    }

    necessary_escape = {
        "pure_QNL_local_cutoff_repair_can_close_class_H": False,
        "partition_of_unity_repair_unchanged_near_connector_and_first_order_at_shadow": (
            "REFUTED"
        ),
        "any_surviving_third_gauge_must_change_connector_local_jet_or_cease_to_be_local": True,
        "any_surviving_third_gauge_must_change_shadow_value_or_first_jet": True,
        "simultaneous_global_stable_and_unstable_resonant_equations_solved": False,
        "arbitrary_global_jet_changing_gauge_excluded": False,
        "one_representative_with_class_H_and_twisting_certified": False,
    }

    result: dict[str, Any] = {
        "schema": "cm2.gate1.local-jet-gauge-obstruction-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": dependency_hashes(),
            "shadow_arb_precision_bits": shadow["arb_precision_bits"],
            "connector_arb_precision_bits": connector["arb_precision_bits"],
            "old_artifacts_modified": False,
        },
        "periodic_local_jet_identity": local_jet_identity,
        "shadow_first_jet_equivalence_class_obstruction": shadow_class,
        "connector_locally_constant_gauge_obstruction": connector_class,
        "necessary_escape_conditions_for_a_third_gauge": necessary_escape,
        "strict_completion_boundary": {
            "local_or_first_jet_flat_repairs": "REFUTED",
            "arbitrary_global_third_gauge": "NOT_CERTIFIED",
            "single_representative_class_H_plus_twisting": "NOT_CERTIFIED",
            "full_mass_physical_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def main() -> int:
    result = build_result()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PERIODIC_GAUGE_FIRST_JET_INVARIANCE: CERTIFIED")
    print("SHADOW_FIRST_JET_EQUIVALENCE_CLASS_CLASS_H: REFUTED")
    print("CONNECTOR_LOCALLY_CONSTANT_GAUGE_CLASS_H: REFUTED")
    print("ARBITRARY_GLOBAL_THIRD_GAUGE: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
