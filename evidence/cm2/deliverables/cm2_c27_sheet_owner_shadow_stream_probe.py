#!/usr/bin/env python3
"""C27-independent owner/shadow sheet-role binding probe.

The candidate universe is reconstructed from the sealed C21A/C21B sheet
theorems, joined to C15 member/component identities, and independently
exhausted by the C26 A1 feature universe.  It does not derive the half-open
side inclusion predicate from the sheet equations, and C26 has no shadow
node, so it is not a terminal-totality proof.  No Round306C27 source or edge
ledger is read.  This is a local zero-credit semantic subgate only.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterator


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


def role_record(
    *, sheet_id: str, mechanism: str, role: str, member_id: str,
    component_id: str, source_row_sha256: str, c26_row_sha256: str,
) -> dict[str, Any]:
    return {
        "sheet_id": sheet_id,
        "mechanism": mechanism,
        "terminal": "SHEET_OWNER" if role == "OWNER" else "SHEET_SHADOW",
        "role": role,
        "member_id": member_id,
        "fresh_component_id": component_id,
        "source_sheet_row_sha256": source_row_sha256,
        "C26_A1_row_sha256": c26_row_sha256,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=30627001)
    arguments = parser.parse_args()
    need(arguments.seed >= 0, "nonnegative declared seed")

    observed_pins = {name: file_hash(ROOT / name) for name in sorted(PINS)}
    need(observed_pins == {name: PINS[name] for name in sorted(PINS)},
         "exact primitive input pins")

    members: dict[str, tuple[str, str]] = {}
    for ordinal, row in enumerate(checked_rows(C15)):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        member = row["registry_member_id"]
        need(member not in members, "unique C15 member")
        members[member] = (row["fresh_component_id"], row["row_sha256"])
    need(len(members) == 502_204, "C15 complete universe")

    # sheet_id -> primitive sheet role data
    sheets: dict[str, dict[str, Any]] = {}
    c21a_kinds: Counter[str] = Counter()
    for row in checked_rows(C21A):
        kind = row["obligation_kind"]
        c21a_kinds[kind] += 1
        if kind != "A1_R204_TARGET_SHEET":
            continue
        sheet = row["feature_row_id"]
        owner = row["owner_member_id"]
        shadow = row["shadow_member_id"]
        need(sheet not in sheets and owner != shadow, "unique R204 sheet roles")
        need(owner in members and shadow in members, "R204 role members in C15")
        owner_component = members[owner][0]
        shadow_component = members[shadow][0]
        need(
            owner_component == row["owner_fresh_component_id"]
            and shadow_component == row["shadow_fresh_component_id"],
            "R204 exact C15 component join",
        )
        need(owner_component == shadow_component,
             "R204 owner/shadow same physical component")
        need(
            row["formal_credit"] == {"A1": 1, "A2": 0}
            and row["feature_theorem_ast"]["kind"]
            == "A1_UNIQUE_TARGET_REGULAR_GRAPH_SHEET",
            "R204 A1 physical sheet theorem",
        )
        sheets[sheet] = {
            "mechanism": "R204_TARGET_REGULAR_GRAPH_SHEET",
            "owner": owner,
            "shadow": shadow,
            "component": owner_component,
            "physical_sheet_row_sha256": row["row_sha256"],
            "source_row_sha256": row["row_sha256"],
            "theorem_sha256": row["feature_theorem_ast_sha256"],
            "source_kernel": "C21A",
        }
    need(c21a_kinds == {
        "A1_R204_TARGET_SHEET": 224,
        "A2_R204_SOURCE_TARGET_CURVE": 504,
        "A2_R204_SOURCE_TARGET_ENDPOINT": 280,
    }, "C21A complete dimensional partition")

    c21b_count = 0
    for row in checked_rows(C21B):
        c21b_count += 1
        sheet = row["R211_sheet_row_id"]
        owner = row["owner_member_id"]
        shadow = row["shadow_member_id"]
        need(sheet not in sheets and owner != shadow, "unique R211 sheet roles")
        need(owner in members and shadow in members, "R211 role members in C15")
        owner_component = members[owner][0]
        shadow_component = members[shadow][0]
        need(
            owner_component == row["owner_fresh_component_id"]
            and shadow_component == row["shadow_fresh_component_id"],
            "R211 exact C15 component join",
        )
        need(owner_component == shadow_component,
             "R211 owner/shadow same physical component")
        need(
            row["formal_credit"] == {
                "A1_obligation_discharge": 0,
                "A2_obligation_discharge": 0,
                "self_contained_sheet_theorem_materialization": 1,
            }
            and row["theorem_ast"]["kind"]
            == "SELF_CONTAINED_REGULAR_R211_ACTIVE_FACTOR_ZERO_SHEET",
            "R211 materialized physical sheet theorem",
        )
        sheets[sheet] = {
            "mechanism": "R211_ACTIVE_FACTOR_ZERO_SHEET",
            "owner": owner,
            "shadow": shadow,
            "component": owner_component,
            "physical_sheet_row_sha256": row["row_sha256"],
            "source_row_sha256": None,
            "theorem_sha256": None,
            "source_kernel": "C21C",
        }
    need(c21b_count == 17_716 and len(sheets) == 17_940,
         "complete primitive sheet universe")

    c21c_kinds: Counter[str] = Counter()
    c21c_a1_seen: set[str] = set()
    for row in checked_rows(C21C):
        kind = row["obligation_kind"]
        c21c_kinds[kind] += 1
        if kind != "A1_R211_OWNER_SHEET":
            continue
        sheet = row["feature_row_id"]
        need(sheet in sheets and sheet not in c21c_a1_seen,
             "unique C21C A1 sheet discharge")
        source = sheets[sheet]
        need(
            source["source_kernel"] == "C21C"
            and row["owner_member_id"] == source["owner"]
            and row["owner_fresh_component_id"] == source["component"]
            and row["source_bindings"]["C21b_sheet_theorem_row_sha256"]
            == source["physical_sheet_row_sha256"]
            and row["theorem_ast"]["kind"]
            == "A1_R211_REGULAR_ACTIVE_FACTOR_ZERO_SHEET_DISCHARGE"
            and row["formal_credit"] == {"A1": 1, "A2": 0},
            "C21B to C21C materialized A1 join",
        )
        source["source_row_sha256"] = row["row_sha256"]
        source["theorem_sha256"] = row["theorem_ast_sha256"]
        c21c_a1_seen.add(sheet)
    need(c21c_kinds == {
        "A1_R211_OWNER_SHEET": 17_716,
        "A2_R211_OWNER_CURVE": 20_456,
        "A2_R211_OWNER_ENDPOINT": 40_912,
    }, "C21C complete dimensional partition")
    need(len(c21c_a1_seen) == 17_716, "all R211 sheets discharged")

    c26_nodes: Counter[str] = Counter()
    c26_kinds: Counter[str] = Counter()
    seen_features: set[str] = set()
    records: list[dict[str, Any]] = []
    a1_count = 0
    for ordinal, row in enumerate(checked_rows(C26)):
        need(row["feature_ordinal"] == ordinal, "C26 ordinal")
        feature = row["feature_id"]
        need(feature not in seen_features, "C26 unique feature")
        seen_features.add(feature)
        c26_nodes[row["node_id"]] += 1
        c26_kinds[row["obligation_kind"]] += 1
        if row["node_id"] != "A1":
            continue
        a1_count += 1
        need(feature in sheets, "C26 A1 has primitive sheet")
        source = sheets[feature]
        need(
            row["obligation_kind"] in {
                "A1_R204_TARGET_SHEET", "A1_R211_OWNER_SHEET"
            }
            and row["obligation_role"] == "INDEPENDENT_DEFINITION_ROOT"
            and row["depends_on_node_ids"] == []
            and row["owner_member_id"] == source["owner"]
            and row["definition_or_dependency_theorem_ast_sha256"]
            == source["theorem_sha256"]
            and row["source_bindings"]["source_kernel"]
            == source["source_kernel"]
            and row["source_bindings"]["source_row_sha256"]
            == source["source_row_sha256"],
            "C26 A1 exact primitive sheet binding",
        )
        records.append(role_record(
            sheet_id=feature, mechanism=source["mechanism"], role="OWNER",
            member_id=source["owner"], component_id=source["component"],
            source_row_sha256=source["source_row_sha256"],
            c26_row_sha256=row["row_sha256"],
        ))
        records.append(role_record(
            sheet_id=feature, mechanism=source["mechanism"], role="SHADOW",
            member_id=source["shadow"], component_id=source["component"],
            source_row_sha256=source["source_row_sha256"],
            c26_row_sha256=row["row_sha256"],
        ))

    need(len(seen_features) == 691_424 and a1_count == 17_940,
         "C26 complete A1 exhaustion")
    need(c26_nodes == {
        "A1": 17_940, "A2": 62_152, "G1": 5_264, "G2A": 5_264,
        "G2B": 10_128, "R1": 295_340, "R2": 295_336,
    }, "C26 node census")
    need(set(sheets) == {
        row["sheet_id"] for row in records if row["role"] == "OWNER"
    }, "no missing/orphan primitive sheet")
    need(len(records) == 35_880, "exact owner+shadow role rows")

    # Cross-implementation commitment is independent of source traversal.
    records.sort(key=lambda row: (row["sheet_id"].encode(), row["role"].encode()))
    sequence = hashlib.sha256()
    role_census: Counter[str] = Counter()
    mechanism_census: Counter[str] = Counter()
    for record in records:
        sequence.update(canonical(record) + b"\n")
        role_census[record["terminal"]] += 1
        mechanism_census[record["mechanism"]] += 1
    need(role_census == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940},
         "role terminal census")
    need(mechanism_census == {
        "R204_TARGET_REGULAR_GRAPH_SHEET": 448,
        "R211_ACTIVE_FACTOR_ZERO_SHEET": 35_432,
    }, "mechanism role census")

    result = {
        "schema": "cm2.c27.sheet-owner-shadow-role-binding.zero-credit.v1",
        "status": "PASS_LOCAL_ZERO_CREDIT__SHEET_OWNER_SHADOW_ROLE_BINDING_AND_COMPONENT_HANDOFF_SUBGATE",
        "implementation": "STREAMED_C15_C21A_C21B_C21C_C26_ANTI_JOIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "primitive_sheet_count": 17_940,
        "candidate_role_row_count": 35_880,
        "terminal_census": dict(sorted(role_census.items())),
        "mechanism_role_census": dict(sorted(mechanism_census.items())),
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
    print(canonical({**result, "result_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_SHEET_OWNER_SHADOW_ZERO_CREDIT:" + str(error), file=sys.stderr)
        raise SystemExit(2)
