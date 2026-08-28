#!/usr/bin/env python3
"""Freeze the corrected full-support construction-source authority frontier."""

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
PREFIX: Final = "cm2_round306c2_source_g_corrected_full_support_authority_frontier"
OUTPUT: Final = PREFIX + ".json"
SCHEMA: Final = "cm2.round306c2.source-g-corrected-full-support-authority-frontier.v1"
AF3_RESULT: Final = "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json"
AF3_RESULT_SIZE: Final = 198_283
AF3_RESULT_SHA256: Final = "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"
C1_MANIFEST: Final = "cm2_round306c1_source_g_corrected_identity_support_replay_manifest.sha256"
C1_MANIFEST_SIZE: Final = 2_398
C1_MANIFEST_SHA256: Final = "9adfc1499f2c376085b1e7166cce43e41374ac81f4f10ad87409b0d9b14e4b7c"
C1_PREFIX: Final = "cm2_round306c1_source_g_corrected_identity_support_replay"
C1_RESULT: Final = C1_PREFIX + "_result.json"
C1_FAMILY: Final = C1_PREFIX + "_family_census.jsonl.gz"
C1_OBLIGATION: Final = C1_PREFIX + "_theorem_obligation_census.json"
EXPECTED_FAMILIES: Final = {
    "PRESERVED": 126_468,
    "NON_GRAPH": 17_828,
    "R2": 295_336,
    "R292": 9_404,
    "G2A": 38_608,
    "G2B": 76_816,
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


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return digest.hexdigest()
        digest.update(chunk)


def read_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


class HeldFiles:
    def __init__(self, records: tuple[FileRecord, ...]) -> None:
        self.records = records
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.identities: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "HeldFiles":
        before = os.stat(ROOT, follow_symlinks=False)
        require(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for record in self.records:
            info = os.stat(record.filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record.size, "file identity:" + record.filename)
            fd = os.open(record.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            require(identity(opened) == identity(info), "open race:" + record.filename)
            require(hash_fd(fd) == hash_fd(fd) == record.sha256, "two-pass sha:" + record.filename)
            self.fds[record.filename] = fd
            self.identities[record.filename] = identity(opened)
        return self

    def read(self, filename: str) -> bytes:
        return read_fd(self.fds[filename])

    def final(self) -> None:
        for record in reversed(self.records):
            require(identity(os.fstat(self.fds[record.filename])) == self.identities[record.filename], "final fd:" + record.filename)
            require(identity(os.stat(record.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.identities[record.filename], "final path:" + record.filename)
            require(hash_fd(self.fds[record.filename]) == record.sha256, "final sha:" + record.filename)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def exact_document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    require(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "canonical document:" + label)
    return value


def parse_manifest(raw: bytes) -> tuple[FileRecord, ...]:
    require(raw.endswith(b"\n"), "C1 manifest newline")
    records = []
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ")
        require(len(parts) == 2 and len(parts[0]) == 64, "C1 manifest line")
        int(parts[0], 16)
        records.append(FileRecord(parts[1], -1, parts[0]))
    require(len(records) == 16 and len({record.filename for record in records}) == 16, "C1 manifest census")
    return tuple(records)


def legacy_records(af3: dict[str, Any]) -> tuple[FileRecord, ...]:
    merged: dict[str, FileRecord] = {}
    domains = (
        af3["closure"]["records"],
        af3["governance_seals"]["records"],
        af3["authority_contract"]["authority_files"],
    )
    for domain in domains:
        for row in domain:
            record = FileRecord(row["filename"], row.get("exact_size", row.get("size")), row["sha256"])
            prior = merged.setdefault(record.filename, record)
            require(prior == record, "legacy record conflict:" + record.filename)
    require(len(af3["closure"]["records"]) == 143, "legacy closure count")
    require(len(af3["authority_contract"]["authority_files"]) == 45, "legacy authority file count")
    require(len(af3["authority_contract"]["table_authorities"]) == 82, "legacy table count")
    return tuple(sorted(merged.values(), key=lambda record: record.filename))


def construct() -> dict[str, Any]:
    bootstrap = (
        FileRecord(AF3_RESULT, AF3_RESULT_SIZE, AF3_RESULT_SHA256),
        FileRecord(C1_MANIFEST, C1_MANIFEST_SIZE, C1_MANIFEST_SHA256),
    )
    with HeldFiles(bootstrap) as held_bootstrap:
        af3 = exact_document(held_bootstrap.read(AF3_RESULT), "AF3 result")
        c1_manifest_records = parse_manifest(held_bootstrap.read(C1_MANIFEST))
        held_bootstrap.final()
    sized_c1_records = []
    for record in c1_manifest_records:
        info = os.stat(ROOT / record.filename, follow_symlinks=False)
        sized_c1_records.append(FileRecord(record.filename, info.st_size, record.sha256))
    records = legacy_records(af3) + tuple(sized_c1_records)
    merged = {record.filename: record for record in records}
    require(len(merged) == len(records), "cross-frontier filename collision")
    with HeldFiles(tuple(sorted(merged.values(), key=lambda record: record.filename))) as held:
        c1_result = exact_document(held.read(C1_RESULT), "C1 result")
        obligation = exact_document(held.read(C1_OBLIGATION), "C1 obligation")
        require(c1_result["corrected_census"]["member_count"] == 564_460, "corrected member count")
        require(c1_result["corrected_census"]["family_member_counts"] == EXPECTED_FAMILIES, "corrected family census")
        require(c1_result["corrected_census"]["representation_count"] == 611_872, "corrected representation count")
        require(c1_result["corrected_census"]["physical_incidence_count"] == 115_424, "corrected incidence count")
        require(c1_result["corrected_census"]["semantic_gap_count"] == 154_032, "corrected gap count")
        require(c1_result["formal_credit"] == ZERO_CREDIT, "C1 zero credit")
        require(obligation["corrected_total"] == 824_800 and obligation["known_final_feature_ledger_row_count"] is None, "corrected obligation semantics")
        legacy = af3["authority_contract"]
        require(legacy["six_partition_census"]["member_count"] == 564_492, "legacy member count")
        require(legacy["theorem_obligation_census"] == 824_864, "legacy obligation count")
        authority_files = legacy["authority_files"]
        table_authorities = legacy["table_authorities"]
        body = {
            "schema": SCHEMA,
            "status": "PASS_CORRECTED_CONSTRUCTION_SOURCE_AUTHORITY_FRONTIER__ZERO_SUPPORT_CREDIT",
            "source_snapshot": {
                "legacy_transitive_file_count": 143,
                "legacy_transitive_file_bytes": af3["transitive_file_bytes"],
                "legacy_closure_records_sha256": af3["closure"]["records_sha256"],
                "legacy_closure_edges_sha256": af3["closure"]["edges_sha256"],
                "construction_authority_file_count": len(authority_files),
                "construction_authority_file_catalog_sha256": object_sha(authority_files),
                "table_authority_count": len(table_authorities),
                "table_authority_catalog_sha256": object_sha(table_authorities),
                "C1_manifest_filename": C1_MANIFEST,
                "C1_manifest_sha256": C1_MANIFEST_SHA256,
                "C1_manifest_member_count": len(c1_manifest_records),
                "C1_manifest_members_sha256": object_sha([record.__dict__ for record in c1_manifest_records]),
            },
            "authority_precedence": [
                "C1_CORRECTED_MEMBER_COMPONENT_AND_IDENTITY_ROWS",
                "SURVIVING_MEMBER_FILTER_OVER_LEGACY_SUPPORT_CONSTRUCTION_TABLES",
                "LEGACY_GEOMETRIC_AND_ANALYTIC_CONSTRUCTION_ROWS",
                "OUTER_ENVELOPE_AND_DIAGNOSTIC_ROWS_PROVENANCE_ONLY",
            ],
            "corrected_partition": {
                "exhaustive": True,
                "mutually_exclusive": True,
                "member_count": 564_460,
                "family_member_counts": EXPECTED_FAMILIES,
                "legacy_member_count": 564_492,
                "invalidated_member_count": 32,
                "family_deltas": {"PRESERVED": 0, "NON_GRAPH": 0, "R2": 0, "R292": 0, "G2A": -16, "G2B": -16},
                "G2B_valid_reference_count": 76_832,
                "G2B_unique_member_count": 76_816,
                "G2B_duplicate_reference_excess": 16,
            },
            "corrected_obligation_census": {
                "count": 824_800,
                "legacy_count": 824_864,
                "delta": -64,
                "is_final_feature_ledger_row_count": False,
            },
            "construction_authority_files": authority_files,
            "table_authorities": table_authorities,
            "field_scoped_precedence": legacy["field_scoped_precedence"],
            "authority_role_policies": legacy["authority_role_policies"],
            "migration_rules": {
                "legacy_identity_binding_rows_are_authoritative": False,
                "legacy_component_ids_are_authoritative": False,
                "legacy_support_rows_for_invalidated_members_are_admissible": False,
                "surviving_legacy_geometry_may_be_used_as_construction_input": True,
                "outer_envelope_or_inner_witness_may_equal_full_support": False,
                "typed_AST_certificate_and_representation_pullback_required": True,
                "new_legal_cross_component_edge_requires_full_reclosure": True,
            },
            "formal_credit": ZERO_CREDIT,
            "normalized_support_sealed": False,
            "B1A_permitted": False,
            "B2_permitted": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**body, "authority_frontier_sha256": object_sha(body)}
        held.final()
        return result


def publish(path: Path, payload: bytes) -> None:
    require(not path.exists(), "output no-clobber")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-result", action="store_true")
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    require(args.print_result != (args.candidate_dir is not None), "exactly one mode")
    result = construct()
    payload = canonical(result)
    if args.print_result:
        sys.stdout.buffer.write(payload + b"\n")
    else:
        candidate = Path(args.candidate_dir).resolve()
        require(os.path.commonpath((str(candidate), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
        candidate.mkdir(mode=0o700, parents=False, exist_ok=False)
        publish(candidate / OUTPUT, payload)
        print(json.dumps({"status": result["status"], "output": OUTPUT, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "authority_frontier_sha256": result["authority_frontier_sha256"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
