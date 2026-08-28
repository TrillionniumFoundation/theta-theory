#!/usr/bin/env python3
"""Zero-credit exact graph and universal-containment gate for C30q5.

This read-only gate targets the North/South ``03.15.11010101`` compact-q
pair.  It replays the pinned Round176 -> Round180 -> P215 complement, proves
that all 136 residual children per origin lie in exactly one applicable
full-r analytic root, and separately closes the eight clipped-Delta children
through an exact Delta<0 / Delta=0 / Delta>0 partition.

The graph is allowed to cross the shared |p|=1023/1024 face.  Lower strata
are owned once by the lexicographically least incident closed child.  No
formal ledger, seal, release authority, or CM2 state is changed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

from flint import arb, ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
Q4_SOURCE = (
    HERE
    / "cm2_round306c30q4_compact_q_11010111_universal_containment_gate.py"
)
Q4_SOURCE_SHA256 = (
    "cdf1b43cec11aa6f3b03ef3a934cd1260478c1266dc38a89fb23e1996f482232"
)
ROUND184_VERIFIER = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
      "verifier.py"
)
ROUND184_VERIFIER_SHA256 = (
    "55a4e2b44d0f8617d7b7fd0befd251a5cb206d388c23d7b395e39b9a17fa4889"
)
SCHEMA = "cm2.round306c30q5.compact-q-11010101-clipped-graph-gate.v1"
ORIGINS = ("W:N:03.15.11010101", "W:S:H.03.15.11010101")
COMPACT = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
FROZEN_TARGET = "W[1,0]"
FUTURE_TARGET = "W[-1,0]"
EXPECTED_GRAPH_TARGET = {
    "W:N:03.15.11010101": "G[0,1]",
    "W:S:H.03.15.11010101": "G[0,0]",
}
EXPECTED_DERIVATIVE = {
    "W:N:03.15.11010101": "NEGATIVE",
    "W:S:H.03.15.11010101": "POSITIVE",
}
EXPECTED_RESIDUAL_SHA256 = {
    "W:N:03.15.11010101":
        "df9a386901f8eac51c022f2f1fa53ce6c12b30de7ac04761a9c037869f9b4cd4",
    "W:S:H.03.15.11010101":
        "ba72ca95b2de7413f1475b917ca8ccd865154c0181c61bb269307cb02b66ef05",
}
T_DOMAIN = (Q(-21771, 256000), Q(-10797, 128000))
S_DOMAIN = (Q(-1, 400), Q(1, 400))
P_INNER = Q(511, 512)
P_SHARED = Q(1023, 1024)
TARGET_RADIUS = Q(9, 25)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path: Path, expected_hash: str, name: str) -> Any:
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
         name + " source pin")
    specification = importlib.util.spec_from_file_location(name, path)
    need(specification is not None and specification.loader is not None,
         name + " import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == path, name + " import identity")
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
         name + " source stable")
    return module


def source_pins() -> dict[str, str]:
    result = {
        Q4_SOURCE.name: hashlib.sha256(Q4_SOURCE.read_bytes()).hexdigest(),
        ROUND184_VERIFIER.name:
            hashlib.sha256(ROUND184_VERIFIER.read_bytes()).hexdigest(),
    }
    need(
        result == {
            Q4_SOURCE.name: Q4_SOURCE_SHA256,
            ROUND184_VERIFIER.name: ROUND184_VERIFIER_SHA256,
        },
        "Q4/Round184 source pins",
    )
    return result


def arbq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def exact_graph_certificate(q1: Any, probe: Any) -> dict[str, Any]:
    """Prove the common N/S graph branch and freeze a face-crossing refuter."""
    t = probe.r176.base.arb_interval(*T_DOMAIN)
    s = probe.r176.base.arb_interval(*S_DOMAIN)
    a = (arb(1) - t * t).sqrt()
    u = arbq(Q(1, 2)) + s
    A = a * u + t / 2
    B = t * u - a / 2 + arbq(Q(4, 25))
    radius = arbq(TARGET_RADIUS)
    radicand = A * A + B * B - radius * radius
    need(bool(A > 0) and bool(B < 0) and bool(radicand > 0),
         "common graph branch signs")

    def delta_at(value: Q) -> tuple[arb, arb]:
        p = arbq(value)
        b = (arb(1) - p * p).sqrt()
        h = b * A + p * B
        return h, radius * radius - h * h

    h_inner, delta_inner = delta_at(P_INNER)
    h_shared, delta_shared = delta_at(P_SHARED)
    h_one, delta_one = delta_at(Q(1))
    need(
        bool(delta_inner > 0)
        and bool(delta_one < 0)
        and not bool(delta_shared > 0)
        and not bool(delta_shared < 0),
        "positive/overwrap/negative graph faces",
    )

    def point_star(t_value: Q, s_value: Q) -> tuple[dict[str, Any], arb]:
        tt, ss = arbq(t_value), arbq(s_value)
        aa = (arb(1) - tt * tt).sqrt()
        uu = arbq(Q(1, 2)) + ss
        point_A = aa * uu + tt / 2
        point_B = tt * uu - aa / 2 + arbq(Q(4, 25))
        point_D = (
            point_A * point_A + point_B * point_B - radius * radius
        )
        p_star = (
            -radius * point_B + point_A * point_D.sqrt()
        ) / (point_A * point_A + point_B * point_B)
        b_star = (arb(1) - p_star * p_star).sqrt()
        branch_residual = b_star * point_A + p_star * point_B + radius
        need(
            bool(p_star > arbq(P_INNER))
            and bool(p_star < arb(1))
            and not bool(branch_residual > 0)
            and not bool(branch_residual < 0),
            "unsquared point graph branch",
        )
        return {
            "t": str(t_value),
            "s": str(s_value),
            "P_star": q1.bounds(p_star),
            "P_star_minus_shared_face": q1.bounds(p_star - arbq(P_SHARED)),
            "unsquared_branch_residual_h_plus_9_over_25":
                q1.bounds(branch_residual),
        }, p_star

    below, below_value = point_star(T_DOMAIN[0], S_DOMAIN[0])
    above, above_value = point_star(T_DOMAIN[1], S_DOMAIN[1])
    need(
        bool(below_value < arbq(P_SHARED))
        and bool(above_value > arbq(P_SHARED)),
        "shared-face crossing counterexamples",
    )
    return {
        "coordinate_definitions": {
            "P": "abs(p)",
            "a": "sqrt(1-t^2)",
            "b": "sqrt(1-P^2)",
            "u": "1/2+s",
            "A": "a*u+t/2",
            "B": "t*u-a/2+4/25",
        },
        "north_target_G_0_1": {
            "ell": "P*A-b*B",
            "signed_transverse_h": "b*A+P*B",
        },
        "south_target_G_0_0": {
            "ell": "P*A-b*B",
            "signed_transverse_h": "-(b*A+P*B)",
        },
        "common_discriminant": "Delta=(9/25)^2-(b*A+P*B)^2",
        "correct_unsquared_branch": "b*A+P*B=-9/25",
        "unique_graph_formula": (
            "P*=(-(9/25)*B+A*sqrt(A^2+B^2-(9/25)^2))/(A^2+B^2)"
        ),
        "branch_guards": {
            "A_strict_positive": True,
            "B_strict_negative": True,
            "radicand_strict_positive": True,
            "dh_dP_strict_negative_on_511_over_512_to_1": True,
            "squared_extraneous_branch_rejected": True,
        },
        "interval_bounds": {
            "A": q1.bounds(A),
            "B": q1.bounds(B),
            "radicand": q1.bounds(radicand),
            "Delta_at_abs_p_511_over_512": q1.bounds(delta_inner),
            "Delta_at_abs_p_1023_over_1024": q1.bounds(delta_shared),
            "Delta_at_abs_p_1": q1.bounds(delta_one),
            "h_at_abs_p_511_over_512": q1.bounds(h_inner),
            "h_at_abs_p_1023_over_1024": q1.bounds(h_shared),
            "h_at_abs_p_1": q1.bounds(h_one),
        },
        "shared_face_falsification": {
            "claim_refuted":
                "P_star is uniformly confined to one side of 1023/1024",
            "below_face_witness": below,
            "above_face_witness": above,
            "graph_crosses_shared_abs_p_face": True,
            "full_p_graph_claim": False,
        },
    }


def analytic_rebuild(
    q1: Any,
    probe: Any,
    roots_by_origin: dict[str, list[Any]],
    k: Q,
    frozen: dict[str, Any],
) -> list[dict[str, Any]]:
    root_inputs = [{
        "origin_key": row.origin_key,
        "root_key": row.key,
        "source_chart": row.chart_id,
        "p_sign": 1 if row.box.p1 == 1 else -1,
        "active_targets": list(row.active_targets),
        "box": q1.box_row(row.box),
    } for origin in ORIGINS for row in roots_by_origin[origin]]
    q1.progress = lambda _message: None
    origins, _cohorts, analytic = q1.analytic_census(probe, root_inputs, k)
    rebuilt_roots = analytic["root_results"]
    for row in rebuilt_roots:
        parameters = row["cohort_parameters"]
        signed = parameters.pop("derived_abs_p_endpoint_near_q0")
        parameters["derived_signed_p_endpoint_near_q0"] = signed
        parameters["derived_absolute_p_endpoint_near_q0"] = str(abs(Q(signed)))
    frozen_roots = sorted(
        (row for row in frozen["analytic_cohort_census"]["root_results"]
         if row["origin_key"] in ORIGINS),
        key=lambda row: row["root_key"],
    )
    need(canonical(rebuilt_roots) == canonical(frozen_roots),
         "target analytic roots match frozen dual-seed Q1")
    need(
        len(rebuilt_roots) == 32
        and all(row["analytic_root_applicable"] is True
                and row["failure_reasons"] == [] for row in rebuilt_roots)
        and all(row["frozen_target"]["strict"]["ell_negative"] is True
                for row in rebuilt_roots)
        and all(FUTURE_TARGET in row["certified_future_witness_targets"]
                for row in rebuilt_roots),
        "all 32 analytic roots pass",
    )
    return origins


def targeted_replay(
    q1: Any,
    probe: Any,
    round184: Any,
    registry: list[dict[str, Any]],
    pinned_faces: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]], dict[str, list[Any]], Q,
    list[dict[str, Any]], dict[str, Any],
]:
    authority = {
        row["origin_key"]: row
        for row in registry if row["origin_key"] in ORIGINS
    }
    need(set(authority) == set(ORIGINS),
         "target origins in outcome-blind registry")
    state = probe.r176.replay_frontier()
    frontier: dict[str, list[Any]] = defaultdict(list)
    preclosed: Counter[str] = Counter()
    kinds: dict[str, set[str]] = defaultdict(set)
    kinds.update({
        key: set(value) for key, value in state["origin_kinds"].items()
        if key in ORIGINS
    })
    for row in state["frontier"]:
        if row.origin_key not in authority:
            continue
        kind, _evidence = probe.r176.closure(row)
        if kind is None:
            frontier[row.origin_key].append(row)
        else:
            preclosed[row.origin_key] += 1
            kinds[row.origin_key].add(kind)
    need(set(frontier) == set(ORIGINS), "target frontiers rebuilt")
    for rows in frontier.values():
        rows.sort(key=lambda row: row.key)

    roots_by_origin: dict[str, list[Any]] = {}
    for origin in ORIGINS:
        roots_by_origin[origin] = sorted(
            (row for row in frontier[origin]
             if probe.r180.initial_category(row) == COMPACT),
            key=lambda row: row.key,
        )
    dynamic_faces = sorted(
        (probe.q_face_evidence(row)
         for origin in ORIGINS for row in roots_by_origin[origin]),
        key=lambda row: row["root_key"],
    )
    expected_faces = sorted(
        (row for row in pinned_faces if row["origin_key"] in ORIGINS),
        key=lambda row: row["root_key"],
    )
    need(canonical(dynamic_faces) == canonical(expected_faces)
         and len(dynamic_faces) == 32, "target Round218 face replay")

    k_values: set[Q] = set()
    for roots in roots_by_origin.values():
        for row in roots:
            need(row.box.p1 == 1 or row.box.p0 == -1,
                 "compact p endpoint:" + row.key)
            lower = row.box.p0 if row.box.p1 == 1 else -row.box.p1
            k_values.add(Q(1) - lower * lower)
    need(k_values == {Q(1023, 262144)}, "single q scale")

    rows_out: list[dict[str, Any]] = []
    graph_rows: list[dict[str, Any]] = []
    clipped_children: list[Any] = []
    for origin in ORIGINS:
        auth = authority[origin]
        unresolved = frontier[origin]
        need(
            len(unresolved) == auth["Round176_residual_root_count"] == 62
            and preclosed[origin]
                == auth["Round176_preclosed_frontier_count"] == 2
            and sorted(kinds[origin]) == auth["Round176_preclosed_kinds"],
            "target Round176 authority:" + origin,
        )
        refinement = probe.r180.refine_origin(unresolved, 4)
        children = sorted(
            refinement["final_residual_rows"], key=lambda row: row.key
        )
        categories = Counter(probe.r180.residual_category(row)
                             for row in children)
        need(
            len(children) == auth["Round180_residual_child_count"] == 554
            and digest([row.key for row in children])
                == auth["Round180_residual_child_keys_sha256"]
            and q1.map_counter(categories)
                == auth["Round180_residual_category_count"],
            "target Round180 authority:" + origin,
        )
        residual: list[dict[str, Any]] = []
        clipped_boxes: list[Any] = []
        closed = 0
        for child in children:
            category = probe.r180.residual_category(child)
            reduction = probe.p215.exact_behind_reduce(child, category)
            if reduction["closed"]:
                closed += 1
                continue
            containers = sorted(
                root.key for root in roots_by_origin[origin]
                if q1.contained(child.box, root.box)
            )
            need(len(containers) == 1,
                 "unique analytic container:" + child.key)
            residual.append({
                "cell_key": child.key,
                "category": category,
                "active_targets": list(child.active_targets),
                "box": q1.box_row(child.box),
                "analytic_root_container_count": len(containers),
                "analytic_root_containers": containers,
                "residual_reason": reduction["residual_reason"],
            })
            if category != CLIPPED:
                continue
            clipped_children.append(child)
            clipped_boxes.append(child.box)
            proof, reason = round184.clipped_partition_proof(child)
            need(proof is not None and reason == "CLOSED",
                 "native clipped graph proof:" + child.key)
            records = probe.r176.records_for(
                child.chart_id, child.box, child.active_targets
            )
            candidate = [record for record in records
                         if record.classification == "unresolved_discriminant"]
            competitor = [record for record in records
                          if record.target_id == FUTURE_TARGET]
            need(len(candidate) == len(competitor) == 1,
                 "single graph candidate/competitor:" + child.key)
            candidate_record, competitor_record = candidate[0], competitor[0]
            competitor_lower = probe.r176.earliest_lower(competitor_record)
            need(
                competitor_lower is not None
                and probe.r176.target_positive_first(candidate_record, records)
                and proof["target"] == EXPECTED_GRAPH_TARGET[origin]
                and proof["strict_p_derivative_sign"]
                    == EXPECTED_DERIVATIVE[origin]
                and proof["full_p_graph"] is False
                and proof["graph_owner_target"] != FROZEN_TARGET
                and proof["all_three_strata_excluded"] is True
                and proof["whole_closed_cell_excluded"] is True,
                "exact three-stratum graph closure:" + child.key,
            )
            graph_rows.append({
                "origin_key": origin,
                "cell_key": child.key,
                "analytic_root_container": containers[0],
                "box": q1.box_row(child.box),
                "active_targets": list(child.active_targets),
                "candidate_ell": q1.bounds(candidate_record.ell),
                "candidate_radius": str(TARGET_RADIUS),
                "competitor_earliest_lower": q1.bounds(competitor_lower),
                "strict_order_margin":
                    q1.bounds(competitor_lower - candidate_record.ell),
                "three_stratum_proof": proof,
            })

        category_count = Counter(row["category"] for row in residual)
        expected_s = [
            (S_DOMAIN[0] + Q(index, 1600),
             S_DOMAIN[0] + Q(index + 1, 1600))
            for index in range(8)
        ]
        actual_s = sorted((box.s0, box.s1) for box in clipped_boxes)
        expected_p = (
            (P_INNER, P_SHARED) if origin.startswith("W:N:")
            else (-P_SHARED, -P_INNER)
        )
        need(
            closed == 418
            and len(residual) == 136
            and digest(residual) == EXPECTED_RESIDUAL_SHA256[origin]
            and category_count == Counter({COMPACT: 128, CLIPPED: 8})
            and all(row["analytic_root_container_count"] == 1
                    for row in residual)
            and actual_s == expected_s
            and { (box.t0, box.t1) for box in clipped_boxes }
                == {T_DOMAIN}
            and { (box.p0, box.p1) for box in clipped_boxes }
                == {expected_p},
            "136-row split/containment/8-bin graph cover:" + origin,
        )
        rows_out.append({
            "origin_key": origin,
            "Round176_frontier_conservation": "64=2+62",
            "Round176_preclosed_root_count": 2,
            "Round176_unresolved_root_count": 62,
            "Round180_final_child_count": 554,
            "P215_exact_behind_closed_child_count": closed,
            "analytic_residual_child_count": len(residual),
            "residual_category_count": {
                CLIPPED: 8,
                COMPACT: 128,
            },
            "residual_container_multiplicity": {"1": len(residual)},
            "clipped_s_bin_count": 8,
            "clipped_s_bins": [[str(a), str(b)] for a, b in actual_s],
            "residual_rows_sha256": digest(residual),
            "residual_rows": residual,
        })

    graph_rows.sort(key=lambda row: row["cell_key"])
    need(len(graph_rows) == 16 and len(clipped_children) == 16,
         "combined graph row count")
    outer = round184.analytic_outer_ledger(clipped_children, True)
    need(
        outer["outer_proof_status"] == "ALL_EXCLUDED"
        and outer["all_outer_strata_inherit_EXCLUDED_graph_proof"] is True
        and outer["half_open_owner"]
            == "lexicographically least incident closed child key",
        "graph outer half-open ownership",
    )
    return rows_out, roots_by_origin, next(iter(k_values)), graph_rows, outer


def rebuild() -> dict[str, Any]:
    ctx.prec = 256
    initial_source_pins = source_pins()
    q4 = load(Q4_SOURCE, Q4_SOURCE_SHA256, "cm2_c30q4_for_q5")
    q2 = load(q4.Q2_SOURCE, q4.Q2_SOURCE_SHA256, "cm2_c30q2_for_q5")
    q1 = load(q4.Q1_SOURCE, q4.Q1_SOURCE_SHA256, "cm2_c30q1_for_q5")
    before = q1.capture_direct_pins()
    before_files = {
        name: {"sha256": row["sha256"],
               "file_identity": row["identity"]["file"]}
        for name, row in before.items()
    }
    frozen_document, q1_audit_hashes = q2.frozen_q1_audit()
    registry, faces, authority_pins = q1.load_authorities()
    probe = q1.load_definitions()
    round184 = load(
        ROUND184_VERIFIER,
        ROUND184_VERIFIER_SHA256,
        "cm2_round184_clipped_for_q5",
    )
    containment, roots_by_origin, k, graph_rows, graph_outer = targeted_replay(
        q1, probe, round184, registry, faces
    )
    analytic_origins = analytic_rebuild(
        q1, probe, roots_by_origin, k, frozen_document["result"]
    )
    partitions = {
        origin: q4.half_open_partition(origin, roots_by_origin[origin])
        for origin in ORIGINS
    }
    graph_exact = exact_graph_certificate(q1, probe)
    after = q1.capture_direct_pins()
    after_files = {
        name: {"sha256": row["sha256"],
               "file_identity": row["identity"]["file"]}
        for name, row in after.items()
    }
    need(before_files == after_files,
         "all selected input bytes/identities stable across Q5 replay")
    need(initial_source_pins == source_pins(),
         "Q4/Round184 sources stable across Q5 replay")

    return {
        "status": (
            "PASS_TWO_ORIGIN_136_RESIDUAL_CONTAINMENT_AND_16_CLIPPED_GRAPH_"
            "CLOSURE__ZERO_FORMAL_CREDIT"
        ),
        "verdict": "PASS_ZERO_CREDIT_WHOLE_ORIGIN_RESEARCH_GATE",
        "scope": "two frozen 03.15.11010101 compact-q origins only",
        "frozen_inputs": {
            **authority_pins,
            "Q4_source_sha256": Q4_SOURCE_SHA256,
            "Round184_clipped_verifier_sha256": ROUND184_VERIFIER_SHA256,
            "Q1_source_sha256": q4.Q1_SOURCE_SHA256,
            "Q2_source_sha256": q4.Q2_SOURCE_SHA256,
            "Q1_frozen_result_sha256": q2.Q1_RESULT_SHA256,
            "Q1_audit_member_sha256": q1_audit_hashes,
            "direct_input_file_bytes_and_identity_pre_post_stable": True,
        },
        "analytic_root_rebuild": {
            "q_squared_scale": str(k),
            "origin_count": 2,
            "root_count": 32,
            "all_roots_frozen_behind_and_nonfrozen_future_witness": True,
            "origin_rows_sha256": digest(analytic_origins),
            "origin_rows": analytic_origins,
        },
        "universal_residual_containment": {
            "origin_count": 2,
            "residual_child_count": 272,
            "compact_q_residual_child_count": 256,
            "clipped_graph_residual_child_count": 16,
            "all_residuals_in_exactly_one_analytic_root": True,
            "origin_rows_sha256": digest(containment),
            "origin_rows": containment,
        },
        "clipped_graph_three_stratum_closure": {
            "graph_child_count": 16,
            "Delta_negative_zero_positive_all_excluded": True,
            "graph_rows_sha256": digest(graph_rows),
            "graph_rows": graph_rows,
            "analytic_outer_half_open_ledger": graph_outer,
            "exact_common_graph_certificate": graph_exact,
        },
        "cross_root_half_open_partitions": partitions,
        "whole_origin_conclusion": {
            "per_origin_Round176_preclosed_roots": 2,
            "per_origin_P215_exact_behind_children": 418,
            "per_origin_analytic_contained_residual_children": 136,
            "per_origin_compact_q_residual_children": 128,
            "per_origin_clipped_graph_residual_children": 8,
            "per_origin_all_16_full_r_analytic_roots_pass": True,
            "per_origin_all_255_cross_root_strata_owned": True,
            "all_16_clipped_children_have_explicit_three_stratum_closure": True,
            "both_origins_exclude_frozen_first_owner_everywhere": True,
            "graph_uniformly_inside_clipped_slab": False,
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "source_W_formal_remaining": 80,
            "seal_or_release_authority": False,
            "D02": "BLOCKED",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_falsifiable_work": (
            "independently verify the exact graph branch, shared-face owner, "
            "and all 272 containment rows before routing the remaining "
            "non-applicable compact-q cohorts"
        ),
    }


def main() -> int:
    try:
        result = rebuild()
        document = {
            "schema": SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except (Reject, KeyError, StopIteration, TypeError, ValueError, OSError) as error:
        print("REJECT_C30Q5_CLIPPED_GRAPH_GATE:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
