#!/usr/bin/env python3
"""Order-independent SQLite replay of INCLUDED_STRATUM_ATTACHMENTS.

This is intentionally independent of the stream implementation.  It indexes
the selected C25 semantics, primitive C20D source dispositions, matching C26
handles, and C15 owner rows in four tables and performs a relational join
ordered only at the final digest step.  The 276 adjacent positive-t
continuations are routed out before the attachment candidate digest.
Round306C27 and all edge ledgers are outside the input surface.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from typing import Any, Iterator


HERE = Path(__file__).resolve().parent
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_representation_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_transition_ready_handle_ledger.jsonl.gz"
C20D = "cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel_ledger.jsonl.gz"
PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C25: "3259f665e323cde3d56d8eaf6703744bca795208e733f3ac14663ea4882df45d",
    C26: "498088be8302efdf0ed95fb5eca6847fa5d7d3b004af45b9efdf77deaaf80575",
    C20D: "0b3177691d8822a6cad5a73650f612980ee2999ba7b646783604ef084b5c6078",
}
FULL_COUNTS = {C15: 502_204, C25: 549_616, C26: 549_616, C20D: 2_520}
KINDS = {
    "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8_416,
    "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2_520,
}
ASSIGNED_KINDS = {
    "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8_416,
    "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2_244,
}
KIND_KERNELS = {
    "EXACT_SUBCOVER_INCLUSION_DISPOSITION": {"C22B", "C23B"},
    "TYPED_NONFULL_REPRESENTATION_DISPOSITION": {"C20D"},
}
KERNEL_COUNTS = {"C20D": 2_520, "C22B": 7_288, "C23B": 1_128}
ASSIGNED_KERNEL_COUNTS = {"C20D": 2_244, "C22B": 7_288, "C23B": 1_128}
C20D_SEMANTICS = {
    "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER": 720,
    "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL": 1_524,
    "ADJACENT_POSITIVE_T_CONTINUATION": 276,
}
C20D_STRICT = frozenset({
    "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER",
    "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL",
})
C20D_KERNEL_RESULT_SHA256 = "946bf9772c39efb6c9a39a8b518e8e830b96f42e429b6c629c53c031260451ab"
EXPECTED_CANDIDATE_IDS_SHA256 = "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511"
EXPECTED_EXCLUDED_ADJACENT_IDS_SHA256 = "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
EXPECTED_ORIGINAL_NON_EQUALITY_IDS_SHA256 = "e2ffc75d183889b90eee29d15e0c0783976d8290ebde977c3081a82bf57c602f"


class GateFailure(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if value is not True:
        raise GateFailure(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def sha_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            block = source.read(4 * 1024 * 1024)
            if not block:
                return state.hexdigest()
            state.update(block)


def json_lines(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, mode="rt", encoding="ascii") as source:
        for line in source:
            yield json.loads(line)


def closed(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, label + " sha shape")
    body = dict(row)
    body.pop("row_sha256")
    require(sha(body) == claimed, label + " sha closure")


def prepare(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys=OFF;
        PRAGMA journal_mode=OFF;
        PRAGMA synchronous=OFF;
        PRAGMA temp_store=FILE;
        CREATE TABLE c25(
          rep TEXT PRIMARY KEY, owner TEXT NOT NULL, component TEXT NOT NULL,
          base_root TEXT NOT NULL, official_key TEXT NOT NULL,
          support_sha TEXT NOT NULL, kind TEXT NOT NULL, semantic_sha TEXT NOT NULL,
          kernel TEXT NOT NULL, kernel_ledger TEXT, kernel_result TEXT,
          kernel_ref TEXT, coarse TEXT NOT NULL, row_sha TEXT NOT NULL
        ) WITHOUT ROWID;
        CREATE TABLE c26(
          rep TEXT PRIMARY KEY, owner TEXT NOT NULL, component TEXT NOT NULL,
          base_root TEXT NOT NULL, official_key TEXT NOT NULL,
          support_sha TEXT NOT NULL, kind TEXT NOT NULL, semantic_sha TEXT NOT NULL,
          c25_ref TEXT NOT NULL, row_sha TEXT NOT NULL
        ) WITHOUT ROWID;
        CREATE TABLE c15(
          owner TEXT PRIMARY KEY, component TEXT NOT NULL, base_root TEXT NOT NULL,
          official_key TEXT NOT NULL, row_sha TEXT NOT NULL
        ) WITHOUT ROWID;
        CREATE TABLE c20d(
          rep TEXT PRIMARY KEY, owner TEXT NOT NULL, component TEXT NOT NULL,
          support_sha TEXT NOT NULL, source_semantics TEXT NOT NULL,
          relation TEXT NOT NULL, row_sha TEXT NOT NULL
        ) WITHOUT ROWID;
        """
    )


