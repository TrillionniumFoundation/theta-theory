#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round177 tangency ledger.

This file neither imports nor executes either the Round177 producer or the
Round175 producer.  It decodes the sixteen dyadic parents from Gate3,
re-isolates all fourteen H-clipping roots, reconstructs the two algebraic
source seams and their four graph intersections, and verifies every exact
row/key commitment.  A pinned canonical result identity closes fields that
are descriptive rather than numerical; all semantic attacks are re-signed.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
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


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE
    / "cm2_round177_tangency_boundary_and_source_seam_ledger_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round177_tangency_boundary_and_source_seam_ledger_verification.json"
)
PRODUCER = "cm2_round177_tangency_boundary_and_source_seam_ledger.py"
SCHEMA = "cm2.round177.tangency-boundary-and-source-seam-ledger.v1"
VERIFICATION_SCHEMA = (
    "cm2.round177.tangency-boundary-and-source-seam-ledger-verification.v1"
)
PRODUCER_SHA256 = (
    "729136747872d2a0f8f4bfc0d1c635ca94b6c61df0da1e0f2340ac243616a2ab"
)
EXPECTED_RESULT_SHA256 = (
    "9352f036325bc6e884fc6d31da2e1e2a04532d45fb11de90b3e5051103f56a9f"
)
MAX_INPUT_BYTES = 16 * 1024 * 1024
ROOT_STEPS = 72
SEAM_STEPS = 144
SEAM_GRAPH_STEPS = 72
R_W = Q(4, 25)

BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
OWNERSHIP = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
R175_CERT = "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
R175_PRODUCER = "cm2_round175_dimension_safe_tangency_arrangement.py"
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


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


@dataclass(frozen=True)
class Box:
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q
    depth: int
    path: str


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
        raise VerificationError(label)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise VerificationError(f"noninteger number:{value}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"type:{path}",
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


def strict_parse(
    raw: bytes,
    label: str,
    *,
    require_canonical: bool = True,
) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in raw, f"raw NUL:{label}")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid JSON:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"top:{label}")
    if require_canonical:
        require(raw == canonical_bytes(value) + b"\n", f"canonical:{label}")
    return value


