#!/usr/bin/env python3
"""Independent verifier for the Round146 physical 2D frontier.

This verifier imports neither the Round146 producer nor its computational
engine.  It independently maps the two physical coordinates to the source
contact state, reconstructs both complete 1648-collision affine audits, and
recomputes the transverse collision-three D0 event graph.  Only the frozen
Round141 independent affine primitives and the older transitive billiard
stack are reused.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import multiprocessing
import os
import stat
import sys
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Sequence

from flint import arb, ctx

import cm2_fixed_section_common_vertex_cert as ad
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_recentered_affine_k4296_d0_collar_return as r141p
import cm2_round141_recentered_affine_k4296_d0_collar_return_verifier as v141


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PRODUCER = (
    HERE / "cm2_round146_physical_centered_jet_2d_frontier.py"
)
ENGINE = HERE / "cm2_round146_physical_centered_jet_2d_engine.py"
CERTIFICATE = (
    HERE
    / "cm2-round146-physical-centered-jet-2d-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round146-physical-centered-jet-2d-frontier-verification-2026-07-24.json"
)
SCHEMA = "cm2.round146.physical-centered-jet-2d-frontier-verification.v1"
CERTIFICATE_SCHEMA = "cm2.round146.physical-centered-jet-2d-frontier.v1"
CERTIFICATE_STATUS = (
    "CERTIFIED_LOCAL_PHYSICAL_2D_SEED_CELL_AND_TRANSVERSE_D3_EVENT_FRONTIER"
    "__D02_STILL_BLOCKED"
)
PRIMARY_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
RETURN_DEPTH = 1648
POWER = 4296
X_CELL_INDEX = 1
CELL_SPECS = (("negative", -1), ("central", 0))

PRODUCER_SHA256 = (
    "db0241c9bae4937cd1a01f23b4951247fa69fd16d9b06a75d446e5336c9930c4"
)
CERTIFICATE_SHA256 = (
    "38ad7cdd5a2af7cda94792a31a8a83275022f943e8e6b9801ee4bece73b04eac"
)
CERTIFICATE_RESULT_SHA256 = (
    "66936a51409bbe87ef2a10e80f081d345954c8104a23a4a05a21019f0d3b0e67"
)
ENGINE_SHA256 = (
    "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb"
)


DIRECT_PINS = {
    ENGINE.name: ENGINE_SHA256,
    "cm2_round140_fixed_s_adaptive_component_identity_bridge.py":
        "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json":
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    "cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py":
        "4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680",
    "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json":
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    "cm2-one-hundred-fortieth-direct-assault-manifest-2026-07-24.sha256":
        "d46c15f7823f78719b505365e0f9c4c3e70103a3bc09fb075a3032b366639748",
    "cm2_round140_round35_parent_w_r1648_materialization_audit.py":
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json":
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py":
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json":
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    "cm2-round140-round35-parent-w-r1648-materialization-audit-direct-assault-manifest-2026-07-24.sha256":
        "f3b80bfd794087b395be83fc8e94f7e2ba5201db576337858d9b69c939dd1ed9",
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
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier.py":
        "97477687d0013f5a8b426250b930e845858c624685c1f45f6528c336963b7d4c",
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-2026-07-24.json":
        "816284789cc1249efd0ae9b9880e7d0434e8f74499c2616c6b64331997143ba0",
    "cm2_round142_historical_component_crosswalk_outer_atlas_frontier_verifier.py":
        "ef2d2297aec42ef39a2b0ca352f05659a2fbb72435283333713f393193dbbad5",
    "cm2-round142-historical-component-crosswalk-outer-atlas-frontier-verification-2026-07-24.json":
        "3e7abbe91af042cea229b998fba9c3829fe94120227102f98ecea620005db170",
    "cm2-one-hundred-forty-second-direct-assault-manifest-2026-07-24.sha256":
        "13bac7695377bad1311063c3420b5ff00107c992c1223a3dc85b0df354af7bf6",
    "cm2_round144_round137_v1_superseding_migration_schema.py":
        "3665730d98b23ea952d352910a2dd0a5410d6697d14604a087cf0cd12caea80b",
    "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json":
        "bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f",
    "cm2_round144_round137_v1_superseding_migration_schema_verifier.py":
        "413c85a68d2a6623b1250cfbbc502ea13a2036f084ac483c96eb044a16db9265",
    "cm2-round144-round137-v1-superseding-migration-schema-verification-2026-07-24.json":
        "dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5",
    "cm2-one-hundred-forty-fourth-direct-assault-manifest-2026-07-24.sha256":
        "4a2b267f380b983e64d774d58d2973358663f8b400a2934c6cbeff97610a7a1c",
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


def typed_equal(left: Any, right: Any) -> bool:
    """JSON equality that keeps booleans distinct from integers."""

    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return (
            left.keys() == right.keys()
            and all(typed_equal(left[key], right[key]) for key in left)
        )
    if isinstance(left, list):
        return (
            len(left) == len(right)
            and all(typed_equal(a, b) for a, b in zip(left, right))
        )
    return bool(left == right)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    return r139.qstr(Q(value))


def symmetric(radius: arb) -> arb:
    return arb(0, radius.upper())


def point(value: arb) -> arb:
    return arb(value.mid())


def dual_asin(value: ad.Dual) -> ad.Dual:
    denominator = (1 - value.value * value.value).sqrt()
    return ad.Dual(
        value.value.asin(),
        [entry / denominator for entry in value.derivative],
    )


def physical_initial(
    delta_x: ad.Dual,
    delta_beta: ad.Dual,
    t_star: arb,
) -> list[ad.Dual]:
    require(
        delta_x.dimension == 2 and delta_beta.dimension == 2,
        "two physical coordinates",
    )
    sqrt17 = arb(17).sqrt()
    angle = (
        dual_asin(ad.Dual(t_star, dimension=2))
        + delta_x / (r139.lower.aq(r139.lower.R_W) * sqrt17)
    )
    t = ad.dual_sin(angle)
    p_phase = (
        ad.Dual(
            r139.lower.aq(r139.lower.SOURCE_P_STAR).asin(),
            dimension=2,
        )
        + 4 * delta_x / sqrt17
        + delta_beta
    )
    p = ad.dual_sin(p_phase)
    nx, ny = ad.dual_cos(angle), t
    radial = ad.dual_sqrt(ad.Dual(1, dimension=2) - p * p)
    velocity = (
        radial * nx - p * ny,
        radial * ny + p * nx,
    )
    center, radius = v141.target(r139.lower.SOURCE_ABSOLUTE_OWNER)
    position = (
        ad.Dual(center[0], dimension=2) + radius * nx,
        ad.Dual(center[1], dimension=2) + radius * ny,
    )
    return list(position + velocity)


def parameter_cell(beta_cell_index: int) -> tuple[arb, arb, arb, arb]:
    require(beta_cell_index in {-1, 0}, "verified beta cell")
    h = r139.lower.aq(Q(1, 2**POWER))
    return -3 * h / 2, h / 2, 2 * beta_cell_index * h, h


def initial_affine(
    root: tuple[Q, Q],
    beta_cell_index: int,
) -> v141.AffineState:
    x_center, x_radius, beta_center, beta_radius = parameter_cell(
        beta_cell_index
    )
    root_lower, root_upper = map(r139.lower.aq, root)
    root_center = point((root_lower + root_upper) / 2)
    root_ball = root_center + symmetric((root_upper - root_lower) / 2)
    center_values = physical_initial(
        ad.Dual(x_center, [arb(1), arb(0)]),
        ad.Dual(beta_center, [arb(0), arb(1)]),
        root_center,
    )
    interval_values = physical_initial(
        ad.Dual(x_center + symmetric(x_radius), [arb(1), arb(0)]),
        ad.Dual(beta_center + symmetric(beta_radius), [arb(0), arb(1)]),
        root_ball,
    )
    root_only_values = physical_initial(
        ad.Dual(x_center, [arb(1), arb(0)]),
        ad.Dual(beta_center, [arb(0), arb(1)]),
        root_ball,
    )
    raw_generators = v141.dual_rows(center_values)
    generators = [
        [point(entry) for entry in row]
        for row in raw_generators
    ]
    interval_derivatives = v141.dual_rows(interval_values)
    parameter_radii = (x_radius, beta_radius)
    centers = [point(value.value) for value in center_values]
    errors = [
        (center_values[row].value - centers[row]).abs_upper()
        + (
            root_only_values[row].value
            - center_values[row].value
        ).abs_upper()
        + sum(
            (
                raw_generators[row][column]
                - generators[row][column]
            ).abs_upper()
            * parameter_radii[column]
            for column in range(2)
        )
        + sum(
            (
                interval_derivatives[row][column]
                - raw_generators[row][column]
            ).abs_upper()
            * parameter_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return v141.AffineState(
        centers,
        generators,
        errors,
        parameter_radii,
    )


def load_transitive_inputs() -> tuple[list[str], tuple[Q, Q]]:
    path = (
        HERE
        / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
    )
    require(
        sha256(path) == v141.R139_CERTIFICATE_SHA256,
        "Round141-transitive Round139 certificate",
    )
    result = r139.strict_json(path)["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    require(
        len(owners) == RETURN_DEPTH
        and digest(owners) == r139.EXPECTED_OWNER_SEQUENCE_SHA256,
        "frozen owner sequence",
    )
    root = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    return owners, root  # type: ignore[return-value]


def anchor_discriminant(
    delta_x: arb,
    delta_beta: arb,
    t_star: arb,
    owners: Sequence[str],
) -> ad.Dual:
    state = physical_initial(
        ad.Dual(delta_x, [arb(1), arb(0)]),
        ad.Dual(delta_beta, [arb(0), arb(1)]),
        t_star,
    )
    for owner in owners[:2]:
        center, radius = v141.target(owner)
        state, _metrics = v141.ray_map(state, center, radius)
    center, radius = v141.target(r139.ANCHOR)
    displacement = (
        state[0] - center[0],
        state[1] - center[1],
    )
    linear = ad.dual_dot(displacement, state[2:])
    offset = ad.dual_dot(displacement, displacement) - radius * radius
    return linear * linear - offset


def fixed_outer(value: arb, bits: int) -> list[str]:
    raw_lower, raw_upper = r139.lower.round136.arb_pair(value)
    scale = 2**bits
    lower = Q(r139.lower.floor_q(raw_lower * scale) - 1, scale)
    upper = Q(r139.lower.ceil_q(raw_upper * scale) + 1, scale)
    require(
        lower < upper
        and bool(value > r139.lower.aq(lower))
        and bool(value < r139.lower.aq(upper)),
        "fixed padded outer",
    )
    return [qstr(lower), qstr(upper)]


def anchor_exclusion(
    root: tuple[Q, Q],
    owners: Sequence[str],
    beta_cell_index: int,
) -> dict[str, Any]:
    x_center, x_radius, beta_center, beta_radius = parameter_cell(
        beta_cell_index
    )
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + symmetric((root_upper - root_lower) / 2)
    )
    whole = anchor_discriminant(
        x_center + symmetric(x_radius),
        beta_center + symmetric(beta_radius),
        t_star,
        owners,
    )
    corner = anchor_discriminant(
        x_center + x_radius,
        beta_center + beta_radius,
        t_star,
        owners,
    )
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0)
        and bool(corner.value < 0),
        "cell D3 exclusion",
    )
    return {
        "method":
            "full-cell derivative signs plus exact upper-right corner",
        "anchor_candidate": r139.ANCHOR,
        "collision_index": r139.ANCHOR_COLLISION_INDEX,
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "D3_maximum_corner": [
            "delta_x upper",
            "delta_beta upper",
        ],
        "D3_maximum_strict_negative": True,
        "D3_miss_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-corner.value),
        "D3_delta_x_derivative_outer":
            fixed_outer(whole.derivative[0], 128),
        "D3_delta_beta_derivative_outer":
            fixed_outer(whole.derivative[1], 128),
        "t_star_numerical_enclosure_charged_not_parameterized": True,
    }


def replay_cell(beta_cell_index: int, precision_bits: int) -> dict[str, Any]:
    require(precision_bits >= PRIMARY_PRECISION_BITS, "replay precision")
    ctx.prec = precision_bits
    owners, root = load_transitive_inputs()
    model = initial_affine(root, beta_cell_index)
    anchor = anchor_exclusion(root, owners, beta_cell_index)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    cores = tuple(r139.lower.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = (
        r139.lower.component_cert.key_index_tables()
    )
    require(
        registry_sha == r139.OFFICIAL_REGISTRY_SHA256,
        "official registry",
    )
    initial_boxes = model.boxes()
    source_center, source_radius = v141.target(current_target)
    source_nx = (initial_boxes[0] - source_center[0]) / source_radius
    source_ny = (initial_boxes[1] - source_center[1]) / source_radius
    source_p = (
        -initial_boxes[2] * source_ny
        + initial_boxes[3] * source_nx
    )
    previous_cosine = (1 - source_p * source_p).sqrt()
    ledger = v141.Ledger()
    official_ids: list[str] = []
    compact_rows: list[list[Any]] = []
    homogeneity: Counter[str] = Counter()
    incidence: Counter[int] = Counter()
    radius_rows: list[list[Any]] = []
    maximum_radius = arb(0)
    maximum_witness: list[int | None] | None = None
    terminal_phase: dict[str, arb] | None = None
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        for component, radius in enumerate(model.total_radii()):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_witness = [
                    collision_index - 1,
                    component,
                    v141.upper_exponent(radius),
                ]
        boxes = model.boxes()
        state = {
            "contact_x": boxes[0],
            "contact_y": boxes[1],
            "outgoing_x": boxes[2],
            "outgoing_y": boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        owner, _retained = r139.lower.round136.complete_owner(
            state,
            current_target,
            ledger,
            collision_index,
        )
        r139.lower.full_radius4_candidate_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        require(
            owner["selected_target_id"] == expected_owner,
            f"owner:{collision_index}",
        )
        word, word_error = (
            r139.lower.round136.translation_normalized_official_word(
                state,
                current_target,
                owner,
                pair_index,
                pattern_index,
            )
        )
        require(
            word is not None and word_error is None,
            f"word:{collision_index}:{word_error}",
        )
        r139.official_wall_margin_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        model, audit = v141.propagate(model, expected_owner)
        for component, radius in enumerate(audit["output_total"]):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_witness = [
                    collision_index,
                    component,
                    v141.upper_exponent(radius),
                ]
        radius_rows.append([
            collision_index,
            v141.exponents(audit["input_affine"]),
            v141.exponents(audit["input_errors"]),
            v141.exponents(audit["input_total"]),
            v141.exponents(audit["raw_errors"]),
            v141.exponents(audit["center_losses"]),
            v141.exponents(audit["coefficient_losses"]),
            v141.exponents(audit["output_affine"]),
            v141.exponents(audit["output_errors"]),
            v141.exponents(audit["output_total"]),
        ])
        current_target = expected_owner
        current_chart, phase = v141.phase_at_contact(
            model,
            current_target,
        )
        certified_owner = {
            **phase,
            "selected_target_id": expected_owner,
            "selected_root": owner["selected_root"],
        }
        classification, destination, _witnesses = (
            r139.lower.time3.core_classification(
                certified_owner,
                cores,
            )
        )
        if collision_index < RETURN_DEPTH:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                f"preterminal C24:{collision_index}",
            )
        else:
            require(
                classification == "RETURN_AT_3_INNER"
                and destination == r139.EXPECTED_DESTINATION_CORE_ID
                and expected_owner == r139.EXPECTED_TERMINAL_OWNER,
                "terminal C24",
            )
            terminal_phase = phase
        r139.lower.round136.core_margin(
            certified_owner,
            classification,
            destination,
            cores,
            ledger,
        )
        label, _audit = r139.lower.generic_homogeneity_label(
            collision_index,
            phase["cosine"],
            ledger,
        )
        source_rank = r139.lower.round136.capped_reciprocal_cosine_rank(
            previous_cosine,
            ledger,
            collision_index,
            "source",
        )
        target_rank = r139.lower.round136.capped_reciprocal_cosine_rank(
            phase["cosine"],
            ledger,
            collision_index,
            "target",
        )
        rank = max(14, source_rank, target_rank)
        r139.lower.round136.chart_margin(
            {
                "chart": current_chart,
                "normal_x": phase["normal_x"],
                "normal_y": phase["normal_y"],
            },
            ledger,
        )
        official = r139.lower.round136.compact_key(word["key"])[
            "official_word_key_id"
        ]
        official_ids.append(official)
        compact_rows.append([
            collision_index,
            incoming_target,
            expected_owner,
            official,
            label,
            rank,
            classification,
            destination,
        ])
        homogeneity[label] += 1
        incidence[rank] += 1
        previous_cosine = phase["cosine"]
    require(terminal_phase is not None, "terminal phase")
    require(
        digest(official_ids) == r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and digest(compact_rows) == r139.EXPECTED_COMPACT_PATH_SHA256
        and homogeneity == Counter({"H0_CENTRAL": RETURN_DEPTH})
        and incidence == Counter({14: RETURN_DEPTH}),
        "path identities",
    )
    h = Q(1, 2**POWER)
    beta_center = 2 * beta_cell_index * h
    return {
        "status": "PASS",
        "audit_all": True,
        "physical_parameter_generator_count": 2,
        "parameter_generators": ["delta_x", "delta_beta"],
        "t_star_numerical_isolation_is_parameter": False,
        "collision3_physical_anchor_exclusion": anchor,
        "x_power": POWER,
        "x_cell_index": X_CELL_INDEX,
        "beta_power": POWER,
        "beta_cell_index": beta_cell_index,
        "x_center": qstr(-Q(3, 2) * h),
        "x_radius": qstr(h / 2),
        "beta_center": qstr(beta_center),
        "beta_radius": qstr(h),
        "collision_count": RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(homogeneity),
        "incidence_histogram": dict(incidence),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "terminal_strict_return_count": 1,
        "terminal_owner": r139.EXPECTED_TERMINAL_OWNER,
        "terminal_destination_core": r139.EXPECTED_DESTINATION_CORE_ID,
        "model_radius_ledger_row_count": len(radius_rows),
        "model_radius_ledger_sha256": digest(radius_rows),
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            v141.upper_exponent(maximum_radius),
        "maximum_state_radius_witness": maximum_witness,
        "terminal_state_radius_strict_upper_power_of_two_exponents":
            v141.exponents(model.total_radii()),
        "ledger_worst_depth": max(ledger.depths.values()),
        "ledger_worst_names": sorted(
            name
            for name, depth in ledger.depths.items()
            if depth == max(ledger.depths.values())
        ),
        "terminal_phase_fixed_dyadic_outer_bits": 128,
        "terminal_normal_x_fixed_dyadic_outer":
            fixed_outer(terminal_phase["normal_x"], 128),
        "terminal_normal_y_fixed_dyadic_outer":
            fixed_outer(terminal_phase["normal_y"], 128),
        "terminal_p_fixed_dyadic_outer":
            fixed_outer(terminal_phase["p"], 128),
        "terminal_cosine_fixed_dyadic_outer":
            fixed_outer(terminal_phase["cosine"], 128),
    }


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


def _cell_worker(arguments: tuple[str, int, int]) -> tuple[str, dict[str, Any]]:
    label, index, precision = arguments
    return label, replay_cell(index, precision)


def replay_cells(precision: int) -> dict[str, dict[str, Any]]:
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=2, mp_context=context) as executor:
        return dict(executor.map(
            _cell_worker,
            [
                (label, index, precision)
                for label, index in CELL_SPECS
            ],
        ))


def replay_event(precision_bits: int) -> dict[str, Any]:
    require(precision_bits >= PRIMARY_PRECISION_BITS, "event precision")
    ctx.prec = precision_bits
    owners, root = load_transitive_inputs()
    h_q = Q(1, 2**POWER)
    h = r139.lower.aq(h_q)
    x_center, x_radius = -3 * h / 2, h / 2
    beta_lower, beta_upper = 2 * h, 6 * h
    beta_center, beta_radius = 4 * h, 2 * h
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + symmetric((root_upper - root_lower) / 2)
    )
    whole = anchor_discriminant(
        x_center + symmetric(x_radius),
        beta_center + symmetric(beta_radius),
        t_star,
        owners,
    )
    corridor = anchor_discriminant(
        x_center + symmetric(x_radius),
        7 * h / 2 + symmetric(5 * h / 2),
        t_star,
        owners,
    )
    bottom = anchor_discriminant(-h, beta_lower, t_star, owners)
    top = anchor_discriminant(-2 * h, beta_upper, t_star, owners)
    shared = anchor_discriminant(-h, h, t_star, owners)
    positive = anchor_discriminant(-h, 3 * h, t_star, owners)
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0)
        and bool(corridor.derivative[0] > 0)
        and bool(corridor.derivative[1] > 0)
        and bool(bottom.value < 0)
        and bool(top.value > 0)
        and bool(shared.value < 0)
        and bool(positive.value > 0),
        "event signs",
    )
    center_value = anchor_discriminant(
        x_center,
        beta_center,
        t_star,
        owners,
    )
    mean_value = (
        center_value.value
        + whole.derivative[0] * symmetric(x_radius)
    )
    newton = beta_center - mean_value / whole.derivative[1]
    require(
        bool(newton > beta_lower)
        and bool(newton < beta_upper),
        "event Newton inclusion",
    )
    slope = -whole.derivative[0] / whole.derivative[1]
    require(bool(slope < 0), "event slope")
    return {
        "event_kind": "COLLISION3_D0_TANGENCY_D3_ZERO",
        "anchor_candidate": r139.ANCHOR,
        "physical_parameter_box": {
            "delta_x": [qstr(-2 * h_q), qstr(-h_q)],
            "delta_beta": [qstr(2 * h_q), qstr(6 * h_q)],
        },
        "event_function": "D3(delta_x,delta_beta)",
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "bottom_edge_D3_strict_negative": True,
        "top_edge_D3_strict_positive": True,
        "unique_beta_root_for_every_fixed_delta_x": True,
        "parametric_interval_Newton_center_beta": qstr(4 * h_q),
        "parametric_interval_Newton_image_in_h_units":
            fixed_outer(newton / h, 256),
        "parametric_interval_Newton_strictly_inside_event_beta_box":
            True,
        "Jacobian_outer": {
            "partial_D3_partial_delta_x":
                fixed_outer(whole.derivative[0], 128),
            "partial_D3_partial_delta_beta":
                fixed_outer(whole.derivative[1], 128),
        },
        "transverse_to_beta_fibres": True,
        "implicit_graph_slope_outer": fixed_outer(slope, 128),
        "implicit_graph_slope_strict_negative": True,
        "central_x_single_Newton_estimate_beta_in_h_units":
            fixed_outer(
                (
                    beta_center
                    - center_value.value / center_value.derivative[1]
                ) / h,
                256,
            ),
        "certified_cell_upper_shared_face_beta": qstr(h_q),
        "D3_negative_on_whole_shared_face": True,
        "positive_transverse_neighbor": {
            "delta_beta": [qstr(h_q), qstr(3 * h_q)],
            "shares_exact_artificial_face": True,
            "D3_event_enters_neighbor": True,
            "whole_neighbor_has_frozen_owner_path": False,
        },
        "negative_transverse_neighbor": {
            "delta_beta": [qstr(-3 * h_q), qstr(-h_q)],
            "shares_exact_artificial_face": True,
            "D3_event_enters_neighbor": False,
            "complete_path_audit_in_this_result": True,
        },
        "positive_beta_corridor_from_certified_face": {
            "physical_parameter_box": {
                "delta_x": [qstr(-2 * h_q), qstr(-h_q)],
                "delta_beta": [qstr(h_q), qstr(6 * h_q)],
            },
            "D3_strictly_increasing_in_delta_x": True,
            "D3_strictly_increasing_in_delta_beta": True,
            "partial_D3_partial_delta_x_outer":
                fixed_outer(corridor.derivative[0], 128),
            "partial_D3_partial_delta_beta_outer":
                fixed_outer(corridor.derivative[1], 128),
            "shared_face_D3_strict_negative": True,
            "event_box_bottom_D3_strict_negative": True,
            "no_earlier_D3_zero_between_shared_face_and_event_box":
                True,
        },
        "event_curve_is_local_not_exhaustive_global_frontier": True,
    }


EXPECTED_NONPROMOTION = {
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
}


EXPECTED_NONCLAIMS = [
    "the numerical t_star enclosure is an interval constant, not a third physical coordinate",
    "the positive transverse neighbor is event-entering and has no whole-cell frozen-path claim",
    "the local two-cell atlas is not a maximal two-dimensional component atlas",
    "the local D3 event graph does not exhaust every global exit or event frontier",
    "Round144 D02 remains blocked, so D03 and every downstream corrected identifier remain unavailable",
    "no historical Round27 or Round35 identity is inferred from prospective Round137-v1 coordinates",
    "no Round50 owner, Round54 token, Round67 q_j, Gate5 field, or CM2 claim is promoted",
]


def validate_dependencies() -> None:
    require(
        sha256(PRODUCER) == PRODUCER_SHA256,
        "producer pin",
    )
    require(sha256(ENGINE) == ENGINE_SHA256, "engine pin")
    for name, expected in DIRECT_PINS.items():
        require(
            sha256(HERE / name) == expected,
            f"direct dependency:{name}",
        )
    require(
        sha256(
            HERE
            / "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
        ) == DIRECT_PINS[
            "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
        ]
        and Path(v141.__file__).resolve()
        == (
            HERE
            / "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
        ).resolve(),
        "loaded Round141 verifier identity",
    )
    require(
        Path(r141p.__file__).resolve()
        == (
            HERE
            / "cm2_round141_recentered_affine_k4296_d0_collar_return.py"
        ).resolve(),
        "loaded Round141 producer identity",
    )
    # This frozen guard pins the Round139 source/certificate/verifier and its
    # lower numerical dependency stack used transitively below.
    r141p.validate_dependencies()


def preflight_certificate() -> dict[str, Any]:
    """Reject an unclosed certificate before any expensive reconstruction."""

    require(
        sha256(CERTIFICATE) == CERTIFICATE_SHA256,
        "certificate file pin",
    )
    document = r139.strict_json(CERTIFICATE)
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and document["result_sha256"] == CERTIFICATE_RESULT_SHA256
        and digest(document["result"]) == CERTIFICATE_RESULT_SHA256,
        "certificate preflight closure",
    )
    return document


def validate_semantics(
    document: dict[str, Any],
    replays: dict[str, dict[str, Any]],
    event: dict[str, Any],
    check_closure: bool = True,
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA,
        "certificate envelope",
    )
    if check_closure:
        require(
            sha256(CERTIFICATE) == CERTIFICATE_SHA256
            and document["result_sha256"] == CERTIFICATE_RESULT_SHA256
            and digest(document["result"]) == CERTIFICATE_RESULT_SHA256,
            "certificate closure",
        )
    else:
        require(
            document["result_sha256"] == digest(document["result"]),
            "mutated closure",
        )
    result = document["result"]
    require(
        set(result) == {
            "status",
            "minimum_certified_precision_bits",
            "secondary_verifier_precision_bits",
            "provenance",
            "source_identity",
            "physical_centered_coordinates",
            "local_connected_two_cell_atlas",
            "positive_transverse_event_frontier",
            "first_collision3_D0_event_in_positive_beta_direction",
            "Round144_D02_status",
            "count_ledger",
            "strict_nonpromotion",
            "strict_nonclaims",
        }
        and result["status"] == CERTIFICATE_STATUS
        and type(result["minimum_certified_precision_bits"]) is int
        and result["minimum_certified_precision_bits"]
        == PRIMARY_PRECISION_BITS
        and type(result["secondary_verifier_precision_bits"]) is int
        and result["secondary_verifier_precision_bits"]
        == SECONDARY_PRECISION_BITS,
        "top-level semantics",
    )
    provenance = result["provenance"]
    require(
        typed_equal(provenance, {
            "producer_sha256": PRODUCER_SHA256,
            "engine_sha256": ENGINE_SHA256,
            "direct_frozen_dependency_rounds": [140, 141, 142, 144],
            "direct_dependency_sha256": dict(sorted(DIRECT_PINS.items())),
            "Round141_transitive_dependency_guard_replayed": True,
            "append_only": True,
            "Round140_Round141_Round142_Round144_files_modified": False,
        }),
        "provenance",
    )
    source = result["source_identity"]
    require(
        typed_equal(source, {
            "fixed_parameter_s": "0",
            "source_core_id":
                "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7",
            "return_depth_n": RETURN_DEPTH,
            "Round27_compatible_path_tuple_sha256":
                "5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9",
            "official_word_sequence_sha256":
                r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256,
            "Round140_adaptive_path_cell_id":
                "round140-fixed-s0-adaptive-path-cell:a4a3be3cf7115abec08f372382ca7a863838e963a7d03af400d6a6ca58812b6a",
            "Round140_positive_area_seed_exists": True,
        }),
        "source identity",
    )
    coordinates = result["physical_centered_coordinates"]
    require(
        type(coordinates["generator_count"]) is int
        and coordinates["generator_count"] == 2
        and typed_equal(
            coordinates["generators"],
            ["delta_x", "delta_beta"],
        )
        and coordinates["delta_x_definition"]
        == "x-x_star, x=sqrt(17)*r"
        and coordinates["delta_beta_definition"]
        == "(asin(p)-4*r)-b_star"
        and typed_equal(coordinates["exact_initial_map"], {
            "t":
                "sin(asin(t_star)+delta_x/(R_W*sqrt(17)))",
            "p":
                "sin(asin(p_star)+4*delta_x/sqrt(17)+delta_beta)",
        })
        and typed_equal(coordinates["angle_coordinate_Jacobian"], {
            "rows": [
                ["1/(R_W*sqrt(17))", "0"],
                ["4/sqrt(17)", "1"],
            ],
            "determinant": "1/(R_W*sqrt(17))",
            "determinant_strict_positive": True,
        })
        and coordinates[
            "t_star_numerical_enclosure_is_physical_generator"
        ] is False
        and coordinates[
            "t_star_numerical_enclosure_charged_to_initial_remainder"
        ] is True
        and type(coordinates["coordinate_rank"]) is int
        and coordinates["coordinate_rank"] == 2
        and coordinates["coordinate_Jacobian_nondegenerate"] is True,
        "physical coordinates",
    )
    expected_cells = [
        compact_cell("negative", replays["negative"]),
        compact_cell("central", replays["central"]),
    ]
    atlas = result["local_connected_two_cell_atlas"]
    h = Q(1, 2**POWER)
    face_payload = {
        "delta_x": [qstr(-2 * h), qstr(-h)],
        "delta_beta": qstr(-h),
    }
    face_id = (
        "round146-artificial-shared-beta-face:" + digest(face_payload)
    )
    atlas_payload = {
        "cells": [row["cell_id"] for row in expected_cells],
        "shared_face": face_id,
        "path": r139.EXPECTED_COMPACT_PATH_SHA256,
    }
    require(
        atlas["atlas_id"]
        == "round146-local-physical-2d-two-cell-atlas:"
        + digest(atlas_payload)
        and atlas["payload_sha256"] == digest(atlas_payload)
        and atlas["h"] == qstr(h)
        and atlas["delta_x_closed_interval"]
        == [qstr(-2 * h), qstr(-h)]
        and atlas["delta_beta_certified_union"]
        == [qstr(-3 * h), qstr(h)]
        and type(atlas["cell_count"]) is int
        and atlas["cell_count"] == 2
        and typed_equal(atlas["cells"], expected_cells)
        and type(atlas["internal_shared_face_count"]) is int
        and atlas["internal_shared_face_count"] == 1
        and typed_equal(atlas["internal_shared_face"], {
            "face_id": face_id,
            "delta_x_closed_interval": [qstr(-2 * h), qstr(-h)],
            "delta_beta": qstr(-h),
            "negative_cell_upper_face": True,
            "central_cell_lower_face": True,
            "exactly_shared": True,
            "same_exact_physical_initial_map": True,
            "same_1648_selected_circle_composition": True,
        })
        and atlas["adjacency_graph"] == "path_on_2_vertices"
        and atlas["adjacency_graph_connected"] is True
        and atlas["both_cells_complete_full_R1648_audit"] is True
        and atlas[
            "same_owner_word_chart_homogeneity_incidence_C24_path"
        ] is True
        and type(atlas["full_radius4_candidate_test_count"]) is int
        and atlas["full_radius4_candidate_test_count"]
        == 2 * 161 * RETURN_DEPTH
        and type(
            atlas["preterminal_strict_nonreturn_cell_stage_count"]
        ) is int
        and atlas["preterminal_strict_nonreturn_cell_stage_count"]
        == 2 * (RETURN_DEPTH - 1)
        and type(atlas["terminal_strict_return_cell_count"]) is int
        and atlas["terminal_strict_return_cell_count"] == 2,
        "two-cell atlas",
    )
    require(
        typed_equal(
            result["positive_transverse_event_frontier"],
            event,
        ),
        "independent event reconstruction",
    )
    first = result[
        "first_collision3_D0_event_in_positive_beta_direction"
    ]
    require(
        typed_equal(first, {
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
        }),
        "first local physical event",
    )
    d02 = result["Round144_D02_status"]
    require(
        typed_equal(d02, {
            "node_id": "D02",
            "operation": "complete_2D_centered_jet_outer_atlas",
            "frozen_blocker_row_sha256":
                "a25e021d4386ae25437efdd2c658533bb579e195894036b0ab6e26ae0f0b4132",
            "frozen_DAG_row_sha256":
                "9bca02effa51c0cfb6da042c131cdd58fa4cce2bcfc6f133faf5fb5a379733b0",
            "frozen_status": "BLOCKED",
            "local_two_cell_atlas_closes_D02": False,
            "reason":
                "two cells and one local D3 event graph do not exhaust all outer-atlas cells, exits, and event frontiers of the maximal two-dimensional component",
            "maximal_component_outer_atlas_complete": False,
            "all_event_frontiers_exhausted": False,
            "D03_least_rank_negative_oracle_authorized": False,
        }),
        "D02 fail-closed status",
    )
    require(
        typed_equal(result["count_ledger"], {
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
        })
        and typed_equal(
            result["strict_nonpromotion"],
            EXPECTED_NONPROMOTION,
        )
        and typed_equal(result["strict_nonclaims"], EXPECTED_NONCLAIMS),
        "counts and nonpromotion",
    )


def semantic_attack_self_test(
    document: dict[str, Any],
    replays: dict[str, dict[str, Any]],
    event: dict[str, Any],
) -> dict[str, Any]:
    attacks = [
        ("status", lambda r: r.__setitem__("status", "CERTIFIED")),
        (
            "generator_count",
            lambda r: r["physical_centered_coordinates"].__setitem__(
                "generator_count", 3
            ),
        ),
        (
            "tstar_generator",
            lambda r: r["physical_centered_coordinates"].__setitem__(
                "t_star_numerical_enclosure_is_physical_generator", True
            ),
        ),
        (
            "coordinate_rank",
            lambda r: r["physical_centered_coordinates"].__setitem__(
                "coordinate_rank", 1
            ),
        ),
        (
            "cell_count",
            lambda r: r["local_connected_two_cell_atlas"].__setitem__(
                "cell_count", 1
            ),
        ),
        (
            "cell_path",
            lambda r: r["local_connected_two_cell_atlas"]["cells"][0].__setitem__(
                "compact_path_sha256", "0" * 64
            ),
        ),
        (
            "cell_candidates",
            lambda r: r["local_connected_two_cell_atlas"]["cells"][1].__setitem__(
                "full_radius4_candidate_test_count", 0
            ),
        ),
        (
            "cell_radius",
            lambda r: r["local_connected_two_cell_atlas"]["cells"][0].__setitem__(
                "maximum_state_radius_strict_upper_power_of_two_exponent", 0
            ),
        ),
        (
            "shared_face",
            lambda r: r["local_connected_two_cell_atlas"][
                "internal_shared_face"
            ].__setitem__("exactly_shared", False),
        ),
        (
            "adjacency",
            lambda r: r["local_connected_two_cell_atlas"].__setitem__(
                "adjacency_graph_connected", False
            ),
        ),
        (
            "event_dbeta",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "D3_strictly_increasing_in_delta_beta", False
            ),
        ),
        (
            "event_bottom",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "bottom_edge_D3_strict_negative", False
            ),
        ),
        (
            "event_top",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "top_edge_D3_strict_positive", False
            ),
        ),
        (
            "event_unique",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "unique_beta_root_for_every_fixed_delta_x", False
            ),
        ),
        (
            "event_newton",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "parametric_interval_Newton_strictly_inside_event_beta_box",
                False,
            ),
        ),
        (
            "positive_path",
            lambda r: r["positive_transverse_event_frontier"][
                "positive_transverse_neighbor"
            ].__setitem__("whole_neighbor_has_frozen_owner_path", True),
        ),
        (
            "first_event_claim",
            lambda r: r[
                "first_collision3_D0_event_in_positive_beta_direction"
            ].__setitem__("next_positive_neighbor_complete_path_claimed", True),
        ),
        (
            "d02",
            lambda r: r["Round144_D02_status"].__setitem__(
                "local_two_cell_atlas_closes_D02", True
            ),
        ),
        (
            "maximal",
            lambda r: r["Round144_D02_status"].__setitem__(
                "maximal_component_outer_atlas_complete", True
            ),
        ),
        (
            "exhausted",
            lambda r: r["Round144_D02_status"].__setitem__(
                "all_event_frontiers_exhausted", True
            ),
        ),
        (
            "d03",
            lambda r: r["Round144_D02_status"].__setitem__(
                "D03_least_rank_negative_oracle_authorized", True
            ),
        ),
        (
            "component",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "Round137_v1_component_id", "invented"
            ),
        ),
        (
            "rank",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "Round137_v1_maximal_component_rank", 0
            ),
        ),
        (
            "restriction",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "historical_Round35_rn_restriction_id", "invented"
            ),
        ),
        (
            "gate5",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "Gate5", "CERTIFIED"
            ),
        ),
        (
            "cm2",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "CM2", "GO"
            ),
        ),
        (
            "dependency_round",
            lambda r: r["provenance"].__setitem__(
                "direct_frozen_dependency_rounds", [146]
            ),
        ),
        (
            "nonclaim",
            lambda r: r.__setitem__("strict_nonclaims", []),
        ),
        (
            "result_extra_key",
            lambda r: r.__setitem__("unexpected", None),
        ),
        (
            "producer_pin",
            lambda r: r["provenance"].__setitem__(
                "producer_sha256", "0" * 64
            ),
        ),
        (
            "engine_pin",
            lambda r: r["provenance"].__setitem__(
                "engine_sha256", "0" * 64
            ),
        ),
        (
            "exact_initial_p_map",
            lambda r: r["physical_centered_coordinates"][
                "exact_initial_map"
            ].__setitem__("p", "wrong"),
        ),
        (
            "angle_jacobian_determinant",
            lambda r: r["physical_centered_coordinates"][
                "angle_coordinate_Jacobian"
            ].__setitem__("determinant", "0"),
        ),
        (
            "atlas_x_interval",
            lambda r: r["local_connected_two_cell_atlas"].__setitem__(
                "delta_x_closed_interval", ["0", "1"]
            ),
        ),
        (
            "atlas_beta_union",
            lambda r: r["local_connected_two_cell_atlas"].__setitem__(
                "delta_beta_certified_union", ["0", "1"]
            ),
        ),
        (
            "cell_id",
            lambda r: r["local_connected_two_cell_atlas"]["cells"][0].__setitem__(
                "cell_id", "invented"
            ),
        ),
        (
            "cell_ledger_sha",
            lambda r: r["local_connected_two_cell_atlas"]["cells"][0].__setitem__(
                "model_radius_ledger_sha256", "0" * 64
            ),
        ),
        (
            "shared_face_id",
            lambda r: r["local_connected_two_cell_atlas"][
                "internal_shared_face"
            ].__setitem__("face_id", "invented"),
        ),
        (
            "event_dx_sign",
            lambda r: r["positive_transverse_event_frontier"].__setitem__(
                "D3_strictly_increasing_in_delta_x", False
            ),
        ),
        (
            "event_jacobian_outer",
            lambda r: r["positive_transverse_event_frontier"][
                "Jacobian_outer"
            ].__setitem__("partial_D3_partial_delta_beta", ["0", "0"]),
        ),
        (
            "event_corridor_no_earlier_zero",
            lambda r: r["positive_transverse_event_frontier"][
                "positive_beta_corridor_from_certified_face"
            ].__setitem__(
                "no_earlier_D3_zero_between_shared_face_and_event_box",
                False,
            ),
        ),
        (
            "negative_neighbor_complete_audit",
            lambda r: r["positive_transverse_event_frontier"][
                "negative_transverse_neighbor"
            ].__setitem__("complete_path_audit_in_this_result", False),
        ),
        (
            "D02_frozen_blocker_hash",
            lambda r: r["Round144_D02_status"].__setitem__(
                "frozen_blocker_row_sha256", "0" * 64
            ),
        ),
        (
            "count_ledger",
            lambda r: r["count_ledger"].__setitem__(
                "full_radius4_candidate_test_count", 0
            ),
        ),
        (
            "true_as_one",
            lambda r: r["source_identity"].__setitem__(
                "Round140_positive_area_seed_exists", 1
            ),
        ),
        (
            "false_as_zero",
            lambda r: r["Round144_D02_status"].__setitem__(
                "local_two_cell_atlas_closes_D02", 0
            ),
        ),
        (
            "one_as_true_count",
            lambda r: r["local_connected_two_cell_atlas"].__setitem__(
                "internal_shared_face_count", True
            ),
        ),
        (
            "zero_as_false_nonpromotion",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "global_complete_18_field_block_count", False
            ),
        ),
    ]
    rejected: list[str] = []
    for label, mutate in attacks:
        attacked = copy.deepcopy(document)
        mutate(attacked["result"])
        attacked["result_sha256"] = digest(attacked["result"])
        try:
            validate_semantics(
                attacked,
                replays,
                event,
                check_closure=False,
            )
        except (KeyError, RuntimeError, TypeError, ValueError):
            rejected.append(label)
    stale = copy.deepcopy(document)
    stale["result_sha256"] = "0" * 64
    try:
        validate_semantics(
            stale,
            replays,
            event,
            check_closure=False,
        )
    except (KeyError, RuntimeError, TypeError, ValueError):
        rejected.append("stale_result_sha")
    extra = copy.deepcopy(document)
    extra["unexpected"] = None
    try:
        validate_semantics(
            extra,
            replays,
            event,
            check_closure=False,
        )
    except (KeyError, RuntimeError, TypeError, ValueError):
        rejected.append("envelope_extra_key")
    expected_count = len(attacks) + 2
    require(len(rejected) == expected_count, "semantic attacks")
    return {
        "attack_count": expected_count,
        "rejected_attack_count": len(rejected),
        "labels": rejected,
    }


def strict_json_self_test() -> dict[str, Any]:
    fixtures = {
        "duplicate_key": '{"schema":"x","schema":"y"}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "negative_infinity": '{"x":-Infinity}',
        "top_level_array": "[]",
        "top_level_string": '"x"',
        "trailing_data": '{"x":1}{}',
        "decimal_float": '{"x":1.25}',
        "exponent_float": '{"x":1e2}',
        "nested_duplicate": '{"x":{"a":1,"a":2}}',
        "top_level_null": "null",
        "top_level_boolean": "true",
        "top_level_number": "1",
        "empty": "",
        "truncated": '{"x":',
        "utf8_bom": '\ufeff{"x":1}',
    }
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cm2-r146-json-") as directory:
        root = Path(directory)
        for label, payload in fixtures.items():
            path = root / f"{label}.json"
            path.write_text(payload, encoding="utf-8")
            try:
                r139.strict_json(path)
            except (json.JSONDecodeError, RuntimeError, TypeError, ValueError):
                rejected.append(label)
        invalid_utf8 = root / "invalid-utf8.json"
        invalid_utf8.write_bytes(b"\xff")
        try:
            r139.strict_json(invalid_utf8)
        except (OSError, RuntimeError, UnicodeDecodeError, ValueError):
            rejected.append("invalid_utf8")
        regular = root / "regular.json"
        regular.write_text('{"x":1}', encoding="utf-8")
        symlink = root / "symlink.json"
        symlink.symlink_to(regular)
        try:
            r139.strict_json(symlink)
        except (OSError, RuntimeError):
            rejected.append("symlink")
        hardlink = root / "hardlink.json"
        os.link(regular, hardlink)
        try:
            r139.strict_json(regular)
        except (OSError, RuntimeError):
            rejected.append("hardlink")
        directory = root / "directory.json"
        directory.mkdir()
        try:
            r139.strict_json(directory)
        except (OSError, RuntimeError):
            rejected.append("directory")
        fifo = root / "fifo.json"
        os.mkfifo(fifo)
        try:
            r139.strict_json(fifo)
        except (OSError, RuntimeError):
            rejected.append("fifo")
    require(len(rejected) == 21, "strict JSON attacks")
    return {
        "attack_count": 21,
        "rejected_attack_count": len(rejected),
        "labels": sorted(rejected),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        PRODUCER.resolve(),
        ENGINE.resolve(),
        CERTIFICATE.resolve(),
        *((HERE / name).resolve() for name in DIRECT_PINS),
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


def path_safety_self_test() -> dict[str, Any]:
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cm2-r146-path-") as directory:
        root = Path(directory)
        regular = root / "regular.json"
        validate_output_target(regular)
        regular.write_text("sentinel", encoding="utf-8")
        hard = root / "hard.json"
        os.link(regular, hard)
        try:
            validate_output_target(regular)
        except (OSError, RuntimeError):
            rejected.append("hardlink")
        hard.unlink()
        symlink = root / "symlink.json"
        symlink.symlink_to(regular)
        try:
            validate_output_target(symlink)
        except (OSError, RuntimeError):
            rejected.append("symlink")
        alias = root / "producer-alias"
        alias.symlink_to(PRODUCER)
        try:
            validate_output_target(alias)
        except (OSError, RuntimeError):
            rejected.append("producer_alias")
        parent_link = root / "parent-link"
        parent_link.symlink_to(root, target_is_directory=True)
        try:
            validate_output_target(parent_link / "x.json")
        except (OSError, RuntimeError):
            rejected.append("symlink_parent")
        for label, path in (
            ("producer", PRODUCER),
            ("certificate", CERTIFICATE),
            ("engine", ENGINE),
        ):
            try:
                validate_output_target(path)
            except (OSError, RuntimeError):
                rejected.append(label)
    require(len(rejected) == 7, "path attacks")
    return {
        "attack_count": 7,
        "rejected_attack_count": len(rejected),
        "labels": sorted(rejected),
    }


def build_verification() -> dict[str, Any]:
    validate_dependencies()
    document = preflight_certificate()
    primary = replay_cells(PRIMARY_PRECISION_BITS)
    event_primary = replay_event(PRIMARY_PRECISION_BITS)
    validate_semantics(document, primary, event_primary)
    event_secondary = replay_event(SECONDARY_PRECISION_BITS)
    require(
        typed_equal(event_secondary, event_primary),
        "dual-precision event identity",
    )
    semantic = semantic_attack_self_test(
        document,
        primary,
        event_primary,
    )
    strict_json = strict_json_self_test()
    path_safety = path_safety_self_test()
    compact = [
        compact_cell("negative", primary["negative"]),
        compact_cell("central", primary["central"]),
    ]
    result = {
        "status": "PASS",
        "verifier_independence": {
            "imports_Round146_producer": False,
            "imports_Round146_engine": False,
            "independent_physical_initial_map": True,
            "independent_two_cell_affine_reconstruction": True,
            "independent_transverse_D3_event_reconstruction": True,
            "frozen_Round141_independent_affine_primitives_reused": True,
        },
        "pins": {
            "producer_sha256": PRODUCER_SHA256,
            "certificate_sha256": CERTIFICATE_SHA256,
            "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
            "engine_sha256": ENGINE_SHA256,
            "direct_dependency_sha256":
                dict(sorted(DIRECT_PINS.items())),
        },
        "primary_complete_reconstruction": {
            "precision_bits": PRIMARY_PRECISION_BITS,
            "complete_2D_cell_count": 2,
            "cells": compact,
            "cells_sha256": digest(compact),
            "collision_stage_cell_pairs": 2 * RETURN_DEPTH,
            "full_radius4_candidate_test_count":
                2 * 161 * RETURN_DEPTH,
            "all_semantics_match_certificate": True,
        },
        "event_precision_replay": {
            "primary_precision_bits": PRIMARY_PRECISION_BITS,
            "secondary_precision_bits": SECONDARY_PRECISION_BITS,
            "primary_event_sha256": digest(event_primary),
            "secondary_event_sha256": digest(event_secondary),
            "byte_identity_after_canonicalization": True,
        },
        "semantic_attack_self_test": semantic,
        "strict_json_self_test": strict_json,
        "path_safety_self_test": path_safety,
        "D02_remains_blocked": True,
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    supplied_certificate = args.certificate.absolute()
    require(
        not supplied_certificate.is_symlink()
        and supplied_certificate == CERTIFICATE.absolute()
        and supplied_certificate.resolve() == CERTIFICATE.resolve(),
        "exact pinned regular certificate path",
    )
    validate_output_target(args.output)
    document = build_verification()
    atomic_write(args.output, document)
    print(canonical({
        "schema": document["schema"],
        "result_sha256": document["result_sha256"],
        "output": str(args.output.absolute()),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
