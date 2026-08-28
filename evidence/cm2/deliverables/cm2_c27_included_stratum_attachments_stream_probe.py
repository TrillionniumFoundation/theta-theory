#!/usr/bin/env python3
"""C27-independent INCLUDED_STRATUM_ATTACHMENTS zero-credit stream gate.

The candidate universe is derived from the typed C25 representation semantics
and the primitive C20D source-disposition ledger.  It is the disjoint union of:

* EXACT_SUBCOVER_INCLUSION_DISPOSITION (8,416 rows), and
* strict-subcover C20D TYPED_NONFULL dispositions (2,244 rows).

The remaining 276 C20D rows are ADJACENT_POSITIVE_T_CONTINUATION with
disjoint interiors and a shared full face.  They are routed to the still-open
RETAINED_CONTINUATION terminal and are not attachments.

C25 and C26 are consumed in lockstep.  Candidate owners are then joined to
the complete C15 member/component freeze.  No Round306C27 source, family
table, or edge ledger is read.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
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
SELECTED_KINDS = {
    "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8_416,
    "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2_244,
}
KERNELS_BY_KIND = {
    "EXACT_SUBCOVER_INCLUSION_DISPOSITION": {"C22B", "C23B"},
    "TYPED_NONFULL_REPRESENTATION_DISPOSITION": {"C20D"},
}
EXPECTED_KERNELS = {"C20D": 2_244, "C22B": 7_288, "C23B": 1_128}
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


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise GateFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def check_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    need(type(claimed) is str and len(claimed) == 64, label + ":row sha")
    need(digest({key: value for key, value in row.items() if key != "row_sha256"}) == claimed, label + ":row closure")


def validate_triplet(
    c15: dict[str, Any], c25: dict[str, Any], c26: dict[str, Any],
    c20d: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate one selected C15/C25/C26 join and return its canonical body."""

    check_row(c15, "C15 selected")
    check_row(c25, "C25 selected")
    check_row(c26, "C26 selected")
    kind = c25.get("representation_semantic_kind")
    need(kind in SELECTED_KINDS, "selected semantic kind")
    kernel = c25.get("source_bindings", {}).get("semantic_kernel")
    need(kernel in KERNELS_BY_KIND[kind], "semantic kind/kernel partition")
    representation = c25.get("representation_id")
    owner = c25.get("owner_member_id")
    component = c25.get("fresh_component_id")
    need(c15.get("registry_member_id") == owner, "C15 owner join")
    need(c26.get("representation_id") == representation, "C25/C26 representation join")
    need(c26.get("owner_member_id") == owner, "C25/C26 owner join")
    need(c26.get("fresh_component_id") == component == c15.get("fresh_component_id"), "C15/C25/C26 component join")
    need(c26.get("base_root_id") == c25.get("base_root_id") == c15.get("base_root_id"), "base-root join")
    need(c26.get("official_key_id") == c25.get("official_key_id") == c15.get("official_key_id"), "official-key join")
    need(c26.get("owner_normalized_support_ast_sha256") == c25.get("owner_normalized_support_ast_sha256"), "owner support join")
    need(c26.get("representation_semantic_kind") == kind, "semantic-kind join")
    need(c26.get("representation_semantic_certificate_sha256") == c25.get("representation_semantic_certificate_sha256"), "semantic-certificate join")
    need(c26.get("source_bindings", {}).get("C25_representation_row_sha256") == c25.get("row_sha256"), "C26 C25 row binding")
    certificate = c26.get("transition_ready_certificate", {})
    need(certificate.get("kind") == "B1A_TRANSITION_READY_REPRESENTATION_HANDLE", "handle certificate kind")
    need(certificate.get("typed_owner_support_bound") is True, "typed owner support")
    need(certificate.get("typed_representation_semantics_closed") is True, "typed representation semantics")
    need(certificate.get("fresh_component_binding_consumed") is True, "fresh component consumed")
    need(certificate.get("transition_theorem_claimed") is False, "no transition theorem promotion")
    need(certificate.get("pair_routing_claimed") is False, "no pair-routing promotion")
    need(digest(certificate) == c26.get("transition_ready_certificate_sha256"), "handle certificate closure")
    if kernel == "C20D":
        need(c20d is not None, "C20D primitive source join")
        check_row(c20d, "C20D selected")
        need(c20d.get("representation_id") == representation, "C20D representation join")
        need(c20d.get("owner_member_id") == owner, "C20D owner join")
        need(c20d.get("fresh_component_id") == component, "C20D component join")
        need(c20d.get("owner_support_ast_sha256") == c25.get("owner_normalized_support_ast_sha256"), "C20D owner support join")
        need(c25.get("source_bindings", {}).get("semantic_kernel_row_sha256") == c20d.get("row_sha256"), "C25/C20D row binding")
        need(c25.get("source_bindings", {}).get("semantic_kernel_ledger") == C20D, "C25 C20D kernel ledger pin")
        need(c25.get("source_bindings", {}).get("semantic_kernel_result_sha256") == C20D_KERNEL_RESULT_SHA256, "C25 C20D result pin")
        need(c25.get("coarse_family") == "PRESERVED", "C25 C20D coarse family")
        need(c20d.get("source_semantics") in C20D_STRICT, "C20D strict-subcover terminal assignment")
        need(c20d.get("exact_relation_to_owner_support") == "STRICT_SUBCOVER_OF_OWNER_SUPPORT", "C20D strict relation")
    else:
        need(c20d is None, "non-C20D must not consume C20D row")
    return {
        "representation_id": representation,
        "owner_member_id": owner,
        "fresh_component_id": component,
        "base_root_id": c15["base_root_id"],
        "official_key_id": c15["official_key_id"],
        "representation_semantic_kind": kind,
        "semantic_kernel": kernel,
        "owner_normalized_support_ast_sha256": c25["owner_normalized_support_ast_sha256"],
        "representation_semantic_certificate_sha256": c25["representation_semantic_certificate_sha256"],
        "C15_member_row_sha256": c15["row_sha256"],
        "C25_representation_row_sha256": c25["row_sha256"],
        "C26_handle_row_sha256": c26["row_sha256"],
        "C20D_source_semantics": None if c20d is None else c20d["source_semantics"],
        "C20D_row_sha256": None if c20d is None else c20d["row_sha256"],
        "cross_component": False,
        "formal_credit": 0,
    }