def read_regular(
    path: Path,
    expected: str | None = None,
    *,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"regular:{path}")
    require(not path.is_symlink(), f"symlink:{path}")
    require(st.st_nlink == 1, f"hardlink:{path}")
    require(st.st_size <= maximum, f"oversized:{path}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def load_pinned(name: str) -> dict[str, Any]:
    value = strict_parse(
        read_regular(HERE / name, PINS[name]),
        name,
        require_canonical=False,
    )
    require(
        set(value) == {"schema", "result", "result_sha256"}
        and value["result_sha256"] == digest(value["result"]),
        f"envelope:{name}",
    )
    return value


def dependency_check() -> dict[str, Any]:
    require(
        flint.__version__ == "0.9.0"
        and atlas.ctx.prec == 192
        and Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve()
        and Path(ge.__file__).resolve() == (HERE / GE_SOURCE).resolve()
        and Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve(),
        "environment",
    )
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    producer = read_regular(HERE / PRODUCER, PRODUCER_SHA256)
    ownership = strict_parse(
        read_regular(HERE / OWNERSHIP, PINS[OWNERSHIP]),
        OWNERSHIP,
        require_canonical=False,
    )
    require(
        ownership["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes",
        "ownership",
    )
    r175 = load_pinned(R175_CERT)
    v175 = load_pinned(R175_VER)
    require(
        r175["result_sha256"] == R175_RESULT
        and v175["result_sha256"] == R175_VER_RESULT
        and v175["result"]["status"] == "PASS",
        "Round175 chain",
    )
    return {
        "producer_bytes": len(producer),
        "Round175": r175,
        "dependency_sha256": dict(sorted(PINS.items())),
    }


def strict_sign(value: Any) -> str:
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    if bool(value > 0):
        return "STRICT_POSITIVE"
    return "UNRESOLVED"


def reduced_h(t0: Q, t1: Q, p: Q, seam: str) -> Any:
    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    a = 1 / arb(2).sqrt()
    sigma = 1 if seam == "NW" else -1
    aa = base.arbq(R_W) * a * (sigma * radial + t) - t
    bb = (
        base.arbq(R_W)
        + radial * (base.arbq(R_W) * a - 1)
        - base.arbq(R_W) * a * sigma * t
    )
    return cp * aa + base.arbq(p) * bb


def reduced_h_t_derivative(t0: Q, t1: Q, p: Q, seam: str) -> Any:
    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    a = 1 / arb(2).sqrt()
    sigma = 1 if seam == "NW" else -1
    dr = -t / radial
    da = base.arbq(R_W) * a * (sigma * dr + 1) - 1
    db = dr * (base.arbq(R_W) * a - 1) - base.arbq(R_W) * a * sigma
    return cp * da + base.arbq(p) * db


def reduced_delta(t0: Q, t1: Q, p: Q) -> Any:
    t = base.arb_interval(t0, t1)
    radial = ge.sqrt_one_minus_square(t0, t1)
    cp = base.arbq(1 - p * p).sqrt()
    transverse = -cp * t + base.arbq(p) * (base.arbq(R_W) - radial)
    return base.arbq(R_W * R_W) - transverse * transverse


def bisect_root(
    function: Callable[[Q, Q], Any],
    lower: Q,
    upper: Q,
) -> tuple[Q, Q, str, str]:
    sl = strict_sign(function(lower, lower))
    su = strict_sign(function(upper, upper))
    require(sl != "UNRESOLVED" and su != "UNRESOLVED" and sl != su, "root")
    original = sl, su
    for _index in range(ROOT_STEPS):
        middle = (lower + upper) / 2
        sm = strict_sign(function(middle, middle))
        require(sm != "UNRESOLVED", "root midpoint")
        if sm == sl:
            lower = middle
        else:
            upper = middle
    return lower, upper, original[0], original[1]


def seam_bracket() -> tuple[Q, Q]:
    lower, upper = Q(707, 1000), Q(708, 1000)
    for _index in range(SEAM_STEPS):
        middle = (lower + upper) / 2
        if 2 * middle * middle < 1:
            lower = middle
        else:
            upper = middle
    require(2 * lower * lower < 1 < 2 * upper * upper, "source seam")
    return lower, upper


def bisect_p(
    function: Callable[[Q, Q, Q], Any],
    t0: Q,
    t1: Q,
    p0: Q,
    p1: Q,
) -> tuple[Q, Q, str, str]:
    sl, su = strict_sign(function(t0, t1, p0)), strict_sign(
        function(t0, t1, p1)
    )
    require(sl != "UNRESOLVED" and su != "UNRESOLVED" and sl != su, "p root")
    original = sl, su
    for _index in range(SEAM_GRAPH_STEPS):
        middle = (p0 + p1) / 2
        sm = strict_sign(function(t0, t1, middle))
        require(sm != "UNRESOLVED", "p midpoint")
        if sm == sl:
            p0 = middle
        else:
            p1 = middle
    return p0, p1, original[0], original[1]


def split_box(box: Box, bit: str) -> Box:
    widths = (box.t1 - box.t0, box.p1 - box.p0, box.s1 - box.s0)
    axis = max(range(3), key=lambda index: (widths[index], -index))
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            Box(
                box.t0, middle, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "0",
            )
            if bit == "0"
            else Box(
                middle, box.t1, box.p0, box.p1, box.s0, box.s1,
                depth, box.path + "1",
            )
        )
    if axis == 1:
        middle = (box.p0 + box.p1) / 2
        return (
            Box(
                box.t0, box.t1, box.p0, middle, box.s0, box.s1,
                depth, box.path + "0",
            )
            if bit == "0"
            else Box(
                box.t0, box.t1, middle, box.p1, box.s0, box.s1,
                depth, box.path + "1",
            )
        )
    middle = (box.s0 + box.s1) / 2
    return (
        Box(
            box.t0, box.t1, box.p0, box.p1, box.s0, middle,
            depth, box.path + "0",
        )
        if bit == "0"
        else Box(
            box.t0, box.t1, box.p0, box.p1, middle, box.s1,
            depth, box.path + "1",
        )
    )


def decode_box(key: str) -> tuple[str, Box]:
    parts = key.split(":")
    require(len(parts) == 3, f"key:{key}")
    chart_id = f"{parts[0]}:{parts[1]}"
    encoded = parts[2]
    reflected = encoded.startswith("H.")
    direct = encoded[2:] if reflected else encoded
    pieces = direct.split(".")
    require(len(pieces) == 3, f"path:{key}")
    i, j, bits = int(pieces[0]), int(pieces[1]), pieces[2]
    t0 = atlas.T_LOWER + (
        atlas.T_UPPER - atlas.T_LOWER
    ) * Q(i, atlas.INITIAL_T)
    t1 = atlas.T_LOWER + (
        atlas.T_UPPER - atlas.T_LOWER
    ) * Q(i + 1, atlas.INITIAL_T)
    p0 = atlas.P_LOWER + (
        atlas.P_UPPER - atlas.P_LOWER
    ) * Q(j, atlas.INITIAL_P)
    p1 = atlas.P_LOWER + (
        atlas.P_UPPER - atlas.P_LOWER
    ) * Q(j + 1, atlas.INITIAL_P)
    box = Box(
        t0, t1, p0, p1, atlas.S_LOWER, atlas.S_UPPER, 0,
        f"{i:02d}.{j:02d}.",
    )
    for bit in bits:
        box = split_box(box, bit)
    if reflected:
        box = Box(
            box.t0, box.t1, -box.p1, -box.p0, box.s0, box.s1,
            box.depth, "H." + box.path,
        )
    require(box.path == encoded, f"decoded:{key}")
    return chart_id, box


def box_payload(box: Box) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
    }


