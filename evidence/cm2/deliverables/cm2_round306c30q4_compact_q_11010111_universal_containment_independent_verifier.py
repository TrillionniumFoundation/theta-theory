#!/usr/bin/env python3
"""Independent verifier for the zero-credit C30q4 containment ledger."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
PRODUCER = HERE / "cm2_round306c30q4_compact_q_11010111_universal_containment_gate.py"
PRODUCER_SHA256 = "cdf1b43cec11aa6f3b03ef3a934cd1260478c1266dc38a89fb23e1996f482232"
Q2_SOURCE = HERE / "cm2_round306c30q2_compact_q_exact_seven_cohort_counterexample_routing_gate.py"
Q2_SOURCE_SHA256 = "8e3beea8ab742443e028ab5e8c794a5e0f3df3467d70d0c4c3ca29e31983c125"
SCHEMA = "cm2.round306c30q4.compact-q-11010111-universal-containment-gate.v1"
EXPECTED_RESULT_SHA256 = "729d1dc2cef3b35e9c9d8d1e3a45787189c1169130c321d6ac01d6c1572ad188"
ORIGINS = ("W:N:03.15.11010111", "W:S:H.03.15.11010111")
EXPECTED_RESIDUAL_SHA256 = {
    "W:N:03.15.11010111": "6e638b6cd6f3ca0972640e6bef9ee44dbd551a8aa0e72e8922c2357de6821113",
    "W:S:H.03.15.11010111": "0ce975dc4163aea892a0687e2bac04fcbe8144a75fdfe03a4ef206f17aa6ff82",
}
EXPECTED_PARTITIONS = {
    "W:N:03.15.11010111": "0c8739b95a256254af12ddb2b0f0b6e37f3918a2d6857110c67e25b78fee5660",
    "W:S:H.03.15.11010111": "2ecddffb078e9f48e2c7c2c6e37da789bb3a95b3b72d4f078644604a2e506753",
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


def strict_json(raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    try:
        value = json.loads(
            raw.decode(), object_pairs_hook=unique,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict candidate JSON") from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"}, "canonical candidate JSON")
    return value


def load_q2() -> Any:
    need(hashlib.sha256(Q2_SOURCE.read_bytes()).hexdigest() == Q2_SOURCE_SHA256, "Q2 source pin")
    specification = importlib.util.spec_from_file_location("cm2_c30q2_for_q4_verifier", Q2_SOURCE)
    need(specification is not None and specification.loader is not None, "Q2 import spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == Q2_SOURCE, "Q2 import identity")
    return module


def pair(values: list[str], label: str) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2, "interval shape:" + label)
    result = Q(values[0]), Q(values[1])
    need(result[0] < result[1] and [str(result[0]), str(result[1])] == values, "canonical interval:" + label)
    return result


def roots_from_frozen(result: dict[str, Any], origin: str) -> list[dict[str, Any]]:
    roots = sorted(
        (row for row in result["analytic_cohort_census"]["root_results"] if row["origin_key"] == origin),
        key=lambda row: row["root_key"],
    )
    need(
        len(roots) == 16
        and all(row["analytic_root_applicable"] is True and row["failure_reasons"] == [] for row in roots)
        and all(row["frozen_target"]["strict"]["ell_negative"] is True for row in roots)
        and all("W[-1,0]" in row["certified_future_witness_targets"] for row in roots),
        "frozen 16-root analytic theorem:" + origin,
    )
    return roots


def boxes(roots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in roots:
        p = row["cohort_parameters"]
        output.append({
            "root_key": row["root_key"],
            "t": pair(p["exact_t_domain"], "root t"),
            "p": pair(p["source_p_endpoint_domain"], "root p"),
            "s": pair(p["exact_s_domain"], "root s"),
        })
    return output


def contains(child: dict[str, tuple[Q, Q]], root: dict[str, Any]) -> bool:
    return all(root[axis][0] <= child[axis][0] <= child[axis][1] <= root[axis][1] for axis in ("t", "p", "s"))


def atoms(cuts: tuple[Q, ...]) -> list[tuple[str, Q, Q]]:
    output: list[tuple[str, Q, Q]] = []
    for index, point in enumerate(cuts):
        output.append(("POINT", point, point))
        if index + 1 < len(cuts):
            output.append(("OPEN_INTERVAL", point, cuts[index + 1]))
    return output


def partition(roots: list[dict[str, Any]]) -> str:
    t_cuts = tuple(sorted({value for root in roots for value in root["t"]}))
    s_cuts = tuple(sorted({value for root in roots for value in root["s"]}))
    r_cuts = (Q(0), Q(1))
    need(len(t_cuts) == 9 and s_cuts == (Q(-1, 400), Q(0), Q(1, 400)), "partition cuts")
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
                    key: ({"kind": item[0], "value": str(item[1])}
                          if item[0] == "POINT" else
                          {"kind": item[0], "lower": str(item[1]), "upper": str(item[2])})
                    for key, item in axes.items()
                }
                rows.append({
                    "ambient_dimension": sum(item[0] == "OPEN_INTERVAL" for item in axes.values()),
                    "geometry": geometry,
                    "incident_root_keys": incident,
                    "owner_root_key": incident[0],
                    "analytic_disposition": "EXCLUDED_FROZEN_OWNER_STRICTLY_BEHIND",
                })
    rows.sort(key=lambda row: canonical(row["geometry"]))
    need(Counter(row["ambient_dimension"] for row in rows) == Counter({3: 16, 2: 74, 1: 111, 0: 54}), "partition dimensions")
    return digest(rows)


def verify(raw: bytes) -> dict[str, Any]:
    need(hashlib.sha256(PRODUCER.read_bytes()).hexdigest() == PRODUCER_SHA256, "producer source pin")
    candidate = strict_json(raw)
    need(set(candidate) == {"schema", "result", "result_sha256"} and candidate["schema"] == SCHEMA, "candidate top-level")
    result = candidate["result"]
    need(candidate["result_sha256"] == digest(result) == EXPECTED_RESULT_SHA256, "candidate result closure/pin")
    q2 = load_q2()
    frozen_document, _audit = q2.frozen_q1_audit()
    frozen = frozen_document["result"]
    frozen_origins = {row["origin_key"]: row for row in frozen["combined_origin_gate"]["origin_rows"]}
    candidate_origins = {row["origin_key"]: row for row in result["universal_residual_containment"]["origin_rows"]}
    need(set(candidate_origins) == set(ORIGINS), "candidate origin set")
    checked: list[dict[str, Any]] = []
    for origin in ORIGINS:
        frozen_origin = frozen_origins[origin]
        candidate_origin = candidate_origins[origin]
        need(
            frozen_origin["analytic"]["all_analytic_roots_applicable"] is True
            and frozen_origin["complement"]["P215_exact_behind_closed_child_count"] == 420
            and frozen_origin["complement"]["P215_residual_child_count"] == 128
            and frozen_origin["complement"]["residual_rows_sha256"] == EXPECTED_RESIDUAL_SHA256[origin],
            "frozen complement authority:" + origin,
        )
        roots = boxes(roots_from_frozen(frozen, origin))
        rows = candidate_origin["residual_rows"]
        need(
            len(rows) == 128 and len({row["cell_key"] for row in rows}) == 128
            and digest(rows) == candidate_origin["residual_rows_sha256"] == EXPECTED_RESIDUAL_SHA256[origin],
            "candidate residual ledger closure:" + origin,
        )
        for row in rows:
            child = {axis: pair(row["box"][axis], "child " + axis) for axis in ("t", "p", "s")}
            containers = sorted(root["root_key"] for root in roots if contains(child, root))
            need(
                row["category"] == "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
                and row["analytic_root_container_count"] == 1
                and row["analytic_root_containers"] == containers
                and len(containers) == 1,
                "independent universal containment:" + row["cell_key"],
            )
        partition_hash = partition(roots)
        need(
            partition_hash == EXPECTED_PARTITIONS[origin]
            and result["cross_root_half_open_partitions"][origin]["owner_assignment_rows_sha256"] == partition_hash,
            "independent partition:" + origin,
        )
        checked.append({
            "origin_key": origin, "analytic_root_count": 16,
            "residual_child_count": 128, "all_contained_exactly_once": True,
            "residual_rows_sha256": EXPECTED_RESIDUAL_SHA256[origin],
            "partition_sha256": partition_hash,
        })
    need(
        result["status"] == "PASS_TWO_ORIGIN_128_RESIDUAL_UNIVERSAL_CONTAINMENT__ZERO_FORMAL_CREDIT"
        and result["universal_residual_containment"]["residual_child_count"] == 256
        and result["whole_origin_conclusion"]["both_origins_exclude_frozen_first_owner_everywhere"] is True,
        "candidate conclusion",
    )
    boundary = result["strict_nonpromotion"]
    need(
        boundary["formal_credit"] == 0 and boundary["ledger_unchanged"] is True
        and boundary["compact_q_formal_remaining_origins"] == 54
        and boundary["seal_or_release_authority"] is False
        and boundary["CM2"] == "NO-GO_FOR_CLAIM",
        "candidate strict nonpromotion",
    )
    return {
        "origin_count": 2, "analytic_root_count": 32,
        "residual_child_count": 256, "checked_origins": checked,
        "formal_credit": 0,
    }


def main() -> int:
    try:
        raw = sys.stdin.buffer.read() if len(sys.argv) == 1 or sys.argv[1] == "-" else Path(sys.argv[1]).read_bytes()
        reconstruction = verify(raw)
        output = {
            "schema": "cm2.round306c30q4.compact-q-11010111-independent-verification.v1",
            "status": "PASS_INDEPENDENT_C30Q4_256_OF_256_UNIVERSAL_CONTAINMENT__ZERO_FORMAL_CREDIT",
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "reconstruction": reconstruction,
            "formal_credit": 0,
            "compact_q_formal_remaining_origins": 54,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Reject, KeyError, StopIteration, TypeError, ValueError, OSError) as error:
        print("REJECT_C30Q4_INDEPENDENT_VERIFICATION:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
