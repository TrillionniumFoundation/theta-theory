#!/usr/bin/env python3
"""Independent verifier for the zero-credit C30q3 South theorem."""

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
PRODUCER = HERE / "cm2_round306c30q3_compact_q_south_paired_origin_analytic_probe.py"
PRODUCER_SHA256 = "364280a41b868ba1fd3b83b849506040b44af836e2065cd17cc9ef5846673975"
Q2_SOURCE = HERE / "cm2_round306c30q2_compact_q_exact_seven_cohort_counterexample_routing_gate.py"
Q2_SOURCE_SHA256 = "8e3beea8ab742443e028ab5e8c794a5e0f3df3467d70d0c4c3ca29e31983c125"
SCHEMA = "cm2.round306c30q3.compact-q-south-paired-origin-analytic-probe.v1"
EXPECTED_RESULT_SHA256 = "cb94ca0f794627673ed3e24416e92162056270fe46475a6223e68982b26d5479"
ORIGIN = "W:S:H.03.15.01111111"
COMBINED_SHA256 = "14372ae3d265baf2064e91135323e4732729bf2a5822d35e4fa8b2da02cf2777"
ROOTS_SHA256 = "5b39174bbd8428aa73d38d94b24cf843d29eb727eaf17145837c1e8803397584"
PARTITION_SHA256 = "8c4a508be3f582596302a40ae9a9f482646118aefe6e109ebb6946529f648416"
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
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_document(raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate candidate key")
            out[key] = value
        return out
    try:
        value = json.loads(
            raw.decode(), object_pairs_hook=unique,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict candidate JSON") from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"}, "canonical candidate")
    return value


