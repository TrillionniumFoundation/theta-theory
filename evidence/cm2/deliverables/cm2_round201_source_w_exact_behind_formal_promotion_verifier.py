#!/usr/bin/env python3
"""Independent verifier for the formal Round201 source-W promotion.

The Round201 producer is treated only as pinned inert regular-file bytes.  This
verifier imports no Round201 producer or diagnostic probe.  It independently
reconstructs the complete expected result from the frozen Round180 independent
verifier geometry and the pinned Round184 formal package, then requires exact
Python-object and canonical-JSON equality with the 1.1 GB certificate.

The reconstruction code is deliberately standalone in this file.  Its formal
independence boundary is non-import/non-execution plus a fresh process and
upstream evaluator pinning; it is not claimed to be an implementation-diverse
second derivation of every interval formula.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Callable

sys.dont_write_bytecode = True

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round201_source_w_exact_behind_formal_promotion_certificate.json"
)
SCHEMA = "cm2.round201.source-w-exact-behind-formal-promotion.v1"
PRODUCER = (
    HERE / "cm2_round201_source_w_exact_behind_formal_promotion.py"
)
PRODUCER_SHA256 = (
    "f7e53607d9a2c6b2f4fda76c9a6a92845f12cced04e28168f227cb516a1f4010"
)
CERTIFICATE = OUTPUT
CERTIFICATE_SHA256 = (
    "72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536"
)
CERTIFICATE_SIZE = 1_115_443_418
EXPECTED_RESULT_SHA256 = (
    "9d3dc29c07f81ba2b71743e983c3d4718e40a430d3566cc934d4a3098facad3c"
)
VERIFICATION_OUTPUT = (
    HERE
    / "cm2_round201_source_w_exact_behind_formal_promotion_verification.json"
)
VERIFICATION_SCHEMA = (
    "cm2.round201.source-w-exact-behind-formal-promotion.verification.v1"
)
MAX_INPUT_BYTES = 16 * 1024 * 1024

ROUND184_MANIFEST = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_manifest.sha256"
)
ROUND184_MANIFEST_SHA256 = (
    "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1"
)
ROUND184_PINS = {
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py":
        "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_certificate.json":
        "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_verifier.py":
        "55a4e2b44d0f8617d7b7fd0befd251a5cb206d388c23d7b395e39b9a17fa4889",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_verification.json":
        "7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_report.md":
        "21c424cd3180f01a8b7b239ef2747c63d6f2787694c173b89d0d9a35b6594ff1",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_cold_replay.md":
        "b57a96d7205459e4e9b72f159e22e6e2e8e514f88370d1ca41971d7a6b7727e9",
}
ROUND184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_certificate.json"
)
ROUND184_VERIFICATION = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
    "_verification.json"
)
ROUND184_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
ROUND184_VERIFICATION_RESULT_SHA256 = (
    "126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9"
)
ROUND184_REGISTRY_ROWS_SHA256 = (
    "d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e"
)
ROUND184_CLOSED_KEYS_SHA256 = (
    "9105617c4f5d60e2bb9f2e602472cb489bad5af23edcdfb9a2e11de9efd0a8ae"
)

ROUND180_VERIFIER = (
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py"
)
ROUND180_VERIFIER_SHA256 = (
    "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4"
)
ROUND176_VERIFIER = (
    "cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py"
)
ROUND176_VERIFIER_SHA256 = (
    "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796"
)

CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
FULL_P = "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
MULTI = "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
COMPACT_Q = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
TYPED_DOUBLE = "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
H_RESIDUAL = "OUTGOING_H_GRAPH_INTERSECTION_RESIDUAL"

PURE_CLASS = "PURE_SINGLE_CLIPPED_DELTA"
ROOT_CLASS = "PURE_ROOT_EQUALITY"
DELTA_MULTI_CLASS = "DELTA_H_OR_MULTI_NO_Q"
COMPACT_CLASS = "COMPACT_Q_PRESENT"
CLASS_RANK = {
    PURE_CLASS: 0,
    ROOT_CLASS: 1,
    DELTA_MULTI_CLASS: 2,
    COMPACT_CLASS: 3,
}

SOURCE_INTERIOR = "STRICT_PHYSICAL_CHART_INTERIOR"
SOURCE_SEAM = "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
SOURCE_SEAM_FAILURE = (
    "PHYSICAL_SEAM_COMPOSITE_REQUIRES_SEPARATE_HALF_OPEN_PARTITION"
)
TARGET_FAILURE = "TARGET_NOT_STRICT_POSITIVE_FIRST"
FULL_P_FAILURE = "NOT_CLIPPED_FULL_P_GRAPH"
UNRESOLVED_CLASSES = {
    "unresolved_discriminant",
    "unresolved_root_sign",
}

EXPECTED_PURE_TARGET_ORIGIN_COUNT = 162
EXPECTED_PURE_TARGET_ORIGIN_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_PURE_STRICT_CREDIT_COUNT = 156
EXPECTED_PURE_STRICT_CREDIT_KEYS_SHA256 = (
    "801ea4127662806c9e29f8d356ad09279e528460109d71f929ba5ebe51b0f7fd"
)
EXPECTED_PURE_TARGET_SEAM_COUNT = 6
EXPECTED_PURE_TARGET_SEAM_KEYS_SHA256 = (
    "d21a934ed6d43ba876ab514cd710b0f659f3e94e543b3c4e11ea6d719fe0d208"
)
EXPECTED_PURE_DEPTH2_EXACT_BEHIND_CELL_COUNT = 37262
EXPECTED_PURE_DEPTH2_EXACT_BEHIND_KEYS_SHA256 = (
    "060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e"
)
EXPECTED_PURE_DEPTH2_EXACT_BEHIND_VOLUME = Q(
    3297687, 838860800000
)

EXPECTED_GENERALIZED_ORIGIN_COUNT = 650
EXPECTED_GENERALIZED_CLASS_ORIGIN_COUNT = {
    DELTA_MULTI_CLASS: 596,
    COMPACT_CLASS: 54,
}
EXPECTED_GENERALIZED_ORIGIN_KEYS_SHA256 = (
    "36c2f93e9252373ee95fd4574c84f8d8084b1d6cd2e4467ebb6e6670d48e7467"
)
EXPECTED_GENERALIZED_CELL_COUNT = 182776
EXPECTED_GENERALIZED_EXACT_VOLUME = Q(4043919, 52428800000)
DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_COUNT = 390
DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_KEYS_SHA256 = (
    "10d69f94b08b35b199dbb5eeb4d4047b84d7b104b7df1123eb8938121b438080"
)
DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_SEAM_COUNT = 6
DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_SEAM_KEYS_SHA256 = (
    "fe8d0a7d4c04c66f47d011d54478d011849abd8a90152391a4bb269bf42bd812"
)
EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_COUNT = 390
EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_KEYS_SHA256 = (
    "10d69f94b08b35b199dbb5eeb4d4047b84d7b104b7df1123eb8938121b438080"
)
EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_COUNT = 6
EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_KEYS_SHA256 = (
    "fe8d0a7d4c04c66f47d011d54478d011849abd8a90152391a4bb269bf42bd812"
)
EXPECTED_EMPTY_KEYS_SHA256 = (
    "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
)
EXPECTED_GENERALIZED_INCOMPLETE_MIXED_COUNT = 200
DIAGNOSTIC_RESIDUAL_ONLY_UNION_COUNT = 546
DIAGNOSTIC_RESIDUAL_ONLY_UNION_KEYS_SHA256 = (
    "b0c171c0c27bf2e7ea4125dd8b1d46f47532d7d5227fcb3aa00377d2758b95fb"
)
DIAGNOSTIC_COMBINED_FINAL_RESIDUAL_SEAM_COUNT = 12
DIAGNOSTIC_COMBINED_FINAL_RESIDUAL_SEAM_KEYS_SHA256 = (
    "52d6d7a34cec1ad06bfa4065c45f82a3f6d9c99e2e726e798b7bc28b0ebd71b9"
)
EXPECTED_COMBINED_FORMAL_CREDIT_COUNT = 546
EXPECTED_COMBINED_FORMAL_CREDIT_KEYS_SHA256 = (
    "b0c171c0c27bf2e7ea4125dd8b1d46f47532d7d5227fcb3aa00377d2758b95fb"
)
EXPECTED_COMBINED_FORMAL_SEAM_HOLD_COUNT = 12
EXPECTED_COMBINED_FORMAL_SEAM_HOLD_KEYS_SHA256 = (
    "52d6d7a34cec1ad06bfa4065c45f82a3f6d9c99e2e726e798b7bc28b0ebd71b9"
)
EXPECTED_COMBINED_WHOLE_RECORD_EXCLUDED = 74558
EXPECTED_COMBINED_CONSERVATIVE_LIVE = 2274
EXPECTED_REMAINING_ORIGIN_COUNT = 278

FUTURE_PROTECTED = (
    "cm2_round201_source_w_exact_behind_formal_promotion_verifier.py",
    "cm2_round201_source_w_exact_behind_formal_promotion_verification.json",
    "cm2_round201_source_w_exact_behind_formal_promotion_report.md",
    "cm2_round201_source_w_exact_behind_formal_promotion_cold_replay.md",
    "cm2_round201_source_w_exact_behind_formal_promotion_manifest.sha256",
)


def require(condition: bool, label: str) -> None:
    if condition:
        return
    raise RuntimeError(label)


def canonical(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return encoded


def digest(value: Any) -> str:
    state = hashlib.sha256()
    state.update(canonical(value).encode("utf-8"))
    return state.hexdigest()


def pretty_bytes(value: Any) -> bytes:
    rendered = json.dumps(
        value,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    )
    return f"{rendered}\n".encode("utf-8")


def map_counter(value: Counter[Any]) -> dict[str, int]:
    mapped: dict[str, int] = {}
    for key in sorted(value, key=lambda item: str(item)):
        mapped[str(key)] = value[key]
    return mapped


def fraction_map(value: dict[Any, Q]) -> dict[str, str]:
    mapped: dict[str, str] = {}
    for key, item in sorted(value.items()):
        mapped[str(key)] = str(item)
    return mapped


def nested_counter_map(
    value: dict[str, Counter[Any]],
) -> dict[str, dict[str, int]]:
    mapped: dict[str, dict[str, int]] = {}
    for key in sorted(value):
        mapped[key] = map_counter(value[key])
    return mapped


def progress(message: str) -> None:
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


def reject_surrogates(value: Any, label: str) -> None:
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, str):
            bad = any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in item
            )
            require(not bad, f"surrogate:{label}")
        elif type(item) is list:
            pending.extend(item)
        elif type(item) is dict:
            pending.extend(item.keys())
            pending.extend(item.values())


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
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
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


def strict_load(path: Path) -> dict[str, Any]:
    raw = read_regular(path)
    return strict_load_bytes(raw, path.name)


def preimport_pin() -> None:
    pins = (
        (ROUND180_VERIFIER, ROUND180_VERIFIER_SHA256, "Round180"),
        (ROUND176_VERIFIER, ROUND176_VERIFIER_SHA256, "Round176"),
    )
    for filename, expected, label in pins:
        actual = hashlib.sha256(read_regular(HERE / filename)).hexdigest()
        require(actual == expected, f"{label} verifier pre-import pin")


preimport_pin()
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r180 = importlib.import_module(
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier"
)
preimport_pin()
r176 = r180.r176


def check_upstream() -> dict[str, Any]:
    require(
        Path(r180.__file__).resolve() == (HERE / ROUND180_VERIFIER).resolve(),
        "Round180 verifier module identity",
    )
    require(
        Path(r176.__file__).resolve() == (HERE / ROUND176_VERIFIER).resolve(),
        "Round176 verifier module identity",
    )
    require(
        hashlib.sha256(read_regular(HERE / ROUND184_MANIFEST)).hexdigest()
        == ROUND184_MANIFEST_SHA256,
        "Round184 manifest pin",
    )
    manifest_entries: dict[str, str] = {}
    for line in read_regular(HERE / ROUND184_MANIFEST).decode(
        "ascii", "strict"
    ).splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest_entries, f"manifest duplicate:{name}")
        manifest_entries[name] = value
        require(
            name in ROUND184_PINS
            and value == ROUND184_PINS[name]
            and hashlib.sha256(read_regular(HERE / name)).hexdigest()
            == value,
            f"Round184 manifest entry:{name}",
        )
    require(manifest_entries == ROUND184_PINS, "Round184 manifest exact set")

    certificate = strict_load(HERE / ROUND184_CERTIFICATE)
    verification = strict_load(HERE / ROUND184_VERIFICATION)
    require(
        certificate["schema"]
        == "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta.v1"
        and certificate["result_sha256"] == ROUND184_RESULT_SHA256
        and digest(certificate["result"]) == ROUND184_RESULT_SHA256,
        "Round184 certificate result",
    )
    require(
        verification["schema"]
        == (
            "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta."
            "verification.v1"
        )
        and verification["result_sha256"]
        == ROUND184_VERIFICATION_RESULT_SHA256
        and digest(verification["result"])
        == ROUND184_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"]
        == "PASS_PARTIAL_BOUNDED_ROUND184"
        and verification["result"]["independence_contract"][
            "full_expected_canonical_equality"
        ]
        and verification["result"]["independence_contract"][
            "producer_imported_or_executed"
        ] is False,
        "Round184 independent verification",
    )
    result = certificate["result"]
    require(
        result["priority_registry"]["row_count"] == 1444
        and result["priority_registry"]["rows_sha256"]
        == ROUND184_REGISTRY_ROWS_SHA256
        and result["pure_single_clipped_Delta_tranche"][
            "closed_origin_count"
        ] == 620
        and result["pure_single_clipped_Delta_tranche"][
            "closed_exact_origin_keys_sha256"
        ] == ROUND184_CLOSED_KEYS_SHA256
        and result["ledger_composition"]["combined_whole_record_excluded"]
        == 74012
        and result["ledger_composition"]["combined_conservative_live"]
        == 2820
        and result["strict_nonpromotion"]["D02"] == "BLOCKED",
        "Round184 frozen ledger",
    )
    r180.check_chain()
    return {
        "certificate": certificate,
        "verification": verification,
        "Round184_manifest_sha256": ROUND184_MANIFEST_SHA256,
        "Round184_manifest_entries_replayed": True,
        "Round184_result_sha256": ROUND184_RESULT_SHA256,
        "Round184_verification_result_sha256":
            ROUND184_VERIFICATION_RESULT_SHA256,
        "Round180_verifier_sha256": ROUND180_VERIFIER_SHA256,
        "Round176_verifier_sha256": ROUND176_VERIFIER_SHA256,
    }


def box_volume(box: Any) -> Q:
    volume = Q(1)
    for lower, upper in (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    ):
        volume *= upper - lower
    return volume


def support_class(counts: Counter[str]) -> str:
    support = set(counts)
    if COMPACT_Q in support:
        return COMPACT_CLASS
    singleton = {
        CLIPPED: PURE_CLASS,
        FULL_P: ROOT_CLASS,
    }
    if len(support) == 1:
        only = next(iter(support))
        if only in singleton:
            return singleton[only]
    return DELTA_MULTI_CLASS


def reconstruct_registry(
    upstream: dict[str, Any],
) -> dict[str, Any]:
    progress("Round201 replay frozen Round180 frontier")
    replay = r176.replay_frontier()
    base_kinds: defaultdict[str, set[str]] = defaultdict(set)
    base_kinds.update({
        key: set(values)
        for key, values in replay["origin_kinds"].items()
    })
    base_closed_by_origin: Counter[str] = Counter()
    residual_by_origin: dict[str, list[Any]] = defaultdict(list)
    for row in replay["frontier"]:
        kind, _evidence = r176.closure(row)
        if kind is None:
            residual_by_origin[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key].add(kind)
            base_closed_by_origin[row.origin_key] += 1
    for rows in residual_by_origin.values():
        rows.sort(key=lambda row: row.key)
    upper_candidates = sorted(
        origin
        for origin in residual_by_origin
        if base_kinds[origin] <= {"EXCLUDED"}
    )
    require(
        len(upper_candidates) == 1476
        and digest(upper_candidates)
        == "c15ab39fcffba53204de689f631110e5888df616e47d56a08f8cb42f72ee8aad",
        "Round180 upper candidates",
    )

    complete_round180: list[str] = []
    priority_rows: list[dict[str, Any]] = []
    refinements: dict[str, dict[str, Any]] = {}
    final_rows: dict[str, list[Any]] = {}
    for index, origin in enumerate(upper_candidates, 1):
        refinement = r180.refine_origin(residual_by_origin[origin], 4)
        remaining = refinement["final_residual_rows"]
        if not remaining:
            complete_round180.append(origin)
        else:
            refinements[origin] = refinement
            final_rows[origin] = remaining
            counts = Counter(
                r180.residual_category(row) for row in remaining
            )
            initial_counts = Counter(
                r180.initial_category(row)
                for row in residual_by_origin[origin]
            )
            class_name = support_class(counts)
            registry_row = {
                "origin_key": origin,
                "priority_class": class_name,
                "priority_class_rank": CLASS_RANK[class_name],
                "priority_key": [
                    CLASS_RANK[class_name], len(remaining), origin
                ],
                "Round176_residual_root_count":
                    len(residual_by_origin[origin]),
                "Round176_preclosed_frontier_count":
                    base_closed_by_origin[origin],
                "Round176_preclosed_kinds":
                    sorted(base_kinds[origin]),
                "initial_residual_category_count":
                    map_counter(initial_counts),
                "Round180_residual_child_count": len(remaining),
                "Round180_residual_category_count": map_counter(counts),
                "Round180_residual_category_support": sorted(counts),
                "Round180_residual_child_volume": str(sum(
                    (box_volume(child.box) for child in remaining), Q(0)
                )),
                "Round180_residual_child_keys_sha256": digest(
                    sorted(child.key for child in remaining)
                ),
                "selection_uses_new_closure_outcome": False,
            }
            registry_row["row_sha256"] = digest(registry_row)
            priority_rows.append(registry_row)
        if index % 200 == 0 or index == len(upper_candidates):
            progress(
                f"Round201 registry origins {index}/{len(upper_candidates)}"
            )

    complete_round180.sort()
    require(
        len(complete_round180) == 32
        and digest(complete_round180)
        == "70300cade4136fdb41f4b1f8900b47b89f0d9a498f7afd0c0d614296f84b3c87",
        "Round180 complete origins",
    )
    priority_rows.sort(key=lambda row: tuple(row["priority_key"]))
    for ordinal, row in enumerate(priority_rows):
        row["priority_ordinal"] = ordinal
        row["row_sha256"] = digest({
            key: value for key, value in row.items()
            if key != "row_sha256"
        })
    certificate_registry = upstream["certificate"]["result"][
        "priority_registry"
    ]
    require(
        len(priority_rows) == 1444
        and digest(priority_rows) == ROUND184_REGISTRY_ROWS_SHA256
        and priority_rows == certificate_registry["rows"],
        "full canonical Round184 registry reconstruction",
    )
    return {
        "replay": replay,
        "base_kinds": base_kinds,
        "base_closed_by_origin": base_closed_by_origin,
        "residual_by_origin": residual_by_origin,
        "upper_candidates": upper_candidates,
        "complete_round180": complete_round180,
        "priority_rows": priority_rows,
        "priority_by_origin": {
            row["origin_key"]: row for row in priority_rows
        },
        "refinements": refinements,
        "final_rows": final_rows,
    }


def arb_sign_name(value: arb) -> str:
    sign_name = {
        1: "STRICT_POSITIVE",
        -1: "STRICT_NEGATIVE",
        0: "OVERWRAP",
    }
    return sign_name[r176.sign(value)]


def strict_chart(nx: arb, ny: arb) -> str | None:
    candidates: list[str] = []
    for cell, first, second in (
        ("E", nx - ny, nx + ny),
        ("W", -nx - ny, -nx + ny),
        ("N", ny - nx, ny + nx),
        ("S", -ny - nx, -ny + nx),
    ):
        if bool(first > 0) and bool(second > 0):
            candidates.append(cell)
    if len(candidates) != 1:
        return None
    return candidates[0]


def tangent_chart(row: Any, candidate: Any) -> str | None:
    geometry = r176.geometry(row.chart_id, row.box)
    ux, uy = geometry[2], geometry[3]
    target = r176.TARGETS[candidate.target_id]
    radius = r176.base.arbq(r176.base.RADIUS[target.obstacle])
    nx = candidate.transverse * uy / radius
    ny = -candidate.transverse * ux / radius
    return strict_chart(nx, ny)


def clipped_partition_proof(
    row: Any,
) -> tuple[dict[str, Any] | None, str]:
    """Locally rebuild the formal Round184 clipped-Delta decision."""
    records = r176.records_for(
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
    derivative, lower, upper, full = r176.graph_faces(row, candidate)
    if derivative == 0:
        return None, "P_DERIVATIVE_OVERWRAP"
    if full:
        return None, FULL_P_FAILURE
    if not r176.target_positive_first(candidate, records):
        return None, TARGET_FAILURE
    negative = r176.remove_disposition(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        return None, "DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"

    graph_owner = candidate.target_id
    positive_chart: str | None = None
    graph_chart: str | None = None
    if candidate.target_id != r176.FROZEN_OWNER:
        positive = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        graph = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        owner_reason = "candidate target differs from frozen owner"
    else:
        positive_chart = r176.positive_chart(row, candidate)
        if positive_chart is None:
            return None, "DELTA_POSITIVE_OUTGOING_CHART_OVERWRAP"
        if positive_chart == r176.FROZEN_CHART:
            return None, "DELTA_POSITIVE_OUTGOING_CHART_MATCH"
        graph_chart = tangent_chart(row, candidate)
        if graph_chart is None:
            return None, "DELTA_ZERO_GRAPH_OUTGOING_CHART_OVERWRAP"
        if graph_chart == r176.FROZEN_CHART:
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
        "frozen_owner": r176.FROZEN_OWNER,
        "owner_recomputation": owner_reason,
        "Delta_zero_graph_outgoing_chart": (
            graph_chart if graph_chart is not None else "NOT_APPLICABLE"
        ),
        "Delta_positive_outgoing_chart": (
            positive_chart
            if positive_chart is not None
            else "NOT_APPLICABLE"
        ),
        "frozen_outgoing_chart": r176.FROZEN_CHART,
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
    row: Any,
) -> tuple[str | None, dict[str, Any] | None]:
    leaf, _records = r176.classify(
        row.chart_id, row.box, row.active_targets
    )
    disposition, _margins = r176.terminal_disposition(
        row.chart_id, leaf
    )
    if disposition is None:
        return None, None
    coarse = r176.coarse(disposition)
    require(coarse in {"EXCLUDED", "LIVE"}, f"direct coarse:{row.key}")
    evidence = {
        "method": "DIRECT_STRICT_CLOSED_BOX",
        "disposition": disposition,
        "coarse_disposition": coarse,
        "ambient_dimension": 3,
        "whole_closed_child": True,
        "all_owned_boundary_strata_inherit_strict_proof": True,
    }
    return coarse, evidence


def exact_distance_evidence(
    row: Any,
    candidate: Any,
) -> dict[str, Any]:
    """Evaluate exact-behind geometry without importing a diagnostic probe."""
    geometry = r176.geometry(row.chart_id, row.box)
    qx, qy, s = geometry[0], geometry[1], geometry[4]
    target = r176.TARGETS[candidate.target_id]
    ax, ay = r176.base.target_center(target, s)
    displacement = ax - qx, ay - qy
    radius = r176.base.arbq(r176.base.RADIUS[target.obstacle])
    direct = sum(
        (component * component for component in displacement),
        arb(0),
    ) - radius * radius
    identity = candidate.ell * candidate.ell - candidate.discriminant
    require(
        bool(direct.overlaps(identity)),
        f"distance/identity interval overlap:{row.key}:{candidate.target_id}",
    )
    ell_negative = bool(candidate.ell < 0)
    distance_positive = bool(direct > 0)
    eligible = ell_negative and distance_positive
    evidence = {
        "target": candidate.target_id,
        "target_obstacle": target.obstacle,
        "candidate_classification": candidate.classification,
        "Delta_sign": arb_sign_name(candidate.discriminant),
        "ell_sign": arb_sign_name(candidate.ell),
        "direct_distance_margin_sign": arb_sign_name(direct),
        "identity_margin_sign": arb_sign_name(identity),
        "direct_identity_interval_overlap": True,
        "ell_strict_negative": ell_negative,
        "distance_margin_strict_positive": distance_positive,
        "eligible_exact_behind": eligible,
        "whole_box_contract":
            "Delta<0:no real root; Delta>=0 and ell<0 and "
            "distance^2-R^2=ell^2-Delta>0 imply far<0",
    }
    return evidence


def remaining_outgoing_chart(row: Any, leaf: Any) -> str:
    eligible = (
        leaf.classification == "unique_first"
        and leaf.owner_target == r176.FROZEN_OWNER
    )
    if not eligible:
        return "NOT_APPLICABLE"
    chart, _margins = r176.outgoing_generic(
        row.chart_id, row.box
    )
    if chart is None:
        return "OVERWRAP"
    return chart


def box_evidence(row: Any) -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    evidence["chart_id"] = row.chart_id
    evidence["box"] = r176.box_row(row.box)
    evidence["exact_volume"] = str(box_volume(row.box))
    evidence["active_targets"] = list(row.active_targets)
    return evidence


def single_exact_behind_cell(
    row: Any,
    input_class: str,
) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record
        for record in records
        if record.classification == "unresolved_discriminant"
    ]
    require(
        len(unresolved) == 1,
        f"single exact-behind candidate:{row.key}",
    )
    candidate = unresolved[0]
    distance = exact_distance_evidence(row, candidate)
    remaining_records = [
        record
        for record in records
        if record.target_id != candidate.target_id
    ]
    remaining_leaf = r176.classify_records(
        row.chart_id, row.box, remaining_records
    )
    disposition, _margins = r176.terminal_disposition(
        row.chart_id, remaining_leaf
    )
    require(
        disposition
        == r176.remove_disposition(row, records, candidate.target_id),
        f"single reduced disposition cross-check:{row.key}",
    )
    whole_closed = (
        distance["eligible_exact_behind"]
        and disposition is not None
        and disposition.startswith("EXCLUDED")
    )
    failure_reasons: list[str] = []
    if not distance["ell_strict_negative"]:
        failure_reasons.append("ELL_NOT_STRICT_NEGATIVE")
    if not distance["distance_margin_strict_positive"]:
        failure_reasons.append(
            "DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
        )
    if disposition is None or not disposition.startswith("EXCLUDED"):
        failure_reasons.append(
            "REDUCED_DISPOSITION_NOT_STRICT_EXCLUDED"
        )
    evidence = {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "method": "EXACT_BEHIND_SINGLE_CANDIDATE_REMOVAL",
        "input_class": input_class,
        **box_evidence(row),
        "original_record_classification_count": map_counter(Counter(
            record.classification for record in records
        )),
        "candidate_evidence": distance,
        "candidate_deleted_before_reclassification": True,
        "remaining_record_count": len(remaining_records),
        "remaining_record_classification_count": map_counter(Counter(
            record.classification for record in remaining_records
        )),
        "remaining_leaf_classification":
            remaining_leaf.classification,
        "remaining_owner_target": (
            remaining_leaf.owner_target
            if remaining_leaf.owner_target is not None
            else "NONE"
        ),
        "remaining_active_targets":
            list(remaining_leaf.active_targets),
        "remaining_tangency_targets":
            list(remaining_leaf.tangency_targets),
        "remaining_outgoing_chart":
            remaining_outgoing_chart(row, remaining_leaf),
        "remaining_disposition": (
            disposition if disposition is not None else "UNRESOLVED"
        ),
        "failure_reasons": failure_reasons,
        "coarse_disposition":
            "EXCLUDED" if whole_closed else "RESIDUAL",
        "whole_closed_cell_excluded": whole_closed,
        "ambient_dimension": 3,
        "all_owned_boundary_strata_inherit_strict_proof": whole_closed,
    }
    evidence["row_sha256"] = digest(evidence)
    return evidence


def generalized_exact_behind_cell(
    row: Any,
    category: str,
    priority_class: str,
) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = sorted(
        (
            record
            for record in records
            if record.classification in UNRESOLVED_CLASSES
        ),
        key=lambda record: record.target_id,
    )
    candidate_rows = [
        exact_distance_evidence(row, candidate)
        for candidate in unresolved
    ]
    eligible_targets = sorted(
        candidate["target"]
        for candidate in candidate_rows
        if candidate["eligible_exact_behind"]
    )
    current_records = list(records)
    deletion_rounds: list[dict[str, Any]] = []
    for round_index, target in enumerate(eligible_targets, 1):
        require(
            any(
                record.target_id == target
                and record.classification in UNRESOLVED_CLASSES
                for record in current_records
            ),
            f"eligible candidate present:{row.key}:{target}",
        )
        current_records = [
            record
            for record in current_records
            if record.target_id != target
        ]
        leaf = r176.classify_records(
            row.chart_id, row.box, current_records
        )
        disposition, _margins = r176.terminal_disposition(
            row.chart_id, leaf
        )
        deletion_rounds.append({
            "round": round_index,
            "deleted_target": target,
            "remaining_record_count": len(current_records),
            "remaining_leaf_classification": leaf.classification,
            "remaining_owner_target": (
                leaf.owner_target
                if leaf.owner_target is not None
                else "NONE"
            ),
            "remaining_outgoing_chart":
                remaining_outgoing_chart(row, leaf),
            "remaining_disposition": (
                disposition if disposition is not None else "UNRESOLVED"
            ),
        })

    final_leaf = r176.classify_records(
        row.chart_id, row.box, current_records
    )
    final_disposition, _margins = r176.terminal_disposition(
        row.chart_id, final_leaf
    )
    final_excluded = (
        final_disposition is not None
        and final_disposition.startswith("EXCLUDED")
    )
    final_live = (
        final_disposition is not None
        and final_disposition.startswith("LIVE")
    )
    whole_closed = bool(eligible_targets) and final_excluded
    remaining_unresolved = [
        record
        for record in current_records
        if record.classification in UNRESOLVED_CLASSES
    ]
    if priority_class == COMPACT_CLASS:
        residual_reason = (
            "COMPACT_Q_PRIORITY_ORIGIN_REQUIRES_INDEPENDENT_SOURCE_STRATUM"
        )
    elif not eligible_targets:
        residual_reason = "NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE"
    elif final_live:
        residual_reason = "REDUCED_REMAINING_DISPOSITION_LIVE"
    elif not final_excluded:
        residual_reason = "REDUCED_REMAINING_DISPOSITION_UNRESOLVED"
    else:
        residual_reason = "NONE__GEOMETRICALLY_CLOSED"
    evidence = {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "method": "ITERATIVE_EXACT_BEHIND_CANDIDATE_REMOVAL",
        **box_evidence(row),
        "priority_class": priority_class,
        "original_failure_type": row.failure,
        "original_residual_category": category,
        "original_record_count": len(records),
        "original_record_classification_count": map_counter(Counter(
            record.classification for record in records
        )),
        "original_unresolved_candidate_count": len(unresolved),
        "candidate_evidence_rows": candidate_rows,
        "eligible_exact_behind_candidate_count":
            len(eligible_targets),
        "deleted_candidate_targets": eligible_targets,
        "deletion_rounds": deletion_rounds,
        "remaining_record_count": len(current_records),
        "remaining_record_classification_count": map_counter(Counter(
            record.classification for record in current_records
        )),
        "remaining_unresolved_candidate_count":
            len(remaining_unresolved),
        "final_leaf_classification": final_leaf.classification,
        "final_owner_target": (
            final_leaf.owner_target
            if final_leaf.owner_target is not None
            else "NONE"
        ),
        "final_outgoing_chart":
            remaining_outgoing_chart(row, final_leaf),
        "final_disposition": (
            final_disposition
            if final_disposition is not None
            else "UNRESOLVED"
        ),
        "geometric_whole_cell_excluded": whole_closed,
        "residual_reason": residual_reason,
        "coarse_disposition":
            "EXCLUDED" if whole_closed else "RESIDUAL",
        "ambient_dimension": 3,
        "all_owned_boundary_strata_inherit_strict_proof": whole_closed,
    }
    evidence["row_sha256"] = digest(evidence)
    return evidence


def child_frontier(parent: Any, box: Any) -> Any:
    values = (
        parent.chart_id,
        box,
        parent.active_targets,
        parent.origin_key,
        parent.failure,
    )
    return r176.Frontier(*values)


def wrap_round180_terminal(
    origin: str,
    terminal: dict[str, Any],
    root_volumes: dict[str, Q],
) -> dict[str, Any]:
    coverage = Q(
        terminal["coverage_numerator"],
        terminal["coverage_denominator"],
    )
    exact_volume = root_volumes[terminal["root_depth14_cell_key"]] * coverage
    excluded = terminal["coarse_disposition"] == "EXCLUDED"
    row = {
        "cell_key": terminal["cell_key"],
        "origin_key": origin,
        "method": "INHERITED_ROUND180_" + terminal["method"],
        "exact_volume": str(exact_volume),
        "coarse_disposition": terminal["coarse_disposition"],
        "upstream_terminal_row": terminal,
        "whole_closed_cell_excluded": excluded,
        "inherited_from_verified_Round180": True,
    }
    row["row_sha256"] = digest(row)
    return row


def wrap_clipped_terminal(
    row: Any,
    proof: dict[str, Any],
    method: str,
) -> dict[str, Any]:
    wrapped: dict[str, Any] = {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "method": method,
    }
    wrapped.update(box_evidence(row))
    wrapped.update({
        "coarse_disposition": "EXCLUDED",
        "clipped_Delta_proof": proof,
        "whole_closed_cell_excluded": True,
    })
    wrapped["row_sha256"] = digest(wrapped)
    return wrapped


def rebuild_pure_target_cohort(
    upstream: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    result184 = upstream["certificate"]["result"]
    tranche = result184["pure_single_clipped_Delta_tranche"]
    tranche_by_origin = {
        row["origin_key"]: row
        for row in tranche["per_origin_rows"]
    }
    pure_keys = [
        row["origin_key"]
        for row in registry["priority_rows"]
        if row["priority_class"] == PURE_CLASS
    ]
    require(
        len(pure_keys) == 794
        and set(pure_keys) == set(tranche_by_origin),
        "Round184 pure tranche origin set",
    )
    target_keys: list[str] = []
    all_source_seam_keys: list[str] = []
    for index, origin in enumerate(pure_keys, 1):
        proofs: list[dict[str, Any]] = []
        failures: Counter[str] = Counter()
        for row in registry["final_rows"][origin]:
            proof, reason = clipped_partition_proof(row)
            if proof is None:
                failures[reason] += 1
            else:
                proofs.append(proof)
        meta = registry["replay"]["origins"][origin]
        source = r176.physical_domain(
            meta["chart_id"], meta["box"]
        )
        expected_failures = Counter(failures)
        if source["classification"] == SOURCE_SEAM:
            expected_failures[SOURCE_SEAM_FAILURE] += 1
            all_source_seam_keys.append(origin)
        existing = tranche_by_origin[origin]
        require(
            existing["Round180_residual_child_count"]
            == len(registry["final_rows"][origin])
            and existing["closed_residual_child_count"] == len(proofs)
            and existing["proof_rows_sha256"] == digest(proofs)
            and existing["failure_count_by_reason"]
            == map_counter(expected_failures)
            and existing["source_chart_domain"] == source,
            f"Round184 pure row independent reconstruction:{origin}",
        )
        if failures[TARGET_FAILURE]:
            target_keys.append(origin)
        if index % 100 == 0 or index == len(pure_keys):
            progress(
                f"Round201 pure tranche audit {index}/{len(pure_keys)}"
            )
    target_keys.sort()
    all_source_seam_keys.sort()
    require(
        len(target_keys) == EXPECTED_PURE_TARGET_ORIGIN_COUNT
        and digest(target_keys)
        == EXPECTED_PURE_TARGET_ORIGIN_KEYS_SHA256
        and len(all_source_seam_keys) == 18
        and digest(all_source_seam_keys)
        == "6fed61e3a02850e2a0cec911c35e6c71f2accb42eea1f62aa3a7acd6968a58b4",
        "pure target and source-seam cohorts",
    )

    per_origin_rows: list[dict[str, Any]] = []
    strict_credit_keys: list[str] = []
    target_seam_keys: list[str] = []
    exact_behind_rows: list[dict[str, Any]] = []
    exact_behind_keys: list[str] = []
    exact_behind_volume = Q(0)
    terminal_method_count: Counter[str] = Counter()
    terminal_count = 0
    terminal_volume = Q(0)
    split_face_count = 0

    for index, origin in enumerate(target_keys, 1):
        roots = registry["residual_by_origin"][origin]
        refinement = registry["refinements"][origin]
        root_volumes = {
            row.key: box_volume(row.box) for row in roots
        }
        inherited_terminals = [
            wrap_round180_terminal(origin, row, root_volumes)
            for row in refinement["terminal_rows"]
        ]
        require(
            all(
                row["whole_closed_cell_excluded"]
                for row in inherited_terminals
            ),
            f"pure inherited Round180 exclusions:{origin}",
        )
        terminal_rows = list(inherited_terminals)
        extra_split_faces: list[dict[str, Any]] = []
        depth2_exact_count = 0
        depth2_exact_volume = Q(0)
        depth2_residual_reasons: Counter[str] = Counter()

        for final_row in registry["final_rows"][origin]:
            proof, reason = clipped_partition_proof(final_row)
            if proof is not None:
                terminal_rows.append(wrap_clipped_terminal(
                    final_row,
                    proof,
                    "INDEPENDENT_ROUND184_CLIPPED_DELTA_THREE_STRATUM",
                ))
                continue
            require(
                reason == TARGET_FAILURE,
                f"pure target root reason:{origin}:{final_row.key}:{reason}",
            )
            pending = [(final_row, 0)]
            while pending:
                row, depth = pending.pop()
                direct_kind, direct_evidence = direct_strict_terminal(row)
                if direct_kind == "EXCLUDED":
                    require(
                        direct_evidence is not None,
                        f"pure direct evidence:{row.key}",
                    )
                    direct_row = {
                        "cell_key": row.key,
                        "origin_key": origin,
                        "method":
                            "DEPTH2_DIRECT_STRICT_CLOSED_BOX",
                        **box_evidence(row),
                        "coarse_disposition": "EXCLUDED",
                        "direct_evidence": direct_evidence,
                        "whole_closed_cell_excluded": True,
                    }
                    direct_row["row_sha256"] = digest(direct_row)
                    terminal_rows.append(direct_row)
                    continue
                if direct_kind is not None:
                    reason = f"DIRECT_STRICT_{direct_kind}"
                else:
                    child_proof, reason = clipped_partition_proof(row)
                    if child_proof is not None:
                        terminal_rows.append(wrap_clipped_terminal(
                            row,
                            child_proof,
                            "DEPTH2_CLIPPED_DELTA_THREE_STRATUM",
                        ))
                        continue
                if depth < 2:
                    axis = r180.split_axis(row.box)
                    lower, upper = r176.split(row.box, axis)
                    require(
                        box_volume(lower) + box_volume(upper)
                        == box_volume(row.box),
                        f"pure depth2 split volume:{row.key}",
                    )
                    extra_split_faces.append(
                        r180.split_face(row, axis, lower, upper)
                    )
                    pending.append(
                        (child_frontier(row, upper), depth + 1)
                    )
                    pending.append(
                        (child_frontier(row, lower), depth + 1)
                    )
                    continue
                require(
                    reason in {TARGET_FAILURE, FULL_P_FAILURE},
                    f"pure depth2 terminal reason:{row.key}:{reason}",
                )
                input_class = (
                    "TARGET_FIRST_CLIPPED"
                    if reason == TARGET_FAILURE
                    else "FULL_P_FIRST_ROOT_EQUALITY"
                )
                exact_row = single_exact_behind_cell(
                    row, input_class
                )
                require(
                    exact_row["whole_closed_cell_excluded"],
                    f"pure exact-behind terminal:{row.key}",
                )
                terminal_rows.append(exact_row)
                exact_behind_rows.append(exact_row)
                exact_behind_keys.append(row.key)
                row_volume = box_volume(row.box)
                exact_behind_volume += row_volume
                depth2_exact_count += 1
                depth2_exact_volume += row_volume
                depth2_residual_reasons[reason] += 1

        terminal_rows.sort(key=lambda row: row["cell_key"])
        require(
            len({row["cell_key"] for row in terminal_rows})
            == len(terminal_rows)
            and all(
                row["whole_closed_cell_excluded"]
                for row in terminal_rows
            ),
            f"pure terminal uniqueness and exclusion:{origin}",
        )
        origin_input_volume = sum(
            (box_volume(row.box) for row in roots), Q(0)
        )
        origin_terminal_volume = sum(
            (Q(row["exact_volume"]) for row in terminal_rows), Q(0)
        )
        require(
            origin_terminal_volume == origin_input_volume,
            f"pure exact terminal volume:{origin}",
        )
        combined_split_faces = sorted(
            refinement["split_face_rows"] + extra_split_faces,
            key=lambda row: row["parent_cell_key"],
        )
        lower_ledger = r180.lower_strata_ledger(
            combined_split_faces
        )
        source_meta = registry["replay"]["origins"][origin]
        source = r176.physical_domain(
            source_meta["chart_id"], source_meta["box"]
        )
        strict_source = source["classification"] == SOURCE_INTERIOR
        if strict_source:
            strict_credit_keys.append(origin)
        else:
            require(
                source["classification"] == SOURCE_SEAM,
                f"pure source class:{origin}",
            )
            target_seam_keys.append(origin)
        method_counts = Counter(
            row["method"] for row in terminal_rows
        )
        terminal_method_count.update(method_counts)
        terminal_count += len(terminal_rows)
        terminal_volume += origin_terminal_volume
        split_face_count += len(combined_split_faces)
        origin_row = {
            "origin_key": origin,
            "cohort": "PURE_TARGET_FIRST_DEPTH2",
            "priority_ordinal":
                registry["priority_by_origin"][origin][
                    "priority_ordinal"
                ],
            "original_parent_box":
                r176.box_row(source_meta["box"]),
            "source_chart_domain": source,
            "Round176_residual_root_count": len(roots),
            "Round176_preclosed_frontier_count":
                registry["base_closed_by_origin"][origin],
            "Round176_preclosed_kinds":
                sorted(registry["base_kinds"][origin]),
            "Round180_maximum_extra_depth": 4,
            "Round180_inherited_terminal_count":
                len(inherited_terminals),
            "new_depth2_exact_behind_terminal_count":
                depth2_exact_count,
            "new_depth2_exact_behind_exact_volume":
                str(depth2_exact_volume),
            "new_depth2_cutoff_reason_count":
                map_counter(depth2_residual_reasons),
            "complete_terminal_cell_count": len(terminal_rows),
            "complete_terminal_exact_volume":
                str(origin_terminal_volume),
            "terminal_count_by_method":
                map_counter(method_counts),
            "terminal_rows": terminal_rows,
            "terminal_rows_sha256": digest(terminal_rows),
            "split_face_rows": combined_split_faces,
            "split_face_rows_sha256":
                digest(combined_split_faces),
            "lower_dimensional_strata": lower_ledger,
            "target_geometry_complete": True,
            "physical_source_partition_complete": strict_source,
            "all_3D_2D_1D_0D_target_strata_excluded": True,
            "whole_original_physical_parent_excluded":
                strict_source,
            "whole_origin_integer_credit": 1 if strict_source else 0,
            "source_seam_integer_credit": 0,
            "child_count_or_volume_used_as_integer_credit": False,
            "guard_outside_used_as_exterior_credit": False,
        }
        origin_row["row_sha256"] = digest(origin_row)
        per_origin_rows.append(origin_row)
        if index % 20 == 0 or index == len(target_keys):
            progress(
                f"Round201 pure exact-behind origins "
                f"{index}/{len(target_keys)}"
            )

    per_origin_rows.sort(key=lambda row: row["priority_ordinal"])
    strict_credit_keys.sort()
    target_seam_keys.sort()
    exact_behind_keys.sort()
    exact_behind_rows.sort(key=lambda row: row["cell_key"])
    require(
        len(strict_credit_keys) == EXPECTED_PURE_STRICT_CREDIT_COUNT
        and digest(strict_credit_keys)
        == EXPECTED_PURE_STRICT_CREDIT_KEYS_SHA256
        and len(target_seam_keys) == EXPECTED_PURE_TARGET_SEAM_COUNT
        and digest(target_seam_keys)
        == EXPECTED_PURE_TARGET_SEAM_KEYS_SHA256
        and not set(strict_credit_keys) & set(target_seam_keys)
        and len(exact_behind_rows)
        == EXPECTED_PURE_DEPTH2_EXACT_BEHIND_CELL_COUNT
        and len(exact_behind_keys)
        == EXPECTED_PURE_DEPTH2_EXACT_BEHIND_CELL_COUNT
        and digest(exact_behind_keys)
        == EXPECTED_PURE_DEPTH2_EXACT_BEHIND_KEYS_SHA256
        and exact_behind_volume
        == EXPECTED_PURE_DEPTH2_EXACT_BEHIND_VOLUME,
        "pure formal cohort expected census",
    )
    return {
        "selection": {
            "selection_rule":
                "Round184 pure clipped origin with at least one "
                "independently rebuilt TARGET_NOT_STRICT_POSITIVE_FIRST cell",
            "selection_uses_Round201_outcome": False,
            "origin_count": len(target_keys),
            "origin_keys": target_keys,
            "origin_keys_sha256": digest(target_keys),
        },
        "exact_behind_depth2": {
            "cell_count": len(exact_behind_rows),
            "cell_keys_sha256": digest(exact_behind_keys),
            "exact_volume": str(exact_behind_volume),
            "per_cell_rows_sha256": digest(exact_behind_rows),
            "all_cells_strict_exact_behind_and_reduced_excluded":
                True,
        },
        "whole_origin_ledger": {
            "per_origin_rows": per_origin_rows,
            "per_origin_rows_sha256": digest(per_origin_rows),
            "terminal_cell_count": terminal_count,
            "terminal_exact_volume": str(terminal_volume),
            "terminal_count_by_method":
                map_counter(terminal_method_count),
            "split_face_count": split_face_count,
            "geometrically_complete_origin_count":
                len(per_origin_rows),
            "strict_physical_interior_credit_count":
                len(strict_credit_keys),
            "strict_physical_interior_credit_keys":
                strict_credit_keys,
            "strict_physical_interior_credit_keys_sha256":
                digest(strict_credit_keys),
            "source_seam_complete_but_held_count":
                len(target_seam_keys),
            "source_seam_complete_but_held_keys":
                target_seam_keys,
            "source_seam_complete_but_held_keys_sha256":
                digest(target_seam_keys),
            "source_seam_integer_credit": 0,
        },
        "all_pure_source_seam_keys": all_source_seam_keys,
        "all_pure_source_seam_keys_sha256":
            digest(all_source_seam_keys),
    }


def rebuild_generalized_cohort(
    registry: dict[str, Any],
) -> dict[str, Any]:
    selected_registry_rows = [
        row
        for row in registry["priority_rows"]
        if row["priority_class"]
        in {DELTA_MULTI_CLASS, COMPACT_CLASS}
    ]
    selected_keys = sorted(
        row["origin_key"] for row in selected_registry_rows
    )
    require(
        len(selected_registry_rows) == EXPECTED_GENERALIZED_ORIGIN_COUNT
        and digest(selected_keys)
        == EXPECTED_GENERALIZED_ORIGIN_KEYS_SHA256
        and Counter(
            row["priority_class"]
            for row in selected_registry_rows
        )
        == Counter(EXPECTED_GENERALIZED_CLASS_ORIGIN_COUNT),
        "generalized outcome-blind selection",
    )

    cell_rows: list[dict[str, Any]] = []
    per_origin_rows: list[dict[str, Any]] = []
    strict_credit_keys: list[str] = []
    complete_seam_keys: list[str] = []
    diagnostic_strict_residual_complete_keys: list[str] = []
    diagnostic_seam_residual_complete_keys: list[str] = []
    inherited_nonexcluded_complete_keys: list[str] = []
    inherited_nonexcluded_any_origin_keys: list[str] = []
    incomplete_mixed_inherited_nonexcluded_keys: list[str] = []
    inherited_nonexcluded_terminal_count = 0
    inherited_nonexcluded_terminal_count_by_coarse_disposition: (
        Counter[str]
    ) = Counter()
    inherited_nonexcluded_origin_count_by_priority_class: Counter[str] = (
        Counter()
    )
    incomplete_mixed_keys: list[str] = []
    compact_hold_keys: list[str] = []
    geometrically_complete_keys: list[str] = []
    whole_target_complete_keys: list[str] = []

    input_count: Counter[str] = Counter()
    input_volume: defaultdict[str, Q] = defaultdict(Q)
    category_count: Counter[str] = Counter()
    category_volume: defaultdict[str, Q] = defaultdict(Q)
    failure_count: Counter[str] = Counter()
    original_unresolved_cardinality: Counter[int] = Counter()
    eligible_cardinality: Counter[int] = Counter()
    deleted_cardinality: Counter[int] = Counter()
    remaining_unresolved_cardinality: Counter[int] = Counter()
    deleted_target_count: Counter[str] = Counter()
    failed_candidate_reason_count: Counter[str] = Counter()
    final_leaf_count: Counter[str] = Counter()
    final_disposition_count: Counter[str] = Counter()
    geometric_closed_count: Counter[str] = Counter()
    geometric_closed_volume: defaultdict[str, Q] = defaultdict(Q)
    geometric_residual_count: Counter[str] = Counter()
    geometric_residual_volume: defaultdict[str, Q] = defaultdict(Q)
    source_count: Counter[str] = Counter()
    origin_outcome_count: Counter[str] = Counter()
    terminal_method_count: Counter[str] = Counter()
    inherited_terminal_count = 0
    complete_partition_volume = Q(0)

    for index, registry_row in enumerate(selected_registry_rows, 1):
        origin = registry_row["origin_key"]
        priority_class = registry_row["priority_class"]
        final_rows = registry["final_rows"][origin]
        refinement = registry["refinements"][origin]
        roots = registry["residual_by_origin"][origin]
        source_meta = registry["replay"]["origins"][origin]
        source = r176.physical_domain(
            source_meta["chart_id"], source_meta["box"]
        )
        source_count[source["classification"]] += 1
        start_index = len(cell_rows)
        origin_closed_count = 0
        origin_closed_volume = Q(0)
        origin_final_volume = Q(0)
        origin_deleted = 0
        origin_residual_reasons: Counter[str] = Counter()

        for row in final_rows:
            category = r180.residual_category(row)
            evidence = generalized_exact_behind_cell(
                row, category, priority_class
            )
            row_volume = box_volume(row.box)
            cell_rows.append(evidence)
            input_count[priority_class] += 1
            input_volume[priority_class] += row_volume
            category_count[category] += 1
            category_volume[category] += row_volume
            failure_count[row.failure] += 1
            original_unresolved_cardinality[
                evidence["original_unresolved_candidate_count"]
            ] += 1
            eligible_cardinality[
                evidence["eligible_exact_behind_candidate_count"]
            ] += 1
            deleted_cardinality[
                len(evidence["deleted_candidate_targets"])
            ] += 1
            remaining_unresolved_cardinality[
                evidence["remaining_unresolved_candidate_count"]
            ] += 1
            deleted_target_count.update(
                evidence["deleted_candidate_targets"]
            )
            for candidate in evidence["candidate_evidence_rows"]:
                if not candidate["eligible_exact_behind"]:
                    if not candidate["ell_strict_negative"]:
                        failed_candidate_reason_count[
                            "ELL_NOT_STRICT_NEGATIVE"
                        ] += 1
                    if not candidate[
                        "distance_margin_strict_positive"
                    ]:
                        failed_candidate_reason_count[
                            "DISTANCE_MARGIN_NOT_STRICT_POSITIVE"
                        ] += 1
            final_leaf_count[
                evidence["final_leaf_classification"]
            ] += 1
            final_disposition_count[
                evidence["final_disposition"]
            ] += 1
            origin_deleted += len(
                evidence["deleted_candidate_targets"]
            )
            origin_final_volume += row_volume
            if evidence["geometric_whole_cell_excluded"]:
                origin_closed_count += 1
                origin_closed_volume += row_volume
                geometric_closed_count[priority_class] += 1
                geometric_closed_volume[priority_class] += row_volume
            else:
                reason = evidence["residual_reason"]
                origin_residual_reasons[reason] += 1
                geometric_residual_count[reason] += 1
                geometric_residual_volume[reason] += row_volume

        end_index = len(cell_rows)
        origin_cell_rows = cell_rows[start_index:end_index]
        require(
            len(origin_cell_rows) == len(final_rows)
            and digest([row["cell_key"] for row in origin_cell_rows])
            == digest([row.key for row in final_rows])
            and origin_final_volume
            == Q(registry_row["Round180_residual_child_volume"]),
            f"generalized final registry rows:{origin}",
        )
        all_geometric = origin_closed_count == len(final_rows)
        if all_geometric:
            geometrically_complete_keys.append(origin)

        root_volumes = {
            row.key: box_volume(row.box) for row in roots
        }
        inherited_terminals = [
            wrap_round180_terminal(origin, row, root_volumes)
            for row in refinement["terminal_rows"]
        ]
        inherited_nonexcluded = [
            row
            for row in inherited_terminals
            if not row["whole_closed_cell_excluded"]
        ]
        inherited_nonexcluded_terminal_count += len(
            inherited_nonexcluded
        )
        if inherited_nonexcluded:
            inherited_nonexcluded_any_origin_keys.append(origin)
            inherited_nonexcluded_origin_count_by_priority_class[
                priority_class
            ] += 1
            inherited_nonexcluded_terminal_count_by_coarse_disposition.update(
                row["coarse_disposition"]
                for row in inherited_nonexcluded
            )
        all_inherited_excluded = not inherited_nonexcluded
        whole_target_complete = all_geometric and all_inherited_excluded
        if whole_target_complete:
            whole_target_complete_keys.append(origin)
        if (
            all_geometric
            and priority_class == DELTA_MULTI_CLASS
            and source["classification"] == SOURCE_INTERIOR
        ):
            diagnostic_strict_residual_complete_keys.append(origin)
        if (
            all_geometric
            and priority_class == DELTA_MULTI_CLASS
            and source["classification"] == SOURCE_SEAM
        ):
            diagnostic_seam_residual_complete_keys.append(origin)

        strict_credit = (
            whole_target_complete
            and priority_class == DELTA_MULTI_CLASS
            and source["classification"] == SOURCE_INTERIOR
        )
        seam_hold = (
            whole_target_complete
            and priority_class == DELTA_MULTI_CLASS
            and source["classification"] == SOURCE_SEAM
        )
        inherited_hold = (
            all_geometric
            and priority_class == DELTA_MULTI_CLASS
            and not all_inherited_excluded
        )
        if strict_credit:
            strict_credit_keys.append(origin)
            origin_outcome = "STRICT_INTERIOR_WHOLE_ORIGIN_CREDIT"
        elif seam_hold:
            complete_seam_keys.append(origin)
            origin_outcome = "SOURCE_SEAM_COMPLETE_BUT_HELD"
        elif inherited_hold:
            inherited_nonexcluded_complete_keys.append(origin)
            origin_outcome = (
                "FINAL_RESIDUAL_COMPLETE_BUT_INHERITED_ROUND180_"
                "NONEXCLUDED"
            )
        elif priority_class == COMPACT_CLASS:
            compact_hold_keys.append(origin)
            origin_outcome = "COMPACT_Q_ORIGIN_HELD"
        else:
            require(
                priority_class == DELTA_MULTI_CLASS
                and not all_geometric,
                f"generalized residual classification:{origin}",
            )
            incomplete_mixed_keys.append(origin)
            if inherited_nonexcluded:
                incomplete_mixed_inherited_nonexcluded_keys.append(
                    origin
                )
            origin_outcome = "INCOMPLETE_MIXED_ORIGIN_RESIDUAL"
        origin_outcome_count[origin_outcome] += 1
        inherited_volume = sum(
            (Q(row["exact_volume"]) for row in inherited_terminals),
            Q(0),
        )
        origin_input_volume = sum(
            (box_volume(row.box) for row in roots), Q(0)
        )
        require(
            inherited_volume + origin_final_volume
            == origin_input_volume,
            f"generalized root partition volume:{origin}",
        )
        inherited_terminal_count += len(inherited_terminals)
        complete_partition_volume += origin_input_volume
        inherited_methods = Counter(
            row["method"] for row in inherited_terminals
        )
        terminal_method_count.update(inherited_methods)
        terminal_method_count[
            "ITERATIVE_EXACT_BEHIND_CANDIDATE_REMOVAL"
        ] += len(final_rows)
        lower_ledger = r180.lower_strata_ledger(
            refinement["split_face_rows"]
        )
        lower_ledger[
            "3D_closed_terminal_cells_are_primary_proof_objects"
        ] = whole_target_complete
        lower_ledger[
            "all_owned_2D_1D_0D_strata_inherit_a_closed_"
            "EXCLUDED_enclosure"
        ] = whole_target_complete
        origin_row = {
            "origin_key": origin,
            "cohort": "GENERALIZED_MIXED_AND_COMPACT_Q_SCAN",
            "priority_class": priority_class,
            "priority_ordinal": registry_row["priority_ordinal"],
            "original_parent_box":
                r176.box_row(source_meta["box"]),
            "source_chart_domain": source,
            "Round176_residual_root_count": len(roots),
            "Round176_preclosed_frontier_count":
                registry["base_closed_by_origin"][origin],
            "Round176_preclosed_kinds":
                sorted(registry["base_kinds"][origin]),
            "Round180_maximum_extra_depth": 4,
            "Round180_inherited_terminal_count":
                len(inherited_terminals),
            "Round180_inherited_terminal_rows":
                inherited_terminals,
            "Round180_inherited_terminal_rows_sha256":
                digest(inherited_terminals),
            "Round180_inherited_terminal_count_by_coarse_disposition":
                map_counter(Counter(
                    row["coarse_disposition"]
                    for row in inherited_terminals
                )),
            "Round180_inherited_nonexcluded_terminal_count":
                len(inherited_nonexcluded),
            "Round180_all_inherited_terminals_excluded":
                all_inherited_excluded,
            "Round180_final_cell_registry_index_half_open":
                [start_index, end_index],
            "Round180_final_cell_count": len(final_rows),
            "Round180_final_cell_exact_volume":
                str(origin_final_volume),
            "Round180_final_cell_rows_sha256":
                digest(origin_cell_rows),
            "exact_behind_deleted_candidate_count":
                origin_deleted,
            "geometrically_closed_final_cell_count":
                origin_closed_count,
            "geometrically_closed_final_cell_exact_volume":
                str(origin_closed_volume),
            "geometric_residual_reason_count":
                map_counter(origin_residual_reasons),
            "complete_residual_root_partition_exact_volume":
                str(origin_input_volume),
            "split_face_rows": refinement["split_face_rows"],
            "split_face_rows_sha256":
                digest(refinement["split_face_rows"]),
            "lower_dimensional_strata": lower_ledger,
            "all_final_cells_geometrically_excluded":
                all_geometric,
            "all_inherited_and_final_target_cells_excluded":
                whole_target_complete,
            "physical_source_partition_complete":
                source["classification"] == SOURCE_INTERIOR,
            "independent_source_stratum_complete":
                priority_class != COMPACT_CLASS,
            "origin_outcome": origin_outcome,
            "whole_original_physical_parent_excluded":
                strict_credit,
            "whole_origin_integer_credit": 1 if strict_credit else 0,
            "source_seam_integer_credit": 0,
            "compact_q_integer_credit": 0,
            "child_count_or_volume_used_as_integer_credit": False,
            "guard_outside_used_as_exterior_credit": False,
        }
        origin_row["row_sha256"] = digest(origin_row)
        per_origin_rows.append(origin_row)
        if index % 20 == 0 or index == len(selected_registry_rows):
            progress(
                f"Round201 generalized origins "
                f"{index}/{len(selected_registry_rows)}"
            )

    strict_credit_keys.sort()
    complete_seam_keys.sort()
    diagnostic_strict_residual_complete_keys.sort()
    diagnostic_seam_residual_complete_keys.sort()
    inherited_nonexcluded_complete_keys.sort()
    inherited_nonexcluded_any_origin_keys.sort()
    incomplete_mixed_inherited_nonexcluded_keys.sort()
    incomplete_mixed_keys.sort()
    compact_hold_keys.sort()
    geometrically_complete_keys.sort()
    whole_target_complete_keys.sort()
    per_origin_rows.sort(key=lambda row: row["priority_ordinal"])
    total_input_count = sum(input_count.values())
    total_input_volume = sum(input_volume.values(), Q(0))
    total_geometric_closed = sum(geometric_closed_count.values())
    total_geometric_closed_volume = sum(
        geometric_closed_volume.values(), Q(0)
    )
    total_geometric_residual = sum(geometric_residual_count.values())
    total_geometric_residual_volume = sum(
        geometric_residual_volume.values(), Q(0)
    )
    original_candidate_total = sum(
        cardinality * count
        for cardinality, count
        in original_unresolved_cardinality.items()
    )
    deleted_candidate_total = sum(
        cardinality * count
        for cardinality, count in deleted_cardinality.items()
    )
    remaining_candidate_total = sum(
        cardinality * count
        for cardinality, count
        in remaining_unresolved_cardinality.items()
    )
    require(
        total_input_count == EXPECTED_GENERALIZED_CELL_COUNT
        and len(cell_rows) == EXPECTED_GENERALIZED_CELL_COUNT
        and total_input_volume == EXPECTED_GENERALIZED_EXACT_VOLUME
        and total_geometric_closed + total_geometric_residual
        == total_input_count
        and total_geometric_closed_volume
        + total_geometric_residual_volume
        == total_input_volume
        and original_candidate_total
        == deleted_candidate_total + remaining_candidate_total
        and deleted_candidate_total
        == sum(deleted_target_count.values())
        and total_geometric_closed == 161648
        and geometric_closed_count
        == Counter({
            DELTA_MULTI_CLASS: 142866,
            COMPACT_CLASS: 18782,
        })
        and deleted_candidate_total == 233356
        and failed_candidate_reason_count
        == Counter({"ELL_NOT_STRICT_NEGATIVE": 22580})
        and final_disposition_count
        == Counter({
            "EXCLUDED_OUTGOING_CHART_MISMATCH": 18662,
            "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 142986,
            "LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH": 48,
            "UNRESOLVED": 21080,
        }),
        "generalized exact cell and candidate conservation",
    )
    require(
        len(diagnostic_strict_residual_complete_keys)
        == DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_COUNT
        and digest(diagnostic_strict_residual_complete_keys)
        == DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_KEYS_SHA256
        and len(diagnostic_seam_residual_complete_keys)
        == DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_SEAM_COUNT
        and digest(diagnostic_seam_residual_complete_keys)
        == DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_SEAM_KEYS_SHA256
        and len(strict_credit_keys)
        == EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_COUNT
        and digest(strict_credit_keys)
        == EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_KEYS_SHA256
        and len(complete_seam_keys)
        == EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_COUNT
        and digest(complete_seam_keys)
        == EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_KEYS_SHA256
        and not inherited_nonexcluded_complete_keys
        and digest(inherited_nonexcluded_complete_keys)
        == EXPECTED_EMPTY_KEYS_SHA256
        and not (
            set(diagnostic_strict_residual_complete_keys)
            - set(strict_credit_keys)
        )
        and not (
            set(diagnostic_seam_residual_complete_keys)
            - set(complete_seam_keys)
        )
        and len(incomplete_mixed_keys)
        == EXPECTED_GENERALIZED_INCOMPLETE_MIXED_COUNT
        and set(incomplete_mixed_inherited_nonexcluded_keys)
        <= set(incomplete_mixed_keys)
        and set(inherited_nonexcluded_any_origin_keys)
        >= set(incomplete_mixed_inherited_nonexcluded_keys)
        and len(compact_hold_keys) == 54
        and digest(compact_hold_keys)
        == (
            "d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b"
        )
        and len(geometrically_complete_keys) == 424
        and source_count
        == Counter({SOURCE_INTERIOR: 642, SOURCE_SEAM: 8}),
        "generalized whole-origin census",
    )
    return {
        "selection": {
            "selection_rule":
                "Round184 priority class in "
                "{DELTA_H_OR_MULTI_NO_Q,COMPACT_Q_PRESENT}",
            "selection_uses_Round201_outcome": False,
            "origin_count": len(selected_registry_rows),
            "origin_keys_sha256": digest(selected_keys),
            "origin_count_by_priority_class":
                EXPECTED_GENERALIZED_CLASS_ORIGIN_COUNT,
        },
        "full_final_cell_registry": {
            "per_cell_rows": cell_rows,
            "per_cell_rows_sha256": digest(cell_rows),
            "cell_count": total_input_count,
            "exact_volume": str(total_input_volume),
            "cell_count_by_priority_class":
                map_counter(input_count),
            "exact_volume_by_priority_class":
                fraction_map(input_volume),
            "residual_category_count":
                map_counter(category_count),
            "residual_category_exact_volume":
                fraction_map(category_volume),
            "original_failure_type_count":
                map_counter(failure_count),
            "original_unresolved_candidate_count_per_cell":
                map_counter(original_unresolved_cardinality),
            "eligible_exact_behind_candidate_count_per_cell":
                map_counter(eligible_cardinality),
            "deleted_candidate_count_per_cell":
                map_counter(deleted_cardinality),
            "remaining_unresolved_candidate_count_per_cell":
                map_counter(remaining_unresolved_cardinality),
            "original_unresolved_candidate_total":
                original_candidate_total,
            "deleted_candidate_total": deleted_candidate_total,
            "remaining_unresolved_candidate_total":
                remaining_candidate_total,
            "deleted_candidate_target_count":
                map_counter(deleted_target_count),
            "failed_candidate_reason_count":
                map_counter(failed_candidate_reason_count),
            "final_leaf_classification_count":
                map_counter(final_leaf_count),
            "final_disposition_count":
                map_counter(final_disposition_count),
            "geometrically_closed_cell_count_by_priority_class":
                map_counter(geometric_closed_count),
            "geometrically_closed_exact_volume_by_priority_class":
                fraction_map(geometric_closed_volume),
            "geometric_residual_reason_count":
                map_counter(geometric_residual_count),
            "geometric_residual_reason_exact_volume":
                fraction_map(geometric_residual_volume),
            "exact_count_and_volume_conservation": True,
        },
        "whole_origin_ledger": {
            "per_origin_rows": per_origin_rows,
            "per_origin_rows_sha256": digest(per_origin_rows),
            "Round180_inherited_terminal_count":
                inherited_terminal_count,
            "complete_residual_root_partition_exact_volume":
                str(complete_partition_volume),
            "terminal_count_by_method":
                map_counter(terminal_method_count),
            "origin_outcome_count":
                map_counter(origin_outcome_count),
            "final_residual_geometrically_complete_origin_count":
                len(geometrically_complete_keys),
            "final_residual_geometrically_complete_origin_keys":
                geometrically_complete_keys,
            "final_residual_geometrically_complete_origin_keys_sha256":
                digest(geometrically_complete_keys),
            "whole_target_partition_complete_origin_count":
                len(whole_target_complete_keys),
            "whole_target_partition_complete_origin_keys":
                whole_target_complete_keys,
            "whole_target_partition_complete_origin_keys_sha256":
                digest(whole_target_complete_keys),
            "diagnostic_final_residual_strict_interior_complete_count":
                len(diagnostic_strict_residual_complete_keys),
            "diagnostic_final_residual_strict_interior_complete_keys":
                diagnostic_strict_residual_complete_keys,
            "diagnostic_final_residual_strict_interior_complete_keys_sha256":
                digest(diagnostic_strict_residual_complete_keys),
            "strict_physical_interior_credit_count":
                len(strict_credit_keys),
            "strict_physical_interior_credit_keys":
                strict_credit_keys,
            "strict_physical_interior_credit_keys_sha256":
                digest(strict_credit_keys),
            "source_seam_complete_but_held_count":
                len(complete_seam_keys),
            "source_seam_complete_but_held_keys":
                complete_seam_keys,
            "source_seam_complete_but_held_keys_sha256":
                digest(complete_seam_keys),
            "diagnostic_final_residual_source_seam_complete_count":
                len(diagnostic_seam_residual_complete_keys),
            "diagnostic_final_residual_source_seam_complete_keys":
                diagnostic_seam_residual_complete_keys,
            "diagnostic_final_residual_source_seam_complete_keys_sha256":
                digest(diagnostic_seam_residual_complete_keys),
            "final_residual_complete_but_inherited_nonexcluded_count":
                len(inherited_nonexcluded_complete_keys),
            "final_residual_complete_but_inherited_nonexcluded_keys":
                inherited_nonexcluded_complete_keys,
            "final_residual_complete_but_inherited_nonexcluded_keys_sha256":
                digest(inherited_nonexcluded_complete_keys),
            "inherited_nonexcluded_terminal_count":
                inherited_nonexcluded_terminal_count,
            "inherited_nonexcluded_terminal_count_by_coarse_disposition":
                map_counter(
                    inherited_nonexcluded_terminal_count_by_coarse_disposition
                ),
            "inherited_nonexcluded_any_origin_count":
                len(inherited_nonexcluded_any_origin_keys),
            "inherited_nonexcluded_any_origin_keys":
                inherited_nonexcluded_any_origin_keys,
            "inherited_nonexcluded_any_origin_keys_sha256":
                digest(inherited_nonexcluded_any_origin_keys),
            "inherited_nonexcluded_origin_count_by_priority_class":
                map_counter(
                    inherited_nonexcluded_origin_count_by_priority_class
                ),
            "incomplete_mixed_with_inherited_nonexcluded_count":
                len(incomplete_mixed_inherited_nonexcluded_keys),
            "incomplete_mixed_with_inherited_nonexcluded_keys":
                incomplete_mixed_inherited_nonexcluded_keys,
            "incomplete_mixed_with_inherited_nonexcluded_keys_sha256":
                digest(incomplete_mixed_inherited_nonexcluded_keys),
            "incomplete_mixed_with_inherited_nonexcluded_is_overlapping_"
            "diagnostic_subgroup": True,
            "incomplete_mixed_origin_count":
                len(incomplete_mixed_keys),
            "incomplete_mixed_origin_keys":
                incomplete_mixed_keys,
            "incomplete_mixed_origin_keys_sha256":
                digest(incomplete_mixed_keys),
            "compact_q_origin_hold_count":
                len(compact_hold_keys),
            "compact_q_origin_hold_keys":
                compact_hold_keys,
            "compact_q_origin_hold_keys_sha256":
                digest(compact_hold_keys),
            "source_seam_integer_credit": 0,
            "compact_q_integer_credit": 0,
        },
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        (HERE / ROUND184_MANIFEST).resolve(),
        (HERE / ROUND180_VERIFIER).resolve(),
        (HERE / ROUND176_VERIFIER).resolve(),
        *((HERE / name).resolve() for name in ROUND184_PINS),
        *((HERE / name).resolve() for name in FUTURE_PROTECTED),
    }


def caller_authorized_output(path: Path) -> bool:
    return (
        path.name == OUTPUT.name
        or (
            path.name.startswith(".cm2_round201_")
            and path.name.endswith("_certificate.json")
        )
    )


def safe_atomic_write(
    path: Path,
    raw: bytes,
    protected: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent == HERE, "output directory")
    require(path.parent.resolve() == HERE, "output directory resolution")
    require(caller_authorized_output(path), "caller-authorized output")
    if path.exists() or path.is_symlink():
        status = path.lstat()
        require(stat.S_ISREG(status.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(status.st_nlink == 1, "output hardlink")
    require(path.resolve(strict=False) not in protected, "protected output")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(
            path.parent,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(
    name: str,
    operation: Callable[[], Any],
) -> str:
    try:
        operation()
    except Exception:
        return name
    raise RuntimeError(f"path attack accepted:{name}")


def path_attack_suite() -> dict[str, Any]:
    protected = protected_paths()
    require(
        OUTPUT.resolve() not in protected
        and Path(__file__).resolve() in protected,
        "protected path set",
    )
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(
        prefix=".round201-path.",
        dir=HERE,
    ))
    source = scratch / "source"
    source.write_bytes(b"fixture\n")
    symlink = (
        HERE / f".cm2_round201_symlink_{pid}_certificate.json"
    )
    hard_base = (
        HERE / f".cm2_round201_hardbase_{pid}_certificate.json"
    )
    hard_link = (
        HERE / f".cm2_round201_hardlink_{pid}_certificate.json"
    )
    fifo = HERE / f".cm2_round201_fifo_{pid}_certificate.json"
    outside = (
        HERE.parent / f".cm2_round201_escape_{pid}_certificate.json"
    )
    rejected: list[str] = []
    try:
        symlink.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink, b"x", protected),
        ))
        hard_base.write_bytes(b"fixture\n")
        os.link(hard_base, hard_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_link, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "parent directory escape",
            lambda: safe_atomic_write(outside, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "nested subdirectory output",
            lambda: safe_atomic_write(
                scratch
                / ".cm2_round201_nested_certificate.json",
                b"x",
                protected,
            ),
        ))
        rejected.append(expect_rejection(
            "existing directory output",
            lambda: safe_atomic_write(scratch, b"x", protected),
        ))
        os.mkfifo(fifo)
        rejected.append(expect_rejection(
            "FIFO output",
            lambda: safe_atomic_write(fifo, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "producer self",
            lambda: safe_atomic_write(Path(__file__), b"x", protected),
        ))
        rejected.append(expect_rejection(
            "Round184 manifest",
            lambda: safe_atomic_write(
                HERE / ROUND184_MANIFEST, b"x", protected
            ),
        ))
        rejected.append(expect_rejection(
            "future verifier",
            lambda: safe_atomic_write(
                HERE / FUTURE_PROTECTED[0], b"x", protected
            ),
        ))
    finally:
        for path in (
            symlink,
            hard_link,
            hard_base,
            fifo,
            outside,
        ):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    require(
        len(rejected) == 9 and len(set(rejected)) == 9,
        "path attack suite count",
    )
    return {
        "attack_count": 9,
        "rejected_count": 9,
        "all_rejected": True,
        "rejected_attack_names": rejected,
        "write_attempts_against_real_pins": 0,
    }


def assemble_accounted_payload(
    *,
    upstream: dict[str, Any],
    registry: dict[str, Any],
    pure: dict[str, Any],
    generalized: dict[str, Any],
) -> dict[str, Any]:
    """Join independently rebuilt phase products into the exact payload."""
    pure_credit = pure["whole_origin_ledger"][
        "strict_physical_interior_credit_keys"
    ]
    generalized_credit = generalized["whole_origin_ledger"][
        "strict_physical_interior_credit_keys"
    ]
    generalized_diagnostic_strict = generalized[
        "whole_origin_ledger"
    ][
        "diagnostic_final_residual_strict_interior_complete_keys"
    ]
    pure_seams = pure["whole_origin_ledger"][
        "source_seam_complete_but_held_keys"
    ]
    generalized_seams = generalized["whole_origin_ledger"][
        "source_seam_complete_but_held_keys"
    ]
    generalized_diagnostic_seams = generalized[
        "whole_origin_ledger"
    ]["diagnostic_final_residual_source_seam_complete_keys"]
    generalized_inherited_holds = generalized[
        "whole_origin_ledger"
    ][
        "final_residual_complete_but_inherited_nonexcluded_keys"
    ]
    generalized_incomplete_inherited_nonexcluded = generalized[
        "whole_origin_ledger"
    ]["incomplete_mixed_with_inherited_nonexcluded_keys"]
    require(
        not set(pure_credit) & set(generalized_credit)
        and not set(pure_seams) & set(generalized_seams),
        "cohort disjointness",
    )
    new_credit_keys = sorted(pure_credit + generalized_credit)
    diagnostic_residual_only_union = sorted(
        pure_credit + generalized_diagnostic_strict
    )
    complete_seam_keys = sorted(pure_seams + generalized_seams)
    diagnostic_complete_seam_keys = sorted(
        pure_seams + generalized_diagnostic_seams
    )
    generalized_strict_bad_keys = sorted(
        set(generalized_diagnostic_strict)
        - set(generalized_credit)
    )
    generalized_seam_bad_keys = sorted(
        set(generalized_diagnostic_seams)
        - set(generalized_seams)
    )
    require(
        len(pure_credit) == EXPECTED_PURE_STRICT_CREDIT_COUNT
        and digest(pure_credit)
        == EXPECTED_PURE_STRICT_CREDIT_KEYS_SHA256
        and len(generalized_credit)
        == EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_COUNT
        and digest(generalized_credit)
        == EXPECTED_GENERALIZED_FORMAL_STRICT_CREDIT_KEYS_SHA256
        and len(generalized_seams)
        == EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_COUNT
        and digest(generalized_seams)
        == EXPECTED_GENERALIZED_FORMAL_SEAM_HOLD_KEYS_SHA256
        and not generalized_inherited_holds
        and digest(generalized_inherited_holds)
        == EXPECTED_EMPTY_KEYS_SHA256
        and not generalized_strict_bad_keys
        and digest(generalized_strict_bad_keys)
        == EXPECTED_EMPTY_KEYS_SHA256
        and not generalized_seam_bad_keys
        and digest(generalized_seam_bad_keys)
        == EXPECTED_EMPTY_KEYS_SHA256
        and len(new_credit_keys)
        == EXPECTED_COMBINED_FORMAL_CREDIT_COUNT
        and digest(new_credit_keys)
        == EXPECTED_COMBINED_FORMAL_CREDIT_KEYS_SHA256
        and len(complete_seam_keys)
        == EXPECTED_COMBINED_FORMAL_SEAM_HOLD_COUNT
        and digest(complete_seam_keys)
        == EXPECTED_COMBINED_FORMAL_SEAM_HOLD_KEYS_SHA256
        and len(diagnostic_residual_only_union)
        == DIAGNOSTIC_RESIDUAL_ONLY_UNION_COUNT
        and digest(diagnostic_residual_only_union)
        == DIAGNOSTIC_RESIDUAL_ONLY_UNION_KEYS_SHA256
        and len(diagnostic_complete_seam_keys)
        == DIAGNOSTIC_COMBINED_FINAL_RESIDUAL_SEAM_COUNT
        and digest(diagnostic_complete_seam_keys)
        == DIAGNOSTIC_COMBINED_FINAL_RESIDUAL_SEAM_KEYS_SHA256
        and set(generalized_credit)
        <= set(
            generalized["whole_origin_ledger"][
                "diagnostic_final_residual_strict_interior_complete_keys"
            ]
        ),
        "combined conservative exact-behind cohort census",
    )

    result184 = upstream["certificate"]["result"]
    round184_closed_keys = result184[
        "pure_single_clipped_Delta_tranche"
    ]["closed_exact_origin_keys"]
    require(
        len(round184_closed_keys) == 620
        and digest(round184_closed_keys)
        == ROUND184_CLOSED_KEYS_SHA256
        and not set(round184_closed_keys) & set(new_credit_keys),
        "Round184 and Round201 credit disjointness",
    )
    priority_by_origin = registry["priority_by_origin"]
    remaining_keys = sorted(
        set(priority_by_origin)
        - set(round184_closed_keys)
        - set(new_credit_keys)
    )
    remaining_class_count = Counter(
        priority_by_origin[key]["priority_class"]
        for key in remaining_keys
    )
    generalized_incomplete = generalized["whole_origin_ledger"][
        "incomplete_mixed_origin_keys"
    ]
    compact_holds = generalized["whole_origin_ledger"][
        "compact_q_origin_hold_keys"
    ]
    pure_other_seams = sorted(
        set(pure["all_pure_source_seam_keys"]) - set(pure_seams)
    )
    require(
        len(pure_other_seams) == 12
        and set(pure_other_seams) <= set(remaining_keys)
        and all(
            r176.physical_domain(
                registry["replay"]["origins"][key]["chart_id"],
                registry["replay"]["origins"][key]["box"],
            )["classification"] == SOURCE_SEAM
            for key in pure_other_seams
        ),
        "other inherited pure source seams",
    )
    residual_group_sets = {
        "PURE_TARGET_SOURCE_SEAM_COMPLETE_BUT_HELD": set(pure_seams),
        "PURE_OTHER_SOURCE_SEAM_INHERITED_FROM_ROUND184":
            set(pure_other_seams),
        "GENERALIZED_SOURCE_SEAM_COMPLETE_BUT_HELD":
            set(generalized_seams),
        "GENERALIZED_FINAL_RESIDUAL_COMPLETE_BUT_INHERITED_"
        "ROUND180_NONEXCLUDED":
            set(generalized_inherited_holds),
        "GENERALIZED_INCOMPLETE_MIXED":
            set(generalized_incomplete),
        "COMPACT_Q_INDEPENDENT_SOURCE_STRATUM":
            set(compact_holds),
    }
    flattened_residual_groups = set().union(
        *residual_group_sets.values()
    )
    require(
        flattened_residual_groups == set(remaining_keys)
        and sum(len(values) for values in residual_group_sets.values())
        == len(flattened_residual_groups)
        and remaining_class_count
        == Counter({
            PURE_CLASS: 18,
            DELTA_MULTI_CLASS: 596 - len(generalized_credit),
            COMPACT_CLASS: 54,
        }),
        "remaining origin exact partition",
    )
    require(
        len(remaining_keys) == EXPECTED_REMAINING_ORIGIN_COUNT
        and set(generalized_incomplete_inherited_nonexcluded)
        <= set(generalized_incomplete),
        "remaining origin fixed census and diagnostic subgroup",
    )

    pure_origin_by_key = {
        row["origin_key"]: row
        for row in pure["whole_origin_ledger"]["per_origin_rows"]
    }
    generalized_origin_by_key = {
        row["origin_key"]: row
        for row in generalized["whole_origin_ledger"][
            "per_origin_rows"
        ]
    }
    integer_ledger_rows: list[dict[str, Any]] = []
    credited_partition_volume = Q(0)
    for origin in new_credit_keys:
        if origin in pure_origin_by_key:
            source_row = pure_origin_by_key[origin]
            cohort = "PURE_TARGET_FIRST_DEPTH2"
            volume = Q(source_row["complete_terminal_exact_volume"])
        else:
            source_row = generalized_origin_by_key[origin]
            cohort = "GENERALIZED_MIXED"
            volume = Q(
                source_row[
                    "complete_residual_root_partition_exact_volume"
                ]
            )
        require(
            source_row["whole_origin_integer_credit"] == 1
            and source_row[
                "whole_original_physical_parent_excluded"
            ],
            f"credited origin proof row:{origin}",
        )
        credited_partition_volume += volume
        ledger_row = {
            "origin_key": origin,
            "cohort": cohort,
            "source_origin_row_sha256": source_row["row_sha256"],
            "complete_residual_partition_exact_volume": str(volume),
            "whole_origin_integer_credit": 1,
            "child_count_or_volume_used_as_integer_credit": False,
        }
        ledger_row["row_sha256"] = digest(ledger_row)
        integer_ledger_rows.append(ledger_row)
    integer_ledger_rows.sort(key=lambda row: row["origin_key"])

    combined_excluded = 74012 + len(new_credit_keys)
    combined_live = 2820 - len(new_credit_keys)
    require(
        combined_excluded + combined_live == 76832
        and combined_excluded
        == EXPECTED_COMBINED_WHOLE_RECORD_EXCLUDED
        and combined_live == EXPECTED_COMBINED_CONSERVATIVE_LIVE
        and combined_live >= 0,
        "Round201 official ledger conservation",
    )
    path_attacks = path_attack_suite()
    result = {
        "status": (
            "PARTIAL__FORMAL_EXACT_BEHIND_CONSERVATIVE_WHOLE_ORIGIN_"
            "PROMOTION__D02_STILL_BLOCKED"
        ),
        "verdict": "PARTIAL",
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": r176.FROZEN_OWNER,
            "frozen_outgoing_chart": r176.FROZEN_CHART,
            "formal_base_round": 184,
            "Round184_priority_registry_origin_count": 1444,
            "pure_target_first_scan_origin_count":
                EXPECTED_PURE_TARGET_ORIGIN_COUNT,
            "generalized_mixed_and_compact_scan_origin_count":
                EXPECTED_GENERALIZED_ORIGIN_COUNT,
            "selection_fixed_before_Round201_outcomes": True,
            "diagnostic_probe_imported_or_executed": False,
        },
        "upstream_verified_chain": {
            "Round184_manifest_sha256":
                upstream["Round184_manifest_sha256"],
            "Round184_manifest_entries_replayed": True,
            "Round184_result_sha256": ROUND184_RESULT_SHA256,
            "Round184_verification_result_sha256":
                ROUND184_VERIFICATION_RESULT_SHA256,
            "Round184_full_expected_canonical_equality": True,
            "Round180_verifier_sha256": ROUND180_VERIFIER_SHA256,
            "Round176_verifier_sha256": ROUND176_VERIFIER_SHA256,
        },
        "independent_registry_reconstruction": {
            "ordering_rule": [
                "residual support class rank",
                "Round180 residual child count ascending",
                "exact origin key ascending",
            ],
            "row_count": len(registry["priority_rows"]),
            "rows": registry["priority_rows"],
            "rows_sha256": digest(registry["priority_rows"]),
            "full_canonical_equality_with_Round184_certificate": True,
            "selection_uses_Round201_outcome": False,
        },
        "pure_target_first_formal_refinement": pure,
        "generalized_exact_behind_formal_scan": generalized,
        "new_whole_origin_credit": {
            "pure_strict_physical_interior_count": len(pure_credit),
            "pure_strict_physical_interior_keys_sha256":
                digest(pure_credit),
            "generalized_strict_physical_interior_count":
                len(generalized_credit),
            "generalized_strict_physical_interior_keys_sha256":
                digest(generalized_credit),
            "R197_diagnostic_strict_residual_complete_count":
                DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_COUNT,
            "R197_diagnostic_strict_residual_complete_keys_sha256":
                DIAGNOSTIC_GENERALIZED_FINAL_RESIDUAL_STRICT_KEYS_SHA256,
            "R197_diagnostic_origins_rejected_for_inherited_"
            "Round180_nonexcluded_count":
                len(generalized_strict_bad_keys),
            "formal_generalized_strict_bad_count":
                len(generalized_strict_bad_keys),
            "formal_generalized_strict_bad_keys":
                generalized_strict_bad_keys,
            "formal_generalized_strict_bad_keys_sha256":
                digest(generalized_strict_bad_keys),
            "formal_generalized_seam_bad_count":
                len(generalized_seam_bad_keys),
            "formal_generalized_seam_bad_keys":
                generalized_seam_bad_keys,
            "formal_generalized_seam_bad_keys_sha256":
                digest(generalized_seam_bad_keys),
            "diagnostic_residual_only_union_count":
                len(diagnostic_residual_only_union),
            "diagnostic_residual_only_union_keys_sha256":
                digest(diagnostic_residual_only_union),
            "diagnostic_residual_only_union_not_used_as_official_credit":
                True,
            "cohort_intersection_count":
                len(set(pure_credit) & set(generalized_credit)),
            "combined_count": len(new_credit_keys),
            "combined_exact_origin_keys": new_credit_keys,
            "combined_exact_origin_keys_sha256":
                digest(new_credit_keys),
            "integer_ledger_rows": integer_ledger_rows,
            "integer_ledger_rows_sha256":
                digest(integer_ledger_rows),
            "complete_residual_partition_exact_volume":
                str(credited_partition_volume),
            "all_credited_sources_strict_physical_interiors": True,
            "all_credited_target_partitions_3D_2D_1D_0D_complete":
                True,
            "child_count_or_volume_used_as_integer_credit": False,
        },
        "strict_residual_origin_partition": {
            "remaining_origin_count": len(remaining_keys),
            "remaining_exact_origin_keys": remaining_keys,
            "remaining_exact_origin_keys_sha256":
                digest(remaining_keys),
            "remaining_count_by_priority_class":
                map_counter(remaining_class_count),
            "group_count": {
                key: len(values)
                for key, values in sorted(residual_group_sets.items())
            },
            "group_exact_origin_keys": {
                key: sorted(values)
                for key, values in sorted(residual_group_sets.items())
            },
            "group_exact_origin_keys_sha256": {
                key: digest(sorted(values))
                for key, values in sorted(residual_group_sets.items())
            },
            "overlapping_diagnostic_subgroups": {
                "GENERALIZED_INCOMPLETE_MIXED_WITH_INHERITED_"
                "ROUND180_NONEXCLUDED": {
                    "origin_count":
                        len(
                            generalized_incomplete_inherited_nonexcluded
                        ),
                    "exact_origin_keys":
                        generalized_incomplete_inherited_nonexcluded,
                    "exact_origin_keys_sha256":
                        digest(
                            generalized_incomplete_inherited_nonexcluded
                        ),
                    "not_an_additional_partition_group": True,
                    "integer_credit": 0,
                },
            },
            "complete_exact_behind_source_seam_count":
                len(complete_seam_keys),
            "complete_exact_behind_source_seam_keys":
                complete_seam_keys,
            "complete_exact_behind_source_seam_keys_sha256":
                digest(complete_seam_keys),
            "diagnostic_final_residual_complete_source_seam_count":
                len(diagnostic_complete_seam_keys),
            "diagnostic_final_residual_complete_source_seam_keys":
                diagnostic_complete_seam_keys,
            "diagnostic_final_residual_complete_source_seam_keys_sha256":
                digest(diagnostic_complete_seam_keys),
            "source_seam_integer_credit": 0,
            "compact_q_integer_credit": 0,
            "incomplete_mixed_integer_credit": 0,
            "exact_partition_of_all_remaining_Round184_candidates":
                True,
        },
        "ledger_composition": {
            "base_round": 184,
            "base_whole_record_excluded": 74012,
            "base_conservative_live": 2820,
            "Round201_new_whole_parent_excluded":
                len(new_credit_keys),
            "combined_whole_record_excluded": combined_excluded,
            "combined_conservative_live": combined_live,
            "refined_source_W_record_count": 76832,
            "conservation_identity":
                f"{combined_excluded}+{combined_live}=76832",
            "remaining_whole_exclusion_upper_candidates":
                len(remaining_keys),
            "analytic_internal_strata_added_to_integer_record_count":
                False,
            "child_count_or_volume_added_to_integer_record_count":
                False,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_whole_exclusion_upper_candidates":
                len(remaining_keys),
            "remaining_conservative_live": combined_live,
            "source_seam_whole_origin_credit": 0,
            "compact_q_whole_origin_credit": 0,
            "incomplete_mixed_whole_origin_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "independently verify all Round201 per-cell and whole-origin "
            "rows; then attack/cold-replay before any downstream use"
        ),
        "producer_output_safety": {
            "official_certificate_may_be_replaced": OUTPUT.name,
            "cold_replay_rule":
                "hidden .cm2_round201_*_certificate.json in HERE only",
            "other_same_directory_outputs_authorized": False,
            "same_directory_atomic_replace": True,
            "file_fsync_before_replace": True,
            "parent_directory_fsync_after_replace": True,
            "path_attack_suite": path_attacks,
        },
        "provenance": {
            "producer": PRODUCER.name,
            "producer_sha256": PRODUCER_SHA256,
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "imports_only_frozen_Round180_verifier_geometry": True,
            "Round194_probe_imported_or_used_as_math": False,
            "Round197_probe_imported_or_used_as_math": False,
            "older_round_files_modified": False,
        },
    }
    return result


def reconstruct_expected_payload() -> dict[str, Any]:
    """Verifier orchestration; the certificate is not an input to this path."""
    forbidden = (
        "cm2_round187_",
        "cm2_round190_",
        "cm2_round193_",
        "cm2_round194_",
        "cm2_round197_",
        "cm2_round201_source_w_exact_behind_formal_promotion",
    )
    loaded_forbidden = sorted(
        name
        for name in sys.modules
        if name.startswith(forbidden) and name != Path(__file__).stem
    )
    require(not loaded_forbidden, "diagnostic/producer module boundary")
    frozen = check_upstream()
    reconstructed_registry = reconstruct_registry(frozen)
    # These scans are disjoint and neither consumes the other one's outcome.
    generalized_scan = rebuild_generalized_cohort(reconstructed_registry)
    pure_scan = rebuild_pure_target_cohort(
        frozen, reconstructed_registry
    )
    return assemble_accounted_payload(
        upstream=frozen,
        registry=reconstructed_registry,
        pure=pure_scan,
        generalized=generalized_scan,
    )


def sha256_regular_large(
    path: Path,
    *,
    expected_size: int | None = None,
) -> tuple[str, int]:
    """Hash a same-directory regular file without following aliases."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"large input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"large input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(stat.S_ISREG(status.st_mode), f"large input regular:{absolute.name}")
    require(not absolute.is_symlink(), f"large input symlink:{absolute.name}")
    require(status.st_nlink == 1, f"large input hardlink:{absolute.name}")
    require(status.st_size > 0, f"large input empty:{absolute.name}")
    if expected_size is not None:
        require(
            status.st_size == expected_size,
            f"large input size:{absolute.name}",
        )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    value = hashlib.sha256()
    total = 0
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino),
            f"large input race:{absolute.name}",
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"large opened input type:{absolute.name}",
        )
        while True:
            chunk = os.read(descriptor, 8 * 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            value.update(chunk)
        require(total == opened.st_size, f"large short input:{absolute.name}")
    finally:
        os.close(descriptor)
    return value.hexdigest(), total


def strict_load_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"encoding:{label}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate:{label}:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    require(type(value) is dict, f"top object:{label}")
    reject_surrogates(value, label)
    return value


def strict_load_large_certificate(path: Path) -> dict[str, Any]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, "certificate parent")
    require(absolute.parent.resolve() == HERE, "certificate parent resolution")
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and status.st_size == CERTIFICATE_SIZE,
        "certificate lstat contract",
    )
    # The certificate is intentionally read only after the independent
    # expected result has been reconstructed, avoiding any use as an oracle.
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino)
            and stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == CERTIFICATE_SIZE,
            "certificate opened identity",
        )
        chunks: list[bytes] = []
        value = hashlib.sha256()
        remaining = CERTIFICATE_SIZE
        while remaining:
            chunk = os.read(descriptor, min(8 * 1024 * 1024, remaining))
            require(bool(chunk), "certificate short read")
            chunks.append(chunk)
            value.update(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), "certificate grew during read")
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    require(
        len(raw) == CERTIFICATE_SIZE
        and value.hexdigest() == CERTIFICATE_SHA256,
        "certificate byte count and file pin",
    )
    return strict_load_bytes(raw, path.name)


