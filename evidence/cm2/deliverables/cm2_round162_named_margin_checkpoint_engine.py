#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator

from flint import arb, ctx

import cm2_round161_dyadic_sheared_recentering_engine as r161


HERE = Path(__file__).resolve().parent
PRECISION = 8192
ROUND161_ENGINE = "cm2_round161_dyadic_sheared_recentering_engine.py"
ROUND161_ENGINE_SHA256 = (
    "ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f"
)

base = r161.r160.base
lower = r161.r160.r150.r139.lower
round136 = lower.round136
qstr = r161.qstr
digest = r161.digest


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pins() -> None:
    require(
        Path(r161.__file__).resolve() == (HERE / ROUND161_ENGINE).resolve(),
        "round161 engine module identity",
    )
    require(
        sha256(HERE / ROUND161_ENGINE) == ROUND161_ENGINE_SHA256,
        "round161 engine source pin",
    )
    r161.check_pins()


def checkpoint_spec() -> dict[str, str]:
    return {
        "kind": "C24_EVENT",
        "u_lower_h": "2500000000000000",
        "u_upper_h": "2500000000000001",
        "slope_beta_per_abs_x": qstr(r161.SLOPE),
        "w_lower_h": "-410",
        "w_upper_h": "-408",
    }


def family(name: str) -> str:
    if "homogeneity" in name:
        return "HOMOGENEITY"
    if "capped_reciprocal_cosine" in name:
        return "INCIDENCE"
    if "official_wall" in name:
        return "WALL"
    if "chart" in name:
        return "CHART"
    if "core" in name:
        return "CORE"
    if "winner_pairwise_root_gap" in name:
        return "OWNER_ROOT_GAP"
    if (
        "future_root" in name
        or "behind_far_root" in name
        or "selected_root" in name
        or "flight" in name
    ):
        return "FLIGHT_ROOT"
    if "discriminant" in name or "correlated_miss" in name:
        return "CANDIDATE_DISCRIMINANT"
    raise RuntimeError(f"unclassified margin name:{name}")


class PublicAuditLedger(base.AuditLedger):
    """Round141 ledger plus exact minimum intervals and stable witnesses."""

    instances: list["PublicAuditLedger"] = []

    def __init__(self) -> None:
        super().__init__()
        self.minimum_lowers: dict[str, Q] = {}
        self.minimum_uppers: dict[str, Q] = {}
        self.minimum_witnesses: dict[str, dict[str, Any] | None] = {}
        type(self).instances.append(self)

    def observe(
        self,
        name: str,
        value: arb,
        witness: dict[str, Any] | None = None,
    ) -> int:
        depth = super().observe(name, value, witness)
        lower_bound, upper_bound = round136.arb_pair(value)
        if (
            name not in self.minimum_lowers
            or lower_bound < self.minimum_lowers[name]
        ):
            self.minimum_lowers[name] = lower_bound
            self.minimum_uppers[name] = upper_bound
            self.minimum_witnesses[name] = witness
        return depth

    def public(self) -> dict[str, Any]:
        require(
            set(self.depths)
            == set(self.counts)
            == set(self.minimum_lowers)
            == set(self.minimum_uppers)
            == set(self.minimum_witnesses),
            "public ledger key equality",
        )
        result: dict[str, Any] = {}
        for name in sorted(self.depths):
            depth = self.depths[name]
            lower_bound = self.minimum_lowers[name]
            upper_bound = self.minimum_uppers[name]
            require(
                lower_bound > 0
                and lower_bound <= upper_bound
                and lower_bound > Q(1, 2**depth),
                f"strict minimum replay:{name}",
            )
            result[name] = {
                "family": family(name),
                "role": "UNRELATED_NON_EVENT_STRICT_MARGIN",
                "dyadic_depth": depth,
                "strict_dyadic_lower_bound_power": -depth,
                "strict_dyadic_lower_bound_relation": (
                    f"margin > 2^-{depth}"
                ),
                "minimum_observed_interval_exact_rational": [
                    qstr(lower_bound),
                    qstr(upper_bound),
                ],
                "observation_count": self.counts[name],
                "minimum_observed_witness": self.minimum_witnesses[name],
                "parameter_derivative_status":
                    "NOT_EXPORTED_IN_THIS_CHECKPOINT",
                "parameter_derivative_note": (
                    "this checkpoint exports a validated whole-box lower "
                    "bound; stagewise (partial_u,partial_w) propagation is "
                    "deferred to the first-face continuation ledger"
                ),
            }
        return result


@contextmanager
def public_ledger_capture() -> Iterator[None]:
    original = base.AuditLedger
    PublicAuditLedger.instances = []
    try:
        base.AuditLedger = PublicAuditLedger
        yield
    finally:
        base.AuditLedger = original
        require(base.AuditLedger is original, "AuditLedger restoration")


