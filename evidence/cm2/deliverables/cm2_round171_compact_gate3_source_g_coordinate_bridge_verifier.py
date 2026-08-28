#!/usr/bin/env python3
"""Independent verifier for the Round171 source-G coordinate bridge."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


BASE = Path(__file__).resolve().parent
CERTIFICATE = (
    BASE / "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
)
OUTPUT = (
    BASE / "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
)
PRODUCER = BASE / "cm2_round171_compact_gate3_source_g_coordinate_bridge.py"
CERTIFICATE_SCHEMA = "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1"
SCHEMA = (
    "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1"
)
CERTIFIED_STATUS = (
    "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
    "NO_RETURN_KEY_OR_D02_PROMOTION"
)
EXPECTED_PRODUCER_SHA256 = (
    "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75"
)

DEPENDENCIES = {
    "cm2_round162_compact_angular_coordinate_engine.py":
        "f8ec6e2760ff19c6fdd65689ed134cd925b5c382778699e16e0e2f933ae162ed",
    "cm2_round162_compact_angular_coordinate_producer.py":
        "c03761fc21765311f41c65b7cda0da2a975c30071372cbcf613dac31e95af36b",
    "cm2_round162_compact_angular_coordinate_verifier.py":
        "eb97c3cbfea8a69dadfb3b6f264b0f6084841f36a129aa477737be95113f26b6",
    "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json":
        "f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1",
    "cm2_round162_compact_angular_coordinate_infrastructure_"
    "verification_2026_07_25.json":
        "880a8b06af9243314d987493be631e4b3b8c4ff41c49c623ea85f5340e5c6214",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json":
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    "cm2_round169_source_g_return_signature_coverage_survey.py":
        "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9",
    "cm2_round169_source_g_return_signature_coverage_survey_certificate.json":
        "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb",
    "cm2_round169_source_g_return_signature_coverage_survey_verifier.py":
        "ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67",
    "cm2_round169_source_g_return_signature_coverage_survey_verification.json":
        "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f",
}
ALL_PINS = {
    "cm2_round171_compact_gate3_source_g_coordinate_bridge.py":
        EXPECTED_PRODUCER_SHA256,
    **DEPENDENCIES,
}
Q = Fraction
CHART_ORDER = ("E", "N", "W", "S")
CHART_SIGN = {"E": 1, "N": -1, "W": -1, "S": 1}
SEAMS = (
    ("E", 1, "N", -1),
    ("N", 1, "W", -1),
    ("W", 1, "S", -1),
    ("S", 1, "E", -1),
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def demand(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_decode(raw: bytes) -> dict[str, Any]:
    demand(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "raw encoding",
    )

    def duplicate_free(
        pairs: list[tuple[str, Any]]
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            demand(key not in result, "duplicate key")
            result[key] = value
        return result

    def no_special_number(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=duplicate_free,
        parse_constant=no_special_number,
        parse_float=no_special_number,
    )

    def walk(item: Any) -> None:
        if type(item) is str:
            demand(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                walk(child)
        elif type(item) is dict:
            for key, child in item.items():
                walk(key)
                walk(child)

    walk(value)
    demand(type(value) is dict, "top object")
    return value


def safe_input(path: Path) -> None:
    demand(path.exists(), "missing input")
    demand(not path.is_symlink(), "input symlink")
    info = path.stat()
    demand(stat.S_ISREG(info.st_mode), "input not regular")
    demand(info.st_nlink == 1, "input hardlink")
    demand(not path.parent.is_symlink(), "input parent symlink")


def safe_output(path: Path, protected: list[Path]) -> None:
    parent = path.parent
    demand(parent.exists() and parent.is_dir(), "output parent")
    demand(not parent.is_symlink(), "output parent symlink")
    resolved = path.resolve(strict=False)
    protected_resolved = [item.resolve(strict=False) for item in protected]
    demand(resolved not in protected_resolved, "output protected")
    if path.exists() or path.is_symlink():
        demand(not path.is_symlink(), "output symlink")
        info = path.stat()
        demand(stat.S_ISREG(info.st_mode), "output not regular")
        demand(info.st_nlink == 1, "output hardlink")
        for item in protected:
            if item.exists():
                demand(not os.path.samefile(path, item), "output alias")


def load(path: Path) -> dict[str, Any]:
    safe_input(path)
    return strict_decode(path.read_bytes())


def wrapped(
    document: dict[str, Any],
    schema: str,
    result_sha256: str,
    status: str,
) -> dict[str, Any]:
    demand(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    demand(document["schema"] == schema, f"schema:{schema}")
    demand(
        document["result_sha256"] == result_sha256
        == digest(document["result"]),
        f"digest:{schema}",
    )
    demand(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def upstream() -> dict[str, Any]:
    for name, expected in ALL_PINS.items():
        path = BASE / name
        safe_input(path)
        demand(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    compact = load(
        BASE
        / "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json"
    )
    compact_v = load(
        BASE
        / (
            "cm2_round162_compact_angular_coordinate_infrastructure_"
            "verification_2026_07_25.json"
        )
    )
    atlas = load(
        BASE / "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
    )
    r169 = load(
        BASE
        / "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
    )
    r169v = load(
        BASE
        / "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
    )
    compact_result = wrapped(
        compact,
        "cm2.round162.compact-angular-coordinate-infrastructure.v1",
        "7a8d34caeae05f9964e4805d4c22123a53ca02b12351d26c18d4ef4b2208de75",
        "CERTIFIED_COMPACT_ANGULAR_COORDINATE_INFRASTRUCTURE__"
        "D02_STILL_BLOCKED",
    )
    compact_verification = wrapped(
        compact_v,
        "cm2.round162.compact-angular-coordinate-infrastructure.verification.v1",
        "9cddfe7303fac71fb1cbfa48691fb21ecaf031f78aa4ec5fa1bfbb6266937e4e",
        "PASS",
    )
    r169_result = wrapped(
        r169,
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6",
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    r169_verification = wrapped(
        r169v,
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1",
        "PASS",
    )
    demand(
        compact_verification["certificate_result_sha256"]
        == "7a8d34caeae05f9964e4805d4c22123a53ca02b12351d26c18d4ef4b2208de75"
        and r169_verification["certificate_result_sha256"]
        == "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6"
        and r169_verification["full_document_exactly_matched"] is True
        and r169_verification["producer_imported_or_executed"] is False,
        "verification bindings",
    )
    demand(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["domain"] == {
            "t": ["-177/250", "177/250"],
            "p": ["-1", "1"],
            "s": ["-1/400", "1/400"],
        }
        and atlas["coverage"]["every_leaf_spans_full_s_window"] is True
        and atlas["coverage"]["global_leaf_count"] == 143248,
        "atlas",
    )
    return {
        "compact": compact_result,
        "atlas": atlas,
        "round169": r169_result,
    }


def normal_from_axis(axis: tuple[int, int]) -> list[list[int]]:
    ex, ey = axis
    jx, jy = -ey, ex
    return [
        [ex, 2 * jx, -ex],
        [ey, 2 * jy, -ey],
    ]


def chart_axes() -> dict[str, tuple[int, int]]:
    return {
        "E": (1, 0),
        "N": (0, 1),
        "W": (-1, 0),
        "S": (0, -1),
    }


def expected_gate3_normal(chart: str) -> list[list[int]]:
    sign = CHART_SIGN[chart]
    radial = [1, 0, -1]
    tangent = [0, 2 * sign, 0]
    return {
        "E": [radial, tangent],
        "N": [tangent, radial],
        "W": [[-entry for entry in radial], tangent],
        "S": [tangent, [-entry for entry in radial]],
    }[chart]


def turn(rows: list[list[int]]) -> list[list[int]]:
    return [[-entry for entry in rows[1]], list(rows[0])]


def velocity_coefficients(
    rows: list[list[int]],
) -> list[list[list[int]]]:
    rotated = turn(rows)
    return [
        [
            list(rows[component]),
            [2 * entry for entry in rotated[component]],
            [-entry for entry in rows[component]],
        ]
        for component in range(2)
    ]


def scaled(rows: list[list[int]]) -> list[list[str]]:
    return [
        [str(Q(9, 25) * entry) for entry in row]
        for row in rows
    ]


def convolution(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return output


def subtract(left: list[int], right: list[int]) -> list[int]:
    width = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else 0)
        - (right[index] if index < len(right) else 0)
        for index in range(width)
    ]


QK = tuple[Q, Q]


def multiply_qk(left: QK, right: QK) -> QK:
    a, b = left
    c, d = right
    return a * c + b * d, a * d + b * c - 2 * b * d


def power_qk(value: QK, exponent: int) -> QK:
    answer: QK = (Q(1), Q(0))
    for _ in range(exponent):
        answer = multiply_qk(answer, value)
    return answer


def evaluate(coefficients: list[int], sign: int) -> QK:
    variable: QK = (Q(0), Q(sign))
    answer: QK = (Q(0), Q(0))
    for exponent, coefficient in enumerate(coefficients):
        term = power_qk(variable, exponent)
        answer = (
            answer[0] + coefficient * term[0],
            answer[1] + coefficient * term[1],
        )
    return answer


def qk_list(value: QK) -> list[str]:
    return [str(value[0]), str(value[1])]


def census(atlas: dict[str, Any]) -> dict[str, int]:
    rows = [atlas["charts"][f"G:{chart}"] for chart in CHART_ORDER]
    result = {
        "leaf_count": sum(row["leaf_count"] for row in rows),
        "unique_first": sum(row["counts"]["unique_first"] for row in rows),
        "tangency_graph": sum(
            row["counts"]["tangency_graph"] for row in rows
        ),
        "multi_candidate": sum(
            row["counts"]["multi_candidate"] for row in rows
        ),
    }
    demand(
        result == {
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        },
        "source G census",
    )
    return result


def expected_result() -> dict[str, Any]:
    data = upstream()
    compact = data["compact"]["compact_angular_coordinate_infrastructure"]
    atlas = data["atlas"]
    round169 = data["round169"]
    compact_atlas = compact["compact_source_atlas"]
    axes = chart_axes()
    compact_axis_rows = {
        row["chart"]: tuple(row["axis"])
        for row in compact_atlas["charts"]
    }
    demand(compact_axis_rows == axes, "compact axes")
    demand(
        compact["all_four_cyclic_seams_exactly_glued"] is True
        and compact_atlas["source_chart_count"] == 4
        and compact_atlas["state_map"] == {
            "normal":
                "((1-z^2)*e_C+2*z*J*e_C)/(1+z^2)",
            "p": "2*q/(1+q^2)",
            "q": "tan(Phi/2)",
            "radial": "(1-q^2)/(1+q^2)",
            "velocity": "radial*normal+p*J*normal",
            "z": "tan((A-theta_C)/2)",
        }
        and compact_atlas["denominator_positivity"][
            "both_strict_positive_on_closed_chart_domains"
        ] is True
        and compact["kappa_isolation"]["selected_root_in_0_1"] is True
        and compact["kappa_isolation"]["quotient_relation"]
        == "kappa^2=1-2*kappa"
        and compact["source_grazing_ledger"][
            "both_are_physical_boundary_strata"
        ] is True
        and compact["source_grazing_ledger"][
            "neither_is_removed_by_a_coordinate_singularity"
        ] is True,
        "compact infrastructure",
    )
    gap = Q(177, 250) ** 2 - Q(1, 2)
    demand(gap == Q(79, 62500), "cover gap")
    kappa_squared: QK = (Q(1), Q(-2))
    denominator: QK = (Q(2), Q(-2))
    denominator_squared = multiply_qk(denominator, denominator)
    endpoint_residue: QK = (
        8 * kappa_squared[0] - denominator_squared[0],
        8 * kappa_squared[1] - denominator_squared[1],
    )
    demand(endpoint_residue == (Q(0), Q(0)), "endpoint")
    radial_residue = subtract(
        subtract(
            convolution([1, 0, 1], [1, 0, 1]),
            convolution([0, 2], [0, 2]),
        ),
        convolution([1, 0, -1], [1, 0, -1]),
    )
    demand(radial_residue == [0, 0, 0, 0, 0], "radial")

    chart_rows: list[dict[str, Any]] = []
    normals: dict[str, list[list[int]]] = {}
    for chart in CHART_ORDER:
        normal = normal_from_axis(axes[chart])
        normals[chart] = normal
        pinned = expected_gate3_normal(chart)
        demand(normal == pinned, f"normal:{chart}")
        rotated = turn(normal)
        velocity = velocity_coefficients(normal)
        row = atlas["charts"][f"G:{chart}"]
        sign = CHART_SIGN[chart]
        chart_rows.append({
            "compact_chart": chart,
            "gate3_chart_id": f"G:{chart}",
            "coordinate_map": {
                "t": (
                    "2*z/(1+z^2)"
                    if sign == 1
                    else "-2*z/(1+z^2)"
                ),
                "p": "2*q/(1+q^2)",
                "s": "s",
            },
            "normal_denominator": "1+z^2",
            "normal_numerator_coefficients_in_1_z_z2": normal,
            "quarter_turn_normal_numerator_coefficients_in_1_z_z2":
                rotated,
            "velocity_denominator": "(1+z^2)*(1+q^2)",
            "velocity_numerator_coefficients_by_component_q0_q1_q2":
                velocity,
            "source_G_center_coefficients_in_1_s":
                [["0", "0"], ["0", "0"]],
            "source_G_radius": "9/25",
            "position_formula": "center_G+(9/25)*normal",
            "position_denominator": "1+z^2",
            "position_numerator_coefficients_in_1_z_z2": scaled(normal),
            "source_state_partial_s": {
                "position": ["0", "0"],
                "normal": ["0", "0"],
                "velocity": ["0", "0"],
                "p": "0",
            },
            "s_product_role":
                "source-state spectator; retained for target-W center shift "
                "x_W=(2*i+1)/2+s",
            "normal_formula_agrees_exactly": True,
            "quarter_turn_normal_formula_agrees_exactly": True,
            "velocity_formula_agrees_exactly": True,
            "position_formula_agrees_exactly": True,
            "gate3_leaf_count": row["leaf_count"],
            "gate3_counts": row["counts"],
            "gate3_leaf_rows_sha256": row["leaf_rows_sha256"],
            "gate3_provenance": row["provenance"],
            "compact_z_endpoint_map_to_true_t_boundary": {
                "z=-kappa": (
                    "-1/sqrt(2)" if sign == 1 else "1/sqrt(2)"
                ),
                "z=+kappa": (
                    "1/sqrt(2)" if sign == 1 else "-1/sqrt(2)"
                ),
            },
            "compact_q_endpoints_map_to_p_grazing": ["-1", "1"],
        })

    seam_rows: list[dict[str, Any]] = []
    for left, left_sign, right, right_sign in SEAMS:
        left_value = [
            evaluate(row, left_sign) for row in normals[left]
        ]
        right_value = [
            evaluate(row, right_sign) for row in normals[right]
        ]
        demand(left_value == right_value, "seam")
        seam_rows.append({
            "left_face": {
                "chart": left,
                "z": "+kappa" if left_sign == 1 else "-kappa",
            },
            "right_face": {
                "chart": right,
                "z": "+kappa" if right_sign == 1 else "-kappa",
            },
            "common_normal_numerator_in_basis_1_kappa":
                [qk_list(value) for value in left_value],
            "common_denominator_in_basis_1_kappa": qk_list(denominator),
            "normal_glues_exactly": True,
            "quarter_turn_and_velocity_glue_for_every_q": True,
            "source_G_position_glues_exactly": True,
        })

    source_g_census = census(atlas)
    r169_inputs = round169["source_G_existing_inputs"]
    r169_keys = round169["source_G_exact_key_coverage_census"]
    demand(
        r169_inputs["atlas_leaf_count"] == source_g_census["leaf_count"]
        and r169_inputs["atlas_unique_first_leaf_count"]
        == source_g_census["unique_first"]
        and r169_inputs["atlas_tangency_graph_leaf_count"]
        == source_g_census["tangency_graph"]
        and r169_inputs["atlas_multi_candidate_leaf_count"]
        == source_g_census["multi_candidate"]
        and r169_inputs["candidate_exact_key_count"] == 224580
        and r169_keys["global_geometric_exact_key_disposition_count"] == 0
        and r169_keys["keys_without_a_global_geometric_disposition_count"]
        == 224580,
        "Round169 guard",
    )

    return {
        "status": CERTIFIED_STATUS,
        "scope": {
            "source_obstacle": "G",
            "compact_domain":
                "four charts z in [-kappa,kappa], q in [-1,1]",
            "adjoined_parameter_domain": "s in [-1/400,1/400]",
            "gate3_conservative_domain":
                "t in [-177/250,177/250], p in [-1,1], "
                "s in [-1/400,1/400]",
            "coordinate_cover_only": True,
            "source_G_position_rebuilt_independently": True,
            "Round162_source_W_position_templates_reused": False,
            "does_not_classify_gate3_leaves": True,
            "does_not_certify_signed_wall_word_transport": True,
            "does_not_certify_outgoing_chart_transport": True,
            "does_not_add_exact_key_dispositions": True,
            "does_not_exhaust_return_signatures": True,
            "does_not_exhaust_exterior_sheets": True,
        },
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "compact_result_sha256":
                "7a8d34caeae05f9964e4805d4c22123a53ca02b12351d26c18d4ef4b2208de75",
            "compact_verification_result_sha256":
                "9cddfe7303fac71fb1cbfa48691fb21ecaf031f78aa4ec5fa1bfbb6266937e4e",
            "Round169_result_sha256":
                "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6",
            "Round169_verification_result_sha256":
                "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1",
            "Round162_infrastructure_reused_only_for": [
                "kappa isolation and half-angle chart domains",
                "generic normal/radial/velocity formulas",
                "cyclic normal/velocity seams",
                "q=+-1 source-grazing infrastructure",
            ],
            "source_G_center_radius_and_s_role_rebuilt_here": True,
            "gate3_global_leaf_count": 143248,
            "old_artifacts_modified": False,
        },
        "exact_source_G_coordinate_bridge": {
            "chart_rows": chart_rows,
            "chart_rows_sha256": digest(chart_rows),
            "source_G_center": ["0", "0"],
            "source_G_radius": "9/25",
            "source_state_is_exactly_s_independent": True,
            "s_is_retained_as_product_and_target_shift_parameter": True,
            "common_p_map": "p=2*q/(1+q^2)",
            "common_radial_identity":
                "1-p(q)^2=((1-q^2)/(1+q^2))^2",
            "common_t_radial_identity":
                "1-(2z/(1+z^2))^2="
                "((1-z^2)/(1+z^2))^2",
            "t_radial_identity_polynomial_residue_coefficients":
                radial_residue,
            "radial_sign_on_closed_q_domain":
                "(1-q^2)/(1+q^2)>=0",
            "p_map_derivative": "2*(1-q^2)/(1+q^2)^2",
            "p_map_monotone_on_closed_domain": True,
            "p_map_strictly_monotone_on_open_domain": True,
            "t_map_derivative_absolute_value":
                "2*(1-z^2)/(1+z^2)^2",
            "t_map_strictly_monotone_on_each_compact_chart": True,
            "t_map_absolute_endpoint": "1/sqrt(2)",
            "kappa_endpoint_polynomial_residue_in_basis_1_kappa":
                qk_list(endpoint_residue),
            "gate3_rational_t_cover_square_gap": str(gap),
            "gate3_rational_t_cover_strictly_contains_true_chart": True,
            "seam_rows": seam_rows,
            "seam_rows_sha256": digest(seam_rows),
            "all_four_source_G_seams_glue_exactly": True,
            "q_plus_minus_one_are_the_only_source_grazing_strata": True,
            "q_grazing_faces_are_physical_not_coordinate_singularities": True,
        },
        "source_G_coverage_consequence": {
            "every_compact_source_G_point_has_a_gate3_chart_image": True,
            "every_compact_source_G_chart_image_is_covered_by_pinned_gate3_leaves":
                True,
            "compact_image_uses_only_true_dominant_coordinate_subdomains":
                True,
            "gate3_guard_band_reverse_rechart_status":
                "DEFERRED_TO_EXTERIOR_FACE_LEDGER",
            "new_physical_sheet_conclusion_from_guard_bands": "NOT_CLAIMED",
            "source_G_gate3_census": source_g_census,
            "source_G_chart_leaf_row_digests": {
                row["gate3_chart_id"]: row["gate3_leaf_rows_sha256"]
                for row in chart_rows
            },
            "unresolved_leaf_dispositions_added_by_this_bridge": 0,
            "exact_key_dispositions_added_by_this_bridge": 0,
            "reason":
                "the bridge proves coordinate coverage and exact source-state "
                "identity, not owner, wall-word, outgoing-chart or "
                "return-signature geometry",
        },
        "Round169_exact_key_guard": {
            "source_G_candidate_exact_key_envelope_count": 224580,
            "source_G_global_geometric_exact_key_disposition_count": 0,
            "source_G_keys_without_global_geometric_disposition_count": 224580,
            "signed_wall_word_transport_certified_by_Round171": False,
            "outgoing_chart_transport_certified_by_Round171": False,
            "Round169_deficit_is_unchanged": True,
        },
        "strict_nonpromotion": {
            "source_G_global_exact_key_dispositions_complete": False,
            "all_disconnected_exterior_sheets_excluded": False,
            "all_chart_and_grazing_strata_dynamically_typed": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "certify Jx/Jy signed wall-word and outgoing-chart exact-key "
            "transports, then materialize owner/wall-word/outgoing-chart rows "
            "on the 21232 source-G unique-first leaves before refining 45028 "
            "multi-candidate leaves and typing 160 tangency graphs plus "
            "grazing/seam/corner strata",
    }


def expected_document() -> dict[str, Any]:
    result = expected_result()
    return {
        "schema": CERTIFICATE_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def validate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    demand(document == expected, "full expected document equality")


def resign(candidate: dict[str, Any]) -> None:
    candidate["result_sha256"] = digest(candidate["result"])


def attacks(expected: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        candidate = copy.deepcopy(expected)
        mutation(candidate["result"])
        resign(candidate)
        cases.append((label, candidate))

    add("status", lambda r: r.__setitem__("status", "CERTIFIED_D02"))
    add("source", lambda r: r["scope"].__setitem__("source_obstacle", "W"))
    add(
        "reuse W position",
        lambda r: r["scope"].__setitem__(
            "Round162_source_W_position_templates_reused", True
        ),
    )
    add(
        "wall transport",
        lambda r: r["scope"].__setitem__(
            "does_not_certify_signed_wall_word_transport", False
        ),
    )
    add(
        "outgoing transport",
        lambda r: r["scope"].__setitem__(
            "does_not_certify_outgoing_chart_transport", False
        ),
    )
    add(
        "exact dispositions",
        lambda r: r["scope"].__setitem__(
            "does_not_add_exact_key_dispositions", False
        ),
    )
    add(
        "source center",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "source_G_center", ["1/2", "1/2"]
        ),
    )
    add(
        "source radius",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "source_G_radius", "4/25"
        ),
    )
    add(
        "s dependence",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "source_state_is_exactly_s_independent", False
        ),
    )
    add(
        "drop s",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "s_is_retained_as_product_and_target_shift_parameter", False
        ),
    )
    add(
        "chart t sign",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][1]
        ["coordinate_map"].__setitem__("t", "2*z/(1+z^2)"),
    )
    add(
        "normal",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][2]
        ["normal_numerator_coefficients_in_1_z_z2"][0].__setitem__(0, 1),
    )
    add(
        "quarter turn",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][0]
        ["quarter_turn_normal_numerator_coefficients_in_1_z_z2"][0]
        .__setitem__(1, -1),
    )
    add(
        "velocity",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][3]
        ["velocity_numerator_coefficients_by_component_q0_q1_q2"][0][1]
        .__setitem__(0, 9),
    )
    add(
        "position",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][0]
        ["position_numerator_coefficients_in_1_z_z2"][0]
        .__setitem__(0, "4/25"),
    )
    add(
        "partial s",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][0]
        ["source_state_partial_s"]["position"].__setitem__(0, "1"),
    )
    add(
        "endpoint",
        lambda r: r["exact_source_G_coordinate_bridge"]["chart_rows"][1]
        ["compact_z_endpoint_map_to_true_t_boundary"]
        .__setitem__("z=-kappa", "-1/sqrt(2)"),
    )
    add(
        "endpoint residue",
        lambda r: r["exact_source_G_coordinate_bridge"]
        ["kappa_endpoint_polynomial_residue_in_basis_1_kappa"]
        .__setitem__(0, "1"),
    )
    add(
        "cover gap",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "gate3_rational_t_cover_square_gap", "0"
        ),
    )
    add(
        "grazing",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "q_grazing_faces_are_physical_not_coordinate_singularities", False
        ),
    )
    add(
        "seam",
        lambda r: r["exact_source_G_coordinate_bridge"]["seam_rows"][0]
        .__setitem__("source_G_position_glues_exactly", False),
    )
    add(
        "seam digest",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "seam_rows_sha256", "0" * 64
        ),
    )
    add(
        "chart digest",
        lambda r: r["exact_source_G_coordinate_bridge"].__setitem__(
            "chart_rows_sha256", "0" * 64
        ),
    )
    add(
        "leaf digest",
        lambda r: r["source_G_coverage_consequence"]
        ["source_G_chart_leaf_row_digests"].__setitem__("G:E", "0" * 64),
    )
    add(
        "census",
        lambda r: r["source_G_coverage_consequence"]["source_G_gate3_census"]
        .__setitem__("multi_candidate", 45027),
    )
    add(
        "invent key disposition",
        lambda r: r["Round169_exact_key_guard"].__setitem__(
            "source_G_global_geometric_exact_key_disposition_count", 1
        ),
    )
    add(
        "signed key promotion",
        lambda r: r["Round169_exact_key_guard"].__setitem__(
            "signed_wall_word_transport_certified_by_Round171", True
        ),
    )
    add(
        "outgoing promotion",
        lambda r: r["Round169_exact_key_guard"].__setitem__(
            "outgoing_chart_transport_certified_by_Round171", True
        ),
    )
    add(
        "D02",
        lambda r: r["strict_nonpromotion"].__setitem__("D02", "CERTIFIED"),
    )
    add("extra key", lambda r: r.__setitem__("forged", True))
    return cases


def strict_json_tests(expected: dict[str, Any]) -> list[str]:
    raw = canonical(expected).encode("utf-8")
    duplicate = raw.replace(
        b'{"result":',
        b'{"schema":"duplicate","result":',
        1,
    )
    vectors = [
        ("duplicate key", duplicate),
        ("float", b'{"x":1.0}'),
        ("NaN", b'{"x":NaN}'),
        ("BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF8", b'{"x":"\xff"}'),
        ("decoded NUL", b'{"x":"\\u0000"}'),
        ("surrogate", b'{"x":"\\ud800"}'),
        ("top array", b"[]"),
        ("trailing", raw + b"{}"),
    ]
    rejected: list[str] = []
    for label, vector in vectors:
        try:
            value = strict_decode(vector)
            validate(value, expected)
        except Exception:
            rejected.append(label)
    demand(len(rejected) == len(vectors), "strict JSON tests")
    return rejected


def path_tests() -> list[str]:
    rejected: list[str] = []

    def expect(label: str, action: Callable[[], None]) -> None:
        try:
            action()
        except Exception:
            rejected.append(label)
        else:
            raise RuntimeError(f"path attack accepted:{label}")

    with tempfile.TemporaryDirectory(prefix="cm2-r171-") as raw_temp:
        temp = Path(raw_temp)
        good_input = temp / "good.json"
        good_input.write_text("{}\n", encoding="utf-8")
        safe_input(good_input)
        expect("missing input", lambda: safe_input(temp / "missing.json"))
        input_link = temp / "input-link.json"
        input_link.symlink_to(good_input)
        expect("input symlink", lambda: safe_input(input_link))
        input_directory = temp / "input-directory"
        input_directory.mkdir()
        expect("input directory", lambda: safe_input(input_directory))
        hard_source = temp / "hard-source.json"
        hard_source.write_text("{}\n", encoding="utf-8")
        hard_input = temp / "hard-input.json"
        os.link(hard_source, hard_input)
        expect("input hardlink", lambda: safe_input(hard_input))

        protected = [good_input, PRODUCER, Path(__file__).resolve()]
        ordinary_output = temp / "ordinary-output.json"
        safe_output(ordinary_output, protected)
        expect(
            "output certificate",
            lambda: safe_output(good_input, protected),
        )
        expect(
            "output producer",
            lambda: safe_output(PRODUCER, protected),
        )
        expect(
            "output verifier",
            lambda: safe_output(Path(__file__).resolve(), protected),
        )
        dependency = BASE / next(iter(DEPENDENCIES))
        expect(
            "output dependency",
            lambda: safe_output(dependency, [*protected, dependency]),
        )
        output_link = temp / "output-link.json"
        output_link.symlink_to(good_input)
        expect(
            "output symlink",
            lambda: safe_output(output_link, protected),
        )
        output_directory = temp / "output-directory"
        output_directory.mkdir()
        expect(
            "output directory",
            lambda: safe_output(output_directory, protected),
        )
        output_hard_source = temp / "output-hard-source"
        output_hard_source.write_text("x", encoding="utf-8")
        output_hard = temp / "output-hard"
        os.link(output_hard_source, output_hard)
        expect(
            "output hardlink",
            lambda: safe_output(output_hard, protected),
        )
        real_parent = temp / "real-parent"
        real_parent.mkdir()
        linked_parent = temp / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        expect(
            "output parent symlink",
            lambda: safe_output(linked_parent / "out.json", protected),
        )
        expect(
            "missing output parent",
            lambda: safe_output(temp / "absent" / "out.json", protected),
        )
    demand(len(rejected) == 13, "path test count")
    return rejected


def build_verification(
    certificate: dict[str, Any],
    certificate_path: Path,
) -> dict[str, Any]:
    expected = expected_document()
    validate(certificate, expected)
    semantic_rejections: list[str] = []
    for label, candidate in attacks(expected):
        try:
            validate(candidate, expected)
        except Exception:
            semantic_rejections.append(label)
    demand(len(semantic_rejections) == 30, "semantic attacks")
    json_rejections = strict_json_tests(expected)
    path_rejections = path_tests()
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": certificate["result_sha256"],
        "certificate_sha256":
            hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "producer_sha256": hashlib.sha256(PRODUCER.read_bytes()).hexdigest(),
        "producer_imported_or_executed": False,
        "all_certificate_fields_semantically_reconstructed": True,
        "full_document_exactly_matched": True,
        "Q_kappa_endpoint_identity_independently_reduced": True,
        "four_source_G_chart_state_identities_independently_rebuilt": True,
        "source_G_center_radius_position_independently_rebuilt": True,
        "source_state_exact_s_independence_and_target_shift_role_checked": True,
        "all_four_source_G_seams_independently_reduced_in_Q_kappa": True,
        "Gate3_source_G_66420_leaf_census_independently_rebuilt": True,
        "four_Gate3_leaf_row_digests_rebound": True,
        "Round169_zero_of_224580_exact_key_disposition_guard_rechecked": True,
        "semantic_attack_suite": {
            "all_result_mutations_resigned": True,
            "attack_count": len(semantic_rejections),
            "rejected_count": len(semantic_rejections),
            "all_rejected": True,
            "rejected_attack_names": semantic_rejections,
        },
        "strict_json_attack_suite": {
            "attack_count": len(json_rejections),
            "rejected_count": len(json_rejections),
            "all_rejected": True,
            "rejected_attack_names": json_rejections,
        },
        "path_safety_self_test": {
            "attack_count": len(path_rejections),
            "rejected_count": len(path_rejections),
            "all_rejected": True,
            "rejected_attack_names": path_rejections,
        },
        "strict_nonpromotion_recomputed": True,
    }
    demand(
        result["producer_sha256"] == EXPECTED_PRODUCER_SHA256,
        "producer pin",
    )
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    certificate_path = arguments.certificate.resolve()
    safe_input(certificate_path)
    protected = [
        certificate_path,
        PRODUCER,
        Path(__file__).resolve(),
        *[(BASE / name).resolve() for name in DEPENDENCIES],
    ]
    safe_output(arguments.output, protected)
    document = load(certificate_path)
    verification = build_verification(document, certificate_path)
    arguments.output.write_text(
        json.dumps(
            verification,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print("PASS")
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
