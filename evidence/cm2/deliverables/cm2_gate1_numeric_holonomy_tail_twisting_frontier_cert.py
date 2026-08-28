#!/usr/bin/env python3
"""Numerical QNL holonomy tails and selected homoclinic twisting wedges.

This certificate is independent of the frozen immutable-orbit stack.  It
replays a very deep pre-tail of the selected reversible homoclinic orbit,
encloses the finite gauge-normalised excursion, and supplies numerical
majorants for both remaining infinite products.  Every matrix is written in
the exact canonical QNL eigencoordinates used by the frozen resonance proof;
the graph coordinates used by the physical replay are converted explicitly.

The result is deliberately local.  It certifies the four eigen-axis wedges
of this one selected QNL loop, but it does not manufacture a global faithful
coding, all-plaque Holder holonomies, or Butler--Park class H.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEGREE = 4

IMMUTABLE_MANIFEST = (
    HERE / "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json"
)
IMMUTABLE_CERT = HERE / "cm2_gate1_immutable_homoclinic_plaque_entry_frontier_cert.py"
COMPACT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
RESONANCE_MANIFEST = (
    HERE / "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
)
RESONANCE_CERT = HERE / "cm2_gate1_canonical_holonomy_resonance_cert.py"
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TRUE_GRAPH_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
QNL_GRAPH_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_GRAPH_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"

EXPECTED_HASHES = {
    IMMUTABLE_MANIFEST.name: "e583a7c0f43f291f92ffb7dc15a4888bda6702340f3209bfd7ec224101df841c",
    IMMUTABLE_CERT.name: "22e4fca1ff76baef390c40850243b87ac553fa81621fbbac4c2e02195650d3d3",
    COMPACT_MANIFEST.name: "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    RESONANCE_MANIFEST.name: "56dd0e6783e4b37feb2c9c03db67d23cc4c49ad33f0b98631c23f131dc6490b2",
    RESONANCE_CERT.name: "999a2851352944e7611b88076aaf4a4af8b1e4b8f54a12082dfa1f36747d4b22",
    FULL_CROSS_CERT.name: "1eb603891c13e3615f74b5b25151dba3f8dab7933811c2ffeb85a3bf22283942",
    TRUE_GRAPH_CERT.name: "ea90579306b5fd3064cba500ac916cbc5ca8f21e89e8b7863fb711f8a547f4e7",
    QNL_GRAPH_CERT.name: "0945b084263e2f48d4cc8521e3e1f24986d28d057ec62de829a18471b8e46fa9",
    CONNECTOR_GRAPH_CERT.name: "7440b97ad97fc876dbc9d42c56cb9dc1d3239f3eb0d95c30e501f0115e73b77f",
    TANGENT_CERT.name: "d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1",
    SHADOW_CERT.name: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
}

PRECISION_BITS = 5000
TAIL_DEPTH = 260
ROOT_X_CENTER = (
    "-8.293762194329601963437426816426218129136992992541213302685879950938746933679495882046154825340036010743174892558684126391544694649846885859088067348205641235289978138183961800037966087993611724941297924070080341715788907910727582613670011086480203974435489036750325333647236440100451527329092540147809133409697742230321803864868331258410153702375806605390149768919195276305867418145849332101778666361e-15"
)
DEEP_ROOT_RADIUS = "1e-400"
GAUGE_CHART_RADIUS = "1e-10"
GAUGE_CORE_RADIUS = "1e-12"
INCREMENT_MAJORANT = "1e80"
BACKWARD_CONTRACTION = "0.091"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def audit_frozen_inputs() -> tuple[dict, dict, dict]:
    for name, expected in EXPECTED_HASHES.items():
        actual = sha256_path(HERE / name)
        if actual != expected:
            raise RuntimeError(
                f"frozen dependency hash changed: {name}: {actual} != {expected}"
            )
    immutable = json.loads(IMMUTABLE_MANIFEST.read_text(encoding="utf-8"))
    compact = json.loads(COMPACT_MANIFEST.read_text(encoding="utf-8"))
    resonance = json.loads(RESONANCE_MANIFEST.read_text(encoding="utf-8"))
    if immutable["schema"] != (
        "cm2.gate1.immutable-homoclinic-plaque-entry-frontier.manifest.v1"
    ):
        raise RuntimeError("immutable homoclinic dependency schema changed")
    if compact["schema"] != (
        "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.manifest.v1"
    ):
        raise RuntimeError("compact gauge dependency schema changed")
    if resonance["schema"] != "cm2.gate1.canonical-holonomy-resonance.v1":
        raise RuntimeError("canonical resonance dependency schema changed")
    orbit = immutable["result"]["scope_limits"]
    if not orbit["selected_immutable_regular_phase_aligned_qnl_homoclinic_orbit"]:
        raise RuntimeError("selected immutable homoclinic orbit disappeared")
    if orbit["four_twisting_wedges"]:
        raise RuntimeError("immutable predecessor unexpectedly claims twisting")
    local = compact["result"]["scope_limits"]
    if not local["stable_all_pairs_on_one_local_qnl_plaque"]:
        raise RuntimeError("local stable compact-gauge holonomies disappeared")
    if not local["unstable_all_pairs_on_one_local_qnl_plaque"]:
        raise RuntimeError("local unstable compact-gauge holonomies disappeared")
    if resonance["exact_qnl_jet"]["F2_xyy_over_mu"] != "-325/72 exactly":
        raise RuntimeError("canonical exact cubic resonance changed")
    return immutable, compact, resonance


def mat_mul(module, left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(2)), module.arb(0))
            for j in range(2)
        ]
        for i in range(2)
    ]


def mat_diag(module, first, second):
    return [[first, module.arb(0)], [module.arb(0), second]]


def mat_inverse_det_one(module, matrix):
    return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]


def mat_infinity_norm(module, matrix):
    return max(
        sum((abs(entry) for entry in row), module.arb(0)) for row in matrix
    )


def arb_text(value, digits: int = 60) -> str:
    return value.str(digits, radius=True, more=True)


def point_decimal(value, digits: int = 800) -> str:
    return value.mid().str(digits, radius=False, more=True)


def symmetric_ball(module, radius):
    radius = abs(radius).abs_upper()
    text = (4 * radius).str(300, radius=False, more=True)
    ball = module.arb(0, text)
    if not ball.contains(radius) or not ball.contains(-radius):
        raise RuntimeError("failed to construct outward symmetric Arb ball")
    return ball


@dataclass
class Jet4:
    """Two-variable normalized Taylor jet with interval coefficients."""

    module: object
    terms: dict[tuple[int, int], object]

    def __post_init__(self) -> None:
        self.terms = {
            degree: coefficient
            for degree, coefficient in self.terms.items()
            if sum(degree) <= DEGREE
        }

    @classmethod
    def constant(cls, module, value):
        scalar = value if isinstance(value, module.arb) else module.arb(value)
        return cls(module, {(0, 0): scalar})

    @classmethod
    def variable(cls, module, value, index: int):
        result = cls.constant(module, value)
        result.terms[(1, 0) if index == 0 else (0, 1)] = module.arb(1)
        return result

    def coefficient(self, degree: tuple[int, int]):
        return self.terms.get(degree, self.module.arb(0))

    @property
    def value(self):
        return self.coefficient((0, 0))

    def coerce(self, other):
        return other if isinstance(other, Jet4) else Jet4.constant(self.module, other)

    def __add__(self, other):
        other = self.coerce(other)
        terms = dict(self.terms)
        for degree, coefficient in other.terms.items():
            terms[degree] = terms.get(degree, self.module.arb(0)) + coefficient
        return Jet4(self.module, terms)

    __radd__ = __add__

    def __neg__(self):
        return Jet4(self.module, {degree: -value for degree, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms: dict[tuple[int, int], object] = {}
        for (i, j), left in self.terms.items():
            for (k, l), right in other.terms.items():
                degree = (i + k, j + l)
                if sum(degree) <= DEGREE:
                    terms[degree] = terms.get(degree, self.module.arb(0)) + left * right
        return Jet4(self.module, terms)

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = Jet4.constant(self.module, 1)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power >>= 1
        return result

    def unary(self, coefficients):
        # Remove the interval constant structurally.  Subtracting it as an
        # Arb value would lose dependency and inject its radius into u.
        u = Jet4(
            self.module,
            {degree: value for degree, value in self.terms.items() if degree != (0, 0)},
        )
        result = Jet4.constant(self.module, coefficients[0])
        power = Jet4.constant(self.module, 1)
        for order in range(1, DEGREE + 1):
            power = power * u
            result = result + power * coefficients[order]
        return result

    def inverse(self):
        c = self.value
        if c.contains(0):
            raise RuntimeError(f"Jet4 inverse denominator may vanish: {c}")
        return self.unary([1 / c, -1 / c**2, 1 / c**3, -1 / c**4, 1 / c**5])

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def sqrt(self):
        if not self.value > 0:
            raise RuntimeError(f"Jet4 square root may vanish: {self.value}")
        r = self.value.sqrt()
        return self.unary([r, 1 / (2 * r), -1 / (8 * r**3), 1 / (16 * r**5), -5 / (128 * r**7)])

    def sin(self):
        c = self.value
        return self.unary([c.sin(), c.cos(), -c.sin() / 2, -c.cos() / 6, c.sin() / 24])

    def cos(self):
        c = self.value
        return self.unary([c.cos(), -c.sin(), -c.cos() / 2, c.sin() / 6, c.cos() / 24])

    def atan(self):
        c = self.value
        d = 1 + c * c
        return self.unary([
            c.atan(),
            1 / d,
            -c / d**2,
            (3 * c * c - 1) / (3 * d**3),
            c * (1 - c * c) / d**4,
        ])


def jet_dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def qnl_return_jet4(module, slope, x_box, y_box):
    x = Jet4.variable(module, x_box, 0)
    y = Jet4.variable(module, y_box, 1)
    arclength = x + y
    momentum = slope * (x - y)
    theta = Jet4.constant(module, module.arb.pi() / 4) + arclength / module.R_GRAY
    normal = theta.cos(), theta.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - momentum * momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    source = module.obstacle("G", 0, 0)
    position = (
        source.center[0] + source.radius * normal[0],
        source.center[1] + source.radius * normal[1],
    )
    for target_key in (("W", 0, 0), ("G", 0, 0)):
        target = module.obstacle(*target_key)
        displacement = (
            position[0] - target.center[0],
            position[1] - target.center[1],
        )
        linear = jet_dot(displacement, velocity)
        offset = jet_dot(displacement, displacement) - target.radius**2
        discriminant = linear * linear - offset
        flight = -linear - discriminant.sqrt()
        impact = (
            position[0] + flight * velocity[0],
            position[1] + flight * velocity[1],
        )
        target_normal = (
            (impact[0] - target.center[0]) / target.radius,
            (impact[1] - target.center[1]) / target.radius,
        )
        incidence = -jet_dot(velocity, target_normal)
        velocity = (
            velocity[0] + 2 * incidence * target_normal[0],
            velocity[1] + 2 * incidence * target_normal[1],
        )
        position = impact
        source = target
    ratio = target_normal[1] / target_normal[0]
    output_theta = ratio.atan()
    output_tangent = -target_normal[1], target_normal[0]
    output_momentum = jet_dot(velocity, output_tangent)
    output_arclength = module.R_GRAY * (
        output_theta - Jet4.constant(module, module.arb.pi() / 4)
    )
    return (
        (output_arclength + output_momentum / slope) / 2,
        (output_arclength - output_momentum / slope) / 2,
    )


def derivative_bound(jet: Jet4, total_degree: int):
    result = jet.module.arb(0)
    for i in range(total_degree + 1):
        j = total_degree - i
        value = abs(jet.coefficient((i, j))) * math.factorial(i) * math.factorial(j)
        result = result.max(value)
    return result


def canonicalise_graph_jet(jet: Jet4, graph_to_canonical, output_scale):
    return Jet4(
        jet.module,
        {
            (i, j): coefficient * output_scale / graph_to_canonical**j
            for (i, j), coefficient in jet.terms.items()
        },
    )


def canonical_qnl_jets(module, slope, x_box, y_box):
    # The physical replay uses s=x_g+y_g, p=k(x_g-y_g).  The exact resonance
    # source uses x=x_g, y=-2*k*y_g.  This diagonal conversion is essential:
    # applying the logarithmic gauge directly in graph coordinates would use
    # the wrong cubic coefficient.
    scale = -2 * slope
    graph = qnl_return_jet4(module, slope, x_box, y_box / scale)
    return (
        canonicalise_graph_jet(graph[0], scale, module.arb(1)),
        canonicalise_graph_jet(graph[1], scale, scale),
    )


def replay_rectangle(
    full_cross,
    parent,
    qnl,
    connector,
    tangent,
    module,
    slope,
    word,
    center,
    radius,
    transverse,
):
    return full_cross.replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=center,
        parameter_radius=radius,
        transverse_radius=transverse,
        base_angle=module.arb.pi() / 4,
        slope=slope,
        word=word,
    )


def terminal_graph_coordinates(module, slope, replay):
    theta, momentum = replay.value_box(module)
    arclength = module.R_GRAY * (theta - module.arb.pi() / 4)
    return (
        (arclength + momentum / slope) / 2,
        (arclength - momentum / slope) / 2,
    )


def refine_deep_center(
    full_cross,
    parent,
    qnl,
    connector,
    tangent,
    module,
    slope,
    half_word,
    unstable_multiplier,
):
    center = module.arb(ROOT_X_CENTER) / unstable_multiplier**TAIL_DEPTH
    for _ in range(4):
        replay = replay_rectangle(
            full_cross,
            parent,
            qnl,
            connector,
            tangent,
            module,
            slope,
            half_word,
            center,
            module.arb(0),
            module.arb(0),
        )
        residual = replay.value_box(module)[1]
        derivative = replay.derivative_box(module)[1][0]
        if derivative.contains(0):
            raise RuntimeError("deep shooting Newton derivative may vanish")
        center = module.arb(point_decimal(center - residual / derivative))
    return center


def gauge_t(module, coefficient, value):
    if not value.contains(0):
        return coefficient * value * value * abs(value).log()
    upper = abs(value).abs_upper()
    if upper == 0:
        return module.arb(0)
    radius = abs(coefficient) * upper * upper * abs(upper.log())
    return symmetric_ball(module, radius)


def gauge_matrix(module, coefficient, x_value, y_value):
    tx = gauge_t(module, coefficient, x_value)
    ty = gauge_t(module, coefficient, y_value)
    return [[1 + tx * ty, tx], [ty, module.arb(1)]]


def analytic_increment_majorant(module, slope, unstable_multiplier, stable_multiplier):
    radius = module.arb(GAUGE_CHART_RADIUS)
    outputs = canonical_qnl_jets(
        module,
        slope,
        module.arb(0, GAUGE_CHART_RADIUS),
        module.arb(0, GAUGE_CHART_RADIUS),
    )
    origin = canonical_qnl_jets(module, slope, module.arb(0), module.arb(0))
    f1, f2 = origin
    if not f1.coefficient((1, 0)).contains(unstable_multiplier):
        raise RuntimeError("canonical Jet4 misses the unstable multiplier")
    if not f2.coefficient((0, 1)).contains(stable_multiplier):
        raise RuntimeError("canonical Jet4 misses the stable multiplier")
    if not abs(f1.coefficient((0, 1))) < module.arb("1e-1000"):
        raise RuntimeError("canonical off-diagonal linear jet is not zero")
    if not abs(f2.coefficient((1, 0))) < module.arb("1e-1000"):
        raise RuntimeError("canonical off-diagonal linear jet is not zero")
    for output in origin:
        for degree in ((2, 0), (1, 1), (0, 2)):
            if not abs(output.coefficient(degree)) < module.arb("1e-1000"):
                raise RuntimeError(f"canonical quadratic jet is not zero: {degree}")

    gu = f1.coefficient((2, 1))
    gs = f2.coefficient((1, 2))
    expected = module.arb(325) / 144
    if not (gu / unstable_multiplier).contains(expected):
        raise RuntimeError("unstable exact resonance does not equal 325/144")
    if not (gs / stable_multiplier).contains(-expected):
        raise RuntimeError("stable exact resonance does not equal -325/144")

    third = max(derivative_bound(output, 3) for output in outputs)
    fourth = max(derivative_bound(output, 4) for output in outputs)
    graph_constant = 2 * abs(slope)
    if not graph_constant < 14:
        raise RuntimeError("canonical invariant-graph scaling is not <14")
    if not unstable_multiplier < 12:
        raise RuntimeError("QNL unstable multiplier is not <12")
    gauge_coefficient = -module.arb(325) / (144 * stable_multiplier.log())
    if not abs(gauge_coefficient) < 1:
        raise RuntimeError("logarithmic gauge coefficient is not <1")

    # Explicit Taylor categories.  Put |dominant|=r and
    # |subordinate|<=G*r^2.  Since every quadratic base-map derivative
    # vanishes, Taylor's theorem gives the first two constants below.
    # Expanding the critical derivative to quadratic order singles out
    # g_u*r^2 (or g_s*r^2); all cross terms contain the subordinate graph
    # coordinate and the remaining Taylor term uses D^4 F.
    l1_factor = 1 + graph_constant * radius
    base_cubic = third * l1_factor**3 / 6
    derivative_quadratic = third * l1_factor**2 / 2
    critical_cubic = (
        third * (graph_constant + graph_constant**2 * radius / 2)
        + fourth * l1_factor**3 / 6
    )
    dominant_image = unstable_multiplier + base_cubic * radius**2
    if not dominant_image * radius < module.arb("1e-8"):
        raise RuntimeError("Taylor image is too large for the log-gauge bounds")
    image_log_factor = 1 + abs(dominant_image.log())
    gauge_composition = (
        abs(gauge_coefficient) * dominant_image**2 * image_log_factor
    )
    gauge_difference = (
        abs(gauge_coefficient)
        * dominant_image
        * (3 + 2 * abs(dominant_image.log()))
        * base_cubic
    )

    # For the unstable critical entry the exact expansion is
    #   b+a*t(x)-t(X)*(c*t(x)+d).
    # Subtracting g_u*x^2 and applying
    #   g_u*x^2+lambda*t(x)-mu*t(lambda*x)=0
    # leaves precisely the five classes below.  The stable E_21 formula is
    # its reversible counterpart; extra B_u/B_s cross products, including
    # the five-factor t(X)t(Y)c t(x)t(y) term, are covered by the final
    # finite-product ledger.
    log_at_radius = 1 + abs(radius.log())
    unstable_critical_explicit = (
        critical_cubic
        + stable_multiplier * gauge_difference * radius
        + derivative_quadratic * abs(gauge_coefficient) * radius
        + gauge_composition * derivative_quadratic * radius
        + gauge_composition
        * derivative_quadratic
        * abs(gauge_coefficient)
        * radius**3
        * log_at_radius
    )

    # A norm bound for every noncritical entry follows without cancellation:
    # E=DF-A is O(r^2), while B-I and B^-1-I are O(r^2 L).  The coefficient
    # below is the exact submultiplicative expansion of
    # B(Fz)^-1 E B(z)+(B(Fz)^-1 A B(z)-A).
    shear_coefficient = max(abs(gauge_coefficient), gauge_composition)
    gauge_deviation = (
        2 * shear_coefficient
        + shear_coefficient**2 * radius**2 * log_at_radius
    )
    gauge_norm = 1 + gauge_deviation * radius**2 * log_at_radius
    noncritical_explicit = (
        gauge_norm**2 * 2 * derivative_quadratic
        + gauge_norm * unstable_multiplier * gauge_deviation
        + unstable_multiplier * gauge_deviation
    )

    # Expanding B_u B_s, its exact inverse, DF and the reversible stable
    # counterpart produces fewer than 2^12 scalar monomials.  The largest
    # degree is five: the stable (2,1) expansion contains the explicit term
    # t(X)*t(Y)*c*t(x)*t(y).  No other entry has more factors after the exact
    # cubic terms are removed.  Thus this is a literal finite-product
    # domination, not an
    # asymptotic O-constant.  Replacing r by the chart radius only decreases
    # every discarded positive power r and r*L(r).
    category_sum = (
        1
        + base_cubic
        + derivative_quadratic
        + critical_cubic
        + gauge_composition
        + gauge_difference
        + unstable_critical_explicit
        + noncritical_explicit
        + graph_constant
        + unstable_multiplier
        + 1 / stable_multiplier
    )
    derived = module.arb(2) ** 12 * category_sum**5
    declared = module.arb(INCREMENT_MAJORANT)
    if not derived < declared:
        raise RuntimeError(
            f"declared transformed-increment majorant is too small: {derived}"
        )
    return {
        "third_derivative_bound": third,
        "fourth_derivative_bound": fourth,
        "graph_constant": graph_constant,
        "gauge_coefficient": gauge_coefficient,
        "base_cubic_remainder": base_cubic,
        "derivative_quadratic_remainder": derivative_quadratic,
        "critical_cubic_remainder": critical_cubic,
        "gauge_composition_ledger": gauge_composition,
        "gauge_difference_ledger": gauge_difference,
        "unstable_critical_explicit": unstable_critical_explicit,
        "noncritical_explicit": noncritical_explicit,
        "finite_product_monomial_count_bound": 2**12,
        "finite_product_factor_degree_bound": 5,
        "derived_majorant": derived,
        "declared_majorant": declared,
        "critical_bound": "|delta_12|,|delta_21| <= C*r^3*(1+|log r|)",
        "noncritical_bound": "|delta_ij| <= C*r^2*(1+|log r|)",
        "chart_radius": radius,
    }


def certify_numeric_loop():
    immutable, compact, resonance = audit_frozen_inputs()
    full_cross = load(FULL_CROSS_CERT, "cm2_g1_tail_full_cross")
    parent = load(TRUE_GRAPH_CERT, "cm2_g1_tail_parent")
    qnl = load(QNL_GRAPH_CERT, "cm2_g1_tail_qnl")
    connector = load(CONNECTOR_GRAPH_CERT, "cm2_g1_tail_connector")
    tangent = load(TANGENT_CERT, "cm2_g1_tail_tangent")
    shadow = load(SHADOW_CERT, "cm2_g1_tail_shadow")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)
    _, slope, _ = tangent.setup_fixed_data(module)

    graph_radius, graph_quadratic, graph_lipschitz = qnl.certify_graph_transform(module)
    if graph_quadratic != module.arb(1) or graph_lipschitz != module.arb("1e-4"):
        raise RuntimeError("frozen invariant-graph bounds changed")
    graph_domain = qnl.qnl_return(
        module,
        module.arb(0, qnl.RADIUS),
        module.arb(0, (graph_quadratic * graph_radius**2).str(100, radius=False, more=True)),
    )
    projection_expansion = (
        graph_domain.unstable.gradient[0]
        - abs(graph_domain.unstable.gradient[1]) * graph_lipschitz
    )
    backward_q = module.arb(BACKWARD_CONTRACTION)
    if not 1 / projection_expansion < backward_q:
        raise RuntimeError("declared inverse graph contraction is too small")

    exact_origin = canonical_qnl_jets(module, slope, module.arb(0), module.arb(0))
    unstable = exact_origin[0].coefficient((1, 0))
    stable = exact_origin[1].coefficient((0, 1))
    if not abs(unstable * stable - 1) < module.arb("1e-1000"):
        raise RuntimeError("canonical QNL multipliers lost reciprocal identity")

    q5 = tuple(tangent.QNL_FORWARD_WORD)
    connector_word = tuple(tangent.CONNECTOR_REVERSE_FORWARD_WORD)
    qnl_return_word = q5[:2]
    base_half = q5 * 2 + connector_word * 2
    deep_half = qnl_return_word * TAIL_DEPTH + base_half
    if len(qnl_return_word) != 2 or len(base_half) != 48:
        raise RuntimeError("frozen QNL or homoclinic collision count changed")
    if len(deep_half) != 2 * TAIL_DEPTH + 48:
        raise RuntimeError("deep half-word collision count changed")

    center = refine_deep_center(
        full_cross,
        parent,
        qnl,
        connector,
        tangent,
        module,
        slope,
        deep_half,
        unstable,
    )
    root_radius = module.arb(DEEP_ROOT_RADIUS)
    graph_tube = (abs(center) + root_radius) ** 2
    left = replay_rectangle(
        full_cross, parent, qnl, connector, tangent, module, slope, deep_half,
        center - root_radius, module.arb(0), graph_tube,
    )
    right = replay_rectangle(
        full_cross, parent, qnl, connector, tangent, module, slope, deep_half,
        center + root_radius, module.arb(0), graph_tube,
    )
    whole = replay_rectangle(
        full_cross, parent, qnl, connector, tangent, module, slope, deep_half,
        center, root_radius, graph_tube,
    )
    left_momentum = left.value_box(module)[1]
    right_momentum = right.value_box(module)[1]
    derivative = whole.derivative_box(module)[1]
    along_graph = derivative[0] - abs(derivative[1]) * graph_lipschitz
    if not (left_momentum < 0 and right_momentum > 0 and along_graph > 0):
        raise RuntimeError(
            "deep actual-graph shooting root lacks strict face signs/monotonicity"
        )
    for name, threshold in {
        "flight": module.arb(18) / 100,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(63) / 100,
        "clearance": module.arb(22) / 100,
    }.items():
        if not whole.minima[name] > threshold:
            raise RuntimeError(f"deep half-word physical margin {name} fails")

    prefix = replay_rectangle(
        full_cross, parent, qnl, connector, tangent, module, slope,
        qnl_return_word * TAIL_DEPTH, center, root_radius, graph_tube,
    )
    prefix_x, prefix_y = terminal_graph_coordinates(module, slope, prefix)
    prefix_root_error = abs(prefix_x - module.arb(ROOT_X_CENTER))
    if not prefix_root_error < module.arb("1e-50"):
        raise RuntimeError("deep pre-tail does not enter the selected root interval")
    if not abs(prefix_y) < module.arb("7e-29"):
        raise RuntimeError("deep pre-tail misses the selected graph-ordinate tube")

    # Convert the half derivative from physical graph eigencoordinates to the
    # exact canonical resonance eigencoordinates.
    terminal_change = [
        [module.R_GRAY / 2, 1 / (2 * slope)],
        [module.R_GRAY / 2, -1 / (2 * slope)],
    ]
    half_graph = mat_mul(module, terminal_change, whole.derivative_box(module))
    scale = -2 * slope
    conversion = mat_diag(module, module.arb(1), scale)
    conversion_inverse = mat_diag(module, module.arb(1), 1 / scale)
    half = mat_mul(module, mat_mul(module, conversion, half_graph), conversion_inverse)
    reconstructed_d = (1 + half[0][1] * half[1][0]) / half[0][0]
    if not (half[1][1] - reconstructed_d).contains(0):
        raise RuntimeError("physical half derivative conflicts with exact det=1")
    half[1][1] = reconstructed_d
    involution = [[module.arb(0), -1 / (2 * slope)], [scale, module.arb(0)]]
    involution_square = mat_mul(module, involution, involution)
    for i in range(2):
        for j in range(2):
            expected = module.arb(1 if i == j else 0)
            if not involution_square[i][j].contains(expected):
                raise RuntimeError(
                    "canonical billiard involution no longer squares to one"
                )
    full_derivative = mat_mul(
        module,
        mat_mul(module, mat_mul(module, involution, mat_inverse_det_one(module, half)), involution),
        half,
    )

    coefficient = -module.arb(325) / (144 * stable.log())
    x_box = center + symmetric_ball(module, root_radius)
    graph_y_box = symmetric_ball(module, graph_tube)
    y_box = scale * graph_y_box
    reflected_x = -y_box / (2 * slope)
    reflected_y = scale * x_box
    gauge_source = gauge_matrix(module, coefficient, x_box, y_box)
    gauge_target = gauge_matrix(module, coefficient, reflected_x, reflected_y)
    gauged_full = mat_mul(
        module,
        mat_mul(module, mat_inverse_det_one(module, gauge_target), full_derivative),
        gauge_source,
    )
    normalise_left = mat_diag(
        module, unstable ** (-(TAIL_DEPTH + 48)), stable ** (-(TAIL_DEPTH + 48))
    )
    normalise_right = mat_diag(
        module, unstable ** (-TAIL_DEPTH), stable ** (-TAIL_DEPTH)
    )
    finite_loop = mat_mul(
        module, mat_mul(module, normalise_left, gauged_full), normalise_right
    )

    analytic = analytic_increment_majorant(module, slope, unstable, stable)
    tail_r = 2 * abs(slope) * (abs(center) + root_radius)
    if not tail_r < module.arb(GAUGE_CORE_RADIUS):
        raise RuntimeError("deep tail is outside the chi=1 compact gauge core")
    log_weight = 1 + abs(tail_r.log())
    log_q = abs(backward_q.log())
    rho = unstable**2 * backward_q**3
    if not rho < module.arb(1) / 10:
        raise RuntimeError("critical transformed tail ratio is not <1/10")
    right_critical_sum = (
        analytic["declared_majorant"]
        * unstable ** (2 * TAIL_DEPTH + 1)
        * tail_r**3
        * (
            log_weight / (1 - rho)
            + log_q * rho / (1 - rho) ** 2
        )
    )
    square_ratio = backward_q**2
    noncritical_sum = (
        analytic["declared_majorant"]
        * unstable
        * tail_r**2
        * (
            log_weight / (1 - square_ratio)
            + log_q * square_ratio / (1 - square_ratio) ** 2
        )
    )
    # Right increments are
    #   U_n=A^n A_hat(w_(n+1)) A^(-(n+1)),
    # so delta_12 is amplified by lambda^(2n+1).  Left increments are
    #   S_n=A^(-(n+49)) A_hat(Iw_n) A^(n+48),
    # so delta_21 is amplified by lambda^(2n+97).  The fixed lambda^96
    # cannot be absorbed or omitted.
    left_critical_sum = unstable**96 * right_critical_sum
    right_exponent = 4 * (right_critical_sum + noncritical_sum)
    left_exponent = 4 * (left_critical_sum + noncritical_sum)
    right_product_error = right_exponent.exp() - 1
    left_product_error = left_exponent.exp() - 1
    finite_norm = mat_infinity_norm(module, finite_loop)
    loop_error = finite_norm * (
        (1 + left_product_error) * (1 + right_product_error) - 1
    )
    enclosed_loop = [
        [entry + symmetric_ball(module, loop_error) for entry in row]
        for row in finite_loop
    ]
    wedges = {
        "wedge_e1_psi_e1": enclosed_loop[1][0],
        "wedge_e2_psi_e1": -enclosed_loop[0][0],
        "wedge_e1_psi_e2": enclosed_loop[1][1],
        "wedge_e2_psi_e2": -enclosed_loop[0][1],
    }
    for name, wedge in wedges.items():
        if wedge.contains(0):
            raise RuntimeError(
                f"selected twisting wedge may vanish: {name}={wedge}, "
                f"finite={finite_loop}, tail_error={loop_error}"
            )

    result = {
        "schema": "cm2.gate1.numeric-holonomy-tail-twisting-frontier.v1",
        "provenance": {
            "dependencies": EXPECTED_HASHES,
            "immutable_internal_digest": immutable["result"]["internal_digest"],
            "compact_internal_digest": compact["result"]["internal_digest"],
            "resonance_model_id": resonance["model_id"],
        },
        "deep_selected_orbit_replay": {
            "arb_precision_bits": PRECISION_BITS,
            "tail_depth_F_returns": TAIL_DEPTH,
            "deep_half_collision_count": len(deep_half),
            "deep_full_F_return_count": 2 * TAIL_DEPTH + 48,
            "deep_root_center": point_decimal(center, 260),
            "deep_root_radius": DEEP_ROOT_RADIUS,
            "graph_ordinate_tube": arb_text(graph_tube, 40),
            "left_face_momentum": arb_text(left_momentum, 40),
            "right_face_momentum": arb_text(right_momentum, 40),
            "shooting_monotonicity": arb_text(along_graph, 40),
            "actual_graph_whole_tube_IVT": True,
            "actual_graph_unique_by_uniform_monotonicity": True,
            "decimal_center_not_substituted_for_graph_point": True,
            "prefix_enters_selected_root_interval": True,
            "prefix_x_minus_selected_center": arb_text(prefix_x - module.arb(ROOT_X_CENTER), 50),
            "prefix_interval_strictly_inside_selected_radius_1e_minus_50": True,
            "all_collisions_physical_with_frozen_margins": True,
        },
        "canonical_coordinate_and_gauge_audit": {
            "graph_to_canonical": "(x,y)= (x_g,-2*kappa*y_g)",
            "canonical_involution": "[[0,-1/(2*kappa)],[-2*kappa,0]]",
            "canonical_involution_square": "identity exactly",
            "lambda_times_mu": "contains 1 with absolute radius <1e-1000",
            "g_u_over_lambda": "325/144",
            "g_s_over_mu": "-325/144",
            "gauge_coefficient": arb_text(coefficient, 60),
            "gauge_matrix": "B_u(x) B_s(y)",
            "half_derivative_determinant": "1 exactly by ds wedge dp",
        },
        "tail_majorants": {
            "chart_radius": GAUGE_CHART_RADIUS,
            "backward_graph_contraction": BACKWARD_CONTRACTION,
            "critical_ratio_rho": arb_text(rho, 50),
            "third_derivative_bound": arb_text(analytic["third_derivative_bound"], 50),
            "fourth_derivative_bound": arb_text(analytic["fourth_derivative_bound"], 50),
            "base_cubic_remainder_ledger": arb_text(analytic["base_cubic_remainder"], 50),
            "derivative_quadratic_remainder_ledger": arb_text(analytic["derivative_quadratic_remainder"], 50),
            "critical_cubic_remainder_ledger": arb_text(analytic["critical_cubic_remainder"], 50),
            "gauge_composition_ledger": arb_text(analytic["gauge_composition_ledger"], 50),
            "gauge_difference_ledger": arb_text(analytic["gauge_difference_ledger"], 50),
            "unstable_critical_explicit_ledger": arb_text(analytic["unstable_critical_explicit"], 50),
            "noncritical_explicit_ledger": arb_text(analytic["noncritical_explicit"], 50),
            "finite_product_monomial_count_bound": analytic["finite_product_monomial_count_bound"],
            "finite_product_factor_degree_bound": analytic["finite_product_factor_degree_bound"],
            "derived_product_ledger": arb_text(analytic["derived_majorant"], 50),
            "declared_increment_majorant": INCREMENT_MAJORANT,
            "critical_entry_bound": analytic["critical_bound"],
            "noncritical_entry_bound": analytic["noncritical_bound"],
            "right_critical_sum": arb_text(right_critical_sum, 50),
            "left_critical_sum_including_lambda_power_96": arb_text(left_critical_sum, 50),
            "right_tail_exponent_sum": arb_text(right_exponent, 50),
            "left_tail_exponent_sum": arb_text(left_exponent, 50),
            "right_tail_product_error": arb_text(right_product_error, 50),
            "left_tail_product_error": arb_text(left_product_error, 50),
            "two_sided_loop_entry_error": arb_text(loop_error, 50),
            "right_critical_conjugation_power": "lambda^(2*n+1) on delta_12",
            "left_critical_conjugation_power": "lambda^(2*n+97) on delta_21",
            "tail_recursion": "psi_(n+1)=S_n psi_n U_n",
            "submultiplicative_product_bound": "||P-I||_infinity<=exp(sum||K_n-I||_infinity)-1",
            "two_sided_error_formula": "||psi-psi_N||<=||psi_N||*((1+eta_L)*(1+eta_R)-1)",
        },
        "selected_homoclinic_holonomy": {
            "typed_F_return_decomposition": "N + 48 + N = 2*N+48",
            "unstable_approximant": "H^u_N=A_hat^N(w_N) A^(-N):E_p->E_z",
            "stable_approximant": "H^s_N=A^(-(N+48)) A_hat^(N+48)(z):E_z->E_p",
            "finite_truncation_formula": (
                "A^(-(N+48)) B(Iw_N)^(-1) DF^(2N+48)(w_N) "
                "B(w_N) A^(-N)"
            ),
            "finite_matrix": [[arb_text(entry, 70) for entry in row] for row in finite_loop],
            "infinite_matrix_enclosure": [
                [arb_text(entry, 70) for entry in row] for row in enclosed_loop
            ],
            "matrix_in_canonical_QNL_eigenfiber_E_p": True,
            "numeric_Hu_tail": True,
            "numeric_Hs_tail": True,
            "numeric_psi_z": True,
        },
        "four_selected_twisting_wedges": {
            name: arb_text(value, 70) for name, value in wedges.items()
        },
        "scope_limits": {
            "selected_immutable_homoclinic_loop_numeric_enclosure": True,
            "four_selected_QNL_eigen_axis_twisting_wedges": True,
            "comparison_with_periodic_shadow_matrix": False,
            "global_faithful_coding": False,
            "uniform_all_plaque_holder_holonomies": False,
            "butler_park_class_H": False,
            "gate1_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "positive": (
                "the selected immutable QNL homoclinic holonomy has a direct "
                "two-sided numerical enclosure and four nonzero eigen-axis wedges"
            ),
            "negative": (
                "no global faithful coding, uniform all-plaque Holder holonomies, "
                "class H, Gate 1, or unconditional CM2"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest(
        {
            "orbit": result["deep_selected_orbit_replay"],
            "tail": result["tail_majorants"],
            "loop": result["selected_homoclinic_holonomy"],
            "wedges": result["four_selected_twisting_wedges"],
            "scope": result["scope_limits"],
        }
    )
    return result


def main() -> int:
    try:
        result = certify_numeric_loop()
    except Exception as exc:
        print(f"GATE1_NUMERIC_HOLONOMY_TAIL_TWISTING: FAILED: {exc}")
        print("SELECTED_NUMERIC_PSI_Z: NOT_CERTIFIED")
        print("FOUR_SELECTED_QNL_TWISTING_WEDGES: NOT_CERTIFIED")
        print("BUTLER_PARK_CLASS_H: NOT_CERTIFIED")
        print("GATE1: NOT_CERTIFIED")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    print("SELECTED_NUMERIC_PSI_Z: CERTIFIED")
    print("FOUR_SELECTED_QNL_TWISTING_WEDGES: CERTIFIED")
    print("BUTLER_PARK_CLASS_H: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
