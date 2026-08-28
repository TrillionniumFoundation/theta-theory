#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterator

import cm2_round160_sheared_scale_jump_engine as r160


HERE = Path(__file__).resolve().parent
SLOPE = Q(1403486916994043, 500000000000000)
ROUND160_ENGINE = "cm2_round160_sheared_scale_jump_engine.py"
ROUND160_ENGINE_SHA256 = (
    "1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122"
)

qstr = r160.qstr
digest = r160.digest


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins() -> None:
    require(
        Path(r160.__file__).resolve() == (HERE / ROUND160_ENGINE).resolve(),
        "round160 engine module identity",
    )
    require(
        sha256(HERE / ROUND160_ENGINE) == ROUND160_ENGINE_SHA256,
        "round160 engine source pin",
    )
    r160.check_pins()


@contextmanager
def recentered_slope() -> Iterator[None]:
    previous = r160.SLOPE
    try:
        r160.SLOPE = SLOPE
        yield
    finally:
        r160.SLOPE = previous
        require(r160.SLOPE is previous, "round160 slope restoration")


def specs() -> dict[str, dict[str, str]]:
    common = {
        "u_lower_h": "100000",
        "u_upper_h": "2500000000000000",
        "slope_beta_per_abs_x": qstr(SLOPE),
    }
    return {
        "c24": {
            **common,
            "kind": "C24_EVENT",
            "w_lower_h": "-430",
            "w_upper_h": "-405",
        },
        "bridge": {
            **common,
            "kind": "STRICT_RETURN_BRIDGE",
            "w_lower_h": "-405",
            "w_upper_h": "-350",
        },
        "d3": {
            **common,
            "kind": "D3_EVENT",
            "w_lower_h": "-350",
            "w_upper_h": "134111000000",
        },
    }


def _call(function: Callable[..., Any], *arguments: Any) -> Any:
    check_pins()
    with recentered_slope():
        return function(*arguments)


def physical_beta_hull(spec: dict[str, str]) -> list[str]:
    return _call(r160.physical_beta_hull, spec)


def physical_beta_face(spec: dict[str, str], u: Q) -> list[str]:
    return _call(r160.physical_beta_face, spec, u)


def coordinate_record(spec: dict[str, str]) -> dict[str, Any]:
    return _call(r160.coordinate_record, spec)


def c24_frontier(spec: dict[str, str]) -> dict[str, Any]:
    result = _call(r160.c24_frontier, spec)
    result["event_box_id"] = (
        "round161-dyadic-recentered-c24:" + digest(spec)
    )
    return result


def d3_frontier(spec: dict[str, str]) -> dict[str, Any]:
    result = _call(r160.d3_frontier, spec)
    result["event_box_id"] = (
        "round161-dyadic-recentered-d3:" + digest(spec)
    )
    return result


def collision3_anchor_exclusion(
    spec: dict[str, str],
    root: tuple[Q, Q],
) -> dict[str, Any]:
    return _call(r160.collision3_anchor_exclusion, spec, root)


def terminal_return_monotonicity(
    spec: dict[str, str],
    owners: list[str],
    root: tuple[Q, Q],
) -> dict[str, Any]:
    return _call(r160.terminal_return_monotonicity, spec, owners, root)


def _c24_anchor_exclusion_data(
    spec: dict[str, str],
) -> tuple[dict[str, Any], Any]:
    """Preserve the collision-three D3 correlation on the C24 macro box."""

    require(spec["kind"] == "C24_EVENT", "C24 anchor exclusion kind")
    _u0, _u1, _slope, _w0, w1 = r160.parse_spec(spec)
    _whole, derivative = r160.d3_scalar(spec, True)
    require(
        derivative is not None and bool(derivative[1] > 0),
        "C24 anchor D3 w derivative",
    )
    upper = r160.d3_scalar(r160.edge_spec(spec, w1), False)[0]
    require(bool(upper.box() < 0), "C24 anchor D3 upper w edge")
    margin = -upper.box()
    record = {
        "method": (
            "collision-three correlated sheared scalar-affine D3 with "
            "positive w derivative and strictly negative upper-w edge"
        ),
        "collision_index": r160.r150.r139.ANCHOR_COLLISION_INDEX,
        "anchor_candidate": r160.r150.r139.ANCHOR,
        "D3_strictly_increasing_in_w": True,
        "D3_upper_w_edge_in_h_units": qstr(w1),
        "D3_upper_w_edge_outer": r160.fixed_outer(upper.box()),
        "D3_upper_w_edge_strict_negative_for_all_u": True,
        "D3_maximum_strict_negative": True,
        "D3_miss_margin_dyadic_depth":
            r160.r150.r139.lower.round136.strict_dyadic_depth(margin),
        "D3_partial_u_outer": r160.fixed_outer(derivative[0], 128),
        "D3_partial_w_outer": r160.fixed_outer(derivative[1], 128),
        "applies_to_retained_and_full_radius4_candidate_universes": True,
        "general_box_complete_owner_anchor_discriminant_overwraps_zero":
            True,
        "correlation_preserved_by_sheared_scalar_model": True,
    }
    return record, margin


