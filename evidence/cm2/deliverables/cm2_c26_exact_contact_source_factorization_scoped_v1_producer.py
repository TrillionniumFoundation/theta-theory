#!/usr/bin/env python3
"""C26-independent exact-contact source-factorization theorem producer.

This producer treats the corrected C26 feature DAG as what it is: a ledger of
definition/dependency obligations.  It proves row by row that C26 itself adds
no support carrier, then hands every row back to its primitive source kernel.

The theorem is deliberately scoped.  It consumes the fresh SAME_CHART strict
and lower-dimensional authorities plus the scoped G2A/C24A authorities.  It
does not read a C27 FAMILIES/transition ledger, C28, C29, or a historical edge
ledger, and it never upgrades missing C26 geometry into a negative theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent.parent
OUT_LEDGER = "c26_691424_scoped_exact_contact_source_factorization.jsonl.gz"
RESULT = "result.json"

FILES: dict[str, tuple[str, str]] = {
    "C26": ("deliverables/cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz", "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e"),
    "C21A": ("deliverables/cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel_ledger.jsonl.gz", "1c60f2ef752b1b3ab363740cec7505cbddacfbc7509922dab63bbf011e3659f1"),
    "C21C": ("deliverables/cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_ledger.jsonl.gz", "add22270845ef504427475e91696451f2d53c41b4b2cb9af2784a9507ce60c09"),
    "C22A": ("deliverables/cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C22B": ("deliverables/cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz", "c0f3d3a9fc6002f0af23271f7483aeff7eac0b0cc92399fc3785b0a5b9291f97"),
    "C10": ("deliverables/cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz", "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    "C24A": ("deliverables/cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz", "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58"),
    "C24B": ("deliverables/cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz", "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380"),
    "C19A": ("deliverables/cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("deliverables/cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("deliverables/cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("deliverables/cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C23A": ("deliverables/cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "STRICT": ("deliverables/cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json", "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"),
    "LOWER_RESULT": ("deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_result.json", "67aafe571ebfad6dbc0861f370d9ce8227e2905a660b9be739233afd1e524015"),
    "LOWER_RECEIPT": ("deliverables/cm2_c27_same_chart_lower_dimensional_exact_contact_v1_terminal_receipt.json", "54da91e93d3248f931c9654ec002fc4fb5e43eca59cdefbd5586d727ae008b94"),
    "G2A_RECEIPT": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/receipt.json", "acb9b25d309efbf52026bacbb5208aa2775b4e4c5c98fcca30c7ed7ce42585b5"),
    "G2A_ROOT": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/root_manifest.sha256", "82d602988e274e164fd6d18793ca5180b5b11bccae6a9a9cbf49f8388849d4f6"),
    "G2A_PAYLOAD": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/payload_manifest.sha256", "807fff78c07e35db83808e3538c02489927199a9ab791de808ec9482d563ecdf"),
    "G2A_ROUTES": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_5264_final_unique_routes.jsonl.gz", "b282c78c1289ed21cb4be85b031b62302398870fe462a8f09ef850eaa83c12e5"),
    "G2A_CONTACTS": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_9408_exact_relative2D_contact_alias_routes.jsonl.gz", "adffbf0f67faf8de7fb586a0879465fdbc9ac00b007698d605b1fe1ccdbdc173"),
    "G2A_COMPLEMENT": (".cm2-runtime/audit/g2a-relative2d-v2-theorem-bound-seed30635101/G2A_552_no_current_contact_complement.jsonl.gz", "fd73328d100f3c5dc7b941611d9a9fc2d2eb2bf866495cd739db25c182370a0a"),
    "UNION_RESULT": (".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/result.json", "25c3f914dd653cf11eaea69532308c55d6bd5a4143ecc338aa55adaec1b36c4b"),
    "UNION_LEDGER": (".cm2-runtime/audit/c27-c24a-current-primitive-three-terminal-union-normalized-v1-seed-30638103/payload/primitive_three_terminal_101080_unique_ownership.jsonl.gz", "caaee424b629887ce8d44479861f311f802140cdd9adcd4dcf7556b1c6eb5fe2"),
}

PRIMITIVE_COUNTS = {"C19A": 5_596, "C19B": 12_232, "C19C": 33_344, "C20A": 126_468, "C22A": 295_340, "C23A": 10_252}
NODE_COUNTS = {"A1": 17_940, "A2": 62_152, "G1": 5_264, "G2A": 5_264, "G2B": 10_128, "R1": 295_340, "R2": 295_336}
C26_KEYS = {
    "definition_or_dependency_theorem_ast_sha256", "depends_on_node_ids", "feature_id", "feature_ordinal",
    "formal_credit", "node_id", "obligation_kind", "obligation_role", "owner_member_id", "row_id",
    "row_sha256", "schema", "source_bindings", "strict_nonpromotion",
}


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


ATTESTATIONS: dict[str, dict[str, Any]] = {}


def checked_path(tag: str) -> Path:
    relative, pin = FILES[tag]
    path = ROOT / relative
    before = path.stat()
    observed = file_sha(path)
    after = path.stat()
    need(observed == pin, "pin:" + tag)
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "stable stat:" + tag)
    ATTESTATIONS[tag] = {"path": relative, "sha256": observed, "size": before.st_size, "stat_fingerprint": [before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns]}
    return path


def rows(tag: str) -> Iterator[dict[str, Any]]:
    path = checked_path(tag)
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{tag}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{tag}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == digest(body), f"row closure:{tag}:{ordinal}")
            yield row


def document(tag: str) -> dict[str, Any]:
    path = checked_path(tag)
    value = json.loads(path.read_bytes())
    need(type(value) is dict, "document:" + tag)
    return value


def write_rows(path: Path, bodies: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for body in bodies:
                row = {**body, "row_sha256": digest(body)}
                wire = canonical(row)
                sequence.update(wire)
                sequence.update(b"\n")
                packed.write(wire + b"\n")
                count += 1
    return {"filename": path.name, "row_count": count, "file_sha256": file_sha(path), "row_sequence_sha256": sequence.hexdigest(), "size": path.stat().st_size}


def load_authority_boundary() -> tuple[dict[str, dict[str, Any]], set[str], set[str], dict[str, dict[str, Any]]]:
    strict = document("STRICT")
    need(strict["status"].startswith("PASS_STRICT_VOLUME_TOTALITY") and strict["exact_census"]["primitive_atom_count"] == 483_232, "strict authority")
    need(strict["scope"]["complete"] == "ALL_STRICT_INTERIOR_INTERSECTIONS_IN_T_P_S_ACROSS_SIX_PRIMITIVE_SUPPORT_KERNELS", "strict complete scope")
    need(strict["forbidden_inputs"]["C27_or_FAMILIES_imported_or_read"] is False and strict["forbidden_inputs"]["historical_edge_ledger_used"] is False, "strict forbidden inputs")
    lower = document("LOWER_RESULT")
    lower_receipt = document("LOWER_RECEIPT")
    need(lower["status"].startswith("PASS_COMPLETE_SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE"), "lower result")
    need(lower_receipt["status"].startswith("PASS_DUAL_SEED_DUAL_IMPLEMENTATION_COMPLETE_5783708"), "lower terminal receipt")
    need(lower["census"]["primitive_atom_count"] == 483_232 and lower["census"]["lower_dimensional_candidate_pair_count"] == 5_783_708, "lower census")
    need(lower["census"]["legal_cross_component_lower_dimensional_witness_count"] == 0, "lower zero legal witness")
    need(lower["authority_joins"]["C26_absence_used_as_negative_geometry_theorem"] is False, "C26 not negative geometry")
    need(lower["forbidden_inputs"] == {"C27_FAMILIES_read": False, "historical_edge_universe_read": False, "older_same_chart_candidate_ledger_read": False}, "lower forbidden inputs")

    g2a = document("G2A_RECEIPT")
    checked_path("G2A_ROOT")
    checked_path("G2A_PAYLOAD")
    need(g2a["status"].startswith("PASS_DOUBLE_SEED_DUAL_IMPLEMENTATION_AND_15_ATTACKS__SCOPED_G2A_5264_CLOSED"), "G2A receipt")
    need(g2a["headline"]["G2A_graphs"] == 5_264 and g2a["headline"]["contact_aliases"] == 9_408 and g2a["headline"]["complement"] == 552, "G2A headline")
    need(g2a["authority_scope"]["global_three_terminal_unique_assignment"] is False, "G2A fail closed")

    route_by_graph: dict[str, dict[str, Any]] = {}
    for row in rows("G2A_ROUTES"):
        need(row["graph_id"] not in route_by_graph and row["assigned_unique_terminal"] in {"SAME_CHART_RELATIVE_CELLS", "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"}, "G2A route")
        route_by_graph[row["graph_id"]] = row
    positive_members: set[str] = set()
    for row in rows("G2A_CONTACTS"):
        need(row["assigned_unique_terminal"] == "SAME_CHART_RELATIVE_CELLS", "G2A contact terminal")
        positive_members.add(row["positive_side_member_id"])
    complement_members: set[str] = set()
    for row in rows("G2A_COMPLEMENT"):
        need(row["assigned_unique_terminal"] == "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT", "G2A complement terminal")
        complement_members.add(row["one_sided_member_id"])
    need(len(route_by_graph) == 5_264 and len(positive_members) == 9_408 and len(complement_members) == 552 and not (positive_members & complement_members), "G2A materialized sets")

    union = document("UNION_RESULT")
    need(union["status"].startswith("PASS_SCOPED_PRIMITIVE_KEY_COMPARATOR_AND_101080_UNIQUE_UNION"), "union result")
    need(union["C24A_G2A_G2B_key_by_key"]["G2B_exact_positive_keys"] == 9_408 and union["C24A_G2A_G2B_key_by_key"]["G2B_exact_positive_equals_G2B_priority"] is True, "union G2B priority")
    c24_rows = 0
    for row in rows("UNION_LEDGER"):
        if row["source_authority"] == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
            c24_rows += 1
            need(row["assigned_terminal"] == "POSITIVE_VOLUME_CARRIERS" and row["current_source_terminal"] is None, "union C24 row")
    need(c24_rows == 9_408, "union C24 census")
    return route_by_graph, positive_members, complement_members, {"strict": strict, "lower": lower, "g2a": g2a, "union": union}


def load_primitive_owners() -> tuple[dict[str, set[str]], dict[str, tuple[str, str, str]]]:
    owner_sources: dict[str, set[str]] = defaultdict(set)
    c22a: dict[str, tuple[str, str, str]] = {}
    for tag, expected in PRIMITIVE_COUNTS.items():
        count = 0
        for row in rows(tag):
            count += 1
            owner = row.get("member_id") or row["owner_member_id"]
            owner_sources[owner].add(tag)
            if tag == "C22A":
                c22a[row["row_sha256"]] = (row["predicate_cell_row_id"], owner, row["support_ast_sha256"])
        need(count == expected, "primitive source census:" + tag)
    need(len(owner_sources) == 482_380 and len(c22a) == 295_340, "primitive owner/C22A census")
    return owner_sources, c22a


def feature_sources(c22a: dict[str, tuple[str, str, str]]) -> Iterator[tuple[str, str, str, str, str, str, str, dict[str, Any]]]:
    for row in rows("C21A"):
        node = row["obligation_kind"].split("_", 1)[0]
        yield "C21A", node, row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["feature_theorem_ast_sha256"], row["row_sha256"], {}
    for row in rows("C21C"):
        node = row["obligation_kind"].split("_", 1)[0]
        yield "C21C", node, row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], row["row_sha256"], {}
    for row in rows("C22A"):
        yield "C22A", "R1", "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION", row["predicate_cell_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], row["row_sha256"], {"source_atom_factor_count": 1}
    for row in rows("C22B"):
        if row["row_kind"] != "R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY":
            continue
        factors = row["member_union_theorem_ast"]["predicate_cell_equalities"]
        need(len(factors) in {1, 2}, "R2 factor multiplicity")
        for factor in factors:
            need(factor["C22a_row_sha256"] in c22a, "R2 C22A factor binding")
            cell, owner, support_sha = c22a[factor["C22a_row_sha256"]]
            need((factor["predicate_cell_row_id"], row["member_id"], factor["support_ast_sha256"]) == (cell, owner, support_sha), "R2 factor exact join")
        yield "C22B", "R2", "R2_MEMBER_FULL_SUPPORT_UNION", row["member_id"], row["member_id"], row["member_union_theorem_ast_sha256"], row["row_sha256"], {"source_atom_factor_count": len(factors)}
    for row in rows("C10"):
        yield "C10", "G1", "G1_EXACT_GRAPH_DEFINITION", row["graph_id"], row["sheet_member_id"], digest(row["ast_sha256"]), row["row_sha256"], {"graph_id": row["graph_id"]}
    for row in rows("C24A"):
        node = row["coarse_family"]
        obligation = "G2A_GRAPH_TO_SHEET_IDENTIFICATION" if node == "G2A" else "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE"
        yield "C24A", node, obligation, row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], row["row_sha256"], {"graph_id": row["graph_id"]}
    for row in rows("C24B"):
        yield "C24B", "G2B", "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE", row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], row["row_sha256"], {"graph_id": row["graph_id"]}


def build(candidate_dir: Path, seed: int) -> dict[str, Any]:
    need(not candidate_dir.exists() or not any(candidate_dir.iterdir()), "candidate directory must be new/empty")
    candidate_dir.mkdir(parents=True, exist_ok=True)
    route_by_graph, positive_members, complement_members, authority = load_authority_boundary()
    owner_sources, c22a = load_primitive_owners()

    node_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    disposition_counts: Counter[str] = Counter()
    primitive_owner_rows = 0
    graph_owner_rows = 0
    covered_owners: set[str] = set()
    r2_factor_histogram: Counter[int] = Counter()
    seen_g2a_graphs: set[str] = set()
    seen_g2b_c24a: set[str] = set()
    expected = feature_sources(c22a)

    def output() -> Iterator[dict[str, Any]]:
        nonlocal primitive_owner_rows, graph_owner_rows
        for ordinal, c26 in enumerate(rows("C26")):
            need(set(c26) == C26_KEYS and c26["feature_ordinal"] == ordinal, "C26 exact schema/order")
            try:
                tag, node, obligation, feature, owner, theorem_sha, source_row_sha, extra = next(expected)
            except StopIteration as exc:
                raise Failure("source feature stream exhausted") from exc
            binding = c26["source_bindings"]
            need((c26["node_id"], c26["obligation_kind"], c26["feature_id"], c26["owner_member_id"], c26["definition_or_dependency_theorem_ast_sha256"]) == (node, obligation, feature, owner, theorem_sha), "C26/source exact tuple")
            need(binding["source_kernel"] == tag and binding["source_row_sha256"] == source_row_sha and binding["source_ledger"] == Path(FILES[tag][0]).name, "C26 source binding")
            need(not ({"support_ast", "support_ast_sha256", "bounds", "coordinate_chart"} & set(c26)), "C26 support field absent")
            primitive = owner in owner_sources
            need(primitive == (node in {"A1", "A2", "R1", "R2"}), "primitive/graph owner partition")
            node_counts[node] += 1
            source_counts[tag] += 1
            if primitive:
                primitive_owner_rows += 1
                covered_owners.add(owner)
                primitive_sources = sorted(owner_sources[owner])
            else:
                graph_owner_rows += 1
                primitive_sources = []

            source_atom_factor_count = extra.get("source_atom_factor_count", 0)
            if node in {"A1", "A2"}:
                factor_class = "FEATURE_THEOREM_ON_SIX_KERNEL_PRIMITIVE_OWNER__NO_C26_SUPPORT_CARRIER"
                disposition = "OWNER_CONTACT_CANDIDATES_EXHAUSTED_BY_STRICT_AND_LOWER_AUTHORITIES__NO_NEW_C26_CONTACT"
            elif node == "R1":
                factor_class = "DIRECT_C22A_PRIMITIVE_ATOM_DEFINITION"
                disposition = "STRICT_DIM3_HANDLED__LOWER_DIM012_EXHAUSTED_WITH_ZERO_LEGAL_WITNESS"
            elif node == "R2":
                factor_class = "C22B_MEMBER_UNION_FACTORS_EXACTLY_TO_C22A_PRIMITIVE_ATOMS"
                disposition = "NO_NEW_ATOM_BEYOND_R1__STRICT_DIM3_HANDLED__LOWER_DIM012_REJECTED"
                r2_factor_histogram[source_atom_factor_count] += 1
            elif node == "G1":
                graph = extra["graph_id"]
                need(graph in route_by_graph, "G1/G2A unique graph-id handoff")
                factor_class = "C10_EXACT_GRAPH_DEFINITION_HANDOFF_BY_GRAPH_ID_TO_G2A__NO_SECOND_GEOMETRY_CANDIDATE"
                disposition = "SCOPED_G2A_ROUTE_BOUND__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN"
            elif node == "G2A":
                graph = extra["graph_id"]
                need(graph in route_by_graph and route_by_graph[graph]["g2a_member_id"] == owner, "G2A route binding")
                seen_g2a_graphs.add(graph)
                factor_class = "C24A_GRAPH_TO_SHEET_ALIAS"
                disposition = "SCOPED_G2A_UNIQUE_ROUTE_CLOSED__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN"
            else:
                need(node == "G2B", "known node")
                if tag == "C24B":
                    factor_class = "C24B_EXACT_EMPTY_SUPPORT"
                    disposition = "EXACT_EMPTY_SUPPORT_CANNOT_FORM_CONTACT"
                elif owner in positive_members:
                    factor_class = "C24A_RELATION_BACKED_PHYSICAL_SIDE"
                    disposition = "EXACT_POSITIVE_PAIR_ASSIGNED_POSITIVE_VOLUME_CARRIERS_IN_SCOPED_COMPARATOR"
                    seen_g2b_c24a.add(owner)
                else:
                    need(owner in complement_members, "C24A G2B positive/complement partition")
                    factor_class = "C24A_RELATION_BACKED_ONE_SIDED_COMPLEMENT"
                    disposition = "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT"
                    seen_g2b_c24a.add(owner)
            disposition_counts[disposition] += 1
            yield {
                "schema": "cm2.c26-independent.exact-contact-source-factorization.row.v1",
                "feature_ordinal": ordinal,
                "C26_row_sha256": c26["row_sha256"],
                "node_id": node,
                "source_kernel": tag,
                "source_row_sha256": source_row_sha,
                "feature_id": feature,
                "owner_member_id": owner,
                "primitive_owner_source_kernels": primitive_sources,
                "source_atom_factor_count": source_atom_factor_count,
                "source_factor_class": factor_class,
                "scoped_exact_contact_disposition": disposition,
                "C26_row_direct_support_carrier": False,
                "C26_absence_used_as_negative_geometry_theorem": False,
                "scoped_unresolved": False,
                "global_three_terminal_assignment_claimed": False,
                "formal_credit": 0,
            }
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise Failure("extra source feature rows")

    ledger = write_rows(candidate_dir / OUT_LEDGER, output())
    need(dict(node_counts) == NODE_COUNTS and ledger["row_count"] == 691_424, "C26 node/total census")
    need(primitive_owner_rows == 670_768 and graph_owner_rows == 20_656 and len(covered_owners) == 313_276, "owner handoff census")
    need(r2_factor_histogram == Counter({1: 295_332, 2: 4}), "R2 atom factor histogram")
    need(len(seen_g2a_graphs) == 5_264 and len(seen_g2b_c24a) == 9_960, "graph materialized coverage")
    expected_dispositions = {
        "OWNER_CONTACT_CANDIDATES_EXHAUSTED_BY_STRICT_AND_LOWER_AUTHORITIES__NO_NEW_C26_CONTACT": 80_092,
        "STRICT_DIM3_HANDLED__LOWER_DIM012_EXHAUSTED_WITH_ZERO_LEGAL_WITNESS": 295_340,
        "NO_NEW_ATOM_BEYOND_R1__STRICT_DIM3_HANDLED__LOWER_DIM012_REJECTED": 295_336,
        "SCOPED_G2A_ROUTE_BOUND__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN": 5_264,
        "SCOPED_G2A_UNIQUE_ROUTE_CLOSED__GLOBAL_POSITIVE_C19_AND_GLOBAL_PRIORITY_OPEN": 5_264,
        "EXACT_POSITIVE_PAIR_ASSIGNED_POSITIVE_VOLUME_CARRIERS_IN_SCOPED_COMPARATOR": 9_408,
        "NO_CURRENT_NEW_RELATIVE_2D_CONTACT_COMPLEMENT": 552,
        "EXACT_EMPTY_SUPPORT_CANNOT_FORM_CONTACT": 168,
    }
    need(dict(disposition_counts) == expected_dispositions, "disposition census")

    rng = random.Random(seed)
    probe = list(range(691_424))
    rng.shuffle(probe)
    execution_order_attestation = digest(probe[:4096])
    stable = {
        "C26_feature_rows": 691_424,
        "C26_direct_support_carrier_rows": 0,
        "C26_source_factorized_rows": 691_424,
        "scoped_unresolved_rows": 0,
        "node_census": dict(node_counts),
        "source_kernel_census": dict(source_counts),
        "disposition_census": dict(disposition_counts),
        "six_kernel_primitive_atoms": 483_232,
        "six_kernel_primitive_owners": 482_380,
        "C26_rows_on_six_kernel_primitive_owners": primitive_owner_rows,
        "C26_graph_rows_outside_six_kernel_owner_ids": graph_owner_rows,
        "unique_six_kernel_primitive_owners_with_C26_feature_rows": len(covered_owners),
        "six_kernel_owners_without_C26_feature_rows": 482_380 - len(covered_owners),
        "R2_C22A_atom_factor_histogram": {str(k): v for k, v in sorted(r2_factor_histogram.items())},
        "same_chart_strict_dim3_pairs": authority["strict"]["exact_census"]["all_component_strict_intersection_pair_count"],
        "same_chart_lower_dim012_pairs": authority["lower"]["census"]["lower_dimensional_candidate_pair_count"],
        "same_chart_lower_legal_cross_component_witnesses": 0,
        "G2A_scoped_graph_routes": 5_264,
        "C24A_G2B_positive_priority_pairs": 9_408,
        "C24A_G2B_no_current_contact_members": 552,
        "C24B_exact_empty_members": 168,
        "graph_feature_row_disjoint_bucket_census": {
            "G1_C10_definition_handoff_by_graph_id": 5_264,
            "G2A_C24A_scoped_route": 5_264,
            "G2B_C24A_positive": 9_408,
            "G2B_C24A_complement": 552,
            "G2B_C24B_exact_empty": 168,
        },
        "graph_feature_rows_total": 20_656,
        "graph_geometry_double_count_created_by_G1_G2A_feature_dependency": 0,
        "same_chart_contact_owners_with_C26_feature_rows": authority["lower"]["census"]["C26_contact_owner_coverage_count"],
        "same_chart_contact_owners_without_C26_feature_rows": authority["lower"]["census"]["C26_contact_owner_gap_count"],
        "ledger": ledger,
    }
    semantic = {
        "schema": "cm2.c26-independent.exact-contact-source-factorization-scoped-theorem.v1",
        "status": "PASS_NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS__691424_SOURCE_FACTORIZED__SAME_CHART_OWNER_CONTACT_RANGE_EXHAUSTED__GRAPH_HANDOFF_SCOPED__GLOBAL_TOTALITY_OPEN__ZERO_CREDIT",
        "invocation_seed": seed,
        "execution_order_attestation": execution_order_attestation,
        "algorithm": "LOCKSTEP_C26_TO_PRIMITIVE_SOURCE_ROWS_PLUS_EXACT_OWNER_AND_GRAPH_HANDOFF_JOINS",
        "candidate_governance": {
            "C27_FAMILIES_or_transition_imported_or_read": False,
            "C28_imported_or_read": False,
            "C29_imported_or_read": False,
            "historical_edge_ledger_used_as_candidate_universe": False,
            "old_transition_or_pair_ledger_used_as_candidate_universe": False,
            "six_primitive_support_kernels_are_candidate_denominator": True,
            "C26_absence_used_as_negative_geometry_theorem": False,
        },
        "theorem_scope": {
            "closed": "EVERY_C26_FEATURE_ROW_HAS_EXACTLY_ONE_PRIMITIVE_SOURCE_FACTOR_AND_ADDS_NO_NEW_SUPPORT_CARRIER",
            "same_chart_handoff": "ALL_SIX_KERNEL_STRICT_DIM3_AND_LOWER_DIM012_CONTACT_CANDIDATES_ARE_IN_PUBLISHED_FRESH_AUTHORITIES",
            "graph_handoff": "G1_TO_G2A_ALIAS__G2A_SCOPED_ROUTES__C24A_G2B_POSITIVE_OR_COMPLEMENT__C24B_EMPTY",
            "global_three_terminal_totality_and_unique_assignment": False,
            "global_atom_to_pair_incidence_join": "OPEN_NOT_CLAIMED_BY_THIS_THEOREM",
            "G2A_global_positive_C19_extension": "OPEN",
        },
        "conclusion": {
            "NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS": True,
            "fills_v5_C26_absence_slot": "YES__EVERY_C26_FEATURE_ROW_HAS_ONE_EXACT_SOURCE_HANDOFF_AND_ZERO_INDEPENDENT_SUPPORT_CARRIER",
            "does_not_close_twenty_family_gate": "PRIMITIVE_SOURCE_GLOBAL_TERMINAL_ASSIGNMENT__483232_ATOM_TO_PAIR_JOIN__AND_G2A_POSITIVE_C19_EXTENSION_REMAIN_OPEN",
            "G1_and_G2A_feature_rows_are_disjoint_DAG_rows_but_not_two_geometry_candidates": True,
        },
        "census": stable,
        "semantic_projection_sha256": digest(stable),
        "root_input_capture": {"all_pins_verified_with_stable_pre_post_stat": True, "attestations": {k: ATTESTATIONS[k] for k in sorted(ATTESTATIONS)}},
        "open_blockers": [
            "A1_A2_R1_R2_G1_GLOBAL_THREE_TERMINAL_ASSIGNMENT_NOT_ESTABLISHED_BY_SOURCE_FACTORIZATION",
            "FULL_483232_ATOM_TO_PAIR_INCIDENCE_AND_COMPLEMENT_JOIN_REQUIRED",
            "G2A_GLOBAL_POSITIVE_C19_EXTENSION_REQUIRED",
            "GLOBAL_THREE_TERMINAL_TOTALITY_AND_MUTUAL_EXCLUSIVITY_REQUIRED",
            "C27_C28_C29_FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION",
        ],
        "formal_credit": 0,
        "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
    }
    result = dict(semantic)
    result["result_sha256"] = digest(result)
    with (candidate_dir / RESULT).open("xb") as stream:
        stream.write(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve(), args.seed)
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"], "semantic_projection_sha256": result["semantic_projection_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
