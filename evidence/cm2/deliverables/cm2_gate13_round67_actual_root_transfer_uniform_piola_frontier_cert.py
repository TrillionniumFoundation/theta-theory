#!/usr/bin/env python3
"""Producer for the append-only Round-67 Gate-1/3 frontier certificate."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round67.actual-root-transfer-uniform-piola-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round67-actual-root-transfer-uniform-piola-frontier"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_gate13_round67_actual_root_transfer_uniform_piola_frontier_verifier.py"
COMMON = HERE / "cm2_round67_common.py"

PINS = {
    "cm2-sixty-sixth-direct-assault-2026-07-21.md":
        "690cfeb13108314a3a05f5e4cd342d573c41e66551464ebf7f4b5576f374b811",
    "cm2-sixty-sixth-direct-assault-manifest-2026-07-21.sha256":
        "b437761fb84aa431e468af587e2207adadf6e0a996ee593a93df467147be3b5d",
    "cm2-round66-independent-core-frontier-audit-2026-07-21.md":
        "68d9b65f843c6e35e9f8c5e6954fb76e87970fc9bc558e691cecaafeb9850ebd",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.json":
        "b67b76e52d073989fac6fb41eaf3e49167aa1e166d32003c72129e08ec6d46b3",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "6d09b81b683464dcf45815ed9e98635c6c3a94087c19b0e4528eaf4c1659175e",
    "cm2-gate13-round66-same-representative-material-trace-frontier-assault-2026-07-21.md":
        "6d37428dde6b8360d759554a9bcd2bfeb91b0c67c0ab3bcc98d91d850fa49278",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json":
        "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256":
        "4d38f3145099b2cd4222930d32c88dd7ba6bc9797def4673fc9ea00415f3b38e",
    "cm2-gate1-global-coding-class-h-separation-frontier-assault-2026-07-16.md":
        "7ec0d1545ac7ebc52a03ac871adfe10fb7a9b7a070a9d91ee3fcf116d8edfda2",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json":
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.sha256":
        "2187c87105f2b86c9906856733fa025763981b852e54ed0715ba3934dc515d0f",
    "cm2-gate1-variable-diagonal-groupoid-frontier-assault-2026-07-17.md":
        "bbee54be4aea1df1d9b00a8a97145029ee68fd538aa44931dd2b21d1644c1fdd",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.json":
        "dacbae6255707086bc7486e4933d8c890ede1547a9e545995800a5fc18698f83",
    "cm2-gate1-variable-diagonal-groupoid-frontier-manifest-2026-07-17.sha256":
        "9d98591462771a9e553dd93c24518642c22aa2832c269a8380bd827a76666200",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256":
        "c446a1a0f9ef2c67871181a96e4dc6d0bdf7890b739a6f9a2bba13ef6fd5b37b",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md":
        "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json":
        "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256":
        "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-assault-2026-07-21.md":
        "3b75e26e9f5ec518e621b5c575ddddb5d7b66254ada4cb87ecec8bbaac788751",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-assault-2026-07-21.md":
        "c4c1574e546900947a9248275f8a8be16d5b67e6e186c04b818da05fe4900f3a",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.sha256":
        "c7552aa293baad4a021f85bff9c5cba3a15001d78a3e103e6f89cfc2b7c44319",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
             for j in range(2)] for i in range(2)]


def det(a: list[list[Q]]) -> Q:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: list[list[Q]]) -> list[list[Q]]:
    d = det(a)
    require(d != 0, "singular matrix")
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def smat(a: list[list[Q]]) -> list[list[str]]:
    return [[qstr(x) for x in row] for row in a]


def is_power_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def path_ledger(m: list[Q], ell: list[Q]) -> Q:
    require(len(m) == len(ell) and len(m) > 0, "path ledger input")
    total = Q(0)
    for r, lr in enumerate(ell):
        product = Q(1)
        for i, mi in enumerate(m):
            if i != r:
                product *= mi
        total += lr * product
    return total


def build_result() -> dict[str, Any]:
    q_matrix = [[Q(1), Q(1, 2)], [Q(0), Q(1)]]
    e_matrix = [[Q(2), Q(1)], [Q(1), Q(1)]]
    d_matrix = [[Q(13, 12), Q(1, 4)], [Q(1, 3), Q(1)]]
    c_matrix = matmul(matmul(inv(q_matrix), e_matrix), d_matrix)

    defect_rows = []
    for n in range(1, 9):
        defect_rows.append({
            "n": n,
            "endpoint_amplitude_zero": "0",
            "endpoint_amplitude_constant_completion": qstr(Q(1, 4 ** n)),
            "endpoint_amplitude_oscillatory_completion": qstr(Q((-1) ** n, 4 ** n)),
            "renormalized_zero": "0",
            "renormalized_constant": "1",
            "renormalized_oscillatory": str((-1) ** n),
        })

    radius_rows = [{"finite_cutoff": n, "minimum_radius": qstr(Q(1, n))}
                   for n in (1, 2, 4, 8, 16, 32)]

    weighted_rows = []
    for k, (a, b, block) in enumerate(((Q(1), Q(2), Q(1, 3)),
                                        (Q(2), Q(1), Q(4)),
                                        (Q(4), Q(8), Q(1, 2))), start=1):
        weighted_rows.append({
            "block": k, "input_weight": qstr(a), "output_weight": qstr(b),
            "block_norm": qstr(block), "weighted_block_norm": qstr(b * block / a),
        })

    composition_rows = []
    q0, p0, r0 = Q(2), Q(3), Q(5)
    q1, p1, r1 = Q(7), Q(11), Q(13)
    q2, p2, r2 = Q(17), Q(19), Q(23)
    base = q0 * p0 * r0
    derivative = q1 * p0 * r0 + q0 * p1 * r0 + q0 * p0 * r1
    for n in (2, 4, 8, 16, 32):
        s = Q(1, n)
        qs, ps, rs = q0 + s * q1 + s * s * q2, p0 + s * p1 + s * s * p2, r0 + s * r1 + s * s * r2
        normalized = (qs * ps * rs - base - s * derivative) / s
        composition_rows.append({"N": n, "s": qstr(s), "normalized_remainder": qstr(normalized)})

    nonautonomous_rows = []
    good_partial, spike_partial = Q(0), Q(0)
    for n in range(1, 33):
        good_m = [Q(1) if is_power_two(i + 1) else Q(1, 2) for i in range(n)]
        good_l = [Q(1) for _ in range(n)]
        spike_m = [Q(1, 2) for _ in range(n)]
        spike_l = [Q(2 ** (i + 1) * (i + 1)) for i in range(n)]
        good_a = path_ledger(good_m, good_l)
        spike_a = path_ledger(spike_m, spike_l)
        weight = Q(1, n * (n + 1))
        good_partial += weight * good_a
        spike_partial += weight * spike_a
        if n in (1, 2, 4, 8, 16, 32):
            nonautonomous_rows.append({
                "n": n, "good_A_n": qstr(good_a), "spike_A_n": qstr(spike_a),
                "good_weighted_partial": qstr(good_partial),
                "spike_weighted_partial": qstr(spike_partial),
                "good_bound_4n2_2^-n": qstr(Q(4 * n * n, 2 ** n)),
            })

    trace_rows = []
    trace_total = Q(0)
    for tag, w, v, minus, plus in (
        ("face", Q(1), Q(3), Q(1), Q(2)),
        ("clock", Q(2), Q(1, 4), Q(3), Q(4)),
        ("one_shot_cemetery", Q(1, 2), Q(2), Q(5), Q(6)),
    ):
        charge = w * abs(v) * (minus + plus)
        trace_total += charge
        trace_rows.append({
            "tag": tag, "weight": qstr(w), "speed": qstr(v),
            "minus_norm": qstr(minus), "plus_norm": qstr(plus),
            "tagged_charge": qstr(charge),
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
            "maximal_actual_root_crosswalk": {
                "status": "CERTIFIED_ACTUAL_ROOT_AND_EXACT_FORMAL_TRANSFER",
                "root": "finite clean (Sigma_A,sigma,pi) containing immutable QNL p and selected homoclinic z_h",
                "physical_cocycle": "A_log(x)=E_0(sigma x)^-1 D_(pi x)G E_0(x)",
                "diagonal_frame": "A_diag=E(sigma x)^-1 A_log E(x)",
                "compact_representation": "A_q=Q(sigma x)^-1 A_log Q(x)",
                "combined_representation": "A_c=(E D)(sigma x)^-1 A_log(E D)(x), D=U_v L_u",
                "relative_transfer": "C=Q^-1 E D",
                "cohomology": "A_c=C(sigma x)^-1 A_q C(x)",
                "same_root_tokens": "CERTIFIED",
                "same_physical_derivative_cocycle": "CERTIFIED",
                "same_key_Q_E_u_v_rows": "NOT_CERTIFIED",
                "numeric_all_plaque_C_and_inverse_bounds": "NOT_CERTIFIED",
                "rational_replay": {
                    "Q": smat(q_matrix), "E": smat(e_matrix), "D": smat(d_matrix),
                    "C": smat(c_matrix), "det_Q": qstr(det(q_matrix)),
                    "det_E": qstr(det(e_matrix)), "det_D": qstr(det(d_matrix)),
                    "det_C": qstr(det(c_matrix)),
                },
            },
            "endpoint_completion_separator": {
                "status": "CERTIFIED_SHARP_NONDETERMINATION",
                "source": "A=diag(2,1/2) on a stable orbit with distance 2^-n",
                "completions": ["C_0=I", "C_+=I+4^-n E_21", "C_osc=I+(-1)^n4^-n E_21"],
                "shared_properties": ["SL(2)", "Lipschitz on orbit closure", "C(p)=I", "identical selected-orbit values"],
                "renormalized_defects": ["0", "E_21", "(-1)^n E_21"],
                "rows": defect_rows,
                "selected_constants_determine_actual_endpoint_limits": False,
            },
            "wedge_transport_boundary": {
                "status": "CERTIFIED_EXACT_TYPED_BOUNDARY",
                "target_loop": "Psi_c=C(p)^-1(H_q^s+L_s)(H_q^u+L_u)C(p)",
                "unchanged_loop_iff": "H_q^s L_u+L_s H_q^u+L_s L_u=0",
                "simultaneous_exact_transport_preserves_nonzero_wedges": True,
                "actual_tail_limits": "NOT_CERTIFIED",
                "actual_combined_loop_replay": "NOT_CERTIFIED",
                "actual_four_wedges_in_combined_family": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "gate3": {
            "common_material_window": {
                "status": "CERTIFIED_EXACT_IFF",
                "radius_definition": "r_k is the supremal admissible connected material radius for branch k",
                "criterion": "r_*=inf_k r_k>0",
                "actual_depth96_compact_core_radius": "POSITIVE_LOCAL",
                "actual_all_cell_all_depth_infimum": "NOT_CERTIFIED",
                "separator": "r_k=1/k",
                "rows": radius_rows,
            },
            "weighted_direct_sum": {
                "status": "CERTIFIED_EXACT_IFF",
                "operator_norm": "sup_k (b_k/a_k)||J_k||",
                "remainder_norm": "sup_k (b_k/a_k)||J_(s,k)-J_(0,k)-sG_k||/abs(s)",
                "rows": weighted_rows,
                "replay_supremum": "2",
                "actual_uniform_weighted_remainder": "NOT_CERTIFIED",
            },
            "three_factor_uniform_piola": {
                "status": "CERTIFIED_SUFFICIENT_STRONG_BRIDGE",
                "derivative": "Q_1P_0R_0+Q_0P_1R_0+Q_0P_0R_1",
                "remainder_bound": "A^2 sum_F epsilon_F(s)+3 abs(s) A B^2+abs(s)^2 B^3",
                "scalar_base": qstr(base), "scalar_derivative": qstr(derivative),
                "rows": composition_rows,
                "product_differentiability_implies_each_factor": False,
                "cancellation_separator": "R_s=I+sS, P_s=I, Q_s=(I+sS)^-1",
                "actual_strong_Rhat_Phat_Qhat": "NOT_CERTIFIED",
            },
            "side_tagged_trace_current": {
                "status": "CERTIFIED_EXACT_IFF",
                "norm": "sum_e w_e abs(v_e)(||U_e^-Gamma_e^-x||+||U_e^+Gamma_e^+x||)",
                "bounded_iff": "sup over ||x||<=1 of the tagged norm is finite",
                "side_tags_disjoint": True,
                "signed_cross_side_cancellation_allowed": False,
                "rows": trace_rows,
                "replay_total": qstr(trace_total),
                "actual_two_sided_strong_trace": "NOT_CERTIFIED",
                "actual_clock_face_cemetery_current": "NOT_CERTIFIED",
            },
            "nonautonomous_stopped_MT_DQ": {
                "status": "CERTIFIED_EXACT_POSITIVE_SCALAR_AND_SHARP_MAJORANT",
                "path_ledger": "A_n=sum_(r<n)L_r product_(i<n,i!=r)M_i",
                "stopped_criterion": "sum_n p_n A_n<infinity",
                "homogeneous_reduction": "A_n=n L M^(n-1), hence L P'(M)",
                "good_model": "M_i=1 at i+1 powers of two and 1/2 otherwise; L_i=1",
                "good_bound": "A_n<=4 n^2 2^-n despite sup_i M_i=1",
                "spike_model": "M_i=1/2; L_i=2^(i+1)(i+1)",
                "spike_lower_bound": "A_n>=2n, so p_n=1/[n(n+1)] diverges",
                "rows": nonautonomous_rows,
                "actual_pathwise_M_i_L_i": "NOT_CERTIFIED",
                "actual_positive_all_depth_ledger": "NOT_CERTIFIED",
                "physical_MT_DQ": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "latest_same_type_technology_audit": {
            "checked_on": "2026-07-21",
            "arxiv_2502_07765v2": {
                "same_model_positive": "sequential dispersing billiards on a common phase space and common SRB reference under uniform flight, curvature and C3 bounds",
                "result": "projective-cone contraction and sequential CLT for NF-admissible blocks",
                "missing": "material-parameter differentiability, moving incidence atlas, two-sided face current, operator-norm Piola and MT_DQ",
            },
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
    root = result["gate1"]["maximal_actual_root_crosswalk"]
    require(root["rational_replay"]["det_C"] == "1", "relative transfer determinant")
    rows = result["gate1"]["endpoint_completion_separator"]["rows"]
    require(rows[0]["renormalized_oscillatory"] == "-1" and
            rows[1]["renormalized_oscillatory"] == "1", "oscillatory defect")
    g3 = result["gate3"]
    require(g3["weighted_direct_sum"]["replay_supremum"] == "2", "weighted supremum")
    require(g3["side_tagged_trace_current"]["replay_total"] == "47/2", "trace total")
    require(g3["nonautonomous_stopped_MT_DQ"]["rows"][-1]["n"] == 32 and
            g3["nonautonomous_stopped_MT_DQ"]["rows"][-1]["good_A_n"] == "29/33554432",
            "nonautonomous row")
    return {"pins": f"{len(PINS)}/{len(PINS)}", "gate1": "PASS", "gate3": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay or args.audit:
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
        print(f"ROUND67_GATE13_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1: NOT_CERTIFIED")
    print("Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
