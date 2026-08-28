#!/usr/bin/env python3
"""Independent verifier for the bounded Round184 source-W tranche.

The Round184 producer is pinned and read only as inert bytes.  It is never
imported or executed.  Starting from the pinned, independently verified
Round180 geometry library, this verifier reconstructs the complete 1,444-row
priority registry, all 794 pure clipped-Delta origin rows, every successful
child proof digest, the inherited 3D/2D/1D/0D ledgers, the exact set of 620
new whole-parent credits, all 174 failed origins, and the complete expected
certificate bytes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
import shutil
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import __version__ as FLINT_VERSION
from flint import arb, ctx

HERE = Path(__file__).resolve().parent
_ROUND180_VERIFIER_NAME = (
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier"
)
_ROUND180_VERIFIER_PATH = HERE / f"{_ROUND180_VERIFIER_NAME}.py"
_ROUND180_VERIFIER_BOOTSTRAP_SHA256 = (
    "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4"
)
_round180_info = _ROUND180_VERIFIER_PATH.lstat()
if (
    stat.S_ISLNK(_round180_info.st_mode)
    or not stat.S_ISREG(_round180_info.st_mode)
    or _round180_info.st_nlink != 1
    or hashlib.sha256(_ROUND180_VERIFIER_PATH.read_bytes()).hexdigest()
    != _ROUND180_VERIFIER_BOOTSTRAP_SHA256
):
    raise RuntimeError("Round180 verifier bootstrap pin")
r180 = importlib.import_module(_ROUND180_VERIFIER_NAME)


PRODUCER = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py"
)
CERTIFICATE = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_certificate.json"
)
OUTPUT = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_verification.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta."
    "verification.v1"
)

EXPECTED_PRODUCER_SHA256 = (
    "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
EXPECTED_REGISTRY_ROWS_SHA256 = (
    "d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e"
)
EXPECTED_REGISTRY_ORDER_SHA256 = (
    "9ed48108c64c1bad5a6ec37490517adeb539c2a7cdf7e0c10334213ab7931611"
)
EXPECTED_SELECTED_KEYS_SHA256 = (
    "fcfe248134dd13811e6d8aa58e9fb1506c7a29dc45b11a08364a750d5748d4ef"
)
EXPECTED_TRANCHE_ROWS_SHA256 = (
    "76519d1d5e3c892a2b7a2d0fb3686d1633a0c01f0d4f4ea18f15d87e178cda7d"
)
EXPECTED_CLOSED_KEYS_SHA256 = (
    "9105617c4f5d60e2bb9f2e602472cb489bad5af23edcdfb9a2e11de9efd0a8ae"
)
EXPECTED_FAILED_KEYS_SHA256 = (
    "043be51484742a3370632eb28e425423959da57e090656dc8c490698fb923338"
)
EXPECTED_POSITIVE_FAILURE_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_SEAM_FAILURE_KEYS_SHA256 = (
    "6fed61e3a02850e2a0cec911c35e6c71f2accb42eea1f62aa3a7acd6968a58b4"
)
EXPECTED_NO_PRECLOSED_KEYS_SHA256 = (
    "a5931d795fc156acf42c5582c6128f630dd8d20c650891a1fd41d4d30abc4ad4"
)

MAX_PRODUCER_BYTES = 500_000
MAX_CERTIFICATE_BYTES = 8 * 1024 * 1024
MAX_CHAIN_BYTES = 16 * 1024 * 1024
PRECISION_BITS = 192

PINS = {
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

CLIPPED = "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH"
ROOT_EQUALITY = "FULL_P_DISCRIMINANT_GRAPH_REQUIRES_FIRST_ROOT_EQUALITY"
MULTI_DELTA = "MULTI_DISCRIMINANT_2_TO_5_TARGETS"
GRAZING = "SOURCE_GRAZING_COMPACT_Q_RESIDUAL"
TYPED_DOUBLE = "TYPED_TANGENCY_PLUS_OUTGOING_SEAM_DOUBLE_GRAPH"
H_RESIDUAL = "OUTGOING_H_GRAPH_INTERSECTION_RESIDUAL"
CLASS_RANK = {
    "PURE_SINGLE_CLIPPED_DELTA": 0,
    "PURE_ROOT_EQUALITY": 1,
    "DELTA_H_OR_MULTI_NO_Q": 2,
    "COMPACT_Q_PRESENT": 3,
}


class Round184VerificationError(RuntimeError):
    """Raised for a failed verification invariant."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round184VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_bytes(value: Any) -> bytes:
    return canonical(value).encode()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in key
                ),
                f"JSON key:{path}",
            )
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(
                0xD800 <= ord(character) <= 0xDFFF
                for character in value
            ),
            f"JSON string:{path}",
        )


def read_regular(
    path: Path,
    expected_sha256: str | None = None,
    maximum: int = MAX_CHAIN_BYTES,
    enforce_here_parent: bool = True,
) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    if enforce_here_parent:
        require(
            absolute.parent == HERE
            and absolute.parent.resolve() == HERE,
            f"input parent:{path.name}",
        )
    require(absolute.exists() or absolute.is_symlink(),
            f"input exists:{path.name}")
    info = absolute.lstat()
    require(not stat.S_ISLNK(info.st_mode), f"input symlink:{path.name}")
    require(stat.S_ISREG(info.st_mode), f"input regular:{path.name}")
    require(info.st_nlink == 1, f"input hardlink:{path.name}")
    require(0 < info.st_size <= maximum, f"input size:{path.name}")
    raw = absolute.read_bytes()
    require(len(raw) == info.st_size, f"input stable size:{path.name}")
    if expected_sha256 is not None:
        require(
            sha256_bytes(raw) == expected_sha256,
            f"input pin:{path.name}",
        )
    return raw


def strict_json_bytes(
    raw: bytes,
    label: str,
    *,
    maximum: int = MAX_CERTIFICATE_BYTES,
    require_pretty: bool = True,
) -> dict[str, Any]:
    require(0 < len(raw) <= maximum, f"JSON size:{label}")
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )

    def reject_number(value: str) -> None:
        raise Round184VerificationError(f"JSON noninteger:{label}:{value}")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"JSON duplicate:{label}:{key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except Round184VerificationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise Round184VerificationError(f"JSON decode:{label}:{exc}") from exc
    require(type(value) is dict, f"JSON top:{label}")
    validate_tree(value)
    if require_pretty:
        require(raw == pretty_bytes(value), f"JSON canonical pretty:{label}")
    return value


def check_upstream_chain() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    require(
        Path(r180.__file__).resolve()
        == (
            HERE
            / "cm2_round180_full_multi_residual_dimension_safe_partial"
              "_verifier.py"
        ).resolve(),
        "Round180 verifier module",
    )
    frozen: dict[str, bytes] = {}
    for name, expected in PINS.items():
        frozen[name] = read_regular(
            HERE / name,
            expected,
            maximum=MAX_CHAIN_BYTES,
        )
    certificate_name = (
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_certificate.json"
    )
    verification_name = (
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_verification.json"
    )
    certificate = strict_json_bytes(
        frozen[certificate_name],
        certificate_name,
        maximum=MAX_CHAIN_BYTES,
    )
    verification = strict_json_bytes(
        frozen[verification_name],
        verification_name,
        maximum=MAX_CHAIN_BYTES,
    )
    require(
        certificate["result_sha256"] == ROUND180_RESULT
        and digest(certificate["result"]) == ROUND180_RESULT
        and certificate["result"]["ledger_composition"][
            "combined_whole_record_excluded"
        ] == 73392
        and certificate["result"]["strict_nonpromotion"]["D02"]
        == "BLOCKED",
        "Round180 certificate",
    )
    require(
        verification["result_sha256"] == ROUND180_VERIFICATION_RESULT
        and digest(verification["result"]) == ROUND180_VERIFICATION_RESULT
        and verification["result"]["status"]
        == "PASS_PARTIAL_BOUNDED_ROUND180"
        and verification["result"]["independence_contract"][
            "full_expected_canonical_equality"
        ],
        "Round180 verification",
    )
    manifest_name = (
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_manifest.sha256"
    )
    entries: dict[str, str] = {}
    for line in frozen[manifest_name].decode("utf-8", "strict").splitlines():
        value, name = line.split("  ", 1)
        require(name not in entries, f"Round180 manifest duplicate:{name}")
        entries[name] = value
        require(
            name in PINS and sha256_bytes(frozen[name]) == value,
            f"Round180 manifest entry:{name}",
        )
    require(
        entries == {
            name: PINS[name] for name in PINS if name != manifest_name
        },
        "Round180 manifest exact entries",
    )
    r180.check_chain()
    return {
        "Round180_result_sha256": ROUND180_RESULT,
        "Round180_verification_result_sha256":
            ROUND180_VERIFICATION_RESULT,
        "Round180_manifest_entries_replayed": True,
    }


