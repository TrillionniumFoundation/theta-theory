#!/usr/bin/env python3
"""Round-45 parent-bundle cross-cell minorization frontier.

The Round-44 shortest line referred to a long canonical parent-W curve.
The frozen registry instead chops every canonical parent-W into Euclidean
cells of length at most 1e-90.  A genuine transverse crossing of the fixed
interior C24 strip has length greater than 1/500 and therefore spans more
than 2e87 canonical IDs.

This certificate corrects that type mismatch, gives an exact countermodel
showing that cellwise density regularity and properness do not control the
weights across those IDs, and freezes the exact extended-parent sufficient
interface.  It is not a physical billiard counterexample and it does not
claim numerical C24 minorization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as numeric_growth


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round45-parent-bundle-cross-cell-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round45-parent-bundle-cross-cell-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json": (
        "10952d4f27df11f6c5c9503999b8ba5795070f84d7cca455d697c7b962a65018"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}

CELL_LENGTH = Q(1, 10**90)
CROSSING_ARC_LOWER = Q(1, 500)
MINIMUM_CROSSING_CELL_COUNT = 2 * 10**87 + 1
DENSITY_RATIO = Q(2000, 1999)
HIT_GAP = Q(21, 111718750)
HYPOTHETICAL_CROSSING_WEIGHT = Q(1, 1772)
HYPOTHETICAL_FAILING_WEIGHT = Q(1, 1773)
CP_EUCLIDEAN = Q(141 * 10**90 * 360493663, 358863)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    prior = load(
        "cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json"
    )["result"]
    if prior["shortest_numeric_frontier"][
        "numeric_proper_family_C24_minorization"
    ] != "NOT_CERTIFIED":
        raise RuntimeError("prior minorization scope")
    if prior["direct_smooth_bump_mixing_route"]["epsilon_hit"] != str(HIT_GAP):
        raise RuntimeError("hit gap")

    growth = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if growth["replay_summary"]["density_ratio"] != str(DENSITY_RATIO):
        raise RuntimeError("density ratio")
    source = HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py"
    if sha(source) != DEPENDENCIES[source.name]:
        raise RuntimeError("numeric Growth source")
    numeric = numeric_growth.certify()
    cone = numeric["invariant_density_and_distortion"][
        "invariant_adapted_density_cone"
    ]
    if cone["canonical_maximum_adapted_curve_length"] != str(CELL_LENGTH):
        raise RuntimeError("adapted cell length")
    constants = numeric["numeric_growth_and_recovery"][
        "numeric_Growth_Lemma_constants"
    ]
    if constants["euclidean_C_p"] != str(CP_EUCLIDEAN):
        raise RuntimeError("proper constant")

    parent = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]["Q2_parent_W_Borel_registry"]
    if parent["actual_parent_W_registry"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("parent registry")
    if parent["adapted_cell_length_upper"] != "1e-90":
        raise RuntimeError("parent cell length")
    if parent["natural_short_cell_rule"] != (
        "oriented Euclidean arclength intervals [k*1e-90,(k+1)*1e-90] clipped at leaf endpoints"
    ):
        raise RuntimeError("natural cells")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    registry = carrier["arbitrary_Rn_parent_W_Borel_registry"]
    if registry["source_parent_W_id"] != (
        "rn-parent-W:(component-id):(s,b):(source-interval-rank):(incidence-rank-path):(short-cell-k)"
    ):
        raise RuntimeError("arbitrary parent ID")
    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("common carrier")


def crossing_scale_audit() -> dict[str, Any]:
    if MINIMUM_CROSSING_CELL_COUNT != 2 * 10**87 + 1:
        raise RuntimeError("crossing count")
    if not (MINIMUM_CROSSING_CELL_COUNT - 1) * CELL_LENGTH == CROSSING_ARC_LOWER:
        raise RuntimeError("cell threshold equality")
    if not MINIMUM_CROSSING_CELL_COUNT * CELL_LENGTH > CROSSING_ARC_LOWER:
        raise RuntimeError("cell threshold strictness")
    return {
        "fixed_inner_C24_strip": {
            "chart": "G:E",
            "t_interval": "[11/1000,19/1000]",
            "p_interval": "[-1/1000,1/1000]",
            "closure_inside_frozen_bump_support": True,
            "closure_inside_one_C24_axis_core": True,
        },
        "transverse_crossing_definition": (
            "one connected graph arc stays in the t interval and joins p=-1/1000 to p=1/1000"
        ),
        "crossing_arc_lower_reason": (
            "Delta_phi=2*arcsin(1/1000)>1/500, and Euclidean graph arclength dominates abs(Delta_phi)"
        ),
        "crossing_arc_Euclidean_length_strict_lower": str(CROSSING_ARC_LOWER),
        "canonical_natural_cell_Euclidean_length_upper": str(CELL_LENGTH),
        "minimum_distinct_short_cell_IDs_in_one_crossing": (
            MINIMUM_CROSSING_CELL_COUNT
        ),
        "single_canonical_parent_W_ID_can_be_a_transverse_crossing": False,
        "round44_long_canonical_parent_W_wording": "CORRECTED",
        "status": "CERTIFIED_EXACT_SCALE_MISMATCH",
    }


def cross_cell_nonimplication() -> dict[str, Any]:
    if not Q(10**90) < CP_EUCLIDEAN:
        raise RuntimeError("proper countermodel")
    return {
        "purpose": (
            "show that the currently certified cellwise facts do not imply target mass across an extended parent; this is not a counterexample to the physical billiard"
        ),
        "abstract_parent": (
            "an ordered union of more than 2e87 adjacent length-1e-90 cells whose geometric union crosses the inner C24 strip"
        ),
        "cell_density": "constant on every occupied cell",
        "per_cell_density_ratio": "1<2000/1999",
        "family_weights": (
            "all mass is placed on one avoiding cell; target-crossing cells have zero family weight"
        ),
        "Z_over_mass": "1e90",
        "euclidean_proper_constant": str(CP_EUCLIDEAN),
        "family_is_proper": True,
        "geometric_extended_parent_crosses_C24": True,
        "C24_hit_mass": "0",
        "logical_conclusion": (
            "adjacent-cell weight continuation or an evolved extended-parent density ledger is required"
        ),
    }


def extended_parent_interface() -> dict[str, Any]:
    component_graph_length_upper = Q(6)
    hypothetical_pair_hit = Q(1, 3000) / DENSITY_RATIO
    threshold = HIT_GAP / hypothetical_pair_hit
    if hypothetical_pair_hit != Q(1999, 6000000):
        raise RuntimeError("pair hit")
    if threshold != Q(4032, 7146425):
        raise RuntimeError("crossing threshold")
    if not HYPOTHETICAL_CROSSING_WEIGHT > threshold:
        raise RuntimeError("safe reciprocal")
    if not HYPOTHETICAL_FAILING_WEIGHT < threshold:
        raise RuntimeError("failing reciprocal")
    return {
        "extended_pre_recut_pair_length_bound": {
            "monotone_unstable_graph": True,
            "largest_boundary_r_variation_strict_upper": "396/175",
            "phi_variation_strict_upper": "22/7",
            "Euclidean_graph_length_strict_upper": str(component_graph_length_upper),
        },
        "required_new_object": (
            "one same-ID extended pre-recut parent bundle with certified adjacent-cell density/weight continuation"
        ),
        "conditional_density_input": (
            "max(rho_extended)/min(rho_extended)<=R_ext on the entire extended pair"
        ),
        "conditional_one_pair_hit_fraction": (
            "mass(pair intersect C24)/mass(pair)>1/(3000*R_ext)"
        ),
        "conditional_family_covering_input": (
            "after H_cover collisions, extended crossing pairs carry total family weight beta"
        ),
        "conditional_family_hit_fraction": "mass(C24)/mass(G)>beta/(3000*R_ext)",
        "exact_sufficient_threshold": "beta>3000*R_ext*(21/111718750)",
        "cellwise_ratio_cannot_be_used_as_R_ext": True,
        "hypothetical_only_if_R_ext_equals_2000_over_1999": {
            "one_crossing_pair_hit_fraction_strict_lower": str(
                hypothetical_pair_hit
            ),
            "required_beta_strict_lower": str(threshold),
            "safe_reciprocal_beta": str(HYPOTHETICAL_CROSSING_WEIGHT),
            "next_reciprocal_fails": str(HYPOTHETICAL_FAILING_WEIGHT),
        },
        "numeric_R_ext": None,
        "numeric_H_cover": None,
        "numeric_beta": None,
        "status": "EXACT_SUFFICIENT_INTERFACE_ONLY",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "claim_type": (
                "exact canonical-cell scale correction, logical nonimplication and extended-parent sufficient interface"
            ),
            "literature_checked_through": "2026-07-19",
        },
        "canonical_crossing_scale_audit": crossing_scale_audit(),
        "cross_cell_weight_nonimplication": cross_cell_nonimplication(),
        "extended_parent_bundle_minorization_interface": extended_parent_interface(),
        "shortest_numeric_frontier": {
            "first_missing_registry": (
                "extended pre-recut parent-bundle IDs joining consecutive artificial short cells"
            ),
            "first_missing_analytic_bound": (
                "cross-cell density/weight continuation R_ext on each joined parent bundle"
            ),
            "first_missing_covering_bound": (
                "uniform H_cover and beta for C24-crossing extended bundles"
            ),
            "post_C24_cut_same_proper_class_return": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "single_canonical_short_cell_covering_route": "DISPROVED_BY_SCALE",
            "extended_parent_bundle_registry": "NOT_CERTIFIED",
            "cross_cell_density_weight_continuation": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
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
        default=(
            HERE
            / "cm2_gate34_round45_parent_bundle_cross_cell_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "CANONICAL_SHORT_CELL_CROSSING_ROUTE:",
        result["strict_nonpromotion"]["single_canonical_short_cell_covering_route"],
    )
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
