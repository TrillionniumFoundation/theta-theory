#!/usr/bin/env python3
"""Round-38 F10 analytic-margin exponent frontier.

The existing one-step physical boundary-tube theorem is linear in the actual
tube width h.  This certificate derives the exact dyadic integrability
criterion: a margin tail of exponent alpha and an F10 blow-up exponent r
give an L^p bound only when r*p<alpha.  It also gives a sharp probability
model with a linear tube law and pointwise finite inverse-margin F10, but an
infinite L1 sum at the critical exponent.

The model is a logical sharpness witness, not a billiard face law.  The
physical arbitrary-R_n blow-up exponent and same-ID shell ledger remain to
be certified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round38-f10-margin-exponent-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round38-f10-margin-exponent-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json": (
        "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73"
    ),
    "cm2-gate5-round37-f10-summability-obstruction-manifest-2026-07-19.json": (
        "80109b172504e6ca2a406b49e992dca54ba5204c055e9511639e96520ca58e09"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
}


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
    boundary = load(
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    )["result"]
    tube = boundary["fair_dyadic_boundary_tube_theorem"]
    if tube["uniform_parameter_averaged_normalized_collision_SRB_bound"] != (
        "mu(U_d)<(50/39)h_d for every fair frontier with d>=24"
    ):
        raise RuntimeError("tube law")
    if tube["fair_depth_scale"] if "fair_depth_scale" in tube else None:
        raise RuntimeError("unexpected nested field")
    budget = boundary["dependency_neutral_derivative_budget"]
    if budget["fair_depth_scale"] != "h_d=2^(-floor(d/3))":
        raise RuntimeError("depth scale")
    if boundary["strict_nonpromotion"]["arbitrary_n_Rn_Qn_partition"] != "NOT_CERTIFIED":
        raise RuntimeError("tube scope")

    compact = load(
        "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"
    )["result"]
    search = compact["canonical_dyadic_radius_and_F10_search"]
    if search["canonical_finite_integer_F10_value_exists_for_each_germ"] is not True:
        raise RuntimeError("pointwise F10")
    if search["uniform_radius_or_integer_over_all_germs"] != "NOT_ASSERTED":
        raise RuntimeError("F10 uniform scope")

    old = load(
        "cm2-gate5-round37-f10-summability-obstruction-manifest-2026-07-19.json"
    )["result"]
    if old["strict_nonpromotion"]["complete_global_F10_field"] != "NOT_CERTIFIED":
        raise RuntimeError("global F10 scope")

    rank = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if rank["strict_nonpromotion"]["D1_rank_sum_is_full_branch_C1_pullback_cost"] is not False:
        raise RuntimeError("rank scope")


def dyadic_integrability_theorem() -> dict[str, Any]:
    return {
        "margin_variable": "eta in (0,1]",
        "physical_tail_hypothesis": "mu{eta<=t}<=C_eta*t^alpha for 0<t<=1",
        "F10_blowup_hypothesis": "N_F10<=A_eta*eta^(-r)",
        "dyadic_shell": "2^(-(k+1))<eta<=2^(-k)",
        "shell_mass_upper": "C_eta*2^(-alpha*k)",
        "shell_F10_p_upper": "A_eta^p*2^(r*p*(k+1))",
        "geometric_series_ratio": "2^(r*p-alpha)",
        "sufficient_and_sharp_strict_condition": "r*p<alpha",
        "one_explicit_Lp_bound": (
            "integral N_F10^p dmu <= A_eta^p*C_eta*2^(r*p)/(1-2^(r*p-alpha))"
        ),
        "critical_or_supercritical_conclusion_from_these_hypotheses_alone": (
            "no finite Lp bound follows when r*p>=alpha"
        ),
        "theorem_status": "CERTIFIED_EXACT_DYADIC_CRITERION",
    }


def critical_linear_countermodel() -> dict[str, Any]:
    rows = []
    for k in range(1, 9):
        rows.append(
            {
                "k": k,
                "shell_mass": qstr(Q(1, 1 << (k + 1))),
                "margin_eta": qstr(Q(1, 1 << k)),
                "finite_F10_integer": 1 << k,
                "L1_contribution": "1/2",
            }
        )
    return {
        "scope": "exact logical sharpness model, not asserted as the billiard F10 law",
        "safe_atom": "mass 1/2, eta=1, N_F10=1",
        "shells": "for k>=1: mass=2^(-(k+1)), eta=2^(-k), N_F10=2^k",
        "total_mass": "1",
        "linear_margin_tail": "mu{eta<=t}<=t for every 0<t<1",
        "pointwise_F10_is_finite": True,
        "critical_exponents": "alpha=1, r=1, p=1",
        "each_shell_L1_contribution": "1/2",
        "first_K_shell_L1_sum": "K/2",
        "global_F10_L1_sum": "infinity",
        "representative_first_eight_shells": rows,
        "linear_tube_tail_alone_implies_inverse_margin_F10_L1": False,
        "physical_CM2_impossibility_claimed": False,
    }


def physical_exponent_budget() -> dict[str, Any]:
    return {
        "available_one_step_tube_width_law": "mu(U_d)<(50/39)*h_d",
        "actual_physical_width": "h_d=2^(-floor(d/3))",
        "physical_margin_exponent_interpretation": "alpha=1 in h, not alpha=1/3",
        "computational_depth_rate": "O(2^(-d/3))",
        "one_step_parameter_averaged_scope_only": True,
        "certified_physical_F10_blowup_exponent_r": None,
        "certified_arbitrary_Rn_margin_tail_exponent_alpha": None,
        "if_one_optimistically_used_alpha_1": (
            "an Lp target requires r<1/p; in particular every p>1 requires r<1"
        ),
        "current_compact_germ_result_supplies_only": (
            "pointwise finite radius and integer, with no quantitative margin-to-F10 power"
        ),
        "current_D1_rank_tail_closes_path_margin_products": False,
        "next_required_certificate": (
            "derive a physical r and arbitrary-Rn alpha on the same face IDs, prove r*p<alpha, and sum rank-path factors"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "exact F10 margin-tail exponent criterion and sharpness frontier",
        },
        "dyadic_margin_integrability_theorem": dyadic_integrability_theorem(),
        "critical_linear_tube_countermodel": critical_linear_countermodel(),
        "physical_F10_exponent_budget": physical_exponent_budget(),
        "strict_nonpromotion": {
            "exact_margin_tail_vs_F10_blowup_criterion": "CERTIFIED",
            "one_step_physical_boundary_tube_tail": "CERTIFIED_PREVIOUSLY",
            "physical_arbitrary_Rn_F10_blowup_exponent": "NOT_CERTIFIED",
            "physical_arbitrary_Rn_margin_tail": "NOT_CERTIFIED",
            "complete_global_F10_field": "NOT_CERTIFIED",
            "return_wide_F12": "NOT_CERTIFIED",
            "moving_current_F13": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
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
        default=HERE / "cm2_gate5_round38_f10_margin_exponent_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "MARGIN_F10_CRITERION:",
        result["strict_nonpromotion"]["exact_margin_tail_vs_F10_blowup_criterion"],
    )
    print("PHYSICAL_ARBITRARY_RN_F10_EXPONENT: NOT_CERTIFIED")
    print("GATE5_MATURITY: 7/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
