#!/usr/bin/env python3
"""Independent verifier for the Round123 stage-3/F14 frontier skeleton.

This verifier never imports either Round123 producer.  At 2048-bit precision
it uses the already independent Round121 geometry implementation to rebuild
the actual third collision, checks the north-chart orientation, verifies all
192 level roots, and reconstructs the 23+192 cut merge, 193 output natural
cells, 216 output fragments, 24 mass partitions, and 120 fail-closed F14
full-key frontier rows.

The verifier deliberately does not install F14.  The final Round122 bridge is
not pinned by the certificate, so a passing result certifies only the stage-3
properization and the fail-closed frontier structure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier as v121


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round123-rank3-stage3-output-properization-f14-frontier-2026-07-23.json"
)
DEFAULT_OUTPUT = (
    HERE
    / "cm2-round123-rank3-stage3-output-properization-f14-frontier-verification-2026-07-23.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round123.rank3-stage3-output-properization-f14-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round123.rank3-stage3-output-properization-f14-frontier-verification.v1"
)
VERIFIER_BITS = 2048

ROUND121 = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND121_SHA256 = (
    "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e"
)
ROUND121_PRODUCER_SHA256 = (
    "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed"
)
ROUND121_VERIFIER_SHA256 = (
    "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95"
)

Q_REGULARITY = Q(93, 100)
THETA_INVERSE = Q(144000, 180337)
DISTORTION_CJ = 15000000000000000000000000
REGULAR_DENSITY_CONE_K = 500000000000000000000000000
DISTORTION_ONLY_FRONTIER_CONSTANT = 13950000000000000000000001
F14_ONE_STEP_FRONTIER_VALUE = 34
F14_THREE_LEG_FRONTIER_PRODUCT = 39304

RESULT_KEYS = {
    "F14_frontier_slot_count",
    "F14_installation_gate",
    "F14_installed_slot_count",
    "candidate_maturity_after_future_R122_and_F14",
    "accepted_norm_leg_output_rows",
    "accepted_norm_leg_output_rows_sha256",
    "cm2_verdict",
    "complete_18_field_block_count",
    "derived_count_ledger",
    "gate5_F14_frontier_slot_rows",
    "gate5_F14_frontier_slot_rows_sha256",
    "gate5_actual_child_field_status",
    "gate5_global_maturity",
    "input_child_output_partition_rows",
    "input_child_output_partition_rows_sha256",
    "merged_cut_spacing_audit",
    "merged_internal_cut_rows",
    "merged_internal_cut_rows_sha256",
    "precision_bits",
    "rank3_seed_child_field_maturity",
    "regular_density_frontier_theorem",
    "root_bisections",
    "stage3_adapted_coordinate_contract",
    "stage3_endpoint_rows",
    "stage3_endpoint_rows_sha256",
    "stage3_natural_cell_rows",
    "stage3_natural_cell_rows_sha256",
    "stage3_output_fragment_rows",
    "stage3_output_fragment_rows_sha256",
    "status",
    "strict_nonclaims",
    "strict_scope",
    "upstream_and_helper_pins",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qvalue(value: Any, label: str) -> Q:
    return v121.qvalue(value, label)


def qstr(value: Q) -> str:
    return str(Q(value))


def row_digest(row: dict[str, Any]) -> str:
    return digest({key: value for key, value in row.items() if key != "row_sha256"})


def interval_pair(value: arb) -> tuple[Q, Q]:
    return v121.arb_pair(value)


def stored_contains(stored: Any, fresh: arb, label: str) -> None:
    v121.interval_encloses_cross_precision(stored, fresh, label)


def source_boundary_id(which: str, seed_id: str) -> str:
    require(which in {"left", "right"}, "source boundary side")
    return f"round121-source-{which}-endpoint:" + digest(
        ["round121-source-boundary-v1", seed_id, which]
    )


def endpoint_id(seed_id: str, level: int) -> str:
    payload = [
        "round123-stage3-output-level-root-v0",
        seed_id,
        "actual-third-chart:N",
        "orientation:U3=a3(0)-a3(x)",
        f"U3={level}*delta",
    ]
    return "round123-stage3-endpoint:" + digest(payload)


def stage3_cell_id(seed_id: str, natural_index: int) -> str:
    payload = [
        "round123-stage3-output-natural-cell-v0",
        seed_id,
        "actual-third-chart:N",
        "orientation:U3=a3(0)-a3(x)",
        natural_index,
    ]
    return "round123-stage3-output-natural-cell:" + digest(payload)


def f14_slot_id(immutable_key: list[Any]) -> str:
    return "round123-gate5-f14-frontier-slot:" + digest(
        ["round123-gate5-f14-frontier-slot-v1", immutable_key]
    )


def load_round121() -> dict[str, Any]:
    require(sha256(ROUND121) == ROUND121_SHA256, "Round121 certificate pin")
    require(
        sha256(HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py")
        == ROUND121_PRODUCER_SHA256,
        "Round121 producer pin",
    )
    require(
        sha256(
            HERE
            / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py"
        )
        == ROUND121_VERIFIER_SHA256,
        "Round121 independent verifier pin",
    )
    document = v121.strict_json(ROUND121.read_text(encoding="utf-8"))
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "Round121 envelope",
    )
    require(
        document["schema"]
        == "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
        "Round121 schema",
    )
    require(
        document["result_sha256"] == digest(document["result"]),
        "Round121 result digest",
    )
    return document["result"]


def a3(theta_star: arb, x: arb, differentiated: bool) -> v121.Dual:
    state = v121.source_and_collisions(theta_star, x, differentiated)
    actual = state["actual_third"]
    return (
        v121.Dual(arb.pi() / 2)
        - actual[4].asin()
        + actual[6].asin()
    )


def u3_value(theta_star: arb, a3_zero: arb, lower: Q, upper: Q) -> arb:
    return a3_zero - a3(
        theta_star, v121.interval(lower, upper), False
    ).value


def image_u_value(
    geometry: dict[str, Any], stage: int, lower: Q, upper: Q
) -> arb:
    require(stage in {1, 2}, "image adapted stage")
    state = v121.source_and_collisions(
        geometry["theta_star"],
        v121.interval(lower, upper),
        False,
    )
    if stage == 1:
        return geometry["u1_zero"] - state["a1"].value
    return state["a2"].value - geometry["u2_zero"]


def independent_geometry() -> dict[str, Any]:
    values = v121.load_inputs()
    indexes = v121.seed_indexes(values)
    anchor = v121.isolate_anchor(indexes)
    theta_star = anchor["theta_ball"]
    a3_zero = a3(theta_star, arb(0), False).value
    a3_one = a3(theta_star, arb(1), False).value
    whole = a3(theta_star, v121.interval(Q(0), Q(1)), True)
    delta = v121.aq(v121.DELTA)
    ratio = (a3_zero - a3_one) / delta
    derivative_ratio = -whole.derivative / delta
    ratio_lower, ratio_upper = interval_pair(ratio)
    derivative_lower, derivative_upper = interval_pair(derivative_ratio)
    zero_state = v121.source_and_collisions(theta_star, arb(0), False)
    require(
        Q(192) < ratio_lower <= ratio_upper < Q(193),
        "independent stage3 length",
    )
    require(
        Q(192)
        < derivative_lower
        <= derivative_upper
        < Q(193),
        "independent stage3 orientation",
    )
    return {
        "theta_star": theta_star,
        "a3_zero": a3_zero,
        "ratio": ratio,
        "derivative_ratio": derivative_ratio,
        "ratio_pair": (ratio_lower, ratio_upper),
        "derivative_pair": (derivative_lower, derivative_upper),
        "u1_zero": zero_state["a1"].value,
        "u2_zero": zero_state["a2"].value,
    }


def verify_coordinate_contract(
    result: dict[str, Any], geometry: dict[str, Any]
) -> None:
    contract = result["stage3_adapted_coordinate_contract"]
    require(
        set(contract)
        == {
            "U3",
            "U3_1_over_delta_strict_enclosure",
            "a3",
            "actual_third_collision_chart",
            "actual_third_owner",
            "normalized_U3_derivative_strict_enclosure",
            "orientation",
            "simple_length_bound",
        },
        "closed coordinate contract",
    )
    require(contract["a3"] == "pi/2-asin(n3_x)+asin(p3)", "a3 formula")
    require(contract["U3"] == "a3(0)-a3(x)", "U3 formula")
    require(
        contract["actual_third_collision_chart"] == "N"
        and contract["actual_third_owner"] == "G[-1,-2]",
        "actual third chart and owner",
    )
    require(
        contract["orientation"] == "STRICTLY_INCREASING_U3",
        "U3 orientation label",
    )
    require(
        contract["simple_length_bound"] == "192<U3(1)/delta<193",
        "simple length label",
    )
    stored_contains(
        contract["U3_1_over_delta_strict_enclosure"],
        geometry["ratio"],
        "stored U3 length",
    )
    stored_contains(
        contract["normalized_U3_derivative_strict_enclosure"],
        geometry["derivative_ratio"],
        "stored U3 derivative",
    )


def verify_endpoints(
    result: dict[str, Any],
    round121: dict[str, Any],
    geometry: dict[str, Any],
) -> None:
    rows = result["stage3_endpoint_rows"]
    require(type(rows) is list and len(rows) == 192, "192 endpoint rows")
    require(
        result["stage3_endpoint_rows_sha256"] == digest(rows),
        "endpoint rows digest",
    )
    seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    theta_star = geometry["theta_star"]
    a3_zero = geometry["a3_zero"]
    delta = v121.aq(v121.DELTA)
    ids: set[str] = set()
    prior_upper = Q(0)
    for level, row in enumerate(rows, 1):
        require(type(row) is dict, "endpoint row type")
        require(row["natural_index_j"] == level and row["stage"] == 3,
                f"endpoint level:{level}")
        expected_id = endpoint_id(seed_id, level)
        require(row["endpoint_id"] == expected_id, f"endpoint ID:{level}")
        require(expected_id not in ids, f"unique endpoint ID:{level}")
        ids.add(expected_id)
        require(
            row["exact_root_equation_id"]
            == f"round123-U3-equals-{level}-delta"
            and row["exact_root_equation"] == f"U3(x)={level}*10^-90",
            f"endpoint exact equation:{level}",
        )
        require(
            row["actual_third_chart"] == "N"
            and row["orientation"] == "U3(x)=a3(0)-a3(x)",
            f"endpoint chart/orientation:{level}",
        )
        bracket = row["x_dyadic_bracket"]
        require(type(bracket) is list and len(bracket) == 2,
                f"endpoint bracket:{level}")
        lower = qvalue(bracket[0], f"endpoint lower:{level}")
        upper = qvalue(bracket[1], f"endpoint upper:{level}")
        require(prior_upper < lower < upper <= 1, f"endpoint order:{level}")
        prior_upper = upper
        require(
            qvalue(row["x_bracket_width"], f"endpoint width:{level}")
            == upper - lower,
            f"endpoint width identity:{level}",
        )
        target = v121.aq(Q(level) * v121.DELTA)
        lower_value = u3_value(theta_star, a3_zero, lower, lower) - target
        upper_value = u3_value(theta_star, a3_zero, upper, upper) - target
        require(
            v121.strict_sign(lower_value) == -1
            and v121.strict_sign(upper_value) == 1,
            f"endpoint signs:{level}",
        )
        derivative = -a3(
            theta_star, v121.interval(lower, upper), True
        ).derivative / delta
        derivative_lower, derivative_upper = interval_pair(derivative)
        require(
            Q(192)
            < derivative_lower
            <= derivative_upper
            < Q(193),
            f"endpoint derivative:{level}",
        )
        stored_contains(
            row["normalized_derivative_strict_enclosure"],
            derivative,
            f"stored endpoint derivative:{level}",
        )
        require(
            row["left_function_sign"] == -1
            and row["right_function_sign"] == 1
            and row["unique_root_certified"] is True,
            f"endpoint root certificate:{level}",
        )
        require(
            row["numeric_bracket_participates_in_ID"] is False,
            f"endpoint identity semantics:{level}",
        )
        require(
            row["lower_owner"] == f"stage-3-natural-cell-{level - 1}"
            and row["upper_owner"] == f"stage-3-natural-cell-{level}",
            f"endpoint owners:{level}",
        )
        require(row["row_sha256"] == row_digest(row),
                f"endpoint row digest:{level}")


def verify_natural_cells(
    result: dict[str, Any], round121: dict[str, Any]
) -> None:
    rows = result["stage3_natural_cell_rows"]
    endpoints = result["stage3_endpoint_rows"]
    require(type(rows) is list and len(rows) == 193, "193 natural cells")
    require(
        result["stage3_natural_cell_rows_sha256"] == digest(rows),
        "natural-cell rows digest",
    )
    seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    left = source_boundary_id("left", seed_id)
    right = source_boundary_id("right", seed_id)
    endpoint_ids = [left, *(row["endpoint_id"] for row in endpoints), right]
    ratio_lower, ratio_upper = (
        qvalue(value, "stored stage3 length")
        for value in result["stage3_adapted_coordinate_contract"][
            "U3_1_over_delta_strict_enclosure"
        ]
    )
    for index, row in enumerate(rows):
        full = index < 192
        require(row["natural_index_j"] == index and row["stage"] == 3,
                f"natural-cell index:{index}")
        require(
            row["recut_instance_id"] == stage3_cell_id(seed_id, index),
            f"natural-cell ID:{index}",
        )
        require(
            row["adapted_coordinate_id"]
            == "round123-U3-north-chart-output",
            f"natural-cell coordinate:{index}",
        )
        require(row["adapted_lower"] == f"{index}*delta",
                f"natural-cell lower:{index}")
        require(
            row["adapted_upper"]
            == (f"{index + 1}*delta" if full else "U3(1)"),
            f"natural-cell upper:{index}",
        )
        expected_length = (
            [Q(1), Q(1)]
            if full
            else [ratio_lower - 192, ratio_upper - 192]
        )
        stored_length = [
            qvalue(value, f"natural-cell length:{index}")
            for value in row["normalized_adapted_length_enclosure"]
        ]
        require(stored_length == expected_length,
                f"natural-cell length identity:{index}")
        require(
            row["lower_endpoint_id"] == endpoint_ids[index]
            and row["upper_endpoint_id"] == endpoint_ids[index + 1],
            f"natural-cell endpoints:{index}",
        )
        require(
            row["lower_closed"] is True
            and row["upper_closed"] is False
            and row["internal_cut_is_owned_by_right_cell"] is True
            and row["source_parent_right_endpoint_remains_open"] is True,
            f"natural-cell ownership:{index}",
        )
        require(
            row["full_delta_cell"] is full
            and row["terminal_partial_cell"] is (not full),
            f"natural-cell terminal flags:{index}",
        )
        require(
            row["actual_third_owner"] == "G[-1,-2]"
            and row["actual_third_collision_chart"] == "N",
            f"natural-cell actual third:{index}",
        )
        require(row["row_sha256"] == row_digest(row),
                f"natural-cell row digest:{index}")


def cut_gap_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    gaps: list[tuple[Q, str, str, str]] = []
    for left, right in zip(rows, rows[1:]):
        gap = qvalue(
            right["x_dyadic_bracket"][0], "right cut lower"
        ) - qvalue(left["x_dyadic_bracket"][1], "left cut upper")
        require(gap > 0, "strict merged cut order")
        origins = {left["origin"], right["origin"]}
        if origins == {"ROUND123_STAGE3_OUTPUT_CUT"}:
            kind = "STAGE3_TO_STAGE3"
        elif origins == {"ROUND121_EXISTING_INPUT_CUT"}:
            kind = "EXISTING_TO_EXISTING"
        else:
            kind = "CROSS_ORIGIN"
        gaps.append((gap, kind, left["endpoint_id"], right["endpoint_id"]))
    minimum = min(gaps, key=lambda item: item[0])
    by_kind: dict[str, tuple[Q, str, str]] = {}
    for gap, kind, left_id, right_id in gaps:
        if kind not in by_kind or gap < by_kind[kind][0]:
            by_kind[kind] = (gap, left_id, right_id)
    return {
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


def verify_merged_cuts(
    result: dict[str, Any],
    round121: dict[str, Any],
    geometry: dict[str, Any],
) -> None:
    rows = result["merged_internal_cut_rows"]
    require(type(rows) is list and len(rows) == 215, "215 merged cuts")
    require(
        result["merged_internal_cut_rows_sha256"] == digest(rows),
        "merged rows digest",
    )
    old = {
        row["endpoint_id"]: row for row in round121["pullback_endpoint_rows"]
    }
    new = {
        row["endpoint_id"]: row for row in result["stage3_endpoint_rows"]
    }
    require(len(old) == 23 and len(new) == 192, "cut source census")
    theta_star = geometry["theta_star"]
    a3_zero = geometry["a3_zero"]
    seen_old: set[str] = set()
    seen_new: set[str] = set()
    prior_upper = Q(0)
    for row in rows:
        endpoint = row["endpoint_id"]
        lower = qvalue(row["x_dyadic_bracket"][0], "merged lower")
        upper = qvalue(row["x_dyadic_bracket"][1], "merged upper")
        require(prior_upper < lower < upper < 1, "merged bracket order")
        prior_upper = upper
        if endpoint in old:
            source = old[endpoint]
            seen_old.add(endpoint)
            require(
                row["origin"] == "ROUND121_EXISTING_INPUT_CUT"
                and row["stage"] == source["stage"]
                and row["natural_index_j"] == source["natural_index_j"]
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"],
                "existing merged cut crosswalk",
            )
            fresh = (
                u3_value(theta_star, a3_zero, lower, upper)
                / v121.aq(v121.DELTA)
            )
            stored_contains(
                row["u3_over_delta_enclosure"],
                fresh,
                "existing merged cut U3",
            )
        elif endpoint in new:
            source = new[endpoint]
            seen_new.add(endpoint)
            level = source["natural_index_j"]
            require(
                row["origin"] == "ROUND123_STAGE3_OUTPUT_CUT"
                and row["stage"] == 3
                and row["natural_index_j"] == level
                and row["x_dyadic_bracket"] == source["x_dyadic_bracket"]
                and row["u3_over_delta_enclosure"]
                == [str(level), str(level)],
                "stage3 merged cut crosswalk",
            )
        else:
            raise RuntimeError("unknown merged endpoint")
    require(seen_old == set(old) and seen_new == set(new),
            "complete merged cut census")
    require(
        result["merged_cut_spacing_audit"] == cut_gap_audit(rows),
        "merged cut spacing audit",
    )


def expected_fragments_and_partitions(
    result: dict[str, Any],
    round121: dict[str, Any],
    geometry: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    left = {
        "endpoint_id": source_boundary_id("left", seed_id),
        "origin": "SOURCE_OUTER_LEFT",
        "x_dyadic_bracket": ["0", "0"],
    }
    right = {
        "endpoint_id": source_boundary_id("right", seed_id),
        "origin": "SOURCE_OUTER_RIGHT",
        "x_dyadic_bracket": ["1", "1"],
    }
    boundaries = [left, *result["merged_internal_cut_rows"], right]
    children = sorted(
        round121["common_refinement_rows"],
        key=lambda row: row["common_rank"],
    )
    require(
        [row["common_rank"] for row in children] == list(range(24)),
        "Round121 common ranks",
    )
    input_rank = 0
    stage3_index = 0
    fragments: list[dict[str, Any]] = []
    grouped: dict[int, list[dict[str, Any]]] = {
        rank: [] for rank in range(24)
    }
    for fragment_rank, (lower, upper) in enumerate(
        zip(boundaries, boundaries[1:])
    ):
        lower_high = qvalue(lower["x_dyadic_bracket"][1], "fragment lower")
        upper_low = qvalue(upper["x_dyadic_bracket"][0], "fragment upper")
        require(lower_high < upper_low, "positive fragment gap")
        fresh_output_length = (
            u3_value(
                geometry["theta_star"],
                geometry["a3_zero"],
                upper_low,
                upper_low,
            )
            - u3_value(
                geometry["theta_star"],
                geometry["a3_zero"],
                lower_high,
                lower_high,
            )
        ) / v121.aq(v121.DELTA)
        stored_output_length = result["stage3_output_fragment_rows"][
            fragment_rank
        ]["normalized_stage3_output_length_strict_enclosure"]
        stored_contains(
            stored_output_length,
            fresh_output_length,
            f"output fragment length:{fragment_rank}",
        )
        output_length_lower = qvalue(
            stored_output_length[0],
            f"output fragment lower:{fragment_rank}",
        )
        require(
            output_length_lower > Q(4, 125),
            f"uniform output fragment lower:{fragment_rank}",
        )
        child = children[input_rank]
        fragment_id = "round123-stage3-output-fragment:" + digest(
            [
                "round123-stage3-output-fragment-v0",
                seed_id,
                child["common_child_id"],
                lower["endpoint_id"],
                upper["endpoint_id"],
                stage3_index,
            ]
        )
        row = {
            "output_fragment_id": fragment_id,
            "fragment_rank": fragment_rank,
            "input_common_child_id": child["common_child_id"],
            "input_common_rank": input_rank,
            "stage3_natural_index_j": stage3_index,
            "stage3_output_recut_instance_id": stage3_cell_id(
                seed_id, stage3_index
            ),
            "source_x_lower_endpoint_id": lower["endpoint_id"],
            "source_x_upper_endpoint_id": upper["endpoint_id"],
            "source_x_open_gap_strict_lower": qstr(upper_low - lower_high),
            "normalized_stage3_output_length_strict_enclosure": (
                stored_output_length
            ),
            "normalized_stage3_output_length_strict_lower_exceeds": "4/125",
            "adapted_output_containment": (
                f"[{stage3_index}*delta,"
                + (
                    f"{stage3_index + 1}*delta)"
                    if stage3_index < 192
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
        grouped[input_rank].append(row)
        if upper["origin"] == "ROUND121_EXISTING_INPUT_CUT":
            input_rank += 1
        elif upper["origin"] == "ROUND123_STAGE3_OUTPUT_CUT":
            stage3_index += 1
    require(input_rank == 23 and stage3_index == 192,
            "terminal refinement indices")

    partitions: list[dict[str, Any]] = []
    for rank, child in enumerate(children):
        parts = grouped[rank]
        require(parts, f"nonempty input partition:{rank}")
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
                    qvalue(
                        fragment[
                            "normalized_stage3_output_length_strict_enclosure"
                        ][0],
                        "partition output length",
                    )
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


def expected_frontier_theorem() -> dict[str, Any]:
    q = Q_REGULARITY
    theta = THETA_INVERSE
    cj = DISTORTION_CJ
    cone = REGULAR_DENSITY_CONE_K
    one_step = q * cone + cj
    three_step = q**3 * cone + cj * (1 + q + q**2)
    cross_margin = 93**3 * 180337 - 144000 * 100**3
    require(theta < q**3 and cross_margin == 1055328309,
            "theta arithmetic")
    require(one_step < cone and three_step < cone, "cone arithmetic")
    require(
        DISTORTION_ONLY_FRONTIER_CONSTANT == 1 + q * cj,
        "distortion-only arithmetic",
    )
    return {
        "status": "ARITHMETIC_AND_ASSEMBLY_FRONTIER_ONLY__NOT_F14",
        "authoritative_one_step_recurrence": (
            "Reg_out <= (93/100)*Reg_in + C_J"
        ),
        "warning": "C_J is additive and is not multiplied by 93/100",
        "q": str(q),
        "theta_inverse": str(theta),
        "theta_strictly_less_than_q_cubed": True,
        "theta_q_cubed_integer_cross_margin": cross_margin,
        "C_J": str(cj),
        "regular_density_cone_K": str(cone),
        "one_step_cone_image_upper": str(one_step),
        "one_step_cone_margin": str(cone - one_step),
        "three_step_cone_image_upper": str(three_step),
        "three_step_cone_margin": str(cone - three_step),
        "distortion_only_frontier_constant": str(
            DISTORTION_ONLY_FRONTIER_CONSTANT
        ),
        "distortion_only_constant_identity": "1+(93/100)*C_J",
        "distortion_only_constant_is_an_accepted_F14_cost": False,
        "short_length_hypothesis": (
            "every input and output recut cell has adapted length <= delta=10^-90"
        ),
        "rejected_fragmentwise_bound": (
            "C14*M_fragment does not control the accepted"
            " M_fragment/ell_fragment norm term"
        ),
        "certified_output_length_lower": (
            "every materialized stage3 output fragment has"
            " ell_fragment > (3/100)*delta"
        ),
        "certified_family_level_mass_weighted_bound": (
            "sum_fragment M_fragment/ell_fragment"
            " < (100/(3*delta))*M_input_child"
        ),
        "fragment_number_does_not_multiply_the_mass_weighted_bound": True,
        "arbitrary_fragment_masses_are_symbolic_and_not_assumed_equal": True,
        "round122_final_F10_F13_F16_bridge_pin": "PENDING",
        "independent_round123_replay": "PENDING",
        "F14_theorem_installed": False,
    }


def expected_f14_rows(
    round121: dict[str, Any],
    partitions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    partition_by_child = {
        row["input_common_child_id"]: row for row in partitions
    }
    coordinates = [
        row
        for row in round121["gate5_F1_F6_slot_rows"]
        if row["field_index"] == 1
    ]
    coordinates.sort(
        key=lambda row: canonical(
            [
                row["official_word_key_id"],
                row["refined_homogeneous_subbranch_id"],
                row["roof_level_j"],
            ]
        )
    )
    require(len(coordinates) == 120, "120 F14 coordinates")
    rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    for coordinate in coordinates:
        partition = partition_by_child[coordinate["common_child_id"]]
        immutable_key = [
            coordinate["official_word_key_id"],
            coordinate["refined_homogeneous_subbranch_id"],
            coordinate["roof_level_j"],
            "regular_density_operator_cost",
        ]
        require(canonical(immutable_key) not in keys, "unique F14 key")
        keys.add(canonical(immutable_key))
        row = {
            "slot_id": f14_slot_id(immutable_key),
            "immutable_slot_key": immutable_key,
            "official_word_key_id": coordinate["official_word_key_id"],
            "refined_homogeneous_subbranch_id": coordinate[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_j": coordinate["roof_level_j"],
            "field_index": 14,
            "field_name": "regular_density_operator_cost",
            "common_child_id": coordinate["common_child_id"],
            "input_common_rank": partition["input_common_rank"],
            "stage3_output_fragment_count": partition[
                "output_fragment_count"
            ],
            "stage3_output_fragment_ids": partition[
                "output_fragment_ids"
            ],
            "field_value": "NOT_INSTALLED",
            "distortion_only_frontier_constant": str(
                DISTORTION_ONLY_FRONTIER_CONSTANT
            ),
            "distortion_only_constant_is_an_accepted_F14_cost": False,
            "certified_mass_weighted_inverse_length_assembly": (
                "sum_fragment M_fragment/ell_fragment"
                "<(100/(3*delta))*M_input_child"
            ),
            "slot_status": "FRONTIER_ONLY__FAIL_CLOSED__NOT_INSTALLED",
            "blocking_dependencies": [
                "FINAL_ROUND122_F10_F13_F16_BRIDGE_PIN",
                "INDEPENDENT_ROUND123_STAGE3_AND_F14_VERIFIER",
            ],
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def verify_static_and_assembly(
    document: dict[str, Any],
    round121: dict[str, Any],
    geometry: dict[str, Any],
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS,
            "closed certificate result")
    require(document["result_sha256"] == digest(result),
            "certificate result digest")
    require(
        type(result["precision_bits"]) is int
        and not isinstance(result["precision_bits"], bool)
        and result["precision_bits"] >= 1024,
        "producer precision",
    )
    require(
        type(result["root_bisections"]) is int
        and not isinstance(result["root_bisections"], bool)
        and result["root_bisections"] >= 200,
        "producer root depth",
    )
    require(
        result["status"]
        == "PRODUCER_SKELETON__STAGE3_OUTPUT_MATERIALIZED__F14_FAIL_CLOSED",
        "fail-closed status",
    )
    require(
        result["upstream_and_helper_pins"]
        == {
            "deliverables/cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json": ROUND121_SHA256,
            "deliverables/cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py": ROUND121_PRODUCER_SHA256,
        },
        "closed upstream pins without Round122",
    )
    require(
        all("round122" not in key.lower()
            for key in result["upstream_and_helper_pins"]),
        "Round122 must not be pinned provisionally",
    )
    require(
        result["regular_density_frontier_theorem"]
        == expected_frontier_theorem(),
        "regular-density frontier theorem",
    )

    expected_fragments, expected_partitions = expected_fragments_and_partitions(
        result, round121, geometry
    )
    require(
        result["stage3_output_fragment_rows"] == expected_fragments
        and result["stage3_output_fragment_rows_sha256"]
        == digest(expected_fragments),
        "independent output fragments",
    )
    require(
        result["input_child_output_partition_rows"] == expected_partitions
        and result["input_child_output_partition_rows_sha256"]
        == digest(expected_partitions),
        "independent input mass partitions",
    )
    counts = [row["output_fragment_count"] for row in expected_partitions]
    histogram: dict[str, int] = {}
    for count in counts:
        histogram[str(count)] = histogram.get(str(count), 0) + 1
    expected_ledger = {
        "existing_round121_internal_cut_count": 23,
        "stage3_internal_cut_count": 192,
        "stage3_natural_cell_count": 193,
        "combined_internal_cut_count": 215,
        "output_fragment_count": 216,
        "input_common_child_count": 24,
        "output_fragment_count_per_input_child_min": min(counts),
        "output_fragment_count_per_input_child_max": max(counts),
        "output_fragment_count_per_input_child_histogram": histogram,
        "global_minimum_normalized_stage3_output_length_strict_lower": qstr(
            min(
                qvalue(
                    row[
                        "minimum_normalized_stage3_output_length_strict_lower"
                    ],
                    "partition minimum output length",
                )
                for row in expected_partitions
            )
        ),
        "uniform_output_fragment_length_strict_lower": "3/100",
        "family_mass_weighted_inverse_length_coefficient": "100/(3*delta)",
        "all_counts_derived_without_expected_output_fragment_literal": True,
    }
    require(result["derived_count_ledger"] == expected_ledger,
            "derived count ledger")

    f14_rows = expected_f14_rows(round121, expected_partitions)
    require(
        result["gate5_F14_frontier_slot_rows"] == f14_rows
        and result["gate5_F14_frontier_slot_rows_sha256"]
        == digest(f14_rows)
        and result["F14_frontier_slot_count"] == 120,
        "independent 120 F14 frontier slots",
    )
    require(
        result["F14_installed_slot_count"] == 0
        and result["F14_installation_gate"]
        == {
            "stage3_output_properization_materialized_by_producer": True,
            "final_round122_bridge_pinned": False,
            "independent_round123_verifier_passed": False,
            "all_required_conditions_met": False,
            "fail_closed": True,
        },
        "F14 remains fail-closed",
    )
    require(
        result["gate5_actual_child_field_status"]
        == round121["gate5_actual_child_field_status"]
        and result["gate5_actual_child_field_status"]["F14"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "actual-child field status",
    )
    require(
        result["rank3_seed_child_field_maturity"] == "6/18"
        and result["candidate_maturity_after_future_R122_and_F14"]
        == "15/18__FRONTIER_ONLY__NOT_INSTALLED"
        and result["gate5_global_maturity"] == "10/18"
        and result["complete_18_field_block_count"] == 0
        and result["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "strict Gate5 and CM2 status",
    )


def verify(certificate: Path) -> dict[str, Any]:
    ctx.prec = VERIFIER_BITS
    document = v121.strict_json(certificate.read_text(encoding="utf-8"))
    round121 = load_round121()
    geometry = independent_geometry()
    verify_static_and_assembly(document, round121, geometry)
    result = document["result"]
    verify_coordinate_contract(result, geometry)
    verify_endpoints(result, round121, geometry)
    verify_natural_cells(result, round121)
    verify_merged_cuts(result, round121, geometry)
    verification = {
        "status": "PASS__STAGE3_PROPERIZATION__F14_REMAINS_FAIL_CLOSED",
        "verifier_precision_bits": VERIFIER_BITS,
        "certificate_sha256": sha256(certificate),
        "certificate_result_sha256": document["result_sha256"],
        "independently_verified_stage3_internal_cut_count": 192,
        "independently_verified_stage3_natural_cell_count": 193,
        "independently_verified_merged_internal_cut_count": 215,
        "independently_verified_output_fragment_count": 216,
        "independently_verified_input_partition_count": 24,
        "independently_verified_F14_frontier_slot_count": 120,
        "F14_installed_slot_count": 0,
        "round122_final_bridge_pinned": False,
        "rank3_seed_child_field_maturity": "6/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    document = verify(args.certificate)
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
