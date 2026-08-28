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
PREFIX = "cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion"
SCHEMA = "cm2.round306c14d.source-g-exact-sheet-to-side-edge-promotion.v1"
EDGES = PREFIX + "_edge_promotion_ledger.jsonl.gz"
NEGATIVE = PREFIX + "_negative_disposition_ledger.jsonl.gz"
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
    return {**row, "row_sha256": obj(row)}


def ref(row: dict[str, Any]) -> dict[str, str]:
    return {"row_id": row["row_id"], "row_sha256": row["row_sha256"]}


@dataclass(frozen=True)
class Pin:
    name: str
    filename: str
    size: int
    sha256: str


PINS = [
    Pin("C14C_ADMISSION", "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz", 2526805, "7f65ab28ad43a762d1e02bbd9d869965950b7b6d6db9cceef3fdd8cef12cc205"),
    Pin("C14C_RESULT", "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_result.json", 4684, "9484448678ae157ab7fb9f061cf4fd986bc269d535a98651f5e4e4fb5c9f8e98"),
    Pin("C11A_KERNEL", "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_ledger.jsonl.gz", 18096972, "87a37e007408adf667ae30a7575c928263512bf8a08cfd9e7144db11296680cd"),
    Pin("C11A_RESULT", "cm2_round306c11a_source_g_r235_side_sign_stratum_and_trace_kernel_result.json", 7892, "0450965cdebb245532fbfd2875d78306b0f2d237ef3976ec29f9bcf9038abdb8"),
    Pin("C6_MEMBER", "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz", 213125489, "730a1501402d29f9689655b0093edd4d7e499f3a34c6b65e9f21ee6f3f5ffce2"),
]

