#!/usr/bin/env python3
"""C27-independent SINGLE_GRAPHS physical-totality probe (stream implementation).

The graph-root universe is classified from the pinned C10 graph geometry before
the C24 support kernels are opened.  Every C24A positive row and C24B exact-empty
row is then assigned to exactly one C10 terminal.  Only the SINGLE partition is
materialized as candidate proof rows.  No transition-family table or historical
edge ledger is used.  This gate is deliberately zero-credit until the complete
primitive twenty-terminal gate is independently closed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
SCHEMA = "cm2.c27.single-graphs-physical-totality-zero-credit.v1"

C10 = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz"
C24B = "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"

PINS = {
    C10: "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C24A: "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58",
    C24B: "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}

CLASS_TO_TERMINAL = {
    "R242_UNIQUE_GRAPH_FULL_PATCH": "OUTGOING_GRAPHS",
    "R235_TARGET_POSITIVE_PARTIAL_BASE": "SINGLE_GRAPHS",
    "R235_SOURCE_EXACT_FACE_FULL_BASE": "SINGLE_GRAPHS",
    "R235D_SOURCE_EXACT_FACE_FULL_BASE": "DOUBLE_GRAPHS",
}
EXPECTED_ROOT_PARTITION = {"DOUBLE_GRAPHS": 16, "OUTGOING_GRAPHS": 264, "SINGLE_GRAPHS": 4984}
EXPECTED_SINGLE_CLASSES = {
    "R235_TARGET_POSITIVE_PARTIAL_BASE": 4432,
    "R235_SOURCE_EXACT_FACE_FULL_BASE": 552,
}
EXPECTED_C24A_ALLOCATION = {
    "DOUBLE_GRAPHS": {"G2A": 16, "G2B": 16},
    "OUTGOING_GRAPHS": {"G2A": 264, "G2B": 528},
    "SINGLE_GRAPHS": {"G2A": 4984, "G2B": 9416},
}
EXPECTED_C24B_ALLOCATION = {
    "DOUBLE_GRAPHS": {"G2B": 16},
    "OUTGOING_GRAPHS": {},
    "SINGLE_GRAPHS": {"G2B": 152},
}
ROLE_ORDER = {"G2A_SHEET": 0, "G2B_POSITIVE_SIDE": 1, "G2B_EXACT_EMPTY_SIDE": 2}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def path_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def rows(name: str) -> Iterable[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for raw_line in stream:
            need(raw_line.endswith(b"\n"), "source newline:" + name)
            row = json.loads(raw_line[:-1])
            need(isinstance(row, dict), "source row object:" + name)
            yield row


def row_closure(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), "row closure:" + label)


def validate_pins() -> None:
    for name, expected in PINS.items():
        need(path_sha(ROOT / name) == expected, "input pin:" + name)


def validate_graph_geometry(row: dict[str, Any]) -> dict[str, Any]:
    row_closure(row, "C10")
    graph_id = row.get("graph_id")
    graph_class = row.get("graph_class")
    need(isinstance(graph_id, str) and graph_class in CLASS_TO_TERMINAL, "C10 recognized graph")
    need(row.get("coordinate_parameter") == "TPS", "C10 TPS coordinate")
    for name in ("base_domain_ast", "carrier_domain_ast", "equation_ast", "exact_support_ast"):
        need(row["ast_sha256"][name + "_sha256"] == digest(row[name]), "C10 AST closure:" + name)
    need(row["exact_support_ast"] == {
        "op": "AND",
        "args": [row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]],
    }, "C10 exact-support construction")
    props = row["support_properties"]
    need(props.get("R248_rectangle_used_as_support") is False, "C10 rectangle not promoted to support")
    need(props.get("connected") is True and props.get("nonempty") is True, "C10 connected nonempty support")
    need(props.get("one_graph_point_per_exact_base_point") is True, "C10 one graph point")
    certificate = row["monotone_graph_certificate"]
    need(certificate.get("unique_t_for_every_exact_base_point") is True, "C10 graph uniqueness")
    if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
        need(graph_id.startswith("round235-single-endpoint:"), "single partial graph authority")
        need(props.get("s_independent_equation") is True, "single partial s independence")
        need(certificate.get("kind") == "STRICT_T_MONOTONE_IMPLICIT_GRAPH_OVER_CONNECTED_SIGN_STRADDLE_BASE", "single partial monotone kind")
        topology = certificate.get("face_p_topology_certificate", {})
        need(topology.get("topology") in {"INTERNAL_P_BAND", "LOWER_P_ATTACHED", "UPPER_P_ATTACHED"}, "single partial topology")
        need(topology.get("connected_sign_straddle_p_interval") is True, "single partial connected p interval")
        expected_cut_count = 2 if topology.get("topology") == "INTERNAL_P_BAND" else 1
        need(topology.get("implicit_cut_root_count") == expected_cut_count, "single partial cut-root count")
        need(len(topology.get("implicit_cut_root_descriptors", [])) == expected_cut_count, "single partial cut descriptors")
        need(topology.get("s_independence", {}).get("full_s_interval_retained") is True, "single partial full s interval")
    elif graph_class == "R235_SOURCE_EXACT_FACE_FULL_BASE":
        need(graph_id.startswith("round235-single-endpoint:"), "single exact-face graph authority")
        need(props.get("s_independent_equation") is True, "single exact-face s independence")
        need(certificate.get("kind") == "EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH", "single exact-face kind")
        need(certificate.get("strict_t_derivative_exact") == {"denominator": 25, "numerator": 9}, "single exact-face derivative")
    return {
        "graph_id": graph_id,
        "graph_class": graph_class,
        "terminal": CLASS_TO_TERMINAL[graph_class],
        "sheet_member_id": row["sheet_member_id"],
        "ast_sha256": dict(row["ast_sha256"]),
        "c10_row_sha256": row["row_sha256"],
        "geometry_root_sha256": digest({
            "graph_id": graph_id,
            "graph_class": graph_class,
            "base_domain_ast": row["base_domain_ast"],
            "carrier_domain_ast": row["carrier_domain_ast"],
            "equation_ast": row["equation_ast"],
            "exact_support_ast": row["exact_support_ast"],
        }),
    }


def load_graphs() -> tuple[dict[str, dict[str, Any]], dict[str, int], dict[str, int]]:
    graphs: dict[str, dict[str, Any]] = {}
    terminals: Counter[str] = Counter()
    single_classes: Counter[str] = Counter()
    for row in rows(C10):
        graph = validate_graph_geometry(row)
        graph_id = graph["graph_id"]
        need(graph_id not in graphs, "C10 unique graph id")
        graphs[graph_id] = graph
        terminals[graph["terminal"]] += 1
        if graph["terminal"] == "SINGLE_GRAPHS":
            single_classes[graph["graph_class"]] += 1
    need(len(graphs) == 5264 and dict(terminals) == EXPECTED_ROOT_PARTITION, "C10 terminal partition")
    need(dict(single_classes) == EXPECTED_SINGLE_CLASSES, "C10 single class partition")
    return graphs, dict(terminals), dict(single_classes)


def load_relation_kernels(
    graphs: dict[str, dict[str, Any]],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any], dict[str, Any]]:
    selected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_members: set[str] = set()
    allocation_a: dict[str, Counter[str]] = defaultdict(Counter)
    allocation_b: dict[str, Counter[str]] = defaultdict(Counter)
    c24a_rows = 0
    for row in rows(C24A):
        row_closure(row, "C24A")
        c24a_rows += 1
        graph_id = row.get("graph_id")
        need(graph_id in graphs, "C24A graph belongs to C10 universe")
        family = row.get("coarse_family")
        need(family in {"G2A", "G2B"}, "C24A family")
        kind = "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY" if family == "G2A" else "G2B_RELATION_BACKED_SIDE_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
        need(row.get("row_kind") == kind, "C24A row kind")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24A support closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24A theorem closure")
        member_id = row.get("member_id")
        need(isinstance(member_id, str) and member_id not in seen_members, "C24A unique member allocation")
        seen_members.add(member_id)
        terminal = graphs[graph_id]["terminal"]
        allocation_a[terminal][family] += 1
        if terminal == "SINGLE_GRAPHS":
            selected[graph_id].append({**row, "support_kernel": "C24A"})
    need(c24a_rows == 15224, "C24A full denominator")
    need({k: dict(v) for k, v in allocation_a.items()} == EXPECTED_C24A_ALLOCATION, "C24A exact terminal allocation")
    c24b_rows = 0
    for row in rows(C24B):
        row_closure(row, "C24B")
        c24b_rows += 1
        graph_id = row.get("graph_id")
        need(graph_id in graphs, "C24B graph belongs to C10 universe")
        need(row.get("coarse_family") == "G2B", "C24B G2B family")
        need(row.get("row_kind") == "G2B_NEGATIVE_NONINCIDENCE_EMPTY_MEMBER_AND_REPRESENTATION_SET_EQUALITY", "C24B row kind")
        need(row.get("normalized_support_ast") == {"ambient_coordinates": ["t", "p", "s"], "coordinate_parameter": "TPS", "kind": "EMPTY_SET"}, "C24B exact empty support")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24B support closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24B theorem closure")
        theorem = row["semantic_theorem_ast"]
        need(theorem.get("strict_branch_intersection_with_complete_defining_carrier_is_empty") is True, "C24B exact nonincidence")
        need(theorem.get("sole_registered_representation_set_equals_empty_member_support") is True, "C24B empty representation equality")
        member_id = row.get("member_id")
        need(isinstance(member_id, str) and member_id not in seen_members, "C24A/C24B unique member allocation")
        seen_members.add(member_id)
        terminal = graphs[graph_id]["terminal"]
        allocation_b[terminal]["G2B"] += 1
        if terminal == "SINGLE_GRAPHS":
            selected[graph_id].append({**row, "support_kernel": "C24B"})
    need(c24b_rows == 168, "C24B full denominator")
    normalized_b = {terminal: dict(allocation_b.get(terminal, Counter())) for terminal in EXPECTED_C24B_ALLOCATION}
    need(normalized_b == EXPECTED_C24B_ALLOCATION, "C24B exact terminal allocation")
    single_ids = {graph_id for graph_id, graph in graphs.items() if graph["terminal"] == "SINGLE_GRAPHS"}
    need(set(selected) == single_ids, "all single roots have kernel rows")
    pattern: Counter[tuple[str, int, int, int]] = Counter()
    selected_members: set[str] = set()
    for graph_id in sorted(single_ids):
        graph = graphs[graph_id]
        values = selected[graph_id]
        positive = Counter(row["coarse_family"] for row in values if row["support_kernel"] == "C24A")
        empty = sum(row["support_kernel"] == "C24B" for row in values)
        pattern[(graph["graph_class"], positive["G2A"], positive["G2B"], empty)] += 1
        need(positive["G2A"] == 1, "single exactly one G2A sheet")
        sheet = next(row for row in values if row["support_kernel"] == "C24A" and row["coarse_family"] == "G2A")
        need(sheet["normalized_support_ast_sha256"] == graph["ast_sha256"]["base_domain_ast_sha256"], "single sheet/base equality")
        support_kind = sheet["semantic_theorem_ast"].get("support_kind")
        if graph["graph_class"] == "R235_TARGET_POSITIVE_PARTIAL_BASE":
            need(sheet["member_id"] != graph["sheet_member_id"], "partial graph uses fresh exact-partial sheet")
            need(support_kind == "G2A_NEW_EXACT_PARTIAL_BASE_SHEET", "partial exact-sheet semantic kind")
        else:
            need(sheet["member_id"] == graph["sheet_member_id"], "exact-face C10/C24A sheet identity")
            need(support_kind == "G2A_EXISTING_EXACT_BASE_SHEET", "exact-face existing-sheet semantic kind")
        selected_members.update(row["member_id"] for row in values)
    expected_pattern = Counter({
        ("R235_TARGET_POSITIVE_PARTIAL_BASE", 1, 2, 0): 4432,
        ("R235_SOURCE_EXACT_FACE_FULL_BASE", 1, 1, 0): 400,
        ("R235_SOURCE_EXACT_FACE_FULL_BASE", 1, 1, 1): 152,
    })
    need(pattern == expected_pattern, "single exact per-root kernel pattern")
    need(len(selected_members) == 14552, "single selected member denominator")
    allocation = {
        "C24A": {terminal: dict(allocation_a[terminal]) for terminal in sorted(EXPECTED_C24A_ALLOCATION)},
        "C24B": {terminal: dict(allocation_b.get(terminal, Counter())) for terminal in sorted(EXPECTED_C24B_ALLOCATION)},
    }
    pattern_json = [
        {"graph_class": key[0], "G2A_positive": key[1], "G2B_positive": key[2], "G2B_exact_empty": key[3], "root_count": count}
        for key, count in sorted(pattern.items())
    ]
    return selected, allocation, {"pattern": pattern_json, "member_ids": selected_members}


def load_current_members(member_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    c15: dict[str, dict[str, Any]] = {}
    for row in rows(C15):
        member_id = row.get("registry_member_id")
        if member_id not in member_ids:
            continue
        row_closure(row, "C15")
        need(member_id not in c15, "C15 selected unique")
        c15[member_id] = row
    c25: dict[str, dict[str, Any]] = {}
    for row in rows(C25):
        member_id = row.get("member_id")
        if member_id not in member_ids:
            continue
        row_closure(row, "C25")
        need(member_id not in c25, "C25 selected unique")
        c25[member_id] = row
    need(set(c15) == member_ids and set(c25) == member_ids, "C15/C25 selected cover")
    return c15, c25


def load_features(single_graphs: dict[str, dict[str, Any]], member_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    g1: dict[str, dict[str, Any]] = {}
    g2: dict[str, dict[str, Any]] = {}
    for row in rows(C26):
        node = row.get("node_id")
        feature_id = row.get("feature_id")
        chosen = (node == "G1" and feature_id in single_graphs) or (node in {"G2A", "G2B"} and feature_id in member_ids)
        if not chosen:
            continue
        row_closure(row, "C26")
        target = g1 if node == "G1" else g2
        need(feature_id not in target, "C26 selected unique")
        target[feature_id] = row
    need(set(g1) == set(single_graphs), "C26 G1 single cover")
    need(set(g2) == member_ids, "C26 G2 single cover")
    return g1, g2


def proof_row(relation: dict[str, Any], c15: dict[str, Any], c25: dict[str, Any], c26: dict[str, Any]) -> dict[str, Any]:
    member_id = relation["member_id"]
    family = relation["coarse_family"]
    kernel = relation["support_kernel"]
    need(c15["registry_member_id"] == c25["member_id"] == member_id, "member identity join")
    need(c15["fresh_component_id"] == c25["fresh_component_id"] == relation["fresh_component_id"], "component join")
    need(c15["base_root_id"] == c25["base_root_id"] == relation["base_root_id"], "base-root join")
    need(c15["official_key_id"] == c25["official_key_id"] == relation["official_key_id"], "official-key join")
    need(c25["coarse_family"] == family, "family join")
    need(c25["normalized_support_ast_sha256"] == relation["normalized_support_ast_sha256"], "support join")
    need(c25["support_semantic_certificate_sha256"] == relation["semantic_theorem_ast_sha256"], "theorem join")
    need(c25["source_bindings"]["support_kernel"] == kernel, "C25 kernel join")
    need(c25["source_bindings"]["support_kernel_row_sha256"] == relation["row_sha256"], "C25 kernel row join")
    need(c25["source_bindings"]["C15_member_row_sha256"] == c15["row_sha256"], "C25 C15 binding")
    expected_semantic = "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY" if kernel == "C24A" else "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY"
    need(c25["support_semantic_kind"] == expected_semantic, "C25 semantic kind")
    need(c26["node_id"] == family and c26["owner_member_id"] == member_id, "C26 feature owner")
    expected_obligation = (
        "G2A_GRAPH_TO_SHEET_IDENTIFICATION" if family == "G2A" else
        "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE" if kernel == "C24A" else
        "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE"
    )
    need(c26["obligation_kind"] == expected_obligation, "C26 obligation kind")
    need(c26["definition_or_dependency_theorem_ast_sha256"] == relation["semantic_theorem_ast_sha256"], "C26 theorem join")
    need(c26["source_bindings"]["source_kernel"] == kernel, "C26 kernel join")
    need(c26["source_bindings"]["source_row_sha256"] == relation["row_sha256"], "C26 source-row join")
    role = "G2A_SHEET" if family == "G2A" else "G2B_POSITIVE_SIDE" if kernel == "C24A" else "G2B_EXACT_EMPTY_SIDE"
    return {
        "role": role,
        "support_kernel": kernel,
        "member_id": member_id,
        "fresh_component_id": c15["fresh_component_id"],
        "base_root_id": c15["base_root_id"],
        "official_key_id": c15["official_key_id"],
        "normalized_support_ast_sha256": relation["normalized_support_ast_sha256"],
        "semantic_theorem_ast_sha256": relation["semantic_theorem_ast_sha256"],
        "C15_row_sha256": c15["row_sha256"],
        "C24_row_sha256": relation["row_sha256"],
        "C25_row_sha256": c25["row_sha256"],
        "C26_row_sha256": c26["row_sha256"],
    }


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_pins()
    graphs, root_partition, single_classes = load_graphs()
    relations, allocation, pattern_info = load_relation_kernels(graphs)
    member_ids = pattern_info.pop("member_ids")
    single_graphs = {graph_id: graph for graph_id, graph in graphs.items() if graph["terminal"] == "SINGLE_GRAPHS"}
    c15, c25 = load_current_members(member_ids)
    g1, g2 = load_features(single_graphs, member_ids)
    output: list[dict[str, Any]] = []
    for graph_id in sorted(single_graphs):
        graph = single_graphs[graph_id]
        feature = g1[graph_id]
        need(feature["obligation_kind"] == "G1_EXACT_GRAPH_DEFINITION", "C26 G1 obligation")
        need(feature["owner_member_id"] == graph["sheet_member_id"], "C26 G1 owner")
        need(feature["definition_or_dependency_theorem_ast_sha256"] == digest(graph["ast_sha256"]), "C26 G1 AST binding")
        need(feature["source_bindings"]["source_kernel"] == "C10", "C26 G1 kernel")
        need(feature["source_bindings"]["source_row_sha256"] == graph["c10_row_sha256"], "C26 G1 row binding")
        dispositions = [proof_row(row, c15[row["member_id"]], c25[row["member_id"]], g2[row["member_id"]]) for row in relations[graph_id]]
        dispositions.sort(key=lambda row: (ROLE_ORDER[row["role"]], row["member_id"]))
        census = Counter(row["role"] for row in dispositions)
        need(census["G2A_SHEET"] == 1 and census["G2B_POSITIVE_SIDE"] in {1, 2} and census["G2B_EXACT_EMPTY_SIDE"] in {0, 1}, "single disposition shape")
        need(len({row["member_id"] for row in dispositions}) == len(dispositions), "single disposition unique members")
        body = {
            "schema": SCHEMA + ".candidate-row.v1",
            "terminal": "SINGLE_GRAPHS",
            "graph_id": graph_id,
            "graph_class": graph["graph_class"],
            "geometry_root_sha256": graph["geometry_root_sha256"],
            "base_domain_ast_sha256": graph["ast_sha256"]["base_domain_ast_sha256"],
            "carrier_domain_ast_sha256": graph["ast_sha256"]["carrier_domain_ast_sha256"],
            "equation_ast_sha256": graph["ast_sha256"]["equation_ast_sha256"],
            "exact_support_ast_sha256": graph["ast_sha256"]["exact_support_ast_sha256"],
            "C10_row_sha256": graph["c10_row_sha256"],
            "C26_G1_row_sha256": feature["row_sha256"],
            "dispositions": dispositions,
            "physical_totality_certificate": {
                "root_classified_from_C10_before_relation_join": True,
                "exactly_one_G2A_sheet": True,
                "positive_and_exact_empty_registered_G2B_rows_exhaust_C24A_C24B_for_root": True,
                "all_dispositions_materially_join_C15_C24_C25_C26": True,
                "terminal_assignment_unique_in_full_C10_C24_partition": True,
                "G2B_positive_count": census["G2B_POSITIVE_SIDE"],
                "G2B_exact_empty_count": census["G2B_EXACT_EMPTY_SIDE"],
                "unresolved": 0,
            },
            "formal_credit": 0,
        }
        output.append({**body, "candidate_digest": digest(body)})
    need(len(output) == 4984 and len({row["candidate_digest"] for row in output}) == 4984, "4984 unique single candidates")
    result_body = {
        "schema": SCHEMA + ".result.v1",
        "status": "PASS_ZERO_CREDIT__SINGLE_GRAPHS_4984_ROOTS_4984_SHEETS_9416_POSITIVE_SIDES_152_EXACT_EMPTY_SIDES",
        "implementation_neutral_semantics": "STREAM_OR_SQLITE_MUST_REBUILD_IDENTICAL_MATERIALIZED_PROOF_ROWS",
        "candidate_universe": "C10_GRAPH_CLASS_AND_EXACT_GEOMETRY_BEFORE_C24A_C24B_C25_C26_JOINS",
        "C10_terminal_partition": root_partition,
        "single_graph_class_partition": single_classes,
        "C24_full_terminal_allocation": allocation,
        "single_per_root_kernel_patterns": pattern_info["pattern"],
        "single_root_count": len(output),
        "G2A_sheet_count": 4984,
        "G2B_positive_side_count": 9416,
        "G2B_exact_empty_side_count": 152,
        "selected_member_count": 14552,
        "unresolved_count": 0,
        "duplicate_or_orphan_count": 0,
        "ordered_candidate_digests_sha256": digest([row["candidate_digest"] for row in output]),
        "input_pins": [{"filename": name, "sha256": PINS[name]} for name in sorted(PINS)],
        "legacy_transition_family_table_used": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0,
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return output, {**result_body, "result_sha256": digest(result_body)}


def write_output(target: Path, ledger: list[dict[str, Any]], result: dict[str, Any]) -> None:
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    with gzip.GzipFile(filename="", mode="wb", fileobj=(target / "ledger.jsonl.gz").open("wb"), mtime=0) as stream:
        for row in ledger:
            stream.write(canonical(row) + b"\n")
    (target / "result.json").write_bytes(canonical(result))
    manifest = {"ledger.jsonl.gz": path_sha(target / "ledger.jsonl.gz"), "result.json": path_sha(target / "result.json")}
    (target / "manifest.json").write_bytes(canonical(manifest))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed.isdigit(), "numeric seed")
    ledger, result = reconstruct()
    write_output(AUDIT / args.output_tag, ledger, result)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
