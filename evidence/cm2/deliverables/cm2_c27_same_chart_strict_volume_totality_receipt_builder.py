#!/usr/bin/env python3
"""Final zero-credit receipt builder for the strict-volume SAME_CHART subgate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_same_chart_strict_volume_totality_v1"
RESULT = PREFIX + "_result.json"
LEDGERS = [
    PREFIX + "_witness_occurrences.jsonl.gz",
    PREFIX + "_member_pairs.jsonl.gz",
    PREFIX + "_component_edges.jsonl.gz",
    PREFIX + "_affected_clusters.jsonl.gz",
]


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(2 << 20):
            h.update(block)
    return h.hexdigest()


def closed_json(path: Path, closure: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n"), "newline:" + path.name)
    value = json.loads(raw)
    need(canonical(value) + b"\n" == raw, "canonical:" + path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(claimed == digest(body), "closure:" + path.name)
    return value


def run_result(run_dir: Path) -> tuple[dict[str, Any], Path]:
    need((run_dir / "exit_code.txt").read_text().strip() == "0", "numeric exit:" + run_dir.name)
    need((run_dir / "stderr.txt").read_bytes() == b"", "stderr empty:" + run_dir.name)
    need("Exit status: 0" in (run_dir / "time.txt").read_text(), "time exit:" + run_dir.name)
    candidate = run_dir / "candidate"
    result = closed_json(candidate / RESULT, "result_sha256")
    stdout = (run_dir / "stdout.json").read_bytes()
    need(stdout.endswith(b"\n") and canonical(json.loads(stdout)) + b"\n" == stdout, "stdout canonical:" + run_dir.name)
    return result, candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-a", required=True)
    parser.add_argument("--run-b", required=True)
    parser.add_argument("--verification-a", required=True)
    parser.add_argument("--verification-b", required=True)
    parser.add_argument("--attack", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run_a, run_b = Path(args.run_a).resolve(), Path(args.run_b).resolve()
    result_a, candidate_a = run_result(run_a)
    result_b, candidate_b = run_result(run_b)
    need(result_a["seed"] != result_b["seed"], "distinct real producer seeds")
    need(result_a["semantic_projection_sha256"] == result_b["semantic_projection_sha256"], "producer semantic replay")
    ledger_pins = {}
    for filename in LEDGERS:
        left, right = file_sha(candidate_a / filename), file_sha(candidate_b / filename)
        need(left == right, "byte-identical double-seed ledger:" + filename)
        need(left == result_a["census"]["ledgers"][filename]["sha256"] == result_b["census"]["ledgers"][filename]["sha256"], "result ledger pin:" + filename)
        ledger_pins[filename] = {"sha256": left, "row_count": result_a["census"]["ledgers"][filename]["row_count"], "byte_identical_across_producer_seeds": True}

    verification_a = closed_json(Path(args.verification_a).resolve(), "verification_sha256")
    verification_b = closed_json(Path(args.verification_b).resolve(), "verification_sha256")
    need(verification_a["verification_seed"] != verification_b["verification_seed"], "distinct verifier seeds")
    need(verification_a["candidate_semantic_projection_sha256"] == verification_b["candidate_semantic_projection_sha256"] == result_a["semantic_projection_sha256"], "verifier semantic match")
    need(verification_a["cross_component_strict_pair_count"] == verification_b["cross_component_strict_pair_count"] == 32240, "verifier pair count")
    attack = closed_json(Path(args.attack).resolve(), "result_sha256")
    need(attack["attack_count"] == attack["rejected_count"] and attack["attack_count"] >= 28, "all coherent attacks reject")
    need(any(row["attack"] == "cross_chart_injection" and row["rejected"] for row in attack["attacks"]), "cross-chart attack")
    need(any(row["attack"] == "drop_chart_partition" and row["rejected"] for row in attack["attacks"]), "chart-partition attack")
    failed_diagnosis = ROOT.parent / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run2/failure_diagnosis.json"
    need(file_sha(failed_diagnosis) == "ab5499a0e93aab58a963638862f06a9df0844050d0188b43f02c4d497744d75b", "failed-run diagnosis pin")

    source_files = [
        "cm2_c27_same_chart_strict_volume_totality_probe.py",
        "cm2_c27_same_chart_strict_volume_totality_independent_verifier.py",
        "cm2_c27_same_chart_strict_volume_totality_attack_harness.py",
        "cm2_c27_same_chart_strict_volume_totality_receipt_builder.py",
    ]
    sources = {filename: file_sha(ROOT / filename) for filename in source_files}
    census = result_a["census"]
    body = {
        "schema": "cm2.c27.same-chart-strict-volume-totality.v1.final-zero-credit-receipt.v1",
        "status": "PASS_STRICT_VOLUME_TOTALITY__228_BASELINE_PLUS_32012_INCREMENTAL_NONIDENTICAL_OCCURRENCES__14580_NOVEL_COMPONENT_EDGES__LOWER_DIMENSIONAL_CONTACTS_STILL_OPEN__ZERO_CREDIT",
        "scope": {
            "complete": "ALL_STRICT_INTERIOR_INTERSECTIONS_IN_T_P_S_ACROSS_SIX_PRIMITIVE_SUPPORT_KERNELS",
            "not_promoted": "DIM1_DIM2_CLOSURE_CONTACTS",
            "endpoint_bits_used_for_strict_volume": False,
        },
        "failed_predecessor_run": {
            "run": "c27-same-chart-strict-volume-v1-seed-30632101-run2",
            "diagnosis_sha256": "ab5499a0e93aab58a963638862f06a9df0844050d0188b43f02c4d497744d75b",
            "cause": "SINGLE_RTREE_QUERY_OMITTED_CHART_PARTITION",
            "authority": "FAILED_RUN_ONLY",
        },
        "producer_replay": {
            "seeds": [result_a["seed"], result_b["seed"]],
            "semantic_projection_sha256": result_a["semantic_projection_sha256"],
            "result_file_sha256": [file_sha(candidate_a / RESULT), file_sha(candidate_b / RESULT)],
            "ledgers": ledger_pins,
        },
        "independent_sweep_verification": {
            "seeds": [verification_a["verification_seed"], verification_b["verification_seed"]],
            "verification_object_sha256": [verification_a["verification_sha256"], verification_b["verification_sha256"]],
            "algorithm": "DIRECT_SOURCE_STRICT_T_SWEEP_ACTIVE_SET_THEN_EXACT_P_S_RANK_COMPARISON__NO_SQLITE_NO_RTREE",
        },
        "coherent_attacks": {
            "attack_count": attack["attack_count"],
            "rejected_count": attack["rejected_count"],
            "attack_result_sha256": attack["result_sha256"],
            "includes_cross_chart_injection_and_drop_chart_partition": True,
        },
        "exact_census": {
            "primitive_atom_count": census["primitive_atom_count"],
            "all_component_strict_intersection_pair_count": census["all_component_strict_intersection_pair_count"],
            "same_C15_component_strict_intersection_pair_count": census["same_C15_component_strict_intersection_pair_count"],
            "cross_C15_component_strict_intersection_pair_count": census["cross_C15_component_strict_intersection_pair_count"],
            "source_pair_census": census["cross_component_source_pair_census"],
            "known_228_exact_equal_baseline_occurrence_count": census["known_exact_equal_baseline_occurrence_count"],
            "incremental_nonidentical_overlap_occurrence_count": census["incremental_nonidentical_overlap_occurrence_count"],
            "unique_cross_component_member_pair_count": census["unique_cross_component_member_pair_count"],
            "union_component_edge_count": census["union_component_edge_count"],
            "known_baseline_component_edge_count": census["known_baseline_component_edge_count"],
            "incremental_component_edge_count": census["incremental_component_edge_count"],
            "baseline_and_incremental_edge_overlap_count": census["baseline_and_incremental_edge_overlap_count"],
            "novel_component_edge_count_beyond_known_228": census["novel_component_edge_count_beyond_known_228"],
            "affected_old_C15_component_vertex_count": census["affected_old_C15_component_vertex_count"],
            "affected_cluster_count": census["affected_cluster_count"],
            "forced_DSU_rank_reduction": census["forced_DSU_rank_reduction"],
            "provisional_component_count_after_strict_volume_edges_only": census["provisional_component_count_after_strict_volume_edges_only"],
        },
        "sources": sources,
        "forbidden_inputs": result_a["forbidden_inputs"],
        "authority": "PROVISIONAL_WITNESS_EVIDENCE__C27_TO_C29_REBUILD_REQUIRED__NOT_MAXIMALITY__NOT_A_FORMAL_SEAL",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    Path(args.output).resolve().write_bytes(canonical(receipt) + b"\n")
    print(canonical(receipt).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
