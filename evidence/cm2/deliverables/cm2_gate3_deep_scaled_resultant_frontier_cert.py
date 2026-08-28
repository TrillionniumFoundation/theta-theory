#!/usr/bin/env python3
"""Gate-3 deep endpoint-scaled/resultant frontier certificate.

This is a strict extension of the frozen fourteenth-pass Gate-3 stack.  It
never edits or reinterprets that stack.  The new layer exports the exact
half-open coordinate ledger of the old and deep source-tagged terminal
records, injects the already certified endpoint-scaled ``c_p`` witness only
after coordinatewise containment has been checked, and then continues the
ordinary miss/root/candidate/owner audit on those same boxes.

The critical boxes are independently replayed with a second-t derivative
interval jet.  No box is removed unless the relevant regular-value or
downstream classification test is strict on its full closed rectangle.
"""

from __future__ import annotations

import copy
import hashlib
import json
import multiprocessing
import os
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_endpoint_scaled_resultant_frontier_cert as previous
import cm2_gate3_physical_first_unresolved_frontier_cert as frozen
import cm2_gate3_finite_s_future_singularity_outer_atlas_cert as outer


# Match the frozen fourteenth replay bit-for-bit.  The second-derivative
# resultant test below uses the same rigorous precision rather than silently
# changing the terminal partition through a precision increase.
ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
PREVIOUS_MANIFEST = (
    HERE / "cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box_record(row_index: int, row: dict[str, Any], box: outer.FutureBox) -> dict[str, Any]:
    return {
        "row_index": row_index,
        "occurrence_id": row["occurrence_id"],
        "t": [str(box.t0), str(box.t1)],
        "v": [str(box.v0), str(box.v1)],
        "s": [str(box.s0), str(box.s1)],
        "t_depth": box.t_depth,
        "v_depth": box.v_depth,
    }


def terminal_replay_one_row(
    task: tuple[int, dict[str, Any], int, int],
) -> dict[str, Any]:
    """Replay one row and export every terminal rectangle coordinate.

    This follows the frozen control flow exactly through terminalization.  It
    deliberately omits accepted graph records, which are irrelevant to the
    containment ledger.  The exported terminal counts/digests are checked
    against the frozen aggregate replay before any new inference is made.
    """

    row_index, row, selective_t, selective_v = task
    pending = frozen.initial_boxes_for_row(row_index)
    terminal: list[dict[str, Any]] = []
    calls = 0
    while pending:
        box = pending.pop()
        calls += 1
        status, witness = outer.audit_box(row, box)
        if status == "refine_t" and box.t_depth < frozen.MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status == "refine_t" and box.v_depth < frozen.MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.v_depth < frozen.MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.t_depth < frozen.MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status in {
            "analytic_unresolved", "owner_unresolved", "multi_or_tangent_unresolved",
        }:
            if box.t_depth < frozen.MAX_T_DEPTH:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < frozen.MAX_V_DEPTH:
                pending.extend(reversed(box.split_v()))
                continue

        if status in {"immutable", "transverse_root_strip"}:
            if status == "transverse_root_strip":
                candidate = witness["candidate_relative_to_miss_source"]
                ok, _typed = frozen.physical_first_witness(row, box, candidate)
                if not ok:
                    if box.t_depth < selective_t:
                        pending.extend(reversed(box.split_t()))
                        continue
                    if box.v_depth < selective_v:
                        pending.extend(reversed(box.split_v()))
                        continue
            continue

        reason = witness.get("reason", status)
        if reason == "transverse_candidate_not_bracketed_on_full_s_slab":
            candidate = witness.get("candidate_relative_to_miss_source")
            if isinstance(candidate, str):
                ok, conditional = frozen.physical_first_witness(row, box, candidate)
                if ok:
                    continue
                if box.t_depth < selective_t:
                    pending.extend(reversed(box.split_t()))
                    continue
                if box.v_depth < selective_v:
                    pending.extend(reversed(box.split_v()))
                    continue
                reason = conditional.get("physical_first_failure", reason)
        if box.t_depth < selective_t:
            pending.extend(reversed(box.split_t()))
            continue
        if box.v_depth < selective_v:
            pending.extend(reversed(box.split_v()))
            continue
        covered, _graphs, summary = frozen.candidate_graph_cover(row, box)
        if covered:
            continue
        reason = summary.get("graph_cover_failure", reason)
        terminal.append({
            **box_record(row_index, row, box),
            "terminal_status": status,
            "terminal_reason": reason,
            "outer_witness_digest": canonical_digest(witness),
            "graph_summary_digest": canonical_digest(summary),
        })
    terminal.sort(key=canonical_json)
    return {
        "row_index": row_index,
        "audit_call_count": calls,
        "terminal_records": terminal,
    }


def replay_terminal_records(
    rows: list[dict[str, Any]], selective_t: int, selective_v: int,
) -> dict[str, Any]:
    workers = min(int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64)
    tasks = [(index, row, selective_t, selective_v) for index, row in enumerate(rows)]
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        parts = list(pool.imap_unordered(terminal_replay_one_row, tasks, chunksize=1))
    parts.sort(key=lambda part: part["row_index"])
    records = [record for part in parts for record in part["terminal_records"]]
    records.sort(key=canonical_json)
    reasons = Counter(record["terminal_reason"] for record in records)
    return {
        "records": records,
        "reason_counts": dict(sorted(reasons.items())),
        "record_ledger_sha256": canonical_digest(records),
        "audit_call_count": sum(part["audit_call_count"] for part in parts),
        "per_row_terminal_record_digests": [
            {
                "row_index": part["row_index"],
                "terminal_count": len(part["terminal_records"]),
                "terminal_digest": canonical_digest(part["terminal_records"]),
            }
            for part in parts
        ],
    }


def source_band_descriptor(row_index: int, row: dict[str, Any]) -> dict[str, Any] | None:
    sides = [
        side for side in ("left_boundary", "right_boundary")
        if row[side]["kind"] == outer.finite.maximal.SOURCE_GRAZING
    ]
    if not sides:
        return None
    assert len(sides) == 1
    side = sides[0]
    width = Q(1, 1024)
    t0, t1 = (Q(0), width) if side == "left_boundary" else (1 - width, Q(1))
    return {
        "row_index": row_index,
        "side": side,
        "t": [str(t0), str(t1)],
        "parameter_cell_count": 64,
    }


def source_containment_ledger(
    rows: list[dict[str, Any]], records: list[dict[str, Any]], *, deep: bool,
) -> dict[str, Any]:
    bands = {
        index: descriptor
        for index, row in enumerate(rows)
        if (descriptor := source_band_descriptor(index, row)) is not None
    }
    source = [record for record in records if record["terminal_reason"] == "source_cp_not_strict"]
    ledger: list[dict[str, Any]] = []
    for record in source:
        row_index = int(record["row_index"])
        band = bands.get(row_index)
        assert band is not None
        t0, t1 = map(Q, record["t"])
        b0, b1 = map(Q, band["t"])
        v0, v1 = map(Q, record["v"])
        # The canonical witness uses 64 closed parameter cells.  Deep
        # 128-cell slabs must be contained in one of them; old slabs coincide.
        parent_v_index = int(v0 * 64)
        pv0, pv1 = Q(parent_v_index, 64), Q(parent_v_index + 1, 64)
        assert b0 <= t0 < t1 <= b1
        assert pv0 <= v0 < v1 <= pv1
        if not deep:
            assert (t0, t1) == (b0, b1)
            assert (v0, v1) == (pv0, pv1)
        ledger.append({
            "row_index": row_index,
            "occurrence_id": record["occurrence_id"],
            "side": band["side"],
            "record_t": record["t"],
            "record_v": record["v"],
            "containing_canonical_t_band": band["t"],
            "containing_canonical_v_cell": [str(pv0), str(pv1)],
            "coordinatewise_contained": True,
            "closed_v1_owned": v1 == 1,
        })
    ledger.sort(key=canonical_json)
    return {
        "source_tagged_record_count": len(source),
        "source_tagged_row_count": len({record["row_index"] for record in source}),
        "canonical_source_band_count": len(bands),
        "coordinatewise_containment_certified_for_every_record": True,
        "old_records_equal_canonical_cells" if not deep else "deep_records_contained_in_canonical_cells": True,
        "closed_v1_record_count": sum(record["closed_v1_owned"] for record in ledger),
        "coordinate_ledger_sha256": canonical_digest(ledger),
        "ledger": ledger,
    }


@dataclass(frozen=True)
class JetTT:
    """Interval value, first t/s derivatives and second t derivative."""

    value: arb
    dt: arb
    ds: arb
    dtt: arb = arb(0)

    @classmethod
    def constant(cls, value: Any) -> "JetTT":
        if not isinstance(value, arb):
            value = outer.arbq(Q(value))
        return cls(value, arb(0), arb(0), arb(0))

    @classmethod
    def t_variable(cls, value: arb) -> "JetTT":
        return cls(value, arb(1), arb(0), arb(0))

    @classmethod
    def s_variable(cls, value: arb) -> "JetTT":
        return cls(value, arb(0), arb(1), arb(0))

    def coerce(self, other: Any) -> "JetTT":
        return other if isinstance(other, JetTT) else JetTT.constant(other)

    def __add__(self, other: Any) -> "JetTT":
        other = self.coerce(other)
        return JetTT(self.value + other.value, self.dt + other.dt,
                     self.ds + other.ds, self.dtt + other.dtt)

    __radd__ = __add__

    def __neg__(self) -> "JetTT":
        return JetTT(-self.value, -self.dt, -self.ds, -self.dtt)

    def __sub__(self, other: Any) -> "JetTT":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "JetTT":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "JetTT":
        other = self.coerce(other)
        return JetTT(
            self.value * other.value,
            self.dt * other.value + self.value * other.dt,
            self.ds * other.value + self.value * other.ds,
            self.dtt * other.value + 2 * self.dt * other.dt + self.value * other.dtt,
        )

    __rmul__ = __mul__

    def inverse(self) -> "JetTT":
        if self.value.contains(0):
            raise ValueError("interval inverse crosses zero")
        square = self.value * self.value
        cube = square * self.value
        return JetTT(
            1 / self.value,
            -self.dt / square,
            -self.ds / square,
            2 * self.dt * self.dt / cube - self.dtt / square,
        )

    def __truediv__(self, other: Any) -> "JetTT":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: Any) -> "JetTT":
        return self.coerce(other) / self

    def sqrt(self) -> "JetTT":
        if not bool(self.value > 0):
            raise ValueError("interval square root not strictly positive")
        root = self.value.sqrt()
        return JetTT(
            root,
            self.dt / (2 * root),
            self.ds / (2 * root),
            self.dtt / (2 * root) - self.dt * self.dt / (4 * root * root * root),
        )

    def sin(self) -> "JetTT":
        sine, cosine = self.value.sin(), self.value.cos()
        return JetTT(sine, cosine * self.dt, cosine * self.ds,
                     cosine * self.dtt - sine * self.dt * self.dt)

    def cos(self) -> "JetTT":
        sine, cosine = self.value.sin(), self.value.cos()
        return JetTT(cosine, -sine * self.dt, -sine * self.ds,
                     -sine * self.dtt - cosine * self.dt * self.dt)


