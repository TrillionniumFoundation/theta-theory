#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterator

from flint import arb, ctx

import cm2_round141_centered_affine_d0_collar_spike as base
import cm2_round146_physical_centered_jet_2d_engine as r146
import cm2_round150_connected_2d_corridor_engine as r150
import cm2_round151_dual_boundary_event_census_engine as boundary
import cm2_round152_open_strip_bridge_engine as bridge


HERE = Path(__file__).resolve().parent
POWER = 4296
PRECISION = 8192
SLOPE = Q(2807, 1000)
PINS = {
    "cm2_round141_centered_affine_d0_collar_spike.py":
        "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1",
    "cm2_round146_physical_centered_jet_2d_engine.py":
        "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb",
    "cm2_round150_connected_2d_corridor_engine.py":
        "4d80a8e3cef5e3e754e1b10221716239bc123aa228c6ab27a30b9fc76af336fc",
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2_round152_open_strip_bridge_engine.py":
        "21c3c7dbce2a288489f5de109df98f90a768d2d42db2fd3c7cc74bbb74134738",
}


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def check_pins() -> None:
    modules = {
        "cm2_round141_centered_affine_d0_collar_spike.py": base,
        "cm2_round146_physical_centered_jet_2d_engine.py": r146,
        "cm2_round150_connected_2d_corridor_engine.py": r150,
        "cm2_round151_dual_boundary_event_census_engine.py": boundary,
        "cm2_round152_open_strip_bridge_engine.py": bridge,
    }
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"pin:{name}")
        require(
            Path(modules[name].__file__).resolve() == (HERE / name).resolve(),
            f"module identity:{name}",
        )


def qstr(value: Q) -> str:
    return r150.r139.qstr(value)


def fixed_outer(value: arb, bits: int = 256) -> list[str]:
    return [
        qstr(bound)
        for bound in base.fixed_padded_outer(value, bits)
    ]


def specs() -> dict[str, dict[str, str]]:
    common = {
        "u_lower_h": "352",
        "u_upper_h": "100000",
        "slope_beta_per_abs_x": "2807/1000",
    }
    return {
        "c24": {
            **common,
            "kind": "C24_EVENT",
            "w_lower_h": "-420",
            "w_upper_h": "-405",
        },
        "bridge": {
            **common,
            "kind": "STRICT_RETURN_BRIDGE",
            "w_lower_h": "-405",
            "w_upper_h": "-10",
        },
        "d3": {
            **common,
            "kind": "D3_EVENT",
            "w_lower_h": "-10",
            "w_upper_h": "10",
        },
    }


def parse_spec(spec: dict[str, str]) -> tuple[Q, Q, Q, Q, Q]:
    required = {
        "kind",
        "u_lower_h",
        "u_upper_h",
        "slope_beta_per_abs_x",
        "w_lower_h",
        "w_upper_h",
    }
    require(set(spec) == required, "spec keys")
    require(all(type(value) is str for value in spec.values()), "spec strings")
    u0 = Q(spec["u_lower_h"])
    u1 = Q(spec["u_upper_h"])
    slope = Q(spec["slope_beta_per_abs_x"])
    w0 = Q(spec["w_lower_h"])
    w1 = Q(spec["w_upper_h"])
    require(
        0 <= u0 < u1
        and slope == SLOPE
        and w0 <= w1,
        "spec domain",
    )
    return u0, u1, slope, w0, w1


def edge_spec(spec: dict[str, str], w: Q) -> dict[str, str]:
    result = dict(spec)
    result["w_lower_h"] = result["w_upper_h"] = qstr(w)
    return result


def physical_beta_hull(spec: dict[str, str]) -> list[str]:
    u0, u1, slope, w0, w1 = parse_spec(spec)
    require(slope > 0, "positive shear")
    return [qstr(slope * u0 + w0), qstr(slope * u1 + w1)]


def physical_beta_face(spec: dict[str, str], u: Q) -> list[str]:
    _u0, _u1, slope, w0, w1 = parse_spec(spec)
    return [qstr(slope * u + w0), qstr(slope * u + w1)]


def coordinate_record(spec: dict[str, str]) -> dict[str, Any]:
    u0, u1, slope, w0, w1 = parse_spec(spec)
    return {
        "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
        "u_definition": "u=abs(delta_x)/h=-delta_x/h",
        "w_definition": "w=delta_beta/h-s*u",
        "slope_s": qstr(slope),
        "u_in_h_units": [qstr(u0), qstr(u1)],
        "w_in_h_units": [qstr(w0), qstr(w1)],
        "physical_delta_beta_hull_in_h_units": physical_beta_hull(spec),
        "generator_jacobian_to_physical_coordinates": [
            ["-h", "0"],
            [qstr(slope) + "*h", "h"],
        ],
    }