def candidate_from_join(row: sqlite3.Row) -> dict[str, Any]:
    require(row["owner25"] == row["owner26"] == row["owner15"], "owner join")
    require(row["component25"] == row["component26"] == row["component15"], "component join")
    require(row["root25"] == row["root26"] == row["root15"], "base-root join")
    require(row["key25"] == row["key26"] == row["key15"], "official-key join")
    require(row["support25"] == row["support26"], "support join")
    require(row["kind25"] == row["kind26"] and row["kind25"] in KINDS, "kind join")
    require(row["semantic25"] == row["semantic26"], "semantic certificate join")
    require(row["c25_ref"] == row["row25"], "C26-to-C25 row binding")
    require(row["kernel"] in KIND_KERNELS[row["kind25"]], "kind/kernel partition")
    if row["kernel"] == "C20D":
        require(row["source_semantics"] in C20D_STRICT, "C20D strict-subcover terminal assignment")
        require(row["relation"] == "STRICT_SUBCOVER_OF_OWNER_SUPPORT", "C20D strict relation")
        require(row["rep20d"] == row["rep"], "C20D representation join")
        require(row["owner20d"] == row["owner25"], "C20D owner join")
        require(row["component20d"] == row["component25"], "C20D component join")
        require(row["support20d"] == row["support25"], "C20D owner support join")
        require(row["kernel_ref"] == row["row20d"], "C25/C20D row binding")
        require(row["kernel_ledger"] == C20D, "C25 C20D kernel ledger pin")
        require(row["kernel_result"] == C20D_KERNEL_RESULT_SHA256, "C25 C20D result pin")
        require(row["coarse"] == "PRESERVED", "C25 C20D coarse family")
    else:
        require(row["source_semantics"] is None and row["row20d"] is None, "non-C20D has no C20D join")
    return {
        "representation_id": row["rep"],
        "owner_member_id": row["owner15"],
        "fresh_component_id": row["component15"],
        "base_root_id": row["root15"],
        "official_key_id": row["key15"],
        "representation_semantic_kind": row["kind25"],
        "semantic_kernel": row["kernel"],
        "owner_normalized_support_ast_sha256": row["support25"],
        "representation_semantic_certificate_sha256": row["semantic25"],
        "C15_member_row_sha256": row["row15"],
        "C25_representation_row_sha256": row["row25"],
        "C26_handle_row_sha256": row["row26"],
        "C20D_source_semantics": row["source_semantics"],
        "C20D_row_sha256": row["row20d"],
        "cross_component": False,
        "formal_credit": 0,
    }


