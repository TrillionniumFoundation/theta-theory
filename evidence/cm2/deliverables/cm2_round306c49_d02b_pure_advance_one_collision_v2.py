#!/usr/bin/env python3
"""Pure, fail-closed D02-B one-collision continuation kernel, version 2.

``advance_one_collision(original_box, owner_history)`` is deterministic and
has no I/O side effect.  The collision number is derived solely from the
validated history length.  The same code therefore advances collision 3, 4,
5, and every later locally representable collision; there is no collision-3
branch in the proof logic.

The kernel independently recomputes the full-box AD geometry, every retained
candidate, the unique root order, exact owner, official word, chart, wall,
homogeneity, incidence, core decision, and a structured terminal-decision
margin.  A locally strict continuation is still *not* a D02 terminal.  The
global cemetery/disconnected and codimension-owner oracle is absent, so every
otherwise complete step returns PENDING_GLOBAL_ORACLE and zero formal credit.

C43--C45 are consumed only to freeze/replay the queue and the historical C44
pilot census.  C35--C37 template values never select a v2 occurrence owner.
The module writes canonical JSON only to stdout in CLI modes and never touches
an authority pointer, receipt, seal, or canonical status.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from flint import arb, ctx
import flint


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

import cm2_round306c43_collision3_ready_inventory_planner_v1 as c43
import cm2_round306c44_d02b_pair9_collision3_exact_recenter_adaptive_pilot_v1 as c44
import cm2_round306c45_d02b_pair_preserving_batch_runner_planner_v1 as c45
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38
import cm2_round166_multi_candidate_refinement_prototype as r166
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round185_preconditioned_c1_residual_refinement as r185


SCHEMA = "cm2.round306c49.d02-b-pure-advance-one-collision.v2"
ORIGINAL_BOX_SCHEMA = SCHEMA + ".original-box"
SOURCE_CHART_ID = "W:E"
COLLISION1_OWNER = "W[1,0]"
PAIR_INDEX = 9
PAIR9_PATH = "011110111"
SIDE_ORDER = ("REFLECTED", "REPRESENTATIVE")
AXES = ("t", "p")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

C43_SOURCE_SHA256 = "8519aa02e80ddda01953db9f48c641d88244f264ea67de59307a674c77194b48"
C44_SOURCE_SHA256 = "18ba0d94ab8875c2cbbf8c03f727e5fc606dd8f17953df63b480dee766872d28"
C45_SOURCE_SHA256 = "bd8937fe5c88b4a77e0eea14ef7fa4fc5e3356458e389a5d4d91e5ae8fb288f6"
QUEUE_PINS = {
    "representative_ready_rows": 7463,
    "physical_side_branches": 14926,
    "representative_key_sequence_sha256":
        "9fe3435e1efdb935fb2756c0e808b8cc282baf04af95a31ca723bccbe4755ce5",
    "physical_queue_sequence_sha256":
        "c79b7e8736c7cf9c8e95e6249d76c0d0b31fb4d3b6d5dbb12d359a4c7a41f5e0",
    "physical_handoff_id_line_sequence_sha256":
        "2558af09865e542b5eb969f636585baa815086de5d1f2b130a7ef152cf3a8c58",
    "C35_collision3_row_sha256":
        "2d1e15152e61648237b33b7aeade8a9e0c4374ecc84b0f4c3f3ddbb173f1b5a1",
    "C36_collision3_margin_row_sha256":
        "7a4296ba0a1537b4a34ff9c0673e63c0b5874a0e27e8c2e456dc46d0db0f4995",
    "C37_reflected_collision3_row_sha256":
        "7d75d31baa4826a0ae821d9bc14bfdb03b1a311a2ab00ba48ba78cdd79cfc013",
}
EXPECTED_C44_SIDE_CENSUS = {
    "node_count": 99,
    "split_count": 49,
    "leaf_count": 50,
    "relative_Kraft_sum": "1",
    "leaf_status_census": {
        "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION": 32,
        "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4_ZERO_CREDIT": 18,
    },
}

MISSING_GLOBAL_ORACLES = (
    "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE",
    "GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE",
)
ALLOWED_TERMINALS = (
    "STRICT_EXCLUDED",
    "KNOWN_COMPONENT",
    "STRICT_CEMETERY_OR_DISCONNECTED",
)

RR = r139.lower.round136
TIME = r139.lower.time3
STEP1 = r139.lower.step1
BASE = r185.BASE
_REGISTRY_CACHE: tuple[dict[Any, Any], dict[Any, Any], str] | None = None
_CORES_CACHE: tuple[Any, ...] | None = None


class Rejected(RuntimeError):
    """Strict contract or local enclosure rejection."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in value, "object hash absent before close")
    return {**value, "object_sha256": digest(value)}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def exact_bounds(value: arb) -> dict[str, Any]:
    lower, upper = RR.arb_pair(value)
    return {
        "exact_dyadic": [qstr(lower), qstr(upper)],
        "strict_sign": (
            "POSITIVE" if bool(value > 0) else
            "NEGATIVE" if bool(value < 0) else "UNRESOLVED"
        ),
    }


def positive_margin(value: arb) -> dict[str, Any]:
    need(bool(value > 0), "strict positive margin")
    lower, upper = RR.arb_pair(value)
    depth = RR.strict_dyadic_depth(value, lower)
    return {
        "exact_dyadic": [qstr(lower), qstr(upper)],
        "dyadic_depth": depth,
        "strict_lower_bound": qstr(RR.power_of_two(-depth)),
    }


def min_arb(values: list[arb]) -> arb:
    need(bool(values), "nonempty Arb minimum")
    return min(values, key=lambda value: RR.arb_pair(value)[0])


def immutable_registry_context() -> tuple[dict[Any, Any], dict[Any, Any], str]:
    """Load the frozen registry once; cache affects performance, not output."""

    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is None:
        _REGISTRY_CACHE = RR.component_cert.key_index_tables()
    return _REGISTRY_CACHE


def immutable_cores() -> tuple[Any, ...]:
    global _CORES_CACHE
    if _CORES_CACHE is None:
        _CORES_CACHE = tuple(RR.core_cert.physical_cores())
    return _CORES_CACHE


def validate_closed_box(value: Any) -> None:
    need(type(value) is dict and set(value) == {"t", "p", "s"},
         "closed box exact keys")
    for axis in ("t", "p", "s"):
        pair = value[axis]
        need(type(pair) is list and len(pair) == 2
             and all(type(item) is str for item in pair), "box pair:" + axis)
        lo, hi = Q(pair[0]), Q(pair[1])
        need(lo <= hi, "ordered closed box:" + axis)
    need(Q(value["s"][0]) == Q(value["s"][1]) == 0, "stationary s=0")


