#!/usr/bin/env python3
"""Independent high-precision verifier for the Round116 interior collars.

This verifier deliberately does not import the Round116 producer.  It
reconstructs every frozen tangent strip from pinned upstream data, re-evaluates
the two implicit root equations, all candidate orders, and all official word
keys at higher precision, and checks every stored dyadic margin lower bound.
"""
from __future__ import annotations

import argparse
import copy
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
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round116.rank3-interior-two-sided-transverse-collar.v1"
VERIFY_SCHEMA = "cm2.round116.rank3-interior-two-sided-transverse-collar.verification.v1"
CERTIFICATE = HERE / "cm2-round116-rank3-interior-two-sided-transverse-collar-2026-07-23.json"
PRODUCER = HERE / "cm2_round116_rank3_interior_two_sided_transverse_collar.py"
CERTIFICATE_SHA256 = "504e070eea10fbab3b1968423ecedcda6fa8fc20549adb9ef3e9ed42bd2c45b3"
PRODUCER_SHA256 = "91ea057ad31517ce6b390561e9b894e219a837fa3a3be793fc96db082566f3f7"
PRECISION_BITS = 640
ROOT_WIDTH = Q(1, 2**64)
REGISTRY_ROWS_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"

FILES = {
    "round100": "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json",
    "round102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "round109": "cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json",
    "round110": "cm2-round110-rank3-gap-tube-side-decomposition-2026-07-22.json",
}
UPSTREAM_PINS = {
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

RESULT_KEYS = {
    "BYPASS_winner_histogram", "D0_singular_trace_edge_count",
    "HIT_BYPASS_are_separate_real_root_charts", "actual_homogeneous_child_count",
    "candidate_count_triple_histogram", "certified_BYPASS_root_sheet_strip_count",
    "certified_HIT_root_sheet_strip_count", "certified_full_two_sided_interior_link_count",
    "certified_link_type_histogram", "certified_two_sided_root_sheet_strip_count",
    "global_CM2", "global_Gate5", "input_gap_link_count",
    "input_registered_arc_link_count", "input_tangent_strip_count",
    "input_total_interior_link_count", "interior_link_rows", "interior_link_rows_sha256",
    "new_Gate5_field_count", "official_path_run_count", "producer_precision_bits",
    "remaining_interior_link_count", "remaining_strip_residual_count",
    "root_coordinate_depth", "root_coordinate_width", "strict_nonclaims", "strict_scope",
    "third_competitor_classification_histogram", "upstream_and_executable_pins",
    "cross_link_registered_port_collar_stitch_installed",
    "whole_face_transverse_collar_atlas_certified",
}
ROW_KEYS = {
    "BYPASS_designated_miss_and_actual_winner_on_open_sheet_certified",
    "BYPASS_root_equation", "BYPASS_winner_histogram",
    "HIT_designated_actual_owner_on_open_sheet_certified", "HIT_root_equation",
    "candidate_count_triple_histogram", "certified_BYPASS_root_sheet_strip_count",
    "certified_HIT_root_sheet_strip_count", "certified_adjacent_strip_seam_count",
    "certified_two_sided_root_sheet_strip_count", "common_singular_edge",
    "complete_candidate_owner_constancy_certified", "designated_third_candidate_id",
    "discrete_strip_evidence_sha256", "face_id", "first_second_owner_constancy_certified",
    "implicit_graph_axis", "interior_transverse_collar_id", "left_registered_port_id",
    "link_rank", "link_type", "official_path_run_count", "official_path_runs",
    "official_path_runs_sha256", "official_three_key_path_constancy_certified",
    "regular_root_coordinate_domain", "relative_interior_full_two_sided_collar_certified",
    "residual_rows", "residual_rows_sha256", "residual_strip_count",
    "right_registered_port_id", "root_coordinate_depth", "root_coordinate_width",
    "second_selected_target_id", "signed_transverse_tangency_factor_sign",
    "source_core_index", "source_parameter_axis", "strict_margin_lower_bounds",
    "tangent_strip_count", "tangent_tube_boxes_sha256",
    "third_competitor_classification_histogram", "tube_method",
}
MARGIN_NAMES = {
    "BYPASS_negative_face_after_shift", "HIT_actual_root_positive",
    "HIT_positive_face_after_shift", "absolute_transverse_D_t_derivative",
    "adjacent_t_enclosure_overlap", "bypass_winner_below_flight_cap",
    "bypass_winner_pairwise_gap", "bypass_winner_root_positive",
    "competitor_after_tangent_flight", "competitor_behind_far_root",
    "competitor_future_root_positive", "competitor_miss_discriminant",
    "designated_tangent_flight_below_cap", "designated_tangent_flight_positive",
}
OPTIONAL_MARGIN_NAMES = {"competitor_behind_far_root"}

WORK_CORES: tuple[Any, ...] = ()
PAIR_INDEX: dict[tuple[str, str], int] = {}
PATTERN_INDEX: dict[tuple[str, ...], int] = {}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite number: {token}")


def strict_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)


