#!/usr/bin/env python3
"""Produce the candidate-only C30f retained physical-seam exclusion audit.

The two origins are discovered from the pinned Round212 retained-seam ledger
and cross-checked against the pinned Round184 registry, the Round215 seam
exclusion census, and the sealed C30a frontier.  No origin key is a selection
constant.

For each selected origin this producer locally reconstructs the exact
Round176/Round180 lineage.  The 72 already reduced cells are rebound to their
Round201 strict owner-mismatch exclusions; the other 72 cells are replayed
through the sealed C30a reduced clipped-Delta kernel.  Under the pinned inputs
all 144 cells are excluded, including every Delta=0 graph and its owned
1D/0D boundary.

The target theorem is then restricted to the exact algebraic source seam
``2*t^2=1``.  An atomic p/s grid gives every seam-relative 2D atom, every 1D
grid edge, and every 0D grid vertex a deterministic dyadic leaf owner.  The
vertical N/S chart shadows the equality and E owns it; the open guard side is
re-coordinated to E using the pinned Round212 map.  Because every possible
dyadic owner is already an excluded closed enclosure, all intersections with
target analytic strata remain excluded without an unproved transversality or
cross-root gluing assumption.

This is only a producer contract.  C30b--C30e are unsealed ordering
predecessors and none of their results, ledgers, or credits is consumed.
Every formal-credit field emitted here is zero.  A successful candidate run
does not mutate the official Source-W ledger and is not a verifier, attack
harness, replay, manifest, or seal.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import stat
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30f_source_w_retained_physical_seam_"
    "whole_origin_exclusion"
)
CELL_LEDGER = PREFIX + "_target_cell_ledger.jsonl.gz"
SOURCE_STRATA_LEDGER = PREFIX + "_source_half_open_strata_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C30A_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
C30A_SOURCE = C30A_PREFIX + "_producer.py"
C30A_MANIFEST = C30A_PREFIX + "_manifest.sha256"
C30A_SEALED = Path("cm2_round306c30a_sealed")
C30A_RESULT = C30A_SEALED / (C30A_PREFIX + "_result.json")

R184_CERTIFICATE = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "certificate.json"
)
R184_MANIFEST = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "manifest.sha256"
)
R184_VERIFICATION = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_"
    "verification.json"
)
R212_PREFIX = "cm2_round212_source_w_half_open_source_seam_promotion"
R212_SOURCE = R212_PREFIX + ".py"
R212_CERTIFICATE = R212_PREFIX + "_certificate.json"
R212_MANIFEST = R212_PREFIX + "_manifest.sha256"
R212_VERIFICATION = R212_PREFIX + "_verification.json"
R215_PROBE = "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
R215_CERTIFICATE = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_certificate.json"
)
R215_MANIFEST = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_manifest.sha256"
)
R215_VERIFICATION = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_verification.json"
)

UNSEALED_ORDERING_PREDECESSORS = {
    "C30b": (
        "cm2_round306c30b_source_w_outgoing_h_"
        "whole_origin_disposition_producer.py"
    ),
    "C30c": (
        "cm2_round306c30c_source_w_full_delta_"
        "whole_origin_disposition_producer.py"
    ),
    "C30d": (
        "cm2_round306c30d_source_w_multi_delta_"
        "whole_origin_exclusion_producer.py"
    ),
    "C30e": (
        "cm2_round306c30e_source_w_reduced_live_"
        "whole_origin_disposition_producer.py"
    ),
}

INPUT_PINS = {
    C30A_SOURCE:
        "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
    C30A_MANIFEST:
        "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc",
    os.fspath(C30A_RESULT):
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    R184_CERTIFICATE:
        "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f",
    R184_MANIFEST:
        "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1",
    R184_VERIFICATION:
        "7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6",
    R212_SOURCE:
        "dae73423b0db54987a23121197764feb3fee4c32763cf7a4b9e2275b7d5a6485",
    R212_CERTIFICATE:
        "70ad8ce31edba0d0a8b082d72ba5f191224193c683ee49181213119f762a18e9",
    R212_MANIFEST:
        "86a46848e016e99646bf03ea860b4c162d880e203803d259d88785a8e429b919",
    R212_VERIFICATION:
        "09b8a3282539740187776cb41e957212b2d61fafaa33d6984544564ddaa17aea",
    R215_PROBE:
        "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1",
    R215_CERTIFICATE:
        "9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec",
    R215_MANIFEST:
        "6a6463c2574b971ce6909593886f6ad4c23bddb232772fdacebb4ecca70a405a",
    R215_VERIFICATION:
        "9af901607edd4b95f1ec149bb6426a84315de22decbcd331a8d71d727894c519",
}

C30A_RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)
R184_RESULT_SHA256 = (
    "70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe"
)
R212_RESULT_SHA256 = (
    "a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d"
)
R212_VERIFICATION_RESULT_SHA256 = (
    "5ab0bb7fa213fa0e86c1252dad1a21b96ab54d4b48025e767c8af7a953383d2e"
)
R215_RESULT_SHA256 = (
    "39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee"
)
R215_BOUNDED_RESULT_SHA256 = (
    "e6af59b19440723c4770a286d6261d950fb2a22702ec8900d285b43a06d0158c"
)

EXPECTED_ORIGINS = 2
EXPECTED_FINAL_PER_ORIGIN = 144
EXPECTED_ROUND201_EXCLUDED_PER_ORIGIN = 72
EXPECTED_NEW_CLIPPED_PER_ORIGIN = 72
SEALED_BASELINE = {
    "excluded": 74_744,
    "conservative_live": 2_088,
    "remaining": 92,
    "total": 76_832,
}


class Failure(RuntimeError):
    """A fail-closed C30f contract violation."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def bootstrap_file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def import_sealed_c30a() -> Any:
    """Load only the sealed C30a mathematics, never an unsealed C30 lane."""
    path = ROOT / C30A_SOURCE
    status = path.lstat()
    need(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and bootstrap_file_hash(path) == INPUT_PINS[C30A_SOURCE],
        "sealed C30a producer source",
    )
    module_name = C30A_SOURCE[:-3]
    need(module_name not in sys.modules, "C30a not preloaded")
    specification = importlib.util.spec_from_file_location(module_name, path)
    need(
        specification is not None and specification.loader is not None,
        "C30a import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    need(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and bootstrap_file_hash(path) == INPUT_PINS[C30A_SOURCE],
        "imported sealed C30a identity",
    )
    return module


c30a = import_sealed_c30a()
canonical = c30a.canonical
digest = c30a.digest
file_hash = c30a.file_hash
r176 = c30a.r176
r180 = c30a.r180
r215 = c30a.r215
ctx = c30a.ctx


