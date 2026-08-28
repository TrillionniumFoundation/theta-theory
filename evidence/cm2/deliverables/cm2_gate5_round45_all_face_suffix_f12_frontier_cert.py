#!/usr/bin/env python3
"""Round-45 all-face arbitrary-suffix F12 certificate.

Round 36 certified unit-speed C2 faces on all five physical grammars and
every finite regular rank path.  Round 44 placed their two traces on the same
arbitrary-Rn suffix IDs.  For a suffix with incidence ranks B_i, the frozen
one-step derivative envelope gives

    D_suffix = product_i (150*2^B_i).

The chain rule therefore bounds the C1 trace pullback by 1+D_suffix, with
identity cost one for an empty suffix.  This fills parameterized F12 on all
five physical face grammars.  The value is finite pathwise but has no global
rank-path moment.

The empty-suffix part of F16 inherits the Round-44 F13 charge.  A precise
rank-shell countermodel shows why the available 3B/2 moment cannot promote
nonempty suffixes to strong F16.  The countermodel is only a logical
nonimplication, not a physical billiard counterexample.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round45-all-face-suffix-f12-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round45-all-face-suffix-f12-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

MINIMUM_RANK = 14
DERIVATIVE_NUMERATOR = 150
F13_OVER_X = Q(3816937, 7800000)
F13_OVER_D1 = Q(3816937, 47112000)


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
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    if carrier["common_forward_reverse_carrier_pair"][
        "actual_parameterized_common_fw_rev_carrier_pair_registry"
    ] != "CERTIFIED":
        raise RuntimeError("common carrier")
    if carrier["provenance"]["depth_scope"] != "every finite n>=1":
        raise RuntimeError("carrier depth")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    if f9["strict_nonpromotion"][
        "complete_F9_physical_face_C2_parameterized_atlas"
    ] != "CERTIFIED":
        raise RuntimeError("F9")
    recurrence = f9["general_base_face_rank_path_recurrence"]
    if recurrence["one_step_envelopes"][0] != "L(B)=150*2^B":
        raise RuntimeError("derivative envelope")
    if len(f9["five_face_kind_matrix"]) != 5:
        raise RuntimeError("five face F9")

    f13 = load(
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    )["result"]
    if not f13["five_face_F13_Borel_join"][
        "all_five_physical_face_grammars_have_a_Borel_F13_payload"
    ]:
        raise RuntimeError("F13 face join")
    charge = f13["same_ID_physical_F13_trace_charge"]
    if charge["exact_F13_over_X_ratio"] != str(F13_OVER_X):
        raise RuntimeError("F13/X")
    if charge["exact_F13_over_D1_ratio"] != str(F13_OVER_D1):
        raise RuntimeError("F13/D1")
    if f13["strict_nonpromotion"]["Gate5_maturity"] != "8/18":
        raise RuntimeError("prior maturity")

    words = load(
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    )["result"]
    schema = words["required_operator_field_schema"]
    if schema["required_fields"][11] != "C1_face_trace_pullback_bound":
        raise RuntimeError("F12 schema")
    if schema["required_fields"][15] != "flux_face_operator_cost":
        raise RuntimeError("F16 schema")


def one_step_derivative(rank: int) -> int:
    if type(rank) is not int or rank < MINIMUM_RANK:
        raise ValueError("rank must be an integer at least 14")
    return DERIVATIVE_NUMERATOR * (1 << rank)


def suffix_c1_bound(ranks: Iterable[int]) -> dict[str, Any]:
    rank_path = tuple(ranks)
    derivative = 1
    for rank in rank_path:
        derivative *= one_step_derivative(rank)
    cost = 1 if not rank_path else 1 + derivative
    return {
        "suffix_rank_path": list(rank_path),
        "suffix_depth": len(rank_path),
        "suffix_D_infinity_strict_upper": str(derivative),
        "C1_trace_pullback_multiplier_strict_upper": str(cost),
        "identity_suffix_exact_cost": not rank_path,
    }


def all_face_f12() -> dict[str, Any]:
    face_kinds = [
        "source_core_clipping_face",
        "intermediate_core_avoidance_preimage_face",
        "terminal_core_preimage_face",
        "collision_singularity_or_owner_change_face",
        "moving_occurrence_face",
    ]
    rows = [
        {
            "kind": kind,
            "unit_speed_face_available": True,
            "arbitrary_regular_suffix_F12": (
                "CERTIFIED_BY_SUFFIX_RANK_PATH_CHAIN_RULE"
            ),
        }
        for kind in face_kinds
    ]
    samples = [
        suffix_c1_bound(()),
        suffix_c1_bound((14,)),
        suffix_c1_bound((14, 15)),
        suffix_c1_bound((14, 16, 18)),
        suffix_c1_bound((20, 14, 17, 15)),
    ]
    return {
        "test_norm": "norm_C1(Phi)=norm_infinity(Phi)+norm_infinity(DPhi)",
        "chain_rule": (
            "norm_C1(Phi composed S on face)<(1+D_suffix)*norm_C1(Phi) for nonempty suffix"
        ),
        "empty_suffix": "identity trace pullback has exact cost 1",
        "one_step_derivative_envelope": "L(B)=150*2^B, B>=14",
        "suffix_derivative": "D_suffix=product_i L(B_i)",
        "face_rows": rows,
        "face_rows_sha256": digest(rows),
        "all_five_physical_face_grammars_covered": True,
        "path_scope": "every finite regular arbitrary-R_n suffix rank path",
        "parameterized_slot_token": (
            "(common-Rn-restriction-id,time_j,face-kind,side-label,suffix-rank-path,F12)"
        ),
        "sample_replays": samples,
        "sample_replays_sha256": digest(samples),
        "global_rank_path_moment_required_for_F12_field": False,
        "status": "CERTIFIED_PARAMETERIZED_ALL_FACE_F12",
    }


def rank_shell_nonimplication() -> dict[str, Any]:
    finite_moment = 127 * (1 << 18)
    if finite_moment != 33292288:
        raise RuntimeError("rank-shell moment")
    return {
        "purpose": (
            "show that the current one-time 3B/2 moment does not imply the derivative-weighted nonempty-suffix F16 moment; this is not a physical billiard counterexample"
        ),
        "law": (
            "for m>=4 let B=4m and P(m)=(127/128)*(1/128)^(m-4)"
        ),
        "probability_sums_to_one": True,
        "finite_available_moment": (
            "E[2^(3B/2)]=127*2^18=33292288<infinity"
        ),
        "finite_available_moment_value": finite_moment,
        "divergent_required_product_moment": "E[2^(2B)]=infinity",
        "same_rank_two-time_model": (
            "one insertion factor 2^B times one nonempty-suffix derivative factor 2^B"
        ),
        "logical_conclusion": (
            "nonempty-suffix strong F16 needs a joint rank tail, a lower effective derivative exponent, or an exact flux/test cancellation"
        ),
    }


def f16_frontier() -> dict[str, Any]:
    return {
        "empty_suffix_subspace": {
            "F12_multiplier": "1",
            "trace_charge_bound": (
                "c_F16,empty<=c_F13,n<=(3816937/7800000)c_X,n"
            ),
            "D1_bound": "c_F16,empty<=(3816937/47112000)c_D1,n",
            "physical_L6over5_moment": "CERTIFIED_BY_F13_DOMINATION",
            "physical_block_tail_exponent": "1/6",
            "status": "CERTIFIED_TERMINAL_EMPTY_SUFFIX_SUBLAYER",
        },
        "nonempty_suffix_pathwise_charge": (
            "c_F16,path=sum_(j,e) TV(trace_(j,e))*(1+D_suffix(j))"
        ),
        "nonempty_suffix_value_finite_on_each_fixed_finite_rank_path": True,
        "nonempty_suffix_global_physical_moment": "NOT_CERTIFIED",
        "all_face_standard_family_strong_F16": "NOT_CERTIFIED",
        "cemetery_compatible_F16": "NOT_CERTIFIED",
        "moment_nonimplication": rank_shell_nonimplication(),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "depth_scope": "every finite regular arbitrary-R_n suffix",
            "claim_type": (
                "all-face parameterized F12 plus terminal empty-suffix F16 sublayer and exact strong-F16 moment frontier"
            ),
        },
        "all_face_arbitrary_suffix_F12": all_face_f12(),
        "F16_frontier": f16_frontier(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "8/18",
            "newly_completed_parameterized_field": (
                "F12 C1_face_trace_pullback_bound"
            ),
            "current_global_maturity": "9/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "all_five_face_arbitrary_suffix_F12": "CERTIFIED",
            "terminal_empty_suffix_F16_sublayer": "CERTIFIED",
            "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
            "nonempty_suffix_strong_F16": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5_maturity": "9/18",
            "complete_18_field_operator_block_count": 0,
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
        default=(
            HERE
            / "cm2_gate5_round45_all_face_suffix_f12_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "ALL_FIVE_FACE_ARBITRARY_SUFFIX_F12:",
        result["strict_nonpromotion"]["all_five_face_arbitrary_suffix_F12"],
    )
    print("GATE5_MATURITY: 9/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
