#!/usr/bin/env python3
"""Zero-credit active-graph audit for Round277 depth-8 face residuals.

This does not infer absence from a finite dyadic depth.  Instead it asks
whether every non-strict depth-8 terminal cell has the same normal form used
by Rounds274/275: one explicitly named active equality with strict tangent
derivatives and strictly signed extremal witnesses.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
from fractions import Fraction as Q
from pathlib import Path

from flint import arb, ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277


HERE = Path(__file__).resolve().parent
RESIDUAL = HERE / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
GROUPS: list[tuple] = []
TABLES = None
FACE_DEPTH = 8


def active_dual(geometry: dict, reason: str):
    if reason == "outgoing_chart_seam":
        return geometry["outgoing_equality"]
    kind, axis, wall = reason.split(":")
    assert kind == "wall_endpoint_or_count_transition"
    dual = geometry["hit_x" if axis == "X" else "hit_y"]
    return dual[0] - arb(int(wall)), dual[1]


def source_factor(geometry: dict, reason: str):
    if reason == "outgoing_chart_seam":
        return None
    _kind, axis, wall = reason.split(":")
    dual = geometry["source_x" if axis == "X" else "source_y"]
    return dual[0] - arb(int(wall)), dual[1]


def make_box(axis: int, coordinate: Q, rect: tuple, label: str):
    q = []
    j = 0
    for k in range(3):
        if k == axis:
            q += [coordinate, coordinate]
        else:
            q += list(rect[j])
            j += 1
    return r174.atlas.AtlasBox(*q, 0, label)


def split_rect(rect: tuple):
    widths = [x[1] - x[0] for x in rect]
    split = 0 if widths[0] >= widths[1] else 1
    mid = (rect[split][0] + rect[split][1]) / 2
    children = []
    for side, z in enumerate(((rect[split][0], mid), (mid, rect[split][1]))):
        child = list(rect)
        child[split] = z
        children.append((tuple(child), split, side))
    return children


def extrema(
    chart: str,
    target: str,
    axis: int,
    coordinate: Q,
    rect: tuple,
    reason: str,
    derivative_signs: list[str | None],
):
    points = []
    for want_maximum in (False, True):
        coordinates = []
        j = 0
        for k in range(3):
            if k == axis:
                coordinates.append(coordinate)
                continue
            lower, upper = rect[j]
            j += 1
            sign = derivative_signs[k]
            if sign == "STRICT_POSITIVE":
                coordinates.append(upper if want_maximum else lower)
            elif sign == "STRICT_NEGATIVE":
                coordinates.append(lower if want_maximum else upper)
            elif sign == "EXACT_ZERO":
                coordinates.append((lower + upper) / 2)
            else:
                return None
        point = r174.atlas.AtlasBox(
            coordinates[0],
            coordinates[0],
            coordinates[1],
            coordinates[1],
            coordinates[2],
            coordinates[2],
            0,
            "round277-active-graph-extremum",
        )
        geometry = r179.interval_geometry(chart, target, point)
        value_sign = r179.sign(active_dual(geometry, reason)[0])
        signature, rejected = r174.dynamic_signature(chart, point, target, TABLES)
        points.append((value_sign, signature, rejected))
    return points


def classify_active_cell(
    chart: str,
    target: str,
    axis: int,
    coordinate: Q,
    rect: tuple,
    reason: str,
):
    box = make_box(axis, coordinate, rect, "round277-active-graph-cell")
    geometry = r179.interval_geometry(chart, target, box)
    source = source_factor(geometry, reason)
    source_sign = "NOT_APPLICABLE" if source is None else r179.sign(source[0])
    dual = active_dual(geometry, reason)
    factor_sign = r179.sign(dual[0])
    derivative_signs = [
        None
        if value is None
        else "EXACT_ZERO"
        if value == 0
        else r179.sign(value)
        for value in dual[1]
    ]
    tangent_signs = tuple(
        derivative_signs[k] for k in range(3) if k != axis
    )
    if source is not None and source_sign not in {
        "STRICT_NEGATIVE",
        "STRICT_POSITIVE",
    }:
        return (
            "FAILCLOSED_SOURCE_AND_HIT_ENDPOINT_FACTORS_BOTH_ACTIVE",
            source_sign,
            tangent_signs,
            None,
        )
    if factor_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}:
        midpoint = []
        j = 0
        for k in range(3):
            if k == axis:
                midpoint.append(coordinate)
            else:
                lower, upper = rect[j]
                j += 1
                midpoint.append((lower + upper) / 2)
        point = r174.atlas.AtlasBox(
            midpoint[0], midpoint[0], midpoint[1], midpoint[1],
            midpoint[2], midpoint[2], 0, "round277-active-whole-sign-midpoint",
        )
        signature, rejected = r174.dynamic_signature(chart, point, target, TABLES)
        assert signature is not None, rejected
        signature_hash = r276.digest(r277.payload(signature, chart))
        return (
            "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_WHOLE_CELL_SIGN",
            source_sign,
            tangent_signs,
            ((factor_sign, factor_sign), (signature_hash, signature_hash)),
        )
    if any(
        sign not in {"STRICT_NEGATIVE", "STRICT_POSITIVE", "EXACT_ZERO"}
        for sign in tangent_signs
    ):
        return (
            "FAILCLOSED_TANGENT_DERIVATIVE_NOT_STRICT",
            source_sign,
            tangent_signs,
            None,
        )
    ext = extrema(
        chart, target, axis, coordinate, rect, reason, derivative_signs
    )
    assert ext is not None
    value_signs = tuple(item[0] for item in ext)
    if any(sign not in {"STRICT_NEGATIVE", "STRICT_POSITIVE"} for sign in value_signs):
        return (
            "FAILCLOSED_EXTREMAL_ACTIVE_FACTOR_NOT_STRICT",
            source_sign,
            tangent_signs,
            value_signs,
        )
    if value_signs[0] == value_signs[1]:
        classification = "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_EXTREMA"
    else:
        classification = "ACTIVE_EQUALITY_REGULAR_MONOTONE_GRAPH"
    sig_status = []
    for _value_sign, signature, rejected in ext:
        if signature is None:
            sig_status.append("REJECT:" + "|".join(sorted(rejected)))
        else:
            sig_status.append(
                r276.digest(r277.payload(signature, chart))
            )
    if any(status.startswith("REJECT:") for status in sig_status):
        return (
            "FAILCLOSED_EXTREMAL_SIGNATURE_NOT_STRICT",
            source_sign,
            tangent_signs,
            (value_signs, tuple(sig_status)),
        )
    if classification == "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_EXTREMA":
        assert sig_status[0] == sig_status[1]
    else:
        assert sig_status[0] != sig_status[1]
    return (
        classification,
        source_sign,
        tangent_signs,
        (value_signs, tuple(sig_status)),
    )


def terminal_cells(chart: str, target: str, axis: int, coordinate: Q, overlap: tuple):
    pending = [(overlap, 0, ())]
    rows = []
    while pending:
        rect, depth, path = pending.pop()
        box = make_box(axis, coordinate, rect, "round277-active-prune")
        signature, reasons = r174.dynamic_signature(chart, box, target, TABLES)
        if signature is not None:
            rows.append(("STRICT", rect, path, signature, ()))
            continue
        if depth == FACE_DEPTH:
            rows.append(("ACTIVE", rect, path, None, tuple(reasons)))
            continue
        for child, split, side in split_rect(rect):
            pending.append((child, depth + 1, path + (f"{split}:{side}",)))
    return rows


def worker(group_index: int):
    a, b, chart, target, axis, coordinate, overlap, hashes, indices = GROUPS[group_index]
    counts = collections.Counter()
    normal_forms = collections.Counter()
    hash_relations = collections.Counter()
    requested_found = set()
    unresolved = False
    for kind, rect, path, signature, reasons in terminal_cells(
        chart, target, axis, coordinate, overlap
    ):
        if kind == "STRICT":
            digest = r276.digest(r277.payload(signature, chart))
            assert digest not in hashes
            counts["STRICT_DIFFERENT_COMPLETE_SIGNATURE_CELL"] += 1
            continue
        if len(reasons) != 1 or reasons[0] not in {
            "outgoing_chart_seam",
            "wall_endpoint_or_count_transition:X:-1",
            "wall_endpoint_or_count_transition:X:0",
            "wall_endpoint_or_count_transition:X:1",
            "wall_endpoint_or_count_transition:Y:-1",
            "wall_endpoint_or_count_transition:Y:0",
            "wall_endpoint_or_count_transition:Y:1",
        }:
            counts["FAILCLOSED_UNSUPPORTED_ACTIVE_REASON_SET"] += 1
            normal_forms[tuple(reasons)] += 1
            unresolved = True
            continue
        reason = reasons[0]
        classification, source_sign, tangent_signs, detail = classify_active_cell(
            chart, target, axis, coordinate, rect, reason
        )
        counts[classification] += 1
        if classification.startswith("FAILCLOSED"):
            unresolved = True
        normal_forms[(reason, source_sign, tangent_signs, classification)] += 1
        if detail is not None:
            value_signs, extrema_hashes = detail
            if not classification.startswith("FAILCLOSED"):
                requested_found.update(set(extrema_hashes) & hashes)
            relations = tuple(
                "REQUESTED" if h in hashes else h for h in extrema_hashes
            )
            requested_side_count = sum(h in hashes for h in extrema_hashes)
            hash_relations[
                (classification, value_signs, requested_side_count)
            ] += 1
    candidate_dispositions = collections.Counter()
    unresolved_rows = []
    for i in indices:
        requested = r277.CAND[i][2]
        if requested in requested_found:
            candidate_dispositions["EXACT_POSITIVE_MATCH_SIDE_FOUND"] += 1
        elif unresolved:
            candidate_dispositions["FAILCLOSED_ACTIVE_GRAPH_TAIL"] += 1
            unresolved_rows.append(
                {
                    "candidate_index": i,
                    "requested_signature_sha256": requested,
                    "failclosed_normal_forms": [
                        [
                            reason,
                            source_sign,
                            list(tangent_signs),
                            classification,
                            count,
                        ]
                        for (
                            reason,
                            source_sign,
                            tangent_signs,
                            classification,
                        ), count in sorted(normal_forms.items(), key=str)
                        if str(classification).startswith("FAILCLOSED")
                    ],
                }
            )
        else:
            candidate_dispositions["EXACT_NO_MATCHING_OPEN_REGION"] += 1
    return (
        group_index,
        len(indices),
        tuple(sorted(counts.items())),
        tuple(sorted(normal_forms.items(), key=str)),
        tuple(sorted(hash_relations.items(), key=str)),
        tuple(sorted(candidate_dispositions.items())),
        tuple(unresolved_rows),
    )


def load_groups():
    global GROUPS, TABLES
    cache_path = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache_path.exists():
        r277.CAND, r277.BOX, r277.TABLES = pickle.loads(cache_path.read_bytes())
    else:
        r277.build()
    TABLES = r277.TABLES
    document = json.loads(gzip.decompress(RESIDUAL.read_bytes()))
    indices = [row["candidate_index"] for row in document["rows"]]
    grouped = {}
    for i in indices:
        a, b, h, chart, target, axis, coordinate, overlap = r277.CAND[i]
        key = (a, b, chart, target, axis, coordinate, overlap)
        item = grouped.setdefault(key, [set(), []])
        item[0].add(h)
        item[1].append(i)
    GROUPS = [
        (*key, frozenset(hashes), tuple(candidate_indices))
        for key, (hashes, candidate_indices) in sorted(grouped.items(), key=str)
    ]
    assert len(indices) == 32668


def main():
    global GROUPS
    parser = argparse.ArgumentParser()
    parser.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    parser.add_argument("--limit-groups", type=int)
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE
        / "cm2_round277_source_g_depth8_residual_active_graph_strategy_probe_result.json",
    )
    args = parser.parse_args()
    ctx.prec = 256
    load_groups()
    if args.limit_groups is not None:
        GROUPS = GROUPS[: args.limit_groups]
    census = collections.Counter()
    weighted_census = collections.Counter()
    normal_forms = collections.Counter()
    hash_relations = collections.Counter()
    candidate_dispositions = collections.Counter()
    unresolved_rows = []
    with mp.get_context("fork").Pool(args.processes) as pool:
        for _group, multiplicity, counts, forms, relations, dispositions, unresolved in pool.imap_unordered(
            worker, range(len(GROUPS)), chunksize=16
        ):
            for key, value in counts:
                census[key] += value
                weighted_census[key] += multiplicity * value
            for key, value in forms:
                normal_forms[key] += value
            for key, value in relations:
                hash_relations[key] += value
            for key, value in dispositions:
                candidate_dispositions[key] += value
            unresolved_rows.extend(unresolved)
            done = sum(candidate_dispositions.values())
            if done and done % 10000 == 0:
                print(
                    json.dumps(
                        {
                            "progress_geometric_face_groups": done,
                            "total": len(GROUPS),
                            "cell_census": dict(census),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    result = {
        "status": "ROUND277_DEPTH8_RESIDUAL_ACTIVE_GRAPH_STRATEGY_PROBE__ZERO_CREDIT",
        "geometric_face_group_count": len(GROUPS),
        "terminal_cell_count": sum(census.values()),
        "candidate_weighted_terminal_cell_count": sum(weighted_census.values()),
        "candidate_disposition_census": dict(sorted(candidate_dispositions.items())),
        "terminal_cell_census": dict(sorted(census.items())),
        "candidate_weighted_terminal_cell_census": dict(sorted(weighted_census.items())),
        "active_normal_form_histogram": {
            "|".join(
                [
                    str(key[0]),
                    str(key[1]),
                    ",".join("NONE" if x is None else str(x) for x in key[2]),
                    str(key[3]),
                ]
            ): value
            for key, value in sorted(normal_forms.items(), key=lambda item: str(item[0]))
        },
        "extremal_signature_relation_histogram": {
            json.dumps(key, sort_keys=True, separators=(",", ":")): value
            for key, value in sorted(hash_relations.items(), key=lambda item: str(item[0]))
        },
        "strict_interpretation": [
            "FINITE_DEPTH_NONDETECTION_IS_NOT_AN_ABSENCE_CERTIFICATE",
            "ONLY_ACTIVE_EQUALITY_NORMAL_FORMS_ARE_AUDITED",
            "ALL_RESULTS_REMAIN_ZERO_CREDIT",
        ],
    }
    unresolved_rows.sort(key=lambda row: row["candidate_index"])
    ledger = {
        "status": "ROUND277_DEPTH8_ACTIVE_GRAPH_REMAINING_TAIL_LEDGER__ZERO_CREDIT",
        "row_count": len(unresolved_rows),
        "candidate_indices_sha256": r276.digest(
            [row["candidate_index"] for row in unresolved_rows]
        ),
        "rows": unresolved_rows,
        "strict_warning": "ROWS ARE FAIL-CLOSED AND EARN ZERO CREDIT",
    }
    ledger_path = (
        HERE
        / "cm2_round277_source_g_depth8_active_graph_remaining_tails_zero_credit.json.gz"
    )
    ledger_bytes = (
        json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    ledger_path.write_bytes(gzip.compress(ledger_bytes, compresslevel=9, mtime=0))
    result["remaining_tail_ledger"] = ledger_path.name
    result["remaining_tail_ledger_file_sha256"] = hashlib.sha256(
        ledger_path.read_bytes()
    ).hexdigest()
    result["remaining_tail_candidate_indices_sha256"] = ledger[
        "candidate_indices_sha256"
    ]
    result["strict_nonpromotion"] = {
        "expanded_occurrence_credit": 0,
        "component_edge_credit": 0,
        "maximality_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "geometric_face_group_count": len(GROUPS),
                "terminal_cell_census": result["terminal_cell_census"],
                "candidate_disposition_census": result[
                    "candidate_disposition_census"
                ],
                "remaining_tail_candidate_indices_sha256": result[
                    "remaining_tail_candidate_indices_sha256"
                ],
                "result_file_sha256": hashlib.sha256(
                    args.output.read_bytes()
                ).hexdigest(),
                "remaining_tail_ledger_file_sha256": result[
                    "remaining_tail_ledger_file_sha256"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
