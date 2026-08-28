#!/usr/bin/env python3
"""Round-38 sampled C24 projective-order strong-tail certificate.

The sparse C24 opening theorem already returns every normalized scheduled
block output to a strict projective subcone, and the round-34 hit-gap
certificate gives an explicit mass survival factor.  Combining finite
Hilbert diameter with the order norm of Demers--Liverani upgrades that
scheduled weak mass tail to a qualitative strong tail in the projective
cone order norm, with an explicit rational exponential rate.

This is not a standard-family Growth/Z estimate.  An exact disintegration
countermodel records why the density-level cone object does not determine a
representation-dependent standard-family Z.  The all-collision full-Q_N
carrier bridge therefore remains open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round38-sampled-projective-strong-tail.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json": (
        "4166a72c603666a5ff2b5422dd167b5dd4fa1e4ab25fdd99b77af2e543cc33a8"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}

EPSILON = Q(21, 111718750)
SURVIVAL = 1 - EPSILON
WEIGHT = Q(SURVIVAL.denominator + SURVIVAL.numerator, 2 * SURVIVAL.numerator)
WEIGHTED_SURVIVAL = WEIGHT * SURVIVAL


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


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
    opening = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]["sparse_opening_theorem_interface"]
    if opening["large_hole_sparse_opening_cone_recovery"] != (
        "CERTIFIED_THEOREM_MATCH_WITH_EXISTENTIAL_DELTA_CHI_J_NSTAR"
    ):
        raise RuntimeError("open cone recovery")
    if opening["numeric_cone_contraction_chi"] is not None:
        raise RuntimeError("chi scope")
    if opening["theorem_supplied_sparse_constants_uniform_over_parameter_window"] is not True:
        raise RuntimeError("uniform theorem interface")

    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]
    hit = sparse["uniform_recovered_cone_hit_gap"]
    if hit["explicit_per_block_hit_gap_epsilon"] != qstr(EPSILON):
        raise RuntimeError("epsilon")
    if hit["explicit_per_block_survival_factor"] != qstr(SURVIVAL):
        raise RuntimeError("survival")
    if hit["numeric_N_open"] is not None:
        raise RuntimeError("N_open scope")
    if not hit["induction_closure"].startswith("Proposition_8.7_returns_every"):
        raise RuntimeError("induction closure")
    tail = sparse["scheduled_and_all_time_tail"]
    if tail["uniform_unweighted_exponential_collision_return_tail"] != "CERTIFIED":
        raise RuntimeError("weak tail")

    delayed = load(
        "cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json"
    )["result"]
    if delayed["strict_nonpromotion"]["full_QN_uniform_characteristic_multiplier"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("full QN scope")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("common carrier")
    if carrier["strict_nonpromotion"]["complete_numeric_C_fw_C_rev"] != "NOT_CERTIFIED":
        raise RuntimeError("carrier scope")


def projective_order_bridge() -> dict[str, Any]:
    return {
        "source": (
            "Demers--Liverani arXiv:2104.06947v3, Proposition 8.7, "
            "Proposition 6.13, Definition 8.14 and Lemma 8.15"
        ),
        "base_cone": "C=C_{c,A,L}(delta)",
        "strict_normalized_image": "C_chi=C_{chi*c,chi*A,chi*L}(delta)",
        "theorem_supplied_finite_Hilbert_diameter": "Delta_open<infinity",
        "order_norm": "||f||_*=inf{lambda>=0:-lambda<=_C f<=_C lambda}",
        "same_mass_projective_coordinates": (
            "for mass(h)=mass(1)=1, alpha(h,1)<=1<=beta(h,1)"
        ),
        "diameter_implication": (
            "beta/alpha<=exp(Delta_open) implies exp(-Delta_open)<=alpha<=1<=beta<=exp(Delta_open)"
        ),
        "normalized_strong_bound": "||h||_*<=K_cone:=exp(Delta_open)",
        "constant_density_one_is_the_projective_reference": True,
        "uniform_qualitative_K_cone_over_parameter_window": True,
        "numeric_Delta_open": None,
        "numeric_K_cone": None,
        "bridge_status": "CERTIFIED_QUALITATIVE",
    }


def sampled_strong_tail() -> dict[str, Any]:
    if not WEIGHT > 1 or not WEIGHTED_SURVIVAL < 1:
        raise RuntimeError("weight")
    if 1 - WEIGHTED_SURVIVAL != Q(21, 223437500):
        raise RuntimeError("weighted margin")
    return {
        "scheduled_block_operator": "K_s f=L_s^N_open(1_{C24^c}f)",
        "input_scope": "f>=0 in the base projective cone, for every fixed |s|<=1/400",
        "normalized_block_output": "K_s^k f / mass(K_s^k f) lies in C_chi for every k>=1",
        "explicit_mass_survival_factor_r": qstr(SURVIVAL),
        "weak_mass_bound": "mass(K_s^k f)<r^k*mass(f)",
        "projective_order_strong_bound": (
            "||K_s^k f||_*<K_cone*r^k*mass(f), k>=1"
        ),
        "one_rational_block_weight_w": qstr(WEIGHT),
        "weighted_factor_w_times_r": qstr(WEIGHTED_SURVIVAL),
        "weighted_factor_margin": qstr(1 - WEIGHTED_SURVIVAL),
        "weighted_green_sum_safe_upper": (
            "sum_{k>=1}w^k||K_s^k f||_*"
            "<K_cone*(223437500/21)*mass(f)"
        ),
        "explicit_rational_rate_and_resolvent": "CERTIFIED",
        "strong_norm_type": "Demers--Liverani projective-cone order norm",
        "numeric_collision_time_rate": "NOT_CERTIFIED_BECAUSE_N_open_IS_NONNUMERIC",
    }


def standard_family_nonuniqueness() -> dict[str, Any]:
    rows = []
    for pieces in (1, 2, 4, 8, 16):
        rows.append(
            {
                "pieces_per_horizontal_leaf": pieces,
                "piece_length": qstr(Q(1, pieces)),
                "weight_per_piece": qstr(Q(1, pieces)),
                "same_total_density": "1_on_[0,1]^2",
                "standard_family_Z": str(pieces),
            }
        )
    return {
        "scope": "exact disintegration nonuniqueness, not a billiard impossibility theorem",
        "density": "Lebesgue density 1 on the unit square",
        "unsplit_disintegration": "full horizontal leaves of length 1 with Z=1",
        "split_disintegration": (
            "split every horizontal leaf into k equal pieces, assign each normalized piece weight 1/k, and obtain Z=k"
        ),
        "growth_functional": "Z=sum_component weight(component)/length(component)",
        "same_density_and_same_projective_cone_element_for_every_k": True,
        "same_projective_order_norm_for_every_k": True,
        "representation_dependent_Z_is_unbounded": True,
        "representative_rows": rows,
        "projective_order_tail_implies_standard_family_Z_tail": False,
        "required_bridge": (
            "join each scheduled cone output to the frozen canonical same-ID parent-W disintegration with a uniform Z comparison"
        ),
    }


def installation_frontier() -> dict[str, Any]:
    return {
        "scheduled_sparse_C24_projective_strong_skeleton": "CERTIFIED_QUALITATIVE",
        "all_collision_first_return_Qn_projective_strong_tail": "NOT_CERTIFIED",
        "full_QN_standard_family_characteristic_C_N": "NOT_CERTIFIED",
        "canonical_same_ID_cone_to_standard_family_Z_comparison": "NOT_CERTIFIED",
        "native_no_hidden_cut_dwell": "NOT_CERTIFIED",
        "silently_replace_frozen_first_return_by_sampled_return": False,
        "replacement_requires": (
            "a same-phase Kac/inducing equivalence and transport of DQ, currents and cemetery"
        ),
        "next_exact_target": (
            "prove a uniform cone-to-canonical-Z comparison on scheduled survivors, or directly prove full-Q_N C_N*a^N<1"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "uniformly for every fixed |s|<=1/400",
            "claim_type": "scheduled projective-order strong tail with exact nonpromotion",
        },
        "projective_order_norm_bridge": projective_order_bridge(),
        "sampled_C24_killed_strong_tail": sampled_strong_tail(),
        "standard_family_representation_nonuniqueness": standard_family_nonuniqueness(),
        "physical_installation_frontier": installation_frontier(),
        "strict_nonpromotion": {
            "scheduled_C24_projective_order_norm_exponential_tail": (
                "CERTIFIED_QUALITATIVE_WITH_EXPLICIT_RATIONAL_RATE"
            ),
            "numeric_N_open_Delta_open_K_cone": "NOT_CERTIFIED",
            "all_collision_full_QN_strong_tail": "NOT_CERTIFIED",
            "standard_family_Z_or_Growth_tail": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate34_round38_sampled_projective_strong_tail_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "SCHEDULED_PROJECTIVE_STRONG_TAIL:",
        result["strict_nonpromotion"][
            "scheduled_C24_projective_order_norm_exponential_tail"
        ],
    )
    print("STANDARD_FAMILY_Z_TAIL: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
