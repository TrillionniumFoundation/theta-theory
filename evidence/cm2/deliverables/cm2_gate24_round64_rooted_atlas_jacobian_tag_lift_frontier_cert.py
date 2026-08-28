#!/usr/bin/env python3
"""Producer for the append-only Round-64 Gate-2/4 frontier certificate."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round64_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round64.rooted-atlas-jacobian-tag-lift.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate24_round64_rooted_atlas_jacobian_tag_lift_frontier_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-third-direct-assault-2026-07-21.md":
        "9cde412ba689be87d777906404c9c9426a2a8a102385a2c4c510df8f9b7a6a05",
    "cm2-sixty-third-direct-assault-manifest-2026-07-21.sha256":
        "a0b512f32914ef2692b31466a4ea156c44698b1eaf44d8ead45b2c74ee73230e",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.json":
        "3aae6d018fc15aaab47116d311eed8333c56b87542b0b5761b849221cbf76d6b",
    "cm2-round63-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "8227dd32e36d2879f9dbbdced54f3c50b3eac1536ce8fceac480d22cb8617bfd",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json":
        "955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256":
        "a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def scalar_weighted_median(values: list[Q], weights: list[Q]) -> Q:
    ordered = sorted(zip(values, weights), key=lambda row: row[0])
    cumulative = Q(0)
    for value, weight in ordered:
        cumulative += weight
        if cumulative >= Q(1, 2):
            return value
    raise CertError("weighted median")


def weighted_cost(values: list[Q], weights: list[Q], median: Q) -> Q:
    return sum((w * abs(x - median) for x, w in zip(values, weights)), Q(0))


def pairwise(values: list[Q], weights: list[Q]) -> Q:
    return sum((weights[i] * weights[j] * abs(values[i] - values[j])
                for i in range(len(values)) for j in range(i + 1, len(values))), Q(0))


def build_result() -> dict[str, Any]:
    bridge = {
        "a_u": Q(2), "b_u": Q(3), "a_v": Q(4), "b_v": Q(5),
        "j_minus": Q(6), "j_plus": Q(7), "F": Q(2), "R": Q(3),
        "theta": Q(1, 2), "L": Q(10), "C_p_test": Q(100),
    }
    m = bridge["a_u"] / (bridge["j_plus"] * bridge["b_v"])
    big_m = bridge["b_u"] / (bridge["j_minus"] * bridge["a_v"])
    original_left = bridge["F"] * bridge["R"] * big_m
    original_right = bridge["C_p_test"] * m * m * bridge["theta"] * bridge["L"]
    transformed_left = (bridge["F"] * bridge["R"] * bridge["b_u"] *
                        bridge["j_plus"]**2 * bridge["b_v"]**2)
    transformed_right = (bridge["C_p_test"] * bridge["j_minus"] * bridge["a_v"] *
                         bridge["a_u"]**2 * bridge["theta"] * bridge["L"])

    weights = [Q(1, 5), Q(1, 2), Q(3, 10)]
    markers = [[Q(0), Q(1)], [Q(1), Q(3)], [Q(4), Q(0)]]
    medians: list[Q] = []
    costs: list[Q] = []
    dispersions: list[Q] = []
    for coordinate in range(2):
        values = [marker[coordinate] for marker in markers]
        median = scalar_weighted_median(values, weights)
        medians.append(median)
        costs.append(weighted_cost(values, weights, median))
        dispersions.append(pairwise(values, weights))
    delta = sum(costs, Q(0)) / 2
    dispersion = sum(dispersions, Q(0)) / 2

    tag_rows = []
    for n in range(1, 13):
        mass = Q(3, 4**n)
        weight = Q(2**n)
        tag_rows.append({
            "n": n, "kappa_mass": qstr(mass), "tag_weight": qstr(weight),
            "moment_term": qstr(mass * weight), "unit_L1_atom_lift_norm": qstr(weight),
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True, "old_artifacts_modified": False,
            "pinned_round63_and_actual_graph": PINS,
        },
        "jacobian_arclength_bridge": {
            "status": "CERTIFIED_EXACT_CONDITIONAL",
            "compatibility": "J(hx)rho_v(hx)=rho_u(x)/lambda(x)",
            "lambda": "rho_u(x)/(J(hx)rho_v(hx))",
            "zero_marker_defect_transport": "psi_v(hx)=psi_u(x)/lambda(x)",
            "strict_budget": "F R b_u j_+^2 b_v^2<C_p j_- a_v a_u^2 theta L",
            "replay": {
                **{key: qstr(value) for key, value in bridge.items()},
                "m_lower": qstr(m), "M_upper": qstr(big_m),
                "original_left": qstr(original_left), "original_right": qstr(original_right),
                "transformed_left": qstr(transformed_left),
                "transformed_right": qstr(transformed_right),
                "both_strict": original_left < original_right and transformed_left < transformed_right,
            },
            "actual_density_J_metric_rows": "NOT_CERTIFIED",
        },
        "rooted_atlas_saturation": {
            "status": "CERTIFIED_EXACT_COUNTABLE_INTERFACE",
            "integrability": "sum_i w_i ||P_i^-1 g_i||_1<infinity",
            "formula": "delta=integral inf_t sum_i w_i |P_i^-1 g_i-t| dmu_0",
            "zero_iff_all_pulled_back_markers_equal": True,
            "pairwise_sandwich": "P<=delta<=2P",
            "commuting_tree_source_landing_delta_equal": True,
            "replay": {
                "weights": [qstr(x) for x in weights],
                "markers": [[qstr(x) for x in marker] for marker in markers],
                "coordinate_medians": [qstr(x) for x in medians],
                "coordinate_costs": [qstr(x) for x in costs],
                "coordinate_pairwise": [qstr(x) for x in dispersions],
                "delta_atlas": qstr(delta), "P": qstr(dispersion),
                "strict_sandwich": dispersion < delta < 2 * dispersion,
            },
            "actual_root_edges_zero_defect": "NOT_CERTIFIED",
        },
        "graph_tag_lift": {
            "actual_round62_covariance": "CERTIFIED_PINNED",
            "exact_norm": "||L_K nu||_X_D=integral W_D d|nu|",
            "bounded_iff": "W_D in L_infinity(kappa_B)",
            "operator_norm": "ess_sup W_D",
            "separator": {
                "law": "kappa_n=3*4^-n; D(n)=n; deterministic K",
                "rows": tag_rows,
                "full_mass": "1",
                "full_one_vector_moment": "3",
                "W_D_unbounded": True,
                "unit_L1_atom_lift_norm_tends_to_infinity": True,
            },
            "actual_weighted_operator_bound": "NOT_CERTIFIED",
            "physical_anisotropic_Piola_lift": "NOT_CERTIFIED",
        },
        "latest_technology_boundary": {
            "arxiv_2604_25881v1": "local product structure for MME, not collision-SRB owner law",
            "arxiv_2606_10155v1": "review, not a physical landing materialization",
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
    return {
        "schema": MANIFEST_SCHEMA, "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result, "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    atlas = result["rooted_atlas_saturation"]["replay"]
    require(Q(atlas["delta_atlas"]) == Q(6, 5) and Q(atlas["P"]) == Q(3, 4),
            "atlas replay")
    separator = result["graph_tag_lift"]["separator"]
    require(Q(separator["full_mass"]) == 1 and Q(separator["full_one_vector_moment"]) == 3,
            "tag separator")
    return {"pins": "8/8", "atlas": "PASS", "tag_rows": 12, "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            print(json.dumps(replay(), sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND64_GATE24_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate2: NOT_CERTIFIED")
    print("Gate4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
