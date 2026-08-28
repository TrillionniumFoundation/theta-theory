#!/usr/bin/env python3
"""Round-55 Gate-5 synchronised-pairing and delayed-collar certificate.

This append-only leaf supplements the normalized-product coupling used as a
canonical witness in Round 54.  The physical hit/miss current also has a
source-synchronised coupling obtained by integrating the two kernels over the
same Jordan source point.  It has the required marginals without measurable
selection.  Neither coupling cost dominates the other in general; taking the
minimum of the two valid bounds is never worse than the Round-54 witness and
is sometimes strictly better.

The leaf also installs a sharp analytic separator: a single transverse
analytic crossing can give full collar-admissible trace mass while the
Round-54 inverse-collar debt is infinite.  Finally it proves an abstract
dyadic debt-layer recovery theorem.  A level-k collar becomes uniformly
proper after k+1 compatible numerical C24 Growth blocks, and the discounted
emission ledger only needs a weak clearance moment with exact threshold
alpha > log_2(w_Z).  The required physical suffix schedule, weak moment and
same-source image rate are not certified, so no Gate-5 field is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round55-synchronised-pairing-delayed-collar.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": (
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
}

SURVIVAL_R = Q(111718729, 111718750)
BLOCK_DEPTH = 9148
RHO = SURVIVAL_R**BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
ALPHA_LOWER = Q(12409395510954121, 10**19)
ALPHA_UPPER = Q(12409395510954122, 10**19)


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def decimal_constants() -> tuple[Decimal, Decimal, Decimal]:
    with localcontext() as context:
        context.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        weight = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        alpha = weight.ln() / Decimal(2).ln()
        return +rho, +weight, +alpha


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> dict[str, dict[str, Any]]:
    loaded = {name: load(name) for name in DEPENDENCIES}

    r54 = loaded[
        "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
    ]["result"]
    collar54 = r54["recordwise_owner_collar_E_Tr"]
    if "ell(omega)=2^(-(k(omega)+1))<d(omega)" not in collar54[
        "canonical_Borel_selection"
    ]:
        raise RuntimeError("Round54 dyadic collar selection")
    if collar54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 A_col frontier")
    if "finiteness is NOT_CERTIFIED" not in collar54[
        "standard_family_shape_debt"
    ]:
        raise RuntimeError("Round54 collar debt frontier")
    pair54 = r54["signed_hit_miss_pairing_resolvent"]
    if "(mu_p^+ tensor mu_p^-)/m_p" not in pair54["coupling_kernel"]:
        raise RuntimeError("Round54 product coupling witness")
    if pair54["physical_pair_separation_rate"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 pair-rate frontier")
    if r54["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round54 Gate5 maturity")

    r42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    growth = r42["numerical_C24_killed_Growth"]
    if growth["block_depth_n_star"] != BLOCK_DEPTH:
        raise RuntimeError("Round42 block depth")
    if growth["block_bound"] != "Z(O_s^9148 G)<=gamma*Z(G)+Z0*mass(G)":
        raise RuntimeError("Round42 Growth recurrence")
    if growth["gamma_strict_bracket"] != "0.4999<gamma<1/2":
        raise RuntimeError("Round42 gamma bracket")
    if growth["hereditary_under_positive_C24_killing"] is not True:
        raise RuntimeError("Round42 hereditary killing")
    aggregate = r42["aggregate_canonical_Z_resolvent"]
    if aggregate["mass_factor_rho"] != "(111718729/111718750)^9148":
        raise RuntimeError("Round42 rho")
    if aggregate["explicit_block_index_weight"] != "w_Z=(1+rho^(-1))/2":
        raise RuntimeError("Round42 weight")

    if not Q(4999, 10000) < GAMMA < Q(1, 2):
        raise RuntimeError("exact gamma arithmetic")
    if not Q(1) < W_Z < Q(2):
        raise RuntimeError("exact weak-moment weight window")
    _, _, alpha = decimal_constants()
    lower = Decimal(ALPHA_LOWER.numerator) / Decimal(ALPHA_LOWER.denominator)
    upper = Decimal(ALPHA_UPPER.numerator) / Decimal(ALPHA_UPPER.denominator)
    if not lower < alpha < upper:
        raise RuntimeError("critical exponent bracket")
    return loaded


def synchronised_pairing_audit() -> dict[str, Any]:
    separator_rows = [
        {
            "source_atom": "0",
            "source_mass": "1/2",
            "H_image": "0",
            "M_image": "0",
            "synchronised_cost": "0",
        },
        {
            "source_atom": "1",
            "source_mass": "1/2",
            "H_image": "1",
            "M_image": "1",
            "synchronised_cost": "0",
        },
    ]
    return {
        "scope": (
            "one immutable physical source record/rank p at a time, with the actual "
            "Jordan source law lambda_p=lambda_p^+-lambda_p^- and the same Round44 "
            "Borel hit/miss Markov kernels H_p,M_p"
        ),
        "positive_marginals": (
            "mu_p^+=H_p*lambda_p^+ + M_p*lambda_p^- and "
            "mu_p^-=M_p*lambda_p^+ + H_p*lambda_p^-"
        ),
        "synchronised_coupling": (
            "pi_p^sync=integral (H_p(x) tensor M_p(x)) d lambda_p^+(x) + "
            "integral (M_p(x) tensor H_p(x)) d lambda_p^-(x)"
        ),
        "first_marginal": "(pr_1)_*pi_p^sync=mu_p^+",
        "second_marginal": "(pr_2)_*pi_p^sync=mu_p^-",
        "total_mass": "mass(pi_p^sync)=abs(lambda_p)(source)=m_p",
        "Borel_typing": (
            "products and parameter integrals of the two fixed standard-Borel Markov "
            "kernels are Borel; no measurable selection or cross-source pairing occurs"
        ),
        "BL_cost": (
            "d_p^sync=integral min(2,d(y_H,y_M)) d pi_p^sync(y_H,y_M)"
        ),
        "BL_bound": "norm(J_p)_(BL*)<=d_p^sync",
        "Round54_product_cost": (
            "d_p^product=integral min(2,d(y+,y-)) d pi_p^product(y+,y-)"
        ),
        "best_available_cost": "d_p^best=min(d_p^product,d_p^sync)",
        "combined_BL_bound": "norm(J_p)_(BL*)<=d_p^best",
        "comparison_scope": (
            "the synchronised and normalized-product costs are not totally ordered; "
            "only their minimum is certified never worse than either chosen witness"
        ),
        "deterministic_reduction": (
            "if H_p(x)=delta_(h_p(x)) and M_p(x)=delta_(m_p(x)), then "
            "d_p^sync=integral min(2,d(h_p(x),m_p(x))) d abs(lambda_p)(x)"
        ),
        "same_source_rate_sufficient_condition": (
            "d_p^sync<=C_sync*delta_sync^p with w_Z*delta_sync<1 implies "
            "sum_p w_Z^p norm(J_p)_(BL*)<=C_sync/(1-w_Z*delta_sync)"
        ),
        "product_coupling_nonsharp_separator": {
            "model": (
                "source {0,1} has positive law lambda=(delta_0+delta_1)/2, "
                "target metric d(0,1)=1, and deterministic H=M=identity"
            ),
            "rows": separator_rows,
            "rows_sha256": digest(separator_rows),
            "current": "J=(H-M)lambda=0",
            "synchronised_cost": "0",
            "Round54_normalized_product_cost": "1/2",
            "conclusion": (
                "the Round54 normalized-product witness is valid but can stay positive "
                "when the current vanishes; synchronisation is strictly better in this model"
            ),
        },
        "synchronised_coupling_nonsharp_separator": {
            "model": (
                "source {0,1} has positive law lambda=(delta_0+delta_1)/2, "
                "target metric d(0,1)=1, deterministic H=identity and "
                "M=flip with M(0)=1,M(1)=0"
            ),
            "current": "J=(H-M)lambda=0",
            "synchronised_cost": "1",
            "Round54_normalized_product_cost": "1/2",
            "conclusion": (
                "synchronisation can be worse than the normalized product; no global "
                "ordering is asserted, while d_p^best remains equal to 1/2"
            ),
        },
        "no_automatic_rate_separator": {
            "model": (
                "for every p use one source atom of mass one with deterministic "
                "h_p(x)=0 and m_p(x)=1 in the fixed two-point metric"
            ),
            "current": "J_p=delta_0-delta_1",
            "exact_BL_norm": "1",
            "synchronised_cost": "1",
            "conclusion": (
                "equal positive mass and constant-test cancellation alone imply no "
                "delta_sync<1 image-separation rate"
            ),
        },
        "physical_same_source_pair_rate": "NOT_CERTIFIED",
        "positive_face_or_cemetery_consequence": "NOT_CERTIFIED",
        "status": (
            "CERTIFIED_ALTERNATIVE_SAME_SOURCE_WITNESS_SOMETIMES_STRICTLY_BETTER"
        ),
    }


def analytic_transverse_collar_separator() -> dict[str, Any]:
    rows = []
    for k in range(1, 9):
        mass = Q(1, 2**k)
        ell = Q(1, 2 ** (k + 1))
        rows.append(
            {
                "dyadic_level_k": k,
                "level_trace_mass_m_k": qstr(mass),
                "collar_length_ell_k": qstr(ell),
                "inverse_collar_debt_m_k_over_ell_k": qstr(mass / ell),
                "partial_debt_through_level_k": str(2 * k),
            }
        )
    return {
        "model": (
            "owner/root parameter t in (-1,1) with probability nu=dt/2; the selected "
            "anchor face is b_0(t)=0 and one other analytic boundary is b_1(t)=t, "
            "so the two boundaries have one transverse crossing at t=0 and "
            "d(t)=abs(t) away from it"
        ),
        "no_grazing_accumulation": (
            "there is exactly one analytic transverse zero of the clearance and no "
            "countable homogeneity-shell accumulation in this separator"
        ),
        "collar_admissible_set": "A_col=(-1,1)\\{0}",
        "A_col_trace_mass": "nu(A_col)=1",
        "zero_clearance_trace_mass": "nu({d=0})=0",
        "dyadic_level": (
            "C_k={t:2^(-k)<=abs(t)<2^(-(k-1))}, k>=1; the Round54 selector "
            "has ell(t)=2^(-(k+1)) on C_k"
        ),
        "level_mass": "m_k=nu(C_k)=2^(-k)",
        "level_debt": "m_k/ell_k=2 for every k>=1",
        "rows": rows,
        "rows_sha256": digest(rows),
        "collar_debt": "Z_col=sum_(k>=1) 2=infinity",
        "equivalent_integral_bound": (
            "for 0<abs(t)<1, abs(t)/4<ell(t)<=abs(t)/2 and hence "
            "2/abs(t)<=ell(t)^(-1)<4/abs(t)"
        ),
        "finite_parent_debt": (
            "if every parent curve has length one and owner rank B=14, then "
            "Z_parent=1 and Z_parent,B=2^14=16384"
        ),
        "logical_conclusion": (
            "even full A_col trace mass, a null zero-clearance set and analytic "
            "transversality do not imply finite Z_col or a uniformly proper trace bridge"
        ),
        "status": "CERTIFIED_FULL_MASS_ANALYTIC_TRANSVERSE_INFINITE_COLLAR_DEBT_SEPARATOR",
    }


def delayed_collar_recovery_audit() -> dict[str, Any]:
    rho_dec, weight_dec, alpha_dec = decimal_constants()
    sample_levels = []
    for k in (0, 1, 2, 4, 8, 16):
        sample_levels.append(
            {
                "level_k": k,
                "initial_debt": "z_(k,0)=2^(k+1)*m_k",
                "scheduled_C24_blocks": k + 1,
                "contracted_initial_term": "(2*gamma)^(k+1)*m_k<m_k",
            }
        )
    return {
        "abstract_layer_typing": (
            "C_k={omega:k(omega)=k}, nu_k=nu restricted to C_k, m_k=mass(nu_k), "
            "and the Round54 constant-density collar extension has "
            "z_(k,0)=2^(k+1)*m_k"
        ),
        "required_same_operator_hypothesis": (
            "the actual labelled Round54 killed-word collar output on C_k is an input "
            "to the exact Round42 positive killed C24 operator O_s^9148, with the "
            "same owner IDs and no relabelling or unregistered boundary cut"
        ),
        "required_suffix_horizon": (
            "level k retains at least k+1 consecutive compatible 9148-collision C24 "
            "blocks after its insertion; mass is nonincreasing, m_(k,r)<=m_k"
        ),
        "one_block_recurrence": "z_(k,r+1)<=gamma*z_(k,r)+Z0*m_(k,r)",
        "exact_constants": {
            "gamma_formula": (
                "gamma=(2000/1999)*(1+48*9148)*(900337/901685)^9148"
            ),
            "gamma_bracket": "0.4999<gamma<1/2",
            "gamma_fraction_binary_sha256": fraction_digest(GAMMA),
            "Z0": "Z0=2/delta_open=54/(5*delta_9148)",
        },
        "iteration_at_delay_k_plus_1": (
            "z_(k,k+1)<=gamma^(k+1)*2^(k+1)*m_k + "
            "Z0*(1-gamma^(k+1))/(1-gamma)*m_k"
        ),
        "uniform_recovered_bound": (
            "z_(k,k+1)<C_rec*m_k, where C_rec=1+Z0/(1-gamma), because 2*gamma<1"
        ),
        "sample_levels": sample_levels,
        "sample_levels_sha256": digest(sample_levels),
        "discounted_emission_ledger": (
            "sum_k w_Z^(k+1)*z_(k,k+1) < "
            "C_rec*sum_k w_Z^(k+1)*m_k"
        ),
        "weak_clearance_moment": "M_col,w=sum_k w_Z^(k+1)*m_k<infinity",
        "strictly_weaker_than_Z_col": (
            "for the analytic transverse separator m_k=2^(-k), k>=1, "
            "Z_col=infinity but M_col,w=w_Z^2/(2-w_Z)<infinity"
        ),
        "clearance_tail_sufficient_condition": (
            "if nu({0<d<t})<=C_d*t^alpha for 0<t<=1 and total mass is M, then "
            "M_col,w<=w_Z*M+C_d*w_Z^2/(1-w_Z*2^(-alpha)) whenever "
            "w_Z*2^(-alpha)<1"
        ),
        "exact_critical_exponent": "alpha_*=log(w_Z)/log(2)",
        "critical_iff_for_geometric_dyadic_tail": (
            "sum_k w_Z^(k+1)*2^(-alpha*k)<infinity iff alpha>alpha_*"
        ),
        "critical_rational_bracket": (
            "12409395510954121/10^19 < alpha_* < "
            "12409395510954122/10^19"
        ),
        "critical_decimal_100_digit_audit": format(alpha_dec, "f"),
        "rho_decimal_100_digit_audit": format(rho_dec, "f"),
        "weight_decimal_100_digit_audit": format(weight_dec, "f"),
        "rho_fraction_binary_sha256": fraction_digest(RHO),
        "weight_fraction_binary_sha256": fraction_digest(W_Z),
        "physical_weak_clearance_moment": "NOT_CERTIFIED",
        "physical_k_plus_1_C24_suffix_schedule": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "short_horizon_remainder_ledger": "NOT_CERTIFIED",
        "quantitative_trace_contraction": "NOT_CERTIFIED",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "status": (
            "CERTIFIED_CONDITIONAL_DYADIC_DELAYED_RECOVERY_THEOREM_"
            "WITH_EXACT_WEAK_MOMENT_THRESHOLD"
        ),
    }


def arens_eells_trace_technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-20",
        "bibliographic_pointer_only": True,
        "source": {
            "arxiv": "2503.09536v2",
            "title": "On the normal trace space of extended divergence-measure fields",
            "author": "Christopher Irving",
            "version_date": "2026-05-29",
            "url": "https://arxiv.org/abs/2503.09536v2",
        },
        "relevant_typed_result": (
            "the normal trace of an extended divergence-measure field lies in the "
            "Arens-Eells space AE(partial E), the predual of bounded Lipschitz "
            "functions; on locally uniformly quasiconvex domains, including Lipschitz "
            "domains, the trace map is onto and has a bounded not-necessarily-linear "
            "right inverse, with an analogous DM^1 statement"
        ),
        "possible_use": (
            "AE(partial E) is a natural fixed signed BL trace target for the Round54 "
            "directional-BV and synchronised-pairing sublayers"
        ),
        "why_no_promotion": (
            "the result supplies neither positivity nor a linear Markov extension, "
            "same-ID killed-word intertwining, numeric billiard constants, membership "
            "of every physical source in the divergence-measure class, nor a rho-rate"
        ),
        "external_source_vendored_or_used_as_dependency": False,
        "Gate5_field_credit": "NONE",
        "status": "RELEVANT_SIGNED_TRACE_TECHNOLOGY_AUDITED_WITHOUT_IMPORT",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": (
                "the abstract coupling is recordwise; the delayed C24 theorem has the "
                "Round42 fixed |s|<=1/400 scope; no moving-sequence theorem is asserted"
            ),
            "claim_type": (
                "alternative synchronised signed pairing with a never-worse minimum "
                "bound, sharp full-mass collar separator, and conditional dyadic "
                "delayed-recovery interface"
            ),
        },
        "synchronised_hit_miss_pairing": synchronised_pairing_audit(),
        "analytic_transverse_full_mass_collar_separator": (
            analytic_transverse_collar_separator()
        ),
        "dyadic_debt_layer_delayed_recovery": delayed_collar_recovery_audit(),
        "Arens_Eells_normal_trace_technology_audit": (
            arens_eells_trace_technology_audit()
        ),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "source-synchronised hit/miss BL coupling with exact marginals",
                "full-mass analytic-transverse infinite-collar-debt separator",
                "conditional dyadic k+1-block recovery theorem",
                "exact weak-clearance critical exponent alpha_*=log_2(w_Z)",
            ],
            "reason_no_new_field_credit": (
                "the physical same-source rate, weak clearance moment, same-operator "
                "Round54/Round42 join and unbounded suffix horizon are all missing"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "Round54_product_pairing_bound_remains_valid": "CERTIFIED",
            "synchronised_same_source_pairing_bound": (
                "CERTIFIED_ALTERNATIVE_SAME_SOURCE_WITNESS_SOMETIMES_STRICTLY_BETTER"
            ),
            "combined_minimum_pairing_bound": (
                "CERTIFIED_NEVER_WORSE_THAN_ROUND54_PRODUCT"
            ),
            "physical_same_source_pair_rate": "NOT_CERTIFIED",
            "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
            "positive_F10_or_cemetery_from_signed_pairing": "NOT_CERTIFIED",
            "full_A_col_mass_implies_finite_Z_col": "FALSE_BY_CERTIFIED_COUNTEREXAMPLE",
            "analytic_transverse_full_mass_infinite_Z_col_separator": "CERTIFIED",
            "dyadic_delayed_recovery_abstract_theorem": "CERTIFIED_CONDITIONAL",
            "weak_clearance_moment_exact_threshold": "CERTIFIED",
            "physical_weak_clearance_moment": "NOT_CERTIFIED",
            "physical_k_plus_1_C24_suffix_schedule": "NOT_CERTIFIED",
            "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "unconditional_trace_resolvent": "NOT_CERTIFIED",
            "Arens_Eells_normal_trace_physical_import": "NOT_CERTIFIED",
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
        json.dumps(
            build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False
        )
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
            / "cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("SYNC_PAIRING:", strict["synchronised_same_source_pairing_bound"])
    print(
        "FULL_MASS_FINITE_Z_COL:",
        strict["full_A_col_mass_implies_finite_Z_col"],
    )
    print(
        "DELAYED_RECOVERY:",
        strict["dyadic_delayed_recovery_abstract_theorem"],
    )
    print("PHYSICAL_TRACE_CONTRACTION:", strict["quantitative_trace_survivor_contraction"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
