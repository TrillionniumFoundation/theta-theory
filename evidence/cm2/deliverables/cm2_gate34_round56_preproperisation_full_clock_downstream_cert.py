#!/usr/bin/env python3
"""Round-56 downstream closure of the ambient preproperisation clock.

This append-only leaf performs one deliberately narrow substitution.  Round
51 already constructs two proper Borel view kernels and one selected
once-charged proper reference law recordwise, without assuming a global
clock moment.  Round 52 then gives a uniform finite terminal time, zero
marginal shells and a parent-charged total ambient clock formula conditional
on

    I_D = integral p(y) exp(Dbar(y)/6) dlambda(y) < infinity.

After the independently audited Round-56 Kac-mesh leaf certifies precisely
that same physical moment, the condition can be discharged.  The resulting
full ambient two-view max-clock exponential moment, its L^(6/5) envelope and
its absolutely-continuous Borel-exhaustion tail are finite.

This does not construct the common-refinement numerator J_cap, a proper
same-ID physical first-return kernel, intermediate C24 avoidance, any later
or repeated recovery-clock moment, physical q, or the strong cemetery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round56-preproperisation-full-clock-downstream.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round56-preproperisation-full-clock-downstream-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round56_preproperisation_full_clock_downstream_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json": (
        "7ddecb544fa5a2b243882eaf2028159c22f8437fc3fbb49fda4eb487ab181798"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json": (
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414"
    ),
}

HALF_BLOCK = 696
CLOCK_DENOMINATOR = 4176
PRECLOCK_EXPONENT = Q(HALF_BLOCK, CLOCK_DENOMINATOR)
DEFECT_COEFFICIENT = Q(35, 99 * 2**309)


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
        require(expected != "R56_FINAL_SHA256", "Round56 dependency not frozen")
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    round51 = loaded[
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    ]["result"]
    object_lemma = round51["physical_two_proper_view_object_lemma"]
    selected = round51["selected_forward_proper_common_law"]
    full_clock = round51["full_clock_conditional_bridge"]
    frontier51 = round51["intersection_and_gate_frontier"]
    require(
        object_lemma["status"]
        == "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM",
        "Round51 two-view object lemma",
    )
    require(object_lemma["same_ID_once_charge"] is True, "Round51 once charge")
    require(
        selected["status"]
        == "CERTIFIED_SELECTED_FORWARD_PROPER_COMMON_LAW_WITH_BOREL_REVERSE_TRANSPORT",
        "Round51 selected law",
    )
    require(selected["parent_charged_once"] is True, "Round51 parent charge")
    require(
        full_clock["status"]
        == "CERTIFIED_EXACT_FULL_CLOCK_FORMULA_CONDITIONAL_ON_MISSING_DEFECT_MOMENT",
        "Round51 full-clock bridge",
    )
    require(full_clock["exact_preclock_exponent"] == "696/4176=1/6", "Round51 exponent")
    require(
        full_clock["required_same_kernel_moment"]
        == "I_D=integral p(y)*exp(Dbar(y)/6) dlambda(y)<infinity",
        "Round51 I_D typing",
    )
    require(
        full_clock["conditional_integrated_bound"]
        == "integral Wtilde_r_star^r dm_star<integral p dlambda+2*A_H*I_D",
        "Round51 integrated bound",
    )
    require(
        frontier51["proper_common_fw_rev_return"] == "NOT_CERTIFIED"
        and frontier51["collision_time_q"] == "NOT_CERTIFIED"
        and frontier51["strong_trace_current_cemetery"] == "NOT_CERTIFIED",
        "Round51 nonpromotion",
    )

    round52 = loaded[
        "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    cell = round52["cell_level_retyping_audit"]
    terminal = round52["uniform_outer_majorant_terminal_join"]
    separator = round52["large_common_mass_geometric_nonpromotion"]
    require(cell["Borel_and_once_charge"].startswith("CERTIFIED:"), "Round52 cell law")
    require(
        cell["singleton_family_typing"].startswith("CERTIFIED:"),
        "Round52 singleton properisation",
    )
    require(
        terminal["H_joint_exists_uniformly_for_all_parameters_and_proper_views"] is True,
        "Round52 finite H_joint",
    )
    require(terminal["numeric_H_joint"] is None, "Round52 H_joint nonnumeric")
    require(
        terminal["dyadic_shells"]
        == "k_fw=k_rev=0 because h_fw/p,h_rev/p>499/500>1/2",
        "Round52 shell removal",
    )
    require(
        terminal["total_orientation_clock"]
        == "C_sigma,total=696*Dbar+H_joint+221328",
        "Round52 total clock",
    )
    require(
        terminal["conditional_total_ambient_max_clock_envelope"].startswith(
            "if I_D=integral p*exp(Dbar/6)<infinity"
        ),
        "Round52 total ambient bridge",
    )
    require(
        terminal["terminal_not_intermediate"].startswith(
            "the conclusion controls the C24 predicate at the single terminal collision only"
        ),
        "Round52 terminal-only scope",
    )
    require(
        terminal["physical_collision_time_q_L6over5"] == "NOT_CERTIFIED"
        and terminal["strong_singular_current_cemetery"] == "NOT_CERTIFIED",
        "Round52 q/cemetery frontier",
    )
    require(
        separator["status"]
        == "CERTIFIED_LARGE_COMMON_MASS_BOREL_TWO_VIEW_FIELDS_DO_NOT_IMPLY_PROPER_INTERSECTION",
        "Round52 common-geometry separator",
    )

    round53 = loaded[
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    defect53 = round53["fractional_cell_Z_to_defect_moment"]
    common53 = round53["common_refinement_Z_to_proper_return_clock"]
    separation53 = round53["two_Z_and_cemetery_nonimplication_audit"]
    require(
        defect53["direct_linear_tail_layer_cake_bound"]
        == "I_D<nu(X)+[35/(99*2^309)]*J_pair",
        "Round53 J_pair-to-I_D bridge",
    )
    require(
        common53["physical_common_refinement_J_cap_certified"] is False
        and common53["physical_proper_same_ID_return_certified"] is False,
        "Round53 J_cap frontier",
    )
    require(
        separation53["finite_marginal_Z_does_not_supply_J_cap"].endswith(
            "common-refinement J_cap=infinity"
        ),
        "Round53 independent J_cap obstruction",
    )
    require(
        separation53["finite_absolute_continuous_Z_does_not_supply_strong_cemetery"].endswith(
            "independent theorem"
        ),
        "Round53 cemetery separation",
    )

    round56 = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]
    defect56 = round56["physical_defect_moment_join"]
    strict56 = round56["strict_nonpromotion"]
    require(defect56["same_measure"] is True, "Round56 same measure")
    require(
        defect56["physical_I_D"] == "CERTIFIED_FINITE"
        and defect56["status"]
        == "CERTIFIED_PHYSICAL_DEFECT_EXPONENTIAL_MOMENT_FROM_J_PAIR",
        "Round56 physical I_D",
    )
    require(
        strict56["physical_J_pair"] == "CERTIFIED_FINITE"
        and strict56["physical_defect_moment_I_D"] == "CERTIFIED_FINITE",
        "Round56 physical closure",
    )
    require(
        strict56["physical_common_refinement_J_cap_total"] == "NOT_CERTIFIED"
        and strict56["physical_proper_same_ID_first_return"] == "NOT_CERTIFIED"
        and strict56["intermediate_C24_avoidance_after_properisation"]
        == "NOT_CERTIFIED"
        and strict56["later_and_repeated_recovery_clock_moments"]
        == "NOT_CERTIFIED"
        and strict56["physical_collision_time_q_L6over5"] == "NOT_CERTIFIED"
        and strict56["strong_singular_current_cemetery"] == "NOT_CERTIFIED",
        "Round56 strict frontier",
    )
    return loaded


def acyclic_dependency_ledger() -> dict[str, Any]:
    require(PRECLOCK_EXPONENT == Q(1, 6), "preclock exponent arithmetic")
    return {
        "logical_order": [
            "Round50/51: each finite cell has finite Borel Dbar and the stopped maps P_fw,P_rev are constructed recordwise",
            "Round51: the two proper view kernels and selected once-charged forward reference law m_star exist without a global Dbar moment",
            "Round52: cellwise once-charge retyping, uniform finite H_joint and k_fw=k_rev=0 are certified without I_D",
            "Round55/56: the terminal B_max/Kac/refinement chain proves physical J_pair and then I_D on that cell law without invoking the full-clock conclusion",
            "this leaf: substitute the now-certified I_D into the already proved Round51/52 conditional formula",
        ],
        "recordwise_geometry_requires_global_I_D": False,
        "round56_J_pair_proof_uses_full_clock_conclusion": False,
        "file_dependency_is_not_hypothesis_cycle": (
            "Round56 pins the Round53 bridge, which in turn pins earlier typing leaves; "
            "the J_pair-to-I_D implication assumes neither the Round51 full-clock conclusion "
            "nor the finiteness of that conclusion"
        ),
        "exact_preclock_factor": "exp((696*Dbar)/4176)=exp(Dbar/6)",
        "physical_preproperisation_moment": (
            "I_D=integral p(y)*exp(Dbar(y)/6)dlambda(y)<infinity"
        ),
        "status": "CERTIFIED_ACYCLIC_DISCHARGE_OF_THE_PREPROPERISATION_MOMENT",
    }


def actual_full_clock_consequence() -> dict[str, Any]:
    return {
        "selected_reference_law": (
            "m_star=lambda(dy)K_fw_star(y,dz), with reverse data transported by "
            "Theta_y; the parent charge is counted once"
        ),
        "postclock": "C_fw,post=C_rev,post=H_joint+221328 because k_fw=k_rev=0",
        "total_clock": "C_sigma,total=696*Dbar+H_joint+221328",
        "A_H_joint": "A_Hjoint=(6/5)^(318+ceil(H_joint/696))<infinity",
        "ambient_weight": (
            "Wtilde_r_star=max(1,1_Sfw_star*exp(C_fw,total/(4176*r)),"
            "1_Srev_star*exp(C_rev,total/(4176*r)))"
        ),
        "scope": (
            "every fixed |s|<=1/400, the Round52 cell-retyped physical first-return "
            "law, its uniform finite terminal schedule H_joint, and every integer r>=1"
        ),
        "actual_integrated_bound": (
            "integral Wtilde_r_star^r dm_star<nu(X)+2*A_Hjoint*I_D<infinity"
        ),
        "expanded_J_pair_bound": (
            "integral Wtilde_r_star^r dm_star"
            "<nu(X)+2*A_Hjoint*(nu(X)+[35/(99*2^309)]*J_pair)<infinity"
        ),
        "numeric_value_claimed": False,
        "why_nonnumeric": (
            "H_joint is one certified uniform finite constant but is not materialized, "
            "and Round56 proves J_pair finite without a closed numerical upper bound"
        ),
        "physical_preproperisation_exp_Dbar_over_6_moment": "CERTIFIED_FINITE",
        "full_ambient_two_view_max_clock_exponential_moment": (
            "CERTIFIED_QUALITATIVELY_FINITE"
        ),
        "parent_charged_total_ambient_max_envelope_L6over5": (
            "CERTIFIED_QUALITATIVELY_FINITE"
        ),
        "status": "CERTIFIED_ACTUAL_FULL_AMBIENT_CLOCK_MOMENT_FROM_PHYSICAL_I_D",
    }


def exhaustion_consequence() -> dict[str, Any]:
    return {
        "envelope_type": (
            "the parent-charged total ambient max-clock envelope on the selected "
            "once-charged two-view reference law"
        ),
        "absolute_continuity": True,
        "statement": (
            "for every increasing Borel exhaustion E_j with union of full base-law "
            "measure, the ambient envelope mass of E_j^c tends to zero"
        ),
        "reason": "integrability plus continuity from above / dominated convergence",
        "weak_mass_cemetery_only": True,
        "trace_current_control_inferred": False,
        "status": "CERTIFIED_AMBIENT_AC_BOREL_EXHAUSTION_TAIL_VANISHES",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "two_proper_view_measure_isomorphism": "CERTIFIED_PINNED_ROUND51",
        "selected_once_charged_proper_reference_law": "CERTIFIED_PINNED_ROUND51",
        "two_proper_view_common_law_blocks_ambient_preclock": False,
        "physical_J_pair": "CERTIFIED_FINITE_PINNED_ROUND56",
        "physical_defect_moment_I_D": "CERTIFIED_FINITE_PINNED_ROUND56",
        "physical_preproperisation_exp_Dbar_over_6_moment": "CERTIFIED_FINITE",
        "full_ambient_two_view_max_clock_exponential_moment": (
            "CERTIFIED_QUALITATIVELY_FINITE"
        ),
        "parent_charged_total_ambient_max_envelope_L6over5": (
            "CERTIFIED_QUALITATIVELY_FINITE"
        ),
        "ambient_AC_Borel_exhaustion_tail": "CERTIFIED_VANISHING",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "proper_common_terminal_two_view_carrier": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
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
            "old_artifacts_modified": False,
            "claim_type": (
                "acyclic discharge of the physical preproperisation exponential "
                "moment and strict ambient full-clock/envelope promotion"
            ),
            "external_theorem_promoted": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
        },
        "acyclic_dependency_ledger": acyclic_dependency_ledger(),
        "actual_full_clock_consequence": actual_full_clock_consequence(),
        "ambient_exhaustion_consequence": exhaustion_consequence(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file(), "verifier missing")
    require(not verifier.is_symlink(), "verifier symlink")
    require(verifier.parent == HERE, "verifier outside deliverables")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": dict(result["strict_nonpromotion"]),
    }


def pretty_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    text = pretty_manifest(args.verifier)
    if args.write_manifest is not None:
        target = args.write_manifest.resolve()
        require(target.parent == HERE, "manifest target outside deliverables")
        target.write_text(text, encoding="utf-8")
        return 0
    if args.manifest_json:
        print(text, end="")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("PRECLOCK_I_D:", strict["physical_preproperisation_exp_Dbar_over_6_moment"])
    print("AMBIENT_FULL_CLOCK:", strict["full_ambient_two_view_max_clock_exponential_moment"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
