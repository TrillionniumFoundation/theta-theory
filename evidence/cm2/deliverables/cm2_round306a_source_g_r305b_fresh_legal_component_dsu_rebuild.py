#!/usr/bin/env python3
"""Round306A: fresh legal-component DSU rebuild with the sealed Round305B edges.

This producer deliberately replays the complete source member and edge universe
through the SHA-pinned Round304 engine.  It never loads the serialized Round304
member/component ledger as DSU state.  The Round304 quotient is reconstructed
only as an in-memory checkpoint used to lift the eight independently admitted
Round305B quotient edges back to exact occurrence/base-root pairs.

The generated batch is a zero-credit candidate until an independent Round306A
verifier publishes its final verification marker.  In particular, this round
does not claim full maximality: it reprojections the complete 3,232-row R300A
frontier, but leaves transformed-face, cross-chart, retained/event, and
occurrence-fibre exhaustion as explicit downstream blockers.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Iterator


def discover_root(source: Path) -> Path:
    for candidate in (source.resolve().parent, *source.resolve().parents):
        if (candidate / "deliverables").is_dir() and (
            candidate / ".venv-cm2"
        ).is_dir():
            return candidate
    raise RuntimeError("workspace root not found")


ROOT = discover_root(Path(__file__))
DATA = ROOT / "deliverables"
PREFIX = "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild"
SCHEMA = "cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1"
SEED_A = 306_101
SEED_B = 306_997

FILES = {
    "edge": PREFIX + "_edge_application_ledger.json.gz",
    "member": PREFIX + "_member_component_ledger.json.gz",
    "promoted": PREFIX + "_r305b_promoted_edge_application_ledger.json.gz",
    "frontier": PREFIX + "_r300a_reprojection_ledger.json.gz",
    "wtail": PREFIX + "_wtail_disposition_ledger.json.gz",
    "residual": PREFIX + "_residual_gate_ledger.json.gz",
    "result": PREFIX + "_result.json",
}
TABLES = {
    "edge": "fresh_edge_application_rows",
    "member": "fresh_member_component_rows",
    "promoted": "Round305B_promoted_edge_application_rows",
    "frontier": "Round300A_complete_reprojection_rows",
    "wtail": "W_tail_disposition_rows",
    "residual": "residual_gate_rows",
}
ID_FIELDS = {
    "edge": "Round306A_fresh_edge_application_row_id",
    "member": "Round306A_fresh_member_component_row_id",
    "promoted": "Round306A_Round305B_promoted_edge_application_row_id",
    "frontier": "Round306A_Round300A_reprojection_row_id",
    "wtail": "Round306A_W_tail_disposition_row_id",
    "residual": "Round306A_residual_gate_row_id",
}

R304_ENGINE = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild.py"
)
R304_ENGINE_SHA256 = (
    "fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5"
)
R304_MANIFEST = (
    "cm2_round304_source_g_fresh_extended_registry_legal_component_dsu_rebuild_manifest.sha256"
)
R304_MANIFEST_SHA256 = (
    "de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c"
)
R304_PARTITION_SHA256 = (
    "72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff"
)

R305B_PREFIX = (
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion"
)
R305B_MANIFEST = R305B_PREFIX + "_manifest.sha256"
R305B_MANIFEST_SHA256 = (
    "1b80e7470e1ad1893f9323f47c64bd0d1aa48b35e0920c0821b25fe316b7dca7"
)
R305B_PHYSICAL = R305B_PREFIX + "_physical_witness_ledger.json.gz"
R305B_EDGE = R305B_PREFIX + "_canonical_component_edge_ledger.json.gz"
R305B_RESULT = R305B_PREFIX + "_result.json"
R305B_VERIFICATION = R305B_PREFIX + "_verification.json"
R305B_ATTACK = R305B_PREFIX + "_attack_suite.json"
R305B_MANIFEST_PINS = {
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion.py": "bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b",
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_wire_spec.json": "8cd6cbcd936875885b76fe501f76bf949e81233c07d75f715c003beb021ef573",
    "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_wire_contract_fixture.json": "c2695472d522f1a24a2b8b7bbea0dff6e2c932b5dc63f154b27c6887b02e3f02",
    R305B_PHYSICAL: "629b8501e73c1e7bec9a9e21b1a27a4ca6021f9574c79caf83910ec25f3f95fb",
    R305B_PREFIX + "_anchor_ledger.json.gz": "491a696e582bce2c1fe57692e62caf461073812adec953a1bf46d8d7da2423df",
    R305B_PREFIX + "_closure_contact_ledger.json.gz": "19a25d6b462eb13522ed285cf447421410c5a4958642d59106c4cc1dcb58d0bd",
    R305B_PREFIX + "_owner_locus_ledger.json.gz": "9cf42df2be1994a5669c52732434a9823cef7c1532ea86175c8e8996b44ce690",
    R305B_EDGE: "cf56d9b57cd972a2a3272ea465f83f6fadbc3c7ed6962cb70809f19e44addb27",
    R305B_RESULT: "fcc18e0f0c2b05ca06c0c075521e50f00d5fe18bb1f39d853157f5c63cca3932",
    R305B_PREFIX + "_verifier.py": "39e2514d7617bd7e638cf2739dcc40bca3be356802654800499f5065bad29bf9",
    R305B_ATTACK: "b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735",
    R305B_VERIFICATION: "4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9",
    R305B_PREFIX + "_report.md": "3e8ac390bd4c12a5609b0c4de9c6589d912517cda5ab6ddd772e0028cb3bedbb",
    R305B_PREFIX + "_cold_replay.md": "9b59bfce5e41f93eb87f90d629d499cd6da27245db5dfd1f13bbd90d7d6eeecf",
}
R305B_PRODUCER = R305B_PREFIX + ".py"
R305B_WIRE = R305B_PREFIX + "_wire_spec.json"
R305B_FIXTURE = R305B_PREFIX + "_wire_contract_fixture.json"
R305B_ANCHOR = R305B_PREFIX + "_anchor_ledger.json.gz"
R305B_CONTACT = R305B_PREFIX + "_closure_contact_ledger.json.gz"
R305B_OWNER = R305B_PREFIX + "_owner_locus_ledger.json.gz"
R305B_VERIFIER = R305B_PREFIX + "_verifier.py"
R305B_REPORT = R305B_PREFIX + "_report.md"
R305B_COLD_REPLAY = R305B_PREFIX + "_cold_replay.md"
R305B_CANDIDATE_FILES = (
    R305B_PHYSICAL,
    R305B_ANCHOR,
    R305B_CONTACT,
    R305B_OWNER,
    R305B_EDGE,
    R305B_RESULT,
)
R305B_LEDGER_FIELDS = frozenset({
    "schema", "status", "every_row_closed_by_own_sha256", "formal_credit",
    "row_count", "row_ids_sha256", "row_hashes_sha256", "rows_sha256",
    "rows", "ledger_sha256",
})
R305B_PHYSICAL_ROW_SCHEMA = (
    "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
    "component-edge-promotion.v1.physical-witness-row.v1"
)
R305B_EDGE_ROW_SCHEMA = (
    "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
    "component-edge-promotion.v1.canonical-component-edge-row.v1"
)
R305B_PHYSICAL_LEDGER_SCHEMA = (
    "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
    "component-edge-promotion.v1.physical-witness-ledger.v1"
)
R305B_EDGE_LEDGER_SCHEMA = (
    "cm2.round305b.source-g-r305a-two-sided-physical-inclusion-"
    "component-edge-promotion.v1.canonical-component-edge-ledger.v1"
)
R305B_LEDGER_STATUS = (
    "PASS_ZERO_CREDIT_CANDIDATE_LEDGER__PUBLISHED_OR_STAGED__"
    "PENDING_INDEPENDENT_VERIFICATION"
)
R305B_PHYSICAL_FIELDS = frozenset({
    "Round305B_physical_witness_row_id", "schema",
    "source_Round305A_scope_reprojection_row_id",
    "source_Round305A_scope_reprojection_row_sha256",
    "source_Round300A_row_id", "source_Round300A_row_sha256",
    "canonical_registry_occurrence_pair", "Round304_final_component_pair",
    "official_key_pair", "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "proof_core_patch_id", "owner_extension_patch_id", "active_function_id",
    "guard_id", "branch_id", "exact_relative_physical_domain",
    "exact_graph_Gamma", "anchor_row_ids", "anchor_row_sha256s",
    "closure_contact_row_ids", "closure_contact_row_sha256s",
    "owner_locus_row_ids", "owner_locus_row_sha256s",
    "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis",
    "G0_exact_provenance_pins_and_row_closures",
    "G1_endpoint_occurrence_connected_supports",
    "G2_nonempty_connected_included_lower_stratum",
    "G3_left_closure_attaches_to_included_patch",
    "G4_right_closure_attaches_to_included_patch",
    "G5_endpoint_patch_provenance_exactly_closed",
    "relative_physical_closure_limit_lemma_id",
    "corridor_box_used_as_Gamma_intersection", "D4_transfer_used",
    "candidate_physical_connectivity_conclusion",
    "formal_physical_witness_credit", "formal_component_edge_credit",
    "formal_DSU_rank_reduction_credit", "formal_maximality_credit",
    "formal_fibre_credit", "formal_global_disposition_credit", "row_sha256",
})
R305B_EDGE_FIELDS = frozenset({
    "Round305B_canonical_component_edge_row_id", "schema",
    "canonical_Round304_final_component_pair", "physical_witness_row_count",
    "physical_witness_row_ids_sha256", "physical_witness_row_sha256s_sha256",
    "canonical_occurrence_pairs_sha256", "canonical_official_key_pair",
    "cross_official_key_physical_edge_permitted",
    "occurrence_identity_collapsed", "official_key_identity_merged",
    "all_128_witnesses_satisfy_G0_G5",
    "deduplicated_from_witness_rows_not_union_rows",
    "formal_component_edge_credit", "eligible_for_later_fresh_DSU_application",
    "formal_DSU_rank_reduction_credit", "row_sha256",
})

EXPECTED_PARTITION_SHA256 = (
    "a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c"
)

ENCODER = json.JSONEncoder(
    ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
)
FileIdentity = tuple[int, int, int, int, int, int, int]
DirectoryIdentity = tuple[int, int, int]
INPUT_SNAPSHOTS: dict[Path, FileIdentity] = {}
PARENT_DIRECTORY_SNAPSHOTS: dict[Path, DirectoryIdentity] = {}
RAW_INPUT_CACHE: dict[Path, bytes] = {}


class BuildBlocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise BuildBlocked(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_identity(info: os.stat_result) -> FileIdentity:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def directory_identity(info: os.stat_result) -> DirectoryIdentity:
    return (info.st_dev, info.st_ino, info.st_mode)


def lexical_directory_without_symlinks(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        need(os.path.lexists(current), label + ":missing:" + part)
        info = os.lstat(current)
        need(
            stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
            label + ":symlink-or-nondirectory:" + part,
        )
    return absolute


def open_bound_directory(directory: Path, label: str) -> tuple[Path, int]:
    lexical = lexical_directory_without_symlinks(directory, label + ":parent")
    descriptor = os.open(
        lexical,
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    actual = directory_identity(os.fstat(descriptor))
    need(actual == directory_identity(os.lstat(lexical)), label + ":open-race")
    prior = PARENT_DIRECTORY_SNAPSHOTS.setdefault(lexical, actual)
    need(prior == actual, label + ":parent-identity-drift")
    return lexical, descriptor


def safe_regular_at(
    name: str,
    directory: Path,
    directory_descriptor: int,
    maximum: int,
    label: str,
) -> FileIdentity:
    need(name not in {"", ".", ".."} and Path(name).name == name, label)
    info = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    need(
        stat.S_ISREG(info.st_mode)
        and not stat.S_ISLNK(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        label + ":nonregular-hardlink-or-unbounded",
    )
    identity = file_identity(info)
    path = directory / name
    prior = INPUT_SNAPSHOTS.setdefault(path, identity)
    need(prior == identity, label + ":PRE-POST-identity-drift")
    return identity


@contextmanager
def fd_bound_binary(
    path: Path,
    *,
    maximum: int = 3_000_000_000,
    label: str,
) -> Iterator[BinaryIO]:
    lexical, directory_descriptor = open_bound_directory(path.parent, label)
    descriptor: int | None = None
    stream: BinaryIO | None = None
    try:
        absolute = Path(os.path.abspath(os.fspath(path)))
        need(absolute.parent == lexical, label + ":path-escape")
        expected = safe_regular_at(
            absolute.name, lexical, directory_descriptor, maximum, label,
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
        need(file_identity(os.fstat(stream.fileno())) == expected,
             label + ":file-open-race")
        yield stream
        need(file_identity(os.fstat(stream.fileno())) == expected,
             label + ":fd-identity-drift")
        current = os.stat(
            absolute.name, dir_fd=directory_descriptor, follow_symlinks=False,
        )
        need(file_identity(current) == expected, label + ":filename-swap")
        need(
            directory_identity(os.fstat(directory_descriptor))
            == PARENT_DIRECTORY_SNAPSHOTS[lexical]
            == directory_identity(os.lstat(lexical)),
            label + ":parent-swap",
        )
    finally:
        if stream is not None:
            stream.close()
        elif descriptor is not None:
            os.close(descriptor)
        os.close(directory_descriptor)


def stable_read_bytes(
    path: Path,
    *,
    maximum: int = 3_000_000_000,
) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    cached = RAW_INPUT_CACHE.get(absolute)
    if cached is not None:
        lexical, descriptor = open_bound_directory(absolute.parent, "cached-input")
        try:
            need(absolute.parent == lexical, "cached-input:path-escape")
            safe_regular_at(
                absolute.name, lexical, descriptor, maximum, "cached-input",
            )
        finally:
            os.close(descriptor)
        return cached
    chunks: list[bytes] = []
    total = 0
    with fd_bound_binary(
        absolute, maximum=maximum, label="stable-input:" + absolute.name,
    ) as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "stable-input:bounded:" + absolute.name)
            chunks.append(block)
    raw = b"".join(chunks)
    RAW_INPUT_CACHE[absolute] = raw
    return raw


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with fd_bound_binary(path, label="input-hash:" + path.name) as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def assert_input_snapshots_unchanged() -> None:
    for path, expected in sorted(INPUT_SNAPSHOTS.items(), key=lambda item: str(item[0])):
        need(os.path.lexists(path) and not path.is_symlink(),
             "input snapshot disappeared:" + path.name)
        need(file_identity(os.lstat(path)) == expected,
             "input snapshot changed:" + path.name)
    for directory, expected in sorted(
        PARENT_DIRECTORY_SNAPSHOTS.items(), key=lambda item: str(item[0])
    ):
        lexical = lexical_directory_without_symlinks(directory, "snapshot-parent")
        need(directory_identity(os.lstat(lexical)) == expected,
             "input parent changed:" + directory.name)


ROW_SCHEMAS = {
    key: SCHEMA + "." + suffix for key, suffix in {
        "edge": "fresh-edge-application-row.v1",
        "member": "fresh-member-component-row.v1",
        "promoted": "r305b-promoted-edge-application-row.v1",
        "frontier": "r300a-reprojection-row.v1",
        "wtail": "wtail-disposition-row.v1",
        "residual": "residual-gate-row.v1",
    }.items()
}
ROW_FIELDS = {
    "edge": frozenset({
        ID_FIELDS["edge"], "schema", "application_index", "source_channel",
        "source_row_id", "source_row_sha256",
        "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
        "fed_to_new_empty_DSU", "forward_rank_reduction",
        "forward_cycle_or_redundant", "candidate_DSU_rank_reduction",
        "serialized_Round304_partition_used_as_state",
        "formal_credit_without_independent_verification_marker",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "row_sha256",
    }),
    "member": frozenset({
        ID_FIELDS["member"], "schema", "registry_occurrence_id", "base_root_id",
        "official_key_id", "final_component_id", "member_identity_preserved",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "row_sha256",
    }),
    "promoted": frozenset({
        ID_FIELDS["promoted"], "schema", "promoted_edge_index",
        "source_Round305B_component_edge_row_id",
        "source_Round305B_component_edge_row_sha256",
        "source_Round305B_selected_physical_witness_row_id",
        "source_Round305B_selected_physical_witness_row_sha256",
        "selection_rule", "Round304_fresh_checkpoint_component_pair",
        "selected_occurrence_pair", "projected_base_root_pair",
        "official_key_pair", "cross_checkpoint_components_before_application",
        "forward_rank_reduction", "witness_rows_are_not_union_rows",
        "formal_official_key_merge_credit",
        "formal_occurrence_identity_collapse_credit",
        "formal_credit_without_independent_verification_marker", "row_sha256",
    }),
    "frontier": frozenset({
        ID_FIELDS["frontier"], "schema", "source_Round300A_row_id",
        "source_Round300A_row_sha256", "canonical_occurrence_pair",
        "projected_base_root_pair", "Round306A_final_component_pair",
        "same_Round306A_final_component", "prior_R295A_witness_present",
        "source_Round305B_physical_witness_row_id",
        "source_Round305B_physical_witness_row_sha256", "disposition",
        "Round300A_frontier_residual_credit", "formal_full_maximality_credit",
        "row_sha256",
    }),
    "wtail": frozenset({
        ID_FIELDS["wtail"], "schema", "source_W_tail_row_id",
        "source_W_tail_row_sha256", "source_Round300D_row_id",
        "canonical_occurrence_endpoint_pair", "projected_base_root_pair",
        "Round306A_final_component_pair", "same_Round306A_final_component",
        "disposition", "stronger_legal_path", "source_row_fed_to_DSU",
        "formal_component_edge_credit", "formal_maximality_credit", "row_sha256",
    }),
    "residual": frozenset({
        ID_FIELDS["residual"], "schema", "Round300A_complete_pair_count",
        "Round300A_cross_component_residual_count",
        "Round305B_physical_witness_rows_consumed_as_edge_provenance",
        "Round305B_canonical_component_edge_applications",
        "Round305B_rank_reductions", "transformed_face_exhaustion_proved",
        "cross_chart_exhaustion_proved", "retained_event_exhaustion_proved",
        "occurrence_fibre_exhaustion_proved", "full_maximality_proved",
        "formal_maximality_credit", "formal_fibre_credit",
        "formal_global_disposition_credit", "D02_status", "CM2_status",
        "row_sha256",
    }),
}
LEDGER_FIELDS = frozenset({
    "schema", "schema_snapshot_sha256", "status", "row_count",
    "row_ids_sha256", "row_hashes_sha256", "rows_sha256",
    "ledger_sha256",
})
RESULT_FIELDS = frozenset({
    "schema", "schema_snapshot_sha256", "status", "producer_file_sha256",
    "frozen_Round304_engine", "Round305B_seal", "member_universe",
    "fresh_source_reconstruction_chain", "fresh_Round304_checkpoint",
    "fresh_forward_application", "fresh_reverse_application",
    "forward_reverse_same_partition", "Round305B_edge_application",
    "Round300A_reprojection", "full_maximality_gate",
    "formal_credit_without_independent_verification_marker",
    "candidate_credit_if_independently_verified", "output_ledgers",
    "seed_affects_output", "D02_status", "CM2_status", "result_sha256",
})
SCHEMA_SNAPSHOT = {
    "schema": SCHEMA + ".schema-snapshot.v1",
    "output_files": FILES,
    "tables": TABLES,
    "id_fields": ID_FIELDS,
    "row_schemas": ROW_SCHEMAS,
    "row_fields": {
        key: sorted(fields) for key, fields in sorted(ROW_FIELDS.items())
    },
    "ledger_fields_excluding_table": sorted(LEDGER_FIELDS),
    "result_fields": sorted(RESULT_FIELDS),
    "upstream_Round305B_physical_row_schema": R305B_PHYSICAL_ROW_SCHEMA,
    "upstream_Round305B_physical_fields": sorted(R305B_PHYSICAL_FIELDS),
    "upstream_Round305B_edge_row_schema": R305B_EDGE_ROW_SCHEMA,
    "upstream_Round305B_edge_fields": sorted(R305B_EDGE_FIELDS),
}
SCHEMA_SNAPSHOT_SHA256 = digest(SCHEMA_SNAPSHOT)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         label + ":raw-json-boundary")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, label + ":duplicate-key:" + key)
            out[key] = value
        return out

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            BuildBlocked(label + ":float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            BuildBlocked(label + ":constant:" + token)
        ),
    )
    need(type(value) is dict, label + ":object")
    return value


def strict_json(name: str) -> dict[str, Any]:
    return strict_json_bytes(stable_read_bytes(DATA / name), name)


def check_self(document: dict[str, Any], field: str, label: str) -> None:
    need(type(document.get(field)) is str, label + ":self-field")
    payload = dict(document)
    expected = payload.pop(field)
    need(digest(payload) == expected, label + ":self-hash")


def parse_manifest(name: str, expected_sha: str) -> dict[str, str]:
    path = DATA / name
    raw = stable_read_bytes(path, maximum=10_000_000)
    need(hashlib.sha256(raw).hexdigest() == expected_sha, name + ":file-pin")
    output: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2, name + ":line")
        pin, member = pieces
        need(
            len(pin) == 64
            and all(ch in "0123456789abcdef" for ch in pin)
            and member not in output
            and Path(member).name == member,
            name + ":member",
        )
        output[member] = pin
    return output


def validate_round305b_seal() -> dict[str, str]:
    entries = parse_manifest(R305B_MANIFEST, R305B_MANIFEST_SHA256)
    need(entries == R305B_MANIFEST_PINS, "Round305B exact 14-member manifest")
    for name, expected in entries.items():
        need(file_sha256(DATA / name) == expected, "Round305B member:" + name)
    verification = strict_json(R305B_VERIFICATION)
    check_self(verification, "verification_sha256", R305B_VERIFICATION)
    expected_candidate_pins = {
        name: entries[name] for name in R305B_CANDIDATE_FILES
    }
    need(
        verification["status"]
        == "PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_INCLUSION_COMPONENT_EDGE_PROMOTION"
        and verification["formal_Round305B_promotion_permitted"] is True
        and verification["producer"] == {
            "filename": R305B_PRODUCER,
            "file_sha256": entries[R305B_PRODUCER],
            "imported_executed_parsed_or_tokenized": False,
            "treated_as_inert_pinned_bytes_only": True,
        }
        and verification["runtime_verifier"] == {
            "filename": R305B_VERIFIER,
            "file_sha256": entries[R305B_VERIFIER],
            "sha256_computed_from_runtime_file_bytes": True,
            "source_contains_no_verifier_self_pin": True,
        }
        and verification["attack_suite"]["attack_count"] == 99
        and verification["attack_suite"]["rejected_count"] == 99
        and verification["attack_suite"]["all_rejected"] is True
        and verification["attack_suite"]["filename"] == R305B_ATTACK
        and verification["attack_suite"]["file_sha256"] == entries[R305B_ATTACK]
        and verification["candidate"]["exact_file_sha256s"]
        == expected_candidate_pins
        and verification["candidate"]["exact_six_file_set"]
        == list(R305B_CANDIDATE_FILES)
        and verification["candidate"]["all_six_files_equal_independently_rebuilt_bytes"]
        is True
        and verification["candidate"]["opened_only_after_full_independent_reconstruction"]
        is True
        and verification["candidate"]["candidate_outputs_written_or_replaced_during_admission"]
        is False,
        "Round305B independent admission marker",
    )
    need(
        verification["formal_credit_without_verification_commit_marker"]
        == {
            "formal_DSU_rank_reduction_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_maximality_credit": 0,
            "officially_admitted_anchor_binding_credit": 0,
            "officially_admitted_component_edge_credit": 0,
            "officially_admitted_physical_witness_credit": 0,
        },
        "Round305B sole-marker pre-credit boundary",
    )
    credit = verification[
        "formal_credit_transition_at_this_verification_commit_marker"
    ]
    need(
        credit
        == {
            "formal_DSU_rank_reduction_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "formal_maximality_credit": 0,
            "officially_admitted_anchor_binding_credit": 2048,
            "officially_admitted_component_edge_credit": 8,
            "officially_admitted_physical_witness_credit": 1024,
        },
        "Round305B exact credit marker",
    )
    attack = strict_json(R305B_ATTACK)
    check_self(attack, "attack_suite_sha256", R305B_ATTACK)
    need(
        verification["attack_suite"]["object_self_sha256"]
        == attack["attack_suite_sha256"]
        and verification["attack_suite"]["canonical_object_sha256"]
        == entries[R305B_ATTACK],
        "Round305B exact attack binding",
    )
    result = strict_json(R305B_RESULT)
    check_self(result, "result_sha256", R305B_RESULT)
    need(
        result["status"]
        == "PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__PENDING_INDEPENDENT_VERIFICATION__ZERO_OFFICIALLY_ADMITTED_CREDIT",
        "Round305B zero-credit candidate result boundary",
    )
    need(
        verification["candidate"]["independent_expected_result_sha256"]
        == result["result_sha256"]
        and verification["strict_credit_boundary"] == {
            "CM2_status": "NO-GO_FOR_CLAIM",
            "D02_status": "BLOCKED",
            "Source_G_global_dispositions_completed": 0,
            "anchor_binding_rows_promoted": 2048,
            "canonical_component_edges_promoted": 8,
            "fresh_DSU_rebuild_performed": False,
            "maximality_proved": False,
            "official_fibres_exhausted": 0,
            "physical_witness_rows_promoted": 1024,
            "witness_rows_are_not_union_rows": True,
        }
        and verification["atomic_publication_contract"][
            "verification_is_last_and_sole_formal_credit_commit_marker"
        ] is True
        and verification["atomic_publication_contract"]["attack_suite_is_first"]
        is True,
        "Round305B exact sole-marker semantics",
    )
    return entries


def load_engine() -> Any:
    path = DATA / R304_ENGINE
    source = stable_read_bytes(path, maximum=5_000_000)
    need(hashlib.sha256(source).hexdigest() == R304_ENGINE_SHA256,
         "Round304 engine pin")
    name = "_cm2_round304_frozen_engine"
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(path))
    need(spec is not None, "Round304 inert engine spec")
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    module.configure_root(ROOT)
    need(file_sha256(path) == R304_ENGINE_SHA256, "Round304 engine post-import pin")
    return module


def validate_round304_seal() -> dict[str, str]:
    entries = parse_manifest(R304_MANIFEST, R304_MANIFEST_SHA256)
    need(len(entries) == 11 and entries.get(R304_ENGINE) == R304_ENGINE_SHA256,
         "Round304 exact seal")
    for name, expected in entries.items():
        need(file_sha256(DATA / name) == expected, "Round304 member:" + name)
    return entries


def validate_closed_ledger(
    name: str,
    table: str,
    id_field: str,
    expected_count: int,
    ledger_schema: str,
    row_schema: str,
    row_fields: frozenset[str],
) -> list[dict[str, Any]]:
    compressed = stable_read_bytes(DATA / name, maximum=100_000_000)
    chunks: list[bytes] = []
    total = 0
    with gzip.GzipFile(fileobj=io.BytesIO(compressed), mode="rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= 100_000_000, name + ":uncompressed-bound")
            chunks.append(block)
    raw = b"".join(chunks)
    document = strict_json_bytes(raw, name)
    need(
        set(document) == R305B_LEDGER_FIELDS
        and document["schema"] == ledger_schema
        and document["status"] == R305B_LEDGER_STATUS
        and document["every_row_closed_by_own_sha256"] is True
        and document["formal_credit"] == 0,
        name + ":exact-ledger-schema",
    )
    rows = document.get(table)
    need(type(rows) is list and len(rows) == expected_count, name + ":count")
    seen: set[str] = set()
    ids: list[str] = []
    hashes: list[str] = []
    for row in rows:
        need(
            type(row) is dict
            and set(row) == row_fields
            and row.get("schema") == row_schema
            and type(row.get(id_field)) is str,
            name + ":exact-row-schema",
        )
        check_self(row, "row_sha256", name + ":row")
        need(row[id_field] not in seen, name + ":duplicate-row")
        seen.add(row[id_field])
        ids.append(row[id_field])
        hashes.append(row["row_sha256"])
    need(
        document["row_count"] == expected_count
        and document["row_ids_sha256"] == digest(ids)
        and document["row_hashes_sha256"] == digest(hashes)
        and document["rows_sha256"] == digest(rows),
        name + ":list commitments",
    )
    check_self(document, "ledger_sha256", name + ":ledger")
    return rows


@dataclass(frozen=True)
class Lift:
    edge_row_id: str
    edge_row_sha256: str
    component_pair: tuple[str, str]
    witness_row_id: str
    witness_row_sha256: str
    occurrence_pair: tuple[str, str]
    root_pair: tuple[str, str]
    official_key_pair: tuple[str, str]


def build_round305b_lifts(
    engine: Any,
    members: dict[str, Any],
    roots: set[str],
    checkpoint_map: dict[str, str],
    r300a_rows: list[dict[str, Any]],
) -> tuple[list[Any], list[Lift], dict[str, dict[str, Any]]]:
    physical = validate_closed_ledger(
        R305B_PHYSICAL,
        "rows",
        "Round305B_physical_witness_row_id",
        1024,
        R305B_PHYSICAL_LEDGER_SCHEMA,
        R305B_PHYSICAL_ROW_SCHEMA,
        R305B_PHYSICAL_FIELDS,
    )
    edge_rows = validate_closed_ledger(
        R305B_EDGE,
        "rows",
        "Round305B_canonical_component_edge_row_id",
        8,
        R305B_EDGE_LEDGER_SCHEMA,
        R305B_EDGE_ROW_SCHEMA,
        R305B_EDGE_FIELDS,
    )
    r300a_by_id: dict[str, dict[str, Any]] = {}
    expected_physical_sources: set[str] = set()
    checkpoint_histogram: Counter[str] = Counter()
    for source_row in r300a_rows:
        source_id = source_row["Round300A_canonical_occurrence_pair_row_id"]
        pair = source_row["canonical_unordered_Round294_registry_occurrence_ids"]
        need(
            source_id not in r300a_by_id
            and type(pair) is list
            and len(pair) == 2
            and pair == sorted(pair)
            and pair[0] != pair[1]
            and all(item in members for item in pair),
            "fresh Round300A exact source universe",
        )
        r300a_by_id[source_id] = source_row
        root_pair = [engine.project(item, members, roots) for item in pair]
        same = checkpoint_map[root_pair[0]] == checkpoint_map[root_pair[1]]
        prior = source_row["R295A_explicit_lower_graph_sheet_witness_present"]
        need(type(prior) is bool, "Round300A prior witness boolean")
        disposition = (
            "PRIOR_SAME" if prior and same else
            "PRIOR_CROSS" if prior else
            "UNPRIOR_SAME" if same else
            "UNPRIOR_CROSS"
        )
        checkpoint_histogram[disposition] += 1
        if disposition == "UNPRIOR_CROSS":
            expected_physical_sources.add(source_id)
    need(
        len(r300a_by_id) == 3232
        and dict(sorted(checkpoint_histogram.items())) == {
            "PRIOR_SAME": 128,
            "UNPRIOR_CROSS": 1024,
            "UNPRIOR_SAME": 2080,
        }
        and len(expected_physical_sources) == 1024,
        "fresh Round304 checkpoint exact Round300A census",
    )

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_source: dict[str, dict[str, Any]] = {}
    g_fields = (
        "G0_exact_provenance_pins_and_row_closures",
        "G1_endpoint_occurrence_connected_supports",
        "G2_nonempty_connected_included_lower_stratum",
        "G3_left_closure_attaches_to_included_patch",
        "G4_right_closure_attaches_to_included_patch",
        "G5_endpoint_patch_provenance_exactly_closed",
    )
    for row in physical:
        component_pair = tuple(row["Round304_final_component_pair"])
        occurrence_pair = tuple(row["canonical_registry_occurrence_pair"])
        source = row["source_Round300A_row_id"]
        source_row = r300a_by_id.get(source)
        need(
            len(component_pair) == 2
            and list(component_pair) == sorted(component_pair)
            and component_pair[0] != component_pair[1]
            and len(occurrence_pair) == 2
            and list(occurrence_pair) == sorted(occurrence_pair)
            and occurrence_pair[0] != occurrence_pair[1]
            and all(item in members for item in occurrence_pair)
            and source_row is not None
            and row["source_Round300A_row_sha256"] == source_row["row_sha256"]
            and list(occurrence_pair)
            == source_row["canonical_unordered_Round294_registry_occurrence_ids"]
            and source_row["R295A_explicit_lower_graph_sheet_witness_present"]
            is False
            and all(
                type(row.get(field)) is dict
                and row[field].get("satisfied") is True
                for field in g_fields
            )
            and row["cross_official_key_physical_edge_permitted"] is True
            and row["occurrence_identity_collapsed"] is False
            and row["official_key_identity_merged"] is False
            and row[
                "owner_extension_sidecar_not_Gamma_core_or_attachment_or_edge_basis"
            ] is True
            and row["corridor_box_used_as_Gamma_intersection"] is False
            and row["D4_transfer_used"] is False
            and row["candidate_physical_connectivity_conclusion"] is True
            and row["formal_physical_witness_credit"] == 1
            and row["formal_component_edge_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_maximality_credit"] == 0
            and row["formal_fibre_credit"] == 0
            and row["formal_global_disposition_credit"] == 0,
            "Round305B physical witness boundary",
        )
        need(source not in by_source, "Round305B source witness uniqueness")
        root_pair = tuple(
            engine.project(item, members, roots) for item in occurrence_pair
        )
        fresh_pair = tuple(sorted(checkpoint_map[item] for item in root_pair))
        actual_keys = [members[item].official_key for item in occurrence_pair]
        need(
            fresh_pair == component_pair
            and checkpoint_map[root_pair[0]] != checkpoint_map[root_pair[1]]
            and all(type(item) is str for item in actual_keys)
            and len(set(actual_keys)) == 2
            and row["official_key_pair"] == sorted(actual_keys)
            and len(row["official_key_pair"]) == 2,
            "Round305B every witness fresh component/key lift",
        )
        by_source[source] = row
        grouped[component_pair].append(row)
    need(
        set(by_source) == expected_physical_sources
        and len(grouped) == 8
        and {len(value) for value in grouped.values()} == {128}
        and len({item for pair in grouped for item in pair}) == 16,
        "Round305B 8-edge matching census",
    )
    edges: list[Any] = []
    lifts: list[Lift] = []
    seen_pairs: set[tuple[str, str]] = set()
    for edge_row in sorted(
        edge_rows, key=lambda row: row["Round305B_canonical_component_edge_row_id"]
    ):
        component_pair = tuple(edge_row["canonical_Round304_final_component_pair"])
        witnesses = grouped.get(component_pair, [])
        witness_ids = sorted(
            row["Round305B_physical_witness_row_id"] for row in witnesses
        )
        witness_by_id = {
            row["Round305B_physical_witness_row_id"]: row for row in witnesses
        }
        witness_hashes = [witness_by_id[item]["row_sha256"] for item in witness_ids]
        occurrence_pairs = sorted(
            row["canonical_registry_occurrence_pair"] for row in witnesses
        )
        key_profiles = {tuple(row["official_key_pair"]) for row in witnesses}
        need(
            component_pair not in seen_pairs
            and len(component_pair) == 2
            and list(component_pair) == sorted(component_pair)
            and component_pair[0] != component_pair[1]
            and len(witnesses) == 128
            and edge_row["physical_witness_row_count"] == 128
            and edge_row["physical_witness_row_ids_sha256"] == digest(witness_ids)
            and edge_row["physical_witness_row_sha256s_sha256"]
            == digest(witness_hashes)
            and edge_row["canonical_occurrence_pairs_sha256"]
            == digest(occurrence_pairs)
            and len(key_profiles) == 1
            and edge_row["canonical_official_key_pair"]
            == list(next(iter(key_profiles)))
            and edge_row["cross_official_key_physical_edge_permitted"] is True
            and edge_row["occurrence_identity_collapsed"] is False
            and edge_row["official_key_identity_merged"] is False
            and edge_row["all_128_witnesses_satisfy_G0_G5"] is True
            and edge_row["deduplicated_from_witness_rows_not_union_rows"] is True
            and edge_row["formal_component_edge_credit"] == 1
            and edge_row["eligible_for_later_fresh_DSU_application"] is True
            and edge_row["formal_DSU_rank_reduction_credit"] == 0,
            "Round305B canonical edge closure",
        )
        seen_pairs.add(component_pair)
        chosen = min(
            witnesses,
            key=lambda row: (
                tuple(row["canonical_registry_occurrence_pair"]),
                row["Round305B_physical_witness_row_id"],
            ),
        )
        occurrence_pair = tuple(chosen["canonical_registry_occurrence_pair"])
        need(all(item in members for item in occurrence_pair), "lift occurrence universe")
        root_pair = tuple(engine.project(item, members, roots) for item in occurrence_pair)
        reprojected = tuple(sorted(checkpoint_map[item] for item in root_pair))
        need(
            reprojected == component_pair and checkpoint_map[root_pair[0]] != checkpoint_map[root_pair[1]],
            "lift exact fresh Round304 checkpoint pair",
        )
        lift = Lift(
            edge_row["Round305B_canonical_component_edge_row_id"],
            edge_row["row_sha256"],
            component_pair,
            chosen["Round305B_physical_witness_row_id"],
            chosen["row_sha256"],
            occurrence_pair,
            root_pair,
            tuple(chosen["official_key_pair"]),
        )
        lifts.append(lift)
        edges.append(
            engine.Edge(
                "R305B_PHYSICAL_COMPONENT_EDGE",
                lift.edge_row_id,
                lift.edge_row_sha256,
                lift.occurrence_pair,
                lift.root_pair,
            )
        )
    need(
        len(edges) == len(lifts) == 8 and seen_pairs == set(grouped),
        "exact eight fully covered lifted edges",
    )
    return edges, lifts, by_source


def make_row(id_field: str, namespace: str, payload: dict[str, Any]) -> dict[str, Any]:
    need(id_field not in payload and "row_sha256" not in payload, "row closure boundary")
    row = {id_field: namespace + digest([namespace, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


def deterministic_gzip(document: dict[str, Any]) -> bytes:
    raw = canonical(document)
    output = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0,
                       compresslevel=9) as stream:
        stream.write(raw)
    return output.getvalue()


def build_ledger(
    key: str, rows: Iterable[dict[str, Any]]
) -> tuple[bytes, dict[str, Any]]:
    materialized = list(rows)
    id_field = ID_FIELDS[key]
    ids = [row[id_field] for row in materialized]
    hashes = [row["row_sha256"] for row in materialized]
    need(len(ids) == len(set(ids)), "generated duplicate IDs:" + key)
    for row in materialized:
        need(
            set(row) == ROW_FIELDS[key]
            and row["schema"] == ROW_SCHEMAS[key],
            "generated exact schema:" + key,
        )
        check_self(row, "row_sha256", "generated:" + key)
    payload = {
        "schema": SCHEMA + "." + key + "-ledger.v1",
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "status": "PASS_DETERMINISTIC_ZERO_CREDIT_CANDIDATE_LEDGER",
        "row_count": len(materialized),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(hashes),
        "rows_sha256": digest(materialized),
        TABLES[key]: materialized,
    }
    document = {**payload, "ledger_sha256": digest(payload)}
    need(
        set(document) == LEDGER_FIELDS | {TABLES[key]},
        "generated exact ledger schema:" + key,
    )
    raw = deterministic_gzip(document)
    return raw, {
        "filename": FILES[key],
        "schema": document["schema"],
        "row_count": len(materialized),
        "row_ids_sha256": document["row_ids_sha256"],
        "row_hashes_sha256": document["row_hashes_sha256"],
        "rows_sha256": document["rows_sha256"],
        "ledger_sha256": document["ledger_sha256"],
        "file_sha256": hashlib.sha256(raw).hexdigest(),
    }


def iter_edge_rows(engine: Any, roots: set[str], edges: list[Any]) -> Iterator[dict[str, Any]]:
    dsu = engine.DSU(roots)
    for index, edge in enumerate(edges):
        reduced = dsu.union(*edge.roots)
        yield make_row(
            ID_FIELDS["edge"],
            "round306a-edge-application:",
            {
                "schema": SCHEMA + ".fresh-edge-application-row.v1",
                "application_index": index,
                "source_channel": edge.channel,
                "source_row_id": edge.source_id,
                "source_row_sha256": edge.source_sha,
                "canonical_occurrence_endpoint_pair": list(edge.endpoints),
                "projected_base_root_pair": sorted(edge.roots),
                "fed_to_new_empty_DSU": True,
                "forward_rank_reduction": int(reduced),
                "forward_cycle_or_redundant": int(not reduced),
                "candidate_DSU_rank_reduction": int(reduced),
                "serialized_Round304_partition_used_as_state": False,
                "formal_credit_without_independent_verification_marker": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            },
        )


def iter_member_rows(members: dict[str, Any], final_map: dict[str, str]) -> Iterator[dict[str, Any]]:
    for member_id in sorted(members):
        member = members[member_id]
        yield make_row(
            ID_FIELDS["member"],
            "round306a-member-component:",
            {
                "schema": SCHEMA + ".fresh-member-component-row.v1",
                "registry_occurrence_id": member.member_id,
                "base_root_id": member.base_root,
                "official_key_id": member.official_key,
                "final_component_id": final_map[member.base_root],
                "member_identity_preserved": True,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
            },
        )


def promoted_rows(lifts: list[Lift]) -> Iterator[dict[str, Any]]:
    for index, lift in enumerate(lifts):
        yield make_row(
            ID_FIELDS["promoted"],
            "round306a-r305b-promoted-edge-application:",
            {
                "schema": SCHEMA + ".r305b-promoted-edge-application-row.v1",
                "promoted_edge_index": index,
                "source_Round305B_component_edge_row_id": lift.edge_row_id,
                "source_Round305B_component_edge_row_sha256": lift.edge_row_sha256,
                "source_Round305B_selected_physical_witness_row_id": lift.witness_row_id,
                "source_Round305B_selected_physical_witness_row_sha256": lift.witness_row_sha256,
                "selection_rule": "LEXICOGRAPHIC_MIN_OCCURRENCE_PAIR_THEN_WITNESS_ID",
                "Round304_fresh_checkpoint_component_pair": list(lift.component_pair),
                "selected_occurrence_pair": list(lift.occurrence_pair),
                "projected_base_root_pair": list(lift.root_pair),
                "official_key_pair": list(lift.official_key_pair),
                "cross_checkpoint_components_before_application": True,
                "forward_rank_reduction": 1,
                "witness_rows_are_not_union_rows": True,
                "formal_official_key_merge_credit": 0,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_credit_without_independent_verification_marker": 0,
            },
        )


def frontier_rows(
    engine: Any,
    members: dict[str, Any],
    roots: set[str],
    final_map: dict[str, str],
    witness_by_source: dict[str, dict[str, Any]],
    r300a_source_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    output: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    for row in r300a_source_rows:
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        root_pair = [engine.project(item, members, roots) for item in pair]
        component_pair = sorted(final_map[item] for item in root_pair)
        same = component_pair[0] == component_pair[1]
        prior = row["R295A_explicit_lower_graph_sheet_witness_present"]
        source_id = row["Round300A_canonical_occurrence_pair_row_id"]
        r305b = witness_by_source.get(source_id)
        if r305b is not None:
            need(
                r305b["source_Round300A_row_sha256"] == row["row_sha256"]
                and r305b["canonical_registry_occurrence_pair"] == pair,
                "Round300A/Round305B exact frontier join",
            )
        disposition = (
            "PRIOR_R295A_WITNESSED__SAME_ROUND306A_COMPONENT"
            if prior and same
            else (
                "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_ROUND305B_PHYSICAL_EDGE"
                if (not prior and r305b is not None and same)
                else (
                    "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH"
                    if (not prior and same)
                    else "CROSS_COMPONENT__FULL_MAXIMALITY_BLOCKER"
                )
            )
        )
        histogram[disposition] += 1
        output.append(
            make_row(
                ID_FIELDS["frontier"],
                "round306a-r300a-reprojection:",
                {
                    "schema": SCHEMA + ".r300a-reprojection-row.v1",
                    "source_Round300A_row_id": source_id,
                    "source_Round300A_row_sha256": row["row_sha256"],
                    "canonical_occurrence_pair": pair,
                    "projected_base_root_pair": sorted(root_pair),
                    "Round306A_final_component_pair": component_pair,
                    "same_Round306A_final_component": same,
                    "prior_R295A_witness_present": prior,
                    "source_Round305B_physical_witness_row_id": (
                        r305b["Round305B_physical_witness_row_id"] if r305b else None
                    ),
                    "source_Round305B_physical_witness_row_sha256": (
                        r305b["row_sha256"] if r305b else None
                    ),
                    "disposition": disposition,
                    "Round300A_frontier_residual_credit": int(not same),
                    "formal_full_maximality_credit": 0,
                },
            )
        )
    expected = {
        "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_OTHER_LEGAL_DSU_PATH": 2080,
        "PREVIOUSLY_UNWITNESSED__RECLOSED_BY_ROUND305B_PHYSICAL_EDGE": 1024,
        "PRIOR_R295A_WITNESSED__SAME_ROUND306A_COMPONENT": 128,
    }
    need(len(output) == 3232 and dict(sorted(histogram.items())) == expected,
         "Round300A exact zero-residual reprojection")
    return output, dict(sorted(histogram.items()))


def wtail_rows(engine: Any, unresolved: list[dict[str, Any]], final_map: dict[str, str],
               forest: dict[str, list[tuple[str, Any]]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for item in sorted(unresolved, key=lambda row: row["row_id"]):
        left, right = item["roots"]
        same = final_map[left] == final_map[right]
        path = engine.witness_path(left, right, forest) if same else []
        need(same and bool(path), "Round306A W-tail reclosure")
        output.append(
            make_row(
                ID_FIELDS["wtail"],
                "round306a-wtail-disposition:",
                {
                    "schema": SCHEMA + ".wtail-disposition-row.v1",
                    "source_W_tail_row_id": item["row_id"],
                    "source_W_tail_row_sha256": item["row_sha256"],
                    "source_Round300D_row_id": item["source_Round300D_row_id"],
                    "canonical_occurrence_endpoint_pair": list(item["endpoints"]),
                    "projected_base_root_pair": sorted(item["roots"]),
                    "Round306A_final_component_pair": sorted(
                        [final_map[left], final_map[right]]
                    ),
                    "same_Round306A_final_component": True,
                    "disposition": "RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE",
                    "stronger_legal_path": path,
                    "source_row_fed_to_DSU": False,
                    "formal_component_edge_credit": 0,
                    "formal_maximality_credit": 0,
                },
            )
        )
    need(len(output) == 4, "exact four W-tail rows")
    return output


def reconstruct_state(seed: int) -> dict[str, Any]:
    need(type(seed) is int and 0 <= seed < 2**63, "seed")
    source_before = file_sha256(Path(__file__))
    validate_round304_seal()
    validate_round305b_seal()
    engine = load_engine()
    engine.validate_admission_and_historical_seals()
    members, roots, universe = engine.reconstruct_members()
    old_edges = engine.collect_old_edges(members, roots)
    prior_map, prior, _ = engine.apply_edges(
        roots, old_edges, component_namespace="round301-legal-component:"
    )
    need(
        prior["edge_rows"] == 434606
        and prior["rank_reduction"] == 246016
        and prior["component_count"] == 121948,
        "fresh pre-R303B checkpoint",
    )
    r303b_edges, unresolved, r303b_census = engine.collect_round303b(
        members, roots, prior_map
    )
    base_edges = old_edges + r303b_edges
    checkpoint_map, checkpoint, _ = engine.apply_edges(roots, base_edges)
    need(
        checkpoint["edge_rows"] == 478710
        and checkpoint["rank_reduction"] == 275268
        and checkpoint["component_count"] == 92696
        and checkpoint["partition_sha256"] == R304_PARTITION_SHA256,
        "fresh exact Round304 checkpoint",
    )
    r300a_source_rows = list(engine.validated_gzip_rows(
        engine.R300A_LEDGER,
        "canonical_occurrence_pair_rows",
        "Round300A_canonical_occurrence_pair_row_id",
        engine.R300A_PAIR_COMMITMENT,
    ))
    new_edges, lifts, witness_by_source = build_round305b_lifts(
        engine, members, roots, checkpoint_map, r300a_source_rows
    )
    all_edges = base_edges + new_edges
    final_map, forward, forest = engine.apply_edges(
        roots,
        all_edges,
        witness_forest=True,
        component_namespace="round306-fresh-legal-component:",
    )
    reverse_map, reverse, _ = engine.apply_edges(
        roots,
        reversed(all_edges),
        component_namespace="round306-fresh-legal-component:",
    )
    need(
        final_map == reverse_map
        and forward["edge_rows"] == reverse["edge_rows"] == 478718
        and forward["rank_reduction"] == reverse["rank_reduction"] == 275276
        and forward["component_count"] == reverse["component_count"] == 92688
        and forward["partition_sha256"]
        == reverse["partition_sha256"]
        == EXPECTED_PARTITION_SHA256
        and forward["per_channel_rank_reduction"].get(
            "R305B_PHYSICAL_COMPONENT_EDGE"
        )
        == 8,
        "Round306A exact fresh forward/reverse outcome",
    )
    need(
        reverse["per_channel_rank_reduction"].get(
            "R305B_PHYSICAL_COMPONENT_EDGE"
        )
        == 8,
        "Round306A reverse Round305B matching rank",
    )
    r300a_rows, r300a_histogram = frontier_rows(
        engine, members, roots, final_map, witness_by_source, r300a_source_rows
    )
    tail_rows = wtail_rows(engine, unresolved, final_map, forest)
    engine.assert_input_snapshots_unchanged()
    need(file_sha256(Path(__file__)) == source_before, "producer source changed")
    assert_input_snapshots_unchanged()
    return {
        "source_sha256": source_before,
        "engine": engine,
        "members": members,
        "roots": roots,
        "universe": universe,
        "prior": prior,
        "r303b_census": r303b_census,
        "checkpoint": checkpoint,
        "all_edges": all_edges,
        "lifts": lifts,
        "final_map": final_map,
        "forward": forward,
        "reverse": reverse,
        "r300a_rows": r300a_rows,
        "r300a_histogram": r300a_histogram,
        "tail_rows": tail_rows,
    }


def build_candidate(seed: int) -> tuple[dict[str, bytes], dict[str, Any]]:
    state = reconstruct_state(seed)
    artifacts: dict[str, bytes] = {}
    metadata: dict[str, Any] = {}
    for key, rows in (
        ("edge", iter_edge_rows(state["engine"], state["roots"], state["all_edges"])),
        ("member", iter_member_rows(state["members"], state["final_map"])),
        ("promoted", promoted_rows(state["lifts"])),
        ("frontier", state["r300a_rows"]),
        ("wtail", state["tail_rows"]),
    ):
        raw, meta = build_ledger(key, rows)
        artifacts[FILES[key]] = raw
        metadata[key] = meta
    residual_row = make_row(
        ID_FIELDS["residual"],
        "round306a-residual-gate:",
        {
            "schema": SCHEMA + ".residual-gate-row.v1",
            "Round300A_complete_pair_count": 3232,
            "Round300A_cross_component_residual_count": 0,
            "Round305B_physical_witness_rows_consumed_as_edge_provenance": 1024,
            "Round305B_canonical_component_edge_applications": 8,
            "Round305B_rank_reductions": 8,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "occurrence_fibre_exhaustion_proved": False,
            "full_maximality_proved": False,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "D02_status": "BLOCKED",
            "CM2_status": "NO-GO_FOR_CLAIM",
        },
    )
    raw, meta = build_ledger("residual", [residual_row])
    artifacts[FILES["residual"]] = raw
    metadata["residual"] = meta
    result_payload = {
        "schema": SCHEMA + ".zero-credit-candidate-result.v1",
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "status": (
            "PASS_ROUND306A_FRESH_478718_EDGE_DSU_CANDIDATE__"
            "275276_RANK_REDUCTIONS__92688_COMPONENTS__"
            "PENDING_INDEPENDENT_VERIFICATION__"
            "ZERO_NEW_FORMAL_DSU_AND_MAXIMALITY_CREDIT"
        ),
        "producer_file_sha256": state["source_sha256"],
        "frozen_Round304_engine": {
            "filename": R304_ENGINE,
            "file_sha256": R304_ENGINE_SHA256,
            "complete_source_member_and_edge_universe_rebuilt": True,
            "serialized_Round304_partition_loaded_as_state": False,
        },
        "Round305B_seal": {
            "manifest_filename": R305B_MANIFEST,
            "manifest_file_sha256": R305B_MANIFEST_SHA256,
            "manifest_member_count": 14,
            "physical_witness_rows": 1024,
            "canonical_component_edges": 8,
            "independent_verification_is_formal_credit_marker": True,
        },
        "member_universe": state["universe"],
        "fresh_source_reconstruction_chain": {
            "pre_R303B_checkpoint": state["prior"],
            "Round303B_census": state["r303b_census"],
            "fresh_Round304_checkpoint": state["checkpoint"],
            "serialized_Round304_partition_loaded_as_state": False,
        },
        "fresh_Round304_checkpoint": state["checkpoint"],
        "fresh_forward_application": state["forward"],
        "fresh_reverse_application": state["reverse"],
        "forward_reverse_same_partition": True,
        "Round305B_edge_application": {
            "physical_witness_rows_are_not_union_rows": True,
            "edge_application_count": 8,
            "rank_reduction_count": 8,
            "sixteen_distinct_pre_edge_components": True,
            "selection_rule": "LEXICOGRAPHIC_MIN_OCCURRENCE_PAIR_THEN_WITNESS_ID",
            "inherited_officially_admitted_Round305B_component_edge_credit": 8,
            "new_component_edge_credit_issued_by_Round306A": 0,
            "candidate_incremental_DSU_rank_reduction_count": 8,
        },
        "Round300A_reprojection": {
            "row_count": 3232,
            "cross_component_residual_count": 0,
            "disposition_histogram": state["r300a_histogram"],
            "full_maximality_credit": 0,
        },
        "full_maximality_gate": {
            "Round300A_frontier_reprojected_to_zero": True,
            "transformed_face_exhaustion_proved": False,
            "cross_chart_exhaustion_proved": False,
            "retained_event_exhaustion_proved": False,
            "occurrence_fibre_exhaustion_proved": False,
            "full_maximality_proved": False,
            "formal_maximality_credit": 0,
        },
        "formal_credit_without_independent_verification_marker": {
            "formal_legal_component_edge_application_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_union_credit": 0,
            "formal_component_quotient_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "candidate_credit_if_independently_verified": {
            "credit_semantics": (
                "REPLACEMENT_CERTIFICATE__NOT_ADDITIVE_TO_ROUND304_TOTALS"
            ),
            "superseded_Round304_totals": {
                "legal_edge_application_count": 478710,
                "DSU_rank_reduction_count": 275268,
                "post_Round304_component_count": 92696,
            },
            "incremental_over_sealed_Round304": {
                "new_Round305B_component_edge_applications": 8,
                "additional_DSU_rank_reductions": 8,
                "component_count_decrease": 8,
                "physical_witness_rows": 1024,
                "physical_witness_rows_are_not_union_rows": True,
            },
            "formal_legal_component_edge_application_credit": 478718,
            "formal_DSU_rank_reduction_credit": 275276,
            "formal_component_union_credit": 275276,
            "formal_component_quotient_credit": 1,
            "formal_post_Round306A_component_count": 92688,
            "formal_maximality_credit": 0,
        },
        "output_ledgers": metadata,
        "seed_affects_output": False,
        "D02_status": "BLOCKED",
        "CM2_status": "NO-GO_FOR_CLAIM",
    }
    result = {**result_payload, "result_sha256": digest(result_payload)}
    need(set(result) == RESULT_FIELDS, "generated exact result schema")
    result_raw = canonical(result)
    parsed = strict_json_bytes(result_raw, "generated result")
    check_self(parsed, "result_sha256", "generated result")
    artifacts[FILES["result"]] = result_raw
    state["engine"].assert_input_snapshots_unchanged()
    assert_input_snapshots_unchanged()
    need(file_sha256(Path(__file__)) == state["source_sha256"],
         "producer changed before candidate return")
    return artifacts, result


def open_workspace_parent_fd(parent: Path) -> int:
    root = Path(os.path.abspath(os.fspath(ROOT)))
    candidate = Path(os.path.abspath(os.fspath(parent)))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise BuildBlocked("private stage parent outside workspace") from exc
    flags = (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0)
    )
    root_entry = os.lstat(root)
    need(
        stat.S_ISDIR(root_entry.st_mode) and not stat.S_ISLNK(root_entry.st_mode),
        "private stage workspace root",
    )
    descriptor = os.open(root, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino) == (root_entry.st_dev, root_entry.st_ino)
            and opened.st_uid == os.geteuid(),
            "private stage root fd binding",
        )
        for part in relative.parts:
            entry = os.stat(part, dir_fd=descriptor, follow_symlinks=False)
            need(stat.S_ISDIR(entry.st_mode),
                 "private stage parent chain:" + part)
            child = os.open(part, flags, dir_fd=descriptor)
            child_entry = os.fstat(child)
            need(
                (child_entry.st_dev, child_entry.st_ino)
                == (entry.st_dev, entry.st_ino)
                and child_entry.st_uid == os.geteuid(),
                "private stage parent fd binding:" + part,
            )
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def create_private_stage_directory(stage: Path) -> tuple[Path, int, int]:
    resolved = Path(os.path.abspath(os.fspath(stage)))
    root = Path(os.path.abspath(os.fspath(ROOT)))
    deliverables = Path(os.path.abspath(os.fspath(DATA)))
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise BuildBlocked("private stage outside workspace") from exc
    need(relative.parts, "private stage refuses workspace root")
    try:
        resolved.relative_to(deliverables)
    except ValueError:
        pass
    else:
        raise BuildBlocked("private stage refuses deliverables subtree")
    need(resolved.name not in {"", ".", ".."}, "private stage name")
    parent_descriptor = open_workspace_parent_fd(resolved.parent)
    stage_descriptor: int | None = None
    try:
        try:
            os.mkdir(resolved.name, 0o700, dir_fd=parent_descriptor)
        except FileExistsError as exc:
            raise BuildBlocked("private stage must be new") from exc
        os.fsync(parent_descriptor)
        entry = os.stat(
            resolved.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        need(stat.S_ISDIR(entry.st_mode), "private stage created entry")
        stage_descriptor = os.open(
            resolved.name,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=parent_descriptor,
        )
        os.fchmod(stage_descriptor, 0o700)
        opened = os.fstat(stage_descriptor)
        need(
            (opened.st_dev, opened.st_ino) == (entry.st_dev, entry.st_ino)
            and opened.st_uid == os.geteuid()
            and stat.S_IMODE(opened.st_mode) == 0o700,
            "private stage directory fd binding",
        )
        return resolved, parent_descriptor, stage_descriptor
    except BaseException:
        if stage_descriptor is not None:
            os.close(stage_descriptor)
        os.close(parent_descriptor)
        raise


def exclusive_private_write_and_readback(
    stage_descriptor: int,
    name: str,
    payload: bytes,
) -> None:
    need(name == Path(name).name and name not in {"", ".", ".."},
         "private stage flat filename")
    descriptor = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        0o600,
        dir_fd=stage_descriptor,
    )
    try:
        os.fchmod(descriptor, 0o600)
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_uid == os.geteuid()
            and stat.S_IMODE(opened.st_mode) == 0o600,
            "private output file boundary:" + name,
        )
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            count = os.write(descriptor, view[offset:])
            need(count > 0, "private output short write:" + name)
            offset += count
        os.fsync(descriptor)
        final = os.fstat(descriptor)
        need(final.st_size == len(payload), "private output size:" + name)
    finally:
        os.close(descriptor)
    entry = os.stat(name, dir_fd=stage_descriptor, follow_symlinks=False)
    need(
        (entry.st_dev, entry.st_ino) == (final.st_dev, final.st_ino)
        and entry.st_nlink == 1,
        "private output entry binding:" + name,
    )
    reader = os.open(
        name,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
        dir_fd=stage_descriptor,
    )
    try:
        need(file_identity(os.fstat(reader)) == file_identity(entry),
             "private output readback fd binding:" + name)
        offset = 0
        while True:
            block = os.read(reader, 1 << 20)
            if not block:
                break
            need(
                block == payload[offset:offset + len(block)],
                "private output readback bytes:" + name,
            )
            offset += len(block)
        need(offset == len(payload), "private output readback length:" + name)
    finally:
        os.close(reader)


def publish_private_candidate(directory: Path, artifacts: dict[str, bytes]) -> None:
    expected = set(FILES.values())
    need(set(artifacts) == expected, "exact candidate artifact set")
    ordered = sorted(expected - {FILES["result"]}) + [FILES["result"]]
    resolved, parent_descriptor, stage_descriptor = create_private_stage_directory(
        directory
    )
    committed: set[str] = set()
    try:
        for name in ordered:
            if name == FILES["result"]:
                need(
                    set(os.listdir(stage_descriptor)) == committed,
                    "result requires exact prior private ledger prefix",
                )
                assert_input_snapshots_unchanged()
            exclusive_private_write_and_readback(
                stage_descriptor, name, artifacts[name]
            )
            committed.add(name)
            need(
                set(os.listdir(stage_descriptor)) == committed,
                "private stage exact committed prefix",
            )
        need(committed == expected, "private stage exact final file set")
        os.fsync(stage_descriptor)
        stage_entry = os.stat(
            resolved.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        opened_stage = os.fstat(stage_descriptor)
        need(
            (stage_entry.st_dev, stage_entry.st_ino)
            == (opened_stage.st_dev, opened_stage.st_ino),
            "private stage final directory binding",
        )
        os.fsync(parent_descriptor)
    finally:
        # Preserve any exact private 0700 orphan for forensic recovery.
        os.close(stage_descriptor)
        os.close(parent_descriptor)


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".contract.v1",
        "schema_snapshot_sha256": SCHEMA_SNAPSHOT_SHA256,
        "status": "IMPLEMENTED_ZERO_CREDIT_PRODUCER__FULL_REBUILD_REQUIRED",
        "Round304_engine_sha256": R304_ENGINE_SHA256,
        "Round304_manifest_sha256": R304_MANIFEST_SHA256,
        "Round305B_manifest_sha256": R305B_MANIFEST_SHA256,
        "Round305B_manifest_member_count": 14,
        "expected_member_count": 564492,
        "expected_base_root_count": 367964,
        "expected_edge_application_count": 478718,
        "expected_rank_reduction_count": 275276,
        "expected_component_count": 92688,
        "expected_partition_sha256": EXPECTED_PARTITION_SHA256,
        "expected_Round300A_reprojection_rows": 3232,
        "expected_Round300A_cross_component_residual": 0,
        "formal_full_maximality_credit": 0,
        "output_artifact_count": len(FILES),
        "dual_seeds": [SEED_A, SEED_B],
        "built_in_dual_seed_is_named_seed_or_cold_process_evidence": False,
        "external_independent_process_replays_required": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--dual-seed", action="store_true")
    parser.add_argument("--seed", type=int, default=SEED_A)
    args = parser.parse_args()
    if args.print_contract:
        print(canonical(contract()).decode("ascii"))
        return
    if args.self_test:
        sample = {"schema": "self-test", "value": 1}
        print(
            canonical(
                {
                    **contract(),
                    "deterministic_gzip": deterministic_gzip(sample)
                    == deterministic_gzip(sample),
                    "Round304_engine_pin_matches": file_sha256(DATA / R304_ENGINE)
                    == R304_ENGINE_SHA256,
                    "Round304_manifest_pin_matches": file_sha256(DATA / R304_MANIFEST)
                    == R304_MANIFEST_SHA256,
                    "Round305B_manifest_pin_matches": file_sha256(DATA / R305B_MANIFEST)
                    == R305B_MANIFEST_SHA256,
                    "formal_artifact_written": False,
                }
            ).decode("ascii")
        )
        return
    need(sum((args.no_write, args.candidate_dir is not None, args.dual_seed)) == 1,
         "choose exactly one of --no-write, --candidate-dir, --dual-seed")
    if args.dual_seed:
        first, first_result = build_candidate(SEED_A)
        first_hashes = {name: hashlib.sha256(raw).hexdigest()
                        for name, raw in first.items()}
        del first
        second, second_result = build_candidate(SEED_B)
        second_hashes = {name: hashlib.sha256(raw).hexdigest()
                         for name, raw in second.items()}
        need(first_hashes == second_hashes and canonical(first_result) == canonical(second_result),
             "dual-seed candidate divergence")
        print(canonical({
            "status": "PASS_EXACT_IN_PROCESS_REPEAT__NOT_NAMED_SEED_EVIDENCE",
            "file_sha256s": first_hashes,
            "result": first_result,
            "named_seed_evidence": False,
            "cold_process_evidence": False,
        }).decode("ascii"))
        return
    artifacts, result = build_candidate(args.seed)
    if args.candidate_dir is not None:
        publish_private_candidate(args.candidate_dir, artifacts)
    print(canonical(result).decode("ascii"))


if __name__ == "__main__":
    main()
