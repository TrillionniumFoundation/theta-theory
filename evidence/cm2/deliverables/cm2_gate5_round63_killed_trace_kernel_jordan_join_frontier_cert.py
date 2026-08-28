#!/usr/bin/env python3
"""Round-63 Gate-5 killed trace-kernel/Jordan frontier certificate.

This leaf proves a positive time-labelled kernel/Lyapunov interface and an
actual fixed-insertion orientation-cost Jordan join.  It deliberately does
not claim an actual insertion-time drift, the Round-54 signed-flux Jordan
law, universal suffix truth, strong cemetery, a new Gate-5 field, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round63-killed-trace-kernel-jordan-join-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round63-killed-trace-kernel-jordan-join-frontier-manifest-2026-07-21.json"

DEPENDENCIES = {
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json": "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json": "ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9",
}

ROUND62_PINS = {
    "cm2-sixty-second-direct-assault-2026-07-21.md": "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256": "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-assault-2026-07-21.md": "cd90cc734264c34d518365f219dce3fbe058232d91213002cc8dd9d04b766f46",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256": "ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61",
    "cm2-round62-independent-core-frontier-audit-2026-07-21.md": "123f8ffc563e7d2b364f7caf565ac1a953ecc45123d1c483bc0f97b24c3cfeb4",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json": "19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.sha256": "32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414",
}

BLOCK_DEPTH = 9148
FORWARD_F10 = Q(395304765824751, 220000)
REVERSE_F10 = Q(162772550633721, 176000)
BIDIRECTIONAL_F10 = Q(2395081816467609, 880000)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def constants() -> dict[str, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        return {"rho": +rho, "w_Z": +w, "threshold": +(Decimal(1) / w)}


def _safe(name: str, expected: str) -> Path:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe pin: {name}")
    if sha(path) != expected:
        raise RuntimeError(f"hash mismatch: {name}")
    return path


def load_json_pin(name: str, expected: str) -> dict[str, Any]:
    path = _safe(name, expected)
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"non-object pin: {name}")
    return value


def validate_dependencies() -> None:
    loaded = {name: load_json_pin(name, expected) for name, expected in DEPENDENCIES.items()}
    for name, expected in ROUND62_PINS.items():
        if name.endswith(".json"):
            load_json_pin(name, expected)
        else:
            _safe(name, expected)

    r39 = loaded["cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"]["result"]
    if "4^(-b)" not in r39["physical_rank_L3over2_derivation"]["rank_tail"]:
        raise RuntimeError("Round39 tail")
    r50 = loaded["cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if "time-j" not in r50["candidate_representation_token"]:
        raise RuntimeError("Round50 time token")
    r52 = loaded["cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["sums_over_insertion_times"] is not False or r52["transferred_bidirectional_F10_L1_strict_upper"] != str(BIDIRECTIONAL_F10):
        raise RuntimeError("Round52 fixed-j")
    r54 = loaded["cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"]["result"]["recordwise_owner_collar_E_Tr"]
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 coverage")
    r61 = loaded["cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json"]["result"]
    if r61["strict_nonpromotion"]["Gate5_maturity"] != "10/18" or r61["seven_bit_common_Borel_code_materialisation"]["unconditional_Borel_predicate_count"] != 7:
        raise RuntimeError("Round61 baseline")
    r62 = loaded["cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json"]["result"]
    if r62["strict_nonpromotion"]["Gate5_maturity"] != "10/18" or r62["all_time_owner_registry"]["cross_j_deduplication"] != "CERTIFIED_ILLEGAL_FOR_THE_FROZEN_OPERATOR_IDENTITY":
        raise RuntimeError("Round62 baseline")


def killed_kernel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    w = Q(3, 2)
    for label, kappa, n in (
        ("subcritical", Q(1, 2), 12),
        ("critical", Q(2, 3), 12),
        ("supercritical", Q(3, 4), 12),
    ):
        ratio = w * kappa
        partial = sum((ratio**j for j in range(n + 1)), Q(0))
        rows.append(
            {
                "label": label,
                "w_test": str(w),
                "kappa_test": str(kappa),
                "ratio": str(ratio),
                "N": n,
                "partial_sum": str(partial),
                "finite_geometric_criterion": ratio < 1,
            }
        )
    return rows


def killed_trace_kernel_frontier() -> dict[str, Any]:
    c = constants()
    rows = killed_kernel_rows()
    return {
        "time_labelled_carrier": "E_all=disjoint_union_(j>=0)({j}xE_j); each K_j maps only slice j to j+1, preserves the frozen non-time owner lineage labels, and never quotients distinct insertion times",
        "positive_law": "Lambda_j is a finite positive debt law on E_j and Lambda_(j+1)<=Lambda_j K_j as measures",
        "substochastic_kernel": "K_j:E_j->SubProb(E_(j+1))",
        "Lyapunov_drift": "V_j>=1, K_j V_(j+1)<=kappa V_j, Lambda_0(V_0)<infinity",
        "weighted_conclusion": "if w_Z*kappa<1 then sum_j w_Z^j Lambda_j(1)<=Lambda_0(V_0)/(1-w_Z*kappa)<infinity",
        "proof": "positivity gives Lambda_j(V_j)<=kappa^j Lambda_0(V_0), V_j>=1 controls mass, and Tonelli sums the geometric majorant",
        "debt_sectors": ["complement_F10", "clock_rawZ_powerOrlicz", "orientation_cost_variation", "orientation_cost_common_mode", "pre_regularization_cemetery"],
        "sharp_one_point_model": "on one point, K retains mass kappa and V=1, so Lambda_j(1)=kappa^j and the weighted series is finite iff w_Z*kappa<1",
        "stationary_obstruction": "if a nonzero shift-covariant or identity-kernel positive charge is preserved, Lambda_j(1)=c>0 and sum_j w_Z^j c diverges because w_Z>1",
        "Round52_guard": "collision survivor rho^j does not imply trace drift: the pinned collision-null face tower retains trace charge one, corresponding to kappa=1 on the face",
        "actual_K_j": "NOT_CERTIFIED",
        "actual_V_j": "NOT_CERTIFIED",
        "actual_kappa_below_threshold": "NOT_CERTIFIED",
        "w_Z_decimal": str(c["w_Z"]),
        "kappa_threshold_decimal": str(c["threshold"]),
        "replay_rows": rows,
        "replay_rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_CONDITIONAL_SHARP_INTERFACE_NO_ACTUAL_DRIFT",
    }


def fixed_j_orientation_cost_jordan() -> dict[str, Any]:
    if FORWARD_F10 + REVERSE_F10 != BIDIRECTIONAL_F10:
        raise RuntimeError("F10 sum")
    return {
        "actual_same_owner_law": "xi_j^f=C_bad,j^f nu_j and xi_j^r=C_bad,j^r nu_j on the same actual fixed-j owner/root law",
        "forward_strict_upper": str(FORWARD_F10),
        "reverse_strict_upper": str(REVERSE_F10),
        "bidirectional_strict_upper": str(BIDIRECTIONAL_F10),
        "exact_sum_check": FORWARD_F10 + REVERSE_F10 == BIDIRECTIONAL_F10,
        "cost_signed_measure": "J_j^cost=xi_j^f-xi_j^r",
        "cost_common_mode": "lambda_j^cost=xi_j^f wedge xi_j^r",
        "lattice_identity": "xi_j^f+xi_j^r=|J_j^cost|+2 lambda_j^cost",
        "variation_strict_upper": str(BIDIRECTIONAL_F10),
        "common_mode_strict_upper": str(min(FORWARD_F10, REVERSE_F10)),
        "complement_restriction": "restriction to A_col^c preserves the lattice identity and fixed-j finiteness of variation, common mode and total positive orientation cost",
        "cemetery_pushforward_guard": "the labelled positive cemetery pushforward preserves total positive charge; separate Jordan parts are not asserted preserved under a noninjective pushforward",
        "type_guard": "J_j^cost is the Jordan law of Round61 orientation-positive F10 cost measures; it is not identified with the Round54 actual signed-flux hit/miss J_p or its charge",
        "fixed_j_orientation_cost_Jordan_join": "CERTIFIED",
        "fixed_j_variation_common_complement_finite": "CERTIFIED",
        "Round54_physical_signed_flux_alignment": "NOT_CERTIFIED",
        "all_time_weighted_cost_variation": "NOT_CERTIFIED",
        "all_time_weighted_cost_common_mode": "NOT_CERTIFIED",
        "all_time_weighted_complement": "NOT_CERTIFIED",
        "status": "CERTIFIED_ACTUAL_FIXED_J_ORIENTATION_COST_JORDAN_ONLY",
    }


def complement_strata_frontier() -> dict[str, Any]:
    rows = [
        {
            "stratum": "source_endpoint_exact_grazing",
            "mass": "CERTIFIED_ZERO_FIXED_J_ROUND62",
            "orientation_F10_cost": "CERTIFIED_ZERO_FIXED_J",
            "proof": "xi_j^f,xi_j^r<<nu_j and nu_j(G_src,j)=0",
        },
        {
            "stratum": "remaining_exact_cut_union_N_cut_rem",
            "mass": "NOT_CERTIFIED_ZERO",
            "orientation_F10_cost": "NOT_CERTIFIED_ZERO",
            "proof": "for a countable enumeration C_(j,m), positivity gives chi_j(N_cut_rem)=0 iff every chi_j(C_(j,m))=0; the required same-law zero-set rows are absent",
        },
        {
            "stratum": "positive_individual_gaps_with_zero_infimum_N_acc",
            "mass": "NOT_CERTIFIED_ZERO",
            "orientation_F10_cost": "NOT_CERTIFIED_ZERO",
            "proof": "A_(j,k)={all registered gaps positive and inf_m d_(j,m)<=2^(-k)} decreases to N_acc, hence chi_j(N_acc)=lim_k chi_j(A_(j,k)); no full-word small-gap tail is pinned",
        },
        {
            "stratum": "pre_regularization_corner_or_simultaneous_cemetery",
            "mass": "NOT_CERTIFIED_FINITE_OR_ZERO",
            "orientation_F10_cost": "NOT_CERTIFIED_FINITE",
            "proof": "absence inside the regular owner domain is a domain statement and does not bound the removed pre-regularization law",
        },
    ]
    return {
        "positive_cost_law": "chi_j=1_(A_col^c)(xi_j^f+xi_j^r)",
        "exact_cut_criterion": "chi_j(N_cut_rem)=0 iff chi_j(C_(j,m))=0 for every member of a countable exact-cut enumeration",
        "accumulation_criterion": "chi_j(N_acc)=lim_(k->infinity)chi_j(A_(j,k)) for the decreasing small-gap sets A_(j,k)",
        "sufficient_small_gap_row": "chi_j(A_(j,k))<=C_j*tau^k with tau<1 proves fixed-j N_acc cost nullity; drift-compatible C_j would also pay the all-time sum",
        "source_rank_guard": "the frozen B/eta tail controls only source endpoint grazing and cannot be renamed as a later/full-word d_other tail",
        "rows": rows,
        "rows_sha256": digest(rows),
        "global_A_col_coverage": "NOT_CERTIFIED",
        "remaining_complement_all_time_charge": "NOT_CERTIFIED",
        "strong_pre_regularization_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_SOURCE_GRAZING_ZERO_COST_AND_EXACT_REMAINING_INTERFACES",
    }


def suffix_clearance_frontier() -> dict[str, Any]:
    return {
        "Borel_suffix_predicates": "CERTIFIED_7_OF_7_PINNED_ROUND61",
        "universal_values": "2_TRUE_5_OPEN",
        "five_open_bits": ["L_input", "L_C24", "L_operator", "L_output", "L_horizon"],
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "first_failure_cells": "F_b={J_0=...=J_(b-1)=1,J_b=0} are Borel and {R<r_K}=disjoint_union_b(F_b intersect {b<r_K})",
        "drift_scope_guard": "a positive killed-kernel drift can pay failure charge but does not prove universal pointwise truth or make first-failure cells empty",
        "outer_active_Abel": "CERTIFIED_EXTENDED_IDENTITY_PINNED_ROUND62_FINITE_RHS_NOT_CERTIFIED",
        "outer_rawZ_power_Orlicz": "CERTIFIED_EXACT_IFF_PINNED_ROUND62_FINITE_RHS_NOT_CERTIFIED",
        "actual_all_time_positive_debt_kernel": "NOT_CERTIFIED",
        "status": "NO_NEW_SUFFIX_VALUE_OR_CLEARANCE_FINITE_RHS",
    }


def technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-21",
        "official_sources_checked": ["arXiv:2604.19671v2", "arXiv:2412.04615v3", "arXiv:2606.19621v2", "official arXiv API latest-query results through 2026-07-21"],
        "small_hole_guard": "2604.19671v2 starts from already-standard families and survival normalization; it does not construct the singular owner/coarea trace lineage or its Lyapunov drift",
        "renewal_guard": "2412.04615v3 studies operator-renewal escape/hitting asymptotics with applications stated for one-dimensional nonuniformly expanding systems; it does not identify the CM2 trace law",
        "signed_transport_guard": "2606.19621v2 does not pay positive common mode, complement, or all-time cemetery",
        "latest_finding": "no checked source supplies a same-owner insertion-time substochastic trace kernel with w_Z-contracting Lyapunov drift, the five suffix values, or positive all-time cemetery decay",
        "external_dependency_imported": False,
        "status": "CHECKED_NO_DIRECT_GATE5_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "Gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "new_global_field_completed": None,
        "actual_same_owner_all_time_recurrence": "NOT_CERTIFIED",
        "actual_killed_trace_kernel_Lyapunov_drift": "NOT_CERTIFIED",
        "conditional_killed_trace_kernel_theorem": "CERTIFIED_EXACT_SHARP",
        "cross_time_deduplication": "CERTIFIED_ILLEGAL_PINNED_ROUND62",
        "source_grazing_orientation_cost_zero_fixed_j": "CERTIFIED",
        "remaining_N_cut_N_acc_paid": "NOT_CERTIFIED",
        "pre_regularization_cemetery": "NOT_CERTIFIED",
        "fixed_j_orientation_cost_Jordan_join": "CERTIFIED",
        "Round54_physical_signed_flux_Jordan_alignment": "NOT_CERTIFIED",
        "all_time_weighted_variation_common_complement": "NOT_CERTIFIED",
        "physical_active_Abel_rawZ_Orlicz_finite": "NOT_CERTIFIED",
        "all_seven_suffix_predicates_Borel": "CERTIFIED_7_OF_7",
        "physical_all_seven_suffix_bits_true": "NOT_CERTIFIED_2_TRUE_5_OPEN",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "complete_positive_F10": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
    }


def maturity_update() -> dict[str, Any]:
    return {
        "previous_global_maturity": "10/18",
        "new_global_field_completed": None,
        "newly_certified_sublayers": [
            "time-labelled positive substochastic trace-kernel/Lyapunov theorem with sharp threshold and stationarity obstruction",
            "actual fixed-j same-owner orientation-cost Jordan join and finite variation/common/complement",
            "source exact-grazing zero F10 charge plus exact N_cut/N_acc small-gap interfaces",
        ],
        "reason_no_new_field_credit": "no actual insertion-time drift, remaining complement/cemetery payment, five suffix values, physical signed-flux Jordan alignment or finite Abel/raw-Z/Orlicz RHS is certified",
        "current_global_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
    }


def build_result() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "Round62_artifact_sha256": dict(ROUND62_PINS),
            "old_artifacts_modified": False,
            "parameter_scope": "base s=0 actual fixed-j owner laws; all-time kernel theorem is exact conditional and separators are logical positive models, not a new billiard realization",
            "claim_type": "killed trace-kernel drift interface, actual fixed-j orientation-cost Jordan join, and complement zero/small-gap frontier",
        },
        "killed_trace_kernel_frontier": killed_trace_kernel_frontier(),
        "fixed_j_orientation_cost_Jordan": fixed_j_orientation_cost_jordan(),
        "complement_strata_frontier": complement_strata_frontier(),
        "suffix_clearance_frontier": suffix_clearance_frontier(),
        "latest_technology_audit": technology_audit(),
        "Gate5_maturity_update": maturity_update(),
        "strict_nonpromotion": strict_nonpromotion(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(DEPENDENCIES),
        "Round62_artifact_sha256": dict(ROUND62_PINS),
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(verifier: Path) -> bytes:
    return (json.dumps(build_manifest(verifier), sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round63_killed_trace_kernel_jordan_join_frontier_verifier.py")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    validate_dependencies()
    data = render_manifest(args.verifier)
    if args.output:
        args.output.write_bytes(data)
        print(f"WROTE: {args.output}")
        return 0
    print(data.decode(), end="")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
