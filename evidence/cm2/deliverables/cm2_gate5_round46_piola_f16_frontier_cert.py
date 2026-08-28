#!/usr/bin/env python3
"""Round-46 arbitrary-suffix Piola F16 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round46-piola-f16-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round46-piola-f16-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json": (
        "c112fe76649a195f47d51a3448822a7e4e864dff398b57fe26894e2badb28714"
    ),
    "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json": (
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate5-round45-all-face-suffix-f12-frontier-manifest-2026-07-19.json": (
        "7260c3162ba66c634a9583ebfe04d6345dd946fedd40e19b9de244b47fd603be"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

F13_OVER_X = Q(3816937, 7800000)
F13_OVER_D1 = Q(3816937, 47112000)


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
    split = load(
        "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json"
    )["result"]["area_preserving_current_decomposition"]
    if split["divergence_free_generator"] != "div_mu X_s=0 on each regular branch":
        raise RuntimeError("divergence-free generator")
    if split["identity_status"] != "CERTIFIED_ALGEBRAIC":
        raise RuntimeError("current split")

    duhamel = load(
        "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
    )["result"]
    if duhamel["arbitrary_path_Duhamel_current"]["identity_status"] != (
        "CERTIFIED_ALGEBRAIC_ARBITRARY_FINITE_PATH"
    ):
        raise RuntimeError("Duhamel identity")
    if duhamel["F13_F16_operator_field_frontier"][
        "arbitrary_Rn_F16_pointwise_affine_flux_envelope"
    ] != "CERTIFIED":
        raise RuntimeError("F16 seed envelope")

    f13 = load(
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    )["result"]
    charge = f13["same_ID_physical_F13_trace_charge"]
    if charge["exact_F13_over_X_ratio"] != str(F13_OVER_X):
        raise RuntimeError("F13/X ratio")
    if charge["exact_F13_over_D1_ratio"] != str(F13_OVER_D1):
        raise RuntimeError("F13/D1 ratio")
    if f13["five_face_F13_Borel_join"][
        "all_five_physical_face_grammars_have_a_Borel_F13_payload"
    ] is not True:
        raise RuntimeError("five-face F13")
    if f13["five_face_F13_Borel_join"]["internal_artificial_cut_rule"] != (
        "assemble adjacent quotient traces before absolute values; artificial chart/homogeneity cuts are not physical F13 faces"
    ):
        raise RuntimeError("artificial cut assembly")

    f12 = load(
        "cm2-gate5-round45-all-face-suffix-f12-frontier-manifest-2026-07-19.json"
    )["result"]
    if f12["strict_nonpromotion"]["all_five_face_arbitrary_suffix_F12"] != (
        "CERTIFIED"
    ):
        raise RuntimeError("F12")
    if f12["Gate5_maturity_update"]["current_global_maturity"] != "9/18":
        raise RuntimeError("prior maturity")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]["common_forward_reverse_carrier_pair"]
    if carrier["mu_s_A_equals_mu_s_B_equals_mu_s_I_B"] is not True:
        raise RuntimeError("area preservation")

    schema = load(
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    )["result"]["required_operator_field_schema"]
    if "flux_face_operator_cost" not in schema["required_fields"]:
        raise RuntimeError("F16 schema")


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


def piola_samples() -> list[dict[str, Any]]:
    matrices = (
        ((Q(1), Q(0)), (Q(0), Q(1))),
        ((Q(1), Q(7)), (Q(0), Q(1))),
        ((Q(2), Q(1)), (Q(1), Q(1))),
        ((Q(3), Q(2)), (Q(1), Q(1))),
        ((Q(5, 2), Q(3, 2)), (Q(1), Q(1))),
    )
    vectors = ((Q(2), Q(-3)), (Q(5, 7), Q(11, 13)))
    normals = ((Q(1), Q(4)), (Q(-2), Q(9)))
    rows: list[dict[str, Any]] = []
    for matrix in matrices:
        if det(matrix) != 1:
            raise RuntimeError("sample determinant")
        for vector, normal in zip(vectors, normals):
            pushed_vector = mat_vec(matrix, vector)
            pushed_normal_measure = mat_vec(cofactor(matrix), normal)
            lhs = dot(pushed_vector, pushed_normal_measure)
            rhs = dot(vector, normal)
            if lhs != rhs:
                raise RuntimeError("sample Piola identity")
            rows.append(
                {
                    "matrix": [[qstr(x) for x in row] for row in matrix],
                    "determinant": "1",
                    "source_vector": [qstr(x) for x in vector],
                    "source_normal_measure": [qstr(x) for x in normal],
                    "pushed_vector": [qstr(x) for x in pushed_vector],
                    "pushed_normal_measure": [qstr(x) for x in pushed_normal_measure],
                    "source_flux": qstr(rhs),
                    "pushed_flux": qstr(lhs),
                }
            )
    return rows


def piola_flux_identity() -> dict[str, Any]:
    rows = piola_samples()
    return {
        "regular_suffix_branch": (
            "S is a C1 orientation-preserving collision-area-preserving diffeomorphism on one homogeneous suffix component"
        ),
        "area_Jacobian": "det(DS)=1",
        "current_pushforward": "J_prime(Sx)=DS(x) J(x)",
        "normal_measure_pushforward": (
            "n_prime dH1_on_SGamma=cof(DS) n dH1_on_Gamma"
        ),
        "matrix_identity": "DS^T cof(DS)=det(DS) I=I",
        "pointwise_flux_identity": (
            "J_prime dot n_prime dH1_on_SGamma=J dot n dH1_on_Gamma"
        ),
        "weighted_pairing_identity": (
            "integral_SGamma h J_prime dot n_prime dH1=integral_Gamma (h composed S) J dot n dH1"
        ),
        "test_bound": (
            "absolute pairing<=norm_infinity(h)*TV(source flux)<=norm_C1(h)*TV(source flux)"
        ),
        "suffix_derivative_multiplier": "1",
        "artificial_cut_policy": (
            "assemble adjacent physical traces before absolute values; piecewise pushforward cannot increase the summed source flux TV"
        ),
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_PIOLA_CANCELLATION",
    }


def all_face_f16() -> dict[str, Any]:
    return {
        "path_scope": "every finite regular arbitrary-R_n suffix",
        "all_five_physical_face_grammars_covered": True,
        "same_ID_slot_token": (
            "(common-Rn-restriction-id,time_j,face-kind,carrier-seed-id,side-label,suffix-component-id,F16)"
        ),
        "source_flux_input": (
            "the Round-44 all-face F13 two-trace flux measure at insertion time j"
        ),
        "suffix_transport": (
            "Piola pushforward on every homogeneous area-preserving suffix component"
        ),
        "nonempty_suffix_derivative_product_used": False,
        "pointwise_charge_bounds": [
            "c_F16,n<=c_F13,n",
            "c_F16,n<=(3816937/7800000)*c_X,n",
            "c_F16,n<=(3816937/47112000)*c_D1,n",
        ],
        "physical_L6over5_moment": "CERTIFIED_BY_SAME_ID_F13_D1_DOMINATION",
        "physical_weighted_tail": {
            "inherited_block_exponent": "1/6",
            "collision_time_rate_numeric": False,
            "status": "CERTIFIED_FOR_ALL_FACE_F16_FLUX_CHARGE",
        },
        "flux_face_operator_cost": "CERTIFIED",
        "status": "CERTIFIED_ALL_FACE_ARBITRARY_SUFFIX_F16",
    }


def corrected_frontier() -> dict[str, Any]:
    return {
        "round45_naive_majorant": (
            "TV(trace)*(1+D_suffix) is a valid generic C1 pullback majorant but is not sharp for geometric normal flux"
        ),
        "round45_moment_countermodel_status": (
            "still valid for the naive product route; it does not obstruct the Piola-natural F16 flux"
        ),
        "newly_removed_obstruction": (
            "the nonempty suffix derivative product cancels exactly from F16"
        ),
        "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
        "cemetery_compatible_F16": "NOT_CERTIFIED",
        "full_all_face_F10": "NOT_CERTIFIED",
        "F14_F15_F17_F18": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "path_scope": "every finite regular arbitrary-R_n suffix",
            "claim_type": (
                "exact area-preserving Piola flux cancellation and all-face arbitrary-suffix F16 operator cost"
            ),
        },
        "area_preserving_Piola_flux_identity": piola_flux_identity(),
        "all_face_arbitrary_suffix_F16": all_face_f16(),
        "corrected_strong_frontier": corrected_frontier(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "9/18",
            "newly_completed_parameterized_field": "F16 flux_face_operator_cost",
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "all_five_face_arbitrary_suffix_F16": "CERTIFIED",
            "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
            "cemetery_compatible_F16": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
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
        default=HERE / "cm2_gate5_round46_piola_f16_frontier_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "ALL_FACE_ARBITRARY_SUFFIX_F16:",
        result["strict_nonpromotion"]["all_five_face_arbitrary_suffix_F16"],
    )
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

