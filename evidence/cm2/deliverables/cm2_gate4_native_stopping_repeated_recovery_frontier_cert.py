#!/usr/bin/env python3
"""Gate-4 native stopping and repeated-recovery frontier certificate.

This replay uses the corrected physical cumulative-mass coordinate ``u_e,s``
on every one of the 64 maximal event rows.  It constructs a genuine
query-independent prefix antichain in the binary filtration of that physical
coordinate, without adjoining the auxiliary product-depth random variable.

The construction is deliberately audited all the way through the recovery
charge.  Encoding the level K inside the physical coordinate consumes 2K+2
bits; appending K payload bits gives physical leaf depth 3K+2.  Thus the
native antichain has the desired level law but its inverse-mass/recovery
moment is critical and diverges.  This is an exact obstruction, not a missing
numerical experiment.

Two further exact audits are included:

* arbitrary characteristic restrictions can have infinite standard-family
  boundary Z after just one cut, and a simple repeated quarter-cut makes the
  normalized Z grow as 4^h;
* the proof chains behind the imported Growth Lemmas contain unevaluated
  constants, so qualitative existence of C_p and vartheta_p cannot be used as
  a numerical C_fw/C_rev/q certificate.

The certificate therefore closes the native physical-coordinate antichain
algebra and the finite registered-restart formula, but it fail-closes Gate 4.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
FINITE_S_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
PRODUCT_DEPTH_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
CONTROLLED_ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)
GEOMETRIC_COST_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], ...]:
    finite_s = json.loads(FINITE_S_MANIFEST.read_text(encoding="utf-8"))
    product = json.loads(PRODUCT_DEPTH_MANIFEST.read_text(encoding="utf-8"))
    algebra = json.loads(CONTROLLED_ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    costs = json.loads(GEOMETRIC_COST_MANIFEST.read_text(encoding="utf-8"))
    assert finite_s["verdict"]["finite_s_common_endpoint_mesh"] == "CERTIFIED"
    assert finite_s["verdict"]["uniform_one_time_finite_s_recovery"] == "CERTIFIED"
    assert finite_s["verdict"]["complete_propagated_numeric_C_fw_C_rev_q"] == "NOT_CERTIFIED"
    assert product["verdict"]["supercritical_depth_tail_and_E_2K"] == "CERTIFIED"
    assert algebra["verdict"]["controlled_dyadic_stopped_interval_algebra"] == "CERTIFIED"
    assert costs["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    assert costs["verdict"]["bidirectional_log_density_costs"] == "CERTIFIED"
    return finite_s, product, algebra, costs


def native_prefix_antichain(
    maximum_checked_level: int = 64,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build the exact self-delimiting prefix code in the physical u-coordinate.

    The code for K is (00)^K q with q in {01,10,11}.  Once K is known,
    append K arbitrary payload bits j.  The parent shell is one interval,
    while each (K,q,j) leaf is one dyadic interval.
    """
    rows: list[dict[str, Any]] = []
    for level in range(maximum_checked_level + 1):
        code_depth = 2 * level + 2
        leaf_depth = 3 * level + 2
        shell_mass = Q(3, 4) * Q(1, 4**level)
        leaf_mass = Q(1, 1 << leaf_depth)
        leaf_count = 3 * (1 << level)
        assert leaf_count * leaf_mass == shell_mass
        shell_left = Q(1, 4 ** (level + 1))
        shell_right = Q(1, 4**level)
        assert shell_right - shell_left == shell_mass
        listed_mass = 1 - Q(1, 4 ** (level + 1))
        partial_inverse_mass_charge = 3 * ((1 << (level + 1)) - 1)
        assert sum(
            (Q(3, 4) * Q(1, 4**k) for k in range(level + 1)), Q(0)
        ) == listed_mass
        assert sum((3 * (1 << k) for k in range(level + 1))) == (
            partial_inverse_mass_charge
        )
        rows.append({
            "K": level,
            "K_code": f"(00)^{level} q, q in {{01,10,11}}",
            "code_stopping_depth": code_depth,
            "payload_bits_after_K_is_known": level,
            "physical_leaf_depth": leaf_depth,
            "shell_interval": [str(shell_left), str(shell_right)],
            "shell_mass": str(shell_mass),
            "leaf_count": leaf_count,
            "one_leaf_mass": str(leaf_mass),
            "listed_mass_through_K": str(listed_mass),
            "zero_cemetery_mass_after_infinite_limit": True,
            "partial_expected_full_parent_normalization_charge": str(
                partial_inverse_mass_charge
            ),
        })
    return rows, {
        "physical_coordinate": (
            "u_e,s(theta)=m_e,s((left_s,theta))/m_e,s(row_s) in (0,1)"
        ),
        "binary_filtration": "dyadic Borel filtration of the physical u_e,s coordinate",
        "self_delimiting_K_code": "(00)^K q with q in {01,10,11}",
        "K_shell": "S_K=[4^(-(K+1)),4^-K)",
        "native_level_law": "m(S_K)=(3/4)*4^-K",
        "payload": "after the first nonzero pair q, read K bits j",
        "leaf_record": "(occurrence e, parameter s, K, q, j)",
        "leaf_depth": "D_K=3K+2",
        "leaf_count": "3*2^K",
        "one_leaf_mass_fraction": "2^(-(3K+2))",
        "prefix_free": True,
        "binary_filtration_stopping_time": True,
        "full_mass_except_u_equals_zero": True,
        "zero_cemetery_mass": True,
        "query_independent": True,
        "record_fixed_before_orientation_time_mode_and_final_test": True,
        "same_occurrence_and_same_restricted_measure_in_both_orientations": True,
        "no_auxiliary_randomness": True,
        "physical_mass_coordinate_native_antichain": "CERTIFIED",
        "orbit_return_word_stopping_antichain": False,
        "checked_level_range": [0, maximum_checked_level],
        "rows_sha256": canonical_digest(rows),
    }