def fraction(value: Q) -> str:
    return str(value)


def regular_bytes(path: Path, maximum: int = 256 * 1024 * 1024) -> bytes:
    """Read one regular singleton below deliverables without following links."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.is_relative_to(ROOT), "input below deliverables")
    status = absolute.lstat()
    need(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        "regular singleton input:" + absolute.name,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino) == (status.st_dev, status.st_ino)
            and opened.st_size == status.st_size,
            "input race:" + absolute.name,
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "short input read:" + absolute.name)
            chunks.append(block)
            remaining -= len(block)
        need(not os.read(descriptor, 1), "input growth:" + absolute.name)
    finally:
        os.close(descriptor)
    return b"".join(chunks)


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    need(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "JSON encoding:" + label,
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    need(type(value) is dict, "JSON object:" + label)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    return strict_object(regular_bytes(path), path.name)


def sealed_row(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "row hash inserted once")
    return {**body, "row_sha256": digest(body)}


def validate_and_select_scope() -> dict[str, Any]:
    """Pin all sealed inputs and derive the two keys without literals."""
    pins: list[dict[str, str]] = []
    for filename, expected in sorted(INPUT_PINS.items()):
        actual = file_hash(ROOT / filename)
        need(actual == expected, "input pin:" + filename)
        pins.append({"filename": filename, "sha256": actual})

    c30a_result = strict_json(ROOT / C30A_RESULT)
    r184 = strict_json(ROOT / R184_CERTIFICATE)
    r212 = strict_json(ROOT / R212_CERTIFICATE)
    r212_verification = strict_json(ROOT / R212_VERIFICATION)
    r215_certificate = strict_json(ROOT / R215_CERTIFICATE)
    r215_verification = strict_json(ROOT / R215_VERIFICATION)
    need(
        c30a_result["result_sha256"] == C30A_RESULT_OBJECT_SHA256
        and digest({
            key: value for key, value in c30a_result.items()
            if key != "result_sha256"
        }) == C30A_RESULT_OBJECT_SHA256
        and r184["result_sha256"] == R184_RESULT_SHA256
        and digest(r184["result"]) == R184_RESULT_SHA256
        and r212["result_sha256"] == R212_RESULT_SHA256
        and digest(r212["result"]) == R212_RESULT_SHA256
        and r212_verification["result_sha256"]
        == R212_VERIFICATION_RESULT_SHA256
        and r212_verification["result"]["verdict"] == "PASS"
        and r212_verification["result"]["status"]
        == "PASS_FORMAL_ROUND212"
        and r215_certificate["result_sha256"] == R215_RESULT_SHA256
        and digest(r215_certificate["result"]) == R215_RESULT_SHA256
        and r215_certificate["result"]["bounded_probe_result_sha256"]
        == R215_BOUNDED_RESULT_SHA256
        and r215_verification["result"]["verdict"] == "PASS",
        "sealed R184/R212/R215/C30a result identities",
    )

    retained_rows = sorted(
        (
            row for row in r212["result"]["whole_origin_ledger"]
            ["per_origin_rows"]
            if row["outcome"] == "TARGET_INCOMPLETE_SEAM_ORIGIN_RESIDUAL"
            and row["complete_target_partition"] is False
            and row["whole_origin_integer_credit"] == 0
        ),
        key=lambda row: row["origin_key"],
    )
    origin_keys = [row["origin_key"] for row in retained_rows]
    retained_by_origin = {row["origin_key"]: row for row in retained_rows}

    bounded = r215_certificate["result"]["bounded_probe_result"]
    seam_census = bounded["Round212_seam_exclusion"]
    registry = {
        row["origin_key"]: row
        for row in r184["result"]["priority_registry"]["rows"]
        if row["origin_key"] in set(origin_keys)
    }
    need(
        len(origin_keys) == EXPECTED_ORIGINS
        and len(set(origin_keys)) == EXPECTED_ORIGINS
        and origin_keys == sorted(origin_keys)
        and origin_keys
        == r212["result"]["whole_origin_ledger"]
        ["retained_target_incomplete_source_seam_keys"]
        and digest(origin_keys)
        == r212["result"]["whole_origin_ledger"]
        ["retained_target_incomplete_source_seam_keys_sha256"]
        and origin_keys == seam_census["seam_origin_keys"]
        and digest(origin_keys) == seam_census["seam_origin_keys_sha256"]
        and seam_census["seam_origin_count"] == EXPECTED_ORIGINS
        and seam_census["seam_residual_cell_count"]
        == EXPECTED_ORIGINS * EXPECTED_NEW_CLIPPED_PER_ORIGIN
        and seam_census["seam_residual_reason_count"]
        == {"NO_EXACT_BEHIND_UNRESOLVED_CANDIDATE": 144}
        and set(registry) == set(origin_keys)
        and c30a_result["whole_origin_census"]
        ["retained_source_seam_origins_outside_active_cohort"]
        == EXPECTED_ORIGINS
        and c30a_result["source_W_ledger_transition"]["after"]
        ["remaining_partition"]["mixed_retained_source_seams"]
        == EXPECTED_ORIGINS,
        "dynamic retained physical-seam identity",
    )
    for origin in origin_keys:
        row = retained_by_origin[origin]
        source = row["source_half_open_partition"]
        target = row["target_closure"]
        need(
            registry[origin]["priority_class"] == "DELTA_H_OR_MULTI_NO_Q"
            and registry[origin]["selection_uses_new_closure_outcome"] is False
            and registry[origin]["Round180_residual_child_count"]
            == EXPECTED_FINAL_PER_ORIGIN
            and row["physical_source_partition_complete"] is True
            and row["original_chart_id"] in {"W:N", "W:S"}
            and source["source_t_sign"] == "POSITIVE"
            and source["unique_selected_seam"] == "+1/sqrt(2)"
            and source["source_seam_half_open_owner"] == "E"
            and source["original_chart_owns_source_seam"] is False
            and source["adjacent_coordinate_chart"] == "E"
            and source["chart_owned_part_seam_and_guard_are_disjoint"]
            is True
            and source["chart_owned_part_plus_seam_plus_guard_is_complete"]
            is True
            and source["exact_rechart"]
            ["Jacobian_strictly_nonzero_on_open_guard_slice"] is True
            and source["exact_rechart"]
            ["same_physical_normal_position_velocity_and_s"] is True
            and target["Round180_final_cell_count"]
            == EXPECTED_FINAL_PER_ORIGIN
            and target["inherited_terminal_count"] == 124
            and target["final_disposition_count"] == {
                "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 72,
                "UNRESOLVED": 72,
            }
            and target["all_inherited_target_strata_excluded"] is True
            and target["target_partition_count_and_exact_volume_conserved"]
            is True,
            "per-origin retained seam contract:" + origin,
        )
    return {
        "input_pins": pins,
        "c30a_result": c30a_result,
        "origin_keys": origin_keys,
        "retained_by_origin": retained_by_origin,
        "registry": registry,
        "seam_census": seam_census,
    }


def original_origin_leaf(origin: str) -> Any:
    """Reconstruct one atlas origin without building the full atlas."""
    chart_id, path = origin.rsplit(":", 1)
    reflected = path.startswith("H.")
    raw_path = path[2:] if reflected else path
    source_chart = "W:N" if reflected else chart_id
    need(
        source_chart == "W:N"
        and chart_id in {"W:N", "W:S"}
        and len(raw_path) == 14
        and raw_path[2] == "."
        and raw_path[5] == ".",
        "retained seam origin path:" + origin,
    )
    initial_path = raw_path[:6]
    matches = [
        box for box in r176.initial_boxes() if box.path == initial_path
    ]
    need(len(matches) == 1, "origin initial box:" + origin)
    box = matches[0]
    for bit in raw_path[6:]:
        need(bit in "01", "origin path bit:" + origin)
        box = r176.split(box)[int(bit)]
    leaf, _records = r176.classify(
        source_chart,
        box,
        r176.CANDIDATES[source_chart],
    )
    if reflected:
        leaf = r176.reflect_horizontal(leaf)
    need(
        leaf.box.path == path
        and leaf.classification == "multi_candidate"
        and r176.FROZEN_OWNER in leaf.active_targets,
        "origin atlas leaf:" + origin,
    )
    return leaf


def local_round176_replay(origin: str) -> dict[str, Any]:
    """Rebuild one pinned origin and its exact depth-six frontier."""
    source_leaf = original_origin_leaf(origin)
    chart_id = origin.rsplit(":", 1)[0]
    pending = [r176.Node(
        chart_id,
        source_leaf.box,
        source_leaf.active_targets,
        source_leaf.box.path,
    )]
    frontier: list[Any] = []
    prior: list[dict[str, Any]] = []
    origin_kinds: set[str] = set()
    for relative_depth in range(7):
        next_pending: list[Any] = []
        for node in pending:
            leaf, records = r176.classify(
                node.chart_id,
                node.box,
                node.active_targets,
            )
            disposition, margins = r176.terminal_disposition(
                node.chart_id,
                leaf,
            )
            if disposition is not None:
                evidence: dict[str, Any] = {
                    "leaf_key": f"{node.chart_id}:{node.box.path}",
                    "relative_depth": relative_depth,
                    "dimension": 3,
                    "disposition": disposition,
                    "coverage_numerator_64": 2 ** (6 - relative_depth),
                }
                if margins is not None:
                    evidence["closed_interval_outgoing_margin_signs"] = {
                        key: (
                            "POSITIVE" if bool(value > 0)
                            else "NEGATIVE" if bool(value < 0)
                            else "OVERWRAPPED"
                        )
                        for key, value in sorted(margins.items())
                    }
                prior.append(evidence)
                origin_kinds.add(
                    "EXCLUDED" if disposition.startswith("EXCLUDED")
                    else "LIVE"
                )
                continue
            failure = r176.failure_type(leaf, records, margins)
            inherited = (
                (r176.FROZEN_OWNER,)
                if leaf.classification == "unique_first"
                else node.active_targets
                if leaf.classification == "tangency_graph"
                else leaf.active_targets
            )
            if relative_depth == 6:
                frontier.append(r176.Frontier(
                    node.chart_id,
                    node.box,
                    inherited,
                    origin,
                    failure,
                ))
            else:
                axis = max(
                    range(3),
                    key=lambda index: (
                        node.box.t1 - node.box.t0,
                        node.box.p1 - node.box.p0,
                        node.box.s1 - node.box.s0,
                    )[index],
                )
                next_pending.extend(
                    r176.Node(
                        node.chart_id,
                        child,
                        inherited,
                        node.origin_path,
                    )
                    for child in r176.split(node.box, axis)
                )
        pending = next_pending
    need(
        origin_kinds <= {"EXCLUDED"}
        and all(row["disposition"].startswith("EXCLUDED") for row in prior),
        "prior exclusion:" + origin,
    )
    return {
        "frontier": sorted(frontier, key=lambda row: row.key),
        "origins": {origin: {
            "chart_id": chart_id,
            "path": source_leaf.box.path,
            "box": source_leaf.box,
            "active_targets": tuple(source_leaf.active_targets),
        }},
        "prior": {origin: sorted(prior, key=lambda row: row["leaf_key"])},
        "origin_kinds": {origin: origin_kinds},
    }


def reduction_projection(reduction: dict[str, Any]) -> dict[str, Any]:
    return {
        "category": reduction["category"],
        "residual_reason": reduction["residual_reason"],
        "closed": reduction["closed"],
        "disposition": reduction["disposition"],
        "eligible_targets": reduction["eligible_targets"],
        "candidate_evidence": reduction["candidate_evidence"],
    }


def round201_excluded_cell_row(
    ordinal: int,
    row: Any,
    reduction: dict[str, Any],
) -> dict[str, Any]:
    need(
        reduction["closed"] is True
        and bool(reduction["eligible_targets"])
        and reduction["disposition"] is not None
        and reduction["disposition"].startswith("EXCLUDED"),
        "Round201 excluded seam cell:" + row.key,
    )
    projection = reduction_projection(reduction)
    return sealed_row({
        "schema": "cm2.round306c30f.retained-seam.target-cell.row.v1",
        "cell_ordinal": ordinal,
        "source_kind": "PINNED_ROUND201_EXACT_BEHIND_EXCLUDED",
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "exact_volume": fraction(r215.box_volume(row.box)),
        "active_targets": list(row.active_targets),
        "reduction_projection": projection,
        "reduction_projection_sha256": digest(projection),
        "whole_closed_cell_disposition": "EXCLUDED",
        "closed_box_and_all_owned_faces_edges_vertices_excluded": True,
        "candidate_credit_if_independently_verified": {
            "target_cell_disposition": 1,
            "whole_closed_cell_exclusion": 1,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "target_cell_disposition": 0,
            "whole_closed_cell_exclusion": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__PINNED_UPSTREAM_PROOF_REBOUND_AT_ZERO_CREDIT"
        ),
    })


def clipped_excluded_cell_row(
    ordinal: int,
    row: Any,
    reduction: dict[str, Any],
) -> dict[str, Any]:
    evidence = r215.analyze_residual_cell(row, reduction) | {
        "source_chart_id": row.chart_id,
        "closed_box": r176.box_row(row.box),
        "active_targets": list(row.active_targets),
    }
    evidence["row_sha256"] = digest(evidence)
    need(
        evidence["analytic_closed"] is False
        and evidence["blocker"]
        == "SINGLE_CLIPPED_DELTA_ENDPOINT_OVERWRAP"
        and evidence["method"] == "SINGLE_DELTA_MONOTONE_ENDPOINT_PROBE",
        "retained seam clipped blocker:" + row.key,
    )
    replayed = c30a.reduced_clipped_row(ordinal, evidence)
    need(
        replayed["candidate_target"] == r176.FROZEN_OWNER
        and replayed["disposition"]
        == "CLOSED_REDUCED_FROZEN_OWNER_OUTGOING_MISMATCH"
        and replayed["whole_closed_cell_excluded"] is True
        and replayed["partition"]
        ["closed_box_and_all_owned_faces_edges_vertices_excluded"] is True
        and replayed["partition"]
        ["all_graph_face_edge_corner_strata_inherit_the_graph_disposition"]
        is True,
        "sealed C30a clipped kernel closure:" + row.key,
    )
    body = {
        key: value for key, value in replayed.items()
        if key not in {"row_sha256", "formal_credit", "strict_nonpromotion"}
    }
    return sealed_row({
        **body,
        "schema": "cm2.round306c30f.retained-seam.target-cell.row.v1",
        "cell_ordinal": ordinal,
        "source_kind": "SEALED_C30A_REDUCED_CLIPPED_KERNEL_REPLAY",
        "whole_closed_cell_disposition": "EXCLUDED",
        "candidate_credit_if_independently_verified": {
            "target_cell_disposition": 1,
            "whole_closed_cell_exclusion": 1,
            "whole_source_W_origin_exclusion": 0,
        },
        "formal_credit": {
            "target_cell_disposition": 0,
            "whole_closed_cell_exclusion": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__SEALED_C30A_KERNEL_REPLAY__ZERO_FORMAL_CREDIT"
        ),
    })


def seam_side(box: Any) -> str:
    """Classify a positive-t rational box against the irrational seam."""
    values = (
        2 * box.t0 * box.t0 - 1,
        2 * box.t1 * box.t1 - 1,
    )
    need(
        box.t0 > 0
        and box.t1 > box.t0
        and values[0] != 0
        and values[1] != 0,
        "positive rational endpoints avoid algebraic seam",
    )
    if values[1] < 0:
        return "PHYSICAL_INTERIOR"
    if values[0] > 0:
        return "GUARD_RECHART"
    need(values[0] < 0 < values[1], "unique seam bracket")
    return "CROSSES_SOURCE_SEAM"


def source_half_open_atomic_rows(
    origin: str,
    parent: Any,
    leaf_rows: dict[str, Any],
    proof_source: dict[str, str],
    source_partition: dict[str, Any],
    target_owner_audit: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Atomize the algebraic source seam over the exact dyadic p/s grid."""
    need(
        set(leaf_rows) == set(proof_source)
        and source_partition["source_seam_half_open_owner"] == "E"
        and source_partition["original_chart_owns_source_seam"] is False
        and source_partition["adjacent_coordinate_chart"] == "E"
        and target_owner_audit[
            "all_owner_rows_reduce_to_excluded_closed_3D_enclosures"
        ] is True,
        "source overlay prerequisites:" + origin,
    )
    chart_cell = origin.split(":")[1]
    need(chart_cell in {"N", "S"}, "vertical seam shadow chart")
    owner_audit_sha = digest(target_owner_audit)
    classes = {key: seam_side(row.box) for key, row in leaf_rows.items()}
    crossing = {
        key: leaf_rows[key]
        for key, value in classes.items()
        if value == "CROSSES_SOURCE_SEAM"
    }
    need(bool(crossing), "source seam crosses reconstructed leaf grid")

    rows: list[dict[str, Any]] = []

    def add(body: dict[str, Any]) -> None:
        rows.append(sealed_row({
            **body,
            "origin_key": origin,
            "target_disposition": "EXCLUDED",
            "target_disposition_basis": (
                "RESTRICTION_OF_WHOLE_CLOSED_EXCLUDED_DYADIC_ENCLOSURE"
            ),
            "target_owner_audit_sha256": owner_audit_sha,
            "analytic_target_intersections_inherit_exclusion": True,
            "formal_credit": {
                "source_stratum_disposition": 0,
                "whole_source_W_origin_exclusion": 0,
            },
        }))

    for key in sorted(leaf_rows):
        box = leaf_rows[key].box
        side = classes[key]
        regions = (
            ("PHYSICAL_INTERIOR", "2*t^2<1"),
            ("GUARD_RECHART", "2*t^2>1"),
        ) if side == "CROSSES_SOURCE_SEAM" else ((
            side,
            "2*t^2<1" if side == "PHYSICAL_INTERIOR" else "2*t^2>1",
        ),)
        for region, predicate in regions:
            source_owner = chart_cell if region == "PHYSICAL_INTERIOR" else "E"
            geometry = {
                "dyadic_closed_enclosure": r176.box_row(box),
                "relative_open_predicate": predicate,
            }
            add({
                "schema": (
                    "cm2.round306c30f.source-half-open-3D-component.row.v1"
                ),
                "stratum_id": "SOURCE_3D:" + digest({
                    "leaf": key, "region": region,
                }),
                "ambient_dimension": 3,
                "stratum_kind": region,
                "geometry": geometry,
                "dyadic_owner_leaf_key": key,
                "dyadic_owner_proof_source": proof_source[key],
                "source_chart_half_open_owner": source_owner,
                "original_vertical_chart_is_shadow_on_equality": True,
                "guard_rechart": (
                    source_partition["exact_rechart"]
                    if region == "GUARD_RECHART" else "NOT_APPLICABLE"
                ),
                "nonempty": True,
            })

    p_cuts = sorted({
        value
        for row in crossing.values()
        for value in (row.box.p0, row.box.p1)
    })
    s_cuts = sorted({
        value
        for row in crossing.values()
        for value in (row.box.s0, row.box.s1)
    })
    need(
        p_cuts[0] == parent.p0 and p_cuts[-1] == parent.p1
        and s_cuts[0] == parent.s0 and s_cuts[-1] == parent.s1,
        "seam cross-section reaches parent p/s boundary",
    )

    def candidates(
        *,
        fixed: dict[str, Q],
        open_spans: dict[str, tuple[Q, Q]],
    ) -> list[str]:
        midpoints = {
            axis: (span[0] + span[1]) / 2
            for axis, span in open_spans.items()
        }
        found = [
            key for key, row in crossing.items()
            if all(
                getattr(row.box, axis + "0") <= value
                <= getattr(row.box, axis + "1")
                for axis, value in fixed.items()
            )
            and all(
                getattr(row.box, axis + "0") < value
                < getattr(row.box, axis + "1")
                for axis, value in midpoints.items()
            )
        ]
        need(bool(found), "source seam atomic owner exists")
        return sorted(found)

    seam_area = Q(0)
    for p0, p1 in zip(p_cuts, p_cuts[1:]):
        for s0, s1 in zip(s_cuts, s_cuts[1:]):
            owners = candidates(open_spans={"p": (p0, p1), "s": (s0, s1)}, fixed={})
            need(len(owners) == 1, "unique relative-interior seam owner")
            owner = owners[0]
            area = (p1 - p0) * (s1 - s0)
            seam_area += area
            geometry = {
                "fixed": {"t": "+1/sqrt(2)"},
                "open_spans": {
                    "p": [fraction(p0), fraction(p1)],
                    "s": [fraction(s0), fraction(s1)],
                },
            }
            add({
                "schema": "cm2.round306c30f.source-seam-2D-atom.row.v1",
                "stratum_id": "SOURCE_SEAM_2D:" + digest(geometry),
                "ambient_dimension": 2,
                "stratum_kind": "SOURCE_SEAM_RELATIVE_INTERIOR_ATOM",
                "geometry": geometry,
                "exact_coordinate_measure": fraction(area),
                "dyadic_owner_leaf_key": owner,
                "dyadic_owner_proof_source": proof_source[owner],
                "dyadic_owner_selection_rule": "UNIQUE_OPEN_ATOM_OWNER",
                "source_chart_half_open_owner": "E",
                "original_vertical_chart_is_shadow_on_equality": True,
                "nonempty": True,
            })

    for p in p_cuts:
        for s0, s1 in zip(s_cuts, s_cuts[1:]):
            owners = candidates(
                fixed={"p": p},
                open_spans={"s": (s0, s1)},
            )
            owner = owners[0]
            geometry = {
                "fixed": {"t": "+1/sqrt(2)", "p": fraction(p)},
                "open_span": {"s": [fraction(s0), fraction(s1)]},
            }
            add({
                "schema": "cm2.round306c30f.source-seam-1D-atom.row.v1",
                "stratum_id": "SOURCE_SEAM_1D:" + digest(geometry),
                "ambient_dimension": 1,
                "stratum_kind": "SOURCE_SEAM_ATOMIC_GRID_EDGE",
                "geometry": geometry,
                "exact_coordinate_measure": fraction(s1 - s0),
                "dyadic_owner_leaf_key": owner,
                "dyadic_owner_proof_source": proof_source[owner],
                "dyadic_owner_selection_rule": (
                    "LEXICOGRAPHIC_LEAST_CLOSED_ENCLOSURE_CONTAINING_EDGE"
                ),
                "source_chart_half_open_owner": "E",
                "original_vertical_chart_is_shadow_on_equality": True,
                "nonempty": True,
            })
    for s in s_cuts:
        for p0, p1 in zip(p_cuts, p_cuts[1:]):
            owners = candidates(
                fixed={"s": s},
                open_spans={"p": (p0, p1)},
            )
            owner = owners[0]
            geometry = {
                "fixed": {"t": "+1/sqrt(2)", "s": fraction(s)},
                "open_span": {"p": [fraction(p0), fraction(p1)]},
            }
            add({
                "schema": "cm2.round306c30f.source-seam-1D-atom.row.v1",
                "stratum_id": "SOURCE_SEAM_1D:" + digest(geometry),
                "ambient_dimension": 1,
                "stratum_kind": "SOURCE_SEAM_ATOMIC_GRID_EDGE",
                "geometry": geometry,
                "exact_coordinate_measure": fraction(p1 - p0),
                "dyadic_owner_leaf_key": owner,
                "dyadic_owner_proof_source": proof_source[owner],
                "dyadic_owner_selection_rule": (
                    "LEXICOGRAPHIC_LEAST_CLOSED_ENCLOSURE_CONTAINING_EDGE"
                ),
                "source_chart_half_open_owner": "E",
                "original_vertical_chart_is_shadow_on_equality": True,
                "nonempty": True,
            })

    for p in p_cuts:
        for s in s_cuts:
            owners = candidates(fixed={"p": p, "s": s}, open_spans={})
            owner = owners[0]
            geometry = {"point": {
                "t": "+1/sqrt(2)",
                "p": fraction(p),
                "s": fraction(s),
            }}
            add({
                "schema": "cm2.round306c30f.source-seam-0D-atom.row.v1",
                "stratum_id": "SOURCE_SEAM_0D:" + digest(geometry),
                "ambient_dimension": 0,
                "stratum_kind": "SOURCE_SEAM_ATOMIC_GRID_VERTEX",
                "geometry": geometry,
                "dyadic_owner_leaf_key": owner,
                "dyadic_owner_proof_source": proof_source[owner],
                "dyadic_owner_selection_rule": (
                    "LEXICOGRAPHIC_LEAST_CLOSED_ENCLOSURE_CONTAINING_VERTEX"
                ),
                "source_chart_half_open_owner": "E",
                "original_vertical_chart_is_shadow_on_equality": True,
                "nonempty": True,
            })

    rows.sort(key=lambda row: row["stratum_id"])
    dimension_census = Counter(row["ambient_dimension"] for row in rows)
    source_kind_census = Counter(row["stratum_kind"] for row in rows)
    expected_area = (parent.p1 - parent.p0) * (parent.s1 - parent.s0)
    need(
        seam_area == expected_area
        and all(row["target_disposition"] == "EXCLUDED" for row in rows)
        and all(set(row["formal_credit"].values()) == {0} for row in rows)
        and dimension_census[3] > 0
        and dimension_census[2] > 0
        and dimension_census[1] > 0
        and dimension_census[0] > 0,
        "complete source seam 3D/2D/1D/0D atomization:" + origin,
    )
    theorem = {
        "kind": "SOURCE_W_EXACT_ALGEBRAIC_SOURCE_SEAM_ATOMIC_OWNER_THEOREM",
        "unique_positive_source_seam": "+1/sqrt(2)",
        "rational_t_endpoints_are_exactly_classified_by_2_t_squared_minus_1": True,
        "open_physical_3D_side_owner": chart_cell,
        "open_guard_3D_side_recharted_owner": "E",
        "source_seam_2D_1D_0D_half_open_owner": "E",
        "original_vertical_chart_shadows_every_equality_atom": True,
        "seam_2D_atoms_exactly_reclose_parent_p_s_rectangle": True,
        "seam_1D_and_0D_grid_skeleton_fully_materialized": True,
        "every_dyadic_owner_is_bound_to_an_excluded_closed_enclosure": True,
        "all_target_analytic_intersections_inherit_exclusion": True,
        "transversality_or_cross_root_gluing_assumption_used": False,
        "dimension_census": {
            str(key): value for key, value in sorted(dimension_census.items())
        },
        "stratum_kind_census": dict(sorted(source_kind_census.items())),
        "source_strata_rows_sha256": digest(rows),
    }
    return rows, theorem


