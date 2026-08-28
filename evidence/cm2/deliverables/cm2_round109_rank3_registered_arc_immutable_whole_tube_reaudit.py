#!/usr/bin/env python3
"""Immutable complete-candidate whole-tube reaudit of 52 registered arcs.

Round100 deliberately skipped the already-registered arcs when rebuilding the
56 unregistered links.  This producer closes that audit asymmetry: every
REGISTERED_PHYSICAL_ARC link in the corrected Round102 quotient is passed
through the same IFT tube engine with the corrected immutable candidate tuple.

The scope is the tangent-face tube only.  This file does not construct or
claim either transverse D-sign cell, a homogeneity child, or any Gate5 field.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
from collections import Counter
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round100_rank3_immutable_interior_gap_closure as round100
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1"
PRECISION_BITS = 512
FILES = {
    "round87": "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "round99": "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "round102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "round87_source": "cm2_round87_rank3_port_event_continuation_cert.py",
    "round89_source": "cm2_round89_rank3_projective_gap_closure_cert.py",
    "round99_source": "cm2_round99_rank3_registered_port_candidate_audit.py",
    "round100_source": "cm2_round100_rank3_immutable_interior_gap_closure.py",
}
PINS = {
    FILES["round87"]: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    FILES["round99"]: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    FILES["round102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["round87_source"]: "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834",
    FILES["round89_source"]: "6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf",
    FILES["round99_source"]: "bbacd4407aa026850d9a410b61e841bd6e799e67ba16549e4a478a9fcfb7a26f",
    FILES["round100_source"]: "be5c7d9413f03810210eea8b8d2eb37a9256886f0a339cdcd4ddcf1d32c1e224",
}
WORK_CORES: tuple[Any, ...] = ()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_closed(path: Path, schema: str) -> dict[str, Any]:
    document = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError(f"non-closed dependency: {path.name}")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError(f"invalid dependency envelope: {path.name}")
    return document["result"]


def init_worker(precision_bits: int) -> None:
    global WORK_CORES
    ctx.prec = precision_bits
    WORK_CORES = tuple(core_cert.physical_cores())
    round87.WORK_CORES = WORK_CORES
    round87.physical_type = round100.immutable_physical_type


def audit_arc(task: tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]) -> tuple[int, dict[str, Any]]:
    index, link, pair, left, right = task
    row = round89.certify_gap(left, right, WORK_CORES)
    if row["left_registered_port_id"] != link["left_registered_port_id"]:
        raise RuntimeError("left endpoint changed")
    if row["right_registered_port_id"] != link["right_registered_port_id"]:
        raise RuntimeError("right endpoint changed")
    if row["whole_chain_two_collision_status"] != "SURVIVE_THROUGH_2_INNER":
        raise RuntimeError("two-collision chain changed")
    if row["whole_chain_third_event_status"] != "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION":
        raise RuntimeError("third tangent event changed")
    if row["complete_translated_candidate_count_histogram"] != {57: row["strip_count"]}:
        raise RuntimeError("complete immutable candidate accounting changed")
    identity = {
        "face_id": link["face_id"],
        "link_rank": link["link_rank"],
        "left_registered_port_id": link["left_registered_port_id"],
        "right_registered_port_id": link["right_registered_port_id"],
        "physical_root_component_id": pair["physical_root_component_id"],
    }
    return index, {
        "registered_arc_reaudit_id": "physical-s0-rank3-registered-arc-immutable-reaudit:" + digest(identity),
        **identity,
        "source_core_index": row["source_core_index"],
        "second_selected_target_id": row["second_selected_target_id"],
        "third_candidate_id": row["third_candidate_id"],
        "signed_transverse_tangency_factor_sign": row["signed_transverse_tangency_factor_sign"],
        "strip_count": row["strip_count"],
        "dependent_collar_depth": row["dependent_collar_depth"],
        "implicit_graph_axis": row["implicit_graph_axis"],
        "certified_tube_boxes_sha256": row["certified_tube_boxes_sha256"],
        "strip_sign_rows_sha256": row["strip_sign_rows_sha256"],
        "whole_chain_two_collision_status": row["whole_chain_two_collision_status"],
        "whole_chain_third_event_status": row["whole_chain_third_event_status"],
        "complete_translated_candidate_count_histogram": row["complete_translated_candidate_count_histogram"],
        "whole_chain_competitor_rows_sha256": row["whole_chain_competitor_rows_sha256"],
        "immutable_candidate_table_materialization": "TUPLE_BEFORE_MEMBERSHIP_OR_ITERATION",
        "tangent_face_whole_tube_complete_candidate_chain_certified": True,
        "transverse_D_sign_side_cell_asserted": False,
        "homogeneity_child_asserted": False,
        "Gate5_field_installed": False,
    }


def build(precision_bits: int = PRECISION_BITS, workers: int = 8) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    round99 = load_closed(
        HERE / FILES["round99"], "cm2.round99.rank3-registered-port-candidate-audit.v1"
    )
    round102 = load_closed(
        HERE / FILES["round102"], "cm2.round102.rank3-corrected-face-quotient.v1"
    )
    event_rows, historical_pair_rows = round89.load()
    event_by_id = {row["registered_port_id"]: row for row in event_rows}
    corrected_ids = set(round99["corrected_locally_physical_registered_port_ids"])
    pair_by_endpoints = {
        frozenset(row["registered_elementary_arc_endpoint_port_ids"]): row
        for row in historical_pair_rows
    }
    links = sorted(
        (
            row for row in round102["interior_link_rows"]
            if row["link_type"] == "REGISTERED_PHYSICAL_ARC"
        ),
        key=lambda row: (row["face_id"], row["link_rank"]),
    )
    if len(links) != 52:
        raise RuntimeError("Round102 registered-arc accounting changed")
    tasks = []
    for index, link in enumerate(links):
        endpoints = frozenset((link["left_registered_port_id"], link["right_registered_port_id"]))
        if endpoints not in pair_by_endpoints or not endpoints <= corrected_ids:
            raise RuntimeError("registered link lacks corrected historical pair")
        pair = pair_by_endpoints[endpoints]
        if pair["physical_root_component_id"] != link["evidence_id"]:
            raise RuntimeError("Round102 registered-arc component evidence mismatch")
        tasks.append((
            index, link, pair,
            event_by_id[link["left_registered_port_id"]],
            event_by_id[link["right_registered_port_id"]],
        ))
    context = mp.get_context("fork")
    with context.Pool(
        min(workers, os.cpu_count() or 1),
        initializer=init_worker,
        initargs=(precision_bits,),
    ) as pool:
        raw = list(pool.imap_unordered(audit_arc, tasks))
    raw.sort(key=lambda item: item[0])
    rows = [row for _, row in raw]
    total_strips = sum(row["strip_count"] for row in rows)
    result = {
        "precision_bits": precision_bits,
        "input_corrected_face_count": round102["corrected_rank3_physical_face_count"],
        "input_registered_physical_arc_link_count": len(links),
        "certified_registered_arc_whole_tube_count": len(rows),
        "remaining_unaudited_registered_arc_count": len(links) - len(rows),
        "whole_tube_strip_count": total_strips,
        "complete_immutable_candidate_tuple_replay_count": total_strips,
        "complete_translated_candidate_equation_count": 57 * total_strips,
        "complete_nontarget_competitor_equation_count": 56 * total_strips,
        "strip_count_histogram": dict(sorted(Counter(row["strip_count"] for row in rows).items())),
        "dependent_collar_depth_histogram": dict(sorted(Counter(row["dependent_collar_depth"] for row in rows).items())),
        "implicit_graph_axis_histogram": dict(sorted(Counter(row["implicit_graph_axis"] for row in rows).items())),
        "registered_arc_rows": rows,
        "registered_arc_rows_sha256": digest(rows),
        "strict_scope": "immutable complete-candidate IFT whole-tube chain reaudit of all 52 REGISTERED_PHYSICAL_ARC links in the corrected Round102 tangent-face quotient",
        "strict_nonclaims": [
            "no transverse D-positive or D-negative adjacent-cell collar is certified by this tangent-face audit",
            "no homogeneous operator child or official Gate5 word-key crosswalk is materialized",
            "no cell-keyed F1-F6 slot, RN block, or global gate is installed",
            "the 56 immutable gap links and exterior endpoint collars are outside this registered-arc-only certificate",
        ],
        "upstream_and_executable_pins": PINS,
    }
    if len(rows) != 52 or total_strips != 41984:
        raise RuntimeError("registered-arc whole-tube census changed")
    if Counter(row["strip_count"] for row in rows) != Counter({1024: 36, 512: 8, 128: 8}):
        raise RuntimeError("registered-arc strip census changed")
    if Counter(row["dependent_collar_depth"] for row in rows) != Counter({16: 28, 12: 24}):
        raise RuntimeError("registered-arc collar census changed")
    if Counter(row["implicit_graph_axis"] for row in rows) != Counter({"t_as_function_of_p": 52}):
        raise RuntimeError("registered-arc IFT-axis census changed")
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build(args.precision_bits, args.workers), sort_keys=True, indent=2) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
