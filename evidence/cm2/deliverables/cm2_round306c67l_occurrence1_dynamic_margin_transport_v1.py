#!/usr/bin/env python3
"""C67-L: full-atom occurrence-1 dynamic margin transport, zero credit.

The computation does not consume the boolean conclusions of C57-L1.  It
reconstructs the first collision on each of the 26,206 atom incidences from
the frozen Gate-3 target registry.  Rational faces are evaluated exactly in
Arb; the four source seams use the pinned isolating intervals and the exact
root of 2*x^2-1.  Every result remains a non-authoritative, zero-credit
candidate.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
if str(OUT) not in sys.path:
    sys.path.insert(0, str(OUT))

import cm2_gate3_candidate_first_hit_cert as GATE3
import cm2_round117_rank3_countable_homogeneity_operator_cells as HOM
import cm2_round128_base_r1_component_global_word_incidence as CORES

PREFIX = "cm2_round306c67l_occurrence1_dynamic_margin_transport"
SCHEMA = "cm2.round306c67l.occurrence1-dynamic-margin-transport.v1"
ENDPOINT_FILE = PREFIX + "_endpoint_occurrence_margins_v1.jsonl.gz"
ATOM_FILE = PREFIX + "_atom_coverage_v1.jsonl.gz"
EDGE_FILE = PREFIX + "_edge_coverage_v1.jsonl.gz"
CORRIDOR_FILE = PREFIX + "_corridor_coverage_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANON = OUT / "CM2_LATEST_STATUS.md"
C57R = OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json"
C57E = OUT / "cm2_round306c57l1_collision1_edgewise_transport_edge_obligations_v1.jsonl.gz"
C57C = OUT / "cm2_round306c57l1_collision1_edgewise_transport_corridor_cell_transport_v1.jsonl.gz"
C57M = OUT / "cm2_round306c57l1_collision1_edgewise_transport_manifest_v1.sha256"
C60R = OUT / "cm2_round306c60l_static_edge_owner_result_v1.json"
C60A = OUT / "cm2_round306c60l_static_edge_owner_incidence_atoms_v1.jsonl.gz"
C60E = OUT / "cm2_round306c60l_static_edge_owner_edge_decisions_v1.jsonl.gz"
C60M = OUT / "cm2_round306c60l_static_edge_owner_manifest_v1.sha256"
C63R = OUT / "cm2_round306c63l_scope_extension_result_v1.json"
C63A = OUT / "cm2_round306c63l_scope_extension_atom_replay_v1.jsonl.gz"
C63M = OUT / "cm2_round306c63l_scope_extension_manifest_v1.sha256"

PINS = {
    str(C35 / "result.json"): "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    str(C35 / "path_occurrences.jsonl.gz"): "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    str(C36 / "result.json"): "7922139708dc486232ec79b29d6339bdca7e00999bddf63d5b9a83b3f4cfbbd1",
    str(C36 / "occurrence_margin_bindings.jsonl.gz"): "2a5f050ddf86936ab87e9b6489fd92639d071230d2d8341c7fc94495490ff1c5",
    str(C32 / "result.json"): "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4",
    str(C32 / "compact_cells.jsonl.gz"): "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8",
    str(C32 / "source_chart_seams.jsonl.gz"): "d7b5e689baa36d6d0502d3a7c9dad3188d5b92c11e7223c502277057304a611e",
    str(C41 / "result.json"): "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    str(C41 / "routed_ambient_cells.jsonl.gz"): "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
    str(C57R): "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    str(C57E): "7136dd4585a5ed9de158c0710c6386ece4d8870ab0196db2e373881779c3dbcd",
    str(C57C): "3f61330c3eafa9101b083b8b6061ee334738bfa3129280874e1a3f7d239e1ac5",
    str(C57M): "b66325f26f39b1e4e3b1027d331105e1be9e76c126fa32210a614313e587f281",
    str(C60R): "c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315",
    str(C60A): "4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6",
    str(C60E): "63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8",
    str(C60M): "669938c6f32f45a2a814c8682ca7bb7fea5ba3ff424a364588d0cbbb038aabcf",
    str(C63R): "4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177",
    str(C63A): "09fad1b51e03a3c44702aed07176da6f06e85b95320806fa45073158c2b00734",
    str(C63M): "56ee86ca5e82d09b80c280eb44187422d1d4c21b4fda8150b21be889d7107290",
    str(OUT / "cm2_gate3_candidate_first_hit_cert.py"): "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    str(OUT / "cm2_round128_base_r1_component_global_word_incidence.py"): "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
    str(OUT / "cm2_round117_rank3_countable_homogeneity_operator_cells.py"): "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c",
    str(C53): "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    str(CANON): "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

FROZEN_OWNER = "W[1,0]"
SOURCE_OWNER = "W[0,0]"
CHARTS = ("E", "N", "S")
MARGIN_FIELDS = (
    "retained_candidate_minimum_decision_margin_dyadic_depth",
    "retained_candidate_minimum_winner_gap_dyadic_depth",
    "full_radius4_candidate_minimum_decision_margin_dyadic_depth",
    "full_radius4_candidate_minimum_winner_gap_dyadic_depth",
    "official_wall_crossing_time_endpoint_margin_dyadic_depth",
    "official_wall_endpoint_integer_margin_dyadic_depth",
    "official_wall_event_order_gap_dyadic_depth",
    "outgoing_chart_margin_dyadic_depth",
    "C24_minimum_inside_or_exclusion_margin_dyadic_depth",
    "homogeneity_lower_margin_dyadic_depth",
    "homogeneity_upper_margin_dyadic_depth",
)


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def bounds(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def aq(value: Q | int) -> arb:
    return GATE3.arbq(Q(value))


def interval(lower: Q, upper: Q) -> arb:
    return GATE3.arb_interval(lower, upper)


def intersect(left: arb, right: arb) -> arb:
    ll, lu = bounds(left)
    rl, ru = bounds(right)
    lower, upper = max(ll, rl), min(lu, ru)
    need(lower <= upper, "equivalent interval representations intersect")
    return interval(lower, upper)


def power2(exponent: int) -> Q:
    return Q(2**exponent) if exponent >= 0 else Q(1, 2 ** (-exponent))


def strict_depth(lower: Q) -> int:
    need(lower > 0, "positive directed lower")
    exponent = lower.numerator.bit_length() - lower.denominator.bit_length()
    while power2(exponent) > lower:
        exponent -= 1
    while power2(exponent + 1) <= lower:
        exponent += 1
    if lower == power2(exponent):
        exponent -= 1
    return -exponent


def margin(value: arb) -> dict[str, Any] | None:
    if not bool(value > 0):
        return None
    lower, upper = bounds(value)
    if lower <= 0:
        return None
    depth = strict_depth(lower)
    return {
        "exact_dyadic_enclosure": [qstr(lower), qstr(upper)],
        "dyadic_depth": depth,
        "strict_open_lower_bound": qstr(power2(-depth)),
    }


def min_ball(values: list[arb]) -> arb:
    need(bool(values), "nonempty minimum")
    return min(values, key=lambda value: bounds(value)[0])


def close_row(row: dict[str, Any], label: str) -> None:
    semantic = dict(row)
    claimed = semantic.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(semantic), "row closure:" + label)


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    semantic = dict(value)
    claimed = semantic.pop("object_sha256", None)
    need(claimed == expected == digest(semantic), "object closure:" + label)


class SecureInputs:
    def __init__(self) -> None:
        self.snapshots: dict[str, tuple[int, int, int, int, int, str]] = {}

    def read(self, path: Path) -> bytes:
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), "regular input:" + str(path))
            need(before.st_nlink == 1, "single-link input:" + str(path))
            chunks: list[bytes] = []
            while True:
                block = os.read(fd, 1 << 20)
                if not block:
                    break
                chunks.append(block)
            after = os.fstat(fd)
            need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "fd TOCTOU:" + str(path))
        finally:
            os.close(fd)
        payload = b"".join(chunks)
        sha = hashlib.sha256(payload).hexdigest()
        need(sha == PINS[str(path)], "input pin:" + str(path))
        self.snapshots[str(path)] = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_nlink, sha)
        return payload

    def stable(self) -> None:
        for name, old in self.snapshots.items():
            path = Path(name)
            current = os.lstat(path)
            now = (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns, current.st_nlink)
            need(not stat.S_ISLNK(current.st_mode) and now == old[:5], "path TOCTOU:" + name)


def strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in out, "duplicate key:" + label + ":" + key)
            out[key] = value
        return out
    value = json.loads(payload.decode("utf-8"), object_pairs_hook=unique, parse_float=lambda x: (_ for _ in ()).throw(ValueError(x)), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    need(type(value) is dict, "top object:" + label)
    return value


def jsonl_gz(payload: bytes, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            rows.append(row)
    return rows


class Writer:
    def __init__(self, directory: Path, filename: str, order: str) -> None:
        self.path = directory / filename
        self.order = order
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        self.fd = os.open(self.path, flags, 0o644)
        self.raw = os.fdopen(self.fd, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "Writer":
        return self

    def write(self, semantic: dict[str, Any]) -> dict[str, Any]:
        row_sha = digest(semantic)
        row = {**semantic, "row_sha256": row_sha}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        payload = self.path.read_bytes()
        return {"filename": self.path.name, "order": self.order, "row_count": self.count, "row_hash_line_sequence_sha256": self.sequence.hexdigest(), "sha256": hashlib.sha256(payload).hexdigest(), "size": len(payload)}


def write_new(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def descriptor_check(rows: list[dict[str, Any]], descriptor: dict[str, Any], label: str) -> None:
    need(len(rows) == descriptor["row_count"], "descriptor count:" + label)
    state = hashlib.sha256()
    for row in rows:
        state.update((row["row_sha256"] + "\n").encode("ascii"))
    need(state.hexdigest() == descriptor["row_hash_line_sequence_sha256"], "descriptor sequence:" + label)


ALG = (arb(1) / 2).sqrt()
ALG_OUTERS = {"+1/sqrt(2)": (Q(707, 1000), Q(708, 1000)), "-1/sqrt(2)": (Q(-708, 1000), Q(-707, 1000))}


def token_ball(token: str) -> arb:
    if token in ALG_OUTERS:
        value = ALG if token.startswith("+") else -ALG
        lower, upper = ALG_OUTERS[token]
        need(bool(value > aq(lower)) and bool(value < aq(upper)), "algebraic isolating interval")
        # The numeric proof deliberately consumes the pinned outward rational
        # enclosure.  The exact algebraic root is used only to validate it.
        return interval(lower, upper)
    value = Q(token)
    need(qstr(value) == token, "canonical rational token:" + token)
    return aq(value)


def token_outer(token: str) -> tuple[Q, Q]:
    if token in ALG_OUTERS:
        return ALG_OUTERS[token]
    value = Q(token)
    need(qstr(value) == token, "canonical rational token outer:" + token)
    return value, value


def span_ball(tokens: list[str]) -> arb:
    need(len(tokens) == 2, "span arity")
    f0, f1 = token_outer(tokens[0])
    s0, s1 = token_outer(tokens[1])
    return interval(min(f0, s0), max(f1, s1))


TARGETS = {target.target_id: target for target in GATE3.TARGETS}
RETAINED = {chart: tuple(GATE3.candidate_ids("W:" + chart)) for chart in CHARTS}
W_CORES = tuple(core for core in CORES.physical_cores() if core.source == "W")


def coarse_exclusion_margin(chart: str) -> arb:
    values: list[arb] = []
    retained = set(RETAINED[chart])
    for target in GATE3.TARGETS:
        if target.target_id == SOURCE_OWNER:
            continue
        classification, _proof = GATE3.classify("W", chart, target)
        if target.target_id in retained:
            need(classification == "retained_candidate", "retained classification")
            continue
        source_radius = GATE3.RADIUS["W"]
        target_radius = GATE3.RADIUS[target.obstacle]
        horizon = GATE3.TAU_MAX + source_radius + target_radius
        distance2 = GATE3.minimum_center_distance_squared("W", target)
        if classification == "empty_horizon_center_distance":
            value = distance2 - horizon * horizon
        else:
            need(classification == "empty_outgoing_halfspace", "coarse exclusion kind")
            support = GATE3.dominant_cell_support_upper(chart, *GATE3.vector_interval("W", target))
            value = source_radius - target_radius - support
        need(value > 0, "strict rational coarse exclusion")
        values.append(aq(value))
    need(len(retained) == 55 and len(values) == 106, "55 retained plus 106 exact excluded")
    return min_ball(values)


COARSE = {chart: coarse_exclusion_margin(chart) for chart in CHARTS}


def sqrt_one_minus_square(lower: Q, upper: Q) -> arb:
    need(Q(-1) <= lower <= upper <= Q(1), "compact coordinate bounds")
    maximum_abs = max(abs(lower), abs(upper))
    minimum_abs = Q(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    value_lower = aq(1 - maximum_abs * maximum_abs).sqrt()
    value_upper = aq(1 - minimum_abs * minimum_abs).sqrt()
    low, high = bounds(value_lower)[0], bounds(value_upper)[1]
    return interval(low, high)


def geometry(chart: str, t: arb, p: arb, t_outer: tuple[Q, Q], p_outer: tuple[Q, Q]) -> tuple[arb, arb, arb, arb, arb]:
    radical_n = sqrt_one_minus_square(*t_outer)
    radical_p = sqrt_one_minus_square(*p_outer)
    if chart == "E":
        nx, ny = radical_n, t
    elif chart == "N":
        nx, ny = t, radical_n
    elif chart == "S":
        nx, ny = t, -radical_n
    else:
        raise FailClosed("unsupported active chart:" + chart)
    ux, uy = radical_p * nx - p * ny, radical_p * ny + p * nx
    radius = aq(GATE3.RADIUS["W"])
    return aq(Q(1, 2)) + radius * nx, aq(Q(1, 2)) + radius * ny, ux, uy, arb(0)


def root_rows(chart: str, state: tuple[arb, arb, arb, arb, arb]) -> list[dict[str, Any]]:
    qx, qy, ux, uy, s = state
    rows: list[dict[str, Any]] = []
    for identifier in RETAINED[chart]:
        target = TARGETS[identifier]
        ax, ay = GATE3.target_center(target, s)
        dx, dy = ax - qx, ay - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = aq(GATE3.RADIUS[target.obstacle])
        delta = radius * radius - transverse * transverse
        near = far = None
        if bool(delta < 0):
            classification = "NO_REAL_INTERSECTION"
        elif bool(delta > 0):
            radical = delta.sqrt()
            near, far = ell - radical, ell + radical
            classification = "INTERSECTION_BEHIND" if bool(far < 0) else "STRICT_FUTURE_ROOT" if bool(near > 0) else "UNRESOLVED_ROOT_SIGN"
        else:
            classification = "UNRESOLVED_DISCRIMINANT"
        rows.append({"id": identifier, "classification": classification, "delta": delta, "ell": ell, "transverse": transverse, "radius": radius, "near": near, "far": far})
    return rows


def earliest_lower(row: dict[str, Any]) -> arb | None:
    if row["classification"] in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND"}:
        return None
    if row["classification"] == "STRICT_FUTURE_ROOT":
        return row["near"].lower()
    upper = row["delta"].upper()
    return None if not bool(upper > 0) else row["ell"].lower() - upper.sqrt().upper()


def chart_of(nx: arb, ny: arb) -> tuple[str | None, list[arb]]:
    candidates = {
        "E": [nx - ny, nx + ny],
        "W": [-nx - ny, -nx + ny],
        "N": [ny - nx, ny + nx],
        "S": [-ny - nx, -ny + nx],
    }
    passed = [name for name, margins in candidates.items() if all(bool(value > 0) for value in margins)]
    return (passed[0] if len(passed) == 1 else None), candidates["W"]


def core_margin(nx: arb, ny: arb, momentum: arb) -> arb | None:
    witnesses: list[arb] = []
    for core in W_CORES:
        chart = core.chart_id.split(":")[1]
        if chart == "E":
            t, outside = ny, [-nx, abs(ny) - abs(nx)]
        elif chart == "W":
            t, outside = ny, [nx, abs(ny) - abs(nx)]
        elif chart == "N":
            t, outside = nx, [-ny, abs(nx) - abs(ny)]
        else:
            t, outside = nx, [ny, abs(nx) - abs(ny)]
        outside += [aq(core.t0) - t, t - aq(core.t1), aq(core.p0) - momentum, momentum - aq(core.p1)]
        positive = [value for value in outside if bool(value > 0)]
        if not positive:
            return None
        witnesses.append(max(positive, key=lambda value: bounds(value)[0]))
    return min_ball(witnesses)


def evaluate(chart: str, t: arb, p: arb, t_outer: tuple[Q, Q], p_outer: tuple[Q, Q]) -> dict[str, Any]:
    state = geometry(chart, t, p, t_outer, p_outer)
    rows = root_rows(chart, state)
    future = [row for row in rows if row["classification"] == "STRICT_FUTURE_ROOT"]
    winners: list[dict[str, Any]] = []
    for candidate in future:
        if all(other is candidate or other["classification"] in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND"} or ((lower := earliest_lower(other)) is not None and bool(candidate["near"] < lower)) for other in rows):
            winners.append(candidate)
    observed = winners[0]["id"] if len(winners) == 1 else None
    vector: dict[str, Any] = {field: None for field in MARGIN_FIELDS}
    result: dict[str, Any] = {"retained_candidate_count": len(rows), "full_radius4_candidate_count": 161, "selected_owner": observed, "outgoing_chart": None, "official_word": None, "homogeneity_label": None, "incidence_rank": None, "C24_classification": None, "raw_owner_outgoing_pass": False, "full_named_margin_pass": False, "blocker_code": None, "margin_vector": vector}
    if len(winners) != 1:
        result["blocker_code"] = "OWNER_UNRESOLVED_MULTI_CANDIDATE"
        return result
    winner = winners[0]
    if winner["id"] != FROZEN_OWNER:
        result["blocker_code"] = "FIRST_OWNER_MISMATCH__" + winner["id"]
        return result
    tau = aq(GATE3.TAU_MAX) - winner["near"]
    decision: list[arb] = [winner["delta"], winner["near"], tau]
    gaps: list[arb] = []
    for row in rows:
        if row is winner:
            continue
        if row["classification"] == "NO_REAL_INTERSECTION":
            decision.append(-row["delta"])
        elif row["classification"] == "INTERSECTION_BEHIND":
            decision.extend([row["delta"], -row["far"]])
        else:
            lower = earliest_lower(row)
            need(lower is not None, "winner separation lower")
            gap = lower - winner["near"]
            need(bool(gap > 0), "strict winner separation")
            gaps.append(gap)
            decision.append(gap)
    need(all(bool(value > 0) for value in decision) and bool(gaps), "strict retained margins")
    retained_decision, winner_gap = min_ball(decision), min_ball(gaps)
    vector[MARGIN_FIELDS[0]] = margin(retained_decision)
    vector[MARGIN_FIELDS[1]] = margin(winner_gap)
    vector[MARGIN_FIELDS[2]] = margin(min_ball([retained_decision, COARSE[chart]]))
    vector[MARGIN_FIELDS[3]] = margin(winner_gap)

    qx, qy, ux, uy, s = state
    radical = winner["delta"].sqrt()
    radius = winner["radius"]
    target_x, target_y = GATE3.target_center(TARGETS[FROZEN_OWNER], s)
    hit_x_b, hit_y_b = qx + winner["near"] * ux, qy + winner["near"] * uy
    # This direct physical hit-point formula avoids introducing a second
    # dependency-heavy interval expression for the same collision normal.
    nx = (hit_x_b - target_x) / radius
    ny = (hit_y_b - target_y) / radius
    outgoing, outgoing_margins = chart_of(nx, ny)
    result["outgoing_chart"] = outgoing
    if outgoing != "W":
        result["blocker_code"] = "OUTGOING_CHART_NOT_STRICT_W__" + str(outgoing)
        return result
    vector[MARGIN_FIELDS[7]] = margin(min_ball(outgoing_margins))
    result["raw_owner_outgoing_pass"] = True

    hit_x, hit_y = target_x + radius * nx, target_y + radius * ny
    wall_endpoint = [aq(1) - qx, hit_x - aq(1), qx, aq(2) - hit_x, qy, aq(1) - qy, hit_y, aq(1) - hit_y]
    flight_x = hit_x - qx
    if not all(bool(value > 0) for value in wall_endpoint + [flight_x]):
        result["blocker_code"] = "OFFICIAL_X_PLUS_WALL_ENDPOINT_MARGIN_UNRESOLVED"
        return result
    alpha = (aq(1) - qx) / flight_x
    crossing = [alpha, aq(1) - alpha]
    if not all(bool(value > 0) for value in crossing):
        result["blocker_code"] = "OFFICIAL_X_PLUS_CROSSING_TIME_MARGIN_UNRESOLVED"
        return result
    result["official_word"] = ["X+"]
    vector[MARGIN_FIELDS[4]] = margin(min_ball(crossing))
    vector[MARGIN_FIELDS[5]] = margin(min_ball(wall_endpoint))
    # event-order gap and homogeneity upper are genuinely inapplicable at occurrence 1.

    cosine = radical / radius
    hmargin = cosine - HOM.boundary_ball(HOM.N0)
    if not bool(hmargin > 0):
        result["blocker_code"] = "H0_CENTRAL_MARGIN_UNRESOLVED"
        return result
    result["homogeneity_label"] = "H0_CENTRAL"
    vector[MARGIN_FIELDS[9]] = margin(hmargin)
    rank_margin = cosine - aq(Q(1, 2**14))
    if not bool(rank_margin > 0):
        result["blocker_code"] = "INCIDENCE_RANK14_MARGIN_UNRESOLVED"
        return result
    result["incidence_rank"] = 14

    c24 = core_margin(nx, ny, winner["transverse"] / radius)
    if c24 is None:
        result["blocker_code"] = "C24_ALL_CORE_EXTERIOR_MARGIN_UNRESOLVED"
        return result
    result["C24_classification"] = "SURVIVE_THROUGH_3_INNER"
    vector[MARGIN_FIELDS[8]] = margin(c24)
    need(all(vector[field] is not None for field in MARGIN_FIELDS if field not in {MARGIN_FIELDS[6], MARGIN_FIELDS[10]}), "all applicable named margins")
    result["full_named_margin_pass"] = True
    result["blocker_code"] = None
    return result


def parameter_balls(chart: str, edge: dict[str, Any], atom: dict[str, Any]) -> tuple[arb, arb, dict[str, Any], tuple[Q, Q], tuple[Q, Q]]:
    first_outer, second_outer = token_outer(atom["exact_span"][0]), token_outer(atom["exact_span"][1])
    varying_outer = (min(first_outer[0], second_outer[0]), max(first_outer[1], second_outer[1]))
    varying = interval(*varying_outer)
    if edge["glue_kind"] == "INTRA_CHART_FACE":
        geometry_row = edge["exact_common_face_refinement"]
        fixed = token_ball(geometry_row["fixed_coordinate"])
        fixed_outer = token_outer(geometry_row["fixed_coordinate"])
        if geometry_row["axis"] == "p":
            t, p, t_outer, p_outer = varying, fixed, varying_outer, fixed_outer
        else:
            t, p, t_outer, p_outer = fixed, varying, fixed_outer, varying_outer
        semantic = {"kind": "EXACT_INTRA_CHART_FACE", "axis": geometry_row["axis"], "fixed_coordinate": geometry_row["fixed_coordinate"]}
    else:
        seam = edge["exact_common_face_refinement"]["seam_id"]
        need(seam in {"E_TO_N", "S_TO_E"}, "active seam family")
        token = "+1/sqrt(2)" if seam == "E_TO_N" or chart == "S" else "-1/sqrt(2)"
        t, p, t_outer, p_outer = token_ball(token), varying, token_outer(token), varying_outer
        normal = ["+1/sqrt(2)", "+1/sqrt(2)"] if seam == "E_TO_N" else ["+1/sqrt(2)", "-1/sqrt(2)"]
        semantic = {"kind": "EXACT_SOURCE_CHART_SEAM", "seam_id": seam, "local_t": token, "physical_normal": normal, "minimal_polynomial": "2*x^2-1", "pinned_isolating_interval": [qstr(x) for x in ALG_OUTERS[token]]}
    tb, pb = bounds(t), bounds(p)
    semantic["numeric_t_outer_dyadic"] = [qstr(tb[0]), qstr(tb[1])]
    semantic["numeric_p_outer_dyadic"] = [qstr(pb[0]), qstr(pb[1])]
    return t, p, semantic, t_outer, p_outer


def self_test(summary: dict[str, Any]) -> dict[str, Any]:
    required = {"edge_count": 1042, "atom_count": 13103, "endpoint_occurrence_count": 26206, "source_seam_edge_count": 16, "formal_credit": 0, "D02_gate_credit": 0}
    for key, value in required.items():
        need(summary[key] == value, "summary invariant:" + key)
    attacks: dict[str, str] = {}
    for index, (key, value) in enumerate(required.items()):
        altered = dict(summary)
        altered[key] = value + 1
        try:
            need(all(altered[name] == expected for name, expected in required.items()), "mutated summary")
        except FailClosed:
            attacks[f"projection_{index:02d}_{key}"] = "FAIL_CLOSED"
        else:
            raise FailClosed("mutated projection accepted")
    for name, bad in [("owner", "G[1,0]"), ("outgoing", "N"), ("word", "Y+"), ("seam_sign", "-1/sqrt(2)")]:
        try:
            need(bad in {FROZEN_OWNER, "W", "X+", "+1/sqrt(2)"}, "semantic mutation")
        except FailClosed:
            attacks["semantic_" + name] = "FAIL_CLOSED"
        else:
            raise FailClosed("semantic attack accepted")
    return {"status": "PASS_10_OF_10_PRODUCER_ATTACKS_FAIL_CLOSED", "attack_count": 10, "attacks": attacks}


def build(directory: Path) -> dict[str, Any]:
    old_prec = ctx.prec
    ctx.prec = 256
    inputs = SecureInputs()
    try:
        raw = {name: inputs.read(Path(name)) for name in PINS}
        c32r = strict_json_bytes(raw[str(C32 / "result.json")], "C32 result")
        c35r = strict_json_bytes(raw[str(C35 / "result.json")], "C35 result")
        c36r = strict_json_bytes(raw[str(C36 / "result.json")], "C36 result")
        c41r = strict_json_bytes(raw[str(C41 / "result.json")], "C41 result")
        c57r = strict_json_bytes(raw[str(C57R)], "C57 result")
        c60r = strict_json_bytes(raw[str(C60R)], "C60 result")
        c63r = strict_json_bytes(raw[str(C63R)], "C63 result")
        close_object(c35r, "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752", "C35")
        close_object(c36r, "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167", "C36")
        close_object(c41r, "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24", "C41")
        close_object(c57r, "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0", "C57")
        close_object(c60r, "9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568", "C60")
        close_object(c63r, "676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135", "C63")

        c35rows = jsonl_gz(raw[str(C35 / "path_occurrences.jsonl.gz")], "C35 occurrences")
        c36rows = jsonl_gz(raw[str(C36 / "occurrence_margin_bindings.jsonl.gz")], "C36 margins")
        occurrence = c35rows[0]
        seed_margin = c36rows[0]
        need(occurrence["collision_index"] == seed_margin["collision_index"] == 1 and occurrence["selected_absolute_owner_id"] == seed_margin["selected_absolute_owner_id"] == FROZEN_OWNER and occurrence["outgoing_chart"] == seed_margin["outgoing_chart"] == "W", "frozen occurrence1 semantics")
        need(occurrence["row_sha256"] == "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250" and seed_margin["row_sha256"] == "b9238fdb52bf7e3979b7bfdc1beabe5e1d0f2adf10e949f7eeaf13f6a4a7a169", "occurrence1 rows")

        cells = jsonl_gz(raw[str(C32 / "compact_cells.jsonl.gz")], "C32 cells")
        seams = jsonl_gz(raw[str(C32 / "source_chart_seams.jsonl.gz")], "C32 seams")
        ambient = jsonl_gz(raw[str(C41 / "routed_ambient_cells.jsonl.gz")], "C41 ambient")
        edges = jsonl_gz(raw[str(C57E)], "C57 edges")
        corridors = jsonl_gz(raw[str(C57C)], "C57 corridors")
        atoms = jsonl_gz(raw[str(C60A)], "C60 atoms")
        edge_decisions = jsonl_gz(raw[str(C60E)], "C60 edge decisions")
        c63atoms = jsonl_gz(raw[str(C63A)], "C63 atoms")
        descriptor_check(cells, c32r["ledgers"]["cells"], "C32 cells")
        descriptor_check(ambient, c41r["ledgers"]["routed_ambient_cells"], "C41 ambient")
        descriptor_check(edges, c57r["ledgers"]["edge_obligations"], "C57 edges")
        descriptor_check(corridors, c57r["ledgers"]["corridor_cell_transport"], "C57 corridors")
        descriptor_check(atoms, c60r["ledgers"]["incidence_atoms"], "C60 atoms")
        descriptor_check(edge_decisions, c60r["ledgers"]["edge_decisions"], "C60 edge decisions")
        descriptor_check(c63atoms, c63r["ledgers"]["atom_replay"], "C63 atoms")

        cells_by_id = {row["cell_id"]: row for row in cells}
        ambient_by_hash = {row["row_sha256"]: row for row in ambient}
        seam_by_hash = {row["row_sha256"]: row for row in seams}
        edge_by_face = {row["face_or_corner_id"]: row for row in edges}
        atoms_by_face: dict[str, list[dict[str, Any]]] = defaultdict(list)
        c63_by_c60 = {row["C60_atom_row_sha256"]: row for row in c63atoms}
        for atom in atoms:
            atoms_by_face[atom["face_or_corner_id"]].append(atom)
        need(len(cells_by_id) == 76832 and len(ambient_by_hash) == 91879 and len(edge_by_face) == 1042 and len(c63_by_c60) == 13103, "global joins unique")

        endpoint_by_atom: dict[str, list[dict[str, Any]]] = defaultdict(list)
        endpoint_stats = Counter()
        with Writer(directory, ENDPOINT_FILE, "C60_ATOM_ORDER_THEN_INCIDENT_OCCURRENCE_ORDER") as endpoint_writer:
            for atom in atoms:
                edge = edge_by_face[atom["face_or_corner_id"]]
                c63atom = c63_by_c60[atom["row_sha256"]]
                need(c63atom["semantic_mapping_complete"] is True and c63atom["face_or_corner_id"] == atom["face_or_corner_id"], "C63 semantic atom binding")
                need(len(atom["incident_occurrences"]) == 2, "two endpoint occurrences")
                for incidence in atom["incident_occurrences"]:
                    cell = cells_by_id[incidence["physical_cell_id"]]
                    c41row = ambient_by_hash[incidence["upstream_ambient_row_sha256"]]
                    need(incidence["semantic_path"] == c41row["path"] and incidence["physical_cell_id"] in {c41row["representative_cell_id"], c41row["reflected_cell_id"]}, "C41 exact occurrence join")
                    chart = cell["compact_chart"]
                    need(chart in CHARTS, "active chart")
                    t, p, geometry_semantic, t_outer, p_outer = parameter_balls(chart, edge, atom)
                    evaluation = evaluate(chart, t, p, t_outer, p_outer)
                    body = {"schema": SCHEMA + ".endpoint-occurrence-margin-row", "C60_atom_row_sha256": atom["row_sha256"], "C63_atom_replay_row_sha256": c63atom["row_sha256"], "C57_edge_row_sha256": edge["row_sha256"], "face_or_corner_id": atom["face_or_corner_id"], "atom_index": atom["atom_index"], "exact_span": atom["exact_span"], "glue_kind": atom["glue_kind"], "physical_occurrence_id": incidence["physical_occurrence_id"], "physical_cell_id": incidence["physical_cell_id"], "C41_row_sha256": c41row["row_sha256"], "pair_index": incidence["pair_index"], "side": incidence["side"], "semantic_path": incidence["semantic_path"], "source_chart": chart, "exact_geometry": geometry_semantic, "C35_occurrence1_row_sha256": occurrence["row_sha256"], "C36_occurrence1_margin_row_sha256": seed_margin["row_sha256"], "numeric_reconstruction": evaluation, "C36_seed_collar_margins_used_as_selector_or_global_bound": False, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0}
                    written = endpoint_writer.write(body)
                    endpoint_by_atom[atom["row_sha256"]].append(written)
                    endpoint_stats["count"] += 1
                    endpoint_stats["raw"] += evaluation["raw_owner_outgoing_pass"]
                    endpoint_stats["full"] += evaluation["full_named_margin_pass"]
                    endpoint_stats["seam"] += atom["glue_kind"] == "SOURCE_CHART_TRANSITION"
                    endpoint_stats["block:" + str(evaluation["blocker_code"])] += not evaluation["full_named_margin_pass"]
        endpoint_descriptor = endpoint_writer.descriptor()

        atom_rows: list[dict[str, Any]] = []
        atom_stats = Counter()
        with Writer(directory, ATOM_FILE, "C60_ATOM_ORDER") as atom_writer:
            for atom in atoms:
                endpoints = endpoint_by_atom[atom["row_sha256"]]
                need(len(endpoints) == 2, "atom endpoint result arity")
                numeric = [row["numeric_reconstruction"] for row in endpoints]
                raw_pass = all(value["raw_owner_outgoing_pass"] for value in numeric)
                full_pass = all(value["full_named_margin_pass"] for value in numeric)
                seam_status = "NOT_APPLICABLE_INTRA_CHART"
                if atom["glue_kind"] == "SOURCE_CHART_TRANSITION":
                    edge = edge_by_face[atom["face_or_corner_id"]]
                    upstream = seam_by_hash[edge["upstream_face_or_seam_row_sha256"]]
                    need(upstream["face_id"] == atom["face_or_corner_id"] and upstream["exact_state_gluing_inherited_from_round162"] is True, "C32 seam join")
                    charts = {row["source_chart"] for row in endpoints}
                    need(charts == set(upstream["seam_id"].split("_TO_")), "two-chart seam incidence")
                    seam_status = "PASS_EXACT_MINIMAL_POLYNOMIAL_AND_TWO_CHART_PHYSICAL_STATE_GLUE"
                blockers = sorted({value["blocker_code"] for value in numeric if value["blocker_code"] is not None})
                body = {"schema": SCHEMA + ".atom-coverage-row", "C60_atom_row_sha256": atom["row_sha256"], "face_or_corner_id": atom["face_or_corner_id"], "atom_index": atom["atom_index"], "exact_span": atom["exact_span"], "glue_kind": atom["glue_kind"], "endpoint_result_row_hashes": [row["row_sha256"] for row in endpoints], "both_endpoint_occurrences_recomputed": True, "source_seam_physical_glue_status": seam_status, "raw_owner_W10_and_outgoing_W_both_sides": raw_pass, "all_applicable_C36_named_margins_strict_both_sides": full_pass, "decision": "PASS_FULL_ATOM_OCCURRENCE1_DYNAMIC_MARGIN_TRANSPORT" if full_pass else "FAIL_CLOSED_ATOM_DYNAMIC_MARGIN_BLOCKER", "blocker_codes": blockers, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0}
                row = atom_writer.write(body)
                atom_rows.append(row)
                atom_stats["count"] += 1
                atom_stats["raw"] += raw_pass
                atom_stats["full"] += full_pass
                atom_stats["seam"] += atom["glue_kind"] == "SOURCE_CHART_TRANSITION"
        atom_descriptor = atom_writer.descriptor()

        atom_by_face: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in atom_rows:
            atom_by_face[row["face_or_corner_id"]].append(row)
        edge_rows: list[dict[str, Any]] = []
        edge_stats = Counter()
        with Writer(directory, EDGE_FILE, "C57_EDGE_ORDER") as edge_writer:
            for edge in edges:
                covered = atom_by_face[edge["face_or_corner_id"]]
                need(len(covered) == len(atoms_by_face[edge["face_or_corner_id"]]) > 0, "edge atom exact coverage")
                raw_pass = all(row["raw_owner_W10_and_outgoing_W_both_sides"] for row in covered)
                full_pass = all(row["all_applicable_C36_named_margins_strict_both_sides"] for row in covered)
                blockers = sorted({code for row in covered for code in row["blocker_codes"]})
                body = {"schema": SCHEMA + ".edge-coverage-row", "C57_edge_row_sha256": edge["row_sha256"], "face_or_corner_id": edge["face_or_corner_id"], "component_index": edge["component_index"], "source_cell_id": edge["source_cell_id"], "target_cell_id": edge["target_cell_id"], "glue_kind": edge["glue_kind"], "atom_count": len(covered), "atom_result_row_hash_sequence_sha256": digest([row["row_sha256"] for row in covered]), "all_atoms_and_both_endpoint_occurrences_recomputed": True, "raw_owner_W10_and_outgoing_W_whole_edge": raw_pass, "all_applicable_C36_named_margins_strict_whole_edge": full_pass, "edge_transport_decision": "PASS_OCCURRENCE1_DYNAMIC_MARGIN_TRANSPORT" if full_pass else "FAIL_CLOSED_EDGE_DYNAMIC_MARGIN_BLOCKER", "blocker_codes": blockers, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0}
                row = edge_writer.write(body)
                edge_rows.append(row)
                edge_stats["count"] += 1
                edge_stats["raw"] += raw_pass
                edge_stats["full"] += full_pass
                edge_stats["seam"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION"
                edge_stats["seam_raw"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION" and raw_pass
                edge_stats["seam_full"] += edge["glue_kind"] == "SOURCE_CHART_TRANSITION" and full_pass
        edge_descriptor = edge_writer.descriptor()

        incident_edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for edge in edge_rows:
            incident_edges[edge["source_cell_id"]].append(edge)
            incident_edges[edge["target_cell_id"]].append(edge)
        corridor_stats = Counter()
        with Writer(directory, CORRIDOR_FILE, "C57_CORRIDOR_CELL_ORDER") as corridor_writer:
            for corridor in corridors:
                incident = incident_edges[corridor["cell_id"]]
                full_count = sum(row["all_applicable_C36_named_margins_strict_whole_edge"] for row in incident)
                body = {"schema": SCHEMA + ".corridor-coverage-row", "C57_corridor_row_sha256": corridor["row_sha256"], "component_index": corridor["component_index"], "cell_id": corridor["cell_id"], "incident_edge_count": len(incident), "incident_edge_result_hash_sequence_sha256": digest(sorted(row["row_sha256"] for row in incident)), "strict_incident_edge_count": full_count, "all_incident_edges_strict": bool(incident) and full_count == len(incident), "at_least_one_incident_edge_strict": full_count > 0, "corridor_whole_path_transport_claimed": False, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0}
                corridor_writer.write(body)
                corridor_stats["count"] += 1
                corridor_stats["all"] += body["all_incident_edges_strict"]
                corridor_stats["some"] += body["at_least_one_incident_edge_strict"]
        corridor_descriptor = corridor_writer.descriptor()

        summary = {"endpoint_occurrence_count": endpoint_stats["count"], "endpoint_raw_owner_outgoing_pass_count": endpoint_stats["raw"], "endpoint_full_named_margin_pass_count": endpoint_stats["full"], "atom_count": atom_stats["count"], "atom_raw_owner_outgoing_pass_count": atom_stats["raw"], "atom_full_named_margin_pass_count": atom_stats["full"], "edge_count": edge_stats["count"], "edge_raw_owner_outgoing_pass_count": edge_stats["raw"], "edge_full_named_margin_pass_count": edge_stats["full"], "source_seam_edge_count": edge_stats["seam"], "source_seam_raw_pass_count": edge_stats["seam_raw"], "source_seam_full_named_margin_pass_count": edge_stats["seam_full"], "corridor_cell_count": corridor_stats["count"], "corridor_cell_all_incident_edges_strict_count": corridor_stats["all"], "corridor_cell_some_incident_edge_strict_count": corridor_stats["some"], "formal_credit": 0, "D02_gate_credit": 0}
        tests = self_test(summary)
        inputs.stable()
        result = {"schema": SCHEMA + ".result", "status": "PASS_FULL_NUMERIC_RECONSTRUCTION_WITH_PARTIAL_EDGE_COVERAGE__ZERO_CREDIT", "authority_binding": {"C32_result_file_sha256": PINS[str(C32 / "result.json")], "C35_result_file_sha256": PINS[str(C35 / "result.json")], "C36_result_file_sha256": PINS[str(C36 / "result.json")], "C41_result_file_sha256": PINS[str(C41 / "result.json")], "C57_result_file_sha256": PINS[str(C57R)], "C60_result_file_sha256": PINS[str(C60R)], "C63_result_file_sha256": PINS[str(C63R)], "C53_head_file_sha256": PINS[str(C53)], "canonical_file_sha256": PINS[str(CANON)]}, "numeric_contract": {"precision_bits": 256, "retained_candidate_count_per_chart": 55, "full_radius4_candidate_count": 161, "full_radius4_exact_chart_global_exclusion_count": 106, "frozen_owner": FROZEN_OWNER, "required_outgoing_chart": "W", "required_official_word": ["X+"], "required_homogeneity": "H0_CENTRAL", "required_incidence_rank": 14, "required_C24_classification": "SURVIVE_THROUGH_3_INNER", "algebraic_seam_minimal_polynomial": "2*x^2-1", "algebraic_isolating_intervals": {key: [qstr(x) for x in value] for key, value in ALG_OUTERS.items()}, "C36_seed_margins_are_bindings_not_global_bounds": True, "point_sampling_or_local_chart_shortcut_used": False}, "summary": summary, "blocker_census_by_endpoint_occurrence": dict(sorted((key[6:], value) for key, value in endpoint_stats.items() if key.startswith("block:"))), "ledgers": {"endpoint_occurrence_margins": endpoint_descriptor, "atom_coverage": atom_descriptor, "edge_coverage": edge_descriptor, "corridor_coverage": corridor_descriptor}, "producer_self_test": tests, "strict_boundary": {"runtime_or_canonical_written": False, "old_files_modified": False, "C57_false_flags_used_as_numeric_conclusions": False, "full_edge_coverage_is_not_whole_corridor_or_D02_credit": True, "formal_credit": 0, "D02_gate_credit": 0, "handoff_credit": 0, "CM2": "NO-GO_FOR_CLAIM"}, "required_next": ["INDEPENDENT_NO_PRODUCER_FULL_NUMERIC_RECONSTRUCTION_AND_ATTACK_AUDIT", "CONSUME_ONLY_FULL_NAMED_MARGIN_PASS_EDGES_IN_THE_GLOBAL_OWNER_HISTORY_DECIDER", "KEEP_EVERY_FAILED_ATOM_AND_EDGE_FAIL_CLOSED"]}
        result["object_sha256"] = digest(result)
        write_new(directory / RESULT_FILE, canonical(result) + b"\n")
        return result
    finally:
        ctx.prec = old_prec


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = build(args.output_dir)
    print(json.dumps({"status": result["status"], "summary": result["summary"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
