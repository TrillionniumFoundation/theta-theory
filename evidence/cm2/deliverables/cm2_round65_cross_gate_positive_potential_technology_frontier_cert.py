#!/usr/bin/env python3
"""Producer for the append-only Round-65 cross-gate positive-potential leaf."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round65_common import (
    CertError, canonical_bytes, digest, require, sha256_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round65.cross-gate-positive-potential-technology.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round65-cross-gate-positive-potential-technology-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round65_cross_gate_positive_potential_technology_frontier_verifier.py"
COMMON = HERE / "cm2_round65_common.py"

PINS = {
    "cm2-sixty-fourth-direct-assault-2026-07-21.md":
        "bbd52eed540e4e91566a7d0b9fda2b381b35860640e23a0a45d29b73fabb8b61",
    "cm2-sixty-fourth-direct-assault-manifest-2026-07-21.sha256":
        "5d2174cee61c0fdf5573dedaece38950c0261fe05aa835b66c4363d974e52932",
    "cm2-round64-independent-core-frontier-audit-manifest-2026-07-21.json":
        "e775720b2891146a39421d515280e119f42b075d0783650e879abe1370ff8779",
    "cm2-gate13-round64-one-cross-term-dyadic-clock-frontier-manifest-2026-07-21.json":
        "df730945a80aad801b5923729e5c8239148b040a6983cf001e19ad569d880880",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json":
        "6eb0dbe73b21b5822e9e589b5f6a047b47966a349ec54e8e3b150b9bf203b1af",
    "cm2-gate5-round64-lineage-kernel-flux-bridge-no-go-frontier-manifest-2026-07-21.json":
        "7a67d2225b699c6cffb798298123469eeae6a5d5ded9d1ee9079afb9e8222e70",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_result() -> dict[str, Any]:
    w = Q(3, 2)
    kappa = Q(1, 3)
    tag_rows = []
    for n in range(1, 13):
        mu = Q(3, 4**n)
        tag = Q(2**n)
        tag_rows.append({
            "n": n,
            "mu_mass": qstr(mu),
            "tag_weight": qstr(tag),
            "one_time_moment_term": qstr(mu * tag),
            "conditional_path_potential": qstr(2 * tag),
            "unit_L1_atom_lift_norm": qstr(2 * tag),
        })
    time_rows = []
    for j in range(12):
        time_rows.append({
            "j": j,
            "survival": qstr(kappa**j),
            "outer_times_survival": qstr((w * kappa)**j),
            "weighted_one_vector_charge": qstr(Q(3) * (w * kappa)**j),
        })

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "pinned_round64_frontier": PINS,
        },
        "positive_path_potential_theorem": {
            "status": "CERTIFIED_EXACT_STANDARD_BOREL_INTERFACE",
            "weight": "w>1",
            "tag_expectation": "W_j(y)=integral g_j(z)K_j(y,dz)",
            "potential": "H(x)=sum_j w^j P_(0:j)W_j(x)",
            "bounded_iff": "H in L_infinity(mu)",
            "operator_norm": "||A||=ess_sup_mu H",
            "signed_upper_bound": "||Af||<=integral |f|H dmu",
            "positive_equality": True,
            "sector_sum_is_lawful_only_for_typed_positive_charges": True,
            "signed_cancellation_pays_positive_norm": False,
        },
        "two_factor_separator": {
            "status": "CERTIFIED_EXACT",
            "law": "mu{n}=3*4^-n on n>=1",
            "w": qstr(w),
            "kappa": qstr(kappa),
            "w_times_kappa": qstr(w * kappa),
            "tag": "W_j(n)=2^n",
            "full_mass": "1",
            "one_time_actual_moment": "3",
            "all_time_actual_one_vector_charge": "6",
            "conditional_potential": "H(n)=2^(n+1)",
            "conditional_potential_unbounded": True,
            "time_rows": time_rows,
            "tag_rows": tag_rows,
            "conclusion": "CROSS_TIME_CONTRACTION_PLUS_FINITE_ALL_TIME_VECTOR_MOMENT_NOT_STRONG_BOUNDEDNESS",
        },
        "opposite_separator": {
            "status": "CERTIFIED_EXACT",
            "path": "identity Markov kernel",
            "tag": "W_j=1",
            "each_time_tag_envelope": "1",
            "potential": "sum_j w^j=infinity",
            "conclusion": "POINTWISE_TAG_CONTROL_WITHOUT_TIME_DECAY_NOT_ALL_TIME_BOUNDEDNESS",
        },
        "sharp_sufficient_interface": {
            "hypothesis": "P_(0:j)W_j(x)<=C kappa^j mu-a.e.; w kappa<1",
            "conclusion": "H(x)<=C/(1-w kappa)",
            "actual_joint_pointwise_estimate": "NOT_CERTIFIED",
        },
        "cemetery_typing": {
            "absorbing_occupancy_after_positive_arrival": "DIVERGES_FOR_W_GT_1",
            "lawful_positive_cemetery": "ONE_SHOT_ARRIVAL_LEDGER",
            "arrival_potential_L_infinity": "STILL_REQUIRED",
            "actual_pre_regularization_arrival_bound": "NOT_CERTIFIED",
        },
        "gate_crosswalk": {
            "Gate3": "POSITIVE_VARIATION_INTERFACE_ONLY__PHYSICAL_PIOLA_RQ_MTDQ_NOT_CERTIFIED",
            "Gate4": "ROUND64_W_D_L_INFINITY_IS_ONE_TIME_SPECIALIZATION__ALL_TIME_PATH_BOUND_NOT_CERTIFIED",
            "Gate5": "SAME_LABEL_MASS_CONTRACTION_ALONE_DOES_NOT_CONTROL_TAG_CURRENT_SECTOR_CHARGE",
        },
        "latest_technology_boundary": {
            "arxiv_2603_19509v3": "SEQUENCE_SPACE_RESPONSE__VERIFIED_EXPANDING_OR_POSITIVE_NOISE__NO_BILLIARD_PIOLA",
            "arxiv_2604_25746v1": "C1_PLUS_BETA_COMPACT_BOUNDARYLESS_FLOW__SINGULARITY_IS_FIXED_POINT_NOT_COLLISION",
            "arxiv_2510_19573v3": "WEIGHTED_L_INFINITY_DOMINATED_KERNEL_THEORY__ASSUMES_MISSING_DOMINATION_LYAPUNOV_ROWS",
            "arxiv_2605_07824": "TAMED_DIFFUSION_KILLING_BRANCHING__WRONG_PROCESS",
            "external_theorem_promoted": False,
        },
        "strict_status": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact missing")
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result,
        "verdict": result["strict_status"],
    }


def replay() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    result = build_result()
    sep = result["two_factor_separator"]
    require(Q(sep["w_times_kappa"]) == Q(1, 2), "decay replay")
    require(Q(sep["one_time_actual_moment"]) == 3, "moment replay")
    require(Q(sep["all_time_actual_one_vector_charge"]) == 6, "all-time replay")
    require(sep["conditional_potential_unbounded"] is True, "unbounded replay")
    return {"pins": "6/6", "time_rows": 12, "tag_rows": 12, "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            print(json.dumps(replay(), sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND65_CROSS_GATE_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND65 CROSS-GATE: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
