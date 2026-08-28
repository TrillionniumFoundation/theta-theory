#!/usr/bin/env python3
"""Round-41 hereditary C24 standard-family Growth certificate.

Round 40 treated Canestrari's ``hat F`` as a conditional survivor map and
therefore left a geometry match open.  The cited construction instead keeps
all mass and merely adds the hole boundary to the singularity set.  Demers'
general-hole hypotheses are exactly finite cutting complexity (H1) and weak
stable transversality (H2).  The frozen C24 geometry already supplies both.

This certificate installs the resulting block Growth inequality for the
extra-cut map and, by positive-subfamily monotonicity, for the unnormalised
every-collision C24 killed family.  It also records the qualitative weighted
aggregate-Z resolvent obtained after joining the recurrence to the scheduled
C24 mass tail.  Numerical n_*, Z_0, C_fw, C_rev and q remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round41-c24-hereditary-growth.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round40-c24-standard-family-growth-frontier-manifest-2026-07-19.json": (
        "0d41fffde0a5e2061bff789a3899f88894c48417b181860b8f71a5be2a28bf76"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json": (
        "6aab6003fecfb705c924cced3ca5eb0d64012b1bf4db4816a2a9ac7012b2f6bf"
    ),
    "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json": (
        "cb5adf88c8b650786d5237e7d5b78296835851692e1159637da7111c6131e142"
    ),
}

B0 = 49
C0 = 1493
THETA = Q(900337, 901685)
SURVIVAL = Q(111718729, 111718750)
BARE_HALF_BLOCK = 9148


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


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
        "cm2-gate34-round40-c24-standard-family-growth-frontier-manifest-2026-07-19.json"
    )["result"]
    target = prior["native_C24_standard_family_Growth_target"]
    if target["hereditary_C24_open_Growth"] != "NOT_CERTIFIED":
        raise RuntimeError("round40 frontier")
    if target["operator_type"] != (
        "fixed-s conditional survivor evolution on the same canonical parent-W standard-family registry"
    ):
        raise RuntimeError("round40 operator statement to correct")

    geometry = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    stable = geometry["stable_curve_open_hole_geometry"]
    inventory = geometry["frozen_core_inventory"]
    interface = geometry["sparse_opening_theorem_interface"]
    if stable["O1_complexity_P0"] != B0:
        raise RuntimeError("C24 H1")
    if stable["certified_O2_constant_Ct"] != C0:
        raise RuntimeError("C24 H2")
    if stable["stable_slope_interval"] != (
        "-4108425/145348<dphi/dr<-25/9"
    ):
        raise RuntimeError("stable cone")
    if inventory["boundary_edge_count_per_collision_component"] != 48:
        raise RuntimeError("C24 edges")
    if interface["compact_uniform_table_family"] is not True:
        raise RuntimeError("uniform table family")

    growth = load(
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if growth["global_one_step_Xi_strict_upper"] != qstr(THETA):
        raise RuntimeError("closed one-step expansion")
    if growth["global_one_step_weighted_Growth_contraction"] is not True:
        raise RuntimeError("closed contraction")

    strong = load(
        "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json"
    )["result"]
    sampled = strong["sampled_C24_killed_strong_tail"]
    if sampled["explicit_mass_survival_factor_r"] != qstr(SURVIVAL):
        raise RuntimeError("scheduled mass rate")
    if sampled["scheduled_block_operator"] != (
        "K_s f=L_s^N_open(1_{C24^c}f)"
    ):
        raise RuntimeError("scheduled operator")

    initial = load(
        "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
    )["result"]
    family = initial["oriented_standard_family_contract"]
    if family["single_depth_K_atom_initial_standard_family_boundary"] != (
        "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K"
    ):
        raise RuntimeError("finite-Z initial families")


def exact_bare_threshold() -> dict[str, Any]:
    n = BARE_HALF_BLOCK
    current_left = 2 * (1 + n * (B0 - 1)) * pow(THETA.numerator, n)
    current_right = pow(THETA.denominator, n)
    previous = n - 1
    previous_left = (
        2
        * (1 + previous * (B0 - 1))
        * pow(THETA.numerator, previous)
    )
    previous_right = pow(THETA.denominator, previous)
    if not current_left < current_right:
        raise RuntimeError("bare half-block")
    if not previous_left >= previous_right:
        raise RuntimeError("bare half-block minimality")
    return {
        "closed_map_one_step_expansion_theta": qstr(THETA),
        "C24_cut_piece_bound_B0": B0,
        "Demers_fragmentation_factor": "1+n*(B0-1)=1+48*n",
        "exact_bare_Jacobian_half_threshold": n,
        "threshold_inequality": "(1+48*9148)*theta^9148<1/2",
        "previous_integer_fails": "(1+48*9147)*theta^9147>=1/2",
        "final_standard_family_block_is_9148": False,
        "why_not_final": (
            "the density-ratio, cone-metric and chopping prefactor is finite but not numerical"
        ),
    }


def operator_correction() -> dict[str, Any]:
    return {
        "round40_superseded_operator_typing": (
            "hat_F_C24 was called conditional survivor evolution"
        ),
        "correct_hat_operator": (
            "the closed billiard map with boundary(C24) added as artificial discontinuities; every descendant mass is retained"
        ),
        "conditional_operator_in_2604_19671v2": (
            "L_t restricts to survivors and renormalizes by surviving mass"
        ),
        "operator_correction_status": "CERTIFIED",
        "small_hole_perturbation_needed_for_this_Growth_step": False,
        "normalization_needed_for_unnormalized_killed_Growth": False,
    }


def demers_interface() -> dict[str, Any]:
    return {
        "primary_source": {
            "author": "Mark F. Demers",
            "title": "Dispersing Billiards with Small Holes",
            "year": 2014,
            "doi": "10.1007/978-1-4939-0419-8_8",
            "author_pdf_sha256_checked_2026_07_19": (
                "348c78b8096e013e6f38e39b77c9b8e148dedbe599ac46255c6e0481c0586f67"
            ),
        },
        "H1": (
            "every stable curve of length below delta0 is cut into at most B0 pieces by boundary(H)"
        ),
        "H2": (
            "m_W(N_epsilon(boundary(H)))<=C0*epsilon^(1/2) for small epsilon"
        ),
        "Demers_general_hole_class": "finite unions with finitely many compact smooth boundary arcs satisfying H1/H2",
        "C24_H1": "B0=49 on each collision component",
        "C24_stronger_tube_law": "m_W(N_epsilon(boundary(C24)))<=1493*epsilon",
        "C24_implies_H2": (
            "1493*epsilon<=1493*epsilon^(1/2) for 0<epsilon<=1"
        ),
        "unstable_time_reversed_geometry": {
            "slope": "25/9<dphi/dr<4108425/145348",
            "each_vertical_or_horizontal_edge_is_met_at_most_once": True,
            "piece_bound": B0,
            "tube_constant": C0,
        },
        "parameter_uniformity": (
            "all H1/H2, cone, horizon and closed one-step constants are uniform for every fixed |s|<=1/400"
        ),
        "general_hole_interface_status": "CERTIFIED_FOR_C24",
    }


def hereditary_growth() -> dict[str, Any]:
    return {
        "extra_cut_map": "hat_F_(s,C24)",
        "extra_cut_map_keeps_all_mass": True,
        "fragmentation_bound": (
            "sum_j |J F_s^(-n)|_* <= (1+48*n)*theta^n on sufficiently short descendants"
        ),
        "density_and_curvature_invariance": (
            "artificial boundary cuts restrict proper pairs without changing their on-piece density; closed-map distortion then preserves the proper class"
        ),
        "block_statement": (
            "for every chosen gamma in (0,1), there exist uniform finite n_*(gamma), Z0(gamma), Z1 with "
            "Z(hat_F^((p+1)n_*)G)<=gamma*Z(hat_F^(p n_*)G)+Z0*mass(G)"
        ),
        "chosen_reference_gamma": "1/2",
        "numeric_n_star": None,
        "numeric_Z0": None,
        "numeric_Z1": None,
        "uniform_parameter_scope": "every fixed |s|<=1/400",
        "hat_family_Growth": "CERTIFIED_QUALITATIVE_UNIFORM",
    }


def killed_subfamily() -> dict[str, Any]:
    return {
        "every_collision_killed_operator": (
            "O_s G=drop from hat_F_(s,C24)G every connected descendant lying in C24"
        ),
        "same_ID_registry": True,
        "positive_subfamily_monotonicity": (
            "for unnormalized weights, deleting descendants can only decrease mass and Z=sum_j p_j/|W_j|"
        ),
        "one_block_recurrence": (
            "Z(O_s^n_* G)<=gamma*Z(G)+Z0*mass(G), gamma=1/2"
        ),
        "recurrence_is_hereditary": (
            "the surviving subfamily remains proper and the same argument restarts after every block"
        ),
        "conditional_survival_normalization_used": False,
        "hereditary_C24_open_Growth": "CERTIFIED_QUALITATIVE_UNIFORM",
    }


def aggregate_resolvent() -> dict[str, Any]:
    return {
        "input": (
            "a controlled canonical finite-Z physical initial family dominated as a positive measure by an admissible base-cone source"
        ),
        "scheduled_mass_tail": (
            "mass(O_s^(k*N_open)G)<=r^k*mass(base source), r=111718729/111718750"
        ),
        "subset_reason": (
            "avoiding C24 at every collision is a subset of avoiding it only at scheduled N_open collisions"
        ),
        "common_block": "L=N_open*n_* collision steps",
        "common_block_coefficients": {
            "Growth_factor_g": "gamma^N_open<1",
            "mass_factor_rho": "r^n_*<1",
            "source_constant_C": "Z0/(1-gamma)<infinity",
        },
        "recurrence": "z_(p+1)<=g*z_p+C*m_p; m_p<=rho^p*m_base",
        "explicit_solution": (
            "z_p<=g^p*z_0+C*m_base*sum_(j=0)^(p-1) g^(p-1-j)*rho^j"
        ),
        "weighted_conclusion": (
            "there exists w_Z>1 with w_Z*max(g,rho)<1, hence sum_p w_Z^p z_p<infinity"
        ),
        "numeric_w_Z": None,
        "numeric_resolvent_constant": None,
        "cellwise_2_to_retained_depth_moment_used": False,
        "canonical_trace_from_projective_norm_used": False,
        "physical_aggregate_Z_weighted_tail": (
            "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "Round40 operator correction, general-hole C24 Growth installation, killed-subfamily inheritance and qualitative aggregate-Z resolvent"
            ),
            "literature_checked_through": "2026-07-19",
        },
        "round40_operator_correction": operator_correction(),
        "C24_Demers_H1_H2_match": demers_interface(),
        "exact_expansion_fragmentation_replay": exact_bare_threshold(),
        "extra_cut_standard_family_Growth": hereditary_growth(),
        "unnormalized_killed_subfamily_Growth": killed_subfamily(),
        "aggregate_canonical_Z_resolvent": aggregate_resolvent(),
        "strict_nonpromotion": {
            "round40_hat_operator_typing": "CORRECTED",
            "C24_Demers_H1_H2_general_hole_match": "CERTIFIED",
            "C24_extra_cut_Growth": "CERTIFIED_QUALITATIVE_UNIFORM",
            "hereditary_C24_open_Growth": "CERTIFIED_QUALITATIVE_UNIFORM",
            "physical_aggregate_Z_uniform_or_weighted_bound": (
                "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES"
            ),
            "numeric_n_star_Z0_Z1": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18_UNCHANGED",
            "Gate5": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate34_round41_c24_hereditary_growth_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "HEREDITARY_C24_OPEN_GROWTH:",
        result["strict_nonpromotion"]["hereditary_C24_open_Growth"],
    )
    print("NUMERIC_N_STAR_Z0_Z1: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
