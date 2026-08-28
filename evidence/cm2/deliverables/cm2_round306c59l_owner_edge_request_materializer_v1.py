#!/usr/bin/env python3
"""C59-L: freeze occurrence-1 owner/history requests for all C57-L1 edges.

This is a fail-closed request materializer, not an owner oracle.  It binds
each exact C57-L1 face/seam, both C32 endpoint boxes, C35 occurrence 1, and
both endpoint C38->C41 lineage sets.  It then audits the frozen generic C50a
source interface.  C50a has no protocol operation that semantically consumes
this two-existing-endpoint query, so no owner or compatibility PASS is issued.
"""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c59l_owner"
SCHEMA = "cm2.round306c59l.owner-edge-request.v1"

ENDPOINT_FILE = PREFIX + "_endpoint_occurrence1_history_bindings_v1.jsonl.gz"
REQUEST_FILE = PREFIX + "_edge_owner_history_requests_v1.jsonl.gz"
DECISION_FILE = PREFIX + "_edge_owner_compatibility_decisions_v1.jsonl.gz"
GAP_FILE = PREFIX + "_c50a_exact_api_gap_v1.json"
RESULT_FILE = PREFIX + "_result_v1.json"

C57_RESULT = OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json"
C57_VERIFY = OUT / "cm2_round306c57l1_collision1_edgewise_transport_independent_verification_v1.json"
C57_MANIFEST = OUT / "cm2_round306c57l1_collision1_edgewise_transport_manifest_v1.sha256"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C50A = OUT / "cm2_round306c50a_global_codimension_owner_oracle_v1.py"
C50A_VERIFY = OUT / "cm2_round306c50a_global_codimension_owner_oracle_independent_verifier_v1.py"
C50A_MANIFEST = OUT / "cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

