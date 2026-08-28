#!/usr/bin/env python3
"""Finite two-rank face-cost domination by the actual tagged branch RN law."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
R1 = HERE / "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
R1_F9 = HERE / "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
R2 = HERE / "cm2-round76-r2-numeric-fields-2026-07-21.json"
RN = HERE / "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build() -> dict[str, Any]:
    r1 = load(R1)["result"]
    r1_f9 = load(R1_F9)["result"]
    r2 = load(R2)["result"]
    rn = load(RN)["result"]
    if rn["actual_branch_RN_covariance"]["status"] != (
        "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE"
    ):
        raise RuntimeError("RN source status changed")
    if len(r1["rows"]) != 32 or len(r2["rows"]) != 32:
        raise RuntimeError("face registry changed")

    r1_f9_fields = r1_f9["actual_local_field_attachment"]
    r1_f9_sum = Q(r1_f9_fields["F9_32_face_finite_sum_upper"])
    r2_f9_sum = Q(r2["F9_32_face_integer_sum"])
    r1_f10_sum = Q(r1["F10_integer_sum"])
    r2_f10_sum = Q(r2["F10_32_face_integer_sum"])
    r1_f13_sum = Q(r1["F13_32_face_current_variation_strict_upper"])
    r2_f13_sum = Q(r2["F13_32_face_current_variation_strict_upper"])
    r1_f16_sum = Q(r1["F16_32_face_flux_cost_strict_upper"])
    r2_f16_sum = Q(r2["F16_32_face_Piola_flux_cost_strict_upper"])

    face_rows = []
    for row in r1["rows"]:
        face_rows.append({
            "rank": 1,
            "face_id": row["component_id"],
            "source_core_index": row["source_core_index"],
            "RN_charge": "kappa_B(U_f)=integral_U_f g_B dmu_U",
            "RN_charge_bounds": ["0", "mu_U(U_f)"],
            "unit_reference_mass_upper": "1",
            "F9_upper": r1_f9_fields["F9_per_face_unit_speed_C2_upper"],
            "F10_upper": row["F10_integer_upper"],
            "F13_strict_upper": row["F13_current_variation_strict_upper"],
            "F16_strict_upper": row["F16_Piola_flux_cost_strict_upper"],
        })
    for row in r2["rows"]:
        face_rows.append({
            "rank": 2,
            "face_id": row["curve_id"],
            "source_core_index": row["source_core_index"],
            "RN_charge": "kappa_B(U_f)=integral_U_f g_B dmu_U",
            "RN_charge_bounds": ["0", "mu_U(U_f)"],
            "unit_reference_mass_upper": "1",
            "F9_upper": row["F9_unit_speed_C2_integer_upper"],
            "F10_upper": row["F10_density_C1_integer_upper"],
            "F13_strict_upper": row["F13_full_face_current_variation_strict_upper"],
            "F16_strict_upper": row["F16_full_face_Piola_flux_cost_strict_upper"],
        })
    combined = {
        "F9_actual_RN_weighted_upper": str(r1_f9_sum + r2_f9_sum),
        "F10_actual_RN_weighted_upper": str(r1_f10_sum + r2_f10_sum),
        "F13_actual_RN_weighted_strict_upper": str(r1_f13_sum + r2_f13_sum),
        "F16_actual_RN_weighted_strict_upper": str(r1_f16_sum + r2_f16_sum),
    }
    return {
        "schema": "cm2.round77.rn-weighted-finite-face-sum.v1",
        "pins": {path.name: sha256_path(path) for path in (R1, R1_F9, R2, RN)},
        "result": {
            "face_count": len(face_rows),
            "rank_histogram": {"1": 32, "2": 32},
            "actual_RN_law": "0<=g_B=d kappa_B/d mu_U<=1 on every immutable tagged branch",
            "incidence_weighting": "each physical face inherits the charge of its adjacent immutable tagged first-return path cell; no face/interior point equality is asserted",
            "jacobian_guard": "the coordinate Jacobian cancels in the marked/unmarked RN ratio; no extra Jacobian factor is inserted",
            "face_rows": face_rows,
            "finite_two_rank_actual_RN_dominated_sum": combined,
            "exact_numeric_RN_weights": "NOT_CERTIFIED__DENSITY_VALUES_NOT_MATERIALIZED_ON_THE_64_FACE_INCIDENCES",
            "official_limiting_path_law_sum": "NOT_CERTIFIED__RANKS_GE_3_AND_UNIFORM_SUMMABILITY_MISSING",
            "gate5_promotion": "NO",
        },
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
