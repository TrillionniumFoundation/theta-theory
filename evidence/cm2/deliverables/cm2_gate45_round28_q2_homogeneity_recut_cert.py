#!/usr/bin/env python3
"""Round-28 physical homogeneity and canonical-recut payload on strict Q2 atoms.

This append-only leaf reruns the frozen round-26 time-two adaptive recursion at
384-bit Arb precision.  On every terminal strict Q2-inner box it checks the
two physical collision owners, the enlarged central homogeneity strip with
cutoff k0=6121, and the target normal-chart seams.  A deterministic chart-free
physical canonical-recut branch-rule contract is then attached before each
collision.  The frozen universal unstable estimates become one numerical
candidate-local F5 universal branch-rule slot and one numerical candidate-local
F6 universal branch-rule slot on every two-step homogeneous child.  No actual
standard-curve recut-instance ID is materialized.  Target normal-chart seams are separately audited:
they are representation boundaries, not physical F5/F6 cuts, but an atom that
does not strictly exclude one receives no full-chart F4 promotion.

The producer is deliberately fail closed.  If a Q2 box fails to isolate a
physical homogeneity rank, it is retained in the blocked ledger and receives
no F5/F6 branch-rule slot.  Collision-area mass, coordinate-base mass, invariant area Jacobian,
adaptive-coordinate Jacobian and unstable one-dimensional Jacobian remain
strongly typed and are never identified.  F7 and F14--F18, numerical strong
q2, weighted tails, induced Lasota--Yorke coefficients and Gate 4/5 remain
uncertified.
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
import cm2_gate4_componentwise_global_growth_recovery_frontier_cert as componentwise_cert
import cm2_gate45_round27_q2_branch_payload_frontier_cert as round27_cert


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

RESULT_SCHEMA = "cm2.gate45.round28-q2-homogeneity-recut.v1"
MANIFEST_SCHEMA = "cm2.gate45.round28-q2-homogeneity-recut.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2_gate45_round27_q2_branch_payload_frontier_cert.py": (
        "be96ada6c90e792b7abe556982c65b78dae051498b680ebad3267117f44078c9"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py": (
        "90b7f7a9c0f02c19a80a9679ff393818318675c378ff4c1f139985ae23f069e1"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

K0 = 6121
CENTRAL_COSINE_LOWER = Q(1, 2 * K0 * K0)
CENTRAL_COSINE_SQUARE_LOWER = CENTRAL_COSINE_LOWER**2
THETA = Q(144000, 180337)
TWO_STEP_THETA = THETA**2
ONE_STEP_LOG_VARIATION = Q(3, 200000)
TWO_STEP_LOG_VARIATION = 2 * ONE_STEP_LOG_VARIATION
CANONICAL_ADAPTED_LENGTH = "1e-90"
FIELDS = (
    "nonempty_or_empty_domain_proof",
    "physical_homogeneity_subbranch_table",
    "homogeneous_prefix_chart",
    "homogeneous_suffix_chart",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
    "one_step_cut_growth_Z_sum",
    "face_transversality_lower",
    "face_C2_atlas_bound",
    "coarea_density_regular_bound",
    "dynamic_Holder_test_pullback_bound",
    "C1_face_trace_pullback_bound",
    "moving_boundary_DQ_current_and_two_traces",
    "regular_density_operator_cost",
    "standard_family_operator_cost",
    "flux_face_operator_cost",
    "dynamic_test_operator_cost",
    "operator_phase_block",
)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


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
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency JSON type: {name}")
            loaded[name] = value

    prior = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]
    require(prior["verdict"]["Q2_exact_mass_slots"] == "CERTIFIED_114006", "prior mass")
    require(prior["verdict"]["Q2_F5_F6"] == "NOT_CERTIFIED", "prior F5/F6")
    template = prior["result"]["Q2_conditional_unstable_payload_template"]
    require(template["F5_materialized_slot_count"] == 0, "prior F5 zero")
    require(template["F6_materialized_slot_count"] == 0, "prior F6 zero")
    require(
        template["required_missing_row_fields"]
        == [
            "time1_physical_homogeneity_child_id",
            "time2_physical_homogeneity_child_id",
            "canonical_recut_component_ids",
        ],
        "prior missing fields",
    )

    time2 = loaded[
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    ]["result"]
    registry = time2["Q1_time2_adaptive_registry"]
    require(registry["time2_leaf_count"] == 416994, "time2 leaf count")
    require(registry["strict_Q2_inner_atom_count"] == 114006, "Q2 count")
    require(registry["strict_R2_inner_atom_count"] == 0, "finite R2 count")
    require(time2["Q1_time2_mass_frontier"]["Q2_inner_base_mass"] == "5257799/5120000000", "Q2 mass")

    growth_summary = loaded[
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    ]["replay_summary"]
    incidence = componentwise_cert.short_curve_central_incidence_theorem()
    require(growth_summary["homogeneity_cutoff_k0"] == K0, "manifest k0")
    require(incidence["homogeneity_cutoff_k0"] == K0, "k0")
    require(incidence["central_cosine_strict_lower"] == qstr(CENTRAL_COSINE_LOWER), "central cosine")
    require(incidence["chart_seams_are_not_physical_cuts"] is True, "chart seam typing")

    universal = loaded[
        "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json"
    ]["result"]["universal_full_collision_branch_templates"]
    require(universal["canonical_adapted_length_upper"] == CANONICAL_ADAPTED_LENGTH, "canonical length")
    require(
        universal["field_5_inverse_Jacobian_seed"]["physical_type"]
        == "adapted unstable one-dimensional Jacobian",
        "F5 type",
    )
    require(
        universal["field_5_inverse_Jacobian_seed"]["universal_adapted_inverse_strict_upper"]
        == qstr(THETA),
        "F5 bound",
    )
    require(
        universal["field_6_log_Jacobian_distortion_seed"]["canonical_curve_log_variation_strict_upper"]
        == qstr(ONE_STEP_LOG_VARIATION),
        "F6 bound",
    )

    adaptive = loaded[
        "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
    ]["result"]["fixed_s_adaptive_face_theorem"]
    require(adaptive["intersection_with_one_atom"] == "empty_or_one_interval", "atom interval")
    require(adaptive["canonical_curve_contract"].startswith("t(r) monotone"), "canonical graph")

    schema = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["required_operator_field_schema"]
    require(tuple(schema["required_fields"]) == FIELDS, "18-field schema")
    return loaded


def owner_from_outgoing(
    atom: Any, state: dict[str, arb | str]
) -> tuple[dict[str, Any] | None, str]:
    """Frozen round-26 second-owner test, with the time-one state retained."""

    qx, qy = state["contact_x"], state["contact_y"]
    ux, uy, s, chart = (
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
        state["chart"],
    )
    assert isinstance(qx, arb) and isinstance(qy, arb)
    assert isinstance(ux, arb) and isinstance(uy, arb) and isinstance(s, arb)
    assert isinstance(chart, str)
    rows: list[tuple[str, dict[str, Any]]] = []
    missed = 0
    behind = 0
    for candidate_id in time2_cert.translated_candidate_ids(
        atom.source_core.target_id, chart
    ):
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
    winners: list[tuple[str, dict[str, Any]]] = []
    for candidate_id, row in rows:
        near = row["near"]
        assert isinstance(near, arb)
        if all(
            candidate_id == other_id or bool(near < other["near"])
            for other_id, other in rows
        ):
            winners.append((candidate_id, row))
    if len(winners) != 1:
        return None, "unresolved_strict_root_order"
    selected_id, selected = winners[0]
    root = selected["near"]
    if not bool(root < time2_cert.step1.arbq(time2_cert.first_hit.TAU_MAX)):
        return None, "selected_root_not_strictly_below_tau_max"
    radical, transverse, radius = (
        selected["radical"],
        selected["transverse"],
        selected["radius"],
    )
    assert all(isinstance(value, arb) for value in (root, radical, transverse, radius))
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    p = transverse / radius
    return {
        "time1_chart_id": f"{atom.source_core.target_id[0]}:{chart}",
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": p,
        "retained_candidate_count": missed + behind + len(rows),
        "missed_candidate_count": missed,
        "behind_candidate_count": behind,
        "strict_future_candidate_count": len(rows),
    }, "strict_unique_second_collision_owner"


def classify_with_geometry(
    atom: Any, cores: tuple[Any, ...]
) -> tuple[str, str, str | None, dict[str, Any] | None, dict[str, Any] | None]:
    """Recompute the round-26 class while returning both collision states."""

    state = time2_cert.first_collision_outgoing(atom)
    if state is None:
        return (
            "UNRESOLVED_TIME2_OUTER",
            "unresolved_time1_outgoing_chart_or_geometry",
            None,
            None,
            None,
        )
    owner, status = owner_from_outgoing(atom, state)
    if owner is None:
        return "UNRESOLVED_TIME2_OUTER", status, None, state, None

    normal_x, normal_y, p = owner["normal_x"], owner["normal_y"], owner["p"]
    assert isinstance(normal_x, arb) and isinstance(normal_y, arb) and isinstance(p, arb)
    inside: list[str] = []
    unresolved: list[str] = []
    for destination in cores:
        if destination.source != owner["selected_target_id"][0]:
            continue
        identifier = time2_cert.step1.core_id(destination)
        cell = destination.chart_id.split(":")[1]
        t, inside_chart_tests, outside_chart_tests = time2_cert.step1.chart_tests(
            cell, normal_x, normal_y
        )
        inside_tests = inside_chart_tests + [
            ("t_gt_t0", bool(t > time2_cert.step1.arbq(destination.t0))),
            ("t_lt_t1", bool(t < time2_cert.step1.arbq(destination.t1))),
            ("p_gt_p0", bool(p > time2_cert.step1.arbq(destination.p0))),
            ("p_lt_p1", bool(p < time2_cert.step1.arbq(destination.p1))),
        ]
        if all(value for _name, value in inside_tests):
            inside.append(identifier)
            continue
        separators = outside_chart_tests + [
            ("t_lt_t0", bool(t < time2_cert.step1.arbq(destination.t0))),
            ("t_gt_t1", bool(t > time2_cert.step1.arbq(destination.t1))),
            ("p_lt_p0", bool(p < time2_cert.step1.arbq(destination.p0))),
            ("p_gt_p1", bool(p > time2_cert.step1.arbq(destination.p1))),
        ]
        if not any(value for _name, value in separators):
            unresolved.append(identifier)
    if unresolved or len(inside) > 1:
        classification = "UNRESOLVED_TIME2_OUTER"
        destination_id = None
    elif len(inside) == 1:
        classification = "RETURN_AT_2_INNER"
        destination_id = inside[0]
    else:
        classification = "SURVIVE_THROUGH_2_INNER"
        destination_id = None
    return classification, status, destination_id, state, owner


def compact_terminal_row(
    parent: dict[str, Any], atom: Any, classification: str, status: str,
    destination_id: str | None, selected_target_id: str | None,
) -> dict[str, Any]:
    suffix = atom.path[len(parent["dyadic_path"]):]
    box = {
        "t": [str(atom.t0), str(atom.t1)],
        "p": [str(atom.p0), str(atom.p1)],
        "s": [str(atom.s0), str(atom.s1)],
    }
    identity = {
        "Q1_parent_atom_id": parent["atom_id"],
        "refinement_suffix": suffix,
        "source_box": box,
    }
    return {
        "time2_atom_id": "full-core-time2:" + canonical_digest(identity),
        **identity,
        "source_core_index": atom.source_core_index,
        "total_depth": atom.depth,
        "classification": classification,
        "owner_status": status,
        "selected_second_target_id": selected_target_id,
        "destination_core_id": destination_id,
        "parameter_averaged_unnormalized_base_mass": str(
            time2_cert.step1.base_mass(atom)
        ),
        "canonical_invariant_area_Jacobian_per_regular_collision": "1",
    }


def central_homogeneity(p: arb) -> bool:
    radial_square = 1 - p * p
    threshold = time2_cert.step1.arbq(CENTRAL_COSINE_SQUARE_LOWER)
    return bool(radial_square > threshold)


def materialized_payload(
    row: dict[str, Any], atom: Any, state: dict[str, Any], owner: dict[str, Any],
    cores: tuple[Any, ...], prior_template_id: str,
) -> tuple[dict[str, Any] | None, str | None, dict[str, Any]]:
    """Return a typed F5/F6 payload or the first exact blocker."""

    p1, p2 = state["p"], owner["p"]
    assert isinstance(p1, arb) and isinstance(p2, arb)
    chart1 = state["chart"]
    assert isinstance(chart1, str)
    chart2 = time2_cert.strict_chart(owner["normal_x"], owner["normal_y"])
    audit = {
        "time1_owner": atom.source_core.target_id,
        "time2_owner": owner["selected_target_id"],
        "time1_target_chart": f"{atom.source_core.target_id[0]}:{chart1}",
        "time2_target_chart": (
            None if chart2 is None else f"{owner['selected_target_id'][0]}:{chart2}"
        ),
        "time1_central_H0_k0_6121": central_homogeneity(p1),
        "time2_central_H0_k0_6121": central_homogeneity(p2),
        "Arb_geometry_witness_sha256": canonical_digest({
            "p1": str(p1),
            "p2": str(p2),
            "time1_normal_x": str(state["normal_x"]),
            "time1_normal_y": str(state["normal_y"]),
            "time2_normal_x": str(owner["normal_x"]),
            "time2_normal_y": str(owner["normal_y"]),
            "time1_root": str(state["root"]),
            "time2_root": str(owner["selected_root"]),
        }),
    }
    if not audit["time1_central_H0_k0_6121"]:
        return None, "time1_homogeneity_rank_not_whole_box_isolated", audit
    if not audit["time2_central_H0_k0_6121"]:
        return None, "time2_homogeneity_rank_not_whole_box_isolated", audit
    prior = round27_cert.branch_payload_row(row, cores, prior_template_id)
    require(prior["two_collision_invariant_area_Jacobian"] == "1", "prior area")
    require(prior["time1_homogeneity_child_id"] is None, "prior h1")
    require(prior["time2_homogeneity_child_id"] is None, "prior h2")
    core = cores[row["source_core_index"]]
    source_core_id = time2_cert.step1.core_id(core)
    chart1_id = audit["time1_target_chart"]
    chart2_id = audit["time2_target_chart"]

    h1_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "collision_step": 1,
        "source_core_id": source_core_id,
        "owner_target_id": core.target_id,
        "physical_source_section": core.source,
        "physical_target_section": core.target_id[0],
        "homogeneity_label": f"central H_0(k0={K0})",
        "target_cosine_strict_lower": qstr(CENTRAL_COSINE_LOWER),
        "whole_box_strict": True,
    }
    h1_id = "h:q2:step1:" + canonical_digest(h1_payload)
    h2_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "collision_step": 2,
        "parent_homogeneity_child_id": h1_id,
        "owner_target_id": owner["selected_target_id"],
        "physical_source_section": core.target_id[0],
        "physical_target_section": owner["selected_target_id"][0],
        "homogeneity_label": f"central H_0(k0={K0})",
        "target_cosine_strict_lower": qstr(CENTRAL_COSINE_LOWER),
        "whole_box_strict": True,
    }
    h2_id = "h:q2:step2:" + canonical_digest(h2_payload)

    recut0_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "stage": "before_collision_1",
        "physical_homogeneity_child_id": h1_id,
        "full_dimensional_branch": "owned connected adaptive source box on one physical owner/H0 branch",
        "canonical_curve_intersection": "empty_or_one_interval",
        "canonical_adapted_arclength_upper": CANONICAL_ADAPTED_LENGTH,
        "instance_id_schema": "recut-instance:(component-id):(canonical-parent-W-id):natural-index-j",
        "endpoint_ownership": "adapted-arclength half-open cells; last endpoint closed",
    }
    recut0_id = "recut-rule:q2:step0:" + canonical_digest(recut0_payload)
    recut1_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "stage": "before_collision_2",
        "parent_recut_branch_rule_id": recut0_id,
        "physical_homogeneity_child_id": h2_id,
        "full_dimensional_branch": "connected step1 image on one smooth physical owner/H0 branch",
        "normal_chart_seam_role": "representation seam; not a physical cut and not used by F5/F6",
        "canonical_recut_rule": "split by adapted arclength at deterministic multiples of 1e-90",
        "canonical_adapted_arclength_upper": CANONICAL_ADAPTED_LENGTH,
        "instance_id_schema": "recut-instance:(component-id):(image-parent-W-id):natural-index-j",
        "endpoint_ownership": "adapted-arclength half-open cells; last endpoint closed",
    }
    recut1_id = "recut-rule:q2:step1:" + canonical_digest(recut1_payload)
    two_step_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "time1_physical_homogeneity_child_id": h1_id,
        "time2_physical_homogeneity_child_id": h2_id,
        "canonical_recut_branch_rule_ids": [recut0_id, recut1_id],
        "restriction_id": prior["restriction_id"],
    }
    child_id = "child:q2:two-step:" + canonical_digest(two_step_payload)

    f5_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "two_step_homogeneous_child_id": child_id,
        "restriction_id": prior["restriction_id"],
        "canonical_recut_branch_rule_ids": [recut0_id, recut1_id],
        "physical_type": "adapted unstable one-dimensional Jacobian",
        "one_step_inverse_strict_uppers": [qstr(THETA), qstr(THETA)],
        "two_step_inverse_strict_upper": qstr(TWO_STEP_THETA),
        "composition": "pointwise product on every actual two-step curve instance generated by the branch rules",
        "slot_scope": "one universal branch-rule slot; not an actual curve-instance count",
        "invariant_area_Jacobian_slot_used": False,
        "adaptive_t_p_coordinate_Jacobian_used": False,
    }
    f5_id = "slot:q2:f5:" + canonical_digest(f5_payload)
    f6_payload = {
        "time2_atom_id": row["time2_atom_id"],
        "two_step_homogeneous_child_id": child_id,
        "restriction_id": prior["restriction_id"],
        "canonical_recut_branch_rule_ids": [recut0_id, recut1_id],
        "physical_type": "leafwise log-distortion of adapted unstable one-dimensional Jacobian",
        "one_step_log_variation_strict_uppers": [
            qstr(ONE_STEP_LOG_VARIATION), qstr(ONE_STEP_LOG_VARIATION)
        ],
        "two_step_log_variation_strict_upper": qstr(TWO_STEP_LOG_VARIATION),
        "composition": "sum on every pair retained in one actual two-step curve instance generated by the branch rules",
        "slot_scope": "one universal branch-rule slot; not an actual curve-instance count",
        "invariant_area_log_distortion_used": False,
        "adaptive_t_p_coordinate_log_distortion_used": False,
    }
    f6_id = "slot:q2:f6:" + canonical_digest(f6_payload)
    payload = {
        "time2_atom_id": row["time2_atom_id"],
        "source_core_id": source_core_id,
        "restriction_id": prior["restriction_id"],
        "mass_slot_id": prior["mass_slot_id"],
        "area_Jacobian_slot_id": prior["area_Jacobian_slot_id"],
        "time1_physical_homogeneity_child_id": h1_id,
        "time2_physical_homogeneity_child_id": h2_id,
        "canonical_recut_branch_rule_ids": [recut0_id, recut1_id],
        "two_step_homogeneous_child_id": child_id,
        "time1_target_chart_id": chart1_id,
        "time2_target_chart_id": chart2_id,
        "time2_target_chart_status": (
            "STRICT_SINGLE_CHART" if chart2_id is not None
            else "TARGET_NORMAL_CHART_SEAM_NOT_STRICTLY_EXCLUDED"
        ),
        "F5_numeric_slot_id": f5_id,
        "F5_two_step_adapted_inverse_strict_upper": qstr(TWO_STEP_THETA),
        "F6_numeric_slot_id": f6_id,
        "F6_two_step_log_variation_strict_upper": qstr(TWO_STEP_LOG_VARIATION),
        "two_collision_invariant_area_Jacobian": "1",
        "coordinate_base_mass_exact_rational": prior["coordinate_base_mass_exact_rational"],
        "collision_area_mass_exact_symbolic": prior[
            "parameter_averaged_unnormalized_collision_area_mass_exact"
        ],
        "numeric_strong_q2": None,
        "Arb_geometry_witness_sha256": audit["Arb_geometry_witness_sha256"],
    }
    return payload, None, audit


def downstream_frontier() -> dict[str, Any]:
    reasons = {
        4: "5,280 Q2 boxes do not strictly exclude the time-two target normal-chart seam; only the chart-free physical branch is frozen there",
        7: "canonical artificial recut endpoints and Q2 word boundaries lack a charged characteristic-Z sum",
        14: "no branchwise regular-density assembly or numerical common-carrier recovery cost",
        15: "no survivor-conditioned standard-family recovery theorem on the Q2 registry",
        16: "no limiting physical coarea/DQ face atlas on the Q2 branch registry",
        17: "no return-wide dynamic tests and no numerical C_fw/C_rev",
        18: "F14-F17 are not assembled into one operator phase block",
    }
    rows = [{
        "field_index": index,
        "field_name": FIELDS[index - 1],
        "materialized_Q2_slot_count": 0,
        "status": "NOT_CERTIFIED",
        "first_missing_dependency": reasons[index],
    } for index in (4, 7, 14, 15, 16, 17, 18)]
    return {
        "first_unfillable_field_on_the_full_Q2_chart_ledger": {
            "field_index": 4,
            "field_name": FIELDS[3],
            "reason": reasons[4],
        },
        "first_missing_field_after_the_strict_single_chart_subledger": {
            "field_index": 7,
            "field_name": FIELDS[6],
            "reason": reasons[7],
        },
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "F4_strict_single_time2_chart_slot_count": 108726,
        "F7_materialized_Q2_slot_count": 0,
        "F14_through_F18_materialized_Q2_slot_count": 0,
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    step1_manifest = time2_cert.load_step1_manifest()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "physical cores")
    # Freshly replay the complete first-owner claims on all parent cores.
    core_rows = [core_cert.certify_core(core) for core in cores]
    require(all(row["strict_first_hit"] is True for row in core_rows), "step1 owners")
    require(all(row["incoming_and_outgoing_cos_phi_strict_lower"] == "19/20" for row in core_rows), "core central")

    q1_rows = [
        row
        for row in step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    require(len(q1_rows) == 2868, "Q1 parents")
    q1_rows.sort(key=lambda row: row["atom_id"])
    prior_template_id = round27_cert.strong_template()["conditional_template_id"]

    classification_histogram: Counter[str] = Counter()
    depth_histogram: Counter[int] = Counter()
    owner_histogram: Counter[str] = Counter()
    target_word_histogram: Counter[str] = Counter()
    chart1_histogram: Counter[str] = Counter()
    chart2_histogram: Counter[str] = Counter()
    blocker_histogram: Counter[str] = Counter()
    mass_by_kind: Counter[str] = Counter()
    terminal_ids: set[str] = set()
    q2_ids: set[str] = set()
    h1_ids: set[str] = set()
    h2_ids: set[str] = set()
    recut_rule_ids: set[str] = set()
    child_ids: set[str] = set()
    f5_ids: set[str] = set()
    f6_ids: set[str] = set()
    restriction_ids: set[str] = set()
    mass_ids: set[str] = set()
    area_ids: set[str] = set()
    payload_digest = hashlib.sha256()
    audit_digest = hashlib.sha256()
    terminal_order_digest = hashlib.sha256()
    terminal_order_digest.update(b"[")
    first_terminal_id = True
    representatives: list[dict[str, Any]] = []
    first_blocker: dict[str, Any] | None = None

    for parent in q1_rows:
        stack = [time2_cert.atom_from_step1_row(parent, cores)]
        while stack:
            atom = stack.pop()
            classification, status, destination_id, state, owner = classify_with_geometry(
                atom, cores
            )
            if (
                classification == "UNRESOLVED_TIME2_OUTER"
                and atom.depth < time2_cert.MAX_TOTAL_BINARY_DEPTH
            ):
                left, right = time2_cert.step1.split_atom(atom)
                stack.append(right)
                stack.append(left)
                continue
            selected_target = None if owner is None else owner["selected_target_id"]
            row = compact_terminal_row(
                parent, atom, classification, status, destination_id, selected_target
            )
            require(row["time2_atom_id"] not in terminal_ids, "terminal atom ID")
            terminal_ids.add(row["time2_atom_id"])
            if not first_terminal_id:
                terminal_order_digest.update(b",")
            terminal_order_digest.update(canonical_json(row["time2_atom_id"]).encode("utf-8"))
            first_terminal_id = False
            classification_histogram[classification] += 1
            depth_histogram[atom.depth] += 1
            owner_histogram[status] += 1
            mass_by_kind[classification] += Q(
                row["parameter_averaged_unnormalized_base_mass"]
            )
            if classification != "SURVIVE_THROUGH_2_INNER":
                continue
            require(state is not None and owner is not None, "Q2 collision geometry")
            q2_ids.add(row["time2_atom_id"])
            payload, blocker, audit = materialized_payload(
                row, atom, state, owner, cores, prior_template_id
            )
            audit_digest.update(canonical_json({
                "time2_atom_id": row["time2_atom_id"], **audit,
            }).encode("utf-8"))
            audit_digest.update(b"\n")
            if payload is None:
                assert blocker is not None
                blocker_histogram[blocker] += 1
                if first_blocker is None:
                    first_blocker = {
                        "time2_atom_id": row["time2_atom_id"],
                        "reason": blocker,
                        "audit": audit,
                    }
                continue
            payload_digest.update(canonical_json(payload).encode("utf-8"))
            payload_digest.update(b"\n")
            h1_ids.add(payload["time1_physical_homogeneity_child_id"])
            h2_ids.add(payload["time2_physical_homogeneity_child_id"])
            recut_rule_ids.update(payload["canonical_recut_branch_rule_ids"])
            child_ids.add(payload["two_step_homogeneous_child_id"])
            f5_ids.add(payload["F5_numeric_slot_id"])
            f6_ids.add(payload["F6_numeric_slot_id"])
            restriction_ids.add(payload["restriction_id"])
            mass_ids.add(payload["mass_slot_id"])
            area_ids.add(payload["area_Jacobian_slot_id"])
            chart1_histogram[payload["time1_target_chart_id"]] += 1
            chart2_histogram[
                payload["time2_target_chart_id"]
                if payload["time2_target_chart_id"] is not None
                else "UNRESOLVED_REPRESENTATION_SEAM"
            ] += 1
            target_word_histogram[
                f"{atom.source_core.target_id}->{owner['selected_target_id']}"
            ] += 1
            if len(representatives) < 3:
                representatives.append(payload)

    terminal_order_digest.update(b"]")
    expected_classification = {
        "SURVIVE_THROUGH_2_INNER": 114006,
        "UNRESOLVED_TIME2_OUTER": 302988,
    }
    expected_depth = {
        0: 4, 4: 4, 5: 8, 7: 116, 8: 670, 9: 248, 10: 1130,
        11: 4690, 12: 3648, 13: 9434, 14: 27556, 15: 14738, 16: 354748,
    }
    expected_owner = {
        "strict_unique_second_collision_owner": 130794,
        "unresolved_competitor:unresolved_discriminant": 272840,
        "unresolved_time1_outgoing_chart_or_geometry": 13360,
    }
    require(dict(classification_histogram) == expected_classification, "classification replay")
    require(dict(depth_histogram) == expected_depth, "depth replay")
    require(dict(owner_histogram) == expected_owner, "owner replay")
    require(len(terminal_ids) == 416994 and len(q2_ids) == 114006, "terminal counts")
    require(terminal_order_digest.hexdigest() == "30a8922a3763e3f8d6e049a744a2d41d82103c2b73b97c118c5c58b558d63aaf", "terminal IDs")
    require(mass_by_kind["SURVIVE_THROUGH_2_INNER"] == Q(5257799, 5120000000), "Q2 mass")
    require(mass_by_kind["UNRESOLVED_TIME2_OUTER"] == Q(106721, 204800000), "unresolved mass")
    require(mass_by_kind["RETURN_AT_2_INNER"] == 0, "finite R2 mass")
    require(sum(mass_by_kind.values()) == Q(123841, 80000000), "Q1 mass")

    eligible = len(child_ids)
    require(len(h1_ids) == len(h2_ids) == eligible, "homogeneity ID uniqueness")
    require(len(recut_rule_ids) == 2 * eligible, "recut branch-rule ID uniqueness")
    require(len(f5_ids) == len(f6_ids) == eligible, "F5/F6 ID uniqueness")
    require(len(restriction_ids) == len(mass_ids) == len(area_ids) == eligible, "typed prior IDs")
    require(eligible + sum(blocker_histogram.values()) == 114006, "Q2 exhaustion")
    strict_time2_chart_count = eligible - chart2_histogram[
        "UNRESOLVED_REPRESENTATION_SEAM"
    ]
    require(strict_time2_chart_count == 108726, "strict time2 chart subledger")
    require(
        chart2_histogram["UNRESOLVED_REPRESENTATION_SEAM"] == 5280,
        "time2 seam frontier",
    )

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "source_registry": "round26 strict Q2-inner depth<=16 admitted atoms",
            "replay_engine": "fresh 384-bit Arb full adaptive geometry with retained collision states",
            "canonical_recut_policy": "deterministic adapted-arclength branch rules producing cells of length at most 1e-90",
        },
        "full_time2_Arb_replay": {
            "precision_bits": 384,
            "Q1_parent_count": 2868,
            "terminal_leaf_count": len(terminal_ids),
            "classification_histogram": dict(sorted(classification_histogram.items())),
            "depth_histogram": {str(k): v for k, v in sorted(depth_histogram.items())},
            "owner_status_histogram": dict(sorted(owner_histogram.items())),
            "terminal_atom_ids_sha256": terminal_order_digest.hexdigest(),
            "strict_Q2_atom_count": len(q2_ids),
            "strict_Q2_atom_ids_sha256": canonical_digest(sorted(q2_ids)),
            "Q2_coordinate_base_mass_exact": qstr(
                mass_by_kind["SURVIVE_THROUGH_2_INNER"]
            ),
            "unresolved_coordinate_base_mass_exact": qstr(
                mass_by_kind["UNRESOLVED_TIME2_OUTER"]
            ),
            "finite_depth_R2_admitted_count": classification_histogram[
                "RETURN_AT_2_INNER"
            ],
        },
        "Q2_two_step_homogeneity_and_recut_registry": {
            "homogeneity_cutoff_k0": K0,
            "central_H0_target_cosine_strict_lower": qstr(CENTRAL_COSINE_LOWER),
            "strict_Q2_atom_count": len(q2_ids),
            "fully_materialized_Q2_atom_count": eligible,
            "blocked_Q2_atom_count": sum(blocker_histogram.values()),
            "blocker_histogram": dict(sorted(blocker_histogram.items())),
            "first_blocker": first_blocker,
            "fresh_step1_parent_core_owner_replay_count": 24,
            "fresh_step2_unique_owner_Q2_count": len(q2_ids),
            "time1_physical_homogeneity_child_id_count": len(h1_ids),
            "time2_physical_homogeneity_child_id_count": len(h2_ids),
            "two_step_homogeneous_child_id_count": len(child_ids),
            "canonical_recut_branch_rule_id_count": len(recut_rule_ids),
            "canonical_recut_branch_rules_per_materialized_Q2_atom": 2,
            "actual_curve_recut_instance_id_count": 0,
            "actual_curve_recut_instance_id_schema": "recut-instance:(branch-rule-id):(parent-W-id):natural-index-j",
            "branch_rule_ids_are_actual_curve_instance_ids": False,
            "whole_atom_crosses_physical_homogeneity_boundary_count": sum(
                value for key, value in blocker_histogram.items() if "homogeneity" in key
            ),
            "strict_single_time2_target_chart_Q2_atom_count": strict_time2_chart_count,
            "time2_target_chart_seam_not_strictly_excluded_Q2_atom_count": (
                chart2_histogram["UNRESOLVED_REPRESENTATION_SEAM"]
            ),
            "chart_seams_are_representation_boundaries_not_physical_cuts": True,
            "chart_free_physical_homogeneity_recut_used_for_F5_F6": True,
            "time1_target_chart_histogram": dict(sorted(chart1_histogram.items())),
            "time2_target_chart_histogram": dict(sorted(chart2_histogram.items())),
            "collision_target_word_histogram_sha256": canonical_digest(
                dict(sorted(target_word_histogram.items()))
            ),
            "full_Q2_geometry_audit_rows_sha256": audit_digest.hexdigest(),
            "materialized_payload_rows_sha256": payload_digest.hexdigest(),
            "representative_materialized_rows": representatives,
        },
        "Q2_numeric_F5_F6_slot_registry": {
            "materialized_two_step_homogeneous_child_count": eligible,
            "F5_universal_branch_rule_slot_count": len(f5_ids),
            "F6_universal_branch_rule_slot_count": len(f6_ids),
            "actual_curve_instance_slot_count": 0,
            "universal_quantifier": "for every actual canonical standard-curve recut instance generated by the two branch rules on this 2D Q2 branch",
            "slot_counts_are_actual_curve_instance_counts": False,
            "one_step_adapted_unstable_inverse_strict_upper": qstr(THETA),
            "two_step_adapted_unstable_inverse_strict_upper": qstr(TWO_STEP_THETA),
            "one_step_canonical_recut_log_variation_strict_upper": qstr(
                ONE_STEP_LOG_VARIATION
            ),
            "two_step_canonical_recut_log_variation_strict_upper": qstr(
                TWO_STEP_LOG_VARIATION
            ),
            "F5_universal_branch_rule_slot_ids_sha256": canonical_digest(sorted(f5_ids)),
            "F6_universal_branch_rule_slot_ids_sha256": canonical_digest(sorted(f6_ids)),
            "homogeneity_child_ids_sha256": canonical_digest(
                sorted(h1_ids | h2_ids)
            ),
            "canonical_recut_branch_rule_ids_sha256": canonical_digest(
                sorted(recut_rule_ids)
            ),
            "prior_conditional_template_reference_id": prior_template_id,
            "literal_prior_canonical_recut_component_field_filled": False,
            "literal_prior_conditional_template_join": "NOT_CERTIFIED",
            "universal_template_reinstantiated_as_branch_rule_theorem": eligible > 0,
            "unsplit_Q2_atom_given_one_global_unstable_Jacobian_value": False,
        },
        "strong_type_separation": {
            "joined_prior_restriction_id_count": len(restriction_ids),
            "joined_prior_coordinate_and_collision_mass_slot_count": len(mass_ids),
            "joined_prior_invariant_area_Jacobian_slot_count": len(area_ids),
            "coordinate_base_mass_is_exact_collision_area_mass": False,
            "invariant_area_Jacobian_is_adaptive_coordinate_Jacobian": False,
            "invariant_area_Jacobian_is_unstable_one_dimensional_Jacobian": False,
            "invariant_area_log_distortion_is_F6": False,
            "F5_F6_use_only_the_frozen_universal_unstable_template_and_physical_homogeneity_recut_branch_rule_ids": True,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_strong_q2_count": 0,
        },
        "downstream_frontier": downstream_frontier(),
        "strict_nonpromotion": {
            "finite_depth_R2_admitted_zero_means_physical_R2_empty": False,
            "complete_limiting_R2_Q2_partition_reproved_here": False,
            "arbitrary_n_component_registry": "NOT_CERTIFIED",
            "F7_characteristic_cut_growth": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "numeric_strong_q2": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    registry = result["Q2_two_step_homogeneity_and_recut_registry"]
    slots = result["Q2_numeric_F5_F6_slot_registry"]
    eligible = registry["fully_materialized_Q2_atom_count"]
    full = eligible == registry["strict_Q2_atom_count"]
    return {
        "Q2_two_step_physical_homogeneity_children": (
            f"CERTIFIED_{eligible}" if full else f"MAXIMAL_CERTIFIED_SUBLEDGER_{eligible}"
        ),
        "Q2_canonical_recut_branch_rule_ids": f"CERTIFIED_{2 * eligible}",
        "Q2_actual_curve_recut_instance_ids_materialized": 0,
        "Q2_numeric_F5_slots": (
            f"CERTIFIED_{slots['F5_universal_branch_rule_slot_count']}_UNIVERSAL_BRANCH_RULE_SLOTS"
        ),
        "Q2_numeric_F6_slots": (
            f"CERTIFIED_{slots['F6_universal_branch_rule_slot_count']}_UNIVERSAL_BRANCH_RULE_SLOTS"
        ),
        "Q2_numeric_strong_q2": "NOT_CERTIFIED",
        "Q2_F7_F14_F18": "NOT_CERTIFIED",
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
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round28_q2_homogeneity_recut_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    registry = result["Q2_two_step_homogeneity_and_recut_registry"]
    slots = result["Q2_numeric_F5_F6_slot_registry"]
    print(f"Q2_HOMOGENEITY_RECUT_CHILDREN: {registry['fully_materialized_Q2_atom_count']}")
    print(f"Q2_CANONICAL_RECUT_BRANCH_RULE_IDS: {registry['canonical_recut_branch_rule_id_count']}")
    print("Q2_ACTUAL_CURVE_RECUT_INSTANCE_IDS: 0")
    print(
        "Q2_NUMERIC_F5_F6_UNIVERSAL_BRANCH_RULE_SLOTS: "
        f"{slots['F5_universal_branch_rule_slot_count']}/"
        f"{slots['F6_universal_branch_rule_slot_count']}"
    )
    print("Q2_F7_F14_F18: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
