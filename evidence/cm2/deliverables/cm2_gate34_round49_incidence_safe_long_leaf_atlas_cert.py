#!/usr/bin/env python3
"""Round-49 incidence-safe long-leaf atlas frontier certificate.

Round 48 reduced numerical C24 minorisation to a target-sensitive atlas on
proper-family leaves of adapted length at least ``delta_long``.  This layer
turns that input into a compact, incidence-safe family:

* a central adapted half controls source grazing;
* explicit collars around all one-step signed tangency sheets control target
  grazing; and
* a final short-component discard produces a uniform Euclidean length scale
  suitable for a sufficient-rectangles theorem.

The 2026 sufficient-rectangles theorem supplies only fixed-map qualitative
existence.  It does not expose a numerical time, a source-mass fraction, or a
constant uniform in the parameter window.  Accordingly this certificate does
not promote H_cover, beta, C_fw/C_rev, q, cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round49-incidence-safe-long-leaf-atlas.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json": (
        "68f0ee7595688ef4ea1ab5eb1e101ab8c2ccd327d3bcf40876ccbd40a5d9bfab"
    ),
    "cm2-gate34-round46-extended-parent-density-frontier-manifest-2026-07-19.json": (
        "5144220fb226d0b00265d16e40cadde91ae2f4d2346f73ce31274b2b10b4c501"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
}

DENSITY_RATIO = Q(2000, 1999)
LONG_WEIGHT = Q(1, 2)
DELTA_LONG = Q(358863, 2883949304 * 10**90)
HIT_GAP = Q(21, 111718750)
BETA_WDIAG_THRESHOLD = Q(230400, 5197322039)
TANGENCY_INTERSECTIONS = 152
TRUE_COMPONENTS = 153
V_LOWER = Q(25, 9)
V_UPPER = Q(29)
KAPPA_UPPER = Q(25, 4)
DELTA_DERIVATIVE_LOWER = Q(36337, 900000)
RADIUS_UPPER = Q(9, 25)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def validate_dependencies() -> None:
    prior = load_json(
        "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
    )["result"]
    reduction = prior["proper_family_long_leaf_target_cover_reduction"]
    if Q(reduction["delta_long"]) != DELTA_LONG:
        raise RuntimeError("Round48 delta_long")
    if reduction["long_leaf_weight_lower"] != "1/2":
        raise RuntimeError("Round48 long weight")
    if prior["corrected_frontier"]["numeric_H_cover"] is not None:
        raise RuntimeError("Round48 H overclaim")
    if prior["corrected_frontier"]["numeric_actual_beta_Wdiag"] is not None:
        raise RuntimeError("Round48 beta overclaim")

    density = load_json(
        "cm2-gate34-round46-extended-parent-density-frontier-manifest-2026-07-19.json"
    )["result"]["numeric_cross_cell_density_continuation"]
    if density["source_conditional_density_ratio_upper"] != str(DENSITY_RATIO):
        raise RuntimeError("source density ratio")

    growth = load_json(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]["physical_branch_length_pullback"]
    if growth["abs_dDelta_dr_low_region_strict_lower"] != str(
        DELTA_DERIVATIVE_LOWER
    ):
        raise RuntimeError("Delta derivative")
    if growth["image_unstable_slope_strict_upper"] != "29":
        raise RuntimeError("slope upper")
    if growth["ray_circle_coordinates"] != (
        "Delta=R_1^2-w^2=R_1^2*c_1^2, a=u dot d=tau+sqrt(Delta)"
    ):
        raise RuntimeError("target discriminant identity")

    cone = load_json(
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    )["result"]["global_invariant_geometric_cone"]
    if cone["fixed_geometric_unstable_cone"] != (
        "25/9<V=dphi/dr<4108425/145348<29"
    ):
        raise RuntimeError("invariant cone")
    if cone["curvature_upper"] != "25/4":
        raise RuntimeError("curvature upper")

    complexity = load_json(
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if complexity["true_singularity_intersection_upper"] != TANGENCY_INTERSECTIONS:
        raise RuntimeError("tangency count")
    if complexity["true_continuity_component_upper"] != TRUE_COMPONENTS:
        raise RuntimeError("component count")

    source = HERE / "cm2_gate3_candidate_first_hit_cert.py"
    if not source.is_file() or source.is_symlink() or sha(source) != DEPENDENCIES[source.name]:
        raise RuntimeError("first-hit source")
    source_text = source.read_text(encoding="utf-8")
    if 'RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}' not in source_text:
        raise RuntimeError("radius registry")


def rank_bracket(lower: Q, exponent: int) -> dict[str, Any]:
    return {
        "strict_lower": str(lower),
        "dyadic_bracket": f"2^-{exponent}<lower<2^-{exponent - 1}",
        "lower_exceeds_left_endpoint": lower > Q(1, 2**exponent),
        "lower_below_right_endpoint": lower < Q(1, 2 ** (exponent - 1)),
    }


def compact_incidence_safe_core() -> dict[str, Any]:
    # Central adapted half: dphi/dell_*=V/(kappa+V)>100/1269.
    source_cp = Q(175, 13959) * DELTA_LONG
    slope4_source_cp = Q(28, 451) * DELTA_LONG
    central_leaf_mass = Q(1, 2) / DENSITY_RATIO
    central_family_mass = LONG_WEIGHT * central_leaf_mass

    # Delete an adapted open collar of radius L/(8*152) around every one-step
    # signed tangency sheet.  Total collar length is at most L/4.
    collar_radius_fraction = Q(1, 8 * TANGENCY_INTERSECTIONS)
    total_collar_fraction = 2 * TANGENCY_INTERSECTIONS * collar_radius_fraction
    target_r_distance_fraction = collar_radius_fraction / (KAPPA_UPPER + V_UPPER)
    target_cp_squared = (
        DELTA_DERIVATIVE_LOWER
        * DELTA_LONG
        * target_r_distance_fraction
        / (RADIUS_UPPER**2)
    )

    # Discard all remaining components shorter than L/(8*153).  At most 153
    # components are present, so less than another L/8 is lost.  The surviving
    # union has adapted length >L/8 and every piece has a uniform Euclidean
    # length lower bound.
    component_cut_fraction = Q(1, 8 * TRUE_COMPONENTS)
    discarded_short_fraction = TRUE_COMPONENTS * component_cut_fraction
    incidence_safe_leaf_length_fraction = Q(1, 2) - total_collar_fraction - discarded_short_fraction
    incidence_safe_leaf_mass = incidence_safe_leaf_length_fraction / DENSITY_RATIO
    incidence_safe_family_mass = LONG_WEIGHT * incidence_safe_leaf_mass
    euclidean_delta = DELTA_LONG * component_cut_fraction / (KAPPA_UPPER + V_UPPER)

    assert central_leaf_mass == Q(1999, 4000)
    assert central_family_mass == Q(1999, 8000)
    assert collar_radius_fraction == Q(1, 1216)
    assert total_collar_fraction == Q(1, 4)
    assert target_r_distance_fraction == Q(1, 42864)
    assert target_cp_squared == Q(
        4346668277, 480625240334358528 * 10**91
    )
    assert target_cp_squared < Q(1, 4)
    assert target_cp_squared > Q(1, 2**330)
    assert source_cp > Q(1, 2**319)
    assert slope4_source_cp > Q(1, 2**316)
    assert component_cut_fraction == Q(1, 1224)
    assert discarded_short_fraction == Q(1, 8)
    assert incidence_safe_leaf_length_fraction == Q(1, 8)
    assert incidence_safe_family_mass == Q(1999, 32000)
    assert euclidean_delta == DELTA_LONG / 43146

    rows = [
        {
            "kind": "general invariant proper leaf",
            "source_rank_upper": 319,
            "target_rank_upper": 165,
            "incidence_rank_upper": 319,
        },
        {
            "kind": "slope-4 canonical leaf sub-class",
            "source_rank_upper": 316,
            "target_rank_upper": 165,
            "incidence_rank_upper": 316,
        },
    ]
    return {
        "object_scope": (
            "conditional per admissible canonical proper standard family; the physical arbitrary-R_n whole-family grouping is not installed"
        ),
        "leaf_hypothesis": (
            "L=ell_*(W)>=delta_long on an invariant proper unstable leaf whose canonical conditional density ratio is <2000/1999"
        ),
        "invariant_cone": "25/9<V<29 and kappa<=25/4",
        "central_adapted_interval": "[L/4,3L/4]",
        "source_grazing_angle_lower": "25*L/1269",
        "source_cp_lower": rank_bracket(source_cp, 319),
        "slope4_only_source_cp_lower": rank_bracket(slope4_source_cp, 316),
        "central_half_leaf_mass_strict_lower": str(central_leaf_mass),
        "central_half_family_mass_strict_lower": str(central_family_mass),
        "tangency_sheet_count_upper": TANGENCY_INTERSECTIONS,
        "true_component_count_upper": TRUE_COMPONENTS,
        "one_tangency_collar_adapted_radius_fraction": str(collar_radius_fraction),
        "all_tangency_collars_adapted_length_fraction_upper": str(total_collar_fraction),
        "target_r_distance_fraction_strict_lower": str(target_r_distance_fraction),
        "target_cp_squared_lower": rank_bracket(target_cp_squared, 330),
        "target_cp_case_split": (
            "while Delta<=R_1^2/4 integrate the Round42 derivative lower bound from the deleted tangency collar; if the path exits that region then c_p^2=Delta/R_1^2>1/4, which is stronger because the displayed lower is <1/4"
        ),
        "target_rank_upper": 165,
        "post_collar_short_component_cut_fraction": str(component_cut_fraction),
        "short_component_total_discard_fraction_strict_upper": str(discarded_short_fraction),
        "incidence_safe_adapted_length_fraction_strict_lower": str(incidence_safe_leaf_length_fraction),
        "incidence_safe_family_mass_strict_lower": str(incidence_safe_family_mass),
        "incidence_safe_piece_Euclidean_length_strict_lower": str(euclidean_delta),
        "incidence_safe_piece_count_per_leaf_upper": TRUE_COMPONENTS,
        "rank_rows": rows,
        "rank_rows_sha256": digest(rows),
        "status": "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY_NUMERIC_COMPACT_CORE",
    }


def threshold_ledger() -> dict[str, Any]:
    central_mass = Q(1999, 8000)
    safe_mass = Q(1999, 32000)
    central_zeta = BETA_WDIAG_THRESHOLD / central_mass
    safe_wdiag_zeta = BETA_WDIAG_THRESHOLD / safe_mass
    direct_zeta = HIT_GAP / safe_mass
    assert central_zeta == Q(1843200000, 10389446755961)
    assert safe_wdiag_zeta == Q(7372800000, 10389446755961)
    assert direct_zeta == Q(2688, 893303125)
    assert Q(1, 1409) > safe_wdiag_zeta > Q(1, 1410)
    assert Q(1, 332330) > direct_zeta > Q(1, 332331)
    return {
        "Round47_beta_Wdiag_threshold": str(BETA_WDIAG_THRESHOLD),
        "central_source_rank_only_family_mass": str(central_mass),
        "central_source_rank_only_required_Wdiag_fraction": str(central_zeta),
        "incidence_safe_family_mass": str(safe_mass),
        "incidence_safe_required_Wdiag_fraction": str(safe_wdiag_zeta),
        "incidence_safe_Wdiag_safe_reciprocal": "1/1409",
        "incidence_safe_Wdiag_next_reciprocal_fails": "1/1410",
        "direct_C24_hit_gap": str(HIT_GAP),
        "incidence_safe_required_direct_C24_fraction": str(direct_zeta),
        "direct_C24_safe_reciprocal": "1/332330",
        "direct_C24_next_reciprocal_fails": "1/332331",
        "Wdiag_to_direct_requirement_ratio": "660000000000/2798558021",
        "direct_target_route_is_about_236_times_less_demanding": True,
        "actual_fraction_certified": False,
        "status": "CERTIFIED_EXACT_CONDITIONAL_THRESHOLD_LEDGER",
    }


def sufficient_rectangles_interface() -> dict[str, Any]:
    euclidean_delta = DELTA_LONG / 43146
    return {
        "technology_checked": [
            {
                "paper": "Climenhaga-Day, arXiv:2604.25881v1",
                "result": "Proposition 3.19 (Sufficient rectangles)",
                "safe_quantifiers": (
                    "for one fixed finite-horizon Sinai billiard T, every delta>0 and every rectangle R0 in its Cantor cover admit finitely many auxiliary rectangles and some N so that each unstable curve of Euclidean length at least delta contains a subcurve whose Nth image crosses R0"
                ),
            },
            {
                "paper": "Baladi-Demers, arXiv:1807.02330v4",
                "result": "Cantor-rectangle construction",
                "safe_quantifiers": (
                    "for a fixed billiard, a regular open target contains a positive Cantor rectangle with solid rectangle contained in that target"
                ),
            },
        ],
        "numeric_input_delta_rect": str(euclidean_delta),
        "target_open_set": "one closure-contained W-diagonal C24 core",
        "target_rectangle_inside_C24": (
            "QUALITATIVE_FIXED_S_EXISTENCE_SEPARATE_FROM_THE_SUFFICIENT_COVER"
        ),
        "fixed_s_target_sensitive_hit": (
            "CONDITIONAL_ON_TARGET_RECTANGLE_IN_SUFFICIENT_COVER"
        ),
        "same_cover_bridge_installed": False,
        "why_crossing_would_hit_C24": (
            "conditional on adding the selected solid C24 target rectangle to the same sufficient cover used by Proposition 3.19"
        ),
        "common_over_parameter_window": False,
        "numeric_rectangle_rows_materialized": False,
        "numeric_N": None,
        "numeric_source_subcurve_fraction": None,
        "numeric_H_cover": None,
        "numeric_actual_beta_Wdiag": None,
        "strict_inferable_uniform_beta_lower": "0",
        "not_the_Round47_full_p_band_predicate": True,
        "missing_effectivity": [
            "the compactness proof gives no explicit finite subcover or N",
            "Liouville mixing positivity and rectangle-density constants are not numerical",
            "the theorem gives existence, not a source-length or source-mass lower bound",
            "no common N or rectangle atlas is supplied for all |s|<=1/400",
            "forward and reverse applications do not supply one same-ID common clock",
            "the separately constructed C24 target rectangle has not been inserted into the exact Cantor cover used by Proposition 3.19",
        ],
        "status": "CONDITIONAL_FIXED_S_TARGET_INTERFACE",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "uniform numeric trimming for each fixed |s|<=1/400; sufficient-rectangle import only fixed-s qualitative",
            "claim_type": "incidence-safe compact long-leaf core and exact remaining cover thresholds",
        },
        "incidence_safe_long_leaf_compact_core": compact_incidence_safe_core(),
        "exact_remaining_cover_thresholds": threshold_ledger(),
        "latest_sufficient_rectangles_interface": sufficient_rectangles_interface(),
        "corrected_frontier": {
            "numeric_long_leaf_incidence_safe_core": (
                "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY"
            ),
            "fixed_s_qualitative_C24_target_hit": (
                "NOT_CERTIFIED_PENDING_SAME_COVER_BRIDGE"
            ),
            "uniform_parameter_window_numeric_rectangle_atlas": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_actual_beta_Wdiag": None,
            "same_ID_two_orientation_cover": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "numeric_incidence_safe_long_leaf_compact_core": (
                "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY"
            ),
            "exact_conditional_Wdiag_and_direct_C24_thresholds": "CERTIFIED",
            "fixed_s_qualitative_target_sensitive_rectangle_interface": (
                "CONDITIONAL_NOT_INSTALLED"
            ),
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
        default=HERE / "cm2_gate34_round49_incidence_safe_long_leaf_atlas_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "INCIDENCE_SAFE_LONG_LEAF_CORE:",
        result["strict_nonpromotion"]["numeric_incidence_safe_long_leaf_compact_core"],
    )
    print("NUMERIC_H_COVER_AND_BETA: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
