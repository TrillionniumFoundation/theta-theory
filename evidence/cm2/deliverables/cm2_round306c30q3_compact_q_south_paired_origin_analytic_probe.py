#!/usr/bin/env python3
"""Zero-credit whole-origin theorem for the C30q2 South paired origin.

This does not infer geometry from the observed North/South key pairing.  It
binds the frozen two-seed C30q1-v3 census, selects the physical
``W:S:H.03.15.01111111`` origin, checks every one of its 16 full-r q roots,
derives the South-chart inequalities directly, and owns all cross-root
3D/2D/1D/0D strata by a deterministic half-open rule.

The result is research-only.  It grants no formal credit and changes no
ledger, seal, release gate, or CM2 claim state.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True

HERE = Path(__file__).absolute().parent
Q2_SOURCE = HERE / "cm2_round306c30q2_compact_q_exact_seven_cohort_counterexample_routing_gate.py"
Q2_SOURCE_SHA256 = "8e3beea8ab742443e028ab5e8c794a5e0f3df3467d70d0c4c3ca29e31983c125"
SCHEMA = "cm2.round306c30q3.compact-q-south-paired-origin-analytic-probe.v1"
ORIGIN = "W:S:H.03.15.01111111"
SOURCE_CHART = "W:S"
FROZEN_TARGET = "W[1,0]"
FUTURE_TARGET = "W[-1,0]"
OTHER_TARGET = "G[0,0]"
COMBINED_ROW_SHA256 = "14372ae3d265baf2064e91135323e4732729bf2a5822d35e4fa8b2da02cf2777"
ROOT_ROWS_SHA256 = "5b39174bbd8428aa73d38d94b24cf843d29eb727eaf17145837c1e8803397584"
ROOT_KEYS_SHA256 = "53f9b2d8d2ac6e5b917dcb9299d8d574ebb120683a6f4968badd2fd7f323ce47"
K = Q(1023, 262144)
RHO = Q(4, 25)
T_CUTS = tuple(Q(value) for value in (
    "-1593/16000", "-12567/128000", "-1239/12800",
    "-12213/128000", "-3009/32000", "-11859/128000",
    "-5841/64000", "-2301/25600", "-177/2000",
))
R_CUTS = (Q(0), Q(1))
S_CUTS = (Q(-1, 400), Q(0), Q(1, 400))


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_q2() -> Any:
    raw = Q2_SOURCE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == Q2_SOURCE_SHA256, "Q2 source pin")
    specification = importlib.util.spec_from_file_location("cm2_c30q2_for_q3", Q2_SOURCE)
    need(specification is not None and specification.loader is not None, "Q2 import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == Q2_SOURCE, "Q2 imported identity")
    need(hashlib.sha256(Q2_SOURCE.read_bytes()).hexdigest() == Q2_SOURCE_SHA256, "Q2 source stable")
    return module


def fraction_pair(values: list[str]) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2, "rational interval shape")
    pair = Q(values[0]), Q(values[1])
    need(pair[0] < pair[1], "strict rational interval")
    return pair


def frozen_origin(q2: Any) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str]]:
    document, audit_hashes = q2.frozen_q1_audit()
    result = document["result"]
    combined = result["combined_origin_gate"]["origin_rows"]
    selected = [row for row in combined if row["origin_key"] == ORIGIN]
    need(len(selected) == 1, "unique South origin in Q1")
    origin = selected[0]
    roots = sorted(
        (row for row in result["analytic_cohort_census"]["root_results"]
         if row["origin_key"] == ORIGIN),
        key=lambda row: row["root_key"],
    )
    need(digest(origin) == COMBINED_ROW_SHA256, "South combined-row pin")
    need(digest(roots) == ROOT_ROWS_SHA256, "South root-row pin")
    need(digest([row["root_key"] for row in roots]) == ROOT_KEYS_SHA256, "South root-key pin")
    return origin, roots, audit_hashes


def root_boxes(roots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    boxes: list[dict[str, Any]] = []
    actual: set[tuple[Q, Q, Q, Q]] = set()
    expected = {
        (T_CUTS[index], T_CUTS[index + 1], S_CUTS[side], S_CUTS[side + 1])
        for index in range(8) for side in range(2)
    }
    for row in roots:
        params = row["cohort_parameters"]
        t0, t1 = fraction_pair(params["exact_t_domain"])
        s0, s1 = fraction_pair(params["exact_s_domain"])
        need(
            params["source_chart"] == SOURCE_CHART
            and params["p_sign"] == -1
            and params["active_target_set"] == [OTHER_TARGET, FUTURE_TARGET]
            and params["exact_r_domain"] == ["0", "1"]
            and params["exact_q_squared_scale"] == str(K)
            and params["exact_p_parameterization"] == "-sqrt(1-(1023/262144)*r^2)"
            and params["source_p_endpoint_domain"] == ["-1", "-511/512"]
            and row["analytic_root_applicable"] is True
            and row["failure_reasons"] == []
            and row["frozen_target"]["target"] == FROZEN_TARGET
            and row["frozen_target"]["strict"]["f_at_0_positive"] is True
            and row["frozen_target"]["strict"]["ell_negative"] is True
            and row["certified_future_witness_targets"] == [FUTURE_TARGET],
            "direct South root theorem input:" + row["root_key"],
        )
        future = next(item for item in row["future_targets"] if item["target"] == FUTURE_TARGET)
        need(
            future["target_definition"] == {"ix": -1, "iy": 0, "obstacle": "W", "radius": "4/25"}
            and all(future["strict"][key] is True for key in (
                "f_at_0_positive", "f_at_1_negative",
                "transverse_margin_positive", "discriminant_positive",
            )),
            "direct South future-root checks:" + row["root_key"],
        )
        need(
            row["frozen_target"]["target_definition"]
            == {"ix": 1, "iy": 0, "obstacle": "W", "radius": "4/25"},
            "direct South frozen-target definition:" + row["root_key"],
        )
        actual.add((t0, t1, s0, s1))
        boxes.append({
            "root_key": row["root_key"],
            "t": [str(t0), str(t1)], "r": ["0", "1"],
            "s": [str(s0), str(s1)],
        })
    need(len(boxes) == 16 and actual == expected, "exact South 8x1x2 root product")
    return boxes


def axis_atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    need(tuple(sorted(set(cuts))) == cuts, "ordered atomic cuts")
    atoms: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        atoms.append(("POINT", point, point))
        if index + 1 < len(cuts):
            atoms.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return atoms


def partition(boxes: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = [{
        "root_key": box["root_key"],
        "t": tuple(Q(x) for x in box["t"]),
        "r": tuple(Q(x) for x in box["r"]),
        "s": tuple(Q(x) for x in box["s"]),
    } for box in boxes]
    rows: list[dict[str, Any]] = []
    for ta in axis_atoms(T_CUTS):
        for ra in axis_atoms(R_CUTS):
            for sa in axis_atoms(S_CUTS):
                atom = {"t": ta, "r": ra, "s": sa}
                incidents: list[str] = []
                for box in parsed:
                    if all(
                        box[axis][0] <= data[1] <= data[2] <= box[axis][1]
                        for axis, data in atom.items()
                    ):
                        incidents.append(box["root_key"])
                incidents.sort()
                need(bool(incidents), "atomic stratum incident root")
                geometry = {
                    axis: ({"kind": data[0], "value": str(data[1])}
                           if data[0] == "POINT" else
                           {"kind": data[0], "lower": str(data[1]), "upper": str(data[2])})
                    for axis, data in atom.items()
                }
                rows.append({
                    "ambient_dimension": sum(data[0] == "OPEN_INTERVAL" for data in atom.values()),
                    "geometry": geometry,
                    "incident_root_keys": incidents,
                    "owner_root_key": incidents[0],
                    "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    dimensions = Counter(row["ambient_dimension"] for row in rows)
    owners = Counter(row["owner_root_key"] for row in rows)
    need(
        len(rows) == 255
        and dimensions == Counter({3: 16, 2: 74, 1: 111, 0: 54})
        and set(owners) == {box["root_key"] for box in boxes}
        and all(row["owner_root_key"] == min(row["incident_root_keys"]) for row in rows),
        "South complete 3D/2D/1D/0D partition",
    )
    return {
        "rule": "lexicographically least incident South root owns each relative-open product stratum",
        "root_box_count": 16,
        "atomic_stratum_count": 255,
        "atomic_stratum_count_by_dimension": {str(k): dimensions[k] for k in (3, 2, 1, 0)},
        "owner_root_count": len(owners),
        "owner_assignment_rows_sha256": digest(rows),
        "all_strata_owned_exactly_once": True,
        "all_analytic_dispositions_inherit_on_boundaries": True,
    }


def exact_theorem() -> dict[str, Any]:
    t0, t1 = T_CUTS[0], T_CUTS[-1]
    p2 = Q(255, 256)
    a2 = Q(63, 64)
    pa2 = p2 * a2
    plus0, plus1 = t0 + RHO, t1 + RHO
    ell_lower = Q(1, 2) - Q(1, 16) * plus1
    transverse_upper = Q(1, 16) + plus1
    radius_margin = RHO - transverse_upper
    f0_left_lower = Q(1) + 2 * RHO * t0
    need(
        K < Q(1, 256) and max(abs(t0), abs(t1)) < Q(1, 8)
        and pa2 > Q(1, 4)
        and (plus0, plus1) == (Q(967, 16000), Q(143, 2000))
        and ell_lower == Q(15857, 32000)
        and transverse_upper == Q(67, 500)
        and radius_margin == Q(13, 500)
        and f0_left_lower == Q(48407, 50000),
        "exact South rational margins",
    )
    return {
        "direct_physical_coordinates_not_key_pair_inference": {
            "normal": "n_S=(t,-a), a=sqrt(1-t^2)>0",
            "velocity": "u_S=(q*t-P*a,-q*a-P*t), P=sqrt(1-q^2)>0",
            "source_point": "(1/2+s+rho*t,1/2-rho*a), rho=4/25",
            "frozen_displacement": "d_F=(1-rho*t,rho*a)",
            "future_displacement": "d_L=(-1-rho*t,rho*a)",
            "direct_dot_product_frozen": "u_S dot d_F=q*(t-rho)-P*a",
            "direct_dot_product_future": "u_S dot d_L=P*a-q*(t+rho)",
            "south_target_registry_checked_on_all_16_roots": True,
        },
        "exact_domain": {
            "origin_key": ORIGIN, "source_chart": SOURCE_CHART, "p_sign": -1,
            "t": [str(t0), str(t1)], "r": ["0", "1"],
            "s": [str(S_CUTS[0]), str(S_CUTS[-1])],
            "q": "sqrt(1023/262144)*r",
            "p": "-sqrt(1-(1023/262144)*r^2)",
        },
        "coarse_exact_witnesses": {
            "q_squared_exact_maximum": str(K),
            "q_squared_strict_upper": "1/256",
            "absolute_t_strict_upper": "1/8",
            "P_squared_strict_lower": str(p2),
            "a_squared_strict_lower": str(a2),
            "P_times_a_squared_strict_lower": str(pa2),
            "P_times_a_strict_lower": "1/2",
        },
        "frozen_target_strictly_behind": {
            "target": FROZEN_TARGET,
            "forward_projection": "q*(t-4/25)-P*a",
            "uniform_strict_upper": "-1/2",
            "future_root_possible": False,
        },
        "certified_nonfrozen_strict_future_root": {
            "target": FUTURE_TARGET,
            "forward_projection": "P*a-q*(t+4/25)",
            "forward_projection_strict_lower": str(ell_lower),
            "absolute_transverse_strict_upper": str(transverse_upper),
            "target_radius": str(RHO),
            "radius_minus_absolute_transverse_strict_lower": str(radius_margin),
            "center_distance_squared_minus_target_radius_squared_strict_lower": str(f0_left_lower),
            "discriminant_strictly_positive": True,
            "near_root_strictly_positive_and_less_than_one": True,
        },
        "whole_origin_logic": {
            "all_16_full_r_root_domains_covered": True,
            "all_cross_root_dimensions_owned": [3, 2, 1, 0],
            "one_nonfrozen_future_collision_exists_everywhere": True,
            "frozen_target_has_no_future_root_everywhere": True,
            "nonfrozen_ties_do_not_change_frozen-owner_exclusion": True,
            "whole_origin_excludes_frozen_first_owner": True,
        },
    }


def rebuild() -> dict[str, Any]:
    q2 = load_q2()
    origin, roots, audit_hashes = frozen_origin(q2)
    boxes = root_boxes(roots)
    complement = origin["complement"]
    need(
        origin["conditional_origin_applicable"] is True
        and origin["rejection_reasons"] == []
        and complement["P215_residual_child_count"] == 1
        and complement["P215_exact_behind_closed_child_count"] == 327
        and complement["unique_compact_residual_in_exactly_one_root_box"] is True
        and len(complement["residual_witnesses"]) == 1
        and complement["residual_witnesses"][0]["analytic_root_container_count"] == 1,
        "South non-q complement plus unique q residual binding",
    )
    return {
        "status": "PASS_SOUTH_PAIRED_ORIGIN_WHOLE_ORIGIN_ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT",
        "verdict": "PASS_ZERO_CREDIT_RESEARCH_THEOREM",
        "scope": "one independently checked South compact-q origin only",
        "frozen_inputs": {
            "Q2_source_sha256": Q2_SOURCE_SHA256,
            "Q1_frozen_result_sha256": q2.Q1_RESULT_SHA256,
            "Q1_frozen_stdout_sha256": q2.Q1_STDOUT_SHA256,
            "Q1_audit_member_sha256": audit_hashes,
            "South_combined_row_sha256": COMBINED_ROW_SHA256,
            "South_root_rows_sha256": ROOT_ROWS_SHA256,
        },
        "selected_origin": {
            "origin_key": ORIGIN,
            "root_count": len(boxes),
            "root_keys_sha256": ROOT_KEYS_SHA256,
            "root_boxes": boxes,
            "pinned_complement_sha256": digest(complement),
            "pinned_complement_exact_behind_closed_child_count": 327,
            "pinned_complement_unique_q_residual_child_count": 1,
        },
        "analytic_whole_origin_certificate": exact_theorem(),
        "cross_root_half_open_partition": partition(boxes),
        "strict_nonpromotion": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "compact_q_formal_remaining_origins": 54,
            "source_W_formal_remaining": 80,
            "seal_or_release_authority": False,
            "D02": "BLOCKED", "D03": "UNAUTHORIZED", "D04": "NOT_MINTED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_falsifiable_work": (
            "independently verify and attack this South theorem; then derive a "
            "parameter-level route for one of the four blocked fully-analytic "
            "cohort-7 origins without extrapolating from this paired case"
        ),
    }


def main() -> int:
    try:
        result = rebuild()
        document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except (Reject, StopIteration, KeyError, TypeError, ValueError) as error:
        print("REJECT_C30Q3_SOUTH_THEOREM:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
