#!/usr/bin/env python3
"""Independent SQLite reconstruction of the declared sheet-role candidate set.

This implementation deliberately does not import the streamed probe, a C27
producer, a family table, or an edge ledger.  It verifies and loads the sealed
C15/C21A/C21B/C21C/C26 JSONL inputs into relational tables, changes insertion
order as a function of the declared seed, and proves declared-role binding
totality/uniqueness with SQL joins and anti-joins.  It does not derive
half-open side inclusion, so terminal physical totality stays rejected.  The
result is local zero-credit evidence only.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import random
import sqlite3
import sys
from typing import Any, Callable, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parent
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C21A = "cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel_ledger.jsonl.gz"
C21B = "cm2_round306c21b_source_g_17716_r211_self_contained_sheet_theorem_materialization_ledger.jsonl.gz"
C21C = "cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C21A: "1c60f2ef752b1b3ab363740cec7505cbddacfbc7509922dab63bbf011e3659f1",
    C21B: "1500052cf49cfa7a22388567173a912be6b79d2ba647ad5d1906f9e170dc26bb",
    C21C: "add22270845ef504427475e91696451f2d53c41b4b2cb9af2784a9507ce60c09",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
}
NONPROMOTION_21 = {
    "B1A": 0, "B2": 0, "CM2": 0, "DSU_edge": 0,
    "DSU_union": 0, "maximality": 0,
}
NONPROMOTION_26 = {
    "B2": 0, "CM2": 0, "DSU_edge": 0, "maximality": 0,
    "member_identity": 0, "pair_routing": 0, "transition_theorem": 0,
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def checked_rows(name: str) -> Iterator[dict[str, Any]]:
    with gzip.open(ROOT / name, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), f"newline:{name}:{ordinal}")
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) + b"\n" == raw,
                 f"canonical:{name}:{ordinal}")
            claimed = row.get("row_sha256")
            need(type(claimed) is str and len(claimed) == 64,
                 f"row hash field:{name}:{ordinal}")
            body = dict(row)
            del body["row_sha256"]
            need(digest(body) == claimed, f"row hash:{name}:{ordinal}")
            yield row


def shuffled_batches(
    rows: Iterable[Sequence[Any]], seed: int, batch_size: int = 4096,
) -> Iterator[list[Sequence[Any]]]:
    """Change insertion order without changing the relational candidate set."""
    rng = random.Random(seed)
    batch: list[Sequence[Any]] = []
    for row in rows:
        batch.append(row)
        if len(batch) == batch_size:
            rng.shuffle(batch)
            yield batch
            batch = []
    if batch:
        rng.shuffle(batch)
        yield batch


def insert_shuffled(
    connection: sqlite3.Connection, sql: str, rows: Iterable[Sequence[Any]],
    seed: int,
) -> None:
    for batch in shuffled_batches(rows, seed):
        connection.executemany(sql, batch)


def one(connection: sqlite3.Connection, sql: str, parameters: Sequence[Any] = ()) -> Any:
    row = connection.execute(sql, parameters).fetchone()
    need(row is not None and len(row) == 1, "single SQL scalar")
    return row[0]


def exact_counter(
    connection: sqlite3.Connection, sql: str, expected: dict[str, int], label: str,
) -> None:
    observed = dict(connection.execute(sql).fetchall())
    need(observed == expected, label)


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys=ON;
        PRAGMA journal_mode=OFF;
        PRAGMA synchronous=OFF;
        PRAGMA temp_store=FILE;
        PRAGMA cache_size=-65536;

        CREATE TABLE members(
          member_id TEXT PRIMARY KEY,
          component_id TEXT NOT NULL,
          source_row_sha256 TEXT NOT NULL,
          member_ordinal INTEGER NOT NULL UNIQUE
        ) WITHOUT ROWID;

        CREATE TABLE sheets(
          sheet_id TEXT PRIMARY KEY,
          source_class TEXT NOT NULL CHECK(source_class IN ('R204','R211')),
          mechanism TEXT NOT NULL,
          owner_member_id TEXT NOT NULL,
          shadow_member_id TEXT NOT NULL,
          owner_claimed_component_id TEXT NOT NULL,
          shadow_claimed_component_id TEXT NOT NULL,
          physical_sheet_row_sha256 TEXT NOT NULL,
          physical_theorem_sha256 TEXT NOT NULL,
          source_kernel TEXT NOT NULL,
          source_row_sha256 TEXT,
          discharge_theorem_sha256 TEXT,
          source_formal_credit TEXT NOT NULL,
          source_theorem_kind TEXT NOT NULL,
          source_strict_nonpromotion TEXT NOT NULL
        ) WITHOUT ROWID;

        CREATE TABLE r211_discharges(
          sheet_id TEXT PRIMARY KEY,
          owner_member_id TEXT NOT NULL,
          owner_claimed_component_id TEXT NOT NULL,
          c21b_sheet_row_sha256 TEXT NOT NULL,
          source_row_sha256 TEXT NOT NULL,
          theorem_sha256 TEXT NOT NULL,
          theorem_kind TEXT NOT NULL,
          formal_credit TEXT NOT NULL,
          strict_nonpromotion TEXT NOT NULL
        ) WITHOUT ROWID;

        CREATE TABLE features(
          feature_id TEXT PRIMARY KEY,
          feature_ordinal INTEGER NOT NULL UNIQUE,
          node_id TEXT NOT NULL,
          obligation_kind TEXT NOT NULL,
          obligation_role TEXT NOT NULL,
          owner_member_id TEXT,
          depends_on_node_ids TEXT NOT NULL,
          theorem_sha256 TEXT NOT NULL,
          source_kernel TEXT,
          source_row_sha256 TEXT,
          source_ledger TEXT,
          formal_credit TEXT NOT NULL,
          strict_nonpromotion TEXT NOT NULL,
          c26_row_sha256 TEXT NOT NULL
        ) WITHOUT ROWID;
        CREATE INDEX features_node ON features(node_id);
        CREATE INDEX features_kind ON features(obligation_kind);
        """
    )