def native_recovery_charge_obstruction(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cutoffs = [0, 1, 2, 4, 8, 16, 32, 64]
    cutoff_rows = []
    by_level = {row["K"]: row for row in rows}
    for cutoff in cutoffs:
        expected_leaf_normalization = sum(
            int(by_level[level]["leaf_count"]) for level in range(cutoff + 1)
        )
        expected_physical_depth_factor = sum(
            Q(by_level[level]["shell_mass"])
            * (1 << int(by_level[level]["physical_leaf_depth"]))
            for level in range(cutoff + 1)
        )
        shell_only_inverse_mass = Q(cutoff + 1)
        formula = 3 * ((1 << (cutoff + 1)) - 1)
        assert expected_leaf_normalization == formula
        assert expected_physical_depth_factor == formula
        cutoff_rows.append({
            "cutoff_N": cutoff,
            "native_leaf_expected_inverse_mass_charge": str(
                expected_leaf_normalization
            ),
            "native_expected_2_to_physical_leaf_depth": str(
                expected_physical_depth_factor
            ),
            "shell_only_expected_inverse_shell_mass_charge": str(
                shell_only_inverse_mass
            ),
        })
    return cutoff_rows, {
        "auxiliary_product_policy_reference": (
            "external K with w_K=(3/4)4^-K and physical depth K has E[2^K]=3/2"
        ),
        "native_encoding_cost": (
            "K must be encoded in 2K+2 physical bits before K payload bits; D_K=3K+2"
        ),
        "native_level_charge": (
            "w_K*2^(D_K)=3*2^K, equivalently one unit per nonempty leaf"
        ),
        "native_partial_charge_through_N": "3*(2^(N+1)-1)",
        "native_full_parent_normalization_moment": "infinity",
        "shell_only_partial_charge_through_N": "N+1",
        "shell_only_normalization_moment": "infinity",
        "general_partition_identity": (
            "for disjoint positive-mass atoms A_i with normalization cost 1/mu(A_i), "
            "sum_i mu(A_i)/mu(A_i)=number of atoms"
        ),
        "full_mass_native_countable_partition_no_go": (
            "if leaf a has physical probability p_a>0 and is normalized leafwise at "
            "cost p_a^-1, then E[p_A^-1]=sum_a p_a*p_a^-1=sum_a 1=infinity"
        ),
        "level_K_counting_form": (
            "if level K has 2^K positive-mass native leaves, that level contributes "
            "2^K to the expected inverse-leaf-mass charge, independently of w_K"
        ),
        "why_product_kernel_escapes_counting_no_go": (
            "K is an external mark of mass w_K; conditional on K the physical row is "
            "cut only into 2^K atoms and pays 2^K, so the charge is sum_K w_K*2^K=3/2, "
            "not the inverse joint-atom cost (w_K*2^-K)^-1"
        ),
        "possible_unnormalized_escape_not_certified": (
            "evolve all stopped leaves as one unnormalized/reweighted family and prove a "
            "global Z/recovery bound without leafwise p_a^-1 normalization"
        ),
        "other_possible_escapes_not_certified": [
            "a finite native antichain plus a quantitatively charged cemetery",
            "an external product/reweighting mark (the existing auxiliary policy)",
            "a replacement Gate-4 cost functional that does not normalize every leaf",
        ],
        "countably_infinite_native_partition_has_finite_inverse_mass_moment": False,
        "native_antichain_replaces_auxiliary_product_record_algebra": True,
        "native_antichain_replaces_auxiliary_product_recovery_moment": False,
        "native_depth_plus_recovery_target": "DIVERGES_BEFORE_RECOVERY",
        "cutoff_rows_sha256": canonical_digest(cutoff_rows),
    }


def repeated_indicator_countermodels() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    quarter_rows = []
    for generation in range(17):
        component_count = 1 << generation
        one_length = Q(1, 4**generation)
        retained_mass = component_count * one_length
        normalized_weight = one_length / retained_mass
        normalized_z = component_count * normalized_weight / one_length
        assert retained_mass == Q(1, 1 << generation)
        assert normalized_weight == Q(1, 1 << generation)
        assert normalized_z == 4**generation
        quarter_rows.append({
            "generation_h": generation,
            "component_count": component_count,
            "one_component_length": str(one_length),
            "retained_mass": str(retained_mass),
            "normalized_weight_per_component": str(normalized_weight),
            "normalized_boundary_Z": str(normalized_z),
        })

    open_set_rows = []
    for count in (1, 2, 4, 8, 16, 32, 64):
        lengths = [Q(1, 1 << (2 * index + 2)) for index in range(1, count + 1)]
        mass = sum(lengths, Q(0))
        assert mass == Q(1, 12) * (1 - Q(1, 4**count))
        normalized_z = Q(count, 1) / mass
        open_set_rows.append({
            "component_cutoff_N": count,
            "truncated_open_set_mass": str(mass),
            "normalized_boundary_Z": str(normalized_z),
        })
    return quarter_rows, open_set_rows, {
        "repeated_cut": (
            "on every current interval retain its first and last quarter"
        ),
        "repeated_cut_normalized_Z": "Z_h=4^h",
        "repeated_cut_has_no_uniform_properness_without_recovery_wait": True,
        "single_open_indicator": (
            "U=union_(n>=1) (2^-n,2^-n+2^(-2n-2))"
        ),
        "single_open_indicator_mass": "1/12",
        "single_open_indicator_component_count": "countably infinite",
        "single_open_indicator_normalized_Z": "infinity",
        "arbitrary_characteristic_restriction_preserves_finite_Z": False,
        "one_cut_can_leave_the_standard_family_class": True,
        "quarter_rows_sha256": canonical_digest(quarter_rows),
        "open_set_rows_sha256": canonical_digest(open_set_rows),
    }


def finite_registered_restart_formula(c_mesh: str) -> dict[str, Any]:
    return {
        "admissible_finite_history": (
            "H fixed cuts, each cut already registered as a finite regular standard-family "
            "decomposition with Z_i/mu_i<=C_mesh*2^K_i"
        ),
        "mandatory_order": (
            "restrict, retain the immutable occurrence record, recover to properness in both "
            "orientations, only then admit the next indicator"
        ),
        "initial_numeric_C_mesh": c_mesh,
        "symbolic_two_orientation_wait": (
            "R_total<=2H*A0+2A1*sum_(i=1)^H K_i"
        ),
        "fixed_H_product_depth_moment": (
            "E[2^sum(K_i)*exp(gamma*R_total)] "
            "<=exp(2gamma*H*A0)*((3/4)/(1-exp(2gamma*A1)/2))^H"
        ),
        "admissible_gamma": "0<gamma<log(2)/(2A1)",
        "finite_registered_separated_cut_restart": "CERTIFIED_CONDITIONAL_SCHEMA",
        "uses_auxiliary_product_depth_marks": True,
        "native_physical_repeated_indicator_law": False,
        "arbitrary_or_unseparated_repeated_cuts": False,
        "minimal_missing_restriction_interface": (
            "for every physical branch history and next actual indicator, a query-independent "
            "record-preserving decomposition with finite normalized Z and a uniform moment "
            "for its boundary/recovery charge"
        ),
        "also_missing_for_unbounded_cut_count": (
            "a tail on H strong enough to sum the accumulated restart charge"
        ),
    }


def growth_constant_dependency_audit(c_mesh: str) -> dict[str, Any]:
    # Qualitative 0<theta<1 permits both of these values.  The second forces
    # A1 to be enormous: -log(1-x) < x/(1-x), log(2)>1/2.
    slow_x = Q(1, 1 << 20)
    slow_a1_lower = ((1 << 20) - 1 + 1) // 2
    assert slow_a1_lower == 1 << 19
    return {
        "numerical_geometry_already_certified": {
            "parameter_window": "|s|<=1/400",
            "tau_min": "36337/800000>1/25",
            "curvature_interval": "[25/9,25/4]",
            "finite_horizon": "(3,1/512)",
            "one_collision_bidirectional_coefficient": "204",
            "initial_C_mesh": c_mesh,
        },
        "SYZ_Lemma_12_statement": (
            "there exist C_gr>0 and 0<vartheta_gr<1; the proof is referred to "
            "the fixed-configuration literature and no values are supplied"
        ),
        "SYZ_Lemma_16_statement": (
            "there exist C_p>1 and 0<vartheta_p<1; it is called a direct "
            "consequence of the Growth Lemma and no values are supplied"
        ),
        "SYZ_nonnumeric_leaf_constants": [
            "c_hat and Lambda (Lemma 6 hyperbolicity)",
            "sufficiently large homogeneity cutoff k0",
            "C_c and vartheta_c (Lemma 8 carrier curvature)",
            "C_d0 and C_d (Lemma 9 distortion)",
            "C_s (separation-time metric comparison)",
            "C_r (regular-density constant)",
            "C_gr and vartheta_gr (Lemma 12)",
            "C_p and vartheta_p (Lemma 16)",
        ],
        "Canestrari_6_13_6_14_nonnumeric_leaf_constants": [
            "theta_* and the sequence delta_n from Demers Lemma 8.4",
            "C_metric, Q_3, C_cone and varpi_2",
            "n_* selected from a strict contraction inequality",
            "delta_*=min(delta_n*,1) and Z_0=2e^varpi_2 Q_3 C_cone/delta_*",
        ],
        "existing_symbolic_recovery_constants": (
            "A0=ceil(log(C_mesh)/abs(log(vartheta_p)))+1, "
            "A1=ceil(log(2)/abs(log(vartheta_p)))"
        ),
        "qualitative_theta_fast_example": "vartheta_p=1/4 gives A1=1",
        "qualitative_theta_slow_example": "vartheta_p=1-2^-20",
        "slow_example_exact_inequality": (
            "-log(1-2^-20)<1/(2^20-1) and log(2)>1/2"
        ),
        "slow_example_forces_A1_at_least": slow_a1_lower,
        "qualitative_existence_determines_numeric_A1": False,
        "theorem_constants_can_be_honestly_replaced_by_arbitrary_numerals": False,
        "complete_propagated_numeric_C_fw_C_rev_q": False,
        "smallest_executable_numeric_task": (
            "certify one explicit n-step expansion/cut sum and distortion ratio on the "
            "declared homogeneity atlas, yielding numeric vartheta_gr,C_gr and hence C_p"
        ),
    }


def certify() -> dict[str, Any]:
    finite_s, product, algebra, costs = load_dependencies()
    c_mesh = finite_s["result"]["finite_s_density_mesh_and_numeric_C_mesh"][
        "explicit_initial_C_mesh"
    ]
    assert c_mesh == "69986663973833932800"
    rows, antichain = native_prefix_antichain()
    cutoff_rows, native_obstruction = native_recovery_charge_obstruction(rows)
    quarter_rows, open_rows, indicator = repeated_indicator_countermodels()
    restart = finite_registered_restart_formula(c_mesh)
    constants = growth_constant_dependency_audit(c_mesh)
    assert product["result"]["mass_preserving_product_stopped_kernel"][
        "exact_normalization_moment"
    ] == "E[2^K]=3/2"
    assert algebra["result"]["all_maximal_row_contracts"][
        "maximal_occurrence_count"
    ] == 64
    assert costs["result"]["scope_limits"][
        "all_row_bidirectional_carrier_C2_bounds"
    ] is True
    return {
        "schema": "cm2.gate4.native-stopping-repeated-recovery-frontier.v1",
        "provenance": {
            "finite_s_common_mesh_recovery_manifest": FINITE_S_MANIFEST.name,
            "product_stopped_depth_manifest": PRODUCT_DEPTH_MANIFEST.name,
            "controlled_interval_algebra_manifest": CONTROLLED_ALGEBRA_MANIFEST.name,
            "geometric_cost_manifest": GEOMETRIC_COST_MANIFEST.name,
            "maximal_occurrence_count": 64,
            "parameter_window": "|s|<=1/400",
        },
        "native_physical_mass_coordinate_prefix_antichain": antichain,
        "native_recovery_charge_obstruction": native_obstruction,
        "repeated_indicator_countermodels": indicator,
        "finite_registered_restart_frontier": restart,
        "numeric_growth_constant_dependency_audit": constants,
        "exact_remaining_frontier": {
            "certified_now": [
                "full-mass query-independent prefix antichain in each physical row mass coordinate",
                "same-occurrence same-restriction bidirectional record without auxiliary randomness",
                "exact native inverse-mass/recovery divergence audit",
                "exact arbitrary-indicator and repeated-quarter-cut Z countermodels",
                "finite registered separated-cut symbolic restart formula",
                "complete dependency audit for the missing numerical Growth constants",
            ],
            "still_missing": [
                "an orbit-return-word native stopping antichain with the required charged moment",
                "a physical restriction regularizer for every actual repeated indicator history",
                "a tail for an unbounded number of repeated cuts",
                "numeric C_gr,vartheta_gr/distortion inputs and hence numeric C_p,vartheta_p",
                "complete propagated numeric C_fw,C_rev and one same-occurrence q",
            ],
        },
        "scope_limits": {
            "native_physical_mass_coordinate_prefix_antichain": True,
            "query_independent_same_occurrence_bidirectional_record": True,
            "auxiliary_random_depth_needed_for_record_algebra": False,
            "native_antichain_finite_normalization_recovery_moment": False,
            "native_orbit_return_word_stopping_antichain": False,
            "hereditary_repeated_indicator_recovery": False,
            "finite_registered_separated_cut_restart_schema": True,
            "theorem_recovery_constants_numeric": False,
            "complete_propagated_numeric_C_fw_C_rev_q": False,
            "gate4_certified": False,
        },
        "internal_replay_digests": {
            "native_rows": canonical_digest(rows),
            "native_cutoff_rows": canonical_digest(cutoff_rows),
            "quarter_cut_rows": canonical_digest(quarter_rows),
            "open_indicator_rows": canonical_digest(open_rows),
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_NATIVE_PHYSICAL_MASS_COORDINATE_PREFIX_ANTICHAIN: CERTIFIED")
    print("GATE4_NATIVE_DEPTH_PLUS_RECOVERY_MOMENT: NOT_CERTIFIED")
    print("GATE4_HEREDITARY_REPEATED_INDICATOR_RECOVERY: NOT_CERTIFIED")
    print("GATE4_PROPAGATED_NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
