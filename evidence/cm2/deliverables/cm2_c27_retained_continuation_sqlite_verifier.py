#!/usr/bin/env python3
"""Independent SQLite reconstruction of RETAINED_CONTINUATION.

This implementation does not import the stream gate.  It materializes the
complete C20A/C20D geometric relation in SQLite and selects continuations by
an exact normalized-rational face join before consuming current C15/C25/C26
authority rows.  It emits commitments comparable with the stream gate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from typing import Any, Iterator


HERE = Path(__file__).resolve().parent
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C20A = "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz"
C20D = "cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel_ledger.jsonl.gz"
C20D_I2 = "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_representation_index.jsonl.gz"
R295A = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_representation_alias_ledger.json.gz"
C25M = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C25R = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_representation_ledger.jsonl.gz"
C26H = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_transition_ready_handle_ledger.jsonl.gz"
PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C20A: "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922",
    C20D: "0b3177691d8822a6cad5a73650f612980ee2999ba7b646783604ef084b5c6078",
    C20D_I2: "68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83",
    R295A: "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    C25M: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C25R: "3259f665e323cde3d56d8eaf6703744bca795208e733f3ac14663ea4882df45d",
    C26H: "498088be8302efdf0ed95fb5eca6847fa5d7d3b004af45b9efdf77deaaf80575",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def path_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(HERE / name, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def close_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    need(isinstance(claimed, str) and claimed == digest(
        {key: value for key, value in row.items() if key != "row_sha256"}),
         label + ":row closure")


def box(ast: dict[str, Any], label: str) -> tuple[str, str, tuple[str, ...]]:
    need(ast.get("kind") == "OPEN_RATIONAL_BOX", label + ":kind")
    coordinates = ast.get("coordinates")
    need(coordinates in (["t", "p", "s"], ["t^2", "p", "s"]), label + ":coordinates")
    bounds = tuple(Fraction(value) for value in ast.get("bounds", []))
    need(len(bounds) == 6 and bounds[0] < bounds[1] and bounds[2] < bounds[3]
         and bounds[4] < bounds[5], label + ":bounds")
    volume = (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
    claimed = ast.get("exact_coordinate_volume", ast.get("exact_volume"))
    need(volume == Fraction(claimed), label + ":volume")
    normalized = tuple(str(value) for value in bounds)
    return str(ast["coordinate_chart"]), str(coordinates[0]), normalized


def build(seed: int) -> dict[str, Any]:
    need(type(seed) is int, "integer seed")
    for name, expected in PINS.items():
        need(path_hash(HERE / name) == expected, "pin:" + name)

    with tempfile.TemporaryDirectory(prefix="cm2-retained-sqlite-") as tmp:
        database = sqlite3.connect(str(Path(tmp) / "gate.sqlite"))
        database.executescript("""
        PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=MEMORY;
        CREATE TABLE owner(
          member TEXT PRIMARY KEY, component TEXT, chart TEXT, coord TEXT,
          t0 TEXT, t1 TEXT, p0 TEXT, p1 TEXT, s0 TEXT, s1 TEXT,
          support_sha TEXT, row_sha TEXT
        ) WITHOUT ROWID;
        CREATE TABLE typed(
          representation TEXT PRIMARY KEY, owner_member TEXT, component TEXT,
          chart TEXT, coord TEXT, t0 TEXT, t1 TEXT, p0 TEXT, p1 TEXT, s0 TEXT, s1 TEXT,
          semantic TEXT, relation TEXT, source_sha TEXT, owner_sha TEXT, row_sha TEXT
        ) WITHOUT ROWID;
        CREATE TABLE authority(
          representation TEXT PRIMARY KEY, owner_member TEXT, component TEXT,
          base_root TEXT, official_key TEXT, face_sha TEXT,
          source_sha TEXT, owner_sha TEXT, c15_sha TEXT, c20a_sha TEXT, c20d_sha TEXT,
          i2_sha TEXT, r295_sha TEXT,
          c25m_sha TEXT, c25r_sha TEXT, c26h_sha TEXT
        ) WITHOUT ROWID;
        """)

        owner_rows: dict[str, dict[str, Any]] = {}
        for ordinal, row in enumerate(rows(C20A)):
            need(row.get("ordinal") == ordinal, "C20A ordinal")
            close_row(row, "C20A")
            need(row["support_ast_sha256"] == digest(row["support_ast"]), "C20A AST")
            chart, coord, bounds = box(row["support_ast"], "C20A")
            member = row["member_id"]
            need(member not in owner_rows, "C20A unique")
            owner_rows[member] = row
            database.execute("INSERT INTO owner VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                             (member, row["fresh_component_id"], chart, coord, *bounds,
                              row["support_ast_sha256"], row["row_sha256"]))
        need(len(owner_rows) == 126_468, "C20A count")

        semantic_census: Counter[str] = Counter()
        relation_census: Counter[str] = Counter()
        typed_rows: dict[str, dict[str, Any]] = {}
        for ordinal, row in enumerate(rows(C20D)):
            need(row.get("ordinal") == ordinal, "C20D ordinal")
            close_row(row, "C20D")
            need(row["typed_source_support_ast_sha256"] == digest(row["typed_source_support_ast"]),
                 "C20D AST")
            chart, coord, bounds = box(row["typed_source_support_ast"], "C20D")
            representation = row["representation_id"]
            need(representation not in typed_rows, "C20D unique")
            typed_rows[representation] = row
            semantic_census[row["source_semantics"]] += 1
            relation_census[row["exact_relation_to_owner_support"]] += 1
            database.execute("INSERT INTO typed VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                             (representation, row["owner_member_id"], row["fresh_component_id"],
                              chart, coord, *bounds, row["source_semantics"],
                              row["exact_relation_to_owner_support"],
                              row["typed_source_support_ast_sha256"], row["owner_support_ast_sha256"],
                              row["row_sha256"]))
        need(len(typed_rows) == 2_520, "C20D count")
        need(semantic_census == {
            "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER": 720,
            "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL": 1_524,
            "ADJACENT_POSITIVE_T_CONTINUATION": 276,
        }, "semantic census")
        need(relation_census == {
            "STRICT_SUBCOVER_OF_OWNER_SUPPORT": 2_244,
            "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE": 276,
        }, "relation census")

        predicate = """
          t.coord='t' AND o.coord='t' AND t.chart=o.chart AND t.t0='0'
          AND t.t1=o.t0 AND t.p0=o.p0 AND t.p1=o.p1 AND t.s0=o.s0 AND t.s1=o.s1
        """
        candidates = list(database.execute(
            "SELECT t.representation,t.owner_member,t.component,t.chart,t.t1,t.p0,t.p1,t.s0,t.s1,"
            "t.source_sha,t.owner_sha,t.row_sha,o.support_sha,o.row_sha,t.semantic,t.relation "
            "FROM typed t JOIN owner o ON o.member=t.owner_member WHERE " + predicate +
            " ORDER BY t.representation"
        ))
        need(len(candidates) == 276, "SQL geometry denominator")
        mismatch = database.execute(
            "SELECT COUNT(*) FROM typed t JOIN owner o ON o.member=t.owner_member WHERE "
            "((" + predicate + ") != (t.semantic='ADJACENT_POSITIVE_T_CONTINUATION'))"
        ).fetchone()[0]
        need(mismatch == 0, "geometry/semantic iff")
        need(all(row[14] == "ADJACENT_POSITIVE_T_CONTINUATION" and
                 row[15] == "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"
                 for row in candidates), "candidate labels")
        selected_reps = {row[0] for row in candidates}
        selected_owners = {row[1] for row in candidates}
        need(len(selected_reps) == len(selected_owners) == 276, "unique candidate owner")

        i2_selected: dict[str, dict[str, Any]] = {}
        i2_count = 0
        for row in rows(C20D_I2):
            i2_count += 1
            close_row(row, "I2")
            if row.get("representation_semantics") != "ADJACENT_POSITIVE_T_CONTINUATION":
                continue
            representation = row.get("representation_id")
            need(representation not in i2_selected, "I2 selected unique")
            need(row.get("source_kind") == "R295A_ROUND179_ADJACENT_POSITIVE_T_CONTINUATION",
                 "I2 source kind")
            need(row.get("representation_role") == "PRESERVED_ALIAS_HANDLE", "I2 role")
            i2_selected[representation] = row
        need(i2_count == 183_572 and set(i2_selected) == selected_reps, "I2 totality")
        with gzip.open(HERE / R295A, "rt", encoding="utf-8") as stream:
            r295_top = json.load(stream)
        need(r295_top.get("row_count") == 276 and
             r295_top.get("every_row_closed_by_own_SHA256") is True, "R295A top")
        r295_rows: dict[str, dict[str, Any]] = {}
        for row in r295_top.get("rows", []):
            close_row(row, "R295A")
            row_id = row.get("Round295A_retained_continuation_alias_row_id")
            need(isinstance(row_id, str) and row_id not in r295_rows, "R295A unique")
            r295_rows[row_id] = row
        need(len(r295_rows) == 276, "R295A count")

        c15: dict[str, dict[str, Any]] = {}
        c25m: dict[str, dict[str, Any]] = {}
        for ordinal, row in enumerate(rows(C15)):
            need(row.get("member_ordinal") == ordinal, "C15 ordinal")
            if row.get("registry_member_id") in selected_owners:
                close_row(row, "C15")
                c15[row["registry_member_id"]] = row
        for ordinal, row in enumerate(rows(C25M)):
            need(row.get("member_ordinal") == ordinal, "C25M ordinal")
            if row.get("member_id") in selected_owners:
                close_row(row, "C25M")
                c25m[row["member_id"]] = row
        need(set(c15) == selected_owners == set(c25m), "owner authority cover")

        c25r: dict[str, dict[str, Any]] = {}
        c26h: dict[str, dict[str, Any]] = {}
        rep_iter = iter(rows(C25R)); handle_iter = iter(rows(C26H))
        for ordinal in range(549_616):
            rep = next(rep_iter, None); handle = next(handle_iter, None)
            need(rep is not None and handle is not None, "handle length")
            need(rep.get("representation_ordinal") == handle.get("handle_ordinal") == ordinal,
                 "handle ordinal")
            need(rep.get("representation_id") == handle.get("representation_id"), "handle id")
            need(handle.get("source_bindings", {}).get("C25_representation_row_sha256") == rep.get("row_sha256"),
                 "handle row link")
            if rep["representation_id"] in selected_reps:
                close_row(rep, "C25R"); close_row(handle, "C26H")
                c25r[rep["representation_id"]] = rep
                c26h[rep["representation_id"]] = handle
        need(next(rep_iter, None) is None and next(handle_iter, None) is None, "handle exhaustion")
        need(set(c25r) == selected_reps == set(c26h), "handle cover")

        for candidate in candidates:
            representation, member, component, chart, tface, p0, p1, s0, s1, source_sha, owner_sha, c20d_sha, _, c20a_sha, _, _ = candidate
            a = owner_rows[member]; d = typed_rows[representation]
            index = i2_selected[representation]
            r295 = r295_rows[index["source_row_id"]]
            m15 = c15[member]; m25 = c25m[member]; r25 = c25r[representation]; h26 = c26h[representation]
            need(component == a["fresh_component_id"] == m15["fresh_component_id"] ==
                 m25["fresh_component_id"] == r25["fresh_component_id"] == h26["fresh_component_id"],
                 "component join")
            need(m15["base_root_id"] == m25["base_root_id"] == r25["base_root_id"] == h26["base_root_id"],
                 "root join")
            need(m15["official_key_id"] == m25["official_key_id"] == r25["official_key_id"] == h26["official_key_id"],
                 "key join")
            need(m25["source_bindings"]["support_kernel"] == "C20A" and
                 m25["source_bindings"]["support_kernel_row_sha256"] == c20a_sha and
                 m25["source_bindings"]["C15_member_row_sha256"] == m15["row_sha256"],
                 "C20A/C15 bindings")
            need(r25["source_bindings"]["semantic_kernel"] == "C20D" and
                 r25["source_bindings"]["semantic_kernel_row_sha256"] == c20d_sha,
                 "C20D binding")
            need(index["source_row_sha256"] == r295["row_sha256"] == d["source_row_sha256"],
                 "C20D/I2/R295A source join")
            need(index["owner_member_id"] == r295["target_Round294_registry_occurrence_id"] == member,
                 "C20D/I2/R295A owner join")
            need(r295["retained_positive_t_open_box"] == d["typed_source_support_ast"]["bounds"] and
                 r295["resolved_sibling_open_box"] == a["support_ast"]["bounds"],
                 "R295A two-box join")
            need(r295["source_chart"] == a["support_ast"]["coordinate_chart"] and
                 r295["exact_full_face_shared"] is True and r295["exact_volume_conserved"] is True,
                 "R295A gluing")
            need(r295["same_origin_unique_index1_sibling"] is True and
                 r295["signature_or_box_equality_used_as_identity_basis"] is False and
                 r295["symmetry_used_as_identity_basis"] is False,
                 "R295A same-origin identity")
            need(r295["complete_Round294_registry_positive_volume_overlap_count"] == 0 and
                 r295["undesignated_positive_volume_overlap_count"] == 0,
                 "R295A no overlap")
            need(r25["owner_member_id"] == h26["owner_member_id"] == member, "owner join")
            need(r25["owner_normalized_support_ast_sha256"] ==
                 h26["owner_normalized_support_ast_sha256"] == owner_sha, "owner support")
            need(r25["representation_semantic_kind"] == h26["representation_semantic_kind"] ==
                 "TYPED_NONFULL_REPRESENTATION_DISPOSITION", "semantic join")
            cert = h26["transition_ready_certificate"]
            need(h26["transition_ready_certificate_sha256"] == digest(cert), "certificate closure")
            need(cert["typed_owner_support_bound"] is True and
                 cert["typed_representation_semantics_closed"] is True and
                 cert["fresh_component_binding_consumed"] is True and
                 cert["transition_theorem_claimed"] is False and cert["pair_routing_claimed"] is False,
                 "certificate nonpromotion")
            face_sha = digest({"coordinate_chart": chart, "t": tface,
                               "p": [p0, p1], "s": [s0, s1]})
            database.execute("INSERT INTO authority VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                             (representation, member, component, m15["base_root_id"],
                              m15["official_key_id"], face_sha, source_sha, owner_sha,
                              m15["row_sha256"], c20a_sha, c20d_sha, index["row_sha256"],
                              r295["row_sha256"], m25["row_sha256"],
                              r25["row_sha256"], h26["row_sha256"]))
        database.commit()

        material = list(database.execute(
            "SELECT representation,owner_member,component,base_root,official_key,face_sha,"
            "source_sha,owner_sha,c15_sha,c20a_sha,c20d_sha,i2_sha,r295_sha,c25m_sha,c25r_sha,c26h_sha "
            "FROM authority ORDER BY representation"
        ))
        need(len(material) == 276, "materialized authority count")
        ids = hashlib.sha256(); sequence = hashlib.sha256(); face_set: set[str] = set()
        chart_census = Counter(row[3] for row in candidates)
        for row in material:
            (representation, member, component, root, key, face_sha, source_sha, owner_sha,
             c15_sha, c20a_sha, c20d_sha, i2_sha, r295_sha, c25m_sha, c25r_sha, c26h_sha) = row
            need(face_sha not in face_set, "unique face")
            face_set.add(face_sha)
            body = {
                "representation_id": representation,
                "owner_member_id": member,
                "fresh_component_id": component,
                "base_root_id": root,
                "official_key_id": key,
                "shared_full_face_sha256": face_sha,
                "typed_source_support_ast_sha256": source_sha,
                "owner_support_ast_sha256": owner_sha,
                "C15_row_sha256": c15_sha,
                "C20A_row_sha256": c20a_sha,
                "C20D_row_sha256": c20d_sha,
                "I2_row_sha256": i2_sha,
                "R295A_row_sha256": r295_sha,
                "C25_member_row_sha256": c25m_sha,
                "C25_representation_row_sha256": c25r_sha,
                "C26_handle_row_sha256": c26h_sha,
                "formal_credit": 0,
            }
            ids.update(representation.encode("ascii") + b"\n")
            sequence.update(bytes.fromhex(digest(body)))

    result = {
        "schema": "cm2.c27.retained-continuation-physical-totality-zero-credit.v1",
        "status": "PASS_LOCAL_ZERO_CREDIT__276_RETAINED_CONTINUATIONS__EXACT_POSITIVE_T_FULL_FACE_ADJACENCY__ZERO_GAPS",
        "implementation": "SQLITE_EXACT_FACE_JOIN_THEN_AUTHORITY_BINDING",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "seed_declared_but_not_semantically_used": True,
        "input_pins": dict(sorted(PINS.items())),
        "full_ledger_census": {C15: 502_204, C20A: 126_468, C20D: 2_520,
                               C20D_I2: 183_572, R295A: 276,
                               C25M: 502_204, C25R: 549_616, C26H: 549_616},
        "C20D_source_semantic_census": dict(sorted(semantic_census.items())),
        "C20D_relation_census": dict(sorted(relation_census.items())),
        "candidate_universe": {
            "definition": "ALL_AND_ONLY_C20D_TYPED_BOXES_SHARING_COMPLETE_POSITIVE_T_FACE_WITH_THEIR_C20A_OWNER",
            "candidate_count": 276,
            "chart_census": dict(sorted(chart_census.items())),
            "candidate_representation_ids_sha256": ids.hexdigest(),
            "candidate_row_sequence_sha256": sequence.hexdigest(),
            "order": "representation_id_ASCII",
        },
        "join_gap_census": {
            "C20D_owner_missing_from_C20A": 0, "I2_representation_orphan": 0,
            "R295A_identity_or_geometry_orphan": 0, "C15_owner_orphan": 0,
            "C25_member_orphan": 0, "C25_representation_orphan": 0,
            "C26_handle_orphan": 0, "component_root_key_mismatch": 0,
            "support_or_source_binding_mismatch": 0,
            "duplicate_owner_or_shared_face_assignment": 0, "unresolved_geometry": 0,
        },
        "unique_assignment": "PASS_BY_EXACT_C20D_GEOMETRY_PARTITION__276_ADJACENT_VS_2244_STRICT_SUBCOVER",
        "attachment_terminal_overlap_after_required_C20D_SOURCE_SPLIT": 0,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_COMPLETE_TWENTY_TERMINAL_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    print(canonical(build(args.seed)).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
