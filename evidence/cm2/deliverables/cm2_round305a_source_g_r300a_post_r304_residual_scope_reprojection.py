#!/usr/bin/env python3
"""Round305A exact post-Round304 residual-scope reprojection producer.

This producer admits the complete sealed Round300A and Round304 packages,
streams the complete 3,232-row Round300A frontier and the complete 564,492-row
Round304 member/component ledger, and freezes the exact 1,024-pair residual
scope.  Round303B is admitted only as sealed lineage.  No physical inclusion,
component edge, DSU, maximality, fibre, global-disposition, or Jx/Jy credit is
issued here.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
import re
import stat
import tempfile
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, TextIO


PREFIX = "cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection"
FILES = {
    "producer": PREFIX + ".py",
    "ledger": PREFIX + "_scope_reprojection_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
TABLE = "post_Round304_scope_reprojection_rows"
ROW_ID = "Round305A_scope_reprojection_row_id"
ROW_SCHEMA = "cm2.round305a.r300a-post-r304-scope-reprojection-row.v1"
LEDGER_SCHEMA = (
    "cm2.round305a.r300a-post-r304-residual-scope-reprojection.ledger.v1"
)
RESULT_SCHEMA = (
    "cm2.round305a.source-g-r300a-post-r304-residual-scope-reprojection.v1"
)
SEED_A = 305_001
SEED_B = 305_997

R300A_PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
R300A_MANIFEST = R300A_PREFIX + "_manifest.sha256"
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"
R300A_RESULT = R300A_PREFIX + "_result.json"
R300A_VERIFICATION = R300A_PREFIX + "_verification.json"
R300A_MANIFEST_SHA256 = (
    "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8"
)
R300A_LEDGER_FILE_SHA256 = (
    "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d"
)
R300A_RESULT_FILE_SHA256 = (
    "b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4"
)
R300A_RESULT_OBJECT_SHA256 = (
    "dbba3aaa96a494144427709c7d908fc816c12cd9f87ff13ec06a818c832d7f98"
)
R300A_VERIFICATION_FILE_SHA256 = (
    "e976fc2912c1d902029b8c4c7d4864bd8bb1cb6895bc09c215f2a5ac2400c696"
)
R300A_VERIFICATION_OBJECT_SHA256 = (
    "fed82ab1403e0f496245066b469d686b3126a3588c27459d9b0b53f8b08e7495"
)
R300A_PAIR_COMMITMENT = {
    "row_count": 3_232,
    "row_ids_sha256": (
        "876617c3beda3cc50bcff712e6273786ba87a513d5422e875960353c6eb64332"
    ),
    "row_hashes_sha256": (
        "2f34355d24534220e6cf42e636925d0f5adf9d7430b61563f20f2d4d928faac4"
    ),
    "rows_sha256": (
        "7991da0c6f268cfb87628f1bee88f560ed319bec1028bee43e427c65ac8f6f16"
    ),
}

R303B_PREFIX = "cm2_round303b_source_g_unified_attachment_edge_promotion"
R303B_MANIFEST = R303B_PREFIX + "_manifest.sha256"
R303B_RESULT = R303B_PREFIX + "_result.json"
R303B_VERIFICATION = R303B_PREFIX + "_verification.json"
R303B_MANIFEST_SHA256 = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
R303B_RESULT_FILE_SHA256 = (
    "4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1"
)
R303B_RESULT_OBJECT_SHA256 = (
    "2ca258de5a58175164267bd3ca81b0da8b25a4ebffcd998805e8f7254d172fc2"
)
R303B_VERIFICATION_FILE_SHA256 = (
    "6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a"
)
R303B_VERIFICATION_OBJECT_SHA256 = (
    "a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57"
)

R304_PREFIX = "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
R304_MANIFEST = R304_PREFIX + "_manifest.sha256"
R304_MEMBER_LEDGER = R304_PREFIX + "_member_component_ledger.json.gz"
R304_RESULT = R304_PREFIX + "_result.json"
R304_VERIFICATION = R304_PREFIX + "_verification.json"
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)
R304_MEMBER_LEDGER_FILE_SHA256 = (
    "9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0"
)
R304_RESULT_FILE_SHA256 = (
    "2975a8cc61c1b7812fedff6bc9dffd4db8517e822311c54a09317403b3592f7d"
)
R304_RESULT_OBJECT_SHA256 = (
    "d9f0c8b573d8d3462091bb075711a4983219b8eb23a3ac5db91bc83e0ded5a0c"
)
R304_VERIFICATION_FILE_SHA256 = (
    "482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3"
)
R304_VERIFICATION_OBJECT_SHA256 = (
    "9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a"
)
R304_MEMBER_COMMITMENT = {
    "row_count": 564_492,
    "row_ids_sha256": (
        "e9a61126c08810e716f000e34a11983d93249d7ece85ecbe7eeeec74754b25fa"
    ),
    "row_hashes_sha256": (
        "be117bd1cf28af09e13409c26be949ccda1f1927d27791aa55f0329b293152bb"
    ),
    "rows_sha256": (
        "7c32876075c8da2ff243db50e5ff73860dc11a386a91c76130078fa3fd379bb1"
    ),
}

LEGACY_REPROJECTION_SHA256 = (
    "8646795f43524e80a04eeaa7852ba331a3f9767842ee14bcad66db9aa6b03b08"
)
RESIDUAL_PAIR_SET_SHA256 = (
    "f7f9941f84428df71039b4708dfa251eae6c962267f68ccd13945ee445c5bf29"
)
RESIDUAL_ENDPOINT_SET_SHA256 = (
    "b09fe8149f89a95c2c9effcbce33bc49df24065987c870fc65b09ac85fe98779"
)
RESIDUAL_SOURCE_ROW_IDS_SHA256 = (
    "72bebd529ba7bdda941c5cdd198d04a7d4bec878c8f65ea5688929f75e64832c"
)
RESIDUAL_SOURCE_ROW_HASHES_SHA256 = (
    "c726bdc422969e2280457f0ed6d87de03ab63b8d410b6c61171fbf85138a7017"
)
COMPLETE_PAIR_SET_SHA256 = (
    "e7206fca536d237276ccf84da9542e32b3a0c82e44d0e8541275b5a5dead4275"
)
COMPLETE_ENDPOINT_SET_SHA256 = (
    "306c249d452b5778cfb462296c981f1644a430700451df24bee6b735f5eba6f5"
)
PRIOR_WITNESSED_PAIR_SET_SHA256 = (
    "b94b42a876e85fd63123ba88ba4fe7c8ab6731424d1c8f9415f390492fb17699"
)

R300A_EXPECTED_MEMBERS = frozenset(
    {
        R300A_PREFIX + ".py",
        R300A_PREFIX + "_verifier.py",
        R300A_LEDGER,
        R300A_RESULT,
        R300A_PREFIX + "_attack_suite.json",
        R300A_VERIFICATION,
        R300A_PREFIX + "_report.md",
        R300A_PREFIX + "_cold_replay.md",
    }
)
R303B_EXPECTED_MEMBERS = frozenset(
    {
        "cm2_round303b_source_g_unified_attachment_edge_producer.py",
        R303B_PREFIX + "_b1_graph_attachment_lemma_ledger.json.gz",
        R303B_PREFIX + "_b2a_analytic_sheet_lemma_ledger.json.gz",
        R303B_PREFIX + "_b2b_physical_inclusion_lemma_ledger.json.gz",
        R303B_PREFIX + "_component_edge_ledger.json.gz",
        R303B_PREFIX + "_wtail_unresolved_ledger.json.gz",
        R303B_RESULT,
        R303B_PREFIX + "_verifier.py",
        R303B_PREFIX + "_attack_suite.json",
        R303B_VERIFICATION,
        R303B_PREFIX + "_report.md",
        R303B_PREFIX + "_cold_replay.md",
    }
)
R304_EXPECTED_MEMBERS = frozenset(
    {
        R304_PREFIX + ".py",
        R304_PREFIX + "_edge_application_ledger.json.gz",
        R304_MEMBER_LEDGER,
        R304_PREFIX + "_wtail_disposition_ledger.json.gz",
        R304_PREFIX + "_residual_gate_ledger.json.gz",
        R304_RESULT,
        R304_PREFIX + "_promotion_verifier.py",
        R304_PREFIX + "_attack_suite.json",
        R304_VERIFICATION,
        R304_PREFIX + "_report.md",
        R304_PREFIX + "_cold_replay.md",
    }
)

R300A_ROW_FIELDS = frozenset(
    {
        "R295A_explicit_lower_graph_sheet_witness_present",
        "R295A_physical_incidence_binding_row_ids",
        "R295A_physical_incidence_binding_row_sha256s",
        "Round300A_canonical_occurrence_pair_row_id",
        "canonical_unordered_Round294_registry_occurrence_ids",
        "duplicate_source_expansion_count",
        "endpoint_specific_common_positive_area_zero_trace_proved",
        "exact_positive_open_support_intersection",
        "formal_DSU_rank_reduction_credit",
        "formal_component_edge_credit",
        "formal_maximality_credit",
        "formal_occurrence_identity_collapse_credit",
        "formal_seam_edge_credit",
        "frontier_disposition",
        "left_Round294_registry_occurrence_id",
        "opposite_strict_side_exclusion_proved",
        "parent_regular_graph_zero_in_closure_is_not_itself_an_edge",
        "right_Round294_registry_occurrence_id",
        "row_sha256",
        "self_pair",
        "source_Round287_pair_row_ids",
        "source_expansion_provenance_count",
    }
)
R304_MEMBER_ROW_FIELDS = frozenset(
    {
        "Round304_fresh_member_component_row_id",
        "base_root_id",
        "final_component_id",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_maximality_credit",
        "member_identity_preserved",
        "official_key_id",
        "registry_occurrence_id",
        "row_sha256",
        "schema",
    }
)
ROW_FIELDS = frozenset(
    {
        ROW_ID,
        "schema",
        "source_Round300A_row_id",
        "source_Round300A_row_sha256",
        "canonical_Round294_registry_occurrence_pair",
        "left_Round294_registry_occurrence_id",
        "right_Round294_registry_occurrence_id",
        "left_Round304_member_row_id",
        "left_Round304_member_row_sha256",
        "right_Round304_member_row_id",
        "right_Round304_member_row_sha256",
        "left_base_root_id",
        "right_base_root_id",
        "projected_base_root_pair",
        "left_final_component_id",
        "right_final_component_id",
        "final_component_pair",
        "prior_R295A_witness_present",
        "same_Round304_final_component",
        "post_Round304_disposition",
        "requires_formal_physical_inclusion",
        "source_row_fed_to_DSU",
        "unsealed_temp_scope_consumed",
        "formal_physical_inclusion_credit",
        "formal_component_edge_credit",
        "formal_DSU_rank_reduction_credit",
        "formal_maximality_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_Jx_Jy_same_point_glue_credit",
        "row_sha256",
    }
)
LEDGER_FIELDS = frozenset(
    {
        "schema",
        "status",
        "row_count",
        "row_ids_sha256",
        "row_hashes_sha256",
        "rows_sha256",
        "legacy_Round304_classification_rows_sha256",
        "classification_histogram",
        "complete_pair_count",
        "complete_sorted_occurrence_pairs_sha256",
        "complete_endpoint_count",
        "complete_sorted_occurrence_endpoints_sha256",
        "prior_R295A_witnessed_pair_count",
        "prior_R295A_witnessed_sorted_occurrence_pairs_sha256",
        "Round304_mapped_frontier_endpoint_count",
        "Round304_expected_frontier_endpoint_count",
        "residual_source_Round300A_row_count",
        "residual_source_Round300A_row_ids_sha256",
        "residual_source_Round300A_row_hashes_sha256",
        "residual_sorted_source_Round300A_id_hash_pairs_sha256",
        "residual_pair_count",
        "residual_sorted_occurrence_pairs_sha256",
        "residual_endpoint_count",
        "residual_sorted_occurrence_endpoints_sha256",
        "residual_sorted_projected_base_root_pairs_sha256",
        "residual_sorted_final_component_pairs_sha256",
        "residual_endpoint_degree_histogram",
        TABLE,
        "ledger_sha256",
    }
)
RESULT_FIELDS = frozenset(
    {
        "schema",
        "status",
        "producer_file_sha256",
        "schema_snapshot_sha256",
        "seed_affects_output",
        "upstream_seals",
        "lineage_only_seals",
        "reprojection_census",
        "residual_scope_commitments",
        "formal_credit_transition",
        "strict_boundary",
        "atomicity_contract",
        "output_ledger",
        "result_sha256",
    }
)

R300A_VERIFICATION_STATUS = (
    "PASS_INDEPENDENT_CACHELESS_ROUND300A_FAIL_CLOSED_FRONTIER_EXHAUSTION__"
    "3488_TO_6292_TO_3232__128_PRIOR_WITNESSED__3104_UNRESOLVED__"
    "ZERO_COMPONENT_EDGE_CREDIT"
)
R304_RESULT_STATUS = (
    "PASS_ROUND304_FRESH_EXTENDED_REGISTRY_LEGAL_DSU__"
    "275268_RANK_REDUCTIONS__92696_COMPONENTS__"
    "ZERO_MAXIMALITY_FIBRE_GLOBAL_DISPOSITION_CREDIT"
)
R300A_RESULT_STATUS = (
    "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
    "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION"
)
R304_VERIFICATION_STATUS = "PASS_EXACT_CACHELESS_EXPECTED_STATE"
R303B_VERIFICATION_STATUS = "PASS_EXACT_CACHELESS_EXPECTED_STATE"

ENCODER = json.JSONEncoder(
    ensure_ascii=True,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
)
PIN = re.compile(r"^[0-9a-f]{64}$")
FileIdentity = tuple[int, int, int, int, int, int, int]
DirectoryIdentity = tuple[int, int, int]
INPUT_SNAPSHOTS: dict[Path, FileIdentity] = {}
PARENT_DIRECTORY_SNAPSHOTS: dict[Path, DirectoryIdentity] = {}
ROOT = Path(os.path.abspath(os.fspath(Path(__file__).parent.parent)))
DATA = ROOT / "deliverables"


class PromotionBlocked(RuntimeError):
    """Raised for every fail-closed admission or publication failure."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PromotionBlocked(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