def atan2_jettt(y: JetTT, x: JetTT) -> JetTT:
    denominator = x.value * x.value + y.value * y.value
    if denominator.contains(0):
        raise ValueError("atan2 derivative denominator crosses zero")
    numerator = x.value * y.dt - y.value * x.dt
    numerator_t = x.value * y.dtt - y.value * x.dtt
    denominator_t = 2 * (x.value * x.dt + y.value * y.dt)
    return JetTT(
        arb.atan2(y.value, x.value),
        numerator / denominator,
        (x.value * y.ds - y.value * x.ds) / denominator,
        (numerator_t * denominator - numerator * denominator_t) /
        (denominator * denominator),
    )


def critical_discriminant_jettt(
    row: dict[str, Any], box: outer.FutureBox, candidate: str,
) -> JetTT:
    """Evaluate a candidate discriminant with a rigorous second t jet."""

    old_class = outer.Jet2
    old_atan2 = outer.atan2_jet
    try:
        outer.Jet2 = JetTT  # type: ignore[assignment]
        outer.atan2_jet = atan2_jettt  # type: ignore[assignment]
        result = outer.second_geometry(
            row,
            JetTT.t_variable(outer.arb_interval(box.t0, box.t1)),
            JetTT.s_variable(outer.arb_interval(box.s0, box.s1)),
            candidate_only=candidate,
        )["candidates"][candidate]["discriminant"]
        assert isinstance(result, JetTT)
        return result
    finally:
        outer.Jet2 = old_class  # type: ignore[assignment]
        outer.atan2_jet = old_atan2  # type: ignore[assignment]