def build_origin(
    ordinal: int,
    cell_ordinal: int,
    origin: str,
    registry: dict[str, Any],
    retained_row: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    replay = local_round176_replay(origin)
    frontier = replay["frontier"]
    roots: list[Any] = []
    base_rows: list[Any] = []
    base_kinds: set[str] = set()
    for row in frontier:
        kind, _evidence = r176.closure(row)
        if kind is None:
            roots.append(row)
        else:
            base_rows.append(row)
            base_kinds.add(kind)
    roots.sort(key=lambda row: row.key)
    base_rows.sort(key=lambda row: row.key)
    need(
        base_kinds <= {"EXCLUDED"}
        and len(base_rows) == registry["Round176_preclosed_frontier_count"]
        and len(roots) == registry["Round176_residual_root_count"],
        "retained seam Round176 frontier:" + origin,
    )

    refinement = r180.refine_origin(roots, 4)
    inherited = sorted(
        refinement["terminal_rows"],
        key=lambda value: value["cell_key"],
    )
    final_rows = sorted(
        refinement["final_residual_rows"],
        key=lambda value: value.key,
    )
    need(
        all(row["coarse_disposition"] == "EXCLUDED" for row in inherited)
        and len(inherited) == retained_row["target_closure"]
        ["inherited_terminal_count"]
        and len(final_rows) == EXPECTED_FINAL_PER_ORIGIN,
        "retained seam inherited/final reconstruction:" + origin,
    )

    prior = c30a.generalized_prior_partition(replay, origin)
    leaves = r215.reconstruct_refinement_leaf_frontiers(roots, refinement)
    proof_source = {
        key: "PINNED_PRE_DEPTH14_EXCLUDED"
        for key in prior["prior_closed_rows"]
    }
    proof_source.update({
        row.key: "PINNED_ROUND176_PRECLOSED_EXCLUDED" for row in base_rows
    })
    proof_source.update({
        row["cell_key"]: "PINNED_ROUND180_INHERITED_EXCLUDED"
        for row in inherited
    })

    cell_rows: list[dict[str, Any]] = []
    round201_count = 0
    clipped_count = 0
    for row in final_rows:
        reduction = r215.exact_behind_reduce(
            row,
            r180.residual_category(row),
        )
        if reduction["closed"]:
            candidate = round201_excluded_cell_row(
                cell_ordinal + len(cell_rows), row, reduction
            )
            round201_count += 1
        else:
            candidate = clipped_excluded_cell_row(
                cell_ordinal + len(cell_rows), row, reduction
            )
            clipped_count += 1
        cell_rows.append(candidate)
        proof_source[row.key] = (
            "ROUND306C30F_REBOUND_ROUND201_EXCLUDED"
            if candidate["source_kind"]
            == "PINNED_ROUND201_EXACT_BEHIND_EXCLUDED"
            else "ROUND306C30F_C30A_KERNEL_CLIPPED_EXCLUDED"
        )
    need(
        round201_count == EXPECTED_ROUND201_EXCLUDED_PER_ORIGIN
        and clipped_count == EXPECTED_NEW_CLIPPED_PER_ORIGIN
        and all(row["whole_closed_cell_disposition"] == "EXCLUDED"
                for row in cell_rows),
        "retained seam final exclusion partition:" + origin,
    )

    leaf_rows: dict[str, Any] = dict(prior["prior_closed_rows"])
    leaf_rows.update({row.key: row for row in base_rows})
    leaf_rows.update(leaves["terminal"])
    leaf_rows.update(leaves["final"])
    need(set(leaf_rows) == set(proof_source), "complete leaf proof map")
    owner_audit = r215.strict_lower_strata_owner_audit(
        prior["split_face_rows"],
        refinement["split_face_rows"],
        replay["origins"][origin]["box"],
        leaf_rows,
        proof_source,
    )
    need(
        owner_audit[
            "all_owner_rows_reduce_to_excluded_closed_3D_enclosures"
        ]
        and owner_audit["internal_and_outer_strata_classes_are_disjoint"]
        and owner_audit["trusted_legacy_ledger_conclusion_boolean"] is False,
        "target atomic half-open owner audit:" + origin,
    )

    parent = replay["origins"][origin]["box"]
    source_rows, source_theorem = source_half_open_atomic_rows(
        origin,
        parent,
        leaf_rows,
        proof_source,
        retained_row["source_half_open_partition"],
        owner_audit,
    )

    parent_volume = r215.box_volume(parent)
    prior_volume = prior["prior_closed_exact_volume"]
    base_volume = sum((r215.box_volume(row.box) for row in base_rows), Q(0))
    root_volume = sum((r215.box_volume(row.box) for row in roots), Q(0))
    inherited_volume = sum(
        (r215.box_volume(row.box) for row in leaves["terminal"].values()),
        Q(0),
    )
    final_volume = sum((r215.box_volume(row.box) for row in final_rows), Q(0))
    need(
        prior_volume + base_volume + root_volume == parent_volume
        and inherited_volume + final_volume == root_volume,
        "retained seam exact rational enclosure conservation:" + origin,
    )
    lower_ledger = r180.lower_strata_ledger(refinement["split_face_rows"])
    theorem = {
        "kind": (
            "SOURCE_W_RETAINED_PHYSICAL_SEAM_WHOLE_ORIGIN_"
            "EXCLUSION_THEOREM_CANDIDATE"
        ),
        "origin_selected_dynamically_from_pinned_Round212_retained_ledger": True,
        "Round176_prior_and_frontier_partition_exact": True,
        "Round180_inherited_target_strata_all_excluded": True,
        "Round201_exact_behind_cells_all_excluded": True,
        "sealed_C30a_reduced_clipped_kernel_closes_every_other_cell": True,
        "every_target_3D_2D_1D_0D_stratum_has_one_excluded_half_open_owner": True,
        "source_physical_interior_seam_guard_partition_exact": True,
        "source_seam_2D_1D_0D_atomic_grid_complete": True,
        "source_seam_owner_E_and_vertical_chart_shadow_rule_applied": True,
        "guard_rechart_preserves_physical_normal_position_velocity_and_s": True,
        "all_source_target_cross_strata_are_excluded_by_restriction": True,
        "rank_aware_multi_graph_or_cross_root_gluing_needed": False,
        "whole_original_physical_origin_excluded_candidate": True,
    }
    body = {
        "schema": (
            "cm2.round306c30f.retained-physical-seam."
            "whole-origin-row.candidate.v1"
        ),
        "origin_ordinal": ordinal,
        "origin_key": origin,
        "priority_ordinal": registry["priority_ordinal"],
        "source_chart_id": replay["origins"][origin]["chart_id"],
        "original_parent_box": r176.box_row(parent),
        "dynamic_Round212_binding": {
            "retained_row_sha256": retained_row["row_sha256"],
            "source_half_open_partition": retained_row[
                "source_half_open_partition"
            ],
            "target_closure_summary": retained_row["target_closure"],
        },
        "lineage_census": {
            "Round176_prior_closed": prior["prior_closed_count"],
            "Round176_preclosed_frontier": len(base_rows),
            "Round176_residual_roots": len(roots),
            "Round180_inherited_excluded": len(inherited),
            "Round180_final": len(final_rows),
            "Round201_exact_behind_excluded": round201_count,
            "Round306C30F_C30a_kernel_clipped_excluded": clipped_count,
            "closed_3D_leaf_count": len(leaf_rows),
        },
        "target_cell_rows_sha256": digest(cell_rows),
        "target_atomic_half_open_owner_audit": owner_audit,
        "target_lower_dimensional_strata": lower_ledger,
        "source_half_open_strata_row_count": len(source_rows),
        "source_half_open_strata_rows_sha256": digest(source_rows),
        "source_half_open_atomic_theorem": source_theorem,
        "source_half_open_atomic_theorem_sha256": digest(source_theorem),
        "exact_rational_enclosure_volume_conservation": {
            "original_parent": fraction(parent_volume),
            "Round176_prior": fraction(prior_volume),
            "Round176_preclosed_frontier": fraction(base_volume),
            "Round176_residual_roots": fraction(root_volume),
            "Round180_inherited": fraction(inherited_volume),
            "Round180_final": fraction(final_volume),
            "all_equalities_verified": True,
            "algebraic_source_substrata_volume_used_as_credit": False,
        },
        "whole_origin_exclusion_theorem_candidate": theorem,
        "whole_origin_exclusion_theorem_candidate_sha256": digest(theorem),
        "whole_origin_disposition_candidate": "EXCLUDED",
        "whole_original_physical_origin_excluded_candidate": True,
        "candidate_credit_if_all_dependencies_and_checks_later_seal": {
            "resolved_source_W_origin_disposition": 1,
            "whole_source_W_origin_exclusion": 1,
        },
        "formal_credit": {
            "resolved_source_W_origin_disposition": 0,
            "whole_source_W_origin_exclusion": 0,
        },
        "strict_nonpromotion": (
            "PRODUCER_ONLY__NO_C30F_VERIFIER_MANIFEST_OR_UPSTREAM_SEAL_CHAIN"
        ),
    }
    return sealed_row(body), cell_rows, source_rows


def candidate_directory(path: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute != ROOT and absolute.parent != absolute, "candidate path")
    if absolute.exists():
        status = absolute.lstat()
        need(
            stat.S_ISDIR(status.st_mode)
            and not absolute.is_symlink()
            and not any(absolute.iterdir()),
            "empty candidate directory",
        )
    else:
        need(absolute.parent.is_dir(), "candidate parent exists")
        absolute.mkdir()
    return absolute


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str]:
    sequence = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=9,
            fileobj=raw,
            mtime=0,
        ) as stream:
            for row in rows:
                need(
                    row["row_sha256"] == digest({
                        key: value for key, value in row.items()
                        if key != "row_sha256"
                    }),
                    "row closure:" + path.name,
                )
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return count, sequence.hexdigest()


