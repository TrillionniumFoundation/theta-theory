#!/usr/bin/env python3
"""Round183 bounded face-bracket refinement of the Round181 residual.

The collision-2 residual is processed as a disjoint pipeline:

* root/Delta outers receive bounded dyadic face refinement;
* every resulting wall carrier receives two additional levels;
* every resulting outgoing-chart carrier receives four additional levels.

At terminal graph outers, nonzero derivatives certify regularity only.
Nonemptiness is recorded solely when strict opposite-sign rational boundary
witnesses are found.  All exact-key rows remain local 3D occurrences.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

import flint

import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round178_later_return_exact_key_bridge as r178
import cm2_round181_parametric_collision2_graph_arrangement as r181


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round183_residual_face_bracket_refinement_certificate.json"
SCHEMA = "cm2.round183.residual-face-bracket-refinement.v1"
MAX_INPUT_BYTES = 96 * 1024 * 1024
R181_PRODUCER = "cm2_round181_parametric_collision2_graph_arrangement.py"
R181_CERT = "cm2_round181_parametric_collision2_graph_arrangement_certificate.json"
R181_VERIFIER = "cm2_round181_parametric_collision2_graph_arrangement_verifier.py"
R181_VERIFICATION = "cm2_round181_parametric_collision2_graph_arrangement_verification.json"
R181_MANIFEST = "cm2_round181_parametric_collision2_graph_arrangement_manifest.sha256"
PINS = {
    R181_PRODUCER:
        "6e9d51229c209caacf3964d24600295375bd08e963b4e154774625707aa1524c",
    R181_CERT:
        "199e1793bf55062bf8ce26c7449aad4336896f3d312261f1c5c13efcdff41e77",
    R181_VERIFIER:
        "5a4e18ea095d2f41b02b20f65cb20f230f0e51de48e176e3d39d9606ddfddd73",
    R181_VERIFICATION:
        "5511bcf66035a49917ea407140a863bc7e898428498cdac8c385b1a9473f8cf1",
    R181_MANIFEST:
        "4a9c5bfa1e6dfe8e68c6260ecf9eaa77bab2f8c39e5012f152bdc84bcdf2e219",
}
R181_RESULT = "fec1dc3e2c7d5145a9b6663f70b59903b0791e6f26099001296399995213f21e"
R181_VERIFICATION_RESULT = (
    "4bab0cb1623371b122c67bb3f17a67a9d9a74a1d9a8d82aa0b430c2fa2d294a6"
)
ROOT_DEPTH = {
    "REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER": 4,
    "POINT_WINNER_NONSTRICT_ON_FULL_BOX_COLLAR": 4,
    "MULTI_MONOTONE_DELTA_GRAPH_ARRANGEMENT_OUTER": 6,
}
WALL_EXTRA_DEPTH = 2
OUTGOING_EXTRA_DEPTH = 4
CANDIDATES = r181.CANDIDATES


class Round183Error(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round183Error(label)


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["row_sha256"] = digest(result)
    return result


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise Round183Error(f"noninteger number:{value}")


def read_regular(path: Path, expected: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"hardlink:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
            f"encoding:{label}")
    value = json.loads(raw.decode("utf-8", "strict"),
                       object_pairs_hook=unique_pairs,
                       parse_float=reject_number,
                       parse_constant=reject_number)
    require(type(value) is dict, f"top:{label}")
    return value


def load_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    require(flint.__version__ == "0.9.0" and atlas.ctx.prec == 384, "flint")
    require(Path(r181.__file__).resolve() == (HERE / R181_PRODUCER).resolve(),
            "Round181 module")
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    certificate = strict_json(read_regular(HERE / R181_CERT, PINS[R181_CERT]),
                              R181_CERT)
    verification = strict_json(
        read_regular(HERE / R181_VERIFICATION, PINS[R181_VERIFICATION]),
        R181_VERIFICATION,
    )
    require(certificate["result_sha256"] == R181_RESULT and
            certificate["result_sha256"] == digest(certificate["result"]),
            "Round181 result")
    require(verification["result_sha256"] == R181_VERIFICATION_RESULT and
            verification["result_sha256"] == digest(verification["result"]) and
            verification["result"]["status"] == "PASS" and
            verification["result"]["full_expected_result_canonical_equality"],
            "Round181 verification")
    return certificate["result"], r181.load_chain()


def volume(box: atlas.AtlasBox) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def box_payload(box: atlas.AtlasBox) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "volume": str(volume(box)),
    }


def collision2_geometry(state: dict[str, Any]
                        ) -> tuple[Any, Any, Any, Any, Any]:
    return (state["contact_x"], state["contact_y"], state["outgoing_x"],
            state["outgoing_y"], state["s"])


def classify_box(
    parent_key: str,
    box: atlas.AtlasBox,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[str, dict[str, Any]]:
    state = r181.collision1_state_direct(parent_key, box)
    geometry = collision2_geometry(state)
    point_status, point_selected = r181.point_owner(parent_key, box)
    if point_status != "STRICT_UNIQUE_OWNER" or point_selected is None:
        return "POINT_OWNER_NOT_UNIQUE", {
            "point_owner_status": point_status,
        }
    incumbent = point_selected[0]
    incumbent_kind, incumbent_data = r178.root_record(*geometry, incumbent)
    if incumbent_kind != "STRICT_FUTURE" or incumbent_data is None:
        return "POINT_WINNER_NONSTRICT", {
            "point_owner": incumbent,
            "full_box_point_owner_root_kind": incumbent_kind,
        }
    active = []
    for candidate in CANDIDATES:
        if candidate == incumbent:
            continue
        kind, _data = r178.root_record(*geometry, candidate)
        if kind in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND",
                    "STRICT_FUTURE"}:
            continue
        raw = r181.raw_candidate(geometry, candidate)
        if bool(raw["ell"] + raw["radius"] < 0):
            continue
        if bool(incumbent_data["near"] < raw["ell"] - raw["radius"]):
            continue
        derivative = (
            2 * raw["transverse"] * raw["ell"] / state["cosine"]
        )
        active.append({
            "candidate": candidate,
            "root_kind": kind,
            "p1_derivative_sign":
                ">0" if bool(derivative > 0)
                else "<0" if bool(derivative < 0)
                else "UNRESOLVED",
        })
    if active:
        return f"ACTIVE_DELTA_{len(active)}", {
            "point_owner": incumbent,
            "active_candidates": active,
        }
    official, reason = r178.gate5_key(
        state, (incumbent, incumbent_data), pair_index, pattern_index
    )
    if official is None:
        return "WALL_ENDPOINT", {
            "point_owner": incumbent,
            "reason": reason,
        }
    next_state = r178.collision_state(
        geometry, (incumbent, incumbent_data)
    )
    outgoing = r178.strict_chart(
        next_state["normal_x"], next_state["normal_y"]
    )
    if outgoing is None:
        return "OUTGOING_H2", {
            "point_owner": incumbent,
            **official,
        }
    return "LOCAL_EXACT_KEY", {
        "point_owner": incumbent,
        **official,
        "collision2_outgoing_chart": outgoing,
    }


def point_state(parent_key: str, box: atlas.AtlasBox,
                t: Q, p: Q, s: Q) -> dict[str, Any]:
    point = atlas.AtlasBox(t, t, p, p, s, s, box.depth,
                           box.path + ".face-witness")
    return r181.collision1_state_direct(parent_key, point)


def corner_values(box: atlas.AtlasBox) -> list[tuple[Q, Q, Q]]:
    return list(itertools.product(
        (box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)
    ))


def opposite_pair(
    signed: list[tuple[tuple[Q, Q, Q], int, str | None]]
) -> dict[str, Any] | None:
    for left_index, left in enumerate(signed):
        for right in signed[left_index + 1:]:
            if left[1] * right[1] < 0:
                differing = sum(a != b for a, b in zip(left[0], right[0]))
                return {
                    "negative_point": {
                        "t": str(left[0][0]), "p": str(left[0][1]),
                        "s": str(left[0][2]),
                    } if left[1] < 0 else {
                        "t": str(right[0][0]), "p": str(right[0][1]),
                        "s": str(right[0][2]),
                    },
                    "positive_point": {
                        "t": str(left[0][0]), "p": str(left[0][1]),
                        "s": str(left[0][2]),
                    } if left[1] > 0 else {
                        "t": str(right[0][0]), "p": str(right[0][1]),
                        "s": str(right[0][2]),
                    },
                    "segment_kind":
                        "BOX_EDGE" if differing == 1 else "BOX_DIAGONAL",
                    "negative_side_chart_or_owner":
                        left[2] if left[1] < 0 else right[2],
                    "positive_side_chart_or_owner":
                        left[2] if left[1] > 0 else right[2],
                }
    return None


def delta_face_record(parent_key: str, box: atlas.AtlasBox,
                      candidate: str) -> dict[str, Any]:
    state = r181.collision1_state_direct(parent_key, box)
    raw = r181.raw_candidate(collision2_geometry(state), candidate)
    derivative = 2 * raw["transverse"] * raw["ell"] / state["cosine"]
    derivative_sign = (
        ">0" if bool(derivative > 0)
        else "<0" if bool(derivative < 0)
        else "UNRESOLVED"
    )
    signed = []
    for coordinates in corner_values(box):
        point = point_state(parent_key, box, *coordinates)
        geometry = collision2_geometry(point)
        delta = r181.raw_candidate(geometry, candidate)["Delta"]
        sign = 1 if bool(delta > 0) else -1 if bool(delta < 0) else 0
        status, selected = r178.select_owner(geometry, CANDIDATES)
        owner = selected[0] if (
            status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple)
        ) else None
        signed.append((coordinates, sign, owner))
    bracket = opposite_pair(signed)
    return {
        "candidate": candidate,
        "equation": f"Delta_{candidate}=0",
        "exact_regular_coordinate": "p1",
        "derivative_formula":
            "dDelta/dp1=2*eta_candidate*ell_candidate/sqrt(1-p1^2)",
        "strict_derivative_sign": derivative_sign,
        "regular_if_present": derivative_sign != "UNRESOLVED",
        "strict_opposite_sign_boundary_bracket": bracket,
        "nonempty_2D_graph_certified": (
            derivative_sign != "UNRESOLVED" and bracket is not None
        ),
        "scope":
            "nonzero derivative alone is not an existence certificate",
        "half_open_layering":
            "Delta<0 and Delta>0 are disjoint 3D sides; Delta=0 retained "
            "once as a 2D grazing carrier",
    }


def incumbent_face_record(parent_key: str, box: atlas.AtlasBox,
                          candidate: str) -> dict[str, Any]:
    record = delta_face_record(parent_key, box, candidate)
    record["role"] = "POINT_INCUMBENT_NOT_STRICT_ON_FULL_BOX"
    return record


def outgoing_face_record(parent_key: str, box: atlas.AtlasBox,
                         identifier: str) -> dict[str, Any]:
    signed = []
    for coordinates in corner_values(box):
        state = point_state(parent_key, box, *coordinates)
        geometry = collision2_geometry(state)
        kind, data = r178.root_record(*geometry, identifier)
        if kind != "STRICT_FUTURE" or data is None:
            signed.append((coordinates, 0, None))
            continue
        next_state = r178.collision_state(geometry, (identifier, data))
        value = (
            next_state["normal_x"] * next_state["normal_x"]
            - next_state["normal_y"] * next_state["normal_y"]
        )
        sign = 1 if bool(value > 0) else -1 if bool(value < 0) else 0
        chart = r178.strict_chart(
            next_state["normal_x"], next_state["normal_y"]
        )
        signed.append((coordinates, sign, chart))
    bracket = opposite_pair(signed)
    return {
        "equation": "H2=n2_x^2-n2_y^2=0",
        "local_phase_formula": "H2=1-2*t2^2",
        "local_phase_derivative": "dH2/dt2=-4*t2",
        "derivative_nonzero_on_H2_zero": True,
        "strict_opposite_sign_boundary_bracket": bracket,
        "nonempty_2D_graph_certified": bracket is not None,
        "H2_positive_side": "E or W according to sign(n2_x)",
        "H2_negative_side": "N or S according to sign(n2_y)",
        "H2_zero_half_open_owner": "E or W owns; N or S excludes",
        "integer_or_global_credit": 0,
    }


def wall_face_record(parent_key: str, box: atlas.AtlasBox,
                     identifier: str) -> dict[str, Any]:
    state = r181.collision1_state_direct(parent_key, box)
    geometry = collision2_geometry(state)
    kind, data = r178.root_record(*geometry, identifier)
    require(kind == "STRICT_FUTURE" and data is not None, "wall owner root")
    hit_y = state["contact_y"] + data["near"] * state["outgoing_y"]
    integers = [value for value in range(-8, 9)
                if not bool(hit_y < value) and not bool(hit_y > value)]
    signed_by_integer = []
    for integer in integers:
        signed = []
        for coordinates in corner_values(box):
            point = point_state(parent_key, box, *coordinates)
            point_geometry = collision2_geometry(point)
            point_kind, point_data = r178.root_record(
                *point_geometry, identifier
            )
            if point_kind != "STRICT_FUTURE" or point_data is None:
                signed.append((coordinates, 0, None))
                continue
            point_hit_y = (
                point["contact_y"]
                + point_data["near"] * point["outgoing_y"]
            )
            difference = point_hit_y - integer
            sign = (
                1 if bool(difference > 0)
                else -1 if bool(difference < 0)
                else 0
            )
            signed.append((coordinates, sign, None))
        signed_by_integer.append({
            "integer_wall": integer,
            "strict_opposite_sign_boundary_bracket": opposite_pair(signed),
        })
    return {
        "equations": [f"hit_y-{value}=0" for value in integers],
        "face_brackets": signed_by_integer,
        "pullback_Jacobian_nonzero": False,
        "nonempty_regular_2D_graph_certified": False,
        "half_open_word_owner":
            "endpoint equality retained separately until Jacobian and both "
            "official side words are closed",
        "integer_or_global_credit": 0,
    }


def terminal_row(
    item: dict[str, Any],
    stage: str,
    stage_extra_depth: int,
    status: str,
    detail: dict[str, Any],
) -> dict[str, Any]:
    box = item["box"]
    face: dict[str, Any] | None = None
    if status.startswith("ACTIVE_DELTA_"):
        face = {
            "candidate_graphs": [
                delta_face_record(
                    item["parent_key"], box, row["candidate"]
                )
                for row in detail["active_candidates"]
            ]
        }
    elif status == "POINT_WINNER_NONSTRICT":
        face = {
            "incumbent_graph": incumbent_face_record(
                item["parent_key"], box, detail["point_owner"]
            )
        }
    elif status == "OUTGOING_H2":
        face = {
            "outgoing_graph": outgoing_face_record(
                item["parent_key"], box, detail["point_owner"]
            )
        }
    elif status == "WALL_ENDPOINT":
        face = {
            "wall_graph": wall_face_record(
                item["parent_key"], box, detail["point_owner"]
            )
        }
    return closed_row({
        "origin_status": item["origin_status"],
        "origin_parent_key": item["parent_key"],
        "origin_terminal_path": item["origin_path"],
        "terminal_path": box.path,
        "stage": stage,
        "stage_extra_depth": stage_extra_depth,
        "box": box_payload(box),
        "status": status,
        "detail": detail,
        "face_bracket_or_graph_record": face,
        "local_exact_key_is_global_disposition": False,
        "whole_parent_or_stratum_credit": 0,
    })


def split_item(item: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    left, right = ge.split(item["box"])
    first, second = dict(item), dict(item)
    first["box"], second["box"] = left, right
    return first, second


def root_refinement(
    inputs: list[dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]], list[dict[str, Any]]]:
    exact_rows, wall_queue, outgoing_queue, residual_rows = [], [], [], []
    for initial in inputs:
        maximum = ROOT_DEPTH[initial["origin_status"]]
        pending = [(initial, 0)]
        while pending:
            item, depth = pending.pop()
            status, detail = classify_box(
                item["parent_key"], item["box"], pair_index, pattern_index
            )
            refinable = (
                status in {"POINT_OWNER_NOT_UNIQUE", "POINT_WINNER_NONSTRICT"}
                or status.startswith("ACTIVE_DELTA_")
            )
            if refinable and depth < maximum:
                left, right = split_item(item)
                pending.extend(((right, depth + 1), (left, depth + 1)))
                continue
            if status == "LOCAL_EXACT_KEY":
                exact_rows.append(terminal_row(
                    item, "ROOT_FACE_REFINEMENT", depth, status, detail
                ))
            elif status == "WALL_ENDPOINT":
                next_item = dict(item)
                next_item["root_stage_depth"] = depth
                wall_queue.append(next_item)
            elif status == "OUTGOING_H2":
                next_item = dict(item)
                next_item["root_stage_depth"] = depth
                outgoing_queue.append(next_item)
            else:
                residual_rows.append(terminal_row(
                    item, "ROOT_FACE_REFINEMENT", depth, status, detail
                ))
    return exact_rows, wall_queue, outgoing_queue, residual_rows


def wall_refinement(
    inputs: list[dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]]]:
    exact_rows, outgoing_queue, residual_rows = [], [], []
    for initial in inputs:
        pending = [(initial, 0)]
        while pending:
            item, depth = pending.pop()
            status, detail = classify_box(
                item["parent_key"], item["box"], pair_index, pattern_index
            )
            if status == "WALL_ENDPOINT" and depth < WALL_EXTRA_DEPTH:
                left, right = split_item(item)
                pending.extend(((right, depth + 1), (left, depth + 1)))
                continue
            if status == "LOCAL_EXACT_KEY":
                exact_rows.append(terminal_row(
                    item, "WALL_FACE_REFINEMENT", depth, status, detail
                ))
            elif status == "OUTGOING_H2":
                next_item = dict(item)
                next_item["wall_stage_depth"] = depth
                outgoing_queue.append(next_item)
            else:
                residual_rows.append(terminal_row(
                    item, "WALL_FACE_REFINEMENT", depth, status, detail
                ))
    return exact_rows, outgoing_queue, residual_rows


def outgoing_refinement(
    inputs: list[dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    exact_rows, residual_rows = [], []
    for initial in inputs:
        pending = [(initial, 0)]
        while pending:
            item, depth = pending.pop()
            status, detail = classify_box(
                item["parent_key"], item["box"], pair_index, pattern_index
            )
            if status == "OUTGOING_H2" and depth < OUTGOING_EXTRA_DEPTH:
                left, right = split_item(item)
                pending.extend(((right, depth + 1), (left, depth + 1)))
                continue
            if status == "LOCAL_EXACT_KEY":
                exact_rows.append(terminal_row(
                    item, "OUTGOING_FACE_REFINEMENT", depth, status, detail
                ))
            else:
                residual_rows.append(terminal_row(
                    item, "OUTGOING_FACE_REFINEMENT", depth, status, detail
                ))
    return exact_rows, residual_rows


def fraction_map(values: dict[str, Q]) -> dict[str, str]:
    return {key: str(value) for key, value in sorted(values.items())}


def build_result(producer_sha256: str) -> dict[str, Any]:
    upstream181, upstream178 = load_chain()
    pair_index, pattern_index, registry_digest = registry.key_index_tables()
    require(registry_digest == r178.GATE5_REGISTRY_DIGEST, "registry")
    round178_rows = upstream178["bounded_full_parent_3D_ledger"]["terminal_rows"]
    lookup = {
        (row["parent_key"], row["terminal_path"]): row
        for row in round178_rows
    }
    arrangement_rows = upstream181[
        "collision2_root_order_arrangement"
    ]["arrangement_rows"]
    root_inputs = []
    for row in arrangement_rows:
        if row["status"] in ROOT_DEPTH:
            source = lookup[(row["parent_key"], row["terminal_path"])]
            root_inputs.append({
                "origin_status": row["status"],
                "origin_path": row["terminal_path"],
                "parent_key": row["parent_key"],
                "box": r181.box_from_row(source),
            })
    require(Counter(item["origin_status"] for item in root_inputs) == {
        "REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER": 584,
        "POINT_WINNER_NONSTRICT_ON_FULL_BOX_COLLAR": 1396,
        "MULTI_MONOTONE_DELTA_GRAPH_ARRANGEMENT_OUTER": 6,
    }, "root inputs")
    original_wall_inputs = []
    for row in upstream181["collision2_wall_graph_arrangement"]["rows"]:
        source = lookup[(row["parent_key"], row["terminal_path"])]
        original_wall_inputs.append({
            "origin_status": "ROUND181_WALL_ENDPOINT_OUTER",
            "origin_path": row["terminal_path"],
            "parent_key": row["parent_key"],
            "box": r181.box_from_row(source),
        })
    original_outgoing_inputs = []
    for row in arrangement_rows:
        if row["status"] == "ROOT_ORDER_RESOLVED__OUTGOING_CHART_GRAPH_COLLAR":
            source = lookup[(row["parent_key"], row["terminal_path"])]
            original_outgoing_inputs.append({
                "origin_status": "ROUND181_OUTGOING_H2_OUTER",
                "origin_path": row["terminal_path"],
                "parent_key": row["parent_key"],
                "box": r181.box_from_row(source),
            })
    require(len(original_wall_inputs) == 168 and
            len(original_outgoing_inputs) == 1128, "wall/outgoing inputs")
    dynamic_inputs = (
        root_inputs + original_wall_inputs + original_outgoing_inputs
    )
    dynamic_input_volume = sum(volume(item["box"]) for item in dynamic_inputs)
    root_exact, root_walls, root_outgoing, root_residual = root_refinement(
        root_inputs, pair_index, pattern_index
    )
    wall_exact, wall_outgoing, wall_residual = wall_refinement(
        original_wall_inputs + root_walls, pair_index, pattern_index
    )
    outgoing_exact, outgoing_residual = outgoing_refinement(
        original_outgoing_inputs + root_outgoing + wall_outgoing,
        pair_index, pattern_index
    )
    exact_rows = sorted(
        root_exact + wall_exact + outgoing_exact,
        key=lambda row: (
            row["origin_parent_key"], row["terminal_path"], row["stage"]
        ),
    )
    residual_rows = sorted(
        root_residual + wall_residual + outgoing_residual,
        key=lambda row: (
            row["origin_parent_key"], row["terminal_path"], row["stage"]
        ),
    )
    output_volume = sum(
        Q(row["box"]["volume"]) for row in exact_rows + residual_rows
    )
    require(output_volume == dynamic_input_volume, "dynamic volume")
    exact_volume = sum(Q(row["box"]["volume"]) for row in exact_rows)
    dynamic_residual_volume = sum(
        Q(row["box"]["volume"]) for row in residual_rows
    )
    exact_counts = Counter(row["stage"] for row in exact_rows)
    residual_counts = Counter(row["status"] for row in residual_rows)
    residual_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    for row in residual_rows:
        residual_volumes[row["status"]] += Q(row["box"]["volume"])
    exact_key_ids = sorted({
        row["detail"]["official_gate5_key"]["word_key_id"]
        for row in exact_rows
    })
    exact_ordinals = sorted({
        row["detail"]["official_gate5_key"]["ordinal_zero_based"]
        for row in exact_rows
    })
    phase_statuses = {
        "COLLISION1_DELTA_ROOT_COLLAR",
        "COLLISION1_OUTGOING_CHART_COLLAR",
        "COLLISION1_ROOT_ORDER_COLLAR",
        "SOURCE_CHART_SEAM_COLLAR",
    }
    phase_rows = [
        {
            "parent_key": row["parent_key"],
            "terminal_path": row["terminal_path"],
            "status": row["status"],
            "box_volume": row["box"]["volume"],
        }
        for row in round178_rows if row["status"] in phase_statuses
    ]
    phase_counts = Counter(row["status"] for row in phase_rows)
    phase_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    for row in phase_rows:
        phase_volumes[row["status"]] += Q(row["box_volume"])
    require(phase_counts == {
        "COLLISION1_DELTA_ROOT_COLLAR": 276,
        "COLLISION1_OUTGOING_CHART_COLLAR": 172,
        "COLLISION1_ROOT_ORDER_COLLAR": 50,
        "SOURCE_CHART_SEAM_COLLAR": 32,
    }, "phase replay")
    total_input_volume = dynamic_input_volume + sum(phase_volumes.values())
    require(
        total_input_volume == Q(
            upstream181["exact_residual_census"][
                "residual_exact_coordinate_outer_volume"
            ]
        ),
        "Round181 residual volume",
    )
    total_residual_volume = (
        dynamic_residual_volume + sum(phase_volumes.values())
    )
    nominal_graphs = 0
    certified_graphs = 0
    nominal_pair_outers = 0
    certified_edge_brackets = 0
    certified_diagonal_brackets = 0
    outgoing_graphs = 0
    wall_graphs = 0
    for row in residual_rows:
        face = row["face_bracket_or_graph_record"]
        if not face:
            continue
        if "candidate_graphs" in face:
            graphs = face["candidate_graphs"]
            nominal_graphs += len(graphs)
            certified_graphs += sum(
                graph["nonempty_2D_graph_certified"] for graph in graphs
            )
            nominal_pair_outers += math.comb(len(graphs), 2)
            for graph in graphs:
                bracket = graph["strict_opposite_sign_boundary_bracket"]
                if bracket is not None:
                    if bracket["segment_kind"] == "BOX_EDGE":
                        certified_edge_brackets += 1
                    else:
                        certified_diagonal_brackets += 1
        elif "incumbent_graph" in face:
            graph = face["incumbent_graph"]
            nominal_graphs += 1
            certified_graphs += graph["nonempty_2D_graph_certified"]
            bracket = graph["strict_opposite_sign_boundary_bracket"]
            if bracket is not None:
                if bracket["segment_kind"] == "BOX_EDGE":
                    certified_edge_brackets += 1
                else:
                    certified_diagonal_brackets += 1
        elif "outgoing_graph" in face:
            outgoing_graphs += 1
            graph = face["outgoing_graph"]
            certified_graphs += graph["nonempty_2D_graph_certified"]
            bracket = graph["strict_opposite_sign_boundary_bracket"]
            if bracket is not None:
                if bracket["segment_kind"] == "BOX_EDGE":
                    certified_edge_brackets += 1
                else:
                    certified_diagonal_brackets += 1
        elif "wall_graph" in face:
            wall_graphs += 1
    combined_nominal_graphs = nominal_graphs + outgoing_graphs + wall_graphs
    per_parent_exact = Counter(
        row["origin_parent_key"] for row in exact_rows
    )
    parent_rows = []
    for row in upstream181["per_parent_partial_ledger"]["rows"]:
        key = row["parent_key"]
        parent_rows.append(closed_row({
            "parent_key": key,
            "Round181_combined_strict_inner_box_count":
                row["combined_strict_inner_box_count"],
            "Round183_new_local_exact_key_box_count":
                per_parent_exact[key],
            "combined_local_exact_key_box_count":
                row["combined_strict_inner_box_count"]
                + per_parent_exact[key],
            "complete_collision2_live_stratum_closed": False,
            "status": "PARTIAL",
            "whole_parent_or_stratum_credit": 0,
        }))
    first_residual = residual_rows[0] if residual_rows else None
    return {
        "status": (
            "PARTIAL_BOUNDED_FACE_BRACKET_RESIDUAL_REFINEMENT__"
            "NO_GLOBAL_DISPOSITION"
        ),
        "Round181_binding": {
            "certificate_result_sha256": R181_RESULT,
            "verification_result_sha256": R181_VERIFICATION_RESULT,
            "input_residual_parent_box_count": 3812,
            "input_residual_exact_coordinate_outer_volume":
                upstream181["exact_residual_census"][
                    "residual_exact_coordinate_outer_volume"
                ],
            "Round181_files_modified": False,
        },
        "bounded_refinement_contract": {
            "root_extra_depth_by_origin": dict(sorted(ROOT_DEPTH.items())),
            "wall_extra_depth": WALL_EXTRA_DEPTH,
            "outgoing_extra_depth": OUTGOING_EXTRA_DEPTH,
            "root_then_wall_then_outgoing_pipeline_is_disjoint": True,
            "nonzero_derivative_alone_certifies_existence": False,
            "graph_nonemptiness_requires_strict_opposite_sign_boundary_bracket":
                True,
            "pairwise_Krawczyk_incidence_promoted_without_contraction": False,
        },
        "dynamic_input_ledger": {
            "root_input_count": len(root_inputs),
            "wall_input_count": len(original_wall_inputs),
            "outgoing_input_count": len(original_outgoing_inputs),
            "dynamic_input_count": len(dynamic_inputs),
            "dynamic_input_exact_volume": str(dynamic_input_volume),
        },
        "new_local_exact_key_ledger": {
            "row_count": len(exact_rows),
            "rows_sha256": digest(exact_rows),
            "rows": exact_rows,
            "stage_counts": dict(sorted(exact_counts.items())),
            "exact_coordinate_volume": str(exact_volume),
            "local_gate5_key_ids": exact_key_ids,
            "local_gate5_ordinals_zero_based": exact_ordinals,
            "global_Gate5_dispositions": 0,
            "whole_parent_or_stratum_credit": 0,
        },
        "dynamic_residual_ledger": {
            "row_count": len(residual_rows),
            "rows_sha256": digest(residual_rows),
            "rows": residual_rows,
            "status_counts": dict(sorted(residual_counts.items())),
            "status_volumes": fraction_map(residual_volumes),
            "exact_coordinate_volume": str(dynamic_residual_volume),
            "exact_conservation":
                f"{exact_volume}+{dynamic_residual_volume}={dynamic_input_volume}",
        },
        "face_bracket_dimension_ledger": {
            "nominal_candidate_or_incumbent_2D_graph_carriers":
                nominal_graphs,
            "nominal_outgoing_H2_2D_graph_carriers": outgoing_graphs,
            "nominal_wall_2D_graph_carriers": wall_graphs,
            "combined_nominal_2D_graph_carriers": combined_nominal_graphs,
            "certified_nonempty_regular_2D_graph_carriers":
                certified_graphs,
            "strict_edge_brackets": certified_edge_brackets,
            "strict_diagonal_brackets": certified_diagonal_brackets,
            "nominal_pairwise_1D_incidence_outers":
                nominal_pair_outers,
            "certified_unique_pairwise_1D_incidences": 0,
            "certified_0D_multiple_incidence_points": 0,
            "half_open_rule":
                "strict sides are disjoint; every equality carrier is "
                "retained once in its own dimension",
            "two_or_one_or_zero_dimensional_integer_credit": 0,
        },
        "inherited_collision1_and_source_seam_replay": {
            "row_count": len(phase_rows),
            "rows_sha256": digest(phase_rows),
            "status_counts": dict(sorted(phase_counts.items())),
            "status_volumes": fraction_map(phase_volumes),
            "guard_rechart_rows_sha256":
                upstream178["guard_adjacent_chart_recoordinates"][
                    "rows_sha256"
                ],
            "source_seam_2D_half_open_owner": "E",
            "adjacent_N_or_S_representation_excluded": True,
            "one_dimensional_Delta_or_H_intersections_counted_once": 4,
            "new_integer_credit": 0,
        },
        "exact_residual_census": {
            "Round181_input_parent_box_count": 3812,
            "Round181_input_exact_coordinate_outer_volume":
                str(total_input_volume),
            "Round183_new_local_exact_key_box_count": len(exact_rows),
            "Round183_new_local_exact_key_volume": str(exact_volume),
            "dynamic_residual_terminal_box_count": len(residual_rows),
            "inherited_collision1_or_source_carrier_box_count":
                len(phase_rows),
            "combined_residual_box_count":
                len(residual_rows) + len(phase_rows),
            "combined_residual_exact_coordinate_outer_volume":
                str(total_residual_volume),
            "integer_census_delta": 0,
        },
        "per_parent_partial_ledger": {
            "parent_count": len(parent_rows),
            "rows_sha256": digest(parent_rows),
            "rows": parent_rows,
            "collision2_fully_closed_live_strata": 0,
            "collision2_partial_live_strata": 16,
            "whole_parent_or_stratum_promotions": 0,
        },
        "first_analytic_hard_blocker": {
            "first_residual_status":
                first_residual["status"] if first_residual else None,
            "first_residual_parent_key":
                first_residual["origin_parent_key"] if first_residual else None,
            "first_residual_terminal_path":
                first_residual["terminal_path"] if first_residual else None,
            "reason": (
                "bounded face refinement leaves graph tubes without a "
                "uniform interval-Newton/Krawczyk contraction; nominal "
                "pairwise incidences therefore remain outers"
            ),
        },
        "strict_nonpromotion": {
            "all_new_exact_keys_are_local_strict_3D_boxes": True,
            "observed_point_289591_global_disposition": 0,
            "inner_or_refined_box_290575_global_disposition": 0,
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "uniform interval-Newton contractions on the remaining "
            "candidate/incumbent and H2 graph tubes, coupled Krawczyk on "
            "pairwise incidences, then collision1/source-seam carriers"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": atlas.ctx.prec,
            "Round181_files_modified": False,
        },
    }


def safe_write(path: Path, data: bytes) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == HERE, "output directory")
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    require(absolute.resolve(strict=False) not in protected, "protected output")
    if absolute.exists() or absolute.is_symlink():
        st = absolute.lstat()
        require(stat.S_ISREG(st.st_mode) and not absolute.is_symlink()
                and st.st_nlink == 1, "output type")
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.", suffix=".tmp", dir=absolute.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
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
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
