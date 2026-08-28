#!/usr/bin/env python3
"""Feasibility spike for a centered-affine enlargement of Round139.

This intentionally small program propagates the frozen Round139 collision
owner sequence on the exact slope-four leaf.  It replaces natural interval
iteration by a two-generator affine model: one generator is the intrinsic
leaf coordinate and the other is the certified D0-root enclosure.

The spike is not a certificate.  It exists only to locate the first exact
failure before a fail-closed Round141 producer and independent verifier are
built.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Sequence

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139


HERE = Path(__file__).resolve().parent
R139_CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)


class Dual:
    """First-order Arb dual number with a fixed derivative dimension."""

    __slots__ = ("value", "derivative")

    def __init__(
        self,
        value: arb | int,
        derivative: Sequence[arb] | None = None,
        dimension: int = 0,
    ) -> None:
        self.value = value if isinstance(value, arb) else arb(value)
        self.derivative = (
            list(derivative)
            if derivative is not None
            else [arb(0) for _ in range(dimension)]
        )

    @property
    def dimension(self) -> int:
        return len(self.derivative)

    def coerce(self, other: Dual | arb | int) -> Dual:
        if isinstance(other, Dual):
            if other.dimension != self.dimension:
                raise ValueError("incompatible dual dimensions")
            return other
        return Dual(other, dimension=self.dimension)

    def __add__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value + other.value,
            [a + b for a, b in zip(self.derivative, other.derivative)],
        )

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.value, [-entry for entry in self.derivative])

    def __sub__(self, other: Dual | arb | int) -> Dual:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) - self

    def __mul__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value * other.value,
            [
                a * other.value + self.value * b
                for a, b in zip(self.derivative, other.derivative)
            ],
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        denominator = other.value * other.value
        return Dual(
            self.value / other.value,
            [
                (a * other.value - self.value * b) / denominator
                for a, b in zip(self.derivative, other.derivative)
            ],
        )

    def __rtruediv__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) / self


def dsqrt(value: Dual) -> Dual:
    root = value.value.sqrt()
    return Dual(root, [entry / (2 * root) for entry in value.derivative])


def dsin(value: Dual) -> Dual:
    return Dual(
        value.value.sin(),
        [value.value.cos() * entry for entry in value.derivative],
    )


def dcos(value: Dual) -> Dual:
    return Dual(
        value.value.cos(),
        [-value.value.sin() * entry for entry in value.derivative],
    )


def dot(left: Sequence[Dual], right: Sequence[Dual]) -> Dual:
    return left[0] * right[0] + left[1] * right[1]


def rows(values: Sequence[Dual]) -> list[list[arb]]:
    return [list(value.derivative) for value in values]


def symmetric(radius: arb) -> arb:
    return arb(0, radius.upper())


def point(value: arb) -> arb:
    """Replace an Arb ball by its exact midpoint."""

    return arb(value.mid())


@dataclass
class Model:
    centers: list[arb]
    affine: list[list[arb]]
    remainders: list[arb]
    domain_radii: tuple[arb, arb]

    def radii(self) -> list[arb]:
        return [
            sum(
                self.affine[row][column].abs_upper()
                * self.domain_radii[column]
                for column in range(2)
            )
            + self.remainders[row]
            for row in range(4)
        ]

    def boxes(self) -> list[arb]:
        return [
            self.centers[row] + symmetric(radius)
            for row, radius in enumerate(self.radii())
        ]


def target_geometry(identifier: str) -> tuple[tuple[arb, arb], arb]:
    lower = r139.lower
    center = lower.time3.time2_cert.target_center(identifier, arb(0))
    radius = lower.aq(
        lower.time3.time2_cert.first_hit.RADIUS[identifier[0]]
    )
    return center, radius


def collision(
    state: Sequence[Dual],
    target_center: tuple[arb, arb],
    target_radius: arb,
) -> tuple[list[Dual], tuple[Dual, Dual, Dual]]:
    position, velocity = state[:2], state[2:]
    displacement = (
        position[0] - target_center[0],
        position[1] - target_center[1],
    )
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - target_radius * target_radius
    discriminant = linear * linear - offset
    if not bool(discriminant.value > 0):
        raise RuntimeError(f"nonpositive discriminant:{discriminant.value}")
    flight = -linear - dsqrt(discriminant)
    if not bool(flight.value > 0):
        raise RuntimeError(f"nonforward flight:{flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - target_center[0]) / target_radius,
        (impact[1] - target_center[1]) / target_radius,
    )
    arrival = -dot(velocity, normal)
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    return list(impact + reflected), (flight, discriminant, arrival)


def initial_state(z: Dual, t_star: Dual) -> list[Dual]:
    lower = r139.lower
    sqrt17 = arb(17).sqrt()
    angle = Dual(0, dimension=2) + (
        Dual(lower.aq(lower.R_W), dimension=2) * 0
    )
    # asin(t_star) is represented through its derivative explicitly.
    root_angle = Dual(
        t_star.value.asin(),
        [
            derivative / dsqrt(
                Dual(1, dimension=2) - t_star * t_star
            ).value
            for derivative in t_star.derivative
        ],
    )
    angle = root_angle + z / (lower.aq(lower.R_W) * sqrt17)
    t = dsin(angle)
    p_angle = (
        Dual(lower.aq(lower.SOURCE_P_STAR).asin(), dimension=2)
        + 4 * z / sqrt17
    )
    p = dsin(p_angle)
    nx, ny = dcos(angle), t
    tangent = (-ny, nx)
    radial = dsqrt(Dual(1, dimension=2) - p * p)
    velocity = (
        radial * nx + p * tangent[0],
        radial * ny + p * tangent[1],
    )
    center, radius = target_geometry(r139.lower.SOURCE_ABSOLUTE_OWNER)
    position = (
        Dual(center[0], dimension=2) + radius * nx,
        Dual(center[1], dimension=2) + radius * ny,
    )
    return list(position + velocity)


def initial_model(
    power: int,
    root: tuple[Q, Q],
    cell_index: int = 0,
) -> Model:
    if type(cell_index) is not int or cell_index < 0:
        raise RuntimeError("nonnegative translated cell index")
    ell = r139.lower.aq(Q(1, 2**power))
    z_center = -(2 * cell_index + 1) * ell / 2
    z_radius = ell / 2
    root_lower, root_upper = map(r139.lower.aq, root)
    root_center = (root_lower + root_upper) / 2
    root_radius = (root_upper - root_lower) / 2

    center_inputs = (
        Dual(z_center, [arb(1), arb(0)]),
        Dual(root_center, [arb(0), arb(1)]),
    )
    interval_inputs = (
        Dual(z_center + symmetric(z_radius), [arb(1), arb(0)]),
        Dual(root_center + symmetric(root_radius), [arb(0), arb(1)]),
    )
    center_values = initial_state(*center_inputs)
    interval_values = initial_state(*interval_inputs)
    raw_affine = rows(center_values)
    affine = [[point(entry) for entry in row] for row in raw_affine]
    interval_derivatives = rows(interval_values)
    domain_radii = (z_radius, root_radius)
    remainders = [
        (center_values[row].value - point(center_values[row].value)).abs_upper()
        + sum(
            (
                raw_affine[row][column] - affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        +
        sum(
            (
                interval_derivatives[row][column]
                - raw_affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return Model(
        [point(value.value) for value in center_values],
        affine,
        remainders,
        domain_radii,
    )


def step_model_with_audit(
    model: Model,
    target_id: str,
) -> tuple[Model, dict[str, Any]]:
    state_radii = model.radii()
    state_boxes = [
        model.centers[index] + symmetric(state_radii[index])
        for index in range(4)
    ]
    interval_state = [
        Dual(
            state_boxes[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center_state = [
        Dual(
            model.centers[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center, radius = target_geometry(target_id)
    center_outputs, _center_metrics = collision(center_state, center, radius)
    try:
        interval_outputs, _interval_metrics = collision(
            interval_state, center, radius
        )
    except Exception as exc:
        raise RuntimeError(
            f"{exc}; state_radii={state_radii}; "
            f"center_discriminant={_center_metrics[1].value}"
        ) from exc
    local_interval = rows(interval_outputs)
    local_center = rows(center_outputs)
    raw_new_affine = [
        [
            sum(
                local_center[row][inner] * model.affine[inner][column]
                for inner in range(4)
            )
            for column in range(2)
        ]
        for row in range(4)
    ]
    new_affine = [
        [point(entry) for entry in row]
        for row in raw_new_affine
    ]
    affine_radii = [
        sum(
            model.affine[row][column].abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    raw_new_remainders = [
        sum(
            (
                local_interval[row][inner] - local_center[row][inner]
            ).abs_upper()
            * affine_radii[inner]
            + local_interval[row][inner].abs_upper()
            * model.remainders[inner]
            for inner in range(4)
        )
        for row in range(4)
    ]
    new_centers = [point(value.value) for value in center_outputs]
    center_losses = [
        (center_outputs[row].value - new_centers[row]).abs_upper()
        for row in range(4)
    ]
    coefficient_losses = [
        sum(
            (
                raw_new_affine[row][column]
                - new_affine[row][column]
            ).abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    new_remainders = [
        raw_new_remainders[row]
        + center_losses[row]
        + coefficient_losses[row]
        for row in range(4)
    ]
    result = Model(
        new_centers,
        new_affine,
        new_remainders,
        model.domain_radii,
    )
    new_affine_radii = [
        sum(
            new_affine[row][column].abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return result, {
        "input_state_radii": state_radii,
        "input_affine_radii": affine_radii,
        "input_remainders": list(model.remainders),
        "interval_flight": _interval_metrics[0].value,
        "interval_discriminant": _interval_metrics[1].value,
        "interval_incidence": _interval_metrics[2].value,
        "raw_propagated_remainders": raw_new_remainders,
        "center_recenter_losses": center_losses,
        "coefficient_recenter_losses": coefficient_losses,
        "output_affine_radii": new_affine_radii,
        "output_remainders": new_remainders,
        "output_state_radii": result.radii(),
    }


def step_model(model: Model, target_id: str) -> Model:
    result, _audit = step_model_with_audit(model, target_id)
    return result


class NoLedger:
    def observe(
        self,
        _name: str,
        value: arb,
        _witness: dict[str, Any] | None = None,
    ) -> int:
        if not bool(value > 0):
            raise RuntimeError(f"nonstrict margin:{value}")
        return r139.lower.round136.strict_dyadic_depth(value)


class AuditLedger(NoLedger):
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
        depth = super().observe(name, value, witness)
        self.counts[name] += 1
        if name not in self.depths or depth > self.depths[name]:
            self.depths[name] = depth
            self.witnesses[name] = witness
        return depth


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def strict_upper_power_of_two_exponent(value: arb) -> int | None:
    """Return the least e proved to satisfy abs(value) < 2**e."""

    upper = value.abs_upper()
    if upper == 0:
        return None
    log_two = arb(2).log()
    estimate = math.ceil(float((upper.log() / log_two).mid()))
    while not bool(upper < arb(2) ** estimate):
        estimate += 1
    while bool(upper < arb(2) ** (estimate - 1)):
        estimate -= 1
    return estimate


def vector_upper_exponents(values: Sequence[arb]) -> list[int | None]:
    return [strict_upper_power_of_two_exponent(value) for value in values]


def fixed_padded_outer(value: arb, bits: int) -> tuple[Q, Q]:
    raw_lower, raw_upper = r139.lower.round136.arb_pair(value)
    scale = 2**bits
    lower = Q(r139.lower.floor_q(raw_lower * scale) - 1, scale)
    upper = Q(r139.lower.ceil_q(raw_upper * scale) + 1, scale)
    if not (
        lower < upper
        and bool(value > r139.lower.aq(lower))
        and bool(value < r139.lower.aq(upper))
    ):
        raise RuntimeError("fixed padded outer")
    return lower, upper


def chart_and_owner_state(
    model: Model,
    current_target: str,
) -> tuple[str, dict[str, Any]]:
    lower = r139.lower
    boxes = model.boxes()
    center, radius = target_geometry(current_target)
    nx = (boxes[0] - center[0]) / radius
    ny = (boxes[1] - center[1]) / radius
    chart = lower.time3.time2_cert.strict_chart(nx, ny)
    if chart is None:
        raise RuntimeError(f"unresolved chart:{current_target}:{nx}:{ny}")
    p = -boxes[2] * ny + boxes[3] * nx
    cosine = -(boxes[2] * nx + boxes[3] * ny)
    # At a contact after reflection, the outward velocity has positive normal
    # component.  Round136's owner cosine is the incoming absolute component,
    # equal to the outgoing positive component.
    cosine = -cosine
    return chart, {
        "normal_x": nx,
        "normal_y": ny,
        "p": p,
        "cosine": cosine,
    }


def run(
    power: int,
    precision: int,
    audit_candidates: bool,
    audit_all: bool,
    cell_index: int,
) -> None:
    ctx.prec = precision
    document = json.loads(R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    root = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model = initial_model(power, root, cell_index)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger: NoLedger = AuditLedger() if audit_all else NoLedger()
    maximum_radius = arb(0)
    maximum_radius_witness: list[Any] | None = None
    model_radius_rows: list[list[Any]] = []
    official_ids: list[str] = []
    compact_rows: list[list[Any]] = []
    homogeneity_labels: list[str] = []
    incidence_ranks: list[int] = []
    pair_index = pattern_index = None
    cores = None
    if audit_all:
        cores = tuple(r139.lower.core_cert.physical_cores())
        pair_index, pattern_index, registry_sha = (
            r139.lower.component_cert.key_index_tables()
        )
        if registry_sha != r139.OFFICIAL_REGISTRY_SHA256:
            raise RuntimeError("official registry digest")
    initial_boxes = model.boxes()
    source_center, source_radius = target_geometry(current_target)
    initial_nx = (initial_boxes[0] - source_center[0]) / source_radius
    initial_ny = (initial_boxes[1] - source_center[1]) / source_radius
    initial_p = -initial_boxes[2] * initial_ny + initial_boxes[3] * initial_nx
    previous_cosine = (1 - initial_p * initial_p).sqrt()
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        state_boxes = model.boxes()
        for component, radius in enumerate(model.radii()):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_radius_witness = [
                    collision_index - 1,
                    component,
                    strict_upper_power_of_two_exponent(radius),
                ]
        state = None
        owner = None
        if audit_candidates or audit_all:
            state = {
                "contact_x": state_boxes[0],
                "contact_y": state_boxes[1],
                "outgoing_x": state_boxes[2],
                "outgoing_y": state_boxes[3],
                "s": arb(0),
                "chart": current_chart,
            }
            if collision_index == r139.ANCHOR_COLLISION_INDEX:
                candidates = tuple(
                    r139.lower.time3.time2_cert.translated_candidate_ids(
                        current_target, current_chart
                    )
                )
                owner, _audit = r139.candidates_owner_excluding_anchor(
                    state,
                    current_target,
                    candidates,
                    ledger,
                    collision_index,
                    False,
                )
                full, _full_audit = r139.candidates_owner_excluding_anchor(
                    state,
                    current_target,
                    r139.lower.charge.candidate_ids_around(current_target),
                    ledger,
                    collision_index,
                    True,
                )
                if full["selected_target_id"] != owner["selected_target_id"]:
                    raise RuntimeError("retained/full mismatch")
            else:
                owner, _audit = r139.lower.round136.complete_owner(
                    state, current_target, ledger, collision_index
                )
                r139.lower.full_radius4_candidate_audit(
                    state, current_target, owner, ledger, collision_index
                )
            if owner["selected_target_id"] != expected_owner:
                raise RuntimeError(
                    f"owner mismatch:{collision_index}:"
                    f"{owner['selected_target_id']}:{expected_owner}"
                )
        word = None
        if audit_all:
            assert state is not None and owner is not None
            assert pair_index is not None and pattern_index is not None
            word, error = (
                r139.lower.round136.translation_normalized_official_word(
                    state,
                    current_target,
                    owner,
                    pair_index,
                    pattern_index,
                )
            )
            if word is None or error is not None:
                raise RuntimeError(
                    f"official word:{collision_index}:{error}"
                )
            r139.official_wall_margin_audit(
                state, current_target, owner, ledger, collision_index
            )
        try:
            model, step_audit = step_model_with_audit(
                model, expected_owner
            )
        except Exception as exc:
            raise RuntimeError(
                f"centered propagation failed at collision "
                f"{collision_index} target {expected_owner}: {exc}"
            ) from exc
        output_radii = step_audit["output_state_radii"]
        for component, radius in enumerate(output_radii):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_radius_witness = [
                    collision_index,
                    component,
                    strict_upper_power_of_two_exponent(radius),
                ]
        model_radius_rows.append([
            collision_index,
            vector_upper_exponents(step_audit["input_affine_radii"]),
            vector_upper_exponents(step_audit["input_remainders"]),
            vector_upper_exponents(step_audit["input_state_radii"]),
            vector_upper_exponents(step_audit["raw_propagated_remainders"]),
            vector_upper_exponents(step_audit["center_recenter_losses"]),
            vector_upper_exponents(step_audit["coefficient_recenter_losses"]),
            vector_upper_exponents(step_audit["output_affine_radii"]),
            vector_upper_exponents(step_audit["output_remainders"]),
            vector_upper_exponents(step_audit["output_state_radii"]),
        ])
        current_target = expected_owner
        current_chart, owner_state = chart_and_owner_state(
            model, current_target
        )
        if not bool(owner_state["cosine"] > 0):
            raise RuntimeError(f"nonpositive cosine:{collision_index}")
        if audit_all:
            assert owner is not None and word is not None and cores is not None
            certified_owner = {
                **owner_state,
                "selected_target_id": expected_owner,
                "selected_root": owner["selected_root"],
            }
            classification, destination, _witnesses = (
                r139.lower.time3.core_classification(
                    certified_owner, cores
                )
            )
            if collision_index < len(owners):
                if (
                    classification != "SURVIVE_THROUGH_3_INNER"
                    or destination is not None
                ):
                    raise RuntimeError(
                        f"preterminal C24:{collision_index}:"
                        f"{classification}:{destination}"
                    )
            elif (
                classification != "RETURN_AT_3_INNER"
                or destination != r139.EXPECTED_DESTINATION_CORE_ID
            ):
                raise RuntimeError(
                    f"terminal C24:{classification}:{destination}"
                )
            r139.lower.round136.core_margin(
                certified_owner,
                classification,
                destination,
                cores,
                ledger,
            )
            homogeneity, _homogeneity_audit = (
                r139.lower.generic_homogeneity_label(
                    collision_index, owner_state["cosine"], ledger
                )
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
                    owner_state["cosine"],
                    ledger,
                    collision_index,
                    "target",
                )
            )
            incidence = max(14, source_rank, target_rank)
            r139.lower.round136.chart_margin(
                {
                    "chart": current_chart,
                    "normal_x": owner_state["normal_x"],
                    "normal_y": owner_state["normal_y"],
                },
                ledger,
            )
            compact_key = r139.lower.round136.compact_key(word["key"])
            official_ids.append(compact_key["official_word_key_id"])
            homogeneity_labels.append(homogeneity)
            incidence_ranks.append(incidence)
            compact_rows.append([
                collision_index,
                incoming_target,
                expected_owner,
                compact_key["official_word_key_id"],
                homogeneity,
                incidence,
                classification,
                destination,
            ])
            previous_cosine = owner_state["cosine"]
        if collision_index % 100 == 0 or collision_index == len(owners):
            log_two = arb(2).log()
            radius_logs = [
                float((radius.log() / log_two).mid())
                for radius in model.radii()
            ]
            print(
                collision_index,
                current_target,
                current_chart,
                "max_radius_log2",
                float((maximum_radius.log() / log_two).mid()),
                "current_radius_log2",
                radius_logs,
                flush=True,
            )
    print(
        json.dumps(
            {
                "status": "FEASIBLE",
                "power": power,
                "cell_index": cell_index,
                "precision": precision,
                "collision_count": len(owners),
                "candidate_audit": audit_candidates or audit_all,
                "complete_audit": audit_all,
                "maximum_state_radius": str(maximum_radius),
                "maximum_state_radius_strict_upper_power_of_two_exponent":
                    strict_upper_power_of_two_exponent(maximum_radius),
                "maximum_state_radius_witness":
                    maximum_radius_witness,
                "terminal_state_radius_strict_upper_power_of_two_exponents":
                    vector_upper_exponents(model.radii()),
                "model_radius_ledger_row_count": len(model_radius_rows),
                "model_radius_ledger_sha256": digest(model_radius_rows),
                "official_sequence_sha256":
                    digest(official_ids) if audit_all else None,
                "compact_rows_sha256":
                    digest(compact_rows) if audit_all else None,
                "homogeneity_histogram":
                    dict(Counter(homogeneity_labels)) if audit_all else None,
                "incidence_histogram":
                    dict(Counter(incidence_ranks)) if audit_all else None,
                "ledger_worst_depth": (
                    max(ledger.depths.values())
                    if isinstance(ledger, AuditLedger)
                    else None
                ),
                "ledger_worst_names": (
                    sorted(
                        name
                        for name, depth in ledger.depths.items()
                        if depth == max(ledger.depths.values())
                    )
                    if isinstance(ledger, AuditLedger)
                    else None
                ),
                "strict_margin_ledger": (
                    {
                        name: {
                            "dyadic_depth": ledger.depths[name],
                            "observation_count": ledger.counts[name],
                            "one_worst_depth_witness":
                                ledger.witnesses[name],
                        }
                        for name in sorted(ledger.depths)
                    }
                    if isinstance(ledger, AuditLedger)
                    else None
                ),
                "terminal_phase_fixed_dyadic_outer_bits": 128,
                "terminal_normal_x_fixed_dyadic_outer": [
                    r139.qstr(value)
                    for value in fixed_padded_outer(
                        owner_state["normal_x"], 128
                    )
                ],
                "terminal_normal_y_fixed_dyadic_outer": [
                    r139.qstr(value)
                    for value in fixed_padded_outer(
                        owner_state["normal_y"], 128
                    )
                ],
                "terminal_p_fixed_dyadic_outer": [
                    r139.qstr(value)
                    for value in fixed_padded_outer(
                        owner_state["p"], 128
                    )
                ],
                "terminal_cosine_fixed_dyadic_outer": [
                    r139.qstr(value)
                    for value in fixed_padded_outer(
                        owner_state["cosine"], 128
                    )
                ],
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=4296)
    parser.add_argument("--precision", type=int, default=12288)
    parser.add_argument("--audit-candidates", action="store_true")
    parser.add_argument("--audit-all", action="store_true")
    parser.add_argument("--cell-index", type=int, default=0)
    args = parser.parse_args()
    run(
        args.power,
        args.precision,
        args.audit_candidates,
        args.audit_all,
        args.cell_index,
    )


if __name__ == "__main__":
    main()