def point_leaf(chart_id: str, box: Box, point: dict[str, str]) -> Any:
    t, p, s = Q(point["t"]), Q(point["p"]), Q(point["s"])
    candidate = atlas.AtlasBox(
        t, t, p, p, s, s, box.depth, box.path + ".verify-point"
    )
    return atlas.classify_box(chart_id, candidate)


def verify_witnesses(
    row: dict[str, Any],
    upstream: dict[str, Any],
    box: Box,
) -> None:
    require(
        row["strict_live_open_witness"] == upstream["strict_live_open_witness"]
        and row["strict_mismatch_open_witness"]
        == upstream["strict_mismatch_open_witness"],
        f"witness copy:{row['ambient_leaf_key']}",
    )
    live = row["strict_live_open_witness"]
    t, p, s = (
        Q(live["point"]["t"]),
        Q(live["point"]["p"]),
        Q(live["point"]["s"]),
    )
    require(
        box.t0 < t < box.t1
        and box.p0 < p < box.p1
        and box.s0 <= s <= box.s1
        and 2 * t * t < 1,
        f"live point:{row['ambient_leaf_key']}",
    )
    leaf = point_leaf(row["chart_id"], box, live["point"])
    require(
        leaf.classification == "unique_first"
        and leaf.owner_target == "W[1,0]",
        f"live replay:{row['ambient_leaf_key']}",
    )
    mismatch = row["strict_mismatch_open_witness"]
    t, p, s = (
        Q(mismatch["point"]["t"]),
        Q(mismatch["point"]["p"]),
        Q(mismatch["point"]["s"]),
    )
    require(
        box.t0 < t < box.t1
        and box.p0 < p < box.p1
        and box.s0 <= s <= box.s1
        and 2 * t * t < 1,
        f"mismatch point:{row['ambient_leaf_key']}",
    )


