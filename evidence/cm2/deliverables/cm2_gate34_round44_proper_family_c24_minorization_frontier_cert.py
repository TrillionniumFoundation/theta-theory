#!/usr/bin/env python3
"""Round-44 direct proper-family C24 minorization frontier.

The numerical C24 killed-Growth block is already available, but Growth and
properness only control inverse unstable length.  They do not by themselves
force mass into a fixed target.  This certificate freezes the two shortest
valid numerical interfaces:

* a proper-family mixing estimate against the existing interior C24 bump;
* a C24-contained coupling magnet with a numerical coupling fraction.

It also audits the exact constants used by Stenlund--Young--Zhang
arXiv:1210.0011v4.  Those constants are existential and the frozen C24
rectangles have not been certified as a stable-saturated magnet.  Hence this
is a fail-closed frontier, not a numerical minorization claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round44-proper-family-c24-minorization-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round44-proper-family-c24-minorization-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round43-nopen-effectivity-frontier-manifest-2026-07-19.json": (
        "a1cadbde072056713d4d7fb1b83b02a7681a6c665578024376c48acd01d8d96b"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
}

BUMP_MASS = Q(21, 55859375)
HIT_GAP = Q(21, 111718750)
BUMP_C1 = 2724
N_GROWTH = 9148


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


def validate_dependencies() -> None:
    prior = load(
        "cm2-gate34-round43-nopen-effectivity-frontier-manifest-2026-07-19.json"
    )["result"]
    if prior["native_standard_family_bypass_frontier"][
        "numeric_native_standard_family_hit_minorization"
    ] != "NOT_CERTIFIED":
        raise RuntimeError("prior minorization scope")

    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]
    bump = sparse["explicit_C1_bump"]
    if bump["normalized_collision_SRB_integral_strict_lower"] != str(BUMP_MASS):
        raise RuntimeError("bump mass")
    if bump["C1_norm_strict_upper"] != str(BUMP_C1):
        raise RuntimeError("bump C1")
    hit = sparse["uniform_recovered_cone_hit_gap"]
    if hit["explicit_per_block_hit_gap_epsilon"] != str(HIT_GAP):
        raise RuntimeError("hit gap")
    if hit["numeric_N_open"] is not None:
        raise RuntimeError("sparse block overclaim")

    growth = load(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]
    killed = growth["numerical_C24_killed_Growth"]
    if killed["block_depth_n_star"] != N_GROWTH:
        raise RuntimeError("Growth depth")
    if killed["gamma_strict_bracket"] != "0.4999<gamma<1/2":
        raise RuntimeError("Growth coefficient")

    geometry = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    if geometry["frozen_core_inventory"]["core_count"] != 24:
        raise RuntimeError("C24 inventory")
    if geometry["frozen_core_inventory"]["boundary_edge_count_per_collision_component"] != 48:
        raise RuntimeError("C24 edges")

    recovery = load(
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    )
    if recovery["verdict"]["uniform_one_time_finite_s_recovery"] != "CERTIFIED":
        raise RuntimeError("one-time recovery")
    if recovery["result"]["scope_limits"]["physical_prefix_suffix_costs"] is not False:
        raise RuntimeError("recovery scope")


def scalar_nonimplication_countermodel() -> dict[str, Any]:
    cp = Q(4)
    theta = Q(1, 2)
    z_over_mass = Q(1)
    for depth in range(16):
        rhs = cp / 2 * (1 + theta**depth * z_over_mass)
        if z_over_mass > rhs:
            raise RuntimeError("countermodel Growth inequality")
    return {
        "purpose": (
            "show that the scalar properness/Growth inequalities alone do not imply a fixed-target hit; this is not a counterexample to the physical billiard"
        ),
        "abstract_space": "two disjoint unit unstable curves W_avoid and W_target",
        "map": "identity on both curves",
        "target": "W_target",
        "normalized_family": "unit density on W_avoid",
        "Z_over_mass": "1",
        "proper_constant_Cp": "4",
        "Growth_theta": "1/2",
        "Growth_inequality": "Z_n/m<=Cp/2*(1+theta^n*Z_0/m)",
        "Growth_inequality_holds_for_every_n": True,
        "family_is_proper": True,
        "target_hit_mass_at_every_time": "0",
        "logical_conclusion": (
            "a target-sensitive mixing or magnet input is necessary in addition to Growth"
        ),
    }


def bump_mixing_route() -> dict[str, Any]:
    if BUMP_MASS != 2 * HIT_GAP:
        raise RuntimeError("half-bump arithmetic")
    return {
        "frozen_bump": {
            "support": "closure strictly inside one C24 core",
            "pointwise": "0<=g<=1_C24",
            "mu_s_g_strict_lower": str(BUMP_MASS),
            "C1_norm_strict_upper": str(BUMP_C1),
            "uniform_parameter_window": "|s|<=1/400",
        },
        "required_proper_family_estimate": (
            "abs(G(g composed T_s^H)/mass(G)-mu_s(g))<=C_SF*theta_SF^H*norm_C1(g)"
        ),
        "required_numeric_inputs": [
            "C_SF>=1",
            "0<theta_SF<1",
            "one numerical H valid for every canonical proper family and every |s|<=1/400",
            "same-family closure/recovery after C24 restriction",
        ],
        "safe_threshold_formula": (
            "H_SF=max(0,1+ceil(log(2724*C_SF/epsilon_hit)/(-log(theta_SF))))"
        ),
        "epsilon_hit": str(HIT_GAP),
        "conditional_conclusion": (
            "mass(1_C24*T_s^H_SF G)>epsilon_hit*mass(G)"
        ),
        "numeric_C_SF": None,
        "numeric_theta_SF": None,
        "numeric_H_SF": None,
        "status": "EXACT_SUFFICIENT_INTERFACE_ONLY",
    }


def magnet_route() -> dict[str, Any]:
    missing = [
        "numeric Cp,vartheta_p,np in Lemma 16",
        "one reference unstable curve W_tilde_f whose stable magnet is contained in C24",
        "numeric local-stable-leaf density and gap distribution inside that C24 magnet",
        "numeric finite-scale mixing time s and crossing fraction zeta_0 in Proposition 31",
        "numeric distortion/cropping loss converting zeta_0 to the Corollary-32 coupling fraction zeta",
        "numeric recovery constants r,C,lambda from Lemma 30",
        "numeric coupling spacing Delta from Lemma 33",
        "uniform verification of all preceding constants for every |s|<=1/400",
    ]
    return {
        "official_source": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
        "source_chain": [
            "Lemma 16: proper-family recovery with existential Cp and vartheta_p",
            "Proposition 31 and Corollary 32: existential magnet crossing/coupling fraction zeta",
            "Lemma 30: existential gap-recovery constants r,C,lambda",
            "Lemma 33 and Corollary 34: uncoupled tail (1-zeta/2)^(n/Delta-1)",
        ],
        "published_constants_are_uniform_but_not_numerical": True,
        "C24_rectangle_geometry_is_a_certified_SYZ_magnet": False,
        "C24_stable_saturation_and_physical_holonomy": "NOT_CERTIFIED",
        "conditional_C24_hit": (
            "if S_C24 subset C24 and the Corollary-32 fraction is zeta>0, then one coupling block hits C24 with mass at least zeta*mass(G)"
        ),
        "conditional_collision_tail": (
            "uncoupled_mass(n)<= (1-zeta/2)^(n/Delta-1)"
        ),
        "conditional_collision_rate": "q_magnet=(1-zeta/2)^(1/Delta)<1",
        "missing_numerical_or_shape_inputs": missing,
        "missing_input_count": len(missing),
        "numeric_zeta": None,
        "numeric_Delta": None,
        "status": "THEOREM_ARCHITECTURE_MATCHED_BUT_C24_MAGNET_NOT_INSTALLED",
    }


def shortest_frontier() -> dict[str, Any]:
    return {
        "already_numeric": {
            "C24_killed_Growth_depth": N_GROWTH,
            "C24_killed_Growth_coefficient": "gamma<1/2",
            "interior_bump_mass": str(BUMP_MASS),
            "desired_hit_gap": str(HIT_GAP),
            "standard_family_recovery_clock": "R(D)<=301500+1005*D",
        },
        "first_missing_target_sensitive_object": (
            "a numerical canonical-proper-family C24 minorization with same-family return"
        ),
        "shortest_native_computational_contract": (
            "for every proper parent-W family G, certify one H_SF and epsilon_SF>0 on the same physical IDs, plus a numerical post-restriction return to the same proper class"
        ),
        "why_9148_is_not_H_SF": (
            "9148 contracts boundary Z for the C24-cut family; it contains no fixed-target mixing lower bound"
        ),
        "why_R_D_is_not_H_SF": (
            "R(D) recovers standard-family properness; it contains no C24 target incidence"
        ),
        "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
        "numeric_collision_time_C_fw_C_rev_q": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "literature_checked_through": "2026-07-19",
            "official_sources": [
                "arXiv:1210.0011v4",
                "arXiv:2104.06947v3",
                "arXiv:2604.19671v2",
                "arXiv:2606.10155v1",
            ],
            "claim_type": "exact sufficient interfaces and effectivity frontier",
        },
        "properness_Growth_nonimplication": scalar_nonimplication_countermodel(),
        "direct_smooth_bump_mixing_route": bump_mixing_route(),
        "C24_contained_coupling_magnet_route": magnet_route(),
        "shortest_numeric_frontier": shortest_frontier(),
        "strict_nonpromotion": {
            "properness_Growth_alone_implies_C24_hit": False,
            "numeric_proper_family_C24_minorization": "NOT_CERTIFIED",
            "numeric_C24_coupling_magnet": "NOT_CERTIFIED",
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
            / "cm2_gate34_round44_proper_family_c24_minorization_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "PROPER_FAMILY_C24_MINORZATION:",
        result["strict_nonpromotion"]["numeric_proper_family_C24_minorization"],
    )
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
