#!/usr/bin/env python3
"""Round-28 fail-closed strong-q weighted-tail transfer frontier.

This append-only leaf joins the round-27 arbitrary-n first-return mass ledger,
the C24 unweighted exponential survivor tail, the finite Q2 once-charged
payload, and the frozen numerical recovery stack.  It proves three exact
transfer lemmas for a nonnegative branch charge q=c*m:

* a survivor-conditioned L^p envelope preserves the unweighted tail rate;
* a global L^p envelope yields the Hölder-degraded exponential rate;
* a pointwise exponential cost transfers by a block series precisely when
  the *series route* satisfies G^N r < 1.

The last condition is an exact compatibility condition for that bounding
route, not a claim that CM2 weighted tails are impossible outside it.  The
current frozen stack has no numerical first-return C_fw/C_rev rows and hence
satisfies none of the new sufficient hypotheses.  Gate 4, Gate 5 and the
induced Lasota--Yorke coefficient therefore remain fail-closed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round28-weighted-tail-transfer-frontier.v1"
MANIFEST_SCHEMA = "cm2.gate45.round28-weighted-tail-transfer-frontier.manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": (
        "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6"
    ),
}

TAIL_A = Q(550000, 147)
TAIL_R = Q(111718729, 111718750)
TAIL_EPSILON = Q(21, 111718750)
TAIL_RECIPROCAL = Q(111718750, 111718729)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency type: {name}")
        loaded[name] = value

    sparse = loaded[
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    ]
    require(
        sparse["verdict"]["C24_uniform_unweighted_exponential_return_tail"]
        == "CERTIFIED",
        "unweighted tail",
    )
    hit = sparse["result"]["uniform_recovered_cone_hit_gap"]
    require(
        hit["explicit_per_block_survival_factor"] == str(TAIL_R),
        "block survival factor",
    )
    require(hit["explicit_per_block_hit_gap_epsilon"] == str(TAIL_EPSILON), "epsilon")
    scheduled = sparse["result"]["scheduled_and_all_time_tail"]
    require(
        scheduled["block_length_is_theorem_supplied_not_numerically_materialized"]
        is True,
        "N_open typing",
    )
    require(
        scheduled["collision_time_exponential_form"]["rho_open"]
        == "(111718729/111718750)^(1/N_open)",
        "rho_open",
    )

    paths = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    require(
        paths["verdict"]["arbitrary_n_Rn_Qn_measurable_level_and_mass_schema"]
        == "CERTIFIED",
        "arbitrary-n mass schema",
    )
    level = paths["result"]["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    require(
        level["unweighted_exponential_Rn_Qn_mass_ledger"] == "CERTIFIED_SYMBOLIC",
        "mass ledger",
    )
    require(level["q_weighted_strong_tail"] == "NOT_CERTIFIED", "weighted scope")
    require(
        level["symbolic_physical_mass"]["numeric_component_masses_materialized"]
        is False,
        "numeric component scope",
    )
    require(
        level["normalized_core_mass_interval"]
        == ["147/550000_strict_lower", "29021/75000000_strict_upper"],
        "normalized core mass interval",
    )
    require(Q(0) < Q(147, 550000) < Q(29021, 75000000) < Q(1), "core mass in (0,1)")

    q2 = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]
    charge = q2["result"]["Q2_symbolic_strong_charge_registry"]
    require(charge["symbolic_q2_charge_count"] == 114006, "symbolic q2")
    require(charge["numeric_C_fw_count"] == 0, "numeric Cfw")
    require(charge["numeric_C_rev_count"] == 0, "numeric Crev")
    require(charge["numeric_q2_count"] == 0, "numeric q2")
    registry = q2["result"]["Q2_exact_mass_and_restriction_registry"]
    require(registry["common_forward_reverse_restriction_id_count"] == 114006, "restriction IDs")
    require(registry["common_strong_recovery_carrier_count"] == 0, "strong carrier scope")

    numeric = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    require(
        numeric["verdict"]["native_levelwise_unnormalized_recovery_moment"]
        == "CERTIFIED",
        "native moment",
    )
    require(
        numeric["verdict"]["complete_unnormalized_reweighted_native_recovery"]
        == "NOT_CERTIFIED",
        "reweighted scope",
    )
    require(
        numeric["verdict"]["complete_numeric_C_fw_C_rev_final_q"]
        == "NOT_CERTIFIED",
        "final q scope",
    )
    summary = numeric["replay_summary"]
    require(summary["vartheta_p"] == "360134800/360493663", "vartheta_p")
    require(summary["A0"] == 301500 and summary["A1"] == 1005, "recovery constants")
    require(summary["native_gamma"] == "1/12060", "native gamma")

    product = loaded[
        "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
    ]["verdict"]
    require(product["numeric_joint_B_K_recovery_moment"] == "CERTIFIED", "product moment")
    require(product["fixed_finite_H_registered_restart_moment"] == "CERTIFIED", "fixed H")
    require(
        product["arbitrary_or_unbounded_repeated_indicator_recovery"]
        == "NOT_CERTIFIED",
        "unbounded scope",
    )

    native = loaded[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]["verdict"]
    require(native["native_physical_mass_coordinate_prefix_antichain"] == "CERTIFIED", "native antichain")
    require(native["native_depth_plus_recovery_moment"] == "NOT_CERTIFIED", "native moment scope")
    require(native["hereditary_repeated_indicator_recovery"] == "NOT_CERTIFIED", "hereditary scope")

    obstruction = loaded[
        "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json"
    ]
    require(
        obstruction["verdict"]["open_to_induced_coefficient_nonimplication"]
        == "CERTIFIED",
        "open/induced obstruction",
    )
    require(
        obstruction["verdict"]["induced_strong_coefficient"] == "NOT_CERTIFIED",
        "induced scope",
    )
    return loaded


def first_return_mass_join(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    paths = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]["result"]
    level = paths["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    component = paths["canonical_regular_connected_component_schema"]
    q2 = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]["result"]
    charge = q2["Q2_symbolic_strong_charge_registry"]
    registry = q2["Q2_exact_mass_and_restriction_registry"]
    return {
        "return_clock": level["return_clock"],
        "level_identity_mod_null": level["level_identity_mod_null"],
        "finite_telescope_mod_null": level["finite_telescope_mod_null"],
        "infinite_first_return_partition_mod_null": level[
            "infinite_first_return_partition_mod_null"
        ],
        "normalized_survivor_mass_symbol": "S_n=mu_s(Q_n)/mu_s(C_s)",
        "normalized_first_return_component_mass_symbol": (
            "mbar_s,n,k=m_s,n,k/mu_s(C_s)"
        ),
        "normalized_first_return_level_mass_symbol": (
            "a_n=sum_k mbar_s,n,k=S_(n-1)-S_n"
        ),
        "normalized_first_return_component_charge_symbol": (
            "qbar_s,n,k=q_s,n,k/mu_s(C_s)"
        ),
        "uniform_unweighted_tail": (
            "S_n<(550000/147)*(111718729/111718750)^floor(n/N_open)"
        ),
        "tail_prefactor_A": str(TAIL_A),
        "tail_block_factor_r": str(TAIL_R),
        "tail_hit_gap_epsilon": str(TAIL_EPSILON),
        "N_open": "one_uniform_theorem_supplied_integer>=1_not_numeric",
        "singular_and_core_boundary_cemetery_collision_SRB_mass": "0",
        "regular_component_partition_exists_mod_null": component[
            "R_n_and_Q_n_regular_component_partition_exists_mod_null"
        ],
        "exact_nonempty_component_rows_enumerated": component[
            "component_coordinates_and_nonempty_ranks_enumerated"
        ],
        "numeric_arbitrary_n_component_masses_materialized": level[
            "symbolic_physical_mass"
        ]["numeric_component_masses_materialized"],
        "finite_Q2_exact_mass_and_common_restriction_rows": registry[
            "strict_Q2_inner_atom_count"
        ],
        "finite_Q2_symbolic_once_charged_rows": charge["symbolic_q2_charge_count"],
        "finite_Q2_numeric_C_fw_rows": charge["numeric_C_fw_count"],
        "finite_Q2_numeric_C_rev_rows": charge["numeric_C_rev_count"],
        "finite_Q2_numeric_q_rows": charge["numeric_q2_count"],
        "finite_Q2_common_strong_recovery_carrier_rows": registry[
            "common_strong_recovery_carrier_count"
        ],
        "physical_first_return_q_density_rows_ready_for_tail_sum": 0,
    }


def weighted_tail_transfer_theorem() -> dict[str, Any]:
    require(TAIL_R == 1 - TAIL_EPSILON, "r=1-epsilon")
    require(TAIL_R * TAIL_RECIPROCAL == 1, "reciprocal")
    require(Q(1) < TAIL_RECIPROCAL < Q(1000001, 1000000), "reciprocal scale")

    definitions = {
        "normalized_component_mass": "mbar_j,k=m_j,k/mu_s(C_s)",
        "normalized_component_charge": "qbar_j,k=q_j,k/mu_s(C_s)",
        "positive_mass_component_density": (
            "c_j,k=qbar_j,k/mbar_j,k=q_j,k/m_j,k>=0 when mbar_j,k>0"
        ),
        "zero_mass_policy": (
            "mbar_j,k=0 requires qbar_j,k=0 for an absolutely-continuous charge"
        ),
        "normalized_weighted_first_return_tail": (
            "Wbar_n=sum_{j>n}sum_k qbar_j,k"
        ),
        "normalized_unweighted_first_return_tail": (
            "S_n=sum_{j>n}sum_k mbar_j,k=mu_s(Q_n)/mu_s(C_s)"
        ),
        "physical_weighted_tail_corollary": (
            "Wphys_n=mu_s(C_s)*Wbar_n<=Wbar_n because 0<mu_s(C_s)<1"
        ),
        "scope": "regular first-return components; cemetery strong charge is accounted separately",
        "two_views_charge_policy": "q=max(C_fw,C_rev,2)*m is charged once, never once per view",
    }

    conditional_lp = {
        "hypotheses": [
            "p>1",
            "0<K_p<infinity",
            "for every n: sum_{j>n,k} mbar_j,k*c_j,k^p <= K_p^p*S_n",
            "all qbar_j,k are on the same physical first-return component and common fw/rev restriction",
        ],
        "holder_step": (
            "Wbar_n<=(sum_tail mbar*c^p)^(1/p)*S_n^(1-1/p)<=K_p*S_n"
        ),
        "conclusion": "Wbar_n<K_p*A*r^floor(n/N_open)",
        "physical_conclusion": "Wphys_n<Wbar_bound",
        "rate_effect": "preserves_the_unweighted_block_factor_r",
        "status": "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM",
    }

    global_lp = {
        "hypotheses": [
            "p>1",
            "0<M_p<infinity",
            "sum_{j>=1,k} mbar_j,k*c_j,k^p <= M_p",
            "all qbar_j,k are physical first-return charges on the normalized mass ledger",
        ],
        "holder_step": (
            "Wbar_n<=M_p^(1/p)*S_n^(1-1/p)"
        ),
        "conclusion": (
            "Wbar_n<M_p^(1/p)*A^(1-1/p)*r^((1-1/p)*floor(n/N_open))"
        ),
        "p_equals_2_specialization": (
            "Wbar_n<sqrt(M_2*A)*r^(floor(n/N_open)/2)"
        ),
        "physical_conclusion": "Wphys_n<Wbar_bound",
        "rate_effect": "block_exponent_is_multiplied_by_1-1/p",
        "status": "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM",
    }

    pointwise = {
        "hypotheses": [
            "C>0 and G>=1",
            "c_j,k<=C*G^j on every positive-mass first-return component",
            "G^N_open*r<1",
        ],
        "block_indexing": "block b contains return times b*N_open<j<=(b+1)*N_open",
        "block_mass_bound": "sum_{b*N_open<j<=(b+1)*N_open,k}mbar_j,k<=S_(b*N_open)<A*r^b",
        "geometric_series_bound": (
            "Wbar_n<C*A*G^N_open*(G^N_open*r)^floor(n/N_open)/(1-G^N_open*r)"
        ),
        "series_route_compatibility": "G^N_open*r<1 iff G<r^(-1/N_open)",
        "uniform_cost_special_case": (
            "if G=1 then direct domination gives Wbar_n<=C*S_n<C*A*r^floor(n/N_open)"
        ),
        "physical_conclusion": "Wphys_n<Wbar_bound",
        "status": "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM",
        "necessity_scope": (
            "compatibility is necessary only for this geometric upper-series route, not for the physical CM2 tail"
        ),
    }

    blockwise = {
        "hypotheses": [
            "C>0 and H>=1",
            "c_j,k<=C*H^ceil(j/N_open) on every positive-mass first-return component",
            "H*r<1",
        ],
        "conclusion": (
            "Wbar_n<C*A*H*(H*r)^floor(n/N_open)/(1-H*r)"
        ),
        "physical_conclusion": "Wphys_n<Wbar_bound",
        "series_route_compatibility": "H*r<1 iff H<1/r",
        "status": "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM",
    }

    compatibility = {
        "r": str(TAIL_R),
        "epsilon_equals_1_minus_r": str(TAIL_EPSILON),
        "one_over_r": str(TAIL_RECIPROCAL),
        "one_over_r_minus_one": "21/111718729",
        "exact_log_window": (
            "21/111718750 < -log(r) < 21/111718729"
        ),
        "log_window_reason": "for 0<x<1: x<-log(1-x)<x/(1-x)",
        "per_collision_series_condition": "log(G)<-log(r)/N_open",
        "per_block_series_condition": "log(H)<-log(r)",
        "any_G_at_least_one_over_r_fails_the_series_condition_for_every_integer_N_open_at_least_1": True,
        "any_H_at_least_one_over_r_fails_the_block_series_condition": True,
        "every_integer_G_at_least_2_fails_the_series_condition": True,
        "numeric_N_open_needed_to_turn_r^(-1/N_open)_into_a_numeric_per_collision_threshold": True,
        "no_impossibility_claim_for_other_transfer_routes": True,
    }
    return {
        "definitions": definitions,
        "survivor_conditioned_Lp_transfer": conditional_lp,
        "global_Lp_transfer": global_lp,
        "pointwise_per_collision_exponential_transfer": pointwise,
        "pointwise_per_block_exponential_transfer": blockwise,
        "exact_compatibility_window": compatibility,
    }


def current_stack_instantiation(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    numeric = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    product = loaded[
        "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json"
    ]["verdict"]
    native = loaded[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]["verdict"]
    return {
        "certified_numeric_recovery_constants": {
            "global_D_std_strict_upper": numeric["replay_summary"][
                "global_D_std_strict_upper"
            ],
            "vartheta_p": numeric["replay_summary"]["vartheta_p"],
            "A0": numeric["replay_summary"]["A0"],
            "A1": numeric["replay_summary"]["A1"],
            "native_gamma": numeric["replay_summary"]["native_gamma"],
            "native_levelwise_unnormalized_recovery_moment": "CERTIFIED",
        },
        "strict_type_boundary": {
            "complete_unnormalized_reweighted_native_recovery": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_final_q": "NOT_CERTIFIED",
            "product_same_occurrence_joint_moment": product[
                "numeric_joint_B_K_recovery_moment"
            ],
            "product_fixed_finite_H_restart": product[
                "fixed_finite_H_registered_restart_moment"
            ],
            "product_arbitrary_or_unbounded_repeated_indicator_recovery": product[
                "arbitrary_or_unbounded_repeated_indicator_recovery"
            ],
            "native_physical_prefix_antichain": native[
                "native_physical_mass_coordinate_prefix_antichain"
            ],
            "native_depth_plus_recovery_moment": native[
                "native_depth_plus_recovery_moment"
            ],
            "hereditary_repeated_indicator_recovery": native[
                "hereditary_repeated_indicator_recovery"
            ],
            "fixed_product_mark_is_a_physical_first_return_component_moment": False,
            "open_power_coefficient_is_an_induced_first_return_coefficient": False,
        },
        "new_transfer_hypothesis_status": {
            "uniform_survivor_conditioned_Lp_first_return_envelope_count": 0,
            "global_Lp_physical_first_return_charge_envelope_count": 0,
            "compatible_pointwise_exponential_first_return_envelope_count": 0,
            "numeric_strong_cemetery_charge_rows": 0,
            "transfer_hypothesis_satisfied_by_current_frozen_stack": False,
        },
        "weighted_tail_status": {
            "unweighted_first_return_tail": "CERTIFIED",
            "strong_q_weighted_first_return_tail": "NOT_CERTIFIED",
            "strong_q_weighted_cemetery_tail": "NOT_CERTIFIED",
            "numeric_tail_rho_for_induced_strong_space": "NOT_CERTIFIED",
        },
    }


def missing_interface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "index": 1,
            "record": "nonempty_physical_first_return_component_rows",
            "current": "EXISTENCE_SCHEMA_ONLY",
            "needed": "component IDs, positive mass, and R_n/Q_n first-return typing",
        },
        {
            "index": 2,
            "record": "common_fw_rev_restriction_and_recovery_carrier",
            "current": "FINITE_Q2_RESTRICTION_IDS_ONLY_STRONG_CARRIER_COUNT_0",
            "needed": "one physical component carrier shared by both nonadditive views",
        },
        {
            "index": 3,
            "record": "numeric_once_charged_C_fw_C_rev_q_density",
            "current": "SYMBOLIC_Q2_COUNT_114006_NUMERIC_COUNT_0",
            "needed": "c_j,k=max(C_fw,C_rev,2) on each positive-mass branch",
        },
        {
            "index": 4,
            "record": "first_return_tail_transfer_envelope",
            "current": "COUNT_0",
            "needed": "survivor-conditioned Lp, global Lp, or compatible pointwise block envelope",
        },
        {
            "index": 5,
            "record": "strong_singular_cemetery_charge",
            "current": "COUNT_0",
            "needed": "strong-space absolute-continuity or an independent summable cemetery estimate",
        },
        {
            "index": 6,
            "record": "induced_common_space_Lasota_Yorke_assembly",
            "current": "NOT_CERTIFIED",
            "needed": "weighted tail plus complete branch F14-F18 costs and compatible contraction",
        },
    ]
    require([row["index"] for row in rows] == list(range(1, 7)), "row indices")
    return rows


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    rows = missing_interface_rows()
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "audit_policy": "exact_manifest_join_plus_exact_rational_tail_transfer_lemmas",
            "parameter_quantifier": "uniformly_for_every_fixed_|s|<=1/400",
            "charge_typing": "one_physical_first_return_component_one_once_charged_q",
        },
        "first_return_mass_ledger_join": first_return_mass_join(loaded),
        "weighted_tail_transfer_theorem": weighted_tail_transfer_theorem(),
        "current_frozen_stack_instantiation": current_stack_instantiation(loaded),
        "missing_first_return_strong_interface": {
            "required_record_count": len(rows),
            "currently_complete_record_count": 0,
            "rows": rows,
            "rows_sha256": canonical_digest(rows),
            "shortest_next_target": (
                "materialize same-ID first-return c=q/m rows and prove a survivor-conditioned Lp envelope"
            ),
        },
        "strict_nonpromotion": {
            "conditional_transfer_theorem_implies_current_CM2_weighted_tail": False,
            "fixed_finite_H_product_restart_is_unbounded_physical_return_recovery": False,
            "unweighted_tail_plus_symbolic_q_implies_weighted_tail": False,
            "collision_null_cemetery_mass_alone_bounds_strong_cemetery_charge": False,
            "open_operator_coefficient_reused_as_induced_coefficient": False,
            "q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "complete_18_field_operator_blocks": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    payload = copy.deepcopy(result)
    result["internal_replay_digest"] = canonical_digest(payload)
    return result


def verdict() -> dict[str, Any]:
    return {
        "C24_first_return_mass_and_unweighted_tail_join": "CERTIFIED",
        "survivor_conditioned_Lp_weighted_tail_transfer": "CERTIFIED_CONDITIONAL_THEOREM",
        "global_Lp_weighted_tail_transfer": "CERTIFIED_CONDITIONAL_THEOREM",
        "pointwise_exponential_series_compatibility_threshold": "CERTIFIED_EXACT",
        "current_physical_first_return_transfer_hypothesis": "NOT_CERTIFIED",
        "current_strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": build_result(),
        "verdict": verdict(),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round28_weighted_tail_transfer_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    join = result["first_return_mass_ledger_join"]
    print("C24_FIRST_RETURN_MASS_AND_UNWEIGHTED_TAIL_JOIN: CERTIFIED")
    print("WEIGHTED_TAIL_TRANSFER_LEMMAS: CERTIFIED_CONDITIONAL")
    print(f"TAIL_BLOCK_FACTOR_R: {join['tail_block_factor_r']}")
    print("CURRENT_PHYSICAL_STRONG_Q_TAIL: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