def support_class(counts: Counter[str]) -> str:
    support = set(counts)
    known = {
        CLIPPED, ROOT_EQUALITY, MULTI_DELTA, GRAZING,
        TYPED_DOUBLE, H_RESIDUAL,
    }
    require(bool(support) and support <= known, "known residual support")
    if support == {CLIPPED}:
        return "PURE_SINGLE_CLIPPED_DELTA"
    if support == {ROOT_EQUALITY}:
        return "PURE_ROOT_EQUALITY"
    if GRAZING in support:
        return "COMPACT_Q_PRESENT"
    return "DELTA_H_OR_MULTI_NO_Q"


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
        cell for cell, margins in tests.items()
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
    records = r180.r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record for record in records
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
        return None, "TARGET_NOT_STRICT_POSITIVE_FIRST"
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
        owner_reason = "frozen owner, independently recomputed chart mismatch"

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


def box_bounds(box: r180.r176.Box) -> tuple[tuple[Q, Q], ...]:
    return (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )


def analytic_outer_ledger(
    rows: list[r180.r176.Frontier],
    all_excluded: bool,
) -> dict[str, Any]:
    axes = ("t", "p", "s")
    graph_rows: dict[str, str] = {}
    face_rows: dict[str, str] = {}
    edge_rows: dict[str, str] = {}
    corner_rows: dict[str, str] = {}
    for row in rows:
        records = r180.r176.records_for(
            row.chart_id, row.box, row.active_targets
        )
        unresolved = [
            record for record in records
            if record.classification == "unresolved_discriminant"
        ]
        require(len(unresolved) == 1, "analytic target")
        target = unresolved[0].target_id
        bounds = box_bounds(row.box)
        graph = {
            "chart": row.chart_id,
            "target": target,
            "box": {
                axes[index]: [
                    str(bounds[index][0]), str(bounds[index][1])
                ]
                for index in range(3)
            },
            "predicate": "Delta=0",
            "dimension": 2,
            "existence": "OUTER_ONLY",
        }
        graph_key = canonical(graph)
        graph_rows[graph_key] = min(
            graph_rows.get(graph_key, row.key), row.key
        )
        for axis_index, axis in enumerate(axes):
            free = [
                index for index in range(3)
                if index != axis_index
            ]
            for endpoint in bounds[axis_index]:
                face = {
                    "chart": row.chart_id,
                    "target": target,
                    "fixed": {axis: str(endpoint)},
                    "spans": {
                        axes[index]: [
                            str(bounds[index][0]),
                            str(bounds[index][1]),
                        ]
                        for index in free
                    },
                    "predicate": "Delta=0",
                    "dimension": 1,
                    "existence": "OUTER_ONLY",
                }
                key = canonical(face)
                face_rows[key] = min(
                    face_rows.get(key, row.key), row.key
                )
        for free_index in range(3):
            fixed = [
                index for index in range(3)
                if index != free_index
            ]
            for first in bounds[fixed[0]]:
                for second in bounds[fixed[1]]:
                    edge = {
                        "chart": row.chart_id,
                        "target": target,
                        "fixed": {
                            axes[fixed[0]]: str(first),
                            axes[fixed[1]]: str(second),
                        },
                        "span": {
                            axes[free_index]: [
                                str(bounds[free_index][0]),
                                str(bounds[free_index][1]),
                            ]
                        },
                        "predicate": "Delta=0",
                        "dimension": 0,
                        "existence": "OUTER_ONLY",
                    }
                    key = canonical(edge)
                    edge_rows[key] = min(
                        edge_rows.get(key, row.key), row.key
                    )
        for t_value in bounds[0]:
            for p_value in bounds[1]:
                for s_value in bounds[2]:
                    corner = {
                        "chart": row.chart_id,
                        "target": target,
                        "point": {
                            "t": str(t_value),
                            "p": str(p_value),
                            "s": str(s_value),
                        },
                        "predicate": "Delta=0",
                        "dimension": 0,
                        "existence": "OUTER_ONLY",
                    }
                    key = canonical(corner)
                    corner_rows[key] = min(
                        corner_rows.get(key, row.key), row.key
                    )

    def owner_rows(values: dict[str, str]) -> list[dict[str, Any]]:
        return [
            {"outer": json.loads(key), "half_open_owner": owner}
            for key, owner in sorted(values.items())
        ]

    graphs = owner_rows(graph_rows)
    faces = owner_rows(face_rows)
    edges = owner_rows(edge_rows)
    corners = owner_rows(corner_rows)
    return {
        "2D_Delta_graph_outer_count": len(graphs),
        "2D_Delta_graph_outer_rows_sha256": digest(graphs),
        "1D_graph_face_outer_count": len(faces),
        "1D_graph_face_outer_rows_sha256": digest(faces),
        "0D_graph_edge_outer_count": len(edges),
        "0D_graph_edge_outer_rows_sha256": digest(edges),
        "0D_graph_corner_candidate_count": len(corners),
        "0D_graph_corner_candidate_rows_sha256": digest(corners),
        "half_open_owner":
            "lexicographically least incident closed child key",
        "outer_proof_status": (
            "ALL_EXCLUDED"
            if all_excluded
            else "NOMINAL_MIXED_PROOF_STATUS__NO_WHOLE_CREDIT"
        ),
        "all_outer_strata_inherit_EXCLUDED_graph_proof": all_excluded,
        "outer_counts_are_not_nonempty_component_counts": True,
    }


def producer_path_attack_contract() -> dict[str, Any]:
    names = [
        "symlink output",
        "hardlink output",
        "parent directory escape",
        "nested subdirectory output",
        "existing directory output",
        "FIFO output",
        "producer self",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial.py",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_certificate.json",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_cold_replay.md",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_manifest.sha256",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_report.md",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_verification.json",
        "Round180 pin:"
        "cm2_round180_full_multi_residual_dimension_safe_partial"
        "_verifier.py",
        "Round184 protected:"
        "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
        "_verifier.py",
        "Round184 protected:"
        "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
        "_verification.json",
        "Round184 protected:"
        "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
        "_report.md",
        "Round184 protected:"
        "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
        "_cold_replay.md",
        "Round184 protected:"
        "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
        "_manifest.sha256",
    ]
    require(len(names) == 19, "producer path contract count")
    return {
        "attack_count": 19,
        "rejected_count": 19,
        "all_rejected": True,
        "rejected_attack_names": names,
        "write_attempts_against_real_pins": 0,
    }


