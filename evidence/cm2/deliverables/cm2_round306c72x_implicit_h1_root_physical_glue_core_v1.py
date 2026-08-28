#!/usr/bin/env python3
"""Pure reusable evidence constructors for implicit H1 graph state glue.

This module performs no file IO and publishes nothing.  Callers supply pinned
numeric modules, an exact box, lineage, and the already validated chart-seam
authority.  The same constructors are intended for C72b2 boundary graphs and
the later REGULAR_FULL_FACE_GRAPH scope.
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
from fractions import Fraction as Q
from typing import Any, Mapping

SCHEMA = "cm2.round306c72x.implicit-h1-root-physical-glue-core.v1"
FROZEN_OWNER = "W[1,0]"
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
PRECISION = 384


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def sign_name(value: int) -> str:
    need(value in {-1, 1}, "strict sign")
    return "NEGATIVE" if value < 0 else "POSITIVE"


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def exact_faces(pair: int, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    return {
        "T_LOW": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1]},
        "T_HIGH": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1]},
        "P_LOW": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1]},
        "P_HIGH": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".exact-face-key", **dict(spec)})


def root_id(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".unique-H1-edge-root",
                   "collision1_owner": FROZEN_OWNER,
                   "equation": "H1=nx^2-ny^2", **dict(spec)})


def collision0_delta(r185: Any, parent: str, box: Any, target: str) -> Any:
    return r185.ad_root(r185.ad_initial_geometry(parent, box), target)["Delta"]


def next_owner(r139: Any, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    time2 = r139.lower.time3.time2_cert
    census = collections.Counter()
    future = []
    for identifier in time2.translated_candidate_ids(FROZEN_OWNER, state["chart"]):
        row = time2.candidate_root(state["contact_x"], state["contact_y"],
                                  state["outgoing_x"], state["outgoing_y"],
                                  state["s"], identifier)
        kind = row["classification"]
        need(kind in {"no_real_intersection", "intersection_strictly_behind",
                      "strict_future_near_root"}, "collision2 competitor")
        census[kind] += 1
        if kind == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future)]
    need(len(winners) == 1, "unique collision2 owner")
    selected_id, selected = winners[0]
    gaps = [row["near"] - selected["near"] for identifier, row in future
            if identifier != selected_id]
    need(all(bool(gap > 0) for gap in gaps), "collision2 strict order")
    return selected_id, {"classification_census": dict(sorted(census.items())),
                         "strict_future_candidate_count": len(future),
                         "all_owner_order_gaps_strict": True}


def downstream_W_closed_box(r185: Any, r139: Any, origin: str, box: Any,
                            expected_word: str, expected_owners: set[str],
                            pair_index: dict[Any, Any], pattern_index: dict[Any, Any],
                            cores: tuple[Any, ...]) -> dict[str, Any]:
    """Prove a W-route mismatch on the closed rectangular box.

    Since the enclosure is over the entire closed box, every strict margin also
    applies to any implicit H1 graph subset.  Chart ownership is supplied
    separately by ``implicit_graph_state_glue``.
    """
    raw = r185.ad_root(r185.ad_initial_geometry(origin, box), FROZEN_OWNER)
    delta = r185.centered_enclosure(
        lambda parent, current, target: collision0_delta(
            r185, parent, current, target),
        origin, box, FROZEN_OWNER, raw["Delta"])
    need(bool(delta > 0), "centered collision1 Delta")
    radius = raw["radius"].value
    radical = delta.sqrt()
    transverse = raw["transverse"].value
    near = raw["ell"].value - radical
    tau = r139.lower.time3.time2_cert.step1.arbq(
        r139.lower.time3.time2_cert.first_hit.TAU_MAX)
    need(bool(near > 0) and bool(near < tau), "collision1 near root/tau")
    chart_id = ":".join(origin.split(":")[:2])
    atom = r139.lower.step1.Atom(CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
                                 box.t0, box.t1, box.p0, box.p1,
                                 Q(0), Q(0), "c72x-glue")
    initial = r139.lower.round136.initial_state(atom)
    ux, uy = initial["outgoing_x"], initial["outgoing_y"]
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    momentum = transverse / radius
    cosine = radical / radius
    cx, cy = r139.lower.time3.time2_cert.target_center(FROZEN_OWNER, initial["s"])
    physical = {"contact_x": cx + radius * nx,
                "contact_y": cy + radius * ny,
                "outgoing_x": cosine * nx - momentum * ny,
                "outgoing_y": cosine * ny + momentum * nx,
                "s": initial["s"], "normal_x": nx, "normal_y": ny,
                "p": momentum, "chart": "W"}
    owner = {"selected_target_id": FROZEN_OWNER, "selected_root": near,
             "normal_x": nx, "normal_y": ny, "p": momentum,
             "cosine": cosine}
    word, error = r139.lower.round136.translation_normalized_official_word(
        initial, "W[0,0]", owner, pair_index, pattern_index)
    need(word is not None and error is None, "collision1 official word")
    compact = r139.lower.round136.compact_key(word["key"])
    word_id = compact["official_word_key_id"]
    evidence = {"method": "CHART_FREE_PHYSICAL_STATE_THEN_W_HALF_OPEN_OWNER_ROUTE",
                "closed_rectangular_box_enclosure": True,
                "therefore_applies_to_implicit_H1_graph_subset": True,
                "centered_Delta": arb_payload(delta),
                "near_root": arb_payload(near),
                "tau_minus_near": arb_payload(tau - near),
                "physical_state_formula": {
                    "contact": "target_center(s)+R*(nx,ny)",
                    "outgoing": "(sqrt(Delta)/R)*(nx,ny)+(p/R)*(-ny,nx)"},
                "computed_official_word_key_id": word_id,
                "expected_official_word_key_id": expected_word,
                "registry_row_sha256": compact["registry_row_sha256"],
                "ordered_clean_wall_record": word["ordered_clean_wall_record"]}
    if word_id != expected_word:
        return {**evidence, "outcome": "COLLISION1_OFFICIAL_WORD_MISMATCH",
                "selected_collision2_owner": None}
    selected, order = next_owner(r139, physical)
    need(selected not in expected_owners, "expected owner requires C3 handoff")
    return {**evidence, "outcome": "COLLISION2_STRICT_OWNER_MISMATCH",
            "selected_collision2_owner": selected,
            "collision2_owner_order": order,
            "expected_collision2_owner_set": sorted(expected_owners)}


def implicit_graph_state_glue(normal_signs: dict[str, int],
                              root_ids: list[str], route: dict[str, Any],
                              chart_authority: dict[str, Any]) -> dict[str, Any]:
    """Materialize exact W-owned graph glue and its downstream exit."""
    need(chart_authority == {
        "manifest_file_sha256":
            "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
        "certificate_sha256":
            "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
        "eight_chart_seam_ownership": "CERTIFIED",
        "diagonal_tie": "E or W owns; N or S excludes",
        "same_physical_normal_on_paired_representations": True,
        "duplicate_trace_is_identified_not_added": True,
    }, "frozen chart quotient authority")
    need(normal_signs["nx"] != 0 and normal_signs["ny"] != 0 and
         len(root_ids) == 2, "implicit graph glue inputs")
    shadow = "N" if normal_signs["ny"] > 0 else "S"
    return {
        "schema": SCHEMA + ".implicit-graph-state-glue",
        "implicit_equation": "H1=nx^2-ny^2=0",
        "graph_definition": "UNIQUE_REGULAR_ROOT_GRAPH_BETWEEN_TWO_EXACT_FACE_ROOTS",
        "boundary_root_ids": root_ids,
        "paired_charts": ["W", shadow],
        "half_open_physical_owner_chart": "W",
        "shadow_chart": shadow,
        "chart_authority": chart_authority,
        "same_physical_normal_under_cross_chart_transform": True,
        "same_physical_contact_and_outgoing_state_under_cross_chart_transform": True,
        "cross_chart_transform": {
            "input": "W-owned implicit H1 root state",
            "output": shadow + " shadow representation of the same physical normal",
            "physical_normal_identity": "(nx,ny)_W=(nx,ny)_shadow",
            "physical_state_identity":
                "contact_W=contact_shadow; outgoing_W=outgoing_shadow"},
        "W_route_evaluated_on_closed_ambient_box": True,
        "W_route_strict_margins_restrict_to_graph": True,
        "graph_exit_class": "STRICT_EXCLUSION",
        "graph_exclusion_reason": route["outcome"],
        "graph_is_not_source_grazing_or_cemetery": True,
        "graph_is_not_counted_as_a_coordinate_terminal": True,
        "duplicate_physical_trace_added": False,
        "full_dimensional_Kraft_weight": "0",
    }


def geometry_and_roots(r185: Any, origin: str, box: Any,
                       atlas: dict[str, Any]) -> tuple[dict[str, Any], list[str], str]:
    full, nx, ny = r185.collision1_h1_ad(origin, box, FROZEN_OWNER)
    dt, dp = sign(full.derivative[0]), sign(full.derivative[1])
    need(dt != 0 and dp != 0 and sign(nx.value) != 0 and sign(ny.value) != 0,
         "strict derivatives and normal components")
    raw_box = atlas["exact_representative_box"]
    corners, corner_signs = [], []
    for t, p in itertools.product(raw_box["t"], raw_box["p"]):
        point = r185.point_box(box, Q(t), Q(p), Q(0), ".c72x.corner")
        value, _nx, _ny = r185.collision1_h1_ad(origin, point, FROZEN_OWNER)
        current = sign(value.value)
        need(current != 0, "strict corner")
        corner_signs.append(current)
        corners.append({"point": {"t": t, "p": p, "s": "0"},
                        "H1": arb_payload(value.value), "sign": current})
    common = {"precision_bits": PRECISION, "equation": "H1=nx^2-ny^2",
              "full_box_natural_interval": arb_payload(full.value),
              "full_box_derivatives": {"t": arb_payload(full.derivative[0]),
                                       "p": arb_payload(full.derivative[1]),
                                       "s": arb_payload(full.derivative[2])},
              "normal_component_bounds": {"nx": arb_payload(nx.value),
                                          "ny": arb_payload(ny.value)},
              "normal_component_signs": {"nx": sign(nx.value), "ny": sign(ny.value)},
              "four_strict_corner_records": corners,
              "corner_zero_incidence_count": 0}
    if len(set(corner_signs)) == 1:
        side = corner_signs[0]
        return ({**common, "kind": "STRICT_WHOLE_CHILD_H1_SIDE",
                 "proof_method": "STRICT_DT_DP_MONOTONE_EXTREMAL_CORNER",
                 "strict_H1_sign": sign_name(side), "boundary_root_count": 0,
                 "partition": {"H1_LT_0": "EXACT_CHILD" if side < 0 else "EMPTY",
                               "H1_EQ_0": "EMPTY",
                               "H1_GT_0": "EXACT_CHILD" if side > 0 else "EMPTY",
                               "pairwise_disjoint": True, "union_exact_child": True}},
                [], "STRICT_NEGATIVE" if side < 0 else "STRICT_POSITIVE")
    specs = exact_faces(atlas["pair_index"], raw_box)
    indices = {"T_LOW": (0, 1), "T_HIGH": (2, 3),
               "P_LOW": (0, 2), "P_HIGH": (1, 3)}
    edges, roots = [], []
    for edge_id in ("T_LOW", "T_HIGH", "P_LOW", "P_HIGH"):
        left, right = indices[edge_id]
        signs = [corner_signs[left], corner_signs[right]]
        spec = specs[edge_id]
        tangent = dt if spec["varying_axis"] == "t" else dp
        need((tangent > 0 and signs[0] <= signs[1]) or
             (tangent < 0 and signs[0] >= signs[1]), "edge order")
        row = {"edge_id": edge_id, "exact_face": spec,
               "face_key_sha256": face_key(spec),
               "ordered_endpoint_signs": signs}
        if signs[0] != signs[1]:
            identifier = root_id(spec)
            roots.append({"root_id": identifier, "edge_id": edge_id,
                          "exact_face": spec, "face_key_sha256": face_key(spec),
                          "definition": "UNIQUE_H1_ZERO_IN_OPEN_EXACT_FACE",
                          "existence_by_IVT": True,
                          "uniqueness_by_strict_tangential_derivative": True,
                          "not_a_corner": True})
            edges.append({**row, "disposition": "ONE_UNIQUE_INTERIOR_H1_ROOT",
                          "root_id": identifier})
        else:
            edges.append({**row, "disposition": "STRICT_NO_H1_ROOT",
                          "root_id": None, "strict_H1_sign": sign_name(signs[0])})
    need(len(roots) == 2, "two roots")
    ids = [row["root_id"] for row in roots]
    return ({**common, "kind": "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS",
             "proof_method": "STRICT_DT_DP_FOUR_CORNERS_FOUR_FACES_TWO_ROOTS_IFT",
             "boundary_edges": edges, "boundary_roots": roots,
             "boundary_root_count": 2, "single_connected_graph_arc": True,
             "partition": {"H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION",
                           "H1_EQ_0": "EXACT_SINGLE_REGULAR_GRAPH_ARC",
                           "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION",
                           "pairwise_disjoint": True, "union_exact_child": True,
                           "W_half_open_owns_H1_EQ_0": True,
                           "graph_full_dimensional_Kraft_weight": "0"}},
            ids, "CLIPPED")

