#!/usr/bin/env python3
"""Rebuild the surviving rank-three interior gaps with immutable candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round90_rank3_tracked_residual_gap_closure_cert as round90
import cm2_round99_rank3_registered_port_candidate_audit as round99
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND87 = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
ROUND89 = HERE / "cm2-round89-rank3-projective-gap-closure-2026-07-22.json"
ROUND99 = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
PINS = {
    ROUND87.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    ROUND89.name: "189044e2b366b9a1620375f2a1eeaf163d2eff0a8996ccf76869fa2294a34a08",
    ROUND99.name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
}
SCHEMA = "cm2.round100.rank3-immutable-interior-gap-closure.v1"
PRECISION_BITS = 512


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def immutable_physical_type(
    state2: dict[str, Any], current_target: str, tangent_target: str,
) -> tuple[str, dict[str, Any]]:
    candidate_x, candidate_y = time3.time2_cert.target_center(tangent_target, state2["s"])
    dx = candidate_x - state2["contact_x"]
    dy = candidate_y - state2["contact_y"]
    ux, uy = state2["outgoing_x"], state2["outgoing_y"]
    tangent_flight = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    tangent_sign = strict_sign(tangent_flight)
    transverse_sign = strict_sign(transverse)
    if tangent_sign == 0 or transverse_sign == 0:
        raise RuntimeError("unresolved tangent event sign")
    denominator = arb(1) + ux
    if strict_sign(denominator) != 1:
        raise RuntimeError("projective q denominator is not positive")
    rows, winner, full_count, consumed_prefix = round99.immutable_competitor_rows(
        state2, current_target, tangent_target, tangent_flight
    )
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    if tangent_sign < 0:
        status = "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_NEGATIVE"
    elif bool(tangent_flight > tau_max):
        status = "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION"
        tau_relation = "STRICTLY_ABOVE_TAU_MAX"
    elif bool(tangent_flight < tau_max):
        tau_relation = "STRICTLY_BETWEEN_ZERO_AND_TAU_MAX"
        before = [
            row["candidate_id"] for row in rows
            if row["relation_to_tangent_target_flight"] == "STRICTLY_BEFORE_TANGENT_TARGET"
        ]
        status = (
            "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION"
            if before else "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        )
        if before and winner not in before:
            raise RuntimeError("immutable earliest winner mismatch")
    else:
        raise RuntimeError("unresolved tangent flight / tau-max relation")
    q_value = uy / denominator
    return status, {
        "oriented_line_projective_chart": "Q_TAN_HALF_EQUALS_UY_OVER_ONE_PLUS_UX",
        "projective_chart_denominator_strict_sign": 1,
        "projective_q_enclosure": str(q_value),
        "signed_transverse_tangency_factor_sign": transverse_sign,
        "target_tangent_flight_sign": tangent_sign,
        "target_tangent_flight_tau_relation": tau_relation,
        "complete_translated_candidate_count": full_count,
        "historically_consumed_prefix_count": consumed_prefix,
        "competitor_rows": rows,
        "competitor_rows_sha256": digest(rows),
        "unique_strict_future_competitor_winner": winner,
    }


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    rows, pair_rows = round89.load()
    old_by_id = {row["registered_port_id"]: row for row in rows}
    corrected_ids = set(json.loads(ROUND99.read_text())["result"]["corrected_locally_physical_registered_port_ids"])
    physical = {port_id: old_by_id[port_id] for port_id in corrected_ids}
    by_branch: dict[tuple[int, str, str, int], list[str]] = defaultdict(list)
    for port_id, row in physical.items():
        by_branch[round89.key(row)].append(port_id)
    for branch, ids in by_branch.items():
        ids.sort(key=lambda port_id: float(round89.qball(physical[port_id]).mid()))
        if any(strict_sign(round89.qball(physical[b]) - round89.qball(physical[a])) != 1 for a, b in zip(ids, ids[1:])):
            raise RuntimeError(f"non-strict corrected q order: {branch}")
    registered: set[frozenset[str]] = set()
    source_caps = []
    ignored_historical_pairs = 0
    for pair in pair_rows:
        left, right = pair["registered_elementary_arc_endpoint_port_ids"]
        left_physical, right_physical = left in physical, right in physical
        if left_physical and right_physical:
            if round89.key(physical[left]) != round89.key(physical[right]):
                raise RuntimeError("corrected registered arc branch mismatch")
            registered.add(frozenset((left, right)))
        elif left_physical != right_physical:
            port_id = left if left_physical else right
            source_id = right if left_physical else left
            if source_id in old_by_id:
                raise RuntimeError("corrected physical port paired to non-source nonphysical port")
            branch = round89.key(physical[port_id])
            order = by_branch[branch]
            rank = order.index(port_id)
            side = "LEFT_PROJECTIVE_END" if rank == 0 else "RIGHT_PROJECTIVE_END" if rank == len(order) - 1 else "NONEXTREME"
            if side == "NONEXTREME":
                raise RuntimeError("source cap is not projectively extreme")
            source_caps.append({
                "registered_source_port_id": source_id,
                "mated_physical_port_id": port_id,
                "branch_key": list(branch),
                "projective_end": side,
            })
        else:
            ignored_historical_pairs += 1
    old_round89 = json.loads(ROUND89.read_text())["result"]
    old_tracked_pairs = {
        frozenset((row["left_registered_port_id"], row["right_registered_port_id"]))
        for row in old_round89["unresolved_gap_rows"]
    }
    cores = core_cert.physical_cores()
    round87.WORK_CORES = cores
    round87.physical_type = immutable_physical_type
    gap_rows = []
    branch_rows = []
    for branch in sorted(by_branch):
        ids = by_branch[branch]
        direct_count = 0
        tracked_count = 0
        for left, right in zip(ids, ids[1:]):
            pair = frozenset((left, right))
            if pair in registered:
                continue
            if pair in old_tracked_pairs:
                gap = round90.tracked_gap(physical[left], physical[right], cores)
                gap["immutable_candidate_reaudit_method"] = "TRACKED_NODE_ROOT_CHAIN"
                tracked_count += 1
            else:
                gap = round89.certify_gap(physical[left], physical[right], cores)
                gap["immutable_candidate_reaudit_method"] = "WHOLE_TUBE_IFT_CHAIN"
                direct_count += 1
            gap_rows.append(gap)
        branch_source_caps = [row for row in source_caps if tuple(row["branch_key"]) == branch]
        branch_rows.append({
            "source_core_index": branch[0],
            "second_selected_target_id": branch[1],
            "third_candidate_id": branch[2],
            "signed_transverse_tangency_factor_sign": branch[3],
            "strictly_ordered_physical_port_count": len(ids),
            "registered_source_boundary_endpoint_count": len(branch_source_caps),
            "registered_adjacent_arc_count": sum(frozenset(pair) in registered for pair in zip(ids, ids[1:])),
            "immutable_whole_tube_gap_count": direct_count,
            "immutable_tracked_gap_count": tracked_count,
            "total_registered_endpoint_parity": (len(ids) + len(branch_source_caps)) % 2,
            "ordered_physical_port_ids_sha256": digest(ids),
        })
    method_histogram = Counter(row["immutable_candidate_reaudit_method"] for row in gap_rows)
    result = {
        "precision_bits": precision_bits,
        "corrected_locally_physical_port_count": len(physical),
        "surviving_oriented_projective_branch_count": len(by_branch),
        "surviving_registered_physical_arc_count": len(registered),
        "surviving_registered_source_cap_count": len(source_caps),
        "ignored_withdrawn_historical_pair_count": ignored_historical_pairs,
        "corrected_unregistered_interior_gap_count": len(gap_rows),
        "certified_immutable_candidate_interior_gap_count": len(gap_rows),
        "remaining_unresolved_interior_gap_count": 0,
        "gap_method_histogram": dict(sorted(method_histogram.items())),
        "source_cap_rows": sorted(source_caps, key=lambda row: (row["branch_key"], row["projective_end"])),
        "source_cap_rows_sha256": digest(sorted(source_caps, key=lambda row: (row["branch_key"], row["projective_end"]))),
        "branch_rows": branch_rows,
        "branch_rows_sha256": digest(branch_rows),
        "gap_rows": gap_rows,
        "gap_rows_sha256": digest(gap_rows),
        "strict_scope": "immutable-candidate whole-chain recertification of every interior gap on the twelve corrected surviving rank-three branches",
        "strict_nonclaims": [
            "the eight projective ends without source caps remain open rays",
            "interior continuation alone does not install a complete rank-three face quotient",
            "no RN or Gate5 row is promoted",
        ],
        "upstream_pins": PINS,
    }
    if len(physical) != 120 or len(by_branch) != 12:
        raise RuntimeError("corrected input accounting")
    if len(registered) != 52 or len(source_caps) != 16 or ignored_historical_pairs != 428:
        raise RuntimeError("corrected registered-pair accounting")
    if len(gap_rows) != 56 or method_histogram != Counter({"WHOLE_TUBE_IFT_CHAIN": 48, "TRACKED_NODE_ROOT_CHAIN": 8}):
        raise RuntimeError("corrected gap accounting")
    if any(row["total_registered_endpoint_parity"] for row in branch_rows):
        raise RuntimeError("corrected branch parity")
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
