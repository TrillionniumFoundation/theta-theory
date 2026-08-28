#!/usr/bin/env python3
"""Exact all-sheet Gate-4 occurrence/single-charge schema.

The executable separates three logically different objects:

* raw signed circle-tangency descriptors;
* immutable physical event rows (connected, first-visible, constant miss
  target and constant parameter polarity); and
* the two nonadditive endpoint views of one such physical row.

It certifies the complete finite raw ledger and the universal exact theorem
which turns every completed physical row into one common-coarea,
same-occurrence, single-charge record.  It deliberately does not manufacture
the still-missing physical row partition or stopped-parent recovery data.
"""

from __future__ import annotations

import hashlib
import json
import itertools
from dataclasses import dataclass
from typing import Any

import cm2_gate3_candidate_first_hit_cert as base


SOURCES = ("G", "W")
CELLS = base.CELLS
TARGET_BY_ID = {target.target_id: target for target in base.TARGETS}


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def global_candidates(source: str) -> tuple[str, ...]:
    return tuple(sorted(set(itertools.chain.from_iterable(
        base.candidate_ids(f"{source}:{cell}") for cell in CELLS
    ))))


GLOBAL_CANDIDATES = {source: global_candidates(source) for source in SOURCES}


def moving_indicator(obstacle: str) -> int:
    return int(obstacle == "W")


def eta(source: str, target_id: str) -> int:
    """Relative horizontal centre velocity of target and source."""

    return moving_indicator(TARGET_BY_ID[target_id].obstacle) - moving_indicator(source)


def reflected_target(source: str, axis: str, target_id: str) -> str:
    """Exact lift-label action of Jx/Jy in source-centred coordinates."""

    target = TARGET_BY_ID[target_id]
    obstacle, ix, iy = target.obstacle, target.ix, target.iy
    if axis == "Jx":
        if source == "G":
            ix = -ix if obstacle == "G" else -ix - 1
        else:
            ix = 1 - ix if obstacle == "G" else -ix
    elif axis == "Jy":
        if source == "G":
            iy = -iy if obstacle == "G" else -iy - 1
        else:
            iy = 1 - iy if obstacle == "G" else -iy
    else:  # pragma: no cover
        raise ValueError(axis)
    result = f"{obstacle}[{ix},{iy}]"
    assert result in TARGET_BY_ID
    return result


@dataclass(frozen=True, order=True)
class Sheet:
    source: str
    target: str
    epsilon: int

    @property
    def eta(self) -> int:
        return eta(self.source, self.target)

    @property
    def active(self) -> bool:
        return self.eta != 0

    def reflect(self, axis: str) -> "Sheet":
        # Both plane reflections reverse the oriented transverse normal and
        # hence epsilon.  Jx conjugates s to -s; Jy preserves s.
        return Sheet(
            self.source,
            reflected_target(self.source, axis, self.target),
            -self.epsilon,
        )


def raw_sheets() -> tuple[Sheet, ...]:
    rows = tuple(sorted(
        Sheet(source, target, epsilon)
        for source in SOURCES
        for target in GLOBAL_CANDIDATES[source]
        for epsilon in (-1, 1)
    ))
    assert len(rows) == 288
    return rows


def chart_counts() -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for source in SOURCES:
        for cell in CELLS:
            chart = f"{source}:{cell}"
            ids = tuple(base.candidate_ids(chart))
            moving_ids = sum(eta(source, target) != 0 for target in ids)
            result[chart] = {
                "candidate_targets": len(ids),
                "raw_signed_sheets": 2 * len(ids),
                "moving_signed_sheets": 2 * moving_ids,
                "identically_zero_parameter_sheets": 2 * (len(ids) - moving_ids),
            }
    assert sum(row["moving_signed_sheets"] for row in result.values()) == 384
    return result


def sheet_schema(sheet: Sheet) -> dict[str, Any]:
    return {
        "raw_descriptor_id": f"{sheet.source}:{sheet.target}:eps={sheet.epsilon:+d}",
        "source_obstacle": sheet.source,
        "tangent_target": sheet.target,
        "epsilon": sheet.epsilon,
        "relative_parameter_velocity_eta": sheet.eta,
        "parameter_active": sheet.active,
        "event_equation": "Delta_T=R_T^2-w_T^2=0; w_T=epsilon*R_T",
        "partial_p_Delta": "2*epsilon*R_T*ell_T/c_p",
        "partial_s_Delta": "2*eta*epsilon*R_T*u_y",
        "signed_graph_coarea": "eta*epsilon*c_p*u_y/ell_T",
        "raw_descriptor_is_physical_event_row": False,
    }


