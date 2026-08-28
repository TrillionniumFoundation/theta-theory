#!/usr/bin/env python3
"""Independent verifier for the corrected full-support authority frontier."""

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
PREFIX: Final = "cm2_round306c2_source_g_corrected_full_support_authority_frontier"
OUTPUT: Final = PREFIX + ".json"
ATTACK: Final = PREFIX + "_attack_suite.json"
VERIFICATION: Final = PREFIX + "_verification.json"
REPORT: Final = PREFIX + "_report.md"
COLD: Final = PREFIX + "_cold_replay.md"
MANIFEST: Final = PREFIX + "_manifest.sha256"
SCHEMA: Final = "cm2.round306c2.source-g-corrected-full-support-authority-frontier.v1"
AF3_RESULT: Final = "cm2_round306b1af3_source_g_full_support_construction_source_authority_frontier_independent_replay_result.json"
C1_MANIFEST: Final = "cm2_round306c1_source_g_corrected_identity_support_replay_manifest.sha256"
C1_PREFIX: Final = "cm2_round306c1_source_g_corrected_identity_support_replay"
C1_RESULT: Final = C1_PREFIX + "_result.json"
C1_OBLIGATION: Final = C1_PREFIX + "_theorem_obligation_census.json"
PRODUCER: Final = PREFIX + "_producer.py"
BOOTSTRAP: Final = {
    AF3_RESULT: (198_283, "5b9a4ba7920fb4fc98615fa9b69fb3dd6e4201ef76c4d2005fde6f85e777071f"),
    C1_MANIFEST: (2_398, "9adfc1499f2c376085b1e7166cce43e41374ac81f4f10ad87409b0d9b14e4b7c"),
    PRODUCER: (13_698, "ec505b7be99fc0d8a4e943d478c9f110c9b38495940e5f92322091c1361e98af"),
}
FAMILIES: Final = {"PRESERVED": 126_468, "NON_GRAPH": 17_828, "R2": 295_336, "R292": 9_404, "G2A": 38_608, "G2B": 76_816}
ZERO: Final = {"normalized_support": 0, "representation_cover": 0, "A1_A2": 0, "physical_incidence": 0, "pullback_equivalence": 0, "transition": 0, "B1A": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0}
MANIFEST_MEMBERS: Final = (PRODUCER, OUTPUT, Path(__file__).name, ATTACK, VERIFICATION, REPORT, COLD)