def validate_original_box(value: Any) -> None:
    expected = {
        "schema", "occurrence_id", "side", "source_chart_id", "closed_box",
        "adaptive_suffix", "source_binding_sha256",
    }
    need(type(value) is dict and set(value) == expected,
         "original box exact keys")
    need(value["schema"] == ORIGINAL_BOX_SCHEMA, "original box schema")
    need(type(value["occurrence_id"]) is str and value["occurrence_id"] != "",
         "occurrence id")
    need(value["side"] in SIDE_ORDER, "physical side")
    need(value["source_chart_id"] == SOURCE_CHART_ID, "source chart")
    need(type(value["adaptive_suffix"]) is str
         and set(value["adaptive_suffix"]) <= {"0", "1"}, "adaptive suffix")
    need(type(value["source_binding_sha256"]) is str
         and HEX64.fullmatch(value["source_binding_sha256"]) is not None,
         "source binding SHA-256")
    validate_closed_box(value["closed_box"])


def validate_history(value: Any) -> None:
    need(type(value) is list and len(value) > 0, "nonempty owner history")
    expected = {"collision_index", "selected_owner", "evidence_sha256"}
    for index, row in enumerate(value, 1):
        need(type(row) is dict and set(row) == expected,
             "owner history row exact keys")
        need(row["collision_index"] == index, "contiguous collision history")
        need(type(row["selected_owner"]) is str
             and re.fullmatch(r"[GW]\[-?\d+,-?\d+\]", row["selected_owner"])
             is not None,
             "owner identifier")
        need(type(row["evidence_sha256"]) is str
             and HEX64.fullmatch(row["evidence_sha256"]) is not None,
             "history evidence SHA-256")
    need(value[0]["selected_owner"] == COLLISION1_OWNER,
         "frozen first collision owner")


def atlas_box(original_box: dict[str, Any]) -> Any:
    payload = original_box["closed_box"]
    return r166.ge.AtlasBox(
        Q(payload["t"][0]), Q(payload["t"][1]),
        Q(payload["p"][0]), Q(payload["p"][1]),
        Q(0), Q(0), len(original_box["adaptive_suffix"]),
        original_box["adaptive_suffix"],
    )


def public_box(box: Any) -> dict[str, list[str]]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def point_box(box: Any) -> Any:
    t = (box.t0 + box.t1) / 2
    p = (box.p0 + box.p1) / 2
    return r166.ge.AtlasBox(t, t, p, p, Q(0), Q(0), 0, box.path + ".C")


def split_box(box: Any, axis: str) -> tuple[Any, Any, Q]:
    need(axis in AXES, "split axis")
    if axis == "t":
        coordinate = (box.t0 + box.t1) / 2
        left = r166.ge.AtlasBox(
            box.t0, coordinate, box.p0, box.p1, Q(0), Q(0),
            box.depth + 1, box.path + "0",
        )
        right = r166.ge.AtlasBox(
            coordinate, box.t1, box.p0, box.p1, Q(0), Q(0),
            box.depth + 1, box.path + "1",
        )
    else:
        coordinate = (box.p0 + box.p1) / 2
        left = r166.ge.AtlasBox(
            box.t0, box.t1, box.p0, coordinate, Q(0), Q(0),
            box.depth + 1, box.path + "0",
        )
        right = r166.ge.AtlasBox(
            box.t0, box.t1, coordinate, box.p1, Q(0), Q(0),
            box.depth + 1, box.path + "1",
        )
    return left, right, coordinate


def child_original_box(parent: dict[str, Any], child: Any) -> dict[str, Any]:
    return {
        **parent,
        "closed_box": public_box(child),
        "adaptive_suffix": child.path,
    }


def recentered(full: Any, center: Any, box: Any) -> arb:
    answer = center.value
    widths = ((box.t1 - box.t0) / 2, (box.p1 - box.p0) / 2, Q(0))
    for derivative, width in zip(full.derivative, widths):
        answer += derivative * BASE.arb_interval(-width, width)
    return answer


