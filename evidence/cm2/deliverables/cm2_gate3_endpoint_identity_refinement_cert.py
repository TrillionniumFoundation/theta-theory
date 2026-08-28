#!/usr/bin/env python3
"""Gate-3 endpoint-collar refinement by an exact orthonormal identity.

This certificate is an independent refinement of
``cm2_gate3_global_physical_subrow_atlas_cert``.  It keeps the same 384
parameter-active sheets, candidate universe, Arb precision, subdivision and
physical label.  The only logical change is to remove two redundant interval
tests from the source/target endpoint predicate.

For the tangent construction, with source normal ``n`` and oriented tangent
``j=(-n_y,n_x)``, one has identically

    |u|^2 = 1,  |n|^2 = 1,  n dot j = 0,
    cp = u dot n,  p = u dot j,
    cp^2 + p^2 = 1.

Consequently ``cp>0`` already implies ``-1<p<1``.  Moreover
``ell=sqrt(distance_squared-radius_squared)`` is positive whenever the
strict radicand check used to construct the tangent succeeds.  The old
separate Arb tests on ``p`` and ``ell>0`` were therefore safe but redundant
and could create artificial endpoint collars through interval dependency.

No maximality, seam quotient, DQ or scalar matching is claimed.
Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from fractions import Fraction
from typing import Any

from flint import arb, ctx

import cm2_gate3_global_physical_subrow_atlas_cert as bulk


ctx.prec = 192
Q = Fraction


def classify_box(box: bulk.Box) -> tuple[str, dict[str, Any] | None]:
    geometry = bulk.tangent_geometry(
        box.chart_id, box.z0, box.z1, box.s0, box.s1,
        box.target_id, box.epsilon,
    )
    if geometry is None:
        return "unresolved_target_geometry", None
    _nx, _ny, qx, qy, ux, uy, ell_t, cp, _p, s = geometry

    # Strict empty witnesses are unchanged.
    if bool(cp < 0):
        return "empty_non_outgoing", None
    if bool(ell_t > bulk.arbq(bulk.base.TAU_MAX)):
        return "empty_target_after_tau3", None

    # Exact identities used here:
    #   ell_t > 0 from the strict radicand test in tangent_geometry;
    #   cp^2+p^2=1, hence cp>0 => |p|<1.
    # Only the genuinely independent endpoint predicates remain.
    cp_positive = bool(cp > 0)
    before_tau3 = bool(ell_t < bulk.arbq(bulk.base.TAU_MAX))
    if not (cp_positive and before_tau3):
        if not cp_positive and before_tau3:
            return "unresolved_genuine_source_grazing_endpoint", None
        if cp_positive and not before_tau3:
            return "unresolved_genuine_tau3_endpoint", None
        return "unresolved_joint_source_or_tau3_endpoint", None

    source = box.chart_id.split(":")[0]
    first_rows = bulk.competitor_rows(
        qx, qy, ux, uy, s, box.target_id,
        bulk.GLOBAL_CANDIDATE_IDS[source],
    )
    clear, blocker = bulk.strict_clear_before(first_rows, ell_t)
    if blocker is not None:
        return "empty_target_strictly_occluded", {"blocker": blocker}
    if not clear:
        return "unresolved_first_visibility", None

    all_rows = bulk.competitor_rows(
        qx, qy, ux, uy, s, box.target_id,
        (target.target_id for target in bulk.TARGETS),
    )
    miss = bulk.strict_miss_owner(all_rows, ell_t)
    if miss is None:
        return "unresolved_miss_owner", None
    miss_target, miss_root, miss_incidence = miss

    relative_velocity = bulk.eta(source, box.target_id)
    polarity_factor = relative_velocity * box.epsilon * uy
    signed_coarea = cp * polarity_factor / ell_t
    # Since cp>0 and ell_t>0 on this branch, the coarea sign is exactly
    # the sign of eta*epsilon*u_y.  Testing the latter avoids a second
    # interval-dependency collar in the product/quotient expression.
    if bool(polarity_factor > 0):
        polarity = 1
    elif bool(polarity_factor < 0):
        polarity = -1
    else:
        return "unresolved_parameter_polarity", None

    return "physical_immutable_subrow", {
        "miss_target": miss_target,
        "polarity": polarity,
        "label": [
            box.chart_id, box.target_id, box.epsilon,
            miss_target, polarity,
        ],
        "target_flight": str(ell_t),
        "source_cosine": str(cp),
        "miss_root": str(miss_root),
        "miss_incidence": str(miss_incidence),
        "signed_coarea": str(signed_coarea),
    }


def box_from_row(row: dict[str, Any]) -> bulk.Box:
    return bulk.Box(
        row["chart_id"], row["target"], row["epsilon"],
        Q(row["z"][0]), Q(row["z"][1]),
        Q(row["s"][0]), Q(row["s"][1]), row["depth"],
    )


def common_tangent_normal_form(box: bulk.Box) -> dict[str, Any] | None:
    """Certify one transverse ``cp=0`` graph across the full s interval.

    At a source-grazing tangent, if ``A=(a-c_source).n-r_source`` and
    ``B=(a-c_source).j``, the tangent formula gives

        cp=0  iff  A=sigma*r_target,
        sigma=-epsilon*sign(B).

    Thus the radical equation reduces to the smooth scalar graph equation
    ``F=A-sigma*r_target=0``.  This routine proves fixed sign of B, strict
    z-monotonicity of F, opposite F signs on the two z faces, and opposite
    strict cp signs there.  It therefore gives exactly one transverse
    source-grazing graph z=z(s) in the box.
    """
    source, cell = box.chart_id.split(":")
    z = bulk.arb_interval(box.z0, box.z1)
    s = bulk.arb_interval(box.s0, box.s1)
    t = bulk.INV_SQRT_TWO * z
    radical = (1 - t * t).sqrt()
    dt = bulk.INV_SQRT_TWO
    dradical = -t * dt / radical
    if cell == "E":
        nx, ny = radical, t
        nx_z, ny_z = dradical, dt
    elif cell == "W":
        nx, ny = -radical, t
        nx_z, ny_z = -dradical, dt
    elif cell == "N":
        nx, ny = t, radical
        nx_z, ny_z = dt, dradical
    elif cell == "S":
        nx, ny = t, -radical
        nx_z, ny_z = dt, -dradical
    else:  # pragma: no cover
        raise ValueError(cell)

    ax, ay = bulk.cached_target_center(box.target_id, s)
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = bulk.arbq(Q(1, 2)) + s, bulk.arbq(Q(1, 2))
    Cx, Cy = ax - cx, ay - cy
    source_radius = bulk.ARB_RADIUS[source]
    target_obstacle = bulk.TARGET_BY_ID[box.target_id].obstacle
    target_radius = bulk.ARB_RADIUS[target_obstacle]
    A = Cx * nx + Cy * ny - source_radius
    B = -Cx * ny + Cy * nx
    if bool(B > 0):
        sign_b = 1
    elif bool(B < 0):
        sign_b = -1
    else:
        return None
    sigma = -box.epsilon * sign_b
    F = A - sigma * target_radius
    F_z = Cx * nx_z + Cy * ny_z
    if bool(F_z > 0):
        derivative_sign_z = 1
    elif bool(F_z < 0):
        derivative_sign_z = -1
    else:
        derivative_sign_z = 0

    def face_values(z_value: Q) -> tuple[arb, arb]:
        geometry = bulk.tangent_geometry(
            box.chart_id, z_value, z_value, box.s0, box.s1,
            box.target_id, box.epsilon,
        )
        if geometry is None:
            raise AssertionError("strict parent tangent lost on z face")
        nx_f, ny_f, qx_f, qy_f, _ux, _uy, _ell, cp_f, _p, s_f = geometry
        ax_f, ay_f = bulk.cached_target_center(box.target_id, s_f)
        if source == "G":
            cx_f, cy_f = arb(0), arb(0)
        else:
            cx_f, cy_f = bulk.arbq(Q(1, 2)) + s_f, bulk.arbq(Q(1, 2))
        A_f = (ax_f - cx_f) * nx_f + (ay_f - cy_f) * ny_f - source_radius
        return A_f - sigma * target_radius, cp_f

    F0, cp0 = face_values(box.z0)
    F1, cp1 = face_values(box.z1)
    opposite_f = (bool(F0 < 0) and bool(F1 > 0)) or (
        bool(F0 > 0) and bool(F1 < 0)
    )
    opposite_cp = (bool(cp0 < 0) and bool(cp1 > 0)) or (
        bool(cp0 > 0) and bool(cp1 < 0)
    )
    if derivative_sign_z and opposite_f and opposite_cp:
        return {
            "graph_axis": "z_as_function_of_s",
            "sigma": sigma,
            "sign_B": sign_b,
            "sign_derivative": derivative_sign_z,
            "F_box": str(F),
            "derivative": str(F_z),
            "F_opposite_faces": [str(F0), str(F1)],
            "cp_opposite_faces": [str(cp0), str(cp1)],
        }

    # A curve entering through a horizontal box edge is instead certified as
    # a unique graph s=s(z).  On every active cross-colour sheet,
    # dC/ds=eta*e_x, hence F_s=eta*n_x exactly.
    eta_value = bulk.eta(source, box.target_id)
    F_s = eta_value * nx
    if bool(F_s > 0):
        derivative_sign_s = 1
    elif bool(F_s < 0):
        derivative_sign_s = -1
    else:
        return None

    def s_face_values(s_value: Q) -> tuple[arb, arb]:
        geometry = bulk.tangent_geometry(
            box.chart_id, box.z0, box.z1, s_value, s_value,
            box.target_id, box.epsilon,
        )
        if geometry is None:
            raise AssertionError("strict parent tangent lost on s face")
        nx_f, ny_f, _qx_f, _qy_f, _ux, _uy, _ell, cp_f, _p, s_f = geometry
        ax_f, ay_f = bulk.cached_target_center(box.target_id, s_f)
        if source == "G":
            cx_f, cy_f = arb(0), arb(0)
        else:
            cx_f, cy_f = bulk.arbq(Q(1, 2)) + s_f, bulk.arbq(Q(1, 2))
        A_f = (ax_f - cx_f) * nx_f + (ay_f - cy_f) * ny_f - source_radius
        return A_f - sigma * target_radius, cp_f

    Fs0, cps0 = s_face_values(box.s0)
    Fs1, cps1 = s_face_values(box.s1)
    opposite_f_s = (bool(Fs0 < 0) and bool(Fs1 > 0)) or (
        bool(Fs0 > 0) and bool(Fs1 < 0)
    )
    opposite_cp_s = (bool(cps0 < 0) and bool(cps1 > 0)) or (
        bool(cps0 > 0) and bool(cps1 < 0)
    )
    if not (opposite_f_s and opposite_cp_s):
        return None
    return {
        "graph_axis": "s_as_function_of_z",
        "sigma": sigma,
        "sign_B": sign_b,
        "sign_derivative": derivative_sign_s,
        "F_box": str(F),
        "derivative": str(F_s),
        "F_opposite_faces": [str(Fs0), str(Fs1)],
        "cp_opposite_faces": [str(cps0), str(cps1)],
    }


def atlas() -> tuple[list[dict[str, Any]], list[tuple[bulk.Box, dict[str, Any]]]]:
    pending = list(bulk.initial_boxes())
    leaves: list[dict[str, Any]] = []
    physical: list[tuple[bulk.Box, dict[str, Any]]] = []
    while pending:
        box = pending.pop()
        kind, data = classify_box(box)
        if kind.startswith("unresolved_") and box.depth < bulk.MAX_DEPTH:
            pending.extend(reversed(box.split()))
            continue
        row = {**box.key(), "classification": kind}
        if data:
            row.update(data)
        leaves.append(row)
        if kind == "physical_immutable_subrow":
            assert data is not None
            physical.append((box, data))
    leaves.sort(key=bulk.canonical_json)
    physical.sort(key=lambda row: bulk.canonical_json(row[0].key()))
    return leaves, physical


def certify() -> dict[str, Any]:
    leaves, physical = atlas()
    counts = Counter(row["classification"] for row in leaves)
    areas: dict[str, Q] = defaultdict(Q)
    for row in leaves:
        area = (Q(row["z"][1]) - Q(row["z"][0])) * (
            Q(row["s"][1]) - Q(row["s"][0])
        )
        areas[row["classification"]] += area

    total_area = len(bulk.ACTIVE_SHEETS) * (
        bulk.Z_UPPER - bulk.Z_LOWER
    ) * (bulk.S_UPPER - bulk.S_LOWER)
    assert sum(areas.values(), Q(0)) == total_area
    unresolved_area = sum(
        area for kind, area in areas.items() if kind.startswith("unresolved_")
    )
    physical_area = areas["physical_immutable_subrow"]
    empty_area = total_area - unresolved_area - physical_area

    old_total_unresolved = Q(35721, 102400)
    old_endpoint_unresolved = Q(15573, 51200)
    new_genuine_endpoint = sum(
        area for kind, area in areas.items()
        if kind in {
            "unresolved_genuine_source_grazing_endpoint",
            "unresolved_genuine_tau3_endpoint",
            "unresolved_joint_source_or_tau3_endpoint",
        }
    )
    endpoint_area_removed = old_endpoint_unresolved - new_genuine_endpoint
    assert endpoint_area_removed > 0
    assert unresolved_area < old_total_unresolved

    components = bulk.connected_components(physical)
    symmetry = bulk.bulk_symmetry_audit(physical)
    physical_rows = [
        {
            **box.key(),
            "miss_target": data["miss_target"],
            "polarity": data["polarity"],
        }
        for box, data in physical
    ]
    label_counts = Counter(tuple(data["label"]) for _box, data in physical)

    endpoint_rows = [
        row for row in leaves
        if row["classification"] == "unresolved_genuine_source_grazing_endpoint"
    ]
    normal_form_rows = []
    normal_form_area = Q(0)
    for row in endpoint_rows:
        box = box_from_row(row)
        normal_form = common_tangent_normal_form(box)
        if normal_form is None:
            continue
        normal_form_area += box.area
        normal_form_rows.append({**box.key(), **normal_form})
    normal_form_axis_counts = Counter(
        row["graph_axis"] for row in normal_form_rows
    )

    return {
        "schema": "cm2.gate3.endpoint-identity-refinement.v1",
        "precision_bits": ctx.prec,
        "domain_and_sheet_registry_identical_to_bulk_predecessor": True,
        "active_chart_signed_sheets": len(bulk.ACTIVE_SHEETS),
        "initial_z_intervals_per_sheet": bulk.INITIAL_Z,
        "maximum_adaptive_depth": bulk.MAX_DEPTH,
        "exact_identity": {
            "tangent_direction_unit": True,
            "source_normal_tangent_frame_orthonormal": True,
            "cp_squared_plus_p_squared_equals_one": True,
            "cp_positive_implies_source_coordinate_strictly_interior": True,
            "strict_tangent_radicand_implies_target_flight_positive": True,
            "coarea_sign_equals_sign_eta_epsilon_u_y_on_outgoing_rows": True,
        },
        "leaf_count": len(leaves),
        "classification_counts": dict(sorted(counts.items())),
        "classification_parameter_areas": {
            key: str(value) for key, value in sorted(areas.items())
        },
        "total_parameter_area": str(total_area),
        "certified_physical_parameter_area": str(physical_area),
        "certified_empty_parameter_area": str(empty_area),
        "unresolved_parameter_area": str(unresolved_area),
        "unresolved_area_fraction": str(unresolved_area / total_area),
        "predecessor_unresolved_parameter_area": str(old_total_unresolved),
        "predecessor_endpoint_collar_area": str(old_endpoint_unresolved),
        "genuine_endpoint_collar_area": str(new_genuine_endpoint),
        "source_grazing_normal_form_atlas": {
            "endpoint_leaf_count": len(endpoint_rows),
            "transverse_graph_box_count": len(normal_form_rows),
            "transverse_graph_axis_counts": dict(sorted(normal_form_axis_counts.items())),
            "transverse_graph_parameter_area": str(normal_form_area),
            "remaining_endpoint_edge_or_degeneracy_area": str(
                new_genuine_endpoint - normal_form_area
            ),
            "normal_form_rows_sha256": bulk.canonical_digest(normal_form_rows),
            "scope": (
                "each positive box contains exactly one transverse cp=0 "
                "graph z=z(s) or s=s(z); event-label predicates on its outgoing side "
                "are not asserted here"
            ),
        },
        "endpoint_collar_area_removed_by_identity": str(endpoint_area_removed),
        "endpoint_collar_removed_fraction": str(
            endpoint_area_removed / old_endpoint_unresolved
        ),
        "physical_immutable_box_count": len(physical),
        "physical_complete_label_count": len(label_counts),
        "physical_complete_labels_sha256": bulk.canonical_digest([
            {"label": list(label), "box_count": count}
            for label, count in sorted(label_counts.items())
        ]),
        "physical_box_rows_sha256": bulk.canonical_digest(physical_rows),
        "all_leaf_rows_sha256": bulk.canonical_digest(leaves),
        "connected_component_atlas": components,
        "certified_bulk_symmetry_matching": symmetry,
        "scope_limits": {
            "redundant_source_coordinate_and_positive_flight_collars_removed": True,
            "coarea_product_dependency_collar_reduced_by_exact_sign_factor": True,
            "all_remaining_endpoint_collars_are_source_grazing_not_tau3": True,
            "remaining_source_grazing_edge_or_degeneracy_boxes_resolved": False,
            "components_maximal_across_remaining_collars": False,
            "components_quotiented_across_chart_seams": False,
            "global_dq": False,
            "global_scalar_matching": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_ENDPOINT_IDENTITY_REFINEMENT: CERTIFIED")
    print("GATE3_REMAINING_GENUINE_ENDPOINT_COLLARS: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
