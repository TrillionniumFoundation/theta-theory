#!/usr/bin/env python3
"""Independent exact verifier for the compact-to-Gate3 coordinate bridge."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERTIFICATE = (
    HERE / "cm2_round162_compact_gate3_coordinate_bridge_certificate.json"
)
OUTPUT = (
    HERE / "cm2_round162_compact_gate3_coordinate_bridge_verification.json"
)
CERTIFICATE_SCHEMA = "cm2.round162.compact-gate3-coordinate-bridge.v1"
SCHEMA = "cm2.round162.compact-gate3-coordinate-bridge.verification.v1"
STATUS = (
    "CERTIFIED_COMPACT_TO_GATE3_SOURCE_W_COORDINATE_COVER__"
    "DYNAMICAL_EXTERIOR_CENSUS_AND_D02_STILL_BLOCKED"
)
PRODUCER = "cm2_round162_compact_gate3_coordinate_bridge.py"
COMPACT_CERTIFICATE = (
    "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json"
)
COMPACT_VERIFICATION = (
    "cm2_round162_compact_angular_coordinate_infrastructure_"
    "verification_2026_07_25.json"
)
GATE3_MANIFEST = (
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
)
GATE3_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
PINS = {
    PRODUCER:
        "52efd57078f7ba2b1f99d7ae9a9d76f1ab2424b597f0cd66cf1c6e5e98cde228",
    COMPACT_CERTIFICATE:
        "f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1",
    COMPACT_VERIFICATION:
        "880a8b06af9243314d987493be631e4b3b8c4ff41c49c623ea85f5340e5c6214",
    GATE3_MANIFEST:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    GATE3_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}
DEPENDENCY_PINS = {
    key: value for key, value in PINS.items() if key != PRODUCER
}
COMPACT_RESULT_SHA256 = (
    "7a8d34caeae05f9964e4805d4c22123a53ca02b12351d26c18d4ef4b2208de75"
)
COMPACT_VERIFICATION_RESULT_SHA256 = (
    "9cddfe7303fac71fb1cbfa48691fb21ecaf031f78aa4ec5fa1bfbb6266937e4e"
)
CHART_SIGNS = {"E": 1, "N": -1, "W": -1, "S": 1}


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load_raw(raw: bytes) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "raw encoding",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "duplicate key")
            result[key] = value
        return result

    value = json.loads(
        raw.decode(),
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
                "decoded string encoding",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, "top object")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


def inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    compact = strict_load(HERE / COMPACT_CERTIFICATE)
    verification = strict_load(HERE / COMPACT_VERIFICATION)
    gate3 = strict_load(HERE / GATE3_MANIFEST)
    require(
        compact["result_sha256"] == COMPACT_RESULT_SHA256
        == digest(compact["result"]),
        "compact result",
    )
    require(
        verification["result_sha256"]
        == COMPACT_VERIFICATION_RESULT_SHA256
        == digest(verification["result"])
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == COMPACT_RESULT_SHA256,
        "compact verification",
    )
    require(
        gate3["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and gate3["coverage"]["domain"]
        == {
            "t": ["-177/250", "177/250"],
            "p": ["-1", "1"],
            "s": ["-1/400", "1/400"],
        }
        and gate3["coverage"]["every_leaf_spans_full_s_window"]
        and gate3["coverage"]["global_leaf_count"] == 143248,
        "Gate3 coverage",
    )
    return compact, verification, gate3


def source_w_census(gate3: dict[str, Any]) -> dict[str, int]:
    rows = [gate3["charts"][f"W:{chart}"] for chart in CHART_SIGNS]
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
            "leaf_count": 76828,
            "unique_first": 26204,
            "tangency_graph": 56,
            "multi_candidate": 50568,
        },
        "source-W census",
    )
    return result


def independent_compact_normal(chart: str) -> list[list[int]]:
    return {
        "E": [[1, 0, -1], [0, 2, 0]],
        "N": [[0, -2, 0], [1, 0, -1]],
        "W": [[-1, 0, 1], [0, -2, 0]],
        "S": [[0, 2, 0], [-1, 0, 1]],
    }[chart]


def independent_gate3_normal(
    chart: str,
    sign: int,
) -> list[list[int]]:
    radial = [1, 0, -1]
    tangent = [0, 2 * sign, 0]
    return {
        "E": [radial, tangent],
        "N": [tangent, radial],
        "W": [[-value for value in radial], tangent],
        "S": [tangent, [-value for value in radial]],
    }[chart]


def independent_quarter_turn(
    rows: list[list[int]],
) -> list[list[int]]:
    return [
        [-value for value in rows[1]],
        list(rows[0]),
    ]


def independent_velocity_tensor(
    rows: list[list[int]],
) -> list[list[list[int]]]:
    turned = independent_quarter_turn(rows)
    return [
        [
            list(rows[component]),
            [2 * value for value in turned[component]],
            [-value for value in rows[component]],
        ]
        for component in range(2)
    ]


def independent_polynomial_product(
    left: list[int],
    right: list[int],
) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def independent_polynomial_difference(
    left: list[int],
    right: list[int],
) -> list[int]:
    size = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else 0)
        - (right[index] if index < len(right) else 0)
        for index in range(size)
    ]


def expected_result() -> dict[str, Any]:
    compact, _verification, gate3 = inputs()
    infra = compact["result"]["compact_angular_coordinate_infrastructure"]
    require(
        infra["all_four_cyclic_seams_exactly_glued"]
        and infra["compact_source_atlas"]["source_chart_count"] == 4
        and infra["source_grazing_ledger"][
            "both_are_physical_boundary_strata"
        ]
        and infra["source_grazing_ledger"][
            "neither_is_removed_by_a_coordinate_singularity"
        ]
        and infra["kappa_isolation"]["selected_root_in_0_1"],
        "compact infrastructure",
    )
    cover_square_gap = Q(177, 250) ** 2 - Q(1, 2)
    require(cover_square_gap == Q(79, 62500) > 0, "cover gap")

    # Independent Q[kappa] reduction.
    def product(x: tuple[Q, Q], y: tuple[Q, Q]) -> tuple[Q, Q]:
        a, b = x
        c, d = y
        return a * c + b * d, a * d + b * c - 2 * b * d

    kappa2 = (Q(1), Q(-2))
    denominator = (Q(2), Q(-2))
    squared = product(denominator, denominator)
    residue = (
        8 * kappa2[0] - squared[0],
        8 * kappa2[1] - squared[1],
    )
    require(residue == (Q(0), Q(0)), "endpoint residue")
    t_radial_identity_residue = independent_polynomial_difference(
        independent_polynomial_difference(
            independent_polynomial_product([1, 0, 1], [1, 0, 1]),
            independent_polynomial_product([0, 2], [0, 2]),
        ),
        independent_polynomial_product([1, 0, -1], [1, 0, -1]),
    )
    require(
        t_radial_identity_residue == [0, 0, 0, 0, 0],
        "t radial polynomial identity",
    )

    chart_rows: list[dict[str, Any]] = []
    for chart, sign in CHART_SIGNS.items():
        gate3_id = f"W:{chart}"
        row = gate3["charts"][gate3_id]
        compact_normal = independent_compact_normal(chart)
        gate3_normal = independent_gate3_normal(chart, sign)
        compact_turned = independent_quarter_turn(compact_normal)
        gate3_turned = independent_quarter_turn(gate3_normal)
        compact_velocity = independent_velocity_tensor(compact_normal)
        gate3_velocity = independent_velocity_tensor(gate3_normal)
        compact_product_center = [["1/2", "1"], ["1/2", "0"]]
        gate3_source_w_center = [["1/2", "1"], ["1/2", "0"]]
        require(
            compact_normal == gate3_normal
            and compact_turned == gate3_turned
            and compact_velocity == gate3_velocity,
            f"state numerator identity:{chart}",
        )
        require(
            compact_product_center == gate3_source_w_center,
            f"source-W product center:{chart}",
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
            "normal_numerator_coefficients_in_1_z_z2":
                compact_normal,
            "quarter_turn_normal_numerator_coefficients_in_1_z_z2":
                compact_turned,
            "velocity_numerator_coefficients_by_component_q0_q1_q2":
                compact_velocity,
            "source_W_center_coefficients_in_1_s":
                compact_product_center,
            "position_formula":
                "center_W(s)+(4/25)*normal",
            "compact_s0_to_gate3_s_product_extension":
                "x(s)=x(0)+s; y(s)=y(0)",
            "normal_formula_agrees_exactly": compact_normal == gate3_normal,
            "quarter_turn_normal_formula_agrees_exactly":
                compact_turned == gate3_turned,
            "velocity_formula_agrees_exactly":
                compact_velocity == gate3_velocity,
            "position_formula_agrees_exactly":
                compact_product_center == gate3_source_w_center
                and compact_normal == gate3_normal,
            "gate3_leaf_count": row["leaf_count"],
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

    return {
        "status": STATUS,
        "scope": {
            "source_obstacle": "W",
            "compact_domain":
                "four charts z in [-kappa,kappa], q in [-1,1]",
            "adjoined_parameter_domain": "s in [-1/400,1/400]",
            "gate3_conservative_domain":
                "t in [-177/250,177/250], p in [-1,1], "
                "s in [-1/400,1/400]",
            "coordinate_cover_only": True,
            "does_not_classify_gate3_leaves": True,
            "does_not_exhaust_return_signatures": True,
            "does_not_exhaust_exterior_sheets": True,
        },
        "provenance": {
            "dependency_sha256": DEPENDENCY_PINS,
            "compact_result_sha256": COMPACT_RESULT_SHA256,
            "compact_verification_result_sha256":
                COMPACT_VERIFICATION_RESULT_SHA256,
            "gate3_global_leaf_count": 143248,
            "old_artifacts_modified": False,
        },
        "exact_coordinate_bridge": {
            "chart_rows": chart_rows,
            "chart_row_sha256": digest(chart_rows),
            "common_p_map": "p=2*q/(1+q^2)",
            "common_t_radial_identity":
                "1-(2z/(1+z^2))^2="
                "((1-z^2)/(1+z^2))^2",
            "t_radial_identity_polynomial_residue_coefficients":
                t_radial_identity_residue,
            "t_radial_positive_root_selected_on_compact_domain": True,
            "reason_for_positive_t_radial_root":
                "kappa is certified in (0,1), so 1-z^2>=0 on "
                "z in [-kappa,kappa]",
            "common_radial_identity":
                "1-p(q)^2=((1-q^2)/(1+q^2))^2",
            "radial_sign_on_closed_q_domain":
                "(1-q^2)/(1+q^2)>=0",
            "p_map_monotone_on_closed_domain": True,
            "p_map_strictly_monotone_on_open_domain": True,
            "t_map_absolute_endpoint": "1/sqrt(2)",
            "t_map_strictly_monotone_on_each_compact_chart": True,
            "kappa_endpoint_polynomial_residue_in_basis_1_kappa":
                [str(residue[0]), str(residue[1])],
            "gate3_rational_t_cover_square_gap":
                str(cover_square_gap),
            "gate3_rational_t_cover_strictly_contains_true_chart":
                True,
            "four_compact_seams_supply_exact_overlap_gluing": True,
            "q_plus_minus_one_are_the_only_source_grazing_strata":
                True,
        },
        "coverage_consequence": {
            "every_compact_source_W_point_has_a_gate3_chart_image": True,
            "every_compact_source_W_chart_image_is_covered_by_pinned_gate3_leaves":
                True,
            "compact_image_uses_only_true_dominant_coordinate_subdomains":
                True,
            "gate3_guard_band_reverse_rechart_status":
                "DEFERRED_TO_EXTERIOR_FACE_LEDGER",
            "new_physical_sheet_conclusion_from_guard_bands":
                "NOT_CLAIMED",
            "source_W_gate3_census": source_w_census(gate3),
            "unresolved_leaf_dispositions_added_by_this_bridge": 0,
            "reason":
                "the bridge proves coordinate coverage and state equality, "
                "not dynamical owner or return-word classification",
        },
        "strict_nonpromotion": {
            "all_disconnected_exterior_sheets_excluded": False,
            "all_chart_and_grazing_strata_dynamically_typed": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "pull Gate3 leaf boxes back through the exact chart maps, "
            "then assign connected/event/excluded/cemetery dispositions "
            "for every relevant return signature with zero unresolved leaves"
        ),
    }


def validate(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and type(document["result"]) is dict
        and type(document["result_sha256"]) is str
        and document["result_sha256"] == digest(document["result"])
        and canonical(document["result"]) == canonical(expected),
        "certificate exact reconstruction",
    )


def mutate(
    document: dict[str, Any],
    path: tuple[Any, ...],
    value: Any,
) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    cursor: Any = candidate
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    candidate["result_sha256"] = digest(candidate["result"])
    return candidate


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    cases = {
        "status": mutate(document, ("result", "status"), "PASS"),
        "source": mutate(
            document, ("result", "scope", "source_obstacle"), "G"
        ),
        "coordinate cover promoted": mutate(
            document,
            ("result", "scope", "does_not_classify_gate3_leaves"),
            False,
        ),
        "t sign": mutate(
            document,
            (
                "result", "exact_coordinate_bridge", "chart_rows", 1,
                "coordinate_map", "t",
            ),
            "2*z/(1+z^2)",
        ),
        "p map": mutate(
            document,
            ("result", "exact_coordinate_bridge", "common_p_map"),
            "p=q",
        ),
        "radial identity": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "common_radial_identity",
            ),
            "false",
        ),
        "t radial identity residue": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "t_radial_identity_polynomial_residue_coefficients", 2,
            ),
            1,
        ),
        "t radial root sign": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "t_radial_positive_root_selected_on_compact_domain",
            ),
            False,
        ),
        "endpoint residue": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "kappa_endpoint_polynomial_residue_in_basis_1_kappa",
                0,
            ),
            "1",
        ),
        "cover gap": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "gate3_rational_t_cover_square_gap",
            ),
            "0",
        ),
        "chart digest": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "chart_row_sha256",
            ),
            "0" * 64,
        ),
        "leaf digest": mutate(
            document,
            (
                "result", "exact_coordinate_bridge", "chart_rows", 0,
                "gate3_leaf_rows_sha256",
            ),
            "0" * 64,
        ),
        "normal numerator": mutate(
            document,
            (
                "result", "exact_coordinate_bridge", "chart_rows", 2,
                "normal_numerator_coefficients_in_1_z_z2", 0, 0,
            ),
            0,
        ),
        "endpoint orientation": mutate(
            document,
            (
                "result", "exact_coordinate_bridge", "chart_rows", 1,
                "compact_z_endpoint_map_to_true_t_boundary",
                "z=-kappa",
            ),
            "-1/sqrt(2)",
        ),
        "position product extension": mutate(
            document,
            (
                "result", "exact_coordinate_bridge", "chart_rows", 0,
                "source_W_center_coefficients_in_1_s", 0, 1,
            ),
            "0",
        ),
        "grazing erased": mutate(
            document,
            (
                "result", "exact_coordinate_bridge",
                "q_plus_minus_one_are_the_only_source_grazing_strata",
            ),
            False,
        ),
        "guard band reverse rechart promoted": mutate(
            document,
            (
                "result", "coverage_consequence",
                "gate3_guard_band_reverse_rechart_status",
            ),
            "CERTIFIED",
        ),
        "guard band physical conclusion promoted": mutate(
            document,
            (
                "result", "coverage_consequence",
                "new_physical_sheet_conclusion_from_guard_bands",
            ),
            "NO_NEW_SHEETS",
        ),
        "dispositions invented": mutate(
            document,
            (
                "result", "coverage_consequence",
                "unresolved_leaf_dispositions_added_by_this_bridge",
            ),
            76828,
        ),
        "census": mutate(
            document,
            (
                "result", "coverage_consequence",
                "source_W_gate3_census", "multi_candidate",
            ),
            0,
        ),
        "D02": mutate(
            document,
            ("result", "strict_nonpromotion", "D02"),
            "READY",
        ),
        "exterior": mutate(
            document,
            (
                "result", "strict_nonpromotion",
                "all_disconnected_exterior_sheets_excluded",
            ),
            True,
        ),
        "bool-int": mutate(
            document,
            (
                "result", "scope",
                "does_not_exhaust_exterior_sheets",
            ),
            1,
        ),
        "extra": mutate(document, ("result", "extra"), True),
    }
    rejected = 0
    for label, candidate in cases.items():
        try:
            validate(candidate, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"semantic attack accepted:{label}")
    return {
        "attack_count": len(cases),
        "rejected_count": rejected,
        "all_rejected": rejected == len(cases),
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"x":1,"x":2}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'\xef\xbb\xbf{"x":1}',
        b'{"x":"\\u0000"}',
        b'{"x":"\\ud800"}',
        b'{"x":1}\x00',
    ]
    rejected = 0
    for raw in attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("strict JSON attack accepted")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_rejected": rejected == len(attacks),
    }


def build() -> dict[str, Any]:
    document = strict_load(CERTIFICATE)
    expected = expected_result()
    validate(document, expected)
    semantic = semantic_attacks(document, expected)
    strict_attacks = strict_json_attacks()
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "producer_imported_or_executed": False,
        "Q_kappa_endpoint_identity_independently_reduced": True,
        "four_chart_signs_and_state_identities_independently_rebuilt": True,
        "Gate3_source_W_coverage_census_independently_rebuilt": True,
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_attacks,
        "strict_nonpromotion_recomputed": True,
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    document = build()
    if not arguments.self_test:
        arguments.output.write_text(
            json.dumps(
                document,
                sort_keys=True,
                indent=2,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
