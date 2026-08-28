#!/usr/bin/env python3
"""C27-independent RETAINED_CONTINUATION physical-totality stream gate.

The candidate universe is reconstructed from the complete C20D typed-nonfull
kernel, not from a C27 family table.  A retained continuation is selected iff
its typed open box and its C20A owner open box have disjoint interiors and
share the complete positive-t face with identical chart, p interval and s
interval.  C15/C25/C26 are then consumed only to bind the materialized
geometry to the current owner/component and transition-ready handle.

This is a local zero-credit gate.  It cannot authorize C27/C28/C29 until the
complete primitive twenty-terminal gate is closed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.c27.retained-continuation-physical-totality-zero-credit.v1"

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

FULL_COUNTS = {C15: 502_204, C20A: 126_468, C20D: 2_520,
               C20D_I2: 183_572, R295A: 276,
               C25M: 502_204, C25R: 549_616, C26H: 549_616}
SOURCE_SEMANTIC_CENSUS = {
    "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_SUBCOVER": 720,
    "EXACT_T2_P_S_EXISTING_OCCURRENCE_SUBCOVER_CELL": 1_524,
    "ADJACENT_POSITIVE_T_CONTINUATION": 276,
}


class GateFailure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise GateFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            state.update(block)
    return state.hexdigest()


def rows(name: str) -> Iterable[dict[str, Any]]:
    with gzip.open(HERE / name, "rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "newline:" + name)
            value = json.loads(raw[:-1])
            need(isinstance(value, dict), "object:" + name)
            yield value


def check_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    need(isinstance(claimed, str) and claimed == digest(
        {key: value for key, value in row.items() if key != "row_sha256"}
    ), "row closure:" + label)


def rational_box(ast: dict[str, Any], label: str) -> tuple[str, str, tuple[Fraction, ...]]:
    need(ast.get("kind") == "OPEN_RATIONAL_BOX", label + ":open box")
    coordinates = ast.get("coordinates")
    need(coordinates in (["t", "p", "s"], ["t^2", "p", "s"]),
         label + ":coordinates")
    bounds = ast.get("bounds")
    need(isinstance(bounds, list) and len(bounds) == 6, label + ":six bounds")
    values = tuple(Fraction(value) for value in bounds)
    need(values[0] < values[1] and values[2] < values[3] and values[4] < values[5],
         label + ":positive widths")
    volume = (values[1] - values[0]) * (values[3] - values[2]) * (values[5] - values[4])
    need(volume == Fraction(ast["exact_coordinate_volume"] if "exact_coordinate_volume" in ast
                            else ast["exact_volume"]), label + ":volume")
    chart = ast.get("coordinate_chart")
    need(chart in {"G:E", "G:N", "G:W", "G:S"}, label + ":chart")
    return chart, coordinates[0], values


def is_positive_t_full_face_adjacency(source: dict[str, Any], owner: dict[str, Any]) -> tuple[bool, str]:
    source_chart, source_t, s = rational_box(source, "typed source")
    owner_chart, owner_t, o = rational_box(owner, "owner")
    face_key = digest({
        "coordinate_chart": source_chart,
        "t": str(s[1]),
        "p": [str(s[2]), str(s[3])],
        "s": [str(s[4]), str(s[5])],
    })
    adjacent = (
        source_t == owner_t == "t"
        and source_chart == owner_chart
        and s[2:6] == o[2:6]
        and s[0] == 0
        and s[1] == o[0]
    )
    return adjacent, face_key


def build(seed: int) -> dict[str, Any]:
    need(type(seed) is int, "integer seed")
    for name, expected in PINS.items():
        path = HERE / name
        need(path.is_file() and not path.is_symlink(), "regular input:" + name)
        need(file_hash(path) == expected, "input pin:" + name)

    owners: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(rows(C20A)):
        need(row.get("ordinal") == ordinal, "C20A ordinal")
        check_row(row, "C20A")
        member = row.get("member_id")
        need(isinstance(member, str) and member not in owners, "C20A unique member")
        need(row.get("support_ast_sha256") == digest(row.get("support_ast")), "C20A AST closure")
        owners[member] = row
    need(len(owners) == FULL_COUNTS[C20A], "C20A exhaustion")

    c20d_all: dict[str, dict[str, Any]] = {}
    selected: dict[str, tuple[dict[str, Any], str]] = {}
    semantic_census: Counter[str] = Counter()
    relation_census: Counter[str] = Counter()
    chart_census: Counter[str] = Counter()
    geometric_adjacency_count = 0
    for ordinal, row in enumerate(rows(C20D)):
        need(row.get("ordinal") == ordinal, "C20D ordinal")
        check_row(row, "C20D")
        representation = row.get("representation_id")
        need(isinstance(representation, str) and representation not in c20d_all,
             "C20D unique representation")
        c20d_all[representation] = row
        semantic = row.get("source_semantics")
        relation = row.get("exact_relation_to_owner_support")
        semantic_census[semantic] += 1
        relation_census[relation] += 1
        owner = owners.get(row.get("owner_member_id"))
        need(owner is not None, "C20D owner in complete C20A")
        need(row.get("fresh_component_id") == owner.get("fresh_component_id"), "C20D/C20A component")
        need(row.get("owner_support_ast_sha256") == owner.get("support_ast_sha256"), "C20D/C20A owner support")
        need(row.get("typed_source_support_ast_sha256") == digest(row.get("typed_source_support_ast")),
             "C20D typed-source AST closure")
        adjacent, face_key = is_positive_t_full_face_adjacency(
            row["typed_source_support_ast"], owner["support_ast"]
        )
        if adjacent:
            geometric_adjacency_count += 1
            need(semantic == "ADJACENT_POSITIVE_T_CONTINUATION", "adjacency semantic iff")
            need(relation == "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE",
                 "adjacency relation iff")
            need(row.get("negative_disposition") ==
                 "NOT_A_COMPLETE_SUPPORT_REPRESENTATION__RETAIN_AS_TYPED_NONFULL_ALIAS_HANDLE",
                 "retained typed-nonfull disposition")
            chart_census[row["typed_source_support_ast"]["coordinate_chart"]] += 1
            selected[representation] = (row, face_key)
        else:
            need(semantic != "ADJACENT_POSITIVE_T_CONTINUATION", "nonadjacency semantic iff")
            need(relation == "STRICT_SUBCOVER_OF_OWNER_SUPPORT", "nonadjacency strict subcover")
    need(len(c20d_all) == FULL_COUNTS[C20D], "C20D exhaustion")
    need(dict(semantic_census) == SOURCE_SEMANTIC_CENSUS, "C20D semantic partition")
    need(relation_census == {
        "STRICT_SUBCOVER_OF_OWNER_SUPPORT": 2_244,
        "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE": 276,
    }, "C20D relation partition")
    need(geometric_adjacency_count == len(selected) == 276, "retained geometry denominator")
    need(chart_census == {"G:E": 69, "G:N": 69, "G:S": 69, "G:W": 69},
         "retained chart balance")

    # Reconstruct the same-origin/no-event identity route independently of
    # the collapsed C20D label: I2 binds each representation to one R295A
    # material row, and R295A contains the two exact adjacent boxes.
    i2_selected: dict[str, dict[str, Any]] = {}
    i2_count = 0
    for row in rows(C20D_I2):
        i2_count += 1
        check_row(row, "I2")
        if row.get("representation_semantics") != "ADJACENT_POSITIVE_T_CONTINUATION":
            continue
        representation = row.get("representation_id")
        need(representation not in i2_selected, "I2 selected unique")
        need(row.get("source_kind") == "R295A_ROUND179_ADJACENT_POSITIVE_T_CONTINUATION",
             "I2 source kind")
        need(row.get("coverage_semantics") ==
             "ALIAS_OR_SUBCOVER_EVIDENCE_ONLY__COMPLETE_SUPPORT_SET_EQUALITY_NOT_PROVED",
             "I2 coverage semantics")
        need(row.get("representation_role") == "PRESERVED_ALIAS_HANDLE", "I2 role")
        i2_selected[representation] = row
    need(i2_count == FULL_COUNTS[C20D_I2], "I2 exhaustion")
    need(set(i2_selected) == set(selected), "I2 retained representation totality")

    with gzip.open(HERE / R295A, "rt", encoding="utf-8") as stream:
        r295_top = json.load(stream)
    need(r295_top.get("row_count") == 276 and r295_top.get("every_row_closed_by_own_SHA256") is True,
         "R295A top contract")
    r295_rows: dict[str, dict[str, Any]] = {}
    for row in r295_top.get("rows", []):
        check_row(row, "R295A")
        row_id = row.get("Round295A_retained_continuation_alias_row_id")
        need(isinstance(row_id, str) and row_id not in r295_rows, "R295A unique row id")
        r295_rows[row_id] = row
    need(len(r295_rows) == FULL_COUNTS[R295A], "R295A row exhaustion")
    consumed_r295: set[str] = set()
    for representation, (source, _) in selected.items():
        index = i2_selected[representation]
        row_id = index["source_row_id"]
        r295 = r295_rows.get(row_id)
        need(r295 is not None and row_id not in consumed_r295, "R295A one-to-one cover")
        consumed_r295.add(row_id)
        owner = owners[source["owner_member_id"]]
        need(index["source_row_sha256"] == r295["row_sha256"] == source["source_row_sha256"],
             "C20D/I2/R295A source-row join")
        need(index["owner_member_id"] == r295["target_Round294_registry_occurrence_id"] ==
             source["owner_member_id"], "C20D/I2/R295A owner join")
        need(r295["retained_positive_t_open_box"] == source["typed_source_support_ast"]["bounds"],
             "R295A retained box join")
        need(r295["resolved_sibling_open_box"] == owner["support_ast"]["bounds"],
             "R295A sibling box join")
        need(r295["source_chart"] == owner["support_ast"]["coordinate_chart"],
             "R295A chart join")
        need(r295["exact_full_face_shared"] is True and r295["exact_volume_conserved"] is True,
             "R295A exact gluing")
        need(r295["same_origin_unique_index1_sibling"] is True and
             r295["signature_or_box_equality_used_as_identity_basis"] is False and
             r295["symmetry_used_as_identity_basis"] is False,
             "R295A independent same-origin identity")
        need(r295["complete_Round294_registry_positive_volume_overlap_count"] == 0 and
             r295["undesignated_positive_volume_overlap_count"] == 0,
             "R295A no positive-volume overlap")
        need(r295["formal_occurrence_ID_issued"] is False and
             r295["formal_identity_collapse_credit"] == 0,
             "R295A truthful noncollapse")
    need(consumed_r295 == set(r295_rows), "R295A exact consumption")

    selected_owners = {row[0]["owner_member_id"] for row in selected.values()}
    c15: dict[str, dict[str, Any]] = {}
    c25m: dict[str, dict[str, Any]] = {}
    for ordinal, row in enumerate(rows(C15)):
        need(row.get("member_ordinal") == ordinal, "C15 ordinal")
        member = row.get("registry_member_id")
        if member in selected_owners:
            check_row(row, "selected C15")
            need(member not in c15, "selected C15 unique")
            c15[member] = row
    for ordinal, row in enumerate(rows(C25M)):
        need(row.get("member_ordinal") == ordinal, "C25M ordinal")
        member = row.get("member_id")
        if member in selected_owners:
            check_row(row, "selected C25M")
            need(member not in c25m, "selected C25M unique")
            c25m[member] = row
    need(set(c15) == selected_owners == set(c25m), "current owner cover")

    c25r: dict[str, dict[str, Any]] = {}
    c26h: dict[str, dict[str, Any]] = {}
    r_iter = iter(rows(C25R))
    h_iter = iter(rows(C26H))
    for ordinal in range(FULL_COUNTS[C25R]):
        rep = next(r_iter, None)
        handle = next(h_iter, None)
        need(rep is not None and handle is not None, "C25R/C26H length")
        need(rep.get("representation_ordinal") == handle.get("handle_ordinal") == ordinal,
             "C25R/C26H ordinal lockstep")
        need(rep.get("representation_id") == handle.get("representation_id"),
             "C25R/C26H id lockstep")
        need(handle.get("source_bindings", {}).get("C25_representation_row_sha256") == rep.get("row_sha256"),
             "C25R/C26H row lockstep")
        representation = rep.get("representation_id")
        if representation in selected:
            check_row(rep, "selected C25R")
            check_row(handle, "selected C26H")
            c25r[representation] = rep
            c26h[representation] = handle
    need(next(r_iter, None) is None and next(h_iter, None) is None, "C25R/C26H exhaustion")
    need(set(c25r) == set(selected) == set(c26h), "selected handle cover")

    commitments: list[tuple[str, str]] = []
    face_keys: set[str] = set()
    owner_ids: set[str] = set()
    for representation, (source, face_key) in selected.items():
        owner_id = source["owner_member_id"]
        owner = owners[owner_id]
        current = c15[owner_id]
        member = c25m[owner_id]
        rep = c25r[representation]
        handle = c26h[representation]
        need(owner_id not in owner_ids and face_key not in face_keys,
             "unique owner and shared-face assignment")
        owner_ids.add(owner_id); face_keys.add(face_key)
        need(current["fresh_component_id"] == member["fresh_component_id"] ==
             rep["fresh_component_id"] == handle["fresh_component_id"] == source["fresh_component_id"],
             "component join")
        need(current["base_root_id"] == member["base_root_id"] == rep["base_root_id"] == handle["base_root_id"],
             "base-root join")
        need(current["official_key_id"] == member["official_key_id"] == rep["official_key_id"] == handle["official_key_id"],
             "official-key join")
        need(member["normalized_support_ast_sha256"] == owner["support_ast_sha256"],
             "C25M/C20A owner support")
        need(member["source_bindings"]["support_kernel"] == "C20A" and
             member["source_bindings"]["support_kernel_row_sha256"] == owner["row_sha256"],
             "C25M C20A binding")
        need(member["source_bindings"]["C15_member_row_sha256"] == current["row_sha256"],
             "C25M C15 binding")
        need(rep["source_bindings"]["semantic_kernel"] == "C20D" and
             rep["source_bindings"]["semantic_kernel_row_sha256"] == source["row_sha256"],
             "C25R C20D binding")
        need(rep["owner_member_id"] == handle["owner_member_id"] == owner_id,
             "representation owner join")
        need(rep["owner_normalized_support_ast_sha256"] == handle["owner_normalized_support_ast_sha256"] ==
             owner["support_ast_sha256"], "representation owner support join")
        need(rep["representation_semantic_kind"] == handle["representation_semantic_kind"] ==
             "TYPED_NONFULL_REPRESENTATION_DISPOSITION", "retained semantic kind")
        certificate = handle["transition_ready_certificate"]
        need(certificate["typed_owner_support_bound"] is True and
             certificate["typed_representation_semantics_closed"] is True and
             certificate["fresh_component_binding_consumed"] is True and
             certificate["transition_theorem_claimed"] is False and
             certificate["pair_routing_claimed"] is False,
             "truthful transition-ready nonpromotion")
        need(handle["transition_ready_certificate_sha256"] == digest(certificate),
             "handle certificate closure")
        body = {
            "representation_id": representation,
            "owner_member_id": owner_id,
            "fresh_component_id": source["fresh_component_id"],
            "base_root_id": current["base_root_id"],
            "official_key_id": current["official_key_id"],
            "shared_full_face_sha256": face_key,
            "typed_source_support_ast_sha256": source["typed_source_support_ast_sha256"],
            "owner_support_ast_sha256": owner["support_ast_sha256"],
            "C15_row_sha256": current["row_sha256"],
            "C20A_row_sha256": owner["row_sha256"],
            "C20D_row_sha256": source["row_sha256"],
            "I2_row_sha256": i2_selected[representation]["row_sha256"],
            "R295A_row_sha256": r295_rows[i2_selected[representation]["source_row_id"]]["row_sha256"],
            "C25_member_row_sha256": member["row_sha256"],
            "C25_representation_row_sha256": rep["row_sha256"],
            "C26_handle_row_sha256": handle["row_sha256"],
            "formal_credit": 0,
        }
        commitments.append((representation, digest(body)))
    commitments.sort()
    ids = hashlib.sha256(); row_sequence = hashlib.sha256()
    for representation, row_hash in commitments:
        ids.update(representation.encode("ascii") + b"\n")
        row_sequence.update(bytes.fromhex(row_hash))

    result = {
        "schema": SCHEMA,
        "status": "PASS_LOCAL_ZERO_CREDIT__276_RETAINED_CONTINUATIONS__EXACT_POSITIVE_T_FULL_FACE_ADJACENCY__ZERO_GAPS",
        "implementation": "STREAM_C20D_GEOMETRY_THEN_CURRENT_AUTHORITY_JOIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "seed_declared_but_not_semantically_used": True,
        "input_pins": dict(sorted(PINS.items())),
        "full_ledger_census": dict(sorted(FULL_COUNTS.items())),
        "C20D_source_semantic_census": dict(sorted(semantic_census.items())),
        "C20D_relation_census": dict(sorted(relation_census.items())),
        "candidate_universe": {
            "definition": "ALL_AND_ONLY_C20D_TYPED_BOXES_SHARING_COMPLETE_POSITIVE_T_FACE_WITH_THEIR_C20A_OWNER",
            "candidate_count": len(commitments),
            "chart_census": dict(sorted(chart_census.items())),
            "candidate_representation_ids_sha256": ids.hexdigest(),
            "candidate_row_sequence_sha256": row_sequence.hexdigest(),
            "order": "representation_id_ASCII",
        },
        "join_gap_census": {
            "C20D_owner_missing_from_C20A": 0,
            "I2_representation_orphan": 0,
            "R295A_identity_or_geometry_orphan": 0,
            "C15_owner_orphan": 0,
            "C25_member_orphan": 0,
            "C25_representation_orphan": 0,
            "C26_handle_orphan": 0,
            "component_root_key_mismatch": 0,
            "support_or_source_binding_mismatch": 0,
            "duplicate_owner_or_shared_face_assignment": 0,
            "unresolved_geometry": 0,
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
    arguments = parser.parse_args()
    print(canonical(build(arguments.seed)).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
