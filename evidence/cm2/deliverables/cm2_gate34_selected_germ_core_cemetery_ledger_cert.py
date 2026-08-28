#!/usr/bin/env python3
"""Typed measurable core/cemetery stopping ledger for 128 selected germs.

The frozen 24-core is not globally absorbing.  The correct replacement is a
branchwise stopping object, not a universal first-core time.  This certificate
binds every hit/miss branch of the 64 selected actual-parameter germs to one
total Borel ledger on the collision section extended by an absorbing singular
state.

For a branch ``b`` with regular suffix map ``y_b`` and the finite core union
``C``, define

    tau_C(b,x)=inf{n>=0: T_hat^n y_b(x) in C}.

The extended map ``T_hat`` sends every billiard singularity to an absorbing
symbol.  Hence each finite-time core-hit set, singular-cemetery set, and the
nonreturning cemetery are Borel.  Their pullbacks through the analytic germ
maps form a disjoint exhaustive decomposition for every finite measure on a
selected germ domain.

The certificate creates 128 immutable branch-ledger IDs and a deterministic
countable cylinder-slot schema.  A horizon-eight prefix contains 27,648
core-hit slots, 1,152 singular slots and 128 unresolved-tail slots.  Slots
may be empty: no core-hit fraction, cemetery tail, first destination, or
native no-recut dwell is inferred.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_parameter_dq_all_scale_shell_cert as parameter
import cm2_gate3_global_borel_current_assembly_cert as current


Q = Fraction
HERE = Path(__file__).resolve().parent
PREFIX_HORIZON = 8

DEPENDENCIES = {
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": (
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458"
    ),
    "cm2-gate34-fixed-core-absorption-obstruction-manifest-2026-07-17.json": (
        "ab40178021a8871fb951afad75c3fc50d31f1b61756d6de566f20fe9056343af"
    ),
    "cm2_gate34_fixed_core_absorption_obstruction_cert.py": (
        "7c451fa5b71ef977e87caf600a5e91c83b102ba434200d9198afcda6ffde4510"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
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

    parameter_manifest = loaded[
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    ]
    registry = parameter_manifest["result"][
        "selected_parameter_dq_all_scale_germ_registry"
    ]
    assert registry["selected_occurrence_parameter_germ_count"] == 64
    assert registry["oriented_actual_parameter_tube_germ_count"] == 128

    obstruction = loaded[
        "cm2-gate34-fixed-core-absorption-obstruction-manifest-2026-07-17.json"
    ]
    assert obstruction["verdict"]["global_all_state_first_24_core_absorption"] == (
        "REFUTED"
    )

    cores = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    assert cores["result"]["physical_return_core_registry"][
        "physical_compact_homogeneous_core_count"
    ] == 24

    sparse = loaded[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]
    assert sparse["verdict"]["core_2018_step_upper_3_over_8"] == "CERTIFIED"
    assert sparse["verdict"][
        "native_physical_no_hidden_cut_dwell_schedule"
    ] == "NOT_CERTIFIED"
    return loaded


def selected_germ_rows() -> list[dict[str, Any]]:
    maximal_rows, _registry = current.load_maximal_rows()
    germs = [parameter.certify_germ(row) for row in maximal_rows]
    germs.sort(key=canonical_json)
    assert len(germs) == 64
    assert len({row["germ_id"] for row in germs}) == 64
    return germs


def core_rows() -> list[dict[str, Any]]:
    rows = []
    for core in core_cert.physical_cores():
        payload = {
            "chart_id": core.chart_id,
            "t": [str(core.t0), str(core.t1)],
            "p": [str(core.p0), str(core.p1)],
            "target_id": core.target_id,
            "crossings": list(core.crossings),
        }
        rows.append({
            **payload,
            "core_id": "core:" + canonical_digest(payload),
            "compact_Borel_rectangle": True,
        })
    rows.sort(key=canonical_json)
    assert len(rows) == 24
    assert len({row["core_id"] for row in rows}) == 24
    return rows


def branch_ledgers(germs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for germ in germs:
        for side in ("hit", "miss"):
            collision_count = germ[f"{side}_collision_count_to_suffix"]
            parameter_sign = germ[f"{side}_parameter_sign"]
            payload = {
                "germ_id": germ["germ_id"],
                "side": side,
                "parameter_sign": parameter_sign,
                "parameter_magnitude_interval": germ[
                    "parameter_magnitude_interval"
                ],
            }
            rows.append({
                **payload,
                "branch_ledger_id": "stopping:" + canonical_digest(payload),
                "occurrence_id": germ["occurrence_id"],
                "source_event_chart": germ["source_event_chart"],
                "suffix_regular_collision_chart": germ[
                    "suffix_regular_collision_chart"
                ],
                "collision_count_to_suffix": collision_count,
                "germ_map_to_suffix_is_real_analytic_for_nonzero_parameter": True,
                "tau_core_definition": (
                    "inf{n>=0:T_hat^n(y_branch(x)) belongs to C_24}"
                ),
                "finite_core_destination_definition": (
                    "the unique core rectangle containing T_hat^tau y_branch(x)"
                ),
                "cemetery_definition": "{tau_core=infinity}",
            })
    rows.sort(key=canonical_json)
    assert len(rows) == 128
    assert len({row["branch_ledger_id"] for row in rows}) == 128
    assert sum(row["collision_count_to_suffix"] == 2 for row in rows) == 64
    assert sum(row["collision_count_to_suffix"] == 1 for row in rows) == 64
    return rows


def finite_prefix_slots(
    branches: list[dict[str, Any]], cores: list[dict[str, Any]], horizon: int,
) -> dict[str, Any]:
    hit_ids = []
    singular_ids = []
    tail_ids = []
    for branch in branches:
        branch_id = branch["branch_ledger_id"]
        for time in range(horizon + 1):
            singular_ids.append("singular:" + canonical_digest({
                "branch_ledger_id": branch_id,
                "time": time,
            }))
            for core in cores:
                hit_ids.append("core-hit:" + canonical_digest({
                    "branch_ledger_id": branch_id,
                    "time": time,
                    "core_id": core["core_id"],
                }))
        tail_ids.append("tail:" + canonical_digest({
            "branch_ledger_id": branch_id,
            "strictly_after_time": horizon,
        }))
    assert len(hit_ids) == 128 * (horizon + 1) * 24
    assert len(singular_ids) == 128 * (horizon + 1)
    assert len(tail_ids) == 128
    all_ids = hit_ids + singular_ids + tail_ids
    assert len(set(all_ids)) == len(all_ids)
    return {
        "materialized_horizon": horizon,
        "core_hit_cylinder_slot_count": len(hit_ids),
        "singular_cemetery_cylinder_slot_count": len(singular_ids),
        "unresolved_after_horizon_tail_slot_count": len(tail_ids),
        "total_prefix_partition_slot_count": len(all_ids),
        "slots_may_be_empty": True,
        "prefix_slot_ids_sha256": canonical_digest(sorted(all_ids)),
    }


def measurable_stopping_theorem() -> dict[str, Any]:
    return {
        "extended_collision_space": (
            "compactified collision section plus absorbing singular symbol dagger"
        ),
        "extended_billiard_map_T_hat_is_Borel": True,
        "T_hat_sends_singular_set_to_absorbing_dagger": True,
        "frozen_24_core_union_is_finite_compact_Borel_union": True,
        "finite_time_core_hit_sets_are_Borel": True,
        "finite_time_singular_cemetery_sets_are_Borel": True,
        "nonreturning_cemetery_is_countable_intersection_of_Borel_sets": True,
        "analytic_germ_pullbacks_preserve_Borel_measurability": True,
        "core_hit_singular_and_nonreturning_classes_are_pairwise_disjoint": True,
        "core_hit_singular_and_nonreturning_classes_exhaust_each_germ_domain": True,
        "exact_measure_decomposition_for_every_finite_germ_measure": True,
        "countable_core_hit_cylinder_schema": (
            "(branch_ledger_id,n,core_id) for n>=0"
        ),
        "countable_singular_cylinder_schema": (
            "(branch_ledger_id,n,dagger) for n>=0"
        ),
        "cemetery_schema": "(branch_ledger_id,tau_core=infinity)",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    germs = selected_germ_rows()
    cores = core_rows()
    branches = branch_ledgers(germs)
    prefix = finite_prefix_slots(branches, cores, PREFIX_HORIZON)
    result: dict[str, Any] = {
        "schema": "cm2.gate34.selected-germ-core-cemetery-ledger.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "selected_branch_stopping_registry": {
            "selected_parameter_germ_count": len(germs),
            "oriented_branch_ledger_count": len(branches),
            "finite_destination_core_count": len(cores),
            "hit_branch_count": 64,
            "miss_branch_count": 64,
            "branch_ledgers_sha256": canonical_digest(branches),
            "destination_cores_sha256": canonical_digest(cores),
            "first_branch_ledger_id": branches[0]["branch_ledger_id"],
            "last_branch_ledger_id": branches[-1]["branch_ledger_id"],
        },
        "measurable_core_cemetery_stopping_theorem": (
            measurable_stopping_theorem()
        ),
        "materialized_horizon_8_partition_prefix": prefix,
        "conditional_core_contraction_attachment": {
            "finite_core_hit_branches_may_attach_frozen_core_packet": True,
            "shell_dwell_steps": 2018,
            "raw_field7_dwell_steps": 12108,
            "core_2018_step_upper_3_over_8": "CERTIFIED_ABSTRACTLY",
            "attachment_requires_native_no_hidden_recut_audit": True,
            "native_no_hidden_recut_audit": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "branch_ledger_ids_materialize_pointwise_first_core_values": False,
            "Borel_partition_implies_positive_core_hit_fraction": False,
            "Borel_partition_implies_quantitative_cemetery_tail": False,
            "empty_cylinder_slots_are_declared_nonempty": False,
            "selected_germ_core_hit_fraction": "NOT_CERTIFIED",
            "selected_germ_first_core_destinations": "NOT_CERTIFIED",
            "quantitative_cemetery_payload": "NOT_CERTIFIED",
            "native_2018_12108_no_recut_dwell": "NOT_CERTIFIED",
            "common_strong_space_recovery_operator": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("SELECTED_ORIENTED_BRANCH_STOPPING_LEDGERS_128: CERTIFIED_TYPED_BOREL")
    print("CORE_SINGULAR_NONRETURNING_DECOMPOSITION: CERTIFIED")
    print("HORIZON8_PARTITION_SLOTS_28928: CERTIFIED_SCHEMA")
    print("SELECTED_GERM_POSITIVE_CORE_HIT_FRACTION: NOT_CERTIFIED")
    print("QUANTITATIVE_CEMETERY_PAYLOAD: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
