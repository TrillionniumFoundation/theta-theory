#!/usr/bin/env python3
"""Fail-closed verifier for the Round-50 whole-family grouping leaf."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round50_physical_whole_family_grouping_cert as cert


TOP_LEVEL_KEYS = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    if set(value) != TOP_LEVEL_KEYS:
        raise ValueError("manifest exact top-level keys")
    return value


def expected_defect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for M in (0, 14, 299, 310, 311, 319, 330, 400):
        d = cert.safe_defect_from_min_length_rank(M)
        rows.append(
            {
                "common_min_length_rank_M": M,
                "common_Z_over_mass_upper": f"2^{M}",
                "safe_defect_Dbar": d,
                "preproperization_clock": 696 * d,
                "already_proper_from_upper_bound": d == 0,
            }
        )
    return rows


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    a = Q(360134800, 360493663)
    cp = Q(4 * 10**90 * 360493663, 358863)
    if Q(2 * 10**90) / (1 - a) != cp / 2:
        errors.append("steady term")
    if not 2 * 360134800**695 > 360493663**695:
        errors.append("695 comparison")
    if not 2 * 360134800**696 < 360493663**696:
        errors.append("696 comparison")
    if Q(696, 4176) != Q(1, 6):
        errors.append("preclock exponent")
    if (Q(6, 5) - 1) / (1 - Q(6, 5) / 2) != Q(1, 2):
        errors.append("tail layer cake")

    rows = expected_defect_rows()
    grouping = result.get("physical_Borel_whole_family_grouping", {})
    if grouping.get("sample_defect_rows") != rows:
        errors.append("defect rows")
    if grouping.get("sample_defect_rows_sha256") != cert.digest(rows):
        errors.append("defect digest")
    for row in rows:
        M = row["common_min_length_rank_M"]
        d = row["safe_defect_Dbar"]
        ratio = Q(2**M)
        if d == 0:
            if ratio > cp:
                errors.append("zero defect unsafe")
        else:
            if not Q(1, 2**d) * ratio < cp / 2:
                errors.append("defect insufficient")
            if d > 1 and not Q(1, 2 ** (d - 1)) * ratio >= cp / 2:
                errors.append("defect not minimal")

    counter = result.get("D1_inverse_length_nonimplication", {})
    rows2 = counter.get("rows", [])
    if counter.get("rows_sha256") != cert.digest(rows2):
        errors.append("countermodel digest")
    if len(rows2) != 5:
        errors.append("countermodel row count")
    for row in rows2:
        n = row["band_n"]
        count = 2 ** (n * n)
        width = Q(1, 2**n)
        length = Q(1, count)
        if width * count * length != width:
            errors.append("countermodel mass")
        if (width * count) / width != count:
            errors.append("countermodel J ratio")
        d = 0
        if Q(count) > cp:
            d = 1
            while Q(1, 2**d) * count >= cp / 2:
                d += 1
        if row["safe_actual_defect"] != d:
            errors.append("countermodel defect")

    replay = copy.deepcopy(result)
    stored = replay.pop("internal_replay_digest", None)
    if stored != cert.digest(replay):
        errors.append("internal replay digest")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink() or path.resolve().parent != cert.HERE:
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")
        result = source.get("result", {})
        if not isinstance(result, dict):
            return errors + ["result type"]
        errors.extend(independent_arithmetic(result))

        grouping = result.get("physical_Borel_whole_family_grouping", {})
        if grouping.get("status") != (
            "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J"
        ):
            errors.append("grouping status")
        if "forget natural-short-cell-k" not in grouping.get("grouping_projection", ""):
            errors.append("whole-cell grouping")
        if "uniform finite rank-path derivative product" not in grouping.get(
            "why_each_group_has_finitely_many_cells", ""
        ):
            errors.append("finite-cell reason")
        if "half-open" not in grouping.get("half_open_endpoint_owner", ""):
            errors.append("endpoint owner")
        if "exactly one owner" not in grouping.get("endpoint_scope", ""):
            errors.append("endpoint uniqueness")
        if "changes no positive-mass Round35 restriction" not in grouping.get(
            "upstream_recut_compatibility", ""
        ):
            errors.append("upstream recut compatibility")
        if grouping.get("finite_rank_path_derivative_product") != (
            "D_path(y)=product_{i=1}^n(150*2^B_i)<infinity for every fixed finite incidence-rank path"
        ):
            errors.append("rank-path derivative product")
        if grouping.get("image_length_bound") != (
            "length(H(A_k))<=D_path(y)*length(A_k)<infinity"
        ):
            errors.append("finite image length")
        if "Lusin-Novikov" not in grouping.get("finite_fibre_Borel_projection", ""):
            errors.append("finite-fibre Borel projection")
        identities = grouping.get("kernel_partition_identities_mod_null", [])
        if identities != [
            "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
            "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
        ]:
            errors.append("mod-null kernel identities")
        if "half-open ownership" not in grouping.get("kernel_identity_scope", ""):
            errors.append("kernel identity endpoint scope")
        if "modulo its null boundary" not in grouping.get("exact_outer_disintegration", ""):
            errors.append("mod-null outer disintegration")
        if grouping.get("physical_full_registry_reconstructed") is not True:
            errors.append("physical reconstruction")
        if grouping.get("numeric_nonempty_component_enumeration_claimed") is not False:
            errors.append("enumeration overclaim")
        if grouping.get("uniform_J_over_mass_bound_claimed") is not False:
            errors.append("uniform J overclaim")
        if len(grouping.get("boundary_numerators", [])) != 2:
            errors.append("two boundary numerators")

        proper = result.get("recordwise_properization_and_common_parent_law", {})
        if proper.get("status") != (
            "CERTIFIED_RECORDWISE_TWO_ORIENTATION_PROPERIZATION__COMMON_PARENT_LAW_JOIN_NOT_INSTALLED"
        ):
            errors.append("properization status")
        if proper.get("two_orientation_boundary_bound") != "max(J_fw,J_rev)<=2^M*p(y)":
            errors.append("two-orientation Z bound")
        if proper.get("common_preproperization_clock") != "R0(y)=696*Dbar(M(y))":
            errors.append("preclock")
        if proper.get("raw_K_par_is_a_proper_whole_family") is not False:
            errors.append("raw K_par properness overclaim")
        if "does not make the raw K_par geometry proper" not in proper.get(
            "raw_K_par_type_mismatch_with_Round49", ""
        ):
            errors.append("raw K_par type mismatch")
        if proper.get("literal_single_common_proper_kernel") != "NOT_INSTALLED":
            errors.append("literal common proper kernel overclaim")
        if proper.get("two_proper_view_pullback_lemma") != "NOT_INSTALLED":
            errors.append("two-proper-view pullback overclaim")
        if proper.get("Round49_W_r_hypotheses_after_recordwise_properization") is not False:
            errors.append("W_r literal join overclaim")
        if proper.get("postproperization_fixed_H_W_r_moment_certified") is not False:
            errors.append("W_r moment overclaim")
        if proper.get("preproperization_clock_included_in_conditional_W_r") is not False:
            errors.append("preclock overclaim")
        if "exp(Dbar(y)/6)" not in proper.get("missing_integrability_for_total_clock", ""):
            errors.append("missing moment")
        if "(6/5)^Dbar" not in proper.get("rational_sufficient_moment", ""):
            errors.append("rational moment")

        bridge = result.get("conditional_linear_short_length_tail_bridge", {})
        if bridge.get("status") != "CERTIFIED_CONDITIONAL_LINEAR_SHORT_LENGTH_TAIL_BRIDGE":
            errors.append("tail bridge status")
        if bridge.get("conditional_bound") != (
            "integral (6/5)^M p <= mass_total+C_len/2"
        ):
            errors.append("tail bridge bound")
        if bridge.get("available_for_physical_arbitrary_Rn_grouped_restrictions") is not False:
            errors.append("tail overclaim")
        if bridge.get("Round26_C24_one_step_tube_is_this_same_measure_kernel") is not False:
            errors.append("tube mismatch")

        counter = result.get("D1_inverse_length_nonimplication", {})
        if counter.get("status") != "CERTIFIED_EXACT_D1_VERSUS_INVERSE_LENGTH_NONIMPLICATION":
            errors.append("countermodel status")
        if counter.get("Round35_D1_implies_D_Z_moment") is not False:
            errors.append("D1 implication overclaim")
        if "not asserted to be an actual billiard" not in counter.get("logical_scope", ""):
            errors.append("countermodel scope")

        cemetery = result.get("cemetery_frontier", {})
        if cemetery.get("status") != "CERTIFIED_WEAK_MASS_CEMETERY_ONLY":
            errors.append("cemetery status")
        if cemetery.get("Borel_and_nested") is not True:
            errors.append("Borel exhaustion")
        if cemetery.get("union_covers_regular_registry") is not True:
            errors.append("exhaustion coverage")
        if "fixed (s,n)" not in cemetery.get("scope", ""):
            errors.append("fixed-depth cemetery scope")
        if cemetery.get("global_depth_owner") != (
            "return depth n is an explicit code rank in E_M^global"
        ):
            errors.append("global depth cemetery owner")
        if "n<=M" not in cemetery.get("finite_rank_exhaustion", ""):
            errors.append("global depth exhaustion")
        if cemetery.get("weak_L1_cemetery") != "CERTIFIED":
            errors.append("weak cemetery")
        for key in ("discarded_boundary_J_tends_to_zero", "discarded_D_Z_weighted_mass_tends_to_zero"):
            if cemetery.get(key) != "NOT_CERTIFIED":
                errors.append(f"strong cemetery overclaim: {key}")
        if cemetery.get("strong_trace_current_cemetery") != "NOT_CERTIFIED":
            errors.append("strong cemetery field")
        if cemetery.get("proper_common_fw_rev_intersection") != "NOT_CERTIFIED":
            errors.append("intersection overclaim")

        frontier = result.get("corrected_frontier", {})
        for key in (
            "Borel_family_id",
            "exact_outer_disintegration_reconstructing_physical_mass",
            "recordwise_finite_J_fw_J_rev",
            "Borel_D_Z_and_recordwise_696_D_Z_properization",
        ):
            if frontier.get(key) != "CERTIFIED":
                errors.append(f"frontier missing: {key}")
        if frontier.get("raw_K_par_is_Round49_proper_outer_kernel") is not False:
            errors.append("frontier raw K_par overclaim")
        if frontier.get("two_proper_view_pullback_lemma") != "NOT_INSTALLED":
            errors.append("frontier pullback overclaim")
        if frontier.get("same_ID_common_parent_law_join_after_recordwise_properization") != (
            "NOT_CERTIFIED"
        ):
            errors.append("frontier common law")
        if frontier.get("conditional_postproperization_W_r_formula") != (
            "CERTIFIED_CONDITIONAL_ON_TWO_PROPER_VIEW_PULLBACK_LEMMA"
        ):
            errors.append("frontier conditional W_r formula")
        for key in (
            "physical_exponential_moment_of_preproperization_D_Z",
            "full_total_clock_common_law_Lp_join",
            "proper_common_fw_rev_intersection",
            "complete_numeric_C_fw_C_rev_q",
            "strong_cemetery",
        ):
            if frontier.get(key) != "NOT_CERTIFIED":
                errors.append(f"frontier overclaim: {key}")
        if frontier.get("numeric_H_cover") is not None or frontier.get("numeric_actual_beta") is not None:
            errors.append("cover overclaim")

        expected = {
            "physical_Borel_whole_standard_family_grouping": "CERTIFIED",
            "recordwise_finite_J_and_properization": "CERTIFIED",
            "postproperization_same_ID_common_parent_law": "NOT_CERTIFIED",
            "Round49_W_r_literal_join": "NOT_INSTALLED",
            "global_preproperization_clock_moment": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[Any, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "parameter_scope"), "joint s"),
        (("result", "physical_Borel_whole_family_grouping", "status"), "NOT_CERTIFIED"),
        (("result", "physical_Borel_whole_family_grouping", "Borel_family_id"), "none"),
        (("result", "physical_Borel_whole_family_grouping", "grouping_projection"), "one cell"),
        (("result", "physical_Borel_whole_family_grouping", "why_each_group_has_finitely_many_cells"), "finite mass"),
        (("result", "physical_Borel_whole_family_grouping", "half_open_endpoint_owner"), "closed overlap"),
        (("result", "physical_Borel_whole_family_grouping", "endpoint_scope"), "double owner"),
        (("result", "physical_Borel_whole_family_grouping", "upstream_recut_compatibility"), "changes mass"),
        (("result", "physical_Borel_whole_family_grouping", "finite_rank_path_derivative_product"), "pointwise finite"),
        (("result", "physical_Borel_whole_family_grouping", "image_length_bound"), "unbounded"),
        (("result", "physical_Borel_whole_family_grouping", "finite_fibre_Borel_projection"), "projection is automatically Borel"),
        (("result", "physical_Borel_whole_family_grouping", "kernel_partition_identities_mod_null"), []),
        (("result", "physical_Borel_whole_family_grouping", "kernel_identity_scope"), "double count endpoints"),
        (("result", "physical_Borel_whole_family_grouping", "exact_outer_disintegration"), "surrogate measure"),
        (("result", "physical_Borel_whole_family_grouping", "physical_full_registry_reconstructed"), False),
        (("result", "physical_Borel_whole_family_grouping", "numeric_nonempty_component_enumeration_claimed"), True),
        (("result", "physical_Borel_whole_family_grouping", "uniform_J_over_mass_bound_claimed"), True),
        (("result", "physical_Borel_whole_family_grouping", "boundary_numerators"), []),
        (("result", "physical_Borel_whole_family_grouping", "sample_defect_rows"), []),
        (("result", "physical_Borel_whole_family_grouping", "sample_defect_rows_sha256"), "0" * 64),
        (("result", "recordwise_properization_and_common_parent_law", "status"), "GLOBAL"),
        (("result", "recordwise_properization_and_common_parent_law", "two_orientation_boundary_bound"), "false"),
        (("result", "recordwise_properization_and_common_parent_law", "safe_defect"), "0"),
        (("result", "recordwise_properization_and_common_parent_law", "common_preproperization_clock"), "0"),
        (("result", "recordwise_properization_and_common_parent_law", "raw_K_par_is_a_proper_whole_family"), True),
        (("result", "recordwise_properization_and_common_parent_law", "raw_K_par_type_mismatch_with_Round49"), "no mismatch"),
        (("result", "recordwise_properization_and_common_parent_law", "literal_single_common_proper_kernel"), "INSTALLED"),
        (("result", "recordwise_properization_and_common_parent_law", "two_proper_view_pullback_lemma"), "INSTALLED"),
        (("result", "recordwise_properization_and_common_parent_law", "Round49_W_r_hypotheses_after_recordwise_properization"), True),
        (("result", "recordwise_properization_and_common_parent_law", "postproperization_fixed_H_W_r_moment_certified"), True),
        (("result", "recordwise_properization_and_common_parent_law", "preproperization_clock_included_in_conditional_W_r"), True),
        (("result", "recordwise_properization_and_common_parent_law", "missing_integrability_for_total_clock"), "none"),
        (("result", "recordwise_properization_and_common_parent_law", "rational_sufficient_moment"), "none"),
        (("result", "conditional_linear_short_length_tail_bridge", "status"), "UNCONDITIONAL"),
        (("result", "conditional_linear_short_length_tail_bridge", "conditional_bound"), "infinite"),
        (("result", "conditional_linear_short_length_tail_bridge", "available_for_physical_arbitrary_Rn_grouped_restrictions"), True),
        (("result", "conditional_linear_short_length_tail_bridge", "Round26_C24_one_step_tube_is_this_same_measure_kernel"), True),
        (("result", "D1_inverse_length_nonimplication", "status"), "NO_OBSTRUCTION"),
        (("result", "D1_inverse_length_nonimplication", "Round35_D1_implies_D_Z_moment"), True),
        (("result", "D1_inverse_length_nonimplication", "logical_scope"), "actual billiard theorem"),
        (("result", "D1_inverse_length_nonimplication", "rows"), []),
        (("result", "D1_inverse_length_nonimplication", "rows_sha256"), "0" * 64),
        (("result", "cemetery_frontier", "status"), "STRONG"),
        (("result", "cemetery_frontier", "Borel_and_nested"), False),
        (("result", "cemetery_frontier", "union_covers_regular_registry"), False),
        (("result", "cemetery_frontier", "scope"), "unscoped"),
        (("result", "cemetery_frontier", "global_depth_owner"), "n omitted"),
        (("result", "cemetery_frontier", "finite_rank_exhaustion"), "n unbounded"),
        (("result", "cemetery_frontier", "weak_L1_cemetery"), "NOT_CERTIFIED"),
        (("result", "cemetery_frontier", "discarded_boundary_J_tends_to_zero"), True),
        (("result", "cemetery_frontier", "discarded_D_Z_weighted_mass_tends_to_zero"), True),
        (("result", "cemetery_frontier", "strong_trace_current_cemetery"), "CERTIFIED"),
        (("result", "cemetery_frontier", "proper_common_fw_rev_intersection"), "CERTIFIED"),
        (("result", "corrected_frontier", "physical_exponential_moment_of_preproperization_D_Z"), "CERTIFIED"),
        (("result", "corrected_frontier", "raw_K_par_is_Round49_proper_outer_kernel"), True),
        (("result", "corrected_frontier", "two_proper_view_pullback_lemma"), "INSTALLED"),
        (("result", "corrected_frontier", "same_ID_common_parent_law_join_after_recordwise_properization"), "CERTIFIED"),
        (("result", "corrected_frontier", "full_total_clock_common_law_Lp_join"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_beta"), "1"),
        (("result", "strict_nonpromotion", "global_preproperization_clock_moment"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "postproperization_same_ID_common_parent_law"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Round49_W_r_literal_join"), "INSTALLED"),
        (("result", "strict_nonpromotion", "full_numeric_C_fw_C_rev"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "5/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    mutations: list[str] = []
    for keys, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append(json.dumps(mutation))
    for key, replacement in (
        ("schema", "bad"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("result", {}),
        ("verdict", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append(json.dumps(mutation))
    mutation = copy.deepcopy(source)
    mutation["unexpected_top_level_key"] = True
    mutations.append(json.dumps(mutation))
    mutation = copy.deepcopy(source)
    mutation["result"]["corrected_frontier"]["numeric_H_cover"] = float("nan")
    mutations.append(json.dumps(mutation))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    mutations.append(duplicate[:-1] + ',"schema":"duplicate"}')

    rejected = 0
    for body in mutations:
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", prefix=".cm2-r50-group-hostile-",
            suffix=".json", dir=cert.HERE, delete=False
        )
        target = Path(handle.name)
        try:
            with handle:
                handle.write(body)
            errs = verify(target)
            rejected += bool(errs and errs != ["unsafe manifest"])
        finally:
            target.unlink(missing_ok=True)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--independent-arithmetic-only", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print("ERROR:", error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"SELF_TEST: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.independent_arithmetic_only:
        print("INDEPENDENT_ARITHMETIC: PASS")
        return 0
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("MANIFEST: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
