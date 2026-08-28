#!/usr/bin/env python3
"""Round-57 unshifted first-return typing and killed-path frontier.

The preceding Round-57 leaf closes the physical common boundary numerator
``J_cap`` and constructs a proper two-view *reference* carrier.  This leaf
audits the next type boundary.  The common raw restriction already lies in
the original first-return cells, so its unshifted Borel return graph and the
original excursion avoidance are genuine.  What remains missing is
geometric properness at that unshifted landing time.

We prove that a positive post-return recovery clock can never repair this
while retaining first-hit semantics, construct the strongest legal tagged
proper graph lift, and separate terminal nonhit from killed-path avoidance.
No proper physical first-return kernel, later-clock envelope, physical q,
strong cemetery, Gate 4, or CM2 is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round57-unshifted-first-return-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate4_round57_unshifted_first_return_frontier_verifier.py"
)


# The Round-57 dependency is replaced by its final digest only after that leaf
# is frozen.  Keeping a literal sentinel makes premature emission fail closed.
DEPENDENCIES = {
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json": (
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414"
    ),
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json": (
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8"
    ),
}


C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_LENGTH = Q(1, 2) / C_P
AVOIDANCE_CYCLE = 1001
AVOIDANCE_HORIZON = AVOIDANCE_CYCLE + 1


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
        require(len(expected) == 64, f"dependency digest not frozen: {name}")
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    r51 = loaded[
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    ]["result"]
    view = r51["physical_two_proper_view_object_lemma"]
    selected = r51["selected_forward_proper_common_law"]
    require(
        view["status"]
        == "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM",
        "Round51 proper views",
    )
    require(view["same_ID_once_charge"] is True, "Round51 once charge")
    require(view["raw_geometry_is_proper"] is False, "Round51 raw scope")
    require("P_fw" in view["fibrewise_inverse_maps"][0], "Round51 inverse")
    require(selected["parent_charged_once"] is True, "Round51 selected charge")
    require(selected["separate_normalization_used"] is False, "Round51 normalization")
    require("Theta" in selected["view_transfer_map"], "Round51 transport")

    r56 = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]
    path = r56["path_max_mesh_and_Kac_tower"]
    paired = r56["paired_leafwise_reverse_replay"]
    metric = r56["metric_and_once_charge_terminal_source_join"]
    require(
        path["first_return_partition"]
        == "R_n=C_s intersect {tau_C_s^+=n}, n>=1",
        "Round56 first-return partition",
    )
    require(
        metric["source_return_atom"]
        == "A subset R_n on one regular rank-path branch",
        "Round56 source atom",
    )
    require(metric["target_return_atom"] == "B=T_s^n(A) subset C_s", "Round56 target")
    require("no-intermediate-C_s" in paired["reverse_first_return"], "Round56 avoidance")
    require(paired["normalization_used"] is False, "Round56 normalization")

    r57 = loaded[
        "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
    ]["result"]
    closure = r57["physical_common_refinement_closure"]
    obstruction = r57["independent_downstream_obstructions"]
    strict = r57["strict_nonpromotion"]
    require(
        closure["status"]
        == "CERTIFIED_PHYSICAL_COMMON_REFINEMENT_J_CAP_AND_SINGLE_D_CAP_CLOCK",
        "Round57 closure",
    )
    require("identical raw point restriction" in closure["same_raw_restriction"], "Round57 raw identity")
    require("original A_c" in closure["step_4_back_to_source"], "Round57 source pullback")
    require("finite adapted Z" in closure["step_3_reverse_predicate"], "Round57 landing Z")
    require("inherits the original tau_R=n" in closure["not_yet_physical_first_return"], "Round57 inherited graph")
    require("do not define one physical first-hit landing map" in closure["not_yet_physical_first_return"], "Round57 type guard")
    require(
        "tau_R=n" in obstruction["proper_same_ID_first_return"]["inherited_but_insufficient_graph"],
        "Round57 inherited first-return graph",
    )
    require(
        obstruction["proper_same_ID_first_return"]["status"]
        == "INDEPENDENT_PHYSICAL_KERNEL_INTERFACE_NOT_CERTIFIED",
        "Round57 first-return guard",
    )
    require(
        obstruction["intermediate_C24_avoidance"]["status"]
        == "TERMINAL_NONHIT_DOES_NOT_IMPLY_INTERMEDIATE_AVOIDANCE",
        "Round57 avoidance guard",
    )
    require(strict["physical_common_refinement_J_cap_total"] == "CERTIFIED_FINITE", "Round57 J_cap")
    require(strict["physical_proper_same_ID_first_return_kernel"] == "NOT_CERTIFIED", "Round57 nonpromotion")
    return loaded


def recovery_rows() -> list[dict[str, Any]]:
    """Exact two-state return/recovery separator.

    State C has adapted length 1/(2 C_p), state O has adapted length 1.
    The map swaps them by the mass coordinate.  The first C-to-C return is
    time two.  Odd extra clocks produce a proper carrier outside C; even
    extra clocks land in C only after the time-two first return and remain
    geometrically short.
    """
    rows: list[dict[str, Any]] = []
    for r in range(7):
        landing_state = "C24" if r % 2 == 0 else "outside_C24"
        normalized_z = Q(2) * C_P if landing_state == "C24" else Q(1)
        rows.append(
            {
                "extra_recovery_r": r,
                "total_time_n_plus_r": 2 + r,
                "landing_state": landing_state,
                "landing_normalized_Z": qstr(normalized_z),
                "landing_is_proper": normalized_z < C_P,
                "is_C24_first_return": r == 0,
                "all_three_first_return_C24_and_proper": False,
            }
        )
    require(rows[0]["is_C24_first_return"] is True, "base first return")
    require(rows[0]["landing_is_proper"] is False, "base improper")
    require(all(not row["all_three_first_return_C24_and_proper"] for row in rows), "trilemma")
    return rows


def direct_sum_rows() -> list[dict[str, Any]]:
    return [
        {
            "construction": "selected_forward_only",
            "forward_weight": "1",
            "reverse_weight": "0",
            "total_mass_over_h": "1",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "1",
            "ambient_object": "one tagged proper reference view",
        },
        {
            "construction": "unweighted_tagged_direct_sum",
            "forward_weight": "1",
            "reverse_weight": "1",
            "total_mass_over_h": "2",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "2",
            "ambient_object": "double charge unless explicitly renormalized",
        },
        {
            "construction": "half_weighted_tagged_direct_sum",
            "forward_weight": "1/2",
            "reverse_weight": "1/2",
            "total_mass_over_h": "1",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "1",
            "ambient_object": "artificial disjoint-union reference, not collision space",
        },
    ]


def avoidance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for j in (0, 1, 2, AVOIDANCE_CYCLE - 1, AVOIDANCE_CYCLE, AVOIDANCE_HORIZON):
        state = j % AVOIDANCE_CYCLE
        rows.append(
            {
                "collision_time_j": j,
                "cycle_state": state,
                "in_C24": state == 0,
                "is_terminal_time": j == AVOIDANCE_HORIZON,
            }
        )
    require(rows[-2]["in_C24"] is True, "intermediate hit")
    require(rows[-1]["in_C24"] is False, "terminal nonhit")
    return rows


def raw_common_first_return_typing() -> dict[str, Any]:
    return {
        "raw_domain": "G_A,cap is the exact positive common restriction of A_c subset R_n, pulled back to the original C_s source coordinate",
        "Borel_stopping_time": "tau_cap(y,x)=n(y); n is an immutable positive integer first-return tag on the countable half-open registry",
        "physical_map": "Q_cap(y,x)=T_s^n(x) in B_c subset C_s",
        "first_hit_semantics": "T_s^j(x) notin C_s for 1<=j<n and T_s^n(x) in C_s",
        "same_restriction_ID": "the original Round35 component/source-parent/n/path/re-cut ID is retained; terminal proof tags only refine it",
        "charge": "the common raw point is charged exactly once and neither terminal pullback is normalized",
        "source_finite_Z": "CERTIFIED by the Round57 palindrome pullback to subintervals of original A_c",
        "landing_finite_Z": "CERTIFIED because the common I(B_c) restriction has finite adapted Z and time reversal preserves Z",
        "graph_measure_identity": "Gamma_cap=(id,Q_cap)_#kappa_cap is an exact physical C_s-to-C_s first-return graph measure",
        "unshifted_landing_proper": "NOT_CERTIFIED",
        "typing_triplet": {
            "exact_same_ID_first_return_graph_tau_cap_equals_n": "CERTIFIED_BUT_UNPROPER",
            "source_and_landing_finite_Z": "CERTIFIED",
            "proper_landing_kernel": "NOT_CERTIFIED",
        },
        "non_equivalence_guard": "tau_cap=n inherits only the original R_n C_s-first-return segment; it does not assert C24 avoidance during any later postproperisation or terminal schedule",
        "strict_scope": "measurable same-ID first-return graph with finite-Z marginals, not a proper strong-space return kernel",
        "status": "CERTIFIED_BUT_UNPROPER",
    }


def finite_Z_not_proper() -> dict[str, Any]:
    require(SHORT_LENGTH > 0, "short length")
    require(Q(1) / SHORT_LENGTH == 2 * C_P, "short Z")
    require(2 * C_P > C_P, "improper threshold")
    return {
        "properness_contract": "a positive family of mass h is proper only if Z/h<C_p",
        "countermodel": "one positive uniform carrier of mass one and adapted length ell=1/(2*C_p)",
        "ell": qstr(SHORT_LENGTH),
        "finite_normalized_Z": qstr(Q(1) / SHORT_LENGTH),
        "threshold_C_p": qstr(C_P),
        "finite_but_improper": True,
        "representation_lower_bound": "every exact positive carrier representation of this isolated support uses carriers of length<=ell, hence Z>=sum p_i/ell=1/ell=2*C_p",
        "cuts_and_tags": "positive cuts only shorten carriers; retaining or forgetting proof tags cannot lower this support-length bound",
        "conclusion": "finite physical source/landing Z does not imply an exact proper disintegration at the same unshifted collision coordinate",
        "status": "CERTIFIED_FINITE_Z_DOES_NOT_IMPLY_UNSHIFTED_PROPERNESS",
    }


def recovery_clock_obstruction() -> dict[str, Any]:
    rows = recovery_rows()
    return {
        "general_postclock_dichotomy": "if x first returns to C_s at n and r(x)>0, then T_s^(n+r)x is either outside C_s or, if it is in C_s, time n is an earlier C_s hit; n+r is never the first return",
        "fixed_or_variable_scope": "the argument is pointwise and applies equally to fixed, global, tag-constant, Borel-variable, or synchronized positive clocks",
        "preclock_scope": "for 0<r<n, z=T_s^r x lies outside C_s by the R_n predicate; z can parametrize the residual excursion but is not a C_s source of the induced first-return map",
        "late_preclock_scope": "for r>=n the shifted source has already crossed the original first return",
        "palindrome_scope": "an exact identity palindrome may pull a predicate and finite Z back to the original source, but at its final physical coordinate it has not turned the original unshifted landing marginal into a proper one",
        "D_cap_consequence": "the 696*D_cap evolution is a valid proper reference-view clock; on every D_cap>0 stratum it cannot be appended to tau_cap and called the original physical first-return time",
        "only_unshifted_route": "prove the exact time-n landing law already proper, or construct an exact same-time positive coarsening/disintegration with Z/h<C_p; no positive dynamical recovery may be hidden in tau_cap",
        "two_state_separator": {
            "space": "two mass-coordinate interval states C24 and O, with T swapping them",
            "adapted_lengths": {"C24": qstr(SHORT_LENGTH), "O": "1"},
            "first_return_time": 2,
            "rows": rows,
            "rows_sha256": digest(rows),
        },
        "status": "CERTIFIED_FIRST_HIT_POSTRECOVERY_NO_GO_AND_EXACT_TRILEMMA",
    }


def proper_reference_graph_lift() -> dict[str, Any]:
    rows = direct_sum_rows()
    return {
        "raw_law": "kappa_cap on tagged records (y,x) with x in G_A,cap",
        "selected_proper_map": "S_fw sends each raw record through the retained tag-constant properisation branch and keeps y, clock and half-open proof tags",
        "selected_reference_law": "kappa_fw_star=(S_fw)_#kappa_cap; it is proper and once charged",
        "tagged_Borel_inverse": "X(z)=physical_source_projection(S_fw^-1(z)) is Borel modulo the pinned null cemetery",
        "physical_endpoint_map": "Y(z)=T_s^n(X(z)), using the retained original return-depth tag n",
        "exact_graph_identity": "(X,Y)_#kappa_fw_star=(id,Q_cap)_#kappa_cap=Gamma_cap",
        "reverse_transport": "Theta=S_rev o S_fw^-1 transports the reverse fields without a second parent charge",
        "certified_object": "a proper latent/reference parametrization of the exact physical first-return graph",
        "not_a_physical_kernel": [
            "the proper coordinate z need not lie in C_s",
            "Y(z) is defined through the inverse endpoint map X, not asserted to be the first C_s hit of the orbit starting at z",
            "X_#kappa_fw_star=kappa_cap is the original finite-Z law and is not proved proper",
            "no physical strong-norm or transfer-operator intertwining through X and Y is certified",
        ],
        "two_view_direct_sum": "the half-weighted tagged direct sum also recovers Gamma_cap after inverse endpoint maps, but lives on an artificial disjoint union; the unweighted sum doubles mass",
        "direct_sum_rows": rows,
        "direct_sum_rows_sha256": digest(rows),
        "status": "CERTIFIED_ONCE_CHARGED_PROPER_REFERENCE_GRAPH_LIFT_NOT_PHYSICAL_KERNEL",
    }


def intermediate_avoidance_frontier() -> dict[str, Any]:
    rows = avoidance_rows()
    require(Q(1, AVOIDANCE_CYCLE) < Q(1, 1000), "small core mass")
    return {
        "original_excursion": "CERTIFIED: because G_A,cap subset R_n, every raw point avoids C_s for 1<=j<tau_cap=n",
        "postproperisation_or_terminal_schedule": "NOT_CERTIFIED: the Round57 terminal predicates inspect terminal nonhit, not every intermediate collision of the added clocks",
        "exact_separator": {
            "space": "X=(Z/1001Z)x[0,1] with uniform invariant law",
            "map": "T(i,u)=(i+1 mod 1001,u)",
            "core": "C24={0}x[0,1]",
            "core_mass": "1/1001<1/1000",
            "start": "state 0",
            "terminal_time_H": AVOIDANCE_HORIZON,
            "terminal_state": 1,
            "terminal_nonhit_mass": "1",
            "first_intermediate_return_time": AVOIDANCE_CYCLE,
            "all_intermediate_avoidance_mass": "0",
            "rows": rows,
            "rows_sha256": digest(rows),
        },
        "needed_killed_predicate": "K_H(x)=product_(j=1)^H 1_(C_s^c)(T_s^j x) on the identical raw restriction and clock tag",
        "first_return_variant": "for a C_s return at tau, require product_(j=1)^(tau-1)1_(C_s^c)(T_s^j x) times 1_(C_s)(T_s^tau x)",
        "early_hit_rule": "if an added recovery path hits C_s early, that first hit must be extracted as the physical return branch and its unshifted landing law proved proper; it may not be discarded or relabelled as the planned terminal time",
        "Growth_scope": "hereditary killed-Growth estimates can control Z for an already defined positive killed subfamily, but do not by themselves prove positive common mass or unshifted landing properness",
        "shortest_remaining_input": "prove the exact time-n common landing marginal proper with no recovery; otherwise construct a same-ID first-hit extraction whose every retained landing marginal is proper and whose early-hit pieces cover the common law exactly once",
        "status": "CERTIFIED_RAW_RN_AVOIDANCE_AND_TERMINAL_VERSUS_KILLED_SEPARATOR__POSTRECOVERY_OPEN",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE_PINNED_ROUND57",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE_PINNED_ROUND57",
        "physical_same_ID_unshifted_first_return_graph_tau_cap_equals_n": "CERTIFIED_BUT_UNPROPER",
        "physical_first_return_source_and_landing_finite_Z": "CERTIFIED",
        "original_R_n_intermediate_C_s_avoidance": "CERTIFIED",
        "proper_once_charged_reference_graph_lift": "CERTIFIED",
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
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "unshifted first-return typing, recovery no-go, proper reference graph lift, and killed-path frontier",
            "external_theorem_promoted": False,
        },
        "raw_common_first_return_typing": raw_common_first_return_typing(),
        "finite_Z_not_unshifted_proper": finite_Z_not_proper(),
        "recovery_clock_first_hit_obstruction": recovery_clock_obstruction(),
        "proper_reference_graph_lift": proper_reference_graph_lift(),
        "intermediate_avoidance_frontier": intermediate_avoidance_frontier(),
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
    strict = build_result()["strict_nonpromotion"]
    print("RAW_FIRST_RETURN_GRAPH:", strict["physical_same_ID_unshifted_first_return_graph_tau_cap_equals_n"])
    print("REFERENCE_GRAPH_LIFT:", strict["proper_once_charged_reference_graph_lift"])
    print("PHYSICAL_PROPER_RETURN:", strict["physical_proper_same_ID_first_return_kernel"])
    print("POSTRECOVERY_AVOIDANCE:", strict["intermediate_C24_avoidance_during_added_recovery"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
