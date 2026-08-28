#!/usr/bin/env python3
"""Independent fail-closed verifier for the candidate-only C30e lane.

The C30e producer is never imported or executed.  A pinned independent C30b
verifier supplies only audited interval arithmetic, H-sheet reconstruction,
and exact atomic half-open geometry.  This module dynamically selects the two
``REDUCED_LIVE_3D_CELL`` origins from pinned R184/R215, reconstructs their
R176/R180/R201/R215 lineage and sealed C30a baseline, and compares every byte
of the future C30e candidate to an independently rebuilt reference.

The sole ledger predecessor is a manifest-first sealed C30d 58-state handoff.
All C30d publication hashes are deliberately unset in development, making
this verifier fail closed before it imports its independent mathematical
base.  Verification success still grants zero formal credit: only a later
C30e publication can authorize the proposed 58-to-56 transition.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from types import MappingProxyType
from typing import Any

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30e_source_w_reduced_live_"
    "whole_origin_disposition"
)
H_CELL_LEDGER = PREFIX + "_h_cell_ledger.jsonl.gz"
LIVE_CELL_LEDGER = PREFIX + "_strict_live_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
PRODUCER = PREFIX + "_producer.py"
PRODUCER_SHA256 = (
    "5d0088e07ab29c8be18c43312a9fe7c6532a4da4ebfc13e7fa091f10b73795da"
)

C30B_PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
C30B_VERIFIER = C30B_PREFIX + "_independent_verifier.py"
C30B_VERIFIER_SHA256 = (
    "1776137520b1add49a218e6ccce680aaffdafc195c99ef7992c1a5ee31694b66"
)
C30B_PRODUCER = C30B_PREFIX + "_producer.py"
C30B_PRODUCER_SHA256 = (
    "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762"
)
C30D_PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion"
C30D_ROOT_MANIFEST = C30D_PREFIX + "_root_manifest.sha256"
C30D_PAYLOAD_MANIFEST = C30D_PREFIX + "_payload_manifest.sha256"
C30D_VERIFICATION = C30D_PREFIX + "_verification.json"
C30D_SEALED = Path("cm2_round306c30d_sealed")
C30D_ROOT_MANIFEST_SHA256: str | None = None
C30D_VERIFICATION_SHA256: str | None = None
C30D_RESULT_OBJECT_SHA256: str | None = None
C30D_SEALED_MEMBER_SHA256: dict[str, str] | None = None
C30D_SEALED_MEMBERS = tuple(sorted((
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    C30D_PREFIX + "_multi_delta_cell_ledger.jsonl.gz",
    C30D_PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz",
    C30D_PREFIX + "_whole_origin_ledger.jsonl.gz",
    C30D_PREFIX + "_result.json",
)))

REDUCED_LIVE_BLOCKER = "REDUCED_LIVE_3D_CELL"
OUTGOING_H_BLOCKER = "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST"
EXPECTED_ORIGIN_COUNT = 2
EXPECTED_REDUCED_LIVE_PER_ORIGIN = 24
EXPECTED_OUTGOING_H_PER_ORIGIN = 128


class Reject(RuntimeError):
    """A stable, user-visible fail-closed reason."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def bootstrap_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def regular_singleton(path: Path, expected: str) -> bool:
    try:
        status = path.lstat()
    except OSError:
        return False
    return bool(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and bootstrap_hash(path) == expected
    )


def bootstrap_validate_c30d_pins() -> None:
    require(
        C30D_ROOT_MANIFEST_SHA256 is not None
        and C30D_VERIFICATION_SHA256 is not None
        and C30D_RESULT_OBJECT_SHA256 is not None
        and C30D_SEALED_MEMBER_SHA256 is not None,
        "C30D_58_STATE_AUTHORITY_PINS_UNSET",
    )
    assert C30D_ROOT_MANIFEST_SHA256 is not None
    assert C30D_VERIFICATION_SHA256 is not None
    assert C30D_RESULT_OBJECT_SHA256 is not None
    assert C30D_SEALED_MEMBER_SHA256 is not None
    values = (
        C30D_ROOT_MANIFEST_SHA256,
        C30D_VERIFICATION_SHA256,
        C30D_RESULT_OBJECT_SHA256,
        *C30D_SEALED_MEMBER_SHA256.values(),
    )
    require(
        set(C30D_SEALED_MEMBER_SHA256) == set(C30D_SEALED_MEMBERS)
        and all(
            type(value) is str
            and len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            for value in values
        ),
        "C30D_58_STATE_AUTHORITY_PINS_MALFORMED",
    )


def import_pinned_base() -> Any:
    path = ROOT / C30B_VERIFIER
    require(
        regular_singleton(path, C30B_VERIFIER_SHA256),
        "pinned independent C30b verifier",
    )
    forbidden = {PRODUCER[:-3], C30B_PRODUCER[:-3]}
    require(forbidden.isdisjoint(sys.modules), "no producer preloaded")
    module_name = C30B_VERIFIER[:-3]
    require(module_name not in sys.modules, "C30b verifier not preloaded")
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(
        specification is not None and specification.loader is not None,
        "C30b verifier import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    require(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and regular_singleton(path, C30B_VERIFIER_SHA256),
        "imported independent C30b verifier identity",
    )
    return module


bootstrap_validate_c30d_pins()
base = import_pinned_base()
wire = base.wire
digest = base.digest
file_hash = base.file_hash
regular_bytes = base.regular_bytes
strict_json = base.strict_json
canonical_rows = base.canonical_rows
sealed = base.sealed
r176 = base.r176
r180 = base.r180
r215 = base.r215
ctx = base.flint.ctx


@dataclass(frozen=True)
class HSource:
    source_kind: str
    row: Any
    source_binding: dict[str, Any]


@dataclass(frozen=True)
class LiveSource:
    source_kind: str
    row: Any
    leaf: Any
    strict_disposition: str
    source_binding: dict[str, Any]
    exact_behind_candidate_evidence: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class Reference:
    pins: tuple[tuple[str, str], ...]
    c30d_authority: Any
    origin_keys: tuple[str, ...]
    registry: Any
    summaries: Any
    h_sources: tuple[HSource, ...]
    live_sources: tuple[LiveSource, ...]
    contexts: Any


def verifier_parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        parts = line.split("  ", 1)
        require(
            len(parts) == 2
            and len(parts[0]) == 64
            and all(character in "0123456789abcdef" for character in parts[0]),
            "manifest syntax:" + label,
        )
        sha256, filename = parts
        relative = Path(filename)
        require(
            filename not in rows
            and filename == relative.as_posix()
            and not relative.is_absolute()
            and ".." not in relative.parts,
            "manifest path:" + label,
        )
        rows[filename] = sha256
    require(bool(rows), "nonempty manifest:" + label)
    return rows


