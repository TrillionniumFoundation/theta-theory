#!/usr/bin/env python3
"""Round-43 effectivity audit for the scheduled C24 block N_open.

The sparse-hit certificate supplies an explicit hit gap but only an
existential collision block.  Round 42 made the native killed Growth block
fully numerical, so this certificate traces every remaining dependency in
the Demers--Liverani large-hole/mixing route.  Proposition 8.7 explicitly
declines to make the large-hole block dependence effective; the local frozen
artifacts likewise contain no numerical values for the required cone
recovery and projective-mixing constants.

The result is an exact effectivity frontier and a numerical replacement
interface.  It does not claim that no effective proof can exist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round43-nopen-effectivity-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round43-nopen-effectivity-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
}

HIT_GAP = Q(21, 111718750)
SURVIVAL = 1 - HIT_GAP
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
    growth = load(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]
    killed = growth["numerical_C24_killed_Growth"]
    if killed["block_depth_n_star"] != N_GROWTH:
        raise RuntimeError("numeric Growth block")
    if killed["numeric_n_star_Z0_Z1"] != "CERTIFIED_EXACT_SYMBOLIC":
        raise RuntimeError("numeric Growth constants")
    if growth["aggregate_canonical_Z_resolvent"][
        "scheduled_projective_block_N_open"
    ] is not None:
        raise RuntimeError("N_open was unexpectedly numerical")

    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]["uniform_recovered_cone_hit_gap"]
    if sparse["explicit_per_block_hit_gap_epsilon"] != str(HIT_GAP):
        raise RuntimeError("hit gap")
    if sparse["explicit_per_block_survival_factor"] != str(SURVIVAL):
        raise RuntimeError("survival")
    if sparse["numeric_N_open"] is not None:
        raise RuntimeError("sparse N_open scope")

    recovery = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    summary = recovery["replay_summary"]
    if summary["A0"] != 301500 or summary["A1"] != 1005:
        raise RuntimeError("standard-family recovery clock")
    if summary["numeric_C_fw_C_rev"] is not False:
        raise RuntimeError("recovery scope")


def theorem_effectivity_chain() -> dict[str, Any]:
    missing = [
        "C_delta in n_delta<=C_delta*log(delta^-1) from Lemma 8.6",
        "C_H and vartheta_H in the Lemma-8.6 closed-mixing estimate",
        "nbar_delta from Lemma 8.8",
        "minimal enlarged cone parameters c_double,A_double,L_double,delta_double",
        "Cstar_prime,kstar,nstar in NF_prime=Cstar_prime*abs(log delta)+kstar*nstar",
        "projective contraction chi for the enlarged cone",
        "J=m1+1 returning the enlarged cone to the base cone",
        "finite projective diameter Delta for that numerical enlarged cone",
        "Theorem-7.3 constants C_mix and vartheta_mix",
    ]
    return {
        "official_source": "arXiv:2104.06947v3",
        "large_hole_statement": "Proposition 8.7 with Lemmas 8.6 and 8.8",
        "published_effectivity_warning": (
            "Proposition 8.7 states that n_star has a worse dependence on delta that the authors refrain from making explicit"
        ),
        "explicit_enlarged_cone_relations": {
            "c_prime": "c*P0",
            "A_prime": "6*A/(1-mu(H))",
            "L_prime": "9*L/(1-mu(H))",
            "C24_P0": 49,
            "C24_Ct": 1493,
            "mu_H_strict_upper": "1/2500",
        },
        "conditional_large_hole_block": (
            "n_star=max(NF_prime,nbar_delta), N_return=J*n_star"
        ),
        "conditional_extra_mixing_time": (
            "m_mix=max(0,1+ceil(log(2724*C_mix/epsilon_hit)/(-log(vartheta_mix))))"
        ),
        "safe_conditional_schedule": (
            "N_open=max(N_return,nbar_delta+m_mix)"
        ),
        "epsilon_hit": str(HIT_GAP),
        "missing_numerical_inputs": missing,
        "missing_numerical_input_count": len(missing),
        "published_chain_evaluates_to_an_integer_from_frozen_data": False,
        "effectivity_gap_status": "CERTIFIED_MISSING_NUMERICAL_THEOREM_CONSTANTS",
    }


def local_bypass_audit() -> dict[str, Any]:
    return {
        "numerical_native_inputs_already_available": {
            "C24_killed_Growth_block": N_GROWTH,
            "C24_killed_Growth_coefficient": "gamma<1/2",
            "standard_family_recovery_clock": "R(D)<=301500+1005*D",
            "explicit_projective_hit_gap": str(HIT_GAP),
        },
        "type_separation": {
            "killed_Growth": "controls boundary Z after restriction",
            "standard_family_recovery": "controls properness/boundary complexity",
            "projective_hit_gap": "controls C24 mass only after cone recovery and mixing",
        },
        "invalid_inference_rejected": (
            "finite or recovered boundary Z alone does not imply positive mass in the fixed C24 target"
        ),
        "native_replacement_target": {
            "proper_class": "canonical parent-W families with Z(G)<=Z_proper*mass(G)",
            "required_numeric_minorization": (
                "find H_SF>=1 and epsilon_SF>0 such that mass(1_C24*T_s^H_SF G)>=epsilon_SF*mass(G) uniformly in |s|<=1/400"
            ),
            "required_same_family_return": (
                "the surviving normalized output returns to the same proper class after a numerical block"
            ),
            "why_sufficient": (
                "combined with the 9148-step killed Growth block it yields a numerical collision-time survival factor and removes N_open from the projective route"
            ),
        },
        "numeric_native_standard_family_hit_minorization": "NOT_CERTIFIED",
        "projective_route_replaced": False,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "literature_checked_through": "2026-07-19",
            "official_arXiv_snapshot": [
                "2104.06947v3",
                "2604.19671v2",
                "2606.10155v1",
            ],
            "claim_type": (
                "effectivity audit and exact replacement interface, not an impossibility theorem"
            ),
        },
        "published_projective_N_open_chain": theorem_effectivity_chain(),
        "native_standard_family_bypass_frontier": local_bypass_audit(),
        "strict_nonpromotion": {
            "numeric_C24_killed_Growth_block": "CERTIFIED_PREVIOUSLY_9148",
            "numeric_standard_family_recovery_clock": "CERTIFIED_PREVIOUSLY",
            "N_open_effectivity_gap": "CERTIFIED",
            "numeric_N_open": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate34_round43_nopen_effectivity_frontier_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print("N_OPEN_EFFECTIVITY_GAP:", result["strict_nonpromotion"]["N_open_effectivity_gap"])
    print("NUMERIC_N_OPEN: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