def intentional_c24_graph_zero(
    spec: dict[str, str],
) -> dict[str, Any]:
    frontier = r161.c24_frontier(spec)
    required = {
        "event_kind": "COLLISION1648_TERMINAL_C24_P0_ZERO",
        "event_function": "terminal_p(u,w)+1/50",
        "unique_w_root_for_every_fixed_u": True,
        "transverse_to_w_fibres": True,
        "partial_event_partial_w_strict_positive": True,
        "parametric_interval_newton_strictly_inside_event_box": True,
    }
    require(
        all(frontier[key] == value for key, value in required.items()),
        "intentional C24 graph",
    )
    return {
        "role": "INTENTIONAL_TYPED_EVENT_GRAPH_ZERO",
        "collision_index": 1648,
        "event_kind": frontier["event_kind"],
        "event_function": frontier["event_function"],
        "event_function_outer": frontier["event_function_outer"],
        "partial_event_partial_u_outer":
            frontier["partial_event_partial_u_outer"],
        "partial_event_partial_w_outer":
            frontier["partial_event_partial_w_outer"],
        "partial_event_partial_w_strict_positive": True,
        "parametric_interval_newton_w_outer":
            frontier["parametric_interval_newton_w_outer"],
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_w_root_for_every_fixed_u": True,
        "transverse_to_w_fibres": True,
        "excluded_from_unrelated_non_event_minimum": True,
    }


def build_checkpoint() -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    spec = checkpoint_spec()
    intentional = intentional_c24_graph_zero(spec)
    with public_ledger_capture():
        full_audit = r161.audit_c24(spec)
    require(
        len(PublicAuditLedger.instances) == 1,
        "one full-audit ledger",
    )
    ledger = PublicAuditLedger.instances[0]
    public = ledger.public()
    required_families = {
        "CANDIDATE_DISCRIMINANT",
        "FLIGHT_ROOT",
        "OWNER_ROOT_GAP",
        "WALL",
        "CHART",
        "HOMOGENEITY",
        "INCIDENCE",
        "CORE",
    }
    observed_families = {row["family"] for row in public.values()}
    require(
        observed_families == required_families,
        "complete named family census",
    )
    require(
        full_audit["status"] == "PASS"
        and full_audit["collision_count"] == 1648
        and full_audit["full_radius4_candidate_test_count"] == 161 * 1648
        and full_audit["ledger_worst_depth"] == max(ledger.depths.values()),
        "full C24 audit",
    )
    weakest_depth = max(row["dyadic_depth"] for row in public.values())
    weakest = [
        {
            "name": name,
            "family": row["family"],
            "dyadic_depth": row["dyadic_depth"],
            "minimum_observed_interval_exact_rational":
                row["minimum_observed_interval_exact_rational"],
            "minimum_observed_witness": row["minimum_observed_witness"],
        }
        for name, row in public.items()
        if row["dyadic_depth"] == weakest_depth
    ]
    return {
        "status": "CERTIFIED_NAMED_MARGIN_CHECKPOINT__D02_STILL_BLOCKED",
        "checkpoint": {
            "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
            "specification": spec,
            "physical_beta_hull_in_h_units":
                r161.physical_beta_hull(spec),
            "precision_bits": PRECISION,
            "checkpoint_role": "C24_EVENT_INTERIOR_SUBBOX",
        },
        "intentional_typed_event_graph_zeros": [intentional],
        "unrelated_non_event_named_margins": public,
        "named_margin_family_census": {
            "required_families": sorted(required_families),
            "observed_families": sorted(observed_families),
            "named_margin_count": len(public),
            "all_unrelated_non_event_margins_strict": True,
            "intentional_graph_zeros_excluded_from_minimum": True,
        },
        "weakest_unrelated_non_event_margin_depth": weakest_depth,
        "weakest_unrelated_non_event_margins": weakest,
        "full_R1648_checkpoint_audit": {
            "collision_count": full_audit["collision_count"],
            "full_radius4_candidate_test_count":
                full_audit["full_radius4_candidate_test_count"],
            "official_sequence_sha256":
                full_audit["official_sequence_sha256"],
            "compact_rows_sha256": full_audit["compact_rows_sha256"],
            "homogeneity_histogram":
                full_audit["homogeneity_histogram"],
            "incidence_histogram": full_audit["incidence_histogram"],
            "preterminal_strict_nonreturn_count":
                full_audit["preterminal_strict_nonreturn_count"],
            "terminal_event": full_audit["terminal_event"],
            "strict_margin_ledger_sha256":
                full_audit["strict_margin_ledger_sha256"],
            "ledger_worst_depth": full_audit["ledger_worst_depth"],
            "collision3_correlated_anchor_exclusion":
                full_audit["collision3_correlated_anchor_exclusion"],
            "collision3_correlated_candidate_audits":
                full_audit["collision3_correlated_candidate_audits"],
            "runtime_adapter_restored":
                full_audit["collision3_correlated_adapter_restored"],
        },
        "parameter_derivative_coverage": {
            "intentional_C24_event_graph": "EXPORTED_VALIDATED_OUTERS",
            "unrelated_non_event_named_margins":
                "VALIDATED_LOWER_BOUNDS_EXPORTED__DERIVATIVES_DEFERRED",
            "deferred_requirement": (
                "export stagewise partial_u and partial_w for every named "
                "non-event margin before claiming an interval first-face "
                "exclusion"
            ),
        },
        "strict_nonclaims": [
            "this one-unit checkpoint is not a continuation interval",
            "this checkpoint does not identify the globally first face",
            "this checkpoint does not extend the full typed chain",
            "this checkpoint does not exhaust disconnected exterior sheets",
        ],
        "strict_nonpromotion": {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "add stagewise parameter derivatives for every named margin, "
            "then validate consecutive compact-angular checkpoints until "
            "the first non-intentional named margin reaches zero"
        ),
    }


if __name__ == "__main__":
    raise SystemExit("library module")
