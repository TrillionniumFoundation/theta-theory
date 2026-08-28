#!/usr/bin/env python3
"""Producer for the append-only Round-65 Gate-1/3 frontier certificate."""

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
RESULT_SCHEMA = "cm2.gate13.round65.actual-cross-tail-piola-current-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round65-actual-cross-tail-piola-current-frontier"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_gate13_round65_actual_cross_tail_piola_current_frontier_verifier.py"
COMMON = HERE / "cm2_round64_common.py"

PINS = {
    "cm2-sixty-fourth-direct-assault-2026-07-21.md":
        "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256":
        "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-2026-07-21.md":
        "786922ef94b522498440cf90df562c77a65d991a03c01637d9740a22f0dcae49",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json":
        "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "d61e8f2ea2d3e5b172846a16fdfa75373058ec8b91759aea0e393c500ea0740b",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-assault-2026-07-21.md":
        "c4c1574e546900947a9248275f8a8be16d5b67e6e186c04b818da05fe4900f3a",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256":
        "c7552aa293baad4a021f85bff9c5cba3a15001d78a3e103e6f89cfc2b7c44319",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-assault-2026-07-21.md":
        "338f2aebff9501e8457d978898dc8c1cd9bfe06e1cc9a3d720bba7163d78cdeb",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json":
        "81a994f232af17d050a1582c396f8deeaae09e86856b5290e5eda764a238d4b8",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.sha256":
        "55fd5b62f3bab1fbea0c3334b4264176ab0bde8f140f3b7241d131b684756722",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-assault-2026-07-21.md":
        "3b75e26e9f5ec518e621b5c575ddddb5d7b66254ada4cb87ecec8bbaac788751",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md":
        "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json":
        "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256":
        "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256":
        "c446a1a0f9ef2c67871181a96e4dc6d0bdf7890b739a6f9a2bba13ef6fd5b37b",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def mmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
             for j in range(2)] for i in range(2)]


def matrix_strings(matrix: list[list[Q]]) -> list[list[str]]:
    return [[qstr(entry) for entry in row] for row in matrix]


def resonant_model(a: Q, b: Q, ell: Q, u: Q, name: str) -> dict[str, Any]:
    stable = [[a, Q(0)], [ell, 1 / a]]
    unstable = [[b, u], [Q(0), 1 / b]]
    loop = mmul(stable, unstable)
    wedges = [-loop[1][0], loop[0][0], -loop[1][1], loop[0][1]]
    determinant = loop[0][0] * loop[1][1] - loop[0][1] * loop[1][0]
    return {
        "name": name,
        "a": qstr(a), "b": qstr(b), "l": qstr(ell), "u": qstr(u),
        "stable": matrix_strings(stable),
        "unstable": matrix_strings(unstable),
        "loop": matrix_strings(loop),
        "determinant": qstr(determinant),
        "four_oriented_wedges": [qstr(value) for value in wedges],
        "all_four_nonzero": all(value != 0 for value in wedges),
        "noncancellation_scalar": qstr(1 + a * b * ell * u),
    }


