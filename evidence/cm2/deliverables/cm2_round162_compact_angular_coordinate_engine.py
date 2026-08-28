#!/usr/bin/env python3
"""Exact compact angular-coordinate infrastructure for CM2 Round162.

This module does not continue the R1648 orbit and does not perform the
exterior-sheet branch-and-bound.  It supplies the exact four-chart source
atlas, its algebraic seam ledger, and a rigorous lift of the three Round161
endpoint faces into the current E half-angle chart.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round161_dyadic_sheared_recentering_engine as r161


HERE = Path(__file__).resolve().parent
PRECISION = 8192
OUTER_BITS = 4608
POWER = 4296
ENDPOINT_U = Q(2500000000000000)
KAPPA_ISOLATION_BITS = 256
ROUND161_ENGINE = "cm2_round161_dyadic_sheared_recentering_engine.py"
ROUND161_ENGINE_SHA256 = (
    "ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f"
)
ROUND146_PHYSICAL_ENGINE = "cm2_round146_physical_centered_jet_2d_engine.py"
ROUND146_PHYSICAL_ENGINE_SHA256 = (
    "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb"
)

CHART_AXES: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {
    "E": ((1, 0), (0, 1)),
    "N": ((0, 1), (-1, 0)),
    "W": ((-1, 0), (0, -1)),
    "S": ((0, -1), (1, 0)),
}
CYCLIC_SEAMS = (
    ("E", 1, "N", -1),
    ("N", 1, "W", -1),
    ("W", 1, "S", -1),
    ("S", 1, "E", -1),
)
ENDPOINT_TYPED_FACES = {
    "C24_EVENT": (Q(-430), Q(-405)),
    "STRICT_RETURN_BRIDGE": (Q(-405), Q(-350)),
    "D3_EVENT": (Q(-350), Q(134111000000)),
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


def qstr(value: Q) -> str:
    return r161.qstr(value)


def check_pins() -> None:
    require(
        Path(r161.__file__).resolve() == (HERE / ROUND161_ENGINE).resolve(),
        "Round161 engine module identity",
    )
    require(
        sha256(HERE / ROUND161_ENGINE) == ROUND161_ENGINE_SHA256,
        "Round161 engine source pin",
    )
    require(
        sha256(HERE / ROUND146_PHYSICAL_ENGINE)
        == ROUND146_PHYSICAL_ENGINE_SHA256,
        "Round146 physical-map source pin",
    )
    require(
        r161.r160.POWER == POWER
        and r161.r160.r150.r139.lower.SOURCE_ABSOLUTE_OWNER == "W[0,0]"
        and r161.r160.r150.r139.lower.R_W == Q(4, 25)
        and r161.r160.r150.r139.lower.SOURCE_P_STAR
        == Q(-1587, 1638400),
        "pinned physical-map constants",
    )
    r161.check_pins()


def fixed_outer(value: arb, bits: int = OUTER_BITS) -> list[str]:
    return r161.r160.fixed_outer(value, bits)


def overlap_all(left: list[arb], right: list[arb], label: str) -> None:
    require(len(left) == len(right), label + " dimension")
    require(
        all(a.overlaps(b) for a, b in zip(left, right)),
        label + " enclosure overlap",
    )


@dataclass(frozen=True)
class QK:
    """Element a+b*kappa in Q[kappa]/(kappa^2+2*kappa-1)."""

    a: Q
    b: Q = Q(0)

    @staticmethod
    def coerce(value: QK | Q | int) -> QK:
        if isinstance(value, QK):
            return value
        return QK(Q(value))

    def __add__(self, other: QK | Q | int) -> QK:
        rhs = self.coerce(other)
        return QK(self.a + rhs.a, self.b + rhs.b)

    __radd__ = __add__

    def __neg__(self) -> QK:
        return QK(-self.a, -self.b)

    def __sub__(self, other: QK | Q | int) -> QK:
        return self + (-self.coerce(other))

    def __rsub__(self, other: QK | Q | int) -> QK:
        return self.coerce(other) - self

    def __mul__(self, other: QK | Q | int) -> QK:
        rhs = self.coerce(other)
        return QK(
            self.a * rhs.a + self.b * rhs.b,
            self.a * rhs.b
            + self.b * rhs.a
            - 2 * self.b * rhs.b,
        )

    __rmul__ = __mul__

    def inverse(self) -> QK:
        determinant = self.a * self.a - 2 * self.a * self.b - self.b * self.b
        require(determinant != 0, "Q(kappa) nonzero divisor")
        return QK(
            (self.a - 2 * self.b) / determinant,
            -self.b / determinant,
        )

    def __truediv__(self, other: QK | Q | int) -> QK:
        return self * self.coerce(other).inverse()

    def record(self) -> list[str]:
        return [qstr(self.a), qstr(self.b)]


KAPPA = QK(Q(0), Q(1))


def kappa_isolation() -> dict[str, Any]:
    scale = 1 << KAPPA_ISOLATION_BITS
    sqrt2_floor = math.isqrt(1 << (2 * KAPPA_ISOLATION_BITS + 1))
    lower = Q(sqrt2_floor - scale, scale)
    upper = Q(sqrt2_floor - scale + 1, scale)

    def polynomial(x: Q) -> Q:
        return x * x + 2 * x - 1

    p_lower = polynomial(lower)
    p_upper = polynomial(upper)
    require(
        Q(0) < lower < upper < Q(1)
        and upper - lower == Q(1, scale)
        and p_lower < 0 < p_upper,
        "kappa dyadic isolation",
    )
    require(2 * lower + 2 > 0, "kappa polynomial monotonicity")
    return {
        "algebraic_definition": "kappa=sqrt(2)-1",
        "minimal_polynomial": "x^2+2*x-1",
        "dyadic_isolating_interval": [qstr(lower), qstr(upper)],
        "isolating_width": qstr(upper - lower),
        "polynomial_at_lower": qstr(p_lower),
        "polynomial_at_upper": qstr(p_upper),
        "lower_sign": "NEGATIVE",
        "upper_sign": "POSITIVE",
        "derivative": "2*x+2",
        "derivative_lower_bound": qstr(2 * lower + 2),
        "derivative_strict_positive_on_interval": True,
        "unique_root_in_interval": True,
        "selected_root_in_0_1": True,
        "quotient_relation": "kappa^2=1-2*kappa",
    }


def chart_normal(chart: str, z: QK) -> tuple[QK, QK]:
    require(chart in CHART_AXES, "chart id")
    e, je = CHART_AXES[chart]
    denominator = QK(1) + z * z
    along = (QK(1) - z * z) / denominator
    across = (2 * z) / denominator
    return (
        e[0] * along + je[0] * across,
        e[1] * along + je[1] * across,
    )


def rotate(normal: tuple[QK, QK]) -> tuple[QK, QK]:
    return (-normal[1], normal[0])


def symbolic_state_template(
    normal: tuple[QK, QK],
) -> dict[str, Any]:
    jnormal = rotate(normal)
    center = QK(Q(1, 2))
    radius = Q(4, 25)
    position = (
        center + radius * normal[0],
        center + radius * normal[1],
    )
    velocity_numerator = (
        (normal[0], 2 * jnormal[0], -normal[0]),
        (normal[1], 2 * jnormal[1], -normal[1]),
    )
    return {
        "coefficient_field": (
            "Q[kappa]/(kappa^2+2*kappa-1); each scalar is [a,b]=a+b*kappa"
        ),
        "normal": [entry.record() for entry in normal],
        "quarter_turn_normal": [entry.record() for entry in jnormal],
        "position": [entry.record() for entry in position],
        "velocity_denominator": "1+q^2",
        "velocity_numerator_coefficients_in_1_q_q2": [
            [entry.record() for entry in row]
            for row in velocity_numerator
        ],
    }


def seam_ledger() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for left_chart, left_sign, right_chart, right_sign in CYCLIC_SEAMS:
        left_normal = chart_normal(left_chart, left_sign * KAPPA)
        right_normal = chart_normal(right_chart, right_sign * KAPPA)
        require(left_normal == right_normal, "exact cyclic normal gluing")
        left_state = symbolic_state_template(left_normal)
        right_state = symbolic_state_template(right_normal)
        require(left_state == right_state, "exact cyclic physical gluing")
        left_digest = digest(left_state)
        right_digest = digest(right_state)
        require(left_digest == right_digest, "cyclic state digest equality")
        records.append(
            {
                "left_face": {
                    "chart": left_chart,
                    "z": "+kappa" if left_sign > 0 else "-kappa",
                },
                "right_face": {
                    "chart": right_chart,
                    "z": "+kappa" if right_sign > 0 else "-kappa",
                },
                "shared_q_domain": ["-1", "1"],
                "left_physical_state_template": left_state,
                "right_physical_state_template": right_state,
                "left_physical_state_sha256": left_digest,
                "right_physical_state_sha256": right_digest,
                "physical_state_digests_equal": True,
                "exact_gluing_for_every_q": True,
            }
        )
    require(len(records) == 4, "four cyclic seams")
    return records


def chart_atlas() -> dict[str, Any]:
    charts = []
    for chart, (axis, quarter_turn) in CHART_AXES.items():
        charts.append(
            {
                "chart": chart,
                "theta": {
                    "E": "0",
                    "N": "pi/2",
                    "W": "pi",
                    "S": "-pi/2",
                }[chart],
                "axis": list(axis),
                "quarter_turn_axis": list(quarter_turn),
                "z_domain": ["-kappa", "kappa"],
                "q_domain": ["-1", "1"],
            }
        )
    return {
        "physical_parameter_quotient": "S1_A x [-1,1]_p",
        "lift_fold": "Phi identified with pi-Phi through p=sin(Phi)",
        "source_chart_count": 4,
        "charts": charts,
        "state_map": {
            "z": "tan((A-theta_C)/2)",
            "q": "tan(Phi/2)",
            "normal": "((1-z^2)*e_C+2*z*J*e_C)/(1+z^2)",
            "p": "2*q/(1+q^2)",
            "radial": "(1-q^2)/(1+q^2)",
            "velocity": "radial*normal+p*J*normal",
        },
        "denominator_positivity": {
            "1+z^2_lower_bound": "1",
            "1+q^2_lower_bound": "1",
            "both_strict_positive_on_closed_chart_domains": True,
            "no_inverse_trigonometric_or_square_root_dependency_in_state_map":
                True,
        },
    }


def grazing_ledger() -> dict[str, Any]:
    return {
        "q_plus_one": {
            "q": "1",
            "denominator": "2",
            "p": "1",
            "radial": "0",
            "velocity": "+J*normal",
            "stratum": "SOURCE_GRAZING_P_PLUS_ONE",
        },
        "q_minus_one": {
            "q": "-1",
            "denominator": "2",
            "p": "-1",
            "radial": "0",
            "velocity": "-J*normal",
            "stratum": "SOURCE_GRAZING_P_MINUS_ONE",
        },
        "both_are_physical_boundary_strata": True,
        "neither_is_removed_by_a_coordinate_singularity": True,
        "classification_credit": (
            "typed infrastructure only; no exterior leaf is classified here"
        ),
    }


def _endpoint_angles(w_lower: Q, w_upper: Q) -> dict[str, Any]:
    ctx.prec = PRECISION
    aq = r161.r160.r150.r139.lower.aq
    root = r161.r160.r150.load_seed()[1]
    root_lower, root_upper = map(aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + r161.r160.r146.symmetric((root_upper - root_lower) / 2)
    )
    h = aq(Q(1, 2**POWER))
    sqrt17 = aq(Q(17)).sqrt()
    radius = aq(Q(4, 25))
    u = aq(ENDPOINT_U)
    w_center = (w_lower + w_upper) / 2
    w_radius = (w_upper - w_lower) / 2
    w_ball = aq(w_center) + r161.r160.r146.symmetric(aq(w_radius))
    slope = aq(r161.SLOPE)
    angle_a = t_star.asin() - u * h / (radius * sqrt17)
    phase_phi = (
        aq(r161.r160.r150.r139.lower.SOURCE_P_STAR).asin()
        + (-4 * u / sqrt17 + slope * u + w_ball) * h
    )
    z = (angle_a / 2).tan()
    q = (phase_phi / 2).tan()
    eta_lower = Q(w_lower, 2**POWER)
    eta_upper = Q(w_upper, 2**POWER)

    kappa_lower = Q(kappa_isolation()["dyadic_isolating_interval"][0])
    require(
        bool(z > -aq(kappa_lower))
        and bool(z < aq(kappa_lower))
        and bool(q > -1)
        and bool(q < 1),
        "Round161 endpoint strictly inside E compact chart",
    )
    require(
        bool(phase_phi > -aq(1))
        and bool(phase_phi < aq(1)),
        "positive-radial Phi branch",
    )

    normal = (
        (1 - z * z) / (1 + z * z),
        2 * z / (1 + z * z),
    )
    p = 2 * q / (1 + q * q)
    radial = (1 - q * q) / (1 + q * q)
    jnormal = (-normal[1], normal[0])
    position = (
        aq(Q(1, 2)) + radius * normal[0],
        aq(Q(1, 2)) + radius * normal[1],
    )
    velocity = (
        radial * normal[0] + p * jnormal[0],
        radial * normal[1] + p * jnormal[1],
    )

    direct_normal = (angle_a.cos(), angle_a.sin())
    direct_p = phase_phi.sin()
    direct_radial = phase_phi.cos()
    direct_jnormal = (-direct_normal[1], direct_normal[0])
    direct_state = [
        aq(Q(1, 2)) + radius * direct_normal[0],
        aq(Q(1, 2)) + radius * direct_normal[1],
        direct_radial * direct_normal[0] + direct_p * direct_jnormal[0],
        direct_radial * direct_normal[1] + direct_p * direct_jnormal[1],
    ]
    rational_state = list(position + velocity)
    overlap_all(
        rational_state,
        direct_state,
        "half-angle and pinned physical map",
    )
    return {
        "chart": "E",
        "u_in_h_units": qstr(ENDPOINT_U),
        "w_in_h_units": [qstr(w_lower), qstr(w_upper)],
        "A_outer": fixed_outer(angle_a),
        "Phi_outer": fixed_outer(phase_phi),
        "z_outer": fixed_outer(z),
        "q_outer": fixed_outer(q),
        "eta_definition": "eta=Phi-Phi0-m*(A-A0)=h*w",
        "eta_exact_enclosure": [qstr(eta_lower), qstr(eta_upper)],
        "m_definition": (
            "m=4*R_W-R_W*sqrt(17)*s with "
            "s=1403486916994043/500000000000000"
        ),
        "z_strictly_inside_minus_kappa_kappa": True,
        "q_strictly_inside_minus_one_one": True,
        "positive_radial_branch": True,
        "q_strictly_increasing_in_eta_at_fixed_A": True,
        "half_angle_state_outer": [
            fixed_outer(value) for value in rational_state
        ],
        "pinned_physical_map_state_outer": [
            fixed_outer(value) for value in direct_state
        ],
        "half_angle_and_pinned_physical_state_enclosures_overlap":
            True,
    }


def endpoint_face_lift() -> dict[str, Any]:
    check_pins()
    faces = {
        kind: _endpoint_angles(lower, upper)
        for kind, (lower, upper) in ENDPOINT_TYPED_FACES.items()
    }
    common_z = {canonical(face["z_outer"]) for face in faces.values()}
    require(len(common_z) == 1, "common endpoint E-chart z enclosure")
    common_z_outer = faces["C24_EVENT"]["z_outer"]
    require(
        faces["C24_EVENT"]["eta_exact_enclosure"][1]
        == faces["STRICT_RETURN_BRIDGE"]["eta_exact_enclosure"][0]
        and faces["STRICT_RETURN_BRIDGE"]["eta_exact_enclosure"][1]
        == faces["D3_EVENT"]["eta_exact_enclosure"][0],
        "exact endpoint eta seam adjacency",
    )
    return {
        "source_round": 161,
        "source_endpoint_u_in_h_units": qstr(ENDPOINT_U),
        "source_slope_s": qstr(r161.SLOPE),
        "current_source_chart": "E",
        "all_three_faces_strictly_inside_E_chart": True,
        "all_three_faces_strictly_away_from_q_grazing": True,
        "common_z_outer": common_z_outer,
        "typed_faces": faces,
        "exact_eta_face_adjacencies_preserved": True,
        "this_is_a_coordinate_lift_not_a_new_continuation_slab": True,
    }


def build_infrastructure() -> dict[str, Any]:
    check_pins()
    kappa = kappa_isolation()
    seams = seam_ledger()
    lift = endpoint_face_lift()
    return {
        "status": (
            "CERTIFIED_COMPACT_ANGULAR_COORDINATE_INFRASTRUCTURE__"
            "D02_STILL_BLOCKED"
        ),
        "precision_bits": PRECISION,
        "serialized_outer_bits": OUTER_BITS,
        "kappa_isolation": kappa,
        "compact_source_atlas": chart_atlas(),
        "cyclic_seam_ledger": seams,
        "all_four_cyclic_seams_exactly_glued": True,
        "source_grazing_ledger": grazing_ledger(),
        "round161_endpoint_compact_lift": lift,
        "physical_map_pin": {
            "file": ROUND146_PHYSICAL_ENGINE,
            "sha256": ROUND146_PHYSICAL_ENGINE_SHA256,
            "map": (
                "A=asin(t_star)+delta_x/(R_W*sqrt(17)); "
                "Phi=asin(P_star)+4*delta_x/sqrt(17)+delta_beta"
            ),
        },
        "strict_scope": {
            "extends_certified_u_corridor": False,
            "first_global_R1648_face_located": False,
            "disconnected_exterior_sheets_exhausted": False,
            "unresolved_exterior_leaf_count_certified_zero": False,
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "propagate all named R1648 margins from the Round161 E-chart "
            "endpoint in compact coordinates to the first certified face; "
            "then run the four-chart exterior branch-and-bound to zero "
            "unresolved leaves"
        ),
    }