def _member_rows() -> Iterator[Sequence[Any]]:
    count = 0
    for source_ordinal, row in enumerate(checked_rows(C15)):
        need(row["member_ordinal"] == source_ordinal, "C15 source ordinal")
        count += 1
        yield (
            row["registry_member_id"], row["fresh_component_id"],
            row["row_sha256"], row["member_ordinal"],
        )
    need(count == 502_204, "C15 complete source count")


def _r204_rows() -> Iterator[Sequence[Any]]:
    kinds: Counter[str] = Counter()
    count = 0
    for row in checked_rows(C21A):
        count += 1
        kind = row["obligation_kind"]
        kinds[kind] += 1
        if kind != "A1_R204_TARGET_SHEET":
            continue
        yield (
            row["feature_row_id"], "R204",
            "R204_TARGET_REGULAR_GRAPH_SHEET",
            row["owner_member_id"], row["shadow_member_id"],
            row["owner_fresh_component_id"],
            row["shadow_fresh_component_id"], row["row_sha256"],
            row["feature_theorem_ast_sha256"], "C21A", row["row_sha256"],
            row["feature_theorem_ast_sha256"], canonical(row["formal_credit"]).decode(),
            row["feature_theorem_ast"]["kind"],
            canonical(row["strict_nonpromotion"]).decode(),
        )
    need(count == 1_008, "C21A complete source count")
    need(kinds == {
        "A1_R204_TARGET_SHEET": 224,
        "A2_R204_SOURCE_TARGET_CURVE": 504,
        "A2_R204_SOURCE_TARGET_ENDPOINT": 280,
    }, "C21A dimensional census")


def _r211_rows() -> Iterator[Sequence[Any]]:
    count = 0
    for source_ordinal, row in enumerate(checked_rows(C21B)):
        need(row["ordinal"] == source_ordinal, "C21B source ordinal")
        count += 1
        yield (
            row["R211_sheet_row_id"], "R211",
            "R211_ACTIVE_FACTOR_ZERO_SHEET",
            row["owner_member_id"], row["shadow_member_id"],
            row["owner_fresh_component_id"],
            row["shadow_fresh_component_id"], row["row_sha256"],
            row["theorem_ast_sha256"], "C21C", None, None,
            canonical(row["formal_credit"]).decode(),
            row["theorem_ast"]["kind"],
            canonical(row["strict_nonpromotion"]).decode(),
        )
    need(count == 17_716, "C21B complete source count")


def _r211_discharge_rows() -> Iterator[Sequence[Any]]:
    kinds: Counter[str] = Counter()
    count = 0
    for row in checked_rows(C21C):
        count += 1
        kind = row["obligation_kind"]
        kinds[kind] += 1
        if kind != "A1_R211_OWNER_SHEET":
            continue
        yield (
            row["feature_row_id"], row["owner_member_id"],
            row["owner_fresh_component_id"],
            row["source_bindings"]["C21b_sheet_theorem_row_sha256"],
            row["row_sha256"], row["theorem_ast_sha256"],
            row["theorem_ast"]["kind"],
            canonical(row["formal_credit"]).decode(),
            canonical(row["strict_nonpromotion"]).decode(),
        )
    need(count == 79_084, "C21C complete source count")
    need(kinds == {
        "A1_R211_OWNER_SHEET": 17_716,
        "A2_R211_OWNER_CURVE": 20_456,
        "A2_R211_OWNER_ENDPOINT": 40_912,
    }, "C21C dimensional census")