def critical_candidates(row: dict[str, Any], box: outer.FutureBox) -> list[str]:
    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    centre, interval = outer.geometry_on_box(row, box.t0, box.t1, box.s0, box.s1)
    out = []
    for candidate in sorted(interval["candidates"]):
        d = frozen.enclosure(
            centre["candidates"][candidate]["discriminant"],
            interval["candidates"][candidate]["discriminant"],
            t_radius, s_radius,
        )
        if d.contains(0) and interval["candidates"][candidate]["discriminant"].dt.contains(0):
            out.append(candidate)
    return out


def box_from_record(record: dict[str, Any]) -> outer.FutureBox:
    return outer.FutureBox(
        int(record["row_index"]), Q(record["t"][0]), Q(record["t"][1]),
        Q(record["v"][0]), Q(record["v"][1]),
        int(record["t_depth"]), int(record["v_depth"]),
    )


def critical_resultant_audit(
    rows: list[dict[str, Any]], deep_records: list[dict[str, Any]],
) -> dict[str, Any]:
    critical_records = [
        record for record in deep_records
        if record["terminal_reason"] == "candidate_zero_with_dt_containing_zero"
    ]
    assert len(critical_records) == 12
    witnesses = []
    for record in critical_records:
        row = rows[int(record["row_index"])]
        box = box_from_record(record)
        candidates = critical_candidates(row, box)
        assert candidates
        for candidate in candidates:
            d = critical_discriminant_jettt(row, box, candidate)
            determinant = -(d.ds * d.dtt)
            witnesses.append({
                "row_index": int(record["row_index"]),
                "occurrence_id": record["occurrence_id"],
                "t": record["t"],
                "v": record["v"],
                "candidate": candidate,
                "Delta_enclosure": str(d.value),
                "Delta_t_enclosure": str(d.dt),
                "Delta_s_enclosure": str(d.ds),
                "Delta_tt_enclosure": str(d.dtt),
                "critical_Jacobian_minus_Delta_s_Delta_tt_enclosure": str(determinant),
                "strict_nonzero_on_full_box": not determinant.contains(0),
            })
    witnesses.sort(key=canonical_json)
    strict = sum(w["strict_nonzero_on_full_box"] for w in witnesses)
    return {
        "critical_terminal_box_count": len(critical_records),
        "critical_candidate_witness_count": len(witnesses),
        "strict_full_box_resultant_nonvanishing_count": strict,
        "unresolved_resultant_witness_count": len(witnesses) - strict,
        "all_critical_boxes_regular_value_certified": strict == len(witnesses),
        "critical_witness_ledger_sha256": canonical_digest(witnesses),
        "critical_witnesses": witnesses,
    }


def critical_system_enclosure(
    row: dict[str, Any], box: outer.FutureBox, candidate: str,
) -> tuple[arb, arb, JetTT]:
    ordinary = outer.second_geometry(
        row,
        outer.Jet2.t_variable(outer.arb_interval(box.t0, box.t1)),
        outer.Jet2.s_variable(outer.arb_interval(box.s0, box.s1)),
        candidate_only=candidate,
    )["candidates"][candidate]["discriminant"]
    second = critical_discriminant_jettt(row, box, candidate)
    return ordinary.value, ordinary.dt, second


def refine_one_critical_candidate(
    row_index: int, row: dict[str, Any], initial: outer.FutureBox,
    candidate: str, *, additional_t: int = 5, additional_v: int = 5,
) -> dict[str, Any]:
    """Cover the simultaneous system ``(Delta,Delta_t)=0`` fail-closed."""

    queue = [initial]
    regular: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    calls = 0
    while queue:
        box = queue.pop()
        calls += 1
        try:
            delta, delta_t, d = critical_system_enclosure(row, box, candidate)
            if not delta.contains(0):
                excluded.append({
                    **box_record(row_index, row, box),
                    "exclusion": "Delta_strict_sign",
                    "Delta": str(delta),
                })
                continue
            if not delta_t.contains(0):
                dt_lower = min(abs(delta_t.lower()), abs(delta_t.upper()))
                ds_upper = max(abs(d.ds.lower()), abs(d.ds.upper()))
                slope_ball = (ds_upper / dt_lower / 200).upper().ceil()
                slope_fmpz = slope_ball.unique_fmpz()
                assert slope_fmpz is not None
                excluded.append({
                    **box_record(row_index, row, box),
                    "exclusion": "Delta_t_strict_sign",
                    "Delta_t": str(delta_t),
                    "possibly_empty_transverse_zero_graph": True,
                    "normalized_dt_dv_absolute_slope_integer_upper": int(slope_fmpz),
                })
                continue
            determinant = -(d.ds * d.dtt)
            if not determinant.contains(0):
                regular.append({
                    **box_record(row_index, row, box),
                    "candidate": candidate,
                    "Delta": str(delta),
                    "Delta_t": str(delta_t),
                    "Delta_s": str(d.ds),
                    "Delta_tt": str(d.dtt),
                    "minus_Delta_s_Delta_tt": str(determinant),
                    "regular_fold_cover": True,
                    "fixed_s_zero_count_upper_on_this_convex_leaf": 2,
                })
                continue
        except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
            d = None
            determinant = None
            exception = type(exc).__name__
        else:
            exception = None

        can_t = box.t_depth < initial.t_depth + additional_t
        can_v = box.v_depth < initial.v_depth + additional_v
        if can_t or can_v:
            # Alternate the normalized refinements, preferring the coordinate
            # with fewer added levels.  This is deterministic and makes no
            # inference from a non-strict interval.
            added_t = box.t_depth - initial.t_depth
            added_v = box.v_depth - initial.v_depth
            if can_t and (not can_v or added_t <= added_v):
                queue.extend(reversed(box.split_t()))
            else:
                queue.extend(reversed(box.split_v()))
            continue
        unresolved.append({
            **box_record(row_index, row, box),
            "candidate": candidate,
            "exception": exception,
            "Delta_s": None if d is None else str(d.ds),
            "Delta_tt": None if d is None else str(d.dtt),
            "minus_Delta_s_Delta_tt": None if determinant is None else str(determinant),
        })

    regular.sort(key=canonical_json)
    excluded.sort(key=canonical_json)
    unresolved.sort(key=canonical_json)
    return {
        "row_index": row_index,
        "candidate": candidate,
        "initial_box": box_record(row_index, row, initial),
        "audit_call_count": calls,
        "regular_fold_leaf_count": len(regular),
        "excluded_leaf_count": len(excluded),
        "Delta_strict_excluded_leaf_count": sum(
            leaf["exclusion"] == "Delta_strict_sign" for leaf in excluded
        ),
        "transverse_candidate_graph_leaf_count": sum(
            leaf["exclusion"] == "Delta_t_strict_sign" for leaf in excluded
        ),
        "transverse_candidate_graph_normalized_slope_sum_upper": sum(
            leaf.get("normalized_dt_dv_absolute_slope_integer_upper", 0)
            for leaf in excluded
        ),
        "unresolved_leaf_count": len(unresolved),
        "maximum_additional_t_depth": additional_t,
        "maximum_additional_v_depth": additional_v,
        "regular_fold_fixed_s_zero_count_upper": 2 * len(regular),
        "regular_leaf_ledger_sha256": canonical_digest(regular),
        "excluded_leaf_ledger_sha256": canonical_digest(excluded),
        "unresolved_leaf_ledger_sha256": canonical_digest(unresolved),
        "regular_leaves": regular,
        "unresolved_leaves": unresolved,
    }


