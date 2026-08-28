#!/usr/bin/env python3
"""Data-driven no-credit migration preflight for corrected Round306C1."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Final, Iterator


class Rejected(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306c1_source_g_corrected_identity_support_migration_preflight"
SCHEMA: Final = "cm2.round306c1.source-g-corrected-identity-support-migration-preflight.v1"
RESULT_NAME: Final = PREFIX + "_result.json"


@dataclass(frozen=True)
class Pin:
    role: str
    filename: str
    size: int
    sha256: str


PINS: Final = (
    Pin("C0_MANIFEST", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_manifest.sha256", 2_182, "9ddb6e0ad37b634de8b2edf8573247e7c1263a5c3693c77a7d001241712b25f8"),
    Pin("C0_INVALIDATION", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_member_invalidation_ledger.jsonl.gz", 11_867, "865185d9b49d4e220459cb083683fd5a074f63eff4f7f2f8217a5c5204991eae"),
    Pin("C0_ROOT_DISPOSITION", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_base_root_disposition_ledger.jsonl.gz", 115_696_187, "6c8e84a6f247a00470f4abd2b6bb7c4caff6ff813236c3e63f04b884998eccdb"),
    Pin("C0_MEMBER_COMPONENT", "cm2_round306c0_source_g_r235d_corrected_fresh_freeze_fresh_member_component_ledger.jsonl.gz", 188_288_564, "81c5a772b12dfb0cf9196b13319bbdff7b07806f6df22d9966a4fc9399bed12e"),
    Pin("I4_MANIFEST", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_manifest.sha256", 2_176, "53b84967618f80c0781c6728ceef4f0e88df7862bd37c5f4cae4055caf960051"),
    Pin("I4_MEMBER", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_member_ledger.jsonl.gz", 245_580_399, "0fbdbbb35b833272429499c005e3d24eb1c669cd5d557898e72605668347b4c8"),
    Pin("I4_REPRESENTATION", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_representation_ledger.jsonl.gz", 162_325_503, "3adcddcf414d2aedc23dab6770cd11ba3dbcf1f911573d5686a7d287b7094712"),
    Pin("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    Pin("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    Pin("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    Pin("B1G0_GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
)

FAMILIES: Final = ("PRESERVED", "NON_GRAPH", "R2", "R292", "G2A", "G2B")
EXPECTED_MEMBERS: Final = {
    "PRESERVED": 126_468, "NON_GRAPH": 17_828, "R2": 295_336,
    "R292": 9_404, "G2A": 38_608, "G2B": 76_816,
}
EXPECTED_REPRESENTATIONS: Final = {
    "PRESERVED": 165_744, "NON_GRAPH": 17_828, "R2": 302_624,
    "R292": 10_252, "G2A": 38_608, "G2B": 76_816,
}
EXPECTED_REBINDS: Final = {
    "PRESERVED": 14_400, "NON_GRAPH": 1_776, "R2": 800,
    "R292": 3_776, "G2A": 584, "G2B": 512,
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def hash_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    hasher = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1_048_576)
        if not chunk:
            return hasher.hexdigest()
        hasher.update(chunk)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.fds: dict[str, int] = {}
        self.ids: dict[str, tuple[int, ...]] = {}

    def __enter__(self) -> "Snapshot":
        before_dir = os.stat(ROOT, follow_symlinks=False)
        require(stat.S_ISDIR(before_dir.st_mode) and not ROOT.is_symlink(), "deliverables directory")
        self.dirfd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        for pin in PINS:
            before = os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == pin.size, "pin stat:" + pin.role)
            fd = os.open(pin.filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.dirfd)
            opened = os.fstat(fd)
            require(identity(opened) == identity(before), "pin race:" + pin.role)
            first = hash_fd(fd); second = hash_fd(fd)
            require(first == second == pin.sha256, "pin digest:" + pin.role)
            self.fds[pin.role] = fd
            self.ids[pin.role] = identity(opened)
        return self

    def duplicate(self, role: str) -> int:
        duplicate = os.dup(self.fds[role])
        os.lseek(duplicate, 0, os.SEEK_SET)
        return duplicate

    def final_revalidate(self) -> None:
        for pin in reversed(PINS):
            fd = self.fds[pin.role]
            require(identity(os.fstat(fd)) == self.ids[pin.role], "final held identity:" + pin.role)
            require(identity(os.stat(pin.filename, dir_fd=self.dirfd, follow_symlinks=False)) == self.ids[pin.role], "final path identity:" + pin.role)
            require(hash_fd(fd) == pin.sha256, "final digest:" + pin.role)

    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dirfd >= 0:
            os.close(self.dirfd)


def jsonl_rows(snapshot: Snapshot, role: str) -> Iterator[dict[str, Any]]:
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    require(line.endswith(b"\n") and len(line) <= 8_388_609, "jsonl wire:" + role)
                    value = json.loads(line)
                    require(type(value) is dict and canonical(value) + b"\n" == line, "jsonl canonical:" + role + ":" + str(ordinal))
                    yield value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def gzip_document(snapshot: Snapshot, role: str) -> dict[str, Any]:
    fd = snapshot.duplicate(role)
    try:
        with os.fdopen(fd, "rb", closefd=True) as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                value = json.load(stream)
        require(type(value) is dict, "gzip document:" + role)
        return value
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def sequence_sha(values: list[str]) -> str:
    return object_sha(values)


def build_result(snapshot: Snapshot) -> dict[str, Any]:
    invalid_ids = sorted(row["registry_member_id"] for row in jsonl_rows(snapshot, "C0_INVALIDATION"))
    require(len(invalid_ids) == len(set(invalid_ids)) == 32, "C0 invalidation census")

    rekey_components: set[str] = set()
    for row in jsonl_rows(snapshot, "C0_ROOT_DISPOSITION"):
        if row["disposition"] == "REKEY_ROOT":
            rekey_components.add(row["old_component_id"])
    require(len(rekey_components) == 4, "rekey old component census")

    c0_members: dict[str, tuple[str, str, str]] = {}
    for row in jsonl_rows(snapshot, "C0_MEMBER_COMPONENT"):
        member_id = row["registry_member_id"]
        require(member_id not in c0_members, "duplicate C0 member")
        c0_members[member_id] = (row["corrected_component_id"], row["row_id"], row["row_sha256"])
    require(len(c0_members) == 564_460, "C0 member census")

    old_member_counts = Counter()
    corrected_member_counts = Counter()
    absent_member_counts = Counter()
    rebind_counts = Counter()
    absent_from_i4: list[str] = []
    surviving_member_ids: dict[str, list[str]] = {family: [] for family in FAMILIES}
    for row in jsonl_rows(snapshot, "I4_MEMBER"):
        family = row["coarse_family"]
        require(family in surviving_member_ids, "I4 member family")
        member_id = row["member_id"]
        old_member_counts[family] += 1
        if member_id not in c0_members:
            absent_member_counts[family] += 1
            absent_from_i4.append(member_id)
            continue
        corrected_member_counts[family] += 1
        surviving_member_ids[family].append(member_id)
        if row["Round306A_component_id"] in rekey_components:
            rebind_counts[family] += 1
    require(sorted(absent_from_i4) == invalid_ids, "I4 missing set equals exact C0 invalidation set")
    require(dict(corrected_member_counts) == EXPECTED_MEMBERS, "corrected member family census")
    require(dict(rebind_counts) == EXPECTED_REBINDS, "affected rebind family census")

    old_representation_counts = Counter()
    corrected_representation_counts = Counter()
    absent_representation_counts = Counter()
    surviving_representation_ids: dict[str, list[str]] = {family: [] for family in FAMILIES}
    for row in jsonl_rows(snapshot, "I4_REPRESENTATION"):
        family = row["coarse_family"]
        old_representation_counts[family] += 1
        if row["owner_member_id"] not in c0_members:
            absent_representation_counts[family] += 1
            continue
        corrected_representation_counts[family] += 1
        surviving_representation_ids[family].append(row["representation_id"])
    require(dict(corrected_representation_counts) == EXPECTED_REPRESENTATIONS, "corrected representation family census")

    sheet_rows = gzip_document(snapshot, "B1G0_SHEET")["graph_sheet_join_rows"]
    selected_sheet = [row for row in sheet_rows if row["sheet_member_id"] in c0_members]
    require(len(selected_sheet) == 38_608, "corrected sheet incidence census")

    side_rows = gzip_document(snapshot, "B1G0_SIDE")["graph_side_join_rows"]
    selected_side_by_member: dict[str, dict[str, Any]] = {}
    valid_side_reference_count = 0
    for row in side_rows:
        member_id = row["side_member_id"]
        if member_id not in c0_members:
            continue
        valid_side_reference_count += 1
        prior = selected_side_by_member.get(member_id)
        if prior is None or row["Round306B1G0_graph_side_join_row_id"] < prior["Round306B1G0_graph_side_join_row_id"]:
            selected_side_by_member[member_id] = row
    require(valid_side_reference_count == 76_832, "valid side reference census")
    require(len(selected_side_by_member) == 76_816, "corrected unique side incidence census")

    gap_rows = gzip_document(snapshot, "B1G0_GAP")["gap_rows"]
    selected_gap_ids: list[str] = []
    side_gap_by_member: dict[str, dict[str, Any]] = {}
    gap_kind_counts = Counter()
    for row in gap_rows:
        member_id = row["member_id"]
        if member_id not in c0_members:
            continue
        if row["gap_kind"] == "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING":
            prior = side_gap_by_member.get(member_id)
            if prior is None or row["Round306B1G0_gap_row_id"] < prior["Round306B1G0_gap_row_id"]:
                side_gap_by_member[member_id] = row
        else:
            selected_gap_ids.append(row["Round306B1G0_gap_row_id"])
            gap_kind_counts[row["gap_kind"]] += 1
    for row in side_gap_by_member.values():
        selected_gap_ids.append(row["Round306B1G0_gap_row_id"])
        gap_kind_counts[row["gap_kind"]] += 1
    require(len(selected_gap_ids) == 154_032, "corrected gap census")
    require(gap_kind_counts == Counter({
        "SOURCE_FREE_GRAPH_DEFINITION_THEOREM_PENDING": 38_608,
        "GRAPH_TO_SHEET_PHYSICAL_IDENTIFICATION_THEOREM_PENDING": 38_608,
        "GRAPH_SIDE_POSITIVE_3D_PHYSICAL_INCIDENCE_THEOREM_PENDING": 76_816,
    }), "corrected gap kind census")

    family_receipts = {}
    for family in FAMILIES:
        member_ids = sorted(surviving_member_ids[family])
        representation_ids = sorted(surviving_representation_ids[family])
        family_receipts[family] = {
            "member_count": len(member_ids),
            "member_ids_sha256": sequence_sha(member_ids),
            "representation_count": len(representation_ids),
            "representation_ids_sha256": sequence_sha(representation_ids),
            "affected_component_rebind_count": rebind_counts[family],
        }

    source_frontier = [
        {"role": pin.role, "filename": pin.filename, "size": pin.size, "sha256": pin.sha256}
        for pin in PINS
    ]
    body = {
        "schema": SCHEMA + ".result.v1",
        "status": "PASS_DATA_DRIVEN_CORRECTED_SIX_FAMILY_MIGRATION_PREFLIGHT__ZERO_SUPPORT_CREDIT",
        "source_frontier": source_frontier,
        "source_frontier_sha256": object_sha(source_frontier),
        "family_order": list(FAMILIES),
        "family_receipts": family_receipts,
        "old_member_counts": dict(old_member_counts),
        "corrected_member_counts": dict(corrected_member_counts),
        "absent_member_counts": dict(absent_member_counts),
        "old_representation_counts": dict(old_representation_counts),
        "corrected_representation_counts": dict(corrected_representation_counts),
        "absent_representation_counts": dict(absent_representation_counts),
        "exact_C0_invalid_member_ids_sha256": sequence_sha(invalid_ids),
        "I4_absent_member_ids_equal_exact_C0_invalidation_set": True,
        "corrected_member_count": sum(corrected_member_counts.values()),
        "corrected_representation_count": sum(corrected_representation_counts.values()),
        "rekey_old_component_count": len(rekey_components),
        "affected_component_rebind_count": sum(rebind_counts.values()),
        "physical_incidence": {
            "sheet_count": len(selected_sheet),
            "valid_side_reference_count": valid_side_reference_count,
            "unique_side_member_count": len(selected_side_by_member),
            "duplicate_side_reference_excess": valid_side_reference_count - len(selected_side_by_member),
            "corrected_total": len(selected_sheet) + len(selected_side_by_member),
            "selected_sheet_source_row_ids_sha256": sequence_sha(sorted(row["Round306B1G0_graph_sheet_join_row_id"] for row in selected_sheet)),
            "selected_side_source_row_ids_sha256": sequence_sha(sorted(row["Round306B1G0_graph_side_join_row_id"] for row in selected_side_by_member.values())),
        },
        "semantic_gap": {
            "corrected_total": len(selected_gap_ids),
            "counts_by_kind": dict(gap_kind_counts),
            "selected_source_gap_row_ids_sha256": sequence_sha(sorted(selected_gap_ids)),
        },
        "theorem_obligation_census_not_feature_ledger_rows": 824_800,
        "outer_envelope_or_inner_witness_may_substitute_for_full_support": False,
        "formal_credit": {
            "normalized_support": 0, "representation_cover": 0, "A1_A2": 0,
            "physical_incidence": 0, "B1A": 0, "B2": 0, "maximality": 0,
            "fibre": 0, "global_disposition": 0, "CM2": 0,
        },
    }
    return {**body, "result_sha256": object_sha(body)}


def source_sha() -> str:
    path = Path(__file__)
    before = os.stat(path, follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "construction source")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        require(identity(os.fstat(fd)) == identity(before), "construction source race")
        first = hash_fd(fd); second = hash_fd(fd)
        require(first == second, "construction source digest")
        return first
    finally:
        os.close(fd)


def run(publish: bool) -> dict[str, Any]:
    with Snapshot() as snapshot:
        result = build_result(snapshot)
        snapshot.final_revalidate()
    body = dict(result)
    claimed = body.pop("result_sha256")
    body["construction_source_filename"] = Path(__file__).name
    body["construction_source_sha256"] = source_sha()
    result = {**body, "result_sha256": object_sha(body)}
    require(claimed != result["result_sha256"], "source binding changes result closure")
    if publish:
        output = ROOT / RESULT_NAME
        require(not output.exists(), "result no-clobber")
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
        try:
            os.write(fd, canonical(result)); os.fsync(fd)
        finally:
            os.close(fd)
    return result


def main() -> int:
    require(type(sys.flags.isolated) is int and sys.flags.isolated == 1, "python -I required")
    require(sys.dont_write_bytecode is True, "python -B required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    require(args.publish != args.no_write, "choose exactly one mode")
    print(json.dumps(run(args.publish), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