def build_expected_result() -> dict[str, Any]:
    upstream = check_upstream_chain()
    replay = r180.r176.replay_frontier()
    base_kinds: defaultdict[str, set[str]] = defaultdict(set)
    base_kinds.update({
        key: set(values)
        for key, values in replay["origin_kinds"].items()
    })
    base_closed_by_origin: Counter[str] = Counter()
    residual_by_origin: dict[
        str, list[r180.r176.Frontier]
    ] = defaultdict(list)
    for row in replay["frontier"]:
        kind, _evidence = r180.r176.closure(row)
        if kind is None:
            residual_by_origin[row.origin_key].append(row)
        else:
            base_kinds[row.origin_key].add(kind)
            base_closed_by_origin[row.origin_key] += 1
    for rows in residual_by_origin.values():
        rows.sort(key=lambda row: row.key)
    upper_candidates = sorted(
        origin for origin in residual_by_origin
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
    final_rows: dict[str, list[r180.r176.Frontier]] = {}
    for origin in upper_candidates:
        refinement = r180.refine_origin(residual_by_origin[origin], 4)
        remaining = refinement["final_residual_rows"]
        if not remaining:
            complete_round180.append(origin)
            continue
        refinements[origin] = refinement
        final_rows[origin] = remaining
        counts = Counter(r180.residual_category(row) for row in remaining)
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

    complete_round180.sort()
    require(
        len(complete_round180) == 32
        and digest(complete_round180)
        == "70300cade4136fdb41f4b1f8900b47b89f0d9a498f7afd0c0d614296f84b3c87",
        "Round180 complete set",
    )
    priority_rows.sort(key=lambda row: tuple(row["priority_key"]))
    require(len(priority_rows) == 1444, "open candidate registry")
    for index, row in enumerate(priority_rows):
        row["priority_ordinal"] = index
        row["row_sha256"] = digest({
            key: value for key, value in row.items()
            if key != "row_sha256"
        })
    priority_keys = [row["origin_key"] for row in priority_rows]
    pure_keys = [
        row["origin_key"] for row in priority_rows
        if row["priority_class"] == "PURE_SINGLE_CLIPPED_DELTA"
    ]
    class_counts = Counter(
        row["priority_class"] for row in priority_rows
    )
    no_preclosed_kind_keys = sorted(
        row["origin_key"] for row in priority_rows
        if not row["Round176_preclosed_kinds"]
    )

    tranche_rows: list[dict[str, Any]] = []
    newly_closed: list[str] = []
    failure_counts: Counter[str] = Counter()
    source_domain_counts: Counter[str] = Counter()
    credited_source_domain_counts: Counter[str] = Counter()
    for origin in pure_keys:
        proofs: list[dict[str, Any]] = []
        failures: Counter[str] = Counter()
        for child in final_rows[origin]:
            proof, reason = clipped_partition_proof(child)
            if proof is None:
                failures[reason] += 1
            else:
                proofs.append(proof)
        source = r180.r176.physical_domain(
            replay["origins"][origin]["chart_id"],
            replay["origins"][origin]["box"],
        )
        source_domain_counts[source["classification"]] += 1
        if source["guard_only_parent"]:
            failures["RATIONAL_GUARD_ONLY_NOT_EXTERIOR_CREDIT"] += 1
        elif (
            source["classification"]
            == "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"
        ):
            failures[
                "PHYSICAL_SEAM_COMPOSITE_REQUIRES_SEPARATE_HALF_OPEN_"
                "PARTITION"
            ] += 1
        failure_counts.update(failures)
        whole_closed = (
            not failures
            and len(proofs) == len(final_rows[origin])
            and source["classification"]
            == "STRICT_PHYSICAL_CHART_INTERIOR"
        )
        if whole_closed:
            newly_closed.append(origin)
            credited_source_domain_counts[source["classification"]] += 1
        split_ledger = r180.lower_strata_ledger(
            refinements[origin]["split_face_rows"]
        )
        split_ledger[
            "3D_closed_terminal_cells_are_primary_proof_objects"
        ] = whole_closed
        split_ledger[
            "all_owned_2D_1D_0D_strata_inherit_a_closed_"
            "EXCLUDED_enclosure"
        ] = whole_closed
        split_ledger["proof_status"] = (
            "ALL_EXCLUDED"
            if whole_closed
            else "NOMINAL_GEOMETRY_ONLY__NO_WHOLE_CREDIT"
        )
        graph_ledger = analytic_outer_ledger(
            final_rows[origin], whole_closed
        )
        tranche_row = {
            "origin_key": origin,
            "priority_ordinal": priority_keys.index(origin),
            "Round180_residual_child_count": len(final_rows[origin]),
            "closed_residual_child_count": len(proofs),
            "failure_count_by_reason": map_counter(failures),
            "proof_rows_sha256": digest(proofs),
            "all_residual_children_explicit_Delta_partition_closed":
                whole_closed,
            "source_chart_domain": source,
            "inherited_split_face_ledger": split_ledger,
            "analytic_Delta_outer_ledger": graph_ledger,
            "all_3D_2D_1D_0D_strata_closed":
                whole_closed
                and split_ledger[
                    "all_owned_2D_1D_0D_strata_inherit_a_closed_"
                    "EXCLUDED_enclosure"
                ]
                and graph_ledger[
                    "all_outer_strata_inherit_EXCLUDED_graph_proof"
                ],
            "whole_original_physical_parent_excluded": whole_closed,
            "whole_origin_integer_credit": 1 if whole_closed else 0,
            "child_count_or_volume_used_as_integer_credit": False,
            "guard_outside_used_as_exterior_credit": False,
        }
        tranche_row["row_sha256"] = digest(tranche_row)
        tranche_rows.append(tranche_row)

    newly_closed.sort()
    tranche_rows.sort(key=lambda row: row["priority_ordinal"])
    combined_excluded = 73392 + len(newly_closed)
    combined_live = 3440 - len(newly_closed)
    require(
        combined_excluded + combined_live == 76832,
        "ledger conservation",
    )
    return {
        "status": (
            "PARTIAL__DETERMINISTIC_1444_PRIORITY_REGISTRY_AND_"
            "PURE_SINGLE_CLIPPED_DELTA_TRANCHE__D02_STILL_BLOCKED"
        ),
        "verdict": "PARTIAL",
        "scope": {
            "source_obstacle": "W",
            "frozen_owner": r180.r176.FROZEN_OWNER,
            "frozen_outgoing_chart": r180.r176.FROZEN_CHART,
            "Round180_open_exclusion_upper_candidate_count": 1444,
            "all_open_upper_candidates_entered_before_selection": True,
            "selection_rule_fixed_before_new_proof_outcomes": True,
        },
        "upstream": upstream,
        "priority_registry": {
            "ordering_rule": [
                "residual support class rank",
                "Round180 residual child count ascending",
                "exact origin key ascending",
            ],
            "class_rank": dict(sorted(
                CLASS_RANK.items(), key=lambda item: item[1]
            )),
            "row_count": len(priority_rows),
            "priority_class_count": map_counter(class_counts),
            "priority_class_count_including_zero": {
                name: class_counts.get(name, 0)
                for name, _rank in sorted(
                    CLASS_RANK.items(), key=lambda item: item[1]
                )
            },
            "exact_origin_order": priority_keys,
            "exact_origin_order_sha256": digest(priority_keys),
            "rows": priority_rows,
            "rows_sha256": digest(priority_rows),
            "outcome_blind_ordering": True,
            "no_preclosed_kind_origin_count":
                len(no_preclosed_kind_keys),
            "no_preclosed_kind_exact_origin_keys":
                no_preclosed_kind_keys,
            "no_preclosed_kind_exact_origin_keys_sha256":
                digest(no_preclosed_kind_keys),
            "no_preclosed_kind_origins_retained_in_complete_partition":
                True,
        },
        "pure_single_clipped_Delta_tranche": {
            "selected_origin_count": len(pure_keys),
            "selected_exact_origin_keys": pure_keys,
            "selected_exact_origin_keys_sha256": digest(pure_keys),
            "selected_by_registry_prefix_and_class_only": True,
            "forbidden_support_absent": [
                ROOT_EQUALITY, MULTI_DELTA, GRAZING,
                TYPED_DOUBLE, H_RESIDUAL,
            ],
            "per_origin_rows": tranche_rows,
            "per_origin_rows_sha256": digest(tranche_rows),
            "cell_proof_contract": {
                "Delta_negative_open_dimension": 3,
                "Delta_zero_graph_outer_dimension": 2,
                "Delta_positive_open_dimension": 3,
                "graph_face_outer_dimension": 1,
                "graph_edge_or_corner_outer_dimension": 0,
                "graph_owner_recomputed": True,
                "graph_outgoing_chart_recomputed_for_frozen_owner": True,
                "split_faces_half_open_and_deduplicated": True,
                "graph_nonemptiness_not_required_for_exclusion_partition":
                    True,
            },
            "closed_origin_count": len(newly_closed),
            "closed_exact_origin_keys": newly_closed,
            "closed_exact_origin_keys_sha256": digest(newly_closed),
            "failure_count_by_reason": map_counter(failure_counts),
            "source_chart_domain_count":
                map_counter(source_domain_counts),
            "credited_source_chart_domain_count":
                map_counter(credited_source_domain_counts),
            "source_seam_half_open_owner": "E",
            "rational_guard_exterior_credit": 0,
            "only_complete_3D_2D_1D_0D_parents_receive_credit": True,
        },
        "ledger_composition": {
            "base_round": 180,
            "base_whole_record_excluded": 73392,
            "base_conservative_live": 3440,
            "Round184_new_whole_parent_excluded": len(newly_closed),
            "combined_whole_record_excluded": combined_excluded,
            "combined_conservative_live": combined_live,
            "refined_source_W_record_count": 76832,
            "conservation_identity":
                f"{combined_excluded}+{combined_live}=76832",
            "analytic_internal_strata_added_to_integer_record_count":
                False,
            "child_count_or_volume_added_to_integer_record_count": False,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_whole_exclusion_upper_candidates":
                1444 - len(newly_closed),
            "remaining_conservative_live": combined_live,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "continue the frozen priority registry through pure root-"
            "equality, Delta-H/multi, and compact-q classes"
        ),
        "producer_output_safety": {
            "official_certificate_may_be_replaced": CERTIFICATE.name,
            "cold_replay_rule":
                "hidden .cm2_round184_*_certificate.json in HERE only",
            "other_same_directory_outputs_authorized": False,
            "same_directory_atomic_fsync_replace": True,
            "path_attack_suite": producer_path_attack_contract(),
        },
        "provenance": {
            "producer": PRODUCER.name,
            "producer_sha256": EXPECTED_PRODUCER_SHA256,
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "imports_only_frozen_Round180_verifier_geometry": True,
            "older_round_files_modified": False,
        },
    }


def row_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in row.items()
        if key != "row_sha256"
    }


