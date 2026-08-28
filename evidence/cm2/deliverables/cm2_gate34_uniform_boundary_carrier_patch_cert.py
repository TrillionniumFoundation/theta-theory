#!/usr/bin/env python3
"""Uniform positive-width event patches for all 64 recovery carriers."""

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
import cm2_gate34_occurrence_boundary_recovery_carrier_cert as carrier


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
HALF_WIDTH = Q(1, 1024)

DEPENDENCIES = {
    "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json": (
        "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5"
    ),
    "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py": (
        "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a"
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
        (HERE / next(iter(DEPENDENCIES))).read_text(encoding="utf-8")
    )
    assert manifest["verdict"]["boundary_recovery_carriers_64"] == "CERTIFIED"
    assert manifest["verdict"]["transported_occurrence_to_24_core_incidence"] == (
        "NOT_CERTIFIED"
    )


def suffix_cell(nx: arb, ny: arb) -> str | None:
    if bool(nx > abs(ny)):
        return "E"
    if bool(nx < -abs(ny)):
        return "W"
    if bool(ny > abs(nx)):
        return "N"
    if bool(ny < -abs(nx)):
        return "S"
    return None


def certify_patch(
    row: dict[str, Any], carrier_row: dict[str, Any],
) -> dict[str, Any]:
    z = Q(row["witness"]["z"])
    box = bulk.Box(
        row["witness"]["chart_id"], row["target"], row["epsilon"],
        z - HALF_WIDTH, z + HALF_WIDTH,
        -HALF_WIDTH, HALF_WIDTH, 10,
    )
    assert bulk.Z_LOWER < box.z0 < box.z1 < bulk.Z_UPPER
    assert bulk.S_LOWER < box.s0 < box.s1 < bulk.S_UPPER
    kind, data = endpoint.classify_box(box)
    assert kind == "physical_immutable_subrow"
    assert data is not None
    assert data["miss_target"] == row["miss_target"]
    assert data["polarity"] == row["parameter_coarea_polarity"]

    geometry = bulk.tangent_geometry(
        box.chart_id, box.z0, box.z1, box.s0, box.s1,
        box.target_id, box.epsilon,
    )
    assert geometry is not None
    _nx, _ny, qx, qy, ux, uy, ell_t, cp, p_source, s = geometry
    assert bool(cp > arbq(Q(1, 10)))

    competitors = bulk.competitor_rows(
        qx, qy, ux, uy, s, row["target"],
        bulk.GLOBAL_CANDIDATE_IDS[row["source"]],
    )
    ell_m, delta_m, cross_m = competitors[row["miss_target"]]
    assert bool(delta_m > 0)
    miss = bulk.TARGET_BY_ID[row["miss_target"]]
    miss_radius = bulk.ARB_RADIUS[miss.obstacle]
    radical_m = delta_m.sqrt()
    root_m = ell_m - radical_m
    gap = root_m - ell_t
    p_miss = cross_m / miss_radius
    cosine_miss = radical_m / miss_radius
    assert bool(gap > arbq(Q(1, 5)))
    assert bool(root_m < arbq(Q(2)))
    assert bool(abs(p_miss) < arbq(Q(199, 200)))
    assert bool(cosine_miss > arbq(Q(1, 10)))

    miss_x, miss_y = bulk.cached_target_center(row["miss_target"], s)
    contact_x = qx + root_m * ux
    contact_y = qy + root_m * uy
    normal_x = (contact_x - miss_x) / miss_radius
    normal_y = (contact_y - miss_y) / miss_radius
    cell = suffix_cell(normal_x, normal_y)
    assert cell is not None
    p_out = p_miss
    outgoing_cosine = cosine_miss
    assert bool(outgoing_cosine > arbq(Q(1, 10)))
    assert bool(abs(p_out) < arbq(Q(199, 200)))
    chart_coordinate = normal_y if cell in {"E", "W"} else normal_x
    suffix_chart = f"{miss.obstacle}:{cell}"
    patch_payload = {
        "source_box": box.key(),
        "suffix_chart": suffix_chart,
        "suffix_chart_coordinate": str(chart_coordinate),
        "suffix_p": str(p_out),
        "miss_flight": str(root_m),
        "post_tangent_gap": str(gap),
        "miss_cosine": str(cosine_miss),
    }
    patch_id = "patch:" + canonical_digest({
        "carrier": carrier_row["common_boundary_recovery_carrier_id"],
        "source_box": box.key(),
    })
    return {
        "patch_id": patch_id,
        "occurrence_id": row["occurrence_id"],
        "boundary_recovery_carrier_id": carrier_row[
            "common_boundary_recovery_carrier_id"
        ],
        "source_event_chart": box.chart_id,
        "suffix_regular_collision_chart": suffix_chart,
        "source_box_half_width_z_and_s": str(HALF_WIDTH),
        "source_box_area_in_z_times_s": str((2 * HALF_WIDTH) ** 2),
        "immutable_physical_label_on_full_box": True,
        "common_miss_collision_regular_on_full_box": True,
        "patch_geometry_sha256": canonical_digest(patch_payload),
    }


def patch_registry() -> dict[str, Any]:
    maximal_rows, maximal_registry = current.load_maximal_rows()
    carrier_rows, carrier_registry = carrier.build_carrier_registry()
    carriers_by_occurrence = {
        row["occurrence_id"]: row for row in carrier_rows
    }
    patches = [
        certify_patch(row, carriers_by_occurrence[row["occurrence_id"]])
        for row in maximal_rows
    ]
    patches.sort(key=canonical_json)
    assert len(patches) == 64
    assert len({row["patch_id"] for row in patches}) == 64
    assert len({row["boundary_recovery_carrier_id"] for row in patches}) == 64
    source_histogram = Counter(row["source_event_chart"] for row in patches)
    suffix_histogram = Counter(
        row["suffix_regular_collision_chart"] for row in patches
    )
    expected_suffix = Counter({
        "G:N": 12,
        "G:S": 12,
        "G:E": 10,
        "G:W": 10,
        "W:N": 6,
        "W:S": 6,
        "W:E": 4,
        "W:W": 4,
    })
    assert suffix_histogram == expected_suffix
    patch_area = (2 * HALF_WIDTH) ** 2
    labelled_total_area = len(patches) * patch_area
    assert patch_area == Q(1, 262144)
    assert labelled_total_area == Q(1, 4096)
    return {
        "uniform_positive_width_patch_count": len(patches),
        "patch_half_width_in_both_z_and_s": str(HALF_WIDTH),
        "per_patch_event_coordinate_area": str(patch_area),
        "labelled_occurrence_sheet_coproduct_area": str(labelled_total_area),
        "all_patches_strictly_inside_parameter_and_chart_windows": True,
        "all_patches_have_one_immutable_physical_label": True,
        "all_patches_map_to_one_regular_suffix_collision_chart": True,
        "all_64_boundary_carriers_receive_one_patch": True,
        "uniform_patch_bounds": {
            "source_cosine_strict_lower": "1/10",
            "source_abs_p_strict_upper": "199/200",
            "post_tangent_flight_gap_strict_lower": "1/5",
            "common_miss_flight_strict_upper": "2",
            "common_miss_abs_p_strict_upper": "199/200",
            "common_miss_cosine_strict_lower": "1/10",
        },
        "source_event_chart_histogram": dict(sorted(source_histogram.items())),
        "suffix_regular_chart_histogram": dict(sorted(suffix_histogram.items())),
        "patch_rows_sha256": canonical_digest(patches),
        "imported_carrier_rows_sha256": carrier_registry["carrier_rows_sha256"],
        "imported_maximal_rows_sha256": maximal_registry[
            "maximal_row_rows_sha256"
        ],
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.uniform-boundary-carrier-patch.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
        },
        "uniform_boundary_carrier_patch_registry": patch_registry(),
        "strict_nonpromotion": {
            "event_sheet_patch_is_two_sided_transverse_shell": False,
            "labelled_event_coordinate_area_is_collision_SRB_mass": False,
            "regular_suffix_chart_is_24_core_destination": False,
            "two_sided_open_shell_transport": "NOT_CERTIFIED",
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
    print("UNIFORM_BOUNDARY_CARRIER_PATCHES_64: CERTIFIED")
    print("REGULAR_SUFFIX_COLLISION_CHARTS_64: CERTIFIED")
    print("TWO_SIDED_OPEN_SHELL_TRANSPORT: NOT_CERTIFIED")
    print("FIRST_24_CORE_DESTINATION: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
