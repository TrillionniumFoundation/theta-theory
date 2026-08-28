#!/usr/bin/env python3
"""Gate-1 same-representative / resonant-shadow frontier.

The fourteenth-round stack deliberately separates two cohomologous physical
representatives on the selected clean subsystem:

* an invariant-frame diagonal representative with Butler--Park class H and
  identically zero same-axis twisting; and
* the compact QNL logarithmic gauge with four certified nonzero twisting
  wedges, but without an all-plaque class-H certificate.

This certificate makes that separation quantitative in two ways.

First it records the exact finite-n cohomology-defect identity.  Canonical
holonomies are transported through a Holder transfer only when an amplified
tail defect tends to the identity; ordinary Holder continuity is insufficient
outside fiber bunching.  Since the diagonal loop has zero same-axis wedges
whereas the compact-gauge loop has four nonzero wedges, at least one of the
selected stable/unstable defects is necessarily nontrivial.

Second, it tests the compact gauge at the already frozen 96-collision periodic
shadow of the same QNL homoclinic excursion.  A 5000-bit order-two Arb replay
of the complete word is converted to the canonical QNL resonance coordinates.
The compact gauge is analytic at this nonzero periodic point.  In the
eigenbasis of its gauged return, the derivative of the lower-left cocycle
entry in the physical stable direction is strictly nonzero.  The standard
stable-tail increment therefore grows like the unstable multiplier to the
n-th power, so the compact gauge cannot have a canonical stable holonomy on
any clean horseshoe containing this periodic shadow and a nontrivial local
stable tail accumulating on it.  The shadow uses the
same physical excursion word as the selected homoclinic, but membership of
the shadow in the particular existential horseshoe chosen by the predecessor
is not silently asserted.

This is a scoped obstruction to the existing compact gauge, not a no-go
theorem for every possible C^{1,alpha} gauge.  A third representative could
still solve the all-plaque resonant equations while retaining twisting.
Consequently Gate 1 and unconditional CM2 remain fail-closed.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import hashlib
import importlib.util
import contextlib
import io
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

GLOBAL_MANIFEST = (
    HERE / "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
)
NUMERIC_MANIFEST = (
    HERE / "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json"
)
COMPACT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
SHADOW_MANIFEST = HERE / "cm2-gate1-closed-shadow-twisting-manifest-2026-07-15.json"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
QNL_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"

EXPECTED_HASHES = {
    GLOBAL_MANIFEST.name: "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec",
    NUMERIC_MANIFEST.name: "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    COMPACT_MANIFEST.name: "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    SHADOW_MANIFEST.name: "31a62a2544d266f76dc973e4c26d83ec34941ddb80d1b139c808750d8ced5800",
    SHADOW_CERT.name: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
    TANGENT_CERT.name: "d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1",
    QNL_CERT.name: "0945b084263e2f48d4cc8521e3e1f24986d28d057ec62de829a18471b8e46fa9",
}

PRECISION_BITS = 5000
REFINED_SHADOW_RADIUS = "1e-800"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def short(value: object, digits: int = 80) -> str:
    method = getattr(value, "str", None)
    return method(digits) if callable(method) else str(value)


def point_decimal(value, digits: int = 1200) -> str:
    return value.mid().str(digits, radius=False, more=True)


def mat_mul(module, left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(2)), module.arb(0))
            for j in range(2)
        ]
        for i in range(2)
    ]


def mat_add(left, right):
    return [[left[i][j] + right[i][j] for j in range(2)] for i in range(2)]


def mat_neg(matrix):
    return [[-matrix[i][j] for j in range(2)] for i in range(2)]


def mat_inv(module, matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant.contains(0):
        raise RuntimeError(f"matrix inverse determinant may vanish: {determinant}")
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def mat_vec(module, matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(2)), module.arb(0))
        for i in range(2)
    ]


def audit_frozen_inputs() -> dict[str, Any]:
    for name, expected in EXPECTED_HASHES.items():
        if sha256_path(HERE / name) != expected:
            raise RuntimeError(f"frozen dependency hash changed: {name}")

    global_data = json.loads(GLOBAL_MANIFEST.read_text(encoding="utf-8"))
    numeric = json.loads(NUMERIC_MANIFEST.read_text(encoding="utf-8"))
    compact = json.loads(COMPACT_MANIFEST.read_text(encoding="utf-8"))
    shadow = json.loads(SHADOW_MANIFEST.read_text(encoding="utf-8"))

    if global_data["verdict"]["diagonal_invariant_frame_class_H"] != "CERTIFIED":
        raise RuntimeError("frozen diagonal class-H result disappeared")
    if global_data["verdict"]["diagonal_invariant_frame_weak_typicality"] != "REFUTED":
        raise RuntimeError("frozen zero-twisting result disappeared")
    if numeric["verdict"]["four_selected_QNL_twisting_wedges"] != "CERTIFIED":
        raise RuntimeError("frozen compact-gauge twisting result disappeared")
    if compact["result"]["scope_limits"]["global_all_pairs_holder_holonomies"]:
        raise RuntimeError("compact predecessor unexpectedly claims global holonomies")
    if shadow["verdict"]["finite_closed_same_orbit_shadow_loop"] != "CERTIFIED":
        raise RuntimeError("frozen physical periodic shadow disappeared")

    return {
        "dependencies": dict(EXPECTED_HASHES),
        "global_internal_digest": global_data["result"]["internal_digest"],
        "numeric_internal_digest": numeric["result"]["internal_digest"],
        "compact_internal_digest": compact["result"]["internal_digest"],
        "shadow_schema": shadow["schema"],
    }


def cohomology_transport_frontier() -> dict[str, Any]:
    return {
        "cohomology_convention": "B(x)=D(fx)^-1 A(x) D(x)",
        "finite_n_identity": (
            "H^s_B(x,y;n)=D(y)^-1 A^n(y)^-1 "
            "[D(f^n y)D(f^n x)^-1] A^n(x)D(x)"
        ),
        "right_factored_defect": (
            "L^s_D(x,y;n)=A^n(x)^-1[D(f^n y)D(f^n x)^-1]A^n(x)"
        ),
        "transport_if_and_only_if_defect_limit_is_identity": True,
        "holder_transfer_alone_forces_identity_defect": False,
        "reason": (
            "the tail D(f^n y)D(f^n x)^-1-I may be exponentially amplified "
            "by the non-fiber-bunched condition number of A^n"
        ),
        "diagonal_loop_same_axis_wedges": "both exactly zero",
        "compact_loop_four_wedges": "all four strictly nonzero",
        "all_selected_stable_unstable_defects_can_be_identity": False,
        "conclusion": (
            "the four compact-gauge wedges cannot be imported from the diagonal "
            "class-H representative by formal Holder cohomology transport"
        ),
    }


def collision_step(qnl, module, theta, momentum, source, target):
    normal = theta.cos(), theta.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - momentum * momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    position = (
        qnl.Jet2.constant(module, source.center[0]) + source.radius * normal[0],
        qnl.Jet2.constant(module, source.center[1]) + source.radius * normal[1],
    )
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = qnl.jet_dot(displacement, velocity)
    offset = qnl.jet_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"shadow jet discriminant may vanish: {discriminant.value}")
    flight = -linear - discriminant.sqrt()
    if not flight.value > 0:
        raise RuntimeError(f"shadow jet flight may be nonpositive: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    target_normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    incidence = -qnl.jet_dot(velocity, target_normal)
    if not incidence.value > 0:
        raise RuntimeError(f"shadow jet incidence may vanish: {incidence.value}")
    reflected = (
        velocity[0] + 2 * incidence * target_normal[0],
        velocity[1] + 2 * incidence * target_normal[1],
    )
    output_angle = qnl.jet_atan2(module, target_normal[1], target_normal[0])
    output_tangent = -target_normal[1], target_normal[0]
    output_momentum = qnl.jet_dot(reflected, output_tangent)
    return output_angle, output_momentum


def compact_gauge_data(module, coefficient, x, y):
    if x.contains(0) or y.contains(0):
        raise RuntimeError("periodic shadow meets a logarithmic gauge axis")
    tx = coefficient * x * x * abs(x).log()
    ty = coefficient * y * y * abs(y).log()
    dtx = coefficient * x * (2 * abs(x).log() + 1)
    dty = coefficient * y * (2 * abs(y).log() + 1)
    matrix = [[1 + tx * ty, tx], [ty, module.arb(1)]]
    inverse = [[module.arb(1), -tx], [-ty, 1 + tx * ty]]
    return matrix, inverse, dtx, dty


def gauge_direction(module, tx, ty, dtx, dty, vector):
    dx = dtx * vector[0]
    dy = dty * vector[1]
    return [[dx * ty + tx * dy, dx], [dy, module.arb(0)]]


def certify_shadow_mixed_jet() -> dict[str, Any]:
    shadow = load(SHADOW_CERT, "cm2_gate1_same_rep_shadow")
    tangent = load(TANGENT_CERT, "cm2_gate1_same_rep_tangent")
    qnl = load(QNL_CERT, "cm2_gate1_same_rep_qnl")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)
    # The frozen root routine emits a long human diagnostic.  It is replayed
    # in full but captured here so this certificate's stdout remains a stable
    # machine-readable object plus verdict labels.
    with contextlib.redirect_stdout(io.StringIO()):
        _, slope, _ = tangent.setup_fixed_data(module)

    # Refine the frozen interval-Newton root at the active precision.  This is
    # the same shooting equation and word, not a new orbit.  The much narrower
    # box is needed because the second derivative of this hyperbolic word is
    # enormous and the predecessor's 1e-200 root box was sized only for its
    # first-derivative task.
    q_word = tuple(tangent.QNL_FORWARD_WORD)
    b_word = tuple(tangent.CONNECTOR_REVERSE_FORWARD_WORD)
    half_word = q_word * 2 + b_word * 2
    center = module.arb(shadow.SHADOW_A_CENTER)
    for _ in range(5):
        replay = shadow.propagate_symmetric(tangent, module, center, half_word)
        derivative = replay.momentum.derivative[0]
        if derivative.contains(0):
            raise RuntimeError("shadow refinement derivative may vanish")
        center = module.arb(point_decimal(center - replay.momentum.value / derivative))
    x0 = module.arb(point_decimal(center), REFINED_SHADOW_RADIUS)
    box_replay = shadow.propagate_symmetric(tangent, module, x0, half_word)
    box_derivative = box_replay.momentum.derivative[0]
    center_replay = shadow.propagate_symmetric(tangent, module, center, half_word)
    interval_newton = center - center_replay.momentum.value / box_derivative
    if not x0.contains_interior(interval_newton):
        raise RuntimeError("refined shadow interval-Newton inclusion failed")

    # In canonical QNL resonance coordinates
    #   s=x-y/(2*kappa), p=kappa*x+y/2.
    y0 = -2 * slope * x0
    if not abs(x0) < module.arb("1e-12") or not abs(y0) < module.arb("1e-12"):
        raise RuntimeError("periodic shadow leaves the frozen chi=1 gauge core")
    x = qnl.Jet2.variable(module, x0, 0)
    y = qnl.Jet2.variable(module, y0, 1)
    arclength = x - y / (2 * slope)
    momentum = slope * x + y / 2
    theta = qnl.Jet2.constant(module, module.arb.pi() / 4) + arclength / module.R_GRAY

    full_word = q_word * 2 + b_word * 4 + q_word * 2
    if len(full_word) != 96:
        raise RuntimeError("frozen periodic shadow word length changed")

    current_kind = "G"
    for target_key in full_word:
        source = module.obstacle(current_kind, 0, 0)
        target = module.obstacle(*target_key)
        theta, momentum = collision_step(qnl, module, theta, momentum, source, target)
        current_kind = target_key[0]

    output_arclength = module.R_GRAY * (
        theta - qnl.Jet2.constant(module, module.arb.pi() / 4)
    )
    output_x = (output_arclength + momentum / slope) / 2
    output_y = momentum - slope * output_arclength
    if not output_x.value.contains(x0) or not output_y.value.contains(y0):
        raise RuntimeError("order-two replay lost exact reversible closure")

    linear = [output_x.gradient, output_y.gradient]
    determinant = linear[0][0] * linear[1][1] - linear[0][1] * linear[1][0]
    if not determinant.contains(1):
        raise RuntimeError(f"shadow return derivative lost det=1: {determinant}")
    trace = linear[0][0] + linear[1][1]
    if not trace > module.arb("1e53"):
        raise RuntimeError(f"shadow return lost hyperbolicity: {trace}")
    discriminant = trace * trace - 4
    unstable = (trace + discriminant.sqrt()) / 2
    stable = 1 / unstable

    off_diagonal = linear[0][1]
    if off_diagonal.contains(0):
        raise RuntimeError("shadow eigenvector chart is singular")
    unstable_slope = (unstable - linear[0][0]) / off_diagonal
    stable_slope = (stable - linear[0][0]) / off_diagonal
    eigenvectors = [
        [module.arb(1), module.arb(1)],
        [unstable_slope, stable_slope],
    ]
    eigenvectors_inverse = mat_inv(module, eigenvectors)

    origin = qnl.qnl_return(module, module.arb(0), module.arb(0))
    qnl_stable = origin.stable.gradient[1]
    if not qnl_stable > 0 or not qnl_stable < 1:
        raise RuntimeError("QNL stable multiplier changed")
    coefficient = -module.arb(325) / (144 * qnl_stable.log())
    gauge, gauge_inverse, dtx, dty = compact_gauge_data(
        module, coefficient, x0, y0
    )

    gauged_eigenvectors = mat_mul(module, gauge_inverse, eigenvectors)
    gauged_eigenvectors_inverse = mat_inv(module, gauged_eigenvectors)
    gauged_return = mat_mul(module, mat_mul(module, gauge_inverse, linear), gauge)
    diagonal_check = mat_mul(
        module,
        mat_mul(module, gauged_eigenvectors_inverse, gauged_return),
        gauged_eigenvectors,
    )
    if not diagonal_check[0][0].contains(unstable):
        raise RuntimeError("gauged unstable eigenvalue mismatch")
    if not diagonal_check[1][1].contains(stable):
        raise RuntimeError("gauged stable eigenvalue mismatch")
    if not diagonal_check[0][1].contains(0) or not diagonal_check[1][0].contains(0):
        raise RuntimeError("gauged return is not diagonal in its eigenbasis")

    stable_vector = [module.arb(1), stable_slope]
    image_stable_vector = mat_vec(module, linear, stable_vector)
    d_gauge_source = gauge_direction(
        module,
        gauge[0][1],
        gauge[1][0],
        dtx,
        dty,
        stable_vector,
    )
    d_gauge_target = gauge_direction(
        module,
        gauge[0][1],
        gauge[1][0],
        dtx,
        dty,
        image_stable_vector,
    )

    hessians = [output_x.hessian, output_y.hessian]
    d_linear = [
        [
            hessians[i][j][0] * stable_vector[0]
            + hessians[i][j][1] * stable_vector[1]
            for j in range(2)
        ]
        for i in range(2)
    ]
    # d(B(Gz)^-1 DG(z) B(z)) at the fixed point.  Since d(B^-1)
    # = -B^-1(dB)B^-1, this is the exact three-term product rule.
    term_target = mat_neg(
        mat_mul(
            module,
            mat_mul(
                module,
                mat_mul(module, gauge_inverse, d_gauge_target),
                gauge_inverse,
            ),
            mat_mul(module, linear, gauge),
        )
    )
    term_cocycle = mat_mul(module, mat_mul(module, gauge_inverse, d_linear), gauge)
    term_source = mat_mul(module, mat_mul(module, gauge_inverse, linear), d_gauge_source)
    derivative_gauged = mat_add(mat_add(term_target, term_cocycle), term_source)
    derivative_eigenbasis = mat_mul(
        module,
        mat_mul(module, gauged_eigenvectors_inverse, derivative_gauged),
        gauged_eigenvectors,
    )
    stable_lower_left = derivative_eigenbasis[1][0]
    if stable_lower_left.contains(0):
        raise RuntimeError(
            f"compact-gauge shadow stable mixed coefficient meets zero: {stable_lower_left}"
        )

    return {
        "arb_precision_bits": PRECISION_BITS,
        "refined_shadow_root_radius": REFINED_SHADOW_RADIUS,
        "periodic_shadow_collision_count": 96,
        "periodic_shadow_half_word": "Q^10 B^2",
        "periodic_shadow_full_word": "Q^10 B^4 Q^10",
        "same_selected_homoclinic_excursion_word": True,
        "shadow_qnl_x_coordinate": short(x0),
        "shadow_qnl_y_coordinate": short(y0),
        "compact_gauge_cutoff_is_one_near_shadow": True,
        "compact_gauge_is_C_infinity_near_shadow": True,
        "return_determinant_contains_one": True,
        "return_trace_gt_1e53": True,
        "return_unstable_multiplier": short(unstable),
        "return_stable_multiplier": short(stable),
        "compact_gauge_coefficient": short(coefficient),
        "gauged_stable_direction_lower_left_derivative": short(stable_lower_left),
        "gauged_stable_direction_lower_left_derivative_excludes_zero": True,
        "stable_increment_asymptotic": (
            "(K_n)_21 ~ -Lambda*c*d*Lambda^n for a nontrivial stable tail"
        ),
        "compact_gauge_stable_canonical_limit_at_shadow": "DIVERGENT",
        "nontrivial_local_stable_tail_required": True,
        "compact_gauge_class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail": False,
        "shadow_membership_in_predecessor_existential_horseshoe": "NOT_CERTIFIED",
    }


def certify_frontier() -> dict[str, Any]:
    provenance = audit_frozen_inputs()
    transport = cohomology_transport_frontier()
    shadow = certify_shadow_mixed_jet()
    scope = {
        "finite_faithful_clean_coding_from_predecessor": True,
        "diagonal_representative_class_H_from_predecessor": True,
        "diagonal_representative_weak_typicality": False,
        "compact_gauge_selected_four_wedges_from_predecessor": True,
        "formal_cohomology_transport_merges_the_two_representatives": False,
        "nontrivial_local_stable_tail_required": True,
        "compact_gauge_class_H_on_clean_horseshoe_containing_shadow_and_nontrivial_stable_tail": False,
        "shadow_membership_in_predecessor_existential_horseshoe": False,
        "every_possible_third_representative_obstructed": False,
        "single_representative_class_H_and_twisting_certified": False,
        "full_mass_global_singular_coding": False,
        "physical_projective_PPE": False,
        "gate1_certified": False,
        "unconditional_cm2": False,
    }
    result = {
        "schema": "cm2.gate1.same-representative-resonant-shadow-frontier.v1",
        "provenance": provenance,
        "cohomology_transport_frontier": transport,
        "compact_gauge_periodic_shadow_obstruction": shadow,
        "scope_limits": scope,
        "strict_frontier": {
            "positive": (
                "the exact non-fiber-bunched cohomology defect is typed, and a "
                "5000-bit full-word mixed-jet replay refutes class H for the existing "
                "compact twisting gauge on a clean horseshoe containing the shadow "
                "and a nontrivial local-stable tail accumulating on it"
            ),
            "negative": (
                "no theorem excludes a different resonant gauge with both all-plaque "
                "canonical holonomies and the selected twisting"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest(
        {"transport": transport, "shadow": shadow, "scope": scope}
    )
    return result


def main() -> int:
    try:
        result = certify_frontier()
    except Exception as exc:
        print(f"GATE1_SAME_REPRESENTATIVE_RESONANT_SHADOW: FAILED: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    print("COHOMOLOGY_TRANSPORT_DEFECT: CERTIFIED")
    print("COMPACT_GAUGE_SHADOW_STABLE_CANONICAL_LIMIT: DIVERGENT")
    print("COMPACT_GAUGE_CLASS_H_ON_SHADOW_HORSESHOE_WITH_NONTRIVIAL_STABLE_TAIL: REFUTED")
    print("THIRD_REPRESENTATIVE_CLASS_H_PLUS_TWISTING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
