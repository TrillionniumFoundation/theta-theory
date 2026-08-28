#!/usr/bin/env python3
"""Reconstruct and stratify Round277 depth-4 fail-closed residuals.

This is deliberately a zero-credit diagnostic.  In particular,
NO_PATCH_AT_DEPTH_4 is not an absence proof.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
from pathlib import Path

import cm2_round276_source_g_collar_region_face_binding_probe as P
import cm2_round277_source_g_collar_common_face_match_probe as R277

HERE = Path(__file__).resolve().parent


def find_patch(i):
    a, b, h, chart, target, axis, coordinate, overlap = R277.CAND[i]
    pending = [(overlap, 0, [])]
    while pending:
        rect, depth, path = pending.pop()
        q = []
        j = 0
        for k in range(3):
            if k == axis:
                q += [coordinate, coordinate]
            else:
                q += list(rect[j])
                j += 1
        if R277.evaluate(chart, target, h, q, f"r277r:{i}:f:{depth}"):
            return q, path
        if depth == R277.FACE_DEPTH:
            continue
        widths = [x[1] - x[0] for x in rect]
        split = 0 if widths[0] >= widths[1] else 1
        mid = (rect[split][0] + rect[split][1]) / 2
        for side, z in enumerate(
            ((rect[split][0], mid), (mid, rect[split][1]))
        ):
            child = list(rect)
            child[split] = z
            pending.append((tuple(child), depth + 1, path + [f"{split}:{side}"]))
    return None


def face_only_worker(i):
    """Cheap residual reconstruction: do not replay already-tested corridors."""
    _, _, h, chart, target, axis, coordinate, overlap = R277.CAND[i]
    pending = [(overlap, 0, [])]
    terminal_profile = collections.Counter()
    while pending:
        rect, depth, path = pending.pop()
        q = []
        j = 0
        for k in range(3):
            if k == axis:
                q += [coordinate, coordinate]
            else:
                q += list(rect[j])
                j += 1
        signature, reasons = R277.R.dynamic_signature(
            chart, R277.R.atlas.AtlasBox(*q, 0, f"r277rf:{i}:{depth}"), target, R277.TABLES
        )
        if signature is not None:
            actual = P.digest(R277.payload(signature, chart))
            if actual == h:
                return ("FOUND_POSITIVE_MATCH_PATCH__CORRIDORS_NOT_REPLAYED", i, path)
            category = "STRICT_DIFFERENT_COMPLETE_SIGNATURE"
        else:
            category = "REJECT:" + "|".join(sorted(reasons))
        if depth == R277.FACE_DEPTH:
            terminal_profile[category] += 1
            continue
        widths = [x[1] - x[0] for x in rect]
        split = 0 if widths[0] >= widths[1] else 1
        mid = (rect[split][0] + rect[split][1]) / 2
        for side, z in enumerate(
            ((rect[split][0], mid), (mid, rect[split][1]))
        ):
            child = list(rect)
            child[split] = z
            pending.append((tuple(child), depth + 1, path + [f"{split}:{side}"]))
    return (
        "FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT",
        i,
        [[category, count] for category, count in sorted(terminal_profile.items())],
    )


def corrected_worker(i):
    """Round277 worker with corridor side inferred from geometry, not ID order."""
    a, b, h, chart, target, axis, coordinate, _ = R277.CAND[i]
    patch = find_patch(i)
    if patch is None:
        return ("FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT", i, None)
    q, path = patch
    directions = []
    for rid in (a, b):
        box = R277.BOX[rid]
        is_negative = box[2 * axis + 1] == coordinate
        is_positive = box[2 * axis] == coordinate
        if is_negative == is_positive:
            return ("FAILCLOSED_INVALID_FACE_ORIENTATION", i, None)
        directions.append((rid, is_negative))
    if sum(int(negative) for _, negative in directions) != 1:
        return ("FAILCLOSED_INVALID_FACE_ORIENTATION", i, None)
    depths = []
    for rid, negative in directions:
        box = R277.BOX[rid]
        span = box[2 * axis + 1] - box[2 * axis]
        ok = None
        for depth in range(1, 25):
            z = list(q)
            width = span / (2**depth)
            z[2 * axis : 2 * axis + 2] = (
                [coordinate - width, coordinate]
                if negative
                else [coordinate, coordinate + width]
            )
            if R277.evaluate(chart, target, h, z, f"r277r:{i}:c:{depth}"):
                ok = depth
                break
        if ok is None:
            return ("FAILCLOSED_NO_TWO_SIDED_INWARD_CORRIDOR", i, None)
        depths.append(ok)
    return ("ACCEPT_POSITIVE_MATCH_PATCH_AND_TWO_INWARD_CORRIDORS", i, (path, depths))


def round_metadata():
    """Return source-round sets and compact signature metadata by node."""
    result = {}
    for rnd, name, ledger, leaf_field, _ in P.SOURCES:
        for row in P.load(name)[ledger]["rows"]:
            sig = row["local_return_signature"]
            h = row.get("complete_10_field_return_signature_sha256", P.digest(sig))
            node = result.setdefault(
                (row[leaf_field], h),
                {
                    "rounds": set(),
                    "target_chart": sig["target_chart"],
                    "target_lift": sig["target_lift"],
                    "official_key_id": sig["official_key_id"],
                    "pattern": ",".join(sig["signed_wall_word"]),
                    "event_count": len(sig["ordered_integer_wall_events"]),
                    "outgoing_cell": sig["outgoing_cell"],
                },
            )
            node["rounds"].add(rnd)
    return result


def stratum_for(i, meta):
    a, b, h, chart, target, axis, coordinate, overlap = R277.CAND[i]
    ma = meta[(a, h)]
    mb = meta[(b, h)]
    ra = "+".join(map(str, sorted(ma["rounds"])))
    rb = "+".join(map(str, sorted(mb["rounds"])))
    rounds = "/".join(sorted((ra, rb)))
    return {
        "round_pair": rounds,
        "chart": chart,
        "axis": axis,
        "owner_target": target,
        "target_chart": ma["target_chart"],
        "official_key_id": ma["official_key_id"],
        "pattern": ma["pattern"],
        "event_count": ma["event_count"],
        "outgoing_cell": ma["outgoing_cell"],
        "signature_sha256": h,
        "face_group": P.digest(
            [a, b, chart, target, axis, str(coordinate), [[str(x), str(y)] for x, y in overlap]]
        ),
    }


def run_indices(indices, processes, collect_failures=False, worker_fn=corrected_worker):
    counts = collections.Counter()
    details = {}
    failures = []
    ctx = mp.get_context("fork")
    with ctx.Pool(processes) as pool:
        for status, i, detail in pool.imap_unordered(worker_fn, indices, chunksize=32):
            counts[status] += 1
            if status.startswith("FAILCLOSED"):
                if collect_failures:
                    failures.append((status, i, detail))
            elif detail is not None:
                details[i] = detail
            done = sum(counts.values())
            if done and done % 10000 == 0:
                print(
                    json.dumps(
                        {"progress": done, "total": len(indices), "histogram": dict(counts)},
                        sort_keys=True,
                    ),
                    flush=True,
                )
    return counts, details, failures


def stratified_sample(residual, meta, per_stratum):
    strata = collections.defaultdict(list)
    for i in residual:
        s = stratum_for(i, meta)
        strata[(s["round_pair"], s["chart"], s["axis"], s["owner_target"])].append(i)
    sample = []
    for key in sorted(strata, key=str):
        rows = strata[key]
        # Deterministic quantiles, including both endpoints when possible.
        if len(rows) <= per_stratum:
            sample.extend(rows)
        elif per_stratum == 1:
            sample.append(rows[len(rows) // 2])
        else:
            sample.extend(rows[(j * (len(rows) - 1)) // (per_stratum - 1)] for j in range(per_stratum))
    return sorted(set(sample)), strata


def top(counter, n=100):
    return [[list(k) if isinstance(k, tuple) else k, v] for k, v in counter.most_common(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    ap.add_argument("--expected-residual", type=int, default=89792)
    ap.add_argument("--sample-per-stratum", type=int, default=4)
    ap.add_argument("--deep-depth", type=int, default=8)
    ap.add_argument("--deeper-depth", type=int, default=12)
    ap.add_argument("--deeper-sample-limit", type=int, default=128)
    args = ap.parse_args()

    cache_path = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache_path.exists():
        R277.CAND, R277.BOX, R277.TABLES = pickle.loads(cache_path.read_bytes())
    else:
        R277.build()
        cache_path.write_bytes(
            pickle.dumps((R277.CAND, R277.BOX, R277.TABLES), protocol=pickle.HIGHEST_PROTOCOL)
        )
    meta = round_metadata()
    orientation = collections.Counter()
    for a, b, _, _, _, axis, coordinate, _ in R277.CAND:
        a_negative = R277.BOX[a][2 * axis + 1] == coordinate
        b_positive = R277.BOX[b][2 * axis] == coordinate
        orientation[
            "LEXICOGRAPHIC_ORDER_MATCHES_GEOMETRIC_NEGATIVE_POSITIVE"
            if a_negative and b_positive
            else "LEXICOGRAPHIC_ORDER_REVERSES_GEOMETRIC_NEGATIVE_POSITIVE"
        ] += 1

    # Reconstruct the finite-depth residual index set exactly.
    R277.FACE_DEPTH = 4
    counts4, _, failures4 = run_indices(
        list(range(len(R277.CAND))),
        args.processes,
        collect_failures=True,
        worker_fn=face_only_worker,
    )
    residual = [
        i
        for status, i, _ in failures4
        if status == "FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT"
    ]
    terminal_profiles = {
        i: detail
        for status, i, detail in failures4
        if status == "FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT"
    }
    residual.sort()
    if len(residual) != args.expected_residual:
        raise AssertionError((len(residual), args.expected_residual))

    sample8, strata = stratified_sample(residual, meta, args.sample_per_stratum)
    R277.FACE_DEPTH = args.deep_depth
    counts8, details8, failures8 = run_indices(
        sample8, args.processes, collect_failures=True
    )
    still8 = sorted(
        i for status, i, _ in failures8
        if status == "FAILCLOSED_NO_POSITIVE_MATCH_PATCH_AT_DEPTH_LIMIT"
    )
    # A bounded deterministic sample of depth-8 survivors at depth 12.
    sample12 = still8[: args.deeper_sample_limit]
    R277.FACE_DEPTH = args.deeper_depth
    counts12, _, _ = run_indices(sample12, args.processes)

    counters = {
        "round_pair": collections.Counter(),
        "chart": collections.Counter(),
        "axis": collections.Counter(),
        "chart_axis": collections.Counter(),
        "owner_target": collections.Counter(),
        "round_pair_chart_axis": collections.Counter(),
        "target_chart": collections.Counter(),
        "official_key_id": collections.Counter(),
        "pattern": collections.Counter(),
        "event_count": collections.Counter(),
        "outgoing_cell": collections.Counter(),
        "signature_sha256": collections.Counter(),
        "face_group": collections.Counter(),
        "terminal_cell_reason": collections.Counter(),
        "terminal_profile": collections.Counter(),
    }
    rows = []
    for i in residual:
        s = stratum_for(i, meta)
        counters["round_pair"][s["round_pair"]] += 1
        counters["chart"][s["chart"]] += 1
        counters["axis"][str(s["axis"])] += 1
        counters["chart_axis"][(s["chart"], s["axis"])] += 1
        counters["owner_target"][s["owner_target"]] += 1
        counters["round_pair_chart_axis"][(s["round_pair"], s["chart"], s["axis"])] += 1
        for key in (
            "target_chart",
            "official_key_id",
            "pattern",
            "event_count",
            "outgoing_cell",
            "signature_sha256",
            "face_group",
        ):
            counters[key][str(s[key])] += 1
        profile = terminal_profiles[i]
        for category, count in profile:
            counters["terminal_cell_reason"][category] += count
        counters["terminal_profile"][json.dumps(profile, separators=(",", ":"))] += 1
        rows.append({"candidate_index": i, "depth4_terminal_profile": profile, **s})

    ledger_path = HERE / "cm2_round277_source_g_depth4_residual_indices_zero_credit.json.gz"
    ledger = {
        "status": "ROUND277_DEPTH4_RESIDUAL_INDEX_LEDGER__ZERO_CREDIT",
        "face_depth": 4,
        "candidate_universe_count": len(R277.CAND),
        "residual_count": len(residual),
        "candidate_indices_sha256": P.digest(residual),
        "rows": rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    ledger_bytes = (
        json.dumps(ledger, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    ledger_path.write_bytes(gzip.compress(ledger_bytes, compresslevel=9, mtime=0))
    ledger_file_sha256 = hashlib.sha256(ledger_path.read_bytes()).hexdigest()

    result = {
        "status": "ROUND277_DEPTH4_RESIDUAL_STRATIFICATION__ZERO_CREDIT",
        "candidate_universe_count": len(R277.CAND),
        "original_probe_corridor_orientation_audit": dict(sorted(orientation.items())),
        "depth4_disposition_histogram_replay": dict(sorted(counts4.items())),
        "depth4_residual_count": len(residual),
        "depth4_residual_candidate_indices_sha256": P.digest(residual),
        "depth4_residual_ledger": ledger_path.name,
        "depth4_residual_ledger_file_sha256": ledger_file_sha256,
        "unique_residual_face_group_count": len(counters["face_group"]),
        "classification": {
            k: top(v, 200 if k in {"round_pair_chart_axis", "signature_sha256"} else 100)
            for k, v in counters.items()
        },
        "depth8_stratified_sample": {
            "stratum_definition": ["round_pair", "chart", "axis", "owner_target"],
            "stratum_count": len(strata),
            "sample_count": len(sample8),
            "sample_indices_sha256": P.digest(sample8),
            "disposition_histogram": dict(sorted(counts8.items())),
        },
        "depth12_sample_of_depth8_survivors": {
            "sample_limit": args.deeper_sample_limit,
            "sample_count": len(sample12),
            "sample_indices_sha256": P.digest(sample12),
            "disposition_histogram": dict(sorted(counts12.items())),
        },
        "strict_interpretation": [
            "NO_PATCH_AT_A_FINITE_DEPTH_IS_FAIL_CLOSED, NOT AN ABSENCE CERTIFICATE",
            "ALL_ACCEPTANCES_REMAIN PROBE-LEVEL AND EARN ZERO OCCURRENCE/EDGE CREDIT",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