def load_closed(name: str, schema: str) -> dict[str, Any]:
    document = strict_json((HERE / name).read_text(encoding="utf-8"))
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError("dependency is not closed")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError("dependency envelope mismatch")
    return document["result"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def static_contract(document: dict[str, Any], check_digest: bool = True) -> dict[str, Any]:
    require(set(document) == {"schema", "result", "result_sha256"}, "top-level keys")
    require(document["schema"] == SCHEMA, "schema")
    result = document["result"]
    require(isinstance(result, dict) and set(result) == RESULT_KEYS, "result keys")
    if check_digest:
        require(document["result_sha256"] == digest(result), "result digest")
    require(result["producer_precision_bits"] == 512, "producer precision")
    require(result["input_registered_arc_link_count"] == 52, "registered census")
    require(result["input_gap_link_count"] == 56, "gap census")
    require(result["input_total_interior_link_count"] == 108, "link census")
    require(result["input_tangent_strip_count"] == 67584, "strip census")
    require(result["root_coordinate_width"] == str(ROOT_WIDTH), "root width")
    require(result["root_coordinate_depth"] == 64, "root depth")
    require(result["certified_full_two_sided_interior_link_count"] == 108, "collar count")
    require(result["certified_HIT_root_sheet_strip_count"] == 67584, "HIT count")
    require(result["certified_BYPASS_root_sheet_strip_count"] == 67584, "BYPASS count")
    require(result["certified_two_sided_root_sheet_strip_count"] == 135168, "sheet count")
    require(result["remaining_interior_link_count"] == 0, "link residual")
    require(result["remaining_strip_residual_count"] == 0, "strip residual")
    require(result["candidate_count_triple_histogram"] == {
        "55/55/57": 36864, "57/55/57": 30720,
    }, "candidate triples")
    require(result["official_path_run_count"] == 108, "path-run count")
    require(result["D0_singular_trace_edge_count"] == 108, "trace edge count")
    require(result["HIT_BYPASS_are_separate_real_root_charts"] is True, "separate charts")
    require(result["cross_link_registered_port_collar_stitch_installed"] is False, "cross-link stitch nonclaim")
    require(result["whole_face_transverse_collar_atlas_certified"] is False, "whole-face atlas nonclaim")
    require(result["actual_homogeneous_child_count"] == 0, "homogeneous nonclaim")
    require(result["new_Gate5_field_count"] == 0, "Gate5 field nonclaim")
    require(result["global_Gate5"] == "10/18", "Gate5 status")
    require(result["global_CM2"] == "NO-GO_FOR_CLAIM", "CM2 status")
    require(result["upstream_and_executable_pins"] == UPSTREAM_PINS, "pin map")
    require(result["interior_link_rows_sha256"] == digest(result["interior_link_rows"]), "row digest")
    require(len(result["interior_link_rows"]) == 108, "row length")
    for row in result["interior_link_rows"]:
        require(isinstance(row, dict) and set(row) == ROW_KEYS, "row keys")
        require(row["root_coordinate_depth"] == 64 and row["root_coordinate_width"] == str(ROOT_WIDTH), "row width")
        require(row["implicit_graph_axis"] == "t_as_function_of_p" and row["source_parameter_axis"] == "p", "row axes")
        require(row["relative_interior_full_two_sided_collar_certified"] is True, "row collar")
        require(row["HIT_designated_actual_owner_on_open_sheet_certified"] is True, "row HIT")
        require(row["BYPASS_designated_miss_and_actual_winner_on_open_sheet_certified"] is True, "row BYPASS")
        require(row["residual_strip_count"] == 0 and row["residual_rows"] == [], "row residual")
        require(row["residual_rows_sha256"] == digest([]), "residual digest")
        require(row["official_path_run_count"] == 1 and len(row["official_path_runs"]) == 1, "row path run")
        require(row["official_path_runs_sha256"] == digest(row["official_path_runs"]), "path digest")
        margin_names = set(row["strict_margin_lower_bounds"])
        require(
            MARGIN_NAMES - OPTIONAL_MARGIN_NAMES <= margin_names <= MARGIN_NAMES,
            "margin names",
        )
        require("excluded from both regular sheets" in row["common_singular_edge"], "singular-edge exclusion")
        require(row["regular_root_coordinate_domain"].startswith("HIT 0<c3"), "open root domain")
        for name, margin in row["strict_margin_lower_bounds"].items():
            require(set(margin) == {"strict_lower_bound", "dyadic_depth", "observation_count"}, f"margin keys:{name}")
            depth = margin["dyadic_depth"]
            exact = Q(2**(-depth), 1) if depth < 0 else Q(1, 2**depth)
            require(Q(margin["strict_lower_bound"]) == exact and margin["observation_count"] > 0, f"margin encoding:{name}")
        run = row["official_path_runs"][0]
        require(run["strip_start_inclusive"] == 0 and run["strip_end_exclusive"] == row["tangent_strip_count"], "run coverage")
        for side in ("HIT", "BYPASS"):
            ids = run[f"{side}_official_word_key_ids"]
            require(len(ids) == 3, "three key path")
            require(run[f"{side}_official_path_id"] == f"gate5-rank3-interior-{side}-path:" + digest(ids), "path id")
    return result


def init_worker(precision_bits: int) -> None:
    global WORK_CORES, PAIR_INDEX, PATTERN_INDEX
    ctx.prec = precision_bits
    WORK_CORES = tuple(core_cert.physical_cores())
    round87.WORK_CORES = WORK_CORES
    PAIR_INDEX, PATTERN_INDEX, registry_sha = component_cert.key_index_tables()
    require(registry_sha == REGISTRY_ROWS_SHA256, "registry replay")


def standard_boxes(left: dict[str, Any], right: dict[str, Any], source: Any, count: int, depth: int) -> list[tuple[Q, Q, Q, Q]]:
    a, b = round89.root_rect(left), round89.root_rect(right)
    ts = ((a[0] + a[1]) / 2, (b[0] + b[1]) / 2)
    ps = ((a[2] + a[3]) / 2, (b[2] + b[3]) / 2)
    require(abs(ts[1] - ts[0]) < abs(ps[1] - ps[0]), "axis")
    collar = (source.t1 - source.t0) / Q(2**depth)
    boxes = []
    for index in range(count):
        u0, u1 = Q(index, count), Q(index + 1, count)
        p0, p1 = ps[0] + u0 * (ps[1] - ps[0]), ps[0] + u1 * (ps[1] - ps[0])
        t0, t1 = ts[0] + u0 * (ts[1] - ts[0]), ts[0] + u1 * (ts[1] - ts[0])
        boxes.append((max(source.t0, min(t0, t1) - collar), min(source.t1, max(t0, t1) + collar), min(p0, p1), max(p0, p1)))
    return boxes


def tracked_boxes(left: dict[str, Any], right: dict[str, Any], source: Any, branch: tuple[int, str, str, int], count: int, depth: int) -> list[tuple[Q, Q, Q, Q]]:
    a, b = round89.root_rect(left), round89.root_rect(right)
    ts = ((a[0] + a[1]) / 2, (b[0] + b[1]) / 2)
    ps = ((a[2] + a[3]) / 2, (b[2] + b[3]) / 2)
    width = source.t1 - source.t0
    def value(p: Q, t: Q) -> arb:
        return third_tangency_jet(source, branch[1], branch[2], t, t, p, p).value
    nodes = []
    for index in range(count + 1):
        u = Q(index, count); p = ps[0] + u * (ps[1] - ps[0]); prediction = ts[0] + u * (ts[1] - ts[0]); bracket = None
        for search_depth in range(4, 49, 4):
            radius = width / Q(2**search_depth); lower = max(source.t0, prediction - radius); upper = min(source.t1, prediction + radius)
            ls, us = strict_sign(value(p, lower)), strict_sign(value(p, upper))
            if ls * us != -1: continue
            for _ in range(48):
                middle = (lower + upper) / 2; ms = strict_sign(value(p, middle))
                if ms == 0: break
                if ms == ls: lower, ls = middle, ms
                else: upper, us = middle, ms
            else: bracket = (p, lower, upper); break
        require(bracket is not None, "tracked node")
        nodes.append(bracket)
    collar = width / Q(2**depth); boxes = []
    for index in range(count):
        p0, t00, t01 = nodes[index]; p1, t10, t11 = nodes[index + 1]
        boxes.append((max(source.t0, min(t00, t10) - collar), min(source.t1, max(t01, t11) + collar), min(p0, p1), max(p0, p1)))
    return boxes


class BoundChecker:
    def __init__(self, stored: dict[str, Any]) -> None:
        self.bounds = {name: aq(Q(row["strict_lower_bound"])) for name, row in stored.items()}
        self.expected = {name: row["observation_count"] for name, row in stored.items()}
        self.counts: Counter[str] = Counter()
    def observe(self, name: str, value: arb) -> None:
        require(name in self.bounds and bool(value > self.bounds[name]), f"stored margin failed:{name}")
        self.counts[name] += 1
    def finish(self) -> None:
        require(dict(self.counts) == self.expected, "margin observation counts")


def candidate_order(state2: dict[str, Any], current: str, target: str, tangent: arb, checker: BoundChecker) -> tuple[str, arb, Counter[str], int]:
    ids = tuple(time3.time2_cert.translated_candidate_ids(current, state2["chart"])); require(target in ids, "target membership")
    future = []; histogram: Counter[str] = Counter()
    for candidate_id in ids:
        if candidate_id == target: continue
        cx, cy = time3.time2_cert.target_center(candidate_id, state2["s"]); dx, dy = cx - state2["contact_x"], cy - state2["contact_y"]
        ell = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy
        transverse = -state2["outgoing_y"] * dx + state2["outgoing_x"] * dy
        radius = aq(time3.time2_cert.first_hit.RADIUS[candidate_id[0]]); discriminant = radius * radius - transverse * transverse
        if strict_sign(discriminant) == -1:
            histogram["no_real_intersection"] += 1; checker.observe("competitor_miss_discriminant", -discriminant); continue
        require(strict_sign(discriminant) == 1, "candidate discriminant")
        radical = discriminant.sqrt(); near, far = ell - radical, ell + radical
        if strict_sign(far) == -1:
            histogram["intersection_strictly_behind"] += 1; checker.observe("competitor_behind_far_root", -far); continue
        require(strict_sign(near) == 1, "candidate root")
        histogram["strict_future_near_root"] += 1; checker.observe("competitor_future_root_positive", near); checker.observe("competitor_after_tangent_flight", near - tangent); future.append((candidate_id, near))
    winners = [(identifier, near) for identifier, near in future if all(identifier == other or bool(near < other_near) for other, other_near in future)]
    require(len(winners) == 1, "winner"); winner, root = winners[0]; tau = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    checker.observe("bypass_winner_root_positive", root); checker.observe("bypass_winner_below_flight_cap", tau - root)
    for identifier, near in future:
        if identifier != winner: checker.observe("bypass_winner_pairwise_gap", near - root)
    return winner, root, histogram, len(ids)


def compact_key(key: dict[str, Any]) -> dict[str, Any]:
    return {"official_word_key_id": key["word_key_id"], "ordinal_zero_based": key["ordinal_zero_based"], "registry_row_sha256": key["row_sha256"], "registry_row": key["row"]}


def verify_link(task: dict[str, Any]) -> dict[str, Any]:
    row = task["certificate_row"]; source = WORK_CORES[row["source_core_index"]]; left, right = task["left"], task["right"]; branch = round89.key(left)
    require(branch == round89.key(right), "branch")
    boxes = tracked_boxes(left, right, source, branch, row["tangent_strip_count"], task["collar_depth"]) if row["tube_method"] == "TRACKED_NODE_ROOT_CHAIN" else standard_boxes(left, right, source, row["tangent_strip_count"], task["collar_depth"])
    require(digest([list(map(str, box)) for box in boxes]) == row["tangent_tube_boxes_sha256"], "tube digest")
    checker = BoundChecker(row["strict_margin_lower_bounds"]); c_interval = time3.time2_cert.first_hit.arb_interval(Q(0), ROOT_WIDTH); c_upper = aq(ROOT_WIDTH)
    target_radius = aq(time3.time2_cert.first_hit.RADIUS[branch[2][0]]); radius_square = target_radius * target_radius; tau = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    first_key = component_cert.word_key(source.chart_id, source.target_id, tuple(source.crossings), PAIR_INDEX, PATTERN_INDEX)
    discrete = []; signatures = []; triples: Counter[str] = Counter(); competitors: Counter[str] = Counter(); winners: Counter[str] = Counter(); previous = None
    for index, box in enumerate(boxes):
        if previous is not None:
            require(previous[3] == box[2], "p seam"); overlap = min(previous[1], box[1]) - max(previous[0], box[0]); require(overlap > 0, "t seam"); checker.observe("adjacent_t_enclosure_overlap", aq(overlap))
        previous = box; t0, t1, p0, p1 = box; jet = third_tangency_jet(source, branch[1], branch[2], *box); ds = strict_sign(jet.gradient[0]); require(ds != 0, "IFT derivative"); checker.observe("absolute_transverse_D_t_derivative", jet.gradient[0] if ds > 0 else -jet.gradient[0])
        faces = [third_tangency_jet(source, branch[1], branch[2], t, t, p0, p1).value for t in (t0, t1)]; negative = [x for x in faces if strict_sign(x) == -1]; positive = [x for x in faces if strict_sign(x) == 1]; require(len(negative) == len(positive) == 1, "faces")
        checker.observe("HIT_positive_face_after_shift", positive[0] - radius_square * c_upper * c_upper); checker.observe("BYPASS_negative_face_after_shift", -(negative[0] + radius_square * c_upper * c_upper))
        atom = step1.Atom(branch[0], source, *box, Q(0), Q(0), f"round116-verifier:{task['index']}:{index}")
        first_root, first_missed, first_later = time3.time2_cert.first_hit.certify_first_hit_patch(
            atom.phase_box, source.target_id
        )
        require(bool(first_root > 0) and first_missed + first_later + 1 == len(time3.time2_cert.first_hit.candidate_ids(source.chart_id)), "complete first owner replay")
        state1 = time3.time2_cert.first_collision_outgoing(atom)
        require(state1 is not None, "first outgoing state")
        owner2, second_status = time3.time2_cert.strict_second_owner(atom)
        require(owner2 is not None and second_status == "strict_unique_second_collision_owner" and owner2["selected_target_id"] == branch[1], "complete second owner replay")
        state2 = time3.second_outgoing_state(atom, state1, owner2); require(state2 is not None, "state2")
        tx, ty = time3.time2_cert.target_center(branch[2], state2["s"]); dx, dy = tx - state2["contact_x"], ty - state2["contact_y"]
        tangent = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy; transverse = -state2["outgoing_y"] * dx + state2["outgoing_x"] * dy; require(strict_sign(transverse) == branch[3], "orientation")
        checker.observe("designated_tangent_flight_positive", tangent); checker.observe("designated_tangent_flight_below_cap", tau - tangent); hit_root = tangent - target_radius * c_interval; checker.observe("HIT_actual_root_positive", hit_root)
        winner, winner_root, histogram, third_count = candidate_order(state2, branch[1], branch[2], tangent, checker); competitors.update(histogram); winners[winner] += 1
        counts = (len(time3.time2_cert.first_hit.candidate_ids(source.chart_id)), len(tuple(time3.time2_cert.translated_candidate_ids(source.target_id, state1["chart"]))), third_count); triples["/".join(map(str, counts))] += 1
        second, error = component_cert.second_word_for_atom(atom, branch[1], PAIR_INDEX, PATTERN_INDEX); require(second is not None and error is None, "second word")
        hit, error = time3.third_word(state2, branch[1], {"selected_target_id": branch[2], "selected_root": hit_root}, PAIR_INDEX, PATTERN_INDEX); require(hit is not None, f"HIT word:{error}")
        bypass, error = time3.third_word(state2, branch[1], {"selected_target_id": winner, "selected_root": winner_root}, PAIR_INDEX, PATTERN_INDEX); require(bypass is not None, f"BYPASS word:{error}")
        hit_ids = [first_key["word_key_id"], second["key"]["word_key_id"], hit["key"]["word_key_id"]]; bypass_ids = [first_key["word_key_id"], second["key"]["word_key_id"], bypass["key"]["word_key_id"]]
        signature = {"candidate_counts_by_leg": list(counts), "outgoing_chart_sequence": [source.chart_id, state1["chart"], state2["chart"]], "common_first_two_owner_ids": [source.target_id, branch[1]], "HIT_third_owner_id": branch[2], "BYPASS_third_owner_id": winner, "HIT_official_word_key_ids": hit_ids, "BYPASS_official_word_key_ids": bypass_ids, "HIT_official_path_id": "gate5-rank3-interior-HIT-path:" + digest(hit_ids), "BYPASS_official_path_id": "gate5-rank3-interior-BYPASS-path:" + digest(bypass_ids), "first_official_key": compact_key(first_key), "second_official_key": compact_key(second["key"]), "HIT_third_official_key": compact_key(hit["key"]), "BYPASS_third_official_key": compact_key(bypass["key"])}
        signatures.append((index, signature)); discrete.append({"strip_index": index, "D_t_derivative_sign": ds, "D_face_signs_in_t_order": [strict_sign(x) for x in faces], "candidate_counts_by_leg": list(counts), "competitor_classification_histogram": dict(sorted(histogram.items())), "outgoing_chart_sequence": signature["outgoing_chart_sequence"], "BYPASS_third_owner_id": winner, "HIT_official_word_key_ids": hit_ids, "BYPASS_official_word_key_ids": bypass_ids})
    runs = []
    for index, signature in signatures:
        sd = digest(signature)
        if runs and runs[-1]["strip_end_exclusive"] == index and runs[-1]["signature_sha256"] == sd: runs[-1]["strip_end_exclusive"] = index + 1
        else: runs.append({"strip_start_inclusive": index, "strip_end_exclusive": index + 1, "signature_sha256": sd, **signature})
    checker.finish(); require(digest(discrete) == row["discrete_strip_evidence_sha256"], "discrete digest"); require(runs == row["official_path_runs"], "path runs"); require(dict(sorted(triples.items())) == row["candidate_count_triple_histogram"], "triple histogram"); require(dict(sorted(competitors.items())) == row["third_competitor_classification_histogram"], "competitor histogram"); require(dict(sorted(winners.items())) == row["BYPASS_winner_histogram"], "winner histogram")
    return {"index": task["index"], "strip_count": len(boxes), "triples": dict(triples), "competitors": dict(competitors), "winners": dict(winners), "discrete_sha256": digest(discrete), "runs_sha256": digest(runs)}


def build_tasks(result: dict[str, Any]) -> list[dict[str, Any]]:
    round100 = load_closed(FILES["round100"], "cm2.round100.rank3-immutable-interior-gap-closure.v1"); round102 = load_closed(FILES["round102"], "cm2.round102.rank3-corrected-face-quotient.v1"); round109 = load_closed(FILES["round109"], "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1")
    events, _ = round89.load(); event_by_id = {row["registered_port_id"]: row for row in events}; registered = {frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row for row in round109["registered_arc_rows"]}; gaps = {frozenset((row["left_registered_port_id"], row["right_registered_port_id"])): row for row in round100["gap_rows"]}; links = sorted(round102["interior_link_rows"], key=lambda row: (row["face_id"], row["link_rank"])); cert_rows = result["interior_link_rows"]; require(len(links) == len(cert_rows) == 108, "task census")
    tasks = []
    for index, (link, cert) in enumerate(zip(links, cert_rows)):
        require((link["face_id"], link["link_rank"], link["left_registered_port_id"], link["right_registered_port_id"]) == (cert["face_id"], cert["link_rank"], cert["left_registered_port_id"], cert["right_registered_port_id"]), "task identity")
        endpoints = frozenset((link["left_registered_port_id"], link["right_registered_port_id"])); tube = registered[endpoints] if link["link_type"] == "REGISTERED_PHYSICAL_ARC" else gaps[endpoints]
        tasks.append({"index": index, "certificate_row": cert, "left": event_by_id[link["left_registered_port_id"]], "right": event_by_id[link["right_registered_port_id"]], "collar_depth": tube["dependent_collar_depth"]})
    return tasks


def hostile_static_tests(document: dict[str, Any]) -> int:
    mutations = [
        ("result", "certified_full_two_sided_interior_link_count", 107),
        ("result", "root_coordinate_width", "0"),
        ("result", "global_Gate5", "18/18"),
        ("result", "global_CM2", "CLAIM"),
        ("result", "remaining_strip_residual_count", 1),
        ("result", "actual_homogeneous_child_count", 1),
        ("result", "new_Gate5_field_count", 1),
        ("row", "relative_interior_full_two_sided_collar_certified", False),
        ("row", "BYPASS_designated_miss_and_actual_winner_on_open_sheet_certified", False),
        ("row", "regular_root_coordinate_domain", "closed"),
        ("row", "common_singular_edge", "included operator child"),
        ("row", "official_path_run_count", 2),
    ]
    rejected = 0
    for level, key, value in mutations:
        attack = copy.deepcopy(document)
        if level == "result": attack["result"][key] = value
        else: attack["result"]["interior_link_rows"][0][key] = value
        attack["result"]["interior_link_rows_sha256"] = digest(attack["result"]["interior_link_rows"])
        attack["result_sha256"] = digest(attack["result"])
        try: static_contract(attack)
        except RuntimeError: rejected += 1
    require(rejected == len(mutations), "hostile semantic rejection")
    return rejected


def verify(precision_bits: int = PRECISION_BITS, workers: int = 8) -> dict[str, Any]:
    require(precision_bits >= 640, "verification precision")
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer pin")
    require(sha256(CERTIFICATE) == CERTIFICATE_SHA256, "certificate pin")
    for name, expected in UPSTREAM_PINS.items(): require(sha256(HERE / name) == expected, f"upstream pin:{name}")
    document = strict_json(CERTIFICATE.read_text(encoding="utf-8")); result = static_contract(document)
    context = mp.get_context("fork")
    with context.Pool(min(workers, os.cpu_count() or 1), initializer=init_worker, initargs=(precision_bits,)) as pool:
        verified = list(pool.imap(verify_link, build_tasks(result)))
    require(sum(row["strip_count"] for row in verified) == 67584, "verified strip count")
    triples: Counter[str] = Counter(); competitors: Counter[str] = Counter(); winners: Counter[str] = Counter()
    for row in verified: triples.update(row["triples"]); competitors.update(row["competitors"]); winners.update(row["winners"])
    require(dict(sorted(triples.items())) == result["candidate_count_triple_histogram"], "global triples")
    require(dict(sorted(competitors.items())) == result["third_competitor_classification_histogram"], "global competitors")
    require(dict(sorted(winners.items())) == result["BYPASS_winner_histogram"], "global winners")
    semantic_attacks = hostile_static_tests(document)
    strict_attacks = 0
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        try: strict_json(text)
        except ValueError: strict_attacks += 1
    require(strict_attacks == 3, "strict JSON attacks")
    output = {
        "verification_precision_bits": precision_bits,
        "producer_module_imported": False,
        "independently_reconstructed_interior_link_count": len(verified),
        "independently_reconstructed_tangent_strip_count": 67584,
        "independently_verified_two_sided_root_sheet_strip_count": 135168,
        "independently_verified_candidate_count_triple_histogram": dict(sorted(triples.items())),
        "independently_verified_third_competitor_classification_histogram": dict(sorted(competitors.items())),
        "independently_verified_BYPASS_winner_histogram": dict(sorted(winners.items())),
        "all_stored_dyadic_margin_lower_bounds_rechecked": True,
        "all_official_three_key_paths_rechecked": True,
        "hostile_semantic_mutations_rejected": semantic_attacks,
        "strict_json_attacks_rejected": strict_attacks,
        "certificate_sha256": CERTIFICATE_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "verdict": "PASS",
    }
    return {"schema": VERIFY_SCHEMA, "result": output, "result_sha256": digest(output)}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS); parser.add_argument("--workers", type=int, default=8); parser.add_argument("--output", type=Path); args = parser.parse_args()
    rendered = json.dumps(verify(args.precision_bits, args.workers), sort_keys=True, indent=2) + "\n"
    if args.output is None: print(rendered, end="")
    else: args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__": raise SystemExit(main())
