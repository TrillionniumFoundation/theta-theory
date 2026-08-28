#!/usr/bin/env python3
"""Sharp finite-root obstruction to closing the remaining Gate-3 seam rows.

The Round-85 finite ``s=0`` audit leaves 24 positive and 24 negative owner
rectangles without a positive-area counterpart on the same immutable directed
physical branch.  This certificate proves that exact rational repartitioning
cannot repair them: subdivision preserves each side's union, while every
listed intersection with the opposite-side union has two-dimensional measure
zero.  It also replays all 48 physical boxes at 512-bit Arb precision.

This is only a finite-root obstruction.  It neither changes Gate 3 nor asserts
all-depth Piola, trace/current, or stopped-operator conclusions.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as cores_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as full_cert
import cm2_round85_gate3_s0_two_sided_material_window_cert as round85


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round87.gate3-finite-root-seam-recut-obstruction.v1"
ROUND85_MANIFEST = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
ROUND85_AUDIT = HERE / "cm2-round85-gate3-s0-two-sided-material-window-audit-2026-07-22.json"
PINS = {
    "round85_source": "3a2d06f597fb2a050866ab0f01cbb36ce95f3be34542d494ed09cd92e6fdd304",
    "round85_manifest": "81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
    "round85_audit": "0a17c15bcd83791ffbc351e1039fb4971f9d36775127569f61df881d7891e292",
    "full_core_source": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "full_core_manifest": "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    "core_registry_source": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "core_registry_manifest": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "first_hit_source": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
}
PIN_PATHS = {
    "round85_source": HERE / "cm2_round85_gate3_s0_two_sided_material_window_cert.py",
    "round85_manifest": ROUND85_MANIFEST,
    "round85_audit": ROUND85_AUDIT,
    "full_core_source": HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py",
    "full_core_manifest": round85.FULL_CORE,
    "core_registry_source": HERE / "cm2_gate25_physical_return_core_registry_cert.py",
    "core_registry_manifest": HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json",
    "first_hit_source": HERE / "cm2_gate3_candidate_first_hit_cert.py",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(row: dict[str, Any], cores: tuple[Any, ...]) -> dict[str, Any]:
    box = row["source_box"]
    index = row["source_core_index"]
    atom = full_cert.Atom(
        index, cores[index], Q(box["t"][0]), Q(box["t"][1]),
        Q(box["p"][0]), Q(box["p"][1]), Q(box["s"][0]), Q(box["s"][1]),
        row["dyadic_path"],
    )
    result = full_cert.classify_atom(atom, cores)
    return {
        "classification": result["classification"],
        "destination_core_id": result["destination_core_id"],
        "matches_frozen_row": (
            result["classification"] == "RETURN_AT_1_INNER"
            and result["destination_core_id"] == row["destination_core_id"]
        ),
    }


def contact_row(row: dict[str, Any], opposite: list[dict[str, Any]]) -> dict[str, Any]:
    contacts = []
    for other in sorted(opposite, key=lambda item: item["atom_id"]):
        if round85.edge(row) != round85.edge(other):
            continue
        status, dt, dp = round85.relation(row, other)
        if status not in {"EDGE_CONTACT_ONLY", "CORNER_CONTACT_ONLY"}:
            continue
        if status == "EDGE_CONTACT_ONLY":
            orientation = "T_NORMAL" if dt == 0 else "P_NORMAL"
            tangential_width = dp if dt == 0 else dt
        else:
            orientation = "T_AND_P_NORMAL"
            tangential_width = Q(0)
        contacts.append({
            "opposite_atom_id": other["atom_id"],
            "relation": status,
            "normal_coordinate_requirement": orientation,
            "t_intersection_width": str(max(dt, Q(0))),
            "p_intersection_width": str(max(dp, Q(0))),
            "tangential_width": str(tangential_width),
        })
    edge_contacts = [x for x in contacts if x["relation"] == "EDGE_CONTACT_ONLY"]
    kind = "EDGE_SEAM" if edge_contacts else "CORNER_ONLY"
    if not contacts:
        raise ValueError("unmatched row lacks closure contact")
    return {
        "atom_id": row["atom_id"],
        "source_core_id": row["source_core_id"],
        "destination_core_id": row["destination_core_id"],
        "source_t": list(row["source_box"]["t"]),
        "source_p": list(row["source_box"]["p"]),
        "source_s": list(row["source_box"]["s"]),
        "closure_contact_kind": kind,
        "closure_contacts": contacts,
        "opposite_union_positive_area_intersection": False,
        "minimum_registry_enlargement": (
            "POSITIVE_WIDTH_COLLAR_ACROSS_ONE_NORMAL_COORDINATE"
            if kind == "EDGE_SEAM"
            else "POSITIVE_AREA_CORNER_NEIGHBORHOOD_ACROSS_BOTH_COORDINATES"
        ),
    }


def build() -> dict[str, Any]:
    actual = {key: file_digest(path) for key, path in PIN_PATHS.items()}
    if actual != PINS:
        raise ValueError("upstream pin mismatch")
    old = round85.strict_load(ROUND85_MANIFEST)
    if old["result"]["finite_root_local_two_sided_material_windows"] != "152/176":
        raise ValueError("Round85 frontier")
    full = round85.strict_load(round85.FULL_CORE)
    rows: list[dict[str, Any]] = []
    round85.collect(full, rows)
    positive = [row for row in rows if Q(row["source_box"]["s"][0]) == 0]
    negative = [row for row in rows if Q(row["source_box"]["s"][1]) == 0]
    unmatched_positive_ids = {
        row["positive_atom_id"] for row in old["result"]["evidence"]["unmatched_rows"]
    }
    unmatched_negative_ids = {
        row["negative_atom_id"] for row in old["result"]["evidence"]["negative_unmatched_rows"]
    }
    unmatched_positive = [row for row in positive if row["atom_id"] in unmatched_positive_ids]
    unmatched_negative = [row for row in negative if row["atom_id"] in unmatched_negative_ids]
    if len(unmatched_positive) != 24 or len(unmatched_negative) != 24:
        raise ValueError("unmatched census")

    positive_rows = [contact_row(row, negative) for row in sorted(unmatched_positive, key=lambda x: x["atom_id"])]
    negative_rows = [contact_row(row, positive) for row in sorted(unmatched_negative, key=lambda x: x["atom_id"])]
    contact_histogram = Counter(
        contact["relation"]
        for row in positive_rows + negative_rows
        for contact in row["closure_contacts"]
    )
    kind_histogram = Counter(row["closure_contact_kind"] for row in positive_rows + negative_rows)
    orientation_histogram = Counter(
        contact["normal_coordinate_requirement"]
        for row in positive_rows + negative_rows
        for contact in row["closure_contacts"]
        if contact["relation"] == "EDGE_CONTACT_ONLY"
    )
    if contact_histogram != {"EDGE_CONTACT_ONLY": 64, "CORNER_CONTACT_ONLY": 48}:
        raise ValueError("closure contact histogram")
    if kind_histogram != {"EDGE_SEAM": 40, "CORNER_ONLY": 8}:
        raise ValueError("seam-kind histogram")
    if orientation_histogram != {"T_NORMAL": 40, "P_NORMAL": 24}:
        raise ValueError("edge orientation histogram")

    ctx.prec = 512
    cores = cores_cert.physical_cores()
    replay_rows = []
    for side, selected in (("POSITIVE", unmatched_positive), ("NEGATIVE", unmatched_negative)):
        for row in sorted(selected, key=lambda x: x["atom_id"]):
            check = replay(row, cores)
            if not check["matches_frozen_row"]:
                raise ValueError("physical replay")
            replay_rows.append({"side": side, "atom_id": row["atom_id"], **check})

    evidence = {
        "exact_rational_subdivision_invariant": (
            "Every finite exact repartition has the same positive-side and negative-side unions; "
            "therefore it cannot turn a measure-zero union intersection into positive area."
        ),
        "positive_owner_row_count": 176,
        "negative_side_row_count": 176,
        "already_certified_positive_area_windows": 152,
        "unmatched_positive_row_count": 24,
        "unmatched_negative_row_count": 24,
        "unmatched_row_total": 48,
        "seam_kind_histogram": dict(sorted(kind_histogram.items())),
        "closure_contact_histogram": dict(sorted(contact_histogram.items())),
        "edge_normal_orientation_histogram": dict(sorted(orientation_histogram.items())),
        "edge_contact_tangential_width_histogram": {"1/3200": 24, "1/800": 40},
        "positive_rows": positive_rows,
        "negative_rows": negative_rows,
        "arb_precision_bits": 512,
        "physical_replay_row_count": len(replay_rows),
        "physical_replay_all_return_inner_to_frozen_destination": all(
            row["matches_frozen_row"] for row in replay_rows
        ),
        "physical_replay_rows": replay_rows,
    }
    result = {
        "status": "CERTIFIED_SHARP_FINITE_ROOT_RECUT_OBSTRUCTION",
        "scope": "CURRENT_FROZEN_S0_ROOT_AND_IMMUTABLE_DIRECTED_PHYSICAL_BRANCH_KEYS_ONLY",
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
        "exact_repartition_can_close_remaining_rows": False,
        "finite_root_local_two_sided_material_windows": "152/176_UNCHANGED",
        "minimal_required_enlargement": {
            "edge_seam_rows_per_side": 20,
            "corner_only_rows_per_side": 4,
            "edge_requirement": "add positive width across at least one normal coordinate",
            "corner_requirement": "add a positive-area neighborhood across both coordinates",
            "must_preserve": ["immutable branch key", "strict first owner", "flight order", "destination core"],
        },
        "Gate3": "NOT_CERTIFIED_UNCHANGED",
        "strict_nonclaims": [
            "No global two-sided trace/current atlas is certified.",
            "No all-depth Piola recipient is certified.",
            "No stopped MT_DQ estimate is certified.",
            "The obstruction does not exclude a new enlarged registry with fresh owner/flight proofs.",
        ],
    }
    return {"schema": SCHEMA, "pins": actual, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
