#!/usr/bin/env python3
"""Round-46 extended pre-recut parent density certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert as numeric_growth


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round46-extended-parent-density-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round46-extended-parent-density-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round45-parent-bundle-cross-cell-frontier-manifest-2026-07-19.json": (
        "a616f9e2bd1ce44cb6c7aada76df8b25d55083899dc92ac42161f5f38a039bdf"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json": (
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}

CELL_LENGTH = Q(1, 10**90)
SOURCE_DENSITY_RATIO = Q(2000, 1999)
ONE_STEP_LOG_VARIATION = Q(3, 200000)
JACOBIAN_RATIO = Q(200000, 199997)
R_EXT = SOURCE_DENSITY_RATIO * JACOBIAN_RATIO
PAIR_HIT = 1 / (3000 * R_EXT)
HIT_GAP = Q(21, 111718750)
BETA_THRESHOLD = HIT_GAP / PAIR_HIT
SAFE_BETA = Q(1, 1772)
FAILING_BETA = Q(1, 1773)


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
        "cm2-gate34-round45-parent-bundle-cross-cell-frontier-manifest-2026-07-19.json"
    )["result"]
    if prior["shortest_numeric_frontier"]["first_missing_registry"] != (
        "extended pre-recut parent-bundle IDs joining consecutive artificial short cells"
    ):
        raise RuntimeError("prior registry frontier")
    if prior["extended_parent_bundle_minorization_interface"][
        "exact_sufficient_threshold"
    ] != "beta>3000*R_ext*(21/111718750)":
        raise RuntimeError("prior sufficient interface")

    growth_manifest = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if growth_manifest["replay_summary"]["density_ratio"] != str(
        SOURCE_DENSITY_RATIO
    ):
        raise RuntimeError("source density ratio")
    source = HERE / "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py"
    if sha(source) != DEPENDENCIES[source.name]:
        raise RuntimeError("numeric Growth source")
    numeric = numeric_growth.certify()
    distortion = numeric["invariant_density_and_distortion"]
    log_jacobian = distortion["all_standard_curve_log_jacobian"]
    density = distortion["invariant_adapted_density_cone"]
    if log_jacobian["adapted_one_step_one_third_constant"] != (
        "15000000000000000000000000"
    ):
        raise RuntimeError("one-step distortion constant")
    if log_jacobian["numeric_all_iterated_standard_curve_distortion"] != (
        "CERTIFIED"
    ):
        raise RuntimeError("global distortion scope")
    if density["canonical_maximum_adapted_curve_length"] != str(CELL_LENGTH):
        raise RuntimeError("source cell length")
    if density["per_curve_density_ratio_upper"] != str(SOURCE_DENSITY_RATIO):
        raise RuntimeError("density cone ratio")

    q2 = load(
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    )["result"]
    if q2["Q2_numeric_F5_F6_slot_registry"][
        "one_step_canonical_recut_log_variation_strict_upper"
    ] != str(ONE_STEP_LOG_VARIATION):
        raise RuntimeError("one-step F6 variation")

    parent = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]
    recut = parent["Q2_actual_recut_instance_schema"]
    if recut["per_image_parent_natural_cell_count_formula"] != (
        "ceil(adapted_length(image-parent-W)/1e-90)"
    ):
        raise RuntimeError("image parent cells")
    if recut["actual_recut_instance_registry"] != (
        "CERTIFIED_PARAMETERIZED_SCHEMA"
    ):
        raise RuntimeError("recut registry")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("common carrier")


def extended_parent_registry() -> dict[str, Any]:
    return {
        "source_object": (
            "one canonical adapted source short cell on one regular physical owner and homogeneity branch"
        ),
        "image_object": (
            "the connected one-collision image before the deterministic artificial 1e-90 adapted recut"
        ),
        "extended_parent_bundle_id_schema": (
            "extended-pre-recut-parent:(common-restriction-id):(collision-time):(physical-owner-homogeneity-child):(image-parent-rank)"
        ),
        "ordered_child_id_schema": (
            "extended-child:(extended-pre-recut-parent-id):(natural-short-cell-k)"
        ),
        "child_union": (
            "the ordered half-open artificial children have disjoint interiors and their union is the entire pre-recut image parent"
        ),
        "artificial_recut_preserves_measure": True,
        "child_weights": (
            "restrictions of one pushforward conditional density; not independent family weights"
        ),
        "same_ID_forward_reverse_compatibility": True,
        "path_scope": "every one-step image inside every finite regular arbitrary-R_n path",
        "finite_integer_bundle_count_claimed": False,
        "status": "CERTIFIED_PARAMETERIZED_EXTENDED_PRE_RECUT_BUNDLE_REGISTRY",
    }


def density_continuation() -> dict[str, Any]:
    if ONE_STEP_LOG_VARIATION != Q(15_000_000_000_000_000_000_000_000, 10**30):
        raise RuntimeError("distortion scaling")
    if JACOBIAN_RATIO != 1 / (1 - ONE_STEP_LOG_VARIATION):
        raise RuntimeError("Jacobian ratio")
    if R_EXT != Q(400000000, 399794003):
        raise RuntimeError("R_ext")
    if not R_EXT < Q(446875, 252):
        raise RuntimeError("feasibility threshold")
    return {
        "source_cell_adapted_length_upper": str(CELL_LENGTH),
        "source_conditional_density_ratio_upper": str(SOURCE_DENSITY_RATIO),
        "one_step_log_Jacobian_variation_strict_upper": str(
            ONE_STEP_LOG_VARIATION
        ),
        "Jacobian_ratio_upper_via_exp_x_le_1_over_1_minus_x": str(
            JACOBIAN_RATIO
        ),
        "pushforward_density_formula": (
            "rho_image(y)=rho_source(x)/J_star(x), y=T_s(x); normalization cancels in ratios"
        ),
        "extended_parent_density_ratio_strict_upper_R_ext": str(R_EXT),
        "cross_cell_weight_continuation": (
            "every artificial child weight is the integral of this single pre-recut pushforward density over that child"
        ),
        "independent_child_weight_model_excluded": True,
        "status": "CERTIFIED_NUMERIC_CROSS_CELL_DENSITY_AND_WEIGHT_CONTINUATION",
    }


def covering_frontier() -> dict[str, Any]:
    if PAIR_HIT != Q(399794003, 1200000000000):
        raise RuntimeError("pair hit")
    if BETA_THRESHOLD != Q(4608000, 8167220347):
        raise RuntimeError("beta threshold")
    if not SAFE_BETA > BETA_THRESHOLD:
        raise RuntimeError("safe beta")
    if not FAILING_BETA <= BETA_THRESHOLD:
        raise RuntimeError("failing beta")
    return {
        "one_crossing_extended_parent_hit_fraction_strict_lower": str(PAIR_HIT),
        "family_hit_fraction": "mass(C24)/mass(G)>beta*399794003/1200000000000",
        "exact_sufficient_crossing_bundle_weight": (
            "beta>4608000/8167220347"
        ),
        "safe_reciprocal_beta": str(SAFE_BETA),
        "next_reciprocal_fails": str(FAILING_BETA),
        "numeric_R_ext": str(R_EXT),
        "numeric_H_cover": None,
        "numeric_beta": None,
        "first_remaining_gate4_input": (
            "uniform physical covering time H_cover and crossing extended-bundle family weight beta>4608000/8167220347"
        ),
        "post_C24_cut_same_proper_class_return": "NOT_CERTIFIED",
        "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "path_scope": "every finite regular arbitrary-R_n path",
            "claim_type": (
                "parameterized extended pre-recut bundle registry and numeric cross-cell pushforward-density continuation"
            ),
        },
        "extended_pre_recut_parent_bundle_registry": extended_parent_registry(),
        "numeric_cross_cell_density_continuation": density_continuation(),
        "C24_covering_frontier_after_R_ext": covering_frontier(),
        "strict_nonpromotion": {
            "extended_pre_recut_parent_bundle_registry": "CERTIFIED",
            "numeric_cross_cell_R_ext": "CERTIFIED",
            "numeric_H_cover_and_beta": "NOT_CERTIFIED",
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
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
        default=(
            HERE
            / "cm2_gate34_round46_extended_parent_density_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "EXTENDED_PARENT_R_EXT:",
        result["numeric_cross_cell_density_continuation"][
            "extended_parent_density_ratio_strict_upper_R_ext"
        ],
    )
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

