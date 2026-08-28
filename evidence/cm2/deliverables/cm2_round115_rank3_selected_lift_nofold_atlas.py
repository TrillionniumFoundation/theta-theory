#!/usr/bin/env python3
"""Certify the selected-lift no-fold atlas on the eight shared root edges.

Round114 proved only IVT coverage of the shared ``c3=b3=0`` edge.  This
producer adds the missing injectivity statement, but deliberately keeps it
separate from physical-owner, reach, and collar claims.

The corner is stationary in projective q: q'(0)=0.  That is an exact
source-grazing flow-shift identity, not a numerical nonzero derivative.  On
``c0>0`` we certify a uniform sign of ``q'(c0)/c0`` by enclosing the implicit
second derivative q'' on a correlated affine root tube.
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
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round114_rank3_seam_root_stitch_gap_atlas as round114
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND114 = HERE / "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json"
ROUND114_PRODUCER = HERE / "cm2_round114_rank3_seam_root_stitch_gap_atlas.py"
PINS = {
    ROUND114.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    ROUND114_PRODUCER.name: "47a231e32df2121058185a0fd82cbfb6c6105ace0d268a257103bc005b46ed02",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
}
SCHEMA = "cm2.round115.rank3-selected-lift-nofold-atlas.v1"
ROUND114_SCHEMA = "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1"
PRECISION_BITS = 640
EDGE_WIDTH = Q(1, 16384)
AFFINE_TUBE_RADIUS = Q(3, 100_000_000)
Q_SECOND_SIGN_MARGIN = Q(1, 1000)
T_FIRST_ABS_UPPER = Q(2)
T_SECOND_ABS_UPPER = Q(10)
Q_SECOND_ABS_UPPER = Q(10)
LEAF_POWERS = (9, 9, 9, 9, 9, 9, 11, 11)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_round114() -> dict[str, Any]:
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    document = json.loads(
        ROUND114.read_text(),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("open Round114 document")
    if document["schema"] != ROUND114_SCHEMA or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("Round114 closed-contract mismatch")
    result = document["result"]
    if (
        result["selected_lift_end_to_end_trace_coverage_count"] != 8
        or result["whole_trace_no_fold_atlas_count"] != 0
        or result["physical_owner_end_to_end_trace_closure_count"] != 0
    ):
        raise RuntimeError("Round114 scope mismatch")
    # This also checks every helper/upstream byte pin used by the inherited
    # root formulas.  Its return value is needed for the Round112 sheet map.
    round114.load_documents()
    return result


def arb_pair(value: arb) -> tuple[Q, Q]:
    return round114.arb_pair(value)


def positive_lower(value: arb, label: str) -> Q:
    if strict_sign(value) != 1:
        raise RuntimeError(f"non-strict {label}")
    lower, _ = arb_pair(value)
    if lower <= 0:
        raise RuntimeError(f"nonpositive directed lower bound: {label}")
    return lower


def abs_upper(value: arb) -> Q:
    lo, hi = arb_pair(value)
    return max(abs(lo), abs(hi))


def affine_edge_jet(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    c_lower: Q,
    c_upper: Q,
    e_lower: Q,
    e_upper: Q,
) -> dict[str, Jet]:
    """Evaluate the selected lift in correlated coordinates (c0,e).

    ``t=t_reference+affine_slope*(c0-c_center)+e``.  Indices 0 and 1 of
    the Jet are respectively c0 and e; index 2 is unused.
    """
    c0 = Jet.variable(interval(c_lower, c_upper), 0)
    error = Jet.variable(interval(e_lower, e_upper), 1)
    t = Jet(aq(t_reference)) + aq(affine_slope) * (c0 - aq(c_center)) + error
    zero = Jet(arb(0))
    source_normal_x, source_normal_y = normal(source.chart_id.split(":")[1], t)
    source_p = source_sign * (arb(1) - c0 * c0).sqrt()
    velocity_x = c0 * source_normal_x - source_p * source_normal_y
    velocity_y = c0 * source_normal_y + source_p * source_normal_x
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    point_x = source_x + aq(round112.radius(source.source)) * source_normal_x
    point_y = source_y + aq(round112.radius(source.source)) * source_normal_y

    first_x, first_y = center(source.target_id, zero)
    first = round112.collision_diagnostic(
        point_x, point_y, velocity_x, velocity_y,
        first_x, first_y, round112.radius(source.target_id),
    )
    first_momentum = first["momentum"]
    first_c = (arb(1) - first_momentum * first_momentum).sqrt()
    outgoing1_x = first_c * first["normal_x"] - first_momentum * first["normal_y"]
    outgoing1_y = first_c * first["normal_y"] + first_momentum * first["normal_x"]

    second_x, second_y = center(branch[1], zero)
    second = round112.collision_diagnostic(
        first["hit_x"], first["hit_y"], outgoing1_x, outgoing1_y,
        second_x, second_y, round112.radius(branch[1]),
    )
    second_momentum = second["momentum"]
    second_c = (arb(1) - second_momentum * second_momentum).sqrt()
    outgoing2_x = second_c * second["normal_x"] - second_momentum * second["normal_y"]
    outgoing2_y = second_c * second["normal_y"] + second_momentum * second["normal_x"]

    candidate_x, candidate_y = center(branch[2], zero)
    dx, dy = candidate_x - second["hit_x"], candidate_y - second["hit_y"]
    transverse = -outgoing2_y * dx + outgoing2_x * dy
    radius3 = aq(round112.radius(branch[2]))
    equation = radius3 * radius3 - transverse * transverse
    denominator = arb(1) + outgoing2_x
    projective_q = outgoing2_y / denominator
    return {
        "equation": equation,
        "projective_q": projective_q,
        "projective_q_denominator": denominator,
    }


def implicit_derivatives(values: dict[str, Jet]) -> dict[str, arb]:
    equation = values["equation"]
    projective_q = values["projective_q"]
    error_prime = -equation.gradient[0] / equation.gradient[1]
    error_second = -(
        equation.hessian[0][0]
        + 2 * equation.hessian[0][1] * error_prime
        + equation.hessian[1][1] * error_prime * error_prime
    ) / equation.gradient[1]
    q_prime = projective_q.gradient[0] + projective_q.gradient[1] * error_prime
    q_second = (
        projective_q.hessian[0][0]
        + 2 * projective_q.hessian[0][1] * error_prime
        + projective_q.hessian[1][1] * error_prime * error_prime
        + projective_q.gradient[1] * error_second
    )
    return {
        "error_prime": error_prime,
        "error_second": error_second,
        "q_prime": q_prime,
        "q_second": q_second,
    }


def mean_face(
    source: Any,
    branch: tuple[Any, ...],
    source_sign: int,
    t_reference: Q,
    affine_slope: Q,
    c_center: Q,
    face: Q,
) -> arb:
    point = affine_edge_jet(
        source, branch, source_sign, t_reference, affine_slope, c_center,
        c_center, c_center, face, face,
    )["equation"]
    box = affine_edge_jet(
        source, branch, source_sign, t_reference, affine_slope, c_center,
        Q(0), EDGE_WIDTH, face, face,
    )["equation"]
    half_width = EDGE_WIDTH / 2
    return point.value + box.gradient[0] * interval(-half_width, half_width)


def chart_orientation(chart: str) -> int:
    # Counterclockwise J(x,y)=(-y,x): n_t=epsilon*J*n/s.
    return 1 if chart in ("E", "S") else -1


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 512:
        raise RuntimeError("insufficient precision")
    ctx.prec = precision_bits
    inherited = load_round114()
    docs = round114.load_documents()
    cores = core_cert.physical_cores()
    sheet_groups: dict[str, dict[str, dict[str, Any]]] = {}
    for row in docs["r112"]["sheet_rows"]:
        sheet_groups.setdefault(row["exterior_port_id"], {})[row["sheet_kind"]] = row

    rows: list[dict[str, Any]] = []
    for stitched in sorted(inherited["root_edge_stitch_rows"], key=lambda row: row["ray_index"]):
        ray_index = stitched["ray_index"]
        port_id = stitched["exterior_port_id"]
        branch = tuple(stitched["branch_key"])
        hit = sheet_groups[port_id]["HIT"]
        source_sign = hit["source_grazing_sign_sigma0"]
        source = replace(cores[branch[0]], chart_id=hit["source_chart"])
        t_box = tuple(map(Q, hit["enclosing_parameter_box"]["t"]))
        c_center = EDGE_WIDTH / 2
        center_root = round114.isolate_edge_root(source, branch, source_sign, c_center, *t_box)
        t_reference = (center_root[0] + center_root[1]) / 2
        point = round114.edge_jet(
            source, branch, source_sign,
            center_root[0], center_root[1], c_center, c_center,
        )["equation"]
        slope_box = -point.gradient[1] / point.gradient[0]
        slope_lo, slope_hi = arb_pair(slope_box)
        affine_slope = (slope_lo + slope_hi) / 2

        affine_t_at_zero = t_reference - affine_slope * c_center
        affine_t_at_outer = t_reference + affine_slope * c_center
        affine_t_lower = min(affine_t_at_zero, affine_t_at_outer) - AFFINE_TUBE_RADIUS
        affine_t_upper = max(affine_t_at_zero, affine_t_at_outer) + AFFINE_TUBE_RADIUS
        if not (t_box[0] < affine_t_lower < affine_t_upper < t_box[1]):
            raise RuntimeError("affine root tube leaves Round112 box")

        tube = affine_edge_jet(
            source, branch, source_sign, t_reference, affine_slope, c_center,
            Q(0), EDGE_WIDTH, -AFFINE_TUBE_RADIUS, AFFINE_TUBE_RADIUS,
        )
        equation_error_derivative = tube["equation"].gradient[1]
        error_derivative_sign = strict_sign(equation_error_derivative)
        if error_derivative_sign == 0:
            raise RuntimeError("affine root tube loses unique graph")
        lower_face = mean_face(
            source, branch, source_sign, t_reference, affine_slope, c_center,
            -AFFINE_TUBE_RADIUS,
        )
        upper_face = mean_face(
            source, branch, source_sign, t_reference, affine_slope, c_center,
            AFFINE_TUBE_RADIUS,
        )
        lower_sign, upper_sign = strict_sign(lower_face), strict_sign(upper_face)
        if lower_sign != -error_derivative_sign or upper_sign != error_derivative_sign:
            raise RuntimeError("parameterised affine root-tube face inclusion")
        if not (
            bool(error_derivative_sign * equation_error_derivative > aq(Q(7)))
            and bool(lower_sign * lower_face > aq(Q(1, 1_000_000_000)))
            and bool(upper_sign * upper_face > aq(Q(1, 1_000_000_000)))
        ):
            raise RuntimeError("affine root-tube stored margin contract")

        power = LEAF_POWERS[ray_index]
        leaf_count = 1 << power
        q_second_sign: int | None = None
        q_second_margin = None
        max_t_first = Q(0)
        max_t_second = Q(0)
        max_q_second = Q(0)
        leaf_statuses: list[tuple[int, int]] = []
        for leaf_index in range(leaf_count):
            c_lower = EDGE_WIDTH * leaf_index / leaf_count
            c_upper = EDGE_WIDTH * (leaf_index + 1) / leaf_count
            leaf = affine_edge_jet(
                source, branch, source_sign, t_reference, affine_slope, c_center,
                c_lower, c_upper, -AFFINE_TUBE_RADIUS, AFFINE_TUBE_RADIUS,
            )
            derivatives = implicit_derivatives(leaf)
            sign = strict_sign(derivatives["q_second"])
            if sign == 0:
                raise RuntimeError(f"indeterminate q second derivative: ray {ray_index}, leaf {leaf_index}")
            if q_second_sign is None:
                q_second_sign = sign
            elif q_second_sign != sign:
                raise RuntimeError("q second derivative changes sign")
            signed_second = sign * derivatives["q_second"]
            if not bool(signed_second > aq(Q_SECOND_SIGN_MARGIN)):
                raise RuntimeError(f"q second derivative margin: ray {ray_index}, leaf {leaf_index}")
            margin = positive_lower(signed_second, "signed q second derivative")
            q_second_margin = margin if q_second_margin is None else min(q_second_margin, margin)
            t_first = aq(affine_slope) + derivatives["error_prime"]
            max_t_first = max(max_t_first, abs_upper(t_first))
            max_t_second = max(max_t_second, abs_upper(derivatives["error_second"]))
            max_q_second = max(max_q_second, abs_upper(derivatives["q_second"]))
            leaf_statuses.append((leaf_index, sign))
        if q_second_sign is None or q_second_margin is None:
            raise RuntimeError("empty q-second partition")
        if not (
            max_t_first < T_FIRST_ABS_UPPER
            and max_t_second < T_SECOND_ABS_UPPER
            and max_q_second < Q_SECOND_ABS_UPPER
        ):
            raise RuntimeError("C2 bound contract")

        projective_direction = 1 if stitched["projective_end"] == "RIGHT_PROJECTIVE_END" else -1
        if projective_direction * q_second_sign != -1:
            raise RuntimeError("root-edge/base-chain orientation mismatch")
        outer_parameter = tuple(map(Q, stitched["outer_parameter_enclosure"]))
        tail_parameter = tuple(map(Q, stitched["pre_root_tail_parameter_interval"]))
        corner_parameter = tuple(map(Q, stitched["corner_parameter_enclosure"]))
        if not (outer_parameter[1] < tail_parameter[0] < tail_parameter[1] < corner_parameter[0]):
            raise RuntimeError("unique root-edge/base-chain overlap order")
        epsilon = chart_orientation(source.chart_id.split(":")[1])
        structural_lambda_sign = epsilon * source_sign

        rows.append({
            "ray_index": ray_index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": stitched["projective_end"],
            "source_chart": source.chart_id,
            "source_grazing_sign_sigma0": source_sign,
            "source_chart_orientation_epsilon": epsilon,
            "root_coordinate_interval": ["0", str(EDGE_WIDTH)],
            "affine_center_c0": str(c_center),
            "affine_center_t_root_bracket": [str(center_root[0]), str(center_root[1])],
            "affine_t_reference": str(t_reference),
            "affine_slope": str(affine_slope),
            "affine_error_radius": str(AFFINE_TUBE_RADIUS),
            "affine_tube_inside_round112_t_box": True,
            "parameterized_root_tube_lower_face_sign": lower_sign,
            "parameterized_root_tube_upper_face_sign": upper_sign,
            "parameterized_root_tube_equation_error_derivative_sign": error_derivative_sign,
            "parameterized_root_tube_equation_error_derivative_abs_lower_bound": "7",
            "parameterized_root_tube_lower_face_abs_margin": "1/1000000000",
            "parameterized_root_tube_upper_face_abs_margin": "1/1000000000",
            "parameterized_root_tube_theorem": "UNIFORM_OPPOSITE_FACES_PLUS_FIXED_F_e_SIGN_GIVES_ONE_ROOT_FOR_EVERY_c0",
            "corner_flow_shift_lambda_sign": structural_lambda_sign,
            "corner_stationary_identity": "q_prime(0)=0_EXACT_BY_SOURCE_GRAZING_FLOW_SHIFT",
            "corner_flow_shift_lemma": "J(x,y)=(-y,x); v=c0*n+p0*J*n; n_t=epsilon*J*n/s; lambda=epsilon*sigma0*s; D(x,v)=(R0*v,0); downstream_Delta3_and_q_are_free-flight-shift-invariant",
            "q_second_derivative_formula": "q_cc+2*q_ce*e_prime+q_ee*e_prime^2+q_e*e_second",
            "implicit_error_first_formula": "e_prime=-F_c/F_e",
            "implicit_error_second_formula": "e_second=-(F_cc+2*F_ce*e_prime+F_ee*e_prime^2)/F_e",
            "dyadic_leaf_power": power,
            "dyadic_leaf_count": leaf_count,
            "dyadic_leaf_sign_digest": digest(leaf_statuses),
            "q_second_derivative_sign": q_second_sign,
            "q_second_derivative_abs_lower_bound": str(Q_SECOND_SIGN_MARGIN),
            "certified_uniform_q_prime_over_c0_abs_lower_bound": str(Q_SECOND_SIGN_MARGIN),
            "q_prime_sign_for_c0_positive": q_second_sign,
            "q_prime_closed_interval_avoids_zero": False,
            "projective_parameter_direction": projective_direction,
            "projective_parameter_derivative_sign_for_c0_positive": -1,
            "root_edge_q_injective": True,
            "root_edge_to_base_chain_transition": "UNIQUE_MONOTONE_q_CROSSWALK_ON_ROUND114_OVERLAP",
            "root_edge_to_base_chain_transition_coordinate": "SAME_STEREOGRAPHIC_PROJECTIVE_q",
            "root_edge_to_base_chain_stitch_parameter": stitched["pre_root_tail_parameter_interval"][0],
            "root_edge_overlaps_certified_base_before_tail_margin": str(tail_parameter[0] - outer_parameter[1]),
            "stereographic_q_denominator_lower_bound_inherited_from_round114": stitched["stereographic_q_denominator_lower_bound"],
            "pre_root_tail_parameter_interval": stitched["pre_root_tail_parameter_interval"],
            "outer_parameter_enclosure": stitched["outer_parameter_enclosure"],
            "corner_parameter_enclosure": stitched["corner_parameter_enclosure"],
            "root_graph_abs_dt_dc0_upper_bound": str(T_FIRST_ABS_UPPER),
            "root_graph_abs_d2t_dc0_2_upper_bound": str(T_SECOND_ABS_UPPER),
            "root_graph_parameter_plane_curvature_upper_bound": str(T_SECOND_ABS_UPPER),
            "root_q_abs_second_derivative_upper_bound": str(Q_SECOND_ABS_UPPER),
            "selected_lift_whole_trace_no_fold_atlas_installed": True,
            "physical_owner_atlas_installed": False,
            "positive_reach_installed": False,
            "uniform_other_singularity_separation_installed": False,
            "two_sided_physical_collar_installed": False,
        })

    if len(rows) != 8 or [row["ray_index"] for row in rows] != list(range(8)):
        raise RuntimeError("eight-ray no-fold accounting")
    result = {
        "precision_bits": precision_bits,
        "input_round114_selected_lift_trace_coverage_count": 8,
        "certified_affine_root_tube_count": 8,
        "certified_exact_stationary_corner_count": 8,
        "certified_root_edge_q_injective_count": 8,
        "certified_selected_lift_whole_trace_no_fold_atlas_count": 8,
        "physical_owner_whole_trace_no_fold_atlas_count": 0,
        "root_graph_c2_bound_count": 8,
        "whole_trace_positive_reach_certificate_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "whole_trace_two_sided_physical_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "new_gate5_actual_child_field_count": 0,
        "edge_width": str(EDGE_WIDTH),
        "affine_root_tube_radius": str(AFFINE_TUBE_RADIUS),
        "certified_q_second_and_q_prime_over_c0_margin": str(Q_SECOND_SIGN_MARGIN),
        "closed_interval_q_prime_nonvanishing_claim": False,
        "root_edge_rows": rows,
        "root_edge_rows_sha256": digest(rows),
        "strict_scope": "eight selected-lift shared grazing edges with parameterized affine root tubes, exact stationary corner flow-shift identities, strict q_prime/c0 signs, injective q crosswalks, and C2 root-graph bounds",
        "strict_nonclaims": [
            "q_prime equals zero at c0=0; only q_prime/c0 on c0>0 has a uniform strict sign",
            "selected-lift no-fold does not install first/second/third physical-owner ordering",
            "a C2 graph and injective q coordinate do not by themselves install positive normal reach for the whole physical trace",
            "no uniform distance to every other collision singularity, wall corner, flight cap, or representation seam is installed",
            "HIT and BYPASS remain separate real sheets sharing only c3=b3=0",
            "no two-sided physical collar, complete 57-candidate order, homogeneity child, official word, or Gate5 field is installed",
        ],
        "strict_separator": {
            "selected_lift_algebraic_trace_coverage": "8/8",
            "selected_lift_whole_trace_no_fold_atlas": "8/8",
            "physical_owner_trace_closure": "0/8",
            "whole_trace_positive_reach": "0/8",
            "whole_trace_two_sided_physical_collar": "0/8",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "upstream_and_helper_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
