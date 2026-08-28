#!/usr/bin/env python3
"""Produce the candidate-only C30e reduced-live source-W disposition.

The scope is selected from the pinned Round215 whole-origin census rather
than from a handwritten key list: exactly those strict-interior origins whose
first obstruction is ``REDUCED_LIVE_3D_CELL``.  Under the pinned inputs this
is a two-origin lane.  Each origin contains strict reduced-LIVE closed cells
and outgoing-H cells that still require an exact sheet partition.

This producer composes four ingredients:

* the pinned R176/R180 top-level dyadic lineage;
* the pinned R201/R215 exact-behind reductions;
* the C30b exact outgoing-H 3D/2D/1D/0D partition machinery; and
* a disposition-aware atomic half-open owner audit of the original origin.

The result is deliberately candidate-only.  Its only ledger authority is a
future manifest-first sealed C30d 58-state handoff.  All C30d publication
hashes are intentionally unset during development, so this module fails
closed before importing reusable mathematics or creating a candidate.  Even
after those pins are filled, every formal-credit field remains zero until an
independent verifier, attacks, controlled-seed replay, cold replay and a new
manifest authorize the proposed 58-to-56 transition.
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
from fractions import Fraction as Q
from pathlib import Path
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

C30B_SOURCE = (
    "cm2_round306c30b_source_w_outgoing_h_"
    "whole_origin_disposition_producer.py"
)
C30B_SOURCE_SHA256 = (
    "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762"
)

# C30d is the sole formal ledger authority.  These pins must be copied only
# from its final publication, never from a producer candidate.
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

CONTROLLED_HASH_SEEDS = frozenset({"30630071", "30630929"})
CONTROLLED_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
}
HASH_SEED_SENTINEL = "CM2_C30E_HASH_SEED_SENTINEL_v1"
HASH_FINGERPRINTS = {
    "30630071": -7414891537403211358,
    "30630929": 6822900610173514366,
}
INITIAL_SAFE_SYS_PATH = tuple(sys.path)

REDUCED_LIVE_BLOCKER = "REDUCED_LIVE_3D_CELL"
OUTGOING_H_BLOCKER = "NO_UNRESOLVED_RECORD_BUT_UNIQUE_FIRST"
EXPECTED_ORIGIN_COUNT = 2
EXPECTED_REDUCED_LIVE_PER_ORIGIN = 24
EXPECTED_OUTGOING_H_PER_ORIGIN = 128


class BootstrapFailure(RuntimeError):
    """Failure before the pinned C30b failure type is available."""


def bootstrap_need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise BootstrapFailure(label)


def bootstrap_file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def regular_single_link_with_hash(path: Path, expected: str) -> bool:
    try:
        status = path.lstat()
    except OSError:
        return False
    return bool(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and bootstrap_file_hash(path) == expected
    )


def bootstrap_validate_release_contract() -> None:
    """Reject development pins and fake ``-I`` hash-seed runs up front."""
    bootstrap_need(
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
    bootstrap_need(
        set(C30D_SEALED_MEMBER_SHA256) == set(C30D_SEALED_MEMBERS)
        and all(
            type(value) is str
            and len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
            for value in values
        ),
        "C30D_58_STATE_AUTHORITY_PINS_MALFORMED",
    )
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    bootstrap_need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is True
        and sys.flags.no_user_site == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.hash_randomization == 1,
        "C30E_REQUIRES_ENV_I_AND_PYTHON_P_S_B__PYTHON_I_FORBIDDEN",
    )
    bootstrap_need(
        seed in CONTROLLED_HASH_SEEDS
        and environment == CONTROLLED_ENVIRONMENT
        and hash(HASH_SEED_SENTINEL) == HASH_FINGERPRINTS[seed],
        "C30E_CONTROLLED_HASH_SEED_OR_ENVIRONMENT_MISMATCH",
    )
    bootstrap_need(
        "" not in INITIAL_SAFE_SYS_PATH
        and os.fspath(ROOT) not in INITIAL_SAFE_SYS_PATH,
        "C30E_UNSAFE_INITIAL_MODULE_SEARCH_PATH",
    )


def import_pinned_c30b() -> Any:
    """Load the reusable C30b mathematics under its original guards."""
    path = ROOT / C30B_SOURCE
    bootstrap_need(
        regular_single_link_with_hash(path, C30B_SOURCE_SHA256),
        "pinned unsealed C30b producer source",
    )
    module_name = C30B_SOURCE[:-3]
    bootstrap_need(module_name not in sys.modules, "C30b not preloaded")
    specification = importlib.util.spec_from_file_location(module_name, path)
    bootstrap_need(
        specification is not None and specification.loader is not None,
        "C30b import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    bootstrap_need(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and regular_single_link_with_hash(path, C30B_SOURCE_SHA256),
        "imported C30b identity/hash",
    )
    return module


bootstrap_validate_release_contract()
c30b = import_pinned_c30b()
need = c30b.need
canonical = c30b.canonical
digest = c30b.digest
file_hash = c30b.file_hash
strict_json = c30b.strict_json
sealed_row = c30b.sealed_row
fraction = c30b.fraction
write_rows = c30b.write_rows
descriptor = c30b.descriptor
candidate_directory = c30b.candidate_directory
r176 = c30b.r176
r180 = c30b.r180
r215 = c30b.r215
c30a = c30b.c30a
ctx = c30b.ctx


def _identity(status: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        status.st_dev, status.st_ino, status.st_size,
        status.st_mtime_ns, status.st_ctime_ns,
    )


def capture_regular_authority_file(
    path: Path, expected_sha256: str, maximum: int
) -> bytes:
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1
        and 0 < before.st_size <= maximum,
        "C30d authority regular singleton:" + path.name,
    )
    handle = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(handle)
        need(_identity(opened) == _identity(before),
             "C30d authority open race:" + path.name)
        chunks: list[bytes] = []
        while block := os.read(handle, 1 << 20):
            chunks.append(block)
        closed = os.fstat(handle)
    finally:
        os.close(handle)
    raw = b"".join(chunks)
    need(
        _identity(opened) == _identity(closed) == _identity(path.lstat())
        and len(raw) == opened.st_size
        and hashlib.sha256(raw).hexdigest() == expected_sha256,
        "C30d authority capture/hash:" + path.name,
    )
    return raw


def parse_exact_manifest(raw: bytes, label: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        parts = line.split("  ", 1)
        need(
            len(parts) == 2
            and len(parts[0]) == 64
            and all(character in "0123456789abcdef" for character in parts[0]),
            "manifest syntax:" + label,
        )
        sha256, filename = parts
        relative = Path(filename)
        need(
            filename not in rows
            and filename == relative.as_posix()
            and not relative.is_absolute()
            and ".." not in relative.parts,
            "manifest path:" + label,
        )
        rows[filename] = sha256
    need(bool(rows), "nonempty manifest:" + label)
    return rows


def strict_object_bytes(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in values:
            need(type(key) is str and key not in output,
                 "unique JSON keys:" + label)
            output[key] = value
        return output

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs)
    need(type(value) is dict and canonical(value) == raw,
         "canonical JSON object:" + label)
    return value


def capture_c30d_authority() -> dict[str, Any]:
    """Capture and validate the manifest-first sealed 58-state handoff."""
    # The bootstrap check already proved these are fully populated.
    assert C30D_ROOT_MANIFEST_SHA256 is not None
    assert C30D_VERIFICATION_SHA256 is not None
    assert C30D_RESULT_OBJECT_SHA256 is not None
    assert C30D_SEALED_MEMBER_SHA256 is not None
    root_raw = capture_regular_authority_file(
        ROOT / C30D_ROOT_MANIFEST, C30D_ROOT_MANIFEST_SHA256, 64 * 1024
    )
    root_rows = parse_exact_manifest(root_raw, "C30d root")
    payload_expected = root_rows.get(C30D_PAYLOAD_MANIFEST)
    need(type(payload_expected) is str, "C30d payload manifest root binding")
    payload_raw = capture_regular_authority_file(
        ROOT / C30D_PAYLOAD_MANIFEST, payload_expected, 4 * 1024 * 1024
    )
    verification_raw = capture_regular_authority_file(
        ROOT / C30D_VERIFICATION, C30D_VERIFICATION_SHA256, 4 * 1024 * 1024
    )
    need(
        root_rows == {
            C30D_PAYLOAD_MANIFEST: hashlib.sha256(payload_raw).hexdigest(),
            C30D_VERIFICATION: C30D_VERIFICATION_SHA256,
        },
        "C30d exact two-member root manifest",
    )
    verification = strict_object_bytes(verification_raw, C30D_VERIFICATION)
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
    need(
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
    need(
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
        need(
            _identity(opened) == _identity(directory_before)
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
            need(
                stat.S_ISREG(item_before.st_mode)
                and item_before.st_nlink == 1
                and _identity(item_before) == _identity(item_after)
                and len(raw) == item_before.st_size
                and hashlib.sha256(raw).hexdigest()
                == C30D_SEALED_MEMBER_SHA256[filename],
                "C30d sealed member capture:" + filename,
            )
            sealed[filename] = raw
        need(
            _identity(opened) == _identity(os.fstat(directory_fd))
            == _identity(directory.lstat())
            and set(os.listdir(directory_fd)) == names,
            "C30d sealed directory changed during capture",
        )
    finally:
        os.close(directory_fd)

    result_name = C30D_PREFIX + "_result.json"
    result = strict_object_bytes(sealed[result_name], result_name)
    result_body = dict(result)
    result_object_sha256 = result_body.pop("result_sha256", None)
    need(
        result_object_sha256 == C30D_RESULT_OBJECT_SHA256
        and digest(result_body) == C30D_RESULT_OBJECT_SHA256
        and result.get("proposed_source_W_transition_if_C30d_is_independently_sealed", {}).get("after")
        == after,
        "C30d sealed result 58-state boundary",
    )
    published = verification.get("sealed_publication", {}).get("sealed_files")
    need(
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


def validate_runtime_and_contracts() -> None:
    """Validate the reusable C30b mathematics (never as ledger authority)."""
    c30b.validate_runtime()
    c30b.validate_imported_mathematics()
    need(
        sys.modules.get(C30B_SOURCE[:-3]) is c30b
        and Path(c30b.__file__).resolve(strict=True)
        == (ROOT / C30B_SOURCE).resolve(strict=True)
        and file_hash(ROOT / C30B_SOURCE) == C30B_SOURCE_SHA256,
        "C30b reusable contract identity/hash",
    )


def sign_name(value: Any) -> str:
    return c30b.sign_name(value)


def live_boundary_rows(
    cell_key: str,
    source_kind: str,
    strict_disposition: str,
) -> list[dict[str, Any]]:
    """Restrict a strict closed-box LIVE proof to its 26 outer strata."""
    rows: list[dict[str, Any]] = []
    axes = ("t", "p", "s")
    for fixed_count in (1, 2, 3):
        for fixed_axes in itertools.combinations(axes, fixed_count):
            for sides in itertools.product(
                ("LOWER", "UPPER"), repeat=fixed_count
            ):
                rows.append(sealed_row({
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
    need(len(rows) == 26, "six faces twelve edges eight vertices")
    return rows


def strict_live_cell_body(
    row: Any,
    *,
    source_kind: str,
    leaf: Any,
    strict_disposition: str,
    source_binding: dict[str, Any],
    exact_behind_candidate_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    """Materialize a whole closed LIVE cell and every outer restriction."""
    disposition, margins = r176.terminal_disposition(row.chart_id, leaf)
    outgoing_chart, outgoing_margins = r176.outgoing_generic(
        row.chart_id, row.box
    )
    need(
        leaf.classification == "unique_first"
        and leaf.owner_target == r176.FROZEN_OWNER
        and strict_disposition == disposition
        and disposition == "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"
        and margins is not None
        and outgoing_chart == r176.FROZEN_CHART == "W",
        "strict reduced/direct LIVE identity:" + row.key,
    )
    margin_signs = {
        key: sign_name(value) for key, value in sorted(margins.items())
    }
    outgoing_signs = {
        key: sign_name(value)
        for key, value in sorted(outgoing_margins.items())
    }
    need(
        margin_signs == outgoing_signs
        and all(value != "OVERWRAP" for value in margin_signs.values())
        and all(
            evidence["eligible_exact_behind"] is True
            and evidence["ell_strict_negative"] is True
            and evidence["distance_margin_strict_positive"] is True
            for evidence in exact_behind_candidate_evidence
        ),
        "strict LIVE margins/exact-behind candidates:" + row.key,
    )
    boundary_rows = live_boundary_rows(
        row.key, source_kind, strict_disposition
    )
    body = {
        "schema": "cm2.round306c30e.strict-live.cell-row.v1",
        "source_kind": source_kind,
        "origin_key": row.origin_key,
        "cell_key": row.key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": fraction(r215.box_volume(row.box)),
        "active_targets": list(row.active_targets),
        "source_binding": source_binding,
        "exact_behind_candidate_evidence": exact_behind_candidate_evidence,
        "remaining_leaf_classification": leaf.classification,
        "remaining_unique_first_owner": leaf.owner_target,
        "strict_disposition": strict_disposition,
        "outgoing_chart": outgoing_chart,
        "all_eight_outgoing_margin_signs": margin_signs,
        "all_outgoing_margins_strict": True,
        "ambient_3D_disposition": "LIVE",
        "positive_measure": True,
        "outer_boundary_restriction_rows": boundary_rows,
        "outer_boundary_restriction_row_count": len(boundary_rows),
        "outer_boundary_restriction_rows_sha256": digest(boundary_rows),
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
    return body


def h_cell_candidate_body(
    source_kind: str,
    row: Any,
    source_binding: dict[str, Any],
) -> dict[str, Any]:
    """Reuse C30b geometry while replacing all ledger credit by zero."""
    reused = c30b.h_cell_body(source_kind, row, source_binding)
    partition = reused["H_partition"]
    need(
        partition[
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True,
        "exact H partition:" + row.key,
    )
    return {
        **reused,
        "schema": "cm2.round306c30e.reduced-live-lane.h-cell.row.v1",
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


def select_frozen_scope() -> tuple[
    tuple[str, ...],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    """Discover, and then strictly census, the two pinned reduced-live keys."""
    r184 = strict_json(ROOT / c30b.R184_CERTIFICATE)
    bounded = strict_json(ROOT / c30b.R215_CERTIFICATE)["result"][
        "bounded_probe_result"
    ]
    selected_summaries = sorted(
        (
            row
            for row in bounded["whole_origin_outcome"]["per_origin_rows"]
            if row["first_obstruction"] == REDUCED_LIVE_BLOCKER
        ),
        key=lambda value: value["origin_key"],
    )
    keys = tuple(row["origin_key"] for row in selected_summaries)
    summaries = {row["origin_key"]: row for row in selected_summaries}
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(keys)
    }
    need(
        len(keys) == EXPECTED_ORIGIN_COUNT
        and len(set(keys)) == EXPECTED_ORIGIN_COUNT
        and tuple(sorted(keys)) == keys
        and set(registry) == set(keys)
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
            for summary in selected_summaries
        ),
        "dynamic pinned reduced-live two-origin selection",
    )
    return keys, registry, summaries


def exact_atomic_closure(owner_audit: dict[str, Any]) -> bool:
    exact = owner_audit["exact_3D_enclosure"]
    return bool(
        exact["all_leaf_boxes_contained_in_parent_and_nondegenerate"]
        and exact["pairwise_leaf_interiors_disjoint"]
        and exact["leaf_exact_volume_sum_equals_parent"]
        and owner_audit["all_raw_2D_strata_exactly_reclosed"]
        and owner_audit["all_raw_1D_strata_exactly_reclosed"]
        and owner_audit["atomic_2D_owner_row_count"] > 0
        and owner_audit["atomic_1D_owner_row_count"] > 0
        and owner_audit["atomic_0D_owner_row_count"] > 0
    )


def producer_materialize_atomic_owner_rows(
    parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    leaf_disposition: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Materialize the complete mixed 3D/2D/1D/0D owner complex.

    This implementation is local to the producer.  The verifier has a
    separately written materializer and never imports this module.
    """
    axes = ("t", "p", "s")
    origin = next(iter(leaf_rows.values())).origin_key
    bounds = {
        key: {
            "t": (row.box.t0, row.box.t1),
            "p": (row.box.p0, row.box.p1),
            "s": (row.box.s0, row.box.s1),
        }
        for key, row in leaf_rows.items()
    }
    need(
        bool(bounds)
        and set(bounds) == set(proof_source) == set(leaf_disposition),
        "complete producer atomic owner maps:" + origin,
    )
    grid = {
        axis: sorted({value for box in bounds.values() for value in box[axis]})
        for axis in axes
    }

    def parts(
        geometry: dict[str, Any],
    ) -> tuple[dict[str, Q], dict[str, tuple[Q, Q]]]:
        return (
            {axis: Q(value) for axis, value in geometry["fixed"].items()},
            {
                axis: (Q(span[0]), Q(span[1]))
                for axis, span in geometry["open_spans"].items()
            },
        )

    def atom(
        dimension: int,
        geometry: dict[str, Any],
        incident_sources: list[str],
    ) -> dict[str, Any]:
        fixed, spans = parts(geometry)
        midpoints = {
            axis: (lower + upper) / 2
            for axis, (lower, upper) in spans.items()
        }
        containing = sorted(
            key for key, box in bounds.items()
            if all(
                box[axis][0] <= value <= box[axis][1]
                for axis, value in fixed.items()
            )
            and all(
                box[axis][0] <= lower < upper <= box[axis][1]
                for axis, (lower, upper) in spans.items()
            )
            and all(
                box[axis][0] < value < box[axis][1]
                for axis, value in midpoints.items()
            )
        )
        need(bool(containing), "producer atomic owner exists:" + origin)
        owner = containing[0]
        incidence_rows: list[dict[str, Any]] = []
        for leaf_key in containing:
            signature: dict[str, str] = {}
            for axis, value in sorted(fixed.items()):
                if value == bounds[leaf_key][axis][0]:
                    signature[axis] = "LOWER"
                elif value == bounds[leaf_key][axis][1]:
                    signature[axis] = "UPPER"
            incidence_rows.append(sealed_row({
                "schema": "cm2.round306c30e.atomic-leaf-incidence.row.v2",
                "leaf_key": leaf_key,
                "relative_boundary_signature": signature,
                "relative_boundary_codimension": len(signature),
                "selected_by_half_open_owner": leaf_key == owner,
                "proof_source": proof_source[leaf_key],
                "leaf_disposition": leaf_disposition[leaf_key],
            }))
        measure = Q(1)
        for lower, upper in spans.values():
            measure *= upper - lower
        sources = sorted(set(incident_sources))
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
            "exact_measure": fraction(measure),
            "measure_kind": (
                "COUNTING_0D" if dimension == 0 else f"LEBESGUE_{dimension}D"
            ),
            "incident_sources": sources,
            "incident_source_count": len(sources),
            "closed_containing_leaf_keys": containing,
            "closed_incident_leaf_rows": incidence_rows,
            "closed_incident_leaf_rows_sha256": digest(incidence_rows),
            "half_open_owner_leaf_key": owner,
            "owner_selection_rule": (
                "DETERMINISTIC_LEAF_KEY_LEXICOGRAPHIC_MIN_CONTAINING_LEAF"
            ),
            "owner_proof_source": proof_source[owner],
            "owner_disposition": leaf_disposition[owner],
            "cross_dimensional_source_incidence_complete": True,
        }
        if dimension == 3:
            need(len(containing) == 1,
                 "unique producer open 3D leaf atom:" + origin)
            source_row = {
                "leaf_key": owner,
                "exact_closed_box": r176.box_row(leaf_rows[owner].box),
                "proof_source": proof_source[owner],
                "disposition": leaf_disposition[owner],
            }
            body["source_3D_leaf_row"] = source_row
            body["source_3D_leaf_row_sha256"] = digest(source_row)
        return sealed_row(body)

    rows_3d = [
        atom(
            3,
            {
                "fixed": {},
                "open_spans": {
                    axis: [fraction(bounds[key][axis][0]),
                           fraction(bounds[key][axis][1])]
                    for axis in axes
                },
            },
            ["CLOSED_3D_LEAF:" + key + ":" + proof_source[key]],
        )
        for key in sorted(bounds)
    ]

    face_groups: dict[str, dict[str, Any]] = {}
    for leaf_key, box in sorted(bounds.items()):
        for fixed_axis in axes:
            free_axes = [axis for axis in axes if axis != fixed_axis]
            for side, coordinate in (
                ("LOWER", box[fixed_axis][0]),
                ("UPPER", box[fixed_axis][1]),
            ):
                interval_lists: list[list[tuple[Q, Q]]] = []
                for axis in free_axes:
                    coordinates = [
                        value for value in grid[axis]
                        if box[axis][0] <= value <= box[axis][1]
                    ]
                    interval_lists.append(list(zip(
                        coordinates, coordinates[1:]
                    )))
                for product in itertools.product(*interval_lists):
                    geometry = {
                        "fixed": {fixed_axis: fraction(coordinate)},
                        "open_spans": {
                            axis: [fraction(span[0]), fraction(span[1])]
                            for axis, span in zip(
                                free_axes, product, strict=True
                            )
                        },
                    }
                    key = canonical(geometry).decode("ascii")
                    group = face_groups.setdefault(
                        key, {"geometry": geometry, "sources": []}
                    )
                    group["sources"].append(
                        "LEAF_FACE:" + leaf_key + ":" + fixed_axis + ":" + side
                    )
    rows_2d = [
        atom(2, group["geometry"], group["sources"])
        for _key, group in sorted(face_groups.items())
    ]

    line_groups: dict[str, dict[str, Any]] = {}
    for face in rows_2d:
        fixed, spans = parts(face["geometry"])
        for boundary_axis in sorted(spans):
            free_axis = next(axis for axis in spans if axis != boundary_axis)
            for side, endpoint in (
                ("LOWER", spans[boundary_axis][0]),
                ("UPPER", spans[boundary_axis][1]),
            ):
                geometry = {
                    "fixed": {
                        axis: fraction(value)
                        for axis, value in sorted({
                            **fixed, boundary_axis: endpoint,
                        }.items())
                    },
                    "open_spans": {
                        free_axis: [
                            fraction(spans[free_axis][0]),
                            fraction(spans[free_axis][1]),
                        ]
                    },
                }
                key = canonical(geometry).decode("ascii")
                group = line_groups.setdefault(
                    key, {"geometry": geometry, "sources": []}
                )
                group["sources"].append(
                    "ATOMIC_2D:" + face["row_sha256"] + ":"
                    + boundary_axis + ":" + side
                )
    rows_1d = [
        atom(1, group["geometry"], group["sources"])
        for _key, group in sorted(line_groups.items())
    ]

    point_groups: dict[str, dict[str, Any]] = {}
    for line in rows_1d:
        fixed, spans = parts(line["geometry"])
        free_axis, span = next(iter(spans.items()))
        for side, endpoint in (("LOWER", span[0]), ("UPPER", span[1])):
            geometry = {
                "fixed": {
                    axis: fraction(value)
                    for axis, value in sorted({**fixed, free_axis: endpoint}.items())
                },
                "open_spans": {},
            }
            key = canonical(geometry).decode("ascii")
            group = point_groups.setdefault(
                key, {"geometry": geometry, "sources": []}
            )
            group["sources"].append(
                "ATOMIC_1D:" + line["row_sha256"] + ":" + side
            )
    rows_0d = [
        atom(0, group["geometry"], group["sources"])
        for _key, group in sorted(point_groups.items())
    ]
    all_rows = sorted(
        rows_3d + rows_2d + rows_1d + rows_0d,
        key=lambda row: row["ledger_order_key"],
    )
    need(
        all(rows for rows in (rows_3d, rows_2d, rows_1d, rows_0d))
        and all(row["incident_source_count"] > 0 for row in all_rows)
        and set(row["owner_disposition"] for row in all_rows)
        <= {"EXCLUDED", "LIVE", "MIXED"},
        "complete producer mixed atomic dimensions:" + origin,
    )

    parent_volume = r215.box_volume(parent)
    leaf_volume = sum(
        (r215.box_volume(row.box) for row in leaf_rows.values()), Q(0)
    )
    pair_rows: list[dict[str, Any]] = []
    ordered = sorted(bounds)
    for first_ordinal, first in enumerate(ordered):
        for second in ordered[first_ordinal + 1:]:
            overlap = all(
                max(bounds[first][axis][0], bounds[second][axis][0])
                < min(bounds[first][axis][1], bounds[second][axis][1])
                for axis in axes
            )
            need(not overlap,
                 "producer atomic 3D leaf interior overlap:" + origin)
            pair_rows.append({
                "first": first,
                "second": second,
                "interior_overlap": overlap,
            })
    need(leaf_volume == parent_volume,
         "producer atomic 3D volume exhaustion:" + origin)
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
        "closed_3D_leaf_count": len(leaf_rows),
        "closed_3D_leaf_keys_sha256": digest(sorted(leaf_rows)),
        "closed_3D_leaf_proof_sources_sha256": digest(proof_source),
        "closed_3D_leaf_dispositions_sha256": digest(leaf_disposition),
        "parent_exact_volume": fraction(parent_volume),
        "closed_3D_leaf_exact_volume_sum": fraction(leaf_volume),
        "tested_unordered_3D_leaf_pair_count": len(pair_rows),
        "tested_unordered_3D_leaf_pairs_sha256": digest(pair_rows),
        "axis_grid_coordinates_sha256": digest({
            axis: [fraction(value) for value in values]
            for axis, values in grid.items()
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


def whole_origin_row(
    ordinal: int,
    origin: str,
    replay: dict[str, Any],
    roots: list[Any],
    base_rows: list[Any],
    refinement: dict[str, Any],
    leaves: dict[str, Any],
    h_rows: list[dict[str, Any]],
    live_rows: list[dict[str, Any]],
    final_closed_sources: dict[str, dict[str, Any]],
    registry: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Compose every top-level leaf and every half-open lower stratum."""
    prior = c30a.generalized_prior_partition(replay, origin)
    inherited = sorted(
        refinement["terminal_rows"], key=lambda value: value["cell_key"]
    )
    final_rows = sorted(
        refinement["final_residual_rows"], key=lambda value: value.key
    )
    h_rows = sorted(h_rows, key=lambda value: value["cell_key"])
    live_rows = sorted(live_rows, key=lambda value: value["cell_key"])
    h_by_key = {row["cell_key"]: row for row in h_rows}
    live_by_key = {row["cell_key"]: row for row in live_rows}
    need(
        set(h_by_key).isdisjoint(live_by_key)
        and set(final_closed_sources).isdisjoint(h_by_key)
        and set(final_closed_sources).isdisjoint(live_by_key),
        "disjoint origin lineage buckets:" + origin,
    )

    audit_leaf_rows: dict[str, Any] = dict(prior["prior_closed_rows"])
    audit_leaf_rows.update({row.key: row for row in base_rows})
    audit_leaf_rows.update(leaves["terminal"])
    audit_leaf_rows.update(leaves["final"])
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED"
        for key in prior["prior_closed_rows"]
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED" for row in base_rows
    })
    leaf_disposition = {
        key: "EXCLUDED" for key in prior["prior_closed_rows"]
    }
    leaf_disposition.update({row.key: "EXCLUDED" for row in base_rows})

    inherited_keys = {row["cell_key"] for row in inherited}
    final_keys = {row.key for row in final_rows}
    for evidence in inherited:
        key = evidence["cell_key"]
        if key in h_by_key:
            proof_source[key] = "ROUND306C30E_MATERIALIZED_INHERITED_H"
            leaf_disposition[key] = h_by_key[key][
                "whole_H_cell_disposition"
            ]
        elif key in live_by_key:
            proof_source[key] = "ROUND306C30E_PINNED_ROUND180_STRICT_LIVE"
            leaf_disposition[key] = "LIVE"
        else:
            need(
                evidence["coarse_disposition"] == "EXCLUDED",
                "unbound inherited nonexclusion:" + key,
            )
            proof_source[key] = "PINNED_ROUND180_INHERITED_EXCLUDED"
            leaf_disposition[key] = "EXCLUDED"
    for row in final_rows:
        key = row.key
        if key in h_by_key:
            proof_source[key] = "ROUND306C30E_MATERIALIZED_FINAL_H"
            leaf_disposition[key] = h_by_key[key][
                "whole_H_cell_disposition"
            ]
        elif key in live_by_key:
            proof_source[key] = "ROUND306C30E_REDUCED_STRICT_LIVE"
            leaf_disposition[key] = "LIVE"
        else:
            need(key in final_closed_sources, "unbound final leaf:" + key)
            proof_source[key] = final_closed_sources[key]["source_kind"]
            leaf_disposition[key] = "EXCLUDED"
    need(
        set(proof_source) == set(leaf_disposition) == set(audit_leaf_rows)
        and set(h_by_key) | set(live_by_key) | set(final_closed_sources)
        <= inherited_keys | final_keys,
        "complete origin proof/disposition maps:" + origin,
    )

    owner_slice, owner_rows = producer_materialize_atomic_owner_rows(
        replay["origins"][origin]["box"],
        audit_leaf_rows,
        proof_source,
        leaf_disposition,
    )

    disposition_census = Counter(leaf_disposition.values())
    disposition_support = set(disposition_census)
    if disposition_support == {"EXCLUDED"}:
        whole_disposition = "EXCLUDED"
    elif disposition_support == {"LIVE"}:
        whole_disposition = "RESOLVED_LIVE"
    else:
        need(
            disposition_support <= {"EXCLUDED", "LIVE", "MIXED"},
            "origin disposition support:" + origin,
        )
        whole_disposition = "RESOLVED_MIXED"

    reduced_live_rows = [
        row for row in live_rows
        if row["source_kind"] == "ROUND215_REDUCED_LIVE_3D_CELL"
    ]
    inherited_live_rows = [
        row for row in live_rows
        if row["source_kind"] == "ROUND180_DIRECT_STRICT_LIVE"
    ]
    final_h_rows = [
        row for row in h_rows
        if row["source_kind"] == "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H"
    ]
    inherited_h_rows = [
        row for row in h_rows
        if row["source_kind"].startswith("ROUND180_INHERITED_")
    ]
    h_partitions_exact = all(
        row["H_partition"][
            "exact_exhaustive_disjoint_3D_2D_1D_0D_partition_verified"
        ] is True
        for row in h_rows
    )
    strict_live_partitions_exact = all(
        row["partition_theorem"]["all_3D_2D_1D_0D_strata_disposed"]
        and row["outer_boundary_restriction_row_count"] == 26
        for row in live_rows
    )
    need(
        len(reduced_live_rows) == EXPECTED_REDUCED_LIVE_PER_ORIGIN
        and len(final_h_rows) == EXPECTED_OUTGOING_H_PER_ORIGIN
        and bool(reduced_live_rows)
        and "EXCLUDED" in disposition_support
        and "LIVE" in disposition_support
        and whole_disposition == "RESOLVED_MIXED"
        and h_partitions_exact
        and strict_live_partitions_exact,
        "reduced-live whole-origin candidate theorem:" + origin,
    )

    parent_volume = r215.box_volume(replay["origins"][origin]["box"])
    disposition_volumes: defaultdict[str, Q] = defaultdict(Q)
    for key, row in audit_leaf_rows.items():
        disposition_volumes[leaf_disposition[key]] += r215.box_volume(row.box)
    need(
        sum(disposition_volumes.values(), Q(0)) == parent_volume
        and disposition_volumes["LIVE"] > 0
        and disposition_volumes["EXCLUDED"] > 0,
        "origin disposition volume control:" + origin,
    )
    first_live = min(
        (
            {
                "cell_key": row["cell_key"],
                "source_kind": row["source_kind"],
                "exact_volume": row["exact_volume"],
                "strictly_positive_measure": Q(row["exact_volume"]) > 0,
            }
            for row in live_rows
        ),
        key=canonical,
    )
    theorem = {
        "kind": (
            "SOURCE_W_REDUCED_LIVE_WHOLE_ORIGIN_"
            "RESOLVED_MIXED_THEOREM_CANDIDATE"
        ),
        "origin_selected_dynamically_from_pinned_Round215_blocker": True,
        "top_level_dyadic_leaf_partition_exact": True,
        "top_level_leaf_disposition_support": sorted(disposition_support),
        "every_H_cell_has_exact_exhaustive_3D_2D_1D_0D_partition": (
            h_partitions_exact
        ),
        "every_strict_LIVE_cell_and_outer_stratum_is_LIVE": (
            strict_live_partitions_exact
        ),
        "whole_origin_half_open_atomic_3D_2D_1D_0D_owner_audit": True,
        "positive_measure_LIVE_subset_exists": True,
        "positive_measure_EXCLUDED_subset_exists": True,
        "whole_original_physical_origin_disposition": "RESOLVED_MIXED",
        "whole_original_physical_origin_excluded": False,
        "child_count_sheet_count_or_volume_used_as_integer_credit": False,
    }
    body = {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live."
            "whole-origin-row.candidate.v1"
        ),
        "origin_ordinal": ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": replay["origins"][origin]["chart_id"],
        "original_parent_box": r176.box_row(
            replay["origins"][origin]["box"]
        ),
        "lineage_census": {
            "Round176_prior_closed": prior["prior_closed_count"],
            "Round176_preclosed": len(base_rows),
            "Round176_residual_roots": len(roots),
            "Round180_inherited_total": len(inherited),
            "Round180_inherited_H_materialized": len(inherited_h_rows),
            "Round180_inherited_direct_LIVE": len(inherited_live_rows),
            "Round180_final_total": len(final_rows),
            "Round215_reduced_LIVE": len(reduced_live_rows),
            "Round215_reduced_unique_first_outgoing_H": len(final_h_rows),
            "final_closed": len(final_closed_sources),
            "atomic_top_level_leaf_count": len(audit_leaf_rows),
        },
        "top_level_leaf_disposition_census": dict(sorted(
            disposition_census.items()
        )),
        "top_level_disposition_exact_volumes": {
            key: fraction(value)
            for key, value in sorted(disposition_volumes.items())
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
            for key, value in sorted(final_closed_sources.items())
        ],
        "atomic_half_open_owner_ledger_slice": owner_slice,
        "exact_volume_conservation": {
            "original_parent": fraction(parent_volume),
            "sum_by_top_level_disposition": fraction(sum(
                disposition_volumes.values(), Q(0)
            )),
            "all_equalities_verified": True,
        },
        "lexicographic_first_positive_measure_LIVE_witness": first_live,
        "whole_origin_theorem_candidate": theorem,
        "whole_origin_theorem_candidate_sha256": digest(theorem),
        "whole_origin_disposition": whole_disposition,
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
    return sealed_row(body), owner_rows


def build(candidate_path: Path) -> dict[str, Any]:
    validate_runtime_and_contracts()
    c30d_authority = capture_c30d_authority()
    ctx.prec = 192
    candidate = candidate_directory(candidate_path)
    runtime_path = candidate / c30b.RUNTIME_ATTESTATION
    runtime_path.write_bytes(c30b.BOOTSTRAP_RUNTIME_ATTESTATION_RAW)
    need(
        file_hash(runtime_path) == c30b.RUNTIME_ATTESTATION_RAW_SHA256,
        "published runtime attestation bytes",
    )

    origin_keys, registry, summaries = select_frozen_scope()
    replay = r176.replay_frontier()
    target_set = set(origin_keys)
    roots_by_origin: dict[str, list[Any]] = defaultdict(list)
    base_by_origin: dict[str, list[Any]] = defaultdict(list)
    base_kinds: dict[str, set[str]] = defaultdict(set)
    for row in replay["frontier"]:
        if row.origin_key not in target_set:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots_by_origin[row.origin_key].append(row)
        else:
            base_by_origin[row.origin_key].append(row)
            base_kinds[row.origin_key].add(kind)
    need(
        set(roots_by_origin) == target_set
        and all(base_kinds[key] <= {"EXCLUDED"} for key in origin_keys),
        "dynamic two-origin frozen base reconstruction",
    )

    all_h_rows: list[dict[str, Any]] = []
    all_live_rows: list[dict[str, Any]] = []
    all_atomic_owner_rows: list[dict[str, Any]] = []
    origin_rows: list[dict[str, Any]] = []
    for origin_ordinal, origin in enumerate(origin_keys):
        roots = sorted(
            roots_by_origin[origin], key=lambda value: value.key
        )
        base_rows = sorted(
            base_by_origin[origin], key=lambda value: value.key
        )
        refinement = r180.refine_origin(roots, 4)
        leaves = r215.reconstruct_refinement_leaf_frontiers(
            roots, refinement
        )
        h_rows: list[dict[str, Any]] = []
        live_rows: list[dict[str, Any]] = []

        for evidence in sorted(
            refinement["terminal_rows"],
            key=lambda value: value["cell_key"],
        ):
            if evidence["coarse_disposition"] == "EXCLUDED":
                continue
            frontier = leaves["terminal"][evidence["cell_key"]]
            if evidence["method"] == "DIRECT_STRICT_CLOSED_BOX":
                leaf, _records = r176.classify(
                    frontier.chart_id,
                    frontier.box,
                    frontier.active_targets,
                )
                replayed_disposition, _margins = r176.terminal_disposition(
                    frontier.chart_id, leaf
                )
                need(
                    evidence["coarse_disposition"] == "LIVE"
                    and evidence["disposition"] == replayed_disposition
                    and evidence["all_owned_boundary_strata_inherit_strict_proof"]
                    is True,
                    "Round180 direct strict LIVE:" + frontier.key,
                )
                body = strict_live_cell_body(
                    frontier,
                    source_kind="ROUND180_DIRECT_STRICT_LIVE",
                    leaf=leaf,
                    strict_disposition=evidence["disposition"],
                    source_binding={
                        "Round180_terminal_evidence": evidence,
                        "Round180_terminal_sha256": evidence["terminal_sha256"],
                        "replayed_terminal_disposition": replayed_disposition,
                    },
                    exact_behind_candidate_evidence=[],
                )
                live_rows.append(sealed_row(body))
                continue
            if evidence["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE":
                source_kind, source_binding = c30b.inherited_source_binding(
                    evidence, None
                )
            else:
                need(
                    evidence["method"]
                    == "SAME_SIGN_MONOTONE_DELTA_CLOSED_BOX",
                    "unexpected inherited nonexclusion:" + frontier.key,
                )
                source_kind = "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
                source_binding = (
                    c30b.inherited_same_sign_delta_followup_h_binding(evidence)
                )
            h_rows.append(sealed_row(h_cell_candidate_body(
                source_kind, frontier, source_binding
            )))

        final_closed_sources: dict[str, dict[str, Any]] = {}
        rebuilt_reduced_live = 0
        rebuilt_outgoing_h = 0
        for row in sorted(
            refinement["final_residual_rows"], key=lambda value: value.key
        ):
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            reduction_binding = c30b.reduction_binding(reduction)
            if reduction["closed"]:
                final_closed_sources[row.key] = {
                    "source_kind": "ROUND201_EXACT_BEHIND_EXCLUDED",
                    "reduction_sha256": digest(reduction_binding),
                }
                continue
            evidence = c30b.reconstructed_r215_evidence(row, reduction)
            if evidence["analytic_closed"]:
                final_closed_sources[row.key] = {
                    "source_kind": "ROUND215_ANALYTIC_EXCLUDED",
                    "Round215_cell_row_sha256": evidence["row_sha256"],
                }
                continue
            if evidence["blocker"] == REDUCED_LIVE_BLOCKER:
                need(
                    reduction["residual_reason"]
                    == "REDUCED_REMAINING_DISPOSITION_LIVE"
                    and reduction["disposition"] is not None
                    and reduction["disposition"].startswith("LIVE")
                    and bool(reduction["eligible_targets"]),
                    "pinned reduced-live reduction:" + row.key,
                )
                body = strict_live_cell_body(
                    row,
                    source_kind="ROUND215_REDUCED_LIVE_3D_CELL",
                    leaf=reduction["leaf"],
                    strict_disposition=reduction["disposition"],
                    source_binding={
                        "Round215_cell_evidence": evidence,
                        "Round215_cell_row_sha256": evidence["row_sha256"],
                        "Round215_reduction": reduction_binding,
                        "Round215_reduction_sha256": digest(reduction_binding),
                    },
                    exact_behind_candidate_evidence=[
                        candidate
                        for candidate in reduction["candidate_evidence"]
                        if candidate["eligible_exact_behind"]
                    ],
                )
                live_rows.append(sealed_row(body))
                rebuilt_reduced_live += 1
                continue
            need(
                evidence["blocker"] == OUTGOING_H_BLOCKER
                and reduction["leaf"].classification == "unique_first"
                and reduction["leaf"].owner_target == r176.FROZEN_OWNER,
                "unexpected reduced-live-lane residual:" + row.key,
            )
            h_rows.append(sealed_row(h_cell_candidate_body(
                "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H",
                row,
                c30b.r215_source_binding(evidence, reduction),
            )))
            rebuilt_outgoing_h += 1

        summary = summaries[origin]
        need(
            rebuilt_reduced_live == EXPECTED_REDUCED_LIVE_PER_ORIGIN
            and rebuilt_outgoing_h == EXPECTED_OUTGOING_H_PER_ORIGIN
            and summary["Round215_analytic_closed_cell_count"] == sum(
                value["source_kind"] == "ROUND215_ANALYTIC_EXCLUDED"
                for value in final_closed_sources.values()
            ),
            "per-origin reduced-live final census:" + origin,
        )
        origin_row, owner_rows = whole_origin_row(
            origin_ordinal,
            origin,
            replay,
            roots,
            base_rows,
            refinement,
            leaves,
            h_rows,
            live_rows,
            final_closed_sources,
            registry[origin],
        )
        all_h_rows.extend(h_rows)
        all_live_rows.extend(live_rows)
        all_atomic_owner_rows.extend(owner_rows)
        origin_rows.append(origin_row)

    all_h_rows.sort(key=lambda value: value["cell_key"])
    all_live_rows.sort(key=lambda value: value["cell_key"])
    all_atomic_owner_rows.sort(key=lambda value: value["ledger_order_key"])
    origin_rows.sort(key=lambda value: value["origin_key"])
    need(
        len(origin_rows) == EXPECTED_ORIGIN_COUNT
        and [row["origin_key"] for row in origin_rows] == list(origin_keys)
        and all(
            row["whole_origin_disposition"] == "RESOLVED_MIXED"
            and row["whole_original_physical_origin_excluded"] is False
            and set(row["formal_credit"].values()) == {0}
            for row in origin_rows
        )
        and sum(
            row["source_kind"] == "ROUND215_REDUCED_LIVE_3D_CELL"
            for row in all_live_rows
        ) == EXPECTED_ORIGIN_COUNT * EXPECTED_REDUCED_LIVE_PER_ORIGIN
        and sum(
            row["source_kind"]
            == "ROUND215_REDUCED_UNIQUE_FIRST_OUTGOING_H"
            for row in all_h_rows
        ) == EXPECTED_ORIGIN_COUNT * EXPECTED_OUTGOING_H_PER_ORIGIN
        and all(set(row["formal_credit"].values()) == {0}
                for row in all_h_rows + all_live_rows),
        "global C30e candidate census and zero formal credit",
    )
    need(
        bool(all_atomic_owner_rows)
        and [row["ledger_order_key"] for row in all_atomic_owner_rows]
        == sorted(row["ledger_order_key"] for row in all_atomic_owner_rows)
        and set(row["origin_key"] for row in all_atomic_owner_rows)
        == set(origin_keys)
        and set(row["ambient_dimension"] for row in all_atomic_owner_rows)
        == {0, 1, 2, 3},
        "global external atomic owner ledger completeness/order",
    )

    h_count, h_sequence = write_rows(candidate / H_CELL_LEDGER, all_h_rows)
    live_count, live_sequence = write_rows(
        candidate / LIVE_CELL_LEDGER, all_live_rows
    )
    origin_count, origin_sequence = write_rows(
        candidate / ORIGIN_LEDGER, origin_rows
    )
    owner_count, owner_sequence = write_rows(
        candidate / ATOMIC_OWNER_LEDGER, all_atomic_owner_rows
    )
    h_descriptor = descriptor(
        candidate / H_CELL_LEDGER,
        h_count,
        h_sequence,
        "LEXICOGRAPHIC_SOURCE_W_CELL_KEY",
    )
    live_descriptor = descriptor(
        candidate / LIVE_CELL_LEDGER,
        live_count,
        live_sequence,
        "LEXICOGRAPHIC_SOURCE_W_CELL_KEY",
    )
    origin_descriptor = descriptor(
        candidate / ORIGIN_LEDGER,
        origin_count,
        origin_sequence,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    owner_descriptor = descriptor(
        candidate / ATOMIC_OWNER_LEDGER,
        owner_count,
        owner_sequence,
        "LEXICOGRAPHIC_ORIGIN_THEN_DESCENDING_DIMENSION_THEN_GEOMETRY_SHA256",
    )
    runtime_descriptor = {
        "filename": c30b.RUNTIME_ATTESTATION,
        "size": len(c30b.BOOTSTRAP_RUNTIME_ATTESTATION_RAW),
        "sha256": c30b.RUNTIME_ATTESTATION_RAW_SHA256,
        "attestation_payload_sha256": (
            c30b.RUNTIME_ATTESTATION_PAYLOAD_SHA256
        ),
        "auditor_sha256": c30b.RUNTIME_AUDITOR_SHA256,
        "schema": c30b.BOOTSTRAP_RUNTIME_ATTESTATION["schema"],
        "verdict": c30b.BOOTSTRAP_RUNTIME_ATTESTATION["verdict"],
    }
    input_pins = sorted(
        c30b.INPUT_PINS
        + [{"filename": C30B_SOURCE, "sha256": C30B_SOURCE_SHA256}]
        + [
            {"filename": filename, "sha256": sha256}
            for filename, sha256 in c30d_authority["pins"].items()
        ],
        key=lambda value: value["filename"],
    )
    h_census = Counter(
        row["whole_H_cell_disposition"] for row in all_h_rows
    )
    live_source_census = Counter(row["source_kind"] for row in all_live_rows)
    body = {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live-"
            "whole-origin-disposition.candidate.v1"
        ),
        "status": (
            "PASS_CANDIDATE_ROUND306C30E_REDUCED_LIVE_DISPOSITION__"
            "AWAITING_INDEPENDENT_VERIFICATION_AND_RELEASE_CONTROLS"
        ),
        "input_pins": input_pins,
        "runtime_attestation": runtime_descriptor,
        "controlled_dual_hash_seed_contract": {
            "required_launch": (
                "env -i HOME=/nonexistent LC_ALL=C.UTF-8 TZ=UTC "
                "PYTHONHASHSEED=<30630071|30630929> python -P -s -B"
            ),
            "accepted_seeds": sorted(CONTROLLED_HASH_SEEDS),
            "hash_seed_sentinel": HASH_SEED_SENTINEL,
            "hash_fingerprints": {
                key: value for key, value in sorted(HASH_FINGERPRINTS.items())
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
                for row in all_h_rows
            ),
        },
        "cell_census": {
            "H_cell_count": len(all_h_rows),
            "H_cell_by_disposition": dict(sorted(h_census.items())),
            "strict_LIVE_cell_count": len(all_live_rows),
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
                "producer_source": C30B_SOURCE,
                "producer_source_sha256": C30B_SOURCE_SHA256,
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
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    need(
        {path.name for path in candidate.iterdir()} == {
            H_CELL_LEDGER,
            LIVE_CELL_LEDGER,
            ATOMIC_OWNER_LEDGER,
            ORIGIN_LEDGER,
            RESULT,
            c30b.RUNTIME_ATTESTATION,
        },
        "candidate final exact file set",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    arguments = parser.parse_args()
    result = build(Path(arguments.candidate_dir))
    print(canonical({
        "status": result["status"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
