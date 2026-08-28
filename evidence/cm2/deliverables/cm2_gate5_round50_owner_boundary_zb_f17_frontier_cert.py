#!/usr/bin/env python3
"""Round-50 owner-aware boundary-Z_B and dynamic-F17 frontier.

This append-only layer performs four tasks left by Round 49.

* It turns the countable arbitrary-R_n path/face grammars into one global
  standard-Borel, owner-deduplicated *marked* trace kernel.  The resulting
  owner boundary-Z_B functional is measurable with values in [0,infinity].
  Finiteness is deliberately not inferred.
* It tests the positive boundary-Z_B route against the certified physical
  homogeneity expansion ledger.  The available full 2^B high-strip
  majorant diverges.  More generally the same majorant is finite exactly
  below exponent theta=1/2.
* It freezes the exact aggregate-Z_B resolvent that would follow from a
  genuinely contracting owner-Z_B recurrence and computes its sharp
  block-weight threshold.
* It proves an exact branch-adapted dynamic-test isometry for the F17 bulk
  current, then separates it from the still-missing branch-uniform physical
  C1/CM2 test embedding by an area-preserving diagonal countermodel.

No complete F10 or F17 field is promoted.  Gate-5 maturity stays 10/18.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_componentwise_global_growth_recovery_frontier_cert as growth_cert
import cm2_gate4_global_growth_distortion_frontier_cert as distortion_cert


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round50-owner-boundary-zb-f17-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
)

DEPENDENCIES = {
    "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json": (
        "1a53a0bac41f6c0d6f8155c69b67daf31337b5f13578af9fb9f497d16277d6ad"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py": (
        "90b7f7a9c0f02c19a80a9679ff393818318675c378ff4c1f139985ae23f069e1"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2_gate4_global_growth_distortion_frontier_cert.py": (
        "c6043e74b32722b05de365dfc81fe5ef10833170d9baca15802729b8fca829d6"
    ),
}

K0 = 6121
TRUE_COMPONENT_UPPER = 153
CENTRAL_INVERSE = Q(144000, 180337)
DENSITY_RATIO = Q(2000, 1999)
SURVIVAL_R = Q(111718729, 111718750)
BLOCK_DEPTH = 9148
FULL_ZB_EXPONENT = Q(1)
SOFT_EXPONENT_THRESHOLD = Q(1, 2)

F13_OVER_D1 = Q(3816937, 47112000)
X_OVER_D1 = Q(25, 151)
QUARTER_CDYN_THRESHOLD = Q(7961063, 7800000)
UNIT_CDYN_THRESHOLD = Q(43295063, 7800000)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def fraction_digest(value: Q) -> str:
    """Hash a huge exact fraction without decimal string materialization."""

    numerator = value.numerator.to_bytes(
        (value.numerator.bit_length() + 7) // 8, "big"
    )
    denominator = value.denominator.to_bytes(
        (value.denominator.bit_length() + 7) // 8, "big"
    )
    return hashlib.sha256(
        len(numerator).to_bytes(8, "big") + numerator + denominator
    ).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    if path.suffix != ".json":
        return {}
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def ceil_log2_integer(value: int) -> int:
    if value <= 0:
        raise ValueError("positive integer required")
    return (value - 1).bit_length()


def validate_dependencies() -> dict[str, Any]:
    for name in DEPENDENCIES:
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != DEPENDENCIES[name]:
            raise RuntimeError(f"dependency hash: {name}")

    prior = load(
        "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json"
    )["result"]
    route = prior["conditional_boundary_ZB_alternative"]
    if route["trace_multiplier"] != "10000/1999":
        raise RuntimeError("Round49 trace multiplier")
    if route["conditional_occurrence_ZB_coefficient"] != "1030000/1999":
        raise RuntimeError("Round49 ZB coefficient")
    if prior["strict_nonpromotion"]["F17_bulk_dynamic_test"] != "NOT_CERTIFIED":
        raise RuntimeError("Round49 F17 scope")
    if prior["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round49 maturity")

    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]
    face = f8["parameterized_connected_face_registry"]
    if face["each_parent_W_face_family_intersection_count"] != "0_or_1":
        raise RuntimeError("F8 root multiplicity")
    if face["connected_rank_assignment"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("F8 connected rank")
    if face["corner_or_simultaneous_root_policy"] != "cemetery":
        raise RuntimeError("F8 corner policy")

    path = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    universe = path["C24_full_dimensional_arbitrary_n_candidate_path_join"]
    if universe["path_universe_over_all_finite_n_is_countable"] is not True:
        raise RuntimeError("path countability")
    if universe["each_regular_collision_step_has_exactly_one_frozen_key_owner"] is not True:
        raise RuntimeError("path owner")
    if path["arbitrary_n_Rn_Qn_level_and_mass_schema"]["path_fibre_refinement"][
        "same_level_fibres_pairwise_disjoint_by_frozen_exact_key_ownership"
    ] is not True:
        raise RuntimeError("path disjointness")

    f13 = load(
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    )["result"]
    join = f13["five_face_F13_Borel_join"]
    if join["face_kind_count"] != 5:
        raise RuntimeError("five-face count")
    if join["all_five_physical_face_grammars_have_a_Borel_F13_payload"] is not True:
        raise RuntimeError("Borel face payload")
    if f13["same_ID_physical_F13_trace_charge"][
        "arbitrary_Rn_suffix_pushed_two_trace_TV_ledger"
    ] != "CERTIFIED":
        raise RuntimeError("F13 suffix ledger")

    block = load(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]
    aggregate = block["aggregate_canonical_Z_resolvent"]
    if aggregate["explicit_block_index_weight"] != "w_Z=(1+rho^(-1))/2":
        raise RuntimeError("aggregate weight")
    if aggregate["mass_factor_rho"] != "(111718729/111718750)^9148":
        raise RuntimeError("aggregate rho")

    summary = load(
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if summary["homogeneity_cutoff_k0"] != K0:
        raise RuntimeError("k0")
    if summary["true_continuity_component_upper"] != TRUE_COMPONENT_UPPER:
        raise RuntimeError("component count")
    if summary["global_high_strip_tail_strict_upper"] != "1/5":
        raise RuntimeError("high strip tail")

    replay = growth_cert.certify()
    weighted = replay["componentwise_weighted_growth_join"]
    if weighted["high_child_inverse_expansion_strict_upper"] != "4/k^2":
        raise RuntimeError("high-strip inverse")
    if weighted["high_child_multiplicity_upper_per_sign_and_rank"] != 153:
        raise RuntimeError("high-strip multiplicity")
    if weighted["central_inverse_expansion_strict_upper"] != qstr(CENTRAL_INVERSE):
        raise RuntimeError("central inverse")
    distortion = distortion_cert.certify()
    high_geometry = distortion["homogeneous_oriented_carrier_log_distortion"][
        "high_strip_geometry"
    ]
    if high_geometry["target_cosine_bounds"] != (
        "1/(2(k+1)^2)<c_1<k^-2"
    ):
        raise RuntimeError("high-strip target cosine")
    return {
        "round49": prior,
        "f8": f8,
        "path": path,
        "f13": f13,
        "block": block,
        "growth": replay,
        "distortion": distortion,
    }


def owner_aware_boundary_kernel() -> dict[str, Any]:
    face_rows = [
        "source_core_clipping_face",
        "intermediate_core_avoidance_preimage_face",
        "terminal_core_preimage_face",
        "collision_singularity_or_owner_change_face",
        "moving_occurrence_face",
    ]
    side_rows = []
    for kind in face_rows:
        for side in ("minus", "plus"):
            side_rows.append(
                {
                    "physical_face_kind": kind,
                    "side_label": side,
                    "connected_rank": 0,
                    "regular_root_multiplicity_on_one_parent_W": "0_or_1",
                }
            )
    return {
        "parameter_scope": "base parameter s=0",
        "global_index_space": (
            "the countable disjoint union over finite n, arbitrary-R_n path key, "
            "canonical component, parent-W id, time j<n, physical face kind, "
            "carrier/primitive key, connected-rank-0 and trace side"
        ),
        "index_space_is_standard_Borel": True,
        "candidate_representation_token": (
            "(restriction-id,time-j,physical-event-signature,primitive-key,"
            "connected-rank-0,side-label)"
        ),
        "physical_event_signature": (
            "(restriction-id,time-j,physical-face-kind,exact geometric event labels,side-label)"
        ),
        "active_regular_root_section": (
            "the Borel graph of the unique transverse rank-0 root on the parent W"
        ),
        "owner_rule": (
            "within one physical-event signature, retain the lexicographically least "
            "active primitive key; E_i^owner=E_i minus union_(h<i)E_h"
        ),
        "owner_sets_pairwise_disjoint": True,
        "owner_sets_cover_all_regular_active_representations": True,
        "different_physical_events_are_never_deduplicated": True,
        "corner_or_simultaneous_event_policy": "cemetery, before owner minimization",
        "artificial_chart_or_homogeneity_faces": (
            "assembled before absolute values and excluded from the physical owner kernel"
        ),
        "side_rows": side_rows,
        "side_rows_sha256": digest(side_rows),
        "owner_marked_trace_kernel": (
            "K_owner(y,A)=sum_i K_i(y,A intersect E_i^owner), a countable "
            "standard-Borel sigma-finite marked kernel"
        ),
        "owner_boundary_ZB_functional": (
            "Z_B^owner(G)=integral sum_(owned regular roots xi on W) "
            "2^B_inc(xi)/length_*(W) dlambda(W) in [0,infinity]"
        ),
        "extended_valued_functional_is_Borel": True,
        "finite_on_every_fixed_finite_regular_record": True,
        "finite_after_sum_over_all_depths": "NOT_CERTIFIED",
        "nonempty_component_coordinates_enumerated": False,
        "global_owner_deduplication_requires_finite_enumeration": False,
        "status": "CERTIFIED_GLOBAL_STANDARD_BOREL_OWNER_ZB_KERNEL_SCHEMA",
    }


def homogeneity_zb_majorant_frontier() -> dict[str, Any]:
    central_cp_inverse_upper = 2 * K0 * K0
    central_rank_upper = ceil_log2_integer(central_cp_inverse_upper)
    if central_cp_inverse_upper != 74933282 or central_rank_upper != 27:
        raise RuntimeError("central rank")
    central_full_weight = DENSITY_RATIO * CENTRAL_INVERSE * (1 << central_rank_upper)
    if central_full_weight != Q(38654705664000000, 360493663):
        raise RuntimeError("central weighted coefficient")

    shell_rows = []
    for k in (K0, 8192, 16384, 32768):
        bbar = ceil_log2_integer(2 * (k + 1) * (k + 1))
        full_term = Q(2 * TRUE_COMPONENT_UPPER * 4 * (1 << bbar), k * k)
        shell_rows.append(
            {
                "k": k,
                "Bbar_k": bbar,
                "full_weight_available_majorant_term": qstr(full_term),
            }
        )

    divergence_rows = [
        {
            "number_of_high_strips": count,
            "partial_majorant_strict_lower": str(2448 * count),
        }
        for count in (1, 16, 64)
    ]
    return {
        "certified_unweighted_high_strip_input": (
            "sum_(j<=153)sum_(sign)sum_(k>=6121)4/k^2<1/5"
        ),
        "homogeneity_rank_contract": (
            "on H_(sign,k), cp>1/(2(k+1)^2), hence the new target "
            "rank is <=Bbar(k)=ceil(log2(2(k+1)^2))"
        ),
        "central_child": {
            "cp_inverse_strict_upper": central_cp_inverse_upper,
            "incidence_rank_upper": central_rank_upper,
            "full_2^B_density_weighted_inverse_majorant": qstr(central_full_weight),
            "already_exceeds_one": True,
        },
        "high_strip_available_theta_majorant": (
            "M_theta=sum_(sign,j,k>=6121)(4/k^2)*2^(theta*Bbar(k)) "
            "for the new target-rank part"
        ),
        "full_theta_one_term_lower": (
            "because 2^Bbar(k)>=2(k+1)^2, every theta=1 majorant term "
            "is >=2448*(k+1)^2/k^2>2448"
        ),
        "full_theta_one_available_majorant": "INFINITE",
        "soft_exponent_exact_threshold": "M_theta<infinity iff 0<=theta<1/2",
        "threshold_proof": [
            "2^ceil(log2 x)<2x",
            "for theta<1/2 the summand is O(k^(2theta-2)) and is summable",
            "for theta>=1/2 it is bounded below by a positive multiple of k^(2theta-2), whose series diverges",
        ],
        "representative_shell_rows": shell_rows,
        "representative_shell_rows_sha256": digest(shell_rows),
        "divergence_rows": divergence_rows,
        "divergence_rows_sha256": digest(divergence_rows),
        "logical_scope": (
            "the currently certified positive expansion ledger supplies no finite "
            "full-Z_B bound; this does not assert divergence of the actual signed physical current"
        ),
        "required_replacement": (
            "face-specific cancellation/sparsity beyond the positive homogeneity majorant, "
            "or a different anisotropic trace norm; a softened theta<1/2 norm cannot pay the F10 2^B amplitude"
        ),
        "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
        "status": "CERTIFIED_SHARP_AVAILABLE_MAJORANT_THRESHOLD",
    }


def conditional_aggregate_zb_resolvent() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    w = (1 + 1 / rho) / 2
    threshold = 1 / w
    if threshold != 2 * rho / (1 + rho):
        raise RuntimeError("weight threshold identity")
    if not Q(99914, 100000) < threshold < Q(99915, 100000):
        raise RuntimeError("weight threshold bracket")
    return {
        "block_mass_rate": "rho=(111718729/111718750)^9148",
        "Round42_weight": "w_Z=(1+rho^(-1))/2",
        "hypothetical_owner_ZB_recurrence": (
            "b_(p+1)<=kappa_B*b_p+A_B*z_p+C_B*m_p"
        ),
        "exact_weighted_resolvent": (
            "sum_(p>=0)w_Z^p*b_p <= "
            "[b_0+w_Z*A_B*sum w_Z^p*z_p+w_Z*C_B*sum w_Z^p*m_p]/(1-w_Z*kappa_B)"
        ),
        "sharp_contraction_requirement": "kappa_B<w_Z^(-1)=2rho/(1+rho)",
        "threshold_strict_bracket": "99914/100000 < 2rho/(1+rho) < 99915/100000",
        "threshold_fraction_binary_sha256": fraction_digest(threshold),
        "Round42_Z_and_mass_forcing_sums_available": True,
        "owner_ZB_recurrence_coefficient_available": False,
        "current_positive_majorant_coefficient": "INFINITE_AT_THETA_1",
        "conditional_block_index_face_tower_moment": (
            "CERTIFIED_IF_A_FINITE_RECURRENCE_WITH_KAPPA_BELOW_THE_SHARP_THRESHOLD_IS_SUPPLIED"
        ),
        "collision_time_conversion": (
            "if L=9148*N_open is numeric and b_p is total face charge in block p, "
            "eta=log(w_Z)/L gives sum_t exp(eta*t)q_t<=w_Z*sum_p w_Z^p b_p"
        ),
        "numeric_collision_time_eta": None,
        "reason_eta_not_numeric": "N_open remains nonnumeric",
        "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
        "return_depth_face_tower_moment": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_CONDITIONAL_RESOLVENT_AND_SHARP_THRESHOLD",
    }


def dynamic_f17_frontier() -> dict[str, Any]:
    source_ratio = X_OVER_D1 + F13_OVER_D1
    if source_ratio != Q(11616937, 47112000) or not source_ratio < Q(1, 4):
        raise RuntimeError("source ratio")
    if QUARTER_CDYN_THRESHOLD != (Q(1, 4) - F13_OVER_D1) / X_OVER_D1:
        raise RuntimeError("quarter threshold")
    if UNIT_CDYN_THRESHOLD != (1 - F13_OVER_D1) / X_OVER_D1:
        raise RuntimeError("unit threshold")

    rows = []
    for exponent in (0, 4, 8, 12, 16):
        scale = 1 << exponent
        rows.append(
            {
                "L": scale,
                "matrix": f"diag({scale},1/{scale})",
                "determinant": "1",
                "Piola_normal_flux_multiplier": "1",
                "C1_pullback_multiplier_for_phi_y1": scale,
            }
        )
    return {
        "finite_regular_suffix": "S:U->V is one C1 area-preserving branch",
        "branch_adapted_test_norm": (
            "norm(phi)_(dyn,S)=norm(phi composed S)_C1(U)"
        ),
        "exact_dual_isometry": (
            "norm(S_*T)_(dyn,S)^*=norm(T)_(C1(U))^*"
        ),
        "branch_adapted_suffix_multiplier": "C_dyn=1",
        "branch_adapted_multiplier_below_quarter_threshold": True,
        "source_bulk_plus_trace_ratio": qstr(source_ratio),
        "required_physical_multiplier_thresholds": {
            "preserve_less_than_one_quarter": qstr(QUARTER_CDYN_THRESHOLD),
            "preserve_less_than_one": qstr(UNIT_CDYN_THRESHOLD),
        },
        "why_this_is_not_F17": (
            "the norm depends on the suffix branch; F17 requires one common physical "
            "dynamic-C1/CM2 test space and a uniform embedding of the target observables"
        ),
        "common_branch_norm_candidate": (
            "norm(phi)_common=sup_S norm(phi composed S)_C1"
        ),
        "area_preserving_embedding_countermodel": {
            "branches": "A_L=diag(L,L^(-1))",
            "test": "phi(y)=y_1",
            "physical_C1_norm": "1 up to the harmless zeroth-order chart constant",
            "common_dynamic_gradient_norm": "sup_L L=infinity",
            "rows": rows,
            "rows_sha256": digest(rows),
        },
        "logical_conclusion": (
            "area preservation, Piola flux cancellation and exact branch-adapted "
            "transport do not provide the branch-uniform physical-test embedding"
        ),
        "first_missing_interface": (
            "a billiard-specific anisotropic/dynamic test space T_dyn with "
            "sup_suffix norm(phi composed S_suffix)_source <= C_dyn*norm(phi)_T_dyn "
            "and C_dyn<43295063/7800000 (preferably <7961063/7800000)"
        ),
        "branch_dependent_dynamic_isometry": "CERTIFIED",
        "branch_uniform_physical_dynamic_test_embedding": "NOT_CERTIFIED",
        "F17_dynamic_test_operator_cost": "NOT_CERTIFIED",
        "status": "CERTIFIED_BRANCH_ADAPTED_ISOMETRY_AND_EMBEDDING_OBSTRUCTION",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base parameter s=0",
            "depth_scope": "all finite arbitrary-R_n records, followed by the unbounded depth audit",
            "claim_type": (
                "global owner-marked Borel Z_B kernel schema, exact homogeneity-majorant "
                "threshold, conditional Z_B resolvent and branch-adapted dynamic-test frontier"
            ),
        },
        "global_owner_aware_boundary_ZB_kernel": owner_aware_boundary_kernel(),
        "full_ZB_homogeneity_majorant_frontier": homogeneity_zb_majorant_frontier(),
        "conditional_aggregate_ZB_resolvent": conditional_aggregate_zb_resolvent(),
        "dynamic_anisotropic_F17_frontier": dynamic_f17_frontier(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "global standard-Borel owner-deduplicated extended-valued boundary-Z_B kernel schema",
                "sharp theta=1/2 threshold for the available positive homogeneity majorant",
                "exact conditional aggregate-Z_B resolvent and block threshold",
                "exact branch-adapted dynamic-test isometry and physical-embedding obstruction",
            ],
            "reason_no_new_field_credit": (
                "full Z_B finiteness/recurrence, return-depth face moment and one "
                "branch-uniform physical dynamic-test embedding remain missing"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "global_owner_aware_boundary_ZB_kernel_schema": "CERTIFIED",
            "global_owner_ZB_finiteness": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "branch_dependent_dynamic_isometry": "CERTIFIED",
            "branch_uniform_physical_dynamic_test_embedding": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate5_round50_owner_boundary_zb_f17_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("OWNER_ZB_KERNEL:", strict["global_owner_aware_boundary_ZB_kernel_schema"])
    print("AGGREGATE_ZB:", strict["unconditional_aggregate_ZB_resolvent"])
    print("F17:", strict["F17_bulk_dynamic_test"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
