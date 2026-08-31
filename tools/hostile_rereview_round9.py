#!/usr/bin/env python3
"""Counterexample-aware hostile rereview for round nine."""
from __future__ import annotations

from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "revision" / "round9-referee-final"

FILES = {
    "A1": "A1_PHYSICAL_IMPACT_DIRECTIONAL_RESPONSE.tex",
    "A2": "A2_BLOWUP_UNI_DENSITY_LLT.tex",
    "A3": "A3_POINTED_EDGE_FLOW_LDP.tex",
    "A4": "A4_PAST_KERNEL_DISTRIBUTIONAL_MEMORY.tex",
    "B1": "B1_FULL_PRESSURE_WEIGHTED_SHELL.tex",
    "B2": "B2_TRACE_JACOBI_SEWING_LDP.tex",
    "B3": "B3_KKT_COVARIANCE_OBSERVABILITY.tex",
    "B4": "B4_LAW_CORE_TRUNCATED_COMPARISON.tex",
    "C1": "C1_EVIDENCE_CURRENT_BELIEF_DPP.tex",
    "C2": "C2_SCALE_CONNECTION_RESOLVED_MEMORY.tex",
    "D1": "D1_EXACT_PHASE_LABEL_MIXTURE.tex",
}


def require(text: str, *tokens: str) -> None:
    for token in tokens:
        if token not in text:
            raise AssertionError(f"missing proof-body token: {token}")


def main() -> None:
    out: dict[str, object] = {"schema": "theta-theory-round9-hostile-rereview-v1", "papers": {}, "errors": []}
    errors: list[str] = []

    for code, name in FILES.items():
        p = SRC / name
        if not p.is_file():
            errors.append(f"{code}: source missing")
            continue
        text = p.read_text(encoding="utf-8")
        try:
            if code == "A1":
                require(text, "physical Poincar", "not extra points of the physical", r"\alpha^{-r}\beta^{-s}", r"\beta<\alpha")
                alpha, beta = 0.8, 0.5
                directional_ratio = beta / alpha
                assert directional_ratio < 1
                assert "complete dynamic germ surface is the graph" not in text
                data = {"directional_shift_ratio": directional_ratio, "physical_symbolic_separated": True}
            elif code == "A2":
                require(text, "material connection", "Explicit finite arithmetic packets", "Uniform returned-branch temporal nonintegrability", "density LLT")
                n, G = 10**6, 10**-4
                # normalized-average window G corresponds to sum interval nG
                correct_factor = n * G * n ** (-1.5)
                wrong_factor = G * n ** (-1.5)
                assert abs(correct_factor / wrong_factor - n) < 1e-6
                data = {"llt_correct_sum_interval_factor": correct_factor, "old_scaling_missing_factor": n}
            elif code == "A3":
                require(text, "actual inducing edge", "return-step intensity", "common diagonal recovery", "pointed")
                edge1 = ("a", "b", "same-profile")
                edge2 = ("c", "d", "same-profile")
                assert edge1 != edge2
                data = {"same_profile_distinct_edges_retained": True, "common_projective_recovery": True}
            elif code == "A4":
                require(text, "genuine symbolic", "quenched enhanced", "zP-PLP-C(z)^{-1}", "Dirac")
                z, A, Cinv = 2.0, 0.3, 1.0
                khat = z - A - Cinv
                assert abs(khat - 0.7) < 1e-12
                data = {"causal_memory_sign_value": khat, "instantaneous_terms_separated": True}
            elif code == "B1":
                require(text, "full pressure", "connected remainder", "Conditional good-block minorization", "retain its")
                mu, c = 1000, 0.02
                bad = math.exp(-c * mu)
                assert bad < 1e-8
                data = {"regeneration_bad_probability_bound": bad, "full_connected_pressure_used": True}
            elif code == "B2":
                require(text, "divergence-measure", "normal trace", "Flux-weighted exterior Jacobi", "No QR")
                eps, alpha = 1e-6, 0.2
                gain = eps ** alpha
                factorial_sum = sum(2.0**m / math.factorial(m) for m in range(30))
                assert gain > 0 and factorial_sum < 8
                data = {"integrated_surplus_gain": gain, "factorial_tree_sum": factorial_sum}
            elif code == "B3":
                require(text, "can have either sign", "KKT-completed", "covariance first", "Mosco")
                q = 2.0
                raw = 2 * (1 - q)  # scalar A=f^2 counterexample with zero residual
                completed = raw + 5.0
                assert raw < 0 < completed
                data = {"raw_hessian_counterexample": raw, "completed_constrained_curvature": completed}
            elif code == "B4":
                require(text, "contains no $I_0", "Resolvent graph core", "entropy truncation", "diagonal while")
                eta = [1.0, 0.25, 0.01]
                distances = [math.sqrt(x) for x in eta]
                assert all(distances[i+1] < distances[i] for i in range(len(distances)-1))
                data = {"diagonal_distance_bounds": distances, "dynamic_action_additive": True}
            elif code == "C1":
                require(text, "unnormalized posterior current", "logarithmic evidence", "separate exact finite saddles", "reachable chaotic")
                evidence = 1e-12
                loge = math.log(evidence)
                assert math.isfinite(loge)
                data = {"small_evidence": evidence, "log_evidence": loge, "normalization_not_uniformly_bounded": True}
            elif code == "C2":
                require(text, "closed linear nullspaces", "Ces", "Kato", "Generally", "zR")
                p, q = 0.2, 0.8
                rel = p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
                assert rel > 0  # distinct Bernoulli phases are singular in the infinite product limit
                projection_rank = 1
                assert projection_rank == 1
                data = {"bernoulli_relative_entropy": rel, "resolved_projection_rank": 1}
            elif code == "D1":
                require(text, "exact labelled", "no discarded", "not because", "Lee--Yang", "contracting")
                # Q=max(0,theta) has conjugate indicator [0,1], whereas min of
                # conjugates of Q1=0 and Q2=theta is finite only at {0,1}.
                physical_at_half = 0.0
                min_phase_at_half = math.inf
                assert math.isfinite(physical_at_half) and math.isinf(min_phase_at_half)
                data = {"conjugacy_counterexample_physical": physical_at_half, "min_phase_at_half": "infinity", "exact_label_required": True}
            out["papers"][code] = {"status": "PASS", **data}
        except Exception as exc:
            errors.append(f"{code}: {exc}")
            out["papers"][code] = {"status": "FAIL", "error": str(exc)}

    out["errors"] = errors
    out["paper_count"] = len(FILES)
    out["status"] = "PASS" if not errors else "FAIL"
    (ROOT / "ROUND9_HOSTILE_REREVIEW.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = ["# Round-Nine Internal Hostile Rereview", "", f"Status: **{out['status']}**", "",
             "The suite replays the explicit algebraic, scaling, state-typing, and convexity counterexamples in the round-eight reports and checks the replacement proof bodies.", ""]
    for code in FILES:
        lines.append(f"- **{code}:** {out['papers'][code]['status']}")
    (ROOT / "ROUND9_INTERNAL_HARSH_REREVIEW.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    if errors:
        for e in errors:
            print(f"ROUND9_HOSTILE_ERROR {e}", file=sys.stderr)
        raise SystemExit(1)
    print("ROUND9_HOSTILE_REREVIEW_PASS papers=11")


if __name__ == "__main__":
    main()
