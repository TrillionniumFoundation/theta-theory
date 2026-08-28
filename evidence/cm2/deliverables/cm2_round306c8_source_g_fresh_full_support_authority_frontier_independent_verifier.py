#!/usr/bin/env python3
"""Independently replay the fresh C6/C7 construction authority frontier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Final


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c8_source_g_fresh_full_support_authority_frontier"
OUTPUT: Final = PREFIX + ".json"
PRODUCER: Final = PREFIX + "_producer.py"
ATTACK: Final = PREFIX + "_attack_suite.json"
VERIFICATION: Final = PREFIX + "_verification.json"
REPORT: Final = PREFIX + "_report.md"
COLD: Final = PREFIX + "_cold_replay.md"
MANIFEST: Final = PREFIX + "_manifest.sha256"
SCHEMA: Final = "cm2.round306c8.source-g-fresh-full-support-authority-frontier.v1"
AF3_RESULT: Final = "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json"
C2_MANIFEST: Final = "cm2_round306c2_source_g_corrected_full_support_authority_frontier_manifest.sha256"
C3_MANIFEST: Final = "cm2_round306c3_source_g_corrected_g2_exact_join_filter_manifest.sha256"
C6_MANIFEST: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C6_RESULT: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_result.json"
C7_RESULT: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_result.json"
BOOTSTRAP: Final = {
    AF3_RESULT: (198_283, "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"),
    C2_MANIFEST: (1_026, "b015004605876ff7525f3f2a45375c42225e307ef52745cde9adfbd62bdc346f"),
    C3_MANIFEST: (956, "f05f172ec8fc25564067539091f77f39bc33395dd5e0232f38bde9c587493761"),
    C6_MANIFEST: (2_211, "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"),
    C7_MANIFEST: (2_184, "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"),
    PRODUCER: (19_265, "432b4e847c3d417938c8676d53bbd1b1a6f564d1977bfaab84844dabeb665535"),
}
FAMILY_MEMBERS: Final = {"PRESERVED": 126_468, "NON_GRAPH": 51_172, "R2": 295_336, "R292": 9_404, "G2A": 5_264, "G2B": 10_128}
FAMILY_REPRESENTATIONS: Final = {"PRESERVED": 165_744, "NON_GRAPH": 51_172, "R2": 302_624, "R292": 10_252, "G2A": 5_264, "G2B": 10_128}
ZERO_CREDIT: Final = {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "physical_incidence": 0, "pullback_equivalence": 0, "transition": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0}
MANIFEST_MEMBERS: Final = (PRODUCER, OUTPUT, Path(__file__).name, ATTACK, VERIFICATION, REPORT, COLD)


@dataclass(frozen=True)
class Record:
    filename: str
    size: int
    sha256: str


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(file_descriptor: int) -> str:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        chunk = os.read(file_descriptor, 1_048_576)
        if not chunk:
            return digest.hexdigest()
        digest.update(chunk)


def read_fd(file_descriptor: int) -> bytes:
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(file_descriptor, 1_048_576)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


class Snapshot:
    def __init__(self, records: tuple[Record, ...], directory: Path = ROOT) -> None:
        self.records = records
        self.directory = directory
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not self.directory.is_symlink(), "snapshot directory")
        self.directory_descriptor = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for record in self.records:
            info = os.stat(record.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record.size, "snapshot identity:" + record.filename)
            file_descriptor = os.open(record.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(file_descriptor)
            need(identity(opened) == identity(info), "snapshot race:" + record.filename)
            digest = hash_fd(file_descriptor)
            need(digest == hash_fd(file_descriptor) == record.sha256, "snapshot digest:" + record.filename)
            self.file_descriptors[record.filename] = file_descriptor
            self.identities[record.filename] = identity(opened)
            self.hashes[record.filename] = digest
        return self

    def read(self, filename: str) -> bytes:
        return read_fd(self.file_descriptors[filename])

    def final(self) -> None:
        for record in reversed(self.records):
            need(identity(os.fstat(self.file_descriptors[record.filename])) == self.identities[record.filename], "final fd:" + record.filename)
            need(identity(os.stat(record.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[record.filename], "final path:" + record.filename)
            need(hash_fd(self.file_descriptors[record.filename]) == record.sha256, "final digest:" + record.filename)

    def __exit__(self, *_: Any) -> None:
        for file_descriptor in self.file_descriptors.values():
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def exact_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "canonical document:" + label)
    return value


def parse_manifest(raw: bytes, label: str, expected_count: int) -> tuple[Record, ...]:
    need(raw.endswith(b"\n"), label + " manifest newline")
    records = []
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64 and Path(parts[1]).name == parts[1], label + " manifest line")
        int(parts[0], 16)
        info = os.stat(ROOT / parts[1], follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, label + " member identity")
        records.append(Record(parts[1], info.st_size, parts[0]))
    need(len(records) == expected_count and len({record.filename for record in records}) == expected_count, label + " manifest census")
    return tuple(records)


def legacy_records(af3: dict[str, Any]) -> tuple[Record, ...]:
    merged: dict[str, Record] = {}
    for rows in (af3["closure"]["records"], af3["governance_seals"]["records"], af3["authority_contract"]["authority_files"]):
        for row in rows:
            record = Record(row["filename"], row.get("exact_size", row.get("size")), row["sha256"])
            prior = merged.setdefault(record.filename, record)
            need(prior == record, "legacy record conflict:" + record.filename)
    need(len(af3["closure"]["records"]) == 143 and len(af3["authority_contract"]["authority_files"]) == 45 and len(af3["authority_contract"]["table_authorities"]) == 82, "legacy census")
    return tuple(sorted(merged.values(), key=lambda record: record.filename))


def validate_sources(c6_result: dict[str, Any], c7_result: dict[str, Any]) -> None:
    need(c6_result["fresh_freeze_census"] == {"base_roots": 334_604, "component_member_size_vector_sha256": "b814f69e61d8f9c38db99aa8e138b13f0686b0edbd154bd5c28b4389952d80b0", "components": 61_928, "cross_component_pair_denominator": 123_410_984_634, "members": 497_772, "partition_sha256": "989fa50c0915cbea0c5cf13e20c0c01c858580a47d366ad05f179d7392f75bbb"}, "C6 fresh census")
    need(c6_result["edge_application_census"]["retained_edges"] == 476_118 and c6_result["edge_application_census"]["dropped_edges"] == 2_600, "C6 edge census")
    need(c6_result["member_invalidation_census"]["invalid_distinct_members"] == 66_688, "C6 invalidation census")
    need(c7_result["fresh_base"] == {"member_count": 497_772, "root_count": 334_604, "component_count": 61_928, "cross_component_pair_denominator": 123_410_984_634}, "C7 fresh base")
    fresh_census = c7_result["fresh_census"]
    need(fresh_census["family_member_counts"] == FAMILY_MEMBERS and fresh_census["family_representation_counts"] == FAMILY_REPRESENTATIONS, "C7 family census")
    need((fresh_census["member_count"], fresh_census["representation_count"], fresh_census["physical_incidence_count"], fresh_census["semantic_gap_count"], fresh_census["component_rebind_count"], fresh_census["transition_handle_count"]) == (497_772, 545_184, 15_392, 15_392, 497_772, 497_772), "C7 mechanical census")
    need(c7_result["C5_semantic_effect"]["empty_graph_surviving_side_reclassified_to_NON_GRAPH_count"] == 33_344, "C7 reclassification")
    need(c7_result["legacy_115440_incidence_denominator_reused"] is False and c7_result["legacy_76832_side_member_denominator_reused"] is False and c7_result["formal_credit"] == ZERO_CREDIT, "C7 semantic boundary")


def expected_frontier(af3: dict[str, Any], c6_records: tuple[Record, ...], c7_records: tuple[Record, ...], c6_result: dict[str, Any], c7_result: dict[str, Any]) -> dict[str, Any]:
    validate_sources(c6_result, c7_result)
    legacy = af3["authority_contract"]
    authority_files = legacy["authority_files"]
    table_authorities = legacy["table_authorities"]
    producer_record = Record(PRODUCER, BOOTSTRAP[PRODUCER][0], BOOTSTRAP[PRODUCER][1])
    c2_record = Record(C2_MANIFEST, BOOTSTRAP[C2_MANIFEST][0], BOOTSTRAP[C2_MANIFEST][1])
    c3_record = Record(C3_MANIFEST, BOOTSTRAP[C3_MANIFEST][0], BOOTSTRAP[C3_MANIFEST][1])
    c6_manifest_record = Record(C6_MANIFEST, BOOTSTRAP[C6_MANIFEST][0], BOOTSTRAP[C6_MANIFEST][1])
    c7_manifest_record = Record(C7_MANIFEST, BOOTSTRAP[C7_MANIFEST][0], BOOTSTRAP[C7_MANIFEST][1])
    body = {
        "schema": SCHEMA,
        "status": "PASS_FRESH_C6_C7_CONSTRUCTION_SOURCE_AUTHORITY_FRONTIER__ZERO_SUPPORT_CREDIT",
        "producer_source": producer_record.__dict__,
        "source_snapshot": {
            "legacy_transitive_file_count": 143,
            "legacy_transitive_file_bytes": af3["transitive_file_bytes"],
            "legacy_closure_records_sha256": af3["closure"]["records_sha256"],
            "legacy_closure_edges_sha256": af3["closure"]["edges_sha256"],
            "construction_authority_file_count": len(authority_files),
            "construction_authority_file_catalog_sha256": object_sha(authority_files),
            "table_authority_count": len(table_authorities),
            "table_authority_catalog_sha256": object_sha(table_authorities),
            "C6_manifest": c6_manifest_record.__dict__,
            "C6_manifest_member_count": len(c6_records),
            "C6_manifest_member_catalog_sha256": object_sha([record.__dict__ for record in c6_records]),
            "C7_manifest": c7_manifest_record.__dict__,
            "C7_manifest_member_count": len(c7_records),
            "C7_manifest_member_catalog_sha256": object_sha([record.__dict__ for record in c7_records]),
        },
        "invalidated_component_bound_seals": [
            {**c2_record.__dict__, "authoritative_after_C6": False, "reason": "PRE_C6_COMPONENT_BOUND_FRONTIER"},
            {**c3_record.__dict__, "authoritative_after_C6": False, "reason": "PRE_C5_G2_RELATIONAL_AND_PRE_C6_COMPONENT_BOUND_CENSUS"},
        ],
        "authority_precedence": ["C6_FRESH_MEMBER_COMPONENT_AND_DSU_ROWS", "C7_FRESH_IDENTITY_REPRESENTATION_INCIDENCE_GAP_AND_HANDLE_ROWS", "SURVIVING_MEMBER_FILTER_OVER_LEGACY_SUPPORT_CONSTRUCTION_TABLES", "LEGACY_GEOMETRIC_AND_ANALYTIC_CONSTRUCTION_ROWS", "OUTER_ENVELOPE_AND_DIAGNOSTIC_ROWS_PROVENANCE_ONLY"],
        "fresh_partition": {"exhaustive": True, "mutually_exclusive": True, "member_count": 497_772, "root_count": 334_604, "component_count": 61_928, "cross_component_pair_denominator": 123_410_984_634, "family_member_counts": FAMILY_MEMBERS, "family_representation_counts": FAMILY_REPRESENTATIONS, "representation_count": 545_184, "physical_incidence_relation_count": 15_392, "open_physical_semantic_gap_count": 15_392, "invalidated_member_count": 66_688, "empty_graph_surviving_side_reclassified_to_NON_GRAPH_count": 33_344},
        "current_theorem_obligation_census": {"known_exact_count": None, "must_be_rebuilt_from_fresh_six_family_support": True, "historical_counts_are_not_authoritative": [{"count": 824_864, "scope": "legacy_AF3"}, {"count": 824_800, "scope": "pre_C5_C2"}, {"count": 824_832, "scope": "pre_C5_C3_relational"}], "is_final_feature_ledger_row_count": False},
        "construction_authority_files": authority_files,
        "table_authorities": table_authorities,
        "field_scoped_precedence": legacy["field_scoped_precedence"],
        "authority_role_policies": legacy["authority_role_policies"],
        "migration_rules": {"C6_fresh_member_component_rows_are_authoritative": True, "C7_fresh_mechanical_rows_are_authoritative_for_identity_and_routing_only": True, "C2_component_bound_frontier_is_authoritative": False, "C3_component_bound_relational_census_is_authoritative": False, "legacy_identity_binding_rows_are_authoritative": False, "legacy_component_ids_are_authoritative": False, "surviving_legacy_geometry_may_be_used_as_construction_input": True, "outer_envelope_or_inner_witness_may_equal_full_support": False, "physical_incidence_pullback_and_one_sided_trace_must_be_rebuilt_for_15_392_relations": True, "typed_AST_certificate_and_representation_pullback_required": True, "new_legal_cross_component_edge_requires_full_reclosure": True},
        "formal_credit": ZERO_CREDIT,
        "normalized_support_sealed": False,
        "B1A_permitted": False,
        "B2_permitted": False,
        "CM2": "NO-GO_FOR_CLAIM",
        "seed_serialized_or_semantically_used": False,
    }
    return {**body, "authority_frontier_sha256": object_sha(body)}


def reconstruct() -> dict[str, Any]:
    bootstrap_records = tuple(Record(filename, size, digest) for filename, (size, digest) in BOOTSTRAP.items())
    with Snapshot(bootstrap_records) as bootstrap:
        af3 = exact_document(bootstrap.read(AF3_RESULT), "AF3 result")
        parse_manifest(bootstrap.read(C2_MANIFEST), "C2", 7)
        parse_manifest(bootstrap.read(C3_MANIFEST), "C3", 7)
        c6_records = parse_manifest(bootstrap.read(C6_MANIFEST), "C6", 14)
        c7_records = parse_manifest(bootstrap.read(C7_MANIFEST), "C7", 14)
        all_records = legacy_records(af3) + c6_records + c7_records
        merged = {record.filename: record for record in all_records}
        need(len(merged) == len(all_records), "frontier filename collision")
        with Snapshot(tuple(sorted(merged.values(), key=lambda record: record.filename))) as sources:
            c6_result = exact_document(sources.read(C6_RESULT), "C6 result")
            c7_result = exact_document(sources.read(C7_RESULT), "C7 result")
            expected = expected_frontier(af3, c6_records, c7_records, c6_result, c7_result)
            sources.final()
        bootstrap.final()
    return expected


def closed_frontier(raw: bytes) -> dict[str, Any]:
    value = exact_document(raw, "candidate")
    body = dict(value)
    claimed = body.pop("authority_frontier_sha256", None)
    need(type(claimed) is str and claimed == object_sha(body), "candidate closure")
    need(value["schema"] == SCHEMA and value["status"] == "PASS_FRESH_C6_C7_CONSTRUCTION_SOURCE_AUTHORITY_FRONTIER__ZERO_SUPPORT_CREDIT", "candidate contract")
    need(value["fresh_partition"]["member_count"] == 497_772 and value["fresh_partition"]["component_count"] == 61_928, "candidate fresh census")
    need(value["fresh_partition"]["family_member_counts"] == FAMILY_MEMBERS and value["fresh_partition"]["physical_incidence_relation_count"] == 15_392, "candidate family census")
    need(value["current_theorem_obligation_census"]["known_exact_count"] is None and value["current_theorem_obligation_census"]["must_be_rebuilt_from_fresh_six_family_support"] is True, "candidate obligation boundary")
    need(value["migration_rules"]["C2_component_bound_frontier_is_authoritative"] is False and value["migration_rules"]["C3_component_bound_relational_census_is_authoritative"] is False, "candidate invalidation boundary")
    need(value["formal_credit"] == ZERO_CREDIT and value["normalized_support_sealed"] is False and value["B1A_permitted"] is False and value["B2_permitted"] is False, "candidate zero credit")
    return value


def candidate_raw(candidate_dir: Path) -> tuple[bytes, Record]:
    resolved = candidate_dir.resolve()
    need(os.path.commonpath((str(resolved), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
    before = os.stat(candidate_dir, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode) and set(os.listdir(candidate_dir)) == {OUTPUT}, "candidate exact directory")
    info = os.stat(candidate_dir / OUTPUT, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "candidate identity")
    file_descriptor = os.open(candidate_dir / OUTPUT, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(file_descriptor)
        need(identity(opened) == identity(info), "candidate race")
        digest = hash_fd(file_descriptor)
        need(digest == hash_fd(file_descriptor), "candidate digest")
        raw = read_fd(file_descriptor)
        need(identity(os.fstat(file_descriptor)) == identity(opened), "candidate final fd")
    finally:
        os.close(file_descriptor)
    need(identity(os.stat(candidate_dir / OUTPUT, follow_symlinks=False)) == identity(info), "candidate final path")
    closed_frontier(raw)
    return raw, Record(OUTPUT, info.st_size, digest)


def receipt(candidate_record: Record, expected: dict[str, Any]) -> dict[str, Any]:
    return {"status": "PASS_INDEPENDENT_FRESH_C6_C7_AUTHORITY_FRONTIER_REPLAY__ZERO_SUPPORT_CREDIT", "candidate_filename": OUTPUT, "candidate_size": candidate_record.size, "candidate_sha256": candidate_record.sha256, "authority_frontier_sha256": expected["authority_frontier_sha256"], "legacy_source_file_count": 143, "construction_authority_file_count": 45, "table_authority_count": 82, "fresh_member_count": 497_772, "fresh_component_count": 61_928, "fresh_representation_count": 545_184, "physical_incidence_relation_count": 15_392, "producer_imported_or_executed": False, "formal_credit": ZERO_CREDIT}


def verify(candidate_dir: Path) -> dict[str, Any]:
    raw, candidate_record = candidate_raw(candidate_dir)
    expected = reconstruct()
    need(raw == canonical(expected), "candidate byte identity")
    return receipt(candidate_record, expected)


def self_sha() -> str:
    path = Path(__file__)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "verifier identity")
    file_descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(identity(os.fstat(file_descriptor)) == identity(info), "verifier race")
        digest = hash_fd(file_descriptor)
        need(digest == hash_fd(file_descriptor), "verifier digest")
        return digest
    finally:
        os.close(file_descriptor)


def rewrite_closed(path: Path, mutator: Any) -> None:
    value = json.loads(path.read_bytes())
    mutator(value)
    body = dict(value)
    body.pop("authority_frontier_sha256", None)
    value = {**body, "authority_frontier_sha256": object_sha(body)}
    path.write_bytes(canonical(value))


def attack_suite(candidate_dir: Path) -> dict[str, Any]:
    baseline = verify(candidate_dir)
    expected = reconstruct()
    work = Path(tempfile.mkdtemp(prefix="cm2-c8-fresh-authority-attacks-"))
    original = candidate_dir / OUTPUT
    attacks = []

    def restore() -> None:
        path = work / OUTPUT
        if path.exists() or path.is_symlink():
            path.unlink()
        shutil.copyfile(original, path)

    def attack_verify() -> None:
        raw, _ = candidate_raw(work)
        need(raw == canonical(expected), "candidate byte identity")

    def execute(attack_id: str, mutation: Any, cleanup: Any | None = None) -> None:
        restore()
        try:
            mutation()
            rejection = None
            try:
                attack_verify()
            except (Rejected, OSError, json.JSONDecodeError) as error:
                rejection = type(error).__name__ + ":" + str(error)
            need(rejection is not None, "attack accepted:" + attack_id)
            body = {"attack_id": attack_id, "rejected": True, "rejection_boundary": rejection}
            attacks.append({**body, "row_sha256": object_sha(body)})
        finally:
            if cleanup is not None:
                cleanup()

    try:
        execute("A01_EXTRA_FILE", lambda: (work / "foreign").write_bytes(b"x"), lambda: (work / "foreign").unlink())
        execute("A02_MISSING_OUTPUT", lambda: (work / OUTPUT).unlink())
        execute("A03_OUTPUT_SYMLINK", lambda: ((work / OUTPUT).unlink(), (work / OUTPUT).symlink_to(original)))
        def hardlink() -> None:
            (work / OUTPUT).unlink()
            target = work.parent / (work.name + "-target")
            shutil.copyfile(original, target)
            os.link(target, work / OUTPUT)
        execute("A04_OUTPUT_HARDLINK", hardlink, lambda: (work.parent / (work.name + "-target")).unlink())
        execute("A05_SCHEMA", lambda: rewrite_closed(work / OUTPUT, lambda value: value.__setitem__("schema", "foreign")))
        execute("A06_PRODUCER_PIN", lambda: rewrite_closed(work / OUTPUT, lambda value: value["producer_source"].__setitem__("sha256", "0" * 64)))
        execute("A07_MEMBER_COUNT", lambda: rewrite_closed(work / OUTPUT, lambda value: value["fresh_partition"].__setitem__("member_count", 497_773)))
        execute("A08_COMPONENT_COUNT", lambda: rewrite_closed(work / OUTPUT, lambda value: value["fresh_partition"].__setitem__("component_count", 61_929)))
        execute("A09_NON_GRAPH_COUNT", lambda: rewrite_closed(work / OUTPUT, lambda value: value["fresh_partition"]["family_member_counts"].__setitem__("NON_GRAPH", 17_828)))
        execute("A10_PHYSICAL_DENOMINATOR", lambda: rewrite_closed(work / OUTPUT, lambda value: value["fresh_partition"].__setitem__("physical_incidence_relation_count", 115_440)))
        execute("A11_FABRICATED_OBLIGATION", lambda: rewrite_closed(work / OUTPUT, lambda value: value["current_theorem_obligation_census"].__setitem__("known_exact_count", 824_832)))
        execute("A12_REENABLE_C2", lambda: rewrite_closed(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("C2_component_bound_frontier_is_authoritative", True)))
        execute("A13_REENABLE_C3", lambda: rewrite_closed(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("C3_component_bound_relational_census_is_authoritative", True)))
        execute("A14_PRECEDENCE_SWAP", lambda: rewrite_closed(work / OUTPUT, lambda value: value["authority_precedence"].__setitem__(slice(0, 2), reversed(value["authority_precedence"][:2]))))
        execute("A15_AUTHORITY_FILE_DROP", lambda: rewrite_closed(work / OUTPUT, lambda value: value["construction_authority_files"].pop()))
        execute("A16_TABLE_DROP", lambda: rewrite_closed(work / OUTPUT, lambda value: value["table_authorities"].pop()))
        execute("A17_CREDIT_INJECTION", lambda: rewrite_closed(work / OUTPUT, lambda value: value["formal_credit"].__setitem__("normalized_support", 1)))
        execute("A18_OUTER_WITNESS_PROMOTION", lambda: rewrite_closed(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("outer_envelope_or_inner_witness_may_equal_full_support", True)))
        execute("A19_DISABLE_INCIDENCE_REBUILD", lambda: rewrite_closed(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("physical_incidence_pullback_and_one_sided_trace_must_be_rebuilt_for_15_392_relations", False)))
        execute("A20_DISABLE_RECLOSURE", lambda: rewrite_closed(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("new_legal_cross_component_edge_requires_full_reclosure", False)))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 20, "attack count")
    body = {"schema": SCHEMA + ".coherent-attack-suite.v1", "status": "PASS_20_OF_20_COHERENT_ATTACKS_REJECTED", "verifier_filename": Path(__file__).name, "verifier_file_sha256": self_sha(), "attack_count": 20, "rejected_count": 20, "all_rejected": True, "baseline_candidate_sha256": baseline["candidate_sha256"], "attacks": attacks}
    return {**body, "attack_suite_sha256": object_sha(body)}


def read_closed(path: Path, closure: str) -> tuple[dict[str, Any], bytes]:
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "closed document identity:" + path.name)
    raw = path.read_bytes()
    value = exact_document(raw, path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(type(claimed) is str and claimed == object_sha(body), "closed document digest:" + path.name)
    return value, raw


def verification_doc(result: dict[str, Any]) -> dict[str, Any]:
    suite, raw = read_closed(ROOT / ATTACK, "attack_suite_sha256")
    need(suite["verifier_file_sha256"] == self_sha() and (suite["attack_count"], suite["rejected_count"], suite["all_rejected"]) == (20, 20, True), "attack binding")
    body = {"schema": SCHEMA + ".verification.v1", **result, "attack_suite": {"filename": ATTACK, "file_sha256": hashlib.sha256(raw).hexdigest(), "object_self_sha256": suite["attack_suite_sha256"], "attack_count": 20, "rejected_count": 20, "all_rejected": True}, "formal_credit_marker": ZERO_CREDIT}
    return {**body, "verification_sha256": object_sha(body)}


class ManifestBundle:
    def __init__(self) -> None:
        self.directory_descriptor = -1
        self.manifest_descriptor = -1
        self.manifest_identity: tuple[int, ...] = ()
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}
        self.hashes: dict[str, str] = {}

    def __enter__(self) -> "ManifestBundle":
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        info = os.stat(MANIFEST, dir_fd=self.directory_descriptor, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest identity")
        self.manifest_descriptor = os.open(MANIFEST, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
        opened = os.fstat(self.manifest_descriptor)
        need(identity(opened) == identity(info), "manifest race")
        self.manifest_identity = identity(opened)
        raw = read_fd(self.manifest_descriptor)
        need(raw.endswith(b"\n"), "manifest newline")
        lines = raw.decode("ascii").splitlines()
        need(len(lines) == len(MANIFEST_MEMBERS), "manifest count")
        for line, filename in zip(lines, MANIFEST_MEMBERS):
            parts = line.split("  ")
            need(len(parts) == 2 and parts[1] == filename and len(parts[0]) == 64, "manifest ordered member:" + filename)
            member_info = os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            need(stat.S_ISREG(member_info.st_mode) and member_info.st_nlink == 1, "manifest member identity:" + filename)
            file_descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            member_opened = os.fstat(file_descriptor)
            need(identity(member_opened) == identity(member_info), "manifest member race:" + filename)
            digest = hash_fd(file_descriptor)
            need(digest == hash_fd(file_descriptor) == parts[0], "manifest member digest:" + filename)
            self.file_descriptors[filename] = file_descriptor
            self.identities[filename] = identity(member_opened)
            self.hashes[filename] = digest
        return self

    def read(self, filename: str) -> bytes:
        return read_fd(self.file_descriptors[filename])

    def final(self) -> None:
        for filename in reversed(MANIFEST_MEMBERS):
            need(identity(os.fstat(self.file_descriptors[filename])) == self.identities[filename], "manifest final fd:" + filename)
            need(identity(os.stat(filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[filename], "manifest final path:" + filename)
            need(hash_fd(self.file_descriptors[filename]) == self.hashes[filename], "manifest final digest:" + filename)
        need(identity(os.fstat(self.manifest_descriptor)) == self.manifest_identity and identity(os.stat(MANIFEST, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.manifest_identity, "manifest final identity")

    def __exit__(self, *_: Any) -> None:
        for file_descriptor in self.file_descriptors.values():
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        if self.manifest_descriptor >= 0:
            os.close(self.manifest_descriptor)
        if self.directory_descriptor >= 0:
            os.close(self.directory_descriptor)


def manifest_first() -> dict[str, Any]:
    with ManifestBundle() as bundle:
        need(bundle.hashes[Path(__file__).name] == self_sha(), "manifest verifier binding")
        raw = bundle.read(OUTPUT)
        closed_frontier(raw)
        expected = reconstruct()
        need(raw == canonical(expected), "manifest candidate byte identity")
        candidate_record = Record(OUTPUT, bundle.identities[OUTPUT][4], bundle.hashes[OUTPUT])
        result = receipt(candidate_record, expected)
        need(bundle.read(VERIFICATION) == canonical(verification_doc(result)), "manifest verification byte identity")
        bundle.final()
    return {"status": "PASS_MANIFEST_FIRST_HELD_FD_FRESH_C6_C7_AUTHORITY_FRONTIER__ZERO_WRITES_ZERO_SUPPORT_CREDIT", "manifest_filename": MANIFEST, "manifest_member_count": len(MANIFEST_MEMBERS), "candidate_sha256": candidate_record.sha256, "authority_frontier_sha256": expected["authority_frontier_sha256"], "legacy_source_file_count": 143, "construction_authority_file_count": 45, "table_authority_count": 82, "deliverables_write_syscalls": 0, "formal_credit": ZERO_CREDIT}


def publish_document(filename: str, value: dict[str, Any]) -> None:
    path = ROOT / filename
    need(not path.exists(), "publish no-clobber:" + filename)
    file_descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        os.write(file_descriptor, canonical(value))
        os.fsync(file_descriptor)
    finally:
        os.close(file_descriptor)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-dir")
    parser.add_argument("--verify-no-write", action="store_true")
    parser.add_argument("--attack-publish", action="store_true")
    parser.add_argument("--verify-publish", action="store_true")
    parser.add_argument("--manifest-first-no-write", action="store_true")
    arguments = parser.parse_args()
    need(sum((arguments.verify_no_write, arguments.attack_publish, arguments.verify_publish, arguments.manifest_first_no_write)) == 1, "exactly one mode")
    if arguments.manifest_first_no_write:
        result = manifest_first()
    else:
        need(arguments.candidate_dir is not None, "candidate required")
        candidate_dir = Path(arguments.candidate_dir)
        if arguments.attack_publish:
            suite = attack_suite(candidate_dir)
            publish_document(ATTACK, suite)
            result = {"status": suite["status"], "attack_count": 20, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            result = verify(candidate_dir)
            if arguments.verify_publish:
                publish_document(VERIFICATION, verification_doc(result))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
