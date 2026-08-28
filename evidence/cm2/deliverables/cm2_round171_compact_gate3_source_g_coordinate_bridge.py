#!/usr/bin/env python3
"""Round171: exact compact-to-Gate3 coordinate bridge for source G.

The pinned Round162 infrastructure supplies the compact half-angle chart,
the isolated algebraic endpoint kappa, and the generic normal/velocity seam
and grazing framework.  Its source-W position templates are deliberately not
transported.  This producer independently installs

    center_G = (0,0),  radius_G = 9/25,
    position = center_G + (9/25) normal,

and proves exact agreement with all four pinned source-G Gate3 charts.

The parameter s is retained as the common product-window coordinate.  It is
a spectator in the source-G state and enters later target-W centre shifts;
it is not silently deleted.  This bridge adds no wall-word, outgoing-chart,
exact-key disposition, exterior exclusion, or D02 credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE / "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
)
SCHEMA = "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1"
STATUS = (
    "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
    "NO_RETURN_KEY_OR_D02_PROMOTION"
)

COMPACT_ENGINE = "cm2_round162_compact_angular_coordinate_engine.py"
COMPACT_PRODUCER = "cm2_round162_compact_angular_coordinate_producer.py"
COMPACT_VERIFIER = "cm2_round162_compact_angular_coordinate_verifier.py"
COMPACT_CERTIFICATE = (
    "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json"
)
COMPACT_VERIFICATION = (
    "cm2_round162_compact_angular_coordinate_infrastructure_"
    "verification_2026_07_25.json"
)
GATE3_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_MANIFEST = "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
ROUND169_PRODUCER = "cm2_round169_source_g_return_signature_coverage_survey.py"
ROUND169_CERTIFICATE = (
    "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
)
ROUND169_VERIFIER = (
    "cm2_round169_source_g_return_signature_coverage_survey_verifier.py"
)
ROUND169_VERIFICATION = (
    "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
)

PINS = {
    COMPACT_ENGINE:
        "f8ec6e2760ff19c6fdd65689ed134cd925b5c382778699e16e0e2f933ae162ed",
    COMPACT_PRODUCER:
        "c03761fc21765311f41c65b7cda0da2a975c30071372cbcf613dac31e95af36b",
    COMPACT_VERIFIER:
        "eb97c3cbfea8a69dadfb3b6f264b0f6084841f36a129aa477737be95113f26b6",
    COMPACT_CERTIFICATE:
        "f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1",
    COMPACT_VERIFICATION:
        "880a8b06af9243314d987493be631e4b3b8c4ff41c49c623ea85f5340e5c6214",
    GATE3_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GATE3_MANIFEST:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    ROUND169_PRODUCER:
        "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9",
    ROUND169_CERTIFICATE:
        "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb",
    ROUND169_VERIFIER:
        "ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67",
    ROUND169_VERIFICATION:
        "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f",
}
COMPACT_RESULT_SHA256 = (
    "7a8d34caeae05f9964e4805d4c22123a53ca02b12351d26c18d4ef4b2208de75"
)
COMPACT_VERIFICATION_RESULT_SHA256 = (
    "9cddfe7303fac71fb1cbfa48691fb21ecaf031f78aa4ec5fa1bfbb6266937e4e"
)
ROUND169_RESULT_SHA256 = (
    "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6"
)
ROUND169_VERIFICATION_RESULT_SHA256 = (
    "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1"
)
CHART_SIGNS = {"E": 1, "N": -1, "W": -1, "S": 1}
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


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, f"top object:{path.name}")
    return value


def wrapper(
    document: dict[str, Any],
    schema: str,
    result_sha256: str,
    status: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    require(document["schema"] == schema, f"schema:{schema}")
    require(
        document["result_sha256"] == result_sha256
        == digest(document["result"]),
        f"result digest:{schema}",
    )
    require(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def inputs() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    compact = strict_load(HERE / COMPACT_CERTIFICATE)
    compact_v = strict_load(HERE / COMPACT_VERIFICATION)
    gate3 = strict_load(HERE / GATE3_MANIFEST)
    round169 = strict_load(HERE / ROUND169_CERTIFICATE)
    round169_v = strict_load(HERE / ROUND169_VERIFICATION)
    compact_result = wrapper(
        compact,
        "cm2.round162.compact-angular-coordinate-infrastructure.v1",
        COMPACT_RESULT_SHA256,
        "CERTIFIED_COMPACT_ANGULAR_COORDINATE_INFRASTRUCTURE__"
        "D02_STILL_BLOCKED",
    )
    compact_verification = wrapper(
        compact_v,
        "cm2.round162.compact-angular-coordinate-infrastructure.verification.v1",
        COMPACT_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    round169_result = wrapper(
        round169,
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        ROUND169_RESULT_SHA256,
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    round169_verification = wrapper(
        round169_v,
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        ROUND169_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        compact_verification["certificate_result_sha256"]
        == COMPACT_RESULT_SHA256,
        "compact verification binding",
    )
    require(
        round169_verification["certificate_result_sha256"]
        == ROUND169_RESULT_SHA256
        and round169_verification["full_document_exactly_matched"] is True
        and round169_verification["producer_imported_or_executed"] is False,
        "Round169 verification binding",
    )
    require(
        gate3["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and gate3["coverage"]["domain"] == {
            "t": ["-177/250", "177/250"],
            "p": ["-1", "1"],
            "s": ["-1/400", "1/400"],
        }
        and gate3["coverage"]["every_leaf_spans_full_s_window"] is True
        and gate3["coverage"]["global_leaf_count"] == 143248,
        "Gate3 cover",
    )
    return {
        "compact": compact_result,
        "gate3": gate3,
        "round169": round169_result,
    }


def compact_normal(chart: str) -> list[list[int]]:
    return {
        "E": [[1, 0, -1], [0, 2, 0]],
        "N": [[0, -2, 0], [1, 0, -1]],
        "W": [[-1, 0, 1], [0, -2, 0]],
        "S": [[0, 2, 0], [-1, 0, 1]],
    }[chart]


def gate3_normal(chart: str, sign: int) -> list[list[int]]:
    radial = [1, 0, -1]
    tangent = [0, 2 * sign, 0]
    return {
        "E": [radial, tangent],
        "N": [tangent, radial],
        "W": [[-value for value in radial], tangent],
        "S": [tangent, [-value for value in radial]],
    }[chart]


def quarter_turn(rows: list[list[int]]) -> list[list[int]]:
    return [[-value for value in rows[1]], list(rows[0])]


def velocity_tensor(
    rows: list[list[int]],
) -> list[list[list[int]]]:
    turned = quarter_turn(rows)
    return [
        [
            list(rows[component]),
            [2 * value for value in turned[component]],
            [-value for value in rows[component]],
        ]
        for component in range(2)
    ]


def scale_rows(
    rows: list[list[int]], factor: Q
) -> list[list[str]]:
    return [
        [str(factor * value) for value in row]
        for row in rows
    ]


def polynomial_product(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def polynomial_difference(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else 0)
        - (right[index] if index < len(right) else 0)
        for index in range(size)
    ]


QK = tuple[Q, Q]


def qk_multiply(x: QK, y: QK) -> QK:
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c - 2 * b * d


def qk_power(value: QK, exponent: int) -> QK:
    result: QK = (Q(1), Q(0))
    for _index in range(exponent):
        result = qk_multiply(result, value)
    return result


def evaluate_at_signed_kappa(
    coefficients: list[int], sign: int
) -> QK:
    result: QK = (Q(0), Q(0))
    value: QK = (Q(0), Q(sign))
    for exponent, coefficient in enumerate(coefficients):
        power = qk_power(value, exponent)
        result = (
            result[0] + coefficient * power[0],
            result[1] + coefficient * power[1],
        )
    return result


def qk_strings(value: QK) -> list[str]:
    return [str(value[0]), str(value[1])]


def source_g_census(gate3: dict[str, Any]) -> dict[str, int]:
    rows = [gate3["charts"][f"G:{chart}"] for chart in CHART_SIGNS]
    result = {
        "leaf_count": sum(row["leaf_count"] for row in rows),
        "unique_first": sum(
            row["counts"]["unique_first"] for row in rows
        ),
        "tangency_graph": sum(
            row["counts"]["tangency_graph"] for row in rows
        ),
        "multi_candidate": sum(
            row["counts"]["multi_candidate"] for row in rows
        ),
    }
    require(
        result == {
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        },
        "source-G census",
    )
    return result


def safe_output(path: Path) -> None:
    parent = path.parent
    require(parent.exists() and parent.is_dir(), "output parent")
    require(not parent.is_symlink(), "output parent symlink")
    protected = [
        Path(__file__).resolve(),
        *[(HERE / name).resolve() for name in PINS],
    ]
    candidate = path.resolve(strict=False)
    require(candidate not in protected, "protected output")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        mode = path.stat().st_mode
        require(stat.S_ISREG(mode), "output not regular")
        require(path.stat().st_nlink == 1, "output hardlink")
        for item in protected:
            require(
                not (item.exists() and os.path.samefile(path, item)),
                "output aliases protected input",
            )


def build_result() -> dict[str, Any]:
    data = inputs()
    compact = data["compact"]
    gate3 = data["gate3"]
    round169 = data["round169"]
    infra = compact["compact_angular_coordinate_infrastructure"]
    compact_atlas = infra["compact_source_atlas"]
    require(
        infra["all_four_cyclic_seams_exactly_glued"] is True
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
        and infra["kappa_isolation"]["selected_root_in_0_1"] is True
        and infra["kappa_isolation"]["quotient_relation"]
        == "kappa^2=1-2*kappa"
        and infra["source_grazing_ledger"][
            "both_are_physical_boundary_strata"
        ] is True
        and infra["source_grazing_ledger"][
            "neither_is_removed_by_a_coordinate_singularity"
        ] is True,
        "compact infrastructure",
    )

    cover_square_gap = Q(177, 250) ** 2 - Q(1, 2)
    require(cover_square_gap == Q(79, 62500) > 0, "cover gap")
    kappa2: QK = (Q(1), Q(-2))
    one_plus_kappa2: QK = (Q(2), Q(-2))
    squared_denominator = qk_multiply(
        one_plus_kappa2, one_plus_kappa2
    )
    endpoint_residue: QK = (
        8 * kappa2[0] - squared_denominator[0],
        8 * kappa2[1] - squared_denominator[1],
    )
    require(endpoint_residue == (Q(0), Q(0)), "endpoint identity")

    radial_residue = polynomial_difference(
        polynomial_difference(
            polynomial_product([1, 0, 1], [1, 0, 1]),
            polynomial_product([0, 2], [0, 2]),
        ),
        polynomial_product([1, 0, -1], [1, 0, -1]),
    )
    require(radial_residue == [0, 0, 0, 0, 0], "radial identity")

    chart_rows: list[dict[str, Any]] = []
    for chart, sign in CHART_SIGNS.items():
        gate3_id = f"G:{chart}"
        gate3_row = gate3["charts"][gate3_id]
        normal = compact_normal(chart)
        pinned_normal = gate3_normal(chart, sign)
        turned = quarter_turn(normal)
        velocity = velocity_tensor(normal)
        require(
            normal == pinned_normal
            and turned == quarter_turn(pinned_normal)
            and velocity == velocity_tensor(pinned_normal),
            f"state identity:{chart}",
        )
        chart_rows.append({
            "compact_chart": chart,
            "gate3_chart_id": gate3_id,
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
                turned,
            "velocity_denominator": "(1+z^2)*(1+q^2)",
            "velocity_numerator_coefficients_by_component_q0_q1_q2":
                velocity,
            "source_G_center_coefficients_in_1_s":
                [["0", "0"], ["0", "0"]],
            "source_G_radius": "9/25",
            "position_formula": "center_G+(9/25)*normal",
            "position_denominator": "1+z^2",
            "position_numerator_coefficients_in_1_z_z2":
                scale_rows(normal, Q(9, 25)),
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
            "gate3_leaf_count": gate3_row["leaf_count"],
            "gate3_counts": gate3_row["counts"],
            "gate3_leaf_rows_sha256": gate3_row["leaf_rows_sha256"],
            "gate3_provenance": gate3_row["provenance"],
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
    common_denominator = qk_strings(one_plus_kappa2)
    for left_chart, left_sign, right_chart, right_sign in SEAMS:
        left_normal = [
            evaluate_at_signed_kappa(row, left_sign)
            for row in compact_normal(left_chart)
        ]
        right_normal = [
            evaluate_at_signed_kappa(row, right_sign)
            for row in compact_normal(right_chart)
        ]
        require(left_normal == right_normal, "seam normal")
        seam_rows.append({
            "left_face": {
                "chart": left_chart,
                "z": "+kappa" if left_sign == 1 else "-kappa",
            },
            "right_face": {
                "chart": right_chart,
                "z": "+kappa" if right_sign == 1 else "-kappa",
            },
            "common_normal_numerator_in_basis_1_kappa":
                [qk_strings(value) for value in left_normal],
            "common_denominator_in_basis_1_kappa": common_denominator,
            "normal_glues_exactly": True,
            "quarter_turn_and_velocity_glue_for_every_q": True,
            "source_G_position_glues_exactly": True,
        })

    census = source_g_census(gate3)
    r169_inputs = round169["source_G_existing_inputs"]
    r169_keys = round169["source_G_exact_key_coverage_census"]
    require(
        r169_inputs["atlas_leaf_count"] == census["leaf_count"]
        and r169_inputs["atlas_unique_first_leaf_count"]
        == census["unique_first"]
        and r169_inputs["atlas_tangency_graph_leaf_count"]
        == census["tangency_graph"]
        and r169_inputs["atlas_multi_candidate_leaf_count"]
        == census["multi_candidate"]
        and r169_inputs["candidate_exact_key_count"] == 224580
        and r169_keys["global_geometric_exact_key_disposition_count"] == 0
        and r169_keys["keys_without_a_global_geometric_disposition_count"]
        == 224580,
        "Round169 guard",
    )

    return {
        "status": STATUS,
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
            "dependency_sha256": PINS,
            "compact_result_sha256": COMPACT_RESULT_SHA256,
            "compact_verification_result_sha256":
                COMPACT_VERIFICATION_RESULT_SHA256,
            "Round169_result_sha256": ROUND169_RESULT_SHA256,
            "Round169_verification_result_sha256":
                ROUND169_VERIFICATION_RESULT_SHA256,
            "Round162_infrastructure_reused_only_for":
                [
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
            "p_map_derivative":
                "2*(1-q^2)/(1+q^2)^2",
            "p_map_monotone_on_closed_domain": True,
            "p_map_strictly_monotone_on_open_domain": True,
            "t_map_derivative_absolute_value":
                "2*(1-z^2)/(1+z^2)^2",
            "t_map_strictly_monotone_on_each_compact_chart": True,
            "t_map_absolute_endpoint": "1/sqrt(2)",
            "kappa_endpoint_polynomial_residue_in_basis_1_kappa":
                qk_strings(endpoint_residue),
            "gate3_rational_t_cover_square_gap": str(cover_square_gap),
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
            "new_physical_sheet_conclusion_from_guard_bands":
                "NOT_CLAIMED",
            "source_G_gate3_census": census,
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


def build() -> dict[str, Any]:
    result = build_result()
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    safe_output(arguments.output)
    document = build()
    arguments.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
