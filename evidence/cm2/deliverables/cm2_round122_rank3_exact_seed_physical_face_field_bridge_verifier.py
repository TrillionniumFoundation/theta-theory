#!/usr/bin/env python3
"""Independent Round122 exact-seed parameter-collar verifier.

The verifier intentionally does not import the Round122 producer or any
Round122 proof helper.  Its core starts from the frozen Round113/117/120/121
objects, isolates the exact Round121 seed again, and evaluates the fixed-gauge
horizontal W-translation with a native two-variable second-order interval jet.

The core replay certifies, at 3072-bit precision:

* the complete 57+55+57 candidate universes on ``|s| <= 2^-512``;
* the same three actual owners, charts, and strict future-root ordering;
* all 6+17 moving adapted-recut faces and their first/second implicit
  parameter derivatives;
* persistence and strict ordering of the 23 face tubes and hence all 24
  common-refinement children.

The certificate contract and mutation suite are deliberately kept separate
from this mathematical layer so that they can be bound to the final producer
schema without sharing any producer code.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq, interval
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
)
CERTIFICATE_SCHEMA = "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1"
VERIFICATION_SCHEMA = (
    "cm2.round122.rank3-exact-seed-physical-face-field-bridge-verification.v1"
)
VERIFIER_PRECISION_BITS = 3072

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
ROUND121 = (
    HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
)

UPSTREAM_PINS = {
    ROUND113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND117.name: "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND120.name: "a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5",
    ROUND121.name: "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
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
PARAMETER_RADIUS = Q(1, 2**512)
ROOT_BISECTIONS = 1152
FACE_BISECTIONS = 384
FACE_TUBE_PADDING = Q(1, 2**180)

OFFICIAL_WORD_IDS = (
    "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
    "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e",
    "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
)
ROOF_COUNTS = (2, 1, 2)
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

# Final child-local field constants.  In particular F7 is the actual
# density-corrected field value, not the bare characteristic Xi.
F7_DENSITY_RATIO = Q(2000, 1999)
F7_XI = Q(900337, 901685)
F7_ACTUAL = Q(360134800, 360493663)
F8_WEDGE_LOWER = Q(1, 6)
F9_STAGE_BOUNDS = {
    1: Q(80253367137726629098291200),
    2: Q(310359909615573026525432020225398669312000000),
}
F11_STAGE_BOUNDS = {0: Q(4915200), 1: Q(2457600), 2: Q(2457600)}
F12_STAGE_BOUNDS = {
    0: Q(29686813949952000001),
    1: Q(6039797760001),
    2: Q(2457601),
}
NEW_FIELDS = (
    (7, "one_step_cut_growth_Z_sum"),
    (8, "face_transversality_lower"),
    (9, "face_C2_atlas_bound"),
    (10, "coarea_density_regular_bound"),
    (11, "dynamic_Holder_test_pullback_bound"),
    (12, "C1_face_trace_pullback_bound"),
    (13, "moving_boundary_DQ_current_and_two_traces"),
    (16, "flux_face_operator_cost"),
)
SAFE_PHYSICAL_MARGINS = {
    "candidate_tangency": Q(1, 10**12),
    "coordinate_velocity_zero": Q(1, 10),
    "core_face": Q(1, 3),
    "integer_corner_ray": Q(1, 20),
    "owner_gap": Q(9, 10),
    "root_sign": Q(1, 10),
    "source_chart_seam": Q(1, 10),
    "source_endpoint_wall": Q(1, 25),
    "source_homogeneity": Q(1, 10**14),
    "target_chart_seam": Q(1, 25),
    "target_endpoint_wall": Q(1, 5),
    "target_homogeneity": Q(4, 5),
}
EXPECTED_PHYSICAL_COUNTS = {
    "candidate_tangency": 4056,
    "coordinate_velocity_zero": 144,
    "core_face": 1152,
    "integer_corner_ray": 2040,
    "owner_gap": 144,
    "root_sign": 384,
    "source_chart_seam": 72,
    "source_endpoint_wall": 72,
    "source_homogeneity": 72,
    "target_chart_seam": 72,
    "target_endpoint_wall": 72,
    "target_homogeneity": 72,
}

RESULT_KEYS = set(
    """precision_bits round121_contract parameter_collar_contract
    physical_face_typed_empty_audit physical_face_typed_empty_audit_sha256
    physical_five_face_grammar_rows physical_five_face_grammar_rows_sha256
    physical_seven_boundary_kind_rows physical_seven_boundary_kind_rows_sha256
    parameterized_recut_face_rows parameterized_recut_face_rows_sha256
    stationary_outer_face_rows stationary_outer_face_rows_sha256
    recut_face_trace_rows recut_face_trace_rows_sha256
    child_face_incidence_rows child_face_incidence_rows_sha256 dynamic_F11_rows
    gate5_F7_F13_F16_slot_rows gate5_F7_F13_F16_slot_rows_sha256
    combined_F1_F13_F16_slot_registry field_bridge_theorems count_ledger
    gate5_actual_child_field_status rank3_seed_child_field_maturity
    gate5_global_maturity complete_18_field_block_count gate5_block_count
    cm2_verdict strict_scope strict_nonclaims upstream_and_helper_pins""".split()
)
PHYSICAL_KEYS = set(
    """core_clearance_rows core_clearance_rows_sha256 child_stage_boundary_rows
    child_stage_boundary_rows_sha256 check_counts actual_interval_lower_minima
    claimed_strict_lower_margins along_seed_adapted_forward_Lipschitz_actual_upper
    physical_five_face_incidence_count residual_physical_face_count
    legacy_parameterized_moving_occurrence_grammar_seed_count
    rank3_candidate_occurrence_stage_counts
    rank3_candidate_occurrence_count_per_common_child
    rank3_candidate_occurrence_total_check_count
    complete_new_rank3_candidate_census_replaces_old_Q2_locator
    old_Q2_time2_atom_or_occurrence_ID_reused""".split()
)
CORE_ROW_KEYS = set(
    """common_child_id common_rank collision_section physical_face_grammar_kind
    obstacle chart typed_C24_core_face_check_count distance_strict_lower
    actual_interval_lower_minimum incidence_count row_sha256""".split()
)
CHILD_STAGE_KEYS = set(
    """common_child_id common_rank stage source_owner actual_next_owner source_chart
    s_collar candidate_check_count active_integer_corner_ray_check_count
    typed_boundary_check_counts typed_boundary_actual_interval_lower_minima
    typed_boundary_claimed_strict_lower physical_boundary_incidence_count
    BYPASS_designated_b3_used_as_collision_angle
    along_seed_adapted_forward_Lipschitz_actual_upper
    along_seed_diagnostic_only_not_F11_field_value row_sha256""".split()
)
FIVE_ROW_KEYS = {"kind", "clearance_evidence", "actual_instance_count", "row_sha256"}
MOVING_GRAMMAR_EXTRA_KEYS = {
    "legacy_parameterized_grammar_seed_count",
    "rank3_candidate_occurrence_count_per_common_child",
    "rank3_candidate_occurrence_total_check_count",
    "old_Q2_time2_atom_or_occurrence_ID_reused",
}
SEVEN_ROW_KEYS = {
    "kind", "audit_keys", "check_count", "strict_lower_margins",
    "actual_instance_count", "row_sha256",
}
MOVING_FACE_KEYS = set(
    """face_id face_kind exact_seed_id stage natural_index_j boundary_label
    exact_level_equation_id exact_level_equation delta s_collar
    round121_s0_endpoint_id s0_x_dyadic_bracket
    equation_decimal_participates_in_id base_image_chart base_image_obstacle
    base_curvature source_pullback_rank_path owner_below owner_above
    lower_trace_id upper_trace_id F_x_sign F_x_s0_abs_lower
    F_x_collar_abs_lower F_x_claimed_strict_lower F_s_abs_upper
    F_xx_abs_upper F_xs_abs_upper F_ss_abs_upper
    implicit_x_s_first_derivative_actual_abs_upper
    implicit_x_s_first_derivative_abs_upper
    implicit_x_s_second_derivative_actual_abs_upper
    implicit_x_s_second_derivative_abs_upper unique_analytic_graph
    graph_stays_in_s0_guard cut_order_preserved minimum_pair_separation_lower
    F8_normalized_wedge_strict_lower F8_formula F8_unstable_slope_interval
    F8_worst_case_squared_residual F9_source_pullback_unit_speed_C2_strict_upper
    F12_suffix_rank_path F12_C1_trace_pullback_strict_upper
    artificial_not_physical row_sha256""".split()
)
OUTER_FACE_KEYS = MOVING_FACE_KEYS | {"external_neighbor_materialized"}
TRACE_ROW_KEYS = set(
    """trace_id face_id side adjacent_common_child_id adjacent_common_rank
    external_neighbor_materialized owner_predicate
    F12_C1_trace_pullback_strict_upper artificial_not_physical row_sha256""".split()
)
INCIDENCE_ROW_KEYS = set(
    """common_child_id common_rank lower_face_id upper_face_id lower_trace_id
    upper_trace_id exactly_two_artificial_boundary_faces both_face_origins_retained
    row_sha256""".split()
)
DYNAMIC_ROW_KEYS = {
    "stage", "full_phase_dynamic_Holder_test_pullback_strict_upper",
    "alpha_scope", "along_seed_tight_diagnostic_upper",
    "along_seed_tight_diagnostic_used_as_field_value",
}
SLOT_ROW_KEYS = set(
    """slot_id immutable_slot_key official_word_key_id
    refined_homogeneous_subbranch_id common_child_id stage roof_level_j
    field_index field_name field_value_or_contract field_bound_semantics
    lower_artificial_face_id upper_artificial_face_id
    child_face_incidence_row_sha256 face_pair_F9_exact_max face_pair_F12_exact_max
    complete_artificial_face_registry_digest_replicated_across_roofs
    physical_face_empty_audit_sha256 F7_Xi_strict_upper
    F7_invariant_density_ratio_upper F7_actual_density_weighted_product
    F11_uses_full_phase_authoritative_envelope
    transparent_wall_roof_split_does_not_add_F7_F11_factor
    artificial_faces_not_erased_by_physical_empty_claim slot_status""".split()
)


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
    require(type(value) is dict, "top-level JSON object")
    reject_surrogates(value)
    return value


def require_integer(value: Any, label: str) -> int:
    require(type(value) is int, f"{label}:integer")
    return value


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str, f"{label}:fraction type")
    require(
        re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value) is not None,
        f"{label}:canonical fraction syntax",
    )
    result = Q(value)
    require(str(result) == value, f"{label}:reduced fraction")
    return result


def row_digest(row: dict[str, Any]) -> str:
    return digest({key: value for key, value in row.items() if key != "row_sha256"})


def arb_pair(value: arb) -> tuple[Q, Q]:
    def dyadic(point: arb) -> Q:
        mantissa, exponent = point.man_exp()
        return Q(int(mantissa)) * Q(2) ** int(exponent)

    return dyadic(value.lower()), dyadic(value.upper())


def padded_pair(value: arb, padding: Q = Q(1, 10**220)) -> list[str]:
    lower, upper = arb_pair(value)
    return [str(lower - padding), str(upper + padding)]


def upper_abs(value: arb) -> Q:
    lower, upper = arb_pair(value)
    return max(abs(lower), abs(upper))


class Jet2:
    """Two-variable second-order interval jet in variables x and s."""

    __slots__ = ("value", "x", "s", "xx", "xs", "ss")

    def __init__(
        self,
        value: arb | int,
        x: arb | int = 0,
        s: arb | int = 0,
        xx: arb | int = 0,
        xs: arb | int = 0,
        ss: arb | int = 0,
    ):
        self.value = value if isinstance(value, arb) else arb(value)
        self.x = x if isinstance(x, arb) else arb(x)
        self.s = s if isinstance(s, arb) else arb(s)
        self.xx = xx if isinstance(xx, arb) else arb(xx)
        self.xs = xs if isinstance(xs, arb) else arb(xs)
        self.ss = ss if isinstance(ss, arb) else arb(ss)

    @staticmethod
    def coerce(value: Any) -> "Jet2":
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other: Any) -> "Jet2":
        other = self.coerce(other)
        return Jet2(
            self.value + other.value,
            self.x + other.x,
            self.s + other.s,
            self.xx + other.xx,
            self.xs + other.xs,
            self.ss + other.ss,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet2":
        return Jet2(
            -self.value, -self.x, -self.s, -self.xx, -self.xs, -self.ss
        )

    def __sub__(self, other: Any) -> "Jet2":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "Jet2":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "Jet2":
        other = self.coerce(other)
        return Jet2(
            self.value * other.value,
            self.x * other.value + self.value * other.x,
            self.s * other.value + self.value * other.s,
            (
                self.xx * other.value
                + 2 * self.x * other.x
                + self.value * other.xx
            ),
            (
                self.xs * other.value
                + self.x * other.s
                + self.s * other.x
                + self.value * other.xs
            ),
            (
                self.ss * other.value
                + 2 * self.s * other.s
                + self.value * other.ss
            ),
        )

    __rmul__ = __mul__

    def compose(self, value: arb, first: arb, second: arb) -> "Jet2":
        return Jet2(
            value,
            first * self.x,
            first * self.s,
            second * self.x * self.x + first * self.xx,
            second * self.x * self.s + first * self.xs,
            second * self.s * self.s + first * self.ss,
        )

    def reciprocal(self) -> "Jet2":
        first = -arb(1) / (self.value * self.value)
        second = 2 / (self.value * self.value * self.value)
        return self.compose(arb(1) / self.value, first, second)

    def __truediv__(self, other: Any) -> "Jet2":
        return self * self.coerce(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "Jet2":
        return self.coerce(other) / self

    def sqrt(self) -> "Jet2":
        root = self.value.sqrt()
        return self.compose(
            root,
            arb(1) / (2 * root),
            -arb(1) / (4 * root * root * root),
        )

    def sin(self) -> "Jet2":
        return self.compose(self.value.sin(), self.value.cos(), -self.value.sin())

    def cos(self) -> "Jet2":
        return self.compose(self.value.cos(), -self.value.sin(), -self.value.cos())

    def asin(self) -> "Jet2":
        one_minus = arb(1) - self.value * self.value
        root = one_minus.sqrt()
        return self.compose(
            self.value.asin(),
            arb(1) / root,
            self.value / (one_minus * root),
        )


def shifted_center(target: str, s: Jet2) -> tuple[Jet2, Jet2]:
    obstacle = target[0]
    ix, iy = map(int, target[2:-1].split(","))
    offset = Q(1, 2) if obstacle == "W" else Q(0)
    x = Jet2(aq(Q(ix) + offset))
    y = Jet2(aq(Q(iy) + offset))
    if obstacle == "W":
        x = x + s
    return x, y


def target_radius(target: str) -> arb:
    return aq(Q(9, 25) if target[0] == "G" else Q(4, 25))


def collision(
    qx: Jet2,
    qy: Jet2,
    ux: Jet2,
    uy: Jet2,
    target: str,
    s: Jet2,
) -> tuple[Jet2, Jet2, Jet2, Jet2, Jet2, Jet2, Jet2, Jet2, Jet2]:
    cx, cy = shifted_center(target, s)
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
    cosine = (Jet2(arb(1)) - momentum * momentum).sqrt()
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


def source_and_collisions(
    theta_star: arb, x: Jet2, s: Jet2
) -> dict[str, Any]:
    delta = aq(DELTA)
    theta0 = Jet2(theta_star) + aq(Q(25, 61)) * delta * x
    phi0 = Jet2(aq(SEED_C0).acos()) + aq(Q(36, 61)) * delta * x
    c0 = phi0.cos()
    t = theta0.sin()
    normal_x, normal_y = theta0.cos(), t
    p0 = (Jet2(arb(1)) - c0 * c0).sqrt()
    source_radius = aq(Q(9, 25))
    qx, qy = source_radius * normal_x, source_radius * normal_y
    ux = c0 * normal_x - p0 * normal_y
    uy = c0 * normal_y + p0 * normal_x
    first = collision(qx, qy, ux, uy, "W[-1,-1]", s)
    second = collision(*first[:4], "G[0,0]", s)
    actual_third = collision(*second[:4], SEED_ACTUAL_THIRD, s)

    # The designated W[-1,-2] is a miss.  Its negative discriminant defines
    # b3 and is never used as the actual third collision momentum.
    cx3, cy3 = shifted_center("W[-1,-2]", s)
    dx3, dy3 = cx3 - second[0], cy3 - second[1]
    transverse3 = -second[3] * dx3 + second[2] * dy3
    r3 = target_radius("W[-1,-2]")
    designated_discriminant = r3 * r3 - transverse3 * transverse3
    b3 = (-designated_discriminant).sqrt() / r3

    # Frozen first/second image charts are N and S.
    a1 = Jet2(arb.pi() / 2) - first[4].asin() + first[6].asin()
    a2 = Jet2(-arb.pi() / 2) + second[4].asin() + second[6].asin()
    cp1 = (Jet2(arb(1)) - first[6] * first[6]).sqrt()
    cp2 = (Jet2(arb(1)) - second[6] * second[6]).sqrt()
    cp3 = (Jet2(arb(1)) - actual_third[6] * actual_third[6]).sqrt()
    return {
        "source": (qx, qy, ux, uy),
        "collisions": (
            (normal_x, normal_y, p0, c0),
            (first[4], first[5], first[6], cp1),
            (second[4], second[5], second[6], cp2),
            (actual_third[4], actual_third[5], actual_third[6], cp3),
        ),
        "c0": c0,
        "t": t,
        "b3": b3,
        "first": first,
        "second": second,
        "actual_third": actual_third,
        "designated_discriminant": designated_discriminant,
        "a1": a1,
        "a2": a2,
    }


def candidate_geometry(
    state: tuple[Jet2, Jet2, Jet2, Jet2],
    candidate_id: str,
    s: Jet2,
) -> dict[str, Any]:
    qx, qy, ux, uy = state
    cx, cy = shifted_center(candidate_id, s)
    dx, dy = cx - qx, cy - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = target_radius(candidate_id)
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant.value < 0):
        return {
            "candidate_id": candidate_id,
            "classification": "STRICT_WHOLE_LINE_MISS",
            "discriminant": discriminant,
        }
    require(bool(discriminant.value > 0), f"candidate discriminant:{candidate_id}")
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far.value < 0):
        return {
            "candidate_id": candidate_id,
            "classification": "STRICT_INTERSECTION_BEHIND",
            "discriminant": discriminant,
            "far": far,
        }
    require(bool(near.value > 0), f"candidate root sign:{candidate_id}")
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    return {
        "candidate_id": candidate_id,
        "classification": "STRICT_FUTURE_NEAR_ROOT",
        "discriminant": discriminant,
        "near": near,
        "normal_x": normal_x,
        "normal_y": normal_y,
    }


def strict_chart(normal_x: Jet2, normal_y: Jet2) -> str:
    nx, ny = normal_x.value, normal_y.value
    ax, ay = abs(nx), abs(ny)
    if bool(ax > ay):
        if bool(nx > 0):
            return "E"
        if bool(nx < 0):
            return "W"
    if bool(ay > ax):
        if bool(ny > 0):
            return "N"
        if bool(ny < 0):
            return "S"
    raise RuntimeError("collision chart seam")


def replay_leg(
    state: tuple[Jet2, Jet2, Jet2, Jet2],
    current_target: str,
    chart: str,
    expected_owner: str,
    expected_chart: str,
    s: Jet2,
) -> dict[str, Any]:
    candidate_ids = tuple(time2.translated_candidate_ids(current_target, chart))
    require(
        len(candidate_ids) == len(set(candidate_ids))
        and expected_owner in candidate_ids,
        "candidate universe",
    )
    rows = [candidate_geometry(state, candidate_id, s) for candidate_id in candidate_ids]
    future = [
        row for row in rows if row["classification"] == "STRICT_FUTURE_NEAR_ROOT"
    ]
    require(future, "future candidate census")
    winners = [
        row
        for row in future
        if all(
            row is other or bool(row["near"].value < other["near"].value)
            for other in future
        )
    ]
    require(len(winners) == 1, "unique candidate winner")
    winner = winners[0]
    require(winner["candidate_id"] == expected_owner, "actual candidate owner")
    require(strict_chart(winner["normal_x"], winner["normal_y"]) == expected_chart,
            "actual candidate chart")
    gaps = [
        other["near"] - winner["near"]
        for other in future
        if other is not winner
    ]
    require(all(bool(gap.value > 0) for gap in gaps), "strict owner gaps")
    histogram = Counter(row["classification"] for row in rows)
    tangent_margins = [
        min(abs(arb_pair(row["discriminant"].value)[0]),
            abs(arb_pair(row["discriminant"].value)[1]))
        for row in rows
    ]
    root_rows = [
        row for row in rows
        if row["classification"] in {
            "STRICT_INTERSECTION_BEHIND", "STRICT_FUTURE_NEAR_ROOT"
        }
    ]
    root_margins = [
        (
            -arb_pair(row["far"].value)[1]
            if row["classification"] == "STRICT_INTERSECTION_BEHIND"
            else arb_pair(row["near"].value)[0]
        )
        for row in root_rows
    ]
    return {
        "current_target": current_target,
        "source_chart": chart,
        "candidate_count": len(rows),
        "candidate_ids_sha256": digest(list(candidate_ids)),
        "classification_histogram": dict(sorted(histogram.items())),
        "future_candidate_count": len(future),
        "root_sign_check_count": len(root_rows),
        "candidate_tangency_strict_lower": str(min(tangent_margins)),
        "root_sign_strict_lower": str(min(root_margins)),
        "owner_gap_check_count": len(gaps),
        "selected_owner_id": winner["candidate_id"],
        "selected_collision_chart": expected_chart,
        "minimum_owner_gap_enclosure": (
            padded_pair(min(gaps, key=lambda item: item.value.lower()).value)
            if gaps
            else None
        ),
    }


def load_inputs() -> dict[str, Any]:
    for name, expected in UPSTREAM_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
        require(sha256(path) == expected, f"byte pin:{name}")
    schemas = {
        "r113": round113.SCHEMA,
        "r117": "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
        "r120": "cm2.round120.rank3-relative-interior-actual-standard-curve-recut.v1",
        "r121": "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    }
    values: dict[str, Any] = {}
    for key, path in (
        ("r113", ROUND113),
        ("r117", ROUND117),
        ("r120", ROUND120),
        ("r121", ROUND121),
    ):
        document = strict_json(path.read_text(encoding="utf-8"))
        require(
            set(document) == {"schema", "result", "result_sha256"},
            f"{key}:envelope",
        )
        require(document["schema"] == schemas[key], f"{key}:schema")
        require(document["result_sha256"] == digest(document["result"]), f"{key}:digest")
        values[key] = document["result"]
    return values


def seed_indexes(values: dict[str, Any]) -> dict[str, Any]:
    sheet = None
    parent = None
    for candidate_sheet in values["r113"]["sheet_rows"]:
        for cell in candidate_sheet["certified_cells"]:
            if cell["cell_id"] == SEED_PARENT_ID:
                sheet, parent = candidate_sheet, cell
    require(sheet is not None and parent is not None, "R113 seed parent")
    row117 = next(
        row
        for row in values["r117"]["common_refinement_rows"]
        if row["parent_round113_cell_id"] == SEED_PARENT_ID
    )
    row120 = next(
        row
        for row in values["r120"]["child_generator_rows"]
        if row["parent_round113_cell_id"] == SEED_PARENT_ID
    )
    require(tuple(sheet["branch_key"]) == SEED_BRANCH, "seed branch")
    require(sheet["sheet_kind"] == "BYPASS", "seed sheet")
    require(sheet["source_chart"] == SEED_SOURCE_CHART, "seed source chart")
    require(
        row117["actual_third_collision_owner_id"] == SEED_ACTUAL_THIRD,
        "seed actual third",
    )
    require(row117["bypass_b3_is_collision_angle"] is False, "b3 role")
    require(row120["official_word_key_ids"] == list(OFFICIAL_WORD_IDS), "word IDs")
    r121 = values["r121"]
    require(len(r121["pullback_endpoint_rows"]) == 23, "R121 endpoint census")
    require(len(r121["common_refinement_rows"]) == 24, "R121 child census")
    require(
        len(r121["refined_homogeneous_subbranch_rows"]) == 24,
        "R121 refined census",
    )
    return {"sheet": sheet, "parent": parent, "r117": row117, "r120": row120}


def isolate_anchor(indexes: dict[str, Any]) -> arb:
    lower, upper = map(Q, indexes["parent"]["implicit_t_root_enclosure"])
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
    require(lower_sign * upper_sign == -1, "anchor signs")
    for _ in range(ROOT_BISECTIONS):
        middle = (lower + upper) / 2
        sign = strict_sign(equation(middle))
        require(sign != 0, "anchor bisection")
        if sign == lower_sign:
            lower = middle
        else:
            require(sign == upper_sign, "anchor sign orientation")
            upper = middle
    t_ball = interval(lower, upper)
    require(bool(t_ball > 0) and bool(t_ball < 1), "anchor chart")
    return arb.pi() - t_ball.asin()


def face_value(theta_star: arb, stage: int, natural_index: int, x: Q) -> arb:
    xjet, sjet = Jet2(aq(x)), Jet2(arb(0))
    zero = source_and_collisions(theta_star, Jet2(arb(0)), sjet)
    state = source_and_collisions(theta_star, xjet, sjet)
    coordinate = zero["a1"] - state["a1"] if stage == 1 else state["a2"] - zero["a2"]
    return coordinate.value - aq(DELTA * natural_index)


def isolate_face(
    theta_star: arb, stage: int, natural_index: int
) -> tuple[Q, Q]:
    lower, upper = Q(0), Q(1)
    lower_sign = strict_sign(face_value(theta_star, stage, natural_index, lower))
    upper_sign = strict_sign(face_value(theta_star, stage, natural_index, upper))
    require(lower_sign == -1 and upper_sign == 1, "face endpoint signs")
    for _ in range(FACE_BISECTIONS):
        middle = (lower + upper) / 2
        sign = strict_sign(face_value(theta_star, stage, natural_index, middle))
        require(sign != 0, "face bisection")
        if sign == lower_sign:
            lower = middle
        else:
            require(sign == upper_sign, "face bisection orientation")
            upper = middle
    return lower, upper


def face_jet(
    theta_star: arb,
    stage: int,
    natural_index: int,
    x_lower: Q,
    x_upper: Q,
) -> Jet2:
    x = Jet2(interval(x_lower, x_upper), x=arb(1))
    s = Jet2(interval(-PARAMETER_RADIUS, PARAMETER_RADIUS), s=arb(1))
    zero = source_and_collisions(theta_star, Jet2(arb(0)), s)
    state = source_and_collisions(theta_star, x, s)
    coordinate = zero["a1"] - state["a1"] if stage == 1 else state["a2"] - zero["a2"]
    return coordinate - aq(DELTA * natural_index)


def replay_faces(theta_star: arb) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stage, count, normalized_fx_lower, first_claim, second_claim in (
        (1, 6, Q(5), Q(4), Q(56)),
        (2, 17, Q(16), Q(13), Q(616)),
    ):
        for natural_index in range(1, count + 1):
            root_lower, root_upper = isolate_face(theta_star, stage, natural_index)
            tube_lower = root_lower - FACE_TUBE_PADDING
            tube_upper = root_upper + FACE_TUBE_PADDING
            require(0 < tube_lower < tube_upper < 1, "face tube domain")
            left = face_jet(
                theta_star, stage, natural_index, tube_lower, tube_lower
            )
            right = face_jet(
                theta_star, stage, natural_index, tube_upper, tube_upper
            )
            require(bool(left.value < 0) and bool(right.value > 0), "collar face signs")
            jet = face_jet(
                theta_star, stage, natural_index, tube_lower, tube_upper
            )
            require(bool(jet.x / aq(DELTA) > aq(normalized_fx_lower)), "face Fx")
            root_s = -jet.s / jet.x
            root_ss = -(
                jet.ss + 2 * jet.xs * root_s + jet.xx * root_s * root_s
            ) / jet.x
            first_upper = upper_abs(root_s)
            second_upper = upper_abs(root_ss)
            require(first_upper < first_claim, "implicit first derivative")
            require(second_upper < second_claim, "implicit second derivative")
            rows.append(
                {
                    "cut_label": f"S{stage}:{natural_index}",
                    "stage": stage,
                    "natural_index_j": natural_index,
                    "root_dyadic_bracket": [str(root_lower), str(root_upper)],
                    "collar_root_tube": [str(tube_lower), str(tube_upper)],
                    "collar_face_signs": [-1, 1],
                    "Fx_over_delta_enclosure": padded_pair(jet.x / aq(DELTA)),
                    "Fs_enclosure": padded_pair(jet.s),
                    "Fxx_over_delta_enclosure": padded_pair(jet.xx / aq(DELTA)),
                    "Fxs_enclosure": padded_pair(jet.xs),
                    "Fss_enclosure": padded_pair(jet.ss),
                    "implicit_x_s_enclosure": padded_pair(root_s),
                    "implicit_x_ss_enclosure": padded_pair(root_ss),
                    "implicit_first_parameter_upper": str(first_upper),
                    "implicit_second_parameter_upper": str(second_upper),
                    "implicit_first_claim": str(first_claim),
                    "implicit_second_claim": str(second_claim),
                }
            )
    rows.sort(key=lambda row: Q(row["root_dyadic_bracket"][0]))
    require(tuple(row["cut_label"] for row in rows) == EXPECTED_CUT_ORDER,
            "face order")
    for left, right in zip(rows, rows[1:]):
        require(
            Q(right["collar_root_tube"][0]) - Q(left["collar_root_tube"][1])
            > Q(1, 201),
            "face tube separation",
        )
    return rows


def replay_candidates(theta_star: arb, indexes: dict[str, Any]) -> list[dict[str, Any]]:
    x = Jet2(interval(Q(0), Q(1)), x=arb(1))
    s = Jet2(interval(-PARAMETER_RADIUS, PARAMETER_RADIUS), s=arb(1))
    geometry = source_and_collisions(theta_star, x, s)
    first_chart = indexes["parent"]["leg_audits"][0]["selected_collision_chart"]
    second_chart = indexes["parent"]["leg_audits"][1]["selected_collision_chart"]
    rows = [
        replay_leg(
            geometry["source"],
            "G[0,0]",
            SEED_SOURCE_CHART.split(":")[1],
            "W[-1,-1]",
            first_chart,
            s,
        ),
        replay_leg(
            geometry["first"][:4],
            "W[-1,-1]",
            first_chart,
            "G[0,0]",
            second_chart,
            s,
        ),
        replay_leg(
            geometry["second"][:4],
            "G[0,0]",
            second_chart,
            SEED_ACTUAL_THIRD,
            strict_chart(geometry["actual_third"][4], geometry["actual_third"][5]),
            s,
        ),
    ]
    require([row["candidate_count"] for row in rows] == [57, 55, 57],
            "169 candidate census")
    require(sum(row["candidate_count"] for row in rows) == 169, "candidate total")
    require(bool(geometry["designated_discriminant"].value < 0), "designated miss")
    require(
        geometry["actual_third"][6].value < 0
        and bool((arb(1) - geometry["actual_third"][6].value**2).sqrt() > aq(Q(4, 5))),
        "actual third central winner",
    )
    return rows


def abs_lower(value: arb) -> Q:
    lower, upper = arb_pair(value)
    if lower > 0:
        return lower
    if upper < 0:
        return -upper
    return Q(0)


def distance_to_interval(value: arb, lower: Q, upper: Q) -> Q:
    value_lower, value_upper = arb_pair(value)
    if value_upper < lower:
        return lower - value_upper
    if value_lower > upper:
        return value_lower - upper
    return Q(0)


def nearest_integer_margin(value: arb) -> Q:
    return min(abs_lower(value - arb(integer)) for integer in range(-7, 8))


def chart_coordinate(chart: str, nx: Jet2, ny: Jet2) -> Jet2:
    return ny if chart in {"E", "W"} else nx


def chart_margin(nx: Jet2, ny: Jet2) -> Q:
    return abs_lower(abs(nx.value) - abs(ny.value))


def core_face_distance(t: arb, p: arb, core: Any, face: str) -> Q:
    if face == "t0":
        return max(abs_lower(t - aq(core.t0)), distance_to_interval(p, core.p0, core.p1))
    if face == "t1":
        return max(abs_lower(t - aq(core.t1)), distance_to_interval(p, core.p0, core.p1))
    if face == "p0":
        return max(abs_lower(p - aq(core.p0)), distance_to_interval(t, core.t0, core.t1))
    if face == "p1":
        return max(abs_lower(p - aq(core.p1)), distance_to_interval(t, core.t0, core.t1))
    raise RuntimeError(f"unknown core face:{face}")


def replay_physical_boundaries(
    theta_star: arb,
    candidate_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Independent complete five-face/seven-kind empty audit on the collar.

    Evaluating the whole x interval at once is stronger than repeating the
    same checks on the 24 Round121 child subintervals.  The returned counts
    are multiplied by 24 only after every whole-seed strict margin has passed.
    """

    x = Jet2(interval(Q(0), Q(1)), x=arb(1))
    s = Jet2(interval(-PARAMETER_RADIUS, PARAMETER_RADIUS), s=arb(1))
    geometry = source_and_collisions(theta_star, x, s)
    counts = {key: 0 for key in SAFE_PHYSICAL_MARGINS}
    minima: dict[str, Q | None] = {key: None for key in SAFE_PHYSICAL_MARGINS}

    def observe(key: str, value: Q, multiplicity: int = 1) -> None:
        require(value > SAFE_PHYSICAL_MARGINS[key], f"physical margin:{key}")
        counts[key] += multiplicity
        if minima[key] is None or value < minima[key]:
            minima[key] = value

    for row in candidate_rows:
        observe(
            "candidate_tangency",
            Q(row["candidate_tangency_strict_lower"]),
            row["candidate_count"],
        )
        observe("root_sign", Q(row["root_sign_strict_lower"]), row["root_sign_check_count"])
        if row["owner_gap_check_count"]:
            require(row["minimum_owner_gap_enclosure"] is not None, "owner gap enclosure")
            observe(
                "owner_gap",
                Q(row["minimum_owner_gap_enclosure"][0]),
                row["owner_gap_check_count"],
            )

    charts = ("W", "N", "S", "N")
    obstacles = ("G", "W", "G", "G")
    h128 = aq(Q(1, 128**2)).sin()
    cores = core_cert.physical_cores()
    for section, ((nx, ny, p, cp), chart, obstacle) in enumerate(
        zip(geometry["collisions"], charts, obstacles)
    ):
        t = chart_coordinate(chart, nx, ny).value
        matching = [core for core in cores if core.chart_id == f"{obstacle}:{chart}"]
        require(len(matching) == 3, "three C24 cores per section")
        section_count = 0
        for core in matching:
            for face in ("t0", "t1", "p0", "p1"):
                observe("core_face", core_face_distance(t, p.value, core, face))
                section_count += 1
        require(section_count == 12, "twelve core faces per section")

    selected = (geometry["first"], geometry["second"], geometry["actual_third"])
    current_targets = ("G[0,0]", "W[-1,-1]", "G[0,0]")
    for stage in range(3):
        qx, qy, ux, uy = (
            geometry["source"]
            if stage == 0
            else geometry["first"][:4]
            if stage == 1
            else geometry["second"][:4]
        )
        nx, ny, _p, cp = geometry["collisions"][stage]
        next_nx, next_ny, _next_p, next_cp = geometry["collisions"][stage + 1]
        observe(
            "source_endpoint_wall",
            min(nearest_integer_margin(qx.value), nearest_integer_margin(qy.value)),
        )
        observe("source_chart_seam", chart_margin(nx, ny))
        observe("source_homogeneity", arb_pair(cp.value - h128)[0])
        observe("coordinate_velocity_zero", abs_lower(ux.value))
        observe("coordinate_velocity_zero", abs_lower(uy.value))
        observe(
            "target_endpoint_wall",
            min(
                nearest_integer_margin(selected[stage][0].value),
                nearest_integer_margin(selected[stage][1].value),
            ),
        )
        observe("target_chart_seam", chart_margin(next_nx, next_ny))
        observe("target_homogeneity", arb_pair(next_cp.value - h128)[0])

        _obstacle, ix, iy = time2.parse_target(current_targets[stage])
        active = 0
        for corner_x in range(ix - 5, ix + 6):
            for corner_y in range(iy - 5, iy + 6):
                dx, dy = arb(corner_x) - qx.value, arb(corner_y) - qy.value
                longitudinal = ux.value * dx + uy.value * dy
                lower, upper = arb_pair(longitudinal)
                if upper <= Q(1, 2) or lower >= Q(3):
                    continue
                transverse = -uy.value * dx + ux.value * dy
                observe("integer_corner_ray", abs_lower(transverse))
                active += 1
        require(active > 0, "active corner census")

    base_counts = dict(counts)
    counts = {key: value * 24 for key, value in counts.items()}
    require(counts == EXPECTED_PHYSICAL_COUNTS, "physical boundary census")
    require(all(value is not None for value in minima.values()), "all physical minima")
    return {
        "whole_seed_check_counts": base_counts,
        "certificate_repeated_child_check_counts": counts,
        "independent_strict_lower_minima": {
            key: str(value) for key, value in sorted(minima.items()) if value is not None
        },
        "physical_five_face_incidence_count": 0,
        "residual_physical_face_count": 0,
    }


