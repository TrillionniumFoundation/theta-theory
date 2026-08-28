#!/usr/bin/env python3
"""Independent verifier for the Round121 exact-seed three-leg recut.

This verifier deliberately does not import the Round121 producer.  It starts
from the frozen Round112/113/117/120 objects, isolates the exact anchor root at
2048-bit precision, reconstructs the source curve and its first three
collisions, and then independently builds the two image adapted coordinates.
It certifies all 6+17 pullback cuts, their strict order and separation, the 26
natural cells, 24 common-refinement children, and the 720 immutable F1--F6
slots.  Global Gate5 remains 10/18 and CM2 remains unavailable.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq, interval
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)
CERTIFICATE_SCHEMA = "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1"
VERIFICATION_SCHEMA = (
    "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1"
)
VERIFIER_PRECISION_BITS = 2048

ROUND112 = (
    HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
)
ROUND113 = (
    HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
)
ROUND117 = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
)
ROUND120 = (
    HERE
    / "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json"
)
ROUND47 = (
    HERE / "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
)
ROUND50 = (
    HERE
    / "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
)
GATE5 = HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
UNIVERSAL = (
    HERE
    / "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
)
CONE = HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
DSTD = (
    HERE
    / "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
)
GATE4_COMPONENTWISE = (
    HERE
    / "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
)

UPSTREAM_PINS = {
    ROUND112.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND117.name: "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND120.name: "a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5",
    ROUND47.name: "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    ROUND50.name: "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    GATE5.name: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    UNIVERSAL.name: "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
    CONE.name: "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    DSTD.name: "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d",
    GATE4_COMPONENTWISE.name: (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": (
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6"
    ),
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": (
        "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f"
    ),
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py": (
        "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e"
    ),
    "cm2_round76_r2_numeric_fields_generator.py": (
        "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf"
    ),
    "cm2_round79_tangency_intersection_generator.py": (
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7"
    ),
}

SEED_PARENT_ID = (
    "round113-cell:"
    "08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
)
SEED_OPERATOR_ID = (
    "round117-operator-cell:"
    "dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1"
)
SEED_BRANCH = (7, "G[0,0]", "W[-1,-2]", 1)
SEED_SOURCE_CHART = "G:W"
SEED_ACTUAL_THIRD = "G[-1,-2]"
SEED_C0 = Q(1, 16384)
SEED_B3 = Q(3, 65536)
DELTA = Q(1, 10**90)
THETA = Q(144000, 180337)
ONE_STEP_LOG_VARIATION = Q(3, 200000)
THREE_STEP_THETA = THETA**3
THREE_STEP_LOG_VARIATION = 3 * ONE_STEP_LOG_VARIATION
ROOT_BISECTIONS = 960
# This differs from the producer's 200-step endpoint brackets while remaining
# far sharper than every claimed separation.  The deeper independent anchor
# isolation makes all 240 endpoint sign decisions strict at 2048 bits and
# ensures every fresh enclosure is at least as sharp as its producer witness.
ENDPOINT_BISECTIONS = 240

OFFICIAL_WORD_IDS = (
    "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
    "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
    "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
)
ROOF_COUNTS = (2, 1, 2)
GATE5_FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
)
EXPECTED_CUT_ORDER = (
    "S2:1",
    "S2:2",
    "S1:1",
    "S2:3",
    "S2:4",
    "S2:5",
    "S1:2",
    "S2:6",
    "S2:7",
    "S1:3",
    "S2:8",
    "S2:9",
    "S2:10",
    "S1:4",
    "S2:11",
    "S2:12",
    "S1:5",
    "S2:13",
    "S2:14",
    "S2:15",
    "S1:6",
    "S2:16",
    "S2:17",
)

RESULT_KEYS = {
    "precision_bits",
    "exact_seed_contract",
    "exact_parent_W_witness_rows",
    "source_adapted_cell_rows",
    "stage_adapted_coordinate_contract",
    "stage_recut_rows",
    "stage_recut_rows_sha256",
    "pullback_endpoint_rows",
    "pullback_endpoint_rows_sha256",
    "common_refinement_rows",
    "common_refinement_rows_sha256",
    "refined_homogeneous_subbranch_rows",
    "refined_homogeneous_subbranch_rows_sha256",
    "gate5_F1_F6_slot_rows",
    "gate5_F1_F6_slot_rows_sha256",
    "three_leg_restriction_theorem",
    "whole_seed_owner_candidate_replay",
    "count_ledger",
    "boundary_owner_ledger",
    "gate5_actual_child_field_status",
    "rank3_seed_child_field_maturity",
    "gate5_global_maturity",
    "complete_18_field_block_count",
    "gate5_block_count",
    "cm2_verdict",
    "strict_scope",
    "strict_nonclaims",
    "upstream_and_helper_pins",
}
WITNESS_KEYS = {
    "exact_parent_W_seed_id",
    "anchor_t_unique_root_dyadic_bracket",
    "anchor_root_face_signs",
    "anchor_t_bracket_width_strict_upper",
    "anchor_root_partial_t_sign",
    "inherited_parent_uniform_partial_t_sign",
    "anchor_root_partial_t_abs_strict_lower",
    "anchor_root_partial_t_nonzero_and_unique",
    "theta_star_enclosure",
    "b_star_enclosure",
    "b_star_is_an_exact_analytic_real_not_the_enclosure_text",
    "materialized_exact_b_witness",
}
SOURCE_ROW_KEYS = {
    "source_recut_instance_id",
    "source_adapted_index_k",
    "source_parameter_domain",
    "right_endpoint_closed",
    "delta",
    "theta0",
    "phi0",
    "t",
    "c0",
    "b3",
    "source_adapted_coordinate",
    "source_adapted_length_exact",
    "c0_enclosure",
    "b3_enclosure",
    "within_R113_R117_regular_relative_interior",
    "H128_upper_boundary_sin_128_minus_2_enclosure",
    "c0_minus_H128_upper_boundary_strict_lower",
    "source_H0_CENTRAL_OUTER_membership_whole_cell",
    "coefficient_identity",
    "slope_four_parent_W_identity",
    "p0_equals_sin_4r_plus_b_star_whole_cell",
    "slope_four_intercept_enclosure",
    "c0_x_derivative_sign",
    "c0_x_derivative_over_delta_enclosure",
    "b3_x_derivative_sign",
    "b3_x_derivative_over_delta_enclosure",
    "source_adapted_density",
    "source_adapted_coordinate_identity",
    "u0_x_derivative_exact",
}
ENDPOINT_KEYS = {
    "endpoint_id",
    "exact_parent_W_seed_id",
    "stage",
    "natural_index_j",
    "exact_root_equation_id",
    "exact_root_equation",
    "x_dyadic_bracket",
    "x_bracket_width_upper",
    "left_function_sign",
    "right_function_sign",
    "derivative_sign",
    "normalized_derivative_abs_strict_lower",
    "unique_root_certified",
    "source_c0_enclosure",
    "source_t_enclosure",
    "source_b3_enclosure",
    "lower_owner",
    "upper_owner",
    "numeric_bracket_or_Arb_text_participates_in_endpoint_ID",
    "evidence_sha256",
}
RECUT_KEYS = {
    "recut_instance_id",
    "exact_parent_W_seed_id",
    "stage",
    "natural_index_j",
    "adapted_coordinate_id",
    "adapted_lower",
    "adapted_upper",
    "adapted_length_upper",
    "normalized_adapted_length_strict_lower",
    "lower_endpoint_id",
    "upper_endpoint_id",
    "lower_closed",
    "upper_closed",
    "source_parent_right_endpoint_is_open",
    "internal_cut_owned_by_right_natural_cell",
    "official_word_key_id",
    "roof_level_count",
    "actual_materialized_input_recut",
    "row_sha256",
}
COMMON_KEYS = {
    "common_rank",
    "common_child_id",
    "refined_homogeneous_subbranch_id",
    "source_x_lower_endpoint_id",
    "source_x_upper_endpoint_id",
    "lower_closed",
    "upper_closed",
    "source_parent_right_endpoint_is_open",
    "covering_stage_indices",
    "source_recut_instance_id",
    "first_image_recut_instance_id",
    "second_image_recut_instance_id",
    "all_three_inputs_contained_in_one_materialized_canonical_cell",
    "round117_operator_cell_id",
    "official_path_id",
    "positive_source_x_length_strict_lower",
    "actual_standard_curve_child_installed",
    "row_sha256",
}
REFINED_KEYS = {
    "refined_homogeneous_subbranch_id",
    "common_child_id",
    "round117_operator_cell_id",
    "exact_parent_W_seed_id",
    "source_adapted_index_k",
    "common_rank",
    "physical_homogeneity",
    "row_sha256",
}
SLOT_KEYS = {
    "slot_id",
    "immutable_slot_key",
    "official_word_key_id",
    "refined_homogeneous_subbranch_id",
    "common_child_id",
    "stage",
    "roof_level_j",
    "field_index",
    "field_name",
    "field_value_or_contract",
    "materialized_input_recut_instance_id",
    "slot_status",
    "transparent_wall_roof_split_does_not_add_a_collision_Jacobian_factor",
}


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def require_integer(value: Any, label: str) -> int:
    require(type(value) is int, f"{label}:integer type")
    return value


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(token: str) -> Any:
    raise ValueError(f"non-finite JSON number:{token}")


def reject_float(token: str) -> Any:
    raise ValueError(f"JSON float forbidden:{token}")


def strict_integer(token: str) -> int:
    if token == "-0":
        raise ValueError("negative zero forbidden")
    if len(token.lstrip("-")) > 1024:
        raise ValueError("oversized integer")
    return int(token)


def reject_surrogates(value: Any) -> None:
    if type(value) is str:
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            "unpaired surrogate",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key)
            reject_surrogates(item)


def strict_json(text: str) -> dict[str, Any]:
    if text.startswith("\ufeff"):
        raise ValueError("BOM forbidden")
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=reject_float,
        parse_int=strict_integer,
    )
    if type(value) is not dict:
        raise TypeError("top-level JSON must be object")
    reject_surrogates(value)
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str, f"{label}:fraction type")
    require(re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value) is not None,
            f"{label}:noncanonical fraction")
    result = Q(value)
    require(str(result) == value, f"{label}:nonreduced fraction")
    return result


def qstr(value: Q) -> str:
    return str(value)


def arb_pair(value: arb) -> tuple[Q, Q]:
    """Outward rational endpoints parsed from Arb's exact endpoint objects."""
    def exact_dyadic(point: arb) -> Q:
        mantissa, exponent = point.man_exp()
        return Q(int(mantissa)) * Q(2) ** int(exponent)

    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def arb_hull(values: list[arb]) -> arb:
    require(len(values) > 0, "nonempty Arb hull")
    pairs = [arb_pair(value) for value in values]
    return interval(
        min(lower for lower, _ in pairs),
        max(upper for _, upper in pairs),
    )


def padded_pair(value: arb, padding: Q = Q(1, 10**180)) -> list[str]:
    lower, upper = arb_pair(value)
    return [str(lower - padding), str(upper + padding)]


