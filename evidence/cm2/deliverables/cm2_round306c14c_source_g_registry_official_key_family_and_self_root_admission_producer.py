#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission"
SCHEMA = "cm2.round306c14c.source-g-registry-official-key-family-and-self-root-admission.v1"
ADMISSIONS = PREFIX + "_new_exact_sheet_admission_ledger.jsonl.gz"
FAMILIES = PREFIX + "_old_outer_envelope_family_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"


def need(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def obj(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(row: dict[str, Any]) -> dict[str, Any]:
    body = dict(row)
    return {**body, "row_sha256": obj(body)}


def ref(row: dict[str, Any]) -> dict[str, str]:
    return {"row_id": row["row_id"], "row_sha256": row["row_sha256"]}


@dataclass(frozen=True)
class Pin:
    name: str
    filename: str
    size: int
    sha256: str


PINS = [
    Pin("C14B_EXACT", "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_exact_sheet_member_ledger.jsonl.gz", 7121724, "6f69b5e82377cde72e7223e86b518da12e19ef85b93a5706989ebb81ab78a6d6"),
    Pin("C14B_DISPOSITION", "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_outer_envelope_disposition_ledger.jsonl.gz", 2406374, "20211713323322593d0992008448fc97216ae91cf9055a22312f3080bd363fb0"),
    Pin("C14B_RESULT", "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta_result.json", 5250, "48ef2f629a17ccea59eadfc5f4e3b9fe8486e09f6af9c36e4663236a0364c2e7"),
    Pin("C6_MEMBER", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213125489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
    Pin("C6_INVALIDATION", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_invalidation_ledger.jsonl.gz", 37615714, "7f4c361b5039b9adac60cdb08405f384dc4a05bbe66b4ae2eac49ac02204e3db"),
    Pin("C7_IDENTITY", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_member_identity_support_ledger.jsonl.gz", 269633111, "de85e6f26b64299d70c5006df76c5e4a242dc46d5b4885bca1f37b13d923c4e0"),
    Pin("C7_REPRESENTATION", "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_representation_ledger.jsonl.gz", 240400592, "1dc805b60f15ec8491b5200ccf9f04a239ce1532f6845a026045709feaaaa468"),
    Pin("C8_FRONTIER", "cm2_round306c8_source_g_fresh_full_support_authority_frontier.json", 98772, "1ec052ba9a6c26929d3a8242f3d12f405640f6399c331977acf51a315e201792"),
    Pin("R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205148977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
]

ZERO = {"representation_pullback": 0, "member_normalized_support": 0,
        "global_normalized_support": 0, "DSU_edge": 0, "DSU_union": 0,
        "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}


def pin_paths() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for pin in PINS:
        p = ROOT / pin.filename
        need(p.is_file() and not p.is_symlink(), "pin regular:" + pin.name)
        data = p.read_bytes()
        need(len(data) == pin.size and hashlib.sha256(data).hexdigest() == pin.sha256,
             "pin bytes:" + pin.name)
        out[pin.name] = p
    return out


def rows(path: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        for ordinal, line in enumerate(handle):
            row = json.loads(line)
            digest = row.pop("row_sha256")
            need(obj(row) == digest, label + " row hash")
            row["row_sha256"] = digest
            yield row
        need(ordinal >= 0, label + " nonempty")


class Ledger:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.buf = io.BytesIO()
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.buf, mtime=0, compresslevel=9)
        self.count = 0
        self.uncompressed = hashlib.sha256()

    def add(self, row: dict[str, Any]) -> None:
        closed = close(row)
        wire = canonical(closed) + b"\n"
        self.uncompressed.update(wire)
        self.gz.write(wire)
        self.count += 1

    def finish(self) -> tuple[bytes, dict[str, Any]]:
        self.gz.close()
        wire = self.buf.getvalue()
        return wire, {"filename": self.filename, "row_count": self.count,
                      "size": len(wire), "sha256": hashlib.sha256(wire).hexdigest(),
                      "uncompressed_sha256": self.uncompressed.hexdigest()}


def build() -> tuple[dict[str, Any], bytes, bytes]:
    src = pin_paths()
    c14b = json.loads(src["C14B_RESULT"].read_bytes())
    need(c14b["result_sha256"] == obj({k: v for k, v in c14b.items() if k != "result_sha256"}),
         "C14b result closure")
    need(c14b["census"]["exact_partial_sheet_identities_constructed"] == 4432 and
         c14b["strict_nonpromotion"]["new_registry_members_admitted"] == 0,
         "C14b scope")

    exact: dict[str, dict[str, Any]] = {}
    exact_by_graph: dict[str, dict[str, Any]] = {}
    for row in rows(src["C14B_EXACT"], "C14b exact"):
        new = row["new_exact_sheet_member_id"]
        graph = row["graph_id"]
        need(new not in exact and graph not in exact_by_graph and
             row["exact_sheet_identity_construction_credit"] == 1 and
             row["graph_sheet_set_equality_credit"] == 1 and
             row["registry_member_admission_credit"] == 0 and
             row["representation_universe_admission_credit"] == 0,
             "C14b exact scope")
        exact[new] = row
        exact_by_graph[graph] = row
    need(len(exact) == 4432, "C14b exact exhaustion")

    disposition: dict[str, dict[str, Any]] = {}
    for row in rows(src["C14B_DISPOSITION"], "C14b disposition"):
        old = row["old_outer_envelope_sheet_member_id"]
        need(old not in disposition and row["new_exact_sheet_member_id"] in exact and
             row["old_outer_envelope_physical_member_retained"] is True and
             row["old_outer_envelope_representation_retained"] is True and
             row["old_member_reclassification_credit"] == 0 and
             row["old_member_deletion_or_invalidation_credit"] == 0,
             "C14b disposition scope")
        need(row["graph_id"] == exact[row["new_exact_sheet_member_id"]]["graph_id"],
             "C14b graph join")
        disposition[old] = row
    need(len(disposition) == 4432, "C14b disposition exhaustion")

    old_ids = set(disposition)
    new_ids = set(exact)
    c6_old: dict[str, dict[str, Any]] = {}
    old_roots: set[str] = set()
    c6_members: set[str] = set()
    c6_total = 0
    for row in rows(src["C6_MEMBER"], "C6 member"):
        c6_total += 1
        member = row["registry_member_id"]
        need(member not in c6_members, "C6 member unique")
        c6_members.add(member)
        old_roots.add(row["new_base_root_id"])
        if member in old_ids:
            c6_old[member] = row
    need(c6_total == 497772 and len(c6_old) == 4432 and not (new_ids & c6_members),
         "C6 exhaustion and new collision")

    invalid_target = set()
    invalid_total = 0
    for row in rows(src["C6_INVALIDATION"], "C6 invalidation"):
        invalid_total += 1
        if row["registry_member_id"] in old_ids:
            invalid_target.add(row["registry_member_id"])
    need(invalid_total == 66688 and not invalid_target, "old sheet not invalidated")

    identities: dict[str, dict[str, Any]] = {}
    identity_total = 0
    for row in rows(src["C7_IDENTITY"], "C7 identity"):
        identity_total += 1
        member = row["member_id"]
        if member in old_ids:
            need(member not in identities and row["coarse_family"] == "G2A",
                 "old identity family")
            identities[member] = row
    need(identity_total == 497772 and len(identities) == 4432, "C7 identity exhaustion")

    representations: dict[str, dict[str, Any]] = {}
    old_rep_ids: set[str] = set()
    representation_total = 0
    for row in rows(src["C7_REPRESENTATION"], "C7 representation"):
        representation_total += 1
        owner = row["owner_member_id"]
        old_rep_ids.add(row["representation_id"])
        if owner in old_ids:
            need(owner not in representations and row["coarse_family"] == "G2A",
                 "old representation family")
            representations[owner] = row
    need(representation_total == 545184 and len(representations) == 4432,
         "C7 representation exhaustion")
    need(all(r["new_canonical_representation_id"] not in old_rep_ids for r in exact.values()),
         "new representation collision")

    c8 = json.loads(src["C8_FRONTIER"].read_bytes())
    auth = [r for r in c8["table_authorities"]
            if r["authority"] == "R248.formal_wall_half_open_sheet_owner_ledger"]
    need(len(auth) == 1 and auth[0]["admitted_for_construction"] is True and
         auth[0]["authority_role"] == "CONSTRUCTION_LINEAGE" and
         auth[0]["row_count"] == 38360 and
         auth[0]["source_sha256"] == PINS[-1].sha256,
         "C8 R248 construction authority")

    r248 = json.loads(src["R248"].read_bytes())
    owner_rows = r248["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    need(len(owner_rows) == 38360, "R248 owner row count")
    owners: dict[str, dict[str, Any]] = {}
    for row in owner_rows:
        old = row["wall_sheet_node_id"]
        if old in old_ids:
            need(old not in owners and row["source_partition_kind"] == "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET" and
                 row["endpoint_factor"] == "target" and
                 row["exact_positive_2D_sheet_area"] != "0" and
                 row["sheet_three_dimensional_coordinate_volume"] == "0" and
                 row["owner_edge_current_quotient_lower_bound_credit"] == 1,
                 "R248 retained physical sheet")
            owners[old] = row
    need(len(owners) == 4432, "R248 target exhaustion")

    admission = Ledger(ADMISSIONS)
    family = Ledger(FAMILIES)
    keys: set[str] = set()
    roots: set[str] = set()
    components: set[str] = set()
    for old in sorted(old_ids):
        disp = disposition[old]
        new = disp["new_exact_sheet_member_id"]
        sheet = exact[new]
        old_member = c6_old[old]
        identity = identities[old]
        representation = representations[old]
        owner = owners[old]
        official = old_member["official_key_id"]
        need(owner["owner_official_key_id"] == official and
             owner["source_partition_row_id"] == sheet["graph_id"],
             "official key and graph authority join")
        keys.add(official)
        components.add(old_member["fresh_component_id"])
        self_root = "round306c14c-exact-partial-sheet-self-root:" + obj([new, official])
        need(self_root not in old_roots and self_root not in roots, "self root collision")
        roots.add(self_root)
        family.add({
            "schema": SCHEMA + ".old-family-disposition-row.v1",
            "row_id": PREFIX + ":old-family-disposition:" + obj([old, new, official]),
            "disposition_ordinal": family.count,
            "old_outer_envelope_sheet_member_id": old,
            "new_exact_sheet_member_id": new,
            "graph_id": sheet["graph_id"],
            "official_key_id": official,
            "C14b_disposition_ref": ref(disp),
            "C6_old_member_ref": ref(old_member),
            "C7_old_identity_ref": ref(identity),
            "C7_old_representation_ref": ref(representation),
            "R248_owner_row_sha256": owner["row_sha256"],
            "R248_exact_positive_2D_sheet_area": owner["exact_positive_2D_sheet_area"],
            "R248_sheet_three_dimensional_coordinate_volume": owner["sheet_three_dimensional_coordinate_volume"],
            "old_member_retained": True,
            "old_representation_retained": True,
            "old_member_independently_nonempty_construction_row": True,
            "old_member_not_C6_invalidated": True,
            "old_graph_relation_is_set_equality": False,
            "old_family_before": "G2A",
            "old_family_after": "NON_GRAPH",
            "forced_family_disposition_credit": 1,
            "member_deletion_or_invalidation_credit": 0,
            "old_root_or_component_changed": False,
            "DSU_edge_or_union_authorized": False,
            "downstream_nonpromotion": ZERO,
        })
        admission.add({
            "schema": SCHEMA + ".new-exact-sheet-admission-row.v1",
            "row_id": PREFIX + ":new-exact-sheet-admission:" + obj([new, official, self_root]),
            "admission_ordinal": admission.count,
            "new_exact_sheet_member_id": new,
            "new_canonical_representation_id": sheet["new_canonical_representation_id"],
            "graph_id": sheet["graph_id"],
            "official_key_id": official,
            "self_base_root_id": self_root,
            "C14b_exact_sheet_ref": ref(sheet),
            "C14b_old_disposition_ref": ref(disp),
            "C6_old_member_ref_for_official_key_only": ref(old_member),
            "R248_owner_row_sha256": owner["row_sha256"],
            "C8_authority": "R248.formal_wall_half_open_sheet_owner_ledger:CONSTRUCTION_LINEAGE",
            "registry_member_admission_credit": 1,
            "G2A_family_admission_credit": 1,
            "canonical_representation_admission_credit": 1,
            "official_key_binding_credit": 1,
            "self_root_authority_credit": 1,
            "official_key_shared_with_old_member": True,
            "old_root_or_component_inheritance_credit": 0,
            "self_root_is_distinct_from_all_C6_roots": True,
            "fresh_component_assignment_credit": 0,
            "DSU_edge_or_union_authorized": False,
            "representation_pullback_credit": 0,
            "downstream_nonpromotion": ZERO,
        })

    need(len(keys) == 32 and len(roots) == 4432 and len(components) == 192,
         "key/root/component census")
    awire, adesc = admission.finish()
    fwire, fdesc = family.finish()
    need(adesc["row_count"] == fdesc["row_count"] == 4432, "output row count")
    source = Path(__file__).read_bytes()
    body = {
        "schema": SCHEMA,
        "status": "PASS_4432_OLD_FAMILIES_DISPOSED_AND_4432_NEW_EXACT_SHEETS_ADMITTED_WITH_SELF_ROOTS",
        "producer_source": {"filename": Path(__file__).name, "size": len(source),
                            "sha256": hashlib.sha256(source).hexdigest()},
        "source_pins": [pin.__dict__ for pin in PINS],
        "source_exhaustion": {
            "C14b_exact_rows": len(exact), "C14b_disposition_rows": len(disposition),
            "C6_member_rows": c6_total, "C6_invalidation_rows": invalid_total,
            "C7_identity_rows": identity_total, "C7_representation_rows": representation_total,
            "R248_owner_rows": len(owner_rows), "target_R248_rows": len(owners),
            "old_target_invalidation_intersection": 0, "new_member_id_collisions": 0,
            "new_representation_id_collisions": 0, "new_self_root_collisions": 0,
        },
        "formal_member_and_family_census": {
            "member_count": 502204, "representation_count": 549616,
            "authorized_base_root_count_before_edges": 339036,
            "PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336,
            "R292": 9404, "G2A": 5264, "G2B": 10128,
            "distinct_official_keys_for_new_members": 32,
            "old_components_touched_but_not_changed": 192,
        },
        "formal_credit": {
            "old_outer_envelope_forced_NON_GRAPH_family_disposition": 4432,
            "new_registry_member_admission": 4432,
            "new_G2A_family_admission": 4432,
            "new_canonical_representation_admission": 4432,
            "new_official_key_binding": 4432,
            "new_self_root_authority": 4432,
        },
        "strict_nonpromotion": {
            "old_root_collapse": 0, "old_component_transfer": 0,
            "new_member_components_assigned": 0, "new_DSU_edges": 0,
            "new_DSU_unions": 0, "representation_pullback": 0,
            "normalized_support": 0, "B1A": 0, "B2": 0,
            "maximality": 0, "CM2": "NO-GO_FOR_CLAIM",
        },
        "corrected_physical_relation_denominator": {
            "total": 15224, "graph_to_sheet": 5264, "graph_to_side": 9960,
        },
        "new_exact_sheet_admission_ledger": adesc,
        "old_outer_envelope_family_disposition_ledger": fdesc,
        "required_next": "SEAL_8864_C14D_EDGE_PROMOTIONS_OR_NEGATIVE_DISPOSITIONS_THEN_FRESH_DSU_AND_C6_C14_REPLAY",
    }
    return {**body, "result_sha256": obj(body)}, awire, fwire


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
    result, admissions, families = build()
    directory = ROOT if args.publish else Path(args.candidate_dir).resolve()
    if not args.publish:
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    write(directory, ADMISSIONS, admissions)
    write(directory, FAMILIES, families)
    write(directory, RESULT, canonical(result))
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"]},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
