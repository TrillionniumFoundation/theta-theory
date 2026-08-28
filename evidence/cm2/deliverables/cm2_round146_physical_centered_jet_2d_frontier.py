#!/usr/bin/env python3
"""Round146: local physical two-dimensional centered-jet frontier.

The genuine source coordinates are

    delta_x = x - x_star,                     x = sqrt(17) r,
    delta_beta = (asin(p) - 4 r) - b_star.

Two adjacent closed cells are certified with the complete R1648 audit:

    delta_x    in [-2 h, -h],
    delta_beta in [-3 h, -h] or [-h, h],      h = 2^-4296.

The cells share the exact artificial face ``delta_beta=-h``.  The next
positive transverse cell is not assigned the frozen itinerary: the
collision-three D0 discriminant has a unique transverse zero graph there.

This is intentionally a local frontier certificate.  It does not close the
Round144 D02 requirement for a maximal two-dimensional outer atlas and it
does not mint any component, rank, restriction, owner, token, or output ID.
"""

from __future__ import annotations

import argparse
import hashlib
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

import cm2_round141_recentered_affine_k4296_d0_collar_return as r141
import cm2_round146_physical_centered_jet_2d_engine as engine


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json"
)
FUTURE_VERIFIER = (
    HERE / "cm2_round146_physical_centered_jet_2d_frontier_verifier.py"
)
SCHEMA = "cm2.round146.physical-centered-jet-2d-frontier.v1"
STATUS = (
    "CERTIFIED_LOCAL_PHYSICAL_2D_SEED_CELL_AND_TRANSVERSE_D3_EVENT_FRONTIER"
    "__D02_STILL_BLOCKED"
)
PRIMARY_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
RETURN_DEPTH = 1648
POWER = 4296
X_CELL_INDEX = 1
CELL_SPECS = (("negative", -1), ("central", 0))


def dependency(name: str) -> Path:
    return HERE / name


ENGINE = dependency("cm2_round146_physical_centered_jet_2d_engine.py")