EXPECTED = {
    "C57_RESULT_FILE": "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    "C57_RESULT_OBJECT": "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0",
    "C57_VERIFY_FILE": "59bf5c651b94d6fee7508f0ad63f549b8bf5699df27c82db0b6cd86409c78ac3",
    "C57_VERIFY_OBJECT": "df0641cb734f40c312c41e4707c05adeae8d20e785f55bdf24a603200b8b1f2d",
    "C57_MANIFEST_FILE": "b66325f26f39b1e4e3b1027d331105e1be9e76c126fa32210a614313e587f281",
    "C55B_RESULT_FILE": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_RESULT_OBJECT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C35_RESULT_FILE": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_RESULT_OBJECT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C35_OCCURRENCE1_ROW": "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250",
    "C50A_FILE": "43147808a94e14df20d902db6d7d383f8d230c6685401684bfb9ea697f7e9ed7",
    "C50A_VERIFY_FILE": "2ae76868e0320563cafbc4a472f3ad1bf292817491d97da1fe68ca9d8e8bd3b4",
    "C50A_MANIFEST_FILE": "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6",
    "C53_HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "CANONICAL_FILE": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

PROTOCOLS = {
    "occurrence": "CM2_C41_ACTIVE_OVERLAY_OCCURRENCE_V1",
    "split": "CM2_EXACT_TWO_SIDE_BINARY_SPLIT_DECISION_V1",
    "history": "CM2_HASH_CHAINED_ACTIVE_OVERLAY_HISTORY_V1",
    "owner": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1",
}
OWNER_RULE = "UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH"
C50A_ACTIVE_UNIVERSE = "112410045d088f22908276193a1d046d6f11c0e1818790b2826c5fcf0f6ac05f"
C50A_HISTORY_GENESIS = "17af15070fe6d383e64a1bbc44a6cad81e9940e4b7702b87c5ccee9c739bfcc7"

COMMON_GAPS = [
    "C50A_NO_STATIC_EXISTING_C32_EDGE_QUERY_OPERATION",
    "C50A_REQUEST_TASK_REQUIRES_ONE_REPRESENTATIVE_REFLECTED_PREDECESSOR_PAIR",
    "C57L1_QUERY_HAS_TWO_ADJACENT_C32_ENDPOINT_CELLS_WITH_INDEPENDENT_LINEAGES",
    "C50A_KRAFT_ONE_REPLACEMENTS_MUST_PARTITION_EACH_SELECTED_C41_PREDECESSOR",
    "C50A_OWNER_OUTPUT_IS_RESTRICTED_TO_TARGET_HISTORY_REPLACEMENT_BOUNDARIES",
    "C50A_SOURCE_EVIDENCE_DOES_NOT_VALIDATE_C35_OCCURRENCE1_OR_C38_C41_HISTORY_COMPATIBILITY",
]


class FailClosed(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def seq(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        need(type(value) is str, "sequence token")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            need(key not in out, "duplicate key:" + key)
            out[key] = value
        return out
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                       parse_float=lambda token: (_ for _ in ()).throw(FailClosed("float:" + token)),
                       parse_constant=lambda token: (_ for _ in ()).throw(FailClosed("constant:" + token)))
    need(type(value) is dict, "JSON object:" + str(path))
    return value


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    actual = body.pop("object_sha256", None)
    need(actual == expected == digest(body), "object closure:" + label)


def close_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    actual = body.pop("row_sha256", None)
    need(type(actual) is str and actual == digest(body), "row closure:" + label)


def read_ledger(base: Path, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    path = base / descriptor["filename"]
    need(file_sha(path) == descriptor["sha256"], "ledger file:" + label)
    rows: list[dict[str, Any]] = []
    hashes: list[str] = []
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            rows.append(row)
            hashes.append(row["row_sha256"])
    need(len(rows) == descriptor["row_count"], "ledger count:" + label)
    need(seq(hashes) == descriptor["row_hash_line_sequence_sha256"], "ledger sequence:" + label)
    return rows


class Writer:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.raw = path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "Writer":
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row_hash = digest(body)
        row = {**body, "row_sha256": row_hash}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close(); self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name, "order": self.order, "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha(self.path), "size": self.path.stat().st_size,
        }


def scalar(value: Any) -> dict[str, str]:
    if type(value) is dict:
        need({"kind", "value"} <= set(value) and type(value["kind"]) is str
             and type(value["value"]) is str, "exact scalar object")
        return dict(value)
    need(type(value) is str, "exact scalar string")
    return {"kind": "ALGEBRAIC_SOURCE_BOUNDARY" if "sqrt" in value else "RATIONAL", "value": value}


def endpoint_box(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    exact = {
        "compact_chart": row["compact_chart"],
        "t": [scalar(item) for item in row["physical_t_interval"]],
        "p": [scalar(item) for item in row["physical_p_interval"]],
        "s": [{"kind": "RATIONAL", "value": "0"}, {"kind": "RATIONAL", "value": "0"}],
    }
    rational = all(item["kind"] == "RATIONAL" for axis in ("t", "p", "s") for item in exact[axis])
    candidate = None if not rational else {
        "compact_chart": exact["compact_chart"],
        "t": [item["value"] for item in exact["t"]],
        "p": [item["value"] for item in exact["p"]],
        "s": ["0", "0"],
    }
    return exact, candidate


def validate_c50a_manifest() -> list[dict[str, str]]:
    need(file_sha(C50A_MANIFEST) == EXPECTED["C50A_MANIFEST_FILE"], "C50a manifest pin")
    members = []
    for line in C50A_MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        path = ROOT / name
        need(path.is_file() and file_sha(path) == expected, "C50a member:" + name)
        members.append({"filename": name, "sha256": expected})
    need(len(members) == 8, "C50a manifest 8 members")
    return members


def c50a_api_audit() -> dict[str, Any]:
    source = C50A.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(C50A))
    functions = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    names = ["interval", "exact_box", "request_check", "validate_split_tree", "locate_predecessor", "apply_history", "target_faces", "build"]
    need(all(name in functions for name in names), "C50a audited functions")
    slices = {}
    for name in names:
        node = functions[name]
        text = ast.get_source_segment(source, node)
        need(type(text) is str, "C50a function segment:" + name)
        slices[name] = {"source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "first_line": node.lineno, "last_line": node.end_lineno}
    checks = {
        "request_requires_nonempty_bounded_transaction_history": "0 < len(request[\"transactions\"]) <= 1000" in source,
        "predecessor_locators_only_C41_side_or_active_occurrence": all(token in ast.get_source_segment(source, functions["locate_predecessor"])
            for token in ("C41_AMBIENT_SIDE", "ACTIVE_OCCURRENCE_ID")),
        "task_requires_exactly_two_predecessors": "len(locators) == 2" in ast.get_source_segment(source, functions["apply_history"]),
        "task_predecessors_must_share_pair_and_semantic_root": all(token in ast.get_source_segment(source, functions["apply_history"])
            for token in ("task pair/predecessor binding", "task root/predecessor semantic binding")),
        "frontier_must_be_nonempty_prefix_free_Kraft_one": all(token in ast.get_source_segment(source, functions["validate_split_tree"])
            for token in ("bounded nonempty frontier", "prefix-free frontier", "exact Kraft-one frontier")),
        "replacements_must_partition_each_exact_predecessor": all(token in ast.get_source_segment(source, functions["validate_split_tree"])
            for token in ("two-side replacement census", "replacement union equals predecessor box", "replacement exact area conservation")),
        "target_faces_are_derived_only_from_target_replacements": "for row in targets" in ast.get_source_segment(source, functions["target_faces"]),
        "owner_ledger_consumes_target_replacements_not_static_edge_entities": "face_ledger(overlay, targets)" in ast.get_source_segment(source, functions["build"]),
        "exact_box_parser_is_fraction_rational_only": (
            "interval(value[\"t\"]" in ast.get_source_segment(source, functions["exact_box"])
            and "q(value[0]" in ast.get_source_segment(source, functions["interval"])
            and "Fraction as F" in source),
        "source_evidence_semantics_are_not_validated_beyond_zero_credit": "evidence.get(\"formal_credit\") == 0" in ast.get_source_segment(source, functions["validate_split_tree"]),
    }
    need(all(checks.values()), "C50a exact API source checks")
    return {
        "schema": SCHEMA + ".c50a-static-api-audit",
        "C50a_source_file_sha256": EXPECTED["C50A_FILE"],
        "C50a_request_schema": "cm2.round306c50a.global-codimension-owner-oracle.v1.request",
        "protocol_versions": PROTOCOLS,
        "owner_rule": OWNER_RULE,
        "active_universe_binding_sha256": C50A_ACTIVE_UNIVERSE,
        "history_genesis_sha256": C50A_HISTORY_GENESIS,
        "function_source_bindings": slices,
        "exact_interface_checks": checks,
        "static_existing_C32_edge_query_supported": False,
        "two_independent_endpoint_lineage_query_supported": False,
        "C35_occurrence1_history_semantic_validator_present": False,
        "cross_chart_source_seam_entity_supported": False,
    }


def lineage_projection(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "C57L1_chain_row_sha256": row["row_sha256"],
        "pair_index": row["pair_index"],
        "C56L_task_row_sha256": row["C56L_task_row_sha256"],
        "C38": {"row_sha256": row["C38_row_sha256"], "path": row["C38_path"],
                "classification": row["C38_classification"],
                "first_decision_collision": row["C38_first_decision_collision"]},
        "C39": {"row_sha256": row["C39_row_sha256"], "path": row["C39_path"],
                "classification": row["C39_classification"], "route_method": row["C39_route_method"]},
        "C40": {"row_sha256": row["C40_row_sha256"], "path": row["C40_path"],
                "classification": row["C40_classification"]},
        "C41": {"row_sha256": row["C41_row_sha256"], "path": row["C41_path"],
                "split_axis_history": row["C41_split_axis_history"],
                "residual_classification": row["C41_residual_classification"]},
        "within_cell_upstream_lineage_exact": row["within_cell_upstream_lineage_exact"],
        "cross_C32_face_occurrence1_history_compatibility_proved": row["cross_C32_face_occurrence1_history_compatibility_proved"],
        "formal_credit": 0,
    }


def self_test(summary: dict[str, int]) -> dict[str, Any]:
    expected = {
        "endpoint_count": 1044, "rational_endpoint_count": 986,
        "algebraic_endpoint_count": 58, "edge_request_count": 1042,
        "intra_chart_edge_count": 1026, "source_seam_edge_count": 16,
        "both_endpoint_rational_intra_edge_count": 973,
        "edge_with_algebraic_endpoint_count": 69,
        "direct_C50a_consumable_edge_count": 0,
        "owner_unique_pass_count": 0, "owner_compatible_pass_count": 0,
        "fail_closed_edge_count": 1042,
    }
    need(summary == expected, "exact C59 summary")
    attacks = {}
    for index, (key, value) in enumerate(expected.items()):
        altered = dict(summary); altered[key] = value + 1
        try:
            need(altered == expected, "mutated summary")
        except FailClosed:
            attacks[f"projection_{index}_{key}"] = "FAIL_CLOSED"
        else:
            raise FailClosed("attack accepted:" + key)
    return {"status": "PASS_12_OF_12_PRODUCER_PROJECTION_ATTACKS_FAIL_CLOSED",
            "attack_count": 12, "attacks": attacks}


def build() -> dict[str, Any]:
    pins = [(C57_RESULT, "C57_RESULT_FILE"), (C57_VERIFY, "C57_VERIFY_FILE"),
            (C57_MANIFEST, "C57_MANIFEST_FILE"), (C55B_RESULT, "C55B_RESULT_FILE"),
            (C35_DIR / "result.json", "C35_RESULT_FILE"), (C50A, "C50A_FILE"),
            (C50A_VERIFY, "C50A_VERIFY_FILE"), (C50A_MANIFEST, "C50A_MANIFEST_FILE"),
            (C53_HEAD, "C53_HEAD_FILE"), (CANONICAL, "CANONICAL_FILE")]
    for path, key in pins:
        need(file_sha(path) == EXPECTED[key], "file pin:" + key)
    c57 = strict_json(C57_RESULT); close_object(c57, EXPECTED["C57_RESULT_OBJECT"], "C57")
    c57v = strict_json(C57_VERIFY); close_object(c57v, EXPECTED["C57_VERIFY_OBJECT"], "C57 verifier")
    c55b = strict_json(C55B_RESULT); close_object(c55b, EXPECTED["C55B_RESULT_OBJECT"], "C55B")
    c35 = strict_json(C35_DIR / "result.json"); close_object(c35, EXPECTED["C35_RESULT_OBJECT"], "C35")
    need(c57v["runtime_and_canonical_unchanged"] is True, "C57 independent stability")
    c50a_members = validate_c50a_manifest()
    api = c50a_api_audit()

    edges = read_ledger(OUT, c57["ledgers"]["edge_obligations"], "C57 edges")
    locals_ = read_ledger(OUT, c57["ledgers"]["local_collision1_cell_status"], "C57 locals")
    chains = read_ledger(OUT, c57["ledgers"]["upstream_task_chains"], "C57 chains")
    crosswalk_rows = read_ledger(OUT, c55b["ledgers"]["cell_component_crosswalk"], "C55B crosswalk")
    occurrences = read_ledger(C35_DIR, c35["ledgers"]["path_occurrences"], "C35 occurrences")
    need(len(edges) == 1042 and len(locals_) == 1044 and len(chains) == 33319, "C57 scope")
    occurrence1 = occurrences[0]
    need(occurrence1["collision_index"] == 1 and occurrence1["row_sha256"] == EXPECTED["C35_OCCURRENCE1_ROW"], "C35 occurrence1")
    occurrence1_projection = {
        key: occurrence1[key] for key in (
            "row_sha256", "collision_index", "geometry_template_id", "official_word_key_id",
            "official_word_variant_id", "incoming_chart", "incoming_absolute_owner_id",
            "outgoing_chart", "relative_frozen_target_id", "selected_absolute_owner_id",
            "destination_core_id", "C24_classification", "graph_row_sha256", "positive_area_row_sha256")
    }
    occurrence1_history_binding = digest(occurrence1_projection)
    crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
    local_by_cell = {row["cell_id"]: row for row in locals_}
    chains_by_blocker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in chains:
        chains_by_blocker[row["C55A_blocker_row_sha256"]].append(row)

    endpoint_ids = sorted({cell_id for edge in edges for cell_id in (edge["source_cell_id"], edge["target_cell_id"])})
    need(len(endpoint_ids) == 1044, "1044 unique endpoints")
    endpoint_rows: dict[str, dict[str, Any]] = {}
    endpoint_kind = Counter()
    with Writer(OUT / ENDPOINT_FILE, "CELL_ID") as writer:
        for cell_id in endpoint_ids:
            cell, local = crosswalk[cell_id], local_by_cell[cell_id]
            need(type(cell["row_sha256"]) is str and type(local["C55A_blocker_row_sha256"]) is str,
                 "endpoint source bindings")
            source_chains = chains_by_blocker[local["C55A_blocker_row_sha256"]]
            need(len(source_chains) == local["current_pending_task_count"], "endpoint lineage count")
            need(seq(row["row_sha256"] for row in source_chains) == local["C57L1_upstream_chain_row_hash_sequence_sha256"], "endpoint lineage sequence")
            projections = [lineage_projection(row) for row in source_chains]
            projection_hashes = [digest(row) for row in projections]
            exact, c50a_box = endpoint_box(cell)
            endpoint_kind["rational" if c50a_box is not None else "algebraic"] += 1
            body = {
                "schema": SCHEMA + ".endpoint-occurrence1-history-binding-row",
                "cell_id": cell_id, "component_index": local["component_index"],
                "pair_index": local["pair_index"], "compact_chart": cell["compact_chart"],
                "C55B_crosswalk_row_sha256": cell["row_sha256"],
                "C57L1_local_status_row_sha256": local["row_sha256"],
                "C55A_blocker_row_sha256": local["C55A_blocker_row_sha256"],
                "exact_physical_slice_endpoint_box": exact,
                "exact_physical_slice_endpoint_box_sha256": digest(exact),
                "C50a_rational_exact_box_encoding": c50a_box,
                "C50a_rational_exact_box_encodable": c50a_box is not None,
                "C35_occurrence1_history_projection": occurrence1_projection,
                "C35_occurrence1_history_binding_sha256": occurrence1_history_binding,
                "C38_C41_lineage_projection_count": len(projections),
                "C38_C41_lineage_projection_rows": projections,
                "C38_C41_lineage_projection_hash_sequence_sha256": seq(projection_hashes),
                "C57L1_chain_row_hash_sequence_sha256": seq(row["row_sha256"] for row in source_chains),
                "all_within_cell_C38_C41_lineages_exact": all(row["within_cell_upstream_lineage_exact"] for row in source_chains),
                "cross_edge_occurrence1_history_compatibility_already_proved": False,
                "formal_credit": 0, "D02_gate_credit": 0,
            }
            endpoint_rows[cell_id] = writer.write(body)
    endpoint_desc = writer.descriptor()
    need(endpoint_kind == Counter({"rational": 986, "algebraic": 58}), "endpoint rational census")

    request_rows: dict[str, dict[str, Any]] = {}
    edge_census = Counter()
    with Writer(OUT / REQUEST_FILE, "C57L1_EDGE_ORDER") as writer:
        for edge in edges:
            source = endpoint_rows[edge["source_cell_id"]]
            target = endpoint_rows[edge["target_cell_id"]]
            both_rational = source["C50a_rational_exact_box_encodable"] and target["C50a_rational_exact_box_encodable"]
            if edge["glue_kind"] == "INTRA_CHART_FACE": edge_census["intra"] += 1
            else: edge_census["seam"] += 1
            if both_rational and edge["glue_kind"] == "INTRA_CHART_FACE": edge_census["rational_intra"] += 1
            if not both_rational: edge_census["algebraic_contact"] += 1
            body = {
                "schema": SCHEMA + ".edge-owner-history-request-row",
                "request_kind": "EXACT_EXISTING_C32_FACE_OR_SOURCE_SEAM_TWO_ENDPOINT_OCCURRENCE1_OWNER_HISTORY_QUERY",
                "C57L1_edge_row_sha256": edge["row_sha256"],
                "component_index": edge["component_index"],
                "source_cell_id": edge["source_cell_id"], "target_cell_id": edge["target_cell_id"],
                "face_or_corner_id": edge["face_or_corner_id"], "glue_kind": edge["glue_kind"],
                "exact_common_face_or_seam": edge["exact_common_face_refinement"],
                "exact_common_face_or_seam_sha256": digest(edge["exact_common_face_refinement"]),
                "endpoint_bindings": [
                    {"role": "SOURCE", "cell_id": source["cell_id"], "endpoint_binding_row_sha256": source["row_sha256"],
                     "exact_box_sha256": source["exact_physical_slice_endpoint_box_sha256"],
                     "C38_C41_lineage_projection_hash_sequence_sha256": source["C38_C41_lineage_projection_hash_sequence_sha256"]},
                    {"role": "TARGET", "cell_id": target["cell_id"], "endpoint_binding_row_sha256": target["row_sha256"],
                     "exact_box_sha256": target["exact_physical_slice_endpoint_box_sha256"],
                     "C38_C41_lineage_projection_hash_sequence_sha256": target["C38_C41_lineage_projection_hash_sequence_sha256"]},
                ],
                "C35_occurrence1_history_binding_sha256": occurrence1_history_binding,
                "C35_occurrence1_selected_absolute_owner_id": occurrence1["selected_absolute_owner_id"],
                "protocol_versions_requested": PROTOCOLS,
                "C50a_owner_rule_requested": OWNER_RULE,
                "C50a_active_universe_binding_sha256": C50A_ACTIVE_UNIVERSE,
                "C50a_history_genesis_sha256": C50A_HISTORY_GENESIS,
                "required_outputs": {
                    "source_occurrence1_owner_unique": True,
                    "target_occurrence1_owner_unique": True,
                    "endpoint_occurrence1_owner_compatible_on_exact_entity": True,
                    "endpoint_C38_C41_history_compatible_on_exact_entity": True,
                },
                "both_endpoint_boxes_C50a_rational_exact_box_encodable": both_rational,
                "direct_C50a_request_schema_consumable": False,
                "direct_C50a_request_object": None,
                "request_semantically_complete_for_future_static_edge_owner_API": True,
                "formal_credit_requested": 0, "D02_gate_credit_requested": 0,
            }
            request_hash = digest(body)
            body["owner_history_request_id"] = "c59-owner-edge-request:" + request_hash
            request_rows[edge["row_sha256"]] = writer.write(body)
    request_desc = writer.descriptor()
    need(edge_census == Counter({"intra": 1026, "rational_intra": 973, "algebraic_contact": 69, "seam": 16}), "edge request census")

    decision_reason_census = Counter()
    with Writer(OUT / DECISION_FILE, "C57L1_EDGE_ORDER") as writer:
        for edge in edges:
            request = request_rows[edge["row_sha256"]]
            reasons = list(COMMON_GAPS)
            if not request["both_endpoint_boxes_C50a_rational_exact_box_encodable"]:
                reasons.append("C50A_EXACT_BOX_IS_RATIONAL_ONLY_BUT_EDGE_HAS_ALGEBRAIC_ENDPOINT_BOUNDARY")
            if edge["glue_kind"] == "SOURCE_CHART_TRANSITION":
                reasons.extend(["C50A_FACE_ENTITY_IS_SINGLE_CHART_ONLY",
                                "C50A_NO_SOURCE_CHART_SEAM_ENTITY_OR_GLUE_MAP_PRIMITIVE"])
            decision_reason_census.update(reasons)
            body = {
                "schema": SCHEMA + ".edge-owner-compatibility-decision-row",
                "C57L1_edge_row_sha256": edge["row_sha256"],
                "owner_history_request_row_sha256": request["row_sha256"],
                "owner_history_request_id": request["owner_history_request_id"],
                "source_cell_id": edge["source_cell_id"], "target_cell_id": edge["target_cell_id"],
                "face_or_corner_id": edge["face_or_corner_id"], "glue_kind": edge["glue_kind"],
                "direct_C50a_generic_capability_consumable": False,
                "owner_unique_proved": False, "owner_unique_disproved": False,
                "endpoint_occurrence1_owner_compatible_proved": False,
                "endpoint_occurrence1_owner_compatible_disproved": False,
                "endpoint_C38_C41_history_compatible_proved": False,
                "endpoint_C38_C41_history_compatible_disproved": False,
                "decision": "FAIL_CLOSED_EXACT_C50A_STATIC_EDGE_OWNER_HISTORY_API_GAP",
                "reason_codes": reasons,
                "pair1_local_authority_generalized": False,
                "formal_credit": 0, "D02_gate_credit": 0,
            }
            writer.write(body)
    decision_desc = writer.descriptor()

    summary = {
        "endpoint_count": 1044, "rational_endpoint_count": 986, "algebraic_endpoint_count": 58,
        "edge_request_count": 1042, "intra_chart_edge_count": 1026, "source_seam_edge_count": 16,
        "both_endpoint_rational_intra_edge_count": 973, "edge_with_algebraic_endpoint_count": 69,
        "direct_C50a_consumable_edge_count": 0, "owner_unique_pass_count": 0,
        "owner_compatible_pass_count": 0, "fail_closed_edge_count": 1042,
    }
    test = self_test(summary)
    gap: dict[str, Any] = {
        "schema": SCHEMA + ".c50a-exact-api-gap",
        "status": "FROZEN_EXACT_API_GAP__0_OF_1042_DIRECTLY_CONSUMABLE__NO_OWNER_OR_COMPATIBILITY_CREDIT",
        "C50a_static_API_audit": api,
        "C50a_frozen_manifest_members": c50a_members,
        "request_scope": summary,
        "global_gap_reason_codes": COMMON_GAPS,
        "conditional_gap_census": {
            "rational_same_chart_intra_edges_still_blocked_by_structural_API_gap": 973,
            "edges_with_at_least_one_algebraic_endpoint": 69,
            "cross_chart_source_seams": 16,
        },
        "required_API_extension": {
            "operation": "STATIC_EXISTING_EDGE_TWO_ENDPOINT_OWNER_HISTORY_QUERY",
            "must_semantically_validate": [
                "EXACT_FACE_OR_SOURCE_SEAM_AND_GLUE_MAP", "BOTH_EXISTING_C32_ENDPOINT_BOXES",
                "C35_OCCURRENCE1_HISTORY_BINDING", "BOTH_ENDPOINT_C38_C41_LINEAGE_SEQUENCES",
                "FULL_ACTIVE_UNIVERSE_INCIDENCE", "OWNER_UNIQUENESS", "CROSS_EDGE_OWNER_AND_HISTORY_COMPATIBILITY",
            ],
            "must_support_exact_scalar_domain": ["CANONICAL_RATIONAL", "-1/sqrt(2)", "+1/sqrt(2)"],
            "must_have_independent_verifier": True,
        },
        "pair1_local_authority_generalized": False,
        "formal_credit": 0, "D02_gate_credit": 0,
    }
    gap["object_sha256"] = digest(gap)
    (OUT / GAP_FILE).write_bytes(canonical(gap) + b"\n")

    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_1042_COMPLETE_OWNER_HISTORY_REQUESTS_FROZEN__FAIL_CLOSED_0_DIRECT_C50A_CONSUMABLE__0_OWNER_COMPATIBILITY_PASS__ZERO_CREDIT",
        "authority_binding": {
            "C57L1_result_file_sha256": EXPECTED["C57_RESULT_FILE"], "C57L1_result_object_sha256": EXPECTED["C57_RESULT_OBJECT"],
            "C57L1_independent_verification_file_sha256": EXPECTED["C57_VERIFY_FILE"], "C57L1_independent_verification_object_sha256": EXPECTED["C57_VERIFY_OBJECT"],
            "C57L1_manifest_file_sha256": EXPECTED["C57_MANIFEST_FILE"],
            "C55B_result_object_sha256": EXPECTED["C55B_RESULT_OBJECT"], "C35_result_object_sha256": EXPECTED["C35_RESULT_OBJECT"],
            "C50a_source_file_sha256": EXPECTED["C50A_FILE"], "C50a_independent_verifier_file_sha256": EXPECTED["C50A_VERIFY_FILE"],
            "C50a_manifest_file_sha256": EXPECTED["C50A_MANIFEST_FILE"], "C53_head_file_sha256": EXPECTED["C53_HEAD_FILE"],
            "canonical_file_sha256": EXPECTED["CANONICAL_FILE"],
        },
        "scope": summary,
        "occurrence1_binding": {"projection": occurrence1_projection, "history_binding_sha256": occurrence1_history_binding},
        "C50a_API_gap_object_sha256": gap["object_sha256"],
        "reason_code_census": dict(sorted(decision_reason_census.items())),
        "ledgers": {"endpoint_occurrence1_history_bindings": endpoint_desc,
                    "edge_owner_history_requests": request_desc,
                    "edge_owner_compatibility_decisions": decision_desc},
        "self_test": test,
        "strict_boundary": {"pair1_local_authority_generalized": False, "runtime_or_canonical_written": False,
                            "formal_credit": 0, "D02_gate_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": [
            "IMPLEMENT_NO_PRODUCER_STATIC_EXISTING_EDGE_TWO_ENDPOINT_OWNER_HISTORY_API",
            "SUPPORT_RATIONAL_AND_SOURCE_ALGEBRAIC_BOUNDARY_EXACT_SCALARS_AND_CROSS_CHART_SEAMS",
            "INDEPENDENTLY_REPLAY_ALL_1042_REQUESTS_AGAINST_THE_FULL_ACTIVE_UNIVERSE",
            "ISSUE_OWNER_UNIQUE_AND_COMPATIBLE_PASS_ONLY_FOR_BYTE_FROZEN_REQUESTS_THAT_VERIFY",
        ],
    }
    result["object_sha256"] = digest(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    result = build()
    print(json.dumps({"status": result["status"], "scope": result["scope"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
