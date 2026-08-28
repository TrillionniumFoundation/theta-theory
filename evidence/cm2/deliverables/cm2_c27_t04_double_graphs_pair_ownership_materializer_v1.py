#!/usr/bin/env python3
"""Materialize the fresh primitive T04/DOUBLE_GRAPHS pair denominator.

This is deliberately a zero-credit, append-only authority candidate.  It does
not read Round306C27 FAMILIES, a transition ledger, C28, C29, or any component
edge ledger.  The large two buckets are regenerated from the primitive source
sheet x R291 physical-cell product.  The 192 graph-side and 24 lower-owner
buckets are admitted only after the already independent P0-A projections agree
exactly and their coherent attack suite passes.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
AUDIT = WORKSPACE / ".cm2-runtime" / "audit"

Q_SOURCE = ROOT / "cm2_c27_explicit_quotient_map_alias_zero_credit_probe_v2.py"
P0_SOURCE = ROOT / "cm2_c27_p0a_192_24_semantic_attack_harness.py"

GRAPH_V4 = AUDIT / "c27-semantic-double-graphs-v4-seed-30627931" / "cm2_c27_semantic_counterexample_gate_double_graphs_zero_credit_v2_candidate_partition_ledger.jsonl.gz"
GRAPH_INDEPENDENT = AUDIT / "c27-graph-side-t0-independent-seed-30627918" / "ledger.jsonl.gz"
LOWER_V2 = AUDIT / "c27-lower-owner-v2-seed-30627971" / "cm2_c27_lower_owner_shadow_transfer_zero_credit_v1_contact_ledger.jsonl.gz"

Q_FINALS = (
    AUDIT / "c27-explicit-quotient-map-alias-v2-final-seed-30627301",
    AUDIT / "c27-explicit-quotient-map-alias-v2-final-seed-30627981",
)
TRANSVERSE_FINALS = (
    AUDIT / "c27-same-chart-transverse-1d-zero-credit-seed-30627101",
    AUDIT / "c27-same-chart-transverse-1d-zero-credit-seed-30627991",
)
GRAPH_FINALS = (
    AUDIT / "c27-graph-side-t0-independent-seed-30627018",
    AUDIT / "c27-graph-side-t0-independent-seed-30627918",
)
LOWER_FINALS = (
    AUDIT / "c27-lower-owner-v2-debug-30627202",
    AUDIT / "c27-lower-owner-v2-seed-30627971",
)

BUCKET_CROSS = "CROSS_CHART_QUOTIENT_RECHART"
BUCKET_TRANSVERSE = "SAME_CHART_TRANSVERSE_1D"
BUCKET_GRAPH = "CROSS_CHART_GRAPH_SIDE_T0"
BUCKET_LOWER = "CODIMENSION_TWO_LOWER_OWNER"
EXPECTED = {
    BUCKET_CROSS: 1_361_424,
    BUCKET_TRANSVERSE: 448,
    BUCKET_GRAPH: 192,
    BUCKET_LOWER: 24,
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, "module spec:" + name)
    item = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(item)
    return item


def gz_rows(path: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            need(line.endswith("\n"), "jsonl newline:" + str(path))
            row = json.loads(line)
            if "row_sha256" in row:
                body = dict(row)
                claim = body.pop("row_sha256")
                need(claim == digest(body), "row closure:" + str(path))
            output.append(row)
    return output


def audit_wrapped_manifest(directory: Path) -> dict[str, Any]:
    manifests = sorted(directory.glob("*manifest.json"))
    need(len(manifests) == 1, "one wrapped manifest:" + str(directory))
    document = json.loads(manifests[0].read_bytes())
    body = document.get("manifest")
    need(type(body) is dict and document.get("manifest_sha256") == digest(body),
         "manifest object closure:" + str(directory))
    members = body.get("members")
    need(type(members) is list and body.get("member_count") == len(members),
         "manifest member count:" + str(directory))
    for entry in members:
        path = directory / entry["name"]
        need(path.is_file() and path.stat().st_size == entry["size"]
             and file_sha(path) == entry["sha256"],
             "manifest member closure:" + str(path))
    return {
        "directory": str(directory.relative_to(WORKSPACE)),
        "manifest_file_sha256": file_sha(manifests[0]),
        "manifest_object_sha256": document["manifest_sha256"],
        "member_count": len(members),
    }


def audit_plain_graph(directory: Path) -> dict[str, Any]:
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes())
    ledger = directory / "ledger.jsonl.gz"
    result = directory / "result.json"
    need(manifest["ledger_sha256"] == file_sha(ledger)
         and manifest["result_sha256"] == file_sha(result),
         "plain graph manifest closure:" + str(directory))
    return {
        "directory": str(directory.relative_to(WORKSPACE)),
        "manifest_file_sha256": file_sha(manifest_path),
        "ledger_file_sha256": manifest["ledger_sha256"],
        "result_file_sha256": manifest["result_sha256"],
    }


def audit_existing_subgates() -> dict[str, Any]:
    q = [audit_wrapped_manifest(path) for path in Q_FINALS]
    t = [audit_wrapped_manifest(path) for path in TRANSVERSE_FINALS]
    g = [audit_plain_graph(path) for path in GRAPH_FINALS]
    l = [audit_wrapped_manifest(path) for path in LOWER_FINALS]
    need(q[0]["manifest_object_sha256"] == q[1]["manifest_object_sha256"],
         "quotient dual-seed manifest objects")
    need(t[0]["manifest_object_sha256"] == t[1]["manifest_object_sha256"],
         "transverse dual-seed manifest objects")
    need(g[0]["ledger_file_sha256"] == g[1]["ledger_file_sha256"]
         and g[0]["result_file_sha256"] == g[1]["result_file_sha256"],
         "graph dual-seed bytes")
    need(l[0]["manifest_object_sha256"] == l[1]["manifest_object_sha256"],
         "lower dual-seed manifest objects")
    return {"quotient_rechart": q, "transverse_1d": t,
            "graph_side": g, "lower_owner": l}


def candidate_row(bucket: str, key: dict[str, Any], route: str,
                  proof: dict[str, Any]) -> dict[str, Any]:
    identity = {"T04_terminal": "DOUBLE_GRAPHS", "bucket": bucket,
                "candidate_key": key}
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.pair-ownership-row.v1",
        "T04_terminal": "DOUBLE_GRAPHS",
        "bucket": bucket,
        "candidate_id": "t04-double-graphs-pair:" + digest(identity),
        "candidate_key": key,
        "candidate_key_sha256": digest(key),
        "pair_owner_count": 1,
        "pair_owner_terminal": "T04_DOUBLE_GRAPHS",
        "exact_disposition_route": route,
        "exact_physical_proof": proof,
        "resolved": True,
        "unresolved": False,
        "legal_cross_component_same_physical_point_witness": False,
        "formal_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def prepare_primitive(q: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    q.validate_seed_runtime()
    q.validate_independent_input_boundary()
    q.validate_geometry_authorities()
    sheets, _ = q.reconstruct_source_sheets()
    q.action_fixed_set_audit(sheets)
    cells, _, transverse_ids = q.load_physical_cells()
    q.bind_transverse_boxes(cells, transverse_ids)
    sheets.sort(key=lambda row: row["member_id"])
    cells.sort(key=lambda row: (row["disposition_row_id"],
                                row["physical_witness_cell_index"],
                                row["cell_sha256"]))
    need(len(sheets) == 16 and len({row["member_id"] for row in sheets}) == 16,
         "primitive 16 sheets")
    need(len(cells) == 113_452
         and len({row["key"] for row in cells}) == 113_452,
         "primitive 113452 cells")
    return sheets, cells


def primitive_rows(q: Any, sheets: list[dict[str, Any]],
                   cells: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    cross = transverse = 0
    for cell in cells:
        bounds = [Fraction(value) for value in cell["exact_containing_t_p_s_bounds"]]
        t0, t1, p0, p1, s0, s1 = bounds
        need(Fraction(-1) < t0 <= t1 < Fraction(1), "strict primitive t envelope")
        for sheet in sheets:
            key = {
                "source_sheet_member_id": sheet["member_id"],
                "R291_disposition_row_id": cell["disposition_row_id"],
                "R291_physical_witness_cell_index": cell["physical_witness_cell_index"],
                "R291_physical_witness_cell_sha256": cell["cell_sha256"],
            }
            if sheet["chart"] != cell["chart"]:
                exact = q.solve_global_position_equation(sheet["chart"], cell["chart"], t0, t1)
                need(exact["target_t_solution_intersects_support"] is False,
                     "cross-chart empty exact solution")
                relation = exact["relation"]
                if relation == "OPPOSITE_DOMINANT_CHART":
                    route = "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_STRICT_SIGN"
                    proof = {
                        "implementation": "EXPLICIT_GLOBAL_PHASE_N_Q_EQUATIONS",
                        "source_chart": sheet["chart"], "target_chart": cell["chart"],
                        "target_t_envelope": [str(t0), str(t1)],
                        "chart_relation": relation,
                        "target_radical_square_minimum_margin": exact["target_radical_square_minimum_margin"],
                        "normal_position_solution_set": "EMPTY",
                    }
                else:
                    need(relation == "PERPENDICULAR_DOMINANT_CHART", "cross chart relation")
                    route = "EXACT_NONINCIDENCE__PERPENDICULAR_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT"
                    proof = {
                        "implementation": "EXPLICIT_GLOBAL_PHASE_N_Q_EQUATIONS",
                        "source_chart": sheet["chart"], "target_chart": cell["chart"],
                        "target_t_envelope": [str(t0), str(t1)],
                        "chart_relation": relation,
                        "required_target_t": exact["required_target_t"],
                        "exact_gap_from_required_endpoint": exact["exact_gap_from_required_endpoint"],
                        "normal_position_solution_set": "EMPTY_ON_DECLARED_ENVELOPE",
                    }
                cross += 1
                yield candidate_row(BUCKET_CROSS, key, route, proof)
            elif cell["witness_kind"] == "ROUND182_TRANSVERSE_1D_LINE":
                base = [Fraction(value) for value in sheet["closed_p_s_rectangle"]]
                if base[1] < p0:
                    order = "SOURCE_P_STRICTLY_LEFT"
                    gap = p0 - base[1]
                else:
                    need(p1 < base[0], "strict transverse p ordering")
                    order = "TRANSVERSE_P_STRICTLY_LEFT"
                    gap = base[0] - p1
                need(gap > 0, "strict transverse p gap")
                route = "EXACT_NONINCIDENCE__STRICT_RATIONAL_P_GAP"
                proof = {
                    "implementation": "DIRECT_INTERVAL_PROJECTION_GAP",
                    "source_chart": sheet["chart"], "target_chart": cell["chart"],
                    "source_sheet_closed_p_interval": [str(base[0]), str(base[1])],
                    "transverse_containing_p_interval": [str(p0), str(p1)],
                    "strict_p_order": order, "exact_p_gap": str(gap),
                    "actual_transverse_support_subset_of_declared_envelope": True,
                    "same_point_solution_set": "EMPTY",
                }
                transverse += 1
                yield candidate_row(BUCKET_TRANSVERSE, key, route, proof)
    need(cross == EXPECTED[BUCKET_CROSS], "cross-chart exact denominator")
    need(transverse == EXPECTED[BUCKET_TRANSVERSE], "transverse exact denominator")


def p0_rows(p0: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    v4 = gz_rows(GRAPH_V4)
    independent = gz_rows(GRAPH_INDEPENDENT)
    lower = gz_rows(LOWER_V2)
    graph_a = p0.graph1(v4)
    graph_b = p0.graph2(independent)
    p0.verify_graph(graph_a); p0.verify_graph(graph_b)
    need(sorted(graph_a, key=encode) == sorted(graph_b, key=encode),
         "graph two implementations exact")
    lower_a = p0.lower1(lower)
    lower_b = p0.lower2(v4)
    p0.verify_lower(lower_a); p0.verify_lower(lower_b)
    need(sorted(lower_a, key=encode) == sorted(lower_b, key=encode),
         "lower two implementations exact")
    attacks = p0.attack_suite(graph_b, lower_b)
    need(len(attacks) == 12 and all(attacks.values()), "P0-A 12 coherent attacks")
    return graph_b, lower_b, attacks


def small_rows(graph: list[dict[str, Any]], lower: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for source in sorted(graph, key=encode):
        key = {"source_sheet_member_id": source["sheet_member_id"],
               "target_graph_side_member_id": source["side_member_id"]}
        proof = {
            "implementation": "INDEPENDENT_T0_GLOBAL_PHASE_CARDINAL_NORMAL_SOLVER",
            "source_chart": source["sheet_chart"], "target_chart": source["side_chart"],
            "source_normal": source["sheet_normal"], "target_normal": source["side_normal"],
            "source_position": source["sheet_position"], "target_position": source["side_position"],
            "normal_and_position_equal": False,
            "same_point_solution_set": "EMPTY",
        }
        yield candidate_row(BUCKET_GRAPH, key,
                            "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH", proof)
    for source in sorted(lower, key=encode):
        key = {
            "source_sheet_member_id": source["key"][0],
            "target_registry_occurrence_id": source["key"][1],
            "R291_disposition_row_id": source["key"][2],
            "R291_physical_witness_cell_index": source["key"][3],
        }
        proof = {
            "implementation": "COMPLETE_T0_SOURCE_SHEET_OWNER_COMPONENT_COVER",
            "chart": source["chart"], "contact_point_t_p_s": source["point"],
            "target_open_support_bounds": source["target_bounds"],
            "covering_member_ids": source["covering_members"],
            "covering_member_count": source["covering_member_count"],
            "unique_owner_component_id": source["owner_component"],
            "source_component_id": source["source_component"],
            "target_component_id": source["target_component"],
            "target_open_support_contains_contact": False,
            "complete_t0_owner_component_equals_source_component": True,
            "same_point_cross_component_witness": False,
        }
        yield candidate_row(BUCKET_LOWER, key,
                            "EXACT_NONEDGE__OPEN_TARGET_EXCLUSION_AND_UNIQUE_SOURCE_COMPONENT_T0_OWNER", proof)


def write_gzip(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str, dict[str, int], dict[str, str]]:
    count = 0
    census: Counter[str] = Counter()
    states: dict[str, Any] = {}
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as stream:
            for row in rows:
                bucket = row["bucket"]
                state = states.setdefault(bucket, hashlib.sha256())
                payload = encode(row) + b"\n"
                stream.write(payload)
                state.update(payload)
                census[bucket] += 1
                count += 1
    return count, file_sha(path), dict(sorted(census.items())), {
        key: value.hexdigest() for key, value in sorted(states.items())}


def empty_witness_ledger(path: Path) -> str:
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0):
            pass
    return file_sha(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed in {"30627301", "30627981"}, "declared true seed")
    need(os.environ.get("PYTHONHASHSEED") == args.seed, "active true seed")
    output = Path(args.out_dir)
    need(not output.exists() and output.parent.resolve() == AUDIT.resolve(),
         "fresh direct audit output")

    existing = audit_existing_subgates()
    q = module(Q_SOURCE, "cm2_t04_explicit_q_v2")
    p0 = module(P0_SOURCE, "cm2_t04_p0_crosscheck")
    sheets, cells = prepare_primitive(q)
    graph, lower, attacks = p0_rows(p0)
    need(len(graph) == 192 and len(lower) == 24, "small bucket counts")

    output.mkdir(mode=0o700)
    ledger = output / "t04_double_graphs_1362088_pair_ownership.jsonl.gz"
    combined: Iterator[dict[str, Any]] = iter((*(),))
    def all_rows() -> Iterator[dict[str, Any]]:
        yield from primitive_rows(q, sheets, cells)
        yield from small_rows(graph, lower)
    count, ledger_sha, census, bucket_sequence_sha = write_gzip(ledger, all_rows())
    q.close_capture_fds()
    need(count == sum(EXPECTED.values()) == 1_362_088, "T04 pair count")
    need(census == EXPECTED, "T04 exact bucket census")
    witness_path = output / "t04_double_graphs_legal_cross_component_physical_witnesses.jsonl.gz"
    witness_sha = empty_witness_ledger(witness_path)

    source_pins = {
        str(Q_SOURCE.relative_to(WORKSPACE)): file_sha(Q_SOURCE),
        str(P0_SOURCE.relative_to(WORKSPACE)): file_sha(P0_SOURCE),
    }
    result = {
        "schema": "cm2.c27-independent.t04-double-graphs.pair-ownership-result.v1",
        "status": "PASS_T04_DOUBLE_GRAPHS_1362088_PAIR_LEVEL_TOTALITY_UNIQUE_OWNERSHIP_ZERO_WITNESS__ZERO_CREDIT_CANDIDATE",
        "decision": "PASS_CANDIDATE_PENDING_INDEPENDENT_NO_IMPORT_VERIFIER_AND_COHERENT_ATTACK_SEAL",
        "scope": {
            "terminal": "T04_DOUBLE_GRAPHS",
            "candidate_universe": "FRESH_PRIMITIVE_P0A_FOUR_BUCKET_DISJOINT_UNION_ONLY",
            "old_C27_FAMILIES_read_or_imported": False,
            "old_transition_ledger_read_or_imported": False,
            "C28_read_or_imported": False, "C29_read_or_imported": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
        },
        "pair_contract": {
            "candidate_pairs": count,
            "bucket_census": census,
            "bucket_sum": sum(census.values()),
            "pair_owner_count_for_every_row": 1,
            "buckets_mutually_exclusive_by_typed_primitive_key": True,
            "every_candidate_resolved": True,
            "unresolved": 0,
            "legal_cross_component_same_physical_point_witnesses": 0,
            "candidate_ledger_file_sha256": ledger_sha,
            "bucket_row_sequence_sha256": bucket_sequence_sha,
        },
        "physical_witness_contract": {
            "witness_count": 0,
            "empty_witness_ledger_file_sha256": witness_sha,
        },
        "P0A_existing_subgate_audit": existing,
        "P0A_graph_lower_cross_implementation": {
            "graph_pairs": 192, "lower_contacts": 24,
            "projection_exact_across_two_semantic_implementations": True,
            "coherent_attacks_rejected": len(attacks), "attacks": attacks,
        },
        "source_pins": source_pins,
        "active_seed_intentionally_omitted_for_byte_identity": True,
        "formal_credit": 0,
        "manifest_authorized": False,
        "strict_nonpromotion": {"C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED",
                                "C29": "UNAUTHORIZED", "Source_W": 80,
                                "CM2": "NO-GO_FOR_CLAIM"},
    }
    wrapper = {"result": result, "result_sha256": digest(result)}
    result_path = output / "result.json"
    result_path.write_bytes(encode(wrapper) + b"\n")
    members = []
    for path in (ledger, witness_path, result_path):
        members.append({"path": path.name, "sha256": file_sha(path),
                        "size": path.stat().st_size})
    manifest_body = {
        "schema": "cm2.c27-independent.t04-double-graphs.candidate-manifest.v1",
        "member_count": len(members), "members": members,
        "members_sha256": digest(members), "formal_credit": 0,
        "manifest_authorized": False,
    }
    manifest = {"manifest": manifest_body,
                "manifest_sha256": digest(manifest_body)}
    (output / "manifest.json").write_bytes(encode(manifest) + b"\n")
    print(encode({"status": result["status"], "pairs": count,
                  "ledger_sha256": ledger_sha,
                  "result_sha256": wrapper["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_MATERIALIZER_REJECT:" + str(exc))
        raise SystemExit(2)
