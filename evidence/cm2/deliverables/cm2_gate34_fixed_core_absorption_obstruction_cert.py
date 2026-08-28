#!/usr/bin/env python3
"""Exact obstruction to treating the frozen 24-core union as a global trap."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate5_actual_phase_graph_cert as phase_cert


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json": (
        "ab914a9274b9365defaed5d8808b7a33bacefcce2fc56342881350665c811642"
    ),
    "cm2_gate5_actual_phase_graph_cert.py": (
        "7ec30f8a51abdb651cf1fdba0dfba755c356272f9058149b974a3149fe2f1a0c"
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
    parameter = json.loads(
        (
            HERE
            / "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    cores = json.loads(
        (
            HERE
            / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
        ).read_text(encoding="utf-8")
    )
    phase = json.loads(
        (
            HERE
            / "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"
        ).read_text(encoding="utf-8")
    )
    assert parameter["verdict"][
        "selected_parameter_DQ_all_scale_germs_64"
    ] == "CERTIFIED"
    assert parameter["verdict"]["first_24_core_destination"] == (
        "NOT_CERTIFIED"
    )
    assert cores["verdict"]["positive_mass_physical_core_registry"] == (
        "CERTIFIED"
    )
    assert phase["physical_first_hit_witnesses"]["gray_white_gray"][
        "physical_word"
    ] == "G(0,0)->W(0,0)->G(0,0)"


def core_coordinate_envelope() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    assert len(cores) == 24
    axis = [core for core in cores if core.family == "axis_translate"]
    diagonal = [core for core in cores if core.family.startswith("diagonal_")]
    assert len(axis) == 8
    assert len(diagonal) == 16
    assert all(
        core.t0 == Q(1, 100) and core.t1 == Q(1, 50)
        for core in axis
    )
    assert all(
        Q(69, 100) <= abs(core.t0) <= Q(7, 10)
        and Q(69, 100) <= abs(core.t1) <= Q(7, 10)
        for core in diagonal
    )
    assert all(core.p0 <= 0 <= core.p1 for core in cores)
    rows = [{
        "chart_id": core.chart_id,
        "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)],
        "family": core.family,
    } for core in cores]
    return {
        "physical_core_count": len(cores),
        "axis_core_count": len(axis),
        "diagonal_core_count": len(diagonal),
        "axis_t_interval": ["1/100", "1/50"],
        "diagonal_absolute_t_interval": ["69/100", "7/10"],
        "every_core_absolute_t_strict_upper_or_equal": "7/10",
        "core_rows_sha256": canonical_digest(rows),
    }


def exact_qnl_avoidance() -> dict[str, Any]:
    word = phase_cert.gray_white_gray_normal_word()
    assert word["physical_word"] == "G(0,0)->W(0,0)->G(0,0)"
    assert word["time_reverse_second_leg"] is True
    assert Q(1, 2) > Q(7, 10) ** 2
    assert Q(1, 2) > Q(1, 50) ** 2
    return {
        "parameter": "s=0",
        "exact_period": 2,
        "physical_word": word["physical_word"],
        "gray_phase": {
            "outward_normal": ["1/sqrt(2)", "1/sqrt(2)"],
            "p": "0",
        },
        "white_phase": {
            "outward_normal": ["-1/sqrt(2)", "-1/sqrt(2)"],
            "p": "0",
        },
        "dominant_chart_seam_at_both_collisions": True,
        "seam_ownership_independent_collision_coordinate": (
            "abs(t)=1/sqrt(2)"
        ),
        "exact_separation": {
            "one_over_sqrt_two_strictly_greater_than_7_over_10": (
                "1/2>(7/10)^2=49/100"
            ),
            "therefore_outside_every_axis_and_diagonal_core_t_interval": True,
        },
        "qnl_orbit_intersects_frozen_24_core_union": False,
        "first_24_core_entrance_time": "infinity",
        "finite_periodic_orbit_collision_SRB_mass": "0",
    }


def absorption_consequence() -> dict[str, Any]:
    return {
        "frozen_24_core_union_is_positive_collision_SRB_mass": True,
        "frozen_24_core_union_is_global_absorbing_trap": False,
        "claim_every_regular_collision_state_has_finite_first_core_entrance": (
            "REFUTED_BY_EXACT_QNL_PERIOD_TWO_ORBIT"
        ),
        "uniform_first_core_time_over_entire_regular_section": "IMPOSSIBLE",
        "valid_stopping_replacement": (
            "tau_core=inf{n>=0:T^n x in C}; cemetery={tau_core=infinity}"
        ),
        "the_displayed_qnl_cemetery_subset_has_zero_SRB_mass": True,
        "total_cemetery_mass_or_tail_from_this_counterexample": (
            "NOT_QUANTIFIED"
        ),
        "selected_128_parameter_germs_may_still_admit_branchwise_core_or_cemetery_typing": True,
        "selected_128_parameter_germ_first_core_destinations": "NOT_CERTIFIED",
        "required_next_object": (
            "a branchwise measurable core/cemetery stopping ledger with a charged "
            "tail or a positive-fraction unnormalised recovery theorem"
        ),
        "deterministic_all-state_core_propagation_is_not_a_valid_next_lemma": True,
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.fixed-core-absorption-obstruction.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "frozen_core_coordinate_envelope": core_coordinate_envelope(),
        "exact_qnl_core_avoidance": exact_qnl_avoidance(),
        "first_core_absorption_consequence": absorption_consequence(),
        "strict_nonpromotion": {
            "qnl_counterexample_lies_in_one_of_selected_128_parameter_germs": False,
            "selected_germ_core_reachability_refuted": False,
            "quantitative_cemetery_payload": "NOT_CERTIFIED",
            "native_2018_step_no_recut_dwell": "NOT_CERTIFIED",
            "native_12108_step_no_recut_dwell": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("EXACT_QNL_PERIOD_TWO_AVOIDS_24_CORE: CERTIFIED")
    print("GLOBAL_ALL_STATE_FIRST_24_CORE_ABSORPTION: REFUTED")
    print("SELECTED_PARAMETER_GERM_CORE_OR_CEMETERY_LEDGER: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
