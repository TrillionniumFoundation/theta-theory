#!/usr/bin/env python3
"""Independent Round305A residual-scope reprojection promotion verifier.

The producer is treated as inert bytes only: it is never imported, executed,
parsed, or tokenized.  This verifier validates the complete sealed R300A,
R303B, and R304 admissions, independently reconstructs the 3,232-row scope
ledger and result before opening candidate output, runs coherently re-signed
attacks, and publishes attack-suite first and verification last.
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
import zlib
from collections import Counter
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, TextIO


class VerificationBlocked(RuntimeError):
    """Fail-closed Round305A verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationBlocked(label)


def discover_workspace_root(source: Path) -> Path:
    resolved = source.resolve()
    for ancestor in resolved.parents:
        deliverables = ancestor / "deliverables"
        sentinel = (
            deliverables
            / "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_manifest.sha256"
        )
        if (
            deliverables.is_dir()
            and not deliverables.is_symlink()
            and sentinel.is_file()
            and not sentinel.is_symlink()
        ):
            return ancestor
    raise RuntimeError("workspace root with sealed Round304 not found")


ROOT = discover_workspace_root(Path(__file__))
DATA = ROOT / "deliverables"
PIN = re.compile(r"^[0-9a-f]{64}$")
ENCODER = json.JSONEncoder(
    ensure_ascii=True,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
)
FileIdentity = tuple[int, int, int, int, int, int, int]
DirectoryIdentity = tuple[int, int, int]
SOURCE_SNAPSHOTS: dict[Path, FileIdentity] = {}
CANDIDATE_SNAPSHOTS: dict[Path, FileIdentity] = {}
PARENT_DIRECTORY_SNAPSHOTS: dict[Path, DirectoryIdentity] = {}

