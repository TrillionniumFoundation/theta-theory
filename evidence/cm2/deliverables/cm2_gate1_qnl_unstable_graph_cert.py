#!/usr/bin/env python3
"""Validated local unstable graph for the exact QNL period-two orbit.

This certificate works on the standard solid-collision section at the gray
normal point.  In QNL eigen-coordinates ``(x,y)`` the exact two-collision
return is written ``F=(A,B)`` with ``x`` unstable and ``y`` stable.  A
fail-closed graph-transform audit proves that there is a unique local
unstable graph

    W^u_loc(QNL) = {(x,h(x)): |x| <= r},

in the declared quadratic/Lipschitz class.  In particular, this is an
actual invariant-manifold statement, not an affine eigentangent statement.

The certificate intentionally stops after the QNL side.  It does not
validate the connector stable graph and therefore does not claim a true
heteroclinic intersection or a common magnet.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


FROZEN_CERT = Path(__file__).with_name("cm2_fixed_section_common_vertex_cert.py")
TANGENT_CERT = Path(__file__).with_name("cm2_gate1_tangent_line_matching_cert.py")
PRECISION_BITS = 300
# The interval graph transform is deliberately local enough to contain the
# QNL shooting seed |t|=1.3962e-9 while keeping direct interval dependency
# under control.  The quadratic constant is conservative; it is validated,
# not fitted from floating-point manifold samples.
RADIUS = "2e-9"
QUADRATIC_CONSTANT = "1"
LIPSCHITZ_CONSTANT = "1e-4"
SHOOTING_X = "-1.396101069259116746830594312272814e-9"


def load_frozen_certificate():
    spec = importlib.util.spec_from_file_location("cm2_v52_qnl_graph", FROZEN_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen certificate {FROZEN_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.ctx.prec = PRECISION_BITS
    return module


def load_tangent_certificate():
    spec = importlib.util.spec_from_file_location("cm2_gate1_tangent_replay", TANGENT_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load tangent replay helper {TANGENT_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@dataclass
class Jet2:
    """Two-variable, order-two interval jet.

    ``value`` is evaluated on an Arb box; ``gradient`` and ``hessian`` are
    interval enclosures over the same box.  The elementary operations below
    are the ordinary chain rules, hence they are inclusion isotone whenever
    their scalar Arb operations are defined.
    """

    value: object
    gradient: list[object]
    hessian: list[list[object]]

    @classmethod
    def constant(cls, module, value, dimension: int = 2):
        scalar = value if isinstance(value, module.arb) else module.arb(value)
        return cls(
            scalar,
            [module.arb(0) for _ in range(dimension)],
            [[module.arb(0) for _ in range(dimension)] for _ in range(dimension)],
        )

    @classmethod
    def variable(cls, module, value, index: int, dimension: int = 2):
        result = cls.constant(module, value, dimension)
        result.gradient[index] = module.arb(1)
        return result

    @property
    def dimension(self) -> int:
        return len(self.gradient)

    def coerce(self, other):
        if isinstance(other, Jet2):
            if other.dimension != self.dimension:
                raise ValueError("incompatible Jet2 dimensions")
            return other
        # Construct an exact scalar zero.  Using ``self.value-self.value``
        # here would inject the width of the current interval into every
        # scalar coercion and destroy the dependency enclosure.
        scalar_type = type(self.value)
        zero = scalar_type(0)
        scalar = other if isinstance(other, scalar_type) else scalar_type(other)
        return Jet2(
            scalar,
            [zero for _ in range(self.dimension)],
            [[zero for _ in range(self.dimension)] for _ in range(self.dimension)],
        )

    def __add__(self, other):
        other = self.coerce(other)
        return Jet2(
            self.value + other.value,
            [a + b for a, b in zip(self.gradient, other.gradient)],
            [
                [self.hessian[i][j] + other.hessian[i][j] for j in range(self.dimension)]
                for i in range(self.dimension)
            ],
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet2(
            -self.value,
            [-entry for entry in self.gradient],
            [[-entry for entry in row] for row in self.hessian],
        )

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        dimension = self.dimension
        return Jet2(
            self.value * other.value,
            [
                self.gradient[i] * other.value + self.value * other.gradient[i]
                for i in range(dimension)
            ],
            [
                [
                    self.hessian[i][j] * other.value
                    + self.gradient[i] * other.gradient[j]
                    + self.gradient[j] * other.gradient[i]
                    + self.value * other.hessian[i][j]
                    for j in range(dimension)
                ]
                for i in range(dimension)
            ],
        )

    __rmul__ = __mul__

    def compose(self, value, first, second):
        dimension = self.dimension
        return Jet2(
            value,
            [first * self.gradient[i] for i in range(dimension)],
            [
                [
                    first * self.hessian[i][j]
                    + second * self.gradient[i] * self.gradient[j]
                    for j in range(dimension)
                ]
                for i in range(dimension)
            ],
        )

    def inverse(self):
        if self.value.contains(0):
            raise RuntimeError(f"Jet2 inverse denominator may vanish: {self.value}")
        first = -1 / (self.value * self.value)
        second = 2 / (self.value * self.value * self.value)
        return self.compose(1 / self.value, first, second)

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def sqrt(self):
        if not self.value > 0:
            raise RuntimeError(f"Jet2 square-root argument is not positive: {self.value}")
        root = self.value.sqrt()
        return self.compose(root, 1 / (2 * root), -1 / (4 * root * root * root))

    def sin(self):
        return self.compose(self.value.sin(), self.value.cos(), -self.value.sin())

    def cos(self):
        return self.compose(self.value.cos(), -self.value.sin(), -self.value.cos())


def jet_dot(left: tuple[Jet2, Jet2], right: tuple[Jet2, Jet2]) -> Jet2:
    return left[0] * right[0] + left[1] * right[1]


def jet_atan2(module, y: Jet2, x: Jet2) -> Jet2:
    """Order-two chain rule for atan2(y,x), away from the origin."""

    radius2 = x.value * x.value + y.value * y.value
    if not radius2 > 0:
        raise RuntimeError(f"atan2 radius may vanish: {radius2}")
    radius4 = radius2 * radius2
    gx = -y.value / radius2
    gy = x.value / radius2
    gxx = 2 * x.value * y.value / radius4
    gxy = (y.value * y.value - x.value * x.value) / radius4
    gyy = -2 * x.value * y.value / radius4
    dimension = x.dimension
    gradient = [gx * x.gradient[i] + gy * y.gradient[i] for i in range(dimension)]
    hessian = []
    for i in range(dimension):
        row = []
        for j in range(dimension):
            row.append(
                gx * x.hessian[i][j]
                + gy * y.hessian[i][j]
                + gxx * x.gradient[i] * x.gradient[j]
                + gxy
                * (x.gradient[i] * y.gradient[j] + y.gradient[i] * x.gradient[j])
                + gyy * y.gradient[i] * y.gradient[j]
            )
        hessian.append(row)
    return Jet2(module.arb.atan2(y.value, x.value), gradient, hessian)


@dataclass
class ReturnData:
    unstable: Jet2
    stable: Jet2
    minimum_flight: object
    minimum_discriminant: object
    minimum_incidence: object
    minimum_clearance: object


def same_obstacle(left, right) -> bool:
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def clearance(module, source, target, source_obstacle, target_obstacle):
    minimum = None
    for candidate in module.all_lattice_obstacles():
        if same_obstacle(candidate, source_obstacle) or same_obstacle(
            candidate, target_obstacle
        ):
            continue
        distance_squared = module.minimum_line_segment_distance_squared(
            source, target, candidate.center
        )
        if not distance_squared > candidate.radius * candidate.radius:
            raise RuntimeError(
                "an unintended obstacle may meet the QNL local flight: "
                f"{(candidate.kind, candidate.i, candidate.j)}"
            )
        candidate_clearance = distance_squared.sqrt() - candidate.radius
        minimum = (
            candidate_clearance
            if minimum is None
            else minimum.min(candidate_clearance)
        )
    if minimum is None:
        raise RuntimeError("empty clearance enumeration")
    return minimum


def qnl_return(module, x_box, y_box) -> ReturnData:
    """Evaluate the exact G->W->G return and its first two derivatives."""

    x = Jet2.variable(module, x_box, 0)
    y = Jet2.variable(module, y_box, 1)
    sqrt_two = module.arb(2).sqrt()
    beta = (module.arb(859) - 550 * sqrt_two) / 100
    gamma = module.arb(625) * (25 - 4 * sqrt_two) / 324
    slope = (gamma / beta).sqrt()

    arclength = x + y
    momentum = slope * (x - y)
    theta = module.arb.pi() / 4 + arclength / module.R_GRAY
    normal = theta.cos(), theta.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - momentum * momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    source_obstacle = module.obstacle("G", 0, 0)
    position = (
        source_obstacle.center[0] + source_obstacle.radius * normal[0],
        source_obstacle.center[1] + source_obstacle.radius * normal[1],
    )

    minima = {"flight": None, "discriminant": None, "incidence": None, "clearance": None}
    previous_diagnostic = None
    for target_key in (("W", 0, 0), ("G", 0, 0)):
        target_obstacle = module.obstacle(*target_key)
        displacement = (
            position[0] - target_obstacle.center[0],
            position[1] - target_obstacle.center[1],
        )
        linear = jet_dot(displacement, velocity)
        offset = jet_dot(displacement, displacement) - target_obstacle.radius**2
        discriminant = linear * linear - offset
        if not discriminant.value > 0:
            raise RuntimeError(
                f"QNL target discriminant may vanish for {target_key}: "
                f"linear={linear.value}, offset={offset.value}, "
                f"discriminant={discriminant.value}, "
                f"position={(position[0].value, position[1].value)}, "
                f"velocity={(velocity[0].value, velocity[1].value)}, "
                f"previous={previous_diagnostic}"
            )
        flight = -linear - discriminant.sqrt()
        if not flight.value > 0:
            raise RuntimeError(f"QNL flight may be nonpositive: {flight.value}")
        impact = (
            position[0] + flight * velocity[0],
            position[1] + flight * velocity[1],
        )
        for endpoint in (position, impact):
            for coordinate in endpoint:
                if not coordinate.value > 0 or not coordinate.value < 1:
                    raise RuntimeError(
                        "QNL graph domain leaves the open fundamental square: "
                        f"{coordinate.value}"
                    )
        normal = (
            (impact[0] - target_obstacle.center[0]) / target_obstacle.radius,
            (impact[1] - target_obstacle.center[1]) / target_obstacle.radius,
        )
        incoming = -jet_dot(velocity, normal)
        if not incoming.value > 0:
            raise RuntimeError(f"QNL incidence may vanish: {incoming.value}")
        segment_clearance = clearance(
            module,
            (position[0].value, position[1].value),
            (impact[0].value, impact[1].value),
            source_obstacle,
            target_obstacle,
        )
        values = {
            "flight": flight.value,
            "discriminant": discriminant.value,
            "incidence": incoming.value,
            "clearance": segment_clearance,
        }
        for name, value in values.items():
            minima[name] = value if minima[name] is None else minima[name].min(value)

        reflected = (
            velocity[0] + 2 * incoming * normal[0],
            velocity[1] + 2 * incoming * normal[1],
        )
        previous_diagnostic = {
            "linear": linear.value,
            "discriminant": discriminant.value,
            "flight": flight.value,
            "normal": (normal[0].value, normal[1].value),
            "incoming": incoming.value,
            "reflected": (reflected[0].value, reflected[1].value),
        }
        # Diagnostics are retained in failure messages rather than printed on
        # successful certificate runs.
        position = impact
        velocity = reflected
        source_obstacle = target_obstacle

    final_normal = (
        position[0] / module.R_GRAY,
        position[1] / module.R_GRAY,
    )
    final_theta = jet_atan2(module, final_normal[1], final_normal[0])
    final_tangent = -final_normal[1], final_normal[0]
    final_momentum = jet_dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_theta - module.arb.pi() / 4)
    unstable = (final_arclength + final_momentum / slope) / 2
    stable = (final_arclength - final_momentum / slope) / 2
    return ReturnData(
        unstable,
        stable,
        minima["flight"],
        minima["discriminant"],
        minima["incidence"],
        minima["clearance"],
    )


def certify_graph_transform(module):
    r = module.arb(RADIUS)
    c = module.arb(QUADRATIC_CONSTANT)
    lipschitz = module.arb(LIPSCHITZ_CONSTANT)
    ordinate_radius = (c * r * r).str(90, radius=False, more=True)
    domain = qnl_return(
        module, module.arb(0, RADIUS), module.arb(0, ordinate_radius)
    )
    center = qnl_return(module, module.arb(0), module.arb(0))

    a_x = domain.unstable.gradient[0]
    a_y = domain.unstable.gradient[1]
    b_x = domain.stable.gradient[0]
    b_y = domain.stable.gradient[1]
    derivative_determinant = a_x * b_y - a_y * b_x
    m_a = a_x - abs(a_y) * lipschitz
    image_lipschitz = (abs(b_x) + abs(b_y) * lipschitz) / m_a
    contraction = abs(b_y) + (
        abs(b_x) + lipschitz * abs(b_y)
    ) * abs(a_y) / m_a

    # Taylor's theorem at the fixed point.  D_x B(0)=0 and D_y B(0)=mu.
    hessian = domain.stable.hessian
    quadratic_remainder = (
        abs(hessian[0][0])
        + 2 * abs(hessian[0][1]) * c * r
        + abs(hessian[1][1]) * c * c * r * r
    ) / 2
    quadratic_image = (
        abs(center.stable.gradient[1]) * c + quadratic_remainder
    ) / (m_a * m_a)

    sqrt_two = module.arb(2).sqrt()
    alpha = (module.arb(661) - 325 * sqrt_two) / 36
    beta = (module.arb(859) - 550 * sqrt_two) / 100
    gamma = module.arb(625) * (25 - 4 * sqrt_two) / 324
    eigen_root = (beta * gamma).sqrt()
    exact_unstable_multiplier = alpha + eigen_root
    exact_stable_multiplier = alpha - eigen_root

    if not center.unstable.value.contains(0) or not center.stable.value.contains(0):
        raise RuntimeError("QNL center does not return to the origin")
    if not center.unstable.gradient[0] > 11:
        raise RuntimeError("QNL unstable center multiplier is not >11")
    if not center.unstable.gradient[0].contains(exact_unstable_multiplier):
        raise RuntimeError("Jet2 unstable multiplier misses the frozen exact value")
    if not center.stable.gradient[1].contains(exact_stable_multiplier):
        raise RuntimeError("Jet2 stable multiplier misses the frozen exact value")
    if not (
        center.stable.gradient[1] > module.arb(9) / 100
        and center.stable.gradient[1] < module.arb(91) / 1000
    ):
        raise RuntimeError("QNL stable center multiplier leaves (0.09,0.091)")
    if not abs(center.stable.gradient[0]) < module.arb("1e-70"):
        raise RuntimeError("QNL center D_xB is not sharply zero")
    if not abs(center.unstable.gradient[1]) < module.arb("1e-70"):
        raise RuntimeError("QNL center D_yA is not sharply zero")
    if not derivative_determinant > 0:
        raise RuntimeError(
            f"QNL return may fail to be a local diffeomorphism: {derivative_determinant}"
        )
    if not center.stable.gradient[0].contains(0):
        raise RuntimeError(f"D_x B(0) is not zero: {center.stable.gradient[0]}")
    if not center.unstable.gradient[1].contains(0):
        raise RuntimeError(f"D_y A(0) is not zero: {center.unstable.gradient[1]}")
    if not m_a > 1:
        raise RuntimeError(f"unstable graph projection does not cover: m_A={m_a}")
    if not image_lipschitz < lipschitz:
        raise RuntimeError(
            f"graph transform does not preserve derivative cone: {image_lipschitz}"
        )
    if not contraction < 1:
        raise RuntimeError(f"graph transform is not a contraction: {contraction}")
    if not quadratic_image < c:
        raise RuntimeError(
            f"graph transform does not preserve quadratic tube: {quadratic_image}"
        )
    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(9) / 10,
        "clearance": module.arb(1) / 5,
    }
    physical = {
        "flight": domain.minimum_flight,
        "discriminant": domain.minimum_discriminant,
        "incidence": domain.minimum_incidence,
        "clearance": domain.minimum_clearance,
    }
    for name, threshold in thresholds.items():
        if not physical[name] > threshold:
            raise RuntimeError(
                f"local QNL physical margin {name} fails: {physical[name]}"
            )
    # Every certified endpoint is in (0,1)^2.  A gray or white lift with an
    # index outside [-3,3] therefore has a coordinate gap at least three;
    # subtracting the largest radius 9/25 still leaves more than two units.
    if not module.arb(3) - module.R_GRAY > 2:
        raise RuntimeError("omitted-lift exhaustion inequality failed")

    print("QNL_LOCAL_UNSTABLE_GRAPH: CERTIFIED")
    print(f"  arb_precision_bits={module.ctx.prec}")
    print(f"  eigen_domain_radius={r}")
    print(f"  quadratic_remainder_bound=|h(x)|<={c}*x^2")
    print(f"  derivative_cone_bound=|h'(x)|<={lipschitz}")
    print(f"  D_F_center={module.arb_mat([center.unstable.gradient, center.stable.gradient])}")
    print(f"  D_F_domain={module.arb_mat([domain.unstable.gradient, domain.stable.gradient])}")
    print(f"  det_D_F_domain={derivative_determinant}")
    print(f"  unstable_projection_lower={m_a}")
    print(f"  graph_transform_lipschitz_image={image_lipschitz}")
    print(f"  graph_transform_contraction={contraction}")
    print(f"  graph_transform_quadratic_image={quadratic_image}")
    print(f"  B_hessian_domain={module.arb_mat(hessian)}")
    for name, value in physical.items():
        print(f"  minimum_{name}={value}")
    print("  physical_word=(G(0,0),W(0,0),G(0,0))")
    print("  lift_exhaustion=[-3,3]^2 inherited from frozen lattice registry")
    return r, c, lipschitz


def certify_ten_collision_graph_tube_replay(module, r, c):
    """Replay the full QNL graph tube through the frozen ten-collision word.

    The graph theorem only gives a quadratic enclosure for the unknown exact
    ordinate.  This check propagates the *whole* ordinate interval, so it is
    a legitimate physical-word audit.  Its terminal box is intentionally not
    used as a heteroclinic matching box: ordinary interval wrapping makes it
    far too wide for that purpose.
    """

    tangent = load_tangent_certificate()
    x = module.arb(SHOOTING_X)
    if not abs(x) < r:
        raise RuntimeError(f"shooting parameter leaves graph domain: {x} versus {r}")
    y_radius = c * abs(x) * abs(x)
    y = module.arb(0, y_radius.str(90, radius=False, more=True))
    sqrt_two = module.arb(2).sqrt()
    beta = (module.arb(859) - 550 * sqrt_two) / 100
    gamma = module.arb(625) * (25 - 4 * sqrt_two) / 324
    slope = (gamma / beta).sqrt()
    x_dual = module.Dual(x, dimension=0)
    y_dual = module.Dual(y, dimension=0)
    theta = module.Dual(module.arb.pi() / 4, dimension=0) + (
        x_dual + y_dual
    ) / module.R_GRAY
    momentum = slope * (x_dual - y_dual)
    output = tangent.propagate(
        module,
        "G",
        theta,
        momentum,
        tangent.QNL_FORWARD_WORD,
    )
    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(1) / 2,
        "clearance": module.arb(1) / 10,
    }
    for name, threshold in thresholds.items():
        if not output.minima[name] > threshold:
            raise RuntimeError(
                f"ten-collision graph-tube margin {name} fails: {output.minima[name]}"
            )
    print("QNL_GRAPH_TUBE_TEN_COLLISION_REPLAY: CERTIFIED")
    print(f"  shooting_x={x}")
    print(f"  graph_ordinate_tube={y}")
    print(f"  terminal_theta_box={output.theta.value}")
    print(f"  terminal_momentum_box={output.momentum.value}")
    for name, value in output.minima.items():
        print(f"  replay_minimum_{name}={value}")
    print(f"  replay_word={tangent.QNL_FORWARD_WORD}")
    print("  warning=terminal interval width is a wrapping bound, not a matching enclosure")


def main() -> int:
    module = load_frozen_certificate()
    try:
        r, c, _ = certify_graph_transform(module)
        certify_ten_collision_graph_tube_replay(module, r, c)
    except Exception as exc:
        print(f"QNL_LOCAL_UNSTABLE_GRAPH: FAILED: {exc}")
        print("TRUE_HETEROCLINIC_MATCHING: NOT CERTIFIED")
        print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
        return 1
    print("QNL_EIGENTANGENT_UPGRADE: CERTIFIED")
    print("  scope=actual QNL local unstable manifold only")
    print("CONNECTOR_LOCAL_STABLE_GRAPH_IN_QNL_CERT: NOT CERTIFIED")
    print("TRUE_HETEROCLINIC_MATCHING: NOT CERTIFIED")
    print("  reason=connector stable graph and true two-graph Krawczyk remain open")
    print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