R140_B_SOURCE = dependency(
    "cm2_round140_fixed_s_adaptive_component_identity_bridge.py"
)
R140_B_CERT = dependency(
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
R140_B_VERIFIER = dependency(
    "cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py"
)
R140_B_VERIFICATION = dependency(
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json"
)
R140_B_MANIFEST = dependency(
    "cm2-one-hundred-fortieth-direct-assault-manifest-2026-07-24.sha256"
)

R140_W_SOURCE = dependency(
    "cm2_round140_round35_parent_w_r1648_materialization_audit.py"
)
R140_W_CERT = dependency(
    "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
R140_W_VERIFIER = dependency(
    "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py"
)
R140_W_VERIFICATION = dependency(
    "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)
R140_W_MANIFEST = dependency(
    "cm2-round140-round35-parent-w-r1648-materialization-audit-direct-assault-manifest-2026-07-24.sha256"
)

R141_SOURCE = dependency(
    "cm2_round141_recentered_affine_k4296_d0_collar_return.py"
)
R141_CERT = dependency(
    "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json"
)
R141_VERIFIER = dependency(
    "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
)
R141_VERIFICATION = dependency(
    "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json"
)
R141_MANIFEST = dependency(
    "cm2-round141-recentered-affine-k4296-d0-collar-return-manifest-2026-07-24.sha256"
)

R142_SOURCE = dependency(
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier.py"
)
R142_CERT = dependency(
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json"
)
R142_VERIFIER = dependency(
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier_verifier.py"
)
R142_VERIFICATION = dependency(
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-verification-2026-07-24.json"
)
R142_MANIFEST = dependency(
    "cm2-one-hundred-forty-second-direct-assault-manifest-2026-07-24.sha256"
)

R144_SOURCE = dependency(
    "cm2_round144_round137_v1_superseding_migration_schema.py"
)
R144_CERT = dependency(
    "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
)
R144_VERIFIER = dependency(
    "cm2_round144_round137_v1_superseding_migration_schema_verifier.py"
)
R144_VERIFICATION = dependency(
    "cm2-round144-round137-v1-superseding-migration-schema-verification-2026-07-24.json"
)
R144_MANIFEST = dependency(
    "cm2-one-hundred-forty-fourth-direct-assault-manifest-2026-07-24.sha256"
)


PINS = {
    ENGINE.name:
        "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb",
    R140_B_SOURCE.name:
        "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2",
    R140_B_CERT.name:
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    R140_B_VERIFIER.name:
        "4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680",
    R140_B_VERIFICATION.name:
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    R140_B_MANIFEST.name:
        "d46c15f7823f78719b505365e0f9c4c3e70103a3bc09fb075a3032b366639748",
    R140_W_SOURCE.name:
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    R140_W_CERT.name:
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    R140_W_VERIFIER.name:
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    R140_W_VERIFICATION.name:
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    R140_W_MANIFEST.name:
        "f3b80bfd794087b395be83fc8e94f7e2ba5201db576337858d9b69c939dd1ed9",
    R141_SOURCE.name:
        "687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28",
    R141_CERT.name:
        "a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe",
    R141_VERIFIER.name:
        "1bb85fdd8dc22aa941084666b5eb9c41154f9e890f6d87c42eaf8808a4748f65",
    R141_VERIFICATION.name:
        "43770a85918cd4986e232cc1e3c401bae9ff8d0ee772b92eea8c46c3c55d4e3c",
    R141_MANIFEST.name:
        "06351a018876a3ec96cc099b9fd44d779c8a533543c7f7cb75379181dc32de52",
    R142_SOURCE.name:
        "97477687d0013f5a8b426250b930e845858c624685c1f45f6528c336963b7d4c",
    R142_CERT.name:
        "816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0",
    R142_VERIFIER.name:
        "ef2d2297aec42ef39a2b0ca352f05659a2fbb72435283333713f393193dbbad5",
    R142_VERIFICATION.name:
        "3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170",
    R142_MANIFEST.name:
        "13bac7695377bad1311063c3420b5ff00107c992c1223a3dc85b0df354af7bf6",
    R144_SOURCE.name:
        "3665730d98b23ea952d352910a2dd0a5410d6697d14604a087cf0cd12caea80b",
    R144_CERT.name:
        "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    R144_VERIFIER.name:
        "413c85a68d2a6623b1250cfbbc502ea13a2036f084ac483c96eb044a16db9265",
    R144_VERIFICATION.name:
        "dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5",
    R144_MANIFEST.name:
        "4a2b267f380b983e64d774d58d2973358663f8b400a2934c6cbeff97610a7a1c",
}


CLOSED = {
    R140_B_CERT.name: (
        "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1",
        "60a364ec21cc1bedf83f7287a7e8f4e9a90a2be431d04cec8fed3f9c0102496b",
        "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION",
    ),
    R140_B_VERIFICATION.name: (
        "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1",
        "c9b36397f28a63f5408fc82ee474617fe54e73774382c607dc10bc3e9b6dd746",
        "PASS",
    ),
    R140_W_CERT.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
        "7988f4c9588894ec964e2c6efec4dd07dd28d5011c0bf004ad73f99414534eed",
        "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648",
    ),
    R140_W_VERIFICATION.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
        "9d898c0cea05069511732acd2be74f04d66f416d10f4ca72cd6e6bccf8b9cf33",
        "PASS",
    ),
    R141_CERT.name: (
        "cm2.round141.recentered-affine-k4296-d0-collar-return.v1",
        "48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f",
        "CERTIFIED_RECENTERED_AFFINE_K4296_D0_COLLAR_STRICT_R1648_RETURN",
    ),
    R141_VERIFICATION.name: (
        "cm2.round141.recentered-affine-k4296-d0-collar-return-verification.v1",
        "8c94e2f846062cae13be0d9fb8520877cb6de7903354090df87ad084d74153a4",
        "PASS",
    ),
    R142_CERT.name: (
        "cm2.round142.historical-component-crosswalk-outer-atlas-frontier.v1",
        "e734b4008ab822710c8b4c5aec5cc1a871f16d7bcea2230ba80eb2f493f0a37e",
        "CERTIFIED_HISTORICAL_ENUMERATION_UNDERDETERMINATION_AND_OUTER_ATLAS_FRONTIER",
    ),
    R142_VERIFICATION.name: (
        "cm2.round142.historical-component-crosswalk-outer-atlas-frontier-verification.v1",
        "6b5d015ecc67626a6c30ab8d7b837d44aea6c280b42655415ef4fa371895f8eb",
        "PASS",
    ),
    R144_CERT.name: (
        "cm2.round144.round137-v1-superseding-migration-schema.v1",
        "0c7a1711ca1df912b24abd3251a40ad8ddd20f0ea39a44a90113b7a41273aa42",
        "CERTIFIED_VERSIONED_SUPERSEDING_MIGRATION_SCHEMA__NO_CORRECTED_COMPONENT_MINTED",
    ),
    R144_VERIFICATION.name: (
        "cm2.round144.round137-v1-superseding-migration-schema-verification.v1",
        "b0fc814004e58832c9979cedeab0ffc236707a9947eb1d4eaeba487465c4f709",
        "PASS",
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
    return engine.r139.qstr(Q(value))


def strict_json(path: Path) -> dict[str, Any]:
    return engine.r139.strict_json(path)


def validate_dependencies() -> dict[str, dict[str, Any]]:
    paths = (ENGINE,) + tuple(HERE / name for name in PINS if name != ENGINE.name)
    require(set(PINS) == {path.name for path in paths}, "complete direct pins")
    documents: dict[str, dict[str, Any]] = {}
    for path in paths:
        require(path.exists(), f"missing dependency:{path.name}")
        require(sha256(path) == PINS[path.name], f"dependency pin:{path.name}")
        if path.name not in CLOSED:
            continue
        document = strict_json(path)
        schema, result_sha, status = CLOSED[path.name]
        require(
            set(document) == {"schema", "result", "result_sha256"}
            and document["schema"] == schema
            and document["result_sha256"] == result_sha
            and digest(document["result"]) == result_sha
            and document["result"]["status"] == status,
            f"closed dependency:{path.name}",
        )
        documents[path.name] = document["result"]
    # Round141 is the frozen transitive guard for the older numerical stack.
    r141.validate_dependencies()
    return documents


def _cell_worker(arguments: tuple[str, int, int]) -> tuple[str, dict[str, Any]]:
    label, beta_cell_index, precision = arguments
    row = engine.run_cell(
        POWER,
        X_CELL_INDEX,
        POWER,
        beta_cell_index,
        precision,
        True,
    )
    return label, row


def replay_cells(precision: int) -> dict[str, dict[str, Any]]:
    require(
        type(precision) is int and precision >= PRIMARY_PRECISION_BITS,
        "producer precision",
    )
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=2, mp_context=context) as executor:
        pairs = list(executor.map(
            _cell_worker,
            [
                (label, beta_cell_index, precision)
                for label, beta_cell_index in CELL_SPECS
            ],
        ))
    return dict(pairs)


def validate_cell(label: str, index: int, row: dict[str, Any]) -> None:
    require(
        row["status"] == "PASS"
        and row["audit_all"] is True
        and row["physical_parameter_generator_count"] == 2
        and row["parameter_generators"] == ["delta_x", "delta_beta"]
        and row["t_star_numerical_isolation_is_parameter"] is False
        and row["x_power"] == POWER
        and row["x_cell_index"] == X_CELL_INDEX
        and row["beta_power"] == POWER
        and row["beta_cell_index"] == index
        and row["collision_count"] == RETURN_DEPTH
        and row["full_radius4_candidate_test_count"] == 161 * RETURN_DEPTH
        and row["official_sequence_sha256"]
        == engine.r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and row["compact_rows_sha256"]
        == engine.r139.EXPECTED_COMPACT_PATH_SHA256
        and row["homogeneity_histogram"] == {"H0_CENTRAL": RETURN_DEPTH}
        and row["incidence_histogram"] == {14: RETURN_DEPTH}
        and row["preterminal_strict_nonreturn_count"] == RETURN_DEPTH - 1
        and row["terminal_strict_return_count"] == 1
        and row["terminal_owner"] == engine.r139.EXPECTED_TERMINAL_OWNER
        and row["terminal_destination_core"]
        == engine.r139.EXPECTED_DESTINATION_CORE_ID
        and row["model_radius_ledger_row_count"] == RETURN_DEPTH
        and row[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ] <= -13
        and row["collision3_physical_anchor_exclusion"][
            "D3_maximum_strict_negative"
        ] is True,
        f"complete physical cell:{label}",
    )


def compact_cell(label: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "cell_label": label,
        "cell_id":
            "round146-physical-2d-cell:"
            + digest({
                "x_center": row["x_center"],
                "x_radius": row["x_radius"],
                "beta_center": row["beta_center"],
                "beta_radius": row["beta_radius"],
                "path": row["compact_rows_sha256"],
            }),
        "delta_x_center": row["x_center"],
        "delta_x_halfwidth": row["x_radius"],
        "delta_beta_center": row["beta_center"],
        "delta_beta_halfwidth": row["beta_radius"],
        "collision_count": row["collision_count"],
        "full_radius4_candidate_test_count":
            row["full_radius4_candidate_test_count"],
        "official_sequence_sha256": row["official_sequence_sha256"],
        "compact_path_sha256": row["compact_rows_sha256"],
        "homogeneity_histogram": row["homogeneity_histogram"],
        "incidence_histogram": {
            str(key): value
            for key, value in row["incidence_histogram"].items()
        },
        "preterminal_strict_nonreturn_count":
            row["preterminal_strict_nonreturn_count"],
        "terminal_strict_return_count":
            row["terminal_strict_return_count"],
        "terminal_owner": row["terminal_owner"],
        "terminal_destination_core": row["terminal_destination_core"],
        "model_radius_ledger_row_count":
            row["model_radius_ledger_row_count"],
        "model_radius_ledger_sha256":
            row["model_radius_ledger_sha256"],
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            row["maximum_state_radius_strict_upper_power_of_two_exponent"],
        "maximum_state_radius_witness":
            row["maximum_state_radius_witness"],
        "terminal_state_radius_strict_upper_power_of_two_exponents":
            row[
                "terminal_state_radius_strict_upper_power_of_two_exponents"
            ],
        "ledger_worst_depth": row["ledger_worst_depth"],
        "ledger_worst_names": row["ledger_worst_names"],
        "collision3_physical_anchor_exclusion":
            row["collision3_physical_anchor_exclusion"],
        "terminal_phase_fixed_dyadic_outer_bits":
            row["terminal_phase_fixed_dyadic_outer_bits"],
        "terminal_normal_x_fixed_dyadic_outer":
            row["terminal_normal_x_fixed_dyadic_outer"],
        "terminal_normal_y_fixed_dyadic_outer":
            row["terminal_normal_y_fixed_dyadic_outer"],
        "terminal_p_fixed_dyadic_outer":
            row["terminal_p_fixed_dyadic_outer"],
        "terminal_cosine_fixed_dyadic_outer":
            row["terminal_cosine_fixed_dyadic_outer"],
    }


def build(precision_bits: int = PRIMARY_PRECISION_BITS) -> dict[str, Any]:
    closed = validate_dependencies()
    cells = replay_cells(precision_bits)
    require(set(cells) == {"negative", "central"}, "two cell labels")
    validate_cell("negative", -1, cells["negative"])
    validate_cell("central", 0, cells["central"])
    compact = [
        compact_cell("negative", cells["negative"]),
        compact_cell("central", cells["central"]),
    ]

    ctx.prec = precision_bits
    r140 = closed[R140_B_CERT.name]
    r140_w = closed[R140_W_CERT.name]
    r142 = closed[R142_CERT.name]
    r144 = closed[R144_CERT.name]
    root = tuple(
        Q(value)
        for value in engine.r139.strict_json(
            engine.R139_CERTIFICATE
        )["result"]["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    event = engine.transverse_D3_event_frontier(root)
    # The event engine is deliberately event-only.  The producer has just
    # completed the separate full path audit of this negative neighbor.
    event["negative_transverse_neighbor"][
        "complete_path_audit_in_this_result"
    ] = True
    event[
        "central_x_single_Newton_estimate_beta_in_h_units"
    ] = event.pop("central_x_root_beta_in_h_units")
    h = Q(1, 2**POWER)
    h_arb = engine.r139.lower.aq(h)
    root_lower, root_upper = map(engine.r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + engine.symmetric((root_upper - root_lower) / 2)
    )
    corridor = engine.anchor_discriminant(
        -3 * h_arb / 2 + engine.symmetric(h_arb / 2),
        7 * h_arb / 2 + engine.symmetric(5 * h_arb / 2),
        t_star,
    )
    require(
        bool(corridor.derivative[0] > 0)
        and bool(corridor.derivative[1] > 0),
        "positive-beta D3 corridor monotonicity",
    )
    event["positive_beta_corridor_from_certified_face"] = {
        "physical_parameter_box": {
            "delta_x": [qstr(-2 * h), qstr(-h)],
            "delta_beta": [qstr(h), qstr(6 * h)],
        },
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "partial_D3_partial_delta_x_outer":
            engine.fixed_outer(corridor.derivative[0], 128),
        "partial_D3_partial_delta_beta_outer":
            engine.fixed_outer(corridor.derivative[1], 128),
        "shared_face_D3_strict_negative": True,
        "event_box_bottom_D3_strict_negative": True,
        "no_earlier_D3_zero_between_shared_face_and_event_box": True,
    }
    require(
        event["D3_strictly_increasing_in_delta_x"] is True
        and event["D3_strictly_increasing_in_delta_beta"] is True
        and event["bottom_edge_D3_strict_negative"] is True
        and event["top_edge_D3_strict_positive"] is True
        and event["unique_beta_root_for_every_fixed_delta_x"] is True
        and event[
            "parametric_interval_Newton_strictly_inside_event_beta_box"
        ] is True
        and event["transverse_to_beta_fibres"] is True
        and event["positive_transverse_neighbor"][
            "D3_event_enters_neighbor"
        ] is True
        and event["positive_transverse_neighbor"][
            "whole_neighbor_has_frozen_owner_path"
        ] is False,
        "transverse D3 event frontier",
    )

    shared_face = {
        "face_id":
            "round146-artificial-shared-beta-face:"
            + digest({
                "delta_x": [qstr(-2 * h), qstr(-h)],
                "delta_beta": qstr(-h),
            }),
        "delta_x_closed_interval": [qstr(-2 * h), qstr(-h)],
        "delta_beta": qstr(-h),
        "negative_cell_upper_face": True,
        "central_cell_lower_face": True,
        "exactly_shared": True,
        "same_exact_physical_initial_map": True,
        "same_1648_selected_circle_composition": True,
    }
    atlas_payload = {
        "cells": [row["cell_id"] for row in compact],
        "shared_face": shared_face["face_id"],
        "path": engine.r139.EXPECTED_COMPACT_PATH_SHA256,
    }
    atlas_id = (
        "round146-local-physical-2d-two-cell-atlas:"
        + digest(atlas_payload)
    )

    path = r140["Round27_path_instance"]
    adaptive = r140["fixed_s_adaptive_path_cell"]
    d02 = next(
        row
        for row in r144["migration_DAG_rows"]
        if row["node_id"] == "D02"
    )
    require(
        path["return_depth_n"] == RETURN_DEPTH
        and path["Round27_compatible_candidate_path_tuple_sha256"]
        == "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9"
        and path["positive_area_nonempty_path_fibre_witness"] is True
        and r140_w["fixed_parameter_and_exact_implicit_leaf"]["s"] == "0"
        and r142["centered_jet_outer_atlas_frontier"][
            "complete_2D_centered_jet_cell_count"
        ] == 0
        and r142["centered_jet_outer_atlas_frontier"][
            "maximal_component_U_boundary_exhausted"
        ] is False
        and d02["status"] == "BLOCKED"
        and d02["row_sha256"]
        == "9bca02effa51c0cfb6da042c131cdd58fa4cce2bcfc6f133faf5fb5a379733b0",
        "frozen identity and D02 frontier",
    )

    result = {
        "status": STATUS,
        "minimum_certified_precision_bits": PRIMARY_PRECISION_BITS,
        "secondary_verifier_precision_bits": SECONDARY_PRECISION_BITS,
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "engine_sha256": PINS[ENGINE.name],
            "direct_frozen_dependency_rounds": [140, 141, 142, 144],
            "direct_dependency_sha256": dict(sorted(PINS.items())),
            "Round141_transitive_dependency_guard_replayed": True,
            "append_only": True,
            "Round140_Round141_Round142_Round144_files_modified": False,
        },
        "source_identity": {
            "fixed_parameter_s": "0",
            "source_core_id": path["source_core_id"],
            "return_depth_n": RETURN_DEPTH,
            "Round27_compatible_path_tuple_sha256":
                path[
                    "Round27_compatible_candidate_path_tuple_sha256"
                ],
            "official_word_sequence_sha256":
                path["official_word_key_sequence_sha256"],
            "Round140_adaptive_path_cell_id":
                adaptive["adaptive_path_cell_id"],
            "Round140_positive_area_seed_exists": True,
        },
        "physical_centered_coordinates": {
            "generator_count": 2,
            "generators": ["delta_x", "delta_beta"],
            "delta_x_definition": "x-x_star, x=sqrt(17)*r",
            "delta_beta_definition":
                "(asin(p)-4*r)-b_star",
            "exact_initial_map": {
                "t":
                    "sin(asin(t_star)+delta_x/(R_W*sqrt(17)))",
                "p":
                    "sin(asin(p_star)+4*delta_x/sqrt(17)+delta_beta)",
            },
            "angle_coordinate_Jacobian": {
                "rows":
                    [
                        ["1/(R_W*sqrt(17))", "0"],
                        ["4/sqrt(17)", "1"],
                    ],
                "determinant": "1/(R_W*sqrt(17))",
                "determinant_strict_positive": True,
            },
            "t_star_numerical_enclosure_is_physical_generator": False,
            "t_star_numerical_enclosure_charged_to_initial_remainder": True,
            "coordinate_rank": 2,
            "coordinate_Jacobian_nondegenerate": True,
        },
        "local_connected_two_cell_atlas": {
            "atlas_id": atlas_id,
            "payload_sha256": digest(atlas_payload),
            "h": qstr(h),
            "delta_x_closed_interval": [qstr(-2 * h), qstr(-h)],
            "delta_beta_certified_union": [qstr(-3 * h), qstr(h)],
            "cell_count": 2,
            "cells": compact,
            "internal_shared_face_count": 1,
            "internal_shared_face": shared_face,
            "adjacency_graph": "path_on_2_vertices",
            "adjacency_graph_connected": True,
            "both_cells_complete_full_R1648_audit": True,
            "same_owner_word_chart_homogeneity_incidence_C24_path": True,
            "full_radius4_candidate_test_count":
                2 * 161 * RETURN_DEPTH,
            "preterminal_strict_nonreturn_cell_stage_count":
                2 * (RETURN_DEPTH - 1),
            "terminal_strict_return_cell_count": 2,
        },
        "positive_transverse_event_frontier": event,
        "first_collision3_D0_event_in_positive_beta_direction": {
            "certified_atlas_upper_face_delta_beta": qstr(h),
            "D3_strictly_negative_on_whole_upper_face": True,
            "next_positive_neighbor_delta_beta":
                [qstr(h), qstr(3 * h)],
            "next_positive_neighbor_shares_exact_artificial_face": True,
            "next_positive_neighbor_complete_path_claimed": False,
            "collision3_D0_D3_zero_enters_next_positive_neighbor": True,
            "event_box_delta_beta": [qstr(2 * h), qstr(6 * h)],
            "event_is_unique_beta_graph_for_every_fixed_delta_x": True,
            "event_Jacobian_partial_beta_excludes_zero": True,
            "event_graph_transverse_to_beta_fibres": True,
            "event_graph_slope_strict_negative": True,
            "claim_scope":
                "first zero in the collision3 D0 candidate family in the positive-beta direction; not claimed first among all physical events and not an exhaustion of every global component frontier",
        },
        "Round144_D02_status": {
            "node_id": "D02",
            "operation": d02["operation"],
            "frozen_blocker_row_sha256":
                r144["first_exact_blocker"]["row_sha256"],
            "frozen_DAG_row_sha256": d02["row_sha256"],
            "frozen_status": d02["status"],
            "local_two_cell_atlas_closes_D02": False,
            "reason":
                "two cells and one local D3 event graph do not exhaust all outer-atlas cells, exits, and event frontiers of the maximal two-dimensional component",
            "maximal_component_outer_atlas_complete": False,
            "all_event_frontiers_exhausted": False,
            "D03_least_rank_negative_oracle_authorized": False,
        },
        "count_ledger": {
            "physical_parameter_generator_count": 2,
            "complete_2D_cell_count": 2,
            "exact_internal_shared_face_count": 1,
            "collision_stage_cell_pairs": 2 * RETURN_DEPTH,
            "full_radius4_candidate_test_count":
                2 * 161 * RETURN_DEPTH,
            "preterminal_strict_nonreturn_cell_stage_pairs":
                2 * (RETURN_DEPTH - 1),
            "terminal_strict_return_cell_count": 2,
            "local_transverse_event_graph_count": 1,
            "historical_or_versioned_component_ID_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_nonpromotion": {
            "historical_Round27_canonical_component_rank": None,
            "historical_Round27_c24_component_id": None,
            "Round137_v1_maximal_component_rank": None,
            "Round137_v1_component_id": None,
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
            "the numerical t_star enclosure is an interval constant, not a third physical coordinate",
            "the positive transverse neighbor is event-entering and has no whole-cell frozen-path claim",
            "the local two-cell atlas is not a maximal two-dimensional component atlas",
            "the local D3 event graph does not exhaust every global exit or event frontier",
            "Round144 D02 remains blocked, so D03 and every downstream corrected identifier remain unavailable",
            "no historical Round27 or Round35 identity is inferred from prospective Round137-v1 coordinates",
            "no Round50 owner, Round54 token, Round67 q_j, Gate5 field, or CM2 claim is promoted",
        ],
    }
    require(
        result["Round144_D02_status"]["local_two_cell_atlas_closes_D02"]
        is False
        and result["strict_nonpromotion"]["global_gate5_maturity"]
        == "10/18"
        and result["strict_nonpromotion"]["Gate5"] == "NOT_CERTIFIED"
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
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1,
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
    parser.add_argument(
        "--precision-bits",
        type=int,
        default=PRIMARY_PRECISION_BITS,
    )
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
