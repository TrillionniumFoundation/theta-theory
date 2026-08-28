#!/usr/bin/env python3
"""Round177 exact boundary/source-seam ledger for 16 tangency composites.

Round175 proved that all sixteen parents contain both a strict live open
witness and a strict mismatch open witness.  This continuation therefore
does not issue whole-parent credit.  It resolves the previously nominal
outgoing-H clipping boundaries, distinguishes the true algebraic source
chart boundary ``2*t**2=1`` from the rational atlas guard, and records the
dimension of every distinguished Delta/H/source-seam stratum.

The producer uses the independently verified Round175 result as an upstream
registry.  The Round177 verifier does not import or execute this producer or
the Round175 producer; it reconstructs the rows from the pinned Gate3
geometry.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Callable

import flint
from flint import arb

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_round175_dimension_safe_tangency_arrangement as r175


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json"
)
SCHEMA = "cm2.round177.tangency-boundary-and-source-seam-ledger.v1"
MAX_INPUT_BYTES = 16 * 1024 * 1024
ROOT_STEPS = 72
SEAM_STEPS = 144
SEAM_GRAPH_STEPS = 72
R_W = Q(4, 25)

BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
OWNERSHIP = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
R175_PRODUCER = "cm2_round175_dimension_safe_tangency_arrangement.py"
R175_CERT = "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
R175_VERIFIER = "cm2_round175_dimension_safe_tangency_arrangement_verifier.py"
R175_VER = "cm2_round175_dimension_safe_tangency_arrangement_verification.json"

PINS: dict[str, str] = {
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GE_SOURCE:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    OWNERSHIP:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    R175_PRODUCER:
        "16122dcc7c39b140d45139a01bac6d6f41d7cbb60da2499ecc50fbeac2766355",
    R175_CERT:
        "a2a69b3d4559fadb647d8f9ea6a06ef4c1625647965423cdb25f53fa08d2deee",
    R175_VERIFIER:
        "2c8a5906806adef423ba5d409cbf294c4988db72a1b9cfdf26a61ee9a7d290e6",
    R175_VER:
        "6f1d8e515be0cdc977445e7e0d8633df510c793ff99e0f76cf3b4578d2d2bfca",
}
R175_RESULT = "827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72"
R175_VER_RESULT = "ed5fd96874a65b49a1e05d5589e2dd9711f224d08a99123e582bc54bce294f6a"

CROSS_KEYS = (
    "W:E:00.15.0000000",
    "W:E:07.00.1111111",
)


class Round177Error(RuntimeError):
    """Fail-closed Round177 error."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round177Error(label)


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["row_sha256"] = digest(result)
    return result


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise Round177Error(f"non-integer JSON number:{value}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str and "\x00" not in key, f"key:{path}")
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"NUL:{path}")


def read_regular(path: Path, expected: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"hardlink:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def strict_json(data: bytes, label: str) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"raw NUL:{label}")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round177Error(f"invalid JSON:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"top object:{label}")
    return value


def load_envelope(name: str) -> dict[str, Any]:
    value = strict_json(read_regular(HERE / name, PINS[name]), name)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope:{name}",
    )
    require(value["result_sha256"] == digest(value["result"]), f"digest:{name}")
    return value


