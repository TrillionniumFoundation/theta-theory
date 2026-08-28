#!/usr/bin/env python3
"""Interior-witness hardening for the zero-credit C30q1 cohort gate.

The hash-pinned v2 gate performs the complete 54-origin census.  This additive
layer replaces its q=0 boundary diagnostic with a strictly interior r=1/2
algebraic witness.  The witness proves, by an exact rational square gap, that
the frozen-target forward projection is positive on one original root.  It
therefore refutes only automatic extension of the representative
frozen-behind sufficient certificate; it does not refute CM2, establish a
first owner, mint credit, or authorize a seal.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True

from flint import ctx


HERE = Path(__file__).absolute().parent
V2_SOURCE = (
    HERE
    / "cm2_round306c30q1_compact_q_54_origin_analytic_cohort_"
      "counterexample_gate_v2.py"
)
V2_SHA256 = (
    "343212a2110304f2c3eef835892a57175939baea6d867273d077ce5aa67bd261"
)
SCHEMA = (
    "cm2.round306c30q1.compact-q-54-origin-analytic-cohort-"
    "counterexample-gate.v3"
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def exact_interior_witness(result: dict[str, Any], probe: Any) -> dict[str, Any]:
    rows = result["analytic_cohort_census"]["root_results"]
    candidate = next(
        row for row in rows
        if row["cohort_parameters"]["source_chart"] == "W:N"
        and row["cohort_parameters"]["p_sign"] == -1
        and "FROZEN_NOT_CERTIFIED_STRICTLY_BEHIND" in row["failure_reasons"]
    )
    parameters = candidate["cohort_parameters"]
    t0, t1 = (Q(value) for value in parameters["exact_t_domain"])
    s0, s1 = (Q(value) for value in parameters["exact_s_domain"])
    r0, r1 = (Q(value) for value in parameters["exact_r_domain"])
    p0, p1 = (Q(value) for value in parameters["source_p_endpoint_domain"])
    t = (t0 + t1) / 2
    s = (s0 + s1) / 2
    r = Q(1, 2)
    k = Q(parameters["exact_q_squared_scale"])
    rho = Q(probe.r176.base.RADIUS["W"])
    need(
        t0 < t < t1
        and s0 < s < s1
        and r0 < r < r1
        and -1 < t < 1
        and 2 * t * t < 1
        and Q(0) < k < 1
        and t < rho,
        "strict interior physical witness domain",
    )

    q_squared = k * r * r
    p_absolute_squared = Q(1) - q_squared
    a_squared = Q(1) - t * t
    need(
        q_squared > 0
        and p_absolute_squared > 0
        and a_squared > 0
        and p0 == -1
        and p1 < 0
        and (-p1) * (-p1) < p_absolute_squared < (-p0) * (-p0),
        "strict algebraic p coordinate in original negative branch interval",
    )

    positive_term_squared = p_absolute_squared * a_squared
    negative_term_squared = q_squared * (rho - t) * (rho - t)
    square_gap = positive_term_squared - negative_term_squared
    frozen_f0 = Q(1) - 2 * rho * t
    need(
        positive_term_squared > 0
        and negative_term_squared > 0
        and square_gap > 0
        and frozen_f0 > 0,
        "exact frozen forward projection reverse inequality",
    )

    incident_roots: list[str] = []
    for row in rows:
        if row["origin_key"] != candidate["origin_key"]:
            continue
        domain = row["cohort_parameters"]
        left_t, right_t = (Q(value) for value in domain["exact_t_domain"])
        left_s, right_s = (Q(value) for value in domain["exact_s_domain"])
        left_r, right_r = (Q(value) for value in domain["exact_r_domain"])
        if left_t < t < right_t and left_s < s < right_s and left_r < r < right_r:
            incident_roots.append(row["root_key"])
    need(
        incident_roots == [candidate["root_key"]],
        "unique strict-interior source-grazing root",
    )

    return {
        "claim_falsified": (
            "the frozen target W[1,0] is strictly behind throughout this "
            "original source-grazing root domain"
        ),
        "scope": (
            "exact strict-interior parameter counterexample to the C30q0 "
            "frozen-behind sufficient subclaim only; not a CM2 counterexample "
            "and not a first-owner classification"
        ),
        "origin_key": candidate["origin_key"],
        "root_key": candidate["root_key"],
        "source_chart": "W:N",
        "original_root_domain_membership": {
            "t_strictly_inside_root_interval": True,
            "s_strictly_inside_root_interval": True,
            "r_strictly_inside_root_interval": True,
            "derived_algebraic_p_strictly_inside_original_p_interval": True,
            "physical_source_chart_predicate_2t_squared_less_than_1": True,
            "unique_strict_interior_incident_root": True,
            "incident_root_keys": incident_roots,
            "exact_t_interval": parameters["exact_t_domain"],
            "exact_s_interval": parameters["exact_s_domain"],
            "exact_r_interval": parameters["exact_r_domain"],
            "exact_original_p_interval": parameters["source_p_endpoint_domain"],
        },
        "exact_parameters": {
            "t": str(t),
            "s": str(s),
            "r": str(r),
            "q": "sqrt(" + str(q_squared) + ")",
            "q_squared": str(q_squared),
            "discrete_p_branch_sign": -1,
            "derived_continuous_p_coordinate": (
                "-sqrt(" + str(p_absolute_squared) + ")"
            ),
            "p_squared": str(p_absolute_squared),
            "a": "sqrt(" + str(a_squared) + ")",
            "a_squared": str(a_squared),
            "q_parameterization_identity": (
                "q=sqrt(" + str(k) + ")*(1/2)"
            ),
            "p_parameterization_identity": (
                "p=-sqrt(1-(" + str(k) + ")*(1/2)^2)"
            ),
            "p_squared_plus_q_squared": "1",
        },
        "exact_frozen_forward_projection_sign_proof": {
            "geometry_formula": (
                "ell_F=q*(t-rho)-p*a="
                "sqrt(p^2)*sqrt(a^2)-sqrt(q^2)*(rho-t)"
            ),
            "rho": str(rho),
            "rho_minus_t": str(rho - t),
            "positive_term_squared": str(positive_term_squared),
            "negative_term_squared": str(negative_term_squared),
            "positive_term_square_minus_negative_term_square": str(square_gap),
            "both_terms_strictly_positive": True,
            "square_gap_strictly_positive": True,
            "ell_sign": "STRICT_POSITIVE",
            "reverses_strictly_behind_ell_negative": True,
        },
        "exact_frozen_f_at_0": {
            "formula": "1-2*rho*t",
            "value": str(frozen_f0),
            "sign": "STRICT_POSITIVE",
        },
        "boundary_ownership_dependency": False,
    }


def rebuild() -> dict[str, Any]:
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    v2 = importlib.import_module(V2_SOURCE.stem)
    need(Path(v2.__file__).absolute() == V2_SOURCE, "v2 module identity")
    v1 = importlib.import_module(v2.V1_SOURCE.stem)
    before_raw, before_identity = v1.capture_no_follow(V2_SOURCE, "C30q1 v2 source")
    need(hashlib.sha256(before_raw).hexdigest() == V2_SHA256, "C30q1 v2 source pin")
    result = v2.rebuild()
    after_raw, after_identity = v1.capture_no_follow(V2_SOURCE, "C30q1 v2 source post")
    need(
        before_raw == after_raw
        and before_identity == after_identity
        and hashlib.sha256(after_raw).hexdigest() == V2_SHA256,
        "C30q1 v2 source stable",
    )
    boundary = result.pop("exact_frozen_behind_reverse_parameter_witness")
    boundary["v3_use"] = "SUPERSEDED_BOUNDARY_DIAGNOSTIC_ONLY"
    boundary["independent_r0_half_open_ownership_established"] = False
    result["superseded_q0_boundary_diagnostic"] = boundary
    probe = importlib.import_module(v1.ROUND218_REPLAY.stem)
    result["exact_strict_interior_frozen_behind_reverse_parameter_witness"] = (
        exact_interior_witness(result, probe)
    )
    result["status"] = (
        "REJECT_AUTOMATIC_REPRESENTATIVE_CERTIFICATE_EXTENSION__"
        "EXACT_STRICT_INTERIOR_FROZEN_BEHIND_WITNESS__ZERO_FORMAL_CREDIT"
    )
    result["verdict"] = "REJECT_AUTOMATIC_CERTIFICATE_EXTENSION"
    result["certificate_logic_scope"] = {
        "whole_box_arb_failure_meaning": (
            "failure to establish this sufficient box certificate; not by "
            "itself a physical point counterexample"
        ),
        "exact_counterexample_scope": (
            "only the frozen-behind subclaim, at the strict-interior algebraic "
            "parameter witness"
        ),
        "q0_boundary_diagnostic_used": False,
        "does_not_refute_CM2": True,
        "does_not_establish_an_alternative_first_owner": True,
    }
    result["frozen_inputs"]["C30q1_v2_probe_sha256"] = V2_SHA256
    result["strict_nonpromotion"]["formal_credit"] = 0
    result["strict_nonpromotion"]["no_seal_or_release_authority"] = True
    result["interpretation"] = (
        "The representative sufficient certificate cannot be extended "
        "automatically to all 54 origins. The exact strict-interior witness "
        "reverses only its frozen-behind subclaim. All other arb failures are "
        "fail-close coverage obstructions. Formal credit remains zero."
    )
    return result


def main() -> int:
    ctx.prec = 192
    try:
        result = rebuild()
        document = {"schema": SCHEMA, "result": result}
        document["result_sha256"] = digest(result)
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except (Reject, RuntimeError, OSError, ValueError, KeyError, StopIteration) as error:
        print("REJECT_C30Q1_V3_PROBE_INTEGRITY:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
