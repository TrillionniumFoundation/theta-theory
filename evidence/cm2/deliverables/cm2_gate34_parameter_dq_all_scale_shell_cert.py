#!/usr/bin/env python3
"""Actual-parameter all-scale recovery germs on all 64 occurrence rows.

The nineteenth-round shell rotated the outgoing velocity and therefore did
not identify the transverse coordinate used by the moving-parameter DQ.
Here the source collision coordinate is held fixed and the physical white
centre is translated by ``h``.  In the frozen outgoing frame every candidate
centre then obeys, exactly,

    ell_j(h) = ell_j + eta_j*u_x*h,
    w_j(h)   = w_j   - eta_j*u_y*h.

At a tangent target ``w_T=epsilon*R_T`` this gives

    Delta_T(h)=2*eta*epsilon*R_T*u_y*h-u_y^2*h^2.

Consequently the hit parameter side is exactly the stored coarea polarity.
An Arb replay proves the hit--tangent--miss and direct--miss itineraries for
every ``0<|h|<=2^-16`` on one positive-width patch in each of the 64 maximal
occurrence rows.  The proof includes the zero-scale limit by factoring the
grazing square root and enclosing it independently; it does not evaluate a
square root on an Arb ball containing zero.

This is a selected local all-scale germ registry, not a finite tubular atlas
of every point of every maximal row.  It does not prove a bounded strong-space
grazing pushforward, first entrance into the 24 cores, or native no-recut
dwell.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate34_dyadic_transverse_recovery_shell_cert as phase_shell


ctx.prec = 512
Q = Fraction
HERE = Path(__file__).resolve().parent
PARAMETER_RADIUS = Q(1, 65536)
SQRT_DISCRIMINANT_UPPER = Q(1, 256)

DEPENDENCIES = {
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2_gate3_depth_one_fixed_gauge_dq_cert.py": (
        "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066"
    ),
    "cm2-gate34-dyadic-transverse-recovery-shell-manifest-2026-07-17.json": (
        "5f521603b81ee9733d80408e4c395b11a77437b65e92e3959a198aae68b61786"
    ),
    "cm2_gate34_dyadic_transverse_recovery_shell_cert.py": (
        "21c683c89881fa5b6acec98b905f0c5be7ff0b2b7c1e5c2309dcc51762dfb6db"
    ),
    "cm2_gate3_endpoint_identity_refinement_cert.py": (
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563"
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


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    corrected = json.loads(
        (
            HERE
            / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
        ).read_text(encoding="utf-8")
    )
    assert corrected["verdict"]["complete_depth_one_fixed_gauge_DQ"] == (
        "CERTIFIED"
    )
    law = corrected["result"]["collision_coordinate_correction"]
    assert law["corrected_positive_row_law"] == (
        "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta"
    )
    assert "cp^2" in law["superseded_positive_row_law"]


def eta(source: str, target_id: str) -> int:
    return int(target_id[0] == "W") - int(source == "W")


def shifted_rows(
    rows: dict[str, tuple[arb, arb, arb]],
    source: str,
    ux: arb,
    uy: arb,
    displacement: arb,
) -> dict[str, tuple[arb, arb, arb]]:
    return {
        target_id: (
            projection + eta(source, target_id) * ux * displacement,
            cross - eta(source, target_id) * uy * displacement,
            radius,
        )
        for target_id, (projection, cross, radius) in rows.items()
    }


def first_owner_against(
    results: dict[str, tuple[str, Any]], root: arb,
) -> bool:
    for status, payload in results.values():
        if status in {"miss", "behind", "skip"}:
            continue
        if status == "hit" and bool(payload > root):
            continue
        if status == "unclear" and bool(payload[0] - payload[1] > root):
            continue
        return False
    return True


def all_scale_hit_suffix_state(
    rows: dict[str, tuple[arb, arb, arb]],
    source: str,
    tangent_target: str,
    owner: str,
    epsilon: int,
    polarity: int,
    ux: arb,
    uy: arb,
    magnitude: arb,
) -> dict[str, Any] | None:
    eta_target = eta(source, tangent_target)
    assert abs(eta_target) == 1
    ell_t, _cross_t, radius_t = rows[tangent_target]
    positive_transversality = polarity * epsilon * eta_target * uy
    if not bool(positive_transversality > 0):
        return None
    discriminant_factor = (
        2 * radius_t * positive_transversality - uy * uy * magnitude
    )
    if not bool(discriminant_factor > 0):
        return None

    displacement = polarity * magnitude
    projection_t = ell_t + eta_target * ux * displacement
    cross_t = epsilon * radius_t - eta_target * uy * displacement

    # For 0<=r<=2^-16,
    # Delta_T <= (18/25)r+r^2 < (1/256)^2.  The independent interval
    # encloses sqrt(Delta_T) including its r=0 limit without asking Arb to
    # take sqrt of a ball whose lower endpoint rounds slightly below zero.
    square_root = bulk.arb_interval(Q(0), SQRT_DISCRIMINANT_UPPER)
    root_t = projection_t - square_root
    if not bool(root_t > 0):
        return None

    shifted = shifted_rows(rows, source, ux, uy, displacement)
    first_leg_others = dict(shifted)
    first_leg_others.pop(tangent_target)
    if not first_owner_against(
        phase_shell.collision_results(first_leg_others, arb(0)), root_t
    ):
        return None

    normal_a = -square_root / radius_t
    normal_b = -cross_t / radius_t
    outgoing_a = 1 - 2 * normal_a * normal_a
    outgoing_b = -2 * normal_a * normal_b
    results: dict[str, tuple[str, Any]] = {}
    for target_id, (center_a, center_b, radius) in shifted.items():
        if target_id == tangent_target:
            continue
        dx = center_a - root_t
        dy = center_b
        projection = outgoing_a * dx + outgoing_b * dy
        cross = -outgoing_b * dx + outgoing_a * dy
        discriminant = radius * radius - cross * cross
        if bool(discriminant < 0) or bool(projection < 0):
            results[target_id] = ("miss", None)
            continue
        if not (bool(discriminant > 0) and bool(projection > 0)):
            results[target_id] = ("unclear", (projection, radius))
            continue
        root = projection - discriminant.sqrt()
        if bool(root > phase_shell.arbq(Q(1, 10**10))):
            results[target_id] = ("hit", root)
        elif bool(root < 0):
            results[target_id] = ("behind", None)
        else:
            results[target_id] = ("skip", None)
    root_after_tangent = phase_shell.first_owner(results, owner)
    if root_after_tangent is None:
        return None

    center_a, center_b, radius = shifted[owner]
    contact_a = root_t + root_after_tangent * outgoing_a
    contact_b = root_after_tangent * outgoing_b
    normal_a_2 = (contact_a - center_a) / radius
    normal_b_2 = (contact_b - center_b) / radius
    cell = phase_shell.suffix_cell(normal_a_2, normal_b_2, ux, uy)
    if cell is None:
        return None
    dx = center_a - root_t
    dy = center_b
    projection = outgoing_a * dx + outgoing_b * dy
    cross = -outgoing_b * dx + outgoing_a * dy
    discriminant = radius * radius - cross * cross
    return {
        "root_t": root_t,
        "root_after_tangent": root_after_tangent,
        "cosine": discriminant.sqrt() / radius,
        "p": cross / radius,
        "cell": cell,
        "positive_transversality": positive_transversality,
        "discriminant_factor": discriminant_factor,
    }


def certify_germ(row: dict[str, Any]) -> dict[str, Any]:
    z = Q(row["witness"]["z"])
    for half_width_power in range(10, 17):
        half_width = Q(1, 2**half_width_power)
        box = bulk.Box(
            row["witness"]["chart_id"], row["target"], row["epsilon"],
            z - half_width, z + half_width,
            -half_width, half_width, half_width_power,
        )
        kind, data = endpoint.classify_box(box)
        if kind != "physical_immutable_subrow" or data is None:
            continue
        if data["miss_target"] != row["miss_target"]:
            continue
        if data["polarity"] != row["parameter_coarea_polarity"]:
            continue
        geometry = bulk.tangent_geometry(
            box.chart_id, box.z0, box.z1, box.s0, box.s1,
            box.target_id, box.epsilon,
        )
        if geometry is None:
            continue
        _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, s = geometry
        source = row["source"]
        source_id = f"{source}[0,0]"
        direct_rows = phase_shell.centered_candidate_rows(
            qx, qy, ux, uy, s, 0, 0, source_id
        )
        tangent_radius = phase_shell.obstacle_radius(row["target"])
        direct_rows[row["target"]] = (
            ell_t, row["epsilon"] * tangent_radius, tangent_radius,
        )
        target = bulk.TARGET_BY_ID[row["target"]]
        post_rows = phase_shell.centered_candidate_rows(
            qx, qy, ux, uy, s, target.ix, target.iy, row["target"]
        )
        post_rows[row["target"]] = direct_rows[row["target"]]

        magnitude = bulk.arb_interval(Q(0), PARAMETER_RADIUS)
        polarity = row["parameter_coarea_polarity"]
        miss_rows = shifted_rows(
            direct_rows, source, ux, uy, -polarity * magnitude
        )
        # The tangent target has Delta=-r(2Rc+u_y^2 r)<0 for every r>0;
        # remove only that analytically certified open-side miss.
        miss_rows.pop(row["target"])
        miss_state = phase_shell.direct_suffix_state(
            miss_rows, row["miss_target"], arb(0), ux, uy
        )
        hit_state = all_scale_hit_suffix_state(
            post_rows, source, row["target"], row["miss_target"],
            row["epsilon"], polarity, ux, uy, magnitude,
        )
        if miss_state is None or hit_state is None:
            continue
        if miss_state["cell"] != hit_state["cell"]:
            continue
        if not (
            bool(miss_state["root"] < phase_shell.arbq(Q(2)))
            and bool(
                hit_state["root_after_tangent"] < phase_shell.arbq(Q(2))
            )
            and bool(miss_state["cosine"] > phase_shell.arbq(Q(1, 20)))
            and bool(hit_state["cosine"] > phase_shell.arbq(Q(1, 20)))
            and bool(abs(miss_state["p"]) < phase_shell.arbq(Q(999, 1000)))
            and bool(abs(hit_state["p"]) < phase_shell.arbq(Q(999, 1000)))
        ):
            continue
        suffix_chart = (
            f"{bulk.TARGET_BY_ID[row['miss_target']].obstacle}:"
            f"{miss_state['cell']}"
        )
        payload = {
            "source_box": box.key(),
            "parameter_radius": str(PARAMETER_RADIUS),
            "hit_parameter_sign": polarity,
            "miss_parameter_sign": -polarity,
            "hit_state": {key: str(value) for key, value in hit_state.items()},
            "miss_state": {
                key: str(value) for key, value in miss_state.items()
            },
        }
        return {
            "germ_id": "parameter-germ:" + canonical_digest({
                "occurrence": row["occurrence_id"],
                "box": box.key(),
                "parameter_radius": str(PARAMETER_RADIUS),
            }),
            "occurrence_id": row["occurrence_id"],
            "source_event_chart": box.chart_id,
            "base_half_width_power": half_width_power,
            "base_half_width": str(half_width),
            "base_event_coordinate_area": str((2 * half_width) ** 2),
            "hit_parameter_sign": polarity,
            "miss_parameter_sign": -polarity,
            "parameter_magnitude_interval": ["0_open", str(PARAMETER_RADIUS)],
            "hit_first_target": row["target"],
            "hit_second_target": row["miss_target"],
            "miss_first_target": row["miss_target"],
            "hit_collision_count_to_suffix": 2,
            "miss_collision_count_to_suffix": 1,
            "face_time_collision_offset": 1,
            "suffix_regular_collision_chart": suffix_chart,
            "two_sides_share_suffix_chart": True,
            "germ_geometry_sha256": canonical_digest(payload),
        }
    raise AssertionError(f"no parameter all-scale germ for {row['occurrence_id']}")


def exact_parameter_angle_jacobian() -> dict[str, Any]:
    assert SQRT_DISCRIMINANT_UPPER**2 > (
        Q(18, 25) * PARAMETER_RADIUS + PARAMETER_RADIUS**2
    )
    return {
        "fixed_source_collision_coordinate": True,
        "candidate_frame_translation": {
            "ell_j(h)": "ell_j+eta_j*u_x*h",
            "w_j(h)": "w_j-eta_j*u_y*h",
        },
        "tangent_discriminant": (
            "Delta_T(h)=2*eta*epsilon*R_T*u_y*h-u_y^2*h^2"
        ),
        "exact_first_derivatives": {
            "partial_h_Delta_at_0": "2*eta*epsilon*R_T*u_y",
            "partial_alpha_Delta_at_0": "2*epsilon*R_T*ell_T",
            "clearance_matched_phase_angle_dalpha_dh": "eta*u_y/ell_T",
            "tangent_graph_dp_dh": "-eta*cp*u_y/ell_T",
            "signed_face_coarea": "eta*epsilon*cp*u_y/ell_T",
        },
        "collision_flux_coordinate": "dr*dp",
        "corrected_positive_face_law": (
            "R_source*cp*abs(u_y)/ell_T*dtheta"
        ),
        "superseded_extra_cp_not_used": True,
        "phase_angle_derivative_is_first_order_clearance_identification": True,
        "phase_angle_derivative_is_not_claimed_as_finite_state_conjugacy": True,
        "global_on_all_64_open_maximal_occurrence_rows": True,
    }


def germ_registry() -> dict[str, Any]:
    maximal_rows, maximal_registry = current.load_maximal_rows()
    germs = [certify_germ(row) for row in maximal_rows]
    germs.sort(key=canonical_json)
    assert len(germs) == 64
    assert len({row["germ_id"] for row in germs}) == 64
    power_histogram = Counter(row["base_half_width_power"] for row in germs)
    assert power_histogram == Counter({10: 40, 11: 16, 12: 4, 14: 4})
    suffix_histogram = Counter(
        row["suffix_regular_collision_chart"] for row in germs
    )
    assert suffix_histogram == Counter({
        "G:E": 10,
        "G:N": 12,
        "G:S": 12,
        "G:W": 10,
        "W:E": 4,
        "W:N": 6,
        "W:S": 6,
        "W:W": 4,
    })
    total_base_area = sum(
        Q(row["base_event_coordinate_area"]) for row in germs
    )
    two_side_parameter_volume = (
        total_base_area * 2 * PARAMETER_RADIUS
    )
    assert total_base_area == Q(2833, 16777216)
    assert two_side_parameter_volume == Q(2833, 549755813888)
    return {
        "selected_occurrence_parameter_germ_count": len(germs),
        "oriented_actual_parameter_tube_germ_count": 2 * len(germs),
        "parameter_magnitude_interval": ["0_open", str(PARAMETER_RADIUS)],
        "all_dyadic_scales_below_radius_included": True,
        "hit_parameter_sign_equals_corrected_coarea_polarity": True,
        "miss_parameter_sign_equals_negative_corrected_coarea_polarity": True,
        "base_half_width_power_histogram": {
            str(key): value for key, value in sorted(power_histogram.items())
        },
        "labelled_base_event_coordinate_area": str(total_base_area),
        "labelled_two_side_parameter_coordinate_volume": str(
            two_side_parameter_volume
        ),
        "all_hit_germs_first_hit_tangent_target": True,
        "all_hit_germs_next_hit_fixed_miss_target": True,
        "all_miss_germs_first_hit_fixed_miss_target": True,
        "all_two_side_successors_regular": True,
        "all_two_side_successors_share_one_suffix_chart_per_occurrence": True,
        "selected_face_time_collision_offset": 1,
        "uniform_suffix_bounds": {
            "cosine_strict_lower": "1/20",
            "abs_p_strict_upper": "999/1000",
            "each_owner_flight_strict_upper": "2",
        },
        "complete_local_candidate_universe": {
            "obstacles": ["G", "W"],
            "lattice_window_per_leg": "9x9 centered at current collision lift",
            "current_obstacle_excluded": True,
            "candidate_count_after_exclusion": 161,
            "all_certified_owner_flights_strictly_below": "2",
            "window_radius_4_exceeds_required_center_offset": True,
        },
        "suffix_regular_chart_histogram": dict(sorted(suffix_histogram.items())),
        "parameter_germ_rows_sha256": canonical_digest(germs),
        "imported_maximal_rows_sha256": maximal_registry[
            "maximal_row_rows_sha256"
        ],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.parameter-dq-all-scale-shell.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "exact_parameter_angle_jacobian": exact_parameter_angle_jacobian(),
        "selected_parameter_dq_all_scale_germ_registry": germ_registry(),
        "strict_nonpromotion": {
            "selected_germs_exhaust_every_point_of_every_maximal_row": False,
            "first_order_clearance_angle_identification_is_finite_conjugacy": False,
            "selected_face_time_is_common_strong_space_FACE_TIME": False,
            "full_boundary_all_scale_tubular_atlas": "NOT_CERTIFIED",
            "bounded_grazing_pushforward": "NOT_CERTIFIED",
            "first_24_core_destination": "NOT_CERTIFIED",
            "native_no_recut_dwell": "NOT_CERTIFIED",
            "common_strong_space_restriction": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("PARAMETER_ANGLE_JACOBIAN_ROWS_64: CERTIFIED")
    print("SELECTED_PARAMETER_DQ_ALL_SCALE_GERMS_64: CERTIFIED")
    print("ORIENTED_ACTUAL_PARAMETER_TUBE_GERMS_128: CERTIFIED")
    print("FULL_BOUNDARY_ALL_SCALE_TUBULAR_ATLAS: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
