#!/usr/bin/env python3
"""Produce corrected zero-credit G2 exact-join commitments from sealed sources."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final, Iterable


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c3_source_g_corrected_g2_exact_join_filter"
OUTPUT: Final = PREFIX + "_result.json"
SCHEMA: Final = "cm2.round306c3.source-g-corrected-g2-exact-join-filter.v1"
ZERO: Final = {"normalized_support": 0, "representation_cover": 0, "source_graph_definition": 0, "physical_incidence": 0, "pullback_equivalence": 0, "transition": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0}


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C2_MANIFEST", "cm2_round306c2_source_g_corrected_full_support_authority_frontier_manifest.sha256", 1_026, "b015004605876ff7525f3f2a45375c42225e307ef52745cde9adfbd62bdc346f"),
    Pin("C0_INVALID", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    Pin("C0_MEMBER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    Pin("SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    value = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return value.hexdigest()
        value.update(chunk)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            info = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == pin.size, "pin identity:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(identity(opened) == identity(info), "pin race:" + pin.role)
            need(hash_fd(fd) == hash_fd(fd) == pin.sha256, "pin digest:" + pin.role)
            self.fds[pin.role] = fd
            self.ids[pin.role] = identity(opened)
        return self

    def duplicate(self, role: str) -> int:
        fd = os.dup(self.fds[role])
        os.lseek(fd, 0, os.SEEK_SET)
        return fd

    def final(self) -> None:
        for pin in reversed(PINS):
            fd = self.fds[pin.role]
            need(identity(os.fstat(fd)) == self.ids[pin.role], "final fd:" + pin.role)
            need(identity(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[pin.role], "final path:" + pin.role)
            need(hash_fd(fd) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def gzip_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            value = json.load(stream)
        need(type(value) is dict, "gzip document:" + role)
        return value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def jsonl(snapshot: Snapshot, role: str) -> Iterable[dict[str, Any]]:
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for number, line in enumerate(stream):
                row = json.loads(line)
                need(type(row) is dict and line.endswith(b"\n") and canonical(row) + b"\n" == line, "canonical JSONL:" + role + ":" + str(number))
                yield row
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def sequence_sha(values: Iterable[Any]) -> str:
    digest = hashlib.sha256()
    digest.update(b"[")
    first = True
    for value in values:
        if not first:
            digest.update(b",")
        digest.update(canonical(value))
        first = False
    digest.update(b"]")
    return digest.hexdigest()


def commitment(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    return {"row_count": len(rows), "rows_sha256": sequence_sha(rows), "row_ids_sha256": sequence_sha(row[id_field] for row in rows), "row_hashes_sha256": sequence_sha(row["row_sha256"] for row in rows)}


def build() -> dict[str, Any]:
    with Snapshot() as snapshot:
        surviving = {row["registry_member_id"] for row in jsonl(snapshot, "C0_MEMBER")}
        invalid = sorted(row["registry_member_id"] for row in jsonl(snapshot, "C0_INVALID"))
        need(len(surviving) == 564_460 and len(invalid) == len(set(invalid)) == 32 and not surviving.intersection(invalid), "C0 census")
        graph_doc = gzip_document(snapshot, "GRAPH")
        sheet_doc = gzip_document(snapshot, "SHEET")
        side_doc = gzip_document(snapshot, "SIDE")
        gap_doc = gzip_document(snapshot, "GAP")
        graph_rows = graph_doc["graph_source_inventory_rows"]
        sheet_rows = sheet_doc["graph_sheet_join_rows"]
        side_rows = side_doc["graph_side_join_rows"]
        gap_rows = gap_doc["gap_rows"]
        need((len(graph_rows), len(sheet_rows), len(side_rows), len(gap_rows)) == (38_624, 38_624, 76_848, 154_096), "legacy G2 census")

        selected_sheets = [row for row in sheet_rows if row["sheet_member_id"] in surviving]
        sheet_graph_ids = {row["graph_source_inventory_row_id"] for row in selected_sheets}
        selected_side_refs = [row for row in side_rows if row["side_member_id"] in surviving]
        side_graph_ids = {row["graph_source_inventory_row_id"] for row in selected_side_refs}
        selected_graph_ids = sheet_graph_ids | side_graph_ids
        selected_graphs = [row for row in graph_rows if row["Round306B1G0_graph_source_inventory_row_id"] in selected_graph_ids]
        side_by_member: dict[str, dict[str, Any]] = {}
        side_refs_by_member: dict[str, list[dict[str, Any]]] = {}
        for row in selected_side_refs:
            member = row["side_member_id"]
            side_refs_by_member.setdefault(member, []).append(row)
            prior = side_by_member.get(member)
            if prior is None or row["Round306B1G0_graph_side_join_row_id"] < prior["Round306B1G0_graph_side_join_row_id"]:
                side_by_member[member] = row
        selected_sides = [side_by_member[member] for member in sorted(side_by_member)]
        need(len(selected_graphs) == 38_624 and len(selected_sheets) == 38_608, "corrected graph and G2A census")
        need(len(selected_side_refs) == 76_832 and len(selected_sides) == 76_816, "corrected G2B census")
        need(side_graph_ids == selected_graph_ids, "every graph retained by a surviving side")
        orphan_graph_ids = sorted(side_graph_ids - sheet_graph_ids)
        orphan_side_refs = [row for row in selected_side_refs if row["graph_source_inventory_row_id"] in set(orphan_graph_ids)]
        need(len(orphan_graph_ids) == len(orphan_side_refs) == len({row["side_member_id"] for row in orphan_side_refs}) == 16, "surviving side without surviving sheet census")

        duplicate_side_members = sorted(member for member, rows in side_refs_by_member.items() if len(rows) == 2)
        need(len(duplicate_side_members) == 16, "duplicate side member census")
        for member in duplicate_side_members:
            rows = side_refs_by_member[member]
            need(len({row["graph_source_inventory_row_id"] for row in rows}) == len({row["Round306B1G0_graph_side_join_row_id"] for row in rows}) == 2, "duplicate side refs are distinct incidences:" + member)

        invalid_sheet = sorted({row["sheet_member_id"] for row in sheet_rows}.intersection(invalid))
        invalid_side = sorted({row["side_member_id"] for row in side_rows}.intersection(invalid))
        need(len(invalid_sheet) == len(invalid_side) == 16 and not set(invalid_sheet).intersection(invalid_side), "invalid G2 split")
        need(sorted(invalid_sheet + invalid_side) == invalid, "invalid G2 exhaustion")

        selected_sheet_join_ids = {row["Round306B1G0_graph_sheet_join_row_id"] for row in selected_sheets}
        selected_side_join_ids = {row["Round306B1G0_graph_side_join_row_id"] for row in selected_side_refs}
        selected_gaps = []
        gap_kinds: dict[str, int] = {}
        for row in gap_rows:
            incidence = row["incidence_join_row_id"]
            keep = row["graph_source_inventory_row_id"] in selected_graph_ids if incidence is None else incidence in selected_sheet_join_ids or incidence in selected_side_join_ids
            if keep:
                selected_gaps.append(row)
                gap_kinds[row["gap_kind"]] = gap_kinds.get(row["gap_kind"], 0) + 1
        need(len(selected_gaps) == 154_064, "corrected relational gap census")
        need(gap_kinds == {"SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING": 38_624, "GRAPH_TO_SHEET_PHYSICAL_IDENTIFICATION_THEOREM_PENDING": 38_608, "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING": 76_832}, "corrected relational gap kinds")

        body = {
            "schema": SCHEMA,
            "status": "PASS_CORRECTED_G2_RELATIONAL_JOIN__SUPERSEDES_MECHANICAL_OBLIGATION_CENSUS__ZERO_SUPPORT_CREDIT",
            "source_pins": [pin.__dict__ for pin in PINS],
            "legacy_census": {"graph_rows": 38_624, "sheet_rows": 38_624, "side_references": 76_848, "side_distinct_members": 76_832, "gap_rows": 154_096},
            "corrected_census": {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064},
            "invalidated_G2": {"sheet_member_count": 16, "side_member_count": 16, "union_count": 32, "sheet_member_ids_sha256": objsha(invalid_sheet), "side_member_ids_sha256": objsha(invalid_side), "union_member_ids_sha256": objsha(invalid)},
            "relational_survivor_correction": {"graph_without_surviving_sheet_but_with_surviving_side_count": 16, "orphan_graph_ids_sha256": objsha(orphan_graph_ids), "orphan_side_reference_rows_sha256": sequence_sha(orphan_side_refs), "duplicate_side_member_count": 16, "duplicate_side_members_sha256": objsha(duplicate_side_members), "each_duplicate_has_two_distinct_graphs": True, "each_duplicate_has_two_distinct_incidence_rows": True, "side_references_must_not_be_canonicalized_for_incidence_obligations": True},
            "row_commitments": {"graph": commitment(selected_graphs, "Round306B1G0_graph_source_inventory_row_id"), "sheet": commitment(selected_sheets, "Round306B1G0_graph_sheet_join_row_id"), "side_reference": commitment(selected_side_refs, "Round306B1G0_graph_side_join_row_id"), "side_member_canonical": commitment(selected_sides, "Round306B1G0_graph_side_join_row_id"), "gap": commitment(selected_gaps, "Round306B1G0_gap_row_id")},
            "gap_kind_counts": gap_kinds,
            "join_audit": {"unbound_graphs": 0, "unbound_sheets": 0, "unbound_side_references": 0, "invalid_member_antijoin": 0, "sheet_side_member_overlap": 0, "duplicate_graph_ids": 0, "duplicate_sheet_members": 0, "graphs_without_surviving_dependents": 0},
            "canonical_side_member_rule": "MIN_UNSIGNED_ASCII_ROUND306B1G0_GRAPH_SIDE_JOIN_ROW_ID_PER_MEMBER_FOR_IDENTITY_ONLY",
            "corrected_theorem_obligation_census": {"root": 351_904, "dependent": 472_928, "total": 824_832, "prior_C1_C2_mechanical_total": 824_800, "missing_graph_definition_roots_in_prior_mechanical_census": 16, "missing_distinct_side_incidence_relations_in_prior_mechanical_census": 16, "delta_from_prior_mechanical_census": 32, "is_final_feature_ledger_row_count": False},
            "required_supersession": {"C1_mechanical_obligation_census_is_support_semantically_authoritative": False, "C2_embedded_obligation_census_is_support_semantically_authoritative": False, "future_AF2_B1A_B2_must_pin_this_corrected_relational_census": True},
            "formal_blockers": {"source_graph_definition_theorems_pending": 38_624, "physical_incidence_theorems_pending": 115_440, "representation_pullbacks_pending": 115_440, "one_sided_trace_obligations_pending": 76_832, "R236_codimension_two_dispositions_pending": 16},
            "formal_credit": ZERO,
            "normalized_support_sealed": False,
            "B1A_permitted": False,
            "B2_permitted": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**body, "result_sha256": objsha(body)}
        snapshot.final()
        return result


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    need(args.print_result != (args.candidate_dir is not None), "exactly one mode")
    result = build()
    raw = canonical(result)
    if args.print_result:
        sys.stdout.buffer.write(raw + b"\n")
    else:
        target = Path(args.candidate_dir).resolve()
        need(os.path.commonpath((str(target), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        target.mkdir(mode=0o700, exist_ok=False)
        path = target / OUTPUT
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
        try:
            os.write(fd, raw)
            os.fsync(fd)
        finally:
            os.close(fd)
        print(json.dumps({"status": result["status"], "filename": OUTPUT, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "result_sha256": result["result_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