def build_result() -> dict[str, Any]:
    selected_rate = Q(91, 1000)
    qnl_rho_display = Q(9281, 100000)
    cross_rows = []
    for n in range(1, 9):
        bad_r = Q(1, 4**n)
        bad_du = Q((-1) ** n, 4**n)
        cross_rows.append({
            "n": n,
            "selected_decay_row": qstr(selected_rate**n),
            "bad_plaque_R_n": qstr(bad_r),
            "bad_plaque_du_n": qstr(bad_du),
            "bad_plaque_T_n": qstr(bad_du / bad_r),
        })

    critical = resonant_model(Q(1), Q(1), Q(-1), Q(1),
                              "round64_critical_one_zero_wedge")
    all_four = resonant_model(Q(1), Q(1), Q(-1, 2), Q(1),
                              "nearby_all_four_nonzero")

    trace_rows = []
    for n in (1, 2, 4, 8, 16, 32):
        trace_rows.append({
            "N": n,
            "f_N": "2N(1-Nx)_+",
            "L1_norm": "1",
            "right_trace_at_zero": str(2 * n),
            "moving_current_coefficient": str(2 * n),
        })

    translation_rows = []
    for j in range(7):
        h = Q(1, 2**j)
        translation_rows.append({
            "h": qstr(h),
            "L1_norm": qstr(h * h),
            "derivative_L1_norm": qstr(2 * h),
            "W11_norm": qstr(h * h + 2 * h),
            "difference_quotient_remainder_L1": qstr(2 * h),
            "remainder_over_W11": qstr(Q(2, 1) / (h + 2)),
        })

    stopped_rows = []
    for cutoff in (1, 2, 4, 8, 16, 32):
        mass = sum((Q(1, n * (n + 1)) for n in range(1, cutoff + 1)), Q(0))
        derivative = sum((Q(1, n + 1) for n in range(1, cutoff + 1)), Q(0))
        stopped_rows.append({
            "cutoff": cutoff,
            "partial_mass": qstr(mass),
            "partial_depth_weighted_derivative": qstr(derivative),
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "direct_pin_count": len(PINS),
            "pins": PINS,
        },
        "gate1": {
            "selected_QNL_vs_combined_Green_typing": {
                "status": "CERTIFIED_EXACT_TYPE_MISMATCH",
                "q_QNL": qstr(selected_rate),
                "rho_QNL_display_upper": qstr(qnl_rho_display),
                "tempting_display_quotient": qstr(selected_rate / qnl_rho_display),
                "tempting_display_quotient_less_than_one": selected_rate < qnl_rho_display,
                "q_QNL_role": "selected compact-log inverse graph contraction",
                "rho_QNL_role": "selected compact-log upper critical conjugated tail ratio",
                "round64_numerator_role": "uniform all-plaque lower-Green Holder defect rate lambda_u^alpha",
                "round64_denominator_role": "uniform all-plaque lower bound rho_star for the combined-Green diagonal product",
                "same_gauge": False,
                "same_registry": False,
                "same_quantifier": False,
                "same_inequality_direction": False,
                "lawful_q_cross_instantiation": False,
            },
            "two_plaque_completion_separator": {
                "status": "CERTIFIED_EXACT_LOGICAL_SEPARATOR",
                "rows": cross_rows,
                "selected_sequence_decays": True,
                "bad_plaque_T_n_alternates": True,
                "all_plaque_uniform_limit": False,
                "scope": "logical all-plaque completion; not a billiard realization",
            },
            "four_wedge_resonant_criterion": {
                "status": "CERTIFIED_EXACT_IFF",
                "stable": "H_A^s+L_s=[[a,0],[l,a^-1]]",
                "unstable": "H_A^u+L_u=[[b,u],[0,b^-1]]",
                "loop": "[[ab,au],[lb,lu+(ab)^-1]]",
                "four_wedges": "[-lb,ab,-(lu+(ab)^-1),au]",
                "standing_hypothesis": "a*b!=0",
                "iff": "l!=0 and u!=0 and 1+a*b*l*u!=0",
                "models": [critical, all_four],
                "actual_same_representative_a_b_l_u": "NOT_CERTIFIED",
                "actual_noncancellation": "NOT_CERTIFIED",
            },
            "actual_join": {
                "supporting_rows_total": 9,
                "positive_physical_input_rows": 4,
                "typing_obstruction_rows": 1,
                "selected_QNL_loop_and_wedges": "CERTIFIED_LOCAL_DIFFERENT_GAUGE",
                "finite_faithful_clean_SFT": "CERTIFIED",
                "separate_all_plaque_Green_gauges": "CERTIFIED_THEOREMS",
                "one_cross_term_identity": "CERTIFIED_EXACT",
                "QNL_to_combined_constant_substitution": "CERTIFIED_FALSE_TYPING",
                "actual_uniform_Holder_limit_T_n": "NOT_CERTIFIED",
                "actual_same_representative_tail_scalars": "NOT_CERTIFIED",
                "exact_compact_to_combined_loop_transport": "NOT_CERTIFIED",
                "full_mass_physical_PPE": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "gate3": {
            "material_coordinate_calculus": {
                "status": "CERTIFIED_EXACT_INTERFACE",
                "definitions": [
                    "Rhat_s=J_s^-1 R_s",
                    "Phat_s=J_s^-1 P_s J_s",
                    "Qhat_s=Q_s J_s",
                ],
                "factorization": "T_s=Qhat_s Phat_s Rhat_s",
                "derivative": "DT=(DQhat)Phat Rhat+Qhat(DPhat)Rhat+Qhat Phat(DRhat)",
                "material_cell_consequence": "R_s=J_s R_0 implies Rhat_s=R_0 and DRhat=0",
                "not_absorbed_by_J_s": [
                    "branch birth or death",
                    "mismatched physical incidence",
                    "immutable output-time tag change",
                    "cemetery arrival",
                ],
                "actual_common_finite_s_material_atlas": "NOT_CERTIFIED",
            },
            "strong_trace_criterion": {
                "status": "CERTIFIED_EXACT_IFF_ON_TAGGED_CURRENT_SUM",
                "one_cut": "DR_0 f=e'(0)(gamma_e^-(f)delta_e,-gamma_e^+(f)delta_e)",
                "countable": "Gamma f=(abs(e_k')gamma_k^-(f),abs(e_k')gamma_k^+(f))_k is bounded X->ell1",
                "necessity_source": "retained side/face tags make the current rows disjoint",
                "weak_L1_separator_rows": trace_rows,
                "weak_L1_norm_one_implies_strong_trace": False,
                "actual_physical_weighted_trace_operator": "NOT_CERTIFIED",
            },
            "Piola_derivative_loss": {
                "status": "CERTIFIED_EXACT_SEPARATOR",
                "family": "phi(t)=(1-abs(t))_+; f_h(x)=h phi(x/h); tau_h f(x)=f(x+h)",
                "rows": translation_rows,
                "limit_remainder_over_W11": "1",
                "operator_norm_differentiable_W11_to_L1": False,
                "pointwise_differentiable_for_each_fixed_W11_vector": True,
                "W21_sufficient_remainder": "||(tau_s f-f)/s-f'||_1<=abs(s)||f''||_1/2",
                "actual_anisotropic_o_s_remainder": "NOT_CERTIFIED",
            },
            "stopped_MT_DQ": {
                "status": "CERTIFIED_EXACT_DEPTH_WEIGHTED_INTERFACE",
                "iterate_rule": "D(T^n)=sum_(k=0)^(n-1)T^(n-1-k)(DT)T^k",
                "norm_bound": "||D(T^n)||<=n M^(n-1)L when ||T||<=M and ||DT||<=L",
                "separator_law": "p_n=1/[n(n+1)]",
                "rows": stopped_rows,
                "total_mass": "1",
                "depth_weighted_derivative_sum": "DIVERGES",
                "finite_stopped_mass_implies_MT_DQ": False,
                "actual_same_law_depth_weighted_derivative_ledger": "NOT_CERTIFIED",
            },
            "physical_boundary": {
                "actual_stopped_Borel_partition": "CERTIFIED",
                "actual_weak_graph_TV_R_Q": "CERTIFIED_NORM_ONE",
                "regular_base_F13_face_charge": "CERTIFIED",
                "common_finite_s_material_J_s": "NOT_CERTIFIED",
                "strong_weighted_trace_Gamma": "NOT_CERTIFIED",
                "dyadic_clock_and_strong_cemetery": "NOT_CERTIFIED",
                "anisotropic_Piola_generator_and_remainder": "NOT_CERTIFIED",
                "bounded_differentiable_Rhat_Phat_Qhat": "NOT_CERTIFIED",
                "physical_MT_DQ": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "latest_same_type_technology_audit": {
            "checked_on": "2026-07-21",
            "arxiv_2603_19509v3": "abstract framework assumes strong differentiability and memory loss; verified applications are sequential C3 expanding maps and noisy random maps",
            "arxiv_2604_25746v1": "Bernoulli theorem on a compact boundaryless manifold; singularities are vector-field zeros/fixed flow points, not billiard collision discontinuities",
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
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
    require(DEFAULT_REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result,
        "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    g1 = result["gate1"]
    require(g1["selected_QNL_vs_combined_Green_typing"]["tempting_display_quotient"] == "9100/9281",
            "QNL display quotient")
    require([row["bad_plaque_T_n"] for row in g1["two_plaque_completion_separator"]["rows"]]
            == ["-1", "1", "-1", "1", "-1", "1", "-1", "1"],
            "alternating cross tail")
    models = g1["four_wedge_resonant_criterion"]["models"]
    require(models[0]["all_four_nonzero"] is False and models[1]["all_four_nonzero"] is True,
            "four-wedge models")
    g3 = result["gate3"]
    require(g3["strong_trace_criterion"]["weak_L1_separator_rows"][-1]["moving_current_coefficient"] == "64",
            "trace separator")
    require(g3["Piola_derivative_loss"]["rows"][-1]["remainder_over_W11"] == "128/129",
            "translation separator")
    require(g3["stopped_MT_DQ"]["rows"][0] == {
        "cutoff": 1, "partial_mass": "1/2", "partial_depth_weighted_derivative": "1/2"
    }, "stopped first row")
    return {"pins": f"{len(PINS)}/{len(PINS)}", "gate1": "PASS", "gate3": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
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
        print(f"ROUND65_GATE13_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1: NOT_CERTIFIED")
    print("Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
