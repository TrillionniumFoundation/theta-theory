#!/usr/bin/env python3
"""Independent verifier for the Round-58 unshifted-landing frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_cert.py"
MANIFEST_PATH = (
    HERE
    / "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
)
RESULT_SCHEMA = "cm2.gate4.round58-unshifted-landing-minimal-z-first-hit-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"

EXPECTED_DEPENDENCIES = {
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

EXPECTED_REPORTS = {
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-assault-2026-07-20.md": (
        "33cec817b1c809278353e12f18de7e94224523e1bd7a6c011ab62276fd32d489"
    ),
}

C_P = Q(4 * 10**90 * 360493663, 358863)
COMMON_MASS = Q(999, 1000)
GAP_MASS = Q(1, 1000)
N_COMPONENTS = C_P.numerator // C_P.denominator + 1
COMPONENT_LENGTH = COMMON_MASS / N_COMPONENTS
GAP_LENGTH = GAP_MASS / (N_COMPONENTS - 1)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def no_nonfinite(token: str) -> None:
    raise ValueError(f"non-finite token: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=no_nonfinite)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file() or MANIFEST_PATH.is_symlink():
        raise ValueError("manifest path")
    value = strict_load_text(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def dependency_check(data: dict[str, Any]) -> None:
    if data["dependencies"] != EXPECTED_DEPENDENCIES:
        raise ValueError("dependency registry drift")
    if data["pinned_reports"] != EXPECTED_REPORTS:
        raise ValueError("report registry drift")
    provenance = data["result"]["provenance"]
    if provenance["dependency_sha256"] != EXPECTED_DEPENDENCIES:
        raise ValueError("provenance dependency drift")
    if provenance["pinned_report_sha256"] != EXPECTED_REPORTS:
        raise ValueError("provenance report drift")
    for registry in (EXPECTED_DEPENDENCIES, EXPECTED_REPORTS):
        for name, expected in registry.items():
            path = HERE / name
            if (
                len(expected) != 64
                or not path.is_file()
                or path.is_symlink()
                or path.resolve().parent != HERE
                or sha256_path(path) != expected
            ):
                raise ValueError(f"pinned integrity: {name}")


def integrity_check(data: dict[str, Any]) -> None:
    if set(data) != {
        "certificate_sha256",
        "dependencies",
        "pinned_reports",
        "result",
        "schema",
        "verdict",
        "verifier_sha256",
    }:
        raise ValueError("top-level shape")
    if data["schema"] != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if not CERT_PATH.is_file() or CERT_PATH.is_symlink():
        raise ValueError("certificate path")
    if data["certificate_sha256"] != sha256_path(CERT_PATH):
        raise ValueError("certificate digest")
    if data["verifier_sha256"] != sha256_path(Path(__file__).resolve()):
        raise ValueError("verifier digest")
    dependency_check(data)
    result = data["result"]
    if result["schema"] != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay = copy.deepcopy(result)
    observed = replay.pop("internal_replay_digest")
    if observed != digest(replay):
        raise ValueError("internal replay digest")
    if data["verdict"] != result["strict_nonpromotion"]:
        raise ValueError("verdict mirror")


def expected_sample_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_index": str(index),
            "component_mass": qstr(COMPONENT_LENGTH),
            "component_length": qstr(COMPONENT_LENGTH),
            "component_Z": "1",
            "has_gap_after": index < N_COMPONENTS - 1,
            "gap_length_if_present": qstr(GAP_LENGTH) if index < N_COMPONENTS - 1 else "0",
        }
        for index in (0, 1, N_COMPONENTS - 2, N_COMPONENTS - 1)
    ]


def expected_reinduction_rows() -> list[dict[str, Any]]:
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


def expected_strict_frontier() -> dict[str, Any]:
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


def semantic_replay(data: dict[str, Any]) -> None:
    result = data["result"]
    if set(result) != {
        "finite_high_mass_Dcap_zero_separator",
        "full_ambient_marker_typing",
        "internal_replay_digest",
        "landing_bad_stratum_interface",
        "latest_technical_literature_audit",
        "maximal_component_minimum_Z_theorem",
        "once_covering_first_hit_reinduction",
        "pinned_input_audit",
        "provenance",
        "schema",
        "strict_nonpromotion",
    }:
        raise ValueError("result shape")

    provenance = result["provenance"]
    if provenance != {
        "claim_type": "maximal-component minimal-Z theorem, unshifted landing iff, ambient-marker separator, and once-covering reinduction frontier",
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "external_theorem_promoted": False,
        "old_artifacts_modified": False,
        "parameter_scope": "parameterwise for every fixed |s|<=1/400",
        "pinned_report_sha256": EXPECTED_REPORTS,
    }:
        raise ValueError("provenance")

    pinned = result["pinned_input_audit"]
    if pinned["status"] != "CERTIFIED_PINNED_INPUT_TYPE_AUDIT":
        raise ValueError("pinned audit")
    if "exactly once" not in pinned["Round56_full_induced_output"]:
        raise ValueError("full induced output")
    if "finite Z" not in pinned["Round57_physical_graph"]:
        raise ValueError("physical graph")
    if "neither" not in pinned["type_gap"]:
        raise ValueError("type gap")

    theorem = result["maximal_component_minimum_Z_theorem"]
    if theorem["status"] != "CERTIFIED_MAXIMAL_COMPONENT_EXACT_MINIMUM_AND_UNSHIFTED_PROPERNESS_IFF":
        raise ValueError("minimum theorem")
    if theorem["minimum_definition"] != "J_land,min(y)=sum_C kappa_y(C)/ell(C)":
        raise ValueError("minimum definition")
    if "monotone countable sum" not in theorem["Borel_measurability"]:
        raise ValueError("minimum Borel measurability")
    if "h(y)=0" not in theorem["zero_policy"] or "never normalized" not in theorem["zero_policy"]:
        raise ValueError("minimum zero policy")
    if "strictly positive regular density" not in theorem["lower_bound_proof"]:
        raise ValueError("support proof")
    if "attains" not in theorem["attainment"]:
        raise ValueError("minimum attainment")
    if "iff J_land,min(y)<C_p*h(y)" not in theorem["strict_same_time_iff"]:
        raise ValueError("properness iff")
    if "outer mass-weighted average" not in theorem["multiple_family_iff"] or "strictly <C_p" not in theorem["multiple_family_iff"]:
        raise ValueError("multiple-family iff")
    if theorem["threshold_C_p"] != qstr(C_P):
        raise ValueError("proper threshold")
    if "future cross-y or cross-chart" not in theorem["cross_registry_guard"]:
        raise ValueError("cross-registry guard")
    if "J_land,min,total<=Z_3<infinity" not in theorem["Round57_global_join"]:
        raise ValueError("global landing join")

    separator = result["finite_high_mass_Dcap_zero_separator"]
    if separator["status"] != "CERTIFIED_FINITE_HIGH_MASS_DCAP_ZERO_UNSHIFTED_LANDING_SEPARATOR":
        raise ValueError("separator status")
    if separator["N"] != str(N_COMPONENTS) or separator["N_rule"] != "floor(C_p)+1":
        raise ValueError("separator N")
    if separator["component_length"] != qstr(COMPONENT_LENGTH):
        raise ValueError("component length")
    if separator["gap_length"] != qstr(GAP_LENGTH):
        raise ValueError("gap length")
    if separator["physical_landing_J_min"] != str(N_COMPONENTS):
        raise ValueError("landing J")
    if separator["physical_landing_normalized_Z_min"] != qstr(Q(N_COMPONENTS) / COMMON_MASS):
        raise ValueError("landing normalized Z")
    if separator["physical_landing_improper"] is not True:
        raise ValueError("landing improper")
    if separator["reference_two_view_J_cap"] != "2":
        raise ValueError("reference Jcap")
    if separator["reference_z_cap"] != qstr(Q(2) / COMMON_MASS):
        raise ValueError("reference zcap")
    if separator["reference_D_cap"] != 0:
        raise ValueError("reference Dcap")
    if "true positive gaps" not in separator["physical_ID_and_gap_policy"]:
        raise ValueError("physical gap policy")
    if "not a same-coordinate physical coarsening" not in separator["reference_type_guard"]:
        raise ValueError("reference type guard")
    if "J_cap=1+1=2" not in separator["reference_type_guard"]:
        raise ValueError("reference Jcap typing")
    rows = expected_sample_rows()
    if separator["sample_rows"] != rows or separator["sample_rows_sha256"] != digest(rows):
        raise ValueError("separator rows")
    if not (Q(N_COMPONENTS - 1) <= C_P < Q(N_COMPONENTS)):
        raise ValueError("independent ceiling")
    if N_COMPONENTS * COMPONENT_LENGTH + (N_COMPONENTS - 1) * GAP_LENGTH != 1:
        raise ValueError("independent partition")
    if not (Q(21, 111718750) < GAP_MASS < Q(1, 500)):
        raise ValueError("independent hit window")
    if not (COMMON_MASS > Q(249, 250)):
        raise ValueError("independent common mass")
    if not (Q(N_COMPONENTS) / COMMON_MASS > C_P > Q(2) / COMMON_MASS):
        raise ValueError("physical/reference separation")

    marker = result["full_ambient_marker_typing"]
    if marker["status"] != "CERTIFIED_FULL_AMBIENT_RETURN_PLUS_MARKER_IS_WEAK_ONLY_WITHOUT_LANDING_THRESHOLD":
        raise ValueError("marker status")
    if "J_land,min" not in marker["strong_level"]:
        raise ValueError("marker strong cost")
    if "cannot absorb" not in marker["full_output_nonimplication"]:
        raise ValueError("ambient nonimplication")
    if "same-coordinate" not in marker["required_multiplier_interface"]:
        raise ValueError("required multiplier")

    bad = result["landing_bad_stratum_interface"]
    if bad["status"] != "CERTIFIED_BAD_STRATUM_TAIL_AND_EXACT_MISSING_THRESHOLD":
        raise ValueError("bad stratum status")
    if "D_land=0" not in bad["landing_defect"]:
        raise ValueError("Dland definition")
    if "z_land=C_p" not in bad["strict_boundary"] or "D_land=2" not in bad["strict_boundary"]:
        raise ValueError("Dland strict boundary")
    if "2^D_land<=4*z_land/C_p" not in bad["dyadic_pointwise_bound"]:
        raise ValueError("Dland pointwise")
    if "H+(4/C_p)*J_land,min,total<infinity" not in bad["dyadic_moment"]:
        raise ValueError("Dland moment")
    if "J_land,min,total/(2^k*C_p)" not in bad["markov_bound"]:
        raise ValueError("bad tail")
    if "only finite/small, not zero" not in bad["why_not_closure"]:
        raise ValueError("bad mass guard")
    if "D_cap is computed" not in bad["D_cap_independence"] or "D_land" not in bad["D_cap_independence"]:
        raise ValueError("Dcap/Dland guard")
    if "cannot be appended" not in bad["clock_typing"]:
        raise ValueError("Dland clock typing")

    reinduced = result["once_covering_first_hit_reinduction"]
    if reinduced["status"] != "CERTIFIED_ONCE_COVERING_NEXT_RETURN_FINITE_Z__PROPERNESS_AND_ORIGINAL_TIME_REMAIN_OPEN":
        raise ValueError("reinduction status")
    if "exactly once" not in reinduced["once_covering_extraction"]:
        raise ValueError("once covering")
    if "finite aggregate landing Z" not in reinduced["finite_Z_consequence"]:
        raise ValueError("next landing Z")
    if "second return" not in reinduced["rebase_from_physical_landing"]:
        raise ValueError("rebase occurrence")
    if "remains" not in reinduced["source_problem"]:
        raise ValueError("rebase source guard")
    if "not a C_s-to-C_s first-return kernel" not in reinduced["reference_view_variant"]:
        raise ValueError("entrance/return guard")
    rrows = expected_reinduction_rows()
    if reinduced["separator_rows"] != rrows or reinduced["separator_rows_sha256"] != digest(rrows):
        raise ValueError("reinduction rows")
    if any(row["landing_is_proper"] for row in rrows):
        raise ValueError("reinduction separator")

    literature = result["latest_technical_literature_audit"]
    if literature["status"] != "AUDITED_NO_DIRECT_SAME_TIME_LANDING_PROPERNESS_THEOREM_FOUND":
        raise ValueError("literature status")
    if literature["external_theorem_promoted"] is not False:
        raise ValueError("literature promotion")
    if len(literature["official_sources"]) != 3:
        raise ValueError("literature sources")

    if result["strict_nonpromotion"] != expected_strict_frontier():
        raise ValueError("strict frontier")


def validate(data: dict[str, Any]) -> None:
    integrity_check(data)
    semantic_replay(data)


def assign_path(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load_manifest()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("dependencies", "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"), "0" * 64),
        (("pinned_reports", "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-assault-2026-07-20.md"), "0" * 64),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "external_theorem_promoted"), True),
        (("result", "pinned_input_audit", "status"), "NOT_CERTIFIED"),
        (("result", "pinned_input_audit", "Round56_full_induced_output"), "two charges"),
        (("result", "pinned_input_audit", "Round57_physical_graph"), "no Z"),
        (("result", "pinned_input_audit", "type_gap"), "equivalent"),
        (("result", "maximal_component_minimum_Z_theorem", "status"), "NOT_CERTIFIED"),
        (("result", "maximal_component_minimum_Z_theorem", "minimum_definition"), "J=0"),
        (("result", "maximal_component_minimum_Z_theorem", "Borel_measurability"), "nonmeasurable"),
        (("result", "maximal_component_minimum_Z_theorem", "zero_policy"), "normalize zero"),
        (("result", "maximal_component_minimum_Z_theorem", "lower_bound_proof"), "cross gaps"),
        (("result", "maximal_component_minimum_Z_theorem", "attainment"), "unknown"),
        (("result", "maximal_component_minimum_Z_theorem", "strict_same_time_iff"), "finite iff"),
        (("result", "maximal_component_minimum_Z_theorem", "multiple_family_iff"), "splitting always repairs"),
        (("result", "maximal_component_minimum_Z_theorem", "threshold_C_p"), "1"),
        (("result", "maximal_component_minimum_Z_theorem", "cross_registry_guard"), "all redisintegrations excluded"),
        (("result", "maximal_component_minimum_Z_theorem", "Round57_global_join"), "recordwise only"),
        (("result", "finite_high_mass_Dcap_zero_separator", "status"), "CERTIFIED_PROPER"),
        (("result", "finite_high_mass_Dcap_zero_separator", "N"), "1"),
        (("result", "finite_high_mass_Dcap_zero_separator", "component_length"), "1"),
        (("result", "finite_high_mass_Dcap_zero_separator", "gap_length"), "1"),
        (("result", "finite_high_mass_Dcap_zero_separator", "physical_landing_J_min"), "1"),
        (("result", "finite_high_mass_Dcap_zero_separator", "physical_landing_normalized_Z_min"), "1"),
        (("result", "finite_high_mass_Dcap_zero_separator", "physical_landing_improper"), False),
        (("result", "finite_high_mass_Dcap_zero_separator", "reference_two_view_J_cap"), "0"),
        (("result", "finite_high_mass_Dcap_zero_separator", "reference_z_cap"), "0"),
        (("result", "finite_high_mass_Dcap_zero_separator", "reference_D_cap"), 2),
        (("result", "finite_high_mass_Dcap_zero_separator", "physical_ID_and_gap_policy"), "merge gaps"),
        (("result", "finite_high_mass_Dcap_zero_separator", "reference_type_guard"), "physical coarsening"),
        (("result", "finite_high_mass_Dcap_zero_separator", "sample_rows", 0, "component_Z"), "0"),
        (("result", "finite_high_mass_Dcap_zero_separator", "sample_rows", 3, "has_gap_after"), True),
        (("result", "finite_high_mass_Dcap_zero_separator", "sample_rows_sha256"), "0" * 64),
        (("result", "full_ambient_marker_typing", "status"), "CERTIFIED_PHYSICAL_KERNEL"),
        (("result", "full_ambient_marker_typing", "strong_level"), "ambient Z"),
        (("result", "full_ambient_marker_typing", "full_output_nonimplication"), "implies"),
        (("result", "full_ambient_marker_typing", "required_multiplier_interface"), "any coordinate"),
        (("result", "landing_bad_stratum_interface", "status"), "CLOSED"),
        (("result", "landing_bad_stratum_interface", "landing_defect"), "D_land=0 always"),
        (("result", "landing_bad_stratum_interface", "strict_boundary"), "equality proper"),
        (("result", "landing_bad_stratum_interface", "dyadic_pointwise_bound"), "unbounded"),
        (("result", "landing_bad_stratum_interface", "dyadic_moment"), "infinite"),
        (("result", "landing_bad_stratum_interface", "markov_bound"), "zero"),
        (("result", "landing_bad_stratum_interface", "why_not_closure"), "null"),
        (("result", "landing_bad_stratum_interface", "D_cap_independence"), "D_cap=D_land"),
        (("result", "landing_bad_stratum_interface", "clock_typing"), "append to tau"),
        (("result", "once_covering_first_hit_reinduction", "status"), "CERTIFIED_PROPER_ORIGINAL_RETURN"),
        (("result", "once_covering_first_hit_reinduction", "once_covering_extraction"), "double charge"),
        (("result", "once_covering_first_hit_reinduction", "finite_Z_consequence"), "proper"),
        (("result", "once_covering_first_hit_reinduction", "rebase_from_physical_landing"), "original return"),
        (("result", "once_covering_first_hit_reinduction", "source_problem"), "proper"),
        (("result", "once_covering_first_hit_reinduction", "reference_view_variant"), "physical return"),
        (("result", "once_covering_first_hit_reinduction", "separator_rows", 0, "landing_is_proper"), True),
        (("result", "once_covering_first_hit_reinduction", "separator_rows_sha256"), "0" * 64),
        (("result", "latest_technical_literature_audit", "status"), "THEOREM_FOUND"),
        (("result", "latest_technical_literature_audit", "external_theorem_promoted"), True),
        (("result", "latest_technical_literature_audit", "official_sources"), []),
        (("result", "strict_nonpromotion", "maximal_component_exact_minimum_Z"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_unshifted_J_land_min_total"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_unshifted_D_land_full_dyadic_moment"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "full_ambient_return_plus_common_marker_strong_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "once_covering_rebased_next_return_graph"), "CERTIFIED_PROPER"),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_landing_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "intermediate_C24_avoidance_during_added_recovery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        (("verdict", "Gate4"), "CERTIFIED"),
    ]
    rejected = 0
    accepted: list[tuple[Any, ...]] = []
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        try:
            validate(candidate)
        except (OSError, ValueError, KeyError, TypeError):
            rejected += 1
        else:
            accepted.append(path)

    strict_cases = (
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
        '[1,2,3]',
    )
    for payload in strict_cases:
        try:
            parsed = strict_load_text(payload)
            if not isinstance(parsed, dict):
                raise ValueError("strict root")
        except ValueError:
            rejected += 1
    if accepted:
        raise ValueError(f"hostile mutations accepted: {accepted}")
    return rejected, len(mutations) + len(strict_cases)


def generator_replay(manifest_bytes: bytes) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT_PATH), "--manifest-json"],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ValueError(f"generator exit {proc.returncode}: {proc.stderr.decode(errors='replace')}")
    if proc.stdout != manifest_bytes:
        raise ValueError("generator reemit mismatch")


def encoded(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        validate(data)
        if args.self_test:
            rejected, total = hostile_self_test()
            if rejected != total:
                raise ValueError(f"hostile rejection shortfall {rejected}/{total}")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 0
        if args.replay:
            generator_replay(MANIFEST_PATH.read_bytes())
        if args.reemit is not None:
            target = args.reemit.resolve()
            if target.parent != HERE:
                raise ValueError("reemit outside deliverables")
            target.write_text(encoded(data), encoding="utf-8")
            print(f"REEMIT: {target}")
            return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(f"ROUND58_GATE4_LANDING_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.integrity_only or args.replay:
        print("ROUND58_GATE4_LANDING_INTEGRITY: PASS")
        print("MINIMAL_Z_AND_REINDUCTION_REPLAY: PASS")
        print("NO_GATE_PROMOTION: PASS")
        return 0

    strict = data["result"]["strict_nonpromotion"]
    print("J_LAND_MIN:", strict["physical_unshifted_J_land_min_total"])
    print("D_LAND_MOMENT:", strict["physical_unshifted_D_land_full_dyadic_moment"])
    print("UNSHIFTED_PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