def static_inert_boundary_audit() -> dict[str, Any]:
    import ast

    producer_raw = read_regular(PRODUCER)
    require(
        hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    producer_tree = ast.parse(
        producer_raw.decode("utf-8", "strict"), filename=PRODUCER.name
    )
    verifier_raw = read_regular(Path(__file__))
    verifier_tree = ast.parse(
        verifier_raw.decode("utf-8", "strict"), filename=Path(__file__).name
    )
    forbidden_prefixes = (
        "cm2_round187_",
        "cm2_round190_",
        "cm2_round193_",
        "cm2_round194_",
        "cm2_round197_",
        "cm2_round201_source_w_exact_behind_formal_promotion",
    )

    def imported_names(tree: ast.AST) -> list[str]:
        names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.append(node.module or "")
        return sorted(names)

    verifier_imports = imported_names(verifier_tree)
    require(
        not any(
            name.startswith(forbidden_prefixes) for name in verifier_imports
        ),
        "verifier forbidden import",
    )
    producer_imports = imported_names(producer_tree)
    require(
        not any(
            name.startswith((
                "cm2_round187_",
                "cm2_round190_",
                "cm2_round193_",
                "cm2_round194_",
                "cm2_round197_",
            ))
            for name in producer_imports
        ),
        "producer diagnostic import",
    )
    require(
        not any(
            name.startswith(forbidden_prefixes)
            for name in sys.modules
            if name != Path(__file__).stem
        ),
        "forbidden module already loaded",
    )
    def function_bodies(tree: ast.Module) -> dict[str, str]:
        rows: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = ast.Module(body=node.body, type_ignores=[])
                rows[node.name] = hashlib.sha256(
                    ast.dump(
                        body,
                        annotate_fields=True,
                        include_attributes=False,
                    ).encode("utf-8")
                ).hexdigest()
        return rows

    producer_bodies = function_bodies(producer_tree)
    verifier_bodies = function_bodies(verifier_tree)
    reverse_producer: defaultdict[str, list[str]] = defaultdict(list)
    reverse_verifier: defaultdict[str, list[str]] = defaultdict(list)
    for name, value in producer_bodies.items():
        reverse_producer[value].append(name)
    for name, value in verifier_bodies.items():
        reverse_verifier[value].append(name)
    common_bodies = sorted(set(reverse_producer) & set(reverse_verifier))
    exact_pairs = sorted(
        {
            (producer_name, verifier_name)
            for value in common_bodies
            for producer_name in reverse_producer[value]
            for verifier_name in reverse_verifier[value]
        }
    )
    require(
        ("build_result", "reconstruct_expected_payload") not in exact_pairs
        and ("build_result", "assemble_accounted_payload") not in exact_pairs
        and ("main", "main") not in exact_pairs,
        "producer build/main body overlap",
    )
    return {
        "producer_treated_as_inert_regular_bytes": True,
        "producer_imported_or_executed": False,
        "producer_sha256": PRODUCER_SHA256,
        "producer_ast_parse": "PASS",
        "verifier_ast_parse": "PASS",
        "verifier_forbidden_import_count": 0,
        "diagnostic_probe_imported_or_executed": False,
        "producer_top_level_function_count": len(producer_bodies),
        "verifier_top_level_function_count": len(verifier_bodies),
        "exact_AST_body_overlap_pair_count": len(exact_pairs),
        "exact_AST_body_overlap_pairs": [
            {
                "producer_function": producer_name,
                "verifier_function": verifier_name,
            }
            for producer_name, verifier_name in exact_pairs
        ],
        "producer_build_result_body_reused": False,
        "producer_main_body_reused": False,
        "shared_lower_level_algorithm_risk_quantified": True,
    }


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> Any:
    cursor = root
    for item in path[:-1]:
        cursor = cursor[item]
    old = cursor[path[-1]]
    cursor[path[-1]] = value
    return old


def semantic_attack_suite(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    """Genuinely re-sign bounded in-place mutations; never deepcopy 1.1 GB."""
    result = certificate["result"]
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        (
            "whole credit count",
            ("new_whole_origin_credit", "combined_count"),
            547,
        ),
        (
            "whole credit ledger row",
            (
                "new_whole_origin_credit",
                "integer_ledger_rows",
                0,
                "whole_origin_integer_credit",
            ),
            0,
        ),
        (
            "inherited exclusion flag",
            (
                "generalized_exact_behind_formal_scan",
                "whole_origin_ledger",
                "per_origin_rows",
                0,
                "Round180_all_inherited_terminals_excluded",
            ),
            False,
        ),
        (
            "generalized cell disposition",
            (
                "generalized_exact_behind_formal_scan",
                "full_final_cell_registry",
                "per_cell_rows",
                0,
                "coarse_disposition",
            ),
            "LIVE",
        ),
        (
            "source seam integer credit",
            ("strict_residual_origin_partition", "source_seam_integer_credit"),
            1,
        ),
        (
            "residual partition count",
            ("strict_residual_origin_partition", "remaining_origin_count"),
            277,
        ),
        (
            "official excluded ledger",
            ("ledger_composition", "combined_whole_record_excluded"),
            74559,
        ),
        (
            "D02 promotion",
            ("strict_nonpromotion", "D02"),
            "OPEN",
        ),
        (
            "D03 authorization",
            ("strict_nonpromotion", "D03_negative_oracle"),
            "AUTHORIZED",
        ),
        (
            "Gate5 promotion",
            ("strict_nonpromotion", "global_Gate5_fields"),
            "18/18",
        ),
        (
            "complete block promotion",
            ("strict_nonpromotion", "global_complete_18_field_blocks"),
            1,
        ),
        (
            "CM2 claim promotion",
            ("strict_nonpromotion", "CM2"),
            "GO_FOR_CLAIM",
        ),
        (
            "child integer credit",
            (
                "new_whole_origin_credit",
                "child_count_or_volume_used_as_integer_credit",
            ),
            True,
        ),
    ]
    rejected: list[str] = []
    original_document_hash = certificate["result_sha256"]
    for name, path, replacement in attacks:
        old = set_path(result, path, replacement)
        if old == replacement:
            if type(old) is bool:
                replacement = not old
            elif type(old) is int:
                replacement = old + 1
            elif type(old) is str:
                replacement = old + "__MUTATED"
            else:
                raise RuntimeError(f"attack replacement collision:{name}")
            set_path(result, path, replacement)
        try:
            resigned = digest(result)
            certificate["result_sha256"] = resigned
            require(
                resigned != EXPECTED_RESULT_SHA256,
                f"attack digest changed:{name}",
            )
            require(result != expected, f"attack equality rejected:{name}")
            rejected.append(name)
        finally:
            set_path(result, path, old)
            certificate["result_sha256"] = original_document_hash
    require(
        result == expected
        and certificate["result_sha256"] == EXPECTED_RESULT_SHA256,
        "semantic attack restoration",
    )
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "attack_names": rejected,
        "mutation_strategy": (
            "in-place mutate/re-sign/compare/restore; no giant deepcopy"
        ),
        "every_attack_result_digest_recomputed": True,
    }


