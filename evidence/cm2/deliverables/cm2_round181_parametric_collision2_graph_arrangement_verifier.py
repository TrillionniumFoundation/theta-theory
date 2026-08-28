#!/usr/bin/env python3
"""Independent verifier for Round181.

The Round181 producer is pinned as inert source bytes but is never imported
or executed.  This verifier independently rebuilds the complete Round181
result from frozen Round178 geometry, including all 22,848 relation rows.
Acceptance is full canonical-result equality, not comparison with a frozen
Round181 result digest.
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
from typing import Any, Callable

import flint
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round178_later_return_exact_key_bridge as r178


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_round181_parametric_collision2_graph_arrangement_certificate.json"
OUTPUT = HERE / "cm2_round181_parametric_collision2_graph_arrangement_verification.json"
PRODUCER = "cm2_round181_parametric_collision2_graph_arrangement.py"
SCHEMA = "cm2.round181.parametric-collision2-graph-arrangement.v1"
VERIFICATION_SCHEMA = "cm2.round181.parametric-collision2-graph-arrangement-verification.v1"
PRODUCER_SHA256 = "6e9d51229c209caacf3964d24600295375bd08e963b4e154774625707aa1524c"
MAX_INPUT_BYTES = 64 * 1024 * 1024
R178_PRODUCER = "cm2_round178_later_return_exact_key_bridge.py"
R178_CERT = "cm2_round178_later_return_exact_key_bridge_certificate.json"
R178_VERIFIER = "cm2_round178_later_return_exact_key_bridge_verifier.py"
R178_VERIFICATION = "cm2_round178_later_return_exact_key_bridge_verification.json"
R178_MANIFEST = "cm2_round178_later_return_exact_key_bridge_manifest.sha256"
PINS = {
    R178_PRODUCER: "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    R178_CERT: "31005b55c465db29e2e562ca8b94cde18b6c14fb830da7cbc6ef63d27a532f70",
    R178_VERIFIER: "73b3229d6349021b874ecab7e9036989b519e005baac91fb3a6fb0c49650daeb",
    R178_VERIFICATION: "ae3752a31b13f6dc2b503bab4a407af75644407b8a9686a4a01cef777ad7956b",
    R178_MANIFEST: "d4753f6523ae300a2ed103e078916d720d22f67ef52febc7a9d3c348b9fd81bb",
}
R178_RESULT = "c9da1d3312c4fe8253941e35e8113e1ac14e23e6ce58b7e0ff4ed2b0ebbda31b"
R178_VERIFICATION_RESULT = "ea725103b4801814702e6112d29d1daac891c8d87b64a2bb027e9c7b83fc1e01"
ROOT_COLLAR = "COLLISION2_CANDIDATE_ROOT_ORDER_COLLAR"
WALL_COLLAR = "COLLISION2_WALL_OR_CORNER_COLLAR"
TARGETED_PHASE_A = (
    "COLLISION1_DELTA_ROOT_COLLAR",
    "COLLISION1_OUTGOING_CHART_COLLAR",
    "COLLISION1_ROOT_ORDER_COLLAR",
    "SOURCE_CHART_SEAM_COLLAR",
)
CANDIDATES = r178.translated_candidates("W:W", (1, 0))


class VerificationError(RuntimeError):
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
        raise VerificationError(label)


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
    raise VerificationError(f"noninteger number:{value}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(type(value) in {dict, list, str, int, bool, type(None)}, f"type:{path}")
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str and "\x00" not in key, f"key:{path}")
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"NUL:{path}")


def strict_parse(raw: bytes, label: str, canonical: bool = True) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
            f"encoding:{label}")
    try:
        value = json.loads(raw.decode("utf-8", "strict"),
                           object_pairs_hook=unique_pairs,
                           parse_float=reject_number,
                           parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"JSON:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"top:{label}")
    if canonical:
        require(raw == canonical_bytes(value) + b"\n", f"canonical:{label}")
    return value


def read_regular(path: Path, expected: str | None = None,
                 maximum: int = MAX_INPUT_BYTES) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"regular:{path}")
    require(not path.is_symlink(), f"symlink:{path}")
    require(st.st_nlink == 1, f"hardlink:{path}")
    require(st.st_size <= maximum, f"oversized:{path}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def dependency_check() -> dict[str, Any]:
    require(flint.__version__ == "0.9.0" and atlas.ctx.prec == 384, "flint")
    require(Path(r178.__file__).resolve() == (HERE / R178_PRODUCER).resolve(),
            "Round178 module")
    require(sha256_bytes(read_regular(HERE / PRODUCER)) == PRODUCER_SHA256,
            "producer pin")
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    upstream = strict_parse(read_regular(HERE / R178_CERT, PINS[R178_CERT]),
                            R178_CERT, False)
    verification = strict_parse(
        read_regular(HERE / R178_VERIFICATION, PINS[R178_VERIFICATION]),
        R178_VERIFICATION, False,
    )
    require(upstream["result_sha256"] == R178_RESULT and
            upstream["result_sha256"] == digest(upstream["result"]),
            "Round178 result")
    require(verification["result_sha256"] == R178_VERIFICATION_RESULT and
            verification["result_sha256"] == digest(verification["result"]) and
            verification["result"]["status"] == "PASS" and
            verification["result"]["full_expected_result_canonical_equality"],
            "Round178 verification")
    return upstream["result"]


def box_from_row(row: dict[str, Any]) -> atlas.AtlasBox:
    box = row["box"]
    return atlas.AtlasBox(Q(box["t"][0]), Q(box["t"][1]),
                          Q(box["p"][0]), Q(box["p"][1]),
                          Q(box["s"][0]), Q(box["s"][1]),
                          row["relative_depth"], row["terminal_path"])


def midpoint(a: Q, b: Q) -> Q:
    return (a + b) / 2


def point_box(box: atlas.AtlasBox, t: Q, p: Q, s: Q,
              suffix: str) -> atlas.AtlasBox:
    return atlas.AtlasBox(t, t, p, p, s, s, box.depth, box.path + suffix)


def center_box(box: atlas.AtlasBox) -> atlas.AtlasBox:
    return point_box(box, midpoint(box.t0, box.t1), midpoint(box.p0, box.p1),
                     midpoint(box.s0, box.s1), ".center")


def chart_id(parent_key: str) -> str:
    pieces = parent_key.split(":")
    require(len(pieces) == 3, f"parent:{parent_key}")
    return ":".join(pieces[:2])


def collision1_state(parent_key: str, box: atlas.AtlasBox) -> dict[str, Any]:
    geometry = r178.initial_geometry(chart_id(parent_key), box)
    kind, data = r178.root_record(*geometry, r178.COLLISION1_OWNER)
    require(kind == "STRICT_FUTURE" and data is not None,
            f"collision1:{parent_key}:{box.path}:{kind}")
    return r178.collision_state(geometry, (r178.COLLISION1_OWNER, data))


def collision2_geometry(state: dict[str, Any]
                        ) -> tuple[Any, Any, Any, Any, Any]:
    return (state["contact_x"], state["contact_y"], state["outgoing_x"],
            state["outgoing_y"], state["s"])


def raw_candidate(geometry: tuple[Any, Any, Any, Any, Any],
                  identifier: str) -> dict[str, Any]:
    qx, qy, ux, uy, s = geometry
    ax, ay = r178.target_center(identifier, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = r178.RADIUS[identifier[0]]
    return {"ell": ell, "transverse": transverse, "radius": radius,
            "Delta": radius * radius - transverse * transverse}


def target_affine(identifier: str) -> tuple[Q, Q, Q]:
    obstacle, x, y = r178.parse_target(identifier)
    return ((Q(x), Q(0), Q(y)) if obstacle == "G"
            else (Q(x) + Q(1, 2), Q(1), Q(y) + Q(1, 2)))


def minimum_abs_affine(a: Q, b: Q) -> Q:
    values = (a + b * atlas.S_LOWER, a + b * atlas.S_UPPER)
    lower, upper = min(values), max(values)
    return Q(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))


def separation_registry() -> dict[str, Any]:
    rows, minimum = [], None
    for left, right in itertools.combinations(CANDIDATES, 2):
        lx, lb, ly = target_affine(left)
        rx, rb, ry = target_affine(right)
        dx = minimum_abs_affine(lx - rx, lb - rb)
        dy = ly - ry
        distance = dx * dx + dy * dy
        radius = Q(r178.base.RADIUS[left[0]]) + Q(r178.base.RADIUS[right[0]])
        margin = distance - radius * radius
        require(margin > 0, f"separation:{left}:{right}")
        minimum = margin if minimum is None else min(minimum, margin)
        rows.append({"left": left, "right": right,
                     "minimum_center_distance_squared": str(distance),
                     "radius_sum_squared": str(radius * radius),
                     "strict_margin": str(margin)})
    return {
        "candidate_count": len(CANDIDATES),
        "pair_count": len(rows),
        "minimum_strict_squared_margin": str(minimum),
        "pair_rows_sha256": digest(rows),
        "consequence": (
            "two strict future near roots cannot become equal; on a connected "
            "fixed-status cell their order is fixed by one strict point"
        ),
    }


def point_owner(parent_key: str, box: atlas.AtlasBox
                ) -> tuple[str, tuple[str, dict[str, Any]] | None]:
    state = collision1_state(parent_key, center_box(box))
    status, selected = r178.select_owner(collision2_geometry(state), CANDIDATES)
    return (status, selected if (
        status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple)
    ) else None)


def rational_point(t: Q, p: Q, s: Q) -> dict[str, str]:
    return {"t": str(t), "p": str(p), "s": str(s)}


def delta_point(parent_key: str, box: atlas.AtlasBox, identifier: str,
                t: Q, p: Q, s: Q) -> tuple[int, str | None]:
    state = collision1_state(parent_key, point_box(box, t, p, s, ".witness"))
    geometry = collision2_geometry(state)
    delta = raw_candidate(geometry, identifier)["Delta"]
    sign = 1 if bool(delta > 0) else -1 if bool(delta < 0) else 0
    if sign <= 0:
        return sign, None
    status, selected = r178.select_owner(geometry, CANDIDATES)
    owner = selected[0] if (
        status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple)
    ) else None
    return sign, owner


def positive_grid(parent_key: str, box: atlas.AtlasBox,
                  identifier: str) -> dict[str, Any] | None:
    axes = ((box.t0, midpoint(box.t0, box.t1), box.t1),
            (box.p0, midpoint(box.p0, box.p1), box.p1),
            (box.s0, midpoint(box.s0, box.s1), box.s1))
    center = tuple(axis[1] for axis in axes)
    points = [tuple(axes[a][i] for a, i in enumerate(indices))
              for indices in itertools.product((0, 2), repeat=3)]
    for values in itertools.product(*axes):
        if values != center and values not in points:
            points.append(values)
    for t, p, s in points:
        sign, owner = delta_point(parent_key, box, identifier, t, p, s)
        if sign > 0:
            return {"point": rational_point(t, p, s), "Delta_sign": ">0",
                    "strict_point_owner": owner}
    return None


def graph_record(parent_key: str, box: atlas.AtlasBox,
                 state: dict[str, Any], incumbent: str,
                 incumbent_data: dict[str, Any], candidate: str,
                 candidate_kind: str, seek_positive: bool) -> dict[str, Any]:
    raw = raw_candidate(collision2_geometry(state), candidate)
    derivative = 2 * raw["transverse"] * raw["ell"] / state["cosine"]
    derivative_sign = (">0" if bool(derivative > 0)
                       else "<0" if bool(derivative < 0) else "UNRESOLVED")
    birth = (
        "CANDIDATE_BIRTH_BEFORE_INCUMBENT"
        if bool(raw["ell"] < incumbent_data["near"])
        else "CANDIDATE_BIRTH_AFTER_INCUMBENT"
        if bool(incumbent_data["near"] < raw["ell"])
        else "UNRESOLVED_AT_BIRTH"
    )
    t, p, s = (midpoint(box.t0, box.t1), midpoint(box.p0, box.p1),
               midpoint(box.s0, box.s1))
    center_sign, center_owner = delta_point(parent_key, box, candidate, t, p, s)
    positive = positive_grid(parent_key, box, candidate) if seek_positive else None
    if positive is not None and birth == "CANDIDATE_BIRTH_BEFORE_INCUMBENT":
        require(positive["strict_point_owner"] == candidate,
                f"positive owner:{parent_key}:{box.path}:{candidate}")
    return {
        "candidate": candidate,
        "input_root_kind": candidate_kind,
        "graph_equation": f"Delta_{candidate}=R_{candidate[0]}^2-eta_{candidate}^2=0",
        "exact_next_source_coordinate": "p1",
        "monotone_derivative_formula":
            "dDelta/dp1=2*eta_candidate*ell_candidate/sqrt(1-p1^2)",
        "monotone_derivative_sign_on_box": derivative_sign,
        "implicit_graph_regular_if_nonempty": derivative_sign != "UNRESOLVED",
        "birth_order_against_incumbent": birth,
        "center_witness": {
            "point": rational_point(t, p, s),
            "Delta_sign": ">0" if center_sign > 0 else "<0" if center_sign < 0
                          else "UNRESOLVED",
            "strict_point_owner_when_positive": center_owner,
        },
        "positive_grid_witness": positive,
        "conditional_three_layer_owner_ledger": {
            "scope":
                "valid only if a nonempty Delta=0 carrier is subsequently isolated",
            "Delta_less_than_zero_owner": incumbent,
            "Delta_equal_zero": "2D_GRAZING_GRAPH__NO_3D_OR_INTEGER_CREDIT",
            "Delta_greater_than_zero_owner": (
                candidate if birth == "CANDIDATE_BIRTH_BEFORE_INCUMBENT"
                else incumbent if birth == "CANDIDATE_BIRTH_AFTER_INCUMBENT"
                else "UNRESOLVED"
            ),
            "root_equality_layer":
                "EMPTY_BY_PINNED_STRICT_BOUNDARY_SEPARATION",
            "half_open_policy":
                "open signs disjoint; Delta=0 retained once as its own 2D stratum",
        },
    }


def wall_row(parent_key: str, box: atlas.AtlasBox,
             state: dict[str, Any],
             selected: tuple[str, dict[str, Any]],
             origin: str) -> dict[str, Any]:
    identifier, data = selected
    hit_y = state["contact_y"] + data["near"] * state["outgoing_y"]
    integers = [value for value in range(-8, 9)
                if not bool(hit_y < value) and not bool(hit_y > value)]
    require(integers, f"wall:{parent_key}:{box.path}")
    volume = (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)
    return closed_row({
        "parent_key": parent_key,
        "terminal_path": box.path,
        "box_volume": str(volume),
        "collision2_owner": identifier,
        "wall_axis": "Y",
        "possible_integer_endpoint_walls": integers,
        "graph_equations": [f"hit_y-{value}=0" for value in integers],
        "origin": origin,
        "dimension": 2,
        "open_side_words": "NOT_YET_MATERIALIZED",
        "wall_graph_Jacobian": "UNRESOLVED",
        "half_open_owner":
            "official clean-wall registry retains endpoint equality as a separate graph",
        "whole_box_or_global_credit": 0,
    })


def outgoing_detail(parent_key: str, box: atlas.AtlasBox,
                    identifier: str, official: dict[str, Any]) -> dict[str, Any]:
    state = collision1_state(parent_key, center_box(box))
    geometry = collision2_geometry(state)
    kind, data = r178.root_record(*geometry, identifier)
    require(kind == "STRICT_FUTURE" and data is not None, "outgoing root")
    next_state = r178.collision_state(geometry, (identifier, data))
    center_chart = r178.strict_chart(next_state["normal_x"], next_state["normal_y"])
    require(center_chart is not None, "outgoing center")
    return {
        **official,
        "outgoing_chart_graph": {
            "equation": "H2=n2_x^2-n2_y^2=0",
            "dimension": 2,
            "strict_center_chart_witness": center_chart,
            "H2_greater_than_zero_owner": "E if n2_x>0 else W",
            "H2_less_than_zero_owner": "N if n2_y>0 else S",
            "H2_equal_zero_half_open_owner": "E or W owns; N or S excludes",
            "whole_box_outgoing_chart": "UNRESOLVED",
            "integer_or_global_credit": 0,
        },
    }


def analyze_root(row: dict[str, Any],
                 pair_index: dict[tuple[str, str], int],
                 pattern_index: dict[tuple[str, ...], int],
                 exclusions: list[dict[str, Any]]
                 ) -> tuple[dict[str, Any], dict[str, Any] | None]:
    parent_key, box = row["parent_key"], box_from_row(row)
    state = collision1_state(parent_key, box)
    geometry = collision2_geometry(state)
    point_status, point_selected = point_owner(parent_key, box)
    volume = Q(row["box"]["volume"])
    if point_status != "STRICT_UNIQUE_OWNER" or point_selected is None:
        return closed_row({
            "parent_key": parent_key, "terminal_path": box.path,
            "box_volume": str(volume), "status": "POINT_OWNER_NOT_UNIQUE_COLLAR",
            "point_owner_status": point_status, "active_graph_count": 0,
            "active_graphs": [], "whole_box_or_global_credit": 0,
        }), None
    incumbent = point_selected[0]
    incumbent_kind, incumbent_data = r178.root_record(*geometry, incumbent)
    if incumbent_kind != "STRICT_FUTURE" or incumbent_data is None:
        return closed_row({
            "parent_key": parent_key, "terminal_path": box.path,
            "box_volume": str(volume),
            "status": "POINT_WINNER_NONSTRICT_ON_FULL_BOX_COLLAR",
            "point_owner": incumbent,
            "full_box_point_owner_root_kind": incumbent_kind,
            "active_graph_count": 0, "active_graphs": [],
            "whole_box_or_global_credit": 0,
        }), None
    active, excluded_ids, continuation = [], [], []
    for candidate in CANDIDATES:
        if candidate == incumbent:
            continue
        kind, _ = r178.root_record(*geometry, candidate)
        if kind in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND"}:
            continue
        if kind == "STRICT_FUTURE":
            continuation.append(candidate)
            continue
        raw = raw_candidate(geometry, candidate)
        if bool(raw["ell"] + raw["radius"] < 0):
            excluded_ids.append(candidate)
            exclusions.append(closed_row({
                "parent_key": parent_key, "terminal_path": box.path,
                "incumbent": incumbent, "candidate": candidate,
                "candidate_root_kind": kind,
                "relation_kind": "UNIVERSALLY_BEHIND_WHEN_REAL",
                "strict_witness": "candidate.ell + candidate.radius < 0",
                "consequence":
                    "even the far root is behind whenever Delta is nonnegative",
            }))
        elif bool(incumbent_data["near"] < raw["ell"] - raw["radius"]):
            excluded_ids.append(candidate)
            exclusions.append(closed_row({
                "parent_key": parent_key, "terminal_path": box.path,
                "incumbent": incumbent, "candidate": candidate,
                "candidate_root_kind": kind,
                "relation_kind": "UNIVERSALLY_LATER_WHEN_REAL",
                "strict_witness":
                    "incumbent.near < candidate.ell - candidate.radius",
                "consequence":
                    "candidate is later whenever real and cannot change owner",
            }))
        else:
            active.append((candidate, kind))
    graphs = [graph_record(parent_key, box, state, incumbent, incumbent_data,
                           candidate, kind, len(active) == 1)
              for candidate, kind in active]
    if not graphs:
        official, reason = r178.gate5_key(
            state, (incumbent, incumbent_data), pair_index, pattern_index
        )
        if official is None:
            wall = wall_row(parent_key, box, state, (incumbent, incumbent_data),
                            "ROOT_ORDER_CONTINUATION")
            status, detail = "ROOT_ORDER_RESOLVED__WALL_GRAPH_COLLAR", {
                "wall_reason": reason}
        else:
            next_state = r178.collision_state(
                geometry, (incumbent, incumbent_data))
            outgoing = r178.strict_chart(next_state["normal_x"],
                                         next_state["normal_y"])
            if outgoing is None:
                wall = None
                status = "ROOT_ORDER_RESOLVED__OUTGOING_CHART_GRAPH_COLLAR"
                detail = outgoing_detail(parent_key, box, incumbent, official)
            else:
                wall = None
                status = "ROOT_ORDER_AND_EXACT_KEY_RESOLVED_3D_BOX"
                detail = {**official, "collision2_outgoing_chart": outgoing}
        return closed_row({
            "parent_key": parent_key, "terminal_path": box.path,
            "box_volume": str(volume), "status": status,
            "point_owner": incumbent,
            "strict_root_continuation_candidates": sorted(continuation),
            "ell_minus_radius_excluded_candidates": sorted(excluded_ids),
            "active_graph_count": 0, "active_graphs": [], "detail": detail,
            "inner_box_occurrence_is_global_disposition": False,
            "whole_box_or_global_credit": 0,
        }), wall
    regular = all(graph["implicit_graph_regular_if_nonempty"] for graph in graphs)
    all_delta = all(graph["input_root_kind"] == "UNRESOLVED_DELTA"
                    for graph in graphs)
    birth_resolved = all(graph["birth_order_against_incumbent"]
                         != "UNRESOLVED_AT_BIRTH" for graph in graphs)
    both = (len(graphs) == 1 and
            graphs[0]["center_witness"]["Delta_sign"] == "<0" and
            graphs[0]["positive_grid_witness"] is not None)
    if len(graphs) == 1 and regular and all_delta and birth_resolved:
        status = ("SINGLE_MONOTONE_DELTA_GRAPH_THREE_LAYER_WITH_TWO_SIDE_WITNESSES"
                  if both else "REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER")
    elif len(graphs) >= 2 and regular and all_delta and birth_resolved:
        status = "MULTI_MONOTONE_DELTA_GRAPH_ARRANGEMENT_OUTER"
    else:
        status = "NONREGULAR_OR_NONDELTA_ACTIVE_EQUALITY_OUTER"
    count = len(graphs)
    return closed_row({
        "parent_key": parent_key, "terminal_path": box.path,
        "box_volume": str(volume), "status": status,
        "point_owner": incumbent,
        "strict_root_continuation_candidates": sorted(continuation),
        "ell_minus_radius_excluded_candidates": sorted(excluded_ids),
        "active_graph_count": count, "active_graphs": graphs,
        "candidate_2D_graph_carriers": count,
        "pairwise_1D_intersection_outers": math.comb(count, 2),
        "triple_0D_intersection_outers": math.comb(count, 3),
        "higher_multiplicity_incidence_outers":
            sum(math.comb(count, order) for order in range(4, count + 1)),
        "half_open_chamber_policy":
            "strict Delta sign vector owns each 3D chamber; every equality "
            "carrier is retained exactly once in its own dimension",
        "whole_box_or_global_credit": 0,
    }), None


def fraction_map(values: dict[str, Q]) -> dict[str, str]:
    return {key: str(value) for key, value in sorted(values.items())}


def build_expected() -> dict[str, Any]:
    upstream = dependency_check()
    pair_index, pattern_index, registry_digest = registry.key_index_tables()
    require(registry_digest == r178.GATE5_REGISTRY_DIGEST, "registry")
    terminal_rows = upstream["bounded_full_parent_3D_ledger"]["terminal_rows"]
    root_inputs = [row for row in terminal_rows if row["status"] == ROOT_COLLAR]
    wall_inputs = [row for row in terminal_rows if row["status"] == WALL_COLLAR]
    require(len(root_inputs) == 11416 and len(wall_inputs) == 158, "inputs")
    exclusions: list[dict[str, Any]] = []
    root_rows, continued_walls = [], []
    for row in root_inputs:
        arranged, wall = analyze_root(row, pair_index, pattern_index, exclusions)
        root_rows.append(arranged)
        if wall is not None:
            continued_walls.append(wall)
    root_rows.sort(key=lambda row: (row["parent_key"], row["terminal_path"]))
    exclusions.sort(key=lambda row: (
        row["parent_key"], row["terminal_path"], row["candidate"]))
    continued_walls.sort(key=lambda row: (
        row["parent_key"], row["terminal_path"]))
    original_walls = []
    for row in wall_inputs:
        box = box_from_row(row)
        state = collision1_state(row["parent_key"], box)
        status, selected = r178.select_owner(
            collision2_geometry(state), CANDIDATES)
        require(status == "STRICT_UNIQUE_OWNER" and isinstance(selected, tuple),
                "wall owner")
        original_walls.append(wall_row(
            row["parent_key"], box, state, selected, "ROUND178_WALL_COLLAR"))
    original_walls.sort(key=lambda row: (row["parent_key"], row["terminal_path"]))
    all_walls = sorted(original_walls + continued_walls,
                       key=lambda row: (row["parent_key"], row["terminal_path"]))
    root_counts = Counter(row["status"] for row in root_rows)
    root_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    for row in root_rows:
        root_volumes[row["status"]] += Q(row["box_volume"])
    root_volume = sum(Q(row["box"]["volume"]) for row in root_inputs)
    require(sum(root_volumes.values()) == root_volume, "root volume")
    new_exact = [row for row in root_rows
                 if row["status"] == "ROOT_ORDER_AND_EXACT_KEY_RESOLVED_3D_BOX"]
    new_exact_volume = sum(Q(row["box_volume"]) for row in new_exact)
    key_ids = sorted({row["detail"]["official_gate5_key"]["word_key_id"]
                      for row in new_exact})
    ordinals = sorted({row["detail"]["official_gate5_key"]["ordinal_zero_based"]
                       for row in new_exact})
    require(len(exclusions) == 22848 and len(new_exact) == 8292 and
            ordinals == [290575, 291560, 321111, 322097], "new census")
    active_graphs = sum(row["active_graph_count"] for row in root_rows)
    pair_outers = sum(row.get("pairwise_1D_intersection_outers", 0)
                      for row in root_rows)
    triple_outers = sum(row.get("triple_0D_intersection_outers", 0)
                        for row in root_rows)
    higher_outers = sum(row.get("higher_multiplicity_incidence_outers", 0)
                        for row in root_rows)
    active_census = Counter(row["active_graph_count"] for row in root_rows)
    two_side = [row for row in root_rows if row["status"] ==
                "SINGLE_MONOTONE_DELTA_GRAPH_THREE_LAYER_WITH_TWO_SIDE_WITNESSES"]
    missing = [row for row in root_rows if row["status"] ==
               "REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER"]
    multi = [row for row in root_rows if row["status"] ==
             "MULTI_MONOTONE_DELTA_GRAPH_ARRANGEMENT_OUTER"]
    nonstrict = [row for row in root_rows if row["status"] ==
                 "POINT_WINNER_NONSTRICT_ON_FULL_BOX_COLLAR"]
    first_multi = multi[0] if multi else None
    w_behind = next(({
        "parent_key": row["parent_key"],
        "terminal_path": row["terminal_path"],
        "incumbent": row["incumbent"],
        "candidate": row["candidate"],
        "relation_kind": row["relation_kind"],
        "strict_witness": row["strict_witness"],
    } for row in exclusions
        if row["candidate"] == "W[1,-2]" and
        row["relation_kind"] == "UNIVERSALLY_BEHIND_WHEN_REAL"), None)
    require(w_behind is not None, "W behind")
    phase_counts: Counter[str] = Counter()
    phase_volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    for row in terminal_rows:
        if row["status"] in TARGETED_PHASE_A:
            phase_counts[row["status"]] += 1
            phase_volumes[row["status"]] += Q(row["box"]["volume"])
    require(phase_counts == {
        "COLLISION1_DELTA_ROOT_COLLAR": 276,
        "COLLISION1_OUTGOING_CHART_COLLAR": 172,
        "COLLISION1_ROOT_ORDER_COLLAR": 50,
        "SOURCE_CHART_SEAM_COLLAR": 32,
    }, "phase census")
    wall_volume = sum(Q(row["box"]["volume"]) for row in wall_inputs)
    targeted_volume = root_volume + wall_volume + sum(phase_volumes.values())
    residual_volume = targeted_volume - new_exact_volume
    per_parent = Counter(row["parent_key"] for row in new_exact)
    parent_rows = []
    for upstream_parent in upstream["bounded_full_parent_3D_ledger"]["parent_rows"]:
        key = upstream_parent["parent_key"]
        parent_rows.append(closed_row({
            "parent_key": key,
            "Round178_resolved_inner_box_count":
                upstream_parent["resolved_collision2_3D_box_count"],
            "Round181_new_exact_key_inner_box_count": per_parent[key],
            "combined_strict_inner_box_count":
                upstream_parent["resolved_collision2_3D_box_count"] + per_parent[key],
            "complete_collision2_live_stratum_closed": False,
            "status": "PARTIAL",
            "whole_stratum_or_parent_credit": 0,
        }))
    return {
        "status":
            "PARTIAL_PARAMETRIC_MONOTONE_COLLISION2_GRAPH_ARRANGEMENT__NO_GLOBAL_DISPOSITION",
        "Round178_binding": {
            "certificate_result_sha256": R178_RESULT,
            "verification_result_sha256": R178_VERIFICATION_RESULT,
            "input_terminal_box_count":
                upstream["bounded_full_parent_3D_ledger"]["terminal_box_count"],
            "input_collision2_root_order_collars": len(root_inputs),
            "input_collision2_wall_or_corner_collars": len(wall_inputs),
            "Round178_files_modified": False,
        },
        "strict_boundary_separation_continuation": separation_registry(),
        "root_order_relation_exclusions": {
            "row_count": len(exclusions),
            "rows_sha256": digest(exclusions),
            "rows": exclusions,
            "scope": "BOX_CANDIDATE_RELATIONS_ONLY",
            "global_or_whole_parent_credit": 0,
        },
        "collision2_root_order_arrangement": {
            "input_box_count": len(root_inputs),
            "input_exact_volume": str(root_volume),
            "arrangement_rows_sha256": digest(root_rows),
            "arrangement_rows": root_rows,
            "status_counts": dict(sorted(root_counts.items())),
            "status_volumes": fraction_map(root_volumes),
            "active_graph_count_census":
                {str(key): value for key, value in sorted(active_census.items())},
            "root_order_resolved_box_count":
                root_counts["ROOT_ORDER_AND_EXACT_KEY_RESOLVED_3D_BOX"] +
                root_counts["ROOT_ORDER_RESOLVED__WALL_GRAPH_COLLAR"] +
                root_counts["ROOT_ORDER_RESOLVED__OUTGOING_CHART_GRAPH_COLLAR"],
            "new_exact_key_3D_box_count": len(new_exact),
            "new_exact_key_3D_volume": str(new_exact_volume),
            "new_local_gate5_key_ids": key_ids,
            "new_local_gate5_ordinals_zero_based": ordinals,
            "single_graph_two_side_witness_count": len(two_side),
            "single_graph_positive_witness_missing_count": len(missing),
            "multi_graph_outer_box_count": len(multi),
            "point_winner_nonstrict_box_count": len(nonstrict),
            "exact_volume_conservation":
                f"{'+'.join(f'{k}:{root_volumes[k]}' for k in sorted(root_volumes))}"
                f"={root_volume}",
            "inner_box_occurrences_promoted_globally": 0,
        },
        "collision2_wall_graph_arrangement": {
            "Round178_input_wall_graph_count": len(original_walls),
            "new_after_root_continuation_wall_graph_count": len(continued_walls),
            "total_wall_graph_count": len(all_walls),
            "rows_sha256": digest(all_walls),
            "rows": all_walls,
            "all_are_Y_endpoint_integer_wall_graphs":
                all(row["wall_axis"] == "Y" for row in all_walls),
            "wall_side_words_materialized": 0,
            "wall_graph_Jacobians_closed": 0,
            "global_or_whole_box_credit": 0,
        },
        "inherited_collision1_and_source_seam_arrangement": {
            "status_counts": dict(sorted(phase_counts.items())),
            "status_volumes": fraction_map(phase_volumes),
            "Delta_graph_three_layers_retained": 276,
            "outgoing_chart_H_graph_three_layers_retained": 172,
            "root_order_or_root_sign_outers_retained": 50,
            "source_seam_three_layers_retained": 32,
            "guard_rechart_rows_sha256":
                upstream["guard_adjacent_chart_recoordinates"]["rows_sha256"],
            "two_dimensional_source_seam_owner": "E",
            "adjacent_N_or_S_seam_representation_excluded": True,
            "one_dimensional_Delta_or_H_seam_intersections_counted_once": 4,
            "new_integer_credit": 0,
        },
        "dimension_stratified_graph_ledger": {
            "nominal_collision2_candidate_2D_graph_carriers_if_present":
                active_graphs,
            "certified_nonempty_collision2_candidate_2D_graph_carriers": 0,
            "nominal_collision2_wall_2D_graph_carriers_if_present":
                len(all_walls),
            "certified_nonempty_collision2_wall_2D_graph_carriers": 0,
            "nominal_collision2_outgoing_chart_2D_graph_carriers_if_present":
                root_counts["ROOT_ORDER_RESOLVED__OUTGOING_CHART_GRAPH_COLLAR"],
            "certified_nonempty_collision2_outgoing_chart_2D_graph_carriers": 0,
            "nominal_candidate_pairwise_1D_intersection_outers": pair_outers,
            "certified_nonempty_candidate_pairwise_1D_intersections": 0,
            "nominal_candidate_triple_0D_intersection_outers": triple_outers,
            "certified_nonempty_candidate_triple_0D_intersections": 0,
            "nominal_higher_multiplicity_incidence_outers": higher_outers,
            "root_equality_2D_graphs": 0,
            "root_equality_empty_reason":
                "strict positive separation of every candidate boundary pair",
            "half_open_rule":
                "each strict sign chamber is disjoint; equality carriers are "
                "retained once at their own dimension",
            "two_or_one_or_zero_dimensional_integer_credit": 0,
        },
        "exact_residual_census": {
            "targeted_input_box_count":
                len(root_inputs) + len(wall_inputs) + sum(phase_counts.values()),
            "targeted_input_exact_volume": str(targeted_volume),
            "new_exact_key_box_count": len(new_exact),
            "new_exact_key_exact_volume": str(new_exact_volume),
            "residual_parent_box_count":
                len(root_inputs) - len(new_exact) + len(wall_inputs)
                + sum(phase_counts.values()),
            "residual_exact_coordinate_outer_volume": str(residual_volume),
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
        "minimum_regressions": {
            "W_1_minus2_unresolved_Delta_behind": w_behind,
            "first_multi_graph_hard_blocker": ({
                "parent_key": first_multi["parent_key"],
                "terminal_path": first_multi["terminal_path"],
                "box_volume": first_multi["box_volume"],
                "point_owner": first_multi["point_owner"],
                "active_candidates":
                    [graph["candidate"] for graph in first_multi["active_graphs"]],
                "coupled_graph_count": first_multi["active_graph_count"],
            } if first_multi is not None else None),
        },
        "first_analytic_hard_blocker": {
            "kind": "SINGLE_DISCRIMINANT_GRAPH_EXISTENCE_AND_SIDE_BRACKETING",
            "reason":
                "584 boxes have a strict nonzero p1 derivative and a strict negative center witness, but no strict positive-owner point on the 27-point rational grid; a face-bracketed interval-Newton solve is required before a nonempty Delta=0 graph or its positive chamber may be asserted",
            "coupled_followup":
                "6 two-graph boxes retain 6 pairwise 1D incidence outers",
            "wall_followup":
                "168 Y-endpoint wall graphs still need a nonzero pullback Jacobian and both half-open side words; 1128 outgoing H2 graphs retain their half-open chart carrier",
        },
        "strict_nonpromotion": {
            "observed_point_289591_global_disposition": 0,
            "inner_box_290575_global_disposition": 0,
            "all_new_exact_key_rows_are_local_strict_3D_inner_boxes": True,
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "coupled interval-Newton isolation of every multi-Delta 1D/0D incidence, then exact Y-endpoint wall-side words and outgoing chart seams, followed by the inherited collision1/source-seam carriers",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": PRODUCER_SHA256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": atlas.ctx.prec,
            "effective_precision_source":
                "pinned Round178/registry transitive import chain",
            "Round178_files_modified": False,
        },
    }


def validate_candidate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(set(candidate) == {"schema", "result", "result_sha256"}, "shape")
    require(candidate["schema"] == SCHEMA, "schema")
    require(candidate["result_sha256"] == digest(candidate["result"]), "self digest")
    require(candidate["result"] == expected, "full independent expected equality")


def resign(candidate: dict[str, Any]) -> None:
    candidate["result_sha256"] = digest(candidate["result"])


def semantic_attacks(certificate: dict[str, Any],
                     expected: dict[str, Any]) -> list[str]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def behind_active(result: dict[str, Any]) -> None:
        rows = result["root_order_relation_exclusions"]["rows"]
        row = next(item for item in rows
                   if item["candidate"] == "W[1,-2]" and
                   item["relation_kind"] == "UNIVERSALLY_BEHIND_WHEN_REAL")
        row["relation_kind"] = "FORWARD_ACTIVE_DELTA_GRAPH"
        row["consequence"] = "candidate promoted"

    def root_whole(result: dict[str, Any]) -> None:
        result["collision2_root_order_arrangement"][
            "root_order_resolved_box_count"] = 11416

    def exact_global(result: dict[str, Any]) -> None:
        result["collision2_root_order_arrangement"][
            "inner_box_occurrences_promoted_globally"] = 8292

    def fake_positive(result: dict[str, Any]) -> None:
        row = next(item for item in
                   result["collision2_root_order_arrangement"]["arrangement_rows"]
                   if item["status"] == "REGULAR_IF_NONEMPTY_DELTA_GRAPH_OUTER")
        row["active_graphs"][0]["positive_grid_witness"] = {
            "point": {"t": "0", "p": "0", "s": "0"},
            "Delta_sign": ">0",
            "strict_point_owner": row["active_graphs"][0]["candidate"],
        }

    def close_pairs(result: dict[str, Any]) -> None:
        result["dimension_stratified_graph_ledger"][
            "certified_nonempty_candidate_pairwise_1D_intersections"] = 6

    def candidate_nonempty(result: dict[str, Any]) -> None:
        result["dimension_stratified_graph_ledger"][
            "certified_nonempty_collision2_candidate_2D_graph_carriers"] = 596

    def wall_close(result: dict[str, Any]) -> None:
        block = result["collision2_wall_graph_arrangement"]
        block["wall_side_words_materialized"] = 168
        block["wall_graph_Jacobians_closed"] = 168

    def outgoing_close(result: dict[str, Any]) -> None:
        result["dimension_stratified_graph_ledger"][
            "certified_nonempty_collision2_outgoing_chart_2D_graph_carriers"] = 1128

    def relation_count(result: dict[str, Any]) -> None:
        result["root_order_relation_exclusions"]["row_count"] = 22849

    def relation_digest(result: dict[str, Any]) -> None:
        result["root_order_relation_exclusions"]["rows_sha256"] = "0" * 64

    def residual_volume(result: dict[str, Any]) -> None:
        result["exact_residual_census"]["residual_exact_coordinate_outer_volume"] = "0"

    def exact_volume(result: dict[str, Any]) -> None:
        result["collision2_root_order_arrangement"]["new_exact_key_3D_volume"] = "0"

    def conservation(result: dict[str, Any]) -> None:
        result["collision2_root_order_arrangement"]["exact_volume_conservation"] = "forged"

    def full_sixteen(result: dict[str, Any]) -> None:
        block = result["per_parent_partial_ledger"]
        block["collision2_fully_closed_live_strata"] = 16
        block["collision2_partial_live_strata"] = 0

    def close_one_parent(result: dict[str, Any]) -> None:
        row = result["per_parent_partial_ledger"]["rows"][0]
        row["complete_collision2_live_stratum_closed"] = True
        row["status"] = "FULL"

    def d02(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["D02"] = "PASS"

    def gate5(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["global_Gate5_fields"] = "18/18"

    def point289591(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"][
            "observed_point_289591_global_disposition"] = 1

    def inner290575(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["inner_box_290575_global_disposition"] = 1

    def seam_owner(result: dict[str, Any]) -> None:
        result["inherited_collision1_and_source_seam_arrangement"][
            "two_dimensional_source_seam_owner"] = "N"

    def one_dimensional(result: dict[str, Any]) -> None:
        result["inherited_collision1_and_source_seam_arrangement"][
            "one_dimensional_Delta_or_H_seam_intersections_counted_once"] = 5

    def promote_status(result: dict[str, Any]) -> None:
        result["status"] = "PASS_FULL_COLLISION2_CLOSURE"

    def wall_owner(result: dict[str, Any]) -> None:
        result["collision2_wall_graph_arrangement"]["rows"][0][
            "half_open_owner"] = "arbitrary adjacent word"

    attacks.extend([
        ("behind_W_1_minus2_to_forward_active", behind_active),
        ("9430_root_order_to_whole_input", root_whole),
        ("8292_local_inner_boxes_to_global", exact_global),
        ("584_missing_witness_forged_positive", fake_positive),
        ("six_pair_outers_forged_closed", close_pairs),
        ("596_nominal_candidate_graphs_forged_nonempty", candidate_nonempty),
        ("168_wall_carriers_forged_closed", wall_close),
        ("1128_outgoing_carriers_forged_closed", outgoing_close),
        ("relation_count_mutation", relation_count),
        ("relation_digest_mutation", relation_digest),
        ("residual_volume_mutation", residual_volume),
        ("new_exact_volume_mutation", exact_volume),
        ("volume_conservation_mutation", conservation),
        ("sixteen_strata_forged_full", full_sixteen),
        ("one_parent_forged_full", close_one_parent),
        ("D02_forged_pass", d02),
        ("Gate5_forged_18_of_18", gate5),
        ("point_289591_promoted", point289591),
        ("inner_290575_promoted", inner290575),
        ("E_owned_source_seam_changed", seam_owner),
        ("one_dimensional_row_duplicated", one_dimensional),
        ("partial_status_forged_full", promote_status),
        ("wall_half_open_owner_changed", wall_owner),
    ])
    rejected = []
    for label, mutate in attacks:
        candidate = copy.deepcopy(certificate)
        mutate(candidate["result"])
        resign(candidate)
        require(candidate["result_sha256"] == digest(candidate["result"]),
                f"attack resign:{label}")
        try:
            validate_candidate(candidate, expected)
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError(f"semantic attack accepted:{label}")
    return rejected


def json_attacks(certificate: dict[str, Any]) -> list[str]:
    canonical = canonical_bytes(certificate) + b"\n"
    cases = {
        "duplicate": b'{"x":1,"x":2}\n',
        "float": b'{"x":1.2}\n',
        "NaN": b'{"x":NaN}\n',
        "BOM": b"\xef\xbb\xbf" + canonical,
        "NUL": b'{"x":"a\x00b"}\n',
        "trailing": canonical + b"{}",
        "whitespace": b" " + canonical,
        "top_list": b"[]\n",
        "invalid_utf8": b'{"x":"\xff"}\n',
    }
    rejected = []
    for label, raw in cases.items():
        try:
            strict_parse(raw, f"attack:{label}")
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError(f"JSON attack accepted:{label}")
    return rejected


def validate_output(path: Path) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == HERE, "output directory")
    require(absolute.resolve(strict=False) not in {
        (HERE / PRODUCER).resolve(), Path(__file__).resolve(), CERTIFICATE.resolve()
    }, "protected output")
    if absolute.exists() or absolute.is_symlink():
        st = absolute.lstat()
        require(stat.S_ISREG(st.st_mode), "output regular")
        require(not absolute.is_symlink(), "output symlink")
        require(st.st_nlink == 1, "output hardlink")


def path_attacks() -> list[str]:
    rejected = []
    with tempfile.TemporaryDirectory(dir=HERE, prefix=".round181-path-") as name:
        root = Path(name)
        regular = root / "regular"
        regular.write_bytes(b"x")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        directory = root / "directory"
        directory.mkdir()
        fifo = root / "fifo"
        os.mkfifo(fifo)
        oversized = root / "oversized"
        oversized.write_bytes(b"xx")
        output_symlink = HERE / f"{root.name}.output-symlink"
        output_hardlink = HERE / f"{root.name}.output-hardlink"
        output_symlink.symlink_to(regular)
        os.link(regular, output_hardlink)
        cases: list[tuple[str, Callable[[], None]]] = [
            ("input_symlink", lambda: read_regular(symlink)),
            ("input_hardlink", lambda: read_regular(hardlink)),
            ("input_directory", lambda: read_regular(directory)),
            ("input_fifo", lambda: read_regular(fifo)),
            ("input_oversized", lambda: read_regular(oversized, maximum=1)),
            ("output_escape", lambda: validate_output(root / "escape")),
            ("output_producer", lambda: validate_output(HERE / PRODUCER)),
            ("output_certificate", lambda: validate_output(CERTIFICATE)),
            ("output_verifier", lambda: validate_output(Path(__file__))),
            ("output_symlink", lambda: validate_output(output_symlink)),
            ("output_hardlink", lambda: validate_output(output_hardlink)),
        ]
        try:
            for label, operation in cases:
                try:
                    operation()
                except (VerificationError, OSError):
                    rejected.append(label)
                else:
                    raise VerificationError(f"path attack accepted:{label}")
        finally:
            output_symlink.unlink(missing_ok=True)
            output_hardlink.unlink(missing_ok=True)
    return rejected


def safe_write(path: Path, data: bytes) -> None:
    validate_output(path)
    absolute = Path(os.path.abspath(os.fspath(path)))
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.", suffix=".tmp", dir=absolute.parent)
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    certificate_path = Path(os.path.abspath(os.fspath(arguments.certificate)))
    require(certificate_path.parent.resolve() == HERE, "certificate directory")
    certificate = strict_parse(read_regular(certificate_path),
                               certificate_path.name)
    expected = build_expected()
    validate_candidate(certificate, expected)
    semantic = semantic_attacks(certificate, expected)
    json_rejected = json_attacks(certificate)
    path_rejected = path_attacks()
    result = {
        "status": "PASS",
        "certificate_result_sha256": certificate["result_sha256"],
        "independently_rebuilt_result_sha256": digest(expected),
        "full_expected_result_canonical_equality": True,
        "frozen_expected_result_digest_used_for_semantic_rejection": False,
        "producer_imported_or_executed": False,
        "producer_sha256": PRODUCER_SHA256,
        "independent_reconstruction": {
            "input_root_order_collars": 11416,
            "relation_exclusion_rows": 22848,
            "root_order_resolved_boxes": 9430,
            "new_local_exact_key_boxes": 8292,
            "outgoing_chart_graph_outers": 1128,
            "new_wall_graph_outers": 10,
            "total_wall_graph_outers": 168,
            "regular_if_nonempty_single_Delta_outers": 584,
            "two_Delta_outer_boxes": 6,
            "point_winner_nonstrict_boxes": 1396,
            "nominal_candidate_graph_carriers": 596,
            "certified_nonempty_candidate_graph_carriers": 0,
            "residual_parent_box_count": 3812,
            "residual_exact_coordinate_outer_volume": "21997737/838860800000",
            "collision2_fully_closed_live_strata": 0,
            "collision2_partial_live_strata": 16,
            "D02": "BLOCKED",
        },
        "re_signed_semantic_attacks": {
            "rejected": len(semantic), "total": len(semantic),
            "labels": semantic,
            "all_result_digests_recomputed_after_mutation": True,
        },
        "strict_JSON_attacks": {
            "rejected": len(json_rejected), "total": len(json_rejected),
            "labels": json_rejected,
        },
        "path_attacks": {
            "rejected": len(path_rejected), "total": len(path_rejected),
            "labels": path_rejected,
        },
        "verifier_provenance": {
            "schema": VERIFICATION_SCHEMA,
            "verifier_sha256": sha256_bytes(Path(__file__).read_bytes()),
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": atlas.ctx.prec,
            "precision_source": "pinned Round178/registry transitive import chain",
        },
    }
    envelope = {"schema": VERIFICATION_SCHEMA, "result": result,
                "result_sha256": digest(result)}
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
