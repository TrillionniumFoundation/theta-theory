#!/usr/bin/env python3
"""Round-58 Gate-5 owner-ledger / positive-transport frontier.

This append-only leaf audits the complete Round-49--57 Gate-5 owner/collar
chain together with the numerical Round-42 C24 Growth block.  It constructs
the strongest object actually available on the physical owner/root law: a
Borel, extended-valued dyadic clearance ledger and its exact Abel tail
identity.  Finiteness, full A_col coverage, a compatible suffix horizon and
the same-operator tag are deliberately not inferred.

The leaf also repairs the typing of the Round-57 density route.  A root atom
integrated over parent curves is not a density along a collar coordinate, and
the artificial uniform E_j collar density is ell(a)^(-1); aggregating it is
exactly the missing raw collar Z debt.  A valid kernel-disintegrated
Minkowski-density-gap theorem is stated conditionally.

Finally, it proves two sharp separations.  The same physical clearance/rank
marginal has a finite recovered ledger under a long aligned completion and an
infinite raw debt under a short/misaligned completion.  Moreover signed
optimal-transport cost may vanish identically while the positive collar and
cemetery-weighted charge is infinite.  Hence cancellation cannot promote a
positive F10 or strong cemetery field.
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
RESULT_SCHEMA = "cm2.gate5.round58-owner-ledger-positive-transport-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json": (
        "1a53a0bac41f6c0d6f8155c69b67daf31337b5f13578af9fb9f497d16277d6ad"
    ),
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": (
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46"
    ),
    "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json": (
        "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5"
    ),
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": (
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b"
    ),
    "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json": (
        "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590"
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
    "cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json": (
        "89d2bed9f93140637d6079d7b425ce44ed1541e2da59776a446f4bd0f428c0f3"
    ),
}

BLOCK_DEPTH = 9148
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2


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
        return {
            "gamma": +gamma,
            "rho": +rho,
            "weight": +weight,
            "beta": +beta,
            "alpha_opt": +alpha,
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

    r42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    growth = r42["numerical_C24_killed_Growth"]
    if growth["block_depth_n_star"] != BLOCK_DEPTH:
        raise RuntimeError("Round42 block depth")
    if growth["block_bound"] != "Z(O_s^9148 G)<=gamma*Z(G)+Z0*mass(G)":
        raise RuntimeError("Round42 operator recurrence")
    if growth["hereditary_under_positive_C24_killing"] is not True:
        raise RuntimeError("Round42 killing scope")

    r49 = loaded[
        "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    if r49["F17_suffix_product_countermodel"]["joint_insertion_suffix_rank_tail"] != "NOT_CERTIFIED":
        raise RuntimeError("Round49 joint suffix frontier")

    r50 = loaded[
        "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
    ]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if r50["index_space_is_standard_Borel"] is not True:
        raise RuntimeError("Round50 Borel owner registry")
    if r50["finite_after_sum_over_all_depths"] != "NOT_CERTIFIED":
        raise RuntimeError("Round50 aggregate frontier")

    r51 = loaded[
        "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"
    ]["result"]["common_dynamic_suffix_envelope"]
    if "all finite regular suffix branches" not in r51["regular_suffix_registry"]:
        raise RuntimeError("Round51 suffix registry")
    if r51["F17_dynamic_test_operator_cost"] != "NOT_CERTIFIED":
        raise RuntimeError("Round51 operator frontier")

    r52 = loaded[
        "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"
    ]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["transfer_constant"] != "1" or r52["sums_over_insertion_times"] is not False:
        raise RuntimeError("Round52 fixed-time scope")
    if "4^(-b)" not in r52["transferred_rank_tail"]:
        raise RuntimeError("Round52 rank tail")

    r53 = loaded[
        "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json"
    ]["result"]["transverse_trace_standard_family_audit"]
    if "root atom" not in r53["typed_owner_law"]:
        raise RuntimeError("Round53 owner law type")
    if r53["owner_trace_is_an_unstable_standard_family_law"] is not False:
        raise RuntimeError("Round53 trace/family separator")

    r54 = loaded[
        "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
    ]["result"]["recordwise_owner_collar_E_Tr"]
    if "finite Borel measure" not in r54["trace_law_typing"]:
        raise RuntimeError("Round54 owner law")
    if "measurable integer minima" not in r54["canonical_Borel_selection"]:
        raise RuntimeError("Round54 Borel selector")
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 coverage frontier")
    if "finiteness is NOT_CERTIFIED" not in r54["standard_family_shape_debt"]:
        raise RuntimeError("Round54 raw debt frontier")

    r55 = loaded[
        "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json"
    ]["result"]["dyadic_debt_layer_delayed_recovery"]
    if r55["physical_Round54_to_Round42_same_operator_join"] != "NOT_CERTIFIED":
        raise RuntimeError("Round55 same-operator frontier")
    if r55["physical_k_plus_1_C24_suffix_schedule"] != "NOT_CERTIFIED":
        raise RuntimeError("Round55 horizon frontier")

    r56 = loaded[
        "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"
    ]["result"]["optimal_exact_gamma_recovery_clock"]
    if "ceil(beta*(k+1))" not in r56["exact_clock_definition"]:
        raise RuntimeError("Round56 clock")

    r57 = loaded[
        "cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json"
    ]["result"]
    if r57["exact_clearance_negative_moment_equivalence"]["physical_same_law_negative_moment"] != "NOT_CERTIFIED":
        raise RuntimeError("Round57 physical moment frontier")
    if r57["hybrid_suffix_horizon_criterion"]["physical_hybrid_suffix_schedule"] != "NOT_CERTIFIED":
        raise RuntimeError("Round57 hybrid frontier")

    if not Q(4999, 10000) < GAMMA < Q(1, 2):
        raise RuntimeError("gamma arithmetic")
    if not Q(1) < W_Z < Q(4, 3):
        raise RuntimeError("weight arithmetic")
    return loaded


def audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "leaf": "Round49",
            "available": "typed fixed-record measures and suffix-product nonimplication",
            "missing_for_owner_clock": "joint insertion/suffix law",
        },
        {
            "leaf": "Round50",
            "available": "global standard-Borel owner-deduplicated root registry",
            "missing_for_owner_clock": "finite all-depth owner aggregate",
        },
        {
            "leaf": "Round51",
            "available": "registry of all finite regular suffix branches",
            "missing_for_owner_clock": "a selected compatible horizon and physical operator embedding",
        },
        {
            "leaf": "Round52",
            "available": "constant-one fixed-insertion source-rank B tail",
            "missing_for_owner_clock": "all-time sum and any comparison B versus clearance K",
        },
        {
            "leaf": "Round53",
            "available": "owner root atom over the outer parent law",
            "missing_for_owner_clock": "collar-coordinate absolute continuity/density",
        },
        {
            "leaf": "Round54",
            "available": "Borel A_col, clearance d, level K, collar ell and labelled E/Tr",
            "missing_for_owner_clock": "A_col coverage and aggregate collar debt",
        },
        {
            "leaf": "Round55",
            "available": "conditional delayed recovery and exact required tags",
            "missing_for_owner_clock": "physical same-operator join and compatible horizon",
        },
        {
            "leaf": "Round56",
            "available": "pointwise minimal exact-gamma clock r_K",
            "missing_for_owner_clock": "same-law clock moment and post-recovery join",
        },
        {
            "leaf": "Round57",
            "available": "negative-moment equivalence and conditional hybrid ledger",
            "missing_for_owner_clock": "finite physical moment, H/J joint law and positive lift",
        },
        {
            "leaf": "Round42",
            "available": "numerical positive killed C24 operator recurrence O_s^9148",
            "missing_for_owner_clock": "Gate5 owner/event/side/word-cell domain equality",
        },
    ]


def frozen_chain_audit() -> dict[str, Any]:
    rows = audit_rows()
    return {
        "scope": "all targeted owner/collar/suffix manifests Round49--57 plus the numerical Round42 block",
        "rows": rows,
        "rows_sha256": digest(rows),
        "positive_findings": (
            "the owner/root registry, A_col predicate, clearance d, dyadic K and "
            "minimal clock r_K are Borel on one retained physical law"
        ),
        "negative_findings": (
            "no frozen field supplies a finite same-law clearance moment, a "
            "compatible block horizon H, or the same-operator Boolean J"
        ),
        "rank_scope_guard": (
            "the Round52 mark B is source incidence rank; no frozen inequality "
            "controls the independent full-word clearance level K by B"
        ),
        "status": "CERTIFIED_COMPLETE_FROZEN_CHAIN_FIELD_AUDIT",
    }


def tail_rows() -> list[dict[str, Any]]:
    beta = decimal_constants()["beta"]
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4381, 10000):
        rows.append(
            {
                "level_K": k,
                "clock_r_K": optimal_clock(k, beta),
                "weight_a_K": f"w_Z^{optimal_clock(k, beta)}",
                "tail_increment": (
                    f"w_Z^{optimal_clock(k + 1, beta)}-w_Z^{optimal_clock(k, beta)}"
                ),
            }
        )
    return rows


def same_owner_extended_ledger() -> dict[str, Any]:
    rows = tail_rows()
    return {
        "physical_base": (
            "the Round50/54 standard-Borel owner/root base with its actual finite "
            "Borel law nu, restricted without normalization to A_col"
        ),
        "Borel_marks": (
            "delta(a)=min(1,d_other(a)), K(a)=min{k>=0:2^-k<=delta(a)}, "
            "ell(a)=2^(-(K(a)+1)) and r(a)=r_K(a) are Borel"
        ),
        "level_law": "m_k=nu({a in A_col:K(a)=k})",
        "extended_clock_ledger": "M_clock=sum_(k>=0) w_Z^r_k*m_k in [0,infinity]",
        "tail_function": "F_j=nu({a in A_col:K(a)>j})",
        "exact_Abel_identity": (
            "M_clock=w_Z^r_0*nu(A_col)+sum_(j>=0)"
            "(w_Z^r_(j+1)-w_Z^r_j)*F_j"
        ),
        "truncation": (
            "every M_clock^(N)=sum_(k<=N)w_Z^r_k*m_k is finite and increases "
            "to M_clock; this does not bound the limit"
        ),
        "coverage_axis": (
            "this ledger covers only A_col; a complete positive bridge also "
            "needs nu(A_col^c)=0 or a separately typed positive cemetery charge"
        ),
        "coverage_not_certified": "nu(A_col^c)=0 is NOT_CERTIFIED",
        "finiteness_not_certified": "M_clock<infinity is NOT_CERTIFIED",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE",
    }


def density_typing_frontier() -> dict[str, Any]:
    return {
        "root_law_type": (
            "Round53 selects one root atom xi(W) on each parent W and integrates "
            "that atom against the outer parent law; it is not an along-collar density"
        ),
        "why_recordwise_Da_is_not_frozen": (
            "conditioning on the complete owner/root record leaves a Dirac root, "
            "so dnu_a/dc<=D_a is not a certified density statement"
        ),
        "artificial_extension_density": (
            "Round54 E_a spreads that root uniformly on a synthetic collar with "
            "conditional density D_ext(a)=ell(a)^(-1)"
        ),
        "extension_aggregate_identity": (
            "integral_(A_col)D_ext(a)dnu(a)=integral ell(a)^(-1)dnu(a)="
            "sum_k 2^(k+1)m_k=Z_col"
        ),
        "no_gain_from_constant_density": (
            "using the E_a constant density therefore assumes exactly the missing "
            "raw collar debt, which is stronger than the optimal weak moment"
        ),
        "correct_kernel_hypotheses": (
            "choose a coarser standard-Borel chart base (b,lambda) and a genuine "
            "conditional kernel nu_b(dc); require dnu_b/dc<=D_b, "
            "Leb{dist(c,E_b)<epsilon}<=A_b*epsilon^eta, and "
            "delta_b(c)>=g_b*dist(c,E_b)^q"
        ),
        "kernel_tail_bound": (
            "nu{delta<t}<=t^(eta/q)*integral D_b*A_b*g_b^(-eta/q)dlambda(b)"
        ),
        "kernel_sufficient_ledger": (
            "C_pull=integral D_b*A_b*g_b^(-eta/q)dlambda(b)<infinity and "
            "eta/q>alpha_opt imply M_clock<infinity"
        ),
        "missing_kernel_fields": [
            "a common coarsened chart/disintegration retaining owner IDs",
            "conditional absolute continuity on the actual law",
            "full-word boundary Minkowski constants",
            "a pullback gap lower bound and integrable joint constant",
        ],
        "physical_D_A_g_ledger_finite": "NOT_CERTIFIED",
        "status": "CERTIFIED_ROOT_ATOM_DENSITY_TYPE_AUDIT_AND_KERNEL_ROUTE",
    }


def completion_rows() -> list[dict[str, Any]]:
    beta = decimal_constants()["beta"]
    rows: list[dict[str, Any]] = []
    for n in (0, 1, 2, 4, 8, 16):
        k = 2 * n
        r = optimal_clock(k, beta)
        rows.append(
            {
                "n": n,
                "mass": f"2^-{n + 1}",
                "K": k,
                "r_K": r,
                "aligned_H": r,
                "short_H": 0,
                "raw_term": f"2^{n}",
            }
        )
    return rows


def horizon_operator_frontier() -> dict[str, Any]:
    rows = completion_rows()
    return {
        "missing_marks": (
            "H(a)=number of consecutive compatible 9148-collision blocks after "
            "insertion and J(a)=1 iff the labelled Round54 word is the exact "
            "Round42 O_s^9148 input/output chain"
        ),
        "joint_law_if_supplied": "Lambda=(K,H,J)_#(nu|A_col) on N x N x {0,1}",
        "canonical_positive_policy": (
            "recover when J=1 and H>=r_K; otherwise retain the collar and pay raw debt"
        ),
        "policy_ledger": (
            "Q_policy=integral[1_{J=1,H>=r_K}*C_rec*w_Z^r_K+"
            "1_{J=0 or H<r_K}*2^(K+1)]dnu"
        ),
        "exact_policy_criterion": (
            "Q_policy<infinity iff its aligned-long recovered integral and its "
            "misaligned-or-short raw-debt integral are both finite"
        ),
        "why_Round51_is_not_H": (
            "a registry of every finite regular suffix branch is not a selected "
            "same-law compatible horizon and carries no residual-block distribution"
        ),
        "why_Round54_Round42_do_not_compose_yet": (
            "Round54 retains owner/event/side/word-cell tags for K_word, while "
            "Round42 proves a recurrence on O_s^9148; no frozen equality of their "
            "domains, killed bits and outputs is asserted"
        ),
        "typed_noncomposition_separator": (
            "a contraction on a disjoint tagged carrier has the same scalar "
            "recurrence but gives no bound on the collar carrier; scalar constants "
            "cannot replace domain/tag equality"
        ),
        "same_marginal_separator": {
            "law": (
                "on levels K=2n put mass m_n=2^(-(n+1)), B=14, full A_col and "
                "the same owner/root labels in both completions"
            ),
            "aligned_completion": "J=1 and H=r_K on every level",
            "aligned_bound": (
                "because r_(2n)<=2n+1 and w_Z^2/2<1, sum m_n*w_Z^r_(2n)"
                "<=(w_Z/2)/(1-w_Z^2/2)<infinity"
            ),
            "short_completion": "J=0 and H=0 on every level",
            "short_divergence": (
                "sum m_n*2^(K+1)=sum_n 2^n=infinity"
            ),
            "logical_conclusion": (
                "the complete frozen K/clearance/owner/rank marginal cannot imply "
                "a hybrid suffix ledger without the H/J joint law"
            ),
        },
        "rows": rows,
        "rows_sha256": digest(rows),
        "physical_H_joint_law": "NOT_CERTIFIED",
        "physical_J_same_operator": "NOT_CERTIFIED",
        "physical_short_debt": "NOT_CERTIFIED",
        "status": "CERTIFIED_MINIMAL_K_H_J_POLICY_AND_TWO_COMPLETION_SEPARATOR",
    }


def positive_transport_rows() -> list[dict[str, Any]]:
    alpha = decimal_constants()["alpha_opt"]
    rows: list[dict[str, Any]] = []
    for n in (1, 100, 806, 807, 1000, 2000):
        exponent = alpha * Decimal(n * n) - Decimal(n)
        rows.append(
            {
                "record_n": n,
                "Jordan_mass_each_sign": "2^(-n)",
                "clearance": "2^(-n^2)",
                "d_OT": "0",
                "log2_one_sign_positive_term": format(exponent, "f"),
            }
        )
    return rows


def positive_transport_frontier() -> dict[str, Any]:
    rows = positive_transport_rows()
    return {
        "signed_scope": (
            "for equal-mass positive Jordan marginals mu^+,mu^- and any coupling "
            "pi, truncated OT bounds only J=mu^+-mu^- in BL*"
        ),
        "positive_cost_identity": (
            "for every nonnegative Borel charge a, integral[a(y+)+a(y-)]dpi="
            "integral a dmu^+ + integral a dmu^-; it is coupling-independent"
        ),
        "necessary_and_sufficient_positive_interface": (
            "the positive a-charge is finite iff that coupling-independent "
            "two-marginal moment is finite; minimizing displacement cannot reduce it"
        ),
        "conditional_transport_lift": (
            "if a(y+)<=C*a(y-)+L*c(y+,y-) pi-a.e., then integral a dmu^+"
            "<=C*integral a dmu^-+L*integral c dpi; one finite positive anchor "
            "moment is still indispensable"
        ),
        "zero_cost_infinite_positive_separator": (
            "on record n put mu_n^+=mu_n^-=2^-n*delta_(x_n), B=14 and "
            "d_n=2^(-n^2); then J_n=0 and d_n^OT=0 for every n, but for "
            "a_n=d_n^(-alpha_opt) each sign has sum 2^(alpha_opt*n^2-n)=infinity"
        ),
        "strong_cemetery_separator": (
            "send both equal Jordan marginals to the same cemetery-labelled atom "
            "with charge a_n; signed cemetery current is zero while positive total "
            "variation/weighted charge is infinite"
        ),
        "all_signed_weighted_resolvents": "identically zero in the separator",
        "full_A_col_and_rank_fields": (
            "nu(A_col)=1, one other boundary per record, B=14, finite parent Z_B "
            "and every fixed source-rank moment"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "positive_F10_from_signed_OT": "FALSE_BY_CERTIFIED_SEPARATOR",
        "strong_cemetery_from_signed_OT": "FALSE_BY_CERTIFIED_SEPARATOR",
        "status": "CERTIFIED_COUPLING_INVARIANT_POSITIVE_COST_BOUNDARY",
    }


def coverage_frontier() -> dict[str, Any]:
    return {
        "axis_one": (
            "full A_col coverage does not imply M_clock<infinity: the pinned "
            "Round57 B=14, d_n=2^(-n^2), p_n=2^-n separator has full coverage "
            "and infinite moment"
        ),
        "axis_two": (
            "M_clock on A_col may equal zero when A_col is empty while the whole "
            "owner law remains uncovered; thus a finite restricted ledger does not "
            "imply a complete positive bridge"
        ),
        "joint_requirement": (
            "a complete collar route needs both nu(A_col^c)=0 (or a strong positive "
            "cemetery theorem) and M_clock<infinity on A_col"
        ),
        "status": "CERTIFIED_COVERAGE_AND_MOMENT_LOGICAL_INDEPENDENCE",
    }


def latest_technology_audit() -> dict[str, Any]:
    return {
        "official_query_date": "2026-07-20",
        "official_source": "export.arxiv.org API",
        "queries": [
            "signed optimal transport / unbalanced optimal transport",
            "dispersing billiards / Sinai billiards / standard families",
        ],
        "new_relevant_version": "2606.19621v2",
        "new_relevant_title": (
            "Regularity of the positional penalization function in inter-sign "
            "optimal transport on real measures"
        ),
        "why_not_imported": (
            "the paper studies feasibility, duality and regularity for signed "
            "transport with matched Jordan masses; it does not turn cancellation "
            "cost into an unbounded positive collar moment or strong cemetery norm. "
            "The current billiard review/linear-response sources still do not "
            "supply the owner-clearance H/J join"
        ),
        "direct_physical_Gate5_import_found": False,
        "external_source_used_as_dependency": False,
        "status": "CHECKED_NO_DIRECT_OWNER_LEDGER_OR_POSITIVE_LIFT_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "physical_same_law_extended_clearance_ledger": "CERTIFIED_BOREL_EXTENDED_VALUED",
        "physical_same_law_clearance_ledger_finite": "NOT_CERTIFIED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "physical_D_A_g_kernel_ledger_finite": "NOT_CERTIFIED",
        "physical_clearance_horizon_joint_law": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_short_horizon_debt": "NOT_CERTIFIED",
        "physical_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "clearance_marginal_implies_hybrid_suffix": "FALSE_BY_CERTIFIED_SEPARATOR",
        "signed_OT_implies_positive_F10": "FALSE_BY_CERTIFIED_SEPARATOR",
        "signed_OT_implies_strong_cemetery": "FALSE_BY_CERTIFIED_SEPARATOR",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
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
                "the physical owner/collar audit has the frozen fixed-|s|<=1/400 "
                "scope; the signed transport separator is recordwise at s=0"
            ),
            "claim_type": (
                "same-owner extended ledger, root-density type audit, minimal K/H/J "
                "policy, two-completion nonimplication and positive-transport boundary"
            ),
        },
        "frozen_chain_field_audit": frozen_chain_audit(),
        "physical_same_owner_extended_clearance_ledger": same_owner_extended_ledger(),
        "root_density_kernelised_pullback_frontier": density_typing_frontier(),
        "clearance_horizon_same_operator_frontier": horizon_operator_frontier(),
        "signed_OT_positive_charge_frontier": positive_transport_frontier(),
        "A_col_coverage_moment_independence": coverage_frontier(),
        "latest_technology_audit": latest_technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "physical same-owner Borel extended clearance ledger and Abel identity",
                "root-atom versus collar-density type audit",
                "kernel-disintegrated D/A/g sufficient theorem",
                "minimal K/H/J positive policy ledger",
                "same-marginal long/short two-completion separator",
                "coupling-invariant positive-cost identity and zero-OT separator",
                "A_col coverage/moment independence",
            ],
            "reason_no_new_field_credit": (
                "the extended physical ledger is not finite, A_col coverage and the "
                "H/J operator join are absent, and signed cancellation cannot pay a "
                "positive F10 or strong cemetery charge"
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
        default=(HERE / "cm2_gate5_round58_owner_ledger_positive_transport_frontier_verifier.py"),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("PHYSICAL_LEDGER:", strict["physical_same_law_extended_clearance_ledger"])
    print("PHYSICAL_LEDGER_FINITE:", strict["physical_same_law_clearance_ledger_finite"])
    print("SIGNED_OT_POSITIVE_F10:", strict["signed_OT_implies_positive_F10"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
