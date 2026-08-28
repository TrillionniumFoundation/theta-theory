#!/usr/bin/env python3
"""Independent verifier for the Round-71 witnessed R1 face germs."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, digest, require, semantic_mutation_test, sha256_path,
    strict_json_path, strict_json_self_test, validate_pins,
)
from cm2_round71_r1_nonempty_face_germs_cert import (
    COMMON, MANIFEST_SCHEMA, PINS, RESULT_SCHEMA, WITNESSES, build_result,
    core_id, face_id, physical_cores,
)


HERE = Path(__file__).resolve().parent
PREFIX = "cm2-round71-r1-nonempty-face-germs"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_round71_r1_nonempty_face_germs_cert.py"
VERIFIER = Path(__file__).resolve()
getcontext().prec = 100


def decimal_q(value: Q) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def target_indices(target_id: str) -> tuple[str, int, int]:
    obstacle = target_id[0]
    ix, iy = map(int, target_id[2:-1].split(","))
    return obstacle, ix, iy


def collision_output(source: Any, destination: Any, t_value: Q, p_value: Q) -> tuple[Decimal, Decimal]:
    t = decimal_q(t_value)
    p = decimal_q(p_value)
    one = Decimal(1)
    normal_radical = (one - t * t).sqrt()
    momentum_radical = (one - p * p).sqrt()
    source_obstacle, cell = source.chart_id.split(":")
    if cell == "E":
        normal_x, normal_y = normal_radical, t
    elif cell == "W":
        normal_x, normal_y = -normal_radical, t
    elif cell == "N":
        normal_x, normal_y = t, normal_radical
    else:
        normal_x, normal_y = t, -normal_radical
    velocity_x = momentum_radical * normal_x - p * normal_y
    velocity_y = momentum_radical * normal_y + p * normal_x
    if source_obstacle == "G":
        center_x = center_y = Decimal(0)
        source_radius = Decimal(9) / 25
    else:
        center_x = center_y = Decimal(1) / 2
        source_radius = Decimal(4) / 25
    point_x = center_x + source_radius * normal_x
    point_y = center_y + source_radius * normal_y
    target_obstacle, ix, iy = target_indices(source.target_id)
    target_radius = Decimal(9) / 25 if target_obstacle == "G" else Decimal(4) / 25
    target_x = Decimal(ix) + (Decimal(1) / 2 if target_obstacle == "W" else 0)
    target_y = Decimal(iy) + (Decimal(1) / 2 if target_obstacle == "W" else 0)
    delta_x, delta_y = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * delta_x + velocity_y * delta_y
    transverse = -velocity_y * delta_x + velocity_x * delta_y
    root = longitudinal - (target_radius * target_radius - transverse * transverse).sqrt()
    hit_x, hit_y = point_x + root * velocity_x, point_y + root * velocity_y
    target_normal_x = (hit_x - target_x) / target_radius
    target_normal_y = (hit_y - target_y) / target_radius
    target_p = transverse / target_radius
    destination_cell = destination.chart_id.split(":")[1]
    target_t = target_normal_y if destination_cell in ("E", "W") else target_normal_x
    return target_t, target_p


def integrity(data: dict[str, Any], check_files: bool = True) -> None:
    require(data["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(data["result"]["schema"] == RESULT_SCHEMA, "result schema")
    require(data["pins"] == PINS, "pins")
    if check_files:
        validate_pins(HERE, PINS)
        require(data["report_sha256"] == sha256_path(REPORT), "report hash")
        require(data["witnesses_sha256"] == sha256_path(WITNESSES), "witness hash")
        require(data["certificate_sha256"] == sha256_path(CERT), "certificate hash")
        require(data["verifier_sha256"] == sha256_path(VERIFIER), "verifier hash")
        require(data["common_sha256"] == sha256_path(COMMON), "common hash")
    replay = copy.deepcopy(data["result"])
    claimed = replay.pop("internal_replay_digest")
    require(claimed == digest(replay), "result digest")
    require(data["verdict"] == data["result"]["strict_frontier"], "verdict")


def semantics(result: dict[str, Any]) -> None:
    require(result == build_result(), "canonical result")
    registry = result["base_fibre_nonempty_face_witness_registry"]
    require(registry["status"] == "CERTIFIED_32_NONEMPTY_REGULAR_LOCAL_FACE_GERMS",
            "registry status")
    require(registry["parameter"] == "s=0" and registry["positive_R1_edge_cell_count"] == 16,
            "base cells")
    require(registry["candidate_family_count_total"] == 1152 and
            registry["witnessed_distinct_candidate_family_count"] == 32 and
            registry["unresolved_candidate_family_count"] == 1120, "family partition")
    require(registry["materialized_local_component_count_after_round71"] == 32 and
            registry["materialized_one_sided_trace_count"] == 64, "component counts")
    rows = registry["component_rows"]
    require(len(rows) == 32 and len({row["component_id"] for row in rows}) == 32,
            "component rows")
    require(len({row["path_cell_id"] for row in rows}) == 16, "path cells")
    require(len({trace["trace_id"] for row in rows for trace in row["trace_rows"]}) == 64,
            "trace rows")
    require(all(row["time_j"] == 1 and row["connected_rank"] == 0 for row in rows),
            "typed local ranks")
    require(all(row["F8_normalized_transversality_strict_lower"] == "1/5" for row in rows),
            "F8 rows")
    require(all(row["F9_unit_speed_C2_upper"] == "691839371876953699123200" for row in rows),
            "F9 rows")
    fields = result["actual_local_field_attachment"]
    require(fields["F9_per_face_unit_speed_C2_upper"] == "691839371876953699123200" and
            fields["F9_32_face_finite_sum_upper"] == "22138859900062518371942400",
            "F9 finite sum")
    require(fields["F10_actual_compact_germs_in_search_domain"] == 32 and
            fields["F10_numeric_integers_materialized"] == 0 and
            fields["F13_numeric_rows_materialized"] == 0, "no numeric promotion")
    frontier = result["strict_frontier"]
    require(frontier["complete_1152_family_empty_nonempty_classification"] ==
            "NOT_CERTIFIED__32_POSITIVE_1120_UNRESOLVED", "classification frontier")
    require(frontier["complete_composite_gates"] == "0/5" and
            frontier["CM2"] == "NO-GO_FOR_CLAIM", "strict verdict")


def independent_replay() -> dict[str, str]:
    witness_document = strict_json_path(WITNESSES)
    require(witness_document["schema"] == "cm2.round71.r1-nonempty-face-witnesses.v1",
            "witness schema")
    witnesses = witness_document["rows"]
    cores = physical_cores()
    require(len(witnesses) == 32, "witness count")
    pairs: dict[tuple[str, str], int] = {}
    maximum_length = Q(0)
    minimum_margin_ratio: Decimal | None = None
    for witness in witnesses:
        source = cores[witness["source_core_index"]]
        destination = cores[witness["destination_core_index"]]
        require(witness["source_core_id"] == core_id(source), "replay source ID")
        require(witness["destination_core_id"] == core_id(destination), "replay destination ID")
        require(witness["destination_face_id"] == face_id(destination, witness["side"]),
                "replay face ID")
        coordinate_index = 0 if witness["level_coordinate"] == "t" else 1
        other_index = 1 - coordinate_index
        level = decimal_q(Q(witness["level_value"]))
        outputs = []
        for key in ("witness_minus", "witness_plus"):
            row = witness[key]
            output = collision_output(source, destination, Q(row["t"]), Q(row["p"]))
            outputs.append(output)
            sign = -1 if output[coordinate_index] < level else 1
            require(sign == row["level_sign"], "endpoint sign")
        require(witness["witness_minus"]["level_sign"] *
                witness["witness_plus"]["level_sign"] == -1, "sign change")
        if other_index == 1:
            lower, upper = destination.p0, destination.p1
        else:
            lower, upper = destination.t0, destination.t1
        margin = min(min(output[other_index] - decimal_q(lower),
                         decimal_q(upper) - output[other_index]) for output in outputs)
        length = Q(witness["source_segment_l1_length"])
        drift = Decimal(2457600) * decimal_q(length)
        require(margin > drift > 0, "other coordinate remains interior")
        ratio = margin / drift
        minimum_margin_ratio = ratio if minimum_margin_ratio is None else min(minimum_margin_ratio, ratio)
        maximum_length = max(maximum_length, length)
        pair = (witness["source_core_id"], witness["destination_core_id"])
        pairs[pair] = pairs.get(pair, 0) + 1
    require(len(pairs) == 16 and set(pairs.values()) == {2}, "two faces per edge")
    require(maximum_length == Q(23, 23058430092136939520000), "maximum segment")
    require(minimum_margin_ratio is not None and minimum_margin_ratio > Decimal("3.7e11"),
            "margin ratio")
    return {
        "positive_edge_cells": "16/16",
        "sign_changing_face_witnesses": "32/32",
        "one_sided_traces": "64/64",
        "minimum_margin_over_drift": ">3.7e11",
        "status": "PASS",
    }


def deterministic(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
    )
    require(proc.returncode == 0, f"producer: {proc.stderr.decode().strip()}")
    require(proc.stdout == MANIFEST.read_bytes() and strict_json_path(MANIFEST) == data,
            "deterministic producer")


def run_audit(data: dict[str, Any], regenerate: bool = True) -> None:
    integrity(data)
    semantics(data["result"])
    independent_replay()
    if regenerate:
        deterministic(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = strict_json_path(MANIFEST)
        if args.audit:
            run_audit(data)
            print("AUDIT: PASS")
            return 0
        if args.replay:
            integrity(data)
            semantics(data["result"])
            print(json.dumps(independent_replay(), sort_keys=True))
            return 0
        if args.self_test:
            run_audit(data)
            semantic = semantic_mutation_test(data, integrity, semantics)
            strict = strict_json_self_test()
            print(f"HOSTILE_SEMANTIC_REJECTED: {semantic}/{semantic}")
            print(f"HOSTILE_JSON_REJECTED: {strict}/{strict}")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            proc = subprocess.run(
                [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
                cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=300,
            )
            require(proc.returncode == 0, "reemit producer")
            args.reemit.write_bytes(proc.stdout)
            require(args.reemit.read_bytes() == MANIFEST.read_bytes(), "reemit bytes")
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError,
            subprocess.SubprocessError) as exc:
        print(f"ROUND71_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND71 R1 NONEMPTY FACE GERMS: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
