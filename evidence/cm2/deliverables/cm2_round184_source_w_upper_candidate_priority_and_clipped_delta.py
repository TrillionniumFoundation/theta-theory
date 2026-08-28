#!/usr/bin/env python3
"""Round184 deterministic priority registry and pure clipped-Delta tranche.

The complete set of 1,444 Round180 still-open whole-exclusion upper
candidates is reconstructed before any new closure is attempted.  Origins
are ordered without looking at the success of the new proof:

    residual support class, residual child count, exact origin key.

Only the first class -- origins whose entire Round180 residual support is a
single clipped discriminant graph -- enters the bounded proof tranche.
Integer credit is granted only when every residual child admits an explicit
Delta<0 / Delta=0 / Delta>0 exclusion proof and the inherited 3D/2D/1D/0D
ownership ledger is complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_round180_full_multi_residual_dimension_safe_partial_verifier as r180


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_certificate.json"
)
SCHEMA = (
    "cm2.round184.source-w-upper-candidate-priority-and-clipped-delta.v1"
)
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
NON_CERTIFICATE_PROTECTED = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_verifier.py",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_verification.json",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_report.md",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_cold_replay.md",
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
      "_manifest.sha256",
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


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
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
    require(type(value) is dict, f"top:{path.name}")
    return value


def check_chain() -> dict[str, Any]:
    require(
        Path(r180.__file__).resolve()
        == (
            HERE
            / "cm2_round180_full_multi_residual_dimension_safe_partial"
              "_verifier.py"
        ).resolve(),
        "Round180 verifier module",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            == expected,
            f"pin:{name}",
        )
    certificate = strict_load(
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial"
          "_certificate.json"
    )
    verification = strict_load(
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial"
          "_verification.json"
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
    manifest = (
        HERE
        / "cm2_round180_full_multi_residual_dimension_safe_partial"
          "_manifest.sha256"
    )
    entries = {}
    for line in manifest.read_text().splitlines():
        value, name = line.split("  ", 1)
        entries[name] = value
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == value,
            f"manifest:{name}",
        )
    require(entries == {
        name: PINS[name] for name in PINS if name != manifest.name
    }, "Round180 manifest entries")
    r180.check_chain()
    return {
        "Round180_result_sha256": ROUND180_RESULT,
        "Round180_verification_result_sha256":
            ROUND180_VERIFICATION_RESULT,
        "Round180_manifest_entries_replayed": True,
    }


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def support_class(counts: Counter[str]) -> str:
    support = set(counts)
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
                face_rows[key] = min(face_rows.get(key, row.key), row.key)
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
        for t in bounds[0]:
            for p in bounds[1]:
                for s in bounds[2]:
                    corner = {
                        "chart": row.chart_id,
                        "target": target,
                        "point": {
                            "t": str(t), "p": str(p), "s": str(s)
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


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
        *((HERE / name).resolve() for name in NON_CERTIFICATE_PROTECTED),
    }


def caller_authorized_output(path: Path) -> bool:
    return (
        path.name == OUTPUT.name
        or (
            path.name.startswith(".cm2_round184_")
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
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(
    name: str, operation: Callable[[], Any]
) -> str:
    try:
        operation()
    except Exception:
        return name
    raise RuntimeError(f"path attack accepted:{name}")


def path_attacks() -> dict[str, Any]:
    actual = protected_paths()
    expected = {
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
        *((HERE / name).resolve() for name in NON_CERTIFICATE_PROTECTED),
    }
    require(actual == expected and OUTPUT.resolve() not in actual,
            "protected set")
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(prefix=".round184-path.", dir=HERE))
    source = scratch / "source"
    source.write_bytes(b"fixture\n")
    symlink = HERE / f".cm2_round184_symlink_{pid}_certificate.json"
    hard_base = HERE / f".cm2_round184_hardbase_{pid}_certificate.json"
    hard_link = HERE / f".cm2_round184_hardlink_{pid}_certificate.json"
    fifo = HERE / f".cm2_round184_fifo_{pid}_certificate.json"
    outside = HERE.parent / f".cm2_round184_escape_{pid}_certificate.json"
    fixtures: list[Path] = []
    rejected: list[str] = []
    try:
        symlink.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink, b"x", actual),
        ))
        hard_base.write_bytes(b"fixture\n")
        os.link(hard_base, hard_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_link, b"x", actual),
        ))
        rejected.append(expect_rejection(
            "parent directory escape",
            lambda: safe_atomic_write(outside, b"x", actual),
        ))
        rejected.append(expect_rejection(
            "nested subdirectory output",
            lambda: safe_atomic_write(
                scratch / ".cm2_round184_nested_certificate.json",
                b"x",
                actual,
            ),
        ))
        rejected.append(expect_rejection(
            "existing directory output",
            lambda: safe_atomic_write(scratch, b"x", actual),
        ))
        os.mkfifo(fifo)
        rejected.append(expect_rejection(
            "FIFO output",
            lambda: safe_atomic_write(fifo, b"x", actual),
        ))
        labels = [
            "producer self",
            *(f"Round180 pin:{name}" for name in sorted(PINS)),
            *(
                f"Round184 protected:{name}"
                for name in NON_CERTIFICATE_PROTECTED
            ),
        ]
        for index, label in enumerate(labels):
            fixture = (
                HERE
                / f".cm2_round184_protected_{pid}_{index}_certificate.json"
            )
            fixture.write_bytes(b"fixture\n")
            fixtures.append(fixture)
            fixture_protected = actual | {fixture.resolve()}
            rejected.append(expect_rejection(
                label,
                lambda fixture=fixture, fixture_protected=fixture_protected:
                    safe_atomic_write(fixture, b"x", fixture_protected),
            ))
    finally:
        for path in (
            symlink, hard_link, hard_base, fifo, outside, *fixtures
        ):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    require(len(rejected) == 19, "path attack count")
    return {
        "attack_count": 19,
        "rejected_count": 19,
        "all_rejected": True,
        "rejected_attack_names": rejected,
        "write_attempts_against_real_pins": 0,
    }


def build_result() -> dict[str, Any]:
    upstream = check_chain()
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
        row = {
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
        row["row_sha256"] = digest(row)
        priority_rows.append(row)

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
        row = {
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
        row["row_sha256"] = digest(row)
        tranche_rows.append(row)

    newly_closed.sort()
    tranche_rows.sort(key=lambda row: row["priority_ordinal"])
    combined_excluded = 73392 + len(newly_closed)
    combined_live = 3440 - len(newly_closed)
    require(
        combined_excluded + combined_live == 76832,
        "ledger conservation",
    )
    result = {
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
            "official_certificate_may_be_replaced": OUTPUT.name,
            "cold_replay_rule":
                "hidden .cm2_round184_*_certificate.json in HERE only",
            "other_same_directory_outputs_authorized": False,
            "same_directory_atomic_fsync_replace": True,
            "path_attack_suite": path_attacks(),
        },
        "provenance": {
            "producer": Path(__file__).name,
            "producer_sha256":
                hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_flint_version": "0.9.0",
            "arb_precision_bits": 192,
            "imports_only_frozen_Round180_verifier_geometry": True,
            "older_round_files_modified": False,
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ctx.prec = 192
    result = build_result()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_atomic_write(
        arguments.output, pretty_bytes(document), protected_paths()
    )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
