#!/usr/bin/env python3
"""Round-57 Gate-5 clearance-negative-moment / transport frontier.

This append-only leaf makes three exact refinements of the frozen Round-54--56
frontier without promoting a physical Gate-5 field.

* The optimal delayed-collar moment is quantitatively equivalent to the
  alpha_opt negative moment of the *same* physical clearance law.
* A deterministic unbounded suffix horizon can be replaced abstractly by a
  long/short joint ledger: recover the long part and pay raw collar debt only
  on the short exceptional part.
* Inside each immutable signed-current record, the truncated optimal
  transport cost is never worse than either the synchronised or normalized
  product coupling.  Weighted summability, not a uniform geometric rate, is
  the exact sufficient interface.

The frozen owner law is only a finite Borel law.  A countable-record separator
with B=14, full positive clearance, one other boundary per record and finite
parent Z_B has infinite alpha_opt negative moment.  Thus no physical weak
clearance theorem, same-operator join, suffix schedule, positive F10 or
cemetery conclusion is inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round57-clearance-negative-moment-ot-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": (
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b"
    ),
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": (
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5"
    ),
    "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json": (
        "ff54ad55f1e065ccf390f83a83cc6135aa22f0cabc7753fd700b38e05af1701c"
    ),
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json": (
        "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479"
    ),
}

BLOCK_DEPTH = 9148
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2
ALPHA_OPT_LOWER = Q(12406563164308641, 10**19)
ALPHA_OPT_UPPER = Q(12406563164308642, 10**19)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def decimal_constants() -> dict[str, Decimal]:
    with localcontext() as context:
        context.prec = 120
        gamma = (
            Decimal(2000)
            / Decimal(1999)
            * Decimal(1 + 48 * BLOCK_DEPTH)
            * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        )
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        weight = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * weight.ln() / Decimal(2).ln()
        inverse_square_q_limit = (Decimal(2) / Decimal(3)) / alpha
        return {
            "gamma": +gamma,
            "rho": +rho,
            "weight": +weight,
            "beta": +beta,
            "alpha_opt": +alpha,
            "inverse_square_pullback_power_limit": +inverse_square_q_limit,
        }


def optimal_clock(k: int, beta: Decimal | None = None) -> int:
    if k < 0:
        raise ValueError("negative collar level")
    if beta is None:
        beta = decimal_constants()["beta"]
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != expected:
            raise RuntimeError(f"dependency hash: {name}")
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_json_constant,
        )
        if not isinstance(value, dict):
            raise RuntimeError(f"dependency root: {name}")
        loaded[name] = value
    return loaded


def validate_dependencies() -> dict[str, dict[str, Any]]:
    loaded = load_dependencies()

    r56 = loaded[
        "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"
    ]["result"]
    clock = r56["optimal_exact_gamma_recovery_clock"]
    moment = r56["sharp_optimal_clock_weighted_moment"]
    if "ceil(beta*(k+1))" not in clock["exact_clock_definition"]:
        raise RuntimeError("Round56 optimal clock")
    if moment["optimal_critical_exponent"] != "alpha_opt=beta*log(w_Z)/log(2)":
        raise RuntimeError("Round56 alpha definition")
    if r56["strict_nonpromotion"]["physical_weak_clearance_moment"] != "NOT_CERTIFIED":
        raise RuntimeError("Round56 clearance frontier")
    if r56["strict_nonpromotion"]["physical_unbounded_compatible_suffix_schedule"] != "NOT_CERTIFIED":
        raise RuntimeError("Round56 suffix frontier")

    r55 = loaded[
        "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json"
    ]["result"]
    pairing = r55["synchronised_hit_miss_pairing"]
    if pairing["best_available_cost"] != "d_p^best=min(d_p^product,d_p^sync)":
        raise RuntimeError("Round55 best coupling")
    if pairing["physical_same_source_pair_rate"] != "NOT_CERTIFIED":
        raise RuntimeError("Round55 same-source frontier")

    r54 = loaded[
        "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
    ]["result"]["recordwise_owner_collar_E_Tr"]
    if "finite Borel measure" not in r54["trace_law_typing"]:
        raise RuntimeError("Round54 trace typing")
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 A_col frontier")
    separator = r54["parent_Z_does_not_control_collar_Z_separator"]
    if "p_k=2^(-k)" not in separator["law"] or "ell_k=2^(-k^2)" not in separator["law"]:
        raise RuntimeError("Round54 separator")

    r52 = loaded[
        "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"
    ]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["transfer_constant"] != "1" or r52["sums_over_insertion_times"] is not False:
        raise RuntimeError("Round52 transfer scope")
    if "4^(-b)" not in r52["transferred_rank_tail"]:
        raise RuntimeError("Round52 rank tail")

    dec = decimal_constants()
    alpha = dec["alpha_opt"]
    lo = Decimal(ALPHA_OPT_LOWER.numerator) / Decimal(ALPHA_OPT_LOWER.denominator)
    hi = Decimal(ALPHA_OPT_UPPER.numerator) / Decimal(ALPHA_OPT_UPPER.denominator)
    if not Q(4999, 10000) < GAMMA < Q(1, 2):
        raise RuntimeError("gamma arithmetic")
    if not Q(1) < W_Z < Q(2):
        raise RuntimeError("weight arithmetic")
    if not lo < alpha < hi:
        raise RuntimeError("alpha arithmetic")
    return loaded


def equivalence_rows() -> list[dict[str, Any]]:
    beta = decimal_constants()["beta"]
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4381, 10000):
        rows.append(
            {
                "dyadic_level_k": k,
                "optimal_clock_r_k": optimal_clock(k, beta),
                "clearance_cell": (
                    "delta=1" if k == 0 else "2^(-k)<=delta<2^(-(k-1))"
                ),
                "pointwise_comparison": (
                    "w_Z^beta*delta^(-alpha_opt)<=w_Z^r_k<"
                    "w_Z^(beta+1)*2^alpha_opt*delta^(-alpha_opt)"
                ),
            }
        )
    return rows


def exact_negative_moment_equivalence() -> dict[str, Any]:
    dec = decimal_constants()
    rows = equivalence_rows()
    return {
        "same_law_variables": (
            "on the actual owner law nu restricted to A_col, set "
            "delta(omega)=min(1,d_other(omega))>0 and use the exact Round54 "
            "dyadic level k(omega) and Round56 clock r_k"
        ),
        "critical_order": "alpha_opt=beta*log(w_Z)/log(2)",
        "alpha_opt_decimal_120_digit_audit": format(dec["alpha_opt"], "f"),
        "clock_moment": "M_clock=integral w_Z^r_(k(omega)) dnu=sum_k w_Z^r_k*m_k",
        "negative_clearance_moment": "M_neg=integral delta(omega)^(-alpha_opt) dnu",
        "pointwise_two_sided_bound": (
            "w_Z^beta*delta^(-alpha_opt)<=w_Z^r_k<"
            "w_Z^(beta+1)*2^alpha_opt*delta^(-alpha_opt)"
        ),
        "integrated_two_sided_bound": (
            "w_Z^beta*M_neg<=M_clock<"
            "w_Z^(beta+1)*2^alpha_opt*M_neg"
        ),
        "finiteness_equivalence": "M_clock<infinity iff M_neg<infinity",
        "layer_cake_identity": (
            "M_neg=nu(A_col)+alpha_opt*integral_0^1 "
            "t^(-alpha_opt-1)*nu{delta<t} dt"
        ),
        "power_tail_sufficient_condition": (
            "nu{delta<t}<=C*t^eta with eta>alpha_opt implies "
            "M_neg<=nu(A_col)+alpha_opt*C/(eta-alpha_opt)"
        ),
        "critical_Dini_sufficient_condition": (
            "nu{delta<t}<=C*t^alpha_opt/(log(e/t))^(1+epsilon) implies "
            "M_neg<=nu(A_col)+alpha_opt*C/epsilon"
        ),
        "critical_log_separator": (
            "the probability CDF F(t)=t^alpha_opt/log(e/t), 0<t<=1, "
            "has the critical power but infinite alpha_opt negative moment"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "physical_same_law_negative_moment": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_OPTIMAL_CLOCK_NEGATIVE_MOMENT_EQUIVALENCE",
    }


def pullback_minkowski_dini_route() -> dict[str, Any]:
    dec = decimal_constants()
    return {
        "recordwise_hypotheses": (
            "write nu=sum_a nu_a; in a collar coordinate c, assume "
            "dnu_a/dc<=D_a, Leb{dist(c,E_a)<epsilon}<=A_a*epsilon^eta, "
            "and delta_a>=g_a*dist(c,E_a)^q for 0<g_a<=1"
        ),
        "recordwise_tail": (
            "nu_a{delta_a<t}<=D_a*A_a*g_a^(-eta/q)*t^(eta/q)"
        ),
        "aggregate_constant": (
            "C_pull=sum_a D_a*A_a*g_a^(-eta/q); uniform boundedness of "
            "D_a,A_a,g_a^(-1) is unnecessary if this sum is finite"
        ),
        "sharp_exponent_condition": "eta/q>alpha_opt",
        "aggregate_conclusion": (
            "if C_pull<infinity and eta/q>alpha_opt, then the exact same-law "
            "M_neg and hence the optimal delayed-collar moment are finite"
        ),
        "inverse_square_specialisation": (
            "Round56 gives eta=2/3 for the abstract inverse-square shell; "
            "it tolerates any pullback power q<(2/3)/alpha_opt provided the "
            "record constants are summable"
        ),
        "inverse_square_pullback_power_limit_decimal": format(
            dec["inverse_square_pullback_power_limit"], "f"
        ),
        "strict_gain_over_uniform_route": (
            "the sufficient interface is summability of the recordwise "
            "Minkowski-density-gap constants, not separate uniform density, "
            "uniform finite boundary count and uniform bi-Lipschitz gap"
        ),
        "physical_owner_density_bound": "NOT_CERTIFIED",
        "physical_full_word_Minkowski_constants": "NOT_CERTIFIED",
        "physical_pullback_gap_summability": "NOT_CERTIFIED",
        "status": "CERTIFIED_CONDITIONAL_SUMMABLE_PULLBACK_MINKOWSKI_ROUTE",
    }


def separator_rows() -> list[dict[str, Any]]:
    alpha = decimal_constants()["alpha_opt"]
    rows: list[dict[str, Any]] = []
    for n in (1, 100, 500, 805, 806, 807, 1000, 2000):
        exponent = alpha * Decimal(n * n) - Decimal(n)
        rows.append(
            {
                "record_n": n,
                "mass_p_n": "2^(-n)",
                "clearance_d_n": "2^(-n^2)",
                "dyadic_level": n * n,
                "log2_negative_moment_term": format(exponent, "f"),
            }
        )
    return rows


def rank_tail_nonimplication_separator() -> dict[str, Any]:
    rows = separator_rows()
    return {
        "law": (
            "on disjoint records a_n, n>=1, put p_n=2^(-n), parent length "
            "one, B_n=14 and one other analytic boundary at distance "
            "d_n=2^(-n^2) from the owned anchor"
        ),
        "total_mass": "sum_n p_n=1",
        "A_col_mass": "nu(A_col)=1 and nu{d_other=0}=0",
        "boundary_complexity": (
            "each record has exactly one other boundary and identity pullback; "
            "only the cross-record gap d_n collapses"
        ),
        "parent_debts": "Z_parent=1 and Z_parent,B=2^14=16384",
        "fixed_insertion_rank_tail": (
            "nu{B>b}=0 for every b>=14, stronger than the frozen Round52 "
            "constant-one 4^(-b) upper tail"
        ),
        "all_positive_rank_moments": "integral 2^(qB)dnu=2^(14q)<infinity for every finite q",
        "raw_collar_debt": "sum_n p_n*2^(n^2+1)=infinity",
        "negative_moment": (
            "sum_n p_n*d_n^(-alpha_opt)=sum_n "
            "2^(alpha_opt*n^2-n)=infinity because its terms tend to infinity"
        ),
        "optimal_clock_moment": (
            "infinite by the certified two-sided equivalence, even though the "
            "pointwise Round56 recovery clock exists on every record"
        ),
        "logical_conclusion": (
            "full positive clearance, finite per-record boundary complexity, "
            "finite parent Z_B and every fixed-insertion source-rank moment do "
            "not imply the physical weak-clearance moment"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_RANK_TAIL_DOES_NOT_IMPLY_OPTIMAL_CLEARANCE_MOMENT",
    }


def hybrid_suffix_horizon_criterion() -> dict[str, Any]:
    return {
        "joint_split": (
            "for level k, let L_k={available compatible horizon H>=r_k} and "
            "S_k={H<r_k}; write masses m_k^long and m_k^short"
        ),
        "long_part": (
            "on L_k, under the exact Round54/Round42 same-ID same-operator "
            "join, recovery costs at most C_rec*w_Z^r_k*m_k^long"
        ),
        "short_part": (
            "on S_k, retain the unrecovered collar and pay its exact direct "
            "shape debt 2^(k+1)*m_k^short; short mass alone is insufficient"
        ),
        "mixed_ledger": (
            "Q_hybrid<=C_rec*sum_k w_Z^r_k*m_k^long+"
            "sum_k 2^(k+1)*m_k^short"
        ),
        "abstract_sufficient_condition": (
            "both displayed sums finite; this replaces pointwise unbounded "
            "horizon by a joint clearance-horizon exceptional-debt condition"
        ),
        "strict_scope": (
            "the theorem is an accounting refinement only; operator typing, "
            "post-recovery norm entry and the direct short-part standard-family "
            "join must all hold on the same immutable IDs"
        ),
        "physical_same_operator_long_join": "NOT_CERTIFIED",
        "physical_short_horizon_direct_debt": "NOT_CERTIFIED",
        "physical_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "status": "CERTIFIED_CONDITIONAL_LONG_SHORT_HYBRID_SUFFIX_LEDGER",
    }


def transport_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in (0, 1, 2, 8, 32):
        rows.append(
            {
                "block_p": p,
                "critical_polynomial_cost": "w_Z^(-p)/(p+1)^2",
                "weighted_term": f"1/{(p + 1) ** 2}",
            }
        )
    return rows


def optimal_transport_frontier() -> dict[str, Any]:
    rows = transport_rows()
    return {
        "scope": (
            "inside one immutable physical record/rank p, with equal-mass "
            "positive Jordan image marginals mu_p^+,mu_p^- on a metric target"
        ),
        "truncated_cost": "c(y+,y-)=min(2,d(y+,y-))",
        "optimal_transport_scalar": (
            "d_p^OT=inf_{pi in Couplings(mu_p^+,mu_p^-)} integral c d pi"
        ),
        "no_selection_claim": (
            "the scalar infimum is used; no continuously indexed measurable "
            "optimal-coupling kernel or physical operator is asserted"
        ),
        "BL_bound": "norm(J_p)_(BL*)<=d_p^OT",
        "dominance": (
            "d_p^OT<=min(d_p^sync,d_p^product)=d_p^best"
        ),
        "strict_flip_example": (
            "for uniform lambda on {0,1}, H=identity and M=flip, one has "
            "mu^+=mu^-=uniform, d_OT=0<d_best=1/2<d_sync=1"
        ),
        "exact_weighted_interface": (
            "sum_p w_Z^p*d_p^OT<infinity implies sum_p "
            "w_Z^p*norm(J_p)_(BL*)<infinity"
        ),
        "good_bad_source_bound": (
            "for any admissible coupling of mass m_p with distance<=epsilon_p "
            "off a bad set of coupling mass b_p, d_p^OT<=m_p*epsilon_p+2*b_p"
        ),
        "critical_polynomial_route": (
            "d_p^OT<=w_Z^(-p)/(p+1)^2 gives weighted sum <=2"
        ),
        "strictly_weaker_than_geometric_rate": (
            "w_Z^(-p)/(p+1)^2 is not bounded by C*delta^p for any finite C "
            "and delta<1/w_Z"
        ),
        "critical_rows": rows,
        "critical_rows_sha256": digest(rows),
        "physical_OT_or_good_bad_decay": "NOT_CERTIFIED",
        "positive_F10_or_cemetery_consequence": "NOT_CERTIFIED",
        "status": "CERTIFIED_TRUNCATED_OT_DOMINANCE_AND_WEIGHTED_SUMMABILITY_ROUTE",
    }


def latest_technology_audit() -> dict[str, Any]:
    return {
        "official_query_date": "2026-07-20",
        "official_source": "export.arxiv.org API",
        "queries": [
            "dispersing billiards / standard families / moving billiards, 2025-2026",
            "Sinai billiards linear response, 2025-2026",
            "normal trace divergence-measure fields, 2025-2026",
        ],
        "relevant_versions": [
            "2606.10155v1",
            "2604.19671v2",
            "2503.09536v2",
            "2607.11467v1",
        ],
        "direct_owner_clearance_or_same_source_theorem_found": False,
        "why_not_imported": (
            "the billiard sources do not provide the same owner-law negative "
            "clearance moment, full-word pullback-Minkowski constants or a "
            "hit/miss image transport decay; the trace papers provide signed "
            "normal-trace spaces/Gauss-Green theory but not positivity, owner IDs, "
            "the killed C24 operator join or numerical suffix scheduling"
        ),
        "external_source_used_as_dependency": False,
        "status": "CHECKED_NO_DIRECT_PHYSICAL_GATE5_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "optimal_clock_negative_moment_equivalence": "CERTIFIED",
        "critical_Dini_clearance_frontier": "CERTIFIED",
        "summable_pullback_Minkowski_route": "CERTIFIED_CONDITIONAL",
        "fixed_insertion_rank_tail_implies_weak_clearance": "FALSE_BY_CERTIFIED_SEPARATOR",
        "hybrid_long_short_suffix_ledger": "CERTIFIED_CONDITIONAL",
        "truncated_optimal_transport_BL_bound": "CERTIFIED",
        "OT_cost_never_worse_than_Round55_best": "CERTIFIED",
        "critical_polynomial_weighted_BL_route": "CERTIFIED_CONDITIONAL",
        "physical_same_law_negative_clearance_moment": "NOT_CERTIFIED",
        "physical_owner_density_or_Minkowski_constants": "NOT_CERTIFIED",
        "physical_pullback_gap_summability": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_unbounded_or_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "physical_same_source_or_OT_decay": "NOT_CERTIFIED",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
        "positive_F10_from_signed_transport": "NOT_CERTIFIED",
        "complete_all_face_F10": "NOT_CERTIFIED",
        "strong_F13": "NOT_CERTIFIED",
        "F14_F15_F17_F18": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": (
                "the collar statements use the frozen fixed-|s|<=1/400 "
                "Round54--56 owner/collar interface; the transport statement is "
                "recordwise at s=0; no moving-map sequence is asserted"
            ),
            "claim_type": (
                "exact optimal-clock negative-moment equivalence, summable "
                "pullback/Dini and hybrid-suffix frontiers, rank-tail "
                "nonimplication, and recordwise truncated-transport improvement"
            ),
        },
        "exact_clearance_negative_moment_equivalence": exact_negative_moment_equivalence(),
        "recordwise_pullback_minkowski_dini_route": pullback_minkowski_dini_route(),
        "rank_tail_optimal_clock_nonimplication_separator": rank_tail_nonimplication_separator(),
        "hybrid_suffix_horizon_criterion": hybrid_suffix_horizon_criterion(),
        "recordwise_truncated_transport_BL_frontier": optimal_transport_frontier(),
        "latest_technology_audit": latest_technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "exact optimal-clock/negative-clearance-moment equivalence",
                "critical Dini and summable pullback-Minkowski criterion",
                "fixed-rank-tail optimal-clock nonimplication separator",
                "conditional long/short hybrid suffix ledger",
                "truncated optimal-transport dominance over both Round55 witnesses",
                "critical-polynomial weighted signed-BL route",
            ],
            "reason_no_new_field_credit": (
                "the physical same-law negative moment, pullback constants, "
                "same-operator join, joint suffix ledger and signed transport "
                "decay are absent; signed cancellation cannot pay positive mass"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": strict_nonpromotion(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(verifier: Path) -> bytes:
    return (
        json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode()


def write_manifest(path: Path, verifier: Path) -> None:
    path.write_bytes(render_manifest(verifier))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(HERE / "cm2_gate5_round57_clearance_negative_moment_ot_frontier_verifier.py"),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("NEGATIVE_MOMENT_EQUIVALENCE:", strict["optimal_clock_negative_moment_equivalence"])
    print("OT_DOMINANCE:", strict["OT_cost_never_worse_than_Round55_best"])
    print("PHYSICAL_WEAK_CLEARANCE:", strict["physical_same_law_negative_clearance_moment"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
