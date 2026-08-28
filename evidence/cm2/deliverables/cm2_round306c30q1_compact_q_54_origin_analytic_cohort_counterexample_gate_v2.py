#!/usr/bin/env python3
"""Terminology-hardened wrapper for the additive C30q1 cohort gate.

The underlying v1 computation is hash-pinned and reused without weakening its
input-chain checks.  This v2 layer distinguishes a rigorous interval failure
to certify an entire box from a point counterexample, records signed and
absolute p endpoints separately, and derives one exact algebraic parameter
point that reverses the frozen-behind inequality.  It remains zero-credit and
has no sealing or release authority.
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
V1_SOURCE = (
    HERE
    / "cm2_round306c30q1_compact_q_54_origin_analytic_cohort_"
      "counterexample_gate.py"
)
V1_SHA256 = (
    "0242a62bf9ff443a9ff979fc789ac81a7bde4a2b8bc082f81dff813b8bf24936"
)
SCHEMA = (
    "cm2.round306c30q1.compact-q-54-origin-analytic-cohort-"
    "counterexample-gate.v2"
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


def rewrite_p_endpoint_terms(value: Any) -> Any:
    if type(value) is list:
        return [rewrite_p_endpoint_terms(item) for item in value]
    if type(value) is not dict:
        return value
    result: dict[str, Any] = {}
    for key, child in value.items():
        if key == "derived_abs_p_endpoint_near_q0":
            need(type(child) is str, "signed p endpoint type")
            signed = Q(child)
            need(str(signed) == child and signed != 0, "signed p endpoint value")
            result["derived_signed_p_endpoint_near_q0"] = child
            result["derived_absolute_p_endpoint_near_q0"] = str(abs(signed))
        else:
            result[key] = rewrite_p_endpoint_terms(child)
    return result


def exact_frozen_reverse_witness(result: dict[str, Any], probe: Any) -> dict[str, Any]:
    rows = result["analytic_cohort_census"]["root_results"]
    candidate = next(
        row for row in rows
        if "FROZEN_NOT_CERTIFIED_STRICTLY_BEHIND" in row["failure_reasons"]
        and (
            (row["cohort_parameters"]["source_chart"] == "W:N"
             and row["cohort_parameters"]["p_sign"] == -1)
            or
            (row["cohort_parameters"]["source_chart"] == "W:S"
             and row["cohort_parameters"]["p_sign"] == 1)
        )
    )
    parameters = candidate["cohort_parameters"]
    t0, t1 = (Q(value) for value in parameters["exact_t_domain"])
    s0, s1 = (Q(value) for value in parameters["exact_s_domain"])
    t = (t0 + t1) / 2
    s = (s0 + s1) / 2
    need(t0 < t < t1 and s0 < s < s1 and -1 < t < 1, "interior witness point")
    chart = parameters["source_chart"]
    p_sign = parameters["p_sign"]
    p0, p1 = (Q(value) for value in parameters["source_p_endpoint_domain"])
    p_coordinate = Q(p_sign)
    k = Q(parameters["exact_q_squared_scale"])
    need(
        p0 <= p_coordinate <= p1
        and parameters["exact_r_domain"] == ["0", "1"]
        and k > 0
        and p_coordinate * p_coordinate == 1 - k * Q(0) * Q(0)
        and 2 * t * t < 1,
        "exact witness original domain and parameterization",
    )
    incident_roots = []
    for row in rows:
        if row["origin_key"] != candidate["origin_key"]:
            continue
        domain = row["cohort_parameters"]
        left_t, right_t = (Q(value) for value in domain["exact_t_domain"])
        left_s, right_s = (Q(value) for value in domain["exact_s_domain"])
        left_r, right_r = (Q(value) for value in domain["exact_r_domain"])
        if left_t < t < right_t and left_s < s < right_s and left_r <= 0 <= right_r:
            incident_roots.append(row["root_key"])
    need(incident_roots == [candidate["root_key"]], "unique q0 half-open root witness")
    rho = Q(probe.r176.base.RADIUS["W"])
    distance_margin = Q(1) - 2 * rho * t
    ell_squared = Q(1) - t * t
    need(distance_margin > 0 and ell_squared > 0, "exact reverse witness signs")
    ell_formula = (
        "sqrt(1-t^2)"
        if (chart, p_sign) in {("W:N", -1), ("W:S", 1)}
        else "UNREACHABLE"
    )
    need(ell_formula != "UNREACHABLE", "reverse witness cohort")
    return {
        "claim_falsified": (
            "the frozen target W[1,0] is strictly behind throughout this "
            "exact root domain"
        ),
        "scope": (
            "exact parameter counterexample to the representative sufficient "
            "criterion only; not a counterexample to CM2 or proof of a first owner"
        ),
        "origin_key": candidate["origin_key"],
        "root_key": candidate["root_key"],
        "source_chart": chart,
        "original_root_domain_membership": {
            "t_strictly_inside_root_interval": True,
            "s_strictly_inside_root_interval": True,
            "r_is_q0_boundary_stratum": True,
            "derived_p_coordinate_in_original_p_interval": True,
            "Round218_q0_face_replay_binds_this_root": True,
            "unique_t_s_root_interior_and_r0_half_open_owner": True,
            "incident_root_keys": incident_roots,
            "physical_source_chart_predicate_2t_squared_less_than_1": True,
            "exact_t_interval": parameters["exact_t_domain"],
            "exact_s_interval": parameters["exact_s_domain"],
            "exact_r_interval": parameters["exact_r_domain"],
            "exact_original_p_interval": parameters["source_p_endpoint_domain"],
        },
        "exact_parameters": {
            "t": str(t),
            "s": str(s),
            "r": "0",
            "q": "0",
            "discrete_p_branch_sign": p_sign,
            "derived_continuous_p_coordinate": str(p_coordinate),
            "parameterization_identity": (
                "p=sign*sqrt(1-(" + str(k) + ")*r^2)="
                + str(p_coordinate)
            ),
            "a": "sqrt(1-(" + str(t) + ")^2)>0",
        },
        "frozen_forward_projection": {
            "exact_formula_after_substitution": ell_formula,
            "ell_squared": str(ell_squared),
            "ell_sign": "STRICT_POSITIVE",
            "reverses_strictly_behind_ell_negative": True,
        },
        "frozen_f_at_0": {
            "exact_formula": "1-2*(" + str(rho) + ")*t",
            "exact_value": str(distance_margin),
            "sign": "STRICT_POSITIVE",
        },
    }


def rebuild() -> dict[str, Any]:
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    module_name = V1_SOURCE.stem
    v1 = importlib.import_module(module_name)
    need(Path(v1.__file__).absolute() == V1_SOURCE, "v1 module identity")
    before_raw, before_identity = v1.capture_no_follow(V1_SOURCE, "C30q1 v1 source")
    need(hashlib.sha256(before_raw).hexdigest() == V1_SHA256, "C30q1 v1 source pin")
    original = v1.rebuild()
    after_raw, after_identity = v1.capture_no_follow(V1_SOURCE, "C30q1 v1 source post")
    need(
        before_raw == after_raw
        and before_identity == after_identity
        and hashlib.sha256(after_raw).hexdigest() == V1_SHA256,
        "C30q1 v1 source stable",
    )
    result = rewrite_p_endpoint_terms(original)
    probe = importlib.import_module(v1.ROUND218_REPLAY.stem)
    reverse = exact_frozen_reverse_witness(result, probe)
    result["status"] = (
        "REJECT_AUTOMATIC_REPRESENTATIVE_CERTIFICATE_EXTENSION__"
        "EXACT_CRITERION_WITNESS__ZERO_FORMAL_CREDIT"
    )
    result["verdict"] = "REJECT_AUTOMATIC_CERTIFICATE_EXTENSION"
    result["certificate_logic_scope"] = {
        "arb_box_failure_meaning": (
            "a false strict arb comparison means this whole-box sufficient "
            "certificate was not established; it is not by itself a point counterexample"
        ),
        "actual_point_counterexample_claimed_only_for": (
            "the frozen-behind subclaim at the exact algebraic parameter witness below"
        ),
        "does_not_refute_CM2": True,
        "does_not_establish_an_alternative_first_owner": True,
    }
    result["exact_frozen_behind_reverse_parameter_witness"] = reverse
    result["frozen_inputs"]["C30q1_v1_probe_sha256"] = V1_SHA256
    result["strict_nonpromotion"]["formal_credit"] = 0
    result["strict_nonpromotion"]["no_seal_or_release_authority"] = True
    result["interpretation"] = (
        "The current representative sufficient certificate does not extend "
        "automatically to all 54 origins. Whole-box interval failures are "
        "fail-close obstructions, while the separately derived algebraic point "
        "is an exact reversal of the frozen-behind subclaim. No formal credit."
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
        print("REJECT_C30Q1_V2_PROBE_INTEGRITY:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
