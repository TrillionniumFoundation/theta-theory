#!/usr/bin/env python3
"""Round-58 Gate-4 unshifted-landing minimal-Z frontier.

Round 57 constructs an exact same-ID physical first-return graph whose source
and landing marginals have finite adapted boundary functional, but it does not
prove that the unshifted landing is proper.  This append-only leaf proves the
sharp same-time representation theorem: within an immutable physical carrier
ID, the maximal connected positive components minimize ``Z`` among every
exact positive canonical representation.  Hence unshifted properness is
equivalent to one strict threshold and cannot be repaired by more cuts,
proof tags, or legal coarsening.

The leaf also supplies a finite high-common-mass separator in which the full
induced return is proper and the Round-57 reference ``D_cap`` is zero while
the exact physical first-return landing is improper.  Finally it types the
strongest legal first-hit/reinduction object.  No recovery time is appended
to the original first return, and no reference graph is promoted to a
physical kernel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round58-unshifted-landing-minimal-z-first-hit-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE
    / "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json": (
        "275022bb78748941339bc27de022830346ebb220188d97b3bfa886af42049bfb"
    ),
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json": (
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414"
    ),
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json": (
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8"
    ),
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json": (
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424"
    ),
}

PINNED_REPORTS = {
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-assault-2026-07-20.md": (
        "33cec817b1c809278353e12f18de7e94224523e1bd7a6c011ab62276fd32d489"
    ),
}

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
GAP_MASS = Q(1, 1000)
COMMON_LOWER = Q(249, 250)
HIT_LOWER = Q(21, 111718750)
HIT_UPPER = Q(1, 500)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1
COMPONENT_LENGTH = COMMON_MASS / N_COMPONENTS
GAP_LENGTH = GAP_MASS / (N_COMPONENTS - 1)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


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
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    for name, expected in PINNED_REPORTS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"report path: {name}")
        require(path.resolve().parent == HERE, f"report scope: {name}")
        require(sha256_path(path) == expected, f"report hash: {name}")
        text = path.read_text(encoding="utf-8")
        require(
            "E_fw,total=(T_C_s)_#(mu_s|C_s)=mu_s|C_s" in text,
            "Round56 full induced output identity",
        )

    r41 = loaded[
        "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
    ]["result"]
    growth41 = r41["aggregate_canonical_Z_resolvent"]
    require(
        growth41["input"].startswith("a controlled canonical finite-Z"),
        "Round41 finite-Z input",
    )
    require(
        growth41["physical_aggregate_Z_weighted_tail"]
        == "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES",
        "Round41 weighted resolvent",
    )

    r42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    require(
        r42["numerical_C24_killed_Growth"]["hereditary_under_positive_C24_killing"]
        is True,
        "Round42 hereditary positive killing",
    )

    r51 = loaded[
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    ]["result"]
    view51 = r51["physical_two_proper_view_object_lemma"]
    require(
        view51["status"]
        == "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM",
        "Round51 proper views",
    )
    require(view51["raw_geometry_is_proper"] is False, "Round51 raw guard")

    r55 = loaded[
        "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json"
    ]["result"]
    terminal55 = r55["two_orientation_coarse_terminal_Z_join"]
    require(
        terminal55["status"]
        == "CERTIFIED_TWO_ORIENTATION_COARSE_TERMINAL_Z_L1_FINITE_NONNUMERIC_N_OPEN",
        "Round55 terminal Z",
    )

    r56 = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]
    source56 = r56["metric_and_once_charge_terminal_source_join"]
    require("mu_s|C_s exactly once" in source56["coarse_source_family"], "Round56 full source")
    require(
        r56["hereditary_replay_and_image_recut_join"]["physical_J_pair"]
        == "CERTIFIED_FINITE",
        "Round56 J_pair",
    )

    r57cap = loaded[
        "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
    ]["result"]
    closure57 = r57cap["physical_common_refinement_closure"]
    require(
        closure57["status"]
        == "CERTIFIED_PHYSICAL_COMMON_REFINEMENT_J_CAP_AND_SINGLE_D_CAP_CLOCK",
        "Round57 Jcap",
    )
    require(
        closure57["physical_maximal_component_registry"].startswith(
            "within each fixed y, view and physical carrier chart"
        ),
        "Round57 maximal components",
    )
    require(
        r57cap["strict_nonpromotion"]["physical_proper_same_ID_first_return_kernel"]
        == "NOT_CERTIFIED",
        "Round57 kernel boundary",
    )

    r57return = loaded[
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    raw57 = r57return["raw_common_first_return_typing"]
    require(raw57["status"] == "CERTIFIED_BUT_UNPROPER", "Round57 raw graph")
    require(raw57["landing_finite_Z"].startswith("CERTIFIED"), "Round57 landing Z")
    require(raw57["unshifted_landing_proper"] == "NOT_CERTIFIED", "Round57 landing guard")
    return loaded


def separator_sample_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in (0, 1, N_COMPONENTS - 2, N_COMPONENTS - 1):
        rows.append(
            {
                "component_index": str(index),
                "component_mass": qstr(COMPONENT_LENGTH),
                "component_length": qstr(COMPONENT_LENGTH),
                "component_Z": "1",
                "has_gap_after": index < N_COMPONENTS - 1,
                "gap_length_if_present": qstr(GAP_LENGTH) if index < N_COMPONENTS - 1 else "0",
            }
        )
    return rows


def reinduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "induced_occurrence": occurrence,
            "first_return_time_from_current_C_s_source": 1,
            "physical_component_count": str(N_COMPONENTS),
            "landing_J_min": str(N_COMPONENTS),
            "landing_normalized_Z_min": qstr(Q(N_COMPONENTS) / COMMON_MASS),
            "landing_is_proper": False,
        }
        for occurrence in range(1, 5)
    ]


def pinned_input_audit() -> dict[str, Any]:
    return {
        "Round56_full_induced_output": "E_fw,total=(T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once, with the frozen finite-Z canonical replay",
        "Round57_physical_graph": "Gamma_cap=(id,T_s^n)_#kappa_cap is the exact same-ID C_s first-return graph and its physical landing has finite Z",
        "Round57_reference_result": "J_cap,total and the D_cap moment are finite and produce one proper once-charged two-view reference carrier",
        "type_gap": "neither the full ambient induced output nor the proper reference carrier proves that the marked common physical landing restriction is proper",
        "status": "CERTIFIED_PINNED_INPUT_TYPE_AUDIT",
    }


def maximal_component_minimum_Z() -> dict[str, Any]:
    return {
        "registry_scope": "fix one immutable (y, physical landing carrier chart, physical restriction ID); remove singular, null and cemetery punctures and use the maximal connected positive components C of the actual landing support",
        "minimum_definition": "J_land,min(y)=sum_C kappa_y(C)/ell(C)",
        "Borel_measurability": "Round57 enumerates maximal positive components by a least-rational owner with Borel endpoint infimum/supremum; component mass and adapted length are Borel, and the monotone countable sum of mass/length is Borel",
        "zero_policy": "h(y)=0 has the empty component registry, J_land,min(y)=0 and z_land(y)=0 and is never normalized",
        "lower_bound_proof": "a canonical pair has strictly positive regular density on its connected carrier W, so W cannot cross a positive-length gap or omitted puncture; W lies in one C and ell(W)<=ell(C), hence integrating p_W/ell(W) over all pairs in C gives at least kappa_y(C)/ell(C)",
        "attainment": "restrict the inherited regular density once to each maximal component C; this is an exact positive representation and attains sum_C kappa_y(C)/ell(C)",
        "cuts": "positive cuts only shorten W and cannot decrease the minimum",
        "coarsening": "every legal same-ID same-chart coarsening is already included by the maximal actual-union components; no merge may cross a true gap, singularity or cemetery puncture",
        "tags": "forgetting proof-only tags cannot go below J_land,min; forgetting an immutable physical ID is outside the kernel contract",
        "cross_registry_guard": "the theorem does not exclude a future cross-y or cross-chart physical Rokhlin redisintegration built from an actual stable-holonomy quotient; that would be a new Gate-2/physical interface, not a same-ID coarsening",
        "strict_same_time_iff": "an exact positive unshifted landing standard family preserving y and the physical ID is proper iff J_land,min(y)<C_p*h(y)",
        "multiple_family_iff": "allowing a countable exact partition into positive candidate families does not weaken the threshold: if every positive subfamily has J_i/h_i<C_p then sum_i J_i/sum_i h_i is their outer mass-weighted average and is strictly <C_p; conversely J_land,min<C_p*h makes the single maximal-component family proper; zero-mass fibres are empty",
        "threshold_C_p": qstr(C_P),
        "Round57_global_join": "Round57 step 3 constructs the common restriction on I(B) with global affine bound Z_3<infinity; time reversal preserves adapted length and Z, and maximal physical coarsening gives J_land,min,total<=Z_3<infinity on B",
        "Round57_consequence": "J_land,min,total is therefore physically finite, but global finiteness is not the fibrewise strict C_p*h threshold",
        "status": "CERTIFIED_MAXIMAL_COMPONENT_EXACT_MINIMUM_AND_UNSHIFTED_PROPERNESS_IFF",
    }


def finite_high_mass_separator() -> dict[str, Any]:
    rows = separator_sample_rows()
    full_length = N_COMPONENTS * COMPONENT_LENGTH + (N_COMPONENTS - 1) * GAP_LENGTH
    physical_z = Q(N_COMPONENTS) / COMMON_MASS
    reference_jcap = Q(2)
    reference_zcap = reference_jcap / COMMON_MASS
    require(full_length == 1, "separator unit interval")
    require(HIT_LOWER < GAP_MASS < HIT_UPPER, "separator hit window")
    require(COMMON_MASS > COMMON_LOWER, "separator common mass")
    require(Q(N_COMPONENTS - 1) <= C_P < Q(N_COMPONENTS), "separator ceiling")
    require(physical_z > C_P, "separator physical improper")
    require(reference_zcap < C_P, "separator reference proper")
    return {
        "scope": "logical exact-standard-family nonimplication model, not a claim that the billiard realizes this fragmentation",
        "ambient_space": "one unit half-open collision interval with Lebesgue law and identity first-return map at time one",
        "full_induced_output": "the whole ambient law returns to itself exactly once and has normalized Z=1<C_p",
        "common_marker": "retain N equal positive intervals of total length and mass 999/1000, separated by N-1 equal positive gaps of total mass 1/1000",
        "N": str(N_COMPONENTS),
        "N_rule": "floor(C_p)+1",
        "component_length": qstr(COMPONENT_LENGTH),
        "gap_length": qstr(GAP_LENGTH),
        "common_mass": qstr(COMMON_MASS),
        "common_mass_strict_lower": "999/1000>249/250",
        "hit_mass": qstr(GAP_MASS),
        "hit_window": "21/111718750<1/1000<1/500",
        "physical_landing_J_min": str(N_COMPONENTS),
        "physical_landing_normalized_Z_min": qstr(physical_z),
        "physical_landing_improper": True,
        "physical_first_return": "tau=1, Q=id on the common marker; the unshifted source and landing are the same fragmented exact law",
        "physical_ID_and_gap_policy": "all N common intervals and N-1 true positive gaps lie in one immutable half-open physical landing chart/ID; each endpoint has a unique owner, and no exact positive physical coarsening may cross a gap",
        "reference_reassembler": "a finite piecewise-translation Borel measure isomorphism sends the N retained components adjacently onto [0,999/1000); it is analytic on every retained piece and extends by translating the gaps onto the complement",
        "reference_type_guard": "the reassembler is a stopped/reference coordinate map, not a same-coordinate physical coarsening of the landing; its two identical orientation views contribute J_cap=1+1=2 while the physical landing minimum remains N",
        "reference_two_view_J_cap": qstr(reference_jcap),
        "reference_z_cap": qstr(reference_zcap),
        "reference_D_cap": 0,
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "conclusion": "full ambient proper return + high common mass + finite physical landing Z + finite J_cap + D_cap=0 do not imply unshifted physical landing properness",
        "status": "CERTIFIED_FINITE_HIGH_MASS_DCAP_ZERO_UNSHIFTED_LANDING_SEPARATOR",
    }


def ambient_marker_typing() -> dict[str, Any]:
    return {
        "weak_level": "the full induced identity and a Borel marker chi give a legal dominated marked measure and exact weak first-return graph integrals",
        "strong_level": "multiplication by chi replaces the ambient law by chi*mu; its strong standard-family boundary cost is the maximal-component minimum J_land,min, not the boundary cost of the unmarked ambient law",
        "full_output_nonimplication": "even a proper full induced output cannot absorb the endpoints of an arbitrary positive common marker",
        "reference_nonimplication": "transporting the marker to a proper stopped reference view controls that view only; inverse endpoint maps recover the exact graph but may return an improper physical landing law",
        "required_multiplier_interface": "a same-coordinate characteristic-multiplier theorem must prove J_land,min<C_p*h (or a stronger physical strong-norm bound) on the identical marked IDs",
        "current_scope": "the pinned strong/Growth inputs apply after a proper-family hypothesis or control finite Z; they do not erase marker boundaries at the original time-n coordinate",
        "status": "CERTIFIED_FULL_AMBIENT_RETURN_PLUS_MARKER_IS_WEAK_ONLY_WITHOUT_LANDING_THRESHOLD",
    }


def bad_stratum_interface() -> dict[str, Any]:
    return {
        "normalized_field": "z_land(y)=J_land,min(y)/h(y) for h(y)>0; z_land=0 on the empty fibre",
        "landing_defect": "D_land=0 if z_land<C_p; otherwise D_land=min{d>=1:2^-d*z_land<C_p/2}",
        "strict_boundary": "z_land=C_p is not proper and gives D_land=2 because d=1 reaches equality C_p/2",
        "dyadic_pointwise_bound": "on D_land>0, minimality gives 2^D_land<=4*z_land/C_p",
        "dyadic_moment": "integral h(y)*2^D_land(y)dlambda(y)<=H+(4/C_p)*J_land,min,total<infinity",
        "bad_set": "B_land={y:z_land(y)>=C_p}",
        "exact_kernel_condition": "the unshifted physical landing kernel is proper on the original outer registry iff lambda-almost every positive fibre lies outside B_land",
        "integrability_available": "J_land,min,total<infinity follows from the frozen finite physical landing representation and maximal-component coarsening",
        "markov_bound": "for B_k={z_land>=2^k*C_p}, integral_(B_k)h dlambda <= J_land,min,total/(2^k*C_p), so the very-bad tail vanishes as k tends to infinity",
        "why_not_closure": "the k=0 bound is only finite/small, not zero; discarding B_land loses physical first-return mass, while normalization or charging it to a null cemetery would be false",
        "D_cap_independence": "D_cap is computed in the stopped proper-view common-refinement geometry, whereas D_land is computed on the unshifted physical B geometry; the finite separator has D_cap=0 but D_land>0",
        "clock_typing": "the finite D_land moment is a real landing-complexity upgrade, but evolving 696*D_land collisions from B cannot be appended to tau_cap=n and called the original first return",
        "shortest_sufficient_input": "prove J_land,min(y)<C_p*h(y) for almost every positive same-ID fibre, preferably with a uniform margin (1-epsilon)C_p*h",
        "status": "CERTIFIED_BAD_STRATUM_TAIL_AND_EXACT_MISSING_THRESHOLD",
    }


def first_hit_reinduction_frontier() -> dict[str, Any]:
    rows = reinduction_rows()
    return {
        "once_covering_extraction": "for a controlled finite-Z positive law on C_s, the disjoint first-hit cylinders {tau_C_s^+=j} cover the recurrent law modulo the frozen null set, retain the input ID with a new return-path suffix, and charge every point exactly once",
        "finite_Z_consequence": "the Round41/42 hereditary killed resolvent and Round55 terminal extraction give a finite aggregate landing Z for this next-return law",
        "rebase_from_physical_landing": "applying the construction to the unshifted B marginal gives an exact first return from B to C_s; viewed from the original A endpoint it is the second return, not the original tau_cap=n first return",
        "source_problem": "the rebased B source remains the same finite-Z but possibly improper physical landing law",
        "landing_problem": "aggregate finite Z of the next-return output again does not imply its maximal-component ratio is below C_p",
        "reference_view_variant": "starting from the proper stopped reference view gives a physical first entrance if that view is outside C_s, not a C_s-to-C_s first-return kernel and not the original time-n graph",
        "iteration_nonimplication": "no finite number of reinductions forces properness; the identity-return finite separator leaves the same fragmented improper law at every occurrence",
        "separator_rows": rows,
        "separator_rows_sha256": digest(rows),
        "legal_upgrade_if_future_threshold_holds": "if one rebased source and its first-return landing both satisfy their maximal-component thresholds on the retained IDs, that rebased occurrence supplies a proper physical first-return kernel; it still does not retroactively properize the original time-n landing",
        "status": "CERTIFIED_ONCE_COVERING_NEXT_RETURN_FINITE_Z__PROPERNESS_AND_ORIGINAL_TIME_REMAIN_OPEN",
    }


def literature_audit() -> dict[str, Any]:
    return {
        "checked_on": "2026-07-20",
        "official_sources": [
            "arXiv:2606.10155v1, Demers--Liverani, Recent Progress in the Application of Transfer Operators to Dispersing Billiards",
            "arXiv:2104.06947v3, Demers--Liverani, Projective Cones for Sequential Dispersing Billiards",
            "arXiv:2501.16102v2, Balint--Komalovics, Improved estimates of statistical properties in some non-uniformly hyperbolic dynamical systems",
        ],
        "finding": "the 2026 survey reviews Growth/projective-cone/open-system technology but states no theorem turning an arbitrary marked finite-Z induced landing into a proper landing at the same physical time; the other two sources likewise do not provide this CM2-specific same-ID threshold",
        "external_theorem_promoted": False,
        "status": "AUDITED_NO_DIRECT_SAME_TIME_LANDING_PROPERNESS_THEOREM_FOUND",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE_PINNED_ROUND57",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE_PINNED_ROUND57",
        "exact_same_ID_unshifted_first_return_graph": "CERTIFIED_BUT_UNPROPER_PINNED_ROUND57",
        "physical_unshifted_source_and_landing_finite_Z": "CERTIFIED",
        "maximal_component_exact_minimum_Z": "CERTIFIED",
        "physical_unshifted_J_land_min_total": "CERTIFIED_FINITE",
        "physical_unshifted_D_land_full_dyadic_moment": "CERTIFIED_FINITE",
        "same_time_positive_disintegration_freedom": "EXHAUSTED_WITHIN_FROZEN_ID_AND_CHART_BY_J_LAND_MIN_IFF",
        "bad_landing_dyadic_mass_tail": "CERTIFIED_VANISHING_AT_INFINITE_THRESHOLD",
        "full_ambient_return_plus_common_marker_strong_kernel": "NOT_CERTIFIED",
        "once_covering_rebased_next_return_graph": "CERTIFIED_FINITE_Z_BUT_UNPROPER",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_during_added_recovery": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "pinned_report_sha256": dict(PINNED_REPORTS),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "maximal-component minimal-Z theorem, unshifted landing iff, ambient-marker separator, and once-covering reinduction frontier",
            "external_theorem_promoted": False,
        },
        "pinned_input_audit": pinned_input_audit(),
        "maximal_component_minimum_Z_theorem": maximal_component_minimum_Z(),
        "finite_high_mass_Dcap_zero_separator": finite_high_mass_separator(),
        "full_ambient_marker_typing": ambient_marker_typing(),
        "landing_bad_stratum_interface": bad_stratum_interface(),
        "once_covering_first_hit_reinduction": first_hit_reinduction_frontier(),
        "latest_technical_literature_audit": literature_audit(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier outside deliverables")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "dependencies": dict(DEPENDENCIES),
        "pinned_reports": dict(PINNED_REPORTS),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
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
        print(f"ROUND58_GATE4_LANDING_CERT_FAILURE: {exc}")
        return 1

    strict = build_result()["strict_nonpromotion"]
    print("MAXIMAL_COMPONENT_MINIMUM_Z:", strict["maximal_component_exact_minimum_Z"])
    print("UNSHIFTED_PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
    print("REBASING:", strict["once_covering_rebased_next_return_graph"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
