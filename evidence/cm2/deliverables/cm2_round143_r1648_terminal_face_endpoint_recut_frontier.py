#!/usr/bin/env python3
"""Round143: the R1648 terminal-face endpoint and recut frontier.

This producer works on the exact implicit fixed-s=0, slope-four leaf frozen
by Round139.  It composes the frozen 1648 absolute collision owners with
validated Arb dual numbers and isolates the unique scaled displacement

    lambda = (x_star - x) 2^4289

at which the terminal G:S momentum equals -1/50.  A complete radius-four
owner audit is repeated on a narrow enclosure of that endpoint.  Thus the
endpoint is a genuine local preimage of the destination-core p=-1/50 face.

The producer deliberately does *not* identify the whole interval between
that endpoint and the collision-three D0 endpoint with a maximal regular
component.  The currently pinned chain has no validated all-owner corridor
cover at scale 2^-4289 and no historical Round35 coordinate/rank crosswalk.
It therefore emits coordinate-explicit prospective Round137-v1 ranks and a
conditional deterministic image-recut ledger, while every historical
component, parent-W, image-recut and restriction identifier remains null.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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

import cm2_round137_seed_independent_dyadic_basis_rank_contract as rank137
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round143-r1648-terminal-face-endpoint-recut-frontier-2026-07-24.json"
)
FUTURE_VERIFIER = (
    HERE / "cm2_round143_r1648_terminal_face_endpoint_recut_frontier_verifier.py"
)
SCHEMA = "cm2.round143.r1648-terminal-face-endpoint-recut-frontier.v1"

DISCOVERY_PRECISION_BITS = 24576
PRECISION_BITS = 12288
RETURN_DEPTH = 1648
LAMBDA_SCALE_POWER = 4289
NEWTON_BITS = 2048
NEWTON_ITERATIONS = 4
ROOT_HALF_WIDTH_POWER = 1536
OUTER_BITS = 8192
RECUT_DENOMINATOR = 10**90
DELTA_14 = Q(1, 2**23)
TERMINAL_FACE_P = Q(-1, 50)
DESTINATION_T_BOUNDS = (Q(69, 100), Q(7, 10))
DESTINATION_P_BOUNDS = (Q(-1, 50), Q(1, 50))

R139_SOURCE = (
    HERE / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)
R139_CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
R139_VERIFIER = (
    HERE
    / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py"
)
R139_VERIFICATION = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json"
)
R139_MANIFEST = (
    HERE
    / "cm2-one-hundred-thirty-ninth-direct-assault-manifest-2026-07-24.sha256"
)
R140_BRIDGE_SOURCE = (
    HERE / "cm2_round140_fixed_s_adaptive_component_identity_bridge.py"
)
R140_BRIDGE_CERTIFICATE = (
    HERE / "cm2-round140-fixed-s-adaptive-component-identity-bridge-2026-07-24.json"
)
R140_BRIDGE_VERIFIER = (
    HERE / "cm2_round140_fixed_s_adaptive_component_identity_bridge_verifier.py"
)
R140_BRIDGE_VERIFICATION = (
    HERE
    / "cm2-round140-fixed-s-adaptive-component-identity-bridge-verification-2026-07-24.json"
)
R140_BRIDGE_MANIFEST = (
    HERE / "cm2-one-hundred-fortieth-direct-assault-manifest-2026-07-24.sha256"
)
R140_PARENT_SOURCE = (
    HERE / "cm2_round140_round35_parent_w_r1648_materialization_audit.py"
)
R140_PARENT_CERTIFICATE = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
R140_PARENT_VERIFIER = (
    HERE
    / "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py"
)
R140_PARENT_VERIFICATION = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)
R140_PARENT_MANIFEST = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-direct-assault-manifest-2026-07-24.sha256"
)
R137_SOURCE = (
    HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract.py"
)
R47_MANIFEST = (
    HERE
    / "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
)
R55_MANIFEST = (
    HERE
    / "cm2-gate34-round55-global-image-recut-cap-natural-mesh-frontier-manifest-2026-07-20.json"
)

PINS = {
    R139_SOURCE.name:
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    R139_CERTIFICATE.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    R139_VERIFIER.name:
        "cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09",
    R139_VERIFICATION.name:
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    R139_MANIFEST.name:
        "f8f13619b07ff8d5d0bc238335722f1951abc81e1d8ad07ccb325f95aab9a198",
    R140_BRIDGE_SOURCE.name:
        "838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2",
    R140_BRIDGE_CERTIFICATE.name:
        "e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353",
    R140_BRIDGE_VERIFIER.name:
        "4f2c18fb476fe9754009ea7f5bba737fa95084a3e81e2b70e0043203ac774680",
    R140_BRIDGE_VERIFICATION.name:
        "75500f473e1932151bc643109187e99e88033c3b9457b584ecb1df4c0860b611",
    R140_BRIDGE_MANIFEST.name:
        "d46c15f7823f78719b505365e0f9c4c3e70103a3bc09fb075a3032b366639748",
    R140_PARENT_SOURCE.name:
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    R140_PARENT_CERTIFICATE.name:
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    R140_PARENT_VERIFIER.name:
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    R140_PARENT_VERIFICATION.name:
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
    R140_PARENT_MANIFEST.name:
        "f3b80bfd794087b395be83fc8e94f7e2ba5201db576337858d9b69c939dd1ed9",
    R137_SOURCE.name:
        "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac",
    R47_MANIFEST.name:
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    R55_MANIFEST.name:
        "12270ccbdea2b3c6bf203529e94b31a298061d6b057ddc14757853763059e95e",
}

CLOSED_SCHEMAS = {
    R139_CERTIFICATE.name:
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
    R139_VERIFICATION.name:
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
    R140_BRIDGE_CERTIFICATE.name:
        "cm2.round140.fixed-s-adaptive-component-identity-bridge.v1",
    R140_BRIDGE_VERIFICATION.name:
        "cm2.round140.fixed-s-adaptive-component-identity-bridge-verification.v1",
    R140_PARENT_CERTIFICATE.name:
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
    R140_PARENT_VERIFICATION.name:
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
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
    value = Q(value)
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink(),
        f"unsafe dependency:{path.name}",
    )
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite:{token}")
        ),
    )
    require(type(value) is dict, f"dependency root:{path.name}")
    return value


def load_closed(path: Path) -> dict[str, Any]:
    document = strict_json(path)
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CLOSED_SCHEMAS[path.name]
        and type(document["result"]) is dict
        and document["result_sha256"] == digest(document["result"]),
        f"closed dependency:{path.name}",
    )
    return document["result"]


def validate_dependencies() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"dependency pin:{name}",
        )
    r139_result = load_closed(R139_CERTIFICATE)
    r139_verification = load_closed(R139_VERIFICATION)
    bridge = load_closed(R140_BRIDGE_CERTIFICATE)
    bridge_verification = load_closed(R140_BRIDGE_VERIFICATION)
    parent = load_closed(R140_PARENT_CERTIFICATE)
    parent_verification = load_closed(R140_PARENT_VERIFICATION)
    require(
        r139_result["status"]
        == "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"
        and r139_result["strict_nonpromotion"]["global_gate5_maturity"] == "10/18"
        and r139_verification["status"] == "PASS",
        "Round139 frontier",
    )
    require(
        bridge["status"]
        == "CERTIFIED_FIXED_S_ADAPTIVE_IDENTITY_STRICT_NONSUBSTITUTION"
        and bridge_verification["status"] == "PASS",
        "Round140 bridge",
    )
    require(
        parent["status"]
        == "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648"
        and parent_verification["status"] == "PASS",
        "Round140 parent audit",
    )
    round47 = strict_json(R47_MANIFEST)["result"]
    require(
        round47["corrected_adapted_source_cell_registry"]["status"]
        == "CERTIFIED_CORRECTED_ADAPTED_SOURCE_CELL_SCHEMA"
        and "u_* intervals [k*1e-90,(k+1)*1e-90)"
        in round47["corrected_adapted_source_cell_registry"]["superseding_rule"],
        "Round47 corrected source recut",
    )
    round55 = strict_json(R55_MANIFEST)["result"]
    require(
        round55["global_connected_image_recut_cap"][
            "deterministic_adapted_recut_scale"
        ] == "1/1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "Round55 recut scale",
    )
    return {
        "Round139": r139_result,
        "Round140_bridge": bridge,
        "Round140_parent": parent,
        "Round47": round47,
        "Round55": round55,
    }


def aq(value: Q | int) -> arb:
    return r139.lower.aq(Q(value))


def interval(lower: Q, upper: Q) -> arb:
    return r139.lower.interval(lower, upper)


def nearest_dyadic(value: Q, bits: int) -> Q:
    scale = 2**bits
    shifted = value * scale + Q(1, 2)
    return Q(shifted.numerator // shifted.denominator, scale)


def fixed_outer(value: arb, bits: int = OUTER_BITS) -> tuple[Q, Q]:
    lower, upper = r139.lower.round136.arb_pair(value)
    scale = 2**bits
    left = Q(r139.lower.floor_q(lower * scale) - 1, scale)
    right = Q(r139.lower.ceil_q(upper * scale) + 1, scale)
    require(
        left < right and bool(value > aq(left)) and bool(value < aq(right)),
        "fixed outer",
    )
    return left, right


def encoded_integer(value: int) -> dict[str, Any]:
    require(value >= 0, "encoded nonnegative integer")
    decimal = str(value)
    return {
        "decimal": decimal,
        "hexadecimal": "0x" + format(value, "x"),
        "bit_length": value.bit_length(),
        "decimal_digit_count": len(decimal),
        "sha256_of_decimal":
            hashlib.sha256(decimal.encode("ascii")).hexdigest(),
    }


class Dual:
    """First-order Arb dual number with an explicit derivative dimension."""

    __slots__ = ("value", "gradient")

    def __init__(
        self,
        value: arb | int,
        gradient: Sequence[arb] | None = None,
        dimension: int = 0,
    ) -> None:
        self.value = value if isinstance(value, arb) else arb(value)
        self.gradient = (
            list(gradient)
            if gradient is not None
            else [arb(0) for _ in range(dimension)]
        )

    @property
    def dimension(self) -> int:
        return len(self.gradient)

    def coerce(self, other: Dual | arb | int) -> Dual:
        if isinstance(other, Dual):
            require(other.dimension == self.dimension, "dual dimension")
            return other
        return Dual(other, dimension=self.dimension)

    def __add__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value + other.value,
            [a + b for a, b in zip(self.gradient, other.gradient)],
        )

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.value, [-value for value in self.gradient])

    def __sub__(self, other: Dual | arb | int) -> Dual:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) - self

    def __mul__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value * other.value,
            [
                left * other.value + self.value * right
                for left, right in zip(self.gradient, other.gradient)
            ],
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        denominator = other.value * other.value
        return Dual(
            self.value / other.value,
            [
                (left * other.value - self.value * right) / denominator
                for left, right in zip(self.gradient, other.gradient)
            ],
        )

    def __rtruediv__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) / self


def dsqrt(value: Dual) -> Dual:
    root = value.value.sqrt()
    require(bool(root > 0), "dual sqrt positive")
    return Dual(root, [entry / (2 * root) for entry in value.gradient])


def dsin(value: Dual) -> Dual:
    return Dual(
        value.value.sin(),
        [value.value.cos() * entry for entry in value.gradient],
    )


def dcos(value: Dual) -> Dual:
    return Dual(
        value.value.cos(),
        [-value.value.sin() * entry for entry in value.gradient],
    )


def dasin(value: Dual) -> Dual:
    denominator = dsqrt(
        Dual(1, dimension=value.dimension) - value * value
    ).value
    return Dual(
        value.value.asin(),
        [entry / denominator for entry in value.gradient],
    )


def dot(left: Sequence[Dual], right: Sequence[Dual]) -> Dual:
    return left[0] * right[0] + left[1] * right[1]


def target_geometry(identifier: str) -> tuple[tuple[arb, arb], arb]:
    center = r139.lower.time3.time2_cert.target_center(identifier, arb(0))
    radius = aq(
        r139.lower.time3.time2_cert.first_hit.RADIUS[identifier[0]]
    )
    return center, radius


def initial_state(lambda_value: Dual, t_star: Dual) -> list[Dual]:
    require(
        lambda_value.dimension == t_star.dimension,
        "initial dual dimensions",
    )
    dimension = lambda_value.dimension
    sqrt17 = arb(17).sqrt()
    angle = dasin(t_star) - lambda_value / (
        arb(2) ** LAMBDA_SCALE_POWER * aq(r139.lower.R_W) * sqrt17
    )
    t = dsin(angle)
    p_angle = Dual(
        aq(r139.lower.SOURCE_P_STAR).asin(),
        dimension=dimension,
    ) - (
        4 * lambda_value / (arb(2) ** LAMBDA_SCALE_POWER * sqrt17)
    )
    p = dsin(p_angle)
    nx, ny = dcos(angle), t
    tangent = (-ny, nx)
    radial = dsqrt(Dual(1, dimension=dimension) - p * p)
    velocity = (
        radial * nx + p * tangent[0],
        radial * ny + p * tangent[1],
    )
    center, radius = target_geometry(r139.lower.SOURCE_ABSOLUTE_OWNER)
    position = (
        Dual(center[0], dimension=dimension) + radius * nx,
        Dual(center[1], dimension=dimension) + radius * ny,
    )
    return list(position + velocity)


def symmetric(radius: arb) -> arb:
    return arb(0, radius.upper())


def point(value: arb) -> arb:
    return arb(value.mid())


def gradient_rows(values: Sequence[Dual]) -> list[list[arb]]:
    return [list(value.gradient) for value in values]


@dataclass
class Model:
    """Two-generator recentered affine enclosure of the four-state map."""

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


def initial_model(
    lambda_box: tuple[Q, Q],
    t_star_box: tuple[Q, Q],
) -> tuple[Model, list[list[arb]]]:
    lambda_lower, lambda_upper = map(aq, lambda_box)
    t_lower, t_upper = map(aq, t_star_box)
    lambda_center = (lambda_lower + lambda_upper) / 2
    lambda_radius = (lambda_upper - lambda_lower) / 2
    t_center = (t_lower + t_upper) / 2
    t_radius = (t_upper - t_lower) / 2
    center_inputs = (
        Dual(lambda_center, [arb(1), arb(0)]),
        Dual(t_center, [arb(0), arb(1)]),
    )
    interval_inputs = (
        Dual(
            lambda_center + symmetric(lambda_radius),
            [arb(1), arb(0)],
        ),
        Dual(t_center + symmetric(t_radius), [arb(0), arb(1)]),
    )
    center_values = initial_state(*center_inputs)
    interval_values = initial_state(*interval_inputs)
    raw_affine = gradient_rows(center_values)
    affine = [[point(entry) for entry in row] for row in raw_affine]
    interval_gradients = gradient_rows(interval_values)
    domain_radii = (lambda_radius, t_radius)
    remainders = [
        (center_values[row].value - point(center_values[row].value)).abs_upper()
        + sum(
            (
                raw_affine[row][column] - affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        + sum(
            (
                interval_gradients[row][column]
                - raw_affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return (
        Model(
            [point(value.value) for value in center_values],
            affine,
            remainders,
            domain_radii,
        ),
        interval_gradients,
    )


def collide_state(
    state: Sequence[Dual],
    target_id: str,
) -> list[Dual]:
    """Dimension-generic exact selected-circle collision map."""

    center, radius = target_geometry(target_id)
    position, velocity = state[:2], state[2:]
    displacement = (
        position[0] - center[0],
        position[1] - center[1],
    )
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - radius * radius
    discriminant = linear * linear - offset
    require(bool(discriminant.value > 0), "model selected discriminant")
    flight = -linear - dsqrt(discriminant)
    require(bool(flight.value > 0), "model selected flight")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - center[0]) / radius,
        (impact[1] - center[1]) / radius,
    )
    arrival = -dot(velocity, normal)
    require(bool(arrival.value > 0), "model selected arrival")
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    return list(impact + reflected)


def step_model(
    model: Model,
    sensitivity: list[list[arb]],
    target_id: str,
) -> tuple[Model, list[list[arb]]]:
    state_boxes = model.boxes()
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
    center_outputs = collide_state(center_state, target_id)
    interval_outputs = collide_state(interval_state, target_id)
    local_interval = gradient_rows(interval_outputs)
    local_center = gradient_rows(center_outputs)
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
    new_centers = [point(value.value) for value in center_outputs]
    new_remainders = [
        sum(
            (
                local_interval[row][inner] - local_center[row][inner]
            ).abs_upper()
            * affine_radii[inner]
            + local_interval[row][inner].abs_upper()
            * model.remainders[inner]
            for inner in range(4)
        )
        + (center_outputs[row].value - new_centers[row]).abs_upper()
        + sum(
            (
                raw_new_affine[row][column]
                - new_affine[row][column]
            ).abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    new_sensitivity = [
        [
            sum(
                local_interval[row][inner] * sensitivity[inner][column]
                for inner in range(4)
            )
            for column in range(2)
        ]
        for row in range(4)
    ]
    return (
        Model(
            new_centers,
            new_affine,
            new_remainders,
            model.domain_radii,
        ),
        new_sensitivity,
    )


def model_terminal_coordinates(
    model: Model,
    sensitivity: list[list[arb]],
) -> tuple[arb, arb, tuple[arb, arb]]:
    boxes = model.boxes()
    variables = [
        Dual(
            boxes[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center, radius = target_geometry(r139.EXPECTED_TERMINAL_OWNER)
    nx = (variables[0] - center[0]) / radius
    ny = (variables[1] - center[1]) / radius
    p = -variables[2] * ny + variables[3] * nx
    require(
        r139.lower.time3.time2_cert.strict_chart(nx.value, ny.value) == "S",
        "model terminal S chart",
    )
    final_gradient = tuple(
        sum(
            p.gradient[inner] * sensitivity[inner][column]
            for inner in range(4)
        )
        for column in range(2)
    )
    return nx.value, p.value, final_gradient


class MarginLedger:
    def __init__(self) -> None:
        self.count = 0
        self.worst_depth = -1
        self.histogram: Counter[str] = Counter()

    def observe(self, name: str, value: arb) -> int:
        require(bool(value > 0), f"nonstrict margin:{name}")
        # Do not turn every one of the 265,328 radius-four decisions into a
        # giant exact Fraction.  Arb's rigorous lower endpoint already has an
        # exact mantissa/exponent representation, so its binary exponent gives
        # the identical conservative dyadic-depth ledger in constant time.
        lower_bound = value.lower()
        require(bool(lower_bound > 0), f"positive lower bound:{name}")
        mantissa, exponent = lower_bound.man_exp()
        integer = int(mantissa)
        require(integer > 0, f"positive mantissa:{name}")
        floor_log2 = integer.bit_length() - 1 + int(exponent)
        if integer & (integer - 1) == 0:
            floor_log2 -= 1
        depth = -floor_log2
        self.count += 1
        self.worst_depth = max(self.worst_depth, depth)
        self.histogram[name] += 1
        return depth

    def public(self) -> dict[str, Any]:
        return {
            "strict_margin_count": self.count,
            "worst_dyadic_depth": self.worst_depth,
            "margin_kind_histogram": dict(sorted(self.histogram.items())),
        }


def full_radius_owner_audit(
    state: Sequence[Dual],
    current_target: str,
    expected_target: str,
    collision_index: int,
    ledger: MarginLedger,
) -> dict[str, arb]:
    qx, qy, ux, uy = (entry.value for entry in state)
    future: list[tuple[str, dict[str, arb]]] = []
    candidates = tuple(r139.lower.charge.candidate_ids_around(current_target))
    require(len(candidates) == 161, "radius-four candidate count")
    histogram: Counter[str] = Counter()
    for candidate_id in candidates:
        center_x, center_y = target_geometry(candidate_id)[0]
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = aq(
            r139.lower.time3.time2_cert.first_hit.RADIUS[candidate_id[0]]
        )
        discriminant = radius * radius - transverse * transverse
        if bool(discriminant < 0):
            ledger.observe("candidate_miss_discriminant", -discriminant)
            histogram["no_real_intersection"] += 1
            continue
        require(
            bool(discriminant > 0),
            f"candidate discriminant resolved:{collision_index}:{candidate_id}:"
            f"{discriminant}",
        )
        ledger.observe("candidate_positive_discriminant", discriminant)
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            ledger.observe("candidate_behind_far_root", -far)
            histogram["intersection_strictly_behind"] += 1
            continue
        require(
            bool(near > 0),
            f"candidate near root resolved:{collision_index}:{candidate_id}:"
            f"{near}",
        )
        ledger.observe("candidate_future_root_positive", near)
        histogram["strict_future_near_root"] += 1
        future.append((
            candidate_id,
            {
                "near": near,
                "radical": radical,
                "transverse": transverse,
                "radius": radius,
                "discriminant": discriminant,
            },
        ))
    selected = next(
        (row for identifier, row in future if identifier == expected_target),
        None,
    )
    require(selected is not None, f"expected target future:{collision_index}")
    for identifier, row in future:
        if identifier != expected_target:
            ledger.observe(
                "winner_pairwise_root_gap",
                row["near"] - selected["near"],
            )
    ledger.observe("selected_root_positive", selected["near"])
    ledger.observe(
        "selected_root_below_tau_max",
        aq(r139.lower.time3.time2_cert.first_hit.TAU_MAX) - selected["near"],
    )
    ledger.observe("selected_discriminant_positive", selected["discriminant"])
    radical, transverse, radius = (
        selected["radical"],
        selected["transverse"],
        selected["radius"],
    )
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    return {
        **selected,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": transverse / radius,
        "cosine": radical / radius,
        "candidate_count": arb(len(candidates)),
        "miss_count": arb(histogram["no_real_intersection"]),
        "behind_count": arb(histogram["intersection_strictly_behind"]),
        "future_count": arb(histogram["strict_future_near_root"]),
    }


def collide(
    state: Sequence[Dual],
    target_id: str,
    ledger: MarginLedger | None = None,
) -> tuple[list[Dual], tuple[Dual, Dual, Dual]]:
    center, radius = target_geometry(target_id)
    position, velocity = state[:2], state[2:]
    displacement = (
        position[0] - center[0],
        position[1] - center[1],
    )
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - radius * radius
    discriminant = linear * linear - offset
    require(bool(discriminant.value > 0), "selected discriminant")
    flight = -linear - dsqrt(discriminant)
    require(bool(flight.value > 0), "selected forward flight")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - center[0]) / radius,
        (impact[1] - center[1]) / radius,
    )
    arrival = -dot(velocity, normal)
    require(bool(arrival.value > 0), "selected incoming cosine")
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    if ledger is not None:
        ledger.observe("selected_dual_discriminant", discriminant.value)
        ledger.observe("selected_dual_flight", flight.value)
        ledger.observe("selected_dual_arrival", arrival.value)
    return list(impact + reflected), (flight, discriminant, arrival)


def terminal_coordinates(
    state: Sequence[Dual],
) -> tuple[Dual, Dual, str]:
    center, radius = target_geometry(r139.EXPECTED_TERMINAL_OWNER)
    nx = (state[0] - center[0]) / radius
    ny = (state[1] - center[1]) / radius
    p = -state[2] * ny + state[3] * nx
    chart = r139.lower.time3.time2_cert.strict_chart(nx.value, ny.value)
    require(chart == "S", "terminal S chart")
    return nx, p, chart


def branch_replay(
    lambda_box: tuple[Q, Q],
    t_star_box: tuple[Q, Q],
    owners: Sequence[str],
    *,
    audit_all_owners: bool,
) -> dict[str, Any]:
    lambda_dual = Dual(
        interval(*lambda_box),
        [arb(1), arb(0)],
    )
    t_star_dual = Dual(
        interval(*t_star_box),
        [arb(0), arb(1)],
    )
    state = initial_state(lambda_dual, t_star_dual)
    ledger = MarginLedger()
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    preterminal_survive_count = 0
    terminal_owner: dict[str, arb] | None = None
    for collision_index, expected in enumerate(owners, start=1):
        audited: dict[str, arb] | None = None
        if audit_all_owners:
            audited = full_radius_owner_audit(
                state,
                current_target,
                expected,
                collision_index,
                ledger,
            )
        state, _metrics = collide(state, expected, ledger)
        if audited is not None:
            owner = {
                "selected_target_id": expected,
                "normal_x": audited["normal_x"],
                "normal_y": audited["normal_y"],
                "p": audited["p"],
                "cosine": audited["cosine"],
            }
            classification, destination, _witnesses = (
                r139.lower.time3.core_classification(
                    owner, tuple(r139.lower.core_cert.physical_cores())
                )
            )
            if collision_index < RETURN_DEPTH:
                require(
                    classification == "SURVIVE_THROUGH_3_INNER"
                    and destination is None,
                    f"preterminal nonreturn:{collision_index}",
                )
                preterminal_survive_count += 1
            else:
                require(
                    classification == "UNRESOLVED_TIME3_OUTER"
                    and destination is None,
                    "terminal face unresolved only",
                )
                terminal_owner = owner
        current_target = expected
    t_terminal, p_terminal, chart = terminal_coordinates(state)
    if terminal_owner is not None:
        require(
            bool(t_terminal.value > aq(DESTINATION_T_BOUNDS[0]))
            and bool(t_terminal.value < aq(DESTINATION_T_BOUNDS[1]))
            and bool(p_terminal.value > aq(Q(-21, 1000)))
            and bool(p_terminal.value < aq(Q(-19, 1000))),
            "only terminal p0 face active",
        )
    return {
        "t": t_terminal,
        "p": p_terminal,
        "chart": chart,
        "ledger": ledger.public(),
        "preterminal_survive_count": preterminal_survive_count,
        "all_owner_audit": audit_all_owners,
    }


def model_branch_replay(
    lambda_box: tuple[Q, Q],
    t_star_box: tuple[Q, Q],
    owners: Sequence[str],
    *,
    audit_all_owners: bool,
) -> dict[str, Any]:
    """Recenter after every collision and rigorously propagate sensitivities."""

    model, sensitivity = initial_model(lambda_box, t_star_box)
    ledger = MarginLedger()
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    preterminal_survive_count = 0
    maximum_radius = arb(0)
    for collision_index, expected in enumerate(owners, start=1):
        state_boxes = model.boxes()
        maximum_radius = max(
            [maximum_radius]
            + [radius.abs_upper() for radius in model.radii()]
        )
        if audit_all_owners:
            audited = full_radius_owner_audit(
                [Dual(value) for value in state_boxes],
                current_target,
                expected,
                collision_index,
                ledger,
            )
            owner = {
                "selected_target_id": expected,
                "normal_x": audited["normal_x"],
                "normal_y": audited["normal_y"],
                "p": audited["p"],
                "cosine": audited["cosine"],
            }
            classification, destination, _witnesses = (
                r139.lower.time3.core_classification(
                    owner, tuple(r139.lower.core_cert.physical_cores())
                )
            )
            if collision_index < RETURN_DEPTH:
                require(
                    classification == "SURVIVE_THROUGH_3_INNER"
                    and destination is None,
                    f"model preterminal nonreturn:{collision_index}",
                )
                preterminal_survive_count += 1
            else:
                require(
                    classification == "UNRESOLVED_TIME3_OUTER"
                    and destination is None,
                    "model terminal face unresolved only",
                )
        model, sensitivity = step_model(model, sensitivity, expected)
        current_target = expected
    t_terminal, p_terminal, terminal_gradient = model_terminal_coordinates(
        model, sensitivity
    )
    if audit_all_owners:
        require(
            bool(t_terminal > aq(DESTINATION_T_BOUNDS[0]))
            and bool(t_terminal < aq(DESTINATION_T_BOUNDS[1]))
            and bool(p_terminal > aq(Q(-21, 1000)))
            and bool(p_terminal < aq(Q(-19, 1000))),
            "model only terminal p0 face active",
        )
    return {
        "t_value": t_terminal,
        "p_value": p_terminal,
        "p_gradient": terminal_gradient,
        "ledger": ledger.public(),
        "preterminal_survive_count": preterminal_survive_count,
        "all_owner_audit": audit_all_owners,
        "maximum_state_radius_outer": fixed_outer(maximum_radius, 256),
    }


def point_branch(
    lambda_value: Q,
    t_star_value: Q,
    owners: Sequence[str],
) -> tuple[Q, Q]:
    replay = branch_replay(
        (lambda_value, lambda_value),
        (t_star_value, t_star_value),
        owners,
        audit_all_owners=False,
    )
    value = r139.lower.round136.exact_dyadic(
        (replay["p"].value - aq(TERMINAL_FACE_P)).mid()
    )
    derivative = r139.lower.round136.exact_dyadic(
        replay["p"].gradient[0].mid()
    )
    require(derivative < 0, "Newton derivative negative")
    return value, derivative


def isolate_endpoint(
    t_star_box: tuple[Q, Q],
    owners: Sequence[str],
) -> tuple[tuple[Q, Q], dict[str, Any]]:
    t_mid = (t_star_box[0] + t_star_box[1]) / 2
    center = Q(
        "1.1414841623589467399290134536804803505190298238970554707648068"
    )
    rows: list[dict[str, Any]] = []
    for index in range(NEWTON_ITERATIONS):
        value, derivative = point_branch(center, t_mid, owners)
        next_center = nearest_dyadic(
            center - value / derivative,
            NEWTON_BITS,
        )
        rows.append({
            "iteration": index + 1,
            "center_sha256": digest(qstr(center)),
            "value_sign": -1 if value < 0 else (1 if value > 0 else 0),
            "derivative_sign": -1,
            "next_center_sha256": digest(qstr(next_center)),
        })
        center = next_center
    half = Q(1, 2**ROOT_HALF_WIDTH_POWER)
    bracket = (center - half, center + half)
    # Point Newton above is only a locator.  Every formal sign, derivative,
    # owner and nonreturn assertion below is rebuilt with the recentered
    # affine state model at its separately frozen precision.
    ctx.prec = PRECISION_BITS
    left = model_branch_replay(
        (bracket[0], bracket[0]),
        t_star_box,
        owners,
        audit_all_owners=False,
    )
    right = model_branch_replay(
        (bracket[1], bracket[1]),
        t_star_box,
        owners,
        audit_all_owners=False,
    )
    whole = model_branch_replay(
        bracket,
        t_star_box,
        owners,
        audit_all_owners=True,
    )
    left_f = left["p_value"] - aq(TERMINAL_FACE_P)
    right_f = right["p_value"] - aq(TERMINAL_FACE_P)
    derivative = whole["p_gradient"][0]
    require(
        bool(left_f > 0)
        and bool(right_f < 0)
        and bool(derivative < 0),
        "terminal endpoint isolation",
    )
    require(
        Q(1) < bracket[0] < bracket[1] < Q(2),
        "endpoint between dyadic probes",
    )
    return bracket, {
        "newton_rows": rows,
        "left_endpoint_sign": 1,
        "right_endpoint_sign": -1,
        "whole_derivative_sign": -1,
        "whole_derivative_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-derivative),
        "terminal_t_outer": [
            qstr(value) for value in fixed_outer(whole["t_value"])
        ],
        "terminal_p_outer": [
            qstr(value) for value in fixed_outer(whole["p_value"])
        ],
        "complete_radius4_owner_audit": whole["ledger"],
        "maximum_recentered_state_radius_outer": [
            qstr(value) for value in whole["maximum_state_radius_outer"]
        ],
        "preterminal_strict_nonreturn_count":
            whole["preterminal_survive_count"],
        "terminal_only_active_face":
            "G:S p0=-1/50 of core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2",
    }


def first_two_strict_points(
    lower_outer: tuple[Q, Q],
    upper_outer: tuple[Q, Q],
    level: int,
) -> tuple[int, int] | None:
    denominator = 2**level
    left = (
        lower_outer[1].numerator * denominator
        // lower_outer[1].denominator
        + 1
    )
    right = left + 1
    if (
        left >= 1
        and right <= denominator - 1
        and Q(left, denominator) > lower_outer[1]
        and Q(right, denominator) < upper_outer[0]
    ):
        return left, right
    return None


def least_contained_1d_row(
    lower_outer: tuple[Q, Q],
    upper_outer: tuple[Q, Q],
) -> tuple[int, int, int]:
    require(
        Q(0) < lower_outer[0] < lower_outer[1]
        < upper_outer[0] < upper_outer[1] < Q(1),
        "normalized candidate interval",
    )
    level = 2
    while True:
        pair = first_two_strict_points(lower_outer, upper_outer, level)
        if pair is not None:
            row = (level, *pair)
            rank137.validate_1d_row(row)
            if level > 2:
                require(
                    first_two_strict_points(
                        lower_outer, upper_outer, level - 1
                    ) is None,
                    "minimal contained level",
                )
            return row
        level += 1


def coordinate_rank(
    name: str,
    lower_value: arb,
    upper_value: arb,
) -> dict[str, Any]:
    lower_outer = fixed_outer(lower_value)
    upper_outer = fixed_outer(upper_value)
    row = least_contained_1d_row(lower_outer, upper_outer)
    rank = rank137.rank_1d(row)
    require(rank137.unrank_1d(rank) == row, "1D rank roundtrip")
    denominator = 2**row[0]
    require(
        lower_outer[1] < Q(row[1], denominator)
        < Q(row[2], denominator) < upper_outer[0],
        "rank row strict containment",
    )
    return {
        "coordinate": name,
        "endpoint_fixed_dyadic_outers": {
            "left": [qstr(value) for value in lower_outer],
            "right": [qstr(value) for value in upper_outer],
        },
        "contained_primitive_basis_row": list(row),
        "contained_primitive_basis_rank": encoded_integer(rank),
        "rank_unrank_roundtrip_exact": True,
        "minimal_level_with_two_strict_grid_points": True,
        "lex_first_consecutive_pair_at_that_level": True,
        "least_Round137_v1_rank_for_this_declared_coordinate_interval": True,
        "historical_Round35_coordinate_crosswalk": False,
    }


def exact_ceil_ball(value: arb) -> int:
    lower, upper = r139.lower.round136.arb_pair(value)
    lower_floor = r139.lower.floor_q(lower)
    upper_floor = r139.lower.floor_q(upper)
    require(lower_floor == upper_floor and lower > lower_floor, "exact ceil ball")
    return lower_floor + 1


def build() -> dict[str, Any]:
    ctx.prec = DISCOVERY_PRECISION_BITS
    dependencies = validate_dependencies()
    round139 = dependencies["Round139"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in round139["collision_rows"]
    ]
    require(
        len(owners) == RETURN_DEPTH
        and digest(owners) == r139.EXPECTED_OWNER_SEQUENCE_SHA256
        and owners[-1] == r139.EXPECTED_TERMINAL_OWNER,
        "frozen owner sequence",
    )
    t_star_box = tuple(
        Q(value)
        for value in round139["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    require(len(t_star_box) == 2 and t_star_box[0] < t_star_box[1], "D0 root")
    lambda_box, endpoint_proof = isolate_endpoint(t_star_box, owners)

    lambda_ball = interval(*lambda_box)
    t_star_ball = interval(*t_star_box)
    sqrt17 = arb(17).sqrt()
    displacement_x = lambda_ball / (arb(2) ** LAMBDA_SCALE_POWER)
    x_right = sqrt17 * aq(r139.lower.R_W) * t_star_ball.asin()
    x_left = x_right - displacement_x
    t_left = (
        t_star_ball.asin()
        - displacement_x / (aq(r139.lower.R_W) * sqrt17)
    ).sin()
    u_left = 100 * t_left - 1
    u_right = 100 * t_star_ball - 1
    rank_x = coordinate_rank("x=sqrt(17)*r", x_left, x_right)
    rank_u = coordinate_rank(
        "u=(t-1/100)/(1/100)=100*t-1",
        u_left,
        u_right,
    )
    require(
        rank_x["contained_primitive_basis_row"][0] !=
        rank_u["contained_primitive_basis_row"][0],
        "coordinate dependence witness",
    )

    source_adapted_length = (
        aq(Q(41, 4)) * displacement_x / sqrt17
    )
    require(
        bool(source_adapted_length > 0)
        and bool(source_adapted_length < aq(DELTA_14))
        and bool(source_adapted_length < aq(Q(1, RECUT_DENOMINATOR))),
        "one source mesh and recut cell",
    )
    source_length_outer = fixed_outer(source_adapted_length)

    right_replay = model_branch_replay(
        (Q(0), Q(0)),
        t_star_box,
        owners,
        audit_all_owners=False,
    )
    left_t = interval(
        *(Q(value) for value in endpoint_proof["terminal_t_outer"])
    )
    right_t = right_replay["t_value"]
    right_p = right_replay["p_value"]
    image_length_expression = (
        right_t.asin()
        - left_t.asin()
        + right_p.asin()
        - aq(TERMINAL_FACE_P).asin()
    )
    require(
        bool(image_length_expression > 0)
        and bool(image_length_expression < aq(Q(1))),
        "formal image endpoint length expression",
    )
    image_length_outer = fixed_outer(image_length_expression)
    image_recut_count = exact_ceil_ball(
        image_length_expression * RECUT_DENOMINATOR
    )
    require(image_recut_count > 1, "nontrivial image recut count")

    prospective_interval_payload = {
        "Round139_result_sha256":
            digest(round139),
        "owner_sequence_sha256": digest(owners),
        "lambda_scale_power": LAMBDA_SCALE_POWER,
        "lambda_bracket": [qstr(value) for value in lambda_box],
        "right_endpoint": "collision-3 D0 tangency x_star",
        "left_endpoint": "terminal G:S p=-1/50 face preimage",
    }
    prospective_interval_id = (
        "round143-prospective-face-to-d0-leaf-interval:"
        + digest(prospective_interval_payload)
    )
    prospective_recut_payload = {
        "prospective_interval_id": prospective_interval_id,
        "source_short_cell_k": 0,
        "formal_image_length_outer":
            [qstr(value) for value in image_length_outer],
        "image_recut_count": str(image_recut_count),
    }

    result = {
        "status":
            "CERTIFIED_LOCAL_R1648_TERMINAL_FACE_ENDPOINT_WITH_PROSPECTIVE_RECUT_FRONTIER",
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_or_Round140_files_modified": False,
            "Round141_or_Round142_files_modified": False,
        },
        "frozen_branch": {
            "return_depth": RETURN_DEPTH,
            "owner_sequence_sha256": digest(owners),
            "official_sequence_sha256":
                round139["local_first_return_summary"][
                    "official_word_key_sequence_sha256"
                ],
            "compact_path_sha256":
                round139["local_first_return_summary"][
                    "combined_compact_path_rows_sha256"
                ],
            "terminal_absolute_owner": r139.EXPECTED_TERMINAL_OWNER,
            "destination_core_id": r139.EXPECTED_DESTINATION_CORE_ID,
            "s": "0",
            "leaf": "asin(p)-4*r=b_star",
            "intrinsic_coordinate": "x=sqrt(17)*r",
        },
        "terminal_face_endpoint": {
            "scaled_coordinate":
                "lambda=(x_star-x)*2^4289, increasing to the left",
            "lambda_bracket": [qstr(value) for value in lambda_box],
            "lambda_bracket_width": qstr(lambda_box[1] - lambda_box[0]),
            "lambda_between_one_and_two": True,
            "equivalent_displacement_bounds":
                "2^-4289 < x_star-x_left < 2^-4288",
            "face_equation": "p_1648(lambda)=-1/50",
            "endpoint_sign_order":
                "p_1648(lambda_lower)>-1/50>p_1648(lambda_upper)",
            "strict_derivative":
                "d p_1648/d lambda < 0 on the whole root bracket",
            "unique_root_in_bracket": True,
            "discovery_point_dual_precision_bits":
                DISCOVERY_PRECISION_BITS,
            "validated_recentered_affine_precision_bits": PRECISION_BITS,
            "proof": endpoint_proof,
            "local_full_radius4_owner_sequence_certified": True,
            "local_preterminal_nonreturn_certified": True,
            "local_terminal_only_active_face_certified": True,
        },
        "candidate_full_leaf_interval": {
            "prospective_interval_id": prospective_interval_id,
            "payload_sha256": digest(prospective_interval_payload),
            "left_endpoint": "unique terminal-face root above",
            "right_endpoint": "Round139 collision-3 D0 root x_star",
            "open_interval": "(x_left,x_star)",
            "positive_width": True,
            "source_adapted_line_element":
                "dell_*=(25/4+4)|dr|=(41/(4*sqrt(17)))dx",
            "source_adapted_length_outer":
                [qstr(value) for value in source_length_outer],
            "source_adapted_length_below_delta_14": True,
            "source_adapted_length_below_1e_minus_90": True,
            "whole_interval_owner_corridor_certified": False,
            "whole_interval_equals_maximal_U_intersection_leaf_certified": False,
            "exact_first_blocker": (
                "the pinned chain certifies the frozen word only on the "
                "Round139 2^-5888 collar and locally at the new face root; "
                "it has no validated connected all-owner/nonreturn cover of "
                "the intervening scale-2^-4289 corridor"
            ),
        },
        "coordinate_explicit_Round137_v1_leaf_ranks": {
            "contract": "round137-dyadic-basis-enumeration-v1",
            "canonical_H1_x_candidate": rank_x,
            "Round140_normalized_t_candidate": rank_u,
            "coordinate_dependence_witnessed_by_different_levels": True,
            "historical_Round35_leaf_coordinate_frozen": False,
            "historical_Round35_source_interval_rank": None,
            "reason_historical_rank_null": (
                "Round35 did not freeze the leaf-coordinate normalization, "
                "and the candidate interval has not been identified with a "
                "maximal U-intersection leaf"
            ),
        },
        "B14_source_mesh_frontier": {
            "incidence_rank_B": 14,
            "mesh_formula": "delta_B=2^-ceil(3(B+1)/2)",
            "delta_14": qstr(DELTA_14),
            "candidate_interval_is_one_clipped_B14_cell": True,
            "corrected_Round47_source_coordinate":
                "adapted u_* from the oriented left endpoint",
            "candidate_interval_is_one_clipped_1e_minus_90_source_cell": True,
            "prospective_left_anchored_natural_short_cell_k": 0,
            "historical_natural_short_cell_k": None,
            "historical_source_parent_W_id": None,
            "reason_historical_k_null":
                "the maximal physical source interval and its historical oriented origin are not materialized",
        },
        "formal_image_recut_frontier": {
            "terminal_chart": "G:S",
            "left_endpoint": {
                "t_outer": endpoint_proof["terminal_t_outer"],
                "p": "-1/50",
            },
            "right_branch_limit_endpoint": {
                "t_outer": [
                    qstr(value) for value in fixed_outer(right_t)
                ],
                "p_outer": [
                    qstr(value) for value in fixed_outer(right_p)
                ],
                "actual_regular_D0_endpoint_claimed": False,
            },
            "adapted_length_endpoint_formula":
                "asin(t_right)-asin(t_left)+asin(p_right)-asin(-1/50)",
            "formal_adapted_length_outer":
                [qstr(value) for value in image_length_outer],
            "deterministic_recut_scale": "1e-90",
            "conditional_image_recut_count":
                encoded_integer(image_recut_count),
            "conditional_image_recut_rank_range":
                [0, str(image_recut_count - 1)],
            "conditional_first_image_recut_rank": 0,
            "conditional_last_image_recut_rank":
                str(image_recut_count - 1),
            "prospective_recut_registry_id":
                "round143-prospective-image-recut-registry:"
                + digest(prospective_recut_payload),
            "full_connected_physical_image_parent_certified": False,
            "historical_image_recut_rank": None,
            "historical_Round35_restriction_id": None,
            "conditional_scope": (
                "the count/rank range becomes the deterministic image recut "
                "ledger exactly if the missing full source corridor is "
                "certified as one connected physical branch; it is not a "
                "historical Round35 identifier in this round"
            ),
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
        "count_ledger": {
            "local_terminal_face_endpoint_count": 1,
            "complete_radius4_candidate_test_count":
                161 * RETURN_DEPTH,
            "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
            "coordinate_explicit_prospective_leaf_rank_count": 2,
            "historical_leaf_rank_count": 0,
            "historical_parent_W_count": 0,
            "historical_image_recut_rank_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_nonclaims": [
            "the local terminal-face root plus the Round139 D0 root do not by themselves prove every intervening point has the frozen word",
            "the candidate face-to-D0 interval is not asserted to be a maximal regular component or U-intersection leaf",
            "coordinate-explicit Round137-v1 ranks are prospective locators, not the unnamed historical Round35 source interval rank",
            "k=0 and the image rank range are conditional deterministic ledgers, not historical IDs",
            "the D0 branch-limit image endpoint is not asserted to be an actual regular trajectory",
            "no Gate5 field, complete block, or CM2 claim is promoted",
        ],
    }
    require(
        result["strict_nonpromotion"]["global_gate5_maturity"] == "10/18"
        and result["strict_nonpromotion"][
            "global_complete_18_field_block_count"
        ] == 0
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "global nonpromotion",
    )
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    require(not path.is_symlink(), "output symlink")
    resolved = path.resolve()
    protected = {
        Path(__file__).resolve(),
        FUTURE_VERIFIER.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }
    require(resolved not in protected, "output aliases protected input")
    require(
        resolved.name not in {"", ".", ".."}
        and resolved.parent.is_dir()
        and not path.parent.is_symlink(),
        "safe output directory",
    )
    if path.exists():
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink(),
            "safe existing output",
        )
        require(
            all(
                not item.exists() or not os.path.samefile(path, item)
                for item in protected
            ),
            "output hardlink aliases protected input",
        )
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{resolved.name}.",
        suffix=".tmp",
        dir=resolved.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    envelope = build()
    write_atomic(args.output, envelope)
    print(canonical({
        "status": envelope["result"]["status"],
        "lambda_bracket":
            envelope["result"]["terminal_face_endpoint"]["lambda_bracket"],
        "x_rank_level":
            envelope["result"][
                "coordinate_explicit_Round137_v1_leaf_ranks"
            ]["canonical_H1_x_candidate"]["contained_primitive_basis_row"][0],
        "conditional_image_recut_count_sha256":
            envelope["result"]["formal_image_recut_frontier"][
                "conditional_image_recut_count"
            ]["sha256_of_decimal"],
        "historical_parent_W_id": None,
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