class Dual:
    """First-order interval dual used only by the independent verifier."""

    def __init__(self, value: arb | int, derivative: arb | int = 0):
        self.value = value if isinstance(value, arb) else arb(value)
        self.derivative = (
            derivative if isinstance(derivative, arb) else arb(derivative)
        )

    def __add__(self, other: Any) -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Dual":
        return self + (-other if isinstance(other, Dual) else -other)

    def __rsub__(self, other: Any) -> "Dual":
        return Dual(other) - self

    def __mul__(self, other: Any) -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value / other.value,
            (
                self.derivative * other.value
                - self.value * other.derivative
            )
            / (other.value * other.value),
        )

    def __rtruediv__(self, other: Any) -> "Dual":
        return Dual(other) / self

    def sqrt(self) -> "Dual":
        root = self.value.sqrt()
        return Dual(root, self.derivative / (2 * root))

    def sin(self) -> "Dual":
        return Dual(self.value.sin(), self.value.cos() * self.derivative)

    def cos(self) -> "Dual":
        return Dual(self.value.cos(), -self.value.sin() * self.derivative)

    def asin(self) -> "Dual":
        return Dual(
            self.value.asin(),
            self.derivative / (arb(1) - self.value * self.value).sqrt(),
        )


def target_center(target: str) -> tuple[arb, arb]:
    obstacle = target[0]
    ix, iy = map(int, target[2:-1].split(","))
    offset = Q(1, 2) if obstacle == "W" else Q(0)
    return aq(Q(ix) + offset), aq(Q(iy) + offset)


def target_radius(target: str) -> arb:
    return aq(Q(9, 25) if target[0] == "G" else Q(4, 25))


def dual_collision(
    qx: Dual, qy: Dual, ux: Dual, uy: Dual, target: str
) -> tuple[Dual, Dual, Dual, Dual, Dual, Dual, Dual, Dual, Dual]:
    cx, cy = target_center(target)
    dx, dy = cx - qx, cy - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = target_radius(target)
    discriminant = radius * radius - transverse * transverse
    radical = discriminant.sqrt()
    flight = ell - radical
    hit_x, hit_y = qx + flight * ux, qy + flight * uy
    normal_x, normal_y = (hit_x - cx) / radius, (hit_y - cy) / radius
    momentum = transverse / radius
    cosine = (Dual(arb(1)) - momentum * momentum).sqrt()
    out_x = cosine * normal_x - momentum * normal_y
    out_y = cosine * normal_y + momentum * normal_x
    return (
        hit_x,
        hit_y,
        out_x,
        out_y,
        normal_x,
        normal_y,
        momentum,
        flight,
        discriminant,
    )


def load_inputs() -> dict[str, Any]:
    for name, expected in UPSTREAM_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
        require(sha256(path) == expected, f"byte pin:{name}")
    values: dict[str, Any] = {}
    for key, path, schema in (
        ("r112", ROUND112, round112.SCHEMA),
        ("r113", ROUND113, round113.SCHEMA),
        (
            "r117",
            ROUND117,
            "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
        ),
        (
            "r120",
            ROUND120,
            "cm2.round120.rank3-relative-interior-actual-standard-curve-recut.v1",
        ),
    ):
        doc = strict_json(path.read_text(encoding="utf-8"))
        require(set(doc) == {"schema", "result", "result_sha256"}, f"{key}:envelope")
        require(doc["schema"] == schema, f"{key}:schema")
        require(doc["result_sha256"] == digest(doc["result"]), f"{key}:digest")
        values[key] = doc["result"]
    for key, path in (
        ("round47", ROUND47),
        ("round50", ROUND50),
        ("gate5", GATE5),
        ("universal", UNIVERSAL),
        ("cone", CONE),
        ("dstd", DSTD),
        ("g4c", GATE4_COMPONENTWISE),
    ):
        values[key] = strict_json(path.read_text(encoding="utf-8"))
    return values


def seed_indexes(values: dict[str, Any]) -> dict[str, Any]:
    r113_sheet: dict[str, Any] | None = None
    parent: dict[str, Any] | None = None
    for sheet in values["r113"]["sheet_rows"]:
        for cell in sheet["certified_cells"]:
            if cell["cell_id"] == SEED_PARENT_ID:
                r113_sheet, parent = sheet, cell
    require(r113_sheet is not None and parent is not None, "R113 seed lookup")
    sheet112 = next(
        row
        for row in values["r112"]["sheet_rows"]
        if row["sheet_id"] == r113_sheet["sheet_id"]
    )
    row117 = next(
        row
        for row in values["r117"]["common_refinement_rows"]
        if row["parent_round113_cell_id"] == SEED_PARENT_ID
    )
    generator = next(
        row
        for row in row117["generator_families"]
        if row["stable_id_interface_sample"]["operator_cell_id"]
        == SEED_OPERATOR_ID
    )
    row120 = next(
        row
        for row in values["r120"]["child_generator_rows"]
        if row["parent_round113_cell_id"] == SEED_PARENT_ID
    )
    require(tuple(r113_sheet["branch_key"]) == SEED_BRANCH, "seed branch")
    require(r113_sheet["sheet_kind"] == "BYPASS", "seed sheet kind")
    require(r113_sheet["source_chart"] == SEED_SOURCE_CHART, "seed chart")
    require(sheet112["source_grazing_sign_sigma0"] == 1, "seed source sign")
    require(row117["actual_third_collision_owner_id"] == SEED_ACTUAL_THIRD,
            "actual third owner")
    require(row117["bypass_b3_is_collision_angle"] is False, "b3 role")
    require(row117["actual_third_collision_homogeneity_label"] == "H0_CENTRAL",
            "actual third H0")
    require(row117["central_outer_source_child_nonempty"] is True,
            "seed nonempty")
    require(row120["official_word_key_ids"] == list(OFFICIAL_WORD_IDS),
            "official words")
    return {
        "sheet113": r113_sheet,
        "parent": parent,
        "sheet112": sheet112,
        "row117": row117,
        "generator": generator,
        "row120": row120,
    }


def isolate_anchor(idx: dict[str, Any]) -> dict[str, Any]:
    parent = idx["parent"]
    lower, upper = map(Q, parent["implicit_t_root_enclosure"])
    source = replace(
        core_cert.physical_cores()[SEED_BRANCH[0]], chart_id=SEED_SOURCE_CHART
    )

    def equation(t: Q) -> arb:
        return round113.equation_value(
            source,
            SEED_BRANCH,
            1,
            "BYPASS",
            t,
            SEED_C0,
            SEED_C0,
            SEED_B3,
            SEED_B3,
        )

    lower_sign, upper_sign = strict_sign(equation(lower)), strict_sign(equation(upper))
    require(lower_sign * upper_sign == -1, "anchor endpoint signs")
    completed = 0
    for _ in range(ROOT_BISECTIONS):
        middle = (lower + upper) / 2
        sign = strict_sign(equation(middle))
        if sign == 0:
            break
        if sign == lower_sign:
            lower = middle
        elif sign == upper_sign:
            upper = middle
        else:
            raise RuntimeError("anchor bisection sign")
        completed += 1
    require(completed >= 320, "anchor isolation depth")
    t_ball = interval(lower, upper)
    require(bool(t_ball > 0) and bool(t_ball < 1), "anchor chart interval")
    theta_ball = arb.pi() - t_ball.asin()
    return {
        "t_lower": lower,
        "t_upper": upper,
        "t_ball": t_ball,
        "theta_ball": theta_ball,
        "lower_sign": lower_sign,
        "upper_sign": upper_sign,
        "bisections": completed,
    }


def source_and_collisions(
    theta_star: arb, x_value: arb, differentiated: bool
) -> dict[str, Any]:
    x = Dual(x_value, arb(1) if differentiated else arb(0))
    delta = aq(DELTA)
    theta0 = Dual(theta_star) + aq(Q(25, 61)) * delta * x
    phi0 = Dual(aq(SEED_C0).acos()) + aq(Q(36, 61)) * delta * x
    c0 = phi0.cos()
    t = theta0.sin()
    normal_x, normal_y = theta0.cos(), t
    p0 = (Dual(arb(1)) - c0 * c0).sqrt()
    source_radius = aq(Q(9, 25))
    qx, qy = source_radius * normal_x, source_radius * normal_y
    ux = c0 * normal_x - p0 * normal_y
    uy = c0 * normal_y + p0 * normal_x
    first = dual_collision(qx, qy, ux, uy, "W[-1,-1]")
    second = dual_collision(*first[:4], "G[0,0]")
    actual_third = dual_collision(*second[:4], SEED_ACTUAL_THIRD)

    # The designated W[-1,-2] is a strict whole-line miss.  Its negative
    # discriminant defines b3; it is not a collision momentum.
    cx3, cy3 = target_center("W[-1,-2]")
    dx3, dy3 = cx3 - second[0], cy3 - second[1]
    transverse3 = -second[3] * dx3 + second[2] * dy3
    r3 = target_radius("W[-1,-2]")
    designated_discriminant = r3 * r3 - transverse3 * transverse3
    b3 = (-designated_discriminant).sqrt() / r3

    # Frozen charts N and S give canonical unwrapped normal angles.
    a1 = Dual(arb.pi() / 2) - first[4].asin() + first[6].asin()
    a2 = Dual(-arb.pi() / 2) + second[4].asin() + second[6].asin()
    return {
        "c0": c0,
        "t": t,
        "b3": b3,
        "first": first,
        "second": second,
        "actual_third": actual_third,
        "a1": a1,
        "a2": a2,
    }


def isolate_endpoint(
    function: Callable[[Q], arb], stage: int, natural_index: int
) -> dict[str, Any]:
    lower, upper = Q(0), Q(1)
    lower_sign, upper_sign = strict_sign(function(lower)), strict_sign(function(upper))
    require(lower_sign == -1 and upper_sign == 1, f"endpoint signs S{stage}:{natural_index}")
    for _ in range(ENDPOINT_BISECTIONS):
        middle = (lower + upper) / 2
        sign = strict_sign(function(middle))
        require(sign != 0, f"endpoint indeterminate S{stage}:{natural_index}")
        if sign == lower_sign:
            lower = middle
        else:
            upper = middle
    require(strict_sign(function(lower)) == -1, "endpoint lower replay")
    require(strict_sign(function(upper)) == 1, "endpoint upper replay")
    return {
        "stage": stage,
        "natural_index_j": natural_index,
        "lower": lower,
        "upper": upper,
        "left_sign": -1,
        "right_sign": 1,
    }