PREFIX = "cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection"
CANDIDATE_FILES = {
    "producer": PREFIX + ".py",
    "ledger": PREFIX + "_scope_reprojection_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
TABLE = "post_Round304_scope_reprojection_rows"
ROW_ID_FIELD = "Round305A_scope_reprojection_row_id"
ROW_SCHEMA = "cm2.round305a.r300a-post-r304-scope-reprojection-row.v1"
LEDGER_SCHEMA = (
    "cm2.round305a.r300a-post-r304-residual-scope-reprojection.ledger.v1"
)
RESULT_SCHEMA = (
    "cm2.round305a.source-g-r300a-post-r304-residual-scope-reprojection.v1"
)
ATTACK_SCHEMA = RESULT_SCHEMA + ".attack-suite.v1"
VERIFICATION_SCHEMA = RESULT_SCHEMA + ".independent-verification.v1"
VERIFIER_FILENAME = PREFIX + "_promotion_verifier.py"
ATTACK_FILENAME = PREFIX + "_attack_suite.json"
VERIFICATION_FILENAME = PREFIX + "_verification.json"

FINAL_PRODUCER_SHA256 = (
    "42e7cc1eeabaedee883a37b8de9301ee71d5ba068d2fb76fafc80b95061b6772"
)

R300A_PREFIX = "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
R300A_MANIFEST = R300A_PREFIX + "_manifest.sha256"
R300A_MANIFEST_SHA256 = (
    "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8"
)
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"
R300A_LEDGER_SHA256 = (
    "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d"
)
R300A_RESULT = R300A_PREFIX + "_result.json"
R300A_RESULT_FILE_SHA256 = (
    "b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4"
)
R300A_RESULT_OBJECT_SHA256 = (
    "dbba3aaa96a494144427709c7d908fc816c12cd9f87ff13ec06a818c832d7f98"
)
R300A_VERIFICATION = R300A_PREFIX + "_verification.json"
R300A_VERIFICATION_FILE_SHA256 = (
    "e976fc2912c1d902029b8c4c7d4864bd8bb1cb6895bc09c215f2a5ac2400c696"
)
R300A_VERIFICATION_OBJECT_SHA256 = (
    "fed82ab1403e0f496245066b469d686b3126a3588c27459d9b0b53f8b08e7495"
)
R300A_EXPECTED_MEMBERS = frozenset({
    R300A_PREFIX + ".py",
    R300A_PREFIX + "_verifier.py",
    R300A_LEDGER,
    R300A_RESULT,
    R300A_PREFIX + "_attack_suite.json",
    R300A_VERIFICATION,
    R300A_PREFIX + "_report.md",
    R300A_PREFIX + "_cold_replay.md",
})
R300A_COMMITMENT = {
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
R303B_MANIFEST_SHA256 = (
    "7d7293c488a05c8873a63b7d63d0bf125260c6b9d3c60595201896cfde0c9786"
)
R303B_RESULT = R303B_PREFIX + "_result.json"
R303B_RESULT_FILE_SHA256 = (
    "4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1"
)
R303B_RESULT_OBJECT_SHA256 = (
    "2ca258de5a58175164267bd3ca81b0da8b25a4ebffcd998805e8f7254d172fc2"
)
R303B_VERIFICATION = R303B_PREFIX + "_verification.json"
R303B_VERIFICATION_FILE_SHA256 = (
    "6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a"
)
R303B_VERIFICATION_OBJECT_SHA256 = (
    "a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57"
)
R303B_EXPECTED_MEMBERS = frozenset({
    "cm2_round303b_source_g_unified_attachment_edge_producer.py",
    R303B_PREFIX + "_component_edge_ledger.json.gz",
    R303B_PREFIX + "_wtail_unresolved_ledger.json.gz",
    R303B_PREFIX + "_b1_graph_attachment_lemma_ledger.json.gz",
    R303B_PREFIX + "_b2a_analytic_sheet_lemma_ledger.json.gz",
    R303B_PREFIX + "_b2b_physical_inclusion_lemma_ledger.json.gz",
    R303B_RESULT,
    R303B_PREFIX + "_verifier.py",
    R303B_PREFIX + "_attack_suite.json",
    R303B_VERIFICATION,
    R303B_PREFIX + "_report.md",
    R303B_PREFIX + "_cold_replay.md",
})

R304_PREFIX = "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild"
R304_MANIFEST = R304_PREFIX + "_manifest.sha256"
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)
R304_MEMBER_LEDGER = R304_PREFIX + "_member_component_ledger.json.gz"
R304_MEMBER_LEDGER_SHA256 = (
    "9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0"
)
R304_RESULT = R304_PREFIX + "_result.json"
R304_RESULT_FILE_SHA256 = (
    "2975a8cc61c1b7812fedff6bc9dffd4db8517e822311c54a09317403b3592f7d"
)
R304_RESULT_OBJECT_SHA256 = (
    "d9f0c8b573d8d3462091bb075711a4983219b8eb23a3ac5db91bc83e0ded5a0c"
)
R304_VERIFICATION = R304_PREFIX + "_verification.json"
R304_VERIFICATION_FILE_SHA256 = (
    "482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3"
)
R304_VERIFICATION_OBJECT_SHA256 = (
    "9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a"
)
R304_PARTITION_SHA256 = (
    "72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff"
)
R304_EXPECTED_MEMBERS = frozenset({
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
})
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

LEGACY_REPROJECTION_ROWS_SHA256 = (
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
RESIDUAL_PROJECTION_ROWS_SHA256 = (
    "d8b736196d1525c00d66f97031940c0264bf7dc96936abaa06f4e5b3d9bf96ff"
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

DISPOSITION_WITNESSED = "PRIOR_R295A_WITNESSED__SAME_FINAL_COMPONENT"
DISPOSITION_RECLOSED = "UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH"
DISPOSITION_RESIDUAL = (
    "UNWITNESSED__CROSS_COMPONENT__FORMAL_PHYSICAL_INCLUSION_PACKAGE_REQUIRED"
)
EXPECTED_HISTOGRAM = {
    DISPOSITION_WITNESSED: 128,
    DISPOSITION_RESIDUAL: 1_024,
    DISPOSITION_RECLOSED: 2_080,
}

EXACT_ROW_FIELDS = frozenset({
    ROW_ID_FIELD,
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
})
EXACT_LEDGER_FIELDS = frozenset({
    "schema",
    "status",
    "ledger_sha256",
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
})
EXACT_RESULT_FIELDS = frozenset({
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
})

DOWNSTREAM_CREDIT_FIELDS = (
    "formal_physical_inclusion_credit",
    "formal_component_edge_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
    "formal_Jx_Jy_same_point_glue_credit",
)

ATTACK_MECHANISMS = (
    "upstream_manifest_member_set",
    "upstream_result_or_verification_downgrade",
    "upstream_member_row_binding",
    "source_pair_provenance",
    "source_pair_order_or_identity",
    "prior_witness_flip",
    "Round304_member_row_provenance",
    "base_root_projection",
    "final_component_projection",
    "same_component_flag",
    "classification_disposition",
    "classification_census",
    "residual_pair_set_same_count_resign",
    "residual_endpoint_set_same_count_resign",
    "legacy_projection_commitment",
    "temporary_scope_consumption",
    "physical_inclusion_credit_nonzero",
    "component_edge_credit_nonzero",
    "DSU_credit_nonzero",
    "maximality_credit_nonzero",
    "fibre_credit_nonzero",
    "global_disposition_credit_nonzero",
    "Jx_Jy_credit_nonzero",
    "Gate5_or_D02_or_CM2_upgrade",
    "seed_dependent_output",
    "duplicate_JSON_key",
    "noncanonical_or_nonintegral_JSON",
    "gzip_member_or_integrity",
    "symlink_or_hardlink_input",
    "path_escape",
    "producer_import_exec_parse_tokenize",
    "temporary_runtime_dependency",
    "existing_target_clobber",
    "target_appears_after_preflight",
    "input_candidate_or_source_TOCTOU",
    "wrong_atomic_commit_order",
)
ATTACK_CATEGORY_BY_MECHANISM = {
    **{
        mechanism: "UPSTREAM" for mechanism in (
            "upstream_manifest_member_set",
            "upstream_result_or_verification_downgrade",
            "Round304_member_row_provenance",
        )
    },
    **{
        mechanism: "CREDIT" for mechanism in (
            "physical_inclusion_credit_nonzero",
            "component_edge_credit_nonzero",
            "DSU_credit_nonzero",
            "maximality_credit_nonzero",
            "fibre_credit_nonzero",
            "global_disposition_credit_nonzero",
            "Jx_Jy_credit_nonzero",
            "Gate5_or_D02_or_CM2_upgrade",
        )
    },
    **{
        mechanism: "WIRE_OS_AST" for mechanism in (
            "duplicate_JSON_key",
            "noncanonical_or_nonintegral_JSON",
            "gzip_member_or_integrity",
            "symlink_or_hardlink_input",
            "path_escape",
            "producer_import_exec_parse_tokenize",
            "temporary_runtime_dependency",
            "existing_target_clobber",
            "target_appears_after_preflight",
            "input_candidate_or_source_TOCTOU",
            "wrong_atomic_commit_order",
        )
    },
}
ATTACK_CATEGORY_BY_MECHANISM.update({
    mechanism: "CASCADE"
    for mechanism in ATTACK_MECHANISMS
    if mechanism not in ATTACK_CATEGORY_BY_MECHANISM
})
EXPECTED_ATTACK_CATEGORY_COUNTS = {
    "CASCADE": 14,
    "CREDIT": 8,
    "UPSTREAM": 3,
    "WIRE_OS_AST": 11,
}
EXPECTED_COHERENTLY_RESIGNED_FIXTURES = 25


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


SCHEMA_SNAPSHOT = {
    "row_schema": ROW_SCHEMA,
    "ledger_schema": LEDGER_SCHEMA,
    "result_schema": RESULT_SCHEMA,
    "table": TABLE,
    "row_fields": sorted(EXACT_ROW_FIELDS),
    "ledger_fields": sorted(EXACT_LEDGER_FIELDS),
    "result_fields": sorted(EXACT_RESULT_FIELDS),
}
SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)
FROZEN_SCHEMA_SNAPSHOT_SHA256 = (
    "19dd648b76f13ff02d161d4e5f3968c7e527f74887cb37c725c7a467912515f3"
)


def close_object(payload: dict[str, Any], field: str) -> dict[str, Any]:
    need(field not in payload, "preexisting closure field:" + field)
    return {**payload, field: digest(payload)}


def json_object_keys_are_strings(value: Any) -> bool:
    if isinstance(value, dict):
        return all(
            type(key) is str and json_object_keys_are_strings(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return all(json_object_keys_are_strings(item) for item in value)
    return True


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    raw = canonical(document)
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=output,
        compresslevel=9,
        mtime=0,
    ) as stream:
        stream.write(raw)
    return output.getvalue()


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
    resolved = root.resolve()
    need(lexical == resolved, "workspace root symlink/dot escape")
    deliverables = lexical_directory_without_symlinks(
        resolved / "deliverables",
        "workspace deliverables",
    )
    ROOT = resolved
    DATA = deliverables
    SOURCE_SNAPSHOTS.clear()
    CANDIDATE_SNAPSHOTS.clear()
    PARENT_DIRECTORY_SNAPSHOTS.clear()


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


def assert_parent_directory_snapshots(label: str) -> None:
    for directory, expected in sorted(
        PARENT_DIRECTORY_SNAPSHOTS.items(), key=lambda item: str(item[0])
    ):
        lexical = lexical_directory_without_symlinks(directory, label + " parent")
        need(
            directory_identity(os.lstat(lexical)) == expected,
            label + " parent renamed/swapped:" + directory.name,
        )


def safe_regular_at(
    name: str,
    directory: Path,
    directory_descriptor: int,
    snapshots: dict[Path, FileIdentity],
    maximum: int,
    label: str,
) -> FileIdentity:
    need(name not in {"", ".", ".."} and Path(name).name == name, label)
    info = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        label + " hardlink/nonregular/unbounded",
    )
    identity = file_identity(info)
    path = directory / name
    prior = snapshots.setdefault(path, identity)
    need(prior == identity, label + " PRE/POST mismatch")
    return identity


@contextmanager
def fd_bound_binary(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> Iterator[BinaryIO]:
    lexical, directory_descriptor = open_bound_directory(directory, label)
    descriptor: int | None = None
    stream: BinaryIO | None = None
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
        descriptor = os.open(
            absolute.name,
            os.O_RDONLY
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=directory_descriptor,
        )
        stream = os.fdopen(descriptor, "rb", closefd=True)
        descriptor = None
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
            label + " filename swapped",
        )
        need(
            directory_identity(os.fstat(directory_descriptor))
            == PARENT_DIRECTORY_SNAPSHOTS[lexical]
            == directory_identity(os.lstat(lexical)),
            label + " parent swapped",
        )
    finally:
        if stream is not None:
            stream.close()
        elif descriptor is not None:
            os.close(descriptor)
        os.close(directory_descriptor)


def stable_file_sha256(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> str:
    state = hashlib.sha256()
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=maximum,
        label=label,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read_bytes(
    path: Path,
    directory: Path,
    snapshots: dict[Path, FileIdentity],
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> bytes:
    chunks: list[bytes] = []
    total = 0
    with fd_bound_binary(
        path,
        directory,
        snapshots,
        maximum=maximum,
        label=label,
    ) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            total += len(block)
            need(total <= maximum, label + " bounded read")
            chunks.append(block)
    return b"".join(chunks)


def source_sha256(path: Path, maximum: int = 3_000_000_000) -> str:
    require_formal_runtime_input(path, "formal source hash")
    return stable_file_sha256(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        maximum=maximum,
        label="source hash:" + path.name,
    )


def require_formal_runtime_input(path: Path, label: str) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    forbidden_component = "." + "tmp"
    need(
        absolute.parent == DATA
        and forbidden_component not in absolute.parts,
        label + " must be a top-level sealed deliverable",
    )


def validate_inert_producer_access_plan(operations: tuple[str, ...]) -> None:
    need(
        operations == ("fd-bound-byte-read", "sha256"),
        "producer may only be read and hashed as inert bytes",
    )


def validate_promotion_commit_order(order: tuple[str, ...]) -> None:
    need(
        order == (ATTACK_FILENAME, VERIFICATION_FILENAME),
        "attack suite must commit before verification",
    )


def assert_snapshot_map(snapshots: dict[Path, FileIdentity], label: str) -> None:
    for path, expected in sorted(snapshots.items(), key=lambda item: str(item[0])):
        need(os.path.lexists(path) and not path.is_symlink(), label + " disappeared")
        need(file_identity(os.lstat(path)) == expected, label + " changed:" + path.name)
    assert_parent_directory_snapshots(label)


def strict_object(
    raw: bytes,
    label: str,
    *,
    allow_single_terminal_lf: bool = False,
) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise VerificationBlocked("nonintegral/nonfinite JSON:" + label + ":" + token)

    if allow_single_terminal_lf:
        need(
            raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
            "exact single terminal LF required:" + label,
        )
        parse_raw = raw[:-1]
    else:
        need(not raw.endswith(b"\n"), "unexpected terminal LF:" + label)
        parse_raw = raw
    value = json.loads(
        parse_raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, "top-level JSON object:" + label)
    need(canonical(value) == parse_raw, "noncanonical JSON bytes:" + label)
    return value


def verify_self(document: dict[str, Any], field: str, label: str) -> None:
    payload = dict(document)
    claimed = payload.pop(field, None)
    need(type(claimed) is str and claimed == digest(payload), "self hash:" + label)


def read_source_json(
    name: str,
    maximum: int = 50_000_000,
    *,
    allow_single_terminal_lf: bool = False,
) -> dict[str, Any]:
    require_formal_runtime_input(DATA / name, "source JSON:" + name)
    raw = stable_read_bytes(
        DATA / name,
        DATA,
        SOURCE_SNAPSHOTS,
        maximum=maximum,
        label="source JSON:" + name,
    )
    return strict_object(
        raw,
        name,
        allow_single_terminal_lf=allow_single_terminal_lf,
    )


class ListHash:
    def __init__(self) -> None:
        self._state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self._state.update(b",")
        self._state.update(canonical(value))
        self.count += 1

    def finish(self) -> str:
        state = self._state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(stream: TextIO, marker: str, initial: str = "") -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "stream duplicate key:" + key)
            output[key] = value
        return output

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            VerificationBlocked("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationBlocked("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated JSON array")
            buffer = block
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
                need(bool(block), "truncated JSON row")
                buffer += block
        need(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]


def stream_gzip_rows(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
) -> Iterator[dict[str, Any]]:
    rows, ids, hashes = ListHash(), ListHash(), ListHash()
    seen: set[str] = set()
    path = DATA / name
    require_formal_runtime_input(path, "gzip source:" + name)
    with fd_bound_binary(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        label="gzip source:" + name,
    ) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as binary:
            with io.TextIOWrapper(binary, encoding="utf-8", newline="") as stream:
                for row in iter_array(stream, '"' + table + '":['):
                    verify_self(row, "row_sha256", name)
                    row_id = row.get(id_field)
                    need(type(row_id) is str and row_id not in seen, "row id:" + name)
                    seen.add(row_id)
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
    need(actual == expected, "source ledger commitment:" + name)


def parse_manifest(name: str, expected_sha256: str) -> dict[str, str]:
    path = DATA / name
    require_formal_runtime_input(path, "sealed manifest:" + name)
    need(source_sha256(path, 500_000) == expected_sha256, "manifest file pin:" + name)
    raw = stable_read_bytes(
        path,
        DATA,
        SOURCE_SNAPSHOTS,
        maximum=500_000,
        label="manifest:" + name,
    )
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        pin, member = match.groups()
        need(Path(member).name == member and member not in entries, "manifest set:" + name)
        entries[member] = pin
    need(bool(entries), "empty manifest:" + name)
    return entries


def verify_entire_manifest(
    name: str,
    expected_sha256: str,
    expected_members: frozenset[str],
) -> dict[str, str]:
    entries = parse_manifest(name, expected_sha256)
    need(set(entries) == set(expected_members), "exact manifest member set:" + name)
    for member, pin in sorted(entries.items()):
        need(source_sha256(DATA / member) == pin, "manifest member pin:" + name + ":" + member)
    return entries


def validate_upstream_admission() -> dict[str, Any]:
    """Validate all three complete seals before opening either source ledger."""

    r300a_manifest = verify_entire_manifest(
        R300A_MANIFEST,
        R300A_MANIFEST_SHA256,
        R300A_EXPECTED_MEMBERS,
    )
    r303b_manifest = verify_entire_manifest(
        R303B_MANIFEST,
        R303B_MANIFEST_SHA256,
        R303B_EXPECTED_MEMBERS,
    )
    r304_manifest = verify_entire_manifest(
        R304_MANIFEST,
        R304_MANIFEST_SHA256,
        R304_EXPECTED_MEMBERS,
    )
    need(
        r300a_manifest[R300A_LEDGER] == R300A_LEDGER_SHA256
        and r300a_manifest[R300A_RESULT] == R300A_RESULT_FILE_SHA256
        and r300a_manifest[R300A_VERIFICATION]
        == R300A_VERIFICATION_FILE_SHA256,
        "Round300A exact manifest pins",
    )
    need(
        r303b_manifest[R303B_RESULT] == R303B_RESULT_FILE_SHA256
        and r303b_manifest[R303B_VERIFICATION]
        == R303B_VERIFICATION_FILE_SHA256,
        "Round303B exact manifest pins",
    )
    need(
        r304_manifest[R304_MEMBER_LEDGER] == R304_MEMBER_LEDGER_SHA256
        and r304_manifest[R304_RESULT] == R304_RESULT_FILE_SHA256
        and r304_manifest[R304_VERIFICATION]
        == R304_VERIFICATION_FILE_SHA256,
        "Round304 exact manifest pins",
    )

    r300a_result = read_source_json(
        R300A_RESULT, allow_single_terminal_lf=True
    )
    r300a_verification = read_source_json(
        R300A_VERIFICATION, allow_single_terminal_lf=True
    )
    verify_self(r300a_result, "result_sha256", R300A_RESULT)
    verify_self(r300a_verification, "verification_sha256", R300A_VERIFICATION)
    need(
        r300a_result["result_sha256"] == R300A_RESULT_OBJECT_SHA256
        and r300a_result.get("status")
        == (
            "PASS_ROUND300A_EXHAUSTIVE_FAIL_CLOSED_DIAGNOSTIC__"
            "NO_GRAPH_ZERO_COMPONENT_EDGE_PROMOTION"
        )
        and r300a_result["frontier_ledger"][
            "canonical_occurrence_pair_row_count"
        ]
        == 3_232
        and r300a_result["prior_witness_partition"][
            "R295A_explicit_lower_graph_sheet_witness_pair_count"
        ]
        == 128
        and r300a_result["prior_witness_partition"][
            "unresolved_exact_pair_count"
        ]
        == 3_104
        and r300a_verification["verification_sha256"]
        == R300A_VERIFICATION_OBJECT_SHA256
        and str(r300a_verification.get("status", "")).startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND300A"
        ),
        "Round300A sealed semantic admission",
    )

    r303b_result = read_source_json(
        R303B_RESULT, allow_single_terminal_lf=True
    )
    r303b_verification = read_source_json(
        R303B_VERIFICATION, allow_single_terminal_lf=True
    )
    verify_self(r303b_result, "result_sha256", R303B_RESULT)
    verify_self(r303b_verification, "verification_sha256", R303B_VERIFICATION)
    need(
        r303b_result["result_sha256"] == R303B_RESULT_OBJECT_SHA256
        and r303b_result.get("status")
        == (
            "PASS_ROUND303B_43912_B1_192_B2_COMPONENT_EDGES__"
            "4_WTAIL_UNRESOLVED__ZERO_DSU_AND_DOWNSTREAM_CREDIT"
        )
        and r303b_verification["verification_sha256"]
        == R303B_VERIFICATION_OBJECT_SHA256
        and r303b_verification.get("status")
        == "PASS_EXACT_CACHELESS_EXPECTED_STATE",
        "Round303B sealed lineage admission",
    )

    r304_result = read_source_json(R304_RESULT)
    r304_verification = read_source_json(R304_VERIFICATION)
    verify_self(r304_result, "result_sha256", R304_RESULT)
    verify_self(r304_verification, "verification_sha256", R304_VERIFICATION)
    maximality = r304_result.get("maximality_gate")
    forward = r304_result.get("forward_application")
    need(
        r304_result["result_sha256"] == R304_RESULT_OBJECT_SHA256
        and r304_result.get("status")
        == (
            "PASS_ROUND304_FRESH_EXTENDED_REGISTRY_LEGAL_DSU__"
            "275268_RANK_REDUCTIONS__92696_COMPONENTS__"
            "ZERO_MAXIMALITY_FIBRE_GLOBAL_DISPOSITION_CREDIT"
        )
        and type(forward) is dict
        and forward.get("rank_reduction") == 275_268
        and forward.get("component_count") == 92_696
        and forward.get("partition_sha256") == R304_PARTITION_SHA256
        and type(maximality) is dict
        and maximality.get("complete_Round300A_pair_count") == 3_232
        and maximality.get("complete_reprojection_rows_sha256")
        == LEGACY_REPROJECTION_ROWS_SHA256
        and maximality.get("post_Round304_disposition_histogram")
        == EXPECTED_HISTOGRAM
        and maximality.get("cross_component_unwitnessed_pair_count") == 1_024
        and maximality.get("formal_maximality_credit") == 0
        and maximality.get("maximality_proved") is False
        and r304_result["output_ledgers"]["member"]["file_sha256"]
        == R304_MEMBER_LEDGER_SHA256
        and r304_verification["verification_sha256"]
        == R304_VERIFICATION_OBJECT_SHA256
        and r304_verification.get("status")
        == "PASS_EXACT_CACHELESS_EXPECTED_STATE"
        and r304_verification.get("formal_Round304_promotion_permitted") is True,
        "Round304 sealed partition admission",
    )
    return {
        "Round300A": {
            "manifest_filename": R300A_MANIFEST,
            "manifest_file_sha256": R300A_MANIFEST_SHA256,
            "manifest_member_count": 8,
            "ledger_filename": R300A_LEDGER,
            "ledger_file_sha256": R300A_LEDGER_SHA256,
            "result_filename": R300A_RESULT,
            "result_file_sha256": R300A_RESULT_FILE_SHA256,
            "result_object_sha256": R300A_RESULT_OBJECT_SHA256,
            "verification_filename": R300A_VERIFICATION,
            "verification_file_sha256": R300A_VERIFICATION_FILE_SHA256,
            "verification_object_sha256": R300A_VERIFICATION_OBJECT_SHA256,
            "complete_manifest_validated": True,
        },
        "Round303B": {
            "manifest_filename": R303B_MANIFEST,
            "manifest_file_sha256": R303B_MANIFEST_SHA256,
            "manifest_member_count": 12,
            "result_file_sha256": R303B_RESULT_FILE_SHA256,
            "result_object_sha256": R303B_RESULT_OBJECT_SHA256,
            "verification_file_sha256": R303B_VERIFICATION_FILE_SHA256,
            "verification_object_sha256": R303B_VERIFICATION_OBJECT_SHA256,
            "complete_manifest_validated": True,
            "used_as_scope_state": False,
        },
        "Round304": {
            "manifest_filename": R304_MANIFEST,
            "manifest_file_sha256": R304_MANIFEST_SHA256,
            "manifest_member_count": 11,
            "member_ledger_filename": R304_MEMBER_LEDGER,
            "member_ledger_file_sha256": R304_MEMBER_LEDGER_SHA256,
            "result_filename": R304_RESULT,
            "result_file_sha256": R304_RESULT_FILE_SHA256,
            "result_object_sha256": R304_RESULT_OBJECT_SHA256,
            "verification_filename": R304_VERIFICATION,
            "verification_file_sha256": R304_VERIFICATION_FILE_SHA256,
            "verification_object_sha256": R304_VERIFICATION_OBJECT_SHA256,
            "complete_manifest_validated": True,
        },
    }


def read_R300A_frontier() -> tuple[list[dict[str, Any]], set[str]]:
    rows: list[dict[str, Any]] = []
    endpoints: set[str] = set()
    pair_set: set[tuple[str, str]] = set()
    witnessed = 0
    prior_row_id: str | None = None
    for row in stream_gzip_rows(
        R300A_LEDGER,
        "canonical_occurrence_pair_rows",
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_COMMITMENT,
    ):
        row_id = row.get("Round300A_canonical_occurrence_pair_row_id")
        pair = row.get("canonical_unordered_Round294_registry_occurrence_ids")
        prior = row.get("R295A_explicit_lower_graph_sheet_witness_present")
        need(
            set(row) == set(R300A_ROW_EXACT_FIELDS)
            and type(row_id) is str
            and (prior_row_id is None or prior_row_id < row_id)
            and type(pair) is list
            and len(pair) == 2
            and all(type(item) is str for item in pair)
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and tuple(pair) not in pair_set
            and row.get("left_Round294_registry_occurrence_id") == pair[0]
            and row.get("right_Round294_registry_occurrence_id") == pair[1]
            and type(prior) is bool
            and row.get("self_pair") is False
            and row.get("formal_component_edge_credit") == 0
            and row.get("formal_DSU_rank_reduction_credit") == 0
            and row.get("formal_maximality_credit") == 0
            and row.get("formal_occurrence_identity_collapse_credit") == 0
            and row.get("formal_seam_edge_credit") == 0,
            "Round300A canonical-pair boundary",
        )
        prior_row_id = row_id
        pair_set.add(tuple(pair))
        endpoints.update(pair)
        witnessed += int(prior)
        rows.append({
            "row_id": row_id,
            "row_sha256": row["row_sha256"],
            "pair": list(pair),
            "prior_witness": prior,
        })
    need(
        len(rows) == 3_232
        and len(pair_set) == 3_232
        and witnessed == 128
        and len(endpoints) == 4_892,
        "exact Round300A 3232-pair/4892-endpoint frontier",
    )
    return rows, endpoints


R300A_ROW_EXACT_FIELDS = frozenset({
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
})


R304_MEMBER_EXACT_FIELDS = frozenset({
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
})


def read_R304_endpoint_projection(
    requested_endpoints: set[str],
) -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    selected: dict[str, dict[str, str]] = {}
    occurrences: set[str] = set()
    root_to_component: dict[str, str] = {}
    official_keys: set[str] = set()
    for row in stream_gzip_rows(
        R304_MEMBER_LEDGER,
        "fresh_member_component_rows",
        "Round304_fresh_member_component_row_id",
        R304_MEMBER_COMMITMENT,
    ):
        need(
            set(row) == set(R304_MEMBER_EXACT_FIELDS)
            and row.get("schema")
            == "cm2.round304.fresh-member-component-row.v1"
            and row.get("member_identity_preserved") is True
            and row.get("formal_maximality_credit") == 0
            and row.get("formal_fibre_credit") == 0
            and row.get("formal_global_disposition_credit") == 0,
            "Round304 member row boundary",
        )
        occurrence = row.get("registry_occurrence_id")
        base_root = row.get("base_root_id")
        component = row.get("final_component_id")
        official_key = row.get("official_key_id")
        need(
            type(occurrence) is str
            and occurrence not in occurrences
            and type(base_root) is str
            and type(component) is str
            and type(official_key) is str,
            "Round304 member projection fields",
        )
        occurrences.add(occurrence)
        prior_component = root_to_component.setdefault(base_root, component)
        need(prior_component == component, "Round304 base-root component split")
        official_keys.add(official_key)
        if occurrence in requested_endpoints:
            need(occurrence not in selected, "duplicate requested endpoint")
            selected[occurrence] = {
                "source_row_id": row["Round304_fresh_member_component_row_id"],
                "source_row_sha256": row["row_sha256"],
                "base_root_id": base_root,
                "final_component_id": component,
            }
    need(
        len(occurrences) == 564_492
        and len(root_to_component) == 367_964
        and len(set(root_to_component.values())) == 92_696
        and len(official_keys) == 124
        and set(selected) == requested_endpoints
        and len(selected) == 4_892,
        "complete Round304 universe and endpoint coverage",
    )
    component_roots: dict[str, list[str]] = {}
    for root, component in root_to_component.items():
        component_roots.setdefault(component, []).append(root)
    components = sorted(sorted(group) for group in component_roots.values())
    need(digest(components) == R304_PARTITION_SHA256, "Round304 partition replay")
    for component, roots in component_roots.items():
        ordered = sorted(roots)
        need(
            component == "round304-fresh-legal-component:" + digest(ordered),
            "Round304 component content address",
        )
    return selected, {
        "member_count": len(occurrences),
        "base_root_count": len(root_to_component),
        "final_component_count": len(component_roots),
        "official_key_count": len(official_keys),
        "requested_endpoint_count": len(selected),
        "partition_sha256": R304_PARTITION_SHA256,
    }


def close_expected_row(payload: dict[str, Any]) -> dict[str, Any]:
    need(set(payload) == set(EXACT_ROW_FIELDS - {ROW_ID_FIELD, "row_sha256"}), "row payload fields")
    row_id = "round305a-scope-reprojection:" + digest([
        "ROUND305A_SCOPE_REPROJECTION_V1",
        payload["source_Round300A_row_id"],
        payload["source_Round300A_row_sha256"],
        payload,
    ])
    row = close_object({ROW_ID_FIELD: row_id, **payload}, "row_sha256")
    need(set(row) == set(EXACT_ROW_FIELDS), "closed exact row fields")
    return row


def build_reprojection_rows(
    source_rows: list[dict[str, Any]],
    endpoint_map: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    legacy_rows: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    for source in source_rows:
        left_occurrence, right_occurrence = source["pair"]
        left = endpoint_map[left_occurrence]
        right = endpoint_map[right_occurrence]
        same = left["final_component_id"] == right["final_component_id"]
        prior = source["prior_witness"]
        disposition = (
            DISPOSITION_WITNESSED
            if prior and same
            else (
                "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY"
                if prior
                else (DISPOSITION_RECLOSED if same else DISPOSITION_RESIDUAL)
            )
        )
        need(
            disposition != "PRIOR_R295A_WITNESSED__CROSS_FINAL_COMPONENT_INCONSISTENCY",
            "prior witnessed pair split by Round304",
        )
        histogram[disposition] += 1
        base_root_pair = sorted([left["base_root_id"], right["base_root_id"]])
        component_pair = sorted([
            left["final_component_id"],
            right["final_component_id"],
        ])
        legacy = {
            "source_Round300A_row_id": source["row_id"],
            "source_Round300A_row_sha256": source["row_sha256"],
            "canonical_occurrence_pair": list(source["pair"]),
            "projected_base_root_pair": base_root_pair,
            "final_component_pair": component_pair,
            "prior_R295A_witness_present": prior,
            "same_final_component": same,
            "post_Round304_disposition": disposition,
        }
        legacy_rows.append(legacy)
        payload = {
            "schema": ROW_SCHEMA,
            "source_Round300A_row_id": source["row_id"],
            "source_Round300A_row_sha256": source["row_sha256"],
            "canonical_Round294_registry_occurrence_pair": list(source["pair"]),
            "left_Round294_registry_occurrence_id": left_occurrence,
            "right_Round294_registry_occurrence_id": right_occurrence,
            "left_Round304_member_row_id": left["source_row_id"],
            "left_Round304_member_row_sha256": left["source_row_sha256"],
            "right_Round304_member_row_id": right["source_row_id"],
            "right_Round304_member_row_sha256": right["source_row_sha256"],
            "left_base_root_id": left["base_root_id"],
            "right_base_root_id": right["base_root_id"],
            "projected_base_root_pair": base_root_pair,
            "left_final_component_id": left["final_component_id"],
            "right_final_component_id": right["final_component_id"],
            "final_component_pair": component_pair,
            "prior_R295A_witness_present": prior,
            "same_Round304_final_component": same,
            "post_Round304_disposition": disposition,
            "requires_formal_physical_inclusion": disposition == DISPOSITION_RESIDUAL,
            "source_row_fed_to_DSU": False,
            "unsealed_temp_scope_consumed": False,
            "formal_physical_inclusion_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
        }
        rows.append(close_expected_row(payload))
    need(
        len(rows) == 3_232
        and dict(sorted(histogram.items())) == EXPECTED_HISTOGRAM
        and digest(legacy_rows) == LEGACY_REPROJECTION_ROWS_SHA256,
        "exact Round304-compatible classification replay",
    )
    residual_legacy = [
        row for row in legacy_rows
        if row["post_Round304_disposition"] == DISPOSITION_RESIDUAL
    ]
    need(digest(residual_legacy) == RESIDUAL_PROJECTION_ROWS_SHA256, "residual legacy rows")
    return rows, legacy_rows, dict(sorted(histogram.items()))


def validate_expected_row(row: dict[str, Any], label: str) -> None:
    need(set(row) == set(EXACT_ROW_FIELDS), label + " exact fields")
    need(row.get("schema") == ROW_SCHEMA, label + " schema")
    verify_self(row, "row_sha256", label)
    pair = row.get("canonical_Round294_registry_occurrence_pair")
    roots = row.get("projected_base_root_pair")
    components = row.get("final_component_pair")
    disposition = row.get("post_Round304_disposition")
    prior = row.get("prior_R295A_witness_present")
    same = row.get("same_Round304_final_component")
    expected_disposition = (
        DISPOSITION_WITNESSED
        if prior is True and same is True
        else (
            None
            if prior is True
            else (DISPOSITION_RECLOSED if same is True else DISPOSITION_RESIDUAL)
        )
    )
    need(
        type(pair) is list
        and len(pair) == 2
        and pair == sorted(pair)
        and pair[0] != pair[1]
        and row.get("left_Round294_registry_occurrence_id") == pair[0]
        and row.get("right_Round294_registry_occurrence_id") == pair[1]
        and type(roots) is list
        and len(roots) == 2
        and roots == sorted([
            row.get("left_base_root_id"), row.get("right_base_root_id")
        ])
        and type(components) is list
        and len(components) == 2
        and components == sorted([
            row.get("left_final_component_id"),
            row.get("right_final_component_id"),
        ])
        and type(prior) is bool
        and type(same) is bool
        and same
        is (row.get("left_final_component_id") == row.get("right_final_component_id"))
        and expected_disposition is not None
        and disposition == expected_disposition
        and row.get("requires_formal_physical_inclusion")
        is (disposition == DISPOSITION_RESIDUAL)
        and row.get("source_row_fed_to_DSU") is False
        and row.get("unsealed_temp_scope_consumed") is False
        and all(row.get(field) == 0 for field in DOWNSTREAM_CREDIT_FIELDS),
        label + " semantic boundary",
    )


def build_expected_artifacts() -> tuple[dict[str, bytes], dict[str, Any]]:
    """Rebuild complete expected candidate bytes before candidate opens."""

    need(PIN.fullmatch(FINAL_PRODUCER_SHA256) is not None, "producer pin unfilled")
    need(
        SCHEMA_SNAPSHOT_SHA256 == FROZEN_SCHEMA_SNAPSHOT_SHA256,
        "schema snapshot mismatch",
    )
    validate_upstream_admission()
    source_rows, endpoint_set = read_R300A_frontier()
    endpoint_map, universe = read_R304_endpoint_projection(endpoint_set)
    rows, legacy_rows, histogram = build_reprojection_rows(source_rows, endpoint_map)
    for index, row in enumerate(rows):
        validate_expected_row(row, "expected row:" + str(index))
    row_ids = [row[ROW_ID_FIELD] for row in rows]
    row_hashes = [row["row_sha256"] for row in rows]
    need(len(row_ids) == len(set(row_ids)) == 3_232, "unique expected row IDs")

    residual_rows = [
        row for row in rows
        if row["post_Round304_disposition"] == DISPOSITION_RESIDUAL
    ]
    residual_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"]
        for row in residual_rows
    )
    residual_endpoints = sorted({
        endpoint for pair in residual_pairs for endpoint in pair
    })
    residual_roots = sorted(
        row["projected_base_root_pair"] for row in residual_rows
    )
    residual_components = sorted(
        row["final_component_pair"] for row in residual_rows
    )
    complete_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"] for row in rows
    )
    complete_endpoints = sorted({
        endpoint for pair in complete_pairs for endpoint in pair
    })
    prior_witnessed_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"]
        for row in rows
        if row["prior_R295A_witness_present"]
    )
    residual_ids = [row["source_Round300A_row_id"] for row in residual_rows]
    residual_hashes = [
        row["source_Round300A_row_sha256"] for row in residual_rows
    ]
    residual_id_hash_pairs = sorted(
        [row["source_Round300A_row_id"], row["source_Round300A_row_sha256"]]
        for row in residual_rows
    )
    endpoint_degree = Counter(
        endpoint for pair in residual_pairs for endpoint in pair
    )
    commitments = {
        "legacy_Round304_classification_rows_sha256": digest(legacy_rows),
        "classification_histogram": histogram,
        "complete_pair_count": len(complete_pairs),
        "complete_sorted_occurrence_pairs_sha256": digest(complete_pairs),
        "complete_endpoint_count": len(complete_endpoints),
        "complete_sorted_occurrence_endpoints_sha256": digest(complete_endpoints),
        "prior_R295A_witnessed_pair_count": len(prior_witnessed_pairs),
        "prior_R295A_witnessed_sorted_occurrence_pairs_sha256": digest(
            prior_witnessed_pairs
        ),
        "Round304_mapped_frontier_endpoint_count": len(endpoint_map),
        "Round304_expected_frontier_endpoint_count": 4_892,
        "residual_source_Round300A_row_count": len(residual_rows),
        "residual_source_Round300A_row_ids_sha256": digest(residual_ids),
        "residual_source_Round300A_row_hashes_sha256": digest(residual_hashes),
        "residual_sorted_source_Round300A_id_hash_pairs_sha256": digest(
            residual_id_hash_pairs
        ),
        "residual_pair_count": len(residual_pairs),
        "residual_sorted_occurrence_pairs_sha256": digest(residual_pairs),
        "residual_endpoint_count": len(residual_endpoints),
        "residual_sorted_occurrence_endpoints_sha256": digest(
            residual_endpoints
        ),
        "residual_sorted_projected_base_root_pairs_sha256": digest(
            residual_roots
        ),
        "residual_sorted_final_component_pairs_sha256": digest(
            residual_components
        ),
        "residual_endpoint_degree_histogram": {
            str(degree): frequency
            for degree, frequency in sorted(
                Counter(endpoint_degree.values()).items()
            )
        },
    }
    need(
        len(residual_rows) == 1_024
        and len(complete_pairs) == 3_232
        and digest(complete_pairs) == COMPLETE_PAIR_SET_SHA256
        and len(complete_endpoints) == 4_892
        and digest(complete_endpoints) == COMPLETE_ENDPOINT_SET_SHA256
        and len(prior_witnessed_pairs) == 128
        and digest(prior_witnessed_pairs) == PRIOR_WITNESSED_PAIR_SET_SHA256
        and len(residual_pairs) == len(set(map(tuple, residual_pairs))) == 1_024
        and digest(residual_pairs) == RESIDUAL_PAIR_SET_SHA256
        and len(residual_endpoints) == 2_048
        and digest(residual_endpoints) == RESIDUAL_ENDPOINT_SET_SHA256
        and commitments["residual_source_Round300A_row_ids_sha256"]
        == RESIDUAL_SOURCE_ROW_IDS_SHA256
        and commitments["residual_source_Round300A_row_hashes_sha256"]
        == RESIDUAL_SOURCE_ROW_HASHES_SHA256
        and commitments["residual_endpoint_degree_histogram"] == {"1": 2_048},
        "exact residual 1024-pair/2048-endpoint matching",
    )

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
    need(set(ledger) == set(EXACT_LEDGER_FIELDS), "exact expected ledger fields")
    verify_self(ledger, "ledger_sha256", "expected ledger")
    ledger_object_sha256 = digest(ledger)
    ledger_raw = deterministic_gzip(ledger)
    ledger_file_sha256 = hashlib.sha256(ledger_raw).hexdigest()
    output_metadata = {
        "filename": CANDIDATE_FILES["ledger"],
        "schema": LEDGER_SCHEMA,
        "ledger_self_sha256": ledger["ledger_sha256"],
        "ledger_object_sha256": ledger_object_sha256,
        "ledger_file_sha256": ledger_file_sha256,
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
        "producer_file_sha256": FINAL_PRODUCER_SHA256,
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "seed_affects_output": False,
        "upstream_seals": {
            "Round300A": {
                "manifest_filename": R300A_MANIFEST,
                "manifest_file_sha256": R300A_MANIFEST_SHA256,
                "manifest_member_count": 8,
                "ledger_filename": R300A_LEDGER,
                "ledger_file_sha256": R300A_LEDGER_SHA256,
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
                "manifest_member_count": 11,
                "member_ledger_filename": R304_MEMBER_LEDGER,
                "member_ledger_file_sha256": R304_MEMBER_LEDGER_SHA256,
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
                "manifest_member_count": 12,
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
        "reprojection_census": reprojection_census_from_commitments(
            commitments,
            len(rows),
        ),
        "residual_scope_commitments": commitments,
        "formal_credit_transition": {
            field: 0 for field in DOWNSTREAM_CREDIT_FIELDS
        },
        "strict_boundary": {
            "exact_residual_scope_reprojection_sealed": True,
            "unsealed_temp_scope_consumed": False,
            "temporary_file_or_directory_used_as_input": False,
            "Round303B_used_as_projection_input": False,
            "Round304_serialized_DSU_state_replayed": False,
            "Round304_member_component_ledger_used_only_as_sealed_projection_map": True,
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
    need(set(result) == set(EXACT_RESULT_FIELDS), "exact expected result fields")
    verify_self(result, "result_sha256", "expected result")
    result_raw = canonical(result)
    need(
        json_object_keys_are_strings(result)
        and canonical(strict_object(result_raw, "expected result replay")) == result_raw,
        "expected result canonical replay",
    )
    assert_snapshot_map(SOURCE_SNAPSHOTS, "upstream expected reconstruction")
    artifacts = {
        CANDIDATE_FILES["ledger"]: ledger_raw,
        CANDIDATE_FILES["result"]: result_raw,
    }
    need(universe["requested_endpoint_count"] == 4_892, "endpoint coverage")
    return artifacts, result


def expected_gzip_uncompressed_size(raw: bytes, label: str) -> int:
    """Read the trusted deterministic-gzip ISIZE without expanding it."""

    need(len(raw) >= 18, "expected gzip framing:" + label)
    size = int.from_bytes(raw[-4:], "little")
    need(0 < size < (1 << 31), "expected gzip ISIZE boundary:" + label)
    return size


def bounded_single_member_gzip(
    raw: bytes,
    maximum_uncompressed: int,
    label: str,
) -> bytes:
    """Expand exactly one gzip member with a strict output-memory ceiling."""

    need(maximum_uncompressed > 0, "positive gzip expansion ceiling:" + label)
    decoder = zlib.decompressobj(wbits=31)
    output: list[bytes] = []
    total = 0
    try:
        for offset in range(0, len(raw), 1 << 20):
            pending = raw[offset:offset + (1 << 20)]
            while pending:
                remaining = maximum_uncompressed - total
                block = decoder.decompress(pending, remaining + 1)
                need(
                    len(block) <= remaining,
                    "gzip expansion exceeds expected bytes:" + label,
                )
                output.append(block)
                total += len(block)
                pending = decoder.unconsumed_tail
                need(
                    not decoder.unused_data,
                    "gzip concatenation/trailing:" + label,
                )
        remaining = maximum_uncompressed - total
        tail = decoder.flush(remaining + 1)
    except zlib.error as exc:
        raise VerificationBlocked("gzip integrity:" + label) from exc
    need(
        len(tail) <= remaining,
        "gzip flush exceeds expected bytes:" + label,
    )
    output.append(tail)
    total += len(tail)
    need(
        decoder.eof
        and not decoder.unused_data
        and not decoder.unconsumed_tail
        and 0 < total <= maximum_uncompressed,
        "single complete bounded gzip member:" + label,
    )
    return b"".join(output)


def decode_candidate_ledger(
    raw: bytes,
    label: str,
    maximum_uncompressed: int,
) -> dict[str, Any]:
    unpacked = bounded_single_member_gzip(raw, maximum_uncompressed, label)
    ledger = strict_object(unpacked, label)
    need(deterministic_gzip(ledger) == raw, "deterministic gzip bytes:" + label)
    return ledger


def derive_candidate_commitments(rows: list[dict[str, Any]]) -> dict[str, Any]:
    legacy_rows = [
        {
            "source_Round300A_row_id": row["source_Round300A_row_id"],
            "source_Round300A_row_sha256": row["source_Round300A_row_sha256"],
            "canonical_occurrence_pair":
                row["canonical_Round294_registry_occurrence_pair"],
            "projected_base_root_pair": row["projected_base_root_pair"],
            "final_component_pair": row["final_component_pair"],
            "prior_R295A_witness_present": row["prior_R295A_witness_present"],
            "same_final_component": row["same_Round304_final_component"],
            "post_Round304_disposition": row["post_Round304_disposition"],
        }
        for row in rows
    ]
    histogram = Counter(row["post_Round304_disposition"] for row in rows)
    complete_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"] for row in rows
    )
    complete_endpoints = sorted({
        endpoint for pair in complete_pairs for endpoint in pair
    })
    prior_witnessed_pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"]
        for row in rows
        if row["prior_R295A_witness_present"]
    )
    residual = [
        row for row in rows
        if row["post_Round304_disposition"] == DISPOSITION_RESIDUAL
    ]
    pairs = sorted(
        row["canonical_Round294_registry_occurrence_pair"] for row in residual
    )
    endpoints = sorted({endpoint for pair in pairs for endpoint in pair})
    roots = sorted(row["projected_base_root_pair"] for row in residual)
    components = sorted(row["final_component_pair"] for row in residual)
    source_ids = [row["source_Round300A_row_id"] for row in residual]
    source_hashes = [row["source_Round300A_row_sha256"] for row in residual]
    source_pairs = sorted(
        [row["source_Round300A_row_id"], row["source_Round300A_row_sha256"]]
        for row in residual
    )
    degree = Counter(endpoint for pair in pairs for endpoint in pair)
    return {
        "legacy_Round304_classification_rows_sha256": digest(legacy_rows),
        "classification_histogram": dict(sorted(histogram.items())),
        "complete_pair_count": len(complete_pairs),
        "complete_sorted_occurrence_pairs_sha256": digest(complete_pairs),
        "complete_endpoint_count": len(complete_endpoints),
        "complete_sorted_occurrence_endpoints_sha256": digest(complete_endpoints),
        "prior_R295A_witnessed_pair_count": len(prior_witnessed_pairs),
        "prior_R295A_witnessed_sorted_occurrence_pairs_sha256": digest(
            prior_witnessed_pairs
        ),
        "Round304_mapped_frontier_endpoint_count": len(complete_endpoints),
        "Round304_expected_frontier_endpoint_count": 4_892,
        "residual_source_Round300A_row_count": len(residual),
        "residual_source_Round300A_row_ids_sha256": digest(source_ids),
        "residual_source_Round300A_row_hashes_sha256": digest(source_hashes),
        "residual_sorted_source_Round300A_id_hash_pairs_sha256": digest(source_pairs),
        "residual_pair_count": len(pairs),
        "residual_sorted_occurrence_pairs_sha256": digest(pairs),
        "residual_endpoint_count": len(endpoints),
        "residual_sorted_occurrence_endpoints_sha256": digest(endpoints),
        "residual_sorted_projected_base_root_pairs_sha256": digest(roots),
        "residual_sorted_final_component_pairs_sha256": digest(components),
        "residual_endpoint_degree_histogram": {
            str(item): count
            for item, count in sorted(Counter(degree.values()).items())
        },
    }


def derive_occurrence_member_bindings(
    rows: list[dict[str, Any]],
    label: str,
) -> dict[str, list[str]]:
    bindings: dict[str, list[str]] = {}
    for row in rows:
        for side in ("left", "right"):
            occurrence = row[side + "_Round294_registry_occurrence_id"]
            binding = [
                row[side + "_Round304_member_row_id"],
                row[side + "_Round304_member_row_sha256"],
            ]
            need(
                type(occurrence) is str
                and all(type(item) is str for item in binding),
                label + " binding types",
            )
            prior = bindings.setdefault(occurrence, binding)
            need(prior == binding, label + " conflicting occurrence binding")
    return dict(sorted(bindings.items()))


def reprojection_census_from_commitments(
    commitments: dict[str, Any],
    row_count: int,
) -> dict[str, Any]:
    histogram = commitments["classification_histogram"]
    return {
        "complete_Round300A_pair_count": row_count,
        "prior_R295A_witnessed_same_component_count":
            histogram.get(DISPOSITION_WITNESSED, 0),
        "unwitnessed_reclosed_by_other_legal_path_count":
            histogram.get(DISPOSITION_RECLOSED, 0),
        "unwitnessed_cross_component_residual_count":
            histogram.get(DISPOSITION_RESIDUAL, 0),
        "prior_R295A_witnessed_cross_component_inconsistency_count": 0,
        "legacy_Round304_classification_rows_sha256":
            commitments["legacy_Round304_classification_rows_sha256"],
        "exact_Round304_classification_reproduced": True,
        "complete_pair_set_sha256":
            commitments["complete_sorted_occurrence_pairs_sha256"],
        "complete_endpoint_count": commitments["complete_endpoint_count"],
        "complete_endpoint_set_sha256":
            commitments["complete_sorted_occurrence_endpoints_sha256"],
        "prior_R295A_witnessed_pair_set_sha256": commitments[
            "prior_R295A_witnessed_sorted_occurrence_pairs_sha256"
        ],
        "Round304_mapped_frontier_endpoint_count": commitments[
            "Round304_mapped_frontier_endpoint_count"
        ],
        "Round304_expected_frontier_endpoint_count": 4_892,
    }


def validate_artifact_bundle(
    bundle: dict[str, bytes],
    expected: dict[str, bytes],
) -> tuple[dict[str, Any], dict[str, Any]]:
    need(set(bundle) == set(expected), "candidate exact artifact set")
    expected_uncompressed_size = expected_gzip_uncompressed_size(
        expected[CANDIDATE_FILES["ledger"]],
        "independently rebuilt expected ledger",
    )
    ledger = decode_candidate_ledger(
        bundle[CANDIDATE_FILES["ledger"]],
        CANDIDATE_FILES["ledger"],
        expected_uncompressed_size,
    )
    reference_ledger = decode_candidate_ledger(
        expected[CANDIDATE_FILES["ledger"]],
        "independently rebuilt binding reference ledger",
        expected_uncompressed_size,
    )
    result = strict_object(
        bundle[CANDIDATE_FILES["result"]],
        CANDIDATE_FILES["result"],
    )
    need(set(ledger) == set(EXACT_LEDGER_FIELDS), "candidate ledger fields")
    need(set(result) == set(EXACT_RESULT_FIELDS), "candidate result fields")
    verify_self(ledger, "ledger_sha256", "candidate ledger")
    verify_self(result, "result_sha256", "candidate result")
    rows = ledger.get(TABLE)
    need(type(rows) is list and len(rows) == 3_232, "candidate 3232 rows")
    for index, row in enumerate(rows):
        need(type(row) is dict, "candidate row object")
        validate_expected_row(row, "candidate row:" + str(index))
    reference_rows = reference_ledger.get(TABLE)
    need(
        type(reference_rows) is list and len(reference_rows) == 3_232,
        "independently rebuilt binding reference rows",
    )
    candidate_bindings = derive_occurrence_member_bindings(rows, "candidate")
    expected_bindings = derive_occurrence_member_bindings(
        reference_rows,
        "expected",
    )
    # The per-occurrence map proves every candidate binding is the sealed one;
    # the complete endpoint-set commitment below supplies the exact key set.
    need(
        all(
            expected_bindings.get(occurrence) == binding
            for occurrence, binding in candidate_bindings.items()
        ),
        "candidate occurrence-to-Round304-member binding",
    )
    row_ids = [row[ROW_ID_FIELD] for row in rows]
    row_hashes = [row["row_sha256"] for row in rows]
    commitments = derive_candidate_commitments(rows)
    need(
        ledger.get("schema") == LEDGER_SCHEMA
        and ledger.get("status")
        == (
            "PASS_EXACT_3232_POST_ROUND304_REPROJECTION__"
            "1024_RESIDUAL_SCOPE__ZERO_DOWNSTREAM_CREDIT"
        )
        and ledger.get("row_count") == 3_232
        and len(set(row_ids)) == 3_232
        and ledger.get("row_ids_sha256") == digest(row_ids)
        and ledger.get("row_hashes_sha256") == digest(row_hashes)
        and ledger.get("rows_sha256") == digest(rows)
        and all(ledger.get(key) == value for key, value in commitments.items()),
        "candidate ledger cascade closure",
    )
    need(
        commitments["residual_endpoint_count"] == 2_048
        and commitments["residual_sorted_occurrence_endpoints_sha256"]
        == RESIDUAL_ENDPOINT_SET_SHA256,
        "candidate exact residual endpoint-set commitment",
    )
    need(
        commitments["legacy_Round304_classification_rows_sha256"]
        == LEGACY_REPROJECTION_ROWS_SHA256,
        "candidate exact legacy Round304 projection commitment",
    )
    need(
        commitments["classification_histogram"] == EXPECTED_HISTOGRAM
        and commitments["complete_pair_count"] == 3_232
        and commitments["complete_sorted_occurrence_pairs_sha256"]
        == COMPLETE_PAIR_SET_SHA256
        and commitments["complete_endpoint_count"] == 4_892
        and commitments["complete_sorted_occurrence_endpoints_sha256"]
        == COMPLETE_ENDPOINT_SET_SHA256
        and commitments["prior_R295A_witnessed_pair_count"] == 128
        and commitments[
            "prior_R295A_witnessed_sorted_occurrence_pairs_sha256"
        ]
        == PRIOR_WITNESSED_PAIR_SET_SHA256
        and commitments["Round304_mapped_frontier_endpoint_count"] == 4_892
        and commitments["Round304_expected_frontier_endpoint_count"] == 4_892
        and commitments["residual_pair_count"] == 1_024
        and commitments["residual_sorted_occurrence_pairs_sha256"]
        == RESIDUAL_PAIR_SET_SHA256
        and commitments["residual_source_Round300A_row_ids_sha256"]
        == RESIDUAL_SOURCE_ROW_IDS_SHA256
        and commitments["residual_source_Round300A_row_hashes_sha256"]
        == RESIDUAL_SOURCE_ROW_HASHES_SHA256
        and commitments["residual_endpoint_degree_histogram"] == {"1": 2_048},
        "candidate exact sealed scope commitments",
    )
    output = result.get("output_ledger")
    formal = result.get("formal_credit_transition")
    strict = result.get("strict_boundary")
    need(
        result.get("schema") == RESULT_SCHEMA
        and result.get("status")
        == (
            "PASS_ROUND305A_EXACT_R300A_POST_R304_RESIDUAL_SCOPE_"
            "REPROJECTION__1024_RESIDUAL_PAIRS__ZERO_DOWNSTREAM_CREDIT"
        )
        and result.get("producer_file_sha256") == FINAL_PRODUCER_SHA256
        and result.get("schema_snapshot_sha256") == SCHEMA_SNAPSHOT_SHA256
        and result.get("seed_affects_output") is False
        and result.get("residual_scope_commitments") == commitments
        and result.get("reprojection_census")
        == reprojection_census_from_commitments(commitments, len(rows))
        and type(formal) is dict
        and set(formal) == set(DOWNSTREAM_CREDIT_FIELDS)
        and all(formal[field] == 0 for field in DOWNSTREAM_CREDIT_FIELDS)
        and type(strict) is dict
        and strict.get("unsealed_temp_scope_consumed") is False
        and strict.get("temporary_file_or_directory_used_as_input") is False
        and strict.get("physical_inclusion_package_present") is False
        and strict.get("two_sided_gluing_theorem_present") is False
        and strict.get("new_component_edges_issued") == 0
        and strict.get("fresh_DSU_rebuild_performed") is False
        and strict.get("Gate5_complete_18_field_block_count") == 0
        and strict.get("D02_status") == "BLOCKED"
        and strict.get("CM2_status") == "NO-GO_FOR_CLAIM"
        and type(output) is dict
        and output.get("filename") == CANDIDATE_FILES["ledger"]
        and output.get("ledger_self_sha256") == ledger["ledger_sha256"]
        and output.get("ledger_object_sha256") == digest(ledger)
        and output.get("ledger_file_sha256")
        == hashlib.sha256(bundle[CANDIDATE_FILES["ledger"]]).hexdigest()
        and output.get("row_ids_sha256") == ledger["row_ids_sha256"]
        and output.get("row_hashes_sha256") == ledger["row_hashes_sha256"]
        and output.get("rows_sha256") == ledger["rows_sha256"],
        "candidate result semantic boundary",
    )
    need(
        bundle[CANDIDATE_FILES["ledger"]]
        == expected[CANDIDATE_FILES["ledger"]]
        and bundle[CANDIDATE_FILES["result"]]
        == expected[CANDIDATE_FILES["result"]],
        "candidate exact independently rebuilt bytes",
    )
    return ledger, result


def resolve_candidate_directory(candidate_dir: Path) -> Path:
    lexical = lexical_directory_without_symlinks(candidate_dir, "candidate directory")
    resolved = candidate_dir.resolve()
    need(lexical == resolved, "candidate directory symlink/dot escape")
    need(
        resolved == DATA.resolve() or ROOT.resolve() in resolved.parents,
        "candidate directory outside workspace",
    )
    need(resolved != ROOT.resolve(), "workspace root is not candidate directory")
    return resolved


def read_candidate_bundle(
    candidate_dir: Path,
    expected: dict[str, bytes],
) -> dict[str, bytes]:
    resolved = resolve_candidate_directory(candidate_dir)
    output: dict[str, bytes] = {}
    for key in ("ledger", "result"):
        name = CANDIDATE_FILES[key]
        output[name] = stable_read_bytes(
            resolved / name,
            resolved,
            CANDIDATE_SNAPSHOTS,
            maximum=len(expected[name]),
            label="candidate exact-size boundary:" + name,
        )
    return output


def resign_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = dict(row)
    payload.pop(ROW_ID_FIELD, None)
    payload.pop("row_sha256", None)
    return close_expected_row(payload)


def cascade_objects(
    ledger: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, bytes]:
    """Re-sign every candidate layer after an in-memory semantic mutation."""

    ledger_payload = dict(ledger)
    ledger_payload.pop("ledger_sha256", None)
    rows = ledger_payload[TABLE]
    commitments = derive_candidate_commitments(rows)
    for key, value in commitments.items():
        ledger_payload[key] = value
    ledger_payload["row_count"] = len(rows)
    ledger_payload["row_ids_sha256"] = digest([
        row[ROW_ID_FIELD] for row in rows
    ])
    ledger_payload["row_hashes_sha256"] = digest([
        row["row_sha256"] for row in rows
    ])
    ledger_payload["rows_sha256"] = digest(rows)
    resigned_ledger = close_object(ledger_payload, "ledger_sha256")
    ledger_raw = deterministic_gzip(resigned_ledger)

    result_payload = dict(result)
    result_payload.pop("result_sha256", None)
    result_payload["residual_scope_commitments"] = commitments
    result_payload["reprojection_census"] = reprojection_census_from_commitments(
        commitments,
        len(rows),
    )
    result_payload["output_ledger"] = {
        "filename": CANDIDATE_FILES["ledger"],
        "schema": LEDGER_SCHEMA,
        "ledger_self_sha256": resigned_ledger["ledger_sha256"],
        "ledger_object_sha256": digest(resigned_ledger),
        "ledger_file_sha256": hashlib.sha256(ledger_raw).hexdigest(),
        "row_count": len(rows),
        "row_ids_sha256": resigned_ledger["row_ids_sha256"],
        "row_hashes_sha256": resigned_ledger["row_hashes_sha256"],
        "rows_sha256": resigned_ledger["rows_sha256"],
    }
    resigned_result = close_object(result_payload, "result_sha256")
    return {
        CANDIDATE_FILES["ledger"]: ledger_raw,
        CANDIDATE_FILES["result"]: canonical(resigned_result),
    }


def rejected(callback: Callable[[], None]) -> bool:
    try:
        callback()
    except (VerificationBlocked, OSError, ValueError, KeyError, TypeError):
        return True
    return False


def semantic_mutation_bundle(
    expected: dict[str, bytes],
    mutate: Callable[[dict[str, Any], dict[str, Any]], None],
) -> dict[str, bytes]:
    ledger = decode_candidate_ledger(
        expected[CANDIDATE_FILES["ledger"]],
        "attack baseline ledger",
        expected_gzip_uncompressed_size(
            expected[CANDIDATE_FILES["ledger"]],
            "attack expected ledger",
        ),
    )
    result = strict_object(
        expected[CANDIDATE_FILES["result"]],
        "attack baseline result",
    )
    mutate(ledger, result)
    return cascade_objects(ledger, result)


def result_mutation_bundle(
    expected: dict[str, bytes],
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, bytes]:
    result = strict_object(
        expected[CANDIDATE_FILES["result"]],
        "attack result baseline",
    )
    payload = dict(result)
    payload.pop("result_sha256", None)
    mutate(payload)
    resigned = close_object(payload, "result_sha256")
    return {
        CANDIDATE_FILES["ledger"]: expected[CANDIDATE_FILES["ledger"]],
        CANDIDATE_FILES["result"]: canonical(resigned),
    }


def build_attack_suite(
    expected: dict[str, bytes],
    baseline_pins: dict[str, str],
    verifier_sha256: str,
) -> dict[str, Any]:
    """Run independently validated coherent, wire, and OS-boundary fixtures."""

    baseline_ledger = decode_candidate_ledger(
        expected[CANDIDATE_FILES["ledger"]],
        "attack expected ledger",
        expected_gzip_uncompressed_size(
            expected[CANDIDATE_FILES["ledger"]],
            "attack expected ledger",
        ),
    )
    rows = baseline_ledger[TABLE]
    residual_indices = [
        index for index, row in enumerate(rows)
        if row["requires_formal_physical_inclusion"]
    ]
    need(len(residual_indices) == 1_024, "attack baseline residual census")
    residual_index = residual_indices[0]
    reclosed_index = next(
        index for index, row in enumerate(rows)
        if row["post_Round304_disposition"] == DISPOSITION_RECLOSED
    )

    fixtures: list[tuple[str, str, bool, Callable[[], None]]] = []

    def add_semantic(
        mechanism: str,
        mutate: Callable[[dict[str, Any], dict[str, Any]], None],
        category: str = "CASCADE",
    ) -> None:
        def callback() -> None:
            candidate = semantic_mutation_bundle(expected, mutate)
            validate_artifact_bundle(candidate, expected)
        fixtures.append((category, mechanism, True, callback))

    def add_result(
        mechanism: str,
        mutate: Callable[[dict[str, Any]], None],
        category: str,
    ) -> None:
        def callback() -> None:
            candidate = result_mutation_bundle(expected, mutate)
            validate_artifact_bundle(candidate, expected)
        fixtures.append((category, mechanism, True, callback))

    def mutate_row(
        index: int,
        change: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any], dict[str, Any]], None]:
        def apply(ledger: dict[str, Any], _result: dict[str, Any]) -> None:
            row = dict(ledger[TABLE][index])
            change(row)
            ledger[TABLE][index] = resign_row(row)
        return apply

    add_result(
        "upstream_manifest_member_set",
        lambda value: value["upstream_seals"]["Round304"].__setitem__(
            "manifest_member_count", 10
        ),
        "UPSTREAM",
    )
    add_result(
        "upstream_result_or_verification_downgrade",
        lambda value: value["upstream_seals"]["Round304"].__setitem__(
            "verification_object_sha256", "0" * 64
        ),
        "UPSTREAM",
    )
    add_semantic(
        "source_pair_provenance",
        mutate_row(0, lambda row: row.__setitem__("source_Round300A_row_sha256", "0" * 64)),
    )
    add_semantic(
        "source_pair_order_or_identity",
        mutate_row(
            0,
            lambda row: row.__setitem__(
                "canonical_Round294_registry_occurrence_pair",
                list(reversed(row["canonical_Round294_registry_occurrence_pair"])),
            ),
        ),
    )
    add_semantic(
        "prior_witness_flip",
        mutate_row(
            reclosed_index,
            lambda row: row.__setitem__("prior_R295A_witness_present", True),
        ),
    )
    add_semantic(
        "Round304_member_row_provenance",
        mutate_row(
            residual_index,
            lambda row: row.__setitem__("left_Round304_member_row_sha256", "0" * 64),
        ),
        "UPSTREAM",
    )
    add_semantic(
        "base_root_projection",
        mutate_row(
            residual_index,
            lambda row: row.__setitem__("left_base_root_id", "forged-root"),
        ),
    )

    def component_flip(row: dict[str, Any]) -> None:
        row["right_final_component_id"] = row["left_final_component_id"]
        row["final_component_pair"] = sorted([
            row["left_final_component_id"], row["right_final_component_id"]
        ])
        row["same_Round304_final_component"] = True
        row["post_Round304_disposition"] = DISPOSITION_RECLOSED
        row["requires_formal_physical_inclusion"] = False

    add_semantic("final_component_projection", mutate_row(residual_index, component_flip))
    add_semantic(
        "classification_disposition",
        mutate_row(
            residual_index,
            lambda row: row.__setitem__("post_Round304_disposition", DISPOSITION_RECLOSED),
        ),
    )

    def pair_forgery(row: dict[str, Any]) -> None:
        pair = list(row["canonical_Round294_registry_occurrence_pair"])
        pair[1] = "source-g-expanded-occurrence:" + "f" * 64
        pair.sort()
        row["canonical_Round294_registry_occurrence_pair"] = pair
        row["left_Round294_registry_occurrence_id"] = pair[0]
        row["right_Round294_registry_occurrence_id"] = pair[1]

    add_semantic(
        "residual_pair_set_same_count_resign",
        mutate_row(residual_index, pair_forgery),
    )
    add_semantic(
        "temporary_scope_consumption",
        mutate_row(
            residual_index,
            lambda row: row.__setitem__("unsealed_temp_scope_consumed", True),
        ),
    )
    target_member_row_id = rows[residual_index]["left_Round304_member_row_id"]
    donor_member_binding = next(
        (
            row[side + "_Round304_member_row_id"],
            row[side + "_Round304_member_row_sha256"],
        )
        for row in rows
        for side in ("left", "right")
        if row[side + "_Round304_member_row_id"] != target_member_row_id
    )
    add_semantic(
        "upstream_member_row_binding",
        mutate_row(
            residual_index,
            lambda row: row.update({
                "left_Round304_member_row_id": donor_member_binding[0],
                "left_Round304_member_row_sha256": donor_member_binding[1],
            }),
        ),
    )
    add_semantic(
        "same_component_flag",
        mutate_row(
            residual_index,
            lambda row: row.__setitem__("same_Round304_final_component", True),
        ),
    )
    add_result(
        "classification_census",
        lambda value: value["reprojection_census"].__setitem__(
            "unwitnessed_cross_component_residual_count", 1_023
        ),
        "CASCADE",
    )

    residual_endpoint_set = {
        endpoint
        for index in residual_indices
        for endpoint in rows[index]["canonical_Round294_registry_occurrence_pair"]
    }
    need(len(residual_endpoint_set) == 2_048, "attack baseline residual endpoints")
    target_row = rows[residual_index]
    retained_endpoint = target_row["left_Round294_registry_occurrence_id"]
    removed_endpoint = target_row["right_Round294_registry_occurrence_id"]
    retained_component = target_row["left_final_component_id"]
    donor_projection = next(
        {
            "occurrence": row[side + "_Round294_registry_occurrence_id"],
            "member_row_id": row[side + "_Round304_member_row_id"],
            "member_row_sha256": row[side + "_Round304_member_row_sha256"],
            "base_root_id": row[side + "_base_root_id"],
            "final_component_id": row[side + "_final_component_id"],
        }
        for row in rows
        for side in ("left", "right")
        if row[side + "_Round294_registry_occurrence_id"]
        not in residual_endpoint_set
        and row[side + "_final_component_id"] != retained_component
    )
    attacked_endpoint_set = sorted(
        (residual_endpoint_set - {removed_endpoint})
        | {donor_projection["occurrence"]}
    )
    need(
        retained_endpoint != donor_projection["occurrence"]
        and len(attacked_endpoint_set) == 2_048
        and digest(attacked_endpoint_set) != RESIDUAL_ENDPOINT_SET_SHA256,
        "real same-count changed residual endpoint-set fixture",
    )

    def replace_residual_endpoint(
        ledger: dict[str, Any],
        _result: dict[str, Any],
    ) -> None:
        row = dict(ledger[TABLE][residual_index])
        retained = {
            "occurrence": retained_endpoint,
            "member_row_id": row["left_Round304_member_row_id"],
            "member_row_sha256": row["left_Round304_member_row_sha256"],
            "base_root_id": row["left_base_root_id"],
            "final_component_id": row["left_final_component_id"],
        }
        projections = sorted(
            (retained, donor_projection),
            key=lambda item: item["occurrence"],
        )
        pair = [item["occurrence"] for item in projections]
        row["canonical_Round294_registry_occurrence_pair"] = pair
        for side, projection in zip(("left", "right"), projections, strict=True):
            row[side + "_Round294_registry_occurrence_id"] = projection["occurrence"]
            row[side + "_Round304_member_row_id"] = projection["member_row_id"]
            row[side + "_Round304_member_row_sha256"] = projection[
                "member_row_sha256"
            ]
            row[side + "_base_root_id"] = projection["base_root_id"]
            row[side + "_final_component_id"] = projection["final_component_id"]
        row["projected_base_root_pair"] = sorted([
            row["left_base_root_id"], row["right_base_root_id"]
        ])
        row["final_component_pair"] = sorted([
            row["left_final_component_id"], row["right_final_component_id"]
        ])
        ledger[TABLE][residual_index] = resign_row(row)

    add_semantic(
        "residual_endpoint_set_same_count_resign",
        replace_residual_endpoint,
    )

    def mutate_legacy_projection(
        ledger: dict[str, Any],
        _result: dict[str, Any],
    ) -> None:
        row = dict(ledger[TABLE][reclosed_index])
        row["left_base_root_id"] = "round305a-forged-base-root"
        row["projected_base_root_pair"] = sorted([
            row["left_base_root_id"], row["right_base_root_id"]
        ])
        ledger[TABLE][reclosed_index] = resign_row(row)

    add_semantic("legacy_projection_commitment", mutate_legacy_projection)
    for mechanism, field in (
        ("physical_inclusion_credit_nonzero", "formal_physical_inclusion_credit"),
        ("component_edge_credit_nonzero", "formal_component_edge_credit"),
        ("DSU_credit_nonzero", "formal_DSU_rank_reduction_credit"),
        ("maximality_credit_nonzero", "formal_maximality_credit"),
        ("fibre_credit_nonzero", "formal_fibre_credit"),
        ("global_disposition_credit_nonzero", "formal_global_disposition_credit"),
        ("Jx_Jy_credit_nonzero", "formal_Jx_Jy_same_point_glue_credit"),
    ):
        add_semantic(
            mechanism,
            mutate_row(residual_index, lambda row, key=field: row.__setitem__(key, 1)),
            "CREDIT",
        )
    add_result(
        "Gate5_or_D02_or_CM2_upgrade",
        lambda value: value["strict_boundary"].update({
            "Gate5_complete_18_field_block_count": 1,
            "D02_status": "PASS",
            "CM2_status": "UNCONDITIONAL",
        }),
        "CREDIT",
    )
    add_result(
        "seed_dependent_output",
        lambda value: value.__setitem__("seed_affects_output", True),
        "CASCADE",
    )

    def validate_raw_bundle(bundle: dict[str, bytes]) -> None:
        validate_artifact_bundle(bundle, expected)

    duplicate = expected[CANDIDATE_FILES["result"]].replace(
        b'{"atomicity_contract":',
        b'{"schema":"duplicate","atomicity_contract":',
        1,
    )
    fixtures.append((
        "WIRE_OS_AST",
        "duplicate_JSON_key",
        False,
        lambda: validate_raw_bundle({
            CANDIDATE_FILES["ledger"]: expected[CANDIDATE_FILES["ledger"]],
            CANDIDATE_FILES["result"]: duplicate,
        }),
    ))
    fixtures.append((
        "WIRE_OS_AST",
        "noncanonical_or_nonintegral_JSON",
        False,
        lambda: validate_raw_bundle({
            CANDIDATE_FILES["ledger"]: expected[CANDIDATE_FILES["ledger"]],
            CANDIDATE_FILES["result"]: expected[CANDIDATE_FILES["result"]] + b"\n",
        }),
    ))
    def overexpansion_gzip(maximum: int) -> bytes:
        compressor = zlib.compressobj(level=9, wbits=31)
        pieces: list[bytes] = []
        remaining = maximum + 1
        chunk = b"x" * min(1 << 20, remaining)
        while remaining:
            block = chunk[:min(len(chunk), remaining)]
            pieces.append(compressor.compress(block))
            remaining -= len(block)
        pieces.append(compressor.flush())
        return b"".join(pieces)

    def gzip_boundary_fixture() -> None:
        concatenated = {
            CANDIDATE_FILES["ledger"]:
                expected[CANDIDATE_FILES["ledger"]] * 2,
            CANDIDATE_FILES["result"]: expected[CANDIDATE_FILES["result"]],
        }
        need(
            rejected(lambda: validate_raw_bundle(concatenated)),
            "concatenated gzip subfixture rejected",
        )
        expansion_limit = expected_gzip_uncompressed_size(
            expected[CANDIDATE_FILES["ledger"]],
            "gzip attack expected ledger",
        )
        validate_raw_bundle({
            CANDIDATE_FILES["ledger"]: overexpansion_gzip(expansion_limit),
            CANDIDATE_FILES["result"]: expected[CANDIDATE_FILES["result"]],
        })

    fixtures.append((
        "WIRE_OS_AST",
        "gzip_member_or_integrity",
        False,
        gzip_boundary_fixture,
    ))
    fixtures.append((
        "WIRE_OS_AST",
        "path_escape",
        False,
        lambda: resolve_candidate_directory(ROOT),
    ))

    def write_exclusive(path: Path, raw: bytes) -> None:
        descriptor = os.open(
            path,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0),
            0o600,
        )
        try:
            os.write(descriptor, raw)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def link_input_fixture() -> None:
        with tempfile.TemporaryDirectory(
            prefix=".r305a-link-attack-",
            dir=ROOT,
        ) as raw_directory:
            directory = Path(raw_directory)
            base = directory / "base"
            hardlink = directory / "hardlink"
            symlink = directory / "symlink"
            write_exclusive(base, b"x")
            os.link(base, hardlink)
            os.symlink(base.name, symlink)
            descriptor = os.open(
                directory,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_CLOEXEC", 0),
            )
            try:
                local_snapshots: dict[Path, FileIdentity] = {}
                need(
                    rejected(lambda: safe_regular_at(
                        hardlink.name,
                        directory,
                        descriptor,
                        local_snapshots,
                        10,
                        "hardlink attack",
                    )),
                    "hardlink subfixture rejected",
                )
                safe_regular_at(
                    symlink.name,
                    directory,
                    descriptor,
                    local_snapshots,
                    10,
                    "symlink attack",
                )
            finally:
                os.close(descriptor)

    fixtures.append((
        "WIRE_OS_AST",
        "symlink_or_hardlink_input",
        False,
        link_input_fixture,
    ))
    fixtures.append((
        "WIRE_OS_AST",
        "producer_import_exec_parse_tokenize",
        False,
        lambda: validate_inert_producer_access_plan((
            "import-producer-module",
            "execute-producer",
            "parse-producer-source",
            "tokenize-producer-source",
        )),
    ))
    fixtures.append((
        "WIRE_OS_AST",
        "temporary_runtime_dependency",
        False,
        lambda: require_formal_runtime_input(
            ROOT / ("." + "tmp") / "forged-upstream.json",
            "temporary runtime attack",
        ),
    ))

    def isolated_publisher_attack(
        callback: Callable[[Path], None],
        prefix: str,
    ) -> None:
        prior_parents = dict(PARENT_DIRECTORY_SNAPSHOTS)
        try:
            with tempfile.TemporaryDirectory(prefix=prefix, dir=ROOT) as raw_directory:
                callback(Path(raw_directory))
        finally:
            PARENT_DIRECTORY_SNAPSHOTS.clear()
            PARENT_DIRECTORY_SNAPSHOTS.update(prior_parents)

    def conflicting_target_attack(directory: Path) -> None:
        write_exclusive(directory / ATTACK_FILENAME, b"conflicting-attack")
        publish_attack_then_verification(directory, b"expected-attack", b"verification")

    fixtures.append((
        "WIRE_OS_AST",
        "existing_target_clobber",
        False,
        lambda: isolated_publisher_attack(
            conflicting_target_attack,
            ".r305a-clobber-attack-",
        ),
    ))

    def appeared_after_preflight_fixture() -> None:
        with tempfile.TemporaryDirectory(
            prefix=".r305a-race-attack-",
            dir=ROOT,
        ) as raw_directory:
            directory = Path(raw_directory)
            stage = directory / "stage"
            stage.mkdir(mode=0o700)
            source_name = "staged"
            target_name = "target"
            write_exclusive(stage / source_name, b"staged")
            source_descriptor = os.open(
                stage,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            target_descriptor = os.open(
                directory,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                try:
                    os.stat(
                        target_name,
                        dir_fd=target_descriptor,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    pass
                else:
                    raise VerificationBlocked("race target unexpectedly present")
                write_exclusive(directory / target_name, b"racer")
                try:
                    rename_noreplace(
                        source_descriptor,
                        source_name,
                        target_descriptor,
                        target_name,
                    )
                except FileExistsError as exc:
                    raise VerificationBlocked(
                        "target appeared after preflight and was not replaced"
                    ) from exc
            finally:
                os.close(source_descriptor)
                os.close(target_descriptor)

    fixtures.append((
        "WIRE_OS_AST",
        "target_appears_after_preflight",
        False,
        appeared_after_preflight_fixture,
    ))

    def toctou_fixture() -> None:
        with tempfile.TemporaryDirectory(
            prefix=".r305a-toctou-attack-",
            dir=ROOT,
        ) as raw_directory:
            path = Path(raw_directory) / "bound-input"
            write_exclusive(path, b"before")
            before = file_identity(os.lstat(path))
            os.unlink(path)
            write_exclusive(path, b"after-and-different")
            need(
                file_identity(os.lstat(path)) == before,
                "input/candidate/source PRE/POST identity mismatch",
            )

    fixtures.append((
        "WIRE_OS_AST",
        "input_candidate_or_source_TOCTOU",
        False,
        toctou_fixture,
    ))

    def verification_before_attack(directory: Path) -> None:
        write_exclusive(directory / VERIFICATION_FILENAME, b"verification")
        publish_attack_then_verification(directory, b"attack", b"verification")

    fixtures.append((
        "WIRE_OS_AST",
        "wrong_atomic_commit_order",
        False,
        lambda: isolated_publisher_attack(
            verification_before_attack,
            ".r305a-order-attack-",
        ),
    ))
    attack_rows: list[dict[str, Any]] = []
    for index, (category, mechanism, coherent, callback) in enumerate(fixtures):
        outcome = rejected(callback)
        need(outcome, "attack accepted:" + mechanism)
        payload = {
            "schema": RESULT_SCHEMA + ".attack-row.v1",
            "category": category,
            "mechanism": mechanism,
            "fixture_index": index,
            "all_cryptographic_layers_resigned": coherent,
            "rejected": outcome,
            "formal_credit": 0,
        }
        attack_id = "round305a-attack:" + digest([index, mechanism, payload])
        attack_rows.append(close_object(
            {"Round305A_attack_row_id": attack_id, **payload},
            "attack_row_sha256",
        ))
    mechanism_coverage = sorted({row["mechanism"] for row in attack_rows})
    need(
        set(mechanism_coverage) == set(ATTACK_MECHANISMS)
        and len(attack_rows) == len(ATTACK_MECHANISMS),
        "complete attack mechanism coverage",
    )
    need(
        all(
            row["category"] == ATTACK_CATEGORY_BY_MECHANISM[row["mechanism"]]
            for row in attack_rows
        ),
        "attack category assignment",
    )
    category_counts = dict(sorted(Counter(
        row["category"] for row in attack_rows
    ).items()))
    need(category_counts == EXPECTED_ATTACK_CATEGORY_COUNTS, "attack category census")
    coherently_resigned_count = sum(
        int(row["all_cryptographic_layers_resigned"])
        for row in attack_rows
    )
    need(
        coherently_resigned_count == EXPECTED_COHERENTLY_RESIGNED_FIXTURES,
        "coherently re-signed fixture census",
    )
    payload = {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_ALL_ROUND305A_ATTACK_FIXTURES_REJECTED",
        "producer_file_sha256": FINAL_PRODUCER_SHA256,
        "verifier_file_sha256": verifier_sha256,
        "baseline_candidate_file_pins": dict(sorted(baseline_pins.items())),
        "mechanism_count": len(ATTACK_MECHANISMS),
        "fixture_count": len(attack_rows),
        "rejected_count": len(attack_rows),
        "category_counts": category_counts,
        "mechanisms": list(ATTACK_MECHANISMS),
        "coherently_resigned_fixture_count": coherently_resigned_count,
        "attack_row_ids_sha256": digest([
            row["Round305A_attack_row_id"] for row in attack_rows
        ]),
        "attack_row_hashes_sha256": digest([
            row["attack_row_sha256"] for row in attack_rows
        ]),
        "attack_rows_sha256": digest(attack_rows),
        "attack_rows": attack_rows,
        "all_rejected": True,
        "formal_attack_credit": 0,
    }
    return close_object(payload, "attack_suite_sha256")


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


def read_recovery_stage_file(
    stage_descriptor: int,
    name: str,
    expected: bytes,
    label: str,
) -> None:
    info = os.stat(name, dir_fd=stage_descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_uid == os.geteuid()
        and info.st_nlink == 1
        and info.st_size == len(expected),
        label + " stage file boundary",
    )
    descriptor = os.open(
        name,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        dir_fd=stage_descriptor,
    )
    try:
        need(file_identity(os.fstat(descriptor)) == file_identity(info), label + " race")
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        need(b"".join(chunks) == expected, label + " exact bytes")
        need(file_identity(os.fstat(descriptor)) == file_identity(info), label + " drift")
    finally:
        os.close(descriptor)


def recover_private_promotion_stages(
    output_descriptor: int,
    artifacts: dict[str, bytes],
) -> None:
    for stage_name in sorted(os.listdir(output_descriptor)):
        if not stage_name.startswith(".r305a-promotion-stage-"):
            continue
        info = os.stat(stage_name, dir_fd=output_descriptor, follow_symlinks=False)
        need(
            stat.S_ISDIR(info.st_mode)
            and info.st_uid == os.geteuid()
            and stat.S_IMODE(info.st_mode) == 0o700,
            "promotion recovery stage boundary",
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
                "promotion recovery stage race",
            )
            names = set(os.listdir(stage_descriptor))
            need(names <= set(artifacts), "promotion recovery exact subset")
            for name in sorted(names):
                read_recovery_stage_file(
                    stage_descriptor,
                    name,
                    artifacts[name],
                    "promotion recovery:" + name,
                )
                os.unlink(name, dir_fd=stage_descriptor)
            os.fsync(stage_descriptor)
        finally:
            os.close(stage_descriptor)
        os.rmdir(stage_name, dir_fd=output_descriptor)
    os.fsync(output_descriptor)


def read_local_output(
    directory: Path,
    name: str,
    expected: bytes,
    snapshots: dict[Path, FileIdentity],
    label: str,
) -> bytes:
    raw = stable_read_bytes(
        directory / name,
        directory,
        snapshots,
        maximum=max(1, len(expected)),
        label=label,
    )
    need(raw == expected, label + " exact bytes")
    return raw


def publish_attack_then_verification(
    candidate_dir: Path,
    attack_raw: bytes,
    verification_raw: bytes,
) -> None:
    resolved = resolve_candidate_directory(candidate_dir)
    artifacts = {
        ATTACK_FILENAME: attack_raw,
        VERIFICATION_FILENAME: verification_raw,
    }
    ordered = [ATTACK_FILENAME, VERIFICATION_FILENAME]
    validate_promotion_commit_order(tuple(ordered))
    output_descriptor = os.open(
        resolved,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    bound = directory_identity(os.fstat(output_descriptor))
    need(bound == directory_identity(os.lstat(resolved)), "promotion directory race")
    output_snapshots: dict[Path, FileIdentity] = {}
    try:
        fcntl.flock(output_descriptor, fcntl.LOCK_EX)
        recover_private_promotion_stages(output_descriptor, artifacts)
        preexisting: set[str] = set()
        for name in ordered:
            if os.path.lexists(resolved / name):
                read_local_output(
                    resolved,
                    name,
                    artifacts[name],
                    output_snapshots,
                    "preexisting promotion:" + name,
                )
                preexisting.add(name)
        need(
            VERIFICATION_FILENAME not in preexisting
            or ATTACK_FILENAME in preexisting,
            "verification cannot preexist without attack suite",
        )
        with tempfile.TemporaryDirectory(
            prefix=".r305a-promotion-stage-",
            dir=resolved,
        ) as raw_stage:
            stage = Path(raw_stage)
            for name in ordered:
                descriptor = os.open(
                    stage / name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o644,
                )
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
                        read_local_output(
                            resolved,
                            name,
                            artifacts[name],
                            output_snapshots,
                            "stable preexisting promotion:" + name,
                        )
                        continue
                    assert_snapshot_map(SOURCE_SNAPSHOTS, "source before promotion")
                    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate before promotion")
                    try:
                        os.stat(name, dir_fd=output_descriptor, follow_symlinks=False)
                    except FileNotFoundError:
                        pass
                    else:
                        raise VerificationBlocked(
                            "promotion target appeared after preflight:" + name
                        )
                    try:
                        rename_noreplace(
                            stage_descriptor,
                            name,
                            output_descriptor,
                            name,
                        )
                    except FileExistsError as exc:
                        raise VerificationBlocked(
                            "promotion target raced commit:" + name
                        ) from exc
                    os.fsync(output_descriptor)
                os.fsync(stage_descriptor)
            finally:
                os.close(stage_descriptor)
        os.fsync(output_descriptor)
        for name in ordered:
            read_local_output(
                resolved,
                name,
                artifacts[name],
                output_snapshots,
                "published promotion:" + name,
            )
        assert_snapshot_map(output_snapshots, "promotion output")
        assert_snapshot_map(SOURCE_SNAPSHOTS, "source after promotion")
        assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate after promotion")
    finally:
        need(
            bound
            == directory_identity(os.fstat(output_descriptor))
            == directory_identity(os.lstat(resolved)),
            "promotion directory swapped",
        )
        fcntl.flock(output_descriptor, fcntl.LOCK_UN)
        os.close(output_descriptor)


def resolve_inert_source(path: Path, basename: str, label: str) -> Path:
    need(
        path.name == basename
        and os.path.lexists(path)
        and not path.is_symlink()
        and stat.S_ISREG(os.lstat(path).st_mode)
        and os.lstat(path).st_nlink == 1,
        label + " regular single-link basename",
    )
    lexical = path.absolute()
    resolved = path.resolve()
    need(
        lexical == resolved and ROOT.resolve() in resolved.parents,
        label + " root/symlink boundary",
    )
    return resolved


def verify_candidate(
    candidate_dir: Path,
    producer_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    # This complete cacheless reconstruction occurs before any candidate or
    # producer output is opened.
    expected, expected_result = build_expected_artifacts()
    resolved_candidate = resolve_candidate_directory(candidate_dir)
    resolved_producer = resolve_inert_source(
        producer_path,
        CANDIDATE_FILES["producer"],
        "producer",
    )
    require_formal_runtime_input(resolved_producer, "frozen producer")
    validate_inert_producer_access_plan(("fd-bound-byte-read", "sha256"))
    producer_sha256 = stable_file_sha256(
        resolved_producer,
        resolved_producer.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="inert producer bytes",
    )
    need(producer_sha256 == FINAL_PRODUCER_SHA256, "frozen producer pin")
    verifier_path = resolve_inert_source(
        Path(__file__),
        VERIFIER_FILENAME,
        "verifier",
    )
    verifier_sha256 = stable_file_sha256(
        verifier_path,
        verifier_path.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="verifier runtime self hash",
    )
    candidate = read_candidate_bundle(resolved_candidate, expected)
    _, candidate_result = validate_artifact_bundle(candidate, expected)
    candidate_pins = {
        name: hashlib.sha256(raw).hexdigest()
        for name, raw in candidate.items()
    }
    expected_pins = {
        name: hashlib.sha256(raw).hexdigest()
        for name, raw in expected.items()
    }
    need(candidate_pins == expected_pins, "candidate/expected pin map")
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source before attacks")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate before attacks")
    baseline_pins = {
        CANDIDATE_FILES["producer"]: producer_sha256,
        **candidate_pins,
    }
    attacks = build_attack_suite(expected, baseline_pins, verifier_sha256)
    attack_raw = canonical(attacks)
    attack_file_sha256 = hashlib.sha256(attack_raw).hexdigest()
    attack_rows = attacks["attack_rows"]
    need(
        attacks["mechanism_count"] == len(ATTACK_MECHANISMS)
        and attacks["fixture_count"] == len(ATTACK_MECHANISMS)
        and attacks["rejected_count"] == len(ATTACK_MECHANISMS)
        and attacks["coherently_resigned_fixture_count"]
        == EXPECTED_COHERENTLY_RESIGNED_FIXTURES
        and attacks["all_rejected"] is True
        and all(row["rejected"] is True for row in attack_rows),
        "complete attack-suite census",
    )
    payload = {
        "schema": VERIFICATION_SCHEMA,
        "status": "PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION",
        "producer": {
            "filename": CANDIDATE_FILES["producer"],
            "file_sha256": producer_sha256,
            "treated_as_inert_bytes_only": True,
            "imported_executed_parsed_or_tokenized": False,
        },
        "verifier": {
            "filename": VERIFIER_FILENAME,
            "file_sha256": verifier_sha256,
            "self_hash_computed_at_runtime_without_circular_source_pin": True,
        },
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "candidate_opened_only_after_complete_expected_bytes": True,
        "candidate_exact_file_pins": dict(sorted(candidate_pins.items())),
        "independently_rebuilt_expected_file_pins": dict(
            sorted(expected_pins.items())
        ),
        "exact_scope_census": {
            "complete_Round300A_pair_count": 3_232,
            "complete_Round300A_endpoint_count": 4_892,
            "prior_R295A_witnessed_same_component_count": 128,
            "unwitnessed_reclosed_count": 2_080,
            "residual_cross_component_pair_count": 1_024,
            "residual_distinct_endpoint_count": 2_048,
            "complete_pair_set_sha256": COMPLETE_PAIR_SET_SHA256,
            "complete_endpoint_set_sha256": COMPLETE_ENDPOINT_SET_SHA256,
            "prior_witnessed_pair_set_sha256": PRIOR_WITNESSED_PAIR_SET_SHA256,
            "residual_pair_set_sha256": RESIDUAL_PAIR_SET_SHA256,
            "residual_endpoint_set_sha256": RESIDUAL_ENDPOINT_SET_SHA256,
            "legacy_Round304_projection_sha256":
                LEGACY_REPROJECTION_ROWS_SHA256,
            "occurrence_member_binding_keyset_contract": (
                "EVERY_CANDIDATE_OCCURRENCE_MATCHES_EXPECTED_BINDING__"
                "COMPLETE_ENDPOINT_SET_COMMITMENT_SUPPLIES_EXACT_KEYSET"
            ),
        },
        "attack_suite": {
            "filename": ATTACK_FILENAME,
            "file_sha256": attack_file_sha256,
            "attack_suite_sha256": attacks["attack_suite_sha256"],
            "mechanism_count": attacks["mechanism_count"],
            "fixture_count": attacks["fixture_count"],
            "rejected_count": attacks["rejected_count"],
            "category_counts": attacks["category_counts"],
            "coherently_resigned_fixture_count":
                attacks["coherently_resigned_fixture_count"],
            "attack_rows_sha256": attacks["attack_rows_sha256"],
            "all_rejected": True,
        },
        "strict_zero_downstream_credit": {
            **{field: 0 for field in DOWNSTREAM_CREDIT_FIELDS},
            "Gate5_complete_18_field_block_count": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
        "all_source_and_candidate_PRE_POST_fd_identities_equal": True,
        "verification_built_only_after_candidate_and_attacks_passed": True,
        "atomic_promotion_pair": {
            "attack_suite_is_required_first": True,
            "verification_is_required_last_commit_marker": True,
            "two_target_no_clobber_preflight_required": True,
            "atomic_RENAME_NOREPLACE_required": True,
            "exact_private_stage_orphan_recovery_required_before_retry": True,
        },
        "candidate_result_object_sha256": candidate_result["result_sha256"],
        "formal_Round305A_scope_promotion_permitted": True,
    }
    verification = close_object(payload, "verification_sha256")
    assert_snapshot_map(SOURCE_SNAPSHOTS, "source final")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "candidate final")
    return attacks, verification


def compare_dual_seed_directories(
    directory_a: Path,
    directory_b: Path,
) -> dict[str, Any]:
    expected, _ = build_expected_artifacts()
    pins: dict[str, str] = {}
    for label, directory in (("A", directory_a), ("B", directory_b)):
        resolved = resolve_candidate_directory(directory)
        bundle = read_candidate_bundle(resolved, expected)
        validate_artifact_bundle(bundle, expected)
        for name, raw in bundle.items():
            need(raw == expected[name], "dual seed expected bytes:" + label + ":" + name)
            prior = pins.setdefault(name, hashlib.sha256(raw).hexdigest())
            need(prior == hashlib.sha256(raw).hexdigest(), "dual seed divergence:" + name)
    assert_snapshot_map(SOURCE_SNAPSHOTS, "dual seed source")
    assert_snapshot_map(CANDIDATE_SNAPSHOTS, "dual seed candidate")
    return {
        "schema": RESULT_SCHEMA + ".dual-seed-exact-bytes.v1",
        "status": "PASS_DUAL_SEED_EXACT_BYTES",
        "producer_seeds": [305_001, 305_997],
        "seed_affects_output": False,
        "artifact_sha256": dict(sorted(pins.items())),
        "candidate_outputs_written": False,
    }


def lightweight_boundary_attack_selftest() -> dict[str, bool]:
    """Exercise fail-closed wire/OS helpers without opening heavy inputs."""

    sample = close_object({"schema": "gzip-boundary", "value": 1}, "self_sha256")
    sample_raw = canonical(sample)
    packed = deterministic_gzip(sample)
    need(
        bounded_single_member_gzip(packed, len(sample_raw), "self-test gzip")
        == sample_raw,
        "bounded gzip positive control",
    )
    gzip_concatenation = rejected(lambda: bounded_single_member_gzip(
        packed + packed,
        len(sample_raw),
        "self-test concatenated gzip",
    ))
    compressor = zlib.compressobj(level=9, wbits=31)
    overexpanded = compressor.compress(b"xy") + compressor.flush()
    gzip_overexpansion = rejected(lambda: bounded_single_member_gzip(
        overexpanded,
        1,
        "self-test overexpansion gzip",
    ))
    producer_separation = rejected(lambda: validate_inert_producer_access_plan((
        "import-producer-module",
        "parse-producer-source",
    )))
    temporary_input = rejected(lambda: require_formal_runtime_input(
        ROOT / ("." + "tmp") / "forged",
        "self-test temporary input",
    ))
    commit_order = rejected(lambda: validate_promotion_commit_order((
        VERIFICATION_FILENAME,
        ATTACK_FILENAME,
    )))

    def write_local(path: Path, raw: bytes) -> None:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            os.write(descriptor, raw)
        finally:
            os.close(descriptor)

    with tempfile.TemporaryDirectory(
        prefix=".r305a-light-attack-",
        dir=ROOT,
    ) as raw_directory:
        directory = Path(raw_directory)
        base = directory / "base"
        hard = directory / "hard"
        symbolic = directory / "symbolic"
        write_local(base, b"x")
        os.link(base, hard)
        os.symlink(base.name, symbolic)
        descriptor = os.open(
            directory,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            hardlink = rejected(lambda: safe_regular_at(
                hard.name,
                directory,
                descriptor,
                {},
                10,
                "self-test hardlink",
            ))
            symlink = rejected(lambda: safe_regular_at(
                symbolic.name,
                directory,
                descriptor,
                {},
                10,
                "self-test symlink",
            ))
        finally:
            os.close(descriptor)

        stage = directory / "stage"
        stage.mkdir(mode=0o700)
        write_local(stage / "source", b"source")
        write_local(directory / "target", b"target")
        stage_descriptor = os.open(
            stage,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        target_descriptor = os.open(
            directory,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            noreplace_race = rejected(lambda: rename_noreplace(
                stage_descriptor,
                "source",
                target_descriptor,
                "target",
            ))
        finally:
            os.close(stage_descriptor)
            os.close(target_descriptor)

        bound = directory / "bound"
        write_local(bound, b"before")
        before = file_identity(os.lstat(bound))
        os.unlink(bound)
        write_local(bound, b"after-and-different")
        identity_drift = rejected(lambda: need(
            file_identity(os.lstat(bound)) == before,
            "self-test identity drift",
        ))

    outcomes = {
        "gzip_concatenation": gzip_concatenation,
        "gzip_overexpansion": gzip_overexpansion,
        "producer_separation": producer_separation,
        "temporary_input": temporary_input,
        "commit_order": commit_order,
        "hardlink": hardlink,
        "symlink": symlink,
        "noreplace_race": noreplace_race,
        "identity_drift": identity_drift,
    }
    need(all(outcomes.values()), "lightweight boundary attack self-test")
    return outcomes


def self_test() -> dict[str, Any]:
    path = resolve_inert_source(Path(__file__), VERIFIER_FILENAME, "self-test verifier")
    raw = stable_read_bytes(
        path,
        path.parent,
        SOURCE_SNAPSHOTS,
        maximum=5_000_000,
        label="self-test verifier bytes",
    )
    forbidden = (
        b"os" + b".replace",
        b"import" + b" pickle",
        b"from" + b" pickle",
        b"__py" + b"cache__",
        b"." + b"tmp/",
    )
    need(all(item not in raw for item in forbidden), "forbidden source mechanism")
    sample = close_object({"schema": "self-test", "value": 1}, "self_sha256")
    packed = deterministic_gzip(sample)
    need(
        strict_object(canonical(sample), "self-test canonical") == sample
        and deterministic_gzip(sample) == packed
        and len(EXACT_ROW_FIELDS) == 31
        and len(EXACT_LEDGER_FIELDS) == 29
        and len(EXACT_RESULT_FIELDS) == 14
        and SCHEMA_SNAPSHOT_SHA256 == FROZEN_SCHEMA_SNAPSHOT_SHA256
        and PIN.fullmatch(FINAL_PRODUCER_SHA256) is not None
        and len(ATTACK_MECHANISMS) == len(set(ATTACK_MECHANISMS)),
        "lightweight self-test contract",
    )
    category_counts = dict(sorted(Counter(
        ATTACK_CATEGORY_BY_MECHANISM.values()
    ).items()))
    need(
        set(ATTACK_CATEGORY_BY_MECHANISM) == set(ATTACK_MECHANISMS)
        and category_counts == EXPECTED_ATTACK_CATEGORY_COUNTS,
        "lightweight attack taxonomy self-test",
    )
    boundary_attacks = lightweight_boundary_attack_selftest()
    assert_snapshot_map(SOURCE_SNAPSHOTS, "self-test source")
    return {
        "schema": RESULT_SCHEMA + ".verifier-self-test.v1",
        "status": "PASS_LIGHTWEIGHT_FAIL_CLOSED_SELF_TEST",
        "producer_file_sha256_pin": FINAL_PRODUCER_SHA256,
        "verifier_runtime_file_sha256": hashlib.sha256(raw).hexdigest(),
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "exact_field_counts": {"row": 31, "ledger": 29, "result": 14},
        "attack_mechanism_count": len(ATTACK_MECHANISMS),
        "attack_fixture_count": len(ATTACK_MECHANISMS),
        "expected_coherently_resigned_fixture_count":
            EXPECTED_COHERENTLY_RESIGNED_FIXTURES,
        "attack_category_counts": category_counts,
        "lightweight_boundary_attack_rejections": boundary_attacks,
        "deterministic_single_member_gzip": True,
        "candidate_opened": False,
        "upstream_heavy_ledger_opened": False,
        "formal_artifact_written": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--producer-path", type=Path)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dual-seed-dir-a", type=Path)
    parser.add_argument("--dual-seed-dir-b", type=Path)
    args = parser.parse_args()
    if args.root is not None:
        configure_root(args.root)
    if args.self_test:
        need(
            args.candidate_dir is None
            and args.producer_path is None
            and args.dual_seed_dir_a is None
            and args.dual_seed_dir_b is None,
            "self-test conflicts with candidate options",
        )
        print(canonical(self_test()).decode("ascii"))
        return
    if args.dual_seed_dir_a is not None or args.dual_seed_dir_b is not None:
        need(
            args.dual_seed_dir_a is not None
            and args.dual_seed_dir_b is not None
            and args.candidate_dir is None
            and args.producer_path is None,
            "dual seed requires exactly two directories",
        )
        print(canonical(compare_dual_seed_directories(
            args.dual_seed_dir_a,
            args.dual_seed_dir_b,
        )).decode("ascii"))
        return
    need(args.candidate_dir is not None, "--candidate-dir required")
    producer_path = (
        args.producer_path
        if args.producer_path is not None
        else args.candidate_dir / CANDIDATE_FILES["producer"]
    )
    attacks, verification = verify_candidate(args.candidate_dir, producer_path)
    attack_raw = canonical(attacks)
    verification_raw = canonical(verification)
    if args.no_write:
        summary = {
            "schema": RESULT_SCHEMA + ".no-write-exact-output-hashes.v1",
            "status": verification["status"],
            "attack_suite": {
                "filename": ATTACK_FILENAME,
                "file_sha256": hashlib.sha256(attack_raw).hexdigest(),
                "object_sha256": attacks["attack_suite_sha256"],
            },
            "verification": {
                "filename": VERIFICATION_FILENAME,
                "file_sha256": hashlib.sha256(verification_raw).hexdigest(),
                "object_sha256": verification["verification_sha256"],
            },
            "candidate_and_promotion_outputs_written": False,
        }
        print(canonical(summary).decode("ascii"))
        return
    publish_attack_then_verification(
        args.candidate_dir,
        attack_raw,
        verification_raw,
    )
    print(verification_raw.decode("ascii"))


if __name__ == "__main__":
    main()
