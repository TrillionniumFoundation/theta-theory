#!/usr/bin/env python3
"""Round-47 two-trace C1-dual and C24 core-edge F10-seed certificate.

Round 44 provided all-face signed two-trace measures in Borel total
variation, and Round 46 provided the Piola-natural F16 flux.  A finite signed
measure embeds in the dual of C1 with constant one.  This certificate freezes
that embedding for the two-trace sublayer on every finite regular path.  It
also freezes a rank-zero affine C24 core-edge normal-flux seed and the
previously only transient 720-case small-integer SL(2) Piola audit.

It does not identify that boundary measure with the complete Duhamel current:
the bulk divergence current still pays a suffix derivative.  Complete strong
F13 and full-face F10 therefore remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round47-regular-c1dual-f13.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate5-round46-piola-f16-frontier-manifest-2026-07-19.json": (
        "ee4a4fd441ff5b63e5607bcd367b04c336a49173d3e7be8ca4b5e1181d3e5a49"
    ),
    "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json": (
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5"
    ),
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": (
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
}

F13_OVER_X = Q(3816937, 7800000)
F13_OVER_D1 = Q(3816937, 47112000)
X_OVER_D1 = Q(25, 151)
FULL_SOURCE_CURRENT_OVER_D1 = Q(11616937, 47112000)
VECTORS = ((Q(2), Q(-3)), (Q(5, 7), Q(11, 13)))
NORMALS = ((Q(1), Q(4)), (Q(-2), Q(9)))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


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
    f13 = load(
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    )["result"]
    if f13["provenance"]["base_parameter"] != "s=0":
        raise RuntimeError("F13 base parameter")
    join = f13["five_face_F13_Borel_join"]
    charge = f13["same_ID_physical_F13_trace_charge"]
    transport = f13["occurrence_suffix_two_trace_transport"]
    if join["all_five_physical_face_grammars_have_a_Borel_F13_payload"] is not True:
        raise RuntimeError("five-face F13")
    if charge["exact_F13_over_X_ratio"] != str(F13_OVER_X):
        raise RuntimeError("F13/X")
    if charge["exact_F13_over_D1_ratio"] != str(F13_OVER_D1):
        raise RuntimeError("F13/D1")
    if transport["status"] != "CERTIFIED_ON_EVERY_FINITE_REGULAR_SUFFIX":
        raise RuntimeError("suffix traces")

    f16 = load(
        "cm2-gate5-round46-piola-f16-frontier-manifest-2026-07-19.json"
    )["result"]
    piola = f16["area_preserving_Piola_flux_identity"]
    if piola["matrix_identity"] != "DS^T cof(DS)=det(DS) I=I":
        raise RuntimeError("Piola identity")
    if f16["all_face_arbitrary_suffix_F16"]["flux_face_operator_cost"] != "CERTIFIED":
        raise RuntimeError("F16")
    if f16["Gate5_maturity_update"]["current_global_maturity"] != "10/18":
        raise RuntimeError("maturity")

    duhamel_result = load(
        "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
    )["result"]
    duhamel = duhamel_result["arbitrary_path_Duhamel_current"]
    if duhamel["identity_status"] != "CERTIFIED_ALGEBRAIC_ARBITRARY_FINITE_PATH":
        raise RuntimeError("Duhamel")
    x_charge = duhamel_result["physical_D1_dominated_eulerian_charge"]
    if x_charge["pointwise_same_ID_identity"] != (
        "c_X,n=(25/151)*c_D1,n<c_D1,n"
    ):
        raise RuntimeError("X/D1")

    occurrence = load(
        "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
    )["result"]["moving_occurrence_seed_F10_L3over2_installation"]
    if occurrence["reverse_raw_seed_cost"] != "<18/5+(4374/125)*2^B<35*2^B":
        raise RuntimeError("reverse occurrence F10")
    if occurrence["forward_raw_seed_cost"] != "<18/5+(8424/125)*2^B<68*2^B":
        raise RuntimeError("forward occurrence F10")
    if occurrence["valid_for_every_rank"] != "integer B>=14":
        raise RuntimeError("F10 rank")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("common carrier")


def det(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def mat_vec(
    matrix: tuple[tuple[Q, Q], tuple[Q, Q]], vector: tuple[Q, Q]
) -> tuple[Q, Q]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def cofactor(
    matrix: tuple[tuple[Q, Q], tuple[Q, Q]]
) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    return (
        (matrix[1][1], -matrix[1][0]),
        (-matrix[0][1], matrix[0][0]),
    )


def dot(left: tuple[Q, Q], right: tuple[Q, Q]) -> Q:
    return left[0] * right[0] + left[1] * right[1]


def exhaustive_piola_rows() -> tuple[int, list[dict[str, Any]]]:
    matrices: list[tuple[tuple[Q, Q], tuple[Q, Q]]] = []
    for a in range(-4, 5):
        for b in range(-4, 5):
            for c in range(-4, 5):
                for d in range(-4, 5):
                    matrix = ((Q(a), Q(b)), (Q(c), Q(d)))
                    if det(matrix) == 1:
                        matrices.append(matrix)
    if len(matrices) != 180:
        raise RuntimeError("SL2 matrix count")

    rows: list[dict[str, Any]] = []
    for matrix in matrices:
        for vector in VECTORS:
            for normal in NORMALS:
                pushed_vector = mat_vec(matrix, vector)
                pushed_normal = mat_vec(cofactor(matrix), normal)
                source_flux = dot(vector, normal)
                pushed_flux = dot(pushed_vector, pushed_normal)
                if source_flux != pushed_flux:
                    raise RuntimeError("Piola sample")
                rows.append(
                    {
                        "matrix": [[qstr(x) for x in row] for row in matrix],
                        "vector": [qstr(x) for x in vector],
                        "normal_measure": [qstr(x) for x in normal],
                        "pushed_vector": [qstr(x) for x in pushed_vector],
                        "pushed_normal_measure": [qstr(x) for x in pushed_normal],
                        "source_flux": qstr(source_flux),
                        "pushed_flux": qstr(pushed_flux),
                    }
                )
    if len(rows) != 720:
        raise RuntimeError("Piola case count")
    return len(matrices), rows


def exhaustive_piola_audit() -> dict[str, Any]:
    matrix_count, rows = exhaustive_piola_rows()
    return {
        "integer_entry_box": "[-4,4]^4",
        "determinant_predicate": "a*d-b*c=1",
        "SL2_matrix_count": matrix_count,
        "vector_count": len(VECTORS),
        "normal_measure_count": len(NORMALS),
        "cross_product_case_count": len(rows),
        "all_source_and_pushed_fluxes_equal": True,
        "canonical_case_rows_sha256": digest(rows),
        "full_rows_stored_in_manifest": False,
        "status": "CERTIFIED_EXHAUSTIVE_SMALL_INTEGER_AUDIT",
    }


def two_trace_c1dual_sublayer() -> dict[str, Any]:
    return {
        "path_scope": "every finite regular arbitrary-R_n path and all five physical face grammars",
        "signed_two_trace_boundary_measure": "B=sigma*(tau_plus-tau_minus), tau_plus,tau_minus positive finite measures",
        "C1_norm_convention": "norm_C1(h)>=norm_infinity(h)",
        "dual_bound": "abs(B(h))<=TV(B)*norm_infinity(h)<=TV(B)*norm_C1(h)",
        "C1_dual_embedding_multiplier": "1",
        "suffix_pushforward_identity": "(S_*B)(h)=B(h composed S)",
        "finite_measure_bound": "norm_(C1)*(S_*B)<=TV(S_*B)<=TV(B)",
        "constant_test_cancellation": "B(1)=0 is preserved by every suffix pushforward",
        "same_ID_pointwise_charges": [
            "c_F13,n<=(3816937/7800000)*c_X,n",
            "c_F13,n<=(3816937/47112000)*c_D1,n",
        ],
        "physical_L6over5_moment": "CERTIFIED_BY_EXISTING_SAME_ID_D1_DOMINATION",
        "complete_Duhamel_bulk_current_included": False,
        "finite_regular_path_two_trace_C1dual_intertwiner": "CERTIFIED",
        "status": "CERTIFIED_TWO_TRACE_C1DUAL_SUBLAYER_ONLY",
    }


def core_edge_f10_seed() -> dict[str, Any]:
    x_bound = Q(5621, 760)
    dx_bound = Q(28105, 608)
    trace_bound = x_bound + dx_bound
    target = Q(103, 151) + Q(192 * 55, 151 * 2**14)
    assert x_bound < 8
    assert dx_bound < 47
    assert trace_bound == Q(163009, 3040) < 55
    assert target == Q(26533, 38656) < 1
    return {
        "coordinates": "collision arclength/area coordinates (r=R*theta,p=sin(phi))",
        "translation_label": "eta in {-1,0,1}",
        "Eulerian_generator": {
            "X_r": "eta*(sin(theta)-(p/c)*cos(theta))",
            "X_p": "(eta/R)*(c*sin(theta)-p*cos(theta))",
            "c": "sqrt(1-p^2)",
            "divergence": "0",
        },
        "C24_output_edge_domain": ["abs(p)<=1/50", "c>19/20", "R>=4/25"],
        "pointwise_l1_generator_strict_upper": qstr(x_bound),
        "Jacobian_l1_column_norm_strict_upper": qstr(dx_bound),
        "affine_core_edge_normal_flux_density": "a=X dot n",
        "affine_core_edge_C1_trace_strict_upper": qstr(trace_bound),
        "pure_translation_parameter_derivative": "partial_s a=0",
        "certified_face_scope": "intermediate/terminal affine C24 core edges only",
        "status": "CERTIFIED_RANK_ZERO_C24_CORE_EDGE_F10_SEED",
        "full_face_join_target_not_a_theorem": {
            "occurrence_bidirectional_raw_cost": "(35+68)*sum_i 2^B_i=103*sum_i 2^B_i",
            "oriented_core_trace_count": 192,
            "rank_floor": "B>=14",
            "conditional_D1_ratio": qstr(target),
            "formula": "103/151+(192*55)/(151*2^14)=26533/38656<1",
            "same_measure_arbitrary_Rn_join": "NOT_CERTIFIED",
        },
    }


def bulk_and_anisotropic_nonpromotion_guard() -> dict[str, Any]:
    assert X_OVER_D1 + F13_OVER_D1 == FULL_SOURCE_CURRENT_OVER_D1
    assert FULL_SOURCE_CURRENT_OVER_D1 < Q(1, 4)
    return {
        "complete_source_current": "T=-div(K)+B with K=X*(P_j h)*mu and B the signed two-trace boundary measure",
        "source_time_C1dual_bound": (
            "norm(T)_(C1)*<=(c_X+c_F13)*norm(h)_infinity=(11616937/47112000)*c_D1*norm(h)_infinity<(1/4)*c_D1*norm(h)_infinity"
        ),
        "nonempty_suffix_safe_bound": "D_suffix*c_X+c_F13, D_suffix=product_i(150*2^B_i)",
        "Piola_cancels_only": "normal flux boundary factor; not the bulk/tangential C1 pullback",
        "matrix_family": "A_L=diag(L,L^(-1)), L>1",
        "determinant": "1",
        "Piola_flux_multiplier": "1",
        "test": "h(y)=y_1 on a local chart",
        "pullback": "h composed A_L=L*x_1",
        "C1_gradient_multiplier": "L",
        "logical_conclusion": (
            "area preservation and normal-flux invariance alone do not bound tangential density variation, the bulk divergence current, or the source-strong-space to trace restriction"
        ),
        "complete_strong_F13_from_Piola_alone": False,
        "status": "CERTIFIED_EXACT_LINEAR_COUNTERMODEL",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base parameter s=0",
            "path_scope": "every finite regular arbitrary-R_n path",
            "claim_type": (
                "finite-regular-path two-trace C1-dual sublayer, C24 core-edge F10 seed, and frozen exhaustive small-integer Piola audit"
            ),
        },
        "exhaustive_small_integer_Piola_audit": exhaustive_piola_audit(),
        "finite_regular_path_two_trace_C1dual_F13_sublayer": two_trace_c1dual_sublayer(),
        "rank_zero_C24_core_edge_F10_seed": core_edge_f10_seed(),
        "bulk_current_and_Piola_nonpromotion_guard": (
            bulk_and_anisotropic_nonpromotion_guard()
        ),
        "corrected_strong_frontier": {
            "newly_removed_issue": (
                "on finite regular paths the Borel two-trace boundary measure embeds in (C1)* with constant one; affine C24 core-edge flux has a rank-zero C1 seed"
            ),
            "complete_return_depth_strong_F13_intertwiner": "NOT_CERTIFIED",
            "remaining_inputs": [
                "F17-type dynamic-test control or a joint insertion/suffix rank tail for the bulk current",
                "numeric q-weighted summation over unbounded return depth",
                "common branch-record convergence needed by dynamic MT_DQ",
                "strong cemetery domination on singular/corner/atlas-failure labels",
                "same-measure arbitrary-R_n join of moving occurrence and all-face F10 traces",
            ],
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "reason_no_new_field_credit": "the two-trace C1-dual and affine core-edge F10 seeds do not include the bulk current or the all-face same-measure join",
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "finite_regular_path_two_trace_C1dual_F13_sublayer": "CERTIFIED",
            "rank_zero_C24_core_edge_F10_seed": "CERTIFIED",
            "exhaustive_720_case_Piola_audit": "CERTIFIED",
            "complete_return_depth_strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
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
        default=HERE / "cm2_gate5_round47_regular_c1dual_f13_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "FINITE_REGULAR_PATH_TWO_TRACE_C1DUAL_F13_SUBLAYER:",
        result["strict_nonpromotion"]["finite_regular_path_two_trace_C1dual_F13_sublayer"],
    )
    print("RANK_ZERO_C24_CORE_EDGE_F10_SEED: CERTIFIED")
    print("COMPLETE_RETURN_DEPTH_STRONG_F13: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