def independent_geometry(values: dict[str, Any], idx: dict[str, Any]) -> dict[str, Any]:
    anchor = isolate_anchor(idx)
    theta_star = anchor["theta_ball"]
    zero = source_and_collisions(theta_star, arb(0), False)
    one = source_and_collisions(theta_star, arb(1), False)
    whole = source_and_collisions(theta_star, interval(Q(0), Q(1)), True)
    delta = aq(DELTA)
    u1_length = zero["a1"].value - one["a1"].value
    u2_length = one["a2"].value - zero["a2"].value
    u1_ratio = u1_length / delta
    u2_ratio = u2_length / delta
    require(bool(u1_ratio > 6) and bool(u1_ratio < 7), "U1 length ratio")
    require(bool(u2_ratio > 17) and bool(u2_ratio < 18), "U2 length ratio")
    # Subdivision removes dependency inflation while covering all of [0,1].
    # The producer used one whole-cell interval; this independent verifier
    # deliberately uses two dyadic leaves and hulls their derivative ranges.
    derivative_leaves = [
        source_and_collisions(
            theta_star, interval(Q(piece, 2), Q(piece + 1, 2)), True
        )
        for piece in range(2)
    ]
    c0_derivative = arb_hull(
        [leaf["c0"].derivative / delta for leaf in derivative_leaves]
    )
    b3_derivative = arb_hull(
        [leaf["b3"].derivative / delta for leaf in derivative_leaves]
    )
    u1_derivative = arb_hull(
        [-leaf["a1"].derivative / delta for leaf in derivative_leaves]
    )
    u2_derivative = arb_hull(
        [leaf["a2"].derivative / delta for leaf in derivative_leaves]
    )
    require(bool(u1_derivative > 6), "U1 monotonic derivative")
    require(bool(u2_derivative > 17), "U2 monotonic derivative")

    def u1(x: Q) -> arb:
        state = source_and_collisions(theta_star, aq(x), False)
        return zero["a1"].value - state["a1"].value

    def u2(x: Q) -> arb:
        state = source_and_collisions(theta_star, aq(x), False)
        return state["a2"].value - zero["a2"].value

    endpoints: list[dict[str, Any]] = []
    for stage, count, function in ((1, 6, u1), (2, 17, u2)):
        for natural_index in range(1, count + 1):
            target = aq(DELTA * natural_index)
            endpoint = isolate_endpoint(
                lambda x, f=function, target=target: f(x) - target,
                stage,
                natural_index,
            )
            endpoint["cut_label"] = f"S{stage}:{natural_index}"
            endpoints.append(endpoint)
    endpoints.sort(key=lambda row: row["lower"])
    require(tuple(row["cut_label"] for row in endpoints) == EXPECTED_CUT_ORDER,
            "pullback cut order")
    for left, right in zip(endpoints, endpoints[1:]):
        require(right["lower"] - left["upper"] > Q(1, 200),
                "pullback cut separation")

    # The entire seed curve lies in the frozen parent box and hence inherits
    # the complete R113 candidate/owner replay.
    c0_lower, c0_upper = map(Q, idx["parent"]["parameter_box"]["c0"])
    b3_lower, b3_upper = map(Q, idx["parent"]["parameter_box"]["b3"])
    # Direct interval evaluation of cos(phi_*+[0,36 delta/61]) has a tiny
    # symmetric dependency overhang at x=0.  The 1e-80 comparison allowance
    # is still 75 orders smaller than the parent-box margin; monotonicity is
    # checked separately below.
    endpoint_rounding = aq(Q(1, 10**80))
    require(bool(whole["c0"].derivative < 0), "source c0 orientation")
    require(bool(whole["t"].derivative < 0), "source t orientation")
    require(bool(whole["b3"].derivative < 0), "designated b3 orientation")
    for state in (zero, one, whole):
        require(
            bool(state["c0"].value >= aq(c0_lower) - endpoint_rounding),
            "source c0 lower",
        )
        require(
            bool(state["c0"].value <= aq(c0_upper) + endpoint_rounding),
            "source c0 upper",
        )
        require(bool(state["b3"].value > aq(b3_lower)), "source b3 lower")
        require(bool(state["b3"].value < aq(b3_upper)), "source b3 upper")
    require(bool(whole["actual_third"][8].value > 0), "actual third discriminant")
    require(bool(whole["actual_third"][6].value < 0), "actual third momentum sign")
    require(bool((arb(1) - whole["actual_third"][6].value**2).sqrt() > aq(Q(4, 5))),
            "actual third H0")
    require(bool(whole["first"][4].value > 0) and bool(whole["first"][5].value > 0),
            "first chart N")
    require(bool(whole["second"][5].value < 0), "second chart S")

    def state_endpoint_hull(lower: Q, upper: Q) -> dict[str, arb]:
        lower_state = source_and_collisions(theta_star, aq(lower), False)
        upper_state = source_and_collisions(theta_star, aq(upper), False)
        return {
            key: arb_hull([lower_state[key].value, upper_state[key].value])
            for key in ("c0", "t", "b3")
        }

    return {
        "anchor": anchor,
        "zero": zero,
        "one": one,
        "whole": whole,
        "u1_ratio": u1_ratio,
        "u2_ratio": u2_ratio,
        "c0_derivative": c0_derivative,
        "b3_derivative": b3_derivative,
        "u1_derivative": u1_derivative,
        "u2_derivative": u2_derivative,
        "endpoints": endpoints,
        "u1": u1,
        "u2": u2,
        "state": lambda lower, upper: source_and_collisions(
            theta_star, interval(lower, upper), True
        ),
        "state_endpoint_hull": state_endpoint_hull,
    }


def exact_seed_id() -> str:
    payload = [
        "round121-exact-parent-W-v1",
        SEED_PARENT_ID,
        SEED_OPERATOR_ID,
        "round120-angular-lift:G:W:k0",
        "c0=1/16384",
        "b3=3/65536",
        "unique-root:F_BYPASS(t,c0,b3)=0",
    ]
    return "round121-exact-parent-W:" + digest(payload)


def source_boundary_id(which: str, seed_id: str) -> str:
    require(which in {"left", "right"}, "source boundary name")
    return (
        f"round121-source-{which}-endpoint:"
        + digest(["round121-source-boundary-v1", seed_id, which])
    )


def recut_id(seed_id: str, stage: int, natural_index: int) -> str:
    return "round121-recut-instance:" + digest(
        [
            "round121-materialized-adapted-input-recut-v1",
            seed_id,
            stage,
            natural_index,
        ]
    )


def row_digest(row: dict[str, Any], digest_key: str) -> str:
    return digest({key: value for key, value in row.items() if key != digest_key})


def interval_contract(value: Any, label: str) -> tuple[Q, Q]:
    require(type(value) is list and len(value) == 2, f"{label}:interval")
    lower, upper = qvalue(value[0], f"{label}:lower"), qvalue(
        value[1], f"{label}:upper"
    )
    require(lower <= upper, f"{label}:order")
    return lower, upper


def interval_contains(stored: Any, value: arb, label: str) -> None:
    lower, upper = interval_contract(stored, label)
    fresh_lower, fresh_upper = arb_pair(value)
    require(lower <= fresh_lower and upper >= fresh_upper, f"{label}:containment")


def interval_encloses_cross_precision(stored: Any, value: arb, label: str) -> None:
    """Require literal containment of a fresh independent 2048-bit enclosure."""

    lower, upper = interval_contract(stored, label)
    fresh_lower, fresh_upper = arb_pair(value)
    require(
        lower <= fresh_lower and upper >= fresh_upper,
        f"{label}:cross-precision containment",
    )


