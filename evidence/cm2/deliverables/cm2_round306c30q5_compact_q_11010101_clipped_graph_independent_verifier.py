#!/usr/bin/env python3
"""Independent verifier for the zero-credit C30q5 clipped-graph gate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

from flint import arb, ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
PRODUCER = (
    HERE / "cm2_round306c30q5_compact_q_11010101_clipped_graph_gate.py"
)
PRODUCER_SHA256 = (
    "ba6ee02b1e4910762f242bebc8697c389d789a12be21d0e57761f81e5be06972"
)
Q2_SOURCE = (
    HERE
    / "cm2_round306c30q2_compact_q_exact_seven_cohort_"
      "counterexample_routing_gate.py"
)
Q2_SOURCE_SHA256 = (
    "8e3beea8ab742443e028ab5e8c794a5e0f3df3467d70d0c4c3ca29e31983c125"
)
SCHEMA = "cm2.round306c30q5.compact-q-11010101-clipped-graph-gate.v1"
EXPECTED_RESULT_SHA256 = (
    "dcfb2b96903d1cbae3530c66660f4d30a033d3499e5ea9858ddc5011ea10797e"
)
ORIGINS = ("W:N:03.15.11010101", "W:S:H.03.15.11010101")
COMPACT = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
EXPECTED_TARGET = {
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
R_G = Q(9, 25)
R_W = Q(4, 25)


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


def strict_json(raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_float=lambda token:
                (_ for _ in ()).throw(ValueError(token)),
            parse_constant=lambda token:
                (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict candidate JSON") from error
    need(
        type(value) is dict
        and raw in {canonical(value), canonical(value) + b"\n"},
        "canonical candidate JSON",
    )
    return value


def load_q2() -> Any:
    need(hashlib.sha256(Q2_SOURCE.read_bytes()).hexdigest()
         == Q2_SOURCE_SHA256, "Q2 source pin")
    specification = importlib.util.spec_from_file_location(
        "cm2_c30q2_for_q5_independent_verifier", Q2_SOURCE
    )
    need(specification is not None and specification.loader is not None,
         "Q2 import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == Q2_SOURCE,
         "Q2 import identity")
    return module


def pair(values: list[str], label: str) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2,
         "interval shape:" + label)
    result = Q(values[0]), Q(values[1])
    need(result[0] < result[1]
         and [str(result[0]), str(result[1])] == values,
         "canonical interval:" + label)
    return result


def roots_from_frozen(
    frozen: dict[str, Any], origin: str
) -> list[dict[str, Any]]:
    rows = sorted(
        (row for row in frozen["analytic_cohort_census"]["root_results"]
         if row["origin_key"] == origin),
        key=lambda row: row["root_key"],
    )
    need(
        len(rows) == 16
        and all(row["analytic_root_applicable"] is True
                and row["failure_reasons"] == [] for row in rows)
        and all(row["frozen_target"]["strict"]["ell_negative"] is True
                for row in rows)
        and all("W[-1,0]" in row["certified_future_witness_targets"]
                for row in rows),
        "frozen 16-root analytic theorem:" + origin,
    )
    output: list[dict[str, Any]] = []
    for row in rows:
        parameters = row["cohort_parameters"]
        output.append({
            "root_key": row["root_key"],
            "t": pair(parameters["exact_t_domain"], "root t"),
            "p": pair(parameters["source_p_endpoint_domain"], "root p"),
            "s": pair(parameters["exact_s_domain"], "root s"),
        })
    return output


def contains(child: dict[str, tuple[Q, Q]], root: dict[str, Any]) -> bool:
    return all(
        root[axis][0] <= child[axis][0]
        <= child[axis][1] <= root[axis][1]
        for axis in ("t", "p", "s")
    )


def atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    need(tuple(sorted(set(cuts))) == cuts, "strict partition cuts")
    output: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        output.append(("POINT", point, point))
        if index + 1 < len(cuts):
            output.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return output


def partition_hash(roots: list[dict[str, Any]]) -> str:
    t_cuts = tuple(sorted({value for root in roots for value in root["t"]}))
    s_cuts = tuple(sorted({value for root in roots for value in root["s"]}))
    r_cuts = (Q(0), Q(1))
    need(len(t_cuts) == 9
         and s_cuts == (Q(-1, 400), Q(0), Q(1, 400)),
         "root partition cuts")
    rows: list[dict[str, Any]] = []
    for ta in atoms(t_cuts):
        for ra in atoms(r_cuts):
            for sa in atoms(s_cuts):
                incident = sorted(
                    root["root_key"] for root in roots
                    if root["t"][0] <= ta[1] <= ta[2] <= root["t"][1]
                    and root["s"][0] <= sa[1] <= sa[2] <= root["s"][1]
                )
                need(bool(incident), "partition atom incident")
                axes = {"t": ta, "r": ra, "s": sa}
                geometry = {
                    key: (
                        {"kind": item[0], "value": str(item[1])}
                        if item[0] == "POINT"
                        else {"kind": item[0], "lower": str(item[1]),
                              "upper": str(item[2])}
                    ) for key, item in axes.items()
                }
                rows.append({
                    "ambient_dimension": sum(
                        item[0] == "OPEN_INTERVAL" for item in axes.values()
                    ),
                    "geometry": geometry,
                    "incident_root_keys": incident,
                    "owner_root_key": incident[0],
                    "analytic_disposition":
                        "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    need(
        len(rows) == 255
        and Counter(row["ambient_dimension"] for row in rows)
            == Counter({3: 16, 2: 74, 1: 111, 0: 54}),
        "partition dimensions",
    )
    return digest(rows)


def arbq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "arb interval order")
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return arbq(middle) + arb(0, arbq(radius).upper())


def bounds(value: arb) -> dict[str, str]:
    return {
        "enclosure": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def clipped_geometry(
    origin: str, box: dict[str, tuple[Q, Q]]
) -> dict[str, Any]:
    north = origin.startswith("W:N:")
    need(box["t"] == T_DOMAIN, "clipped t domain:" + origin)
    expected_p = (
        (P_INNER, P_SHARED) if north else (-P_SHARED, -P_INNER)
    )
    need(box["p"] == expected_p, "clipped p domain:" + origin)
    t = arb_interval(*box["t"])
    s = arb_interval(*box["s"])
    P = arb_interval(P_INNER, P_SHARED)
    a = (arb(1) - t * t).sqrt()
    b = (arb(1) - P * P).sqrt()
    u = arbq(Q(1, 2)) + s
    A = a * u + t / 2
    B = t * u - a / 2 + arbq(R_W)
    ell_G = P * A - b * B
    h = b * A + P * B
    Delta_G = arbq(R_G) * arbq(R_G) - h * h
    dh_dP = B - (P / b) * A
    dDelta_dP = -2 * h * dh_dP
    signed_derivative = dDelta_dP if north else -dDelta_dP

    ell_W = P * a - b * (t + arbq(R_W))
    transverse_W = b * a + P * (t + arbq(R_W))
    Delta_W = arbq(R_W) * arbq(R_W) - transverse_W * transverse_W
    need(bool(Delta_W > 0), "competitor discriminant:" + origin)
    near_W = ell_W - Delta_W.sqrt()
    order_margin = near_W - ell_G
    need(
        bool(A > 0) and bool(B < 0) and bool(h < 0)
        and bool(dh_dP < 0)
        and bool(ell_G - arbq(R_G) > 0)
        and bool(near_W > 0)
        and bool(order_margin > 0)
        and not bool(Delta_G > 0) and not bool(Delta_G < 0)
        and (bool(signed_derivative < 0) if north
             else bool(signed_derivative > 0)),
        "independent clipped graph inequalities:" + origin,
    )
    return {
        "A": bounds(A),
        "B": bounds(B),
        "ell_G": bounds(ell_G),
        "ell_G_minus_radius": bounds(ell_G - arbq(R_G)),
        "Delta_G": bounds(Delta_G),
        "dh_dP": bounds(dh_dP),
        "dDelta_dp": bounds(signed_derivative),
        "near_W_minus_ell_G": bounds(order_margin),
    }


def p_star(t_value: Q, s_value: Q) -> tuple[arb, arb]:
    t, s = arbq(t_value), arbq(s_value)
    a = (arb(1) - t * t).sqrt()
    u = arbq(Q(1, 2)) + s
    A = a * u + t / 2
    B = t * u - a / 2 + arbq(R_W)
    radius = arbq(R_G)
    D = A * A + B * B - radius * radius
    need(bool(A > 0) and bool(B < 0) and bool(D > 0),
         "point graph branch guards")
    denominator = A * A + B * B
    correct = (-radius * B + A * D.sqrt()) / denominator
    extraneous = (-radius * B - A * D.sqrt()) / denominator
    b = (arb(1) - correct * correct).sqrt()
    residual = b * A + correct * B + radius
    need(
        bool(arbq(P_INNER) < correct) and bool(correct < arb(1))
        and bool(extraneous < arbq(P_INNER))
        and not bool(residual > 0) and not bool(residual < 0),
        "correct unsquared root / extraneous rejection",
    )
    return correct, extraneous


def verify_common_graph(result: dict[str, Any]) -> dict[str, Any]:
    section = result["clipped_graph_three_stratum_closure"][
        "exact_common_graph_certificate"
    ]
    below, below_spurious = p_star(T_DOMAIN[0], S_DOMAIN[0])
    above, above_spurious = p_star(T_DOMAIN[1], S_DOMAIN[1])
    need(
        bool(below < arbq(P_SHARED))
        and bool(above > arbq(P_SHARED))
        and section["correct_unsquared_branch"] == "b*A+P*B=-9/25"
        and section["shared_face_falsification"]
            ["graph_crosses_shared_abs_p_face"] is True
        and section["shared_face_falsification"]
            ["full_p_graph_claim"] is False
        and section["branch_guards"]["squared_extraneous_branch_rejected"]
            is True,
        "independent common graph branch/face crossing",
    )
    return {
        "below_shared_face_P_star": bounds(below),
        "above_shared_face_P_star": bounds(above),
        "below_extraneous_quadratic_root": bounds(below_spurious),
        "above_extraneous_quadratic_root": bounds(above_spurious),
        "shared_face_crossed": True,
        "extraneous_squared_branch_rejected": True,
    }


def outer_ledger(graph_rows: list[dict[str, Any]]) -> dict[str, Any]:
    axes = ("t", "p", "s")
    graph_map: dict[str, str] = {}
    face_map: dict[str, str] = {}
    edge_map: dict[str, str] = {}
    corner_map: dict[str, str] = {}
    for row in graph_rows:
        bounds_by_axis = tuple(pair(row["box"][axis], "outer " + axis)
                               for axis in axes)
        chart = "W:N" if row["origin_key"].startswith("W:N:") else "W:S"
        target = EXPECTED_TARGET[row["origin_key"]]
        graph = {
            "chart": chart,
            "target": target,
            "box": {
                axes[index]: [str(value) for value in bounds_by_axis[index]]
                for index in range(3)
            },
            "predicate": "Delta=0",
            "dimension": 2,
            "existence": "OUTER_ONLY",
        }
        graph_key = canonical(graph).decode()
        graph_map[graph_key] = min(
            graph_map.get(graph_key, row["cell_key"]), row["cell_key"]
        )
        for axis_index, axis in enumerate(axes):
            free = [index for index in range(3) if index != axis_index]
            for endpoint in bounds_by_axis[axis_index]:
                face = {
                    "chart": chart,
                    "target": target,
                    "fixed": {axis: str(endpoint)},
                    "spans": {
                        axes[index]: [str(value)
                                      for value in bounds_by_axis[index]]
                        for index in free
                    },
                    "predicate": "Delta=0",
                    "dimension": 1,
                    "existence": "OUTER_ONLY",
                }
                key = canonical(face).decode()
                face_map[key] = min(
                    face_map.get(key, row["cell_key"]), row["cell_key"]
                )
        for free_index in range(3):
            fixed = [index for index in range(3) if index != free_index]
            for first in bounds_by_axis[fixed[0]]:
                for second in bounds_by_axis[fixed[1]]:
                    edge = {
                        "chart": chart,
                        "target": target,
                        "fixed": {
                            axes[fixed[0]]: str(first),
                            axes[fixed[1]]: str(second),
                        },
                        "span": {
                            axes[free_index]: [
                                str(value)
                                for value in bounds_by_axis[free_index]
                            ]
                        },
                        "predicate": "Delta=0",
                        "dimension": 0,
                        "existence": "OUTER_ONLY",
                    }
                    key = canonical(edge).decode()
                    edge_map[key] = min(
                        edge_map.get(key, row["cell_key"]), row["cell_key"]
                    )
        for t_value in bounds_by_axis[0]:
            for p_value in bounds_by_axis[1]:
                for s_value in bounds_by_axis[2]:
                    corner = {
                        "chart": chart,
                        "target": target,
                        "point": {"t": str(t_value), "p": str(p_value),
                                  "s": str(s_value)},
                        "predicate": "Delta=0",
                        "dimension": 0,
                        "existence": "OUTER_ONLY",
                    }
                    key = canonical(corner).decode()
                    corner_map[key] = min(
                        corner_map.get(key, row["cell_key"]), row["cell_key"]
                    )

    def owned(values: dict[str, str]) -> list[dict[str, Any]]:
        return [{"outer": json.loads(key), "half_open_owner": owner}
                for key, owner in sorted(values.items())]

    graphs, faces = owned(graph_map), owned(face_map)
    edges, corners = owned(edge_map), owned(corner_map)
    return {
        "2D_Delta_graph_outer_count": len(graphs),
        "2D_Delta_graph_outer_rows_sha256": digest(graphs),
        "1D_graph_face_outer_count": len(faces),
        "1D_graph_face_outer_rows_sha256": digest(faces),
        "0D_graph_edge_outer_count": len(edges),
        "0D_graph_edge_outer_rows_sha256": digest(edges),
        "0D_graph_corner_candidate_count": len(corners),
        "0D_graph_corner_candidate_rows_sha256": digest(corners),
        "half_open_owner":
            "lexicographically least incident closed child key",
        "outer_proof_status": "ALL_EXCLUDED",
        "all_outer_strata_inherit_EXCLUDED_graph_proof": True,
        "outer_counts_are_not_nonempty_component_counts": True,
    }


def verify(raw: bytes) -> dict[str, Any]:
    ctx.prec = 256
    need(hashlib.sha256(PRODUCER.read_bytes()).hexdigest()
         == PRODUCER_SHA256, "producer source pin")
    candidate = strict_json(raw)
    need(
        set(candidate) == {"schema", "result", "result_sha256"}
        and candidate["schema"] == SCHEMA,
        "candidate top-level",
    )
    result = candidate["result"]
    need(candidate["result_sha256"] == digest(result)
         == EXPECTED_RESULT_SHA256, "candidate result closure/pin")
    q2 = load_q2()
    frozen_document, _audit = q2.frozen_q1_audit()
    frozen = frozen_document["result"]
    frozen_origins = {
        row["origin_key"]: row
        for row in frozen["combined_origin_gate"]["origin_rows"]
    }
    candidate_origins = {
        row["origin_key"]: row
        for row in result["universal_residual_containment"]["origin_rows"]
    }
    need(set(candidate_origins) == set(ORIGINS), "candidate origin set")
    graph_rows = result["clipped_graph_three_stratum_closure"]["graph_rows"]
    graph_by_key = {row["cell_key"]: row for row in graph_rows}
    need(len(graph_rows) == len(graph_by_key) == 16,
         "candidate graph row set")

    checked: list[dict[str, Any]] = []
    all_clipped_keys: set[str] = set()
    geometry_rows: list[dict[str, Any]] = []
    for origin in ORIGINS:
        frozen_origin = frozen_origins[origin]
        row = candidate_origins[origin]
        need(
            frozen_origin["analytic"]["all_analytic_roots_applicable"]
                is True
            and frozen_origin["complement"]
                ["P215_exact_behind_closed_child_count"] == 418
            and frozen_origin["complement"]
                ["P215_residual_child_count"] == 136
            and frozen_origin["complement"]["residual_rows_sha256"]
                == EXPECTED_RESIDUAL_SHA256[origin],
            "frozen complement authority:" + origin,
        )
        roots = roots_from_frozen(frozen, origin)
        residual = row["residual_rows"]
        need(
            len(residual) == len({item["cell_key"] for item in residual})
                == 136
            and digest(residual) == row["residual_rows_sha256"]
                == EXPECTED_RESIDUAL_SHA256[origin]
            and Counter(item["category"] for item in residual)
                == Counter({COMPACT: 128, CLIPPED: 8}),
            "candidate residual ledger closure:" + origin,
        )
        clipped_rows: list[dict[str, Any]] = []
        for item in residual:
            child = {axis: pair(item["box"][axis], "child " + axis)
                     for axis in ("t", "p", "s")}
            containers = sorted(
                root["root_key"] for root in roots
                if contains(child, root)
            )
            need(
                item["analytic_root_container_count"] == 1
                and item["analytic_root_containers"] == containers
                and len(containers) == 1,
                "independent universal containment:" + item["cell_key"],
            )
            if item["category"] == CLIPPED:
                clipped_rows.append(item)
                all_clipped_keys.add(item["cell_key"])
                graph = graph_by_key[item["cell_key"]]
                proof = graph["three_stratum_proof"]
                proof_without_hash = {
                    key: value for key, value in proof.items()
                    if key != "proof_sha256"
                }
                need(
                    item["active_targets"]
                        == [EXPECTED_TARGET[origin], "W[-1,0]"]
                    and item["residual_reason"]
                        == "NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE"
                    and graph["origin_key"] == origin
                    and graph["box"] == item["box"]
                    and graph["active_targets"] == item["active_targets"]
                    and graph["analytic_root_container"] == containers[0]
                    and proof["proof_sha256"] == digest(proof_without_hash)
                    and proof["origin_key"] == origin
                    and proof["cell_key"] == item["cell_key"]
                    and proof["target"] == EXPECTED_TARGET[origin]
                    and proof["graph_owner_target"]
                        == EXPECTED_TARGET[origin]
                    and proof["frozen_owner"] == "W[1,0]"
                    and proof["strict_p_derivative_sign"]
                        == EXPECTED_DERIVATIVE[origin]
                    and proof["full_p_graph"] is False
                    and proof["target_strict_positive_first_on_closed_outer"]
                        is True
                    and proof["Delta_negative_open_3D_disposition"]
                        == "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
                    and proof["Delta_zero_2D_graph_disposition"]
                        == "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
                    and proof["Delta_positive_open_3D_disposition"]
                        == "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
                    and proof["all_three_strata_excluded"] is True
                    and proof["whole_closed_cell_excluded"] is True,
                    "independent three-stratum semantics:" + item["cell_key"],
                )
                geometry_rows.append({
                    "cell_key": item["cell_key"],
                    "inequalities": clipped_geometry(origin, child),
                })
        expected_s_pairs = [
            (S_DOMAIN[0] + Q(index, 1600),
             S_DOMAIN[0] + Q(index + 1, 1600))
            for index in range(8)
        ]
        expected_s = [[str(a), str(b)] for a, b in expected_s_pairs]
        actual_s_pairs = sorted(
            pair(item["box"]["s"], "clipped s bin")
            for item in clipped_rows
        )
        need(
            len(clipped_rows) == 8
            and actual_s_pairs == expected_s_pairs
            and row["clipped_s_bins"] == expected_s,
            "exact clipped eight-bin cover:" + origin,
        )
        rebuilt_partition = partition_hash(roots)
        need(
            result["cross_root_half_open_partitions"][origin]
                ["owner_assignment_rows_sha256"] == rebuilt_partition,
            "independent root partition:" + origin,
        )
        checked.append({
            "origin_key": origin,
            "analytic_root_count": 16,
            "residual_child_count": 136,
            "compact_q_child_count": 128,
            "clipped_graph_child_count": 8,
            "residual_rows_sha256": EXPECTED_RESIDUAL_SHA256[origin],
            "partition_sha256": rebuilt_partition,
        })

    need(all_clipped_keys == set(graph_by_key),
         "graph/residual exact key equality")
    rebuilt_outer = outer_ledger(graph_rows)
    need(
        rebuilt_outer == result["clipped_graph_three_stratum_closure"]
            ["analytic_outer_half_open_ledger"]
        and rebuilt_outer["2D_Delta_graph_outer_count"] == 16
        and rebuilt_outer["1D_graph_face_outer_count"] == 82
        and rebuilt_outer["0D_graph_edge_outer_count"] == 136
        and rebuilt_outer["0D_graph_corner_candidate_count"] == 72,
        "independent graph outer half-open ledger",
    )
    common = verify_common_graph(result)
    need(
        result["status"] == (
            "PASS_TWO_ORIGIN_136_RESIDUAL_CONTAINMENT_AND_16_CLIPPED_GRAPH_"
            "CLOSURE__ZERO_FORMAL_CREDIT"
        )
        and result["universal_residual_containment"]
            ["residual_child_count"] == 272
        and result["whole_origin_conclusion"]
            ["both_origins_exclude_frozen_first_owner_everywhere"] is True
        and result["whole_origin_conclusion"]
            ["graph_uniformly_inside_clipped_slab"] is False,
        "candidate conclusion",
    )
    boundary = result["strict_nonpromotion"]
    need(
        boundary["formal_credit"] == 0
        and boundary["ledger_unchanged"] is True
        and boundary["compact_q_formal_remaining_origins"] == 54
        and boundary["source_W_formal_remaining"] == 80
        and boundary["seal_or_release_authority"] is False
        and boundary["D02"] == "BLOCKED"
        and boundary["CM2"] == "NO-GO_FOR_CLAIM",
        "candidate strict nonpromotion",
    )
    return {
        "origin_count": 2,
        "analytic_root_count": 32,
        "residual_child_count": 272,
        "clipped_graph_child_count": 16,
        "checked_origins": checked,
        "geometry_rows_sha256": digest(geometry_rows),
        "outer_half_open_ledger": rebuilt_outer,
        "common_graph_reconstruction": common,
        "formal_credit": 0,
    }


def main() -> int:
    try:
        raw = (
            sys.stdin.buffer.read()
            if len(sys.argv) == 1 or sys.argv[1] == "-"
            else Path(sys.argv[1]).read_bytes()
        )
        reconstruction = verify(raw)
        output = {
            "schema": (
                "cm2.round306c30q5.compact-q-11010101-clipped-graph-"
                "independent-verification.v1"
            ),
            "status": (
                "PASS_INDEPENDENT_C30Q5_272_CONTAINMENTS_AND_16_GRAPH_"
                "CLOSURES__ZERO_FORMAL_CREDIT"
            ),
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "reconstruction": reconstruction,
            "formal_credit": 0,
            "compact_q_formal_remaining_origins": 54,
            "source_W_formal_remaining": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, KeyError, StopIteration, TypeError, ValueError, OSError) as error:
        print(
            "REJECT_C30Q5_INDEPENDENT_VERIFICATION:" + str(error),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
