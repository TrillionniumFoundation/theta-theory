#!/usr/bin/env python3
"""Independent verifier for the Round119 extended-cylinder reach certificate.

This module deliberately does not import the Round119 producer.  It rebuilds
the reverse-projective-q two-jet on the eight corrected base traces and the
implicit Round115 root two-jet from pinned, older geometry modules.  It pays
per-trace reach in both unrestricted ambient extended source cylinders

    (R_0 * theta, c),       ds_c^2 = R_0^2 dtheta^2 + dc^2,
    (R_0 * theta, p),       ds_p^2 = R_0^2 dtheta^2 + dp^2.

The second statement is not an endpoint-inclusive two-sided collar in bounded
physical phase ``|p|<=1``: at c=0 one has p=+/-1 on its boundary.
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
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE
    / "cm2-round119-rank3-eight-grazing-trace-extended-cylinder-reach-2026-07-23.json"
)
ROUND87 = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
ROUND99 = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
ROUND111 = (
    HERE
    / "cm2-round111-rank3-round101-zero-width-correction-impact-audit-2026-07-23.json"
)
ROUND115 = HERE / "cm2-round115-rank3-selected-lift-nofold-atlas-2026-07-23.json"
ROUND118 = (
    HERE
    / "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json"
)

CERTIFICATE_SCHEMA = "cm2.round119.rank3-eight-grazing-trace-extended-cylinder-reach.v1"
VERIFICATION_SCHEMA = (
    "cm2.round119.rank3-eight-grazing-trace-extended-cylinder-reach-verification.v1"
)
UPSTREAM_SCHEMAS = {
    ROUND87.name: "cm2.round87.rank3-port-event-continuation.v1",
    ROUND99.name: "cm2.round99.rank3-registered-port-candidate-audit.v1",
    ROUND111.name: "cm2.round111.rank3-round101-zero-width-correction-impact-audit.v1",
    ROUND115.name: "cm2.round115.rank3-selected-lift-nofold-atlas.v1",
    ROUND118.name: "cm2.round118.rank3-repaired-endpoint-source-cylinder-transfer-atlas.v1",
}
UPSTREAM_PINS = {
    ROUND87.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    ROUND99.name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    ROUND111.name: "e343a15d5ad4838c2b9a808d64f9724e564e850cbdb13168c5e31e8f059794f1",
    ROUND115.name: "bcaa3612fe6369b7a6a55e51cd7d345d3a7e4817906dd5998ad544d945035263",
    ROUND118.name: "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f",
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_round76_r2_numeric_fields_generator.py": (
        "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf"
    ),
    "cm2_round93_rank3_full_source_chart_exit_cert.py": (
        "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023"
    ),
    "cm2_round95_rank3_centered_reverse_interval_cert.py": (
        "c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b"
    ),
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": (
        "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f"
    ),
}
EXPECTED_CERTIFICATE_PINS = {
    "cm2-round118-rank3-repaired-endpoint-source-cylinder-transfer-atlas-2026-07-23.json": (
        "91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f"
    ),
    "cm2_round118_rank3_repaired_endpoint_source_cylinder_transfer_atlas.py": (
        "bfd517d6dd71aa923ed89400719302bd022945db9cce38e4b74f163ed0fa45f4"
    ),
    ROUND115.name: UPSTREAM_PINS[ROUND115.name],
    "cm2_round115_rank3_selected_lift_nofold_atlas.py": (
        "2552bcd8ad4cf769b2d65665d43e661331fffd9a0e00330af4bb11283169db7b"
    ),
    "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json": (
        "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4"
    ),
    "cm2_round114_rank3_seam_root_stitch_gap_atlas.py": (
        "47a231e32df2121058185a0fd82cbfb6c6105ace0d268a257103bc005b46ed02"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": UPSTREAM_PINS[
        "cm2_gate25_physical_return_core_registry_cert.py"
    ],
    "cm2_round76_r2_numeric_fields_generator.py": UPSTREAM_PINS[
        "cm2_round76_r2_numeric_fields_generator.py"
    ],
    "cm2_round79_tangency_intersection_generator.py": (
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7"
    ),
    "cm2_round93_rank3_full_source_chart_exit_cert.py": UPSTREAM_PINS[
        "cm2_round93_rank3_full_source_chart_exit_cert.py"
    ],
    "cm2_round95_rank3_centered_reverse_interval_cert.py": UPSTREAM_PINS[
        "cm2_round95_rank3_centered_reverse_interval_cert.py"
    ],
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": UPSTREAM_PINS[
        "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py"
    ],
}

VERIFIER_PRECISION_BITS = 1024
BASE_INITIAL_PARTITION = 1024
BASE_MAX_SPLIT_DEPTH = 32
JOIN_PARTITION = 512
JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH = 1
JOIN_REPLAY_MAX_REFINEMENT_DEPTH = 3
EDGE_WIDTH = Q(1, 16384)
ROOT_TUBE_RADIUS = Q(3, 100_000_000)
THETA_FIRST_LOWER = Q(2, 5)
THETA_FIRST_UPPER = Q(28)
THETA_SECOND_UPPER = Q(30_000_000)
SOURCE_RADIUS = Q(9, 25)
M = Q(18, 125)
A = Q(11_000_000)
RHO = Q(1, 2_500_000_000)
NORMAL_MAP_MARGIN = Q(49, 15_625)
ENDPOINT_TAYLOR_MARGIN = Q(1021, 62_500)
NORMAL_MAP_DETERMINANT_LOWER = Q(1021, 9_000)
PROJECTIVE_LIFT_ANGULAR_SPAN = Q(3, 2)
PERIODIC_LIFT_CLEARANCE = Q(81, 50)
MOMENTUM_ABS_LOWER = Q(1, 51)
MOMENTUM_SECOND_UPPER = Q(132_651)
SOURCE_ACCELERATION_UPPER = Q(10_800_000)
AMBIENT_MOMENTUM_ACCELERATION_UPPER = Q(10_932_651)
EXPECTED_ROOT_LEAF_COUNTS = (512, 512, 512, 512, 512, 512, 2048, 2048)

JOIN_LOWER_REPLAY_FIELDS = {
    "root_equation_error_derivative_abs_lower_bound": "root_fe_lower",
    "root_q_second_derivative_abs_lower_bound": "q_second_lower",
    "first_discriminant_lower_bound": "first_discriminant_lower",
    "second_discriminant_lower_bound": "second_discriminant_lower",
    "source_to_first_flight_lower_bound": "first_flight_lower",
    "first_to_second_flight_lower_bound": "second_flight_lower",
    "second_to_tangent_flight_lower_bound": "tangent_flight_lower",
    "projective_q_denominator_lower_bound": "projective_q_denominator_lower",
    "signed_tangent_side_lower_bound": "signed_tangent_side_lower",
}
JOIN_UPPER_REPLAY_FIELDS = {
    "correlated_root_error_enclosure_width_upper": "maximum_error_width",
    "tangent_side_residual_abs_upper": "maximum_tangent_side_residual",
    "low_level_equation_residual_abs_upper": "maximum_equation_residual",
}

# Each orthogonal matrix selects one projective normal lift.  Reflections are
# intentional: all eight lifted theta derivatives then have the same sign.
PROJECTIVE_MATRICES = (
    ((0, -1), (1, 0)),
    ((0, 1), (1, 0)),
    ((-1, 0), (0, 1)),
    ((1, 0), (0, 1)),
    ((-1, 0), (0, -1)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
    ((0, 1), (-1, 0)),
)

EXPECTED_SCOPE = (
    "eight individual repaired source-grazing traces; per-trace self-reach in the "
    "extended cosine and momentum source cylinders, including endpoint and periodic "
    "copy cases; no separation between different traces or other singular strata"
)
EXPECTED_NONCLAIMS = [
    "the eight traces are certified separately; reach of their union is not installed",
    "no uniform separation from other collision singularities, wall corners, flight caps, or unrelated strata is installed",
    "at c=0 one has p=+1 or -1, so the bounded physical phase space admits no endpoint-inclusive two-sided momentum collar",
    "extended-cylinder/stratified-master reach is not a physical-owner collar and does not create a standard-curve child",
    "no complete 57-candidate collar ordering, homogeneity child, official word, or Gate5 field is installed",
]
EXPECTED_UNIT_IDENTITY_GEOMETRIC_PROOF = (
    "each circle normal is (hit-center)/R and the certified hit equation gives unit "
    "norm; the stereographic tangent direction is unit and reflection preserves norm, "
    "so both normal0 and initial are unit vectors.  The planar Lagrange "
    "identity (initial dot normal0)^2+(normal0 cross initial)^2="
    "|initial|^2|normal0|^2 gives c^2+p^2=1 exactly"
)
EXPECTED_EXACT_MOMENTUM_CONTRACT = {
    "definitions": "c=initial dot normal0; p=normal0 cross initial",
    "unit_chain": (
        "on the base, circle normalization and the certified hit equations make "
        "normal0 unit, while the stereographic tangent is unit and specular "
        "reflections are orthogonal, so initial is unit; planar Lagrange gives "
        "c^2+p^2=1 exactly. On the root, the source-chart normal is unit and "
        "p=sigma0*sqrt(1-c^2) by construction, giving the same identity directly"
    ),
    "splice_branch_identity": (
        "the exact geometric involution identifies the base and root states on the "
        "positive-width overlap with the same fixed sigma0 momentum branch"
    ),
    "fixed_momentum_branch_abs_lower_bound": str(MOMENTUM_ABS_LOWER),
    "first_derivative_exact": "p_c=-c/p",
    "second_derivative_exact": "p_cc=-1/p^3",
    "momentum_second_derivative_bound_derivation": (
        "|p|>1/51 implies |p_cc|=1/|p|^3<51^3=132651"
    ),
    "metric_speed_bound_derivation": (
        "r_c=(9/25)*theta_c>(9/25)*(2/5)=18/125, hence |gamma'|>18/125"
    ),
    "metric_acceleration_bound_derivation": (
        "|r_cc|<10800000 and |p_cc|<132651 imply "
        "|gamma''|<=|r_cc|+|p_cc|<10932651<11000000"
    ),
    "endpoint_values": "c=0 and p=sigma0 in {+1,-1}",
    "analytic_derivatives_used_for_speed_and_acceleration_bounds": True,
}
EXPECTED_DOUBLE_MINIMIZER_PROOF = (
    "if y has two nearest points gamma(c),gamma(d), c<d, h=d-c, "
    "w=y-gamma(c), Delta=gamma(d)-gamma(c), equal distance gives "
    "w dot Delta=|Delta|^2/2.  At the lower point, interior stationarity "
    "or the left-endpoint one-sided minimum gives w dot gamma'(c)<=0. "
    "Taylor gives Delta=h*gamma'(c)+E with |E|<=A*h^2/2, hence "
    "|Delta|^2/2<=rho*A*h^2/2, while r'>=m gives |Delta|>=m*h. "
    "This contradicts m^2-A*rho=1021/62500>0 and covers every "
    "interior/endpoint combination, including both endpoints"
)
EXPECTED_NORMAL_MAP_INJECTIVITY_PROOF = (
    "N'=J(I-TT^T)gamma''/|gamma'| gives |N'|<=A/m.  For h<=m/A, "
    "tangent projection gives at least m*h/2 while two normal offsets "
    "give less than rho*A*h/m<m*h/4.  For h>=m/A, monotone r separates "
    "centres by at least m^2/A>2*rho.  Same-parameter offsets are unique"
)
EXPECTED_PERIODIC_COPY_PROOF = (
    "each lifted angular span is <3/2.  Since pi>3, distinct 2*pi "
    "copies of the centre trace are separated in r by more than "
    "(9/25)*(6-3/2)=81/50>2*rho; also rho<3R/4<pi*R/4"
)
EXPECTED_JOIN_PROOFS = {
    "exact_identity_proof": (
        "F=0 and the projective-q definition put outgoing2 on the same signed tangent "
        "line. The two specular reflections are algebraic involutions. Fixed circle-root "
        "choices, incidence signs, and positive flights therefore make the reverse branch "
        "unique and return the root source state exactly"
    ),
    "unique_implicit_root_proof": (
        "the MVT error enclosure stays in the Round115 affine tube; F_e has fixed sign "
        "and the tube faces are opposite. Thus no second source state on this branch can "
        "share the same (c,q) data"
    ),
    "c2_splice_proof": (
        "the exact involution identity holds on the positive-width analytic neighborhood "
        "[edge/2,edge], where q_prime is nonzero. Hence theta,c,p and their first/second "
        "derivatives agree through the closure at the unique c=edge root. Base metric "
        "coverage contains its frozen q enclosure and root bounds begin at c=edge"
    ),
}

RESULT_KEYS = frozenset(
    {
        "precision_bits",
        "arithmetic",
        "input_repaired_source_grazing_trace_count",
        "certified_whole_trace_c2_splice_count",
        "certified_per_trace_ambient_extended_cosine_master_reach_count",
        "certified_per_trace_ambient_extended_momentum_cylinder_reach_count",
        "pinned_round115_corner_stationary_identity_replayed_count",
        "pinned_round115_root_existence_uniqueness_contract_replayed_count",
        "certified_periodic_copy_separation_count",
        "cross_trace_union_reach_count",
        "source_component",
        "source_radius",
        "ambient_models",
        "threshold_contract",
        "unit_identity_geometric_proof",
        "unit_identity_geometric_proof_certified",
        "exact_unit_identity_and_analytic_momentum_derivative_contract",
        "interval_dependency_residual_width_used_as_acceptance_predicate",
        "root_base_global_regularization",
        "reach_theorem",
        "base_initial_partition_count_per_trace",
        "base_maximum_adaptive_depth",
        "base_total_accepted_leaf_count",
        "base_accepted_leaf_counts",
        "base_achieved_maximum_depths",
        "root_total_dyadic_leaf_count",
        "trace_rows",
        "trace_rows_sha256",
        "physical_endpoint_obstruction",
        "strict_scope",
        "strict_nonclaims",
        "physical_owner_whole_trace_atlas_installed",
        "bounded_phase_space_endpoint_inclusive_two_sided_collar_count",
        "whole_trace_uniform_other_singularity_separation_count",
        "actual_standard_curve_child_count",
        "canonical_curve_recut_instance_count",
        "new_gate5_actual_child_field_count",
        "gate5_child_field_counts",
        "gate5_global_maturity",
        "gate5_block_count",
        "cm2_verdict",
        "upstream_and_helper_pins",
    }
)
TRACE_KEYS = frozenset(
    {
        "ray_index",
        "repaired_endpoint_id",
        "exterior_port_id",
        "branch_key",
        "projective_end",
        "source_component",
        "source_radius",
        "source_grazing_sign_sigma0",
        "local_normal_matrix",
        "local_angular_lift",
        "local_matrix_is_orthogonal",
        "local_matrix_orientation_may_be_reflected",
        "base_certificate",
        "root_certificate",
        "root_base_c2_splice_certificate",
        "whole_trace_extrema",
        "whole_trace_theta_span_strictly_below_3_over_2",
        "ambient_extended_cosine_master_self_reach",
        "ambient_extended_momentum_cylinder_self_reach",
        "periodic_source_cylinder_copy_separation_certified",
        "unit_identity_geometric_proof_certified",
        "analytic_momentum_derivatives_from_exact_identity_certified",
        "cross_trace_union_reach_installed",
        "bounded_phase_space_two_sided_endpoint_collar_installed",
    }
)
AMBIENT_MODEL_KEYS = frozenset(
    {"cosine_master", "momentum_master", "flattened_coordinate", "bounded_physical_phase_space"}
)
THRESHOLD_KEYS = frozenset(
    {
        "theta_c_strict_lower_bound",
        "theta_c_strict_upper_bound",
        "theta_cc_abs_strict_upper_bound",
        "momentum_abs_strict_lower_bound",
        "momentum_cc_abs_strict_upper_bound",
        "r_cc_abs_strict_upper_bound",
        "metric_speed_strict_lower_bound",
        "momentum_curve_acceleration_strict_upper_bound",
        "theta_span_strict_upper_bound",
        "reach_radius",
    }
)
EXTREMA_KEYS = frozenset(
    {
        "theta_lower",
        "theta_upper",
        "theta_c_lower",
        "theta_c_upper",
        "theta_cc_abs_upper",
        "momentum_abs_lower",
        "r_cc_abs_upper",
        "local_x_lower",
        "cosine_lower",
        "cosine_upper",
    }
)
WHOLE_EXTREMA_KEYS = EXTREMA_KEYS | {"theta_span_upper_bound"}
BASE_CERTIFICATE_KEYS = frozenset(
    {
        "parameter_interval",
        "q_interval",
        "initial_partition_count",
        "maximum_adaptive_depth_allowed",
        "achieved_maximum_adaptive_depth",
        "accepted_leaf_count",
        "failed_leaf_count",
        "accepted_leaf_partition_sha256",
        "fixed_reverse_path",
        "far_endpoint_source_cosine_lower_bound",
        "extrema",
        "path_and_equation_margins",
    }
)
BASE_PATH_MARGIN_KEYS = frozenset(
    {
        "oriented_minus_dc_dq_lower",
        "line_radicand_lower",
        "ray1_radicand_lower",
        "ray0_radicand_lower",
        "line_incidence_lower",
        "ray1_incidence_abs_lower",
        "ray0_incidence_abs_lower",
        "flight1_lower",
        "flight0_lower",
        "tangent_flight_lower",
        "tangent_equation_residual_abs_upper",
    }
)
ROOT_CERTIFICATE_KEYS = frozenset(
    {
        "root_coordinate_interval",
        "dyadic_leaf_power",
        "dyadic_leaf_count",
        "failed_leaf_count",
        "leaf_q_second_sign_sha256",
        "equation_error_derivative_abs_lower_bound",
        "q_second_derivative_abs_lower_bound",
        "exact_corner_identity",
        "strict_positive_c_q_prime_sign",
        "fixed_regular_reverse_path_for_c0_positive",
        "root_tube_forward_path_margins",
        "source_reverse_radicand_exact_factorization",
        "source_reverse_incidence_exact_factorization",
        "projective_q_prime_exact_endpoint_factorization",
        "regular_open_root_source_radicand_and_incidence_strict_for_c0_positive",
        "endpoint_stratum",
        "closed_root_downstream_radicands_incidences_and_three_flights_certified",
        "closed_root_source_grazing_quantity_falsely_claimed_strict",
        "extrema",
    }
)
ROOT_PATH_MARGIN_KEYS = frozenset(
    {
        "first_discriminant_lower",
        "second_discriminant_lower",
        "first_incidence_square_lower",
        "second_incidence_square_lower",
        "source_to_first_flight_lower",
        "first_to_second_flight_lower",
        "second_to_tangent_flight_lower",
        "third_tangency_equation_residual_abs_upper",
        "root_error_enclosure_width_upper",
    }
)
ENDPOINT_STRATUM_KEYS = frozenset(
    {
        "source_cosine",
        "source_reverse_radicand",
        "source_reverse_incidence",
        "source_momentum",
        "projective_q_prime",
        "kept_in_singularity_ledger",
        "counted_as_regular_collision_owner",
    }
)
JOIN_CERTIFICATE_KEYS = frozenset(
    {
        "join_mode",
        "canonical_splice_root_coordinate",
        "canonical_splice_projective_parameter_enclosure",
        "base_metric_cover_parameter_upper",
        "base_metric_cover_contains_splice_enclosure",
        "outer_upper_is_only_a_cover_bound_not_an_asserted_physical_point",
        "additional_projective_path_anchor_interval",
        "additional_projective_path_anchor_width",
        "strict_interior_projective_anchor_at_c_edge_over_2",
        "correlated_positive_c_identity_neighborhood",
        "correlated_positive_c_identity_neighborhood_certified",
        "correlated_partition_count",
        "correlated_partition_sha256",
        "fixed_reverse_path",
        "root_equation_error_derivative_abs_lower_bound",
        "root_q_second_derivative_abs_lower_bound",
        "derived_root_q_prime_abs_lower_bound_on_identity_neighborhood",
        "derived_q_prime_proof",
        "first_discriminant_lower_bound",
        "second_discriminant_lower_bound",
        "source_to_first_flight_lower_bound",
        "first_to_second_flight_lower_bound",
        "second_to_tangent_flight_lower_bound",
        "projective_q_denominator_lower_bound",
        "signed_tangent_side_lower_bound",
        "tangent_side_identity",
        "tangent_side_residual_abs_upper",
        "tangent_side_residual_width_used_as_acceptance_predicate",
        "correlated_root_error_enclosure_width_upper",
        "low_level_equation_residual_abs_upper",
        "raw_interval_state_composition_used_as_acceptance_predicate",
        "raw_whole_q_image_minmax_used_as_acceptance_predicate",
        "exact_identity_proof",
        "unique_implicit_root_proof",
        "c2_splice_proof",
        "physical_state_c2_join_certified",
    }
)
REACH_THEOREM_KEYS = frozenset(
    {
        "common_monotone_coordinate",
        "ambient_models_paid_by_this_common_lemma",
        "strict_r_derivative_lower_bound",
        "common_acceleration_upper_bound",
        "certified_radius",
        "double_minimizer_exact_margin_m2_minus_A_rho",
        "normal_map_exact_margin_m2_minus_4A_rho",
        "normal_map_determinant_lower_bound",
        "double_minimizer_proof",
        "normal_map_injectivity_proof",
        "periodic_copy_proof",
        "compact_nearest_point_existence",
        "endpoint_cases_paid_inside_double_minimizer_argument",
        "periodic_cylinder_copy_separation_paid",
    }
)

_CANONICAL_Q = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_int(token: str) -> int:
    if token == "-0" or len(token.lstrip("-")) > 1024:
        raise ValueError(f"noncanonical or oversized JSON integer: {token[:40]}")
    return int(token)


def reject_float(token: str) -> Any:
    raise ValueError(f"JSON floating-point number forbidden: {token}")


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_json(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_int=strict_int,
        parse_float=reject_float,
        parse_constant=reject_nonfinite,
    )
    validate_json_unicode(value)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value is not an object")
    return value


def validate_json_unicode(value: Any) -> None:
    if isinstance(value, str):
        value.encode("utf-8", errors="strict")
        return
    if isinstance(value, list):
        for entry in value:
            validate_json_unicode(entry)
        return
    if isinstance(value, dict):
        for key, entry in value.items():
            key.encode("utf-8", errors="strict")
            validate_json_unicode(entry)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("ascii")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qvalue(value: Any, label: str) -> Q:
    require(type(value) is str and _CANONICAL_Q.fullmatch(value) is not None, label)
    parsed = Q(value)
    require(str(parsed) == value, f"noncanonical rational: {label}")
    return parsed


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def exact_arb_endpoint(value: arb) -> Q:
    mantissa, exponent = value.man_exp()
    mantissa, exponent = int(mantissa), int(exponent)
    return (
        Q(mantissa * (1 << exponent))
        if exponent >= 0
        else Q(mantissa, 1 << (-exponent))
    )


def arb_pair(value: arb) -> tuple[Q, Q]:
    """Extract rigorous binary endpoints without parsing abbreviated display text."""

    return exact_arb_endpoint(value.lower()), exact_arb_endpoint(value.upper())


def abs_upper_q(value: arb) -> Q:
    lower, upper = arb_pair(value)
    return max(abs(lower), abs(upper))


def load_closed(path: Path, schema: str, expected_sha256: str | None = None) -> dict[str, Any]:
    if expected_sha256 is not None:
        require(sha256(path) == expected_sha256, f"byte pin: {path.name}")
    document = strict_json(path.read_text(encoding="utf-8"))
    require(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{path.name}")
    require(document["schema"] == schema, f"schema:{path.name}")
    require(document["result_sha256"] == digest(document["result"]), f"digest:{path.name}")
    require(isinstance(document["result"], dict), f"result object:{path.name}")
    return document


def add(left: tuple[Any, Any], right: tuple[Any, Any]) -> tuple[Any, Any]:
    return left[0] + right[0], left[1] + right[1]


def sub(left: tuple[Any, Any], right: tuple[Any, Any]) -> tuple[Any, Any]:
    return left[0] - right[0], left[1] - right[1]


def scale(factor: Any, vector: tuple[Any, Any]) -> tuple[Any, Any]:
    return factor * vector[0], factor * vector[1]


def dot(left: tuple[Any, Any], right: tuple[Any, Any]) -> Any:
    return left[0] * right[0] + left[1] * right[1]


def cross(left: tuple[Any, Any], right: tuple[Any, Any]) -> Any:
    return left[0] * right[1] - left[1] * right[0]


def reflect(vector: tuple[Any, Any], normal: tuple[Any, Any]) -> tuple[Any, Any]:
    return sub(vector, scale(2 * dot(vector, normal), normal))


def object_center(identifier: str) -> tuple[Jet, Jet]:
    return center(identifier, Jet(arb(0)))


def radius(identifier: str) -> Q:
    return Q(9, 25) if identifier[0] == "G" else Q(4, 25)


def tangent(
    branch: tuple[Any, ...], q: Jet
) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet]:
    ux = (1 - q * q) / (1 + q * q)
    uy = 2 * q / (1 + q * q)
    normal = (-uy, ux)
    direction = (normal[1], -normal[0])
    height = dot(normal, object_center(branch[2])) - branch[3] * aq(radius(branch[2]))
    return normal, direction, height


def line_hit(
    normal: tuple[Jet, Jet],
    direction: tuple[Jet, Jet],
    height: Jet,
    identifier: str,
    sign: int,
) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet]:
    target = object_center(identifier)
    object_radius = aq(radius(identifier))
    distance = height - dot(normal, target)
    radicand = object_radius * object_radius - distance * distance
    radical = radicand.sqrt()
    foot = add(target, scale(distance, normal))
    hit = add(foot, scale(sign * radical, direction))
    return hit, scale(1 / object_radius, sub(hit, target)), radicand


def ray_hit(
    point: tuple[Jet, Jet],
    direction: tuple[Jet, Jet],
    identifier: str,
    sign: int,
) -> tuple[tuple[Jet, Jet], tuple[Jet, Jet], Jet, Jet]:
    target = object_center(identifier)
    object_radius = aq(radius(identifier))
    delta = sub(target, point)
    longitudinal = dot(direction, delta)
    transverse = cross(direction, delta)
    radicand = object_radius * object_radius - transverse * transverse
    radical = radicand.sqrt()
    flight = longitudinal + sign * radical
    hit = add(point, scale(flight, direction))
    return hit, scale(1 / object_radius, sub(hit, target)), flight, radicand


def matrix_normal(
    matrix: tuple[tuple[int, int], tuple[int, int]], normal: tuple[Jet, Jet]
) -> tuple[Jet, Jet]:
    return (
        matrix[0][0] * normal[0] + matrix[0][1] * normal[1],
        matrix[1][0] * normal[0] + matrix[1][1] * normal[1],
    )


def reverse_q_state(
    source: Any,
    branch: tuple[Any, ...],
    q: Jet,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> dict[str, Any]:
    """Reverse a third-tangent projective-q Jet through the fixed path."""

    tangent_normal, direction, height = tangent(branch, q)
    hit2, normal2, line_radicand = line_hit(
        tangent_normal, direction, height, branch[1], path[0]
    )
    incoming2 = reflect(direction, normal2)
    reverse1 = scale(-1, incoming2)
    hit1, normal1, flight1, ray1_radicand = ray_hit(
        hit2, reverse1, source.target_id, path[1]
    )
    initial = reflect(incoming2, normal1)
    reverse0 = scale(-1, initial)
    _hit0, normal0, flight0, ray0_radicand = ray_hit(
        hit1, reverse0, f"{source.source}[0,0]", path[2]
    )
    line_incidence = dot(direction, normal2)
    ray1_incidence = dot(reverse1, normal1)
    ray0_incidence = dot(reverse0, normal0)
    trace_identity_guards = [
        line_radicand,
        ray1_radicand,
        ray0_radicand,
        line_incidence,
        -ray1_incidence,
        -ray0_incidence,
        flight1,
        flight0,
    ]
    # This base interval deliberately crosses the old source-chart seam.
    # A fixed source-chart radial sign is therefore not a physical/path gate;
    # the selected projective lift is controlled by local_x below.
    require(
        all(strict_sign(value.value) == 1 for value in trace_identity_guards),
        "reverse-q trace identity/path guard",
    )
    cosine = dot(initial, normal0)
    momentum = cross(normal0, initial)
    local_x, local_y = matrix_normal(matrix, normal0)
    z = local_y / (1 + local_x)
    third_delta = sub(object_center(branch[2]), hit2)
    tangent_flight = dot(direction, third_delta)
    tangent_transverse = cross(direction, third_delta)
    third_radius = aq(radius(branch[2]))
    tangent_residual = (
        third_radius * third_radius - tangent_transverse * tangent_transverse
    )
    return {
        "cosine": cosine,
        "momentum": momentum,
        "normal0": normal0,
        "initial": initial,
        "local_x": local_x,
        "z": z,
        "line_radicand": line_radicand,
        "ray1_radicand": ray1_radicand,
        "ray0_radicand": ray0_radicand,
        "line_incidence": line_incidence,
        "ray1_incidence": ray1_incidence,
        "ray0_incidence": ray0_incidence,
        "flight1": flight1,
        "flight0": flight0,
        "tangent_flight": tangent_flight,
        "tangent_residual": tangent_residual,
    }


def reverse_q_two_jet(
    source: Any,
    branch: tuple[Any, ...],
    qa: Q,
    qb: Q,
    path: tuple[int, int, int],
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> dict[str, Any]:
    """Rebuild the reverse-q source cosine and projective normal two-jet."""

    q = Jet.variable(interval(min(qa, qb), max(qa, qb)), 0)
    result = reverse_q_state(
        source,
        branch,
        q,
        path,
        matrix,
    )
    cosine = result["cosine"]
    z = result["z"]
    cosine_q = cosine.gradient[0]
    cosine_qq = cosine.hessian[0][0]
    momentum = result["momentum"]
    momentum_q = momentum.gradient[0]
    momentum_qq = momentum.hessian[0][0]
    z_q = z.gradient[0]
    z_qq = z.hessian[0][0]
    z_c = z_q / cosine_q
    z_cc = (z_qq * cosine_q - z_q * cosine_qq) / (
        cosine_q * cosine_q * cosine_q
    )
    result.update(
        {
            "cosine_q": cosine_q,
            "cosine_qq": cosine_qq,
            "momentum_q": momentum_q,
            "momentum_qq": momentum_qq,
            "momentum_c": momentum_q / cosine_q,
            "momentum_cc": (
                momentum_qq * cosine_q - momentum_q * cosine_qq
            ) / (cosine_q * cosine_q * cosine_q),
            "theta_c": 2 * z_c / (1 + z.value * z.value),
            "theta_cc": (
                2 * z_cc / (1 + z.value * z.value)
                - 4 * z.value * z_c * z_c / ((1 + z.value * z.value) ** 2)
            ),
        }
    )
    return result


def reverse_q_prefix(
    source: Any,
    branch: tuple[Any, ...],
    q: Jet,
    path: tuple[int, int, int],
) -> dict[str, Any]:
    """Reverse the two regular downstream legs, stopping before source grazing."""

    require(path == (1, -1, -1), "fixed reverse prefix path")
    tangent_normal, outgoing2, height = tangent(branch, q)
    hit2, normal2, line_radicand = line_hit(
        tangent_normal, outgoing2, height, branch[1], path[0]
    )
    incoming2 = reflect(outgoing2, normal2)
    reverse1 = scale(-1, incoming2)
    hit1, normal1, flight1, ray1_radicand = ray_hit(
        hit2, reverse1, source.target_id, path[1]
    )
    initial = reflect(incoming2, normal1)
    reverse0 = scale(-1, initial)
    candidate_delta = sub(object_center(branch[2]), hit2)
    tangent_flight = dot(outgoing2, candidate_delta)
    tangent_transverse = cross(outgoing2, candidate_delta)
    tangent_residual = (
        aq(radius(branch[2])) * aq(radius(branch[2]))
        - tangent_transverse * tangent_transverse
    )
    require(bool(line_radicand.value > 0), "prefix line radicand")
    require(bool(ray1_radicand.value > 0), "prefix ray1 radicand")
    require(bool(dot(outgoing2, normal2).value > 0), "prefix line incidence")
    require(bool(dot(reverse1, normal1).value < 0), "prefix ray1 incidence")
    require(bool(flight1.value > 0), "prefix flight1")
    require(bool(tangent_flight.value > 0), "prefix tangent flight")
    require(tangent_residual.value.contains(0), "prefix tangent equation")
    return {
        "hit1": hit1,
        "reverse0": reverse0,
        "tangent_residual": tangent_residual,
    }


def collision(
    point_x: Jet,
    point_y: Jet,
    velocity_x: Jet,
    velocity_y: Jet,
    target_x: Jet,
    target_y: Jet,
    target_radius: Q,
) -> dict[str, Jet]:
    object_radius = aq(target_radius)
    dx, dy = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    discriminant = object_radius * object_radius - transverse * transverse
    radical = discriminant.sqrt()
    flight = longitudinal - radical
    hit_x = point_x + flight * velocity_x
    hit_y = point_y + flight * velocity_y
    return {
        "hit_x": hit_x,
        "hit_y": hit_y,
        "normal_x": (hit_x - target_x) / object_radius,
        "normal_y": (hit_y - target_y) / object_radius,
        "momentum": transverse / object_radius,
        "discriminant": discriminant,
        "flight": flight,
    }


def chart_normal(cell: str, coordinate: Jet) -> tuple[Jet, Jet]:
    radial = (arb(1) - coordinate * coordinate).sqrt()
    if cell == "E":
        return radial, coordinate
    if cell == "W":
        return -radial, coordinate
    if cell == "N":
        return coordinate, radial
    require(cell == "S", f"unknown source chart cell:{cell}")
    return coordinate, -radial


def root_two_jet(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    matrix: tuple[tuple[int, int], tuple[int, int]],
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    c_lower: Q,
    c_upper: Q,
    error_lower: Q,
    error_upper: Q,
) -> dict[str, Jet]:
    """Rebuild the correlated implicit root and lifted source normal."""

    c0 = Jet.variable(interval(c_lower, c_upper), 0)
    error = Jet.variable(interval(error_lower, error_upper), 1)
    t = Jet(aq(t_reference)) + aq(affine_slope) * (c0 - aq(c_center)) + error
    nx0, ny0 = chart_normal(source.chart_id.split(":")[1], t)
    p0 = source_sign * (arb(1) - c0 * c0).sqrt()
    ux0, uy0 = c0 * nx0 - p0 * ny0, c0 * ny0 + p0 * nx0
    zero = Jet(arb(0))
    sx, sy = center(f"{source.source}[0,0]", zero)
    px = sx + aq(radius(source.source)) * nx0
    py = sy + aq(radius(source.source)) * ny0

    first_x, first_y = center(source.target_id, zero)
    first = collision(px, py, ux0, uy0, first_x, first_y, radius(source.target_id))
    first_p = first["momentum"]
    first_c_square = arb(1) - first_p * first_p
    first_c = first_c_square.sqrt()
    ux1 = first_c * first["normal_x"] - first_p * first["normal_y"]
    uy1 = first_c * first["normal_y"] + first_p * first["normal_x"]

    second_x, second_y = center(branch[1], zero)
    second = collision(
        first["hit_x"],
        first["hit_y"],
        ux1,
        uy1,
        second_x,
        second_y,
        radius(branch[1]),
    )
    second_p = second["momentum"]
    second_c_square = arb(1) - second_p * second_p
    second_c = second_c_square.sqrt()
    ux2 = second_c * second["normal_x"] - second_p * second["normal_y"]
    uy2 = second_c * second["normal_y"] + second_p * second["normal_x"]

    third_x, third_y = center(branch[2], zero)
    dx, dy = third_x - second["hit_x"], third_y - second["hit_y"]
    transverse = -uy2 * dx + ux2 * dy
    tangent_flight = ux2 * dx + uy2 * dy
    third_radius = aq(radius(branch[2]))
    equation = third_radius * third_radius - transverse * transverse
    projective_q = uy2 / (arb(1) + ux2)
    local_x, local_y = matrix_normal(matrix, (nx0, ny0))
    z = local_y / (1 + local_x)
    return {
        "equation": equation,
        "projective_q": projective_q,
        "local_x": local_x,
        "z": z,
        "source_cosine": c0,
        "source_momentum": p0,
        "source_normal_x": nx0,
        "source_normal_y": ny0,
        "source_velocity_x": ux0,
        "source_velocity_y": uy0,
        "source_point_x": px,
        "source_point_y": py,
        "first_hit_x": first["hit_x"],
        "first_hit_y": first["hit_y"],
        "first_discriminant": first["discriminant"],
        "second_discriminant": second["discriminant"],
        "first_incidence_square": first_c_square,
        "second_incidence_square": second_c_square,
        "first_flight": first["flight"],
        "second_flight": second["flight"],
        "third_tangent_flight": tangent_flight,
        "third_transverse": transverse,
        "outgoing2_x": ux2,
    }


def implicit_two_jet(values: dict[str, Jet]) -> dict[str, arb]:
    equation = values["equation"]
    error_first = -equation.gradient[0] / equation.gradient[1]
    error_second = -(
        equation.hessian[0][0]
        + 2 * equation.hessian[0][1] * error_first
        + equation.hessian[1][1] * error_first * error_first
    ) / equation.gradient[1]

    z = values["z"]
    z_first = z.gradient[0] + z.gradient[1] * error_first
    z_second = (
        z.hessian[0][0]
        + 2 * z.hessian[0][1] * error_first
        + z.hessian[1][1] * error_first * error_first
        + z.gradient[1] * error_second
    )
    theta_first = 2 * z_first / (1 + z.value * z.value)
    theta_second = (
        2 * z_second / (1 + z.value * z.value)
        - 4 * z.value * z_first * z_first / ((1 + z.value * z.value) ** 2)
    )
    momentum = values["source_momentum"]
    momentum_first = momentum.gradient[0] + momentum.gradient[1] * error_first
    momentum_second = (
        momentum.hessian[0][0]
        + 2 * momentum.hessian[0][1] * error_first
        + momentum.hessian[1][1] * error_first * error_first
        + momentum.gradient[1] * error_second
    )
    projective_q = values["projective_q"]
    projective_q_first = (
        projective_q.gradient[0] + projective_q.gradient[1] * error_first
    )
    projective_q_second = (
        projective_q.hessian[0][0]
        + 2 * projective_q.hessian[0][1] * error_first
        + projective_q.hessian[1][1] * error_first * error_first
        + projective_q.gradient[1] * error_second
    )
    return {
        "error_first": error_first,
        "error_second": error_second,
        "theta_c": theta_first,
        "theta_cc": theta_second,
        "momentum_c": momentum_first,
        "momentum_cc": momentum_second,
        "projective_q_c": projective_q_first,
        "projective_q_cc": projective_q_second,
    }


def correlated_implicit_jet(
    value: Jet, error_first: arb, error_second: arb
) -> Jet:
    """Compose a two-variable tube Jet with the unique implicit error graph."""

    first = value.gradient[0] + value.gradient[1] * error_first
    second = (
        value.hessian[0][0]
        + 2 * value.hessian[0][1] * error_first
        + value.hessian[1][1] * error_first * error_first
        + value.gradient[1] * error_second
    )
    zero = arb(0)
    return Jet(
        value.value,
        [first, zero, zero],
        [[second, zero, zero], [zero, zero, zero], [zero, zero, zero]],
    )


def validate_fixed_path(values: dict[str, Any], label: str) -> None:
    """Revalidate every signed branch guard, not just the final equation."""

    for key in ("line_radicand", "ray1_radicand", "ray0_radicand"):
        require(bool(values[key].value > 0), f"{key}:{label}")
    require(bool(values["line_incidence"].value > 0), f"line incidence:{label}")
    require(bool(values["ray1_incidence"].value < 0), f"ray1 incidence:{label}")
    require(bool(values["ray0_incidence"].value < 0), f"ray0 incidence:{label}")
    require(bool(values["flight1"].value > 0), f"flight1:{label}")
    require(bool(values["flight0"].value > 0), f"flight0:{label}")
    require(bool(values["tangent_flight"].value > 0), f"tangent flight:{label}")
    require(
        values["tangent_residual"].value.contains(0),
        f"tangent equation residual:{label}",
    )


def validate_root_fixed_path(
    values: dict[str, Any],
    source_cosine: Jet,
    c_lower: Q,
    label: str,
) -> None:
    """Endpoint-stratified path check for the closed root sheet."""

    for key in ("line_radicand", "ray1_radicand"):
        require(bool(values[key].value > 0), f"{key}:{label}")
    require(bool(values["line_incidence"].value > 0), f"line incidence:{label}")
    require(bool(values["ray1_incidence"].value < 0), f"ray1 incidence:{label}")
    require(bool(values["flight1"].value > 0), f"flight1:{label}")
    require(bool(values["flight0"].value > 0), f"flight0:{label}")
    require(bool(values["tangent_flight"].value > 0), f"tangent flight:{label}")
    require(
        values["tangent_residual"].value.contains(0),
        f"tangent equation residual:{label}",
    )

    # The source-circle leg is the distinguished grazing stratum.  Its exact
    # geometry gives incidence=-c0 and radicand=R_G^2*c0^2.  Thus both vanish
    # at c0=0, while every leaf with c_lower>0 has the normalized strict
    # margins 1 and R_G^2.  Interval residuals below are secondary sanity
    # checks, not the proof of the factorization.
    radius_squared = aq(SOURCE_RADIUS * SOURCE_RADIUS)
    require(
        (
            values["ray0_radicand"].value
            - radius_squared * source_cosine.value * source_cosine.value
        ).contains(0),
        f"source radicand factorization sanity:{label}",
    )
    require(
        (values["ray0_incidence"].value + source_cosine.value).contains(0),
        f"source incidence factorization sanity:{label}",
    )
    require(c_lower >= 0, f"root c lower:{label}")
    if c_lower > 0:
        require(SOURCE_RADIUS * SOURCE_RADIUS > 0, f"normalized radicand:{label}")


def mean_root_face(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    matrix: tuple[tuple[int, int], tuple[int, int]],
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    face: Q,
) -> arb:
    center_value = root_two_jet(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        c_center,
        c_center,
        face,
        face,
    )["equation"]
    full_value = root_two_jet(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        Q(0),
        EDGE_WIDTH,
        face,
        face,
    )["equation"]
    return center_value.value + full_value.gradient[0] * interval(
        -EDGE_WIDTH / 2, EDGE_WIDTH / 2
    )


def root_error_enclosure(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    matrix: tuple[tuple[int, int], tuple[int, int]],
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    c_lower: Q,
    c_upper: Q,
    full_values: dict[str, Jet],
) -> tuple[Q, Q]:
    """Mean-value enclosure for the unique affine-tube root error."""

    zero_values = root_two_jet(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        c_lower,
        c_upper,
        Q(0),
        Q(0),
    )
    enclosure = -zero_values["equation"].value / full_values["equation"].gradient[1]
    lower, upper = arb_pair(enclosure)
    lower = max(lower, -ROOT_TUBE_RADIUS)
    upper = min(upper, ROOT_TUBE_RADIUS)
    require(lower < upper, "nonempty implicit-root error enclosure")
    return lower, upper


def validate_projective_matrix(
    matrix: tuple[tuple[int, int], tuple[int, int]]
) -> None:
    rows = matrix
    require(sum(x * x for x in rows[0]) == 1, "projective matrix row 0 norm")
    require(sum(x * x for x in rows[1]) == 1, "projective matrix row 1 norm")
    require(sum(rows[0][i] * rows[1][i] for i in range(2)) == 0, "matrix rows")
    determinant = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
    require(abs(determinant) == 1, "projective matrix determinant")


def validate_theta_bounds(values: dict[str, Any], label: str) -> None:
    require(bool(values["local_x"].value > 0), f"projective hemisphere:{label}")
    require(bool(values["theta_c"] > aq(THETA_FIRST_LOWER)), f"theta_c:{label}")
    require(
        bool(abs(values["theta_cc"]) < aq(THETA_SECOND_UPPER)),
        f"theta_cc:{label}",
    )
    require(bool(aq(SOURCE_RADIUS) * values["theta_c"] > aq(M)), f"m:{label}")
    require(
        bool(aq(SOURCE_RADIUS) * abs(values["theta_cc"]) < aq(A)),
        f"A:{label}",
    )


def validate_momentum_bounds(
    cosine: arb,
    momentum: arb,
    momentum_sign: int,
    label: str,
) -> None:
    """Use the exact circle identity, never a residual-width predicate.

    The base construction consists only of unit circle normals and specular
    reflections, so the planar Lagrange identity gives ``c^2+p^2=1``
    algebraically.  The root construction writes
    ``p=sigma*sqrt(1-c^2)`` explicitly.  Once the signed momentum interval is
    separated from zero, exact differentiation therefore gives the following
    two formulae on both pieces, including the c=0 endpoint.
    """

    require(
        type(momentum_sign) is int and momentum_sign in (-1, 1),
        f"momentum sign literal:{label}",
    )
    require(
        bool(momentum_sign * momentum > aq(MOMENTUM_ABS_LOWER)),
        f"momentum sign/lower:{label}",
    )
    # The strict signed lower bound gives |p_cc|=1/|p|^3<51^3=132651
    # exactly; evaluating the dependency-prone interval quotient is not an
    # acceptance predicate.
    require(51**3 == MOMENTUM_SECOND_UPPER, f"analytic p_cc bound:{label}")
    require(
        SOURCE_ACCELERATION_UPPER + MOMENTUM_SECOND_UPPER
        == AMBIENT_MOMENTUM_ACCELERATION_UPPER
        < A,
        f"ambient acceleration:{label}",
    )


def validate_metric_bounds(values: dict[str, Any], momentum_sign: int, label: str) -> None:
    validate_theta_bounds(values, label)
    validate_momentum_bounds(
        values["cosine"].value,
        values["momentum"].value,
        momentum_sign,
        label,
    )
    require(bool(values["theta_c"] < aq(THETA_FIRST_UPPER)), f"theta_c upper:{label}")
    radial_second = aq(SOURCE_RADIUS) * values["theta_cc"]
    # r_c>m already bounds the norm of either ambient curve derivative.
    require(
        bool(aq(SOURCE_RADIUS) * values["theta_c"] > aq(M)),
        f"metric speed:{label}",
    )
    require(
        bool(abs(radial_second) < aq(SOURCE_ACCELERATION_UPPER)),
        f"radial acceleration:{label}",
    )
    # |gamma_cc| <= |r_cc|+|p_cc| < 10,932,651 < 11,000,000.
    require(
        SOURCE_ACCELERATION_UPPER + MOMENTUM_SECOND_UPPER
        == AMBIENT_MOMENTUM_ACCELERATION_UPPER
        < A,
        f"metric acceleration:{label}",
    )


def theta_value(values: dict[str, Any]) -> arb:
    """Principal value of the selected projective normal lift."""

    return 2 * values["z"].value.atan()


def source_chart_coordinate(
    normal0: tuple[Jet, Jet], chart_id: str
) -> Jet:
    side = chart_id.split(":")[1]
    return normal0[1] if side in ("E", "W") else normal0[0]


def source_chart_radial(normal0: tuple[Jet, Jet], chart_id: str) -> Jet:
    side = chart_id.split(":")[1]
    if side == "E":
        return normal0[0]
    if side == "W":
        return -normal0[0]
    if side == "N":
        return normal0[1]
    require(side == "S", f"unknown source chart:{chart_id}")
    return -normal0[1]


def replay_join(
    ray_index: int,
    source: Any,
    branch: tuple[Any, ...],
    q0: Q,
    direction: int,
    path: tuple[int, int, int],
    row: dict[str, Any],
    refinement_depth: int = JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
) -> dict[str, Any]:
    """Rebuild the correlated positive-c identity neighborhood."""

    require(
        type(refinement_depth) is int
        and JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH
        <= refinement_depth
        <= JOIN_REPLAY_MAX_REFINEMENT_DEPTH,
        f"join refinement depth:{ray_index}",
    )
    matrix = PROJECTIVE_MATRICES[ray_index]
    outer_lower, outer_upper = (
        qvalue(value, f"join outer:{ray_index}")
        for value in row["outer_parameter_enclosure"]
    )
    tail_lower = qvalue(
        row["pre_root_tail_parameter_interval"][0], f"join tail:{ray_index}"
    )
    require(outer_lower <= outer_upper < tail_lower, f"join anchors:{ray_index}")
    error_radius = qvalue(row["affine_error_radius"], f"join error radius:{ray_index}")
    t_reference = qvalue(row["affine_t_reference"], f"join t reference:{ray_index}")
    affine_slope = qvalue(row["affine_slope"], f"join affine slope:{ray_index}")
    c_center = qvalue(row["affine_center_c0"], f"join c center:{ray_index}")
    root_source = replace(source, chart_id=row["source_chart"])
    c_overlap_lower, c_overlap_upper = EDGE_WIDTH / 2, EDGE_WIDTH
    c_width = c_overlap_upper - c_overlap_lower
    maximum_state_residual = Q(0)
    maximum_equation_residual = Q(0)
    maximum_tangent_side_residual = Q(0)
    maximum_error_width = Q(0)
    minimum_root_fe: Q | None = None
    minimum_q_second: Q | None = None
    minimum_first_discriminant: Q | None = None
    minimum_second_discriminant: Q | None = None
    minimum_first_flight: Q | None = None
    minimum_second_flight: Q | None = None
    minimum_tangent_flight: Q | None = None
    minimum_projective_q_denominator: Q | None = None
    minimum_signed_tangent_side: Q | None = None
    evidence: list[int] = []
    refinement_factor = 1 << refinement_depth
    replay_partition = JOIN_PARTITION * refinement_factor
    for refined_index in range(replay_partition):
        c_lower = c_overlap_lower + c_width * Q(refined_index, replay_partition)
        c_upper = c_overlap_lower + c_width * Q(
            refined_index + 1, replay_partition
        )
        full_values = root_two_jet(
            root_source,
            branch,
            row["source_grazing_sign_sigma0"],
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            -error_radius,
            error_radius,
        )
        error_lower, error_upper = root_error_enclosure(
            root_source,
            branch,
            row["source_grazing_sign_sigma0"],
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            full_values,
        )
        maximum_error_width = max(maximum_error_width, error_upper - error_lower)
        values = root_two_jet(
            root_source,
            branch,
            row["source_grazing_sign_sigma0"],
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        implicit = implicit_two_jet(values)
        label = f"join:{ray_index}:{refined_index}/{replay_partition}"
        fe_sign = row["parameterized_root_tube_equation_error_derivative_sign"]
        require(
            bool(fe_sign * values["equation"].gradient[1] > aq(Q(7))),
            f"join F_e:{label}",
        )
        root_fe_lower = arb_pair(
            fe_sign * values["equation"].gradient[1]
        )[0]
        minimum_root_fe = (
            root_fe_lower
            if minimum_root_fe is None
            else min(minimum_root_fe, root_fe_lower)
        )
        q_second_sign = row["q_second_derivative_sign"]
        require(
            bool(q_second_sign * implicit["projective_q_cc"] > aq(Q(1, 1000))),
            f"join q_second:{label}",
        )
        q_second_lower = arb_pair(
            q_second_sign * implicit["projective_q_cc"]
        )[0]
        minimum_q_second = (
            q_second_lower
            if minimum_q_second is None
            else min(minimum_q_second, q_second_lower)
        )
        reverse = reverse_q_prefix(
            source, branch, values["projective_q"], path
        )
        for residual in (
            reverse["hit1"][0].value - values["first_hit_x"].value,
            reverse["hit1"][1].value - values["first_hit_y"].value,
            reverse["reverse0"][0].value + values["source_velocity_x"].value,
            reverse["reverse0"][1].value + values["source_velocity_y"].value,
        ):
            maximum_state_residual = max(
                maximum_state_residual, abs_upper_q(residual)
            )
        source_delta = sub(
            (values["source_point_x"], values["source_point_y"]),
            reverse["hit1"],
        )
        require(
            cross(reverse["reverse0"], source_delta).value.contains(0),
            f"join source collinearity:{label}",
        )
        require(
            bool(dot(reverse["reverse0"], source_delta).value > 0),
            f"join source reverse flight:{label}",
        )
        require(c_lower > 0, f"join positive root c:{label}")
        require(values["equation"].value.contains(0), f"join F residual:{label}")
        projective_q_denominator = arb(1) + values["outgoing2_x"].value
        require(
            bool(projective_q_denominator > 0),
            f"join stereographic denominator:{label}",
        )
        denominator_lower = arb_pair(projective_q_denominator)[0]
        minimum_projective_q_denominator = (
            denominator_lower
            if minimum_projective_q_denominator is None
            else min(minimum_projective_q_denominator, denominator_lower)
        )
        signed_tangent_residual = (
            values["third_transverse"].value
            - aq(Q(branch[3]) * radius(branch[2]))
        )
        signed_tangent_side = branch[3] * values["third_transverse"].value
        require(
            signed_tangent_residual.contains(0)
            and bool(
                signed_tangent_side
                > aq(radius(branch[2]) / 2)
            ),
            f"join signed tangent side:{label}",
        )
        signed_tangent_lower = arb_pair(signed_tangent_side)[0]
        minimum_signed_tangent_side = (
            signed_tangent_lower
            if minimum_signed_tangent_side is None
            else min(minimum_signed_tangent_side, signed_tangent_lower)
        )
        maximum_tangent_side_residual = max(
            maximum_tangent_side_residual,
            abs_upper_q(signed_tangent_residual),
        )
        for key, minimum_name in (
            ("first_discriminant", "first_discriminant"),
            ("second_discriminant", "second_discriminant"),
            ("first_flight", "first_flight"),
            ("second_flight", "second_flight"),
            ("third_tangent_flight", "third_tangent_flight"),
        ):
            lower = arb_pair(values[key].value)[0]
            require(lower > 0, f"join positive lower {minimum_name}:{label}")
            if key == "first_discriminant":
                minimum_first_discriminant = (
                    lower
                    if minimum_first_discriminant is None
                    else min(minimum_first_discriminant, lower)
                )
            elif key == "second_discriminant":
                minimum_second_discriminant = (
                    lower
                    if minimum_second_discriminant is None
                    else min(minimum_second_discriminant, lower)
                )
            elif key == "first_flight":
                minimum_first_flight = (
                    lower
                    if minimum_first_flight is None
                    else min(minimum_first_flight, lower)
                )
            elif key == "second_flight":
                minimum_second_flight = (
                    lower
                    if minimum_second_flight is None
                    else min(minimum_second_flight, lower)
                )
            else:
                minimum_tangent_flight = (
                    lower
                    if minimum_tangent_flight is None
                    else min(minimum_tangent_flight, lower)
                )
        maximum_equation_residual = max(
            maximum_equation_residual, abs_upper_q(values["equation"].value)
        )
        if refined_index % refinement_factor == refinement_factor - 1:
            evidence.append(refined_index // refinement_factor)
    require(
        all(
            value is not None
            for value in (
                minimum_root_fe,
                minimum_q_second,
                minimum_first_discriminant,
                minimum_second_discriminant,
                minimum_first_flight,
                minimum_second_flight,
                minimum_tangent_flight,
                minimum_projective_q_denominator,
                minimum_signed_tangent_side,
            )
        ),
        f"join replay minima:{ray_index}",
    )
    require(
        row["q_second_derivative_sign"] == -direction,
        f"join oriented q curvature:{ray_index}",
    )
    derived_q_prime_lower = EDGE_WIDTH / 2 * Q(1, 1000)
    anchor_c = EDGE_WIDTH / 2
    anchor_full = root_two_jet(
        root_source,
        branch,
        row["source_grazing_sign_sigma0"],
        matrix,
        t_reference,
        affine_slope,
        c_center,
        anchor_c,
        anchor_c,
        -error_radius,
        error_radius,
    )
    anchor_error_lower, anchor_error_upper = root_error_enclosure(
        root_source,
        branch,
        row["source_grazing_sign_sigma0"],
        matrix,
        t_reference,
        affine_slope,
        c_center,
        anchor_c,
        anchor_c,
        anchor_full,
    )
    anchor_values = root_two_jet(
        root_source,
        branch,
        row["source_grazing_sign_sigma0"],
        matrix,
        t_reference,
        affine_slope,
        c_center,
        anchor_c,
        anchor_c,
        anchor_error_lower,
        anchor_error_upper,
    )
    anchor_parameter = (
        anchor_values["projective_q"].value - aq(q0)
    ) / direction
    anchor_parameter_lower, anchor_parameter_upper = arb_pair(anchor_parameter)
    require(
        outer_upper < anchor_parameter_lower
        and anchor_parameter_upper < tail_lower,
        f"join strict interior anchor:{ray_index}",
    )
    return {
        "canonical_splice_root_coordinate": str(EDGE_WIDTH),
        "canonical_splice_parameter_enclosure": [str(outer_lower), str(outer_upper)],
        "base_metric_cover_parameter_upper": str(outer_upper),
        "anchor_interval": [str(outer_upper), str(tail_lower)],
        "identity_neighborhood": [str(c_overlap_lower), str(c_overlap_upper)],
        "strict_interior_anchor": [
            str(anchor_parameter_lower),
            str(anchor_parameter_upper),
        ],
        "partition_count": JOIN_PARTITION,
        "partition_sha256": digest(evidence),
        "refinement_depth": refinement_depth,
        "refinement_factor": refinement_factor,
        "refined_subinterval_count": replay_partition,
        "derived_q_prime_lower": derived_q_prime_lower,
        "root_fe_lower": minimum_root_fe,
        "q_second_lower": minimum_q_second,
        "first_discriminant_lower": minimum_first_discriminant,
        "second_discriminant_lower": minimum_second_discriminant,
        "first_flight_lower": minimum_first_flight,
        "second_flight_lower": minimum_second_flight,
        "tangent_flight_lower": minimum_tangent_flight,
        "projective_q_denominator_lower": minimum_projective_q_denominator,
        "signed_tangent_side_lower": minimum_signed_tangent_side,
        "maximum_error_width": maximum_error_width,
        "maximum_state_residual": maximum_state_residual,
        "maximum_equation_residual": maximum_equation_residual,
        "maximum_tangent_side_residual": maximum_tangent_side_residual,
        "physical_state_c2_join_certified": True,
    }


def replay_base_ray(
    ray_index: int,
    source: Any,
    branch: tuple[Any, ...],
    q0: Q,
    direction: int,
    cell_edge: Q,
    end: Q,
    momentum_sign: int,
    verification_precision_bits: int,
) -> dict[str, Any]:
    require(cell_edge < end, f"base interval:{ray_index}")
    matrix = PROJECTIVE_MATRICES[ray_index]
    validate_projective_matrix(matrix)
    ctx.prec = 768
    midpoint_q = q0 + direction * (cell_edge + end) / 2
    path = round95.discover_path(source, branch, midpoint_q)
    width = end - cell_edge

    def evaluate(cell: int, subcell: int, depth: int) -> dict[str, Any]:
        denominator = BASE_INITIAL_PARTITION * (1 << depth)
        lower_index = cell * (1 << depth) + subcell
        lower = cell_edge + width * Q(lower_index, denominator)
        upper = cell_edge + width * Q(lower_index + 1, denominator)
        qa, qb = q0 + direction * lower, q0 + direction * upper
        values = reverse_q_two_jet(source, branch, qa, qb, path, matrix)
        require(bool(values["cosine"].value > 0), "source cosine")
        require(bool(direction * values["cosine_q"] < 0), "oriented cosine")
        label = f"base:{ray_index}:{cell}:{subcell}/{depth}"
        validate_metric_bounds(values, momentum_sign, label)
        validate_fixed_path(values, label)
        return {"values": values, "lower": lower, "upper": upper}

    # Phase one exactly reproduces the producer's deterministic 768-bit
    # partition and digest without importing any Round119 implementation.
    pending = [(cell, 0, 0) for cell in range(BASE_INITIAL_PARTITION)]
    leaves: list[tuple[int, int, int]] = []
    failures: list[tuple[int, int, int, str]] = []
    while pending:
        cell, subcell, depth = pending.pop()
        try:
            evaluate(cell, subcell, depth)
            leaves.append((cell, subcell, depth))
        except Exception as exc:
            if depth >= BASE_MAX_SPLIT_DEPTH:
                failures.append(
                    (cell, subcell, depth, f"{type(exc).__name__}:{exc}")
                )
                continue
            pending.append((cell, 2 * subcell + 1, depth + 1))
            pending.append((cell, 2 * subcell, depth + 1))
    leaves.sort(key=lambda row: (row[0], Q(row[1], 1 << row[2]), row[2]))
    failures.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    require(not failures, f"base residual:{ray_index}:{failures[:1]}")

    # Phase two rechecks every accepted leaf at the stronger verifier
    # precision.  No new adaptive decisions are made in this phase.
    ctx.prec = verification_precision_bits
    theta_hull: arb | None = None
    interval_rows: list[tuple[Q, Q]] = []
    for cell, subcell, depth in leaves:
        checked = evaluate(cell, subcell, depth)
        theta = theta_value(checked["values"])
        theta_hull = theta if theta_hull is None else theta_hull.union(theta)
        interval_rows.append((checked["lower"], checked["upper"]))
    require(interval_rows and interval_rows[0][0] == cell_edge, f"base start:{ray_index}")
    require(interval_rows[-1][1] == end, f"base end:{ray_index}")
    require(
        all(left[1] == right[0] for left, right in zip(interval_rows, interval_rows[1:])),
        f"base leaf partition:{ray_index}",
    )

    # The two extended-curve endpoints differ by at least the source cosine at
    # the non-grazing endpoint.  This is a separate endpoint/endpoint check;
    # it is not inferred from the two-interior-point normal-map argument.
    endpoint_q = q0 + direction * cell_edge
    endpoint = reverse_q_two_jet(
        source, branch, endpoint_q, endpoint_q, path, matrix
    )
    validate_metric_bounds(endpoint, momentum_sign, f"base endpoint:{ray_index}")
    validate_fixed_path(endpoint, f"base endpoint:{ray_index}")
    require(
        bool(endpoint["cosine"].value > aq(2 * RHO)),
        f"double endpoint distance:{ray_index}",
    )
    require(theta_hull is not None, f"base theta hull:{ray_index}")
    return {
        "leaf_count": len(leaves),
        "maximum_depth": max(depth for _, _, depth in leaves),
        "leaf_rows_sha256": digest(leaves),
        "residual_count": len(failures),
        "path": path,
        "endpoint_distance_gt_2rho": True,
        "theta_hull": theta_hull,
    }


def replay_root_ray(
    ray_index: int,
    source: Any,
    branch: tuple[Any, ...],
    row: dict[str, Any],
    path: tuple[int, int, int],
) -> dict[str, Any]:
    matrix = PROJECTIVE_MATRICES[ray_index]
    require(path == (1, -1, -1), f"root fixed regular path:{ray_index}")
    source_sign = row["source_grazing_sign_sigma0"]
    require(source_sign in (-1, 1), f"source sign:{ray_index}")
    t_reference = qvalue(row["affine_t_reference"], "root t reference")
    affine_slope = qvalue(row["affine_slope"], "root affine slope")
    c_center = qvalue(row["affine_center_c0"], "root c center")
    require(c_center == EDGE_WIDTH / 2, f"root center:{ray_index}")
    require(
        qvalue(row["affine_error_radius"], "root error radius") == ROOT_TUBE_RADIUS,
        f"root radius:{ray_index}",
    )
    leaf_count = row["dyadic_leaf_count"]
    require(
        type(leaf_count) is int and leaf_count == EXPECTED_ROOT_LEAF_COUNTS[ray_index],
        f"root leaf count:{ray_index}",
    )

    tube = root_two_jet(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        Q(0),
        EDGE_WIDTH,
        -ROOT_TUBE_RADIUS,
        ROOT_TUBE_RADIUS,
    )
    equation_error_derivative = tube["equation"].gradient[1]
    derivative_sign = strict_sign(equation_error_derivative)
    lower_face = mean_root_face(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        -ROOT_TUBE_RADIUS,
    )
    upper_face = mean_root_face(
        source,
        branch,
        source_sign,
        matrix,
        t_reference,
        affine_slope,
        c_center,
        ROOT_TUBE_RADIUS,
    )
    require(derivative_sign != 0, f"root derivative sign:{ray_index}")
    require(bool(derivative_sign * equation_error_derivative > aq(Q(7))), "root F_e")
    require(strict_sign(lower_face) == -derivative_sign, f"root lower face:{ray_index}")
    require(strict_sign(upper_face) == derivative_sign, f"root upper face:{ray_index}")

    evidence: list[list[int]] = []
    theta_hull: arb | None = None
    for leaf_index in range(leaf_count):
        c_lower = EDGE_WIDTH * leaf_index / leaf_count
        c_upper = EDGE_WIDTH * (leaf_index + 1) / leaf_count
        full_values = root_two_jet(
            source,
            branch,
            source_sign,
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            -ROOT_TUBE_RADIUS,
            ROOT_TUBE_RADIUS,
        )
        error_lower, error_upper = root_error_enclosure(
            source,
            branch,
            source_sign,
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            full_values,
        )
        values = root_two_jet(
            source,
            branch,
            source_sign,
            matrix,
            t_reference,
            affine_slope,
            c_center,
            c_lower,
            c_upper,
            error_lower,
            error_upper,
        )
        implicit = implicit_two_jet(values)
        label = f"root:{ray_index}:{leaf_index}"
        metric_values = {
            "local_x": values["local_x"],
            "theta_c": implicit["theta_c"],
            "theta_cc": implicit["theta_cc"],
            "cosine": values["source_cosine"],
            "momentum": values["source_momentum"],
            "momentum_c": implicit["momentum_c"],
            "momentum_cc": implicit["momentum_cc"],
        }
        validate_metric_bounds(metric_values, source_sign, label)
        equation_error_sign = strict_sign(full_values["equation"].gradient[1])
        require(
            equation_error_sign
            == row["parameterized_root_tube_equation_error_derivative_sign"],
            f"root F_e sign:{label}",
        )
        require(
            bool(
                equation_error_sign * full_values["equation"].gradient[1]
                > aq(Q(7))
            ),
            f"root F_e margin:{label}",
        )
        q_second_sign = strict_sign(implicit["projective_q_cc"])
        require(
            q_second_sign == row["q_second_derivative_sign"],
            f"root q_cc sign:{label}",
        )
        require(
            bool(q_second_sign * implicit["projective_q_cc"] > aq(Q(1, 1000))),
            f"root q_cc margin:{label}",
        )
        for key in (
            "first_discriminant",
            "second_discriminant",
            "first_incidence_square",
            "second_incidence_square",
            "first_flight",
            "second_flight",
            "third_tangent_flight",
        ):
            require(bool(values[key].value > 0), f"root forward {key}:{label}")
        require(
            values["equation"].value.contains(0),
            f"root third tangency equation:{label}",
        )
        require(
            bool(arb(1) + values["outgoing2_x"].value > 0),
            f"root stereographic denominator:{label}",
        )
        signed_tangent_residual = (
            values["third_transverse"].value
            - aq(Q(branch[3]) * radius(branch[2]))
        )
        require(
            signed_tangent_residual.contains(0)
            and bool(branch[3] * values["third_transverse"].value > 0),
            f"root signed tangent side:{label}",
        )
        require(c_lower >= 0, f"root endpoint stratum:{label}")
        if c_lower > 0:
            require(
                SOURCE_RADIUS * SOURCE_RADIUS > 0,
                f"root source normalized radicand:{label}",
            )
        theta = theta_value(values)
        theta_hull = theta if theta_hull is None else theta_hull.union(theta)
        evidence.append([leaf_index, q_second_sign])
    require(theta_hull is not None, f"root theta hull:{ray_index}")
    return {
        "leaf_count": leaf_count,
        "leaf_power": row["dyadic_leaf_power"],
        "leaf_rows_sha256": digest(evidence),
        "residual_count": 0,
        "theta_hull": theta_hull,
    }


def exact_int(value: Any, expected: int, label: str) -> None:
    require(type(value) is int and value == expected, label)


def digest_string(value: Any, label: str) -> None:
    require(
        type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
        label,
    )


def validate_extrema(
    values: Any, label: str, *, whole: bool = False
) -> dict[str, Q]:
    expected = WHOLE_EXTREMA_KEYS if whole else EXTREMA_KEYS
    require(type(values) is dict and set(values) == expected, f"{label}:keys")
    parsed = {key: qvalue(value, f"{label}:{key}") for key, value in values.items()}
    require(parsed["theta_lower"] <= parsed["theta_upper"], f"{label}:theta order")
    require(parsed["theta_c_lower"] > THETA_FIRST_LOWER, f"{label}:theta_c lower")
    require(parsed["theta_c_upper"] < THETA_FIRST_UPPER, f"{label}:theta_c upper")
    require(parsed["theta_cc_abs_upper"] < THETA_SECOND_UPPER, f"{label}:theta_cc")
    require(parsed["momentum_abs_lower"] > MOMENTUM_ABS_LOWER, f"{label}:p lower")
    require(
        parsed["r_cc_abs_upper"] < SOURCE_ACCELERATION_UPPER,
        f"{label}:r_cc",
    )
    require(parsed["local_x_lower"] > 0, f"{label}:local_x")
    require(0 <= parsed["cosine_lower"] <= parsed["cosine_upper"], f"{label}:cosine")
    if whole:
        require(
            parsed["theta_span_upper_bound"] < PROJECTIVE_LIFT_ANGULAR_SPAN,
            f"{label}:theta span",
        )
    return parsed


def validate_path(path: Any, label: str) -> None:
    require(type(path) is list and len(path) == 3, f"{label}:shape")
    for entry, expected in zip(path, (1, -1, -1)):
        exact_int(entry, expected, f"{label}:entry")


def static_contract(document: dict[str, Any]) -> dict[str, Any]:
    require(set(document) == {"schema", "result", "result_sha256"}, "document keys")
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict and set(result) == RESULT_KEYS, "result keys")
    require(document["result_sha256"] == digest(result), "certificate result digest")
    require(type(result["trace_rows"]) is list, "trace rows type")
    require(result["trace_rows_sha256"] == digest(result["trace_rows"]), "trace digest")
    require(type(result["precision_bits"]) is int and result["precision_bits"] >= 768, "producer precision")

    for key, expected in {
        "input_repaired_source_grazing_trace_count": 8,
        "certified_whole_trace_c2_splice_count": 8,
        "certified_per_trace_ambient_extended_cosine_master_reach_count": 8,
        "certified_per_trace_ambient_extended_momentum_cylinder_reach_count": 8,
        "pinned_round115_corner_stationary_identity_replayed_count": 8,
        "pinned_round115_root_existence_uniqueness_contract_replayed_count": 8,
        "certified_periodic_copy_separation_count": 8,
        "cross_trace_union_reach_count": 0,
        "base_initial_partition_count_per_trace": BASE_INITIAL_PARTITION,
        "base_maximum_adaptive_depth": BASE_MAX_SPLIT_DEPTH,
        "root_total_dyadic_leaf_count": sum(EXPECTED_ROOT_LEAF_COUNTS),
        "bounded_phase_space_endpoint_inclusive_two_sided_collar_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "actual_standard_curve_child_count": 0,
        "canonical_curve_recut_instance_count": 0,
        "new_gate5_actual_child_field_count": 0,
        "gate5_block_count": 0,
    }.items():
        exact_int(result[key], expected, f"count:{key}")
    require(result["source_component"] == "G", "source component")
    require(qvalue(result["source_radius"], "source radius") == SOURCE_RADIUS, "source radius")
    require(
        result["arithmetic"]
        == "768-bit-or-higher directed Arb interval arithmetic; exact rationals for all acceptance thresholds and reach inequalities",
        "arithmetic",
    )

    ambient = result["ambient_models"]
    require(type(ambient) is dict and set(ambient) == AMBIENT_MODEL_KEYS, "ambient model keys")
    require(
        ambient
        == {
            "cosine_master": "S^1_(9/25) x R_c with metric dr^2+dc^2",
            "momentum_master": "S^1_(9/25) x R_p with metric dr^2+dp^2",
            "flattened_coordinate": "r=(9/25)*theta",
            "bounded_physical_phase_space": "S^1_(9/25) x [-1,1]_p",
        },
        "ambient model confusion",
    )
    threshold = result["threshold_contract"]
    require(type(threshold) is dict and set(threshold) == THRESHOLD_KEYS, "threshold keys")
    expected_thresholds = {
        "theta_c_strict_lower_bound": THETA_FIRST_LOWER,
        "theta_c_strict_upper_bound": THETA_FIRST_UPPER,
        "theta_cc_abs_strict_upper_bound": THETA_SECOND_UPPER,
        "momentum_abs_strict_lower_bound": MOMENTUM_ABS_LOWER,
        "momentum_cc_abs_strict_upper_bound": MOMENTUM_SECOND_UPPER,
        "r_cc_abs_strict_upper_bound": SOURCE_ACCELERATION_UPPER,
        "metric_speed_strict_lower_bound": M,
        "momentum_curve_acceleration_strict_upper_bound": A,
        "theta_span_strict_upper_bound": PROJECTIVE_LIFT_ANGULAR_SPAN,
        "reach_radius": RHO,
    }
    for key, expected in expected_thresholds.items():
        require(qvalue(threshold[key], f"threshold:{key}") == expected, f"threshold:{key}")
    require(
        result["unit_identity_geometric_proof"] == EXPECTED_UNIT_IDENTITY_GEOMETRIC_PROOF,
        "unit identity proof",
    )
    require(result["unit_identity_geometric_proof_certified"] is True, "unit identity flag")
    require(
        result["exact_unit_identity_and_analytic_momentum_derivative_contract"]
        == EXPECTED_EXACT_MOMENTUM_CONTRACT,
        "exact analytic momentum contract",
    )
    require(
        result["interval_dependency_residual_width_used_as_acceptance_predicate"]
        is False,
        "interval dependency residual promoted to acceptance predicate",
    )
    require(
        result["root_base_global_regularization"]
        == (
            "the second-order base metric block covers the complete Round115 outer q enclosure. "
            "The canonical splice is the unique implicit root point c*=1/16384 whose q value lies "
            "in that enclosure; outer_upper is only the base-cover bound, not an asserted physical "
            "point. A correlated fixed-path replay on c in [1/32768,1/16384] identifies the "
            "reverse and implicit formulae as one analytic state, so their first/second derivatives "
            "agree at c* while the root bounds cover the remainder"
        ),
        "global regularization proof",
    )

    theorem = result["reach_theorem"]
    require(type(theorem) is dict and set(theorem) == REACH_THEOREM_KEYS, "reach theorem keys")
    require(theorem["common_monotone_coordinate"] == "r=(9/25)*theta", "monotone coordinate")
    require(
        theorem["ambient_models_paid_by_this_common_lemma"]
        == [
            "extended/periodic cosine master (r,c)",
            "extended/periodic momentum cylinder (r,p)",
        ],
        "reach ambient models",
    )
    for key, expected in {
        "strict_r_derivative_lower_bound": M,
        "common_acceleration_upper_bound": A,
        "certified_radius": RHO,
        "double_minimizer_exact_margin_m2_minus_A_rho": ENDPOINT_TAYLOR_MARGIN,
        "normal_map_exact_margin_m2_minus_4A_rho": NORMAL_MAP_MARGIN,
        "normal_map_determinant_lower_bound": NORMAL_MAP_DETERMINANT_LOWER,
    }.items():
        require(qvalue(theorem[key], f"theorem:{key}") == expected, f"theorem:{key}")
    for key, expected in {
        "double_minimizer_proof": EXPECTED_DOUBLE_MINIMIZER_PROOF,
        "normal_map_injectivity_proof": EXPECTED_NORMAL_MAP_INJECTIVITY_PROOF,
        "periodic_copy_proof": EXPECTED_PERIODIC_COPY_PROOF,
    }.items():
        require(theorem[key] == expected, f"theorem proof:{key}")
    for key in (
        "compact_nearest_point_existence",
        "endpoint_cases_paid_inside_double_minimizer_argument",
        "periodic_cylinder_copy_separation_paid",
    ):
        require(theorem[key] is True, f"theorem flag:{key}")
    require(M * M - A * RHO == ENDPOINT_TAYLOR_MARGIN > 0, "endpoint exact margin")
    require(M * M - 4 * A * RHO == NORMAL_MAP_MARGIN > 0, "normal exact margin")
    require(M - A * RHO / M == NORMAL_MAP_DETERMINANT_LOWER > 0, "determinant exact margin")
    require(
        SOURCE_RADIUS * (6 - PROJECTIVE_LIFT_ANGULAR_SPAN)
        == PERIODIC_LIFT_CLEARANCE
        > 2 * RHO,
        "periodic exact allowance",
    )

    obstruction = result["physical_endpoint_obstruction"]
    require(
        obstruction
        == {
            "root_endpoint_source_cosine": "c=0",
            "root_endpoint_momentum": "p=sigma0=+1_or_-1",
            "distance_to_bounded_momentum_boundary": "1-|p|=0",
            "uniform_endpoint_inclusive_two_sided_physical_collar_impossible": True,
        },
        "physical endpoint obstruction",
    )
    require(result["strict_scope"] == EXPECTED_SCOPE, "scope")
    require(result["strict_nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims")
    require(result["physical_owner_whole_trace_atlas_installed"] is False, "physical owner")
    require(result["gate5_global_maturity"] == "10/18", "Gate5 maturity")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "CM2 verdict")
    require(
        type(result["gate5_child_field_counts"]) is dict
        and set(result["gate5_child_field_counts"]) == {f"F{i}" for i in range(1, 7)},
        "Gate5 field keys",
    )
    for field in (f"F{i}" for i in range(1, 7)):
        exact_int(result["gate5_child_field_counts"][field], 0, f"Gate5:{field}")
    require(result["upstream_and_helper_pins"] == EXPECTED_CERTIFICATE_PINS, "certificate pins")

    base_counts = result["base_accepted_leaf_counts"]
    base_depths = result["base_achieved_maximum_depths"]
    require(type(base_counts) is list and len(base_counts) == 8, "base count list")
    require(type(base_depths) is list and len(base_depths) == 8, "base depth list")
    for index, value in enumerate(base_counts):
        require(type(value) is int and value > 0, f"base count type:{index}")
    for index, value in enumerate(base_depths):
        require(type(value) is int and 0 <= value <= BASE_MAX_SPLIT_DEPTH, f"base depth type:{index}")
    require(
        type(result["base_total_accepted_leaf_count"]) is int
        and result["base_total_accepted_leaf_count"] == sum(base_counts),
        "base count total",
    )

    require(len(result["trace_rows"]) == 8, "trace row census")
    for ray_index, row in enumerate(result["trace_rows"]):
        label = f"trace:{ray_index}"
        require(type(row) is dict and set(row) == TRACE_KEYS, f"{label}:keys")
        exact_int(row["ray_index"], ray_index, f"{label}:index")
        require(row["source_component"] == "G", f"{label}:source")
        require(qvalue(row["source_radius"], f"{label}:radius") == SOURCE_RADIUS, f"{label}:radius")
        require(
            type(row["source_grazing_sign_sigma0"]) is int
            and row["source_grazing_sign_sigma0"] in (-1, 1),
            f"{label}:source sign",
        )
        require(
            type(row["branch_key"]) is list
            and len(row["branch_key"]) == 4
            and type(row["branch_key"][0]) is int
            and type(row["branch_key"][3]) is int
            and type(row["branch_key"][1]) is str
            and type(row["branch_key"][2]) is str,
            f"{label}:branch key",
        )
        matrix = row["local_normal_matrix"]
        require(matrix == [list(x) for x in PROJECTIVE_MATRICES[ray_index]], f"{label}:matrix")
        require(
            all(type(entry) is int for matrix_row in matrix for entry in matrix_row),
            f"{label}:matrix types",
        )
        validate_projective_matrix(tuple(tuple(x) for x in matrix))
        require(row["local_angular_lift"] == "theta=2*atan(local_y/(1+local_x))", f"{label}:lift")
        require(row["local_matrix_is_orthogonal"] is True, f"{label}:orthogonal")
        require(row["local_matrix_orientation_may_be_reflected"] is True, f"{label}:reflection")

        base = row["base_certificate"]
        require(type(base) is dict and set(base) == BASE_CERTIFICATE_KEYS, f"{label}:base keys")
        exact_int(base["initial_partition_count"], BASE_INITIAL_PARTITION, f"{label}:base initial")
        exact_int(base["maximum_adaptive_depth_allowed"], BASE_MAX_SPLIT_DEPTH, f"{label}:base max")
        exact_int(base["achieved_maximum_adaptive_depth"], base_depths[ray_index], f"{label}:base depth")
        exact_int(base["accepted_leaf_count"], base_counts[ray_index], f"{label}:base leaves")
        exact_int(base["failed_leaf_count"], 0, f"{label}:base residual")
        digest_string(base["accepted_leaf_partition_sha256"], f"{label}:base digest")
        validate_path(base["fixed_reverse_path"], f"{label}:base path")
        require(
            type(base["parameter_interval"]) is list
            and len(base["parameter_interval"]) == 2
            and qvalue(base["parameter_interval"][0], f"{label}:base lo")
            < qvalue(base["parameter_interval"][1], f"{label}:base hi"),
            f"{label}:base interval",
        )
        require(type(base["q_interval"]) is list and len(base["q_interval"]) == 2, f"{label}:q interval")
        for side, value in enumerate(base["q_interval"]):
            qvalue(value, f"{label}:q interval:{side}")
        require(qvalue(base["far_endpoint_source_cosine_lower_bound"], f"{label}:far c") > 2 * RHO, f"{label}:far endpoint")
        validate_extrema(base["extrema"], f"{label}:base extrema")
        margins = base["path_and_equation_margins"]
        require(type(margins) is dict and set(margins) == BASE_PATH_MARGIN_KEYS, f"{label}:base margins")
        for key, value in margins.items():
            parsed = qvalue(value, f"{label}:base margin:{key}")
            require(parsed >= 0 if "residual" in key else parsed > 0, f"{label}:base margin:{key}")

        root = row["root_certificate"]
        require(type(root) is dict and set(root) == ROOT_CERTIFICATE_KEYS, f"{label}:root keys")
        require(root["root_coordinate_interval"] == ["0", str(EDGE_WIDTH)], f"{label}:root interval")
        exact_int(root["dyadic_leaf_power"], EXPECTED_ROOT_LEAF_COUNTS[ray_index].bit_length() - 1, f"{label}:root power")
        exact_int(root["dyadic_leaf_count"], EXPECTED_ROOT_LEAF_COUNTS[ray_index], f"{label}:root leaves")
        exact_int(root["failed_leaf_count"], 0, f"{label}:root residual")
        digest_string(root["leaf_q_second_sign_sha256"], f"{label}:root digest")
        require(qvalue(root["equation_error_derivative_abs_lower_bound"], f"{label}:F_e") > 7, f"{label}:F_e")
        require(qvalue(root["q_second_derivative_abs_lower_bound"], f"{label}:q_cc") > Q(1, 1000), f"{label}:q_cc")
        require(root["exact_corner_identity"] == "q_prime(0)=0_BY_SOURCE_GRAZING_FLOW_SHIFT", f"{label}:corner")
        require(type(root["strict_positive_c_q_prime_sign"]) is int and root["strict_positive_c_q_prime_sign"] in (-1, 1), f"{label}:q sign")
        validate_path(
            root["fixed_regular_reverse_path_for_c0_positive"],
            f"{label}:root path",
        )
        require(
            root["source_reverse_radicand_exact_factorization"]
            == "(9/25)^2*c0^2",
            f"{label}:source radicand factorization",
        )
        require(
            root["source_reverse_incidence_exact_factorization"] == "-c0",
            f"{label}:source incidence factorization",
        )
        require(
            root["projective_q_prime_exact_endpoint_factorization"]
            == (
                "q_prime(c0)=c0*H(c0), with fixed nonzero H sign and |H|>1/1000 "
                "from the replayed q_second mean-value bound"
            ),
            f"{label}:q prime factorization",
        )
        require(
            root[
                "regular_open_root_source_radicand_and_incidence_strict_for_c0_positive"
            ]
            is True,
            f"{label}:open root strict",
        )
        require(
            root[
                "closed_root_downstream_radicands_incidences_and_three_flights_certified"
            ]
            is True,
            f"{label}:closed downstream path",
        )
        require(
            root["closed_root_source_grazing_quantity_falsely_claimed_strict"]
            is False,
            f"{label}:false endpoint strictness",
        )
        endpoint = root["endpoint_stratum"]
        require(
            type(endpoint) is dict and set(endpoint) == ENDPOINT_STRATUM_KEYS,
            f"{label}:endpoint keys",
        )
        require(
            endpoint
            == {
                "source_cosine": "0",
                "source_reverse_radicand": "0",
                "source_reverse_incidence": "0",
                "source_momentum": str(row["source_grazing_sign_sigma0"]),
                "projective_q_prime": "0",
                "kept_in_singularity_ledger": True,
                "counted_as_regular_collision_owner": False,
            },
            f"{label}:endpoint stratum",
        )
        root_margins = root["root_tube_forward_path_margins"]
        require(type(root_margins) is dict and set(root_margins) == ROOT_PATH_MARGIN_KEYS, f"{label}:root margins")
        for key, value in root_margins.items():
            parsed = qvalue(value, f"{label}:root margin:{key}")
            require(parsed >= 0 if "residual" in key else parsed > 0, f"{label}:root margin:{key}")
        validate_extrema(root["extrema"], f"{label}:root extrema")

        join = row["root_base_c2_splice_certificate"]
        require(type(join) is dict and set(join) == JOIN_CERTIFICATE_KEYS, f"{label}:join keys")
        require(
            join["join_mode"]
            == "EXACT_GEOMETRIC_INVOLUTION_PLUS_UNIQUE_IMPLICIT_ROOT",
            f"{label}:join mode",
        )
        require(
            join["canonical_splice_root_coordinate"] == str(EDGE_WIDTH),
            f"{label}:canonical root coordinate",
        )
        splice_enclosure = join[
            "canonical_splice_projective_parameter_enclosure"
        ]
        require(
            type(splice_enclosure) is list
            and len(splice_enclosure) == 2
            and qvalue(splice_enclosure[0], f"{label}:splice lo")
            <= qvalue(splice_enclosure[1], f"{label}:splice hi"),
            f"{label}:splice enclosure",
        )
        require(
            join["base_metric_cover_parameter_upper"] == splice_enclosure[1],
            f"{label}:base cover upper",
        )
        require(join["base_metric_cover_contains_splice_enclosure"] is True, f"{label}:splice cover")
        require(
            join["outer_upper_is_only_a_cover_bound_not_an_asserted_physical_point"]
            is True,
            f"{label}:outer bound semantics",
        )
        anchor_interval = join["additional_projective_path_anchor_interval"]
        require(
            type(anchor_interval) is list
            and len(anchor_interval) == 2
            and qvalue(anchor_interval[0], f"{label}:anchor lo")
            < qvalue(anchor_interval[1], f"{label}:anchor hi"),
            f"{label}:anchor interval",
        )
        require(
            qvalue(join["additional_projective_path_anchor_width"], f"{label}:anchor width")
            == qvalue(anchor_interval[1], f"{label}:anchor hi2")
            - qvalue(anchor_interval[0], f"{label}:anchor lo2"),
            f"{label}:anchor width",
        )
        strict_anchor = join["strict_interior_projective_anchor_at_c_edge_over_2"]
        require(
            type(strict_anchor) is list
            and len(strict_anchor) == 2
            and qvalue(anchor_interval[0], f"{label}:anchor domain lo")
            < qvalue(strict_anchor[0], f"{label}:strict anchor lo")
            <= qvalue(strict_anchor[1], f"{label}:strict anchor hi")
            < qvalue(anchor_interval[1], f"{label}:anchor domain hi"),
            f"{label}:strict anchor",
        )
        require(
            join["correlated_positive_c_identity_neighborhood"]
            == [str(EDGE_WIDTH / 2), str(EDGE_WIDTH)],
            f"{label}:identity neighborhood",
        )
        require(
            join["correlated_positive_c_identity_neighborhood_certified"] is True,
            f"{label}:identity neighborhood flag",
        )
        exact_int(join["correlated_partition_count"], JOIN_PARTITION, f"{label}:join count")
        digest_string(join["correlated_partition_sha256"], f"{label}:join digest")
        validate_path(join["fixed_reverse_path"], f"{label}:join path")
        require(
            qvalue(
                join["root_equation_error_derivative_abs_lower_bound"],
                f"{label}:join F_e",
            )
            > 7,
            f"{label}:join F_e",
        )
        require(
            qvalue(
                join["root_q_second_derivative_abs_lower_bound"],
                f"{label}:join q_cc",
            )
            > Q(1, 1000),
            f"{label}:join q_cc",
        )
        require(
            qvalue(
                join[
                    "derived_root_q_prime_abs_lower_bound_on_identity_neighborhood"
                ],
                f"{label}:join q_c",
            )
            == EDGE_WIDTH / 2 * Q(1, 1000),
            f"{label}:join q_c",
        )
        require(
            join["derived_q_prime_proof"]
            == (
                "q_prime(0)=0 exactly and signed q_second>1/1000 on [0,edge], "
                "so |q_prime(c)|>c/1000>=edge/2000 throughout [edge/2,edge]"
            ),
            f"{label}:derived q proof",
        )
        for key in (
            "first_discriminant_lower_bound",
            "second_discriminant_lower_bound",
            "source_to_first_flight_lower_bound",
            "first_to_second_flight_lower_bound",
            "second_to_tangent_flight_lower_bound",
            "projective_q_denominator_lower_bound",
            "signed_tangent_side_lower_bound",
        ):
            require(qvalue(join[key], f"{label}:join:{key}") > 0, f"{label}:join:{key}")
        require(
            0
            < qvalue(
                join["correlated_root_error_enclosure_width_upper"],
                f"{label}:join error width",
            )
            <= 2 * ROOT_TUBE_RADIUS,
            f"{label}:join error width",
        )
        require(
            join["tangent_side_identity"]
            == "third_transverse=branch_sign*R3",
            f"{label}:tangent side identity",
        )
        require(
            qvalue(
                join["tangent_side_residual_abs_upper"],
                f"{label}:tangent side residual",
            )
            >= 0,
            f"{label}:tangent side residual",
        )
        require(
            join[
                "tangent_side_residual_width_used_as_acceptance_predicate"
            ]
            is False,
            f"{label}:tangent side residual predicate",
        )
        require(
            qvalue(
                join["low_level_equation_residual_abs_upper"],
                f"{label}:join equation residual",
            )
            >= 0,
            f"{label}:join equation residual",
        )
        require(
            join["raw_interval_state_composition_used_as_acceptance_predicate"]
            is False,
            f"{label}:raw state predicate",
        )
        require(
            join["raw_whole_q_image_minmax_used_as_acceptance_predicate"]
            is False,
            f"{label}:raw q predicate",
        )
        for key, expected in EXPECTED_JOIN_PROOFS.items():
            require(join[key] == expected, f"{label}:join proof:{key}")
        require(join["physical_state_c2_join_certified"] is True, f"{label}:join flag")

        validate_extrema(row["whole_trace_extrema"], f"{label}:whole extrema", whole=True)
        for key in (
            "whole_trace_theta_span_strictly_below_3_over_2",
            "periodic_source_cylinder_copy_separation_certified",
            "unit_identity_geometric_proof_certified",
            "analytic_momentum_derivatives_from_exact_identity_certified",
        ):
            require(row[key] is True, f"{label}:flag:{key}")
        require(row["cross_trace_union_reach_installed"] is False, f"{label}:union promotion")
        require(row["bounded_phase_space_two_sided_endpoint_collar_installed"] is False, f"{label}:physical collar")
        require(
            qvalue(
                row["ambient_extended_cosine_master_self_reach"],
                f"{label}:c reach",
            )
            == RHO,
            f"{label}:c reach",
        )
        require(
            qvalue(
                row["ambient_extended_momentum_cylinder_self_reach"],
                f"{label}:p reach",
            )
            == RHO,
            f"{label}:p reach",
        )

    require(
        result["base_total_accepted_leaf_count"]
        == sum(row["base_certificate"]["accepted_leaf_count"] for row in result["trace_rows"]),
        "base row total",
    )
    return result


def load_upstream() -> dict[str, dict[str, Any]]:
    documents = {}
    for path in (ROUND87, ROUND99, ROUND111, ROUND115, ROUND118):
        documents[path.name] = load_closed(
            path, UPSTREAM_SCHEMAS[path.name], UPSTREAM_PINS[path.name]
        )["result"]
    for name, expected in UPSTREAM_PINS.items():
        if name in documents:
            continue
        require(sha256(HERE / name) == expected, f"helper pin:{name}")
    return documents


def replay_join_quantitative_bounds(
    join: dict[str, Any],
) -> tuple[dict[str, Q], dict[str, Q]]:
    return (
        {
            saved_key: join[replayed_key]
            for saved_key, replayed_key in JOIN_LOWER_REPLAY_FIELDS.items()
        },
        {
            saved_key: join[replayed_key]
            for saved_key, replayed_key in JOIN_UPPER_REPLAY_FIELDS.items()
        },
    )


def validate_saved_join_dominance(
    saved_join: dict[str, Any],
    independent_lower_bounds: dict[str, Q],
    independent_upper_bounds: dict[str, Q],
    ray_index: int,
) -> None:
    require(
        set(independent_lower_bounds) == set(JOIN_LOWER_REPLAY_FIELDS),
        f"join lower evidence keys:{ray_index}",
    )
    require(
        set(independent_upper_bounds) == set(JOIN_UPPER_REPLAY_FIELDS),
        f"join upper evidence keys:{ray_index}",
    )
    for saved_key, independent_lower in independent_lower_bounds.items():
        require(
            qvalue(
                saved_join[saved_key],
                f"saved join lower:{ray_index}:{saved_key}",
            )
            <= independent_lower,
            f"join lower-bound replay:{ray_index}:{saved_key}",
        )
    for saved_key, independent_upper in independent_upper_bounds.items():
        require(
            qvalue(
                saved_join[saved_key],
                f"saved join upper:{ray_index}:{saved_key}",
            )
            >= independent_upper,
            f"join upper-bound replay:{ray_index}:{saved_key}",
        )


def mathematical_replay(
    result: dict[str, Any],
    verification_precision_bits: int,
    ray_indices: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    selected = tuple(range(8)) if ray_indices is None else ray_indices
    require(
        type(selected) is tuple
        and selected
        and all(type(ray_index) is int and 0 <= ray_index < 8 for ray_index in selected)
        and len(set(selected)) == len(selected),
        "replay ray selection",
    )
    selected_set = set(selected)
    upstream = load_upstream()
    round87 = upstream[ROUND87.name]
    round99 = upstream[ROUND99.name]
    round111 = upstream[ROUND111.name]
    round115 = upstream[ROUND115.name]
    round118 = upstream[ROUND118.name]
    correction_rows = sorted(round111["ray_correction_rows"], key=lambda row: row["ray_index"])
    root_rows = {
        row["ray_index"]: row
        for row in round115["root_edge_rows"]
    }
    repaired_rows = {
        row["ray_index"]: row for row in round118["repaired_endpoint_rows"]
    }
    require(
        len(correction_rows) == len(root_rows) == len(repaired_rows) == 8,
        "upstream ray census",
    )
    by_port = {row["registered_port_id"]: row for row in round87["port_event_rows"]}
    physical = {
        port_id: by_port[port_id]
        for port_id in round99["corrected_locally_physical_registered_port_ids"]
    }
    cores = core_cert.physical_cores()

    base_total = 0
    root_total = 0
    replay_rows: list[dict[str, Any]] = []
    for frozen, saved in zip(correction_rows, result["trace_rows"]):
        ray_index = frozen["ray_index"]
        if ray_index not in selected_set:
            continue
        require(ray_index == saved["ray_index"], f"ray join:{ray_index}")
        branch = tuple(frozen["branch_key"])
        port_id = frozen["exterior_port_id"]
        require(saved["branch_key"] == list(branch), f"branch join:{ray_index}")
        require(saved["exterior_port_id"] == port_id, f"port join:{ray_index}")
        require(saved["projective_end"] == frozen["projective_end"], f"end join:{ray_index}")
        require(
            saved["repaired_endpoint_id"]
            == repaired_rows[ray_index]["repaired_endpoint_id"],
            f"repaired endpoint join:{ray_index}",
        )
        q0, direction, cell_edge, _inner, _seam, *_ = round93.isolate_event(
            branch, frozen["projective_end"], port_id, physical, cores
        )
        root_row = root_rows[ray_index]
        require(root_row["branch_key"] == list(branch), f"root branch:{ray_index}")
        require(
            root_row["corner_stationary_identity"]
            == "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT",
            f"pinned root corner stationarity:{ray_index}",
        )
        require(
            root_row["corner_flow_shift_lemma"]
            == (
                "J(x,y)=(-y,x); v=c0*n+p0*J*n; n_t=epsilon*J*n/s; "
                "lambda=epsilon*sigma0*s; D(x,v)=(R0*v,0); "
                "downstream_Delta3_and_q_are_free-flight-shift-invariant"
            ),
            f"pinned flow-shift lemma:{ray_index}",
        )
        require(
            type(root_row["corner_flow_shift_lambda_sign"]) is int
            and root_row["corner_flow_shift_lambda_sign"] in (-1, 1),
            f"pinned flow-shift lambda sign:{ray_index}",
        )
        require(
            root_row["root_coordinate_interval"] == ["0", str(EDGE_WIDTH)]
            and root_row["q_prime_closed_interval_avoids_zero"] is False
            and root_row["affine_tube_inside_round112_t_box"] is True,
            f"pinned root tube domain:{ray_index}",
        )
        require(
            root_row["parameterized_root_tube_theorem"]
            == "UNIFORM_OPPOSITE_FACES_PLUS_FIXED_F_e_SIGN_GIVES_ONE_ROOT_FOR_EVERY_c0",
            f"pinned root existence/uniqueness theorem:{ray_index}",
        )
        stored_fe_sign = root_row[
            "parameterized_root_tube_equation_error_derivative_sign"
        ]
        require(
            type(stored_fe_sign) is int
            and stored_fe_sign in (-1, 1)
            and root_row["parameterized_root_tube_lower_face_sign"]
            == -stored_fe_sign
            and root_row["parameterized_root_tube_upper_face_sign"]
            == stored_fe_sign,
            f"pinned oriented root tube faces:{ray_index}",
        )
        require(
            qvalue(
                root_row["parameterized_root_tube_lower_face_abs_margin"],
                f"pinned root lower face:{ray_index}",
            )
            > 0
            and qvalue(
                root_row["parameterized_root_tube_upper_face_abs_margin"],
                f"pinned root upper face:{ray_index}",
            )
            > 0
            and qvalue(
                root_row[
                    "parameterized_root_tube_equation_error_derivative_abs_lower_bound"
                ],
                f"pinned root F_e:{ray_index}",
            )
            >= 7,
            f"pinned root tube margins:{ray_index}",
        )
        require(
            root_row["root_edge_q_injective"] is True
            and root_row["root_edge_to_base_chain_transition"]
            == "UNIQUE_MONOTONE_q_CROSSWALK_ON_ROUND114_OVERLAP"
            and root_row["root_edge_to_base_chain_transition_coordinate"]
            == "SAME_STEREOGRAPHIC_PROJECTIVE_q"
            and qvalue(
                root_row["root_edge_overlaps_certified_base_before_tail_margin"],
                f"pinned root/base overlap margin:{ray_index}",
            )
            > 0,
            f"pinned root/base uniqueness contract:{ray_index}",
        )
        outer = tuple(
            qvalue(value, f"root outer:{ray_index}")
            for value in root_row["outer_parameter_enclosure"]
        )
        tail_lower = qvalue(
            root_row["pre_root_tail_parameter_interval"][0],
            f"root tail lower:{ray_index}",
        )
        require(cell_edge < outer[0] < outer[1], f"base/root overlap order:{ray_index}")
        require(outer[1] < tail_lower, f"analytic join order:{ray_index}")
        saved_base = saved["base_certificate"]
        saved_root = saved["root_certificate"]
        saved_join = saved["root_base_c2_splice_certificate"]
        require(
            saved_base["parameter_interval"] == [str(cell_edge), str(outer[1])],
            f"base metric interval:{ray_index}",
        )
        require(
            saved_join["canonical_splice_root_coordinate"] == str(EDGE_WIDTH)
            and saved_join["canonical_splice_projective_parameter_enclosure"]
            == [str(outer[0]), str(outer[1])],
            f"canonical root splice:{ray_index}",
        )
        require(
            saved_join["base_metric_cover_parameter_upper"] == str(outer[1])
            and saved_join["base_metric_cover_contains_splice_enclosure"] is True
            and saved_join[
                "outer_upper_is_only_a_cover_bound_not_an_asserted_physical_point"
            ]
            is True,
            f"canonical metric cover:{ray_index}",
        )
        require(
            saved_join["additional_projective_path_anchor_interval"]
            == [str(outer[1]), str(tail_lower)]
            and saved_join["correlated_positive_c_identity_neighborhood"]
            == [str(EDGE_WIDTH / 2), str(EDGE_WIDTH)],
            f"analytic identity domain:{ray_index}",
        )
        source = cores[branch[0]]
        require(source.source == "G" and radius(source.source) == SOURCE_RADIUS, "source radius")
        base = replay_base_ray(
            ray_index,
            source,
            branch,
            q0,
            direction,
            cell_edge,
            outer[1],
            root_row["source_grazing_sign_sigma0"],
            verification_precision_bits,
        )
        root_source = replace(source, chart_id=root_row["source_chart"])
        root = replay_root_ray(ray_index, root_source, branch, root_row, base["path"])
        join: dict[str, Any] | None = None
        join_lower_bounds: dict[str, Q] = {}
        join_upper_bounds: dict[str, Q] = {}
        join_refinement_failures: list[str] = []
        for refinement_depth in range(
            JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
            JOIN_REPLAY_MAX_REFINEMENT_DEPTH + 1,
        ):
            try:
                candidate_join = replay_join(
                    ray_index,
                    source,
                    branch,
                    q0,
                    direction,
                    base["path"],
                    root_row,
                    refinement_depth=refinement_depth,
                )
                candidate_lower, candidate_upper = (
                    replay_join_quantitative_bounds(candidate_join)
                )
                validate_saved_join_dominance(
                    saved_join,
                    candidate_lower,
                    candidate_upper,
                    ray_index,
                )
            except RuntimeError as exc:
                join_refinement_failures.append(
                    f"depth={refinement_depth}:{type(exc).__name__}:{exc}"
                )
                continue
            join = candidate_join
            join_lower_bounds = candidate_lower
            join_upper_bounds = candidate_upper
            break
        require(
            join is not None,
            f"bounded join refinement exhausted:{ray_index}:"
            f"{join_refinement_failures}",
        )
        theta_hull = base["theta_hull"].union(root["theta_hull"])
        theta_span = theta_hull.upper() - theta_hull.lower()
        require(
            bool(theta_span < aq(PROJECTIVE_LIFT_ANGULAR_SPAN)),
            f"projective angular span:{ray_index}",
        )
        require(
            saved_base["accepted_leaf_count"] == base["leaf_count"],
            f"base leaf replay:{ray_index}",
        )
        require(
            saved_base["achieved_maximum_adaptive_depth"] == base["maximum_depth"],
            f"base depth replay:{ray_index}",
        )
        require(
            saved_base["accepted_leaf_partition_sha256"] == base["leaf_rows_sha256"],
            f"base digest replay:{ray_index}",
        )
        require(
            saved_root["dyadic_leaf_count"] == root["leaf_count"],
            f"root leaf replay:{ray_index}",
        )
        require(
            saved_root["dyadic_leaf_power"] == root["leaf_power"],
            f"root power replay:{ray_index}",
        )
        require(
            saved_root["leaf_q_second_sign_sha256"] == root["leaf_rows_sha256"],
            f"root digest replay:{ray_index}",
        )
        require(
            saved_join["correlated_partition_count"] == join["partition_count"]
            and saved_join["correlated_partition_sha256"]
            == join["partition_sha256"]
            and saved_join["canonical_splice_root_coordinate"]
            == join["canonical_splice_root_coordinate"]
            and saved_join["canonical_splice_projective_parameter_enclosure"]
            == join["canonical_splice_parameter_enclosure"]
            and saved_join["base_metric_cover_parameter_upper"]
            == join["base_metric_cover_parameter_upper"]
            and saved_join["additional_projective_path_anchor_interval"]
            == join["anchor_interval"]
            and saved_join["correlated_positive_c_identity_neighborhood"]
            == join["identity_neighborhood"]
            and qvalue(
                saved_join[
                    "derived_root_q_prime_abs_lower_bound_on_identity_neighborhood"
                ],
                f"saved join q prime:{ray_index}",
            )
            == join["derived_q_prime_lower"],
            f"join replay:{ray_index}",
        )
        saved_anchor = saved_join[
            "strict_interior_projective_anchor_at_c_edge_over_2"
        ]
        replayed_anchor = join["strict_interior_anchor"]
        saved_anchor_lower = qvalue(
            saved_anchor[0], f"saved anchor lo:{ray_index}"
        )
        saved_anchor_upper = qvalue(
            saved_anchor[1], f"saved anchor hi:{ray_index}"
        )
        replayed_anchor_lower = qvalue(
            replayed_anchor[0], f"replayed anchor lo:{ray_index}"
        )
        replayed_anchor_upper = qvalue(
            replayed_anchor[1], f"replayed anchor hi:{ray_index}"
        )
        require(
            max(saved_anchor_lower, replayed_anchor_lower)
            <= min(saved_anchor_upper, replayed_anchor_upper),
            f"join anchor enclosure overlap replay:{ray_index}",
        )
        validate_saved_join_dominance(
            saved_join,
            join_lower_bounds,
            join_upper_bounds,
            ray_index,
        )

        # The common endpoint/interior case for both ambient curves is paid by
        # the one-sided Taylor form of the double-minimizer lemma: r'>=m and
        # |gamma''|<=A force the same m^2-A*rho contradiction, without using
        # a sign assertion for the second ambient coordinate.
        require(
            M > 0 and ENDPOINT_TAYLOR_MARGIN > 0,
            f"endpoint Taylor lemma:{ray_index}",
        )
        require(
            NORMAL_MAP_DETERMINANT_LOWER > 0 and NORMAL_MAP_MARGIN > 0,
            f"normal strip lemma:{ray_index}",
        )

        # Distinct periodic lifts are separated even after two radius-rho
        # perturbations.  local_x>0 confines the selected projective lift to
        # one open semicircle.  Its complementary half-period is pi*R0;
        # pi>3 gives the exact rational allowance used here.
        require(
            PERIODIC_LIFT_CLEARANCE > 2 * RHO,
            f"periodic allowance:{ray_index}",
        )
        require(base["endpoint_distance_gt_2rho"], f"endpoint distance:{ray_index}")
        base_total += base["leaf_count"]
        root_total += root["leaf_count"]
        replay_rows.append(
            {
                "ray_index": ray_index,
                "base_leaf_count": base["leaf_count"],
                "base_leaf_partition_sha256": base["leaf_rows_sha256"],
                "root_leaf_count": root["leaf_count"],
                "root_leaf_sign_sha256": root["leaf_rows_sha256"],
                "join_partition_count": join["partition_count"],
                "join_partition_sha256": join["partition_sha256"],
                "join_replay_refinement_depth": join["refinement_depth"],
                "join_replay_refinement_factor": join["refinement_factor"],
                "join_replay_refined_subinterval_count": join[
                    "refined_subinterval_count"
                ],
                "join_replay_failed_refinement_count": len(
                    join_refinement_failures
                ),
                "join_independent_lower_bounds": {
                    key: str(value)
                    for key, value in sorted(join_lower_bounds.items())
                },
                "join_independent_upper_bounds": {
                    key: str(value)
                    for key, value in sorted(join_upper_bounds.items())
                },
            }
        )
    replay_rows.sort(key=lambda row: row["ray_index"])
    require(
        [row["ray_index"] for row in replay_rows] == sorted(selected),
        "replay row census",
    )
    expected_base_total = sum(
        result["trace_rows"][ray_index]["base_certificate"]["accepted_leaf_count"]
        for ray_index in selected
    )
    expected_root_total = sum(EXPECTED_ROOT_LEAF_COUNTS[ray_index] for ray_index in selected)
    require(base_total == expected_base_total, "base total")
    require(root_total == expected_root_total, "root total")
    return {
        "independently_replayed_base_leaf_count": base_total,
        "independently_replayed_root_leaf_count": root_total,
        "independently_replayed_trace_count": len(selected),
        "independently_rechecked_endpoint_interior_count": len(selected),
        "independently_rechecked_double_endpoint_count": len(selected),
        "independently_rechecked_periodic_lift_count": len(selected),
        "independently_rechecked_base_root_overlap_count": len(selected),
        "join_replay_total_refined_subinterval_count": sum(
            row["join_replay_refined_subinterval_count"] for row in replay_rows
        ),
        "join_replay_total_failed_refinement_count": sum(
            row["join_replay_failed_refinement_count"] for row in replay_rows
        ),
        "independently_replayed_trace_rows": replay_rows,
        "independently_replayed_trace_rows_sha256": digest(replay_rows),
    }


def isolated_trace_replay_worker(
    payload: tuple[dict[str, Any], int, int],
) -> dict[str, Any]:
    """Spawn-safe worker: one frozen certificate row, one private FLINT context."""

    result, verification_precision_bits, ray_index = payload
    require(
        type(verification_precision_bits) is int
        and verification_precision_bits >= 1024,
        "worker precision",
    )
    require(type(ray_index) is int and 0 <= ray_index < 8, "worker ray")
    ctx.prec = verification_precision_bits
    return mathematical_replay(
        result,
        verification_precision_bits,
        ray_indices=(ray_index,),
    )


def parallel_mathematical_replay(
    result: dict[str, Any],
    verification_precision_bits: int,
    workers: int,
) -> dict[str, Any]:
    """Run trace replays in spawn-isolated processes and merge deterministically."""

    require(type(workers) is int and 1 <= workers <= 8, "worker count")
    if workers == 1:
        return mathematical_replay(result, verification_precision_bits)

    import multiprocessing
    from concurrent.futures import ProcessPoolExecutor

    payloads = [
        (result, verification_precision_bits, ray_index)
        for ray_index in range(8)
    ]
    spawn_context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=spawn_context,
    ) as executor:
        partials = list(executor.map(isolated_trace_replay_worker, payloads))

    replay_rows = sorted(
        (
            row
            for partial in partials
            for row in partial["independently_replayed_trace_rows"]
        ),
        key=lambda row: row["ray_index"],
    )
    require(
        [row["ray_index"] for row in replay_rows] == list(range(8)),
        "parallel replay row census",
    )
    count_keys = (
        "independently_replayed_base_leaf_count",
        "independently_replayed_root_leaf_count",
        "independently_replayed_trace_count",
        "independently_rechecked_endpoint_interior_count",
        "independently_rechecked_double_endpoint_count",
        "independently_rechecked_periodic_lift_count",
        "independently_rechecked_base_root_overlap_count",
        "join_replay_total_refined_subinterval_count",
        "join_replay_total_failed_refinement_count",
    )
    combined = {
        key: sum(partial[key] for partial in partials)
        for key in count_keys
    }
    combined["independently_replayed_trace_rows"] = replay_rows
    combined["independently_replayed_trace_rows_sha256"] = digest(replay_rows)
    require(combined["independently_replayed_trace_count"] == 8, "parallel trace total")
    require(
        combined["independently_replayed_base_leaf_count"]
        == result["base_total_accepted_leaf_count"],
        "parallel base total",
    )
    require(
        combined["independently_replayed_root_leaf_count"]
        == sum(EXPECTED_ROOT_LEAF_COUNTS),
        "parallel root total",
    )
    return combined


def ray0_join_refinement_ladder(
    result: dict[str, Any],
    replay: dict[str, Any],
    verification_precision_bits: int,
) -> list[dict[str, Any]]:
    """Cache every permitted refinement depth for dynamic dominance attacks."""

    replay_row = next(
        row
        for row in replay["independently_replayed_trace_rows"]
        if row["ray_index"] == 0
    )
    require(
        replay_row["join_replay_refinement_depth"]
        == JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
        "ray0 selected refinement depth",
    )
    ladder = [
        {
            "refinement_depth": replay_row["join_replay_refinement_depth"],
            "refinement_factor": replay_row["join_replay_refinement_factor"],
            "refined_subinterval_count": replay_row[
                "join_replay_refined_subinterval_count"
            ],
            "independent_lower_bounds": replay_row[
                "join_independent_lower_bounds"
            ],
            "independent_upper_bounds": replay_row[
                "join_independent_upper_bounds"
            ],
        }
    ]

    ctx.prec = verification_precision_bits
    upstream = load_upstream()
    round87 = upstream[ROUND87.name]
    round99 = upstream[ROUND99.name]
    frozen = {
        row["ray_index"]: row
        for row in upstream[ROUND111.name]["ray_correction_rows"]
    }[0]
    root_row = {
        row["ray_index"]: row
        for row in upstream[ROUND115.name]["root_edge_rows"]
    }[0]
    by_port = {
        row["registered_port_id"]: row for row in round87["port_event_rows"]
    }
    physical = {
        port_id: by_port[port_id]
        for port_id in round99[
            "corrected_locally_physical_registered_port_ids"
        ]
    }
    cores = core_cert.physical_cores()
    branch = tuple(frozen["branch_key"])
    source = cores[branch[0]]
    q0, direction, cell_edge, _inner, _seam, *_ = round93.isolate_event(
        branch,
        frozen["projective_end"],
        frozen["exterior_port_id"],
        physical,
        cores,
    )
    outer_upper = qvalue(
        root_row["outer_parameter_enclosure"][1],
        "ray0 mutation ladder outer",
    )
    path = round95.discover_path(
        source,
        branch,
        q0 + direction * (cell_edge + outer_upper) / 2,
    )
    for refinement_depth in range(
        JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH + 1,
        JOIN_REPLAY_MAX_REFINEMENT_DEPTH + 1,
    ):
        join = replay_join(
            0,
            source,
            branch,
            q0,
            direction,
            path,
            root_row,
            refinement_depth=refinement_depth,
        )
        lower_bounds, upper_bounds = replay_join_quantitative_bounds(join)
        ladder.append(
            {
                "refinement_depth": refinement_depth,
                "refinement_factor": join["refinement_factor"],
                "refined_subinterval_count": join[
                    "refined_subinterval_count"
                ],
                "independent_lower_bounds": {
                    key: str(value)
                    for key, value in sorted(lower_bounds.items())
                },
                "independent_upper_bounds": {
                    key: str(value)
                    for key, value in sorted(upper_bounds.items())
                },
            }
        )
    require(
        [row["refinement_depth"] for row in ladder]
        == list(
            range(
                JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
                JOIN_REPLAY_MAX_REFINEMENT_DEPTH + 1,
            )
        ),
        "ray0 mutation refinement ladder",
    )
    return ladder


def resign(document: dict[str, Any]) -> None:
    result = document.get("result")
    if isinstance(result, dict) and isinstance(result.get("trace_rows"), list):
        result["trace_rows_sha256"] = digest(result["trace_rows"])
    if isinstance(result, dict):
        document["result_sha256"] = digest(result)


def set_nested(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def mutation_tests(document: dict[str, Any]) -> list[str]:
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        (
            "cosine_metric_confusion",
            ("result", "ambient_models", "cosine_master"),
            "bounded physical phase",
        ),
        (
            "reach_radius_inflation",
            ("result", "threshold_contract", "reach_radius"),
            "1/100",
        ),
        (
            "noncanonical_fraction_leading_zero",
            ("result", "threshold_contract", "reach_radius"),
            "01/2500000000",
        ),
        (
            "noncanonical_fraction_zero_numerator",
            ("result", "threshold_contract", "reach_radius"),
            "0/2",
        ),
        (
            "noncanonical_fraction_negative_denominator",
            ("result", "threshold_contract", "reach_radius"),
            "1/-2500000000",
        ),
        (
            "noncanonical_fraction_negative_zero",
            ("result", "threshold_contract", "reach_radius"),
            "-0",
        ),
        (
            "momentum_lower_reverted_to_false_one_over_fifty",
            ("result", "threshold_contract", "momentum_abs_strict_lower_bound"),
            "1/50",
        ),
        (
            "momentum_second_bound_forgery",
            ("result", "threshold_contract", "momentum_cc_abs_strict_upper_bound"),
            "1",
        ),
        (
            "common_acceleration_forgery",
            ("result", "reach_theorem", "common_acceleration_upper_bound"),
            "1",
        ),
        (
            "double_nearest_lemma_erasure",
            ("result", "reach_theorem", "double_minimizer_proof"),
            "interior points only",
        ),
        (
            "normal_map_proof_same_length_forgery",
            ("result", "reach_theorem", "normal_map_injectivity_proof"),
            "x" * len(EXPECTED_NORMAL_MAP_INJECTIVITY_PROOF),
        ),
        (
            "periodic_copy_proof_same_length_forgery",
            ("result", "reach_theorem", "periodic_copy_proof"),
            "x" * len(EXPECTED_PERIODIC_COPY_PROOF),
        ),
        (
            "unit_geometric_proof_erasure",
            ("result", "unit_identity_geometric_proof"),
            "interval residual only",
        ),
        (
            "analytic_pcc_formula_forgery",
            (
                "result",
                "exact_unit_identity_and_analytic_momentum_derivative_contract",
                "second_derivative_exact",
            ),
            "p_cc=-1/p^2",
        ),
        (
            "analytic_pc_formula_forgery",
            (
                "result",
                "exact_unit_identity_and_analytic_momentum_derivative_contract",
                "first_derivative_exact",
            ),
            "p_c=c/p",
        ),
        (
            "exact_unit_chain_same_length_forgery",
            (
                "result",
                "exact_unit_identity_and_analytic_momentum_derivative_contract",
                "unit_chain",
            ),
            "x" * len(EXPECTED_EXACT_MOMENTUM_CONTRACT["unit_chain"]),
        ),
        (
            "analytic_momentum_branch_lower_forgery",
            (
                "result",
                "exact_unit_identity_and_analytic_momentum_derivative_contract",
                "fixed_momentum_branch_abs_lower_bound",
            ),
            "1/50",
        ),
        (
            "analytic_derivatives_use_flag_erasure",
            (
                "result",
                "exact_unit_identity_and_analytic_momentum_derivative_contract",
                "analytic_derivatives_used_for_speed_and_acceleration_bounds",
            ),
            False,
        ),
        (
            "interval_residual_promoted_to_acceptance_predicate",
            (
                "result",
                "interval_dependency_residual_width_used_as_acceptance_predicate",
            ),
            True,
        ),
        (
            "trace_exact_analytic_derivative_flag_erasure",
            (
                "result",
                "trace_rows",
                0,
                "analytic_momentum_derivatives_from_exact_identity_certified",
            ),
            False,
        ),
        (
            "delete_base_leaf",
            ("result", "trace_rows", 0, "base_certificate", "accepted_leaf_count"),
            document["result"]["trace_rows"][0]["base_certificate"][
                "accepted_leaf_count"
            ]
            - 1,
        ),
        (
            "hide_base_residual",
            ("result", "trace_rows", 0, "base_certificate", "failed_leaf_count"),
            1,
        ),
        (
            "root_endpoint_falsely_strict",
            (
                "result",
                "trace_rows",
                0,
                "root_certificate",
                "closed_root_source_grazing_quantity_falsely_claimed_strict",
            ),
            True,
        ),
        (
            "root_endpoint_regular_owner_promotion",
            (
                "result",
                "trace_rows",
                0,
                "root_certificate",
                "endpoint_stratum",
                "counted_as_regular_collision_owner",
            ),
            True,
        ),
        (
            "canonical_splice_bound_as_fake_point",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "canonical_splice_root_coordinate",
            ),
            document["result"]["trace_rows"][0][
                "root_base_c2_splice_certificate"
            ]["base_metric_cover_parameter_upper"],
        ),
        (
            "canonical_outer_bound_semantics_erasure",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "outer_upper_is_only_a_cover_bound_not_an_asserted_physical_point",
            ),
            False,
        ),
        (
            "raw_state_composition_promoted_to_predicate",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "raw_interval_state_composition_used_as_acceptance_predicate",
            ),
            True,
        ),
        (
            "raw_q_minmax_promoted_to_predicate",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "raw_whole_q_image_minmax_used_as_acceptance_predicate",
            ),
            True,
        ),
        (
            "derived_qprime_bound_erasure",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "derived_root_q_prime_abs_lower_bound_on_identity_neighborhood",
            ),
            "0",
        ),
        (
            "projective_denominator_erasure",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "projective_q_denominator_lower_bound",
            ),
            "0",
        ),
        (
            "signed_tangent_side_identity_erasure",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "tangent_side_identity",
            ),
            "squared equation only",
        ),
        (
            "exact_join_identity_same_length_forgery",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "exact_identity_proof",
            ),
            "x" * len(EXPECTED_JOIN_PROOFS["exact_identity_proof"]),
        ),
        (
            "implicit_root_proof_same_length_forgery",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "unique_implicit_root_proof",
            ),
            "x" * len(EXPECTED_JOIN_PROOFS["unique_implicit_root_proof"]),
        ),
        (
            "c2_splice_proof_same_length_forgery",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "c2_splice_proof",
            ),
            "x" * len(EXPECTED_JOIN_PROOFS["c2_splice_proof"]),
        ),
        (
            "tangent_residual_promoted_to_predicate",
            (
                "result",
                "trace_rows",
                0,
                "root_base_c2_splice_certificate",
                "tangent_side_residual_width_used_as_acceptance_predicate",
            ),
            True,
        ),
        (
            "periodic_allowance_erasure",
            (
                "result",
                "trace_rows",
                0,
                "periodic_source_cylinder_copy_separation_certified",
            ),
            False,
        ),
        (
            "physical_endpoint_collar_promotion",
            (
                "result",
                "trace_rows",
                0,
                "bounded_phase_space_two_sided_endpoint_collar_installed",
            ),
            True,
        ),
        (
            "global_physical_collar_promotion",
            (
                "result",
                "bounded_phase_space_endpoint_inclusive_two_sided_collar_count",
            ),
            8,
        ),
        (
            "cross_trace_union_promotion",
            ("result", "trace_rows", 0, "cross_trace_union_reach_installed"),
            True,
        ),
        (
            "scope_promoted_to_twelve_faces",
            ("result", "strict_scope"),
            "twelve-face endpoint-inclusive physical collar theorem",
        ),
        ("precision_bool_substitution", ("result", "precision_bits"), True),
        (
            "root_existence_uniqueness_count_bool_substitution",
            (
                "result",
                "pinned_round115_root_existence_uniqueness_contract_replayed_count",
            ),
            True,
        ),
        (
            "zero_count_bool_substitution",
            ("result", "cross_trace_union_reach_count"),
            False,
        ),
        ("ray_index_bool_substitution", ("result", "trace_rows", 0, "ray_index"), False),
        (
            "leaf_depth_bool_substitution",
            (
                "result",
                "trace_rows",
                0,
                "base_certificate",
                "achieved_maximum_adaptive_depth",
            ),
            False,
        ),
        (
            "source_sign_bool_substitution",
            ("result", "trace_rows", 0, "source_grazing_sign_sigma0"),
            True,
        ),
        (
            "matrix_entry_bool_substitution",
            ("result", "trace_rows", 0, "local_normal_matrix", 0, 0),
            False,
        ),
        ("gate5_field_bool_substitution", ("result", "gate5_child_field_counts", "F1"), False),
        (
            "upstream_pin_mutation",
            (
                "result",
                "upstream_and_helper_pins",
                ROUND115.name,
            ),
            "0" * 64,
        ),
        ("gate5_promotion", ("result", "gate5_global_maturity"), "18/18"),
        ("other_singularity_promotion", ("result", "whole_trace_uniform_other_singularity_separation_count"), 8),
    ]
    rejected: list[str] = []
    for label, path, value in attacks:
        mutant = copy.deepcopy(document)
        try:
            set_nested(mutant, path, value)
            resign(mutant)
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"semantic mutation accepted:{label}")
    for label, location in (
        ("unknown_envelope_key", ()),
        ("unknown_result_key", ("result",)),
        ("unknown_trace_key", ("result", "trace_rows", 0)),
        (
            "unknown_base_certificate_key",
            ("result", "trace_rows", 0, "base_certificate"),
        ),
        (
            "unknown_root_certificate_key",
            ("result", "trace_rows", 0, "root_certificate"),
        ),
        (
            "unknown_join_certificate_key",
            ("result", "trace_rows", 0, "root_base_c2_splice_certificate"),
        ),
    ):
        mutant = copy.deepcopy(document)
        target: Any = mutant
        for key in location:
            target = target[key]
        target["hostile_unknown_key"] = True
        resign(mutant)
        try:
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(label)
        else:
            raise RuntimeError(f"unknown-key mutation accepted:{label}")
    return rejected


def replay_dominance_mutation_tests(
    document: dict[str, Any],
    replay: dict[str, Any],
    refinement_ladder: list[dict[str, Any]],
) -> list[str]:
    """Attack all measured join bounds through the full bounded search."""

    rows = replay["independently_replayed_trace_rows"]
    require(
        type(rows) is list
        and [row["ray_index"] for row in rows] == list(range(8)),
        "dynamic mutation replay rows",
    )
    require(
        type(refinement_ladder) is list
        and [
            row["refinement_depth"] for row in refinement_ladder
        ]
        == list(
            range(
                JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
                JOIN_REPLAY_MAX_REFINEMENT_DEPTH + 1,
            )
        ),
        "dynamic mutation refinement ladder",
    )
    parsed_ladder: list[tuple[int, dict[str, Q], dict[str, Q]]] = []
    for evidence in refinement_ladder:
        refinement_depth = evidence["refinement_depth"]
        require(
            evidence["refinement_factor"] == 1 << refinement_depth
            and evidence["refined_subinterval_count"]
            == JOIN_PARTITION * (1 << refinement_depth),
            f"dynamic mutation refinement metadata:{refinement_depth}",
        )
        independent_lower = {
            key: qvalue(
                value,
                f"dynamic lower evidence:{refinement_depth}:{key}",
            )
            for key, value in evidence["independent_lower_bounds"].items()
        }
        independent_upper = {
            key: qvalue(
                value,
                f"dynamic upper evidence:{refinement_depth}:{key}",
            )
            for key, value in evidence["independent_upper_bounds"].items()
        }
        require(
            set(independent_lower) == set(JOIN_LOWER_REPLAY_FIELDS)
            and set(independent_upper) == set(JOIN_UPPER_REPLAY_FIELDS),
            f"dynamic mutation evidence keys:{refinement_depth}",
        )
        parsed_ladder.append(
            (refinement_depth, independent_lower, independent_upper)
        )

    initial_lower = parsed_ladder[0][1]
    initial_upper = parsed_ladder[0][2]
    attacks: list[tuple[str, str, Q]] = []
    for key in initial_lower:
        forged = 2 * max(
            independent_lower[key]
            for _, independent_lower, _ in parsed_ladder
        )
        attacks.append((f"join_lower_inflation:{key}", key, forged))
    for key, bound in initial_upper.items():
        forged = (
            Q(0)
            if key
            in {
                "tangent_side_residual_abs_upper",
                "low_level_equation_residual_abs_upper",
            }
            else min(
                independent_upper[key]
                for _, _, independent_upper in parsed_ladder
            )
            / 2
        )
        attacks.append((f"join_upper_deflation:{key}", key, forged))

    rejected: list[str] = []
    for label, key, forged in attacks:
        mutant = copy.deepcopy(document)
        mutant_join = mutant["result"]["trace_rows"][0][
            "root_base_c2_splice_certificate"
        ]
        mutant_join[key] = str(forged)
        resign(mutant)
        try:
            static_contract(mutant)
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            raise RuntimeError(
                f"replay-dominance mutation was not isolated from static checks:"
                f"{label}:{exc}"
            ) from exc
        depth_failures: list[int] = []
        for refinement_depth, independent_lower, independent_upper in parsed_ladder:
            try:
                validate_saved_join_dominance(
                    mutant_join,
                    independent_lower,
                    independent_upper,
                    0,
                )
            except (KeyError, TypeError, ValueError, RuntimeError):
                depth_failures.append(refinement_depth)
            else:
                raise RuntimeError(
                    f"replay-dominance mutation accepted:{label}:"
                    f"depth={refinement_depth}"
                )
        require(
            depth_failures
            == list(
                range(
                    JOIN_REPLAY_INITIAL_REFINEMENT_DEPTH,
                    JOIN_REPLAY_MAX_REFINEMENT_DEPTH + 1,
                )
            ),
            f"replay-dominance mutation incomplete bounded search:{label}",
        )
        rejected.append(label)
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
            raise RuntimeError(f"strict JSON attack accepted:{label}")
    return rejected


def verify(
    certificate: Path = DEFAULT_CERTIFICATE,
    precision_bits: int = VERIFIER_PRECISION_BITS,
    workers: int = 1,
) -> dict[str, Any]:
    require(precision_bits >= 1024, "verifier precision below 1024 bits")
    require(type(workers) is int and 1 <= workers <= 8, "worker count")
    ctx.prec = precision_bits
    document = strict_json(certificate.read_text(encoding="utf-8"))
    result = static_contract(document)
    replay = parallel_mathematical_replay(result, precision_bits, workers)
    refinement_ladder = ray0_join_refinement_ladder(
        result,
        replay,
        precision_bits,
    )
    static_semantic_attacks = mutation_tests(document)
    replay_dominance_attacks = replay_dominance_mutation_tests(
        document,
        replay,
        refinement_ladder,
    )
    semantic_attacks = static_semantic_attacks + replay_dominance_attacks
    json_attacks = strict_json_tests()
    verification = {
        "verdict": "PASS",
        "verification_precision_bits": precision_bits,
        "round119_producer_module_imported": False,
        "shared_round119_mathematics_helper_imported": False,
        **replay,
        "normal_map_exact_margin": str(NORMAL_MAP_MARGIN),
        "endpoint_interior_exact_margin": str(ENDPOINT_TAYLOR_MARGIN),
        "normal_map_determinant_lower_bound": str(NORMAL_MAP_DETERMINANT_LOWER),
        "periodic_lift_clearance_lower_bound": str(PERIODIC_LIFT_CLEARANCE),
        "ambient_extended_cosine_master_self_reach_count": 8,
        "ambient_extended_momentum_cylinder_self_reach_count": 8,
        "bounded_phase_space_endpoint_inclusive_two_sided_collar_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "gate5_child_field_counts": {f"F{i}": 0 for i in range(1, 7)},
        "static_semantic_mutations_rejected": len(static_semantic_attacks),
        "static_semantic_mutation_labels": static_semantic_attacks,
        "replay_dominance_mutations_rejected": len(replay_dominance_attacks),
        "replay_dominance_mutation_labels": replay_dominance_attacks,
        "replay_dominance_refinement_depths_checked": [
            row["refinement_depth"] for row in refinement_ladder
        ],
        "replay_dominance_refinement_factors_checked": [
            row["refinement_factor"] for row in refinement_ladder
        ],
        "replay_dominance_refined_subinterval_counts_checked": [
            row["refined_subinterval_count"] for row in refinement_ladder
        ],
        "replay_dominance_total_refined_subinterval_count_checked": sum(
            row["refined_subinterval_count"] for row in refinement_ladder
        ),
        "semantic_mutations_rejected": len(semantic_attacks),
        "semantic_mutation_labels": semantic_attacks,
        "strict_json_attacks_rejected": len(json_attacks),
        "strict_json_attack_labels": json_attacks,
        "certificate_sha256": sha256(certificate),
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": digest(verification),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--precision-bits", type=int, default=VERIFIER_PRECISION_BITS)
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="spawn-isolated trace replay processes (1-8; does not alter results)",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(
        verify(args.certificate, args.precision_bits, args.workers),
        sort_keys=True,
        indent=2,
        ensure_ascii=True,
    ) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
