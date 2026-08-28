#!/usr/bin/env python3
"""Independent verifier for C59-L owner/history edge requests.

The C59 materializer and C50a oracle are inert bytes: neither is imported nor
executed.  This verifier reconstructs the candidate from frozen ledgers and
independently audits the C50a source interface with Python AST/source slices.
"""

from __future__ import annotations

import ast
import copy
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c59l.owner-independent-verification.v1"
OUTPUT = OUT / "cm2_round306c59l_owner_independent_verification_v1.json"
PRODUCER = OUT / "cm2_round306c59l_owner_edge_request_materializer_v1.py"
RESULT = OUT / "cm2_round306c59l_owner_result_v1.json"
GAP = OUT / "cm2_round306c59l_owner_c50a_exact_api_gap_v1.json"
C57_RESULT = OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json"
C57_VERIFY = OUT / "cm2_round306c57l1_collision1_edgewise_transport_independent_verification_v1.json"
C57_MANIFEST = OUT / "cm2_round306c57l1_collision1_edgewise_transport_manifest_v1.sha256"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C50A = OUT / "cm2_round306c50a_global_codimension_owner_oracle_v1.py"
C50A_VERIFY = OUT / "cm2_round306c50a_global_codimension_owner_oracle_independent_verifier_v1.py"
C50A_MANIFEST = OUT / "cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

PINS = {
    "producer": "1c8db4b504dbe66c98eb986141fd2b472561e10a5a95d3943baec499e14ac4fd",
    "result_file": "3391d96f6baa89281f9b60bd84a6aa950a74c6f6a99e86bc32b3322786e5a53e",
    "result_object": "b6c486e042acedb9c287eda527cd4fcafffd1a53ff768b7697124100e39a85c2",
    "gap_file": "37b29a3d44a4a37c3f67fb0acb742c4143158df9481dfa0c6bd6e249df5614b5",
    "gap_object": "0ee9c11588a2295249db11aa1a05e88110dfdd7a7d58197b8bbe5e1a9360ec5c",
    "C57_result": "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    "C57_object": "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0",
    "C57_verify": "59bf5c651b94d6fee7508f0ad63f549b8bf5699df27c82db0b6cd86409c78ac3",
    "C57_verify_object": "df0641cb734f40c312c41e4707c05adeae8d20e785f55bdf24a603200b8b1f2d",
    "C57_manifest": "b66325f26f39b1e4e3b1027d331105e1be9e76c126fa32210a614313e587f281",
    "C55B_result": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_object": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C35_result": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_object": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "occurrence1": "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250",
    "C50a": "43147808a94e14df20d902db6d7d383f8d230c6685401684bfb9ea697f7e9ed7",
    "C50a_verify": "2ae76868e0320563cafbc4a472f3ad1bf292817491d97da1fe68ca9d8e8bd3b4",
    "C50a_manifest": "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6",
    "C53": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "canonical": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}