def endpoint_scaled_proof_for_box(
    row_index: int, row: dict[str, Any], box: outer.FutureBox,
) -> dict[str, Any] | None:
    """Return the containing canonical endpoint witness, if there is one."""

    band = source_band_descriptor(row_index, row)
    if band is None:
        return None
    b0, b1 = map(Q, band["t"])
    if not (b0 <= box.t0 < box.t1 <= b1):
        return None
    parent_index = int(box.v0 * 64)
    v0, v1 = Q(parent_index, 64), Q(parent_index + 1, 64)
    if not (v0 <= box.v0 < box.v1 <= v1):
        return None
    s0 = outer.S_LOWER + (outer.S_UPPER - outer.S_LOWER) * v0
    s1 = outer.S_LOWER + (outer.S_UPPER - outer.S_LOWER) * v1
    witness = previous.source_grazing_endpoint_scaled_cp(
        row, band["side"], s0, s1, Q(1, 1024)
    )
    assert witness["source_cp_strict_sign_from_separate_factors"] == 1
    return {
        "canonical_side": band["side"],
        "canonical_t_band": band["t"],
        "canonical_v_cell": [str(v0), str(v1)],
        "box_t": [str(box.t0), str(box.t1)],
        "box_v": [str(box.v0), str(box.v1)],
        "coordinatewise_containment": True,
        "endpoint_witness_digest": canonical_digest(witness),
    }


