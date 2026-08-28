#!/usr/bin/env python3
"""Universal 128-residual containment gate for two compact-q origins.

The earlier C30q1 combined gate required exactly one residual child.  That is
a sufficient routing convenience, not a mathematical necessity.  This
zero-credit gate targets the smaller fully-analytic ``03.15.11010111``
North/South pair, replays their complete Round176 -> Round180 -> P215
complement, and tests the actual universal condition: every surviving child
is compact-q and is contained in exactly one of the 16 full-r analytic root
domains.  Cross-root boundary strata are owned explicitly in all dimensions.

No formal ledger, seal, release authority, or CM2 state is changed.
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

from flint import ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
Q1_SOURCE = HERE / "cm2_round306c30q1_compact_q_54_origin_analytic_cohort_counterexample_gate.py"
Q1_SOURCE_SHA256 = "0242a62bf9ff443a9ff979fc789ac81a7bde4a2b8bc082f81dff813b8bf24936"
Q2_SOURCE = HERE / "cm2_round306c30q2_compact_q_exact_seven_cohort_counterexample_routing_gate.py"
Q2_SOURCE_SHA256 = "8e3beea8ab742443e028ab5e8c794a5e0f3df3467d70d0c4c3ca29e31983c125"
SCHEMA = "cm2.round306c30q4.compact-q-11010111-universal-containment-gate.v1"
ORIGINS = ("W:N:03.15.11010111", "W:S:H.03.15.11010111")
COMPACT_CATEGORY = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
FROZEN_TARGET = "W[1,0]"
FUTURE_TARGET = "W[-1,0]"
EXPECTED_RESIDUAL_SHA256 = {
    "W:N:03.15.11010111": "6e638b6cd6f3ca0972640e6bef9ee44dbd551a8aa0e72e8922c2357de6821113",
    "W:S:H.03.15.11010111": "0ce975dc4163aea892a0687e2bac04fcbe8144a75fdfe03a4ef206f17aa6ff82",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path: Path, expected_hash: str, name: str) -> Any:
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash, name + " source pin")
    specification = importlib.util.spec_from_file_location(name, path)
    need(specification is not None and specification.loader is not None, name + " import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == path, name + " imported identity")
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash, name + " source stable")
    return module


def axis_atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    need(tuple(sorted(set(cuts))) == cuts, "strict atom cuts")
    output: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        output.append(("POINT", point, point))
        if index + 1 < len(cuts):
            output.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return output


def half_open_partition(origin: str, roots: list[Any]) -> dict[str, Any]:
    t_cuts = tuple(sorted({value for row in roots for value in (row.box.t0, row.box.t1)}))
    s_cuts = tuple(sorted({value for row in roots for value in (row.box.s0, row.box.s1)}))
    r_cuts = (Q(0), Q(1))
    need(len(t_cuts) == 9 and s_cuts == (Q(-1, 400), Q(0), Q(1, 400)), "8x1x2 root cuts:" + origin)
    rectangles = {(row.box.t0, row.box.t1, row.box.s0, row.box.s1) for row in roots}
    expected = {
        (t_cuts[i], t_cuts[i + 1], s_cuts[j], s_cuts[j + 1])
        for i in range(8) for j in range(2)
    }
    need(len(roots) == 16 and rectangles == expected, "complete root rectangles:" + origin)
    rows: list[dict[str, Any]] = []
    for ta in axis_atoms(t_cuts):
        for ra in axis_atoms(r_cuts):
            for sa in axis_atoms(s_cuts):
                atom = {"t": ta, "r": ra, "s": sa}
                incident = sorted(
                    root.key for root in roots
                    if root.box.t0 <= ta[1] <= ta[2] <= root.box.t1
                    and Q(0) <= ra[1] <= ra[2] <= Q(1)
                    and root.box.s0 <= sa[1] <= sa[2] <= root.box.s1
                )
                need(bool(incident), "atom incidence:" + origin)
                geometry = {
                    key: ({"kind": item[0], "value": str(item[1])}
                          if item[0] == "POINT" else
                          {"kind": item[0], "lower": str(item[1]), "upper": str(item[2])})
                    for key, item in atom.items()
                }
                rows.append({
                    "ambient_dimension": sum(item[0] == "OPEN_INTERVAL" for item in atom.values()),
                    "geometry": geometry,
                    "incident_root_keys": incident,
                    "owner_root_key": incident[0],
                    "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    dimensions = Counter(row["ambient_dimension"] for row in rows)
    need(len(rows) == 255 and dimensions == Counter({3: 16, 2: 74, 1: 111, 0: 54}), "whole root partition:" + origin)
    return {
        "t_cuts": [str(value) for value in t_cuts],
        "s_cuts": [str(value) for value in s_cuts],
        "root_count": 16,
        "atomic_stratum_count": 255,
        "atomic_stratum_count_by_dimension": {str(key): dimensions[key] for key in (3, 2, 1, 0)},
        "owner_assignment_rows_sha256": digest(rows),
        "all_strata_owned_exactly_once": True,
    }


def targeted_replay(q1: Any, probe: Any, registry: list[dict[str, Any]], pinned_faces: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, list[Any]], Q]:
    authority = {row["origin_key"]: row for row in registry if row["origin_key"] in ORIGINS}
    need(set(authority) == set(ORIGINS), "target origins in outcome-blind registry")
    state = probe.r176.replay_frontier()
    frontier: dict[str, list[Any]] = defaultdict(list)
    preclosed: Counter[str] = Counter()
    kinds: dict[str, set[str]] = defaultdict(set)
    kinds.update({key: set(value) for key, value in state["origin_kinds"].items() if key in ORIGINS})
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
        roots = sorted(
            (row for row in frontier[origin] if probe.r180.initial_category(row) == COMPACT_CATEGORY),
            key=lambda row: row.key,
        )
        roots_by_origin[origin] = roots
    dynamic_faces = sorted(
        (probe.q_face_evidence(row) for origin in ORIGINS for row in roots_by_origin[origin]),
        key=lambda row: row["root_key"],
    )
    expected_faces = sorted(
        (row for row in pinned_faces if row["origin_key"] in ORIGINS),
        key=lambda row: row["root_key"],
    )
    need(canonical(dynamic_faces) == canonical(expected_faces) and len(dynamic_faces) == 32, "target Round218 face replay")
    k_values: set[Q] = set()
    for roots in roots_by_origin.values():
        for row in roots:
            need(row.box.p1 == 1 or row.box.p0 == -1, "compact p endpoint:" + row.key)
            lower = row.box.p0 if row.box.p1 == 1 else -row.box.p1
            k_values.add(Q(1) - lower * lower)
    need(k_values == {Q(1023, 262144)}, "single q scale")
    rows_out: list[dict[str, Any]] = []
    for origin in ORIGINS:
        auth = authority[origin]
        unresolved = frontier[origin]
        need(
            len(unresolved) == auth["Round176_residual_root_count"] == 55
            and preclosed[origin] == auth["Round176_preclosed_frontier_count"] == 7
            and sorted(kinds[origin]) == auth["Round176_preclosed_kinds"],
            "target Round176 authority:" + origin,
        )
        refinement = probe.r180.refine_origin(unresolved, 4)
        children = sorted(refinement["final_residual_rows"], key=lambda row: row.key)
        categories = Counter(probe.r180.residual_category(row) for row in children)
        need(
            len(children) == auth["Round180_residual_child_count"] == 548
            and digest([row.key for row in children]) == auth["Round180_residual_child_keys_sha256"]
            and q1.map_counter(categories) == auth["Round180_residual_category_count"],
            "target Round180 authority:" + origin,
        )
        residual: list[dict[str, Any]] = []
        closed = 0
        for child in children:
            category = probe.r180.residual_category(child)
            reduction = probe.p215.exact_behind_reduce(child, category)
            if reduction["closed"]:
                closed += 1
                continue
            containers = sorted(root.key for root in roots_by_origin[origin] if q1.contained(child.box, root.box))
            residual.append({
                "cell_key": child.key,
                "category": category,
                "active_targets": list(child.active_targets),
                "box": q1.box_row(child.box),
                "analytic_root_container_count": len(containers),
                "analytic_root_containers": containers,
                "residual_reason": reduction["residual_reason"],
            })
        need(
            closed == 420 and len(residual) == 128
            and digest(residual) == EXPECTED_RESIDUAL_SHA256[origin]
            and all(row["category"] == COMPACT_CATEGORY for row in residual)
            and all(row["analytic_root_container_count"] == 1 for row in residual),
            "universal 128-row containment:" + origin,
        )
        rows_out.append({
            "origin_key": origin,
            "Round176_frontier_conservation": "62=7+55",
            "Round176_preclosed_root_count": 7,
            "Round176_unresolved_root_count": 55,
            "Round180_final_child_count": 548,
            "P215_exact_behind_closed_child_count": closed,
            "analytic_residual_child_count": len(residual),
            "residual_category_count": {COMPACT_CATEGORY: len(residual)},
            "residual_container_multiplicity": {"1": len(residual)},
            "residual_rows_sha256": digest(residual),
            "residual_rows": residual,
        })
    return rows_out, roots_by_origin, next(iter(k_values))


def analytic_rebuild(q1: Any, probe: Any, roots_by_origin: dict[str, list[Any]], k: Q, frozen: dict[str, Any]) -> list[dict[str, Any]]:
    root_inputs = [{
        "origin_key": row.origin_key,
        "root_key": row.key,
        "source_chart": row.chart_id,
        "p_sign": 1 if row.box.p1 == 1 else -1,
        "active_targets": list(row.active_targets),
        "box": q1.box_row(row.box),
    } for origin in ORIGINS for row in roots_by_origin[origin]]
    origins, _cohorts, analytic = q1.analytic_census(probe, root_inputs, k)
    rebuilt_roots = analytic["root_results"]
    # C30q1-v2 renamed the misleading v1 field (which was signed on the
    # negative-p branch) into explicit signed and absolute fields.  Apply the
    # same terminology-only normalization before comparing with frozen v3.
    for row in rebuilt_roots:
        parameters = row["cohort_parameters"]
        signed = parameters.pop("derived_abs_p_endpoint_near_q0")
        parameters["derived_signed_p_endpoint_near_q0"] = signed
        parameters["derived_absolute_p_endpoint_near_q0"] = str(abs(Q(signed)))
    frozen_roots = sorted(
        (row for row in frozen["analytic_cohort_census"]["root_results"] if row["origin_key"] in ORIGINS),
        key=lambda row: row["root_key"],
    )
    need(canonical(rebuilt_roots) == canonical(frozen_roots), "target analytic roots match frozen two-seed Q1")
    need(
        len(rebuilt_roots) == 32
        and all(row["analytic_root_applicable"] is True and row["failure_reasons"] == [] for row in rebuilt_roots)
        and all(row["frozen_target"]["strict"]["ell_negative"] is True for row in rebuilt_roots)
        and all(FUTURE_TARGET in row["certified_future_witness_targets"] for row in rebuilt_roots),
        "all 32 full-r analytic root domains pass",
    )
    return origins


def rebuild() -> dict[str, Any]:
    ctx.prec = 192
    q2 = load(Q2_SOURCE, Q2_SOURCE_SHA256, "cm2_c30q2_for_q4")
    q1 = load(Q1_SOURCE, Q1_SOURCE_SHA256, "cm2_c30q1_for_q4")
    before = q1.capture_direct_pins()
    before_files = {
        name: {"sha256": row["sha256"], "file_identity": row["identity"]["file"]}
        for name, row in before.items()
    }
    frozen_document, q1_audit_hashes = q2.frozen_q1_audit()
    registry, faces, authority = q1.load_authorities()
    probe = q1.load_definitions()
    containment, roots_by_origin, k = targeted_replay(q1, probe, registry, faces)
    analytic_origins = analytic_rebuild(q1, probe, roots_by_origin, k, frozen_document["result"])
    partitions = {origin: half_open_partition(origin, roots_by_origin[origin]) for origin in ORIGINS}
    after = q1.capture_direct_pins()
    after_files = {
        name: {"sha256": row["sha256"], "file_identity": row["identity"]["file"]}
        for name, row in after.items()
    }
    # Other agents legitimately create unrelated deliverables during this
    # long replay, changing the parent-directory stat.  Each no-follow capture
    # still verifies its ancestor chain at capture time; TOCTOU stability here
    # is the byte hash and exact file identity of every selected input.
    need(before_files == after_files, "all direct input files stable across Q4 replay")
    return {
        "status": "PASS_TWO_ORIGIN_128_RESIDUAL_UNIVERSAL_CONTAINMENT__ZERO_FORMAL_CREDIT",
        "verdict": "PASS_ZERO_CREDIT_WHOLE_ORIGIN_RESEARCH_GATE",
        "scope": "two frozen 03.15.11010111 compact-q origins only",
        "frozen_inputs": {
            **authority,
            "Q1_source_sha256": Q1_SOURCE_SHA256,
            "Q2_source_sha256": Q2_SOURCE_SHA256,
            "Q1_frozen_result_sha256": q2.Q1_RESULT_SHA256,
            "Q1_audit_member_sha256": q1_audit_hashes,
            "direct_input_file_bytes_and_identity_pre_post_stable": True,
            "unrelated_parent_directory_stat_changes_ignored": True,
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
            "residual_child_count": 256,
            "all_residuals_compact_q": True,
            "all_residuals_in_exactly_one_analytic_root": True,
            "origin_rows_sha256": digest(containment),
            "origin_rows": containment,
        },
        "cross_root_half_open_partitions": partitions,
        "whole_origin_conclusion": {
            "per_origin_round176_preclosed_roots": 7,
            "per_origin_P215_exact_behind_children": 420,
            "per_origin_analytic_contained_residual_children": 128,
            "per_origin_all_16_full_r_analytic_roots_pass": True,
            "per_origin_all_255_cross_root_strata_owned": True,
            "both_origins_exclude_frozen_first_owner_everywhere": True,
            "C30q1_exactly_one_residual_requirement_shown_unnecessary_for_these_origins": True,
        },
        "strict_nonpromotion": {
            "formal_credit": 0, "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "source_W_formal_remaining": 80,
            "seal_or_release_authority": False,
            "D02": "BLOCKED", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_falsifiable_work": (
            "apply the same universal-containment criterion to the 03.15.11010101 "
            "pair, explicitly separating its 128 compact-q residuals from its "
            "eight clipped/face-overwrap residuals"
        ),
    }


def main() -> int:
    try:
        result = rebuild()
        document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except (Reject, KeyError, StopIteration, TypeError, ValueError, OSError) as error:
        print("REJECT_C30Q4_UNIVERSAL_CONTAINMENT:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
