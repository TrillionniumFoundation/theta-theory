#!/usr/bin/env python3
"""Positive-width collar closure of the finite Round-69 Gate-3 seam rows.

Round 87 proves that exact recutting cannot repair the 24 positive and 24
negative unmatched rows: their current unions only meet opposite-side boxes
on edges or corners.  This append-only certificate performs the smallest
kind of legal repair.  It places an exact rational collar across one selected
contact for every unmatched row, keeps the collar strictly inside its pinned
physical source core, and replays collision geometry, strict flight order and
the unique destination core with Arb on the whole three-dimensional collar.

The result closes only the finite ``s=0`` two-sided material-window census.
It does not supply the all-depth Piola, trace/current or stopped-operator
fields required for global Gate 3.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as full_cert
import cm2_round85_gate3_s0_two_sided_material_window_cert as round85


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round88.gate3-finite-root-collar-extension.v1"
ROUND85 = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"
ROUND87 = HERE / "cm2-round87-gate3-finite-root-seam-recut-obstruction-2026-07-22.json"
ROUND87_AUDIT = HERE / "cm2-round87-gate3-finite-root-seam-recut-obstruction-audit-2026-07-22.json"

# The transverse radius is smaller than half of every selected edge overlap;
# the s-radius is exactly the already certified Round-85 finite-root radius.
TP_RADIUS = Q(1, 4096)
S_RADIUS = Q(1, 6400)

PIN_PATHS = {
    "round87_source": HERE / "cm2_round87_gate3_finite_root_seam_recut_obstruction_cert.py",
    "round87_verifier": HERE / "cm2_round87_gate3_finite_root_seam_recut_obstruction_verifier.py",
    "round87_manifest": ROUND87,
    "round87_audit": ROUND87_AUDIT,
    "round85_source": HERE / "cm2_round85_gate3_s0_two_sided_material_window_cert.py",
    "round85_manifest": ROUND85,
    "round85_audit": HERE / "cm2-round85-gate3-s0-two-sided-material-window-audit-2026-07-22.json",
    "full_core_source": HERE / "cm2_gate34_full_core_return_adaptive_frontier_cert.py",
    "full_core_manifest": round85.FULL_CORE,
    "core_registry_source": HERE / "cm2_gate25_physical_return_core_registry_cert.py",
    "core_registry_manifest": HERE / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json",
    "first_hit_source": HERE / "cm2_gate3_candidate_first_hit_cert.py",
    "first_hit_manifest": HERE / "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json",
    "gate5_key_source": HERE / "cm2_gate5_return_word_three_norm_frontier_cert.py",
    "gate5_key_manifest": HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
}
PINS = {
    "round87_source": "de539d4fc442b9369dde4b48b9971e5387c20ba94596bbc206651e1383466821",
    "round87_verifier": "59820b7af6720efb111876eb68183a523d96e220ebc6948e947f93a1dc66d848",
    "round87_manifest": "2083f87923be4b5e0c306badb7946fa0f8edc27762a413696156d02b0432a921",
    "round87_audit": "93df2fc910a315b7513d42c1e9623b5306f3768eb85caefbdfefba642cacdad8",
    "round85_source": "3a2d06f597fb2a050866ab0f01cbb36ce95f3be34542d494ed09cd92e6fdd304",
    "round85_manifest": "81356d91e1725c9f454ac010b264a0bd1fbd92b2892cca602f1ff5f9ae64b2c7",
    "round85_audit": "0a17c15bcd83791ffbc351e1039fb4971f9d36775127569f61df881d7891e292",
    "full_core_source": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "full_core_manifest": "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    "core_registry_source": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "core_registry_manifest": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "first_hit_source": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "first_hit_manifest": "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    "gate5_key_source": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "gate5_key_manifest": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def interval(a: Q, b: Q) -> list[str]:
    return [str(a), str(b)]


def selected_contact(row: dict[str, Any], opposite: list[dict[str, Any]]) -> tuple[str, Q, Q, dict[str, Any]]:
    choices: list[tuple[str, Q, Q, dict[str, Any]]] = []
    for other in opposite:
        if round85.edge(row) != round85.edge(other):
            continue
        relation, dt, dp = round85.relation(row, other)
        if relation in {"EDGE_CONTACT_ONLY", "CORNER_CONTACT_ONLY"}:
            choices.append((relation, dt, dp, other))
    if not choices:
        raise ValueError("unmatched row without opposite contact")
    # Prefer a one-coordinate edge collar; then maximize its exact tangential
    # overlap.  Atom id is a deterministic final tie-breaker.
    choices.sort(key=lambda x: (x[0] != "EDGE_CONTACT_ONLY", -max(x[1], x[2]), x[3]["atom_id"]))
    return choices[0]


def collar_row(side: str, row: dict[str, Any], opposite: list[dict[str, Any]], cores: tuple[Any, ...]) -> dict[str, Any]:
    relation, dt, dp, other = selected_contact(row, opposite)
    a, b = round85.box(row), round85.box(other)
    if dt == 0:
        t_center = max(a[0], b[0])
        p_center = (max(a[2], b[2]) + min(a[3], b[3])) / 2 if dp > 0 else max(a[2], b[2])
        normal = "T" if dp > 0 else "T_AND_P"
    else:
        t_center = (max(a[0], b[0]) + min(a[1], b[1])) / 2
        p_center = max(a[2], b[2])
        normal = "P"
    bounds = (
        t_center - TP_RADIUS, t_center + TP_RADIUS,
        p_center - TP_RADIUS, p_center + TP_RADIUS,
    )
    core = cores[row["source_core_index"]]
    source_margins = (
        bounds[0] - core.t0, core.t1 - bounds[1],
        bounds[2] - core.p0, core.p1 - bounds[3],
    )
    if min(source_margins) <= 0:
        raise ValueError("collar leaves source core")
    atom = full_cert.Atom(
        row["source_core_index"], core,
        bounds[0], bounds[1], bounds[2], bounds[3],
        -S_RADIUS, S_RADIUS, "round88-collar",
    )
    classification = full_cert.classify_atom(atom, cores)
    if (
        classification["classification"] != "RETURN_AT_1_INNER"
        or classification["destination_core_id"] != row["destination_core_id"]
    ):
        raise ValueError("collar physical replay")
    original = round85.box(row)
    counterpart = round85.box(other)
    row_dt = min(bounds[1], original[1]) - max(bounds[0], original[0])
    row_dp = min(bounds[3], original[3]) - max(bounds[2], original[2])
    other_dt = min(bounds[1], counterpart[1]) - max(bounds[0], counterpart[0])
    other_dp = min(bounds[3], counterpart[3]) - max(bounds[2], counterpart[2])
    if min(row_dt, row_dp, other_dt, other_dp) <= 0:
        raise ValueError("collar lacks positive-area incidence")
    return {
        "side": side,
        "unmatched_atom_id": row["atom_id"],
        "selected_opposite_atom_id": other["atom_id"],
        "source_core_index": row["source_core_index"],
        "source_core_id": row["source_core_id"],
        "destination_core_id": row["destination_core_id"],
        "contact_relation": relation,
        "normal_coordinates_extended": normal,
        "contact_t_width": str(max(dt, Q(0))),
        "contact_p_width": str(max(dp, Q(0))),
        "collar": {
            "t": interval(bounds[0], bounds[1]),
            "p": interval(bounds[2], bounds[3]),
            "s": interval(-S_RADIUS, S_RADIUS),
        },
        "strict_source_core_minimum_margin": str(min(source_margins)),
        "unmatched_row_positive_area_intersection": [str(row_dt), str(row_dp)],
        "opposite_row_positive_area_intersection": [str(other_dt), str(other_dp)],
        "strict_first_owner_inherited_from_whole_parent_core": True,
        "whole_collar_collision_classification": classification["classification"],
        "whole_collar_destination_core_id": classification["destination_core_id"],
        "whole_collar_output_enclosures": classification["output_enclosures"],
    }


def build() -> dict[str, Any]:
    actual = {key: file_digest(path) for key, path in PIN_PATHS.items()}
    if actual != PINS:
        raise ValueError("upstream pin mismatch")
    old85 = round85.strict_load(ROUND85)
    old87 = round85.strict_load(ROUND87)
    audit87 = round85.strict_load(ROUND87_AUDIT)
    if old85["result"]["finite_root_local_two_sided_material_windows"] != "152/176":
        raise ValueError("Round85 frontier")
    if old87["result"]["finite_root_local_two_sided_material_windows"] != "152/176_UNCHANGED":
        raise ValueError("Round87 frontier")
    if audit87["result"]["verdict"] != "PASS":
        raise ValueError("Round87 audit")

    full = round85.strict_load(round85.FULL_CORE)
    all_rows: list[dict[str, Any]] = []
    round85.collect(full, all_rows)
    positive = [row for row in all_rows if Q(row["source_box"]["s"][0]) == 0]
    negative = [row for row in all_rows if Q(row["source_box"]["s"][1]) == 0]
    positive_ids = {x["positive_atom_id"] for x in old85["result"]["evidence"]["unmatched_rows"]}
    negative_ids = {x["negative_atom_id"] for x in old85["result"]["evidence"]["negative_unmatched_rows"]}
    unmatched_positive = [row for row in positive if row["atom_id"] in positive_ids]
    unmatched_negative = [row for row in negative if row["atom_id"] in negative_ids]
    if len(unmatched_positive) != 24 or len(unmatched_negative) != 24:
        raise ValueError("unmatched census")

    ctx.prec = 512
    cores = core_cert.physical_cores()
    parent_indices = sorted({row["source_core_index"] for row in unmatched_positive + unmatched_negative})
    parent_owner_rows = [core_cert.certify_core(cores[index]) for index in parent_indices]
    if not all(row["strict_first_hit"] for row in parent_owner_rows):
        raise ValueError("parent first-owner replay")
    rows = [
        collar_row("POSITIVE_OWNER", row, negative, cores)
        for row in sorted(unmatched_positive, key=lambda x: x["atom_id"])
    ] + [
        collar_row("NEGATIVE_SIDE", row, positive, cores)
        for row in sorted(unmatched_negative, key=lambda x: x["atom_id"])
    ]
    relation_histogram = Counter(row["contact_relation"] for row in rows)
    side_histogram = Counter(row["side"] for row in rows)
    if relation_histogram != {"EDGE_CONTACT_ONLY": 40, "CORNER_CONTACT_ONLY": 8}:
        raise ValueError("selected contact histogram")
    if side_histogram != {"POSITIVE_OWNER": 24, "NEGATIVE_SIDE": 24}:
        raise ValueError("side histogram")
    unique_collars = {
        canonical({
            "source": row["source_core_id"],
            "destination": row["destination_core_id"],
            "collar": row["collar"],
        }) for row in rows
    }
    if len(unique_collars) != 40:
        raise ValueError("unique collar census")
    minimum_source_margin = min(Q(row["strict_source_core_minimum_margin"]) for row in rows)
    if minimum_source_margin != Q(7, 102400):
        raise ValueError("source margin frontier")

    evidence = {
        "arb_precision_bits": 512,
        "old_certified_positive_owner_rows": 152,
        "new_positive_owner_collar_rows": 24,
        "new_negative_side_collar_rows": 24,
        "collar_incidence_row_count": 48,
        "unique_physical_collar_count": len(unique_collars),
        "selected_contact_histogram": dict(sorted(relation_histogram.items())),
        "side_histogram": dict(sorted(side_histogram.items())),
        "uniform_t_p_radius": str(TP_RADIUS),
        "uniform_s_radius": str(S_RADIUS),
        "minimum_strict_source_core_margin": str(minimum_source_margin),
        "parent_source_core_count": len(parent_indices),
        "parent_source_core_indices": parent_indices,
        "parent_first_owner_rows_sha256": digest(parent_owner_rows),
        "all_parent_cores_replayed_strict_first_owner": True,
        "all_collars_wholly_return_inner_to_immutable_destination": True,
        "all_collars_have_positive_area_in_both_contacting_rows": True,
        "collar_rows": rows,
    }
    result = {
        "status": "CERTIFIED_FINITE_ROOT_COLLAR_EXTENSION",
        "scope": "ROUND69_FINITE_S0_ROOT_WITH_EXPLICIT_ENLARGED_COLLAR_REGISTRY_ONLY",
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
        "finite_root_local_two_sided_material_windows": "176/176_CERTIFIED_ON_ENLARGED_COLLAR_REGISTRY",
        "old_registry_recut_obstruction": "PRESERVED_ROUND87",
        "new_registry_operation": "40_UNIQUE_POSITIVE_WIDTH_OR_AREA_COLLARS_WITH_48_SIDE_INCIDENCES",
        "branch_key_owner_flight_destination_recertification": "CERTIFIED_ON_EVERY_WHOLE_COLLAR",
        "Gate3": "NOT_CERTIFIED_UNCHANGED",
        "strict_nonclaims": [
            "The collars do not certify an all-cell or all-depth common material radius.",
            "No uniform Piola remainder or global two-sided trace/current atlas is certified.",
            "No stopped MT_DQ estimate or global strong recipient is certified.",
            "The 176/176 conclusion is confined to the explicit finite Round69 s=0 root and enlarged collar registry.",
        ],
    }
    return {"schema": SCHEMA, "pins": actual, "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
