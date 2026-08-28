#!/usr/bin/env python3
"""Round117 exact countable homogeneity operator-cell schema.

This append-only producer refines the 72 closed Round113 endpoint proof boxes
by the *exact* q=2 homogeneity partition

    H_n = (sin((n+1)^-2), sin(n^-2)],  n >= 128.

The small rational parameter square extends to 1/16384, which is strictly
larger than sin(128^-2).  The difference is retained as the central/outer H0
child; it is never silently discarded.  HIT sheets use the independent source
and actual-third cosine indices.  BYPASS sheets use the source index only: the
analytic b3 coordinate is not a collision angle, while the actual G-winner is
proved to lie in central H0 on every parent proof box.

The output is a countable two-dimensional operator-cell generator and its
actual parameter-region intersections.  It is deliberately not an actual
standard-curve recut and installs no Gate5 F1--F6 field.
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
import cm2_round113_rank3_root_sheet_owner_ordering_spike as round113
from cm2_round76_r2_numeric_fields_generator import aq
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
ROUND112_JSON = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND113_JSON = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND113_MANIFEST = HERE / "cm2-one-hundred-thirteenth-direct-assault-manifest-2026-07-23.sha256"
SCHEMA = "cm2.round117.rank3-countable-homogeneity-operator-cells.v1"
PRECISION_BITS = 512
BOUNDARY_PRECISION_BITS = 256
N0 = 128
OUTER = Q(1, 16384)
EVIDENCE_PADDING = Q(1, 10**6)
BOUNDARY_QUERY_INDICES = (128, 129, 255, 256, 1024, 10**6)
PINS = {
    ROUND112_JSON.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND113_JSON.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    ROUND113_MANIFEST.name: "245857f51b8da2fb1707cdfaa9d0cb2d76f13e2d03ddb3e53e415b5cdca69ac7",
    "cm2_round113_rank3_root_sheet_owner_ordering_spike.py": "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"non-object JSON dependency: {path.name}")
    return value


def validate_pins() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"direct dependency byte pin mismatch: {name}")


def exact_dyadic(point: arb) -> Q:
    """Convert an exact finite Arb point to an exact rational dyadic."""
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def homogeneity_boundary(index: int, precision_bits: int = BOUNDARY_PRECISION_BITS) -> dict[str, Any]:
    """Directed-rounded query for b_index = sin(index^-2)."""
    if not isinstance(index, int) or isinstance(index, bool) or index < N0:
        raise ValueError(f"homogeneity boundary index must be an integer >= {N0}")
    if precision_bits < 128:
        raise ValueError("boundary precision must be at least 128 bits")
    old_precision = ctx.prec
    try:
        ctx.prec = precision_bits
        angle = Q(1, index * index)
        value = (arb(1) / arb(index * index)).sin()
        lower = exact_dyadic(value.lower())
        upper = exact_dyadic(value.upper())
    finally:
        ctx.prec = old_precision
    if not (Q(0) < lower < upper < angle):
        raise RuntimeError("directed boundary enclosure or sin(x)<x failed")
    return {
        "index": index,
        "exact_angle_radians": str(angle),
        "directed_lower_rational": str(lower),
        "directed_upper_rational": str(upper),
        "precision_bits": precision_bits,
        "strictly_between_zero_and_exact_angle": True,
    }


def boundary_ball(index: int) -> arb:
    if index < N0:
        raise ValueError("boundary index")
    return (arb(1) / arb(index * index)).sin()


def arb_bounds(value: arb) -> list[str]:
    padding = aq(EVIDENCE_PADDING)
    return [str(value.lower() - padding), str(value.upper() + padding)]


def label_code(label: str) -> int:
    if label == "H0_CENTRAL_OUTER":
        return 0
    if not label.startswith("H") or not label[1:].isdigit():
        raise ValueError(f"invalid homogeneity label: {label}")
    index = int(label[1:])
    if index < N0:
        raise ValueError(f"tail index below {N0}: {index}")
    return index - N0 + 1


def cantor_pair(left: int, right: int) -> int:
    if left < 0 or right < 0:
        raise ValueError("Cantor pairing domain")
    total = left + right
    return total * (total + 1) // 2 + right


def operator_cell_id(
    parent_cell_id: str,
    sheet_kind: str,
    sigma0: int,
    source_label: str,
    third_label: str,
    third_sigma: int,
) -> str:
    source_code = label_code(source_label)
    third_code = label_code(third_label)
    paired = cantor_pair(source_code, third_code)
    payload = [
        parent_cell_id, sheet_kind, sigma0, source_label,
        third_sigma, third_label, paired,
    ]
    return "round117-operator-cell:" + digest(payload)


def source_only_operator_cell_id(
    parent_cell_id: str, sigma0: int, source_label: str,
    actual_third_owner: str, actual_third_sigma: int,
) -> str:
    payload = [
        parent_cell_id, "BYPASS", sigma0, source_label,
        label_code(source_label), actual_third_owner,
        actual_third_sigma, "H0_CENTRAL",
    ]
    return "round117-operator-cell:" + digest(payload)


def symbolic_tail_theorem() -> dict[str, Any]:
    tests = []
    for index in BOUNDARY_QUERY_INDICES:
        left = Q(1, (index + 1) ** 2)
        right = Q(1, index**2)
        middle = (left + right) / 2
        if not (Q(0) < left < middle < right):
            raise RuntimeError("exact symbolic strip test")
        tests.append({
            "index": index,
            "left_angle": str(left),
            "interior_test_angle": str(middle),
            "right_angle": str(right),
            "boundary_owner_label": f"H{index}",
            "interior_unique_index": index,
        })
    return {
        "q_exponent": 2,
        "minimum_tail_index": N0,
        "boundary_function": "b(n)=sin(n^(-2))",
        "exact_strip_definition": "H_n=(b(n+1),b(n)] for every integer n>=128",
        "central_outer_definition_on_local_square": "H0=(b(128),1/16384]",
        "natural_grazing_definition": "c=0 is a singular trace-ledger stratum, not an operator cell",
        "strict_monotonicity_proof": (
            "for n>=128, 0<(n+1)^(-2)<n^(-2)<pi/2 and sin is strictly increasing, "
            "hence 0<b(n+1)<b(n)"
        ),
        "adjacency_no_overlap_no_gap_proof": (
            "H_n is open at b(n+1) and closed at b(n); b(n) is owned by H_n, "
            "so consecutive strips meet with exactly one owner and distinct interiors"
        ),
        "limit_and_union_proof": (
            "n^(-2) decreases to 0 and sin is continuous at 0, so b(n) decreases to 0; "
            "therefore the union over all n>=128 is exactly (0,b(128)]"
        ),
        "unique_index_formula": "n=floor(asin(c)^(-1/2)) for 0<c<=b(128)",
        "unique_index_formula_proof": (
            "b(n+1)<c<=b(n) iff (n+1)^(-2)<asin(c)<=n^(-2), "
            "iff n<=asin(c)^(-1/2)<n+1"
        ),
        "tail_is_symbolic_and_not_finitely_enumerated": True,
        "finite_interface_test_rows": tests,
    }


def hit_generator_families(parent_cell_id: str, sigma0: int, sigma3: int) -> list[dict[str, Any]]:
    base = {
        "actual_region_intersection": (
            "Round113 parent root-graph region intersected with both listed exact half-open angle classes"
        ),
        "active_intersection_predicate": (
            "max(parent_lower,boundary_lower)<min(parent_upper,boundary_upper), with both owner conventions applied"
        ),
        "official_path_inheritance": "unchanged from the Round113 parent relative interior",
    }
    rows = [
        {
            **base,
            "family": "HIT_TAIL_TAIL",
            "source_label_domain": "H_j, every integer j>=128",
            "third_label_domain": "H_k, every integer k>=128",
            "stable_index": "Cantor(code(H_j),code(H_k))",
            "cardinality": "COUNTABLY_INFINITE_N2",
        },
        {
            **base,
            "family": "HIT_TAIL_CENTRAL_OUTER",
            "source_label_domain": "H_j, every integer j>=128",
            "third_label_domain": "H0_CENTRAL_OUTER",
            "stable_index": "Cantor(code(H_j),0)",
            "cardinality": "COUNTABLY_INFINITE_N",
        },
        {
            **base,
            "family": "HIT_CENTRAL_OUTER_TAIL",
            "source_label_domain": "H0_CENTRAL_OUTER",
            "third_label_domain": "H_k, every integer k>=128",
            "stable_index": "Cantor(0,code(H_k))",
            "cardinality": "COUNTABLY_INFINITE_N",
        },
        {
            **base,
            "family": "HIT_CENTRAL_OUTER_CENTRAL_OUTER",
            "source_label_domain": "H0_CENTRAL_OUTER",
            "third_label_domain": "H0_CENTRAL_OUTER",
            "stable_index": "Cantor(0,0)=0",
            "cardinality": "ONE",
        },
    ]
    # A concrete stable-ID interface test, without pretending to enumerate the tail.
    for row, labels in zip(rows, (("H128", "H128"), ("H128", "H0_CENTRAL_OUTER"),
                                  ("H0_CENTRAL_OUTER", "H128"),
                                  ("H0_CENTRAL_OUTER", "H0_CENTRAL_OUTER"))):
        row["stable_id_interface_sample"] = {
            "source_label": labels[0],
            "third_label": labels[1],
            "operator_cell_id": operator_cell_id(
                parent_cell_id, "HIT", sigma0, labels[0], labels[1], sigma3,
            ),
        }
    return rows


def bypass_generator_families(
    parent_cell_id: str,
    sigma0: int,
    source_outer_nonempty: bool,
    actual_owner: str,
    actual_sigma: int,
) -> list[dict[str, Any]]:
    common = {
        "actual_region_intersection": (
            "Round113 BYPASS parent root-graph region intersected with the listed exact source class; b3 remains unindexed"
        ),
        "actual_third_collision_class": "H0_CENTRAL",
        "official_path_inheritance": "unchanged from the Round113 parent relative interior",
    }
    rows = [{
        **common,
        "family": "BYPASS_SOURCE_TAIL__ACTUAL_THIRD_H0",
        "source_label_domain": "H_j, every integer j>=128 satisfying the exact parent-intersection predicate",
        "source_active_intersection_predicate": (
            "max(parent_c0_lower,b(j+1))<min(parent_c0_upper,b(j)), with both owner conventions applied"
        ),
        "cardinality": "COUNTABLE_SUBFAMILY_OF_N",
        "stable_id_interface_sample": {
            "source_label": "H128",
            "operator_cell_id": source_only_operator_cell_id(
                parent_cell_id, sigma0, "H128", actual_owner, actual_sigma,
            ),
            "sample_is_an_ID_API_test_not_a_nonempty-claim_for_this_parent": True,
        },
    }]
    if source_outer_nonempty:
        rows.append({
            **common,
            "family": "BYPASS_SOURCE_CENTRAL_OUTER__ACTUAL_THIRD_H0",
            "source_label_domain": "H0_CENTRAL_OUTER",
            "source_active_intersection_predicate": "parent c0 interval intersects (b(128),1/16384]",
            "cardinality": "ONE",
            "stable_id_interface_sample": {
                "source_label": "H0_CENTRAL_OUTER",
                "operator_cell_id": source_only_operator_cell_id(
                    parent_cell_id, sigma0, "H0_CENTRAL_OUTER", actual_owner, actual_sigma,
                ),
                "sample_is_certified_nonempty_for_this_parent": True,
            },
        })
    return rows


def common_refinement_row(
    audited_sheet: dict[str, Any],
    input_sheet: dict[str, Any],
    parent: dict[str, Any],
    b128: arb,
    b128_directed: dict[str, Any],
    cores: list[Any],
) -> tuple[dict[str, Any], Q | None]:
    branch = tuple(input_sheet["branch_key"])
    sigma0 = input_sheet["source_grazing_sign_sigma0"]
    sigma_designated = input_sheet["designated_third_transverse_sign_sigma3"]
    if sigma0 not in (-1, 1) or sigma_designated not in (-1, 1):
        raise RuntimeError("grazing sign")
    common = {
        "parent_round113_cell_id": parent["cell_id"],
        "parent_round113_sheet_id": audited_sheet["sheet_id"],
        "sheet_kind": audited_sheet["sheet_kind"],
        "corner_index": audited_sheet["corner_index"],
        "branch_key": audited_sheet["branch_key"],
        "parent_parameter_box": parent["parameter_box"],
        "parent_implicit_t_root_enclosure": parent["implicit_t_root_enclosure"],
        "parent_artificial_boundary_ownership": audited_sheet[
            "artificial_boundary_half_open_ownership_convention"
        ],
        "source_grazing_sign_sigma0": sigma0,
        "official_path_id_inherited": parent["official_path_id"],
        "official_word_key_ids_inherited": parent["official_word_key_ids"],
        "official_path_scope": "Round113 regular relative interior and all one-sided closures already certified there",
        "natural_source_boundary_c0_zero_owned_by_trace_ledger": True,
        "actual_standard_curve_child_installed": False,
        "gate5_F1_through_F6_installed": False,
    }
    if audited_sheet["sheet_kind"] == "HIT":
        if parent["ordered_regular_relative_interior_owner_ids"][2] != branch[2]:
            raise RuntimeError("HIT designated third owner")
        row = {
            **common,
            "designated_third_grazing_sign_sigma3": sigma_designated,
            "actual_third_collision_owner_id": branch[2],
            "actual_third_collision_cosine_coordinate": "c3",
            "actual_third_cosine_identity": "Delta3=R3^2*c3^2 and c3>=0 imply sqrt(Delta3)/R3=c3",
            "source_and_actual_third_indices": "independent labels (j,k), with each label H0 or an integer >=128",
            "generator_families": hit_generator_families(
                parent["cell_id"], sigma0, sigma_designated,
            ),
            "central_outer_source_child_nonempty": True,
            "central_outer_actual_third_child_nonempty": True,
            "natural_actual_third_boundary_c3_zero_owned_by_trace_ledger": True,
            "bypass_b3_homogeneity_index": None,
        }
        return row, None

    coordinate = "b3"
    c00, c01 = map(Q, parent["parameter_box"]["c0"])
    z0, z1 = map(Q, parent["parameter_box"][coordinate])
    t0, t1 = map(Q, parent["implicit_t_root_enclosure"])
    source = replace(cores[branch[0]], chart_id=input_sheet["source_chart"])
    geometry = round113.path_geometry(
        source, branch, sigma0, "BYPASS", t0, t1, c00, c01, z0, z1,
    )
    actual_owner = parent["ordered_regular_relative_interior_owner_ids"][2]
    winner = round113.candidate_geometry(geometry["states"][2], actual_owner)
    if winner.get("classification") != "STRICT_FUTURE_NEAR_ROOT":
        raise RuntimeError("BYPASS actual winner collision status")
    radius = aq(round112.radius(actual_owner))
    actual_cosine = winner["radical"].value / radius
    actual_momentum = winner["transverse"].value / radius
    actual_sigma = strict_sign(actual_momentum)
    central_margin = actual_cosine - b128
    identity = actual_cosine * actual_cosine + actual_momentum * actual_momentum - arb(1)
    if actual_sigma == 0 or not bool(actual_cosine > b128) or not identity.contains(0):
        raise RuntimeError("BYPASS central H0 or collision identity")
    b128_upper = Q(b128_directed["directed_upper_rational"])
    source_outer_nonempty = c01 > b128_upper and max(c00, b128_upper) < c01
    row = {
        **common,
        "designated_third_grazing_sign_sigma3": sigma_designated,
        "actual_third_collision_owner_id": actual_owner,
        "actual_third_collision_momentum_sign_sigma_actual": actual_sigma,
        "actual_third_collision_cosine_coordinate": "sqrt(discriminant_of_actual_G_winner)/R_actual",
        "actual_third_collision_cosine_enclosure": arb_bounds(actual_cosine),
        "actual_third_collision_momentum_enclosure": arb_bounds(actual_momentum),
        "actual_third_collision_cosine_square_plus_momentum_square_minus_one_enclosure": arb_bounds(identity),
        "actual_third_collision_cosine_minus_b128_enclosure": arb_bounds(central_margin),
        "actual_third_collision_homogeneity_label": "H0_CENTRAL",
        "actual_third_collision_H0_strict_whole_parent_cell": True,
        "source_index_only": "source label j is H0 or an integer >=128",
        "bypass_b3_homogeneity_index": None,
        "bypass_b3_is_collision_angle": False,
        "bypass_b3_role": "analytic miss-side root coordinate for the designated tangent target only",
        "central_outer_source_child_nonempty": source_outer_nonempty,
        "generator_families": bypass_generator_families(
            parent["cell_id"], sigma0, source_outer_nonempty, actual_owner, actual_sigma,
        ),
        "natural_designated_tangent_boundary_b3_zero_owned_by_trace_ledger": True,
    }
    strict_lower = exact_dyadic(central_margin.lower()) - EVIDENCE_PADDING
    if strict_lower <= 0:
        raise RuntimeError("BYPASS central margin strict lower")
    return row, strict_lower


def boundary_ledger(round113_result: dict[str, Any]) -> dict[str, Any]:
    natural = []
    for trace in round113_result["natural_boundary_trace_rows"]:
        natural.append({
            "corner_index": trace["corner_index"],
            "round113_trace_id": trace["trace_id"],
            "source_c0_zero": "NATURAL_SOURCE_GRAZING_TRACE_LEDGER",
            "hit_c3_zero": "NATURAL_DESIGNATED_THIRD_GRAZING_TRACE_LEDGER",
            "bypass_b3_zero": "NATURAL_DESIGNATED_TARGET_TANGENCY_TRACE_LEDGER; b3 is not the actual-winner collision cosine",
            "regular_operator_child_owns_natural_boundary": False,
        })
    return {
        "artificial_homogeneity_boundary_rule": (
            "for every n>=128, c=b(n) is owned by H_n; H_(n-1), or H0 when n=128, is open there"
        ),
        "artificial_parent_dyadic_boundary_rule": (
            "inherit the exact Round113 [lower,upper) owner, except a leaf ending at the outer endpoint owns it"
        ),
        "two_owner_conflict_resolution": (
            "an operator region is the conjunction of the unique Round113 parent owner and unique homogeneity owner"
        ),
        "natural_trace_rows": natural,
        "natural_trace_rows_sha256": digest(natural),
    }


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 256:
        raise RuntimeError("precision must be at least 256 bits")
    ctx.prec = precision_bits
    validate_pins()
    doc112 = strict_load(ROUND112_JSON)
    doc113 = strict_load(ROUND113_JSON)
    if (
        set(doc112) != {"schema", "result", "result_sha256"}
        or doc112["schema"] != round112.SCHEMA
        or doc112["result_sha256"] != digest(doc112["result"])
    ):
        raise RuntimeError("Round112 document contract")
    if (
        set(doc113) != {"schema", "result", "result_sha256"}
        or doc113["schema"] != round113.SCHEMA
        or doc113["result_sha256"] != digest(doc113["result"])
    ):
        raise RuntimeError("Round113 document contract")
    upstream = doc113["result"]
    if (
        upstream.get("closed_root_sheet_count") != 16
        or upstream.get("certified_parameter_cell_count") != 72
        or upstream.get("residual_parameter_cell_count") != 0
        or upstream.get("whole_sheet_regular_relative_interior_unique_owner_ordering_installed") is not True
        or upstream.get("official_gate5_paths_installed_on_every_certified_relative_interior_cell") is not True
        or upstream.get("homogeneity_tail_or_canonical_child_installed") is not False
        or upstream.get("gate5_actual_child_field_count") != 0
        or upstream.get("sheet_rows_sha256") != digest(upstream.get("sheet_rows"))
    ):
        raise RuntimeError("Round113 semantic handoff")
    input_sheets = {row["sheet_id"]: row for row in doc112["result"]["sheet_rows"]}
    if len(input_sheets) != 16:
        raise RuntimeError("Round112 sheet join")

    b128_directed = homogeneity_boundary(N0)
    b128 = boundary_ball(N0)
    b128_upper = Q(b128_directed["directed_upper_rational"])
    outer_sliver_lower = OUTER - b128_upper
    if outer_sliver_lower <= 0 or not bool(aq(OUTER) > b128):
        raise RuntimeError("central outer sliver is not strict")

    cores = core_cert.physical_cores()
    rows: list[dict[str, Any]] = []
    bypass_lowers: list[Q] = []
    for sheet in upstream["sheet_rows"]:
        input_sheet = input_sheets.get(sheet["sheet_id"])
        if input_sheet is None:
            raise RuntimeError("missing Round112 sheet join")
        for parent in sheet["certified_cells"]:
            row, bypass_lower = common_refinement_row(
                sheet, input_sheet, parent, b128, b128_directed, cores,
            )
            rows.append(row)
            if bypass_lower is not None:
                bypass_lowers.append(bypass_lower)
    rows.sort(key=lambda row: row["parent_round113_cell_id"])
    if len(rows) != 72 or len(bypass_lowers) != 64:
        raise RuntimeError("common refinement row count")

    ledger = boundary_ledger(upstream)
    query_rows = [homogeneity_boundary(index) for index in BOUNDARY_QUERY_INDICES]
    for left, right in zip(query_rows, query_rows[1:]):
        if Q(right["directed_upper_rational"]) >= Q(left["directed_lower_rational"]):
            raise RuntimeError("sampled boundary monotonicity")

    hit_rows = [row for row in rows if row["sheet_kind"] == "HIT"]
    bypass_rows = [row for row in rows if row["sheet_kind"] == "BYPASS"]
    source_outer_rows = sum(row["central_outer_source_child_nonempty"] for row in rows)
    family_count = sum(len(row["generator_families"]) for row in rows)
    result = {
        "precision_bits": precision_bits,
        "boundary_query_precision_bits": BOUNDARY_PRECISION_BITS,
        "minimum_homogeneity_tail_index": N0,
        "local_rational_outer_cosine_coordinate": str(OUTER),
        "b128_directed_enclosure": b128_directed,
        "central_outer_sliver_definition": "sin(128^(-2))<c<=1/16384",
        "central_outer_sliver_strict_rational_lower_width": str(outer_sliver_lower),
        "central_outer_sliver_nonempty": True,
        "exact_symbolic_tail_theorem": symbolic_tail_theorem(),
        "directed_boundary_query_rows": query_rows,
        "directed_boundary_query_rows_sha256": digest(query_rows),
        "label_integer_code": "code(H0_CENTRAL_OUTER)=0; code(H_n)=n-127 for every n>=128",
        "cantor_pairing": "Cantor(a,b)=((a+b)*(a+b+1))/2+b on nonnegative integers",
        "cantor_pairing_interface_tests": [
            {"a": 0, "b": 0, "value": cantor_pair(0, 0)},
            {"a": 1, "b": 0, "value": cantor_pair(1, 0)},
            {"a": 0, "b": 1, "value": cantor_pair(0, 1)},
            {"a": 1, "b": 1, "value": cantor_pair(1, 1)},
            {"a": 129, "b": 257, "value": cantor_pair(129, 257)},
        ],
        "round113_parent_proof_box_count": len(rows),
        "hit_parent_proof_box_count": len(hit_rows),
        "bypass_parent_proof_box_count": len(bypass_rows),
        "finite_generator_family_template_instance_count": family_count,
        "parent_rows_with_nonempty_source_central_outer_child": source_outer_rows,
        "hit_double_index_generator_installed": True,
        "bypass_source_only_index_generator_installed": True,
        "bypass_actual_winner_whole_parent_cell_H0_count": len(bypass_rows),
        "bypass_b3_used_as_collision_angle_count": 0,
        "global_bypass_actual_cosine_minus_b128_strict_rational_lower": str(min(bypass_lowers)),
        "common_refinement_rows": rows,
        "common_refinement_rows_sha256": digest(rows),
        "boundary_ownership_ledger": ledger,
        "boundary_ownership_ledger_sha256": digest(ledger),
        "operator_cell_schema_installed": True,
        "operator_cell_regions_are_actual_parameter_root_graph_intersections": True,
        "countable_tail_paid_by_symbolic_generator_not_finite_cutoff": True,
        "actual_parent_W_standard_curve_join_installed": False,
        "actual_standard_curve_child_count": 0,
        "canonical_curve_recut_instance_count": 0,
        "gate5_child_field_counts": {f"F{index}": 0 for index in range(1, 7)},
        "gate5_global_maturity": "10/18",
        "gate5_block_count": 0,
        "whole_trace_collar_installed": False,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "exact countable q=2 homogeneity generator and boundary ownership on the 72 Round113 endpoint proof-box root-graph regions; "
            "HIT has independent source/actual-third indices and BYPASS has a source index plus a rigorously central actual G-winner"
        ),
        "strict_nonclaims": [
            "the analytic BYPASS coordinate b3 is not a collision angle and receives no homogeneity index",
            "finite directed-boundary queries test the interface but do not enumerate or replace the symbolic infinite tail",
            "a two-dimensional operator-cell/root-graph parameter region is not an actual standard-curve child",
            "official paths are inherited from Round113 parents; no parent-W curve join or adapted-arclength recut is installed",
            "no Gate5 F1--F6 field, whole-trace collar, or CM2 theorem is installed",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--query-boundary", type=int)
    parser.add_argument("--boundary-precision-bits", type=int, default=BOUNDARY_PRECISION_BITS)
    args = parser.parse_args()
    if args.query_boundary is not None:
        payload = {
            "schema": "cm2.round117.directed-homogeneity-boundary-query.v1",
            "result": homogeneity_boundary(args.query_boundary, args.boundary_precision_bits),
        }
        print(json.dumps(payload, sort_keys=True, indent=2))
        return 0
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
