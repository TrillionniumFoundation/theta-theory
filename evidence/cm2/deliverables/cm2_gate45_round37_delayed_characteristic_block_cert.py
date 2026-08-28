#!/usr/bin/env python3
"""Exact delayed-characteristic contraction thresholds for round 37.

The corrected base-Z frontier asks for hereditary C24 open Growth.  This
certificate proves that the frozen closed-map contraction is already strong
enough *scalarwise* if an entire survivor block can be represented by one
characteristic multiplier independent of block depth.  A two-component
multiplier contracts after exactly 697 closed steps; the frozen generic F7
multiplier contracts after exactly 5694 steps.

Neither multiplier is presently certified for the full arbitrary-depth
survivor union.  The arbitrary-n path schema grows as 24*441280^n and has no
uniform characteristic strong bound, while the sparse-hit theorem controls
weak survivor mass with a nonnumeric block length.  The result is therefore a
conditional scalar bridge and an exact target, not a physical gate closure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round37-delayed-characteristic-block.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json": (
        "890a95cb71a19bdb2f32963d5c3812c29d0d3bb9f427076c4bf7cc1b684d4393"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
}

A = Q(360134800, 360493663)
TWO_COMPONENT = Q(4000, 1999)
GENERIC_F7 = Q(580000, 1999)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def integer_digest(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


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
    correction = load(
        "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json"
    )["result"]
    if correction["strict_nonpromotion"]["hereditary_C24_open_Growth"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("corrected frontier")
    numeric = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if numeric["replay_summary"]["vartheta_p"] != qstr(A):
        raise RuntimeError("a")
    f7 = load(
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    )["result"]
    if f7["all_key_all_component_characteristic_registry"][
        "uniform_unnormalized_characteristic_Z_multiplier_upper"
    ] != qstr(GENERIC_F7):
        raise RuntimeError("F7")
    if f7["strict_nonpromotion"][
        "finite_characteristic_bound_implies_hereditary_repeated_recovery"
    ] is not False:
        raise RuntimeError("F7 scope")
    paths = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    universe = paths["C24_full_dimensional_arbitrary_n_candidate_path_join"]
    if universe["depth_n_candidate_universe_size"] != "24*441280^n":
        raise RuntimeError("path universe")
    if paths["strict_nonpromotion"]["finite_complete_Rn_Qn_raw_branch_table"] != (
        "NOT_MATERIALIZED"
    ):
        raise RuntimeError("path scope")
    sparse = load(
        "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
    )["result"]
    hit = sparse["uniform_recovered_cone_hit_gap"]
    if hit["numeric_N_open"] is not None or not hit[
        "combined_sparse_block_length"
    ].startswith("N_open_is_one_uniform_integer"):
        raise RuntimeError("N_open scope")
    scheduled = load(
        "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json"
    )["result"]
    if scheduled["strict_nonpromotion"][
        "abstract_schedule_implies_native_recut_schedule"
    ] is not False:
        raise RuntimeError("scheduled scope")


@lru_cache(maxsize=None)
def least_contraction_block(multiplier: Q) -> tuple[int, Q, Q]:
    lower = 0
    upper = 1
    while multiplier * A**upper >= 1:
        lower = upper
        upper *= 2
    while upper - lower > 1:
        midpoint = (lower + upper) // 2
        if multiplier * A**midpoint >= 1:
            lower = midpoint
        else:
            upper = midpoint
    steps = upper
    coefficient = multiplier * A**steps
    previous = coefficient / A
    if not previous >= 1 > coefficient:
        raise RuntimeError("minimal block")
    return steps, coefficient, previous


def threshold_record(name: str, multiplier: Q, expected: int, upper: Q) -> dict[str, Any]:
    steps, coefficient, previous = least_contraction_block(multiplier)
    if steps != expected or not coefficient < upper < 1:
        raise RuntimeError(f"threshold: {name}")
    weight = (1 + 1 / upper) / 2
    weighted_upper = weight * upper
    if not weight > 1 or not weighted_upper < 1:
        raise RuntimeError(f"weight: {name}")
    witness = {
        "numerator_sha256": integer_digest(coefficient.numerator),
        "denominator_sha256": integer_digest(coefficient.denominator),
        "previous_numerator_sha256": integer_digest(previous.numerator),
        "previous_denominator_sha256": integer_digest(previous.denominator),
    }
    return {
        "route": name,
        "characteristic_multiplier": qstr(multiplier),
        "least_closed_steps_for_inherited_Z_contraction": steps,
        "previous_step_coefficient_is_at_least_one": True,
        "threshold_coefficient_is_below_one": True,
        "threshold_coefficient_rational_witness_sha256": digest(witness),
        "simple_strict_coefficient_upper": qstr(upper),
        "pointwise_resolvent_strict_upper": qstr(1 / (1 - upper)),
        "one_rational_exponential_block_weight": qstr(weight),
        "weighted_coefficient_strict_upper": qstr(weighted_upper),
        "weighted_resolvent_strict_upper": qstr(1 / (1 - weighted_upper)),
        "comparison_replayed_by_exact_integer_arithmetic": True,
    }


def conditional_block_theorem() -> dict[str, Any]:
    return {
        "closed_N_step_Growth": (
            "Z(T_*^N F)<=a^N Z(F)+b*(1-a^N)/(1-a)*mass(F)"
        ),
        "conditional_characteristic_hypothesis": (
            "Z(M_QN G)<=C_N Z(G) on the same unnormalised strong carrier"
        ),
        "conditional_killed_block_bound": (
            "Z(M_QN T_*^N F)<=C_N*a^N Z(F)+C_N*b*(1-a^N)/(1-a)*mass(F)"
        ),
        "conclusion_if_C_N_aN_below_one": (
            "a deterministic pointwise and weighted block Green resolvent follows"
        ),
        "inverse_component_mass_used": False,
        "cellwise_retained_depth_used": False,
        "conditional_scalar_bridge": "CERTIFIED",
    }


def physical_installation_frontier() -> dict[str, Any]:
    return {
        "one_step_two_component_multiplier_scope": (
            "one short curve minus one core interval only; not an N-step survivor union"
        ),
        "generic_F7_multiplier_scope": (
            "one frozen finite return-word key fibre or one maximal component; not the union over arbitrary path words"
        ),
        "arbitrary_depth_candidate_universe": "24*441280^n",
        "uniform_or_subexponential_C_N_for_full_Q_N": "NOT_CERTIFIED",
        "same_strong_carrier_delayed_characteristic_join": "NOT_CERTIFIED",
        "nonnumeric_N_open_compared_to_697_or_5694": False,
        "weak_sparse_hit_tail_is_strong_characteristic_bound": False,
        "native_no_hidden_recut_dwell_schedule": "NOT_CERTIFIED",
        "exact_next_scalar_target": (
            "find one physical N and C_N with full-survivor characteristic multiplier C_N and C_N*a^N<1"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    two = threshold_record(
        "hypothetical_uniform_two-component_survivor_block",
        TWO_COMPONENT,
        697,
        Q(49973, 50000),
    )
    generic = threshold_record(
        "hypothetical_uniform_generic_F7_survivor_block",
        GENERIC_F7,
        5694,
        Q(24983, 25000),
    )
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "exact conditional delayed-characteristic scalar bridge",
        },
        "conditional_delayed_characteristic_theorem": conditional_block_theorem(),
        "two_component_exact_threshold": two,
        "generic_F7_exact_threshold": generic,
        "physical_installation_frontier": physical_installation_frontier(),
        "strict_nonpromotion": {
            "conditional_delayed_characteristic_scalar_bridge": "CERTIFIED",
            "full_QN_uniform_characteristic_multiplier": "NOT_CERTIFIED",
            "physical_killed_strong_block_contraction": "NOT_CERTIFIED",
            "hereditary_C24_open_Growth": "NOT_CERTIFIED",
            "physical_aggregate_Z_uniform_or_weighted_bound": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate45_round37_delayed_characteristic_block_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "TWO_COMPONENT_MIN_BLOCK:",
        result["two_component_exact_threshold"][
            "least_closed_steps_for_inherited_Z_contraction"
        ],
    )
    print(
        "GENERIC_F7_MIN_BLOCK:",
        result["generic_F7_exact_threshold"][
            "least_closed_steps_for_inherited_Z_contraction"
        ],
    )
    print("PHYSICAL_FULL_QN_CHARACTERISTIC: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
