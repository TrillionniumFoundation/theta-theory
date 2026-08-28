#!/usr/bin/env python3
"""Producer for the append-only Round-66 Gate-1/3 frontier certificate."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate13.round66.same-representative-material-trace-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate13-round66-same-representative-material-trace-frontier"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_gate13_round66_same_representative_material_trace_frontier_verifier.py"
COMMON = HERE / "cm2_round66_common.py"

PINS = {
    "cm2-sixty-fifth-direct-assault-2026-07-21.md":
        "aeaafaf3411e90d6d1843159e248f18af12e5fdf993acfb9685adcc1b14e7bb0",
    "cm2-sixty-fifth-direct-assault-manifest-2026-07-21.sha256":
        "22283d37c12651e955b2502ad7660fa22d309c1d1902c471b1527470d6cc1cc2",
    "cm2-round65-independent-core-frontier-audit-2026-07-21.md":
        "b33405043f505f3f6323a6faf0de8f33e3f4c1f28db7ac891a56b2242a4df9e4",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.json":
        "92ba883654f761a4df5974d889f99aa077769bb37ba0cd5d6fd03ceb8470629f",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "56cdbe5748338979e03eca9a859f119fda8c88d7b6663f530400f00f69583ed9",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-assault-2026-07-21.md":
        "634eb5d96d5837fb1a09f6c87d18b362a35d62be296c8a516d6e9ad648a016a8",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.json":
        "e87bb0896c1fc59b6b020d1325bd9462fd932f5d186acabb0fcf770ed9b34701",
    "cm2-gate13-round65-actual-cross-tail-piola-current-frontier-manifest-2026-07-21.sha256":
        "1adc6c78ae09bfd0113271794d5a99ad95655297e54e248c87c16eddbab6ab49",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md":
        "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json":
        "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256":
        "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
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
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-assault-2026-07-21.md":
        "338f2aebff9501e8457d978898dc8c1cd9bfe06e1cc9a3d720bba7163d78cdeb",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.json":
        "81a994f232af17d050a1582c396f8deeaae09e86856b5290e5eda764a238d4b8",
    "cm2-gate13-round64-resonant-tail-transport-current-clock-frontier-manifest-2026-07-21.sha256":
        "55fd5b62f3bab1fbea0c3334b4264176ab0bde8f140f3b7241d131b684756722",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.sha256":
        "c446a1a0f9ef2c67871181a96e4dc6d0bdf7890b739a6f9a2bba13ef6fd5b37b",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def matrix_strings(matrix: list[list[Q]]) -> list[list[str]]:
    return [[qstr(value) for value in row] for row in matrix]


def relative_transfer(uq: Q, vq: Q, uc: Q, vc: Q) -> dict[str, Any]:
    dv = vc - vq
    matrix = [
        [1 + dv * uc, dv],
        [uc - uq * (1 + dv * uc), 1 - uq * dv],
    ]
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return {
        "u_q": qstr(uq), "v_q": qstr(vq), "u_c": qstr(uc), "v_c": qstr(vc),
        "delta_v": qstr(dv), "matrix": matrix_strings(matrix),
        "determinant": qstr(det),
        "is_identity": matrix == [[Q(1), Q(0)], [Q(0), Q(1)]],
    }


def loop_correction(a: Q, b: Q, ell: Q, u: Q) -> dict[str, Any]:
    correction = [[Q(0), a * u], [ell * b, ell * u]]
    return {
        "a": qstr(a), "b": qstr(b), "l": qstr(ell), "u": qstr(u),
        "correction": matrix_strings(correction),
        "vanishes": all(value == 0 for row in correction for value in row),
    }


def build_result() -> dict[str, Any]:
    transfer_identity = relative_transfer(Q(2, 3), Q(5, 7), Q(2, 3), Q(5, 7))
    transfer_mismatch = relative_transfer(Q(1, 2), Q(1, 3), Q(2, 3), Q(5, 6))

    remainder_rows = []
    for n in (2, 4, 8, 16, 32, 64):
        remainder_rows.append({
            "N": n,
            "s": qstr(Q(1, n)),
            "fixed_branch_k_1_remainder": qstr(Q(1, n)),
            "global_supremum": "1",
        })

    depth_rows = []
    for cutoff in (1, 2, 4, 8, 16, 32):
        at_one = sum((Q(1, n + 1) for n in range(1, cutoff + 1)), Q(0))
        at_half = sum((Q(1, 2) ** (n - 1) / Q(n + 1)
                       for n in range(1, cutoff + 1)), Q(0))
        depth_rows.append({
            "cutoff": cutoff,
            "P_prime_at_1_partial": qstr(at_one),
            "P_prime_at_half_partial": qstr(at_half),
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
            "frozen_same_gauge_audit": {
                "status": "CERTIFIED_EXACT_FIELD_AUDIT",
                "selected_gauge_syntax": "B_u(x)B_s(y)",
                "selected_carrier": "one immutable QNL homoclinic in canonical eigenfibre E_p",
                "selected_tail_and_four_wedges": "CERTIFIED_LOCAL",
                "combined_gauge_syntax": "U_v L_u",
                "combined_one_sided_all_plaque": "CERTIFIED_THEOREMS",
                "same_scalar_functions": "NOT_CERTIFIED",
                "same_orbit_plaque_gauge_key": "NOT_CERTIFIED",
                "compact_to_combined_finite_loop": "NOT_CERTIFIED",
                "shared_triangular_syntax_implies_same_gauge": False,
                "lawful_frozen_QNL_to_T_n_transport": False,
            },
            "relative_shear_transfer": {
                "status": "CERTIFIED_EXACT_IFF",
                "definition": "C=G_q^-1 G_c=L_-u_q U_(v_c-v_q)L_u_c",
                "matrix": "[[1+dv*u_c,dv],[u_c-u_q*(1+dv*u_c),1-u_q*dv]]",
                "determinant": "1",
                "identity_iff": "v_c-v_q=0 and u_c=u_q",
                "models": [transfer_identity, transfer_mismatch],
            },
            "all_plaque_tail_transport": {
                "status": "CERTIFIED_EXACT_IFF_ON_COMMON_REGISTRY",
                "cohomology": "B(x)=C(fx)^-1 A(x)C(x)",
                "stable_defect": "Delta_n^s=A^n(y)^-1[C(f^n y)C(f^n x)^-1-I]A^n(x)",
                "finite_identity": "H_B^s(n)=C(y)^-1[H_A^s(n)+Delta_n^s]C(x)",
                "iff": "given A in class H and bounded Holder C,C^-1, B is class H iff forward/backward Delta_n have uniform Holder limits",
                "stable_limit": "H_B^s=C(y)^-1(H_A^s+L_s)C(x)",
                "unstable_limit": "H_B^u=C(y)^-1(H_A^u+L_u)C(x)",
                "zero_tail_required": False,
                "actual_common_registry": "NOT_CERTIFIED",
            },
            "selected_loop_transport": {
                "status": "CERTIFIED_EXACT_IFF",
                "target_loop": "Psi_B=C(p)^-1(H_A^s+L_s)(H_A^u+L_u)C(p)",
                "exact_source_loop_transport_iff": "H_A^s L_u+L_s H_A^u+L_s L_u=0",
                "simultaneous_axis_transport_preserves_nonzero_wedges": True,
                "diagonal_triangular_correction": "[[0,a*u],[l*b,l*u]]",
                "diagonal_source_exact_transport_iff": "l=0 and u=0 when a*b!=0",
                "models": [
                    loop_correction(Q(2), Q(3), Q(0), Q(0)),
                    loop_correction(Q(2), Q(3), Q(-1, 2), Q(1)),
                ],
                "actual_QNL_to_combined_tail_limits": "NOT_CERTIFIED",
                "actual_loop_correction_or_recomputation": "NOT_CERTIFIED",
            },
            "minimal_keyed_registry": {
                "status": "0/8_ACTUAL_COMMON_ROWS",
                "rows": [
                    "one base/orbit/plaque ID and physical cocycle",
                    "exact G_q and G_c on that carrier",
                    "oriented relative transfer and endpoint axes",
                    "all-plaque forward/backward Delta_n records",
                    "uniform limits and uniform Holder moduli",
                    "selected finite approximants aligned to QNL return counts",
                    "loop correction identity or direct changed-loop replay",
                    "four wedges in the same representative",
                ],
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "gate3": {
            "physical_compact_interior_atlas": {
                "status": "CERTIFIED_LOCAL",
                "physical_input": "positive-width strict 96-collision word plus exact circular branch formula",
                "compact_core": "K strictly inside one regular word cell",
                "margin": "abs(u_j dot n_(j+1))>=gamma and gamma<=tau_j<=3-gamma with positive clearance",
                "contact_tau_derivative": "2 R_i (u_j dot n_(j+1))",
                "conclusion": "one finite-parameter C2 material atlas on a compact physical depth-96 core",
                "smooth_local_remainder": "uniform O(s^2) on each fixed W21-to-L1-type regular scale",
                "all_cells_all_depth_common_s_window": "NOT_CERTIFIED",
                "physical_anisotropic_recipient": "NOT_CERTIFIED",
            },
            "direct_sum_uniform_remainder": {
                "status": "CERTIFIED_EXACT_IFF",
                "identity": "||(direct_sum J_s-I-s direct_sum G)/s||=sup_k ||J_(s,k)-I-sG_k||/abs(s)",
                "uniform_o_s_iff": "sup_k epsilon_k(s)->0",
                "pointwise_model": "epsilon_k(1/N)=min(1,k/N)",
                "rows": remainder_rows,
                "each_fixed_branch_converges": True,
                "global_uniform_remainder": False,
                "actual_anisotropic_uniform_remainder": "NOT_CERTIFIED",
            },
            "material_trace_join": {
                "status": "CERTIFIED_EXACT_TYPED_INTERFACE",
                "persistent_requirement": "direct-sum uniform remainder",
                "topology_requirement": "Gamma:X->ell1(face/side tags) bounded",
                "disjoint_tags_prevent_cross_cancellation": True,
                "clock_and_cemetery_remain_separate": True,
                "actual_join": "NOT_CERTIFIED",
            },
            "stopped_generating_function": {
                "status": "CERTIFIED_EXACT_POSITIVE_SCALAR_CRITERION",
                "iterate_bound": "||D(T^n)||<=n M^(n-1)L",
                "depth_ledger": "L P'(M)=L sum_n p_n n M^(n-1)",
                "positive_tagged_scalar_iff": True,
                "general_operator_role": "sharp norm-majorant route",
                "separator_law": "p_n=1/[n(n+1)]",
                "closed_form_for_0_lt_M_lt_1": "P'(M)=(-log(1-M)-M)/M^2",
                "finite_for_M_lt_1": True,
                "diverges_at_M_eq_1": True,
                "rows": depth_rows,
                "actual_weak_graph_TV_norm": "1",
                "actual_common_strong_M_lt_1": "NOT_CERTIFIED",
            },
            "minimal_physical_registry": {
                "immutable_key": "PARTIAL_FIXED_DEPTH",
                "all_depth_finite_s_incidence_atlas": "NOT_CERTIFIED",
                "uniform_J_and_inverse": "NOT_CERTIFIED",
                "two_sided_weighted_trace_Gamma": "NOT_CERTIFIED",
                "anisotropic_generators": "NOT_CERTIFIED",
                "uniform_supremum_remainder": "NOT_CERTIFIED",
                "differentiable_Rhat_Phat_Qhat": "NOT_CERTIFIED",
                "clock_face_one_shot_cemetery_sums": "NOT_CERTIFIED",
                "same_law_P_prime_or_positive_potential": "NOT_CERTIFIED",
                "physical_MT_DQ": "NOT_CERTIFIED",
            },
            "strict_status": "NOT_CERTIFIED",
        },
        "latest_same_type_technology_audit": {
            "checked_on": "2026-07-21",
            "arxiv_2603_19509v3": "assumes common strong spaces, differentiability and memory loss; expanding/noisy applications",
            "arxiv_2604_19671v2": "fixed billiard with changing hole and already regular standard families",
            "arxiv_2604_25746v1": "smooth compact boundaryless hyperbolic flows",
            "arxiv_2606_10155v1": "anisotropic billiard-space review",
            "butler_park_1909_11548v2": "defines canonical class-H holonomies but supplies no unpaid transfer invariance",
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
    models = g1["relative_shear_transfer"]["models"]
    require(models[0]["is_identity"] is True, "identity transfer")
    require(models[1]["matrix"] == [["4/3", "1/2"], ["0", "3/4"]], "mismatch transfer")
    require(models[1]["determinant"] == "1", "mismatch determinant")
    corrections = g1["selected_loop_transport"]["models"]
    require(corrections[0]["vanishes"] is True and corrections[1]["vanishes"] is False,
            "loop corrections")
    g3 = result["gate3"]
    require(g3["direct_sum_uniform_remainder"]["rows"][-1] == {
        "N": 64, "s": "1/64", "fixed_branch_k_1_remainder": "1/64",
        "global_supremum": "1",
    }, "uniform remainder final row")
    require(g3["stopped_generating_function"]["rows"][0] == {
        "cutoff": 1, "P_prime_at_1_partial": "1/2", "P_prime_at_half_partial": "1/2",
    }, "depth first row")
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
        print(f"ROUND66_GATE13_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("Gate1: NOT_CERTIFIED")
    print("Gate3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
