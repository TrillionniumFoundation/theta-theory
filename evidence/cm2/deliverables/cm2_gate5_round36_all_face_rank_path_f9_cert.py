#!/usr/bin/env python3
"""All-face F9 bounds on every finite regular C24 return path.

The stationary-core pullback certificate handled only affine core faces.
This append-only layer supplies the two missing base geometries:

* physical collision/owner boundaries, split into the seven frozen branch
  types; and
* the 64 moving first-event occurrence faces.

Circle tangency sheets are treated as level-set faces in the source
collision section, not as recovery carriers.  Their graph slope and second
derivative follow from the circular-caustic identities.  Transparent-wall
corner rays are point-caustic graphs and receive a separate exact distance
lower bound.  The remaining branch types are affine coordinate faces or
regular pullbacks of such faces.

For a base graph level G(r,phi)=phi-h(r), the certificate records
||dG||_1<=G0, ||dG||_1>=1 and ||D2G||<=K0.  Composing with an arbitrary
finite regular rank path gives the exact safe recurrence

    K_pull < K0*D_j^2 + G0*H_j,

where D_j, E_j and H_j are the forward, inverse and Hessian envelopes of
the prefix.  This fills parameterized F9 values on all five physical face
grammars.  It does not fill F10, sum the rank-path costs, or create a
complete 18-field block.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round36-all-face-rank-path-f9.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json": (
        "323cdeb40a78d29e0e767b438ef1e6fe0c28d8da80a10e0b4f4d717d4f308515"
    ),
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": (
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91"
    ),
    "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json": (
        "003d3e0d742829039e85649975e8dca4a992fa7a389063eef4478df02ec03064"
    ),
    "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json": (
        "b38772a41d0b610e1e1cd4fb4509cfb76227cc8f4983af0699d2cf38e60650c5"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
}

MINIMUM_RANK = 14
DERIVATIVE_NUMERATOR = 150
HESSIAN_NUMERATOR = 42672
KAPPA_MAX = Q(25, 4)
GLOBAL_DISK_GAP = Q(36337, 800000)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def one_step_bounds(rank: int) -> tuple[int, int]:
    if type(rank) is not int or rank < MINIMUM_RANK:
        raise ValueError("rank must be an integer at least 14")
    return (
        DERIVATIVE_NUMERATOR * (1 << rank),
        HESSIAN_NUMERATOR * (1 << (3 * rank)),
    )


def prefix_bounds(ranks: Iterable[int]) -> tuple[int, int, int]:
    derivative = 1
    inverse_derivative = 1
    hessian = 0
    for rank in ranks:
        one_derivative, one_hessian = one_step_bounds(rank)
        hessian = (
            one_hessian * derivative * derivative
            + one_derivative * hessian
        )
        derivative *= one_derivative
        inverse_derivative *= one_derivative
    return derivative, inverse_derivative, hessian


def pullback_face_bound(
    ranks: Iterable[int], gradient_upper: int, hessian_upper: int
) -> dict[str, Any]:
    rank_path = tuple(ranks)
    if type(gradient_upper) is not int or gradient_upper < 1:
        raise ValueError("gradient upper")
    if type(hessian_upper) is not int or hessian_upper < 0:
        raise ValueError("hessian upper")
    derivative, inverse_derivative, prefix_hessian = prefix_bounds(rank_path)
    face_hessian = (
        hessian_upper * derivative * derivative
        + gradient_upper * prefix_hessian
    )
    curvature = Q(3, 2) * inverse_derivative * face_hessian
    return {
        "rank_path": list(rank_path),
        "time_depth": len(rank_path),
        "base_gradient_l1_upper": gradient_upper,
        "base_gradient_l1_lower": "1",
        "base_Hessian_operator_upper": hessian_upper,
        "prefix_D_infinity_strict_upper": str(derivative),
        "prefix_inverse_D_infinity_strict_upper": str(inverse_derivative),
        "prefix_D2_infinity_strict_upper": str(prefix_hessian),
        "pullback_gradient_l1_strict_lower": f"1/{inverse_derivative}",
        "pullback_Hessian_operator_strict_upper": str(face_hessian),
        "unit_speed_face_C2_seminorm_strict_upper": qstr(curvature),
    }


def base_face_geometry() -> dict[str, Any]:
    tangent_slope = KAPPA_MAX + 1 / GLOBAL_DISK_GAP
    tangent_curvature = (
        KAPPA_MAX / GLOBAL_DISK_GAP
        + 2 / GLOBAL_DISK_GAP**2
        + Q(9, 25) / GLOBAL_DISK_GAP**3
    )
    if not tangent_slope < 29:
        raise RuntimeError("tangent slope")
    if not tangent_curvature < 4949:
        raise RuntimeError("tangent curvature")

    gray_other_corner = 1 - Q(9, 25)
    white_center_corner_squared = Q(199, 400) ** 2 + Q(1, 2) ** 2
    if not white_center_corner_squared > Q(7, 10) ** 2:
        raise RuntimeError("white corner center gap")
    white_corner = Q(7, 10) - Q(4, 25)
    corner_distance = min(gray_other_corner, white_corner)
    if corner_distance != Q(27, 50) or not corner_distance > Q(1, 2):
        raise RuntimeError("corner distance")
    corner_slope = KAPPA_MAX + 2
    corner_curvature = 2 * KAPPA_MAX + 8
    if corner_slope != Q(33, 4) or not corner_slope < 9:
        raise RuntimeError("corner slope")
    if corner_curvature != Q(41, 2) or not corner_curvature < 21:
        raise RuntimeError("corner curvature")

    return {
        "global_distinct_disk_boundary_gap_strict_lower": qstr(GLOBAL_DISK_GAP),
        "global_circle_tangency_face": {
            "graph_slope_formula": "h'=-kappa_source-cp_source/ell",
            "graph_second_derivative_bound": (
                "abs(h'')<=kappa/ell+2/ell^2+R_target/ell^3"
            ),
            "absolute_graph_slope_strict_upper": "29",
            "graph_C2_strict_upper": "4949",
            "level_function": "G(r,phi)=phi-h(r)",
            "level_gradient_l1_lower": "1",
            "level_gradient_l1_upper": "30",
            "level_Hessian_operator_strict_upper": "4949",
            "face_not_recovery_carrier": True,
        },
        "selected_64_moving_occurrence_face": {
            "selected_tangent_flight_strict_lower": "1/10",
            "absolute_graph_slope_strict_upper": "17",
            "graph_C2_strict_upper": "623",
            "level_gradient_l1_upper": "18",
            "level_Hessian_operator_strict_upper": "623",
            "same_64_occurrence_ids_as_parameterized_F10_seeds": True,
        },
        "forward_integer_corner_face": {
            "gray_same_center_corner_excluded": (
                "the ray to the source center has negative outgoing cosine"
            ),
            "gray_other_integer_corner_distance_lower": qstr(gray_other_corner),
            "white_integer_corner_center_distance_strict_lower": "7/10",
            "white_integer_corner_boundary_distance_strict_lower": qstr(
                white_corner
            ),
            "uniform_corner_ray_length_strict_lower": "1/2",
            "point_caustic_slope_formula": "h'=-kappa_source-cp_source/lambda",
            "absolute_graph_slope_strict_upper": "9",
            "graph_C2_strict_upper": "21",
            "level_gradient_l1_upper": "10",
            "level_Hessian_operator_strict_upper": "21",
        },
        "affine_coordinate_faces": {
            "kinds": [
                "target endpoint, wall chart seam or target homogeneity face before pullback",
                "coordinate velocity zero after fixed-angle reparameterization",
                "source endpoint or source chart seam",
                "source momentum homogeneity face",
                "stationary C24 core face",
            ],
            "base_level_gradient_l1_upper": "1",
            "base_level_Hessian": "0",
            "coordinate_velocity_zero_graph_slope_absolute_upper": "25/4",
            "coordinate_velocity_zero_graph_second_derivative": "0",
        },
    }


def seven_kind_matrix() -> list[dict[str, Any]]:
    rows = [
        {
            "type": "candidate_signed_tangency",
            "base_model": "global_circle_tangency_face",
            "base_gradient_upper": 30,
            "base_Hessian_upper": 4949,
        },
        {
            "type": "target_endpoint_on_wall_or_target_chart_seam",
            "base_model": "affine_target_coordinate_then_regular_pullback",
            "base_gradient_upper": 1,
            "base_Hessian_upper": 0,
        },
        {
            "type": "target_momentum_homogeneity_face",
            "base_model": "affine_target_phi_then_regular_pullback",
            "base_gradient_upper": 1,
            "base_Hessian_upper": 0,
        },
        {
            "type": "forward_integer_corner_ray",
            "base_model": "point_caustic_graph",
            "base_gradient_upper": 10,
            "base_Hessian_upper": 21,
        },
        {
            "type": "coordinate_velocity_zero",
            "base_model": "fixed_global_angle_graph",
            "base_gradient_upper": 8,
            "base_Hessian_upper": 0,
        },
        {
            "type": "source_endpoint_on_wall_or_source_chart_seam",
            "base_model": "affine_source_r",
            "base_gradient_upper": 1,
            "base_Hessian_upper": 0,
        },
        {
            "type": "source_momentum_homogeneity_face",
            "base_model": "affine_source_phi",
            "base_gradient_upper": 1,
            "base_Hessian_upper": 0,
        },
    ]
    if len({row["type"] for row in rows}) != 7:
        raise RuntimeError("seven types")
    for row in rows:
        row["arbitrary_regular_prefix_pullback_F9"] = (
            "CERTIFIED_BY_RANK_PATH_CHAIN_RULE"
        )
    return rows


def build_result() -> dict[str, Any]:
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    prior = load(
        "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json"
    )["result"]
    roots = load(
        "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
    )["result"]
    slopes = load(
        "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
    )["result"]
    curvature = load(
        "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
    )["result"]
    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]

    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("carrier")
    if prior["five_face_kind_matrix"]["terminal_core_preimage_face"]["F9"] != (
        "CERTIFIED_RANK_PATH_TEMPLATE_ON_EACH_REGULAR_COMPONENT"
    ):
        raise RuntimeError("prior F9")
    grammar = roots["physical_branch_slope_and_root_grammar"]
    if grammar["branch_type_count"] != 7:
        raise RuntimeError("branch grammar")
    if not grammar["every_active_branch_has_at_most_one_isolated_root"]:
        raise RuntimeError("root simplicity")
    if slopes["exact_oriented_slope_bounds"][
        "tangent_to_miss_gap_strict_lower"
    ] != qstr(GLOBAL_DISK_GAP):
        raise RuntimeError("disk gap")
    c2 = curvature["curvature_log_density_and_partial_cost"][
        "bidirectional_carrier_C2_bounds"
    ]
    if c2["source_reverse_curvature_strict_upper"] != "623":
        raise RuntimeError("source curvature")
    if c2["miss_forward_curvature_strict_upper"] != "4949":
        raise RuntimeError("global curvature")
    if not f8["parameterized_connected_face_registry"][
        "all_five_physical_face_grammars_covered"
    ]:
        raise RuntimeError("five face grammar")

    kind_rows = seven_kind_matrix()
    frozen_types = [row["type"] for row in grammar["branch_types"]]
    if [row["type"] for row in kind_rows] != frozen_types:
        raise RuntimeError("branch type join")

    samples = [
        pullback_face_bound((), 30, 4949),
        pullback_face_bound((14,), 30, 4949),
        pullback_face_bound((14, 15), 18, 623),
        pullback_face_bound((14, 16, 18), 10, 21),
        pullback_face_bound((20, 14, 17, 15), 1, 0),
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "depth_scope": "every finite regular arbitrary-R_n rank path",
        },
        "base_physical_face_geometry": base_face_geometry(),
        "seven_one_step_boundary_kind_F9_join": {
            "frozen_branch_type_count": 7,
            "rows": kind_rows,
            "rows_sha256": digest(kind_rows),
            "all_frozen_one_step_physical_boundary_types_covered": True,
            "owner_changes_reduce_to_tangency_or_coordinate_boundary_types": True,
            "equal_positive_roots_of_distinct_disks_used": False,
        },
        "general_base_face_rank_path_recurrence": {
            "prefix_values": "D_0=E_0=1, H_0=0",
            "prefix_recurrence": [
                "D_j=L(B_j)D_(j-1)",
                "E_j=L(B_j)E_(j-1)",
                "H_j=M(B_j)D_(j-1)^2+L(B_j)H_(j-1)",
            ],
            "one_step_envelopes": [
                "L(B)=150*2^B",
                "M(B)=42672*2^(3B)",
            ],
            "base_contract": "1<=||dG||_1<=G0 and ||D2G||<=K0",
            "pullback_gradient_lower": "||d(G o T^j)||_1>1/E_j",
            "pullback_Hessian_upper": "K0*D_j^2+G0*H_j",
            "unit_speed_C2_upper": (
                "(3/2)*E_j*(K0*D_j^2+G0*H_j)"
            ),
            "finite_for_every_finite_rank_path": True,
            "sample_replays": samples,
            "sample_replays_sha256": digest(samples),
        },
        "five_face_kind_matrix": {
            "source_core_clipping_face": {
                "F9": "CERTIFIED_LEVEL_ZERO_AFFINE",
                "F10": "CERTIFIED_LEVEL_ZERO_STATIONARY_ONLY",
            },
            "intermediate_core_avoidance_preimage_face": {
                "F9": "CERTIFIED_ALL_FINITE_RANK_PATHS",
                "F10": "NOT_CERTIFIED",
            },
            "terminal_core_preimage_face": {
                "F9": "CERTIFIED_ALL_FINITE_RANK_PATHS",
                "F10": "NOT_CERTIFIED",
            },
            "collision_singularity_or_owner_change_face": {
                "F9": "CERTIFIED_ALL_SEVEN_BASE_KINDS_AND_FINITE_PULLBACKS",
                "F10": "NOT_CERTIFIED",
            },
            "moving_occurrence_face": {
                "F9": "CERTIFIED_64_BASE_FACES_AND_FINITE_PULLBACKS",
                "F10": "CERTIFIED_SEED_LEVEL_PARAMETERIZED_ONLY",
            },
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "6/18",
            "newly_completed_parameterized_field": "F9 face_C2_atlas_bound",
            "current_global_maturity": "7/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "recovery_carrier_curvature_retyped_as_face_curvature": False,
            "rank_path_values_are_uniform_in_depth_or_rank": False,
            "F9_rank_path_cost_has_global_physical_Lp_sum": False,
            "complete_F9_physical_face_C2_parameterized_atlas": "CERTIFIED",
            "complete_F10_all_face_coarea_regular_atlas": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate5_round36_all_face_rank_path_f9_verifier.py",
    )
    args = parser.parse_args()
    if args.print_manifest:
        print(json.dumps(manifest(args.verifier), indent=2, sort_keys=True))
        return 0
    result = build_result()
    print("ALL_FIVE_FACE_KIND_F9: CERTIFIED_PARAMETERIZED")
    print(result["strict_nonpromotion"]["Gate5_maturity"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
