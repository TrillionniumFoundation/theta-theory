#!/usr/bin/env python3
"""Independent SQLite verifier for the OUTGOING_GRAPHS zero-credit gate.

This file does not import the stream probe.  It independently parses the
pinned primitive ledgers, materializes relational tables, performs SQL joins,
and reconstructs every candidate digest before inspecting candidate output.
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
SCHEMA = "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1"
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
    "R242_UNIQUE_GRAPH_FULL_PATCH": "OUTGOING",
    "R235_TARGET_POSITIVE_PARTIAL_BASE": "SINGLE",
    "R235_SOURCE_EXACT_FACE_FULL_BASE": "SINGLE",
    "R235D_SOURCE_EXACT_FACE_FULL_BASE": "DOUBLE",
}
EXPECTED_PARTITION = {"OUTGOING": 264, "SINGLE": 4984, "DOUBLE": 16}


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
        for line in stream:
            need(line.endswith(b"\n"), "source newline:" + name)
            row = json.loads(line[:-1])
            need(isinstance(row, dict), "source row object:" + name)
            yield row


def row_closure(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(isinstance(claimed, str) and claimed == digest(body), "source row closure:" + label)


def validate_pins() -> None:
    for name, claimed in PINS.items():
        need(path_sha(ROOT / name) == claimed, "source pin:" + name)


def qjson(value: Any) -> str:
    return canonical(value).decode("ascii")


def build_database() -> tuple[sqlite3.Connection, dict[str, int]]:
    validate_pins()
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
      CREATE TABLE graph(
        graph_id TEXT PRIMARY KEY, terminal TEXT NOT NULL, graph_class TEXT NOT NULL,
        sheet_member_id TEXT NOT NULL, c10_sha TEXT NOT NULL, ast_json TEXT NOT NULL,
        geometry_sha TEXT NOT NULL
      );
      CREATE TABLE relation(
        member_id TEXT PRIMARY KEY, graph_id TEXT NOT NULL, family TEXT NOT NULL,
        base_root TEXT NOT NULL, support_sha TEXT NOT NULL, theorem_sha TEXT NOT NULL,
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
        for field in ("base_domain_ast", "carrier_domain_ast", "equation_ast", "exact_support_ast"):
            need(row["ast_sha256"][field + "_sha256"] == digest(row[field]), "C10 AST closure:" + field)
        need(row["exact_support_ast"].get("op") == "AND" and row["exact_support_ast"].get("args") == [row["carrier_domain_ast"], row["base_domain_ast"], row["equation_ast"]], "C10 exact support composition")
        terminal = CLASS_TO_TERMINAL[graph_class]
        if terminal == "OUTGOING":
            need(graph_id.startswith("round242-positive-2d-transition-sheet-patch:"), "outgoing graph authority")
            need(row["coordinate_parameter"] == "TPS", "outgoing TPS")
            cert = row["monotone_graph_certificate"]
            need(cert.get("kind") == "SEALED_R242_STRICT_T_MONOTONE_UNIQUE_FULL_PATCH_GRAPH", "outgoing monotone kind")
            need(cert.get("unique_t_for_every_exact_base_point") is True, "outgoing monotone totality")
            orientation = (cert.get("lower_t_face_F_sign"), cert.get("strict_t_derivative_sign"), cert.get("upper_t_face_F_sign"))
            need(orientation in {
                ("STRICT_NEGATIVE", "STRICT_POSITIVE", "STRICT_POSITIVE"),
                ("STRICT_POSITIVE", "STRICT_NEGATIVE", "STRICT_NEGATIVE"),
            }, "outgoing monotone orientation")
            props = row["support_properties"]
            need(props.get("nonempty") is True and props.get("connected") is True and props.get("one_graph_point_per_exact_base_point") is True, "outgoing support properties")
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
                graph_id, terminal, graph_class, row["sheet_member_id"], row["row_sha256"],
                qjson(row["ast_sha256"]), geometry,
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C10 graph") from exc
    partition = dict(db.execute("SELECT terminal,count(*) FROM graph GROUP BY terminal").fetchall())
    need(partition == EXPECTED_PARTITION and sum(partition.values()) == 5264, "SQL C10 partition")
    outgoing = {row[0] for row in db.execute("SELECT graph_id FROM graph WHERE terminal='OUTGOING'")}
    for row in source_rows(C24A):
        if row.get("graph_id") not in outgoing:
            continue
        row_closure(row, "C24A")
        family = row.get("coarse_family")
        need(family in {"G2A", "G2B"}, "C24A family")
        kind = "G2A_GRAPH_TO_SHEET_MEMBER_AND_REPRESENTATION_SET_EQUALITY" if family == "G2A" else "G2B_RELATION_BACKED_SIDE_MEMBER_AND_REPRESENTATION_SET_EQUALITY"
        need(row.get("row_kind") == kind, "C24A row kind")
        need(row["normalized_support_ast_sha256"] == digest(row["normalized_support_ast"]), "C24A support closure")
        need(row["semantic_theorem_ast_sha256"] == digest(row["semantic_theorem_ast"]), "C24A theorem closure")
        try:
            db.execute("INSERT INTO relation VALUES(?,?,?,?,?,?,?)", (
                row["member_id"], row["graph_id"], family, row["base_root_id"],
                row["normalized_support_ast_sha256"], row["semantic_theorem_ast_sha256"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate outgoing relation member") from exc
    for row in source_rows(C24B):
        need(row.get("graph_id") not in outgoing, "outgoing root appears in C24B")
    need(db.execute("SELECT count(*) FROM relation").fetchone()[0] == 792, "SQL relation denominator")
    bad_groups = db.execute("""
      SELECT graph_id FROM relation GROUP BY graph_id
      HAVING count(*)<>3 OR sum(family='G2A')<>1 OR sum(family='G2B')<>2 OR count(DISTINCT base_root)<>1
    """).fetchall()
    need(not bad_groups, "SQL one-sheet-two-side grouping")
    need(db.execute("SELECT count(DISTINCT graph_id) FROM relation").fetchone()[0] == 264, "SQL root coverage")
    need(not db.execute("""
      SELECT g.graph_id FROM graph g JOIN relation r ON r.graph_id=g.graph_id
      WHERE g.terminal='OUTGOING' AND r.family='G2A' AND r.member_id<>g.sheet_member_id
    """).fetchall(), "SQL sheet identity")
    need(not db.execute("""
      SELECT g.graph_id FROM graph g JOIN relation r ON r.graph_id=g.graph_id
      WHERE g.terminal='OUTGOING' AND r.family='G2A'
        AND r.support_sha<>json_extract(g.ast_json,'$.base_domain_ast_sha256')
    """).fetchall(), "SQL sheet/base support")
    member_ids = {row[0] for row in db.execute("SELECT member_id FROM relation")}
    for row in source_rows(C15):
        member_id = row.get("registry_member_id")
        if member_id not in member_ids:
            continue
        row_closure(row, "C15")
        try:
            db.execute("INSERT INTO current15 VALUES(?,?,?,?,?)", (
                member_id, row["fresh_component_id"], row["base_root_id"], row["official_key_id"], row["row_sha256"],
            ))
        except sqlite3.IntegrityError as exc:
            raise Failure("duplicate C15 selected member") from exc
    for row in source_rows(C25):
        member_id = row.get("member_id")
        if member_id not in member_ids:
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
            raise Failure("duplicate C25 selected member") from exc
    need(db.execute("SELECT count(*) FROM current15").fetchone()[0] == 792, "SQL C15 cover")
    need(db.execute("SELECT count(*) FROM current25").fetchone()[0] == 792, "SQL C25 cover")
    for row in source_rows(C26):
        node = row.get("node_id")
        feature_id = row.get("feature_id")
        selected = (node == "G1" and feature_id in outgoing) or (node in {"G2A", "G2B"} and feature_id in member_ids)
        if not selected:
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
            raise Failure("duplicate C26 selected feature") from exc
    need(db.execute("SELECT count(*) FROM feature WHERE node='G1'").fetchone()[0] == 264, "SQL G1 cover")
    need(db.execute("SELECT count(*) FROM feature WHERE node IN ('G2A','G2B')").fetchone()[0] == 792, "SQL G2 cover")
    db.commit()
    return db, partition


def validate_joins(db: sqlite3.Connection) -> None:
    gaps = db.execute("""
      SELECT r.member_id FROM relation r
      LEFT JOIN current15 a ON a.member_id=r.member_id
      LEFT JOIN current25 b ON b.member_id=r.member_id
      LEFT JOIN feature f ON f.node=r.family AND f.feature_id=r.member_id
      WHERE a.member_id IS NULL OR b.member_id IS NULL OR f.feature_id IS NULL
        OR a.component<>b.component OR a.base_root<>b.base_root OR a.official_key<>b.official_key
        OR r.base_root<>a.base_root OR r.family<>b.family OR r.support_sha<>b.support_sha
        OR b.semantic_kind<>'RELATION_BACKED_MEMBER_SUPPORT_EQUALITY' OR b.semantic_sha<>r.theorem_sha
        OR b.kernel<>'C24A' OR b.kernel_row_sha<>r.c24_sha OR b.c15_binding_sha<>a.c15_sha
        OR f.owner<>r.member_id OR f.theorem_sha<>r.theorem_sha OR f.kernel<>'C24A' OR f.source_sha<>r.c24_sha
        OR f.obligation<>(CASE WHEN r.family='G2A' THEN 'G2A_GRAPH_TO_SHEET_IDENTIFICATION' ELSE 'G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE' END)
    """).fetchall()
    need(not gaps, "SQL C15/C24/C25/C26 disposition joins")
    root_gaps = db.execute("""
      SELECT g.graph_id FROM graph g
      LEFT JOIN feature f ON f.node='G1' AND f.feature_id=g.graph_id
      WHERE g.terminal='OUTGOING' AND (
        f.feature_id IS NULL OR f.obligation<>'G1_EXACT_GRAPH_DEFINITION' OR f.owner<>g.sheet_member_id
        OR f.theorem_sha<>lower(hex(sha256(g.ast_json))) OR f.kernel<>'C10' OR f.source_sha<>g.c10_sha
      )
    """).fetchall() if False else []
    # sqlite has no built-in SHA-256; perform the small 264-row G1 hash check here.
    for graph_id, sheet, c10_sha, ast_json, theorem, owner, kernel, source_sha, obligation in db.execute("""
      SELECT g.graph_id,g.sheet_member_id,g.c10_sha,g.ast_json,
             f.theorem_sha,f.owner,f.kernel,f.source_sha,f.obligation
      FROM graph g LEFT JOIN feature f ON f.node='G1' AND f.feature_id=g.graph_id
      WHERE g.terminal='OUTGOING'
    """):
        need(obligation == "G1_EXACT_GRAPH_DEFINITION", "SQL G1 obligation")
        need(owner == sheet and theorem == digest(json.loads(ast_json)), "SQL G1 owner/AST")
        need(kernel == "C10" and source_sha == c10_sha, "SQL G1 source binding")
    for graph_id, groups, components, roots, keys in db.execute("""
      SELECT r.graph_id,count(*),count(DISTINCT a.component),count(DISTINCT a.base_root),count(DISTINCT a.official_key)
      FROM relation r JOIN current15 a ON a.member_id=r.member_id GROUP BY r.graph_id
    """):
        need(groups == 3 and components == roots == keys == 1, "SQL shared physical ownership:" + graph_id)


def reconstruct_sqlite() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    db, partition = build_database()
    try:
        validate_joins(db)
        output: list[dict[str, Any]] = []
        graphs = db.execute("""
          SELECT graph_id,graph_class,c10_sha,ast_json,geometry_sha FROM graph
          WHERE terminal='OUTGOING' ORDER BY graph_id
        """).fetchall()
        for graph_id, graph_class, c10_sha, ast_json, geometry_sha in graphs:
            ast_sha = json.loads(ast_json)
            g1 = db.execute("SELECT c26_sha FROM feature WHERE node='G1' AND feature_id=?", (graph_id,)).fetchone()
            need(g1 is not None, "SQL output G1")
            dispositions: list[dict[str, Any]] = []
            records = db.execute("""
              SELECT r.family,r.member_id,a.component,a.base_root,a.official_key,r.support_sha,r.theorem_sha,
                     a.c15_sha,r.c24_sha,b.c25_sha,f.c26_sha
              FROM relation r JOIN current15 a ON a.member_id=r.member_id
              JOIN current25 b ON b.member_id=r.member_id
              JOIN feature f ON f.node=r.family AND f.feature_id=r.member_id
              WHERE r.graph_id=? ORDER BY CASE r.family WHEN 'G2A' THEN 0 ELSE 1 END,r.member_id
            """, (graph_id,)).fetchall()
            for family, member, component, base_root, official_key, support_sha, theorem_sha, c15_sha, c24_sha, c25_sha, c26_sha in records:
                dispositions.append({
                    "role": "G2A_SHEET" if family == "G2A" else "G2B_SIDE",
                    "member_id": member,
                    "fresh_component_id": component,
                    "base_root_id": base_root,
                    "official_key_id": official_key,
                    "normalized_support_ast_sha256": support_sha,
                    "semantic_theorem_ast_sha256": theorem_sha,
                    "C15_row_sha256": c15_sha,
                    "C24A_row_sha256": c24_sha,
                    "C25_row_sha256": c25_sha,
                    "C26_row_sha256": c26_sha,
                })
            body = {
                "schema": SCHEMA + ".candidate-row.v1",
                "terminal": "OUTGOING_GRAPHS",
                "graph_id": graph_id,
                "graph_class": graph_class,
                "geometry_root_sha256": geometry_sha,
                "base_domain_ast_sha256": ast_sha["base_domain_ast_sha256"],
                "carrier_domain_ast_sha256": ast_sha["carrier_domain_ast_sha256"],
                "equation_ast_sha256": ast_sha["equation_ast_sha256"],
                "exact_support_ast_sha256": ast_sha["exact_support_ast_sha256"],
                "C10_row_sha256": c10_sha,
                "C26_G1_row_sha256": g1[0],
                "dispositions": dispositions,
                "physical_totality_certificate": {
                    "root_generated_before_C24_C26_join": True,
                    "exactly_one_G2A_sheet": True,
                    "exactly_two_G2B_sides": True,
                    "C24B_negative_dispositions": 0,
                    "all_G2A_G2B_C26_obligations_joined": True,
                    "current_C15_C25_component_base_root_official_key_agree": True,
                    "unresolved": 0,
                },
                "formal_credit": 0,
            }
            output.append({**body, "candidate_digest": digest(body)})
        need(len(output) == 264, "SQL output count")
        result_body = {
            "schema": SCHEMA + ".result.v1",
            "status": "PASS_ZERO_CREDIT__OUTGOING_GRAPHS_264_ROOTS_264_G2A_528_G2B_PHYSICAL_TOTALITY",
            "implementation_neutral_semantics": "STREAM_OR_SQLITE_MUST_REBUILD_IDENTICAL_CANDIDATE_DIGESTS",
            "candidate_universe": "C10_GRAPH_CLASS_BASE_AST_EQUATION_AST__NOT_C27_FAMILIES_OR_EDGE_LEDGER",
            "C10_actual_G1_partition": partition,
            "outgoing_root_count": len(output),
            "G2A_sheet_disposition_count": sum(row["role"] == "G2A_SHEET" for item in output for row in item["dispositions"]),
            "G2B_side_disposition_count": sum(row["role"] == "G2B_SIDE" for item in output for row in item["dispositions"]),
            "C24B_negative_disposition_count": 0,
            "unresolved_count": 0,
            "duplicate_or_orphan_count": 0,
            "ordered_candidate_digests_sha256": digest([row["candidate_digest"] for row in output]),
            "input_pins": [{"filename": name, "sha256": PINS[name]} for name in sorted(PINS)],
            "C27_FAMILIES_imported_or_read": False,
            "edge_ledger_used_as_candidate_universe": False,
            "formal_credit": 0,
            "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        }
        return output, {**result_body, "result_sha256": digest(result_body)}
    finally:
        db.close()


def validate_candidate_rows(candidate: list[dict[str, Any]], reference: list[dict[str, Any]]) -> None:
    need(len(candidate) == len(reference) == 264, "candidate/reference count")
    need([row.get("graph_id") for row in candidate] == sorted(row.get("graph_id") for row in candidate), "candidate order")
    need(len({row.get("graph_id") for row in candidate}) == 264, "candidate unique ids")
    for row in candidate:
        body = dict(row)
        claimed = body.pop("candidate_digest", None)
        need(isinstance(claimed, str) and claimed == digest(body), "candidate row closure")
        need(Counter(item.get("role") for item in row.get("dispositions", [])) == {"G2A_SHEET": 1, "G2B_SIDE": 2}, "candidate disposition shape")
    for supplied, rebuilt in zip(candidate, reference):
        need(supplied.get("graph_id") == rebuilt["graph_id"], "per-candidate identity")
        need(supplied.get("candidate_digest") == rebuilt["candidate_digest"], "per-candidate digest")
        need(canonical(supplied) == canonical(rebuilt), "per-candidate exact semantics")


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
    need(manifest == {
        "ledger.jsonl.gz": path_sha(candidate_dir / "ledger.jsonl.gz"),
        "result.json": path_sha(candidate_dir / "result.json"),
    }, "candidate manifest")
    return supplied, result


def verify(candidate_dir: Path) -> dict[str, Any]:
    reference_rows, reference_result = reconstruct_sqlite()
    supplied_rows, supplied_result = read_candidate(candidate_dir)
    validate_candidate_rows(supplied_rows, reference_rows)
    need(canonical(supplied_result) == canonical(reference_result), "stream/SQLite result exact")
    body = {
        "schema": SCHEMA + ".sqlite-independent-verification.v1",
        "status": "PASS_SQLITE_INDEPENDENT_REBUILD__264_PER_CANDIDATE_DIGESTS_EXACT_IDENTICAL__ZERO_CREDIT",
        "candidate_count": 264,
        "G2A_count": 264,
        "G2B_count": 528,
        "per_candidate_digest_mismatch_count": 0,
        "stream_result_sha256": supplied_result["result_sha256"],
        "sqlite_result_sha256": reference_result["result_sha256"],
        "ordered_candidate_digests_sha256": reference_result["ordered_candidate_digests_sha256"],
        "C27_FAMILIES_imported_or_read": False,
        "edge_ledger_used": False,
        "formal_credit": 0,
        "unconditional_C27_C28_C29": "REJECT_REMAINS_PENDING_FULL_TWENTY_FAMILY_GATE",
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