def validate_chain() -> dict[str, Any]:
    require(
        flint.__version__ == "0.9.0"
        and atlas.ctx.prec == 192
        and Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve()
        and Path(ge.__file__).resolve() == (HERE / GE_SOURCE).resolve()
        and Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve()
        and Path(r175.__file__).resolve() == (HERE / R175_PRODUCER).resolve(),
        "module identity/environment",
    )
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    ownership = strict_json(
        read_regular(HERE / OWNERSHIP, PINS[OWNERSHIP]), OWNERSHIP
    )
    require(
        ownership["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and ownership["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes",
        "half-open ownership",
    )
    certificate = load_envelope(R175_CERT)
    verification = load_envelope(R175_VER)
    require(
        certificate["result_sha256"] == R175_RESULT
        and verification["result_sha256"] == R175_VER_RESULT
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"] == R175_RESULT
        and verification["result"]["independence_contract"][
            "full_expected_canonical_equality"
        ] is True,
        "Round175 verified chain",
    )
    prior = certificate["result"]
    require(
        prior["parent_arrangement_census"]["fully_excluded_parent_count"] == 6
        and prior["parent_arrangement_census"]["mixed_composite_parent_count"] == 16
        and prior["Round172_to_Round175_composition"][
            "combined_whole_record_excluded"
        ] == 73178
        and prior["Round172_to_Round175_composition"][
            "Round175_conservative_live"
        ] == 3654,
        "Round175 census/ledger",
    )
    return certificate


def strict_sign(value: Any) -> str:
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    if bool(value > 0):
        return "STRICT_POSITIVE"
    return "UNRESOLVED"


def reduced_h(t0: Q, t1: Q, p: Q, seam: str) -> Any:
    """Outgoing H with exact cancellation of the source-centre s terms."""

    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    inv_sqrt_two = 1 / arb(2).sqrt()
    sigma = 1 if seam == "NW" else -1
    aa = (
        base.arbq(R_W) * inv_sqrt_two * (sigma * radial + t)
        - t
    )
    bb = (
        base.arbq(R_W)
        + radial * (base.arbq(R_W) * inv_sqrt_two - 1)
        - base.arbq(R_W) * inv_sqrt_two * sigma * t
    )
    return cp * aa + base.arbq(p) * bb


def reduced_h_t_derivative(t0: Q, t1: Q, p: Q, seam: str) -> Any:
    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    inv_sqrt_two = 1 / arb(2).sqrt()
    sigma = 1 if seam == "NW" else -1
    dr = -t / radial
    da = (
        base.arbq(R_W) * inv_sqrt_two * (sigma * dr + 1)
        - 1
    )
    db = (
        dr * (base.arbq(R_W) * inv_sqrt_two - 1)
        - base.arbq(R_W) * inv_sqrt_two * sigma
    )
    return cp * da + base.arbq(p) * db


def reduced_owner_delta(t0: Q, t1: Q, p: Q) -> Any:
    """Delta for W[1,0], after cancelling the common W-centre shift."""

    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    transverse = -cp * t + base.arbq(p) * (base.arbq(R_W) - radial)
    return base.arbq(R_W * R_W) - transverse * transverse


def bisect_strict_root(
    function: Callable[[Q, Q], Any],
    lower: Q,
    upper: Q,
    steps: int,
) -> tuple[Q, Q, str, str]:
    lower_sign = strict_sign(function(lower, lower))
    upper_sign = strict_sign(function(upper, upper))
    require(
        "UNRESOLVED" not in {lower_sign, upper_sign}
        and lower_sign != upper_sign,
        "root endpoint signs",
    )
    initial_lower_sign = lower_sign
    initial_upper_sign = upper_sign
    for _index in range(steps):
        middle = (lower + upper) / 2
        middle_sign = strict_sign(function(middle, middle))
        require(middle_sign != "UNRESOLVED", "root midpoint sign")
        if middle_sign == lower_sign:
            lower = middle
        else:
            upper = middle
    require(
        strict_sign(function(lower, lower)) == initial_lower_sign
        and strict_sign(function(upper, upper)) == initial_upper_sign,
        "final root signs",
    )
    return lower, upper, initial_lower_sign, initial_upper_sign


def positive_source_seam_bracket() -> tuple[Q, Q]:
    lower, upper = Q(707, 1000), Q(708, 1000)
    require(2 * lower * lower < 1 < 2 * upper * upper, "seam seed")
    for _index in range(SEAM_STEPS):
        middle = (lower + upper) / 2
        if 2 * middle * middle < 1:
            lower = middle
        else:
            upper = middle
    require(2 * lower * lower < 1 < 2 * upper * upper, "seam bracket")
    return lower, upper


def bisect_graph_over_t_bracket(
    function: Callable[[Q, Q, Q], Any],
    t0: Q,
    t1: Q,
    p0: Q,
    p1: Q,
) -> tuple[Q, Q, str, str]:
    lower_sign = strict_sign(function(t0, t1, p0))
    upper_sign = strict_sign(function(t0, t1, p1))
    require(
        "UNRESOLVED" not in {lower_sign, upper_sign}
        and lower_sign != upper_sign,
        "seam graph endpoint signs",
    )
    initial_lower_sign, initial_upper_sign = lower_sign, upper_sign
    for _index in range(SEAM_GRAPH_STEPS):
        middle = (p0 + p1) / 2
        middle_sign = strict_sign(function(t0, t1, middle))
        require(middle_sign != "UNRESOLVED", "seam graph midpoint")
        if middle_sign == lower_sign:
            p0 = middle
        else:
            p1 = middle
    return p0, p1, initial_lower_sign, initial_upper_sign


def box_row(box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
    }


def graph_boundary_edges(kind: str, clipped: bool, live_side: str) -> list[dict[str, Any]]:
    if not clipped:
        labels = ("t_lower", "t_upper", "s_lower", "s_upper")
    else:
        outer_t = "t_lower" if live_side == "LOWER_T_SIDE" else "t_upper"
        labels = (outer_t, "p_clipping_face", "s_lower", "s_upper")
    return [
        {
            "edge_id": f"{kind}:{label}",
            "dimension": 1,
            "integer_credit": 0,
        }
        for label in labels
    ]


def physical_partition(key: str, box: Any) -> dict[str, Any]:
    maximum_abs = max(abs(box.t0), abs(box.t1))
    if 2 * maximum_abs * maximum_abs < 1:
        return {
            "classification": "WHOLE_PARENT_STRICT_PHYSICAL_CHART_INTERIOR",
            "chart_domain_polynomial": "C(t)=1-2*t^2",
            "C_sign_on_parent": "STRICT_POSITIVE",
            "three_dimensional_open_strata": 1,
            "two_dimensional_source_seam_strata": 0,
            "three_dimensional_guard_outside_strata": 0,
            "guard_outside_exterior_credit": 0,
            "rational_endpoint_proof": f"2*({maximum_abs})^2<1",
        }
    require(key in CROSS_KEYS, f"unexpected source seam:{key}")
    alpha0, alpha1 = positive_source_seam_bracket()
    negative = box.t1 < 0
    seam_bracket = (-alpha1, -alpha0) if negative else (alpha0, alpha1)
    require(
        box.t0 < seam_bracket[0] < seam_bracket[1] < box.t1,
        f"seam inside:{key}",
    )
    adjacent = "W:S" if negative else "W:N"
    relation = (
        "t_E<-1/sqrt(2)"
        if negative else "t_E>1/sqrt(2)"
    )
    return {
        "classification": "EXACT_PHYSICAL_INTERIOR_SEAM_GUARD_OUTSIDE_PARTITION",
        "chart_domain_polynomial": "C(t)=1-2*t^2",
        "algebraic_source_seam": {
            "equation": "2*t^2=1",
            "selected_root": "-1/sqrt(2)" if negative else "+1/sqrt(2)",
            "rational_isolating_bracket": [
                str(seam_bracket[0]), str(seam_bracket[1])
            ],
            "dimension": 2,
            "half_open_owner": "E",
            "adjacent_nonowner_chart": adjacent.split(":")[1],
            "integer_credit": 0,
        },
        "physical_E_chart_interior": {
            "C_sign": "STRICT_POSITIVE",
            "dimension": 3,
            "positive_volume": True,
        },
        "guard_outside": {
            "C_sign": "STRICT_NEGATIVE",
            "dimension": 3,
            "positive_volume": True,
            "exact_side": relation,
            "disposition": "CHART_REJECTION_REQUIRES_ADJACENT_RECOORDINATION",
            "adjacent_chart": adjacent,
            "recoordination": {
                "t_adjacent": "sqrt(1-t_E^2)",
                "p_adjacent": "p_E",
                "s_adjacent": "s_E",
                "same_physical_normal_and_tangent_frame": True,
            },
            "exterior_exclusion_credit": 0,
        },
        "three_dimensional_open_strata": 2,
        "two_dimensional_source_seam_strata": 1,
        "three_dimensional_guard_outside_strata": 1,
        "guard_outside_exterior_credit": 0,
    }


def source_seam_intersections(
    key: str,
    box: Any,
    seam: str,
) -> dict[str, Any] | None:
    if key not in CROSS_KEYS:
        return None
    alpha0, alpha1 = positive_source_seam_bracket()
    t0, t1 = (
        (-alpha1, -alpha0) if box.t1 < 0 else (alpha0, alpha1)
    )
    delta = bisect_graph_over_t_bracket(
        reduced_owner_delta, t0, t1, box.p0, box.p1
    )
    h = bisect_graph_over_t_bracket(
        lambda a, b, p: reduced_h(a, b, p, seam),
        t0, t1, box.p0, box.p1,
    )
    if seam == "NW":
        require(h[1] < delta[0], f"source seam graph order:{key}")
        order = "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH"
    else:
        require(delta[1] < h[0], f"source seam graph order:{key}")
        order = "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH"
    return {
        "source_seam_open_2D_regions_cut_by_Delta_and_H": 3,
        "source_seam_intersect_Delta": {
            "dimension": 1,
            "p_isolating_bracket": [str(delta[0]), str(delta[1])],
            "endpoint_signs": [delta[2], delta[3]],
            "integer_credit": 0,
        },
        "source_seam_intersect_H": {
            "dimension": 1,
            "p_isolating_bracket": [str(h[0]), str(h[1])],
            "endpoint_signs": [h[2], h[3]],
            "half_open_owner": "W",
            "integer_credit": 0,
        },
        "strict_graph_order_on_source_seam": order,
        "source_seam_intersect_Delta_intersect_H": {
            "status": "EMPTY",
            "nominal_dimension": 0,
            "integer_credit": 0,
        },
    }


def validate_witnesses(row: dict[str, Any], box: Any) -> None:
    for label in ("strict_live_open_witness", "strict_mismatch_open_witness"):
        witness = row[label]
        point = witness["point"]
        t, p, s = Q(point["t"]), Q(point["p"]), Q(point["s"])
        require(
            box.t0 < t < box.t1
            and box.p0 < p < box.p1
            and box.s0 <= s <= box.s1
            and 2 * t * t < 1,
            f"witness interior:{row['ambient_leaf_key']}:{label}",
        )
    require(
        row["strict_live_open_witness"]["first_hit_classification"]
        == "unique_first"
        and row["strict_live_open_witness"]["first_owner"] == "W[1,0]",
        f"live witness prefix:{row['ambient_leaf_key']}",
    )


def sign_patterns(row: dict[str, Any]) -> list[dict[str, Any]]:
    seam = row["outgoing_arrangement"]["relevant_seam"]
    owner = row["tangency_target_is_frozen_owner"]
    if owner and seam == "H_NW":
        triples = (
            ("Delta>0", "H_NW>0", "STRICT_COLLISION1_LIVE"),
            ("Delta>0", "H_NW<0", "OUTGOING_CHART_MISMATCH"),
            ("Delta<0", "H_NW<0", "FROZEN_OWNER_ABSENT"),
        )
    elif owner:
        triples = (
            ("Delta<0", "H_SW>0", "FROZEN_OWNER_ABSENT"),
            ("Delta>0", "H_SW>0", "OUTGOING_CHART_MISMATCH"),
            ("Delta>0", "H_SW<0", "STRICT_COLLISION1_LIVE"),
        )
    elif seam == "H_NW":
        triples = (
            ("Delta<0", "H_NW>0", "STRICT_COLLISION1_LIVE"),
            ("Delta<0", "H_NW<0", "OUTGOING_CHART_MISMATCH"),
            ("Delta>0", "H_NW<0", "MISMATCH_TARGET_FIRST"),
        )
    else:
        triples = (
            ("Delta>0", "H_SW>0", "MISMATCH_TARGET_FIRST"),
            ("Delta<0", "H_SW>0", "OUTGOING_CHART_MISMATCH"),
            ("Delta<0", "H_SW<0", "STRICT_COLLISION1_LIVE"),
        )
    return [
        {
            "Delta_sign": delta,
            "H_sign": h,
            "frozen_prefix_disposition": disposition,
            "dimension": 3,
        }
        for delta, h, disposition in triples
    ]


def boundary_row(upstream: dict[str, Any]) -> dict[str, Any]:
    key = upstream["ambient_leaf_key"]
    chart_id, box = r175.decode_parent_box(key)
    require(
        box_row(box) == upstream["parent_box"]
        and upstream["classification"] == "MIXED_COMPOSITE",
        f"upstream row:{key}",
    )
    validate_witnesses(upstream, box)
    owner = upstream["tangency_target_is_frozen_owner"]
    seam_id = upstream["outgoing_arrangement"]["relevant_seam"]
    seam = "NW" if seam_id == "H_NW" else "SW"
    partition = physical_partition(key, box)
    clipping: dict[str, Any]
    if owner:
        face_name = "p_lower" if seam == "NW" else "p_upper"
        p_face = box.p0 if seam == "NW" else box.p1
        root = bisect_strict_root(
            lambda a, b: reduced_h(a, b, p_face, seam),
            box.t0, box.t1, ROOT_STEPS,
        )
        derivative = strict_sign(
            reduced_h_t_derivative(box.t0, box.t1, p_face, seam)
        )
        require(derivative == "STRICT_NEGATIVE", f"H t derivative:{key}")
        live_side = "LOWER_T_SIDE" if seam == "NW" else "UPPER_T_SIDE"
        clipping = {
            "classification": "UNIQUE_TRANSVERSE_H_CLIPPING_LINE",
            "equation": f"{seam_id}(t,{face_name})=0",
            "p_face": str(p_face),
            "t_isolating_bracket": [str(root[0]), str(root[1])],
            "endpoint_signs": [root[2], root[3]],
            "strict_t_derivative_sign_on_parent": derivative,
            "s_interval": [str(box.s0), str(box.s1)],
            "dimension": 1,
            "live_base_side": live_side,
            "mismatch_only_base_side":
                "UPPER_T_SIDE" if live_side == "LOWER_T_SIDE"
                else "LOWER_T_SIDE",
            "integer_credit": 0,
        }
        h_boundary = graph_boundary_edges("H", True, live_side)
        graph_kind = "CLIPPED_GRAPH_OVER_ONE_CONNECTED_BASE_SIDE"
    else:
        clipping = {
            "classification": "NO_P_FACE_CLIPPING_FULL_BASE_GRAPH",
            "dimension": 0,
            "integer_credit": 0,
        }
        h_boundary = graph_boundary_edges("H", False, "")
        graph_kind = "FULL_GRAPH_OVER_T_S_BASE"
    source_intersections = source_seam_intersections(key, box, seam)
    patterns = sign_patterns(upstream)
    chart_multiplier = 2 if key in CROSS_KEYS else 1
    return closed_row({
        "ambient_leaf_key": key,
        "chart_id": chart_id,
        "atlas_path": box.path,
        "parent_box": box_row(box),
        "Round175_row_sha256": upstream["row_sha256"],
        "Round175_tangency_target": upstream["tangency_target"],
        "parent_classification": "MIXED_BOUNDED_RESIDUAL",
        "whole_parent_new_integer_exclusion": False,
        "strict_live_open_witness": upstream["strict_live_open_witness"],
        "strict_mismatch_open_witness": upstream["strict_mismatch_open_witness"],
        "physical_source_chart_partition": partition,
        "three_dimensional_sign_strata": {
            "base_analytic_sign_patterns": patterns,
            "base_pattern_count": 3,
            "chart_domain_multiplier": chart_multiplier,
            "connected_open_3D_stratum_count": 3 * chart_multiplier,
            "guard_outside_patterns_are_chart_residual_not_exterior_credit":
                key in CROSS_KEYS,
        },
        "Delta_zero_graph": {
            "equation": upstream["delta_arrangement"]["equation"],
            "dimension": 2,
            "base_coverage": "FULL_T_S_BASE",
            "strictly_monotone_p_graph": True,
            "half_open_owner":
                upstream["delta_arrangement"]["delta_zero_half_open_owner"],
            "parent_boundary_edge_count": 4,
            "parent_boundary_edges":
                graph_boundary_edges("Delta", False, ""),
            "source_seam_piece_count": 2 if key in CROSS_KEYS else 1,
            "integer_credit": 0,
        },
        "H_zero_graph": {
            "equation": f"{seam_id}=0",
            "dimension": 2,
            "kind": graph_kind,
            "strict_p_derivative_sign": "STRICT_NEGATIVE",
            "half_open_owner": "W",
            "parent_boundary_edge_count": 4,
            "parent_boundary_edges": h_boundary,
            "source_seam_piece_count": 2 if key in CROSS_KEYS else 1,
            "integer_credit": 0,
        },
        "H_parent_face_clipping": clipping,
        "distinguished_intersections": {
            "Delta_intersect_H": {
                "status": "EMPTY_CERTIFIED_BY_ROUND175_AND_REPLAYED_ORDER",
                "nominal_dimension": 1,
                "integer_credit": 0,
            },
            "source_seam_intersections": source_intersections,
            "guard_boundary_credit": 0,
        },
        "later_frozen_prefix_processing": {
            "eligible_only_on_strict_collision1_live_open_stratum": True,
            "eligible_open_component_count": 1,
            "collision1_owner": "W[1,0]",
            "collision1_outgoing_chart": "W",
            "collision2_or_later_exact_key_rows_materialized": 0,
            "bounded_residual_reason": (
                "no pinned global return-coordinate/exact-key bridge is "
                "available for these semi-algebraic live strata"
            ),
            "whole_parent_exclusion_impossible_due_to_strict_live_witness":
                True,
        },
        "dimension_safe_credit": {
            "whole_parent_credit": 0,
            "two_dimensional_graph_credit": 0,
            "one_dimensional_intersection_credit": 0,
            "guard_outside_credit": 0,
        },
    })


def build_result(producer_sha256: str) -> dict[str, Any]:
    certificate = validate_chain()
    upstream = [
        row
        for row in certificate["result"]["parent_arrangement_census"][
            "all_22_parent_rows"
        ]
        if row["classification"] == "MIXED_COMPOSITE"
    ]
    require(len(upstream) == 16, "Round175 residual count")
    rows = sorted(
        (boundary_row(row) for row in upstream),
        key=lambda row: row["ambient_leaf_key"],
    )
    keys = [row["ambient_leaf_key"] for row in rows]
    require(
        [key for key in keys if key in CROSS_KEYS] == list(CROSS_KEYS),
        "cross key order",
    )
    clipped = [
        row for row in rows
        if row["H_parent_face_clipping"]["classification"]
        == "UNIQUE_TRANSVERSE_H_CLIPPING_LINE"
    ]
    full = [
        row for row in rows
        if row["H_parent_face_clipping"]["classification"]
        == "NO_P_FACE_CLIPPING_FULL_BASE_GRAPH"
    ]
    require(len(clipped) == 14 and len(full) == 2, "14/2 H graphs")
    require(
        all(
            row["parent_classification"] == "MIXED_BOUNDED_RESIDUAL"
            and row["whole_parent_new_integer_exclusion"] is False
            for row in rows
        ),
        "0/0/16 parent census",
    )
    three_d = sum(
        row["three_dimensional_sign_strata"][
            "connected_open_3D_stratum_count"
        ]
        for row in rows
    )
    delta_pieces = sum(
        row["Delta_zero_graph"]["source_seam_piece_count"] for row in rows
    )
    h_pieces = sum(
        row["H_zero_graph"]["source_seam_piece_count"] for row in rows
    )
    require(
        three_d == 54 and delta_pieces == 18 and h_pieces == 18,
        "stratum totals",
    )
    return {
        "status": (
            "CERTIFIED_16_EXACT_TANGENCY_BOUNDARY_SOURCE_SEAM_LEDGERS_"
            "ZERO_NEW_WHOLE_PARENT_CREDIT__D02_STILL_BLOCKED"
        ),
        "parent_level_census": {
            "input_Round175_mixed_parents": 16,
            "fully_excluded_parent_count": 0,
            "fully_live_parent_count": 0,
            "mixed_bounded_residual_parent_count": 16,
            "all_retain_strict_live_and_mismatch_open_witnesses": True,
            "new_whole_parent_exclusion_count": 0,
        },
        "exact_boundary_census": {
            "unique_transverse_H_parent_face_clipping_lines": len(clipped),
            "full_base_H_graphs_without_p_face_clipping": len(full),
            "physical_source_chart_cross_seam_parents": len(CROSS_KEYS),
            "physical_source_seam_2D_strata": len(CROSS_KEYS),
            "source_seam_Delta_1D_intersections": len(CROSS_KEYS),
            "source_seam_H_1D_intersections": len(CROSS_KEYS),
            "source_seam_Delta_H_triple_points": 0,
            "Delta_H_1D_intersections": 0,
            "connected_open_3D_sign_strata": three_d,
            "Delta_2D_graph_pieces_after_source_seam_cut": delta_pieces,
            "H_2D_graph_pieces_after_source_seam_cut": h_pieces,
            "H_clipping_1D_rows_sha256": digest([
                row["H_parent_face_clipping"] for row in clipped
            ]),
        },
        "exact_parent_rows_sha256": digest(rows),
        "exact_parent_keys_sha256": digest(keys),
        "exact_parent_keys": keys,
        "exact_parent_rows": rows,
        "source_chart_domain_contract": {
            "true_boundary_equation": "2*t^2=1",
            "physical_interior": "2*t^2<1",
            "guard_outside": "2*t^2>1",
            "rational_atlas_guard": "t in [-177/250,177/250]",
            "E_W_half_open_owner_rule": "E or W owns; N or S excludes",
            "cross_seam_keys": list(CROSS_KEYS),
            "cross_seam_keys_sha256": digest(list(CROSS_KEYS)),
            "guard_outside_is_chart_rejection_not_exterior_exclusion": True,
            "guard_outside_integer_credit": 0,
        },
        "later_prefix_bounded_ledger": {
            "strict_collision1_live_open_components": 16,
            "later_exact_key_rows_materialized": 0,
            "new_later_prefix_whole_parent_exclusions": 0,
            "reason": (
                "later return processing is restricted to the sixteen strict "
                "live open strata; a global return-coordinate/exact-key bridge "
                "for them is not yet pinned"
            ),
        },
        "Round175_to_Round177_composition": {
            "refined_source_W_record_count": 76832,
            "Round175_whole_record_excluded": 73178,
            "Round177_new_whole_parent_excluded": 0,
            "combined_whole_record_excluded": 73178,
            "Round175_conservative_live": 3654,
            "Round177_conservative_live": 3654,
            "live_components": {
                "original_stage_one_match": 518,
                "Round165_seam_live_composites": 504,
                "Round177_mixed_tangency_composites": 16,
                "Round166_owner_active_multi": 2616,
            },
            "conservation_identity": "73178+3654=76832",
        },
        "dimension_safe_noncredit": {
            "Delta_zero_graph_whole_record_credit": 0,
            "H_zero_graph_whole_record_credit": 0,
            "H_parent_face_clipping_line_whole_record_credit": 0,
            "source_chart_seam_whole_record_credit": 0,
            "source_seam_graph_intersection_whole_record_credit": 0,
            "guard_outside_exterior_credit": 0,
            "internal_mismatch_open_strata_whole_parent_credit": 0,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "build a global later-return coordinate/exact-key bridge for the "
            "16 strict live tangency strata, re-coordinate the two positive-"
            "volume adjacent-chart guard slices, and continue the remaining "
            "source-W/source-G exterior ledgers"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "arb_context_precision_bits": atlas.ctx.prec,
            "Round175_producer_used_as_upstream_geometry_helper": True,
            "Round175_files_modified": False,
            "lower_dimensional_strata_promoted_to_integer_credit": False,
        },
    }


def safe_atomic_write(path: Path, data: bytes, protected: set[Path]) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output directory")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(st.st_nlink == 1, "output hardlink")
    require(path.resolve(strict=False) not in protected, "protected alias")
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    source_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    safe_atomic_write(
        arguments.output,
        canonical_bytes(envelope) + b"\n",
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
