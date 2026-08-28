#!/usr/bin/env python3
"""Round-60 Gate-4 physical-RN / good-bad / assembly frontier.

The certificate is append-only and starts from the frozen Round-59 Gate-4
manifest.  It records three exact upgrades without promoting Gate 4.

* The raw common landing is a positive submeasure of the physical induced
  landing law.  Hence it has a Borel RN marker and, on any *supplied*
  physical unstable disintegration, an exact same-measure Bayes formula.
* The Borel good/bad split gives a possibly-zero proper original-time
  *landing* subkernel on ``z_land<C_p`` and preserves the original killed
  first-hit predicate.  Source properness is not inferred, and the bad part
  cannot be discarded as a cemetery.
* Smooth exact product models show that even perfect qualitative fields
  1--4 do not imply the strict quantitative boundary field 5.

Physical product rectangles, stable holonomy, quantitative marker geometry,
the full boundary inequality and strong assembly remain unmaterialized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round60-physical-rn-good-bad-assembly-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
DEFAULT_REPORT = HERE / f"{PREFIX}-assault-2026-07-20.md"
DEFAULT_VERIFIER = HERE / "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_verifier.py"

DEPENDENCIES = {
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json":
        "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json":
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8",
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json":
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json":
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18",
}

PINNED_BASELINE_FILES = {
    "cm2-fifty-ninth-direct-assault-2026-07-20.md":
        "ec0623ec2fd6138c74d3707fd1c6f5e385b98187dcbd616cadee3b19e39dd5ef",
    "cm2-fifty-ninth-direct-assault-manifest-2026-07-20.sha256":
        "c013b5aa22db44308c7aa4cbe2b0800da14f709bcc80250464478b047cfc0712",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-assault-2026-07-20.md":
        "2f66b1aff6551e97729d27f06c87a32957ab21404c0fb0ee3cc0210fa578b468",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256":
        "967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_L = Q(2, 1) / (3 * C_P)
SHORT_Z = Q(1, 1) / SHORT_L
COMMON_MASS = Q(999, 1000)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1
FRAGMENTED_Z = Q(N_COMPONENTS, 1) / COMMON_MASS


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_q(value: str) -> Q:
    return Q(value)


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    d = 1
    while Q(1, 2**d) * z >= C_P / 2:
        d += 1
    return d


def load_inputs() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        data = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(data, dict), f"dependency root: {name}")
        loaded[name] = data

    for name, expected in PINNED_BASELINE_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"baseline path: {name}")
        require(path.resolve().parent == HERE, f"baseline scope: {name}")
        require(sha256_path(path) == expected, f"baseline hash: {name}")

    r59 = loaded[
        "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(
        r59["same_graph_rokhlin_reconditioning"]["status"]
        == "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE",
        "Round59 weak graph theorem",
    )
    require(r59["seven_field_materialization_audit"]["actual_complete_rows"] == "1/7", "Round59 fields")
    require(r59["strict_nonpromotion"]["Gate4"] == "NOT_CERTIFIED", "Round59 Gate4")

    r58 = loaded[
        "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(
        r58["maximal_component_minimum_Z_theorem"]["status"]
        == "CERTIFIED_MAXIMAL_COMPONENT_EXACT_MINIMUM_AND_UNSHIFTED_PROPERNESS_IFF",
        "Round58 properness iff",
    )
    require(
        r58["landing_bad_stratum_interface"]["dyadic_moment"].startswith("integral h(y)*2^D_land"),
        "Round58 bad moment",
    )

    r57 = loaded[
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    ]["result"]["raw_common_first_return_typing"]
    require(r57["status"] == "CERTIFIED_BUT_UNPROPER", "Round57 raw graph")
    require("exact positive common restriction" in r57["raw_domain"], "Round57 positive restriction")
    require("notin C_s" in r57["first_hit_semantics"], "Round57 first-hit kill")
    require("charged exactly once" in r57["charge"], "Round57 once charge")

    pal = loaded[
        "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
    ]["result"]
    require(
        "positive interval restriction" in pal["palindromic_stopped_cut_replay"]["density_and_domination"],
        "positive restriction domination",
    )
    require(
        "identical raw point restriction" in pal["physical_common_refinement_closure"]["same_raw_restriction"],
        "same raw restriction",
    )

    r56 = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]
    require(
        "(T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once"
        in r56["paired_leafwise_reverse_replay"]["induced_return_once_coverage"],
        "induced return invariance",
    )
    require(
        "dominated as the same positive measure"
        in r56["finite_static_source_natural_Z"]["controlled_initial_family_checks"][-1],
        "base positive domination",
    )

    r25 = loaded["cm2-gate2-round25-product-base-manifest-2026-07-18.json"]["result"]
    require(
        r25["exact_positive_cone_product_tile"]["affine_candidate_projection"]
        ["identified_with_physical_stable_holonomy_pi_s"] is False,
        "Round25 physical holonomy guard",
    )
    r49 = loaded[
        "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
    ]["result"]["incidence_safe_long_leaf_compact_core"]
    require(r49["incidence_safe_piece_count_per_leaf_upper"] == 153, "Round49 F")
    require(r49["object_scope"].startswith("conditional per admissible"), "Round49 scope")
    return loaded


def pinned_type_audit() -> dict[str, Any]:
    return {
        "Round59_complete_actual_rows": "1/7; only field 6, the tagged Borel branch inverse, is complete",
        "Round59_measure_typing": "for eta-almost every quotient value, graph/endpoints/tags hold Gamma_u-almost surely; no singleton normalization",
        "Round58_exact_threshold": "original-time landing is proper iff J_land,min(y)<C_p*h(y) on almost every positive physical fibre",
        "Round57_graph": "the same-ID raw graph is an exact positive once-charged first return at tau_cap=n but is unproper",
        "candidate_mismatch": "Round25 is an affine cone-product candidate, while Round49 F=153 belongs only to a conditional source compact core; neither is the actual common landing law",
        "status": "CERTIFIED_FROZEN_ROUND59_TYPE_BASELINE",
    }


def rn_marker_bridge() -> dict[str, Any]:
    return {
        "ambient_law": "let mu_C be the physical collision-SRB law restricted to C_s and let kappa_B be the unshifted common landing marginal",
        "positive_domination": "for every Borel A, kappa_B(A)=kappa_A(T_C_s^(-1)A)<=mu_C(T_C_s^(-1)A)=mu_C(A); the first inequality is the exact positive source restriction and the last equality is induced invariance, hence 0<=kappa_B<=mu_C",
        "RN_marker": "there is a Borel g_B=d kappa_B/d mu_C with 0<=g_B<=1 mu_C-almost everywhere",
        "supplied_physical_disintegration": "if, and only if supplied externally, mu_C=integral mu_u deta(u) is the physical unstable Rokhlin disintegration on actual landing plaques",
        "unnormalized_same_measure_formula": "m(u)=integral g_B dmu_u and tilde_kappa_u=g_B*mu_u give kappa_B=integral tilde_kappa_u deta(u)",
        "normalized_formula": "on {m>0}, eta_B=m*eta and kappa_u=(g_B/m(u))*mu_u give kappa_B=integral kappa_u deta_B(u)",
        "density_formula": "if dmu_u=rho_u ds on an actual unstable plaque, then d tilde_kappa_u/ds=g_B*rho_u; this is an exact formula, not a bound on support fragmentation, g_B, rho_u or log distortion",
        "zero_fibre_policy": "kappa_u is defined only eta_B-almost everywhere; values on {m=0} are arbitrary and carry no endpoint/tag/normalization claim",
        "graph_semantics": "after pulling through the Round59 tagged inverse, source/landing/n/path/ID/owner identities remain Gamma_u-almost surely for eta_B-almost every u",
        "singleton_guard": "m(u) is a conditional integral, never eta({u}); eta may be nonatomic",
        "field4_effect": "actual RN marker plus an exact Bayes formula is certified, but the physical unstable quotient and quantitative same-measure density/distortion bounds are not",
        "status": "CERTIFIED_ACTUAL_RN_MARKER_AND_CONDITIONAL_SAME_MEASURE_BAYES_FORMULA__FIELD4_PARTIAL_ONLY",
    }


def product_separators() -> dict[str, Any]:
    require(SHORT_Z == Q(3, 2) * C_P, "short plaque z")
    require(C_P < SHORT_Z < 2 * C_P, "short plaque range")
    require(defect_depth(SHORT_Z) == 2, "short plaque depth")
    require(Q(N_COMPONENTS - 1) <= C_P < Q(N_COMPONENTS), "ceiling")
    require(C_P < FRAGMENTED_Z < 2 * C_P, "fragmented range")
    require(defect_depth(FRAGMENTED_Z) == 2, "fragmented depth")
    rows = [
        {
            "model": "short_full_plaque",
            "rectangle_count": 1,
            "unstable_plaque_length_L": qstr(SHORT_L),
            "stable_projection": "vertical identity-coordinate projection",
            "two_sided_holonomy_RN_Jacobian": "1",
            "F": 1,
            "theta": "1",
            "R": "1",
            "density": "constant 1/L, log distortion 0",
            "h": "1",
            "J": qstr(SHORT_Z),
            "normalized_boundary": qstr(SHORT_Z),
            "F_R_over_theta_L": qstr(SHORT_Z),
            "D_land": 2,
            "good_fibre": False,
        },
        {
            "model": "unit_plaque_many_gaps",
            "rectangle_count": 1,
            "unstable_plaque_length_L": "1",
            "stable_projection": "vertical identity-coordinate projection",
            "two_sided_holonomy_RN_Jacobian": "1",
            "F": str(N_COMPONENTS),
            "theta": qstr(COMMON_MASS),
            "R": "1",
            "density": "constant 1 on the retained components, log distortion 0",
            "h": qstr(COMMON_MASS),
            "J": str(N_COMPONENTS),
            "normalized_boundary": qstr(FRAGMENTED_Z),
            "F_R_over_theta_L": qstr(FRAGMENTED_Z),
            "D_land": 2,
            "good_fibre": False,
        },
    ]
    return {
        "scope": "exact smooth product identity-return nonimplication models; not asserted to occur in the billiard",
        "common_geometry": "one Euclidean product rectangle, horizontal physical unstable plaques, vertical stable plaques, identity first return and exact branch inverse",
        "rows": rows,
        "rows_sha256": digest(rows),
        "conclusion": "even perfect qualitative fields 1--4, exact field 6 and finite boundary assembly do not imply field 5; short plaque span and marker fragmentation are independent quantitative debts",
        "status": "CERTIFIED_FIELDS_1_TO_4_QUALITATIVELY_PERFECT_DO_NOT_IMPLY_PHYSICAL_BOUNDARY_THRESHOLD",
    }


def field_audit() -> dict[str, Any]:
    rows = [
        {"field": 1, "name": "physical product-rectangle cover of actual common landing", "actual": "NOT_CERTIFIED"},
        {"field": 2, "name": "stable projection and two-sided Borel holonomy Jacobian", "actual": "NOT_CERTIFIED"},
        {"field": 3, "name": "full-span or quantitative common fragmentation", "actual": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-measure unstable conditionals with density/log distortion", "actual": "PARTIAL_RN_MARKER_AND_BAYES_FORMULA_ONLY__PHYSICAL_QUOTIENT_AND_BOUNDS_ABSENT"},
        {"field": 5, "name": "physical boundary charge strictly below C_p", "actual": "NOT_CERTIFIED"},
        {"field": 6, "name": "Borel branch inverse retaining n/path/ID/owner", "actual": "CERTIFIED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "actual": "NOT_CERTIFIED__CONDITIONAL_STANDARD_FAMILY_CATEGORY_ONLY"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "actual_complete_rows": "1/7",
        "partial_rows": [4, 7],
        "official_Gate2_fields_unchanged": "0/17",
        "shortest_remaining_join": "supply actual physical rectangles/projection and plaque conditionals, prove the marker geometry bound F*R<C_p*theta*L almost everywhere, and instantiate exact strong assembly on the same graph law",
        "status": "CERTIFIED_FIELDS_1_TO_4_FULL_AUDIT__RN_FORMULA_PARTIAL_ONLY__ACTUAL_JOIN_STILL_ONE_OF_SEVEN",
    }


def good_bad_split() -> dict[str, Any]:
    return {
        "sets": "G={y:h(y)>0 and z_land(y)<C_p}; B={y:h(y)>0 and z_land(y)>=C_p}; empty fibres are neither normalized nor charged",
        "Borel": "h and J_land,min are Borel, hence G and B are Borel and Gamma_cap=Gamma_G+Gamma_B exactly",
        "good_subkernel": "Gamma_G has a possibly-zero proper physical same-ID landing family on the exact first-return graph at the original time n; physical source properness and hence the full kernel are not inferred",
        "good_killed_semantics": "on Gamma_G, T_s^j(source) notin C_s for 1<=j<n and T_s^n(source) in C_s; this is inherited from the raw R_n graph without an added clock",
        "measure_typing": "under any Round59 reconditioning these identities hold Gamma_u-almost surely for eta-almost every u, not pointwise on null fibres",
        "good_mass_positive": "NOT_CERTIFIED; finite J_land,min,total alone permits G to be empty",
        "bad_mass_zero": "NOT_CERTIFIED; the k=0 Markov estimate is finite, not zero",
        "bad_dyadic_moment": "integral_B h*2^D_land is finite by restriction of the pinned Round58 full moment",
        "all_bad_separator": "the short-full-plaque product model has G empty, B full mass, D_land=2 and integral_B h*2^D_land=4",
        "status": "CERTIFIED_EXACT_GOOD_BAD_GRAPH_SPLIT_AND_POSSIBLY_ZERO_PROPER_GOOD_LANDING_SUBKERNEL__SOURCE_AND_BAD_PART_UNPAID",
    }


def positive_defect_interface() -> dict[str, Any]:
    rows = [
        {"index": 1, "required": "a positive linear endpoint-preserving embedding E_B of Gamma_B into a declared defect/cemetery strong space", "current": "NOT_CERTIFIED"},
        {"index": 2, "required": "no fibre normalization; n/path/ID/owner and one parent charge retained Gamma_B-almost surely", "current": "GRAPH_TAGS_CERTIFIED_WEAKLY__STRONG_EMBEDDING_ABSENT"},
        {"index": 3, "required": "a norm inequality ||E_B Gamma_B||_cem <= C*integral_B h*2^D_land (or a stronger same-law q/current bound)", "current": "NOT_CERTIFIED"},
        {"index": 4, "required": "an exact operator/current identity Full=Good+inclusion_cem(E_B Gamma_B), never deletion or latent D_cap endpoint replacement", "current": "NOT_CERTIFIED"},
        {"index": 5, "required": "a downstream CM2 theorem accepting that positive remainder with the required summability or vanishing conclusion", "current": "NOT_CERTIFIED"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "collision_null_guard": "Gamma_B may have positive ordinary collision-SRB mass and is not part of the frozen null singular cemetery",
        "moment_guard": "finite integral_B h*2^D_land is only a scalar moment; without row 3 it is not a strong trace/current norm",
        "exactness_guard": "if the CM2 contract requires one proper full physical common landing, a positive Gamma_B cannot be hidden or discarded; the all-bad separator would otherwise delete the entire regular identity graph",
        "status": "CERTIFIED_CONDITIONAL_POSITIVE_DEFECT_ROUTE_WITH_FIVE_MISSING_INTERFACES__NO_CURRENT_HYBRID_CLOSURE",
    }


def literature_audit() -> dict[str, Any]:
    return {
        "checked_on": "2026-07-20",
        "official_source": "arXiv:2604.19671v2, Giovanni Canestrari, Linear response for Sinai billiards with small holes",
        "official_pdf_sha256_checked": "fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004",
        "Proposition_4_4": "an already initial (omega1,B1,D1)-standard family evolves under the normalized small-hole conditional dynamics to some regular (omega2,B2,D2)-standard family",
        "Section_6_2": "canonical connected-component evolution gives exact equality of represented measures for the closed, added-discontinuity and normalized surviving evolutions",
        "conditioning_guard": "Lemma 6.17 divides the boundary by total surviving mass and Lemma 6.29 divides by the selected conditioned mass; arbitrary thin marker restrictions therefore receive no uniform free bound",
        "quantitative_guard": "B2 is qualitative and depends on B1 and the table; no explicit B2<C_p or F*R<C_p*theta*L is proved",
        "measure_guard": "the paper's vertical hole-line law and small-hole survivor law are not the actual CM2 common landing restriction",
        "strong_space_guard": "the introduction explicitly states that no known Banach spaces for general piecewise hyperbolic systems contain standard pairs; C1-test coupling is not the requested strong operator assembly",
        "conditional_value": "once an exact initial regular standard-family carrier with the required boundary and density data is independently supplied, the paper supports a canonical standard-family evolution/reassembly subinterface",
        "external_theorem_promoted": False,
        "status": "AUDITED_CONDITIONAL_STANDARD_FAMILY_CATEGORY_SUBINTERFACE__FIELD7_ACTUAL_STRONG_ASSEMBLY_NOT_SUPPLIED",
    }


def downstream_join() -> dict[str, Any]:
    return {
        "whole_graph_condition": "if a future proof establishes the full original-time physical landing proper on the same graph law, no new recovery collision is needed",
        "killed_C24_join": "the original R_n predicate then gives the exact killed first-return factor product_{j=1}^{n-1}1_{C_s^c}(T_s^j x)*1_{C_s}(T_s^n x)=1 on the proper graph",
        "typing": "after Rokhlin reconditioning the killed identity is Gamma_u-almost sure for eta-almost every u; endpoints and n/path/ID/owner remain unchanged",
        "current_actual_scope": "the same killed identity is actual on the possibly-zero good landing subgraph Gamma_G only; source properness is not inferred and it does not dispose of Gamma_B",
        "later_clocks": "moments of every later or repeated recovery clock remain independent; fixed Dbar/D_cap/D_land moments do not imply an all-stage moment",
        "physical_q": "proper first return would still need same-ID numerical C_fw/C_rev and a survivor-conditioned or global L^(6/5) first-return charge envelope before defining physical q",
        "strong_cemetery": "collision-null weak mass and finite absolutely-continuous moments do not supply the singular/current strong cemetery",
        "status": "CERTIFIED_CONDITIONAL_ORIGINAL_RN_KILLED_JOIN__LATER_CLOCK_Q_AND_STRONG_CEMETERY_REMAIN_SEPARATE",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "actual_landing_RN_marker": "CERTIFIED",
        "same_measure_conditional_Bayes_formula": "CERTIFIED_ON_ANY_SUPPLIED_PHYSICAL_DISINTEGRATION",
        "seven_field_physical_landing_join": "1/7_ACTUAL_COMPLETE__FIELD4_AND_FIELD7_PARTIAL_ONLY",
        "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
        "good_original_time_proper_landing_subkernel": "CERTIFIED_POSSIBLY_ZERO__SOURCE_PROPERNESS_NOT_INFERRED",
        "good_subkernel_positive_mass": "NOT_CERTIFIED",
        "bad_landing_mass_zero": "NOT_CERTIFIED",
        "positive_bad_defect_cemetery_route": "CONDITIONAL_FIVE_INTERFACES_MISSING",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
        "full_proper_graph_killed_C24_join": "CERTIFIED_CONDITIONAL",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_inputs()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "baseline_file_sha256": dict(PINNED_BASELINE_FILES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "actual RN marker bridge, exact good/bad split, perfect-product nonimplications, conditional field7 and downstream joins",
            "external_theorem_promoted": False,
        },
        "pinned_round59_type_audit": pinned_type_audit(),
        "actual_landing_RN_marker_bridge": rn_marker_bridge(),
        "perfect_product_fields_1_to_4_nonimplication": product_separators(),
        "seven_field_materialization_audit": field_audit(),
        "good_bad_original_time_graph_split": good_bad_split(),
        "positive_bad_defect_cemetery_interface": positive_defect_interface(),
        "latest_field7_literature_audit": literature_audit(),
        "downstream_original_killed_join": downstream_join(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier outside deliverables")
    require(DEFAULT_REPORT.is_file() and not DEFAULT_REPORT.is_symlink(), "report path")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(DEPENDENCIES),
        "baseline_files": dict(PINNED_BASELINE_FILES),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def encoded_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    args = parser.parse_args()
    try:
        payload = encoded_manifest(args.verifier)
        if args.manifest_json:
            print(payload, end="")
            return 0
        if args.write_manifest:
            DEFAULT_MANIFEST.write_text(payload, encoding="utf-8")
            print(f"WROTE: {DEFAULT_MANIFEST}")
            return 0
    except (OSError, RuntimeError, ValueError, KeyError, TypeError) as exc:
        print(f"ROUND60_GATE4_RN_CERT_FAILURE: {exc}")
        return 1

    strict = build_result()["strict_nonpromotion"]
    print("ACTUAL_RN_MARKER:", strict["actual_landing_RN_marker"])
    print("SEVEN_FIELD_JOIN:", strict["seven_field_physical_landing_join"])
    print("PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
