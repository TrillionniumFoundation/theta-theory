#!/usr/bin/env python3
"""Dual-implementation and coherent-mutation harness for sheet role binding.

The harness runs the streamed and SQLite reconstructions at two declared
seeds, compares their order-independent candidate commitments, then attacks
the SQLite relational verifier inside rollback-only savepoints.  Passing this
harness closes only the declared role-binding/component-handoff subgate.  It
does not prove half-open side inclusion or terminal physical totality.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
STREAM = ROOT / "cm2_c27_sheet_owner_shadow_stream_probe.py"
SQLITE = ROOT / "cm2_c27_sheet_owner_shadow_sqlite_probe.py"


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


def load_sqlite_module() -> Any:
    spec = importlib.util.spec_from_file_location("sheet_role_sqlite_probe", SQLITE)
    need(spec is not None and spec.loader is not None, "SQLite probe module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_stream(seed: int) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(STREAM), "--seed", str(seed)],
        cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    need(completed.returncode == 0, f"stream exit:{seed}:{completed.stderr.decode()}")
    need(completed.stderr == b"", f"stream stderr:{seed}")
    lines = completed.stdout.splitlines()
    need(len(lines) == 1, f"stream one result:{seed}")
    result = json.loads(lines[0])
    claimed = result.pop("result_sha256")
    need(claimed == digest(result), f"stream result digest:{seed}")
    return result


def semantic_projection(result: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "primitive_sheet_count", "candidate_role_row_count", "terminal_census",
        "mechanism_role_census", "candidate_rows_sha256", "unresolved",
        "missing_or_orphan_or_duplicate", "owner_shadow_role_overlap_per_sheet",
        "legal_cross_component_witness", "owner_shadow_same_component",
        "declared_owner_shadow_roles_consumed",
        "half_open_side_inclusion_independently_derived",
        "C26_explicit_shadow_node_present", "terminal_physical_totality",
        "closed_terminal_credit", "input_sha256", "formal_credit",
        "C27_C28_C29", "CM2",
    )
    return {key: result[key] for key in keys}


def first_sheet(connection: sqlite3.Connection, source_class: str) -> str:
    row = connection.execute(
        "SELECT sheet_id FROM sheets WHERE source_class=? ORDER BY sheet_id LIMIT 1",
        (source_class,),
    ).fetchone()
    need(row is not None, "attack source sheet")
    return row[0]


def a01_delete_whole_r211_chain(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute("DELETE FROM features WHERE feature_id=?", (sheet,))
    c.execute("DELETE FROM r211_discharges WHERE sheet_id=?", (sheet,))
    c.execute("DELETE FROM sheets WHERE sheet_id=?", (sheet,))


def a02_add_coherent_fake_sheet_chain(c: sqlite3.Connection) -> None:
    source = first_sheet(c, "R211")
    fake = source + ":COHERENT_FAKE"
    c.execute(
        "INSERT INTO sheets SELECT ?,source_class,mechanism,owner_member_id,"
        "shadow_member_id,owner_claimed_component_id,shadow_claimed_component_id,"
        "physical_sheet_row_sha256,physical_theorem_sha256,source_kernel,"
        "source_row_sha256,discharge_theorem_sha256,source_formal_credit,"
        "source_theorem_kind,source_strict_nonpromotion FROM sheets WHERE sheet_id=?",
        (fake, source),
    )
    c.execute(
        "INSERT INTO r211_discharges SELECT ?,owner_member_id,"
        "owner_claimed_component_id,c21b_sheet_row_sha256,source_row_sha256,"
        "theorem_sha256,theorem_kind,formal_credit,strict_nonpromotion "
        "FROM r211_discharges WHERE sheet_id=?", (fake, source),
    )


def a03_owner_shadow_collapse(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute("""
      UPDATE sheets SET shadow_member_id=owner_member_id,
                        shadow_claimed_component_id=owner_claimed_component_id
      WHERE sheet_id=?
    """, (sheet,))


def a04_cross_component_shadow_rebind(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    owner_component = c.execute(
        "SELECT owner_claimed_component_id FROM sheets WHERE sheet_id=?", (sheet,),
    ).fetchone()[0]
    member, component = c.execute(
        "SELECT member_id,component_id FROM members WHERE component_id<>? "
        "ORDER BY member_id LIMIT 1", (owner_component,),
    ).fetchone()
    c.execute(
        "UPDATE sheets SET shadow_member_id=?,shadow_claimed_component_id=? "
        "WHERE sheet_id=?", (member, component, sheet),
    )


def a05_owner_component_coupled_forgery(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    forged = "round306c15-source-g-component:ATTACK_OWNER"
    c.execute(
        "UPDATE sheets SET owner_claimed_component_id=? WHERE sheet_id=?",
        (forged, sheet),
    )
    c.execute(
        "UPDATE r211_discharges SET owner_claimed_component_id=? WHERE sheet_id=?",
        (forged, sheet),
    )


def a06_shadow_component_forgery(c: sqlite3.Connection) -> None:
    c.execute(
        "UPDATE sheets SET shadow_claimed_component_id='ATTACK_SHADOW_COMPONENT' "
        "WHERE sheet_id=(SELECT sheet_id FROM sheets ORDER BY sheet_id LIMIT 1)"
    )


def a07_discharge_rekey(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute(
        "UPDATE r211_discharges SET sheet_id=? WHERE sheet_id=?",
        (sheet + ":DETACHED", sheet),
    )


def a08_c21b_binding_flip(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute(
        "UPDATE r211_discharges SET c21b_sheet_row_sha256=? WHERE sheet_id=?",
        ("0" * 64, sheet),
    )


def a09_discharge_owner_flip(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute("""
      UPDATE r211_discharges
      SET owner_member_id=(SELECT shadow_member_id FROM sheets WHERE sheet_id=?)
      WHERE sheet_id=?
    """, (sheet, sheet))


def a10_a1_to_a2_coherent_reclassify(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R204")
    c.execute("""
      UPDATE features SET node_id='A2',
        obligation_kind='A2_R204_SOURCE_TARGET_CURVE',
        obligation_role='DEPENDENT_INCIDENCE_CLOSURE',
        depends_on_node_ids='["A1"]'
      WHERE feature_id=?
    """, (sheet,))


def a11_c26_source_rewrite(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute("""
      UPDATE features SET source_kernel='C21B',
        source_ledger='ATTACK_COHERENT_LEDGER'
      WHERE feature_id=?
    """, (sheet,))


def a12_c26_theorem_source_rewrite(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute(
        "UPDATE features SET theorem_sha256=?,source_row_sha256=? WHERE feature_id=?",
        ("1" * 64, "2" * 64, sheet),
    )


def a13_r204_linked_theorem_class_rewrite(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R204")
    forged = "3" * 64
    c.execute("""
      UPDATE sheets SET source_theorem_kind='ATTACK_ALTERNATE_SHEET_THEOREM',
        physical_theorem_sha256=?,discharge_theorem_sha256=? WHERE sheet_id=?
    """, (forged, forged, sheet))
    c.execute(
        "UPDATE features SET theorem_sha256=? WHERE feature_id=?", (forged, sheet),
    )


def a14_r211_linked_physical_rewrite(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    forged = "4" * 64
    c.execute("""
      UPDATE sheets SET source_theorem_kind='ATTACK_R211_THEOREM',
                        physical_sheet_row_sha256=? WHERE sheet_id=?
    """, (forged, sheet))
    c.execute(
        "UPDATE r211_discharges SET c21b_sheet_row_sha256=? WHERE sheet_id=?",
        (forged, sheet),
    )


def a15_mechanism_relabel(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R204")
    c.execute(
        "UPDATE sheets SET mechanism='R211_ACTIVE_FACTOR_ZERO_SHEET' WHERE sheet_id=?",
        (sheet,),
    )


def a16_orphan_a1_rekey(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute(
        "UPDATE features SET feature_id=? WHERE feature_id=?",
        (sheet + ":ORPHAN_A1", sheet),
    )


def a17_nonpromotion_escalation(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R204")
    c.execute(
        "UPDATE sheets SET source_strict_nonpromotion='{}' WHERE sheet_id=?",
        (sheet,),
    )
    c.execute(
        "UPDATE features SET strict_nonpromotion='{}' WHERE feature_id=?",
        (sheet,),
    )


def a18_formal_credit_escalation(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R211")
    c.execute(
        "UPDATE sheets SET source_formal_credit='{\"A1_obligation_discharge\":1}' "
        "WHERE sheet_id=?", (sheet,),
    )
    c.execute(
        "UPDATE r211_discharges SET formal_credit='{\"A1\":2}' WHERE sheet_id=?",
        (sheet,),
    )


def a19_dependency_cycle(c: sqlite3.Connection) -> None:
    sheet = first_sheet(c, "R204")
    c.execute("""
      UPDATE features SET obligation_role='DEPENDENT_INCIDENCE_CLOSURE',
                          depends_on_node_ids='["A1"]'
      WHERE feature_id=?
    """, (sheet,))


def a20_extra_orphan_discharge(c: sqlite3.Connection) -> None:
    source = first_sheet(c, "R211")
    c.execute(
        "INSERT INTO r211_discharges SELECT ?,owner_member_id,"
        "owner_claimed_component_id,c21b_sheet_row_sha256,source_row_sha256,"
        "theorem_sha256,theorem_kind,formal_credit,strict_nonpromotion "
        "FROM r211_discharges WHERE sheet_id=?",
        (source + ":ORPHAN_DISCHARGE", source),
    )


ATTACKS: list[tuple[str, Callable[[sqlite3.Connection], None]]] = [
    ("A01_DELETE_WHOLE_R211_CHAIN", a01_delete_whole_r211_chain),
    ("A02_ADD_COHERENT_FAKE_SHEET_CHAIN", a02_add_coherent_fake_sheet_chain),
    ("A03_OWNER_SHADOW_ROLE_COLLAPSE", a03_owner_shadow_collapse),
    ("A04_CROSS_COMPONENT_SHADOW_REBIND", a04_cross_component_shadow_rebind),
    ("A05_OWNER_COMPONENT_COUPLED_FORGERY", a05_owner_component_coupled_forgery),
    ("A06_SHADOW_COMPONENT_FORGERY", a06_shadow_component_forgery),
    ("A07_R211_DISCHARGE_REKEY", a07_discharge_rekey),
    ("A08_C21B_BINDING_FLIP", a08_c21b_binding_flip),
    ("A09_DISCHARGE_OWNER_FLIP", a09_discharge_owner_flip),
    ("A10_A1_TO_A2_COHERENT_RECLASSIFY", a10_a1_to_a2_coherent_reclassify),
    ("A11_C26_SOURCE_KERNEL_LEDGER_REWRITE", a11_c26_source_rewrite),
    ("A12_C26_THEOREM_SOURCE_REWRITE", a12_c26_theorem_source_rewrite),
    ("A13_R204_LINKED_THEOREM_CLASS_REWRITE", a13_r204_linked_theorem_class_rewrite),
    ("A14_R211_LINKED_PHYSICAL_REWRITE", a14_r211_linked_physical_rewrite),
    ("A15_MECHANISM_RELABEL", a15_mechanism_relabel),
    ("A16_ORPHAN_A1_REKEY", a16_orphan_a1_rekey),
    ("A17_NONPROMOTION_ESCALATION", a17_nonpromotion_escalation),
    ("A18_FORMAL_CREDIT_ESCALATION", a18_formal_credit_escalation),
    ("A19_A1_DEPENDENCY_CYCLE", a19_dependency_cycle),
    ("A20_EXTRA_ORPHAN_DISCHARGE", a20_extra_orphan_discharge),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-a", type=int, default=30627001)
    parser.add_argument("--seed-b", type=int, default=30627991)
    arguments = parser.parse_args()
    need(arguments.seed_a >= 0 and arguments.seed_b >= 0
         and arguments.seed_a != arguments.seed_b, "two distinct nonnegative seeds")
    module = load_sqlite_module()

    stream_a = run_stream(arguments.seed_a)
    stream_b = run_stream(arguments.seed_b)
    need(canonical(stream_a) == canonical(stream_b), "stream double-seed identity")

    connection_a, pins_a = module.load_database(arguments.seed_a)
    connection_b: sqlite3.Connection | None = None
    try:
        sqlite_a, _ = module.verify_database(connection_a, pins_a)
        connection_b, pins_b = module.load_database(arguments.seed_b)
        sqlite_b, _ = module.verify_database(connection_b, pins_b)
        need(canonical(sqlite_a) == canonical(sqlite_b),
             "SQLite double-seed identity")
        need(semantic_projection(stream_a) == semantic_projection(sqlite_a),
             "cross-implementation exact semantic projection")

        attack_rows: list[dict[str, Any]] = []
        for ordinal, (attack_id, mutation) in enumerate(ATTACKS):
            boundaries: list[str] = []
            for seed_label, connection, pins, pristine in (
                ("A", connection_a, pins_a, sqlite_a),
                ("B", connection_b, pins_b, sqlite_b),
            ):
                savepoint = f"attack_{ordinal}_{seed_label}"
                connection.execute(f"SAVEPOINT {savepoint}")
                rejected = False
                boundary = ""
                try:
                    mutation(connection)
                    module.verify_database(connection, pins)
                except (
                    module.Failure, sqlite3.Error, KeyError, TypeError, ValueError,
                ) as error:
                    rejected = True
                    boundary = type(error).__name__ + ":" + str(error)
                finally:
                    connection.execute(f"ROLLBACK TO {savepoint}")
                    connection.execute(f"RELEASE {savepoint}")
                need(rejected, "attack escaped:" + attack_id + ":seed-" + seed_label)
                restored, _ = module.verify_database(connection, pins)
                need(canonical(restored) == canonical(pristine),
                     "rollback restored pristine database:" + attack_id
                     + ":seed-" + seed_label)
                boundaries.append(boundary)
            need(boundaries[0] == boundaries[1],
                 "attack rejection boundary seed invariance:" + attack_id)
            row = {
                "attack_id": attack_id,
                "ordinal": ordinal,
                "rejected": True,
                "rejected_at_both_seeds": True,
                "rejection_boundary": boundaries[0],
            }
            attack_rows.append({**row, "row_sha256": digest(row)})

        result = {
            "schema": "cm2.c27.sheet-owner-shadow-role-binding-attack.v1",
            "status": "PASS_LOCAL_ZERO_CREDIT__DUAL_IMPLEMENTATION_DOUBLE_SEED_AND_20_COHERENT_ATTACKS",
            "stream_double_seed_byte_identical": True,
            "sqlite_double_seed_byte_identical": True,
            "cross_implementation_candidate_commitment_identical": True,
            "candidate_rows_sha256": sqlite_a["candidate_rows_sha256"],
            "candidate_role_row_count": 35_880,
            "primitive_sheet_count": 17_940,
            "attack_count": len(attack_rows),
            "all_attacks_rejected": True,
            "all_attacks_rejected_at_both_seeds": True,
            "rollback_restored_pristine_after_every_attack": True,
            "attack_rows": attack_rows,
            "attacks_sha256": digest(attack_rows),
            "role_binding_component_handoff_subgate": "PASS_LOCAL_ZERO_CREDIT",
            "half_open_side_inclusion_independently_derived": False,
            "terminal_physical_totality": "REJECT_PENDING_SIDE_INCLUSION_DERIVATION_AND_SHADOW_CANDIDATE_EXHAUSTION",
            "closed_terminal_credit": 0,
            "formal_credit": 0,
            "C27_C28_C29": "REJECT_PENDING_ALL_20_TERMINAL_GATE",
            "CM2": "NO-GO_FOR_CLAIM",
        }
    finally:
        connection_a.close()
        if connection_b is not None:
            connection_b.close()

    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        Failure, OSError, KeyError, TypeError, ValueError,
        json.JSONDecodeError, sqlite3.Error,
    ) as error:
        print("REJECT_SHEET_OWNER_SHADOW_ATTACK_HARNESS:" + str(error),
              file=sys.stderr)
        raise SystemExit(2)