def verifier_capture_c30d_authority() -> dict[str, Any]:
    """Independently capture the exact C30d 58-state publication."""
    assert C30D_ROOT_MANIFEST_SHA256 is not None
    assert C30D_VERIFICATION_SHA256 is not None
    assert C30D_RESULT_OBJECT_SHA256 is not None
    assert C30D_SEALED_MEMBER_SHA256 is not None
    root_path = ROOT / C30D_ROOT_MANIFEST
    payload_path = ROOT / C30D_PAYLOAD_MANIFEST
    verification_path = ROOT / C30D_VERIFICATION
    root_before = root_path.lstat()
    root_raw = regular_bytes(root_path, 64 * 1024)
    require(
        hashlib.sha256(root_raw).hexdigest() == C30D_ROOT_MANIFEST_SHA256,
        "pinned C30d root manifest",
    )
    root_rows = verifier_parse_manifest(root_raw, "C30d root")
    payload_expected = root_rows.get(C30D_PAYLOAD_MANIFEST)
    require(type(payload_expected) is str,
            "C30d payload manifest root binding")
    payload_before = payload_path.lstat()
    payload_raw = regular_bytes(payload_path, 4 * 1024 * 1024)
    verification_before = verification_path.lstat()
    verification_raw = regular_bytes(verification_path, 4 * 1024 * 1024)
    require(
        hashlib.sha256(payload_raw).hexdigest() == payload_expected
        and hashlib.sha256(verification_raw).hexdigest()
        == C30D_VERIFICATION_SHA256
        and root_rows == {
            C30D_PAYLOAD_MANIFEST: payload_expected,
            C30D_VERIFICATION: C30D_VERIFICATION_SHA256,
        },
        "C30d exact manifest chain",
    )
    verification = base.strict_object_bytes(
        verification_raw, C30D_VERIFICATION
    )
    verification_body = dict(verification)
    verification_object_sha256 = verification_body.pop(
        "verification_object_sha256", None
    )
    before = {
        "excluded": 74_746,
        "conservative_live": 2_086,
        "resolved_nonexcluded": 2_008,
        "remaining": 78,
        "total": 76_832,
    }
    after = {
        "excluded": 74_766,
        "conservative_live": 2_066,
        "resolved_nonexcluded": 2_008,
        "remaining": 58,
        "total": 76_832,
        "remaining_partition": {
            "reduced_live": 2,
            "retained_source_seams": 2,
            "compact_q": 54,
        },
    }
    handoff = verification.get("formal_handoff", {})
    require(
        verification_object_sha256 == digest(verification_body)
        and type(verification.get("status")) is str
        and verification["status"].startswith("PASS_FORMAL_C30D__")
        and handoff.get("before") == before
        and handoff.get("after") == after
        and handoff.get("credit") == {
            "whole_source_W_origin_exclusions": 20,
            "resolved_nonexcluded": 0,
        }
        and verification.get("strict_nonpromotion", {}).get("D02")
        == "BLOCKED_BY_58_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "C30d formal 58-state handoff",
    )

    directory = ROOT / C30D_SEALED
    directory_before = directory.lstat()
    require(
        stat.S_ISDIR(directory_before.st_mode)
        and not directory.is_symlink(),
        "C30d sealed regular directory",
    )
    directory_fd = os.open(
        directory,
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    sealed: dict[str, bytes] = {}
    try:
        opened = os.fstat(directory_fd)
        names = set(os.listdir(directory_fd))
        require(
            (opened.st_dev, opened.st_ino)
            == (directory_before.st_dev, directory_before.st_ino)
            and names == set(C30D_SEALED_MEMBERS),
            "C30d exact sealed member set",
        )
        for filename in C30D_SEALED_MEMBERS:
            handle = os.open(
                filename,
                os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=directory_fd,
            )
            try:
                item_before = os.fstat(handle)
                chunks: list[bytes] = []
                while block := os.read(handle, 1 << 20):
                    chunks.append(block)
                item_after = os.fstat(handle)
            finally:
                os.close(handle)
            raw = b"".join(chunks)
            require(
                stat.S_ISREG(item_before.st_mode)
                and item_before.st_nlink == 1
                and (
                    item_before.st_dev, item_before.st_ino,
                    item_before.st_size, item_before.st_mtime_ns,
                    item_before.st_ctime_ns,
                ) == (
                    item_after.st_dev, item_after.st_ino,
                    item_after.st_size, item_after.st_mtime_ns,
                    item_after.st_ctime_ns,
                )
                and len(raw) == item_before.st_size
                and hashlib.sha256(raw).hexdigest()
                == C30D_SEALED_MEMBER_SHA256[filename],
                "C30d sealed member capture:" + filename,
            )
            sealed[filename] = raw
        directory_after = os.fstat(directory_fd)
        require(
            (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ) == (
                directory_after.st_dev, directory_after.st_ino,
                directory_after.st_size, directory_after.st_mtime_ns,
                directory_after.st_ctime_ns,
            )
            and set(os.listdir(directory_fd)) == names,
            "C30d sealed directory changed during capture",
        )
    finally:
        os.close(directory_fd)
    root_after = root_path.lstat()
    payload_after = payload_path.lstat()
    verification_after = verification_path.lstat()
    def identity(status: os.stat_result) -> tuple[int, int, int, int, int]:
        return (
            status.st_dev, status.st_ino, status.st_size,
            status.st_mtime_ns, status.st_ctime_ns,
        )
    require(
        identity(root_after) == identity(root_before)
        and identity(payload_after) == identity(payload_before)
        and identity(verification_after) == identity(verification_before),
        "C30d authority files changed during capture",
    )
    result_name = C30D_PREFIX + "_result.json"
    result = base.strict_object_bytes(sealed[result_name], result_name)
    result_body = dict(result)
    result_object_sha256 = result_body.pop("result_sha256", None)
    require(
        result_object_sha256 == C30D_RESULT_OBJECT_SHA256
        and digest(result_body) == C30D_RESULT_OBJECT_SHA256
        and result.get(
            "proposed_source_W_transition_if_C30d_is_independently_sealed", {}
        ).get("after") == after,
        "C30d sealed result 58-state boundary",
    )
    published = verification.get("sealed_publication", {}).get("sealed_files")
    require(
        type(published) is dict
        and set(published) == set(C30D_SEALED_MEMBERS)
        and all(
            published[name].get("sha256") == C30D_SEALED_MEMBER_SHA256[name]
            and published[name].get("size") == len(sealed[name])
            for name in C30D_SEALED_MEMBERS
        ),
        "C30d verification/seal equality",
    )
    pins = {
        C30D_ROOT_MANIFEST: C30D_ROOT_MANIFEST_SHA256,
        C30D_PAYLOAD_MANIFEST: payload_expected,
        C30D_VERIFICATION: C30D_VERIFICATION_SHA256,
        **{
            os.fspath(C30D_SEALED / name): C30D_SEALED_MEMBER_SHA256[name]
            for name in C30D_SEALED_MEMBERS
        },
    }
    return {
        "pins": pins,
        "pins_sha256": digest([
            {"filename": name, "sha256": value}
            for name, value in sorted(pins.items())
        ]),
        "formal_before": before,
        "formal_after": after,
        "verification_object_sha256": verification_object_sha256,
        "result_object_sha256": result_object_sha256,
    }


def validate_contract_sources(
    authority: dict[str, Any],
) -> list[dict[str, str]]:
    """Pin inputs without importing any producer contract."""
    pins = base.validate_sources()
    require(
        regular_singleton(ROOT / PRODUCER, PRODUCER_SHA256)
        and regular_singleton(ROOT / C30B_PRODUCER, C30B_PRODUCER_SHA256),
        "C30e/C30b producer source pins without import",
    )
    candidate_pins = pins + [
        {"filename": C30B_PRODUCER, "sha256": C30B_PRODUCER_SHA256},
    ] + [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in authority["pins"].items()
    ]
    return sorted(candidate_pins, key=lambda value: value["filename"])


def reduction_binding(reduction: dict[str, Any]) -> dict[str, Any]:
    return {
        key: reduction[key]
        for key in (
            "category", "residual_reason", "closed", "disposition",
            "eligible_targets", "candidate_evidence",
        )
    }


def sign_name(value: Any) -> str:
    return base.sign_name(value)


def live_boundary_rows(
    cell_key: str,
    source_kind: str,
    strict_disposition: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    axes = ("t", "p", "s")
    for fixed_count in (1, 2, 3):
        for fixed_axes in itertools.combinations(axes, fixed_count):
            for sides in itertools.product(
                ("LOWER", "UPPER"), repeat=fixed_count
            ):
                rows.append(sealed({
                    "schema": (
                        "cm2.round306c30e.strict-live-outer-"
                        "boundary.row.v1"
                    ),
                    "cell_key": cell_key,
                    "source_kind": source_kind,
                    "fixed_coordinates": dict(zip(
                        fixed_axes, sides, strict=True
                    )),
                    "ambient_dimension": 3 - fixed_count,
                    "strict_parent_disposition": strict_disposition,
                    "restricted_disposition": "LIVE",
                    "strict_interval_predicates_restrict_to_closed_stratum": True,
                    "dyadic_half_open_owner": (
                        "BOUND_BY_WHOLE_ORIGIN_ATOMIC_OWNER_AUDIT"
                    ),
                    "pointwise_disposition_is_unambiguous": True,
                    "formal_credit": 0,
                }))
    require(len(rows) == 26, "strict LIVE 26 outer strata")
    return rows


def expected_live_row(source: LiveSource) -> dict[str, Any]:
    row = source.row
    disposition, margins = r176.terminal_disposition(
        row.chart_id, source.leaf
    )
    outgoing_chart, outgoing_margins = r176.outgoing_generic(
        row.chart_id, row.box
    )
    require(
        source.leaf.classification == "unique_first"
        and source.leaf.owner_target == r176.FROZEN_OWNER
        and disposition == source.strict_disposition
        == "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"
        and margins is not None
        and outgoing_chart == r176.FROZEN_CHART == "W",
        "independent strict LIVE identity:" + row.key,
    )
    margin_signs = {
        key: sign_name(value) for key, value in sorted(margins.items())
    }
    outgoing_signs = {
        key: sign_name(value)
        for key, value in sorted(outgoing_margins.items())
    }
    require(
        margin_signs == outgoing_signs
        and all(value != "OVERWRAP" for value in margin_signs.values())
        and all(
            evidence["eligible_exact_behind"] is True
            and evidence["ell_strict_negative"] is True
            and evidence["distance_margin_strict_positive"] is True
            for evidence in source.exact_behind_candidate_evidence
        ),
        "independent strict LIVE margins:" + row.key,
    )
    boundaries = live_boundary_rows(
        row.key, source.source_kind, source.strict_disposition
    )
    body = {
        "schema": "cm2.round306c30e.strict-live.cell-row.v1",
        "source_kind": source.source_kind,
        "origin_key": row.origin_key,
        "cell_key": row.key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": str(r215.box_volume(row.box)),
        "active_targets": list(row.active_targets),
        "source_binding": source.source_binding,
        "exact_behind_candidate_evidence": list(
            source.exact_behind_candidate_evidence
        ),
        "remaining_leaf_classification": source.leaf.classification,
        "remaining_unique_first_owner": source.leaf.owner_target,
        "strict_disposition": source.strict_disposition,
        "outgoing_chart": outgoing_chart,
        "all_eight_outgoing_margin_signs": margin_signs,
        "all_outgoing_margins_strict": True,
        "ambient_3D_disposition": "LIVE",
        "positive_measure": True,
        "outer_boundary_restriction_rows": boundaries,
        "outer_boundary_restriction_row_count": len(boundaries),
        "outer_boundary_restriction_rows_sha256": digest(boundaries),
        "partition_theorem": {
            "whole_closed_3D_cell_strictly_LIVE": True,
            "all_six_2D_faces_restrict_to_LIVE": True,
            "all_twelve_1D_edges_restrict_to_LIVE": True,
            "all_eight_0D_vertices_restrict_to_LIVE": True,
            "all_3D_2D_1D_0D_strata_disposed": True,
            "dyadic_half_open_owner_deferred_to_origin_atomic_audit": True,
            "whole_closed_cell_disposition": "LIVE",
        },
        "whole_closed_cell_disposition": "LIVE",
        "candidate_credit_if_independently_verified": {
            "strict_live_cell_disposition": 1,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "strict_live_cell_disposition": 0,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__UNSEALED_UPSTREAMS__NO_FORMAL_CREDIT"
        ),
    }
    return sealed(body)


def expected_h_row(source: HSource) -> tuple[dict[str, Any], str]:
    row = source.row
    partition = base.independent_complete_partition(row)
    typed = [
        terminal for terminal in partition["terminal_rectangles"]
        if terminal["coarse_disposition"] == "MIXED"
    ]
    face_rows = [
        item for terminal in typed
        for item in terminal["typed_strata"]["H_zero_1D_face_incidences"]
    ]
    face_region_rows = [
        item for terminal in typed
        for item in terminal["typed_strata"]
        ["terminal_face_2D_H_sign_regions"]
    ]
    edge_rows = [
        item for terminal in typed
        for item in terminal["typed_strata"]["H_zero_0D_edge_incidences"]
    ]
    edge_region_rows = [
        item for terminal in typed
        for item in terminal["typed_strata"]
        ["terminal_edge_1D_H_sign_intervals"]
    ]
    corner_rows = [
        item for terminal in typed
        for item in terminal["typed_strata"]["H_zero_0D_corner_absence_rows"]
    ]
    body = {
        "schema": "cm2.round306c30e.reduced-live-lane.h-cell.row.v1",
        "source_kind": source.source_kind,
        "origin_key": row.origin_key,
        "cell_key": row.key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": str(r215.box_volume(row.box)),
        "unique_first_owner": r176.FROZEN_OWNER,
        "frozen_outgoing_chart": r176.FROZEN_CHART,
        "source_binding": source.source_binding,
        "H_partition": partition,
        "whole_H_cell_disposition": partition["whole_cell_disposition"],
        "typed_H_zero_2D_sheet_count": len(typed),
        "typed_H_zero_2D_sheet_rows_sha256": digest([
            terminal["typed_strata"]["H_zero_2D_sheet"]
            for terminal in typed
        ]),
        "terminal_face_2D_H_sign_region_row_count": len(face_region_rows),
        "terminal_face_2D_H_sign_region_rows_sha256": digest(
            face_region_rows
        ),
        "H_zero_1D_face_incidence_row_count": len(face_rows),
        "H_zero_1D_face_incidence_rows_sha256": digest(face_rows),
        "terminal_edge_1D_H_sign_interval_row_count": len(edge_region_rows),
        "terminal_edge_1D_H_sign_interval_rows_sha256": digest(
            edge_region_rows
        ),
        "H_zero_0D_edge_incidence_row_count": len(edge_rows),
        "H_zero_0D_edge_incidence_rows_sha256": digest(edge_rows),
        "H_zero_0D_corner_absence_row_count": len(corner_rows),
        "H_zero_0D_corner_absence_rows_sha256": digest(corner_rows),
        "half_open_owner_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
        "whole_origin_exclusion_credit": 0,
        "reused_geometry_contract": (
            "PINNED_UNSEALED_C30B_PRODUCER__GEOMETRY_ONLY"
        ),
        "candidate_credit_if_independently_verified": {
            "outgoing_H_cell_disposition": 1,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "outgoing_H_cell_disposition": 0,
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__C30B_GEOMETRY_REUSE_IS_CONDITIONAL"
        ),
    }
    expected = sealed(body)
    require(
        partition[
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        and partition["terminal_exact_atomic_owner_audit"]
        ["all_raw_2D_strata_exactly_reclosed"] is True
        and partition["terminal_exact_atomic_owner_audit"]
        ["all_raw_1D_strata_exactly_reclosed"] is True,
        "independent H 3D/2D/1D/0D closure:" + row.key,
    )
    base.validate_disposition_aware_split_owners(partition)
    for terminal in typed:
        base.validate_typed_boundary_exhaustion(terminal)
    return expected, partition["whole_cell_disposition"]


def dynamic_scope() -> tuple[
    tuple[str, ...],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    bounded = base.pinned_pretty_json(ROOT / base.R215_CERTIFICATE)[
        "result"
    ]["bounded_probe_result"]
    r184 = base.pinned_pretty_json(ROOT / base.R184_CERTIFICATE)
    selected = sorted(
        (
            row for row in bounded["whole_origin_outcome"]["per_origin_rows"]
            if row["first_obstruction"] == REDUCED_LIVE_BLOCKER
        ),
        key=lambda value: value["origin_key"],
    )
    keys = tuple(row["origin_key"] for row in selected)
    summaries = {row["origin_key"]: row for row in selected}
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(keys)
    }
    c30a_promoted = canonical_rows(base.C30A_SEALED / base.C30A_ORIGIN)
    c30a_held = canonical_rows(base.C30A_SEALED / base.C30A_HELD)
    c30a_touched_keys = {
        row["origin_key"] for row in c30a_promoted + c30a_held
    }
    require(
        len(keys) == EXPECTED_ORIGIN_COUNT
        and len(set(keys)) == EXPECTED_ORIGIN_COUNT
        and tuple(sorted(keys)) == keys
        and set(registry) == set(keys)
        and len(c30a_promoted) == 160
        and len(c30a_held) == 2
        and set(keys).isdisjoint(c30a_touched_keys)
        and all(
            summary["source_domain_classification"]
            == "STRICT_PHYSICAL_CHART_INTERIOR"
            and summary["Round201_residual_cell_count"]
            == EXPECTED_REDUCED_LIVE_PER_ORIGIN
            + EXPECTED_OUTGOING_H_PER_ORIGIN
            and summary["Round215_analytic_closed_cell_count"] == 0
            and summary["Round215_blocker_count"] == {
                OUTGOING_H_BLOCKER: EXPECTED_OUTGOING_H_PER_ORIGIN,
                REDUCED_LIVE_BLOCKER: EXPECTED_REDUCED_LIVE_PER_ORIGIN,
            }
            and summary["Round215_method_count"] == {
                "EXACT_BEHIND_RECLASSIFICATION": (
                    EXPECTED_REDUCED_LIVE_PER_ORIGIN
                ),
                "REDUCED_NONTERMINAL_RECORD_CENSUS": (
                    EXPECTED_OUTGOING_H_PER_ORIGIN
                ),
            }
            and registry[summary["origin_key"]]["priority_class"]
            == "DELTA_H_OR_MULTI_NO_Q"
            for summary in selected
        ),
        "dynamic pinned reduced-live scope and sealed C30a disjointness",
    )
    return keys, registry, summaries


def inherited_same_sign_binding(evidence: dict[str, Any]) -> dict[str, Any]:
    require(
        evidence["method"] == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX"
        and evidence["coarse_disposition"] == "MIXED"
        and evidence["Delta_zero_graph_inside_closed_box"] is False
        and evidence["empty_2D_graph_edge_and_corner_ledger"] is True
        and evidence["witness"] == "FOLLOWUP_H_PARTITION",
        "inherited same-sign Delta followup H",
    )
    return {
        "Round180_terminal_evidence": evidence,
        "Round180_terminal_sha256": evidence["terminal_sha256"],
        "Round180_same_sign_Delta_followup": {
            "method": evidence["method"],
            "target": evidence["target"],
            "derivative_sign": evidence["derivative_sign"],
            "strict_common_face_sign": evidence["strict_common_face_sign"],
            "Delta_p_lower_face_sign": evidence["strict_common_face_sign"],
            "Delta_p_upper_face_sign": evidence["strict_common_face_sign"],
            "Delta_zero_graph_inside_closed_box": False,
            "empty_2D_graph_edge_and_corner_ledger": True,
            "witness": evidence["witness"],
        },
    }


def reconstruct_reference() -> Reference:
    authority = verifier_capture_c30d_authority()
    pins = validate_contract_sources(authority)
    origin_keys, registry, summaries = dynamic_scope()
    replay = r176.replay_frontier()
    target_set = set(origin_keys)
    roots_by_origin: dict[str, list[Any]] = defaultdict(list)
    preclosed_by_origin: dict[str, list[Any]] = defaultdict(list)
    preclosed_kinds: dict[str, set[str]] = defaultdict(set)
    preclosed_evidence: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in replay["frontier"]:
        if row.origin_key not in target_set:
            continue
        kind, proof = r176.closure(row)
        if kind is None:
            roots_by_origin[row.origin_key].append(row)
        else:
            preclosed_by_origin[row.origin_key].append(row)
            preclosed_kinds[row.origin_key].add(kind)
            preclosed_evidence[row.origin_key][row.key] = proof
    require(
        set(roots_by_origin) == target_set
        and all(preclosed_kinds[key] <= {"EXCLUDED"} for key in origin_keys),
        "independent two-origin R176 reconstruction",
    )

    h_sources: list[HSource] = []
    live_sources: list[LiveSource] = []
    contexts: dict[str, dict[str, Any]] = {}
    for origin in origin_keys:
        roots = sorted(roots_by_origin[origin], key=lambda value: value.key)
        preclosed = sorted(
            preclosed_by_origin[origin], key=lambda value: value.key
        )
        refinement = r180.refine_origin(roots, 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(
            roots, refinement
        )
        for evidence in sorted(
            refinement["terminal_rows"],
            key=lambda value: value["cell_key"],
        ):
            if evidence["coarse_disposition"] == "EXCLUDED":
                continue
            row = leaves["terminal"][evidence["cell_key"]]
            if evidence["method"] == "DIRECT_STRICT_CLOSED_BOX":
                leaf, _records = r176.classify(
                    row.chart_id, row.box, row.active_targets
                )
                disposition, _margins = r176.terminal_disposition(
                    row.chart_id, leaf
                )
                require(
                    evidence["coarse_disposition"] == "LIVE"
                    and evidence["disposition"] == disposition
                    and evidence[
                        "all_owned_boundary_strata_inherit_strict_proof"
                    ] is True,
                    "independent Round180 direct LIVE:" + row.key,
                )
                live_sources.append(LiveSource(
                    "ROUND180_DIRECT_STRICT_LIVE",
                    row,
                    leaf,
                    disposition,
                    {
                        "Round180_terminal_evidence": evidence,
                        "Round180_terminal_sha256": evidence["terminal_sha256"],
                        "replayed_terminal_disposition": disposition,
                    },
                    (),
                ))
            elif evidence["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
                h_sources.append(HSource(
                    "ROUND180_INHERITED_OUTGOING_H",
                    row,
                    {
                        "Round180_terminal_evidence": evidence,
                        "Round180_terminal_sha256": evidence["terminal_sha256"],
                    },
                ))
            else:
                require(
                    evidence["method"]
                    == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX",
                    "independent inherited nonexclusion:" + row.key,
                )
                h_sources.append(HSource(
                    "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H",
                    row,
                    inherited_same_sign_binding(evidence),
                ))

        final_closed: dict[str, dict[str, Any]] = {}
        reduced_count = 0
        outgoing_count = 0
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            binding = reduction_binding(reduction)
            if reduction["closed"]:
                final_closed[row.key] = {
                    "source_kind": "ROUND201_EXACT_BEHIND_EXCLUDED",
                    "reduction_sha256": digest(binding),
                }
                continue
            evidence = base.independent_r215_evidence(row, reduction)
            if evidence["analytic_closed"]:
                final_closed[row.key] = {
                    "source_kind": "ROUND215_ANALYTIC_EXCLUDED",
                    "Round215_cell_row_sha256": evidence["row_sha256"],
                }
                continue
            if evidence["blocker"] == REDUCED_LIVE_BLOCKER:
                eligible = tuple(
                    item for item in reduction["candidate_evidence"]
                    if item["eligible_exact_behind"]
                )
                require(
                    reduction["residual_reason"]
                    == "REDUCED_REMAINING_DISPOSITION_LIVE"
                    and reduction["disposition"] is not None
                    and reduction["disposition"].startswith("LIVE")
                    and bool(eligible),
                    "independent reduced LIVE:" + row.key,
                )
                live_sources.append(LiveSource(
                    "ROUND215_REDUCED_LIVE_3D_CELL",
                    row,
                    reduction["leaf"],
                    reduction["disposition"],
                    {
                        "Round215_cell_evidence": evidence,
                        "Round215_cell_row_sha256": evidence["row_sha256"],
                        "Round215_reduction": binding,
                        "Round215_reduction_sha256": digest(binding),
                    },
                    eligible,
                ))
                reduced_count += 1
            else:
                require(
                    evidence["blocker"] == OUTGOING_H_BLOCKER
                    and reduction["leaf"].classification == "unique_first"
                    and reduction["leaf"].owner_target == r176.FROZEN_OWNER,
                    "independent reduced outgoing H:" + row.key,
                )
                h_sources.append(HSource(
                    "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H",
                    row,
                    {
                        "Round215_cell_row_sha256": evidence["row_sha256"],
                        "Round215_blocker": evidence["blocker"],
                        "Round215_reduction_sha256": digest(binding),
                    },
                ))
                outgoing_count += 1
        require(
            reduced_count == EXPECTED_REDUCED_LIVE_PER_ORIGIN
            and outgoing_count == EXPECTED_OUTGOING_H_PER_ORIGIN
            and summaries[origin]["Round215_analytic_closed_cell_count"]
            == sum(
                value["source_kind"] == "ROUND215_ANALYTIC_EXCLUDED"
                for value in final_closed.values()
            ),
            "independent 24 LIVE + 128 H per origin:" + origin,
        )
        contexts[origin] = {
            "source_chart_id": replay["origins"][origin]["chart_id"],
            "source_box": replay["origins"][origin]["box"],
            "Round176_prior_rows": replay["prior"][origin],
            "roots": roots,
            "preclosed_rows": preclosed,
            "preclosed_evidence": preclosed_evidence[origin],
            "refinement": refinement,
            "leaves": leaves,
            "final_closed_sources": final_closed,
        }

    h_sources.sort(key=lambda source: source.row.key)
    live_sources.sort(key=lambda source: source.row.key)
    require(
        len({source.row.key for source in h_sources}) == len(h_sources)
        and len({source.row.key for source in live_sources})
        == len(live_sources)
        and {source.row.key for source in h_sources}.isdisjoint(
            source.row.key for source in live_sources
        )
        and sum(
            source.source_kind
            == "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H"
            for source in h_sources
        ) == 2 * EXPECTED_OUTGOING_H_PER_ORIGIN
        and sum(
            source.source_kind == "ROUND215_REDUCED_LIVE_3D_CELL"
            for source in live_sources
        ) == 2 * EXPECTED_REDUCED_LIVE_PER_ORIGIN,
        "independent global C30e source census",
    )
    return Reference(
        tuple((row["filename"], row["sha256"]) for row in pins),
        MappingProxyType(authority),
        origin_keys,
        MappingProxyType(registry),
        MappingProxyType(summaries),
        tuple(h_sources),
        tuple(live_sources),
        MappingProxyType(contexts),
    )


def prior_faces(
    origin: str,
    context: dict[str, Any],
    prior_boxes: dict[str, Any],
) -> list[dict[str, Any]]:
    frontier_keys = {
        row.key for row in context["roots"] + context["preclosed_rows"]
    }
    rows: list[dict[str, Any]] = []
    pending = [(context["source_box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{context['source_chart_id']}:{box.path}"
        if key in prior_boxes:
            continue
        if depth == 6:
            require(key in frontier_keys, "independent R176 frontier:" + key)
            continue
        lower, upper = r176.split(box)
        parent = r176.Frontier(
            context["source_chart_id"], box, (), origin,
            "ROUND176_PARTITION_SPLIT",
        )
        rows.append(r180.split_face(
            parent, r180.split_axis(box), lower, upper
        ))
        pending.extend(((lower, depth + 1), (upper, depth + 1)))
    rows.sort(key=lambda value: value["parent_cell_key"])
    return rows


def verifier_materialize_atomic_owner_rows(
    origin: str,
    parent: Any,
    leaf_boxes: dict[str, Any],
    proof_source: dict[str, str],
    dispositions: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Independent plane-grid materialization of every owner atom."""
    axes = ("t", "p", "s")
    require(
        bool(leaf_boxes)
        and set(leaf_boxes) == set(proof_source) == set(dispositions),
        "complete verifier atomic owner maps:" + origin,
    )
    bounds = {
        key: {
            "t": (box.t0, box.t1),
            "p": (box.p0, box.p1),
            "s": (box.s0, box.s1),
        }
        for key, box in leaf_boxes.items()
    }
    coordinates = {
        axis: sorted({endpoint for box in bounds.values()
                      for endpoint in box[axis]})
        for axis in axes
    }

    def decode_geometry(
        geometry: dict[str, Any],
    ) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        fixed = {
            axis: Q(value) for axis, value in geometry["fixed"].items()
        }
        spans = {
            axis: (Q(values[0]), Q(values[1]))
            for axis, values in geometry["open_spans"].items()
        }
        return fixed, spans

    def make_atom(
        dimension: int,
        geometry: dict[str, Any],
        raw_sources: list[str],
    ) -> dict[str, Any]:
        fixed, spans = decode_geometry(geometry)
        midpoints = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in spans.items()
        }
        incident = sorted(
            leaf_key for leaf_key, box in bounds.items()
            if all(
                box[axis][0] <= value <= box[axis][1]
                for axis, value in fixed.items()
            )
            and all(
                box[axis][0] <= lower < upper <= box[axis][1]
                for axis, (lower, upper) in spans.items()
            )
            and all(
                box[axis][0] < midpoint < box[axis][1]
                for axis, midpoint in midpoints.items()
            )
        )
        require(bool(incident), "verifier atomic owner exists:" + origin)
        owner = incident[0]
        leaf_incidence: list[dict[str, Any]] = []
        for leaf_key in incident:
            signature: dict[str, str] = {}
            for axis, value in sorted(fixed.items()):
                lower, upper = bounds[leaf_key][axis]
                if value == lower:
                    signature[axis] = "LOWER"
                elif value == upper:
                    signature[axis] = "UPPER"
            leaf_incidence.append(sealed({
                "schema": "cm2.round306c30e.atomic-leaf-incidence.row.v2",
                "leaf_key": leaf_key,
                "relative_boundary_signature": signature,
                "relative_boundary_codimension": len(signature),
                "selected_by_half_open_owner": leaf_key == owner,
                "proof_source": proof_source[leaf_key],
                "leaf_disposition": dispositions[leaf_key],
            }))
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        sources = sorted(set(raw_sources))
        geometry_sha256 = digest(geometry)
        body: dict[str, Any] = {
            "schema": "cm2.round306c30e.atomic-half-open-owner.row.v2",
            "origin_key": origin,
            "ambient_dimension": dimension,
            "ledger_order_key": (
                origin + "|" + str(3 - dimension) + "|" + geometry_sha256
            ),
            "geometry": geometry,
            "geometry_sha256": geometry_sha256,
            "exact_measure": str(measure),
            "measure_kind": (
                "COUNTING_0D" if dimension == 0 else f"LEBESGUE_{dimension}D"
            ),
            "incident_sources": sources,
            "incident_source_count": len(sources),
            "closed_containing_leaf_keys": incident,
            "closed_incident_leaf_rows": leaf_incidence,
            "closed_incident_leaf_rows_sha256": digest(leaf_incidence),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": dispositions[owner],
            "cross_dimensional_source_incidence_complete": True,
        }
        if dimension == 3:
            require(len(incident) == 1,
                    "unique verifier open 3D leaf atom:" + origin)
            source_row = {
                "leaf_key": owner,
                "exact_closed_box": r176.box_row(leaf_boxes[owner]),
                "proof_source": proof_source[owner],
                "disposition": dispositions[owner],
            }
            body["source_3D_leaf_row"] = source_row
            body["source_3D_leaf_row_sha256"] = digest(source_row)
        return sealed(body)

    rows_3d = []
    for leaf_key in sorted(bounds):
        geometry = {
            "fixed": {},
            "open_spans": {
                axis: [str(bounds[leaf_key][axis][0]),
                       str(bounds[leaf_key][axis][1])]
                for axis in axes
            },
        }
        rows_3d.append(make_atom(
            3, geometry,
            ["CLOSED_3D_LEAF:" + leaf_key + ":" + proof_source[leaf_key]],
        ))

    faces: dict[str, dict[str, Any]] = {}
    for leaf_key, box in sorted(bounds.items()):
        for normal_axis in axes:
            tangent_axes = [axis for axis in axes if axis != normal_axis]
            for side, level in (
                ("LOWER", box[normal_axis][0]),
                ("UPPER", box[normal_axis][1]),
            ):
                tangent_intervals = []
                for axis in tangent_axes:
                    values = [
                        value for value in coordinates[axis]
                        if box[axis][0] <= value <= box[axis][1]
                    ]
                    tangent_intervals.append(list(zip(values, values[1:])))
                for rectangle in itertools.product(*tangent_intervals):
                    geometry = {
                        "fixed": {normal_axis: str(level)},
                        "open_spans": {
                            axis: [str(span[0]), str(span[1])]
                            for axis, span in zip(
                                tangent_axes, rectangle, strict=True
                            )
                        },
                    }
                    key = wire(geometry).decode("ascii")
                    group = faces.setdefault(
                        key, {"geometry": geometry, "sources": []}
                    )
                    group["sources"].append(
                        "LEAF_FACE:" + leaf_key + ":" + normal_axis + ":" + side
                    )
    rows_2d = [
        make_atom(2, group["geometry"], group["sources"])
        for _key, group in sorted(faces.items())
    ]

    lines: dict[str, dict[str, Any]] = {}
    for face in rows_2d:
        fixed, spans = decode_geometry(face["geometry"])
        for cut_axis in sorted(spans):
            free_axis = next(axis for axis in spans if axis != cut_axis)
            for side, endpoint in (
                ("LOWER", spans[cut_axis][0]),
                ("UPPER", spans[cut_axis][1]),
            ):
                geometry = {
                    "fixed": {
                        axis: str(value)
                        for axis, value in sorted({
                            **fixed, cut_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {
                        free_axis: [
                            str(spans[free_axis][0]),
                            str(spans[free_axis][1]),
                        ]
                    },
                }
                key = wire(geometry).decode("ascii")
                group = lines.setdefault(
                    key, {"geometry": geometry, "sources": []}
                )
                group["sources"].append(
                    "ATOMIC_2D:" + face["row_sha256"] + ":"
                    + cut_axis + ":" + side
                )
    rows_1d = [
        make_atom(1, group["geometry"], group["sources"])
        for _key, group in sorted(lines.items())
    ]

    points: dict[str, dict[str, Any]] = {}
    for line in rows_1d:
        fixed, spans = decode_geometry(line["geometry"])
        free_axis, (lower, upper) = next(iter(spans.items()))
        for side, endpoint in (("LOWER", lower), ("UPPER", upper)):
            geometry = {
                "fixed": {
                    axis: str(value)
                    for axis, value in sorted({**fixed, free_axis: endpoint}.items())
                },
                "open_spans": {},
            }
            key = wire(geometry).decode("ascii")
            group = points.setdefault(
                key, {"geometry": geometry, "sources": []}
            )
            group["sources"].append(
                "ATOMIC_1D:" + line["row_sha256"] + ":" + side
            )
    rows_0d = [
        make_atom(0, group["geometry"], group["sources"])
        for _key, group in sorted(points.items())
    ]
    all_rows = sorted(
        rows_3d + rows_2d + rows_1d + rows_0d,
        key=lambda row: row["ledger_order_key"],
    )
    require(
        all(rows for rows in (rows_3d, rows_2d, rows_1d, rows_0d))
        and all(row["incident_source_count"] > 0 for row in all_rows)
        and set(row["owner_disposition"] for row in all_rows)
        <= {"EXCLUDED", "LIVE", "MIXED"},
        "complete verifier mixed atomic dimensions:" + origin,
    )

    parent_volume = r215.box_volume(parent)
    leaf_volume = sum(
        (r215.box_volume(box) for box in leaf_boxes.values()), Q(0)
    )
    pairs: list[dict[str, Any]] = []
    ordered = sorted(bounds)
    for ordinal, first in enumerate(ordered):
        for second in ordered[ordinal + 1:]:
            overlap = all(
                max(bounds[first][axis][0], bounds[second][axis][0])
                < min(bounds[first][axis][1], bounds[second][axis][1])
                for axis in axes
            )
            require(not overlap,
                    "verifier atomic 3D leaf interior overlap:" + origin)
            pairs.append({
                "first": first,
                "second": second,
                "interior_overlap": overlap,
            })
    require(leaf_volume == parent_volume,
            "verifier atomic 3D volume exhaustion:" + origin)
    census = Counter(str(row["ambient_dimension"]) + "D" for row in all_rows)
    summary = {
        "schema": "cm2.round306c30e.atomic-owner-ledger-slice.v2",
        "origin_key": origin,
        "external_ledger_filename": ATOMIC_OWNER_LEDGER,
        "row_count": len(all_rows),
        "dimension_census": dict(sorted(census.items())),
        "first_ledger_order_key": all_rows[0]["ledger_order_key"],
        "last_ledger_order_key": all_rows[-1]["ledger_order_key"],
        "row_sha256_sequence_sha256": digest([
            row["row_sha256"] for row in all_rows
        ]),
        "rows_sha256": digest(all_rows),
        "closed_3D_leaf_count": len(leaf_boxes),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_boxes)),
        "closed_3D_leaf_proof_sources_sha256": digest(proof_source),
        "closed_3D_leaf_dispositions_sha256": digest(dispositions),
        "parent_exact_volume": str(parent_volume),
        "closed_3D_leaf_exact_volume_sum": str(leaf_volume),
        "tested_unordered_3D_leaf_pair_count": len(pairs),
        "tested_unordered_3D_leaf_pairs_sha256": digest(pairs),
        "axis_grid_coordinates_sha256": digest({
            axis: [str(value) for value in values]
            for axis, values in coordinates.items()
        }),
        "all_3D_interiors_pairwise_disjoint": True,
        "all_3D_leaves_exhaust_parent": True,
        "all_3D_2D_1D_0D_atoms_materialized": True,
        "all_atoms_have_exact_measure_and_incident_sets": True,
        "all_cross_dimensional_source_joins_materialized": True,
        "all_atoms_have_unique_half_open_owner": True,
        "sampled_evidence_used_for_uniform_conclusion": False,
    }
    return summary, all_rows


def origin_owner_reference(
    origin: str,
    context: dict[str, Any],
    h_rows: list[dict[str, Any]],
    live_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    prior_boxes = base.independent_prior_boxes(origin, context)
    leaves = context["leaves"]
    leaf_boxes: dict[str, Any] = {}

    def add(key: str, box: Any) -> None:
        require(key not in leaf_boxes, "independent duplicate leaf:" + key)
        leaf_boxes[key] = box

    for key, box in prior_boxes.items():
        add(key, box)
    for row in context["preclosed_rows"]:
        add(row.key, row.box)
    for key, row in leaves["terminal"].items():
        add(key, row.box)
    for key, row in leaves["final"].items():
        add(key, row.box)

    h_by_key = {row["cell_key"]: row for row in h_rows}
    live_by_key = {row["cell_key"]: row for row in live_rows}
    final_closed = context["final_closed_sources"]
    require(
        len(h_by_key) == len(h_rows)
        and len(live_by_key) == len(live_rows)
        and set(h_by_key).isdisjoint(live_by_key)
        and set(final_closed).isdisjoint(h_by_key)
        and set(final_closed).isdisjoint(live_by_key),
        "independent origin bucket disjointness:" + origin,
    )
    dispositions = {
        key: (
            h_by_key[key]["whole_H_cell_disposition"]
            if key in h_by_key else "LIVE" if key in live_by_key
            else "EXCLUDED"
        )
        for key in leaf_boxes
    }
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED" for key in prior_boxes
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED"
        for row in context["preclosed_rows"]
    })
    for evidence in context["refinement"]["terminal_rows"]:
        key = evidence["cell_key"]
        proof_source[key] = (
            "ROUND306C30E_MATERIALIZED_INHERITED_H"
            if key in h_by_key else
            "ROUND306C30E_PINNED_ROUND180_STRICT_LIVE"
            if key in live_by_key else
            "PINNED_ROUND180_INHERITED_EXCLUDED"
        )
    for row in context["refinement"]["final_residual_rows"]:
        key = row.key
        proof_source[key] = (
            "ROUND306C30E_MATERIALIZED_FINAL_H"
            if key in h_by_key else "ROUND306C30E_REDUCED_STRICT_LIVE"
            if key in live_by_key else final_closed[key]["source_kind"]
        )
    require(
        set(leaf_boxes) == set(dispositions) == set(proof_source),
        "independent complete owner maps:" + origin,
    )
    owner_slice, owner_rows = verifier_materialize_atomic_owner_rows(
        origin,
        context["source_box"],
        leaf_boxes,
        proof_source,
        dispositions,
    )
    return owner_slice, owner_rows, leaf_boxes, dispositions


def expected_origin_row(
    ordinal: int,
    origin: str,
    context: dict[str, Any],
    registry: dict[str, Any],
    h_rows: list[dict[str, Any]],
    live_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    owner_slice, owner_rows, leaf_boxes, dispositions = origin_owner_reference(
        origin, context, h_rows, live_rows
    )
    disposition_census = Counter(dispositions.values())
    require(
        "EXCLUDED" in disposition_census
        and "LIVE" in disposition_census
        and set(disposition_census) <= {"EXCLUDED", "LIVE", "MIXED"}
        and owner_slice["all_3D_interiors_pairwise_disjoint"] is True
        and owner_slice["all_3D_leaves_exhaust_parent"] is True,
        "independent RESOLVED_MIXED 3D reclosure:" + origin,
    )
    refinement = context["refinement"]
    inherited = sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    )
    final_rows = sorted(
        refinement["final_residual_rows"], key=lambda value: value.key
    )
    reduced_live = [
        row for row in live_rows
        if row["source_kind"] == "ROUND215_REDUCED_LIVE_3D_CELL"
    ]
    inherited_live = [
        row for row in live_rows
        if row["source_kind"] == "ROUND180_DIRECT_STRICT_LIVE"
    ]
    final_h = [
        row for row in h_rows
        if row["source_kind"] == "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H"
    ]
    inherited_h = [
        row for row in h_rows
        if row["source_kind"].startswith("ROUND180_INHERITED_")
    ]
    require(
        len(reduced_live) == EXPECTED_REDUCED_LIVE_PER_ORIGIN
        and len(final_h) == EXPECTED_OUTGOING_H_PER_ORIGIN
        and all(
            row["H_partition"]
            ["exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"]
            is True for row in h_rows
        )
        and all(
            row["partition_theorem"]["all_3D_2D_1D_0D_strata_disposed"]
            and row["outer_boundary_restriction_row_count"] == 26
            for row in live_rows
        ),
        "independent per-origin 3D/2D/1D/0D census:" + origin,
    )
    volumes: defaultdict[str, Q] = defaultdict(Q)
    for key, box in leaf_boxes.items():
        volumes[dispositions[key]] += r215.box_volume(box)
    parent_volume = r215.box_volume(context["source_box"])
    require(
        sum(volumes.values(), Q(0)) == parent_volume
        and volumes["LIVE"] > 0 and volumes["EXCLUDED"] > 0,
        "independent mixed positive-measure witnesses:" + origin,
    )
    first_live = min(
        ({
            "cell_key": row["cell_key"],
            "source_kind": row["source_kind"],
            "exact_volume": row["exact_volume"],
            "strictly_positive_measure": Q(row["exact_volume"]) > 0,
        } for row in live_rows),
        key=wire,
    )
    theorem = {
        "kind": (
            "SOURCE_W_REDUCED_LIVE_WHOLE_ORIGIN_"
            "RESOLVED_MIXED_THEOREM_CANDIDATE"
        ),
        "origin_selected_dynamically_from_pinned_Round215_blocker": True,
        "top_level_dyadic_leaf_partition_exact": True,
        "top_level_leaf_disposition_support": sorted(disposition_census),
        "every_H_cell_has_exact_exhaustive_3D_2D_1D_0D_partition": True,
        "every_strict_LIVE_cell_and_outer_stratum_is_LIVE": True,
        "whole_origin_half_open_atomic_3D_2D_1D_0D_owner_audit": True,
        "positive_measure_LIVE_subset_exists": True,
        "positive_measure_EXCLUDED_subset_exists": True,
        "whole_original_physical_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
        "child_count_sheet_count_or_volume_used_as_integer_credit": False,
    }
    final_closed = context["final_closed_sources"]
    body = {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live."
            "whole-origin-row.candidate.v1"
        ),
        "origin_ordinal": ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": context["source_chart_id"],
        "original_parent_box": r176.box_row(context["source_box"]),
        "lineage_census": {
            "Round176_prior_closed": len(context["Round176_prior_rows"]),
            "Round176_preclosed": len(context["preclosed_rows"]),
            "Round176_residual_roots": len(context["roots"]),
            "Round180_inherited_total": len(inherited),
            "Round180_inherited_H_materialized": len(inherited_h),
            "Round180_inherited_direct_LIVE": len(inherited_live),
            "Round180_final_total": len(final_rows),
            "Round215_reduced_LIVE": len(reduced_live),
            "Round215_reduced_unique_first_outgoing_H": len(final_h),
            "final_closed": len(final_closed),
            "atomic_top_level_leaf_count": len(leaf_boxes),
        },
        "top_level_leaf_disposition_census": dict(sorted(
            disposition_census.items()
        )),
        "top_level_disposition_exact_volumes": {
            key: str(value) for key, value in sorted(volumes.items())
        },
        "H_cell_count": len(h_rows),
        "H_cell_keys_sha256": digest([row["cell_key"] for row in h_rows]),
        "H_cell_rows_sha256": digest(h_rows),
        "strict_LIVE_cell_count": len(live_rows),
        "strict_LIVE_cell_keys_sha256": digest([
            row["cell_key"] for row in live_rows
        ]),
        "strict_LIVE_cell_rows_sha256": digest(live_rows),
        "final_closed_evidence": [
            {"cell_key": key, **value}
            for key, value in sorted(final_closed.items())
        ],
        "atomic_half_open_owner_ledger_slice": owner_slice,
        "exact_volume_conservation": {
            "original_parent": str(parent_volume),
            "sum_by_top_level_disposition": str(sum(
                volumes.values(), Q(0)
            )),
            "all_equalities_verified": True,
        },
        "lexicographic_first_positive_measure_LIVE_witness": first_live,
        "whole_origin_theorem_candidate": theorem,
        "whole_origin_theorem_candidate_sha256": digest(theorem),
        "whole_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
        "candidate_credit_if_all_dependencies_and_independent_checks_later_seal": {
            "resolved_source_W_origin_disposition": 1,
            "resolved_nonexcluded": 1,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "resolved_source_W_origin_disposition": 0,
            "resolved_nonexcluded": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__SEALED_C30D_CONSUMED__NO_C30E_PUBLICATION"
        ),
    }
    return sealed(body), owner_rows


def ledger_descriptor(
    path: Path,
    rows: list[dict[str, Any]],
    order: str,
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def expected_result(
    candidate: Path,
    pins: list[dict[str, str]],
    c30d_authority: dict[str, Any],
    origin_keys: tuple[str, ...],
    h_rows: list[dict[str, Any]],
    live_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    origin_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    h_descriptor = ledger_descriptor(
        candidate / H_CELL_LEDGER, h_rows,
        "LEXICOGRAPHIC_SOURCE_W_CELL_KEY",
    )
    live_descriptor = ledger_descriptor(
        candidate / LIVE_CELL_LEDGER, live_rows,
        "LEXICOGRAPHIC_SOURCE_W_CELL_KEY",
    )
    origin_descriptor = ledger_descriptor(
        candidate / ORIGIN_LEDGER, origin_rows,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    owner_descriptor = ledger_descriptor(
        candidate / ATOMIC_OWNER_LEDGER, owner_rows,
        "LEXICOGRAPHIC_ORIGIN_THEN_DESCENDING_DIMENSION_THEN_GEOMETRY_SHA256",
    )
    runtime_descriptor = {
        "filename": base.RUNTIME_ATTESTATION,
        "size": len(base.BOOTSTRAP_RUNTIME_ATTESTATION_RAW),
        "sha256": base.RUNTIME_ATTESTATION_RAW_SHA256,
        "attestation_payload_sha256": (
            base.RUNTIME_ATTESTATION_PAYLOAD_SHA256
        ),
        "auditor_sha256": base.RUNTIME_AUDITOR_SHA256,
        "schema": base.BOOTSTRAP_RUNTIME_ATTESTATION["schema"],
        "verdict": base.BOOTSTRAP_RUNTIME_ATTESTATION["verdict"],
    }
    h_census = Counter(
        row["whole_H_cell_disposition"] for row in h_rows
    )
    live_source_census = Counter(row["source_kind"] for row in live_rows)
    body = {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live-"
            "whole-origin-disposition.candidate.v1"
        ),
        "status": (
            "PASS_CANDIDATE_ROUND306C30E_REDUCED_LIVE_DISPOSITION__"
            "AWAITING_INDEPENDENT_VERIFICATION_AND_RELEASE_CONTROLS"
        ),
        "input_pins": pins,
        "runtime_attestation": runtime_descriptor,
        "controlled_dual_hash_seed_contract": {
            "required_launch": (
                "env -i HOME=/nonexistent LC_ALL=C.UTF-8 TZ=UTC "
                "PYTHONHASHSEED=<30630071|30630929> python -P -s -B"
            ),
            "accepted_seeds": ["30630071", "30630929"],
            "hash_seed_sentinel": "CM2_C30E_HASH_SEED_SENTINEL_v1",
            "hash_fingerprints": {
                "30630071": -7414891537403211358,
                "30630929": 6822900610173514366,
            },
            "required_flags": {
                "isolated": 0,
                "ignore_environment": 0,
                "safe_path": True,
                "no_user_site": 1,
                "dont_write_bytecode": 1,
                "hash_randomization": 1,
            },
            "python_I_forbidden": True,
            "actual_seed_omitted_from_candidate_for_byte_identity": True,
        },
        "dynamic_scope": {
            "selection_source": (
                "PINNED_ROUND215_WHOLE_ORIGIN_ROWS_WITH_"
                "FIRST_OBSTRUCTION_REDUCED_LIVE_3D_CELL"
            ),
            "selection_uses_hardcoded_origin_keys": False,
            "origin_count": len(origin_keys),
            "origin_keys": list(origin_keys),
            "origin_keys_sha256": digest(list(origin_keys)),
            "Round215_reduced_LIVE_cell_count": sum(
                live_source_census.values()
            ) - live_source_census.get("ROUND180_DIRECT_STRICT_LIVE", 0),
            "Round215_reduced_unique_first_outgoing_H_cell_count": sum(
                row["source_kind"]
                == "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H"
                for row in h_rows
            ),
        },
        "cell_census": {
            "H_cell_count": len(h_rows),
            "H_cell_by_disposition": dict(sorted(h_census.items())),
            "strict_LIVE_cell_count": len(live_rows),
            "strict_LIVE_cell_by_source": dict(sorted(
                live_source_census.items()
            )),
        },
        "whole_origin_census": {
            "audited": len(origin_rows),
            "resolved_live": 0,
            "resolved_mixed": len(origin_rows),
            "excluded": 0,
            "whole_origin_disposition_census": {"RESOLVED_MIXED": 2},
        },
        "candidate_theorem": {
            "every_top_level_leaf_is_excluded_live_or_mixed": True,
            "three_way_leaf_dispositions_are_mutually_exclusive": True,
            "three_way_leaf_dispositions_are_pointwise_exhaustive": True,
            "every_H_cell_has_complete_half_open_3D_2D_1D_0D_partition": True,
            "every_strict_LIVE_cell_has_all_26_outer_strata_restricted": True,
            "every_origin_has_complete_atomic_half_open_3D_2D_1D_0D_audit": True,
            "both_whole_origins_are_resolved_mixed": True,
            "both_whole_origins_have_positive_measure_LIVE_witness": True,
            "neither_whole_origin_is_excluded": True,
            "child_sheet_or_volume_count_used_as_integer_credit": False,
        },
        "upstream_authority": {
            "C30b": {
                "producer_source": C30B_PRODUCER,
                "producer_source_sha256": C30B_PRODUCER_SHA256,
                "sealed_result_consumed": False,
                "dependency_kind": "MATHEMATICS_REUSE_ONLY__NOT_LEDGER_AUTHORITY",
                "official_credit_inherited": 0,
            },
            "C30d": {
                "sealed_result_consumed": True,
                "dependency_kind": "SOLE_MANIFEST_FIRST_58_STATE_LEDGER_AUTHORITY",
                "authority_pins_sha256": c30d_authority["pins_sha256"],
                "verification_object_sha256": c30d_authority[
                    "verification_object_sha256"
                ],
                "result_object_sha256": c30d_authority["result_object_sha256"],
                "formal_before": c30d_authority["formal_before"],
                "formal_after": c30d_authority["formal_after"],
            },
        },
        "proposed_source_W_transition_if_C30e_is_independently_sealed": {
            "whole_origin_exclusion": 0,
            "resolved_origin_disposition": 2,
            "resolved_nonexcluded": 2,
            "remaining": -2,
            "excluded": 0,
            "conservative_live": 0,
            "before": c30d_authority["formal_after"],
            "after": {
                "excluded": 74_766,
                "conservative_live": 2_066,
                "resolved_nonexcluded": 2_010,
                "remaining": 56,
                "total": 76_832,
                "remaining_partition": {
                    "retained_source_seams": 2,
                    "compact_q": 54,
                },
            },
            "official_ledger_mutated": False,
        },
        "last_sealed_source_W_state": {
            "source": "ROUND306C30D",
            "excluded": 74_766,
            "conservative_live": 2_066,
            "resolved_nonexcluded": 2_008,
            "remaining": 58,
            "total": 76_832,
            "official_transition_from_this_producer": "NONE",
        },
        "ledgers": {
            "outgoing_H_cell_candidate": h_descriptor,
            "strict_LIVE_cell_candidate": live_descriptor,
            "atomic_half_open_owner_candidate": owner_descriptor,
            "whole_origin_disposition_candidate": origin_descriptor,
        },
        "formal_credit": {
            "outgoing_H_cell_dispositions": 0,
            "strict_LIVE_cell_dispositions": 0,
            "resolved_source_W_origin_dispositions": 0,
            "resolved_nonexcluded": 0,
            "whole_source_W_origin_exclusions": 0,
            "D02": 0,
            "D03": 0,
            "D04": 0,
            "Gate5": 0,
            "CM2": 0,
        },
        "candidate_credit_if_all_dependencies_and_checks_later_seal": {
            "resolved_source_W_origin_dispositions": 2,
            "resolved_nonexcluded": 2,
            "whole_source_W_origin_exclusions": 0,
        },
        "strict_nonpromotion": {
            "producer_only": True,
            "independent_verifier_present": False,
            "attack_harness_present": False,
            "dual_seed_replay_present": False,
            "cold_replay_present": False,
            "manifest_present": False,
            "sealed_result_present": False,
            "C30d_sealed_predecessor_consumed": True,
            "official_source_W_transition": "UNCHANGED_FROM_ROUND306C30D",
            "D02": "BLOCKED_BY_58_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "BUILD_AN_INDEPENDENT_C30E_VERIFIER_ATTACK_HARNESS_DUAL_TRUE_"
            "HASH_SEED_COLD_REPLAY_AND_MANIFEST_"
            "BEFORE_ANY_LEDGER_CREDIT"
        ),
    }
    return {**body, "result_sha256": digest(body)}


def verify_candidate_dir(candidate: Path, reference: Reference) -> dict[str, Any]:
    candidate = Path(os.path.abspath(os.fspath(candidate)))
    status = candidate.lstat()
    require(
        stat.S_ISDIR(status.st_mode) and not candidate.is_symlink(),
        "candidate regular directory",
    )
    expected_files = {
        H_CELL_LEDGER, LIVE_CELL_LEDGER, ATOMIC_OWNER_LEDGER, ORIGIN_LEDGER, RESULT,
        base.RUNTIME_ATTESTATION,
    }
    require(
        {path.name for path in candidate.iterdir()} == expected_files,
        "candidate exact file set",
    )
    require(
        regular_bytes(candidate / base.RUNTIME_ATTESTATION)
        == base.BOOTSTRAP_RUNTIME_ATTESTATION_RAW,
        "candidate runtime attestation byte identity",
    )
    h_rows = canonical_rows(candidate / H_CELL_LEDGER)
    live_rows = canonical_rows(candidate / LIVE_CELL_LEDGER)
    owner_rows = canonical_rows(candidate / ATOMIC_OWNER_LEDGER)
    origin_rows = canonical_rows(candidate / ORIGIN_LEDGER)
    result = strict_json(candidate / RESULT)
    require(
        [row["cell_key"] for row in h_rows]
        == sorted(row["cell_key"] for row in h_rows)
        and [row["cell_key"] for row in live_rows]
        == sorted(row["cell_key"] for row in live_rows)
        and [row["origin_key"] for row in origin_rows]
        == list(reference.origin_keys)
        and [row["ledger_order_key"] for row in owner_rows]
        == sorted(row["ledger_order_key"] for row in owner_rows)
        and set(row["ambient_dimension"] for row in owner_rows) == {0, 1, 2, 3}
        and len(h_rows) == len(reference.h_sources)
        and len(live_rows) == len(reference.live_sources)
        and len(origin_rows) == EXPECTED_ORIGIN_COUNT,
        "candidate ledger row count/order",
    )

    h_dispositions: dict[str, str] = {}
    for candidate_row, source in zip(
        h_rows, reference.h_sources, strict=True
    ):
        expected, disposition = expected_h_row(source)
        require(
            candidate_row == expected,
            "H row exact independent reconstruction:" + source.row.key,
        )
        h_dispositions[source.row.key] = disposition
    for candidate_row, source in zip(
        live_rows, reference.live_sources, strict=True
    ):
        require(
            candidate_row == expected_live_row(source),
            "strict LIVE row exact independent reconstruction:"
            + source.row.key,
        )

    h_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    live_by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in h_rows:
        h_by_origin[row["origin_key"]].append(row)
    for row in live_rows:
        live_by_origin[row["origin_key"]].append(row)
    expected_owner_rows: list[dict[str, Any]] = []
    for ordinal, candidate_row in enumerate(origin_rows):
        origin = reference.origin_keys[ordinal]
        expected, rebuilt_owner_rows = expected_origin_row(
            ordinal,
            origin,
            reference.contexts[origin],
            reference.registry[origin],
            h_by_origin[origin],
            live_by_origin[origin],
        )
        require(
            candidate_row == expected,
            "whole-origin row exact independent reconstruction:" + origin,
        )
        expected_owner_rows.extend(rebuilt_owner_rows)
    expected_owner_rows.sort(key=lambda row: row["ledger_order_key"])
    require(
        owner_rows == expected_owner_rows,
        "atomic owner ledger exact independent reconstruction",
    )

    pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.pins
    ]
    expected_document = expected_result(
        candidate,
        pins,
        dict(reference.c30d_authority),
        reference.origin_keys,
        h_rows,
        live_rows,
        owner_rows,
        origin_rows,
    )
    require(result == expected_document, "candidate result exact reconstruction")
    require(
        result["proposed_source_W_transition_if_C30e_is_independently_sealed"]
        ["before"] == reference.c30d_authority["formal_after"]
        and result[
            "proposed_source_W_transition_if_C30e_is_independently_sealed"
        ]["after"] == {
            "excluded": 74_766,
            "conservative_live": 2_066,
            "resolved_nonexcluded": 2_010,
            "remaining": 56,
            "total": 76_832,
            "remaining_partition": {
                "retained_source_seams": 2,
                "compact_q": 54,
            },
        }
        and set(result["formal_credit"].values()) == {0},
        "sealed C30d baseline, exact 58-to-56 proposal and zero formal credit",
    )
    forbidden = {
        PRODUCER[:-3], C30B_PRODUCER[:-3],
        base.C30A_SOURCE[:-3],
    }
    require(
        forbidden.isdisjoint(sys.modules),
        "producer modules never imported or executed",
    )
    return {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live."
            "independent-verification.candidate.v1"
        ),
        "status": (
            "PASS_INDEPENDENT_C30E_CANDIDATE__2_DYNAMIC_ORIGINS__"
            "24_REDUCED_LIVE_PLUS_128_H_PER_ORIGIN__"
            "BOTH_RESOLVED_MIXED__FORMAL_CREDIT_ZERO"
        ),
        "candidate_result_sha256": result["result_sha256"],
        "candidate_H_ledger_sha256": file_hash(candidate / H_CELL_LEDGER),
        "candidate_LIVE_ledger_sha256": file_hash(
            candidate / LIVE_CELL_LEDGER
        ),
        "candidate_atomic_owner_ledger_sha256": file_hash(
            candidate / ATOMIC_OWNER_LEDGER
        ),
        "candidate_origin_ledger_sha256": file_hash(
            candidate / ORIGIN_LEDGER
        ),
        "dynamic_origin_keys": list(reference.origin_keys),
        "dynamic_origin_keys_sha256": digest(list(reference.origin_keys)),
        "Round215_per_origin_census": {
            "REDUCED_LIVE_3D_CELL": EXPECTED_REDUCED_LIVE_PER_ORIGIN,
            "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST": (
                EXPECTED_OUTGOING_H_PER_ORIGIN
            ),
        },
        "whole_origin_disposition_census": {"RESOLVED_MIXED": 2},
        "ordered_predecessor": "MANIFEST_FIRST_SEALED_C30D_58_STATE",
        "ledger_before": reference.c30d_authority["formal_after"],
        "proposed_ledger_after": {
            "excluded": 74_766,
            "conservative_live": 2_066,
            "resolved_nonexcluded": 2_010,
            "remaining": 56,
            "total": 76_832,
            "remaining_partition": {
                "retained_source_seams": 2,
                "compact_q": 54,
            },
        },
        "candidate_ledger_delta": {
            "remaining": -2,
            "resolved_nonexcluded": 2,
            "excluded": 0,
            "conservative_live": 0,
        },
        "formal_credit": 0,
        "D02": "BLOCKED_BY_58_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE",
        "CM2": "NO-GO_FOR_CLAIM",
        "candidate_producer_imported_or_executed": False,
    }


def verify(candidate: Path) -> dict[str, Any]:
    return verify_candidate_dir(candidate, reconstruct_reference())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    try:
        output = verify(arguments.candidate)
    except (Reject, base.Reject, KeyError, OSError, ValueError, TypeError) as error:
        print(wire({
            "schema": (
                "cm2.round306c30e.source-w-reduced-live."
                "independent-verification.candidate.v1"
            ),
            "status": "FAIL_CLOSED",
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