def verify_physical_partition(row: dict[str, Any], box: Box) -> None:
    key = row["ambient_leaf_key"]
    part = row["physical_source_chart_partition"]
    maximum = max(abs(box.t0), abs(box.t1))
    if key not in CROSS_KEYS:
        require(
            2 * maximum * maximum < 1
            and part["classification"]
            == "WHOLE_PARENT_STRICT_PHYSICAL_CHART_INTERIOR"
            and part["C_sign_on_parent"] == "STRICT_POSITIVE"
            and part["guard_outside_exterior_credit"] == 0
            and part["three_dimensional_open_strata"] == 1
            and part["two_dimensional_source_seam_strata"] == 0,
            f"interior partition:{key}",
        )
        return
    a0, a1 = seam_bracket()
    selected = (-a1, -a0) if box.t1 < 0 else (a0, a1)
    seam = part["algebraic_source_seam"]
    require(
        part["classification"]
        == "EXACT_PHYSICAL_INTERIOR_SEAM_GUARD_OUTSIDE_PARTITION"
        and seam["rational_isolating_bracket"]
        == [str(selected[0]), str(selected[1])]
        and seam["equation"] == "2*t^2=1"
        and seam["dimension"] == 2
        and seam["half_open_owner"] == "E"
        and part["guard_outside"]["exterior_exclusion_credit"] == 0
        and part["guard_outside"]["disposition"]
        == "CHART_REJECTION_REQUIRES_ADJACENT_RECOORDINATION",
        f"cross partition:{key}",
    )


def verify_clipping_and_intersections(
    row: dict[str, Any],
    upstream: dict[str, Any],
    box: Box,
) -> dict[str, int]:
    key = row["ambient_leaf_key"]
    owner = upstream["tangency_target_is_frozen_owner"]
    seam = (
        "NW"
        if upstream["outgoing_arrangement"]["relevant_seam"] == "H_NW"
        else "SW"
    )
    clipping = row["H_parent_face_clipping"]
    if owner:
        p_face = box.p0 if seam == "NW" else box.p1
        root = bisect_root(
            lambda a, b: reduced_h(a, b, p_face, seam),
            box.t0,
            box.t1,
        )
        require(
            clipping["classification"] == "UNIQUE_TRANSVERSE_H_CLIPPING_LINE"
            and clipping["p_face"] == str(p_face)
            and clipping["t_isolating_bracket"]
            == [str(root[0]), str(root[1])]
            and clipping["endpoint_signs"] == [root[2], root[3]]
            and clipping["dimension"] == 1
            and clipping["integer_credit"] == 0
            and strict_sign(
                reduced_h_t_derivative(box.t0, box.t1, p_face, seam)
            ) == "STRICT_NEGATIVE"
            and clipping["strict_t_derivative_sign_on_parent"]
            == "STRICT_NEGATIVE",
            f"H clipping:{key}",
        )
        clipped = 1
    else:
        require(
            clipping
            == {
                "classification": "NO_P_FACE_CLIPPING_FULL_BASE_GRAPH",
                "dimension": 0,
                "integer_credit": 0,
            },
            f"full H graph:{key}",
        )
        clipped = 0
    source = row["distinguished_intersections"]["source_seam_intersections"]
    if key in CROSS_KEYS:
        a0, a1 = seam_bracket()
        t0, t1 = (-a1, -a0) if box.t1 < 0 else (a0, a1)
        delta = bisect_p(reduced_delta, t0, t1, box.p0, box.p1)
        h = bisect_p(
            lambda a, b, p: reduced_h(a, b, p, seam),
            t0, t1, box.p0, box.p1,
        )
        require(
            source["source_seam_intersect_Delta"]["p_isolating_bracket"]
            == [str(delta[0]), str(delta[1])]
            and source["source_seam_intersect_Delta"]["endpoint_signs"]
            == [delta[2], delta[3]]
            and source["source_seam_intersect_Delta"]["dimension"] == 1
            and source["source_seam_intersect_H"]["p_isolating_bracket"]
            == [str(h[0]), str(h[1])]
            and source["source_seam_intersect_H"]["endpoint_signs"]
            == [h[2], h[3]]
            and source["source_seam_intersect_H"]["dimension"] == 1
            and source["source_seam_intersect_H"]["half_open_owner"] == "W"
            and source["source_seam_intersect_Delta_intersect_H"]["status"]
            == "EMPTY",
            f"source intersections:{key}",
        )
        if seam == "NW":
            require(h[1] < delta[0], f"NW graph order:{key}")
        else:
            require(delta[1] < h[0], f"SW graph order:{key}")
        source_count = 1
    else:
        require(source is None, f"unexpected source seam:{key}")
        source_count = 0
    return {"clipped": clipped, "source": source_count}


