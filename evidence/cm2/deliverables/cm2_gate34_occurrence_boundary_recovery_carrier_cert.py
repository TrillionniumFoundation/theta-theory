#!/usr/bin/env python3
"""Boundary recovery carriers for all maximal physical occurrence rows."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json": (
        "2a25426d0a3f90a3fc2df592626d01cf294394f14590a9b1e9338f65ba8614f8"
    ),
    "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json": (
        "dce243c64d4e4fef44a023e8145b22c68233fcce7a8447d83ff86aa0a2d32bdf"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
    "cm2_gate3_global_physical_subrow_atlas_cert.py": (
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def load_dependencies() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))
    assert loaded[
        "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json"
    ]["verdict"]["global_finite_Borel_event_current"] == "CERTIFIED"
    assert loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"][
        "physical_compact_homogeneous_core_count"
    ] == 24
    sparse = loaded[
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    ]
    assert sparse["verdict"]["core_2018_step_upper_3_over_8"] == "CERTIFIED"
    assert sparse["verdict"]["transported_occurrence_to_24_core_incidence"] == (
        "NOT_CERTIFIED"
    )
    return loaded


def target_obstacle(target_id: str) -> str:
    return bulk.TARGET_BY_ID[target_id].obstacle


def witness_common_state(row: dict[str, Any]) -> dict[str, Any]:
    z = Q(row["witness"]["z"])
    geometry = bulk.tangent_geometry(
        row["witness"]["chart_id"], z, z, Q(0), Q(0),
        row["target"], row["epsilon"],
    )
    assert geometry is not None
    nx, ny, qx, qy, ux, uy, ell_t, cp, p_source, s = geometry
    assert bool(cp > arbq(Q(3, 20)))
    assert bool(abs(p_source) < arbq(Q(99, 100)))

    target = bulk.TARGET_BY_ID[row["target"]]
    target_x, target_y = bulk.cached_target_center(row["target"], s)
    target_dx, target_dy = target_x - qx, target_y - qy
    tangent_cross = -uy * target_dx + ux * target_dy
    tangent_radius = bulk.ARB_RADIUS[target.obstacle]
    assert bool(
        abs(tangent_cross - row["epsilon"] * tangent_radius)
        < arbq(Q(1, 10**50))
    )

    competitors = bulk.competitor_rows(
        qx, qy, ux, uy, s, row["target"],
        bulk.GLOBAL_CANDIDATE_IDS[row["source"]],
    )
    ell_m, delta_m, cross_m = competitors[row["miss_target"]]
    assert bool(delta_m > 0)
    miss_radical = delta_m.sqrt()
    root_m = ell_m - miss_radical
    gap = root_m - ell_t
    assert bool(gap > arbq(Q(31, 100)))
    assert bool(root_m < arbq(Q(8, 5)))

    miss = bulk.TARGET_BY_ID[row["miss_target"]]
    miss_radius = bulk.ARB_RADIUS[miss.obstacle]
    p_miss = cross_m / miss_radius
    cosine_miss = miss_radical / miss_radius
    assert bool(abs(p_miss) < arbq(Q(97, 100)))
    assert bool(cosine_miss > arbq(Q(6, 25)))

    miss_x, miss_y = bulk.cached_target_center(row["miss_target"], s)
    hit_x = qx + root_m * ux
    hit_y = qy + root_m * uy
    miss_nx = (hit_x - miss_x) / miss_radius
    miss_ny = (hit_y - miss_y) / miss_radius
    incoming_normal = ux * miss_nx + uy * miss_ny
    assert bool(incoming_normal < -arbq(Q(6, 25)))
    out_x = ux - 2 * incoming_normal * miss_nx
    out_y = uy - 2 * incoming_normal * miss_ny
    assert bool(out_x * miss_nx + out_y * miss_ny > arbq(Q(6, 25)))
    assert bool(abs(-miss_ny * out_x + miss_nx * out_y) < arbq(Q(97, 100)))
    speed_squared = out_x * out_x + out_y * out_y
    assert bool(speed_squared > arbq(Q(999, 1000)))
    assert bool(speed_squared < arbq(Q(1001, 1000)))

    tangent_hit_x = qx + ell_t * ux
    tangent_hit_y = qy + ell_t * uy
    tangent_nx = (tangent_hit_x - target_x) / tangent_radius
    tangent_ny = (tangent_hit_y - target_y) / tangent_radius
    tangent_normal_velocity = ux * tangent_nx + uy * tangent_ny
    assert bool(abs(tangent_normal_velocity) < arbq(Q(1, 10**50)))
    continuation_error_x = tangent_hit_x + gap * ux - hit_x
    continuation_error_y = tangent_hit_y + gap * uy - hit_y
    assert bool(abs(continuation_error_x) < arbq(Q(1, 10**50)))
    assert bool(abs(continuation_error_y) < arbq(Q(1, 10**50)))

    geometry_payload = {
        "source_cp": str(cp),
        "source_p": str(p_source),
        "tangent_flight": str(ell_t),
        "miss_flight": str(root_m),
        "post_tangent_gap": str(gap),
        "miss_p": str(p_miss),
        "miss_cosine": str(cosine_miss),
        "miss_contact": [str(hit_x), str(hit_y)],
        "miss_outgoing_velocity": [str(out_x), str(out_y)],
    }
    return {
        "geometry_sha256": canonical_digest(geometry_payload),
        "tangent_target_p_is_epsilon_exactly": True,
        "tangent_reflection_is_identity_in_boundary_limit": True,
        "hit_then_gap_equals_direct_miss_contact": True,
        "miss_collision_is_strictly_regular": True,
    }


def carrier_row(row: dict[str, Any]) -> dict[str, Any]:
    base_payload = {
        "occurrence_id": row["occurrence_id"],
        "base": row["base"],
        "left_boundary": row["left_boundary"],
        "right_boundary": row["right_boundary"],
    }
    base_signature = "base:" + canonical_digest(base_payload)
    hit_seed = "trace:" + canonical_digest({
        "base": base_signature,
        "kind": "hit",
        "target": row["target"],
        "epsilon": row["epsilon"],
    })
    miss_seed = "trace:" + canonical_digest({
        "base": base_signature,
        "kind": "miss",
        "target": row["miss_target"],
    })
    common_carrier = "recovery:" + canonical_digest({
        "base": base_signature,
        "continuation": [row["target"], row["miss_target"]],
    })
    witness = witness_common_state(row)
    return {
        "occurrence_id": row["occurrence_id"],
        "global_physical_label": row["global_physical_label"],
        "base_signature": base_signature,
        "hit_trace_seed_id": hit_seed,
        "miss_trace_seed_id": miss_seed,
        "common_boundary_recovery_carrier_id": common_carrier,
        "hit_boundary_target_sequence": [row["target"], row["miss_target"]],
        "miss_boundary_target_sequence": [row["miss_target"]],
        "collision_offset_to_common_carrier": {"hit": 1, "miss": 0},
        "common_carrier_collision_target": row["miss_target"],
        "shared_pulled_back_event_base_restriction": True,
        "witness_replay": witness,
    }


def build_carrier_registry() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    maximal_rows, maximal_registry = current.load_maximal_rows()
    rows = [carrier_row(row) for row in maximal_rows]
    rows.sort(key=canonical_json)
    assert len(rows) == 64
    occurrence_ids = {row["occurrence_id"] for row in rows}
    base_ids = {row["base_signature"] for row in rows}
    carrier_ids = {
        row["common_boundary_recovery_carrier_id"] for row in rows
    }
    trace_ids = {
        trace_id
        for row in rows
        for trace_id in (row["hit_trace_seed_id"], row["miss_trace_seed_id"])
    }
    assert len(occurrence_ids) == len(base_ids) == len(carrier_ids) == 64
    assert len(trace_ids) == 128

    by_label = {
        tuple(row["global_physical_label"]): row for row in rows
    }
    reflection_pairs = set()
    for label, row in by_label.items():
        partner = by_label[current.reflected_label(label)]
        pair = tuple(sorted((
            row["common_boundary_recovery_carrier_id"],
            partner["common_boundary_recovery_carrier_id"],
        )))
        reflection_pairs.add(pair)
    assert len(reflection_pairs) == 32

    type_histogram = Counter(
        f"{row['global_physical_label'][0]}->"
        f"{target_obstacle(row['global_physical_label'][1])}(graze)->"
        f"{target_obstacle(row['global_physical_label'][3])}"
        for row in rows
    )
    assert type_histogram == Counter({
        "G->W(graze)->G": 36,
        "W->G(graze)->W": 12,
        "G->W(graze)->W": 8,
        "W->G(graze)->G": 8,
    })
    epsilon_histogram = Counter(
        row["global_physical_label"][2] for row in rows
    )
    assert epsilon_histogram == Counter({-1: 32, 1: 32})

    registry = {
        "maximal_occurrence_row_count": len(rows),
        "oriented_hit_miss_trace_seed_count": len(trace_ids),
        "common_boundary_recovery_carrier_count": len(carrier_ids),
        "distinct_shared_event_base_signature_count": len(base_ids),
        "Jx_reflection_carrier_pair_count": len(reflection_pairs),
        "type_histogram": dict(sorted(type_histogram.items())),
        "epsilon_histogram": {
            str(key): value for key, value in sorted(epsilon_histogram.items())
        },
        "all_open_rows_have_analytic_boundary_continuation_carrier": True,
        "hit_collision_offset_to_common_carrier": 1,
        "miss_collision_offset_to_common_carrier": 0,
        "all_witness_common_collisions_strictly_regular": True,
        "uniform_witness_bounds": {
            "source_cosine_strict_lower": "3/20",
            "source_abs_p_strict_upper": "99/100",
            "post_tangent_flight_gap_strict_lower": "31/100",
            "common_miss_flight_strict_upper": "8/5",
            "common_miss_abs_p_strict_upper": "97/100",
            "common_miss_cosine_strict_lower": "6/25",
        },
        "carrier_rows_sha256": canonical_digest(rows),
        "reflection_pairs_sha256": canonical_digest(sorted(reflection_pairs)),
        "imported_maximal_rows_sha256": maximal_registry[
            "maximal_row_rows_sha256"
        ],
        "first_carrier_id": rows[0]["common_boundary_recovery_carrier_id"],
        "last_carrier_id": rows[-1]["common_boundary_recovery_carrier_id"],
    }
    return rows, registry


def installation_frontier() -> dict[str, Any]:
    return {
        "what_is_now_physical": (
            "each event-base point has two boundary traces whose singular "
            "limits meet on one regular collision graph over the fixed miss target"
        ),
        "common_event_base_restriction_materialized": True,
        "boundary_collision_offsets_materialized": True,
        "open_shell_neighborhood_transport": "NOT_CERTIFIED",
        "uniform_full_open_row_homogeneity_margin": "NOT_CERTIFIED",
        "first_24_core_destination": "NOT_CERTIFIED",
        "native_2018_step_no_recut_dwell": "NOT_CERTIFIED",
        "native_12108_step_no_recut_dwell": "NOT_CERTIFIED",
        "bounded_pushforward_through_grazing_hit": "NOT_CERTIFIED",
        "common_strong_space_restriction": "NOT_CERTIFIED",
        "cemetery_payload": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    _rows, registry = build_carrier_registry()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.occurrence-boundary-recovery-carrier.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "boundary_recovery_carrier_registry": registry,
        "physical_installation_frontier": installation_frontier(),
        "strict_nonpromotion": {
            "boundary_carrier_equals_open_shell_recovery": False,
            "boundary_collision_offset_equals_native_transport_time": False,
            "witness_margin_equals_uniform_row_margin": False,
            "transported_occurrence_to_24_core_incidence": "NOT_CERTIFIED",
            "native_repeated_recovery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("BOUNDARY_RECOVERY_CARRIERS_64: CERTIFIED")
    print("ORIENTED_TRACE_SEEDS_128: CERTIFIED")
    print("BOUNDARY_HIT_MISS_COLLISION_OFFSETS_1_0: CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