SCHEMA_SNAPSHOT = {
    "row_schema": ROW_SCHEMA,
    "ledger_schema": LEDGER_SCHEMA,
    "result_schema": RESULT_SCHEMA,
    "table": TABLE,
    "row_fields": sorted(ROW_FIELDS),
    "ledger_fields": sorted(LEDGER_FIELDS),
    "result_fields": sorted(RESULT_FIELDS),
}
SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)


def all_object_keys_are_strings(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            type(key) is str and all_object_keys_are_strings(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return all(all_object_keys_are_strings(item) for item in value)
    return True


def close_object(payload: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in payload, "preclosed object:" + field)
    need(all_object_keys_are_strings(payload), "non-string JSON object key")
    output = dict(payload)
    output[field] = digest(payload)
    return output


def check_self(document: dict[str, Any], field: str, label: str) -> None:
    payload = dict(document)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and PIN.fullmatch(claimed) is not None, label)
    need(claimed == digest(payload), "self hash:" + label)


def file_identity(info: os.stat_result) -> FileIdentity:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def directory_identity(info: os.stat_result) -> DirectoryIdentity:
    return (info.st_dev, info.st_ino, info.st_mode)


def lexical_directory_without_symlinks(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        need(os.path.lexists(current), label + " missing component")
        info = os.lstat(current)
        need(
            not stat.S_ISLNK(info.st_mode) and stat.S_ISDIR(info.st_mode),
            label + " symlink/non-directory component:" + part,
        )
    return absolute


def configure_root(root: Path) -> None:
    global ROOT, DATA
    lexical = lexical_directory_without_symlinks(root, "workspace root")
    need(lexical == root.resolve(), "workspace root resolution")
    deliverables = lexical_directory_without_symlinks(
        lexical / "deliverables", "workspace deliverables"
    )
    need(deliverables == (lexical / "deliverables").resolve(), "deliverables")
    ROOT, DATA = lexical, deliverables
    INPUT_SNAPSHOTS.clear()
    PARENT_DIRECTORY_SNAPSHOTS.clear()


def open_bound_directory(directory: Path, label: str) -> tuple[Path, int]:
    lexical = lexical_directory_without_symlinks(directory, label + " parent")
    descriptor = os.open(
        lexical,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    actual = directory_identity(os.fstat(descriptor))
    need(actual == directory_identity(os.lstat(lexical)), label + " parent race")
    prior = PARENT_DIRECTORY_SNAPSHOTS.setdefault(lexical, actual)
    need(prior == actual, label + " parent PRE/POST mismatch")
    return lexical, descriptor


def safe_regular_at(
    name: str,
    directory: Path,
    descriptor: int,
    snapshots: dict[Path, FileIdentity],
    maximum: int,
    label: str,
) -> FileIdentity:
    need(name not in {"", ".", ".."} and Path(name).name == name, label)
    info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        label + " nonregular/hardlink/unbounded",
    )
    identity = file_identity(info)
    path = directory / name
    need(snapshots.setdefault(path, identity) == identity, label + " drift")
    return identity


@contextmanager
def fd_bound_binary(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 4_000_000_000,
    label: str,
) -> Iterator[BinaryIO]:
    lexical, directory_descriptor = open_bound_directory(directory, label)
    stream: BinaryIO | None = None
    raw_descriptor: int | None = None
    try:
        absolute = Path(os.path.abspath(os.fspath(path)))
        need(absolute.parent == lexical, label + " path escape")
        expected = safe_regular_at(
            absolute.name,
            lexical,
            directory_descriptor,
            snapshots,
            maximum,
            label,
        )
        raw_descriptor = os.open(
            absolute.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=directory_descriptor,
        )
        stream = os.fdopen(raw_descriptor, "rb", closefd=True)
        raw_descriptor = None
        need(file_identity(os.fstat(stream.fileno())) == expected, label + " open race")
        yield stream
        need(file_identity(os.fstat(stream.fileno())) == expected, label + " fd drift")
        need(
            file_identity(
                os.stat(
                    absolute.name,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
            )
            == expected,
            label + " filename swap",
        )
    finally:
        if stream is not None:
            stream.close()
        elif raw_descriptor is not None:
            os.close(raw_descriptor)
        os.close(directory_descriptor)


def assert_snapshot_map(
    snapshots: dict[Path, FileIdentity], label: str
) -> None:
    for path, expected in sorted(snapshots.items(), key=lambda item: str(item[0])):
        need(os.path.lexists(path) and not path.is_symlink(), label + " disappeared")
        need(file_identity(os.lstat(path)) == expected, label + " drift:" + path.name)
    for directory, expected in sorted(
        PARENT_DIRECTORY_SNAPSHOTS.items(), key=lambda item: str(item[0])
    ):
        lexical = lexical_directory_without_symlinks(directory, label + " parent")
        need(directory_identity(os.lstat(lexical)) == expected, label + " parent swap")


def assert_inputs_unchanged() -> None:
    assert_snapshot_map(INPUT_SNAPSHOTS, "input PRE/POST")


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        label="input hash:" + path.name,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read_bytes(path: Path, maximum: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    with fd_bound_binary(
        path,
        DATA,
        INPUT_SNAPSHOTS,
        maximum=maximum,
        label="input read:" + path.name,
    ) as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "bounded input read:" + path.name)
            chunks.append(block)
    return b"".join(chunks)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise PromotionBlocked("nonintegral/nonfinite JSON:" + label + ":" + token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, "top-level object:" + label)
    return value


def read_canonical_json(
    name: str,
    maximum: int = 100_000_000,
    *,
    allow_single_terminal_lf: bool = False,
) -> dict[str, Any]:
    raw = stable_read_bytes(DATA / name, maximum)
    document = strict_object(raw, name)
    expected = canonical(document) + (b"\n" if allow_single_terminal_lf else b"")
    need(raw == expected, "noncanonical JSON framing:" + name)
    return document


def parse_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    path = DATA / name
    need(file_sha256(path) == expected_sha256, "manifest file pin:" + name)
    raw = stable_read_bytes(path, 500_000)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        value, member = match.groups()
        need(Path(member).name == member and member not in entries, "manifest set")
        entries[member] = value
    need(bool(entries) and name not in entries, "manifest empty/self member")
    return entries


def validate_entire_manifest(
    name: str,
    expected_sha256: str,
    expected_members: frozenset[str],
) -> dict[str, str]:
    entries = parse_manifest(name, expected_sha256)
    need(set(entries) == set(expected_members), "exact manifest member set:" + name)
    for member, expected in sorted(entries.items()):
        need(file_sha256(DATA / member) == expected, "manifest member pin:" + member)
    return entries


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(stream: TextIO, marker: str) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array:" + marker)
        buffer = (buffer + block)[-max(len(marker), len(buffer) + len(block)) :]
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "stream duplicate JSON key:" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise PromotionBlocked("nonintegral/nonfinite streamed JSON:" + token)

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            buffer = stream.read(1 << 20)
            need(bool(buffer), "truncated streamed array")
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "streamed row object")
        yield row
        buffer = buffer[end:]


def validated_gzip_rows(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
    exact_fields: frozenset[str],
    row_schema: str | None,
) -> Iterator[dict[str, Any]]:
    rows, ids, hashes = ListHash(), ListHash(), ListHash()
    with fd_bound_binary(
        DATA / name,
        DATA,
        INPUT_SNAPSHOTS,
        label="gzip ledger:" + name,
    ) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as binary:
            with io.TextIOWrapper(binary, encoding="utf-8", newline="") as stream:
                for row in iter_array(stream, '"' + table + '":['):
                    need(set(row) == set(exact_fields), "exact upstream row fields:" + name)
                    if row_schema is not None:
                        need(row.get("schema") == row_schema, "upstream row schema:" + name)
                    check_self(row, "row_sha256", name)
                    row_id = row.get(id_field)
                    need(type(row_id) is str, "upstream row id:" + name)
                    rows.add(row)
                    ids.add(row_id)
                    hashes.add(row["row_sha256"])
                    yield row
    actual = {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }
    need(actual == expected, "upstream ledger commitments:" + name)


def validate_admission() -> dict[str, Any]:
    r300a = validate_entire_manifest(
        R300A_MANIFEST, R300A_MANIFEST_SHA256, R300A_EXPECTED_MEMBERS
    )
    need(
        r300a[R300A_LEDGER] == R300A_LEDGER_FILE_SHA256
        and r300a[R300A_RESULT] == R300A_RESULT_FILE_SHA256
        and r300a[R300A_VERIFICATION] == R300A_VERIFICATION_FILE_SHA256,
        "Round300A critical manifest members",
    )
    r300a_result = read_canonical_json(
        R300A_RESULT, allow_single_terminal_lf=True
    )
    r300a_verification = read_canonical_json(
        R300A_VERIFICATION, allow_single_terminal_lf=True
    )
    check_self(r300a_result, "result_sha256", R300A_RESULT)
    check_self(r300a_verification, "verification_sha256", R300A_VERIFICATION)
    need(
        r300a_result["result_sha256"] == R300A_RESULT_OBJECT_SHA256
        and r300a_result.get("status") == R300A_RESULT_STATUS
        and r300a_result.get("frontier_ledger", {}).get(
            "canonical_occurrence_pair_row_count"
        )
        == 3_232
        and r300a_result.get("prior_witness_partition", {}).get(
            "R295A_explicit_lower_graph_sheet_witness_pair_count"
        )
        == 128
        and r300a_result.get("prior_witness_partition", {}).get(
            "unresolved_exact_pair_count"
        )
        == 3_104
        and r300a_verification["verification_sha256"]
        == R300A_VERIFICATION_OBJECT_SHA256
        and r300a_verification.get("status") == R300A_VERIFICATION_STATUS,
        "Round300A critical semantic seal",
    )

    r303b = validate_entire_manifest(
        R303B_MANIFEST, R303B_MANIFEST_SHA256, R303B_EXPECTED_MEMBERS
    )
    need(
        r303b[R303B_RESULT] == R303B_RESULT_FILE_SHA256
        and r303b[R303B_VERIFICATION] == R303B_VERIFICATION_FILE_SHA256,
        "Round303B critical lineage members",
    )
    r303b_result = read_canonical_json(
        R303B_RESULT, allow_single_terminal_lf=True
    )
    r303b_verification = read_canonical_json(
        R303B_VERIFICATION, allow_single_terminal_lf=True
    )
    check_self(r303b_result, "result_sha256", R303B_RESULT)
    check_self(r303b_verification, "verification_sha256", R303B_VERIFICATION)
    need(
        r303b_result["result_sha256"] == R303B_RESULT_OBJECT_SHA256
        and r303b_verification["verification_sha256"]
        == R303B_VERIFICATION_OBJECT_SHA256
        and r303b_verification.get("status") == R303B_VERIFICATION_STATUS,
        "Round303B critical lineage seal",
    )

    r304 = validate_entire_manifest(
        R304_MANIFEST, R304_MANIFEST_SHA256, R304_EXPECTED_MEMBERS
    )
    need(
        r304[R304_MEMBER_LEDGER] == R304_MEMBER_LEDGER_FILE_SHA256
        and r304[R304_RESULT] == R304_RESULT_FILE_SHA256
        and r304[R304_VERIFICATION] == R304_VERIFICATION_FILE_SHA256,
        "Round304 critical manifest members",
    )
    r304_result = read_canonical_json(R304_RESULT)
    r304_verification = read_canonical_json(R304_VERIFICATION)
    check_self(r304_result, "result_sha256", R304_RESULT)
    check_self(r304_verification, "verification_sha256", R304_VERIFICATION)
    maximality = r304_result.get("maximality_gate", {})
    output_member = r304_result.get("output_ledgers", {}).get("member", {})
    need(
        r304_result["result_sha256"] == R304_RESULT_OBJECT_SHA256
        and r304_result.get("status") == R304_RESULT_STATUS
        and r304_result.get("member_universe", {}).get("member_count") == 564_492
        and r304_result.get("member_universe", {}).get("base_root_count") == 367_964
        and r304_result.get("forward_application", {}).get("component_count")
        == 92_696
        and r304_result.get("forward_application", {}).get("partition_sha256")
        == "72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff"
        and maximality.get("complete_Round300A_pair_count") == 3_232
        and maximality.get("complete_reprojection_rows_sha256")
        == LEGACY_REPROJECTION_SHA256
        and maximality.get("cross_component_unwitnessed_pair_count") == 1_024
        and maximality.get("formal_maximality_credit") == 0
        and output_member.get("file_sha256") == R304_MEMBER_LEDGER_FILE_SHA256
        and {key: output_member.get(key) for key in R304_MEMBER_COMMITMENT}
        == R304_MEMBER_COMMITMENT
        and r304_verification["verification_sha256"]
        == R304_VERIFICATION_OBJECT_SHA256
        and r304_verification.get("status") == R304_VERIFICATION_STATUS
        and r304_verification.get("formal_Round304_promotion_permitted") is True,
        "Round304 critical semantic seal",
    )
    return {
        "Round300A_manifest_member_count": len(r300a),
        "Round303B_manifest_member_count": len(r303b),
        "Round304_manifest_member_count": len(r304),
    }


def source_sha256() -> str:
    source = Path(os.path.abspath(os.fspath(Path(__file__))))
    need(source.name == FILES["producer"], "formal producer basename")
    need(source.parent == DATA, "formal producer must reside in deliverables")
    state = hashlib.sha256()
    with fd_bound_binary(
        source,
        DATA,
        INPUT_SNAPSHOTS,
        maximum=5_000_000,
        label="producer source",
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def build_projection_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows: list[dict[str, Any]] = []
    target_occurrences: set[str] = set()
    prior_row_id: str | None = None
    for row in validated_gzip_rows(
        R300A_LEDGER,
        "canonical_occurrence_pair_rows",
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_PAIR_COMMITMENT,
        R300A_ROW_FIELDS,
        None,
    ):
        row_id = row["Round300A_canonical_occurrence_pair_row_id"]
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        need(prior_row_id is None or prior_row_id < row_id, "Round300A row order")
        prior_row_id = row_id
        need(
            type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and row["left_Round294_registry_occurrence_id"] == pair[0]
            and row["right_Round294_registry_occurrence_id"] == pair[1]
            and row["self_pair"] is False
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_maximality_credit"] == 0,
            "Round300A pair boundary",
        )
        target_occurrences.update(pair)
        source_rows.append(row)
    need(len(source_rows) == 3_232, "complete Round300A frontier")
    complete_pairs = sorted(
        row["canonical_unordered_Round294_registry_occurrence_ids"]
        for row in source_rows
    )
    complete_endpoints = sorted(target_occurrences)
    prior_witnessed_pairs = sorted(
        row["canonical_unordered_Round294_registry_occurrence_ids"]
        for row in source_rows
        if row["R295A_explicit_lower_graph_sheet_witness_present"]
    )
    need(
        len(complete_pairs) == 3_232
        and len(set(map(tuple, complete_pairs))) == 3_232
        and digest(complete_pairs) == COMPLETE_PAIR_SET_SHA256
        and len(complete_endpoints) == 4_892
        and digest(complete_endpoints) == COMPLETE_ENDPOINT_SET_SHA256
        and len(prior_witnessed_pairs) == 128
        and digest(prior_witnessed_pairs) == PRIOR_WITNESSED_PAIR_SET_SHA256,
        "complete/prior Round300A pair and endpoint sets",
    )

    members: dict[str, dict[str, Any]] = {}
    for row in validated_gzip_rows(
        R304_MEMBER_LEDGER,
        "fresh_member_component_rows",
        "Round304_fresh_member_component_row_id",
        R304_MEMBER_COMMITMENT,
        R304_MEMBER_ROW_FIELDS,
        "cm2.round304.fresh-member-component-row.v1",
    ):
        need(
            row["member_identity_preserved"] is True
            and row["formal_maximality_credit"] == 0
            and row["formal_fibre_credit"] == 0
            and row["formal_global_disposition_credit"] == 0,
            "Round304 member boundary",
        )
        occurrence = row["registry_occurrence_id"]
        if occurrence in target_occurrences:
            need(occurrence not in members, "duplicate targeted Round304 occurrence")
            members[occurrence] = row
    need(
        set(members) == target_occurrences and len(members) == 4_892,
        "Round304 coverage of all 4892 frontier endpoints",
    )

    output: list[dict[str, Any]] = []
    legacy: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    residual_rows: list[dict[str, Any]] = []
    zero_credit_fields = (
        "formal_physical_inclusion_credit",
        "formal_component_edge_credit",
        "formal_DSU_rank_reduction_credit",
        "formal_maximality_credit",
        "formal_fibre_credit",
        "formal_global_disposition_credit",
        "formal_Jx_Jy_same_point_glue_credit",
    )
    for source in source_rows:
        pair = source["canonical_unordered_Round294_registry_occurrence_ids"]
        left, right = members[pair[0]], members[pair[1]]
        roots = sorted([left["base_root_id"], right["base_root_id"]])
        components = sorted(
            [left["final_component_id"], right["final_component_id"]]
        )
        same = left["final_component_id"] == right["final_component_id"]
        witnessed = source["R295A_explicit_lower_graph_sheet_witness_present"]
        need(type(witnessed) is bool, "Round300A witness flag")
        disposition = (
            "PRIOR_R295A_WITNESSED__SAME_FINAL_COMPONENT"
            if witnessed and same
            else (
                "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY"
                if witnessed
                else (
                    "UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH"
                    if same
                    else (
                        "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
                        "INCLUSION_PACKAGE_REQUIRED"
                    )
                )
            )
        )
        legacy_row = {
            "source_Round300A_row_id": source[
                "Round300A_canonical_occurrence_pair_row_id"
            ],
            "source_Round300A_row_sha256": source["row_sha256"],
            "canonical_occurrence_pair": pair,
            "projected_base_root_pair": roots,
            "final_component_pair": components,
            "prior_R295A_witness_present": witnessed,
            "same_final_component": same,
            "post_Round304_disposition": disposition,
        }
        legacy.append(legacy_row)
        histogram[disposition] += 1
        payload = {
            "schema": ROW_SCHEMA,
            "source_Round300A_row_id": legacy_row["source_Round300A_row_id"],
            "source_Round300A_row_sha256": source["row_sha256"],
            "canonical_Round294_registry_occurrence_pair": pair,
            "left_Round294_registry_occurrence_id": pair[0],
            "right_Round294_registry_occurrence_id": pair[1],
            "left_Round304_member_row_id": left[
                "Round304_fresh_member_component_row_id"
            ],
            "left_Round304_member_row_sha256": left["row_sha256"],
            "right_Round304_member_row_id": right[
                "Round304_fresh_member_component_row_id"
            ],
            "right_Round304_member_row_sha256": right["row_sha256"],
            "left_base_root_id": left["base_root_id"],
            "right_base_root_id": right["base_root_id"],
            "projected_base_root_pair": roots,
            "left_final_component_id": left["final_component_id"],
            "right_final_component_id": right["final_component_id"],
            "final_component_pair": components,
            "prior_R295A_witness_present": witnessed,
            "same_Round304_final_component": same,
            "post_Round304_disposition": disposition,
            "requires_formal_physical_inclusion": (
                disposition
                == (
                    "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_"
                    "INCLUSION_PACKAGE_REQUIRED"
                )
            ),
            "source_row_fed_to_DSU": False,
            "unsealed_temp_scope_consumed": False,
            **{field: 0 for field in zero_credit_fields},
        }
        row_id = "round305a-scope-reprojection:" + digest(
            [
                "ROUND305A_SCOPE_REPROJECTION_V1",
                payload["source_Round300A_row_id"],
                payload["source_Round300A_row_sha256"],
                payload,
            ]
        )
        row = close_object({ROW_ID: row_id, **payload}, "row_sha256")
        need(set(row) == set(ROW_FIELDS), "exact Round305A row fields")
        check_self(row, "row_sha256", "generated Round305A row")
        need(all(row[field] == 0 for field in zero_credit_fields), "zero credit row")
        output.append(row)
        if row["requires_formal_physical_inclusion"]:
            residual_rows.append(row)

    expected_histogram = {
        "PRIOR_R295A_WITNESSED__SAME_FINAL_COMPONENT": 128,
        "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_INCLUSION_PACKAGE_REQUIRED":
            1_024,
        "UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH": 2_080,
    }
    need(dict(sorted(histogram.items())) == expected_histogram, "exact classification")
    need(digest(legacy) == LEGACY_REPROJECTION_SHA256, "legacy R304 replay hash")
    need(len(output) == 3_232 and len(residual_rows) == 1_024, "projection census")

    residual_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"] for row in residual_rows
    )
    residual_endpoints = sorted({item for pair in residual_pairs for item in pair})
    degree = Counter(item for pair in residual_pairs for item in pair)
    residual_roots = sorted(row["projected_base_root_pair"] for row in residual_rows)
    residual_components = sorted(row["final_component_pair"] for row in residual_rows)
    residual_ids = [row["source_Round300A_row_id"] for row in residual_rows]
    residual_hashes = [
        row["source_Round300A_row_sha256"] for row in residual_rows
    ]
    residual_id_hash_pairs = sorted(
        [row["source_Round300A_row_id"], row["source_Round300A_row_sha256"]]
        for row in residual_rows
    )
    need(
        len(residual_pairs) == 1_024
        and len(set(map(tuple, residual_pairs))) == 1_024
        and digest(residual_pairs) == RESIDUAL_PAIR_SET_SHA256
        and len(residual_endpoints) == 2_048
        and digest(residual_endpoints) == RESIDUAL_ENDPOINT_SET_SHA256
        and Counter(degree.values()) == {1: 2_048}
        and digest(residual_ids) == RESIDUAL_SOURCE_ROW_IDS_SHA256
        and digest(residual_hashes) == RESIDUAL_SOURCE_ROW_HASHES_SHA256,
        "exact residual pair/endpoint set",
    )
    commitments = {
        "legacy_Round304_classification_rows_sha256": digest(legacy),
        "classification_histogram": expected_histogram,
        "complete_pair_count": len(complete_pairs),
        "complete_sorted_occurrence_pairs_sha256": digest(complete_pairs),
        "complete_endpoint_count": len(complete_endpoints),
        "complete_sorted_occurrence_endpoints_sha256": digest(
            complete_endpoints
        ),
        "prior_R295A_witnessed_pair_count": len(prior_witnessed_pairs),
        "prior_R295A_witnessed_sorted_occurrence_pairs_sha256": digest(
            prior_witnessed_pairs
        ),
        "Round304_mapped_frontier_endpoint_count": len(members),
        "Round304_expected_frontier_endpoint_count": 4_892,
        "residual_source_Round300A_row_count": len(residual_rows),
        "residual_source_Round300A_row_ids_sha256": digest(residual_ids),
        "residual_source_Round300A_row_hashes_sha256": digest(
            residual_hashes
        ),
        "residual_sorted_source_Round300A_id_hash_pairs_sha256": digest(
            residual_id_hash_pairs
        ),
        "residual_pair_count": len(residual_pairs),
        "residual_sorted_occurrence_pairs_sha256": digest(residual_pairs),
        "residual_endpoint_count": len(residual_endpoints),
        "residual_sorted_occurrence_endpoints_sha256": digest(residual_endpoints),
        "residual_sorted_projected_base_root_pairs_sha256": digest(residual_roots),
        "residual_sorted_final_component_pairs_sha256": digest(
            residual_components
        ),
        "residual_endpoint_degree_histogram": {"1": 2_048},
    }
    return output, commitments


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    raw = canonical(document)
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=output, mtime=0, compresslevel=9
    ) as stream:
        stream.write(raw)
    return output.getvalue()


def build_artifacts(seed: int) -> tuple[dict[str, bytes], dict[str, Any]]:
    need(type(seed) is int and 0 <= seed < 2**63, "seed contract")
    producer_sha = source_sha256()
    admission = validate_admission()
    rows, commitments = build_projection_rows()
    row_ids = [row[ROW_ID] for row in rows]
    row_hashes = [row["row_sha256"] for row in rows]
    ledger_payload = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "PASS_EXACT_3232_POST_ROUND304_REPROJECTION__"
            "1024_RESIDUAL_SCOPE__ZERO_DOWNSTREAM_CREDIT"
        ),
        "row_count": len(rows),
        "row_ids_sha256": digest(row_ids),
        "row_hashes_sha256": digest(row_hashes),
        "rows_sha256": digest(rows),
        **commitments,
        TABLE: rows,
    }
    ledger = close_object(ledger_payload, "ledger_sha256")
    need(set(ledger) == set(LEDGER_FIELDS), "exact Round305A ledger fields")
    ledger_object_sha = digest(ledger)
    ledger_raw = canonical(ledger)
    replayed_ledger = strict_object(ledger_raw, "generated ledger")
    need(canonical(replayed_ledger) == ledger_raw, "ledger parse-canonical replay")
    check_self(replayed_ledger, "ledger_sha256", "generated ledger")
    ledger_bytes = deterministic_gzip(ledger)
    ledger_file_sha = hashlib.sha256(ledger_bytes).hexdigest()

    output_metadata = {
        "filename": FILES["ledger"],
        "schema": LEDGER_SCHEMA,
        "ledger_self_sha256": ledger["ledger_sha256"],
        "ledger_object_sha256": ledger_object_sha,
        "ledger_file_sha256": ledger_file_sha,
        "row_count": len(rows),
        "row_ids_sha256": ledger["row_ids_sha256"],
        "row_hashes_sha256": ledger["row_hashes_sha256"],
        "rows_sha256": ledger["rows_sha256"],
    }
    result_payload = {
        "schema": RESULT_SCHEMA,
        "status": (
            "PASS_ROUND305A_EXACT_R300A_POST_R304_RESIDUAL_SCOPE_"
            "REPROJECTION__1024_RESIDUAL_PAIRS__ZERO_DOWNSTREAM_CREDIT"
        ),
        "producer_file_sha256": producer_sha,
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "seed_affects_output": False,
        "upstream_seals": {
            "Round300A": {
                "manifest_filename": R300A_MANIFEST,
                "manifest_file_sha256": R300A_MANIFEST_SHA256,
                "manifest_member_count": admission[
                    "Round300A_manifest_member_count"
                ],
                "ledger_filename": R300A_LEDGER,
                "ledger_file_sha256": R300A_LEDGER_FILE_SHA256,
                "result_filename": R300A_RESULT,
                "result_file_sha256": R300A_RESULT_FILE_SHA256,
                "result_object_sha256": R300A_RESULT_OBJECT_SHA256,
                "verification_filename": R300A_VERIFICATION,
                "verification_file_sha256": R300A_VERIFICATION_FILE_SHA256,
                "verification_object_sha256": R300A_VERIFICATION_OBJECT_SHA256,
                "complete_manifest_validated_before_ledger_consumption": True,
            },
            "Round304": {
                "manifest_filename": R304_MANIFEST,
                "manifest_file_sha256": R304_MANIFEST_SHA256,
                "manifest_member_count": admission[
                    "Round304_manifest_member_count"
                ],
                "member_ledger_filename": R304_MEMBER_LEDGER,
                "member_ledger_file_sha256": R304_MEMBER_LEDGER_FILE_SHA256,
                "member_ledger_row_count": R304_MEMBER_COMMITMENT["row_count"],
                "member_ledger_row_ids_sha256": R304_MEMBER_COMMITMENT[
                    "row_ids_sha256"
                ],
                "member_ledger_row_hashes_sha256": R304_MEMBER_COMMITMENT[
                    "row_hashes_sha256"
                ],
                "member_ledger_rows_sha256": R304_MEMBER_COMMITMENT[
                    "rows_sha256"
                ],
                "result_filename": R304_RESULT,
                "result_file_sha256": R304_RESULT_FILE_SHA256,
                "result_object_sha256": R304_RESULT_OBJECT_SHA256,
                "verification_filename": R304_VERIFICATION,
                "verification_file_sha256": R304_VERIFICATION_FILE_SHA256,
                "verification_object_sha256": R304_VERIFICATION_OBJECT_SHA256,
                "complete_manifest_validated_before_ledger_consumption": True,
            },
        },
        "lineage_only_seals": {
            "Round303B": {
                "manifest_filename": R303B_MANIFEST,
                "manifest_file_sha256": R303B_MANIFEST_SHA256,
                "manifest_member_count": admission[
                    "Round303B_manifest_member_count"
                ],
                "result_filename": R303B_RESULT,
                "result_file_sha256": R303B_RESULT_FILE_SHA256,
                "result_object_sha256": R303B_RESULT_OBJECT_SHA256,
                "verification_filename": R303B_VERIFICATION,
                "verification_file_sha256": R303B_VERIFICATION_FILE_SHA256,
                "verification_object_sha256": R303B_VERIFICATION_OBJECT_SHA256,
                "used_as_projection_input": False,
                "complete_manifest_validated": True,
            }
        },
        "reprojection_census": {
            "complete_Round300A_pair_count": 3_232,
            "prior_R295A_witnessed_same_component_count": 128,
            "unwitnessed_reclosed_by_other_legal_path_count": 2_080,
            "unwitnessed_cross_component_residual_count": 1_024,
            "prior_R295A_witnessed_cross_component_inconsistency_count": 0,
            "legacy_Round304_classification_rows_sha256":
                LEGACY_REPROJECTION_SHA256,
            "exact_Round304_classification_reproduced": True,
            "complete_pair_set_sha256": COMPLETE_PAIR_SET_SHA256,
            "complete_endpoint_count": 4_892,
            "complete_endpoint_set_sha256": COMPLETE_ENDPOINT_SET_SHA256,
            "prior_R295A_witnessed_pair_set_sha256":
                PRIOR_WITNESSED_PAIR_SET_SHA256,
            "Round304_mapped_frontier_endpoint_count": 4_892,
            "Round304_expected_frontier_endpoint_count": 4_892,
        },
        "residual_scope_commitments": commitments,
        "formal_credit_transition": {
            "formal_physical_inclusion_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
        },
        "strict_boundary": {
            "exact_residual_scope_reprojection_sealed": True,
            "unsealed_temp_scope_consumed": False,
            "temporary_file_or_directory_used_as_input": False,
            "Round303B_used_as_projection_input": False,
            "Round304_serialized_DSU_state_replayed": False,
            "Round304_member_component_ledger_used_only_as_sealed_projection_map":
                True,
            "physical_inclusion_package_present": False,
            "two_sided_gluing_theorem_present": False,
            "new_component_edges_issued": 0,
            "fresh_DSU_rebuild_performed": False,
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "atomicity_contract": {
            "input_PRE_POST_identity_equality_required_before_commit": True,
            "complete_batch_no_clobber_preflight_required": True,
            "staged_files_require_atomic_RENAME_NOREPLACE": True,
            "result_is_required_last_commit_marker": True,
            "explicit_root_confined_output_directory_required": True,
            "exact_private_stage_orphan_recovery_required_before_retry": True,
        },
        "output_ledger": output_metadata,
    }
    result = close_object(result_payload, "result_sha256")
    need(set(result) == set(RESULT_FIELDS), "exact Round305A result fields")
    result_bytes = canonical(result)
    replayed_result = strict_object(result_bytes, "generated result")
    need(canonical(replayed_result) == result_bytes, "result parse-canonical replay")
    check_self(replayed_result, "result_sha256", "generated result")
    assert_inputs_unchanged()
    need(source_sha256() == producer_sha, "producer source drift")
    return {
        FILES["ledger"]: ledger_bytes,
        FILES["result"]: result_bytes,
    }, result


def rename_noreplace(
    source_directory_descriptor: int,
    source_name: str,
    target_directory_descriptor: int,
    target_name: str,
) -> None:
    function = getattr(ctypes.CDLL(None, use_errno=True), "renameat2", None)
    need(function is not None, "renameat2(RENAME_NOREPLACE) unavailable")
    function.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    outcome = function(
        source_directory_descriptor,
        os.fsencode(source_name),
        target_directory_descriptor,
        os.fsencode(target_name),
        1,
    )
    if outcome == 0:
        return
    error = ctypes.get_errno()
    if error == errno.EEXIST:
        raise FileExistsError(error, os.strerror(error), target_name)
    raise OSError(error, os.strerror(error), target_name)


def resolve_output_directory(output_dir: Path) -> Path:
    lexical = lexical_directory_without_symlinks(output_dir, "output directory")
    need(lexical == output_dir.resolve(), "output directory symlink/dot escape")
    need(
        lexical == DATA or ROOT in lexical.parents,
        "output directory outside workspace",
    )
    need(lexical != ROOT, "workspace root cannot be output directory")
    return lexical


def read_local_exact(
    directory: Path,
    name: str,
    expected: bytes,
    snapshots: dict[Path, FileIdentity],
    label: str,
) -> bytes:
    with fd_bound_binary(
        directory / name,
        directory,
        snapshots,
        maximum=max(1, len(expected)),
        label=label,
    ) as stream:
        raw = stream.read()
    need(raw == expected, label + " exact bytes")
    return raw


def recover_private_stages(
    output_dir: Path,
    output_descriptor: int,
    artifacts: dict[str, bytes],
) -> None:
    for stage_name in sorted(os.listdir(output_descriptor)):
        if not stage_name.startswith(".r305a-stage-"):
            continue
        info = os.stat(
            stage_name, dir_fd=output_descriptor, follow_symlinks=False
        )
        need(
            stat.S_ISDIR(info.st_mode)
            and info.st_uid == os.geteuid()
            and stat.S_IMODE(info.st_mode) == 0o700,
            "private recovery stage boundary",
        )
        stage_descriptor = os.open(
            stage_name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=output_descriptor,
        )
        try:
            need(
                directory_identity(os.fstat(stage_descriptor))
                == directory_identity(info),
                "private recovery stage race",
            )
            names = set(os.listdir(stage_descriptor))
            need(names <= set(artifacts), "private recovery stage exact subset")
            for name in sorted(names):
                staged = os.stat(
                    name, dir_fd=stage_descriptor, follow_symlinks=False
                )
                need(
                    stat.S_ISREG(staged.st_mode)
                    and staged.st_uid == os.geteuid()
                    and staged.st_nlink == 1
                    and staged.st_size == len(artifacts[name]),
                    "private recovery file boundary",
                )
                descriptor = os.open(
                    name,
                    os.O_RDONLY
                    | getattr(os, "O_NOFOLLOW", 0)
                    | getattr(os, "O_CLOEXEC", 0),
                    dir_fd=stage_descriptor,
                )
                try:
                    chunks: list[bytes] = []
                    while True:
                        block = os.read(descriptor, 1 << 20)
                        if not block:
                            break
                        chunks.append(block)
                    need(
                        b"".join(chunks) == artifacts[name],
                        "private recovery exact bytes",
                    )
                finally:
                    os.close(descriptor)
                os.unlink(name, dir_fd=stage_descriptor)
            os.fsync(stage_descriptor)
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_descriptor)
    os.fsync(output_descriptor)


