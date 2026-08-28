#!/usr/bin/env python3
"""Dimension-safe arrangement of the 22 Round172 tangency composites.

Whole-parent credit is issued only when every physical stratum misses the
frozen prefix.  Typed Δ and outgoing-H graphs, their possible intersections,
source-chart seams, and positive-volume atlas guard slices are never mixed
into the integer record ledger.
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
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
SCHEMA = "cm2.round175.dimension-safe-tangency-arrangement.v1"
MAX_INPUT_BYTES = 16 * 1024 * 1024
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING = "W"
CHARTS = ("W:E", "W:N", "W:S")
MAX_EXCEPTION_BASE_DEPTH = 8
BRACKET_STEPS = 24

ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
OWNERSHIP = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
R172_PRODUCER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning.py"
)
R172_CERT = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_certificate.json"
)
R172_VERIFIER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_verifier.py"
)
R172_VER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_verification.json"
)

PINS: dict[str, str] = {
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GE_SOURCE:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    OWNERSHIP:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    R172_PRODUCER:
        "81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980",
    R172_CERT:
        "3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c",
    R172_VERIFIER:
        "066f84d1517338774a8fc8132bd61006cabedbe7674129a433016fc16ddcad99",
    R172_VER:
        "d095ecdd1b59a6577f96f0317f8a30122e8cd3f6baf73ed550c5d227ed1811c3",
}

R172_RESULT = "a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776"
R172_VER_RESULT = "aa0fb2c28176cf46b058506658a21070679e0a91a4f94ed65245fb378e088603"

EXPECTED_FULLY_EXCLUDED_KEYS = (
    "W:E:01.12.1111010",
    "W:E:01.13.0101010",
    "W:E:03.07.01100",
    "W:E:04.08.10011",
    "W:E:06.02.1010101",
    "W:E:06.03.0000101",
)
EXPECTED_CROSS_SOURCE_SEAM_KEYS = (
    "W:E:00.15.0000000",
    "W:E:07.00.1111111",
)

REPLAY_CANDIDATE_IDS = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in CHARTS
}
REPLAY_TARGETS = {
    target.target_id: target for target in base.TARGETS
}


class ArrangementError(RuntimeError):
    """Fail-closed Round175 error."""


@dataclass(frozen=True)
class BaseCell:
    t0: Q
    t1: Q
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
        raise ArrangementError(label)


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_noninteger_number(value: str) -> None:
    raise ArrangementError(f"non-integer JSON number:{value}")


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str and "\x00" not in key, f"key:{path}")
            require(
                not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"surrogate key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"NUL string:{path}")
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"surrogate string:{path}",
        )


def read_regular(path: Path, expected_sha256: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"multiply linked:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected_sha256 is not None:
        require(sha256_bytes(data) == expected_sha256, f"pin:{path.name}")
    return data


def strict_json(data: bytes, label: str) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"raw NUL:{label}")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_noninteger_number,
            parse_constant=reject_noninteger_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArrangementError(f"invalid JSON:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"top object:{label}")
    return value


def load_envelope(name: str) -> dict[str, Any]:
    value = strict_json(read_regular(HERE / name, PINS[name]), name)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope keys:{name}",
    )
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{name}",
    )
    return value


def validate_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve()
        and Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve()
        and Path(atlas.ge.__file__).resolve() == (HERE / GE_SOURCE).resolve(),
        "module identities",
    )
    require(
        flint.__version__ == "0.9.0" and atlas.ctx.prec == 192,
        "python-flint environment",
    )
    for name in (
        ATLAS_SOURCE,
        BASE_SOURCE,
        GE_SOURCE,
        R172_PRODUCER,
        R172_VERIFIER,
    ):
        read_regular(HERE / name, PINS[name])
    ownership = strict_json(read_regular(HERE / OWNERSHIP, PINS[OWNERSHIP]), OWNERSHIP)
    require(
        ownership["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and ownership["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and ownership["verdict"]["rectangular_bulk_seam_quotient"]
        == "CERTIFIED"
        and ownership["result"]["scope_limits"][
            "ownership_rule_applies_to_analytic_strata"
        ] is True
        and ownership["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True
        and ownership["result"]["unique_half_open_owner_rule"][
            "diagonal_tie"
        ] == "E or W owns; N or S excludes",
        "analytic seam ownership",
    )
    r172 = load_envelope(R172_CERT)
    v172 = load_envelope(R172_VER)
    require(
        r172["schema"]
        == (
            "cm2.round172.dimension-safe-tangency-parent-"
            "frozen-owner-absence-pruning.v1"
        )
        and r172["result_sha256"] == R172_RESULT,
        "Round172 certificate",
    )
    vr = v172["result"]
    require(
        v172["result_sha256"] == R172_VER_RESULT
        and vr["status"] == "PASS"
        and vr["certificate_result_sha256"] == R172_RESULT
        and vr["producer_sha256"] == PINS[R172_PRODUCER]
        and vr["verifier_sha256"] == PINS[R172_VERIFIER]
        and vr["independence_contract"][
            "source_W_atlas_independently_replayed_at_192_bits"
        ] is True
        and vr["independence_contract"][
            "all_32_tangency_parents_reconstructed"
        ] is True
        and vr["independence_contract"][
            "full_expected_canonical_equality"
        ] is True
        and vr["semantic_mutation_attack_suite"]["all_rejected"] is True
        and vr["strict_json_attack_suite"]["all_rejected"] is True
        and vr["path_safety_attack_suite"]["all_rejected"] is True,
        "Round172 verification",
    )
    composition = r172["result"]["Round168_to_Round172_composition"]
    require(
        composition["refined_source_W_record_count"] == 76832
        and composition["combined_whole_record_excluded"] == 73172
        and composition["Round172_conservative_live"] == 3660
        and composition["live_components"]
        == {
            "Round165_seam_live_composites": 504,
            "Round166_owner_active_multi": 2616,
            "original_stage_one_match": 518,
            "remaining_tangency_parent_composites": 22,
        }
        and composition["conservation_identity"] == "73172+3660=76832",
        "Round172 composition",
    )
    return r172, ownership


def decode_parent_box(key: str) -> tuple[str, atlas.AtlasBox]:
    parts = key.split(":")
    require(len(parts) == 3, f"parent key:{key}")
    chart_id = f"{parts[0]}:{parts[1]}"
    encoded_path = parts[2]
    reflected = encoded_path.startswith("H.")
    direct_path = encoded_path[2:] if reflected else encoded_path
    pieces = direct_path.split(".")
    require(len(pieces) == 3, f"atlas path:{key}")
    i, j = int(pieces[0]), int(pieces[1])
    bits = pieces[2]
    require(
        0 <= i < atlas.INITIAL_T
        and 0 <= j < atlas.INITIAL_P
        and set(bits) <= {"0", "1"},
        f"atlas path registry:{key}",
    )
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
    box = atlas.AtlasBox(
        t0,
        t1,
        p0,
        p1,
        atlas.S_LOWER,
        atlas.S_UPPER,
        0,
        f"{i:02d}.{j:02d}.",
    )
    for bit in bits:
        box = atlas.ge.split(box)[int(bit)]
    if reflected:
        box = atlas.AtlasBox(
            box.t0,
            box.t1,
            -box.p1,
            -box.p0,
            box.s0,
            box.s1,
            box.depth,
            "H." + box.path,
        )
    require(box.path == encoded_path, f"decoded path:{key}")
    return chart_id, box


def replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    qx, qy, ux, uy, s, _cp = atlas.geometry(chart_id, box)
    rows: list[atlas.RootRecord] = []
    for target_id in REPLAY_CANDIDATE_IDS[chart_id]:
        target = REPLAY_TARGETS[target_id]
        center_x, center_y = base.target_center(target, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.arbq(base.RADIUS[target.obstacle])
        delta = radius * radius - transverse * transverse
        if bool(delta < 0):
            rows.append(atlas.RootRecord(
                target_id, "no_real_intersection", ell,
                delta, None, None, transverse,
            ))
            continue
        if not bool(delta > 0):
            rows.append(atlas.RootRecord(
                target_id, "unresolved_discriminant", ell,
                delta, None, None, transverse,
            ))
            continue
        radical = delta.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            classification = "intersection_behind"
        elif bool(near > 0):
            classification = "strict_future_root"
        else:
            classification = "unresolved_root_sign"
        rows.append(atlas.RootRecord(
            target_id, classification, ell,
            delta, near, far, transverse,
        ))
    return rows


def fixed_p_box(
    box: atlas.AtlasBox,
    p: Q,
    *,
    t0: Q | None = None,
    t1: Q | None = None,
    s0: Q | None = None,
    s1: Q | None = None,
) -> atlas.AtlasBox:
    return atlas.AtlasBox(
        box.t0 if t0 is None else t0,
        box.t1 if t1 is None else t1,
        p,
        p,
        box.s0 if s0 is None else s0,
        box.s1 if s1 is None else s1,
        box.depth,
        box.path,
    )


def target_delta(
    chart_id: str,
    box: atlas.AtlasBox,
    target_id: str,
) -> Any:
    return next(
        row.discriminant for row in replay_records(chart_id, box)
        if row.target_id == target_id
    )


def seam_value_and_derivative(
    chart_id: str,
    box: atlas.AtlasBox,
    seam: str,
) -> tuple[Any, Any]:
    qx, qy, ux, uy, s, cp = atlas.geometry(chart_id, box)
    radius = base.arbq(base.RADIUS["W"])
    half = base.arbq(Q(1, 2))
    nx = (qx - (half + s)) / radius
    ny = (qy - half) / radius
    inv_sqrt_two = 1 / arb(2).sqrt()
    mx = -inv_sqrt_two
    my = inv_sqrt_two if seam == "NW" else -inv_sqrt_two
    dx = arb(1) + radius * mx - radius * nx
    dy = radius * my - radius * ny
    h_value = ux * dy - uy * dx
    p = base.arb_interval(box.p0, box.p1)
    dux = -(p / cp) * nx - ny
    duy = -(p / cp) * ny + nx
    derivative = dux * dy - duy * dx
    return h_value, derivative


def strict_sign(value: Any) -> str:
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    if bool(value > 0):
        return "STRICT_POSITIVE"
    return "UNRESOLVED"


def source_chart_domain(box: atlas.AtlasBox, chart_id: str) -> dict[str, Any]:
    maximum_abs = max(abs(box.t0), abs(box.t1))
    minimum_abs = min(abs(box.t0), abs(box.t1))
    if box.t0 <= 0 <= box.t1:
        minimum_abs = Q(0)
    if 2 * maximum_abs * maximum_abs < 1:
        return {
            "classification": "STRICT_PHYSICAL_CHART_INTERIOR",
            "physical_chart_equation": "2*t^2<1",
            "source_chart_seam_present": False,
            "guard_outside_positive_volume_present": False,
            "guard_outside_exterior_exclusion_credit": 0,
        }
    require(
        2 * minimum_abs * minimum_abs < 1
        and 2 * maximum_abs * maximum_abs > 1
        and chart_id == "W:E",
        "supported source seam crossing",
    )
    return {
        "classification": "PHYSICAL_CHART_SEAM_AND_GUARD_OUTSIDE_COMPOSITE",
        "physical_chart_equation": "2*t^2=1",
        "source_chart_seam_present": True,
        "source_chart_seam_dimension": 2,
        "source_chart_seam_half_open_owner": "E",
        "physical_E_interior_positive_volume_present": True,
        "guard_outside_positive_volume_present": True,
        "guard_outside_disposition":
            "NEIGHBOR_CHART_RECOORDINATION_REQUIRED_NOT_EXTERIOR",
        "guard_outside_exterior_exclusion_credit": 0,
        "source_seam_intersection_strata": {
            "source_seam_intersect_Delta_nominal_dimension": 1,
            "source_seam_intersect_H_nominal_dimension": 1,
            "Delta_intersect_H_intersect_source_seam":
                "EMPTY_WHEN_DELTA_H_SEPARATION_APPLIES",
            "integer_exclusion_credit": 0,
        },
    }


def point_box(
    parent: atlas.AtlasBox,
    t: Q,
    p: Q,
    s: Q,
) -> atlas.AtlasBox:
    return atlas.AtlasBox(
        t, t, p, p, s, s,
        parent.depth, parent.path + ".round175-point",
    )


def first_hit(chart_id: str, point: atlas.AtlasBox) -> atlas.Leaf:
    original = atlas.records
    atlas.records = replay_records
    try:
        return atlas.classify_box(chart_id, point)
    finally:
        atlas.records = original


def rational_grid(lower: Q, upper: Q, denominator: int) -> list[Q]:
    return [
        lower + (upper - lower) * Q(index, denominator)
        for index in range(1, denominator)
    ]


def edge_adaptive_grid(lower: Q, upper: Q) -> list[Q]:
    fractions: list[Q] = [Q(1, 2)]
    for exponent in range(2, 16):
        denominator = 2 ** exponent
        fractions.extend((Q(1, denominator), Q(denominator - 1, denominator)))
    fractions.extend(Q(index, 32) for index in range(1, 32))
    unique = sorted(set(fractions))
    return [lower + (upper - lower) * fraction for fraction in unique]


def strict_point_witness(
    chart_id: str,
    parent: atlas.AtlasBox,
    tangency_target: str,
    want_live: bool,
) -> dict[str, Any]:
    t_values = edge_adaptive_grid(parent.t0, parent.t1)
    p_values = edge_adaptive_grid(parent.p0, parent.p1)
    s_values = [Q(0)]
    for t in t_values:
        if 2 * t * t >= 1:
            continue
        for s in s_values:
            for p in p_values:
                point = point_box(parent, t, p, s)
                records = replay_records(chart_id, point)
                frozen = next(
                    row for row in records
                    if row.target_id == FROZEN_OWNER
                )
                target = next(
                    row for row in records
                    if row.target_id == tangency_target
                )
                nw, _ = seam_value_and_derivative(chart_id, point, "NW")
                sw, _ = seam_value_and_derivative(chart_id, point, "SW")
                if want_live:
                    if not (
                        frozen.classification == "strict_future_root"
                        and bool(nw > 0)
                        and bool(sw < 0)
                    ):
                        continue
                    leaf = first_hit(chart_id, point)
                    if not (
                        leaf.classification == "unique_first"
                        and leaf.owner_target == FROZEN_OWNER
                    ):
                        continue
                    disposition = "STRICT_FROZEN_W_FIRST_OUTGOING_W_LIVE"
                else:
                    owner_graph = tangency_target == FROZEN_OWNER
                    if owner_graph:
                        if not (
                            frozen.classification == "no_real_intersection"
                            and bool(frozen.discriminant < 0)
                        ):
                            continue
                        leaf = first_hit(chart_id, point)
                        disposition = "STRICT_FROZEN_OWNER_ABSENT_MISMATCH"
                    else:
                        if not (
                            target.classification == "strict_future_root"
                        ):
                            continue
                        leaf = first_hit(chart_id, point)
                        if not (
                            leaf.classification == "unique_first"
                            and leaf.owner_target == tangency_target
                        ):
                            continue
                        disposition = "STRICT_MISMATCH_TARGET_FIRST"
                return {
                    "point": {"t": str(t), "p": str(p), "s": str(s)},
                    "source_physical_chart_interior": True,
                    "classification": disposition,
                    "first_hit_classification": leaf.classification,
                    "first_owner": leaf.owner_target,
                    "frozen_owner_record": frozen.classification,
                    "frozen_owner_discriminant_sign":
                        strict_sign(frozen.discriminant),
                    "tangency_target_record": target.classification,
                    "H_NW_sign": strict_sign(nw),
                    "H_SW_sign": strict_sign(sw),
                }
    raise ArrangementError(
        f"strict {'live' if want_live else 'mismatch'} witness:"
        f"{chart_id}:{parent.path}"
    )


def base_cell_box(
    parent: atlas.AtlasBox,
    cell: BaseCell,
    p: Q,
) -> atlas.AtlasBox:
    return fixed_p_box(
        parent,
        p,
        t0=cell.t0,
        t1=cell.t1,
        s0=cell.s0,
        s1=cell.s1,
    )


def split_base_cell(cell: BaseCell) -> tuple[BaseCell, BaseCell]:
    if cell.t1 - cell.t0 >= cell.s1 - cell.s0:
        middle = (cell.t0 + cell.t1) / 2
        return (
            BaseCell(
                cell.t0, middle, cell.s0, cell.s1,
                cell.depth + 1, cell.path + "0",
            ),
            BaseCell(
                middle, cell.t1, cell.s0, cell.s1,
                cell.depth + 1, cell.path + "1",
            ),
        )
    middle = (cell.s0 + cell.s1) / 2
    return (
        BaseCell(
            cell.t0, cell.t1, cell.s0, middle,
            cell.depth + 1, cell.path + "0",
        ),
        BaseCell(
            cell.t0, cell.t1, middle, cell.s1,
            cell.depth + 1, cell.path + "1",
        ),
    )


def bracket_graph(
    function: Callable[[BaseCell, Q], Any],
    cell: BaseCell,
    p0: Q,
    p1: Q,
) -> tuple[Q, Q] | None:
    sign0 = strict_sign(function(cell, p0))
    sign1 = strict_sign(function(cell, p1))
    if "UNRESOLVED" in (sign0, sign1) or sign0 == sign1:
        return None
    for _step in range(BRACKET_STEPS):
        middle = (p0 + p1) / 2
        middle_sign = strict_sign(function(cell, middle))
        if middle_sign == "UNRESOLVED":
            break
        if middle_sign == sign0:
            p0, sign0 = middle, middle_sign
        else:
            p1, sign1 = middle, middle_sign
    return p0, p1


def exception_graph_separation(
    chart_id: str,
    parent: atlas.AtlasBox,
    tangency_target: str,
    seam: str,
) -> list[dict[str, Any]]:
    initial = BaseCell(
        parent.t0, parent.t1, parent.s0, parent.s1, 0, ""
    )
    pending = [initial]
    terminal: list[dict[str, Any]] = []

    def delta_function(cell: BaseCell, p: Q) -> Any:
        return target_delta(
            chart_id,
            base_cell_box(parent, cell, p),
            tangency_target,
        )

    def h_function(cell: BaseCell, p: Q) -> Any:
        return seam_value_and_derivative(
            chart_id,
            base_cell_box(parent, cell, p),
            seam,
        )[0]

    while pending:
        cell = pending.pop()
        delta_bracket = bracket_graph(
            delta_function, cell, parent.p0, parent.p1
        )
        h_bracket = bracket_graph(
            h_function, cell, parent.p0, parent.p1
        )
        relation: str | None = None
        if delta_bracket is not None and h_bracket is not None:
            if h_bracket[1] < delta_bracket[0]:
                relation = "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH"
            elif delta_bracket[1] < h_bracket[0]:
                relation = "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH"
        if relation is None:
            require(
                cell.depth < MAX_EXCEPTION_BASE_DEPTH,
                "exception graph separation depth",
            )
            pending.extend(split_base_cell(cell))
            continue
        expected = (
            "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH"
            if chart_id == "W:N"
            else "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH"
        )
        require(relation == expected, "exception graph order")
        terminal.append(closed_row({
            "base_cell_path": cell.path,
            "base_cell_depth": cell.depth,
            "t": [str(cell.t0), str(cell.t1)],
            "s": [str(cell.s0), str(cell.s1)],
            "delta_graph_p_bracket": [
                str(delta_bracket[0]), str(delta_bracket[1])
            ],
            "H_graph_p_bracket": [
                str(h_bracket[0]), str(h_bracket[1])
            ],
            "strict_graph_order": relation,
            "H_graph_lies_in_mismatch_target_Delta_negative_side": True,
            "Delta_intersect_H": "EMPTY_ON_BASE_CELL",
        }))
    terminal.sort(key=lambda row: row["base_cell_path"])
    area = sum(
        (Q(row["t"][1]) - Q(row["t"][0]))
        * (Q(row["s"][1]) - Q(row["s"][0]))
        for row in terminal
    )
    require(
        area
        == (parent.t1 - parent.t0) * (parent.s1 - parent.s0),
        "exception base partition area",
    )
    return terminal


def parent_arrangement(
    upstream_row: dict[str, Any],
) -> dict[str, Any]:
    key = upstream_row["ambient_leaf_key"]
    chart_id, parent = decode_parent_box(key)
    tangency_target = upstream_row["Round164_tangency_target"]
    records = replay_records(chart_id, parent)
    tangency_record = next(
        row for row in records if row.target_id == tangency_target
    )
    require(
        atlas.physical_tangency_graph(
            chart_id, parent, tangency_record, records
        ),
        f"physical tangency graph:{key}",
    )
    domain = source_chart_domain(parent, chart_id)
    nw, nw_derivative = seam_value_and_derivative(chart_id, parent, "NW")
    sw, sw_derivative = seam_value_and_derivative(chart_id, parent, "SW")
    nw_sign, sw_sign = strict_sign(nw), strict_sign(sw)
    owner_graph = tangency_target == FROZEN_OWNER
    if sw_sign == "STRICT_NEGATIVE":
        relevant_seam, adjacent_chart = "H_NW", "N"
        relevant_value, relevant_derivative = nw, nw_derivative
        mismatch_sign, live_sign = "STRICT_NEGATIVE", "STRICT_POSITIVE"
        compatible_guard = "H_SW_STRICT_NEGATIVE"
    elif nw_sign == "STRICT_POSITIVE":
        relevant_seam, adjacent_chart = "H_SW", "S"
        relevant_value, relevant_derivative = sw, sw_derivative
        mismatch_sign, live_sign = "STRICT_POSITIVE", "STRICT_NEGATIVE"
        compatible_guard = "H_NW_STRICT_POSITIVE"
    else:
        raise ArrangementError(f"outgoing guard:{key}")
    require(
        strict_sign(relevant_derivative) == "STRICT_NEGATIVE",
        f"strict H derivative:{key}",
    )
    relevant_sign = strict_sign(relevant_value)
    exception_cells: list[dict[str, Any]] = []
    if owner_graph and relevant_sign == mismatch_sign:
        require(
            domain["classification"] == "STRICT_PHYSICAL_CHART_INTERIOR",
            f"full exclusion inside physical chart:{key}",
        )
        classification = "FULLY_EXCLUDED"
        live_witness = None
        mismatch_witness = None
        delta_h = {
            "status": "EMPTY_NO_H_ZERO_IN_PARENT",
            "nominal_dimension_if_nonempty": 1,
            "integer_credit": 0,
        }
        h_graph = {
            "present": False,
            "reason": f"{relevant_seam} is {relevant_sign} on whole parent",
        }
    else:
        require(
            relevant_sign == "UNRESOLVED",
            f"mixed seam interval:{key}",
        )
        classification = "MIXED_COMPOSITE"
        live_witness = strict_point_witness(
            chart_id, parent, tangency_target, True
        )
        mismatch_witness = strict_point_witness(
            chart_id, parent, tangency_target, False
        )
        h_graph = {
            "present": True,
            "kind": "UNIQUE_MONOTONE_CLIPPED_P_GRAPH",
            "equation": f"{relevant_seam}=0",
            "dimension": 2,
            "strict_p_derivative_sign": "STRICT_NEGATIVE",
            "half_open_owner": "W",
            "adjacent_excluded_chart": adjacent_chart,
            "boundary_clipping_or_grazing_nominal_dimension": 1,
            "boundary_component_count_fully_isolated": False,
            "boundary_integer_credit": 0,
        }
        if owner_graph:
            delta_h = {
                "status": "EMPTY_CERTIFIED",
                "nominal_dimension_if_nonempty": 1,
                "proof": (
                    "on H=0 the diagonal-contact chord has "
                    "|dot(D,m)|>1/sqrt(2)-2R_W>19/50, so Delta_W>0"
                ),
                "inverse_sqrt_two_rational_lower_bound": "7/10",
                "diagonal_contact_chord_dot_abs_lower_bound": "19/50",
                "H_graph_lies_strictly_in_Delta_positive_W_first_side":
                    True,
                "integer_credit": 0,
            }
        else:
            seam = "NW" if relevant_seam == "H_NW" else "SW"
            exception_cells = exception_graph_separation(
                chart_id, parent, tangency_target, seam
            )
            delta_h = {
                "status": "EMPTY_CERTIFIED_BY_ADAPTIVE_GRAPH_BRACKETS",
                "nominal_dimension_if_nonempty": 1,
                "terminal_base_cell_count": len(exception_cells),
                "maximum_extra_base_depth_used": max(
                    row["base_cell_depth"] for row in exception_cells
                ),
                "all_terminal_base_cells_sha256": digest(exception_cells),
                "all_terminal_base_cells": exception_cells,
                "H_graph_lies_strictly_in_mismatch_target_Delta_negative_side":
                    True,
                "integer_credit": 0,
            }
    arrangement = {
        "ambient_leaf_key": key,
        "chart_id": chart_id,
        "atlas_path": parent.path,
        "parent_box": {
            "t": [str(parent.t0), str(parent.t1)],
            "p": [str(parent.p0), str(parent.p1)],
            "s": [str(parent.s0), str(parent.s1)],
            "ambient_dimension": 3,
        },
        "Round172_resolution": upstream_row["resolution"],
        "tangency_target": tangency_target,
        "tangency_target_is_frozen_owner": owner_graph,
        "source_chart_domain": domain,
        "delta_arrangement": {
            "equation": f"Delta[{tangency_target}]=0",
            "strictly_monotone_p_graph": True,
            "delta_negative_open_side_dimension": 3,
            "delta_zero_graph_dimension": 2,
            "delta_positive_open_side_dimension": 3,
            "delta_zero_half_open_owner": (
                "W" if owner_graph else "MISMATCH_TARGET"
            ),
            "owner_graph_orientation": (
                {
                    "Delta_negative": "FROZEN_OWNER_ABSENT_MISMATCH",
                    "Delta_zero": "W_OWNED_TANGENCY_GRAPH",
                    "Delta_positive": "W_FIRST_SIDE",
                }
                if owner_graph
                else {
                    "Delta_negative":
                        "MISMATCH_TARGET_ABSENT_CONTAINS_FROZEN_W_LIVE_REGION",
                    "Delta_zero": "MISMATCH_TARGET_TANGENCY_GRAPH",
                    "Delta_positive": "MISMATCH_TARGET_FIRST_SIDE",
                }
            ),
        },
        "outgoing_arrangement": {
            "relevant_seam": relevant_seam,
            "adjacent_mismatch_chart": adjacent_chart,
            "compatible_guard": compatible_guard,
            "whole_parent_relevant_H_sign": relevant_sign,
            "mismatch_H_sign": mismatch_sign,
            "W_live_H_sign": live_sign,
            "H_graph": h_graph,
            "Delta_intersect_H": delta_h,
        },
        "strict_live_open_witness": live_witness,
        "strict_mismatch_open_witness": mismatch_witness,
        "classification": classification,
        "whole_parent_new_integer_exclusion":
            classification == "FULLY_EXCLUDED",
        "conservative_live_composite":
            classification == "MIXED_COMPOSITE",
        "analytic_internal_strata_added_to_integer_record_count": False,
        "guard_outside_or_residual_integer_credit": 0,
    }
    return closed_row(arrangement)


def build_result(producer_sha256: str) -> dict[str, Any]:
    r172, _ownership = validate_chain()
    upstream_rows = [
        row for row in r172["result"]["independent_192_bit_atlas_replay"][
            "all_32_parent_rows"
        ]
        if row["remaining_live_composite"]
    ]
    require(len(upstream_rows) == 22, "Round172 remaining parents")
    rows = [parent_arrangement(row) for row in upstream_rows]
    rows.sort(key=lambda row: row["ambient_leaf_key"])
    fully_excluded = [
        row for row in rows if row["classification"] == "FULLY_EXCLUDED"
    ]
    mixed = [
        row for row in rows if row["classification"] == "MIXED_COMPOSITE"
    ]
    fully_live = [
        row for row in rows if row["classification"] == "FULLY_LIVE"
    ]
    excluded_keys = tuple(
        row["ambient_leaf_key"] for row in fully_excluded
    )
    cross_keys = tuple(
        row["ambient_leaf_key"] for row in rows
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_OUTSIDE_COMPOSITE"
    )
    require(
        excluded_keys == EXPECTED_FULLY_EXCLUDED_KEYS,
        "exact six closures",
    )
    require(
        cross_keys == EXPECTED_CROSS_SOURCE_SEAM_KEYS,
        "exact source guard crossings",
    )
    require(
        len(fully_excluded) == 6
        and len(fully_live) == 0
        and len(mixed) == 16
        and len(rows) == 22,
        "6/0/16 parent census",
    )
    exception_rows = [
        row for row in rows
        if not row["tangency_target_is_frozen_owner"]
    ]
    require(
        len(exception_rows) == 2
        and all(
            row["outgoing_arrangement"]["Delta_intersect_H"]["status"]
            == "EMPTY_CERTIFIED_BY_ADAPTIVE_GRAPH_BRACKETS"
            for row in exception_rows
        ),
        "exception arrangements",
    )
    prior_excluded = 73172
    new_excluded = 6
    combined_excluded = prior_excluded + new_excluded
    live_components = {
        "original_stage_one_match": 518,
        "Round165_seam_live_composites": 504,
        "Round175_remaining_mixed_tangency_composites": 16,
        "Round166_owner_active_multi": 2616,
    }
    live_total = sum(live_components.values())
    require(
        combined_excluded == 73178
        and live_total == 3654
        and combined_excluded + live_total == 76832,
        "Round175 conservation",
    )
    return {
        "status": (
            "CERTIFIED_6_ADDITIONAL_WHOLE_TANGENCY_PARENT_EXCLUSIONS_"
            "WITH_16_EXACT_RESIDUAL_ARRANGEMENTS__D02_STILL_BLOCKED"
        ),
        "frozen_prefix": {
            "source_obstacle": "W",
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": FROZEN_OUTGOING,
            "stage_one_only": True,
        },
        "parent_arrangement_census": {
            "input_Round172_tangency_composites": 22,
            "fully_excluded_parent_count": len(fully_excluded),
            "fully_live_parent_count": len(fully_live),
            "mixed_composite_parent_count": len(mixed),
            "whole_parent_closure_count": len(fully_excluded),
            "exact_residual_arrangement_count": len(mixed),
            "frozen_owner_tangency_parent_count": 20,
            "mismatch_tangency_exception_parent_count": 2,
            "physical_source_chart_cross_seam_parent_count":
                len(cross_keys),
            "all_22_parent_rows_sha256": digest(rows),
            "all_22_parent_rows": rows,
        },
        "new_whole_parent_exclusion_credit": {
            "new_whole_parent_exclusion_count": new_excluded,
            "exact_parent_keys": list(excluded_keys),
            "exact_parent_keys_sha256": digest(list(excluded_keys)),
            "all_strata_mismatch_required": True,
            "all_six_strictly_inside_physical_source_chart": True,
            "credit_from_2D_graph_or_guard_slice": 0,
            "credited_parent_rows_sha256": digest(fully_excluded),
        },
        "residual_arrangement_ledger": {
            "mixed_parent_count": len(mixed),
            "mixed_parent_keys": [
                row["ambient_leaf_key"] for row in mixed
            ],
            "mixed_parent_keys_sha256": digest([
                row["ambient_leaf_key"] for row in mixed
            ]),
            "all_have_strict_live_and_mismatch_open_witnesses": True,
            "analytic_strata_not_added_to_integer_record_count": True,
            "source_chart_cross_seam_keys": list(cross_keys),
            "source_chart_cross_seam_keys_sha256": digest(list(cross_keys)),
            "source_chart_seam_equation": "2*t^2=1",
            "atlas_rational_guard_band": "[-177/250,177/250]",
            "guard_outside_is_chart_domain_rejection_not_exterior_exclusion":
                True,
            "guard_outside_integer_exclusion_credit": 0,
            "physical_diagonal_half_open_owner_rule":
                "E or W owns; N or S excludes",
            "all_live_H_seams_half_open_owned_by_W": True,
        },
        "Round172_to_Round175_composition": {
            "refined_source_W_record_count": 76832,
            "Round172_whole_record_excluded": prior_excluded,
            "Round175_new_whole_parent_excluded": new_excluded,
            "combined_whole_record_excluded": combined_excluded,
            "new_credit_disjoint_from_Round172_credit": True,
            "Round172_conservative_live": 3660,
            "Round175_conservative_live": live_total,
            "live_components": live_components,
            "conservation_identity": "73178+3654=76832",
            "refined_total_unchanged": True,
        },
        "dimension_safe_noncredit": {
            "Delta_zero_graph_whole_parent_credit": 0,
            "outgoing_H_zero_seam_whole_parent_credit": 0,
            "Delta_intersect_H_or_boundary_corner_integer_credit": 0,
            "source_chart_guard_outside_exterior_exclusion_credit": 0,
            "sixteen_mixed_internal_mismatch_strata_whole_parent_credit": 0,
            "Round165_typed_collar_mismatch_side_whole_record_credit": 0,
            "Round166_deep_refinement_profile_whole_record_credit": 0,
        },
        "scope": {
            "every_integer_credit_requires_all_physical_strata_mismatch":
                True,
            "physical_chart_seam_distinguished_from_rational_guard_band":
                True,
            "cross_seam_positive_volume_tubes_remain_residual": True,
            "not_later_frozen_prefix_resolution": True,
            "not_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "isolate the boundary-clipping and source-chart cross-seam "
            "residual strata in all 16 mixed tangency composites, continue "
            "later frozen-prefix processing only on certified live strata, "
            "continue the 224 whole-W rectangles, and resolve the 2,616 "
            "owner-active multi parents"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "arb_context_precision_bits": atlas.ctx.prec,
            "Round172_producer_or_verifier_imported_or_executed": False,
            "parent_boxes_reconstructed_from_pinned_dyadic_paths": True,
            "older_round_files_modified": False,
        },
    }


def safe_atomic_write(
    path: Path,
    data: bytes,
    protected: set[Path],
) -> None:
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
    producer_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(producer_sha256)
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
