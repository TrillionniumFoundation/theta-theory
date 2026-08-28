#!/usr/bin/env python3
"""Source-relative first-core stopping on all 128 charged cylinders.

Round 23 certified the displayed entrance words with the regular suffix
collision declared to be time zero.  On the miss side that suffix is one
collision after the source state; on the hit side it is two collisions after
the source state, with the near-grazing target collision in between.

This append-only replay classifies the 64 shared source states and the 64
hit-side near-grazing intermediate states against the complete frozen
24-core union.  It then joins those strict outside-core classifications to
the preceding suffix-relative stopping replay.  Consequently every one of
the 128 labelled positive cylinders has a first-core stopping time measured
from its source collision state.

The independent Arb enclosure used for a hit intermediate state contains the
singular r=0 boundary trace.  Strict outside-core separation on that larger
closed enclosure therefore applies to every regular open-side state r>0; it
does not turn the boundary trace into a regular collision.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate34_all_occurrence_first_core_stopping_cert as parent
import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 2048

DEPENDENCIES = {
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2_gate34_all_occurrence_first_core_stopping_cert.py": (
        "8a22c1a2483822b849562acb06775298a8e9d3a84d753e29ebe86229d35ad1fb"
    ),
    "cm2_gate34_positive_core_hit_charge_cert.py": (
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf"
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_dependencies() -> dict[str, Any]:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
    manifest = json.loads(
        (
            HERE
            / "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
        ).read_text(encoding="utf-8")
    )
    require(
        manifest["result"]["schema"]
        == "cm2.gate34.all-occurrence-first-core-stopping.v1",
        "parent schema",
    )
    registry = manifest["result"][
        "all_occurrence_first_core_stopping_registry"
    ]
    require(registry["first_core_stopping_cylinder_count"] == 128, "parent count")
    require(
        registry["first_core_stopping_clock_origin"]
        == "regular_suffix_state_at_time_0",
        "parent clock",
    )
    require(
        registry["source_to_regular_suffix_collisions_are_not_in_stopping_clock"]
        is True,
        "parent clock boundary",
    )
    return manifest


def strict_core_classification(
    target_id: str,
    normal_x: arb,
    normal_y: arb,
    ux: arb,
    uy: arb,
) -> dict[str, Any]:
    """Fail-closed classification with deterministic separation witnesses."""
    if bool(abs(normal_x) > abs(normal_y)):
        t = normal_y
        if bool(normal_x > 0):
            cell = "E"
            chart_witness = "abs(nx)>abs(ny);nx>0"
        else:
            require(bool(normal_x < 0), "dominant x sign unresolved")
            cell = "W"
            chart_witness = "abs(nx)>abs(ny);nx<0"
    else:
        require(bool(abs(normal_y) > abs(normal_x)), "chart seam unresolved")
        t = normal_x
        if bool(normal_y > 0):
            cell = "N"
            chart_witness = "abs(ny)>abs(nx);ny>0"
        else:
            require(bool(normal_y < 0), "dominant y sign unresolved")
            cell = "S"
            chart_witness = "abs(ny)>abs(nx);ny<0"
    p = -ux * normal_y + uy * normal_x
    chart_id = f"{target_id[0]}:{cell}"
    chart_cores = [
        core for core in parent.core_cert.physical_cores()
        if core.chart_id == chart_id
    ]
    require(len(chart_cores) == 3, f"core chart cardinality: {chart_id}")

    inside: list[str] = []
    separators: list[dict[str, str]] = []
    for core in chart_cores:
        identifier = parent.core_id(core)
        interior = (
            bool(t > charge.arbq(core.t0))
            and bool(t < charge.arbq(core.t1))
            and bool(p > charge.arbq(core.p0))
            and bool(p < charge.arbq(core.p1))
        )
        if interior:
            inside.append(identifier)
            continue
        ordered_tests = (
            ("t<t0", bool(t < charge.arbq(core.t0))),
            ("t>t1", bool(t > charge.arbq(core.t1))),
            ("p<p0", bool(p < charge.arbq(core.p0))),
            ("p>p1", bool(p > charge.arbq(core.p1))),
        )
        witness = next((name for name, truth in ordered_tests if truth), None)
        require(witness is not None, f"core boundary unresolved: {identifier}")
        separators.append({"core_id": identifier, "first_separator": witness})
    require(len(inside) <= 1, "multiple core interiors")
    payload = {
        "target_id": target_id,
        "chart_id": chart_id,
        "chart_witness": chart_witness,
        "t": str(t),
        "p": str(p),
        "inside": inside,
        "separators": separators,
    }
    if inside:
        require(len(separators) == 2, "inside separator count")
        status = "strict_inside_one_core"
        core_identifier: str | None = inside[0]
    else:
        require(len(separators) == 3, "outside separator count")
        status = "strict_outside_all_24_cores"
        core_identifier = None
    return {
        "status": status,
        "core_id": core_identifier,
        "chart_id": chart_id,
        "classification_witness_sha256": canonical_digest(payload),
    }


def source_state_row(
    row: dict[str, Any], specification: dict[str, Any]
) -> dict[str, Any]:
    radius = Q(1, 2 ** specification["radius_power"])
    charge.BASE_HALF_WIDTH = radius
    charge.PARAMETER_RADIUS = radius
    charge.SQRT_DISCRIMINANT_UPPER = Q(
        1, 2 ** ((specification["radius_power"] - 2) // 2)
    )
    nx, ny, _qx, _qy, ux, uy, _ell, _cp, _p, _s = charge.source_geometry(row)
    classification = strict_core_classification(
        f"{row['source']}[0,0]", nx, ny, ux, uy
    )
    require(
        classification["status"] == "strict_outside_all_24_cores",
        f"source core state: {row['occurrence_id']}",
    )
    payload = {
        "occurrence_id": row["occurrence_id"],
        "source_chart": specification["source_chart"],
        "z": specification["z"],
        "radius_power": specification["radius_power"],
        "classification": classification,
    }
    return {
        "source_state_classification_id": "source-state:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "source_target_id": f"{row['source']}[0,0]",
        "source_chart": classification["chart_id"],
        "classification_status": classification["status"],
        "classification_witness_sha256": classification[
            "classification_witness_sha256"
        ],
        "same_collision_coordinates_on_hit_and_miss_sides": True,
        "source_state_time_from_source": 0,
    }


def hit_intermediate_state_row(
    row: dict[str, Any],
    specification: dict[str, Any],
    source_owner_audit_id: str,
) -> dict[str, Any]:
    radius = Q(1, 2 ** specification["radius_power"])
    charge.BASE_HALF_WIDTH = radius
    charge.PARAMETER_RADIUS = radius
    charge.SQRT_DISCRIMINANT_UPPER = Q(
        1, 2 ** ((specification["radius_power"] - 2) // 2)
    )
    _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, _s = charge.source_geometry(row)
    magnitude = charge.interval(Q(0), radius)
    polarity = row["parameter_coarea_polarity"]
    displacement = polarity * magnitude
    qx, qy = charge.shifted_source_point(row["source"], qx, qy, displacement)
    eta = int(row["target"][0] == "W") - int(row["source"] == "W")
    target_radius = bulk.ARB_RADIUS[row["target"][0]]
    projection = ell_t + eta * ux * displacement
    cross = row["epsilon"] * target_radius - eta * uy * displacement
    transversality = polarity * row["epsilon"] * eta * uy
    require(bool(transversality > 0), "hit transversality")
    factor = 2 * target_radius * transversality - uy * uy * magnitude
    require(bool(factor > 0), "hit discriminant factor")
    require(
        charge.SQRT_DISCRIMINANT_UPPER**2 > 2 * radius,
        "hit radical enclosure",
    )
    radical = charge.interval(Q(0), charge.SQRT_DISCRIMINANT_UPPER)
    root = projection - radical
    require(bool(root > 0), "hit root positivity")

    normal_x = (-radical * ux + cross * uy) / target_radius
    normal_y = (-radical * uy - cross * ux) / target_radius
    discriminant = radical * radical
    outgoing_x = (
        (1 - 2 * discriminant / (target_radius * target_radius)) * ux
        + 2 * radical * cross / (target_radius * target_radius) * uy
    )
    outgoing_y = (
        (1 - 2 * discriminant / (target_radius * target_radius)) * uy
        - 2 * radical * cross / (target_radius * target_radius) * ux
    )
    speed = outgoing_x * outgoing_x + outgoing_y * outgoing_y
    require(bool(speed > charge.arbq(Q(999999, 1000000))), "hit speed lower")
    require(bool(speed < charge.arbq(Q(1000001, 1000000))), "hit speed upper")
    classification = strict_core_classification(
        row["target"], normal_x, normal_y, outgoing_x, outgoing_y
    )
    require(
        classification["status"] == "strict_outside_all_24_cores",
        f"hit intermediate core state: {row['occurrence_id']}",
    )
    payload = {
        "occurrence_id": row["occurrence_id"],
        "source_owner_audit_id": source_owner_audit_id,
        "target": row["target"],
        "radius_power": specification["radius_power"],
        "classification": classification,
    }
    return {
        "hit_intermediate_classification_id": (
            "hit-intermediate:" + canonical_digest(payload)
        ),
        "occurrence_id": row["occurrence_id"],
        "source_owner_audit_id": source_owner_audit_id,
        "hit_target_id": row["target"],
        "hit_target_is_global_first_collision": True,
        "hit_intermediate_time_from_source": 1,
        "classification_status": classification["status"],
        "classification_chart": classification["chart_id"],
        "classification_witness_sha256": classification[
            "classification_witness_sha256"
        ],
        "parameter_magnitude_interval": ["0_open", str(radius)],
        "closed_outer_enclosure_includes_singular_r0_boundary": True,
        "regularity_claim_is_only_for_open_positive_side": True,
    }


def source_relative_registry() -> dict[str, Any]:
    parent_manifest = load_dependencies()
    ctx.prec = PRECISION_BITS
    parent.all_charge.refresh_arb_constants()
    require(ctx.prec == PRECISION_BITS, "precision")

    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    specifications = parent.occurrence_specifications(maximal_rows)
    require(len(by_id) == len(specifications) == 64, "occurrence set")
    require(set(by_id) == set(specifications), "occurrence identity")

    source_rows: list[dict[str, Any]] = []
    hit_rows: list[dict[str, Any]] = []
    branch_rows: list[dict[str, Any]] = []
    mapping_rows: list[dict[str, Any]] = []
    for occurrence_id, specification in sorted(specifications.items()):
        row = dict(by_id[occurrence_id])
        row["witness"] = dict(row["witness"])
        row["witness"]["chart_id"] = specification["source_chart"]
        row["witness"]["z"] = specification["z"]
        owner = parent.physical_row_and_owner_audit(row, specification)
        source_row = source_state_row(row, specification)
        hit_row = hit_intermediate_state_row(
            row, specification, owner["source_owner_audit_id"]
        )
        source_rows.append(source_row)
        hit_rows.append(hit_row)

        for side in ("hit", "miss"):
            suffix_branch = parent.replay_first_stopping_branch(
                row,
                specification,
                side,
                owner["source_owner_audit_id"],
            )
            offset = suffix_branch["source_collision_count_to_regular_suffix"]
            require(offset == (2 if side == "hit" else 1), "side offset")
            suffix_time = suffix_branch[
                "first_core_stopping_time_from_regular_suffix"
            ]
            source_time = suffix_time + offset
            preterminal = (
                suffix_branch["strict_outside_core_state_count_before_stop"]
                + offset
            )
            payload = {
                "parent_first_stopping_branch_id": suffix_branch[
                    "first_stopping_branch_id"
                ],
                "source_state_classification_id": source_row[
                    "source_state_classification_id"
                ],
                "hit_intermediate_classification_id": (
                    hit_row["hit_intermediate_classification_id"]
                    if side == "hit"
                    else None
                ),
                "source_relative_first_core_time": source_time,
                "destination_core_id": suffix_branch["destination_core_id"],
            }
            branch = {
                "source_relative_first_stopping_branch_id": (
                    "source-first-core:" + canonical_digest(payload)
                ),
                "occurrence_id": occurrence_id,
                "side": side,
                "parent_first_stopping_branch_id": suffix_branch[
                    "first_stopping_branch_id"
                ],
                "source_owner_audit_id": owner["source_owner_audit_id"],
                "source_state_classification_id": source_row[
                    "source_state_classification_id"
                ],
                "hit_intermediate_classification_id": (
                    hit_row["hit_intermediate_classification_id"]
                    if side == "hit"
                    else None
                ),
                "source_to_regular_suffix_collision_offset": offset,
                "suffix_relative_first_core_time": suffix_time,
                "source_relative_first_core_time": source_time,
                "strict_preterminal_outside_all_24_core_state_count": preterminal,
                "destination_core_id": suffix_branch["destination_core_id"],
                "destination_chart": suffix_branch["destination_chart"],
                "every_state_before_source_relative_stop_is_strictly_outside": True,
                "terminal_state_is_strictly_inside_unique_destination_core": True,
            }
            branch_rows.append(branch)
            mapping_rows.append(
                {
                    "occurrence_id": occurrence_id,
                    "side": side,
                    "source_relative_first_core_time": source_time,
                    "destination_core_id": suffix_branch["destination_core_id"],
                }
            )

    source_rows.sort(key=canonical_json)
    hit_rows.sort(key=canonical_json)
    branch_rows.sort(key=canonical_json)
    mapping_rows.sort(key=canonical_json)
    require(len(source_rows) == 64, "source row count")
    require(len(hit_rows) == 64, "hit row count")
    require(len(branch_rows) == 128, "branch row count")
    require(
        len({row["source_state_classification_id"] for row in source_rows}) == 64,
        "source row identity",
    )
    require(
        len({row["hit_intermediate_classification_id"] for row in hit_rows}) == 64,
        "hit row identity",
    )
    require(
        len(
            {
                row["source_relative_first_stopping_branch_id"]
                for row in branch_rows
            }
        )
        == 128,
        "branch identity",
    )
    require(
        {(row["occurrence_id"], row["side"]) for row in branch_rows}
        == {(occurrence_id, side) for occurrence_id in by_id for side in ("hit", "miss")},
        "oriented branch set",
    )

    histogram = Counter(
        row["source_relative_first_core_time"] for row in branch_rows
    )
    expected_histogram = {
        "3": 22,
        "4": 32,
        "5": 18,
        "6": 8,
        "8": 8,
        "9": 12,
        "10": 8,
        "11": 4,
        "17": 2,
        "18": 2,
        "20": 4,
        "21": 6,
        "22": 2,
    }
    require(
        {str(key): value for key, value in sorted(histogram.items())}
        == expected_histogram,
        "source clock histogram",
    )
    preterminal_count = sum(
        row["strict_preterminal_outside_all_24_core_state_count"]
        for row in branch_rows
    )
    require(preterminal_count == 948, "preterminal state count")
    destination_ids = {row["destination_core_id"] for row in branch_rows}
    require(len(destination_ids) == 14, "destination core count")
    parent_registry = parent_manifest["result"][
        "all_occurrence_first_core_stopping_registry"
    ]
    return {
        "maximal_reference_occurrence_count": 64,
        "charged_oriented_cylinder_count": 128,
        "shared_source_state_classification_count": 64,
        "source_state_branch_reference_count": 128,
        "hit_pre_suffix_intermediate_state_classification_count": 64,
        "unique_pre_suffix_classification_row_count": 128,
        "all_64_source_states_strictly_outside_all_24_cores": True,
        "all_64_hit_intermediate_states_strictly_outside_all_24_cores": True,
        "all_hit_intermediate_targets_retain_global_first_owner_audit": True,
        "hit_intermediate_closed_enclosure_contains_r0_boundary_trace": True,
        "hit_intermediate_regularity_claim_restricted_to_r_greater_than_0": True,
        "first_core_stopping_clock_origin": "source_collision_state_at_time_0",
        "source_to_regular_suffix_collisions_are_in_stopping_clock": True,
        "hit_source_to_regular_suffix_collision_offset": 2,
        "miss_source_to_regular_suffix_collision_offset": 1,
        "source_relative_first_core_stopping_cylinder_count": 128,
        "source_relative_first_core_time_histogram_by_oriented_cylinder": (
            expected_histogram
        ),
        "maximum_source_relative_first_core_time": 22,
        "strict_preterminal_outside_all_24_core_state_count": preterminal_count,
        "strict_terminal_inside_one_core_state_count": 128,
        "total_source_relative_state_classification_count": preterminal_count + 128,
        "ambiguous_core_classification_count": 0,
        "distinct_destination_core_count": len(destination_ids),
        "all_128_labelled_positive_cylinders_have_source_relative_first_core_stops": True,
        "source_state_rows_sha256": canonical_digest(source_rows),
        "hit_intermediate_state_rows_sha256": canonical_digest(hit_rows),
        "source_relative_branch_rows_sha256": canonical_digest(branch_rows),
        "branch_key_to_source_relative_time_and_core_sha256": canonical_digest(
            mapping_rows
        ),
        "parent_suffix_relative_branch_rows_sha256": parent_registry[
            "first_stopping_branch_rows_sha256"
        ],
        "destination_core_ids_sha256": canonical_digest(sorted(destination_ids)),
        "first_source_relative_branch_id": branch_rows[0][
            "source_relative_first_stopping_branch_id"
        ],
        "last_source_relative_branch_id": branch_rows[-1][
            "source_relative_first_stopping_branch_id"
        ],
    }


def build_result() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": "cm2.gate34.source-relative-first-core-stopping.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "floating_search_role": "none_new_exact_Arb_replay",
            "admission_engine": "python-flint Arb",
            "precision_bits": PRECISION_BITS,
            "classification_policy": "strict_trichotomy_fail_closed",
        },
        "source_relative_first_core_stopping_registry": source_relative_registry(),
        "strict_nonpromotion": {
            "positive_cylinders_cover_entire_maximal_rows": False,
            "positive_cylinders_cover_whole_all_scale_germs": False,
            "labelled_coordinate_volume_is_collision_SRB_fraction": False,
            "singular_r0_boundary_is_a_regular_collision": False,
            "full_physical_source_core_first_return_partition": "NOT_CERTIFIED",
            "quantitative_collision_SRB_cemetery_tail": "NOT_CERTIFIED",
            "post_core_induced_return_operator": "NOT_CERTIFIED",
            "common_two_view_strong_restriction": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("SOURCE_RELATIVE_FIRST_CORE_STOPPING_CYLINDERS_128: CERTIFIED")
    print("SOURCE_STATES_OUTSIDE_CORE_64: CERTIFIED")
    print("HIT_PRE_SUFFIX_STATES_OUTSIDE_CORE_64: CERTIFIED")
    print("MAXIMUM_SOURCE_RELATIVE_FIRST_CORE_TIME_22: CERTIFIED")
    print("FULL_PHYSICAL_FIRST_RETURN_PARTITION: NOT_CERTIFIED")
    print("COLLISION_SRB_CEMETERY_TAIL: NOT_CERTIFIED")
    print("INDUCED_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
