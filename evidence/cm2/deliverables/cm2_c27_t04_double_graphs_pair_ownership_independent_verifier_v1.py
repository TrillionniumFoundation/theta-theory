#!/usr/bin/env python3
"""No-producer-import verifier for the T04 pair ownership materialization."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
AUDIT = WORKSPACE / ".cm2-runtime" / "audit"
ALIAS_SOURCE = ROOT / "cm2_c27_alias_rechart_handoff_zero_credit_probe.py"
GRAPH = AUDIT / "c27-graph-side-t0-independent-seed-30627018" / "ledger.jsonl.gz"
LOWER = AUDIT / "c27-lower-owner-v2-debug-30627202" / "cm2_c27_lower_owner_shadow_transfer_zero_credit_v1_contact_ledger.jsonl.gz"

BUCKET_CROSS = "CROSS_CHART_QUOTIENT_RECHART"
BUCKET_TRANSVERSE = "SAME_CHART_TRANSVERSE_1D"
BUCKET_GRAPH = "CROSS_CHART_GRAPH_SIDE_T0"
BUCKET_LOWER = "CODIMENSION_TWO_LOWER_OWNER"
EXPECTED = {BUCKET_CROSS: 1_361_424, BUCKET_TRANSVERSE: 448,
            BUCKET_GRAPH: 192, BUCKET_LOWER: 24}


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


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("cm2_t04_independent_alias_v1", path)
    need(spec is not None and spec.loader is not None, "alias module spec")
    item = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(item)
    return item


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            need(line.endswith("\n"), "jsonl newline:" + str(path))
            yield json.loads(line)


def closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), "row closure:" + label)


def next_row(stream: Iterator[dict[str, Any]], ordinal: int) -> dict[str, Any]:
    try:
        row = next(stream)
    except StopIteration as exc:
        raise Reject("candidate omission at ordinal:" + str(ordinal)) from exc
    closed(row, str(ordinal))
    need(row.get("pair_owner_count") == 1
         and row.get("pair_owner_terminal") == "T04_DOUBLE_GRAPHS"
         and row.get("resolved") is True and row.get("unresolved") is False
         and row.get("legal_cross_component_same_physical_point_witness") is False
         and row.get("formal_credit") == 0, "common row contract:" + str(ordinal))
    identity = {"T04_terminal": "DOUBLE_GRAPHS", "bucket": row["bucket"],
                "candidate_key": row["candidate_key"]}
    need(row["candidate_id"] == "t04-double-graphs-pair:" + digest(identity)
         and row["candidate_key_sha256"] == digest(row["candidate_key"]),
         "candidate identity:" + str(ordinal))
    return row


def primitive(a: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    a.validate_small_authorities()
    sheets, _ = a.reconstruct_source_sheets()
    cells, _, transverse = a.load_physical_cells()
    a.bind_transverse_boxes(cells, transverse)
    sheets.sort(key=lambda row: row["member_id"])
    cells.sort(key=lambda row: (row["disposition_row_id"],
                                row["physical_witness_cell_index"],
                                row["cell_sha256"]))
    need(len(sheets) == 16 and len({row["member_id"] for row in sheets}) == 16,
         "independent 16 sheets")
    need(len(cells) == 113_452 and len({row["key"] for row in cells}) == 113_452,
         "independent 113452 cells")
    return sheets, cells


def verify_primitive(stream: Iterator[dict[str, Any]], a: Any,
                     sheets: list[dict[str, Any]], cells: list[dict[str, Any]],
                     start: int, census: Counter[str]) -> int:
    ordinal = start
    min_gap: Fraction | None = None
    for cell in cells:
        bounds = [Fraction(value) for value in cell["exact_containing_t_p_s_bounds"]]
        t0, t1, p0, p1, _, _ = bounds
        for sheet in sheets:
            expected_key = {
                "source_sheet_member_id": sheet["member_id"],
                "R291_disposition_row_id": cell["disposition_row_id"],
                "R291_physical_witness_cell_index": cell["physical_witness_cell_index"],
                "R291_physical_witness_cell_sha256": cell["cell_sha256"],
            }
            if sheet["chart"] != cell["chart"]:
                row = next_row(stream, ordinal); ordinal += 1
                census[row["bucket"]] += 1
                need(row["bucket"] == BUCKET_CROSS and row["candidate_key"] == expected_key,
                     "cross pair totality/order")
                relation = a.chart_relation(sheet["chart"], cell["chart"])
                proof = row["exact_physical_proof"]
                need(proof["source_chart"] == sheet["chart"]
                     and proof["target_chart"] == cell["chart"]
                     and proof["target_t_envelope"] == [str(t0), str(t1)]
                     and proof["chart_relation"] == relation["relation"],
                     "cross primitive binding")
                if relation["relation"] == "OPPOSITE_DOMINANT_CHART":
                    margin = Fraction(1) - max(abs(t0), abs(t1)) ** 2
                    need(row["exact_disposition_route"]
                         == "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_STRICT_SIGN"
                         and Fraction(proof["target_radical_square_minimum_margin"]) == margin > 0
                         and proof["normal_position_solution_set"] == "EMPTY",
                         "opposite exact sign proof")
                else:
                    required = Fraction(relation["required_target_t"])
                    gap = required - t1 if required == 1 else t0 - required
                    need(row["exact_disposition_route"]
                         == "EXACT_NONINCIDENCE__PERPENDICULAR_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT"
                         and Fraction(proof["required_target_t"]) == required
                         and Fraction(proof["exact_gap_from_required_endpoint"]) == gap > 0
                         and proof["normal_position_solution_set"] == "EMPTY_ON_DECLARED_ENVELOPE",
                         "perpendicular endpoint proof")
            elif cell["witness_kind"] == "ROUND182_TRANSVERSE_1D_LINE":
                row = next_row(stream, ordinal); ordinal += 1
                census[row["bucket"]] += 1
                need(row["bucket"] == BUCKET_TRANSVERSE
                     and row["candidate_key"] == expected_key
                     and row["exact_disposition_route"]
                        == "EXACT_NONINCIDENCE__STRICT_RATIONAL_P_GAP",
                     "transverse pair totality/order")
                base = [Fraction(value) for value in sheet["exact_closed_p_s_rectangle"]]
                if base[1] < p0:
                    order, gap = "SOURCE_P_STRICTLY_LEFT", p0 - base[1]
                else:
                    need(p1 < base[0], "independent strict transverse order")
                    order, gap = "TRANSVERSE_P_STRICTLY_LEFT", base[0] - p1
                proof = row["exact_physical_proof"]
                need(proof["source_sheet_closed_p_interval"] == [str(base[0]), str(base[1])]
                     and proof["transverse_containing_p_interval"] == [str(p0), str(p1)]
                     and proof["strict_p_order"] == order
                     and Fraction(proof["exact_p_gap"]) == gap > 0
                     and proof["actual_transverse_support_subset_of_declared_envelope"] is True
                     and proof["same_point_solution_set"] == "EMPTY",
                     "transverse independent p-gap proof")
                min_gap = gap if min_gap is None else min(min_gap, gap)
    need(min_gap == Fraction(35, 64), "independent minimum transverse p gap")
    return ordinal


def graph_expected() -> list[dict[str, Any]]:
    raw = list(rows(GRAPH))
    need(len(raw) == 192, "independent graph rows")
    output = []
    for row in raw:
        closed(row, "graph source")
        need(row["sheet_chart"] != row["side_chart"]
             and row["sheet_normal"] != row["side_normal"]
             and row["sheet_position"] != row["side_position"]
             and row["route"] == "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH",
             "graph source exact proof")
        output.append({key: row[key] for key in (
            "sheet_member_id", "side_member_id", "sheet_chart", "side_chart",
            "sheet_normal", "side_normal", "sheet_position", "side_position")})
    return sorted(output, key=encode)


def lower_expected() -> list[dict[str, Any]]:
    raw = list(rows(LOWER))
    need(len(raw) == 24, "independent lower rows")
    output = []
    for row in raw:
        closed(row, "lower source")
        handoff = row["layer_B_lower_owner_physical_support_component_handoff"]
        output.append({
            "key": [row["source_sheet_member_id"], row["target_registry_occurrence_id"],
                    row["R291_disposition_row_id"], row["R291_physical_witness_cell_index"]],
            "chart": row["chart"],
            "point": row["contact_locus"]["representative_t_p_s"],
            "target_bounds": row["target_normalized_support_ast"]["bounds"],
            "covering_members": handoff["covering_member_ids"],
            "covering_member_count": handoff["covering_member_count"],
            "owner_component": handoff["unique_C15_component_id"],
            "source_component": row["source_sheet_component_id"],
            "target_component": row["target_component_id"],
            "witness": bool(handoff["cross_component_same_physical_point_witness"]),
        })
    return output


def verify_small(stream: Iterator[dict[str, Any]], start: int,
                 census: Counter[str]) -> int:
    ordinal = start
    for source in graph_expected():
        row = next_row(stream, ordinal); ordinal += 1
        census[row["bucket"]] += 1
        key = {"source_sheet_member_id": source["sheet_member_id"],
               "target_graph_side_member_id": source["side_member_id"]}
        proof = row["exact_physical_proof"]
        need(row["bucket"] == BUCKET_GRAPH and row["candidate_key"] == key
             and row["exact_disposition_route"]
                == "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH"
             and proof["source_chart"] == source["sheet_chart"]
             and proof["target_chart"] == source["side_chart"]
             and proof["source_normal"] == source["sheet_normal"]
             and proof["target_normal"] == source["side_normal"]
             and proof["source_position"] == source["sheet_position"]
             and proof["target_position"] == source["side_position"]
             and proof["same_point_solution_set"] == "EMPTY",
             "graph normalized proof")
    for source in sorted(lower_expected(), key=encode):
        row = next_row(stream, ordinal); ordinal += 1
        census[row["bucket"]] += 1
        key = {
            "source_sheet_member_id": source["key"][0],
            "target_registry_occurrence_id": source["key"][1],
            "R291_disposition_row_id": source["key"][2],
            "R291_physical_witness_cell_index": source["key"][3],
        }
        proof = row["exact_physical_proof"]
        point = source["point"]
        bounds = source["target_bounds"]
        need(row["bucket"] == BUCKET_LOWER and row["candidate_key"] == key
             and row["exact_disposition_route"]
                == "EXACT_NONEDGE__OPEN_TARGET_EXCLUSION_AND_UNIQUE_SOURCE_COMPONENT_T0_OWNER"
             and proof["contact_point_t_p_s"] == point
             and proof["target_open_support_bounds"] == bounds
             and proof["covering_member_ids"] == source["covering_members"]
             and proof["covering_member_count"] == source["covering_member_count"]
             and proof["unique_owner_component_id"] == source["owner_component"]
             and proof["source_component_id"] == source["source_component"]
             and proof["target_component_id"] == source["target_component"]
             and point[0] == "0" and Fraction(bounds[0]) == 0 < Fraction(bounds[1])
             and proof["target_open_support_contains_contact"] is False
             and proof["complete_t0_owner_component_equals_source_component"] is True
             and proof["same_point_cross_component_witness"] is False,
             "lower normalized owner proof")
    return ordinal


def validate_candidate(directory: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    ledger = directory / "t04_double_graphs_1362088_pair_ownership.jsonl.gz"
    witness = directory / "t04_double_graphs_legal_cross_component_physical_witnesses.jsonl.gz"
    result_path = directory / "result.json"
    manifest_path = directory / "manifest.json"
    document = json.loads(result_path.read_bytes())
    need(document.get("result_sha256") == digest(document["result"]), "result closure")
    result = document["result"]
    manifest_doc = json.loads(manifest_path.read_bytes())
    manifest = manifest_doc["manifest"]
    need(manifest_doc["manifest_sha256"] == digest(manifest), "manifest closure")
    by_path = {entry["path"]: entry for entry in manifest["members"]}
    for path in (ledger, witness, result_path):
        item = by_path[path.name]
        need(item["sha256"] == file_sha(path) and item["size"] == path.stat().st_size,
             "manifest member:" + path.name)
    need(result["pair_contract"]["candidate_ledger_file_sha256"] == file_sha(ledger)
         and result["physical_witness_contract"]["empty_witness_ledger_file_sha256"] == file_sha(witness),
         "result file binding")
    with gzip.open(witness, "rb") as stream:
        need(stream.read(1) == b"", "physical witness ledger empty")
    a = load_module(ALIAS_SOURCE)
    sheets, cells = primitive(a)
    stream = rows(ledger)
    census: Counter[str] = Counter()
    ordinal = verify_primitive(stream, a, sheets, cells, 0, census)
    ordinal = verify_small(stream, ordinal, census)
    try:
        extra = next(stream)
    except StopIteration:
        extra = None
    need(extra is None, "no duplicate/trailing candidate")
    a.close_capture_fds()
    need(ordinal == 1_362_088 and dict(census) == EXPECTED,
         "full exact pair census")
    contract = result["pair_contract"]
    need(contract["candidate_pairs"] == ordinal
         and contract["bucket_census"] == EXPECTED
         and contract["bucket_sum"] == ordinal
         and contract["pair_owner_count_for_every_row"] == 1
         and contract["buckets_mutually_exclusive_by_typed_primitive_key"] is True
         and contract["every_candidate_resolved"] is True
         and contract["unresolved"] == 0
         and contract["legal_cross_component_same_physical_point_witnesses"] == 0,
         "result exact pair contract")
    return result, {"ledger_sha256": file_sha(ledger),
                    "witness_sha256": file_sha(witness),
                    "result_sha256": file_sha(result_path),
                    "manifest_sha256": file_sha(manifest_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-a", required=True)
    parser.add_argument("--candidate-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(not output.exists(), "fresh verifier output")
    a_result, a_files = validate_candidate(Path(args.candidate_a))
    b_result, b_files = validate_candidate(Path(args.candidate_b))
    need(a_files == b_files and a_result == b_result, "dual-seed byte and semantic identity")
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.pair-ownership-independent-verification.v1",
        "status": "PASS_TWO_INDEPENDENT_SEMANTIC_RECONSTRUCTIONS_DUAL_SEED_1362088_EXACT_PAIR_OWNERSHIP_ZERO_WITNESS",
        "candidate_pairs": 1_362_088, "bucket_census": EXPECTED,
        "unresolved": 0, "legal_cross_component_witnesses": 0,
        "dual_seed_all_candidate_files_byte_identical": True,
        "producer_source_imported": False,
        "independent_cross_chart_implementation": "PRIMITIVE_CHART_RELATION_AND_FIXED_SET_EQUATIONS",
        "independent_transverse_implementation": "DIRECT_RATIONAL_INTERVAL_PROJECTION",
        "graph_and_lower_second_primitive_reconstruction_bound": True,
        "old_C27_FAMILIES_or_transition_C28_C29_read": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
        "candidate_file_sha256": a_files,
        "formal_credit": 0, "manifest_authorized": False,
    }
    wrapper = {**body, "verification_sha256": digest(body)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encode(wrapper) + b"\n")
    print(encode(wrapper).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_INDEPENDENT_VERIFIER_REJECT:" + str(exc))
        raise SystemExit(2)
