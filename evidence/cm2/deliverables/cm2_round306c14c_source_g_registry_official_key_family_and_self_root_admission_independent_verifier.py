#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Final, Iterator

ROOT: Final = Path(__file__).resolve().parent
PREFIX: Final = "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission"
ADMISSIONS: Final = PREFIX + "_new_exact_sheet_admission_ledger.jsonl.gz"
FAMILIES: Final = PREFIX + "_old_outer_envelope_family_disposition_ledger.jsonl.gz"
RESULT: Final = PREFIX + "_result.json"
MANIFEST: Final = PREFIX + "_manifest.sha256"
PRODUCER: Final = PREFIX + "_producer.py"
PRODUCER_SHA: Final = "467ab549c405a2587fbd9f85e44e7e58b1531d7a77e931eb7fab32a1eb931b28"


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


def source_rows(path: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        count = 0
        for line in stream:
            row = json.loads(line)
            claimed = row.pop("row_sha256", None)
            need(claimed == obj(row), label + ":row-closure")
            row["row_sha256"] = claimed
            count += 1
            yield row
        need(count > 0, label + ":nonempty")


def candidate_rows(path: Path, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    raw = path.read_bytes()
    need(len(raw) == descriptor["size"] and fsha(path) == descriptor["sha256"],
         label + ":wire")
    h = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    with gzip.open(path, "rb") as stream:
        for line in stream:
            h.update(line)
            row = json.loads(line)
            claimed = row.pop("row_sha256", None)
            need(claimed == obj(row), label + ":row-closure")
            row["row_sha256"] = claimed
            rows.append(row)
    need(len(rows) == descriptor["row_count"] and h.hexdigest() == descriptor["uncompressed_sha256"],
         label + ":descriptor")
    return rows


def manifest_members() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in (ROOT / MANIFEST).read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        need(len(digest) == 64 and name not in out, "manifest syntax")
        out[name] = digest
    return out


def verify(candidate: Path, manifest_first: bool) -> dict[str, Any]:
    if manifest_first:
        members = manifest_members()
        need(len(members) == 9 and all((ROOT / name).is_file() and fsha(ROOT / name) == digest
                                      for name, digest in members.items()), "manifest members")

    result_raw = (candidate / RESULT).read_bytes()
    result = json.loads(result_raw)
    core = dict(result)
    claimed = core.pop("result_sha256", None)
    need(result_raw == canonical(result) and claimed == obj(core), "result closure")
    need(result["producer_source"] == {"filename": PRODUCER, "size": 18518,
                                      "sha256": PRODUCER_SHA}, "producer pin")
    need((ROOT / PRODUCER).stat().st_size == 18518 and fsha(ROOT / PRODUCER) == PRODUCER_SHA,
         "producer bytes")

    pins = result["source_pins"]
    need(len(pins) == 9 and len({p["name"] for p in pins}) == 9, "source pins")
    sources: dict[str, Path] = {}
    for pin in pins:
        path = ROOT / pin["filename"]
        need(path.is_file() and not path.is_symlink(), "source path:" + pin["name"])
        sources[pin["name"]] = path

    admissions = candidate_rows(candidate / ADMISSIONS, result["new_exact_sheet_admission_ledger"],
                                "admission")
    families = candidate_rows(candidate / FAMILIES,
                              result["old_outer_envelope_family_disposition_ledger"], "family")
    need(len(admissions) == len(families) == 4432, "candidate census")
    need(result["formal_member_and_family_census"]["member_count"] == 502204 and
         result["formal_member_and_family_census"]["representation_count"] == 549616 and
         result["strict_nonpromotion"]["new_DSU_edges"] == 0 and
         result["strict_nonpromotion"]["representation_pullback"] == 0,
         "candidate result preflight")
    for row in admissions:
        need(row["registry_member_admission_credit"] == 1 and
             row["G2A_family_admission_credit"] == 1 and
             row["canonical_representation_admission_credit"] == 1 and
             row["official_key_binding_credit"] == 1 and row["self_root_authority_credit"] == 1 and
             row["old_root_or_component_inheritance_credit"] == 0 and
             row["fresh_component_assignment_credit"] == 0 and
             row["DSU_edge_or_union_authorized"] is False and
             row["representation_pullback_credit"] == 0,
             "admission preflight")
    for row in families:
        need(row["old_member_retained"] is True and row["old_representation_retained"] is True and
             row["old_member_not_C6_invalidated"] is True and
             row["old_family_before"] == "G2A" and row["old_family_after"] == "NON_GRAPH" and
             row["forced_family_disposition_credit"] == 1 and
             row["member_deletion_or_invalidation_credit"] == 0 and
             row["old_root_or_component_changed"] is False and
             row["DSU_edge_or_union_authorized"] is False,
             "family preflight")
    for pin in pins:
        path = sources[pin["name"]]
        need(path.stat().st_size == pin["size"] and fsha(path) == pin["sha256"],
             "source pin:" + pin["name"])

    exact: dict[str, dict[str, Any]] = {}
    for row in source_rows(sources["C14B_EXACT"], "C14b exact"):
        new = row["new_exact_sheet_member_id"]
        need(new not in exact and row["registry_member_admission_credit"] == 0 and
             row["representation_universe_admission_credit"] == 0 and
             row["graph_sheet_set_equality_credit"] == 1, "C14b exact scope")
        exact[new] = row
    need(len(exact) == 4432, "C14b exact count")
    dispositions: dict[str, dict[str, Any]] = {}
    for row in source_rows(sources["C14B_DISPOSITION"], "C14b disposition"):
        old = row["old_outer_envelope_sheet_member_id"]
        need(old not in dispositions and row["new_exact_sheet_member_id"] in exact and
             row["old_member_reclassification_credit"] == 0 and
             row["old_member_deletion_or_invalidation_credit"] == 0,
             "C14b disposition scope")
        dispositions[old] = row
    need(len(dispositions) == 4432, "C14b disposition count")

    old_ids = set(dispositions)
    new_ids = set(exact)
    c6: dict[str, dict[str, Any]] = {}
    all_members: set[str] = set()
    all_roots: set[str] = set()
    c6_count = 0
    for row in source_rows(sources["C6_MEMBER"], "C6 member"):
        c6_count += 1
        member = row["registry_member_id"]
        need(member not in all_members, "C6 member unique")
        all_members.add(member)
        all_roots.add(row["new_base_root_id"])
        if member in old_ids:
            c6[member] = row
    need(c6_count == 497772 and len(c6) == 4432 and not (new_ids & all_members),
         "C6 exhaustion")

    invalid = set()
    invalid_count = 0
    for row in source_rows(sources["C6_INVALIDATION"], "C6 invalidation"):
        invalid_count += 1
        if row["registry_member_id"] in old_ids:
            invalid.add(row["registry_member_id"])
    need(invalid_count == 66688 and not invalid, "old invalidation antijoin")

    identities: dict[str, dict[str, Any]] = {}
    identity_count = 0
    for row in source_rows(sources["C7_IDENTITY"], "C7 identity"):
        identity_count += 1
        member = row["member_id"]
        if member in old_ids:
            need(member not in identities and row["coarse_family"] == "G2A", "identity G2A")
            identities[member] = row
    need(identity_count == 497772 and len(identities) == 4432, "identity exhaustion")

    reps: dict[str, dict[str, Any]] = {}
    rep_ids: set[str] = set()
    rep_count = 0
    for row in source_rows(sources["C7_REPRESENTATION"], "C7 representation"):
        rep_count += 1
        rep_ids.add(row["representation_id"])
        owner = row["owner_member_id"]
        if owner in old_ids:
            need(owner not in reps and row["coarse_family"] == "G2A", "representation G2A")
            reps[owner] = row
    need(rep_count == 545184 and len(reps) == 4432 and
         all(r["new_canonical_representation_id"] not in rep_ids for r in exact.values()),
         "representation exhaustion/collision")

    c8 = json.loads(sources["C8_FRONTIER"].read_bytes())
    auth = [r for r in c8["table_authorities"]
            if r["authority"] == "R248.formal_wall_half_open_sheet_owner_ledger"]
    need(len(auth) == 1 and auth[0]["admitted_for_construction"] is True and
         auth[0]["authority_role"] == "CONSTRUCTION_LINEAGE" and auth[0]["row_count"] == 38360,
         "C8 construction authority")
    r248 = json.loads(sources["R248"].read_bytes())
    r248_rows = r248["result"]["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    owners: dict[str, dict[str, Any]] = {}
    for row in r248_rows:
        old = row["wall_sheet_node_id"]
        if old in old_ids:
            need(old not in owners and row["endpoint_factor"] == "target" and
                 row["source_partition_kind"] == "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET" and
                 row["exact_positive_2D_sheet_area"] != "0" and
                 row["sheet_three_dimensional_coordinate_volume"] == "0" and
                 row["owner_edge_current_quotient_lower_bound_credit"] == 1,
                 "R248 retained owner")
            owners[old] = row
    need(len(r248_rows) == 38360 and len(owners) == 4432, "R248 exhaustion")

    by_old = {row["old_outer_envelope_sheet_member_id"]: row for row in families}
    by_new = {row["new_exact_sheet_member_id"]: row for row in admissions}
    need(len(by_old) == len(by_new) == 4432 and set(by_old) == old_ids and set(by_new) == new_ids,
         "candidate key sets")
    ord_a = set()
    ord_f = set()
    keys = set()
    roots = set()
    components = set()
    for old in old_ids:
        disp = dispositions[old]
        new = disp["new_exact_sheet_member_id"]
        sheet = exact[new]
        old_member = c6[old]
        identity = identities[old]
        rep = reps[old]
        owner = owners[old]
        official = old_member["official_key_id"]
        self_root = "round306c14c-exact-partial-sheet-self-root:" + obj([new, official])
        need(owner["owner_official_key_id"] == official and
             owner["source_partition_row_id"] == sheet["graph_id"], "authority join")
        f = by_old[old]
        a = by_new[new]
        need(f["row_id"] == PREFIX + ":old-family-disposition:" + obj([old, new, official]) and
             f["C14b_disposition_ref"] == {"row_id": disp["row_id"], "row_sha256": disp["row_sha256"]} and
             f["C6_old_member_ref"] == {"row_id": old_member["row_id"], "row_sha256": old_member["row_sha256"]} and
             f["C7_old_identity_ref"] == {"row_id": identity["row_id"], "row_sha256": identity["row_sha256"]} and
             f["C7_old_representation_ref"] == {"row_id": rep["row_id"], "row_sha256": rep["row_sha256"]} and
             f["R248_owner_row_sha256"] == owner["row_sha256"] and
             f["old_member_retained"] is True and f["old_representation_retained"] is True and
             f["old_member_not_C6_invalidated"] is True and
             f["old_family_before"] == "G2A" and f["old_family_after"] == "NON_GRAPH" and
             f["forced_family_disposition_credit"] == 1 and
             f["member_deletion_or_invalidation_credit"] == 0 and
             f["old_root_or_component_changed"] is False and
             f["DSU_edge_or_union_authorized"] is False and f["downstream_nonpromotion"] == {
                 "representation_pullback": 0, "member_normalized_support": 0,
                 "global_normalized_support": 0, "DSU_edge": 0, "DSU_union": 0,
                 "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
             "family semantics")
        need(a["row_id"] == PREFIX + ":new-exact-sheet-admission:" + obj([new, official, self_root]) and
             a["new_canonical_representation_id"] == sheet["new_canonical_representation_id"] and
             a["graph_id"] == sheet["graph_id"] and a["official_key_id"] == official and
             a["self_base_root_id"] == self_root and
             a["C14b_exact_sheet_ref"] == {"row_id": sheet["row_id"], "row_sha256": sheet["row_sha256"]} and
             a["registry_member_admission_credit"] == 1 and a["G2A_family_admission_credit"] == 1 and
             a["canonical_representation_admission_credit"] == 1 and
             a["official_key_binding_credit"] == 1 and a["self_root_authority_credit"] == 1 and
             a["old_root_or_component_inheritance_credit"] == 0 and
             a["fresh_component_assignment_credit"] == 0 and
             a["DSU_edge_or_union_authorized"] is False and a["representation_pullback_credit"] == 0,
             "admission semantics")
        need(self_root not in all_roots and self_root not in roots, "self-root antijoin")
        roots.add(self_root)
        keys.add(official)
        components.add(old_member["fresh_component_id"])
        ord_a.add(a["admission_ordinal"])
        ord_f.add(f["disposition_ordinal"])

    need(ord_a == ord_f == set(range(4432)) and len(keys) == 32 and len(roots) == 4432 and
         len(components) == 192, "candidate census")
    need(result["formal_member_and_family_census"] == {
        "member_count": 502204, "representation_count": 549616,
        "authorized_base_root_count_before_edges": 339036,
        "PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336,
        "R292": 9404, "G2A": 5264, "G2B": 10128,
        "distinct_official_keys_for_new_members": 32,
        "old_components_touched_but_not_changed": 192}, "formal census")
    need(sum(result["formal_member_and_family_census"][k]
             for k in ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")) == 502204,
         "family partition")
    need(result["formal_credit"] == {
        "old_outer_envelope_forced_NON_GRAPH_family_disposition": 4432,
        "new_registry_member_admission": 4432, "new_G2A_family_admission": 4432,
        "new_canonical_representation_admission": 4432,
        "new_official_key_binding": 4432, "new_self_root_authority": 4432},
         "formal credit")
    need(result["strict_nonpromotion"] == {
        "old_root_collapse": 0, "old_component_transfer": 0,
        "new_member_components_assigned": 0, "new_DSU_edges": 0, "new_DSU_unions": 0,
        "representation_pullback": 0, "normalized_support": 0, "B1A": 0, "B2": 0,
        "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "nonpromotion")
    need(result["corrected_physical_relation_denominator"] == {
        "total": 15224, "graph_to_sheet": 5264, "graph_to_side": 9960}, "denominator")
    return {"status": "PASS_INDEPENDENT_C14C_VERIFICATION", "result_sha256": claimed,
            "admission_rows": 4432, "family_rows": 4432, "official_keys": 32,
            "self_roots": 4432, "old_components_unchanged": 192}


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--manifest-first", action="store_true")
    args = parser.parse_args()
    need(not (args.candidate_dir and args.manifest_first), "mode")
    candidate = ROOT if args.manifest_first or args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(json.dumps(verify(candidate, args.manifest_first), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)},
                         sort_keys=True, separators=(",", ":")), file=sys.stderr)
        raise SystemExit(1)
