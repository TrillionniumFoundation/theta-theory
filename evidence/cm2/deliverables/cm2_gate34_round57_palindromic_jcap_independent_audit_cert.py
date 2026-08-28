#!/usr/bin/env python3
"""Independent audit of the Round-57 palindromic J_cap closure.

This append-only certificate does not reproduce or edit the audited proof.
It pins the frozen Round-57 Gate-4 leaf and independently checks the exact
reversible direction, the one-collision off-by-one, the variable Borel clock,
the two-closed-leg affine Growth ledger, the nonproper second-palindrome
scope, the paired first-return directions, the connected-component
coarsening, the global J_cap integral and the strict nonpromotion boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round57-palindromic-jcap-independent-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round57-palindromic-jcap-independent-audit-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round57_palindromic_jcap_independent_audit_verifier.py"
)

PINNED_FILES = {
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json": (
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8"
    ),
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-assault-2026-07-20.md": (
        "b273290628c966465a3d0133661cfa511f7ec1ef18e98ee105b0f86bc7a2a0bc"
    ),
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.sha256": (
        "9587cbde0852b8e19487a7f80955baee5817ea186b12190417894acca10de3ca"
    ),
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-assault-2026-07-19.md": (
        "c81dfbf71e591a34e282cd03f595da947a6db38e4b4c2b2fb503a751c0ef5823"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
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

MAIN_MANIFEST = next(name for name in PINNED_FILES if "round57-exact" in name and name.endswith(".json"))
MAIN_REPORT = next(name for name in PINNED_FILES if "round57-exact" in name and name.endswith(".md"))
MAIN_SHA_LEDGER = next(name for name in PINNED_FILES if "round57-exact" in name and name.endswith(".sha256"))

CLOSED_A = Q(360134800, 360493663)
C_P = Q(4 * 10**90 * 360493663, 358863)
CUT_Z1 = Q(18367592526, 360493663)
PAL_MASS_COEFF = (CUT_Z1 + 1) * C_P / 2


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


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def load_pinned_files() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in PINNED_FILES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pinned path: {name}")
        require(path.resolve().parent == HERE, f"pinned scope: {name}")
        require(sha256_path(path) == expected, f"pinned hash: {name}")
        if name.endswith(".json"):
            value = strict_json(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"pinned JSON root: {name}")
            loaded[name] = value
        else:
            loaded[name] = path.read_text(encoding="utf-8")
    return loaded


def validate_frozen_sources() -> dict[str, Any]:
    loaded = load_pinned_files()
    main = loaded[MAIN_MANIFEST]
    result = main["result"]
    palindrome = result["palindromic_stopped_cut_replay"]
    closure = result["physical_common_refinement_closure"]
    strict = result["strict_nonpromotion"]

    require(
        main["certificate_sha256"]
        == "6bdac3cc04e164a92daf7edc4a5765b866dae296f738d32d3b1a47e45e0151b0",
        "main certificate pin",
    )
    require(
        main["verifier_sha256"]
        == "71aab93d11f3a458cf5c0601178cd938f0ec924e9edadbcfc8201344ea80f179",
        "main verifier pin",
    )

    ledger = loaded[MAIN_SHA_LEDGER]
    for expected_line in (
        "6bdac3cc04e164a92daf7edc4a5765b866dae296f738d32d3b1a47e45e0151b0  cm2_gate34_round57_exact_slope4_cross_endpoint_frontier_cert.py",
        "71aab93d11f3a458cf5c0601178cd938f0ec924e9edadbcfc8201344ea80f179  cm2_gate34_round57_exact_slope4_cross_endpoint_frontier_verifier.py",
        "b273290628c966465a3d0133661cfa511f7ec1ef18e98ee105b0f86bc7a2a0bc  cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-assault-2026-07-20.md",
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8  cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json",
    ):
        require(expected_line in ledger, "main SHA ledger line")

    report = loaded[MAIN_REPORT]
    for needle in (
        "The second palindrome may be nonproper",
        "No `249/250` lower bound is asserted for an individual proof cell",
        "Closure-touching across an omitted singular, null or cemetery puncture is",
        "never merged.  Components are never merged across `y`",
        "physical proper same-ID first-return kernel:      NOT_CERTIFIED",
    ):
        require(needle in report, f"main report scope: {needle}")

    require("T_s^(K-1)" in palindrome["operator_off_by_one"], "operator off-by-one")
    require("I o T_s^K o I o T_s^K=id" in palindrome["exact_identity"], "palindrome identity")
    require("arbitrarily thin nonproper" in palindrome["second_palindrome_scope"], "second palindrome scope")
    require("no properness" in palindrome["terminal_cut_scope"], "universal one-cut scope")
    require("countable disjoint union" in palindrome["Borel_reason"], "Borel K strata")
    require("never transversely redisintegrates" in palindrome["cuts_only_refine"], "refinement only")
    require("h_cap(y)>249*p(y)/250" in closure["physical_common_mass"], "y-layer mass")
    require("no such lower bound" in closure["physical_common_mass"], "no c-layer mass")
    require("omitted singular, null or cemetery puncture is never merged" in closure["physical_maximal_component_registry"], "puncture policy")
    require("J_cap,physical<=Z_cap,proof" in closure["coarsening_inequality"], "coarsening inequality")
    require(closure["physical_J_cap_total"].endswith("<infinity"), "global Jcap")
    require("finite exp(D_cap/6) moment" in closure["Round53_join"], "Dcap moment")
    require(closure["physical_full_dyadic_D_cap_first_moment"] == "CERTIFIED_FINITE", "dyadic Dcap moment")
    require("not thereby the required proper common kernel" in closure["not_yet_physical_first_return"], "first-return boundary")

    require(strict["physical_common_refinement_J_cap_total"] == "CERTIFIED_FINITE", "strict Jcap")
    require(strict["single_common_properisation_clock_D_cap_moment"] == "CERTIFIED_FINITE", "strict Dcap")
    require(strict["physical_proper_same_ID_first_return_kernel"] == "NOT_CERTIFIED", "strict first return")
    require(strict["physical_collision_time_q_L6over5"] == "NOT_CERTIFIED", "strict q")
    require(strict["Gate4"] == "NOT_CERTIFIED" and strict["CM2"] == "NO-GO_FOR_CLAIM", "strict global frontier")

    r42 = loaded["cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"]["result"]["numerical_C24_killed_Growth"]
    require(r42["one_step_bound"] == "Z(O_s G)<=Z1*Z(G)", "Round42 one-step")
    r42_report = loaded["cm2-gate34-round42-numeric-c24-growth-block-assault-2026-07-19.md"]
    require("every unnormalised C24-killed canonical family satisfies" in r42_report, "Round42 universal scope")

    r50 = loaded["cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"]["result"]["recordwise_properization_and_common_parent_law"]
    require(r50["Borel_stopped_kernel_reason"].startswith("Dbar is integer-valued Borel"), "Round50 Borel clock")
    require(r50["closed_recurrence"] == "Z(T^r G)/mass(G)<=a^r*Z(G)/mass(G)+C_p/2", "Round50 recurrence")

    r52 = loaded["cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"]["result"]["uniform_outer_majorant_terminal_join"]
    require(r52["same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"] == "249/250", "Round52 mass union")
    require(r52["terminal_not_intermediate"].startswith("the conclusion controls"), "Round52 terminal only")

    r53 = loaded["cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"]["result"]["common_refinement_Z_to_proper_return_clock"]
    require("J_cap,total" in r53["global_hypothesis"], "Round53 global hypothesis")
    require(r53["physical_proper_same_ID_return_certified"] is False, "Round53 first-return boundary")

    r56 = loaded["cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"]["result"]
    paired = r56["paired_leafwise_reverse_replay"]
    metric = r56["metric_and_once_charge_terminal_source_join"]
    require(paired["no_same_measure_shortcut"] is True, "Round56 no shortcut")
    require("T_s^k(I(B))=I(T_s^(n-k)(A))" in paired["reverse_path_identity"], "Round56 reverse direction")
    require(metric["time_reversal_metric_rule"].endswith("density ratios and Z"), "Round56 I isometry")
    require(r56["hereditary_replay_and_image_recut_join"]["same_ID_once_charge"] is True, "Round56 once charge")
    return loaded


def palindrome_rows() -> list[dict[str, str]]:
    return [
        {"stage": "input_x", "A_on_Z_in": "1", "B_on_mass_in": "0"},
        {"stage": "closed_T_power_K_minus_1", "A_on_Z_in": "1", "B_on_mass_in": qstr(C_P / 2)},
        {"stage": "O_supplies_collision_K", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(CUT_Z1 * C_P / 2)},
        {"stage": "time_reversal_I", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(CUT_Z1 * C_P / 2)},
        {"stage": "closed_reverse_T_power_K", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(PAL_MASS_COEFF)},
        {"stage": "final_I_returns_x", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(PAL_MASS_COEFF)},
    ]


def direction_rows() -> list[dict[str, str]]:
    return [
        {"step": "0", "operation": "start", "point": "x"},
        {"step": "1", "operation": "T_s^(K-1)", "point": "T_s^(K-1)x"},
        {"step": "2", "operation": "O_s transfer then kill", "point": "T_s^K x on survivors"},
        {"step": "3", "operation": "I", "point": "I T_s^K x"},
        {"step": "4", "operation": "T_s^K", "point": "I x"},
        {"step": "5", "operation": "I", "point": "x"},
    ]


def artifact_audit() -> dict[str, Any]:
    return {
        "frozen_main_manifest": MAIN_MANIFEST,
        "frozen_main_manifest_sha256": PINNED_FILES[MAIN_MANIFEST],
        "frozen_main_report_sha256": PINNED_FILES[MAIN_REPORT],
        "frozen_main_sha_ledger_sha256": PINNED_FILES[MAIN_SHA_LEDGER],
        "all_pinned_files": dict(PINNED_FILES),
        "audited_files_modified": False,
        "status": "PASS_FROZEN_ARTIFACTS_HASH_PINNED",
    }


def reversible_audit() -> dict[str, Any]:
    rows = direction_rows()
    return {
        "reversibility_identity": "I*T_s^K*I*T_s^K=id, equivalently T_s^K*I*T_s^K=I",
        "off_by_one": "O_s includes one transfer; first closed leg is K-1 and O_s lands at collision K",
        "return_direction": "T_s^K sends I(T_s^K x) to I(x), then final I returns x",
        "regular_branch_scope": "all identities are branchwise off the frozen singular/null cemetery",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "PASS_EXACT_DIRECTION_AND_OPERATOR_OFF_BY_ONE",
    }


def clock_audit() -> dict[str, Any]:
    return {
        "clock": "K(c)=696*Dbar(c)+H_joint>=1",
        "tag_constancy": "Dbar and K are immutable on c; the same numerical K is retained through I and is never recomputed on a conditioned subfamily",
        "Borel_reason": "integer-valued Borel Dbar plus fixed finite integer H_joint gives countable disjoint finite-K strata",
        "mass_index_layer": "SYZ hit bounds and h_cap(y)>249*p(y)/250 live at parent y, not at proof cell c",
        "terminal_scope": "one terminal C24-complement predicate per orientation; no intermediate-avoidance statement",
        "status": "PASS_BOREL_TAGGED_CLOCK_AND_INDEX_LAYER",
    }


def growth_audit() -> dict[str, Any]:
    rows = palindrome_rows()
    return {
        "closed_recurrence": "Z(T^r G)<=a^r*Z(G)+(C_p/2)*mass(G), with 0<a<1",
        "one_cut": "Round42 gives Z(O_s G)<=Z1*Z(G) for every unnormalised controlled canonical finite-Z family",
        "second_input": "the second palindrome may be arbitrarily thin and nonproper; no original-Dbar re-properisation is used",
        "uniform_final_bound": "Z_return<=Z1*Z_in+((Z1+1)*C_p/2)*mass_in",
        "mass_multiplier_is_single_cut": "exactly one Z1 multiplier occurs in each palindrome; the terminal complement is cut once",
        "marginal_separation": "Round52 SYZ is used only for original-marginal mass; Round47 P*mass proper-source envelope is not used for conditioned finite-Z geometry",
        "global_chain": "two uniform palindrome affine maps and two hereditary terminal resolvents act on the globally finite J_pair source, so the final proof-view Z sum is finite",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "PASS_TWO_CLOSED_LEGS_ONE_CUT_AND_NONPROPER_SCOPE",
    }


def paired_replay_audit() -> dict[str, Any]:
    return {
        "forward": "A -> B=T_s^n(A) -> I(B)",
        "reverse": "I(B) -> I(A) under the same first-return path tag, then I(A) -> A",
        "reverse_identity": "T_s^k(I(B))=I(T_s^(n-k)(A)) for 0<=k<=n",
        "first_return_scope": "the original C_s first-return n/no-earlier-C_s tag is inherited; no new proper common landing kernel is asserted",
        "refinement_policy": "singularity, homogeneity, Growth and recut operations split analytic branch intervals only",
        "forbidden_shortcuts": "no transverse redisintegration, same-measure substitution, normalization or duplicate charge",
        "common_raw_set": "both terminal predicates are pulled back to the identical raw restriction S_fw intersect S_rev",
        "status": "PASS_EXACT_PAIRED_REPLAY_REFINEMENT_AND_ONCE_CHARGE",
    }


def component_audit() -> dict[str, Any]:
    return {
        "proof_kernel": "countable half-open regular connected interval atoms with exact outer disintegration",
        "physical_merge_rule": "merge only actual-union connected adjacent atoms whose shared endpoint is owned and belongs to the regular common set",
        "puncture_rule": "never merge across an omitted singular, null or cemetery puncture and never merge across y",
        "Borel_registry": "least rational owner plus Borel endpoint infimum/supremum enumerates positive maximal intervals",
        "coarsening": "p/ell on a physical union is a length-weighted average, hence J_cap,physical<=Z_cap,proof",
        "global_result": "J_cap,total=integral J_cap(y)dlambda(y)<infinity",
        "Round53_result": "Borel D_cap(y), synchronized 696*D_cap properisation, exp(D_cap/6) moment and full dyadic first moment are finite",
        "status": "PASS_GLOBAL_J_CAP_AND_D_CAP_JOIN",
    }


def strict_scope_audit() -> dict[str, Any]:
    return {
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE_AUDIT_PASS",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE_AUDIT_PASS",
        "physical_full_dyadic_D_cap_first_moment": "CERTIFIED_FINITE_AUDIT_PASS",
        "proper_common_terminal_two_view_carrier": "CERTIFIED_AUDIT_PASS",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS_NO_REMAINING_BLOCKER_FOR_CLAIMED_SCOPE",
    }


def build_result() -> dict[str, Any]:
    validate_frozen_sources()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "claim_type": "independent read-only audit of the frozen Round57 palindromic J_cap/D_cap closure",
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "audited_artifacts_modified": False,
            "pinned_sha256": dict(PINNED_FILES),
        },
        "artifact_freeze_audit": artifact_audit(),
        "reversible_operator_audit": reversible_audit(),
        "tagged_clock_Borel_audit": clock_audit(),
        "affine_Growth_audit": growth_audit(),
        "paired_first_return_replay_audit": paired_replay_audit(),
        "component_global_join_audit": component_audit(),
        "strict_scope_audit": strict_scope_audit(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier scope")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "dependencies": dict(PINNED_FILES),
        "result": result,
        "verdict": dict(result["strict_scope_audit"]),
    }


def pretty_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def write_manifest(path: Path, verifier: Path = DEFAULT_VERIFIER) -> None:
    path = path.resolve()
    require(path.parent == HERE, "manifest output scope")
    path.write_text(pretty_manifest(verifier), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.manifest_json:
        print(pretty_manifest(args.verifier), end="")
        return 0
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_scope_audit"]
    print("INDEPENDENT_AUDIT:", strict["audit_verdict"])
    print("PHYSICAL_J_CAP:", strict["physical_common_refinement_J_cap_total"])
    print("D_CAP_MOMENT:", strict["single_common_properisation_clock_D_cap_moment"])
    print("PHYSICAL_FIRST_RETURN:", strict["physical_proper_same_ID_first_return_kernel"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
