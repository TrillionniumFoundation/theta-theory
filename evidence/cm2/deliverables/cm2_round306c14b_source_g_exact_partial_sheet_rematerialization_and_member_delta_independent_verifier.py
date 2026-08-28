#!/usr/bin/env python3
"""Independent verifier for the C14b exact-sheet/member-delta package."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta"
SHEETS: Final = PREFIX + "_exact_sheet_member_ledger.jsonl.gz"
DISPOSITIONS: Final = PREFIX + "_outer_envelope_disposition_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"
MANIFEST: Final = PREFIX + "_manifest.sha256"
PRODUCER_SHA: Final = "ce32231ed4fdcc5aa58159b438ec24e9b1a7568e02d83e48ca7a57ee01ee564d"


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def obj(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576):
            h.update(block)
    return h.hexdigest()


def ref(row: dict[str, Any]) -> dict[str, str]:
    return {"row_id": row["row_id"], "row_sha256": row["row_sha256"]}


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C14A_PARTIAL", "cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_partial_rematerialization_frontier.jsonl.gz", 4567486, "1160dd4c2c4f87141964c49f90cb66f20bedb21ee3e08a4bc2fc989c4a23af0f"),
    Pin("C14A_RESULT", "cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_result.json", 3554, "bb120a19d06f68d8b52de03a38efb765ab0c9d4df282b0ae1d7257498c8a6a51"),
    Pin("C14A_MANIFEST", "cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier_manifest.sha256", 1546, "9a4b05b97453709afb579d5f25ecc4b74bc257a87b4172742468196fecd053c9"),
    Pin("C10", "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization_exact_graph_support_ledger.jsonl.gz", 19958893, "b7b2b02653a404060364b788b3e0ac8693d2d9d8d1c45e6109ca7f4400c4080c"),
    Pin("C6_MEMBER", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213125489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    Pin("C7_IDENTITY", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz", 269633111, "de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),
    Pin("C7_REPRESENTATION", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz", 240400592, "1dc805b60f15ec8491b5200ccf9f04a239ce1532f6845a026045709feaaaa468"),
    Pin("C7_RESULT", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_result.json", 10231, "497838e082d7e48dc1a28d9da829b78bd20e39827d1d54815400ec8d3e78abee"),
)

ZERO: Final = {
    "representation_pullback": 0,
    "member_normalized_support": 0,
    "global_normalized_support": 0,
    "DSU_edge": 0,
    "DSU_union": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "CM2": 0,
}


def pin_path(pin: Pin) -> Path:
    path = ROOT / pin.filename
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_size == pin.size, "pin size:" + pin.role)
    need(fsha(path) == pin.sha256, "pin sha:" + pin.role)
    return path


def source_rows(path: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(claimed == obj(core), f"row closure:{label}:{ordinal}")
            yield row


def candidate_rows(path: Path, descriptor: dict[str, Any], label: str) -> Iterator[dict[str, Any]]:
    need(path.name == descriptor["filename"] and path.stat().st_size == descriptor["compressed_size"],
         "candidate size:" + label)
    need(fsha(path) == descriptor["compressed_sha256"], "candidate compressed sha:" + label)
    plain_hash = hashlib.sha256()
    ordered_hash = hashlib.sha256()
    ordered_hash.update(b"[")
    plain_size = 0
    count = 0
    with gzip.open(path, "rb") as stream:
        for line in stream:
            plain_hash.update(line)
            plain_size += len(line)
            row = json.loads(line)
            need(line == canonical(row) + b"\n", "candidate canonical JSONL:" + label)
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(claimed == obj(core), "candidate row closure:" + label)
            if count:
                ordered_hash.update(b",")
            ordered_hash.update(canonical(row))
            count += 1
            yield row
    ordered_hash.update(b"]")
    need(count == descriptor["row_count"] and plain_size == descriptor["uncompressed_size"] and
         plain_hash.hexdigest() == descriptor["uncompressed_sha256"] and
         ordered_hash.hexdigest() == descriptor["ordered_rows_sha256"],
         "candidate descriptor:" + label)


def partial_predicate(base: dict[str, Any]) -> bool:
    return (base.get("op") == "AND" and
            sum(x.get("op") == "CLOSED_INTERVAL" for x in base.get("args", [])) == 2 and
            sum(x.get("op") == "OR_DISJOINT" for x in base.get("args", [])) == 1)


def rectangle(base: dict[str, Any]) -> list[str]:
    intervals = {row.get("coordinate"): row for row in base.get("args", [])
                 if row.get("op") == "CLOSED_INTERVAL"}
    need(set(intervals) == {"p", "s"}, "partial rectangle")
    return [intervals["p"]["lower"], intervals["p"]["upper"],
            intervals["s"]["lower"], intervals["s"]["upper"]]


def manifest_members() -> dict[str, str]:
    output: dict[str, str] = {}
    for line in (ROOT / MANIFEST).read_text("ascii").splitlines():
        digest, filename = line.split("  ", 1)
        need(filename not in output, "manifest duplicate")
        output[filename] = digest
    return output


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", default=str(ROOT))
    parser.add_argument("--manifest-first", action="store_true")
    args = parser.parse_args()
    candidate = Path(args.candidate_dir).resolve()
    if args.manifest_first:
        members = manifest_members()
        need(len(members) == 9 and all((ROOT / name).is_file() and fsha(ROOT / name) == digest
                                      for name, digest in members.items()), "manifest members")

    result_raw = (candidate / RESULT).read_bytes()
    result = json.loads(result_raw)
    core = dict(result)
    claimed = core.pop("result_sha256", None)
    need(result_raw == canonical(result) and claimed == obj(core), "result closure")
    need(set(result) == {
        "schema", "status", "producer_source", "source_pins", "source_exhaustion",
        "census", "scoped_credit", "formal_credit", "strict_nonpromotion",
        "exact_sheet_member_ledger", "outer_envelope_disposition_ledger",
        "fresh_member_universe_and_DSU_replay_triggered_if_registry_admitted",
        "required_next", "result_sha256",
    }, "result exact keys")
    need(result["schema"] ==
         "cm2.round306c14b.source-g-exact-partial-sheet-rematerialization-and-member-delta.v1" and
         result["status"] ==
         "PASS_4432_EXACT_SHEET_IDENTITIES_CONSTRUCTED__REGISTRY_ADMISSION_AND_OLD_FAMILY_DISPOSITION_PENDING" and
         result["required_next"] ==
         "SEAL_4432_OLD_OUTER_ENVELOPE_FAMILY_DISPOSITIONS_AND_NEW_MEMBER_ROOT_EDGE_AUTHORITY_THEN_FRESH_DSU_REPLAY",
         "result scope/status")
    need(result["producer_source"] == {
        "filename": PREFIX + "_producer.py", "size": 19485, "sha256": PRODUCER_SHA,
    }, "producer binding")
    expected_census = {
        "exact_partial_sheet_identities_constructed": 4432,
        "new_canonical_representation_definitions": 4432,
        "new_graph_sheet_set_equalities": 4432,
        "old_outer_envelope_family_dispositions_unresolved": 4432,
        "old_outer_envelope_members_retained": 4432,
        "old_outer_envelope_relations_disposed": 4432,
        "known_valid_G2A_graph_sheet_member_count": 5264,
        "sealed_NON_GRAPH_member_count_before_old_family_disposition": 51172,
        "candidate_member_count_if_admitted": 502204,
        "candidate_representation_count_if_admitted": 549616,
        "valid_graph_to_sheet_relations": 5264,
        "valid_graph_to_side_relations": 9960,
        "valid_physical_relation_denominator": 15224,
    }
    need(result["census"] == expected_census, "result census")
    need(result["source_exhaustion"] == {
        "C10_graph_rows": 5264, "C6_members": 497772, "C7_identity_rows": 497772,
        "C7_representation_rows": 545184, "new_identity_id_collisions": 0,
        "new_member_id_collisions": 0, "new_representation_id_collisions": 0,
        "target_new_members": 4432, "target_old_members": 4432,
    }, "source exhaustion receipt")
    need(result["scoped_credit"] == {
        "new_canonical_representation_definition": 4432,
        "new_graph_sheet_set_equality": 4432,
        "new_exact_sheet_identity_construction": 4432,
        "old_outer_envelope_member_retention": 4432,
        "old_outer_envelope_relation_disposition": 4432,
    }, "scoped credit")
    need(result["formal_credit"] == ZERO and
         result["fresh_member_universe_and_DSU_replay_triggered_if_registry_admitted"] is True,
         "formal nonpromotion")
    need(result["strict_nonpromotion"] == {
        "CM2": "NO-GO_FOR_CLAIM", "new_DSU_edges": 0,
        "new_member_base_roots_assigned": 0, "new_member_components_assigned": 0,
        "new_registry_members_admitted": 0, "new_representations_admitted": 0,
        "normalized_support_sealed": False, "old_components_or_edges_inherited": 0,
        "representation_pullback_proved": False,
    }, "strict nonpromotion")

    sheets: dict[str, dict[str, Any]] = {}
    new_members: set[str] = set()
    new_representations: set[str] = set()
    for ordinal, row in enumerate(candidate_rows(candidate / SHEETS,
                                                  result["exact_sheet_member_ledger"],
                                                  "sheet")):
        need(row["sheet_ordinal"] == ordinal and row["graph_id"] not in sheets,
             "sheet order/graph uniqueness")
        graph = row["graph_id"]
        new = row["new_exact_sheet_member_id"]
        base = row["exact_partial_base_ast"]
        base_sha = row["exact_partial_base_ast_sha256"]
        need(partial_predicate(base) and obj(base) == base_sha, "sheet partial AST")
        need(new == "round306c14-exact-partial-sheet:" + obj([graph, base_sha]),
             "sheet natural member ID")
        need(row["new_exact_sheet_natural_key"] ==
             ["ROUND306C14_EXACT_PARTIAL_BASE_SHEET", graph, base_sha], "sheet natural key")
        need(row["schema"] ==
             "cm2.round306c14b.source-g-exact-partial-sheet-rematerialization-and-member-delta.v1.exact-sheet-member-row.v1" and
             row["row_id"] == PREFIX + ":exact-sheet:" + obj([graph, new]) and
             row["sheet_construction_kind"] ==
             "EXACT_PARTIAL_BASE_SHEET_DEFINED_BY_C10_GRAPH_PROJECTION",
             "sheet schema/id/construction kind")
        representation = "round306c14b-exact-partial-sheet-representation:" + obj([new, base_sha])
        need(row["new_canonical_representation_id"] == representation and
             row["new_canonical_representation_ast"] == {
                 "ast_kind": "EXACT_PARTIAL_BASE_SHEET_CANONICAL_REPRESENTATION",
                 "owner_member_id": new, "support_ast_sha256": base_sha,
             }, "new representation")
        certificate = row["graph_to_new_sheet_set_equality_certificate"]
        certificate_core = dict(certificate)
        certificate_sha = certificate_core.pop("certificate_sha256", None)
        need(certificate_sha == obj(certificate_core), "equality certificate closure")
        need(set(certificate) == {
            "projection_map", "C10_exact_support_ref", "exact_graph_support_ast_sha256",
            "exact_graph_projection_base_ast_sha256", "new_exact_sheet_support_ast_sha256",
            "one_graph_point_for_every_exact_base_point",
            "every_graph_point_projects_into_exact_base", "projection_is_bijection",
            "new_sheet_support_equals_exact_graph_projection", "certificate_sha256",
        } and certificate["projection_map"] == "(t,p,s)->(p,s)" and
             certificate["exact_graph_projection_base_ast_sha256"] == base_sha and
             certificate["new_exact_sheet_support_ast_sha256"] == base_sha and
             certificate["projection_is_bijection"] is True and
             certificate["new_sheet_support_equals_exact_graph_projection"] is True and
             certificate["one_graph_point_for_every_exact_base_point"] is True and
             certificate["every_graph_point_projects_into_exact_base"] is True,
             "new graph-sheet equality")
        need(row["exact_sheet_identity_construction_credit"] == 1 and
             row["registry_member_admission_credit"] == 0 and
             row["canonical_representation_definition_credit"] == 1 and
             row["representation_universe_admission_credit"] == 0 and
             row["graph_sheet_set_equality_credit"] == 1 and
             row["representation_pullback_credit"] == 0 and
             row["base_root_or_component_inheritance_credit"] == 0 and
             row["DSU_edge_or_union_authorized"] is False and
             row["downstream_nonpromotion"] == ZERO, "sheet credit boundary")
        need(new not in new_members and representation not in new_representations,
             "new identity uniqueness")
        new_members.add(new)
        new_representations.add(representation)
        sheets[graph] = {
            "row": row, "new": new, "base_sha": base_sha,
            "C10_ref": certificate["C10_exact_support_ref"],
        }
    need(len(sheets) == len(new_members) == len(new_representations) == 4432,
         "sheet census")

    dispositions: dict[str, dict[str, Any]] = {}
    old_members: set[str] = set()
    for ordinal, row in enumerate(candidate_rows(candidate / DISPOSITIONS,
                                                  result["outer_envelope_disposition_ledger"],
                                                  "disposition")):
        graph = row["graph_id"]
        need(row["disposition_ordinal"] == ordinal and graph in sheets and
             graph not in dispositions, "disposition order/coverage")
        old = row["old_outer_envelope_sheet_member_id"]
        need(row["new_exact_sheet_member_id"] == sheets[graph]["new"] and
             old not in old_members and old not in new_members, "disposition subjects")
        need(row["schema"] ==
             "cm2.round306c14b.source-g-exact-partial-sheet-rematerialization-and-member-delta.v1.outer-envelope-disposition-row.v1" and
             row["row_id"] == PREFIX + ":outer-envelope-disposition:" +
             obj([graph, old, row["new_exact_sheet_member_id"]]),
             "disposition schema/id")
        need(row["old_outer_envelope_physical_member_retained"] is True and
             row["old_outer_envelope_representation_retained"] is True and
             row["old_graph_to_outer_envelope_relation_disposition"] ==
             "INVALID_AS_SET_EQUALITY__OUTER_ENVELOPE_STRICTLY_COARSER" and
             row["old_member_family_before"] == "G2A" and
             row["old_member_family_after"] ==
             "UNRESOLVED_PENDING_SEALED_FAMILY_AUTHORITY" and
             row["old_member_reclassification_credit"] == 0 and
             row["old_member_deletion_or_invalidation_credit"] == 0 and
             row["old_component_or_edge_transfer_to_new_member_credit"] == 0 and
             row["DSU_edge_or_union_authorized"] is False and
             row["representation_pullback_credit"] == 0 and
             row["downstream_nonpromotion"] == ZERO, "old disposition boundary")
        old_members.add(old)
        dispositions[graph] = row
    need(len(dispositions) == len(old_members) == 4432, "disposition census")

    source = {pin.role: pin_path(pin) for pin in PINS}
    need(result["source_pins"] == [pin.__dict__ for pin in PINS], "source pin list")
    c14a_seen: set[str] = set()
    for row in source_rows(source["C14A_PARTIAL"], "C14a partial"):
        graph = row["graph_id"]
        need(graph in sheets and graph in dispositions, "C14a graph coverage")
        need(sheets[graph]["row"]["C14a_partial_frontier_ref"] == ref(row) and
             dispositions[graph]["C14a_partial_frontier_ref"] == ref(row), "C14a refs")
        need(row["proposed_exact_sheet_member_id"] == sheets[graph]["new"] and
             row["old_outer_envelope_sheet_member_id"] ==
             dispositions[graph]["old_outer_envelope_sheet_member_id"] and
             row["exact_partial_base_ast_sha256"] == sheets[graph]["base_sha"] and
             row["exact_partial_base_ast"] == sheets[graph]["row"]["exact_partial_base_ast"] and
             row["proposed_exact_sheet_natural_key"] ==
             ["ROUND306C14_EXACT_PARTIAL_BASE_SHEET", graph, sheets[graph]["base_sha"]] and
             row["outer_envelope_rectangle"] ==
             rectangle(sheets[graph]["row"]["exact_partial_base_ast"]) and
             row["old_relation_disposition"] ==
             "NOT_SET_EQUAL__OUTER_ENVELOPE_STRICTLY_COARSER_THAN_EXACT_PARTIAL_BASE" and
             row["required_next"] == "REMATERIALIZE_AND_INDEPENDENTLY_VERIFY_EXACT_PARTIAL_SHEET",
             "C14a semantic binding")
        c14a_seen.add(graph)
    need(len(c14a_seen) == 4432, "C14a exhaustion")

    c10_total = 0
    c10_seen: set[str] = set()
    for row in source_rows(source["C10"], "C10"):
        c10_total += 1
        graph = row["graph_id"]
        if graph in sheets:
            need(row["graph_class"] == "R235_TARGET_POSITIVE_PARTIAL_BASE" and
                 ref(row) == sheets[graph]["C10_ref"] and
                 row["ast_sha256"]["base_domain_ast_sha256"] == sheets[graph]["base_sha"] and
                 row["ast_sha256"]["exact_support_ast_sha256"] ==
                 sheets[graph]["row"]["graph_to_new_sheet_set_equality_certificate"]
                              ["exact_graph_support_ast_sha256"] and
                 row["support_properties"]["one_graph_point_per_exact_base_point"] is True,
                 "C10 equality authority")
            c10_seen.add(graph)
    need(c10_total == 5264 and len(c10_seen) == 4432, "C10 exhaustion")

    old_to_graph = {row["old_outer_envelope_sheet_member_id"]: graph
                    for graph, row in dispositions.items()}
    c6_total = 0
    c6_seen: set[str] = set()
    c6_new_collisions = 0
    for row in source_rows(source["C6_MEMBER"], "C6 member"):
        c6_total += 1
        member = row["registry_member_id"]
        if member in new_members:
            c6_new_collisions += 1
        if member in old_members:
            graph = old_to_graph[member]
            need(dispositions[graph]["C6_old_member_ref"] == ref(row), "C6 old ref")
            c6_seen.add(member)
    need(c6_total == 497772 and len(c6_seen) == 4432 and c6_new_collisions == 0,
         "C6 collision exhaustion")

    by_old = {row["old_outer_envelope_sheet_member_id"]: row
              for row in dispositions.values()}
    identity_total = 0
    identity_seen: set[str] = set()
    identity_new_collisions = 0
    for row in source_rows(source["C7_IDENTITY"], "C7 identity"):
        identity_total += 1
        member = row["member_id"]
        if member in new_members:
            identity_new_collisions += 1
        if member in by_old:
            need(row["coarse_family"] == "G2A" and
                 by_old[member]["C7_old_identity_ref"] == ref(row), "C7 old identity")
            identity_seen.add(member)
    need(identity_total == 497772 and len(identity_seen) == 4432 and
         identity_new_collisions == 0, "C7 identity collision exhaustion")

    representation_total = 0
    representation_seen: set[str] = set()
    representation_collisions = 0
    for row in source_rows(source["C7_REPRESENTATION"], "C7 representation"):
        representation_total += 1
        if row["representation_id"] in new_representations:
            representation_collisions += 1
        owner = row["owner_member_id"]
        if owner in by_old:
            need(row["coarse_family"] == "G2A" and
                 by_old[owner]["C7_old_representation_ref"] == ref(row),
                 "C7 old representation")
            need(owner not in representation_seen, "one old representation")
            representation_seen.add(owner)
    need(representation_total == 545184 and len(representation_seen) == 4432 and
         representation_collisions == 0, "C7 representation collision exhaustion")

    status = ("PASS_MANIFEST_FIRST_NO_WRITE_C14B_4432_EXACT_SHEETS_MEMBER_DELTA"
              if args.manifest_first else
              "PASS_INDEPENDENT_C14B_4432_EXACT_SHEETS_MEMBER_DELTA")
    print(json.dumps({"status": status, "result_sha256": claimed},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