def _initial_data(
    root: tuple[Q, Q],
    spec: dict[str, str],
) -> tuple[base.Model, list[list[arb]]]:
    ctx.prec = PRECISION
    u0, u1, slope, w0, w1 = parse_spec(spec)
    uc, ur = (u0 + u1) / 2, (u1 - u0) / 2
    wc, wr = (w0 + w1) / 2, (w1 - w0) / 2
    aq = r150.r139.lower.aq
    h = aq(Q(1, 2**POWER))
    slope_arb = aq(slope)
    u_ball = aq(uc) + r146.symmetric(aq(ur))
    w_ball = aq(wc) + r146.symmetric(aq(wr))
    root_lower, root_upper = map(aq, root)
    root_center = r146.point((root_lower + root_upper) / 2)
    root_ball = (
        root_center
        + r146.symmetric((root_upper - root_lower) / 2)
    )

    def values(u_value: arb, w_value: arb, t_value: arb) -> list[base.Dual]:
        delta_x = base.Dual(-u_value * h, [-h, arb(0)])
        delta_beta = base.Dual(
            (slope_arb * u_value + w_value) * h,
            [slope_arb * h, h],
        )
        return r146.physical_initial(delta_x, delta_beta, t_value)

    center_values = values(aq(uc), aq(wc), root_center)
    interval_values = values(u_ball, w_ball, root_ball)
    root_only_values = values(aq(uc), aq(wc), root_ball)
    raw_affine = base.rows(center_values)
    affine = [
        [r146.point(entry) for entry in row]
        for row in raw_affine
    ]
    interval_derivatives = base.rows(interval_values)
    domain_radii = (aq(ur), aq(wr))
    centers = [r146.point(value.value) for value in center_values]
    remainders = [
        (center_values[row].value - centers[row]).abs_upper()
        + (
            root_only_values[row].value
            - center_values[row].value
        ).abs_upper()
        + sum(
            (
                raw_affine[row][column]
                - affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        + sum(
            (
                interval_derivatives[row][column]
                - raw_affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return (
        base.Model(centers, affine, remainders, domain_radii),
        base.rows(interval_values),
    )


def sheared_initial_model(
    root: tuple[Q, Q],
    spec: dict[str, str],
) -> base.Model:
    return _initial_data(root, spec)[0]


def propagate(
    root: tuple[Q, Q],
    owners: list[str],
    spec: dict[str, str],
    depth: int,
    with_parameter_jacobian: bool,
) -> tuple[base.Model, str, list[list[arb]] | None]:
    model, parameter_jacobian = _initial_data(root, spec)
    current_target = r150.r139.lower.SOURCE_ABSOLUTE_OWNER
    for expected_owner in owners[:depth]:
        if with_parameter_jacobian:
            boxes = model.boxes()
            state = [
                base.Dual(
                    boxes[row],
                    [arb(int(row == column)) for column in range(4)],
                )
                for row in range(4)
            ]
            center, radius = base.target_geometry(expected_owner)
            outputs, _metrics = base.collision(state, center, radius)
            local_jacobian = base.rows(outputs)
            parameter_jacobian = [
                [
                    sum(
                        (
                            local_jacobian[row][inner]
                            * parameter_jacobian[inner][column]
                            for inner in range(4)
                        ),
                        arb(0),
                    )
                    for column in range(2)
                ]
                for row in range(4)
            ]
        model, _audit = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
    return (
        model,
        current_target,
        parameter_jacobian if with_parameter_jacobian else None,
    )


@dataclass
class ScalarModel:
    center: arb
    affine: list[arb]
    remainder: arb
    domain_radii: tuple[arb, arb]

    def radius(self) -> arb:
        return (
            sum(
                self.affine[column].abs_upper()
                * self.domain_radii[column]
                for column in range(2)
            )
            + self.remainder
        )

    def box(self) -> arb:
        return self.center + r146.symmetric(self.radius())


def scalar_from_model(
    model: base.Model,
    function: Callable[[list[base.Dual]], base.Dual],
) -> ScalarModel:
    boxes = model.boxes()
    center_state = [
        base.Dual(
            model.centers[row],
            [arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    interval_state = [
        base.Dual(
            boxes[row],
            [arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    center_value = function(center_state)
    interval_value = function(interval_state)
    center_gradient = center_value.derivative
    interval_gradient = interval_value.derivative
    affine_radii = [
        sum(
            model.affine[row][column].abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    raw_affine = [
        sum(
            (
                center_gradient[inner]
                * model.affine[inner][column]
                for inner in range(4)
            ),
            arb(0),
        )
        for column in range(2)
    ]
    affine = [r146.point(entry) for entry in raw_affine]
    center = r146.point(center_value.value)
    remainder = (
        (center_value.value - center).abs_upper()
        + sum(
            (
                interval_gradient[inner]
                - center_gradient[inner]
            ).abs_upper()
            * affine_radii[inner]
            + interval_gradient[inner].abs_upper()
            * model.remainders[inner]
            for inner in range(4)
        )
        + sum(
            (
                raw_affine[column]
                - affine[column]
            ).abs_upper()
            * model.domain_radii[column]
            for column in range(2)
        )
    )
    return ScalarModel(center, affine, remainder, model.domain_radii)


def parameter_derivative(
    model: base.Model,
    parameter_jacobian: list[list[arb]],
    function: Callable[[list[base.Dual]], base.Dual],
) -> list[arb]:
    boxes = model.boxes()
    interval_state = [
        base.Dual(
            boxes[row],
            [arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    local_gradient = function(interval_state).derivative
    return [
        sum(
            (
                local_gradient[inner]
                * parameter_jacobian[inner][column]
                for inner in range(4)
            ),
            arb(0),
        )
        for column in range(2)
    ]


def terminal_function(
    target: str,
) -> Callable[[list[base.Dual]], base.Dual]:
    center, radius = base.target_geometry(target)

    def function(state: list[base.Dual]) -> base.Dual:
        normal_x = (state[0] - center[0]) / radius
        normal_y = (state[1] - center[1]) / radius
        momentum = -state[2] * normal_y + state[3] * normal_x
        return momentum + r150.r139.lower.aq(Q(1, 50))

    return function


def d3_function() -> Callable[[list[base.Dual]], base.Dual]:
    center, radius = base.target_geometry(r150.r139.ANCHOR)

    def function(state: list[base.Dual]) -> base.Dual:
        dx = center[0] - state[0]
        dy = center[1] - state[1]
        transverse = -state[3] * dx + state[2] * dy
        return radius * radius - transverse * transverse

    return function


def terminal_scalar(
    spec: dict[str, str],
    with_derivative: bool,
) -> tuple[ScalarModel, list[arb] | None, base.Model, str]:
    owners, root = r150.load_seed()
    model, target, jacobian = propagate(
        root,
        owners,
        spec,
        len(owners),
        with_derivative,
    )
    function = terminal_function(target)
    scalar = scalar_from_model(model, function)
    derivative = (
        parameter_derivative(model, jacobian, function)
        if jacobian is not None
        else None
    )
    return scalar, derivative, model, target


def d3_scalar(
    spec: dict[str, str],
    with_derivative: bool,
) -> tuple[ScalarModel, list[arb] | None]:
    owners, root = r150.load_seed()
    model, _target, jacobian = propagate(
        root,
        owners,
        spec,
        2,
        with_derivative,
    )
    function = d3_function()
    scalar = scalar_from_model(model, function)
    derivative = (
        parameter_derivative(model, jacobian, function)
        if jacobian is not None
        else None
    )
    return scalar, derivative


def c24_frontier(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    u0, u1, slope, w0, w1 = parse_spec(spec)
    require(spec["kind"] == "C24_EVENT", "C24 kind")
    whole, derivative, model, target = terminal_scalar(spec, True)
    require(derivative is not None, "C24 derivative")
    require(
        not bool(whole.box() > 0)
        and not bool(whole.box() < 0)
        and bool(derivative[1] > 0),
        "C24 whole graph",
    )
    lower = terminal_scalar(edge_spec(spec, w0), False)[0]
    upper = terminal_scalar(edge_spec(spec, w1), False)[0]
    require(
        bool(lower.box() < 0) and bool(upper.box() > 0),
        "C24 w edges",
    )
    w_center = (w0 + w1) / 2
    middle = terminal_scalar(edge_spec(spec, w_center), False)[0]
    interval_newton = (
        r150.r139.lower.aq(w_center)
        - middle.box() / derivative[1]
    )
    require(
        bool(interval_newton > r150.r139.lower.aq(w0))
        and bool(interval_newton < r150.r139.lower.aq(w1)),
        "C24 sheared Newton",
    )
    residual_slope = -derivative[0] / derivative[1]
    _chart, phase = r146.phase_at_contact(model, target)
    ledger = base.AuditLedger()
    event_core = r150.terminal_event_core_audit(
        {
            **phase,
            "selected_target_id": target,
            "selected_root": None,
        },
        tuple(r150.r139.lower.core_cert.physical_cores()),
        ledger,
    )
    return {
        "status": "PASS",
        "event_box_id": "round160-sheared-c24:" + digest(spec),
        **coordinate_record(spec),
        "event_kind": "COLLISION1648_TERMINAL_C24_P0_ZERO",
        "event_function": "terminal_p(u,w)+1/50",
        "event_function_outer": fixed_outer(whole.box()),
        "lower_w_edge_event_strict_negative": True,
        "upper_w_edge_event_strict_positive": True,
        "partial_event_partial_u_outer": fixed_outer(derivative[0]),
        "partial_event_partial_w_outer": fixed_outer(derivative[1]),
        "partial_event_partial_w_strict_positive": True,
        "parametric_interval_newton_w_outer": fixed_outer(interval_newton),
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_w_root_for_every_fixed_u": True,
        "transverse_to_w_fibres": True,
        "implicit_w_per_u_slope_outer": fixed_outer(residual_slope, 128),
        "implicit_beta_per_abs_x_slope_is_s_plus_residual": True,
        "physical_shear_slope": qstr(slope),
        "sole_unresolved_terminal_core":
            event_core["sole_unresolved_core"],
        "all_other_terminal_core_constraints_strict": True,
    }


def d3_frontier(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    u0, u1, slope, w0, w1 = parse_spec(spec)
    require(spec["kind"] == "D3_EVENT", "D3 kind")
    whole, derivative = d3_scalar(spec, True)
    require(derivative is not None, "D3 derivative")
    require(
        not bool(whole.box() > 0)
        and not bool(whole.box() < 0)
        and bool(derivative[1] > 0),
        "D3 whole graph",
    )
    lower = d3_scalar(edge_spec(spec, w0), False)[0]
    upper = d3_scalar(edge_spec(spec, w1), False)[0]
    require(
        bool(lower.box() < 0) and bool(upper.box() > 0),
        "D3 w edges",
    )
    w_center = (w0 + w1) / 2
    middle = d3_scalar(edge_spec(spec, w_center), False)[0]
    interval_newton = (
        r150.r139.lower.aq(w_center)
        - middle.box() / derivative[1]
    )
    require(
        bool(interval_newton > r150.r139.lower.aq(w0))
        and bool(interval_newton < r150.r139.lower.aq(w1)),
        "D3 sheared Newton",
    )
    residual_slope = -derivative[0] / derivative[1]
    return {
        "status": "PASS",
        "event_box_id": "round160-sheared-d3:" + digest(spec),
        **coordinate_record(spec),
        "event_kind": "COLLISION3_D0_TANGENCY_D3_ZERO",
        "event_function": "D3(u,w)",
        "anchor_candidate": r150.r139.ANCHOR,
        "event_function_outer": fixed_outer(whole.box()),
        "lower_w_edge_D3_strict_negative": True,
        "upper_w_edge_D3_strict_positive": True,
        "partial_D3_partial_u_outer": fixed_outer(derivative[0]),
        "partial_D3_partial_w_outer": fixed_outer(derivative[1]),
        "partial_D3_partial_w_strict_positive": True,
        "parametric_interval_newton_w_outer": fixed_outer(interval_newton),
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_w_root_for_every_fixed_u": True,
        "transverse_to_w_fibres": True,
        "implicit_w_per_u_slope_outer": fixed_outer(residual_slope, 128),
        "implicit_beta_per_abs_x_slope_is_s_plus_residual": True,
        "physical_shear_slope": qstr(slope),
    }


def collision3_anchor_exclusion(
    spec: dict[str, str],
    _root: tuple[Q, Q],
) -> dict[str, Any]:
    require(spec["kind"] == "STRICT_RETURN_BRIDGE", "bridge kind")
    _u0, _u1, _slope, _w0, w1 = parse_spec(spec)
    _whole, derivative = d3_scalar(spec, True)
    require(derivative is not None and bool(derivative[1] > 0), "bridge D3 w")
    upper = d3_scalar(edge_spec(spec, w1), False)[0]
    require(bool(upper.box() < 0), "bridge D3 upper w edge")
    return {
        "method": (
            "sheared scalar-affine D3 with positive w derivative and "
            "strictly negative upper-w edge"
        ),
        "anchor_candidate": r150.r139.ANCHOR,
        "collision_index": r150.r139.ANCHOR_COLLISION_INDEX,
        "D3_strictly_increasing_in_w": True,
        "D3_upper_w_edge_strict_negative_for_all_u": True,
        "D3_maximum_strict_negative": True,
        "D3_miss_margin_dyadic_depth":
            r150.r139.lower.round136.strict_dyadic_depth(-upper.box()),
        "D3_partial_u_outer": fixed_outer(derivative[0], 128),
        "D3_partial_w_outer": fixed_outer(derivative[1], 128),
        "correlation_preserved_by_sheared_scalar_model": True,
    }


def terminal_return_monotonicity(
    spec: dict[str, str],
    _owners: list[str],
    _root: tuple[Q, Q],
) -> dict[str, Any]:
    require(spec["kind"] == "STRICT_RETURN_BRIDGE", "bridge kind")
    _u0, _u1, _slope, w0, _w1 = parse_spec(spec)
    _whole, derivative, _model, _target = terminal_scalar(spec, True)
    require(
        derivative is not None and bool(derivative[1] > 0),
        "bridge terminal w derivative",
    )
    lower = terminal_scalar(edge_spec(spec, w0), False)[0]
    require(bool(lower.box() > 0), "bridge terminal lower w edge")
    return {
        "event_function": "terminal_p(u,w)+1/50",
        "lower_w_edge_event_outer": fixed_outer(lower.box()),
        "lower_w_edge_event_strict_positive_for_all_u": True,
        "partial_event_partial_u_outer": fixed_outer(derivative[0]),
        "partial_event_partial_w_outer": fixed_outer(derivative[1]),
        "partial_event_partial_w_strict_positive_on_full_bridge": True,
        "terminal_event_strict_positive_on_entire_bridge": True,
        "forced_terminal_classification": "RETURN_AT_3_INNER",
        "forced_terminal_destination_core":
            r150.r139.EXPECTED_DESTINATION_CORE_ID,
    }


@contextmanager
def patched(
    module: Any,
    replacements: dict[str, Callable[..., Any]],
) -> Iterator[None]:
    originals = {
        name: getattr(module, name)
        for name in replacements
    }
    try:
        for name, value in replacements.items():
            setattr(module, name, value)
        yield
    finally:
        for name, value in originals.items():
            setattr(module, name, value)
        require(
            all(getattr(module, name) is value for name, value in originals.items()),
            "runtime patch restoration",
        )


def audit_c24(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    require(spec["kind"] == "C24_EVENT", "C24 audit kind")
    with patched(boundary, {"model_for_spec": sheared_initial_model}):
        result = boundary.audit_c24_event_box(spec)
    result["event_box_id"] = "round160-sheared-c24-full:" + digest(spec)
    result.update(coordinate_record(spec))
    result["runtime_adapter_restored"] = True
    return result


def audit_d3(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    require(spec["kind"] == "D3_EVENT", "D3 audit kind")
    with patched(boundary, {"model_for_spec": sheared_initial_model}):
        result = boundary.audit_d3_event_box(spec)
    result["event_box_id"] = "round160-sheared-d3-full:" + digest(spec)
    result.update(coordinate_record(spec))
    result["runtime_adapter_restored"] = True
    return result


def _bridge_qspec(spec: dict[str, str]) -> tuple[Q, Q, Q, Q]:
    u0, u1, _slope, w0, w1 = parse_spec(spec)
    return u0, u1, w0, w1


def audit_bridge(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    require(spec["kind"] == "STRICT_RETURN_BRIDGE", "bridge audit kind")
    replacements = {
        "model_for_spec": sheared_initial_model,
        "collision3_anchor_exclusion": collision3_anchor_exclusion,
        "terminal_return_monotonicity": terminal_return_monotonicity,
        "qspec": _bridge_qspec,
    }
    with patched(bridge, replacements):
        result = bridge.audit_bridge_cell(spec)
    u_range = result.pop("abs_delta_x_in_h_units")
    w_range = result.pop("delta_beta_in_h_units")
    result["bridge_cell_id"] = "round160-sheared-bridge-full:" + digest(spec)
    result.update(coordinate_record(spec))
    require(
        result["u_in_h_units"] == u_range
        and result["w_in_h_units"] == w_range,
        "bridge adapted coordinates",
    )
    result["runtime_adapter_restored"] = True
    return result


def audit_part(kind: str) -> dict[str, Any]:
    rows = specs()
    if kind == "c24":
        spec = rows[kind]
        return {
            "frontier": c24_frontier(spec),
            "full_audit": audit_c24(spec),
        }
    if kind == "bridge":
        spec = rows[kind]
        return {
            "full_audit": audit_bridge(spec),
        }
    if kind == "d3":
        spec = rows[kind]
        return {
            "frontier": d3_frontier(spec),
            "full_audit": audit_d3(spec),
        }
    raise RuntimeError("unknown audit part")


if __name__ == "__main__":
    raise SystemExit("library module")