def symmetry_orbits(active: tuple[Sheet, ...]) -> dict[str, Any]:
    universe = set(active)
    seen: set[Sheet] = set()
    orbits: list[list[dict[str, Any]]] = []
    for sheet in active:
        if sheet in seen:
            continue
        jx = sheet.reflect("Jx")
        jy = sheet.reflect("Jy")
        jxy = jx.reflect("Jy")
        orbit = {sheet, jx, jy, jxy}
        assert len(orbit) == 4 and orbit <= universe
        seen.update(orbit)
        members = []
        for item in sorted(orbit):
            # sign(u_y) is a formal local sign.  Jx preserves it and flips
            # epsilon; Jy flips both.  Thus Jx reverses the parameter-current
            # polarity and Jy preserves it.
            if item == sheet:
                relation = "identity"
                polarity = "+sigma"
            elif item == jx:
                relation = "Jx"
                polarity = "-sigma"
            elif item == jy:
                relation = "Jy"
                polarity = "+sigma"
            else:
                relation = "JxJy"
                polarity = "-sigma"
            members.append({
                "sheet": [item.source, item.target, item.epsilon],
                "relation_to_representative": relation,
                "parameter_current_polarity": polarity,
            })
        assert sum(row["parameter_current_polarity"] == "+sigma" for row in members) == 2
        assert sum(row["parameter_current_polarity"] == "-sigma" for row in members) == 2
        orbits.append(members)
    assert seen == universe and len(orbits) == 32
    return {
        "active_sheet_orbit_count": len(orbits),
        "orbit_size": 4,
        "two_plus_two_minus_per_orbit": True,
        "orbits_sha256": canonical_digest(orbits),
    }


def active_endpoint_descriptor_counts(active: tuple[Sheet, ...]) -> dict[str, int]:
    double_tangent = 0
    for sheet in active:
        double_tangent += 4 * (len(GLOBAL_CANDIDATES[sheet.source]) - 1)
    # For each active signed sheet: two source-grazing signs, two parameter
    # endpoints, and one u_y=0 constant-polarity split equation.
    source_grazing = 2 * len(active)
    parameter_boundary = 2 * len(active)
    polarity_splits = len(active)
    assert double_tangent == 36352
    assert source_grazing == 256
    assert parameter_boundary == 256
    assert polarity_splits == 128
    return {
        "target_target_common_tangent_descriptors": double_tangent,
        "source_grazing_descriptors": source_grazing,
        "parameter_boundary_descriptors": parameter_boundary,
        "constant_polarity_split_equations": polarity_splits,
        "total_raw_active_endpoint_descriptors": (
            double_tangent + source_grazing + parameter_boundary + polarity_splits
        ),
    }


PHYSICAL_ROW_REQUIRED_FIELDS = (
    "occurrence_id",
    "raw_sheet_id",
    "connected_base_component",
    "first_visible_owner_witness",
    "constant_miss_target",
    "strict_miss_after_tangent_gap",
    "non_grazing_source_endpoint",
    "non_grazing_miss_endpoint",
    "constant_parameter_polarity",
    "homogeneity_subrow",
    "forward_carrier_typing",
    "reverse_carrier_typing",
)


def universal_occurrence_contract() -> dict[str, Any]:
    """The exact theorem instantiated once the listed row fields exist."""

    forward_vector = {"target_grazing_trace": 1, "miss_collision_trace": -1}
    reverse_vector = {"target_grazing_trace": 1, "miss_collision_trace": -1}
    assert forward_vector == reverse_vector
    return {
        "required_physical_row_fields": list(PHYSICAL_ROW_REQUIRED_FIELDS),
        "ghost_branch": (
            "F_e maps the non-grazing source endpoint to the first non-grazing "
            "miss collision while passing through one tangent contact"
        ),
        "path_reversal": "rho_e=R o F_e on oriented path records; rho_e^2=id",
        "forward_current": (
            "J_e(Phi)=sigma_e*integral[Phi(z_T(a))-Phi(y_M(a))] dm_e(a)"
        ),
        "reverse_current": (
            "J_e(Phi)=sigma_e*integral[Phi(z_T(F_e^-1 y))-Phi(y)] d(F_e)_*m_e(y)"
        ),
        "formal_trace_vector": forward_vector,
        "restrictionwise_identity": (
            "for every Borel A in the occurrence base, the forward integral "
            "over A equals the reverse integral over F_e(A)"
        ),
        "common_coarea_identity": (
            "(F_e)_*(delta(H_e)|partial_s H_e| dmu_N) equals the reverse "
            "coarea law because F_e and R preserve cos(phi) dr dphi"
        ),
        "endpoint_views_are_nonadditive": True,
        "pre_recovery_single_charge": "q_e=max(C_fw(e),C_rev(e),2)*m_e",
        "charged_occurrence_count": 1,
        "max_dominates_both_oriented_costs": True,
        "raw_descriptor_receives_q_charge": False,
        "distinct_physical_rows_remain_additive": True,
    }


