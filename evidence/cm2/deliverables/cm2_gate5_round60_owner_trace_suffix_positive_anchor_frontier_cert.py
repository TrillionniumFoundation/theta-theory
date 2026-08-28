#!/usr/bin/env python3
"""Round-60 Gate-5 owner-trace / suffix / positive-anchor frontier.

This append-only leaf performs four typed joins left open in Round 59:

* it materialises the exact Round-50 -> Round-54 owner-token projection and
  audits why the Round-25 root grammar still does not prove A_col coverage;
* it records the strongest frozen active-Abel domination, including the
  conditional domination by the raw collar Z functional;
* it materialises all seven suffix predicate definitions, identifies the
  three missing Borel code-map interfaces, and freezes the conditional
  initial-run construction of R;
* it pays fixed-insertion orientation-positive rank/F10 ledgers and audits
  the still-missing join to the Round-54 Jordan marginals.

No all-time sum, physical clearance moment, full suffix join, positive
cemetery theorem, or Gate-5 field is claimed.
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
RESULT_SCHEMA = "cm2.gate5.round60-owner-trace-suffix-positive-anchor-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"

DEPENDENCIES = {
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91",
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json": "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json": "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json": "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json": "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
}

BLOCK_DEPTH = 9148
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
        ctx.prec = 120
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK_DEPTH) * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * w.ln() / Decimal(2).ln()
        return {"gamma": +gamma, "rho": +rho, "w": +w, "beta": +beta, "alpha": +alpha}


def clock(k: int, beta: Decimal | None = None) -> int:
    if k < 0:
        raise ValueError("negative level")
    beta = constants()["beta"] if beta is None else beta
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != expected:
            raise RuntimeError(f"dependency hash: {name}")
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object, parse_constant=reject_json_constant)
        if not isinstance(value, dict):
            raise RuntimeError(f"dependency root: {name}")
        loaded[name] = value
    return loaded


def validate_dependencies() -> dict[str, dict[str, Any]]:
    d = load_dependencies()
    r25 = d["cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"]["result"]["physical_branch_slope_and_root_grammar"]
    if r25["branch_type_count"] != 7 or r25["every_active_branch_has_at_most_one_isolated_root"] is not True:
        raise RuntimeError("Round25 root grammar")
    if r25["curve_by_curve_numeric_root_sequence_materialized"] is not False:
        raise RuntimeError("Round25 root sequence frontier")
    r42 = d["cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"]["result"]["numerical_C24_killed_Growth"]
    if r42["block_depth_n_star"] != BLOCK_DEPTH or r42["hereditary_under_positive_C24_killing"] is not True:
        raise RuntimeError("Round42 C24 block")
    r44 = d["cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"]["result"]["occurrence_suffix_two_trace_transport"]
    if r44["one_sign_global_positive_mass_upper"] != "8064/5" or r44["suffix_transport"]["suffix_positive_pushforward_mass_constant"] != "1":
        raise RuntimeError("Round44 positive traces")
    r50 = d["cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if r50["candidate_representation_token"] != "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label)":
        raise RuntimeError("Round50 owner token")
    if r50["corner_or_simultaneous_event_policy"] != "cemetery, before owner minimization":
        raise RuntimeError("Round50 cemetery policy")
    r51 = d["cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"]["result"]["common_dynamic_suffix_envelope"]
    if "standard-Borel registry" not in r51["regular_suffix_registry"]:
        raise RuntimeError("Round51 suffix registry")
    r52 = d["cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["sums_over_insertion_times"] is not False:
        raise RuntimeError("Round52 time scope")
    if r52["transferred_integral_2^B_strict_upper"] != str(RANK_MOMENT) or r52["transferred_bidirectional_F10_L1_strict_upper"] != str(BIDIRECTIONAL_F10):
        raise RuntimeError("Round52 positive bounds")
    r53 = d["cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json"]["result"]["transverse_trace_standard_family_audit"]
    if "root atom" not in r53["typed_owner_law"]:
        raise RuntimeError("Round53 root atom")
    r54 = d["cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"]["result"]["recordwise_owner_collar_E_Tr"]
    if r54["same_ID_label"] != "(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label,word-cell)":
        raise RuntimeError("Round54 owner token")
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 coverage boundary")
    r56 = d["cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"]["result"]["optimal_exact_gamma_recovery_clock"]
    if "ceil(beta*(k+1))" not in r56["exact_clock_definition"]:
        raise RuntimeError("Round56 clock")
    r58 = d["cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"]["result"]["strict_nonpromotion"]
    if r58["physical_A_col_full_coverage"] != "NOT_CERTIFIED" or r58["physical_clearance_horizon_joint_law"] != "NOT_CERTIFIED":
        raise RuntimeError("Round58 frontier")
    r59 = d["cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json"]["result"]["strict_nonpromotion"]
    if r59["unified_coverage_clock_Abel_criterion"] != "CERTIFIED_EXACT_IFF" or r59["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round59 baseline")
    if FORWARD_F10 + REVERSE_F10 != BIDIRECTIONAL_F10:
        raise RuntimeError("F10 arithmetic")
    return d


def owner_crosswalk_frontier() -> dict[str, Any]:
    token_rows = [
        {"position": 0, "Round50_field": "restriction-id", "Round54_field": "restriction-id", "action": "retain"},
        {"position": 1, "Round50_field": "time-j", "Round54_field": "time-j", "action": "retain"},
        {"position": 2, "Round50_field": "physical-event-signature", "Round54_field": "physical-event-signature", "action": "retain"},
        {"position": 3, "Round50_field": "primitive-key", "Round54_field": "primitive-key", "action": "retain"},
        {"position": 4, "Round50_field": "connected-rank-0", "Round54_field": "connected-rank-0", "action": "retain"},
        {"position": 5, "Round50_field": "side-label", "Round54_field": "side-label", "action": "retain"},
        {"position": 6, "Round50_field": None, "Round54_field": "word-cell", "action": "forget_under_pi_50"},
    ]
    return {
        "Round50_token": "t50=(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label)",
        "Round54_token": "t54=(restriction-id,time-j,physical-event-signature,primitive-key,connected-rank-0,side-label,word-cell)",
        "exact_projection": "pi_50(t54) drops only word-cell and equals t50; within a fixed word-cell the lift t50->t54 is injective",
        "token_rows": token_rows,
        "token_rows_sha256": digest(token_rows),
        "root_coordinate_guard": "the collar root xi and every t50 owner/event field are retained; overlapping collar images are not identified",
        "Round50_to_Round54_same_ID_crosswalk": "CERTIFIED_EXACT_BOREL_PROJECTION",
        "Round25_join_scope": "Round25 certifies seven root types, uniqueness/transversality and weak order, but explicitly has no curve-by-curve numeric root sequence and no Round50 event/primitive token rows",
        "Round25_to_Round50_exact_root_ID_crosswalk": "NOT_MATERIALIZED",
        "regular_bad_partition": "on the Round50 regular owner law after physical corner/simultaneous cemetery removal, A_col^c=N_cut union N_acc: N_cut is coincidence with another nonphysical chart/homogeneity/hole cut and N_acc is accumulation at the root",
        "already_removed_null_layer": "physical corner or simultaneous-event records are sent to cemetery before owner minimization and are absent from the regular owner law",
        "exact_trace_criterion": "nu(A_col^c)=nu(N_cut union N_acc); full coverage iff both N_cut and N_acc are nu-null",
        "minimal_missing_trace_interfaces": [
            "owner-trace nullity of each registered nonphysical cut coincidence, with a countable-union argument",
            "owner-trace nullity of grazing/accumulation roots plus local finiteness of full-word cuts off that set",
        ],
        "atomic_nonjoin_separator": "frozen-field logical model, not a claimed billiard orbit: keep one unique transverse physical owner root with exact t50/t54 crosswalk and put the owner-trace atom on an excluded homogeneity cut; the artificial cut is not a second physical event, d_other=0 and nu(A_col^c)=1",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "status": "CERTIFIED_R50_R54_CROSSWALK_AND_EXACT_OWNER_TRACE_NULLITY_FRONTIER",
    }


def active_abel_audit() -> dict[str, Any]:
    rows = []
    beta = constants()["beta"]
    for k in (0, 1, 2, 16, 4381, 10000):
        r = clock(k, beta)
        rows.append({"K": k, "r_K": r, "clock_weight": f"w_Z^{r}", "raw_collar_weight": f"2^{k + 1}", "pointwise_domination": "w_Z^r_K<2^(K+1)"})
    return {
        "Round59_active_criterion": "Mbar<infinity iff sum_(j in S)w_Z^r_j*Fbar_j<infinity, with S={j:r_(j+1)=r_j+1}",
        "frozen_data_audit": "the pinned owner/root manifests supply no numerical Fbar_j row, summable envelope, explicit physical Orlicz function, or finite raw Z_col",
        "minimal_tail_interface": "supply epsilon_j>=0 on active j with Fbar_j<=epsilon_j*w_Z^(-r_j) and sum_(j in S)epsilon_j<infinity",
        "usable_Orlicz_interface": "supply one explicit increasing convex Phi with Phi(t)/t->infinity and a proved finite integral Phi(w_Z^r_Kbar)dnu; fixed-law existence is not a bound",
        "raw_collar_domination": "because 1<w_Z<2 and r_K<=K+1, w_Z^r_K<2^(K+1)=ell(K)^(-1) pointwise on A_col; hence finite Z_col implies the physical clock moment",
        "raw_collar_finiteness": "NOT_CERTIFIED",
        "rows": rows,
        "rows_sha256": digest(rows),
        "physical_active_Abel_series_finite": "NOT_CERTIFIED",
        "physical_Orlicz_bound": "NOT_CERTIFIED",
        "status": "CERTIFIED_SHARPEST_FROZEN_ABEL_AND_RAW_COLLAR_DOMINATION_AUDIT",
    }


def suffix_predicate_materialisation() -> dict[str, Any]:
    bits = [
        {"bit": "L_id", "predicate_definition": "equality of immutable restriction/owner/event/side/word-cell code", "definition_materialized": True, "Borel_on_frozen_registry": "CERTIFIED", "universal_value_on_A_col": "CERTIFIED_TRUE_ROUND54"},
        {"bit": "L_word", "predicate_definition": "Round54 half-open collar killed-word intertwining code is retained", "definition_materialized": True, "Borel_on_frozen_registry": "CERTIFIED", "universal_value_on_A_col": "CERTIFIED_TRUE_ROUND54"},
        {"bit": "L_input", "predicate_definition": "collar input domain/orientation/density/length/mass code lies in the Round42 canonical-family input schema", "definition_materialized": True, "Borel_on_frozen_registry": "CONDITIONAL_ON_CANONICAL_INPUT_CODE_MAP", "universal_value_on_A_col": "NOT_CERTIFIED"},
        {"bit": "L_C24", "predicate_definition": "finite conjunction over t=0,...,9147 of the registered killed bit equalling the C24 survivor indicator", "definition_materialized": True, "Borel_on_frozen_registry": "CERTIFIED", "universal_value_on_A_col": "NOT_CERTIFIED"},
        {"bit": "L_operator", "predicate_definition": "equality of K_word and the positive C24 restriction of O_s^9148 on a countable determining algebra", "definition_materialized": True, "Borel_on_frozen_registry": "CONDITIONAL_ON_BOTH_KERNEL_EVALUATION_MAPS", "universal_value_on_A_col": "NOT_CERTIFIED"},
        {"bit": "L_output", "predicate_definition": "diagonal equality of output carrier/density/ID code and next-block input code, with no unregistered recut or renormalisation", "definition_materialized": True, "Borel_on_frozen_registry": "CONDITIONAL_ON_OUTPUT_AND_NEXT_INPUT_CODE_MAPS", "universal_value_on_A_col": "NOT_CERTIFIED"},
        {"bit": "L_horizon", "predicate_definition": "integer record-length test plus consecutive block/ID equality for the requested next block", "definition_materialized": True, "Borel_on_frozen_registry": "CERTIFIED", "universal_value_on_A_col": "NOT_CERTIFIED"},
    ]
    samples = [
        {"sample": "all_good", "J_bits": [1, 1, 1, 1], "R": "infinity"},
        {"sample": "fail_at_0", "J_bits": [0, 1, 1, 1], "R": 0},
        {"sample": "fail_at_2", "J_bits": [1, 1, 0, 1], "R": 2},
        {"sample": "fail_at_3", "J_bits": [1, 1, 1, 0], "R": 3},
    ]
    return {
        "bit_rows": bits,
        "bit_rows_sha256": digest(bits),
        "missing_value_count": 5,
        "all_seven_predicate_definitions_materialized": True,
        "unconditional_Borel_predicate_count": 4,
        "conditional_Borel_predicate_count": 3,
        "Borel_typing_guard": "equality on a countable determining algebra is Borel only after both kernel evaluation maps are Borel; Round42/54 do not freeze those two maps on one common code registry",
        "minimal_code_map_interface": [
            "a standard-Borel Round42 canonical-input code map on the actual collar records",
            "Borel evaluations a->K_word(a,b;A_m) and a->O_s^9148(a,b;A_m) for one countable determining algebra {A_m}",
            "Borel output and next-input carrier/density/ID code maps",
        ],
        "block_bit": "J_b=product(L_id,L_word,L_input,L_C24,L_operator,L_output,L_horizon) for block b",
        "R_on_A_col": "R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1} in N union {infinity}, defined only for a in A_col",
        "R_Borel_proof_conditional": "once all seven bit maps are Borel, {R>=q}=intersection_(b<q){J_b=1} and {R=infinity}=intersection_(q>=1){R>=q}; hence R is Borel on A_col",
        "sample_rows": samples,
        "sample_rows_sha256": digest(samples),
        "policy_guard": "C_policy=infinity on A_col^c; only after testing a in A_col may the formula read K(a), R(a), or compare R(a)>=r_K(a)",
        "Borel_recovery_capacity_R_on_A_col": "CONDITIONAL_SCHEMA",
        "physical_all_seven_bits_true": "NOT_CERTIFIED",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "physical_Round54_Round42_operator_join": "NOT_CERTIFIED",
        "status": "CERTIFIED_SEVEN_PREDICATE_DEFINITIONS_WITH_CONDITIONAL_BOREL_R",
    }


def hybrid_complement_policy() -> dict[str, Any]:
    strata = [
        {"owner_signature_stratum": "source_core_clipping_face", "possible_A_col_complement_mechanism": "endpoint/chart-cut coincidence", "actual_trace_mass": "NOT_CERTIFIED"},
        {"owner_signature_stratum": "intermediate_core_avoidance_preimage_face", "possible_A_col_complement_mechanism": "homogeneity/cut coincidence or accumulation", "actual_trace_mass": "NOT_CERTIFIED"},
        {"owner_signature_stratum": "terminal_core_preimage_face", "possible_A_col_complement_mechanism": "homogeneity/cut coincidence or accumulation", "actual_trace_mass": "NOT_CERTIFIED"},
        {"owner_signature_stratum": "collision_singularity_or_owner_change_face", "possible_A_col_complement_mechanism": "tangency/grazing or owner-cut coincidence", "actual_trace_mass": "NOT_CERTIFIED"},
        {"owner_signature_stratum": "moving_occurrence_face", "possible_A_col_complement_mechanism": "grazing/full-word boundary accumulation", "actual_trace_mass": "NOT_CERTIFIED"},
    ]
    return {
        "signature_rows": strata,
        "signature_rows_sha256": digest(strata),
        "trace_typing_guard": "these are singular owner/coarea trace laws; collision-area nullity of a grazing or tangency stratum does not imply zero owner-trace mass",
        "pure_collar_policy": "Round59 assigns infinite cost on A_col^c, so its finiteness forces nu(A_col^c)=0",
        "conditional_hypotheses": [
            "the three missing code-map interfaces are supplied so that R is Borel on A_col",
            "C_bad is a same-owner-law measurable nonnegative charge on A_col^c",
        ],
        "hybrid_policy_definition": "C_hyb=1_Acol*[1_{R>=r_K}*C_rec*w_Z^r_K+1_{R<r_K}*2^(K+1)]+1_(A_col^c)*C_bad, where C_bad is a separately typed nonnegative direct positive trace/cemetery charge",
        "registry_guard": "the A_col branch is tested before K or R is read; C_bad is defined on A_col^c without extending, fabricating, or comparing K/R there",
        "exact_positive_iff": "under the supplied Borel-R and measurable-nonnegative-C_bad hypotheses, integral C_hyb dnu<infinity iff the recovered-long A_col integral, the short/misaligned A_col raw-debt integral, and the A_col^c direct positive-anchor integral are all finite",
        "full_coverage_not_logically_necessary": "a complete hybrid theorem may allow nu(A_col^c)>0 when integral_(A_col^c)C_bad dnu<infinity; full coverage is necessary only for the pure infinite-complement collar policy",
        "minimal_C_bad_fields": [
            "immutable owner/event/side/word signature and Borel A_col-complement stratum",
            "a positive trace or cemetery carrier on that same stratum",
            "a nonnegative F10/cemetery charge C_bad with a finite same-law integral",
            "deduplicated assembly across all insertion times",
        ],
        "physical_A_col_complement_trace_mass": "NOT_CERTIFIED",
        "physical_A_col_complement_positive_anchor": "NOT_CERTIFIED",
        "physical_hybrid_policy_finite": "NOT_CERTIFIED",
        "status": "CERTIFIED_CONDITIONAL_EXACT_IFF_ON_ANY_SUPPLIED_BOREL_R_AND_NONNEGATIVE_C_BAD",
    }


def fixed_time_positive_anchors() -> dict[str, Any]:
    rows = [
        {"ledger": "owner_selected_orientation_rank_2^B", "positive_upper": str(RANK_MOMENT), "Jordan_pair_identification": "NOT_PINNED"},
        {"ledger": "orientation_F10_forward", "positive_upper": str(FORWARD_F10), "Jordan_pair_identification": "NOT_PINNED"},
        {"ledger": "orientation_F10_reverse", "positive_upper": str(REVERSE_F10), "Jordan_pair_identification": "NOT_PINNED"},
        {"ledger": "orientation_F10_bidirectional", "positive_upper": str(BIDIRECTIONAL_F10), "sum_check": "forward+reverse=bidirectional", "Jordan_pair_identification": "NOT_PINNED"},
        {"ledger": "Round54_Jordan_marginal_unweighted_mass", "one_marginal_upper": "8064/5", "charge": "a=1 only"},
    ]
    separator_rows = [
        {"insertion_block": p, "fixed_time_mass": "1", "common_mode_case": "mu_plus=mu_minus", "variation_case": "mu_plus perpendicular mu_minus", "weighted_term": f"w_Z^{p}"}
        for p in (0, 1, 4, 16)
    ]
    return {
        "scope": "one fixed insertion time j, aggregated over all registered finite regular records n>j and owner-selected representations",
        "orientation_anchor": "Round52 certifies positive owner-selected rank and forward/reverse F10 charges at each fixed insertion time",
        "Jordan_pair_type_audit": "Round54 defines mu_plus/mu_minus from the Jordan decomposition of sigma_e and hit/miss kernels, while Round51/52 bounds the positive endpoint coarea law m_occ with forward/reverse orientation costs; no dependency pins these as the same two marginals with the same charge",
        "unweighted_Jordan_anchor": "Round54 separately certifies mu_plus(total)=mu_minus(total)=abs(lambda)(source)<=8064/5 for each fixed marked pair; this pays only charge a=1",
        "minimal_weighted_join": "on the same immutable owner record prove abs(lambda_j)<=m_occ,j^owner and prove the desired Jordan charge a is preserved by H_j/M_j and dominated by the frozen orientation F10 charge",
        "rows": rows,
        "rows_sha256": digest(rows),
        "fixed_insertion_orientation_positive_rank_anchor": "CERTIFIED",
        "fixed_insertion_orientation_positive_F10_anchor": "CERTIFIED",
        "fixed_marked_unweighted_Jordan_marginal_anchor": "CERTIFIED",
        "fixed_insertion_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "fixed_insertion_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "all_time_guard": "the fixed-j bounds are uniform but have no j-decay; summing them over infinitely many insertion times, especially with w_Z^j>1, is illegal",
        "two_global_nonjoin_models": "common-mode model has mu_plus=mu_minus at every j, so J_j=0 but sum_j w_Z^j*lambda_j is infinite; variation model uses disjoint equal-mass marginals, so lambda_j=0 but sum_j w_Z^j*abs(J_j) is infinite",
        "separator_rows": separator_rows,
        "separator_rows_sha256": digest(separator_rows),
        "minimal_global_positive_interface": "prove a summable all-insertion-time owner source charge, or a block bound A_j<=C*kappa^j with w_Z*kappa<1, separately including excluded/cemetery records",
        "global_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "global_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "complete_positive_F10": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_ORIENTATION_POSITIVE_ANCHORS_AND_EXACT_JORDAN_TYPE_NONJOIN",
    }


def technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-20",
        "official_sources_checked": ["arXiv:2606.10155v1", "arXiv:2606.19621v2"],
        "finding": "no checked source supplies the actual owner-trace clearance nullity/tail, the seven-bit physical suffix equality, an all-time positive owner anchor, or strong cemetery",
        "signed_transport_guard": "arXiv:2606.19621v2 concerns inter-sign transport regularity and does not convert signed cancellation into Jordan-variation or common-mode positive moments",
        "external_dependency_imported": False,
        "status": "CHECKED_NO_DIRECT_GATE5_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "Round50_Round54_exact_owner_token_crosswalk": "CERTIFIED",
        "Round25_Round50_exact_root_ID_crosswalk": "NOT_MATERIALIZED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "exact_A_col_complement_positive_hybrid_iff": "CERTIFIED_CONDITIONAL_EXACT_IFF_ON_ANY_SUPPLIED_BOREL_R_AND_NONNEGATIVE_C_BAD",
        "physical_A_col_complement_trace_mass": "NOT_CERTIFIED",
        "physical_A_col_complement_positive_anchor": "NOT_CERTIFIED",
        "physical_hybrid_policy_finite": "NOT_CERTIFIED",
        "physical_active_Abel_series_finite": "NOT_CERTIFIED",
        "physical_tail_or_Orlicz_bound": "NOT_CERTIFIED",
        "all_seven_suffix_predicate_definitions": "CERTIFIED",
        "all_seven_suffix_bits_Borel_predicates": "NOT_CERTIFIED",
        "Borel_recovery_capacity_R_on_A_col": "CONDITIONAL_SCHEMA",
        "physical_all_seven_suffix_bits_true": "NOT_CERTIFIED",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "fixed_insertion_orientation_positive_rank_anchor": "CERTIFIED",
        "fixed_insertion_orientation_positive_F10_anchor": "CERTIFIED",
        "fixed_marked_unweighted_Jordan_marginal_anchor": "CERTIFIED",
        "fixed_insertion_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "fixed_insertion_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "global_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "global_weighted_common_mode_anchor": "NOT_CERTIFIED",
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
            "old_artifacts_modified": False,
            "parameter_scope": "Round25/50 root audit at s=0; Round42/54 suffix schema for fixed |s|<=1/400; fixed-insertion positive anchors at s=0",
            "claim_type": "exact owner-token crosswalk, owner-trace coverage frontier, active-Abel audit, seven suffix predicate definitions with conditional R on A_col, and fixed-insertion orientation-positive anchors",
        },
        "owner_root_crosswalk_and_coverage_frontier": owner_crosswalk_frontier(),
        "active_Abel_Orlicz_physical_audit": active_abel_audit(),
        "seven_bit_suffix_Borel_materialisation": suffix_predicate_materialisation(),
        "A_col_complement_positive_hybrid_policy": hybrid_complement_policy(),
        "fixed_insertion_positive_anchor_and_global_frontier": fixed_time_positive_anchors(),
        "latest_technology_audit": technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "exact Round50-to-Round54 owner-token Borel projection",
                "exact owner-trace bad-set/nullity interface",
                "raw collar Z domination of the optimal clock moment",
                "five previously missing suffix predicate definitions with an exact three-code-map Borel frontier",
                "conditional Borel recovery-capacity construction on A_col",
                "conditional exact A_col-collar plus A_col-complement positive-anchor hybrid iff for supplied Borel R and measurable nonnegative C_bad",
                "fixed-insertion orientation-positive rank/F10 anchors and the exact Jordan-marginal type nonjoin",
            ],
            "reason_no_new_field_credit": "neither pure A_col coverage nor the alternative A_col-complement positive anchor is certified; the active Abel/Orlicz bound is absent; three suffix code maps and every missing universal value remain open; and the fixed-insertion orientation ledgers are not pinned to the weighted Jordan marginals",
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
    return (json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        args.write_manifest.write_bytes(render_manifest(args.verifier))
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("R50_R54_CROSSWALK:", strict["Round50_Round54_exact_owner_token_crosswalk"])
    print("A_COL_COVERAGE:", strict["physical_A_col_full_coverage"])
    print("BOREL_R_ON_A_COL:", strict["Borel_recovery_capacity_R_on_A_col"])
    print("FIXED_INSERTION_ORIENTATION_F10:", strict["fixed_insertion_orientation_positive_F10_anchor"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