@dataclass(frozen=True)
class Record:
    filename: str
    size: int
    sha256: str


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def ident(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def digest_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    value = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return value.hexdigest()
        value.update(chunk)


def bytes_fd(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    output = []
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return b"".join(output)
        output.append(chunk)


class Snapshot:
    def __init__(self, records: tuple[Record, ...], directory: Path = ROOT) -> None:
        self.records = records
        self.directory = directory
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before = os.stat(self.directory, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not self.directory.is_symlink(), "snapshot directory")
        self.dirfd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for record in self.records:
            info = os.stat(record.filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size == record.size, "snapshot identity:" + record.filename)
            fd = os.open(record.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            need(ident(opened) == ident(info), "snapshot race:" + record.filename)
            need(digest_fd(fd) == digest_fd(fd) == record.sha256, "snapshot digest:" + record.filename)
            self.fds[record.filename] = fd
            self.ids[record.filename] = ident(opened)
        return self

    def read(self, filename: str) -> bytes:
        return bytes_fd(self.fds[filename])

    def final(self) -> None:
        for record in reversed(self.records):
            need(ident(os.fstat(self.fds[record.filename])) == self.ids[record.filename], "final fd:" + record.filename)
            need(ident(os.stat(record.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[record.filename], "final path:" + record.filename)
            need(digest_fd(self.fds[record.filename]) == record.sha256, "final digest:" + record.filename)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def document(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and raw in (canonical(value), canonical(value) + b"\n"), "document:" + label)
    return value


def manifest_records(raw: bytes) -> tuple[Record, ...]:
    need(raw.endswith(b"\n"), "manifest newline")
    records = []
    for line in raw.decode("ascii").splitlines():
        digest, filename = line.split("  ")
        need(len(digest) == 64, "manifest digest")
        info = os.stat(ROOT / filename, follow_symlinks=False)
        records.append(Record(filename, info.st_size, digest))
    need(len(records) == 16 and len({record.filename for record in records}) == 16, "manifest count")
    return tuple(records)


def source_records(af3: dict[str, Any]) -> tuple[Record, ...]:
    merged: dict[str, Record] = {}
    for rows in (af3["closure"]["records"], af3["governance_seals"]["records"], af3["authority_contract"]["authority_files"]):
        for row in rows:
            current = Record(row["filename"], row.get("exact_size", row.get("size")), row["sha256"])
            previous = merged.setdefault(current.filename, current)
            need(previous == current, "catalog conflict:" + current.filename)
    need(len(af3["closure"]["records"]) == 143 and len(af3["authority_contract"]["authority_files"]) == 45, "legacy file census")
    need(len(af3["authority_contract"]["table_authorities"]) == 82, "legacy table census")
    return tuple(sorted(merged.values(), key=lambda row: row.filename))


def closed_frontier(raw: bytes) -> dict[str, Any]:
    value = document(raw, "candidate frontier")
    body = dict(value)
    claimed = body.pop("authority_frontier_sha256", None)
    need(type(claimed) is str and claimed == objsha(body), "candidate object closure")
    need(value["schema"] == SCHEMA, "candidate schema")
    need(value["status"] == "PASS_CORRECTED_CONSTRUCTION_SOURCE_AUTHORITY_FRONTIER__ZERO_SUPPORT_CREDIT", "candidate status")
    partition = value["corrected_partition"]
    need(partition["member_count"] == 564_460 and partition["family_member_counts"] == FAMILIES, "candidate corrected partition")
    need(partition["invalidated_member_count"] == 32 and partition["family_deltas"] == {"PRESERVED": 0, "NON_GRAPH": 0, "R2": 0, "R292": 0, "G2A": -16, "G2B": -16}, "candidate invalidation delta")
    need(value["corrected_obligation_census"] == {"count": 824_800, "legacy_count": 824_864, "delta": -64, "is_final_feature_ledger_row_count": False}, "candidate obligations")
    snapshot = value["source_snapshot"]
    need(snapshot["legacy_transitive_file_count"] == 143 and snapshot["construction_authority_file_count"] == 45 and snapshot["table_authority_count"] == 82, "candidate source census")
    need(snapshot["C1_manifest_sha256"] == BOOTSTRAP[C1_MANIFEST][1] and snapshot["C1_manifest_member_count"] == 16, "candidate C1 seal")
    need(len(value["construction_authority_files"]) == 45 and len(value["table_authorities"]) == 82, "candidate catalogs")
    need(value["formal_credit"] == ZERO and value["normalized_support_sealed"] is False and value["B1A_permitted"] is False and value["B2_permitted"] is False and value["CM2"] == "NO-GO_FOR_CLAIM", "candidate zero credit")
    rules = value["migration_rules"]
    need(rules["legacy_identity_binding_rows_are_authoritative"] is False and rules["legacy_component_ids_are_authoritative"] is False and rules["legacy_support_rows_for_invalidated_members_are_admissible"] is False, "candidate legacy demotion")
    need(rules["outer_envelope_or_inner_witness_may_equal_full_support"] is False and rules["typed_AST_certificate_and_representation_pullback_required"] is True and rules["new_legal_cross_component_edge_requires_full_reclosure"] is True, "candidate construction gates")
    return value


def candidate_raw(candidate_dir: Path) -> tuple[bytes, Record]:
    resolved = candidate_dir.resolve()
    need(os.path.commonpath((str(resolved), str(ROOT.resolve()))) != str(ROOT.resolve()), "candidate outside deliverables")
    before = os.stat(candidate_dir, follow_symlinks=False)
    need(stat.S_ISDIR(before.st_mode) and set(os.listdir(candidate_dir)) == {OUTPUT}, "candidate exact directory")
    info = os.stat(candidate_dir / OUTPUT, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "candidate file identity")
    fd = os.open(candidate_dir / OUTPUT, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(fd)
        need(ident(opened) == ident(info), "candidate open race")
        first = digest_fd(fd)
        need(first == digest_fd(fd), "candidate two-pass digest")
        raw = bytes_fd(fd)
        need(ident(os.fstat(fd)) == ident(opened), "candidate final fd")
    finally:
        os.close(fd)
    need(ident(os.stat(candidate_dir / OUTPUT, follow_symlinks=False)) == ident(info), "candidate final path")
    closed_frontier(raw)
    return raw, Record(OUTPUT, info.st_size, first)


def expected_frontier(af3: dict[str, Any], c1_manifest: tuple[Record, ...], c1_result: dict[str, Any], obligation: dict[str, Any]) -> dict[str, Any]:
    need(c1_result["corrected_census"]["member_count"] == 564_460, "C1 members")
    need(c1_result["corrected_census"]["family_member_counts"] == FAMILIES, "C1 families")
    need(c1_result["corrected_census"]["representation_count"] == 611_872, "C1 representations")
    need(c1_result["corrected_census"]["physical_incidence_count"] == 115_424 and c1_result["corrected_census"]["semantic_gap_count"] == 154_032, "C1 incidence and gaps")
    need(c1_result["formal_credit"] == ZERO, "C1 credit")
    need(obligation["corrected_total"] == 824_800 and obligation["known_final_feature_ledger_row_count"] is None, "C1 obligations")
    legacy = af3["authority_contract"]
    need(legacy["six_partition_census"]["member_count"] == 564_492 and legacy["theorem_obligation_census"] == 824_864, "legacy census")
    files = legacy["authority_files"]
    tables = legacy["table_authorities"]
    body = {
        "schema": SCHEMA,
        "status": "PASS_CORRECTED_CONSTRUCTION_SOURCE_AUTHORITY_FRONTIER__ZERO_SUPPORT_CREDIT",
        "source_snapshot": {"legacy_transitive_file_count": 143, "legacy_transitive_file_bytes": af3["transitive_file_bytes"], "legacy_closure_records_sha256": af3["closure"]["records_sha256"], "legacy_closure_edges_sha256": af3["closure"]["edges_sha256"], "construction_authority_file_count": len(files), "construction_authority_file_catalog_sha256": objsha(files), "table_authority_count": len(tables), "table_authority_catalog_sha256": objsha(tables), "C1_manifest_filename": C1_MANIFEST, "C1_manifest_sha256": BOOTSTRAP[C1_MANIFEST][1], "C1_manifest_member_count": 16, "C1_manifest_members_sha256": objsha([record.__dict__ | {"size": -1} for record in c1_manifest])},
        "authority_precedence": ["C1_CORRECTED_MEMBER_COMPONENT_AND_IDENTITY_ROWS", "SURVIVING_MEMBER_FILTER_OVER_LEGACY_SUPPORT_CONSTRUCTION_TABLES", "LEGACY_GEOMETRIC_AND_ANALYTIC_CONSTRUCTION_ROWS", "OUTER_ENVELOPE_AND_DIAGNOSTIC_ROWS_PROVENANCE_ONLY"],
        "corrected_partition": {"exhaustive": True, "mutually_exclusive": True, "member_count": 564_460, "family_member_counts": FAMILIES, "legacy_member_count": 564_492, "invalidated_member_count": 32, "family_deltas": {"PRESERVED": 0, "NON_GRAPH": 0, "R2": 0, "R292": 0, "G2A": -16, "G2B": -16}, "G2B_valid_reference_count": 76_832, "G2B_unique_member_count": 76_816, "G2B_duplicate_reference_excess": 16},
        "corrected_obligation_census": {"count": 824_800, "legacy_count": 824_864, "delta": -64, "is_final_feature_ledger_row_count": False},
        "construction_authority_files": files,
        "table_authorities": tables,
        "field_scoped_precedence": legacy["field_scoped_precedence"],
        "authority_role_policies": legacy["authority_role_policies"],
        "migration_rules": {"legacy_identity_binding_rows_are_authoritative": False, "legacy_component_ids_are_authoritative": False, "legacy_support_rows_for_invalidated_members_are_admissible": False, "surviving_legacy_geometry_may_be_used_as_construction_input": True, "outer_envelope_or_inner_witness_may_equal_full_support": False, "typed_AST_certificate_and_representation_pullback_required": True, "new_legal_cross_component_edge_requires_full_reclosure": True},
        "formal_credit": ZERO,
        "normalized_support_sealed": False,
        "B1A_permitted": False,
        "B2_permitted": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "authority_frontier_sha256": objsha(body)}


def reconstruct() -> dict[str, Any]:
    bootstrap_records = tuple(Record(name, size, digest) for name, (size, digest) in BOOTSTRAP.items())
    with Snapshot(bootstrap_records) as bootstrap:
        af3 = document(bootstrap.read(AF3_RESULT), "AF3")
        c1_manifest = manifest_records(bootstrap.read(C1_MANIFEST))
        bootstrap.final()
    all_records = source_records(af3) + c1_manifest
    merged = {record.filename: record for record in all_records}
    need(len(merged) == len(all_records), "frontier collision")
    with Snapshot(tuple(sorted(merged.values(), key=lambda row: row.filename))) as sources:
        c1_result = document(sources.read(C1_RESULT), "C1 result")
        obligation = document(sources.read(C1_OBLIGATION), "C1 obligation")
        expected = expected_frontier(af3, c1_manifest, c1_result, obligation)
        sources.final()
    return expected


def receipt(candidate_record: Record, expected: dict[str, Any]) -> dict[str, Any]:
    return {"status": "PASS_INDEPENDENT_CORRECTED_AUTHORITY_FRONTIER_REPLAY__ZERO_SUPPORT_CREDIT", "candidate_filename": OUTPUT, "candidate_size": candidate_record.size, "candidate_sha256": candidate_record.sha256, "authority_frontier_sha256": expected["authority_frontier_sha256"], "legacy_source_file_count": 143, "construction_authority_file_count": 45, "table_authority_count": 82, "corrected_member_count": 564_460, "corrected_obligation_count": 824_800, "producer_imported_or_executed": False, "formal_credit": ZERO}


def verify(candidate_dir: Path) -> dict[str, Any]:
    raw, candidate_record = candidate_raw(candidate_dir)
    expected = reconstruct()
    need(raw == canonical(expected), "candidate byte identity")
    return receipt(candidate_record, expected)


def self_sha() -> str:
    path = Path(__file__)
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "verifier identity")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        need(ident(os.fstat(fd)) == ident(info), "verifier race")
        value = digest_fd(fd)
        need(value == digest_fd(fd), "verifier digest")
        return value
    finally:
        os.close(fd)


def rewrite(path: Path, mutator: Any) -> None:
    value = json.loads(path.read_bytes())
    mutator(value)
    body = dict(value)
    body.pop("authority_frontier_sha256", None)
    value = {**body, "authority_frontier_sha256": objsha(body)}
    path.write_bytes(canonical(value))


def attack_suite(candidate_dir: Path) -> dict[str, Any]:
    baseline = verify(candidate_dir)
    work = Path(tempfile.mkdtemp(prefix="cm2-c2-authority-attacks-"))
    original = candidate_dir / OUTPUT
    attacks = []
    def restore() -> None:
        path = work / OUTPUT
        if path.exists() or path.is_symlink():
            path.unlink()
        shutil.copyfile(original, path)
    def execute(attack_id: str, mutation: Any, cleanup: Any | None = None) -> None:
        restore()
        try:
            mutation()
            boundary = None
            try:
                verify(work)
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
        execute("A02_MISSING_FILE", lambda: (work / OUTPUT).unlink())
        execute("A03_SYMLINK", lambda: ((work / OUTPUT).unlink(), (work / OUTPUT).symlink_to(original)))
        def hardlink() -> None:
            (work / OUTPUT).unlink()
            target = work.parent / (work.name + "-target")
            shutil.copyfile(original, target)
            os.link(target, work / OUTPUT)
        execute("A04_HARDLINK", hardlink, lambda: (work.parent / (work.name + "-target")).unlink())
        execute("A05_SCHEMA", lambda: rewrite(work / OUTPUT, lambda value: value.__setitem__("schema", "foreign")))
        execute("A06_MEMBER_COUNT", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_partition"].__setitem__("member_count", 564_492)))
        execute("A07_G2A_COUNT", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_partition"]["family_member_counts"].__setitem__("G2A", 38_624)))
        execute("A08_G2B_COUNT", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_partition"]["family_member_counts"].__setitem__("G2B", 76_832)))
        execute("A09_OBLIGATION_COUNT", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_obligation_census"].__setitem__("count", 824_864)))
        execute("A10_FEATURE_LEDGER_CONFUSION", lambda: rewrite(work / OUTPUT, lambda value: value["corrected_obligation_census"].__setitem__("is_final_feature_ledger_row_count", True)))
        execute("A11_C1_MANIFEST_SUBSTITUTION", lambda: rewrite(work / OUTPUT, lambda value: value["source_snapshot"].__setitem__("C1_manifest_sha256", "0" * 64)))
        execute("A12_AUTHORITY_FILE_DROP", lambda: rewrite(work / OUTPUT, lambda value: value["construction_authority_files"].pop()))
        execute("A13_TABLE_DROP", lambda: rewrite(work / OUTPUT, lambda value: value["table_authorities"].pop()))
        execute("A14_CREDIT_INJECTION", lambda: rewrite(work / OUTPUT, lambda value: value["formal_credit"].__setitem__("normalized_support", 1)))
        execute("A15_OUTER_WITNESS_PROMOTION", lambda: rewrite(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("outer_envelope_or_inner_witness_may_equal_full_support", True)))
        execute("A16_DISABLE_RECLOSURE", lambda: rewrite(work / OUTPUT, lambda value: value["migration_rules"].__setitem__("new_legal_cross_component_edge_requires_full_reclosure", False)))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    need(len(attacks) == 16, "attack count")
    body = {"schema": SCHEMA + ".coherent-attack-suite.v1", "status": "PASS_16_OF_16_COHERENT_ATTACKS_REJECTED", "verifier_filename": Path(__file__).name, "verifier_file_sha256": self_sha(), "attack_count": 16, "rejected_count": 16, "all_rejected": True, "baseline_candidate_sha256": baseline["candidate_sha256"], "attacks": attacks}
    return {**body, "attack_suite_sha256": objsha(body)}


def read_closed(path: Path, closure: str) -> tuple[dict[str, Any], bytes]:
    info = os.stat(path, follow_symlinks=False)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "closed document identity:" + path.name)
    raw = path.read_bytes()
    value = document(raw, path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    need(type(claimed) is str and claimed == objsha(body), "closed document digest:" + path.name)
    return value, raw


def verification_doc(result: dict[str, Any]) -> dict[str, Any]:
    suite, raw = read_closed(ROOT / ATTACK, "attack_suite_sha256")
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
        info = os.stat(MANIFEST, dir_fd=self.dirfd, follow_symlinks=False)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "manifest identity")
        self.manifest_fd = os.open(MANIFEST, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
        opened = os.fstat(self.manifest_fd)
        need(ident(opened) == ident(info), "manifest race")
        self.manifest_id = ident(opened)
        raw = bytes_fd(self.manifest_fd)
        need(raw.endswith(b"\n"), "manifest newline")
        lines = raw.decode("ascii").splitlines()
        need(len(lines) == len(MANIFEST_MEMBERS), "manifest count")
        for line, filename in zip(lines, MANIFEST_MEMBERS):
            parts = line.split("  ")
            need(len(parts) == 2 and parts[1] == filename and len(parts[0]) == 64, "manifest ordered member:" + filename)
            expected = parts[0]
            member_info = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(stat.S_ISREG(member_info.st_mode) and member_info.st_nlink == 1, "manifest member identity:" + filename)
            fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            member_opened = os.fstat(fd)
            need(ident(member_opened) == ident(member_info), "manifest member race:" + filename)
            got = digest_fd(fd)
            need(got == digest_fd(fd) == expected, "manifest member digest:" + filename)
            self.fds[filename] = fd
            self.ids[filename] = ident(member_opened)
            self.hashes[filename] = got
        return self

    def read(self, filename: str) -> bytes:
        return bytes_fd(self.fds[filename])

    def final(self) -> None:
        for filename in reversed(MANIFEST_MEMBERS):
            need(ident(os.fstat(self.fds[filename])) == self.ids[filename], "manifest final fd:" + filename)
            need(ident(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[filename], "manifest final path:" + filename)
            need(digest_fd(self.fds[filename]) == self.hashes[filename], "manifest final digest:" + filename)
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
        closed_frontier(raw)
        expected = reconstruct()
        need(raw == canonical(expected), "manifest candidate byte identity")
        candidate_record = Record(OUTPUT, bundle.ids[OUTPUT][4], bundle.hashes[OUTPUT])
        result = receipt(candidate_record, expected)
        need(bundle.read(VERIFICATION) == canonical(verification_doc(result)), "manifest verification byte identity")
        bundle.final()
    return {"status": "PASS_MANIFEST_FIRST_HELD_FD_CORRECTED_AUTHORITY_FRONTIER__ZERO_WRITES_ZERO_SUPPORT_CREDIT", "manifest_filename": MANIFEST, "manifest_member_count": len(MANIFEST_MEMBERS), "candidate_sha256": candidate_record.sha256, "authority_frontier_sha256": expected["authority_frontier_sha256"], "legacy_source_file_count": 143, "construction_authority_file_count": 45, "table_authority_count": 82, "deliverables_write_syscalls": 0, "formal_credit": ZERO}


def publish_document(filename: str, value: dict[str, Any]) -> None:
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
        candidate_dir = Path(args.candidate_dir)
        if args.attack_publish:
            suite = attack_suite(candidate_dir)
            publish_document(ATTACK, suite)
            result = {"status": suite["status"], "attack_count": 16, "attack_suite_sha256": suite["attack_suite_sha256"]}
        else:
            result = verify(candidate_dir)
            if args.verify_publish:
                publish_document(VERIFICATION, verification_doc(result))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