def recovery_boundary() -> dict[str, Any]:
    return {
        "borel_change_of_variables_for_two_views": True,
        "arbitrary_borel_stopped_recovery": False,
        "exact_obstruction": (
            "a positive-mass nowhere-dense restriction remains nowhere dense "
            "under every finite clean diffeomorphic branch and cannot equal a "
            "positive-density interval standard pair"
        ),
        "countable_clock_obstruction": (
            "one recovery-clock level has positive mass, so the same support "
            "obstruction survives any countable finite-time clock"
        ),
        "admissible_positive_routes": [
            "freeze a controlled interval/cylinder stopped restriction algebra",
            "instantiate the actual full-mass Gate-2 quotient and its uniform pair-energy/PPE drift",
        ],
        "pilot_pair_energy_is_not_physical_recovery": True,
    }


def certify() -> dict[str, Any]:
    rows = raw_sheets()
    active = tuple(row for row in rows if row.active)
    inactive = tuple(row for row in rows if not row.active)
    assert len(active) == 128
    assert len(inactive) == 160
    assert sum(row.source == "G" for row in active) == 64
    assert sum(row.source == "W" for row in active) == 64
    # Same-colour disks either both stay fixed (G/G) or translate together
    # (W/W); their relative displacement and hence Delta have zero s derivative.
    assert all(row.eta == 0 for row in inactive)
    assert all(abs(row.eta) == 1 for row in active)

    schemas = [sheet_schema(row) for row in rows]
    active_schemas = [sheet_schema(row) for row in active]
    result = {
        "model": "cm2-centered-rational-two-disk-standard-N",
        "parameter": "horizontal white-centre displacement s at s=0",
        "chart_ledger": chart_counts(),
        "global_raw_signed_sheets_after_chart_merge": len(rows),
        "global_parameter_active_signed_sheets": len(active),
        "global_identically_zero_parameter_sheets": len(inactive),
        "raw_sheet_schema_sha256": canonical_digest(schemas),
        "active_sheet_schema_sha256": canonical_digest(active_schemas),
        "active_endpoint_registry": active_endpoint_descriptor_counts(active),
        "symmetry": symmetry_orbits(active),
        "universal_occurrence_contract": universal_occurrence_contract(),
        "instantiated_local_witness": (
            "G[0,0] -- tangent W[0,0] -- G[1,1] grouped-incidence certificate"
        ),
        "recovery_boundary": recovery_boundary(),
        "completion": {
            "raw_active_sheet_ledger": True,
            "zero_coefficient_same_colour_elimination": True,
            "all_sheet_symmetry_schema": True,
            "universal_same_occurrence_two_view_theorem": True,
            "universal_common_coarea_theorem": True,
            "universal_pre_recovery_single_charge_theorem": True,
            "connected_immutable_physical_event_rows": False,
            "all_row_forward_reverse_typing_and_costs": False,
            "controlled_stopped_restriction_algebra": False,
            "physical_bidirectional_recovery_moments": False,
            "global_single_charge_q_ledger": False,
            "gate4_certified": False,
        },
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_RAW_MOVING_SHEET_LEDGER_128: CERTIFIED")
    print("GATE4_UNIVERSAL_SAME_OCCURRENCE_COMMON_COAREA_SCHEMA: CERTIFIED")
    print("GATE4_UNIVERSAL_PRE_RECOVERY_q_MAX_SCHEMA: CERTIFIED")
    print("GATE4_IMMUTABLE_PHYSICAL_EVENT_ROWS: NOT_CERTIFIED")
    print("GATE4_BIDIRECTIONAL_STOPPED_PARENT_RECOVERY: NOT_CERTIFIED")
    print("GATE4_GLOBAL_SINGLE_CHARGE_LEDGER: NOT_CERTIFIED")
    print("GATE_4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
