#!/usr/bin/env python3
"""Independent verifier for the Round141 recentered-affine D0 collar.

The verifier does not import the Round141 producer or its centered engine.
It independently implements the two-generator affine recurrence using the
generic first-order dual numbers from the fixed-section module, reconstructs
all 1648 collisions at 8192 and 12288 bits, and repeats every retained,
radius-four, official-wall, chart, homogeneity/incidence, and C24 decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Sequence

from flint import arb, ctx

import cm2_fixed_section_common_vertex_cert as ad
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PRODUCER = (
    HERE / "cm2_round141_recentered_affine_k4296_d0_collar_return.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round141-recentered-affine-k4296-d0-collar-return-verification-2026-07-24.json"
)
ENGINE = HERE / "cm2_round141_centered_affine_d0_collar_spike.py"
SCHEMA = (
    "cm2.round141.recentered-affine-k4296-d0-collar-return-verification.v1"
)
CERTIFICATE_SCHEMA = (
    "cm2.round141.recentered-affine-k4296-d0-collar-return.v1"
)
PRIMARY_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
X_COLLAR_POWER = 4296
RETURN_DEPTH = 1648

PRODUCER_SHA256 = "687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28"
CERTIFICATE_SHA256 = "a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe"
CERTIFICATE_RESULT_SHA256 = "48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f"
ENGINE_SHA256 = "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1"
R139_CERTIFICATE_SHA256 = (
    "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
)


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


def dual_rows(values: Sequence[ad.Dual]) -> list[list[arb]]:
    return [list(value.derivative) for value in values]


@dataclass
class AffineState:
    point_state: list[arb]
    generators: list[list[arb]]
    errors: list[arb]
    parameter_radii: tuple[arb, arb]

    def affine_radii(self) -> list[arb]:
        return [
            sum(
                self.generators[row][column].abs_upper()
                * self.parameter_radii[column]
                for column in range(2)
            )
            for row in range(4)
        ]

    def total_radii(self) -> list[arb]:
        affine = self.affine_radii()
        return [
            affine[row] + self.errors[row]
            for row in range(4)
        ]

    def boxes(self) -> list[arb]:
        return [
            self.point_state[row] + symmetric(radius)
            for row, radius in enumerate(self.total_radii())
        ]


def target(identifier: str) -> tuple[tuple[arb, arb], arb]:
    center = r139.lower.time3.time2_cert.target_center(identifier, arb(0))
    radius = r139.lower.aq(
        r139.lower.time3.time2_cert.first_hit.RADIUS[identifier[0]]
    )
    return center, radius


def ray_map(
    state: Sequence[ad.Dual],
    center: tuple[arb, arb],
    radius: arb,
) -> tuple[list[ad.Dual], tuple[ad.Dual, ad.Dual, ad.Dual]]:
    position, velocity = state[:2], state[2:]
    displacement = (
        position[0] - center[0],
        position[1] - center[1],
    )
    linear = ad.dual_dot(displacement, velocity)
    offset = ad.dual_dot(displacement, displacement) - radius * radius
    discriminant = linear * linear - offset
    require(bool(discriminant.value > 0), "map discriminant")
    flight = -linear - ad.dual_sqrt(discriminant)
    require(bool(flight.value > 0), "map forward flight")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - center[0]) / radius,
        (impact[1] - center[1]) / radius,
    )
    incoming = -ad.dual_dot(velocity, normal)
    reflected = (
        velocity[0] + 2 * incoming * normal[0],
        velocity[1] + 2 * incoming * normal[1],
    )
    return list(impact + reflected), (flight, discriminant, incoming)


def exact_leaf_initial(z: ad.Dual, t_star: ad.Dual) -> list[ad.Dual]:
    sqrt17 = arb(17).sqrt()
    angle = (
        dual_asin(t_star)
        + z / (r139.lower.aq(r139.lower.R_W) * sqrt17)
    )
    t = ad.dual_sin(angle)
    p_phase = (
        ad.Dual(
            r139.lower.aq(r139.lower.SOURCE_P_STAR).asin(),
            dimension=2,
        )
        + 4 * z / sqrt17
    )
    p = ad.dual_sin(p_phase)
    nx, ny = ad.dual_cos(angle), t
    radial = ad.dual_sqrt(ad.Dual(1, dimension=2) - p * p)
    velocity = (
        radial * nx - p * ny,
        radial * ny + p * nx,
    )
    center, radius = target(r139.lower.SOURCE_ABSOLUTE_OWNER)
    position = (
        ad.Dual(center[0], dimension=2) + radius * nx,
        ad.Dual(center[1], dimension=2) + radius * ny,
    )
    return list(position + velocity)


def initial_affine(root: tuple[Q, Q]) -> AffineState:
    width = r139.lower.aq(Q(1, 2**X_COLLAR_POWER))
    z_center, z_radius = -width / 2, width / 2
    root_lower, root_upper = map(r139.lower.aq, root)
    root_center = (root_lower + root_upper) / 2
    root_radius = (root_upper - root_lower) / 2
    center_values = exact_leaf_initial(
        ad.Dual(z_center, [arb(1), arb(0)]),
        ad.Dual(root_center, [arb(0), arb(1)]),
    )
    interval_values = exact_leaf_initial(
        ad.Dual(
            z_center + symmetric(z_radius),
            [arb(1), arb(0)],
        ),
        ad.Dual(
            root_center + symmetric(root_radius),
            [arb(0), arb(1)],
        ),
    )
    raw_generators = dual_rows(center_values)
    generators = [
        [point(entry) for entry in row]
        for row in raw_generators
    ]
    interval_derivatives = dual_rows(interval_values)
    parameter_radii = (z_radius, root_radius)
    errors = [
        (center_values[row].value - point(center_values[row].value)).abs_upper()
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
    return AffineState(
        [point(value.value) for value in center_values],
        generators,
        errors,
        parameter_radii,
    )


def propagate(
    model: AffineState,
    target_id: str,
) -> tuple[AffineState, dict[str, list[arb]]]:
    input_affine = model.affine_radii()
    input_total = model.total_radii()
    boxes = [
        model.point_state[index] + symmetric(input_total[index])
        for index in range(4)
    ]
    interval_state = [
        ad.Dual(
            boxes[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center_state = [
        ad.Dual(
            model.point_state[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center, radius = target(target_id)
    center_outputs, _center_metrics = ray_map(center_state, center, radius)
    interval_outputs, _interval_metrics = ray_map(
        interval_state, center, radius
    )
    local_center = dual_rows(center_outputs)
    local_interval = dual_rows(interval_outputs)
    raw_generators = [
        [
            sum(
                local_center[row][inner]
                * model.generators[inner][column]
                for inner in range(4)
            )
            for column in range(2)
        ]
        for row in range(4)
    ]
    generators = [
        [point(entry) for entry in row]
        for row in raw_generators
    ]
    raw_errors = [
        sum(
            (
                local_interval[row][inner]
                - local_center[row][inner]
            ).abs_upper()
            * input_affine[inner]
            + local_interval[row][inner].abs_upper()
            * model.errors[inner]
            for inner in range(4)
        )
        for row in range(4)
    ]
    centers = [point(value.value) for value in center_outputs]
    center_losses = [
        (center_outputs[row].value - centers[row]).abs_upper()
        for row in range(4)
    ]
    coefficient_losses = [
        sum(
            (
                raw_generators[row][column]
                - generators[row][column]
            ).abs_upper()
            * model.parameter_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    errors = [
        raw_errors[row] + center_losses[row] + coefficient_losses[row]
        for row in range(4)
    ]
    result = AffineState(
        centers,
        generators,
        errors,
        model.parameter_radii,
    )
    return result, {
        "input_affine": input_affine,
        "input_errors": list(model.errors),
        "input_total": input_total,
        "raw_errors": raw_errors,
        "center_losses": center_losses,
        "coefficient_losses": coefficient_losses,
        "output_affine": result.affine_radii(),
        "output_errors": list(result.errors),
        "output_total": result.total_radii(),
    }


class Ledger:
    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()
        self.depths: dict[str, int] = {}
        self.witnesses: dict[str, dict[str, Any] | None] = {}

    def observe(
        self,
        name: str,
        value: arb,
        witness: dict[str, Any] | None = None,
    ) -> int:
        require(bool(value > 0), f"nonstrict margin:{name}")
        depth = r139.lower.round136.strict_dyadic_depth(value)
        self.counts[name] += 1
        if name not in self.depths or depth > self.depths[name]:
            self.depths[name] = depth
            self.witnesses[name] = witness
        return depth


def upper_exponent(value: arb) -> int | None:
    upper = value.abs_upper()
    if upper == 0:
        return None
    estimate = math.ceil(
        float((upper.log() / arb(2).log()).mid())
    )
    while not bool(upper < arb(2) ** estimate):
        estimate += 1
    while bool(upper < arb(2) ** (estimate - 1)):
        estimate -= 1
    return estimate


def exponents(values: Sequence[arb]) -> list[int | None]:
    return [upper_exponent(value) for value in values]


def phase_at_contact(
    model: AffineState,
    target_id: str,
) -> tuple[str, dict[str, arb]]:
    boxes = model.boxes()
    center, radius = target(target_id)
    nx = (boxes[0] - center[0]) / radius
    ny = (boxes[1] - center[1]) / radius
    chart = r139.lower.time3.time2_cert.strict_chart(nx, ny)
    require(chart is not None, "strict contact chart")
    p = -boxes[2] * ny + boxes[3] * nx
    cosine = boxes[2] * nx + boxes[3] * ny
    require(bool(cosine > 0), "positive reflected cosine")
    return chart, {
        "normal_x": nx,
        "normal_y": ny,
        "p": p,
        "cosine": cosine,
    }


def fixed_outer(value: arb, bits: int = 128) -> list[str]:
    raw_lower, raw_upper = r139.lower.round136.arb_pair(value)
    scale = 2**bits
    lower = Q(r139.lower.floor_q(raw_lower * scale) - 1, scale)
    upper = Q(r139.lower.ceil_q(raw_upper * scale) + 1, scale)
    require(
        lower < upper
        and bool(value > r139.lower.aq(lower))
        and bool(value < r139.lower.aq(upper)),
        "terminal padded outer",
    )
    return [r139.qstr(lower), r139.qstr(upper)]


def reconstruct(precision_bits: int) -> dict[str, Any]:
    require(precision_bits >= PRIMARY_PRECISION_BITS, "replay precision")
    ctx.prec = precision_bits
    r139_path = (
        HERE
        / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
    )
    require(sha256(r139_path) == R139_CERTIFICATE_SHA256, "Round139 pin")
    r139_document = r139.strict_json(r139_path)
    r139_result = r139_document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in r139_result["collision_rows"]
    ]
    require(
        len(owners) == RETURN_DEPTH
        and digest(owners) == r139.EXPECTED_OWNER_SEQUENCE_SHA256,
        "frozen owner sequence input",
    )
    root = tuple(
        Q(value)
        for value in r139_result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model = initial_affine(root)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    cores = tuple(r139.lower.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = (
        r139.lower.component_cert.key_index_tables()
    )
    require(
        registry_sha == r139.OFFICIAL_REGISTRY_SHA256,
        "registry digest",
    )
    initial_boxes = model.boxes()
    source_center, source_radius = target(current_target)
    source_nx = (initial_boxes[0] - source_center[0]) / source_radius
    source_ny = (initial_boxes[1] - source_center[1]) / source_radius
    source_p = (
        -initial_boxes[2] * source_ny
        + initial_boxes[3] * source_nx
    )
    previous_cosine = (1 - source_p * source_p).sqrt()
    ledger = Ledger()
    official_ids: list[str] = []
    compact_rows: list[list[Any]] = []
    homogeneity: Counter[str] = Counter()
    incidence: Counter[int] = Counter()
    radius_rows: list[list[Any]] = []
    maximum_radius = arb(0)
    maximum_witness: list[int] | None = None
    terminal_phase: dict[str, arb] | None = None
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        boxes = model.boxes()
        state = {
            "contact_x": boxes[0],
            "contact_y": boxes[1],
            "outgoing_x": boxes[2],
            "outgoing_y": boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        if collision_index == r139.ANCHOR_COLLISION_INDEX:
            retained_candidates = tuple(
                r139.lower.time3.time2_cert.translated_candidate_ids(
                    current_target, current_chart
                )
            )
            owner, _retained = r139.candidates_owner_excluding_anchor(
                state,
                current_target,
                retained_candidates,
                ledger,
                collision_index,
                False,
            )
            full_owner, _full = r139.candidates_owner_excluding_anchor(
                state,
                current_target,
                r139.lower.charge.candidate_ids_around(current_target),
                ledger,
                collision_index,
                True,
            )
            require(
                full_owner["selected_target_id"]
                == owner["selected_target_id"],
                "anchor retained/full owner",
            )
        else:
            owner, _retained = r139.lower.round136.complete_owner(
                state, current_target, ledger, collision_index
            )
            _full = r139.lower.full_radius4_candidate_audit(
                state, current_target, owner, ledger, collision_index
            )
        require(
            owner["selected_target_id"] == expected_owner,
            f"frozen owner:{collision_index}",
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
            f"official word:{collision_index}:{word_error}",
        )
        r139.official_wall_margin_audit(
            state, current_target, owner, ledger, collision_index
        )
        model, model_audit = propagate(model, expected_owner)
        for component, radius in enumerate(model_audit["output_total"]):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_witness = [
                    collision_index,
                    component,
                    upper_exponent(radius),
                ]
        radius_rows.append([
            collision_index,
            exponents(model_audit["input_affine"]),
            exponents(model_audit["input_errors"]),
            exponents(model_audit["input_total"]),
            exponents(model_audit["raw_errors"]),
            exponents(model_audit["center_losses"]),
            exponents(model_audit["coefficient_losses"]),
            exponents(model_audit["output_affine"]),
            exponents(model_audit["output_errors"]),
            exponents(model_audit["output_total"]),
        ])
        current_target = expected_owner
        current_chart, phase = phase_at_contact(model, current_target)
        certified_owner = {
            **phase,
            "selected_target_id": expected_owner,
            "selected_root": owner["selected_root"],
        }
        classification, destination, _witnesses = (
            r139.lower.time3.core_classification(certified_owner, cores)
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
        label, _label_audit = r139.lower.generic_homogeneity_label(
            collision_index, phase["cosine"], ledger
        )
        source_rank = (
            r139.lower.round136.capped_reciprocal_cosine_rank(
                previous_cosine,
                ledger,
                collision_index,
                "source",
            )
        )
        target_rank = (
            r139.lower.round136.capped_reciprocal_cosine_rank(
                phase["cosine"],
                ledger,
                collision_index,
                "target",
            )
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
        compact_key = r139.lower.round136.compact_key(word["key"])
        official_ids.append(compact_key["official_word_key_id"])
        compact_rows.append([
            collision_index,
            incoming_target,
            expected_owner,
            compact_key["official_word_key_id"],
            label,
            rank,
            classification,
            destination,
        ])
        homogeneity[label] += 1
        incidence[rank] += 1
        previous_cosine = phase["cosine"]
    require(terminal_phase is not None, "terminal phase materialized")
    require(
        digest(official_ids) == r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and digest(compact_rows) == r139.EXPECTED_COMPACT_PATH_SHA256
        and homogeneity == Counter({"H0_CENTRAL": RETURN_DEPTH})
        and incidence == Counter({14: RETURN_DEPTH}),
        "frozen path identities",
    )
    return {
        "precision_bits": precision_bits,
        "owner_sequence_sha256": digest(owners),
        "official_sequence_sha256": digest(official_ids),
        "compact_path_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(homogeneity),
        "incidence_histogram": {
            str(key): value for key, value in incidence.items()
        },
        "model_radius_ledger_row_count": len(radius_rows),
        "model_radius_ledger_sha256": digest(radius_rows),
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            upper_exponent(maximum_radius),
        "maximum_state_radius_witness": maximum_witness,
        "terminal_state_radius_strict_upper_power_of_two_exponents":
            exponents(model.total_radii()),
        "ledger_worst_depth": max(ledger.depths.values()),
        "ledger_worst_names": sorted(
            name
            for name, depth in ledger.depths.items()
            if depth == max(ledger.depths.values())
        ),
        "strict_margin_ledger": {
            name: {
                "dyadic_depth": ledger.depths[name],
                "observation_count": ledger.counts[name],
                "one_worst_depth_witness": ledger.witnesses[name],
            }
            for name in sorted(ledger.depths)
        },
        "terminal_phase": {
            "normal_x": fixed_outer(terminal_phase["normal_x"]),
            "normal_y": fixed_outer(terminal_phase["normal_y"]),
            "p": fixed_outer(terminal_phase["p"]),
            "cosine": fixed_outer(terminal_phase["cosine"]),
        },
    }


def validate_semantics(
    document: dict[str, Any],
    primary: dict[str, Any],
    check_closure: bool = True,
) -> None:
    if check_closure:
        require(
            document["schema"] == CERTIFICATE_SCHEMA
            and document["result_sha256"] == CERTIFICATE_RESULT_SHA256
            and digest(document["result"]) == CERTIFICATE_RESULT_SHA256,
            "certificate closure",
        )
    else:
        require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(
        result["status"]
        == "CERTIFIED_RECENTERED_AFFINE_K4296_D0_COLLAR_STRICT_R1648_RETURN",
        "certificate status",
    )
    provenance = result["provenance"]
    require(
        provenance["producer_sha256"] == PRODUCER_SHA256
        and provenance["centered_engine_sha256"] == ENGINE_SHA256
        and provenance["append_only"] is True
        and provenance["Round139_files_modified"] is False
        and provenance["Round140_files_modified"] is False,
        "provenance",
    )
    domain = result["exact_fixed_leaf_domain"]
    require(
        domain["exact_parameter"] == "z=x-x_star in [-2^-4296,0]"
        and domain["exact_half_open_collar"]
        == "[x_star-2^-4296,x_star)"
        and domain["closed_model_domain_includes_endpoint"] is True
        and domain["inside_Round116_strip"] is True
        and domain["inside_source_core"] is True
        and domain["far_D3_strict_negative"] is True
        and domain["D3_strictly_increasing_along_whole_leaf_collar"] is True
        and domain["D3_negative_on_exact_half_open_collar"] is True
        and domain["only_D3_zero_endpoint"] == "x_star",
        "exact leaf domain",
    )
    model = result["recentered_affine_contract"]
    require(
        model["parameter_generator_count"] == 2
        and model["physical_state_dimension"] == 4
        and model["center_recenter_loss_charged_at_every_stage"] is True
        and model["coefficient_recenter_loss_charged_at_every_stage"] is True
        and model["collision_stage_count"] == RETURN_DEPTH
        and model["model_radius_ledger_row_count"]
        == primary["model_radius_ledger_row_count"]
        and model["model_radius_ledger_sha256"]
        == primary["model_radius_ledger_sha256"]
        and model[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        == primary[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        and model["maximum_state_radius_witness"]
        == primary["maximum_state_radius_witness"]
        and model[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ]
        == primary[
            "terminal_state_radius_strict_upper_power_of_two_exponents"
        ],
        "affine model contract",
    )
    replay = result["complete_decision_replay"]
    require(
        replay["return_depth"] == RETURN_DEPTH
        and replay["owner_sequence_sha256"]
        == primary["owner_sequence_sha256"]
        and replay["official_sequence_sha256"]
        == primary["official_sequence_sha256"]
        and replay["compact_path_sha256"]
        == primary["compact_path_sha256"]
        and replay["retained_candidate_stage_count"] == RETURN_DEPTH
        and replay["full_radius4_candidate_stage_count"] == RETURN_DEPTH
        and replay["full_radius4_candidate_count_per_stage"] == 161
        and replay["full_radius4_candidate_test_count"] == 161 * RETURN_DEPTH
        and replay["collision3_D0_anchor_analytic_exclusion_count"] == 1
        and replay["all_nonanchor_candidate_decisions_strict"] is True
        and replay["all_owner_winner_gaps_strict"] is True
        and replay[
            "all_official_wall_endpoint_and_order_decisions_strict"
        ] is True
        and replay["all_outgoing_chart_decisions_strict"] is True
        and replay["homogeneity_histogram"]
        == primary["homogeneity_histogram"]
        and replay["incidence_rank_histogram"]
        == primary["incidence_histogram"]
        and replay["preterminal_strict_nonreturn_count"]
        == RETURN_DEPTH - 1
        and replay["terminal_strict_return_count"] == 1
        and replay["terminal_owner"] == r139.EXPECTED_TERMINAL_OWNER
        and replay["terminal_destination_core"]
        == r139.EXPECTED_DESTINATION_CORE_ID
        and replay["worst_decision_margin_dyadic_depth"]
        == primary["ledger_worst_depth"]
        and replay["worst_decision_margin_names"]
        == primary["ledger_worst_names"],
        "complete decision replay",
    )
    require(
        replay["strict_margin_ledger"]
        == primary["strict_margin_ledger"],
        "strict margin ledger",
    )
    terminal = result["terminal_phase_enclosure"]
    require(
        terminal["fixed_dyadic_outer_bits"] == 128
        and terminal["normal_x"] == primary["terminal_phase"]["normal_x"]
        and terminal["normal_y"] == primary["terminal_phase"]["normal_y"]
        and terminal["p"] == primary["terminal_phase"]["p"]
        and terminal["cosine"] == primary["terminal_phase"]["cosine"]
        and terminal["strictly_inside_destination_core"] is True,
        "terminal phase",
    )
    p_lower, p_upper = map(Q, terminal["p"])
    require(
        Q(-1, 50) < p_lower < p_upper < Q(1, 50),
        "terminal p inside G:S core",
    )
    upgrade = result["width_upgrade"]
    require(
        upgrade["Round139_power"] == 5888
        and upgrade["Round141_power"] == 4296
        and upgrade["certified_width_factor_power_of_two"] == 1592
        and upgrade["certified_width_factor"] == "2^1592"
        and upgrade["same_D0_endpoint"] is True
        and upgrade["same_exact_slope4_leaf"] is True
        and upgrade["same_R1648_owner_and_official_word"] is True,
        "width upgrade",
    )
    nonpromotion = result["strict_nonpromotion"]
    require(
        nonpromotion["historical_maximal_component_materialized"] is False
        and nonpromotion[
            "historical_least_component_rank_materialized"
        ] is False
        and nonpromotion["Round35_restriction_materialized"] is False
        and nonpromotion["natural_short_cell_k_materialized"] is False
        and nonpromotion["parent_W_id_materialized"] is False
        and nonpromotion["image_recut_rank_materialized"] is False
        and nonpromotion["Gate5"] == "NOT_CERTIFIED"
        and nonpromotion["global_gate5_maturity"] == "10/18"
        and nonpromotion["global_complete_18_field_block_count"] == 0
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "strict nonpromotion",
    )


def semantic_attack_self_test(
    document: dict[str, Any],
    primary: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[tuple[str, Any]] = [
        ("status", lambda r: r.__setitem__("status", "CERTIFIED")),
        (
            "width",
            lambda r: r["width_upgrade"].__setitem__(
                "Round141_power", 4289
            ),
        ),
        (
            "factor",
            lambda r: r["width_upgrade"].__setitem__(
                "certified_width_factor_power_of_two", 1599
            ),
        ),
        (
            "model_rows",
            lambda r: r["recentered_affine_contract"].__setitem__(
                "model_radius_ledger_row_count", 1647
            ),
        ),
        (
            "model_hash",
            lambda r: r["recentered_affine_contract"].__setitem__(
                "model_radius_ledger_sha256", "0" * 64
            ),
        ),
        (
            "radius",
            lambda r: r["recentered_affine_contract"].__setitem__(
                "maximum_state_radius_strict_upper_power_of_two_exponent",
                -15,
            ),
        ),
        (
            "owner",
            lambda r: r["complete_decision_replay"].__setitem__(
                "owner_sequence_sha256", "0" * 64
            ),
        ),
        (
            "official",
            lambda r: r["complete_decision_replay"].__setitem__(
                "official_sequence_sha256", "0" * 64
            ),
        ),
        (
            "compact",
            lambda r: r["complete_decision_replay"].__setitem__(
                "compact_path_sha256", "0" * 64
            ),
        ),
        (
            "candidate_count",
            lambda r: r["complete_decision_replay"].__setitem__(
                "full_radius4_candidate_test_count", 0
            ),
        ),
        (
            "anchor",
            lambda r: r["complete_decision_replay"].__setitem__(
                "collision3_D0_anchor_analytic_exclusion_count", 0
            ),
        ),
        (
            "homogeneity",
            lambda r: r["complete_decision_replay"].__setitem__(
                "homogeneity_histogram", {"H0_CENTRAL": 1647}
            ),
        ),
        (
            "incidence",
            lambda r: r["complete_decision_replay"].__setitem__(
                "incidence_rank_histogram", {"13": 1648}
            ),
        ),
        (
            "terminal_owner",
            lambda r: r["complete_decision_replay"].__setitem__(
                "terminal_owner", "G[0,0]"
            ),
        ),
        (
            "terminal_p",
            lambda r: r["terminal_phase_enclosure"].__setitem__(
                "p", ["-1/2", "1/2"]
            ),
        ),
        (
            "component",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "historical_maximal_component_materialized", True
            ),
        ),
        (
            "restriction",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "Round35_restriction_materialized", True
            ),
        ),
        (
            "recut",
            lambda r: r["strict_nonpromotion"].__setitem__(
                "image_recut_rank_materialized", True
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
    ]
    rejected: list[str] = []
    for label, mutation in attacks:
        attacked = json.loads(json.dumps(document))
        mutation(attacked["result"])
        attacked["result_sha256"] = digest(attacked["result"])
        try:
            validate_semantics(attacked, primary, check_closure=False)
        except (KeyError, RuntimeError, TypeError, ValueError):
            rejected.append(label)
    require(len(rejected) == len(attacks), "semantic attack rejection")
    return {
        "attack_count": len(attacks),
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
    }
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cm2-r141-json-") as directory:
        root = Path(directory)
        for label, payload in fixtures.items():
            path = root / f"{label}.json"
            path.write_text(payload, encoding="utf-8")
            try:
                r139.strict_json(path)
            except (json.JSONDecodeError, RuntimeError, TypeError, ValueError):
                rejected.append(label)
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
    require(len(rejected) == 9, "strict JSON self tests")
    return {
        "attack_count": 9,
        "rejected_attack_count": len(rejected),
        "labels": sorted(rejected),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        ENGINE.resolve(),
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
        require(
            all(
                not os.path.samefile(absolute, item)
                for item in protected_paths()
                if item.exists()
            ),
            "output hardlink aliases input",
        )
    return resolved


def path_safety_self_test() -> dict[str, Any]:
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(prefix="cm2-r141-path-") as directory:
        root = Path(directory)
        tests: list[tuple[str, Path]] = [
            ("producer", PRODUCER),
            ("certificate", CERTIFICATE),
            ("engine", ENGINE),
            ("verifier", Path(__file__).resolve()),
            ("directory", root),
            ("missing_parent", root / "missing" / "x.json"),
        ]
        real_parent = root / "real"
        real_parent.mkdir()
        linked_parent = root / "linked"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        tests.append(("symlink_parent", linked_parent / "x.json"))
        regular = root / "regular.json"
        regular.write_text("x", encoding="utf-8")
        output_symlink = root / "output.json"
        output_symlink.symlink_to(regular)
        tests.append(("output_symlink", output_symlink))
        hardlink = root / "hardlink.json"
        os.link(CERTIFICATE, hardlink)
        tests.append(("hardlink", hardlink))
        for label, path in tests:
            try:
                validate_output_target(path)
            except (OSError, RuntimeError):
                rejected.append(label)
    require(len(rejected) == 9, "path safety self tests")
    return {
        "attack_count": 9,
        "rejected_attack_count": len(rejected),
        "labels": rejected,
    }


def build_verification() -> dict[str, Any]:
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer pin")
    require(sha256(CERTIFICATE) == CERTIFICATE_SHA256, "certificate pin")
    require(sha256(ENGINE) == ENGINE_SHA256, "engine pin")
    document = r139.strict_json(CERTIFICATE)
    primary = reconstruct(PRIMARY_PRECISION_BITS)
    validate_semantics(document, primary)
    secondary = reconstruct(SECONDARY_PRECISION_BITS)
    require(
        secondary["owner_sequence_sha256"]
        == primary["owner_sequence_sha256"]
        and secondary["official_sequence_sha256"]
        == primary["official_sequence_sha256"]
        and secondary["compact_path_sha256"]
        == primary["compact_path_sha256"]
        and secondary["homogeneity_histogram"]
        == primary["homogeneity_histogram"]
        and secondary["incidence_histogram"]
        == primary["incidence_histogram"]
        and secondary["model_radius_ledger_row_count"]
        == primary["model_radius_ledger_row_count"]
        and secondary[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        <= primary[
            "maximum_state_radius_strict_upper_power_of_two_exponent"
        ]
        and all(
            secondary_value <= primary_value
            for secondary_value, primary_value in zip(
                secondary[
                    "terminal_state_radius_strict_upper_power_of_two_exponents"
                ],
                primary[
                    "terminal_state_radius_strict_upper_power_of_two_exponents"
                ],
            )
        )
        and secondary["ledger_worst_depth"]
        == primary["ledger_worst_depth"]
        and secondary["ledger_worst_names"]
        == primary["ledger_worst_names"],
        "dual precision structural agreement",
    )
    attacks = semantic_attack_self_test(document, primary)
    json_attacks = strict_json_self_test()
    path_attacks = path_safety_self_test()
    result = {
        "status": "PASS",
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "engine_sha256": ENGINE_SHA256,
        "independence_contract": {
            "producer_imported": False,
            "centered_engine_imported": False,
            "independent_affine_state_class": True,
            "independent_initial_leaf_map": True,
            "independent_collision_map": True,
            "independent_recentered_remainder_recurrence": True,
            "generic_dual_source":
                "cm2_fixed_section_common_vertex_cert.Dual",
            "upstream_Round139_decision_definitions_reused": True,
        },
        "primary_reconstruction": primary,
        "secondary_reconstruction": secondary,
        "dual_precision_consistency": {
            "primary_precision_bits": PRIMARY_PRECISION_BITS,
            "secondary_precision_bits": SECONDARY_PRECISION_BITS,
            "same_owner_official_compact_path": True,
            "same_homogeneity_and_incidence": True,
            "secondary_state_radius_bounds_no_worse": True,
            "same_worst_decision_depth_and_family": True,
        },
        "semantic_attack_audit": attacks,
        "strict_json_attack_audit": json_attacks,
        "path_safety_attack_audit": path_attacks,
        "scope": {
            "local_centered_x_width_power": X_COLLAR_POWER,
            "historical_component_id_certified": False,
            "Round35_restriction_certified": False,
            "image_recut_rank_certified": False,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def atomic_write(path: Path, payload: str) -> None:
    target = validate_output_target(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
        text=True,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(
        args.certificate.resolve() == CERTIFICATE.resolve(),
        "only frozen certificate accepted",
    )
    verification = build_verification()
    payload = json.dumps(
        verification,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    atomic_write(args.output, payload)
    print(json.dumps({
        "schema": verification["schema"],
        "result_sha256": verification["result_sha256"],
        "output": str(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
