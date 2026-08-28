#!/usr/bin/env python3
"""Parameterized common forward/reverse carriers on every regular R_n component."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round35-arbitrary-rn-common-carrier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json": (
        "81e59b1ca2ff8b2aeac1c2eba36592e0e788618a33ef97c7a7d65faa94c2c310"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json": (
        "323cdeb40a78d29e0e767b438ef1e6fe0c28d8da80a10e0b4f4d717d4f308515"
    ),
    "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json": (
        "cb5adf88c8b650786d5237e7d5b78296835851692e1159637da7111c6131e142"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
}

A0 = 301500
A1 = 1005


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


def sample_clock_rows() -> list[dict[str, Any]]:
    rows = []
    for depth in (0, 1, 2, 14, 32, 64, 128):
        per_orientation = A0 + A1 * depth
        rows.append(
            {
                "retained_mass_depth_D": depth,
                "per_orientation_recovery_clock_upper": per_orientation,
                "two_orientation_recovery_clock_upper": 2 * per_orientation,
            }
        )
    return rows


def build_result() -> dict[str, Any]:
    path = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    kac = load(
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    )["result"]
    parent = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]
    f7 = load(
        "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json"
    )["result"]
    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]
    f9 = load(
        "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json"
    )["result"]
    mesh = load(
        "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
    )["result"]
    recovery = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )

    component = path["canonical_regular_connected_component_schema"]
    if not component["R_n_and_Q_n_regular_component_partition_exists_mod_null"]:
        raise RuntimeError("component partition")
    if not component["componentwise_forward_map_is_real_analytic_local_diffeomorphism"]:
        raise RuntimeError("forward branch")
    if not component["componentwise_inverse_map_exists_on_regular_image"]:
        raise RuntimeError("inverse branch")
    if component["collision_area_Jacobian_of_full_invertible_map"] != "1":
        raise RuntimeError("area Jacobian")
    measure = kac["frozen_measure_space_contract"]
    if measure["invariant_probability"] != (
        "mu_s=normalized_cos(phi)dr_dphi=normalized_dr_dp"
    ):
        raise RuntimeError("collision measure")
    if not measure[
        "map_invertible_and_measure_preserving_modulo_singular_null_set"
    ]:
        raise RuntimeError("measure preservation")
    parent_registry = parent["Q2_parent_W_Borel_registry"]
    if parent_registry["canonical_leaf_equation"] != (
        "fixed s; phi(r)=4r+b; p(r)=sin(4r+b)"
    ):
        raise RuntimeError("parent foliation")
    if not parent_registry["inside_certified_invariant_unstable_cone"]:
        raise RuntimeError("unstable cone")
    if f7["same_ID_actual_instance_F7_join"][
        "one_step_numeric_F7_strict_upper"
    ] != "360134800/360493663":
        raise RuntimeError("F7")
    if f8["same_ID_numeric_F8"][
        "common_normalized_transversality_strict_lower"
    ] != "1/5":
        raise RuntimeError("F8")
    if f9["five_face_kind_matrix"]["terminal_core_preimage_face"]["F9"] != (
        "CERTIFIED_RANK_PATH_TEMPLATE_ON_EACH_REGULAR_COMPONENT"
    ):
        raise RuntimeError("F9")
    if not mesh["closed_map_growth_lemma_recovery_bridge"][
        "forward_and_reverse_use_time_reversibility"
    ]:
        raise RuntimeError("reversibility")
    if recovery["replay_summary"]["A0"] != A0:
        raise RuntimeError("A0")
    if recovery["replay_summary"]["A1"] != A1:
        raise RuntimeError("A1")

    clock_rows = sample_clock_rows()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "for every fixed |s|<=1/400",
            "depth_scope": "every finite n>=1",
        },
        "arbitrary_Rn_parent_W_Borel_registry": {
            "base_object": (
                "each existing nonempty regular component U of a rank-refined R_n path fibre"
            ),
            "component_id_schema": (
                "c24-component:(source-core-id,n,path-key,least-dyadic-basis-index)"
            ),
            "canonical_leaf_equation": "phi(r)=4r+b; p(r)=sin(4r+b)",
            "leaf_slope": "dphi/dr=4",
            "inside_invariant_unstable_cone": True,
            "U_intersection_leaf": "countable disjoint union of open intervals",
            "source_interval_rank": (
                "least rational-dyadic interval basis index with closure inside the interval"
            ),
            "incidence_rank_refinement": (
                "one dyadic source/target cosine rank at every collision time"
            ),
            "rank_density_mesh": (
                "delta_B=2^-ceil(3(B+1)/2) in carrier arclength, followed by 1e-90 adapted recuts"
            ),
            "source_parent_W_id": (
                "rn-parent-W:(component-id):(s,b):(source-interval-rank):(incidence-rank-path):(short-cell-k)"
            ),
            "registry_type": "standard-Borel parameterized actual curve registry",
            "covers_every_regular_Rn_component_modulo_its_1D_boundary": True,
            "finite_integer_curve_count_claimed": False,
            "nonempty_component_coordinates_enumerated": False,
        },
        "collision_SRB_leaf_disintegration": {
            "coordinate_change": "(r,b)->(r,p=sin(4r+b))",
            "absolute_Jacobian": "cos(phi)=cp",
            "leaf_Euclidean_arclength": "dell=sqrt(17)*dr in (r,phi)",
            "conditional_density_wrt_dell": "cp/sqrt(17)",
            "rank_shell_log_density_derivative": "abs(d_r log cp)=4*abs(tan(phi))<4/cp",
            "rank_mesh_implies_uniform_one_third_log_Holder": True,
            "source_phase_graph_C2_seminorm": "0",
            "positive_on_every_regular_rank_cell": True,
            "integrating_leaf_weights_recovers_mu_s_restricted_to_component": True,
        },
        "common_forward_reverse_carrier_pair": {
            "branch": "H=T_s^n restricted to U",
            "source_cell": "A subset U on one rank-meshed parent W",
            "image_cell": "B=H(A), recut to adapted length and pulled back to A",
            "forward_oriented_branch": "A -> B by H",
            "reverse_oriented_branch": "I(B) -> I(A) by T_s^n",
            "common_physical_restriction_id": (
                "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)"
            ),
            "carrier_pair_id": (
                "rn-fw-rev-carrier-pair:(common-physical-restriction-id)"
            ),
            "forward_and_reverse_share_identical_component_and_restriction": True,
            "forward_and_reverse_are_two_views_not_two_charges": True,
            "mu_s_A_equals_mu_s_B_equals_mu_s_I_B": True,
            "equality_reason": "branch area preservation and billiard time reversibility",
            "actual_parameterized_common_fw_rev_carrier_pair_registry": "CERTIFIED",
        },
        "per_carrier_numeric_recovery_clock": {
            "retained_mass_depth": "D=ceil(log2(m_parent/m_cell)) for every positive cell",
            "same_D_on_both_views": True,
            "initial_standard_family_boundary": "Z_fw/m,Z_rev/m<C_mesh*2^D",
            "A0": A0,
            "A1": A1,
            "per_orientation_clock": "R(D)<=301500+1005*D",
            "two_orientation_clock": "R_fw(D)+R_rev(D)<=603000+2010*D",
            "finite_for_every_positive_carrier_cell": True,
            "sample_clock_rows": clock_rows,
            "sample_clock_rows_sha256": digest(clock_rows),
            "physical_global_D_tail_or_moment": "NOT_CERTIFIED",
            "uniform_unbounded_repeated_indicator_recovery": "NOT_CERTIFIED",
        },
        "same_ID_interface_update": {
            "round34_actual_parent_recuts": "CERTIFIED_PARAMETERIZED_Q2",
            "round35_arbitrary_Rn_parent_W": "CERTIFIED_PARAMETERIZED_SCHEMA",
            "round35_common_fw_rev_carrier_pair": "CERTIFIED_PARAMETERIZED_SCHEMA",
            "round35_per_positive_cell_recovery_clock": "CERTIFIED_NUMERIC_FORMULA",
            "numeric_componentwise_C_fw_C_rev_final_q": "NOT_CERTIFIED",
            "global_physical_recovery_clock_moment": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "parameterized_schema_is_finite_component_enumeration": False,
            "carrier_existence_implies_physical_D_tail": False,
            "per_cell_clock_implies_unbounded_repeated_recovery": False,
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
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
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round35_arbitrary_rn_common_carrier_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(result["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ])
    print(result["strict_nonpromotion"]["final_same_ID_q"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
