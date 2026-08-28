#!/usr/bin/env python3
"""Read-only, zero-promotion probe for the Round184 source-W strict-first tail.

The probe treats the frozen Round184 producer as inert bytes, reads its pinned
certificate only to identify the exact 162-origin diagnostic cohort, and then
rebuilds every relevant Round184 residual child from the pinned independent
Round180/Round176 geometry.  Only cells whose Round184-equivalent clipped-
Delta proof fails at TARGET_NOT_STRICT_POSITIVE_FIRST are refined further.

This is deliberately not a certificate producer.  It has no output-path
option, performs no filesystem writes, emits progress only on stderr, and
prints one final JSON document on stdout.  All counts remain probe-only and
must not be copied into an official ledger without a separate producer and
independent verifier.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

# Prevent local dependency imports from creating or refreshing __pycache__.
sys.dont_write_bytecode = True

from flint import arb, ctx

import cm2_round180_full_multi_residual_dimension_safe_partial_verifier as r180


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round187.source-w-strict-first-refinement-probe.v1"
MAX_INPUT_BYTES = 8 * 1024 * 1024

ROUND180_PINS = {
    "cm2_round180_full_multi_residual_dimension_safe_partial.py":
        "0ddb815a036a6e351929c484a00a565ce8969286bb137977ee9470577d807955",
    "cm2_round180_full_multi_residual_dimension_safe_partial_certificate.json":
        "46c6f1b2e86f9aa70d9126b28febbf97a81d6a4ac8f610dc2bb82d032a1abb70",
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py":
        "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4",
    "cm2_round180_full_multi_residual_dimension_safe_partial_verification.json":
        "fb1b71c3006fcf4a10ee79d324346e2065ff2002252b28a29bd5085cab7e4caf",
    "cm2_round180_full_multi_residual_dimension_safe_partial_report.md":
        "aae414b750578f7f2c1203e51c59c57a5cf5c5d1aefa5c2cbdb63bcd256233dd",
    "cm2_round180_full_multi_residual_dimension_safe_partial_cold_replay.md":
        "b6dd550c663157d122c6e63e8c2a2974f420144d57814a874db664331b8f740a",
    "cm2_round180_full_multi_residual_dimension_safe_partial_manifest.sha256":
        "19c292b1d2e82388af891340676ccf0eb6f02f0301fe381f9102a52df0fd1aa4",
}
ROUND180_RESULT = (
    "b2d30aade1e60c3b8d1e5943a240bafc8c8a28e35e67c882026b94246dafae3b"
)
ROUND180_VERIFICATION_RESULT = (
    "87b908b0549af255dd20fef31e3b6fbf6205860641d4ebbcf332f30271c9b1ce"
)
ROUND184_PRODUCER = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py"
)
ROUND184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_certificate.json"
)
ROUND184_PRODUCER_SHA256 = (
    "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906"
)
ROUND184_CERTIFICATE_SHA256 = (
    "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f"
)
ROUND184_RESULT = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
ROUND184_SCHEMA = (
    "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta.v1"
)

CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
TARGET_FAILURE = "TARGET_NOT_STRICT_POSITIVE_FIRST"
SOURCE_SEAM = "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
SOURCE_INTERIOR = "STRICT_PHYSICAL_CHART_INTERIOR"
SOURCE_SEAM_FAILURE = (
    "PHYSICAL_SEAM_COMPOSITE_REQUIRES_SEPARATE_HALF_OPEN_PARTITION"
)

EXPECTED_TARGET_ORIGIN_COUNT = 162
EXPECTED_TARGET_ORIGIN_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_TARGET_RESIDUAL_CHILD_COUNT = 18084
EXPECTED_TARGET_FAILURE_CELL_COUNT = 16492
EXPECTED_TARGET_BASELINE_CLOSED_CELL_COUNT = 1592
EXPECTED_ALL_SOURCE_SEAM_COUNT = 18
EXPECTED_ALL_SOURCE_SEAM_KEYS_SHA256 = (
    "6fed61e3a02850e2a0cec911c35e6c71f2accb42eea1f62aa3a7acd6968a58b4"
)
EXPECTED_TARGET_SOURCE_SEAM_COUNT = 6
EXPECTED_TARGET_SOURCE_SEAM_KEYS_SHA256 = (
    "d21a934ed6d43ba876ab514cd710b0f659f3e94e543b3c4e11ea6d719fe0d208"
)
EXPECTED_PURE_KEYS_SHA256 = (
    "fcfe248134dd13811e6d8aa58e9fb1506c7a29dc45b11a08364a750d5748d4ef"
)
EXPECTED_PRIORITY_ROWS_SHA256 = (
    "d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e"
)
EXPECTED_TRANCHE_ROWS_SHA256 = (
    "76519d1d5e3c892a2b7a2d0fb3686d1633a0c01f0d4f4ea18f15d87e178cda7d"
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[Any, Q]) -> dict[str, str]:
    return {
        str(key): str(item) for key, item in sorted(value.items())
    }


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def read_regular(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(stat.S_ISREG(status.st_mode), f"input regular:{absolute.name}")
    require(not absolute.is_symlink(), f"input symlink:{absolute.name}")
    require(status.st_nlink == 1, f"input hardlink:{absolute.name}")
    require(
        0 < status.st_size <= MAX_INPUT_BYTES,
        f"input size:{absolute.name}",
    )
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute, flags)
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino),
            f"input race:{absolute.name}",
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"opened input type:{absolute.name}",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(chunk), f"short input:{absolute.name}")
            chunks.append(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    require(len(raw) == status.st_size, f"input byte count:{absolute.name}")
    return raw


def reject_surrogates(value: Any, label: str) -> None:
    if isinstance(value, str):
        require(
            not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
            f"surrogate:{label}",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item, label)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key, label)
            reject_surrogates(item, label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = read_regular(path)
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{path.name}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    require(type(value) is dict, f"top object:{path.name}")
    reject_surrogates(value, path.name)
    return value


def check_inputs() -> dict[str, Any]:
    expected_module = (
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py"
    )
    require(
        Path(r180.__file__).resolve() == expected_module.resolve(),
        "Round180 verifier module identity",
    )
    for name, expected in ROUND180_PINS.items():
        require(
            hashlib.sha256(read_regular(HERE / name)).hexdigest() == expected,
            f"Round180 pin:{name}",
        )

    round180_certificate = strict_load(
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial"
          "_certificate.json"
    )
    round180_verification = strict_load(
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial"
          "_verification.json"
    )
    require(
        round180_certificate["result_sha256"] == ROUND180_RESULT
        and digest(round180_certificate["result"]) == ROUND180_RESULT
        and round180_certificate["result"]["strict_nonpromotion"]["D02"]
        == "BLOCKED",
        "Round180 certificate result",
    )
    require(
        round180_verification["result_sha256"]
        == ROUND180_VERIFICATION_RESULT
        and digest(round180_verification["result"])
        == ROUND180_VERIFICATION_RESULT
        and round180_verification["result"]["status"]
        == "PASS_PARTIAL_BOUNDED_ROUND180",
        "Round180 verification result",
    )

    manifest_name = (
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_manifest.sha256"
    )
    manifest_entries: dict[str, str] = {}
    for line in read_regular(HERE / manifest_name).decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest_entries, f"manifest duplicate:{name}")
        manifest_entries[name] = value
        require(
            hashlib.sha256(read_regular(HERE / name)).hexdigest() == value,
            f"manifest entry:{name}",
        )
    require(
        manifest_entries
        == {
            name: expected
            for name, expected in ROUND180_PINS.items()
            if name != manifest_name
        },
        "Round180 manifest exact entries",
    )
    r180.check_chain()

    require(
        hashlib.sha256(read_regular(HERE / ROUND184_PRODUCER)).hexdigest()
        == ROUND184_PRODUCER_SHA256,
        "Round184 inert producer pin",
    )
    require(
        hashlib.sha256(read_regular(HERE / ROUND184_CERTIFICATE)).hexdigest()
        == ROUND184_CERTIFICATE_SHA256,
        "Round184 certificate pin",
    )
    envelope = strict_load(HERE / ROUND184_CERTIFICATE)
    require(envelope["schema"] == ROUND184_SCHEMA, "Round184 schema")
    require(
        envelope["result_sha256"] == ROUND184_RESULT
        and digest(envelope["result"]) == ROUND184_RESULT,
        "Round184 result",
    )
    result = envelope["result"]
    require(
        result["status"]
        == (
            "PARTIAL__DETERMINISTIC_1444_PRIORITY_REGISTRY_AND_"
            "PURE_SINGLE_CLIPPED_DELTA_TRANCHE__D02_STILL_BLOCKED"
        )
        and result["scope"]["source_obstacle"] == "W"
        and result["scope"]["frozen_owner"] == r180.r176.FROZEN_OWNER
        and result["scope"]["frozen_outgoing_chart"]
        == r180.r176.FROZEN_CHART
        and result["strict_nonpromotion"]["D02"] == "BLOCKED",
        "Round184 scope and nonpromotion",
    )

    registry = result["priority_registry"]
    tranche = result["pure_single_clipped_Delta_tranche"]
    require(
        registry["row_count"] == 1444
        and registry["rows_sha256"] == EXPECTED_PRIORITY_ROWS_SHA256
        and digest(registry["rows"]) == EXPECTED_PRIORITY_ROWS_SHA256
        and tranche["selected_origin_count"] == 794
        and tranche["closed_origin_count"] == 620
        and tranche["selected_exact_origin_keys_sha256"]
        == EXPECTED_PURE_KEYS_SHA256
        and digest(tranche["selected_exact_origin_keys"])
        == EXPECTED_PURE_KEYS_SHA256
        and tranche["per_origin_rows_sha256"]
        == EXPECTED_TRANCHE_ROWS_SHA256
        and digest(tranche["per_origin_rows"])
        == EXPECTED_TRANCHE_ROWS_SHA256
        and tranche["failure_count_by_reason"]
        == {
            SOURCE_SEAM_FAILURE: EXPECTED_ALL_SOURCE_SEAM_COUNT,
            TARGET_FAILURE: EXPECTED_TARGET_FAILURE_CELL_COUNT,
        }
        and tranche["source_chart_domain_count"]
        == {
            SOURCE_SEAM: EXPECTED_ALL_SOURCE_SEAM_COUNT,
            SOURCE_INTERIOR: 776,
        },
        "Round184 exact tranche census",
    )

    priority_by_origin = {
        row["origin_key"]: row for row in registry["rows"]
    }
    tranche_by_origin = {
        row["origin_key"]: row for row in tranche["per_origin_rows"]
    }
    require(
        len(priority_by_origin) == 1444
        and len(tranche_by_origin) == 794
        and set(tranche_by_origin)
        == set(tranche["selected_exact_origin_keys"]),
        "Round184 unique registry rows",
    )
    target_keys = sorted(
        origin
        for origin, row in tranche_by_origin.items()
        if row["failure_count_by_reason"].get(TARGET_FAILURE, 0) > 0
    )
    source_seam_keys = sorted(
        origin
        for origin, row in tranche_by_origin.items()
        if row["source_chart_domain"]["classification"] == SOURCE_SEAM
    )
    target_source_seam_keys = sorted(
        set(target_keys) & set(source_seam_keys)
    )
    require(
        len(target_keys) == EXPECTED_TARGET_ORIGIN_COUNT
        and digest(target_keys) == EXPECTED_TARGET_ORIGIN_KEYS_SHA256
        and len(source_seam_keys) == EXPECTED_ALL_SOURCE_SEAM_COUNT
        and digest(source_seam_keys)
        == EXPECTED_ALL_SOURCE_SEAM_KEYS_SHA256
        and len(target_source_seam_keys)
        == EXPECTED_TARGET_SOURCE_SEAM_COUNT
        and digest(target_source_seam_keys)
        == EXPECTED_TARGET_SOURCE_SEAM_KEYS_SHA256,
        "Round184 target and source-seam cohorts",
    )
    return {
        "result": result,
        "priority_by_origin": priority_by_origin,
        "tranche_by_origin": tranche_by_origin,
        "target_keys": target_keys,
        "source_seam_keys": source_seam_keys,
        "target_source_seam_keys": target_source_seam_keys,
        "pins": {
            "Round180_result_sha256": ROUND180_RESULT,
            "Round180_verification_result_sha256":
                ROUND180_VERIFICATION_RESULT,
            "Round184_producer_sha256": ROUND184_PRODUCER_SHA256,
            "Round184_certificate_sha256": ROUND184_CERTIFICATE_SHA256,
            "Round184_result_sha256": ROUND184_RESULT,
        },
    }


def box_volume(box: r180.r176.Box) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def arb_sign_name(value: arb) -> str:
    sign = r180.r176.sign(value)
    return (
        "STRICT_POSITIVE"
        if sign > 0
        else "STRICT_NEGATIVE" if sign < 0 else "OVERWRAP"
    )


def strict_chart(nx: arb, ny: arb) -> str | None:
    tests = {
        "E": (nx - ny, nx + ny),
        "W": (-nx - ny, -nx + ny),
        "N": (ny - nx, ny + nx),
        "S": (-ny - nx, -ny + nx),
    }
    cells = [
        cell
        for cell, margins in tests.items()
        if bool(margins[0] > 0) and bool(margins[1] > 0)
    ]
    return cells[0] if len(cells) == 1 else None


def tangent_chart(
    row: r180.r176.Frontier,
    candidate: r180.r176.Root,
) -> str | None:
    _qx, _qy, ux, uy, _s, _rp = r180.r176.geometry(
        row.chart_id, row.box
    )
    radius = r180.r176.base.arbq(
        r180.r176.base.RADIUS[
            r180.r176.TARGETS[candidate.target_id].obstacle
        ]
    )
    nx = candidate.transverse * uy / radius
    ny = -candidate.transverse * ux / radius
    return strict_chart(nx, ny)


def clipped_partition_proof(
    row: r180.r176.Frontier,
) -> tuple[dict[str, Any] | None, str]:
    """Reproduce the Round184 clipped-Delta three-stratum decision exactly."""
    records = r180.r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record
        for record in records
        if record.classification == "unresolved_discriminant"
    ]
    if len(unresolved) != 1:
        return None, f"UNRESOLVED_TARGET_COUNT_{len(unresolved)}"
    candidate = unresolved[0]
    derivative, lower, upper, full = r180.r176.graph_faces(
        row, candidate
    )
    if derivative == 0:
        return None, "P_DERIVATIVE_OVERWRAP"
    if full:
        return None, "NOT_CLIPPED_FULL_P_GRAPH"
    if not r180.r176.target_positive_first(candidate, records):
        return None, TARGET_FAILURE
    negative = r180.r176.remove_disposition(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        return None, "DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"

    graph_owner = candidate.target_id
    positive_chart: str | None = None
    graph_chart: str | None = None
    if candidate.target_id != r180.r176.FROZEN_OWNER:
        positive = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        graph = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        owner_reason = "candidate target differs from frozen owner"
    else:
        positive_chart = r180.r176.positive_chart(row, candidate)
        if positive_chart is None:
            return None, "DELTA_POSITIVE_OUTGOING_CHART_OVERWRAP"
        if positive_chart == r180.r176.FROZEN_CHART:
            return None, "DELTA_POSITIVE_OUTGOING_CHART_MATCH"
        graph_chart = tangent_chart(row, candidate)
        if graph_chart is None:
            return None, "DELTA_ZERO_GRAPH_OUTGOING_CHART_OVERWRAP"
        if graph_chart == r180.r176.FROZEN_CHART:
            return None, "DELTA_ZERO_GRAPH_OUTGOING_CHART_MATCH"
        positive = "EXCLUDED_OUTGOING_CHART_MISMATCH"
        graph = "EXCLUDED_OUTGOING_CHART_MISMATCH"
        owner_reason = (
            "frozen owner, independently recomputed chart mismatch"
        )

    proof = {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "target": candidate.target_id,
        "active_target_count": len(records),
        "strict_p_derivative_sign":
            "POSITIVE" if derivative > 0 else "NEGATIVE",
        "p_lower_face_sign": arb_sign_name(lower),
        "p_upper_face_sign": arb_sign_name(upper),
        "full_p_graph": False,
        "graph_existence_claim": "OUTER_ONLY__NONEMPTY_NOT_REQUIRED",
        "target_strict_positive_first_on_closed_outer": True,
        "Delta_negative_open_3D_disposition": negative,
        "Delta_zero_2D_graph_disposition": graph,
        "Delta_positive_open_3D_disposition": positive,
        "graph_owner_target": graph_owner,
        "frozen_owner": r180.r176.FROZEN_OWNER,
        "owner_recomputation": owner_reason,
        "Delta_zero_graph_outgoing_chart": (
            graph_chart if graph_chart is not None else "NOT_APPLICABLE"
        ),
        "Delta_positive_outgoing_chart": (
            positive_chart
            if positive_chart is not None
            else "NOT_APPLICABLE"
        ),
        "frozen_outgoing_chart": r180.r176.FROZEN_CHART,
        "all_three_strata_excluded": True,
        "ambient_and_stratum_dimensions": {
            "Delta_negative_open": 3,
            "Delta_zero_graph_outer": 2,
            "Delta_positive_open": 3,
            "graph_face_intersection_outer": 1,
            "graph_edge_or_corner_intersection_outer": 0,
        },
        "lower_dimensional_outer_nonemptiness_not_inferred": True,
        "whole_closed_cell_excluded": True,
    }
    proof["proof_sha256"] = digest(proof)
    return proof, "CLOSED"


def direct_strict_terminal(
    row: r180.r176.Frontier,
) -> tuple[str | None, dict[str, Any] | None]:
    """Reproduce the direct strict first branch of pinned Round180 close_node."""
    leaf, _records = r180.r176.classify(
        row.chart_id, row.box, row.active_targets
    )
    disposition, _margins = r180.r176.terminal_disposition(
        row.chart_id, leaf
    )
    if disposition is None:
        return None, None
    coarse = r180.r176.coarse(disposition)
    require(coarse in {"EXCLUDED", "LIVE"}, f"direct coarse:{row.key}")
    return coarse, {
        "method": "DIRECT_STRICT_CLOSED_BOX",
        "disposition": disposition,
        "coarse_disposition": coarse,
        "ambient_dimension": 3,
        "whole_closed_child": True,
        "all_owned_boundary_strata_inherit_strict_proof": True,
    }


def rebuild_round184_target_children(
    inputs: dict[str, Any],
) -> dict[str, Any]:
    target_keys = inputs["target_keys"]
    target_set = set(target_keys)
    priority_by_origin = inputs["priority_by_origin"]
    tranche_by_origin = inputs["tranche_by_origin"]

    progress("replay Round180 frontier from pinned geometry")
    replay = r180.r176.replay_frontier()
    require(
        target_set <= set(replay["origins"]),
        "target origins present in Round180 replay",
    )
    base_kinds: dict[str, set[str]] = {
        origin: set(replay["origin_kinds"].get(origin, ()))
        for origin in target_keys
    }
    residual_roots: dict[str, list[r180.r176.Frontier]] = defaultdict(list)
    for row in replay["frontier"]:
        if row.origin_key not in target_set:
            continue
        kind, _evidence = r180.r176.closure(row)
        if kind is None:
            residual_roots[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key].add(kind)
    require(
        set(residual_roots) == target_set
        and all(base_kinds[origin] <= {"EXCLUDED"} for origin in target_keys),
        "target origins are Round180 upper candidates",
    )
    for rows in residual_roots.values():
        rows.sort(key=lambda row: row.key)

    failed_by_origin: dict[str, list[r180.r176.Frontier]] = {}
    source_by_origin: dict[str, dict[str, Any]] = {}
    baseline_closed_count = 0
    baseline_closed_volume = Q(0)
    target_failure_count = 0
    target_failure_volume = Q(0)
    residual_child_count = 0
    residual_child_volume = Q(0)

    for index, origin in enumerate(target_keys, 1):
        refinement = r180.refine_origin(residual_roots[origin], 4)
        final_rows = refinement["final_residual_rows"]
        require(bool(final_rows), f"Round184 residual support:{origin}")
        categories = Counter(
            r180.residual_category(row) for row in final_rows
        )
        require(
            set(categories) == {CLIPPED},
            f"pure clipped support:{origin}",
        )
        priority = priority_by_origin[origin]
        tranche = tranche_by_origin[origin]
        require(
            priority["priority_class"] == "PURE_SINGLE_CLIPPED_DELTA"
            and priority["Round180_residual_child_count"] == len(final_rows)
            and priority["Round180_residual_child_keys_sha256"]
            == digest(sorted(row.key for row in final_rows)),
            f"Round184 priority row:{origin}",
        )
        volume = sum((box_volume(row.box) for row in final_rows), Q(0))
        require(
            priority["Round180_residual_child_volume"] == str(volume),
            f"Round184 residual volume:{origin}",
        )

        proofs: list[dict[str, Any]] = []
        failures: Counter[str] = Counter()
        failed_rows: list[r180.r176.Frontier] = []
        closed_volume = Q(0)
        failed_volume = Q(0)
        for row in final_rows:
            proof, reason = clipped_partition_proof(row)
            if proof is None:
                failures[reason] += 1
                failed_rows.append(row)
                failed_volume += box_volume(row.box)
            else:
                proofs.append(proof)
                closed_volume += box_volume(row.box)
        require(
            failures == Counter({TARGET_FAILURE: len(failed_rows)})
            and bool(failed_rows),
            f"Round184 target failure only:{origin}",
        )
        source_meta = replay["origins"][origin]
        source = r180.r176.physical_domain(
            source_meta["chart_id"], source_meta["box"]
        )
        expected_failures = Counter(failures)
        if source["classification"] == SOURCE_SEAM:
            expected_failures[SOURCE_SEAM_FAILURE] += 1
        require(
            tranche["Round180_residual_child_count"] == len(final_rows)
            and tranche["closed_residual_child_count"] == len(proofs)
            and tranche["proof_rows_sha256"] == digest(proofs)
            and tranche["failure_count_by_reason"]
            == map_counter(expected_failures)
            and tranche["source_chart_domain"] == source,
            f"Round184 tranche row:{origin}",
        )
        require(
            closed_volume + failed_volume == volume,
            f"Round184 target volume partition:{origin}",
        )
        failed_by_origin[origin] = failed_rows
        source_by_origin[origin] = source
        baseline_closed_count += len(proofs)
        baseline_closed_volume += closed_volume
        target_failure_count += len(failed_rows)
        target_failure_volume += failed_volume
        residual_child_count += len(final_rows)
        residual_child_volume += volume
        if index % 20 == 0 or index == len(target_keys):
            progress(
                f"rebuild Round184 cohort {index}/{len(target_keys)}"
            )

    require(
        residual_child_count == EXPECTED_TARGET_RESIDUAL_CHILD_COUNT
        and baseline_closed_count == EXPECTED_TARGET_BASELINE_CLOSED_CELL_COUNT
        and target_failure_count == EXPECTED_TARGET_FAILURE_CELL_COUNT
        and baseline_closed_count + target_failure_count
        == residual_child_count
        and baseline_closed_volume + target_failure_volume
        == residual_child_volume,
        "Round184 target cohort census",
    )
    source_counts = Counter(
        source["classification"] for source in source_by_origin.values()
    )
    require(
        source_counts
        == Counter({
            SOURCE_INTERIOR:
                EXPECTED_TARGET_ORIGIN_COUNT
                - EXPECTED_TARGET_SOURCE_SEAM_COUNT,
            SOURCE_SEAM: EXPECTED_TARGET_SOURCE_SEAM_COUNT,
        }),
        "target cohort source domains",
    )

    all_source_seam_keys = inputs["source_seam_keys"]
    for origin in all_source_seam_keys:
        meta = replay["origins"][origin]
        source = r180.r176.physical_domain(meta["chart_id"], meta["box"])
        require(
            source["classification"] == SOURCE_SEAM
            and source["source_seam_half_open_owner"] == "E",
            f"all source seams rebuilt:{origin}",
        )

    return {
        "failed_by_origin": failed_by_origin,
        "source_by_origin": source_by_origin,
        "baseline_closed_count": baseline_closed_count,
        "baseline_closed_volume": baseline_closed_volume,
        "target_failure_count": target_failure_count,
        "target_failure_volume": target_failure_volume,
        "residual_child_count": residual_child_count,
        "residual_child_volume": residual_child_volume,
        "source_counts": source_counts,
    }


def child_frontier(
    parent: r180.r176.Frontier,
    box: r180.r176.Box,
) -> r180.r176.Frontier:
    return r180.r176.Frontier(
        parent.chart_id,
        box,
        parent.active_targets,
        parent.origin_key,
        parent.failure,
    )


def refine_failed_roots(
    roots: list[r180.r176.Frontier],
    maximum_depth: int,
) -> dict[str, Any]:
    input_volume = sum((box_volume(row.box) for row in roots), Q(0))
    closed_volume = Q(0)
    residual_volume = Q(0)
    evaluated = 0
    split_count = 0
    closed_count = 0
    residual_count = 0
    split_axes: Counter[str] = Counter()
    closed_methods: Counter[str] = Counter()
    closed_depths: Counter[int] = Counter()
    residual_depths: Counter[int] = Counter()
    residual_reasons: Counter[str] = Counter()
    closed_volume_by_depth: defaultdict[int, Q] = defaultdict(Q)
    residual_volume_by_depth: defaultdict[int, Q] = defaultdict(Q)
    residual_keys: list[str] = []

    for root in roots:
        root_volume = box_volume(root.box)
        root_closed = Q(0)
        root_residual = Q(0)
        pending = [(root, 0)]
        while pending:
            row, depth = pending.pop()
            evaluated += 1
            volume = box_volume(row.box)
            direct_kind, direct_evidence = direct_strict_terminal(row)
            if direct_kind == "EXCLUDED":
                require(
                    direct_evidence is not None
                    and direct_evidence["method"]
                    == "DIRECT_STRICT_CLOSED_BOX"
                    and direct_evidence["whole_closed_child"]
                    and direct_evidence[
                        "all_owned_boundary_strata_inherit_strict_proof"
                    ],
                    f"direct excluded contract:{row.key}",
                )
                closed_count += 1
                closed_methods["DIRECT_STRICT_CLOSED_BOX"] += 1
                closed_depths[depth] += 1
                closed_volume += volume
                root_closed += volume
                closed_volume_by_depth[depth] += volume
                continue
            if direct_kind is not None:
                require(
                    direct_kind in {"LIVE", "MIXED"}
                    and direct_evidence is not None
                    and direct_evidence["whole_closed_child"],
                    f"direct retained contract:{row.key}",
                )
                reason = f"DIRECT_STRICT_{direct_kind}"
                residual_count += 1
                residual_depths[depth] += 1
                residual_reasons[reason] += 1
                residual_volume += volume
                root_residual += volume
                residual_volume_by_depth[depth] += volume
                residual_keys.append(row.key)
                continue

            proof, reason = clipped_partition_proof(row)
            if proof is not None:
                require(
                    reason == "CLOSED"
                    and proof["all_three_strata_excluded"]
                    and proof["whole_closed_cell_excluded"],
                    f"clipped closed proof contract:{row.key}",
                )
                closed_count += 1
                closed_methods["CLIPPED_DELTA_THREE_STRATUM"] += 1
                closed_depths[depth] += 1
                closed_volume += volume
                root_closed += volume
                closed_volume_by_depth[depth] += volume
                continue
            if depth == maximum_depth:
                residual_count += 1
                residual_depths[depth] += 1
                residual_reasons[reason] += 1
                residual_volume += volume
                root_residual += volume
                residual_volume_by_depth[depth] += volume
                residual_keys.append(row.key)
                continue
            axis = r180.split_axis(row.box)
            require(axis in (0, 1, 2), f"split axis:{row.key}")
            lower, upper = r180.r176.split(row.box, axis)
            require(
                box_volume(lower) + box_volume(upper) == volume,
                f"split volume:{row.key}",
            )
            split_count += 1
            split_axes[("t", "p", "s")[axis]] += 1
            pending.append((child_frontier(row, upper), depth + 1))
            pending.append((child_frontier(row, lower), depth + 1))
        require(
            root_closed + root_residual == root_volume,
            f"failed-root volume conservation:{root.key}",
        )

    require(
        closed_volume + residual_volume == input_volume,
        "adaptive failed-cell volume conservation",
    )
    residual_keys.sort()
    return {
        "input_failed_root_count": len(roots),
        "input_failed_root_volume": input_volume,
        "evaluated_node_count": evaluated,
        "split_parent_count": split_count,
        "split_axis_count": split_axes,
        "closed_terminal_cell_count": closed_count,
        "closed_terminal_volume": closed_volume,
        "closed_terminal_count_by_method": closed_methods,
        "closed_terminal_count_by_extra_depth": closed_depths,
        "closed_terminal_volume_by_extra_depth": closed_volume_by_depth,
        "residual_terminal_cell_count": residual_count,
        "residual_terminal_volume": residual_volume,
        "residual_terminal_count_by_extra_depth": residual_depths,
        "residual_terminal_volume_by_extra_depth": residual_volume_by_depth,
        "residual_failure_count": residual_reasons,
        "residual_cell_keys": residual_keys,
    }


def build_probe(extra_depth: int) -> dict[str, Any]:
    require(type(extra_depth) is int, "extra depth type")
    require(0 <= extra_depth <= 4, "extra depth range")
    inputs = check_inputs()
    rebuilt = rebuild_round184_target_children(inputs)

    progress(
        f"probe {EXPECTED_TARGET_FAILURE_CELL_COUNT} failed cells "
        f"through extra depth {extra_depth}"
    )
    aggregate_counts: Counter[str] = Counter()
    aggregate_fractions: defaultdict[str, Q] = defaultdict(Q)
    split_axes: Counter[str] = Counter()
    closed_methods: Counter[str] = Counter()
    closed_depths: Counter[int] = Counter()
    residual_depths: Counter[int] = Counter()
    residual_reasons: Counter[str] = Counter()
    closed_volume_by_depth: defaultdict[int, Q] = defaultdict(Q)
    residual_volume_by_depth: defaultdict[int, Q] = defaultdict(Q)
    residual_keys: list[str] = []
    geometrically_complete: list[str] = []
    strict_interior_complete: list[str] = []
    seam_geometrically_complete: list[str] = []
    residual_origins: list[str] = []

    for index, origin in enumerate(inputs["target_keys"], 1):
        outcome = refine_failed_roots(
            rebuilt["failed_by_origin"][origin],
            extra_depth,
        )
        for key in (
            "input_failed_root_count",
            "evaluated_node_count",
            "split_parent_count",
            "closed_terminal_cell_count",
            "residual_terminal_cell_count",
        ):
            aggregate_counts[key] += outcome[key]
        for key in (
            "input_failed_root_volume",
            "closed_terminal_volume",
            "residual_terminal_volume",
        ):
            aggregate_fractions[key] += outcome[key]
        split_axes.update(outcome["split_axis_count"])
        closed_methods.update(outcome["closed_terminal_count_by_method"])
        closed_depths.update(
            outcome["closed_terminal_count_by_extra_depth"]
        )
        residual_depths.update(
            outcome["residual_terminal_count_by_extra_depth"]
        )
        residual_reasons.update(outcome["residual_failure_count"])
        for depth, volume in outcome[
            "closed_terminal_volume_by_extra_depth"
        ].items():
            closed_volume_by_depth[depth] += volume
        for depth, volume in outcome[
            "residual_terminal_volume_by_extra_depth"
        ].items():
            residual_volume_by_depth[depth] += volume
        residual_keys.extend(outcome["residual_cell_keys"])

        if outcome["residual_terminal_cell_count"] == 0:
            geometrically_complete.append(origin)
            source_class = rebuilt["source_by_origin"][origin][
                "classification"
            ]
            if source_class == SOURCE_INTERIOR:
                strict_interior_complete.append(origin)
            else:
                require(
                    source_class == SOURCE_SEAM,
                    f"complete origin source class:{origin}",
                )
                seam_geometrically_complete.append(origin)
        else:
            residual_origins.append(origin)
        if index % 10 == 0 or index == len(inputs["target_keys"]):
            progress(
                f"adaptive probe origins {index}/{len(inputs['target_keys'])}"
            )

    require(
        aggregate_counts["input_failed_root_count"]
        == EXPECTED_TARGET_FAILURE_CELL_COUNT
        and aggregate_fractions["input_failed_root_volume"]
        == rebuilt["target_failure_volume"]
        and (
            aggregate_fractions["closed_terminal_volume"]
            + aggregate_fractions["residual_terminal_volume"]
        )
        == rebuilt["target_failure_volume"]
        and len(geometrically_complete) + len(residual_origins)
        == EXPECTED_TARGET_ORIGIN_COUNT,
        "global adaptive census and volume",
    )
    target_total_volume = rebuilt["residual_child_volume"]
    total_closed_volume = (
        rebuilt["baseline_closed_volume"]
        + aggregate_fractions["closed_terminal_volume"]
    )
    require(
        total_closed_volume
        + aggregate_fractions["residual_terminal_volume"]
        == target_total_volume,
        "target residual support volume conservation",
    )

    for values in (
        residual_keys,
        geometrically_complete,
        strict_interior_complete,
        seam_geometrically_complete,
        residual_origins,
    ):
        values.sort()
    all_source_seam_keys = inputs["source_seam_keys"]
    target_source_seam_keys = inputs["target_source_seam_keys"]
    outside_target_source_seams = sorted(
        set(all_source_seam_keys) - set(target_source_seam_keys)
    )
    require(
        len(outside_target_source_seams)
        == EXPECTED_ALL_SOURCE_SEAM_COUNT
        - EXPECTED_TARGET_SOURCE_SEAM_COUNT,
        "outside-cohort source seam count",
    )

    result = {
        "status": (
            "READ_ONLY_ZERO_PROMOTION_SOURCE_W_STRICT_FIRST_REFINEMENT_PROBE"
        ),
        "parameters": {
            "extra_depth": extra_depth,
            "legal_extra_depth_range": [0, 4],
            "arb_precision_bits": 192,
            "adaptive_split_rule":
                "Round180 longest exact rational coordinate width; "
                "ties t,p,s",
        },
        "input_chain": inputs["pins"],
        "scope": {
            "source_obstacle": "W",
            "Round184_priority_class": "PURE_SINGLE_CLIPPED_DELTA",
            "target_failure": TARGET_FAILURE,
            "target_origin_count": EXPECTED_TARGET_ORIGIN_COUNT,
            "target_origin_keys_sha256":
                EXPECTED_TARGET_ORIGIN_KEYS_SHA256,
            "target_source_domain_count":
                map_counter(rebuilt["source_counts"]),
            "Round184_residual_child_count":
                rebuilt["residual_child_count"],
            "Round184_residual_child_volume":
                str(rebuilt["residual_child_volume"]),
        },
        "Round184_equivalent_reconstruction": {
            "method":
                "PINNED_ROUND180_GEOMETRY_PLUS_ROUND184_EQUIVALENT_"
                "CLIPPED_DELTA_THREE_STRATUM",
            "baseline_closed_child_count":
                rebuilt["baseline_closed_count"],
            "baseline_closed_child_volume":
                str(rebuilt["baseline_closed_volume"]),
            "target_failure_cell_count":
                rebuilt["target_failure_count"],
            "target_failure_cell_volume":
                str(rebuilt["target_failure_volume"]),
            "exact_child_and_volume_partition_reconfirmed": True,
        },
        "bounded_refinement": {
            "input_failed_root_count":
                aggregate_counts["input_failed_root_count"],
            "input_failed_root_volume":
                str(aggregate_fractions["input_failed_root_volume"]),
            "evaluated_node_count":
                aggregate_counts["evaluated_node_count"],
            "split_parent_count":
                aggregate_counts["split_parent_count"],
            "split_axis_count": map_counter(split_axes),
            "closed_terminal_cell_count":
                aggregate_counts["closed_terminal_cell_count"],
            "closed_terminal_volume":
                str(aggregate_fractions["closed_terminal_volume"]),
            "closed_terminal_count_by_method":
                map_counter(closed_methods),
            "closed_terminal_count_by_extra_depth":
                map_counter(closed_depths),
            "closed_terminal_volume_by_extra_depth":
                fraction_map(closed_volume_by_depth),
            "residual_terminal_cell_count":
                aggregate_counts["residual_terminal_cell_count"],
            "residual_terminal_volume":
                str(aggregate_fractions["residual_terminal_volume"]),
            "residual_terminal_count_by_extra_depth":
                map_counter(residual_depths),
            "residual_terminal_volume_by_extra_depth":
                fraction_map(residual_volume_by_depth),
            "residual_failure_count": map_counter(residual_reasons),
            "residual_cell_keys_sha256": digest(residual_keys),
            "exact_failed_cell_volume_conservation": True,
        },
        "original_origin_probe_outcome": {
            "geometrically_complete_origin_count":
                len(geometrically_complete),
            "geometrically_complete_origin_keys_sha256":
                digest(geometrically_complete),
            "strict_physical_interior_complete_origin_count":
                len(strict_interior_complete),
            "strict_physical_interior_complete_origin_keys":
                strict_interior_complete,
            "strict_physical_interior_complete_origin_keys_sha256":
                digest(strict_interior_complete),
            "source_seam_geometrically_complete_but_held_out_count":
                len(seam_geometrically_complete),
            "source_seam_geometrically_complete_but_held_out_keys":
                seam_geometrically_complete,
            "residual_origin_count": len(residual_origins),
            "residual_origin_keys": residual_origins,
            "residual_origin_keys_sha256": digest(residual_origins),
            "Round184_residual_support_closed_volume":
                str(total_closed_volume),
            "Round184_residual_support_residual_volume":
                str(aggregate_fractions["residual_terminal_volume"]),
            "exact_support_volume_conservation": True,
        },
        "source_seam_holdout": {
            "Round184_pure_tranche_source_seam_origin_count":
                EXPECTED_ALL_SOURCE_SEAM_COUNT,
            "Round184_pure_tranche_source_seam_origin_keys":
                all_source_seam_keys,
            "Round184_pure_tranche_source_seam_origin_keys_sha256":
                EXPECTED_ALL_SOURCE_SEAM_KEYS_SHA256,
            "target_failure_cohort_source_seam_origin_count":
                EXPECTED_TARGET_SOURCE_SEAM_COUNT,
            "target_failure_cohort_source_seam_origin_keys":
                target_source_seam_keys,
            "target_failure_cohort_source_seam_origin_keys_sha256":
                EXPECTED_TARGET_SOURCE_SEAM_KEYS_SHA256,
            "outside_target_failure_cohort_source_seam_origin_count":
                len(outside_target_source_seams),
            "outside_target_failure_cohort_source_seam_origin_keys":
                outside_target_source_seams,
            "required_future_method":
                "SEPARATE_PHYSICAL_SOURCE_SEAM_HALF_OPEN_PARTITION",
            "source_seam_half_open_owner": "E",
            "probe_source_seam_official_credit": 0,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "filesystem_writes": 0,
            "official_ledger_mutated": False,
            "probe_counts_applied_to_official_ledger": False,
            "whole_origin_integer_credit_issued": 0,
            "D02": "UNCHANGED_BLOCKED",
            "D03_negative_oracle": "UNCHANGED_UNAUTHORIZED",
            "CM2": "UNCHANGED_NO_GO",
            "required_next":
                "formal producer plus independent verifier before any "
                "ledger use",
        },
    }
    return {
        "schema": SCHEMA,
        "probe_result": result,
        "probe_result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--extra-depth",
        type=int,
        choices=range(5),
        default=2,
        help="additional bounded binary refinement depth (0..4; default 2)",
    )
    arguments = parser.parse_args()
    ctx.prec = 192
    document = build_probe(arguments.extra_depth)
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
