#!/usr/bin/env python3
"""Build two-sided transverse root collars on all frozen rank-three interior links.

The 52 Round109 registered-arc tubes and 56 Round100 gap tubes are tangent
graph certificates.  This append-only producer replays their actual rational
strip boxes and, on every strip, proves two separate implicit root sheets

    HIT:    Delta_3(t,p) - R_3^2 c_3^2 = 0,
    BYPASS: Delta_3(t,p) + R_3^2 b_3^2 = 0,

for 0 <= c_3,b_3 <= 2^-64.  It then replays the complete first/second owner
searches, the complete immutable third-candidate table, and all three official
Gate-5 word keys.  The D=0 trace is retained only as the common singular edge;
no homogeneous child or Gate5 field is installed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component_cert
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round100_rank3_immutable_interior_gap_closure as round100_source
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round116.rank3-interior-two-sided-transverse-collar.v1"
PRECISION_BITS = 512
ROOT_COORDINATE_DEPTH = 64
ROOT_COORDINATE_WIDTH = Q(1, 2**ROOT_COORDINATE_DEPTH)
REGISTRY_ROWS_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"

FILES = {
    "round100": "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json",
    "round102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "round109": "cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json",
    "round110": "cm2-round110-rank3-gap-tube-side-decomposition-2026-07-22.json",
}
PINS = {
    FILES["round100"]: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    FILES["round102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["round109"]: "fa5231f91f71da8014f9ca606702e3a59499adf78ce86ce09954bb424dae540e",
    FILES["round110"]: "2b49f900e05a29fc65897b8ebf350882a310fa95ebcd0031f94214f87ded38a2",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round80_time3_tangency_curve_generator.py": "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
    "cm2_round87_rank3_port_event_continuation_cert.py": "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834",
    "cm2_round89_rank3_projective_gap_closure_cert.py": "6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf",
    "cm2_round90_rank3_tracked_residual_gap_closure_cert.py": "4f07377f59bb229592f683952868978372e5a46efc9ea9642c04cd340833e16f",
    "cm2_round99_rank3_registered_port_candidate_audit.py": "bbacd4407aa026850d9a410b61e841bd6e799e67ba16549e4a478a9fcfb7a26f",
    "cm2_round100_rank3_immutable_interior_gap_closure.py": "be5c7d9413f03810210eea8b8d2eb37a9256886f0a339cdcd4ddcf1d32c1e224",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
}

WORK_CORES: tuple[Any, ...] = ()
PAIR_INDEX: dict[tuple[str, str], int] = {}
PATTERN_INDEX: dict[tuple[str, ...], int] = {}


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


def load_closed(name: str, schema: str) -> dict[str, Any]:
    document = json.loads(
        (HERE / name).read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError(f"non-closed dependency: {name}")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError(f"dependency envelope mismatch: {name}")
    return document["result"]


def init_worker(precision_bits: int) -> None:
    global WORK_CORES, PAIR_INDEX, PATTERN_INDEX
    ctx.prec = precision_bits
    WORK_CORES = tuple(core_cert.physical_cores())
    round87.WORK_CORES = WORK_CORES
    round87.physical_type = round100_source.immutable_physical_type
    PAIR_INDEX, PATTERN_INDEX, registry_sha = component_cert.key_index_tables()
    if registry_sha != REGISTRY_ROWS_SHA256:
        raise RuntimeError("official word registry replay mismatch")


def standard_boxes(
    left: dict[str, Any], right: dict[str, Any], source: Any,
    strip_count: int, collar_depth: int,
) -> list[tuple[Q, Q, Q, Q]]:
    a, b = round89.root_rect(left), round89.root_rect(right)
    t_end = ((a[0] + a[1]) / 2, (b[0] + b[1]) / 2)
    p_end = ((a[2] + a[3]) / 2, (b[2] + b[3]) / 2)
    if abs(t_end[1] - t_end[0]) >= abs(p_end[1] - p_end[0]):
        raise RuntimeError("frozen tube unexpectedly stopped being t(p)")
    collar = (source.t1 - source.t0) / Q(2**collar_depth)
    boxes: list[tuple[Q, Q, Q, Q]] = []
    for index in range(strip_count):
        u0, u1 = Q(index, strip_count), Q(index + 1, strip_count)
        p0 = p_end[0] + u0 * (p_end[1] - p_end[0])
        p1 = p_end[0] + u1 * (p_end[1] - p_end[0])
        t0 = t_end[0] + u0 * (t_end[1] - t_end[0])
        t1 = t_end[0] + u1 * (t_end[1] - t_end[0])
        p_lower, p_upper = sorted((p0, p1))
        t_lower = max(source.t0, min(t0, t1) - collar)
        t_upper = min(source.t1, max(t0, t1) + collar)
        boxes.append((t_lower, t_upper, p_lower, p_upper))
    return boxes


def tracked_boxes(
    left: dict[str, Any], right: dict[str, Any], source: Any,
    branch: tuple[int, str, str, int], strip_count: int,
    collar_depth: int, bisection_depth: int,
) -> list[tuple[Q, Q, Q, Q]]:
    a, b = round89.root_rect(left), round89.root_rect(right)
    t_end = ((a[0] + a[1]) / 2, (b[0] + b[1]) / 2)
    p_end = ((a[2] + a[3]) / 2, (b[2] + b[3]) / 2)
    if abs(t_end[1] - t_end[0]) >= abs(p_end[1] - p_end[0]):
        raise RuntimeError("tracked tube unexpectedly stopped being t(p)")
    dep_lower, dep_upper = source.t0, source.t1
    dep_width = dep_upper - dep_lower

    def value(p: Q, t: Q) -> arb:
        return third_tangency_jet(
            source, branch[1], branch[2], t, t, p, p
        ).value

    nodes: list[tuple[Q, Q, Q]] = []
    for index in range(strip_count + 1):
        u = Q(index, strip_count)
        p = p_end[0] + u * (p_end[1] - p_end[0])
        prediction = t_end[0] + u * (t_end[1] - t_end[0])
        bracket: tuple[Q, Q, Q] | None = None
        for depth in range(4, 49, 4):
            radius = dep_width / Q(2**depth)
            lower = max(dep_lower, prediction - radius)
            upper = min(dep_upper, prediction + radius)
            lower_sign, upper_sign = strict_sign(value(p, lower)), strict_sign(value(p, upper))
            if lower_sign * upper_sign != -1:
                continue
            for _ in range(bisection_depth):
                middle = (lower + upper) / 2
                middle_sign = strict_sign(value(p, middle))
                if middle_sign == 0:
                    break
                if middle_sign == lower_sign:
                    lower, lower_sign = middle, middle_sign
                else:
                    upper, upper_sign = middle, middle_sign
            else:
                bracket = (p, lower, upper)
                break
        if bracket is None:
            raise RuntimeError(f"tracked root node unresolved: {index}")
        nodes.append(bracket)
    collar = dep_width / Q(2**collar_depth)
    boxes: list[tuple[Q, Q, Q, Q]] = []
    for index in range(strip_count):
        p0, t00, t01 = nodes[index]
        p1, t10, t11 = nodes[index + 1]
        lower = max(dep_lower, min(t00, t10) - collar)
        upper = min(dep_upper, max(t01, t11) + collar)
        boxes.append((lower, upper, min(p0, p1), max(p0, p1)))
    return boxes


def dyadic_margin_depth(value: arb) -> int:
    if strict_sign(value) != 1:
        raise RuntimeError("nonpositive strict margin")
    for depth in range(-16, 1025):
        bound = Q(2**(-depth), 1) if depth < 0 else Q(1, 2**depth)
        if bool(value > aq(bound)):
            return depth
    raise RuntimeError("positive margin below 2^-1024")


class MarginLedger:
    def __init__(self) -> None:
        self.depths: dict[str, int] = {}
        self.counts: Counter[str] = Counter()

    def observe(self, name: str, value: arb) -> None:
        depth = dyadic_margin_depth(value)
        self.depths[name] = max(self.depths.get(name, -16), depth)
        self.counts[name] += 1

    def public(self) -> dict[str, Any]:
        return {
            name: {
                "strict_lower_bound": (
                    str(Q(2**(-depth), 1)) if depth < 0 else str(Q(1, 2**depth))
                ),
                "dyadic_depth": depth,
                "observation_count": self.counts[name],
            }
            for name, depth in sorted(self.depths.items())
        }


def candidate_order(
    state2: dict[str, Any], current_target: str, tangent_target: str,
    tangent_flight: arb, margins: MarginLedger,
) -> tuple[str, arb, Counter[str], int]:
    candidates = tuple(time3.time2_cert.translated_candidate_ids(current_target, state2["chart"]))
    if tangent_target not in candidates:
        raise RuntimeError("designated target absent from immutable third table")
    future: list[tuple[str, arb]] = []
    classifications: Counter[str] = Counter()
    for candidate_id in candidates:
        if candidate_id == tangent_target:
            continue
        center_x, center_y = time3.time2_cert.target_center(candidate_id, state2["s"])
        dx = center_x - state2["contact_x"]
        dy = center_y - state2["contact_y"]
        ell = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy
        transverse = -state2["outgoing_y"] * dx + state2["outgoing_x"] * dy
        radius = aq(time3.time2_cert.first_hit.RADIUS[candidate_id[0]])
        discriminant = radius * radius - transverse * transverse
        if strict_sign(discriminant) == -1:
            classifications["no_real_intersection"] += 1
            margins.observe("competitor_miss_discriminant", -discriminant)
            continue
        if strict_sign(discriminant) != 1:
            raise RuntimeError("unresolved competitor discriminant")
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if strict_sign(far) == -1:
            classifications["intersection_strictly_behind"] += 1
            margins.observe("competitor_behind_far_root", -far)
            continue
        if strict_sign(near) != 1:
            raise RuntimeError("unresolved competitor root sign")
        classifications["strict_future_near_root"] += 1
        margins.observe("competitor_future_root_positive", near)
        margins.observe("competitor_after_tangent_flight", near - tangent_flight)
        future.append((candidate_id, near))
    winners = [
        (candidate_id, near)
        for candidate_id, near in future
        if all(candidate_id == other_id or bool(near < other_near)
               for other_id, other_near in future)
    ]
    if len(winners) != 1:
        raise RuntimeError("nonunique BYPASS winner")
    winner, winner_root = winners[0]
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    margins.observe("bypass_winner_root_positive", winner_root)
    margins.observe("bypass_winner_below_flight_cap", tau_max - winner_root)
    for candidate_id, near in future:
        if candidate_id != winner:
            margins.observe("bypass_winner_pairwise_gap", near - winner_root)
    return winner, winner_root, classifications, len(candidates)


def compact_key(key: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_word_key_id": key["word_key_id"],
        "ordinal_zero_based": key["ordinal_zero_based"],
        "registry_row_sha256": key["row_sha256"],
        "registry_row": key["row"],
    }


def analyze_link(task: dict[str, Any]) -> dict[str, Any]:
    source = WORK_CORES[task["source_core_index"]]
    left, right = task["left_event"], task["right_event"]
    branch = round89.key(left)
    expected_branch = (
        task["source_core_index"], task["second_selected_target_id"],
        task["third_candidate_id"], task["signed_transverse_tangency_factor_sign"],
    )
    if branch != expected_branch or round89.key(right) != branch:
        raise RuntimeError("link branch identity mismatch")
    if task["tube_method"] == "TRACKED_NODE_ROOT_CHAIN":
        boxes = tracked_boxes(
            left, right, source, branch, task["strip_count"],
            task["dependent_collar_depth"], task["node_root_bisection_depth"],
        )
    else:
        boxes = standard_boxes(
            left, right, source, task["strip_count"], task["dependent_collar_depth"]
        )
    box_digest = digest([list(map(str, box)) for box in boxes])
    if box_digest != task["expected_tube_boxes_sha256"]:
        raise RuntimeError("materialized tangent tube digest mismatch")

    first_key = component_cert.word_key(
        source.chart_id, source.target_id, tuple(source.crossings),
        PAIR_INDEX, PATTERN_INDEX,
    )
    c_interval = time3.time2_cert.first_hit.arb_interval(Q(0), ROOT_COORDINATE_WIDTH)
    c_upper = aq(ROOT_COORDINATE_WIDTH)
    target_radius = aq(time3.time2_cert.first_hit.RADIUS[branch[2][0]])
    radius_square = target_radius * target_radius
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    margins = MarginLedger()
    discrete_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    classification_histogram: Counter[str] = Counter()
    triple_histogram: Counter[str] = Counter()
    bypass_winners: Counter[str] = Counter()
    signatures: list[tuple[int, dict[str, Any]]] = []
    previous_box: tuple[Q, Q, Q, Q] | None = None

    for index, box in enumerate(boxes):
        try:
            if previous_box is not None:
                if previous_box[3] != box[2]:
                    raise RuntimeError("noncontiguous p-strip seam")
                overlap = min(previous_box[1], box[1]) - max(previous_box[0], box[0])
                if overlap <= 0:
                    raise RuntimeError("nonoverlapping adjacent t enclosures")
                margins.observe("adjacent_t_enclosure_overlap", aq(overlap))
            previous_box = box
            t_lower, t_upper, p_lower, p_upper = box
            jet = third_tangency_jet(source, branch[1], branch[2], *box)
            derivative_sign = strict_sign(jet.gradient[0])
            if derivative_sign == 0:
                raise RuntimeError("transverse IFT derivative indeterminate")
            margins.observe(
                "absolute_transverse_D_t_derivative",
                jet.gradient[0] if derivative_sign > 0 else -jet.gradient[0],
            )
            face_values = [
                third_tangency_jet(
                    source, branch[1], branch[2], face, face, p_lower, p_upper
                ).value
                for face in (t_lower, t_upper)
            ]
            negative = [value for value in face_values if strict_sign(value) == -1]
            positive = [value for value in face_values if strict_sign(value) == 1]
            if len(negative) != 1 or len(positive) != 1:
                raise RuntimeError("root strip lacks opposite strict D faces")
            hit_face_margin = positive[0] - radius_square * c_upper * c_upper
            bypass_face_margin = -(negative[0] + radius_square * c_upper * c_upper)
            margins.observe("HIT_positive_face_after_shift", hit_face_margin)
            margins.observe("BYPASS_negative_face_after_shift", bypass_face_margin)

            atom = step1.Atom(
                branch[0], source, *box, Q(0), Q(0),
                f"round116:{task['link_index']}:{index}",
            )
            classification, _status2, destination, state1, owner2 = (
                time3.homogeneity_cert.classify_with_geometry(atom, WORK_CORES)
            )
            if (
                classification != "SURVIVE_THROUGH_2_INNER"
                or destination is not None or state1 is None or owner2 is None
                or owner2["selected_target_id"] != branch[1]
            ):
                raise RuntimeError("first/second owner chain changed")
            state2 = time3.second_outgoing_state(atom, state1, owner2)
            if state2 is None:
                raise RuntimeError("second outgoing state/chart unresolved")
            target_x, target_y = time3.time2_cert.target_center(branch[2], state2["s"])
            dx = target_x - state2["contact_x"]
            dy = target_y - state2["contact_y"]
            tangent_flight = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy
            tangent_transverse = -state2["outgoing_y"] * dx + state2["outgoing_x"] * dy
            if strict_sign(tangent_transverse) != branch[3]:
                raise RuntimeError("designated transverse orientation changed")
            margins.observe("designated_tangent_flight_positive", tangent_flight)
            margins.observe("designated_tangent_flight_below_cap", tau_max - tangent_flight)
            hit_root = tangent_flight - target_radius * c_interval
            margins.observe("HIT_actual_root_positive", hit_root)

            winner, winner_root, candidate_hist, third_count = candidate_order(
                state2, branch[1], branch[2], tangent_flight, margins
            )
            classification_histogram.update(candidate_hist)
            bypass_winners[winner] += 1
            first_count = len(time3.time2_cert.first_hit.candidate_ids(source.chart_id))
            second_count = len(tuple(time3.time2_cert.translated_candidate_ids(
                source.target_id, state1["chart"]
            )))
            candidate_triple = (first_count, second_count, third_count)
            triple_histogram["/".join(map(str, candidate_triple))] += 1

            second_word, second_error = component_cert.second_word_for_atom(
                atom, branch[1], PAIR_INDEX, PATTERN_INDEX
            )
            if second_word is None or second_error is not None:
                raise RuntimeError(f"second official word unresolved:{second_error}")
            hit_word, hit_error = time3.third_word(
                state2, branch[1],
                {"selected_target_id": branch[2], "selected_root": hit_root},
                PAIR_INDEX, PATTERN_INDEX,
            )
            if hit_word is None:
                raise RuntimeError(f"HIT third official word unresolved:{hit_error}")
            bypass_word, bypass_error = time3.third_word(
                state2, branch[1],
                {"selected_target_id": winner, "selected_root": winner_root},
                PAIR_INDEX, PATTERN_INDEX,
            )
            if bypass_word is None:
                raise RuntimeError(f"BYPASS third official word unresolved:{bypass_error}")

            key_ids_hit = [
                first_key["word_key_id"], second_word["key"]["word_key_id"],
                hit_word["key"]["word_key_id"],
            ]
            key_ids_bypass = [
                first_key["word_key_id"], second_word["key"]["word_key_id"],
                bypass_word["key"]["word_key_id"],
            ]
            signature = {
                "candidate_counts_by_leg": list(candidate_triple),
                "outgoing_chart_sequence": [source.chart_id, state1["chart"], state2["chart"]],
                "common_first_two_owner_ids": [source.target_id, branch[1]],
                "HIT_third_owner_id": branch[2],
                "BYPASS_third_owner_id": winner,
                "HIT_official_word_key_ids": key_ids_hit,
                "BYPASS_official_word_key_ids": key_ids_bypass,
                "HIT_official_path_id": "gate5-rank3-interior-HIT-path:" + digest(key_ids_hit),
                "BYPASS_official_path_id": "gate5-rank3-interior-BYPASS-path:" + digest(key_ids_bypass),
                "first_official_key": compact_key(first_key),
                "second_official_key": compact_key(second_word["key"]),
                "HIT_third_official_key": compact_key(hit_word["key"]),
                "BYPASS_third_official_key": compact_key(bypass_word["key"]),
            }
            signatures.append((index, signature))
            discrete_rows.append({
                "strip_index": index,
                "D_t_derivative_sign": derivative_sign,
                "D_face_signs_in_t_order": [strict_sign(value) for value in face_values],
                "candidate_counts_by_leg": list(candidate_triple),
                "competitor_classification_histogram": dict(sorted(candidate_hist.items())),
                "outgoing_chart_sequence": signature["outgoing_chart_sequence"],
                "BYPASS_third_owner_id": winner,
                "HIT_official_word_key_ids": key_ids_hit,
                "BYPASS_official_word_key_ids": key_ids_bypass,
            })
        except (RuntimeError, ValueError, ZeroDivisionError) as exc:
            residual_rows.append({"strip_index": index, "reason": str(exc)})

    runs: list[dict[str, Any]] = []
    for index, signature in signatures:
        signature_digest = digest(signature)
        if (
            runs and runs[-1]["strip_end_exclusive"] == index
            and runs[-1]["signature_sha256"] == signature_digest
        ):
            runs[-1]["strip_end_exclusive"] = index + 1
        else:
            runs.append({
                "strip_start_inclusive": index,
                "strip_end_exclusive": index + 1,
                "signature_sha256": signature_digest,
                **signature,
            })
    full = len(discrete_rows) == len(boxes) and not residual_rows
    identity = {
        "face_id": task["face_id"], "link_rank": task["link_rank"],
        "left_registered_port_id": task["left_registered_port_id"],
        "right_registered_port_id": task["right_registered_port_id"],
    }
    return {
        "interior_transverse_collar_id": "physical-s0-rank3-interior-transverse-collar:" + digest(identity),
        **identity,
        "link_type": task["link_type"],
        "source_core_index": branch[0],
        "second_selected_target_id": branch[1],
        "designated_third_candidate_id": branch[2],
        "signed_transverse_tangency_factor_sign": branch[3],
        "tube_method": task["tube_method"],
        "implicit_graph_axis": "t_as_function_of_p",
        "source_parameter_axis": "p",
        "root_coordinate_width": str(ROOT_COORDINATE_WIDTH),
        "root_coordinate_depth": ROOT_COORDINATE_DEPTH,
        "tangent_strip_count": len(boxes),
        "tangent_tube_boxes_sha256": box_digest,
        "certified_HIT_root_sheet_strip_count": len(discrete_rows),
        "certified_BYPASS_root_sheet_strip_count": len(discrete_rows),
        "certified_two_sided_root_sheet_strip_count": 2 * len(discrete_rows),
        "certified_adjacent_strip_seam_count": max(0, len(discrete_rows) - 1) if full else 0,
        "relative_interior_full_two_sided_collar_certified": full,
        "first_second_owner_constancy_certified": full,
        "complete_candidate_owner_constancy_certified": full,
        "official_three_key_path_constancy_certified": full,
        "HIT_designated_actual_owner_on_open_sheet_certified": full,
        "BYPASS_designated_miss_and_actual_winner_on_open_sheet_certified": full,
        "HIT_root_equation": "Delta3(t,p)-R3^2*c3^2=0",
        "BYPASS_root_equation": "Delta3(t,p)+R3^2*b3^2=0",
        "regular_root_coordinate_domain": (
            "HIT 0<c3<=2^-64 and BYPASS 0<b3<=2^-64; the closed interval is used only for one-sided estimates"
        ),
        "common_singular_edge": "c3=b3=0 equals the D=0 tangent trace; excluded from both regular sheets and not an operator child",
        "candidate_count_triple_histogram": dict(sorted(triple_histogram.items())),
        "third_competitor_classification_histogram": dict(sorted(classification_histogram.items())),
        "BYPASS_winner_histogram": dict(sorted(bypass_winners.items())),
        "official_path_run_count": len(runs),
        "official_path_runs": runs,
        "official_path_runs_sha256": digest(runs),
        "strict_margin_lower_bounds": margins.public(),
        "discrete_strip_evidence_sha256": digest(discrete_rows),
        "residual_strip_count": len(residual_rows),
        "residual_rows": residual_rows,
        "residual_rows_sha256": digest(residual_rows),
    }


def build(precision_bits: int = PRECISION_BITS, workers: int = 8) -> dict[str, Any]:
    if precision_bits < 384:
        raise RuntimeError("insufficient producer precision")
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"byte pin mismatch: {name}")
    round100 = load_closed(FILES["round100"], "cm2.round100.rank3-immutable-interior-gap-closure.v1")
    round102 = load_closed(FILES["round102"], "cm2.round102.rank3-corrected-face-quotient.v1")
    round109 = load_closed(FILES["round109"], "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1")
    round110 = load_closed(FILES["round110"], "cm2.round110.rank3-gap-tube-side-decomposition.v1")
    if (
        round109["certified_registered_arc_whole_tube_count"] != 52
        or len(round100["gap_rows"]) != 56
        or round110["complete_two_sided_gap_pair_count"] != 56
    ):
        raise RuntimeError("upstream interior-link census changed")

    event_rows, _pair_rows = round89.load()
    event_by_id = {row["registered_port_id"]: row for row in event_rows}
    registered_by_endpoints = {
        frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row
        for row in round109["registered_arc_rows"]
    }
    gap_by_endpoints = {
        frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row
        for row in round100["gap_rows"]
    }
    links = sorted(round102["interior_link_rows"], key=lambda row: (row["face_id"], row["link_rank"]))
    if len(links) != 108:
        raise RuntimeError("corrected interior-link census changed")
    tasks: list[dict[str, Any]] = []
    for index, link in enumerate(links):
        endpoints = frozenset((link["left_registered_port_id"], link["right_registered_port_id"]))
        if link["link_type"] == "REGISTERED_PHYSICAL_ARC":
            tube = registered_by_endpoints.get(endpoints)
            if tube is None:
                raise RuntimeError("registered link missing Round109 tube")
            method = "WHOLE_TUBE_IFT_CHAIN"
            expected_digest = tube["certified_tube_boxes_sha256"]
        elif link["link_type"] == "IMMUTABLE_CERTIFIED_INTERIOR_GAP":
            tube = gap_by_endpoints.get(endpoints)
            if tube is None:
                raise RuntimeError("gap link missing Round100 tube")
            method = tube["immutable_candidate_reaudit_method"]
            expected_digest = (
                tube["tracked_boxes_sha256"] if method == "TRACKED_NODE_ROOT_CHAIN"
                else tube["certified_tube_boxes_sha256"]
            )
        else:
            raise RuntimeError("unknown interior link type")
        left_id, right_id = link["left_registered_port_id"], link["right_registered_port_id"]
        task = {
            "link_index": index,
            **link,
            "left_event": event_by_id[left_id],
            "right_event": event_by_id[right_id],
            "source_core_index": tube["source_core_index"],
            "second_selected_target_id": tube["second_selected_target_id"],
            "third_candidate_id": tube["third_candidate_id"],
            "signed_transverse_tangency_factor_sign": tube["signed_transverse_tangency_factor_sign"],
            "tube_method": method,
            "strip_count": tube["strip_count"],
            "dependent_collar_depth": tube["dependent_collar_depth"],
            "node_root_bisection_depth": tube.get("node_root_bisection_depth", 0),
            "expected_tube_boxes_sha256": expected_digest,
        }
        tasks.append(task)

    context = mp.get_context("fork")
    with context.Pool(
        min(workers, os.cpu_count() or 1), initializer=init_worker,
        initargs=(precision_bits,),
    ) as pool:
        rows = list(pool.imap(analyze_link, tasks))

    certified = [row for row in rows if row["relative_interior_full_two_sided_collar_certified"]]
    total_strips = sum(row["tangent_strip_count"] for row in rows)
    certified_strips = sum(row["certified_HIT_root_sheet_strip_count"] for row in rows)
    residual_strips = sum(row["residual_strip_count"] for row in rows)
    link_type_histogram = Counter(row["link_type"] for row in certified)
    candidate_triples: Counter[str] = Counter()
    bypass_winners: Counter[str] = Counter()
    competitor_histogram: Counter[str] = Counter()
    for row in rows:
        candidate_triples.update(row["candidate_count_triple_histogram"])
        bypass_winners.update(row["BYPASS_winner_histogram"])
        competitor_histogram.update(row["third_competitor_classification_histogram"])
    result = {
        "producer_precision_bits": precision_bits,
        "input_registered_arc_link_count": 52,
        "input_gap_link_count": 56,
        "input_total_interior_link_count": len(rows),
        "input_tangent_strip_count": total_strips,
        "root_coordinate_width": str(ROOT_COORDINATE_WIDTH),
        "root_coordinate_depth": ROOT_COORDINATE_DEPTH,
        "certified_full_two_sided_interior_link_count": len(certified),
        "certified_link_type_histogram": dict(sorted(link_type_histogram.items())),
        "certified_HIT_root_sheet_strip_count": certified_strips,
        "certified_BYPASS_root_sheet_strip_count": certified_strips,
        "certified_two_sided_root_sheet_strip_count": 2 * certified_strips,
        "remaining_interior_link_count": len(rows) - len(certified),
        "remaining_strip_residual_count": residual_strips,
        "candidate_count_triple_histogram": dict(sorted(candidate_triples.items())),
        "third_competitor_classification_histogram": dict(sorted(competitor_histogram.items())),
        "BYPASS_winner_histogram": dict(sorted(bypass_winners.items())),
        "official_path_run_count": sum(row["official_path_run_count"] for row in rows),
        "D0_singular_trace_edge_count": len(rows),
        "HIT_BYPASS_are_separate_real_root_charts": True,
        "cross_link_registered_port_collar_stitch_installed": False,
        "whole_face_transverse_collar_atlas_certified": False,
        "actual_homogeneous_child_count": 0,
        "new_Gate5_field_count": 0,
        "global_Gate5": "10/18",
        "global_CM2": "NO-GO_FOR_CLAIM",
        "interior_link_rows": rows,
        "interior_link_rows_sha256": digest(rows),
        "strict_scope": (
            "separate positive-width open HIT and BYPASS implicit root sheets, complete owner ordering, "
            "and official three-key path constancy over every certified strip of the 52 Round109 "
            "registered-arc and 56 Round100 gap interior tangent tubes"
        ),
        "strict_nonclaims": [
            "the common D=0 trace edge is singular, excluded from both regular sheets, and is not an operator child",
            "the endpoint/source-grazing collars are outside this interior-link certificate",
            "no registered-port cross-link transverse overlap or whole-face collar atlas is certified",
            "no homogeneity-strip generator, actual standard-curve recut, or F1-F6 row is installed",
            "official word-key constancy does not itself install a Gate5 field",
            "the inherited tangent-tube endpoint convention is not upgraded beyond its frozen scope",
        ],
        "upstream_and_executable_pins": PINS,
    }
    if total_strips != 67584:
        raise RuntimeError(f"unexpected tangent strip census: {total_strips}")
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build(args.precision_bits, args.workers), sort_keys=True, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
