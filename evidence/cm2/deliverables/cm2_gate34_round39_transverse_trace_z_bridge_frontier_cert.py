#!/usr/bin/env python3
"""Round-39 frontier for the projective-order norm to canonical-family Z bridge.

Round 38 supplies a scheduled C24 killed tail in a Demers--Liverani
projective order norm.  The canonical parent-W registry is an unstable,
transverse disintegration.  This certificate isolates the missing typed
operator: a same-ID transverse trace / boundary-Z comparison.

The local model below only proves that the currently recorded stable-leaf
test controls do not by themselves bound a transverse trace.  It is not an
impossibility theorem for an augmented projective cone or for CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round39-transverse-trace-z-bridge-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round39-transverse-trace-z-bridge-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json": (
        "6aab6003fecfb705c924cced3ca5eb0d64012b1bf4db4816a2a9ac7012b2f6bf"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json": (
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
}

SURVIVAL = Q(111718729, 111718750)
WEIGHT = Q(223437479, 223437458)
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
    strong = load(
        "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json"
    )["result"]
    tail = strong["sampled_C24_killed_strong_tail"]
    if tail["explicit_mass_survival_factor_r"] != qstr(SURVIVAL):
        raise RuntimeError("survival rate")
    if tail["weighted_factor_w_times_r"] != qstr(WEIGHTED_SURVIVAL):
        raise RuntimeError("weighted rate")
    if strong["strict_nonpromotion"]["standard_family_Z_or_Growth_tail"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("round38 Z scope")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("common carrier")
    if carrier["strict_nonpromotion"]["complete_numeric_C_fw_C_rev"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("carrier scope")

    parent = load(
        "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
    )["result"]["Q2_parent_W_Borel_registry"]
    if parent["actual_parent_W_registry"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("parent registry")
    if parent["canonical_leaf_equation"] != (
        "fixed s; phi(r)=4r+b; p(r)=sin(4r+b)"
    ):
        raise RuntimeError("parent equation")
    if parent["phase_graph_slope_dphi_dr"] != "4":
        raise RuntimeError("parent slope")
    if parent["inside_certified_invariant_unstable_cone"] is not True:
        raise RuntimeError("parent cone")

    cone = load(
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    )["result"]
    geometry = cone["global_invariant_geometric_cone"]
    if geometry["fixed_geometric_unstable_cone"] != (
        "25/9<V=dphi/dr<4108425/145348<29"
    ):
        raise RuntimeError("global cone")
    if cone["scope_limits"]["proper_family_log_density_bound"] is not False:
        raise RuntimeError("proper family scope")


def canonical_trace_type_audit() -> dict[str, Any]:
    return {
        "projective_object_type": (
            "two-dimensional density tested by stable-curve averages and their transverse comparison"
        ),
        "canonical_parent_W_type": (
            "one-dimensional unstable curve phi(r)=4r+b carrying a conditional density"
        ),
        "parent_W_slope": "4",
        "certified_global_unstable_cone": "25/9<V<4108425/145348",
        "same_ID_parent_registry": "CERTIFIED_PARAMETERIZED",
        "required_operator": (
            "bounded same-ID transverse trace/disintegration into canonical parent-W families"
        ),
        "required_output": (
            "canonical boundary-Z or Growth bound, not an arbitrary representation-dependent Z"
        ),
        "operator_present_in_current_dependency_chain": False,
        "typed_interface_status": "MISSING_EXACTLY_LOCATED",
    }


def stable_test_no_trace_model() -> dict[str, Any]:
    rows = []
    for exponent in (5, 9, 13, 17, 21):
        epsilon = Q(1, 1 << exponent)
        block = (exponent - 1) // 4
        rows.append(
            {
                "epsilon": qstr(epsilon),
                "total_two_dimensional_mass": qstr(2 * epsilon),
                "stable_leaf_full_integral": qstr(epsilon),
                "stable_short_leaf_q14_upper": qstr(Q(1, 1 << (3 * block))),
                "transverse_trace_on_x_equals_zero": "1",
            }
        )
    return {
        "scope": (
            "local logical model for the recorded stable-test interface; not a full cone impossibility theorem"
        ),
        "rectangle": "(-1,1)_x times (-1,1)_y",
        "stable_leaves": "horizontal y=constant segments",
        "straightened_canonical_transversal": "I={x=0}",
        "density": "u_epsilon(x,y)=max(1-|x|/epsilon,0)",
        "stable_segment_integral_bound": "integral_J u_epsilon dx<=min(length(J),2*epsilon)",
        "stable_short_leaf_exponent": "q=1/4",
        "scaled_stable_test_upper": (
            "sup_J length(J)^(-1/4)*integral_J u_epsilon <= (2*epsilon)^(3/4)"
        ),
        "transverse_comparison_of_stable_integrals": "0 because u_epsilon is y-independent",
        "transverse_trace": "u_epsilon restricted to I is identically 1",
        "stable_controls_tend_to_zero_while_trace_stays_one": True,
        "representative_exact_dyadic_rows": rows,
        "conclusion": (
            "the currently recorded stable-test controls alone do not supply the needed transverse trace bound"
        ),
        "augmented_trace_theorem_ruled_out": False,
        "physical_CM2_impossibility_claimed": False,
    }


def bridge_rate_budget() -> dict[str, Any]:
    unweighted_threshold = 1 / SURVIVAL
    weighted_threshold = 1 / WEIGHTED_SURVIVAL
    if WEIGHTED_SURVIVAL != Q(223437479, 223437500):
        raise RuntimeError("weighted arithmetic")
    if unweighted_threshold - 1 != Q(21, 111718729):
        raise RuntimeError("unweighted threshold")
    if weighted_threshold - 1 != Q(21, 223437479):
        raise RuntimeError("weighted threshold")
    return {
        "hypothetical_same_ID_bridge": (
            "Z_can(K_s^k f)<=A_k*||K_s^k f||_* with limsup A_k^(1/k)<=gamma"
        ),
        "projective_rate_r": qstr(SURVIVAL),
        "round38_block_weight_w": qstr(WEIGHT),
        "weighted_projective_rate_wr": qstr(WEIGHTED_SURVIVAL),
        "unweighted_Z_tail_condition": "gamma*r<1",
        "unweighted_gamma_strict_upper": qstr(unweighted_threshold),
        "unweighted_allowed_excess_above_one": qstr(unweighted_threshold - 1),
        "weighted_Green_sum_condition": "gamma*w*r<1",
        "weighted_gamma_strict_upper": qstr(weighted_threshold),
        "weighted_allowed_excess_above_one": qstr(weighted_threshold - 1),
        "fixed_or_polynomial_bridge_loss": (
            "asymptotic root growth 1; compatible with both strict inequalities"
        ),
        "doubling_bridge_loss_gamma_2_unweighted_product": qstr(2 * SURVIVAL),
        "doubling_bridge_loss_gamma_2_weighted_product": qstr(
            2 * WEIGHTED_SURVIVAL
        ),
        "doubling_bridge_loss_is_safe": False,
        "exact_next_rate_target": (
            "construct an augmented trace-Z cone with subexponential loss, or prove full-Q_N C_N*a^N<1 directly"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "typed transverse-trace frontier and exact bridge-rate budget",
        },
        "canonical_parent_W_trace_type_audit": canonical_trace_type_audit(),
        "stable_test_to_transverse_trace_countermodel": stable_test_no_trace_model(),
        "same_ID_Z_bridge_rate_budget": bridge_rate_budget(),
        "strict_nonpromotion": {
            "missing_projective_to_canonical_trace_interface": "CERTIFIED_EXACTLY_LOCATED",
            "same_ID_canonical_parent_W_registry": "CERTIFIED_PREVIOUSLY",
            "scheduled_projective_order_strong_tail": "CERTIFIED_PREVIOUSLY",
            "bounded_canonical_transverse_trace_operator": "NOT_CERTIFIED",
            "canonical_standard_family_Z_tail": "NOT_CERTIFIED",
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
        default=HERE
        / "cm2_gate34_round39_transverse_trace_z_bridge_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "TRANSVERSE_TRACE_INTERFACE:",
        result["strict_nonpromotion"][
            "missing_projective_to_canonical_trace_interface"
        ],
    )
    print("CANONICAL_Z_TAIL: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