def core_replay() -> dict[str, Any]:
    require(F7_DENSITY_RATIO * F7_XI == F7_ACTUAL < 1, "F7 actual identity")
    values = load_inputs()
    indexes = seed_indexes(values)
    theta_star = isolate_anchor(indexes)
    candidate_rows = replay_candidates(theta_star, indexes)
    physical = replay_physical_boundaries(theta_star, candidate_rows)
    face_rows = replay_faces(theta_star)
    child_rows: list[dict[str, Any]] = []
    boundaries: list[tuple[str, Q, Q]] = [
        ("SOURCE_LEFT", Q(0), Q(0)),
        *[
            (
                row["cut_label"],
                Q(row["collar_root_tube"][0]),
                Q(row["collar_root_tube"][1]),
            )
            for row in face_rows
        ],
        ("SOURCE_RIGHT", Q(1), Q(1)),
    ]
    for rank, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
        require(right[1] - left[2] > 0, "positive child collar interval")
        child_rows.append(
            {
                "common_rank": rank,
                "left_face": left[0],
                "right_face": right[0],
                "uniform_source_x_gap_strict_lower": str(right[1] - left[2]),
            }
        )
    require(len(child_rows) == 24, "24 child collar census")
    require(sum(ROOF_COUNTS) * len(child_rows) == 120, "slots per field")
    return {
        "verification_precision_bits": VERIFIER_PRECISION_BITS,
        "parameter_collar": "|s|<=2^-512",
        "parameter_radius": str(PARAMETER_RADIUS),
        "fixed_gauge": "horizontal center translation of every W; G fixed",
        "candidate_leg_rows": candidate_rows,
        "candidate_total": sum(row["candidate_count"] for row in candidate_rows),
        "physical_boundary_replay": physical,
        "moving_face_rows": face_rows,
        "moving_face_count": len(face_rows),
        "stationary_outer_face_count": 2,
        "child_collar_rows": child_rows,
        "common_refinement_child_count": len(child_rows),
        "roof_levels_per_child": sum(ROOF_COUNTS),
        "slots_per_field": len(child_rows) * sum(ROOF_COUNTS),
        "field_constants": {
            "F7_density_ratio": str(F7_DENSITY_RATIO),
            "F7_Xi": str(F7_XI),
            "F7_actual_density_times_Xi": str(F7_ACTUAL),
            "F8_wedge_strict_lower": str(F8_WEDGE_LOWER),
            "F9_stage_strict_uppers": {
                str(key): str(value) for key, value in F9_STAGE_BOUNDS.items()
            },
            "F11_full_phase_strict_uppers": {
                str(key): str(value) for key, value in F11_STAGE_BOUNDS.items()
            },
            "F12_stage_strict_uppers": {
                str(key): str(value) for key, value in F12_STAGE_BOUNDS.items()
            },
            "F10_empty_physical_occurrence_value": "0",
            "F13_empty_physical_occurrence_value": "0",
            "F16_empty_physical_occurrence_value": "0",
        },
        "strict_status": {
            "child_local_F1_F13_and_F16": "CORE_GEOMETRY_REPLAYED",
            "F14": "NOT_INSTALLED",
            "F15": "NOT_INSTALLED",
            "F17": "NOT_INSTALLED",
            "F18": "NOT_INSTALLED",
            "rank3_seed_child_maturity_target": "14/18",
            "global_Gate5": "10/18",
            "complete_18_field_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        },
        "upstream_pin_count": len(UPSTREAM_PINS),
    }


def trace_id(face_id: str, side: str) -> str:
    require(side in {"lower", "upper"}, "trace side")
    return "round122-recut-face-trace:" + digest(
        ["round122-recut-face-trace-v1", face_id, side]
    )


def validate_pin_ledger(ledger: Any) -> None:
    require(type(ledger) is dict and len(ledger) >= 40, "pin ledger")
    for name, expected in ledger.items():
        require(type(name) is str and type(expected) is str, "pin entry types")
        require(re.fullmatch(r"[0-9a-f]{64}", expected) is not None, f"pin hash:{name}")
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
        require(sha256(path) == expected, f"certificate pin:{name}")


def static_contract(
    document: dict[str, Any], values: dict[str, Any], *, check_pins: bool = True
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS, "closed result")
    require(document["result_sha256"] == digest(result), "certificate digest")
    require_integer(result["precision_bits"], "producer precision")
    require(result["precision_bits"] >= 2048, "producer precision lower")

    r121 = values["r121"]
    seed_id = r121["exact_seed_contract"]["exact_parent_W_seed_id"]
    require(
        result["round121_contract"]
        == {
            "schema": "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
            "result_sha256": digest(r121),
            "exact_parent_W_seed_id": seed_id,
            "common_refinement_actual_child_count": 24,
            "pullback_internal_cut_count": 23,
            "inherited_F1_F6_slot_count": 720,
            "inherited_F1_F6_slot_rows_sha256": r121[
                "gate5_F1_F6_slot_rows_sha256"
            ],
            "frozen_Round121_files_modified": False,
        },
        "Round121 contract",
    )
    collar = result["parameter_collar_contract"]
    require(
        collar
        == {
            "parameter": "horizontal displacement of every W obstacle center",
            "closed_collar": f"|s|<={PARAMETER_RADIUS}",
            "epsilon": str(PARAMETER_RADIUS),
            "epsilon_is_exact_dyadic": True,
            "common_to_all_24_children_and_three_legs": True,
            "source_G_obstacle_is_stationary": True,
            "W_obstacles_move_by_(s,0)": True,
            "moving_cut_shift_strict_upper": f"13*{PARAMETER_RADIUS}",
            "moving_cut_shift_below_Round121_2^-200_guard": True,
            "moving_cut_pair_shift_below_1/1000": True,
            "Round121_minimum_distinct_cut_separation_strict_lower": "1/200",
        },
        "parameter collar contract",
    )

    physical = result["physical_face_typed_empty_audit"]
    require(type(physical) is dict and set(physical) == PHYSICAL_KEYS, "physical schema")
    require(
        physical["rank3_candidate_occurrence_stage_counts"] == [57, 55, 57]
        and physical["rank3_candidate_occurrence_count_per_common_child"] == 169
        and physical["rank3_candidate_occurrence_total_check_count"] == 4056
        and physical["legacy_parameterized_moving_occurrence_grammar_seed_count"] == 64
        and physical["complete_new_rank3_candidate_census_replaces_old_Q2_locator"]
        is True
        and physical["old_Q2_time2_atom_or_occurrence_ID_reused"] is False,
        "rank3 candidate census",
    )
    require(physical["check_counts"] == EXPECTED_PHYSICAL_COUNTS, "physical counts")
    require(
        physical["claimed_strict_lower_margins"]
        == {key: str(value) for key, value in sorted(SAFE_PHYSICAL_MARGINS.items())},
        "physical claimed margins",
    )
    require(
        set(physical["actual_interval_lower_minima"]) == set(SAFE_PHYSICAL_MARGINS),
        "physical minima keys",
    )
    for key, stored in physical["actual_interval_lower_minima"].items():
        require(qvalue(stored, f"physical minimum:{key}") > SAFE_PHYSICAL_MARGINS[key],
                f"physical minimum strict:{key}")
    require(
        type(physical["along_seed_adapted_forward_Lipschitz_actual_upper"]) is list
        and len(physical["along_seed_adapted_forward_Lipschitz_actual_upper"]) == 3,
        "along-seed diagnostic",
    )
    for value, bound in zip(
        physical["along_seed_adapted_forward_Lipschitz_actual_upper"], (Q(7), Q(3), Q(12))
    ):
        require(qvalue(value, "along-seed bound") < bound, "along-seed strict")
    require(
        physical["physical_five_face_incidence_count"] == 0
        and physical["residual_physical_face_count"] == 0,
        "physical empty conclusion",
    )

    core_rows = physical["core_clearance_rows"]
    require(type(core_rows) is list and len(core_rows) == 96, "core row count")
    require(physical["core_clearance_rows_sha256"] == digest(core_rows), "core digest")
    child_ids = {
        row["common_rank"]: row["common_child_id"]
        for row in r121["common_refinement_rows"]
    }
    core_keys: set[tuple[int, int]] = set()
    expected_roles = {
        0: "source_core_clipping_face",
        1: "intermediate_core_avoidance_preimage_face",
        2: "intermediate_core_avoidance_preimage_face",
        3: "terminal_core_preimage_face",
    }
    expected_section = {
        0: ("G", "W"),
        1: ("W", "N"),
        2: ("G", "S"),
        3: ("G", "N"),
    }
    for row in core_rows:
        require(type(row) is dict and set(row) == CORE_ROW_KEYS, "core row schema")
        rank = require_integer(row["common_rank"], "core rank")
        section = require_integer(row["collision_section"], "core section")
        require(
            0 <= rank < 24
            and section in expected_roles
            and row["common_child_id"] == child_ids[rank],
            "core row crosswalk",
        )
        require(
            row["physical_face_grammar_kind"] == expected_roles[section]
            and (row["obstacle"], row["chart"]) == expected_section[section]
            and row["typed_C24_core_face_check_count"] == 12
            and row["distance_strict_lower"] == "1/3"
            and qvalue(row["actual_interval_lower_minimum"], "core actual") > Q(1, 3)
            and row["incidence_count"] == 0,
            "core row contract",
        )
        require(row["row_sha256"] == row_digest(row), "core row digest")
        core_keys.add((rank, section))
    require(len(core_keys) == 96, "core unique rows")

    stage_rows = physical["child_stage_boundary_rows"]
    require(type(stage_rows) is list and len(stage_rows) == 72, "stage row count")
    require(
        physical["child_stage_boundary_rows_sha256"] == digest(stage_rows),
        "stage rows digest",
    )
    expected_current = ("G[0,0]", "W[-1,-1]", "G[0,0]")
    expected_selected = ("W[-1,-1]", "G[0,0]", "G[-1,-2]")
    expected_chart = ("W", "N", "S")
    stage_keys: set[tuple[int, int]] = set()
    for row in stage_rows:
        require(type(row) is dict and set(row) == CHILD_STAGE_KEYS, "stage row schema")
        rank = require_integer(row["common_rank"], "stage rank")
        stage = require_integer(row["stage"], "stage index")
        require(
            0 <= rank < 24
            and 0 <= stage < 3
            and row["common_child_id"] == child_ids[rank],
            "stage row crosswalk",
        )
        require(
            row["source_owner"] == expected_current[stage]
            and row["actual_next_owner"] == expected_selected[stage]
            and row["source_chart"] == expected_chart[stage]
            and row["s_collar"] == f"|s|<={PARAMETER_RADIUS}"
            and row["candidate_check_count"] == (57, 55, 57)[stage]
            and row["physical_boundary_incidence_count"] == 0
            and row["BYPASS_designated_b3_used_as_collision_angle"] is False
            and row["along_seed_diagnostic_only_not_F11_field_value"] is True,
            "stage row semantics",
        )
        require(
            set(row["typed_boundary_claimed_strict_lower"])
            == set(row["typed_boundary_actual_interval_lower_minima"])
            == set(row["typed_boundary_check_counts"]),
            "stage typed keys",
        )
        for key, claimed in row["typed_boundary_claimed_strict_lower"].items():
            require(
                qvalue(claimed, f"stage claim:{key}") == SAFE_PHYSICAL_MARGINS[key]
                and qvalue(
                    row["typed_boundary_actual_interval_lower_minima"][key],
                    f"stage actual:{key}",
                )
                > SAFE_PHYSICAL_MARGINS[key],
                f"stage strict margin:{key}",
            )
            require_integer(row["typed_boundary_check_counts"][key], f"stage count:{key}")
        require(row["row_sha256"] == row_digest(row), "stage row digest")
        stage_keys.add((rank, stage))
    require(len(stage_keys) == 72, "stage unique rows")

    five = result["physical_five_face_grammar_rows"]
    seven = result["physical_seven_boundary_kind_rows"]
    require(type(five) is list and len(five) == 5, "five-face rows")
    require(type(seven) is list and len(seven) == 7, "seven-kind rows")
    require(result["physical_five_face_grammar_rows_sha256"] == digest(five),
            "five-face digest")
    require(result["physical_seven_boundary_kind_rows_sha256"] == digest(seven),
            "seven-kind digest")
    five_kinds = {
        "source_core_clipping_face",
        "intermediate_core_avoidance_preimage_face",
        "terminal_core_preimage_face",
        "collision_singularity_or_owner_change_face",
        "moving_occurrence_face",
    }
    require({row["kind"] for row in five} == five_kinds, "five-face kinds")
    for row in five:
        expected_five_keys = (
            FIVE_ROW_KEYS | MOVING_GRAMMAR_EXTRA_KEYS
            if row["kind"] == "moving_occurrence_face"
            else FIVE_ROW_KEYS
        )
        require(type(row) is dict and set(row) == expected_five_keys, "five row schema")
        require(row["actual_instance_count"] == 0, "five-face empty")
        if row["kind"] == "moving_occurrence_face":
            require(
                row["legacy_parameterized_grammar_seed_count"] == 64
                and row["rank3_candidate_occurrence_count_per_common_child"] == 169
                and row["rank3_candidate_occurrence_total_check_count"] == 4056
                and row["old_Q2_time2_atom_or_occurrence_ID_reused"] is False,
                "moving grammar census",
            )
        require(row["row_sha256"] == row_digest(row), "five row digest")
    seven_kinds = {
        "candidate_signed_tangency",
        "target_endpoint_on_wall_or_target_chart_seam",
        "target_momentum_homogeneity_face",
        "forward_integer_corner_ray",
        "coordinate_velocity_zero",
        "source_endpoint_on_wall_or_source_chart_seam",
        "source_momentum_homogeneity_face",
    }
    require({row["kind"] for row in seven} == seven_kinds, "seven kinds")
    for row in seven:
        require(type(row) is dict and set(row) == SEVEN_ROW_KEYS, "seven row schema")
        require(row["actual_instance_count"] == 0, "seven-kind empty")
        require(
            row["check_count"]
            == sum(EXPECTED_PHYSICAL_COUNTS[key] for key in row["audit_keys"]),
            "seven-kind count",
        )
        require(
            row["strict_lower_margins"]
            == {key: str(SAFE_PHYSICAL_MARGINS[key]) for key in row["audit_keys"]},
            "seven-kind margins",
        )
        require(row["row_sha256"] == row_digest(row), "seven row digest")
    physical_digest = digest(
        {
            "core": physical["core_clearance_rows_sha256"],
            "child_stage": physical["child_stage_boundary_rows_sha256"],
            "five": digest(five),
            "seven": digest(seven),
        }
    )
    require(result["physical_face_typed_empty_audit_sha256"] == physical_digest,
            "physical compound digest")

    endpoint_index = {
        (row["stage"], row["natural_index_j"]): row
        for row in r121["pullback_endpoint_rows"]
    }
    moving = result["parameterized_recut_face_rows"]
    require(type(moving) is list and len(moving) == 23, "moving face count")
    require(result["parameterized_recut_face_rows_sha256"] == digest(moving),
            "moving face digest")
    require(
        tuple(f"S{row['stage']}:{row['natural_index_j']}" for row in moving)
        == EXPECTED_CUT_ORDER,
        "moving face order",
    )
    for row in moving:
        require(type(row) is dict and set(row) == MOVING_FACE_KEYS, "moving schema")
        stage = require_integer(row["stage"], "moving stage")
        natural_index = require_integer(row["natural_index_j"], "moving natural index")
        require(stage in {1, 2}, "moving stage domain")
        endpoint = endpoint_index[(stage, natural_index)]
        payload = [
            "round122-parameterized-recut-face-v1",
            seed_id,
            stage,
            natural_index,
            endpoint["exact_root_equation_id"],
        ]
        face_id = "round122-parameterized-recut-face:" + digest(payload)
        first_claim, second_claim = ((Q(4), Q(56)), (Q(13), Q(616)))[stage - 1]
        require(
            row["face_id"] == face_id
            and row["face_kind"] == "PARAMETERIZED_ARTIFICIAL_PULLBACK_RECUT"
            and row["exact_seed_id"] == seed_id
            and row["round121_s0_endpoint_id"] == endpoint["endpoint_id"]
            and row["s0_x_dyadic_bracket"] == endpoint["x_dyadic_bracket"]
            and row["exact_level_equation_id"] == endpoint["exact_root_equation_id"]
            and row["owner_below"] == endpoint["lower_owner"]
            and row["owner_above"] == endpoint["upper_owner"]
            and row["lower_trace_id"] == trace_id(face_id, "lower")
            and row["upper_trace_id"] == trace_id(face_id, "upper"),
            "moving face crosswalk",
        )
        fx_claim = (Q(5), Q(16))[stage - 1] * DELTA
        require(
            row["F_x_sign"] == 1
            and qvalue(row["F_x_claimed_strict_lower"], "moving Fx claim") == fx_claim
            and qvalue(row["F_x_collar_abs_lower"], "moving Fx collar") > fx_claim
            and qvalue(row["F_x_s0_abs_lower"], "moving Fx s0") > fx_claim
            and qvalue(
                row["implicit_x_s_first_derivative_actual_abs_upper"],
                "moving first actual",
            )
            > 0
            and qvalue(
                row["implicit_x_s_first_derivative_actual_abs_upper"],
                "moving first actual upper",
            )
            < first_claim
            and qvalue(row["implicit_x_s_first_derivative_abs_upper"], "moving first claim")
            == first_claim
            and qvalue(
                row["implicit_x_s_second_derivative_actual_abs_upper"],
                "moving second actual",
            )
            > 0
            and qvalue(
                row["implicit_x_s_second_derivative_actual_abs_upper"],
                "moving second actual upper",
            )
            < second_claim
            and qvalue(row["implicit_x_s_second_derivative_abs_upper"], "moving second claim")
            == second_claim,
            "moving implicit derivative contract",
        )
        require(
            row["unique_analytic_graph"] is True
            and row["graph_stays_in_s0_guard"] is True
            and row["cut_order_preserved"] is True
            and row["minimum_pair_separation_lower"] == "1/200"
            and row["F8_normalized_wedge_strict_lower"] == "1/6"
            and row["artificial_not_physical"] is True
            and row["equation_decimal_participates_in_id"] is False,
            "moving graph flags",
        )
        require(
            row["boundary_label"] == f"U{stage}={natural_index}*delta"
            and row["exact_level_equation"]
            == f"U{stage}(x,s)={natural_index}*10^-90"
            and row["delta"] == "1e-90"
            and row["s_collar"] == f"|s|<={PARAMETER_RADIUS}"
            and row["base_image_chart"] == ("N", "S")[stage - 1]
            and row["base_image_obstacle"] == ("W", "G")[stage - 1]
            and row["base_curvature"] == ("25/4", "25/9")[stage - 1]
            and row["source_pullback_rank_path"] == ([15] if stage == 1 else [15, 14])
            and row["F8_formula"]
            == "(kappa+V)/(sqrt(1+kappa^2)*sqrt(1+V^2))"
            and row["F8_unstable_slope_interval"] == "25/9<V<29"
            and row["F8_worst_case_squared_residual"] == "87997/8"
            and row["F12_suffix_rank_path"] == ([14, 14] if stage == 1 else [14]),
            "moving analytic/F8/F12 metadata",
        )
        for key in ("F_s_abs_upper", "F_xx_abs_upper", "F_xs_abs_upper", "F_ss_abs_upper"):
            require(qvalue(row[key], f"moving derivative:{key}") > 0,
                    f"moving derivative positive:{key}")
        require(
            qvalue(row["F9_source_pullback_unit_speed_C2_strict_upper"], "moving F9")
            == F9_STAGE_BOUNDS[stage]
            and qvalue(row["F12_C1_trace_pullback_strict_upper"], "moving F12")
            == F12_STAGE_BOUNDS[stage],
            "moving F9/F12",
        )
        require(row["row_sha256"] == row_digest(row), "moving row digest")

    outer = result["stationary_outer_face_rows"]
    require(type(outer) is list and len(outer) == 2, "outer face count")
    require(result["stationary_outer_face_rows_sha256"] == digest(outer),
            "outer digest")
    for index, row in enumerate(outer):
        require(type(row) is dict and set(row) == OUTER_FACE_KEYS, "outer schema")
        label = ("source-left", "source-right")[index]
        x_value = index
        equation = ("u0(x,s)=0", "u0(x,s)=delta")[index]
        face_id = "round122-outer-recut-face:" + digest(
            ["round122-stationary-outer-recut-face-v1", seed_id, label, equation]
        )
        require(
            row["face_id"] == face_id
            and row["face_kind"] == "STATIONARY_ARTIFICIAL_SOURCE_OUTER_FACE"
            and row["stage"] == 0
            and row["natural_index_j"] == x_value
            and row["boundary_label"] == label
            and row["s0_x_dyadic_bracket"] == [str(x_value), str(x_value)]
            and row["F_x_sign"] == 1
            and row["F_x_s0_abs_lower"] == str(DELTA)
            and row["F_x_collar_abs_lower"] == str(DELTA)
            and row["F_x_claimed_strict_lower"] == str(DELTA)
            and row["F_s_abs_upper"] == row["F_xx_abs_upper"]
            == row["F_xs_abs_upper"] == row["F_ss_abs_upper"] == "0"
            and row["implicit_x_s_first_derivative_abs_upper"] == "0"
            and row["implicit_x_s_second_derivative_abs_upper"] == "0"
            and row["F9_source_pullback_unit_speed_C2_strict_upper"] == "0"
            and row["F12_C1_trace_pullback_strict_upper"] == str(F12_STAGE_BOUNDS[0])
            and row["external_neighbor_materialized"] is False
            and row["artificial_not_physical"] is True,
            "outer face contract",
        )
        require(
            row["delta"] == "1e-90"
            and row["s_collar"] == f"|s|<={PARAMETER_RADIUS}"
            and row["F8_normalized_wedge_strict_lower"] == "1/6"
            and row["F8_formula"]
            == "(kappa+V)/(sqrt(1+kappa^2)*sqrt(1+V^2))"
            and row["F8_unstable_slope_interval"] == "25/9<V<29"
            and row["F8_worst_case_squared_residual"] == "2350204/81"
            and row["base_curvature"] == "25/9"
            and row["base_image_chart"] == "W"
            and row["base_image_obstacle"] == "G"
            and row["source_pullback_rank_path"] == []
            and row["F12_suffix_rank_path"] == [15, 14, 14],
            "outer analytic metadata",
        )
        require(
            (row["owner_below"], row["owner_above"])
            == (
                ("EXTERNAL_NOT_MATERIALIZED", "common-rank-0")
                if index == 0
                else ("common-rank-23", "EXTERNAL_NOT_MATERIALIZED")
            ),
            "outer owners",
        )
        expected_lower = None if index == 0 else trace_id(face_id, "lower")
        expected_upper = trace_id(face_id, "upper") if index == 0 else None
        require(
            row["lower_trace_id"] == expected_lower
            and row["upper_trace_id"] == expected_upper,
            "outer trace IDs",
        )
        require(row["row_sha256"] == row_digest(row), "outer row digest")

    faces = [outer[0], *moving, outer[1]]
    face_index = {row["face_id"]: row for row in faces}
    require(len(face_index) == 25, "unique face IDs")
    traces = result["recut_face_trace_rows"]
    incidences = result["child_face_incidence_rows"]
    require(type(traces) is list and len(traces) == 48, "trace census")
    require(type(incidences) is list and len(incidences) == 24, "incidence census")
    require(result["recut_face_trace_rows_sha256"] == digest(traces), "trace digest")
    require(result["child_face_incidence_rows_sha256"] == digest(incidences),
            "incidence digest")
    trace_index: dict[tuple[str, str], dict[str, Any]] = {}
    face_position = {row["face_id"]: index for index, row in enumerate(faces)}
    for row in traces:
        require(type(row) is dict and set(row) == TRACE_ROW_KEYS, "trace schema")
        require(
            row["face_id"] in face_index
            and row["side"] in {"lower", "upper"}
            and row["trace_id"] == trace_id(row["face_id"], row["side"])
            and row["F12_C1_trace_pullback_strict_upper"]
            == face_index[row["face_id"]]["F12_C1_trace_pullback_strict_upper"]
            and row["artificial_not_physical"] is True,
            "trace contract",
        )
        position = face_position[row["face_id"]]
        expected_rank = position - 1 if row["side"] == "lower" else position
        require(
            row["adjacent_common_rank"] == expected_rank
            and row["adjacent_common_child_id"] == child_ids[expected_rank]
            and row["external_neighbor_materialized"]
            is (row["face_id"] not in {outer[0]["face_id"], outer[1]["face_id"]})
            and row["owner_predicate"]
            == (
                "lower side owns points below the analytic level"
                if row["side"] == "lower"
                else "upper side owns the analytic level and points above it"
            ),
            "trace adjacency/ownership",
        )
        require(row["row_sha256"] == row_digest(row), "trace row digest")
        trace_index[(row["face_id"], row["side"])] = row
    require(len(trace_index) == 48, "unique trace sides")
    incidence_index: dict[str, dict[str, Any]] = {}
    for row in incidences:
        require(type(row) is dict and set(row) == INCIDENCE_ROW_KEYS, "incidence schema")
        rank = require_integer(row["common_rank"], "incidence rank")
        require(
            0 <= rank < 24
            and row["common_child_id"] == child_ids[rank]
            and row["lower_face_id"] == faces[rank]["face_id"]
            and row["upper_face_id"] == faces[rank + 1]["face_id"]
            and row["lower_trace_id"] == trace_id(row["lower_face_id"], "upper")
            and row["upper_trace_id"] == trace_id(row["upper_face_id"], "lower")
            and row["exactly_two_artificial_boundary_faces"] is True
            and row["both_face_origins_retained"] is True,
            "incidence crosswalk",
        )
        require(row["row_sha256"] == row_digest(row), "incidence row digest")
        incidence_index[row["common_child_id"]] = row
    require(len(incidence_index) == 24, "unique incidences")

    dynamic = result["dynamic_F11_rows"]
    require(type(dynamic) is list and len(dynamic) == 3, "dynamic F11 rows")
    for stage, row in enumerate(dynamic):
        require(type(row) is dict and set(row) == DYNAMIC_ROW_KEYS, "dynamic row schema")
        require(
            row["stage"] == stage
            and row["full_phase_dynamic_Holder_test_pullback_strict_upper"]
            == str(F11_STAGE_BOUNDS[stage])
            and row["alpha_scope"] == "0<alpha<=1"
            and row["along_seed_tight_diagnostic_upper"]
            == physical["along_seed_adapted_forward_Lipschitz_actual_upper"][stage]
            and row["along_seed_tight_diagnostic_used_as_field_value"] is False,
            "dynamic F11 contract",
        )

    slots = result["gate5_F7_F13_F16_slot_rows"]
    require(type(slots) is list and len(slots) == 960, "new slot census")
    require(result["gate5_F7_F13_F16_slot_rows_sha256"] == digest(slots), "slot digest")
    field_map = dict(NEW_FIELDS)
    slot_ids: set[str] = set()
    slot_keys: set[tuple[Any, ...]] = set()
    per_field = Counter()
    r121_f1 = {
        (
            row["official_word_key_id"],
            row["refined_homogeneous_subbranch_id"],
            row["roof_level_j"],
        ): row
        for row in r121["gate5_F1_F6_slot_rows"]
        if row["field_index"] == 1
    }
    require(len(r121_f1) == 120, "R121 F1 basis")
    for row in slots:
        require(type(row) is dict and set(row) == SLOT_ROW_KEYS, "slot row schema")
        field_index = require_integer(row["field_index"], "slot field")
        stage = require_integer(row["stage"], "slot stage")
        roof = require_integer(row["roof_level_j"], "slot roof")
        require(field_index in field_map and 0 <= stage < 3, "slot field/stage")
        base_key = (
            row["official_word_key_id"],
            row["refined_homogeneous_subbranch_id"],
            roof,
        )
        require(base_key in r121_f1, "slot R121 basis")
        base = r121_f1[base_key]
        require(
            row["common_child_id"] == base["common_child_id"]
            and row["stage"] == base["stage"]
            and row["field_name"] == field_map[field_index],
            "slot base crosswalk",
        )
        key = [
            row["official_word_key_id"],
            row["refined_homogeneous_subbranch_id"],
            roof,
            row["field_name"],
        ]
        require(
            row["immutable_slot_key"] == key
            and row["slot_id"] == "round122-gate5-slot:" + digest(key),
            "slot immutable ID",
        )
        incidence = incidence_index[row["common_child_id"]]
        require(
            row["lower_artificial_face_id"] == incidence["lower_face_id"]
            and row["upper_artificial_face_id"] == incidence["upper_face_id"]
            and row["child_face_incidence_row_sha256"] == incidence["row_sha256"]
            and row["physical_face_empty_audit_sha256"] == physical_digest
            and row["complete_artificial_face_registry_digest_replicated_across_roofs"]
            is True
            and row["artificial_faces_not_erased_by_physical_empty_claim"] is True
            and row["slot_status"] == "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            "slot incidence",
        )
        pair_f9 = max(
            qvalue(face_index[incidence["lower_face_id"]][
                "F9_source_pullback_unit_speed_C2_strict_upper"
            ], "lower F9"),
            qvalue(face_index[incidence["upper_face_id"]][
                "F9_source_pullback_unit_speed_C2_strict_upper"
            ], "upper F9"),
        )
        pair_f12 = max(
            qvalue(face_index[incidence["lower_face_id"]][
                "F12_C1_trace_pullback_strict_upper"
            ], "lower F12"),
            qvalue(face_index[incidence["upper_face_id"]][
                "F12_C1_trace_pullback_strict_upper"
            ], "upper F12"),
        )
        require(
            qvalue(row["face_pair_F9_exact_max"], "slot pair F9") == pair_f9
            and qvalue(row["face_pair_F12_exact_max"], "slot pair F12") == pair_f12,
            "slot pair maxima",
        )
        expected_values = {
            7: (str(F7_ACTUAL), "STRICT_UPPER"),
            8: (str(F8_WEDGE_LOWER), "STRICT_LOWER"),
            9: (str(F9_STAGE_BOUNDS[2]), "STRICT_UPPER"),
            10: ("0", "EXACT_EMPTY_PHYSICAL_FACE"),
            11: (str(F11_STAGE_BOUNDS[stage]), "STRICT_UPPER"),
            12: (str(F12_STAGE_BOUNDS[0]), "STRICT_UPPER"),
            13: ("0", "EXACT_EMPTY_PHYSICAL_CURRENT_AND_TWO_TRACES"),
            16: ("0", "EXACT_EMPTY_PHYSICAL_FLUX_TRACE"),
        }
        require(
            (row["field_value_or_contract"], row["field_bound_semantics"])
            == expected_values[field_index],
            "slot field value",
        )
        if field_index == 7:
            require(
                row["F7_Xi_strict_upper"] == str(F7_XI)
                and row["F7_invariant_density_ratio_upper"] == str(F7_DENSITY_RATIO)
                and row["F7_actual_density_weighted_product"] == str(F7_ACTUAL),
                "slot F7 factors",
            )
        else:
            require(
                row["F7_Xi_strict_upper"] is None
                and row["F7_invariant_density_ratio_upper"] is None
                and row["F7_actual_density_weighted_product"] is None,
                "non-F7 factors",
            )
        require(
            row["F11_uses_full_phase_authoritative_envelope"] is (field_index == 11),
            "slot F11 source",
        )
        require(
            row["transparent_wall_roof_split_does_not_add_F7_F11_factor"]
            is True,
            "transparent-wall field factor",
        )
        slot_ids.add(row["slot_id"])
        slot_keys.add(tuple(key))
        per_field[field_index] += 1
    require(len(slot_ids) == len(slot_keys) == 960, "unique slots")
    require(per_field == Counter({index: 120 for index, _ in NEW_FIELDS}),
            "slots per field")
    ordered_base_rows = sorted(
        (
            row for row in r121["gate5_F1_F6_slot_rows"]
            if row["field_index"] == 1
        ),
        key=lambda row: (
            row["common_child_id"], row["stage"], row["roof_level_j"]
        ),
    )
    expected_slot_order = [
        [
            base["official_word_key_id"],
            base["refined_homogeneous_subbranch_id"],
            base["roof_level_j"],
            field_name,
        ]
        for base in ordered_base_rows
        for _field_index, field_name in NEW_FIELDS
    ]
    require(
        [row["immutable_slot_key"] for row in slots] == expected_slot_order,
        "canonical slot order",
    )

    combined = result["combined_F1_F13_F16_slot_registry"]
    inherited_ids = [row["slot_id"] for row in r121["gate5_F1_F6_slot_rows"]]
    combined_ids = inherited_ids + [row["slot_id"] for row in slots]
    require(
        combined
        == {
            "inherited_F1_F6_slot_count": 720,
            "new_F7_F13_F16_slot_count": 960,
            "combined_slot_count": 1680,
            "slot_count_per_certified_field": 120,
            "certified_field_indices": list(range(1, 14)) + [16],
            "combined_slot_ids_sha256": digest(combined_ids),
            "all_immutable_slot_keys_are_full_word_subbranch_roof_field_keys": True,
        },
        "combined slot registry",
    )

    bridge = result["field_bridge_theorems"]
    require(set(bridge) == {"F7", "F8", "F9", "F10", "F11", "F12", "F13", "F16"},
            "bridge theorem fields")
    expected_bridge_keys = {
        "F7": {
            "Xi_strict_upper", "invariant_density_ratio_upper",
            "actual_field_value_density_times_Xi", "arithmetic_identity",
            "bare_Xi_installed_as_F7",
            "transparent_wall_roof_split_does_not_add_an_F7_factor",
            "transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split",
        },
        "F8": {
            "artificial_face_count", "stationary_outer_face_count",
            "moving_implicit_recut_face_count", "common_normalized_wedge_strict_lower",
            "proof_formula", "worst_kappa", "unstable_slope_range",
            "worst_case_squared_residual",
        },
        "F9": {
            "stationary_outer_face_C2_strict_upper",
            "stage1_source_pullback_unit_speed_C2_strict_upper",
            "stage2_source_pullback_unit_speed_C2_strict_upper",
            "slot_common_strict_upper", "per_face_origin_mapping_retained",
        },
        "F10": {
            "complete_physical_five_face_incidence_count",
            "coarea_density_regular_bound",
            "artificial_recut_faces_are_not_coarea_physical_faces",
        },
        "F11": {
            "stage0_full_phase_strict_upper", "stage1_full_phase_strict_upper",
            "stage2_full_phase_strict_upper",
            "along_curve_7_3_12_used_as_field_values",
            "transparent_wall_roof_split_does_not_add_an_F11_factor",
            "transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split",
        },
        "F12": {
            "stationary_outer_suffix_rank_path",
            "stationary_outer_C1_trace_pullback_strict_upper",
            "stage1_suffix_rank_path", "stage1_C1_trace_pullback_strict_upper",
            "stage2_suffix_rank_path", "stage2_C1_trace_pullback_strict_upper",
            "slot_common_strict_upper", "internal_signed_trace_count",
            "outer_seed_side_trace_count",
        },
        "F13": {
            "physical_moving_boundary_current_count",
            "physical_one_sided_trace_count", "field_value",
            "artificial_signed_recut_traces_are_separately_typed",
        },
        "F16": {
            "physical_flux_face_trace_count", "field_value",
            "empty_physical_trace_only",
        },
    }
    for field, keys in expected_bridge_keys.items():
        require(type(bridge[field]) is dict and set(bridge[field]) == keys,
                f"{field} theorem schema")
    require(
        bridge["F7"]["Xi_strict_upper"] == str(F7_XI)
        and bridge["F7"]["invariant_density_ratio_upper"] == str(F7_DENSITY_RATIO)
        and bridge["F7"]["actual_field_value_density_times_Xi"] == str(F7_ACTUAL)
        and bridge["F7"]["bare_Xi_installed_as_F7"] is False
        and bridge["F7"]["transparent_wall_roof_split_does_not_add_an_F7_factor"]
        is True
        and bridge["F7"]["transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split"]
        is True,
        "F7 theorem",
    )
    require(
        bridge["F8"]["artificial_face_count"] == 25
        and bridge["F8"]["stationary_outer_face_count"] == 2
        and bridge["F8"]["moving_implicit_recut_face_count"] == 23
        and bridge["F8"]["common_normalized_wedge_strict_lower"] == "1/6",
        "F8 theorem",
    )
    require(
        bridge["F9"]["stationary_outer_face_C2_strict_upper"] == "0"
        and bridge["F9"]["stage1_source_pullback_unit_speed_C2_strict_upper"]
        == str(F9_STAGE_BOUNDS[1])
        and bridge["F9"]["stage2_source_pullback_unit_speed_C2_strict_upper"]
        == str(F9_STAGE_BOUNDS[2])
        and bridge["F9"]["slot_common_strict_upper"] == str(F9_STAGE_BOUNDS[2]),
        "F9 theorem",
    )
    require(
        bridge["F10"]["complete_physical_five_face_incidence_count"] == 0
        and bridge["F10"]["coarea_density_regular_bound"] == "0"
        and bridge["F10"]["artificial_recut_faces_are_not_coarea_physical_faces"]
        is True,
        "F10 theorem",
    )
    require(
        bridge["F11"]["stage0_full_phase_strict_upper"] == str(F11_STAGE_BOUNDS[0])
        and bridge["F11"]["stage1_full_phase_strict_upper"] == str(F11_STAGE_BOUNDS[1])
        and bridge["F11"]["stage2_full_phase_strict_upper"] == str(F11_STAGE_BOUNDS[2])
        and bridge["F11"]["along_curve_7_3_12_used_as_field_values"] is False
        and bridge["F11"]["transparent_wall_roof_split_does_not_add_an_F11_factor"]
        is True
        and bridge["F11"]["transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split"]
        is True,
        "F11 theorem",
    )
    require(
        bridge["F12"]["internal_signed_trace_count"] == 46
        and bridge["F12"]["outer_seed_side_trace_count"] == 2
        and bridge["F12"]["stationary_outer_C1_trace_pullback_strict_upper"]
        == str(F12_STAGE_BOUNDS[0])
        and bridge["F12"]["stage1_C1_trace_pullback_strict_upper"]
        == str(F12_STAGE_BOUNDS[1])
        and bridge["F12"]["stage2_C1_trace_pullback_strict_upper"]
        == str(F12_STAGE_BOUNDS[2])
        and bridge["F12"]["slot_common_strict_upper"] == str(F12_STAGE_BOUNDS[0]),
        "F12 theorem",
    )
    require(
        bridge["F13"]
        == {
            "physical_moving_boundary_current_count": 0,
            "physical_one_sided_trace_count": 0,
            "field_value": "0",
            "artificial_signed_recut_traces_are_separately_typed": True,
        }
        and bridge["F16"]
        == {
            "physical_flux_face_trace_count": 0,
            "field_value": "0",
            "empty_physical_trace_only": True,
        },
        "F13/F16 theorem",
    )

    expected_ledger = {
        "exact_b_seed_count": 1,
        "common_refinement_actual_child_count": 24,
        "child_stage_physical_audit_row_count": 72,
        "core_clearance_row_count": 96,
        "physical_five_face_kind_count": 5,
        "physical_seven_boundary_kind_count": 7,
        "physical_face_instance_count": 0,
        "stationary_outer_artificial_face_count": 2,
        "moving_artificial_recut_face_count": 23,
        "artificial_face_count": 25,
        "internal_signed_artificial_trace_count": 46,
        "outer_seed_side_artificial_trace_count": 2,
        "artificial_trace_count": 48,
        "child_face_incidence_row_count": 24,
        "new_field_count": 8,
        "new_slot_count": 960,
        "combined_certified_field_count": 14,
        "combined_slot_count": 1680,
        "residual_physical_face_count": 0,
        "residual_implicit_face_count": 0,
        "residual_slot_count": 0,
    }
    require(result["count_ledger"] == expected_ledger, "count ledger")
    expected_status = {
        **{
            f"F{index}": "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
            for index in list(range(1, 14)) + [16]
        },
        **{
            f"F{index}": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN"
            for index in (14, 15, 17, 18)
        },
    }
    require(result["gate5_actual_child_field_status"] == expected_status, "field status")
    require(
        result["rank3_seed_child_field_maturity"] == "14/18"
        and result["gate5_global_maturity"] == "10/18"
        and result["complete_18_field_block_count"] == 0
        and result["gate5_block_count"] == 0
        and result["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "fail-closed verdict",
    )
    expected_nonclaims = [
        "no full Borel-b family uniform materialization or ranking theorem",
        "no nonempty physical-face instance, current, trace, coarea or flux claim",
        "no identification of an artificial recut face with a physical singular face",
        "no endpoint-inclusive physical collar or cross-trace union reach",
        "no F14 regular-density operator cost",
        "no F15 standard-family operator cost",
        "no F17 dynamic-test operator cost",
        "no F18 operator phase block",
        "no complete 18-field block",
        "no global Gate5 maturity upgrade",
        "no CM2 claim",
    ]
    require(result["strict_nonclaims"] == expected_nonclaims, "strict nonclaims")
    require(
        result["strict_scope"]
        == (
            "one Round121 exact-b seed, its 24 materialized common-refinement children, "
            "the common dyadic collar |s|<=2^-512, the complete typed physical-face "
            "empty audit, and the two outer plus 23 moving artificial recut faces"
        ),
        "strict scope",
    )
    if check_pins:
        validate_pin_ledger(result["upstream_and_helper_pins"])
    else:
        require(
            type(result["upstream_and_helper_pins"]) is dict
            and len(result["upstream_and_helper_pins"]) >= 40,
            "pin ledger shape",
        )
    return {
        "physical_digest": physical_digest,
        "face_index": face_index,
        "incidence_index": incidence_index,
        "slot_ids": slot_ids,
        "seed_id": seed_id,
    }


def cross_check_core(result: dict[str, Any], core: dict[str, Any]) -> None:
    physical = result["physical_face_typed_empty_audit"]
    fresh = core["physical_boundary_replay"]
    require(core["candidate_total"] == 169, "fresh candidate total")
    require(
        fresh["certificate_repeated_child_check_counts"] == physical["check_counts"],
        "fresh physical census",
    )
    for key, value in fresh["independent_strict_lower_minima"].items():
        require(
            Q(value) > SAFE_PHYSICAL_MARGINS[key],
            f"fresh physical strict:{key}",
        )
    moving = result["parameterized_recut_face_rows"]
    fresh_faces = core["moving_face_rows"]
    require(len(moving) == len(fresh_faces) == 23, "fresh face census")
    for stored, fresh_row in zip(moving, fresh_faces):
        require(
            stored["stage"] == fresh_row["stage"]
            and stored["natural_index_j"] == fresh_row["natural_index_j"]
            and stored["F_x_sign"] == 1,
            "fresh face crosswalk",
        )
        require(
            Q(fresh_row["implicit_first_parameter_upper"])
            < Q(stored["implicit_x_s_first_derivative_abs_upper"])
            and Q(fresh_row["implicit_second_parameter_upper"])
            < Q(stored["implicit_x_s_second_derivative_abs_upper"]),
            "fresh implicit derivative claims",
        )
    require(
        core["moving_face_count"] == 23
        and core["stationary_outer_face_count"] == 2
        and core["common_refinement_child_count"] == 24
        and core["slots_per_field"] == 120,
        "fresh face/child/slot counts",
    )
    fields = core["field_constants"]
    require(
        fields["F7_actual_density_times_Xi"] == str(F7_ACTUAL)
        and fields["F7_Xi"] == str(F7_XI)
        and fields["F7_density_ratio"] == str(F7_DENSITY_RATIO),
        "fresh F7 arithmetic",
    )


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    cursor = root
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def get_path(root: Any, path: tuple[Any, ...]) -> Any:
    cursor = root
    for key in path:
        cursor = cursor[key]
    return cursor


def resign_document(document: dict[str, Any]) -> None:
    """Re-sign every nested digest after a hostile semantic mutation."""

    result = document["result"]
    physical = result["physical_face_typed_empty_audit"]
    for key in ("core_clearance_rows", "child_stage_boundary_rows"):
        for row in physical[key]:
            row["row_sha256"] = row_digest(row)
    physical["core_clearance_rows_sha256"] = digest(physical["core_clearance_rows"])
    physical["child_stage_boundary_rows_sha256"] = digest(
        physical["child_stage_boundary_rows"]
    )
    for key in (
        "physical_five_face_grammar_rows",
        "physical_seven_boundary_kind_rows",
        "parameterized_recut_face_rows",
        "stationary_outer_face_rows",
        "recut_face_trace_rows",
        "child_face_incidence_rows",
    ):
        for row in result[key]:
            row["row_sha256"] = row_digest(row)
        result[f"{key}_sha256"] = digest(result[key])
    physical_digest = digest(
        {
            "core": physical["core_clearance_rows_sha256"],
            "child_stage": physical["child_stage_boundary_rows_sha256"],
            "five": digest(result["physical_five_face_grammar_rows"]),
            "seven": digest(result["physical_seven_boundary_kind_rows"]),
        }
    )
    result["physical_face_typed_empty_audit_sha256"] = physical_digest
    incidence_by_child = {
        row["common_child_id"]: row
        for row in result["child_face_incidence_rows"]
    }
    for slot in result["gate5_F7_F13_F16_slot_rows"]:
        slot["physical_face_empty_audit_sha256"] = physical_digest
        incidence = incidence_by_child.get(slot["common_child_id"])
        if incidence is not None:
            slot["child_face_incidence_row_sha256"] = incidence["row_sha256"]
        if type(slot.get("immutable_slot_key")) is list:
            slot["slot_id"] = "round122-gate5-slot:" + digest(
                slot["immutable_slot_key"]
            )
    result["gate5_F7_F13_F16_slot_rows_sha256"] = digest(
        result["gate5_F7_F13_F16_slot_rows"]
    )
    inherited = values_for_resign["r121"]["gate5_F1_F6_slot_rows"]
    combined_ids = [row["slot_id"] for row in inherited] + [
        row["slot_id"] for row in result["gate5_F7_F13_F16_slot_rows"]
    ]
    result["combined_F1_F13_F16_slot_registry"][
        "combined_slot_ids_sha256"
    ] = digest(combined_ids)
    document["result_sha256"] = digest(result)


# Set only during the attack harness.  Keeping the immutable Round121 rows out
# of every mutation closure makes the re-signing logic explicit and stable.
values_for_resign: dict[str, Any] = {}


def semantic_attacks(
    baseline: dict[str, Any],
    values: dict[str, Any],
    core: dict[str, Any],
) -> list[str]:
    global values_for_resign
    values_for_resign = values
    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = []

    def add(
        label: str,
        path: tuple[Any, ...],
        value: Any,
        *,
        check_pins: bool = False,
    ) -> None:
        attacks.append((label, lambda doc, p=path, v=value: set_path(doc, p, v), check_pins))

    def add_delete(label: str, path: tuple[Any, ...], index: int = 0) -> None:
        attacks.append(
            (
                label,
                lambda doc, p=path, i=index: get_path(doc, p).pop(i),
                False,
            )
        )

    def add_swap(label: str, path: tuple[Any, ...], left: int, right: int) -> None:
        def mutation(doc: dict[str, Any], p: tuple[Any, ...] = path) -> None:
            rows = get_path(doc, p)
            rows[left], rows[right] = rows[right], rows[left]

        attacks.append((label, mutation, False))

    r = ("result",)
    add("collar_widen", r + ("parameter_collar_contract", "epsilon"), str(2 * PARAMETER_RADIUS))
    add("collar_text_widen", r + ("parameter_collar_contract", "closed_collar"), "|s|<=2^-511")
    add("source_G_moves", r + ("parameter_collar_contract", "source_G_obstacle_is_stationary"), False)
    add("W_shift_axis", r + ("parameter_collar_contract", "W_obstacles_move_by_(s,0)"), False)
    add("cut_guard_false", r + ("parameter_collar_contract", "moving_cut_shift_below_Round121_2^-200_guard"), False)
    add("cut_pair_guard_false", r + ("parameter_collar_contract", "moving_cut_pair_shift_below_1/1000"), False)
    add("round121_modified", r + ("round121_contract", "frozen_Round121_files_modified"), True)
    add("round121_digest", r + ("round121_contract", "result_sha256"), "0" * 64)
    add_delete("physical_core_row_delete", r + ("physical_face_typed_empty_audit", "core_clearance_rows"))
    add_delete("physical_stage_row_delete", r + ("physical_face_typed_empty_audit", "child_stage_boundary_rows"))
    add("candidate_census_168", r + ("physical_face_typed_empty_audit", "rank3_candidate_occurrence_count_per_common_child"), 168)
    add("candidate_stage_census", r + ("physical_face_typed_empty_audit", "rank3_candidate_occurrence_stage_counts"), [57, 54, 57])
    add("candidate_total_census", r + ("physical_face_typed_empty_audit", "rank3_candidate_occurrence_total_check_count"), 4032)
    add("legacy_grammar_63", r + ("physical_face_typed_empty_audit", "legacy_parameterized_moving_occurrence_grammar_seed_count"), 63)
    add("old_Q2_reuse", r + ("physical_face_typed_empty_audit", "old_Q2_time2_atom_or_occurrence_ID_reused"), True)
    add("new_rank3_census_false", r + ("physical_face_typed_empty_audit", "complete_new_rank3_candidate_census_replaces_old_Q2_locator"), False)
    for key in sorted(SAFE_PHYSICAL_MARGINS):
        add(
            f"physical_margin_inflate_{key}",
            r + ("physical_face_typed_empty_audit", "claimed_strict_lower_margins", key),
            str(SAFE_PHYSICAL_MARGINS[key] + Q(1, 100)),
        )
    add("physical_minimum_zero", r + ("physical_face_typed_empty_audit", "actual_interval_lower_minima", "owner_gap"), "0")
    add("physical_incidence_nonzero", r + ("physical_face_typed_empty_audit", "physical_five_face_incidence_count"), 1)
    add("physical_residual_nonzero", r + ("physical_face_typed_empty_audit", "residual_physical_face_count"), 1)
    add_delete("five_grammar_delete", r + ("physical_five_face_grammar_rows",))
    add("five_grammar_swap_kind", r + ("physical_five_face_grammar_rows", 0, "kind"), "moving_occurrence_face")
    add("five_grammar_nonempty", r + ("physical_five_face_grammar_rows", 0, "actual_instance_count"), 1)
    add_delete("seven_grammar_delete", r + ("physical_seven_boundary_kind_rows",))
    add("seven_grammar_audit_key", r + ("physical_seven_boundary_kind_rows", 0, "audit_keys"), ["owner_gap"])
    add("seven_grammar_nonempty", r + ("physical_seven_boundary_kind_rows", 0, "actual_instance_count"), 1)
    add_delete("moving_face_delete", r + ("parameterized_recut_face_rows",))

    def duplicate_moving(doc: dict[str, Any]) -> None:
        rows = doc["result"]["parameterized_recut_face_rows"]
        rows[-1] = copy.deepcopy(rows[0])

    attacks.append(("moving_face_duplicate", duplicate_moving, False))
    add_swap("moving_face_reorder", r + ("parameterized_recut_face_rows",), 0, 1)
    add("moving_face_stage", r + ("parameterized_recut_face_rows", 0, "stage"), 1)
    add("moving_face_natural_j", r + ("parameterized_recut_face_rows", 0, "natural_index_j"), 2)
    add("moving_face_equation", r + ("parameterized_recut_face_rows", 0, "exact_level_equation"), "U2=bad")
    add("moving_face_endpoint", r + ("parameterized_recut_face_rows", 0, "round121_s0_endpoint_id"), "bad")
    add("moving_face_bracket", r + ("parameterized_recut_face_rows", 0, "s0_x_dyadic_bracket"), ["0", "1"])
    add("moving_face_Fx_sign", r + ("parameterized_recut_face_rows", 0, "F_x_sign"), -1)
    add("moving_face_Fx_inflate", r + ("parameterized_recut_face_rows", 0, "F_x_claimed_strict_lower"), str(17 * DELTA))
    add("moving_face_Fx_lower_zero", r + ("parameterized_recut_face_rows", 0, "F_x_collar_abs_lower"), "0")
    add("moving_face_Fs_shrink", r + ("parameterized_recut_face_rows", 0, "F_s_abs_upper"), "0")
    add("moving_face_Fxx_shrink", r + ("parameterized_recut_face_rows", 0, "F_xx_abs_upper"), "0")
    add("moving_face_Fxs_shrink", r + ("parameterized_recut_face_rows", 0, "F_xs_abs_upper"), "0")
    add("moving_face_Fss_shrink", r + ("parameterized_recut_face_rows", 0, "F_ss_abs_upper"), "0")
    add("moving_face_xprime_improve", r + ("parameterized_recut_face_rows", 0, "implicit_x_s_first_derivative_abs_upper"), "12")
    add("moving_face_xsecond_improve", r + ("parameterized_recut_face_rows", 0, "implicit_x_s_second_derivative_abs_upper"), "615")
    add("moving_face_unique_false", r + ("parameterized_recut_face_rows", 0, "unique_analytic_graph"), False)
    add("moving_face_order_false", r + ("parameterized_recut_face_rows", 0, "cut_order_preserved"), False)
    add("moving_face_separation_improve", r + ("parameterized_recut_face_rows", 0, "minimum_pair_separation_lower"), "1/199")
    add("moving_face_F8_improve", r + ("parameterized_recut_face_rows", 0, "F8_normalized_wedge_strict_lower"), "1/5")
    add("moving_face_F8_formula", r + ("parameterized_recut_face_rows", 0, "F8_formula"), "wrong")
    add("moving_face_kappa", r + ("parameterized_recut_face_rows", 0, "base_curvature"), "1")
    add("moving_face_cone", r + ("parameterized_recut_face_rows", 0, "F8_unstable_slope_interval"), "0<V<100")
    add("moving_face_F9_improve", r + ("parameterized_recut_face_rows", 0, "F9_source_pullback_unit_speed_C2_strict_upper"), str(F9_STAGE_BOUNDS[2] - 1))
    add("moving_face_F12_path", r + ("parameterized_recut_face_rows", 0, "F12_suffix_rank_path"), [14, 14])
    add("moving_face_F12_improve", r + ("parameterized_recut_face_rows", 0, "F12_C1_trace_pullback_strict_upper"), str(F12_STAGE_BOUNDS[2] - 1))
    add("moving_face_as_physical", r + ("parameterized_recut_face_rows", 0, "artificial_not_physical"), False)
    add_delete("outer_face_delete", r + ("stationary_outer_face_rows",))
    add("outer_Fx_zero", r + ("stationary_outer_face_rows", 0, "F_x_claimed_strict_lower"), "0")
    add("outer_Fx_noncanonical", r + ("stationary_outer_face_rows", 0, "F_x_claimed_strict_lower"), "01/10")
    add("outer_owner", r + ("stationary_outer_face_rows", 0, "owner_above"), "wrong")
    add("outer_as_physical", r + ("stationary_outer_face_rows", 0, "artificial_not_physical"), False)
    add_delete("trace_delete", r + ("recut_face_trace_rows",))
    add("trace_side", r + ("recut_face_trace_rows", 0, "side"), "lower")
    add("trace_child", r + ("recut_face_trace_rows", 0, "adjacent_common_child_id"), "wrong")
    add("trace_as_physical", r + ("recut_face_trace_rows", 0, "artificial_not_physical"), False)
    add_delete("incidence_delete", r + ("child_face_incidence_rows",))

    def swap_incidence_faces(doc: dict[str, Any]) -> None:
        row = doc["result"]["child_face_incidence_rows"][0]
        row["lower_face_id"], row["upper_face_id"] = row["upper_face_id"], row["lower_face_id"]

    attacks.append(("incidence_face_swap", swap_incidence_faces, False))
    add("incidence_two_faces_false", r + ("child_face_incidence_rows", 0, "exactly_two_artificial_boundary_faces"), False)
    add("F7_bare_Xi", r + ("field_bridge_theorems", "F7", "bare_Xi_installed_as_F7"), True)
    add("F7_density", r + ("field_bridge_theorems", "F7", "invariant_density_ratio_upper"), "1")
    add("F7_product", r + ("field_bridge_theorems", "F7", "actual_field_value_density_times_Xi"), str(F7_XI))
    add("F7_roof_factor", r + ("field_bridge_theorems", "F7", "transparent_wall_roof_split_does_not_add_an_F7_factor"), False)
    add("F8_theorem_improve", r + ("field_bridge_theorems", "F8", "common_normalized_wedge_strict_lower"), "1/5")
    add("F9_stage1_improve", r + ("field_bridge_theorems", "F9", "stage1_source_pullback_unit_speed_C2_strict_upper"), str(F9_STAGE_BOUNDS[1] - 1))
    add("F9_stage2_improve", r + ("field_bridge_theorems", "F9", "stage2_source_pullback_unit_speed_C2_strict_upper"), str(F9_STAGE_BOUNDS[2] - 1))
    add("F10_nonzero", r + ("field_bridge_theorems", "F10", "coarea_density_regular_bound"), "1")
    add("F11_tight_seed_value", r + ("field_bridge_theorems", "F11", "stage0_full_phase_strict_upper"), "7")
    add("F11_roof_factor", r + ("field_bridge_theorems", "F11", "transparent_wall_roof_split_does_not_add_an_F11_factor"), False)
    add("F12_bound_improve", r + ("field_bridge_theorems", "F12", "slot_common_strict_upper"), str(F12_STAGE_BOUNDS[0] - 1))
    add("F13_nonzero", r + ("field_bridge_theorems", "F13", "field_value"), "1")
    add("F16_nonzero", r + ("field_bridge_theorems", "F16", "field_value"), "1")
    add("dynamic_F11_seed_value", r + ("dynamic_F11_rows", 0, "full_phase_dynamic_Holder_test_pullback_strict_upper"), "7")
    add("dynamic_F11_diagnostic_used", r + ("dynamic_F11_rows", 0, "along_seed_tight_diagnostic_used_as_field_value"), True)
    add_delete("slot_delete", r + ("gate5_F7_F13_F16_slot_rows",))
    add_swap("slot_reorder", r + ("gate5_F7_F13_F16_slot_rows",), 0, 1)
    add("slot_key", r + ("gate5_F7_F13_F16_slot_rows", 0, "immutable_slot_key", 3), "wrong")
    add("slot_field", r + ("gate5_F7_F13_F16_slot_rows", 0, "field_index"), 8)
    add("slot_roof", r + ("gate5_F7_F13_F16_slot_rows", 0, "roof_level_j"), 99)
    add("slot_subbranch", r + ("gate5_F7_F13_F16_slot_rows", 0, "refined_homogeneous_subbranch_id"), "wrong")
    add("slot_child", r + ("gate5_F7_F13_F16_slot_rows", 0, "common_child_id"), "wrong")
    add("slot_face_pair_F9", r + ("gate5_F7_F13_F16_slot_rows", 0, "face_pair_F9_exact_max"), "0")
    add("slot_bare_Xi", r + ("gate5_F7_F13_F16_slot_rows", 0, "field_value_or_contract"), str(F7_XI))
    add("slot_F7_density", r + ("gate5_F7_F13_F16_slot_rows", 0, "F7_invariant_density_ratio_upper"), "1")
    add("slot_roof_factor", r + ("gate5_F7_F13_F16_slot_rows", 0, "transparent_wall_roof_split_does_not_add_F7_F11_factor"), False)
    add("slot_F11_source", r + ("gate5_F7_F13_F16_slot_rows", 4, "F11_uses_full_phase_authoritative_envelope"), False)
    add("combined_fields_add_F14", r + ("combined_F1_F13_F16_slot_registry", "certified_field_indices"), list(range(1, 17)))
    first_pin = next(iter(baseline["result"]["upstream_and_helper_pins"]))
    add("upstream_pin", r + ("upstream_and_helper_pins", first_pin), "0" * 64, check_pins=True)
    add("precision_downgrade", r + ("precision_bits",), 1024)
    add("count_ledger", r + ("count_ledger", "new_slot_count"), 959)
    add("maturity_inflate", r + ("rank3_seed_child_field_maturity",), "15/18")
    add("global_gate_inflate", r + ("gate5_global_maturity",), "11/18")
    add("F14_install", r + ("gate5_actual_child_field_status", "F14"), "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN")
    add("complete_block_inflate", r + ("complete_18_field_block_count",), 1)
    add("gate5_block_inflate", r + ("gate5_block_count",), 1)
    add("CM2_inflate", r + ("cm2_verdict",), "GO_FOR_CLAIM")
    add_delete("nonclaim_delete", r + ("strict_nonclaims",))
    add("scope_inflate", r + ("strict_scope",), "all Borel seeds")
    add("schema_mutation", ("schema",), "cm2.round122.mutant")
    attacks.append(("unknown_result_field", lambda doc: doc["result"].__setitem__("unknown", 1), False))
    add("bool_as_precision", r + ("precision_bits",), True)
    attacks.append(
        (
            "unknown_moving_row_field",
            lambda doc: doc["result"]["parameterized_recut_face_rows"][0].__setitem__(
                "unknown", True
            ),
            False,
        )
    )

    rejected: list[str] = []
    for label, mutation, check_pins in attacks:
        mutant = copy.deepcopy(baseline)
        mutation(mutant)
        resign_document(mutant)
        try:
            static_contract(mutant, values, check_pins=check_pins)
            cross_check_core(mutant["result"], core)
        except (AssertionError, KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"semantic mutant accepted:{label}")
    require(len(rejected) >= 75 and len(rejected) == len(attacks),
            "semantic attack census")
    return rejected


def strict_json_attacks(
    baseline: dict[str, Any], values: dict[str, Any]
) -> list[str]:
    oversized = "1" * 1025
    parser_cases = [
        ("top_duplicate_key", '{"a":1,"a":2}'),
        ("deep_duplicate_key", '{"a":{"b":1,"b":2}}'),
        ("NaN", '{"a":NaN}'),
        ("Infinity", '{"a":Infinity}'),
        ("negative_Infinity", '{"a":-Infinity}'),
        ("JSON_float", '{"a":1.0}'),
        ("JSON_exponent", '{"a":1e9999}'),
        ("top_array", "[]"),
        ("top_null", "null"),
        ("negative_zero", '{"a":-0}'),
        ("oversized_integer", '{"a":' + oversized + "}"),
        ("BOM", "\ufeff{}"),
        ("unpaired_surrogate", '{"a":"\\ud800"}'),
    ]
    rejected: list[str] = []
    for label, text in parser_cases:
        try:
            strict_json(text)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict JSON mutant accepted:{label}")

    for label, path, value in (
        ("bool_as_integer", ("result", "precision_bits"), True),
        (
            "noncanonical_fraction",
            (
                "result",
                "parameterized_recut_face_rows",
                0,
                "F_x_claimed_strict_lower",
            ),
            "01/2",
        ),
    ):
        mutant = copy.deepcopy(baseline)
        set_path(mutant, path, value)
        resign_document(mutant)
        text = json.dumps(mutant, sort_keys=True)
        try:
            parsed = strict_json(text)
            static_contract(parsed, values, check_pins=False)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"strict contract mutant accepted:{label}")
    require(len(rejected) == 15, "strict JSON attack census")
    return rejected


def verification_result(
    certificate: Path,
    document: dict[str, Any],
    values: dict[str, Any],
) -> dict[str, Any]:
    static = static_contract(document, values)
    core = core_replay()
    cross_check_core(document["result"], core)
    semantic = semantic_attacks(document, values, core)
    strict = strict_json_attacks(document, values)
    return {
        "verdict": "PASS",
        "verification_precision_bits": VERIFIER_PRECISION_BITS,
        "certificate_sha256": sha256(certificate),
        "certificate_result_sha256": document["result_sha256"],
        "independent_candidate_stage_counts": [57, 55, 57],
        "independent_candidate_count": core["candidate_total"],
        "independent_physical_check_counts": core[
            "physical_boundary_replay"
        ]["certificate_repeated_child_check_counts"],
        "stationary_outer_face_count": core["stationary_outer_face_count"],
        "moving_implicit_face_count": core["moving_face_count"],
        "common_refinement_actual_child_count": core[
            "common_refinement_child_count"
        ],
        "artificial_trace_count": len(document["result"]["recut_face_trace_rows"]),
        "new_certified_field_indices": [index for index, _ in NEW_FIELDS],
        "slot_count_per_new_field": core["slots_per_field"],
        "new_full_key_slot_count": len(static["slot_ids"]),
        "combined_F1_F13_F16_slot_count": document["result"][
            "combined_F1_F13_F16_slot_registry"
        ]["combined_slot_count"],
        "F7_Xi": str(F7_XI),
        "F7_density_ratio": str(F7_DENSITY_RATIO),
        "F7_actual_density_weighted_value": str(F7_ACTUAL),
        "semantic_attack_count": len(semantic),
        "semantic_attack_labels": semantic,
        "strict_JSON_attack_count": len(strict),
        "strict_JSON_attack_labels": strict,
        "upstream_and_helper_pin_count": len(
            document["result"]["upstream_and_helper_pins"]
        ),
        "rank3_seed_child_field_maturity": "14/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
    }


def write_verification(
    certificate: Path, output: Path | None
) -> None:
    document = strict_json(certificate.read_text(encoding="utf-8"))
    values = load_inputs()
    result = verification_result(certificate, document, values)
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    text = json.dumps(envelope, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(text, end="")
    else:
        output.write_text(text, encoding="utf-8")


def write_core(path: Path | None) -> None:
    result = core_replay()
    payload = {
        "schema": VERIFICATION_SCHEMA + ".core.v1",
        "result": result,
        "result_sha256": digest(result),
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(text, end="")
    else:
        path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="run the independent 3072-bit mathematical replay before the final certificate exists",
    )
    args = parser.parse_args()
    ctx.prec = VERIFIER_PRECISION_BITS
    if args.core_only:
        write_core(args.output)
        return
    if not args.certificate.is_file():
        raise SystemExit(
            "Round122 certificate is not present; run --core-only while the producer is pending"
        )
    write_verification(args.certificate, args.output)


if __name__ == "__main__":
    main()