def verify_row(
    row: dict[str, Any],
    upstream: dict[str, Any],
) -> dict[str, int]:
    key = row["ambient_leaf_key"]
    require(
        row["row_sha256"] == digest({
            field: value for field, value in row.items()
            if field != "row_sha256"
        }),
        f"row digest:{key}",
    )
    chart_id, box = decode_box(key)
    require(
        row["chart_id"] == chart_id
        and row["atlas_path"] == box.path
        and row["parent_box"] == box_payload(box)
        and row["Round175_row_sha256"] == upstream["row_sha256"]
        and row["Round175_tangency_target"] == upstream["tangency_target"]
        and row["parent_classification"] == "MIXED_BOUNDED_RESIDUAL"
        and row["whole_parent_new_integer_exclusion"] is False,
        f"row identity:{key}",
    )
    verify_witnesses(row, upstream, box)
    verify_physical_partition(row, box)
    counts = verify_clipping_and_intersections(row, upstream, box)
    require(
        row["Delta_zero_graph"]["dimension"] == 2
        and row["Delta_zero_graph"]["base_coverage"] == "FULL_T_S_BASE"
        and row["Delta_zero_graph"]["integer_credit"] == 0
        and row["H_zero_graph"]["dimension"] == 2
        and row["H_zero_graph"]["strict_p_derivative_sign"]
        == "STRICT_NEGATIVE"
        and row["H_zero_graph"]["half_open_owner"] == "W"
        and row["H_zero_graph"]["integer_credit"] == 0
        and row["distinguished_intersections"]["Delta_intersect_H"]["status"]
        == "EMPTY_CERTIFIED_BY_ROUND175_AND_REPLAYED_ORDER"
        and row["later_frozen_prefix_processing"][
            "eligible_only_on_strict_collision1_live_open_stratum"
        ] is True
        and row["later_frozen_prefix_processing"][
            "collision2_or_later_exact_key_rows_materialized"
        ] == 0
        and row["later_frozen_prefix_processing"][
            "whole_parent_exclusion_impossible_due_to_strict_live_witness"
        ] is True
        and set(row["dimension_safe_credit"].values()) == {0},
        f"dimension safe row:{key}",
    )
    patterns = row["three_dimensional_sign_strata"]
    require(
        patterns["base_pattern_count"] == 3
        and len(patterns["base_analytic_sign_patterns"]) == 3
        and sum(
            item["frozen_prefix_disposition"] == "STRICT_COLLISION1_LIVE"
            for item in patterns["base_analytic_sign_patterns"]
        ) == 1
        and patterns["chart_domain_multiplier"]
        == (2 if key in CROSS_KEYS else 1)
        and patterns["connected_open_3D_stratum_count"]
        == (6 if key in CROSS_KEYS else 3),
        f"sign patterns:{key}",
    )
    return counts


