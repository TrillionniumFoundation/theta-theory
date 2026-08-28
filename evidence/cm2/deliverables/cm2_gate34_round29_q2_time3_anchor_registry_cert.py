#!/usr/bin/env python3
"""Round-29 fresh time-three registry on every certified finite Q2 anchor.

This append-only leaf replays all 114,006 strict Q2-inner atoms at 384-bit
Arb precision.  It reconstructs the second outgoing collision state, searches
the complete translated eight-chart candidate table for a strict third owner,
tests the third collision against all 24 physical cores, and reconstructs the
third clean-wall Gate-5 word.  Whole-box strict return and survivor boxes are
materialized as nonempty finite-open R3/Q3 component cells.  Every unresolved
root box and its exact parameter-averaged coordinate-base mass remains in an
explicit finite outer ledger.

The registry deliberately performs no speculative finite-depth extrapolation.
It does not claim that the finite outer is null, that a missing finite R3 count
would make physical R3 empty, or that the observed one-generation ratios are
iterable.  The round-27 arbitrary-n existence/telescope theorem remains the
only limiting statement.  Strong unstable payload is attached only as typed
branch-rule/frontier data; no actual standard-curve instance, numerical q3,
weighted tail, or induced Lasota--Yorke coefficient is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2_cert
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component_cert
import cm2_gate45_round28_q2_homogeneity_recut_cert as homogeneity_cert


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round29-q2-time3-anchor-registry.v1"
MANIFEST_SCHEMA = "cm2.gate34.round29-q2-time3-anchor-registry.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round29-q2-time3-anchor-registry-manifest-2026-07-18.json"
)
PARAMETER_WIDTH = core_cert.S_UPPER - core_cert.S_LOWER

DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate34_round26_q1_time2_frontier_cert.py":
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json":
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d",
    "cm2_gate34_round27_arbitrary_n_path_schema_cert.py":
        "b3071b4af22ad9b4f7941a9896a25cf059e46106c14b1ffb5df0901f90bc3fda",
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json":
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py":
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json":
        "120a3f1cba9f23cc4b2a9753491022f8143175810b19f1a9f9d8ee0214d66b60",
    "cm2_gate45_round28_q2_homogeneity_recut_cert.py":
        "1acf1072caa22b676ed7f579cd2a909f06c6b8249396a7be4cdaa9c37997cf64",
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json":
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3",
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def stream_update(digest: Any, value: Any) -> None:
    digest.update(canonical_json(value).encode())
    digest.update(b"\n")


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value

    schema = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    require(
        schema["verdict"]["arbitrary_n_regular_connected_component_existence_schema"]
        == "CERTIFIED_NONCONSTRUCTIVE",
        "arbitrary-n schema",
    )
    registry = loaded[
        "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
    ]
    require(
        registry["verdict"]["Q2_inner_nonempty_depth2_adaptive_components"]
        == "CERTIFIED_114006",
        "Q2 component anchors",
    )
    require(
        registry["result"]["Q2_nonempty_adaptive_component_registry"]
        ["complete_frozen_Q2_inner_anchor_depth2_key_ownership"] is True,
        "Q2 key ownership",
    )
    homogeneous = loaded[
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    ]
    require(
        homogeneous["verdict"]["Q2_two_step_physical_homogeneity_children"]
        == "CERTIFIED_114006",
        "Q2 homogeneity payload",
    )
    require(
        homogeneous["verdict"]["Q2_actual_curve_recut_instance_ids_materialized"]
        == 0,
        "actual recut frontier",
    )
    return loaded


def atom_from_time2_row(
    row: dict[str, Any],
    parent: dict[str, Any],
    cores: tuple[Any, ...],
) -> Any:
    box = row["source_box"]
    index = row["source_core_index"]
    return time2_cert.step1.Atom(
        index,
        cores[index],
        Q(box["t"][0]), Q(box["t"][1]),
        Q(box["p"][0]), Q(box["p"][1]),
        Q(box["s"][0]), Q(box["s"][1]),
        parent["dyadic_path"] + row["refinement_suffix"],
    )


def second_outgoing_state(
    atom: Any, first_state: dict[str, Any], second_owner: dict[str, Any]
) -> dict[str, Any] | None:
    target = second_owner["selected_target_id"]
    s = first_state["s"]
    normal_x, normal_y, p = (
        second_owner["normal_x"], second_owner["normal_y"], second_owner["p"]
    )
    assert all(isinstance(x, arb) for x in (s, normal_x, normal_y, p))
    radial_square = 1 - p * p
    if not bool(radial_square > 0):
        return None
    chart = time2_cert.strict_chart(normal_x, normal_y)
    if chart is None:
        return None
    radial = radial_square.sqrt()
    center_x, center_y = time2_cert.target_center(target, s)
    radius = time2_cert.step1.arbq(time2_cert.first_hit.RADIUS[target[0]])
    return {
        "contact_x": center_x + radius * normal_x,
        "contact_y": center_y + radius * normal_y,
        "outgoing_x": radial * normal_x - p * normal_y,
        "outgoing_y": radial * normal_y + p * normal_x,
        "s": s,
        "chart": chart,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": p,
    }


def strict_next_owner(
    state: dict[str, Any], current_target: str
) -> tuple[dict[str, Any] | None, str]:
    qx, qy, ux, uy, s = (
        state["contact_x"], state["contact_y"],
        state["outgoing_x"], state["outgoing_y"], state["s"],
    )
    chart = state["chart"]
    assert all(isinstance(x, arb) for x in (qx, qy, ux, uy, s))
    assert isinstance(chart, str)
    rows: list[tuple[str, dict[str, Any]]] = []
    missed = behind = 0
    for candidate_id in time2_cert.translated_candidate_ids(current_target, chart):
        row = time2_cert.candidate_root(qx, qy, ux, uy, s, candidate_id)
        kind = row["classification"]
        if kind == "no_real_intersection":
            missed += 1
        elif kind == "intersection_strictly_behind":
            behind += 1
        elif kind == "strict_future_near_root":
            rows.append((candidate_id, row))
        else:
            return None, f"unresolved_competitor:{kind}"
    winners = [
        (candidate_id, row)
        for candidate_id, row in rows
        if all(
            candidate_id == other_id or bool(row["near"] < other["near"])
            for other_id, other in rows
        )
    ]
    if len(winners) != 1:
        return None, "unresolved_strict_root_order"
    selected_id, selected = winners[0]
    root = selected["near"]
    if not bool(root < time2_cert.step1.arbq(time2_cert.first_hit.TAU_MAX)):
        return None, "selected_root_not_strictly_below_tau_max"
    radical, transverse, radius = (
        selected["radical"], selected["transverse"], selected["radius"]
    )
    assert all(isinstance(x, arb) for x in (root, radical, transverse, radius))
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    p = transverse / radius
    return {
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": p,
        "time2_target_chart_id": f"{current_target[0]}:{chart}",
        "retained_candidate_count": missed + behind + len(rows),
        "missed_candidate_count": missed,
        "behind_candidate_count": behind,
        "strict_future_candidate_count": len(rows),
    }, "strict_unique_third_collision_owner"


def core_classification(
    owner: dict[str, Any], cores: tuple[Any, ...]
) -> tuple[str, str | None, list[dict[str, Any]]]:
    normal_x, normal_y, p = owner["normal_x"], owner["normal_y"], owner["p"]
    assert all(isinstance(x, arb) for x in (normal_x, normal_y, p))
    inside: list[str] = []
    unresolved: list[str] = []
    witnesses: list[dict[str, Any]] = []
    for core in cores:
        if core.source != owner["selected_target_id"][0]:
            continue
        identifier = time2_cert.step1.core_id(core)
        cell = core.chart_id.split(":")[1]
        t, inside_chart, outside_chart = time2_cert.step1.chart_tests(
            cell, normal_x, normal_y
        )
        inside_tests = inside_chart + [
            ("t_gt_t0", bool(t > time2_cert.step1.arbq(core.t0))),
            ("t_lt_t1", bool(t < time2_cert.step1.arbq(core.t1))),
            ("p_gt_p0", bool(p > time2_cert.step1.arbq(core.p0))),
            ("p_lt_p1", bool(p < time2_cert.step1.arbq(core.p1))),
        ]
        if all(value for _name, value in inside_tests):
            inside.append(identifier)
            witnesses.append({"core_id": identifier, "kind": "strict_inside"})
            continue
        separators = outside_chart + [
            ("t_lt_t0", bool(t < time2_cert.step1.arbq(core.t0))),
            ("t_gt_t1", bool(t > time2_cert.step1.arbq(core.t1))),
            ("p_lt_p0", bool(p < time2_cert.step1.arbq(core.p0))),
            ("p_gt_p1", bool(p > time2_cert.step1.arbq(core.p1))),
        ]
        separator = next((name for name, value in separators if value), None)
        if separator is None:
            unresolved.append(identifier)
            witnesses.append({"core_id": identifier, "kind": "unresolved"})
        else:
            witnesses.append({
                "core_id": identifier,
                "kind": "strictly_excluded",
                "first_separator": separator,
            })
    if unresolved or len(inside) > 1:
        return "UNRESOLVED_TIME3_OUTER", None, witnesses
    if len(inside) == 1:
        return "RETURN_AT_3_INNER", inside[0], witnesses
    return "SURVIVE_THROUGH_3_INNER", None, witnesses


def third_word(
    state: dict[str, Any],
    current_target: str,
    owner: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any] | None, str | None]:
    qx, qy, ux, uy = (
        state["contact_x"], state["contact_y"],
        state["outgoing_x"], state["outgoing_y"],
    )
    root = owner["selected_root"]
    assert all(isinstance(x, arb) for x in (qx, qy, ux, uy, root))
    hx, hy = qx + root * ux, qy + root * uy
    x_events, reason = component_cert.ordered_axis_events(qx, hx, "X")
    if x_events is None:
        return None, reason
    y_events, reason = component_cert.ordered_axis_events(qy, hy, "Y")
    if y_events is None:
        return None, reason
    crossings, reason = component_cert.strict_event_order(x_events + y_events)
    if crossings is None:
        return None, reason
    chart = f"{current_target[0]}:{state['chart']}"
    target = component_cert.relative_target(
        current_target, owner["selected_target_id"]
    )
    if target not in time2_cert.first_hit.candidate_ids(chart):
        return None, "relative_target_not_in_frozen_retained_pair"
    key = component_cert.word_key(
        chart, target, crossings, pair_index, pattern_index
    )
    return {
        "key": key,
        "absolute_selected_target_id": owner["selected_target_id"],
        "relative_frozen_target_id": target,
        "ordered_clean_wall_record": list(crossings),
    }, None


def classify_time3(
    atom: Any,
    cores: tuple[Any, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    time2_class, status2, destination2, state1, owner2 = (
        homogeneity_cert.classify_with_geometry(atom, cores)
    )
    require(time2_class == "SURVIVE_THROUGH_2_INNER", "lost Q2 anchor")
    require(destination2 is None and state1 is not None and owner2 is not None,
            "Q2 geometry")
    state2 = second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        return {
            "classification": "UNRESOLVED_TIME3_OUTER",
            "blocker": "unresolved_time2_outgoing_chart_or_geometry",
            "state1": state1,
            "owner2": owner2,
        }
    owner3, status3 = strict_next_owner(state2, owner2["selected_target_id"])
    if owner3 is None:
        return {
            "classification": "UNRESOLVED_TIME3_OUTER",
            "blocker": status3,
            "state1": state1,
            "owner2": owner2,
            "state2": state2,
        }
    word3, word_blocker = third_word(
        state2, owner2["selected_target_id"], owner3,
        pair_index, pattern_index,
    )
    if word3 is None:
        return {
            "classification": "UNRESOLVED_TIME3_OUTER",
            "blocker": f"third_clean_wall_word:{word_blocker}",
            "state1": state1,
            "owner2": owner2,
            "state2": state2,
            "owner3": owner3,
        }
    classification, destination, core_witnesses = core_classification(owner3, cores)
    return {
        "classification": classification,
        "blocker": None if classification != "UNRESOLVED_TIME3_OUTER"
        else "third_core_membership_not_whole_box_strict",
        "destination_core_id": destination,
        "state1": state1,
        "owner2": owner2,
        "state2": state2,
        "owner3": owner3,
        "word3": word3,
        "core_witnesses": core_witnesses,
        "status2": status2,
        "status3": status3,
    }


def public_arb_dict(value: dict[str, Any], omit: set[str] | None = None) -> dict[str, Any]:
    blocked = set() if omit is None else omit
    return {
        key: (str(item) if isinstance(item, arb) else item)
        for key, item in value.items() if key not in blocked
    }


def admitted_payload(
    row: dict[str, Any], atom: Any, geometry: dict[str, Any],
    q2_payload: dict[str, Any], first_key: dict[str, Any],
    second_key: dict[str, Any],
) -> dict[str, Any]:
    owner3 = geometry["owner3"]
    word3 = geometry["word3"]
    p3 = owner3["p"]
    assert isinstance(p3, arb)
    h3_ok = homogeneity_cert.central_homogeneity(p3)
    key_ids = [
        first_key["word_key_id"], second_key["word_key_id"],
        word3["key"]["word_key_id"],
    ]
    identity = {
        "schema": "c24-finite-open-time3-component-cell.v1",
        "time2_atom_id": row["time2_atom_id"],
        "source_box": component_cert.box_payload(atom),
        "classification": geometry["classification"],
        "destination_core_id": geometry.get("destination_core_id"),
        "frozen_path_prefix_word_key_ids": key_ids,
    }
    atom3_id = "full-core-time3:" + canonical_digest(identity)
    h3_payload = {
        "time3_atom_id": atom3_id,
        "collision_step": 3,
        "parent_two_step_homogeneous_child_id":
            q2_payload["two_step_homogeneous_child_id"],
        "owner_target_id": owner3["selected_target_id"],
        "homogeneity_label": f"central H_0(k0={homogeneity_cert.K0})",
        "target_cosine_strict_lower": qstr(
            homogeneity_cert.CENTRAL_COSINE_LOWER
        ),
        "whole_box_strict": h3_ok,
    }
    h3_id = None if not h3_ok else "h:q3:step3:" + canonical_digest(h3_payload)
    restriction_payload = {
        "time3_atom_id": atom3_id,
        "parent_Q2_restriction_id": q2_payload["restriction_id"],
        "depth3_word_key_id": key_ids[-1],
        "third_owner_target_id": owner3["selected_target_id"],
        "source_box": identity["source_box"],
    }
    restriction_id = "restriction:q3:" + canonical_digest(restriction_payload)
    recut_id = None
    f5_id = f6_id = None
    if h3_ok:
        recut_payload = {
            "time3_atom_id": atom3_id,
            "stage": "before_collision_3",
            "parent_Q2_recut_branch_rule_ids":
                q2_payload["canonical_recut_branch_rule_ids"],
            "physical_homogeneity_child_id": h3_id,
            "canonical_recut_rule":
                "split by adapted arclength at deterministic multiples of 1e-90",
            "actual_curve_instance_materialized": False,
        }
        recut_id = "recut-rule:q3:step2:" + canonical_digest(recut_payload)
        f5_id = "slot:q3:f5:" + canonical_digest({
            "time3_atom_id": atom3_id,
            "restriction_id": restriction_id,
            "recut_rule_id": recut_id,
            "three_step_inverse_upper": qstr(homogeneity_cert.THETA ** 3),
            "scope": "universal branch-rule slot not actual curve instance",
        })
        f6_id = "slot:q3:f6:" + canonical_digest({
            "time3_atom_id": atom3_id,
            "restriction_id": restriction_id,
            "recut_rule_id": recut_id,
            "three_step_log_variation_upper": qstr(
                3 * homogeneity_cert.ONE_STEP_LOG_VARIATION
            ),
            "scope": "universal branch-rule slot not actual curve instance",
        })
    mass = component_cert.exact_mass_payload(atom)
    return {
        "time3_atom_id": atom3_id,
        **identity,
        "time3_component_id": "c24-time3-component:" + canonical_digest(identity),
        "frozen_path_prefix_key_ordinals_zero_based": [
            first_key["ordinal_zero_based"], second_key["ordinal_zero_based"],
            word3["key"]["ordinal_zero_based"],
        ],
        "path_prefix_owner_id": "c24-prefix-owner:" + canonical_digest(key_ids),
        "third_word_absolute_selected_target_id":
            word3["absolute_selected_target_id"],
        "third_word_relative_frozen_target_id":
            word3["relative_frozen_target_id"],
        "third_word_ordered_clean_wall_record":
            word3["ordered_clean_wall_record"],
        **mass,
        "parent_Q2_restriction_id": q2_payload["restriction_id"],
        "common_forward_reverse_time3_restriction_id": restriction_id,
        "restriction_is_same_Borel_carrier_in_forward_and_reverse_views": True,
        "restriction_is_smooth_and_invertible_on_each_regular_fixed_s_slice": True,
        "three_collision_invariant_area_Jacobian": "1",
        "invariant_area_Jacobian_is_not_unstable_Jacobian": True,
        "time3_physical_homogeneity_child_id": h3_id,
        "time3_canonical_recut_branch_rule_id": recut_id,
        "actual_curve_recut_instance_id_count": 0,
        "F5_three_step_universal_branch_rule_slot_id": f5_id,
        "F5_three_step_adapted_inverse_strict_upper": (
            qstr(homogeneity_cert.THETA ** 3) if h3_ok else None
        ),
        "F6_three_step_universal_branch_rule_slot_id": f6_id,
        "F6_three_step_log_variation_strict_upper": (
            qstr(3 * homogeneity_cert.ONE_STEP_LOG_VARIATION)
            if h3_ok else None
        ),
        "symbolic_once_charged_q3_formula": (
            "(1+C_fw)*(1+C_rev)*(144000/180337)^3"
        ),
        "numeric_C_fw": None,
        "numeric_C_rev": None,
        "numeric_strong_q3": None,
        "positive_finite_open_rectangle_for_every_s_strictly_inside_cell": True,
        "maximal_physical_path_component_claimed": False,
        "geometry_witness_sha256": canonical_digest({
            "owner2": public_arb_dict(geometry["owner2"]),
            "owner3": public_arb_dict(geometry["owner3"]),
            "core_witnesses": geometry["core_witnesses"],
        }),
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    pair_index, pattern_index, alphabet_digest = component_cert.key_index_tables()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "physical core count")
    step1_manifest = time2_cert.load_step1_manifest()
    q1_rows = [
        row for row in step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    q1_rows.sort(key=lambda row: row["atom_id"])
    require(len(q1_rows) == 2868, "Q1 parent count")
    q1_by_id = {row["atom_id"]: row for row in q1_rows}
    rows2 = time2_cert.adaptive_time2_rows(q1_rows, cores)
    time2_cert.verify_prefix_and_mass(q1_rows, rows2)
    require(len(rows2) == 416994, "time2 replay leaf count")
    q2_rows = [
        row for row in rows2
        if row["classification"] == "SURVIVE_THROUGH_2_INNER"
    ]
    require(len(q2_rows) == 114006, "Q2 anchor count")
    prior_template_id = homogeneity_cert.round27_cert.strong_template()[
        "conditional_template_id"
    ]

    classification_histogram: Counter[str] = Counter()
    blocker_histogram: Counter[str] = Counter()
    owner_target_histogram: Counter[str] = Counter()
    prefix_histogram: Counter[str] = Counter()
    homogeneity_histogram: Counter[str] = Counter()
    mass_by_kind: Counter[str] = Counter()
    admitted_digest = hashlib.sha256()
    outer_digest = hashlib.sha256()
    admitted_ids: set[str] = set()
    component_ids: set[str] = set()
    restriction_ids: set[str] = set()
    recut_rule_ids: set[str] = set()
    f5_ids: set[str] = set()
    f6_ids: set[str] = set()
    representatives: dict[str, dict[str, Any]] = {}
    outer_representatives: list[dict[str, Any]] = []

    for row in q2_rows:
        parent = q1_by_id[row["Q1_parent_atom_id"]]
        atom = atom_from_time2_row(row, parent, cores)
        geometry = classify_time3(atom, cores, pair_index, pattern_index)
        kind = geometry["classification"]
        classification_histogram[kind] += 1
        mass = time2_cert.step1.base_mass(atom)
        require(mass == Q(row["parameter_averaged_unnormalized_base_mass"]),
                "Q2 row mass")
        mass_by_kind[kind] += mass
        if kind == "UNRESOLVED_TIME3_OUTER":
            blocker = str(geometry["blocker"])
            blocker_histogram[blocker] += 1
            outer = {
                "time2_atom_id": row["time2_atom_id"],
                "source_box": component_cert.box_payload(atom),
                "parameter_averaged_coordinate_base_mass_exact": qstr(mass),
                "first_blocker": blocker,
                "finite_outer_promoted_to_collision_null": False,
            }
            stream_update(outer_digest, outer)
            if len(outer_representatives) < 3:
                outer_representatives.append(outer)
            continue

        first_key = component_cert.word_key(
            atom.source_core.chart_id, atom.source_core.target_id,
            tuple(atom.source_core.crossings), pair_index, pattern_index,
        )
        second, reason = component_cert.second_word_for_atom(
            atom, row["selected_second_target_id"], pair_index, pattern_index
        )
        require(second is not None and reason is None, "Q2 second word replay")
        assert second is not None
        q2_payload, payload_blocker, _audit = homogeneity_cert.materialized_payload(
            row, atom, geometry["state1"], geometry["owner2"],
            cores, prior_template_id,
        )
        require(q2_payload is not None and payload_blocker is None,
                "Q2 payload replay")
        assert q2_payload is not None
        payload = admitted_payload(
            row, atom, geometry, q2_payload, first_key, second["key"]
        )
        require(payload["time3_atom_id"] not in admitted_ids, "time3 atom ID")
        require(payload["time3_component_id"] not in component_ids,
                "time3 component ID")
        admitted_ids.add(payload["time3_atom_id"])
        component_ids.add(payload["time3_component_id"])
        restriction_ids.add(payload["common_forward_reverse_time3_restriction_id"])
        if payload["time3_physical_homogeneity_child_id"] is None:
            homogeneity_histogram["third_H0_not_whole_box_strict"] += 1
        else:
            homogeneity_histogram["third_H0_whole_box_strict"] += 1
            recut_rule_ids.add(payload["time3_canonical_recut_branch_rule_id"])
            f5_ids.add(payload["F5_three_step_universal_branch_rule_slot_id"])
            f6_ids.add(payload["F6_three_step_universal_branch_rule_slot_id"])
        owner_target_histogram[payload["third_word_absolute_selected_target_id"]] += 1
        prefix_histogram[",".join(
            str(x) for x in payload["frozen_path_prefix_key_ordinals_zero_based"]
        )] += 1
        stream_update(admitted_digest, payload)
        representatives.setdefault(kind, payload)

    total_mass = sum(mass_by_kind.values(), Q(0))
    require(total_mass == Q(5257799, 5120000000), "Q2 anchor mass conservation")
    admitted_count = (
        classification_histogram["RETURN_AT_3_INNER"]
        + classification_histogram["SURVIVE_THROUGH_3_INNER"]
    )
    require(admitted_count == len(admitted_ids) == len(component_ids),
            "admitted counts")
    require(len(restriction_ids) == admitted_count, "restriction IDs")
    strict_h3 = homogeneity_histogram["third_H0_whole_box_strict"]
    require(len(recut_rule_ids) == len(f5_ids) == len(f6_ids) == strict_h3,
            "third homogeneity payload IDs")
    require(classification_histogram["SURVIVE_THROUGH_3_INNER"] > 0,
            "nonempty Q3 subregistry")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "admission_engine": "python-flint Arb",
            "precision_bits": 384,
            "full_Q2_anchor_replay": True,
            "frozen_Q2_anchor_count": len(q2_rows),
            "frozen_word_alphabet_rows_sha256": alphabet_digest,
            "clock": "source core time0; Q2 avoids times1,2; classify time3",
        },
        "time3_finite_root_registry_contract": {
            "source": "all 114006 certified finite-open Q2-inner anchor boxes",
            "adaptive_extra_depth": 0,
            "admission": (
                "strict third owner, strict clean-wall word, strict core membership "
                "or exclusion on the entire source box"
            ),
            "registered_component_scope": (
                "connected component cell of this finite-open root-box registry"
            ),
            "maximal_component_of_full_physical_path_fibre": False,
            "finite_outer_is_collision_null": False,
            "finite_admitted_zero_would_imply_physical_R3_empty": False,
            "observed_ratios_are_uniform_or_iterable": False,
        },
        "Q2_to_time3_whole_box_registry": {
            "Q2_anchor_count": len(q2_rows),
            "time3_terminal_root_box_count": len(q2_rows),
            "classification_histogram": {
                key: classification_histogram[key]
                for key in (
                    "RETURN_AT_3_INNER",
                    "SURVIVE_THROUGH_3_INNER",
                    "UNRESOLVED_TIME3_OUTER",
                )
            },
            "first_blocker_histogram": dict(sorted(blocker_histogram.items())),
            "materialized_R3_inner_component_count":
                classification_histogram["RETURN_AT_3_INNER"],
            "materialized_Q3_inner_component_count":
                classification_histogram["SURVIVE_THROUGH_3_INNER"],
            "materialized_admitted_component_count": admitted_count,
            "admitted_rows_sha256": admitted_digest.hexdigest(),
            "admitted_time3_atom_ids_sha256": canonical_digest(sorted(admitted_ids)),
            "admitted_component_ids_sha256": canonical_digest(sorted(component_ids)),
            "finite_outer_rows_sha256": outer_digest.hexdigest(),
            "distinct_depth3_word_prefix_count": len(prefix_histogram),
            "depth3_word_prefix_histogram_sha256": canonical_digest(
                dict(sorted(prefix_histogram.items()))
            ),
            "third_owner_target_histogram_sha256": canonical_digest(
                dict(sorted(owner_target_histogram.items()))
            ),
            "parameter_averaged_coordinate_base_mass_by_class": {
                key: qstr(mass_by_kind[key])
                for key in (
                    "RETURN_AT_3_INNER",
                    "SURVIVE_THROUGH_3_INNER",
                    "UNRESOLVED_TIME3_OUTER",
                )
            },
            "parameter_averaged_total_Q2_anchor_mass_exact": qstr(total_mass),
            "R3_plus_Q3_plus_finite_outer_mass_equals_Q2_anchor_mass": True,
            "every_R3_cell_is_first_return_at_exact_collision_time3": True,
            "every_Q3_cell_avoids_C24_at_collision_times1_2_3": True,
            "representative_admitted_rows": [
                representatives[key] for key in sorted(representatives)
            ],
            "representative_finite_outer_rows": outer_representatives,
        },
        "time3_typed_payload_frontier": {
            "common_forward_reverse_restriction_id_count": len(restriction_ids),
            "third_H0_histogram": dict(sorted(homogeneity_histogram.items())),
            "time3_homogeneity_child_id_count": strict_h3,
            "time3_canonical_recut_branch_rule_id_count": len(recut_rule_ids),
            "actual_curve_recut_instance_id_count": 0,
            "F5_three_step_universal_branch_rule_slot_count": len(f5_ids),
            "F5_three_step_inverse_strict_upper": qstr(
                homogeneity_cert.THETA ** 3
            ),
            "F6_three_step_universal_branch_rule_slot_count": len(f6_ids),
            "F6_three_step_log_variation_strict_upper": qstr(
                3 * homogeneity_cert.ONE_STEP_LOG_VARIATION
            ),
            "invariant_area_Jacobian_value_on_every_admitted_branch": "1",
            "invariant_area_Jacobian_is_unstable_Jacobian": False,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_strong_q3_count": 0,
            "charged_characteristic_Z_F7_count": 0,
        },
        "arbitrary_n_and_limiting_frontier": {
            "round27_arbitrary_n_regular_component_existence_schema":
                "CERTIFIED_NONCONSTRUCTIVE_DEPENDENCY",
            "complete_limiting_physical_R3_Q3_partition_mod_collision_null":
                "CERTIFIED_NONCONSTRUCTIVE_DEPENDENCY",
            "complete_limiting_R3_Q3_component_enumeration": "NOT_CERTIFIED",
            "uniform_adaptive_time3_termination_rate": "NOT_CERTIFIED",
            "arbitrary_n_numeric_singularity_growth": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "finite_outer_promoted_to_null": False,
            "finite_histogram_extrapolated_to_tail": False,
            "actual_standard_curve_recut_instances": "NOT_CERTIFIED",
            "numeric_unstable_Jacobian_beyond_universal_branch_rule_slot":
                "NOT_CERTIFIED",
            "numeric_strong_q3": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    registry = result["Q2_to_time3_whole_box_registry"]
    payload = result["time3_typed_payload_frontier"]
    return {
        "all_finite_Q2_anchors_fresh_time3_root_replay": "CERTIFIED_114006",
        "finite_R3_inner_components":
            f"CERTIFIED_{registry['materialized_R3_inner_component_count']}",
        "finite_Q3_inner_components":
            f"CERTIFIED_{registry['materialized_Q3_inner_component_count']}",
        "finite_Q2_anchor_time3_mass_conservation": "CERTIFIED",
        "time3_common_forward_reverse_restriction_ids":
            f"CERTIFIED_{payload['common_forward_reverse_restriction_id_count']}",
        "time3_F5_F6_universal_branch_rule_slots": (
            f"CERTIFIED_{payload['F5_three_step_universal_branch_rule_slot_count']}"
        ),
        "complete_limiting_R3_Q3_component_enumeration": "NOT_CERTIFIED",
        "uniform_adaptive_time3_termination_rate": "NOT_CERTIFIED",
        "strong_q_weighted_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier", type=Path,
        default=HERE / "cm2_gate34_round29_q2_time3_anchor_registry_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    registry = result["Q2_to_time3_whole_box_registry"]
    print("Q2_TIME3_ROOT_REPLAY: CERTIFIED_114006")
    print(f"R3_COMPONENTS: {registry['materialized_R3_inner_component_count']}")
    print(f"Q3_COMPONENTS: {registry['materialized_Q3_inner_component_count']}")
    print("COMPLETE_LIMITING_R3_Q3_ENUMERATION: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