def call_with_source_cp_override(
    function: Any, row: dict[str, Any], box: outer.FutureBox,
) -> Any:
    """Run one frozen box routine after a certified local source-cp override.

    The monkeypatch is process-local and active only during the synchronous
    call.  It changes no frozen source file.  All non-source fields are the
    exact frozen interval fields; only ``source_cp`` is replaced by the exact
    positive constant one after containment has already been certified.
    """

    original = outer.geometry_on_box

    def patched(
        candidate_row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        centre, interval = original(candidate_row, t0, t1, s0, s1)
        if candidate_row is row and (t0, t1, s0, s1) == (box.t0, box.t1, box.s0, box.s1):
            centre = dict(centre)
            interval = dict(interval)
            centre["source_cp"] = outer.Jet2.constant(1)
            interval["source_cp"] = outer.Jet2.constant(1)
        return centre, interval

    outer.geometry_on_box = patched  # type: ignore[assignment]
    try:
        return function(row, box)
    finally:
        outer.geometry_on_box = original  # type: ignore[assignment]


def reclassify_one_source_record(
    row: dict[str, Any], record: dict[str, Any],
) -> dict[str, Any]:
    box = box_from_record(record)
    proof = endpoint_scaled_proof_for_box(int(record["row_index"]), row, box)
    assert proof is not None
    status, witness = call_with_source_cp_override(outer.audit_box, row, box)
    base = {
        **box_record(int(record["row_index"]), row, box),
        "source_override_proof_digest": canonical_digest(proof),
        "post_override_outer_status": status,
    }
    if status == "immutable":
        return {
            **base,
            "classification": "immutable_owner_component",
            "classification_witness_digest": canonical_digest(witness),
        }
    if status == "transverse_root_strip":
        candidate = witness["candidate_relative_to_miss_source"]
        ok, typed = frozen.physical_first_witness(row, box, candidate)
        if ok:
            return {
                **base,
                "classification": "conditionally_physical_first_graph",
                "candidate": candidate,
                "nonempty_root_arc": True,
                "normalized_slope_upper": typed[
                    "normalized_dt_dv_absolute_slope_integer_upper"
                ],
                "dt_sign": typed["dt_discriminant_strict_sign"],
                "classification_witness_digest": canonical_digest({**witness, **typed}),
            }
        return {
            **base,
            "classification": "untyped_transverse_candidate_graph",
            "candidate": candidate,
            "classification_witness_digest": canonical_digest({**witness, **typed}),
        }

    reason = witness.get("reason", status)
    if reason == "transverse_candidate_not_bracketed_on_full_s_slab":
        candidate = witness.get("candidate_relative_to_miss_source")
        if isinstance(candidate, str):
            ok, typed = frozen.physical_first_witness(row, box, candidate)
            if ok:
                return {
                    **base,
                    "classification": "conditionally_physical_first_graph",
                    "candidate": candidate,
                    "nonempty_root_arc": False,
                    "normalized_slope_upper": typed[
                        "normalized_dt_dv_absolute_slope_integer_upper"
                    ],
                    "dt_sign": typed["dt_discriminant_strict_sign"],
                    "classification_witness_digest": canonical_digest({**witness, **typed}),
                }
    covered, graphs, summary = call_with_source_cp_override(
        frozen.candidate_graph_cover, row, box
    )
    if covered:
        return {
            **base,
            "classification": "untyped_candidate_graph_cover",
            "candidate_graph_count": len(graphs),
            "normalized_slope_sum": sum(
                graph["normalized_dt_dv_absolute_slope_integer_upper"]
                for graph in graphs
            ),
            "classification_witness_digest": canonical_digest({
                "outer": witness, "graphs": graphs, "summary": summary,
            }),
        }
    return {
        **base,
        "classification": "positive_width_terminal_retained",
        "terminal_reason": summary.get("graph_cover_failure", reason),
        "classification_witness_digest": canonical_digest({
            "outer": witness, "summary": summary,
        }),
    }


def sweep_added_physical(records: list[dict[str, Any]]) -> dict[str, Any]:
    events: dict[Q, Counter[str]] = {}
    for record in records:
        if record["classification"] != "conditionally_physical_first_graph":
            continue
        v0, v1 = map(Q, record["v"])
        slope = int(record["normalized_slope_upper"])
        for endpoint, sign in ((v0, 1), (v1, -1)):
            event = events.setdefault(endpoint, Counter())
            event["count"] += sign
            event["slope_sum"] += sign * slope
    maxima, closed = frozen.sweep_maxima(events)
    return {
        "maximum_added_graph_count_on_one_fixed_s_slice": int(maxima.get("count", 0)),
        "maximum_added_normalized_slope_sum_on_one_fixed_s_slice": int(
            maxima.get("slope_sum", 0)
        ),
        "closed_v1_added_graph_count": int(closed.get("count", 0)),
        "closed_v1_added_slope_sum": int(closed.get("slope_sum", 0)),
    }


def source_downstream_reclassification(
    rows: list[dict[str, Any]], deep_records: list[dict[str, Any]],
) -> dict[str, Any]:
    source = [
        record for record in deep_records
        if record["terminal_reason"] == "source_cp_not_strict"
    ]
    workers = min(int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64)
    tasks = [(rows[int(record["row_index"])], record) for record in source]
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        classified = list(pool.imap_unordered(
            _reclassify_source_task, tasks, chunksize=4
        ))
    classified.sort(key=canonical_json)
    counts = Counter(record["classification"] for record in classified)
    retained = [
        record for record in classified
        if record["classification"] == "positive_width_terminal_retained"
    ]
    physical = sweep_added_physical(classified)

    # Freeze the exact source width sweep independently of the frozen
    # aggregate maximum.  A constant value makes a later subtraction from
    # the simultaneous terminal union legitimate if and only if no source
    # terminal survives downstream classification.
    events: dict[Q, Counter[str]] = {}
    for record in source:
        v0, v1 = map(Q, record["v"])
        width = Q(record["t"][1]) - Q(record["t"][0])
        for endpoint, sign in ((v0, 1), (v1, -1)):
            events.setdefault(endpoint, Counter())["width"] += sign * width
    maxima, closed = frozen.sweep_maxima(events)
    # Every open slab and the closed final endpoint have the same source
    # width.  The event sweep maximum plus the explicit endpoint value is a
    # compact machine-checkable proxy for that exhaustive ledger property.
    source_width = Q(maxima.get("width", 0))
    assert source_width == Q(1, 128)
    assert Q(closed.get("width", 0)) == source_width
    return {
        "input_deep_source_tagged_record_count": len(source),
        "classification_counts": dict(sorted(counts.items())),
        "positive_width_terminal_retained_count": len(retained),
        "all_deep_source_tagged_records_downstream_classified_without_positive_width_terminal": not retained,
        "uniform_source_terminal_width_before_override": str(source_width),
        "closed_v1_source_terminal_width_before_override": str(closed.get("width", 0)),
        **physical,
        "classified_record_ledger_sha256": canonical_digest(classified),
        "retained_terminal_ledger_sha256": canonical_digest(retained),
        "classified_records": classified,
    }


def _reclassify_source_task(
    task: tuple[dict[str, Any], dict[str, Any]],
) -> dict[str, Any]:
    return reclassify_one_source_record(*task)


def _targeted_source_row(
    task: tuple[int, dict[str, Any], int, int],
) -> list[dict[str, Any]]:
    row_index, row, t_depth, v_depth = task
    t_leaf_width = Q(1, outer.INITIAL_T_CELLS * 2 ** t_depth)
    v_cells = outer.INITIAL_V_CELLS * 2 ** v_depth
    records: list[dict[str, Any]] = []
    band = source_band_descriptor(row_index, row)
    if band is None:
        return records
    b0, b1 = map(Q, band["t"])
    t_leaf_count = int((b1 - b0) / t_leaf_width)
    assert t_leaf_count in {1, 2}
    for ti in range(t_leaf_count):
        t0, t1 = b0 + ti * t_leaf_width, b0 + (ti + 1) * t_leaf_width
        for vi in range(v_cells):
            box = outer.FutureBox(
                row_index, t0, t1, Q(vi, v_cells), Q(vi + 1, v_cells),
                t_depth, v_depth,
            )
            status, witness = outer.audit_box(row, box)
            reason = witness.get("reason", status)
            if reason != "source_cp_not_strict":
                continue
            covered, _graphs, summary = frozen.candidate_graph_cover(row, box)
            assert not covered
            assert summary.get("graph_cover_failure") == "source_cp_not_strict"
            records.append({
                **box_record(row_index, row, box),
                "terminal_status": status,
                "terminal_reason": "source_cp_not_strict",
                "outer_witness_digest": canonical_digest(witness),
                "graph_summary_digest": canonical_digest(summary),
            })
    return records


def targeted_source_terminal_records(
    rows: list[dict[str, Any]], *, t_depth: int, v_depth: int,
) -> list[dict[str, Any]]:
    """Enumerate only dyadic leaves inside the 24 canonical source bands."""

    assert (t_depth, v_depth) in {(5, 3), (6, 4)}
    tasks = [
        (index, row, t_depth, v_depth)
        for index, row in enumerate(rows)
        if source_band_descriptor(index, row) is not None
    ]
    workers = min(int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, len(tasks))
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        parts = list(pool.imap_unordered(_targeted_source_row, tasks, chunksize=1))
    records = [record for part in parts for record in part]
    records.sort(key=canonical_json)
    expected = 1536 if (t_depth, v_depth) == (5, 3) else 2048
    assert len(records) == expected
    return records


def latest_technology_applicability_audit() -> dict[str, Any]:
    """Freeze the no-bridge audit for arXiv:2607.13785v1."""

    return {
        "arxiv_id": "2607.13785v1",
        "title": "Local Uniform Finite Cyclicity of the H_14^3 Semihyperbolic Hemicycle",
        "author": "Haibo Lu",
        "official_arxiv_updated_utc": "2026-07-15T12:41:34Z",
        "relevant_results": [
            "Proposition 4 (Three-box stopped-return principle)",
            "Proposition 8 (Uniform stopped first-hit theorem)",
            "Theorem 10 (Finite stopped word theorem)",
        ],
        "fatal_hypothesis_mismatches": [
            "analytic planar ODE flow boxes and Dulac equations, not a singular billiard collision map",
            "strict flow/Lyapunov coordinate and a finite equilibrium/sector alphabet are assumed and H_14-specific",
            "each labelled corner orbit or invariant half-branch must meet an incoming arc at most once",
            "root-scale zero theorems count zeros of retained analytic return words and do not interval-certify Delta/Delta_t regular values",
            "the paper explicitly disclaims finite-component control for arbitrary transported finite-smooth faces",
            "the final cyclicity bound is existential and supplies no numerical owner/current/DQ constants",
        ],
        "direct_lemma_for_twelve_billiard_resultant_boxes": False,
        "direct_lemma_for_interval_physical_first_owner_typing": False,
        "strategy_analogy_only": True,
        "used_to_remove_or_reclassify_any_box": False,
    }


def critical_terminal_box_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    high_t = ["2039/2048", "255/256"]
    low_t = ["1/256", "9/2048"]
    upper_v = [
        ["33/64", "67/128"],
        ["67/128", "17/32"],
        ["17/32", "69/128"],
    ]
    lower_v = [
        ["59/128", "15/32"],
        ["15/32", "61/128"],
        ["61/128", "31/64"],
    ]
    for row_index, t, slabs in (
        (3, high_t, upper_v),
        (41, low_t, upper_v),
        (20, high_t, lower_v),
        (46, low_t, lower_v),
    ):
        for v in slabs:
            specs.append({"row_index": row_index, "t": t, "v": v})
    specs.sort(key=canonical_json)
    assert len(specs) == 12
    return specs


def critical_box_from_spec(spec: dict[str, Any]) -> outer.FutureBox:
    return outer.FutureBox(
        int(spec["row_index"]), Q(spec["t"][0]), Q(spec["t"][1]),
        Q(spec["v"][0]), Q(spec["v"][1]), 6, 4,
    )


def critical_refinement_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    box_ledger: list[dict[str, Any]] = []
    tasks = []
    for spec in critical_terminal_box_specs():
        row_index = int(spec["row_index"])
        row = rows[row_index]
        box = critical_box_from_spec(spec)
        status, outer_witness = outer.audit_box(row, box)
        covered, _graphs, summary = frozen.candidate_graph_cover(row, box)
        assert not covered
        assert summary.get("graph_cover_failure") == "candidate_zero_with_dt_containing_zero"
        candidates = critical_candidates(row, box)
        assert candidates
        box_ledger.append({
            **spec,
            "outer_status": status,
            "candidate_count": len(candidates),
            "candidate_ledger_sha256": canonical_digest(candidates),
            "outer_witness_sha256": canonical_digest(outer_witness),
            "graph_summary_sha256": canonical_digest(summary),
        })
        tasks.extend((row_index, row, box, candidate) for candidate in candidates)
    assert len(tasks) == 444
    workers = min(int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64)
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        full = list(pool.starmap(
            refine_one_critical_candidate, tasks, chunksize=1
        ))
    summaries = [
        {
            key: item[key]
            for key in (
                "row_index", "candidate", "initial_box", "audit_call_count",
                "regular_fold_leaf_count", "excluded_leaf_count",
                "Delta_strict_excluded_leaf_count",
                "transverse_candidate_graph_leaf_count",
                "transverse_candidate_graph_normalized_slope_sum_upper",
                "unresolved_leaf_count", "maximum_additional_t_depth",
                "maximum_additional_v_depth",
                "regular_fold_fixed_s_zero_count_upper",
                "regular_leaf_ledger_sha256", "excluded_leaf_ledger_sha256",
                "unresolved_leaf_ledger_sha256",
            )
        }
        for item in full
    ]
    assert sum(item["unresolved_leaf_count"] for item in full) == 0
    assert sum(item["regular_fold_leaf_count"] for item in full) == 0
    result = {
        "critical_terminal_box_count": len(box_ledger),
        "coarse_possible_critical_candidate_count": len(tasks),
        "refinement_audit_call_count": sum(item["audit_call_count"] for item in full),
        "Delta_strict_excluded_leaf_count": sum(
            item["Delta_strict_excluded_leaf_count"] for item in full
        ),
        "transverse_candidate_graph_leaf_count": sum(
            item["transverse_candidate_graph_leaf_count"] for item in full
        ),
        "transverse_candidate_graph_normalized_slope_sum_upper": sum(
            item["transverse_candidate_graph_normalized_slope_sum_upper"]
            for item in full
        ),
        "regular_fold_leaf_count": 0,
        "unresolved_critical_leaf_count": 0,
        "all_coarse_critical_boxes_replaced_by_Delta_exclusions_or_strict_dt_graphs": True,
        "no_simultaneous_Delta_Delta_t_zero_on_the_twelve_boxes": True,
        "critical_box_ledger_sha256": canonical_digest(box_ledger),
        "critical_task_summary_ledger_sha256": canonical_digest(summaries),
        "complete_refinement_ledger_sha256": canonical_digest(full),
        "box_ledger": box_ledger,
        "task_summaries": summaries,
    }
    return result


def build_diagnostic() -> dict[str, Any]:
    rows, provenance = frozen.load_dependencies()
    old = replay_terminal_records(rows, 5, 3)
    deep = replay_terminal_records(rows, 6, 4)
    assert old["reason_counts"] == {
        "candidate_zero_with_dt_containing_zero": 11884,
        "interval_geometry_exception": 79660,
        "source_cp_not_strict": 1536,
    }


def build_result() -> dict[str, Any]:
    previous_wrapper = json.loads(PREVIOUS_MANIFEST.read_text(encoding="utf-8"))
    previous_result = previous_wrapper["result"]
    previous_deep = previous_result["deeper_selective_frontier"]
    assert previous_wrapper["verdict"]["gate3"] == "NOT_CERTIFIED"
    assert previous_deep["terminal_reason_counts"] == {
        "candidate_zero_with_dt_containing_zero": 12,
        "interval_geometry_exception": 151500,
        "source_cp_not_strict": 2048,
    }

    rows, provenance = frozen.load_dependencies()
    old_source_records = targeted_source_terminal_records(
        rows, t_depth=5, v_depth=3
    )
    deep_source_records = targeted_source_terminal_records(
        rows, t_depth=6, v_depth=4
    )
    assert canonical_digest(old_source_records) == (
        "6958598bb8c8e4d7a3b80c4c0674d7cd96c8e196905695f155ea5eb082d458e2"
    )
    assert canonical_digest(deep_source_records) == (
        "8cce8a761c621abab3e6666aa2a2745a06ae97cdfaa236367a6319c4ccc90efc"
    )
    old_containment_full = source_containment_ledger(
        rows, old_source_records, deep=False
    )
    deep_containment_full = source_containment_ledger(
        rows, deep_source_records, deep=True
    )
    old_containment = {
        key: value for key, value in old_containment_full.items() if key != "ledger"
    }
    deep_containment = {
        key: value for key, value in deep_containment_full.items() if key != "ledger"
    }
    old_parent_coordinates = {
        (record["row_index"], tuple(record["t"]), tuple(record["v"]))
        for record in old_source_records
    }
    parent_counts: Counter[tuple[Any, ...]] = Counter()
    parent_links = []
    for record in deep_containment_full["ledger"]:
        parent = (
            record["row_index"], tuple(record["containing_canonical_t_band"]),
            tuple(record["containing_canonical_v_cell"]),
        )
        assert parent in old_parent_coordinates
        parent_counts[parent] += 1
        parent_links.append({
            "deep_row_index": record["row_index"],
            "deep_t": record["record_t"],
            "deep_v": record["record_v"],
            "unique_old_parent": [
                record["row_index"], record["containing_canonical_t_band"],
                record["containing_canonical_v_cell"],
            ],
        })
    parent_links.sort(key=canonical_json)
    assert len(parent_counts) == 1024
    assert set(parent_counts.values()) == {2}
    source_reclassification_full = source_downstream_reclassification(
        rows, deep_source_records
    )
    source_reclassification = {
        key: value for key, value in source_reclassification_full.items()
        if key != "classified_records"
    }
    assert source_reclassification["classification_counts"] == {
        "immutable_owner_component": 2048
    }
    assert source_reclassification["classified_record_ledger_sha256"] == (
        "2bf469f35f5ee515614321c52668e9bc42d57af4010e8d9ad1663d628c1d3f05"
    )

    critical_full = critical_refinement_audit(rows)
    critical = {
        key: value for key, value in critical_full.items()
        if key not in {"box_ledger", "task_summaries"}
    }
    assert critical == {
        "critical_terminal_box_count": 12,
        "coarse_possible_critical_candidate_count": 444,
        "refinement_audit_call_count": 3196,
        "Delta_strict_excluded_leaf_count": 932,
        "transverse_candidate_graph_leaf_count": 888,
        "transverse_candidate_graph_normalized_slope_sum_upper": 888,
        "regular_fold_leaf_count": 0,
        "unresolved_critical_leaf_count": 0,
        "all_coarse_critical_boxes_replaced_by_Delta_exclusions_or_strict_dt_graphs": True,
        "no_simultaneous_Delta_Delta_t_zero_on_the_twelve_boxes": True,
        "critical_box_ledger_sha256": "840396efa624a92beb9f4fb351bd5af20d29af8a15e2c5024fe37e9c20f6264d",
        "critical_task_summary_ledger_sha256": "c4fa88af353a887918052e6a5d3c023cdfe9e6cd6ea4957920aa0d49ce639f0c",
        "complete_refinement_ledger_sha256": "9ff1368a866fe7805c5037542b05683885d2f23e93c66dc305ded845c103bb62",
    }

    old_candidate_max = int(
        previous_deep["maximum_candidate_graph_charts_on_one_fixed_s_slice"]
    )
    old_candidate_slope = int(
        previous_deep[
            "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
        ]
    )
    candidate_max = old_candidate_max + critical[
        "transverse_candidate_graph_leaf_count"
    ]
    candidate_slope = old_candidate_slope + critical[
        "transverse_candidate_graph_normalized_slope_sum_upper"
    ]
    assert candidate_max == 1480 and candidate_slope == 52292
    assert Q(previous_deep["uniform_fixed_s_terminal_positive_t_width_outer"]) == Q(603, 1024)
    remaining_width = Q(603, 1024) - Q(
        source_reclassification["uniform_source_terminal_width_before_override"]
    )
    assert remaining_width == Q(595, 1024)
    # Removing the twelve critical rectangles cannot lower the final value
    # below this number: the interval-exception reason alone already attains
    # the same frozen fixed-s maximum.
    assert Q(
        previous_deep["uniform_fixed_s_terminal_reason_t_width_outers"][
            "interval_geometry_exception"
        ]
    ) == remaining_width

    result = {
        "schema": "cm2.gate3.deep-scaled-resultant-frontier.v1",
        "provenance": {
            "frozen_fourteenth_manifest_sha256": file_sha256(PREVIOUS_MANIFEST),
            "frozen_fourteenth_certificate_sha256": file_sha256(Path(previous.__file__).resolve()),
            "frozen_fourteenth_internal_replay_digest": previous_result[
                "internal_replay_digest"
            ],
            "maximal_row_registry_sha256": provenance["maximal_row_registry_sha256"],
            "arithmetic_precision_bits": 384,
        },
        "old_source_terminal_coordinate_ledger": {
            **old_containment,
            "targeted_terminal_record_ledger_sha256": canonical_digest(
                old_source_records
            ),
        },
        "deep_source_terminal_coordinate_ledger": {
            **deep_containment,
            "targeted_terminal_record_ledger_sha256": canonical_digest(
                deep_source_records
            ),
            "deep_record_to_unique_old_parent_containment_certified": True,
            "old_parent_with_deep_source_children_count": len(parent_counts),
            "deep_source_children_per_such_old_parent": 2,
            "parent_child_ledger_sha256": canonical_digest(parent_links),
        },
        "deep_source_downstream_reclassification": source_reclassification,
        "critical_resultant_refinement": critical,
        "updated_outer_frontier": {
            "positive_width_terminal_reason_counts": {
                "interval_geometry_exception": 151500,
            },
            "positive_width_terminal_box_count": 151500,
            "positive_width_terminal_nonphysical_parameter_area_upper_cover": "37875/65536",
            "uniform_fixed_s_positive_t_width_outer": str(remaining_width),
            "source_terminal_width_removed_after_exact_containment_and_reclassification": "1/128",
            "critical_positive_width_terminal_boxes_removed_after_exhaustive_refinement": 12,
            "zero_intercept_complete_future_boundary": False,
        },
        "expanded_candidate_graph_atlas": {
            "frozen_conditionally_physical_first_graph_chart_count": previous_deep[
                "conditionally_physical_first_graph_chart_count"
            ],
            "frozen_nonempty_physical_first_root_arc_count": previous_deep[
                "nonempty_physical_first_root_arc_count"
            ],
            "frozen_untyped_candidate_graph_chart_count": previous_deep[
                "untyped_candidate_graph_chart_count"
            ],
            "new_untyped_transverse_candidate_graph_leaf_count": critical[
                "transverse_candidate_graph_leaf_count"
            ],
            "combined_untyped_candidate_graph_chart_count": (
                int(previous_deep["untyped_candidate_graph_chart_count"])
                + critical["transverse_candidate_graph_leaf_count"]
            ),
            "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": candidate_max,
            "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": candidate_slope,
            "safe_uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient": str(
                2 * candidate_max
            ),
            "safe_uniform_fixed_s_actual_candidate_zero_set_row_law_Z_linear_coefficient": str(
                Q(252, 5) * candidate_max
            ),
            "new_critical_graphs_are_physical_first_typed": False,
            "partial_genuine_physical_marked_current_TV_upper_unchanged": previous_deep[
                "partial_genuine_physical_marked_current_TV_upper"
            ],
        },
        "latest_technology_applicability_audit": latest_technology_applicability_audit(),
        "scope_limits": {
            "old_source_record_coordinatewise_containment": True,
            "deep_source_record_coordinatewise_containment": True,
            "deep_source_downstream_immutable_reclassification": True,
            "all_twelve_coarse_critical_boxes_resolved_to_transverse_graph_atlas": True,
            "all_simultaneous_Delta_Delta_t_critical_zeros_excluded": True,
            "interval_geometry_exception_boxes_resolved": False,
            "all_candidate_graph_charts_typed_physical_first": False,
            "complete_side_owner_current": False,
            "strong_component_restriction_DQ": False,
            "branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            "resolve the 151,500 interval-geometry outer boxes in cancellation-free miss-discriminant/root-gap/candidate coordinates",
            "type the 164 frozen and 888 newly refined untyped candidate graph charts by a unique physical-first miss-side owner",
            "assemble the complete side-owner current with coefficient partial_s_Delta/abs(partial_t_Delta)",
            "prove strong component restriction DQ, branch-record MT_DQ, FACE_2CUT, and FACE_TIME",
        ],
    }
    assert result["expanded_candidate_graph_atlas"][
        "combined_untyped_candidate_graph_chart_count"
    ] == 1052
    assert result["expanded_candidate_graph_atlas"][
        "safe_uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient"
    ] == "2960"
    assert result["expanded_candidate_graph_atlas"][
        "safe_uniform_fixed_s_actual_candidate_zero_set_row_law_Z_linear_coefficient"
    ] == "74592"
    result["internal_replay_digest"] = canonical_digest(result)
    return result
    assert deep["reason_counts"] == {
        "candidate_zero_with_dt_containing_zero": 12,
        "interval_geometry_exception": 151500,
        "source_cp_not_strict": 2048,
    }
    old_source = source_containment_ledger(rows, old["records"], deep=False)
    deep_source = source_containment_ledger(rows, deep["records"], deep=True)
    critical = critical_resultant_audit(rows, deep["records"])
    return {
        "schema": "cm2.gate3.deep-scaled-resultant-diagnostic.v1",
        "provenance": provenance,
        "old_terminal": {
            key: value for key, value in old.items() if key != "records"
        },
        "deep_terminal": {
            key: value for key, value in deep.items() if key != "records"
        },
        "old_source_containment": {
            key: value for key, value in old_source.items() if key != "ledger"
        },
        "deep_source_containment": {
            key: value for key, value in deep_source.items() if key != "ledger"
        },
        "critical_resultants": critical,
        "deep_source_records": [
            record for record in deep["records"]
            if record["terminal_reason"] == "source_cp_not_strict"
        ],
        "deep_interval_records": [
            record for record in deep["records"]
            if record["terminal_reason"] == "interval_geometry_exception"
        ],
        "internal_replay_digest": "diagnostic-only",
    }


if __name__ == "__main__":
    print(json.dumps(build_result(), sort_keys=True, indent=2))