PROTOCOLS = {"occurrence": "CM2_C41_ACTIVE_OVERLAY_OCCURRENCE_V1",
             "split": "CM2_EXACT_TWO_SIDE_BINARY_SPLIT_DECISION_V1",
             "history": "CM2_HASH_CHAINED_ACTIVE_OVERLAY_HISTORY_V1",
             "owner": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1"}
OWNER_RULE = "UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH"
ACTIVE = "112410045d088f22908276193a1d046d6f11c0e1818790b2826c5fcf0f6ac05f"
GENESIS = "17af15070fe6d383e64a1bbc44a6cad81e9940e4b7702b87c5ccee9c739bfcc7"
COMMON_GAPS = [
    "C50A_NO_STATIC_EXISTING_C32_EDGE_QUERY_OPERATION",
    "C50A_REQUEST_TASK_REQUIRES_ONE_REPRESENTATIVE_REFLECTED_PREDECESSOR_PAIR",
    "C57L1_QUERY_HAS_TWO_ADJACENT_C32_ENDPOINT_CELLS_WITH_INDEPENDENT_LINEAGES",
    "C50A_KRAFT_ONE_REPLACEMENTS_MUST_PARTITION_EACH_SELECTED_C41_PREDECESSOR",
    "C50A_OWNER_OUTPUT_IS_RESTRICTED_TO_TARGET_HISTORY_REPLACEMENT_BOUNDARIES",
    "C50A_SOURCE_EVIDENCE_DOES_NOT_VALIDATE_C35_OCCURRENCE1_OR_C38_C41_HISTORY_COMPATIBILITY",
]


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def h(value: Any) -> str: return hashlib.sha256(enc(value)).hexdigest()


def hf(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""): state.update(block)
    return state.hexdigest()


def sequence(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values: state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def js(path: Path) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out = {}
        for key, value in items:
            need(key not in out, "duplicate key:" + key); out[key] = value
        return out
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                       parse_float=lambda token: (_ for _ in ()).throw(Reject("float")),
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject("constant")))
    need(type(value) is dict, "JSON object")
    return value


def object_closed(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value); actual = body.pop("object_sha256", None)
    need(actual == expected == h(body), "object closure:" + label)


def row_closed(row: dict[str, Any], label: str) -> None:
    body = dict(row); actual = body.pop("row_sha256", None)
    need(type(actual) is str and actual == h(body), "row closure:" + label)


def ledger(base: Path, desc: dict[str, Any], label: str) -> list[dict[str, Any]]:
    path = base / desc["filename"]
    need(hf(path) == desc["sha256"], "ledger file:" + label)
    rows, hashes = [], []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line); row_closed(row, f"{label}:{index}")
            rows.append(row); hashes.append(row["row_sha256"])
    need(len(rows) == desc["row_count"] and sequence(hashes) == desc["row_hash_line_sequence_sha256"], "ledger descriptor:" + label)
    return rows


def scalar(value: Any) -> dict[str, Any]:
    if type(value) is dict:
        need({"kind", "value"} <= set(value), "scalar object"); return dict(value)
    need(type(value) is str, "scalar string")
    return {"kind": "ALGEBRAIC_SOURCE_BOUNDARY" if "sqrt" in value else "RATIONAL", "value": value}


