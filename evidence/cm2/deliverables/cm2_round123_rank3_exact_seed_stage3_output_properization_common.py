#!/usr/bin/env python3
"""Round123 exact-seed stage-3 output properization common producer logic.

This is deliberately a non-freezing spike.  It starts from the one exact
Round121 seed and its 24 common-refinement input children, constructs the
actual third collision in the certified north chart, and defines

    U3(x) = a3(0) - a3(x).

It then isolates every canonical output level U3=j*delta, merges those roots
with the 23 already materialized Round121 input cuts, and derives the output
fragment and symbolic mass-partition census without assuming that census in
advance.

This common module does not read or pin Round122 and does not itself install
an F14 slot.  The final Round123 producer adds the frozen bridge and operator
contracts; the retained provisional spike wrapper exposes this build only for
diagnostic replay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as r121


HERE = Path(__file__).resolve().parent
ROUND121 = HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
ROUND121_SHA256 = "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e"
ROUND121_PRODUCER = HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py"
ROUND121_PRODUCER_SHA256 = (
    "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed"
)
SCHEMA = "cm2.round123.stage3-output-properization-spike.v0"
DEFAULT_BITS = 1536
DEFAULT_BISECTIONS = 240


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(Q(value))


def floor_q(value: Q) -> int:
    return value.numerator // value.denominator


def lohi(value: arb) -> tuple[Q, Q]:
    return r121.arb_pair(value)


def interval_strings(value: arb) -> list[str]:
    lower, upper = lohi(value)
    return [qstr(lower), qstr(upper)]


def load_round121() -> dict[str, Any]:
    require(sha256(ROUND121) == ROUND121_SHA256, "Round121 certificate pin")
    require(
        sha256(ROUND121_PRODUCER) == ROUND121_PRODUCER_SHA256,
        "Round121 producer pin",
    )
    document = r121.strict_json(ROUND121)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "Round121 closed envelope",
    )
    require(
        document["schema"]
        == "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
        "Round121 schema",
    )
    require(
        document["result_sha256"] == r121.closed_digest(document["result"]),
        "Round121 result digest",
    )
    return document["result"]


def adapted3(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    x_lower: Q,
    x_upper: Q,
) -> Any:
    state = r121.raw_state(seed, root_bracket, x_lower, x_upper)
    actual = state["actual_third"]
    # The third selected collision chart is N.  In the same convention used
    # by Round121 for its first N-chart image, the adapted coordinate is the
    # outgoing normal angle plus asin(momentum).
    return (
        r121.Jet(arb.pi() / 2)
        - r121.asin_jet(actual["normal_x"])
        + r121.asin_jet(state["actual_third_momentum"])
    )


def u3_value(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    a3_zero: arb,
    x_lower: Q,
    x_upper: Q,
) -> arb:
    return a3_zero - adapted3(seed, root_bracket, x_lower, x_upper).value


def endpoint_id(exact_seed_id: str, level: int) -> str:
    payload = [
        "round123-stage3-output-level-root-v0",
        exact_seed_id,
        "actual-third-chart:N",
        "orientation:U3=a3(0)-a3(x)",
        f"U3={level}*delta",
    ]
    return "round123-stage3-endpoint:" + digest(payload)


def stage3_cell_id(exact_seed_id: str, natural_index: int) -> str:
    payload = [
        "round123-stage3-output-natural-cell-v0",
        exact_seed_id,
        "actual-third-chart:N",
        "orientation:U3=a3(0)-a3(x)",
        natural_index,
    ]
    return "round123-stage3-output-natural-cell:" + digest(payload)


def isolate_stage3_roots(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    exact_seed_id: str,
    a3_zero: arb,
    root_count: int,
    bisections: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for level in range(1, root_count + 1):
        # The already verified
        #
        #   root_count < U3'/delta < root_count + 1
        #
        # gives a narrow exact outer bracket
        # j/(root_count+1) < x_j < j/root_count, with x<1 at the final level.
        low = Q(level, root_count + 1)
        high = min(Q(level, root_count), Q(1))
        target = r121.aq(level * r121.DELTA)
        low_sign = r121.strict_sign(
            u3_value(seed, root_bracket, a3_zero, low, low) - target
        )
        high_sign = r121.strict_sign(
            u3_value(seed, root_bracket, a3_zero, high, high) - target
        )
        require((low_sign, high_sign) == (-1, 1), f"stage3 outer signs: {level}")
        for _ in range(bisections):
            middle = (low + high) / 2
            sign = r121.strict_sign(
                u3_value(seed, root_bracket, a3_zero, middle, middle) - target
            )
            require(sign != 0, f"stage3 bisection sign: {level}")
            if sign < 0:
                low = middle
            else:
                high = middle
        derivative = -adapted3(seed, root_bracket, low, high).gradient[0]
        derivative_lower, derivative_upper = lohi(
            derivative / r121.aq(r121.DELTA)
        )
        require(
            Q(root_count)
            < derivative_lower
            <= derivative_upper
            < Q(root_count + 1),
            f"stage3 root derivative: {level}",
        )
        row = {
            "endpoint_id": endpoint_id(exact_seed_id, level),
            "stage": 3,
            "natural_index_j": level,
            "exact_root_equation_id": f"round123-U3-equals-{level}-delta",
            "exact_root_equation": f"U3(x)={level}*10^-90",
            "actual_third_chart": "N",
            "orientation": "U3(x)=a3(0)-a3(x)",
            "x_dyadic_bracket": [qstr(low), qstr(high)],
            "x_bracket_width": qstr(high - low),
            "left_function_sign": -1,
            "right_function_sign": 1,
            "normalized_derivative_strict_enclosure": [
                qstr(derivative_lower),
                qstr(derivative_upper),
            ],
            "unique_root_certified": True,
            "numeric_bracket_participates_in_ID": False,
            "lower_owner": f"stage-3-natural-cell-{level - 1}",
            "upper_owner": f"stage-3-natural-cell-{level}",
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def boundary_record(
    identifier: str,
    origin: str,
    bracket: tuple[Q, Q],
    stage: int,
    natural_index: int,
    u3_enclosure: tuple[Q, Q] | None,
) -> dict[str, Any]:
    return {
        "endpoint_id": identifier,
        "origin": origin,
        "stage": stage,
        "natural_index_j": natural_index,
        "x_dyadic_bracket": [qstr(bracket[0]), qstr(bracket[1])],
        "u3_over_delta_enclosure": (
            None
            if u3_enclosure is None
            else [qstr(u3_enclosure[0]), qstr(u3_enclosure[1])]
        ),
    }


def merged_boundaries(
    round121: dict[str, Any],
    stage3_rows: list[dict[str, Any]],
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    a3_zero: arb,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in round121["pullback_endpoint_rows"]:
        low, high = map(Q, row["x_dyadic_bracket"])
        u3 = (
            u3_value(seed, root_bracket, a3_zero, low, high)
            / r121.aq(r121.DELTA)
        )
        rows.append(
            boundary_record(
                row["endpoint_id"],
                "ROUND121_EXISTING_INPUT_CUT",
                (low, high),
                row["stage"],
                row["natural_index_j"],
                lohi(u3),
            )
        )
    for row in stage3_rows:
        low, high = map(Q, row["x_dyadic_bracket"])
        level = int(row["natural_index_j"])
        rows.append(
            boundary_record(
                row["endpoint_id"],
                "ROUND123_STAGE3_OUTPUT_CUT",
                (low, high),
                3,
                level,
                (Q(level), Q(level)),
            )
        )
    rows.sort(key=lambda row: Q(row["x_dyadic_bracket"][0]))
    gaps: list[tuple[Q, str, str, str]] = []
    for left, right in zip(rows, rows[1:]):
        gap = Q(right["x_dyadic_bracket"][0]) - Q(
            left["x_dyadic_bracket"][1]
        )
        require(gap > 0, "merged cut overlap or coincidence")
        origins = {left["origin"], right["origin"]}
        if origins == {"ROUND123_STAGE3_OUTPUT_CUT"}:
            kind = "STAGE3_TO_STAGE3"
        elif origins == {"ROUND121_EXISTING_INPUT_CUT"}:
            kind = "EXISTING_TO_EXISTING"
        else:
            kind = "CROSS_ORIGIN"
        gaps.append((gap, kind, left["endpoint_id"], right["endpoint_id"]))
    require(gaps, "merged gap census")
    minimum = min(gaps, key=lambda item: item[0])
    by_kind: dict[str, tuple[Q, str, str]] = {}
    for gap, kind, left_id, right_id in gaps:
        if kind not in by_kind or gap < by_kind[kind][0]:
            by_kind[kind] = (gap, left_id, right_id)
    audit = {
        "combined_internal_cut_count": len(rows),
        "all_cut_brackets_pairwise_strictly_ordered": True,
        "minimum_combined_x_gap": qstr(minimum[0]),
        "minimum_combined_x_gap_kind": minimum[1],
        "minimum_combined_x_gap_pair": [minimum[2], minimum[3]],
        "minimum_x_gap_by_kind": {
            kind: {
                "gap": qstr(value[0]),
                "pair": [value[1], value[2]],
            }
            for kind, value in sorted(by_kind.items())
        },
    }
    return rows, audit


def stage3_natural_cells(
    exact_seed_id: str,
    stage3_rows: list[dict[str, Any]],
    ratio_lower: Q,
    ratio_upper: Q,
) -> list[dict[str, Any]]:
    root_count = len(stage3_rows)
    left_outer = r121.boundary_id("left", exact_seed_id)
    right_outer = r121.boundary_id("right", exact_seed_id)
    endpoint_ids = [
        left_outer,
        *(row["endpoint_id"] for row in stage3_rows),
        right_outer,
    ]
    rows: list[dict[str, Any]] = []
    for natural_index in range(root_count + 1):
        full_delta_cell = natural_index < root_count
        normalized_length = (
            [Q(1), Q(1)]
            if full_delta_cell
            else [
                ratio_lower - root_count,
                ratio_upper - root_count,
            ]
        )
        require(
            Q(0) < normalized_length[0] <= normalized_length[1] <= Q(1),
            "stage3 natural-cell adapted length",
        )
        row = {
            "recut_instance_id": stage3_cell_id(
                exact_seed_id, natural_index
            ),
            "stage": 3,
            "natural_index_j": natural_index,
            "adapted_coordinate_id": "round123-U3-north-chart-output",
            "adapted_lower": f"{natural_index}*delta",
            "adapted_upper": (
                f"{natural_index + 1}*delta"
                if full_delta_cell
                else "U3(1)"
            ),
            "normalized_adapted_length_enclosure": [
                qstr(normalized_length[0]),
                qstr(normalized_length[1]),
            ],
            "lower_endpoint_id": endpoint_ids[natural_index],
            "upper_endpoint_id": endpoint_ids[natural_index + 1],
            "lower_closed": True,
            "upper_closed": False,
            "full_delta_cell": full_delta_cell,
            "terminal_partial_cell": not full_delta_cell,
            "internal_cut_is_owned_by_right_cell": True,
            "source_parent_right_endpoint_remains_open": True,
            "actual_third_owner": "G[-1,-2]",
            "actual_third_collision_chart": "N",
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == root_count + 1, "stage3 natural-cell count")
    return rows


def output_fragments(
    round121: dict[str, Any],
    exact_seed_id: str,
    merged: list[dict[str, Any]],
    stage3_root_count: int,
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    a3_zero: arb,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_outer = r121.boundary_id("left", exact_seed_id)
    right_outer = r121.boundary_id("right", exact_seed_id)
    boundaries = [
        boundary_record(
            left_outer, "SOURCE_OUTER_LEFT", (Q(0), Q(0)), 0, 0, (Q(0), Q(0))
        ),
        *merged,
        boundary_record(
            right_outer, "SOURCE_OUTER_RIGHT", (Q(1), Q(1)), 0, 1, None
        ),
    ]
    children = sorted(
        round121["common_refinement_rows"], key=lambda row: row["common_rank"]
    )
    child_index = {row["common_rank"]: row for row in children}
    input_rank = 0
    stage3_index = 0
    fragments: list[dict[str, Any]] = []
    child_fragments: dict[int, list[dict[str, Any]]] = {
        rank: [] for rank in range(len(children))
    }
    for fragment_rank, (lower, upper) in enumerate(
        zip(boundaries, boundaries[1:])
    ):
        lower_high = Q(lower["x_dyadic_bracket"][1])
        upper_low = Q(upper["x_dyadic_bracket"][0])
        require(lower_high < upper_low, "positive fragment source gap")
        output_length = (
            u3_value(
                seed,
                root_bracket,
                a3_zero,
                upper_low,
                upper_low,
            )
            - u3_value(
                seed,
                root_bracket,
                a3_zero,
                lower_high,
                lower_high,
            )
        ) / r121.aq(r121.DELTA)
        output_length_lower, output_length_upper = lohi(output_length)
        require(
            Q(4, 125)
            < output_length_lower
            <= output_length_upper,
            "uniform stage3 output fragment length",
        )
        child = child_index[input_rank]
        payload = [
            "round123-stage3-output-fragment-v0",
            exact_seed_id,
            child["common_child_id"],
            lower["endpoint_id"],
            upper["endpoint_id"],
            stage3_index,
        ]
        fragment_id = "round123-stage3-output-fragment:" + digest(payload)
        row = {
            "output_fragment_id": fragment_id,
            "fragment_rank": fragment_rank,
            "input_common_child_id": child["common_child_id"],
            "input_common_rank": input_rank,
            "stage3_natural_index_j": stage3_index,
            "stage3_output_recut_instance_id": stage3_cell_id(
                exact_seed_id, stage3_index
            ),
            "source_x_lower_endpoint_id": lower["endpoint_id"],
            "source_x_upper_endpoint_id": upper["endpoint_id"],
            "source_x_open_gap_strict_lower": qstr(upper_low - lower_high),
            "normalized_stage3_output_length_strict_enclosure": [
                qstr(output_length_lower),
                qstr(output_length_upper),
            ],
            "normalized_stage3_output_length_strict_lower_exceeds": "4/125",
            "adapted_output_containment": (
                f"[{stage3_index}*delta,"
                + (
                    f"{stage3_index + 1}*delta)"
                    if stage3_index < stage3_root_count
                    else "U3(1))"
                )
            ),
            "lower_closed": True,
            "upper_closed": False,
            "source_parent_right_endpoint_remains_open": True,
            "internal_stage3_cut_owned_by_right_cell": True,
            "fragment_mass_symbol": f"M_stage3_fragment_{fragment_rank}",
            "fragment_mass_is_nonnegative": True,
            "mass_is_not_sampled_or_assumed_equal": True,
        }
        row["row_sha256"] = digest(row)
        fragments.append(row)
        child_fragments[input_rank].append(row)
        crossed = upper["origin"]
        if crossed == "ROUND121_EXISTING_INPUT_CUT":
            input_rank += 1
        elif crossed == "ROUND123_STAGE3_OUTPUT_CUT":
            stage3_index += 1
    require(input_rank == len(children) - 1, "terminal input rank")
    require(
        stage3_index == stage3_root_count,
        "terminal stage3 natural index",
    )

    partitions: list[dict[str, Any]] = []
    for rank, child in enumerate(children):
        parts = child_fragments[rank]
        require(parts, "nonempty output partition")
        row = {
            "input_common_child_id": child["common_child_id"],
            "input_common_rank": rank,
            "output_fragment_count": len(parts),
            "output_fragment_ids": [
                fragment["output_fragment_id"] for fragment in parts
            ],
            "stage3_natural_index_span": [
                parts[0]["stage3_natural_index_j"],
                parts[-1]["stage3_natural_index_j"],
            ],
            "source_partition_lower_endpoint_id": parts[0][
                "source_x_lower_endpoint_id"
            ],
            "source_partition_upper_endpoint_id": parts[-1][
                "source_x_upper_endpoint_id"
            ],
            "disjoint_half_open_union_equals_input_child": True,
            "symbolic_mass_partition_identity": (
                "M_input_child=sum(output_fragment_masses)"
            ),
            "arbitrary_positive_density_mass_weights_not_preassigned": True,
            "minimum_normalized_stage3_output_length_strict_lower": qstr(
                min(
                    Q(fragment[
                        "normalized_stage3_output_length_strict_enclosure"
                    ][0])
                    for fragment in parts
                )
            ),
            "mass_weighted_inverse_length_assembly": (
                "sum_fragment M_fragment/ell_fragment"
                " < (100/(3*delta))*M_input_child"
            ),
            "fragment_count_does_not_multiply_mass_weighted_bound": True,
        }
        row["row_sha256"] = digest(row)
        partitions.append(row)
    return fragments, partitions


def leg_output_row_id(
    exact_seed_id: str, common_child_id: str, leg_index: int
) -> str:
    payload = [
        "round123-accepted-norm-leg-output-v0",
        exact_seed_id,
        common_child_id,
        leg_index,
    ]
    return "round123-leg-output:" + digest(payload)


def image_member_id(
    exact_seed_id: str, common_child_id: str, output_stage: int
) -> str:
    payload = [
        "round123-existing-common-child-image-member-v0",
        exact_seed_id,
        common_child_id,
        output_stage,
    ]
    return "round123-image-member:" + digest(payload)


def leg_output_rows(
    round121: dict[str, Any],
    exact_seed_id: str,
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    adapted: dict[str, Any],
    fragments: list[dict[str, Any]],
    partitions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    endpoint_brackets = {
        row["endpoint_id"]: tuple(map(Q, row["x_dyadic_bracket"]))
        for row in round121["pullback_endpoint_rows"]
    }
    endpoint_brackets[r121.boundary_id("left", exact_seed_id)] = (Q(0), Q(0))
    endpoint_brackets[r121.boundary_id("right", exact_seed_id)] = (Q(1), Q(1))
    fragments_by_id = {
        row["output_fragment_id"]: row for row in fragments
    }
    partitions_by_rank = {
        row["input_common_rank"]: row for row in partitions
    }
    children = sorted(
        round121["common_refinement_rows"],
        key=lambda row: row["common_rank"],
    )
    require(
        [row["common_rank"] for row in children] == list(range(24)),
        "24 ordered common children",
    )
    rows: list[dict[str, Any]] = []
    for child in children:
        rank = child["common_rank"]
        lower_bracket = endpoint_brackets[
            child["source_x_lower_endpoint_id"]
        ]
        upper_bracket = endpoint_brackets[
            child["source_x_upper_endpoint_id"]
        ]
        lower_inside = lower_bracket[1]
        upper_inside = upper_bracket[0]
        require(lower_inside < upper_inside, "positive common-child core")

        stage_lengths: dict[int, list[list[str]]] = {}
        for output_stage in (1, 2):
            lower_value = r121.u_value(
                seed,
                root_bracket,
                adapted,
                output_stage,
                lower_inside,
            )
            upper_value = r121.u_value(
                seed,
                root_bracket,
                adapted,
                output_stage,
                upper_inside,
            )
            normalized_length = (
                upper_value - lower_value
            ) / r121.aq(r121.DELTA)
            length_lower, length_upper = lohi(normalized_length)
            threshold = Q(3, 100) if output_stage == 1 else Q(17, 200)
            require(
                threshold < length_lower <= length_upper <= Q(1),
                f"stage{output_stage} common-child output length",
            )
            stage_lengths[output_stage] = [
                [qstr(length_lower), qstr(length_upper)]
            ]

        partition = partitions_by_rank[rank]
        stage3_members = [
            fragments_by_id[identifier]
            for identifier in partition["output_fragment_ids"]
        ]
        stage3_lengths = [
            row["normalized_stage3_output_length_strict_enclosure"]
            for row in stage3_members
        ]
        require(
            all(Q(pair[0]) > Q(4, 125) for pair in stage3_lengths),
            "stage3 output-member length lower",
        )

        recut_ids = (
            child["source_recut_instance_id"],
            child["first_image_recut_instance_id"],
            child["second_image_recut_instance_id"],
        )
        for leg_index in range(3):
            output_stage = leg_index + 1
            if output_stage < 3:
                member_ids = [
                    image_member_id(
                        exact_seed_id,
                        child["common_child_id"],
                        output_stage,
                    )
                ]
                length_enclosures = stage_lengths[output_stage]
                threshold = "3/100" if output_stage == 1 else "17/200"
                mass_identity = "M_output_member=M_input_child"
            else:
                member_ids = partition["output_fragment_ids"]
                length_enclosures = stage3_lengths
                threshold = "4/125"
                mass_identity = (
                    "sum_output_fragment_masses=M_input_child"
                )
            row = {
                "leg_output_row_id": leg_output_row_id(
                    exact_seed_id,
                    child["common_child_id"],
                    leg_index,
                ),
                "common_child_id": child["common_child_id"],
                "common_rank": rank,
                "leg_index": leg_index,
                "input_stage": leg_index,
                "output_stage": output_stage,
                "input_materialized_recut_instance_id": recut_ids[leg_index],
                "input_natural_index_j": child[
                    "covering_stage_indices"
                ][leg_index],
                "input_adapted_length_less_or_equal_delta": True,
                "output_member_count": len(member_ids),
                "output_member_ids": member_ids,
                "normalized_output_member_length_strict_enclosures": (
                    length_enclosures
                ),
                "every_output_member_length_strict_lower_exceeds": threshold,
                "output_members_are_half_open": True,
                "conditional_restriction_and_normalization_do_not_increase_Reg": True,
                "zero_mass_output_members_are_omitted": True,
                "mass_partition_identity": mass_identity,
                "arbitrary_positive_normalized_density_scope": True,
            }
            row["row_sha256"] = digest(row)
            rows.append(row)
    require(len(rows) == 72, "72 leg-output rows")
    return rows


def build(bits: int, bisections: int) -> dict[str, Any]:
    require(bits >= 1024, "precision must be at least 1024 bits")
    require(bisections >= 200, "at least 200 bisections required")
    ctx.prec = bits
    values = r121.load_inputs()
    seed = r121.locate_seed(values)
    round121 = load_round121()
    root_low, root_high, _, _ = r121.isolate_anchor_root(seed)
    root_bracket = (root_low, root_high)
    exact_seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    adapted = r121.adapted_data(seed, root_bracket)
    replay = adapted["replay"]
    require(
        tuple(
            row["selected_collision_chart"] for row in replay["leg_audits"]
        )
        == ("N", "S", "N"),
        "three selected collision charts",
    )
    require(
        replay["ordered_regular_relative_interior_owner_ids"][2]
        == "G[-1,-2]",
        "actual third owner",
    )

    a3_zero = adapted3(seed, root_bracket, Q(0), Q(0)).value
    a3_one = adapted3(seed, root_bracket, Q(1), Q(1)).value
    whole = adapted3(seed, root_bracket, Q(0), Q(1))
    ratio = (a3_zero - a3_one) / r121.aq(r121.DELTA)
    derivative_ratio = -whole.gradient[0] / r121.aq(r121.DELTA)
    ratio_lower, ratio_upper = lohi(ratio)
    derivative_lower, derivative_upper = lohi(derivative_ratio)
    require(Q(192) < ratio_lower <= ratio_upper < Q(193), "stage3 length")
    require(
        Q(192) < derivative_lower <= derivative_upper < Q(193),
        "stage3 orientation and derivative",
    )
    root_count = floor_q(ratio_lower)
    require(root_count == floor_q(ratio_upper), "stable stage3 floor")
    require(ratio_upper < root_count + 1, "stage3 upper cell")

    stage3_rows = isolate_stage3_roots(
        seed,
        root_bracket,
        exact_seed_id,
        a3_zero,
        root_count,
        bisections,
    )
    stage3_cells = stage3_natural_cells(
        exact_seed_id,
        stage3_rows,
        ratio_lower,
        ratio_upper,
    )
    merged, spacing = merged_boundaries(
        round121, stage3_rows, seed, root_bracket, a3_zero
    )
    fragments, partitions = output_fragments(
        round121,
        exact_seed_id,
        merged,
        root_count,
        seed,
        root_bracket,
        a3_zero,
    )
    leg_rows = leg_output_rows(
        round121,
        exact_seed_id,
        seed,
        root_bracket,
        adapted,
        fragments,
        partitions,
    )
    fragment_counts = [row["output_fragment_count"] for row in partitions]
    histogram: dict[str, int] = {}
    for count in fragment_counts:
        histogram[str(count)] = histogram.get(str(count), 0) + 1
    global_output_length_lower = min(
        Q(row["normalized_stage3_output_length_strict_enclosure"][0])
        for row in fragments
    )
    require(
        global_output_length_lower > Q(4, 125),
        "global stage3 output length lower",
    )

    result = {
        "status": "SPIKE_ONLY__NOT_FROZEN__NO_F14_SLOT",
        "precision_bits": bits,
        "root_bisections": bisections,
        "strict_scope": (
            "one Round121 exact-b seed; 24 existing input common children; "
            "actual-third north-chart output properization only"
        ),
        "strict_nonclaims": [
            "Round122 is not read or pinned",
            "no F14 slot or Gate5 maturity is installed",
            "no global Borel-b family theorem is claimed",
            "symbolic fragment masses are not replaced by equal sample weights",
        ],
        "stage3_adapted_coordinate_contract": {
            "actual_third_owner": "G[-1,-2]",
            "actual_third_collision_chart": "N",
            "a3": "pi/2-asin(n3_x)+asin(p3)",
            "U3": "a3(0)-a3(x)",
            "orientation": "STRICTLY_INCREASING_U3",
            "normalized_U3_derivative_strict_enclosure": [
                qstr(derivative_lower),
                qstr(derivative_upper),
            ],
            "U3_1_over_delta_strict_enclosure": [
                qstr(ratio_lower),
                qstr(ratio_upper),
            ],
            "simple_length_bound": (
                f"{root_count}<U3(1)/delta<{root_count + 1}"
            ),
        },
        "stage3_endpoint_rows": stage3_rows,
        "stage3_endpoint_rows_sha256": digest(stage3_rows),
        "stage3_natural_cell_rows": stage3_cells,
        "stage3_natural_cell_rows_sha256": digest(stage3_cells),
        "merged_internal_cut_rows": merged,
        "merged_internal_cut_rows_sha256": digest(merged),
        "merged_cut_spacing_audit": spacing,
        "stage3_output_fragment_rows": fragments,
        "stage3_output_fragment_rows_sha256": digest(fragments),
        "input_child_output_partition_rows": partitions,
        "input_child_output_partition_rows_sha256": digest(partitions),
        "accepted_norm_leg_output_rows": leg_rows,
        "accepted_norm_leg_output_rows_sha256": digest(leg_rows),
        "derived_count_ledger": {
            "existing_round121_internal_cut_count": len(
                round121["pullback_endpoint_rows"]
            ),
            "stage3_internal_cut_count": len(stage3_rows),
            "stage3_natural_cell_count": len(stage3_rows) + 1,
            "combined_internal_cut_count": len(merged),
            "output_fragment_count": len(fragments),
            "input_common_child_count": len(partitions),
            "output_fragment_count_per_input_child_min": min(fragment_counts),
            "output_fragment_count_per_input_child_max": max(fragment_counts),
            "output_fragment_count_per_input_child_histogram": histogram,
            "global_minimum_normalized_stage3_output_length_strict_lower": (
                qstr(global_output_length_lower)
            ),
            "stage1_output_member_length_strict_lower": "3/100",
            "stage2_output_member_length_strict_lower": "17/200",
            "stage3_output_fragment_length_strict_lower": "4/125",
            "uniform_all_leg_output_member_length_strict_lower": "3/100",
            "family_mass_weighted_inverse_length_coefficient": (
                "100/(3*delta)"
            ),
            "accepted_norm_leg_output_row_count": len(leg_rows),
            "all_counts_derived_without_expected_output_fragment_literal": True,
        },
        "upstream_and_helper_pins": {
            str(ROUND121.relative_to(HERE.parent)): ROUND121_SHA256,
            str(ROUND121_PRODUCER.relative_to(HERE.parent)): (
                ROUND121_PRODUCER_SHA256
            ),
        },
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=DEFAULT_BITS)
    parser.add_argument("--bisections", type=int, default=DEFAULT_BISECTIONS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    document = build(args.bits, args.bisections)
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
