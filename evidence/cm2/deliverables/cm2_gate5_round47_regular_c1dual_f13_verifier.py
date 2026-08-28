#!/usr/bin/env python3
"""Fail-closed verifier for Round-47 two-trace C1-dual/F10 seeds."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round47_regular_c1dual_f13_cert as cert


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def independent_piola() -> tuple[int, int, str]:
    vectors = ((Q(2), Q(-3)), (Q(5, 7), Q(11, 13)))
    normals = ((Q(1), Q(4)), (Q(-2), Q(9)))
    rows: list[dict[str, Any]] = []
    matrix_count = 0
    for a in range(-4, 5):
        for b in range(-4, 5):
            for c in range(-4, 5):
                for d in range(-4, 5):
                    if a * d - b * c != 1:
                        continue
                    matrix_count += 1
                    for vx, vy in vectors:
                        for nx, ny in normals:
                            pv = (a * vx + b * vy, c * vx + d * vy)
                            pn = (d * nx - c * ny, -b * nx + a * ny)
                            source = vx * nx + vy * ny
                            pushed = pv[0] * pn[0] + pv[1] * pn[1]
                            if source != pushed:
                                raise RuntimeError("independent Piola")
                            rows.append(
                                {
                                    "matrix": [[str(a), str(b)], [str(c), str(d)]],
                                    "vector": [qstr(vx), qstr(vy)],
                                    "normal_measure": [qstr(nx), qstr(ny)],
                                    "pushed_vector": [qstr(pv[0]), qstr(pv[1])],
                                    "pushed_normal_measure": [qstr(pn[0]), qstr(pn[1])],
                                    "source_flux": qstr(source),
                                    "pushed_flux": qstr(pushed),
                                }
                            )
    body = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return matrix_count, len(rows), hashlib.sha256(body).hexdigest()


def independent_seed_arithmetic() -> list[str]:
    errors: list[str] = []
    x_bound = Q(5621, 760)
    dx_bound = Q(28105, 608)
    if not x_bound < 8:
        errors.append("X bound arithmetic")
    if not dx_bound < 47:
        errors.append("DX bound arithmetic")
    if x_bound + dx_bound != Q(163009, 3040):
        errors.append("trace bound arithmetic")
    combined = Q(25, 151) + Q(3816937, 47112000)
    if combined != Q(11616937, 47112000) or not combined < Q(1, 4):
        errors.append("bulk current arithmetic")
    target = Q(103, 151) + Q(192 * 55, 151 * 2**14)
    if target != Q(26533, 38656) or not target < 1:
        errors.append("F10 target arithmetic")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink():
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")

        result = source.get("result", {})
        errors.extend(independent_seed_arithmetic())
        if result.get("provenance", {}).get("parameter_scope") != "base parameter s=0":
            errors.append("parameter scope")
        audit = result.get("exhaustive_small_integer_Piola_audit", {})
        matrices, cases, rows_digest = independent_piola()
        if matrices != 180 or audit.get("SL2_matrix_count") != matrices:
            errors.append("SL2 matrix count")
        if cases != 720 or audit.get("cross_product_case_count") != cases:
            errors.append("Piola case count")
        if audit.get("canonical_case_rows_sha256") != rows_digest:
            errors.append("Piola row digest")
        if audit.get("all_source_and_pushed_fluxes_equal") is not True:
            errors.append("Piola status")

        trace = result.get("finite_regular_path_two_trace_C1dual_F13_sublayer", {})
        if trace.get("C1_dual_embedding_multiplier") != "1":
            errors.append("C1 dual multiplier")
        if trace.get("finite_regular_path_two_trace_C1dual_intertwiner") != "CERTIFIED":
            errors.append("two-trace sublayer")
        if trace.get("complete_Duhamel_bulk_current_included") is not False:
            errors.append("bulk current overclaim")
        if trace.get("same_ID_pointwise_charges") != [
            "c_F13,n<=(3816937/7800000)*c_X,n",
            "c_F13,n<=(3816937/47112000)*c_D1,n",
        ]:
            errors.append("F13 charge")

        f10 = result.get("rank_zero_C24_core_edge_F10_seed", {})
        if f10.get("pointwise_l1_generator_strict_upper") != "5621/760":
            errors.append("F10 X bound")
        if f10.get("Jacobian_l1_column_norm_strict_upper") != "28105/608":
            errors.append("F10 DX bound")
        if f10.get("affine_core_edge_C1_trace_strict_upper") != "163009/3040":
            errors.append("F10 trace bound")
        if f10.get("pure_translation_parameter_derivative") != "partial_s a=0":
            errors.append("F10 parameter derivative")
        target = f10.get("full_face_join_target_not_a_theorem", {})
        if target.get("conditional_D1_ratio") != "26533/38656":
            errors.append("F10 target ratio")
        if target.get("same_measure_arbitrary_Rn_join") != "NOT_CERTIFIED":
            errors.append("F10 join overclaim")

        guard = result.get("bulk_current_and_Piola_nonpromotion_guard", {})
        if guard.get("source_time_C1dual_bound") != (
            "norm(T)_(C1)*<=(c_X+c_F13)*norm(h)_infinity=(11616937/47112000)*c_D1*norm(h)_infinity<(1/4)*c_D1*norm(h)_infinity"
        ):
            errors.append("bulk source bound")
        if guard.get("nonempty_suffix_safe_bound") != (
            "D_suffix*c_X+c_F13, D_suffix=product_i(150*2^B_i)"
        ):
            errors.append("bulk suffix bound")
        if guard.get("C1_gradient_multiplier") != "L":
            errors.append("anisotropic multiplier")
        if guard.get("complete_strong_F13_from_Piola_alone") is not False:
            errors.append("anisotropic nonpromotion")

        frontier = result.get("corrected_strong_frontier", {})
        if frontier.get("complete_return_depth_strong_F13_intertwiner") != "NOT_CERTIFIED":
            errors.append("complete F13 overclaim")
        if frontier.get("complete_all_face_F10") != "NOT_CERTIFIED":
            errors.append("F10 overclaim")
        maturity = result.get("Gate5_maturity_update", {})
        if maturity != {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "reason_no_new_field_credit": "the two-trace C1-dual and affine core-edge F10 seeds do not include the bulk current or the all-face same-measure join",
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        }:
            errors.append("maturity")

        strict = result.get("strict_nonpromotion", {})
        expected = {
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
        }
        if strict != expected:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[str, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "path_scope"), "depth one"),
        (("result", "provenance", "parameter_scope"), "all s"),
        (("result", "exhaustive_small_integer_Piola_audit", "integer_entry_box"), "[-1,1]"),
        (("result", "exhaustive_small_integer_Piola_audit", "SL2_matrix_count"), 179),
        (("result", "exhaustive_small_integer_Piola_audit", "vector_count"), 1),
        (("result", "exhaustive_small_integer_Piola_audit", "normal_measure_count"), 1),
        (("result", "exhaustive_small_integer_Piola_audit", "cross_product_case_count"), 719),
        (("result", "exhaustive_small_integer_Piola_audit", "all_source_and_pushed_fluxes_equal"), False),
        (("result", "exhaustive_small_integer_Piola_audit", "canonical_case_rows_sha256"), "0" * 64),
        (("result", "exhaustive_small_integer_Piola_audit", "full_rows_stored_in_manifest"), True),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "path_scope"), "one face"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "signed_two_trace_boundary_measure"), "unsigned"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "C1_dual_embedding_multiplier"), "2"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "suffix_pushforward_identity"), "false"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "constant_test_cancellation"), "false"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "same_ID_pointwise_charges"), []),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "physical_L6over5_moment"), "NOT_CERTIFIED"),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "complete_Duhamel_bulk_current_included"), True),
        (("result", "finite_regular_path_two_trace_C1dual_F13_sublayer", "finite_regular_path_two_trace_C1dual_intertwiner"), "NOT_CERTIFIED"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "pointwise_l1_generator_strict_upper"), "8"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "Jacobian_l1_column_norm_strict_upper"), "47"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "affine_core_edge_C1_trace_strict_upper"), "55"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "pure_translation_parameter_derivative"), "unknown"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "full_face_join_target_not_a_theorem", "conditional_D1_ratio"), "1"),
        (("result", "rank_zero_C24_core_edge_F10_seed", "full_face_join_target_not_a_theorem", "same_measure_arbitrary_Rn_join"), "CERTIFIED"),
        (("result", "bulk_current_and_Piola_nonpromotion_guard", "source_time_C1dual_bound"), "trace only"),
        (("result", "bulk_current_and_Piola_nonpromotion_guard", "nonempty_suffix_safe_bound"), "c_F13"),
        (("result", "bulk_current_and_Piola_nonpromotion_guard", "C1_gradient_multiplier"), "1"),
        (("result", "bulk_current_and_Piola_nonpromotion_guard", "complete_strong_F13_from_Piola_alone"), True),
        (("result", "corrected_strong_frontier", "complete_return_depth_strong_F13_intertwiner"), "CERTIFIED"),
        (("result", "corrected_strong_frontier", "complete_all_face_F10"), "CERTIFIED"),
        (("result", "Gate5_maturity_update", "new_global_field_completed"), "F14"),
        (("result", "Gate5_maturity_update", "current_global_maturity"), "11/18"),
        (("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("result", "strict_nonpromotion", "complete_return_depth_strong_F13"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "rank_zero_C24_core_edge_F10_seed"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate5_maturity"), "18/18"),
    ]
    mutations: list[tuple[str, str]] = []
    for index, (keys, replacement) in enumerate(changes):
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append((f"mutation-{index}.json", json.dumps(mutation)))
    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append((f"mutation-{len(mutations)}.json", json.dumps(mutation)))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    duplicate = duplicate[:-1] + ',"schema":"duplicate"}'
    mutations.append((f"mutation-{len(mutations)}.json", duplicate))

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for name, body in mutations:
            target = Path(directory) / name
            target.write_text(body, encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