def static_contract(document: dict[str, Any]) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS, "closed result")
    require(document["result_sha256"] == digest(result), "certificate result digest")
    require(
        type(result["precision_bits"]) is int
        and not isinstance(result["precision_bits"], bool)
        and result["precision_bits"] >= 1024,
        "producer precision",
    )

    seed = result["exact_seed_contract"]
    require(type(seed) is dict, "seed contract type")
    require_integer(seed["source_grazing_sign_sigma0"], "seed source sign")
    require(
        seed
        == {
            "round113_parent_id": SEED_PARENT_ID,
            "round117_operator_cell_id": SEED_OPERATOR_ID,
            "round117_family": "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0",
            "sheet_kind": "BYPASS",
            "branch_key": list(SEED_BRANCH),
            "source_chart": SEED_SOURCE_CHART,
            "source_grazing_sign_sigma0": 1,
            "actual_third_owner_id": SEED_ACTUAL_THIRD,
            "anchor": {"c0": "1/16384", "b3": "3/65536"},
            "angular_lift_id": "round120-angular-lift:G:W:k0",
            "root_identity_predicate": (
                "the unique t in the frozen Round112 enclosure with "
                "F_BYPASS(t,1/16384,3/65536)=0"
            ),
            "intercept_definition": (
                "b*=arccos(1/16384)-(36/25)*(pi-arcsin(t*))"
            ),
            "exact_parent_W_seed_id": exact_seed_id(),
            "stable_ID_payload_uses_only_parent_operator_rational_anchor_root_predicate_and_lift": True,
            "Arb_decimal_or_numeric_bracket_participates_in_ID": False,
        },
        "exact seed contract",
    )

    witnesses = result["exact_parent_W_witness_rows"]
    require(type(witnesses) is list and len(witnesses) == 1, "witness census")
    witness = witnesses[0]
    require(type(witness) is dict and set(witness) == WITNESS_KEYS, "witness schema")
    for index, sign in enumerate(witness["anchor_root_face_signs"]):
        require_integer(sign, f"anchor face sign {index}")
    require_integer(witness["anchor_root_partial_t_sign"], "anchor partial t sign")
    require_integer(
        witness["inherited_parent_uniform_partial_t_sign"],
        "inherited partial t sign",
    )
    require(witness["exact_parent_W_seed_id"] == exact_seed_id(), "witness seed ID")
    require(witness["anchor_root_face_signs"] == [1, -1], "anchor signs")
    require(
        witness["anchor_root_partial_t_nonzero_and_unique"] is True
        and witness["anchor_root_partial_t_sign"] == -1
        and witness["inherited_parent_uniform_partial_t_sign"] == -1,
        "anchor root uniqueness",
    )
    require(
        qvalue(
            witness["anchor_root_partial_t_abs_strict_lower"],
            "anchor partial t lower",
        )
        > 0,
        "anchor partial t positive",
    )
    root_lower, root_upper = interval_contract(
        witness["anchor_t_unique_root_dyadic_bracket"], "anchor t"
    )
    require(
        root_upper - root_lower
        < qvalue(
            witness["anchor_t_bracket_width_strict_upper"],
            "anchor width upper",
        )
        <= Q(1, 10**220),
        "anchor width",
    )
    interval_contract(witness["theta_star_enclosure"], "theta star")
    interval_contract(witness["b_star_enclosure"], "b star")
    require(
        witness["b_star_is_an_exact_analytic_real_not_the_enclosure_text"] is True
        and witness["materialized_exact_b_witness"] is True,
        "exact b witness",
    )

    source_rows = result["source_adapted_cell_rows"]
    require(type(source_rows) is list and len(source_rows) == 1, "source row census")
    source = source_rows[0]
    require(type(source) is dict and set(source) == SOURCE_ROW_KEYS, "source row schema")
    require_integer(source["source_adapted_index_k"], "source adapted index")
    require_integer(source["c0_x_derivative_sign"], "source c0 sign")
    require_integer(source["b3_x_derivative_sign"], "source b3 sign")
    require(
        source["source_recut_instance_id"] == recut_id(exact_seed_id(), 0, 0)
        and source["source_adapted_index_k"] == 0
        and source["source_parameter_domain"] == "[0,1)"
        and source["right_endpoint_closed"] is False
        and source["delta"] == "1e-90"
        and source["theta0"] == "theta*+(25/61)*delta*x"
        and source["phi0"] == "arccos(1/16384)+(36/61)*delta*x"
        and source["t"] == "sin(theta0)"
        and source["c0"] == "cos(phi0)"
        and source["b3"] == "sqrt(-Delta3(t,c0))/(4/25)"
        and source["source_adapted_coordinate"] == "u0(x)=delta*x"
        and source["source_adapted_length_exact"] == "1e-90"
        and source["source_adapted_density"] == "61/9"
        and source["source_adapted_coordinate_identity"]
        == "(25/9+4)*(9/25)*(25/61)=1"
        and source["u0_x_derivative_exact"] == "1e-90"
        and source["c0_x_derivative_sign"] == -1
        and source["b3_x_derivative_sign"] == -1
        and source["within_R113_R117_regular_relative_interior"] is True,
        "source row contract",
    )
    require(
        source["coefficient_identity"]
        == "(36/61)=(36/25)*(25/61)=4*(9/25)*(25/61)"
        and source["slope_four_parent_W_identity"]
        == "phi0(x)-4*(9/25)*theta0(x)=b* on the whole cell"
        and source["p0_equals_sin_4r_plus_b_star_whole_cell"] is True
        and source["source_H0_CENTRAL_OUTER_membership_whole_cell"] is True
        and qvalue(
            source["c0_minus_H128_upper_boundary_strict_lower"],
            "source H128 margin",
        )
        > 0,
        "source slope/H128 contract",
    )
    interval_contract(source["c0_enclosure"], "source c0")
    interval_contract(source["b3_enclosure"], "source b3")
    interval_contract(
        source["H128_upper_boundary_sin_128_minus_2_enclosure"],
        "H128 upper",
    )
    interval_contract(source["slope_four_intercept_enclosure"], "slope intercept")
    interval_contract(
        source["c0_x_derivative_over_delta_enclosure"], "c0 derivative"
    )
    interval_contract(
        source["b3_x_derivative_over_delta_enclosure"], "b3 derivative"
    )

    list_contracts = (
        ("stage_recut_rows", "stage_recut_rows_sha256", RECUT_KEYS, "row_sha256"),
        (
            "pullback_endpoint_rows",
            "pullback_endpoint_rows_sha256",
            ENDPOINT_KEYS,
            "evidence_sha256",
        ),
        (
            "common_refinement_rows",
            "common_refinement_rows_sha256",
            COMMON_KEYS,
            "row_sha256",
        ),
        (
            "refined_homogeneous_subbranch_rows",
            "refined_homogeneous_subbranch_rows_sha256",
            REFINED_KEYS,
            "row_sha256",
        ),
    )
    for rows_key, digest_key, keys, row_sha_key in list_contracts:
        rows = result[rows_key]
        require(type(rows) is list, f"{rows_key}:list")
        require(result[digest_key] == digest(rows), f"{rows_key}:digest")
        for row in rows:
            require(type(row) is dict and set(row) == keys, f"{rows_key}:row schema")
            if rows_key == "stage_recut_rows":
                require_integer(row["stage"], "recut stage")
                require_integer(row["natural_index_j"], "recut natural index")
                require_integer(row["roof_level_count"], "recut roof count")
            elif rows_key == "pullback_endpoint_rows":
                require_integer(row["stage"], "endpoint stage")
                require_integer(row["natural_index_j"], "endpoint natural index")
                require_integer(row["left_function_sign"], "endpoint left sign")
                require_integer(row["right_function_sign"], "endpoint right sign")
                require_integer(row["derivative_sign"], "endpoint derivative sign")
            elif rows_key == "common_refinement_rows":
                require_integer(row["common_rank"], "common rank")
                require(type(row["covering_stage_indices"]) is list, "stage index list")
                for index, stage_index in enumerate(row["covering_stage_indices"]):
                    require_integer(stage_index, f"covering stage index {index}")
            else:
                require_integer(row["common_rank"], "refined common rank")
                require_integer(
                    row["source_adapted_index_k"], "refined source index"
                )
            require(
                row[row_sha_key] == row_digest(row, row_sha_key),
                f"{rows_key}:row digest",
            )
    slots = result["gate5_F1_F6_slot_rows"]
    require(type(slots) is list and len(slots) == 720, "slot census")
    require(result["gate5_F1_F6_slot_rows_sha256"] == digest(slots), "slot digest")
    for slot in slots:
        require(type(slot) is dict and set(slot) == SLOT_KEYS, "slot schema")
        require_integer(slot["stage"], "slot stage")
        require_integer(slot["roof_level_j"], "slot roof level")
        require_integer(slot["field_index"], "slot field index")
        require(type(slot["immutable_slot_key"]) is list, "slot key list")
        require_integer(slot["immutable_slot_key"][2], "slot key roof level")

    require(
        len(result["stage_recut_rows"]) == 26
        and len(result["pullback_endpoint_rows"]) == 23
        and len(result["common_refinement_rows"]) == 24
        and len(result["refined_homogeneous_subbranch_rows"]) == 24,
        "materialized row counts",
    )
    ledger = result["count_ledger"]
    require(type(ledger) is dict, "count ledger type")
    for key, value in ledger.items():
        if key == "official_word_roof_level_counts":
            require(type(value) is list, "roof count list")
            for index, count in enumerate(value):
                require_integer(count, f"roof count {index}")
        else:
            require_integer(value, f"count ledger {key}")
    require(
        ledger
        == {
            "exact_b_seed_count": 1,
            "source_natural_cell_count": 1,
            "first_image_natural_cell_count": 7,
            "second_image_natural_cell_count": 18,
            "stage_recut_row_count": 26,
            "first_image_internal_cut_count": 6,
            "second_image_internal_cut_count": 17,
            "pullback_internal_cut_count": 23,
            "common_refinement_actual_child_count": 24,
            "refined_homogeneous_subbranch_count": 24,
            "official_word_roof_level_counts": [2, 1, 2],
            "roof_level_count_per_refined_subbranch": 5,
            "slot_count_per_field": 120,
            "F1_F4_slot_count": 480,
            "F5_slot_count": 120,
            "F6_slot_count": 120,
            "F1_F6_total_slot_count": 720,
            "residual_root_count": 0,
            "residual_recut_count": 0,
            "residual_slot_count": 0,
        },
        "count ledger",
    )
    require(
        result["gate5_actual_child_field_status"]
        == {
            **{
                f"F{index}": "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
                for index in range(1, 7)
            },
            **{
                f"F{index}": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN"
                for index in range(7, 19)
            },
        },
        "Gate5 child fields",
    )
    require(result["rank3_seed_child_field_maturity"] == "6/18", "seed maturity")
    require(result["gate5_global_maturity"] == "10/18", "global maturity")
    require_integer(result["complete_18_field_block_count"], "complete block count")
    require_integer(result["gate5_block_count"], "Gate5 block count")
    require(result["complete_18_field_block_count"] == 0, "complete block")
    require(result["gate5_block_count"] == 0, "Gate5 block")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "CM2 verdict")
    require(
        result["boundary_owner_ledger"]
        == {
            "source_cell": (
                "[0,1); right endpoint is not the last cell in the Borel fibre"
            ),
            "image_parent_right_endpoint_open": True,
            "every_internal_natural_cut_owned_by_the_right_cell": True,
            "common_refinement_cells": (
                "[cut_rank,cut_rank+1) in source orientation"
            ),
            "coincident_artificial_cuts_use_conjunction_of_owner_predicates": True,
            "natural_c0_zero_b3_zero_boundaries_remain_singular_ledger": True,
            "this_seed_is_strictly_separated_from_c0_zero_and_b3_zero": True,
        },
        "boundary ledger",
    )
    require(
        result["strict_scope"]
        == (
            "one exact analytic b seed inside one Round113/Round117 BYPASS "
            "relative-interior operator cell, its 26 materialized stage input "
            "recuts, 23 pullback cuts, 24 common-refinement actual children, "
            "and child-local full-key F1-F6"
        ),
        "strict scope",
    )
    require(
        result["strict_nonclaims"]
        == [
            "the full Round120 Borel-b family is not numerically materialized or uniformly ranked",
            "no Round31 compact-Q2 time2 atom, parent-W ID, branch-rule ID, or recut ID is reused",
            "the designated BYPASS coordinate b3 is not a collision angle or homogeneity index",
            "F7-F18 are not installed on the Round121 exact-seed children",
            "24 seed children do not upgrade the global Gate5 10/18 maturity or create a complete block",
            "no endpoint-inclusive physical collar, cross-trace union reach, or whole-face atlas is claimed",
            "Gate5 and CM2 remain unavailable",
        ],
        "strict nonclaims",
    )
    require(type(result["upstream_and_helper_pins"]) is dict, "pins type")
    r120_pin_names = set(
        strict_json(ROUND120.read_text(encoding="utf-8"))["result"][
            "upstream_and_helper_pins"
        ]
    )
    expected_pin_names = r120_pin_names | {
        GATE4_COMPONENTWISE.name,
        DSTD.name,
        "cm2-one-hundred-twentieth-direct-assault-manifest-2026-07-23.sha256",
        ROUND120.name,
        "cm2_round120_rank3_relative_interior_actual_standard_curve_recut.py",
    }
    require(
        set(result["upstream_and_helper_pins"]) == expected_pin_names,
        "closed stored pin-key schema",
    )
    for name, expected in result["upstream_and_helper_pins"].items():
        require(type(name) is str and type(expected) is str, "pin row type")
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"stored pin target:{name}")
        require(sha256(path) == expected, f"stored pin value:{name}")
    require(
        all(
            result["upstream_and_helper_pins"].get(name) == expected
            for name, expected in UPSTREAM_PINS.items()
        ),
        "required pin subset",
    )
    return result


def stored_interval_contains_pair(
    stored: Any, fresh_lower: Q, fresh_upper: Q, label: str
) -> None:
    lower, upper = interval_contract(stored, label)
    require(lower <= fresh_lower and upper >= fresh_upper, f"{label}:dominance")


def expected_endpoint_id(seed_id: str, stage: int, natural_index: int) -> str:
    payload = [
        "round121-pullback-endpoint-v1",
        seed_id,
        f"U{stage}(x)={natural_index}*delta",
        stage,
        natural_index,
    ]
    return "round121-pullback-endpoint:" + digest(payload)


def expected_refined_id(seed_id: str, rank: int) -> str:
    return "round121-refined-subbranch:" + digest(
        [
            "round121-refined-subbranch-v1",
            SEED_OPERATOR_ID,
            seed_id,
            "source-k=0",
            rank,
        ]
    )


def expected_child_id(seed_id: str, refined_id: str, rank: int) -> str:
    return "round121-common-child:" + digest(
        ["round121-common-child-v1", refined_id, seed_id, rank]
    )


