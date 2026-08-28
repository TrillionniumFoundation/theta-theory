#!/usr/bin/env python3
"""CM2 Gate 1: closed shadowing loop and transported twisting certificate.

The predecessor ``cm2_gate1_full_cross_transport_cert.py`` certifies a true
QNL-to-connector full crossing and its reversible opposite, but deliberately
does not multiply endpoint matrices based at different points.  This file
closes the finite same-orbit matrix gap.

We solve a one-dimensional reversible shooting problem.  Starting on the
time-reversal line ``p=0`` near the QNL orbit, the declared half word is

    Q^10 B^2,

where ``Q`` denotes one two-solid-collision QNL return and ``B`` denotes one
fourteen-solid-collision/period-eight connector cycle.  The stored
``QNL_FORWARD_WORD`` is ``Q^5``.  Its first copy is an outer QNL dwell; the
next ``Q^5 B`` is the actual full-cross transition.  Reflection of the half
word gives the closed word

    Q^10 B^4 Q^10

with 96 solid collisions.  In the full-word factorisation, the middle two
B blocks are the positive connector dwell, while the first and last B
blocks belong to H_AB and H_BA respectively.

Every derivative factor below is evaluated successively on this one
certified orbit.  The reverse factors are obtained only from billiard time
reversal at the paired endpoints.  No matrices based at unrelated points
are multiplied.

This does not silently identify the shadow-basepoint endomorphism with a
Bonatti--Viana stable/unstable holonomy loop acting on the exact QNL periodic
fiber.  That stronger theorem-level fiber identification remains explicitly
fail-closed in the final labels.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"

PRECISION_BITS = 900

# Refined discovery centre.  Acceptance uses the interval-Newton inclusion,
# never the decimal centre by itself.
SHADOW_A_CENTER = (
    "-8.29376219432960196343742704645210405621112831197003390265960702873901556010315973302075521295184438529929771822126109428164376587981382362721643060125486491596811758273935662258197651492590230034640703704758006e-15"
)
SHADOW_A_RADIUS = "1e-200"

SOURCE_T_RADIUS = "1e-20"
SOURCE_TRANSVERSE_RADIUS = "2.1e-18"
TARGET_UNSTABLE_RADIUS = "1e-8"
TARGET_STABLE_RADIUS = "1e-14"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def refresh_exact_geometry(module) -> None:
    """Recreate exact rational constants at the active Arb precision.

    The frozen module is imported at its original 400-bit precision.  Its
    radii are exact rationals, so recreating the same objects at 900 bits is
    a precision refresh, not a change of table or of any frozen artefact.
    """

    module.ZERO = module.arb(0)
    module.ONE = module.arb(1)
    module.HALF = module.ONE / 2
    module.R_GRAY = module.arb(9) / 25
    module.R_WHITE = module.arb(4) / 25
    module.HALF_OBSTACLES = tuple(
        module.obstacle(*key) for key in module.HALF_KEYS
    )
    module.FULL_OBSTACLES = tuple(
        module.obstacle(*key) for key in module.FULL_KEYS
    )


def qnl_coordinates(module, slope, theta, momentum):
    displacement = module.R_GRAY * (theta - module.arb.pi() / 4)
    return (
        (displacement + momentum / slope) / 2,
        (displacement - momentum / slope) / 2,
    )


def connector_coordinates(module, root, slope, theta, momentum):
    displacement = module.R_GRAY * (theta - root.boxes[0])
    return (
        (displacement + momentum / slope) / 2,
        (displacement - momentum / slope) / 2,
    )


def propagate_symmetric(tangent, module, a_box, word):
    a = module.Dual(a_box, [module.arb(1)])
    theta = module.Dual(module.arb.pi() / 4, dimension=1) + (
        2 * a / module.R_GRAY
    )
    momentum = module.Dual(0, [module.arb(0)])
    return tangent.propagate(module, "G", theta, momentum, word)


def propagate_value(tangent, module, theta_box, momentum_box, word):
    return tangent.propagate(
        module,
        "G",
        module.Dual(theta_box, dimension=0),
        module.Dual(momentum_box, dimension=0),
        word,
    )


def symplectic_segment_matrix(tangent, module, theta_box, momentum_box, word):
    """Return the actual segment matrix in gray (s,p) coordinates.

    The fourth entry is reconstructed from det=1.  This keeps the exact
    canonical-area correlation that direct interval determinants lose.
    """

    result = tangent.propagate(
        module,
        "G",
        module.Dual(theta_box, [module.arb(1), module.arb(0)]),
        module.Dual(momentum_box, [module.arb(0), module.arb(1)]),
        word,
    )
    raw = module.arb_mat([result.theta.derivative, result.momentum.derivative])
    a = raw[0, 0]
    b = module.R_GRAY * raw[0, 1]
    c = raw[1, 0] / module.R_GRAY
    if a.contains(0):
        raise RuntimeError(f"segment first entry may vanish: {a}")
    d = (1 + b * c) / a
    return module.arb_mat([[a, b], [c, d]]), result, raw[1, 1]


def reverse_symplectic(module, matrix):
    """D(I F^-1 I) for I(s,p)=(s,-p), assuming det F=1."""

    a, b = matrix[0, 0], matrix[0, 1]
    c, d = matrix[1, 0], matrix[1, 1]
    return module.arb_mat([[d, b], [c, a]])


def require_overlap(module, left, right, label: str) -> None:
    for row in range(2):
        for column in range(2):
            difference = left[row, column] - right[row, column]
            if not difference.contains(0):
                raise RuntimeError(
                    f"{label}[{row},{column}] interval mismatch: {difference}"
                )


def certify() -> int:
    full_cross = load(FULL_CROSS_CERT, "cm2_gate1_closed_loop_full_cross")
    tangent = load(TANGENT_CERT, "cm2_gate1_closed_loop_tangent")

    predecessor_constants = (
        (full_cross.SOURCE_T_RADIUS, SOURCE_T_RADIUS, "source t radius"),
        (
            full_cross.SOURCE_TRANSVERSE_RADIUS,
            SOURCE_TRANSVERSE_RADIUS,
            "source transverse radius",
        ),
        (
            full_cross.TARGET_UNSTABLE_RADIUS,
            TARGET_UNSTABLE_RADIUS,
            "target unstable radius",
        ),
        (
            full_cross.TARGET_STABLE_RADIUS,
            TARGET_STABLE_RADIUS,
            "target stable radius",
        ),
    )
    for actual, expected, label in predecessor_constants:
        if actual != expected:
            raise RuntimeError(f"predecessor {label} changed: {actual} != {expected}")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    refresh_exact_geometry(module)
    root, slope_a, slope_b = tangent.setup_fixed_data(module)
    t_decimal, u_decimal = tangent.refine_center(
        module, root, slope_a, slope_b
    )
    t_center = module.arb(t_decimal)
    u_center = module.arb(u_decimal)

    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    full_word = q_word * 2 + b_word * 4 + q_word * 2
    h_ab_word = q_word + b_word

    if len(q_word) != 10 or len(b_word) != 14:
        raise RuntimeError("frozen QNL/connector block lengths changed")
    if len(half_word) != 48 or len(full_word) != 96:
        raise RuntimeError("closed word length accounting failed")
    if module.FULL_KEYS[1:] != tuple(reversed(module.FULL_KEYS[1:])):
        raise RuntimeError("connector block lost its reversible palindrome")

    center = module.arb(SHADOW_A_CENTER)
    root_box = module.arb(SHADOW_A_CENTER, SHADOW_A_RADIUS)
    center_half = propagate_symmetric(tangent, module, center, half_word)
    box_half = propagate_symmetric(tangent, module, root_box, half_word)
    f_center = center_half.momentum.value
    f_prime = box_half.momentum.derivative[0]
    if f_prime.contains(0) or not f_prime > module.arb("1e22"):
        raise RuntimeError(f"shadow shooting derivative is not separated: {f_prime}")
    interval_newton = center - f_center / f_prime
    if not root_box.contains_interior(interval_newton):
        raise RuntimeError(
            f"shadow interval-Newton inclusion fails: {interval_newton}"
        )

    thresholds = {
        "flight": module.arb(18) / 100,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(63) / 100,
        "clearance": module.arb(22) / 100,
    }
    for name, threshold in thresholds.items():
        if not box_half.minima[name] > threshold:
            raise RuntimeError(
                f"half-word physical margin {name} fails: {box_half.minima[name]}"
            )
    module.certify_lattice_exhaustion(module.arb(1) / 5)
    if box_half.cumulative_lifts[-1] != (0, 0):
        raise RuntimeError("half word does not return to the base gray lift")

    # The exact root starts and ends on Fix(I)={p=0}; reversibility therefore
    # reflects the half itinerary into the second half and proves exact
    # closure of the 96-collision word.
    if not box_half.momentum.value.contains(0):
        raise RuntimeError("half endpoint box misses the reversible line")

    theta_start = module.arb.pi() / 4 + 2 * root_box / module.R_GRAY
    p_start = module.arb(0)

    # First Q block: the outer QNL dwell.  Its endpoint must be strictly in
    # the source rectangle of the certified full-cross branch.
    dwell_a = propagate_value(tangent, module, theta_start, p_start, q_word)
    source_a, source_b = qnl_coordinates(
        module, slope_a, dwell_a.theta.value, dwell_a.momentum.value
    )
    source_t_radius = module.arb(SOURCE_T_RADIUS)
    source_b_radius = module.arb(SOURCE_TRANSVERSE_RADIUS)
    if not abs(source_a - t_center) < source_t_radius:
        raise RuntimeError(
            f"shadow orbit misses full-cross t face: {source_a - t_center}"
        )
    if not abs(source_b) < source_b_radius:
        raise RuntimeError(
            f"shadow orbit misses full-cross transverse face: {source_b}"
        )

    # Evaluate H_AB from that very endpoint, then type its image in the
    # predecessor's connector target rectangle.
    h_ab_matrix, h_ab, h_ab_raw_d = symplectic_segment_matrix(
        tangent,
        module,
        dwell_a.theta.value,
        dwell_a.momentum.value,
        h_ab_word,
    )
    inbound_x, inbound_y = connector_coordinates(
        module, root, slope_b, h_ab.theta.value, h_ab.momentum.value
    )
    target_x_radius = module.arb(TARGET_UNSTABLE_RADIUS)
    target_y_radius = module.arb(TARGET_STABLE_RADIUS)
    if not abs(inbound_x) < target_x_radius:
        raise RuntimeError(f"H_AB image misses target unstable span: {inbound_x}")
    if not inbound_y > u_center - target_y_radius:
        raise RuntimeError(f"H_AB image crosses lower target face: {inbound_y}")
    if not inbound_y < u_center + target_y_radius:
        raise RuntimeError(f"H_AB image crosses upper target face: {inbound_y}")

    # One B block reaches the reversible midpoint.  Its reflected copy is
    # the second (positive) connector dwell block, taking inbound=(x,y) to
    # outbound=(y,x).  Thus the middle dwell has n=2 connector cycles.
    k_matrix, midpoint, k_raw_d = symplectic_segment_matrix(
        tangent,
        module,
        h_ab.theta.value,
        h_ab.momentum.value,
        b_word,
    )
    midpoint_x, midpoint_y = connector_coordinates(
        module, root, slope_b, midpoint.theta.value, midpoint.momentum.value
    )
    if not midpoint.momentum.value.contains(0):
        raise RuntimeError("connector dwell midpoint misses Fix(I)")

    # Consecutive same-orbit derivative factors.  The direct half derivative
    # must overlap their chain-rule product entry by entry.
    a_dwell_matrix, _, a_dwell_raw_d = symplectic_segment_matrix(
        tangent, module, theta_start, p_start, q_word
    )
    half_matrix, _, half_raw_d = symplectic_segment_matrix(
        tangent, module, theta_start, p_start, half_word
    )
    half_chain = k_matrix * h_ab_matrix * a_dwell_matrix
    require_overlap(module, half_chain, half_matrix, "same-orbit half chain")

    # Reflect only the certified paired endpoints.  This is the exact
    # factorisation A_out H_BA K_out K_in H_AB A_in.
    a_out_matrix = reverse_symplectic(module, a_dwell_matrix)
    h_ba_matrix = reverse_symplectic(module, h_ab_matrix)
    k_out_matrix = reverse_symplectic(module, k_matrix)
    closed_chain = (
        a_out_matrix
        * h_ba_matrix
        * k_out_matrix
        * k_matrix
        * h_ab_matrix
        * a_dwell_matrix
    )

    # Preserve the half-map correlation analytically.  If
    # H=[[a,b],[c,d]], det H=1, then S H^-1 S=[[d,b],[c,a]].
    a, b = half_matrix[0, 0], half_matrix[0, 1]
    c, d = half_matrix[1, 0], half_matrix[1, 1]
    loop_a = a * d + b * c
    loop_b = 2 * b * d
    loop_c = 2 * a * c
    loop_matrix = module.arb_mat(
        [[loop_a, loop_b], [loop_c, loop_a]]
    )
    require_overlap(module, closed_chain, loop_matrix, "closed factor chain")

    for label, entry in (
        ("loop a", loop_a),
        ("loop b", loop_b),
        ("loop c", loop_c),
    ):
        if not entry > 0:
            raise RuntimeError(f"{label} is not positive: {entry}")
    if not 2 * loop_a > module.arb("1e52"):
        raise RuntimeError(f"closed loop is not strongly proximal: {loop_a}")

    # Four Perron-line wedges of the transported closed loop, all in the one
    # gray (s,p) chart at the exact closed basepoint.
    slope_square = slope_a * slope_a
    wedge_pp = loop_c - loop_b * slope_square
    wedge_mp = loop_c + 2 * loop_a * slope_a + loop_b * slope_square
    wedge_pm = loop_c - 2 * loop_a * slope_a + loop_b * slope_square
    wedge_mm = wedge_pp
    if not wedge_pp < -module.arb("1e28"):
        raise RuntimeError(f"++/-- twisting wedge is not negative: {wedge_pp}")
    if not wedge_mp > module.arb("1e54"):
        raise RuntimeError(f"-+ twisting wedge is too small: {wedge_mp}")
    if not wedge_pm > module.arb(1000):
        raise RuntimeError(f"+- twisting wedge is too small: {wedge_pm}")

    # A point replay is only a diagnostic; exact closure already follows
    # from the interval root and reversibility.  It independently audits the
    # declared full word and its cumulative lift registry.
    center_theta = module.arb.pi() / 4 + 2 * center / module.R_GRAY
    full_diagnostic = propagate_value(
        tangent, module, center_theta, module.arb(0), full_word
    )
    if not (full_diagnostic.theta.value - center_theta).contains(0):
        raise RuntimeError("full-word angle diagnostic misses zero")
    if not full_diagnostic.momentum.value.contains(0):
        raise RuntimeError("full-word momentum diagnostic misses zero")
    if full_diagnostic.cumulative_lifts[-1] != (0, 0):
        raise RuntimeError("full word changes the universal-cover lift")

    print("FULL_CROSS_PREDECESSOR_CONSTANTS: VERIFIED")
    print("REVERSIBLE_SHADOW_INTERVAL_NEWTON: CERTIFIED")
    print(f"  precision_bits={module.ctx.prec}")
    print(f"  a_root_box={root_box}")
    print(f"  shooting_center_residual={f_center}")
    print(f"  shooting_derivative={f_prime}")
    print(f"  interval_newton_image={interval_newton}")
    print("COMMON_VERTEX_SOURCE_MEMBERSHIP: CERTIFIED")
    print(f"  source_a={source_a}")
    print(f"  source_b={source_b}")
    print(f"  source_a_minus_full_cross_center={source_a - t_center}")
    print(f"  source_half_widths=({source_t_radius},{source_b_radius})")
    print("COMMON_VERTEX_TARGET_MEMBERSHIP: CERTIFIED")
    print(f"  inbound_connector_coordinates=({inbound_x},{inbound_y})")
    print(f"  target_center=(0,{u_center})")
    print(f"  target_half_widths=({target_x_radius},{target_y_radius})")
    print("CONNECTOR_DWELL_SHADOWING: CERTIFIED")
    print("  connector_dwell_cycles=2")
    print("  connector_dwell_solid_collisions=28")
    print(f"  inbound=(x,y)=({inbound_x},{inbound_y})")
    print(f"  reversible_midpoint=(x,y)=({midpoint_x},{midpoint_y})")
    print(f"  outbound=(x,y)=({inbound_y},{inbound_x})")
    print("CLOSED_COMMON_VERTEX_LOOP_WORD: CERTIFIED")
    print("  factorisation=A_out * H_BA * B_out * B_in * H_AB * A_in")
    print("  qnl_outer_dwell_returns_each_side=5")
    print("  H_AB_collision_count=24")
    print("  H_BA_collision_count=24")
    print("  full_solid_collision_count=96")
    print(f"  half_word={half_word}")
    print(f"  full_word={full_word}")
    print(f"  half_cumulative_lifts={box_half.cumulative_lifts}")
    for name, value in box_half.minima.items():
        print(f"  half_minimum_{name}={value}")
    print("SAME_BASEPOINT_DERIVATIVE_CHAIN: CERTIFIED")
    print(f"  D_A_in={a_dwell_matrix}")
    print(f"  D_H_AB={h_ab_matrix}")
    print(f"  D_B_in={k_matrix}")
    print(f"  D_B_out={k_out_matrix}")
    print(f"  D_H_BA={h_ba_matrix}")
    print(f"  D_A_out={a_out_matrix}")
    print(f"  D_half={half_matrix}")
    print(f"  raw_A_dwell_fourth_entry={a_dwell_raw_d}")
    print(f"  raw_H_AB_fourth_entry={h_ab_raw_d}")
    print(f"  raw_B_in_fourth_entry={k_raw_d}")
    print(f"  raw_half_fourth_entry={half_raw_d}")
    print("CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: CERTIFIED")
    print(f"  D_loop={loop_matrix}")
    print("  det_D_loop=1 (exact canonical-area and reversibility identity)")
    print("TRANSPORTED_PINCHING: CERTIFIED")
    print(f"  trace_D_loop={2 * loop_a}")
    print("TRANSPORTED_TWISTING: CERTIFIED")
    print(f"  det(v_plus,L v_plus)={wedge_pp}")
    print(f"  det(v_minus,L v_plus)={wedge_mp}")
    print(f"  det(v_plus,L v_minus)={wedge_pm}")
    print(f"  det(v_minus,L v_minus)={wedge_mm}")
    print("FINITE_CLOSED_SAME_ORBIT_SHADOW_LOOP: CERTIFIED")
    print("FINITE_SHADOW_TRANSPORTED_TWISTING: CERTIFIED")
    print("BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED")
    print("GATE1_FINITE_SHADOW_TWISTING_LAYER: CERTIFIED")
    print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE1_CLOSED_SHADOW_TWISTING: FAILED: {exc}")
        print("CLOSED_COMMON_VERTEX_LOOP_WORD: NOT CERTIFIED")
        print("SAME_BASEPOINT_DERIVATIVE_CHAIN: NOT CERTIFIED")
        print("CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED")
        print("TRANSPORTED_TWISTING: NOT CERTIFIED")
        print("BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED")
        print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