def expect_json_rejection(name: str, raw: bytes) -> str:
    try:
        strict_load_bytes(raw, f"attack:{name}")
    except Exception:
        return name
    raise RuntimeError(f"JSON attack accepted:{name}")


def json_attack_suite() -> dict[str, Any]:
    attacks = [
        ("duplicate key", b'{"a":1,"a":2}'),
        ("float", b'{"a":1.0}'),
        ("NaN", b'{"a":NaN}'),
        ("Infinity", b'{"a":Infinity}'),
        ("negative Infinity", b'{"a":-Infinity}'),
        ("BOM", b'\xef\xbb\xbf{"a":1}'),
        ("NUL", b'{"a":"x\\u0000"}\x00'),
        ("invalid UTF-8", b'{"a":"\xff"}'),
        ("surrogate value", b'{"a":"\\ud800"}'),
        ("surrogate key", b'{"\\udfff":1}'),
        ("trailing JSON", b'{"a":1}{}'),
        ("top array", b'[]'),
        ("empty", b''),
    ]
    rejected = [
        expect_json_rejection(name, raw) for name, raw in attacks
    ]
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "attack_names": rejected,
    }


def verifier_authorized_output(path: Path) -> bool:
    return (
        path.name == VERIFICATION_OUTPUT.name
        or (
            path.name.startswith(".cm2_round201_")
            and path.name.endswith("_verification.json")
        )
    )


