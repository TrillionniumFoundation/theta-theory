#!/usr/bin/env python3
"""Independent verifier for corrected relational G2 exact-join commitments."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from collections import defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Final, Iterable


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c3_source_g_corrected_g2_exact_join_filter"
OUTPUT: Final = PREFIX + "_result.json"
PRODUCER: Final = PREFIX + "_producer.py"
ATTACK: Final = PREFIX + "_attack_suite.json"
VERIFICATION: Final = PREFIX + "_verification.json"
REPORT: Final = PREFIX + "_report.md"
COLD: Final = PREFIX + "_cold_replay.md"
MANIFEST: Final = PREFIX + "_manifest.sha256"
SCHEMA: Final = "cm2.round306c3.source-g-corrected-g2-exact-join-filter.v1"
ZERO: Final = {"normalized_support": 0, "representation_cover": 0, "source_graph_definition": 0, "physical_incidence": 0, "pullback_equivalence": 0, "transition": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0}


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


SOURCE_PINS: Final = (
    Pin("C2_MANIFEST", "cm2_round306c2_source_g_corrected_full_support_authority_frontier_manifest.sha256", 1_026, "b015004605876ff7525f3f2a45375c42225e307ef52745cde9adfbd62bdc346f"),
    Pin("C0_INVALID", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    Pin("C0_MEMBER", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    Pin("SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
)
PRODUCER_PIN: Final = Pin("PRODUCER", PRODUCER, 16_215, "05ead9dbd0b72d8cfdd6ddbecf1795257c4bfd18517a108de5a07d472a51cba0")
PINS: Final = (*SOURCE_PINS, PRODUCER_PIN)
MANIFEST_MEMBERS: Final = (PRODUCER, OUTPUT, Path(__file__).name, ATTACK, VERIFICATION, REPORT, COLD)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def ident(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hashfd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    value = hashlib.sha256()
    while True:
        block = os.read(fd, 1_048_576)
        if not block:
            return value.hexdigest()
        value.update(block)


class Sources:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Sources":
        info = os.stat(ROOT, follow_symlinks=False)
        need(stat.S_ISDIR(info.st_mode) and not ROOT.is_symlink(), "source directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            before = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == pin.size, "source identity:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(ident(opened) == ident(before), "source race:" + pin.role)
            need(hashfd(fd) == hashfd(fd) == pin.sha256, "source digest:" + pin.role)
            self.fds[pin.role] = fd
            self.ids[pin.role] = ident(opened)
        return self

    def duplicate(self, role: str) -> int:
        fd = os.dup(self.fds[role])
        os.lseek(fd, 0, os.SEEK_SET)
        return fd

    def final(self) -> None:
        for pin in reversed(PINS):
            fd = self.fds[pin.role]
            need(ident(os.fstat(fd)) == self.ids[pin.role] and ident(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[pin.role] and hashfd(fd) == pin.sha256, "source final:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def jsonl(sources: Sources, role: str) -> Iterable[dict[str, Any]]:
    fd = sources.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            for number, line in enumerate(stream):
                row = json.loads(line)
                need(type(row) is dict and line.endswith(b"\n") and canonical(row) + b"\n" == line, "JSONL:" + role + ":" + str(number))
                yield row
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def document(sources: Sources, role: str) -> dict[str, Any]:
    fd = sources.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw, gzip.GzipFile(fileobj=raw, mode="rb") as stream:
            value = json.load(stream)
        need(type(value) is dict, "document:" + role)
        return value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def seqsha(values: Iterable[Any]) -> str:
    value = hashlib.sha256()
    value.update(b"[")
    first = True
    for item in values:
        if not first:
            value.update(b",")
        value.update(canonical(item))
        first = False
    value.update(b"]")
    return value.hexdigest()


def commit(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    return {"row_count": len(rows), "rows_sha256": seqsha(rows), "row_ids_sha256": seqsha(row[field] for row in rows), "row_hashes_sha256": seqsha(row["row_sha256"] for row in rows)}


def read_candidate(directory: Path) -> tuple[dict[str, Any], bytes]:
    need(os.path.commonpath((str(directory.resolve()), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
    info = os.stat(directory, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode) and set(os.listdir(directory)) == {OUTPUT}, "candidate exact set")
    path = directory / OUTPUT
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "candidate identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(fd)
        need(ident(opened) == ident(before), "candidate race")
        first = hashfd(fd)
        need(first == hashfd(fd), "candidate digest")
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.read(fd, before.st_size)
        need(len(raw) == before.st_size, "candidate read")
    finally:
        os.close(fd)
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "candidate canonical")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(claimed == objsha(body), "candidate closure")
    candidate_preflight(value)
    return value, raw


def candidate_preflight(value: dict[str, Any]) -> None:
    need(value["schema"] == SCHEMA and value["status"] == "PASS_CORRECTED_G2_RELATIONAL_JOIN__SUPERSEDES_MECHANICAL_OBLIGATION_CENSUS__ZERO_SUPPORT_CREDIT", "candidate identity")
    need(value["source_pins"] == [pin.__dict__ for pin in SOURCE_PINS], "candidate source pins")
    need(value["corrected_census"] == {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064}, "candidate corrected census")
    correction = value["relational_survivor_correction"]
    need(correction["graph_without_surviving_sheet_but_with_surviving_side_count"] == 16 and correction["duplicate_side_member_count"] == 16, "candidate relational correction")
    need(correction["each_duplicate_has_two_distinct_graphs"] is True and correction["each_duplicate_has_two_distinct_incidence_rows"] is True and correction["side_references_must_not_be_canonicalized_for_incidence_obligations"] is True, "candidate duplicate semantics")
    need(value["corrected_theorem_obligation_census"] == {"root": 351_904, "dependent": 472_928, "total": 824_832, "prior_C1_C2_mechanical_total": 824_800, "missing_graph_definition_roots_in_prior_mechanical_census": 16, "missing_distinct_side_incidence_relations_in_prior_mechanical_census": 16, "delta_from_prior_mechanical_census": 32, "is_final_feature_ledger_row_count": False}, "candidate theorem census")
    supersession = value["required_supersession"]
    need(supersession == {"C1_mechanical_obligation_census_is_support_semantically_authoritative": False, "C2_embedded_obligation_census_is_support_semantically_authoritative": False, "future_AF2_B1A_B2_must_pin_this_corrected_relational_census": True}, "candidate supersession")
    need(len(value["row_commitments"]) == 5 and all(value["row_commitments"][role]["row_count"] == count for role, count in {"graph": 38_624, "sheet": 38_608, "side_reference": 76_832, "side_member_canonical": 76_816, "gap": 154_064}.items()), "candidate commitment census")
    need(value["formal_credit"] == ZERO and value["normalized_support_sealed"] is False and value["B1A_permitted"] is False and value["B2_permitted"] is False and value["CM2"] == "NO-GO_FOR_CLAIM", "candidate zero credit")


def replay(candidate: dict[str, Any]) -> dict[str, Any]:
    with Sources() as sources:
        survivors = {row["registry_member_id"] for row in jsonl(sources, "C0_MEMBER")}
        invalid = sorted(row["registry_member_id"] for row in jsonl(sources, "C0_INVALID"))
        need(len(survivors) == 564_460 and len(invalid) == 32, "C0 census")
        graphs = document(sources, "GRAPH")["graph_source_inventory_rows"]
        sheets = document(sources, "SHEET")["graph_sheet_join_rows"]
        sides = document(sources, "SIDE")["graph_side_join_rows"]
        gaps = document(sources, "GAP")["gap_rows"]
        valid_sheets = [row for row in sheets if row["sheet_member_id"] in survivors]
        valid_side_refs = [row for row in sides if row["side_member_id"] in survivors]
        sheet_graphs = {row["graph_source_inventory_row_id"] for row in valid_sheets}
        side_graphs = {row["graph_source_inventory_row_id"] for row in valid_side_refs}
        graph_ids = sheet_graphs | side_graphs
        valid_graphs = [row for row in graphs if row["Round306B1G0_graph_source_inventory_row_id"] in graph_ids]
        refs = defaultdict(list)
        for row in valid_side_refs:
            refs[row["side_member_id"]].append(row)
        canonical_sides = [min(refs[member], key=lambda row: row["Round306B1G0_graph_side_join_row_id"]) for member in sorted(refs)]
        duplicate_members = sorted(member for member, rows in refs.items() if len(rows) == 2)
        need(len(valid_graphs) == 38_624 and len(valid_sheets) == 38_608 and len(valid_side_refs) == 76_832 and len(canonical_sides) == 76_816 and len(duplicate_members) == 16, "corrected census")
        for member in duplicate_members:
            need(len({row["graph_source_inventory_row_id"] for row in refs[member]}) == len({row["Round306B1G0_graph_side_join_row_id"] for row in refs[member]}) == 2, "distinct duplicate incidence")
        orphan_graphs = sorted(side_graphs - sheet_graphs)
        orphan_refs = [row for row in valid_side_refs if row["graph_source_inventory_row_id"] in set(orphan_graphs)]
        need(len(orphan_graphs) == len(orphan_refs) == 16 and side_graphs == graph_ids, "orphan relational roots")
        invalid_sheets = sorted(set(invalid).intersection(row["sheet_member_id"] for row in sheets))
        invalid_sides = sorted(set(invalid).intersection(row["side_member_id"] for row in sides))
        need(len(invalid_sheets) == len(invalid_sides) == 16 and sorted(invalid_sheets + invalid_sides) == invalid, "invalidation exhaustion")
        sheet_joins = {row["Round306B1G0_graph_sheet_join_row_id"] for row in valid_sheets}
        side_joins = {row["Round306B1G0_graph_side_join_row_id"] for row in valid_side_refs}
        valid_gaps = [row for row in gaps if (row["graph_source_inventory_row_id"] in graph_ids if row["incidence_join_row_id"] is None else row["incidence_join_row_id"] in sheet_joins or row["incidence_join_row_id"] in side_joins)]
        need(len(valid_gaps) == 154_064, "gap census")
        expected_commitments = {"graph": commit(valid_graphs, "Round306B1G0_graph_source_inventory_row_id"), "sheet": commit(valid_sheets, "Round306B1G0_graph_sheet_join_row_id"), "side_reference": commit(valid_side_refs, "Round306B1G0_graph_side_join_row_id"), "side_member_canonical": commit(canonical_sides, "Round306B1G0_graph_side_join_row_id"), "gap": commit(valid_gaps, "Round306B1G0_gap_row_id")}
        need(candidate["schema"] == SCHEMA and candidate["status"] == "PASS_CORRECTED_G2_RELATIONAL_JOIN__SUPERSEDES_MECHANICAL_OBLIGATION_CENSUS__ZERO_SUPPORT_CREDIT", "candidate identity")
        need(candidate["source_pins"] == [pin.__dict__ for pin in SOURCE_PINS], "candidate source pins")
        need(candidate["row_commitments"] == expected_commitments, "row commitments")
        need(candidate["corrected_census"] == {"graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_distinct_members": 76_816, "duplicate_side_reference_excess": 16, "physical_incidence_relations": 115_440, "semantic_obligation_rows": 154_064}, "candidate corrected census")
        correction = candidate["relational_survivor_correction"]
        need(correction["graph_without_surviving_sheet_but_with_surviving_side_count"] == 16 and correction["orphan_graph_ids_sha256"] == objsha(orphan_graphs) and correction["orphan_side_reference_rows_sha256"] == seqsha(orphan_refs), "orphan correction")
        need(correction["duplicate_side_members_sha256"] == objsha(duplicate_members) and correction["side_references_must_not_be_canonicalized_for_incidence_obligations"] is True, "duplicate correction")
        need(candidate["corrected_theorem_obligation_census"] == {"root": 351_904, "dependent": 472_928, "total": 824_832, "prior_C1_C2_mechanical_total": 824_800, "missing_graph_definition_roots_in_prior_mechanical_census": 16, "missing_distinct_side_incidence_relations_in_prior_mechanical_census": 16, "delta_from_prior_mechanical_census": 32, "is_final_feature_ledger_row_count": False}, "theorem census correction")
        need(candidate["formal_credit"] == ZERO and candidate["normalized_support_sealed"] is False and candidate["B1A_permitted"] is False and candidate["B2_permitted"] is False and candidate["CM2"] == "NO-GO_FOR_CLAIM", "zero credit")
        sources.final()
    return {"status": "PASS_INDEPENDENT_CORRECTED_G2_RELATIONAL_REPLAY__ZERO_SUPPORT_CREDIT", "candidate_sha256": hashlib.sha256(canonical(candidate)).hexdigest(), "result_sha256": candidate["result_sha256"], "graph_definition_rows": 38_624, "G2A_sheet_members": 38_608, "G2B_side_references": 76_832, "G2B_side_members": 76_816, "semantic_obligation_rows": 154_064, "corrected_theorem_obligation_total": 824_832, "producer_imported_or_executed": False, "formal_credit": ZERO}


def self_sha() -> str:
    path = Path(__file__)
    before = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "verifier identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(ident(os.fstat(fd)) == ident(before), "verifier race")
        value = hashfd(fd)
        need(value == hashfd(fd), "verifier digest")
        return value
    finally:
        os.close(fd)


def rewrite(path: Path, mutator: Any) -> None:
    value = json.loads(path.read_bytes())
    mutator(value)
    body = dict(value)
    body.pop("result_sha256", None)
    value = {**body, "result_sha256": objsha(body)}
    path.write_bytes(canonical(value))


def attack_suite(candidate_dir: Path) -> dict[str, Any]:
    baseline, _ = read_candidate(candidate_dir)
    baseline_receipt = replay(baseline)
    work = Path(tempfile.mkdtemp(prefix="cm2-c3-g2-attacks-"))
    original = candidate_dir / OUTPUT
    attacks = []
    def restore() -> None:
        path = work / OUTPUT
        if path.exists() or path.is_symlink():
            path.unlink()
        shutil.copyfile(original, path)
    def execute(attack_id: str, mutate: Any, cleanup: Any | None = None) -> None:
        restore()
        try:
            mutate()
            boundary = None
            try:
                value, _ = read_candidate(work)
                replay(value)
            except (Rejected, OSError, json.JSONDecodeError) as error:
                boundary = type(error).__name__ + ":" + str(error)
            need(boundary is not None, "attack accepted:" + attack_id)
            body = {"attack_id": attack_id, "rejected": True, "rejection_boundary": boundary}
            attacks.append({**body, "row_sha256": objsha(body)})
        finally:
            if cleanup is not None:
                cleanup()
    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"), lambda: (work / "foreign").unlink())
        execute("A02_MISSING_RESULT", lambda: (work / OUTPUT).unlink())
        execute("A03_SYMLINK_RESULT", lambda: ((work / OUTPUT).unlink(), (work / OUTPUT).symlink_to(original)))
        def hardlink() -> None:
            (work / OUTPUT).unlink()
            target = work.parent / (work.name + "-target")
            shutil.copyfile(original, target)
            os.link(target, work / OUTPUT)
        execute("A04_HARDLINK_RESULT", hardlink, lambda: (work.parent / (work.name + "-target")).unlink())
        execute("A05_STATUS_DOWNGRADE", lambda: rewrite(work / OUTPUT, lambda value: value.__setitem__("status", "PASS_MECHANICAL")))
        execute("A06_GRAPH_ROOT_DROP", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_census"].__setitem__("graph_definition_rows", 38_608)))
        execute("A07_SIDE_REFERENCE_DEDUP", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_census"].__setitem__("G2B_side_references", 76_816)))
        execute("A08_INCIDENCE_DEDUP", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_census"].__setitem__("physical_incidence_relations", 115_424)))
        execute("A09_GAP_DEDUP", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_census"].__setitem__("semantic_obligation_rows", 154_032)))
        execute("A10_OLD_THEOREM_CENSUS", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_theorem_obligation_census"].__setitem__("total", 824_800)))
        execute("A11_ERASE_ORPHAN_GRAPHS", lambda: rewrite(work / OUTPUT, lambda value: value["relational_survivor_correction"].__setitem__("graph_without_surviving_sheet_but_with_surviving_side_count", 0)))
        execute("A12_CANONICALIZE_INCIDENCE", lambda: rewrite(work / OUTPUT, lambda value: value["relational_survivor_correction"].__setitem__("side_references_must_not_be_canonicalized_for_incidence_obligations", False)))
        execute("A13_C2_PIN_SUBSTITUTION", lambda: rewrite(work / OUTPUT, lambda value: value["source_pins"][0].__setitem__("sha256", "0" * 64)))
        execute("A14_CREDIT_INJECTION", lambda: rewrite(work / OUTPUT, lambda value: value["formal_credit"].__setitem__("normalized_support", 1)))
        execute("A15_REAUTHORIZE_C1_CENSUS", lambda: rewrite(work / OUTPUT, lambda value: value["required_supersession"].__setitem__("C1_mechanical_obligation_census_is_support_semantically_authoritative", True)))
        execute("A16_DISABLE_FUTURE_PIN", lambda: rewrite(work / OUTPUT, lambda value: value["required_supersession"].__setitem__("future_AF2_B1A_B2_must_pin_this_corrected_relational_census", False)))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 16, "attack count")
    body = {"schema": SCHEMA + ".coherent-attack-suite.v1", "status": "PASS_16_OF_16_COHERENT_ATTACKS_REJECTED", "verifier_filename": Path(__file__).name, "verifier_file_sha256": self_sha(), "attack_count": 16, "rejected_count": 16, "all_rejected": True, "baseline_candidate_sha256": baseline_receipt["candidate_sha256"], "attacks": attacks}
    return {**body, "attack_suite_sha256": objsha(body)}


def closed_json(path: Path, closure: str) -> tuple[dict[str, Any], bytes]:
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "closed JSON identity:" + path.name)
    raw = path.read_bytes()
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "closed JSON canonical:" + path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(claimed == objsha(body), "closed JSON digest:" + path.name)
    return value, raw


def verification_doc(result: dict[str, Any]) -> dict[str, Any]:
    suite, raw = closed_json(ROOT / ATTACK, "attack_suite_sha256")
    need(suite["verifier_file_sha256"] == self_sha() and (suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (16, 16, True), "attack binding")
    body = {"schema": SCHEMA + ".verification.v1", **result, "attack_suite": {"filename": ATTACK, "file_sha256": hashlib.sha256(raw).hexdigest(), "object_self_sha256": suite["attack_suite_sha256"], "attack_count": 16, "rejected_count": 16, "all_rejected": True}, "formal_credit_marker": ZERO}
    return {**body, "verification_sha256": objsha(body)}


class ManifestBundle:
    def __init__(self) -> None:
        self.dirfd = -1
        self.manifest_fd = -1
        self.manifest_id: tuple[int, ...] = ()
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestBundle":
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        before = os.stat(MANIFEST, dir_fd=self.dirfd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest identity")
        self.manifest_fd = os.open(MANIFEST, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
        opened = os.fstat(self.manifest_fd)
        need(ident(opened) == ident(before), "manifest race")
        self.manifest_id = ident(opened)
        os.lseek(self.manifest_fd, 0, os.SEEK_SET)
        raw = os.read(self.manifest_fd, before.st_size)
        lines = raw.decode("ascii").splitlines()
        need(raw.endswith(b"\n") and len(lines) == len(MANIFEST_MEMBERS), "manifest structure")
        for line, filename in zip(lines, MANIFEST_MEMBERS):
            digest, declared = line.split("  ")
            need(declared == filename and len(digest) == 64, "manifest order:" + filename)
            info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest member identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            member = os.fstat(fd)
            need(ident(member) == ident(info) and hashfd(fd) == hashfd(fd) == digest, "manifest member digest:" + filename)
            self.fds[filename] = fd
            self.ids[filename] = ident(member)
            self.hashes[filename] = digest
        return self

    def read(self, filename: str) -> bytes:
        fd = self.fds[filename]
        os.lseek(fd, 0, os.SEEK_SET)
        return os.read(fd, self.ids[filename][4])

    def final(self) -> None:
        for filename in reversed(MANIFEST_MEMBERS):
            need(ident(os.fstat(self.fds[filename])) == self.ids[filename] and ident(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[filename] and hashfd(self.fds[filename]) == self.hashes[filename], "manifest final:" + filename)
        need(ident(os.fstat(self.manifest_fd)) == self.manifest_id and ident(os.stat(MANIFEST, dir_fd=self.dirfd, follow_symlinks=False)) == self.manifest_id, "manifest final identity")

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.manifest_fd >= 0:
            os.close(self.manifest_fd)
        if self.dirfd >= 0:
            os.close(self.dirfd)


def manifest_first() -> dict[str, Any]:
    with ManifestBundle() as bundle:
        need(bundle.hashes[Path(__file__).name] == self_sha(), "manifest verifier binding")
        raw = bundle.read(OUTPUT)
        value = json.loads(raw)
        need(canonical(value) == raw, "manifest candidate canonical")
        body = dict(value)
        need(body.pop("result_sha256", None) == objsha(body), "manifest candidate closure")
        candidate_preflight(value)
        result = replay(value)
        need(bundle.read(VERIFICATION) == canonical(verification_doc(result)), "manifest verification byte identity")
        bundle.final()
    return {"status": "PASS_MANIFEST_FIRST_HELD_FD_CORRECTED_G2_RELATIONAL_REPLAY__ZERO_WRITES_ZERO_SUPPORT_CREDIT", "manifest_filename": MANIFEST, "manifest_member_count": len(MANIFEST_MEMBERS), "candidate_sha256": result["candidate_sha256"], "result_sha256": result["result_sha256"], "corrected_theorem_obligation_total": 824_832, "deliverables_write_syscalls": 0, "formal_credit": ZERO}


def publish(filename: str, value: dict[str, Any]) -> None:
    path = ROOT / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        os.write(fd, canonical(value))
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    args = parser.parse_args()
    need(sum((args.verify_no_write, args.attack_publish, args.verify_publish, args.manifest_first_no_write)) == 1, "exactly one mode")
    if args.manifest_first_no_write:
        result = manifest_first()
    else:
        need(args.candidate_dir is not None, "candidate required")
        directory = Path(args.candidate_dir)
        if args.attack_publish:
            suite = attack_suite(directory)
            publish(ATTACK, suite)
            result = {"status": suite["status"], "attack_count": 16, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            candidate, _ = read_candidate(directory)
            result = replay(candidate)
            if args.verify_publish:
                publish(VERIFICATION, verification_doc(result))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
