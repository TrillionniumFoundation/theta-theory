#!/usr/bin/env python3
"""Round145: finite connected atlas for the complete R1648 leaf corridor.

The Round143 terminal face and the Round139/R141 D0 boundary are joined by
twelve exact dyadic cells at adaptive widths and one clipped endpoint cell,
where

    lambda = (x_star - x) 2^4289.

Every atlas cell uses the recentered two-generator affine state model and
repeats all 1648 retained/radius-four owner decisions, official words,
charts, homogeneity/incidence labels and C24 decisions.  The D0 candidate is
an analytic double-root boundary only on cell zero.  On every translated
cell it is audited as the ordinary strict miss that it actually is.

The clipped cell is allowed to straddle the unique Round143 terminal
p=-1/50 face.  Its first 1647 stages are strict nonreturns, its entire owner
and official-word path is strict, and Round143's monotone root proof selects
the returning side.  Exact shared faces make the physical open interval a
connected fixed-itinerary branch.

The result promotes coordinate-explicit Round137-v1 leaf and deterministic
recut data.  It does not invent any unnamed historical Round27/Round35 ID.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import multiprocessing
import os
import stat
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as engine
import cm2_round145_leaf_corridor_atlas_spike as atlas_engine


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE / "cm2-round145-finite-connected-leaf-corridor-atlas-2026-07-24.json"
)
FUTURE_VERIFIER = (
    HERE / "cm2_round145_finite_connected_leaf_corridor_atlas_verifier.py"
)
SCHEMA = "cm2.round145.finite-connected-leaf-corridor-atlas.v1"
PRIMARY_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
RETURN_DEPTH = 1648
LAMBDA_SCALE_POWER = 4289
DYADIC_CELL_POWER = 4292
REGULAR_CELL_SPECS = (
    *((4292, index) for index in range(8)),
    *((4294, index) for index in range(32, 36)),
)
REGULAR_CELL_COUNT = len(REGULAR_CELL_SPECS)

ENGINE = HERE / "cm2_round141_centered_affine_d0_collar_spike.py"
ATLAS_ENGINE = HERE / "cm2_round145_leaf_corridor_atlas_spike.py"
R139_CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
R141_SOURCE = (
    HERE / "cm2_round141_recentered_affine_k4296_d0_collar_return.py"
)
R141_CERTIFICATE = (
    HERE / "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json"
)
R141_VERIFIER = (
    HERE / "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
)
R141_VERIFICATION = (
    HERE
    / "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json"
)
R141_MANIFEST = (
    HERE
    / "cm2-round141-recentered-affine-k4296-d0-collar-return-manifest-2026-07-24.sha256"
)
R143_SOURCE = (
    HERE / "cm2_round143_r1648_terminal_face_endpoint_recut_frontier.py"
)
R143_CERTIFICATE = (
    HERE / "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json"
)
R143_VERIFIER = (
    HERE / "cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py"
)
R143_VERIFICATION = (
    HERE
    / "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-verification-2026-07-24.json"
)
R143_MANIFEST = (
    HERE / "cm2-one-hundred-forty-third-direct-assault-manifest-2026-07-24.sha256"
)

PINS = {
    ENGINE.name:
        "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1",
    ATLAS_ENGINE.name:
        "c2bf266f715a8214a13f87308dd9c982e520b39a2747e23fedc1c7955fd62c78",
    R139_CERTIFICATE.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    R141_SOURCE.name:
        "687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28",
    R141_CERTIFICATE.name:
        "a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe",
    R141_VERIFIER.name:
        "1bb85fdd8dc22aa941084666b5eb9c41154f9e890f6d87c42eaf8808a4748f65",
    R141_VERIFICATION.name:
        "43770a85918cd4986e232cc1e3c401bae9ff8d0ee772b92eea8c46c3c55d4e3c",
    R141_MANIFEST.name:
        "06351a018876a3ec96cc099b9fd44d779c8a533543c7f7cb75379181dc32de52",
    R143_SOURCE.name:
        "bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38",
    R143_CERTIFICATE.name:
        "74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67",
    R143_VERIFIER.name:
        "197be350c4a6bed80a1c413822c5b838c2d0bc7da88360998fd7ad939da85601",
    R143_VERIFICATION.name:
        "3ee6fe0e48bdf05a6f76726ded302aa4d632c306a4a260f444e1c2a66dfd9bd7",
    R143_MANIFEST.name:
        "f8215c273ff1a7b9cd01c5f53abae3f6ab03907a5795a6aecaab864129ac6e22",
}

CLOSED = {
    R141_CERTIFICATE.name: (
        "cm2.round141.recentered-affine-k4296-d0-collar-return.v1",
        "48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f",
    ),
    R141_VERIFICATION.name: (
        "cm2.round141.recentered-affine-k4296-d0-collar-return-verification.v1",
        "8c94e2f846062cae13be0d9fb8520877cb6de7903354090df87ad084d74153a4",
    ),
    R143_CERTIFICATE.name: (
        "cm2.round143.r1648-terminal-face-endpoint-recut-frontier.v1",
        "35a9f8e0437086a2feaf294c10c621ce21319dc93aac88f33dbc4024e4507e92",
    ),
    R143_VERIFICATION.name: (
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


def qstr(value: Q | int) -> str:
    return r139.qstr(Q(value))


def strict_json(path: Path) -> dict[str, Any]:
    return r139.strict_json(path)


def validate_dependencies() -> dict[str, dict[str, Any]]:
    paths = (
        ENGINE,
        ATLAS_ENGINE,
        R139_CERTIFICATE,
        R141_SOURCE,
        R141_CERTIFICATE,
        R141_VERIFIER,
        R141_VERIFICATION,
        R141_MANIFEST,
        R143_SOURCE,
        R143_CERTIFICATE,
        R143_VERIFIER,
        R143_VERIFICATION,
        R143_MANIFEST,
    )
    require(set(PINS) == {path.name for path in paths}, "complete dependency pins")
    closed: dict[str, dict[str, Any]] = {}
    for path in paths:
        require(sha256(path) == PINS[path.name], f"dependency pin:{path.name}")
        if path.name not in CLOSED:
            continue
        document = strict_json(path)
        schema, result_sha = CLOSED[path.name]
        require(
            result_sha is not None
            and document["schema"] == schema
            and document["result_sha256"] == result_sha
            and digest(document["result"]) == result_sha,
            f"closed dependency:{path.name}",
        )
        closed[path.name] = document["result"]
    require(
        closed[R141_CERTIFICATE.name]["status"]
        == "CERTIFIED_RECENTERED_AFFINE_K4296_D0_COLLAR_STRICT_R1648_RETURN"
        and closed[R141_VERIFICATION.name]["status"] == "PASS"
        and closed[R143_CERTIFICATE.name]["status"]
        == "CERTIFIED_LOCAL_R1648_TERMINAL_FACE_ENDPOINT_WITH_PROSPECTIVE_RECUT_FRONTIER"
        and closed[R143_VERIFICATION.name]["status"] == "PASS",
        "dependency statuses",
    )
    return closed


def _one_json_summary(capture: str) -> dict[str, Any]:
    rows = [line for line in capture.splitlines() if line.startswith("{")]
    require(len(rows) == 1, "one replay summary")
    return json.loads(rows[0])


def lambda_bounds(power: int, cell_index: int) -> tuple[Q, Q]:
    denominator = 2 ** (power - LAMBDA_SCALE_POWER)
    return Q(cell_index, denominator), Q(cell_index + 1, denominator)


def _cell_worker(
    arguments: tuple[int, int, int, int],
) -> tuple[int, dict[str, Any]]:
    atlas_index, power, cell_index, precision = arguments
    ctx.prec = precision
    capture = io.StringIO()
    if atlas_index > 0:
        r139.candidates_owner_excluding_anchor = (
            atlas_engine.translated_anchor_audit()
        )
    try:
        with contextlib.redirect_stdout(capture):
            engine.run(
                power,
                precision,
                False,
                True,
                cell_index,
            )
    finally:
        r139.candidates_owner_excluding_anchor = (
            atlas_engine.ORIGINAL_ANCHOR_AUDIT
        )
    summary = _one_json_summary(capture.getvalue())
    bounds = lambda_bounds(power, cell_index)
    summary["terminal_derivative_audit"] = (
        atlas_engine.terminal_derivative_audit(
            bounds[0], bounds[1], precision
        )
    )
    return atlas_index, summary


def _endpoint_worker(
    arguments: tuple[str, str, int],
) -> dict[str, Any]:
    lower_text, upper_text, precision = arguments
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        atlas_engine.endpoint_complete_audit(
            Q(lower_text),
            Q(upper_text),
            LAMBDA_SCALE_POWER,
            precision,
        )
    summary = _one_json_summary(capture.getvalue())
    summary["terminal_derivative_audit"] = (
        atlas_engine.terminal_derivative_audit(
            Q(lower_text), Q(upper_text), precision
        )
    )
    return summary


def replay_atlas(
    endpoint_bracket: tuple[Q, Q],
    precision: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(
        type(precision) is int and precision >= PRIMARY_PRECISION_BITS,
        "replay precision",
    )
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(
        max_workers=REGULAR_CELL_COUNT + 1,
        mp_context=context,
    ) as executor:
        endpoint_future = executor.submit(
            _endpoint_worker,
            (
                qstr(Q(9, 8)),
                qstr(endpoint_bracket[1]),
                precision,
            ),
        )
        cell_pairs = list(executor.map(
            _cell_worker,
            [
                (atlas_index, power, cell_index, precision)
                for atlas_index, (power, cell_index)
                in enumerate(REGULAR_CELL_SPECS)
            ],
        ))
        endpoint = endpoint_future.result()
    cells = [row for _index, row in sorted(cell_pairs)]
    return cells, endpoint


def validate_replay(
    cells: list[dict[str, Any]],
    endpoint: dict[str, Any],
) -> None:
    require(len(cells) == REGULAR_CELL_COUNT, "regular atlas cells")
    for atlas_index, (row, spec) in enumerate(
        zip(cells, REGULAR_CELL_SPECS)
    ):
        power, cell_index = spec
        derivative = row["terminal_derivative_audit"]
        require(
            row["status"] == "FEASIBLE"
            and row["power"] == power
            and row["cell_index"] == cell_index
            and row["collision_count"] == RETURN_DEPTH
            and row["complete_audit"] is True
            and row["official_sequence_sha256"]
            == r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
            and row["compact_rows_sha256"]
            == r139.EXPECTED_COMPACT_PATH_SHA256
            and row["homogeneity_histogram"] == {"H0_CENTRAL": RETURN_DEPTH}
            and row["incidence_histogram"] == {"14": RETURN_DEPTH}
            and row[
                "maximum_state_radius_strict_upper_power_of_two_exponent"
            ] <= -10
            and row[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ][2] <= -10
            and derivative["terminal_p_derivative_lambda_sign"] == -1
            and derivative[
                "terminal_image_derivative_lambda_sign"
            ] == -1
            and derivative["terminal_t_strictly_inside_asin_domain"] is True
            and derivative["terminal_p_strictly_inside_asin_domain"] is True,
            f"regular cell replay:{atlas_index}",
        )
    endpoint_derivative = endpoint["terminal_derivative_audit"]
    require(
        endpoint["status"] == "FEASIBLE_ENDPOINT_FACE_CELL"
        and endpoint["collision_count"] == RETURN_DEPTH
        and endpoint["complete_audit"] is True
        and endpoint["ordinary_D0_strict_miss"] is True
        and endpoint["official_sequence_sha256"]
        == r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and endpoint["physical_interior_compact_rows_sha256"]
        == r139.EXPECTED_COMPACT_PATH_SHA256
        and endpoint["homogeneity_histogram"]
        == {"H0_CENTRAL": RETURN_DEPTH}
        and endpoint["incidence_histogram"] == {"14": RETURN_DEPTH}
        and endpoint["preterminal_strict_nonreturn_count"]
        == RETURN_DEPTH - 1
        and endpoint["terminal_box_classification"]
        == "UNRESOLVED_TIME3_OUTER"
        and endpoint["terminal_only_active_face"] == "p=-1/50"
        and endpoint[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ] <= -10,
        "clipped endpoint replay",
    )
    require(
        endpoint_derivative["terminal_p_derivative_lambda_sign"] == -1
        and endpoint_derivative[
            "terminal_image_derivative_lambda_sign"
        ] == -1
        and endpoint_derivative[
            "terminal_t_strictly_inside_asin_domain"
        ] is True
        and endpoint_derivative[
            "terminal_p_strictly_inside_asin_domain"
        ] is True,
        "clipped endpoint replay",
    )


def compact_replay(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "atlas_index": atlas_index,
            "power": power,
            "cell_index": row["cell_index"],
            "lambda_bounds": [
                qstr(value)
                for value in lambda_bounds(power, row["cell_index"])
            ],
            "D0_collision3_mode": (
                "analytic_double_root_only_at_lambda_zero"
                if atlas_index == 0
                else "ordinary_strict_radius4_miss"
            ),
            "model_radius_ledger_sha256":
                row["model_radius_ledger_sha256"],
            "maximum_state_radius_strict_upper_power_of_two_exponent":
                row[
                    "maximum_state_radius_strict_upper_power_of_two_exponent"
                ],
            "maximum_state_radius_witness":
                row["maximum_state_radius_witness"],
            "terminal_state_radius_strict_upper_power_of_two_exponents":
                row[
                    "terminal_state_radius_strict_upper_power_of_two_exponents"
                ],
            "worst_decision_margin_dyadic_depth":
                row["ledger_worst_depth"],
            "worst_decision_margin_names":
                row["ledger_worst_names"],
            "official_sequence_sha256":
                row["official_sequence_sha256"],
            "compact_path_sha256": row["compact_rows_sha256"],
            "terminal_p_derivative_lambda_sign":
                row["terminal_derivative_audit"][
                    "terminal_p_derivative_lambda_sign"
                ],
            "terminal_p_derivative_margin_dyadic_depth":
                row["terminal_derivative_audit"][
                    "terminal_p_derivative_lambda_margin_dyadic_depth"
                ],
            "terminal_image_derivative_lambda_sign":
                row["terminal_derivative_audit"][
                    "terminal_image_derivative_lambda_sign"
                ],
            "terminal_image_derivative_margin_dyadic_depth":
                row["terminal_derivative_audit"][
                    "terminal_image_derivative_lambda_margin_dyadic_depth"
                ],
        }
        for atlas_index, (row, (power, _cell_index))
        in enumerate(zip(rows, REGULAR_CELL_SPECS))
    ]


def build(precision_bits: int = PRIMARY_PRECISION_BITS) -> dict[str, Any]:
    require(
        type(precision_bits) is int
        and precision_bits >= PRIMARY_PRECISION_BITS,
        "producer precision",
    )
    closed = validate_dependencies()
    r141_result = closed[R141_CERTIFICATE.name]
    r143_result = closed[R143_CERTIFICATE.name]
    endpoint_bracket = tuple(
        Q(value)
        for value in r143_result["terminal_face_endpoint"]["lambda_bracket"]
    )
    require(
        Q(9, 8) < endpoint_bracket[0] < endpoint_bracket[1] < Q(5, 4),
        "endpoint after dyadic atlas",
    )
    cells, endpoint = replay_atlas(endpoint_bracket, precision_bits)
    validate_replay(cells, endpoint)
    compact_cells = compact_replay(cells)
    faces = [
        {
            "face_index": index,
            "lambda": compact_cells[index]["lambda_bounds"][0],
            "left_cell": index - 1,
            "right_cell": index,
            "exactly_shared": True,
            "same_parameter_substitution_into_exact_initial_leaf_map": True,
            "same_1648_selected_collision_map_composition": True,
        }
        for index in range(1, REGULAR_CELL_COUNT)
    ]
    faces.append({
        "face_index": REGULAR_CELL_COUNT,
        "lambda": qstr(Q(9, 8)),
        "left_cell": REGULAR_CELL_COUNT - 1,
        "right_cell": "clipped_endpoint_cell",
        "exactly_shared": True,
        "same_parameter_substitution_into_exact_initial_leaf_map": True,
        "same_1648_selected_collision_map_composition": True,
    })
    precision_stable_atlas_identity = {
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
            for row in compact_cells
        ],
        "clipped_endpoint_cell": {
            "lambda_bounds": [
                qstr(Q(9, 8)),
                qstr(endpoint_bracket[1]),
            ],
            "ordinary_D0_collision3_strict_miss": True,
            "official_sequence_sha256":
                endpoint["official_sequence_sha256"],
            "physical_interior_compact_path_sha256":
                endpoint["physical_interior_compact_rows_sha256"],
            "terminal_only_active_face": "G:S p=-1/50",
            "terminal_p_derivative_lambda_sign": -1,
            "terminal_image_derivative_lambda_sign": -1,
        },
        "internal_shared_faces": faces,
        "cell_adjacency_graph": "path_on_13_vertices",
    }
    precision_stable_atlas_identity_sha256 = digest(
        precision_stable_atlas_identity
    )
    interval_payload = {
        "Round143_prospective_interval_id":
            r143_result["candidate_full_leaf_interval"][
                "prospective_interval_id"
            ],
        "lambda_scale_power": LAMBDA_SCALE_POWER,
        "right_boundary": "lambda=0 collision3 D0 tangency",
        "left_boundary_bracket": [
            qstr(value) for value in endpoint_bracket
        ],
        "owner_sequence_sha256":
            r139.EXPECTED_OWNER_SEQUENCE_SHA256,
        "official_sequence_sha256":
            r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256,
        "precision_stable_atlas_identity_sha256":
            precision_stable_atlas_identity_sha256,
    }
    interval_id = (
        "round145-v1-connected-physical-r1648-leaf:"
        + digest(interval_payload)
    )
    rank_source = r143_result[
        "coordinate_explicit_Round137_v1_leaf_ranks"
    ]
    canonical_rank = rank_source["canonical_H1_x_candidate"]
    normalized_rank = rank_source["Round140_normalized_t_candidate"]
    require(
        canonical_rank[
            "least_Round137_v1_rank_for_this_declared_coordinate_interval"
        ] is True
        and canonical_rank["contained_primitive_basis_row"][0] == 4290
        and normalized_rank[
            "least_Round137_v1_rank_for_this_declared_coordinate_interval"
        ] is True
        and normalized_rank["contained_primitive_basis_row"][0] == 4283,
        "Round143 coordinate ranks",
    )
    recut_source = r143_result["formal_image_recut_frontier"]
    mesh_source = r143_result["B14_source_mesh_frontier"]
    recut_payload = {
        "connected_interval_id": interval_id,
        "adapted_length_outer":
            recut_source["formal_adapted_length_outer"],
        "scale": recut_source["deterministic_recut_scale"],
        "count": recut_source["conditional_image_recut_count"]["decimal"],
        "rank_range":
            recut_source["conditional_image_recut_rank_range"],
    }
    result = {
        "status":
            "CERTIFIED_FINITE_CONNECTED_R1648_PHYSICAL_LEAF_CORRIDOR_ATLAS",
        "generation_precision_bits": precision_bits,
        "minimum_certified_precision_bits": PRIMARY_PRECISION_BITS,
        "secondary_verifier_precision_bits": SECONDARY_PRECISION_BITS,
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_Round141_Round143_files_modified": False,
        },
        "scaled_leaf_coordinate": {
            "coordinate": "lambda=(x_star-x)*2^4289",
            "orientation": "increasing from D0 boundary toward terminal face",
            "scale_power": LAMBDA_SCALE_POWER,
            "physical_open_interval":
                "0 < lambda < lambda_terminal",
            "terminal_lambda_bracket": [
                qstr(value) for value in endpoint_bracket
            ],
        },
        "finite_connected_atlas": {
            "regular_dyadic_cell_count": REGULAR_CELL_COUNT,
            "coarse_K4292_cell_count": 8,
            "refined_K4294_terminal_tail_cell_count": 4,
            "clipped_endpoint_cell_count": 1,
            "total_cell_count": REGULAR_CELL_COUNT + 1,
            "coarse_cell_width_lambda": "1/8",
            "coarse_cell_width_x": "2^-4292",
            "refined_tail_cell_width_lambda": "1/32",
            "refined_tail_cell_width_x": "2^-4294",
            "reason_for_terminal_tail_refinement":
                "the single K4292 [1,9/8] enclosure left terminal C24 unresolved; four K4294 cells give strict return through 9/8",
            "precision_stable_identity_sha256":
                precision_stable_atlas_identity_sha256,
            "model_radius_ledger_contract":
                "generation-precision-specific evidence excluded from the branch identity",
            "regular_dyadic_cells": compact_cells,
            "clipped_endpoint_cell": {
                "lambda_bounds": [
                    qstr(Q(9, 8)),
                    qstr(endpoint_bracket[1]),
                ],
                "contains_unique_Round143_terminal_face_root": True,
                "ordinary_D0_collision3_strict_miss": True,
                "model_radius_ledger_sha256":
                    endpoint["model_radius_ledger_sha256"],
                "maximum_state_radius_strict_upper_power_of_two_exponent":
                    endpoint[
                        "maximum_state_radius_strict_upper_power_of_two_exponent"
                    ],
                "maximum_state_radius_witness":
                    endpoint["maximum_state_radius_witness"],
                "terminal_state_radius_strict_upper_power_of_two_exponents":
                    endpoint[
                        "terminal_state_radius_strict_upper_power_of_two_exponents"
                    ],
                "official_sequence_sha256":
                    endpoint["official_sequence_sha256"],
                "physical_interior_compact_path_sha256":
                    endpoint["physical_interior_compact_rows_sha256"],
                "closed_box_compact_path_sha256":
                    endpoint["raw_box_compact_rows_sha256"],
                "preterminal_strict_nonreturn_count":
                    endpoint["preterminal_strict_nonreturn_count"],
                "terminal_closed_box_classification":
                    endpoint["terminal_box_classification"],
                "terminal_only_active_face":
                    "G:S p=-1/50",
                "terminal_p_outer":
                    endpoint["terminal_p_fixed_dyadic_outer"],
                "terminal_normal_y_outer":
                    endpoint["terminal_normal_y_fixed_dyadic_outer"],
                "terminal_normal_x_outer":
                    endpoint["terminal_normal_x_fixed_dyadic_outer"],
                "terminal_p_derivative_lambda_sign": -1,
                "terminal_p_derivative_margin_dyadic_depth":
                    endpoint["terminal_derivative_audit"][
                        "terminal_p_derivative_lambda_margin_dyadic_depth"
                    ],
                "terminal_image_derivative_lambda_sign": -1,
                "terminal_image_derivative_margin_dyadic_depth":
                    endpoint["terminal_derivative_audit"][
                        "terminal_image_derivative_lambda_margin_dyadic_depth"
                    ],
            },
            "internal_shared_faces": faces,
            "all_internal_faces_exactly_shared": True,
            "shared_face_identity_contract":
                "adjacent closed cells substitute the same exact lambda face and D0-root generator into the same analytic initial leaf map and the same 1648 selected-circle composition",
            "cell_adjacency_graph": "path_on_13_vertices",
            "cell_adjacency_graph_connected": True,
            "same_exact_fixed_s_slope4_leaf": True,
            "same_1648_owner_sequence_on_every_cell": True,
            "same_1648_official_word_sequence_on_every_cell": True,
            "same_H0_homogeneity_on_every_stage": True,
            "same_incidence_rank_14_on_every_stage": True,
        },
        "boundary_and_physical_branch_proof": {
            "right_boundary":
                "Round139 collision3 D0 double-root at lambda=0",
            "D0_strict_miss_for_every_positive_lambda_cell": True,
            "left_boundary":
                "Round143 unique terminal G:S p=-1/50 root",
            "Round143_terminal_root_derivative_strictly_negative": True,
            "Round143_terminal_root_unique_in_bracket": True,
            "first_1647_collisions_strict_nonreturn_on_whole_atlas": True,
            "collision_1648_strict_return_on_lambda_below_root": True,
            "collision_1648_exits_only_through_terminal_p_face_at_root": True,
            "terminal_p_strictly_decreasing_on_every_atlas_cell": True,
            "no_owner_word_chart_homogeneity_or_incidence_boundary_inside":
                True,
            "connected_physical_open_branch_certified": True,
            "maximal_for_frozen_itinerary_and_destination_core_on_this_leaf":
                True,
            "global_two_dimensional_component_maximality_certified": False,
            "connected_interval_id": interval_id,
            "payload_sha256": digest(interval_payload),
        },
        "promoted_Round137_v1_leaf_rank": {
            "coordinate_contract":
                "round137-dyadic-basis-enumeration-v1",
            "canonical_coordinate": "x=sqrt(17)*r",
            "canonical_H1_x_least_rank": canonical_rank,
            "normalized_t_cross_check": normalized_rank,
            "canonical_H1_x_level": 4290,
            "normalized_t_level": 4283,
            "rank_is_for_certified_connected_physical_branch": True,
            "historical_Round35_coordinate_crosswalk_available": False,
            "historical_Round35_source_interval_rank": None,
        },
        "promoted_v1_source_short_cell": {
            "connected_interval_id": interval_id,
            "adapted_line_element":
                r143_result["candidate_full_leaf_interval"][
                    "source_adapted_line_element"
                ],
            "adapted_length_outer":
                r143_result["candidate_full_leaf_interval"][
                    "source_adapted_length_outer"
                ],
            "below_delta_14": True,
            "below_1e_minus_90": True,
            "corrected_left_anchored_natural_short_cell_k": 0,
            "corrected_v1_source_cell_id":
                "round145-v1-source-short-cell:" + digest({
                    "interval": interval_id,
                    "k": 0,
                    "scale": "1e-90",
                }),
            "historical_Round35_natural_short_cell_k": None,
            "historical_Round35_parent_W_id": None,
            "Round143_mesh_cross_check_sha256": digest(mesh_source),
        },
        "promoted_v1_image_recut": {
            "connected_source_branch_certified": True,
            "continuous_return_image_of_connected_branch": True,
            "image_is_one_connected_interval": True,
            "image_observable": "asin(t_1648)+asin(p_1648)",
            "image_observable_strictly_decreasing_on_every_atlas_cell": True,
            "image_observable_shared_face_continuity_exact": True,
            "no_internal_image_extremum": True,
            "endpoint_difference_is_complete_image_span": True,
            "adapted_length_endpoint_formula":
                recut_source["adapted_length_endpoint_formula"],
            "formal_adapted_length_outer":
                recut_source["formal_adapted_length_outer"],
            "deterministic_recut_scale":
                recut_source["deterministic_recut_scale"],
            "corrected_v1_image_recut_count":
                recut_source["conditional_image_recut_count"],
            "corrected_v1_image_recut_rank_range":
                recut_source["conditional_image_recut_rank_range"],
            "corrected_v1_first_image_recut_rank": 0,
            "corrected_v1_last_image_recut_rank":
                recut_source["conditional_last_image_recut_rank"],
            "corrected_v1_image_recut_registry_id":
                "round145-v1-image-recut-registry:"
                + digest(recut_payload),
            "Round143_prospective_registry_id":
                recut_source["prospective_recut_registry_id"],
            "historical_Round35_image_recut_rank": None,
            "historical_Round35_restriction_id": None,
        },
        "count_ledger": {
            "atlas_cell_count": REGULAR_CELL_COUNT + 1,
            "exact_internal_shared_face_count": REGULAR_CELL_COUNT,
            "collision_stage_cell_pairs":
                (REGULAR_CELL_COUNT + 1) * RETURN_DEPTH,
            "full_radius4_candidate_test_count":
                (REGULAR_CELL_COUNT + 1) * RETURN_DEPTH * 161,
            "preterminal_strict_nonreturn_cell_stage_pairs":
                (REGULAR_CELL_COUNT + 1) * (RETURN_DEPTH - 1),
            "coordinate_explicit_v1_leaf_rank_count": 2,
            "corrected_v1_source_short_cell_count": 1,
            "corrected_v1_image_recut_registry_count": 1,
            "historical_identifier_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_nonpromotion": {
            "historical_Round27_canonical_component_rank": None,
            "historical_Round27_c24_component_id": None,
            "historical_Round35_source_interval_rank": None,
            "historical_Round35_natural_short_cell_k": None,
            "historical_Round35_source_parent_W_id": None,
            "historical_Round35_image_recut_rank": None,
            "historical_Round35_rn_restriction_id": None,
            "Round50_owner_key_count": 0,
            "Round54_t54_token_count": 0,
            "Round67_q_j_output_count": 0,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the connected fixed-leaf branch does not prove a maximal two-dimensional H1 component",
            "the Round137-v1 rank is a corrected coordinate-explicit rank, not the unnamed historical Round27 or Round35 enumeration",
            "the corrected k=0 and image recut registry are not historical Round35 identifiers",
            "the D0 and terminal-face endpoints are boundary limits, not regular interior trajectories",
            "no Round50 owner, Round54 token, Round67 q_j, Gate5 field or CM2 claim is promoted",
        ],
    }
    require(
        result["strict_nonpromotion"]["global_gate5_maturity"] == "10/18"
        and result["strict_nonpromotion"][
            "global_complete_18_field_block_count"
        ] == 0
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "strict global nonpromotion",
    )
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        FUTURE_VERIFIER.resolve(),
        *((HERE / name).resolve() for name in PINS),
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


def atomic_write(path: Path, document: dict[str, Any]) -> None:
    target = validate_output_target(path)
    payload = json.dumps(
        document,
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
    parser.add_argument("--precision-bits", type=int, default=PRIMARY_PRECISION_BITS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    document = build(args.precision_bits)
    atomic_write(args.output, document)
    print(canonical({
        "schema": document["schema"],
        "result_sha256": document["result_sha256"],
        "output": str(args.output.absolute()),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