def _feature_rows() -> Iterator[Sequence[Any]]:
    count = 0
    for source_ordinal, row in enumerate(checked_rows(C26)):
        need(row["feature_ordinal"] == source_ordinal, "C26 source ordinal")
        bindings = row["source_bindings"]
        count += 1
        yield (
            row["feature_id"], row["feature_ordinal"], row["node_id"],
            row["obligation_kind"], row["obligation_role"],
            row.get("owner_member_id"),
            canonical(row["depends_on_node_ids"]).decode(),
            row["definition_or_dependency_theorem_ast_sha256"],
            bindings.get("source_kernel"), bindings.get("source_row_sha256"),
            bindings.get("source_ledger"), canonical(row["formal_credit"]).decode(),
            canonical(row["strict_nonpromotion"]).decode(), row["row_sha256"],
        )
    need(count == 691_424, "C26 complete source count")


def load_database(seed: int) -> tuple[sqlite3.Connection, dict[str, str]]:
    need(type(seed) is int and seed >= 0, "nonnegative declared seed")
    observed_pins = {name: file_hash(ROOT / name) for name in sorted(PINS)}
    need(observed_pins == {name: PINS[name] for name in sorted(PINS)},
         "exact primitive input pins")

    connection = sqlite3.connect("")
    create_schema(connection)
    with connection:
        insert_shuffled(
            connection,
            "INSERT INTO members VALUES(?,?,?,?)",
            _member_rows(), seed ^ 0x15,
        )
        insert_shuffled(
            connection,
            "INSERT INTO sheets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            _r204_rows(), seed ^ 0x21A,
        )
        insert_shuffled(
            connection,
            "INSERT INTO sheets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            _r211_rows(), seed ^ 0x21B,
        )
        insert_shuffled(
            connection,
            "INSERT INTO r211_discharges VALUES(?,?,?,?,?,?,?,?,?)",
            _r211_discharge_rows(), seed ^ 0x21C,
        )
        insert_shuffled(
            connection,
            "INSERT INTO features VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            _feature_rows(), seed ^ 0x26,
        )
    # Loading uses journal_mode=OFF only as a one-way construction speedup.
    # Switch to a rollback-capable in-memory journal before returning so the
    # attack harness can prove that every mutation is isolated and restored.
    journal_mode = connection.execute("PRAGMA journal_mode=MEMORY").fetchone()[0]
    need(str(journal_mode).lower() == "memory", "rollback-capable audit journal")
    return connection, observed_pins


def role_record(row: Sequence[str], role: str) -> dict[str, Any]:
    (
        sheet, mechanism, owner, shadow, component, source_sha, c26_sha,
    ) = row
    member = owner if role == "OWNER" else shadow
    return {
        "sheet_id": sheet,
        "mechanism": mechanism,
        "terminal": "SHEET_OWNER" if role == "OWNER" else "SHEET_SHADOW",
        "role": role,
        "member_id": member,
        "fresh_component_id": component,
        "source_sheet_row_sha256": source_sha,
        "C26_A1_row_sha256": c26_sha,
    }


