#!/usr/bin/env python3
"""Independent reconstruction verifier for Round306C30a.

This verifier never imports or executes the C30a producer.  It pins and
replays the sealed R184/R215/C29 sources, reconstructs every candidate cell
and whole-origin row, and compares the complete canonical result object.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator

sys.dont_write_bytecode = True

import flint
from flint import arb, ctx


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
CELL_LEDGER = PREFIX + "_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
HELD_LEDGER = PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
PRODUCER = PREFIX + "_producer.py"

R215_PROBE = "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
R215_CERTIFICATE = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_certificate.json"
)
R215_VERIFICATION = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_verification.json"
)
R215_MANIFEST = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_manifest.sha256"
)
R184_PRODUCER = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py"
)
R184_VERIFICATION = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "verification.json"
)
R184_MANIFEST = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "manifest.sha256"
)
C29_RESULT = (
    "cm2_round306c29_source_g_maximal_component_official_key_fibre_"
    "exhaustion_and_global_disposition_result.json"
)
C29_VERIFICATION = (
    "cm2_round306c29_source_g_maximal_component_official_key_fibre_"
    "exhaustion_and_global_disposition_verification.json"
)
C29_MANIFEST = (
    "cm2_round306c29_source_g_maximal_component_official_key_fibre_"
    "exhaustion_and_global_disposition_manifest.sha256"
)
RUNTIME_REQUIREMENTS = "cm2_round306c30a_python_flint_requirements.lock"
RUNTIME_LOCK = "cm2_round306c30a_python_flint_runtime_lock.json"

PINS = {
    R215_PROBE:
        "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1",
    R215_CERTIFICATE:
        "9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec",
    R215_VERIFICATION:
        "9af901607edd4b95f1ec149bb6426a84315de22decbcd331a8d71d727894c519",
    R215_MANIFEST:
        "6a6463c2574b971ce6909593886f6ad4c23bddb232772fdacebb4ecca70a405a",
    R184_PRODUCER:
        "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906",
    R184_VERIFICATION:
        "7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6",
    R184_MANIFEST:
        "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1",
    C29_RESULT:
        "2631e8f1e2603125e9b7d54410dd24784026ad2a6c478bcc7bab76f410e02b02",
    C29_VERIFICATION:
        "cb387139cf7709731d3f2ab7adc8962f5edea750dd1480f7baacf9f43b9f541a",
    C29_MANIFEST:
        "6ef42986bd1fd6b7ae99a57aebb0f5445d107e5cffe1543703a1dfb1fede6aa0",
    RUNTIME_REQUIREMENTS:
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    RUNTIME_LOCK:
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
}

R215_BOUNDED_RESULT_SHA256 = (
    "e6af59b19440723c4770a286d6261d950fb2a22702ec8900d285b43a06d0158c"
)
R215_CELL_ROWS_SHA256 = (
    "50431dc6c73add077aef263c781df428d81493751250bf1683f9c560faa420d9"
)
EXPECTED_ACTIVE_CELLS = 18_432
EXPECTED_CLIPPED_CELLS = 12_888
EXPECTED_CLIPPED_CLOSED = 12_868
EXPECTED_CLIPPED_RESIDUAL = 20
EXPECTED_CANDIDATE_ORIGINS = 162
EXPECTED_PROMOTED_ORIGINS = 160
EXPECTED_HELD_ORIGINS = 2
EXPECTED_PROMOTED_RESIDUAL_CELLS = 14_228
EXPECTED_PROMOTED_OLD_CLOSED_CELLS = 3_428
EXPECTED_PROMOTED_NEW_CELLS = 10_800
EXPECTED_HELD_ORIGIN_KEYS = (
    "W:N:04.00.10101011",
    "W:S:H.04.00.10101011",
)
EXPECTED_HELD_ORIGIN_KEYS_SHA256 = (
    "7a41c001b740c99223c152d96e75176b56f6bf083df962155b912e32b43afd08"
)
R215_PROMOTED = 2
R215_EXCLUDED = 74_584
R215_CONSERVATIVE_LIVE = 2_248
R215_REMAINING = 252
NEW_EXCLUDED = 74_744
NEW_CONSERVATIVE_LIVE = 2_088
NEW_REMAINING = 92


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def regular_bytes(path: Path, maximum: int = 64 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        "regular singleton:" + absolute.name,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino),
            "opened input identity:" + absolute.name,
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(block), "short read:" + absolute.name)
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input:" + absolute.name)
    finally:
        os.close(descriptor)
    return b"".join(chunks)


def strict_object_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "JSON encoding:" + label,
    )

    def reject(value: str) -> None:
        raise Reject("noninteger JSON:" + label + ":" + value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_constant=reject,
        # Sealed verification envelopes contain decimal timing/RSS metadata.
        # Preserve such tokens as strings; canonical candidate equality below
        # still rejects a numeric-float injection because its bytes differ.
        parse_float=str,
    )
    require(type(value) is dict, "JSON top object:" + label)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_object_bytes(regular_bytes(path), path.name)


def validate_runtime() -> None:
    lock = strict_json(ROOT / RUNTIME_LOCK)
    require(
        sys.flags.isolated == 1
        and sys.dont_write_bytecode is True
        and sys.implementation.name == lock["implementation"]
        and os.uname().machine == lock["architecture"]
        and ".".join(str(value) for value in sys.version_info[:3])
        == lock["python_version"]
        and flint.__version__ == lock["python_flint"]
        and flint.__FLINT_VERSION__ == lock["flint_version"]
        and flint.__FLINT_RELEASE__ == lock["flint_release"],
        "locked isolated python-flint runtime",
    )


def validate_sources() -> list[dict[str, str]]:
    pins: list[dict[str, str]] = []
    for filename, expected in sorted(PINS.items()):
        actual = file_hash(ROOT / filename)
        require(actual == expected, "source pin:" + filename)
        pins.append({"filename": filename, "sha256": actual})
    r215_certificate = strict_json(ROOT / R215_CERTIFICATE)
    r215_verification = strict_json(ROOT / R215_VERIFICATION)
    r184_verification = strict_json(ROOT / R184_VERIFICATION)
    c29_result = strict_json(ROOT / C29_RESULT)
    c29_verification = strict_json(ROOT / C29_VERIFICATION)
    require(
        r215_certificate["result"]["bounded_probe_result_sha256"]
        == R215_BOUNDED_RESULT_SHA256
        and r215_verification["result"]["status"]
        == "PASS_PARTIAL_FORMAL_ROUND215"
        and r215_verification["result"]["verdict"] == "PASS"
        and r184_verification["result"]["status"]
        == "PASS_PARTIAL_BOUNDED_ROUND184"
        and c29_result["formal_credit"]["global_disposition"] == 1
        and c29_result["formal_credit"]["maximal_component_assignments"]
        == 57_876
        and c29_result["strict_nonpromotion"]["D02"].startswith(
            "BLOCKED_BY_252"
        )
        and c29_verification["status"].startswith("PASS_INDEPENDENT_C29"),
        "sealed upstream state",
    )
    return pins


validate_runtime()
validate_sources()
if os.fspath(ROOT) not in sys.path:
    sys.path.insert(0, os.fspath(ROOT))
r215 = importlib.import_module(R215_PROBE[:-3])
require(
    Path(r215.__file__).resolve() == (ROOT / R215_PROBE).resolve()
    and file_hash(ROOT / R215_PROBE) == PINS[R215_PROBE],
    "Round215 module identity",
)
r176 = r215.r176
r180 = r215.r180


def capture_round215() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    captured: list[dict[str, Any]] = []
    original = r215.ListDigest.add

    def intercept(instance: Any, value: Any) -> None:
        if (
            type(value) is dict
            and {
                "source_chart_id",
                "closed_box",
                "analytic_closed",
                "method",
                "row_sha256",
            }
            <= set(value)
        ):
            captured.append(value)
        original(instance, value)

    r215.ListDigest.add = intercept
    try:
        bounded = r215.rebuild()
    finally:
        r215.ListDigest.add = original
    require(
        digest(bounded) == R215_BOUNDED_RESULT_SHA256
        and len(captured) == EXPECTED_ACTIVE_CELLS
        and digest(captured) == R215_CELL_ROWS_SHA256,
        "Round215 full independent replay",
    )
    return bounded, captured


def frontier(evidence: dict[str, Any]) -> Any:
    box = evidence["closed_box"]
    return r176.Frontier(
        evidence["source_chart_id"],
        r176.Box(
            Q(box["t"][0]), Q(box["t"][1]),
            Q(box["p"][0]), Q(box["p"][1]),
            Q(box["s"][0]), Q(box["s"][1]),
            0, evidence["cell_key"].split(":", 2)[2],
        ),
        tuple(evidence["active_targets"]),
        evidence["origin_key"],
        evidence["original_failure_type"],
    )


def strict_chart(nx: arb, ny: arb) -> str | None:
    tests = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    choices = [
        key for key, margins in tests.items()
        if bool(margins[0] > 0) and bool(margins[1] > 0)
    ]
    return choices[0] if len(choices) == 1 else None


def tangent_chart(row: Any, candidate: Any) -> str | None:
    _qx, _qy, ux, uy, _s, _rp = r176.geometry(row.chart_id, row.box)
    radius = r176.base.arbq(
        r176.base.RADIUS[r176.TARGETS[candidate.target_id].obstacle]
    )
    return strict_chart(
        candidate.transverse * uy / radius,
        -candidate.transverse * ux / radius,
    )


def sign_name(value: arb) -> str:
    sign = r176.sign(value)
    return (
        "STRICT_POSITIVE" if sign > 0
        else "STRICT_NEGATIVE" if sign < 0
        else "OVERWRAP"
    )


def expected_cell(ordinal: int, evidence: dict[str, Any]) -> dict[str, Any]:
    require(
        evidence["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP",
        "clipped blocker identity",
    )
    row = frontier(evidence)
    reduction = r215.exact_behind_reduce(row, r180.residual_category(row))
    require(
        reduction["category"] == evidence["original_residual_category"]
        and reduction["residual_reason"]
        == evidence["exact_behind_residual_reason"]
        and reduction["eligible_targets"]
        == evidence["eligible_exact_behind_targets"],
        "clipped upstream replay:" + row.key,
    )
    records, centered = r215.enhance_root_sign_records(
        row, reduction["current_records"]
    )
    require(
        centered == evidence["centered_root_sign_evidence"],
        "centered replay:" + row.key,
    )
    unresolved = [
        record for record in records
        if record.classification == "unresolved_discriminant"
    ]
    require(len(unresolved) == 1, "single reduced Delta:" + row.key)
    candidate = unresolved[0]
    derivative, lower, upper, full = r176.graph_faces(row, candidate)
    target_first = r176.target_positive_first(candidate, records)
    negative = r176.remove_disposition(row, records, candidate.target_id)
    positive_chart: str | None = None
    zero_chart: str | None = None
    closed = False
    disposition = "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED"
    if (
        derivative != 0 and not full and target_first
        and negative is not None and negative.startswith("EXCLUDED")
    ):
        if candidate.target_id != r176.FROZEN_OWNER:
            positive_disposition = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            zero_disposition = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
            disposition = "CLOSED_REDUCED_CANDIDATE_OWNER_MISMATCH"
            closed = True
        else:
            positive_chart = r176.positive_chart(row, candidate)
            zero_chart = tangent_chart(row, candidate)
            positive_disposition = (
                "EXCLUDED_OUTGOING_CHART_MISMATCH"
                if positive_chart not in {None, r176.FROZEN_CHART}
                else "UNRESOLVED"
            )
            zero_disposition = (
                "EXCLUDED_OUTGOING_CHART_MISMATCH"
                if zero_chart not in {None, r176.FROZEN_CHART}
                else "UNRESOLVED"
            )
            closed = (
                positive_disposition.startswith("EXCLUDED")
                and zero_disposition.startswith("EXCLUDED")
            )
            disposition = (
                "CLOSED_REDUCED_FROZEN_OWNER_OUTGOING_MISMATCH"
                if closed else "RESIDUAL_REDUCED_FROZEN_OWNER_OUTGOING"
            )
    else:
        positive_disposition = "UNRESOLVED"
        zero_disposition = "UNRESOLVED"
    partition = {
        "kind": "REDUCED_CLIPPED_DELTA_FULL_STRATUM_PARTITION",
        "strict_p_derivative": derivative != 0,
        "full_p_graph": full,
        "graph_nonemptiness_required_for_exclusion": False,
        "Delta_negative_open_3D_disposition": (
            negative if negative is not None else "UNRESOLVED"
        ),
        "Delta_zero_graph_2D_disposition": zero_disposition,
        "Delta_positive_open_3D_disposition": positive_disposition,
        "graph_face_intersection_outer_dimension": 1,
        "graph_edge_or_corner_intersection_outer_dimension": 0,
        "all_graph_face_edge_corner_strata_inherit_the_graph_disposition":
            closed,
        "closed_box_and_all_owned_faces_edges_vertices_excluded": closed,
        "only_complete_closed_box_may_contribute_to_whole_origin_credit":
            True,
    }
    body = {
        "schema": (
            "cm2.round306c30a.source-w-reduced-clipped-delta."
            "cell-row.v1"
        ),
        "cell_ordinal": ordinal,
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "source_chart_id": row.chart_id,
        "closed_box": evidence["closed_box"],
        "active_targets": list(row.active_targets),
        "candidate_target": candidate.target_id,
        "candidate_is_frozen_owner": candidate.target_id == r176.FROZEN_OWNER,
        "strict_p_derivative_sign": (
            "STRICT_POSITIVE" if derivative > 0
            else "STRICT_NEGATIVE" if derivative < 0
            else "OVERWRAP"
        ),
        "p_lower_face_sign": sign_name(lower),
        "p_upper_face_sign": sign_name(upper),
        "target_strict_positive_first": target_first,
        "negative_open_side_disposition": (
            negative if negative is not None else "UNRESOLVED"
        ),
        "positive_open_side_outgoing_chart": (
            positive_chart if positive_chart is not None else "NOT_APPLICABLE"
        ),
        "zero_graph_outgoing_chart": (
            zero_chart if zero_chart is not None else "NOT_APPLICABLE"
        ),
        "partition": partition,
        "partition_sha256": digest(partition),
        "disposition": disposition,
        "whole_closed_cell_excluded": closed,
        "Round215_cell_row_sha256": evidence["row_sha256"],
        "formal_credit": {
            "reduced_clipped_cell_disposition": 1,
            "whole_closed_cell_exclusion": int(closed),
            "whole_origin_exclusion": 0,
        },
        "strict_nonpromotion": {
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        },
    }
    return {**body, "row_sha256": digest(body)}


def prior_partition(replay: dict[str, Any], origin: str) -> dict[str, Any]:
    source = replay["origins"][origin]
    chart = source["chart_id"]
    evidence = sorted(
        replay["prior"][origin], key=lambda row: row["leaf_key"]
    )
    by_key = {row["leaf_key"]: row for row in evidence}
    require(
        len(by_key) == len(evidence)
        and all(row["disposition"].startswith("EXCLUDED") for row in evidence),
        "prior excluded:" + origin,
    )
    frontier_keys = {
        row.key for row in replay["frontier"] if row.origin_key == origin
    }
    closed: dict[str, Any] = {}
    split_faces: list[dict[str, Any]] = []
    pending = [(source["box"], 0)]
    while pending:
        box, depth = pending.pop()
        key = f"{chart}:{box.path}"
        if key in by_key:
            item = by_key[key]
            require(
                item["relative_depth"] == depth
                and item["coverage_numerator_64"] == 2 ** (6 - depth),
                "prior depth:" + key,
            )
            closed[key] = r176.Frontier(
                chart, box, (), origin, "PINNED_PRE_DEPTH14_CLOSED_BOX"
            )
            continue
        if depth == 6:
            require(key in frontier_keys, "frontier identity:" + key)
            continue
        lower, upper = r176.split(box)
        parent = r176.Frontier(
            chart, box, (), origin, "ROUND176_PARTITION_SPLIT"
        )
        split_faces.append(
            r180.split_face(parent, r180.split_axis(box), lower, upper)
        )
        pending.extend([(lower, depth + 1), (upper, depth + 1)])
    prior_volume = sum((r215.box_volume(row.box) for row in closed.values()), Q(0))
    parent_volume = r215.box_volume(source["box"])
    frontier_volume = sum(
        (
            r215.box_volume(row.box)
            for row in replay["frontier"] if row.origin_key == origin
        ),
        Q(0),
    )
    numerator = sum(row["coverage_numerator_64"] for row in evidence)
    require(
        set(closed) == set(by_key)
        and 0 <= numerator <= 64
        and prior_volume == parent_volume * Q(numerator, 64)
        and prior_volume + frontier_volume == parent_volume,
        "prior/frontier partition:" + origin,
    )
    evidence_rows = [
        {
            "upstream_evidence": row,
            "closed_box": r176.box_row(closed[row["leaf_key"]].box),
            "whole_closed_box_excluded": True,
        }
        for row in evidence
    ]
    return {
        "closed": closed,
        "evidence_sha256": digest(evidence_rows),
        "count": len(closed),
        "numerator": numerator,
        "volume": prior_volume,
        "split_faces": sorted(
            split_faces, key=lambda row: row["parent_cell_key"]
        ),
    }


def inherited_candidate_audit(
    candidate_keys: list[str],
) -> tuple[list[str], list[dict[str, Any]]]:
    replay = r176.replay_frontier()
    candidates = set(candidate_keys)
    roots: dict[str, list[Any]] = defaultdict(list)
    base_kinds: dict[str, Counter[str]] = defaultdict(Counter)
    for row in replay["frontier"]:
        if row.origin_key not in candidates:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key][kind] += 1
    promoted: list[str] = []
    held: list[dict[str, Any]] = []
    for candidate_ordinal, origin in enumerate(candidate_keys):
        refinement = r180.refine_origin(roots[origin], 4)
        nonexcluded = [
            row for row in refinement["terminal_rows"]
            if row["coarse_disposition"] != "EXCLUDED"
        ]
        require(
            set(base_kinds[origin]) <= {"EXCLUDED"},
            "candidate base disposition:" + origin,
        )
        if not nonexcluded:
            promoted.append(origin)
            continue
        census = Counter(
            row["coarse_disposition"] for row in refinement["terminal_rows"]
        )
        require(
            census == Counter({"EXCLUDED": 80, "MIXED": 4})
            and len(nonexcluded) == 4
            and all(
                row["method"] == "OUTGOING_H_CLOSED_RECTANGLE_TREE"
                and row["terminal_classes"]
                == {"TYPED_SEAM_GRAPH_AND_TWO_OPEN_SIDES": 1}
                for row in nonexcluded
            )
            and len(refinement["final_residual_rows"]) == 252,
            "candidate inherited H obstruction:" + origin,
        )
        body = {
            "schema": (
                "cm2.round306c30a.source-w-inherited-h-obstruction."
                "row.v1"
            ),
            "held_ordinal": len(held),
            "candidate_ordinal": candidate_ordinal,
            "origin_key": origin,
            "Round176_residual_root_count": len(roots[origin]),
            "Round176_preclosed_kind_census": dict(
                sorted(base_kinds[origin].items())
            ),
            "Round180_terminal_disposition_census": dict(
                sorted(census.items())
            ),
            "Round180_nonexcluded_terminal_count": len(nonexcluded),
            "Round180_nonexcluded_terminal_rows": nonexcluded,
            "Round180_nonexcluded_terminal_rows_sha256": digest(nonexcluded),
            "Round180_final_residual_count": len(
                refinement["final_residual_rows"]
            ),
            "obstruction": (
                "POSITIVE_MEASURE_PREFIX_STAGE_ONE_MATCH_SIDE_REMAINS_"
                "IN_TYPED_OUTGOING_H_PARTITION"
            ),
            "whole_original_physical_origin_excluded": False,
            "whole_origin_integer_credit": 0,
            "formal_credit": {"whole_source_W_origin_exclusion": 0},
            "strict_nonpromotion": {
                "child_or_volume_as_integer_credit": 0,
                "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
            },
        }
        held.append({**body, "row_sha256": digest(body)})
    require(
        len(promoted) == EXPECTED_PROMOTED_ORIGINS
        and len(held) == EXPECTED_HELD_ORIGINS
        and tuple(row["origin_key"] for row in held)
        == EXPECTED_HELD_ORIGIN_KEYS
        and digest([row["origin_key"] for row in held])
        == EXPECTED_HELD_ORIGIN_KEYS_SHA256,
        "candidate promotion/hold partition",
    )
    return promoted, held


def expected_origins(
    bounded: dict[str, Any],
    evidence_by_key: dict[str, dict[str, Any]],
    clipped_by_key: dict[str, dict[str, Any]],
    promoted_keys: list[str],
) -> Iterator[dict[str, Any]]:
    replay = r176.replay_frontier()
    promoted = set(promoted_keys)
    residual_roots: dict[str, list[Any]] = defaultdict(list)
    base_rows: dict[str, list[Any]] = defaultdict(list)
    base_kinds: dict[str, set[str]] = defaultdict(set)
    base_volume: dict[str, Q] = defaultdict(Q)
    for row in replay["frontier"]:
        if row.origin_key not in promoted:
            continue
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_roots[row.origin_key].append(row)
        else:
            base_rows[row.origin_key].append(row)
            base_kinds[row.origin_key].add(kind)
            base_volume[row.origin_key] += r215.box_volume(row.box)
    per_origin = {
        row["origin_key"]: row
        for row in bounded["whole_origin_outcome"]["per_origin_rows"]
    }
    for ordinal, origin in enumerate(promoted_keys):
        roots = residual_roots[origin]
        refinement = r180.refine_origin(roots, 4)
        final_rows = sorted(
            refinement["final_residual_rows"], key=lambda row: row.key
        )
        inherited = sorted(
            refinement["terminal_rows"], key=lambda row: row["cell_key"]
        )
        inherited_nonexcluded = [
            row for row in inherited if row["coarse_disposition"] != "EXCLUDED"
        ]
        root_volumes = {row.key: r215.box_volume(row.box) for row in roots}
        inherited_volume = sum(
            (
                root_volumes[row["root_depth14_cell_key"]]
                * Q(row["coverage_numerator"], row["coverage_denominator"])
                for row in inherited
            ),
            Q(0),
        )
        proof_source: dict[str, str] = {}
        rebuilt_keys: list[str] = []
        exact_count = 0
        exact_volume = Q(0)
        rebuilt_volume = Q(0)
        old_closed = 0
        new_closed = 0
        for row in final_rows:
            reduction = r215.exact_behind_reduce(
                row, r180.residual_category(row)
            )
            if reduction["closed"]:
                exact_count += 1
                exact_volume += r215.box_volume(row.box)
                proof_source[row.key] = (
                    "PINNED_ROUND201_EXACT_BEHIND_CLOSED_BOX"
                )
                continue
            rebuilt_keys.append(row.key)
            rebuilt_volume += r215.box_volume(row.box)
            evidence = evidence_by_key[row.key]
            if evidence["analytic_closed"]:
                old_closed += 1
                proof_source[row.key] = "PINNED_ROUND215_STRICT_CLOSED_BOX"
            else:
                require(
                    clipped_by_key[row.key]["whole_closed_cell_excluded"],
                    "promoted clipped cell:" + row.key,
                )
                new_closed += 1
                proof_source[row.key] = (
                    "ROUND306C30A_REDUCED_CLIPPED_DELTA_FULL_STRATUM_"
                    "EXCLUSION"
                )
        expected = per_origin[origin]
        require(
            rebuilt_keys == sorted(
                key for key, value in evidence_by_key.items()
                if value["origin_key"] == origin
            )
            and len(rebuilt_keys) == expected["Round201_residual_cell_count"]
            and old_closed == expected["Round215_analytic_closed_cell_count"]
            and new_closed == expected["Round215_blocker_count"][
                "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
            ],
            "promoted residual identity:" + origin,
        )
        prior = prior_partition(replay, origin)
        leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
        leaf_rows = {row.key: row for row in base_rows[origin]}
        leaf_rows.update(prior["closed"])
        leaf_rows.update(leaves["terminal"])
        leaf_rows.update(leaves["final"])
        owner_sources = {
            row.key: "PINNED_ROUND176_PRECLOSED_BOX"
            for row in base_rows[origin]
        }
        owner_sources.update({
            key: "PINNED_PRE_DEPTH14_CLOSED_BOX" for key in prior["closed"]
        })
        owner_sources.update({
            key: "PINNED_ROUND180_INHERITED_CLOSED_BOX"
            for key in leaves["terminal"]
        })
        owner_sources.update(proof_source)
        owner_audit = r215.strict_lower_strata_owner_audit(
            prior["split_faces"],
            refinement["split_face_rows"],
            replay["origins"][origin]["box"],
            leaf_rows,
            owner_sources,
        )
        input_root_volume = sum(root_volumes.values(), Q(0))
        final_volume = sum(
            (r215.box_volume(row.box) for row in final_rows), Q(0)
        )
        original_volume = r215.box_volume(replay["origins"][origin]["box"])
        checks = {
            "base": base_kinds[origin] <= {"EXCLUDED"},
            "inherited": not inherited_nonexcluded,
            "owners": owner_audit[
                "all_owner_rows_reduce_to_excluded_closed_3D_enclosures"
            ],
            "disjoint": owner_audit[
                "internal_and_outer_strata_classes_are_disjoint"
            ],
            "legacy": owner_audit[
                "trusted_legacy_ledger_conclusion_boolean"
            ] is False,
            "refinement_volume": inherited_volume + final_volume
            == input_root_volume,
            "final_volume": exact_volume + rebuilt_volume == final_volume,
            "parent_volume": prior["volume"] + base_volume[origin]
            + input_root_volume == original_volume,
        }
        require(all(checks.values()), "dimension-safe closure:" + origin)
        lower_ledger = r180.lower_strata_ledger(refinement["split_face_rows"])
        theorem = {
            "kind": (
                "SOURCE_W_REDUCED_CLIPPED_DELTA_WHOLE_ORIGIN_"
                "EXCLUSION_THEOREM"
            ),
            "Round176_prior_and_frontier_partition_exact": True,
            "Round176_preclosed_all_excluded": True,
            "Round180_inherited_terminals_all_excluded": True,
            "Round201_exact_behind_cells_all_excluded": True,
            "Round215_preclosed_residual_cells_all_excluded": True,
            "Round306C30A_reduced_clipped_cells_all_3D_2D_1D_0D_"
            "strata_excluded": True,
            "every_internal_and_outer_lower_stratum_has_one_excluded_"
            "half_open_owner": True,
            "whole_original_origin_excluded": True,
        }
        body = {
            "schema": (
                "cm2.round306c30a.source-w-reduced-clipped-delta."
                "whole-origin-row.v1"
            ),
            "promotion_ordinal": ordinal,
            "origin_key": origin,
            "priority_ordinal": expected["priority_ordinal"],
            "source_chart_id": replay["origins"][origin]["chart_id"],
            "original_parent_box": r176.box_row(
                replay["origins"][origin]["box"]
            ),
            "Round176_prior_closed_count": prior["count"],
            "Round176_prior_coverage_numerator_64": prior["numerator"],
            "Round176_preclosed_frontier_count": len(base_rows[origin]),
            "Round176_residual_root_count": len(roots),
            "Round180_inherited_terminal_count": len(inherited),
            "Round180_final_cell_count": len(final_rows),
            "Round201_exact_behind_closed_cell_count": exact_count,
            "Round201_residual_cell_count": len(rebuilt_keys),
            "Round215_preclosed_residual_cell_count": old_closed,
            "Round306C30A_new_closed_cell_count": new_closed,
            "Round306C30A_new_closed_cell_keys_sha256": digest([
                key for key in rebuilt_keys if key in clipped_by_key
            ]),
            "exact_volume_conservation": {
                "original_parent": str(original_volume),
                "Round176_prior": str(prior["volume"]),
                "Round176_preclosed_frontier": str(base_volume[origin]),
                "Round176_residual_roots": str(input_root_volume),
                "Round180_inherited": str(inherited_volume),
                "Round180_final": str(final_volume),
                "Round201_exact_behind": str(exact_volume),
                "Round201_residual": str(rebuilt_volume),
            },
            "lower_dimensional_strata": lower_ledger,
            "independent_lower_dimensional_owner_audit": owner_audit,
            "whole_origin_theorem": theorem,
            "whole_origin_theorem_sha256": digest(theorem),
            "whole_original_physical_origin_excluded": True,
            "whole_origin_integer_credit": 1,
            "formal_credit": {
                "whole_source_W_origin_exclusion": 1, "D02": 0,
            },
            "strict_nonpromotion": {
                "child_or_volume_as_integer_credit": 0,
                "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
            },
        }
        yield {**body, "row_sha256": digest(body)}


def candidate_rows(path: Path) -> Iterator[dict[str, Any]]:
    raw = regular_bytes(path, 512 * 1024 * 1024)
    require(
        raw[:2] == b"\x1f\x8b"
        and int.from_bytes(raw[4:8], "little") == 0,
        "deterministic gzip header:" + path.name,
    )
    with gzip.open(path, "rb") as handle:
        for ordinal, line in enumerate(handle):
            require(line.endswith(b"\n"), "ledger newline:" + path.name)
            row = strict_object_bytes(line[:-1], f"{path.name}:{ordinal}")
            require(
                wire(row) + b"\n" == line,
                "canonical ledger row:" + path.name + ":" + str(ordinal),
            )
            claimed = row.get("row_sha256")
            body = dict(row)
            body.pop("row_sha256", None)
            require(
                type(claimed) is str and claimed == digest(body),
                "ledger row closure:" + path.name + ":" + str(ordinal),
            )
            yield row


def descriptor(
    path: Path, count: int, sequence: str, order: str
) -> dict[str, Any]:
    return {
        "filename": path.name,
        "row_count": count,
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence,
        "order": order,
    }


def preflight(candidate: Path, pins: list[dict[str, str]]) -> None:
    raw = regular_bytes(candidate / RESULT)
    result = strict_object_bytes(raw, RESULT)
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    require(
        raw == wire(result)
        and type(claimed) is str
        and claimed == digest(body),
        "preflight result closure",
    )
    require(
        result["schema"]
        == (
            "cm2.round306c30a.source-w-162-reduced-clipped-delta-"
            "whole-origin-promotion.v1"
        )
        and result["status"]
        == (
            "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
            "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
            "160_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
            "2_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
        )
        and result["cell_census"]["input"] == EXPECTED_CLIPPED_CELLS
        and result["cell_census"]["excluded"] == EXPECTED_CLIPPED_CLOSED
        and result["cell_census"]["residual"] == EXPECTED_CLIPPED_RESIDUAL
        and result["whole_origin_census"]["Round306C30A_new_promoted"]
        == EXPECTED_PROMOTED_ORIGINS
        and result["whole_origin_census"][
            "Round306C30A_candidate_origins_audited"
        ] == EXPECTED_CANDIDATE_ORIGINS
        and result["whole_origin_census"]["Round306C30A_inherited_H_held"]
        == EXPECTED_HELD_ORIGINS
        and result["whole_origin_census"][
            "still_open_active_strict_interior_origins"
        ] == 36
        and result["source_W_ledger_transition"]["before"] == {
            "excluded": R215_EXCLUDED,
            "conservative_live": R215_CONSERVATIVE_LIVE,
            "total": 76_832,
            "remaining": R215_REMAINING,
        }
        and result["source_W_ledger_transition"]["after"]["excluded"]
        == NEW_EXCLUDED
        and result["source_W_ledger_transition"]["after"][
            "conservative_live"
        ] == NEW_CONSERVATIVE_LIVE
        and result["source_W_ledger_transition"]["after"]["remaining"]
        == NEW_REMAINING
        and result["source_W_ledger_transition"][
            "new_whole_origin_exclusion_credit"
        ] == EXPECTED_PROMOTED_ORIGINS
        and result["formal_credit"] == {
            "reduced_clipped_cell_dispositions": EXPECTED_CLIPPED_CELLS,
            "reduced_clipped_whole_cell_exclusions": EXPECTED_CLIPPED_CLOSED,
            "whole_source_W_origin_exclusions": EXPECTED_PROMOTED_ORIGINS,
        }
        and result["strict_nonpromotion"] == {
            "D02": "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        and result["input_pins"] == pins
        and result["whole_origin_promotion_theorem"][
            "child_cell_or_volume_credit_used"
        ] is False
        and result["whole_origin_promotion_theorem_sha256"]
        == digest(result["whole_origin_promotion_theorem"])
        and result["ledgers"]["reduced_clipped_cell"]["row_count"]
        == EXPECTED_CLIPPED_CELLS
        and result["ledgers"]["whole_origin_promotion"]["row_count"]
        == EXPECTED_PROMOTED_ORIGINS
        and result["ledgers"]["inherited_H_obstruction_hold"]["row_count"]
        == EXPECTED_HELD_ORIGINS,
        "static theorem/result boundary",
    )


def verify(candidate: Path) -> dict[str, Any]:
    validate_runtime()
    pins = validate_sources()
    require(
        candidate.is_dir()
        and candidate.resolve() != ROOT.resolve(),
        "candidate directory boundary",
    )
    preflight(candidate, pins)
    ctx.prec = 192
    bounded, evidence_rows = capture_round215()
    evidence_by_key = {row["cell_key"]: row for row in evidence_rows}
    require(
        len(evidence_by_key) == EXPECTED_ACTIVE_CELLS,
        "unique Round215 cell keys",
    )
    clipped_evidence = sorted(
        (
            row for row in evidence_rows
            if row["blocker"] == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
        ),
        key=lambda row: row["cell_key"],
    )
    expected_cells = [
        expected_cell(ordinal, row)
        for ordinal, row in enumerate(clipped_evidence)
    ]
    clipped_by_key = {row["cell_key"]: row for row in expected_cells}
    disposition_census = Counter(row["disposition"] for row in expected_cells)
    target_census = Counter(row["candidate_target"] for row in expected_cells)
    closed_census = Counter(
        "CLOSED" if row["whole_closed_cell_excluded"] else "RESIDUAL"
        for row in expected_cells
    )
    require(
        len(clipped_by_key) == EXPECTED_CLIPPED_CELLS
        and closed_census == Counter({
            "CLOSED": EXPECTED_CLIPPED_CLOSED,
            "RESIDUAL": EXPECTED_CLIPPED_RESIDUAL,
        })
        and disposition_census == Counter({
            "CLOSED_REDUCED_CANDIDATE_OWNER_MISMATCH": 9_900,
            "CLOSED_REDUCED_FROZEN_OWNER_OUTGOING_MISMATCH": 2_968,
            "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED": 20,
        })
        and target_census == Counter({
            "G[0,0]": 1_620,
            "G[0,1]": 1_620,
            "G[1,0]": 3_340,
            "G[1,1]": 3_340,
            "W[1,0]": 2_968,
        }),
        "independent reduced clipped census",
    )
    per_origin = bounded["whole_origin_outcome"]["per_origin_rows"]
    candidate_keys = sorted(
        row["origin_key"]
        for row in per_origin
        if set(row["Round215_blocker_count"])
        == {"SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"}
        and all(
            clipped_by_key[key]["whole_closed_cell_excluded"]
            for key, value in evidence_by_key.items()
            if value["origin_key"] == row["origin_key"]
            and value["blocker"]
            == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
        )
    )
    require(
        len(candidate_keys) == EXPECTED_CANDIDATE_ORIGINS,
        "independent candidate cohort",
    )
    promoted_keys, expected_held_rows = inherited_candidate_audit(
        candidate_keys
    )
    promoted_rows = [
        row for row in per_origin if row["origin_key"] in set(promoted_keys)
    ]
    require(
        sum(
            row["Round201_residual_cell_count"] for row in promoted_rows
        ) == EXPECTED_PROMOTED_RESIDUAL_CELLS
        and sum(
            row["Round215_analytic_closed_cell_count"] for row in promoted_rows
        ) == EXPECTED_PROMOTED_OLD_CLOSED_CELLS
        and sum(
            row["Round215_blocker_count"][
                "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
            ]
            for row in promoted_rows
        ) == EXPECTED_PROMOTED_NEW_CELLS,
        "independent whole-origin selection and conservation",
    )

    cell_path = candidate / CELL_LEDGER
    candidate_cell_iterator = candidate_rows(cell_path)
    cell_sequence = hashlib.sha256()
    for ordinal, expected in enumerate(expected_cells):
        actual = next(candidate_cell_iterator, None)
        require(
            actual == expected,
            "cell reconstruction:" + str(ordinal),
        )
        cell_sequence.update(bytes.fromhex(expected["row_sha256"]))
    require(next(candidate_cell_iterator, None) is None, "cell exhaustion")

    origin_path = candidate / ORIGIN_LEDGER
    candidate_origin_iterator = candidate_rows(origin_path)
    origin_sequence = hashlib.sha256()
    origin_count = 0
    for ordinal, expected in enumerate(expected_origins(
        bounded, evidence_by_key, clipped_by_key, promoted_keys
    )):
        actual = next(candidate_origin_iterator, None)
        require(
            actual == expected,
            "whole-origin reconstruction:" + str(ordinal),
        )
        origin_sequence.update(bytes.fromhex(expected["row_sha256"]))
        origin_count += 1
    require(
        next(candidate_origin_iterator, None) is None
        and origin_count == EXPECTED_PROMOTED_ORIGINS,
        "whole-origin exhaustion",
    )
    held_path = candidate / HELD_LEDGER
    candidate_held_iterator = candidate_rows(held_path)
    held_sequence = hashlib.sha256()
    for ordinal, expected in enumerate(expected_held_rows):
        actual = next(candidate_held_iterator, None)
        require(actual == expected, "held-origin reconstruction:" + str(ordinal))
        held_sequence.update(bytes.fromhex(expected["row_sha256"]))
    require(next(candidate_held_iterator, None) is None, "held-origin exhaustion")
    cell_descriptor = descriptor(
        cell_path,
        EXPECTED_CLIPPED_CELLS,
        cell_sequence.hexdigest(),
        "LEXICOGRAPHIC_ROUND215_CELL_KEY",
    )
    origin_descriptor = descriptor(
        origin_path,
        origin_count,
        origin_sequence.hexdigest(),
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    held_descriptor = descriptor(
        held_path,
        EXPECTED_HELD_ORIGINS,
        held_sequence.hexdigest(),
        "LEXICOGRAPHIC_HELD_SOURCE_W_ORIGIN_KEY",
    )
    theorem = {
        "kind": (
            "SOURCE_W_162_CANDIDATE_REDUCED_CLIPPED_DELTA_"
            "160_WHOLE_ORIGIN_PROMOTION_AND_2_INHERITED_H_HOLD_THEOREM"
        ),
        "selection_is_outcome_blind_until_complete_198_origin_replay": True,
        "Round215_18432_cell_replay_exact": True,
        "Round184_dimension_safe_clipped_partition_reapplied_after_"
        "Round201_exact_behind_reduction": True,
        "reduced_clipped_cells_disposed": EXPECTED_CLIPPED_CELLS,
        "reduced_clipped_cells_excluded": EXPECTED_CLIPPED_CLOSED,
        "residual_cells_reserved_for_full_Delta_lane": EXPECTED_CLIPPED_RESIDUAL,
        "candidate_whole_origins_audited": EXPECTED_CANDIDATE_ORIGINS,
        "whole_origins_with_complete_3D_2D_1D_0D_exclusion":
            EXPECTED_PROMOTED_ORIGINS,
        "whole_origins_held_by_inherited_positive_measure_H_side":
            EXPECTED_HELD_ORIGINS,
        "every_promoted_origin_has_independent_half_open_lower_owner_audit":
            True,
        "child_cell_or_volume_credit_used": False,
    }
    remaining_partition = {
        "mixed_active_nonseam": 36,
        "mixed_retained_source_seams": 2,
        "compact_q": 54,
        "total": NEW_REMAINING,
    }
    body = {
        "schema": (
            "cm2.round306c30a.source-w-162-reduced-clipped-delta-"
            "whole-origin-promotion.v1"
        ),
        "status": (
            "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
            "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
            "160_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
            "2_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
        ),
        "cell_census": {
            "input": EXPECTED_CLIPPED_CELLS,
            "excluded": EXPECTED_CLIPPED_CLOSED,
            "residual": EXPECTED_CLIPPED_RESIDUAL,
            "by_disposition": dict(sorted(disposition_census.items())),
            "by_target": dict(sorted(target_census.items())),
        },
        "whole_origin_census": {
            "Round215_active_strict_interior_origins": 198,
            "Round215_prior_promoted": R215_PROMOTED,
            "Round306C30A_candidate_origins_audited":
                EXPECTED_CANDIDATE_ORIGINS,
            "Round306C30A_new_promoted": EXPECTED_PROMOTED_ORIGINS,
            "Round306C30A_promoted_origin_keys_sha256": digest(promoted_keys),
            "Round306C30A_inherited_H_held": EXPECTED_HELD_ORIGINS,
            "Round306C30A_inherited_H_held_origin_keys_sha256":
                EXPECTED_HELD_ORIGIN_KEYS_SHA256,
            "still_open_active_strict_interior_origins": 36,
            "retained_source_seam_origins_outside_active_cohort": 2,
            "compact_q_origins": 54,
        },
        "source_W_ledger_transition": {
            "before": {
                "excluded": R215_EXCLUDED,
                "conservative_live": R215_CONSERVATIVE_LIVE,
                "total": 76_832,
                "remaining": R215_REMAINING,
            },
            "new_whole_origin_exclusion_credit": EXPECTED_PROMOTED_ORIGINS,
            "after": {
                "excluded": NEW_EXCLUDED,
                "conservative_live": NEW_CONSERVATIVE_LIVE,
                "total": 76_832,
                "remaining": NEW_REMAINING,
                "remaining_partition": remaining_partition,
            },
            "conservation_identity": "74744+2088=76832",
        },
        "whole_origin_promotion_theorem": theorem,
        "whole_origin_promotion_theorem_sha256": digest(theorem),
        "ledgers": {
            "reduced_clipped_cell": cell_descriptor,
            "whole_origin_promotion": origin_descriptor,
            "inherited_H_obstruction_hold": held_descriptor,
        },
        "input_pins": pins,
        "formal_credit": {
            "reduced_clipped_cell_dispositions": EXPECTED_CLIPPED_CELLS,
            "reduced_clipped_whole_cell_exclusions": EXPECTED_CLIPPED_CLOSED,
            "whole_source_W_origin_exclusions": EXPECTED_PROMOTED_ORIGINS,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "CLOSE_12_OUTGOING_H_ORIGINS_THEN_2_FULL_DELTA_ORIGINS_"
            "THEN_20_MULTI_DELTA_ORIGINS_THEN_2_REDUCED_LIVE_ORIGINS_"
            "THEN_2_RETAINED_SEAMS_AND_54_COMPACT_Q_ORIGINS"
        ),
    }
    expected_result = {**body, "result_sha256": digest(body)}
    result_path = candidate / RESULT
    raw_result = regular_bytes(result_path)
    actual_result = strict_object_bytes(raw_result, RESULT)
    require(
        raw_result == wire(actual_result)
        and actual_result == expected_result,
        "complete result reconstruction",
    )
    return {
        "status": (
            "PASS_INDEPENDENT_C30A_12888_CELL_ROWS__160_WHOLE_ORIGIN_"
            "ROWS__2_INHERITED_H_HOLDS_RECONSTRUCTED__"
            "252_TO_92_TRANSITION_VERIFIED__"
            "D02_BOUNDARY_PRESERVED"
        ),
        "cell_rows": EXPECTED_CLIPPED_CELLS,
        "whole_origin_rows": EXPECTED_PROMOTED_ORIGINS,
        "held_origin_rows": EXPECTED_HELD_ORIGINS,
        "total_rows": (
            EXPECTED_CLIPPED_CELLS
            + EXPECTED_PROMOTED_ORIGINS
            + EXPECTED_HELD_ORIGINS
        ),
        "result_sha256": expected_result["result_sha256"],
        "promoted_origin_keys_sha256": digest(promoted_keys),
        "runtime": {
            "python": ".".join(str(value) for value in sys.version_info[:3]),
            "python_flint": flint.__version__,
            "flint": flint.__FLINT_VERSION__,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    arguments = parser.parse_args()
    print(wire(verify(Path(arguments.candidate_dir).resolve())).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
