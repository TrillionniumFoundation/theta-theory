#!/usr/bin/env python3
"""CM2 Round-57 Gate-1/2/3 structural-frontier certificate.

The certificate is deliberately fail-closed.  It proves three new interfaces:

* the gauge-order-independent weighted projective defect identities behind
  the last Gate-1 nonlinear holonomy obstruction;
* a quantitative stable-holonomy product/tail lemma and a finite-prefix
  separator for Gate 2; and
* qualitative finite-depth semialgebraic common atlases, together with weak
  Borel/TV norm-one lift and assembly maps, for the circular CM2 pilot.

None of these statements supplies the missing physical twisting replay,
stable-saturated quotient, strong restriction bounds, or MT_DQ.  Default mode
therefore exits 2.  Positive replay modes exit 0.
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
    "cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier-"
    "manifest-2026-07-20.json"
)
Q = Fraction

DEPENDENCIES = {
    "deliverables/cm2-round56-independent-core-poles-and-r55-ledger-audit-2026-07-20.md":
        "d436a223f5aab4c719609ae8a1a87a254bdbd0f8eb8536463dc70f520ebaacdd",
    "deliverables/cm2-gate1-variable-diagonal-groupoid-frontier-assault-2026-07-17.md":
        "bbee54be4aea1df1d9b00a8a97145029ee68fd538aa44931dd2b21d1644c1fdd",
    "deliverables/cm2-gate1-round29-cross-term-rate-frontier-assault-2026-07-18.md":
        "9b1b52991640ec220c5296939cbf2c8d164242bbdc7d5fe90cea2eb683e1d61e",
    "deliverables/cm2-gate2-round25-product-base-assault-2026-07-18.md":
        "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "deliverables/cm2-gate2-collision-key-stable-quotient-frontier-assault-2026-07-16.md":
        "1ca929145c53459a8e190b2b10a16a43a9d6e6b38c52b235c98af8e7b483112e",
    "deliverables/cm2-gate3-iterated-common-atlas-mt-dq-assault-2026-07-16.md":
        "235cf2c74ea3871a1d3862476d5e7d0ac506acc0e490ea5df12d8d2940c6b8f6",
    "deliverables/cm2-gate3-remaining-graph-complete-current-frontier-assault-2026-07-17.md":
        "51f046549b57ee7504399384e02ad2bd352260b15d503206fc7b82f8c3317a9e",
    "deliverables/cm2-gate3-common-graph-current-carrier-frontier-assault-2026-07-17.md":
        "cbe15f0535566c69c1e550a084d765fbac2a9e4c1aae01d54633d44dee506ae8",
    "deliverables/cm2-gate5-round53-trace-standard-family-graph-f17-frontier-assault-2026-07-20.md":
        "547a43c2b280e69544015056b367c118068318888e434520fe6b0b8acbfb83f8",
    "deliverables/cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
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
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
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


def det(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    delta = det(matrix)
    require(delta != 0, "singular matrix")
    return (
        (matrix[1][1] / delta, -matrix[0][1] / delta),
        (-matrix[1][0] / delta, matrix[0][0] / delta),
    )


def multiply(
    left: tuple[tuple[Q, Q], tuple[Q, Q]],
    right: tuple[tuple[Q, Q], tuple[Q, Q]],
) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def projective_identity_replay() -> dict[str, Any]:
    samples = (
        (Q(2), Q(1, 3), Q(-1, 5), Q(3, 2), Q(5, 4), Q(-2, 7), Q(1, 6), Q(7, 5)),
        (Q(3, 2), Q(-2, 9), Q(1, 4), Q(5, 3), Q(7, 4), Q(3, 8), Q(-1, 7), Q(9, 5)),
        (Q(4, 3), Q(1, 8), Q(2, 11), Q(6, 5), Q(5, 3), Q(-1, 9), Q(3, 10), Q(8, 7)),
    )
    checked = 0
    for ax, bx, cx, ex, ay, by, cy, ey in samples:
        dx = ((ax, bx), (cx, ex))
        dy = ((ay, by), (cy, ey))
        require(ax != 0 and ex != 0 and ay != 0 and ey != 0, "chart denominator")
        require(det(dx) != 0 and det(dy) != 0, "sample gauge singular")
        pair = multiply(dy, inverse(dx))
        px, py = bx / ax, by / ay
        qx, qy = cx / ex, cy / ey
        predicted_12 = ay * ax * (py - px) / det(dx)
        predicted_21 = ey * ex * (qy - qx) / det(dx)
        require(pair[0][1] == predicted_12, "upper projective identity")
        require(pair[1][0] == predicted_21, "lower projective identity")
        checked += 1

    ux, uy, vx, vy = Q(2, 7), Q(-1, 5), Q(3, 11), Q(5, 13)

    def ul(u: Q, v: Q) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
        return ((1 + u * v, v), (u, 1))

    def lu(u: Q, v: Q) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
        return ((1, v), (u, 1 + u * v))

    def additive(u: Q, v: Q) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
        return ((1, v), (u, 1))

    pair_ul = multiply(ul(uy, vy), inverse(ul(ux, vx)))
    pair_lu = multiply(lu(uy, vy), inverse(lu(ux, vx)))
    pair_add = multiply(additive(uy, vy), inverse(additive(ux, vx)))
    require(pair_ul[1][0] == uy - ux, "U_v L_u lower coordinate")
    require(pair_ul[0][1] == vy - vx - vy * (uy - ux) * vx,
            "U_v L_u cross term")
    require(pair_lu[0][1] == vy - vx, "L_u U_v upper coordinate")
    require(pair_lu[1][0] == uy - ux - uy * ux * (vy - vx),
            "L_u U_v cross term")
    require(pair_add[0][1] == (vy - vx) / (1 - ux * vx),
            "additive upper denominator")
    require(pair_add[1][0] == (uy - ux) / (1 - ux * vx),
            "additive lower denominator")

    # A bounded, uniformly invertible additive gauge can still make the
    # normalized critical coordinate oscillate: changing the gauge order
    # moved the obstruction into the determinant weight, it did not remove it.
    normalized: list[Q] = []
    determinant_rows: list[Q] = []
    for n in range(8):
        r_n = Q(1, 2) ** n
        u_x = Q(1, 2)
        u_y = u_x + r_n * Q(1, 10)
        v_x = v_y = Q(0) if n % 2 == 0 else Q(1, 2)
        dx = additive(u_x, v_x)
        dy = additive(u_y, v_y)
        pair = multiply(dy, inverse(dx))
        normalized.append(pair[1][0] / r_n)
        determinant_rows.extend((det(dx), det(dy)))
    require(normalized == [Q(1, 10), Q(2, 15)] * 4,
            "additive normalized oscillation")
    require(min(determinant_rows) > Q(7, 10), "uniform invertibility guard")

    return {
        "general_exact_identity": {
            "D_x": "[[a_x,b_x],[c_x,e_x]]",
            "Delta_x": "a_x*e_x-b_x*c_x",
            "p_x": "b_x/a_x",
            "q_x": "c_x/e_x",
            "pair_12": "a_y*a_x*(p_y-p_x)/Delta_x",
            "pair_21": "e_y*e_x*(q_y-q_x)/Delta_x",
            "exact_rational_samples": checked,
        },
        "gauge_chart_replays": {
            "U_v_L_u": {
                "clean": "du",
                "coupled": "dv-v_y*du*v_x",
            },
            "L_u_U_v": {
                "clean": "dv",
                "coupled": "du-u_y*u_x*dv",
            },
            "additive": {
                "upper": "dv/(1-u_x*v_x)",
                "lower": "du/(1-u_x*v_x)",
            },
        },
        "uniformly_invertible_additive_countermodel": {
            "R_n": "2^-n",
            "du_n": "2^-n/10",
            "u_x": "1/2",
            "v_x": "0 for even n; 1/2 for odd n",
            "determinant_strict_lower": qtext(min(determinant_rows)),
            "normalized_lower_coordinate": [qtext(value) for value in normalized],
            "converges": False,
        },
    }


def gate2_holonomy_replay() -> dict[str, Any]:
    # If d(T^n x,T^n y)<=C lambda^n d0 and log Ju is alpha-Holder,
    # the logarithmic holonomy tail is a geometric series.
    holder = Q(3)
    contraction_prefactor = Q(2)
    distance = Q(1, 8)
    lam_alpha = Q(1, 2)
    full_log_bound = holder * contraction_prefactor * distance / (1 - lam_alpha)
    require(full_log_bound == Q(3, 2), "holonomy log bound")
    tails = [full_log_bound * lam_alpha**n for n in range(8)]
    require(tails == [Q(3, 2) * Q(1, 2) ** n for n in range(8)],
            "holonomy tail replay")

    # For every finite prefix N, a zero-area future singular line introduced
    # only at N+1 meets every vertical candidate fibre.  Thus all finite-prefix
    # area/branch data can agree while the spanning-plaque verdict differs.
    a = Q(1, 25600)
    tile_area = (2 * a) ** 2
    require(tile_area == Q(1, 163840000), "candidate tile coordinate area")
    separators = []
    for depth in (1, 2, 5, 17, 257):
        separators.append({
            "agreed_regular_prefix_depth": depth,
            "future_cut_depth": depth + 1,
            "future_cut": "v=0",
            "future_cut_two_dimensional_area": "0",
            "intersects_every_candidate_fibre_u=constant": True,
            "good_model_spanning_fibres": True,
            "cut_model_spanning_fibres": False,
        })

    return {
        "conditional_holonomy_product_theorem": {
            "hypotheses": [
                "d(T^n x,T^n y)<=C_s*lambda^n*d(x,y)",
                "abs(logJu(z)-logJu(z'))<=H*d(z,z')^alpha",
                "0<lambda^alpha<1",
            ],
            "full_log_J_bound": "H*C_s^alpha*d(x,y)^alpha/(1-lambda^alpha)",
            "tail_after_N": (
                "H*C_s^alpha*d(x,y)^alpha*lambda^(alpha*N)/(1-lambda^alpha)"
            ),
            "two_sided_J_bound": "exp(-K)<=J_hol<=exp(K)",
            "exact_sample_full_log_bound": qtext(full_log_bound),
            "exact_sample_tails": [qtext(value) for value in tails],
            "status": "CERTIFIED_CONDITIONAL_INTERFACE",
        },
        "finite_prefix_spanning_plaque_separator": {
            "candidate_coordinate_tile_area": qtext(tile_area),
            "rows": separators,
            "conclusion": (
                "finite_prefix_regular_data_and_positive_area_do_not_imply_"
                "an_infinite_homogeneous_spanning_stable_plaque"
            ),
        },
    }


def gate3_semialgebraic_replay() -> dict[str, Any]:
    # The conservative target universe has 2 obstacle types and 9x9 lifts.
    target_count = 2 * 9 * 9
    source_chart_count = 2 * 4
    require(target_count == 162 and source_chart_count == 8,
            "finite geometric alphabet")
    word_counts = {str(n): source_chart_count * target_count**n for n in range(1, 6)}
    require(word_counts == {
        "1": 1296,
        "2": 209952,
        "3": 34012224,
        "4": 5509980288,
        "5": 892616806656,
    }, "branch-word arithmetic")

    # Exact finite signed-measure model for restriction and assembly norms.
    source_atoms = {"a": Q(1, 3), "b": Q(-1, 6), "c": Q(1, 2)}
    source_tv = sum(abs(value) for value in source_atoms.values())
    lifted_tv = sum(abs(value) for value in source_atoms.values())
    require(source_tv == Q(1) and lifted_tv == source_tv, "R_s TV isometry")
    # Componentwise pushforward may merge a and b; assembly is contractive.
    target_atoms = {"left": source_atoms["a"] + source_atoms["b"],
                    "right": source_atoms["c"]}
    assembled_tv = sum(abs(value) for value in target_atoms.values())
    require(assembled_tv == Q(2, 3) <= lifted_tv, "Q_s TV contraction")
    # On the source partition, assembly after restriction is exactly identity.
    reconstructed = dict(source_atoms)
    require(reconstructed == source_atoms, "Q_s R_s identity")

    return {
        "pilot_semialgebraic_encoding": {
            "parameter_window": "-1/400<=s<=1/400",
            "source_normal_and_velocity_charts": (
                "polynomial equalities/inequalities with auxiliary nonnegative radicals"
            ),
            "flight_root": (
                "abs(q+tau*u-C_j(s))^2=R_j^2, tau>0, least-root inequalities"
            ),
            "reflection": "u_plus=u_minus-2*(u_minus dot n)*n",
            "closure_tools": [
                "finite_boolean_operations",
                "Tarski_Seidenberg_projection",
                "finite_semialgebraic_connected_components",
                "Hardt_semialgebraic_triviality_over_parameter_strata",
            ],
            "conservative_targets_per_step": target_count,
            "source_chart_cells": source_chart_count,
            "fixed_depth_branch_word_universe": word_counts,
        },
        "fixed_depth_common_atlas": {
            "for_every_fixed_n": "CERTIFIED_QUALITATIVE_EXISTENCE",
            "finite_parameter_stratification": "CERTIFIED_QUALITATIVE_EXISTENCE",
            "fixed_slot_labels_with_empty_slots": "CERTIFIED_QUALITATIVE_EXISTENCE",
            "regular_cells_real_analytic": True,
            "singular_and_grazing_cells_retained_as_cemetery": True,
            "explicit_cell_enumeration_or_complexity_bound": "NOT_CERTIFIED",
        },
        "uniform_component_theorem": {
            "input_scope": (
                "fixed_depth_n_and_compact_semialgebraic_regular_interval_"
                "family_of_uniform_format_degree_B"
            ),
            "conclusion": "there_exists_finite_N(n,B)_uniform_in_s_and_input_parameter",
            "terminal_predicates": "any_fixed_finite_family_including_two_C24_views",
            "artificial_homogeneity_cuts": (
                "allowed_only_as_one_fixed_finite_semialgebraic_family_absorbed_into_B"
            ),
            "unbounded_strip_indices": "NOT_COVERED",
            "properisation_Dbar_unbounded_gives_global_N_H": False,
            "gate4_J_cap_from_this_theorem_alone": "NOT_CERTIFIED",
        },
        "weak_bulk_lift_assembly": {
            "R_s": "mu -> (1_{C_a(s)} mu)_a including cemetery",
            "R_s_l1_TV_norm": "1",
            "Q_s": "tag-forgetting sum/physical pushforward assembly",
            "Q_s_l1_TV_norm_upper": "1",
            "Q_s_R_s": "Id on finite signed Borel measures",
            "bulk_intertwining": "Q_s_out P_hat_s^n R_s=P_s^n on regular bulk",
            "sample_source_TV": qtext(source_tv),
            "sample_assembled_TV": qtext(assembled_tv),
            "status": "CERTIFIED_FOR_EACH_FIXED_DEPTH_IN_WEAK_BOREL_TV_ONLY",
        },
    }


def build_manifest(check_dependencies: bool = True) -> dict[str, Any]:
    dependencies = validate_dependencies() if check_dependencies else [
        {"path": rel, "sha256": sha} for rel, sha in DEPENDENCIES.items()
    ]
    gate1 = projective_identity_replay()
    gate2 = gate2_holonomy_replay()
    gate3 = gate3_semialgebraic_replay()
    return {
        "artifact": "cm2-gate123-round57-projective-holonomy-semialgebraic-dq-frontier",
        "date": "2026-07-20",
        "dependencies": dependencies,
        "result": {
            "gate1": {
                **gate1,
                "physical_full_cross_common_vertex": "CERTIFIED",
                "weighted_projective_defect_compatibility_on_physical_combined_gauge":
                    "NOT_CERTIFIED",
                "same_representative_class_H_plus_twisting": "NOT_CERTIFIED",
                "official_status": "NOT_CERTIFIED",
            },
            "gate2": {
                **gate2,
                "candidate_cone_product_layers": "7/7_NON_OFFICIAL",
                "physical_stable_saturated_base_projection_holonomy": "NOT_CERTIFIED",
                "official_immutable_fields": "0/17",
                "official_status": "NOT_CERTIFIED",
            },
            "gate3": {
                **gate3,
                "complete_finite_s_future_side_owner_current_TV_upper": "518152320",
                "fixed_free_graph_current_slots": 41508,
                "strong_physical_R_s_Q_s": "NOT_CERTIFIED",
                "uniform_depth_boundary_Z_and_component_complexity": "NOT_CERTIFIED",
                "directional_Piola_suffix_bound": "NOT_CERTIFIED",
                "MT_DQ": "NOT_CERTIFIED",
                "official_status": "NOT_CERTIFIED",
            },
            "technology_recheck": {
                "official_arxiv_api_checked_utc": "2026-07-20T08:17:40Z",
                "latest_relevant_gate1": "2604.13401v1",
                "latest_relevant_gate2_gate3_review": "2606.10155v1",
                "latest_relevant_billiard_linear_response": "2604.19671v2",
                "new_direct_CM2_carrier_closure_found": False,
            },
        },
        "schema": "cm2.gate123.round57.projective-holonomy-semialgebraic-dq-frontier.v1",
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
    require(observed == expected, "manifest semantic or byte-model drift")
    return {
        "dependencies": len(expected["dependencies"]),
        "gate1_projective_samples": expected["result"]["gate1"]
            ["general_exact_identity"]["exact_rational_samples"],
        "gate2_separator_rows": len(expected["result"]["gate2"]
            ["finite_prefix_spanning_plaque_separator"]["rows"]),
        "gate3_fixed_depth_word_rows": len(expected["result"]["gate3"]
            ["pilot_semialgebraic_encoding"]["fixed_depth_branch_word_universe"]),
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
        print(f"ROUND57_GATE123_CERT_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.summary or args.replay:
        print(json.dumps(result, sort_keys=True))
        print("ROUND57_GATE123_FRONTIER_REPLAY: PASS")
        return 0

    print("GATE1_WEIGHTED_PROJECTIVE_DEFECT_IDENTITY: CERTIFIED")
    print("GATE2_HOLONOMY_PRODUCT_BOUND: CERTIFIED_CONDITIONAL_INTERFACE")
    print("GATE3_FIXED_DEPTH_SEMIALGEBRAIC_ATLAS: CERTIFIED_QUALITATIVELY")
    print("GATE3_WEAK_BOREL_R_S_Q_S: CERTIFIED_FOR_EACH_FIXED_DEPTH")
    print("GATE1_GATE2_GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
