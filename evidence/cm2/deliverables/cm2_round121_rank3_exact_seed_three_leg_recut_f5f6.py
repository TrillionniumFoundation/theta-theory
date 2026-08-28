#!/usr/bin/env python3
"""Round121: one exact grazing parent-W seed with three materialized recuts.

Round120 installed a Borel-parameterized child registry but deliberately left
the exact-b witnesses and image recuts unmaterialized.  This producer pays that
missing interface on one compact relative-interior seed only.

The stable seed identity is defined by a rational anchor and a unique analytic
root predicate.  Neither the Arb root enclosure nor decimal text participates
in an ID.  The source adapted cell has exact length delta=10^-90.  The first
and second image adapted coordinates have respectively 7 and 18 natural
cells.  Their 6+17 internal cuts pull back to 23 distinct source points and
make 24 genuine common-refinement children.

On each of those children the Round120 F1--F4 slots are restricted to the new
child-refined subbranch ID.  The three actual input recuts then bind the
universal one-step F5/F6 estimates to the same full keys.  This is a
single-exact-seed, child-local 6/18 result; it does not upgrade global Gate5.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
SCHEMA = "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1"
PRECISION_BITS = 1024

ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND117 = HERE / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
ROUND120 = HERE / "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json"
ROUND120_PRODUCER = HERE / "cm2_round120_rank3_relative_interior_actual_standard_curve_recut.py"
ROUND120_MANIFEST = HERE / "cm2-one-hundred-twentieth-direct-assault-manifest-2026-07-23.sha256"
GATE4_COMPONENTWISE = HERE / "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
GATE4_NUMERIC = HERE / "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"

PINS = {
    ROUND120.name: "a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5",
    ROUND120_PRODUCER.name: "ea1b4cd78a8009063e87cfe09b0d3fa80097f430a1f742d5f109761c20973a9a",
    ROUND120_MANIFEST.name: "8666b45917a29cef497f8e053629dc42456c3553e8ec6788860124d1d74c9c3d",
    GATE4_COMPONENTWISE.name: "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691",
    GATE4_NUMERIC.name: "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
}

CLOSED_SCHEMAS = {
    ROUND112.name: "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1",
    ROUND113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    ROUND117.name: "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND120.name: "cm2.round120.rank3-relative-interior-actual-standard-curve-recut.v1",
}

PARENT_ID = "round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
OPERATOR_CELL_ID = "round117-operator-cell:dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1"
EXPECTED_SHEET_ID = "round112-bypass-sheet:82388860fd9a24f85561682533f70ba8789125b13ea29deb027aa3bcb293201f"
EXPECTED_BRANCH = (7, "G[0,0]", "W[-1,-2]", 1)
EXPECTED_OWNERS = ("W[-1,-1]", "G[0,0]", "G[-1,-2]")
EXPECTED_WORDS = (
    "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
    "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
    "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
)
EXPECTED_ROOFS = (2, 1, 2)
ANGULAR_LIFT_ID = "round120-angular-lift:G:W:k0"
EXPECTED_CUT_ORDER = (
    (2, 1), (2, 2), (1, 1), (2, 3), (2, 4), (2, 5),
    (1, 2), (2, 6), (2, 7), (1, 3), (2, 8), (2, 9),
    (2, 10), (1, 4), (2, 11), (2, 12), (1, 5), (2, 13),
    (2, 14), (2, 15), (1, 6), (2, 16), (2, 17),
)

ANCHOR_C0 = Q(1, 16384)
ANCHOR_B3 = Q(3, 65536)
DELTA = Q(1, 10**90)
SOURCE_THETA_COEFFICIENT = Q(25, 61)
SOURCE_PHI_COEFFICIENT = Q(36, 61)
SOURCE_RADIUS = Q(9, 25)
CANONICAL_SLOPE = Q(4)
SOURCE_CURVATURE = Q(25, 9)
SOURCE_ADAPTED_DENSITY = SOURCE_CURVATURE + CANONICAL_SLOPE
THETA = Q(144000, 180337)
ONE_STEP_LOG_VARIATION = Q(3, 200000)
THREE_STEP_THETA = THETA**3
THREE_STEP_LOG_VARIATION = 3 * ONE_STEP_LOG_VARIATION
ROOT_BISECTIONS = 800
CUT_BISECTIONS = 200

GATE5_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def closed_digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(Q(value))


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"float forbidden: {token}")),
    )
    require(type(value) is dict, f"top-level object: {path.name}")
    return value


def load_closed(path: Path) -> dict[str, Any]:
    document = strict_json(path)
    require(set(document) == {"schema", "result", "result_sha256"}, f"closed envelope: {path.name}")
    require(document["schema"] == CLOSED_SCHEMAS[path.name], f"schema: {path.name}")
    require(document["result_sha256"] == closed_digest(document["result"]), f"result digest: {path.name}")
    return document["result"]


def exact_dyadic(point: Any) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def interval_strings(value: arb) -> list[str]:
    lower, upper = arb_pair(value)
    return [qstr(lower), qstr(upper)]


def abs_lower(value: arb, label: str) -> Q:
    lower, upper = arb_pair(value)
    if lower > 0:
        return lower
    if upper < 0:
        return -upper
    raise RuntimeError(f"zero in interval: {label}")


def sin_jet(value: Jet) -> Jet:
    return value.unary(value.value.sin(), value.value.cos(), -value.value.sin())


def cos_jet(value: Jet) -> Jet:
    return value.unary(value.value.cos(), -value.value.sin(), -value.value.cos())


def asin_jet(value: Jet) -> Jet:
    radial = (arb(1) - value.value * value.value).sqrt()
    return value.unary(value.value.asin(), 1 / radial, value.value / (radial * radial * radial))


def load_inputs() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"pin mismatch: {name}")
    values = {
        "r112": load_closed(ROUND112),
        "r113": load_closed(ROUND113),
        "r117": load_closed(ROUND117),
        "r120": load_closed(ROUND120),
        "g4c": strict_json(GATE4_COMPONENTWISE),
        "g4n": strict_json(GATE4_NUMERIC),
    }
    inherited = values["r120"]["upstream_and_helper_pins"]
    require(type(inherited) is dict and len(inherited) >= 30, "Round120 inherited pins")
    for name, expected in inherited.items():
        require(sha256(HERE / name) == expected, f"inherited pin mismatch: {name}")
    require(values["r120"]["rank3_actual_child_field_maturity"] == "4/18", "Round120 maturity")
    require(values["r120"]["gate5_global_maturity"] == "10/18", "Round120 global")
    require(values["r120"]["complete_18_field_block_count"] == 0, "Round120 complete block")
    frontier = values["r120"]["uninstalled_actual_child_F5_F6_frontier"]
    require(
        frontier["universal_template_scope"]
        == (
            "every actual homogeneous physical solid-collision child on a canonical "
            "adapted standard curve; before return-word characteristic restriction"
        ),
        "Round120 universal F5/F6 scope",
    )
    require(Q(frontier["one_step_adapted_inverse_strict_upper"]) == THETA, "Round120 F5 frontier")
    require(Q(frontier["one_step_log_variation_strict_upper"]) == ONE_STEP_LOG_VARIATION, "Round120 F6 frontier")
    require(Q(frontier["three_step_adapted_inverse_strict_upper"]) == THREE_STEP_THETA, "Round120 F5 product")
    require(Q(frontier["three_step_log_variation_strict_upper"]) == THREE_STEP_LOG_VARIATION, "Round120 F6 sum")
    require(frontier["per_leg_per_roof_F5_F6_immutable_slots_installed"] is False, "Round120 slots uninstalled")
    require(frontier["restriction_monotonicity_requires_future_actual_child_and_recut_ID_binding"] is True, "Round120 missing binding")
    require(values["g4c"]["replay_summary"]["homogeneity_cutoff_k0"] == 6121, "Gate4 cutoff")
    require(values["g4c"]["replay_summary"]["global_one_step_Xi_strict_upper"] == "900337/901685", "Gate4 cone")
    require(values["g4n"]["replay_summary"]["global_D_std_strict_upper"] == "30000000", "Gate4 D_std")
    return values


def locate_seed(values: dict[str, Any]) -> dict[str, Any]:
    sheet113 = None
    parent113 = None
    for sheet in values["r113"]["sheet_rows"]:
        for parent in sheet["certified_cells"]:
            if parent["cell_id"] == PARENT_ID:
                sheet113, parent113 = sheet, parent
    require(sheet113 is not None and parent113 is not None, "Round113 seed parent")
    require(sheet113["sheet_id"] == EXPECTED_SHEET_ID, "seed sheet")
    require(tuple(sheet113["branch_key"]) == EXPECTED_BRANCH, "seed branch")

    sheet112 = next(
        (row for row in values["r112"]["sheet_rows"] if row["sheet_id"] == EXPECTED_SHEET_ID),
        None,
    )
    require(sheet112 is not None, "Round112 seed sheet")
    require(sheet112["sheet_kind"] == "BYPASS", "seed kind")
    require(sheet112["source_chart"] == "G:W", "seed source chart")
    require(sheet112["source_grazing_sign_sigma0"] == 1, "seed source sign")
    require(sheet112["uniform_dt_sign"] == -1, "seed uniform partial-t sign")
    require(Q(sheet112["uniform_abs_dt_strict_lower_bound"]) >= 3, "seed uniform partial-t lower")

    row117 = next(
        (row for row in values["r117"]["common_refinement_rows"] if row["parent_round113_cell_id"] == PARENT_ID),
        None,
    )
    require(row117 is not None, "Round117 seed parent")
    generator117 = next(
        (
            row for row in row117["generator_families"]
            if row["stable_id_interface_sample"]["operator_cell_id"] == OPERATOR_CELL_ID
        ),
        None,
    )
    require(generator117 is not None, "Round117 seed operator")
    require(generator117["family"] == "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0", "seed family")
    require(row117["actual_third_collision_owner_id"] == EXPECTED_OWNERS[2], "actual BYPASS winner")
    require(row117["actual_third_collision_homogeneity_label"] == "H0_CENTRAL", "actual winner H0")
    require(row117["bypass_b3_is_collision_angle"] is False, "b3 collision-angle exclusion")
    require(tuple(row117["official_word_key_ids_inherited"]) == EXPECTED_WORDS, "seed words")

    row120 = next(
        (row for row in values["r120"]["child_generator_rows"] if row["parent_round113_cell_id"] == PARENT_ID),
        None,
    )
    require(row120 is not None, "Round120 seed row")
    require(tuple(row120["official_word_key_ids"]) == EXPECTED_WORDS, "Round120 words")
    require(tuple(row120["ordered_owner_ids"]) == EXPECTED_OWNERS, "Round120 owners")
    require(
        row120["canonical_parent_W_leaf"]["angular_lift_id"] == ANGULAR_LIFT_ID,
        "Round120 angular lift ID",
    )
    recut_frontier = row120["three_step_adapted_recut_frontier_schema_rows"]
    require(tuple(row["roof_level_count"] for row in recut_frontier) == EXPECTED_ROOFS, "seed roofs")
    require(tuple(row["stage"] for row in recut_frontier) == (0, 1, 2), "seed stages")

    source = replace(
        core_cert.physical_cores()[EXPECTED_BRANCH[0]],
        chart_id=sheet112["source_chart"],
    )
    return {
        "sheet112": sheet112,
        "sheet113": sheet113,
        "parent113": parent113,
        "row117": row117,
        "generator117": generator117,
        "row120": row120,
        "recut_frontier": recut_frontier,
        "source": source,
    }


def isolate_anchor_root(seed: dict[str, Any]) -> tuple[Q, Q, int, int]:
    t_lower, t_upper = map(Q, seed["sheet112"]["enclosing_parameter_box"]["t"])
    source = seed["source"]
    lower_sign = strict_sign(round113.equation_value(
        source, EXPECTED_BRANCH, 1, "BYPASS",
        t_lower, ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
    ))
    upper_sign = strict_sign(round113.equation_value(
        source, EXPECTED_BRANCH, 1, "BYPASS",
        t_upper, ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
    ))
    require(lower_sign * upper_sign == -1, "anchor root bracket signs")
    low, high = t_lower, t_upper
    for _ in range(ROOT_BISECTIONS):
        middle = (low + high) / 2
        sign = strict_sign(round113.equation_value(
            source, EXPECTED_BRANCH, 1, "BYPASS",
            middle, ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
        ))
        require(sign != 0, "anchor root bisection sign")
        if sign == lower_sign:
            low = middle
        else:
            high = middle
    require(high - low < Q(1, 10**220), "anchor root bracket width")
    require(strict_sign(round113.equation_value(
        source, EXPECTED_BRANCH, 1, "BYPASS",
        low, ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
    )) == lower_sign, "anchor lower sign")
    require(strict_sign(round113.equation_value(
        source, EXPECTED_BRANCH, 1, "BYPASS",
        high, ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
    )) == upper_sign, "anchor upper sign")
    return low, high, lower_sign, upper_sign


def seed_id() -> str:
    payload = [
        "round121-exact-parent-W-v1",
        PARENT_ID,
        OPERATOR_CELL_ID,
        ANGULAR_LIFT_ID,
        "c0=1/16384",
        "b3=3/65536",
        "unique-root:F_BYPASS(t,c0,b3)=0",
    ]
    return "round121-exact-parent-W:" + closed_digest(payload)


def raw_state(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    x_lower: Q,
    x_upper: Q,
) -> dict[str, Any]:
    t_star = interval(*root_bracket)
    theta_star = arb.pi() - t_star.asin()
    phi_star = aq(ANCHOR_C0).acos()
    x = Jet.variable(interval(x_lower, x_upper), 0)
    theta0 = Jet(theta_star) + aq(SOURCE_THETA_COEFFICIENT * DELTA) * x
    phi0 = Jet(phi_star) + aq(SOURCE_PHI_COEFFICIENT * DELTA) * x
    t = sin_jet(theta0)
    c0 = cos_jet(phi0)
    normal0_x, normal0_y = normal("W", t)
    p0 = (arb(1) - c0 * c0).sqrt()
    velocity0_x = c0 * normal0_x - p0 * normal0_y
    velocity0_y = c0 * normal0_y + p0 * normal0_x

    zero = Jet(arb(0))
    source_x, source_y = center("G[0,0]", zero)
    point0_x = source_x + aq(SOURCE_RADIUS) * normal0_x
    point0_y = source_y + aq(SOURCE_RADIUS) * normal0_y

    first_x, first_y = center(seed["source"].target_id, zero)
    first = round112.collision_diagnostic(
        point0_x, point0_y, velocity0_x, velocity0_y,
        first_x, first_y, round112.radius(seed["source"].target_id),
    )
    c1 = (arb(1) - first["momentum"] * first["momentum"]).sqrt()
    velocity1_x = c1 * first["normal_x"] - first["momentum"] * first["normal_y"]
    velocity1_y = c1 * first["normal_y"] + first["momentum"] * first["normal_x"]

    second_x, second_y = center(EXPECTED_BRANCH[1], zero)
    second = round112.collision_diagnostic(
        first["hit_x"], first["hit_y"], velocity1_x, velocity1_y,
        second_x, second_y, round112.radius(EXPECTED_BRANCH[1]),
    )
    c2 = (arb(1) - second["momentum"] * second["momentum"]).sqrt()
    velocity2_x = c2 * second["normal_x"] - second["momentum"] * second["normal_y"]
    velocity2_y = c2 * second["normal_y"] + second["momentum"] * second["normal_x"]

    designated_x, designated_y = center(EXPECTED_BRANCH[2], zero)
    dx = designated_x - second["hit_x"]
    dy = designated_y - second["hit_y"]
    transverse3 = -velocity2_y * dx + velocity2_x * dy
    radius3 = aq(round112.radius(EXPECTED_BRANCH[2]))
    delta3 = radius3 * radius3 - transverse3 * transverse3
    b3 = (-delta3).sqrt() / radius3

    actual_state = (
        second["hit_x"], second["hit_y"], velocity2_x, velocity2_y,
    )
    actual_third = round113.candidate_geometry(actual_state, EXPECTED_OWNERS[2])
    require(actual_third["classification"] == "STRICT_FUTURE_NEAR_ROOT", "actual BYPASS third")
    actual_third_momentum = actual_third["transverse"] / aq(round112.radius(EXPECTED_OWNERS[2]))

    # The certified collision charts on the two image inputs are N and S.
    adapted1 = Jet(arb.pi() / 2) - asin_jet(first["normal_x"]) + asin_jet(first["momentum"])
    adapted2 = -Jet(arb.pi() / 2) + asin_jet(second["normal_x"]) + asin_jet(second["momentum"])
    return {
        "x": x,
        "theta0": theta0,
        "phi0": phi0,
        "t": t,
        "c0": c0,
        "b3": b3,
        "first": first,
        "second": second,
        "actual_third": actual_third,
        "actual_third_momentum": actual_third_momentum,
        "adapted1": adapted1,
        "adapted2": adapted2,
    }


def adapted_data(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
) -> dict[str, Any]:
    at_zero = raw_state(seed, root_bracket, Q(0), Q(0))
    at_one = raw_state(seed, root_bracket, Q(1), Q(1))
    whole = raw_state(seed, root_bracket, Q(0), Q(1))
    require(
        SOURCE_PHI_COEFFICIENT
        == CANONICAL_SLOPE * SOURCE_RADIUS * SOURCE_THETA_COEFFICIENT,
        "slope-four source coefficient identity",
    )
    require(
        SOURCE_ADAPTED_DENSITY * SOURCE_RADIUS * SOURCE_THETA_COEFFICIENT == 1,
        "exact source adapted-coordinate identity",
    )
    adapted1_zero = at_zero["adapted1"].value
    adapted2_zero = at_zero["adapted2"].value
    length1 = adapted1_zero - at_one["adapted1"].value
    length2 = at_one["adapted2"].value - adapted2_zero
    length1_ratio = length1 / aq(DELTA)
    length2_ratio = length2 / aq(DELTA)
    derivative1_ratio = -whole["adapted1"].gradient[0] / aq(DELTA)
    derivative2_ratio = whole["adapted2"].gradient[0] / aq(DELTA)
    c0_derivative_ratio = whole["c0"].gradient[0] / aq(DELTA)
    b3_derivative_ratio = whole["b3"].gradient[0] / aq(DELTA)
    require(bool(length1_ratio > 6) and bool(length1_ratio < 7), "stage1 length ratio")
    require(bool(length2_ratio > 17) and bool(length2_ratio < 18), "stage2 length ratio")
    require(bool(length1_ratio > aq(Q(34, 5))), "stage1 terminal cell length")
    require(bool(length2_ratio > aq(Q(87, 5))), "stage2 terminal cell length")
    require(bool(derivative1_ratio > 6) and bool(derivative1_ratio < 7), "stage1 derivative ratio")
    require(bool(derivative2_ratio > 17) and bool(derivative2_ratio < 18), "stage2 derivative ratio")
    require(strict_sign(whole["c0"].gradient[0]) == -1, "source c0 endpoint monotonicity")
    require(strict_sign(whole["b3"].gradient[0]) == -1, "source b3 endpoint monotonicity")

    c0_lower = arb_pair(at_one["c0"].value)[0]
    b3_lower = arb_pair(at_one["b3"].value)[0]
    require(Q(3, 65536) < c0_lower < ANCHOR_C0, "source c0 interior")
    h128_boundary = aq(Q(1, 128**2)).sin()
    h128_margin = aq(c0_lower) - h128_boundary
    require(bool(h128_margin > 0), "source H0_CENTRAL_OUTER lower boundary")
    require(Q(1, 32768) < b3_lower < ANCHOR_B3, "source b3 interior")
    require(bool(at_zero["b3"].value.contains(aq(ANCHOR_B3))), "anchor b3 replay")
    require(bool(whole["actual_third"]["near"].value > 0), "actual third future")
    require(bool(abs(whole["actual_third_momentum"].value) < 1), "actual third momentum")

    pair_index, pattern_index, _registry_digest = component.key_index_tables()
    replay = round113.audit_cell(
        seed["sheet112"], seed["source"], EXPECTED_BRANCH,
        c0_lower, ANCHOR_C0, b3_lower, ANCHOR_B3,
        pair_index, pattern_index,
    )
    require(tuple(replay["ordered_regular_relative_interior_owner_ids"]) == EXPECTED_OWNERS, "whole-cell owners")
    require(tuple(replay["official_word_key_ids"]) == EXPECTED_WORDS, "whole-cell words")
    require(replay["official_path_id"] == seed["parent113"]["official_path_id"], "whole-cell path")
    require(
        tuple(row["selected_collision_chart"] for row in replay["leg_audits"]) == ("N", "S", "N"),
        "whole-cell collision charts",
    )

    return {
        "zero": at_zero,
        "one": at_one,
        "whole": whole,
        "adapted1_zero": adapted1_zero,
        "adapted2_zero": adapted2_zero,
        "length1": length1,
        "length2": length2,
        "length1_ratio": length1_ratio,
        "length2_ratio": length2_ratio,
        "derivative1_ratio": derivative1_ratio,
        "derivative2_ratio": derivative2_ratio,
        "c0_derivative_ratio": c0_derivative_ratio,
        "b3_derivative_ratio": b3_derivative_ratio,
        "source_c0_lower": c0_lower,
        "source_h128_boundary": h128_boundary,
        "source_h128_margin": h128_margin,
        "source_b3_lower": b3_lower,
        "replay": replay,
        "slope_four_intercept_enclosure": (
            whole["phi0"] - aq(CANONICAL_SLOPE * SOURCE_RADIUS) * whole["theta0"]
        ).value,
    }


def u_value(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    adapted: dict[str, Any],
    stage: int,
    x: Q,
) -> arb:
    state = raw_state(seed, root_bracket, x, x)
    if stage == 1:
        return adapted["adapted1_zero"] - state["adapted1"].value
    require(stage == 2, "image stage")
    return state["adapted2"].value - adapted["adapted2_zero"]


def boundary_id(which: str, exact_seed_id: str) -> str:
    require(which in {"left", "right"}, "source boundary")
    return f"round121-source-{which}-endpoint:" + closed_digest(
        ["round121-source-boundary-v1", exact_seed_id, which],
    )


def isolate_pullback_endpoints(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    adapted: dict[str, Any],
    exact_seed_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stage, count in ((1, 6), (2, 17)):
        derivative_lower = Q(6) if stage == 1 else Q(17)
        for natural_index in range(1, count + 1):
            low, high = Q(0), Q(1)
            target = aq(natural_index * DELTA)
            left_sign = strict_sign(u_value(seed, root_bracket, adapted, stage, low) - target)
            right_sign = strict_sign(u_value(seed, root_bracket, adapted, stage, high) - target)
            require((left_sign, right_sign) == (-1, 1), "pullback endpoint outer signs")
            for _ in range(CUT_BISECTIONS):
                middle = (low + high) / 2
                sign = strict_sign(u_value(seed, root_bracket, adapted, stage, middle) - target)
                require(sign != 0, "pullback endpoint bisection sign")
                if sign < 0:
                    low = middle
                else:
                    high = middle
            require(high - low == Q(1, 2**CUT_BISECTIONS), "pullback bracket width")
            state = raw_state(seed, root_bracket, low, high)
            endpoint_payload = [
                "round121-pullback-endpoint-v1",
                exact_seed_id,
                f"U{stage}(x)={natural_index}*delta",
                stage,
                natural_index,
            ]
            endpoint_id = "round121-pullback-endpoint:" + closed_digest(endpoint_payload)
            row = {
                "endpoint_id": endpoint_id,
                "exact_parent_W_seed_id": exact_seed_id,
                "stage": stage,
                "natural_index_j": natural_index,
                "exact_root_equation_id": f"round121-U{stage}-equals-{natural_index}-delta",
                "exact_root_equation": f"U{stage}(x)={natural_index}*10^-90",
                "x_dyadic_bracket": [qstr(low), qstr(high)],
                "x_bracket_width_upper": qstr(Q(1, 2**CUT_BISECTIONS)),
                "left_function_sign": -1,
                "right_function_sign": 1,
                "derivative_sign": 1,
                "normalized_derivative_abs_strict_lower": qstr(derivative_lower),
                "unique_root_certified": True,
                "source_c0_enclosure": interval_strings(state["c0"].value),
                "source_t_enclosure": interval_strings(state["t"].value),
                "source_b3_enclosure": interval_strings(state["b3"].value),
                "lower_owner": f"stage-{stage}-natural-cell-{natural_index - 1}",
                "upper_owner": f"stage-{stage}-natural-cell-{natural_index}",
                "numeric_bracket_or_Arb_text_participates_in_endpoint_ID": False,
            }
            row["evidence_sha256"] = closed_digest(row)
            rows.append(row)
    rows.sort(key=lambda row: (Q(row["x_dyadic_bracket"][0]), row["stage"], row["natural_index_j"]))
    require(
        tuple((row["stage"], row["natural_index_j"]) for row in rows) == EXPECTED_CUT_ORDER,
        "pullback endpoint order",
    )
    for left, right in zip(rows, rows[1:]):
        separation = Q(right["x_dyadic_bracket"][0]) - Q(left["x_dyadic_bracket"][1])
        require(separation > Q(1, 200), "pullback endpoint separation")
    return rows


def recut_instance_id(exact_seed_id: str, stage: int, natural_index: int) -> str:
    return "round121-recut-instance:" + closed_digest([
        "round121-materialized-adapted-input-recut-v1",
        exact_seed_id,
        stage,
        natural_index,
    ])


def stage_recut_rows(
    exact_seed_id: str,
    endpoint_rows: list[dict[str, Any]],
    adapted: dict[str, Any],
) -> list[dict[str, Any]]:
    index = {(row["stage"], row["natural_index_j"]): row for row in endpoint_rows}
    left_boundary = boundary_id("left", exact_seed_id)
    right_boundary = boundary_id("right", exact_seed_id)
    rows: list[dict[str, Any]] = []
    counts = (1, 7, 18)
    for stage, count in enumerate(counts):
        for natural_index in range(count):
            lower_endpoint = (
                left_boundary if natural_index == 0
                else index[(stage, natural_index)]["endpoint_id"]
            )
            upper_endpoint = (
                right_boundary if natural_index == count - 1
                else index[(stage, natural_index + 1)]["endpoint_id"]
            )
            if stage == 0:
                adapted_lower = "0"
                adapted_upper = "1e-90"
                normalized_length_lower = Q(9, 10)
            else:
                adapted_lower = f"{natural_index}e-90"
                adapted_upper = (
                    f"{natural_index + 1}e-90"
                    if natural_index < count - 1
                    else f"U{stage}(1)"
                )
                normalized_length_lower = Q(9, 10)
                if natural_index == count - 1:
                    normalized_length_lower = Q(4, 5) if stage == 1 else Q(2, 5)
            stage_word = EXPECTED_WORDS[stage]
            row = {
                "recut_instance_id": recut_instance_id(exact_seed_id, stage, natural_index),
                "exact_parent_W_seed_id": exact_seed_id,
                "stage": stage,
                "natural_index_j": natural_index,
                "adapted_coordinate_id": (
                    "source-u0-exact-delta-x" if stage == 0 else f"image-U{stage}"
                ),
                "adapted_lower": adapted_lower,
                "adapted_upper": adapted_upper,
                "adapted_length_upper": "1e-90",
                "normalized_adapted_length_strict_lower": qstr(normalized_length_lower),
                "lower_endpoint_id": lower_endpoint,
                "upper_endpoint_id": upper_endpoint,
                "lower_closed": True,
                "upper_closed": False,
                "source_parent_right_endpoint_is_open": True,
                "internal_cut_owned_by_right_natural_cell": True,
                "official_word_key_id": stage_word,
                "roof_level_count": EXPECTED_ROOFS[stage],
                "actual_materialized_input_recut": True,
            }
            row["row_sha256"] = closed_digest(row)
            rows.append(row)
    require(len(rows) == 26, "stage recut row count")
    return rows


def common_refinement(
    exact_seed_id: str,
    endpoints: list[dict[str, Any]],
    stage_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    left_boundary = boundary_id("left", exact_seed_id)
    right_boundary = boundary_id("right", exact_seed_id)
    boundaries: list[dict[str, Any]] = [{
        "endpoint_id": left_boundary,
        "x_dyadic_bracket": ["0", "0"],
        "stage": 0,
        "natural_index_j": 0,
    }, *endpoints, {
        "endpoint_id": right_boundary,
        "x_dyadic_bracket": ["1", "1"],
        "stage": 0,
        "natural_index_j": 1,
    }]
    recut_index = {
        (row["stage"], row["natural_index_j"]): row["recut_instance_id"]
        for row in stage_rows
    }
    stage_indices = [0, 0, 0]
    common_rows: list[dict[str, Any]] = []
    refined_rows: list[dict[str, Any]] = []
    for rank, (lower, upper) in enumerate(zip(boundaries, boundaries[1:])):
        separation = Q(upper["x_dyadic_bracket"][0]) - Q(lower["x_dyadic_bracket"][1])
        require(separation > Q(1, 200), "common child positive length")
        refined_payload = [
            "round121-refined-subbranch-v1",
            OPERATOR_CELL_ID,
            exact_seed_id,
            "source-k=0",
            rank,
        ]
        refined_id = "round121-refined-subbranch:" + closed_digest(refined_payload)
        child_payload = [
            "round121-common-child-v1",
            refined_id,
            exact_seed_id,
            rank,
        ]
        child_id = "round121-common-child:" + closed_digest(child_payload)
        common_row = {
            "common_rank": rank,
            "common_child_id": child_id,
            "refined_homogeneous_subbranch_id": refined_id,
            "source_x_lower_endpoint_id": lower["endpoint_id"],
            "source_x_upper_endpoint_id": upper["endpoint_id"],
            "lower_closed": True,
            "upper_closed": False,
            "source_parent_right_endpoint_is_open": True,
            "covering_stage_indices": list(stage_indices),
            "source_recut_instance_id": recut_index[(0, 0)],
            "first_image_recut_instance_id": recut_index[(1, stage_indices[1])],
            "second_image_recut_instance_id": recut_index[(2, stage_indices[2])],
            "all_three_inputs_contained_in_one_materialized_canonical_cell": True,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "official_path_id": "gate5-rank3-endpoint-sheet-path:9f335e832599b906ffef1f29b1751e5250309a48501b948598115a92ac44b5f7",
            "positive_source_x_length_strict_lower": "1/200",
            "actual_standard_curve_child_installed": True,
        }
        common_row["row_sha256"] = closed_digest(common_row)
        common_rows.append(common_row)
        refined_row = {
            "refined_homogeneous_subbranch_id": refined_id,
            "common_child_id": child_id,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "exact_parent_W_seed_id": exact_seed_id,
            "source_adapted_index_k": 0,
            "common_rank": rank,
            "physical_homogeneity": {
                "source": "H0_CENTRAL_OUTER",
                "collision_1": "H0_CENTRAL",
                "collision_2": "H0_CENTRAL",
                "actual_BYPASS_collision_3": "H0_CENTRAL",
                "designated_b3_is_a_collision_angle": False,
            },
        }
        refined_row["row_sha256"] = closed_digest(refined_row)
        refined_rows.append(refined_row)
        crossed = upper
        if rank < len(endpoints):
            require(crossed["stage"] in (1, 2), "internal cut stage")
            stage_indices[crossed["stage"]] += 1
    require(stage_indices == [0, 6, 17], "terminal natural indices")
    require(len(common_rows) == len(refined_rows) == 24, "common refinement count")
    return common_rows, refined_rows


def slot_rows(
    seed: dict[str, Any],
    common_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for child in common_rows:
        refined_id = child["refined_homogeneous_subbranch_id"]
        stage_recuts = (
            child["source_recut_instance_id"],
            child["first_image_recut_instance_id"],
            child["second_image_recut_instance_id"],
        )
        for frontier in seed["recut_frontier"]:
            stage = frontier["stage"]
            for chart_pair in frontier["roof_level_chart_pairs"]:
                roof_level = chart_pair["roof_level_j"]
                require(0 <= roof_level < frontier["roof_level_count"], "roof level")
                for field_index, field_name in enumerate(GATE5_FIELDS, start=1):
                    if field_index == 1:
                        value = "NONEMPTY_POSITIVE_LENGTH_COMMON_REFINEMENT_INTERVAL"
                    elif field_index == 2:
                        value = (
                            "source=H0_CENTRAL_OUTER; collision1=H0_CENTRAL; "
                            "collision2=H0_CENTRAL; actual-BYPASS-collision3=H0_CENTRAL"
                        )
                    elif field_index == 3:
                        value = chart_pair["prefix_chart"]
                    elif field_index == 4:
                        value = chart_pair["suffix_chart"]
                    elif field_index == 5:
                        value = qstr(THETA)
                    else:
                        value = qstr(ONE_STEP_LOG_VARIATION)
                    key = [
                        frontier["official_word_key_id"],
                        refined_id,
                        roof_level,
                        field_name,
                    ]
                    row = {
                        "slot_id": "round121-gate5-slot:" + closed_digest(key),
                        "immutable_slot_key": key,
                        "official_word_key_id": frontier["official_word_key_id"],
                        "refined_homogeneous_subbranch_id": refined_id,
                        "common_child_id": child["common_child_id"],
                        "stage": stage,
                        "roof_level_j": roof_level,
                        "field_index": field_index,
                        "field_name": field_name,
                        "field_value_or_contract": value,
                        "materialized_input_recut_instance_id": stage_recuts[stage],
                        "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
                        "transparent_wall_roof_split_does_not_add_a_collision_Jacobian_factor": (
                            frontier["roof_level_count"] == 2
                        ),
                    }
                    rows.append(row)
    require(len(rows) == 720, "slot count")
    require(len({row["slot_id"] for row in rows}) == 720, "slot IDs")
    for field_index in range(1, 7):
        require(sum(row["field_index"] == field_index for row in rows) == 120, f"F{field_index} count")
    return rows


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 1024, "precision must be at least 1024 bits")
    ctx.prec = precision_bits
    values = load_inputs()
    seed = locate_seed(values)
    root_low, root_high, root_lower_sign, root_upper_sign = isolate_anchor_root(seed)
    exact_seed_id = seed_id()
    anchor_geometry = round113.path_geometry(
        seed["source"], EXPECTED_BRANCH, 1, "BYPASS",
        root_low, root_high,
        ANCHOR_C0, ANCHOR_C0, ANCHOR_B3, ANCHOR_B3,
    )
    anchor_partial_t = anchor_geometry["equation"].gradient[0]
    anchor_partial_t_sign = strict_sign(anchor_partial_t)
    require(anchor_partial_t_sign != 0, "anchor partial-t nonzero")
    require(anchor_partial_t_sign == seed["parent113"]["uniform_dt_sign"], "anchor partial-t inherited sign")
    require(abs_lower(anchor_partial_t, "anchor partial-t") > 3, "anchor partial-t strict lower")
    adapted = adapted_data(seed, (root_low, root_high))
    endpoint_rows = isolate_pullback_endpoints(
        seed, (root_low, root_high), adapted, exact_seed_id,
    )
    recut_rows = stage_recut_rows(exact_seed_id, endpoint_rows, adapted)
    common_rows, refined_rows = common_refinement(exact_seed_id, endpoint_rows, recut_rows)
    slots = slot_rows(seed, common_rows)

    theta_star = arb.pi() - interval(root_low, root_high).asin()
    b_star = aq(ANCHOR_C0).acos() - aq(Q(36, 25)) * theta_star
    require(tuple((row["stage"], row["natural_index_j"]) for row in endpoint_rows) == EXPECTED_CUT_ORDER, "cut order")

    inherited_pins = dict(values["r120"]["upstream_and_helper_pins"])
    all_pins = {**inherited_pins, **PINS}
    require(len(all_pins) == len(set(all_pins)), "pin keys")
    result = {
        "precision_bits": precision_bits,
        "exact_seed_contract": {
            "exact_parent_W_seed_id": exact_seed_id,
            "round113_parent_id": PARENT_ID,
            "round117_operator_cell_id": OPERATOR_CELL_ID,
            "round117_family": "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0",
            "sheet_kind": "BYPASS",
            "branch_key": list(EXPECTED_BRANCH),
            "source_chart": "G:W",
            "source_grazing_sign_sigma0": 1,
            "actual_third_owner_id": EXPECTED_OWNERS[2],
            "anchor": {"c0": qstr(ANCHOR_C0), "b3": qstr(ANCHOR_B3)},
            "root_identity_predicate": "the unique t in the frozen Round112 enclosure with F_BYPASS(t,1/16384,3/65536)=0",
            "angular_lift_id": ANGULAR_LIFT_ID,
            "intercept_definition": "b*=arccos(1/16384)-(36/25)*(pi-arcsin(t*))",
            "stable_ID_payload_uses_only_parent_operator_rational_anchor_root_predicate_and_lift": True,
            "Arb_decimal_or_numeric_bracket_participates_in_ID": False,
        },
        "exact_parent_W_witness_rows": [{
            "exact_parent_W_seed_id": exact_seed_id,
            "anchor_t_unique_root_dyadic_bracket": [qstr(root_low), qstr(root_high)],
            "anchor_t_bracket_width_strict_upper": qstr(Q(1, 10**220)),
            "anchor_root_face_signs": [root_lower_sign, root_upper_sign],
            "anchor_root_partial_t_nonzero_and_unique": True,
            "anchor_root_partial_t_sign": anchor_partial_t_sign,
            "anchor_root_partial_t_abs_strict_lower": "3",
            "inherited_parent_uniform_partial_t_sign": seed["parent113"]["uniform_dt_sign"],
            "theta_star_enclosure": interval_strings(theta_star),
            "b_star_enclosure": interval_strings(b_star),
            "b_star_is_an_exact_analytic_real_not_the_enclosure_text": True,
            "materialized_exact_b_witness": True,
        }],
        "source_adapted_cell_rows": [{
            "source_recut_instance_id": recut_instance_id(exact_seed_id, 0, 0),
            "source_adapted_index_k": 0,
            "source_parameter_domain": "[0,1)",
            "delta": "1e-90",
            "source_adapted_coordinate": "u0(x)=delta*x",
            "source_adapted_length_exact": "1e-90",
            "source_adapted_density": qstr(SOURCE_ADAPTED_DENSITY),
            "source_adapted_coordinate_identity": "(25/9+4)*(9/25)*(25/61)=1",
            "u0_x_derivative_exact": "1e-90",
            "theta0": "theta*+(25/61)*delta*x",
            "phi0": "arccos(1/16384)+(36/61)*delta*x",
            "t": "sin(theta0)",
            "c0": "cos(phi0)",
            "b3": "sqrt(-Delta3(t,c0))/(4/25)",
            "coefficient_identity": "(36/61)=(36/25)*(25/61)=4*(9/25)*(25/61)",
            "slope_four_parent_W_identity": "phi0(x)-4*(9/25)*theta0(x)=b* on the whole cell",
            "slope_four_intercept_enclosure": interval_strings(
                adapted["slope_four_intercept_enclosure"],
            ),
            "p0_equals_sin_4r_plus_b_star_whole_cell": True,
            "c0_enclosure": [qstr(adapted["source_c0_lower"]), qstr(ANCHOR_C0)],
            "c0_x_derivative_sign": -1,
            "c0_x_derivative_over_delta_enclosure": interval_strings(
                adapted["c0_derivative_ratio"],
            ),
            "H128_upper_boundary_sin_128_minus_2_enclosure": interval_strings(
                adapted["source_h128_boundary"],
            ),
            "c0_minus_H128_upper_boundary_strict_lower": qstr(
                arb_pair(adapted["source_h128_margin"])[0] / 2,
            ),
            "source_H0_CENTRAL_OUTER_membership_whole_cell": True,
            "b3_enclosure": [qstr(adapted["source_b3_lower"]), qstr(ANCHOR_B3)],
            "b3_x_derivative_sign": -1,
            "b3_x_derivative_over_delta_enclosure": interval_strings(
                adapted["b3_derivative_ratio"],
            ),
            "within_R113_R117_regular_relative_interior": True,
            "right_endpoint_closed": False,
        }],
        "stage_adapted_coordinate_contract": {
            "stage_0": "u0(x)=delta*x",
            "stage_1": "a1=Theta_N(n1)+asin(p1); U1(x)=a1(0)-a1(x)",
            "stage_2": "a2=Theta_S(n2)+asin(p2); U2(x)=a2(x)-a2(0)",
            "stage_orientations": [1, -1, 1],
            "stage_length_ratio_enclosures": {
                "U1_1_over_delta": interval_strings(adapted["length1_ratio"]),
                "U2_1_over_delta": interval_strings(adapted["length2_ratio"]),
            },
            "strict_simple_length_bounds": ["6<U1(1)/delta<7", "17<U2(1)/delta<18"],
            "whole_cell_normalized_derivative_enclosures": {
                "U1_prime_over_delta": interval_strings(adapted["derivative1_ratio"]),
                "U2_prime_over_delta": interval_strings(adapted["derivative2_ratio"]),
            },
            "whole_cell_strict_monotonicity": True,
            "adapted_coordinate_uses_both_normal_angle_and_momentum_angle": True,
        },
        "pullback_endpoint_rows": endpoint_rows,
        "pullback_endpoint_rows_sha256": closed_digest(endpoint_rows),
        "stage_recut_rows": recut_rows,
        "stage_recut_rows_sha256": closed_digest(recut_rows),
        "common_refinement_rows": common_rows,
        "common_refinement_rows_sha256": closed_digest(common_rows),
        "refined_homogeneous_subbranch_rows": refined_rows,
        "refined_homogeneous_subbranch_rows_sha256": closed_digest(refined_rows),
        "gate5_F1_F6_slot_rows": slots,
        "gate5_F1_F6_slot_rows_sha256": closed_digest(slots),
        "three_leg_restriction_theorem": {
            "actual_input_stage_count": 3,
            "each_Ti_child_inside_one_materialized_adapted_natural_cell": True,
            "each_materialized_adapted_cell_length_at_most_delta": True,
            "invariant_cone_strict_forward_invariance": True,
            "global_D_std_strict_upper": "30000000",
            "universal_one_step_F5_adapted_inverse_strict_upper": qstr(THETA),
            "universal_one_step_F6_log_variation_strict_upper": qstr(ONE_STEP_LOG_VARIATION),
            "restriction_does_not_increase_pointwise_inverse_upper": True,
            "restriction_does_not_increase_log_Jacobian_oscillation": True,
            "transparent_wall_roof_levels_are_prefix_suffix_splits_of_one_collision_leg": True,
            "transparent_wall_roof_levels_do_not_add_Jacobian_factors": True,
            "three_leg_F5_path_product_strict_upper": qstr(THREE_STEP_THETA),
            "three_leg_F6_path_sum_strict_upper": qstr(THREE_STEP_LOG_VARIATION),
            "area_Jacobian_one_used_as_F5": False,
            "full_key_child_restriction_binding_installed": True,
            "Round120_frontier_missing_actual_recut_and_full_key_binding_paid_here": True,
            "Round120_universal_template_scope_replayed": (
                values["r120"]["uninstalled_actual_child_F5_F6_frontier"][
                    "universal_template_scope"
                ]
            ),
        },
        "count_ledger": {
            "exact_b_seed_count": 1,
            "source_natural_cell_count": 1,
            "first_image_natural_cell_count": 7,
            "second_image_natural_cell_count": 18,
            "stage_recut_row_count": len(recut_rows),
            "first_image_internal_cut_count": 6,
            "second_image_internal_cut_count": 17,
            "pullback_internal_cut_count": len(endpoint_rows),
            "common_refinement_actual_child_count": len(common_rows),
            "refined_homogeneous_subbranch_count": len(refined_rows),
            "official_word_roof_level_counts": list(EXPECTED_ROOFS),
            "roof_level_count_per_refined_subbranch": sum(EXPECTED_ROOFS),
            "slot_count_per_field": 120,
            "F1_F4_slot_count": 480,
            "F5_slot_count": 120,
            "F6_slot_count": 120,
            "F1_F6_total_slot_count": len(slots),
            "residual_root_count": 0,
            "residual_recut_count": 0,
            "residual_slot_count": 0,
        },
        "boundary_owner_ledger": {
            "source_cell": "[0,1); right endpoint is not the last cell in the Borel fibre",
            "image_parent_right_endpoint_open": True,
            "every_internal_natural_cut_owned_by_the_right_cell": True,
            "common_refinement_cells": "[cut_rank,cut_rank+1) in source orientation",
            "coincident_artificial_cuts_use_conjunction_of_owner_predicates": True,
            "natural_c0_zero_b3_zero_boundaries_remain_singular_ledger": True,
            "this_seed_is_strictly_separated_from_c0_zero_and_b3_zero": True,
        },
        "whole_seed_owner_candidate_replay": {
            "ordered_owner_ids": adapted["replay"]["ordered_regular_relative_interior_owner_ids"],
            "official_word_key_ids": adapted["replay"]["official_word_key_ids"],
            "official_path_id": adapted["replay"]["official_path_id"],
            "selected_collision_charts": [
                row["selected_collision_chart"] for row in adapted["replay"]["leg_audits"]
            ],
            "BYPASS_actual_third_owner_id": EXPECTED_OWNERS[2],
            "BYPASS_b3_is_collision_angle": False,
            "full_candidate_owner_path_chart_replay_passed": True,
        },
        "gate5_actual_child_field_status": {
            **{f"F{i}": "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN" for i in range(1, 7)},
            **{f"F{i}": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN" for i in range(7, 19)},
        },
        "rank3_seed_child_field_maturity": "6/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "one exact analytic b seed inside one Round113/Round117 BYPASS relative-interior "
            "operator cell, its 26 materialized stage input recuts, 23 pullback cuts, 24 "
            "common-refinement actual children, and child-local full-key F1-F6"
        ),
        "strict_nonclaims": [
            "the full Round120 Borel-b family is not numerically materialized or uniformly ranked",
            "no Round31 compact-Q2 time2 atom, parent-W ID, branch-rule ID, or recut ID is reused",
            "the designated BYPASS coordinate b3 is not a collision angle or homogeneity index",
            "F7-F18 are not installed on the Round121 exact-seed children",
            "24 seed children do not upgrade the global Gate5 10/18 maturity or create a complete block",
            "no endpoint-inclusive physical collar, cross-trace union reach, or whole-face atlas is claimed",
            "Gate5 and CM2 remain unavailable",
        ],
        "upstream_and_helper_pins": dict(sorted(all_pins.items())),
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": closed_digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build(args.precision_bits)
    args.output.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print("EXACT_B_SEEDS: 1")
    print("MATERIALIZED_STAGE_RECUTS: 26")
    print("COMMON_REFINEMENT_ACTUAL_CHILDREN: 24")
    print("RANK3_SEED_CHILD_FIELDS: 6/18")
    print("GATE5_GLOBAL: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
