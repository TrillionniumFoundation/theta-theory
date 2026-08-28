#!/usr/bin/env python3
"""Exact two-sided s=0 material-window audit on the finite Round-69 root."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.gate3-s0-two-sided-material-window.v1"
FULL_CORE = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
ROUND69 = HERE / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
FROZEN_PINS = {
    "full_core_return_manifest": "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    "full_core_return_source": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "round69_base_root_manifest": "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result
    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    return value


def collect(value: Any, output: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if value.get("classification") == "RETURN_AT_1_INNER" and "source_box" in value:
            output.append(value)
        for child in value.values():
            collect(child, output)
    elif isinstance(value, list):
        for child in value:
            collect(child, output)


def edge(row: dict[str, Any]) -> tuple[str, str]:
    return row["source_core_id"], row["destination_core_id"]


def box(row: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    return tuple(map(Q, row["source_box"]["t"] + row["source_box"]["p"]))  # type: ignore[return-value]


def interval_string(a: Q, b: Q) -> list[str]:
    return [str(a), str(b)]


def relation(positive: dict[str, Any], negative: dict[str, Any]) -> tuple[str, Q, Q]:
    a = box(positive)
    b = box(negative)
    dt = min(a[1], b[1]) - max(a[0], b[0])
    dp = min(a[3], b[3]) - max(a[2], b[2])
    if dt > 0 and dp > 0:
        return ("EXACT_BOX" if a == b else "PARTIAL_POSITIVE_AREA", dt, dp)
    if (dt == 0 and dp > 0) or (dp == 0 and dt > 0):
        return "EDGE_CONTACT_ONLY", dt, dp
    if dt == 0 and dp == 0:
        return "CORNER_CONTACT_ONLY", dt, dp
    return "DISJOINT", dt, dp


def build() -> dict[str, Any]:
    actual_pins = {
        "full_core_return_manifest": file_digest(FULL_CORE),
        "full_core_return_source": file_digest(HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py"),
        "round69_base_root_manifest": file_digest(ROUND69),
    }
    if actual_pins != FROZEN_PINS:
        raise ValueError("frozen upstream pin mismatch")
    full = strict_load(FULL_CORE)
    round69 = strict_load(ROUND69)
    rows: list[dict[str, Any]] = []
    collect(full, rows)
    positive = [row for row in rows if Q(row["source_box"]["s"][0]) == 0]
    negative = [row for row in rows if Q(row["source_box"]["s"][1]) == 0]
    if len(rows) != 4216 or len(positive) != 176 or len(negative) != 176:
        raise ValueError("RETURN_AT_1_INNER s=0 census")
    if round69["result"]["actual_base_s_return_root"]["owned_by_lower_closed_upper_open_rule"] != 176:
        raise ValueError("Round69 owner census")

    pos_by_edge: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    neg_by_edge: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in positive:
        pos_by_edge[edge(row)].append(row)
    for row in negative:
        neg_by_edge[edge(row)].append(row)
    if set(pos_by_edge) != set(neg_by_edge) or len(pos_by_edge) != 16:
        raise ValueError("directed branch-edge registry")

    comparison_rows = []
    relation_histogram: Counter[str] = Counter()
    for branch_edge in sorted(pos_by_edge):
        for pos in sorted(pos_by_edge[branch_edge], key=lambda row: row["atom_id"]):
            for neg in sorted(neg_by_edge[branch_edge], key=lambda row: row["atom_id"]):
                status, dt, dp = relation(pos, neg)
                relation_histogram[status] += 1
                comparison_rows.append({
                    "source_core_id": branch_edge[0],
                    "destination_core_id": branch_edge[1],
                    "positive_atom_id": pos["atom_id"],
                    "negative_atom_id": neg["atom_id"],
                    "relation": status,
                    "t_intersection_width": str(max(dt, Q(0))),
                    "p_intersection_width": str(max(dp, Q(0))),
                })
    expected_histogram = {
        "CORNER_CONTACT_ONLY": 320,
        "DISJOINT": 1640,
        "EDGE_CONTACT_ONLY": 376,
        "EXACT_BOX": 104,
        "PARTIAL_POSITIVE_AREA": 64,
    }
    if dict(sorted(relation_histogram.items())) != expected_histogram:
        raise ValueError("pair relation histogram")

    window_rows = []
    unmatched_rows = []
    for pos in sorted(positive, key=lambda row: row["atom_id"]):
        candidates = []
        contacts: Counter[str] = Counter()
        for neg in neg_by_edge[edge(pos)]:
            status, dt, dp = relation(pos, neg)
            contacts[status] += 1
            if dt > 0 and dp > 0:
                s_positive = Q(pos["source_box"]["s"][1])
                s_negative = -Q(neg["source_box"]["s"][0])
                radius = min(dt / 2, dp / 2, s_positive, s_negative)
                candidates.append((radius, status == "EXACT_BOX", neg["atom_id"], neg, dt, dp))
        if not candidates:
            unmatched_rows.append({
                "positive_atom_id": pos["atom_id"],
                "source_core_id": pos["source_core_id"],
                "destination_core_id": pos["destination_core_id"],
                "source_t": list(pos["source_box"]["t"]),
                "source_p": list(pos["source_box"]["p"]),
                "same_branch_negative_box_count": len(neg_by_edge[edge(pos)]),
                "relation_histogram": dict(sorted(contacts.items())),
                "positive_area_counterpart_count": 0,
                "status": "UNMATCHED_BRANCH_SEAM_OR_ONE_SIDED_CELL",
            })
            continue
        candidates.sort(key=lambda item: (-item[0], not item[1], item[2]))
        radius, exact, _atom_id, neg, dt, dp = candidates[0]
        a, b = box(pos), box(neg)
        t0, t1 = max(a[0], b[0]), min(a[1], b[1])
        p0, p1 = max(a[2], b[2]), min(a[3], b[3])
        window_rows.append({
            "positive_atom_id": pos["atom_id"],
            "negative_atom_id": neg["atom_id"],
            "source_core_id": pos["source_core_id"],
            "destination_core_id": pos["destination_core_id"],
            "pairing": "EXACT_BOX" if exact else "SAME_BRANCH_POSITIVE_AREA_INTERSECTION",
            "common_t": interval_string(t0, t1),
            "common_p": interval_string(p0, p1),
            "common_s": interval_string(-radius, radius),
            "t_width": str(dt),
            "p_width": str(dp),
            "certified_L_infinity_radius": str(radius),
        })

    negative_unmatched_rows = []
    for neg in sorted(negative, key=lambda row: row["atom_id"]):
        contacts: Counter[str] = Counter()
        positive_area = 0
        for pos in pos_by_edge[edge(neg)]:
            status, dt, dp = relation(pos, neg)
            contacts[status] += 1
            positive_area += int(dt > 0 and dp > 0)
        if positive_area == 0:
            negative_unmatched_rows.append({
                "negative_atom_id": neg["atom_id"],
                "source_core_id": neg["source_core_id"],
                "destination_core_id": neg["destination_core_id"],
                "source_t": list(neg["source_box"]["t"]),
                "source_p": list(neg["source_box"]["p"]),
                "same_branch_positive_box_count": len(pos_by_edge[edge(neg)]),
                "relation_histogram": dict(sorted(contacts.items())),
                "positive_area_counterpart_count": 0,
                "status": "UNMATCHED_BRANCH_SEAM_OR_ONE_SIDED_CELL",
            })

    window_histogram = Counter(row["pairing"] for row in window_rows)
    if len(window_rows) != 152 or len(unmatched_rows) != 24:
        raise ValueError("owner coverage frontier")
    if len(negative_unmatched_rows) != 24:
        raise ValueError("negative-side coverage frontier")
    if window_histogram != {"EXACT_BOX": 104, "SAME_BRANCH_POSITIVE_AREA_INTERSECTION": 48}:
        raise ValueError("window pairing histogram")
    if min(Q(row["certified_L_infinity_radius"]) for row in window_rows) != Q(1, 6400):
        raise ValueError("uniform finite-root radius")

    evidence = {
        "exact_rational_arithmetic": True,
        "RETURN_AT_1_INNER_row_count": 4216,
        "s0_touching_box_count": 352,
        "positive_side_owner_box_count": 176,
        "negative_side_box_count": 176,
        "directed_physical_branch_edge_count": 16,
        "same_branch_pair_comparison_count": len(comparison_rows),
        "pair_relation_histogram": expected_histogram,
        "two_sided_window_row_count": len(window_rows),
        "window_pairing_histogram": dict(sorted(window_histogram.items())),
        "covered_positive_owner_row_count": len(window_rows),
        "unmatched_positive_owner_row_count": len(unmatched_rows),
        "covered_negative_side_box_count": len(negative) - len(negative_unmatched_rows),
        "unmatched_negative_side_box_count": len(negative_unmatched_rows),
        "uniform_certified_L_infinity_radius": "1/6400",
        "comparison_rows": comparison_rows,
        "window_rows": window_rows,
        "unmatched_rows": unmatched_rows,
        "negative_unmatched_rows": negative_unmatched_rows,
    }
    result = {
        "status": "CERTIFIED_152_OF_176_FINITE_ROOT_TWO_SIDED_WINDOWS__24_EXACT_BRANCH_SEAM_OBSTRUCTIONS",
        "scope": "Round69 finite s=0 base-owner root only",
        "finite_root_local_two_sided_material_windows": "152/176",
        "full_176_owner_row_two_sided_cover": "NOT_CERTIFIED",
        "obstruction": "24 owner rectangles and 24 negative-side rectangles have zero positive-area counterpart in the opposite-side union on the same directed physical branch edge",
        "adjacency_cannot_close_obstruction": "edge/corner contact has zero two-dimensional material radius",
        "Gate3": "NOT_CERTIFIED_UNCHANGED",
        "strict_nonclaims": [
            "no all-cell or all-depth common material radius",
            "no uniform Piola remainder or strong two-sided trace/current",
            "no claim that the 24 seams cannot be closed after a refined physical repartition",
            "no promotion from the finite Round69 base root to a global material registry",
        ],
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(FROZEN_PINS), "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
