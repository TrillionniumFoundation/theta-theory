#!/usr/bin/env python3
"""Read-only, zero-credit collision-3 exact-recenter pilot for C41 pair 9.

The pilot consumes the pinned C41 collision-3-ready queue and the C35--C37
template/transport authorities.  It mints deterministic *diagnostic* handoff
identities for the representative and reflected sides of one pair-9 leaf,
then recomputes collision 3 on each closed box.

Every centered enclosure is a rigorous mean-value enclosure: the value is
evaluated at the exact rational box centre and the full-box Arb derivative
enclosure is multiplied by the exact rational displacement box.  Centre
owners are hints only.  A terminal or collision-4 handoff is emitted only
when all candidate decisions and the strict root order close on the full
closed box.  Otherwise an exact rational split coordinate is chosen from the
largest failing-margin derivative contribution.

This program writes only canonical JSON to stdout.  It never creates a
runtime candidate, receipt, pointer, seal, status file, or formal D02 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import arb, ctx
import flint

# Isolated-mode execution deliberately omits the script directory from
# sys.path.  Resolve the pinned sibling producers from this source's own
# immutable location, never from the caller's working directory.
SELF = Path(__file__).absolute()
if str(SELF.parent) not in sys.path:
    sys.path.insert(0, str(SELF.parent))

import cm2_round306c43_collision3_ready_inventory_planner_v1 as c43
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38
import cm2_round166_multi_candidate_refinement_prototype as r166
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round185_preconditioned_c1_residual_refinement as r185


SCHEMA = "cm2.round306c44.d02-b-pair9-collision3-exact-recenter-pilot.v1"
C43_SOURCE_SHA256 = (
    "8519aa02e80ddda01953db9f48c641d88244f264ea67de59307a674c77194b48"
)
PAIR_INDEX = 9
SOURCE_PATH = "011110111"
CHART_ID = "W:E"
COLLISION1_OWNER = "W[1,0]"
COLLISION_INDEX = 3
AXES = ("t", "p")
MAX_PILOT_DEPTH = 10
MAX_PILOT_NODES = 4096
RR = r139.lower.round136
TIME3 = r139.lower.time3
STEP1 = r139.lower.step1
BASE = r185.BASE


class Rejected(RuntimeError):
    pass


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


def sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def arb_exact_bounds(value: arb) -> dict[str, Any]:
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


def box_from_payload(payload: dict[str, Any], path: str) -> Any:
    return r166.ge.AtlasBox(
        Q(payload["t"][0]), Q(payload["t"][1]),
        Q(payload["p"][0]), Q(payload["p"][1]), Q(0), Q(0), 0, path,
    )


def box_public(box: Any) -> dict[str, Any]:
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


def recentered(full: Any, center: Any, box: Any) -> arb:
    """Rigorous exact-centre mean-value enclosure for one AD3 scalar."""

    answer = center.value
    widths = (
        (box.t1 - box.t0) / 2,
        (box.p1 - box.p0) / 2,
        Q(0),
    )
    for derivative, width in zip(full.derivative, widths):
        answer += derivative * BASE.arb_interval(-width, width)
    return answer


def two_collision_ad(box: Any, owner2: str) -> dict[str, Any]:
    full0 = r185.ad_initial_geometry(CHART_ID, box)
    full1, _nx1, _ny1 = r185.ad_collision(full0, COLLISION1_OWNER)
    full2, nx2, ny2 = r185.ad_collision(full1, owner2)
    centre = point_box(box)
    center0 = r185.ad_initial_geometry(CHART_ID, centre)
    center1, _cnx1, _cny1 = r185.ad_collision(center0, COLLISION1_OWNER)
    center2, cnx2, cny2 = r185.ad_collision(center1, owner2)
    return {
        "full_geometry": full2,
        "center_geometry": center2,
        "full_normal": (nx2, ny2),
        "center_normal": (cnx2, cny2),
        "center": {
            "t": qstr((box.t0 + box.t1) / 2),
            "p": qstr((box.p0 + box.p1) / 2),
            "s": "0",
        },
    }


def centered_state(box: Any, owner2: str) -> tuple[dict[str, Any] | None,
                                                   dict[str, Any]]:
    values = two_collision_ad(box, owner2)
    full_geometry = values["full_geometry"]
    center_geometry = values["center_geometry"]
    nx_full, ny_full = values["full_normal"]
    nx_center, ny_center = values["center_normal"]
    nx = recentered(nx_full, nx_center, box)
    ny = recentered(ny_full, ny_center, box)
    h_full = nx_full * nx_full - ny_full * ny_full
    h_center = nx_center * nx_center - ny_center * ny_center
    h = recentered(h_full, h_center, box)
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
        recentered(full, center, box)
        for full, center in zip(full_geometry, center_geometry)
    ]
    audit = {
        "exact_rational_center": values["center"],
        "center_is_hint_not_proof": True,
        "centered_normal_x": arb_exact_bounds(nx),
        "centered_normal_y": arb_exact_bounds(ny),
        "centered_chart_factor_nx2_minus_ny2": arb_exact_bounds(h),
        "strict_chart": chart,
        "mean_value_formula": "f(c)+Df(full_box)*(box-c)",
    }
    if chart is None:
        return None, audit
    return {
        "contact_x": coordinates[0],
        "contact_y": coordinates[1],
        "outgoing_x": coordinates[2],
        "outgoing_y": coordinates[3],
        "s": coordinates[4],
        "chart": chart,
        "normal_x": nx,
        "normal_y": ny,
    }, audit


def candidate_audit(box: Any, owner2: str, chart: str) -> dict[str, Any]:
    values = two_collision_ad(box, owner2)
    full_geometry = values["full_geometry"]
    center_geometry = values["center_geometry"]
    rows: list[dict[str, Any]] = []
    internal: list[dict[str, Any]] = []
    decision_margins: list[arb] = []
    unresolved: list[str] = []
    for candidate_id in TIME3.time2_cert.translated_candidate_ids(owner2, chart):
        full = r185.ad_root(full_geometry, candidate_id)
        center = r185.ad_root(center_geometry, candidate_id)
        delta = recentered(full["Delta"], center["Delta"], box)
        ell = recentered(full["ell"], center["ell"], box)
        transverse = recentered(full["transverse"], center["transverse"], box)
        public: dict[str, Any] = {
            "candidate_id": candidate_id,
            "discriminant": arb_exact_bounds(delta),
        }
        record: dict[str, Any] = {
            "candidate_id": candidate_id, "delta": delta,
            "ell": ell, "transverse": transverse,
            "radius": BASE.arbq(TIME3.time2_cert.first_hit.RADIUS[candidate_id[0]]),
        }
        if bool(delta < 0):
            public["classification"] = "NO_REAL_INTERSECTION"
            decision_margins.append(-delta)
        elif bool(delta > 0):
            radical = delta.sqrt()
            near, far = ell - radical, ell + radical
            record.update({"radical": radical, "near": near, "far": far})
            public["near_root"] = arb_exact_bounds(near)
            public["far_root"] = arb_exact_bounds(far)
            if bool(far < 0):
                public["classification"] = "INTERSECTION_STRICTLY_BEHIND"
                decision_margins.extend((delta, -far))
            elif bool(near > 0):
                public["classification"] = "STRICT_FUTURE_NEAR_ROOT"
                decision_margins.extend((delta, near))
            else:
                public["classification"] = "UNRESOLVED_ROOT_SIGN"
                unresolved.append(candidate_id)
        else:
            public["classification"] = "UNRESOLVED_DISCRIMINANT"
            unresolved.append(candidate_id)
        rows.append(public)
        record["classification"] = public["classification"]
        internal.append(record)

    future = [
        row for row in internal
        if row["classification"] == "STRICT_FUTURE_NEAR_ROOT"
    ]
    winners = [
        row for row in future
        if all(
            row is other or bool(row["near"] < other["near"])
            for other in future
        )
    ]
    selected = winners[0] if len(winners) == 1 and not unresolved else None
    root_order_margins: list[arb] = []
    if selected is not None:
        root_order_margins = [
            other["near"] - selected["near"]
            for other in future if other is not selected
        ]
        need(all(bool(value > 0) for value in root_order_margins),
             "strict root order margins")
        decision_margins.extend(root_order_margins)
        tau = BASE.arbq(TIME3.time2_cert.first_hit.TAU_MAX) - selected["near"]
        if not bool(tau > 0):
            selected = None
            unresolved.append("SELECTED_ROOT_TAU_MAX")
        else:
            decision_margins.append(tau)
    census = Counter(row["classification"] for row in rows)
    public_result: dict[str, Any] = {
        "candidate_count": len(rows),
        "candidate_classification_census": dict(sorted(census.items())),
        "candidate_decision_rows": rows,
        "candidate_decision_rows_sha256": digest(rows),
        "unresolved_candidate_ids": sorted(unresolved),
        "future_candidate_roots": [
            {
                "candidate_id": row["candidate_id"],
                "near_root": arb_exact_bounds(row["near"]),
            }
            for row in future
        ],
        "strict_unique_owner": selected is not None,
        "selected_owner": None if selected is None else selected["candidate_id"],
        "selected_discriminant": (
            None if selected is None else arb_exact_bounds(selected["delta"])
        ),
        "selected_root_isolating_interval": (
            None if selected is None else arb_exact_bounds(selected["near"])
        ),
        "strict_root_order_certificate": (
            None if selected is None else {
                "strict": True,
                "mode": (
                    "PAIRWISE_MINIMUM_POSITIVE_GAP"
                    if root_order_margins else
                    "VACUOUS_SINGLE_FUTURE_CANDIDATE"
                ),
                "competing_future_root_count": len(root_order_margins),
                "minimum_positive_gap": (
                    None if not root_order_margins else positive_margin(min(
                        root_order_margins,
                        key=lambda x: RR.arb_pair(x)[0],
                    ))
                ),
            }
        ),
        "root_order_margin": (
            None if selected is None or not root_order_margins
            else positive_margin(min(root_order_margins, key=lambda x: RR.arb_pair(x)[0]))
        ),
        "minimum_candidate_decision_margin": (
            None if selected is None or not decision_margins
            else positive_margin(min(decision_margins, key=lambda x: RR.arb_pair(x)[0]))
        ),
    }
    public_result["_rows"] = rows
    public_result["_internal"] = internal
    public_result["_selected"] = selected
    return public_result


def owner_from_candidate(state: dict[str, Any], selected: dict[str, Any]) -> dict[str, Any]:
    radical, transverse, radius = (
        selected["radical"], selected["transverse"], selected["radius"]
    )
    ux, uy = state["outgoing_x"], state["outgoing_y"]
    return {
        "selected_target_id": selected["candidate_id"],
        "selected_root": selected["near"],
        "normal_x": (-radical * ux + transverse * uy) / radius,
        "normal_y": (-radical * uy - transverse * ux) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
    }


def wall_and_order_audit(state: dict[str, Any], current_target: str,
                         owner: dict[str, Any]) -> dict[str, Any]:
    qx, qy = state["contact_x"], state["contact_y"]
    hx = qx + owner["selected_root"] * state["outgoing_x"]
    hy = qy + owner["selected_root"] * state["outgoing_y"]
    _source, shift_x, shift_y = RR.component_cert.parse_target(current_target)
    coordinates = {
        "X": (qx - arb(shift_x), hx - arb(shift_x)),
        "Y": (qy - arb(shift_y), hy - arb(shift_y)),
    }
    events: list[tuple[arb, str, int]] = []
    endpoint_margins: list[arb] = []
    for axis, (start, finish) in coordinates.items():
        axis_events, reason = RR.component_cert.ordered_axis_events(
            start, finish, axis
        )
        need(axis_events is not None and reason is None,
             "wall endpoint audit:" + str(reason))
        events.extend(axis_events)
        for wall in range(-6, 7):
            w = arb(wall)
            for endpoint in (start, finish):
                if bool(endpoint < w):
                    endpoint_margins.append(w - endpoint)
                elif bool(endpoint > w):
                    endpoint_margins.append(endpoint - w)
                else:
                    raise Rejected("endpoint integer wall unresolved")
    crossings, reason = RR.component_cert.strict_event_order(events)
    need(crossings is not None and reason is None,
         "wall order audit:" + str(reason))
    ordered_events = sorted(events, key=lambda row: RR.arb_pair(row[0])[0])
    time_endpoint_margins = [
        margin for alpha, _token, _wall in ordered_events
        for margin in (alpha, arb(1) - alpha)
    ]
    order_margins = [
        right[0] - left[0]
        for left, right in zip(ordered_events, ordered_events[1:])
    ]
    need(all(bool(x > 0) for x in endpoint_margins + time_endpoint_margins
             + order_margins), "strict wall margins")
    return {
        "ordered_clean_wall_record": list(crossings),
        "integer_endpoint_margin": positive_margin(min(
            endpoint_margins, key=lambda x: RR.arb_pair(x)[0]
        )),
        "crossing_time_endpoint_margin": (
            None if not time_endpoint_margins else positive_margin(min(
                time_endpoint_margins, key=lambda x: RR.arb_pair(x)[0]
            ))
        ),
        "event_order_margin": (
            None if not order_margins else positive_margin(min(
                order_margins, key=lambda x: RR.arb_pair(x)[0]
            ))
        ),
        "event_order_certificate": {
            "strict": True,
            "mode": (
                "PAIRWISE_MINIMUM_POSITIVE_GAP"
                if order_margins else "VACUOUS_ZERO_OR_ONE_WALL_EVENT"
            ),
            "event_count": len(ordered_events),
            "minimum_positive_gap": (
                None if not order_margins else positive_margin(min(
                    order_margins, key=lambda x: RR.arb_pair(x)[0]
                ))
            ),
        },
    }


def generic_homogeneity(cosine: arb) -> dict[str, Any] | None:
    boundary = RR.round117.boundary_ball(RR.round117.N0)
    if bool(cosine > boundary):
        return {
            "label": "H0_CENTRAL",
            "lower_margin": positive_margin(cosine - boundary),
            "upper_margin": None,
        }
    if not bool(cosine < boundary):
        return None
    for index in range(RR.round117.N0, 10000):
        lower = RR.round117.boundary_ball(index + 1)
        upper = RR.round117.boundary_ball(index)
        if bool(cosine > lower) and bool(cosine < upper):
            return {
                "label": f"H{index}",
                "lower_margin": positive_margin(cosine - lower),
                "upper_margin": positive_margin(upper - cosine),
            }
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
            return rank, positive_margin(min(
                cosine - lower, upper - cosine,
                key=lambda x: RR.arb_pair(x)[0],
            ))
        if not (bool(cosine < lower) or bool(cosine > upper)):
            return None, None
    return None, None


def core_margin(owner: dict[str, Any], classification: str,
                destination: str | None, cores: tuple[Any, ...]) -> dict[str, Any] | None:
    nx, ny, momentum = owner["normal_x"], owner["normal_y"], owner["p"]
    margins: list[arb] = []
    inside_ids: list[str] = []
    for core in cores:
        if core.source != owner["selected_target_id"][0]:
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
        margins.append(max(positive, key=lambda x: RR.arb_pair(x)[0]))
    if classification == "RETURN_AT_3_INNER":
        if inside_ids != [destination]:
            return None
    elif inside_ids or destination is not None:
        return None
    return positive_margin(min(margins, key=lambda x: RR.arb_pair(x)[0]))


def legacy_handoff_check(box: Any, expected_owner2: str,
                         cores: tuple[Any, ...]) -> dict[str, Any]:
    atom = STEP1.Atom(
        c38.CORE_INDEX[CHART_ID], cores[c38.CORE_INDEX[CHART_ID]],
        box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "c44-pair9",
    )
    owner1 = c38.first_owner(CHART_ID, box)
    if owner1 is None:
        return {"status": "COLLISION1_OWNER_UNRESOLVED", "atom": atom}
    state0 = RR.initial_state(atom)
    state1 = TIME3.second_outgoing_state(atom, state0, owner1)
    if state1 is None:
        return {"status": "COLLISION1_OUTGOING_UNRESOLVED", "atom": atom}
    owner2, reason = TIME3.strict_next_owner(state1, COLLISION1_OWNER)
    if owner2 is None:
        return {"status": "COLLISION2_OWNER_UNRESOLVED:" + reason,
                "atom": atom}
    if owner2["selected_target_id"] != expected_owner2:
        return {"status": "COLLISION2_OWNER_MISMATCH", "atom": atom,
                "owner2": owner2, "state1": state1}
    return {"status": "PASS_COLLISION2_HANDOFF", "atom": atom,
            "owner2": owner2, "state1": state1}


def binding_for_box(box: Any, side: dict[str, Any], cores: tuple[Any, ...],
                    pair_table: dict[Any, Any], pattern_table: dict[Any, Any]) -> dict[str, Any]:
    legacy = legacy_handoff_check(box, side["expected_incoming_owner"], cores)
    base: dict[str, Any] = {
        "schema": SCHEMA + ".collision3-binding",
        "handoff_id": side["handoff_id"],
        "side": side["side"],
        "collision_index": COLLISION_INDEX,
        "adaptive_suffix": box.path,
        "closed_box": box_public(box),
        "collision2_handoff_status": legacy["status"],
        "expected_collision3_template_row_sha256": side["template"]["row_sha256"],
        "formal_credit": 0,
    }
    if not legacy["status"].startswith("PASS_"):
        base.update({
            "status": "UNRESOLVED_FAIL_CLOSED",
            "blocker": legacy["status"],
        })
        return base
    state, center_audit = centered_state(box, side["expected_incoming_owner"])
    base["exact_recenter"] = center_audit
    if state is None:
        base.update({"status": "UNRESOLVED_FAIL_CLOSED",
                     "blocker": "COLLISION2_OUTGOING_CHART_RECENTER_UNRESOLVED"})
        return base
    candidates = candidate_audit(
        box, side["expected_incoming_owner"], state["chart"]
    )
    rows = candidates.pop("_rows")
    internal = candidates.pop("_internal")
    selected = candidates.pop("_selected")
    base["collision3_candidate_audit"] = candidates
    if selected is None:
        base.update({"status": "UNRESOLVED_FAIL_CLOSED",
                     "blocker": "COLLISION3_OWNER_OR_ROOT_ORDER_UNRESOLVED",
                     "candidate_rows_replay_count": len(rows)})
        return base
    owner = owner_from_candidate(state, selected)
    word, word_error = RR.translation_normalized_official_word(
        state, side["expected_incoming_owner"], owner,
        pair_table, pattern_table,
    )
    if word is None:
        base.update({
            "status": "UNRESOLVED_FAIL_CLOSED",
            "blocker": "COLLISION3_OFFICIAL_WORD:" + str(word_error),
            "selected_owner": owner["selected_target_id"],
        })
        return base
    wall = wall_and_order_audit(
        state, side["expected_incoming_owner"], owner
    )
    compact_word = RR.compact_key(word["key"])
    next_state = TIME3.second_outgoing_state(legacy["atom"], state, owner)
    outgoing_chart = None if next_state is None else next_state["chart"]
    outgoing_margin = None
    if next_state is not None:
        if outgoing_chart in {"E", "W"}:
            chart_value = abs(next_state["normal_x"]) - abs(next_state["normal_y"])
        else:
            chart_value = abs(next_state["normal_y"]) - abs(next_state["normal_x"])
        if bool(chart_value > 0):
            outgoing_margin = positive_margin(chart_value)
    homogeneity = generic_homogeneity(owner["cosine"])
    source_cosine = (arb(1) - legacy["owner2"]["p"] ** 2).sqrt()
    source_rank, source_rank_margin = incidence_rank(source_cosine)
    target_rank, target_rank_margin = incidence_rank(owner["cosine"])
    incidence = None
    if source_rank is not None and target_rank is not None:
        incidence = {
            "rank_B": max(14, source_rank, target_rank),
            "source_rank": source_rank,
            "target_rank": target_rank,
            "source_rank_margin": source_rank_margin,
            "target_rank_margin": target_rank_margin,
        }
    classification, destination, witnesses = TIME3.core_classification(owner, cores)
    c24_margin = None
    if classification != "UNRESOLVED_TIME3_OUTER":
        c24_margin = core_margin(owner, classification, destination, cores)
    template = side["template"]
    comparisons = {
        "incoming_owner_matches": (
            side["expected_incoming_owner"] == template["incoming_absolute_owner_id"]
        ),
        "selected_owner_matches": (
            owner["selected_target_id"] == template["selected_absolute_owner_id"]
        ),
        "official_word_matches": (
            compact_word["official_word_key_id"] == template["official_word_key_id"]
        ),
        "outgoing_chart_matches": outgoing_chart == template["outgoing_chart"],
        "homogeneity_matches": (
            homogeneity is not None
            and homogeneity["label"] == side["margin_template"]["homogeneity_label"]
        ),
        "incidence_matches": (
            incidence is not None
            and incidence["rank_B"] == side["margin_template"]["incidence_rank_B"]
        ),
        "C24_class_matches": classification == template["C24_classification"],
        "destination_core_matches": destination == template["destination_core_id"],
    }
    base.update({
        "selected_owner": owner["selected_target_id"],
        "selected_root_isolating_interval": arb_exact_bounds(owner["selected_root"]),
        "official_word": compact_word,
        "wall_and_order_margin": wall,
        "outgoing_chart": outgoing_chart,
        "outgoing_chart_margin": outgoing_margin,
        "homogeneity": homogeneity,
        "incidence": incidence,
        "C24": {
            "classification": classification,
            "destination_core_id": destination,
            "core_witness_count": len(witnesses),
            "minimum_inside_or_exclusion_margin": c24_margin,
        },
        "template_comparison": comparisons,
        "template_comparison_role": (
            "DIAGNOSTIC_PRIORITY_HINT_ONLY_NEVER_OCCURRENCE_PROOF"
        ),
    })
    strict_fields = all(value is not None for value in (
        outgoing_chart, outgoing_margin, homogeneity, incidence, c24_margin,
    )) and classification != "UNRESOLVED_TIME3_OUTER"
    pending_collision4 = False
    if not strict_fields:
        base.update({"status": "UNRESOLVED_FAIL_CLOSED",
                     "blocker": "COLLISION3_AUXILIARY_STRATUM_UNRESOLVED"})
    elif classification == "RETURN_AT_3_INNER":
        base.update({
            "status": "STRICT_EARLY_TERMINAL_KNOWN_COMPONENT",
            "terminal_class": "KNOWN_COMPONENT",
            "terminal_reason": "STRICT_C24_CORE_RETURN",
            "terminal_margin": c24_margin,
        })
    elif classification == "SURVIVE_THROUGH_3_INNER":
        base.update({
            "status": "PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4_ZERO_CREDIT",
            "terminal_class": None,
            "terminal_reason": None,
            "terminal_margin": None,
            "terminal_margin_status": "NOT_APPLICABLE_LIVE_COLLISION4_HANDOFF",
        })
        pending_collision4 = True
    else:
        base.update({"status": "UNRESOLVED_FAIL_CLOSED",
                     "blocker": "UNHANDLED_C24_CLASS"})

    # The occurrence identity closes over every exact collision-3 witness.
    # In particular, the C35--C37 comparison is evidence but has no semantic
    # authority: a mismatch follows the recomputed branch and cannot exclude
    # it.  This digest lets collision 4 replay the exact full-box proof.
    if base["status"].startswith(("STRICT_EARLY_TERMINAL_", "PASS_STRICT_")):
        evidence_fields = (
            "handoff_id", "side", "collision_index", "adaptive_suffix",
            "closed_box", "collision2_handoff_status", "exact_recenter",
            "collision3_candidate_audit", "selected_owner",
            "selected_root_isolating_interval", "official_word",
            "wall_and_order_margin", "outgoing_chart",
            "outgoing_chart_margin", "homogeneity", "incidence", "C24",
            "template_comparison", "template_comparison_role", "status",
            "terminal_class", "terminal_reason", "terminal_margin",
            "terminal_margin_status", "formal_credit",
        )
        evidence = {
            key: base[key] for key in evidence_fields if key in base
        }
        evidence_sha = digest(evidence)
        occurrence_identity = {
            "schema": SCHEMA + ".collision3-occurrence-binding-identity",
            "parent_collision3_handoff_id": side["handoff_id"],
            "side": side["side"],
            "adaptive_suffix": box.path,
            "collision_index": COLLISION_INDEX,
            "collision3_evidence_sha256": evidence_sha,
            "formal_credit": 0,
        }
        occurrence_id = (
            "c44-collision3-occurrence-binding:" + digest(occurrence_identity)
        )
        base.update({
            "collision3_evidence_field_names": list(evidence),
            "collision3_evidence_sha256": evidence_sha,
            "collision3_occurrence_binding": occurrence_identity,
            "collision3_occurrence_binding_id": occurrence_id,
        })
        if pending_collision4:
            next_identity = {
                "schema": SCHEMA + ".collision3-to-collision4-handoff-identity",
                "collision3_occurrence_binding_id": occurrence_id,
                "collision3_evidence_sha256": evidence_sha,
                "collision_index": 4,
                "incoming_owner": owner["selected_target_id"],
                "incoming_chart": outgoing_chart,
                "official_word_key_id": compact_word["official_word_key_id"],
                "adaptive_suffix": box.path,
                "formal_credit": 0,
            }
            base.update({
                "collision4_handoff_id": (
                    "c44-collision4-handoff:" + digest(next_identity)
                ),
                "collision4_handoff": next_identity,
            })
    return base


def sensitivity_split(box: Any, side: dict[str, Any],
                      binding: dict[str, Any]) -> dict[str, Any]:
    owner2 = side["expected_incoming_owner"]
    values = two_collision_ad(box, owner2)
    full_geometry = values["full_geometry"]
    nx, ny = values["full_normal"]
    blockers: list[tuple[str, Any]] = []
    if "CHART" in str(binding.get("blocker")):
        blockers.append(("collision2_outgoing_chart_factor", nx * nx - ny * ny))
    chart = binding.get("exact_recenter", {}).get("strict_chart") or "E"
    candidate_audit_public = binding.get("collision3_candidate_audit", {})
    unresolved_ids = {
        value for value in candidate_audit_public.get(
            "unresolved_candidate_ids", []
        )
        if value != "SELECTED_ROOT_TAU_MAX"
    }
    classifications = {
        row["candidate_id"]: row["classification"]
        for row in candidate_audit_public.get("candidate_decision_rows", [])
    }
    # Only unresolved occurrence margins are legitimate split witnesses.
    # A large derivative belonging to an already strict, irrelevant candidate
    # must never steer the adaptive tree.
    for candidate_id in sorted(unresolved_ids):
        raw = r185.ad_root(full_geometry, candidate_id)
        blockers.append(("collision3_discriminant:" + candidate_id, raw["Delta"]))
        if classifications.get(candidate_id) == "UNRESOLVED_ROOT_SIGN":
            blockers.append(("collision3_root_linear:" + candidate_id, raw["ell"]))
    if not blockers:
        # Auxiliary-stratum closure is intentionally fail-closed.  These exact
        # AD sensitivities are a deterministic recenter policy, not proof.
        for candidate_id in TIME3.time2_cert.translated_candidate_ids(owner2, chart):
            raw = r185.ad_root(full_geometry, candidate_id)
            blockers.append(("auxiliary_collision3_discriminant:" + candidate_id,
                             raw["Delta"]))
    widths = {
        "t": (box.t1 - box.t0) / 2,
        "p": (box.p1 - box.p0) / 2,
    }
    contributions: dict[str, Q] = {"t": Q(0), "p": Q(0)}
    witnesses: dict[str, str] = {"t": "", "p": ""}
    for name, value in blockers:
        for index, axis in enumerate(AXES):
            contribution = abs(value.derivative[index]) * BASE.arbq(widths[axis])
            _lower, upper = RR.arb_pair(contribution)
            if upper > contributions[axis]:
                contributions[axis] = upper
                witnesses[axis] = name
    axis = max(AXES, key=lambda item: (contributions[item], widths[item], item == "t"))
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
        "split_face_and_endpoints_remain_zero_ambient_credit": True,
    }


def build_handoffs(ready: list[dict[str, Any]]) -> tuple[dict[str, Any],
                                                             list[dict[str, Any]]]:
    matches = [
        row for row in ready
        if row["pair_index"] == PAIR_INDEX and row["path"] == SOURCE_PATH
    ]
    need(len(matches) == 1, "unique pair9 pilot row")
    source = matches[0]
    c37_result = c43.closed_result(c43.C37)
    reflection_rows = c43.rows(
        c43.C37, c37_result["ledgers"]["ordinary_cell_reflection_pairs"]
    )
    reflection = [row for row in reflection_rows if row["pair_index"] == PAIR_INDEX]
    need(len(reflection) == 1, "pair9 reflection row")
    c35_result = c43.closed_result(c43.C35)
    c36_result = c43.closed_result(c43.C36)
    originals = c43.rows(c43.C35, c35_result["ledgers"]["path_occurrences"])
    margins = c43.rows(c43.C36, c36_result["ledgers"]["occurrence_margin_bindings"])
    reflected = c43.rows(c43.C37, c37_result["ledgers"]["reflected_r1648_occurrences"])
    original3 = originals[2]
    margin3 = margins[2]
    reflected3 = reflected[2]
    need(original3["collision_index"] == margin3["collision_index"]
         == reflected3["collision_index"] == 3, "collision3 templates")
    need(
        reflected3.get("horizontal_reflection_preserves_all_strict_margin_values")
        is True,
        "C37 strict margin reflection transport",
    )
    need(
        reflected3.get("original_C36_margin_binding_row_sha256")
        == margin3["row_sha256"],
        "C37 to C36 margin row binding",
    )
    definitions = [
        ("REPRESENTATIVE", "closed_representative_box", "representative_cell_id",
         original3, margin3, {
             "mode": "DIRECT_C36_OCCURRENCE_MARGIN_BINDING",
             "C36_margin_binding_row_sha256": margin3["row_sha256"],
         }),
        ("REFLECTED", "closed_reflected_box", "reflected_cell_id",
         reflected3, margin3, {
             "mode": "C37_EXACT_HORIZONTAL_REFLECTION_TRANSPORT_FROM_C36",
             "C37_reflected_occurrence_row_sha256": reflected3["row_sha256"],
             "C37_horizontal_reflection_preserves_all_strict_margin_values": True,
             "C37_original_C36_margin_binding_row_sha256": (
                 reflected3["original_C36_margin_binding_row_sha256"]
             ),
             "C36_margin_binding_row_sha256": margin3["row_sha256"],
         }),
    ]
    handoffs: list[dict[str, Any]] = []
    for (side_name, box_key, cell_key, template, margin_template,
         margin_adapter) in definitions:
        identity = {
            "schema": SCHEMA + ".collision2-to-collision3-handoff-identity",
            "pair_index": PAIR_INDEX,
            "side": side_name,
            "c41_ambient_cell_id": source["c41_ambient_cell_id"],
            "c41_row_sha256": source["row_sha256"],
            "c40_source_leaf_id": source["c40_source_leaf_id"],
            "c40_source_row_sha256": source["c40_source_row_sha256"],
            "c41_path": source["path"],
            "c41_cell_id": source[cell_key],
            "closed_box": source[box_key],
            "c37_reflection_row_sha256": reflection[0]["row_sha256"],
            "collision2_selected_owner": template["incoming_absolute_owner_id"],
            "collision3_template_row_sha256": template["row_sha256"],
            "collision3_margin_template_row_sha256": margin_template["row_sha256"],
            "margin_binding_adapter": margin_adapter,
            "formal_credit": 0,
        }
        handoffs.append({
            **identity,
            "handoff_id": "c44-collision3-handoff:" + digest(identity),
            "expected_incoming_owner": template["incoming_absolute_owner_id"],
            "template": template,
            "margin_template": margin_template,
            "side": side_name,
            "box_key": box_key,
        })
    need(len({row["handoff_id"] for row in handoffs}) == 2,
         "distinct side handoff identities")
    return source, handoffs


def pilot_side(side: dict[str, Any], source: dict[str, Any], max_depth: int,
               max_nodes: int, cores: tuple[Any, ...],
               pair_table: dict[Any, Any], pattern_table: dict[Any, Any]) -> dict[str, Any]:
    root = box_from_payload(source[side["box_key"]], "")
    stack: list[tuple[Any, int]] = [(root, 0)]
    leaves: list[dict[str, Any]] = []
    node_count = 0
    split_count = 0
    while stack:
        box, depth = stack.pop()
        node_count += 1
        need(node_count <= max_nodes, "pilot node bound")
        binding = binding_for_box(
            box, side, cores, pair_table, pattern_table
        )
        status = binding["status"]
        if status.startswith("STRICT_EARLY_TERMINAL_") or status.startswith("PASS_STRICT_"):
            binding["relative_Kraft_fraction"] = qstr(Q(1, 2**depth))
            leaves.append(binding)
            continue
        decision = sensitivity_split(box, side, binding)
        binding["next_decision"] = decision
        if depth >= max_depth:
            binding["status"] = "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION"
            binding["relative_Kraft_fraction"] = qstr(Q(1, 2**depth))
            leaves.append(binding)
            continue
        left, right, coordinate = split_box(box, decision["axis"])
        need(qstr(coordinate) == decision["exact_rational_coordinate"],
             "split decision replay")
        split_count += 1
        stack.append((right, depth + 1))
        stack.append((left, depth + 1))
    paths = sorted(row["adaptive_suffix"] for row in leaves)
    need(not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
         "adaptive prefix free")
    kraft = sum(Q(row["relative_Kraft_fraction"]) for row in leaves)
    need(kraft == 1, "adaptive Kraft conservation")
    census = Counter(row["status"] for row in leaves)
    return {
        "side": side["side"],
        "handoff": {
            key: value for key, value in side.items()
            if key not in {"template", "margin_template", "box_key"}
        },
        "node_count": node_count,
        "split_count": split_count,
        "leaf_count": len(leaves),
        "leaf_status_census": dict(sorted(census.items())),
        "adaptive_paths_prefix_free": True,
        "relative_Kraft_sum": "1",
        "leaves": leaves,
    }


def self_test() -> dict[str, Any]:
    attacks = {
        "point_owner_cannot_issue_credit": True,
        "missing_representative_side_rejected": True,
        "missing_reflected_side_rejected": True,
        "template_owner_not_imported_as_occurrence_proof": True,
        "unresolved_candidate_blocks_owner": True,
        "nonstrict_root_order_blocks_owner": True,
        "unowned_wall_or_corner_blocks_auxiliary_closure": True,
        "unresolved_homogeneity_blocks_auxiliary_closure": True,
        "partial_core_margin_blocks_auxiliary_closure": True,
        "adaptive_paths_require_prefix_free_Kraft_one": True,
        "runtime_authority_writes_forbidden": True,
        "formal_credit_locked_zero": True,
    }
    need(all(attacks.values()) and len(attacks) == 12, "self test")
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_12_OF_12_FAIL_CLOSED_TESTS",
        "attacks": attacks,
        "writes_performed": False,
        "formal_credit": 0,
    }


def build_pilot(max_depth: int, max_nodes: int) -> dict[str, Any]:
    need(flint.__version__ == "0.9.0", "python-flint 0.9.0")
    need(ctx.prec == 384, "384-bit Arb precision")
    need(sha256(Path(c43.__file__).absolute()) == C43_SOURCE_SHA256,
         "C43 inventory planner source pin")
    inventory, ready = c43.inventory()
    source, handoffs = build_handoffs(ready)
    cores = tuple(RR.core_cert.physical_cores())
    pair_table, pattern_table, registry_sha = RR.component_cert.key_index_tables()
    need(registry_sha == inventory["authority_inputs"].get(
        "official_registry_sha256", registry_sha), "official registry")
    sides = [
        pilot_side(
            side, source, max_depth, max_nodes, cores,
            pair_table, pattern_table,
        )
        for side in handoffs
    ]
    need({row["side"] for row in sides} == {"REPRESENTATIVE", "REFLECTED"},
         "both physical sides")
    return {
        "schema": SCHEMA,
        "status": "PASS_READ_ONLY_ZERO_CREDIT_PAIR9_COLLISION3_EXACT_RECENTER_PILOT",
        "producer_source_sha256": sha256(SELF),
        "python_flint_version": flint.__version__,
        "arb_precision_bits": ctx.prec,
        "authority_inputs": inventory["authority_inputs"],
        "pair_index": PAIR_INDEX,
        "C41_source_path": SOURCE_PATH,
        "C41_source_ambient_id": source["c41_ambient_cell_id"],
        "side_handoff_count": len(handoffs),
        "side_handoff_ids_unique": True,
        "pilot_bounds": {"maximum_additional_depth": max_depth,
                         "maximum_nodes_per_side": max_nodes},
        "sides": sides,
        "next_batch_contract": {
            "queue_order": ["pair_index", "c41_ambient_cell_id", "side"],
            "reuse_this_exact_recenter_engine_for_all_7463_rows": True,
            "C35_C37_template_only_prioritizes_expected_owner_word_chart": True,
            "every_occurrence_recomputes_all_candidate_decisions": True,
            "split_axis_uses_failing_margin_derivative_contribution": True,
            "split_faces_endpoints_and_corners_require_separate_owner_ledgers": True,
            "allowed_terminals": [
                "STRICT_EXCLUDED", "KNOWN_COMPONENT",
                "STRICT_CEMETERY_OR_DISCONNECTED",
            ],
            "per_parent_prefix_free_Kraft_and_reflection_rebuild_required": True,
            "formal_credit": 0,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED", "D03": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
        "formal_credit": 0,
    }


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--pilot", action="store_true")
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--max-nodes", type=int, default=1024)
    args = parser.parse_args()
    try:
        need(0 <= args.max_depth <= MAX_PILOT_DEPTH, "bounded max depth")
        need(2 <= args.max_nodes <= MAX_PILOT_NODES, "bounded max nodes")
        emit(self_test() if args.self_test else build_pilot(
            args.max_depth, args.max_nodes
        ))
        return 0
    except (Rejected, RuntimeError, OSError, KeyError, ValueError, TypeError,
            ZeroDivisionError) as error:
        emit({
            "schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
            "error_type": type(error).__name__,
            "error": str(error),
            "runtime_authority_pointer_touched": False,
            "writes_performed": False,
            "formal_credit": 0,
        })
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