ZERO = {"representation_pullback": 0, "member_normalized_support": 0,
        "global_normalized_support": 0, "DSU_union": 0, "fresh_component_assignment": 0,
        "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0}


def sources() -> dict[str, Path]:
    out = {}
    for pin in PINS:
        p = ROOT / pin.filename
        need(p.is_file() and not p.is_symlink(), "pin regular:" + pin.name)
        raw = p.read_bytes()
        need(len(raw) == pin.size and hashlib.sha256(raw).hexdigest() == pin.sha256,
             "pin bytes:" + pin.name)
        out[pin.name] = p
    return out


def rows(path: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for line in stream:
            row = json.loads(line)
            claimed = row.pop("row_sha256")
            need(claimed == obj(row), label + " row closure")
            row["row_sha256"] = claimed
            yield row


class Ledger:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.buf = io.BytesIO()
        self.gz = gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                                fileobj=self.buf, mtime=0)
        self.count = 0
        self.plain = hashlib.sha256()

    def add(self, row: dict[str, Any]) -> None:
        wire = canonical(close(row)) + b"\n"
        self.gz.write(wire)
        self.plain.update(wire)
        self.count += 1

    def finish(self) -> tuple[bytes, dict[str, Any]]:
        self.gz.close()
        raw = self.buf.getvalue()
        return raw, {"filename": self.filename, "row_count": self.count, "size": len(raw),
                     "sha256": hashlib.sha256(raw).hexdigest(),
                     "uncompressed_sha256": self.plain.hexdigest()}


def build() -> tuple[dict[str, Any], bytes, bytes]:
    src = sources()
    c14c_result = json.loads(src["C14C_RESULT"].read_bytes())
    core = dict(c14c_result)
    claimed = core.pop("result_sha256")
    need(claimed == obj(core) and c14c_result["formal_credit"]["new_registry_member_admission"] == 4432 and
         c14c_result["strict_nonpromotion"]["new_DSU_edges"] == 0, "C14c result scope")
    c11a_result = json.loads(src["C11A_RESULT"].read_bytes())
    c11core = dict(c11a_result)
    c11claimed = c11core.pop("result_sha256")
    need(c11claimed == obj(c11core), "C11a result closure")

    admissions: dict[str, dict[str, Any]] = {}
    new_ids: set[str] = set()
    for row in rows(src["C14C_ADMISSION"], "C14c admission"):
        graph = row["graph_id"]
        need(graph not in admissions and row["registry_member_admission_credit"] == 1 and
             row["self_root_authority_credit"] == 1 and row["DSU_edge_or_union_authorized"] is False,
             "C14c admission scope")
        admissions[graph] = row
        new_ids.add(row["new_exact_sheet_member_id"])
    need(len(admissions) == 4432, "C14c admission exhaustion")

    kernels: list[dict[str, Any]] = []
    graph_counts: dict[str, int] = {}
    side_ids: set[str] = set()
    c11_total = 0
    for row in rows(src["C11A_KERNEL"], "C11a kernel"):
        c11_total += 1
        graph = row["graph_id"]
        if graph in admissions:
            need(row["scoped_credit"] == {"local_graph_side_physical_incidence": 1,
                                          "one_sided_trace": 1} and
                 row["strict_nonpromotion"]["DSU_edge_or_union_authorized"] is False,
                 "C11a theorem scope")
            kernels.append(row)
            graph_counts[graph] = graph_counts.get(graph, 0) + 1
            side_ids.add(row["side_member_id"])
    need(c11_total == 9422 and len(kernels) == 8864 and len(graph_counts) == 4432 and
         set(graph_counts.values()) == {2} and len(side_ids) == 8864,
         "C11a join exhaustion")

    sides: dict[str, dict[str, Any]] = {}
    c6_total = 0
    c6_new_collision = 0
    for row in rows(src["C6_MEMBER"], "C6 member"):
        c6_total += 1
        member = row["registry_member_id"]
        if member in new_ids:
            c6_new_collision += 1
        if member in side_ids:
            need(member not in sides, "side member unique")
            sides[member] = row
    need(c6_total == 497772 and c6_new_collision == 0 and len(sides) == 8864,
         "C6 side exhaustion")

    edge_ledger = Ledger(EDGES)
    negative_ledger = Ledger(NEGATIVE)
    edge_ids: set[str] = set()
    root_pairs: set[tuple[str, str]] = set()
    side_roots: set[str] = set()
    side_components: set[str] = set()
    key_matches = 0
    for kernel in sorted(kernels, key=lambda r: (r["graph_id"], r["side_member_id"])):
        admission = admissions[kernel["graph_id"]]
        side = sides[kernel["side_member_id"]]
        new_root = admission["self_base_root_id"]
        side_root = side["new_base_root_id"]
        need(new_root != side_root and side["registry_member_id"] == kernel["side_member_id"],
             "edge endpoint authority")
        pair = tuple(sorted((new_root, side_root)))
        edge_id = "round306c14d-exact-sheet-side-edge:" + obj([
            admission["new_exact_sheet_member_id"], kernel["side_member_id"],
            kernel["graph_id"], kernel["side_role"]])
        need(edge_id not in edge_ids and pair not in root_pairs, "edge/root-pair unique")
        edge_ids.add(edge_id)
        root_pairs.add(pair)
        side_roots.add(side_root)
        side_components.add(side["fresh_component_id"])
        if admission["official_key_id"] == side["official_key_id"]:
            key_matches += 1
        edge_ledger.add({
            "schema": SCHEMA + ".edge-promotion-row.v1",
            "row_id": PREFIX + ":edge-promotion:" + obj([edge_id, pair]),
            "edge_ordinal": edge_ledger.count,
            "promoted_edge_id": edge_id,
            "graph_id": kernel["graph_id"],
            "new_exact_sheet_member_id": admission["new_exact_sheet_member_id"],
            "side_member_id": kernel["side_member_id"],
            "side_role": kernel["side_role"],
            "new_exact_sheet_self_root_id": new_root,
            "side_existing_base_root_id": side_root,
            "projected_base_root_pair": list(pair),
            "new_exact_sheet_official_key_id": admission["official_key_id"],
            "side_official_key_id": side["official_key_id"],
            "C14c_admission_ref": ref(admission),
            "C11a_local_theorem_ref": ref(kernel),
            "C6_side_member_ref": ref(side),
            "composition_certificate": {
                "graph_equals_new_exact_sheet": True,
                "graph_in_relative_closure_of_side": True,
                "one_sided_trace_to_graph": True,
                "new_exact_sheet_in_relative_closure_of_side": True,
                "kind": "SET_EQUALITY_TRANSPORTS_C11A_CLOSURE_INCIDENCE_TO_NEW_EXACT_SHEET",
                "certificate_sha256": obj([admission["row_sha256"], kernel["row_sha256"],
                                           side["row_sha256"], pair]),
            },
            "edge_promotion_credit": 1,
            "negative_disposition_required": False,
            "fed_to_fresh_DSU_pending": True,
            "fresh_DSU_application_credit": 0,
            "DSU_union_or_component_credit": 0,
            "downstream_nonpromotion": ZERO,
        })

    need(len(edge_ids) == len(root_pairs) == 8864 and len(side_roots) == 6920 and
         len(side_components) == 4172 and key_matches == 4432,
         "edge census")
    ewire, edesc = edge_ledger.finish()
    nwire, ndesc = negative_ledger.finish()
    need(edesc["row_count"] == 8864 and ndesc["row_count"] == 0, "output census")
    source = Path(__file__).read_bytes()
    body = {
        "schema": SCHEMA,
        "status": "PASS_8864_OF_8864_EDGE_PROMOTIONS_SEALED__FRESH_DSU_PENDING",
        "producer_source": {"filename": Path(__file__).name, "size": len(source),
                            "sha256": hashlib.sha256(source).hexdigest()},
        "source_pins": [p.__dict__ for p in PINS],
        "source_exhaustion": {
            "C14c_admission_rows": len(admissions), "C11a_kernel_rows": c11_total,
            "C14c_C11a_join_rows": len(kernels), "joined_graphs": len(graph_counts),
            "relations_per_graph": 2, "C6_member_rows": c6_total,
            "joined_side_members": len(sides), "new_member_C6_collisions": c6_new_collision,
            "duplicate_edge_ids": 0, "duplicate_projected_root_pairs": 0,
            "unpromotable_rows": 0,
        },
        "formal_edge_authority_census": {
            "promoted_edges": 8864, "negative_dispositions": 0,
            "new_exact_sheet_endpoints": 4432, "side_member_endpoints": 8864,
            "distinct_existing_side_roots": 6920, "distinct_existing_side_components": 4172,
            "same_official_key_edges": 4432, "cross_official_key_edges": 4432,
        },
        "formal_credit": {"legal_new_sheet_to_side_edges": 8864,
                          "rowwise_negative_dispositions": 0},
        "strict_nonpromotion": {
            "fresh_DSU_applied_edges": 0, "fresh_DSU_rank_reduction": 0,
            "fresh_components_assigned": 0, "representation_pullback": 0,
            "normalized_support": 0, "B1A": 0, "B2": 0,
            "maximality": 0, "CM2": "NO-GO_FOR_CLAIM",
        },
        "conditional_not_yet_credited_fresh_DSU_census_if_all_sealed_edges_are_applied": {
            "member_count": 502204, "base_root_count": 339036,
            "applied_edge_count": 484982, "rank_reduction": 281160,
            "component_count": 57876, "cross_component_pair_denominator": 125616475670,
            "formal_credit": 0,
        },
        "corrected_physical_relation_denominator": {
            "total": 15224, "graph_to_sheet": 5264, "graph_to_side": 9960,
        },
        "edge_promotion_ledger": edesc,
        "negative_disposition_ledger": ndesc,
        "required_next": "BUILD_FRESH_MEMBER_EDGE_SEAL_AND_DSU_THEN_REPLAY_C6_THROUGH_C14_BEFORE_PULLBACK",
    }
    return {**body, "result_sha256": obj(body)}, ewire, nwire


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
    result, edges, negative = build()
    directory = ROOT if args.publish else Path(args.candidate_dir).resolve()
    if not args.publish:
        directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    write(directory, EDGES, edges)
    write(directory, NEGATIVE, negative)
    write(directory, RESULT, canonical(result))
    print(json.dumps({"status": result["status"], "result_sha256": result["result_sha256"]},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