def mathematical_replay(
    result: dict[str, Any],
    values: dict[str, Any],
    idx: dict[str, Any],
    geometry: dict[str, Any],
) -> dict[str, Any]:
    seed_id = exact_seed_id()
    expected_pins = dict(values["r120"]["upstream_and_helper_pins"])
    expected_pins.update(
        {
            GATE4_COMPONENTWISE.name: UPSTREAM_PINS[GATE4_COMPONENTWISE.name],
            DSTD.name: UPSTREAM_PINS[DSTD.name],
            "cm2-one-hundred-twentieth-direct-assault-manifest-2026-07-23.sha256": (
                "8666b45917a29cef497f8e053629dc42456c3553e8ec6788860124d1d74c9c3d"
            ),
            ROUND120.name: UPSTREAM_PINS[ROUND120.name],
            "cm2_round120_rank3_relative_interior_actual_standard_curve_recut.py": (
                "ea1b4cd78a8009063e87cfe09b0d3fa80097f430a1f742d5f109761c20973a9a"
            ),
        }
    )
    require(
        result["upstream_and_helper_pins"] == expected_pins,
        "closed upstream/helper pin map",
    )
    source = replace(
        core_cert.physical_cores()[SEED_BRANCH[0]], chart_id=SEED_SOURCE_CHART
    )

    # Full frozen R113/R117/R120 crosswalk and candidate replay.
    pair_index, pattern_index, registry_digest = component.key_index_tables()
    parent = idx["parent"]
    c0_lower, c0_upper = map(Q, parent["parameter_box"]["c0"])
    b3_lower, b3_upper = map(Q, parent["parameter_box"]["b3"])
    fresh_parent = round113.audit_cell(
        idx["sheet112"],
        source,
        SEED_BRANCH,
        c0_lower,
        c0_upper,
        b3_lower,
        b3_upper,
        pair_index,
        pattern_index,
    )
    require(
        fresh_parent["official_path_id"]
        == parent["official_path_id"]
        == idx["row117"]["official_path_id_inherited"],
        "R113/R117 path crosswalk",
    )
    require(
        tuple(fresh_parent["official_word_key_ids"]) == OFFICIAL_WORD_IDS
        and fresh_parent["official_word_key_ids"]
        == parent["official_word_key_ids"]
        == idx["row117"]["official_word_key_ids_inherited"],
        "R113/R117 word crosswalk",
    )
    require(
        fresh_parent["ordered_regular_relative_interior_owner_ids"]
        == ["W[-1,-1]", "G[0,0]", SEED_ACTUAL_THIRD],
        "R113 owner replay",
    )
    replay = result["whole_seed_owner_candidate_replay"]
    require(
        replay
        == {
            "full_candidate_owner_path_chart_replay_passed": True,
            "ordered_owner_ids": ["W[-1,-1]", "G[0,0]", SEED_ACTUAL_THIRD],
            "selected_collision_charts": ["N", "S", "N"],
            "official_word_key_ids": list(OFFICIAL_WORD_IDS),
            "official_path_id": parent["official_path_id"],
            "BYPASS_actual_third_owner_id": SEED_ACTUAL_THIRD,
            "BYPASS_b3_is_collision_angle": False,
        },
        "whole seed replay contract",
    )
    require(
        idx["row120"]["ordered_owner_ids"] == replay["ordered_owner_ids"]
        and idx["row120"]["official_word_key_ids"]
        == replay["official_word_key_ids"]
        and idx["row120"]["actual_third_collision_contract"]["owner_id"]
        == SEED_ACTUAL_THIRD
        and idx["row120"]["actual_third_collision_contract"][
            "BYPASS_b3_is_collision_angle"
        ]
        is False,
        "Round120 seed restriction crosswalk",
    )
    require(
        idx["generator"]["family"]
        == "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0"
        and idx["generator"]["stable_id_interface_sample"][
            "sample_is_certified_nonempty_for_this_parent"
        ]
        is True,
        "R117 operator generator crosswalk",
    )

    # Independently validate the stored exact anchor bracket and partial-t
    # uniqueness, rather than trusting the producer's interval witness.
    witness = result["exact_parent_W_witness_rows"][0]
    stored_t_lower, stored_t_upper = map(
        Q, witness["anchor_t_unique_root_dyadic_bracket"]
    )
    lower_value = round113.equation_value(
        source,
        SEED_BRANCH,
        1,
        "BYPASS",
        stored_t_lower,
        SEED_C0,
        SEED_C0,
        SEED_B3,
        SEED_B3,
    )
    upper_value = round113.equation_value(
        source,
        SEED_BRANCH,
        1,
        "BYPASS",
        stored_t_upper,
        SEED_C0,
        SEED_C0,
        SEED_B3,
        SEED_B3,
    )
    require(
        (strict_sign(lower_value), strict_sign(upper_value)) == (1, -1),
        "stored anchor signs replay",
    )
    anchor_geometry = round113.path_geometry(
        source,
        SEED_BRANCH,
        1,
        "BYPASS",
        stored_t_lower,
        stored_t_upper,
        SEED_C0,
        SEED_C0,
        SEED_B3,
        SEED_B3,
    )
    partial_t = anchor_geometry["equation"].gradient[0]
    require(strict_sign(partial_t) == -1, "anchor partial t replay")
    partial_lower, partial_upper = arb_pair(-partial_t)
    require(
        0
        < qvalue(
            witness["anchor_root_partial_t_abs_strict_lower"],
            "stored partial t lower",
        )
        <= partial_lower,
        "anchor partial t lower replay",
    )
    require(
        stored_t_lower <= geometry["anchor"]["t_lower"]
        and stored_t_upper >= geometry["anchor"]["t_upper"],
        "stored anchor contains independent root enclosure",
    )
    theta_star = geometry["anchor"]["theta_ball"]
    b_star = aq(SEED_C0).acos() - aq(Q(36, 25)) * theta_star
    interval_encloses_cross_precision(
        witness["theta_star_enclosure"], theta_star, "stored theta"
    )
    interval_encloses_cross_precision(
        witness["b_star_enclosure"], b_star, "stored b"
    )

    source_row = result["source_adapted_cell_rows"][0]
    interval_encloses_cross_precision(
        source_row["slope_four_intercept_enclosure"],
        b_star,
        "source slope-four intercept",
    )
    zero, one = geometry["zero"], geometry["one"]
    c0_min = min(arb_pair(zero["c0"].value)[0], arb_pair(one["c0"].value)[0])
    c0_max = max(arb_pair(zero["c0"].value)[1], arb_pair(one["c0"].value)[1])
    b3_min = min(arb_pair(zero["b3"].value)[0], arb_pair(one["b3"].value)[0])
    b3_max = max(arb_pair(zero["b3"].value)[1], arb_pair(one["b3"].value)[1])
    source_c0_stored = interval_contract(source_row["c0_enclosure"], "source c0")
    source_b3_stored = interval_contract(source_row["b3_enclosure"], "source b3")
    require(source_c0_stored[1] == SEED_C0, "source c0 anchor upper")
    require(source_b3_stored[1] == SEED_B3, "source b3 anchor upper")
    # At x=0 these values are the exact rational anchor coordinates already
    # checked as the stored upper endpoints; evaluating their composite
    # formulas as Arb balls would only add irrelevant rounding overhang.
    interval_encloses_cross_precision(
        source_row["c0_enclosure"], one["c0"].value, "source c0 one"
    )
    interval_encloses_cross_precision(
        source_row["b3_enclosure"], one["b3"].value, "source b3 one"
    )
    # The source H0_CENTRAL_OUTER cutoff is independently checked using Arb.
    h128_boundary = (aq(Q(1, 128**2))).sin()
    require(
        bool(geometry["whole"]["c0"].value > h128_boundary),
        "source c0 above sin(128^-2)",
    )
    interval_contains(
        source_row["H128_upper_boundary_sin_128_minus_2_enclosure"],
        h128_boundary,
        "stored H128 boundary",
    )
    require(
        qvalue(
            source_row["c0_minus_H128_upper_boundary_strict_lower"],
            "stored source H128 margin",
        )
        <= arb_pair(geometry["whole"]["c0"].value - h128_boundary)[0],
        "source H128 margin replay",
    )
    require(
        Q(36, 61) == Q(36, 25) * Q(25, 61)
        == Q(4) * Q(9, 25) * Q(25, 61),
        "slope-four coefficient identity",
    )
    require(
        (Q(25, 9) + 4) * Q(9, 25) * Q(25, 61) == 1,
        "source adapted-density identity",
    )
    interval_encloses_cross_precision(
        source_row["c0_x_derivative_over_delta_enclosure"],
        geometry["c0_derivative"],
        "source c0 normalized derivative",
    )
    interval_encloses_cross_precision(
        source_row["b3_x_derivative_over_delta_enclosure"],
        geometry["b3_derivative"],
        "source b3 normalized derivative",
    )
    # Full F2 replay against the current Gate4 central cutoff.  Source uses
    # the stricter R117 outer cutoff above; both actual intermediate
    # collisions and the BYPASS actual third are independently central.
    gate4_boundary = (aq(Q(1, 6121**2))).sin()
    first_cosine = (
        arb(1) - geometry["whole"]["first"][6].value**2
    ).sqrt()
    second_cosine = (
        arb(1) - geometry["whole"]["second"][6].value**2
    ).sqrt()
    actual_third_cosine = (
        arb(1) - geometry["whole"]["actual_third"][6].value**2
    ).sqrt()
    require(
        bool(geometry["whole"]["c0"].value > gate4_boundary)
        and bool(first_cosine > gate4_boundary)
        and bool(second_cosine > gate4_boundary)
        and bool(actual_third_cosine > gate4_boundary),
        "four F2 central labels",
    )

    adapted = result["stage_adapted_coordinate_contract"]
    require(
        set(adapted)
        == {
            "stage_0",
            "stage_1",
            "stage_2",
            "stage_orientations",
            "adapted_coordinate_uses_both_normal_angle_and_momentum_angle",
            "stage_length_ratio_enclosures",
            "strict_simple_length_bounds",
            "whole_cell_normalized_derivative_enclosures",
            "whole_cell_strict_monotonicity",
        },
        "adapted coordinate schema",
    )
    require(
        adapted["stage_0"] == "u0(x)=delta*x"
        and adapted["stage_1"]
        == "a1=Theta_N(n1)+asin(p1); U1(x)=a1(0)-a1(x)"
        and adapted["stage_2"]
        == "a2=Theta_S(n2)+asin(p2); U2(x)=a2(x)-a2(0)"
        and adapted["stage_orientations"] == [1, -1, 1]
        and adapted[
            "adapted_coordinate_uses_both_normal_angle_and_momentum_angle"
        ]
        is True
        and adapted["whole_cell_strict_monotonicity"] is True,
        "adapted coordinate formulas",
    )
    for index, orientation in enumerate(adapted["stage_orientations"]):
        require_integer(orientation, f"stage orientation {index}")
    interval_encloses_cross_precision(
        adapted["stage_length_ratio_enclosures"]["U1_1_over_delta"],
        geometry["u1_ratio"],
        "U1 ratio",
    )
    interval_encloses_cross_precision(
        adapted["stage_length_ratio_enclosures"]["U2_1_over_delta"],
        geometry["u2_ratio"],
        "U2 ratio",
    )
    interval_encloses_cross_precision(
        adapted["whole_cell_normalized_derivative_enclosures"][
            "U1_prime_over_delta"
        ],
        geometry["u1_derivative"],
        "U1 derivative",
    )
    interval_encloses_cross_precision(
        adapted["whole_cell_normalized_derivative_enclosures"][
            "U2_prime_over_delta"
        ],
        geometry["u2_derivative"],
        "U2 derivative",
    )
    require(
        adapted["strict_simple_length_bounds"]
        == ["6<U1(1)/delta<7", "17<U2(1)/delta<18"],
        "simple length bounds",
    )

    # All 23 stored roots are independently sign-tested and matched to the
    # 180-step verifier roots.  The producer's numeric brackets are evidence,
    # never part of the endpoint identity.
    endpoints = result["pullback_endpoint_rows"]
    by_key = {(row["stage"], row["natural_index_j"]): row for row in endpoints}
    require(len(by_key) == 23, "endpoint key uniqueness")
    independent_by_key = {
        (row["stage"], row["natural_index_j"]): row
        for row in geometry["endpoints"]
    }
    for stage, count in ((1, 6), (2, 17)):
        function = geometry[f"u{stage}"]
        for natural_index in range(1, count + 1):
            row = by_key[(stage, natural_index)]
            require(
                row["endpoint_id"]
                == expected_endpoint_id(seed_id, stage, natural_index),
                "endpoint stable ID",
            )
            require(
                row["exact_parent_W_seed_id"] == seed_id
                and row["exact_root_equation_id"]
                == f"round121-U{stage}-equals-{natural_index}-delta"
                and row["exact_root_equation"]
                == f"U{stage}(x)={natural_index}*10^-90"
                and row["left_function_sign"] == -1
                and row["right_function_sign"] == 1
                and row["derivative_sign"] == 1
                and row["normalized_derivative_abs_strict_lower"]
                == ("6" if stage == 1 else "17")
                and row["unique_root_certified"] is True
                and row[
                    "numeric_bracket_or_Arb_text_participates_in_endpoint_ID"
                ]
                is False,
                "endpoint theorem fields",
            )
            low, high = interval_contract(row["x_dyadic_bracket"], "endpoint x")
            require(
                high - low
                <= qvalue(row["x_bracket_width_upper"], "endpoint width"),
                "endpoint width dominance",
            )
            target = aq(DELTA * natural_index)
            require(
                strict_sign(function(low) - target) == -1
                and strict_sign(function(high) - target) == 1,
                "endpoint independent signs",
            )
            independent = independent_by_key[(stage, natural_index)]
            require(
                low <= independent["upper"] and high >= independent["lower"],
                "independent endpoint overlap",
            )
            state = geometry["state_endpoint_hull"](low, high)
            interval_encloses_cross_precision(
                row["source_c0_enclosure"], state["c0"], "endpoint c0"
            )
            interval_encloses_cross_precision(
                row["source_t_enclosure"], state["t"], "endpoint t"
            )
            interval_encloses_cross_precision(
                row["source_b3_enclosure"], state["b3"], "endpoint b3"
            )
            require(
                row["lower_owner"]
                == f"stage-{stage}-natural-cell-{natural_index - 1}"
                and row["upper_owner"]
                == f"stage-{stage}-natural-cell-{natural_index}",
                "endpoint owner",
            )
    ordered = sorted(endpoints, key=lambda row: Q(row["x_dyadic_bracket"][0]))
    require(endpoints == ordered, "stored endpoint canonical order")
    require(
        tuple(f"S{row['stage']}:{row['natural_index_j']}" for row in ordered)
        == EXPECTED_CUT_ORDER,
        "stored endpoint order",
    )
    for left, right in zip(ordered, ordered[1:]):
        require(
            Q(right["x_dyadic_bracket"][0])
            - Q(left["x_dyadic_bracket"][1])
            > Q(1, 200),
            "stored endpoint separation",
        )

    # Materialized stage recuts and half-open ownership.
    left_boundary = source_boundary_id("left", seed_id)
    right_boundary = source_boundary_id("right", seed_id)
    recuts = result["stage_recut_rows"]
    recut_index = {
        (row["stage"], row["natural_index_j"]): row for row in recuts
    }
    require(len(recut_index) == 26, "recut key uniqueness")
    counts = (1, 7, 18)
    for stage, count in enumerate(counts):
        for natural_index in range(count):
            row = recut_index[(stage, natural_index)]
            expected_lower = (
                left_boundary
                if natural_index == 0
                else by_key[(stage, natural_index)]["endpoint_id"]
            )
            expected_upper = (
                right_boundary
                if natural_index == count - 1
                else by_key[(stage, natural_index + 1)]["endpoint_id"]
            )
            expected_coordinate = (
                "source-u0-exact-delta-x" if stage == 0 else f"image-U{stage}"
            )
            if stage == 0:
                expected_adapted_lower = "0"
                expected_adapted_upper = "1e-90"
            else:
                expected_adapted_lower = f"{natural_index}e-90"
                expected_adapted_upper = (
                    f"{natural_index + 1}e-90"
                    if natural_index < count - 1
                    else f"U{stage}(1)"
                )
            require(
                row["recut_instance_id"] == recut_id(seed_id, stage, natural_index)
                and row["exact_parent_W_seed_id"] == seed_id
                and row["adapted_coordinate_id"] == expected_coordinate
                and row["adapted_lower"] == expected_adapted_lower
                and row["adapted_upper"] == expected_adapted_upper
                and row["lower_endpoint_id"] == expected_lower
                and row["upper_endpoint_id"] == expected_upper
                and row["lower_closed"] is True
                and row["upper_closed"] is False
                and row["source_parent_right_endpoint_is_open"] is True
                and row["internal_cut_owned_by_right_natural_cell"] is True
                and row["actual_materialized_input_recut"] is True
                and row["official_word_key_id"] == OFFICIAL_WORD_IDS[stage]
                and row["roof_level_count"] == ROOF_COUNTS[stage]
                and row["adapted_length_upper"] == "1e-90",
                "stage recut identity/owner",
            )
            strict_lower = qvalue(
                row["normalized_adapted_length_strict_lower"],
                "recut normalized lower",
            )
            if stage == 0 or natural_index < count - 1:
                require(0 < strict_lower < 1, "full-cell strict lower")
            elif stage == 1:
                require(
                    0 < strict_lower < arb_pair(geometry["u1_ratio"])[0] - 6,
                    "stage1 terminal lower",
                )
            else:
                require(
                    0 < strict_lower < arb_pair(geometry["u2_ratio"])[0] - 17,
                    "stage2 terminal lower",
                )

    # Reconstruct all 24 common-refinement children and stable IDs.
    boundaries: list[dict[str, Any]] = [
        {
            "endpoint_id": left_boundary,
            "x_dyadic_bracket": ["0", "0"],
            "stage": 0,
            "natural_index_j": 0,
        },
        *ordered,
        {
            "endpoint_id": right_boundary,
            "x_dyadic_bracket": ["1", "1"],
            "stage": 0,
            "natural_index_j": 1,
        },
    ]
    common_rows = result["common_refinement_rows"]
    refined_rows = result["refined_homogeneous_subbranch_rows"]
    common_by_rank = {row["common_rank"]: row for row in common_rows}
    refined_by_rank = {row["common_rank"]: row for row in refined_rows}
    require(
        set(common_by_rank) == set(refined_by_rank) == set(range(24)),
        "common/refined ranks",
    )
    require(
        [row["common_rank"] for row in common_rows] == list(range(24))
        and [row["common_rank"] for row in refined_rows] == list(range(24)),
        "common/refined canonical order",
    )
    stage_indices = [0, 0, 0]
    for rank, (lower, upper) in enumerate(zip(boundaries, boundaries[1:])):
        common = common_by_rank[rank]
        refined = refined_by_rank[rank]
        refined_id = expected_refined_id(seed_id, rank)
        child_id = expected_child_id(seed_id, refined_id, rank)
        separation = Q(upper["x_dyadic_bracket"][0]) - Q(
            lower["x_dyadic_bracket"][1]
        )
        require(
            separation
            > qvalue(
                common["positive_source_x_length_strict_lower"],
                "common positive length",
            ),
            "common positive length replay",
        )
        require(
            common["common_child_id"] == child_id
            and common["refined_homogeneous_subbranch_id"] == refined_id
            and common["source_x_lower_endpoint_id"] == lower["endpoint_id"]
            and common["source_x_upper_endpoint_id"] == upper["endpoint_id"]
            and common["covering_stage_indices"] == stage_indices
            and common["source_recut_instance_id"] == recut_id(seed_id, 0, 0)
            and common["first_image_recut_instance_id"]
            == recut_id(seed_id, 1, stage_indices[1])
            and common["second_image_recut_instance_id"]
            == recut_id(seed_id, 2, stage_indices[2])
            and common["lower_closed"] is True
            and common["upper_closed"] is False
            and common["source_parent_right_endpoint_is_open"] is True
            and common[
                "all_three_inputs_contained_in_one_materialized_canonical_cell"
            ]
            is True
            and common["round117_operator_cell_id"] == SEED_OPERATOR_ID
            and common["official_path_id"] == parent["official_path_id"]
            and common["actual_standard_curve_child_installed"] is True,
            "common child replay",
        )
        require(
            refined["refined_homogeneous_subbranch_id"] == refined_id
            and refined["common_child_id"] == child_id
            and refined["round117_operator_cell_id"] == SEED_OPERATOR_ID
            and refined["exact_parent_W_seed_id"] == seed_id
            and refined["source_adapted_index_k"] == 0
            and refined["physical_homogeneity"]
            == {
                "source": "H0_CENTRAL_OUTER",
                "collision_1": "H0_CENTRAL",
                "collision_2": "H0_CENTRAL",
                "actual_BYPASS_collision_3": "H0_CENTRAL",
                "designated_b3_is_a_collision_angle": False,
            },
            "refined subbranch replay",
        )
        if rank < 23:
            stage_indices[upper["stage"]] += 1
    require(stage_indices == [0, 6, 17], "terminal stage indices")

    # All 720 full-key rows are reconstructed from the frozen Round120 roof
    # factorization.  Roof=2 duplicates the one collision bound at two
    # prefix/suffix factor levels, but every slot ID is distinct.
    frontier = idx["row120"]["three_step_adapted_recut_frontier_schema_rows"]
    expected_slots: list[dict[str, Any]] = []
    for common in common_rows:
        refined_id = common["refined_homogeneous_subbranch_id"]
        stage_recuts = (
            common["source_recut_instance_id"],
            common["first_image_recut_instance_id"],
            common["second_image_recut_instance_id"],
        )
        for stage_row in frontier:
            stage = stage_row["stage"]
            for chart_pair in stage_row["roof_level_chart_pairs"]:
                roof = chart_pair["roof_level_j"]
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
                        value = str(THETA)
                    else:
                        value = str(ONE_STEP_LOG_VARIATION)
                    key = [
                        stage_row["official_word_key_id"],
                        refined_id,
                        roof,
                        field_name,
                    ]
                    expected_slots.append(
                        {
                            "slot_id": "round121-gate5-slot:" + digest(key),
                            "immutable_slot_key": key,
                            "official_word_key_id": stage_row[
                                "official_word_key_id"
                            ],
                            "refined_homogeneous_subbranch_id": refined_id,
                            "common_child_id": common["common_child_id"],
                            "stage": stage,
                            "roof_level_j": roof,
                            "field_index": field_index,
                            "field_name": field_name,
                            "field_value_or_contract": value,
                            "materialized_input_recut_instance_id": stage_recuts[
                                stage
                            ],
                            "slot_status": (
                                "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD"
                            ),
                            "transparent_wall_roof_split_does_not_add_a_collision_Jacobian_factor": (
                                stage_row["roof_level_count"] == 2
                            ),
                        }
                    )
    require(result["gate5_F1_F6_slot_rows"] == expected_slots, "720 slot replay")
    require(len({row["slot_id"] for row in expected_slots}) == 720, "slot IDs unique")
    for common in common_rows:
        child_slots = [
            row
            for row in expected_slots
            if row["common_child_id"] == common["common_child_id"]
        ]
        for stage, roof_count in enumerate(ROOF_COUNTS):
            for field_index in (5, 6):
                rows = [
                    row
                    for row in child_slots
                    if row["stage"] == stage and row["field_index"] == field_index
                ]
                require(len(rows) == roof_count, "F5/F6 roof replication count")
                require(
                    len({row["slot_id"] for row in rows}) == roof_count
                    and len(
                        {
                            row["materialized_input_recut_instance_id"]
                            for row in rows
                        }
                    )
                    == 1,
                    "roof split distinct slots same collision recut",
                )

    theorem = result["three_leg_restriction_theorem"]
    require_integer(theorem["actual_input_stage_count"], "theorem stage count")
    universal = values["universal"]["result"][
        "universal_full_collision_branch_templates"
    ]
    require(
        universal["canonical_adapted_length_upper"] == "1e-90"
        and universal["field_5_inverse_Jacobian_seed"][
            "universal_adapted_inverse_strict_upper"
        ]
        == str(THETA)
        and universal["field_6_log_Jacobian_distortion_seed"][
            "canonical_curve_log_variation_strict_upper"
        ]
        == str(ONE_STEP_LOG_VARIATION)
        and universal["scope"].startswith(
            "every actual homogeneous physical solid-collision child"
        ),
        "universal F5/F6 scope",
    )
    require(
        values["cone"]["result"]["global_invariant_geometric_cone"][
            "strict_forward_invariance"
        ]
        is True,
        "global cone replay",
    )
    require(
        values["dstd"]["replay_summary"]["global_D_std_strict_upper"]
        == "30000000",
        "D_std replay",
    )
    require(
        values["g4c"]["replay_summary"]["homogeneity_cutoff_k0"] == 6121,
        "Gate4 homogeneity cutoff",
    )
    require(
        set(theorem)
        == {
            "actual_input_stage_count",
            "each_materialized_adapted_cell_length_at_most_delta",
            "each_Ti_child_inside_one_materialized_adapted_natural_cell",
            "invariant_cone_strict_forward_invariance",
            "global_D_std_strict_upper",
            "universal_one_step_F5_adapted_inverse_strict_upper",
            "universal_one_step_F6_log_variation_strict_upper",
            "restriction_does_not_increase_pointwise_inverse_upper",
            "restriction_does_not_increase_log_Jacobian_oscillation",
            "full_key_child_restriction_binding_installed",
            "transparent_wall_roof_levels_are_prefix_suffix_splits_of_one_collision_leg",
            "transparent_wall_roof_levels_do_not_add_Jacobian_factors",
            "area_Jacobian_one_used_as_F5",
            "three_leg_F5_path_product_strict_upper",
            "three_leg_F6_path_sum_strict_upper",
            "Round120_universal_template_scope_replayed",
            "Round120_frontier_missing_actual_recut_and_full_key_binding_paid_here",
        },
        "restriction theorem schema",
    )
    require(
        theorem["actual_input_stage_count"] == 3
        and theorem["each_materialized_adapted_cell_length_at_most_delta"] is True
        and theorem["each_Ti_child_inside_one_materialized_adapted_natural_cell"]
        is True
        and theorem["invariant_cone_strict_forward_invariance"] is True
        and theorem["global_D_std_strict_upper"] == "30000000"
        and theorem["universal_one_step_F5_adapted_inverse_strict_upper"]
        == str(THETA)
        and theorem["universal_one_step_F6_log_variation_strict_upper"]
        == str(ONE_STEP_LOG_VARIATION)
        and theorem["restriction_does_not_increase_pointwise_inverse_upper"]
        is True
        and theorem[
            "restriction_does_not_increase_log_Jacobian_oscillation"
        ]
        is True
        and theorem["full_key_child_restriction_binding_installed"] is True
        and theorem[
            "transparent_wall_roof_levels_are_prefix_suffix_splits_of_one_collision_leg"
        ]
        is True
        and theorem["transparent_wall_roof_levels_do_not_add_Jacobian_factors"]
        is True
        and theorem["area_Jacobian_one_used_as_F5"] is False
        and qvalue(
            theorem["three_leg_F5_path_product_strict_upper"], "F5 product"
        )
        == THREE_STEP_THETA
        and qvalue(theorem["three_leg_F6_path_sum_strict_upper"], "F6 sum")
        == THREE_STEP_LOG_VARIATION
        and theorem["Round120_universal_template_scope_replayed"]
        == universal["scope"]
        and theorem[
            "Round120_frontier_missing_actual_recut_and_full_key_binding_paid_here"
        ]
        is True,
        "restriction theorem",
    )
    return {
        "official_candidate_registry_rows_sha256": registry_digest,
        "anchor_partial_t_abs_lower": str(partial_lower),
        "independent_U1_length_ratio_enclosure": padded_pair(
            geometry["u1_ratio"], Q(1, 10**130)
        ),
        "independent_U2_length_ratio_enclosure": padded_pair(
            geometry["u2_ratio"], Q(1, 10**130)
        ),
        "independent_U1_derivative_ratio_enclosure": padded_pair(
            geometry["u1_derivative"], Q(1, 10**80)
        ),
        "independent_U2_derivative_ratio_enclosure": padded_pair(
            geometry["u2_derivative"], Q(1, 10**80)
        ),
        "independently_replayed_endpoint_count": len(endpoints),
        "independently_replayed_stage_recut_count": len(recuts),
        "independently_replayed_common_child_count": len(common_rows),
        "independently_replayed_refined_subbranch_count": len(refined_rows),
        "independently_replayed_full_key_slot_count": len(expected_slots),
        "independent_minimum_pullback_x_separation_lower": str(
            min(
                Q(right["x_dyadic_bracket"][0])
                - Q(left["x_dyadic_bracket"][1])
                for left, right in zip(ordered, ordered[1:])
            )
        ),
    }


