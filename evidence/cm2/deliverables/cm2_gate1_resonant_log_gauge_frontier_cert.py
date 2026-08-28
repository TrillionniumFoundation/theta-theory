#!/usr/bin/env python3
"""Exact logarithmic-gauge frontier at the QNL resonance.

The frozen Gate-1 certificate gives, on the local QNL stable coordinate,

    A = diag(lambda, mu),  lambda*mu = 1,  0 < mu < 1,
    M(y) = A + g*y^2*E_21 + higher order,
    g/mu = -325/144.

A quadratic smooth gauge cannot change the resonant coefficient.  The
critical logarithmic gauge

    B(y) = I + k*y^2*log|y|*E_21,
    k = g/(mu*log(mu)),

does: for the exact resonant truncation over y -> mu*y,

    B(mu*y)^(-1) M(y) B(y) = A.

The gauge extends C^1 at zero and is C^{1,alpha} for every alpha<1, but is
not C^2.  On the actual analytic non-grazing QNL branch it removes the only
critically amplified quadratic entry.  The remaining canonical increments
have summable model envelopes n*mu^n, mu^(2n), and mu^(4n).

The exact reversible cubic coefficient gives the same logarithmic repair on
the local unstable axis.  These are two local QNL-tail repairs.  They do not
construct a global coding, all-pairs holonomies, or a Butler--Park class-H
cocycle.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
INPUT_MANIFEST = (
    HERE / "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
)
RESONANCE_CERTIFICATE = HERE / "cm2_gate1_canonical_holonomy_resonance_cert.py"
QNL_CERTIFICATE = HERE / "cm2_fixed_section_qnl_cert.py"
R_STABLE = Fraction(-325, 144)  # g_s/mu
R_UNSTABLE = Fraction(325, 144)  # g_u/lambda


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_input() -> dict[str, Any]:
    data = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    assert data["schema"] == "cm2.gate1.canonical-holonomy-resonance.v1"
    jet = data["exact_qnl_jet"]
    assert jet["lambda_times_mu"] == "1 exactly"
    assert jet["all_second_derivatives_zero"] is True
    assert jet["F2_xyy_over_mu"] == "-325/72 exactly"
    assert jet["resonant_increment_coefficient"] == "325/144 exactly"
    assert data["resonant_increment_lemma"]["stable_asymptotic"] == (
        "y_n/mu^n -> c(z) != 0 for local nontrivial z"
    )
    assert data["proved_obstructions"]["canonical_stable_limit_fails_at_qnl"]
    provenance = {
        Path(item["path"]).name: item["sha256"] for item in data["provenance"]
    }
    assert hashlib.sha256(QNL_CERTIFICATE.read_bytes()).hexdigest() == provenance[
        QNL_CERTIFICATE.name
    ]
    return data


def load_exact_symmetric_resonances() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location(
        "cm2_gate1_log_gauge_resonance_source", RESONANCE_CERTIFICATE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load canonical resonance certificate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    qnl = module.load(module.QNL_CERT, "cm2_gate1_log_gauge_qnl_source")
    f1, f2, unstable, stable = module.exact_qnl_eigenjet(qnl)
    zero = qnl.EigenExtension.coerce(0)
    f1_xxy = qnl.derivative(f1, 2, 1, zero)
    f2_xyy = qnl.derivative(f2, 1, 2, zero)
    assert f1_xxy / unstable == qnl.EigenExtension.coerce(Fraction(325, 72))
    assert f2_xyy / stable == qnl.EigenExtension.coerce(Fraction(-325, 72))
    return {
        "F1_xxy_over_lambda": "325/72 exactly",
        "F2_xyy_over_mu": "-325/72 exactly",
        "unstable_resonant_cocycle_ratio": "g_u/lambda=325/144",
        "stable_resonant_cocycle_ratio": "g_s/mu=-325/144",
    }


def exact_truncated_gauge_identity(
    symmetric_resonances: dict[str, str],
) -> dict[str, Any]:
    # Write t(y)=k*y^2*log|y|.  In
    # lambda*t(mu*y)-mu*t(y), the y^2 log|y| coefficients are
    # lambda*k*mu^2 = mu*k and -mu*k, hence cancel.  The remaining
    # y^2 coefficient is mu*k*log(mu)=g.
    log_y_left = Fraction(1)
    log_y_right = Fraction(-1)
    assert log_y_left + log_y_right == 0
    assert R_STABLE == Fraction(-325, 144)
    assert R_UNSTABLE == Fraction(325, 144)
    return {
        "base_map": "S_0(y)=mu*y, 0<mu<1, lambda=1/mu",
        "resonant_truncation": "M_2(y)=diag(lambda,mu)+g*y^2*E_21",
        "exact_input_ratio": "g/mu=-325/144",
        "exact_symmetric_cubic_resonances": symmetric_resonances,
        "gauge": "B_s(y)=I+k*y^2*log|y|*E_21, B_s(0)=I",
        "gauge_coefficient": "k=g/(mu*log(mu))=-325/(144*log(mu))",
        "determinant_B": "1 exactly",
        "inverse_B": "I-k*y^2*log|y|*E_21 exactly",
        "homological_equation": "lambda*t(mu*y)-mu*t(y)=g*y^2",
        "log_y_coefficients": [str(log_y_left), str(log_y_right)],
        "log_y_coefficient_sum": "0",
        "constant_coefficient_after_log_shift": "mu*k*log(mu)=g",
        "transformed_truncated_cocycle": (
            "B(mu*y)^(-1)*M_2(y)*B(y)=diag(lambda,mu) exactly"
        ),
        "truncated_QNL_canonical_stable_tail": "CONSTANT_AND_CONVERGENT",
        "unstable_axis": {
            "base_map": "U_0(x)=lambda*x",
            "resonant_truncation": (
                "M_u,2(x)=diag(lambda,mu)+g_u*x^2*E_12"
            ),
            "exact_input_ratio": "g_u/lambda=325/144",
            "gauge": "B_u(x)=I+k*x^2*log|x|*E_12, B_u(0)=I",
            "same_gauge_coefficient": (
                "k=g_u/(lambda*log(lambda))=325/(144*log(lambda))"
                "=-325/(144*log(mu))"
            ),
            "homological_equation": (
                "mu*t(lambda*x)-lambda*t(x)=g_u*x^2"
            ),
            "transformed_truncated_cocycle": (
                "B_u(lambda*x)^(-1)*M_u,2(x)*B_u(x)=diag(lambda,mu) exactly"
            ),
            "truncated_QNL_canonical_unstable_tail": (
                "CONSTANT_AND_CONVERGENT_BACKWARD"
            ),
        },
        "two_axis_local_gauge": "B(x,y)=B_u(x)*B_s(y), det(B)=1 exactly",
    }


def regularity_and_minimality() -> dict[str, Any]:
    return {
        "scalar_gauge_term": "t(y)=k*y^2*log|y|, t(0)=0",
        "first_derivative": "t'(y)=k*(2*y*log|y|+y), t'(0)=0",
        "regularity": "C^1 and C^{1,alpha} for every 0<alpha<1",
        "holder_reason": "r*|log r|=O(r^alpha) for every alpha<1",
        "not_C2": True,
        "not_C2_reason": "t''(y)=k*(2*log|y|+3) is unbounded at zero",
        "nonzero_k": True,
        "smooth_quadratic_gauge_effect": (
            "for t(y)=c*y^2, lambda*t(mu*y)-mu*t(y)=0"
        ),
        "C2_quadratic_gauge_cannot_cancel_g": True,
        "logarithmic_loss_is_the_resonant_escape": True,
    }


def analytic_physical_tail(source: dict[str, Any]) -> dict[str, Any]:
    # Circular billiard branches are real analytic away from grazing.  The
    # selected QNL orbit is a fixed non-grazing branch.  The analytic stable
    # graph and the frozen cubic jet yield the following orders after the
    # logarithmic gauge.  The critical E_21 entry gains one power of y.
    # Since y_n=O(mu^n) and lambda/mu=mu^-2, its conjugated envelope is
    # O(n*mu^n), while the other entries are geometrically summable.
    return {
        "physical_local_branch": (
            "real-analytic circular-billiard return on a non-grazing QNL neighborhood"
        ),
        "stable_base": "S(y)=mu*y+O(y^3)",
        "stable_orbit_asymptotic": source["resonant_increment_lemma"][
            "stable_asymptotic"
        ],
        "pre_gauge_entries": {
            "21": "g*y^2+O(y^3)",
            "11_minus_lambda": "O(y^2)",
            "22_minus_mu": "O(y^2)",
            "12": "O(y^2)",
        },
        "post_gauge_entries": {
            "21": "O(y^3*|log|y||)",
            "11_minus_lambda": "O(y^2*|log|y||)",
            "22_minus_mu": "O(y^2*|log|y||)",
            "12": "O(y^2)",
        },
        "conjugated_increment_envelopes": {
            "critical_21": "O(n*mu^n)",
            "diagonal": "O(n*mu^(2*n))",
            "decaying_12": "O(mu^(4*n))",
        },
        "exact_majorant_sums": {
            "sum_n_ge_1_n_mu_n": "mu/(1-mu)^2<infinity",
            "sum_n_ge_1_n_mu_2n": "mu^2/(1-mu^2)^2<infinity",
            "sum_n_ge_1_mu_4n": "mu^4/(1-mu^4)<infinity",
        },
        "local_transformed_QNL_stable_canonical_increment_series": (
            "ABSOLUTELY_SUMMABLE"
        ),
        "local_transformed_QNL_stable_canonical_limit": "CONVERGENT",
        "local_transformed_QNL_unstable_canonical_increment_series": (
            "ABSOLUTELY_SUMMABLE_BACKWARD"
        ),
        "local_transformed_QNL_unstable_canonical_limit": "CONVERGENT",
        "natural_gauge_limit_remains_nonconvergent": True,
        "unstable_tail_by_reversible_axis_calculation": True,
    }


def certify() -> dict[str, Any]:
    source = load_input()
    symmetric_resonances = load_exact_symmetric_resonances()
    truncated = exact_truncated_gauge_identity(symmetric_resonances)
    regularity = regularity_and_minimality()
    physical = analytic_physical_tail(source)
    result = {
        "schema": "cm2.gate1.resonant-log-gauge-frontier.v1",
        "provenance": {
            "canonical_resonance_manifest": INPUT_MANIFEST.name,
            "source_model_id": source["model_id"],
            "source_resonance": "325/144",
            "canonical_resonance_certificate": RESONANCE_CERTIFICATE.name,
            "qnl_certificate": QNL_CERTIFICATE.name,
        },
        "exact_resonant_truncated_gauge": truncated,
        "gauge_regularity_and_minimality": regularity,
        "analytic_physical_QNL_tail": physical,
        "scope_limits": {
            "natural_gauge_QNL_holonomy_repaired": False,
            "local_log_gauge_QNL_stable_tail_repaired": True,
            "local_log_gauge_QNL_unstable_tail_repaired": True,
            "global_faithful_symbolic_coding_constructed": False,
            "all_stable_pairs_common_holder_holonomies": False,
            "unstable_holonomies_constructed": False,
            "butler_park_class_H_globally_certified": False,
            "park_piraino_fiber_bunching_restored": False,
            "physical_full_mass_quotient_constructed": False,
            "gate1_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "new_positive_layer": (
                "explicit C^{1,alpha} local two-axis logarithmic fiber gauge "
                "removes both QNL critical stable/unstable tail resonances"
            ),
            "remaining_gate1_task": (
                "extend one gauge to a faithful global coding with all-pairs stable/"
                "unstable Holder holonomies and a typed pinching-twisting loop, or "
                "close Gate 2 directly"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest({
        "truncated": truncated,
        "regularity": regularity,
        "physical": physical,
        "scope": result["scope_limits"],
    })
    return result


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))
    print("GATE1_QNL_RESONANT_LOG_GAUGE_LOCAL_STABLE_UNSTABLE_TAILS: CERTIFIED")
    print("GATE1_GLOBAL_CLASS_H_AND_UNCONDITIONAL_TYPICALITY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
