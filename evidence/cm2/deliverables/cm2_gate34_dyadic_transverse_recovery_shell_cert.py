#!/usr/bin/env python3
"""One certified dyadic phase-angle recovery shell on every occurrence row."""

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


ctx.prec = 512
Q = Fraction
HERE = Path(__file__).resolve().parent
ANGLE_LOWER = Q(1, 65536)
ANGLE_UPPER = Q(1, 32768)

DEPENDENCIES = {
    "cm2-gate34-uniform-boundary-carrier-patch-manifest-2026-07-17.json": (
        "59873a42cfc12d016b7a87d9abdc18e6d14da1a76ac1f496d88642fb722049f2"
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


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    manifest = json.loads(
        (
            HERE
            / "cm2-gate34-uniform-boundary-carrier-patch-manifest-2026-07-17.json"
        ).read_text(encoding="utf-8")
    )
    assert manifest["verdict"]["uniform_boundary_carrier_patches_64"] == (
        "CERTIFIED"
    )
    assert manifest["verdict"]["two_sided_open_shell_transport"] == (
        "NOT_CERTIFIED"
    )


def obstacle_radius(target_id: str) -> arb:
    return bulk.ARB_RADIUS[target_id[0]]


def centered_candidate_rows(
    qx: arb,
    qy: arb,
    ux: arb,
    uy: arb,
    s: arb,
    center_ix: int,
    center_iy: int,
    excluded: str,
) -> dict[str, tuple[arb, arb, arb]]:
    rows: dict[str, tuple[arb, arb, arb]] = {}
    for obstacle in ("G", "W"):
        for ix in range(center_ix - 4, center_ix + 5):
            for iy in range(center_iy - 4, center_iy + 5):
                target_id = f"{obstacle}[{ix},{iy}]"
                if target_id == excluded:
                    continue
                ax = arb(ix)
                ay = arb(iy)
                if obstacle == "W":
                    ax += arbq(Q(1, 2)) + s
                    ay += arbq(Q(1, 2))
                dx, dy = ax - qx, ay - qy
                rows[target_id] = (
                    ux * dx + uy * dy,
                    -uy * dx + ux * dy,
                    obstacle_radius(target_id),
                )
    assert len(rows) == 161
    return rows


def rotate_coordinates(
    projection: arb, cross: arb, angle: arb,
) -> tuple[arb, arb]:
    cosine = angle.cos()
    sine = angle.sin()
    return (
        projection * cosine + cross * sine,
        cross * cosine - projection * sine,
    )


def collision_results(
    rows: dict[str, tuple[arb, arb, arb]], angle: arb,
) -> dict[str, tuple[str, Any]]:
    results: dict[str, tuple[str, Any]] = {}
    for target_id, (projection_0, cross_0, radius) in rows.items():
        projection, cross = rotate_coordinates(projection_0, cross_0, angle)
        discriminant = radius * radius - cross * cross
        if bool(discriminant < 0) or bool(projection < 0):
            results[target_id] = ("miss", None)
            continue
        if not bool(discriminant > 0) or not bool(projection > 0):
            results[target_id] = ("unclear", (projection, radius))
            continue
        root = projection - discriminant.sqrt()
        if bool(root > 0):
            results[target_id] = ("hit", root)
        elif bool(root < 0):
            results[target_id] = ("behind", None)
        else:
            results[target_id] = ("unclear", (projection, radius))
    return results


def first_owner(
    results: dict[str, tuple[str, Any]], owner: str,
) -> arb | None:
    status, root = results[owner]
    if status != "hit":
        return None
    for target_id, (other_status, payload) in results.items():
        if target_id == owner or other_status in {"miss", "behind"}:
            continue
        if other_status == "hit" and bool(payload > root):
            continue
        if other_status == "unclear" and bool(payload[0] - payload[1] > root):
            continue
        return None
    return root


def posthit_results(
    rows: dict[str, tuple[arb, arb, arb]],
    tangent_target: str,
    angle: arb,
) -> tuple[dict[str, tuple[str, Any]], dict[str, arb]] | None:
    projection_t, cross_t, radius_t = rows[tangent_target]
    cosine = angle.cos()
    sine = angle.sin()
    projection, cross = rotate_coordinates(projection_t, cross_t, angle)
    discriminant = radius_t * radius_t - cross * cross
    if not (bool(discriminant > 0) and bool(projection > 0)):
        return None
    root_t = projection - discriminant.sqrt()
    normal_a = (root_t * cosine - projection_t) / radius_t
    normal_b = (root_t * sine - cross_t) / radius_t
    incoming_normal = (root_t - projection) / radius_t
    outgoing_a = cosine - 2 * incoming_normal * normal_a
    outgoing_b = sine - 2 * incoming_normal * normal_b
    results: dict[str, tuple[str, Any]] = {}
    for target_id, (center_a, center_b, radius) in rows.items():
        if target_id == tangent_target:
            continue
        dx = center_a - root_t * cosine
        dy = center_b - root_t * sine
        projection_2 = outgoing_a * dx + outgoing_b * dy
        cross_2 = -outgoing_b * dx + outgoing_a * dy
        discriminant_2 = radius * radius - cross_2 * cross_2
        if bool(discriminant_2 < 0) or bool(projection_2 < 0):
            results[target_id] = ("miss", None)
            continue
        if not (bool(discriminant_2 > 0) and bool(projection_2 > 0)):
            results[target_id] = ("unclear", (projection_2, radius))
            continue
        root_2 = projection_2 - discriminant_2.sqrt()
        if bool(root_2 > arbq(Q(1, 10**10))):
            results[target_id] = ("hit", root_2)
        elif bool(root_2 < 0):
            results[target_id] = ("behind", None)
        else:
            results[target_id] = ("skip", None)
    state = {
        "root_t": root_t,
        "cosine": cosine,
        "sine": sine,
        "outgoing_a": outgoing_a,
        "outgoing_b": outgoing_b,
    }
    return results, state


def suffix_cell(
    normal_a: arb, normal_b: arb, ux: arb, uy: arb,
) -> str | None:
    normal_x = normal_a * ux - normal_b * uy
    normal_y = normal_a * uy + normal_b * ux
    if bool(normal_x > abs(normal_y)):
        return "E"
    if bool(normal_x < -abs(normal_y)):
        return "W"
    if bool(normal_y > abs(normal_x)):
        return "N"
    if bool(normal_y < -abs(normal_x)):
        return "S"
    return None


def direct_suffix_state(
    rows: dict[str, tuple[arb, arb, arb]],
    owner: str,
    angle: arb,
    ux: arb,
    uy: arb,
) -> dict[str, Any] | None:
    results = collision_results(rows, angle)
    root = first_owner(results, owner)
    if root is None:
        return None
    center_a, center_b, radius = rows[owner]
    cosine = angle.cos()
    sine = angle.sin()
    projection, cross = rotate_coordinates(center_a, center_b, angle)
    discriminant = radius * radius - cross * cross
    normal_a = (root * cosine - center_a) / radius
    normal_b = (root * sine - center_b) / radius
    cell = suffix_cell(normal_a, normal_b, ux, uy)
    if cell is None:
        return None
    return {
        "root": root,
        "cosine": discriminant.sqrt() / radius,
        "p": cross / radius,
        "cell": cell,
    }


def hit_suffix_state(
    rows: dict[str, tuple[arb, arb, arb]],
    tangent_target: str,
    owner: str,
    angle: arb,
    ux: arb,
    uy: arb,
) -> dict[str, Any] | None:
    replay = posthit_results(rows, tangent_target, angle)
    if replay is None:
        return None
    results, state = replay
    root_2 = first_owner(results, owner)
    if root_2 is None:
        return None
    center_a, center_b, radius = rows[owner]
    contact_a = state["root_t"] * state["cosine"] + root_2 * state["outgoing_a"]
    contact_b = state["root_t"] * state["sine"] + root_2 * state["outgoing_b"]
    normal_a = (contact_a - center_a) / radius
    normal_b = (contact_b - center_b) / radius
    cell = suffix_cell(normal_a, normal_b, ux, uy)
    if cell is None:
        return None
    dx = center_a - state["root_t"] * state["cosine"]
    dy = center_b - state["root_t"] * state["sine"]
    projection = state["outgoing_a"] * dx + state["outgoing_b"] * dy
    cross = -state["outgoing_b"] * dx + state["outgoing_a"] * dy
    discriminant = radius * radius - cross * cross
    return {
        "root_t": state["root_t"],
        "root_after_tangent": root_2,
        "cosine": discriminant.sqrt() / radius,
        "p": cross / radius,
        "cell": cell,
    }


def signed_angle_interval(sign: int) -> arb:
    lower = sign * ANGLE_LOWER
    upper = sign * ANGLE_UPPER
    return bulk.arb_interval(min(lower, upper), max(lower, upper))


def certify_shell(row: dict[str, Any]) -> dict[str, Any]:
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
        geometry = bulk.tangent_geometry(
            box.chart_id, box.z0, box.z1, box.s0, box.s1,
            box.target_id, box.epsilon,
        )
        if geometry is None:
            continue
        _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, s = geometry
        source_id = f"{row['source']}[0,0]"
        direct_rows = centered_candidate_rows(
            qx, qy, ux, uy, s, 0, 0, source_id
        )
        tangent_radius = obstacle_radius(row["target"])
        direct_rows[row["target"]] = (
            ell_t, row["epsilon"] * tangent_radius, tangent_radius
        )
        target = bulk.TARGET_BY_ID[row["target"]]
        post_rows = centered_candidate_rows(
            qx, qy, ux, uy, s, target.ix, target.iy, row["target"]
        )
        post_rows[row["target"]] = direct_rows[row["target"]]

        hit_angle = signed_angle_interval(row["epsilon"])
        miss_angle = signed_angle_interval(-row["epsilon"])
        hit_first = first_owner(
            collision_results(direct_rows, hit_angle), row["target"]
        )
        miss_state = direct_suffix_state(
            direct_rows, row["miss_target"], miss_angle, ux, uy
        )
        hit_state = hit_suffix_state(
            post_rows, row["target"], row["miss_target"], hit_angle, ux, uy
        )
        if hit_first is None or miss_state is None or hit_state is None:
            continue
        if not (
            bool(hit_first < arbq(Q(2)))
            and bool(miss_state["root"] < arbq(Q(2)))
            and bool(hit_state["root_after_tangent"] < arbq(Q(2)))
            and bool(miss_state["cosine"] > arbq(Q(1, 20)))
            and bool(hit_state["cosine"] > arbq(Q(1, 20)))
            and bool(abs(miss_state["p"]) < arbq(Q(999, 1000)))
            and bool(abs(hit_state["p"]) < arbq(Q(999, 1000)))
            and miss_state["cell"] == hit_state["cell"]
        ):
            continue
        suffix_chart = (
            f"{bulk.TARGET_BY_ID[row['miss_target']].obstacle}:"
            f"{miss_state['cell']}"
        )
        shell_payload = {
            "source_box": box.key(),
            "hit_angle": [str(row["epsilon"] * ANGLE_LOWER), str(row["epsilon"] * ANGLE_UPPER)],
            "miss_angle": [str(-row["epsilon"] * ANGLE_LOWER), str(-row["epsilon"] * ANGLE_UPPER)],
            "hit_first_root": str(hit_first),
            "miss_direct_state": {
                key: str(value) if key != "cell" else value
                for key, value in miss_state.items()
            },
            "hit_post_state": {
                key: str(value) if key != "cell" else value
                for key, value in hit_state.items()
            },
        }
        shell_id = "shell:" + canonical_digest({
            "occurrence": row["occurrence_id"],
            "box": box.key(),
            "angle_magnitude": [str(ANGLE_LOWER), str(ANGLE_UPPER)],
        })
        return {
            "shell_id": shell_id,
            "occurrence_id": row["occurrence_id"],
            "source_event_chart": box.chart_id,
            "base_half_width_power": half_width_power,
            "base_half_width": str(half_width),
            "base_event_coordinate_area": str((2 * half_width) ** 2),
            "hit_angle_sign": row["epsilon"],
            "miss_angle_sign": -row["epsilon"],
            "suffix_regular_collision_chart": suffix_chart,
            "hit_first_target": row["target"],
            "hit_second_target": row["miss_target"],
            "miss_first_target": row["miss_target"],
            "two_sides_share_suffix_chart": True,
            "shell_geometry_sha256": canonical_digest(shell_payload),
        }
    raise AssertionError(f"no transverse shell for {row['occurrence_id']}")


def shell_registry() -> dict[str, Any]:
    maximal_rows, maximal_registry = current.load_maximal_rows()
    shells = [certify_shell(row) for row in maximal_rows]
    shells.sort(key=canonical_json)
    assert len(shells) == 64
    assert len({row["shell_id"] for row in shells}) == 64
    power_histogram = Counter(row["base_half_width_power"] for row in shells)
    assert power_histogram == Counter({10: 36, 11: 24, 12: 4})
    suffix_histogram = Counter(
        row["suffix_regular_collision_chart"] for row in shells
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
        Q(row["base_event_coordinate_area"]) for row in shells
    )
    total_two_side_coordinate_volume = (
        total_base_area * 2 * (ANGLE_UPPER - ANGLE_LOWER)
    )
    assert total_base_area == Q(169, 1048576)
    assert total_two_side_coordinate_volume == Q(169, 34359738368)
    return {
        "occurrence_shell_count": len(shells),
        "oriented_transverse_tube_count": 2 * len(shells),
        "angle_magnitude_interval": [str(ANGLE_LOWER), str(ANGLE_UPPER)],
        "hit_angle_sign_equals_tangency_epsilon": True,
        "miss_angle_sign_equals_negative_tangency_epsilon": True,
        "base_half_width_power_histogram": {
            str(key): value for key, value in sorted(power_histogram.items())
        },
        "labelled_base_event_coordinate_area": str(total_base_area),
        "labelled_two_side_coordinate_volume": str(
            total_two_side_coordinate_volume
        ),
        "complete_local_candidate_universe": {
            "obstacles": ["G", "W"],
            "lattice_window_per_leg": "9x9 centered at current collision lift",
            "current_obstacle_excluded": True,
            "candidate_count_after_exclusion": 161,
            "all_certified_owner_flights_strictly_below": "2",
            "window_radius_4_exceeds_required_center_offset": True,
        },
        "all_hit_tubes_first_hit_tangent_target": True,
        "all_hit_tubes_next_hit_fixed_miss_target": True,
        "all_miss_tubes_first_hit_fixed_miss_target": True,
        "all_two_side_successors_regular": True,
        "all_two_side_successors_share_one_suffix_chart_per_occurrence": True,
        "uniform_suffix_bounds": {
            "cosine_strict_lower": "1/20",
            "abs_p_strict_upper": "999/1000",
            "each_owner_flight_strict_upper": "2",
        },
        "suffix_regular_chart_histogram": dict(sorted(suffix_histogram.items())),
        "shell_rows_sha256": canonical_digest(shells),
        "imported_maximal_rows_sha256": maximal_registry[
            "maximal_row_rows_sha256"
        ],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.dyadic-transverse-recovery-shell.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "dyadic_transverse_recovery_shell_registry": shell_registry(),
        "strict_nonpromotion": {
            "phase_angle_shell_is_actual_parameter_DQ_transverse_coordinate": False,
            "one_dyadic_shell_is_uniform_all_scale_shell_family": False,
            "common_suffix_chart_means_identical_hit_miss_state": False,
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
    print("DYADIC_TRANSVERSE_RECOVERY_SHELLS_64: CERTIFIED")
    print("ORIENTED_PHASE_SPACE_TUBES_128: CERTIFIED")
    print("COMMON_REGULAR_SUFFIX_CHARTS_64: CERTIFIED")
    print("PARAMETER_DQ_TRANSVERSE_SHELL_FAMILY: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