def build(seed: int) -> dict[str, Any]:
    # The argument is deliberately parsed but never serialized or used.
    need(type(seed) is int, "integer seed")
    for name, expected in PINS.items():
        path = HERE / name
        need(path.is_file() and not path.is_symlink(), "regular input:" + name)
        need(file_hash(path) == expected, "input pin:" + name)

    c20d_rows: dict[str, dict[str, Any]] = {}
    c20d_census: Counter[str] = Counter()
    for ordinal, row in enumerate(rows(HERE / C20D)):
        need(row.get("ordinal") == ordinal, "C20D ordinal")
        check_row(row, "C20D full")
        need(row.get("schema") == "cm2.round306c20d.source-g-2520-preserved-nonfull-alias-negative-disposition-kernel.v1.row.v1", "C20D schema")
        representation = row.get("representation_id")
        need(type(representation) is str and representation not in c20d_rows, "C20D unique representation")
        semantics = row.get("source_semantics")
        need(semantics in C20D_SEMANTICS, "C20D source semantics")
        relation = row.get("exact_relation_to_owner_support")
        expected_relation = (
            "STRICT_SUBCOVER_OF_OWNER_SUPPORT"
            if semantics in C20D_STRICT
            else "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE"
        )
        need(relation == expected_relation, "C20D exact relation/semantics")
        need(row.get("negative_disposition") == "NOT_A_COMPLETE_SUPPORT_REPRESENTATION__RETAIN_AS_TYPED_NONFULL_ALIAS_HANDLE", "C20D negative disposition")
        need(digest(row.get("typed_source_support_ast")) == row.get("typed_source_support_ast_sha256"), "C20D source support closure")
        c20d_rows[representation] = row
        c20d_census[semantics] += 1
    need(len(c20d_rows) == FULL_COUNTS[C20D], "C20D full count")
    need(dict(c20d_census) == C20D_SEMANTICS, "C20D source semantic census")

    selected_pairs: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]] = []
    selected_ids: set[str] = set()
    selected_owners: set[str] = set()
    kind_census: Counter[str] = Counter()
    kernel_census: Counter[str] = Counter()
    c25_iter = rows(HERE / C25)
    c26_iter = rows(HERE / C26)
    c20d_seen: set[str] = set()
    excluded_adjacent_ids: set[str] = set()
    for ordinal in range(FULL_COUNTS[C25]):
        c25 = next(c25_iter, None)
        c26 = next(c26_iter, None)
        need(c25 is not None and c26 is not None, "C25/C26 length")
        need(c25.get("representation_ordinal") == ordinal, "C25 ordinal")
        need(c26.get("handle_ordinal") == ordinal, "C26 ordinal")
        # Full-ledger lockstep fields are checked before candidate filtering.
        need(c25.get("representation_id") == c26.get("representation_id"), "full representation lockstep")
        need(c25.get("owner_member_id") == c26.get("owner_member_id"), "full owner lockstep")
        need(c25.get("fresh_component_id") == c26.get("fresh_component_id"), "full component lockstep")
        need(c25.get("representation_semantic_kind") == c26.get("representation_semantic_kind"), "full semantic lockstep")
        need(c26.get("source_bindings", {}).get("C25_representation_row_sha256") == c25.get("row_sha256"), "full row-hash lockstep")
        kind = c25["representation_semantic_kind"]
        kernel = c25.get("source_bindings", {}).get("semantic_kernel")
        c20d = None
        if kernel == "C20D":
            representation = c25["representation_id"]
            need(representation in c20d_rows, "C25 C20D representation cover")
            c20d = c20d_rows[representation]
            need(c25.get("source_bindings", {}).get("semantic_kernel_row_sha256") == c20d.get("row_sha256"), "full C25/C20D row binding")
            need(c25.get("source_bindings", {}).get("semantic_kernel_ledger") == C20D, "full C25 C20D ledger pin")
            need(c25.get("source_bindings", {}).get("semantic_kernel_result_sha256") == C20D_KERNEL_RESULT_SHA256, "full C25 C20D result pin")
            need(c25.get("representation_semantic_kind") == "TYPED_NONFULL_REPRESENTATION_DISPOSITION", "full C25 C20D semantic kind")
            need(c25.get("coarse_family") == "PRESERVED", "full C25 C20D coarse family")
            need(c25.get("owner_member_id") == c20d.get("owner_member_id"), "full C25/C20D owner join")
            need(c25.get("fresh_component_id") == c20d.get("fresh_component_id"), "full C25/C20D component join")
            need(c25.get("owner_normalized_support_ast_sha256") == c20d.get("owner_support_ast_sha256"), "full C25/C20D support join")
            need(representation not in c20d_seen, "duplicate C25 C20D representation")
            c20d_seen.add(representation)
            if c20d["source_semantics"] == "ADJACENT_POSITIVE_T_CONTINUATION":
                excluded_adjacent_ids.add(representation)
        if kind not in SELECTED_KINDS or (c20d is not None and c20d["source_semantics"] not in C20D_STRICT):
            continue
        check_row(c25, "selected C25")
        check_row(c26, "selected C26")
        representation = c25["representation_id"]
        need(representation not in selected_ids, "duplicate selected representation")
        selected_ids.add(representation)
        selected_owners.add(c25["owner_member_id"])
        kind_census[kind] += 1
        kernel = c25["source_bindings"]["semantic_kernel"]
        need(kernel in KERNELS_BY_KIND[kind], "selected kind/kernel")
        kernel_census[kernel] += 1
        selected_pairs.append((c25, c26, c20d))
    need(next(c25_iter, None) is None and next(c26_iter, None) is None, "C25/C26 exact exhaustion")
    need(dict(kind_census) == SELECTED_KINDS, "selected semantic census")
    need(dict(kernel_census) == EXPECTED_KERNELS, "selected kernel census")
    need(c20d_seen == set(c20d_rows), "C25/C20D exact representation cover")
    need(len(excluded_adjacent_ids) == 276, "C20D adjacent exclusion census")
    need(len(selected_pairs) == 10_660, "selected total")

    owner_rows: dict[str, dict[str, Any]] = {}
    c15_iter = rows(HERE / C15)
    for ordinal in range(FULL_COUNTS[C15]):
        row = next(c15_iter, None)
        need(row is not None and row.get("member_ordinal") == ordinal, "C15 ordinal")
        member = row.get("registry_member_id")
        if member in selected_owners:
            check_row(row, "selected C15")
            need(member not in owner_rows, "duplicate selected C15 owner")
            owner_rows[member] = row
    need(next(c15_iter, None) is None, "C15 exact exhaustion")
    need(set(owner_rows) == selected_owners, "C15 owner cover")

    candidates: list[tuple[str, str]] = []
    for c25, c26, c20d in selected_pairs:
        body = validate_triplet(owner_rows[c25["owner_member_id"]], c25, c26, c20d)
        candidates.append((body["representation_id"], digest(body)))
    candidates.sort()
    sequence = hashlib.sha256()
    ids = hashlib.sha256()
    for representation, row_sha256 in candidates:
        ids.update(representation.encode("ascii") + b"\n")
        sequence.update(bytes.fromhex(row_sha256))
    excluded_ids = hashlib.sha256()
    for representation in sorted(excluded_adjacent_ids):
        excluded_ids.update(representation.encode("ascii") + b"\n")
    original_ids = hashlib.sha256()
    for representation in sorted(selected_ids | excluded_adjacent_ids):
        original_ids.update(representation.encode("ascii") + b"\n")
    need(not (selected_ids & excluded_adjacent_ids), "attachment/adjacent disjointness")
    need(len(selected_ids | excluded_adjacent_ids) == 10_936, "original non-equality union census")
    need(ids.hexdigest() == EXPECTED_CANDIDATE_IDS_SHA256, "corrected attachment ID commitment")
    need(excluded_ids.hexdigest() == EXPECTED_EXCLUDED_ADJACENT_IDS_SHA256, "excluded adjacent ID commitment")
    need(original_ids.hexdigest() == EXPECTED_ORIGINAL_NON_EQUALITY_IDS_SHA256, "original non-equality union commitment")

    result = {
        "schema": "cm2.c27-independent.included-stratum-attachments.stream-zero-credit.v1",
        "status": "PASS_ZERO_CREDIT__10660_INCLUDED_STRATUM_ATTACHMENTS__C20D_PRIMITIVE_SPLIT__C25_C26_LOCKSTEP__C15_OWNER_COMPONENT_JOIN__ZERO_GAPS",
        "implementation": "STREAM_LOCKSTEP_THEN_SELECTED_OWNER_JOIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "seed_declared_but_not_semantically_used": True,
        "input_pins": dict(sorted(PINS.items())),
        "full_ledger_census": dict(sorted(FULL_COUNTS.items())),
        "candidate_universe": {
            "definition": "C25_EXACT_SUBCOVER_PLUS_ONLY_C20D_PRIMITIVE_STRICT_SUBCOVERS",
            "semantic_kind_census": dict(sorted(kind_census.items())),
            "semantic_kernel_census": dict(sorted(kernel_census.items())),
            "C20D_source_semantic_census": dict(sorted(c20d_census.items())),
            "C20D_adjacent_positive_t_excluded_and_reserved_for_open_retained_continuation": 276,
            "excluded_adjacent_representation_ids_sha256": excluded_ids.hexdigest(),
            "candidate_excluded_intersection_count": 0,
            "candidate_plus_excluded_union_count": 10_936,
            "candidate_plus_excluded_union_ids_sha256": original_ids.hexdigest(),
            "candidate_count": len(candidates),
            "candidate_representation_ids_sha256": ids.hexdigest(),
            "candidate_row_sequence_sha256": sequence.hexdigest(),
            "order": "representation_id_ASCII",
        },
        "join_gap_census": {
            "C25_C26_orphan": 0,
            "C20D_C25_orphan_or_row_binding_mismatch": 0,
            "C15_owner_orphan": 0,
            "duplicate_candidate_representation": 0,
            "duplicate_selected_C15_owner": 0,
            "component_mismatch_or_cross_component": 0,
            "base_root_mismatch": 0,
            "official_key_mismatch": 0,
            "support_or_semantic_mismatch": 0,
        },
        "unique_assignment": "PASS_BY_C25_KIND_KERNEL_PLUS_PRIMITIVE_C20D_STRICT_VS_ADJACENT_SOURCE_SEMANTIC_PARTITION",
        "formal_credit": 0,
        "C27_C28_C29": "UNCHANGED_REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(canonical(build(args.seed)).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