def verify_database(
    connection: sqlite3.Connection, observed_pins: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    need(observed_pins == {name: PINS[name] for name in sorted(PINS)},
         "verification primitive pins")
    need(one(connection, "SELECT count(*) FROM members") == 502_204,
         "C15 relational universe")
    need(one(connection, "SELECT min(member_ordinal) FROM members") == 0
         and one(connection, "SELECT max(member_ordinal) FROM members") == 502_203,
         "C15 ordinal interval")
    need(one(connection, "SELECT count(*) FROM sheets") == 17_940,
         "sheet relational universe")
    exact_counter(
        connection, "SELECT source_class,count(*) FROM sheets GROUP BY source_class",
        {"R204": 224, "R211": 17_716}, "sheet source-class census",
    )
    need(one(connection, "SELECT count(*) FROM r211_discharges") == 17_716,
         "R211 discharge universe")
    need(one(connection, "SELECT count(*) FROM features") == 691_424,
         "C26 relational universe")
    need(one(connection, "SELECT min(feature_ordinal) FROM features") == 0
         and one(connection, "SELECT max(feature_ordinal) FROM features") == 691_423,
         "C26 ordinal interval")
    exact_counter(
        connection, "SELECT node_id,count(*) FROM features GROUP BY node_id",
        {"A1": 17_940, "A2": 62_152, "G1": 5_264, "G2A": 5_264,
         "G2B": 10_128, "R1": 295_340, "R2": 295_336},
        "C26 node census",
    )

    # This checks the declared C21 owner/shadow role binding and its component
    # handoff.  It intentionally does not infer half-open side inclusion from
    # those declarations; that separate physical-totality gate remains open.
    invalid_member_join = one(connection, """
      SELECT count(*) FROM sheets s
      LEFT JOIN members o ON o.member_id=s.owner_member_id
      LEFT JOIN members h ON h.member_id=s.shadow_member_id
      WHERE o.member_id IS NULL OR h.member_id IS NULL
         OR s.owner_member_id=s.shadow_member_id
         OR o.component_id<>s.owner_claimed_component_id
         OR h.component_id<>s.shadow_claimed_component_id
         OR o.component_id<>h.component_id
    """)
    need(invalid_member_join == 0, "exact C15 role and same-component join")

    need(one(connection, """
      SELECT count(*) FROM sheets
      WHERE (source_class='R204' AND (
        mechanism<>'R204_TARGET_REGULAR_GRAPH_SHEET' OR source_kernel<>'C21A'
        OR source_row_sha256<>physical_sheet_row_sha256
        OR discharge_theorem_sha256<>physical_theorem_sha256
        OR source_formal_credit<>? OR source_theorem_kind<>?
        OR source_strict_nonpromotion<>?))
      OR (source_class='R211' AND (
        mechanism<>'R211_ACTIVE_FACTOR_ZERO_SHEET' OR source_kernel<>'C21C'
        OR source_formal_credit<>? OR source_theorem_kind<>?
        OR source_strict_nonpromotion<>?))
    """, (
        canonical({"A1": 1, "A2": 0}).decode(),
        "A1_UNIQUE_TARGET_REGULAR_GRAPH_SHEET",
        canonical(NONPROMOTION_21).decode(),
        canonical({
            "A1_obligation_discharge": 0, "A2_obligation_discharge": 0,
            "self_contained_sheet_theorem_materialization": 1,
        }).decode(),
        "SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET",
        canonical(NONPROMOTION_21).decode(),
    )) == 0, "primitive sheet theorem class")

    # Exact materialized C21B -> C21C join; both anti-join directions close.
    need(one(connection, """
      SELECT count(*) FROM sheets s
      LEFT JOIN r211_discharges d ON d.sheet_id=s.sheet_id
      WHERE s.source_class='R211' AND (
        d.sheet_id IS NULL OR d.owner_member_id<>s.owner_member_id
        OR d.owner_claimed_component_id<>s.owner_claimed_component_id
        OR d.c21b_sheet_row_sha256<>s.physical_sheet_row_sha256
        OR d.theorem_kind<>'A1_R211_REGULAR_ACTIVE_FACTOR_ZERO_SHEET_DISCHARGE'
        OR d.formal_credit<>? OR d.strict_nonpromotion<>?)
    """, (
        canonical({"A1": 1, "A2": 0}).decode(),
        canonical(NONPROMOTION_21).decode(),
    )) == 0, "C21B-C21C materialized sheet join")
    need(one(connection, """
      SELECT count(*) FROM r211_discharges d
      LEFT JOIN sheets s ON s.sheet_id=d.sheet_id AND s.source_class='R211'
      WHERE s.sheet_id IS NULL
    """) == 0, "no orphan R211 discharge")

    # Exact C26 A1 exhaustion and source binding.  This independently proves
    # both no missing primitive sheet and no orphan A1 feature.
    need(one(connection, """
      SELECT count(*) FROM sheets s
      LEFT JOIN r211_discharges d ON d.sheet_id=s.sheet_id
      LEFT JOIN features f ON f.feature_id=s.sheet_id AND f.node_id='A1'
      WHERE f.feature_id IS NULL
         OR f.obligation_role<>'INDEPENDENT_DEFINITION_ROOT'
         OR f.depends_on_node_ids<>'[]'
         OR f.owner_member_id<>s.owner_member_id
         OR f.theorem_sha256<>CASE WHEN s.source_class='R204'
                                   THEN s.physical_theorem_sha256
                                   ELSE d.theorem_sha256 END
         OR f.source_kernel<>s.source_kernel
         OR f.source_row_sha256<>CASE WHEN s.source_class='R204'
                                     THEN s.physical_sheet_row_sha256
                                     ELSE d.source_row_sha256 END
         OR f.obligation_kind<>CASE WHEN s.source_class='R204'
                                    THEN 'A1_R204_TARGET_SHEET'
                                    ELSE 'A1_R211_OWNER_SHEET' END
         OR f.formal_credit<>?
         OR f.strict_nonpromotion<>?
      """, (
        canonical({
            "B1A_feature_obligation": 1, "dependent_feature_closure": 0,
            "source_free_definition_root": 1,
        }).decode(),
        canonical(NONPROMOTION_26).decode(),
    )) == 0, "C26 A1 exact primitive binding")
    need(one(connection, """
      SELECT count(*) FROM features f
      LEFT JOIN sheets s ON s.sheet_id=f.feature_id
      WHERE f.node_id='A1' AND s.sheet_id IS NULL
    """) == 0, "no orphan C26 A1 feature")

    joined = connection.execute("""
      SELECT s.sheet_id,s.mechanism,s.owner_member_id,s.shadow_member_id,
             o.component_id,
             CASE WHEN s.source_class='R204' THEN s.physical_sheet_row_sha256
                  ELSE d.source_row_sha256 END,
             f.c26_row_sha256
      FROM sheets s
      JOIN members o ON o.member_id=s.owner_member_id
      LEFT JOIN r211_discharges d ON d.sheet_id=s.sheet_id
      JOIN features f ON f.feature_id=s.sheet_id AND f.node_id='A1'
      ORDER BY s.sheet_id COLLATE BINARY
    """).fetchall()
    need(len(joined) == 17_940, "exact joined sheet count")

    records: list[dict[str, Any]] = []
    # Stream implementation sorts by sheet_id then role; ASCII OWNER precedes
    # SHADOW, so emit in precisely that canonical order.
    for row in joined:
        records.append(role_record(row, "OWNER"))
        records.append(role_record(row, "SHADOW"))
    need(len(records) == 35_880, "exact owner+shadow role rows")
    sequence = hashlib.sha256()
    roles: Counter[str] = Counter()
    mechanisms: Counter[str] = Counter()
    for record in records:
        sequence.update(canonical(record) + b"\n")
        roles[record["terminal"]] += 1
        mechanisms[record["mechanism"]] += 1
    need(roles == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940},
         "role terminal census")
    need(mechanisms == {
        "R204_TARGET_REGULAR_GRAPH_SHEET": 448,
        "R211_ACTIVE_FACTOR_ZERO_SHEET": 35_432,
    }, "mechanism role census")

    result = {
        "schema": "cm2.c27.sheet-owner-shadow-role-binding.zero-credit.v1",
        "status": "PASS_LOCAL_ZERO_CREDIT__SHEET_OWNER_SHADOW_ROLE_BINDING_AND_COMPONENT_HANDOFF_SUBGATE",
        "implementation": "ORDER_INDEPENDENT_SQLITE_C15_C21A_C21B_C21C_C26_RELATIONAL_ANTI_JOIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "primitive_sheet_count": 17_940,
        "candidate_role_row_count": 35_880,
        "terminal_census": dict(sorted(roles.items())),
        "mechanism_role_census": dict(sorted(mechanisms.items())),
        "candidate_rows_sha256": sequence.hexdigest(),
        "unresolved": 0,
        "missing_or_orphan_or_duplicate": 0,
        "owner_shadow_role_overlap_per_sheet": 0,
        "legal_cross_component_witness": 0,
        "owner_shadow_same_component": 17_940,
        "declared_owner_shadow_roles_consumed": True,
        "half_open_side_inclusion_independently_derived": False,
        "C26_explicit_shadow_node_present": False,
        "terminal_physical_totality": "REJECT_PENDING_SIDE_INCLUSION_DERIVATION_AND_SHADOW_CANDIDATE_EXHAUSTION",
        "closed_terminal_credit": 0,
        "input_sha256": observed_pins,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_PENDING_ALL_20_TERMINAL_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return result, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=30627001)
    arguments = parser.parse_args()
    connection, pins = load_database(arguments.seed)
    try:
        result, _ = verify_database(connection, pins)
    finally:
        connection.close()
    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        Failure, OSError, KeyError, TypeError, ValueError,
        json.JSONDecodeError, sqlite3.Error,
    ) as error:
        print("REJECT_SHEET_OWNER_SHADOW_SQLITE_ZERO_CREDIT:" + str(error),
              file=sys.stderr)
        raise SystemExit(2)
