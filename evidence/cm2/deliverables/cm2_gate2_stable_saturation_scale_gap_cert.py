#!/usr/bin/env python3
"""Quantitative Gate-2 stable-saturation/full-mass gap certificate.

This certificate consumes the same frozen geometry used by the certified
two-local-branch construction.  It proves two deliberately narrow facts:

1. the currently certified 96-word source tube has stable half-height
   1e-80, whereas the already certified endpoints of the relevant actual
   stable leaf are separated by more than 8.29e-15 in the loop transverse
   coordinate; and
2. the two currently enumerated raw source strips account for less than
   9.7 percent of the collision-SRB mass of the common rectangle, leaving
   more than 90.3 percent to an unenumerated complement.

Neither fact is an impossibility theorem for a future curvilinear Young
rectangle.  They rule out promoting the *current two raw strips* to a
full-height stable-saturated/full-mass quotient without new geometry and a
complement return registry.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLOSED_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
PLAQUE_CERT = HERE / "cm2_gate2_actual_stable_plaque_continuation_cert.py"
PLAQUE_MANIFEST = (
    HERE / "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json"
)

PRECISION_BITS = 900
QNL_SOURCE_WIDTH = "8.1e-16"
CROSSING_UNCERTAINTY_UPPER = "8.53e-172"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def certify() -> int:
    closed = load(CLOSED_CERT, "cm2_gate2_scale_closed")
    tangent = load(TANGENT_CERT, "cm2_gate2_scale_tangent")
    plaque = load(PLAQUE_CERT, "cm2_gate2_scale_plaque")

    manifest = json.loads(PLAQUE_MANIFEST.read_text(encoding="utf-8"))
    proved = manifest.get("proved_layers", {})
    physical = manifest.get("physical_inputs", {})
    required_predecessor = {
        "actual_stable_plaque_v0_crossing": True,
        "positive_width_actual_plaque_96_word_strip": True,
        "two_local_physical_branches_in_common_rectangle": True,
        "second_branch_stable_saturated": False,
        "two_branch_physical_quotient": False,
    }
    for field, expected in required_predecessor.items():
        if proved.get(field) is not expected:
            raise RuntimeError(f"predecessor layer changed: {field}")
    if physical.get("full_mass_countable_return_partition") is not False:
        raise RuntimeError("predecessor full-mass status was promoted")
    if physical.get("physical_gate2") is not False:
        raise RuntimeError("predecessor physical Gate 2 status was promoted")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    closed.refresh_exact_geometry(module)
    _, slope_qnl, _ = tangent.setup_fixed_data(module)
    a_star = module.arb(closed.SHADOW_A_CENTER, closed.SHADOW_A_RADIUS)

    # Reconstruct the exact loop Perron slope in the common physical
    # (arclength,momentum) trivialisation.  This is needed only for the
    # coordinate-Jacobian factor in the physical mass comparison.
    q_word = tangent.QNL_FORWARD_WORD
    b_word = tangent.CONNECTOR_REVERSE_FORWARD_WORD
    half_word = q_word * 2 + b_word * 2
    theta_star = module.arb.pi() / 4 + 2 * a_star / module.R_GRAY
    half_matrix, _, _ = closed.symplectic_segment_matrix(
        tangent, module, theta_star, module.arb(0), half_word
    )
    aa, bb = half_matrix[0, 0], half_matrix[0, 1]
    cc, dd = half_matrix[1, 0], half_matrix[1, 1]
    loop_b = 2 * bb * dd
    loop_c = 2 * aa * cc
    slope_loop = (loop_c / loop_b).sqrt()
    slope_ratio = slope_loop / slope_qnl
    if not module.arb("0.999999999999999999999999") < slope_ratio:
        raise RuntimeError(f"loop/QNL slope-ratio lower bound lost: {slope_ratio}")
    if not slope_ratio < module.arb("1.000000000000000000000001"):
        raise RuntimeError(f"loop/QNL slope-ratio upper bound lost: {slope_ratio}")

    common_radius = module.arb(plaque.COMMON_RADIUS)
    source_u_radius = module.arb(plaque.SECOND_SOURCE_U_RADIUS)
    source_v_radius = module.arb(plaque.SECOND_SOURCE_V_RADIUS)
    crossing_uncertainty = module.arb(CROSSING_UNCERTAINTY_UPPER)

    # The loop fixed point is (a_*,a_*) in either Perron chart because its
    # physical momentum is zero.  The certified actual stable-leaf crossing
    # is on v=0.  Hence the transverse endpoint separation is |a_*|.
    stable_endpoint_separation = abs(a_star)
    endpoint_reach_factor = stable_endpoint_separation / source_v_radius
    common_halfheight_factor = common_radius / source_v_radius
    current_height_fraction = source_v_radius / common_radius
    uncovered_endpoint_gap = stable_endpoint_separation - source_v_radius
    if not endpoint_reach_factor > module.arb("8.29e65"):
        raise RuntimeError("stable endpoint reach factor lower bound lost")
    if not common_halfheight_factor.contains(module.arb("4.2e65")):
        raise RuntimeError("common half-height factor is not exact")
    if not current_height_fraction < module.arb("2.39e-66"):
        raise RuntimeError("current stable-height fraction bound lost")
    if not uncovered_endpoint_gap > module.arb("8.29e-15"):
        raise RuntimeError("current source unexpectedly reaches the loop point")
    if not crossing_uncertainty / source_u_radius < module.arb("1.07e-104"):
        raise RuntimeError("crossing uncertainty/source-width ratio changed")

    # Collision SRB is constant in (s,p).  A Perron (u,v) chart with slope
    # k has |det d(s,p)/d(u,v)|=2k.  Therefore the QNL full-height source
    # occupies exactly width/(2r)=27/280 of the common rectangle's physical
    # mass.  The entire tiny loop rectangle contributes the second term;
    # using all of it is an upper bound even if only its intersection with
    # the common QNL rectangle is counted.
    qnl_source_fraction = module.arb(QNL_SOURCE_WIDTH) / (2 * common_radius)
    loop_source_fraction_upper = (
        slope_ratio
        * source_u_radius
        * source_v_radius
        / (common_radius * common_radius)
    )
    enumerated_fraction_upper = qnl_source_fraction + loop_source_fraction_upper
    complement_fraction_lower = 1 - enumerated_fraction_upper
    if not qnl_source_fraction.contains(module.arb(27) / 280):
        raise RuntimeError("QNL source fraction exact identity lost")
    if not loop_source_fraction_upper < module.arb("4.54e-119"):
        raise RuntimeError("loop source physical fraction upper bound lost")
    if not enumerated_fraction_upper < module.arb("0.097"):
        raise RuntimeError("enumerated raw-source mass bound lost")
    if not complement_fraction_lower > module.arb("0.903"):
        raise RuntimeError("unregistered complement mass bound lost")

    print("PREDECESSOR_TWO_LOCAL_PHYSICAL_BRANCHES: VERIFIED")
    print("ACTUAL_SINGLE_STABLE_LEAF_ENDPOINTS: VERIFIED")
    print("CURRENT_96_WORD_TUBE_SCALE_GAP: CERTIFIED")
    print(f"  stable_endpoint_separation={stable_endpoint_separation}")
    print(f"  certified_source_v_halfheight={source_v_radius}")
    print(f"  endpoint_reach_factor={endpoint_reach_factor}")
    print(f"  common_halfheight_factor={common_halfheight_factor}")
    print(f"  current_height_fraction={current_height_fraction}")
    print(f"  uncovered_endpoint_gap={uncovered_endpoint_gap}")
    print(f"  crossing_uncertainty_over_source_u={crossing_uncertainty/source_u_radius}")
    print("CURRENT_TWO_RAW_STRIPS_FULL_MASS_ROUTE: RULED_OUT")
    print(f"  qnl_source_physical_fraction={qnl_source_fraction}")
    print(f"  loop_source_physical_fraction_upper={loop_source_fraction_upper}")
    print(f"  enumerated_physical_fraction_upper={enumerated_fraction_upper}")
    print(f"  unregistered_complement_fraction_lower={complement_fraction_lower}")
    print("CURVILINEAR_STABLE_SATURATION_ROUTE: OPEN")
    print("INTERVAL_INDEXED_INVARIANT_PLAQUE_FAMILY: NOT_CERTIFIED")
    print("FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED")
    print("ACTUAL_SRB_GIBBS_WEIGHTS_AND_STOPPED_PPE: NOT_CERTIFIED")
    print("PHYSICAL_GATE2: NOT_CERTIFIED")
    return 0


def main() -> int:
    try:
        return certify()
    except Exception as exc:
        print(f"GATE2_STABLE_SATURATION_SCALE_GAP: FAILED: {exc}")
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
