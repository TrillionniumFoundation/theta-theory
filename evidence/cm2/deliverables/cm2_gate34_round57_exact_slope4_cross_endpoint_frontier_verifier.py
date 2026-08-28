#!/usr/bin/env python3
"""Independent verifier for the Round-57 cross-endpoint frontier leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "cm2_gate34_round57_exact_slope4_cross_endpoint_frontier_cert.py"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
)
RESULT_SCHEMA = "cm2.gate34.round57-exact-slope4-cross-endpoint-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
R = Q(2000, 1999)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )
    require(isinstance(value, dict), "manifest root")
    return value


def load_cert() -> Any:
    require(CERT_PATH.is_file() and not CERT_PATH.is_symlink(), "certificate path")
    spec = importlib.util.spec_from_file_location("cm2_r57_cross_cert", CERT_PATH)
    require(spec is not None and spec.loader is not None, "certificate spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


cert = load_cert()


def get_path(root: Any, path: tuple[str | int, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def set_path(root: Any, path: tuple[str | int, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


REQUIRED_FIELDS: list[tuple[tuple[str | int, ...], Any]] = [
    (("schema",), RESULT_SCHEMA),
    (("provenance", "old_artifacts_modified"), False),
    (("provenance", "external_theorem_promoted"), False),
    (
        ("direct_J_pair_rank_moment_consequence", "physical_full_dyadic_rank_first_moment"),
        "CERTIFIED_FINITE",
    ),
    (
        ("direct_J_pair_rank_moment_consequence", "integrated_bound"),
        "integral sum_c p_c*2^M_c<=nu(X)+2*J_pair<infinity",
    ),
    (
        ("direct_J_pair_rank_moment_consequence", "physical_full_dyadic_Dbar_first_moment"),
        "CERTIFIED_FINITE",
    ),
    (
        ("exact_slope4_cross_endpoint_separator", "common_mass"),
        "499/500>249/250",
    ),
    (
        ("exact_slope4_cross_endpoint_separator", "abstract_normalized_J_pair"),
        "2",
    ),
    (("exact_slope4_cross_endpoint_separator", "abstract_M"), 0),
    (
        ("exact_slope4_cross_endpoint_separator", "status"),
        "CERTIFIED_EXACT_SLOPE4_SAME_METRIC_CROSS_ENDPOINT_SEPARATOR",
    ),
    (
        ("cross_endpoint_component_theorem", "global_upper"),
        "J_cap,total<=R*(Z_fw,marginal+Z_rev,marginal+E_cross)",
    ),
    (
        ("cross_endpoint_component_theorem", "status"),
        "CERTIFIED_EXACT_CROSS_COMPONENT_EQUIVALENCE_AND_SHORTEST_INPUT",
    ),
    (
        ("cross_endpoint_component_theorem", "physical_input_supplied_in_this_leaf"),
        "YES_BY_PALINDROMIC_STOPPED_CUT_REPLAY",
    ),
    (
        ("palindromic_stopped_cut_replay", "exact_identity"),
        "the underlying surviving point reaches T_s^K x and I o T_s^K o I o T_s^K=id on every regular branch, equivalently T_s^K o I o T_s^K=I",
    ),
    (
        ("palindromic_stopped_cut_replay", "operator_off_by_one"),
        "O_s is the pinned one-collision transfer-plus-kill, not a pure current-time restriction; therefore the first closed leg is T_s^(K-1), then O_s supplies collision K",
    ),
    (
        ("palindromic_stopped_cut_replay", "terminal_time_choice"),
        "choose the pinned uniform terminal time H_joint>=1 beyond both Round52 SYZ thresholds",
    ),
    (
        ("palindromic_stopped_cut_replay", "terminal_cut_scope"),
        "the hash-pinned Round42 report states that every unnormalised C24-killed canonical family satisfies Z(O_s G)<=Z1 Z(G); no properness or survivor normalization is required",
    ),
    (
        ("palindromic_stopped_cut_replay", "second_palindrome_scope"),
        "after imposing the forward predicate and transferring to I(B), the input may be an arbitrarily thin nonproper positive canonical subfamily; the same Round42 arbitrary-finite-Z one-step bound applies",
    ),
    (
        ("palindromic_stopped_cut_replay", "status"),
        "CERTIFIED_UNBOUNDED_STOPPED_TIME_TERMINAL_CUT_PULLBACK_WITH_FINITE_Z",
    ),
    (
        ("physical_common_refinement_closure", "physical_J_cap_total"),
        "J_cap,total<=Z_cap,fw-proper-view,proof+Z_cap,rev-proper-view,proof<infinity",
    ),
    (
        ("physical_common_refinement_closure", "status"),
        "CERTIFIED_PHYSICAL_COMMON_REFINEMENT_J_CAP_AND_SINGLE_D_CAP_CLOCK",
    ),
    (
        ("physical_common_refinement_closure", "physical_common_mass"),
        "h_cap(y)>249*p(y)/250 from the pinned Round52 once-charged union bound at the y layer; no such lower bound is asserted for an individual proof cell c",
    ),
    (
        ("physical_common_refinement_closure", "physical_full_dyadic_D_cap_first_moment"),
        "CERTIFIED_FINITE",
    ),
    (
        ("independent_downstream_obstructions", "proper_same_ID_first_return", "status"),
        "INDEPENDENT_PHYSICAL_KERNEL_INTERFACE_NOT_CERTIFIED",
    ),
    (
        ("independent_downstream_obstructions", "intermediate_C24_avoidance", "status"),
        "TERMINAL_NONHIT_DOES_NOT_IMPLY_INTERMEDIATE_AVOIDANCE",
    ),
    (
        ("independent_downstream_obstructions", "later_repeated_clocks", "status"),
        "ONE_OR_FIXED_STAGE_CLOCK_MOMENTS_DO_NOT_IMPLY_ALL_STAGE_MOMENT",
    ),
    (
        ("latest_technical_literature_audit", "pdf_sha256"),
        "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798",
    ),
    (("latest_technical_literature_audit", "external_theorem_promoted"), False),
    (("strict_nonpromotion", "physical_J_pair"), "CERTIFIED_FINITE_PINNED_ROUND56"),
    (
        ("strict_nonpromotion", "physical_full_dyadic_length_rank_first_moment"),
        "CERTIFIED_FINITE",
    ),
    (("strict_nonpromotion", "physical_full_dyadic_Dbar_first_moment"), "CERTIFIED_FINITE"),
    (("strict_nonpromotion", "exact_cross_component_equivalence"), "CERTIFIED"),
    (("strict_nonpromotion", "exact_slope4_same_metric_nonimplication"), "CERTIFIED"),
    (("strict_nonpromotion", "palindromic_unbounded_stopped_cut_replay"), "CERTIFIED_FINITE_Z"),
    (("strict_nonpromotion", "physical_cross_endpoint_energy_E_cross"), "CERTIFIED_FINITE"),
    (("strict_nonpromotion", "physical_common_refinement_J_cap_total"), "CERTIFIED_FINITE"),
    (("strict_nonpromotion", "single_common_properisation_clock_D_cap_moment"), "CERTIFIED_FINITE"),
    (("strict_nonpromotion", "physical_full_dyadic_D_cap_first_moment"), "CERTIFIED_FINITE"),
    (("strict_nonpromotion", "proper_common_terminal_two_view_carrier"), "CERTIFIED"),
    (("strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "intermediate_C24_avoidance_after_properisation"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "physical_collision_time_q_L6over5"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "strong_singular_current_cemetery"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "Gate4"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "complete_composite_gates"), "0/5"),
    (("strict_nonpromotion", "CM2"), "NO-GO_FOR_CLAIM"),
]


def parse_q(text: str) -> Q:
    if "/" in text:
        a, b = text.split("/", 1)
        return Q(int(a), int(b))
    return Q(int(text))


def independent_arithmetic(result: dict[str, Any]) -> None:
    require(Q(499, 500) > Q(249, 250), "common mass strictness")
    require(Q(999, 1000) > Q(499, 500), "marginal mass strictness")
    require(Q(19, 20) > 0, "nongrazing density")

    rank = result["direct_J_pair_rank_moment_consequence"]
    require(rank["rows"] == cert.rank_moment_rows(), "rank rows replay")
    require(rank["rows_sha256"] == cert.digest(rank["rows"]), "rank rows digest")
    for row in rank["rows"]:
        require(parse_q(row["two_to_M"]) <= parse_q(row["one_plus_two_over_min_length"]), "rank row inequality")
    require(rank["full_dyadic_Dbar_bound"] == "integral sum_c p_c*2^Dbar(c)<=nu(X)+2^-309*(nu(X)+2*J_pair)<infinity", "Dbar bound")
    for m in (0, 1, 309, 310, 311, 400, 1000):
        d = 0 if m <= 310 else m - 309
        require(Q(2**d) <= 1 + Q(2**m, 2**309), "Dbar dyadic domination")

    sep = result["exact_slope4_cross_endpoint_separator"]
    require(sep["rows"] == cert.separator_rows(), "separator rows replay")
    require(sep["rows_sha256"] == cert.digest(sep["rows"]), "separator rows digest")
    prior_z = 0
    for row in sep["rows"]:
        k = row["K"]
        require(parse_q(row["forward_common_partial_mass"]) == Q(499, 500) * (1 - Q(1, 2**k)), "separator mass")
        require(int(row["forward_common_u_boundary_Z"]) == k, "separator forward Z")
        require(int(row["total_common_u_boundary_Z"]) == k + 1, "separator total Z")
        require(k > prior_z, "separator K increasing")
        prior_z = k
    require(sep["rows"][-1]["total_common_u_boundary_Z"] == "33", "separator visible divergence")

    theorem = result["cross_endpoint_component_theorem"]
    require(theorem["rows"] == cert.cross_component_rows(), "component rows replay")
    require(theorem["rows_sha256"] == cert.digest(theorem["rows"]), "component rows digest")
    for row in theorem["rows"]:
        n = row["positive_common_components_N"]
        base = parse_q(row["parent_boundary_density"])
        require(parse_q(row["lower_common_Z"]) == Q(n) * base / R, "component lower")
        require(parse_q(row["upper_common_Z"]) == Q(n) * base * R, "component upper")

    palindrome = result["palindromic_stopped_cut_replay"]
    require(palindrome["rows"] == cert.palindrome_affine_rows(), "palindrome rows replay")
    require(palindrome["rows_sha256"] == cert.digest(palindrome["rows"]), "palindrome rows digest")
    require(cert.CLOSED_A < 1, "closed recurrence contraction")
    require(cert.CUT_Z1 == Q(18367592526, 360493663), "terminal cut multiplier")
    require(cert.PAL_MASS_COEFF == (cert.CUT_Z1 + 1) * cert.C_P / 2, "palindrome mass coefficient")
    final_row = palindrome["rows"][-1]
    require(palindrome["rows"][1]["stage"] == "first_closed_T_power_K_minus_1", "palindrome off by one")
    require(parse_q(final_row["A_on_Z_in"]) == cert.CUT_Z1, "palindrome final A")
    require(parse_q(final_row["B_on_mass_in"]) == cert.PAL_MASS_COEFF, "palindrome final B")

    closure = result["physical_common_refinement_closure"]
    require("S_fw intersect S_rev" in closure["same_raw_restriction"], "common raw restriction")
    require(closure["physical_common_mass"].startswith("h_cap(y)>249*p(y)/250"), "common physical mass")
    require("finite physical c-fibre" in closure["per_y_finiteness"], "per-y finiteness")
    require(closure["global_integrability"].endswith("<infinity"), "global Jcap integrability")
    require("P(Z,m)=Z1*Z" in closure["global_affine_chain"] and "R(Z,m)=A_R*Z+B_R*m" in closure["global_affine_chain"], "global affine chain")
    require("independent of y,c,n,Dbar and K" in closure["uniformity_of_global_constants"], "global constant uniformity")
    require("least-rational owner" in closure["physical_maximal_component_registry"], "Borel maximal components")
    require("omitted singular, null or cemetery puncture is never merged" in closure["physical_maximal_component_registry"], "no puncture merge")
    require("J_cap,physical<=Z_cap,proof" in closure["coarsening_inequality"], "physical coarsening")
    require(closure["full_dyadic_D_cap_bound"].startswith("integral h(y)*2^D_cap(y)"), "Dcap dyadic bound")
    require("inherits the original tau_R=n" in closure["not_yet_physical_first_return"], "inherited return graph")
    require("not thereby the required proper common kernel" in closure["not_yet_physical_first_return"], "first-return nonpromotion")

    hits = result["latest_technical_literature_audit"]["targeted_text_hits"]
    require(hits == {"coupling": 1, "holonomy": 2, "standard_famil": 0, "common_return": 0, "common_refinement": 0, "same_ID": 0, "cemetery": 0}, "literature hits")


def independent_checks(manifest: dict[str, Any]) -> None:
    result = manifest["result"]
    for path, expected in REQUIRED_FIELDS:
        require(get_path(result, path) == expected, f"required field: {path}")
    require(manifest["verdict"] == result["strict_nonpromotion"], "verdict parity")
    require(result["internal_replay_digest"] == cert.digest({k: v for k, v in result.items() if k != "internal_replay_digest"}), "result digest")
    independent_arithmetic(result)


def verify_value(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(set(value) == set(expected), "top-level keys")
    require(value == expected, "deterministic manifest mismatch")
    require(value["schema"] == MANIFEST_SCHEMA, "manifest schema")
    require(value["certificate_sha256"] == sha256_path(CERT_PATH), "certificate hash")
    require(value["verifier_sha256"] == sha256_path(Path(__file__).resolve()), "verifier hash")
    require(value["dependencies"] == cert.DEPENDENCIES, "dependency ledger")
    require(value["pinned_reports"] == cert.PINNED_REPORTS, "pinned report ledger")
    independent_checks(value)


def verify_manifest(path: Path) -> tuple[dict[str, Any], bytes, bytes]:
    path = path.resolve()
    require(path.is_file() and not path.is_symlink(), "manifest path")
    require(path.parent == HERE, "manifest outside deliverables")
    raw = path.read_bytes()
    value = strict_load_bytes(raw)
    expected = cert.build_manifest(Path(__file__).resolve())
    verify_value(value, expected)
    for name, expected_hash in cert.DEPENDENCIES.items():
        dependency = HERE / name
        require(dependency.is_file() and not dependency.is_symlink(), f"dependency path: {name}")
        require(dependency.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(dependency) == expected_hash, f"dependency hash: {name}")
    for name, expected_hash in cert.PINNED_REPORTS.items():
        report = HERE / name
        require(report.is_file() and not report.is_symlink(), f"report path: {name}")
        require(report.resolve().parent == HERE, f"report scope: {name}")
        require(sha256_path(report) == expected_hash, f"report hash: {name}")
    reemitted = (json.dumps(expected, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return value, raw, reemitted


def hostile_mutations(base: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    def changed(path: tuple[str | int, ...], value: Any) -> None:
        item = copy.deepcopy(base)
        set_path(item, path, value)
        mutations.append(item)

    changed(("schema",), "bad.schema")
    changed(("certificate_sha256",), "0" * 64)
    changed(("verifier_sha256",), "1" * 64)
    changed(("dependencies",), {})
    changed(("pinned_reports",), {})
    changed(("result", "provenance", "old_artifacts_modified"), True)
    changed(("result", "provenance", "external_theorem_promoted"), True)
    changed(("result", "direct_J_pair_rank_moment_consequence", "physical_full_dyadic_rank_first_moment"), "NOT_CERTIFIED")
    changed(("result", "direct_J_pair_rank_moment_consequence", "integrated_bound"), "false")
    changed(("result", "direct_J_pair_rank_moment_consequence", "physical_full_dyadic_Dbar_first_moment"), "NOT_CERTIFIED")
    changed(("result", "direct_J_pair_rank_moment_consequence", "rows", 0, "inequality"), False)
    changed(("result", "direct_J_pair_rank_moment_consequence", "rows_sha256"), "2" * 64)
    changed(("result", "exact_slope4_cross_endpoint_separator", "common_mass"), "249/250")
    changed(("result", "exact_slope4_cross_endpoint_separator", "abstract_normalized_J_pair"), "infinity")
    changed(("result", "exact_slope4_cross_endpoint_separator", "abstract_M"), 1)
    changed(("result", "exact_slope4_cross_endpoint_separator", "scope"), "physical billiard counterexample")
    changed(("result", "exact_slope4_cross_endpoint_separator", "rows", 0, "total_common_u_boundary_Z"), "0")
    changed(("result", "exact_slope4_cross_endpoint_separator", "rows_sha256"), "3" * 64)
    changed(("result", "cross_endpoint_component_theorem", "global_upper"), "J_cap<=J_pair")
    changed(("result", "cross_endpoint_component_theorem", "global_reverse_control"), "false")
    changed(("result", "cross_endpoint_component_theorem", "shortest_new_physical_input"), "none")
    changed(("result", "cross_endpoint_component_theorem", "not_a_first_return"), "it is a first return")
    changed(("result", "cross_endpoint_component_theorem", "rows", 2, "upper_common_Z"), "0")
    changed(("result", "cross_endpoint_component_theorem", "rows_sha256"), "4" * 64)
    changed(("result", "cross_endpoint_component_theorem", "physical_input_supplied_in_this_leaf"), "NO")
    changed(("result", "palindromic_stopped_cut_replay", "exact_identity"), "false")
    changed(("result", "palindromic_stopped_cut_replay", "terminal_time_choice"), "H_joint=0")
    changed(("result", "palindromic_stopped_cut_replay", "terminal_cut_scope"), "proper only")
    changed(("result", "palindromic_stopped_cut_replay", "second_palindrome_scope"), "not applicable")
    changed(("result", "palindromic_stopped_cut_replay", "variable_K_bound"), "diverges")
    changed(("result", "palindromic_stopped_cut_replay", "cuts_only_refine"), "transverse")
    changed(("result", "palindromic_stopped_cut_replay", "rows", 5, "B_on_mass_in"), "0")
    changed(("result", "palindromic_stopped_cut_replay", "rows_sha256"), "6" * 64)
    changed(("result", "physical_common_refinement_closure", "same_raw_restriction"), "two charges")
    changed(("result", "physical_common_refinement_closure", "physical_common_mass"), "h_cap(c)>249*p_c/250")
    changed(("result", "physical_common_refinement_closure", "physical_maximal_component_registry"), "not Borel")
    changed(("result", "physical_common_refinement_closure", "physical_maximal_component_registry"), "merge whenever closures touch, including omitted singular endpoints")
    changed(("result", "physical_common_refinement_closure", "coarsening_inequality"), "reverse inequality")
    changed(("result", "physical_common_refinement_closure", "global_affine_chain"), "pointwise implies global")
    changed(("result", "physical_common_refinement_closure", "uniformity_of_global_constants"), "depends on K")
    changed(("result", "physical_common_refinement_closure", "physical_J_cap_total"), "infinity")
    changed(("result", "physical_common_refinement_closure", "actual_proper_object"), "physical first return")
    changed(("result", "physical_common_refinement_closure", "not_yet_physical_first_return"), "no stopping graph exists")
    changed(("result", "physical_common_refinement_closure", "status"), "NOT_CERTIFIED")
    changed(("result", "physical_common_refinement_closure", "physical_full_dyadic_D_cap_first_moment"), "NOT_CERTIFIED")
    changed(("result", "independent_downstream_obstructions", "proper_same_ID_first_return", "status"), "CERTIFIED")
    changed(("result", "independent_downstream_obstructions", "intermediate_C24_avoidance", "status"), "CERTIFIED")
    changed(("result", "independent_downstream_obstructions", "later_repeated_clocks", "status"), "CERTIFIED")
    changed(("result", "independent_downstream_obstructions", "physical_q_and_cemetery", "status"), "CERTIFIED")
    changed(("result", "latest_technical_literature_audit", "pdf_sha256"), "5" * 64)
    changed(("result", "latest_technical_literature_audit", "external_theorem_promoted"), True)
    changed(("result", "latest_technical_literature_audit", "targeted_text_hits", "common_return"), 1)
    changed(("result", "strict_nonpromotion", "physical_J_pair"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "palindromic_unbounded_stopped_cut_replay"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "physical_cross_endpoint_energy_E_cross"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "physical_common_refinement_J_cap_total"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "single_common_properisation_clock_D_cap_moment"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "proper_common_terminal_two_view_carrier"), "NOT_CERTIFIED")
    changed(("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "intermediate_C24_avoidance_after_properisation"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "complete_composite_gates"), "1/5")
    changed(("result", "strict_nonpromotion", "CM2"), "GO")
    changed(("result", "internal_replay_digest"), "f" * 64)
    changed(("verdict", "Gate4"), "CERTIFIED")
    item = copy.deepcopy(base)
    item["unexpected"] = True
    mutations.append(item)
    return mutations


def run_self_test(path: Path) -> int:
    base, raw, _ = verify_manifest(path)
    expected = cert.build_manifest(Path(__file__).resolve())
    rejected = 0
    mutations = hostile_mutations(base)
    for index, item in enumerate(mutations):
        try:
            verify_value(item, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"hostile mutation accepted: {index}")
    raw_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}']
    duplicate = raw.replace(
        b'{\n  "certificate_sha256"',
        b'{\n  "schema": "duplicate",\n  "certificate_sha256"',
        1,
    )
    raw_cases.append(duplicate)
    for item in raw_cases:
        try:
            strict_load_bytes(item)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("hostile raw JSON accepted")
    total = len(mutations) + len(raw_cases)
    require(rejected == total, "hostile count")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test(args.manifest)
    manifest, raw, reemitted = verify_manifest(args.manifest)
    if args.reemit:
        require(raw == reemitted, "re-emission mismatch")
        print("REEMIT_BYTE_IDENTICAL: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("DYADIC_RANK_MOMENT:", manifest["verdict"]["physical_full_dyadic_length_rank_first_moment"])
    print("PHYSICAL_E_CROSS:", manifest["verdict"]["physical_cross_endpoint_energy_E_cross"])
    print("PHYSICAL_J_CAP:", manifest["verdict"]["physical_common_refinement_J_cap_total"])
    print("PHYSICAL_Q:", manifest["verdict"]["physical_collision_time_q_L6over5"])
    print("GATE4:", manifest["verdict"]["Gate4"])
    print("CM2:", manifest["verdict"]["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