def verifier_protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        (HERE / ROUND184_MANIFEST).resolve(),
        (HERE / ROUND180_VERIFIER).resolve(),
        (HERE / ROUND176_VERIFIER).resolve(),
        *((HERE / name).resolve() for name in ROUND184_PINS),
        *(
            (HERE / name).resolve()
            for name in FUTURE_PROTECTED
            if name != VERIFICATION_OUTPUT.name
        ),
    }


def verifier_safe_atomic_write(path: Path, raw: bytes) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent == HERE, "verifier output directory")
    require(
        path.parent.resolve() == HERE,
        "verifier output directory resolution",
    )
    require(verifier_authorized_output(path), "verifier output allowlist")
    if path.exists() or path.is_symlink():
        status = path.lstat()
        require(stat.S_ISREG(status.st_mode), "verifier output regular")
        require(not path.is_symlink(), "verifier output symlink")
        require(status.st_nlink == 1, "verifier output hardlink")
    require(
        path.resolve(strict=False) not in verifier_protected_paths(),
        "verifier protected output",
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(
            HERE,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def verifier_path_attack_suite() -> dict[str, Any]:
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(
        prefix=".round201-verifier-path.", dir=HERE
    ))
    source = scratch / "source"
    source.write_bytes(b"fixture\n")
    symlink = HERE / f".cm2_round201_{pid}_symlink_verification.json"
    hard_base = HERE / f".cm2_round201_{pid}_base_verification.json"
    hard_link = HERE / f".cm2_round201_{pid}_hard_verification.json"
    fifo = HERE / f".cm2_round201_{pid}_fifo_verification.json"
    outside = HERE.parent / f".cm2_round201_{pid}_escape_verification.json"
    parent_alias = HERE / f".round201-parent-alias-{pid}"
    rejected: list[str] = []

    def reject(name: str, operation: Callable[[], Any]) -> None:
        rejected.append(expect_rejection(name, operation))

    try:
        symlink.symlink_to(source)
        reject("symlink output", lambda: verifier_safe_atomic_write(symlink, b"x"))
        hard_base.write_bytes(b"fixture\n")
        os.link(hard_base, hard_link)
        reject("hardlink output", lambda: verifier_safe_atomic_write(hard_link, b"x"))
        os.mkfifo(fifo)
        reject("FIFO output", lambda: verifier_safe_atomic_write(fifo, b"x"))
        reject("parent escape", lambda: verifier_safe_atomic_write(outside, b"x"))
        reject(
            "nested output",
            lambda: verifier_safe_atomic_write(
                scratch / ".cm2_round201_nested_verification.json", b"x"
            ),
        )
        parent_alias.symlink_to(HERE, target_is_directory=True)
        reject(
            "symlink parent alias",
            lambda: verifier_safe_atomic_write(
                parent_alias / ".cm2_round201_alias_verification.json", b"x"
            ),
        )
        reject(
            "unallowlisted same-directory output",
            lambda: verifier_safe_atomic_write(
                HERE / "cm2_round201_unlisted_verification.json", b"x"
            ),
        )
        reject(
            "producer protected",
            lambda: verifier_safe_atomic_write(PRODUCER, b"x"),
        )
        reject(
            "certificate protected",
            lambda: verifier_safe_atomic_write(CERTIFICATE, b"x"),
        )
        reject(
            "verifier protected",
            lambda: verifier_safe_atomic_write(Path(__file__), b"x"),
        )
        reject(
            "Round184 manifest protected",
            lambda: verifier_safe_atomic_write(HERE / ROUND184_MANIFEST, b"x"),
        )
        reject(
            "Round180 verifier protected",
            lambda: verifier_safe_atomic_write(HERE / ROUND180_VERIFIER, b"x"),
        )
        reject(
            "Round176 verifier protected",
            lambda: verifier_safe_atomic_write(HERE / ROUND176_VERIFIER, b"x"),
        )
        reject(
            "Round184 certificate protected",
            lambda: verifier_safe_atomic_write(
                HERE / ROUND184_CERTIFICATE, b"x"
            ),
        )
        reject(
            "existing directory",
            lambda: verifier_safe_atomic_write(scratch, b"x"),
        )
        reject(
            "wrong hidden suffix",
            lambda: verifier_safe_atomic_write(
                HERE / f".cm2_round201_{pid}_verification.txt", b"x"
            ),
        )
        reject(
            "certificate-shaped hidden name",
            lambda: verifier_safe_atomic_write(
                HERE / f".cm2_round201_{pid}_certificate.json", b"x"
            ),
        )
    finally:
        for path in (
            symlink,
            hard_link,
            hard_base,
            fifo,
            outside,
            parent_alias,
        ):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    require(len(rejected) == 17, "verifier path attack count")
    return {
        "attack_count": 17,
        "rejected_count": 17,
        "all_rejected": True,
        "attack_names": rejected,
        "real_protected_files_modified": False,
        "file_fsync_before_replace": True,
        "parent_directory_fsync_after_replace": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=VERIFICATION_OUTPUT
    )
    arguments = parser.parse_args()
    ctx.prec = 192
    boundary = static_inert_boundary_audit()
    expected = reconstruct_expected_payload()
    require(
        digest(expected) == EXPECTED_RESULT_SHA256,
        "independent expected result digest",
    )
    certificate = strict_load_large_certificate(CERTIFICATE)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == SCHEMA
        and certificate["result_sha256"] == EXPECTED_RESULT_SHA256
        and digest(certificate["result"]) == EXPECTED_RESULT_SHA256,
        "certificate envelope and result digest",
    )
    require(
        certificate["result"] == expected,
        "full expected Python-object equality",
    )
    canonical_pretty = pretty_bytes(certificate)
    require(
        len(canonical_pretty) == CERTIFICATE_SIZE
        and hashlib.sha256(canonical_pretty).hexdigest()
        == CERTIFICATE_SHA256,
        "full expected canonical pretty-JSON equality",
    )
    del canonical_pretty
    semantic_attacks = semantic_attack_suite(certificate, expected)
    json_attacks = json_attack_suite()
    path_attacks = verifier_path_attack_suite()
    verification_result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND201",
        "verdict": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_file_sha256": CERTIFICATE_SHA256,
        "certificate_size_bytes": CERTIFICATE_SIZE,
        "certificate_result_sha256": EXPECTED_RESULT_SHA256,
        "reconstructed_result_sha256": digest(expected),
        "full_expected_python_object_equality": True,
        "full_expected_canonical_equality": True,
        "verified_census": {
            "pure_exact_behind_cells": 37262,
            "generalized_exact_behind_cells": 182776,
            "new_whole_origin_credit": 546,
            "combined_whole_record_excluded": 74558,
            "combined_conservative_live": 2274,
            "remaining_priority_origins": 278,
            "formal_generalized_strict_bad": 0,
            "formal_generalized_seam_bad": 0,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "independence_contract": {
            **boundary,
            "imports_only_pre_and_post_pinned_Round180_verifier_geometry":
                True,
            "Round184_manifest_and_six_entries_replayed": True,
            "certificate_loaded_only_after_expected_result_rebuilt": True,
            "full_expected_canonical_equality": True,
            "implementation_diverse_second_derivation_claimed": False,
            "shared_algorithm_error_risk_disclosed": True,
        },
        "semantic_attack_suite": semantic_attacks,
        "strict_JSON_attack_suite": json_attacks,
        "path_and_output_attack_suite": path_attacks,
        "output_safety": {
            "strict_allowlist": True,
            "symlink_parent_alias_rejected": True,
            "file_fsync_before_replace": True,
            "parent_directory_fsync_after_replace": True,
        },
    }
    document = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification_result,
        "result_sha256": digest(verification_result),
    }
    verifier_safe_atomic_write(arguments.output, pretty_bytes(document))
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
