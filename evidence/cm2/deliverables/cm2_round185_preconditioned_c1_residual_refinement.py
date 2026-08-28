#!/usr/bin/env python3
"""Round185 preconditioned C0/C1 refinement of the Round183 residual.

Every Round183 dynamic residual box and inherited collision1/source carrier
is processed.  Dynamic boxes receive one bounded dyadic split followed by a
centered mean-value discriminant/outgoing-chart classification.  The
remaining graph outers receive full-box automatic-differentiation evidence.

Regularity and existence are deliberately separate.  A nonzero derivative,
or a nonsingular dyadic oblique preconditioner, never certifies that a zero
set is nonempty.  Nonemptiness requires an independent strict boundary
bracket or an interval-Newton self-map.  No lower-dimensional carrier earns
ambient or whole-parent credit.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import stat
import tempfile
from typing import Any

from flint import arb
import flint

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas
import cm2_gate3_ge_interval_atlas_cert as ge
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as registry
import cm2_round178_later_return_exact_key_bridge as r178
import cm2_round181_parametric_collision2_graph_arrangement as r181
import cm2_round183_residual_face_bracket_refinement as r183


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round185_preconditioned_c1_residual_refinement_certificate.json"
SCHEMA = "cm2.round185.preconditioned-c1-residual-refinement.v1"
MAX_INPUT_BYTES = 160 * 1024 * 1024
R183_PRODUCER = "cm2_round183_residual_face_bracket_refinement.py"
R183_CERT = "cm2_round183_residual_face_bracket_refinement_certificate.json"
R183_VERIFIER = "cm2_round183_residual_face_bracket_refinement_verifier.py"
R183_VERIFICATION = "cm2_round183_residual_face_bracket_refinement_verification.json"
R183_REPORT = "cm2_round183_residual_face_bracket_refinement_report.md"
R183_COLD = "cm2_round183_residual_face_bracket_refinement_cold_replay.md"
R183_MANIFEST = "cm2_round183_residual_face_bracket_refinement_manifest.sha256"
PINS = {
    R183_PRODUCER:
        "ac0e786146df08e1c8695bd9a1cfdbe0bed290d2fd77960f61ffa9e0785133ed",
    R183_CERT:
        "5863d5e7e564d3f6c145cbb2a2e7286f495fce73a40bdc8e11a47f20fd4ff74b",
    R183_VERIFIER:
        "4127372e9ebf58130d8b42bfc31ea82fde532c9637290ba978799215b62780a2",
    R183_VERIFICATION:
        "58f5dacbab0e63185f04f63ad4fa87bf99ae12bab94da59810ad71da44773801",
    R183_REPORT:
        "32347a9782ea5a13a64651bc87d81020b138879026eecbe174567798a37ee93d",
    R183_COLD:
        "fbd32a069da34c16770f6aedb09540ec4b27f434904dae6d6079060c67c2846f",
    R183_MANIFEST:
        "8c34040f0ccc1229b9d68a9377c28adaf3b5639d9bb73485c7d58b0910c3a005",
}
R183_RESULT = "f37eb4f1321ef837a2d67dbfaf7d3816dc320b81d31e151422eb9b649d5a5f53"
R183_VERIFICATION_RESULT = (
    "40beacf08c2168f602c683b1e3b49d91411e90da3dc04ea42e27d95e922cbcf7"
)
DYNAMIC_EXTRA_DEPTH = 1
INHERITED_EXTRA_DEPTH = 1
PRIORITY = {
    "OUTGOING_H2": 0,
    "ACTIVE_DELTA_1": 1,
    "ACTIVE_DELTA_2": 2,
    "POINT_WINNER_NONSTRICT": 3,
}
CANDIDATES = r181.CANDIDATES
BASE = r178.base


class Round185Error(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round185Error(label)


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["row_sha256"] = digest(result)
    return result


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise Round185Error(f"noninteger number:{value}")


def read_regular(path: Path, expected: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"hardlink:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
            f"encoding:{label}")
    value = json.loads(raw.decode("utf-8", "strict"),
                       object_pairs_hook=unique_pairs,
                       parse_float=reject_number,
                       parse_constant=reject_number)
    require(type(value) is dict, f"top:{label}")
    return value


def load_chain() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(flint.__version__ == "0.9.0" and atlas.ctx.prec == 384, "flint")
    require(Path(r183.__file__).resolve() == (HERE / R183_PRODUCER).resolve(),
            "Round183 module")
    for name, expected in PINS.items():
        read_regular(HERE / name, expected)
    certificate = strict_json(
        read_regular(HERE / R183_CERT, PINS[R183_CERT]), R183_CERT
    )
    verification = strict_json(
        read_regular(HERE / R183_VERIFICATION, PINS[R183_VERIFICATION]),
        R183_VERIFICATION,
    )
    require(
        certificate["result_sha256"] == R183_RESULT
        and certificate["result_sha256"] == digest(certificate["result"]),
        "Round183 result",
    )
    require(
        verification["result_sha256"] == R183_VERIFICATION_RESULT
        and verification["result_sha256"] == digest(verification["result"])
        and verification["result"]["status"] == "PASS"
        and verification["result"]["full_expected_result_canonical_equality"],
        "Round183 verification",
    )
    upstream181, upstream178 = r183.load_chain()
    return certificate["result"], upstream181, upstream178


def volume(box: atlas.AtlasBox) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def box_payload(box: atlas.AtlasBox) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "volume": str(volume(box)),
    }


def box_from_payload(payload: dict[str, Any], path: str) -> atlas.AtlasBox:
    return atlas.AtlasBox(
        Q(payload["t"][0]), Q(payload["t"][1]),
        Q(payload["p"][0]), Q(payload["p"][1]),
        Q(payload["s"][0]), Q(payload["s"][1]),
        0, path,
    )


def point_box(box: atlas.AtlasBox, t: Q, p: Q, s: Q,
              suffix: str) -> atlas.AtlasBox:
    return atlas.AtlasBox(t, t, p, p, s, s, box.depth,
                          box.path + suffix)


def fixed_axis_box(box: atlas.AtlasBox, axis: int,
                   value: Q, suffix: str) -> atlas.AtlasBox:
    bounds = [
        [box.t0, box.t1],
        [box.p0, box.p1],
        [box.s0, box.s1],
    ]
    bounds[axis] = [value, value]
    return atlas.AtlasBox(
        bounds[0][0], bounds[0][1],
        bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1],
        box.depth, box.path + suffix,
    )


def arb_bounds(value: arb) -> dict[str, Any]:
    return {
        "lower": str(value.lower()),
        "upper": str(value.upper()),
        "contains_zero": bool(value.contains(0)),
    }


def strict_sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def sign_name(value: int) -> str:
    return "POSITIVE" if value > 0 else "NEGATIVE" if value < 0 else "UNRESOLVED"


@dataclass(frozen=True)
class AD3:
    value: arb
    derivative: tuple[arb, arb, arb]

    def __add__(self, other: Any) -> "AD3":
        right = ad_constant(other)
        return AD3(
            self.value + right.value,
            tuple(a + b for a, b in zip(self.derivative, right.derivative)),
        )

    __radd__ = __add__

    def __neg__(self) -> "AD3":
        return AD3(-self.value, tuple(-value for value in self.derivative))

    def __sub__(self, other: Any) -> "AD3":
        return self + (-ad_constant(other))

    def __rsub__(self, other: Any) -> "AD3":
        return ad_constant(other) - self

    def __mul__(self, other: Any) -> "AD3":
        right = ad_constant(other)
        return AD3(
            self.value * right.value,
            tuple(
                left_d * right.value + self.value * right_d
                for left_d, right_d in zip(
                    self.derivative, right.derivative
                )
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "AD3":
        right = ad_constant(other)
        denominator = right.value * right.value
        return AD3(
            self.value / right.value,
            tuple(
                (left_d * right.value - self.value * right_d) / denominator
                for left_d, right_d in zip(
                    self.derivative, right.derivative
                )
            ),
        )

    def sqrt(self) -> "AD3":
        require(bool(self.value > 0), "AD sqrt domain")
        root = self.value.sqrt()
        return AD3(
            root,
            tuple(value / (2 * root) for value in self.derivative),
        )


def ad_constant(value: Any) -> AD3:
    if isinstance(value, AD3):
        return value
    enclosed = value if isinstance(value, arb) else BASE.arbq(Q(value))
    return AD3(enclosed, (arb(0), arb(0), arb(0)))


def ad_variables(box: atlas.AtlasBox) -> tuple[AD3, AD3, AD3]:
    values = (
        BASE.arb_interval(box.t0, box.t1),
        BASE.arb_interval(box.p0, box.p1),
        BASE.arb_interval(box.s0, box.s1),
    )
    result = []
    for index, value in enumerate(values):
        result.append(AD3(
            value,
            tuple(arb(1) if index == axis else arb(0)
                  for axis in range(3)),
        ))
    return tuple(result)  # type: ignore[return-value]


def ad_target_center(identifier: str, s: AD3) -> tuple[AD3, AD3]:
    obstacle, x, y = r178.parse_target(identifier)
    if obstacle == "G":
        return ad_constant(x), ad_constant(y)
    return (
        ad_constant(x) + ad_constant(Q(1, 2)) + s,
        ad_constant(y) + ad_constant(Q(1, 2)),
    )


def ad_root(
    geometry: tuple[AD3, AD3, AD3, AD3, AD3],
    identifier: str,
) -> dict[str, AD3]:
    qx, qy, ux, uy, s = geometry
    ax, ay = ad_target_center(identifier, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = ad_constant(r178.RADIUS[identifier[0]])
    delta = radius * radius - transverse * transverse
    return {
        "ell": ell,
        "transverse": transverse,
        "radius": radius,
        "Delta": delta,
    }


def ad_collision(
    geometry: tuple[AD3, AD3, AD3, AD3, AD3],
    identifier: str,
) -> tuple[tuple[AD3, AD3, AD3, AD3, AD3], AD3, AD3]:
    raw = ad_root(geometry, identifier)
    radical = raw["Delta"].sqrt()
    qx, qy, ux, uy, s = geometry
    radius = raw["radius"]
    transverse = raw["transverse"]
    nx = (-radical * ux + transverse * uy) / radius
    ny = (-radical * uy - transverse * ux) / radius
    tangential = transverse / radius
    cosine = radical / radius
    ax, ay = ad_target_center(identifier, s)
    return (
        (
            ax + radius * nx,
            ay + radius * ny,
            cosine * nx - tangential * ny,
            cosine * ny + tangential * nx,
            s,
        ),
        nx,
        ny,
    )


def ad_initial_geometry_from_variables(
    parent_key: str, t: AD3, p: AD3, s: AD3
) -> tuple[AD3, AD3, AD3, AD3, AD3]:
    source, cell = parent_key.split(":")[:2]
    radical_n = (ad_constant(1) - t * t).sqrt()
    radical_p = (ad_constant(1) - p * p).sqrt()
    if cell == "E":
        nx, ny = radical_n, t
    elif cell == "W":
        nx, ny = -radical_n, t
    elif cell == "N":
        nx, ny = t, radical_n
    elif cell == "S":
        nx, ny = t, -radical_n
    else:  # pragma: no cover - finite pinned chart set
        raise Round185Error(f"source chart:{cell}")
    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    if source == "G":
        cx, cy = ad_constant(0), ad_constant(0)
    else:
        cx, cy = ad_constant(Q(1, 2)) + s, ad_constant(Q(1, 2))
    radius = ad_constant(r178.RADIUS[source])
    return cx + radius * nx, cy + radius * ny, ux, uy, s


def ad_initial_geometry(
    parent_key: str, box: atlas.AtlasBox
) -> tuple[AD3, AD3, AD3, AD3, AD3]:
    return ad_initial_geometry_from_variables(
        parent_key, *ad_variables(box)
    )


def collision1_ad(
    parent_key: str, box: atlas.AtlasBox
) -> tuple[AD3, AD3, AD3, AD3, AD3]:
    geometry, _nx, _ny = ad_collision(
        ad_initial_geometry(parent_key, box), r178.COLLISION1_OWNER
    )
    return geometry


def delta_ad(parent_key: str, box: atlas.AtlasBox,
             identifier: str) -> AD3:
    return ad_root(collision1_ad(parent_key, box), identifier)["Delta"]


def collision0_delta_ad(parent_key: str, box: atlas.AtlasBox,
                        identifier: str) -> AD3:
    return ad_root(ad_initial_geometry(parent_key, box), identifier)["Delta"]


def source_h0_ad(
    parent_key: str, box: atlas.AtlasBox, _identifier: str
) -> tuple[AD3, AD3, AD3]:
    t, _p, _s = ad_variables(box)
    _source, cell = parent_key.split(":")[:2]
    radical = (ad_constant(1) - t * t).sqrt()
    if cell == "E":
        nx, ny = radical, t
    elif cell == "W":
        nx, ny = -radical, t
    elif cell == "N":
        nx, ny = t, radical
    elif cell == "S":
        nx, ny = t, -radical
    else:  # pragma: no cover
        raise Round185Error(f"source chart:{cell}")
    return nx * nx - ny * ny, nx, ny


def collision1_h1_ad(
    parent_key: str, box: atlas.AtlasBox, _identifier: str
) -> tuple[AD3, AD3, AD3]:
    _geometry, nx, ny = ad_collision(
        ad_initial_geometry(parent_key, box), r178.COLLISION1_OWNER
    )
    return nx * nx - ny * ny, nx, ny


def outgoing_h2_ad(
    parent_key: str, box: atlas.AtlasBox, identifier: str
) -> tuple[AD3, AD3, AD3]:
    _geometry, nx, ny = ad_collision(
        collision1_ad(parent_key, box), identifier
    )
    return nx * nx - ny * ny, nx, ny


def outgoing_hplus_ad(
    parent_key: str, box: atlas.AtlasBox, identifier: str
) -> tuple[AD3, AD3, AD3]:
    _geometry, nx, ny = ad_collision(
        collision1_ad(parent_key, box), identifier
    )
    return nx + ny, nx, ny


def outgoing_hminus_ad(
    parent_key: str, box: atlas.AtlasBox, identifier: str
) -> tuple[AD3, AD3, AD3]:
    _geometry, nx, ny = ad_collision(
        collision1_ad(parent_key, box), identifier
    )
    return nx - ny, nx, ny


OBLIQUE_AXES = ((1, 1), (1, -1))


def oblique_inner_cell(
    box: atlas.AtlasBox, a: int, b: int
) -> dict[str, Q]:
    determinant = Q(a * a + b * b)
    rt = (box.t1 - box.t0) / 2
    rp = (box.p1 - box.p0) / 2
    denominator = Q(abs(a) + abs(b))
    half = min(determinant * rt / denominator,
               determinant * rp / denominator)
    tc = (box.t0 + box.t1) / 2
    pc = (box.p0 + box.p1) / 2
    uc = a * tc + b * pc
    vc = -b * tc + a * pc
    require(half > 0, "oblique half width")
    return {
        "u0": uc - half, "u1": uc + half,
        "v0": vc - half, "v1": vc + half,
        "s0": box.s0, "s1": box.s1,
        "determinant": determinant,
        "relative_tp_area":
            half * half / (determinant * rt * rp),
    }


def oblique_h2_ad(
    parent_key: str,
    cell: dict[str, Q],
    a: int,
    b: int,
    identifier: str,
) -> tuple[AD3, AD3, AD3]:
    values = (
        BASE.arb_interval(cell["u0"], cell["u1"]),
        BASE.arb_interval(cell["v0"], cell["v1"]),
        BASE.arb_interval(cell["s0"], cell["s1"]),
    )
    variables = []
    for index, value in enumerate(values):
        variables.append(AD3(
            value,
            tuple(arb(1) if index == axis else arb(0)
                  for axis in range(3)),
        ))
    u, v, s = variables
    determinant = ad_constant(a * a + b * b)
    t = (a * u - b * v) / determinant
    p = (b * u + a * v) / determinant
    first, _nx1, _ny1 = ad_collision(
        ad_initial_geometry_from_variables(parent_key, t, p, s),
        r178.COLLISION1_OWNER,
    )
    _second, nx, ny = ad_collision(first, identifier)
    return nx * nx - ny * ny, nx, ny


def fixed_oblique_axis_cell(
    cell: dict[str, Q], axis: int, value: Q
) -> dict[str, Q]:
    result = dict(cell)
    names = (("u0", "u1"), ("v0", "v1"), ("s0", "s1"))
    result[names[axis][0]] = value
    result[names[axis][1]] = value
    return result


def oblique_axis_probe(
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
    a: int,
    b: int,
) -> dict[str, Any]:
    cell = oblique_inner_cell(box, a, b)
    full, _nx, _ny = oblique_h2_ad(
        parent_key, cell, a, b, identifier
    )
    du = full.derivative[0]
    low = oblique_h2_ad(
        parent_key,
        fixed_oblique_axis_cell(cell, 0, cell["u0"]),
        a, b, identifier,
    )[0].value
    high = oblique_h2_ad(
        parent_key,
        fixed_oblique_axis_cell(cell, 0, cell["u1"]),
        a, b, identifier,
    )[0].value
    face_bracket = strict_sign(low) * strict_sign(high) < 0
    midpoint = (cell["u0"] + cell["u1"]) / 2
    if strict_sign(du) != 0:
        middle = oblique_h2_ad(
            parent_key,
            fixed_oblique_axis_cell(cell, 0, midpoint),
            a, b, identifier,
        )[0].value
        image = BASE.arbq(midpoint) - middle / du
        self_map = (
            bool(image > BASE.arbq(cell["u0"]))
            and bool(image < BASE.arbq(cell["u1"]))
        )
        image_bounds: dict[str, Any] | None = arb_bounds(image)
    else:
        self_map = False
        image_bounds = None
    return {
        "axis": [a, b],
        "exact_determinant": a * a + b * b,
        "inner_cell_relative_tp_area": str(cell["relative_tp_area"]),
        "strict_u_derivative": strict_sign(du) != 0,
        "u_derivative": arb_bounds(du),
        "strict_opposite_sign_u_faces": face_bracket,
        "strict_interval_Newton_u_self_map": self_map,
        "Newton_image": image_bounds,
        "scope":
            "certifies only the centered inscribed oblique cell, not the "
            "remainder of the source rectangle",
    }


def centered_enclosure(
    function: Any,
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
    full: AD3,
) -> arb:
    center = (
        (box.t0 + box.t1) / 2,
        (box.p0 + box.p1) / 2,
        (box.s0 + box.s1) / 2,
    )
    center_box = point_box(box, *center, ".centered-C0")
    center_value = function(parent_key, center_box, identifier)
    if isinstance(center_value, tuple):
        center_value = center_value[0]
    enclosure = center_value.value
    widths = (
        (box.t1 - box.t0) / 2,
        (box.p1 - box.p0) / 2,
        (box.s1 - box.s0) / 2,
    )
    for derivative, width in zip(full.derivative, widths):
        displacement = BASE.arb_interval(-width, width)
        enclosure += derivative * displacement
    return enclosure


def corner_signs(
    function: Any,
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
) -> list[tuple[tuple[Q, Q, Q], int]]:
    result = []
    for coordinates in itertools.product(
        (box.t0, box.t1), (box.p0, box.p1), (box.s0, box.s1)
    ):
        point = point_box(box, *coordinates, ".corner")
        value = function(parent_key, point, identifier)
        if isinstance(value, tuple):
            value = value[0]
        result.append((coordinates, strict_sign(value.value)))
    return result


def strict_boundary_bracket(
    signed: list[tuple[tuple[Q, Q, Q], int]]
) -> dict[str, Any] | None:
    for left_index, left in enumerate(signed):
        for right in signed[left_index + 1:]:
            if left[1] * right[1] >= 0:
                continue
            negative = left if left[1] < 0 else right
            positive = left if left[1] > 0 else right
            differing = sum(a != b for a, b in zip(left[0], right[0]))
            return {
                "negative_point": {
                    "t": str(negative[0][0]),
                    "p": str(negative[0][1]),
                    "s": str(negative[0][2]),
                },
                "positive_point": {
                    "t": str(positive[0][0]),
                    "p": str(positive[0][1]),
                    "s": str(positive[0][2]),
                },
                "segment_kind":
                    "BOX_EDGE" if differing == 1 else "BOX_DIAGONAL",
            }
    return None


def axis_newton_record(
    function: Any,
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
    full: AD3,
    axis: int,
) -> dict[str, Any]:
    lower, upper = (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )[axis]
    midpoint = (lower + upper) / 2
    derivative = full.derivative[axis]
    derivative_sign = strict_sign(derivative)
    if derivative_sign == 0:
        return {
            "axis": ("t", "p", "s")[axis],
            "strict_derivative": False,
            "strict_interior_self_map": False,
            "image": None,
        }
    face = fixed_axis_box(box, axis, midpoint, ".newton-mid")
    center_value = function(parent_key, face, identifier)
    if isinstance(center_value, tuple):
        center_value = center_value[0]
    image = BASE.arbq(midpoint) - center_value.value / derivative
    self_map = bool(image > BASE.arbq(lower)) and bool(
        image < BASE.arbq(upper)
    )
    return {
        "axis": ("t", "p", "s")[axis],
        "strict_derivative": True,
        "strict_interior_self_map": self_map,
        "image": arb_bounds(image),
    }


def full_axis_face_bracket(
    function: Any,
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
    axis: int,
) -> bool:
    lower, upper = (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )[axis]
    low_value = function(
        parent_key,
        fixed_axis_box(box, axis, lower, ".face-low"),
        identifier,
    )
    high_value = function(
        parent_key,
        fixed_axis_box(box, axis, upper, ".face-high"),
        identifier,
    )
    if isinstance(low_value, tuple):
        low_value = low_value[0]
    if isinstance(high_value, tuple):
        high_value = high_value[0]
    return strict_sign(low_value.value) * strict_sign(high_value.value) < 0


def dyadic_preconditioner(full: AD3) -> dict[str, Any]:
    dt_sign = strict_sign(full.derivative[0])
    dp_sign = strict_sign(full.derivative[1])
    if dt_sign == 0 and dp_sign == 0:
        return {
            "available": False,
            "reason": "neither source-(t,p) derivative is strict",
        }
    a = dt_sign if dt_sign != 0 else 0
    b = dp_sign if dp_sign != 0 else 0
    determinant = a * a + b * b
    numerator = a * full.derivative[0] + b * full.derivative[1]
    directional = numerator / determinant
    require(determinant > 0, "preconditioner determinant")
    return {
        "available": True,
        "coordinate_map": {
            "u": f"{a}*t+{b}*p",
            "v": f"{-b}*t+{a}*p",
            "a": a,
            "b": b,
            "exact_determinant": determinant,
        },
        "inverse_u_direction_derivative": arb_bounds(directional),
        "strict_u_regularity": strict_sign(directional) != 0,
        "scope":
            "regularity only; the transformed parallelogram still needs "
            "an independent u-face bracket or interval-Newton self-map",
    }


def surface_evidence(
    kind: str,
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
    include_axis_tests: bool = False,
) -> dict[str, Any]:
    if kind == "H2":
        function = outgoing_h2_ad
        full, nx, ny = outgoing_h2_ad(parent_key, box, identifier)
        normal_bounds = {"nx": arb_bounds(nx.value), "ny": arb_bounds(ny.value)}
        normal_signs = {
            "nx": sign_name(strict_sign(nx.value)),
            "ny": sign_name(strict_sign(ny.value)),
        }
        equation = "H2=n2_x^2-n2_y^2"
    elif kind == "HPLUS":
        function = outgoing_hplus_ad
        full, nx, ny = outgoing_hplus_ad(parent_key, box, identifier)
        normal_bounds = {"nx": arb_bounds(nx.value), "ny": arb_bounds(ny.value)}
        normal_signs = {
            "nx": sign_name(strict_sign(nx.value)),
            "ny": sign_name(strict_sign(ny.value)),
        }
        equation = "h_plus=n2_x+n2_y"
    elif kind == "HMINUS":
        function = outgoing_hminus_ad
        full, nx, ny = outgoing_hminus_ad(parent_key, box, identifier)
        normal_bounds = {"nx": arb_bounds(nx.value), "ny": arb_bounds(ny.value)}
        normal_signs = {
            "nx": sign_name(strict_sign(nx.value)),
            "ny": sign_name(strict_sign(ny.value)),
        }
        equation = "h_minus=n2_x-n2_y"
    elif kind == "H1":
        function = collision1_h1_ad
        full, nx, ny = collision1_h1_ad(parent_key, box, identifier)
        normal_bounds = {"nx": arb_bounds(nx.value), "ny": arb_bounds(ny.value)}
        normal_signs = {
            "nx": sign_name(strict_sign(nx.value)),
            "ny": sign_name(strict_sign(ny.value)),
        }
        equation = "H1=n1_x^2-n1_y^2"
    elif kind == "H0":
        function = source_h0_ad
        full, nx, ny = source_h0_ad(parent_key, box, identifier)
        normal_bounds = {"nx": arb_bounds(nx.value), "ny": arb_bounds(ny.value)}
        normal_signs = {
            "nx": sign_name(strict_sign(nx.value)),
            "ny": sign_name(strict_sign(ny.value)),
        }
        equation = "H0=n0_x^2-n0_y^2"
    elif kind == "DELTA0":
        function = collision0_delta_ad
        full = collision0_delta_ad(parent_key, box, identifier)
        normal_bounds = None
        normal_signs = None
        equation = f"collision1_Delta_{identifier}=0"
    else:
        function = delta_ad
        full = delta_ad(parent_key, box, identifier)
        normal_bounds = None
        normal_signs = None
        equation = f"Delta_{identifier}=0"
    centered = centered_enclosure(
        function, parent_key, box, identifier, full
    )
    signed = corner_signs(function, parent_key, box, identifier)
    bracket = strict_boundary_bracket(signed)
    newton = []
    face_brackets = []
    if include_axis_tests:
        newton = [
            axis_newton_record(
                function, parent_key, box, identifier, full, axis
            )
            for axis in range(3)
        ]
        face_brackets = [
            full_axis_face_bracket(
                function, parent_key, box, identifier, axis
            )
            for axis in range(3)
        ]
    derivative_bounds = {
        axis: arb_bounds(value)
        for axis, value in zip(("dt", "dp", "ds"), full.derivative)
    }
    regular = any(
        not record["contains_zero"] for record in derivative_bounds.values()
    )
    newton_exists = any(
        row["strict_interior_self_map"] for row in newton
    )
    face_exists = any(face_brackets)
    return {
        "kind": kind,
        "identifier": identifier,
        "equation": equation,
        "direct_C0_enclosure": arb_bounds(full.value),
        "centered_mean_value_C0_enclosure": arb_bounds(centered),
        "centered_C0_sign": sign_name(strict_sign(centered)),
        "full_box_C1_derivatives": derivative_bounds,
        "regular_if_present": regular,
        "strict_corner_segment_bracket": bracket,
        "independently_certified_nonempty":
            bracket is not None or newton_exists or face_exists,
        "axis_full_face_brackets_t_p_s": face_brackets,
        "axis_interval_Newton": newton,
        "dyadic_oblique_preconditioner": dyadic_preconditioner(full),
        "normal_component_bounds": normal_bounds,
        "normal_component_signs": normal_signs,
        "regularity_is_not_existence": True,
    }


def compact_surface_summary(record: dict[str, Any]) -> dict[str, Any]:
    derivatives = record["full_box_C1_derivatives"]
    return {
        "kind": record["kind"],
        "identifier": record["identifier"],
        "centered_C0_sign": record["centered_C0_sign"],
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp", "ds")
            if not derivatives[axis]["contains_zero"]
        ],
        "strict_corner_segment_bracket":
            record["strict_corner_segment_bracket"] is not None,
        "independently_certified_nonempty":
            record["independently_certified_nonempty"],
        "dyadic_oblique_preconditioner_available":
            record["dyadic_oblique_preconditioner"]["available"],
        "evidence_sha256": digest(record),
    }


def h2_exact_from_centered(
    detail: dict[str, Any],
    evidence_rows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    by_kind = {row["kind"]: row for row in evidence_rows}
    evidence = by_kind["H2"]
    sign = evidence["centered_C0_sign"]
    factor_resolution = False
    if sign == "UNRESOLVED":
        plus = by_kind["HPLUS"]["centered_C0_sign"]
        minus = by_kind["HMINUS"]["centered_C0_sign"]
        factor_sign = {
            "POSITIVE": 1,
            "NEGATIVE": -1,
            "UNRESOLVED": 0,
        }
        product = factor_sign[plus] * factor_sign[minus]
        if product != 0:
            sign = "POSITIVE" if product > 0 else "NEGATIVE"
            factor_resolution = True
    normal = evidence["normal_component_bounds"]
    normal_signs = evidence["normal_component_signs"]
    assert normal is not None
    assert normal_signs is not None
    if sign == "POSITIVE":
        if not normal["nx"]["contains_zero"]:
            chart = "E" if normal_signs["nx"] == "POSITIVE" else "W"
        else:
            return None
    elif sign == "NEGATIVE":
        if not normal["ny"]["contains_zero"]:
            chart = "N" if normal_signs["ny"] == "POSITIVE" else "S"
        else:
            return None
    else:
        return None
    return {
        **detail,
        "collision2_outgoing_chart": chart,
        "centered_C0_C1_resolution": True,
        "factorized_h_plus_h_minus_resolution": factor_resolution,
    }


def enhanced_root_record(
    parent_key: str,
    box: atlas.AtlasBox,
    geometry: tuple[Any, Any, Any, Any, Any],
    identifier: str,
) -> tuple[str, dict[str, Any] | None, dict[str, Any] | None]:
    kind, data = r178.root_record(*geometry, identifier)
    if kind in {"NO_REAL_INTERSECTION", "INTERSECTION_BEHIND",
                "STRICT_FUTURE"}:
        return kind, data, None
    evidence = surface_evidence(
        "DELTA", parent_key, box, identifier, include_axis_tests=False
    )
    sign = evidence["centered_C0_sign"]
    if sign == "NEGATIVE":
        return "NO_REAL_INTERSECTION", None, evidence
    if sign != "POSITIVE":
        return kind, data, evidence
    state = r181.collision1_state_direct(parent_key, box)
    raw = r181.raw_candidate(r183.collision2_geometry(state), identifier)
    delta_bounds = evidence["centered_mean_value_C0_enclosure"]
    delta = ge.arb_hull(
        arb(delta_bounds["lower"]).lower(),
        arb(delta_bounds["upper"]).upper(),
    )
    require(bool(delta > 0), "enhanced positive Delta")
    radical = delta.sqrt()
    near, far = raw["ell"] - radical, raw["ell"] + radical
    if bool(far < 0):
        return "INTERSECTION_BEHIND", None, evidence
    if not bool(near > 0):
        return "UNRESOLVED_ROOT_SIGN", None, evidence
    return "STRICT_FUTURE", {
        "near": near,
        "radical": radical,
        "transverse": raw["transverse"],
        "radius": raw["radius"],
    }, evidence


def enhanced_select_owner(
    parent_key: str,
    box: atlas.AtlasBox,
) -> tuple[str, tuple[str, dict[str, Any]] | None,
           list[dict[str, Any]]]:
    state = r181.collision1_state_direct(parent_key, box)
    geometry = r183.collision2_geometry(state)
    rows = {}
    evidence_rows = []
    unresolved = False
    for identifier in CANDIDATES:
        kind, data, evidence = enhanced_root_record(
            parent_key, box, geometry, identifier
        )
        rows[identifier] = (kind, data)
        if evidence is not None:
            evidence_rows.append(evidence)
        if kind in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}:
            unresolved = True
    future = [
        (identifier, data)
        for identifier, (kind, data) in rows.items()
        if kind == "STRICT_FUTURE" and data is not None
    ]
    winners = [
        (identifier, data)
        for identifier, data in future
        if all(
            identifier == other_identifier
            or bool(data["near"] < other_data["near"])
            for other_identifier, other_data in future
        )
    ]
    if len(winners) == 1 and not unresolved:
        return "STRICT_UNIQUE_OWNER", winners[0], evidence_rows
    return "UNRESOLVED_ENHANCED_OWNER", None, evidence_rows


def finish_collision2_owner(
    parent_key: str,
    box: atlas.AtlasBox,
    owner: tuple[str, dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    state = r181.collision1_state_direct(parent_key, box)
    official, reason = r178.gate5_key(
        state, owner, pair_index, pattern_index
    )
    if official is None:
        return "WALL_ENDPOINT", {
            "point_owner": owner[0], "reason": reason,
        }, []
    geometry = r183.collision2_geometry(state)
    next_state = r178.collision_state(geometry, owner)
    outgoing = r178.strict_chart(
        next_state["normal_x"], next_state["normal_y"]
    )
    detail = {"point_owner": owner[0], **official}
    if outgoing is not None:
        return "LOCAL_EXACT_KEY", {
            **detail, "collision2_outgoing_chart": outgoing,
        }, []
    evidence = relevant_surface_evidence(
        parent_key, box, "OUTGOING_H2", detail
    )
    enhanced = h2_exact_from_centered(detail, evidence)
    if enhanced is not None:
        return "LOCAL_EXACT_KEY_CENTERED_C1", enhanced, evidence
    return "OUTGOING_H2", detail, evidence


def relevant_surface_evidence(
    parent_key: str,
    box: atlas.AtlasBox,
    status: str,
    detail: dict[str, Any],
) -> list[dict[str, Any]]:
    if status == "OUTGOING_H2":
        return [
            surface_evidence(
                kind, parent_key, box, detail["point_owner"],
                include_axis_tests=False,
            )
            for kind in ("H2", "HPLUS", "HMINUS")
        ]
    if status.startswith("ACTIVE_DELTA_"):
        return [
            surface_evidence(
                "DELTA", parent_key, box, item["candidate"],
                include_axis_tests=False,
            )
            for item in detail["active_candidates"]
        ]
    if status == "POINT_WINNER_NONSTRICT":
        return [surface_evidence(
            "DELTA", parent_key, box, detail["point_owner"],
            include_axis_tests=False,
        )]
    return []


def resolve_dynamic_box(
    parent_key: str,
    box: atlas.AtlasBox,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[str, dict[str, Any], list[dict[str, Any]], str]:
    baseline_status, baseline_detail = r183.classify_box(
        parent_key, box, pair_index, pattern_index
    )
    if baseline_status == "LOCAL_EXACT_KEY":
        return baseline_status, baseline_detail, [], baseline_status
    if baseline_status == "OUTGOING_H2":
        evidence = relevant_surface_evidence(
            parent_key, box, baseline_status, baseline_detail
        )
        enhanced = h2_exact_from_centered(baseline_detail, evidence)
        if enhanced is not None:
            return (
                "LOCAL_EXACT_KEY_CENTERED_C1",
                enhanced,
                evidence,
                baseline_status,
            )
        return baseline_status, baseline_detail, evidence, baseline_status
    if (
        baseline_status.startswith("ACTIVE_DELTA_")
        or baseline_status in {
            "POINT_WINNER_NONSTRICT", "POINT_OWNER_NOT_UNIQUE"
        }
    ):
        owner_status, owner, evidence = enhanced_select_owner(
            parent_key, box
        )
        if owner_status == "STRICT_UNIQUE_OWNER" and owner is not None:
            status, detail, h2_evidence = finish_collision2_owner(
                parent_key, box, owner, pair_index, pattern_index
            )
            return status, detail, evidence + h2_evidence, baseline_status
        if not evidence:
            evidence = relevant_surface_evidence(
                parent_key, box, baseline_status, baseline_detail
            )
        return baseline_status, baseline_detail, evidence, baseline_status
    return baseline_status, baseline_detail, [], baseline_status


def compact_detail(status: str, detail: dict[str, Any]) -> dict[str, Any]:
    if (
        status.startswith("LOCAL_EXACT_KEY")
        or status.startswith("LOCAL_H2_FACTORIZED")
    ):
        return detail
    result = {
        "detail_sha256": digest(detail),
        "point_owner": detail.get("point_owner"),
    }
    if "reason" in detail:
        result["reason"] = detail["reason"]
    if "active_candidates" in detail:
        result["active_candidates"] = [
            row["candidate"] for row in detail["active_candidates"]
        ]
    if "official_gate5_key" in detail:
        result["official_gate5_key"] = detail["official_gate5_key"]
    return result


def dynamic_terminal_row(
    source: dict[str, Any],
    child: atlas.AtlasBox,
    status: str,
    detail: dict[str, Any],
    evidence: list[dict[str, Any]],
    baseline_child_status: str,
) -> dict[str, Any]:
    delta_identifiers = [
        row["identifier"] for row in evidence if row["kind"] == "DELTA"
    ]
    rank = rank2_record(
        source["origin_parent_key"], child, delta_identifiers
    )
    return closed_row({
        "source_kind": "ROUND183_DYNAMIC_RESIDUAL",
        "origin_parent_key": source["origin_parent_key"],
        "origin_terminal_path": source["terminal_path"],
        "origin_status": source["status"],
        "terminal_path": child.path,
        "Round185_relative_depth": DYNAMIC_EXTRA_DEPTH,
        "box": box_payload(child),
        "baseline_child_status": baseline_child_status,
        "status": status,
        "detail": compact_detail(status, detail),
        "surface_summaries": [
            compact_surface_summary(row) for row in evidence
        ],
        "surface_evidence_rows_sha256": digest(evidence),
        "conditional_rank2_record": rank,
        "global_credit": 0,
        "whole_parent_or_stratum_credit": 0,
    })


def split_axis(
    box: atlas.AtlasBox, axis: int
) -> tuple[atlas.AtlasBox, atlas.AtlasBox]:
    bounds = [
        [box.t0, box.t1],
        [box.p0, box.p1],
        [box.s0, box.s1],
    ]
    middle = (bounds[axis][0] + bounds[axis][1]) / 2
    left_bounds = copy.deepcopy(bounds)
    right_bounds = copy.deepcopy(bounds)
    left_bounds[axis][1] = middle
    right_bounds[axis][0] = middle
    depth = box.depth + 1
    return (
        atlas.AtlasBox(
            left_bounds[0][0], left_bounds[0][1],
            left_bounds[1][0], left_bounds[1][1],
            left_bounds[2][0], left_bounds[2][1],
            depth, box.path + f"{axis}0",
        ),
        atlas.AtlasBox(
            right_bounds[0][0], right_bounds[0][1],
            right_bounds[1][0], right_bounds[1][1],
            right_bounds[2][0], right_bounds[2][1],
            depth, box.path + f"{axis}1",
        ),
    )


def factor_sign(record: dict[str, Any]) -> int:
    return {
        "POSITIVE": 1,
        "NEGATIVE": -1,
        "UNRESOLVED": 0,
    }[record["centered_C0_sign"]]


def chart_from_factor_signs(hplus: int, hminus: int) -> str:
    require(hplus != 0 and hminus != 0, "strict factor signs")
    if hplus == hminus:
        return "E" if hplus > 0 else "W"
    return "N" if hplus > 0 else "S"


def hfactor_records(
    parent_key: str,
    box: atlas.AtlasBox,
    identifier: str,
) -> dict[str, dict[str, Any]]:
    return {
        kind: surface_evidence(
            kind, parent_key, box, identifier, include_axis_tests=True
        )
        for kind in ("HPLUS", "HMINUS")
    }


def hfactor_disposition(
    detail: dict[str, Any],
    records: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any], int | None]:
    plus_sign = factor_sign(records["HPLUS"])
    minus_sign = factor_sign(records["HMINUS"])
    if plus_sign != 0 and minus_sign != 0:
        return "LOCAL_EXACT_KEY_FACTORIZED_C0", {
            **detail,
            "collision2_outgoing_chart":
                chart_from_factor_signs(plus_sign, minus_sign),
            "factor_signs": {
                "h_plus": sign_name(plus_sign),
                "h_minus": sign_name(minus_sign),
            },
            "exact_factorization_resolution": True,
        }, None
    if plus_sign == 0 and minus_sign == 0:
        return "H2_TWO_FACTOR_OVERWRAP_RESIDUAL", {
            "point_owner": detail["point_owner"],
            "reason": "both signed seam factors retain zero",
        }, None
    if plus_sign == 0:
        active_kind, active_record = "HPLUS", records["HPLUS"]
        fixed_kind, fixed_sign = "HMINUS", minus_sign
    else:
        active_kind, active_record = "HMINUS", records["HMINUS"]
        fixed_kind, fixed_sign = "HPLUS", plus_sign
    require(fixed_sign != 0, "fixed factor absent")
    strict_axes = [
        index for index, axis in enumerate(("dt", "dp", "ds"))
        if not active_record["full_box_C1_derivatives"][axis][
            "contains_zero"
        ]
    ]
    if not strict_axes:
        return "H2_FACTOR_C1_RESIDUAL", {
            "point_owner": detail["point_owner"],
            "active_factor": active_kind,
            "fixed_absent_factor": fixed_kind,
        }, None
    dependent_axis = strict_axes[0]
    if active_record["independently_certified_nonempty"]:
        if active_kind == "HPLUS":
            negative_chart = chart_from_factor_signs(-1, fixed_sign)
            positive_chart = chart_from_factor_signs(1, fixed_sign)
            seam_owner = "E" if fixed_sign > 0 else "W"
        else:
            negative_chart = chart_from_factor_signs(fixed_sign, -1)
            positive_chart = chart_from_factor_signs(fixed_sign, 1)
            seam_owner = "E" if fixed_sign > 0 else "W"
        return "LOCAL_H2_FACTORIZED_NONEMPTY_SEAM_ARRANGEMENT", {
            **detail,
            "active_factor": active_kind,
            "fixed_absent_factor": fixed_kind,
            "fixed_factor_sign": sign_name(fixed_sign),
            "strict_dependent_axis": ("t", "p", "s")[dependent_axis],
            "three_stratum_chart_assignment": {
                "active_factor_negative_3D": negative_chart,
                "active_factor_zero_2D_half_open_owner": seam_owner,
                "active_factor_positive_3D": positive_chart,
            },
            "nonempty_regular_2D_seam_certified": True,
            "ambient_3D_sides_fully_classified": True,
            "whole_parent_or_stratum_credit": 0,
        }, dependent_axis
    return "H2_FACTOR_EXISTENCE_RESIDUAL", {
        "point_owner": detail["point_owner"],
        "active_factor": active_kind,
        "fixed_absent_factor": fixed_kind,
        "fixed_factor_sign": sign_name(fixed_sign),
        "strict_dependent_axis": ("t", "p", "s")[dependent_axis],
        "regular_if_present": True,
        "existence_certified": False,
    }, dependent_axis


def process_h2(
    rows: list[dict[str, Any]],
    initial_factor_cache: dict[
        tuple[str, str], dict[str, dict[str, Any]]
    ] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]]]:
    exact_rows, arrangement_rows, residual_rows, attachments = [], [], [], []
    split_face_rows: list[dict[str, Any]] = []
    for source in sorted(rows, key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    )):
        parent_key = source["origin_parent_key"]
        identifier = source["detail"]["point_owner"]
        parent = box_from_payload(source["box"], source["terminal_path"])
        cache_key = (parent_key, source["terminal_path"])
        initial_records = (
            initial_factor_cache[cache_key]
            if initial_factor_cache is not None
            else hfactor_records(parent_key, parent, identifier)
        )
        status, detail, dependent_axis = hfactor_disposition(
            source["detail"], initial_records
        )
        terminals: list[tuple[atlas.AtlasBox, int, str,
                              dict[str, Any],
                              dict[str, dict[str, Any]]]] = []
        if status != "H2_FACTOR_EXISTENCE_RESIDUAL":
            terminals.append((parent, 0, status, detail, initial_records))
        else:
            assert dependent_axis is not None
            pending = [(parent, 0)]
            while pending:
                box, depth = pending.pop()
                records = hfactor_records(parent_key, box, identifier)
                child_status, child_detail, child_dependent = (
                    hfactor_disposition(source["detail"], records)
                )
                if (
                    child_status == "H2_FACTOR_EXISTENCE_RESIDUAL"
                    and depth < 2
                ):
                    assert child_dependent is not None
                    transverse = [
                        axis for axis in range(3)
                        if axis != child_dependent
                    ]
                    widths = (
                        box.t1 - box.t0,
                        box.p1 - box.p0,
                        box.s1 - box.s0,
                    )
                    split_choice = max(
                        transverse, key=lambda axis: widths[axis]
                    )
                    left, right = split_axis(box, split_choice)
                    coordinate = (
                        (box.t0 + box.t1) / 2,
                        (box.p0 + box.p1) / 2,
                        (box.s0 + box.s1) / 2,
                    )[split_choice]
                    left_probe = hfactor_disposition(
                        source["detail"],
                        hfactor_records(parent_key, left, identifier),
                    )[0]
                    right_probe = hfactor_disposition(
                        source["detail"],
                        hfactor_records(parent_key, right, identifier),
                    )[0]
                    face = fixed_axis_box(
                        box, split_choice, coordinate, ".split-face"
                    )
                    face_records = hfactor_records(
                        parent_key, face, identifier
                    )
                    face_status, face_detail, _face_axis = (
                        hfactor_disposition(source["detail"], face_records)
                    )
                    split_face_rows.append(closed_row({
                        "origin_parent_key": parent_key,
                        "split_parent_path": box.path,
                        "axis": ("t", "p", "s")[split_choice],
                        "coordinate": str(coordinate),
                        "face_box": box_payload(face),
                        "dimension": 2,
                        "half_open_owner_child_path": left.path,
                        "excluded_duplicate_child_path": right.path,
                        "child_statuses": [left_probe, right_probe],
                        "child_statuses_differ": left_probe != right_probe,
                        "face_reclassified": True,
                        "face_status": face_status,
                        "face_detail_sha256": digest(face_detail),
                        "face_surface_summaries": [
                            compact_surface_summary(face_records["HPLUS"]),
                            compact_surface_summary(face_records["HMINUS"]),
                        ],
                        "face_surface_evidence_rows_sha256": digest([
                            face_records["HPLUS"],
                            face_records["HMINUS"],
                        ]),
                        "active_factor_intersection_dimension": 1,
                        "active_factor_intersection_nonempty_certified":
                            False,
                        "split_face_boundary_0D_closure_claimed": False,
                        "scope": (
                            "deduplicates the adaptive rectangular cover; "
                            "does not close factor/face or corner incidence"
                        ),
                    }))
                    pending.extend(((right, depth + 1),
                                    (left, depth + 1)))
                    continue
                terminals.append((
                    box, depth, child_status, child_detail, records
                ))
        for box, depth, terminal_status, terminal_detail, records in terminals:
            evidence = [records["HPLUS"], records["HMINUS"]]
            row = dynamic_terminal_row(
                source, box, terminal_status, terminal_detail,
                evidence, "OUTGOING_H2"
            )
            row_payload = copy.deepcopy(row)
            row_payload.pop("row_sha256")
            row_payload["Round185_relative_depth"] = depth
            row = closed_row(row_payload)
            if terminal_status.startswith("LOCAL_EXACT_KEY"):
                exact_rows.append(row)
            elif terminal_status.startswith("LOCAL_H2_FACTORIZED"):
                arrangement_rows.append(row)
            else:
                residual_rows.append(row)
            if len(attachments) < 8:
                attachments.append({
                    "origin_parent_key": parent_key,
                    "terminal_path": box.path,
                    "status": terminal_status,
                    "surface_evidence": evidence,
                })
    key = lambda row: (row["origin_parent_key"], row["terminal_path"])
    return (
        sorted(exact_rows, key=key),
        sorted(arrangement_rows, key=key),
        sorted(residual_rows, key=key),
        attachments,
        sorted(split_face_rows, key=lambda row: (
            row["origin_parent_key"], row["split_parent_path"]
        )),
    )


def process_dynamic(
    rows: list[dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]]]:
    exact_rows, residual_rows = [], []
    split_face_rows: list[dict[str, Any]] = []
    attachments: list[dict[str, Any]] = []
    attachment_counts: Counter[str] = Counter()
    ordered = sorted(
        (row for row in rows if row["status"] != "OUTGOING_H2"),
        key=lambda row: (
        PRIORITY.get(row["status"], 99),
        row["origin_parent_key"], row["terminal_path"],
    ))
    for source in ordered:
        parent_key = source["origin_parent_key"]
        parent = box_from_payload(source["box"], source["terminal_path"])
        left, right = ge.split(parent)
        axis = next(
            index for index, values in enumerate((
                (parent.t0, left.t1, right.t0, parent.t1),
                (parent.p0, left.p1, right.p0, parent.p1),
                (parent.s0, left.s1, right.s0, parent.s1),
            ))
            if values[0] < values[1] == values[2] < values[3]
        )
        coordinate = (
            left.t1, left.p1, left.s1
        )[axis]
        child_statuses = []
        for child in (left, right):
            status, detail, evidence, baseline = resolve_dynamic_box(
                parent_key, child, pair_index, pattern_index
            )
            child_statuses.append(status)
            row = dynamic_terminal_row(
                source, child, status, detail, evidence, baseline
            )
            if status.startswith("LOCAL_EXACT_KEY"):
                exact_rows.append(row)
            else:
                residual_rows.append(row)
            if evidence and attachment_counts[baseline] < 2:
                attachments.append({
                    "origin_parent_key": parent_key,
                    "terminal_path": child.path,
                    "baseline_child_status": baseline,
                    "final_status": status,
                    "surface_evidence": evidence,
                })
                attachment_counts[baseline] += 1
        face = fixed_axis_box(
            parent, axis, coordinate, ".split-face"
        )
        face_status, face_detail, face_evidence, face_baseline = (
            resolve_dynamic_box(
                parent_key, face, pair_index, pattern_index
            )
        )
        split_face_rows.append(closed_row({
            "origin_parent_key": parent_key,
            "split_parent_path": parent.path,
            "axis": ("t", "p", "s")[axis],
            "coordinate": str(coordinate),
            "face_box": box_payload(face),
            "dimension": 2,
            "half_open_owner_child_path": left.path,
            "excluded_duplicate_child_path": right.path,
            "child_statuses": child_statuses,
            "child_statuses_differ": child_statuses[0] != child_statuses[1],
            "face_reclassified": True,
            "face_baseline_status": face_baseline,
            "face_status": face_status,
            "face_detail_sha256": digest(face_detail),
            "face_surface_summaries": [
                compact_surface_summary(row) for row in face_evidence
            ],
            "face_surface_evidence_rows_sha256": digest(face_evidence),
            "nominal_boundary_surface_1D_intersection_outers":
                len(face_evidence),
            "certified_nonempty_transverse_1D_intersections": 0,
            "certified_0D_corner_credit": 0,
            "scope":
                "deduplicates and reclassifies the one-level non-H2 face",
        }))
    exact_rows.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    residual_rows.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    return (
        exact_rows,
        residual_rows,
        attachments,
        ordered,
        sorted(split_face_rows, key=lambda row: (
            row["origin_parent_key"], row["split_parent_path"]
        )),
    )


def inherited_surface_evidence(
    parent_key: str,
    box: atlas.AtlasBox,
    status: str,
) -> list[dict[str, Any]]:
    if status == "SOURCE_CHART_SEAM_COLLAR":
        return [surface_evidence(
            "H0", parent_key, box, "SOURCE_CHART_SEAM",
            include_axis_tests=False,
        )]
    if status == "COLLISION1_OUTGOING_CHART_COLLAR":
        return [surface_evidence(
            "H1", parent_key, box, r178.COLLISION1_OWNER,
            include_axis_tests=False,
        )]
    if status == "COLLISION1_DELTA_ROOT_COLLAR":
        source_cell = r178.source_chart_for_box(parent_key, box)
        if source_cell is None:
            return []
        geometry = r178.initial_geometry(
            ":".join(parent_key.split(":")[:2]), box
        )
        identifiers = r178.translated_candidates(
            f"W:{source_cell}", (0, 0)
        )
        return [
            surface_evidence(
                "DELTA0", parent_key, box, identifier,
                include_axis_tests=False,
            )
            for identifier in identifiers
            if r178.root_record(*geometry, identifier)[0]
            in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}
        ]
    return []


def inherited_terminal_row(
    source: dict[str, Any],
    child: atlas.AtlasBox,
    status: str,
    detail: dict[str, Any] | None,
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    return closed_row({
        "source_kind": "ROUND183_INHERITED_COLLISION1_OR_SOURCE_CARRIER",
        "origin_parent_key": source["parent_key"],
        "origin_terminal_path": source["terminal_path"],
        "origin_status": source["status"],
        "terminal_path": child.path,
        "Round185_relative_depth": INHERITED_EXTRA_DEPTH,
        "box": box_payload(child),
        "status": status,
        "detail": detail,
        "surface_summaries": [
            compact_surface_summary(row) for row in evidence
        ],
        "surface_evidence_rows_sha256": digest(evidence),
        "source_seam_2D_half_open_owner": (
            "E" if source["status"] == "SOURCE_CHART_SEAM_COLLAR"
            else None
        ),
        "global_credit": 0,
        "whole_parent_or_stratum_credit": 0,
    })


def process_inherited(
    rows: list[dict[str, Any]],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]]]:
    exact_rows, excluded_rows, residual_rows, attachments = [], [], [], []
    split_face_rows: list[dict[str, Any]] = []
    attachment_counts: Counter[str] = Counter()
    for source in sorted(rows, key=lambda row: (
        row["parent_key"], row["terminal_path"]
    )):
        parent = r181.box_from_row(source)
        chart_id = ":".join(source["parent_key"].split(":")[:2])
        left, right = ge.split(parent)
        axis = next(
            index for index, values in enumerate((
                (parent.t0, left.t1, right.t0, parent.t1),
                (parent.p0, left.p1, right.p0, parent.p1),
                (parent.s0, left.s1, right.s0, parent.s1),
            ))
            if values[0] < values[1] == values[2] < values[3]
        )
        coordinate = (left.t1, left.p1, left.s1)[axis]
        child_statuses = []
        for child in (left, right):
            phase_status, state = r178.collision1_classification(
                source["parent_key"], chart_id, child
            )
            evidence: list[dict[str, Any]] = []
            detail: dict[str, Any] | None = None
            if phase_status == "STRICT_COLLISION1_LIVE":
                status, dynamic_detail, dynamic_evidence, _baseline = (
                    resolve_dynamic_box(
                        source["parent_key"], child,
                        pair_index, pattern_index,
                    )
                )
                evidence = dynamic_evidence
                detail = compact_detail(status, dynamic_detail)
                final_status = (
                    status if status.startswith("LOCAL_EXACT_KEY")
                    else f"INHERITED_TO_{status}"
                )
            elif phase_status.startswith("STRICT_NOT_LIVE_"):
                final_status = "LOCAL_EXCLUDED_FROM_FROZEN_LIVE_STRATUM"
                detail = {"collision1_disposition": phase_status}
            else:
                final_status = phase_status
                evidence = inherited_surface_evidence(
                    source["parent_key"], child, phase_status
                )
                detail = {
                    "collision1_status": phase_status,
                    "root_order_C1_pair_surface_formalized":
                        phase_status != "COLLISION1_ROOT_ORDER_COLLAR",
                }
            row = inherited_terminal_row(
                source, child, final_status, detail, evidence
            )
            child_statuses.append(final_status)
            if final_status.startswith("LOCAL_EXACT_KEY"):
                exact_rows.append(row)
            elif final_status == "LOCAL_EXCLUDED_FROM_FROZEN_LIVE_STRATUM":
                excluded_rows.append(row)
            else:
                residual_rows.append(row)
            if evidence and attachment_counts[phase_status] < 2:
                attachments.append({
                    "origin_parent_key": source["parent_key"],
                    "terminal_path": child.path,
                    "origin_status": source["status"],
                    "phase_status": phase_status,
                    "surface_evidence": evidence,
                })
                attachment_counts[phase_status] += 1
        face = fixed_axis_box(parent, axis, coordinate, ".split-face")
        face_phase_status, _face_state = r178.collision1_classification(
            source["parent_key"], chart_id, face
        )
        face_evidence: list[dict[str, Any]] = []
        if face_phase_status == "STRICT_COLLISION1_LIVE":
            (
                face_dynamic_status,
                face_dynamic_detail,
                face_evidence,
                _face_baseline,
            ) = resolve_dynamic_box(
                source["parent_key"], face, pair_index, pattern_index
            )
            face_status = face_dynamic_status
            face_detail = compact_detail(
                face_dynamic_status, face_dynamic_detail
            )
        elif face_phase_status.startswith("STRICT_NOT_LIVE_"):
            face_status = "LOCAL_EXCLUDED_FROM_FROZEN_LIVE_STRATUM"
            face_detail = {"collision1_disposition": face_phase_status}
        else:
            face_status = face_phase_status
            face_evidence = inherited_surface_evidence(
                source["parent_key"], face, face_phase_status
            )
            face_detail = {"collision1_status": face_phase_status}
        split_face_rows.append(closed_row({
            "origin_parent_key": source["parent_key"],
            "split_parent_path": parent.path,
            "axis": ("t", "p", "s")[axis],
            "coordinate": str(coordinate),
            "face_box": box_payload(face),
            "dimension": 2,
            "half_open_owner_child_path": left.path,
            "excluded_duplicate_child_path": right.path,
            "child_statuses": child_statuses,
            "child_statuses_differ": child_statuses[0] != child_statuses[1],
            "face_reclassified": True,
            "face_status": face_status,
            "face_detail_sha256": digest(face_detail),
            "face_surface_summaries": [
                compact_surface_summary(row) for row in face_evidence
            ],
            "face_surface_evidence_rows_sha256": digest(face_evidence),
            "nominal_boundary_surface_1D_intersection_outers":
                len(face_evidence),
            "certified_nonempty_transverse_1D_intersections": 0,
            "certified_0D_corner_credit": 0,
            "source_seam_2D_half_open_owner": (
                "E" if source["status"] == "SOURCE_CHART_SEAM_COLLAR"
                else None
            ),
            "scope":
                "deduplicates and reclassifies the inherited split face",
        }))
    key = lambda row: (row["origin_parent_key"], row["terminal_path"])
    return (
        sorted(exact_rows, key=key),
        sorted(excluded_rows, key=key),
        sorted(residual_rows, key=key),
        attachments,
        sorted(split_face_rows, key=lambda row: (
            row["origin_parent_key"], row["split_parent_path"]
        )),
    )


def rank2_record(
    parent_key: str,
    box: atlas.AtlasBox,
    identifiers: list[str],
) -> dict[str, Any] | None:
    if len(identifiers) != 2:
        return None
    left = delta_ad(parent_key, box, identifiers[0])
    right = delta_ad(parent_key, box, identifiers[1])
    pairs = {
        "t_p": (0, 1),
        "t_s": (0, 2),
        "p_s": (1, 2),
    }
    minors = {}
    for name, (first, second) in pairs.items():
        value = (
            left.derivative[first] * right.derivative[second]
            - left.derivative[second] * right.derivative[first]
        )
        minors[name] = {
            **arb_bounds(value),
            "strict_nonzero": strict_sign(value) != 0,
        }
    return {
        "identifiers": identifiers,
        "C1_cross_gradient_minors": minors,
        "strict_rank_2_if_intersection":
            any(row["strict_nonzero"] for row in minors.values()),
        "intersection_existence_certified": False,
        "scope":
            "rank regularity is conditional; independent coupled "
            "Poincare-Miranda/Krawczyk existence is still required",
    }


def h2_baseline_taxonomy(
    rows: list[dict[str, Any]],
    axes: tuple[tuple[int, int], ...] = OBLIQUE_AXES,
) -> dict[str, Any]:
    derivative_counts: Counter[str] = Counter()
    face_counts: Counter[str] = Counter()
    newton_counts: Counter[str] = Counter()
    centered_counts: Counter[str] = Counter()
    corner_brackets = 0
    preconditioners = 0
    oblique = {
        f"{a},{b}": Counter() for a, b in axes
    }
    oblique_areas: dict[str, list[Q]] = {
        f"{a},{b}": [] for a, b in axes
    }
    either_oblique_face = 0
    either_oblique_newton = 0
    first_regression = None
    first_oblique = None
    for source in sorted(rows, key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    )):
        box = box_from_payload(source["box"], source["terminal_path"])
        identifier = source["detail"]["point_owner"]
        evidence = surface_evidence(
            "H2", source["origin_parent_key"], box, identifier,
            include_axis_tests=True,
        )
        for axis in ("dt", "dp", "ds"):
            if not evidence["full_box_C1_derivatives"][axis]["contains_zero"]:
                derivative_counts[axis] += 1
        for index, axis in enumerate(("t", "p", "s")):
            if evidence["axis_full_face_brackets_t_p_s"][index]:
                face_counts[axis] += 1
            if evidence["axis_interval_Newton"][index][
                "strict_interior_self_map"
            ]:
                newton_counts[axis] += 1
        centered_counts[evidence["centered_C0_sign"]] += 1
        corner_brackets += (
            evidence["strict_corner_segment_bracket"] is not None
        )
        preconditioners += evidence[
            "dyadic_oblique_preconditioner"]["available"]
        row_face = False
        row_newton = False
        probes = []
        for a, b in axes:
            probe = oblique_axis_probe(
                source["origin_parent_key"], box, identifier, a, b
            )
            probes.append(probe)
            key = f"{a},{b}"
            oblique[key]["strict_u_derivative"] += probe[
                "strict_u_derivative"]
            oblique[key]["strict_opposite_sign_u_faces"] += probe[
                "strict_opposite_sign_u_faces"]
            oblique[key]["strict_interval_Newton_u_self_map"] += probe[
                "strict_interval_Newton_u_self_map"]
            oblique_areas[key].append(Q(probe[
                "inner_cell_relative_tp_area"]))
            row_face = row_face or probe["strict_opposite_sign_u_faces"]
            row_newton = (
                row_newton
                or probe["strict_interval_Newton_u_self_map"]
            )
        either_oblique_face += row_face
        either_oblique_newton += row_newton
        if first_regression is None:
            first_regression = {
                "origin_parent_key": source["origin_parent_key"],
                "terminal_path": source["terminal_path"],
                "box": source["box"],
                "identifier": identifier,
                "full_H2_evidence": evidence,
                "short_Arb_repr_used_for_sign_decision": False,
                "sign_decisions_use_exact_lower_upper_and_contains_zero":
                    True,
            }
            first_oblique = probes
    require(first_regression is not None, "H2 regression")
    require(sum(centered_counts.values()) == len(rows), "H2 centered census")
    oblique_result = {}
    for key in sorted(oblique):
        areas = oblique_areas[key]
        oblique_result[key] = {
            **dict(sorted(oblique[key].items())),
            "minimum_inner_cell_relative_tp_area": str(min(areas)),
            "maximum_inner_cell_relative_tp_area": str(max(areas)),
        }
    return {
        "input_H2_box_count": len(rows),
        "full_box_strict_derivative_counts":
            dict(sorted(derivative_counts.items())),
        "original_axis_full_opposite_face_counts":
            dict(sorted(face_counts.items())),
        "original_axis_interval_Newton_self_map_counts":
            dict(sorted(newton_counts.items())),
        "centered_mean_value_C0_sign_counts":
            dict(sorted(centered_counts.items())),
        "strict_corner_segment_bracket_count": corner_brackets,
        "dyadic_oblique_preconditioner_available_count": preconditioners,
        "oblique_candidate_axes": [list(pair) for pair in axes],
        "oblique_inner_cell_taxonomy": oblique_result,
        "boxes_with_any_oblique_strict_face_bracket":
            either_oblique_face,
        "boxes_with_any_oblique_interval_Newton_self_map":
            either_oblique_newton,
        "first_full_box_regression": first_regression,
        "first_oblique_probe_rows": first_oblique,
        "regularity_is_not_existence": True,
        "inner_oblique_cells_do_not_cover_source_rectangles": True,
        "whole_parent_or_stratum_credit": 0,
    }


def hfactor_baseline_taxonomy(
    rows: list[dict[str, Any]],
    evidence_cache: dict[
        tuple[str, str], dict[str, dict[str, Any]]
    ] | None = None,
) -> dict[str, Any]:
    factor_counts = {
        "HPLUS": Counter(),
        "HMINUS": Counter(),
    }
    derivative_counts = {
        "HPLUS": Counter(),
        "HMINUS": Counter(),
    }
    face_counts = {
        "HPLUS": Counter(),
        "HMINUS": Counter(),
    }
    newton_counts = {
        "HPLUS": Counter(),
        "HMINUS": Counter(),
    }
    both_centered_overwrap = 0
    both_factors_absent = 0
    any_factor_existence = 0
    both_factor_existence = 0
    unit_normal_interval_excludes_zero = 0
    first = None
    for source in sorted(rows, key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    )):
        box = box_from_payload(source["box"], source["terminal_path"])
        parent_key = source["origin_parent_key"]
        identifier = source["detail"]["point_owner"]
        evidence_by_kind = {}
        existence_flags = []
        absent_flags = []
        for kind in ("HPLUS", "HMINUS"):
            evidence = surface_evidence(
                kind, parent_key, box, identifier,
                include_axis_tests=True,
            )
            evidence_by_kind[kind] = evidence
            absent = evidence["centered_C0_sign"] != "UNRESOLVED"
            existence = evidence["independently_certified_nonempty"]
            regular = evidence["regular_if_present"]
            if absent:
                disposition = "CENTERED_C0_ABSENT"
            elif existence and regular:
                disposition = "NONEMPTY_REGULAR_GRAPH"
            elif existence:
                disposition = "NONEMPTY_DERIVATIVE_UNRESOLVED"
            elif regular:
                disposition = "REGULAR_IF_PRESENT_RESIDUAL"
            else:
                disposition = "C0_C1_RESIDUAL"
            factor_counts[kind][disposition] += 1
            absent_flags.append(absent)
            existence_flags.append(existence)
            for axis in ("dt", "dp", "ds"):
                if not evidence["full_box_C1_derivatives"][axis][
                    "contains_zero"
                ]:
                    derivative_counts[kind][axis] += 1
            for index, axis in enumerate(("t", "p", "s")):
                if evidence["axis_full_face_brackets_t_p_s"][index]:
                    face_counts[kind][axis] += 1
                if evidence["axis_interval_Newton"][index][
                    "strict_interior_self_map"
                ]:
                    newton_counts[kind][axis] += 1
        if evidence_cache is not None:
            evidence_cache[(
                source["origin_parent_key"], source["terminal_path"]
            )] = evidence_by_kind
        both_centered_overwrap += not any(absent_flags)
        both_factors_absent += all(absent_flags)
        any_factor_existence += any(existence_flags)
        both_factor_existence += all(existence_flags)
        _h2, nx, ny = outgoing_h2_ad(parent_key, box, identifier)
        normal_squared = nx.value * nx.value + ny.value * ny.value
        unit_normal_interval_excludes_zero += bool(normal_squared > 0)
        if first is None:
            first = {
                "origin_parent_key": parent_key,
                "terminal_path": source["terminal_path"],
                "identifier": identifier,
                "HPLUS": evidence_by_kind["HPLUS"],
                "HMINUS": evidence_by_kind["HMINUS"],
                "normal_squared_interval": arb_bounds(normal_squared),
            }
    require(first is not None, "factor regression")
    return {
        "input_H2_box_count": len(rows),
        "exact_factorization": (
            "H2=(n2_x+n2_y)*(n2_x-n2_y)=h_plus*h_minus"
        ),
        "factor_disposition_counts": {
            key: dict(sorted(value.items()))
            for key, value in factor_counts.items()
        },
        "factor_full_box_strict_derivative_counts": {
            key: dict(sorted(value.items()))
            for key, value in derivative_counts.items()
        },
        "factor_original_axis_full_face_bracket_counts": {
            key: dict(sorted(value.items()))
            for key, value in face_counts.items()
        },
        "factor_original_axis_interval_Newton_self_map_counts": {
            key: dict(sorted(value.items()))
            for key, value in newton_counts.items()
        },
        "both_factor_centered_C0_overwrap_box_count":
            both_centered_overwrap,
        "both_factors_centered_C0_absent_box_count":
            both_factors_absent,
        "boxes_with_any_independent_factor_existence":
            any_factor_existence,
        "boxes_with_both_factor_existences":
            both_factor_existence,
        "unit_normal_interval_excludes_zero_box_count":
            unit_normal_interval_excludes_zero,
        "simultaneous_h_plus_h_minus_zero_impossible": True,
        "simultaneous_zero_proof": (
            "h_plus=h_minus=0 implies n2_x=n2_y=0, contradicting the "
            "exact collision-normal identity n2_x^2+n2_y^2=1"
        ),
        "first_factor_regression": first,
        "strict_H2_C0_absence_and_factor_existence_ledgers_are_disjoint":
            True,
        "whole_parent_or_stratum_credit": 0,
    }


def fraction_map(values: dict[str, Q]) -> dict[str, str]:
    return {key: str(value) for key, value in sorted(values.items())}


def status_volume(rows: list[dict[str, Any]]) -> tuple[dict[str, int],
                                                       dict[str, str]]:
    counts = Counter(row["status"] for row in rows)
    volumes: dict[str, Q] = defaultdict(lambda: Q(0))
    for row in rows:
        volumes[row["status"]] += Q(row["box"]["volume"])
    return dict(sorted(counts.items())), fraction_map(volumes)


def split_corner_census(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    raw = []
    for row in rows:
        face = row["face_box"]
        for t, p, s in itertools.product(
            (face["t"][0], face["t"][1]),
            (face["p"][0], face["p"][1]),
            (face["s"][0], face["s"][1]),
        ):
            raw.append((
                row["origin_parent_key"], t, p, s
            ))
    unique = sorted(set(raw))
    return {
        "raw_0D_corner_occurrence_count": len(raw),
        "unique_0D_corner_key_count": len(unique),
        "duplicate_0D_corner_occurrence_count": len(raw) - len(unique),
        "unique_0D_corner_keys_sha256": digest(unique),
        "certified_0D_boundary_incidence_credit": 0,
    }


def build_result(producer_sha256: str) -> dict[str, Any]:
    upstream183, upstream181, upstream178 = load_chain()
    pair_index, pattern_index, registry_digest = registry.key_index_tables()
    require(registry_digest == r178.GATE5_REGISTRY_DIGEST, "registry")
    dynamic_inputs = upstream183["dynamic_residual_ledger"]["rows"]
    require(
        len(dynamic_inputs) == 25040
        and Counter(row["status"] for row in dynamic_inputs) == {
            "OUTGOING_H2": 11908,
            "POINT_WINNER_NONSTRICT": 8214,
            "ACTIVE_DELTA_1": 4800,
            "ACTIVE_DELTA_2": 118,
        },
        "Round183 dynamic inputs",
    )
    h2_inputs = [
        row for row in dynamic_inputs if row["status"] == "OUTGOING_H2"
    ]
    h2_taxonomy = h2_baseline_taxonomy(h2_inputs)
    factor_cache: dict[
        tuple[str, str], dict[str, dict[str, Any]]
    ] = {}
    hfactor_taxonomy = hfactor_baseline_taxonomy(
        h2_inputs, factor_cache
    )
    (
        h2_exact,
        h2_arrangements,
        h2_residual,
        h2_attachments,
        h2_split_faces,
    ) = process_h2(h2_inputs, factor_cache)
    (
        other_exact,
        other_residual,
        other_attachments,
        ordered_other,
        other_split_faces,
    ) = process_dynamic(dynamic_inputs, pair_index, pattern_index)
    dynamic_exact = sorted(
        h2_exact + other_exact,
        key=lambda row: (
            row["origin_parent_key"], row["terminal_path"]
        ),
    )
    dynamic_arrangements = h2_arrangements
    dynamic_residual = sorted(
        h2_residual + other_residual,
        key=lambda row: (
            row["origin_parent_key"], row["terminal_path"]
        ),
    )
    phase_statuses = {
        "COLLISION1_DELTA_ROOT_COLLAR",
        "COLLISION1_OUTGOING_CHART_COLLAR",
        "COLLISION1_ROOT_ORDER_COLLAR",
        "SOURCE_CHART_SEAM_COLLAR",
    }
    round178_rows = upstream178[
        "bounded_full_parent_3D_ledger"]["terminal_rows"]
    inherited_inputs = [
        row for row in round178_rows if row["status"] in phase_statuses
    ]
    require(
        len(inherited_inputs) == 530
        and Counter(row["status"] for row in inherited_inputs) == {
            "COLLISION1_DELTA_ROOT_COLLAR": 276,
            "COLLISION1_OUTGOING_CHART_COLLAR": 172,
            "COLLISION1_ROOT_ORDER_COLLAR": 50,
            "SOURCE_CHART_SEAM_COLLAR": 32,
        },
        "Round183 inherited inputs",
    )
    (
        inherited_exact,
        inherited_excluded,
        inherited_residual,
        inherited_attachments,
        inherited_split_faces,
    ) = process_inherited(
        inherited_inputs, pair_index, pattern_index
    )
    dynamic_input_volume = sum(
        Q(row["box"]["volume"]) for row in dynamic_inputs
    )
    require(
        dynamic_input_volume
        == Q(upstream183["dynamic_residual_ledger"][
            "exact_coordinate_volume"]),
        "dynamic input volume",
    )
    dynamic_exact_volume = sum(
        Q(row["box"]["volume"]) for row in dynamic_exact
    )
    dynamic_arrangement_volume = sum(
        Q(row["box"]["volume"]) for row in dynamic_arrangements
    )
    dynamic_residual_volume = sum(
        Q(row["box"]["volume"]) for row in dynamic_residual
    )
    require(
        dynamic_exact_volume
        + dynamic_arrangement_volume
        + dynamic_residual_volume
        == dynamic_input_volume,
        "dynamic conservation",
    )
    inherited_input_volume = sum(
        Q(row["box"]["volume"]) for row in inherited_inputs
    )
    inherited_exact_volume = sum(
        Q(row["box"]["volume"]) for row in inherited_exact
    )
    inherited_excluded_volume = sum(
        Q(row["box"]["volume"]) for row in inherited_excluded
    )
    inherited_residual_volume = sum(
        Q(row["box"]["volume"]) for row in inherited_residual
    )
    require(
        inherited_exact_volume
        + inherited_excluded_volume
        + inherited_residual_volume
        == inherited_input_volume,
        "inherited conservation",
    )
    combined_input_volume = dynamic_input_volume + inherited_input_volume
    require(
        combined_input_volume
        == Q(upstream183["exact_residual_census"][
            "combined_residual_exact_coordinate_outer_volume"]),
        "combined Round183 residual volume",
    )
    combined_residual_volume = (
        dynamic_residual_volume + inherited_residual_volume
    )
    all_split_faces = sorted(
        h2_split_faces + other_split_faces + inherited_split_faces,
        key=lambda row: (
            row["origin_parent_key"], row["split_parent_path"],
            row["axis"], row["coordinate"],
        ),
    )
    split_corner_ledger = split_corner_census(all_split_faces)
    nominal_split_face_1d_outers = sum(
        (
            row.get("nominal_boundary_surface_1D_intersection_outers")
            if "nominal_boundary_surface_1D_intersection_outers" in row
            else 1
        )
        for row in all_split_faces
    )
    all_rows = (
        dynamic_exact + dynamic_arrangements + dynamic_residual
        + inherited_exact + inherited_excluded + inherited_residual
    )
    surface_summaries = [
        summary
        for row in all_rows
        for summary in row["surface_summaries"]
    ]
    surface_kind_counts = Counter(
        row["kind"] for row in surface_summaries
    )
    centered_sign_counts = Counter(
        (row["kind"], row["centered_C0_sign"])
        for row in surface_summaries
    )
    regular_surface_count = sum(
        bool(row["strict_derivative_axes"]) for row in surface_summaries
    )
    nonempty_surface_count = sum(
        row["independently_certified_nonempty"]
        for row in surface_summaries
    )
    rank_rows = [
        row["conditional_rank2_record"]
        for row in all_rows
        if row.get("conditional_rank2_record") is not None
    ]
    strict_rank2_count = sum(
        row["strict_rank_2_if_intersection"] for row in rank_rows
    )
    require(
        all(not row["intersection_existence_certified"]
            for row in rank_rows),
        "rank does not imply existence",
    )
    dynamic_exact_counts, dynamic_exact_volumes = status_volume(dynamic_exact)
    arrangement_counts, arrangement_volumes = status_volume(
        dynamic_arrangements
    )
    dynamic_residual_counts, dynamic_residual_volumes = status_volume(
        dynamic_residual
    )
    inherited_exact_counts, inherited_exact_volumes = status_volume(
        inherited_exact
    )
    inherited_excluded_counts, inherited_excluded_volumes = status_volume(
        inherited_excluded
    )
    inherited_residual_counts, inherited_residual_volumes = status_volume(
        inherited_residual
    )
    local_exact_rows = dynamic_exact + inherited_exact
    local_key_ids = sorted({
        row["detail"]["official_gate5_key"]["word_key_id"]
        for row in local_exact_rows
        if (
            row["detail"] is not None
            and "official_gate5_key" in row["detail"]
        )
    })
    local_ordinals = sorted({
        row["detail"]["official_gate5_key"]["ordinal_zero_based"]
        for row in local_exact_rows
        if (
            row["detail"] is not None
            and "official_gate5_key" in row["detail"]
        )
    })
    residual_by_parent = Counter(
        row["origin_parent_key"]
        for row in dynamic_residual + inherited_residual
    )
    arrangements_by_parent = Counter(
        row["origin_parent_key"] for row in dynamic_arrangements
    )
    exact_by_parent = Counter(
        row["origin_parent_key"]
        for row in dynamic_exact + inherited_exact + inherited_excluded
    )
    parent_rows = []
    for upstream in upstream183["per_parent_partial_ledger"]["rows"]:
        key = upstream["parent_key"]
        complete = (
            residual_by_parent[key] == 0
            and arrangements_by_parent[key] == 0
        )
        parent_rows.append(closed_row({
            "parent_key": key,
            "Round183_combined_local_exact_key_box_count":
                upstream["combined_local_exact_key_box_count"],
            "Round185_local_exact_or_excluded_cell_count":
                exact_by_parent[key],
            "Round185_dimensionally_arranged_H2_outer_count":
                arrangements_by_parent[key],
            "Round185_residual_outer_count": residual_by_parent[key],
            "all_dimensions_under_same_exact_key_closed": complete,
            "status": "FULL" if complete else "PARTIAL",
            "whole_parent_or_stratum_credit": int(complete),
        }))
    full_parents = sum(
        row["all_dimensions_under_same_exact_key_closed"]
        for row in parent_rows
    )
    # This bounded round is not allowed to promote a parent merely because
    # its 3D sides are classified while a local 2D seam arrangement remains.
    require(full_parents == 0, "unexpected whole-parent promotion")
    attachments = (
        h2_attachments + other_attachments + inherited_attachments
    )
    first_residual = (
        dynamic_residual[0] if dynamic_residual
        else inherited_residual[0] if inherited_residual
        else None
    )
    return {
        "status": (
            "PARTIAL_PRECONDITIONED_C0_C1_RESIDUAL_REFINEMENT__"
            "NO_WHOLE_PARENT_PROMOTION"
        ),
        "Round183_binding": {
            "certificate_result_sha256": R183_RESULT,
            "verification_result_sha256": R183_VERIFICATION_RESULT,
            "producer_sha256": PINS[R183_PRODUCER],
            "manifest_sha256": PINS[R183_MANIFEST],
            "dynamic_residual_input_count": len(dynamic_inputs),
            "inherited_carrier_input_count": len(inherited_inputs),
            "combined_input_count":
                len(dynamic_inputs) + len(inherited_inputs),
            "combined_input_exact_coordinate_outer_volume":
                str(combined_input_volume),
            "Round183_files_modified": False,
        },
        "bounded_refinement_contract": {
            "dynamic_non_H2_extra_depth": DYNAMIC_EXTRA_DEPTH,
            "H2_factor_residual_transverse_extra_depth": 2,
            "inherited_extra_depth": INHERITED_EXTRA_DEPTH,
            "all_25040_dynamic_residuals_processed": True,
            "all_530_inherited_carriers_processed": True,
            "centered_mean_value_C0_used": True,
            "full_box_automatic_C1_used": True,
            "H2_exact_signed_factorization_used": True,
            "regularity_alone_certifies_existence": False,
            "rank2_alone_certifies_intersection_existence": False,
            "half_open_equality_carriers_retained_in_own_dimension": True,
            "whole_stratum_requires_all_dimensions_same_exact_key": True,
        },
        "H2_full_box_preconditioned_probe": h2_taxonomy,
        "H2_signed_factor_union_probe": hfactor_taxonomy,
        "dynamic_local_exact_key_ledger": {
            "row_count": len(dynamic_exact),
            "rows_sha256": digest(dynamic_exact),
            "rows": dynamic_exact,
            "status_counts": dynamic_exact_counts,
            "status_volumes": dynamic_exact_volumes,
            "exact_coordinate_volume": str(dynamic_exact_volume),
            "local_gate5_key_ids": local_key_ids,
            "local_gate5_ordinals_zero_based": local_ordinals,
            "global_credit": 0,
            "whole_parent_or_stratum_credit": 0,
        },
        "dimensionally_arranged_H2_factor_seams": {
            "row_count": len(dynamic_arrangements),
            "rows_sha256": digest(dynamic_arrangements),
            "rows": dynamic_arrangements,
            "status_counts": arrangement_counts,
            "support_outer_volumes": arrangement_volumes,
            "support_outer_exact_coordinate_volume":
                str(dynamic_arrangement_volume),
            "ambient_3D_sides_classified": True,
            "nonempty_2D_seams_retained_once": len(dynamic_arrangements),
            "whole_parent_or_stratum_credit": 0,
        },
        "H2_adaptive_split_face_ledger": {
            "row_count": len(h2_split_faces),
            "rows_sha256": digest(h2_split_faces),
            "rows": h2_split_faces,
            "two_dimensional_split_faces_half_open_owned_once":
                len(h2_split_faces),
            "nominal_factor_split_face_1D_intersection_outers":
                len(h2_split_faces),
            "certified_nonempty_factor_split_face_1D_intersections": 0,
            "certified_0D_factor_face_corner_incidents": 0,
            "zero_dimensional_closure_claimed": False,
            "bounded_split_axis_heuristic": (
                "largest raw-width transverse axis; affects efficiency only"
            ),
            "whole_parent_or_stratum_credit": 0,
        },
        "all_adaptive_split_face_dimension_ledger": {
            "row_count": len(all_split_faces),
            "rows_sha256": digest(all_split_faces),
            "rows": all_split_faces,
            "H2_transverse_split_face_count": len(h2_split_faces),
            "non_H2_dynamic_split_face_count": len(other_split_faces),
            "inherited_split_face_count": len(inherited_split_faces),
            "two_dimensional_faces_half_open_owned_once":
                len(all_split_faces),
            "faces_with_different_child_statuses": sum(
                row["child_statuses_differ"] for row in all_split_faces
            ),
            "faces_independently_reclassified": len(all_split_faces),
            "nominal_boundary_surface_1D_intersection_outers":
                nominal_split_face_1d_outers,
            "certified_nonempty_transverse_1D_intersections": 0,
            "zero_dimensional_corner_deduplication": split_corner_ledger,
            "three_dimensional_volume_conservation_is_separate": True,
            "two_or_one_or_zero_dimensional_global_credit": 0,
        },
        "dynamic_residual_ledger": {
            "row_count": len(dynamic_residual),
            "rows_sha256": digest(dynamic_residual),
            "rows": dynamic_residual,
            "status_counts": dynamic_residual_counts,
            "status_volumes": dynamic_residual_volumes,
            "exact_coordinate_outer_volume": str(dynamic_residual_volume),
            "exact_conservation": (
                f"{dynamic_exact_volume}+{dynamic_arrangement_volume}+"
                f"{dynamic_residual_volume}={dynamic_input_volume}"
            ),
        },
        "inherited_local_exact_key_ledger": {
            "row_count": len(inherited_exact),
            "rows_sha256": digest(inherited_exact),
            "rows": inherited_exact,
            "status_counts": inherited_exact_counts,
            "status_volumes": inherited_exact_volumes,
            "exact_coordinate_volume": str(inherited_exact_volume),
            "whole_parent_or_stratum_credit": 0,
        },
        "inherited_local_exclusion_ledger": {
            "row_count": len(inherited_excluded),
            "rows_sha256": digest(inherited_excluded),
            "rows": inherited_excluded,
            "status_counts": inherited_excluded_counts,
            "status_volumes": inherited_excluded_volumes,
            "exact_coordinate_volume": str(inherited_excluded_volume),
            "scope": "excluded only from the frozen collision1 live stratum",
            "global_credit": 0,
        },
        "inherited_residual_ledger": {
            "row_count": len(inherited_residual),
            "rows_sha256": digest(inherited_residual),
            "rows": inherited_residual,
            "status_counts": inherited_residual_counts,
            "status_volumes": inherited_residual_volumes,
            "exact_coordinate_outer_volume": str(inherited_residual_volume),
            "exact_conservation": (
                f"{inherited_exact_volume}+{inherited_excluded_volume}+"
                f"{inherited_residual_volume}={inherited_input_volume}"
            ),
            "source_seam_2D_half_open_owner": "E",
            "adjacent_N_or_S_representation_excluded": True,
        },
        "C0_C1_surface_taxonomy": {
            "surface_record_count": len(surface_summaries),
            "surface_kind_counts": dict(sorted(surface_kind_counts.items())),
            "centered_C0_sign_counts": {
                f"{kind}:{sign}": count
                for (kind, sign), count
                in sorted(centered_sign_counts.items())
            },
            "regular_if_present_surface_count": regular_surface_count,
            "independently_nonempty_surface_count":
                nonempty_surface_count,
            "bounded_full_evidence_attachment_count": len(attachments),
            "bounded_full_evidence_attachments_sha256": digest(attachments),
            "bounded_full_evidence_attachments": attachments,
            "regularity_is_not_existence": True,
        },
        "two_Delta_rank_ledger": {
            "pair_outer_record_count": len(rank_rows),
            "rows_sha256": digest(rank_rows),
            "strict_rank2_if_intersection_count": strict_rank2_count,
            "intersection_existence_certified_count": 0,
            "certified_unique_1D_incidence_count": 0,
            "certified_0D_multiple_incidence_count": 0,
            "whole_parent_or_stratum_credit": 0,
        },
        "exact_residual_census": {
            "Round183_dynamic_residual_input_count": len(dynamic_inputs),
            "Round183_inherited_carrier_input_count": len(inherited_inputs),
            "Round185_dynamic_local_exact_key_count": len(dynamic_exact),
            "Round185_dimensionally_arranged_H2_outer_count":
                len(dynamic_arrangements),
            "Round185_dynamic_residual_outer_count": len(dynamic_residual),
            "Round185_inherited_local_exact_key_count":
                len(inherited_exact),
            "Round185_inherited_local_exclusion_count":
                len(inherited_excluded),
            "Round185_inherited_residual_outer_count":
                len(inherited_residual),
            "combined_remaining_residual_outer_count":
                len(dynamic_residual) + len(inherited_residual),
            "combined_remaining_exact_coordinate_outer_volume":
                str(combined_residual_volume),
            "integer_census_delta": 0,
        },
        "per_parent_partial_ledger": {
            "parent_count": len(parent_rows),
            "rows_sha256": digest(parent_rows),
            "rows": parent_rows,
            "fully_closed_live_strata": full_parents,
            "partial_live_strata": len(parent_rows) - full_parents,
            "whole_parent_or_stratum_promotions": 0,
        },
        "first_analytic_hard_blocker": {
            "first_residual_status":
                first_residual["status"] if first_residual else None,
            "first_residual_parent_key":
                first_residual["origin_parent_key"]
                if first_residual else None,
            "first_residual_terminal_path":
                first_residual["terminal_path"]
                if first_residual else None,
            "reason": (
                "remaining factor/Delta/root outers lack an independent "
                "parametric existence self-map or complete root-order "
                "separation after the bounded transverse refinement"
            ),
        },
        "strict_nonpromotion": {
            "all_new_exact_keys_are_local": True,
            "dimensionally_arranged_H2_seams_are_not_whole_parent_credit":
                True,
            "observed_point_289591_global_credit": 0,
            "inner_or_refined_box_290575_global_credit": 0,
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "continue transverse factor cells only on the bounded H2 "
            "existence residual, then centered/Krawczyk treatment of "
            "Delta/root-order and inherited collision1/source carriers"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": atlas.ctx.prec,
            "Round183_files_modified": False,
        },
    }


def safe_write(path: Path, data: bytes) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == HERE, "output directory")
    protected = {(HERE / name).resolve() for name in PINS}
    protected.add(Path(__file__).resolve())
    require(absolute.resolve(strict=False) not in protected,
            "protected output")
    if absolute.exists() or absolute.is_symlink():
        st = absolute.lstat()
        require(
            stat.S_ISREG(st.st_mode)
            and not absolute.is_symlink()
            and st.st_nlink == 1,
            "output type",
        )
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.", suffix=".tmp", dir=absolute.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    source_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