def verify_certificate(envelope: dict[str, Any], chain: dict[str, Any]) -> None:
    require(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA
        and envelope["result_sha256"] == digest(envelope["result"])
        and envelope["result_sha256"] == EXPECTED_RESULT_SHA256,
        "certificate envelope/identity",
    )
    result = envelope["result"]
    expected_top = {
        "status",
        "parent_level_census",
        "exact_boundary_census",
        "exact_parent_rows_sha256",
        "exact_parent_keys_sha256",
        "exact_parent_keys",
        "exact_parent_rows",
        "source_chart_domain_contract",
        "later_prefix_bounded_ledger",
        "Round175_to_Round177_composition",
        "dimension_safe_noncredit",
        "strict_nonpromotion",
        "next_core_gate",
        "provenance",
    }
    require(set(result) == expected_top, "result exact keys")
    rows = result["exact_parent_rows"]
    keys = result["exact_parent_keys"]
    require(
        len(rows) == len(keys) == 16
        and keys == sorted(keys)
        and keys == [row["ambient_leaf_key"] for row in rows]
        and result["exact_parent_rows_sha256"] == digest(rows)
        and result["exact_parent_keys_sha256"] == digest(keys),
        "row/key registry",
    )
    upstream_rows = {
        row["ambient_leaf_key"]: row
        for row in chain["Round175"]["result"]["parent_arrangement_census"][
            "all_22_parent_rows"
        ]
        if row["classification"] == "MIXED_COMPOSITE"
    }
    require(set(keys) == set(upstream_rows), "upstream exact keys")
    totals = {"clipped": 0, "source": 0}
    for row in rows:
        counts = verify_row(row, upstream_rows[row["ambient_leaf_key"]])
        for key, value in counts.items():
            totals[key] += value
    require(totals == {"clipped": 14, "source": 2}, "replay totals")
    require(
        result["parent_level_census"]
        == {
            "input_Round175_mixed_parents": 16,
            "fully_excluded_parent_count": 0,
            "fully_live_parent_count": 0,
            "mixed_bounded_residual_parent_count": 16,
            "all_retain_strict_live_and_mismatch_open_witnesses": True,
            "new_whole_parent_exclusion_count": 0,
        },
        "parent census",
    )
    census = result["exact_boundary_census"]
    require(
        census["unique_transverse_H_parent_face_clipping_lines"] == 14
        and census["full_base_H_graphs_without_p_face_clipping"] == 2
        and census["physical_source_chart_cross_seam_parents"] == 2
        and census["source_seam_Delta_1D_intersections"] == 2
        and census["source_seam_H_1D_intersections"] == 2
        and census["source_seam_Delta_H_triple_points"] == 0
        and census["Delta_H_1D_intersections"] == 0
        and census["connected_open_3D_sign_strata"] == 54
        and census["Delta_2D_graph_pieces_after_source_seam_cut"] == 18
        and census["H_2D_graph_pieces_after_source_seam_cut"] == 18,
        "boundary census",
    )
    require(
        result["source_chart_domain_contract"][
            "guard_outside_is_chart_rejection_not_exterior_exclusion"
        ] is True
        and result["source_chart_domain_contract"][
            "guard_outside_integer_credit"
        ] == 0
        and result["source_chart_domain_contract"]["cross_seam_keys"]
        == list(CROSS_KEYS)
        and result["later_prefix_bounded_ledger"][
            "later_exact_key_rows_materialized"
        ] == 0
        and result["Round175_to_Round177_composition"][
            "conservation_identity"
        ] == "73178+3654=76832"
        and result["Round175_to_Round177_composition"][
            "Round177_new_whole_parent_excluded"
        ] == 0
        and set(result["dimension_safe_noncredit"].values()) == {0}
        and result["strict_nonpromotion"]
        == {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "global ledger/nonpromotion",
    )
    provenance = result["provenance"]
    require(
        provenance["schema"] == SCHEMA
        and provenance["producer_sha256"] == PRODUCER_SHA256
        and provenance["dependency_sha256"] == chain["dependency_sha256"]
        and provenance["Round175_files_modified"] is False
        and provenance["lower_dimensional_strata_promoted_to_integer_credit"]
        is False,
        "provenance",
    )


def semantic_attacks(
    certificate: dict[str, Any],
    chain: dict[str, Any],
) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []
    for index, row in enumerate(certificate["result"]["exact_parent_rows"]):
        key = row["ambient_leaf_key"]
        mutations.append((
            f"mixed-to-excluded:{key}",
            lambda value, i=index: value["result"]["exact_parent_rows"][i].__setitem__(
                "parent_classification", "FULLY_EXCLUDED"
            ),
        ))
        mutations.append((
            f"fake-whole-credit:{key}",
            lambda value, i=index: value["result"]["exact_parent_rows"][i].__setitem__(
                "whole_parent_new_integer_exclusion", True
            ),
        ))
    for index, row in enumerate(certificate["result"]["exact_parent_rows"]):
        if row["H_parent_face_clipping"]["classification"].startswith("UNIQUE"):
            key = row["ambient_leaf_key"]
            mutations.append((
                f"clipping-bracket:{key}",
                lambda value, i=index: value["result"]["exact_parent_rows"][i][
                    "H_parent_face_clipping"
                ]["t_isolating_bracket"].__setitem__(0, "0"),
            ))
    for cross_key in CROSS_KEYS:
        index = certificate["result"]["exact_parent_keys"].index(cross_key)
        mutations.append((
            f"source-owner:{cross_key}",
            lambda value, i=index: value["result"]["exact_parent_rows"][i][
                "physical_source_chart_partition"
            ]["algebraic_source_seam"].__setitem__("half_open_owner", "N"),
        ))
        mutations.append((
            f"guard-credit:{cross_key}",
            lambda value, i=index: value["result"]["exact_parent_rows"][i][
                "physical_source_chart_partition"
            ]["guard_outside"].__setitem__("exterior_exclusion_credit", 1),
        ))
    mutations.extend([
        (
            "parent census",
            lambda value: value["result"]["parent_level_census"].__setitem__(
                "fully_excluded_parent_count", 1
            ),
        ),
        (
            "open 3D census",
            lambda value: value["result"]["exact_boundary_census"].__setitem__(
                "connected_open_3D_sign_strata", 53
            ),
        ),
        (
            "later exact row",
            lambda value: value["result"]["later_prefix_bounded_ledger"].__setitem__(
                "later_exact_key_rows_materialized", 1
            ),
        ),
        (
            "ledger credit",
            lambda value: value["result"]["Round175_to_Round177_composition"].__setitem__(
                "Round177_new_whole_parent_excluded", 1
            ),
        ),
        (
            "D02 promotion",
            lambda value: value["result"]["strict_nonpromotion"].__setitem__(
                "D02", "PASS"
            ),
        ),
        (
            "extra nested key",
            lambda value: value["result"]["parent_level_census"].__setitem__(
                "forged", 0
            ),
        ),
        (
            "producer pin",
            lambda value: value["result"]["provenance"].__setitem__(
                "producer_sha256", "0" * 64
            ),
        ),
    ])
    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        candidate["result_sha256"] = digest(candidate["result"])
        try:
            verify_certificate(candidate, chain)
        except VerificationError:
            rejected.append(label)
    require(len(rejected) == len(mutations), "semantic attacks")
    return {
        "attack_count": len(mutations),
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_labels_sha256": digest([label for label, _mutation in mutations]),
        "all_candidates_resigned_at_result_envelope": True,
    }


def json_attacks(certificate: dict[str, Any]) -> dict[str, Any]:
    raw = canonical_bytes(certificate) + b"\n"
    attacks = [
        ("duplicate top", raw.replace(
            b'{"result":', b'{"result":{},"result":', 1
        )),
        ("duplicate nested", raw.replace(
            b'"D02":"BLOCKED"', b'"D02":"PASS","D02":"BLOCKED"', 1
        )),
        ("float", raw.replace(b'"input_Round175_mixed_parents":16',
                              b'"input_Round175_mixed_parents":16.0', 1)),
        ("exponent", raw.replace(b'"input_Round175_mixed_parents":16',
                                 b'"input_Round175_mixed_parents":1e1', 1)),
        ("NaN", raw.replace(b'"input_Round175_mixed_parents":16',
                            b'"input_Round175_mixed_parents":NaN', 1)),
        ("BOM", b"\xef\xbb\xbf" + raw),
        ("raw NUL", raw[:20] + b"\x00" + raw[20:]),
        ("invalid UTF8", raw[:20] + b"\xff" + raw[20:]),
        ("noncanonical whitespace", b" " + raw),
    ]
    rejected = 0
    for label, candidate in attacks:
        try:
            strict_parse(candidate, label)
        except VerificationError:
            rejected += 1
    require(rejected == len(attacks), "JSON attacks")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_rejected": True,
        "attack_labels_sha256": digest([label for label, _raw in attacks]),
    }


