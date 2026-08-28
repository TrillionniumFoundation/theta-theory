#!/usr/bin/env python3
"""Construct 4,432 exact partial sheets and freeze the resulting member delta."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta"
SCHEMA: Final = "cm2.round306c14b.source-g-exact-partial-sheet-rematerialization-and-member-delta.v1"
SHEETS: Final = PREFIX + "_exact_sheet_member_ledger.jsonl.gz"
DISPOSITIONS: Final = PREFIX + "_outer_envelope_disposition_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"


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


def close(row: dict[str, Any]) -> dict[str, Any]:
    return {**row, "row_sha256": obj(row)}


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


def path(pin: Pin) -> Path:
    value = ROOT / pin.filename
    info = os.stat(value, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_size == pin.size, "pin size:" + pin.role)
    h = hashlib.sha256()
    with value.open("rb") as stream:
        while block := stream.read(1048576):
            h.update(block)
    need(h.hexdigest() == pin.sha256, "pin sha:" + pin.role)
    return value


def rows(value: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(value, "rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            core = dict(row)
            claimed = core.pop("row_sha256", None)
            need(claimed == obj(core), f"row closure:{label}:{ordinal}")
            yield row


class LedgerBuilder:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.buffer = io.BytesIO()
        self.gzip = gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                                  fileobj=self.buffer, mtime=0)
        self.plain_hash = hashlib.sha256()
        self.ordered_hash = hashlib.sha256()
        self.ordered_hash.update(b"[")
        self.plain_size = 0
        self.count = 0

    def add(self, row: dict[str, Any]) -> None:
        wire = canonical(row)
        line = wire + b"\n"
        self.gzip.write(line)
        self.plain_hash.update(line)
        self.plain_size += len(line)
        if self.count:
            self.ordered_hash.update(b",")
        self.ordered_hash.update(wire)
        self.count += 1

    def finish(self) -> tuple[bytes, dict[str, Any]]:
        self.gzip.close()
        self.ordered_hash.update(b"]")
        wire = self.buffer.getvalue()
        descriptor = {
            "filename": self.filename,
            "compression": "gzip-level9-mtime-zero",
            "row_count": self.count,
            "compressed_size": len(wire),
            "compressed_sha256": hashlib.sha256(wire).hexdigest(),
            "uncompressed_size": self.plain_size,
            "uncompressed_sha256": self.plain_hash.hexdigest(),
            "ordered_rows_sha256": self.ordered_hash.hexdigest(),
        }
        return wire, descriptor


def partial_predicate(base: dict[str, Any]) -> bool:
    return (base.get("op") == "AND" and
            sum(x.get("op") == "CLOSED_INTERVAL" for x in base.get("args", [])) == 2 and
            sum(x.get("op") == "OR_DISJOINT" for x in base.get("args", [])) == 1)


def build() -> tuple[dict[str, Any], bytes, bytes]:
    sources = {pin.role: path(pin) for pin in PINS}
    c14a_result = json.loads(sources["C14A_RESULT"].read_bytes())
    core = dict(c14a_result)
    need(core.pop("result_sha256") == obj(core), "C14a result closure")
    need(c14a_result["census"]["partial_sheet_rematerializations_required"] == 4432,
         "C14a frontier census")

    targets: dict[str, dict[str, Any]] = {}
    old_ids: set[str] = set()
    new_ids: set[str] = set()
    for row in rows(sources["C14A_PARTIAL"], "C14a partial"):
        graph = row["graph_id"]
        need(graph not in targets, "unique graph frontier")
        need(row["old_relation_disposition"] ==
             "NOT_SET_EQUAL__OUTER_ENVELOPE_STRICTLY_COARSER_THAN_EXACT_PARTIAL_BASE",
             "old relation disposition")
        need(row["old_graph_sheet_set_equality_credit"] == 0 and
             row["new_member_or_DSU_credit"] == 0, "C14a nonpromotion")
        targets[graph] = {
            "old": row["old_outer_envelope_sheet_member_id"],
            "new": row["proposed_exact_sheet_member_id"],
            "base_sha": row["exact_partial_base_ast_sha256"],
            "ref": ref(row),
        }
        old_ids.add(row["old_outer_envelope_sheet_member_id"])
        new_ids.add(row["proposed_exact_sheet_member_id"])
    need(len(targets) == len(old_ids) == len(new_ids) == 4432 and not (old_ids & new_ids),
         "frontier uniqueness")

    c10: dict[str, dict[str, Any]] = {}
    c10_total = 0
    for row in rows(sources["C10"], "C10"):
        c10_total += 1
        if row["graph_id"] in targets:
            need(row["graph_class"] == "R235_TARGET_POSITIVE_PARTIAL_BASE",
                 "C10 target class")
            need(row["sheet_member_id"] == targets[row["graph_id"]]["old"],
                 "C10 old sheet binding")
            need(row["ast_sha256"]["base_domain_ast_sha256"] ==
                 targets[row["graph_id"]]["base_sha"], "C10 base binding")
            need(row["support_properties"]["one_graph_point_per_exact_base_point"] is True,
                 "C10 projection bijection")
            c10[row["graph_id"]] = {
                "ref": ref(row),
                "base_sha": row["ast_sha256"]["base_domain_ast_sha256"],
                "support_sha": row["ast_sha256"]["exact_support_ast_sha256"],
            }
    need(c10_total == 5264 and len(c10) == 4432, "C10 exhaustion")

    c6: dict[str, dict[str, Any]] = {}
    c6_total = 0
    new_collisions = 0
    for row in rows(sources["C6_MEMBER"], "C6 member"):
        c6_total += 1
        member = row["registry_member_id"]
        if member in new_ids:
            new_collisions += 1
        if member in old_ids:
            need(member not in c6, "C6 old member unique")
            c6[member] = row
    need(c6_total == 497772 and len(c6) == 4432 and new_collisions == 0,
         "C6 member exhaustion and collision")

    identities: dict[str, dict[str, Any]] = {}
    identity_total = 0
    identity_new_collisions = 0
    for row in rows(sources["C7_IDENTITY"], "C7 identity"):
        identity_total += 1
        member = row["member_id"]
        if member in new_ids:
            identity_new_collisions += 1
        if member in old_ids:
            need(member not in identities and row["coarse_family"] == "G2A",
                 "old identity unique G2A")
            identities[member] = row
    need(identity_total == 497772 and len(identities) == 4432 and
         identity_new_collisions == 0, "C7 identity exhaustion")

    representations: dict[str, dict[str, Any]] = {}
    representation_total = 0
    new_rep_ids: set[str] = set()
    for row in rows(sources["C7_REPRESENTATION"], "C7 representation"):
        representation_total += 1
        owner = row["owner_member_id"]
        if owner in old_ids:
            need(owner not in representations and row["coarse_family"] == "G2A",
                 "one old G2A representation")
            representations[owner] = row
        new_rep_ids.add(row["representation_id"])
    need(representation_total == 545184 and len(representations) == 4432,
         "C7 representation exhaustion")

    sheet_builder = LedgerBuilder(SHEETS)
    disposition_builder = LedgerBuilder(DISPOSITIONS)
    seen_new_representations: set[str] = set()
    for partial in rows(sources["C14A_PARTIAL"], "C14a partial construction"):
        graph = partial["graph_id"]
        old = partial["old_outer_envelope_sheet_member_id"]
        new = partial["proposed_exact_sheet_member_id"]
        base = partial["exact_partial_base_ast"]
        base_sha = partial["exact_partial_base_ast_sha256"]
        need(partial_predicate(base) and obj(base) == base_sha, "exact partial base AST")
        expected_new = "round306c14-exact-partial-sheet:" + obj([graph, base_sha])
        need(new == expected_new, "new member natural key")
        representation_id = "round306c14b-exact-partial-sheet-representation:" + obj([new, base_sha])
        need(representation_id not in new_rep_ids and
             representation_id not in seen_new_representations,
             "new representation collision")
        seen_new_representations.add(representation_id)
        equality = {
            "projection_map": "(t,p,s)->(p,s)",
            "C10_exact_support_ref": c10[graph]["ref"],
            "exact_graph_support_ast_sha256": c10[graph]["support_sha"],
            "exact_graph_projection_base_ast_sha256": base_sha,
            "new_exact_sheet_support_ast_sha256": base_sha,
            "one_graph_point_for_every_exact_base_point": True,
            "every_graph_point_projects_into_exact_base": True,
            "projection_is_bijection": True,
            "new_sheet_support_equals_exact_graph_projection": True,
        }
        equality["certificate_sha256"] = obj(equality)
        sheet_builder.add(close({
            "schema": SCHEMA + ".exact-sheet-member-row.v1",
            "row_id": PREFIX + ":exact-sheet:" + obj([graph, new]),
            "sheet_ordinal": sheet_builder.count,
            "graph_id": graph,
            "new_exact_sheet_member_id": new,
            "new_exact_sheet_natural_key": partial["proposed_exact_sheet_natural_key"],
            "C14a_partial_frontier_ref": ref(partial),
            "exact_partial_base_ast": base,
            "exact_partial_base_ast_sha256": base_sha,
            "sheet_construction_kind": "EXACT_PARTIAL_BASE_SHEET_DEFINED_BY_C10_GRAPH_PROJECTION",
            "graph_to_new_sheet_set_equality_certificate": equality,
            "new_canonical_representation_id": representation_id,
            "new_canonical_representation_ast": {
                "ast_kind": "EXACT_PARTIAL_BASE_SHEET_CANONICAL_REPRESENTATION",
                "owner_member_id": new,
                "support_ast_sha256": base_sha,
            },
            "exact_sheet_identity_construction_credit": 1,
            "registry_member_admission_credit": 0,
            "canonical_representation_definition_credit": 1,
            "representation_universe_admission_credit": 0,
            "graph_sheet_set_equality_credit": 1,
            "representation_pullback_credit": 0,
            "base_root_or_component_inheritance_credit": 0,
            "DSU_edge_or_union_authorized": False,
            "downstream_nonpromotion": ZERO,
        }))
        old_member = c6[old]
        old_identity = identities[old]
        old_representation = representations[old]
        disposition_builder.add(close({
            "schema": SCHEMA + ".outer-envelope-disposition-row.v1",
            "row_id": PREFIX + ":outer-envelope-disposition:" + obj([graph, old, new]),
            "disposition_ordinal": disposition_builder.count,
            "graph_id": graph,
            "old_outer_envelope_sheet_member_id": old,
            "new_exact_sheet_member_id": new,
            "C14a_partial_frontier_ref": ref(partial),
            "C6_old_member_ref": ref(old_member),
            "C7_old_identity_ref": ref(old_identity),
            "C7_old_representation_ref": ref(old_representation),
            "old_outer_envelope_physical_member_retained": True,
            "old_outer_envelope_representation_retained": True,
            "old_graph_to_outer_envelope_relation_disposition":
                "INVALID_AS_SET_EQUALITY__OUTER_ENVELOPE_STRICTLY_COARSER",
            "old_member_family_before": "G2A",
            "old_member_family_after": "UNRESOLVED_PENDING_SEALED_FAMILY_AUTHORITY",
            "old_member_reclassification_credit": 0,
            "old_member_deletion_or_invalidation_credit": 0,
            "old_component_or_edge_transfer_to_new_member_credit": 0,
            "DSU_edge_or_union_authorized": False,
            "representation_pullback_credit": 0,
            "downstream_nonpromotion": ZERO,
        }))

    sheet_wire, sheet_descriptor = sheet_builder.finish()
    disposition_wire, disposition_descriptor = disposition_builder.finish()
    need(sheet_descriptor["row_count"] == disposition_descriptor["row_count"] == 4432,
         "output census")
    c7_result = json.loads(sources["C7_RESULT"].read_bytes())
    need(c7_result["fresh_base"]["member_count"] == 497772 and
         c7_result["fresh_census"]["representation_count"] == 545184,
         "C7 base census")
    source = Path(__file__).read_bytes()
    body = {
        "schema": SCHEMA,
        "status": "PASS_4432_EXACT_SHEET_IDENTITIES_CONSTRUCTED__REGISTRY_ADMISSION_AND_OLD_FAMILY_DISPOSITION_PENDING",
        "producer_source": {
            "filename": Path(__file__).name,
            "size": len(source),
            "sha256": hashlib.sha256(source).hexdigest(),
        },
        "source_pins": [pin.__dict__ for pin in PINS],
        "source_exhaustion": {
            "C10_graph_rows": c10_total,
            "C6_members": c6_total,
            "C7_identity_rows": identity_total,
            "C7_representation_rows": representation_total,
            "target_old_members": len(old_ids),
            "target_new_members": len(new_ids),
            "new_member_id_collisions": new_collisions,
            "new_identity_id_collisions": identity_new_collisions,
            "new_representation_id_collisions": 0,
        },
        "census": {
            "exact_partial_sheet_identities_constructed": 4432,
            "new_graph_sheet_set_equalities": 4432,
            "old_outer_envelope_relations_disposed": 4432,
            "old_outer_envelope_members_retained": 4432,
            "old_outer_envelope_family_dispositions_unresolved": 4432,
            "new_canonical_representation_definitions": 4432,
            "candidate_member_count_if_admitted": 502204,
            "candidate_representation_count_if_admitted": 549616,
            "known_valid_G2A_graph_sheet_member_count": 5264,
            "sealed_NON_GRAPH_member_count_before_old_family_disposition": 51172,
            "valid_physical_relation_denominator": 15224,
            "valid_graph_to_sheet_relations": 5264,
            "valid_graph_to_side_relations": 9960,
        },
        "scoped_credit": {
            "new_exact_sheet_identity_construction": 4432,
            "new_canonical_representation_definition": 4432,
            "new_graph_sheet_set_equality": 4432,
            "old_outer_envelope_relation_disposition": 4432,
            "old_outer_envelope_member_retention": 4432,
        },
        "formal_credit": ZERO,
        "strict_nonpromotion": {
            "new_member_base_roots_assigned": 0,
            "new_member_components_assigned": 0,
            "new_registry_members_admitted": 0,
            "new_representations_admitted": 0,
            "old_components_or_edges_inherited": 0,
            "new_DSU_edges": 0,
            "representation_pullback_proved": False,
            "normalized_support_sealed": False,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "exact_sheet_member_ledger": sheet_descriptor,
        "outer_envelope_disposition_ledger": disposition_descriptor,
        "fresh_member_universe_and_DSU_replay_triggered_if_registry_admitted": True,
        "required_next": "SEAL_4432_OLD_OUTER_ENVELOPE_FAMILY_DISPOSITIONS_AND_NEW_MEMBER_ROOT_EDGE_AUTHORITY_THEN_FRESH_DSU_REPLAY",
    }
    return {**body, "result_sha256": obj(body)}, sheet_wire, disposition_wire


def write(directory: Path, filename: str, content: bytes) -> None:
    output = directory / filename
    need(not output.exists(), "no clobber:" + filename)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        offset = 0
        while offset < len(content):
            offset += os.write(fd, content[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    need((args.candidate_dir is not None) != args.publish, "one mode")
    result, sheets, dispositions = build()
    directory = ROOT if args.publish else Path(args.candidate_dir).resolve()
    if not args.publish:
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    write(directory, SHEETS, sheets)
    write(directory, DISPOSITIONS, dispositions)
    write(directory, RESULT, canonical(result))
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"]},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