def resign_document(document: dict[str, Any]) -> None:
    result = document["result"]
    for rows_key, digest_key, row_sha_key in (
        ("stage_recut_rows", "stage_recut_rows_sha256", "row_sha256"),
        (
            "pullback_endpoint_rows",
            "pullback_endpoint_rows_sha256",
            "evidence_sha256",
        ),
        ("common_refinement_rows", "common_refinement_rows_sha256", "row_sha256"),
        (
            "refined_homogeneous_subbranch_rows",
            "refined_homogeneous_subbranch_rows_sha256",
            "row_sha256",
        ),
    ):
        for row in result[rows_key]:
            row[row_sha_key] = row_digest(row, row_sha_key)
        result[digest_key] = digest(result[rows_key])
    result["gate5_F1_F6_slot_rows_sha256"] = digest(
        result["gate5_F1_F6_slot_rows"]
    )
    document["result_sha256"] = digest(result)


def assign(root: Any, path: tuple[Any, ...], value: Any) -> None:
    cursor = root
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def semantic_mutation_tests(
    document: dict[str, Any],
    values: dict[str, Any],
    idx: dict[str, Any],
    geometry: dict[str, Any],
) -> list[str]:
    """Re-sign hostile mutations and require contract or replay rejection."""

    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def path_attack(label: str, path: tuple[Any, ...], value: Any) -> None:
        attacks.append((label, lambda mutant, p=path, v=value: assign(mutant, p, v)))

    path_attack("global_gate_upgrade", ("result", "gate5_global_maturity"), "11/18")
    path_attack("child_maturity_upgrade", ("result", "rank3_seed_child_field_maturity"), "7/18")
    path_attack("complete_block_forgery", ("result", "complete_18_field_block_count"), 1)
    path_attack("gate5_block_forgery", ("result", "gate5_block_count"), 1)
    path_attack("cm2_upgrade", ("result", "cm2_verdict"), "GO_FOR_CLAIM")
    path_attack(
        "F7_upgrade",
        ("result", "gate5_actual_child_field_status", "F7"),
        "CERTIFIED",
    )
    path_attack("seed_count_forgery", ("result", "count_ledger", "exact_b_seed_count"), 2)
    path_attack(
        "count_bool_as_int",
        ("result", "count_ledger", "exact_b_seed_count"),
        True,
    )
    path_attack("residual_root_forgery", ("result", "count_ledger", "residual_root_count"), 1)
    path_attack("slot_count_forgery", ("result", "count_ledger", "F1_F6_total_slot_count"), 719)
    path_attack("strict_scope_widening", ("result", "strict_scope"), "all Borel b")
    path_attack(
        "old_angular_lift",
        ("result", "exact_seed_contract", "angular_lift_id"),
        "G:W:k0",
    )
    path_attack(
        "decimal_seed_ID",
        ("result", "exact_seed_contract", "Arb_decimal_or_numeric_bracket_participates_in_ID"),
        True,
    )
    path_attack(
        "seed_parent_swap",
        ("result", "exact_seed_contract", "round113_parent_id"),
        "round113-cell:forged",
    )
    path_attack(
        "anchor_partial_t_inflation",
        ("result", "exact_parent_W_witness_rows", 0, "anchor_root_partial_t_abs_strict_lower"),
        "100",
    )
    path_attack(
        "anchor_partial_t_sign_flip",
        ("result", "exact_parent_W_witness_rows", 0, "anchor_root_partial_t_sign"),
        1,
    )
    path_attack(
        "source_H0_erasure",
        ("result", "source_adapted_cell_rows", 0, "source_H0_CENTRAL_OUTER_membership_whole_cell"),
        False,
    )
    path_attack(
        "source_c0_orientation_flip",
        ("result", "source_adapted_cell_rows", 0, "c0_x_derivative_sign"),
        1,
    )
    path_attack(
        "source_b3_orientation_flip",
        ("result", "source_adapted_cell_rows", 0, "b3_x_derivative_sign"),
        1,
    )
    path_attack(
        "source_adapted_density_mutation",
        ("result", "source_adapted_cell_rows", 0, "source_adapted_density"),
        "1",
    )
    path_attack(
        "source_adapted_identity_mutation",
        ("result", "source_adapted_cell_rows", 0, "source_adapted_coordinate_identity"),
        "area-Jacobian=1",
    )
    path_attack(
        "source_slope_four_erasure",
        ("result", "source_adapted_cell_rows", 0, "p0_equals_sin_4r_plus_b_star_whole_cell"),
        False,
    )
    path_attack(
        "source_theta_coefficient_mutation",
        ("result", "source_adapted_cell_rows", 0, "theta0"),
        "theta*+(26/61)*delta*x",
    )
    path_attack(
        "source_phi_coefficient_mutation",
        ("result", "source_adapted_cell_rows", 0, "phi0"),
        "arccos(1/16384)+(35/61)*delta*x",
    )
    path_attack(
        "source_b3_formula_mutation",
        ("result", "source_adapted_cell_rows", 0, "b3"),
        "sqrt(+Delta3(t,c0))/(4/25)",
    )
    path_attack(
        "source_adapted_coordinate_formula_mutation",
        ("result", "source_adapted_cell_rows", 0, "source_adapted_coordinate"),
        "u0(x)=2*delta*x",
    )
    path_attack(
        "slope_intercept_enclosure_shift",
        ("result", "source_adapted_cell_rows", 0, "slope_four_intercept_enclosure"),
        ["0", "1"],
    )
    path_attack(
        "stage_orientation_flip",
        ("result", "stage_adapted_coordinate_contract", "stage_orientations", 1),
        1,
    )
    path_attack(
        "adapted_normal_only",
        (
            "result",
            "stage_adapted_coordinate_contract",
            "adapted_coordinate_uses_both_normal_angle_and_momentum_angle",
        ),
        False,
    )
    path_attack(
        "BYPASS_designated_owner",
        ("result", "whole_seed_owner_candidate_replay", "BYPASS_actual_third_owner_id"),
        "W[-1,-2]",
    )
    path_attack(
        "BYPASS_b3_collision_angle",
        ("result", "whole_seed_owner_candidate_replay", "BYPASS_b3_is_collision_angle"),
        True,
    )
    path_attack(
        "area_Jacobian_as_F5",
        ("result", "three_leg_restriction_theorem", "area_Jacobian_one_used_as_F5"),
        True,
    )
    path_attack(
        "wall_adds_Jacobian",
        (
            "result",
            "three_leg_restriction_theorem",
            "transparent_wall_roof_levels_do_not_add_Jacobian_factors",
        ),
        False,
    )
    path_attack(
        "F5_path_virtual_improvement",
        ("result", "three_leg_restriction_theorem", "three_leg_F5_path_product_strict_upper"),
        "1/10",
    )
    path_attack(
        "F6_path_not_summed",
        ("result", "three_leg_restriction_theorem", "three_leg_F6_path_sum_strict_upper"),
        "3/200000",
    )
    path_attack(
        "common_right_endpoint_closed",
        ("result", "common_refinement_rows", 0, "upper_closed"),
        True,
    )
    path_attack(
        "common_rank_bool_as_int",
        ("result", "common_refinement_rows", 1, "common_rank"),
        True,
    )
    path_attack(
        "common_stage_index_swap",
        ("result", "common_refinement_rows", 5, "covering_stage_indices"),
        [0, 0, 0],
    )
    path_attack(
        "common_length_inflation",
        ("result", "common_refinement_rows", 0, "positive_source_x_length_strict_lower"),
        "1",
    )
    path_attack(
        "refined_b3_as_angle",
        (
            "result",
            "refined_homogeneous_subbranch_rows",
            0,
            "physical_homogeneity",
            "designated_b3_is_a_collision_angle",
        ),
        True,
    )
    path_attack(
        "recut_right_endpoint_closed",
        ("result", "stage_recut_rows", 0, "upper_closed"),
        True,
    )
    path_attack(
        "recut_strict_lower_equal_length",
        ("result", "stage_recut_rows", 0, "normalized_adapted_length_strict_lower"),
        "1",
    )
    path_attack(
        "recut_coordinate_mutation",
        ("result", "stage_recut_rows", 1, "adapted_coordinate_id"),
        "image-U2",
    )
    path_attack(
        "recut_adapted_lower_mutation",
        ("result", "stage_recut_rows", 2, "adapted_lower"),
        "0e-90",
    )
    path_attack(
        "recut_adapted_upper_mutation",
        ("result", "stage_recut_rows", 7, "adapted_upper"),
        "7e-90",
    )
    path_attack(
        "endpoint_numeric_ID",
        (
            "result",
            "pullback_endpoint_rows",
            0,
            "numeric_bracket_or_Arb_text_participates_in_endpoint_ID",
        ),
        True,
    )
    path_attack(
        "endpoint_owner_swap",
        ("result", "pullback_endpoint_rows", 0, "upper_owner"),
        "stage-2-natural-cell-0",
    )
    path_attack(
        "endpoint_derivative_inflation",
        ("result", "pullback_endpoint_rows", 0, "normalized_derivative_abs_strict_lower"),
        "100",
    )
    path_attack(
        "slot_F5_virtual_improvement",
        ("result", "gate5_F1_F6_slot_rows", 4, "field_value_or_contract"),
        "1/10",
    )
    path_attack(
        "slot_field_index_bool_as_int",
        ("result", "gate5_F1_F6_slot_rows", 0, "field_index"),
        True,
    )
    path_attack(
        "slot_roof_bool_as_int",
        ("result", "gate5_F1_F6_slot_rows", 0, "roof_level_j"),
        False,
    )
    path_attack(
        "slot_roof_out_of_range",
        ("result", "gate5_F1_F6_slot_rows", 0, "roof_level_j"),
        2,
    )
    path_attack(
        "slot_recut_mismatch",
        ("result", "gate5_F1_F6_slot_rows", 0, "materialized_input_recut_instance_id"),
        "round121-recut-instance:forged",
    )
    path_attack(
        "upstream_pin_mutation",
        (
            "result",
            "upstream_and_helper_pins",
            "cm2-round120-rank3-relative-interior-actual-standard-curve-recut-2026-07-23.json",
        ),
        "0" * 64,
    )
    path_attack(
        "nonreduced_fraction",
        ("result", "exact_parent_W_witness_rows", 0, "anchor_root_partial_t_abs_strict_lower"),
        "2/4",
    )
    path_attack(
        "zero_denominator_fraction",
        ("result", "pullback_endpoint_rows", 0, "x_bracket_width_upper"),
        "1/0",
    )
    path_attack(
        "negative_denominator_fraction",
        ("result", "common_refinement_rows", 0, "positive_source_x_length_strict_lower"),
        "1/-2",
    )
    path_attack(
        "leading_zero_fraction",
        ("result", "source_adapted_cell_rows", 0, "c0_minus_H128_upper_boundary_strict_lower"),
        "01/2",
    )
    path_attack(
        "wrong_type_count",
        ("result", "count_ledger", "exact_b_seed_count"),
        "1",
    )
    path_attack(
        "wrong_type_endpoint_stage",
        ("result", "pullback_endpoint_rows", 0, "stage"),
        "2",
    )
    path_attack(
        "wrong_type_slot_roof",
        ("result", "gate5_F1_F6_slot_rows", 0, "roof_level_j"),
        "0",
    )

    attacks.extend(
        [
            (
                "endpoint_deleted",
                lambda mutant: mutant["result"]["pullback_endpoint_rows"].pop(),
            ),
            (
                "endpoint_duplicated",
                lambda mutant: mutant["result"]["pullback_endpoint_rows"].append(
                    copy.deepcopy(mutant["result"]["pullback_endpoint_rows"][-1])
                ),
            ),
            (
                "endpoint_reordered",
                lambda mutant: mutant["result"]["pullback_endpoint_rows"].reverse(),
            ),
            (
                "recut_deleted",
                lambda mutant: mutant["result"]["stage_recut_rows"].pop(),
            ),
            (
                "common_child_deleted",
                lambda mutant: mutant["result"]["common_refinement_rows"].pop(),
            ),
            (
                "refined_subbranch_duplicated",
                lambda mutant: mutant["result"][
                    "refined_homogeneous_subbranch_rows"
                ].append(
                    copy.deepcopy(
                        mutant["result"]["refined_homogeneous_subbranch_rows"][-1]
                    )
                ),
            ),
            (
                "slot_deleted",
                lambda mutant: mutant["result"]["gate5_F1_F6_slot_rows"].pop(),
            ),
            (
                "slot_reordered",
                lambda mutant: mutant["result"]["gate5_F1_F6_slot_rows"].reverse(),
            ),
            (
                "strict_nonclaim_deleted",
                lambda mutant: mutant["result"]["strict_nonclaims"].pop(),
            ),
            (
                "unknown_result_field",
                lambda mutant: mutant["result"].__setitem__("unknown_round121", 1),
            ),
            (
                "unknown_endpoint_field",
                lambda mutant: mutant["result"]["pullback_endpoint_rows"][0].__setitem__(
                    "unknown_round121", 1
                ),
            ),
            (
                "unknown_slot_field",
                lambda mutant: mutant["result"]["gate5_F1_F6_slot_rows"][0].__setitem__(
                    "unknown_round121", 1
                ),
            ),
            (
                "unknown_pin_row",
                lambda mutant: mutant["result"]["upstream_and_helper_pins"].__setitem__(
                    "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py",
                    sha256(Path(__file__).resolve()),
                ),
            ),
            (
                "missing_result_field",
                lambda mutant: mutant["result"].pop("boundary_owner_ledger"),
            ),
            (
                "missing_endpoint_field",
                lambda mutant: mutant["result"]["pullback_endpoint_rows"][0].pop(
                    "lower_owner"
                ),
            ),
        ]
    )

    # Deep numeric attacks that preserve every enclosing digest.
    def shift_anchor(mutant: dict[str, Any]) -> None:
        row = mutant["result"]["exact_parent_W_witness_rows"][0]
        lower, upper = map(Q, row["anchor_t_unique_root_dyadic_bracket"])
        width = upper - lower
        row["anchor_t_unique_root_dyadic_bracket"] = [
            str(lower + 10 * width),
            str(upper + 10 * width),
        ]

    attacks.append(("anchor_bracket_shift", shift_anchor))

    def shrink_U2_derivative_enclosure(mutant: dict[str, Any]) -> None:
        row = mutant["result"]["stage_adapted_coordinate_contract"][
            "whole_cell_normalized_derivative_enclosures"
        ]
        lower, upper = map(Q, row["U2_prime_over_delta"])
        midpoint = (lower + upper) / 2
        half_width = (upper - lower) / 200
        row["U2_prime_over_delta"] = [
            str(midpoint - half_width),
            str(midpoint + half_width),
        ]

    attacks.append(("U2_derivative_enclosure_shrink", shrink_U2_derivative_enclosure))

    def shift_endpoint(mutant: dict[str, Any]) -> None:
        row = mutant["result"]["pullback_endpoint_rows"][0]
        lower, upper = map(Q, row["x_dyadic_bracket"])
        width = upper - lower
        row["x_dyadic_bracket"] = [str(lower + Q(1, 100)), str(upper + Q(1, 100))]
        row["x_bracket_width_upper"] = str(width)

    attacks.append(("endpoint_bracket_shift", shift_endpoint))

    rejected: list[str] = []
    for label, mutate in attacks:
        mutant = copy.deepcopy(document)
        mutate(mutant)
        try:
            resign_document(mutant)
            mutated_result = static_contract(mutant)
            mathematical_replay(mutated_result, values, idx, geometry)
        except (KeyError, IndexError, StopIteration, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"semantic mutation accepted:{label}")
    require(len(rejected) == len(attacks), "semantic attack census")
    return rejected


