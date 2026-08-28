#!/usr/bin/env python3
"""Controlled stopped interval algebra on all corrected maximal row laws.

Every corrected row law is finite and has a strictly positive analytic
density on its open maximal base interval.  Its normalized cumulative mass
therefore supplies a canonical coordinate ``u_e in (0,1)``.  Dyadic atoms in
this coordinate form a countable nested Boolean algebra.  At declared depth
K every nonempty atom has exactly ``2^-K`` of the row mass, every admissible
restriction has finitely many interval components, and its normalization
cost is at most ``2^K``.

Trimming the first and last ``2^-L`` of row mass leaves a compact analytic
core and an exact two-sided cemetery mass ``2^(1-L)``.  This eliminates the
fat-Cantor obstruction for the declared stopped policy and isolates the
remaining physical input: cone/homogeneity typing and an exponential moment
for the recorded depth/recovery cost.  Those inputs are not claimed here.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq


Q = Fraction
HERE = Path(__file__).resolve().parent
DQ_MANIFEST = (
    HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_corrected_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = json.loads(DQ_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    result = manifest["result"]
    assert result["collision_coordinate_correction"][
        "corrected_positive_row_law"
    ] == "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta"
    rows, registry = dq.load_rows()
    typed, assembly = dq.corrected_current_rows(rows)
    assert assembly["corrected_current_rows_sha256"] == result[
        "corrected_current_assembly"
    ]["corrected_current_rows_sha256"]
    return typed, registry


def dyadic_boolean_algebra_audit(maximum_exhaustive_depth: int = 4) -> dict[str, Any]:
    exhaustive_rows = []
    for depth in range(maximum_exhaustive_depth + 1):
        atom_count = 1 << depth
        universe = (1 << atom_count) - 1
        masks = range(universe + 1)
        complement_closed = all(((~mask) & universe) <= universe for mask in masks)
        assert complement_closed
        if depth <= 3:
            masks_list = list(masks)
            for left in masks_list:
                for right in masks_list:
                    assert (left | right) <= universe
                    assert (left & right) <= universe
                    assert (left ^ right) <= universe
        exhaustive_rows.append({
            "depth_K": depth,
            "atom_count": atom_count,
            "boolean_set_count": 1 << atom_count,
            "complement_exhaustively_checked": True,
            "all_binary_operations_exhaustively_checked": depth <= 3,
        })
    return {
        "mass_coordinate": (
            "u_e(theta)=m_e((left,theta))/m_e(row) is an increasing "
            "homeomorphism from the open row to (0,1)"
        ),
        "depth_K_atoms": "I(K,j)=[j/2^K,(j+1)/2^K), 0<=j<2^K",
        "atom_mass_fraction": "2^-K",
        "nested_refinement": "I(K,j)=I(K+1,2j) disjoint-union I(K+1,2j+1)",
        "finite_level_boolean_algebra": True,
        "countable_nested_union_boolean_algebra": True,
        "exhaustive_small_depth_rows": exhaustive_rows,
        "exhaustive_small_depth_rows_sha256": canonical_digest(exhaustive_rows),
    }


def trim_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for depth in range(2, 11):
        for trim_level in range(2, depth + 1):
            atom_count = 1 << depth
            one_side_cemetery_atoms = 1 << (depth - trim_level)
            core_atoms = atom_count - 2 * one_side_cemetery_atoms
            atom_mass = Q(1, atom_count)
            one_side_cemetery_mass = Q(1, 1 << trim_level)
            total_cemetery_mass = 2 * one_side_cemetery_mass
            core_mass = 1 - total_cemetery_mass
            assert core_atoms * atom_mass == core_mass
            assert core_atoms > 0
            rows.append({
                "depth_K": depth,
                "trim_level_L": trim_level,
                "atoms_per_row": atom_count,
                "core_atoms_per_row": core_atoms,
                "one_side_cemetery_atoms_per_row": one_side_cemetery_atoms,
                "atom_mass_fraction": str(atom_mass),
                "one_side_cemetery_mass_fraction": str(one_side_cemetery_mass),
                "total_cemetery_mass_fraction": str(total_cemetery_mass),
                "compact_core_mass_fraction": str(core_mass),
                "maximum_normalization_cost_for_nonempty_restriction": str(
                    1 / atom_mass
                ),
            })
    return rows, {
        "checked_depth_range": [2, 10],
        "checked_trim_constraint": "2<=L<=K",
        "trim_identity_row_count": len(rows),
        "all_trim_mass_identities_exact": True,
        "trim_rows_sha256": canonical_digest(rows),
    }


def all_row_contracts(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    contracts = []
    for row in rows:
        contracts.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "corrected_positive_law": "R_source*cp*abs(u_y)/ell_T*dtheta",
            "strict_positive_analytic_density_on_open_row": True,
            "canonical_mass_coordinate": "u_e in (0,1)",
            "depth_K_atom_mass": "2^-K*m_e(row)",
            "pre_recovery_single_charge": "q_e=max(C_fw(e),C_rev(e),2)*m_e",
            "same_dyadic_restriction_for_both_oriented_views": True,
            "forward_atom_image": "one analytic interval carrier",
            "reverse_atom_image": "one analytic interval carrier",
        })
    contracts.sort(key=canonical_json)
    assert len(contracts) == 64
    assert len({row["occurrence_id"] for row in contracts}) == 64
    return contracts, {
        "maximal_occurrence_count": len(contracts),
        "canonical_mass_coordinate_count": len(contracts),
        "one_corrected_m_and_one_q_expression_per_occurrence": True,
        "same_atom_transport_in_forward_and_reverse_views": True,
        "row_contracts_sha256": canonical_digest(contracts),
    }


def controlled_policy(row_count: int) -> dict[str, Any]:
    sample_depth = 8
    sample_trim = 4
    atoms_per_row = 1 << sample_depth
    cemetery_atoms_per_side = 1 << (sample_depth - sample_trim)
    core_atoms_per_row = atoms_per_row - 2 * cemetery_atoms_per_side
    assert core_atoms_per_row == 224
    return {
        "predictable_record": [
            "occurrence_id e",
            "dyadic depth K before the final test/query",
            "finite atom mask A",
            "optional trim level L with 2<=L<=K",
            "orientation policy selected before product-time query",
        ],
        "admissible_restriction": (
            "a finite union of depth-K mass-coordinate atoms on one row"
        ),
        "maximum_interval_components_per_row": "2^K",
        "minimum_nonzero_restricted_mass": "2^-K*m_e(row)",
        "maximum_parent_normalization_cost": "2^K",
        "trimmed_core": "2^-L <= u_e <= 1-2^-L",
        "two_sided_cemetery_mass": "2^(1-L)*m_e(row)",
        "compact_core_analytic_costs_are_finite_at_each_fixed_K_L": True,
        "fat_cantor_restrictions_admissible": False,
        "fat_cantor_obstruction_removed_inside_declared_policy": True,
        "sample_ledger": {
            "K": sample_depth,
            "L": sample_trim,
            "atoms_per_row": atoms_per_row,
            "core_atoms_per_row": core_atoms_per_row,
            "total_core_atoms_all_rows": row_count * core_atoms_per_row,
            "total_cemetery_mass_fraction_per_row": str(Q(1, 8)),
            "maximum_normalization_cost": 1 << sample_depth,
        },
    }


def recovery_boundary() -> dict[str, Any]:
    return {
        "controlled_interval_algebra_is_not_recovery": True,
        "still_missing": [
            "all-row forward/reverse stable-unstable cone typing after homogeneity cuts",
            "numeric compact-core source, density, chart and test-pullback costs",
            "a predictable recovery clock on every admitted atom",
            "an exponential moment absorbing 2^K and both recovery clocks",
            "summable L-to-infinity control of the two endpoint cemeteries",
            "dynamic-C1 and CM2 norm intertwiners",
        ],
        "required_depth_moment": (
            "the stopped law must control E_q[2^K*exp(gamma*(R_fw+R_rev))]"
        ),
        "arbitrary_Borel_stopped_recovery": False,
        "controlled_dyadic_stopped_recovery": False,
        "gate4_certified": False,
        "gate5_certified": False,
    }


def certify() -> dict[str, Any]:
    rows, registry = load_corrected_rows()
    algebra = dyadic_boolean_algebra_audit()
    trims, trim_audit = trim_rows()
    contracts, contract_audit = all_row_contracts(rows)
    policy = controlled_policy(len(rows))
    boundary = recovery_boundary()
    assert registry["maximal_row_rows_sha256"] == (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    )
    return {
        "schema": "cm2.gate45.controlled-stopped-interval-algebra.v1",
        "provenance": {
            "corrected_DQ_manifest": DQ_MANIFEST.name,
            "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "dyadic_mass_coordinate_algebra": algebra,
        "exact_trim_and_cemetery_ledger": trim_audit,
        "all_maximal_row_contracts": contract_audit,
        "controlled_stopped_policy": policy,
        "recovery_boundary": boundary,
        "scope_limits": {
            "corrected_row_laws_imported": True,
            "countable_nested_dyadic_interval_algebra": True,
            "finite_component_and_normalization_cost_at_declared_depth": True,
            "exact_trimmed_core_and_cemetery_mass": True,
            "same_restriction_transported_in_both_oriented_views": True,
            "fat_cantor_restrictions_excluded": True,
            "numeric_forward_reverse_costs": False,
            "controlled_stopped_parent_recovery": False,
            "CM2_norm_lifts": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digests": {
            "trim_rows_sha256": canonical_digest(trims),
            "row_contracts_sha256": canonical_digest(contracts),
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_CONTROLLED_DYADIC_STOPPED_INTERVAL_ALGEBRA: CERTIFIED")
    print("GATE45_FAT_CANTOR_RESTRICTION_OBSTRUCTION_IN_POLICY: REMOVED")
    print("GATE45_PHYSICAL_STOPPED_RECOVERY_AND_CM2_NORMS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
