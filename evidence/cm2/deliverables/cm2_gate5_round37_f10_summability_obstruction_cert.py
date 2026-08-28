#!/usr/bin/env python3
"""Round-37 exact obstruction from pointwise compact-germ F10 to global F10.

Round 36 proves that every compact regular face germ has a finite canonical
F10 integer.  Countability and pointwise finiteness do not imply that these
integers are integrable against physical face mass.  This certificate gives
an exact analytic affine-germ model with total mass one, perfect F8/F9 data,
and a finite F10 integer on every germ, while the weighted F10 sum diverges.

The model is a logical non-implication, not a physical billiard construction.
It freezes the quantitative input required before F10 can be promoted and
before return-wide F12/F13 and the current/flux operator fields can close.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round37-f10-summability-obstruction.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round37-f10-summability-obstruction-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json": (
        "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73"
    ),
    "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json": (
        "2078787d2f4bb990be8a20570a1ca5722ed7bca5f5ff4e0fbf77408c2ca30b4a"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
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
    search = f10["canonical_dyadic_radius_and_F10_search"]
    if search["canonical_finite_integer_F10_value_exists_for_each_germ"] is not True:
        raise RuntimeError("pointwise F10")
    if search["weighted_sum_of_N_F10_over_faces_or_components"] != "NOT_CERTIFIED":
        raise RuntimeError("global F10 scope")

    old = load(
        "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json"
    )["result"]
    if old["F13_moving_boundary_DQ_obstruction"]["F13_status"] != "NOT_CERTIFIED":
        raise RuntimeError("F13")
    if old["Gate5_R1_candidate_local_maturity"][
        "complete_18_field_R1_operator_block_count"
    ] != 0:
        raise RuntimeError("operator block")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("carrier")
    rank = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if rank["strict_nonpromotion"][
        "D1_rank_sum_is_full_branch_C1_pullback_cost"
    ] is not False:
        raise RuntimeError("rank-path scope")


def exact_countable_countermodel() -> dict[str, Any]:
    representative_rows = []
    for k in range(1, 9):
        mass_denominator = 1 << k
        integer = 1 << k
        representative_rows.append(
            {
                "k": k,
                "physical_face_mass": f"1/{mass_denominator}",
                "constant_coarea_density": f"{2 * integer - 1}/2",
                "canonical_F10_integer": integer,
                "weighted_F10_contribution": "1",
            }
        )
    return {
        "scope": (
            "exact logical nonimplication model; not asserted to be the physical billiard face law"
        ),
        "germ_index": "k=1,2,...",
        "physical_face_mass": "m_k=2^-k",
        "total_mass": "sum_(k>=1)m_k=1",
        "analytic_face_model": "G_k(x,s)=x-(2^k-1/2)s",
        "face_geometry": {
            "F8_transversality": "1",
            "F9_curvature": "0",
            "coarea_density": "rho_k=2^k-1/2",
            "tangential_derivative": "0",
            "parameter_derivative": "0",
        },
        "canonical_strict_F10_integer": "N_k=2^k",
        "reason_integer_is_exact": "2^k-1/2<N_k and no smaller positive integer is strict upper",
        "each_compact_germ_has_finite_F10": True,
        "weighted_term": "m_k*N_k=1",
        "partial_weighted_sum": "sum_(k=1)^K m_k*N_k=K",
        "global_weighted_F10_sum": "infinity",
        "representative_first_eight_rows": representative_rows,
        "pointwise_finite_plus_total_mass_implies_weighted_F10_L1": False,
        "physical_CM2_impossibility_claimed": False,
    }


def required_quantitative_interface() -> dict[str, Any]:
    return {
        "one_sufficient_option_uniform": "sup_g N_F10(g)<infinity",
        "one_sufficient_option_Lp": (
            "N_F10 belongs to physical face L^p for some p>1 on a finite face measure"
        ),
        "one_sufficient_option_shell": (
            "sum_l 2^l*mu_face{2^(l-1)<N_F10<=2^l}<infinity"
        ),
        "one_sufficient_option_geometric": (
            "an explicit summable coupling of analytic margin, incidence rank and physical face mass"
        ),
        "current_D1_rank_sum_controls_N_F10": False,
        "reason_D1_does_not_close": (
            "the existing D1 estimate is additive in one-time incidence ranks and does not dominate arbitrary rank-path derivative products or vanishing analytic margins"
        ),
        "arbitrary_Rn_materialized_F10_rows": 0,
        "weighted_F10_L1_or_Lp_bound": "NOT_CERTIFIED",
    }


def downstream_frontier() -> dict[str, Any]:
    return {
        "F12": (
            "only a candidate-local one-step R1 trace template exists; no return-wide arbitrary-Rn physical sum"
        ),
        "F13": (
            "moving occurrence currents and two traces are not globally joined to arbitrary-Rn same IDs"
        ),
        "dynamic_MT_DQ": "NOT_CERTIFIED",
        "F14_through_F18": "NOT_CERTIFIED",
        "complete_operator_block_count": 0,
        "promotion_order": [
            "prove physical global F10 summability",
            "join return-wide F12 on the same face/restriction IDs",
            "join moving-current F13 and two traces",
            "assemble F14-F18 and the induced coefficient",
        ],
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "exact pointwise-to-global summability nonimplication",
        },
        "countable_analytic_affine_germ_countermodel": exact_countable_countermodel(),
        "required_physical_quantitative_interface": required_quantitative_interface(),
        "downstream_same_ID_current_frontier": downstream_frontier(),
        "strict_nonpromotion": {
            "pointwise_compact_germ_F10_schema": "CERTIFIED_PREVIOUSLY",
            "complete_global_F10_field": "NOT_CERTIFIED",
            "global_rank_path_F10_Lp_or_weighted_sum": "NOT_CERTIFIED",
            "return_wide_F12": "NOT_CERTIFIED",
            "moving_current_F13": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate5_round37_f10_summability_obstruction_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("POINTWISE_COMPACT_GERM_F10: CERTIFIED_PREVIOUSLY")
    print("GLOBAL_WEIGHTED_F10_SUM: NOT_CERTIFIED")
    print("GATE5_MATURITY: 7/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
