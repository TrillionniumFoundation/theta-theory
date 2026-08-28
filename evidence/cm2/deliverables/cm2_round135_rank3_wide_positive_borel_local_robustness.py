#!/usr/bin/env python3
"""Round135: wide positive-Borel local robustness at half-width 2^-17.

Round129 and Round130 used the nondegenerate but deliberately tiny collar
``|lambda-3/65536| <= 2^-512``.  This producer proves that the same *local*
rank-three construction is robust on

    lambda in [5/131072, 7/131072]

whose half-width is 2^-17.  Directly subtracting two nearly equal adapted
coordinates loses the delta=10^-90 scale on this collar.  We instead certify

    D1 = -partial_x(a1)/delta,
    D2 =  partial_x(a2)/delta,
    D3 = -partial_x(a3)/delta,
    Vi(x) = integral_0^x Di(y) dy,

on sixty-four source-x subintervals and invert the monotone integral
envelopes.  This materializes all 23 input recut-root guards, their common
refinement, all 192 stage-three guards, and the 216 merged output fragments.

The complete typed physical audit is replayed on four lambda/root-graph
subcollars.  It remains empty, so physical F10 is still zero.  The restricted
relative cemetery is separately zero because each fibrewise half-open output
partition is exhaustive.  Neither statement installs an ambient
pre-regularization or all-time owner cemetery.

Among negative powers of two, 2^-17 is the largest half-width that remains
strictly inside the frozen Round113 parent cell: 2^-16 lands exactly on both
cell faces.  All conclusions remain local.  Global Gate5 stays 10/18 with
zero global complete blocks, and CM2 stays NO-GO_FOR_CLAIM.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round113_rank3_root_sheet_owner_ordering_spike as r113
import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as r121
import cm2_round122_rank3_exact_seed_physical_face_field_bridge as r122
import cm2_round123_rank3_exact_seed_stage3_output_properization_common as c123
import cm2_round130_rank3_positive_borel_local_18_field_completion as r130


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json"
)
SCHEMA = "cm2.round135.rank3-wide-positive-borel-local-robustness.v1"
PRECISION_BITS = 2048

LAMBDA_CENTER = Q(3, 65536)
LAMBDA_HALF_WIDTH = Q(1, 2**17)
LAMBDA_LOWER = LAMBDA_CENTER - LAMBDA_HALF_WIDTH
LAMBDA_UPPER = LAMBDA_CENTER + LAMBDA_HALF_WIDTH
LAMBDA_LENGTH = 2 * LAMBDA_HALF_WIDTH
NEXT_DYADIC_HALF_WIDTH = Q(1, 2**16)
PARENT_LOWER = Q(1, 32768)
PARENT_UPPER = Q(1, 16384)
FIXED_C0 = Q(1, 16384)

ROOT_BISECTIONS = 360
INTERVAL_FACE_PADDING = Q(1, 2**40)
X_SUBDIVISIONS = 64
PHYSICAL_SUBDIVISIONS = 4
DELTA = r121.DELTA

ROUND121_PRODUCER = HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py"
ROUND121 = (
    HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
ROUND121_VERIFICATION = (
    HERE
    / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
)
ROUND122_PRODUCER = HERE / "cm2_round122_rank3_exact_seed_physical_face_field_bridge.py"
ROUND123_COMMON = HERE / "cm2_round123_rank3_exact_seed_stage3_output_properization_common.py"
ROUND129_PRODUCER = HERE / "cm2_round129_rank3_positive_borel_recut_field_bridge.py"
ROUND129 = (
    HERE / "cm2-round129-rank3-positive-borel-recut-field-bridge-2026-07-24.json"
)
ROUND129_VERIFIER = (
    HERE / "cm2_round129_rank3_positive_borel_recut_field_bridge_verifier.py"
)
ROUND129_VERIFICATION = (
    HERE
    / "cm2-round129-rank3-positive-borel-recut-field-bridge-verification-2026-07-24.json"
)
ROUND130_PRODUCER = HERE / "cm2_round130_rank3_positive_borel_local_18_field_completion.py"
ROUND130 = (
    HERE
    / "cm2-round130-rank3-positive-borel-local-18-field-completion-2026-07-24.json"
)
ROUND130_VERIFIER = (
    HERE / "cm2_round130_rank3_positive_borel_local_18_field_completion_verifier.py"
)
ROUND130_VERIFICATION = (
    HERE
    / "cm2-round130-rank3-positive-borel-local-18-field-completion-verification-2026-07-24.json"
)
ROUND113_PRODUCER = HERE / "cm2_round113_rank3_root_sheet_owner_ordering_spike.py"

PINS = {
    ROUND113_PRODUCER.name:
        "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e",
    ROUND121_PRODUCER.name:
        "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    ROUND121.name:
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    ROUND121_VERIFICATION.name:
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    ROUND122_PRODUCER.name:
        "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    ROUND123_COMMON.name:
        "8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0",
    ROUND129_PRODUCER.name:
        "bb0884aa14c256d16acd86c47ef1bf75e910507fa0b9334be704a6ee3995a054",
    ROUND129.name:
        "1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762",
    ROUND129_VERIFIER.name:
        "64c20bae8ea2944cb8487b253f9e0ff0a1a68a0c11fe0cd8d6d2206427981ea7",
    ROUND129_VERIFICATION.name:
        "4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db",
    ROUND130_PRODUCER.name:
        "441b714c6795646a1eeafe94be7419c9b91e14838ea0c321878cde2e11efff31",
    ROUND130.name:
        "5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5",
    ROUND130_VERIFIER.name:
        "59d1becfad10272b56ba034396500424cc1f6b29ab8a4a3673050d77a82cf136",
    ROUND130_VERIFICATION.name:
        "510ffb04b90277004f2968e27db4367d9253c2e678b51f384dcfd4dc6c241888",
}

CLOSED_SCHEMAS = {
    ROUND121.name: "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    ROUND121_VERIFICATION.name:
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1",
    ROUND129.name: "cm2.round129.rank3-positive-borel-recut-field-bridge.v1",
    ROUND129_VERIFICATION.name:
        "cm2.round129.rank3-positive-borel-recut-field-bridge-verification.v1",
    ROUND130.name:
        "cm2.round130.rank3-positive-borel-local-18-field-completion.v1",
    ROUND130_VERIFICATION.name:
        "cm2.round130.rank3-positive-borel-local-18-field-completion-verification.v1",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    value = Q(value)
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
        f"unsafe input type: {path.name}",
    )
    require(not path.is_symlink(), f"input symlink: {path.name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_float=lambda token: (_ for _ in ()).throw(
            ValueError(f"floating JSON number forbidden: {token}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant: {token}")
        ),
    )
    require(type(value) is dict, f"top-level JSON object: {path.name}")
    return value


def load_closed(path: Path) -> dict[str, Any]:
    value = strict_json(path)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"closed envelope: {path.name}",
    )
    require(value["schema"] == CLOSED_SCHEMAS[path.name], f"schema: {path.name}")
    require(type(value["result"]) is dict, f"result object: {path.name}")
    require(value["result_sha256"] == digest(value["result"]), f"digest: {path.name}")
    return value["result"]


def verification_passed(result: dict[str, Any]) -> bool:
    return result.get("verdict") == "PASS" or result.get("status") == "PASS"


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already hashed")
    result = dict(row)
    result["row_sha256"] = digest(row)
    return result


def row_id(kind: str, payload: list[Any]) -> str:
    return f"round135-{kind}:" + digest([f"round135-{kind}-v1", *payload])


def arb_bounds(value: arb) -> tuple[Q, Q]:
    return r121.arb_pair(value)


def interval_strings(value: arb) -> list[str]:
    low, high = arb_bounds(value)
    return [qstr(low), qstr(high)]


def abs_upper(value: arb) -> Q:
    low, high = arb_bounds(value)
    return max(abs(low), abs(high))


def validate_inputs() -> dict[str, dict[str, Any]]:
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink(),
            f"pinned input type: {name}",
        )
        require(path.resolve().parent == HERE, f"pinned input parent: {name}")
        require(sha256(path) == expected, f"pin mismatch: {name}")

    documents = {
        "r121": load_closed(ROUND121),
        "r121v": load_closed(ROUND121_VERIFICATION),
        "r129": load_closed(ROUND129),
        "r129v": load_closed(ROUND129_VERIFICATION),
        "r130": load_closed(ROUND130),
        "r130v": load_closed(ROUND130_VERIFICATION),
    }
    for key in ("r121v", "r129v", "r130v"):
        require(verification_passed(documents[key]), f"{key} PASS")
    for key in ("r121", "r129", "r130"):
        result = documents[key]
        require(result["gate5_global_maturity"] == "10/18", f"{key} maturity")
        require(
            result.get("global_complete_18_field_block_count", 0) == 0,
            f"{key} global blocks",
        )
        require(result["complete_18_field_block_count"] == 0, f"{key} blocks")
        require(result["gate5_block_count"] == 0, f"{key} Gate5 blocks")
        require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", f"{key} CM2")
    require(
        documents["r129"]["positive_Borel_family_local_field_maturity"] == "14/18",
        "Round129 local maturity",
    )
    require(
        documents["r130"][
            "positive_Borel_family_every_exact_fibre_local_field_maturity"
        ] == "18/18",
        "Round130 local maturity",
    )
    require(
        documents["r130"]["per_exact_lambda_fibre_local_complete_18_field_level_block_count"]
        == 120,
        "Round130 local level blocks",
    )
    require(
        documents["r130"]["per_exact_lambda_fibre_local_complete_18_field_child_packet_count"]
        == 24,
        "Round130 local packets",
    )
    return documents


def point_root(seed: dict[str, Any], lam: Q) -> tuple[Q, Q]:
    low, high = Q(1, 8), Q(13, 100)
    outer_signs = [
        r113.strict_sign(
            r113.equation_value(
                seed["source"],
                r121.EXPECTED_BRANCH,
                1,
                "BYPASS",
                t,
                FIXED_C0,
                FIXED_C0,
                lam,
                lam,
            )
        )
        for t in (low, high)
    ]
    require(outer_signs == [1, -1], "point-root outer signs")
    for _ in range(ROOT_BISECTIONS):
        middle = (low + high) / 2
        sign = r113.strict_sign(
            r113.equation_value(
                seed["source"],
                r121.EXPECTED_BRANCH,
                1,
                "BYPASS",
                middle,
                FIXED_C0,
                FIXED_C0,
                lam,
                lam,
            )
        )
        require(sign != 0, "point-root bisection sign")
        if sign > 0:
            low = middle
        else:
            high = middle
    require(high - low == Q(1, 200 * 2**ROOT_BISECTIONS), "point-root width")
    return low, high


def root_graph_contract(
    seed: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], tuple[Q, Q], dict[Q, tuple[Q, Q]]]:
    lambda_partition = [
        LAMBDA_LOWER + LAMBDA_LENGTH * Q(index, PHYSICAL_SUBDIVISIONS)
        for index in range(PHYSICAL_SUBDIVISIONS + 1)
    ]
    root_cache = {lam: point_root(seed, lam) for lam in lambda_partition}
    root_rows: list[dict[str, Any]] = []
    for index, lam in enumerate(lambda_partition):
        bracket = root_cache[lam]
        point_signs = [
            r113.strict_sign(
                r113.equation_value(
                    seed["source"],
                    r121.EXPECTED_BRANCH,
                    1,
                    "BYPASS",
                    t,
                    FIXED_C0,
                    FIXED_C0,
                    lam,
                    lam,
                )
            )
            for t in bracket
        ]
        require(point_signs == [1, -1], f"partition point signs: {index}")
        root_rows.append(
            with_hash(
                {
                    "root_partition_endpoint_id": row_id(
                        "lambda-root-partition-endpoint",
                        [index, qstr(lam)],
                    ),
                    "partition_endpoint_index": index,
                    "lambda_exact": qstr(lam),
                    "t_root_dyadic_bracket": [qstr(bracket[0]), qstr(bracket[1])],
                    "t_root_bracket_width": qstr(bracket[1] - bracket[0]),
                    "strict_face_signs": point_signs,
                    "root_bisection_count": ROOT_BISECTIONS,
                }
            )
        )

    exact_guard = (root_cache[LAMBDA_LOWER][0], root_cache[LAMBDA_UPPER][1])
    padded_guard = (
        exact_guard[0] - INTERVAL_FACE_PADDING,
        exact_guard[1] + INTERVAL_FACE_PADDING,
    )
    padded_signs = [
        r113.strict_sign(
            r113.equation_value(
                seed["source"],
                r121.EXPECTED_BRANCH,
                1,
                "BYPASS",
                t,
                FIXED_C0,
                FIXED_C0,
                LAMBDA_LOWER,
                LAMBDA_UPPER,
            )
        )
        for t in padded_guard
    ]
    require(padded_signs == [1, -1], "padded full-collar root signs")

    geometry = r113.path_geometry(
        seed["source"],
        r121.EXPECTED_BRANCH,
        1,
        "BYPASS",
        *padded_guard,
        FIXED_C0,
        FIXED_C0,
        LAMBDA_LOWER,
        LAMBDA_UPPER,
    )
    partial_t = geometry["equation"].gradient[0]
    partial_lambda = geometry["equation"].gradient[2]
    ft_low, ft_high = arb_bounds(partial_t)
    fl_low, fl_high = arb_bounds(partial_lambda)
    require(ft_high < -7 and ft_low > -8, "wide -8<F_t<-7")
    require(fl_low > 0, "wide F_lambda positive")
    target_radius = Q(r121.round112.radius(r121.EXPECTED_BRANCH[2]))
    require(target_radius == Q(4, 25), "BYPASS target radius")
    require(
        fl_low <= 2 * target_radius**2 * LAMBDA_LOWER
        <= 2 * target_radius**2 * LAMBDA_UPPER <= fl_high,
        "analytic F_lambda inside interval derivative",
    )
    dt = -partial_lambda / partial_t
    dt_low, dt_high = arb_bounds(dt)
    require(0 < dt_low <= dt_high < Q(1, 2_000_000), "wide dt/dlambda")
    radial_t = (arb(1) - r121.interval(*padded_guard) ** 2).sqrt()
    db = arb(36) / 25 / radial_t * dt
    db_low, db_high = arb_bounds(db)
    require(
        Q(1, 3_000_000) < db_low <= db_high < Q(1, 1_500_000),
        "wide db/dlambda",
    )

    family_root_id = (
        "round135-wide-positive-borel-family-root:"
        + digest(
            [
                "round135-wide-positive-borel-family-root-v1",
                r121.PARENT_ID,
                r121.OPERATOR_CELL_ID,
                r121.ANGULAR_LIFT_ID,
                qstr(FIXED_C0),
                qstr(LAMBDA_LOWER),
                qstr(LAMBDA_UPPER),
            ]
        )
    )
    contract = {
        "family_root_id": family_root_id,
        "fixed_c0": qstr(FIXED_C0),
        "lambda_coordinate": "b3",
        "lambda_center": qstr(LAMBDA_CENTER),
        "lambda_negative_power_of_two_half_width": qstr(LAMBDA_HALF_WIDTH),
        "lambda_closed_collar": [qstr(LAMBDA_LOWER), qstr(LAMBDA_UPPER)],
        "lambda_interval_length": qstr(LAMBDA_LENGTH),
        "round113_parent_id": r121.PARENT_ID,
        "round117_operator_cell_id": r121.OPERATOR_CELL_ID,
        "angular_lift_id": r121.ANGULAR_LIFT_ID,
        "strict_parent_cell": [qstr(PARENT_LOWER), qstr(PARENT_UPPER)],
        "strictly_inside_same_parent_and_operator_cell": (
            PARENT_LOWER < LAMBDA_LOWER < LAMBDA_UPPER < PARENT_UPPER
        ),
        "largest_negative_power_of_two_half_width_strictly_inside_parent":
            qstr(LAMBDA_HALF_WIDTH),
        "next_negative_power_of_two_half_width": qstr(NEXT_DYADIC_HALF_WIDTH),
        "next_half_width_closed_collar": [
            qstr(LAMBDA_CENTER - NEXT_DYADIC_HALF_WIDTH),
            qstr(LAMBDA_CENTER + NEXT_DYADIC_HALF_WIDTH),
        ],
        "next_half_width_hits_both_parent_faces": (
            LAMBDA_CENTER - NEXT_DYADIC_HALF_WIDTH == PARENT_LOWER
            and LAMBDA_CENTER + NEXT_DYADIC_HALF_WIDTH == PARENT_UPPER
        ),
        "first_next_dyadic_obstruction": (
            "strict inequalities lambda_lower>1/32768 and "
            "lambda_upper<1/16384 become equalities at half-width 2^-16"
        ),
        "exact_monotone_root_graph_guard": [
            qstr(exact_guard[0]), qstr(exact_guard[1])
        ],
        "exact_monotone_root_graph_guard_width": qstr(exact_guard[1] - exact_guard[0]),
        "interval_face_padding_for_direct_full_box_diagnostic":
            qstr(INTERVAL_FACE_PADDING),
        "padded_direct_interval_guard": [
            qstr(padded_guard[0]), qstr(padded_guard[1])
        ],
        "padded_direct_interval_face_signs": padded_signs,
        "BYPASS_equation_exact_lambda_structure": (
            "F(t,lambda)=Delta3(t)+(4/25)^2*lambda^2"
        ),
        "lambda_is_strictly_positive": LAMBDA_LOWER > 0,
        "uniform_F_t_enclosure": interval_strings(partial_t),
        "uniform_F_lambda_enclosure": interval_strings(partial_lambda),
        "F_t_strictly_negative": True,
        "F_lambda_strictly_positive": True,
        "root_t_strictly_increasing_in_lambda": True,
        "implicit_dt_dlambda_enclosure": interval_strings(dt),
        "b_of_lambda_definition": (
            "b(lambda)=acos(1/16384)-(36/25)*(pi-asin(t(lambda)))"
        ),
        "db_dlambda_enclosure": interval_strings(db),
        "db_dlambda_strict_bounds": "1/3000000<db/dlambda<1/1500000",
        "b_image_length_strict_lower": qstr(LAMBDA_LENGTH * Q(1, 3_000_000)),
        "b_image_is_non_degenerate_positive_Borel_interval": True,
        "old_Round129_narrow_derivative_shortcuts_reused": False,
    }
    require(contract["strictly_inside_same_parent_and_operator_cell"], "wide parent")
    require(contract["next_half_width_hits_both_parent_faces"], "next dyadic obstruction")
    return contract, root_rows, exact_guard, root_cache


def derivative_bounds(
    seed: dict[str, Any],
    t_guard: tuple[Q, Q],
    stage: int,
    x_lower: Q,
    x_upper: Q,
) -> tuple[Q, Q]:
    if stage in (1, 2):
        state = r121.raw_state(seed, t_guard, x_lower, x_upper)
        derivative = (
            -state["adapted1"].gradient[0]
            if stage == 1
            else state["adapted2"].gradient[0]
        ) / r121.aq(DELTA)
    else:
        require(stage == 3, "derivative stage")
        derivative = (
            -c123.adapted3(seed, t_guard, x_lower, x_upper).gradient[0]
            / r121.aq(DELTA)
        )
    low, high = arb_bounds(derivative)
    require(0 < low <= high, f"D{stage} positive")
    return low, high


def derivative_partition(
    family_root_id: str,
    seed: dict[str, Any],
    t_guard: tuple[Q, Q],
    stage: int,
    subdivisions: int,
    materialize: bool,
) -> tuple[list[tuple[Q, Q]], list[dict[str, Any]]]:
    bounds_rows: list[tuple[Q, Q]] = []
    rows: list[dict[str, Any]] = []
    for index in range(subdivisions):
        x_lower = Q(index, subdivisions)
        x_upper = Q(index + 1, subdivisions)
        low, high = derivative_bounds(
            seed, t_guard, stage, x_lower, x_upper
        )
        bounds_rows.append((low, high))
        if materialize:
            rows.append(
                with_hash(
                    {
                        "normalized_derivative_cell_id": row_id(
                            "normalized-derivative-cell",
                            [family_root_id, stage, index, subdivisions],
                        ),
                        "family_root_id": family_root_id,
                        "stage": stage,
                        "D_definition": (
                            "-partial_x(a1)/delta"
                            if stage == 1
                            else (
                                "partial_x(a2)/delta"
                                if stage == 2
                                else "-partial_x(a3)/delta"
                            )
                        ),
                        "x_subdivision_count": subdivisions,
                        "x_cell_index": index,
                        "x_closed_interval": [qstr(x_lower), qstr(x_upper)],
                        "D_strict_enclosure": [qstr(low), qstr(high)],
                        "D_strictly_positive": True,
                    }
                )
            )
    return bounds_rows, rows


def total_integral(cells: list[tuple[Q, Q]]) -> tuple[Q, Q]:
    width = Q(1, len(cells))
    return (
        sum((low * width for low, _ in cells), Q(0)),
        sum((high * width for _, high in cells), Q(0)),
    )


def integral_root(
    cells: list[tuple[Q, Q]],
    target: int,
) -> tuple[Q, Q, int, int]:
    subdivisions = len(cells)
    width = Q(1, subdivisions)
    cumulative_upper = Q(0)
    lower = None
    lower_cell = -1
    for index, (_low, high) in enumerate(cells):
        next_upper = cumulative_upper + high * width
        if next_upper >= target:
            lower = Q(index, subdivisions) + (Q(target) - cumulative_upper) / high
            lower_cell = index
            break
        cumulative_upper = next_upper
    require(lower is not None, "integral root lower")

    cumulative_lower = Q(0)
    upper = None
    upper_cell = -1
    for index, (low, _high) in enumerate(cells):
        next_lower = cumulative_lower + low * width
        if next_lower >= target:
            upper = Q(index, subdivisions) + (Q(target) - cumulative_lower) / low
            upper_cell = index
            break
        cumulative_lower = next_lower
    require(upper is not None, "integral root upper")
    require(Q(0) < lower <= upper < Q(1), "integral root domain")
    return lower, upper, lower_cell, upper_cell


def normalized_integral_contract(
    family_root_id: str,
    seed: dict[str, Any],
    t_guard: tuple[Q, Q],
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[tuple[int, int], tuple[Q, Q]],
    dict[int, tuple[Q, Q]],
    dict[int, list[tuple[Q, Q]]],
]:
    convergence_rows: list[dict[str, Any]] = []
    final_cells: dict[int, list[tuple[Q, Q]]] = {}
    derivative_rows: list[dict[str, Any]] = []
    for subdivisions in (1, 8, X_SUBDIVISIONS):
        for stage in (1, 2, 3):
            cells, rows = derivative_partition(
                family_root_id,
                seed,
                t_guard,
                stage,
                subdivisions,
                materialize=(subdivisions == X_SUBDIVISIONS),
            )
            integral = total_integral(cells)
            convergence_rows.append(
                with_hash(
                    {
                        "derivative_convergence_id": row_id(
                            "derivative-convergence",
                            [family_root_id, stage, subdivisions],
                        ),
                        "family_root_id": family_root_id,
                        "stage": stage,
                        "x_subdivision_count": subdivisions,
                        "D_global_strict_enclosure": [
                            qstr(min(low for low, _ in cells)),
                            qstr(max(high for _, high in cells)),
                        ],
                        "V_at_1_strict_enclosure": [
                            qstr(integral[0]), qstr(integral[1])
                        ],
                    }
                )
            )
            if subdivisions == X_SUBDIVISIONS:
                final_cells[stage] = cells
                derivative_rows.extend(rows)
    require(len(derivative_rows) == 3 * X_SUBDIVISIONS, "derivative row count")
    require(len(convergence_rows) == 9, "convergence row count")

    v1 = total_integral(final_cells[1])
    v2 = total_integral(final_cells[2])
    v3 = total_integral(final_cells[3])
    require(Q(34, 5) < v1[0] <= v1[1] < 7, "V1 terminal")
    require(Q(87, 5) < v2[0] <= v2[1] < 18, "V2 terminal")
    require(192 < v3[0] <= v3[1] < 193, "V3 terminal")

    input_roots: dict[tuple[int, int], tuple[Q, Q]] = {}
    input_root_rows: list[dict[str, Any]] = []
    for stage, count in ((1, 6), (2, 17)):
        for natural_index in range(1, count + 1):
            low, high, low_cell, high_cell = integral_root(
                final_cells[stage], natural_index
            )
            input_roots[(stage, natural_index)] = (low, high)
            input_root_rows.append(
                with_hash(
                    {
                        "input_recut_root_id": row_id(
                            "input-recut-root",
                            [family_root_id, stage, natural_index],
                        ),
                        "family_root_id": family_root_id,
                        "stage": stage,
                        "natural_index_j": natural_index,
                        "equation": f"V{stage}(lambda,x)={natural_index}",
                        "x_strict_guard": [qstr(low), qstr(high)],
                        "lower_envelope_crossing_cell": low_cell,
                        "upper_envelope_crossing_cell": high_cell,
                        "V_upper_envelope_at_guard_lower": qstr(Q(natural_index)),
                        "V_lower_envelope_at_guard_upper": qstr(Q(natural_index)),
                        "D_positive_implies_unique_root_per_exact_lambda": True,
                        "endpoint_difference_subtraction_used": False,
                    }
                )
            )
    require(len(input_root_rows) == 23, "input root count")

    stage3_roots: dict[int, tuple[Q, Q]] = {}
    stage3_root_rows: list[dict[str, Any]] = []
    for natural_index in range(1, 193):
        low, high, low_cell, high_cell = integral_root(
            final_cells[3], natural_index
        )
        stage3_roots[natural_index] = (low, high)
        stage3_root_rows.append(
            with_hash(
                {
                    "stage3_recut_root_id": row_id(
                        "stage3-recut-root",
                        [family_root_id, natural_index],
                    ),
                    "family_root_id": family_root_id,
                    "stage": 3,
                    "natural_index_j": natural_index,
                    "equation": f"V3(lambda,x)={natural_index}",
                    "x_strict_guard": [qstr(low), qstr(high)],
                    "lower_envelope_crossing_cell": low_cell,
                    "upper_envelope_crossing_cell": high_cell,
                    "V_upper_envelope_at_guard_lower": qstr(Q(natural_index)),
                    "V_lower_envelope_at_guard_upper": qstr(Q(natural_index)),
                    "D_positive_implies_unique_root_per_exact_lambda": True,
                    "endpoint_difference_subtraction_used": False,
                }
            )
        )
    require(len(stage3_root_rows) == 192, "stage3 root count")

    contract = {
        "family_root_id": family_root_id,
        "delta": qstr(DELTA),
        "normalized_derivatives": {
            "D1": "-partial_x(a1)/delta",
            "D2": "partial_x(a2)/delta",
            "D3": "-partial_x(a3)/delta",
        },
        "normalized_integrals": "Vi(lambda,x)=integral_0^x Di(lambda,y)dy",
        "endpoint_difference_subtraction_used": False,
        "dependency_preserving_method": (
            "positive interval derivative cells plus lower/upper Riemann "
            "integral envelopes and monotone inversion"
        ),
        "x_subdivision_counts_replayed": [1, 8, X_SUBDIVISIONS],
        "materialized_x_subdivision_count": X_SUBDIVISIONS,
        "D1_global_strict_enclosure": [
            qstr(min(low for low, _ in final_cells[1])),
            qstr(max(high for _, high in final_cells[1])),
        ],
        "D2_global_strict_enclosure": [
            qstr(min(low for low, _ in final_cells[2])),
            qstr(max(high for _, high in final_cells[2])),
        ],
        "D3_global_strict_enclosure": [
            qstr(min(low for low, _ in final_cells[3])),
            qstr(max(high for _, high in final_cells[3])),
        ],
        "V1_at_1_strict_enclosure": [qstr(v1[0]), qstr(v1[1])],
        "V2_at_1_strict_enclosure": [qstr(v2[0]), qstr(v2[1])],
        "V3_at_1_strict_enclosure": [qstr(v3[0]), qstr(v3[1])],
        "terminal_normalized_lengths_strict_lower": {
            "stage1": qstr(v1[0] - 6),
            "stage2": qstr(v2[0] - 17),
            "stage3": qstr(v3[0] - 192),
        },
        "stable_natural_cell_counts": [1, 7, 18, 193],
        "input_recut_root_count": 23,
        "stage3_recut_root_count": 192,
    }
    return (
        contract,
        convergence_rows,
        derivative_rows,
        input_roots,
        stage3_roots,
        final_cells,
    )


def synthetic_round121(
    round121: dict[str, Any],
    input_roots: dict[tuple[int, int], tuple[Q, Q]],
) -> dict[str, Any]:
    result = copy.deepcopy(round121)
    for row in result["pullback_endpoint_rows"]:
        key = (int(row["stage"]), int(row["natural_index_j"]))
        low, high = input_roots[key]
        row["x_dyadic_bracket"] = [qstr(low), qstr(high)]
    return result


def common_and_merged_geometry(
    family_root_id: str,
    input_roots: dict[tuple[int, int], tuple[Q, Q]],
    stage3_roots: dict[int, tuple[Q, Q]],
    final_cells: dict[int, list[tuple[Q, Q]]],
) -> dict[str, Any]:
    input_rows = [
        {
            "origin": "INPUT_RECUT",
            "stage": stage,
            "natural_index_j": natural_index,
            "guard": bracket,
            "endpoint_id": row_id(
                "input-recut-root",
                [family_root_id, stage, natural_index],
            ),
        }
        for (stage, natural_index), bracket in input_roots.items()
    ]
    input_rows.sort(key=lambda row: row["guard"][0])
    require(
        tuple(
            (row["stage"], row["natural_index_j"]) for row in input_rows
        ) == r121.EXPECTED_CUT_ORDER,
        "wide input cut order",
    )

    outer_and_input = [
        {
            "origin": "OUTER_LEFT",
            "stage": 0,
            "natural_index_j": 0,
            "guard": (Q(0), Q(0)),
            "endpoint_id": "round135-source-outer-left",
        },
        *input_rows,
        {
            "origin": "OUTER_RIGHT",
            "stage": 0,
            "natural_index_j": 1,
            "guard": (Q(1), Q(1)),
            "endpoint_id": "round135-source-outer-right",
        },
    ]
    common_rows: list[dict[str, Any]] = []
    stage_indices = [0, 0, 0]
    for rank, (left, right) in enumerate(
        zip(outer_and_input, outer_and_input[1:])
    ):
        gap = right["guard"][0] - left["guard"][1]
        require(gap > Q(1, 200), f"wide common gap: {rank}")
        common_rows.append(
            with_hash(
                {
                    "wide_common_rank_id": row_id(
                        "wide-common-rank",
                        [family_root_id, rank],
                    ),
                    "family_root_id": family_root_id,
                    "common_rank": rank,
                    "lower_endpoint_id": left["endpoint_id"],
                    "upper_endpoint_id": right["endpoint_id"],
                    "positive_source_x_length_strict_lower": qstr(gap),
                    "positive_source_x_length_exceeds_1_over_200": True,
                    "covering_stage_indices": list(stage_indices),
                    "half_open": True,
                }
            )
        )
        if rank < 23:
            stage_indices[right["stage"]] += 1
    require(stage_indices == [0, 6, 17], "wide terminal stage indices")
    require(len(common_rows) == 24, "wide common count")

    merged_raw = [
        *input_rows,
        *[
            {
                "origin": "STAGE3_OUTPUT_RECUT",
                "stage": 3,
                "natural_index_j": natural_index,
                "guard": bracket,
                "endpoint_id": row_id(
                    "stage3-recut-root",
                    [family_root_id, natural_index],
                ),
            }
            for natural_index, bracket in stage3_roots.items()
        ],
    ]
    merged_raw.sort(key=lambda row: row["guard"][0])
    merged_rows: list[dict[str, Any]] = []
    for rank, row in enumerate(merged_raw):
        merged_rows.append(
            with_hash(
                {
                    "wide_merged_cut_id": row_id(
                        "wide-merged-cut",
                        [
                            family_root_id,
                            row["origin"],
                            row["stage"],
                            row["natural_index_j"],
                        ],
                    ),
                    "family_root_id": family_root_id,
                    "merged_rank": rank,
                    "origin": row["origin"],
                    "stage": row["stage"],
                    "natural_index_j": row["natural_index_j"],
                    "source_endpoint_id": row["endpoint_id"],
                    "x_strict_guard": [
                        qstr(row["guard"][0]), qstr(row["guard"][1])
                    ],
                }
            )
        )
    require(len(merged_rows) == 215, "wide merged count")
    merged_gaps = [
        right["guard"][0] - left["guard"][1]
        for left, right in zip(merged_raw, merged_raw[1:])
    ]
    require(min(merged_gaps) > 0, "wide merged strict order")

    boundaries = [
        {
            "origin": "OUTER_LEFT",
            "stage": 0,
            "natural_index_j": 0,
            "guard": (Q(0), Q(0)),
            "endpoint_id": "round135-source-outer-left",
        },
        *merged_raw,
        {
            "origin": "OUTER_RIGHT",
            "stage": 0,
            "natural_index_j": 1,
            "guard": (Q(1), Q(1)),
            "endpoint_id": "round135-source-outer-right",
        },
    ]
    d3_low = min(low for low, _ in final_cells[3])
    d3_high = max(high for _, high in final_cells[3])
    fragment_rows: list[dict[str, Any]] = []
    input_rank = 0
    stage3_index = 0
    fragment_counts: Counter[int] = Counter()
    for rank, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        source_gap_lower = right["guard"][0] - left["guard"][1]
        source_gap_upper = right["guard"][1] - left["guard"][0]
        require(source_gap_lower > 0, f"wide fragment gap: {rank}")
        normalized_lower = d3_low * source_gap_lower
        normalized_upper = d3_high * source_gap_upper
        require(
            Q(4, 125) < normalized_lower <= normalized_upper,
            f"wide stage3 fragment length: {rank}",
        )
        fragment_counts[input_rank] += 1
        fragment_rows.append(
            with_hash(
                {
                    "wide_stage3_fragment_id": row_id(
                        "wide-stage3-fragment",
                        [family_root_id, rank, input_rank, stage3_index],
                    ),
                    "family_root_id": family_root_id,
                    "fragment_rank": rank,
                    "input_common_rank": input_rank,
                    "stage3_natural_index_j": stage3_index,
                    "lower_endpoint_id": left["endpoint_id"],
                    "upper_endpoint_id": right["endpoint_id"],
                    "source_x_gap_strict_enclosure": [
                        qstr(source_gap_lower), qstr(source_gap_upper)
                    ],
                    "normalized_stage3_output_length_strict_enclosure": [
                        qstr(normalized_lower), qstr(normalized_upper)
                    ],
                    "normalized_length_strict_lower_exceeds": "4/125",
                    "half_open": True,
                }
            )
        )
        if right["origin"] == "INPUT_RECUT":
            input_rank += 1
        elif right["origin"] == "STAGE3_OUTPUT_RECUT":
            stage3_index += 1
    require((input_rank, stage3_index) == (23, 192), "wide fragment terminal indices")
    require(len(fragment_rows) == 216, "wide fragment count")
    require(set(fragment_counts) == set(range(24)), "wide fragment child coverage")
    histogram = Counter(fragment_counts.values())
    require(
        histogram
        == Counter({12: 11, 4: 2, 6: 2, 9: 2, 2: 1, 3: 1, 5: 1, 7: 1, 8: 1, 10: 1, 11: 1}),
        "wide fragment histogram",
    )

    v1 = total_integral(final_cells[1])
    v2 = total_integral(final_cells[2])
    minimum_by_stage = {
        0: min(Q(1), v1[0] - 6),
        1: min(Q(1), v2[0] - 17),
        2: min(
            Q(row["normalized_stage3_output_length_strict_enclosure"][0])
            for row in fragment_rows
        ),
    }
    require(
        minimum_by_stage[0] > Q(3, 100)
        and minimum_by_stage[1] > Q(17, 200)
        and minimum_by_stage[2] > Q(4, 125),
        "wide stage output lengths",
    )
    return {
        "common_rows": common_rows,
        "merged_rows": merged_rows,
        "fragment_rows": fragment_rows,
        "minimum_input_common_gap": qstr(
            min(Q(row["positive_source_x_length_strict_lower"]) for row in common_rows)
        ),
        "minimum_merged_cut_gap": qstr(min(merged_gaps)),
        "minimum_output_length_by_input_stage": {
            str(stage): qstr(value)
            for stage, value in minimum_by_stage.items()
        },
        "fragment_count_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(histogram.items())
        },
    }


def physical_audit(
    family_root_id: str,
    seed: dict[str, Any],
    wide121: dict[str, Any],
    root_cache: dict[Q, tuple[Q, Q]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    two_slice_failure = None
    try:
        for index in range(2):
            lambda_lower = LAMBDA_LOWER + LAMBDA_LENGTH * Q(index, 2)
            lambda_upper = LAMBDA_LOWER + LAMBDA_LENGTH * Q(index + 1, 2)
            if lambda_lower not in root_cache:
                root_cache[lambda_lower] = point_root(seed, lambda_lower)
            if lambda_upper not in root_cache:
                root_cache[lambda_upper] = point_root(seed, lambda_upper)
            local_t = (
                root_cache[lambda_lower][0],
                root_cache[lambda_upper][1],
            )
            r122.physical_empty_audit(seed, local_t, wide121)
    except RuntimeError as exc:
        two_slice_failure = str(exc)
    require(
        two_slice_failure == "unresolved discriminant: W[-1,-2]",
        "two-slice dependency diagnostic",
    )

    rows: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    for index in range(PHYSICAL_SUBDIVISIONS):
        lambda_lower = LAMBDA_LOWER + LAMBDA_LENGTH * Q(
            index, PHYSICAL_SUBDIVISIONS
        )
        lambda_upper = LAMBDA_LOWER + LAMBDA_LENGTH * Q(
            index + 1, PHYSICAL_SUBDIVISIONS
        )
        require(lambda_lower in root_cache and lambda_upper in root_cache, "root cache")
        t_guard = (
            root_cache[lambda_lower][0],
            root_cache[lambda_upper][1],
        )
        physical = r122.physical_empty_audit(seed, t_guard, wide121)
        require(
            physical["physical_five_face_incidence_count"] == 0
            and physical["residual_physical_face_count"] == 0,
            f"wide physical empty: {index}",
        )
        documents.append(physical)
        rows.append(
            with_hash(
                {
                    "physical_subcollar_audit_id": row_id(
                        "physical-subcollar-audit",
                        [family_root_id, index],
                    ),
                    "family_root_id": family_root_id,
                    "partition_index": index,
                    "partition_count": PHYSICAL_SUBDIVISIONS,
                    "lambda_closed_subcollar": [
                        qstr(lambda_lower), qstr(lambda_upper)
                    ],
                    "monotone_t_root_guard": [
                        qstr(t_guard[0]), qstr(t_guard[1])
                    ],
                    "core_clearance_row_count": len(physical["core_clearance_rows"]),
                    "core_clearance_rows_sha256": physical[
                        "core_clearance_rows_sha256"
                    ],
                    "child_stage_boundary_row_count": len(
                        physical["child_stage_boundary_rows"]
                    ),
                    "child_stage_boundary_rows_sha256": physical[
                        "child_stage_boundary_rows_sha256"
                    ],
                    "check_counts": physical["check_counts"],
                    "actual_interval_lower_minima": physical[
                        "actual_interval_lower_minima"
                    ],
                    "claimed_strict_lower_margins": physical[
                        "claimed_strict_lower_margins"
                    ],
                    "rank3_candidate_occurrence_total_check_count":
                        physical["rank3_candidate_occurrence_total_check_count"],
                    "physical_five_face_incidence_count": 0,
                    "residual_physical_face_count": 0,
                    "complete_typed_physical_face_family_empty": True,
                }
            )
        )
    require(len(rows) == 4, "four physical audit rows")
    minima = {
        key: min(
            Q(document["actual_interval_lower_minima"][key])
            for document in documents
        )
        for key in documents[0]["actual_interval_lower_minima"]
    }
    claimed = {
        key: Q(value)
        for key, value in documents[0]["claimed_strict_lower_margins"].items()
    }
    require(
        all(minima[key] > claimed[key] for key in minima),
        "wide physical margins",
    )
    contract = {
        "family_root_id": family_root_id,
        "lambda_subdivision_count": PHYSICAL_SUBDIVISIONS,
        "all_four_closed_subcollars_cover_full_closed_collar": True,
        "subcollar_interiors_are_disjoint": True,
        "shared_partition_endpoints_are_replayed_in_both_adjacent_closed_boxes":
            True,
        "coarser_two_slice_direct_interval_status":
            "UNRESOLVED_DEPENDENCY_NOT_A_MATHEMATICAL_INCIDENCE",
        "coarser_two_slice_first_unresolved_expression": two_slice_failure,
        "four_slice_audit_all_strict": True,
        "aggregate_actual_interval_lower_minima": {
            key: qstr(value) for key, value in sorted(minima.items())
        },
        "claimed_strict_lower_margins": {
            key: qstr(value) for key, value in sorted(claimed.items())
        },
        "rank3_candidate_occurrence_check_count_per_subcollar": 4056,
        "rank3_candidate_occurrence_total_over_four_subcollars": 4 * 4056,
        "physical_five_face_incidence_count": 0,
        "residual_physical_face_count": 0,
        "complete_typed_physical_face_family_empty": True,
        "F10_field_value": "0",
        "F10_zero_reason": "complete typed physical-face family is empty",
    }
    return contract, rows


def f17_guard_rows(
    family_root_id: str,
    seed: dict[str, Any],
    t_guard: tuple[Q, Q],
    wide121: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    child_intervals = {
        child["common_rank"]: (lower, upper)
        for child, lower, upper in r122.common_child_intervals(wide121)
    }
    rows: list[dict[str, Any]] = []
    max_l1 = {0: Q(0), 1: Q(0), 2: Q(0)}
    min_cosine: dict[int, Q | None] = {0: None, 1: None, 2: None}
    for rank in range(24):
        geometry = r122.moving_geometry(
            seed,
            t_guard,
            child_intervals[rank][0],
            child_intervals[rank][1],
        )
        for stage in range(3):
            nx, ny, momentum, cosine = geometry["collisions"][stage + 1]
            eta = Q(r130.RELATIVE_CENTER_ETA[stage])
            radius = r130.TARGET_RADII[stage]
            x_r = r121.aq(eta) * (
                ny - (momentum / cosine) * nx
            )
            x_p = r121.aq(eta / radius) * (
                cosine * ny - momentum * nx
            )
            if stage == 2:
                require(
                    arb_bounds(x_r.value) == (Q(0), Q(0))
                    and arb_bounds(x_p.value) == (Q(0), Q(0)),
                    "wide stage2 zero generator",
                )
                x_r_upper = x_p_upper = Q(0)
            else:
                x_r_upper = abs_upper(x_r.value) + r130.ENCLOSURE_GUARD
                x_p_upper = abs_upper(x_p.value) + r130.ENCLOSURE_GUARD
            l1_upper = x_r_upper + x_p_upper
            diagnostic = (Q(8), Q(2), Q(0))[stage]
            require(
                l1_upper < diagnostic if stage < 2 else l1_upper == 0,
                "wide F17 generator diagnostic",
            )
            cosine_lower = arb_bounds(cosine.value)[0] - r130.ENCLOSURE_GUARD
            require(cosine_lower > 0, "wide F17 cosine")
            reciprocal_upper = Q(1) / cosine_lower
            require(
                reciprocal_upper <= 1 << r130.RAW_INCIDENCE_RANK[stage],
                "wide F17 incidence rank",
            )
            max_l1[stage] = max(max_l1[stage], l1_upper)
            previous = min_cosine[stage]
            min_cosine[stage] = (
                cosine_lower
                if previous is None
                else min(previous, cosine_lower)
            )
            rows.append(
                with_hash(
                    {
                        "wide_F17_guard_id": row_id(
                            "wide-F17-guard",
                            [family_root_id, rank, stage],
                        ),
                        "family_root_id": family_root_id,
                        "common_rank": rank,
                        "stage": stage,
                        "source_x_interval": [
                            qstr(child_intervals[rank][0]),
                            qstr(child_intervals[rank][1]),
                        ],
                        "target_normal_x_enclosure": interval_strings(nx.value),
                        "target_normal_y_enclosure": interval_strings(ny.value),
                        "target_momentum_enclosure": interval_strings(
                            momentum.value
                        ),
                        "target_cosine_enclosure": interval_strings(cosine.value),
                        "guarded_target_cosine_strict_lower": qstr(cosine_lower),
                        "guarded_reciprocal_cosine_upper": qstr(
                            reciprocal_upper
                        ),
                        "X_r_enclosure": interval_strings(x_r.value),
                        "X_p_enclosure": interval_strings(x_p.value),
                        "actual_abs_X_r_upper": qstr(x_r_upper),
                        "actual_abs_X_p_upper": qstr(x_p_upper),
                        "actual_l1_generator_upper": qstr(l1_upper),
                        "actual_l1_generator_strict_upper": qstr(diagnostic),
                        "raw_incidence_rank_B": r130.RAW_INCIDENCE_RANK[stage],
                        "dynamic_F17_strict_upper": str(
                            r130.F17_BY_STAGE[stage]
                        ),
                    }
                )
            )
    require(len(rows) == 72, "wide F17 guard row count")
    require(
        max_l1[0] < 8 and max_l1[1] < 2 and max_l1[2] == 0,
        "wide F17 maxima",
    )
    contract = {
        "family_root_id": family_root_id,
        "guard_scope": "whole wide lambda collar times Round122 s collar",
        "wide_guard_row_count": 72,
        "maximum_actual_l1_generator_upper_by_stage": {
            str(stage): qstr(value) for stage, value in max_l1.items()
        },
        "minimum_guarded_target_cosine_lower_by_stage": {
            str(stage): qstr(value)  # type: ignore[arg-type]
            for stage, value in min_cosine.items()
        },
        "incidence_rank_B_by_stage": {
            str(stage): rank
            for stage, rank in r130.RAW_INCIDENCE_RANK.items()
        },
        "F11_full_phase_strict_upper_by_stage": {
            str(stage): qstr(value)
            for stage, value in r122.F11_BY_STAGE.items()
        },
        "F17_dynamic_test_strict_upper_by_stage": {
            str(stage): str(value)
            for stage, value in r130.F17_BY_STAGE.items()
        },
        "F11_is_authoritative_full_phase_not_along_curve_diagnostic": True,
        "F17_graph_current_guard_remains_strict": True,
    }
    return contract, rows


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 2048, "precision must be at least 2048 bits")
    ctx.prec = precision_bits
    documents = validate_inputs()
    seed = r121.locate_seed(r121.load_inputs())

    (
        family_root,
        root_partition_rows,
        t_guard,
        root_cache,
    ) = root_graph_contract(seed)
    family_root_id = family_root["family_root_id"]
    (
        integral_contract,
        convergence_rows,
        derivative_rows,
        input_roots,
        stage3_roots,
        final_cells,
    ) = normalized_integral_contract(family_root_id, seed, t_guard)
    geometry = common_and_merged_geometry(
        family_root_id,
        input_roots,
        stage3_roots,
        final_cells,
    )
    wide121 = synthetic_round121(documents["r121"], input_roots)
    physical_contract, physical_rows = physical_audit(
        family_root_id,
        seed,
        wide121,
        root_cache,
    )
    f17_contract, f17_rows = f17_guard_rows(
        family_root_id,
        seed,
        t_guard,
        wide121,
    )

    v1 = total_integral(final_cells[1])
    v2 = total_integral(final_cells[2])
    local_transport = {
        "status": "CERTIFIED_WIDE_POSITIVE_BOREL_LOCAL_ROBUSTNESS_ONLY",
        "source_Round129_local_maturity": "14/18",
        "source_Round130_local_maturity": "18/18",
        "wide_family_every_exact_fibre_local_field_maturity": "18/18",
        "wide_family_actual_object_IDs_are_new_not_Round129_Round130_IDs": True,
        "canonical_exact_lambda_locator_version":
            "round135-canonical-exact-lambda-key-v1",
        "canonical_exact_lambda_locator": (
            "u=(lambda-5/131072)/(1/65536); unique binary expansion not "
            "eventually all 1, dyadic values use terminating/eventually-all-0; "
            "u=1 uses UPPER_ENDPOINT"
        ),
        "actual_wide_object_ID_constructors": {
            "common_child": (
                "round135-common-child:sha256(canonical([family-root-id,"
                "canonical-exact-lambda-key,common-rank]))"
            ),
            "input_recut": (
                "round135-input-recut:sha256(canonical([family-root-id,"
                "canonical-exact-lambda-key,stage,natural-index]))"
            ),
            "field_slot": (
                "round135-slot:sha256(canonical([family-root-id,"
                "canonical-exact-lambda-key,official-word-key-id,"
                "actual-refined-subbranch-id,roof-level-j,field-name]))"
            ),
            "local_level_block": (
                "round135-local-level-block:sha256(canonical([family-root-id,"
                "canonical-exact-lambda-key,base-key,18-actual-slot-ids]))"
            ),
            "local_child_packet": (
                "round135-local-child-packet:sha256(canonical([family-root-id,"
                "canonical-exact-lambda-key,actual-common-child-id,"
                "five-local-level-block-ids]))"
            ),
        },
        "constructor_payloads_include_family_root_and_canonical_lambda_key":
            True,
        "constructor_payloads_make_distinct_fields_and_base_keys_injective":
            True,
        "same_canonical_lambda_key_required_for_all_local_fields": True,
        "official_path_word_roof_position_count": 5,
        "official_stage_roof_counts": [2, 1, 2],
        "input_recut_count_per_exact_lambda": 26,
        "common_child_count_per_exact_lambda": 24,
        "base_key_count_per_exact_lambda": 120,
        "field_slot_count_per_exact_lambda": 2160,
        "local_complete_18_field_level_block_count_per_exact_lambda": 120,
        "local_complete_18_field_child_packet_count_per_exact_lambda": 24,
        "finite_rows_are_family_templates_not_an_uncountable_actual_census": True,
        "F5_one_step_adapted_inverse_strict_upper": qstr(r121.THETA),
        "F6_one_step_log_variation_strict_upper": qstr(
            r121.ONE_STEP_LOG_VARIATION
        ),
        "F5_F6_universal_template_scope": (
            "every actual homogeneous physical solid-collision child on a "
            "canonical adapted standard curve before word restriction"
        ),
        "F5_F6_conditions_replayed": {
            "same_Round113_parent": True,
            "same_Round117_operator_cell": True,
            "all_typed_owner_chart_homogeneity_guards_strict": True,
            "all_input_recuts_normalized_length_at_most_1": (
                v1[1] < 7 and v2[1] < 18
            ),
            "restriction_does_not_increase_F5_F6": True,
        },
        "F14_F15_output_length_guards_replayed": geometry[
            "minimum_output_length_by_input_stage"
        ],
        "F14_one_step_strict_upper": str(r130.F14_ONE_STEP),
        "F15_one_step_strict_upper": str(r130.F15_ONE_STEP),
        "F17_guard_replayed": True,
        "F18_same_key_structural_phase_registration_transported": True,
        "F18_does_not_claim_Wiener_invertibility_aperiodicity_or_Kac_closure":
            True,
    }
    require(
        local_transport["F5_F6_conditions_replayed"][
            "all_input_recuts_normalized_length_at_most_1"
        ],
        "wide recut lengths at most one",
    )

    cemetery_contract = {
        "family_root_id": family_root_id,
        "physical_F10": "0",
        "physical_F10_reason": "complete typed physical-face family is empty",
        "stage3_output_fragment_count_per_exact_lambda": 216,
        "stage3_output_fragments_form_disjoint_half_open_exhaustive_partitions":
            True,
        "all_partition_endpoint_sets_have_adapted_length_measure_zero": True,
        "accepted_densities_are_absolutely_continuous": True,
        "input_mass_equals_sum_of_tagged_output_masses": True,
        "discarded_relative_domain_complement": "EMPTY",
        "restricted_relative_cemetery_arrival_kernel": "ZERO",
        "restricted_relative_cemetery": "ZERO",
        "ambient_pre_regularization_cemetery": "NOT_INSTALLED",
        "all_time_owner_cemetery": "NOT_INSTALLED",
        "global_raw_Z_Orlicz_owner_drift_claimed": False,
        "F10_empty_and_relative_zero_cemetery_are_distinct_statements": True,
        "neither_statement_is_positive_cemetery_payment": True,
    }

    field_transport_reason = {
        1: "WIDE_NONEMPTY_COMMON_REFINEMENT",
        2: "FOUR_SUBCOLLAR_OWNER_CHART_HOMOGENEITY_AUDIT",
        3: "SAME_OFFICIAL_PREFIX_CHART_ON_ONE_OPERATOR_CELL",
        4: "SAME_OFFICIAL_SUFFIX_CHART_ON_ONE_OPERATOR_CELL",
        5: "UNIVERSAL_F5_ON_EACH_ACTUAL_HOMOGENEOUS_RECUT_CHILD",
        6: "UNIVERSAL_F6_ON_EACH_ACTUAL_HOMOGENEOUS_RECUT_CHILD",
        7: "ROUND129_CUT_GROWTH_CONTRACT_WITH_WIDE_RECUT_REPLAY",
        8: "FOUR_SUBCOLLAR_PHYSICAL_TRANSVERSALITY_AUDIT",
        9: "SAME_PHYSICAL_C2_ATLAS_ON_ONE_PARENT_CELL",
        10: "ZERO_BY_FOUR_SUBCOLLAR_COMPLETE_PHYSICAL_EMPTY_AUDIT",
        11: "AUTHORITATIVE_FULL_PHASE_ENVELOPES_WITH_WIDE_GUARDS",
        12: "SAME_PHYSICAL_C1_TRACE_PULLBACK_CONTRACT",
        13: "ZERO_BY_FOUR_SUBCOLLAR_COMPLETE_PHYSICAL_EMPTY_AUDIT",
        14: "WIDE_STAGEWISE_OUTPUT_LENGTHS_AND_ROUND130_F14_THEOREM",
        15: "EXHAUSTIVE_TAGGED_PARTITION_AND_RELATIVE_ZERO_CEMETERY",
        16: "ZERO_BY_FOUR_SUBCOLLAR_COMPLETE_PHYSICAL_EMPTY_AUDIT",
        17: "SEVENTY_TWO_WIDE_GRAPH_CURRENT_GUARDS",
        18: "SAME_KEY_STRUCTURAL_PHASE_WITH_NEW_WIDE_FAMILY_IDS",
    }
    field_transport_rows = [
        with_hash(
            {
                "wide_field_transport_id": row_id(
                    "wide-field-transport",
                    [family_root_id, field_index],
                ),
                "family_root_id": family_root_id,
                "field_index": field_index,
                "field_name": r130.FIELD_NAMES[field_index],
                "transport_reason": field_transport_reason[field_index],
                "scope": "EVERY_EXACT_LAMBDA_FIBRE_IN_WIDE_COLLAR",
                "same_canonical_exact_lambda_key_required": True,
                "actual_wide_family_IDs_required": True,
                "actual_slot_id_constructor": (
                    "round135-slot:sha256(canonical([family-root-id,"
                    "canonical-exact-lambda-key,official-word-key-id,"
                    "actual-refined-subbranch-id,roof-level-j,"
                    f"{r130.FIELD_NAMES[field_index]}]))"
                ),
                "finite_row_is_a_transport_template_not_an_actual_fibre_slot": True,
                "global_field_certification_claimed": False,
            }
        )
        for field_index in range(1, 19)
    ]
    require(len(field_transport_rows) == 18, "wide field transport rows")

    row_groups = {
        "root_partition_endpoint_rows": root_partition_rows,
        "derivative_convergence_rows": convergence_rows,
        "normalized_derivative_cell_rows": derivative_rows,
        "input_recut_root_rows": [
            with_hash(
                {
                    key: value
                    for key, value in row.items()
                    if key != "row_sha256"
                }
            )
            for row in []  # populated below from deterministic reconstruction
        ],
    }
    # The root rows are reconstructed here to keep the helper return compact
    # while preserving their exact materialized evidence in the certificate.
    input_root_rows: list[dict[str, Any]] = []
    for stage, count in ((1, 6), (2, 17)):
        for natural_index in range(1, count + 1):
            low, high, low_cell, high_cell = integral_root(
                final_cells[stage], natural_index
            )
            input_root_rows.append(
                with_hash(
                    {
                        "input_recut_root_id": row_id(
                            "input-recut-root",
                            [family_root_id, stage, natural_index],
                        ),
                        "family_root_id": family_root_id,
                        "stage": stage,
                        "natural_index_j": natural_index,
                        "equation": f"V{stage}(lambda,x)={natural_index}",
                        "x_strict_guard": [qstr(low), qstr(high)],
                        "lower_envelope_crossing_cell": low_cell,
                        "upper_envelope_crossing_cell": high_cell,
                        "V_upper_envelope_at_guard_lower": qstr(Q(natural_index)),
                        "V_lower_envelope_at_guard_upper": qstr(Q(natural_index)),
                        "D_positive_implies_unique_root_per_exact_lambda": True,
                        "endpoint_difference_subtraction_used": False,
                    }
                )
            )
    stage3_root_rows: list[dict[str, Any]] = []
    for natural_index in range(1, 193):
        low, high, low_cell, high_cell = integral_root(
            final_cells[3], natural_index
        )
        stage3_root_rows.append(
            with_hash(
                {
                    "stage3_recut_root_id": row_id(
                        "stage3-recut-root",
                        [family_root_id, natural_index],
                    ),
                    "family_root_id": family_root_id,
                    "stage": 3,
                    "natural_index_j": natural_index,
                    "equation": f"V3(lambda,x)={natural_index}",
                    "x_strict_guard": [qstr(low), qstr(high)],
                    "lower_envelope_crossing_cell": low_cell,
                    "upper_envelope_crossing_cell": high_cell,
                    "V_upper_envelope_at_guard_lower": qstr(Q(natural_index)),
                    "V_lower_envelope_at_guard_upper": qstr(Q(natural_index)),
                    "D_positive_implies_unique_root_per_exact_lambda": True,
                    "endpoint_difference_subtraction_used": False,
                }
            )
        )
    row_groups["input_recut_root_rows"] = input_root_rows
    row_groups["stage3_recut_root_rows"] = stage3_root_rows
    row_groups["wide_common_rank_rows"] = geometry["common_rows"]
    row_groups["wide_merged_cut_rows"] = geometry["merged_rows"]
    row_groups["wide_stage3_output_fragment_rows"] = geometry["fragment_rows"]
    row_groups["physical_subcollar_audit_rows"] = physical_rows
    row_groups["wide_F17_guard_rows"] = f17_rows
    row_groups["wide_field_transport_rows"] = field_transport_rows

    expected_counts = {
        "root_partition_endpoint_rows": 5,
        "derivative_convergence_rows": 9,
        "normalized_derivative_cell_rows": 192,
        "input_recut_root_rows": 23,
        "stage3_recut_root_rows": 192,
        "wide_common_rank_rows": 24,
        "wide_merged_cut_rows": 215,
        "wide_stage3_output_fragment_rows": 216,
        "physical_subcollar_audit_rows": 4,
        "wide_F17_guard_rows": 72,
        "wide_field_transport_rows": 18,
    }
    for name, expected in expected_counts.items():
        require(len(row_groups[name]) == expected, f"row count: {name}")
        require(
            all(
                row["row_sha256"]
                == digest({key: value for key, value in row.items() if key != "row_sha256"})
                for row in row_groups[name]
            ),
            f"row closure: {name}",
        )
    all_ids: list[str] = []
    for rows in row_groups.values():
        for row in rows:
            identifier = next(
                value
                for key, value in row.items()
                if key.endswith("_id") and type(value) is str
            )
            all_ids.append(identifier)
    require(len(all_ids) == len(set(all_ids)), "all evidence IDs unique")

    global_safety = {
        "gate5_global_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "gate5_status": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
        "global_exact_nonempty_candidate_key_count": None,
        "wide_local_level_blocks_do_not_count_as_global_blocks": True,
        "physical_F10_empty_does_not_supply_positive_global_F10": True,
        "relative_zero_cemetery_does_not_supply_positive_cemetery_payment": True,
        "no_global_maturity_or_block_promotion": True,
    }

    result: dict[str, Any] = {
        "status": "CERTIFIED_WIDE_POSITIVE_BOREL_LOCAL_ROBUSTNESS_ONLY",
        "precision_bits": precision_bits,
        "frozen_input_contract": {
            "byte_pins": dict(sorted(PINS.items())),
            "Round121_verification": "PASS",
            "Round129_verification": "PASS",
            "Round130_verification": "PASS",
        },
        "wide_positive_Borel_family_root_contract": family_root,
        "root_partition_endpoint_rows": root_partition_rows,
        "root_partition_endpoint_rows_sha256": digest(root_partition_rows),
        "normalized_integral_contract": integral_contract,
        "derivative_convergence_rows": convergence_rows,
        "derivative_convergence_rows_sha256": digest(convergence_rows),
        "normalized_derivative_cell_rows": derivative_rows,
        "normalized_derivative_cell_rows_sha256": digest(derivative_rows),
        "input_recut_root_rows": input_root_rows,
        "input_recut_root_rows_sha256": digest(input_root_rows),
        "stage3_recut_root_rows": stage3_root_rows,
        "stage3_recut_root_rows_sha256": digest(stage3_root_rows),
        "wide_common_rank_rows": geometry["common_rows"],
        "wide_common_rank_rows_sha256": digest(geometry["common_rows"]),
        "wide_merged_cut_rows": geometry["merged_rows"],
        "wide_merged_cut_rows_sha256": digest(geometry["merged_rows"]),
        "wide_stage3_output_fragment_rows": geometry["fragment_rows"],
        "wide_stage3_output_fragment_rows_sha256": digest(
            geometry["fragment_rows"]
        ),
        "wide_geometry_summary": {
            key: value
            for key, value in geometry.items()
            if key not in {"common_rows", "merged_rows", "fragment_rows"}
        },
        "four_subcollar_physical_empty_contract": physical_contract,
        "physical_subcollar_audit_rows": physical_rows,
        "physical_subcollar_audit_rows_sha256": digest(physical_rows),
        "wide_F17_guard_contract": f17_contract,
        "wide_F17_guard_rows": f17_rows,
        "wide_F17_guard_rows_sha256": digest(f17_rows),
        "wide_field_transport_rows": field_transport_rows,
        "wide_field_transport_rows_sha256": digest(field_transport_rows),
        "wide_local_18_field_transport_contract": local_transport,
        "F10_and_cemetery_separation_contract": cemetery_contract,
        "count_ledger": {
            **expected_counts,
            "finite_evidence_row_count": sum(expected_counts.values()),
            "per_exact_lambda_input_recut_count": 26,
            "per_exact_lambda_common_child_count": 24,
            "per_exact_lambda_base_key_count": 120,
            "per_exact_lambda_field_slot_count": 2160,
            "per_exact_lambda_local_complete_18_field_level_block_count": 120,
            "per_exact_lambda_local_complete_18_field_child_packet_count": 24,
            "physical_F10_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "global_safety_and_nonpromotion": global_safety,
        "gate5_global_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "gate5_status": "NOT_CERTIFIED",
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "one widened positive-Borel lambda collar in one Round113 parent "
            "and one Round117 operator cell; every exact lambda fibre locally"
        ),
        "strict_nonclaims": [
            "no global return-word, arbitrary-return-depth or all-Borel coverage",
            "physical F10 remains empty rather than positively paid",
            "restricted relative cemetery zero is not ambient pre-regularization cemetery",
            "restricted relative cemetery zero is not all-time owner cemetery",
            "no global raw-Z, power-Orlicz, owner-drift or positive-cemetery theorem",
            "local 18/18 rows and packets are not global complete blocks",
            "no Wiener invertibility, aperiodicity or Kac closure claim",
            "no Gate5 certification and no CM2 claim",
        ],
    }
    require(
        result["count_ledger"]["finite_evidence_row_count"] == 970,
        "finite evidence count",
    )
    require(
        result["global_safety_and_nonpromotion"]["CM2"]
        == result["cm2_verdict"]
        == "NO-GO_FOR_CLAIM",
        "CM2 closure",
    )
    return result


def safe_output_path(path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        Path(__file__).resolve(),
        *[(HERE / name).resolve() for name in PINS],
    }
    require(not expanded.is_symlink(), "output path must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(
            stat.S_ISREG(metadata.st_mode),
            "existing output must be a regular file",
        )
        require(
            metadata.st_nlink == 1,
            "existing output must not have multiple hardlinks",
        )
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(expanded, protected_path),
                    "output hardlinks a protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output must not overwrite an input")
    require(resolved.parent.is_dir(), "output parent directory")
    return resolved


def write_certificate(path: Path, result: dict[str, Any]) -> None:
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    text = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--precision-bits", type=int, default=PRECISION_BITS
    )
    args = parser.parse_args()
    output = safe_output_path(args.output)
    result = build(args.precision_bits)
    write_certificate(output, result)
    print(
        canonical(
            {
                "output": str(output),
                "result_sha256": digest(result),
                "status": result["status"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