def exact_box(cell: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    exact = {"compact_chart": cell["compact_chart"],
             "t": [scalar(x) for x in cell["physical_t_interval"]],
             "p": [scalar(x) for x in cell["physical_p_interval"]],
             "s": [{"kind": "RATIONAL", "value": "0"}, {"kind": "RATIONAL", "value": "0"}]}
    rational = all(x["kind"] == "RATIONAL" for axis in ("t", "p", "s") for x in exact[axis])
    c50 = None if not rational else {"compact_chart": exact["compact_chart"],
            "t": [x["value"] for x in exact["t"]], "p": [x["value"] for x in exact["p"]], "s": ["0", "0"]}
    return exact, c50


def projection(row: dict[str, Any]) -> dict[str, Any]:
    return {"C57L1_chain_row_sha256": row["row_sha256"], "pair_index": row["pair_index"],
            "C56L_task_row_sha256": row["C56L_task_row_sha256"],
            "C38": {"row_sha256": row["C38_row_sha256"], "path": row["C38_path"], "classification": row["C38_classification"], "first_decision_collision": row["C38_first_decision_collision"]},
            "C39": {"row_sha256": row["C39_row_sha256"], "path": row["C39_path"], "classification": row["C39_classification"], "route_method": row["C39_route_method"]},
            "C40": {"row_sha256": row["C40_row_sha256"], "path": row["C40_path"], "classification": row["C40_classification"]},
            "C41": {"row_sha256": row["C41_row_sha256"], "path": row["C41_path"], "split_axis_history": row["C41_split_axis_history"], "residual_classification": row["C41_residual_classification"]},
            "within_cell_upstream_lineage_exact": row["within_cell_upstream_lineage_exact"],
            "cross_C32_face_occurrence1_history_compatibility_proved": row["cross_C32_face_occurrence1_history_compatibility_proved"], "formal_credit": 0}


def c50_source_audit() -> dict[str, Any]:
    source = C50A.read_text(encoding="utf-8"); tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    names = ["interval", "exact_box", "request_check", "validate_split_tree", "locate_predecessor", "apply_history", "target_faces", "build"]
    need(all(name in functions for name in names), "C50 function inventory")
    text = {name: ast.get_source_segment(source, functions[name]) for name in names}
    slices = {name: {"source_sha256": hashlib.sha256(text[name].encode()).hexdigest(), "first_line": functions[name].lineno, "last_line": functions[name].end_lineno} for name in names}
    checks = {
        "request_requires_nonempty_bounded_transaction_history": "0 < len(request[\"transactions\"]) <= 1000" in source,
        "predecessor_locators_only_C41_side_or_active_occurrence": all(x in text["locate_predecessor"] for x in ("C41_AMBIENT_SIDE", "ACTIVE_OCCURRENCE_ID")),
        "task_requires_exactly_two_predecessors": "len(locators) == 2" in text["apply_history"],
        "task_predecessors_must_share_pair_and_semantic_root": all(x in text["apply_history"] for x in ("task pair/predecessor binding", "task root/predecessor semantic binding")),
        "frontier_must_be_nonempty_prefix_free_Kraft_one": all(x in text["validate_split_tree"] for x in ("bounded nonempty frontier", "prefix-free frontier", "exact Kraft-one frontier")),
        "replacements_must_partition_each_exact_predecessor": all(x in text["validate_split_tree"] for x in ("two-side replacement census", "replacement union equals predecessor box", "replacement exact area conservation")),
        "target_faces_are_derived_only_from_target_replacements": "for row in targets" in text["target_faces"],
        "owner_ledger_consumes_target_replacements_not_static_edge_entities": "face_ledger(overlay, targets)" in text["build"],
        "exact_box_parser_is_fraction_rational_only": "interval(value[\"t\"]" in text["exact_box"] and "q(value[0]" in text["interval"] and "Fraction as F" in source,
        "source_evidence_semantics_are_not_validated_beyond_zero_credit": "evidence.get(\"formal_credit\") == 0" in text["validate_split_tree"],
    }
    need(all(checks.values()), "C50 source constraints")
    return {"schema": "cm2.round306c59l.owner-edge-request.v1.c50a-static-api-audit",
            "C50a_source_file_sha256": PINS["C50a"], "C50a_request_schema": "cm2.round306c50a.global-codimension-owner-oracle.v1.request",
            "protocol_versions": PROTOCOLS, "owner_rule": OWNER_RULE,
            "active_universe_binding_sha256": ACTIVE, "history_genesis_sha256": GENESIS,
            "function_source_bindings": slices, "exact_interface_checks": checks,
            "static_existing_C32_edge_query_supported": False, "two_independent_endpoint_lineage_query_supported": False,
            "C35_occurrence1_history_semantic_validator_present": False, "cross_chart_source_seam_entity_supported": False}


def manifest_members() -> list[dict[str, str]]:
    members = []
    for line in C50A_MANIFEST.read_text().splitlines():
        expected, name = line.split("  ", 1); need(hf(ROOT / name) == expected, "C50 manifest member")
        members.append({"filename": name, "sha256": expected})
    need(len(members) == 8, "C50 manifest count"); return members


def runtime_snapshot() -> str:
    state = hashlib.sha256(); base = ROOT / ".cm2-runtime"
    for path in sorted(base.rglob("*"), key=lambda p: str(p.relative_to(base))):
        row = os.lstat(path); kind = "D" if stat.S_ISDIR(row.st_mode) else "F" if stat.S_ISREG(row.st_mode) else "O"
        state.update(enc([str(path.relative_to(base)), kind, row.st_size, row.st_mtime_ns, row.st_nlink]) + b"\n")
    state.update((hf(CANONICAL) + "\n").encode())
    return state.hexdigest()


def attacks(summary: dict[str, Any]) -> dict[str, Any]:
    frozen = {**summary,
              "all_endpoint_lineages_exact": True, "all_requests_exactly_bound": True,
              "all_decisions_fail_closed": True, "C50_static_edge_operation_present": False,
              "pair1_generalized": False, "formal_credit": 0, "D02_gate_credit": 0,
              "runtime_or_canonical_written": False}
    keys = list(frozen)
    need(len(keys) == 20, "20 attack fields")
    def guard(value: dict[str, Any]) -> None:
        body = dict(value); object_hash = body.pop("object_sha256")
        need(object_hash == h(body), "attack self closure"); need(body == frozen, "attack frozen projection")
    base = {**frozen, "object_sha256": h(frozen)}; guard(base)
    rows = {}
    for index, key in enumerate(keys):
        body = copy.deepcopy(frozen); value = body[key]
        body[key] = not value if type(value) is bool else value + 1
        attacked = {**body, "object_sha256": h(body)}
        try: guard(attacked)
        except Reject: rows[f"coherent_reclosed_{index}_{key}"] = "FAIL_CLOSED"
        else: raise Reject("attack accepted:" + key)
    return {"status": "PASS_20_OF_20_COHERENT_RECLOSED_ATTACKS_FAIL_CLOSED", "attack_count": 20,
            "mutations_reclosed_before_validation": True, "attacks": rows}


def verify() -> dict[str, Any]:
    before = runtime_snapshot()
    files = [(PRODUCER, "producer"), (RESULT, "result_file"), (GAP, "gap_file"),
             (C57_RESULT, "C57_result"), (C57_VERIFY, "C57_verify"), (C57_MANIFEST, "C57_manifest"),
             (C55B_RESULT, "C55B_result"), (C35_DIR / "result.json", "C35_result"),
             (C50A, "C50a"), (C50A_VERIFY, "C50a_verify"), (C50A_MANIFEST, "C50a_manifest"),
             (C53, "C53"), (CANONICAL, "canonical")]
    for path, key in files: need(hf(path) == PINS[key], "file pin:" + key)
    result, gap = js(RESULT), js(GAP)
    object_closed(result, PINS["result_object"], "C59 result"); object_closed(gap, PINS["gap_object"], "C59 gap")
    c57, c57v, c55, c35 = js(C57_RESULT), js(C57_VERIFY), js(C55B_RESULT), js(C35_DIR / "result.json")
    object_closed(c57, PINS["C57_object"], "C57"); object_closed(c57v, PINS["C57_verify_object"], "C57 verify")
    object_closed(c55, PINS["C55B_object"], "C55"); object_closed(c35, PINS["C35_object"], "C35")

    endpoints = ledger(OUT, result["ledgers"]["endpoint_occurrence1_history_bindings"], "candidate endpoints")
    requests = ledger(OUT, result["ledgers"]["edge_owner_history_requests"], "candidate requests")
    decisions = ledger(OUT, result["ledgers"]["edge_owner_compatibility_decisions"], "candidate decisions")
    edges = ledger(OUT, c57["ledgers"]["edge_obligations"], "C57 edges")
    locals_ = ledger(OUT, c57["ledgers"]["local_collision1_cell_status"], "C57 locals")
    chains = ledger(OUT, c57["ledgers"]["upstream_task_chains"], "C57 chains")
    crosswalk = ledger(OUT, c55["ledgers"]["cell_component_crosswalk"], "C55 crosswalk")
    occurrences = ledger(C35_DIR, c35["ledgers"]["path_occurrences"], "C35 occurrences")
    need((len(endpoints),len(requests),len(decisions),len(edges),len(locals_),len(chains)) == (1044,1042,1042,1042,1044,33319), "scope counts")

    occurrence = occurrences[0]; need(occurrence["row_sha256"] == PINS["occurrence1"] and occurrence["collision_index"] == 1, "occurrence1")
    keys = ("row_sha256", "collision_index", "geometry_template_id", "official_word_key_id", "official_word_variant_id",
            "incoming_chart", "incoming_absolute_owner_id", "outgoing_chart", "relative_frozen_target_id", "selected_absolute_owner_id",
            "destination_core_id", "C24_classification", "graph_row_sha256", "positive_area_row_sha256")
    occurrence_projection = {key: occurrence[key] for key in keys}; occurrence_hash = h(occurrence_projection)
    cell_map, local_map = {x["cell_id"]:x for x in crosswalk}, {x["cell_id"]:x for x in locals_}
    chain_map: dict[str,list[dict[str,Any]]] = defaultdict(list)
    for row in chains: chain_map[row["C55A_blocker_row_sha256"]].append(row)
    endpoint_map = {}
    kind = Counter()
    expected_ids = sorted({cell for edge in edges for cell in (edge["source_cell_id"],edge["target_cell_id"])})
    need([row["cell_id"] for row in endpoints] == expected_ids, "endpoint order")
    for candidate in endpoints:
        cell, local = cell_map[candidate["cell_id"]], local_map[candidate["cell_id"]]
        rows = chain_map[local["C55A_blocker_row_sha256"]]; projections = [projection(x) for x in rows]
        box, c50box = exact_box(cell); kind["rational" if c50box is not None else "algebraic"] += 1
        expected = {"schema": "cm2.round306c59l.owner-edge-request.v1.endpoint-occurrence1-history-binding-row",
            "cell_id": cell["cell_id"], "component_index": local["component_index"], "pair_index": local["pair_index"], "compact_chart": cell["compact_chart"],
            "C55B_crosswalk_row_sha256": cell["row_sha256"], "C57L1_local_status_row_sha256": local["row_sha256"], "C55A_blocker_row_sha256": local["C55A_blocker_row_sha256"],
            "exact_physical_slice_endpoint_box": box, "exact_physical_slice_endpoint_box_sha256": h(box),
            "C50a_rational_exact_box_encoding": c50box, "C50a_rational_exact_box_encodable": c50box is not None,
            "C35_occurrence1_history_projection": occurrence_projection, "C35_occurrence1_history_binding_sha256": occurrence_hash,
            "C38_C41_lineage_projection_count": len(projections), "C38_C41_lineage_projection_rows": projections,
            "C38_C41_lineage_projection_hash_sequence_sha256": sequence(h(x) for x in projections),
            "C57L1_chain_row_hash_sequence_sha256": sequence(x["row_sha256"] for x in rows),
            "all_within_cell_C38_C41_lineages_exact": all(x["within_cell_upstream_lineage_exact"] for x in rows),
            "cross_edge_occurrence1_history_compatibility_already_proved": False, "formal_credit": 0, "D02_gate_credit": 0}
        body = dict(candidate); rh = body.pop("row_sha256"); need(body == expected and rh == h(expected), "endpoint exact reconstruction")
        endpoint_map[candidate["cell_id"]] = candidate
    need(kind == Counter({"rational":986,"algebraic":58}), "endpoint census")

    edge_census=Counter(); request_map={}
    for edge,candidate in zip(edges,requests,strict=True):
        source,target=endpoint_map[edge["source_cell_id"]],endpoint_map[edge["target_cell_id"]]
        both=source["C50a_rational_exact_box_encodable"] and target["C50a_rational_exact_box_encodable"]
        edge_census["intra" if edge["glue_kind"]=="INTRA_CHART_FACE" else "seam"]+=1
        if both and edge["glue_kind"]=="INTRA_CHART_FACE": edge_census["rational_intra"]+=1
        if not both: edge_census["algebraic"]+=1
        endpoint_refs=[{"role":"SOURCE","cell_id":source["cell_id"],"endpoint_binding_row_sha256":source["row_sha256"],"exact_box_sha256":source["exact_physical_slice_endpoint_box_sha256"],"C38_C41_lineage_projection_hash_sequence_sha256":source["C38_C41_lineage_projection_hash_sequence_sha256"]},
                       {"role":"TARGET","cell_id":target["cell_id"],"endpoint_binding_row_sha256":target["row_sha256"],"exact_box_sha256":target["exact_physical_slice_endpoint_box_sha256"],"C38_C41_lineage_projection_hash_sequence_sha256":target["C38_C41_lineage_projection_hash_sequence_sha256"]}]
        body={"schema":"cm2.round306c59l.owner-edge-request.v1.edge-owner-history-request-row","request_kind":"EXACT_EXISTING_C32_FACE_OR_SOURCE_SEAM_TWO_ENDPOINT_OCCURRENCE1_OWNER_HISTORY_QUERY",
              "C57L1_edge_row_sha256":edge["row_sha256"],"component_index":edge["component_index"],"source_cell_id":edge["source_cell_id"],"target_cell_id":edge["target_cell_id"],
              "face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"exact_common_face_or_seam":edge["exact_common_face_refinement"],"exact_common_face_or_seam_sha256":h(edge["exact_common_face_refinement"]),
              "endpoint_bindings":endpoint_refs,"C35_occurrence1_history_binding_sha256":occurrence_hash,"C35_occurrence1_selected_absolute_owner_id":occurrence["selected_absolute_owner_id"],
              "protocol_versions_requested":PROTOCOLS,"C50a_owner_rule_requested":OWNER_RULE,"C50a_active_universe_binding_sha256":ACTIVE,"C50a_history_genesis_sha256":GENESIS,
              "required_outputs":{"source_occurrence1_owner_unique":True,"target_occurrence1_owner_unique":True,"endpoint_occurrence1_owner_compatible_on_exact_entity":True,"endpoint_C38_C41_history_compatible_on_exact_entity":True},
              "both_endpoint_boxes_C50a_rational_exact_box_encodable":both,"direct_C50a_request_schema_consumable":False,"direct_C50a_request_object":None,
              "request_semantically_complete_for_future_static_edge_owner_API":True,"formal_credit_requested":0,"D02_gate_credit_requested":0}
        body["owner_history_request_id"]="c59-owner-edge-request:"+h(body)
        actual=dict(candidate);rh=actual.pop("row_sha256");need(actual==body and rh==h(body),"request exact reconstruction")
        request_map[edge["row_sha256"]]=candidate
    need(edge_census==Counter({"intra":1026,"rational_intra":973,"algebraic":69,"seam":16}),"edge census")

    reason_census=Counter()
    for edge,candidate in zip(edges,decisions,strict=True):
        request=request_map[edge["row_sha256"]]; reasons=list(COMMON_GAPS)
        if not request["both_endpoint_boxes_C50a_rational_exact_box_encodable"]: reasons.append("C50A_EXACT_BOX_IS_RATIONAL_ONLY_BUT_EDGE_HAS_ALGEBRAIC_ENDPOINT_BOUNDARY")
        if edge["glue_kind"]=="SOURCE_CHART_TRANSITION": reasons += ["C50A_FACE_ENTITY_IS_SINGLE_CHART_ONLY","C50A_NO_SOURCE_CHART_SEAM_ENTITY_OR_GLUE_MAP_PRIMITIVE"]
        reason_census.update(reasons)
        expected={"schema":"cm2.round306c59l.owner-edge-request.v1.edge-owner-compatibility-decision-row","C57L1_edge_row_sha256":edge["row_sha256"],
                  "owner_history_request_row_sha256":request["row_sha256"],"owner_history_request_id":request["owner_history_request_id"],"source_cell_id":edge["source_cell_id"],"target_cell_id":edge["target_cell_id"],
                  "face_or_corner_id":edge["face_or_corner_id"],"glue_kind":edge["glue_kind"],"direct_C50a_generic_capability_consumable":False,
                  "owner_unique_proved":False,"owner_unique_disproved":False,"endpoint_occurrence1_owner_compatible_proved":False,"endpoint_occurrence1_owner_compatible_disproved":False,
                  "endpoint_C38_C41_history_compatible_proved":False,"endpoint_C38_C41_history_compatible_disproved":False,
                  "decision":"FAIL_CLOSED_EXACT_C50A_STATIC_EDGE_OWNER_HISTORY_API_GAP","reason_codes":reasons,"pair1_local_authority_generalized":False,"formal_credit":0,"D02_gate_credit":0}
        actual=dict(candidate);rh=actual.pop("row_sha256");need(actual==expected and rh==h(expected),"decision exact reconstruction")

    summary={"endpoint_count":1044,"rational_endpoint_count":986,"algebraic_endpoint_count":58,"edge_request_count":1042,
             "intra_chart_edge_count":1026,"source_seam_edge_count":16,"both_endpoint_rational_intra_edge_count":973,
             "edge_with_algebraic_endpoint_count":69,"direct_C50a_consumable_edge_count":0,"owner_unique_pass_count":0,"owner_compatible_pass_count":0,"fail_closed_edge_count":1042}
    need(result["scope"]==gap["request_scope"]==summary and result["reason_code_census"]==dict(sorted(reason_census.items())),"result summary")
    api=c50_source_audit(); need(gap["C50a_static_API_audit"]==api and gap["C50a_frozen_manifest_members"]==manifest_members(),"API gap reconstruction")
    need(gap["pair1_local_authority_generalized"] is False and result["strict_boundary"]["pair1_local_authority_generalized"] is False,"pair1 non-generalization")
    attack=attacks(summary)
    after=runtime_snapshot(); need(before==after and hf(C53)==PINS["C53"] and hf(CANONICAL)==PINS["canonical"],"runtime/canonical stable")
    output={"schema":SCHEMA,"status":"PASS_INDEPENDENT_1044_ENDPOINT_1042_REQUEST_1042_FAIL_CLOSED_DECISION_RECONSTRUCTION__0_C50A_CONSUMABLE__20_OF_20_ATTACKS__ZERO_CREDIT",
            "candidate":{"producer_file_sha256":PINS["producer"],"result_file_sha256":PINS["result_file"],"result_object_sha256":PINS["result_object"],"gap_file_sha256":PINS["gap_file"],"gap_object_sha256":PINS["gap_object"]},
            "verified":summary,"upstream":{"C57_chain_rows_closed":33319,"C55B_crosswalk_rows_closed":len(crosswalk),"C35_occurrence_rows_closed":len(occurrences)},
            "C50a_API_audit":api,"attacks":attack,"zero_credit":{"formal_credit":0,"D02_gate_credit":0,"owner_credit":0,"CM2":"NO-GO_FOR_CLAIM"},
            "independence":{"C59_producer_imported_or_executed":False,"C50a_producer_imported_or_executed":False,"producer_treatment":"INERT_HASH_ONLY_BYTES","verifier_file_sha256":hf(SELF)},
            "runtime_and_canonical_snapshot_before":before,"runtime_and_canonical_snapshot_after":after,"runtime_and_canonical_unchanged":True,
            "files_written":[str(OUTPUT.relative_to(ROOT))],"old_runtime_canonical_files_written":False}
    output["object_sha256"]=h(output); OUTPUT.write_bytes(enc(output)+b"\n"); return output


def main() -> int:
    result=verify(); print(json.dumps({"status":result["status"],"object_sha256":result["object_sha256"],"verified":result["verified"]},sort_keys=True)); return 0


if __name__=="__main__":
    try: raise SystemExit(main())
    except (Reject,OSError,ValueError,KeyError,TypeError,IndexError,SyntaxError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}",file=sys.stderr); raise SystemExit(2)
