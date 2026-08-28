#!/usr/bin/env python3
"""Round-61 Gate-5 complement-RN / Borel-code / Orlicz frontier.

This append-only leaf makes three typed advances and no global Gate-5 claim:

* it instantiates the Round-54 owner/root law from the actual fixed-insertion
  Round-52 owner-selected positive law and constructs the forward/reverse
  F10 cost-weighted pushforwards.  Their Radon--Nikodym densities give
  same-law L1 complement anchors at one fixed insertion time only;
* it places the actual collar input, word/C24 kernels and labelled outputs in
  standard-Borel code spaces with countable separating generators.  Thus all
  seven suffix predicates and the initial-run capacity R are Borel, although
  only L_id and L_word are universally true on the frozen records;
* on the same owner law it identifies raw collar Z with an explicit
  power-Orlicz moment of the optimal clock, up to one fixed multiplicative
  constant.  Neither side is proved finite.

No coverage, active-Abel bound, all-time positive sum, Jordan identification,
strong cemetery, complete field, Gate, or CM2 conclusion is promoted.
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
RESULT_SCHEMA = "cm2.gate5.round61-complement-rn-borel-orlicz-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json"

DEPENDENCIES = {
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json": "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json": "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
}

ROUND60_AGGREGATE_PINS = {
    "cm2-sixtieth-direct-assault-2026-07-20.md": "ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212",
    "cm2-sixtieth-direct-assault-manifest-2026-07-20.sha256": "5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.sha256": "ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483",
}

BLOCK_DEPTH = 9148
COAREA_MASS = Q(8064, 5)
FORWARD_F10 = Q(395304765824751, 220000)
REVERSE_F10 = Q(162772550633721, 176000)
BIDIRECTIONAL_F10 = Q(2395081816467609, 880000)
RANK_MOMENT = Q(23253221519103, 880000)


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


def constants() -> dict[str, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 140
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK_DEPTH) * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * w.ln() / Decimal(2).ln()
        q_col = Decimal(1) / alpha
        return {"gamma": +gamma, "rho": +rho, "w": +w, "beta": +beta, "alpha": +alpha, "q_col": +q_col}


def clock(k: int, beta: Decimal | None = None) -> int:
    if k < 0:
        raise ValueError("negative level")
    beta = constants()["beta"] if beta is None else beta
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def _safe_dependency(name: str, expected: str) -> Path:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != expected:
        raise RuntimeError(f"dependency hash: {name}")
    return path


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = _safe_dependency(name, expected)
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object, parse_constant=reject_json_constant)
        if not isinstance(value, dict):
            raise RuntimeError(f"dependency root: {name}")
        loaded[name] = value
    for name, expected in ROUND60_AGGREGATE_PINS.items():
        _safe_dependency(name, expected)
    return loaded


def validate_dependencies() -> dict[str, dict[str, Any]]:
    d = load_dependencies()
    r39_result = d["cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"]["result"]
    r39 = r39_result["moving_occurrence_seed_F10_L3over2_installation"]
    if r39_result["physical_rank_L3over2_derivation"]["positive_coarea_total_mass_upper"] != str(COAREA_MASS) or r39["same_occurrence_ID_seed_count"] != 64:
        raise RuntimeError("Round39 positive coarea law")
    r50 = d["cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if r50["index_space_is_standard_Borel"] is not True or r50["owner_sets_pairwise_disjoint"] is not True:
        raise RuntimeError("Round50 owner registry")
    r52 = d["cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["sums_over_insertion_times"] is not False or r52["source_measure"] != "global positive raw occurrence coarea law m_occ over all 64 seeds":
        raise RuntimeError("Round52 scope")
    if r52["transferred_forward_F10_L1_strict_upper"] != str(FORWARD_F10) or r52["transferred_reverse_F10_L1_strict_upper"] != str(REVERSE_F10) or r52["transferred_bidirectional_F10_L1_strict_upper"] != str(BIDIRECTIONAL_F10):
        raise RuntimeError("Round52 F10 constants")
    r54 = d["cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"]["result"]["recordwise_owner_collar_E_Tr"]
    if r54["collar_admissible_stagewise_mass_E_Tr_schema_installed"] is not True or "Borel probability kernel" not in r54["Borel_kernel_proof"]:
        raise RuntimeError("Round54 Borel collar")
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 coverage frontier")
    r56 = d["cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"]["result"]["optimal_exact_gamma_recovery_clock"]
    if "ceil(beta*(k+1))" not in r56["exact_clock_definition"]:
        raise RuntimeError("Round56 optimal clock")
    r59 = d["cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json"]["result"]["strict_nonpromotion"]
    if r59["Gate5_maturity"] != "10/18" or r59["unified_coverage_clock_Abel_criterion"] != "CERTIFIED_EXACT_IFF":
        raise RuntimeError("Round59 baseline")
    r60 = d["cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"]["result"]
    if r60["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round60 baseline")
    if r60["seven_bit_suffix_Borel_materialisation"]["unconditional_Borel_predicate_count"] != 4:
        raise RuntimeError("Round60 suffix frontier")
    if FORWARD_F10 + REVERSE_F10 != BIDIRECTIONAL_F10:
        raise RuntimeError("F10 arithmetic")
    return d


def owner_complement_rn_anchor() -> dict[str, Any]:
    strata = [
        {"stratum": "N_cut/source_core_clipping", "regularity": "finite_regular_owner_record", "fixed_j_anchor": "orientation-positive RN restriction"},
        {"stratum": "N_cut/intermediate_C24_preimage", "regularity": "finite_regular_owner_record", "fixed_j_anchor": "orientation-positive RN restriction"},
        {"stratum": "N_cut/terminal_C24_preimage", "regularity": "finite_regular_owner_record", "fixed_j_anchor": "orientation-positive RN restriction"},
        {"stratum": "N_cut/collision_or_owner_change", "regularity": "finite_regular_owner_record", "fixed_j_anchor": "orientation-positive RN restriction"},
        {"stratum": "N_acc/moving_or_grazing_accumulation", "regularity": "trace value/nullity unknown", "fixed_j_anchor": "orientation-positive RN restriction wherever the Round52 regular owner law is defined"},
    ]
    return {
        "fixed_insertion_scope": "fix j; take the disjoint marked source law m_j^own=sum_a 1_(E_(j,a)^owner intersect R_(j,a)^reg)*m_occ from Round52, with no sum over j",
        "actual_owner_law_construction": "first refine m_j^own by the countable Round54 word-cell, then apply the Borel root/collar map q_j retaining the full t54 token; define nu_j=(q_j)_#m_j^own",
        "same_law_guard": "nu_j is the same actual pushforward instance of the Round54 finite Borel owner/root law; no arbitrary owner law and no collision-area law is substituted",
        "token_guard": "q_j retains restriction/time/event/primitive/rank/side/word-cell and endpoint/root coordinates; the Round50 projection forgets only word-cell and never merges two retained t54 fibres",
        "bad_set_partition": "A_col^c=N_cut disjoint_union N_acc, where N_cut is the countable union of exact other-cut coincidences and N_acc has every registered positive gap but infimum gap zero",
        "actual_bad_submeasure": "nu_j^bad=1_(A_col^c)*nu_j is a same-owner-law finite Borel submeasure",
        "mass_anchor": "C_bad,j^mass=1 on A_col^c belongs to L1(nu_j^bad), with integral at most nu_j(total)<=m_occ(total)<8064/5",
        "weighted_pushforwards": {
            "forward": "xi_j^f(A)=integral_(q_j^-1 A)c_f dm_j^own",
            "reverse": "xi_j^r(A)=integral_(q_j^-1 A)c_r dm_j^own",
            "bidirectional": "xi_j^bi=xi_j^f+xi_j^r",
        },
        "absolute_continuity": "xi_j^f,xi_j^r,xi_j^bi are finite positive Borel measures and are absolutely continuous with respect to nu_j",
        "RN_costs": "choose Borel versions C_bad,j^f=d xi_j^f/dnu_j, C_bad,j^r=d xi_j^r/dnu_j and C_bad,j^bi=d xi_j^bi/dnu_j=C_bad,j^f+C_bad,j^r; each is defined nu_j-a.e. on the actual owner law",
        "L1_bounds": {
            "mass_strict_upper": str(COAREA_MASS),
            "forward_F10_strict_upper": str(FORWARD_F10),
            "reverse_F10_strict_upper": str(REVERSE_F10),
            "bidirectional_F10_strict_upper": str(BIDIRECTIONAL_F10),
            "complement_bidirectional_integral": "integral_(A_col^c)C_bad,j^bi dnu_j <= xi_j^bi(total) < 2395081816467609/880000",
        },
        "cemetery_pushforward": "omega maps to dagger_(t54(omega),endpoint/root,j) on A_col^c; the label carrier is the standard-Borel product of the t54 token space, the continuous endpoint/root chart and the fixed insertion index, not a countable atom list; this deterministic Borel positive kernel preserves the fixed-j marked mass and RN F10 integral",
        "cemetery_scope_guard": "this preserves only fixed-j marked mass/F10 on a labelled Borel cemetery carrier; it is not a strong trace, all-insertion assembly, survivor contraction, or strong cemetery theorem",
        "signature_rows": strata,
        "signature_rows_sha256": digest(strata),
        "physical_trace_value_or_nullity": "NOT_CERTIFIED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "fixed_insertion_same_law_positive_complement_mass_anchor": "CERTIFIED",
        "fixed_insertion_same_law_positive_complement_F10_anchor": "CERTIFIED",
        "fixed_insertion_labelled_cemetery_pushforward": "CERTIFIED_CHARGE_PRESERVING",
        "all_insertion_time_positive_complement_anchor": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_ACTUAL_FIXED_INSERTION_OWNER_COMPLEMENT_RN_ANCHOR",
    }


def power_orlicz_frontier() -> dict[str, Any]:
    c = constants()
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4381, 10000):
        r = clock(k, c["beta"])
        y = c["w"] ** r
        phi = y ** c["q_col"]
        raw = Decimal(2) ** (k + 1)
        rows.append({
            "K": k,
            "r_K": r,
            "Phi_over_raw": str(+(phi / raw)),
            "lower_check": phi >= raw,
            "upper_check": phi < (c["w"] ** c["q_col"]) * raw,
        })
    return {
        "same_law_scope": "all integrals below are with respect to the same actual nu_j restricted to A_col; no parent-W, collision-SRB or substitute clearance law is used",
        "clock_variable": "Y(omega)=w_Z^r_(K(omega)) on A_col",
        "explicit_power": "q_col=log(2)/(beta*log(w_Z))=1/alpha_opt",
        "q_col_decimal": str(c["q_col"]),
        "Orlicz_function": "Phi(t)=t^q_col; q_col>1, so Phi is increasing convex and Phi(t)/t tends to infinity",
        "pointwise_two_sided_bound": "2^(K+1)<=Phi(Y)<w_Z^q_col*2^(K+1), because beta(K+1)<=r_K<beta(K+1)+1",
        "exact_same_law_iff": "Z_col=integral_(A_col)2^(K+1)dnu_j<infinity iff integral_(A_col)Phi(Y)dnu_j<infinity",
        "clock_consequence": "either equivalent condition implies integral Y dnu_j<infinity, but the converse need not hold",
        "active_Abel_frontier": "the Round59 active series remains the sharp clock criterion; no pinned Fbar_j envelope, finite raw Z_col or finite power-Orlicz RHS exists",
        "finite_truncation": "for K_N=min(K,N), integral Phi(w_Z^r_KN)dnu_j < w_Z^q_col*2^(N+1)*nu_j(A_col), but no N-uniform bound is available",
        "same_law_finite_Z_alignment_audit": "NONE: Round50 parent-W Z_B and Round42 standard-family Z are different laws/functionals; Round54 raw collar Z_col is explicitly uncontrolled",
        "separator": "the pinned full-A_col B=14 clearance family with all polynomial K moments finite but divergent clock moment also has divergent raw Z_col and divergent Phi(Y) moment",
        "rows": rows,
        "rows_sha256": digest(rows),
        "explicit_physical_power_Orlicz_criterion": "CERTIFIED_EXACT_SAME_LAW_IFF",
        "physical_active_Abel_series_finite": "NOT_CERTIFIED",
        "physical_raw_Z_col_finite": "NOT_CERTIFIED",
        "physical_power_Orlicz_bound": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXPLICIT_POWER_ORLICZ_EQUIVALENCE_WITHOUT_FINITE_RHS",
    }


def suffix_code_materialisation() -> dict[str, Any]:
    bits = [
        {"bit": "L_id", "predicate": "equality of immutable restriction/owner/event/side/word-cell coordinates", "Borel": "CERTIFIED", "universal_value": "CERTIFIED_TRUE_ROUND54"},
        {"bit": "L_word", "predicate": "retention of the Round54 half-open killed-word code", "Borel": "CERTIFIED", "universal_value": "CERTIFIED_TRUE_ROUND54"},
        {"bit": "L_input", "predicate": "the totalised C_in code satisfies the numerical Round42 canonical-input inequalities", "Borel": "CERTIFIED", "universal_value": "NOT_CERTIFIED"},
        {"bit": "L_C24", "predicate": "the 9148 registered killed bits equal the C24 survivor indicators", "Borel": "CERTIFIED", "universal_value": "NOT_CERTIFIED"},
        {"bit": "L_operator", "predicate": "K_word and O_s^9148|C24 have equal D_m evaluations for every m", "Borel": "CERTIFIED", "universal_value": "NOT_CERTIFIED"},
        {"bit": "L_output", "predicate": "labelled output chart/density/ID code equals the next C_in code", "Borel": "CERTIFIED", "universal_value": "NOT_CERTIFIED"},
        {"bit": "L_horizon", "predicate": "the integer record length and consecutive block/ID code cover the next requested block", "Borel": "CERTIFIED", "universal_value": "NOT_CERTIFIED"},
    ]
    samples = [
        {"sample": "all_good", "J_bits": [1, 1, 1, 1, 1], "R": "infinity"},
        {"sample": "input_fail", "J_bits": [0, 1, 1, 1, 1], "R": 0},
        {"sample": "operator_fail", "J_bits": [1, 1, 0, 1, 1], "R": 2},
        {"sample": "horizon_fail", "J_bits": [1, 1, 1, 1, 0], "R": 4},
    ]
    return {
        "actual_record_space": "the countable disjoint union A of Round54 actual collar records carrying s,t54,block index, root/endpoint chart, orientation, ell, finite killed-word code and retained omega; A is standard Borel",
        "state_and_kernel_spaces": "the labelled collision-plus-cemetery state X is standard Borel; its cemetery sector is a standard-Borel product of immutable token and continuous endpoint/root chart spaces rather than a countable atom list; subprobabilities form the standard-Borel evaluation space SubProb(X)",
        "countable_separating_generator": "fix a countable algebra D_m generated by rational collision-chart rectangles and a countable generating algebra of the standard-Borel cemetery label product; evaluations on all D_m separate subprobabilities, so K maps to (K(D_m))_m is injective and equality of every coordinate is equivalent to kernel equality",
        "input_code_map": "a maps to C_in(a)=(t54,chart,orientation,endpoints,ell,(E_a(D_m))_m); Round54 makes every coordinate Borel, a sentinel is used off A_col, and the Round42 canonical-input test is a Borel conjunction of its numerical orientation/length/density/shape inequalities",
        "operator_evaluation_maps": "finite composition and C24 restriction of Borel deterministic collision kernels are Borel sub-Markov kernels; hence a maps to K_word(a,D_m) and O_s^9148|C24(a,D_m) are Borel for every m",
        "output_code_map": "because the Round54 labelled collar remains one regular branch with omega retained, code its image chart/orientation/endpoints together with rational-subinterval density integrals and immutable IDs; these are Borel kernel evaluations and determine the density a.e.; use a sentinel when no next record exists",
        "next_input_code_map": "the next registered collar input is coded by the same C_in coordinates, totalised by the same sentinel",
        "equality_guard": "kernel equality and output/input equality are countable intersections of coordinate equalities in these common code spaces; this proves Borel typing only, not equality on actual records",
        "bit_rows": bits,
        "bit_rows_sha256": digest(bits),
        "unconditional_Borel_predicate_count": 7,
        "conditional_Borel_predicate_count": 0,
        "certified_universal_true_count": 2,
        "missing_universal_value_count": 5,
        "block_bit": "J_b is the product of the seven Borel bits on block b",
        "Borel_R": "R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1}; {R>=q}=intersection_(b<q){J_b=1} and {R=infinity}=intersection_(q>=1){R>=q}",
        "R_domain_guard": "R and K are read only after a in A_col is tested; the A_col^c branch uses its separately typed RN complement charge",
        "R_at_least_rK_is_Borel": "{a in A_col:R(a)>=r_K(a)} is Borel because R and integer K are Borel",
        "sample_rows": samples,
        "sample_rows_sha256": digest(samples),
        "value_separator": "Borel materialisation cannot force truth: a record may have a collar too short for the canonical input threshold, a failed C24 bit, unequal word/operator kernels, a nonmatching next input, or horizon below r_K",
        "all_seven_suffix_predicates_Borel": "CERTIFIED",
        "Borel_recovery_capacity_R_on_A_col": "CERTIFIED",
        "physical_all_seven_bits_true": "NOT_CERTIFIED",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "physical_Round54_Round42_operator_join": "NOT_CERTIFIED",
        "status": "CERTIFIED_COMMON_STANDARD_BOREL_CODES_AND_RECOVERY_CAPACITY",
    }


def fixed_j_hybrid() -> dict[str, Any]:
    return {
        "scope": "one fixed insertion time j on the actual owner law nu_j",
        "policy": "C_hyb,j=1_Acol*[1_{R>=r_K}*C_rec*w_Z^r_K+1_{R<r_K}*2^(K+1)]+1_(A_col^c)*C_bad,j^bi",
        "registry_guard": "test A_col before reading K or R; on A_col^c read only the RN density C_bad,j^bi and immutable owner/cemetery label",
        "exact_positive_iff": "integral C_hyb,j dnu_j<infinity iff both A_col long/short positive integrals are finite and the A_col^c RN integral is finite",
        "complement_term": "CERTIFIED_FINITE_AT_FIXED_J",
        "long_recovery_term": "NOT_CERTIFIED_FINITE",
        "short_raw_debt_term": "NOT_CERTIFIED_FINITE",
        "full_fixed_j_policy_finite": "NOT_CERTIFIED",
        "all_insertion_assembly": "NOT_CERTIFIED: the Round52 bounds are uniform in j and have no summable decay",
        "status": "CERTIFIED_EXACT_FIXED_J_HYBRID_WITH_FINITE_COMPLEMENT_TERM",
    }


def jordan_and_all_time_frontier() -> dict[str, Any]:
    rows = [
        {"mode": "common", "mu_plus": "a_j*delta_0", "mu_minus": "a_j*delta_0", "variation": "0", "common_mode": "a_j"},
        {"mode": "variation", "mu_plus": "a_j*delta_0", "mu_minus": "a_j*delta_1", "variation": "2*a_j", "common_mode": "0"},
        {"mode": "mixed", "mu_plus": "2*a_j*delta_0", "mu_minus": "a_j*delta_0+a_j*delta_1", "variation": "2*a_j", "common_mode": "a_j"},
    ]
    return {
        "type_guard": "C_bad,j^f/C_bad,j^r are RN densities of Round52 orientation-positive cost pushforwards; they are not Round54 Jordan mu_plus/mu_minus and no such identification is made",
        "fixed_marked_identity": "for any nonnegative charge a, integral a d(mu_plus+mu_minus)=integral a d|J|+2*integral a d(mu_plus wedge mu_minus)",
        "all_time_exact_criterion": "by positivity, sum_j w_Z^j integral a_j d(mu_plus+mu_minus)<infinity iff both the weighted variation series and weighted common-mode series are finite",
        "complement_series": "a complete cemetery theorem additionally needs sum_j w_Z^j integral_(A_col^c)C_bad,j dnu_j<infinity on the deduplicated owner assembly",
        "frozen_bound_failure": "the certified fixed-j F10 upper is independent of j, so summing it with w_Z^j>1 diverges and proves no all-time bound",
        "rows": rows,
        "rows_sha256": digest(rows),
        "fixed_insertion_orientation_positive_RN_anchor": "CERTIFIED",
        "fixed_marked_unweighted_Jordan_anchor": "CERTIFIED_PINNED_ROUND54",
        "fixed_insertion_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "fixed_insertion_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "all_time_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "all_time_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "all_time_weighted_complement_anchor": "NOT_CERTIFIED",
        "complete_positive_F10": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_FIXED_J_ORIENTATION_RN_AND_EXACT_ALL_TIME_NONJOIN",
    }


def technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-20",
        "sources_checked": ["arXiv:2604.19671v2", "arXiv:2606.19621v2"],
        "finding": "no checked source supplies owner/coarea-trace tangency nullity, a physical active-clearance tail, universal five-bit suffix truth, same-law all-time Jordan decay, or strong positive cemetery",
        "thin_pair_guard": "arXiv:2604.19671v2 evolves already-standard families under holes and requires survival normalization; it does not turn an arbitrarily thin owner trace into a uniformly proper collar family",
        "signed_transport_guard": "arXiv:2606.19621v2 does not turn signed cancellation into positive Jordan variation/common-mode moments",
        "external_dependency_imported": False,
        "status": "CHECKED_NO_DIRECT_GATE5_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "actual_fixed_insertion_owner_law_nu_j": "CERTIFIED",
        "actual_fixed_insertion_A_col_complement_submeasure": "CERTIFIED",
        "physical_A_col_trace_value_or_nullity": "NOT_CERTIFIED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "fixed_insertion_same_law_positive_complement_mass_anchor": "CERTIFIED",
        "fixed_insertion_same_law_positive_complement_F10_anchor": "CERTIFIED",
        "fixed_insertion_labelled_cemetery_pushforward": "CERTIFIED_CHARGE_PRESERVING",
        "all_insertion_time_positive_complement_anchor": "NOT_CERTIFIED",
        "exact_fixed_j_hybrid_with_finite_complement_term": "CERTIFIED",
        "physical_fixed_j_hybrid_policy_finite": "NOT_CERTIFIED",
        "physical_active_Abel_series_finite": "NOT_CERTIFIED",
        "explicit_same_law_power_Orlicz_criterion": "CERTIFIED_EXACT_IFF",
        "physical_raw_Z_col_finite": "NOT_CERTIFIED",
        "physical_power_Orlicz_bound": "NOT_CERTIFIED",
        "all_seven_suffix_predicates_Borel": "CERTIFIED_7_OF_7",
        "Borel_recovery_capacity_R_on_A_col": "CERTIFIED",
        "physical_all_seven_suffix_bits_true": "NOT_CERTIFIED_2_TRUE_5_OPEN",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "physical_Round54_Round42_operator_join": "NOT_CERTIFIED",
        "fixed_insertion_orientation_positive_RN_anchor": "CERTIFIED",
        "fixed_insertion_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "fixed_insertion_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "all_time_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "all_time_weighted_common_mode_anchor": "NOT_CERTIFIED",
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
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "Round60_aggregate_artifact_sha256": dict(ROUND60_AGGREGATE_PINS),
            "old_artifacts_modified": False,
            "parameter_scope": "base s=0 for the actual fixed-insertion owner/F10 law; |s|<=1/400 only for the already-declared suffix code schema",
            "claim_type": "actual fixed-j owner-complement RN anchors, common standard-Borel suffix code maps, exact fixed-j hybrid typing, and same-law raw-collar power-Orlicz equivalence",
        },
        "actual_owner_complement_RN_anchor": owner_complement_rn_anchor(),
        "same_law_power_Orlicz_frontier": power_orlicz_frontier(),
        "seven_bit_common_Borel_code_materialisation": suffix_code_materialisation(),
        "fixed_insertion_positive_hybrid": fixed_j_hybrid(),
        "Jordan_and_all_time_positive_frontier": jordan_and_all_time_frontier(),
        "latest_technology_audit": technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "actual fixed-insertion Round52-to-Round54 owner-law pushforward and A_col-complement Borel submeasure",
                "same-law L1 RN densities for fixed-insertion forward/reverse/bidirectional positive F10 costs",
                "fixed-insertion charge-preserving labelled complement cemetery pushforward",
                "common standard-Borel input/kernel/output codes making all seven suffix predicates and R Borel",
                "exact fixed-insertion hybrid with a finite complement term",
                "same-owner-law raw-collar and explicit power-Orlicz exact equivalence",
            ],
            "reason_no_new_field_credit": "the complement trace value/nullity, both collar integrals, active Abel/raw-Z/Orlicz finiteness, five universal suffix values, R>=r_K, all-insertion decay, Jordan joins and strong cemetery remain open",
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
        "Round60_aggregate_artifact_sha256": dict(ROUND60_AGGREGATE_PINS),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(verifier: Path) -> bytes:
    return (json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round61_complement_rn_borel_orlicz_frontier_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        args.write_manifest.write_bytes(render_manifest(args.verifier))
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("FIXED_J_COMPLEMENT_F10:", strict["fixed_insertion_same_law_positive_complement_F10_anchor"])
    print("SUFFIX_BOREL:", strict["all_seven_suffix_predicates_Borel"])
    print("ORLICZ_CRITERION:", strict["explicit_same_law_power_Orlicz_criterion"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
