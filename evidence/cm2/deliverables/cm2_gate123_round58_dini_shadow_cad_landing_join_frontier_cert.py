#!/usr/bin/env python3
"""CM2 Round-58 Gate-1/2/3 structural-frontier certificate.

This append-only certificate is deliberately fail-closed.  It verifies:

* a uniform Dini/Cauchy interface for the two weighted projective critical
  sequences and an exact twisting-robustness radius in one frozen eigenbasis;
* a projected-singularity-shadow criterion for an infinite stable-plaque
  carrier, plus the exact Gate-2 -> Gate-4 landing-redistribution type split;
* an explicit CAD recurrence bounding every fixed-depth circular-billiard
  atlas, and a sharp reason the installed exponential clock moment does not
  integrate that depth-dependent majorant or a directional Piola norm.

No missing physical hypothesis is synthesized.  Positive replay modes exit
0; default mode exits 2 because Gates 1, 2, 3 and CM2 remain uncertified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "deliverables" / (
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-"
    "manifest-2026-07-20.json"
)
Q = Fraction

DEPENDENCIES = {
    "deliverables/cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-assault-2026-07-20.md":
        "7d012a962eb98f1b35fc988b9d011133148e874ff0dd0f6c3d8b5e8d64337207",
    "deliverables/cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-manifest-2026-07-20.json":
        "58bcb86cac43534a69604553cff6e46d92803af8d098a9b2e585333942b64d9f",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-assault-2026-07-16.md":
        "35f0632a29c93b639120cdffe5720b5d4ba282b02b3a247b476fcfb8f1ab4925",
    "deliverables/cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate4-round57-unshifted-first-return-frontier-assault-2026-07-20.md":
        "a575bd78271a6581c232c3f37354dec75d3b3d73b9bf61474a2f6fbdae0d6fe3",
    "deliverables/cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-assault-2026-07-20.md":
        "b273290628c966465a3d0133661cfa511f7ec1ef18e98ee105b0f86bc7a2a0bc",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def qtext(value: Q) -> str:
    return str(value)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_dependencies() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel, expected in DEPENDENCIES.items():
        path = ROOT / rel
        require(not path.is_symlink(), f"symlink dependency rejected: {rel}")
        require(path.is_file(), f"missing dependency: {rel}")
        require(sha256_path(path) == expected, f"dependency hash drift: {rel}")
        rows.append({"path": rel, "sha256": expected})
    return rows


def gate1_replay() -> dict[str, Any]:
    # Exact geometric Dini model: C_n=1-2^-n, n>=0.  Its successive
    # increments have summable majorant eta_n=2^-(n+1), and the exact tail
    # after N is 2^-N.
    critical = [Q(1) - Q(1, 2) ** n for n in range(10)]
    increments = [critical[n + 1] - critical[n] for n in range(9)]
    require(increments == [Q(1, 2) ** (n + 1) for n in range(9)],
            "Gate1 Dini increment replay")
    tails = [Q(1, 2) ** n for n in range(10)]
    require(all(abs(Q(1) - critical[n]) == tails[n] for n in range(10)),
            "Gate1 Dini tail replay")

    # Vanishing increments alone are not a convergence theorem.  The
    # infinite triangular construction rises from 0 to 1 in m steps of 1/m
    # and falls to 0 in m steps; its increments tend to zero, but it visits
    # both endpoints for every m.
    triangular: list[Q] = [Q(0)]
    endpoint_rows: list[dict[str, Any]] = []
    for m in range(2, 8):
        for k in range(1, m + 1):
            triangular.append(Q(k, m))
        high_index = len(triangular) - 1
        for k in range(1, m + 1):
            triangular.append(Q(m - k, m))
        endpoint_rows.append({
            "block": m,
            "step_absolute": qtext(Q(1, m)),
            "high_value": qtext(triangular[high_index]),
            "terminal_value": qtext(triangular[-1]),
        })
    require(all(row["high_value"] == "1" and row["terminal_value"] == "0"
                for row in endpoint_rows), "Gate1 triangular endpoints")
    require([row["step_absolute"] for row in endpoint_rows]
            == [qtext(Q(1, m)) for m in range(2, 8)],
            "Gate1 triangular vanishing steps")

    # Frozen selected-loop wedge lower margins, rounded strictly inward from
    # the interval-certified values.  In the same normalized QNL eigenbasis,
    # each axis wedge is one signed matrix entry, hence max-entry perturbation
    # delta changes it by at most delta.
    margins = {
        "wedge_e1_psi_e1": Q(10) ** 77,
        "wedge_e2_psi_e1": Q(700),
        "wedge_e1_psi_e2": Q(10) ** 47,
        "wedge_e2_psi_e2": Q(1, 10**28),
    }
    delta = Q(1, 10**29)
    require(all(margin > delta for margin in margins.values()),
            "Gate1 twisting robustness radius")

    return {
        "weighted_projective_critical_dini_theorem": {
            "critical_sequences": [
                "C_n^+=(diagonal/projective weight)*(p_y,n-p_x,n)",
                "C_n^-=(diagonal/projective weight)*(q_y,n-q_x,n)",
            ],
            "hypothesis": (
                "abs(C_0^sigma)<=H_0*d(x,y)^beta and sup_plaque "
                "abs(C_(n+1)^sigma-C_n^sigma)"
                "<=eta_n*d(x,y)^beta for sigma in {+,-}, sum eta_n<infinity"
            ),
            "conclusion": (
                "both critical sequences converge uniformly with Holder tail "
                "d(x,y)^beta*sum_(k>=N)eta_k and limit modulus "
                "(H_0+sum eta_n)*d(x,y)^beta"
            ),
            "exact_sample_C_n": [qtext(value) for value in critical],
            "exact_sample_increments": [qtext(value) for value in increments],
            "exact_sample_tails": [qtext(value) for value in tails],
            "status": "CERTIFIED_CONDITIONAL_INTERFACE",
        },
        "vanishing_increment_separator": {
            "construction": (
                "block m rises 0->1 in m steps of 1/m and falls 1->0 "
                "in m steps of 1/m"
            ),
            "finite_replay_rows": endpoint_rows,
            "increments_tend_to_zero": True,
            "converges": False,
            "conclusion": "vanishing_increment_without_Dini_summability_is_insufficient",
        },
        "same_fibre_twisting_robustness": {
            "required_comparison": (
                "same physical QNL fibre and same normalized eigenbasis; "
                "max-entry loop error <=delta"
            ),
            "strict_inward_wedge_margins": {
                key: qtext(value) for key, value in margins.items()
            },
            "certified_delta": qtext(delta),
            "four_wedges_remain_nonzero": True,
            "physical_combined_gauge_loop_error_bound": "NOT_CERTIFIED",
        },
    }


def gate2_replay() -> dict[str, Any]:
    # Projected shadow criterion on a normalized base interval.  These are
    # shadows in the base coordinate, not 2D singular-set areas.
    shadows = [Q(1, 2) ** (j + 2) for j in range(8)]
    partial = sum(shadows, Q(0))
    full = Q(1, 2)
    tail = full - partial
    require(partial == Q(255, 512) and tail == Q(1, 512),
            "Gate2 projected-shadow arithmetic")
    require(Q(1) - full == Q(1, 2), "Gate2 survivor lower bound")

    # Exact landing support obstruction from Round 57.
    c_p = Q(4 * 10**90 * 360493663, 358863)
    ell = Q(1, 1) / (2 * c_p)
    physical_z = Q(1, 1) / ell
    quotient_z = Q(1)
    require(physical_z == 2 * c_p > c_p, "Gate2->4 physical support lower bound")
    require(quotient_z < c_p, "Gate2->4 latent quotient properness")

    return {
        "projected_singularity_shadow_theorem": {
            "candidate_fibres": "W_u over a reference base interval I",
            "bad_shadow": (
                "B_j={u in I: W_u meets the depth-j singularity or "
                "the depth-j graph transform is undefined}"
            ),
            "hypotheses": [
                "every bad shadow B_j is Borel",
                "Leb(B_j)<=b_j and sum_j b_j<|I|",
                "surviving finite graph transforms have a common cone/contraction/C1 compactness bound",
            ],
            "conclusion": (
                "base measure of all-depth surviving plaques is at least "
                "|I|-sum_j b_j, and the graph-transform limit supplies stable plaques"
            ),
            "exact_sample_first_eight_b_j": [qtext(value) for value in shadows],
            "exact_sample_first_eight_sum": qtext(partial),
            "exact_sample_infinite_sum": qtext(full),
            "exact_sample_survivor_lower": qtext(Q(1) - full),
            "status": "CERTIFIED_CONDITIONAL_INTERFACE",
        },
        "area_vs_shadow_separator": {
            "singular_set": "the line v=0 in the affine cone-product tile",
            "two_dimensional_area": "0",
            "projected_bad_shadow": "the entire base I",
            "conclusion": "area_nullity_does_not_control_spanning_plaque_loss",
        },
        "gate2_to_gate4_landing_join": {
            "actual_C_p": qtext(c_p),
            "isolated_physical_support_length": qtext(ell),
            "physical_same_support_Z_per_mass": qtext(physical_z),
            "reference_interval_Z_per_mass": qtext(quotient_z),
            "same_point_positive_redisintegration_can_be_proper": False,
            "stable_projection_to_reference_can_be_proper": True,
            "stable_projection_preserves_physical_landing_point": False,
            "projection_only_result": "proper_latent_graph_lift_with_endpoint_map",
            "shortest_sufficient_physical_interface": [
                "countable physical product-rectangle cover of the landing support",
                "immutable stable projection and two-sided Borel holonomy Jacobian bounds",
                "common landing restriction full-span or uniformly bounded fragmentation on physical unstable plaques",
                "same-measure Rokhlin unstable conditionals with density and log-distortion bounds",
                "average boundary charge sum p_W/|W| strictly below C_p",
                "Borel branch inverse retaining n/path/same-ID and half-open ownership",
                "strong restriction and assembly bounds for the resulting physical carrier",
            ],
            "status": "CONDITIONAL_JOIN_ONLY",
        },
    }


def cad_prefix(depth: int, steps: int = 3) -> dict[str, Any]:
    require(depth >= 1 and steps >= 1, "CAD arguments")
    variables = 400 * depth + 20
    polynomials = 2000 * depth + 100
    degree = 8
    s_value, d_value = polynomials, degree
    rows: list[dict[str, str | int]] = []
    cell_prefix = 1
    for projection_step in range(steps):
        stack_factor = 2 * s_value * d_value + 1
        cell_prefix *= stack_factor
        rows.append({
            "projection_step": projection_step,
            "polynomial_count_majorant": str(s_value),
            "degree_majorant": str(d_value),
            "stack_factor": str(stack_factor),
            "cell_product_prefix": str(cell_prefix),
        })
        s_value = 2 * (s_value * d_value + 1) ** 2
        d_value = 2 * d_value**2
    return {
        "depth": depth,
        "ambient_auxiliary_variables_k_n": variables,
        "initial_polynomial_count_s_n": polynomials,
        "initial_degree_d": degree,
        "first_projection_rows": rows,
    }


def gate3_replay() -> dict[str, Any]:
    word_counts = {str(n): 8 * 162**n for n in range(1, 6)}
    require(word_counts == {
        "1": 1296,
        "2": 209952,
        "3": 34012224,
        "4": 5509980288,
        "5": 892616806656,
    }, "Gate3 branch-word counts")
    cad_rows = [cad_prefix(depth) for depth in (1, 2, 3)]

    # An exponential clock moment does not pay a superexponential complexity
    # majorant.  For p_d=2^-d, d>=1, sum p_d=1 and, since exp(1/6)<3/2,
    # sum p_d exp(d/6) <= sum (3/4)^d=3.  But p_d*d^d=(d/2)^d does not tend
    # to zero.  This is a nonimplication, not a lower bound on actual atlas
    # complexity.
    weighted_super = [Q(d, 2) ** d for d in range(1, 9)]
    require(weighted_super[-1] == Q(65536), "Gate3 superexponential separator")
    exponential_majorant_sum = sum((Q(3, 4) ** d for d in range(1, 80)), Q(0))
    require(exponential_majorant_sum < Q(3), "Gate3 exponential partial sum")

    # Determinant one does not control directional Piola amplification.
    piola_rows = []
    for n in range(1, 9):
        length = 2**n
        determinant = Q(length) * Q(1, length)
        require(determinant == 1, "Gate3 determinant replay")
        piola_rows.append({
            "n": n,
            "S_n": f"diag({length},1/{length})",
            "determinant": "1",
            "norm_of_S_n_e1": str(length),
        })

    return {
        "explicit_fixed_depth_cad_majorant": {
            "encoding_budget": {
                "auxiliary_variables_k_n": "400*n+20",
                "polynomial_count_s_n": "2000*n+100",
                "degree": 8,
                "branch_words": "8*162^n",
            },
            "cad_recurrence": {
                "S_(r+1)": "2*(S_r*D_r+1)^2",
                "D_(r+1)": "2*D_r^2",
                "lift_stack_factor": "2*S_r*D_r+1",
                "projection_steps": "k_n",
                "total_component_majorant": (
                    "8*162^n times product_(r=0)^(k_n-1)(2*S_r*D_r+1)"
                ),
            },
            "fixed_depth_branch_word_universe": word_counts,
            "exact_first_projection_replays": cad_rows,
            "projection_component_rule": (
                "a continuous coordinate projection cannot split a connected component"
            ),
            "budget_scope": (
                "conditional on an explicit branch formula fitting the declared "
                "k_n,s_n,degree envelope; physical formula enumeration is not claimed"
            ),
            "status": "CERTIFIED_FOR_DECLARED_ENCODING_BUDGET",
        },
        "unbounded_depth_moment_separator": {
            "law": "p_d=2^-d for d>=1",
            "total_mass": "1",
            "exp_d_over_6_moment_upper_using_exp_1_over_6_lt_3_over_2": "3",
            "superexponential_test": "G(d)=d^d",
            "p_d_G_d_first_eight": [qtext(value) for value in weighted_super],
            "superexponential_integral_finite": False,
            "scope": (
                "the installed exponential Dbar moment alone cannot integrate "
                "the CAD majorant; no lower bound on actual component growth is claimed"
            ),
        },
        "directional_piola_separator": {
            "maps": "S_n=diag(2^n,2^-n)",
            "current_direction": "K=e1",
            "rows": piola_rows,
            "conclusion": "determinant_one_does_not_bound_directional_current_amplification",
        },
    }


def build_manifest(check_dependencies: bool = True) -> dict[str, Any]:
    dependencies = validate_dependencies() if check_dependencies else [
        {"path": rel, "sha256": sha} for rel, sha in DEPENDENCIES.items()
    ]
    return {
        "artifact": "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier",
        "date": "2026-07-20",
        "dependencies": dependencies,
        "result": {
            "gate1": {
                **gate1_replay(),
                "physical_weighted_projective_defect_convergence": "NOT_CERTIFIED",
                "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
                "official_status": "NOT_CERTIFIED",
            },
            "gate2": {
                **gate2_replay(),
                "physical_projected_shadow_rows": 0,
                "physical_stable_saturated_base_projection_holonomy": "NOT_CERTIFIED",
                "official_immutable_fields": "0/17",
                "official_status": "NOT_CERTIFIED",
            },
            "gate3": {
                **gate3_replay(),
                "physical_formula_budget_instantiation": "NOT_CERTIFIED",
                "strong_physical_R_s_Q_s": "NOT_CERTIFIED",
                "directional_Piola_suffix_bound": "NOT_CERTIFIED",
                "MT_DQ": "NOT_CERTIFIED",
                "official_status": "NOT_CERTIFIED",
            },
            "technology_recheck": {
                "checked_utc": "2026-07-20T11:45:20Z",
                "official_arxiv_api_queries": {
                    "billiard_holonomy_young_tower": {
                        "response_sha256": "52a696a784ac85a2d61fb5b35b2300aa4658d2245460fa08c28fac6c79d84067",
                        "latest_relevant": "2509.07657v2",
                    },
                    "cocycle_holonomy_twisting_cohomology": {
                        "response_sha256": "3349f389ad2b540e6a7edb309677334d81a90999d50cbf1b4b3ab160801e17a2",
                        "latest_relevant": "2604.13401v1",
                    },
                    "billiard_transfer_perturbation": {
                        "response_sha256": "e8c5429717c3522177ca15b601a2d66e0a91c64efd6092a41a4063ac4cc4d99f",
                        "latest_relevant": "2606.10155v1",
                    },
                },
                "demers_liverani_2606_10155v1_pdf_sha256":
                    "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798",
                "new_direct_CM2_carrier_closure_found": False,
            },
        },
        "schema": "cm2.gate123.round58.dini-shadow-cad-landing-join-frontier.v1",
        "strict_verdict": {
            "gate1": "NOT_CERTIFIED",
            "gate2": "NOT_CERTIFIED",
            "gate3": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "overall": "NO-GO_FOR_CLAIM",
        },
    }


def encoded_manifest(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def strict_load(path: Path) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in rows:
            require(key not in out, f"duplicate JSON key: {key}")
            out[key] = value
        return out

    def nonfinite(token: str) -> None:
        raise CertificateError(f"non-finite JSON token: {token}")

    data = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_constant=nonfinite,
    )
    require(isinstance(data, dict), "manifest root is not an object")
    return data


def replay() -> dict[str, Any]:
    expected = build_manifest(check_dependencies=True)
    observed = strict_load(MANIFEST)
    require(observed == expected, "manifest semantic drift")
    require(MANIFEST.read_text(encoding="utf-8") == encoded_manifest(expected),
            "manifest byte-model drift")
    return {
        "dependencies": len(expected["dependencies"]),
        "gate1_dini_rows": len(expected["result"]["gate1"]
                               ["weighted_projective_critical_dini_theorem"]
                               ["exact_sample_C_n"]),
        "gate2_shadow_rows": len(expected["result"]["gate2"]
                                 ["projected_singularity_shadow_theorem"]
                                 ["exact_sample_first_eight_b_j"]),
        "gate3_cad_depth_rows": len(expected["result"]["gate3"]
                                   ["explicit_fixed_depth_cad_majorant"]
                                   ["exact_first_projection_replays"]),
        "overall": expected["strict_verdict"]["overall"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        if args.reemit is not None:
            args.reemit.write_text(encoded_manifest(build_manifest()), encoding="utf-8")
            print(f"REEMIT: {args.reemit}")
            return 0
        result = replay()
    except (OSError, ValueError, KeyError, TypeError, CertificateError) as exc:
        print(f"ROUND58_GATE123_CERT_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.summary or args.replay:
        print(json.dumps(result, sort_keys=True))
        print("ROUND58_GATE123_FRONTIER_REPLAY: PASS")
        return 0

    print("GATE1_WEIGHTED_PROJECTIVE_DINI_INTERFACE: CERTIFIED_CONDITIONAL")
    print("GATE2_PROJECTED_SHADOW_INTERFACE: CERTIFIED_CONDITIONAL")
    print("GATE3_FIXED_DEPTH_CAD_MAJORANT: CERTIFIED_FOR_DECLARED_ENCODING_BUDGET")
    print("GATE1_GATE2_GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