def run(seed: int) -> dict[str, Any]:
    require(type(seed) is int, "integer seed")
    for filename, expected in PINS.items():
        path = HERE / filename
        require(path.is_file() and not path.is_symlink(), "regular input " + filename)
        require(sha_file(path) == expected, "input pin " + filename)

    with tempfile.TemporaryDirectory(prefix="cm2-c27-included-stratum-sqlite-") as temporary:
        database = Path(temporary) / "join.sqlite3"
        connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        prepare(connection)
        kind_counts: Counter[str] = Counter()
        kernel_counts: Counter[str] = Counter()
        owners: set[str] = set()

        c20d_counts: Counter[str] = Counter()
        count20d = 0
        for row in json_lines(HERE / C20D):
            require(row.get("ordinal") == count20d, "C20D ordinal")
            count20d += 1
            closed(row, "C20D full")
            require(row.get("schema") == "cm2.round306c20d.source-g-2520-preserved-nonfull-alias-negative-disposition-kernel.v1.row.v1", "C20D schema")
            semantics = row.get("source_semantics")
            require(semantics in C20D_SEMANTICS, "C20D source semantics")
            expected_relation = (
                "STRICT_SUBCOVER_OF_OWNER_SUPPORT"
                if semantics in C20D_STRICT
                else "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"
            )
            require(row.get("exact_relation_to_owner_support") == expected_relation, "C20D exact relation/semantics")
            require(row.get("negative_disposition") == "NOT_A_COMPLETE_SUPPORT_REPRESENTATION__RETAIN_AS_TYPED_NONFULL_ALIAS_HANDLE", "C20D negative disposition")
            require(sha(row.get("typed_source_support_ast")) == row.get("typed_source_support_ast_sha256"), "C20D source support closure")
            try:
                connection.execute(
                    "INSERT INTO c20d VALUES(?,?,?,?,?,?,?)",
                    (
                        row["representation_id"], row["owner_member_id"], row["fresh_component_id"],
                        row["owner_support_ast_sha256"], semantics,
                        row["exact_relation_to_owner_support"], row["row_sha256"],
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise GateFailure("duplicate C20D representation") from exc
            c20d_counts[semantics] += 1
        require(count20d == FULL_COUNTS[C20D], "C20D full count")
        require(dict(c20d_counts) == C20D_SEMANTICS, "C20D source semantic census")

        count25 = 0
        for row in json_lines(HERE / C25):
            require(row.get("representation_ordinal") == count25, "C25 ordinal")
            count25 += 1
            kind = row.get("representation_semantic_kind")
            if kind not in KINDS:
                continue
            closed(row, "selected C25")
            kernel = row["source_bindings"]["semantic_kernel"]
            require(kernel in KIND_KERNELS[kind], "C25 kind/kernel")
            try:
                connection.execute(
                    "INSERT INTO c25 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        row["representation_id"], row["owner_member_id"], row["fresh_component_id"],
                        row["base_root_id"], row["official_key_id"], row["owner_normalized_support_ast_sha256"],
                        kind, row["representation_semantic_certificate_sha256"], kernel,
                        row["source_bindings"].get("semantic_kernel_ledger"),
                        row["source_bindings"].get("semantic_kernel_result_sha256"),
                        row["source_bindings"].get("semantic_kernel_row_sha256"),
                        row["coarse_family"], row["row_sha256"],
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise GateFailure("duplicate C25 candidate") from exc
            owners.add(row["owner_member_id"])
            kind_counts[kind] += 1
            kernel_counts[kernel] += 1
        require(count25 == FULL_COUNTS[C25], "C25 full count")
        require(dict(kind_counts) == KINDS, "C25 semantic census")
        require(dict(kernel_counts) == KERNEL_COUNTS, "C25 kernel census")

        count26 = 0
        selected26 = Counter()
        for row in json_lines(HERE / C26):
            require(row.get("handle_ordinal") == count26, "C26 ordinal")
            count26 += 1
            kind = row.get("representation_semantic_kind")
            if kind not in KINDS:
                continue
            closed(row, "selected C26")
            certificate = row.get("transition_ready_certificate", {})
            require(certificate.get("kind") == "B1A_TRANSITION_READY_REPRESENTATION_HANDLE", "handle kind")
            require(certificate.get("typed_owner_support_bound") is True, "handle owner support")
            require(certificate.get("typed_representation_semantics_closed") is True, "handle semantics")
            require(certificate.get("fresh_component_binding_consumed") is True, "handle component")
            require(certificate.get("transition_theorem_claimed") is False, "handle no transition promotion")
            require(certificate.get("pair_routing_claimed") is False, "handle no routing promotion")
            require(sha(certificate) == row.get("transition_ready_certificate_sha256"), "handle certificate closure")
            try:
                connection.execute(
                    "INSERT INTO c26 VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        row["representation_id"], row["owner_member_id"], row["fresh_component_id"],
                        row["base_root_id"], row["official_key_id"], row["owner_normalized_support_ast_sha256"],
                        kind, row["representation_semantic_certificate_sha256"],
                        row["source_bindings"]["C25_representation_row_sha256"], row["row_sha256"],
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise GateFailure("duplicate C26 candidate") from exc
            selected26[kind] += 1
        require(count26 == FULL_COUNTS[C26], "C26 full count")
        require(dict(selected26) == KINDS, "C26 semantic census")

        count15 = 0
        selected15: set[str] = set()
        for row in json_lines(HERE / C15):
            require(row.get("member_ordinal") == count15, "C15 ordinal")
            count15 += 1
            owner = row.get("registry_member_id")
            if owner not in owners:
                continue
            closed(row, "selected C15")
            try:
                connection.execute(
                    "INSERT INTO c15 VALUES(?,?,?,?,?)",
                    (owner, row["fresh_component_id"], row["base_root_id"], row["official_key_id"], row["row_sha256"]),
                )
            except sqlite3.IntegrityError as exc:
                raise GateFailure("duplicate C15 selected owner") from exc
            selected15.add(owner)
        require(count15 == FULL_COUNTS[C15], "C15 full count")
        require(selected15 == owners, "C15 owner cover")
        connection.commit()

        orphan25 = connection.execute("SELECT COUNT(*) FROM c25 LEFT JOIN c26 USING(rep) WHERE c26.rep IS NULL").fetchone()[0]
        orphan26 = connection.execute("SELECT COUNT(*) FROM c26 LEFT JOIN c25 USING(rep) WHERE c25.rep IS NULL").fetchone()[0]
        orphan15 = connection.execute("SELECT COUNT(*) FROM c25 LEFT JOIN c15 ON c15.owner=c25.owner WHERE c15.owner IS NULL").fetchone()[0]
        require((orphan25, orphan26, orphan15) == (0, 0, 0), "relational orphan census")
        c20d_without_c25 = connection.execute("SELECT COUNT(*) FROM c20d LEFT JOIN c25 ON c25.rep=c20d.rep WHERE c25.rep IS NULL").fetchone()[0]
        c25_without_c20d = connection.execute("SELECT COUNT(*) FROM c25 LEFT JOIN c20d ON c20d.rep=c25.rep WHERE c25.kernel='C20D' AND c20d.rep IS NULL").fetchone()[0]
        c20d_binding_mismatch = connection.execute(
            """SELECT COUNT(*) FROM c25 JOIN c20d ON c20d.rep=c25.rep
               WHERE c25.kernel!='C20D'
                  OR c25.kind!='TYPED_NONFULL_REPRESENTATION_DISPOSITION'
                  OR c25.coarse!='PRESERVED'
                  OR c25.owner!=c20d.owner
                  OR c25.component!=c20d.component
                  OR c25.support_sha!=c20d.support_sha
                  OR c25.kernel_ledger!=?
                  OR c25.kernel_result!=?
                  OR c25.kernel_ref!=c20d.row_sha""",
            (C20D, C20D_KERNEL_RESULT_SHA256),
        ).fetchone()[0]
        require((c20d_without_c25, c25_without_c20d, c20d_binding_mismatch) == (0, 0, 0), "C20D/C25 exact join")

        query = """
          SELECT c25.rep AS rep,
            c25.owner AS owner25, c26.owner AS owner26, c15.owner AS owner15,
            c25.component AS component25, c26.component AS component26, c15.component AS component15,
            c25.base_root AS root25, c26.base_root AS root26, c15.base_root AS root15,
            c25.official_key AS key25, c26.official_key AS key26, c15.official_key AS key15,
            c25.support_sha AS support25, c26.support_sha AS support26,
            c25.kind AS kind25, c26.kind AS kind26,
            c25.semantic_sha AS semantic25, c26.semantic_sha AS semantic26,
            c25.kernel AS kernel, c25.kernel_ledger AS kernel_ledger,
            c25.kernel_result AS kernel_result, c25.kernel_ref AS kernel_ref,
            c25.coarse AS coarse, c26.c25_ref AS c25_ref,
            c15.row_sha AS row15, c25.row_sha AS row25, c26.row_sha AS row26,
            c20d.rep AS rep20d, c20d.owner AS owner20d,
            c20d.component AS component20d, c20d.support_sha AS support20d,
            c20d.source_semantics AS source_semantics, c20d.relation AS relation,
            c20d.row_sha AS row20d
          FROM c25 JOIN c26 USING(rep) JOIN c15 ON c15.owner=c25.owner
          LEFT JOIN c20d ON c20d.rep=c25.rep
          WHERE c25.kernel!='C20D' OR c20d.source_semantics IN (
            'EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER',
            'EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL'
          )
          ORDER BY c25.rep COLLATE BINARY
        """
        row_sequence = hashlib.sha256()
        id_sequence = hashlib.sha256()
        candidate_count = 0
        assigned_kind_counts: Counter[str] = Counter()
        assigned_kernel_counts: Counter[str] = Counter()
        for joined in connection.execute(query):
            candidate = candidate_from_join(joined)
            row_sequence.update(bytes.fromhex(sha(candidate)))
            id_sequence.update(candidate["representation_id"].encode("ascii") + b"\n")
            candidate_count += 1
            assigned_kind_counts[candidate["representation_semantic_kind"]] += 1
            assigned_kernel_counts[candidate["semantic_kernel"]] += 1
        require(candidate_count == 10_660, "joined candidate count")
        require(dict(assigned_kind_counts) == ASSIGNED_KINDS, "assigned kind census")
        require(dict(assigned_kernel_counts) == ASSIGNED_KERNEL_COUNTS, "assigned kernel census")
        excluded_ids = hashlib.sha256()
        excluded_count = 0
        for row in connection.execute(
            "SELECT rep FROM c20d WHERE source_semantics='ADJACENT_POSITIVE_T_CONTINUATION' ORDER BY rep COLLATE BINARY"
        ):
            excluded_ids.update(row["rep"].encode("ascii") + b"\n")
            excluded_count += 1
        original_ids = hashlib.sha256()
        for row in connection.execute(
            "SELECT rep FROM c25 ORDER BY rep COLLATE BINARY"
        ):
            original_ids.update(row["rep"].encode("ascii") + b"\n")
        candidate_excluded_intersection = connection.execute(
            """SELECT COUNT(*) FROM c25 JOIN c20d USING(rep)
               WHERE c20d.source_semantics='ADJACENT_POSITIVE_T_CONTINUATION'
                 AND (c25.kernel!='C20D' OR c20d.source_semantics IN (
                   'EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER',
                   'EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL'))"""
        ).fetchone()[0]
        require(excluded_count == 276, "excluded adjacent census")
        require(candidate_excluded_intersection == 0, "attachment/adjacent disjointness")
        require(id_sequence.hexdigest() == EXPECTED_CANDIDATE_IDS_SHA256, "corrected attachment ID commitment")
        require(excluded_ids.hexdigest() == EXPECTED_EXCLUDED_ADJACENT_IDS_SHA256, "excluded adjacent ID commitment")
        require(original_ids.hexdigest() == EXPECTED_ORIGINAL_NON_EQUALITY_IDS_SHA256, "original non-equality union commitment")
        connection.close()

    result = {
        "schema": "cm2.c27-independent.included-stratum-attachments.sqlite-zero-credit.v1",
        "status": "PASS_ZERO_CREDIT__10660_INCLUDED_STRATUM_ATTACHMENTS__C20D_PRIMITIVE_SPLIT__ORDER_INDEPENDENT_SQLITE_JOIN__ZERO_GAPS",
        "implementation": "ORDER_INDEPENDENT_SQLITE_RELATIONAL_JOIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "seed_declared_but_not_semantically_used": True,
        "input_pins": dict(sorted(PINS.items())),
        "full_ledger_census": dict(sorted(FULL_COUNTS.items())),
        "candidate_universe": {
            "definition": "C25_EXACT_SUBCOVER_PLUS_ONLY_C20D_PRIMITIVE_STRICT_SUBCOVERS",
            "semantic_kind_census": dict(sorted(assigned_kind_counts.items())),
            "semantic_kernel_census": dict(sorted(assigned_kernel_counts.items())),
            "C20D_source_semantic_census": dict(sorted(c20d_counts.items())),
            "C20D_adjacent_positive_t_excluded_and_reserved_for_open_retained_continuation": 276,
            "excluded_adjacent_representation_ids_sha256": excluded_ids.hexdigest(),
            "candidate_excluded_intersection_count": candidate_excluded_intersection,
            "candidate_plus_excluded_union_count": 10_936,
            "candidate_plus_excluded_union_ids_sha256": original_ids.hexdigest(),
            "candidate_count": candidate_count,
            "candidate_representation_ids_sha256": id_sequence.hexdigest(),
            "candidate_row_sequence_sha256": row_sequence.hexdigest(),
            "order": "representation_id_SQLITE_BINARY",
        },
        "join_gap_census": {
            "C25_without_C26": 0,
            "C26_without_C25": 0,
            "C25_owner_without_C15": 0,
            "C20D_C25_orphan_or_row_binding_mismatch": 0,
            "duplicate_candidate_representation": 0,
            "duplicate_selected_C15_owner": 0,
            "component_mismatch_or_cross_component": 0,
            "base_root_mismatch": 0,
            "official_key_mismatch": 0,
            "support_or_semantic_mismatch": 0,
        },
        "unique_assignment": "PASS_BY_SQL_KEYS_PLUS_PRIMITIVE_C20D_STRICT_VS_ADJACENT_SOURCE_SEMANTIC_PARTITION",
        "formal_credit": 0,
        "C27_C28_C29": "UNCHANGED_REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "result_sha256": sha(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    options = parser.parse_args()
    print(encode(run(options.seed)).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
