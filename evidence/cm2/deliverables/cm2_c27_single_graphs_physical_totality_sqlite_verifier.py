#!/usr/bin/env python3
"""Independent SQLite rebuild for the SINGLE_GRAPHS zero-credit subgate.

This verifier does not import the stream producer.  It separately validates
the pinned primitive ledgers, builds normalized SQLite tables, proves the full
C24 terminal allocation by SQL grouping, materializes C15/C24/C25/C26 joins,
and compares every rebuilt SINGLE candidate byte-for-byte with the producer.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
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
EXPECTED_SINGLE_CLASSES = {"R235_SOURCE_EXACT_FACE_FULL_BASE": 552, "R235_TARGET_POSITIVE_PARTIAL_BASE": 4432}
EXPECTED_C24A_ALLOCATION = {
    "DOUBLE_GRAPHS": {"G2A": 16, "G2B": 16},
    "OUTGOING_GRAPHS": {"G2A": 264, "G2B": 528},
    "SINGLE_GRAPHS": {"G2A": 4984, "G2B": 9416},
}
EXPECTED_C24B_ALLOCATION = {"DOUBLE_GRAPHS": {"G2B": 16}, "OUTGOING_GRAPHS": {}, "SINGLE_GRAPHS": {"G2B": 152}}


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


def source_rows(name: str) -> Iterable[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for raw_line in stream:
            need(raw_line.endswith(b"\n"), "source newline:" + name)
            row = json.loads(raw_line[:-1])
            need(isinstance(row, dict), "source object:" + name)
            yield row


def row_closure(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), "source row closure:" + label)


def validate_pins() -> None:
    for name, expected in PINS.items():
        need(path_sha(ROOT / name) == expected, "source pin:" + name)


def create_database() -> sqlite3.Connection:
    validate_pins()
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
      CREATE TABLE graph(
        graph_id TEXT PRIMARY KEY, terminal TEXT NOT NULL, graph_class TEXT NOT NULL,
        sheet_member TEXT NOT NULL, ast_json TEXT NOT NULL, c10_sha TEXT NOT NULL,
        geometry_sha TEXT NOT NULL
      );
      CREATE TABLE relation(
        member_id TEXT PRIMARY KEY, graph_id TEXT NOT NULL, kernel TEXT NOT NULL,
        family TEXT NOT NULL, component TEXT NOT NULL, base_root TEXT NOT NULL,
        official_key TEXT NOT NULL, support_sha TEXT NOT NULL, theorem_sha TEXT NOT NULL,
        c24_sha TEXT NOT NULL, FOREIGN KEY(graph_id) REFERENCES graph(graph_id)
      );
      CREATE TABLE current15(
        member_id TEXT PRIMARY KEY, component TEXT NOT NULL, base_root TEXT NOT NULL,
        official_key TEXT NOT NULL, c15_sha TEXT NOT NULL
      );
      CREATE TABLE current25(
        member_id TEXT PRIMARY KEY, family TEXT NOT NULL, component TEXT NOT NULL,
        base_root TEXT NOT NULL, official_key TEXT NOT NULL, support_sha TEXT NOT NULL,
        semantic_kind TEXT NOT NULL, semantic_sha TEXT NOT NULL, kernel TEXT NOT NULL,
        kernel_row_sha TEXT NOT NULL, c15_binding_sha TEXT NOT NULL, c25_sha TEXT NOT NULL
      );
      CREATE TABLE feature(
        node TEXT NOT NULL, feature_id TEXT NOT NULL, obligation TEXT NOT NULL,
        owner TEXT NOT NULL, theorem_sha TEXT NOT NULL, kernel TEXT NOT NULL,
        source_sha TEXT NOT NULL, c26_sha TEXT NOT NULL,
        PRIMARY KEY(node,feature_id)
      );
    """)
    for row in source_rows(C10):
        row_closure(row, "C10")
        graph_id = row.get("graph_id")
        graph_class = row.get("graph_class")
        need(isinstance(graph_id, str) and graph_class in CLASS_TO_TERMINAL, "C10 classification")
        need(row.get("coordinate_parameter") == "TPS", "C10 coordinate")
        for name in ("base_domain_ast", "carrier_domain_ast", "equation_ast", "exact_support_ast"):
            need(row["ast_sha256"][name + "_sha256"] == digest(row[name]), "C10 AST:" + name)
        need(row["exact_support_ast"] == {"op": "AND", "args": [row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]]}, "C10 support composition")
        props = row["support_properties"]
        cert = row["monotone_graph_certificate"]
        need(props.get("R248_rectangle_used_as_support") is False, "C10 no rectangle promotion")
        need(props.get("connected") is True and props.get("nonempty") is True and props.get("one_graph_point_per_exact_base_point") is True, "C10 support geometry")
        need(cert.get("unique_t_for_every_exact_base_point") is True, "C10 unique graph")
        if graph_class == "R235_TARGET_POSITIVE_PARTIAL_BASE":
            topology = cert.get("face_p_topology_certificate", {})
            need(graph_id.startswith("round235-single-endpoint:"), "partial graph authority")
            need(props.get("s_independent_equation") is True, "partial s independence")
            need(cert.get("kind") == "STRICT_T_MONOTONE_IMPLICIT_GRAPH_OVER_CONNECTED_SIGN_STRADDLE_BASE", "partial monotone kind")
            need(topology.get("topology") in {"INTERNAL_P_BAND", "LOWER_P_ATTACHED", "UPPER_P_ATTACHED"}, "partial topology")
            cut_count = 2 if topology.get("topology") == "INTERNAL_P_BAND" else 1
            need(topology.get("connected_sign_straddle_p_interval") is True and topology.get("implicit_cut_root_count") == cut_count, "partial topology proof")
            need(len(topology.get("implicit_cut_root_descriptors", [])) == cut_count, "partial cut descriptors")
            need(topology.get("s_independence", {}).get("full_s_interval_retained") is True, "partial full s")
        elif graph_class == "R235_SOURCE_EXACT_FACE_FULL_BASE":
            need(graph_id.startswith("round235-single-endpoint:"), "exact-face graph authority")
            need(props.get("s_independent_equation") is True, "exact-face s independence")
            need(cert.get("kind") == "EXPLICIT_T_EQUALS_ZERO_FULL_BASE_GRAPH", "exact-face kind")
            need(cert.get("strict_t_derivative_exact") == {"denominator": 25, "numerator": 9}, "exact-face derivative")
        geometry = digest({
            "graph_id": graph_id,
            "graph_class": graph_class,
            "base_domain_ast": row["base_domain_ast"],
            "carrier_domain_ast": row["carrier_domain_ast"],
            "equation_ast": row["equation_ast"],
            "exact_support_ast": row["exact_support_ast"],
        })
        try:
            db.execute("INSERT INTO graph VALUES(?,?,?,?,?,?,?)", (
                graph_id, CLASS_TO_TERMINAL[graph_class], graph_class, row["sheet_member_id"],
                canonical(row["ast_sha256"]).decode("ascii"), row["row_sha256"], geometry,
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C10 graph") from exc
    root_partition = dict(db.execute("SELECT terminal,count(*) FROM graph GROUP BY terminal").fetchall())
    need(root_partition == EXPECTED_ROOT_PARTITION, "SQL root partition")
    single_classes = dict(db.execute("SELECT graph_class,count(*) FROM graph WHERE terminal='SINGLE_GRAPHS' GROUP BY graph_class").fetchall())
    need(single_classes == EXPECTED_SINGLE_CLASSES, "SQL single class partition")
    c24a_count = 0
    for row in source_rows(C24A):
        row_closure(row, "C24A")
        c24a_count += 1
        family = row.get("coarse_family")
        need(family in {"G2A", "G2B"}, "C24A family")
        expected_kind = "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY" if family == "G2A" else "G2B_RELATION_BACKED_SIDE_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
        need(row.get("row_kind") == expected_kind, "C24A row kind")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24A support closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24A theorem closure")
        graph_match = db.execute("SELECT graph_class,sheet_member FROM graph WHERE graph_id=?", (row["graph_id"],)).fetchone()
        need(graph_match is not None, "C24A graph belongs to C10 universe")
        if family == "G2A" and graph_match[0] == "R235_TARGET_POSITIVE_PARTIAL_BASE":
            need(row["member_id"] != graph_match[1], "partial graph uses fresh exact-partial sheet")
            need(row["semantic_theorem_ast"].get("support_kind") == "G2A_NEW_EXACT_PARTIAL_BASE_SHEET", "partial exact-sheet semantic kind")
        elif family == "G2A" and graph_match[0] == "R235_SOURCE_EXACT_FACE_FULL_BASE":
            need(row["member_id"] == graph_match[1], "exact-face existing sheet identity")
            need(row["semantic_theorem_ast"].get("support_kind") == "G2A_EXISTING_EXACT_BASE_SHEET", "exact-face existing-sheet semantic kind")
        try:
            db.execute("INSERT INTO relation VALUES(?,?,?,?,?,?,?,?,?,?)", (
                row["member_id"], row["graph_id"], "C24A", family, row["fresh_component_id"],
                row["base_root_id"], row["official_key_id"], row["normalized_support_ast_sha256"],
                row["semantic_theorem_ast_sha256"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("C24A graph/member allocation") from exc
    need(c24a_count == 15224, "C24A denominator")
    c24b_count = 0
    for row in source_rows(C24B):
        row_closure(row, "C24B")
        c24b_count += 1
        need(row.get("coarse_family") == "G2B", "C24B family")
        need(row.get("row_kind") == "G2B_NEGATIVE_NONINCIDENCE_EMPTY_MEMBER_AND_REPRESENTATION_SET_EQUALITY", "C24B kind")
        need(row.get("normalized_support_ast") == {"ambient_coordinates": ["t", "p", "s"], "coordinate_parameter": "TPS", "kind": "EMPTY_SET"}, "C24B exact empty support")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24B support closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24B theorem closure")
        theorem = row["semantic_theorem_ast"]
        need(theorem.get("strict_branch_intersection_with_complete_defining_carrier_is_empty") is True, "C24B empty intersection")
        need(theorem.get("sole_registered_representation_set_equals_empty_member_support") is True, "C24B representation empty")
        try:
            db.execute("INSERT INTO relation VALUES(?,?,?,?,?,?,?,?,?,?)", (
                row["member_id"], row["graph_id"], "C24B", "G2B", row["fresh_component_id"],
                row["base_root_id"], row["official_key_id"], row["normalized_support_ast_sha256"],
                row["semantic_theorem_ast_sha256"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("C24B graph/member allocation") from exc
    need(c24b_count == 168, "C24B denominator")
    allocation_a: dict[str, dict[str, int]] = {terminal: {} for terminal in EXPECTED_C24A_ALLOCATION}
    for terminal, family, count in db.execute("SELECT g.terminal,r.family,count(*) FROM relation r JOIN graph g USING(graph_id) WHERE r.kernel='C24A' GROUP BY g.terminal,r.family"):
        allocation_a[terminal][family] = count
    allocation_b: dict[str, dict[str, int]] = {terminal: {} for terminal in EXPECTED_C24B_ALLOCATION}
    for terminal, family, count in db.execute("SELECT g.terminal,r.family,count(*) FROM relation r JOIN graph g USING(graph_id) WHERE r.kernel='C24B' GROUP BY g.terminal,r.family"):
        allocation_b[terminal][family] = count
    need(allocation_a == EXPECTED_C24A_ALLOCATION, "SQL C24A allocation")
    need(allocation_b == EXPECTED_C24B_ALLOCATION, "SQL C24B allocation")
    need(not db.execute("""
      SELECT g.graph_id FROM graph g JOIN relation r ON r.graph_id=g.graph_id
      WHERE g.terminal='SINGLE_GRAPHS' GROUP BY g.graph_id
      HAVING sum(r.kernel='C24A' AND r.family='G2A')<>1
         OR sum(r.kernel='C24A' AND r.family='G2B') NOT IN (1,2)
         OR sum(r.kernel='C24B') NOT IN (0,1)
    """).fetchall(), "SQL single per-root shape")
    pattern = db.execute("""
      SELECT g.graph_class,
             sum(r.kernel='C24A' AND r.family='G2A') AS a,
             sum(r.kernel='C24A' AND r.family='G2B') AS b,
             sum(r.kernel='C24B') AS e,
             count(*)
      FROM graph g JOIN relation r ON r.graph_id=g.graph_id
      WHERE g.terminal='SINGLE_GRAPHS'
      GROUP BY g.graph_id
    """).fetchall()
    pattern_counter = Counter((row[0], row[1], row[2], row[3]) for row in pattern)
    need(pattern_counter == Counter({
        ("R235_TARGET_POSITIVE_PARTIAL_BASE", 1, 2, 0): 4432,
        ("R235_SOURCE_EXACT_FACE_FULL_BASE", 1, 1, 0): 400,
        ("R235_SOURCE_EXACT_FACE_FULL_BASE", 1, 1, 1): 152,
    }), "SQL exact per-root kernel patterns")
    need(not db.execute("""
      SELECT g.graph_id FROM graph g JOIN relation r ON r.graph_id=g.graph_id
      WHERE g.terminal='SINGLE_GRAPHS' AND r.kernel='C24A' AND r.family='G2A'
        AND (r.support_sha<>json_extract(g.ast_json,'$.base_domain_ast_sha256')
          OR (g.graph_class='R235_TARGET_POSITIVE_PARTIAL_BASE' AND r.member_id=g.sheet_member)
          OR (g.graph_class='R235_SOURCE_EXACT_FACE_FULL_BASE' AND r.member_id<>g.sheet_member))
    """).fetchall(), "SQL exact-sheet identity/base allocation")
    selected_members = {row[0] for row in db.execute("SELECT r.member_id FROM relation r JOIN graph g USING(graph_id) WHERE g.terminal='SINGLE_GRAPHS'")}
    need(len(selected_members) == 14552, "SQL selected member denominator")
    for row in source_rows(C15):
        member_id = row.get("registry_member_id")
        if member_id not in selected_members:
            continue
        row_closure(row, "C15")
        try:
            db.execute("INSERT INTO current15 VALUES(?,?,?,?,?)", (member_id, row["fresh_component_id"], row["base_root_id"], row["official_key_id"], row["row_sha256"]))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C15 selected") from exc
    for row in source_rows(C25):
        member_id = row.get("member_id")
        if member_id not in selected_members:
            continue
        row_closure(row, "C25")
        bindings = row["source_bindings"]
        try:
            db.execute("INSERT INTO current25 VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
                member_id, row["coarse_family"], row["fresh_component_id"], row["base_root_id"],
                row["official_key_id"], row["normalized_support_ast_sha256"], row["support_semantic_kind"],
                row["support_semantic_certificate_sha256"], bindings["support_kernel"],
                bindings["support_kernel_row_sha256"], bindings["C15_member_row_sha256"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C25 selected") from exc
    need(db.execute("SELECT count(*) FROM current15").fetchone()[0] == 14552, "SQL C15 cover")
    need(db.execute("SELECT count(*) FROM current25").fetchone()[0] == 14552, "SQL C25 cover")
    single_graphs = {row[0] for row in db.execute("SELECT graph_id FROM graph WHERE terminal='SINGLE_GRAPHS'")}
    for row in source_rows(C26):
        node = row.get("node_id")
        feature_id = row.get("feature_id")
        chosen = (node == "G1" and feature_id in single_graphs) or (node in {"G2A", "G2B"} and feature_id in selected_members)
        if not chosen:
            continue
        row_closure(row, "C26")
        bindings = row["source_bindings"]
        try:
            db.execute("INSERT INTO feature VALUES(?,?,?,?,?,?,?,?)", (
                node, feature_id, row["obligation_kind"], row["owner_member_id"],
                row["definition_or_dependency_theorem_ast_sha256"], bindings["source_kernel"],
                bindings["source_row_sha256"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C26 selected") from exc
    need(db.execute("SELECT count(*) FROM feature WHERE node='G1'").fetchone()[0] == 4984, "SQL G1 cover")
    need(db.execute("SELECT count(*) FROM feature WHERE node IN ('G2A','G2B')").fetchone()[0] == 14552, "SQL G2 cover")
    db.commit()
    return db


def validate_materialized_joins(db: sqlite3.Connection) -> None:
    gaps = db.execute("""
      SELECT r.member_id FROM relation r JOIN graph g ON g.graph_id=r.graph_id
      LEFT JOIN current15 a ON a.member_id=r.member_id
      LEFT JOIN current25 b ON b.member_id=r.member_id
      LEFT JOIN feature f ON f.node=r.family AND f.feature_id=r.member_id
      WHERE g.terminal='SINGLE_GRAPHS' AND (
        a.member_id IS NULL OR b.member_id IS NULL OR f.feature_id IS NULL
        OR a.component<>r.component OR a.component<>b.component
        OR a.base_root<>r.base_root OR a.base_root<>b.base_root
        OR a.official_key<>r.official_key OR a.official_key<>b.official_key
        OR b.family<>r.family OR b.support_sha<>r.support_sha OR b.semantic_sha<>r.theorem_sha
        OR b.kernel<>r.kernel OR b.kernel_row_sha<>r.c24_sha OR b.c15_binding_sha<>a.c15_sha
        OR b.semantic_kind<>(CASE r.kernel WHEN 'C24A' THEN 'RELATION_BACKED_MEMBER_SUPPORT_EQUALITY' ELSE 'EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY' END)
        OR f.owner<>r.member_id OR f.theorem_sha<>r.theorem_sha OR f.kernel<>r.kernel OR f.source_sha<>r.c24_sha
        OR f.obligation<>(CASE WHEN r.family='G2A' THEN 'G2A_GRAPH_TO_SHEET_IDENTIFICATION'
                               WHEN r.kernel='C24A' THEN 'G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE'
                               ELSE 'G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE' END)
      )
    """).fetchall()
    need(not gaps, "SQL materialized C15/C24/C25/C26 joins")
    for graph_id, sheet_member, ast_json, c10_sha, obligation, owner, theorem, kernel, source_sha in db.execute("""
      SELECT g.graph_id,g.sheet_member,g.ast_json,g.c10_sha,f.obligation,f.owner,f.theorem_sha,f.kernel,f.source_sha
      FROM graph g LEFT JOIN feature f ON f.node='G1' AND f.feature_id=g.graph_id
      WHERE g.terminal='SINGLE_GRAPHS'
    """):
        need(obligation == "G1_EXACT_GRAPH_DEFINITION", "SQL G1 obligation")
        need(owner == sheet_member and theorem == digest(json.loads(ast_json)), "SQL G1 owner/AST")
        need(kernel == "C10" and source_sha == c10_sha, "SQL G1 source binding")


def reconstruct_sqlite() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    db = create_database()
    try:
        validate_materialized_joins(db)
        output: list[dict[str, Any]] = []
        graph_rows = db.execute("""
          SELECT g.graph_id,g.graph_class,g.ast_json,g.c10_sha,g.geometry_sha,f.c26_sha
          FROM graph g JOIN feature f ON f.node='G1' AND f.feature_id=g.graph_id
          WHERE g.terminal='SINGLE_GRAPHS' ORDER BY g.graph_id
        """).fetchall()
        for graph_id, graph_class, ast_json, c10_sha, geometry_sha, g1_sha in graph_rows:
            ast_sha = json.loads(ast_json)
            dispositions: list[dict[str, Any]] = []
            for kernel, family, member_id, component, base_root, official_key, support_sha, theorem_sha, c15_sha, c24_sha, c25_sha, c26_sha in db.execute("""
              SELECT r.kernel,r.family,r.member_id,a.component,a.base_root,a.official_key,r.support_sha,r.theorem_sha,
                     a.c15_sha,r.c24_sha,b.c25_sha,f.c26_sha
              FROM relation r JOIN current15 a ON a.member_id=r.member_id
              JOIN current25 b ON b.member_id=r.member_id
              JOIN feature f ON f.node=r.family AND f.feature_id=r.member_id
              WHERE r.graph_id=?
              ORDER BY CASE WHEN r.family='G2A' THEN 0 WHEN r.kernel='C24A' THEN 1 ELSE 2 END,r.member_id
            """, (graph_id,)):
                role = "G2A_SHEET" if family == "G2A" else "G2B_POSITIVE_SIDE" if kernel == "C24A" else "G2B_EXACT_EMPTY_SIDE"
                dispositions.append({
                    "role": role,
                    "support_kernel": kernel,
                    "member_id": member_id,
                    "fresh_component_id": component,
                    "base_root_id": base_root,
                    "official_key_id": official_key,
                    "normalized_support_ast_sha256": support_sha,
                    "semantic_theorem_ast_sha256": theorem_sha,
                    "C15_row_sha256": c15_sha,
                    "C24_row_sha256": c24_sha,
                    "C25_row_sha256": c25_sha,
                    "C26_row_sha256": c26_sha,
                })
            census = Counter(row["role"] for row in dispositions)
            need(census["G2A_SHEET"] == 1 and census["G2B_POSITIVE_SIDE"] in {1, 2} and census["G2B_EXACT_EMPTY_SIDE"] in {0, 1}, "SQL output disposition shape")
            body = {
                "schema": SCHEMA + ".candidate-row.v1",
                "terminal": "SINGLE_GRAPHS",
                "graph_id": graph_id,
                "graph_class": graph_class,
                "geometry_root_sha256": geometry_sha,
                "base_domain_ast_sha256": ast_sha["base_domain_ast_sha256"],
                "carrier_domain_ast_sha256": ast_sha["carrier_domain_ast_sha256"],
                "equation_ast_sha256": ast_sha["equation_ast_sha256"],
                "exact_support_ast_sha256": ast_sha["exact_support_ast_sha256"],
                "C10_row_sha256": c10_sha,
                "C26_G1_row_sha256": g1_sha,
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
        need(len(output) == 4984, "SQL output candidate count")
        allocation_a = {terminal: {} for terminal in EXPECTED_C24A_ALLOCATION}
        for terminal, family, count in db.execute("SELECT g.terminal,r.family,count(*) FROM relation r JOIN graph g USING(graph_id) WHERE r.kernel='C24A' GROUP BY g.terminal,r.family"):
            allocation_a[terminal][family] = count
        allocation_b = {terminal: {} for terminal in EXPECTED_C24B_ALLOCATION}
        for terminal, family, count in db.execute("SELECT g.terminal,r.family,count(*) FROM relation r JOIN graph g USING(graph_id) WHERE r.kernel='C24B' GROUP BY g.terminal,r.family"):
            allocation_b[terminal][family] = count
        pattern_rows = db.execute("""
          SELECT graph_class,a,b,e,count(*) FROM (
            SELECT g.graph_id,g.graph_class,
                   sum(r.kernel='C24A' AND r.family='G2A') AS a,
                   sum(r.kernel='C24A' AND r.family='G2B') AS b,
                   sum(r.kernel='C24B') AS e
            FROM graph g JOIN relation r ON r.graph_id=g.graph_id
            WHERE g.terminal='SINGLE_GRAPHS' GROUP BY g.graph_id
          ) GROUP BY graph_class,a,b,e ORDER BY graph_class,a,b,e
        """).fetchall()
        pattern_json = [{"graph_class": row[0], "G2A_positive": row[1], "G2B_positive": row[2], "G2B_exact_empty": row[3], "root_count": row[4]} for row in pattern_rows]
        root_partition = dict(db.execute("SELECT terminal,count(*) FROM graph GROUP BY terminal").fetchall())
        single_classes = dict(db.execute("SELECT graph_class,count(*) FROM graph WHERE terminal='SINGLE_GRAPHS' GROUP BY graph_class").fetchall())
        result_body = {
            "schema": SCHEMA + ".result.v1",
            "status": "PASS_ZERO_CREDIT__SINGLE_GRAPHS_4984_ROOTS_4984_SHEETS_9416_POSITIVE_SIDES_152_EXACT_EMPTY_SIDES",
            "implementation_neutral_semantics": "STREAM_OR_SQLITE_MUST_REBUILD_IDENTICAL_MATERIALIZED_PROOF_ROWS",
            "candidate_universe": "C10_GRAPH_CLASS_AND_EXACT_GEOMETRY_BEFORE_C24A_C24B_C25_C26_JOINS",
            "C10_terminal_partition": root_partition,
            "single_graph_class_partition": single_classes,
            "C24_full_terminal_allocation": {"C24A": allocation_a, "C24B": allocation_b},
            "single_per_root_kernel_patterns": pattern_json,
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
            "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        }
        return output, {**result_body, "result_sha256": digest(result_body)}
    finally:
        db.close()


def read_candidate(candidate_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    supplied: list[dict[str, Any]] = []
    with gzip.open(candidate_dir / "ledger.jsonl.gz", "rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "candidate newline")
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "candidate canonical row")
            supplied.append(row)
    raw_result = (candidate_dir / "result.json").read_bytes()
    result = json.loads(raw_result)
    need(canonical(result) == raw_result, "candidate canonical result")
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    need(claimed == digest(body), "candidate result closure")
    manifest = json.loads((candidate_dir / "manifest.json").read_bytes())
    need(manifest == {"ledger.jsonl.gz": path_sha(candidate_dir / "ledger.jsonl.gz"), "result.json": path_sha(candidate_dir / "result.json")}, "candidate manifest")
    return supplied, result


def validate_candidate_rows(candidate: list[dict[str, Any]], reference: list[dict[str, Any]]) -> None:
    need(len(candidate) == len(reference) == 4984, "candidate/reference count")
    need([row.get("graph_id") for row in candidate] == sorted(row.get("graph_id") for row in candidate), "candidate order")
    need(len({row.get("graph_id") for row in candidate}) == 4984, "candidate unique roots")
    for row in candidate:
        body = dict(row)
        claimed = body.pop("candidate_digest", None)
        need(isinstance(claimed, str) and claimed == digest(body), "candidate row closure")
        roles = Counter(item.get("role") for item in row.get("dispositions", []))
        need(roles["G2A_SHEET"] == 1 and roles["G2B_POSITIVE_SIDE"] in {1, 2} and roles["G2B_EXACT_EMPTY_SIDE"] in {0, 1}, "candidate role shape")
    for supplied, rebuilt in zip(candidate, reference):
        need(supplied.get("graph_id") == rebuilt["graph_id"], "candidate identity")
        need(supplied.get("candidate_digest") == rebuilt["candidate_digest"], "candidate digest")
        need(canonical(supplied) == canonical(rebuilt), "candidate exact semantics")


def verify(candidate_dir: Path) -> dict[str, Any]:
    reference_rows, reference_result = reconstruct_sqlite()
    supplied_rows, supplied_result = read_candidate(candidate_dir)
    validate_candidate_rows(supplied_rows, reference_rows)
    need(canonical(supplied_result) == canonical(reference_result), "stream/SQLite result exact")
    body = {
        "schema": SCHEMA + ".sqlite-independent-verification.v1",
        "status": "PASS_SQLITE_INDEPENDENT_REBUILD__4984_CANDIDATES_AND_14552_PROOF_ROWS_EXACT_IDENTICAL__ZERO_CREDIT",
        "candidate_count": 4984,
        "materialized_disposition_count": 14552,
        "G2A_count": 4984,
        "G2B_positive_count": 9416,
        "G2B_exact_empty_count": 152,
        "per_candidate_digest_mismatch_count": 0,
        "stream_result_sha256": supplied_result["result_sha256"],
        "sqlite_result_sha256": reference_result["result_sha256"],
        "ordered_candidate_digests_sha256": reference_result["ordered_candidate_digests_sha256"],
        "legacy_transition_family_table_used": False,
        "historical_edge_ledger_used": False,
        "formal_credit": 0,
        "unconditional_C27_C28_C29": "REJECT_REMAINS_PENDING_FULL_TWENTY_TERMINAL_GATE",
    }
    return {**body, "verification_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-tag", required=True)
    parser.add_argument("--seed", required=True)
    args = parser.parse_args()
    need(args.seed.isdigit(), "numeric seed")
    target = AUDIT / args.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    result = verify(Path(args.candidate_dir).resolve())
    target.mkdir(mode=0o700)
    (target / "verification.json").write_bytes(canonical(result))
    print(canonical({"status": result["status"], "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
