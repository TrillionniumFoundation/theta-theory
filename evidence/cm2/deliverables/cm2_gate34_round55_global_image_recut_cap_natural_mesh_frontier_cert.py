#!/usr/bin/env python3
"""Round-55 global image-recut cap and natural-mesh frontier.

This fail-closed leaf removes one specific overestimate from the Gate-4
terminal-cell interface.  A connected unstable image has Euclidean length
strictly below 68, and the frozen metric comparison gives adapted length
strictly below 2397.  Therefore deterministic adapted recutting at scale
10^-90 creates at most 2397*10^90+1 image cells under the frozen Round-50
endpoint-owner convention, independently of return depth,
incidence-rank products, and branch derivative products.

For a measured parent whose normalized density has ratio at most R, any
interval refinement into at most N positive cells obeys

    sum_j p_j/ell_j <= R*N*p/ell.

The resulting image-recut multiplier is certified here.  The natural
delta_B mesh is deliberately not promoted: the frozen registry does not say
whether its path rank is a maximum or a timewise union, does not pin the
metric conversion on the same terminal atoms, and does not identify those
atoms with the Round-42 canonical family.  Consequently physical J_pair,
I_D, Gate 4, and CM2 remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round55-global-image-recut-cap-natural-mesh-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round55-global-image-recut-cap-natural-mesh-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE
    / "cm2_gate34_round55_global_image_recut_cap_natural_mesh_frontier_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate34-round54-numeric-growth-gap-rate-interval-atlas-frontier-manifest-2026-07-20.json": (
        "e077bc19445e90eb3bbab6a43386d19515c4a13fdcfdf6c85f8d02bf8ef4d7e6"
    ),
    "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json": (
        "941929e86bdecd1d3fc8d935ed685b346ea2bedc3fba0c24bd949f5f88b66c2f"
    ),
}

EUCLIDEAN_LENGTH_STRICT_UPPER = Q(68)
ADAPTED_OVER_EUCLIDEAN_STRICT_UPPER = Q(141, 4)
ADAPTED_LENGTH_STRICT_UPPER = (
    EUCLIDEAN_LENGTH_STRICT_UPPER * ADAPTED_OVER_EUCLIDEAN_STRICT_UPPER
)
RECUT_DENOMINATOR = 10**90
RECUT_SCALE = Q(1, RECUT_DENOMINATOR)
IMAGE_RECUT_COUNT_UPPER = (
    int(ADAPTED_LENGTH_STRICT_UPPER) * RECUT_DENOMINATOR + 1
)
REGISTERED_DENSITY_RATIO = Q(2000, 1999)
REGISTERED_IMAGE_REFINEMENT_MULTIPLIER = (
    REGISTERED_DENSITY_RATIO * IMAGE_RECUT_COUNT_UPPER
)
Q0_MOMENT_UPPER = Q(134217735, 64)
ROUND42_ONE_STEP_Z1 = Q(18367592526, 360493663)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    registry = carrier["arbitrary_Rn_parent_W_Borel_registry"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if registry["rank_density_mesh"] != (
        "delta_B=2^-ceil(3(B+1)/2) in carrier arclength, followed by 1e-90 adapted recuts"
    ):
        raise RuntimeError("Round35 natural/image recut contract")
    if pair["image_cell"] != "B=H(A), recut to adapted length and pulled back to A":
        raise RuntimeError("Round35 image pullback")
    if not pair["forward_and_reverse_are_two_views_not_two_charges"]:
        raise RuntimeError("Round35 once-charge typing")

    rank = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]["physical_collision_incidence_rank"]
    if rank["chosen_q0"] != "3/2":
        raise RuntimeError("Round35 q0")
    if Q(rank["global_collision_SRB_integral_2^(3B_inc/2)_strict_upper"]) != Q0_MOMENT_UPPER:
        raise RuntimeError("Round35 q0 moment")

    aggregate = load(
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    )["result"]
    separator = aggregate["retained_depth_marginal_countermodel"]
    if separator["perfect_time_correlation"] != "B_i=B for every i>=1":
        raise RuntimeError("Round36 separator law")
    if separator["failure"] != (
        "for every beta>0, E[N_recut,n^beta]=infinity once beta*n>=2"
    ):
        raise RuntimeError("Round36 separator conclusion")
    if aggregate["round36_route_decision"]["cellwise_D_route"] != (
        "DEFERRED: current D1 marginal control does not dominate common-carrier image recuts"
    ):
        raise RuntimeError("Round36 frontier")

    round42 = load(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]
    growth42 = round42["numerical_C24_killed_Growth"]
    if Q(growth42["one_step_Z_multiplier_Z1"]) != ROUND42_ONE_STEP_Z1:
        raise RuntimeError("Round42 Z1")
    if round42["strict_nonpromotion"]["complete_numeric_C_fw_C_rev"] != "NOT_CERTIFIED":
        raise RuntimeError("Round42 nonpromotion")

    round50 = load(
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    )["result"]["physical_Borel_whole_family_grouping"]
    if round50["image_recut_count"] != (
        "N_img(y,k)<=ceil(length(H(A_k))*10^90)+1<infinity"
    ):
        raise RuntimeError("Round50 image recut convention")
    if "same one-sided owner for image recuts" not in round50[
        "half_open_endpoint_owner"
    ]:
        raise RuntimeError("Round50 image endpoint owner")

    round53 = load(
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    )["result"]
    cell = round53["fractional_cell_Z_to_defect_moment"]
    if cell["pair_boundary_numerator"] != (
        "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda"
    ):
        raise RuntimeError("Round53 J_pair target")
    if cell["physical_J_pair_certified"] is not False:
        raise RuntimeError("Round53 J_pair frontier")

    round54_numeric = load(
        "cm2-gate34-round54-numeric-growth-gap-rate-interval-atlas-frontier-manifest-2026-07-20.json"
    )["result"]
    if Q(
        round54_numeric["gap_prefactor_atomisation"][
            "maximum_homogeneous_unstable_curve_length_L0_strict_upper"
        ]
    ) != EUCLIDEAN_LENGTH_STRICT_UPPER:
        raise RuntimeError("Round54 global curve length")
    proof_rows = round54_numeric["new_numeric_growth_lemma"]["proof_rows"]
    if not any(
        "ell_*(W)<=(141/4)ell_E(W)" in row.get("formula", "")
        for row in proof_rows
    ):
        raise RuntimeError("Round54 metric comparison")

    round54_terminal = load(
        "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json"
    )["result"]["two_orientation_terminal_extraction"]
    if round54_terminal["terminal_cell_refinement_to_J_pair_same_ID_Z_join"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 refinement frontier")
    if not round54_terminal["actual_physical_J_pair"].startswith("NOT_CERTIFIED"):
        raise RuntimeError("Round54 J_pair nonpromotion")


def mesh_exponent(B: int) -> int:
    if not isinstance(B, int) or B < 0:
        raise ValueError("B must be a nonnegative integer")
    return (3 * (B + 1) + 1) // 2


def natural_mesh_row(B: int) -> dict[str, Any]:
    exponent = mesh_exponent(B)
    delta_inverse = 1 << exponent
    squared_reference = 1 << (3 * B)
    squared_ratio = Q(delta_inverse * delta_inverse, squared_reference)
    assert squared_ratio in {Q(8), Q(16)}
    assert delta_inverse * delta_inverse <= 16 * squared_reference
    return {
        "B": B,
        "mesh_exponent_ceil_3Bplus3_over_2": exponent,
        "delta_B": f"1/{delta_inverse}",
        "delta_B_inverse_squared_over_2_to_3B": qstr(squared_ratio),
        "parity": "even" if B % 2 == 0 else "odd",
    }


def image_recut_cap() -> dict[str, Any]:
    assert ADAPTED_LENGTH_STRICT_UPPER == Q(2397)
    assert IMAGE_RECUT_COUNT_UPPER == 2397 * 10**90 + 1
    rows = [
        {
            "step": 1,
            "formula": "ell_E(H(A))<68 for every connected unstable image parent",
            "reason": "global unstable-graph length cap; no rank-path derivative product",
        },
        {
            "step": 2,
            "formula": "ell_*(H(A))<(141/4)*68=2397",
            "reason": "frozen Euclidean-to-adapted metric comparison",
        },
        {
            "step": 3,
            "formula": "N_img<=ceil(ell_*(H(A))/10^-90)+1<=2397*10^90+1",
            "reason": "strict length upper plus the frozen Round50 one-sided recut convention",
        },
    ]
    return {
        "connected_image_parent": "H(A) on one regular finite rank-path branch",
        "Euclidean_length_strict_upper": qstr(EUCLIDEAN_LENGTH_STRICT_UPPER),
        "adapted_over_Euclidean_strict_upper": qstr(
            ADAPTED_OVER_EUCLIDEAN_STRICT_UPPER
        ),
        "adapted_length_strict_upper": qstr(ADAPTED_LENGTH_STRICT_UPPER),
        "deterministic_adapted_recut_scale": qstr(RECUT_SCALE),
        "uniform_image_recut_count_upper": str(IMAGE_RECUT_COUNT_UPPER),
        "ceil_strictness": (
            "ell_*/delta_*<2397*10^90, whose right side is an integer, so Round50's ceil(ell_*/delta_*)+1 convention is at most 2397*10^90+1"
        ),
        "rank_path_derivative_product_used": False,
        "proof_rows": rows,
        "proof_rows_sha256": digest(rows),
        "status": "CERTIFIED_GLOBAL_CONNECTED_IMAGE_RECUT_COUNT_CAP",
    }


def refinement_lemma() -> dict[str, Any]:
    # If rho is normalized on W, average rho=1/ell.  A ratio bound gives
    # sup rho <= R/ell.  Every refined cell has p_j/ell_j<=p*sup rho.
    sample = []
    for count in [1, 2, 8, 128, IMAGE_RECUT_COUNT_UPPER]:
        sample.append(
            {
                "cell_count_N": str(count),
                "density_ratio_R": qstr(REGISTERED_DENSITY_RATIO),
                "refined_over_coarse_Z_multiplier_upper": qstr(
                    REGISTERED_DENSITY_RATIO * count
                ),
            }
        )
    return {
        "hypotheses": [
            "one positive measured parent (W,p,rho) with ell(W)>0",
            "rho is normalized on W and sup_W(rho)/inf_W(rho)<=R",
            "a half-open interval refinement into at most N positive cells with no duplicate charge",
            "parent and child lengths are measured in the same declared carrier metric",
        ],
        "pointwise_average_step": "sup_W rho<=R/ell(W)",
        "one_cell_step": "p_j/ell_j<=p*sup_W rho<=R*p/ell(W)",
        "refinement_inequality": "sum_j p_j/ell_j<=R*N*p/ell(W)",
        "uniform_image_recut_specialization": (
            "sum_j p_j/ell_j<=(R*(2397*10^90+1))*p/ell(W)"
        ),
        "registered_density_ratio": qstr(REGISTERED_DENSITY_RATIO),
        "registered_image_refinement_multiplier": qstr(
            REGISTERED_IMAGE_REFINEMENT_MULTIPLIER
        ),
        "paired_conditional_inequality": (
            "J_pair<=N_img*(R_source*Z_source_natural+R_target*Z_image_coarse)"
        ),
        "paired_inequality_typing": (
            "conditional on the same once-charged Round35 IDs, compatible coarse parents in both views, and the stated per-parent density ratios"
        ),
        "sample_rows": sample,
        "sample_rows_sha256": digest(sample),
        "status": "CERTIFIED_ABSTRACT_DENSITY_RATIO_REFINEMENT_LEMMA__PHYSICAL_NATURAL_JOIN_OPEN",
    }


def natural_mesh_frontier() -> dict[str, Any]:
    rows = [natural_mesh_row(B) for B in [14, 15, 16, 31, 64, 65]]
    return {
        "frozen_mesh": "delta_B=2^-ceil(3(B+1)/2)",
        "exact_parity_bound": "delta_B^(-1)<=4*2^(3B/2)",
        "exact_integer_square_check": "delta_B^(-2)<=16*2^(3B)",
        "even_B_is_worst_and_attains_squared_ratio_16": True,
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "available_collision_q0": "3/2",
        "available_global_collision_q0_moment_strict_upper": qstr(Q0_MOMENT_UPPER),
        "three_unpinned_physical_joins": [
            {
                "id": "path_rank_aggregation",
                "needed": (
                    "pin whether the arbitrary-R_n natural mesh uses a path maximum or an additive timewise union, and prove its multiplicity is dominated by the q0 Kac-tower charge rather than a product"
                ),
                "status": "NOT_CERTIFIED",
            },
            {
                "id": "metric_alignment",
                "needed": (
                    "put delta_B, the adapted 10^-90 recut, and both ell_fw/ell_rev boundary functionals into one explicit metric-conversion ledger"
                ),
                "status": "NOT_CERTIFIED",
            },
            {
                "id": "same_ID_canonical_atom",
                "needed": (
                    "identify the Round35 natural/image cells with refinements of the Round42/Round54 coarse terminal canonical atoms on the exact once-charged IDs"
                ),
                "status": "NOT_CERTIFIED",
            },
        ],
        "physical_natural_mesh_Z_sum": "NOT_CERTIFIED",
        "physical_J_pair": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_NATURAL_MESH_ARITHMETIC__THREE_PHYSICAL_JOINS_OPEN",
    }


def separator_retyping() -> dict[str, Any]:
    return {
        "round36_manifest_sha256": DEPENDENCIES[
            "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
        ],
        "round36_countermodel_key": "retained_depth_marginal_countermodel",
        "countermodel_image_recut_model": (
            "N_recut,n proportional to 2^(sum_i B_i)=2^(nB)"
        ),
        "countermodel_still_valid_for_its_installed_fields": True,
        "countermodel_disproves_global_connected_length_cap": False,
        "new_conclusion": (
            "the derivative-product estimate is no longer needed for deterministic image-recut multiplicity once connectedness and ell_*<2397 are joined; the countermodel still blocks any unproved natural-mesh product inference"
        ),
        "image_recut_product_obstruction": "REPLACED_BY_FIXED_MULTIPLIER_ONLY",
        "natural_mesh_product_or_path_join": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "global connected-image length cap, deterministic image-recut multiplicity, abstract density-ratio refinement, and fail-closed natural-mesh frontier"
            ),
            "parameter_scope": "every fixed |s|<=1/400 and every regular finite return branch",
        },
        "global_connected_image_recut_cap": image_recut_cap(),
        "density_ratio_refinement_lemma": refinement_lemma(),
        "natural_delta_B_mesh_frontier": natural_mesh_frontier(),
        "round36_separator_retyping": separator_retyping(),
        "strict_nonpromotion": {
            "global_connected_image_recut_count_cap": "CERTIFIED",
            "image_recut_derivative_product_required": False,
            "density_ratio_refinement_lemma": "CERTIFIED_CONDITIONAL",
            "natural_mesh_path_rank_aggregation": "NOT_CERTIFIED",
            "natural_mesh_metric_alignment": "NOT_CERTIFIED",
            "natural_mesh_same_ID_canonical_atom_join": "NOT_CERTIFIED",
            "coarse_terminal_Z_l1": "NOT_CERTIFIED_BY_THIS_LEAF",
            "terminal_cell_refinement_to_J_pair": "NOT_CERTIFIED",
            "physical_J_pair": "NOT_CERTIFIED",
            "physical_I_D": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    result = build_result()
    cert_path = Path(__file__).resolve()
    verifier_path = verifier.resolve()
    if not verifier_path.is_file() or verifier_path.is_symlink():
        raise RuntimeError("unsafe verifier")
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(cert_path),
        "verifier_sha256": sha(verifier_path),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": dict(result["strict_nonpromotion"]),
    }


def pretty_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.manifest_json:
        print(pretty_manifest(args.verifier), end="")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print(
        "GLOBAL_IMAGE_RECUT_CAP:",
        strict["global_connected_image_recut_count_cap"],
    )
    print("NATURAL_MESH_JOIN:", strict["natural_mesh_same_ID_canonical_atom_join"])
    print("PHYSICAL_J_PAIR:", strict["physical_J_pair"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