def safe_write(
    path: Path,
    data: bytes,
    allowed_parent: Path,
    protected: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == allowed_parent.resolve(), "outside output")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(st.st_nlink == 1, "output hardlink")
    require(path.resolve(strict=False) not in protected, "protected output")
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=allowed_parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def path_attacks() -> dict[str, Any]:
    labels: list[str] = []
    with tempfile.TemporaryDirectory(prefix="round177-path-") as directory:
        root = Path(directory)
        regular = root / "regular"
        regular.write_bytes(b"ok")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        oversized = root / "oversized"
        oversized.write_bytes(b"x" * 17)
        for label, path, maximum in (
            ("input symlink", symlink, 16),
            ("input hardlink", hardlink, 16),
            ("input oversized", oversized, 16),
        ):
            try:
                read_regular(path, maximum=maximum)
            except VerificationError:
                labels.append(label)
        output_symlink = root / "output-symlink"
        output_symlink.symlink_to(regular)
        output_hardlink = root / "output-hardlink"
        os.link(regular, output_hardlink)
        protected = root / "protected"
        protected.write_bytes(b"protected")
        outside = root.parent / f"{root.name}-outside"
        attacks = (
            ("output symlink", output_symlink, set()),
            ("output hardlink", output_hardlink, set()),
            ("protected alias", protected, {protected.resolve()}),
            ("outside output", outside, set()),
        )
        for label, path, protected_set in attacks:
            try:
                safe_write(path, b"x", root, protected_set)
            except VerificationError:
                labels.append(label)
        if outside.exists():
            outside.unlink()
    require(len(labels) == 7, "path attacks")
    return {
        "attack_count": 7,
        "rejected_count": 7,
        "all_rejected": True,
        "attack_labels_sha256": digest(labels),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    chain = dependency_check()
    certificate = strict_parse(
        read_regular(arguments.certificate),
        arguments.certificate.name,
    )
    verify_certificate(certificate, chain)
    semantics = semantic_attacks(certificate, chain)
    json_suite = json_attacks(certificate)
    path_suite = path_attacks()
    verifier_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": verifier_sha256,
        "independence_contract": {
            "Round177_producer_imported_or_executed": False,
            "Round175_producer_imported_or_executed": False,
            "sixteen_dyadic_parent_boxes_independently_decoded": True,
            "fourteen_H_clipping_roots_independently_reisolated": True,
            "two_algebraic_source_seams_independently_reisolated": True,
            "four_source_seam_graph_intersections_independently_reisolated":
                True,
            "all_live_witness_collision1_owners_replayed": True,
            "exact_row_and_key_digests_recomputed": True,
            "pinned_expected_certificate_result_identity": True,
        },
        "replay_census": {
            "parent_rows": 16,
            "fully_excluded": 0,
            "fully_live": 0,
            "mixed": 16,
            "H_clipping_roots": 14,
            "full_base_H_graphs": 2,
            "source_seams": 2,
            "source_seam_graph_intersections": 4,
            "Delta_H_intersections": 0,
            "open_3D_sign_strata": 54,
        },
        "semantic_mutation_attack_suite": semantics,
        "strict_json_attack_suite": json_suite,
        "path_safety_attack_suite": path_suite,
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {
        (HERE / name).resolve() for name in (*PINS, PRODUCER)
    }
    protected.add(Path(__file__).resolve())
    protected.add(arguments.certificate.resolve())
    safe_write(
        arguments.output,
        canonical_bytes(envelope) + b"\n",
        HERE,
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