def c24_collision3_anchor_exclusion(
    spec: dict[str, str],
) -> dict[str, Any]:
    def build() -> dict[str, Any]:
        return _c24_anchor_exclusion_data(spec)[0]

    return _call(build)


def audit_c24(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    require(spec["kind"] == "C24_EVENT", "C24 audit kind")
    collision3_audits: dict[str, Any] = {}
    with recentered_slope():
        anchor_proof, anchor_margin = _c24_anchor_exclusion_data(spec)
        lower = r160.boundary.r139.lower
        original_complete_owner = lower.round136.complete_owner
        original_full_radius4 = lower.full_radius4_candidate_audit

        def complete_owner(
            state: dict[str, Any],
            current_target: str,
            ledger: Any,
            collision_index: int,
        ) -> tuple[dict[str, Any], dict[str, Any]]:
            if collision_index != r160.r150.r139.ANCHOR_COLLISION_INDEX:
                return original_complete_owner(
                    state,
                    current_target,
                    ledger,
                    collision_index,
                )
            candidate_ids = tuple(
                lower.time3.time2_cert.translated_candidate_ids(
                    current_target,
                    state["chart"],
                )
            )
            ledger.observe(
                "round161_collision3_anchor_correlated_miss",
                anchor_margin,
                {
                    "collision_index": collision_index,
                    "candidate_id": r160.r150.r139.ANCHOR,
                },
            )
            owner, audit = (
                r160.r146.candidates_owner_excluding_physical_anchor(
                    state,
                    current_target,
                    candidate_ids,
                    ledger,
                    collision_index,
                    False,
                    anchor_proof,
                )
            )
            collision3_audits["retained"] = audit
            return owner, audit

        def full_radius4_candidate_audit(
            state: dict[str, Any],
            current_target: str,
            selected_owner: dict[str, Any],
            ledger: Any,
            collision_index: int,
        ) -> dict[str, Any]:
            if collision_index != r160.r150.r139.ANCHOR_COLLISION_INDEX:
                return original_full_radius4(
                    state,
                    current_target,
                    selected_owner,
                    ledger,
                    collision_index,
                )
            candidate_ids = tuple(
                lower.charge.candidate_ids_around(current_target)
            )
            ledger.observe(
                "round161_full_radius4_collision3_anchor_correlated_miss",
                anchor_margin,
                {
                    "collision_index": collision_index,
                    "candidate_id": r160.r150.r139.ANCHOR,
                },
            )
            owner, audit = (
                r160.r146.candidates_owner_excluding_physical_anchor(
                    state,
                    current_target,
                    candidate_ids,
                    ledger,
                    collision_index,
                    True,
                    anchor_proof,
                )
            )
            require(
                owner["selected_target_id"]
                == selected_owner["selected_target_id"],
                "collision3 retained/full winner identity",
            )
            collision3_audits["full_radius4"] = audit
            return audit

        replacements = {
            "complete_owner": complete_owner,
        }
        full_replacements = {
            "full_radius4_candidate_audit":
                full_radius4_candidate_audit,
        }
        with (
            r160.patched(lower.round136, replacements),
            r160.patched(lower, full_replacements),
        ):
            result = r160.audit_c24(spec)
        require(
            set(collision3_audits) == {"retained", "full_radius4"}
            and collision3_audits["retained"]["candidate_count"] > 0
            and collision3_audits["full_radius4"]["candidate_count"] == 161,
            "collision3 correlated candidate audits",
        )
    result["event_box_id"] = (
        "round161-dyadic-recentered-c24-full:" + digest(spec)
    )
    result["collision3_correlated_anchor_exclusion"] = anchor_proof
    result["collision3_correlated_candidate_audits"] = collision3_audits
    result["collision3_correlated_adapter_restored"] = True
    return result


def audit_bridge(spec: dict[str, str]) -> dict[str, Any]:
    result = _call(r160.audit_bridge, spec)
    result["bridge_cell_id"] = (
        "round161-dyadic-recentered-bridge-full:" + digest(spec)
    )
    return result


def audit_d3(spec: dict[str, str]) -> dict[str, Any]:
    result = _call(r160.audit_d3, spec)
    result["event_box_id"] = (
        "round161-dyadic-recentered-d3-full:" + digest(spec)
    )
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
        return {"full_audit": audit_bridge(rows[kind])}
    if kind == "d3":
        spec = rows[kind]
        return {
            "frontier": d3_frontier(spec),
            "full_audit": audit_d3(spec),
        }
    raise RuntimeError("unknown audit part")


if __name__ == "__main__":
    raise SystemExit("library module")