def strict_json_tests() -> list[str]:
    payloads = {
        "duplicate_top_key": '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        "duplicate_nested_key": '{"schema":"x","result":{"a":1,"a":2},"result_sha256":"z"}',
        "duplicate_deep_key": '{"a":{"b":{"c":1,"c":2}}}',
        "nan": '{"x":NaN}',
        "positive_infinity": '{"x":Infinity}',
        "negative_infinity": '{"x":-Infinity}',
        "json_float": '{"x":1.25}',
        "overflowing_float": '{"x":1e9999}',
        "negative_zero": '{"x":-0}',
        "top_level_array": "[]",
        "top_level_null": "null",
        "utf8_bom": '\ufeff{"x":1}',
        "unpaired_high_surrogate": '{"x":"\\ud800"}',
        "unpaired_low_surrogate": '{"x":"\\udfff"}',
        "oversized_integer": '{"x":' + "1" * 1025 + "}",
    }
    rejected: list[str] = []
    for label, payload in payloads.items():
        try:
            strict_json(payload)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict JSON mutation accepted:{label}")
    return rejected


def verify(
    certificate: Path = DEFAULT_CERTIFICATE,
    precision_bits: int = VERIFIER_PRECISION_BITS,
    attacks: bool = True,
) -> dict[str, Any]:
    require(
        type(precision_bits) is int
        and not isinstance(precision_bits, bool)
        and precision_bits >= 1536,
        "verifier precision",
    )
    require(type(attacks) is bool, "attacks flag")
    ctx.prec = precision_bits
    document = strict_json(certificate.read_text(encoding="utf-8"))
    result = static_contract(document)
    values = load_inputs()
    idx = seed_indexes(values)
    geometry = independent_geometry(values, idx)
    replay = mathematical_replay(result, values, idx, geometry)
    semantic = (
        semantic_mutation_tests(document, values, idx, geometry) if attacks else []
    )
    strict = strict_json_tests() if attacks else []
    verification = {
        "verdict": "PASS",
        "verification_precision_bits": precision_bits,
        "round121_producer_module_imported": False,
        "shared_round121_mathematics_helper_imported": False,
        "upstream_R113_R117_R120_seed_crosswalk_verified": True,
        "exact_anchor_root_and_partial_t_uniqueness_verified": True,
        "source_slope_four_and_adapted_density_identities_verified": True,
        "whole_source_c0_and_b3_strictly_decreasing_verified": True,
        "four_F2_homogeneity_labels_independently_replayed": True,
        "stage_orientations": [1, -1, 1],
        "stage_natural_cell_counts": [1, 7, 18],
        "pullback_internal_cut_count": 23,
        "common_refinement_actual_child_count": 24,
        "refined_homogeneous_subbranch_count": 24,
        "full_key_F1_F6_slot_count": 720,
        "F5_slot_count": 120,
        "F6_slot_count": 120,
        "roof_two_is_prefix_suffix_factorization_not_extra_collision": True,
        "rank3_seed_child_field_maturity": "6/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        **replay,
        "attacks_enabled": attacks,
        "semantic_mutations_rejected": len(semantic),
        "semantic_mutation_labels": semantic,
        "strict_json_attacks_rejected": len(strict),
        "strict_json_attack_labels": strict,
        "certificate_sha256": sha256(certificate),
        "verified_upstream_and_helper_pin_count": len(
            result["upstream_and_helper_pins"]
        ),
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--precision-bits", type=int, default=VERIFIER_PRECISION_BITS
    )
    parser.add_argument(
        "--attacks",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="run re-signed semantic and strict-JSON attacks (default: enabled)",
    )
    args = parser.parse_args()
    document = verify(
        certificate=args.certificate,
        precision_bits=args.precision_bits,
        attacks=args.attacks,
    )
    rendered = json.dumps(
        document, indent=2, sort_keys=True, ensure_ascii=True
    ) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