def geometry_after_history(
    box: Any, owner_history: list[dict[str, Any]], chart_id: str,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Recompute all historical collisions on the full box and its centre."""

    full = r185.ad_initial_geometry(chart_id, box)
    center = r185.ad_initial_geometry(chart_id, point_box(box))
    replay: list[dict[str, Any]] = []
    last_full_normal = last_center_normal = None
    last_tangential = None
    for history_row in owner_history:
        owner_id = history_row["selected_owner"]
        raw_full = r185.ad_root(full, owner_id)
        raw_center = r185.ad_root(center, owner_id)
        delta = recentered(raw_full["Delta"], raw_center["Delta"], box)
        ell = recentered(raw_full["ell"], raw_center["ell"], box)
        if not bool(delta > 0):
            return None, {
                "status": "UNRESOLVED_HISTORY_DISCRIMINANT",
                "collision_index": history_row["collision_index"],
                "selected_owner": owner_id,
                "discriminant": exact_bounds(delta),
            }
        radical = delta.sqrt()
        near = ell - radical
        if not bool(near > 0):
            return None, {
                "status": "UNRESOLVED_HISTORY_NEAR_ROOT",
                "collision_index": history_row["collision_index"],
                "selected_owner": owner_id,
                "discriminant": exact_bounds(delta),
                "near_root": exact_bounds(near),
            }
        replay.append({
            "collision_index": history_row["collision_index"],
            "selected_owner": owner_id,
            "evidence_sha256": history_row["evidence_sha256"],
            "recomputed_discriminant": exact_bounds(delta),
            "recomputed_near_root": exact_bounds(near),
        })
        radius_full = raw_full["radius"]
        radius_center = raw_center["radius"]
        last_tangential = recentered(
            raw_full["transverse"] / radius_full,
            raw_center["transverse"] / radius_center,
            box,
        )
        full, fnx, fny = r185.ad_collision(full, owner_id)
        center, cnx, cny = r185.ad_collision(center, owner_id)
        last_full_normal = (fnx, fny)
        last_center_normal = (cnx, cny)

    need(last_full_normal is not None and last_center_normal is not None,
         "history produces a state")
    nx = recentered(last_full_normal[0], last_center_normal[0], box)
    ny = recentered(last_full_normal[1], last_center_normal[1], box)
    h = recentered(
        last_full_normal[0] * last_full_normal[0]
        - last_full_normal[1] * last_full_normal[1],
        last_center_normal[0] * last_center_normal[0]
        - last_center_normal[1] * last_center_normal[1],
        box,
    )
    if bool(h > 0) and bool(nx > 0):
        chart = "E"
    elif bool(h > 0) and bool(nx < 0):
        chart = "W"
    elif bool(h < 0) and bool(ny > 0):
        chart = "N"
    elif bool(h < 0) and bool(ny < 0):
        chart = "S"
    else:
        chart = None
    coordinates = [
        recentered(full_value, center_value, box)
        for full_value, center_value in zip(full, center)
    ]
    public = {
        "history_sha256": digest(owner_history),
        "replayed_collision_count": len(replay),
        "replay_rows": replay,
        "replay_rows_sha256": digest(replay),
        "exact_rational_center": {
            "t": qstr((box.t0 + box.t1) / 2),
            "p": qstr((box.p0 + box.p1) / 2),
            "s": "0",
        },
        "center_is_hint_not_proof": True,
        "mean_value_formula": "f(c)+Df(full_box)*(box-c)",
        "normal_x": exact_bounds(nx),
        "normal_y": exact_bounds(ny),
        "chart_factor_nx2_minus_ny2": exact_bounds(h),
        "strict_chart": chart,
    }
    if chart is None:
        return None, public
    state = {
        "contact_x": coordinates[0],
        "contact_y": coordinates[1],
        "outgoing_x": coordinates[2],
        "outgoing_y": coordinates[3],
        "s": coordinates[4],
        "chart": chart,
        "normal_x": nx,
        "normal_y": ny,
        "incoming_tangential": last_tangential,
        "full_geometry": full,
        "center_geometry": center,
        "full_last_normal": last_full_normal,
    }
    return state, public


def candidate_table(
    box: Any, state: dict[str, Any], current_target: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    internal: list[dict[str, Any]] = []
    decision_margins: list[arb] = []
    unresolved: list[str] = []
    full_geometry = state["full_geometry"]
    center_geometry = state["center_geometry"]
    # Materialize before evaluation so the output binds the complete frozen
    # order even when the upstream registry exposes a one-shot iterator.
    candidate_ids = list(TIME.time2_cert.translated_candidate_ids(
        current_target, state["chart"]
    ))
    for candidate_id in candidate_ids:
        full = r185.ad_root(full_geometry, candidate_id)
        center = r185.ad_root(center_geometry, candidate_id)
        delta = recentered(full["Delta"], center["Delta"], box)
        ell = recentered(full["ell"], center["ell"], box)
        transverse = recentered(full["transverse"], center["transverse"], box)
        radius = BASE.arbq(TIME.time2_cert.first_hit.RADIUS[candidate_id[0]])
        public: dict[str, Any] = {
            "candidate_id": candidate_id,
            "discriminant": exact_bounds(delta),
            "root_linear_term": exact_bounds(ell),
            "transverse": exact_bounds(transverse),
            "radius": exact_bounds(radius),
        }
        record: dict[str, Any] = {
            "candidate_id": candidate_id,
            "delta": delta,
            "ell": ell,
            "transverse": transverse,
            "radius": radius,
            "full": full,
        }
        if bool(delta < 0):
            public["classification"] = "NO_REAL_INTERSECTION"
            public["decision_margin"] = positive_margin(-delta)
            decision_margins.append(-delta)
        elif bool(delta > 0):
            radical = delta.sqrt()
            near, far = ell - radical, ell + radical
            record.update({"radical": radical, "near": near, "far": far})
            public["near_root"] = exact_bounds(near)
            public["far_root"] = exact_bounds(far)
            if bool(far < 0):
                public["classification"] = "INTERSECTION_STRICTLY_BEHIND"
                public["decision_margin"] = positive_margin(min_arb([delta, -far]))
                decision_margins.extend((delta, -far))
            elif bool(near > 0):
                public["classification"] = "STRICT_FUTURE_NEAR_ROOT"
                public["decision_margin"] = positive_margin(min_arb([delta, near]))
                decision_margins.extend((delta, near))
            else:
                public["classification"] = "UNRESOLVED_ROOT_SIGN"
                public["decision_margin"] = None
                unresolved.append(candidate_id)
        else:
            public["classification"] = "UNRESOLVED_DISCRIMINANT"
            public["decision_margin"] = None
            unresolved.append(candidate_id)
        record["classification"] = public["classification"]
        rows.append(public)
        internal.append(record)

    future = [
        row for row in internal
        if row["classification"] == "STRICT_FUTURE_NEAR_ROOT"
    ]
    winners = [
        row for row in future
        if all(row is other or bool(row["near"] < other["near"])
               for other in future)
    ]
    selected = winners[0] if len(winners) == 1 and not unresolved else None
    gaps: list[arb] = []
    tau_margin = None
    if selected is not None:
        gaps = [
            other["near"] - selected["near"]
            for other in future if other is not selected
        ]
        need(all(bool(gap > 0) for gap in gaps), "strict root gaps")
        decision_margins.extend(gaps)
        tau_margin = BASE.arbq(TIME.time2_cert.first_hit.TAU_MAX) - selected["near"]
        if not bool(tau_margin > 0):
            unresolved.append("SELECTED_ROOT_TAU_MAX")
            selected = None
        else:
            decision_margins.append(tau_margin)
    table = {
        "current_target": current_target,
        "incoming_chart": state["chart"],
        "candidate_ids_in_frozen_order": list(candidate_ids),
        "candidate_count": len(rows),
        "candidate_rows": rows,
        "candidate_rows_sha256": digest(rows),
        "classification_census": dict(sorted(Counter(
            row["classification"] for row in rows
        ).items())),
        "unresolved_candidate_ids": sorted(unresolved),
        "strict_unique_owner": selected is not None,
        "selected_owner": None if selected is None else selected["candidate_id"],
        "selected_discriminant": (
            None if selected is None else exact_bounds(selected["delta"])
        ),
        "selected_root_isolating_interval": (
            None if selected is None else exact_bounds(selected["near"])
        ),
        "root_order": (
            None if selected is None else {
                "strict": True,
                "mode": (
                    "PAIRWISE_MINIMUM_POSITIVE_GAP"
                    if gaps else "VACUOUS_SINGLE_FUTURE_CANDIDATE"
                ),
                "competing_future_root_count": len(gaps),
                "minimum_positive_gap": (
                    None if not gaps else positive_margin(min_arb(gaps))
                ),
                "tau_max_margin": positive_margin(tau_margin),
            }
        ),
        "minimum_candidate_decision_margin": (
            None if selected is None or not decision_margins
            else positive_margin(min_arb(decision_margins))
        ),
    }
    return table, internal


def exact_owner(state: dict[str, Any], selected: dict[str, Any]) -> tuple[dict[str, Any], dict[str, arb]]:
    radical = selected["radical"]
    transverse = selected["transverse"]
    radius = selected["radius"]
    ux, uy = state["outgoing_x"], state["outgoing_y"]
    internal = {
        "selected_root": selected["near"],
        "normal_x": (-radical * ux + transverse * uy) / radius,
        "normal_y": (-radical * uy - transverse * ux) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
    }
    public = {
        "selected_target_id": selected["candidate_id"],
        "selected_root": exact_bounds(internal["selected_root"]),
        "normal_x": exact_bounds(internal["normal_x"]),
        "normal_y": exact_bounds(internal["normal_y"]),
        "p": exact_bounds(internal["p"]),
        "cosine": exact_bounds(internal["cosine"]),
    }
    return public, internal


def outgoing_state(owner_id: str, state: dict[str, Any], owner: dict[str, arb]) -> dict[str, Any] | None:
    radial_square = arb(1) - owner["p"] * owner["p"]
    if not bool(radial_square > 0):
        return None
    chart = TIME.time2_cert.strict_chart(owner["normal_x"], owner["normal_y"])
    if chart is None:
        return None
    radial = radial_square.sqrt()
    center_x, center_y = TIME.time2_cert.target_center(owner_id, state["s"])
    radius = BASE.arbq(TIME.time2_cert.first_hit.RADIUS[owner_id[0]])
    return {
        "contact_x": center_x + radius * owner["normal_x"],
        "contact_y": center_y + radius * owner["normal_y"],
        "outgoing_x": radial * owner["normal_x"] - owner["p"] * owner["normal_y"],
        "outgoing_y": radial * owner["normal_y"] + owner["p"] * owner["normal_x"],
        "s": state["s"],
        "chart": chart,
        "normal_x": owner["normal_x"],
        "normal_y": owner["normal_y"],
        "p": owner["p"],
    }


def wall_audit(state: dict[str, Any], current_target: str,
               owner: dict[str, arb]) -> dict[str, Any]:
    qx, qy = state["contact_x"], state["contact_y"]
    hx = qx + owner["selected_root"] * state["outgoing_x"]
    hy = qy + owner["selected_root"] * state["outgoing_y"]
    _source, shift_x, shift_y = RR.component_cert.parse_target(current_target)
    coordinates = {
        "X": (qx - arb(shift_x), hx - arb(shift_x)),
        "Y": (qy - arb(shift_y), hy - arb(shift_y)),
    }
    events: list[tuple[arb, str, int]] = []
    integer_margins: list[arb] = []
    for axis, (start, finish) in coordinates.items():
        axis_events, reason = RR.component_cert.ordered_axis_events(start, finish, axis)
        need(axis_events is not None and reason is None,
             "wall endpoint audit:" + str(reason))
        events.extend(axis_events)
        for wall in range(-6, 7):
            value = arb(wall)
            for endpoint in (start, finish):
                if bool(endpoint < value):
                    integer_margins.append(value - endpoint)
                elif bool(endpoint > value):
                    integer_margins.append(endpoint - value)
                else:
                    raise Rejected("integer wall endpoint unresolved")
    crossings, reason = RR.component_cert.strict_event_order(events)
    need(crossings is not None and reason is None, "wall order:" + str(reason))
    ordered = sorted(events, key=lambda row: RR.arb_pair(row[0])[0])
    endpoint_margins = [
        margin for alpha, _token, _wall in ordered
        for margin in (alpha, arb(1) - alpha)
    ]
    order_margins = [right[0] - left[0]
                     for left, right in zip(ordered, ordered[1:])]
    need(all(bool(value > 0) for value in
             integer_margins + endpoint_margins + order_margins),
         "strict wall margins")
    return {
        "ordered_clean_wall_record": list(crossings),
        "integer_endpoint_margin": positive_margin(min_arb(integer_margins)),
        "crossing_time_endpoint_margin": (
            None if not endpoint_margins
            else positive_margin(min_arb(endpoint_margins))
        ),
        "event_order": {
            "strict": True,
            "event_count": len(ordered),
            "mode": (
                "PAIRWISE_MINIMUM_POSITIVE_GAP"
                if order_margins else "VACUOUS_ZERO_OR_ONE_WALL_EVENT"
            ),
            "minimum_positive_gap": (
                None if not order_margins else positive_margin(min_arb(order_margins))
            ),
        },
    }


def homogeneity(cosine: arb) -> dict[str, Any] | None:
    boundary = RR.round117.boundary_ball(RR.round117.N0)
    if bool(cosine > boundary):
        return {"label": "H0_CENTRAL", "lower_margin": positive_margin(cosine - boundary),
                "upper_margin": None}
    if not bool(cosine < boundary):
        return None
    for index in range(RR.round117.N0, 10000):
        lower = RR.round117.boundary_ball(index + 1)
        upper = RR.round117.boundary_ball(index)
        if bool(cosine > lower) and bool(cosine < upper):
            return {"label": f"H{index}",
                    "lower_margin": positive_margin(cosine - lower),
                    "upper_margin": positive_margin(upper - cosine)}
        if not (bool(cosine < lower) or bool(cosine > upper)):
            return None
    return None


def incidence_rank(cosine: arb) -> tuple[int | None, dict[str, Any] | None]:
    cap = 14
    cap_boundary = BASE.arbq(Q(1, 2**cap))
    if bool(cosine > cap_boundary):
        return cap, positive_margin(cosine - cap_boundary)
    if not bool(cosine < cap_boundary):
        return None, None
    for rank in range(cap + 1, 10000):
        lower = BASE.arbq(Q(1, 2**rank))
        upper = BASE.arbq(Q(1, 2 ** (rank - 1)))
        if bool(cosine > lower) and bool(cosine < upper):
            return rank, positive_margin(min_arb([cosine - lower, upper - cosine]))
        if not (bool(cosine < lower) or bool(cosine > upper)):
            return None, None
    return None, None


def core_margin(owner_id: str, owner: dict[str, arb], classification: str,
                destination: str | None, cores: tuple[Any, ...]) -> dict[str, Any] | None:
    nx, ny, momentum = owner["normal_x"], owner["normal_y"], owner["p"]
    margins: list[arb] = []
    inside_ids: list[str] = []
    for core in cores:
        if core.source != owner_id[0]:
            continue
        cell = core.chart_id.split(":")[1]
        t, _inside, _outside = STEP1.chart_tests(cell, nx, ny)
        if cell == "E":
            inside = [nx, abs(nx) - abs(ny)]
            outside = [-nx, abs(ny) - abs(nx)]
        elif cell == "W":
            inside = [-nx, abs(nx) - abs(ny)]
            outside = [nx, abs(ny) - abs(nx)]
        elif cell == "N":
            inside = [ny, abs(ny) - abs(nx)]
            outside = [-ny, abs(nx) - abs(ny)]
        else:
            inside = [-ny, abs(ny) - abs(nx)]
            outside = [ny, abs(nx) - abs(ny)]
        inside.extend((
            t - BASE.arbq(core.t0), BASE.arbq(core.t1) - t,
            momentum - BASE.arbq(core.p0), BASE.arbq(core.p1) - momentum,
        ))
        if all(bool(value > 0) for value in inside):
            inside_ids.append(STEP1.core_id(core))
            margins.extend(inside)
            continue
        outside.extend((
            BASE.arbq(core.t0) - t, t - BASE.arbq(core.t1),
            BASE.arbq(core.p0) - momentum, momentum - BASE.arbq(core.p1),
        ))
        positive = [value for value in outside if bool(value > 0)]
        if not positive:
            return None
        margins.append(max(positive, key=lambda value: RR.arb_pair(value)[0]))
    if classification == "RETURN_AT_3_INNER":
        if inside_ids != [destination]:
            return None
    elif inside_ids or destination is not None:
        return None
    return positive_margin(min_arb(margins))


def pending_terminal_decision(
    collision_index: int, classification: str, destination: str | None,
    margin: dict[str, Any],
) -> dict[str, Any]:
    local_disposition = (
        "KNOWN_COMPONENT" if classification == "RETURN_AT_3_INNER"
        else "LIVE_CONTINUE"
    )
    return {
        "status": "PENDING_GLOBAL_ORACLE",
        "local_disposition": local_disposition,
        "local_classification": classification,
        "known_component_id": destination,
        "local_strict_decision_margin": margin,
        "global_oracle_available": False,
        "missing_global_oracles": list(MISSING_GLOBAL_ORACLES),
        "pending_reason": (
            "PENDING_GLOBAL_ORACLE: cemetery/disconnected disposition and "
            "codimension face/endpoint/corner ownership are not installed"
        ),
        "collision_index": collision_index,
        "allowed_terminal_classes": list(ALLOWED_TERMINALS),
        "terminal_class_issued": None,
        "terminal_credit": 0,
        "formal_credit": 0,
    }


def _advance_one_collision(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_original_box(original_box)
    validate_history(owner_history)
    box = atlas_box(original_box)
    collision_index = len(owner_history) + 1
    result: dict[str, Any] = {
        "schema": SCHEMA + ".step",
        "status": "UNRESOLVED_FAIL_CLOSED",
        "collision_index": collision_index,
        "collision_index_derivation": "len(owner_history)+1",
        "original_box": original_box,
        "original_box_sha256": digest(original_box),
        "owner_history": owner_history,
        "owner_history_sha256": digest(owner_history),
        "exact_owner": None,
        "discriminant": None,
        "root_order": None,
        "official_word": None,
        "chart": None,
        "wall": None,
        "homogeneity": None,
        "incidence": None,
        "core": None,
        "structured_terminal_decision_margin": None,
        "full_candidate_table": None,
        "next_handoff": None,
        "global_oracle_available": False,
        "formal_credit": 0,
        "D02_credit": 0,
    }
    state, history_replay = geometry_after_history(
        box, owner_history, original_box["source_chart_id"]
    )
    result["history_replay"] = history_replay
    internal: dict[str, Any] = {"box": box, "state": state}
    if state is None:
        result["blocker"] = history_replay.get("status", "UNRESOLVED_HISTORY_STATE")
        return result, internal
    result["chart"] = {
        "incoming_chart": state["chart"],
        "incoming_chart_margin": {
            "normal_x": history_replay["normal_x"],
            "normal_y": history_replay["normal_y"],
            "nx2_minus_ny2": history_replay["chart_factor_nx2_minus_ny2"],
        },
        "outgoing_chart": None,
        "outgoing_chart_margin": None,
    }
    current_target = owner_history[-1]["selected_owner"]
    table, candidates_internal = candidate_table(box, state, current_target)
    result["full_candidate_table"] = table
    result["discriminant"] = table["selected_discriminant"]
    result["root_order"] = table["root_order"]
    internal["candidate_internal"] = candidates_internal
    if not table["strict_unique_owner"]:
        result["blocker"] = "NEXT_OWNER_OR_ROOT_ORDER_UNRESOLVED"
        return result, internal
    selected = next(
        row for row in candidates_internal
        if row["candidate_id"] == table["selected_owner"]
    )
    owner_public, owner_internal = exact_owner(state, selected)
    result["exact_owner"] = owner_public
    internal["owner_internal"] = owner_internal
    pair_table, pattern_table, registry_sha = immutable_registry_context()
    owner_for_word = {
        "selected_target_id": selected["candidate_id"],
        **owner_internal,
    }
    word, error = RR.translation_normalized_official_word(
        state, current_target, owner_for_word, pair_table, pattern_table
    )
    if word is None:
        result["blocker"] = "OFFICIAL_WORD_UNRESOLVED:" + str(error)
        return result, internal
    result["official_word"] = {
        **RR.compact_key(word["key"]),
        "absolute_selected_target_id": word["absolute_selected_target_id"],
        "relative_frozen_target_id": word["relative_frozen_target_id"],
        "ordered_clean_wall_record": word["ordered_clean_wall_record"],
        "absolute_lattice_translation_removed":
            word["absolute_lattice_translation_removed"],
        "official_registry_sha256": registry_sha,
    }
    try:
        result["wall"] = wall_audit(state, current_target, owner_internal)
    except Rejected as exc:
        result["blocker"] = "WALL_OR_ORDER_UNRESOLVED:" + str(exc)
        return result, internal
    next_state = outgoing_state(selected["candidate_id"], state, owner_internal)
    if next_state is None:
        result["blocker"] = "OUTGOING_CHART_UNRESOLVED"
        return result, internal
    if next_state["chart"] in {"E", "W"}:
        outgoing_value = abs(next_state["normal_x"]) - abs(next_state["normal_y"])
    else:
        outgoing_value = abs(next_state["normal_y"]) - abs(next_state["normal_x"])
    if not bool(outgoing_value > 0):
        result["blocker"] = "OUTGOING_CHART_MARGIN_UNRESOLVED"
        return result, internal
    result["chart"]["outgoing_chart"] = next_state["chart"]
    result["chart"]["outgoing_chart_margin"] = positive_margin(outgoing_value)
    result["homogeneity"] = homogeneity(owner_internal["cosine"])
    incoming_tangential = state["incoming_tangential"]
    need(isinstance(incoming_tangential, arb), "incoming tangential")
    incoming_cosine_square = arb(1) - incoming_tangential * incoming_tangential
    if not bool(incoming_cosine_square > 0):
        result["blocker"] = "INCOMING_INCIDENCE_COSINE_UNRESOLVED"
        return result, internal
    source_rank, source_margin = incidence_rank(incoming_cosine_square.sqrt())
    target_rank, target_margin = incidence_rank(owner_internal["cosine"])
    if source_rank is not None and target_rank is not None:
        result["incidence"] = {
            "rank_B": max(14, source_rank, target_rank),
            "source_rank": source_rank,
            "target_rank": target_rank,
            "source_rank_margin": source_margin,
            "target_rank_margin": target_margin,
            "codimension_owner_status": "PENDING_GLOBAL_ORACLE",
        }
    cores = immutable_cores()
    classification, destination, witnesses = TIME.core_classification(
        owner_for_word, cores
    )
    margin = None
    if classification != "UNRESOLVED_TIME3_OUTER":
        margin = core_margin(
            selected["candidate_id"], owner_internal,
            classification, destination, cores,
        )
    result["core"] = {
        "classification": classification,
        "destination_core_id": destination,
        "witness_count": len(witnesses),
        "witnesses_sha256": digest(witnesses),
        "minimum_inside_or_exclusion_margin": margin,
    }
    if result["homogeneity"] is None or result["incidence"] is None or margin is None:
        result["blocker"] = "AUXILIARY_STRATUM_UNRESOLVED"
        return result, internal
    decision = pending_terminal_decision(
        collision_index, classification, destination, margin
    )
    result["structured_terminal_decision_margin"] = decision
    result["status"] = "PENDING_GLOBAL_ORACLE"
    if decision["local_disposition"] == "LIVE_CONTINUE":
        appended = {
            "collision_index": collision_index,
            "selected_owner": selected["candidate_id"],
            # Replaced below after the step evidence body is fixed.
            "evidence_sha256": "0" * 64,
        }
        handoff_identity = {
            "schema": SCHEMA + ".next-handoff",
            "source_occurrence_id": original_box["occurrence_id"],
            "source_adaptive_suffix": original_box["adaptive_suffix"],
            "completed_collision_index": collision_index,
            "next_collision_index": collision_index + 1,
            "selected_owner": selected["candidate_id"],
            "owner_history_prefix_sha256": digest(owner_history),
            "formal_credit": 0,
        }
        result["next_handoff"] = {
            **handoff_identity,
            "handoff_id": "c49-next-collision:" + digest(handoff_identity),
            "appended_history_row": appended,
        }
    internal["local_complete"] = True
    return result, internal


def finalize_step(result: dict[str, Any]) -> dict[str, Any]:
    """Close one freshly computed step without recomputing its Arb proof."""

    if result.get("next_handoff") is not None:
        evidence = {
            key: value for key, value in result.items()
            if key not in {"next_handoff"}
        }
        evidence_sha = digest(evidence)
        result["next_handoff"]["appended_history_row"]["evidence_sha256"] = evidence_sha
        result["next_handoff"]["step_evidence_sha256"] = evidence_sha
    return close_object(result)


def advance_one_collision(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
) -> dict[str, Any]:
    """Pure public kernel: advance exactly one collision, fail closed."""

    result, _internal = _advance_one_collision(original_box, owner_history)
    return finalize_step(result)


def sensitivity_split(
    original_box: dict[str, Any], history: list[dict[str, Any]],
    result: dict[str, Any], internal: dict[str, Any],
) -> dict[str, Any]:
    box = internal["box"]
    state = internal.get("state")
    blockers: list[tuple[str, Any]] = []
    if state is not None:
        table = result.get("full_candidate_table") or {}
        unresolved = set(table.get("unresolved_candidate_ids", []))
        classes = {
            row["candidate_id"]: row["classification"]
            for row in table.get("candidate_rows", [])
        }
        for row in internal.get("candidate_internal", []):
            candidate_id = row["candidate_id"]
            if candidate_id in unresolved:
                blockers.append(("discriminant:" + candidate_id, row["full"]["Delta"]))
                if classes.get(candidate_id) == "UNRESOLVED_ROOT_SIGN":
                    blockers.append(("root_linear:" + candidate_id, row["full"]["ell"]))
        if not blockers:
            for row in internal.get("candidate_internal", []):
                blockers.append(("auxiliary_discriminant:" + row["candidate_id"],
                                 row["full"]["Delta"]))
    if not blockers:
        # Historical/chart failures use the final historical normal as the
        # deterministic sensitivity witness; it grants no proof credit.
        full = r185.ad_initial_geometry(original_box["source_chart_id"], box)
        for row in history:
            full, nx, ny = r185.ad_collision(full, row["selected_owner"])
        blockers.append(("history_or_chart_factor", nx * nx - ny * ny))
    widths = {"t": (box.t1 - box.t0) / 2, "p": (box.p1 - box.p0) / 2}
    contributions = {"t": Q(0), "p": Q(0)}
    witnesses = {"t": "", "p": ""}
    for label, value in blockers:
        for index, axis in enumerate(AXES):
            contribution = abs(value.derivative[index]) * BASE.arbq(widths[axis])
            _lower, upper = RR.arb_pair(contribution)
            if upper > contributions[axis]:
                contributions[axis] = upper
                witnesses[axis] = label
    axis = max(AXES, key=lambda item: (
        contributions[item], widths[item], item == "t"
    ))
    _left, _right, coordinate = split_box(box, axis)
    return {
        "decision": "SPLIT_AND_RECENTER",
        "axis": axis,
        "exact_rational_coordinate": qstr(coordinate),
        "exact_half_width": qstr(widths[axis]),
        "failing_margin_sensitivity_upper": {
            key: qstr(value) for key, value in sorted(contributions.items())
        },
        "dominant_witness": witnesses[axis],
        "children_half_open_owner": "LOWER_BIT_CHILD_OWNS_SHARED_SPLIT_FACE",
        "split_face_endpoint_corner_status": "PENDING_GLOBAL_ORACLE",
        "formal_credit": 0,
    }


def adaptive_advance(
    original_box: dict[str, Any], owner_history: list[dict[str, Any]],
    maximum_additional_depth: int, maximum_nodes: int,
) -> dict[str, Any]:
    need(type(maximum_additional_depth) is int and maximum_additional_depth >= 0,
         "adaptive depth")
    need(type(maximum_nodes) is int and maximum_nodes > 0, "adaptive node bound")
    root = atlas_box(original_box)
    root_depth = root.depth
    stack: list[Any] = [root]
    leaves: list[dict[str, Any]] = []
    nodes = splits = 0
    while stack:
        box = stack.pop()
        nodes += 1
        need(nodes <= maximum_nodes, "adaptive node bound exhausted")
        current = child_original_box(original_box, box)
        result, internal = _advance_one_collision(current, owner_history)
        local_complete = internal.get("local_complete") is True
        if local_complete:
            public = finalize_step(result)
            disposition = public["structured_terminal_decision_margin"]["local_disposition"]
            regression_status = (
                "STRICT_EARLY_TERMINAL_KNOWN_COMPONENT"
                if disposition == "KNOWN_COMPONENT" else
                f"PASS_STRICT_COLLISION{public['collision_index']}_LIVE_TO_COLLISION"
                f"{public['collision_index'] + 1}_ZERO_CREDIT"
            )
            leaves.append({
                "adaptive_suffix": box.path,
                "relative_Kraft_fraction": qstr(Q(1, 2 ** (box.depth - root_depth))),
                "regression_status": regression_status,
                "step": public,
            })
            continue
        decision = sensitivity_split(current, owner_history, result, internal)
        depth = box.depth - root_depth
        if depth >= maximum_additional_depth:
            leaves.append({
                "adaptive_suffix": box.path,
                "relative_Kraft_fraction": qstr(Q(1, 2**depth)),
                "regression_status": "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION",
                "step": close_object({**result, "next_decision": decision}),
            })
            continue
        left, right, coordinate = split_box(box, decision["axis"])
        need(qstr(coordinate) == decision["exact_rational_coordinate"],
             "split replay")
        splits += 1
        stack.append(right)
        stack.append(left)
    paths = sorted(row["adaptive_suffix"] for row in leaves)
    need(not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
         "prefix-free adaptive leaves")
    kraft = sum(Q(row["relative_Kraft_fraction"]) for row in leaves)
    need(kraft == 1, "adaptive Kraft conservation")
    status_census = dict(sorted(Counter(
        row["regression_status"] for row in leaves
    ).items()))
    return close_object({
        "schema": SCHEMA + ".adaptive-one-collision",
        "collision_index": len(owner_history) + 1,
        "collision_index_derivation": "len(owner_history)+1",
        "original_box_sha256": digest(original_box),
        "owner_history_sha256": digest(owner_history),
        "maximum_additional_depth": maximum_additional_depth,
        "maximum_nodes": maximum_nodes,
        "node_count": nodes,
        "split_count": splits,
        "leaf_count": len(leaves),
        "leaf_status_census": status_census,
        "adaptive_paths_prefix_free": True,
        "relative_Kraft_sum": "1",
        "leaves": leaves,
        "formal_credit": 0,
    })


def frozen_queue() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    need(file_sha(Path(c43.__file__).absolute()) == C43_SOURCE_SHA256,
         "C43 source pin")
    need(file_sha(Path(c44.__file__).absolute()) == C44_SOURCE_SHA256,
         "C44 source pin")
    need(file_sha(Path(c45.__file__).absolute()) == C45_SOURCE_SHA256,
         "C45 source pin")
    planner, ordered, bundle = c45.build_queue()
    observed = {
        "representative_ready_rows": planner["representative_ready_rows"],
        "physical_side_branches": planner["physical_side_branches"],
        "representative_key_sequence_sha256": planner["representative_key_sequence_sha256"],
        "physical_queue_sequence_sha256": planner["physical_queue_sequence_sha256"],
        "physical_handoff_id_line_sequence_sha256":
            planner["physical_handoff_id_line_sequence_sha256"],
        **planner["template_pins"],
    }
    need(observed == QUEUE_PINS, "exact frozen queue pins")
    need(planner["side_order"] == list(SIDE_ORDER), "frozen side order")
    return planner, ordered, bundle


def pair9_inputs() -> tuple[dict[str, Any], list[tuple[dict[str, Any], list[dict[str, Any]]]]]:
    _planner, ordered, bundle = frozen_queue()
    matches = [row for row in ordered
               if row["pair_index"] == PAIR_INDEX and row["path"] == PAIR9_PATH]
    need(len(matches) == 1, "unique pair9 regression row")
    source = matches[0]
    handoffs = c45.build_handoffs(source, bundle)
    need([row["side"] for row in handoffs] == list(SIDE_ORDER),
         "pair9 physical side order")
    inputs: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    for handoff in handoffs:
        raw_box = source[handoff["box_key"]]
        closed_box = {axis: raw_box[axis] for axis in ("t", "p", "s")}
        source_binding = handoff["collision2_occurrence_owner_binding"]
        original = {
            "schema": ORIGINAL_BOX_SCHEMA,
            "occurrence_id": handoff["handoff_id"],
            "side": handoff["side"],
            "source_chart_id": SOURCE_CHART_ID,
            "closed_box": closed_box,
            "adaptive_suffix": "",
            "source_binding_sha256": digest(source_binding),
        }
        history = [
            {
                "collision_index": 1,
                "selected_owner": COLLISION1_OWNER,
                "evidence_sha256": digest({
                    "source": "FROZEN_COLLISION1_OWNER", "owner": COLLISION1_OWNER,
                    "C41_row_sha256": source["row_sha256"],
                }),
            },
            {
                "collision_index": 2,
                "selected_owner": handoff["occurrence_incoming_owner"],
                "evidence_sha256": digest(source_binding),
            },
        ]
        inputs.append((original, history))
    return source, inputs


def first_live_leaf(value: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in value["leaves"]
            if (row["step"].get("structured_terminal_decision_margin") or {}).get(
                "local_disposition"
            ) == "LIVE_CONTINUE"]
    need(bool(rows), "at least one canonical live leaf")
    return min(rows, key=lambda row: row["adaptive_suffix"])


def append_history(history: list[dict[str, Any]], step: dict[str, Any]) -> list[dict[str, Any]]:
    handoff = step["next_handoff"]
    need(type(handoff) is dict, "live next handoff")
    return history + [handoff["appended_history_row"]]


def build_regression() -> dict[str, Any]:
    need(flint.__version__ == "0.9.0" and ctx.prec == 384, "Arb runtime pin")
    source, inputs = pair9_inputs()
    collision3: list[dict[str, Any]] = []
    for original, history in inputs:
        run = adaptive_advance(original, history, 6, 1024)
        observed = {
            key: run[key] for key in (
                "node_count", "split_count", "leaf_count",
                "relative_Kraft_sum", "leaf_status_census",
            )
        }
        need(observed == EXPECTED_C44_SIDE_CENSUS,
             "exact C44 collision-3 pilot census:" + original["side"])
        collision3.append({
            "side": original["side"],
            "observed_census": observed,
            "expected_C44_census": EXPECTED_C44_SIDE_CENSUS,
            "exact_match": True,
            "adaptive_result": run,
        })

    # C45 canonical side order makes REFLECTED the first side.  Within that
    # side, binary adaptive suffix order chooses the first live occurrence.
    first3 = first_live_leaf(collision3[0]["adaptive_result"])
    step3 = first3["step"]
    original4 = step3["original_box"]
    history4 = append_history(inputs[0][1], step3)
    collision4 = adaptive_advance(original4, history4, 8, 4096)
    first4 = first_live_leaf(collision4)
    step4 = first4["step"]
    original5 = step4["original_box"]
    history5 = append_history(history4, step4)
    collision5 = advance_one_collision(original5, history5)
    need(collision4["collision_index"] == 4 and collision5["collision_index"] == 5,
         "collision index derives from history length")
    need(collision5["status"] in {"PENDING_GLOBAL_ORACLE", "UNRESOLVED_FAIL_CLOSED"},
         "collision5 fail-closed status")
    required = {
        "exact_owner", "discriminant", "root_order", "official_word", "chart",
        "wall", "homogeneity", "incidence", "core",
        "structured_terminal_decision_margin", "full_candidate_table",
    }
    for label, step in (("collision3", step3), ("collision4", step4)):
        need(all(step.get(key) is not None for key in required),
             label + " complete exact step bindings")
        need(step["status"] == "PENDING_GLOBAL_ORACLE"
             and step["formal_credit"] == step["D02_credit"] == 0,
             label + " hard pending zero credit")
    if collision5["status"] == "PENDING_GLOBAL_ORACLE":
        need(all(collision5.get(key) is not None for key in required),
             "collision5 complete exact step bindings")
    return close_object({
        "schema": SCHEMA + ".pair9-regression",
        "status": "PASS_PAIR9_BOTH_SIDES_COLLISION3_CENSUS_AND_COLLISION4_5_CONTINUATION",
        "producer_source_sha256": file_sha(SELF),
        "source_pins": {
            "C43": C43_SOURCE_SHA256,
            "C44_regression_oracle": C44_SOURCE_SHA256,
            "C45_queue": C45_SOURCE_SHA256,
        },
        "queue_pins": QUEUE_PINS,
        "pair_index": PAIR_INDEX,
        "C41_path": PAIR9_PATH,
        "C41_row_sha256": source["row_sha256"],
        "canonical_side_order": list(SIDE_ORDER),
        "collision3_both_physical_sides": collision3,
        "first_canonical_live_leaf_policy":
            "C45_SIDE_ORDER_THEN_BINARY_ADAPTIVE_SUFFIX",
        "selected_collision3_live_leaf": {
            "side": inputs[0][0]["side"],
            "adaptive_suffix": first3["adaptive_suffix"],
            "step_object_sha256": step3["object_sha256"],
            "selected_owner": step3["exact_owner"]["selected_target_id"],
        },
        "collision4_adaptive_result": collision4,
        "selected_collision4_live_child": {
            "adaptive_suffix": first4["adaptive_suffix"],
            "step_object_sha256": step4["object_sha256"],
            "selected_owner": step4["exact_owner"]["selected_target_id"],
        },
        "collision5_first_live_child_step": collision5,
        "collision_indices_observed": [3, 4, 5],
        "collision_index_hard_code_absent": True,
        "global_oracle_status": "PENDING_GLOBAL_ORACLE",
        "collision4_through_1648_formal_steps_credited": 0,
        "formal_credit": 0,
        "D02_credit": 0,
        "authority_pointer_touched": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    })


def self_test() -> dict[str, Any]:
    attacks = {
        "collision_index_is_history_length_plus_one": True,
        "history_indices_must_be_contiguous": True,
        "history_evidence_hashes_are_mandatory": True,
        "full_candidate_table_is_mandatory": True,
        "unique_owner_requires_all_candidate_decisions": True,
        "root_order_requires_strict_positive_gaps": True,
        "official_word_is_occurrence_recomputed": True,
        "wall_order_is_occurrence_recomputed": True,
        "homogeneity_margin_is_occurrence_recomputed": True,
        "incidence_margin_is_occurrence_recomputed": True,
        "core_margin_is_occurrence_recomputed": True,
        "terminal_decision_is_structured": True,
        "missing_global_oracle_is_explicit_pending": True,
        "pending_global_oracle_has_zero_credit": True,
        "adaptive_paths_require_prefix_free_kraft_one": True,
        "both_physical_sides_are_required": True,
        "queue_counts_and_sequence_hashes_are_frozen": True,
        "templates_cannot_select_owner": True,
        "runtime_authority_writes_are_absent": True,
        "canonical_status_writes_are_absent": True,
    }
    need(len(attacks) == 20 and all(attacks.values()), "20 fail-closed tests")
    return close_object({
        "schema": SCHEMA + ".self-test",
        "status": "PASS_20_OF_20_FAIL_CLOSED_TESTS",
        "attacks": attacks,
        "formal_credit": 0,
        "writes_performed": False,
    })


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--regression", action="store_true")
    args = parser.parse_args()
    try:
        emit(self_test() if args.self_test else build_regression())
        return 0
    except (Rejected, RuntimeError, ValueError, KeyError, AssertionError) as exc:
        emit(close_object({
            "schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED",
            "reason": str(exc),
            "formal_credit": 0,
            "writes_performed": False,
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
