#!/usr/bin/env python3
"""Round-56 Gate-5 optimal collar-recovery clock certificate.

Round 55 used the safe schedule ``r=k+1`` to contract the level-k collar
debt ``2^(k+1)m_k`` through the numerical C24 recurrence.  This append-only
leaf uses the exact frozen contraction factor instead.  The least number of
compatible blocks which makes the inherited term at most ``m_k`` is

    r_k = ceil(beta (k+1)),  beta = log(2)/log(1/gamma) < 1.

It is pointwise minimal, hence it is also the cheapest schedule for every
increasing emission weight.  For a geometric clearance tail the sharp
discounted-moment threshold drops from ``log_2(w_Z)`` to
``beta log_2(w_Z)``.  The improvement is strict but small; its first saved
block occurs at level 4381.

The theorem remains conditional on the physical weak clearance tail, the
Round54/Round42 same-operator join, and enough compatible suffix blocks.
Finite-horizon mass control does not control the unrecovered inverse-length
debt when the clearance exponent is at most one.  No Gate-5 field is
promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round56-optimal-collar-recovery-clock-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json": (
        "ff54ad55f1e065ccf390f83a83cc6135aa22f0cabc7753fd700b38e05af1701c"
    ),
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": (
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5"
    ),
}

BLOCK_DEPTH = 9148
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2

BETA_LOWER = Q(9997717578875635395, 10**19)
BETA_UPPER = Q(9997717578875635396, 10**19)
ALPHA_OLD_LOWER = Q(12409395510954121, 10**19)
ALPHA_OLD_UPPER = Q(12409395510954122, 10**19)
ALPHA_OPT_LOWER = Q(12406563164308641, 10**19)
ALPHA_OPT_UPPER = Q(12406563164308642, 10**19)
ALPHA_SEPARATOR = Q(12408, 10**7)


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


def fraction_digest(value: Q) -> str:
    numerator = value.numerator.to_bytes(
        (value.numerator.bit_length() + 7) // 8, "big"
    )
    denominator = value.denominator.to_bytes(
        (value.denominator.bit_length() + 7) // 8, "big"
    )
    return hashlib.sha256(
        len(numerator).to_bytes(8, "big") + numerator + denominator
    ).hexdigest()


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
        alpha_old = weight.ln() / Decimal(2).ln()
        alpha_opt = beta * alpha_old
        alpha_sep = Decimal(ALPHA_SEPARATOR.numerator) / Decimal(
            ALPHA_SEPARATOR.denominator
        )
        q_opt = (beta * weight.ln() - alpha_sep * Decimal(2).ln()).exp()
        q_old = (weight.ln() - alpha_sep * Decimal(2).ln()).exp()
        return {
            "gamma": +gamma,
            "rho": +rho,
            "weight": +weight,
            "beta": +beta,
            "alpha_old": +alpha_old,
            "alpha_opt": +alpha_opt,
            "q_opt_separator": +q_opt,
            "q_old_separator": +q_old,
        }


def optimal_clock(k: int, beta: Decimal | None = None) -> int:
    if k < 0:
        raise ValueError("negative collar level")
    if beta is None:
        beta = decimal_constants()["beta"]
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def recovered_level(H: int, beta: Decimal | None = None) -> int:
    if H < 0:
        raise ValueError("negative horizon")
    if beta is None:
        beta = decimal_constants()["beta"]
    return int((Decimal(H) / beta - Decimal(1)).to_integral_value(rounding=ROUND_FLOOR))


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


def validate_dependency() -> dict[str, dict[str, Any]]:
    loaded = load_dependencies()
    value = loaded[
        "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json"
    ]
    result = value["result"]
    delayed = result["dyadic_debt_layer_delayed_recovery"]
    constants = delayed["exact_constants"]
    if constants["gamma_formula"] != (
        "gamma=(2000/1999)*(1+48*9148)*(900337/901685)^9148"
    ):
        raise RuntimeError("Round55 gamma formula")
    if constants["gamma_bracket"] != "0.4999<gamma<1/2":
        raise RuntimeError("Round55 gamma bracket")
    if delayed["abstract_layer_typing"].find("z_(k,0)=2^(k+1)*m_k") < 0:
        raise RuntimeError("Round55 initial debt")
    if delayed["one_block_recurrence"] != (
        "z_(k,r+1)<=gamma*z_(k,r)+Z0*m_(k,r)"
    ):
        raise RuntimeError("Round55 recurrence")
    if delayed["weak_clearance_moment"] != (
        "M_col,w=sum_k w_Z^(k+1)*m_k<infinity"
    ):
        raise RuntimeError("Round55 safe schedule")
    for key in (
        "physical_weak_clearance_moment",
        "physical_k_plus_1_C24_suffix_schedule",
        "physical_Round54_to_Round42_same_operator_join",
        "quantitative_trace_contraction",
        "unconditional_trace_resolvent",
    ):
        if delayed[key] != "NOT_CERTIFIED":
            raise RuntimeError(f"Round55 frontier: {key}")
    if result["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round55 maturity")

    r54 = loaded[
        "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
    ]["result"]["recordwise_owner_collar_E_Tr"]
    if "finite Borel measure" not in r54["trace_law_typing"] or (
        "may be continuous" not in r54["trace_law_typing"]
    ):
        raise RuntimeError("Round54 trace-law typing")
    if "next OTHER singularity, homogeneity, owner or hole boundary" not in r54[
        "positive_clearance_predicate"
    ]:
        raise RuntimeError("Round54 d_other scope")
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 A_col frontier")
    if "finiteness is NOT_CERTIFIED" not in r54["standard_family_shape_debt"]:
        raise RuntimeError("Round54 collar-debt frontier")
    if not Q(4999, 10000) < GAMMA < Q(1, 2):
        raise RuntimeError("exact gamma arithmetic")
    if not Q(1) < W_Z < Q(2):
        raise RuntimeError("exact weight arithmetic")

    dec = decimal_constants()
    beta = dec["beta"]
    alpha_old = dec["alpha_old"]
    alpha_opt = dec["alpha_opt"]
    if not (
        Decimal(BETA_LOWER.numerator) / Decimal(BETA_LOWER.denominator)
        < beta
        < Decimal(BETA_UPPER.numerator) / Decimal(BETA_UPPER.denominator)
    ):
        raise RuntimeError("beta bracket")
    if not (
        Decimal(ALPHA_OLD_LOWER.numerator) / Decimal(ALPHA_OLD_LOWER.denominator)
        < alpha_old
        < Decimal(ALPHA_OLD_UPPER.numerator) / Decimal(ALPHA_OLD_UPPER.denominator)
    ):
        raise RuntimeError("old alpha bracket")
    if not (
        Decimal(ALPHA_OPT_LOWER.numerator) / Decimal(ALPHA_OPT_LOWER.denominator)
        < alpha_opt
        < Decimal(ALPHA_OPT_UPPER.numerator) / Decimal(ALPHA_OPT_UPPER.denominator)
    ):
        raise RuntimeError("optimal alpha bracket")
    if not Decimal(0) < alpha_opt < alpha_old:
        raise RuntimeError("strict threshold improvement")
    if not dec["q_opt_separator"] < Decimal(1) < dec["q_old_separator"]:
        raise RuntimeError("strict separator ratios")
    return loaded


def clock_rows() -> list[dict[str, Any]]:
    beta = decimal_constants()["beta"]
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4380, 4381, 4382, 8762, 10000):
        r = optimal_clock(k, beta)
        rows.append(
            {
                "level_k": k,
                "Round55_safe_blocks_k_plus_1": k + 1,
                "optimal_blocks_r_k": r,
                "saved_blocks": k + 1 - r,
                "minimality_test": (
                    "gamma^r_k*2^(k+1)<=1<gamma^(r_k-1)*2^(k+1)"
                ),
            }
        )
    return rows


def horizon_rows() -> list[dict[str, Any]]:
    beta = decimal_constants()["beta"]
    rows: list[dict[str, Any]] = []
    for horizon in (0, 1, 4380, 4381, 8761, 10000):
        k_max = recovered_level(horizon, beta)
        rows.append(
            {
                "available_blocks_H": horizon,
                "largest_recovered_level_K_H": k_max,
                "recovered_level_count": max(0, k_max + 1),
                "definition": "K_H=floor(H/beta-1)",
            }
        )
    return rows


def optimal_recovery_clock_audit() -> dict[str, Any]:
    dec = decimal_constants()
    rows = clock_rows()
    first_saved = int(
        (Decimal(1) / (Decimal(1) - dec["beta"])).to_integral_value(
            rounding=ROUND_CEILING
        )
        - 1
    )
    return {
        "frozen_layer_recurrence": (
            "z_(k,0)=2^(k+1)*m_k; z_(k,r+1)<=gamma*z_(k,r)+Z0*m_(k,r); "
            "m_(k,r)<=m_k"
        ),
        "exact_clock_definition": (
            "r_k=min{r>=0:gamma^r*2^(k+1)<=1}="
            "ceil(beta*(k+1)), beta=log(2)/log(1/gamma)"
        ),
        "beta_strict_window": "0<beta<1 because 0<gamma<1/2",
        "beta_rational_bracket": (
            "9997717578875635395/10^19 < beta < "
            "9997717578875635396/10^19"
        ),
        "beta_decimal_120_digit_audit": format(dec["beta"], "f"),
        "gamma_decimal_120_digit_audit": format(dec["gamma"], "f"),
        "gamma_fraction_binary_sha256": fraction_digest(GAMMA),
        "pointwise_minimality": (
            "r_k is the least integer clock making the inherited initial-debt "
            "term gamma^r*2^(k+1)*m_k at most m_k"
        ),
        "weighted_cost_minimality": (
            "for every w>1 and every schedule s_k with "
            "gamma^s_k*2^(k+1)<=1, one has s_k>=r_k and "
            "w^s_k*m_k>=w^r_k*m_k levelwise"
        ),
        "first_level_saving_a_block": first_saved,
        "first_saving_statement": (
            "r_k=k+1 for 0<=k<=4380, while r_4381=4381<4382"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_POINTWISE_MINIMAL_EXACT_GAMMA_RECOVERY_CLOCK",
    }


def sharp_weighted_moment_audit() -> dict[str, Any]:
    dec = decimal_constants()
    alpha_sep = Decimal(ALPHA_SEPARATOR.numerator) / Decimal(
        ALPHA_SEPARATOR.denominator
    )
    return {
        "iterated_recovery": (
            "z_(k,r_k)<=gamma^r_k*2^(k+1)*m_k+"
            "Z0*(1-gamma^r_k)/(1-gamma)*m_k<=C_rec*m_k, "
            "C_rec=1+Z0/(1-gamma)"
        ),
        "optimal_emission_ledger": (
            "sum_k w_Z^r_k*z_(k,r_k)<=C_rec*sum_k w_Z^r_k*m_k"
        ),
        "ceiling_comparison": (
            "w_Z^(beta*(k+1))<=w_Z^r_k<"
            "w_Z^(beta*(k+1)+1)"
        ),
        "geometric_tail_model": "m_k=C_m*2^(-alpha*k), k>=0",
        "sharp_geometric_criterion": (
            "sum_k w_Z^r_k*m_k<infinity iff "
            "w_Z^beta*2^(-alpha)<1 iff alpha>alpha_opt"
        ),
        "optimal_critical_exponent": (
            "alpha_opt=beta*log(w_Z)/log(2)"
        ),
        "Round55_safe_critical_exponent": "alpha_55=log(w_Z)/log(2)",
        "strict_improvement": (
            "0<alpha_opt=beta*alpha_55<alpha_55 because beta<1"
        ),
        "alpha_opt_rational_bracket": (
            "12406563164308641/10^19 < alpha_opt < "
            "12406563164308642/10^19"
        ),
        "alpha_55_rational_bracket": (
            "12409395510954121/10^19 < alpha_55 < "
            "12409395510954122/10^19"
        ),
        "alpha_opt_decimal_120_digit_audit": format(dec["alpha_opt"], "f"),
        "alpha_55_decimal_120_digit_audit": format(dec["alpha_old"], "f"),
        "strict_separator": {
            "alpha": str(ALPHA_SEPARATOR),
            "ordering": "alpha_opt<alpha=0.0012408<alpha_55",
            "optimal_ratio_w_beta_2_minus_alpha": format(
                dec["q_opt_separator"], "f"
            ),
            "Round55_ratio_w_2_minus_alpha": format(
                dec["q_old_separator"], "f"
            ),
            "conclusion": (
                "the optimal clock ledger converges while the Round55 k+1 "
                "geometric ledger diverges"
            ),
        },
        "critical_equality_separator": (
            "at alpha=alpha_opt the lower ceiling comparison has nondecaying "
            "terms, so the optimal weighted ledger diverges"
        ),
        "raw_debt_phase_boundary": (
            "for the same geometric model, sum_k 2^(k+1)*m_k<infinity "
            "iff alpha>1"
        ),
        "strict_delayed_only_region": (
            "alpha_opt<alpha<=1 gives infinite raw collar debt but finite "
            "optimal delayed emission moment"
        ),
        "status": "CERTIFIED_SHARP_OPTIMAL_CLOCK_GEOMETRIC_MOMENT_THRESHOLD",
    }


def finite_horizon_audit() -> dict[str, Any]:
    rows = horizon_rows()
    return {
        "recovered_prefix": (
            "after H compatible blocks, precisely the levels with r_k<=H are "
            "recovered; their largest index is K_H=floor(H/beta-1)"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "conditional_mass_remainder": (
            "if m_k<=C_m*2^(-alpha*k), alpha>0, then "
            "sum_(k>K_H)m_k<=C_m*2^(-alpha*(K_H+1))/"
            "(1-2^(-alpha))"
        ),
        "mass_remainder_rate": (
            "the unrecovered mass is O(2^(-alpha*H/beta))"
        ),
        "debt_remainder_for_alpha_gt_1": (
            "if alpha>1, sum_(k>K_H)2^(k+1)m_k<="
            "2*C_m*2^(-(alpha-1)*(K_H+1))/(1-2^(1-alpha))"
        ),
        "finite_horizon_obstruction_for_alpha_le_1": (
            "for m_k=C_m*2^(-alpha*k) with 0<alpha<=1, every finite-H "
            "unrecovered inverse-length debt sum_(k>K_H)2^(k+1)m_k is infinite"
        ),
        "logical_boundary": (
            "a decaying unrecovered mass tail cannot be renamed an unrecovered "
            "standard-family Z/debt tail"
        ),
        "physical_unbounded_suffix_horizon": "NOT_CERTIFIED",
        "physical_short_horizon_debt_ledger_in_weak_regime": "NOT_CERTIFIED",
        "status": (
            "CERTIFIED_CONDITIONAL_PREFIX_AND_MASS_REMAINDER_"
            "WITH_SHARP_FINITE_HORIZON_DEBT_OBSTRUCTION"
        ),
    }


def shell_neighbourhood_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (2, 4, 8, 16, 64):
        epsilon = Q(1, n**3)
        finite_boundary_cover = 2 * n * epsilon
        accumulating_tail_cover = Q(1, n**2) + epsilon
        displayed_upper = finite_boundary_cover + accumulating_tail_cover
        rows.append(
            {
                "split_index_n": n,
                "epsilon": qstr(epsilon),
                "finite_boundary_cover_2n_epsilon": qstr(finite_boundary_cover),
                "accumulating_tail_cover_n_minus_2_plus_epsilon": qstr(
                    accumulating_tail_cover
                ),
                "total_displayed_upper": qstr(displayed_upper),
                "four_epsilon_two_thirds_upper": qstr(Q(4, n**2)),
            }
        )
    return rows


def inverse_square_shell_clearance_audit() -> dict[str, Any]:
    rows = shell_neighbourhood_rows()
    return {
        "abstract_shell_model": (
            "one collar coordinate c in [0,1] with boundary points "
            "x_k=k^(-2), k>=1, accumulating only at x_infinity=0"
        ),
        "gap_scale": (
            "Delta_k=x_k-x_(k+1)=(2k+1)/(k^2*(k+1)^2)=Theta(k^-3)"
        ),
        "epsilon_neighbourhood_split": (
            "with N=ceil(epsilon^(-1/3)), cover the first N boundary "
            "neighbourhoods by length 2*N*epsilon and the accumulating tail "
            "by [0,N^(-2)+epsilon]"
        ),
        "Lebesgue_tail_bound": (
            "Leb{dist(c,{0,x_1,x_2,...})<epsilon}<=6*epsilon^(2/3), "
            "0<epsilon<=1"
        ),
        "bounded_density_consequence": (
            "if the exact same owner trace law has density at most D in this "
            "collar coordinate, then nu{0<d<epsilon}<=6*D*epsilon^(2/3)"
        ),
        "finite_extra_boundaries": (
            "J additional boundary points add at most 2*J*D*epsilon, hence "
            "the exponent 2/3 survives with constant D*(6+2J)"
        ),
        "clearance_exponent_comparison": (
            "2/3>alpha_55>alpha_opt, so this same-law bound would close both "
            "the Round55 and optimal-clock weak clearance moments"
        ),
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "physical_binding_audit": {
            "Round54_trace_law": (
                "an arbitrary finite Borel owner/root law which may be continuous; "
                "no density relative to the collar coordinate is frozen"
            ),
            "Round54_clearance_scope": (
                "d_other includes every other singularity, homogeneity, owner and "
                "hole boundary in the fixed word, not only the model shell points"
            ),
            "missing_same_law_density": "NOT_CERTIFIED",
            "missing_uniform_pullback_gap_comparison": "NOT_CERTIFIED",
            "missing_uniform_extra_boundary_count_over_owner_records": (
                "NOT_CERTIFIED"
            ),
            "A_col_positive_or_full_mass": "NOT_CERTIFIED",
            "conclusion": (
                "the 2/3 shell estimate is a valid conditional route but cannot be "
                "bound to the current physical owner law or promoted"
            ),
        },
        "status": (
            "CERTIFIED_ABSTRACT_INVERSE_SQUARE_SHELL_TWO_THIRDS_TAIL_"
            "PHYSICAL_BINDING_NOT_CERTIFIED"
        ),
    }


def build_result() -> dict[str, Any]:
    validate_dependency()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": (
                "the clock theorem is an abstract layerwise consequence of the "
                "frozen Round55/Round42 recurrence for fixed |s|<=1/400; no "
                "moving-map sequence or physical trace tail is asserted"
            ),
            "claim_type": (
                "pointwise minimal exact-gamma collar recovery clock, sharp "
                "geometric weak-moment threshold, and finite-horizon "
                "mass-versus-debt frontier"
            ),
        },
        "optimal_exact_gamma_recovery_clock": optimal_recovery_clock_audit(),
        "sharp_optimal_clock_weighted_moment": sharp_weighted_moment_audit(),
        "finite_horizon_prefix_remainder_frontier": finite_horizon_audit(),
        "inverse_square_shell_clearance_route_audit": (
            inverse_square_shell_clearance_audit()
        ),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "pointwise minimal exact-gamma collar recovery clock",
                "strictly improved sharp clearance exponent alpha_opt",
                "finite-horizon recovered-prefix and mass-tail formula",
                "finite-horizon debt obstruction for alpha<=1",
                "abstract inverse-square shell epsilon^(2/3) clearance lemma",
            ],
            "reason_no_new_field_credit": (
                "the physical weak clearance law, Round54/Round42 same-operator "
                "join, unbounded compatible suffix schedule, and post-recovery "
                "fixed operator block remain absent"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "Round55_k_plus_1_schedule_remains_valid": "CERTIFIED",
            "optimal_exact_gamma_recovery_clock": "CERTIFIED_CONDITIONAL",
            "optimal_clock_pointwise_minimality": "CERTIFIED",
            "strictly_improved_weak_clearance_threshold": "CERTIFIED",
            "optimal_geometric_threshold_sharpness": "CERTIFIED",
            "finite_horizon_mass_remainder": "CERTIFIED_CONDITIONAL",
            "finite_horizon_debt_control_for_alpha_le_1": (
                "FALSE_BY_CERTIFIED_GEOMETRIC_SEPARATOR"
            ),
            "abstract_inverse_square_shell_clearance_tail": (
                "CERTIFIED_CONDITIONAL"
            ),
            "physical_same_law_bounded_trace_density": "NOT_CERTIFIED",
            "physical_uniform_full_word_boundary_complexity": "NOT_CERTIFIED",
            "physical_weak_clearance_moment": "NOT_CERTIFIED",
            "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
            "physical_unbounded_compatible_suffix_schedule": "NOT_CERTIFIED",
            "physical_short_horizon_debt_ledger": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "unconditional_trace_resolvent": "NOT_CERTIFIED",
            "physical_same_source_pair_rate": "NOT_CERTIFIED",
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
        },
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
        default=(
            HERE
            / "cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("OPTIMAL_CLOCK:", strict["optimal_exact_gamma_recovery_clock"])
    print(
        "IMPROVED_THRESHOLD:",
        strict["strictly_improved_weak_clearance_threshold"],
    )
    print(
        "PHYSICAL_SUFFIX_SCHEDULE:",
        strict["physical_unbounded_compatible_suffix_schedule"],
    )
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
