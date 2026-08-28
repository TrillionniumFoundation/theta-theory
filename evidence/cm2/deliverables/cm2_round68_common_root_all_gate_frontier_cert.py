#!/usr/bin/env python3
"""Producer for the Round-68 common-root and all-gate frontier certificate."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import canonical_bytes, digest, require, sha256_path, validate_pins


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round68.common-root-all-gate-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round68-common-root-all-gate-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round68_common_root_all_gate_frontier_verifier.py"
COMMON = HERE / "cm2_round68_common.py"

PINS = {
    "cm2-sixty-seventh-direct-assault-2026-07-21.md":
        "fd47134878ae5fbc239ac2a648dd8dd074181162da88d4ba011fea9d98503b82",
    "cm2-sixty-seventh-direct-assault-manifest-2026-07-21.sha256":
        "a0f335e434caa65b1d9a99f9daf92dbb180f407cee1724e83aaabbe34fce27eb",
    "cm2-round67-independent-core-frontier-audit-manifest-2026-07-21.json":
        "95a08ffbb4ead8a56b43de95fb73756db9635adb7ca99a3bea65190a15c97d48",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_result() -> dict[str, Any]:
    join_fields = [
        "restriction_id", "return_component", "insertion_time", "collision_index",
        "event_signature", "primitive_key", "owner_key", "rank_zero_component",
        "plaque_side", "word_cell", "endpoint_coordinate", "root_coordinate",
    ]
    join_atoms = [
        {"atom": index, "left_key": index, "right_key": index ^ 1,
         "mass": "1/4", "diagonal": False}
        for index in range(4)
    ]
    hazard_rows = []
    square_survival = Q(1)
    harmonic_survival = Q(1)
    for n in range(1, 17):
        square_hazard = Q(1, (n + 1) ** 2)
        harmonic_hazard = Q(1, n + 1)
        square_survival *= 1 - square_hazard
        harmonic_survival *= 1 - harmonic_hazard
        hazard_rows.append({
            "n": n,
            "square_hazard": qstr(square_hazard),
            "square_survival": qstr(square_survival),
            "square_closed_form": qstr(Q(n + 2, 2 * (n + 1))),
            "harmonic_hazard": qstr(harmonic_hazard),
            "harmonic_survival": qstr(harmonic_survival),
            "harmonic_closed_form": qstr(Q(1, n + 1)),
        })
    perturbation_rows = []
    for n in range(1, 13):
        delta_a = Q(1, 2**n)
        delta_b = Q(1, 3**n)
        bound = 2 * delta_a + 3 * delta_b + delta_a * delta_b
        perturbation_rows.append({
            "n": n, "norm_A": "3", "norm_B": "2",
            "delta_A": qstr(delta_a), "delta_B": qstr(delta_b),
            "product_error_bound": qstr(bound),
        })
    gate5_sectors = [
        "active_clock", "raw_Z", "Orlicz", "complement", "variation",
        "oriented_common_mode", "one_shot_cemetery",
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_round67_chain": PINS,
        },
        "common_root_join": {
            "status": "EXACT_JOIN_CRITERION_CERTIFIED__ACTUAL_CROSSWALK_ABSENT",
            "criterion": "TWO_DETERMINISTIC_BOREL_VIEWS_OF_ONE_HALF_OPEN_PATH_NAMESPACE_WITH_RECORDWISE_COMPOSITE_KEY_EQUALITY",
            "required_fields": join_fields,
            "actual_joined_fields": "0/12",
            "equal_marginals_sufficient": False,
            "abstract_measure_isomorphism_sufficient": False,
            "forgetful_key_equality_sufficient": False,
            "four_atom_separator": {
                "left_key_multiset": [0, 1, 2, 3],
                "right_key_multiset": [0, 1, 2, 3],
                "atoms": join_atoms,
                "diagonal_graph_mass": "0",
                "conclusion": "EQUAL_KEY_MARGINALS_WITH_ZERO_RECORDWISE_JOIN",
            },
        },
        "gate13_uniform_frontier": {
            "status": "QUANTITATIVE_SUFFICIENT_CONTRACT_CERTIFIED__ACTUAL_ESTIMATES_ABSENT",
            "transport_identity": "A_c(x)=C(sigma x)^-1 A_q(x) C(x)",
            "product_perturbation_bound": "dA*B+A*dB+dA*dB",
            "perturbation_rows": perturbation_rows,
            "finite_selection_separator": {
                "construction": "depth_n_has_one_unobserved_cell_with_unit_error",
                "every_fixed_selected_cell_eventually_zero": True,
                "uniform_error_each_depth": "1",
                "uniform_convergence": False,
            },
            "sufficient_contract": [
                "positive_common_material_radius",
                "uniform_factor_bounds",
                "weighted_block_remainder_to_zero",
                "side_tagged_two_sided_trace_current_summability",
                "nonautonomous_stopped_derivative_sum_finite",
            ],
            "actual_contract_rows": "0/5",
        },
        "gate24_tail_frontier": {
            "status": "EXACT_SURVIVAL_AND_VARIATION_SEPARATORS_CERTIFIED__ACTUAL_FULL_HAZARDS_ABSENT",
            "survival_identity": "eta(S_N)/eta(S_0)=product_(n<=N)(1-h_n)",
            "hazard_rows": hazard_rows,
            "square_limit": "1/2",
            "harmonic_limit": "0",
            "alternating_variation_separator": {
                "level_increment": "(-1)^n/n",
                "increments_tend_to_zero": True,
                "per_level_variation_bounded": True,
                "total_absolute_variation": "infinity",
                "conditional_cancellation_not_weighted_BV": True,
            },
            "required_actual_rows": [
                "same_key_full_conditional_hazards",
                "marker_saturation",
                "strict_path_budget",
                "weighted_transverse_variation",
                "physical_strong_recipient",
            ],
            "actual_full_hazard_rows": "0",
            "gate2_official_fields": "0/17",
            "gate4_landing_join": "1/7__FIELDS_1_4_7_PARTIAL",
        },
        "gate5_positive_potential_frontier": {
            "status": "SECTORWISE_RESOLVENT_CRITERION_CERTIFIED__ACTUAL_TERMINAL_KERNEL_ABSENT",
            "minimal_potential": "H=sum_(j>=0)K^j r",
            "resolvent_bound": "norm(H)<=norm(r)/(1-alpha)_when_norm(K)<=alpha<1",
            "charge_weight": "3/2",
            "attenuated_example": {
                "beta": "1/3", "weighted_ratio": "1/2", "total_potential": "2",
            },
            "critical_example": {
                "beta": "2/3", "weighted_ratio": "1", "total_potential": "infinity",
            },
            "required_sectors": gate5_sectors,
            "actual_new_sectors_closed": "0/7",
            "conditional_terminal_killing_equals_deterministic_eligibility": False,
            "finite_integrated_charge_implies_L_infinity_operator_bound": False,
            "gate5_maturity": "10/18__COMPLETE_BLOCKS_0",
        },
        "technology_boundary": {
            "checked_on": "2026-07-21",
            "queries": [
                "moving scatterers response", "dispersing billiards linear response",
                "sequential dispersing billiards", "recent SRB Markov partition",
            ],
            "arxiv_2502_07765v2": "SEQUENTIAL_CLT_AFTER_PROJECTIVE_CONE_INPUTS__NO_MOVING_BOUNDARY_REGISTRY",
            "arxiv_2104_06947v3": "PROJECTIVE_CONE_MEMORY_LOSS__NO_IMMUTABLE_PHYSICAL_CROSSWALK",
            "arxiv_2604_18929v3": "SMOOTH_AXIOM_A_SRB_PRODUCT__NO_COLLISION_SINGULARITIES",
            "new_same_law_moving_billiard_response_theorem_found": False,
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact presence")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result,
        "verdict": result["strict_status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            validate_pins(HERE, PINS)
            result = build_result()
            print(json.dumps({"digest": result["internal_replay_digest"], "status": "PASS"}, sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError, RuntimeError) as exc:
        print(f"ROUND68_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND68 COMMON ROOT AND ALL GATES: FRONTIER_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