def publish_atomic_batch(output_dir: Path, artifacts: dict[str, bytes]) -> None:
    resolved = resolve_output_directory(output_dir)
    need(set(artifacts) == {FILES["ledger"], FILES["result"]}, "artifact set")
    descriptor = os.open(
        resolved,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    bound = directory_identity(os.fstat(descriptor))
    need(bound == directory_identity(os.lstat(resolved)), "output open race")
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        recover_private_stages(resolved, descriptor, artifacts)
        _publish_atomic_batch_locked(resolved, descriptor, artifacts)
    finally:
        need(
            bound
            == directory_identity(os.fstat(descriptor))
            == directory_identity(os.lstat(resolved)),
            "output directory swap",
        )
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _publish_atomic_batch_locked(
    output_dir: Path,
    output_descriptor: int,
    artifacts: dict[str, bytes],
) -> None:
    ordered = [FILES["ledger"], FILES["result"]]
    output_snapshots: dict[Path, FileIdentity] = {}
    preexisting: set[str] = set()
    for name in ordered:
        if os.path.lexists(output_dir / name):
            read_local_exact(
                output_dir,
                name,
                artifacts[name],
                output_snapshots,
                "preexisting output:" + name,
            )
            preexisting.add(name)
    need(
        FILES["result"] not in preexisting or preexisting == set(ordered),
        "result cannot preexist with partial batch",
    )
    with tempfile.TemporaryDirectory(
        prefix=".r305a-stage-", dir=output_dir
    ) as raw_stage:
        stage = Path(raw_stage)
        for name in ordered:
            descriptor = os.open(stage / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(artifacts[name])
                stream.flush()
                os.fsync(stream.fileno())
        stage_descriptor = os.open(
            stage,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(stage_descriptor)
            for name in ordered:
                if name in preexisting:
                    read_local_exact(
                        output_dir,
                        name,
                        artifacts[name],
                        output_snapshots,
                        "stable preexisting output:" + name,
                    )
                    continue
                if name == FILES["result"]:
                    assert_inputs_unchanged()
                try:
                    os.stat(name, dir_fd=output_descriptor, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise PromotionBlocked("target appeared after preflight:" + name)
                try:
                    rename_noreplace(stage_descriptor, name, output_descriptor, name)
                except FileExistsError as exc:
                    raise PromotionBlocked(
                        "target raced commit after preflight:" + name
                    ) from exc
            os.fsync(stage_descriptor)
            os.fsync(output_descriptor)
        finally:
            os.close(stage_descriptor)
    for name in ordered:
        read_local_exact(
            output_dir,
            name,
            artifacts[name],
            output_snapshots,
            "published output:" + name,
        )
    assert_snapshot_map(output_snapshots, "output PRE/POST")
    assert_inputs_unchanged()


def self_test() -> dict[str, Any]:
    sample = {"schema": "round305a-self-test", "value": 1}
    closed = close_object(sample, "sample_sha256")
    check_self(closed, "sample_sha256", "self test")
    integer_key_rejected = not all_object_keys_are_strings({"histogram": {2: 1}})
    return {
        "schema": "cm2.round305a.local-self-test.v1",
        "status": "PASS_LIGHTWEIGHT_LOCAL_SELF_TEST",
        "canonical_round_trip": strict_object(canonical(sample), "self test") == sample,
        "deterministic_single_member_gzip": (
            deterministic_gzip(sample) == deterministic_gzip(sample)
        ),
        "object_self_hash_closure": closed["sample_sha256"] == digest(sample),
        "non_string_object_key_rejected": integer_key_rejected,
        "frozen_dual_seeds": [SEED_A, SEED_B],
        "formal_artifact_written": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed", type=int, default=SEED_A)
    args = parser.parse_args()
    configure_root(args.root if args.root is not None else ROOT)
    if args.self_test:
        need(args.output_dir is None, "self-test cannot publish")
        print(canonical(self_test()).decode("ascii"))
        return
    if args.no_write:
        need(args.output_dir is None, "--no-write conflicts with --output-dir")
        _, result = build_artifacts(args.seed)
        print(canonical(result).decode("ascii"))
        return
    need(args.output_dir is not None, "formal write requires explicit --output-dir")
    artifacts, result = build_artifacts(args.seed)
    publish_atomic_batch(args.output_dir, artifacts)
    print(canonical(result).decode("ascii"))


if __name__ == "__main__":
    main()