def load_q2() -> Any:
    need(hashlib.sha256(Q2_SOURCE.read_bytes()).hexdigest() == Q2_SOURCE_SHA256, "Q2 source pin")
    specification = importlib.util.spec_from_file_location("cm2_c30q2_for_q3_verifier", Q2_SOURCE)
    need(specification is not None and specification.loader is not None, "Q2 import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == Q2_SOURCE, "Q2 import identity")
    return module


def atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    result: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        result.append(("POINT", point, point))
        if index + 1 < len(cuts):
            result.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return result


def independent_partition(roots: list[dict[str, Any]]) -> tuple[str, Counter[int]]:
    boxes: list[dict[str, Any]] = []
    rectangles: set[tuple[Q, Q, Q, Q]] = set()
    for row in roots:
        params = row["cohort_parameters"]
        t0, t1 = map(Q, params["exact_t_domain"])
        s0, s1 = map(Q, params["exact_s_domain"])
        rectangles.add((t0, t1, s0, s1))
        boxes.append({"root_key": row["root_key"], "t": (t0, t1), "r": R_CUTS, "s": (s0, s1)})
    expected = {
        (T_CUTS[i], T_CUTS[i + 1], S_CUTS[j], S_CUTS[j + 1])
        for i in range(8) for j in range(2)
    }
    need(rectangles == expected and len(boxes) == 16, "independent exact root tiling")
    rows: list[dict[str, Any]] = []
    for ta in atoms(T_CUTS):
        for ra in atoms(R_CUTS):
            for sa in atoms(S_CUTS):
                axis = {"t": ta, "r": ra, "s": sa}
                incident = sorted(
                    box["root_key"] for box in boxes
                    if all(box[key][0] <= item[1] <= item[2] <= box[key][1] for key, item in axis.items())
                )
                need(bool(incident), "independent atom incidence")
                geometry = {
                    key: ({"kind": item[0], "value": str(item[1])}
                          if item[0] == "POINT" else
                          {"kind": item[0], "lower": str(item[1]), "upper": str(item[2])})
                    for key, item in axis.items()
                }
                rows.append({
                    "ambient_dimension": sum(item[0] == "OPEN_INTERVAL" for item in axis.values()),
                    "geometry": geometry,
                    "incident_root_keys": incident,
                    "owner_root_key": incident[0],
                    "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    dimensions = Counter(row["ambient_dimension"] for row in rows)
    need(len(rows) == 255 and dimensions == Counter({3: 16, 2: 74, 1: 111, 0: 54}), "independent stratum census")
    return digest(rows), dimensions


def independent_authority() -> dict[str, Any]:
    producer_raw = PRODUCER.read_bytes()
    need(hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256, "producer source pin")
    q2 = load_q2()
    document, _audit = q2.frozen_q1_audit()
    result = document["result"]
    origin = next(row for row in result["combined_origin_gate"]["origin_rows"] if row["origin_key"] == ORIGIN)
    roots = sorted(
        (row for row in result["analytic_cohort_census"]["root_results"] if row["origin_key"] == ORIGIN),
        key=lambda row: row["root_key"],
    )
    need(digest(origin) == COMBINED_SHA256 and digest(roots) == ROOTS_SHA256, "independent Q1 South pins")
    for row in roots:
        params = row["cohort_parameters"]
        need(
            params["source_chart"] == "W:S" and params["p_sign"] == -1
            and params["active_target_set"] == ["G[0,0]", "W[-1,0]"]
            and params["exact_q_squared_scale"] == "1023/262144"
            and row["analytic_root_applicable"] is True
            and row["failure_reasons"] == []
            and row["frozen_target"]["target_definition"]
                == {"ix": 1, "iy": 0, "obstacle": "W", "radius": "4/25"}
            and row["frozen_target"]["strict"]["ell_negative"] is True
            and row["frozen_target"]["strict"]["f_at_0_positive"] is True
            and row["certified_future_witness_targets"] == ["W[-1,0]"],
            "independent South root metric:" + row["root_key"],
        )
        left = next(item for item in row["future_targets"] if item["target"] == "W[-1,0]")
        need(all(left["strict"][key] is True for key in (
            "f_at_0_positive", "f_at_1_negative", "transverse_margin_positive", "discriminant_positive",
        )), "independent South left-root witness:" + row["root_key"])

    # Direct South algebra, not an inference from North/South key pairing.
    k, rho = Q(1023, 262144), Q(4, 25)
    t0, t1 = T_CUTS[0], T_CUTS[-1]
    p2, a2 = Q(255, 256), Q(63, 64)
    need(
        k < Q(1, 256)
        and max(abs(t0), abs(t1)) < Q(1, 8)
        and p2 * a2 == Q(16065, 16384) > Q(1, 4),
        "independent radical bounds",
    )
    # With n=(t,-a), p=-P and u=(qt-Pa,-qa-Pt):
    # u.d_F=q(t-rho)-Pa and u.d_L=Pa-q(t+rho), using t^2+a^2=1.
    plus_upper = t1 + rho
    ell_lower = Q(1, 2) - Q(1, 16) * plus_upper
    transverse_upper = Q(1, 16) + plus_upper
    need(
        t0 + rho == Q(967, 16000)
        and plus_upper == Q(143, 2000)
        and ell_lower == Q(15857, 32000) > 0
        and transverse_upper == Q(67, 500) < rho
        and rho - transverse_upper == Q(13, 500)
        and Q(1) + 2 * rho * t0 == Q(48407, 50000) > 0,
        "independent South collision margins",
    )
    partition_hash, dimensions = independent_partition(roots)
    need(partition_hash == PARTITION_SHA256, "independent partition digest")
    complement = origin["complement"]
    need(
        origin["conditional_origin_applicable"] is True
        and complement["P215_exact_behind_closed_child_count"] == 327
        and complement["P215_residual_child_count"] == 1
        and complement["unique_compact_residual_in_exactly_one_root_box"] is True
        and complement["residual_witnesses"][0]["analytic_root_container_count"] == 1,
        "independent South complement closure",
    )
    return {
        "origin_key": ORIGIN,
        "root_count": len(roots),
        "partition_sha256": partition_hash,
        "dimensions": {str(key): dimensions[key] for key in (3, 2, 1, 0)},
        "exact_frozen_ell_upper": "-1/2",
        "exact_future_ell_lower": str(ell_lower),
        "exact_transverse_margin_lower": str(rho - transverse_upper),
        "formal_credit": 0,
    }


def verify(raw: bytes) -> dict[str, Any]:
    candidate = strict_document(raw)
    need(set(candidate) == {"schema", "result", "result_sha256"}, "candidate top-level shape")
    need(candidate["schema"] == SCHEMA and type(candidate["result"]) is dict, "candidate schema")
    need(candidate["result_sha256"] == digest(candidate["result"]), "candidate result closure")
    need(candidate["result_sha256"] == EXPECTED_RESULT_SHA256, "candidate frozen expected result")
    authority = independent_authority()
    result = candidate["result"]
    need(
        result["status"] == "PASS_SOUTH_PAIRED_ORIGIN_WHOLE_ORIGIN_ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT"
        and result["verdict"] == "PASS_ZERO_CREDIT_RESEARCH_THEOREM"
        and result["selected_origin"]["origin_key"] == authority["origin_key"]
        and result["selected_origin"]["root_count"] == authority["root_count"]
        and result["cross_root_half_open_partition"]["owner_assignment_rows_sha256"] == authority["partition_sha256"]
        and result["cross_root_half_open_partition"]["atomic_stratum_count_by_dimension"] == authority["dimensions"],
        "candidate theorem agrees with independent reconstruction",
    )
    nonpromotion = result["strict_nonpromotion"]
    need(
        nonpromotion["formal_credit"] == 0
        and nonpromotion["ledger_unchanged"] is True
        and nonpromotion["compact_q_formal_remaining_origins"] == 54
        and nonpromotion["seal_or_release_authority"] is False
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "candidate strict nonpromotion",
    )
    return authority


def main() -> int:
    try:
        if len(sys.argv) == 1 or sys.argv[1] == "-":
            raw = sys.stdin.buffer.read()
        else:
            raw = Path(sys.argv[1]).read_bytes()
        authority = verify(raw)
        output = {
            "schema": "cm2.round306c30q3.compact-q-south-paired-origin-independent-verification.v1",
            "status": "PASS_INDEPENDENT_C30Q3_SOUTH_WHOLE_ORIGIN_THEOREM__ZERO_FORMAL_CREDIT",
            "reconstruction": authority,
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "formal_credit": 0,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, StopIteration, KeyError, TypeError, ValueError, OSError) as error:
        print("REJECT_C30Q3_INDEPENDENT_VERIFICATION:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
