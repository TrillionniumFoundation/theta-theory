#!/usr/bin/env python3
"""Fail-closed verifier for the Round145 finite leaf-corridor atlas.

The verifier does not import the producer.  It independently validates the
closed envelope, dependency pins, exact atlas adjacency, corrected
Round137-v1 ranks, short-cell and image-recut algebra, null historical
fields, and hostile mutations.  It validates a separately materialized
12,288-bit cross-precision replay under an exact semantic/no-worse contract,
then executes the byte-pinned producer again at 8,192 bits under a different
hash seed and requires a byte-identical primary certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round145_finite_connected_leaf_corridor_atlas.py"
)
CERTIFICATE = (
    HERE / "cm2-round145-finite-connected-leaf-corridor-atlas-2026-07-24.json"
)
SECONDARY_CERTIFICATE = (
    HERE
    / "cm2-round145-finite-connected-leaf-corridor-atlas-secondary-12288-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round145-finite-connected-leaf-corridor-atlas-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = "cm2.round145.finite-connected-leaf-corridor-atlas.v1"
VERIFICATION_SCHEMA = (
    "cm2.round145.finite-connected-leaf-corridor-atlas-verification.v1"
)
PRODUCER_SHA256 = (
    "6deed0506b0105eee9ee9a89dd4c28ee9bed81aa4922586eb8b8005a433ba4c7"
)
CERTIFICATE_SHA256 = (
    "5edac93e1425c72992ab671f3b3f7db269d236819ea3ad689b612505426ccec6"
)
CERTIFICATE_RESULT_SHA256 = (
    "16cec30f7af9d3f0d278d0bae85f8dca4a9a3041186021fc7ebd1b9c43a7fc0b"
)
SECONDARY_CERTIFICATE_SHA256 = (
    "c96dd56c7070e6f35d3302245c2e132bbb061388c54ebc96880f232626af2192"
)
SECONDARY_CERTIFICATE_RESULT_SHA256 = (
    "b62020c00b861e1634ab7a4c77ce280aa48b29117d7fc096c39dfe39d4826108"
)
MAX_CERTIFICATE_BYTES = 2_000_000
MAX_JSON_INTEGER_DIGITS = 20_000
RETURN_DEPTH = 1648
PRIMARY_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
OWNER_SEQUENCE_SHA256 = (
    "c50277af0c038521b8933672d2a5a2b9035473895694c3c2878842274337cac3"
)
OFFICIAL_SEQUENCE_SHA256 = (
    "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
)
COMPACT_PATH_SHA256 = (
    "c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17"
)
REGULAR_SPECS = (
    *((4292, index) for index in range(8)),
    *((4294, index) for index in range(32, 36)),
)

INPUT_PINS = {
    "cm2_round141_centered_affine_d0_collar_spike.py":
        "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1",
    "cm2_round145_leaf_corridor_atlas_spike.py":
        "c2bf266f715a8214a13f87308dd9c982e520b39a2747e23fedc1c7955fd62c78",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json":
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2_round141_recentered_affine_k4296_d0_collar_return.py":
        "687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28",
    "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json":
        "a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe",
    "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py":
        "1bb85fdd8dc22aa941084666b5eb9c41154f9e890f6d87c42eaf8808a4748f65",
    "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json":
        "43770a85918cd4986e232cc1e3c401bae9ff8d0ee772b92eea8c46c3c55d4e3c",
    "cm2-round141-recentered-affine-k4296-d0-collar-return-manifest-2026-07-24.sha256":
        "06351a018876a3ec96cc099b9fd44d779c8a533543c7f7cb75379181dc32de52",
    "cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py":
        "bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38",
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json":
        "74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67",
    "cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py":
        "197be350c4a6bed80a1c413822c5b838c2d0bc7da88360998fd7ad939da85601",
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-verification-2026-07-24.json":
        "3ee6fe0e48bdf05a6f76726ded302aa4d632c306a4a260f444e1c2a66dfd9bd7",
    "cm2-one-hundred-forty-third-direct-assault-manifest-2026-07-24.sha256":
        "f8215c273ff1a7b9cd01c5f53abae3f6ab03907a5795a6aecaab864129ac6e22",
}

CLOSED = {
    "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json": (
        "cm2.round141.recentered-affine-k4296-d0-collar-return.v1",
        "48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f",
    ),
    "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json": (
        "cm2.round141.recentered-affine-k4296-d0-collar-return-verification.v1",
        "8c94e2f846062cae13be0d9fb8520877cb6de7903354090df87ad084d74153a4",
    ),
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json": (
        "cm2.round143.r1648-terminal-face-endpoint-recut-frontier.v1",
        "35a9f8e0437086a2feaf294c10c621ce21319dc93aac88f33dbc4024e4507e92",
    ),
    "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-verification-2026-07-24.json": (
        "cm2.round143.r1648-terminal-face-endpoint-recut-frontier-verification.v1",
        "51d616892452c92a4ed47586b6923ffaaf8e722e6b32d48445cbb4f762f9cf1c",
    ),
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path, maximum_bytes: int = MAX_CERTIFICATE_BYTES) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink()
        and metadata.st_size <= maximum_bytes,
        "safe bounded JSON input",
    )
    document = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_int=lambda text: (
            int(text)
            if len(text.lstrip("-")) <= MAX_JSON_INTEGER_DIGITS
            else (_ for _ in ()).throw(ValueError("oversized JSON integer"))
        ),
        parse_float=lambda text: (_ for _ in ()).throw(
            ValueError(f"JSON float forbidden:{text}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite:{token}")
        ),
    )
    require(type(document) is dict, "JSON root object")
    return document


def interval_pair_count(level: int) -> int:
    require(level >= 0, "nonnegative rank level")
    return 0 if level < 2 else (2**level - 1) * (2**level - 2) // 2


def pair_lex_rank(level: int, left: int, right: int) -> int:
    maximum = 2**level - 1
    require(1 <= left < right <= maximum, "rank pair range")
    return (left - 1) * maximum - (left - 1) * left // 2 + right - left - 1


def even_pair_count_before(level: int, left: int, right: int) -> int:
    half_maximum = 2 ** (level - 1) - 1
    even_left_before = (left - 1) // 2
    total = (
        even_left_before * half_maximum
        - even_left_before * (even_left_before + 1) // 2
    )
    if left % 2 == 0:
        total += max(0, (right - 1) // 2 - left // 2)
    return total


def rank_1d(row: list[int]) -> int:
    require(
        len(row) == 3 and all(type(value) is int for value in row),
        "rank row",
    )
    level, left, right = row
    require(level >= 2 and (left % 2 or right % 2), "primitive rank row")
    return (
        interval_pair_count(level - 1)
        + pair_lex_rank(level, left, right)
        - even_pair_count_before(level, left, right)
    )


def encoded_integer_matches(record: dict[str, Any], value: int) -> bool:
    decimal = str(value)
    return record == {
        "decimal": decimal,
        "hexadecimal": "0x" + format(value, "x"),
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


def validate_coordinate_rank(record: dict[str, Any], level: int) -> None:
    row = record["contained_primitive_basis_row"]
    require(row[0] == level and row[2] == row[1] + 1, "rank level/pair")
    endpoint = record["endpoint_fixed_dyadic_outers"]
    lower = tuple(Q(value) for value in endpoint["left"])
    upper = tuple(Q(value) for value in endpoint["right"])
    denominator = 2**level
    require(
        Q(0) < lower[0] < lower[1]
        < Q(row[1], denominator) < Q(row[2], denominator)
        < upper[0] < upper[1] < Q(1),
        "rank strict containment",
    )
    previous = 2 ** (level - 1)
    first_previous = (
        lower[1].numerator * previous // lower[1].denominator + 1
    )
    require(
        not (
            Q(first_previous, previous) > lower[1]
            and Q(first_previous + 1, previous) < upper[0]
        ),
        "rank level minimality",
    )
    value = rank_1d(row)
    require(
        encoded_integer_matches(
            record["contained_primitive_basis_rank"], value
        )
        and record["rank_unrank_roundtrip_exact"] is True
        and record[
            "least_Round137_v1_rank_for_this_declared_coordinate_interval"
        ] is True,
        "rank encoding",
    )


def lambda_bounds(power: int, cell_index: int) -> tuple[Q, Q]:
    denominator = 2 ** (power - 4289)
    return Q(cell_index, denominator), Q(cell_index + 1, denominator)


def precision_stable_atlas_identity(atlas: dict[str, Any]) -> dict[str, Any]:
    return {
        "regular_cells": [
            {
                key: row[key]
                for key in (
                    "atlas_index",
                    "power",
                    "cell_index",
                    "lambda_bounds",
                    "D0_collision3_mode",
                    "official_sequence_sha256",
                    "compact_path_sha256",
                    "terminal_p_derivative_lambda_sign",
                    "terminal_image_derivative_lambda_sign",
                )
            }
            for row in atlas["regular_dyadic_cells"]
        ],
        "clipped_endpoint_cell": {
            key: atlas["clipped_endpoint_cell"][key]
            for key in (
                "lambda_bounds",
                "ordinary_D0_collision3_strict_miss",
                "official_sequence_sha256",
                "physical_interior_compact_path_sha256",
                "terminal_only_active_face",
                "terminal_p_derivative_lambda_sign",
                "terminal_image_derivative_lambda_sign",
            )
        },
        "internal_shared_faces": atlas["internal_shared_faces"],
        "cell_adjacency_graph": atlas["cell_adjacency_graph"],
    }


def validate_dependencies(provenance: dict[str, Any]) -> dict[str, dict[str, Any]]:
    require(
        provenance["dependency_sha256"] == dict(sorted(INPUT_PINS.items())),
        "embedded dependency pins",
    )
    closed: dict[str, dict[str, Any]] = {}
    for name, expected_hash in INPUT_PINS.items():
        path = HERE / name
        require(sha256(path) == expected_hash, f"dependency pin:{name}")
        if name not in CLOSED:
            continue
        document = strict_json(path)
        schema, result_hash = CLOSED[name]
        require(
            document["schema"] == schema
            and document["result_sha256"] == result_hash
            and digest(document["result"]) == result_hash,
            f"closed dependency:{name}",
        )
        closed[name] = document["result"]
    return closed


def validate_result(
    result: dict[str, Any],
    expected_generation_precision_bits: int = PRIMARY_PRECISION_BITS,
) -> None:
    require_no_json_floats(result)
    require(
        result["status"]
        == "CERTIFIED_FINITE_CONNECTED_R1648_PHYSICAL_LEAF_CORRIDOR_ATLAS"
        and result["generation_precision_bits"]
        == expected_generation_precision_bits
        and result["minimum_certified_precision_bits"]
        == PRIMARY_PRECISION_BITS
        and result["secondary_verifier_precision_bits"]
        == SECONDARY_PRECISION_BITS,
        "status and precision",
    )
    provenance = result["provenance"]
    require(
        provenance["producer_sha256"] == PRODUCER_SHA256
        and provenance["append_only"] is True
        and provenance["Round139_Round141_Round143_files_modified"] is False,
        "provenance",
    )
    closed = validate_dependencies(provenance)
    r143 = closed[
        "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json"
    ]
    endpoint_bracket = tuple(
        Q(value)
        for value in r143["terminal_face_endpoint"]["lambda_bracket"]
    )
    scaled = result["scaled_leaf_coordinate"]
    require(
        scaled["scale_power"] == 4289
        and scaled["physical_open_interval"]
        == "0 < lambda < lambda_terminal"
        and tuple(Q(value) for value in scaled["terminal_lambda_bracket"])
        == endpoint_bracket
        and Q(9, 8) < endpoint_bracket[0] < endpoint_bracket[1] < Q(5, 4),
        "scaled leaf coordinate",
    )
    atlas = result["finite_connected_atlas"]
    cells = atlas["regular_dyadic_cells"]
    require(
        atlas["regular_dyadic_cell_count"] == 12
        and atlas["coarse_K4292_cell_count"] == 8
        and atlas["refined_K4294_terminal_tail_cell_count"] == 4
        and atlas["clipped_endpoint_cell_count"] == 1
        and atlas["total_cell_count"] == 13
        and len(cells) == 12,
        "atlas counts",
    )
    stable_identity_sha256 = digest(
        precision_stable_atlas_identity(atlas)
    )
    require(
        atlas["precision_stable_identity_sha256"]
        == stable_identity_sha256
        and atlas["model_radius_ledger_contract"]
        == "generation-precision-specific evidence excluded from the branch identity",
        "precision-stable atlas identity",
    )
    for atlas_index, (cell, spec) in enumerate(zip(cells, REGULAR_SPECS)):
        power, cell_index = spec
        bounds = lambda_bounds(power, cell_index)
        require(
            cell["atlas_index"] == atlas_index
            and cell["power"] == power
            and cell["cell_index"] == cell_index
            and tuple(Q(value) for value in cell["lambda_bounds"]) == bounds
            and cell["D0_collision3_mode"]
            == (
                "analytic_double_root_only_at_lambda_zero"
                if atlas_index == 0
                else "ordinary_strict_radius4_miss"
            )
            and cell["official_sequence_sha256"] == OFFICIAL_SEQUENCE_SHA256
            and cell["compact_path_sha256"] == COMPACT_PATH_SHA256
            and type(cell["model_radius_ledger_sha256"]) is str
            and len(cell["model_radius_ledger_sha256"]) == 64
            and set(cell["model_radius_ledger_sha256"])
            <= set("0123456789abcdef")
            and cell[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ] <= -10
            and type(cell[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ]) is int
            and type(cell["maximum_state_radius_witness"]) is list
            and len(cell["maximum_state_radius_witness"]) == 3
            and all(
                type(value) is int
                for value in cell["maximum_state_radius_witness"]
            )
            and cell["maximum_state_radius_witness"][0] == RETURN_DEPTH
            and cell["maximum_state_radius_witness"][1] == 2
            and cell["maximum_state_radius_witness"][2]
            == cell[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ]
            and type(cell[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ]) is list
            and len(cell[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ]) == 4
            and all(
                type(value) is int and value <= -10
                for value in cell[
                    "terminal_state_radius_strict_upper_power_of_two_exponents"
                ]
            )
            and max(cell[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ]) == cell[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ]
            and cell[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ][2] == cell[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ]
            and type(cell[
                "worst_decision_margin_dyadic_depth"
            ]) is int
            and cell["worst_decision_margin_dyadic_depth"] >= 0
            and type(cell["worst_decision_margin_names"]) is list
            and bool(cell["worst_decision_margin_names"])
            and all(
                type(value) is str and value
                for value in cell["worst_decision_margin_names"]
            )
            and cell["terminal_p_derivative_lambda_sign"] == -1
            and cell["terminal_image_derivative_lambda_sign"] == -1
            and cell["terminal_p_derivative_margin_dyadic_depth"] >= 0
            and cell["terminal_image_derivative_margin_dyadic_depth"] >= 0,
            f"regular cell:{atlas_index}",
        )
    clipped = atlas["clipped_endpoint_cell"]
    require(
        tuple(Q(value) for value in clipped["lambda_bounds"])
        == (Q(9, 8), endpoint_bracket[1])
        and clipped["contains_unique_Round143_terminal_face_root"] is True
        and clipped["ordinary_D0_collision3_strict_miss"] is True
        and type(clipped["model_radius_ledger_sha256"]) is str
        and len(clipped["model_radius_ledger_sha256"]) == 64
        and set(clipped["model_radius_ledger_sha256"])
        <= set("0123456789abcdef")
        and clipped["official_sequence_sha256"] == OFFICIAL_SEQUENCE_SHA256
        and clipped["physical_interior_compact_path_sha256"]
        == COMPACT_PATH_SHA256
        and clipped["preterminal_strict_nonreturn_count"] == RETURN_DEPTH - 1
        and type(clipped[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]) is int
        and clipped[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ] <= -10
        and type(clipped["maximum_state_radius_witness"]) is list
        and len(clipped["maximum_state_radius_witness"]) == 3
        and all(
            type(value) is int
            for value in clipped["maximum_state_radius_witness"]
        )
        and clipped["maximum_state_radius_witness"][0] == RETURN_DEPTH
        and clipped["maximum_state_radius_witness"][1] == 2
        and clipped["maximum_state_radius_witness"][2]
        == clipped[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        and type(clipped[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ]) is list
        and len(clipped[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ]) == 4
        and all(
            type(value) is int and value <= -10
            for value in clipped[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ]
        )
        and max(clipped[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ]) == clipped[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        and clipped[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ][2] == clipped[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        and clipped["terminal_closed_box_classification"]
        == "UNRESOLVED_TIME3_OUTER"
        and clipped["terminal_only_active_face"] == "G:S p=-1/50"
        and clipped["terminal_p_derivative_lambda_sign"] == -1
        and clipped["terminal_image_derivative_lambda_sign"] == -1,
        "clipped endpoint cell",
    )
    faces = atlas["internal_shared_faces"]
    require(len(faces) == 12, "shared face count")
    for index, face in enumerate(faces):
        expected_lambda = (
            Q(cells[index + 1]["lambda_bounds"][0])
            if index < 11
            else Q(9, 8)
        )
        require(
            face["face_index"] == index + 1
            and Q(face["lambda"]) == expected_lambda
            and face["left_cell"] == index
            and face["right_cell"]
            == (index + 1 if index < 11 else "clipped_endpoint_cell")
            and face["exactly_shared"] is True
            and face[
                "same_parameter_substitution_into_exact_initial_leaf_map"
            ] is True
            and face["same_1648_selected_collision_map_composition"] is True,
            f"shared face:{index}",
        )
    require(
        atlas["all_internal_faces_exactly_shared"] is True
        and atlas["cell_adjacency_graph"] == "path_on_13_vertices"
        and atlas["cell_adjacency_graph_connected"] is True
        and all(
            atlas[name] is True
            for name in (
                "same_exact_fixed_s_slope4_leaf",
                "same_1648_owner_sequence_on_every_cell",
                "same_1648_official_word_sequence_on_every_cell",
                "same_H0_homogeneity_on_every_stage",
                "same_incidence_rank_14_on_every_stage",
            )
        ),
        "atlas global identities",
    )
    proof = result["boundary_and_physical_branch_proof"]
    interval_payload = {
        "Round143_prospective_interval_id":
            r143["candidate_full_leaf_interval"]["prospective_interval_id"],
        "lambda_scale_power": 4289,
        "right_boundary": "lambda=0 collision3 D0 tangency",
        "left_boundary_bracket": [
            str(value.numerator)
            if value.denominator == 1
            else f"{value.numerator}/{value.denominator}"
            for value in endpoint_bracket
        ],
        "owner_sequence_sha256": OWNER_SEQUENCE_SHA256,
        "official_sequence_sha256": OFFICIAL_SEQUENCE_SHA256,
        "precision_stable_atlas_identity_sha256":
            stable_identity_sha256,
    }
    expected_interval = (
        "round145-v1-connected-physical-r1648-leaf:"
        + digest(interval_payload)
    )
    require(
        proof["connected_interval_id"] == expected_interval
        and proof["payload_sha256"] == digest(interval_payload)
        and proof["connected_physical_open_branch_certified"] is True
        and proof[
            "maximal_for_frozen_itinerary_and_destination_core_on_this_leaf"
        ] is True
        and proof["global_two_dimensional_component_maximality_certified"]
        is False
        and all(
            proof[name] is True
            for name in (
                "D0_strict_miss_for_every_positive_lambda_cell",
                "Round143_terminal_root_derivative_strictly_negative",
                "Round143_terminal_root_unique_in_bracket",
                "first_1647_collisions_strict_nonreturn_on_whole_atlas",
                "collision_1648_strict_return_on_lambda_below_root",
                "collision_1648_exits_only_through_terminal_p_face_at_root",
                "terminal_p_strictly_decreasing_on_every_atlas_cell",
                "no_owner_word_chart_homogeneity_or_incidence_boundary_inside",
            )
        ),
        "physical branch proof",
    )
    ranks = result["promoted_Round137_v1_leaf_rank"]
    validate_coordinate_rank(ranks["canonical_H1_x_least_rank"], 4290)
    validate_coordinate_rank(ranks["normalized_t_cross_check"], 4283)
    require(
        ranks["coordinate_contract"]
        == "round137-dyadic-basis-enumeration-v1"
        and ranks["canonical_coordinate"] == "x=sqrt(17)*r"
        and ranks["canonical_H1_x_level"] == 4290
        and ranks["normalized_t_level"] == 4283
        and ranks["canonical_H1_x_least_rank"]
        == r143["coordinate_explicit_Round137_v1_leaf_ranks"][
            "canonical_H1_x_candidate"
        ]
        and ranks["normalized_t_cross_check"]
        == r143["coordinate_explicit_Round137_v1_leaf_ranks"][
            "Round140_normalized_t_candidate"
        ]
        and ranks["rank_is_for_certified_connected_physical_branch"] is True
        and ranks["historical_Round35_coordinate_crosswalk_available"] is False
        and ranks["historical_Round35_source_interval_rank"] is None,
        "promoted coordinate ranks",
    )
    short = result["promoted_v1_source_short_cell"]
    source_interval = r143["candidate_full_leaf_interval"]
    mesh_source = r143["B14_source_mesh_frontier"]
    adapted_length_outer = tuple(
        Q(value) for value in short["adapted_length_outer"]
    )
    expected_short_id = "round145-v1-source-short-cell:" + digest({
        "interval": expected_interval,
        "k": 0,
        "scale": "1e-90",
    })
    require(
        short["connected_interval_id"] == expected_interval
        and short["adapted_line_element"]
        == source_interval["source_adapted_line_element"]
        and short["adapted_length_outer"]
        == source_interval["source_adapted_length_outer"]
        and Q(0) < adapted_length_outer[0] < adapted_length_outer[1]
        < Q(1, 10**90)
        and adapted_length_outer[1] < Q(1, 8388608)
        and short["below_delta_14"] is True
        and short["below_1e_minus_90"] is True
        and short["corrected_left_anchored_natural_short_cell_k"] == 0
        and short["corrected_v1_source_cell_id"] == expected_short_id
        and short["historical_Round35_natural_short_cell_k"] is None
        and short["historical_Round35_parent_W_id"] is None
        and short["Round143_mesh_cross_check_sha256"]
        == digest(mesh_source),
        "source short cell",
    )
    recut = result["promoted_v1_image_recut"]
    recut_source = r143["formal_image_recut_frontier"]
    recut_count = int(recut["corrected_v1_image_recut_count"]["decimal"])
    recut_length_outer = tuple(
        Q(value) for value in recut["formal_adapted_length_outer"]
    )
    recut_scale = Q(1, 10**90)
    require(
        recut["adapted_length_endpoint_formula"]
        == recut_source["adapted_length_endpoint_formula"]
        and recut["formal_adapted_length_outer"]
        == recut_source["formal_adapted_length_outer"]
        and recut["deterministic_recut_scale"]
        == recut_source["deterministic_recut_scale"]
        and recut["corrected_v1_image_recut_count"]
        == recut_source["conditional_image_recut_count"]
        and recut["corrected_v1_image_recut_rank_range"]
        == recut_source["conditional_image_recut_rank_range"]
        and recut["corrected_v1_last_image_recut_rank"]
        == recut_source["conditional_last_image_recut_rank"]
        and recut["Round143_prospective_registry_id"]
        == recut_source["prospective_recut_registry_id"]
        and Q(0) < recut_length_outer[0] <= recut_length_outer[1]
        and (recut_count - 1) * recut_scale
        < recut_length_outer[0]
        and recut_length_outer[1] <= recut_count * recut_scale
        and encoded_integer_matches(
            recut["corrected_v1_image_recut_count"], recut_count
        )
        and recut["corrected_v1_image_recut_rank_range"]
        == [0, str(recut_count - 1)]
        and recut["corrected_v1_first_image_recut_rank"] == 0
        and recut["corrected_v1_last_image_recut_rank"]
        == str(recut_count - 1)
        and recut["connected_source_branch_certified"] is True
        and recut["continuous_return_image_of_connected_branch"] is True
        and recut["image_is_one_connected_interval"] is True
        and recut["image_observable"]
        == "asin(t_1648)+asin(p_1648)"
        and recut[
            "image_observable_strictly_decreasing_on_every_atlas_cell"
        ] is True
        and recut["image_observable_shared_face_continuity_exact"] is True
        and recut["no_internal_image_extremum"] is True
        and recut["endpoint_difference_is_complete_image_span"] is True,
        "image recut algebra",
    )
    recut_payload = {
        "connected_interval_id": expected_interval,
        "adapted_length_outer": recut["formal_adapted_length_outer"],
        "scale": recut["deterministic_recut_scale"],
        "count": str(recut_count),
        "rank_range": recut["corrected_v1_image_recut_rank_range"],
    }
    require(
        recut["corrected_v1_image_recut_registry_id"]
        == "round145-v1-image-recut-registry:" + digest(recut_payload)
        and recut["historical_Round35_image_recut_rank"] is None
        and recut["historical_Round35_restriction_id"] is None,
        "image recut registry",
    )
    counts = result["count_ledger"]
    require(
        counts["atlas_cell_count"] == 13
        and counts["exact_internal_shared_face_count"] == 12
        and counts["collision_stage_cell_pairs"] == 13 * RETURN_DEPTH
        and counts["full_radius4_candidate_test_count"]
        == 13 * RETURN_DEPTH * 161
        and counts["preterminal_strict_nonreturn_cell_stage_pairs"]
        == 13 * (RETURN_DEPTH - 1)
        and counts["coordinate_explicit_v1_leaf_rank_count"] == 2
        and counts["corrected_v1_source_short_cell_count"] == 1
        and counts["corrected_v1_image_recut_registry_count"] == 1
        and counts["historical_identifier_count"] == 0
        and counts["global_complete_18_field_block_count"] == 0,
        "count ledger",
    )
    nonpromotion = result["strict_nonpromotion"]
    historical = [
        key for key in nonpromotion
        if key.startswith("historical_")
    ]
    require(
        historical
        and all(nonpromotion[key] is None for key in historical)
        and nonpromotion["Round50_owner_key_count"] == 0
        and nonpromotion["Round54_t54_token_count"] == 0
        and nonpromotion["Round67_q_j_output_count"] == 0
        and nonpromotion["global_gate5_maturity"] == "10/18"
        and nonpromotion["global_complete_18_field_block_count"] == 0
        and nonpromotion["Gate5"] == "NOT_CERTIFIED"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )
    require(
        result["strict_nonclaims"] == [
            "the connected fixed-leaf branch does not prove a maximal two-dimensional H1 component",
            "the Round137-v1 rank is a corrected coordinate-explicit rank, not the unnamed historical Round27 or Round35 enumeration",
            "the corrected k=0 and image recut registry are not historical Round35 identifiers",
            "the D0 and terminal-face endpoints are boundary limits, not regular interior trajectories",
            "no Round50 owner, Round54 token, Round67 q_j, Gate5 field or CM2 claim is promoted",
        ],
        "strict nonclaims",
    )


def mutate_at(value: Any, path: tuple[Any, ...], replacement: Any) -> Any:
    result = copy.deepcopy(value)
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


def require_no_json_floats(value: Any) -> None:
    require(type(value) is not float, "JSON float forbidden")
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str, "JSON object key")
            require_no_json_floats(child)
    elif type(value) is list:
        for child in value:
            require_no_json_floats(child)


def semantic_attack_suite(result: dict[str, Any]) -> dict[str, Any]:
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("status", ("status",), "PASS"),
        ("generation", ("generation_precision_bits",), 1),
        ("primary", ("minimum_certified_precision_bits",), 1),
        ("secondary", ("secondary_verifier_precision_bits",), 1),
        ("producer", ("provenance", "producer_sha256"), "0" * 64),
        ("pins", ("provenance", "dependency_sha256"), {}),
        ("append", ("provenance", "append_only"), False),
        ("scale", ("scaled_leaf_coordinate", "scale_power"), 0),
        ("interval", ("scaled_leaf_coordinate", "physical_open_interval"), "closed"),
        ("cells", ("finite_connected_atlas", "regular_dyadic_cell_count"), 11),
        ("total", ("finite_connected_atlas", "total_cell_count"), 12),
        ("stable_identity", (
            "finite_connected_atlas",
            "precision_stable_identity_sha256",
        ), "0" * 64),
        ("cell_power", ("finite_connected_atlas", "regular_dyadic_cells", 0, "power"), 1),
        ("cell_index", ("finite_connected_atlas", "regular_dyadic_cells", 1, "cell_index"), 99),
        ("cell_bounds", ("finite_connected_atlas", "regular_dyadic_cells", 2, "lambda_bounds"), ["0", "1"]),
        ("owner", ("finite_connected_atlas", "regular_dyadic_cells", 3, "official_sequence_sha256"), "0" * 64),
        ("compact", ("finite_connected_atlas", "regular_dyadic_cells", 4, "compact_path_sha256"), "0" * 64),
        ("dp", ("finite_connected_atlas", "regular_dyadic_cells", 5, "terminal_p_derivative_lambda_sign"), 1),
        ("dimage", ("finite_connected_atlas", "regular_dyadic_cells", 6, "terminal_image_derivative_lambda_sign"), 1),
        ("clipped_bound", ("finite_connected_atlas", "clipped_endpoint_cell", "lambda_bounds"), ["0", "1"]),
        ("clipped_class", ("finite_connected_atlas", "clipped_endpoint_cell", "terminal_closed_box_classification"), "RETURN_AT_3_INNER"),
        ("clipped_face", ("finite_connected_atlas", "clipped_endpoint_cell", "terminal_only_active_face"), "none"),
        ("clipped_radius", (
            "finite_connected_atlas",
            "clipped_endpoint_cell",
            "maximum_state_radius_strict_upper_power_of_two_exponent",
        ), 999),
        ("worst_margin", (
            "finite_connected_atlas",
            "regular_dyadic_cells",
            0,
            "worst_decision_margin_dyadic_depth",
        ), -999),
        ("radius_witness", (
            "finite_connected_atlas",
            "regular_dyadic_cells",
            0,
            "maximum_state_radius_witness",
        ), [999999, 999, -10]),
        ("faces", ("finite_connected_atlas", "internal_shared_faces"), []),
        ("connected", ("finite_connected_atlas", "cell_adjacency_graph_connected"), False),
        ("branch", ("boundary_and_physical_branch_proof", "connected_physical_open_branch_certified"), False),
        ("component", ("boundary_and_physical_branch_proof", "global_two_dimensional_component_maximality_certified"), True),
        ("interval_id", ("boundary_and_physical_branch_proof", "connected_interval_id"), "bad"),
        ("xlevel", ("promoted_Round137_v1_leaf_rank", "canonical_H1_x_level"), 1),
        ("xrow", ("promoted_Round137_v1_leaf_rank", "canonical_H1_x_least_rank", "contained_primitive_basis_row", 0), 1),
        ("ulevel", ("promoted_Round137_v1_leaf_rank", "normalized_t_level"), 1),
        ("k", ("promoted_v1_source_short_cell", "corrected_left_anchored_natural_short_cell_k"), 1),
        ("short_length", (
            "promoted_v1_source_short_cell",
            "adapted_length_outer",
        ), "forged"),
        ("shortid", ("promoted_v1_source_short_cell", "corrected_v1_source_cell_id"), "bad"),
        ("recutcount", ("promoted_v1_image_recut", "corrected_v1_image_recut_count", "decimal"), "1"),
        ("recutrange", ("promoted_v1_image_recut", "corrected_v1_image_recut_rank_range"), [0, "0"]),
        ("recutid", ("promoted_v1_image_recut", "corrected_v1_image_recut_registry_id"), "bad"),
        ("historical", ("strict_nonpromotion", "historical_Round35_rn_restriction_id"), "invented"),
        ("gate", ("strict_nonpromotion", "global_gate5_maturity"), "18/18"),
        ("blocks", ("strict_nonpromotion", "global_complete_18_field_block_count"), 1),
        ("cm2", ("strict_nonpromotion", "CM2"), "GO"),
        ("nonclaims", ("strict_nonclaims",), []),
        ("count", ("count_ledger", "atlas_cell_count"), 12),
        ("numeric_float", (
            "finite_connected_atlas",
            "regular_dyadic_cell_count",
        ), 12.0),
        ("tests", ("count_ledger", "full_radius4_candidate_test_count"), 0),
    ]
    rejected = 0
    for name, path, replacement in attacks:
        candidate = mutate_at(result, path, replacement)
        try:
            validate_result(candidate)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"semantic mutation accepted:{name}")
    coordinated = copy.deepcopy(result)
    recut = coordinated["promoted_v1_image_recut"]
    one = {
        "decimal": "1",
        "hexadecimal": "0x1",
        "bit_length": 1,
        "decimal_digit_count": 1,
        "sha256_of_decimal":
            hashlib.sha256(b"1").hexdigest(),
    }
    recut["corrected_v1_image_recut_count"] = one
    recut["corrected_v1_image_recut_rank_range"] = [0, "0"]
    recut["corrected_v1_last_image_recut_rank"] = "0"
    recut_payload = {
        "connected_interval_id":
            coordinated["boundary_and_physical_branch_proof"][
                "connected_interval_id"
            ],
        "adapted_length_outer": recut["formal_adapted_length_outer"],
        "scale": recut["deterministic_recut_scale"],
        "count": "1",
        "rank_range": [0, "0"],
    }
    recut["corrected_v1_image_recut_registry_id"] = (
        "round145-v1-image-recut-registry:" + digest(recut_payload)
    )
    try:
        validate_result(coordinated)
    except Exception:
        rejected += 1
    else:
        raise RuntimeError(
            "semantic mutation accepted:coordinated_recut"
        )
    return {
        "attack_count": len(attacks) + 1,
        "rejected_count": rejected,
    }


def strict_json_self_test() -> dict[str, Any]:
    payloads = [
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
        '{"a":-Infinity}',
        '{"a":1.0}',
        '{"a":1e999}',
        "[]",
        '{"a":' + "1" * (MAX_JSON_INTEGER_DIGITS + 1) + "}",
        "null",
    ]
    rejected = 0
    with tempfile.TemporaryDirectory(prefix="cm2-r145-json-") as directory:
        root = Path(directory)
        for index, payload in enumerate(payloads):
            path = root / f"attack-{index}.json"
            path.write_text(payload, encoding="utf-8")
            try:
                strict_json(path)
            except Exception:
                rejected += 1
            else:
                raise RuntimeError(f"strict JSON accepted:{index}")
    return {"attack_count": len(payloads), "rejected_count": rejected}


def same_precision_clean_replay(certificate: Path) -> dict[str, Any]:
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer pin")
    with tempfile.TemporaryDirectory(prefix="cm2-r145-replay-") as directory:
        replay = Path(directory) / "replay.json"
        environment = dict(os.environ)
        environment.update({
            "PYTHONHASHSEED": "987654321",
            "LC_ALL": "C",
            "TZ": "UTC",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(HERE),
        })
        completed = subprocess.run(
            [
                sys.executable,
                str(PRODUCER),
                "--precision-bits",
                str(PRIMARY_PRECISION_BITS),
                "--output",
                str(replay),
            ],
            cwd=HERE.parent,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=7200,
            check=False,
        )
        require(
            completed.returncode == 0
            and replay.exists()
            and replay.read_bytes() == certificate.read_bytes(),
            "same-precision producer byte replay",
        )
        stdout_rows = [
            json.loads(line)
            for line in completed.stdout.splitlines()
            if line.startswith("{")
        ]
        require(
            len(stdout_rows) == 1
            and stdout_rows[0]["schema"] == CERTIFICATE_SCHEMA
            and stdout_rows[0]["result_sha256"]
            == CERTIFICATE_RESULT_SHA256
            and completed.stderr == "",
            "same-precision producer process envelope",
        )
        return {
            "precision_bits": PRIMARY_PRECISION_BITS,
            "hash_seed": 987654321,
            "exit_code": completed.returncode,
            "byte_identical": True,
            "stdout_schema": stdout_rows[0]["schema"],
            "stdout_result_sha256": stdout_rows[0]["result_sha256"],
            "stderr_empty": True,
        }


def cross_precision_projection(result: dict[str, Any]) -> dict[str, Any]:
    projection = copy.deepcopy(result)
    projection.pop("generation_precision_bits")
    atlas = projection["finite_connected_atlas"]
    for row in atlas["regular_dyadic_cells"]:
        row.pop("model_radius_ledger_sha256")
    atlas["clipped_endpoint_cell"].pop("model_radius_ledger_sha256")
    return projection


def model_radius_ledger_hashes(result: dict[str, Any]) -> list[str]:
    atlas = result["finite_connected_atlas"]
    return [
        *[
            row["model_radius_ledger_sha256"]
            for row in atlas["regular_dyadic_cells"]
        ],
        atlas["clipped_endpoint_cell"]["model_radius_ledger_sha256"],
    ]


def cross_precision_contract(
    primary_result: dict[str, Any],
    secondary_result: dict[str, Any],
) -> dict[str, Any]:
    primary_projection = cross_precision_projection(primary_result)
    secondary_projection = cross_precision_projection(secondary_result)
    primary_projection_bytes = canonical(primary_projection).encode("utf-8")
    secondary_projection_bytes = canonical(secondary_projection).encode(
        "utf-8"
    )
    require(
        primary_projection_bytes == secondary_projection_bytes,
        "cross-precision exact stable projection",
    )
    primary_ledgers = model_radius_ledger_hashes(primary_result)
    secondary_ledgers = model_radius_ledger_hashes(secondary_result)
    require(
        len(primary_ledgers) == 13
        and len(secondary_ledgers) == 13
        and all(
            type(value) is str
            and len(value) == 64
            and set(value) <= set("0123456789abcdef")
            for value in primary_ledgers + secondary_ledgers
        ),
        "cross-precision model-radius ledgers",
    )
    changed = sum(
        primary != secondary
        for primary, secondary in zip(primary_ledgers, secondary_ledgers)
    )
    require(changed == 13, "expected precision-specific ledger split")
    return {
        "primary_generation_precision_bits": PRIMARY_PRECISION_BITS,
        "secondary_generation_precision_bits": SECONDARY_PRECISION_BITS,
        "stable_projection_byte_exact": True,
        "stable_projection_sha256":
            hashlib.sha256(primary_projection_bytes).hexdigest(),
        "precision_specific_model_radius_ledger_count": 13,
        "precision_specific_model_radius_ledger_changed_count": changed,
        "model_radius_ledger_pair_sha256":
            digest(list(zip(primary_ledgers, secondary_ledgers))),
        "all_topology_faces_paths_radii_margins_derivatives_ranks_ids_exact":
            True,
    }


def validate_secondary_replay(
    primary_result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        sha256(SECONDARY_CERTIFICATE) == SECONDARY_CERTIFICATE_SHA256,
        "secondary certificate pin",
    )
    document = strict_json(SECONDARY_CERTIFICATE)
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and document["result_sha256"]
        == SECONDARY_CERTIFICATE_RESULT_SHA256
        and digest(document["result"])
        == SECONDARY_CERTIFICATE_RESULT_SHA256,
        "closed secondary replay envelope",
    )
    validate_result(document["result"], SECONDARY_PRECISION_BITS)
    contract = cross_precision_contract(
        primary_result,
        document["result"],
    )
    return document, contract


def cross_precision_attack_suite(
    primary_result: dict[str, Any],
    secondary_result: dict[str, Any],
) -> dict[str, Any]:
    attacks = [
        (
            "generation",
            ("generation_precision_bits",),
            PRIMARY_PRECISION_BITS,
        ),
        (
            "radius",
            (
                "finite_connected_atlas",
                "regular_dyadic_cells",
                0,
                "maximum_state_radius_strict_upper_power_of_two_exponent",
            ),
            -9,
        ),
        (
            "witness",
            (
                "finite_connected_atlas",
                "regular_dyadic_cells",
                1,
                "maximum_state_radius_witness",
            ),
            [0, 0, 0],
        ),
        (
            "terminal_outer",
            (
                "finite_connected_atlas",
                "clipped_endpoint_cell",
                "terminal_p_outer",
                0,
            ),
            "0",
        ),
        (
            "interval_id",
            (
                "boundary_and_physical_branch_proof",
                "connected_interval_id",
            ),
            "bad",
        ),
        (
            "precision_specific_ledger",
            (
                "finite_connected_atlas",
                "regular_dyadic_cells",
                0,
                "model_radius_ledger_sha256",
            ),
            primary_result["finite_connected_atlas"][
                "regular_dyadic_cells"
            ][0]["model_radius_ledger_sha256"],
        ),
        (
            "numeric_type",
            (
                "finite_connected_atlas",
                "regular_dyadic_cell_count",
            ),
            12.0,
        ),
    ]
    rejected = 0
    for name, path, replacement in attacks:
        candidate = mutate_at(secondary_result, path, replacement)
        try:
            validate_result(candidate, SECONDARY_PRECISION_BITS)
            cross_precision_contract(primary_result, candidate)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(
                f"cross-precision mutation accepted:{name}"
            )
    return {"attack_count": len(attacks), "rejected_count": rejected}


def protected_paths() -> set[Path]:
    return {
        VERIFIER.resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        SECONDARY_CERTIFICATE.resolve(),
        *((HERE / name).resolve() for name in INPUT_PINS),
    }


def validate_output_target(path: Path) -> Path:
    absolute = path.absolute()
    parent = absolute.parent
    require(
        absolute.name not in {"", ".", ".."}
        and parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "safe output parent",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    require(resolved not in protected_paths(), "output aliases input")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "safe existing output",
        )
    return absolute


def path_safety_self_test() -> dict[str, Any]:
    rejected = 0
    attacks = 0
    with tempfile.TemporaryDirectory(prefix="cm2-r145-path-") as directory:
        root = Path(directory)
        ordinary = root / "ordinary.json"
        ordinary.write_text("sentinel", encoding="utf-8")
        require(validate_output_target(ordinary) == ordinary, "ordinary output")
        targets = [
            PRODUCER,
            CERTIFICATE,
            SECONDARY_CERTIFICATE,
            VERIFIER,
        ]
        for index, target in enumerate(targets):
            attacks += 1
            try:
                validate_output_target(target)
            except Exception:
                rejected += 1
            else:
                raise RuntimeError(f"protected path accepted:{index}")
        symlink = root / "symlink.json"
        symlink.symlink_to(ordinary)
        attacks += 1
        try:
            validate_output_target(symlink)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("symlink output accepted")
        hardlink = root / "hardlink.json"
        os.link(ordinary, hardlink)
        attacks += 1
        try:
            validate_output_target(hardlink)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("hardlink output accepted")
        attacks += 1
        try:
            validate_output_target(root / "missing" / "x.json")
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("missing parent accepted")
    return {"attack_count": attacks, "rejected_count": rejected}


def build_verification(certificate_path: Path) -> dict[str, Any]:
    require(
        certificate_path.resolve() == CERTIFICATE.resolve(),
        "canonical certificate only",
    )
    require(
        sha256(certificate_path) == CERTIFICATE_SHA256,
        "certificate pin",
    )
    document = strict_json(certificate_path)
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and document["result_sha256"] == CERTIFICATE_RESULT_SHA256
        and digest(document["result"]) == CERTIFICATE_RESULT_SHA256,
        "closed certificate envelope",
    )
    validate_result(document["result"])
    semantic = semantic_attack_suite(document["result"])
    secondary, cross_precision = validate_secondary_replay(
        document["result"]
    )
    cross_attacks = cross_precision_attack_suite(
        document["result"],
        secondary["result"],
    )
    parser = strict_json_self_test()
    path = path_safety_self_test()
    replay = same_precision_clean_replay(certificate_path)
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "secondary_certificate_sha256":
            SECONDARY_CERTIFICATE_SHA256,
        "secondary_certificate_result_sha256":
            SECONDARY_CERTIFICATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "independent_checks": {
            "closed_dependency_count": len(INPUT_PINS),
            "regular_cell_count": 12,
            "clipped_endpoint_cell_count": 1,
            "exact_shared_face_count": 12,
            "collision_stage_cell_pair_count": 13 * RETURN_DEPTH,
            "radius4_candidate_test_count": 13 * RETURN_DEPTH * 161,
            "precision_stable_atlas_identity_recomputed": True,
            "independent_Round137_rank_algebra": True,
            "independent_short_cell_and_recut_algebra": True,
            "historical_null_and_global_nonpromotion": True,
        },
        "semantic_attack_suite": semantic,
        "cross_precision_attack_suite": cross_attacks,
        "strict_json_attack_suite": parser,
        "path_safety_attack_suite": path,
        "cross_precision_replay": cross_precision,
        "same_precision_clean_replay": replay,
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    target = validate_output_target(path)
    payload = json.dumps(
        value,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build_verification(args.certificate)
    atomic_write(args.output, document)
    print(canonical({
        "schema": document["schema"],
        "result_sha256": document["result_sha256"],
        "output": str(args.output.absolute()),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