def descriptor(
    path: Path,
    count: int,
    sequence: str,
    order: str,
) -> dict[str, Any]:
    return {
        "filename": path.name,
        "row_count": count,
        "row_sequence_sha256": sequence,
        "sha256": file_hash(path),
        "size": path.stat().st_size,
        "order": order,
    }


def build(candidate_path: Path) -> dict[str, Any]:
    need(
        sys.flags.isolated == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True,
        "isolated no-bytecode runtime",
    )
    ctx.prec = 192
    c30a.validate_runtime()
    inputs = validate_and_select_scope()
    candidate = candidate_directory(candidate_path)

    origin_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    for ordinal, origin in enumerate(inputs["origin_keys"]):
        origin_row, new_cells, new_source_rows = build_origin(
            ordinal,
            len(cell_rows),
            origin,
            inputs["registry"][origin],
            inputs["retained_by_origin"][origin],
        )
        origin_rows.append(origin_row)
        cell_rows.extend(new_cells)
        source_rows.extend(new_source_rows)

    origin_rows.sort(key=lambda row: row["origin_key"])
    cell_rows.sort(key=lambda row: row["cell_key"])
    source_rows.sort(key=lambda row: (row["origin_key"], row["stratum_id"]))
    cell_source_census = Counter(row["source_kind"] for row in cell_rows)
    source_dimension_census = Counter(
        row["ambient_dimension"] for row in source_rows
    )
    need(
        [row["origin_key"] for row in origin_rows] == inputs["origin_keys"]
        and len(origin_rows) == EXPECTED_ORIGINS
        and len(cell_rows) == EXPECTED_ORIGINS * EXPECTED_FINAL_PER_ORIGIN
        and cell_source_census == Counter({
            "PINNED_ROUND201_EXACT_BEHIND_EXCLUDED": 144,
            "SEALED_C30A_REDUCED_CLIPPED_KERNEL_REPLAY": 144,
        })
        and all(row["whole_origin_disposition_candidate"] == "EXCLUDED"
                for row in origin_rows)
        and all(set(row["formal_credit"].values()) == {0}
                for row in origin_rows + cell_rows + source_rows)
        and set(source_dimension_census) == {0, 1, 2, 3},
        "global C30f candidate and zero-credit census",
    )

    cell_count, cell_sequence = write_rows(
        candidate / CELL_LEDGER, cell_rows
    )
    source_count, source_sequence = write_rows(
        candidate / SOURCE_STRATA_LEDGER, source_rows
    )
    origin_count, origin_sequence = write_rows(
        candidate / ORIGIN_LEDGER, origin_rows
    )
    cell_descriptor = descriptor(
        candidate / CELL_LEDGER,
        cell_count,
        cell_sequence,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    source_descriptor = descriptor(
        candidate / SOURCE_STRATA_LEDGER,
        source_count,
        source_sequence,
        "LEXICOGRAPHIC_ORIGIN_KEY_THEN_SOURCE_STRATUM_ID",
    )
    origin_descriptor = descriptor(
        candidate / ORIGIN_LEDGER,
        origin_count,
        origin_sequence,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )

    predecessor_contracts = {
        lane: {
            "producer_source_name": filename,
            "producer_source_consumed_or_imported": False,
            "result_or_ledger_consumed": False,
            "source_hash_used_as_a_mathematical_input": False,
            "dependency_kind": (
                "REQUIRED_CONDITIONAL_LEDGER_ORDER_PREDECESSOR_ONLY"
            ),
            "official_credit_inherited": 0,
        }
        for lane, filename in sorted(UNSEALED_ORDERING_PREDECESSORS.items())
    }
    theorem = {
        "kind": (
            "SOURCE_W_TWO_RETAINED_PHYSICAL_SEAMS_COMPLETE_"
            "EXCLUSION_THEOREM_CANDIDATE"
        ),
        "origin_keys_dynamically_derived_from_pinned_Round212": True,
        "origin_count": len(origin_rows),
        "origin_keys_sha256": digest(inputs["origin_keys"]),
        "all_288_target_cells_excluded": True,
        "all_target_internal_and_outer_3D_2D_1D_0D_strata_excluded": True,
        "source_half_open_physical_interior_seam_guard_partition_exact": True,
        "source_seam_atomic_2D_1D_0D_grid_complete": True,
        "every_source_target_cross_stratum_excluded": True,
        "both_whole_original_physical_origins_excluded_candidate": True,
        "unsealed_C30b_C30c_C30d_C30e_math_or_credit_consumed": False,
        "child_stratum_count_or_volume_used_as_integer_credit": False,
    }
    body = {
        "schema": (
            "cm2.round306c30f.source-w-retained-physical-seam-"
            "whole-origin-exclusion.candidate.v1"
        ),
        "status": (
            "PASS_CANDIDATE_ROUND306C30F_RETAINED_PHYSICAL_SEAMS__"
            "2_WHOLE_ORIGINS_EXCLUDED__ZERO_FORMAL_CREDIT"
        ),
        "input_pins": inputs["input_pins"],
        "dynamic_scope": {
            "selection_source": (
                "PINNED_ROUND212_RETAINED_TARGET_INCOMPLETE_SEAM_ROWS"
            ),
            "selection_uses_hardcoded_origin_keys": False,
            "origin_count": len(inputs["origin_keys"]),
            "origin_keys": inputs["origin_keys"],
            "origin_keys_sha256": digest(inputs["origin_keys"]),
            "Round215_seam_residual_cell_count": inputs["seam_census"]
            ["seam_residual_cell_count"],
        },
        "target_cell_census": {
            "input": len(cell_rows),
            "by_source_kind": dict(sorted(cell_source_census.items())),
            "disposition": {"EXCLUDED": len(cell_rows)},
        },
        "source_half_open_strata_census": {
            "row_count": len(source_rows),
            "by_ambient_dimension": {
                str(key): value
                for key, value in sorted(source_dimension_census.items())
            },
            "disposition": {"EXCLUDED": len(source_rows)},
        },
        "whole_origin_census_candidate": {
            "audited": len(origin_rows),
            "excluded": len(origin_rows),
            "resolved_nonexcluded": 0,
        },
        "candidate_theorem": theorem,
        "candidate_theorem_sha256": digest(theorem),
        "unsealed_upstream_dependencies": {
            **predecessor_contracts,
            "all_absolute_post_C30f_ledger_counts_are_conditional": True,
            "no_unsealed_source_result_ledger_or_credit_is_an_input": True,
        },
        "proposed_source_W_ledger_delta_if_every_predecessor_and_C30f_later_seal": {
            "whole_origin_exclusion": 2,
            "resolved_origin_disposition": 2,
            "resolved_nonexcluded": 0,
            "remaining": -2,
            "excluded": 2,
            "conservative_live": -2,
            "apply_to": (
                "FUTURE_SEALED_POST_C30E_STATE_ONLY__"
                "ABSOLUTE_BASELINE_INTENTIONALLY_UNBOUND"
            ),
            "official_ledger_mutated": False,
        },
        "last_sealed_source_W_state": {
            "source": "ROUND306C30A",
            **SEALED_BASELINE,
            "official_transition_from_this_producer": "NONE",
        },
        "ledgers": {
            "target_cell_candidate": cell_descriptor,
            "source_half_open_strata_candidate": source_descriptor,
            "whole_origin_exclusion_candidate": origin_descriptor,
        },
        "formal_credit": {
            "target_cell_dispositions": 0,
            "target_whole_cell_exclusions": 0,
            "source_half_open_stratum_dispositions": 0,
            "resolved_source_W_origin_dispositions": 0,
            "whole_source_W_origin_exclusions": 0,
            "D02": 0,
            "D03": 0,
            "D04": 0,
            "Gate5": 0,
            "CM2": 0,
        },
        "candidate_credit_if_all_dependencies_and_independent_checks_later_seal": {
            "target_cell_dispositions": len(cell_rows),
            "target_whole_cell_exclusions": len(cell_rows),
            "resolved_source_W_origin_dispositions": 2,
            "whole_source_W_origin_exclusions": 2,
        },
        "strict_nonpromotion": {
            "producer_only": True,
            "independent_verifier_present": False,
            "attack_harness_present": False,
            "dual_seed_replay_present": False,
            "cold_replay_present": False,
            "manifest_present": False,
            "sealed_directory_present": False,
            "C30b_C30c_C30d_C30e_sealed_chain_consumed": False,
            "official_source_W_transition": "UNCHANGED_FROM_SEALED_C30A",
            "D02": "BLOCKED_BY_LAST_SEALED_SOURCE_W_STATE_AND_COMPOSITE_GATE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5_filled_field_slots": "10/18",
            "Gate5_complete_global_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "FIRST_SEAL_THE_REQUIRED_C30B_C30C_C30D_C30E_PREDECESSOR_CHAIN__"
            "THEN_BUILD_AN_INDEPENDENT_C30F_VERIFIER_ATTACK_HARNESS_DUAL_"
            "SEED_COLD_REPLAY_AND_MANIFEST_BEFORE_ANY_LEDGER_CREDIT"
        ),
    }
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    need(
        {path.name for path in candidate.iterdir()} == {
            CELL_LEDGER,
            SOURCE_STRATA_LEDGER,
            ORIGIN_LEDGER,
            RESULT,
        },
        "candidate exact file set",
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
