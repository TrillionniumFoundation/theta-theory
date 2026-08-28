#!/usr/bin/env python3
"""Round-37 typed correction for the aggregate-Z forcing interface.

Round 36 selected the unnormalised aggregate standard-family route, but its
informal four-term ``J_n`` description mixed three different operator types.
This append-only certificate corrects that typing without modifying any old
artifact.

For a fixed parameter, the frozen closed billiard Growth coefficient already
counts continuity, first-owner, singularity and homogeneity cuts.  Moving
occurrence faces belong to the parameter current/flux block, and the strong
cemetery is a separate absorbing strong charge.  The genuinely repeated extra
restriction in the base survivor recurrence is the C24-complement cut.

The available one-interval core multiplier does not control that complement:
one core interval can leave two survivor intervals.  Exact rational arithmetic
and a constant-density affine-cut countermodel show that neither the existing
one-component contraction nor perfect local F8--F10 regularity yields a
mass-additive physical forcing bound.  The first missing base-Z theorem is
therefore hereditary C24 open Growth, or an equivalent physical tail for
two-sided core splits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round37-typed-forcing-correction.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py": (
        "90b7f7a9c0f02c19a80a9679ff393818318675c378ff4c1f139985ae23f069e1"
    ),
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
    "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json": (
        "41c766d25b007944313db93b389a616d086a7318700a867e13d90aedd159be35"
    ),
    "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json": (
        "3475b2cf6af105b4d229e9683eb2f61433be2e4cefc8f1e8f2318c07762f3dd5"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json": (
        "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73"
    ),
    "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json": (
        "ae6c31fb385070bec1c85463d0d125a504089da6c035c8d34d892a768a6f8c2e"
    ),
    "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json": (
        "f2725815d6f995b8d6055255bd50ba60619f06a7904409177a227ff247a2f659"
    ),
}

A = Q(360134800, 360493663)
R = Q(2000, 1999)
ONE_COMPONENT = A * R
TWO_COMPONENT = A * 2 * R
GENERIC_CHARACTERISTIC = Q(580000, 1999)


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


def dependency_path(name: str) -> Path:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    return path


def load(name: str) -> dict[str, Any]:
    value = json.loads(dependency_path(name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    old = load(
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    )["result"]
    if old["same_ID_new_face_injection_interface"]["decomposition"] != (
        "J_n=J_core,n+J_owner,n+J_occurrence,n+J_cemetery,n"
    ):
        raise RuntimeError("round36 interface")

    numeric = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if numeric["replay_summary"]["vartheta_p"] != qstr(A):
        raise RuntimeError("closed Growth coefficient")

    componentwise = load(
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if componentwise["verdict"]["typed_componentwise_growth_join"] != (
        "CERTIFIED_COMPRESSED"
    ):
        raise RuntimeError("componentwise join")
    source = dependency_path(
        "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py"
    ).read_text(encoding="utf-8")
    if componentwise["certificate_sha256"] != sha(
        dependency_path(
            "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py"
        )
    ):
        raise RuntimeError("componentwise source join")
    if '"every_true_and_homogeneity_cut_counted_once": True' not in source:
        raise RuntimeError("cut-count contract")

    inner = load(
        "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
    )
    if inner["replay_summary"]["source_multiplier_norm_upper"] != qstr(R):
        raise RuntimeError("core ratio")
    if inner["replay_summary"]["restricted_contraction"] != qstr(ONE_COMPONENT):
        raise RuntimeError("one-component contraction")

    characteristic = load(
        "cm2-gate25-all-component-characteristic-frontier-manifest-2026-07-17.json"
    )["result"]
    if characteristic["all_key_all_component_characteristic_registry"][
        "uniform_unnormalized_characteristic_Z_multiplier_upper"
    ] != qstr(GENERIC_CHARACTERISTIC):
        raise RuntimeError("generic characteristic")

    green = load(
        "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json"
    )["result"]
    if green["fixed_core_green_kernel"][
        "fixed_core_unbounded_transport_delay_Green_kernel"
    ] != "CERTIFIED":
        raise RuntimeError("fixed-core Green kernel")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    if f9["strict_nonpromotion"][
        "complete_F9_physical_face_C2_parameterized_atlas"
    ] != "CERTIFIED":
        raise RuntimeError("F9")
    f10 = load(
        "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"
    )["result"]
    if f10["strict_nonpromotion"][
        "compact_regular_germ_F10_finite_search_schema"
    ] != "CERTIFIED":
        raise RuntimeError("F10")

    cemetery = load(
        "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json"
    )["result"]
    if cemetery["strict_nonpromotion"]["quantitative_cemetery_payload"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("cemetery scope")
    induced = load(
        "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json"
    )["result"]
    if induced["strict_nonpromotion"][
        "collision_null_cemetery_mass_is_zero_strong_cemetery_charge"
    ] is not False:
        raise RuntimeError("strong cemetery nonimplication")


def typed_forcing_correction() -> dict[str, Any]:
    return {
        "old_round36_four_term_description": (
            "J_n=J_core,n+J_owner,n+J_occurrence,n+J_cemetery,n"
        ),
        "correction_status": "CERTIFIED_APPEND_ONLY_TYPE_CORRECTION",
        "fixed_s_base_standard_family_recurrence": (
            "Z_(n+1)<=a*Z_n+b*m_n+J_C24,n"
        ),
        "closed_map_coefficient_a": qstr(A),
        "closed_map_terms_already_absorbed_in_a": [
            "true continuity and collision singularity components",
            "first-visible owner partition",
            "homogeneity cuts and their multiplicities",
        ],
        "C24_complement_role": (
            "the repeated characteristic restriction external to the frozen closed-map step"
        ),
        "moving_occurrence_role": (
            "parameter derivative current/flux term belonging to F10,F13,F16, not fixed-s base Z"
        ),
        "strong_cemetery_role": (
            "separate absorbing strong boundary/trace charge; not zero and not absorbed by collision-null mass"
        ),
        "abstract_round36_recurrence_remains_valid_as_bookkeeping": True,
        "round36_decomposition_remains_a_typed_physical_bound": False,
        "old_artifacts_modified": False,
    }


def exact_complement_arithmetic() -> dict[str, Any]:
    if ONE_COMPONENT != Q(720269600000, 720626832337):
        raise RuntimeError("one component exact")
    if TWO_COMPONENT != Q(1440539200000, 720626832337):
        raise RuntimeError("two component exact")
    if not ONE_COMPONENT < 1 or not TWO_COMPONENT > 1:
        raise RuntimeError("contraction signs")
    return {
        "core_interval_density_multiplier": qstr(R),
        "one_retained_interval_then_step_coefficient": qstr(ONE_COMPONENT),
        "one_retained_interval_contraction_margin": qstr(1 - ONE_COMPONENT),
        "one_retained_interval_is_contractive": True,
        "one_core_interval_can_leave_two_complement_components": True,
        "safe_two_complement_component_multiplier": qstr(2 * R),
        "two_complement_components_then_step_coefficient": qstr(TWO_COMPONENT),
        "two_component_excess_over_one": qstr(TWO_COMPONENT - 1),
        "two_complement_component_bound_is_contractive": False,
        "generic_all_key_multiplier": qstr(GENERIC_CHARACTERISTIC),
        "generic_all_key_then_step_coefficient": qstr(A * GENERIC_CHARACTERISTIC),
        "generic_all_key_bound_is_contractive": False,
        "one_component_M_core_theorem_controls_M_C24_complement": False,
    }


def affine_cut_countermodel() -> dict[str, Any]:
    return {
        "scope": (
            "exact standard-family functional nonimplication; not a claim about physical C24 frequency"
        ),
        "family": "one interval W_L=[0,L] with constant density one",
        "old_mass": "m_L=L",
        "old_boundary_functional": "Z_old=m_L/length(W_L)=1",
        "cut": (
            "remove one nonempty central interval using two transverse affine stationary faces"
        ),
        "survivor_components": 2,
        "new_boundary_functional": (
            "Z_new=sum_i mass(W_i)/length(W_i)=1+1=2"
        ),
        "local_face_data": {
            "F8_transversality": "1",
            "F9_curvature": "0",
            "F10_stationary_current_density_and_derivatives": "0",
        },
        "mass_additive_candidate": "Z_new<=Z_old+C*m_L",
        "required_inequality": "1<=C*L",
        "violating_sequence": "L_k=2^-k; for every finite C choose k with C*2^-k<1",
        "uniform_finite_mass_additive_C_exists_from_local_F8_F10": False,
        "physical_CM2_impossibility_claimed": False,
        "conclusion": (
            "local smooth face control alone cannot supply a uniform mass-additive J_C24"
        ),
    }


def corrected_frontier() -> dict[str, Any]:
    return {
        "first_missing_base_Z_input": (
            "hereditary C24-complement open Growth/cone inequality on the same unnormalised physical carrier"
        ),
        "equivalent_escape_routes": [
            "a physical weighted tail for two-sided C24 core splits before normalization",
            "a C24-specific sparse-cut theorem controlling inherited Z rather than only survivor mass",
            "a direct killed strong-operator inequality with coefficient strictly below one",
        ],
        "fixed_core_Green_kernel_scope": (
            "transports already summable fixed-core injections; does not prove hereditary new restrictions summable"
        ),
        "parallel_Gate5_work": (
            "global F10 and F12/F13 remain necessary for parameter current/flux, but cannot close base Z by themselves"
        ),
        "next_priority_corrected_from_round36": (
            "C24 hereditary open Growth first; quantitative global F10 summability in parallel"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "depth_scope": "all finite C24 survivor/return levels",
        },
        "typed_forcing_correction": typed_forcing_correction(),
        "C24_complement_exact_arithmetic": exact_complement_arithmetic(),
        "affine_two_survivor_countermodel": affine_cut_countermodel(),
        "corrected_shortest_frontier": corrected_frontier(),
        "strict_nonpromotion": {
            "physical_mass_additive_J_C24": "NOT_CERTIFIED",
            "hereditary_C24_open_Growth": "NOT_CERTIFIED",
            "physical_aggregate_Z_uniform_or_weighted_bound": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate45_round37_typed_forcing_correction_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("ROUND36_J_DECOMPOSITION: CORRECTED_BY_OPERATOR_TYPE")
    print("HEREDITARY_C24_OPEN_GROWTH: NOT_CERTIFIED")
    print("GATE5_MATURITY: 7/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
