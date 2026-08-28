#!/usr/bin/env python3
"""Close the eight corrected exterior rays at immutable-table source grazing."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
import cm2_round96_rank3_correlated_owner_interval_cert as round96
import cm2_round100_rank3_immutable_interior_gap_closure as round100
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
ROUND87 = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
ROUND94 = HERE / "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json"
ROUND99 = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
ROUND100 = HERE / "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
PINS = {
    ROUND87.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    ROUND94.name: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    ROUND99.name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    ROUND100.name: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
}
SCHEMA = "cm2.round101.rank3-eight-ray-source-grazing-closure.v1"
PRECISION_BITS = 512


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corrected_rays(physical, source_caps):
    capped = {(tuple(row["branch_key"]), row["projective_end"]) for row in source_caps}
    grouped = defaultdict(list)
    for port_id, row in physical.items():
        grouped[round89.key(row)].append(port_id)
    rays = []
    for branch, port_ids in sorted(grouped.items()):
        port_ids.sort(key=lambda port_id: float(round89.qball(physical[port_id]).mid()))
        for side, port_id in (
            ("LEFT_PROJECTIVE_END", port_ids[0]),
            ("RIGHT_PROJECTIVE_END", port_ids[-1]),
        ):
            if (branch, side) not in capped:
                rays.append((branch, side, port_id))
    if len(rays) != 8:
        raise RuntimeError("corrected exterior ray accounting")
    return rays


def certify_segment(source, branch, qa, qb, cores):
    path, first_chart, second_chart, first_digest, second_digest, third_digest = round96.certify(
        source, branch, qa, qb
    )
    return {
        "q_interval": [str(qa), str(qb)],
        "source_chart": source.chart_id,
        "reverse_path": list(path),
        "first_outgoing_chart": first_chart,
        "second_outgoing_chart": second_chart,
        "complete_first_competitor_rows_sha256": first_digest,
        "complete_second_competitor_rows_sha256": second_digest,
        "complete_third_competitor_rows_sha256": third_digest,
    }


def build(precision_bits: int = PRECISION_BITS):
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    frozen87 = json.loads(ROUND87.read_text())["result"]
    by_id = {row["registered_port_id"]: row for row in frozen87["port_event_rows"]}
    frozen99 = json.loads(ROUND99.read_text())["result"]
    physical = {
        port_id: by_id[port_id]
        for port_id in frozen99["corrected_locally_physical_registered_port_ids"]
    }
    frozen100 = json.loads(ROUND100.read_text())["result"]
    rays = corrected_rays(physical, frozen100["source_cap_rows"])
    transfers = {
        row["exterior_port_id"]: row
        for row in json.loads(ROUND94.read_text())["result"]["transfer_rows"]
    }
    cores = core_cert.physical_cores()
    round87.WORK_CORES = cores
    round87.physical_type = round100.immutable_physical_type
    rows = []
    for ray_index, (branch, side, port_id) in enumerate(rays):
        if port_id not in transfers:
            raise RuntimeError("corrected open ray lacks adjacent-chart transfer")
        transfer = transfers[port_id]
        if transfer["first_physical_terminal_event_type"] != "SOURCE_GRAZING":
            raise RuntimeError("corrected ray terminal event is not source grazing")
        core_chain = round91.certify_ray(branch, side, port_id, physical, cores)
        q0, direction, cell_edge, inner, seam_outer, event_kind, _, _ = round93.isolate_event(
            branch, side, port_id, physical, cores
        )
        if event_kind != "SOURCE_CHART_SEAM":
            raise RuntimeError("corrected ray does not reach adjacent chart through a seam")
        source = cores[branch[0]]
        source_bounds = [
            cell_edge + (inner - cell_edge) * Q(index, round93.PROBE_COUNT + 1)
            for index in range(round93.PROBE_COUNT + 2)
        ]
        segments = [
            (source, q0 + direction * left, q0 + direction * right, "SOURCE_CHART")
            for left, right in zip(source_bounds, source_bounds[1:])
        ]
        adjacent_source = replace(
            source, chart_id=f"{source.source}:{transfer['adjacent_source_chart']}"
        )
        terminal = Q(transfer["first_physical_terminal_event_parameter_bracket"][0])
        transfer_bounds = [
            seam_outer + (terminal - seam_outer) * Q(index, round94.PROBE_COUNT + 1)
            for index in range(round94.PROBE_COUNT + 2)
        ]
        segments.extend(
            (adjacent_source, q0 + direction * left, q0 + direction * right, "ADJACENT_CHART")
            for left, right in zip(transfer_bounds, transfer_bounds[1:])
        )
        certified = []
        layer_histogram = Counter()
        for segment_source, qa, qb, layer in segments:
            row = certify_segment(segment_source, branch, qa, qb, cores)
            row["layer"] = layer
            certified.append(row)
            layer_histogram[layer] += 1
        rows.append({
            "ray_index": ray_index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": side,
            "old_source_chart": transfer["old_source_chart"],
            "adjacent_source_chart": transfer["adjacent_source_chart"],
            "seam_transfer_status": transfer["seam_transfer_status"],
            "terminal_event_type": "SOURCE_GRAZING",
            "terminal_event_parameter_bracket": transfer["first_physical_terminal_event_parameter_bracket"],
            "immutable_source_core_exit_chain_strip_count": core_chain["physical_chain_strip_count"],
            "immutable_source_core_exit_chain_boxes_sha256": core_chain["physical_chain_boxes_sha256"],
            "immutable_source_core_exit_chain_competitor_rows_sha256": core_chain["physical_chain_competitor_rows_sha256"],
            "certified_segment_count": len(certified),
            "segment_layer_histogram": dict(sorted(layer_histogram.items())),
            "certified_segment_rows_sha256": digest(certified),
        })
    result = {
        "precision_bits": precision_bits,
        "input_corrected_open_exterior_ray_count": len(rays),
        "source_chart_segment_count": sum(row["segment_layer_histogram"]["SOURCE_CHART"] for row in rows),
        "adjacent_chart_segment_count": sum(row["segment_layer_histogram"]["ADJACENT_CHART"] for row in rows),
        "immutable_candidate_certified_segment_count": sum(row["certified_segment_count"] for row in rows),
        "source_grazing_terminal_event_count": sum(row["terminal_event_type"] == "SOURCE_GRAZING" for row in rows),
        "remaining_open_exterior_ray_count": 0,
        "ray_rows": rows,
        "ray_rows_sha256": digest(rows),
        "strict_scope": "immutable-candidate whole-segment continuation of all eight corrected exterior rays through unique adjacent charts to source grazing",
        "strict_nonclaims": [
            "rank-three face quotient installation is deferred to the next ledger",
            "no RN or Gate5 row is promoted in this certificate",
        ],
        "upstream_pins": PINS,
    }
    if len(rows) != 8 or result["immutable_candidate_certified_segment_count"] != 1552:
        raise RuntimeError("corrected ray segment accounting")
    if result["source_chart_segment_count"] != 1032 or result["adjacent_chart_segment_count"] != 520:
        raise RuntimeError("corrected ray layer accounting")
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
