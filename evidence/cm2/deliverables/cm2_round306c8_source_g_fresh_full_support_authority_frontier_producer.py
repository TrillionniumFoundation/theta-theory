#!/usr/bin/env python3
"""Freeze the fresh C6/C7 full-support construction authority frontier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final


class Rejected(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c8_source_g_fresh_full_support_authority_frontier"
OUTPUT: Final = PREFIX + ".json"
SCHEMA: Final = "cm2.round306c8.source-g-fresh-full-support-authority-frontier.v1"
AF3_RESULT: Final = "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json"
AF3_RESULT_SIZE: Final = 198_283
AF3_RESULT_SHA256: Final = "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"
C2_MANIFEST: Final = "cm2_round306c2_source_g_corrected_full_support_authority_frontier_manifest.sha256"
C2_MANIFEST_SIZE: Final = 1_026
C2_MANIFEST_SHA256: Final = "b015004605876ff7525f3f2a45375c42225e307ef52745cde9adfbd62bdc346f"
C3_MANIFEST: Final = "cm2_round306c3_source_g_corrected_g2_exact_join_filter_manifest.sha256"
C3_MANIFEST_SIZE: Final = 956
C3_MANIFEST_SHA256: Final = "f05f172ec8fc25564067539091f77f39bc33395dd5e0232f38bde9c587493761"
C6_MANIFEST: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_manifest.sha256"
C6_MANIFEST_SIZE: Final = 2_211
C6_MANIFEST_SHA256: Final = "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2"
C7_MANIFEST: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_manifest.sha256"
C7_MANIFEST_SIZE: Final = 2_184
C7_MANIFEST_SHA256: Final = "4e534e412a760d13fe7eb278ca063e86ac2a7164bbfdb3b14a3142219267c0c6"
C6_RESULT: Final = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_result.json"
C7_RESULT: Final = "cm2_round306c7_source_g_fresh_identity_support_mechanical_replay_result.json"
FAMILY_MEMBERS: Final = {
    "PRESERVED": 126_468,
    "NON_GRAPH": 51_172,
    "R2": 295_336,
    "R292": 9_404,
    "G2A": 5_264,
    "G2B": 10_128,
}
FAMILY_REPRESENTATIONS: Final = {
    "PRESERVED": 165_744,
    "NON_GRAPH": 51_172,
    "R2": 302_624,
    "R292": 10_252,
    "G2A": 5_264,
    "G2B": 10_128,
}
ZERO_CREDIT: Final = {
    "normalized_support": 0,
    "representation_cover": 0,
    "A1_A2": 0,
    "physical_incidence": 0,
    "pullback_equivalence": 0,
    "transition": 0,
    "B1A": 0,
    "B2": 0,
    "maximality": 0,
    "fibre": 0,
    "global_disposition": 0,
    "CM2": 0,
}


@dataclass(frozen=True)
class FileRecord:
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
    def __init__(self, records: tuple[FileRecord, ...]) -> None:
        self.records = records
        self.directory_descriptor = -1
        self.file_descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(ROOT, follow_symlinks=False)
        require(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.directory_descriptor = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for record in self.records:
            info = os.stat(record.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record.size, "file identity:" + record.filename)
            file_descriptor = os.open(record.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.directory_descriptor)
            opened = os.fstat(file_descriptor)
            require(identity(opened) == identity(info), "open race:" + record.filename)
            require(hash_fd(file_descriptor) == hash_fd(file_descriptor) == record.sha256, "two-pass sha:" + record.filename)
            self.file_descriptors[record.filename] = file_descriptor
            self.identities[record.filename] = identity(opened)
        return self

    def read(self, filename: str) -> bytes:
        return read_fd(self.file_descriptors[filename])

    def final(self) -> None:
        for record in reversed(self.records):
            require(identity(os.fstat(self.file_descriptors[record.filename])) == self.identities[record.filename], "final fd:" + record.filename)
            require(identity(os.stat(record.filename, dir_fd=self.directory_descriptor, follow_symlinks=False)) == self.identities[record.filename], "final path:" + record.filename)
            require(hash_fd(self.file_descriptors[record.filename]) == record.sha256, "final sha:" + record.filename)

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
    require(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "canonical document:" + label)
    return value


def parse_manifest(raw: bytes, label: str, expected_count: int) -> tuple[FileRecord, ...]:
    require(raw.endswith(b"\n"), label + " manifest newline")
    records = []
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        require(len(parts) == 2 and len(parts[0]) == 64 and Path(parts[1]).name == parts[1], label + " manifest line")
        int(parts[0], 16)
        records.append(FileRecord(parts[1], -1, parts[0]))
    require(len(records) == expected_count and len({record.filename for record in records}) == expected_count, label + " manifest census")
    return tuple(records)


def sized_records(records: tuple[FileRecord, ...]) -> tuple[FileRecord, ...]:
    output = []
    for record in records:
        info = os.stat(ROOT / record.filename, follow_symlinks=False)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest member identity:" + record.filename)
        output.append(FileRecord(record.filename, info.st_size, record.sha256))
    return tuple(output)


def legacy_records(af3: dict[str, Any]) -> tuple[FileRecord, ...]:
    merged: dict[str, FileRecord] = {}
    domains = (af3["closure"]["records"], af3["governance_seals"]["records"], af3["authority_contract"]["authority_files"])
    for domain in domains:
        for row in domain:
            record = FileRecord(row["filename"], row.get("exact_size", row.get("size")), row["sha256"])
            prior = merged.setdefault(record.filename, record)
            require(prior == record, "legacy record conflict:" + record.filename)
    require(len(af3["closure"]["records"]) == 143, "legacy closure count")
    require(len(af3["authority_contract"]["authority_files"]) == 45, "legacy authority count")
    require(len(af3["authority_contract"]["table_authorities"]) == 82, "legacy table count")
    return tuple(sorted(merged.values(), key=lambda record: record.filename))


def producer_source_record() -> FileRecord:
    filename = Path(__file__).name
    info = os.stat(__file__, follow_symlinks=False)
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "producer identity")
    file_descriptor = os.open(__file__, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(file_descriptor)
        require(identity(opened) == identity(info), "producer race")
        digest = hash_fd(file_descriptor)
        require(digest == hash_fd(file_descriptor), "producer digest")
        return FileRecord(filename, info.st_size, digest)
    finally:
        os.close(file_descriptor)


def validate_sources(c6_result: dict[str, Any], c7_result: dict[str, Any]) -> None:
    require(c6_result["fresh_freeze_census"] == {
        "base_roots": 334_604,
        "component_member_size_vector_sha256": "b814f69e61d8f9c38db99aa8e138b13f0686b0edbd154bd5c28b4389952d80b0",
        "components": 61_928,
        "cross_component_pair_denominator": 123_410_984_634,
        "members": 497_772,
        "partition_sha256": "989fa50c0915cbea0c5cf13e20c0c01c858580a47d366ad05f179d7392f75bbb",
    }, "C6 fresh census")
    require(c6_result["edge_application_census"]["retained_edges"] == 476_118 and c6_result["edge_application_census"]["dropped_edges"] == 2_600, "C6 edge census")
    require(c6_result["member_invalidation_census"]["invalid_distinct_members"] == 66_688, "C6 invalidation census")
    require(c7_result["fresh_base"] == {"member_count": 497_772, "root_count": 334_604, "component_count": 61_928, "cross_component_pair_denominator": 123_410_984_634}, "C7 fresh base")
    fresh_census = c7_result["fresh_census"]
    require(fresh_census["family_member_counts"] == FAMILY_MEMBERS and fresh_census["family_representation_counts"] == FAMILY_REPRESENTATIONS, "C7 family census")
    require((fresh_census["member_count"], fresh_census["representation_count"], fresh_census["physical_incidence_count"], fresh_census["semantic_gap_count"], fresh_census["component_rebind_count"], fresh_census["transition_handle_count"]) == (497_772, 545_184, 15_392, 15_392, 497_772, 497_772), "C7 mechanical census")
    require(c7_result["C5_semantic_effect"]["empty_graph_surviving_side_reclassified_to_NON_GRAPH_count"] == 33_344, "C7 reclassification")
    require(c7_result["legacy_115440_incidence_denominator_reused"] is False and c7_result["legacy_76832_side_member_denominator_reused"] is False, "C7 denominator boundary")
    require(c7_result["formal_credit"] == ZERO_CREDIT, "C7 zero credit")


def construct() -> dict[str, Any]:
    bootstrap_records = (
        FileRecord(AF3_RESULT, AF3_RESULT_SIZE, AF3_RESULT_SHA256),
        FileRecord(C2_MANIFEST, C2_MANIFEST_SIZE, C2_MANIFEST_SHA256),
        FileRecord(C3_MANIFEST, C3_MANIFEST_SIZE, C3_MANIFEST_SHA256),
        FileRecord(C6_MANIFEST, C6_MANIFEST_SIZE, C6_MANIFEST_SHA256),
        FileRecord(C7_MANIFEST, C7_MANIFEST_SIZE, C7_MANIFEST_SHA256),
    )
    producer_record = producer_source_record()
    with Snapshot(bootstrap_records) as bootstrap:
        af3 = exact_document(bootstrap.read(AF3_RESULT), "AF3 result")
        parse_manifest(bootstrap.read(C2_MANIFEST), "C2", 7)
        parse_manifest(bootstrap.read(C3_MANIFEST), "C3", 7)
        c6_manifest_records = parse_manifest(bootstrap.read(C6_MANIFEST), "C6", 14)
        c7_manifest_records = parse_manifest(bootstrap.read(C7_MANIFEST), "C7", 14)
        c6_records = sized_records(c6_manifest_records)
        c7_records = sized_records(c7_manifest_records)
        source_records = legacy_records(af3) + c6_records + c7_records
        merged = {record.filename: record for record in source_records}
        require(len(merged) == len(source_records), "frontier filename collision")
        with Snapshot(tuple(sorted(merged.values(), key=lambda record: record.filename))) as sources:
            c6_result = exact_document(sources.read(C6_RESULT), "C6 result")
            c7_result = exact_document(sources.read(C7_RESULT), "C7 result")
            validate_sources(c6_result, c7_result)
            legacy = af3["authority_contract"]
            authority_files = legacy["authority_files"]
            table_authorities = legacy["table_authorities"]
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
                    "C6_manifest": bootstrap_records[3].__dict__,
                    "C6_manifest_member_count": len(c6_records),
                    "C6_manifest_member_catalog_sha256": object_sha([record.__dict__ for record in c6_records]),
                    "C7_manifest": bootstrap_records[4].__dict__,
                    "C7_manifest_member_count": len(c7_records),
                    "C7_manifest_member_catalog_sha256": object_sha([record.__dict__ for record in c7_records]),
                },
                "invalidated_component_bound_seals": [
                    {**bootstrap_records[1].__dict__, "authoritative_after_C6": False, "reason": "PRE_C6_COMPONENT_BOUND_FRONTIER"},
                    {**bootstrap_records[2].__dict__, "authoritative_after_C6": False, "reason": "PRE_C5_G2_RELATIONAL_AND_PRE_C6_COMPONENT_BOUND_CENSUS"},
                ],
                "authority_precedence": [
                    "C6_FRESH_MEMBER_COMPONENT_AND_DSU_ROWS",
                    "C7_FRESH_IDENTITY_REPRESENTATION_INCIDENCE_GAP_AND_HANDLE_ROWS",
                    "SURVIVING_MEMBER_FILTER_OVER_LEGACY_SUPPORT_CONSTRUCTION_TABLES",
                    "LEGACY_GEOMETRIC_AND_ANALYTIC_CONSTRUCTION_ROWS",
                    "OUTER_ENVELOPE_AND_DIAGNOSTIC_ROWS_PROVENANCE_ONLY",
                ],
                "fresh_partition": {
                    "exhaustive": True,
                    "mutually_exclusive": True,
                    "member_count": 497_772,
                    "root_count": 334_604,
                    "component_count": 61_928,
                    "cross_component_pair_denominator": 123_410_984_634,
                    "family_member_counts": FAMILY_MEMBERS,
                    "family_representation_counts": FAMILY_REPRESENTATIONS,
                    "representation_count": 545_184,
                    "physical_incidence_relation_count": 15_392,
                    "open_physical_semantic_gap_count": 15_392,
                    "invalidated_member_count": 66_688,
                    "empty_graph_surviving_side_reclassified_to_NON_GRAPH_count": 33_344,
                },
                "current_theorem_obligation_census": {
                    "known_exact_count": None,
                    "must_be_rebuilt_from_fresh_six_family_support": True,
                    "historical_counts_are_not_authoritative": [
                        {"count": 824_864, "scope": "legacy_AF3"},
                        {"count": 824_800, "scope": "pre_C5_C2"},
                        {"count": 824_832, "scope": "pre_C5_C3_relational"},
                    ],
                    "is_final_feature_ledger_row_count": False,
                },
                "construction_authority_files": authority_files,
                "table_authorities": table_authorities,
                "field_scoped_precedence": legacy["field_scoped_precedence"],
                "authority_role_policies": legacy["authority_role_policies"],
                "migration_rules": {
                    "C6_fresh_member_component_rows_are_authoritative": True,
                    "C7_fresh_mechanical_rows_are_authoritative_for_identity_and_routing_only": True,
                    "C2_component_bound_frontier_is_authoritative": False,
                    "C3_component_bound_relational_census_is_authoritative": False,
                    "legacy_identity_binding_rows_are_authoritative": False,
                    "legacy_component_ids_are_authoritative": False,
                    "surviving_legacy_geometry_may_be_used_as_construction_input": True,
                    "outer_envelope_or_inner_witness_may_equal_full_support": False,
                    "physical_incidence_pullback_and_one_sided_trace_must_be_rebuilt_for_15_392_relations": True,
                    "typed_AST_certificate_and_representation_pullback_required": True,
                    "new_legal_cross_component_edge_requires_full_reclosure": True,
                },
                "formal_credit": ZERO_CREDIT,
                "normalized_support_sealed": False,
                "B1A_permitted": False,
                "B2_permitted": False,
                "CM2": "NO-GO_FOR_CLAIM",
                "seed_serialized_or_semantically_used": False,
            }
            result = {**body, "authority_frontier_sha256": object_sha(body)}
            sources.final()
        bootstrap.final()
    return result


def publish(path: Path, payload: bytes) -> None:
    require(not path.exists(), "output no-clobber")
    file_descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        os.write(file_descriptor, payload)
        os.fsync(file_descriptor)
    finally:
        os.close(file_descriptor)


def main() -> int:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    arguments = parser.parse_args()
    require(arguments.print_result != (arguments.candidate_dir is not None), "exactly one mode")
    result = construct()
    payload = canonical(result)
    if arguments.print_result:
        sys.stdout.buffer.write(payload + b"\n")
    else:
        candidate = Path(arguments.candidate_dir).resolve()
        require(os.path.commonpath((str(candidate), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        candidate.mkdir(mode=0o700, parents=False, exist_ok=False)
        publish(candidate / OUTPUT, payload)
        print(json.dumps({"status": result["status"], "output": OUTPUT, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "authority_frontier_sha256": result["authority_frontier_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
