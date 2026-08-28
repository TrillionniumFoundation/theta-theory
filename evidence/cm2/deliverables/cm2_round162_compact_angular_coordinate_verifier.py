#!/usr/bin/env python3
"""Independent verifier for the Round162 compact angular infrastructure.

The verifier intentionally does not import the Round162 engine or producer.
It pins both sources, strictly parses their certificate, independently
reconstructs the algebraic atlas and the 8192-bit Round161 endpoint lift,
then runs semantic and strict-JSON attacks.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_round161_dyadic_sheared_recentering_engine as r161


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / (
        "cm2_round162_compact_angular_coordinate_infrastructure_"
        "verification_2026_07_25.json"
    )
)
CERTIFICATE = (
    "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json"
)
ENGINE = "cm2_round162_compact_angular_coordinate_engine.py"
PRODUCER = "cm2_round162_compact_angular_coordinate_producer.py"
ROUND161_ENGINE = "cm2_round161_dyadic_sheared_recentering_engine.py"
ROUND161_CERTIFICATE = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-2026-07-25.json"
)
ROUND161_VERIFICATION = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-verification-2026-07-25.json"
)
ROUND146_PHYSICAL_ENGINE = "cm2_round146_physical_centered_jet_2d_engine.py"
PINS = {
    ENGINE:
        "f8ec6e2760ff19c6fdd65689ed134cd925b5c382778699e16e0e2f933ae162ed",
    PRODUCER:
        "c03761fc21765311f41c65b7cda0da2a975c30071372cbcf613dac31e95af36b",
    CERTIFICATE:
        "f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1",
    ROUND161_ENGINE:
        "ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f",
    ROUND161_CERTIFICATE:
        "317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd",
    ROUND161_VERIFICATION:
        "01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db",
    ROUND146_PHYSICAL_ENGINE:
        "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb",
}
CERTIFICATE_SCHEMA = (
    "cm2.round162.compact-angular-coordinate-infrastructure.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round162.compact-angular-coordinate-infrastructure.verification.v1"
)
PRECISION = 8192
OUTER_BITS = 4608
POWER = 4296
ENDPOINT_U = Q(2500000000000000)
KAPPA_BITS = 256
CHART_AXES: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {
    "E": ((1, 0), (0, 1)),
    "N": ((0, 1), (-1, 0)),
    "W": ((-1, 0), (0, -1)),
    "S": ((0, -1), (1, 0)),
}
SEAMS = (
    ("E", 1, "N", -1),
    ("N", 1, "W", -1),
    ("W", 1, "S", -1),
    ("S", 1, "E", -1),
)
TYPED_FACES = {
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


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (
            set(left) == set(right)
            and all(typed_equal(left[key], right[key]) for key in left)
        )
    if type(left) is list:
        return (
            len(left) == len(right)
            and all(typed_equal(a, b) for a, b in zip(left, right))
        )
    return left == right


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(value)

    def reject_float(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "encoding",
    )
    result = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject_float,
    )

    def strings(value: Any) -> None:
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in value
                ),
                "decoded string encoding",
            )
        elif type(value) is list:
            for item in value:
                strings(item)
        elif type(value) is dict:
            for key, item in value.items():
                strings(key)
                strings(item)

    strings(result)
    require(type(result) is dict, "top object")
    return result


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_bytes(path.read_bytes())


def check_source_pins() -> None:
    require(
        Path(r161.__file__).resolve()
        == (HERE / ROUND161_ENGINE).resolve(),
        "Round161 module identity",
    )
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, "pin:" + name)
    require(
        r161.r160.POWER == POWER
        and r161.r160.r150.r139.lower.SOURCE_ABSOLUTE_OWNER == "W[0,0]"
        and r161.r160.r150.r139.lower.R_W == Q(4, 25)
        and r161.r160.r150.r139.lower.SOURCE_P_STAR
        == Q(-1587, 1638400),
        "physical constants",
    )
    r161.check_pins()


def check_round161() -> tuple[dict[str, Any], dict[str, Any]]:
    certificate = strict_load(HERE / ROUND161_CERTIFICATE)
    verification = strict_load(HERE / ROUND161_VERIFICATION)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and type(certificate["schema"]) is str
        and type(certificate["result"]) is dict
        and type(certificate["result_sha256"]) is str
        and certificate["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.v1"
        )
        and certificate["result_sha256"] == digest(certificate["result"])
        and certificate["result_sha256"]
        == "842ef791a414e85b5f2eeb458f876d837d269a284f26ae8317059bd4e0fb2f12",
        "Round161 certificate",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.verification.v1"
        )
        and verification["result_sha256"] == digest(verification["result"])
        and verification["result_sha256"]
        == "5c1a78555644f4fb424e8e164e3088fd24a1d393252a6214d4b8829815571e07"
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == certificate["result_sha256"],
        "Round161 verification",
    )
    prior = certificate["result"]
    require(
        prior["status"]
        == (
            "CERTIFIED_DYADIC_SHEARED_RECENTERING_TO_"
            "2500000000000000H__D02_STILL_BLOCKED"
        )
        and prior["certified_abs_delta_x_corridor_in_h_units"]
        == ["0", "2500000000000000"]
        and typed_equal(
            prior["combined_typed_atlas"],
            {
                "connected": True,
                "interior_untyped_event_cell_count": 0,
                "lower_symmetry_axis_terminal": True,
                "slab_count": 75,
                "typed_box_count": 225,
                "upper_endpoint_in_h_units": "2500000000000000",
                "upper_endpoint_terminal": False,
            },
        )
        and typed_equal(
            prior["strict_nonpromotion"],
            {
                "D02_status": "BLOCKED",
                "D03_authorized": False,
                "global_gate5_maturity": "10/18",
                "global_complete_18_field_block_count": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
        ),
        "Round161 state",
    )
    terminal = prior["new_dyadic_sheared_recentering"]["new_macro_slabs"][-1]
    require(
        typed_equal(
            terminal["coordinate_map"],
            {
                "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
                "slope_s": "1403486916994043/500000000000000",
                "u_definition": "u=abs(delta_x)/h=-delta_x/h",
                "w_definition": "w=delta_beta/h-s*u",
            },
        )
        and terminal["u_in_h_units"]
        == ["100000", "2500000000000000"]
        and typed_equal(
            terminal["w_typed_box_chain"],
            [
                {
                    "kind": "C24_EVENT",
                    "w_in_h_units": ["-430", "-405"],
                },
                {
                    "kind": "STRICT_RETURN_BRIDGE",
                    "w_in_h_units": ["-405", "-350"],
                },
                {
                    "kind": "D3_EVENT",
                    "w_in_h_units": ["-350", "134111000000"],
                },
            ],
        ),
        "Round161 terminal macro",
    )
    return certificate, verification


@dataclass(frozen=True)
class QK:
    a: Q
    b: Q = Q(0)

    @staticmethod
    def coerce(value: QK | Q | int) -> QK:
        return value if isinstance(value, QK) else QK(Q(value))

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
        require(determinant != 0, "Q(kappa) division")
        return QK(
            (self.a - 2 * self.b) / determinant,
            -self.b / determinant,
        )

    def __truediv__(self, other: QK | Q | int) -> QK:
        return self * self.coerce(other).inverse()

    def record(self) -> list[str]:
        return [qstr(self.a), qstr(self.b)]


KAPPA = QK(Q(0), Q(1))


def reconstruct_kappa() -> dict[str, Any]:
    scale = 1 << KAPPA_BITS
    floor_sqrt2 = math.isqrt(1 << (2 * KAPPA_BITS + 1))
    lower = Q(floor_sqrt2 - scale, scale)
    upper = lower + Q(1, scale)
    polynomial = lambda x: x * x + 2 * x - 1
    p0, p1 = polynomial(lower), polynomial(upper)
    require(
        0 < lower < upper < 1
        and p0 < 0 < p1
        and 2 * lower + 2 > 0,
        "independent kappa isolation",
    )
    return {
        "algebraic_definition": "kappa=sqrt(2)-1",
        "minimal_polynomial": "x^2+2*x-1",
        "dyadic_isolating_interval": [qstr(lower), qstr(upper)],
        "isolating_width": qstr(upper - lower),
        "polynomial_at_lower": qstr(p0),
        "polynomial_at_upper": qstr(p1),
        "lower_sign": "NEGATIVE",
        "upper_sign": "POSITIVE",
        "derivative": "2*x+2",
        "derivative_lower_bound": qstr(2 * lower + 2),
        "derivative_strict_positive_on_interval": True,
        "unique_root_in_interval": True,
        "selected_root_in_0_1": True,
        "quotient_relation": "kappa^2=1-2*kappa",
    }


def normal(chart: str, z: QK) -> tuple[QK, QK]:
    axis, quarter = CHART_AXES[chart]
    denominator = QK(1) + z * z
    along = (QK(1) - z * z) / denominator
    across = 2 * z / denominator
    return (
        axis[0] * along + quarter[0] * across,
        axis[1] * along + quarter[1] * across,
    )


def state_template(n: tuple[QK, QK]) -> dict[str, Any]:
    jn = (-n[1], n[0])
    center = QK(Q(1, 2))
    position = (
        center + Q(4, 25) * n[0],
        center + Q(4, 25) * n[1],
    )
    velocity = (
        (n[0], 2 * jn[0], -n[0]),
        (n[1], 2 * jn[1], -n[1]),
    )
    return {
        "coefficient_field": (
            "Q[kappa]/(kappa^2+2*kappa-1); each scalar is [a,b]=a+b*kappa"
        ),
        "normal": [entry.record() for entry in n],
        "quarter_turn_normal": [entry.record() for entry in jn],
        "position": [entry.record() for entry in position],
        "velocity_denominator": "1+q^2",
        "velocity_numerator_coefficients_in_1_q_q2": [
            [entry.record() for entry in row] for row in velocity
        ],
    }


def reconstruct_seams() -> list[dict[str, Any]]:
    result = []
    for left_chart, left_sign, right_chart, right_sign in SEAMS:
        left_n = normal(left_chart, left_sign * KAPPA)
        right_n = normal(right_chart, right_sign * KAPPA)
        require(left_n == right_n, "independent seam normal")
        left = state_template(left_n)
        right = state_template(right_n)
        require(typed_equal(left, right), "independent seam state")
        left_hash, right_hash = digest(left), digest(right)
        require(left_hash == right_hash, "independent seam hash")
        result.append(
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
                "left_physical_state_template": left,
                "right_physical_state_template": right,
                "left_physical_state_sha256": left_hash,
                "right_physical_state_sha256": right_hash,
                "physical_state_digests_equal": True,
                "exact_gluing_for_every_q": True,
            }
        )
    return result


def reconstruct_atlas() -> dict[str, Any]:
    charts = []
    theta = {"E": "0", "N": "pi/2", "W": "pi", "S": "-pi/2"}
    for chart, (axis, quarter) in CHART_AXES.items():
        charts.append(
            {
                "chart": chart,
                "theta": theta[chart],
                "axis": list(axis),
                "quarter_turn_axis": list(quarter),
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


def reconstruct_grazing() -> dict[str, Any]:
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


def fixed_outer(value: arb) -> list[str]:
    return r161.r160.fixed_outer(value, OUTER_BITS)


def reconstruct_endpoint_face(w0: Q, w1: Q) -> dict[str, Any]:
    ctx.prec = PRECISION
    aq = r161.r160.r150.r139.lower.aq
    root = r161.r160.r150.load_seed()[1]
    lower, upper = map(aq, root)
    t_star = (
        (lower + upper) / 2
        + r161.r160.r146.symmetric((upper - lower) / 2)
    )
    h = aq(Q(1, 2**POWER))
    sqrt17 = aq(Q(17)).sqrt()
    radius = aq(Q(4, 25))
    u = aq(ENDPOINT_U)
    wc, wr = (w0 + w1) / 2, (w1 - w0) / 2
    w = aq(wc) + r161.r160.r146.symmetric(aq(wr))
    slope = aq(Q(1403486916994043, 500000000000000))
    angle = t_star.asin() - u * h / (radius * sqrt17)
    phase = (
        aq(Q(-1587, 1638400)).asin()
        + (-4 * u / sqrt17 + slope * u + w) * h
    )
    z = (angle / 2).tan()
    q = (phase / 2).tan()
    isolate_lower = Q(reconstruct_kappa()["dyadic_isolating_interval"][0])
    require(
        bool(z > -aq(isolate_lower))
        and bool(z < aq(isolate_lower))
        and bool(q > -1)
        and bool(q < 1)
        and bool(phase > -1)
        and bool(phase < 1),
        "independent endpoint E chart",
    )
    n = ((1 - z * z) / (1 + z * z), 2 * z / (1 + z * z))
    p = 2 * q / (1 + q * q)
    radial = (1 - q * q) / (1 + q * q)
    jn = (-n[1], n[0])
    rational_state = [
        aq(Q(1, 2)) + radius * n[0],
        aq(Q(1, 2)) + radius * n[1],
        radial * n[0] + p * jn[0],
        radial * n[1] + p * jn[1],
    ]
    direct_n = (angle.cos(), angle.sin())
    direct_p, direct_radial = phase.sin(), phase.cos()
    direct_jn = (-direct_n[1], direct_n[0])
    direct_state = [
        aq(Q(1, 2)) + radius * direct_n[0],
        aq(Q(1, 2)) + radius * direct_n[1],
        direct_radial * direct_n[0] + direct_p * direct_jn[0],
        direct_radial * direct_n[1] + direct_p * direct_jn[1],
    ]
    require(
        all(a.overlaps(b) for a, b in zip(rational_state, direct_state)),
        "independent endpoint state overlap",
    )
    return {
        "chart": "E",
        "u_in_h_units": "2500000000000000",
        "w_in_h_units": [qstr(w0), qstr(w1)],
        "A_outer": fixed_outer(angle),
        "Phi_outer": fixed_outer(phase),
        "z_outer": fixed_outer(z),
        "q_outer": fixed_outer(q),
        "eta_definition": "eta=Phi-Phi0-m*(A-A0)=h*w",
        "eta_exact_enclosure": [
            qstr(Q(w0, 2**POWER)),
            qstr(Q(w1, 2**POWER)),
        ],
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
        "half_angle_and_pinned_physical_state_enclosures_overlap": True,
    }


def reconstruct_lift() -> dict[str, Any]:
    faces = {
        kind: reconstruct_endpoint_face(w0, w1)
        for kind, (w0, w1) in TYPED_FACES.items()
    }
    common = faces["C24_EVENT"]["z_outer"]
    require(
        all(typed_equal(face["z_outer"], common) for face in faces.values())
        and faces["C24_EVENT"]["eta_exact_enclosure"][1]
        == faces["STRICT_RETURN_BRIDGE"]["eta_exact_enclosure"][0]
        and faces["STRICT_RETURN_BRIDGE"]["eta_exact_enclosure"][1]
        == faces["D3_EVENT"]["eta_exact_enclosure"][0],
        "independent endpoint adjacency",
    )
    return {
        "source_round": 161,
        "source_endpoint_u_in_h_units": "2500000000000000",
        "source_slope_s": "1403486916994043/500000000000000",
        "current_source_chart": "E",
        "all_three_faces_strictly_inside_E_chart": True,
        "all_three_faces_strictly_away_from_q_grazing": True,
        "common_z_outer": common,
        "typed_faces": faces,
        "exact_eta_face_adjacencies_preserved": True,
        "this_is_a_coordinate_lift_not_a_new_continuation_slab": True,
    }


def reconstruct_infrastructure() -> dict[str, Any]:
    seams = reconstruct_seams()
    require(len(seams) == 4, "independent four seams")
    return {
        "status": (
            "CERTIFIED_COMPACT_ANGULAR_COORDINATE_INFRASTRUCTURE__"
            "D02_STILL_BLOCKED"
        ),
        "precision_bits": 8192,
        "serialized_outer_bits": 4608,
        "kappa_isolation": reconstruct_kappa(),
        "compact_source_atlas": reconstruct_atlas(),
        "cyclic_seam_ledger": seams,
        "all_four_cyclic_seams_exactly_glued": True,
        "source_grazing_ledger": reconstruct_grazing(),
        "round161_endpoint_compact_lift": reconstruct_lift(),
        "physical_map_pin": {
            "file": ROUND146_PHYSICAL_ENGINE,
            "sha256": PINS[ROUND146_PHYSICAL_ENGINE],
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


def expected_result(
    prior_certificate: dict[str, Any],
    prior_verification: dict[str, Any],
) -> dict[str, Any]:
    infrastructure = reconstruct_infrastructure()
    return {
        "status": infrastructure["status"],
        "inheritance": {
            "round161_certificate": ROUND161_CERTIFICATE,
            "round161_certificate_file_sha256": PINS[ROUND161_CERTIFICATE],
            "round161_certificate_result_sha256":
                prior_certificate["result_sha256"],
            "round161_verification": ROUND161_VERIFICATION,
            "round161_verification_file_sha256": PINS[ROUND161_VERIFICATION],
            "round161_verification_result_sha256":
                prior_verification["result_sha256"],
            "round161_verification_status": "PASS",
            "inherited_certified_abs_delta_x_corridor_in_h_units":
                ["0", "2500000000000000"],
            "inherited_combined_typed_atlas":
                prior_certificate["result"]["combined_typed_atlas"],
        },
        "engine_source": {
            "file": ENGINE,
            "sha256": PINS[ENGINE],
        },
        "compact_angular_coordinate_infrastructure": infrastructure,
        "strict_nonpromotion": {
            "certified_abs_delta_x_corridor_extended": False,
            "combined_typed_atlas_changed": False,
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": infrastructure["next_core_gate"],
    }


def verify_document(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"},
        "certificate wrapper keys",
    )
    require(
        type(document["schema"]) is str
        and type(document["result"]) is dict
        and type(document["result_sha256"]) is str,
        "certificate wrapper types",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate self digest",
    )
    require(
        typed_equal(document["result"], expected),
        "independent typed reconstruction",
    )


def rejection(function: Callable[[], None]) -> bool:
    try:
        function()
    except Exception:
        return True
    return False


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> list[dict[str, Any]]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def add(name: str, mutation: Callable[[dict[str, Any]], None]) -> None:
        attacks.append((name, mutation))

    add(
        "schema_tamper",
        lambda d: d.__setitem__("schema", CERTIFICATE_SCHEMA + ".tampered"),
    )
    add(
        "result_digest_tamper",
        lambda d: d.__setitem__("result_sha256", "0" * 64),
    )

    def seam_tamper(d: dict[str, Any]) -> None:
        seam = d["result"]["compact_angular_coordinate_infrastructure"][
            "cyclic_seam_ledger"
        ][0]
        left = seam["left_physical_state_template"]
        right = seam["right_physical_state_template"]
        left["normal"][0][0] = "1"
        right["normal"][0][0] = "1"
        seam["left_physical_state_sha256"] = digest(left)
        seam["right_physical_state_sha256"] = digest(right)
        d["result_sha256"] = digest(d["result"])

    add("coherent_two_sided_seam_tamper", seam_tamper)

    def seam_reorder(d: dict[str, Any]) -> None:
        ledger = d["result"]["compact_angular_coordinate_infrastructure"][
            "cyclic_seam_ledger"
        ]
        ledger[0], ledger[1] = ledger[1], ledger[0]
        d["result_sha256"] = digest(d["result"])

    add("cyclic_seam_reorder", seam_reorder)

    def kappa_tamper(d: dict[str, Any]) -> None:
        kappa = d["result"]["compact_angular_coordinate_infrastructure"][
            "kappa_isolation"
        ]
        kappa["dyadic_isolating_interval"][0] = "0"
        kappa["polynomial_at_lower"] = "-1"
        d["result_sha256"] = digest(d["result"])

    add("coherent_kappa_bracket_tamper", kappa_tamper)

    def grazing_tamper(d: dict[str, Any]) -> None:
        grazing = d["result"]["compact_angular_coordinate_infrastructure"][
            "source_grazing_ledger"
        ]
        grazing["q_plus_one"]["radial"] = "1"
        d["result_sha256"] = digest(d["result"])

    add("q_grazing_stratum_tamper", grazing_tamper)

    def endpoint_chart(d: dict[str, Any]) -> None:
        lift = d["result"]["compact_angular_coordinate_infrastructure"][
            "round161_endpoint_compact_lift"
        ]
        lift["current_source_chart"] = "N"
        for face in lift["typed_faces"].values():
            face["chart"] = "N"
        d["result_sha256"] = digest(d["result"])

    add("coherent_endpoint_chart_tamper", endpoint_chart)

    def adjacency_tamper(d: dict[str, Any]) -> None:
        faces = d["result"]["compact_angular_coordinate_infrastructure"][
            "round161_endpoint_compact_lift"
        ]["typed_faces"]
        faces["STRICT_RETURN_BRIDGE"]["eta_exact_enclosure"][0] = "0"
        d["result_sha256"] = digest(d["result"])

    add("endpoint_eta_adjacency_tamper", adjacency_tamper)

    def endpoint_q_tamper(d: dict[str, Any]) -> None:
        face = d["result"]["compact_angular_coordinate_infrastructure"][
            "round161_endpoint_compact_lift"
        ]["typed_faces"]["D3_EVENT"]
        face["q_outer"] = ["-1", "1"]
        d["result_sha256"] = digest(d["result"])

    add("endpoint_q_outer_tamper", endpoint_q_tamper)

    def inheritance_tamper(d: dict[str, Any]) -> None:
        d["result"]["inheritance"]["round161_certificate_result_sha256"] = (
            "f" * 64
        )
        d["result_sha256"] = digest(d["result"])

    add("inheritance_result_pin_tamper", inheritance_tamper)

    def nonpromotion_tamper(d: dict[str, Any]) -> None:
        d["result"]["strict_nonpromotion"]["D02_status"] = "READY"
        d["result_sha256"] = digest(d["result"])

    add("nonpromotion_D02_tamper", nonpromotion_tamper)

    def bool_int_tamper(d: dict[str, Any]) -> None:
        d["result"]["compact_angular_coordinate_infrastructure"][
            "all_four_cyclic_seams_exactly_glued"
        ] = 1
        d["result_sha256"] = digest(d["result"])

    add("bool_as_int_type_confusion", bool_int_tamper)

    def int_bool_tamper(d: dict[str, Any]) -> None:
        d["result"]["compact_angular_coordinate_infrastructure"][
            "precision_bits"
        ] = True
        d["result_sha256"] = digest(d["result"])

    add("int_as_bool_type_confusion", int_bool_tamper)

    def atlas_count_tamper(d: dict[str, Any]) -> None:
        d["result"]["inheritance"]["inherited_combined_typed_atlas"][
            "typed_box_count"
        ] = 226
        d["result_sha256"] = digest(d["result"])

    add("inherited_atlas_count_tamper", atlas_count_tamper)

    result = []
    for name, mutate in attacks:
        attacked = copy.deepcopy(document)
        mutate(attacked)
        rejected = rejection(lambda: verify_document(attacked, expected))
        require(rejected, "semantic attack accepted:" + name)
        result.append({"attack": name, "rejected": True})
    return result


def strict_json_attacks(raw: bytes) -> list[dict[str, Any]]:
    text = raw.decode("utf-8")
    attacks: list[tuple[str, bytes]] = [
        (
            "floating_point_token",
            text.replace(
                '"precision_bits":8192',
                '"precision_bits":8192.0',
                1,
            ).encode("utf-8"),
        ),
        (
            "duplicate_key",
            text.replace(
                '{"result":',
                '{"schema":"duplicate","result":',
                1,
            ).encode("utf-8"),
        ),
        ("UTF8_BOM", b"\xef\xbb\xbf" + raw),
        ("raw_NUL", raw[:-2] + b"\x00}\n"),
        (
            "escaped_NUL",
            text.replace(
                '"schema":"',
                '"schema":"\\u0000',
                1,
            ).encode("utf-8"),
        ),
        (
            "unicode_surrogate",
            text.replace(
                '"schema":"',
                '"schema":"\\ud800',
                1,
            ).encode("utf-8"),
        ),
        (
            "NaN_constant",
            text.replace(
                '"precision_bits":8192',
                '"precision_bits":NaN',
                1,
            ).encode("utf-8"),
        ),
    ]
    result = []
    for name, attacked in attacks:
        rejected = rejection(lambda data=attacked: strict_load_bytes(data))
        require(rejected, "strict JSON attack accepted:" + name)
        result.append({"attack": name, "rejected": True})
    return result


def build_verification() -> dict[str, Any]:
    check_source_pins()
    prior_certificate, prior_verification = check_round161()
    raw = (HERE / CERTIFICATE).read_bytes()
    document = strict_load_bytes(raw)
    expected = expected_result(prior_certificate, prior_verification)
    verify_document(document, expected)
    semantic = semantic_attacks(document, expected)
    strict = strict_json_attacks(raw)
    return {
        "status": "PASS",
        "certificate": CERTIFICATE,
        "certificate_file_sha256": PINS[CERTIFICATE],
        "certificate_result_sha256": document["result_sha256"],
        "independent_reconstruction": {
            "does_not_import_round162_engine_or_producer": True,
            "kappa_polynomial_isolation_reconstructed": True,
            "four_Q_kappa_cyclic_seams_reconstructed": True,
            "four_physical_state_digest_equalities_reconstructed": True,
            "q_plus_minus_one_grazing_strata_reconstructed": True,
            "round161_endpoint_E_chart_lift_recomputed_at_8192_bits": True,
            "endpoint_eta_face_adjacencies_reconstructed": True,
            "half_angle_and_pinned_physical_state_overlap_recomputed": True,
            "inheritance_and_nonpromotion_reconstructed": True,
            "full_result_type_sensitive_equal": True,
        },
        "pins": {
            name: value for name, value in sorted(PINS.items())
        },
        "semantic_attacks": semantic,
        "semantic_attack_rejection_count": len(semantic),
        "strict_json_attacks": strict,
        "strict_json_attack_rejection_count": len(strict),
        "strict_JSON_type_sensitive": True,
        "bool_int_type_confusion_rejected": True,
        "float_tokens_rejected": True,
        "duplicate_keys_rejected": True,
        "BOM_NUL_and_surrogate_rejected": True,
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = build_verification()
    document = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    arguments.output.write_text(
        canonical(document) + "\n",
        encoding="utf-8",
    )
    print(canonical(document))


if __name__ == "__main__":
    main()
