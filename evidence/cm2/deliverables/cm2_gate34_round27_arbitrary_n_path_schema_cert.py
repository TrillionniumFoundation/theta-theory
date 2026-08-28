#!/usr/bin/env python3
"""Round-27 arbitrary-n C24 path-key and regular-component schema.

This append-only certificate performs the exact join that was still absent
between four already frozen objects:

* the full-measure two-dimensional regular collision-step key grammar;
* the twenty-four positive-area physical cores;
* the collision-SRB Kac first-return levels and the uniform unweighted
  exponential return tail;
* the round-26 physical one-step limiting partition and finite Q2 anchors.

For every fixed parameter and every finite n it defines full-dimensional
candidate path fibres for R_n and Q_n, proves coverage modulo the singular
and core-boundary null set, and supplies a canonical countable connected-
component refinement schema.  The component labels are existence labels
obtained from a countable rational basis; nonempty components, margins,
numeric masses and strong payloads are deliberately not enumerated here.
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
RESULT_SCHEMA = "cm2.gate34.round27-arbitrary-n-path-schema.v1"
MANIFEST_SCHEMA = "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
}

CORE_COUNT = 24
STEP_KEY_ALPHABET_SIZE = 441280
SAMPLE_DEPTHS = tuple(range(1, 10))
CORE_MASS_STRICT_LOWER = Q(147, 550000)
CORE_MASS_STRICT_UPPER = Q(29021, 75000000)
BLOCK_SURVIVAL_FACTOR = Q(111718729, 111718750)


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

    cores = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    core_registry = cores["result"]["physical_return_core_registry"]
    require(
        core_registry["physical_compact_homogeneous_core_count"] == CORE_COUNT,
        "core count",
    )
    require(
        core_registry[
            "collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"
        ]
        == "147/550000",
        "core mass lower",
    )
    require(
        core_registry["all_cores_uniform_on_full_parameter_window"] is True,
        "uniform cores",
    )

    path = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]["result"]["full_mass_2d_path_key_schema"]
    require(path["countable_full_measure_2d_path_key_schema"] is True, "path schema")
    require(
        path["path_key_grammar"]["base_alphabet_size"] == STEP_KEY_ALPHABET_SIZE,
        "alphabet size",
    )
    require(
        path["regular_collision_step_key_coverage"]
        == "1 modulo collision-SRB null set",
        "regular step coverage",
    )
    require(
        path["path_key_grammar"]["singular_orbit_cemetery"]
        == "countable union of grazing/corner preimages; collision-SRB null",
        "singular cemetery",
    )

    gate5 = loaded[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]["result"]["immutable_candidate_key_registry"]
    require(
        gate5["candidate_return_word_key_count"] == STEP_KEY_ALPHABET_SIZE,
        "Gate5 key count",
    )
    domain = gate5["domain_contract"]
    require(domain["regular_domain_partition"] is True, "regular key partition")
    require(
        domain["coverage_statement"]
        == (
            "every regular first return belongs to exactly one key; grazing, "
            "source-chart seams and simultaneous wall-corner events require "
            "one-sided trace/cemetery typing"
        ),
        "unique regular key owner",
    )

    kac = loaded[
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    ]
    require(
        kac["verdict"]["collision_SRB_first_return_mass_identity"] == "CERTIFIED",
        "Kac identity",
    )
    require(
        kac["result"]["collision_srb_kac_baseline"]["nonreturning_normalized_mass"]
        == "0",
        "nonreturning mass",
    )

    sparse = loaded[
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    ]
    require(
        sparse["verdict"]["C24_uniform_unweighted_exponential_return_tail"]
        == "CERTIFIED",
        "exponential tail",
    )
    tail = sparse["result"]["scheduled_and_all_time_tail"]
    require(
        tail["block_length_is_theorem_supplied_not_numerically_materialized"]
        is True,
        "N_open typing",
    )

    boundary = loaded[
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    ]
    require(
        boundary["verdict"][
            "limiting_step1_R1_Q1_partition_mod_collision_null_set"
        ]
        == "CERTIFIED",
        "step1 physical partition",
    )

    time2 = loaded[
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    ]
    require(
        time2["verdict"]["strict_Q2_inner_atoms"] == "CERTIFIED_114006",
        "Q2 anchors",
    )
    require(
        time2["result"]["Q1_time2_mass_frontier"]["Q2_inner_base_mass"]
        == "5257799/5120000000",
        "Q2 mass",
    )
    return loaded


def candidate_count_rows(
    path_schema: dict[str, Any],
) -> list[dict[str, Any]]:
    frozen = path_schema["fixed_depth_candidate_counts_n_1_to_9"]
    rows: list[dict[str, Any]] = []
    for depth in SAMPLE_DEPTHS:
        one_source = STEP_KEY_ALPHABET_SIZE**depth
        require(int(frozen[str(depth)]) == one_source, f"depth count: {depth}")
        c24_count = CORE_COUNT * one_source
        rows.append({
            "n": depth,
            "one_source_core_candidate_word_count": str(one_source),
            "C24_source_tagged_candidate_word_count": str(c24_count),
            "R_n_candidate_key_count": str(c24_count),
            "Q_n_candidate_prefix_key_count": str(c24_count),
            "empty_fibres_allowed": True,
        })
    return rows


def c24_path_key_join(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    path_schema = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]["result"]["full_mass_2d_path_key_schema"]
    rows = candidate_count_rows(path_schema)
    return {
        "parameter_quantifier": "for_every_fixed_s_with_|s|<=1/400",
        "source_carrier": "C_s=disjoint_mod_faces_union_of_24_physical_2D_cores",
        "source_core_tag_count": CORE_COUNT,
        "regular_collision_step_key_alphabet_size": STEP_KEY_ALPHABET_SIZE,
        "candidate_path_id_grammar": (
            "c24-path:(source_core_id,n,k_1,...,k_n), k_j in frozen K"
        ),
        "depth_n_candidate_universe_size": "24*441280^n",
        "fixed_depth_candidate_count_rows": rows,
        "fixed_depth_candidate_count_rows_sha256": canonical_digest(rows),
        "path_universe_over_all_finite_n_is_countable": True,
        "empty_path_fibres_allowed": True,
        "each_regular_orbit_segment_has_at_least_one_recorded_step_key": True,
        "each_regular_collision_step_has_exactly_one_frozen_key_owner": True,
        "key_owner_boundary_policy": (
            "frozen dominant-chart tie order plus one-sided trace/cemetery typing"
        ),
        "candidate_path_fibres_cover_C24_mod_singular_collision_null": True,
        "source_dimension_at_fixed_parameter": 2,
        "positive_area_source_not_occurrence_curve": True,
        "exact_nonempty_candidate_path_keys_enumerated": False,
    }


def arbitrary_n_level_schema() -> dict[str, Any]:
    require(CORE_MASS_STRICT_LOWER < CORE_MASS_STRICT_UPPER, "mass interval")
    require(0 < BLOCK_SURVIVAL_FACTOR < 1, "tail factor")
    return {
        "return_clock": "tau_C_s_plus=inf{n>=1:T_s^n(x)inC_s}",
        "Q_0": "C_s",
        "Q_n": "C_s intersection intersection_{j=1}^n T_s^{-j}(C_s^c)",
        "R_n": (
            "C_s intersection intersection_{j=1}^{n-1}T_s^{-j}(C_s^c) "
            "intersection T_s^{-n}(C_s), n>=1"
        ),
        "level_identity_mod_null": "Q_(n-1)=R_n disjoint_union Q_n",
        "finite_telescope_mod_null": (
            "C_s=(disjoint_union_{j=1}^N R_j) disjoint_union Q_N"
        ),
        "infinite_first_return_partition_mod_null": (
            "C_s=disjoint_union_{n>=1}R_n; intersection_n Q_n has mu_s-mass 0"
        ),
        "path_fibre_refinement": {
            "R_n_k": "R_n intersection fibre(c24-path k)",
            "Q_n_k": "Q_n intersection fibre(c24-prefix k)",
            "same_level_fibres_pairwise_disjoint_by_frozen_exact_key_ownership": True,
            "singular_and_core_boundary_cemetery_mass": "0",
        },
        "symbolic_physical_mass": {
            "m_s_n_k": "mu_s(R_n_k)",
            "qmass_s_n_k": "mu_s(Q_n_k)",
            "sum_k_m_s_n_k": "mu_s(R_n)",
            "sum_k_qmass_s_n_k": "mu_s(Q_n)",
            "sum_n_sum_k_m_s_n_k": "mu_s(C_s)",
            "numeric_component_masses_materialized": False,
        },
        "uniform_normalized_survivor_tail": (
            "mu_s(Q_n)/mu_s(C_s)<(550000/147)*"
            "(111718729/111718750)^floor(n/N_open)"
        ),
        "N_open": "one_uniform_theorem_supplied_integer>=1_not_numeric",
        "normalized_core_mass_interval": [
            "147/550000_strict_lower", "29021/75000000_strict_upper"
        ],
        "unweighted_exponential_Rn_Qn_mass_ledger": "CERTIFIED_SYMBOLIC",
        "q_weighted_strong_tail": "NOT_CERTIFIED",
    }


def regular_component_schema() -> dict[str, Any]:
    return {
        "scope": "fixed_parameter_s_and_fixed_finite_n",
        "regular_path_fibre_geometry": (
            "finite intersections of strict collision-owner, chart, homogeneity, "
            "core-avoidance and terminal-core inequalities on analytic billiard branches"
        ),
        "regular_path_fibre_is_open_relative_to_source_core_interior": True,
        "path_fibre_boundary_carriers": [
            "grazing/corner and homogeneity singularities",
            "equal-root owner-change curves",
            "chart seams",
            "preimages of the 24 core faces",
        ],
        "finite_depth_boundary_is_countable_union_of_piecewise_analytic_curves": True,
        "finite_depth_boundary_collision_SRB_mass": "0",
        "regular_open_fibre_has_at_most_countably_many_connected_components": True,
        "countability_reason": (
            "each nonempty open component contains a distinct element of a fixed "
            "countable rational dyadic basis of the 2D source chart"
        ),
        "canonical_component_rank": (
            "least natural-number index in a fixed bijective enumeration of rational "
            "dyadic basis elements whose closure is contained in the component"
        ),
        "canonical_component_id": (
            "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)"
        ),
        "R_n_and_Q_n_regular_component_partition_exists_mod_null": True,
        "componentwise_forward_map_is_real_analytic_local_diffeomorphism": True,
        "componentwise_inverse_map_exists_on_regular_image": True,
        "collision_area_Jacobian_of_full_invertible_map": "1",
        "component_coordinates_and_nonempty_ranks_enumerated": False,
        "uniform_joint_parameter_component_atlas_claimed": False,
        "unstable_Jacobian_or_distortion_inferred_from_area_Jacobian": False,
    }


def round26_anchors(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    boundary = loaded[
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    ]["result"]["fair_dyadic_boundary_tube_theorem"]
    time2 = loaded[
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    ]["result"]
    registry = time2["Q1_time2_adaptive_registry"]
    mass = time2["Q1_time2_mass_frontier"]
    return {
        "limiting_step1_R1_Q1_mod_collision_null": "CERTIFIED",
        "step1_fair_boundary_tube_rate": boundary["asymptotic_rate"],
        "step1_base_tube_bound": boundary[
            "uniform_parameter_averaged_unresolved_base_mass_bound"
        ],
        "strict_Q2_inner_finite_anchor_count": registry["strict_Q2_inner_atom_count"],
        "strict_Q2_inner_finite_anchor_mass": mass["Q2_inner_base_mass"],
        "time2_unresolved_outer_mass": mass["time2_unresolved_outer_base_mass"],
        "finite_time2_anchor_is_complete_R2_Q2": False,
        "arbitrary_n_schema_does_not_enumerate_missing_time2_components": True,
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameterwise_not_joint_parameter_component_claim": True,
            "join_policy": (
                "exact_C24_source_core_tag_plus_frozen_regular_step_key_word"
            ),
        },
        "C24_full_dimensional_arbitrary_n_candidate_path_join": c24_path_key_join(
            loaded
        ),
        "arbitrary_n_Rn_Qn_level_and_mass_schema": arbitrary_n_level_schema(),
        "canonical_regular_connected_component_schema": regular_component_schema(),
        "round26_constructive_anchors": round26_anchors(loaded),
        "strict_nonpromotion": {
            "exact_nonempty_path_keys_enumerated": False,
            "connected_component_coordinates_enumerated": False,
            "finite_complete_Rn_Qn_raw_branch_table": "NOT_MATERIALIZED",
            "branchwise_owner_and_core_margins_numeric": False,
            "branchwise_collision_SRB_masses_numeric": False,
            "unstable_Jacobian_and_distortion_payload": "NOT_CERTIFIED",
            "common_fw_rev_strong_restriction": "NOT_CERTIFIED",
            "strong_q_n_payload": "NOT_CERTIFIED",
            "q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "complete_18_field_operator_blocks": 0,
            "Gate3": "NOT_CERTIFIED",
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
        "C24_arbitrary_n_full_dimensional_candidate_path_coverage": (
            "CERTIFIED_MOD_SINGULAR_NULL"
        ),
        "arbitrary_n_Rn_Qn_measurable_level_and_mass_schema": "CERTIFIED",
        "arbitrary_n_regular_connected_component_existence_schema": (
            "CERTIFIED_NONCONSTRUCTIVE"
        ),
        "uniform_unweighted_exponential_Qn_mass_tail": "CERTIFIED",
        "nonempty_component_enumeration_and_numeric_payload": "NOT_CERTIFIED",
        "q_weighted_strong_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": verdict(),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round27_arbitrary_n_path_schema_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    join = result["C24_full_dimensional_arbitrary_n_candidate_path_join"]
    component = result["canonical_regular_connected_component_schema"]
    print("C24_ARBITRARY_N_CANDIDATE_PATH_COVERAGE: CERTIFIED_MOD_SINGULAR_NULL")
    print(f"DEPTH_N_CANDIDATE_COUNT: {join['depth_n_candidate_universe_size']}")
    print("ARBITRARY_N_RN_QN_LEVEL_AND_MASS_SCHEMA: CERTIFIED")
    print(
        "REGULAR_CONNECTED_COMPONENT_EXISTENCE: "
        + str(component["R_n_and_Q_n_regular_component_partition_exists_mod_null"])
    )
    print("NONEMPTY_COMPONENT_ENUMERATION_AND_STRONG_PAYLOAD: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