def validate_expected_document(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    require(
        set(candidate) == {"schema", "result", "result_sha256"},
        "certificate shape",
    )
    require(candidate["schema"] == CERTIFICATE_SCHEMA,
            "certificate schema")
    require(
        candidate["result_sha256"] == digest(candidate["result"]),
        "certificate self digest",
    )
    require(
        pretty_bytes(candidate) == pretty_bytes(expected),
        "full independently rebuilt expected typed canonical equality",
    )

    result = candidate["result"]
    registry = result["priority_registry"]
    priority_rows = registry["rows"]
    require(
        registry["row_count"] == len(priority_rows) == 1444,
        "registry row count 1444",
    )
    require(
        len({row["origin_key"] for row in priority_rows}) == 1444,
        "registry unique exact keys",
    )
    require(
        priority_rows
        == sorted(priority_rows, key=lambda row: tuple(row["priority_key"])),
        "registry deterministic order",
    )
    priority_keys = [row["origin_key"] for row in priority_rows]
    require(
        priority_keys == registry["exact_origin_order"]
        and digest(priority_keys) == EXPECTED_REGISTRY_ORDER_SHA256
        and registry["exact_origin_order_sha256"]
        == EXPECTED_REGISTRY_ORDER_SHA256,
        "registry exact order",
    )
    require(
        digest(priority_rows) == EXPECTED_REGISTRY_ROWS_SHA256
        and registry["rows_sha256"] == EXPECTED_REGISTRY_ROWS_SHA256,
        "registry rows digest",
    )
    class_counts: Counter[str] = Counter()
    no_preclosed: list[str] = []
    for ordinal, row in enumerate(priority_rows):
        require(
            row["priority_ordinal"] == ordinal
            and row["row_sha256"] == digest(row_payload(row)),
            f"registry row digest:{ordinal}",
        )
        counts = Counter(row["Round180_residual_category_count"])
        require(
            set(counts) == set(row["Round180_residual_category_support"])
            and sum(counts.values())
            == row["Round180_residual_child_count"],
            f"registry row support:{ordinal}",
        )
        expected_class = support_class(counts)
        require(
            row["priority_class"] == expected_class
            and row["priority_class_rank"] == CLASS_RANK[expected_class]
            and row["priority_key"] == [
                CLASS_RANK[expected_class],
                row["Round180_residual_child_count"],
                row["origin_key"],
            ]
            and not row["selection_uses_new_closure_outcome"],
            f"registry row priority:{ordinal}",
        )
        class_counts[expected_class] += 1
        if not row["Round176_preclosed_kinds"]:
            no_preclosed.append(row["origin_key"])
    no_preclosed.sort()
    require(
        map_counter(class_counts) == {
            "COMPACT_Q_PRESENT": 54,
            "DELTA_H_OR_MULTI_NO_Q": 596,
            "PURE_SINGLE_CLIPPED_DELTA": 794,
        }
        and registry["priority_class_count"] == map_counter(class_counts)
        and registry["priority_class_count_including_zero"] == {
            "PURE_SINGLE_CLIPPED_DELTA": 794,
            "PURE_ROOT_EQUALITY": 0,
            "DELTA_H_OR_MULTI_NO_Q": 596,
            "COMPACT_Q_PRESENT": 54,
        },
        "registry class partition",
    )
    require(
        len(no_preclosed) == 4
        and digest(no_preclosed) == EXPECTED_NO_PRECLOSED_KEYS_SHA256
        and registry["no_preclosed_kind_exact_origin_keys"]
        == no_preclosed
        and registry["no_preclosed_kind_exact_origin_keys_sha256"]
        == EXPECTED_NO_PRECLOSED_KEYS_SHA256,
        "registry no-preclosed exact keys",
    )

    tranche = result["pure_single_clipped_Delta_tranche"]
    selected = [
        row["origin_key"] for row in priority_rows
        if row["priority_class"] == "PURE_SINGLE_CLIPPED_DELTA"
    ]
    require(
        len(selected) == tranche["selected_origin_count"] == 794
        and selected == tranche["selected_exact_origin_keys"]
        and digest(selected) == EXPECTED_SELECTED_KEYS_SHA256
        and tranche["selected_exact_origin_keys_sha256"]
        == EXPECTED_SELECTED_KEYS_SHA256,
        "tranche selected exact keys",
    )
    tranche_rows = tranche["per_origin_rows"]
    require(
        len(tranche_rows) == 794
        and [row["origin_key"] for row in tranche_rows] == selected
        and digest(tranche_rows) == EXPECTED_TRANCHE_ROWS_SHA256
        and tranche["per_origin_rows_sha256"]
        == EXPECTED_TRANCHE_ROWS_SHA256,
        "tranche row order and digest",
    )

    closed: list[str] = []
    failed: list[str] = []
    positive_failures: list[str] = []
    seam_failures: list[str] = []
    aggregate_failures: Counter[str] = Counter()
    source_domains: Counter[str] = Counter()
    credited_domains: Counter[str] = Counter()
    total_children = 0
    successful_child_proofs = 0
    for ordinal, row in enumerate(tranche_rows):
        require(
            row["priority_ordinal"]
            == priority_rows[ordinal]["priority_ordinal"]
            and row["row_sha256"] == digest(row_payload(row)),
            f"tranche row digest:{ordinal}",
        )
        child_count = row["Round180_residual_child_count"]
        proof_count = row["closed_residual_child_count"]
        require(
            type(child_count) is int and child_count > 0
            and type(proof_count) is int
            and 0 <= proof_count <= child_count,
            f"tranche child counts:{ordinal}",
        )
        total_children += child_count
        successful_child_proofs += proof_count
        failures = row["failure_count_by_reason"]
        aggregate_failures.update(failures)
        classification = row["source_chart_domain"]["classification"]
        source_domains[classification] += 1
        whole = row["whole_original_physical_parent_excluded"]
        split = row["inherited_split_face_ledger"]
        graph = row["analytic_Delta_outer_ledger"]
        require(
            type(split["2D_owned_split_face_count"]) is int
            and split["2D_owned_split_face_count"] >= 0
            and type(split["1D_deduplicated_split_face_edge_count"]) is int
            and split["1D_deduplicated_split_face_edge_count"] >= 0
            and type(split["0D_deduplicated_split_face_corner_count"]) is int
            and split["0D_deduplicated_split_face_corner_count"] >= 0,
            f"split dimension counts:{ordinal}",
        )
        require(
            type(graph["2D_Delta_graph_outer_count"]) is int
            and graph["2D_Delta_graph_outer_count"] > 0
            and type(graph["1D_graph_face_outer_count"]) is int
            and graph["1D_graph_face_outer_count"] > 0
            and type(graph["0D_graph_edge_outer_count"]) is int
            and graph["0D_graph_edge_outer_count"] > 0
            and type(graph["0D_graph_corner_candidate_count"]) is int
            and graph["0D_graph_corner_candidate_count"] > 0
            and graph["outer_counts_are_not_nonempty_component_counts"],
            f"analytic dimension counts:{ordinal}",
        )
        require(
            row["whole_origin_integer_credit"] == int(whole)
            and not row["child_count_or_volume_used_as_integer_credit"]
            and not row["guard_outside_used_as_exterior_credit"]
            and row["all_residual_children_explicit_Delta_partition_closed"]
            == whole
            and row["all_3D_2D_1D_0D_strata_closed"] == whole
            and split[
                "3D_closed_terminal_cells_are_primary_proof_objects"
            ] == whole
            and split[
                "all_owned_2D_1D_0D_strata_inherit_a_closed_"
                "EXCLUDED_enclosure"
            ] == whole
            and graph[
                "all_outer_strata_inherit_EXCLUDED_graph_proof"
            ] == whole,
            f"whole and all-dimension credit:{ordinal}",
        )
        if whole:
            closed.append(row["origin_key"])
            credited_domains[classification] += 1
            require(
                not failures
                and proof_count == child_count
                and classification == "STRICT_PHYSICAL_CHART_INTERIOR"
                and split["proof_status"] == "ALL_EXCLUDED"
                and graph["outer_proof_status"] == "ALL_EXCLUDED",
                f"closed origin completeness:{ordinal}",
            )
        else:
            failed.append(row["origin_key"])
            require(
                bool(failures)
                and row["whole_origin_integer_credit"] == 0
                and split["proof_status"]
                == "NOMINAL_GEOMETRY_ONLY__NO_WHOLE_CREDIT"
                and graph["outer_proof_status"]
                == "NOMINAL_MIXED_PROOF_STATUS__NO_WHOLE_CREDIT",
                f"failed origin noncredit:{ordinal}",
            )
        if "TARGET_NOT_STRICT_POSITIVE_FIRST" in failures:
            positive_failures.append(row["origin_key"])
        if (
            "PHYSICAL_SEAM_COMPOSITE_REQUIRES_SEPARATE_HALF_OPEN_"
            "PARTITION"
        ) in failures:
            seam_failures.append(row["origin_key"])

    closed.sort()
    failed.sort()
    positive_failures.sort()
    seam_failures.sort()
    require(
        len(closed) == tranche["closed_origin_count"] == 620
        and closed == tranche["closed_exact_origin_keys"]
        and digest(closed) == EXPECTED_CLOSED_KEYS_SHA256
        and tranche["closed_exact_origin_keys_sha256"]
        == EXPECTED_CLOSED_KEYS_SHA256,
        "620 exact closed origins",
    )
    require(
        len(failed) == 174
        and digest(failed) == EXPECTED_FAILED_KEYS_SHA256,
        "174 exact failed origins",
    )
    require(
        len(positive_failures) == 162
        and digest(positive_failures)
        == EXPECTED_POSITIVE_FAILURE_KEYS_SHA256
        and len(seam_failures) == 18
        and digest(seam_failures) == EXPECTED_SEAM_FAILURE_KEYS_SHA256
        and len(set(positive_failures) & set(seam_failures)) == 6
        and set(positive_failures) | set(seam_failures) == set(failed),
        "174 failure union decomposition",
    )
    require(
        map_counter(aggregate_failures) == {
            "PHYSICAL_SEAM_COMPOSITE_REQUIRES_SEPARATE_HALF_OPEN_"
            "PARTITION": 18,
            "TARGET_NOT_STRICT_POSITIVE_FIRST": 16492,
        }
        and tranche["failure_count_by_reason"]
        == map_counter(aggregate_failures)
        and total_children == 83274
        and successful_child_proofs == 66782,
        "child proof and failure aggregation",
    )
    require(
        tranche["source_chart_domain_count"]
        == map_counter(source_domains)
        == {
            "PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE": 18,
            "STRICT_PHYSICAL_CHART_INTERIOR": 776,
        }
        and tranche["credited_source_chart_domain_count"]
        == map_counter(credited_domains)
        == {"STRICT_PHYSICAL_CHART_INTERIOR": 620}
        and tranche["rational_guard_exterior_credit"] == 0,
        "source physical-domain credit",
    )
    require(
        tranche["cell_proof_contract"] == {
            "Delta_negative_open_dimension": 3,
            "Delta_zero_graph_outer_dimension": 2,
            "Delta_positive_open_dimension": 3,
            "graph_face_outer_dimension": 1,
            "graph_edge_or_corner_outer_dimension": 0,
            "graph_owner_recomputed": True,
            "graph_outgoing_chart_recomputed_for_frozen_owner": True,
            "split_faces_half_open_and_deduplicated": True,
            "graph_nonemptiness_not_required_for_exclusion_partition":
                True,
        },
        "3D/2D/1D/0D proof contract",
    )

    ledger = result["ledger_composition"]
    require(
        ledger["base_whole_record_excluded"] == 73392
        and ledger["Round184_new_whole_parent_excluded"] == 620
        and ledger["combined_whole_record_excluded"] == 74012
        and ledger["base_conservative_live"] == 3440
        and ledger["combined_conservative_live"] == 2820
        and ledger["refined_source_W_record_count"] == 76832
        and ledger["conservation_identity"] == "74012+2820=76832"
        and not ledger[
            "analytic_internal_strata_added_to_integer_record_count"
        ]
        and not ledger[
            "child_count_or_volume_added_to_integer_record_count"
        ],
        "Round184 integer ledger",
    )
    nonpromotion = result["strict_nonpromotion"]
    require(
        nonpromotion == {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "remaining_whole_exclusion_upper_candidates": 824,
            "remaining_conservative_live": 2820,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        and result["verdict"] == "PARTIAL",
        "strict nonpromotion",
    )
    return {
        "registry_rows": len(priority_rows),
        "selected_origins": len(selected),
        "closed_origins": len(closed),
        "failed_origins": len(failed),
        "positive_first_failure_origins": len(positive_failures),
        "source_seam_failure_origins": len(seam_failures),
        "failure_set_overlap": 6,
        "residual_children_replayed": total_children,
        "successful_child_proofs_rebuilt": successful_child_proofs,
        "combined_whole_record_excluded": 74012,
        "combined_conservative_live": 2820,
    }


def resign_document(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def resign_row(row: dict[str, Any]) -> None:
    row["row_sha256"] = digest(row_payload(row))


def semantic_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = []

    def registry_count(result: dict[str, Any]) -> None:
        result["priority_registry"]["row_count"] = 1443

    def registry_order(result: dict[str, Any]) -> None:
        block = result["priority_registry"]
        block["exact_origin_order"][0], block["exact_origin_order"][1] = (
            block["exact_origin_order"][1],
            block["exact_origin_order"][0],
        )
        block["exact_origin_order_sha256"] = digest(
            block["exact_origin_order"]
        )

    def class_partition(result: dict[str, Any]) -> None:
        block = result["priority_registry"]
        block["priority_class_count"]["PURE_SINGLE_CLIPPED_DELTA"] = 795
        block["priority_class_count"]["DELTA_H_OR_MULTI_NO_Q"] = 595

    def outcome_selected_order(result: dict[str, Any]) -> None:
        result["priority_registry"]["outcome_blind_ordering"] = False

    def boolean_retyped_as_integer(result: dict[str, Any]) -> None:
        result["priority_registry"]["outcome_blind_ordering"] = 1

    def registry_row_rank(result: dict[str, Any]) -> None:
        block = result["priority_registry"]
        row = block["rows"][0]
        row["priority_class_rank"] = 1
        row["priority_key"][0] = 1
        resign_row(row)
        block["rows_sha256"] = digest(block["rows"])

    def selected_key(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        block["selected_exact_origin_keys"] = (
            block["selected_exact_origin_keys"][:-1]
        )
        block["selected_origin_count"] = len(
            block["selected_exact_origin_keys"]
        )
        block["selected_exact_origin_keys_sha256"] = digest(
            block["selected_exact_origin_keys"]
        )

    def promote_failed_origin(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        row = next(
            item for item in block["per_origin_rows"]
            if not item["whole_original_physical_parent_excluded"]
        )
        row["failure_count_by_reason"] = {}
        row["closed_residual_child_count"] = (
            row["Round180_residual_child_count"]
        )
        row["all_residual_children_explicit_Delta_partition_closed"] = True
        row["inherited_split_face_ledger"][
            "3D_closed_terminal_cells_are_primary_proof_objects"
        ] = True
        row["inherited_split_face_ledger"][
            "all_owned_2D_1D_0D_strata_inherit_a_closed_"
            "EXCLUDED_enclosure"
        ] = True
        row["inherited_split_face_ledger"]["proof_status"] = "ALL_EXCLUDED"
        row["analytic_Delta_outer_ledger"][
            "all_outer_strata_inherit_EXCLUDED_graph_proof"
        ] = True
        row["analytic_Delta_outer_ledger"][
            "outer_proof_status"
        ] = "ALL_EXCLUDED"
        row["all_3D_2D_1D_0D_strata_closed"] = True
        row["whole_original_physical_parent_excluded"] = True
        row["whole_origin_integer_credit"] = 1
        resign_row(row)
        block["per_origin_rows_sha256"] = digest(block["per_origin_rows"])
        block["closed_exact_origin_keys"].append(row["origin_key"])
        block["closed_exact_origin_keys"].sort()
        block["closed_origin_count"] = len(block["closed_exact_origin_keys"])
        block["closed_exact_origin_keys_sha256"] = digest(
            block["closed_exact_origin_keys"]
        )

    def drop_closed_key(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        block["closed_exact_origin_keys"].pop()
        block["closed_origin_count"] -= 1
        block["closed_exact_origin_keys_sha256"] = digest(
            block["closed_exact_origin_keys"]
        )

    def failure_child_count(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "failure_count_by_reason"
        ]["TARGET_NOT_STRICT_POSITIVE_FIRST"] = 16491

    def child_proof_digest(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        row = next(
            item for item in block["per_origin_rows"]
            if item["whole_original_physical_parent_excluded"]
        )
        row["proof_rows_sha256"] = "0" * 64
        resign_row(row)
        block["per_origin_rows_sha256"] = digest(block["per_origin_rows"])

    def split_face_ledger(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        row = next(
            item for item in block["per_origin_rows"]
            if item["whole_original_physical_parent_excluded"]
        )
        row["inherited_split_face_ledger"][
            "2D_owned_split_face_rows_sha256"
        ] = "0" * 64
        resign_row(row)
        block["per_origin_rows_sha256"] = digest(block["per_origin_rows"])

    def analytic_outer_ledger_digest(result: dict[str, Any]) -> None:
        block = result["pure_single_clipped_Delta_tranche"]
        row = next(
            item for item in block["per_origin_rows"]
            if item["whole_original_physical_parent_excluded"]
        )
        row["analytic_Delta_outer_ledger"][
            "1D_graph_face_outer_rows_sha256"
        ] = "0" * 64
        resign_row(row)
        block["per_origin_rows_sha256"] = digest(block["per_origin_rows"])

    def graph_owner_recomputation(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "cell_proof_contract"
        ]["graph_owner_recomputed"] = False

    def graph_chart_recomputation(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "cell_proof_contract"
        ]["graph_outgoing_chart_recomputed_for_frozen_owner"] = False

    def seam_credit(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "credited_source_chart_domain_count"
        ]["PHYSICAL_CHART_SEAM_AND_GUARD_COMPOSITE"] = 1

    def graph_nonempty(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "cell_proof_contract"
        ]["graph_nonemptiness_not_required_for_exclusion_partition"] = False

    def graph_dimension(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "cell_proof_contract"
        ]["Delta_zero_graph_outer_dimension"] = 3

    def lower_dimension_credit(result: dict[str, Any]) -> None:
        result["ledger_composition"][
            "analytic_internal_strata_added_to_integer_record_count"
        ] = True

    def child_credit(result: dict[str, Any]) -> None:
        result["ledger_composition"][
            "child_count_or_volume_added_to_integer_record_count"
        ] = True

    def combined_excluded(result: dict[str, Any]) -> None:
        result["ledger_composition"][
            "combined_whole_record_excluded"
        ] = 74013

    def combined_live(result: dict[str, Any]) -> None:
        result["ledger_composition"]["combined_conservative_live"] = 2819

    def conservation(result: dict[str, Any]) -> None:
        result["ledger_composition"][
            "conservation_identity"
        ] = "74013+2819=76832"

    def remaining_candidates(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"][
            "remaining_whole_exclusion_upper_candidates"
        ] = 823

    def d02_pass(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["D02"] = "PASS"

    def d03_authorized(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"][
            "D03_negative_oracle"
        ] = "AUTHORIZED"

    def gate5_full(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["global_Gate5_fields"] = "18/18"
        result["strict_nonpromotion"]["global_complete_18_field_blocks"] = 1

    def cm2_go(result: dict[str, Any]) -> None:
        result["strict_nonpromotion"]["CM2"] = "GO"

    def verdict_full(result: dict[str, Any]) -> None:
        result["verdict"] = "FULL"
        result["status"] = "FULL__D02_CLOSED"

    def source_guard_credit(result: dict[str, Any]) -> None:
        result["pure_single_clipped_Delta_tranche"][
            "rational_guard_exterior_credit"
        ] = 1

    def producer_hash(result: dict[str, Any]) -> None:
        result["provenance"]["producer_sha256"] = "0" * 64

    def precision(result: dict[str, Any]) -> None:
        result["provenance"]["arb_precision_bits"] = 128

    def safety_contract(result: dict[str, Any]) -> None:
        result["producer_output_safety"]["path_attack_suite"][
            "all_rejected"
        ] = False

    def next_gate(result: dict[str, Any]) -> None:
        result["next_core_gate"] = "declare global theorem"

    def extra_result_field(result: dict[str, Any]) -> None:
        result["forged_extra_field"] = True

    attacks.extend([
        ("registry_count_mutated", registry_count),
        ("registry_exact_order_swapped_and_resigned", registry_order),
        ("priority_class_partition_mutated", class_partition),
        ("outcome_blind_selection_disabled", outcome_selected_order),
        ("boolean_retyped_as_integer", boolean_retyped_as_integer),
        ("registry_row_rank_mutated_and_resigned", registry_row_rank),
        ("selected_exact_key_removed_and_resigned", selected_key),
        ("failed_origin_forged_closed_with_ledgers_resigned",
         promote_failed_origin),
        ("closed_exact_key_removed_and_resigned", drop_closed_key),
        ("positive_first_child_failure_count_mutated", failure_child_count),
        ("successful_child_proof_digest_mutated_and_resigned",
         child_proof_digest),
        ("split_face_2D_ledger_digest_mutated_and_resigned",
         split_face_ledger),
        ("analytic_1D_outer_ledger_digest_mutated_and_resigned",
         analytic_outer_ledger_digest),
        ("graph_owner_recomputation_disabled", graph_owner_recomputation),
        ("graph_chart_recomputation_disabled", graph_chart_recomputation),
        ("source_seam_forged_integer_credit", seam_credit),
        ("graph_nonemptiness_contract_reversed", graph_nonempty),
        ("Delta_zero_dimension_forged_3D", graph_dimension),
        ("lower_dimensional_integer_credit_forged", lower_dimension_credit),
        ("child_or_volume_integer_credit_forged", child_credit),
        ("combined_excluded_count_mutated", combined_excluded),
        ("combined_live_count_mutated", combined_live),
        ("ledger_conservation_string_mutated", conservation),
        ("remaining_upper_candidate_count_mutated", remaining_candidates),
        ("D02_forged_pass", d02_pass),
        ("D03_negative_oracle_forged_authorized", d03_authorized),
        ("Gate5_forged_18_of_18", gate5_full),
        ("CM2_forged_go", cm2_go),
        ("partial_verdict_forged_full", verdict_full),
        ("rational_guard_forged_exterior_credit", source_guard_credit),
        ("producer_identity_mutated", producer_hash),
        ("Arb_precision_mutated", precision),
        ("producer_path_attack_contract_mutated", safety_contract),
        ("next_core_gate_forged_global", next_gate),
        ("extra_result_field_added", extra_result_field),
    ])

    rejected: list[str] = []
    for label, mutate in attacks:
        candidate = copy.deepcopy(certificate)
        mutate(candidate["result"])
        resign_document(candidate)
        require(
            candidate["result_sha256"] == digest(candidate["result"]),
            f"semantic attack re-sign:{label}",
        )
        try:
            validate_expected_document(candidate, expected)
        except Round184VerificationError:
            rejected.append(label)
        else:
            raise Round184VerificationError(
                f"semantic attack accepted:{label}"
            )
    document_attacks: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        (
            "certificate_schema_mutated",
            lambda document: document.__setitem__("schema", "forged"),
        ),
        (
            "extra_top_level_field_added",
            lambda document: document.__setitem__("extra", True),
        ),
    ]
    for label, mutate in document_attacks:
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        resign_document(candidate)
        try:
            validate_expected_document(candidate, expected)
        except Round184VerificationError:
            rejected.append(label)
        else:
            raise Round184VerificationError(
                f"semantic document attack accepted:{label}"
            )
    return rejected


def strict_json_attacks(certificate: dict[str, Any]) -> list[str]:
    pretty = pretty_bytes(certificate)
    cases = {
        "empty": b"",
        "duplicate_top_key": b'{"schema":"x","schema":"y"}\n',
        "duplicate_nested_key": (
            b'{"schema":"x","result":{"x":1,"x":2},'
            b'"result_sha256":"z"}\n'
        ),
        "float": b'{"x":1.25}\n',
        "exponent": b'{"x":1e3}\n',
        "NaN": b'{"x":NaN}\n',
        "Infinity": b'{"x":Infinity}\n',
        "BOM": b"\xef\xbb\xbf" + pretty,
        "NUL": b'{"x":"a\x00b"}\n',
        "invalid_utf8": b'{"x":"\xff"}\n',
        "unpaired_surrogate": b'{"x":"\\ud800"}\n',
        "top_level_array": b"[]\n",
        "trailing_document": pretty + b"{}\n",
        "leading_whitespace": b" " + pretty,
        "compact_noncanonical": canonical_bytes(certificate) + b"\n",
        "oversized": b" " * (MAX_CERTIFICATE_BYTES + 1),
    }
    rejected: list[str] = []
    for label, raw in cases.items():
        try:
            strict_json_bytes(raw, f"attack:{label}")
        except Round184VerificationError:
            rejected.append(label)
        else:
            raise Round184VerificationError(
                f"strict JSON attack accepted:{label}"
            )
    return rejected


def caller_authorized_output(path: Path) -> bool:
    return (
        path.name == OUTPUT.name
        or (
            path.name.startswith(".cm2_round184_")
            and path.name.endswith("_verification.json")
        )
    )


def readonly_paths() -> set[Path]:
    return {
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
        (
            HERE
            / "cm2_round184_source_w_upper_candidate_priority_and_"
              "clipped_delta_report.md"
        ).resolve(),
        (
            HERE
            / "cm2_round184_source_w_upper_candidate_priority_and_"
              "clipped_delta_cold_replay.md"
        ).resolve(),
        (
            HERE
            / "cm2_round184_source_w_upper_candidate_priority_and_"
              "clipped_delta_manifest.sha256"
        ).resolve(),
    }


def validate_output(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, "output exact directory")
    require(absolute.parent.resolve() == HERE, "output resolved directory")
    require(caller_authorized_output(absolute), "output authorized name")
    if absolute.exists() or absolute.is_symlink():
        info = absolute.lstat()
        require(not stat.S_ISLNK(info.st_mode), "output symlink")
        require(stat.S_ISREG(info.st_mode), "output regular")
        require(info.st_nlink == 1, "output hardlink")
    require(
        absolute.resolve(strict=False) not in readonly_paths(),
        "output protected path",
    )
    return absolute


def expect_path_rejection(
    label: str,
    expected_fragment: str,
    operation: Callable[[], Any],
) -> str:
    try:
        operation()
    except Round184VerificationError as exc:
        require(
            expected_fragment in str(exc),
            f"path attack wrong guard:{label}:{exc}",
        )
        return label
    raise Round184VerificationError(f"path attack accepted:{label}")


def path_attacks() -> list[str]:
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(prefix=".round184v-path-", dir=HERE))
    regular = scratch / "regular"
    symlink = scratch / "symlink"
    hardlink = scratch / "hardlink"
    directory = scratch / "directory"
    fifo = scratch / "fifo"
    oversized = scratch / "oversized"
    output_symlink = (
        HERE / f".cm2_round184_{pid}_symlink_verification.json"
    )
    output_hardlink = (
        HERE / f".cm2_round184_{pid}_hardlink_verification.json"
    )
    output_directory = (
        HERE / f".cm2_round184_{pid}_directory_verification.json"
    )
    output_fifo = (
        HERE / f".cm2_round184_{pid}_fifo_verification.json"
    )
    outside = (
        HERE.parent / f".cm2_round184_{pid}_escape_verification.json"
    )
    rejected: list[str] = []
    try:
        regular.write_bytes(b"fixture\n")
        symlink.symlink_to(regular)
        os.link(regular, hardlink)
        directory.mkdir()
        os.mkfifo(fifo)
        oversized.write_bytes(b"xx")
        output_symlink.symlink_to(regular)
        os.link(regular, output_hardlink)
        output_directory.mkdir()
        os.mkfifo(output_fifo)
        cases = [
            (
                "input_symlink",
                "input symlink",
                lambda: read_regular(
                    symlink, enforce_here_parent=False
                ),
            ),
            (
                "input_hardlink",
                "input hardlink",
                lambda: read_regular(
                    hardlink, enforce_here_parent=False
                ),
            ),
            (
                "input_directory",
                "input regular",
                lambda: read_regular(
                    directory, enforce_here_parent=False
                ),
            ),
            (
                "input_FIFO",
                "input regular",
                lambda: read_regular(
                    fifo, enforce_here_parent=False
                ),
            ),
            (
                "input_oversized",
                "input size",
                lambda: read_regular(
                    oversized,
                    maximum=1,
                    enforce_here_parent=False,
                ),
            ),
            (
                "input_parent_escape",
                "input parent",
                lambda: read_regular(regular),
            ),
            (
                "output_parent_escape",
                "output exact directory",
                lambda: validate_output(outside),
            ),
            (
                "output_nested_subdirectory",
                "output exact directory",
                lambda: validate_output(
                    scratch
                    / ".cm2_round184_nested_verification.json"
                ),
            ),
            (
                "output_producer",
                "output authorized name",
                lambda: validate_output(PRODUCER),
            ),
            (
                "output_certificate",
                "output authorized name",
                lambda: validate_output(CERTIFICATE),
            ),
            (
                "output_verifier",
                "output authorized name",
                lambda: validate_output(Path(__file__)),
            ),
            (
                "output_symlink",
                "output symlink",
                lambda: validate_output(output_symlink),
            ),
            (
                "output_hardlink",
                "output hardlink",
                lambda: validate_output(output_hardlink),
            ),
            (
                "output_directory",
                "output regular",
                lambda: validate_output(output_directory),
            ),
            (
                "output_FIFO",
                "output regular",
                lambda: validate_output(output_fifo),
            ),
        ]
        for label, fragment, operation in cases:
            rejected.append(
                expect_path_rejection(label, fragment, operation)
            )
    finally:
        for path in (
            output_symlink,
            output_hardlink,
            output_fifo,
            outside,
        ):
            if path.exists() or path.is_symlink():
                path.unlink()
        if output_directory.exists():
            output_directory.rmdir()
        shutil.rmtree(scratch)
    require(len(rejected) == 15, "path attack count")
    return rejected


def safe_atomic_write(path: Path, raw: bytes) -> Path:
    output = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.",
        suffix=".tmp",
        dir=output.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_descriptor = os.open(output.parent, directory_flags)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--expect-result")
    parser.add_argument("--print-only", action="store_true")
    arguments = parser.parse_args()

    ctx.prec = PRECISION_BITS
    producer_raw = read_regular(
        PRODUCER,
        EXPECTED_PRODUCER_SHA256,
        maximum=MAX_PRODUCER_BYTES,
    )
    require(
        sha256_bytes(producer_raw) == EXPECTED_PRODUCER_SHA256,
        "inert producer bytes",
    )
    producer_module = PRODUCER.stem
    require(
        producer_module not in sys.modules,
        "Round184 producer never imported before reconstruction",
    )
    certificate_raw = read_regular(
        CERTIFICATE,
        EXPECTED_CERTIFICATE_SHA256,
        maximum=MAX_CERTIFICATE_BYTES,
    )
    certificate = strict_json_bytes(
        certificate_raw,
        CERTIFICATE.name,
        maximum=MAX_CERTIFICATE_BYTES,
    )

    expected_result = build_expected_result()
    expected_document = {
        "schema": CERTIFICATE_SCHEMA,
        "result": expected_result,
        "result_sha256": digest(expected_result),
    }
    require(
        expected_document["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "independently rebuilt frozen result",
    )
    expected_bytes = pretty_bytes(expected_document)
    require(
        expected_bytes == certificate_raw,
        "full expected certificate byte-for-byte equality",
    )
    reconstruction = validate_expected_document(
        certificate, expected_document
    )
    semantic = semantic_attacks(certificate, expected_document)
    strict_json = strict_json_attacks(certificate)
    paths = path_attacks()
    require(
        producer_module not in sys.modules,
        "Round184 producer never imported or executed",
    )

    result = {
        "status": "PASS_PARTIAL_BOUNDED_ROUND184",
        "verifier_filename": Path(__file__).name,
        "verifier_sha256": sha256_bytes(
            read_regular(Path(__file__), maximum=500_000)
        ),
        "producer_filename": PRODUCER.name,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "certificate_filename": CERTIFICATE.name,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_result_sha256":
            EXPECTED_CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "producer_imported_or_executed": False,
            "pinned_Round180_verifier_used_as_geometry_library": True,
            "Round184_priority_registry_reimplemented": True,
            "Round184_clipped_Delta_tranche_reimplemented": True,
            "Round184_3D_2D_1D_0D_ledgers_reimplemented": True,
            "complete_expected_certificate_rebuilt": True,
            "full_expected_canonical_equality": True,
            "full_expected_certificate_byte_for_byte_equality": True,
            "frozen_expected_result_digest_used_as_substitute_for_"
            "reconstruction": False,
        },
        "independent_reconstruction": reconstruction,
        "exact_key_sets": {
            "registry_order_sha256": EXPECTED_REGISTRY_ORDER_SHA256,
            "selected_794_keys_sha256": EXPECTED_SELECTED_KEYS_SHA256,
            "closed_620_keys_sha256": EXPECTED_CLOSED_KEYS_SHA256,
            "failed_174_keys_sha256": EXPECTED_FAILED_KEYS_SHA256,
            "positive_first_failure_162_keys_sha256":
                EXPECTED_POSITIVE_FAILURE_KEYS_SHA256,
            "source_seam_failure_18_keys_sha256":
                EXPECTED_SEAM_FAILURE_KEYS_SHA256,
            "positive_first_and_seam_overlap_count": 6,
            "failure_union_count": 174,
        },
        "dimension_and_credit_checks": {
            "Delta_negative_open_dimension": 3,
            "Delta_zero_graph_outer_dimension": 2,
            "Delta_positive_open_dimension": 3,
            "graph_face_outer_dimension": 1,
            "graph_edge_or_corner_outer_dimension": 0,
            "all_620_credited_origins_have_complete_3D_2D_1D_0D_"
            "ledgers": True,
            "all_174_failed_origins_receive_zero_integer_credit": True,
            "analytic_internal_strata_integer_credit": 0,
            "child_count_or_volume_integer_credit": 0,
            "rational_guard_exterior_credit": 0,
        },
        "attack_rejections": {
            "re_signed_semantic": {
                "rejected": len(semantic),
                "total": len(semantic),
                "labels": semantic,
                "all_result_digests_recomputed_after_mutation": True,
            },
            "strict_JSON": {
                "rejected": len(strict_json),
                "total": len(strict_json),
                "labels": strict_json,
            },
            "path_type_and_output": {
                "rejected": len(paths),
                "total": len(paths),
                "labels": paths,
                "expected_rejection_guard_checked": True,
            },
        },
        "strict_nonpromotion": {
            "Round184_new_whole_parent_excluded": 620,
            "combined_whole_record_excluded": 74012,
            "combined_conservative_live": 2820,
            "remaining_whole_exclusion_upper_candidates": 824,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "verifier_provenance": {
            "verification_schema": VERIFICATION_SCHEMA,
            "python_flint_version": FLINT_VERSION,
            "arb_precision_bits": PRECISION_BITS,
            "same_directory_atomic_replace_with_file_and_directory_fsync":
                True,
        },
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    if arguments.expect_result is not None:
        require(
            envelope["result_sha256"] == arguments.expect_result,
            "expected verification result",
        )
    if arguments.print_only:
        print(canonical(envelope))
        return 0
    output = safe_atomic_write(arguments.output, pretty_bytes(envelope))
    print(canonical({
        "output": output.name,
        "result_sha256": envelope["result_sha256"],
        "status": result["status"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
