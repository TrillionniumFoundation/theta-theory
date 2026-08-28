#!/usr/bin/env python3
"""Round-50 fixed-parameter enlarged-cover target-adjunction certificate.

Round 49 correctly left a gap between two qualitative facts: a positive
Cantor rectangle can be placed inside an open C24 core, while Proposition
3.19 of Climenhaga--Day only names targets in its own sufficient cover.  The
proof of Proposition 3.19 is stable under adjoining one further positive
target rectangle and selecting a separate uniformly dense positive subset
inside it.  The target rectangle itself is not asserted to satisfy the
global 0.9 condition imposed on the published source cover.  This certificate
freezes that fixed-map target-adjunction argument and the pointwise conjugacy
back to the reference map.

The argument is qualitative.  Compactness, Lebesgue density and Liouville
mixing expose neither a finite rectangle table nor a numerical iterate or
source-subcurve mass.  Nothing here promotes a parameter-uniform H_cover,
actual beta, C_fw/C_rev, q, cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round50-same-cover-target-adjunction.v2"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json": (
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18"
    ),
}

ARXIV_2604_SOURCE_SHA256 = (
    "b8f79a99f5f98648f91848cd7b4e489846f4512d6ed35ebd042229da3c89ee94"
)
ARXIV_1807_SOURCE_SHA256 = (
    "c1e0189b271fdd1303b425d096a9e1d8685a83f74d139b37a534a0530a6020aa"
)

DIRECT_REQUIRED_FRACTION = Q(2688, 893303125)
WDIAG_REQUIRED_FRACTION = Q(7372800000, 10389446755961)
SAFE_FAMILY_MASS = Q(1999, 32000)
DIRECT_HIT_GAP = Q(21, 111718750)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependency() -> dict[str, Any]:
    prior = load_json(next(iter(DEPENDENCIES)))
    result = prior["result"]
    core = result["incidence_safe_long_leaf_compact_core"]
    ledger = result["exact_remaining_cover_thresholds"]
    tech = result["latest_sufficient_rectangles_interface"]
    if core["status"] != (
        "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY_NUMERIC_COMPACT_CORE"
    ):
        raise RuntimeError("Round49 compact-core scope")
    if Q(core["incidence_safe_family_mass_strict_lower"]) != SAFE_FAMILY_MASS:
        raise RuntimeError("Round49 safe family mass")
    if Q(ledger["incidence_safe_required_direct_C24_fraction"]) != (
        DIRECT_REQUIRED_FRACTION
    ):
        raise RuntimeError("Round49 direct threshold")
    if Q(ledger["incidence_safe_required_Wdiag_fraction"]) != (
        WDIAG_REQUIRED_FRACTION
    ):
        raise RuntimeError("Round49 Wdiag threshold")
    if Q(ledger["direct_C24_hit_gap"]) != DIRECT_HIT_GAP:
        raise RuntimeError("Round49 hit gap")
    if tech["same_cover_bridge_installed"] is not False:
        raise RuntimeError("Round49 same-cover state")
    if tech["numeric_H_cover"] is not None:
        raise RuntimeError("Round49 H overclaim")
    if tech["numeric_actual_beta_Wdiag"] is not None:
        raise RuntimeError("Round49 beta overclaim")
    if result["strict_nonpromotion"]["Gate4"] != "NOT_CERTIFIED":
        raise RuntimeError("Round49 Gate4")
    return result


def literature_rows() -> list[dict[str, Any]]:
    return [
        {
            "paper": "Climenhaga--Day, arXiv:2604.25881v1",
            "official_source_sha256": ARXIV_2604_SOURCE_SHA256,
            "source_anchor": "Proposition 3.19 and proof sketch, source lines 1568--1586",
            "frozen_fact": (
                "for one fixed finite-horizon Sinai billiard, the authors first choose a countable high-density Cantor cover; for every delta and target R0 in that cover, compactness gives finitely many proper-crossing source rectangles and Liouville mixing gives one finite iterate N for all admissible u-curves at that scale"
            ),
            "effectivity": "qualitative only",
        },
        {
            "paper": "Baladi--Demers, arXiv:1807.02330v4",
            "official_source_sha256": ARXIV_1807_SOURCE_SHA256,
            "source_anchor": (
                "Definitions at source lines 2430--2468; cover construction 3914--3944; open-target rectangle 4067--4096"
            ),
            "frozen_fact": (
                "for a fixed billiard, a regular open set contains a positive Liouville Cantor rectangle whose solid hull stays in the open set; these lines do not assert that this target rectangle itself satisfies the global 0.9 cover condition"
            ),
            "effectivity": "qualitative only",
        },
        {
            "paper": "Baladi--Demers proof mechanism used by Proposition 3.19",
            "official_source_sha256": ARXIV_1807_SOURCE_SHA256,
            "source_anchor": "source lines 2508--2533",
            "frozen_fact": (
                "inside a positive target rectangle, leafwise Lebesgue differentiation and absolute continuity select a separate positive uniformly-dense subset in the required orientation; for a finite proper-crossing source family, Liouville mixing then gives a common finite time and the crossing lemma extracts a target-crossing subcurve"
            ),
            "effectivity": "no numerical time or subcurve width",
        },
    ]


def fixed_s_adjunction(delta_rect: str) -> dict[str, Any]:
    steps = [
        {
            "step": 1,
            "claim": (
                "fix s and write T_s=A_s^{-1} hat_T_s A_s; compactness and the diffeomorphism property give m_s=inf_x sigma_min(DA_s(x))>0, so every reference admissible u-curve V with length at least delta_rect maps to a physical admissible u-curve A_s(V) with length at least hat_delta_s=m_s*delta_rect>0"
            ),
        },
        {
            "step": 2,
            "claim": (
                "map the closure-contained direct-C24 open core O_s to hat_O_s=A_s(O_s), and inside hat_O_s choose a positive locally maximal Cantor rectangle hat_R_* with D(hat_R_*) subset hat_O_s"
            ),
        },
        {
            "step": 3,
            "claim": (
                "inside hat_R_* select a separate positive uniformly-dense subset hat_P_* in the leaf orientation required by the forward unstable-curve crossing argument; no global 0.9 condition is claimed for hat_R_* itself"
            ),
        },
        {
            "step": 4,
            "claim": (
                "adjoin hat_R_* to the published physical countable cover and retain, at the positive scale hat_delta_s, the original finite proper-crossing source subcover; the enlarged cover remains countable and covers the physical regular set"
            ),
        },
        {
            "step": 5,
            "claim": (
                "Liouville mixing for the finitely many original-source/hat_P_* pairs gives one finite N_s; the published crossing argument gives, in every physical admissible u-curve of length at least hat_delta_s, a subcurve whose hat_T_s^N_s image crosses hat_R_*"
            ),
        },
        {
            "step": 6,
            "claim": (
                "pull the enlarged cover, target rectangle and crossing subcurve back by A_s^{-1}; crossing is preserved by conjugacy and D(A_s^{-1}hat_R_*) lies in O_s subset C24, yielding the fixed-s T_s target hit for every reference admissible u-curve of length at least delta_rect"
            ),
        },
    ]
    return {
        "scope": (
            "one fixed parameter s; Proposition 3.19 is applied to the physical finite-horizon billiard hat_T_s and pulled back to T_s=A_s^{-1}hat_T_s A_s; no parameter-uniform statement"
        ),
        "admissible_curve_scope": (
            "V belongs to the pulled-back class A_s^{-1}(hat_V_s^u) of admissible physical u-curves; no claim is made for arbitrary curves outside that class"
        ),
        "numeric_input_delta_rect": delta_rect,
        "pointwise_conjugacy_lower_length_factor_m_s_positive": True,
        "physical_input_scale": "hat_delta_s=m_s*delta_rect>0",
        "numeric_m_s": None,
        "numeric_physical_input_scale": None,
        "target": "one closure-contained direct-C24 open core O_s",
        "target_rectangle": (
            "positive locally maximal physical Cantor rectangle hat_R_* with D(hat_R_*) subset A_s(O_s), pulled back to a target rectangle inside O_s"
        ),
        "target_rectangle_itself_global_point9_claimed": False,
        "uniformly_dense_target_subset": (
            "a separate positive hat_P_* subset hat_R_* with the required oriented short-leaf 0.9 density property"
        ),
        "cover_operation": (
            "enlarge/adjoin: hat_R_prime=hat_R_union_{set}{hat_R_*}, then pull back by A_s^{-1}"
        ),
        "proof_steps": steps,
        "proof_steps_sha256": digest(steps),
        "enlarged_cover_bridge_installed_fixed_s": True,
        "fixed_s_finite_target_hit_iterate_exists": True,
        "target_crossing_implies_C24_entry": True,
        "numeric_target_rectangle_coordinates": None,
        "numeric_finite_source_cover_rows": None,
        "numeric_N_s": None,
        "numeric_source_subcurve_fraction": None,
        "physical_whole_family_join_installed": False,
        "status": "CERTIFIED_FIXED_S_QUALITATIVE_ENLARGED_COVER_ADJUNCTION",
    }


def effectivity_frontier() -> dict[str, Any]:
    missing = [
        {
            "id": "K_rect",
            "meaning": "cardinality and coordinates of the finite proper-crossing physical source subcover at hat_delta_s=m_s*delta_rect",
            "published_value": None,
        },
        {
            "id": "m_conjugacy",
            "meaning": "numerical lower length factor for A_s, and a parameter-uniform version if a common numerical atlas is sought",
            "published_value": None,
        },
        {
            "id": "m_rect",
            "meaning": "positive numerical Liouville masses of all source rectangles and the target dense set P_*",
            "published_value": None,
        },
        {
            "id": "delta_density",
            "meaning": "uniform density radius obtained from the Lebesgue-density step",
            "published_value": None,
        },
        {
            "id": "C_mix_theta_mix",
            "meaning": "effective correlation constants applicable to the rectangle/dense-set indicators",
            "published_value": None,
        },
        {
            "id": "N_mix",
            "meaning": "first iterate making every finite source-target Liouville intersection positive",
            "published_value": None,
        },
        {
            "id": "r_transverse",
            "meaning": "numerical transverse-intersection margin used by the crossing lemma",
            "published_value": None,
        },
        {
            "id": "J_branch",
            "meaning": "branchwise inverse-Jacobian/distortion conversion from target crossing width to source mass",
            "published_value": None,
        },
        {
            "id": "omega_parameter",
            "meaning": "robustness modulus identifying the source/target rows and their margins over all |s|<=1/400",
            "published_value": None,
        },
    ]
    assert SAFE_FAMILY_MASS * DIRECT_REQUIRED_FRACTION == DIRECT_HIT_GAP
    assert Q(1, 332330) > DIRECT_REQUIRED_FRACTION > Q(1, 332331)
    return {
        "missing_numeric_constants": missing,
        "missing_numeric_constants_sha256": digest(missing),
        "direct_C24_required_per_safe_leaf_source_fraction": str(
            DIRECT_REQUIRED_FRACTION
        ),
        "safe_reciprocal": "1/332330",
        "next_reciprocal_fails": "1/332331",
        "incidence_safe_family_mass": str(SAFE_FAMILY_MASS),
        "conditional_direct_hit_product": (
            "(1999/32000)*(2688/893303125)=21/111718750"
        ),
        "actual_source_fraction_from_theorem": None,
        "strict_inferable_uniform_source_fraction_lower": "0",
        "numeric_uniform_H_cover": None,
        "numeric_actual_beta": None,
        "strict_inferable_uniform_beta_lower": "0",
        "why_positivity_is_insufficient": (
            "mixing positivity can be carried by arbitrarily thin crossing subcurves; the cited proof supplies no quantitative transverse ball or source-mass width"
        ),
        "status": "CERTIFIED_EXACT_EFFECTIVITY_FRONTIER_NO_NUMERIC_PROMOTION",
    }


def parameter_frontier() -> dict[str, Any]:
    return {
        "parameter_window": "|s|<=1/400",
        "published_theorem_quantifier": "one fixed physical billiard map hat_T_s",
        "pointwise_fixed_s_enlarged_cover_bridge": "CERTIFIED",
        "pointwise_conjugacy_factor_m_s_positive": True,
        "numeric_uniform_conjugacy_lower_factor": None,
        "common_target_rectangle_registry_over_s": "NOT_CERTIFIED",
        "common_finite_source_cover_rows_over_s": "NOT_CERTIFIED",
        "branch_persistence_and_crossing_margin_over_s": "NOT_CERTIFIED",
        "uniform_Liouville_mixing_constants_over_s": "NOT_CERTIFIED",
        "uniform_integer_N": None,
        "compactness_of_parameter_interval_alone_is_sufficient": False,
        "reason": (
            "one must first quantify the conjugacy length factor and prove an open parameter-neighborhood on which the labelled rectangle branches, proper-crossing margins, singularity avoidance and one mixing/crossing construction persist; no such numerical modulus is present"
        ),
        "status": "POINTWISE_QUALITATIVE_ONLY",
    }


def build_result() -> dict[str, Any]:
    prior = validate_dependency()
    delta_rect = prior["latest_sufficient_rectangles_interface"][
        "numeric_input_delta_rect"
    ]
    rows = literature_rows()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "official_sources_retrieved": [
                "arXiv:2604.25881v1",
                "arXiv:1807.02330v4",
            ],
            "claim_type": (
                "fixed-parameter qualitative enlarged-cover target adjunction, pointwise conjugacy pullback and exact numerical effectivity frontier"
            ),
        },
        "literature_audit": {
            "rows": rows,
            "rows_sha256": digest(rows),
            "enlarged_cover_adjunction_is_a_derived_lemma": True,
            "not_a_verbatim_numbered_theorem": True,
        },
        "fixed_parameter_enlarged_cover_target_adjunction": fixed_s_adjunction(
            delta_rect
        ),
        "numerical_effectivity_frontier": effectivity_frontier(),
        "parameter_window_frontier": parameter_frontier(),
        "corrected_frontier": {
            "fixed_s_qualitative_C24_target_hit": "CERTIFIED",
            "fixed_s_target_in_enlarged_sufficient_cover": "CERTIFIED_BY_ADJUNCTION",
            "fixed_s_finite_H_exists_but_is_not_numerical": True,
            "uniform_parameter_window_numeric_rectangle_atlas": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_actual_beta": None,
            "physical_whole_family_grouping": "NOT_CERTIFIED",
            "same_ID_two_orientation_cover": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "fixed_s_qualitative_enlarged_cover_bridge": "CERTIFIED",
            "uniform_numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
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
        "dependencies": DEPENDENCIES,
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
        default=HERE / "cm2_gate34_round50_same_cover_target_adjunction_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    if args.summary:
        bridge = result["fixed_parameter_enlarged_cover_target_adjunction"]
        frontier = result["numerical_effectivity_frontier"]
        print(f"FIXED_S_ENLARGED_COVER: {bridge['status']}")
        print(f"NUMERIC_H_COVER: {frontier['numeric_uniform_H_cover']}")
        print(f"STRICT_BETA_LOWER: {frontier['strict_inferable_uniform_beta_lower']}")
        print("GATE4: NOT_CERTIFIED")
        print("CM2: NO-GO_FOR_CLAIM")
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
