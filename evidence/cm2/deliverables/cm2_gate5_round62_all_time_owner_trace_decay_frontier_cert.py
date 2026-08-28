#!/usr/bin/env python3
"""Round-62 Gate-5 all-time owner/trace-decay frontier certificate.

This append-only leaf installs the canonical time-labelled direct-sum owner
registry and exact outer-weight ledgers.  It also removes only the source
endpoint-grazing part of the collar complement.  It does not claim an actual
all-time decay, a finite collar/Orlicz moment, five suffix truth values,
Jordan identification, strong cemetery, a completed Gate-5 field, or CM2.
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
RESULT_SCHEMA = "cm2.gate5.round62-all-time-owner-trace-decay-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json"

DEPENDENCIES = {
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json": "46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json": "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
}

ROUND61_AGGREGATE_PINS = {
    "cm2-sixty-first-direct-assault-2026-07-20.md": "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256": "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.sha256": "27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26",
}

BLOCK_DEPTH = 9148
COAREA_MASS = Q(8064, 5)
RANK_TAIL_CONSTANT = Q(9158592, 6875)
BIDIRECTIONAL_F10 = Q(2395081816467609, 880000)


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
        ctx.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK_DEPTH) * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * w.ln() / Decimal(2).ln()
        q_col = Decimal(1) / alpha
        return {"rho": +rho, "w": +w, "gamma": +gamma, "beta": +beta, "alpha": +alpha, "q_col": +q_col}


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
    for name, expected in ROUND61_AGGREGATE_PINS.items():
        _safe_dependency(name, expected)
    return loaded


def validate_dependencies() -> None:
    d = load_dependencies()
    r39 = d["cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"]["result"]
    if r39["physical_rank_L3over2_derivation"]["rank_tail"] != "m{B>b}<=(9158592/6875)*4^(-b) for every integer b>=14":
        raise RuntimeError("Round39 rank tail")
    if r39["physical_rank_L3over2_derivation"]["positive_coarea_total_mass_upper"] != str(COAREA_MASS):
        raise RuntimeError("Round39 coarea mass")
    r50 = d["cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if r50["owner_sets_pairwise_disjoint"] is not True or "time-j" not in r50["candidate_representation_token"]:
        raise RuntimeError("Round50 time-labelled owner")
    r52 = d["cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["sums_over_insertion_times"] is not False or r52["transferred_bidirectional_F10_L1_strict_upper"] != str(BIDIRECTIONAL_F10):
        raise RuntimeError("Round52 fixed-j scope")
    r54 = d["cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"]["result"]["recordwise_owner_collar_E_Tr"]
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
        raise RuntimeError("Round54 coverage boundary")
    r59 = d["cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json"]["result"]["strict_nonpromotion"]
    if r59["Gate5_maturity"] != "10/18" or r59["unified_coverage_clock_Abel_criterion"] != "CERTIFIED_EXACT_IFF":
        raise RuntimeError("Round59 Abel baseline")
    r61 = d["cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json"]["result"]
    if r61["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round61 maturity")
    if r61["seven_bit_common_Borel_code_materialisation"]["unconditional_Borel_predicate_count"] != 7:
        raise RuntimeError("Round61 Borel suffix")


def source_trace_strata() -> dict[str, Any]:
    rows = [
        {
            "stratum": "source_endpoint_exact_grazing_eta=0",
            "fixed_j_regular_owner_law": "CERTIFIED_NULL",
            "proof": "{eta=0} is contained in {B>b} for every b; on the source-marked copy, the projection of m_j^own is dominated by m_occ, whose tail is <=(9158592/6875)4^(-b)",
        },
        {
            "stratum": "corner_or_simultaneous_physical_event_inside_R_reg",
            "fixed_j_regular_owner_law": "CERTIFIED_ABSENT_BY_DOMAIN",
            "proof": "Round50/52 remove this stratum to the labelled cemetery before owner minimisation",
        },
        {
            "stratum": "exact_artificial_homogeneity_chart_endpoint_or_owner_cut",
            "fixed_j_regular_owner_law": "NOT_CERTIFIED_NULL",
            "proof": "no same-law transverse intersection/counting estimate is pinned",
        },
        {
            "stratum": "future_pullback_or_full_word_homogeneity_accumulation_with_eta>0",
            "fixed_j_regular_owner_law": "NOT_CERTIFIED_NULL",
            "proof": "the source endpoint-rank tail does not control later-word clearance",
        },
    ]
    return {
        "actual_law": "nu_j=(q_j)_#m_j^own at base s=0; the source-marked copy retains omega and endpoint/root coordinates from which eta/B are Borel-read, together with the immutable time-j owner token",
        "source_grazing_nullity": "CERTIFIED_ON_EVERY_FIXED_J_REGULAR_OWNER_LAW",
        "source_grazing_pushforward": "if G_src,j={retained eta=0}, then nu_j(G_src,j)=m_j^own(q_j^-1 G_src,j)=0",
        "rank_tail_constant": str(RANK_TAIL_CONSTANT),
        "simultaneous_event_scope_guard": "absence holds only inside the already-regular owner law; the mass/charge sent to cemetery before that restriction is not bounded here",
        "remaining_A_col_complement": "N_cut^(artificial/endpoint/owner) union N_acc^(future/full-word); its value, nullity and positive charge remain open",
        "rows": rows,
        "rows_sha256": digest(rows),
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "global_complement_trace_nullity": "NOT_CERTIFIED",
        "strong_cemetery_for_removed_strata": "NOT_CERTIFIED",
        "status": "CERTIFIED_SOURCE_GRAZING_NULL_SUBSTRATUM_ONLY",
    }


def harmonic_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (0, 1, 3, 7, 15, 31):
        h = sum((Q(1, j + 1) for j in range(n + 1)), Q(0))
        rows.append({"N": n, "weighted_partial_sum": str(h), "strictly_increasing": True})
    return rows


def all_time_owner_registry() -> dict[str, Any]:
    rows = harmonic_rows()
    return {
        "registry": "X_all=disjoint_union_(j>=0)({j}xX_j), a canonical minimal standard-Borel implementation retaining the complete t54 token and insertion coordinate j; injectively equivalent Borel encodings are equally legal",
        "legal_owner_rule": "any valid owner quotient must retain j or an equivalent immutable insertion coordinate; owner minimisation is only among representations of the same physical-event signature, so records at different insertion times are distinct Duhamel/physical events and cannot be collapsed",
        "cross_j_deduplication": "CERTIFIED_ILLEGAL_FOR_THE_FROZEN_OPERATOR_IDENTITY",
        "unweighted_measure": "nu_all=sum_j delta_j tensor nu_j on X_all is sigma-finite; finiteness is not asserted",
        "bad_charge": "c_j=integral_(A_col^c)C_bad,j^bi dnu_j in [0,infinity), finite for each fixed j by Round61",
        "weighted_measure": "Xi_bad^w=sum_j w_Z^j delta_j tensor (1_(A_col^c)C_bad,j^bi nu_j), an extended positive measure on X_all",
        "exact_finiteness_criterion": "Xi_bad^w(X_all)<infinity iff sum_j w_Z^j c_j<infinity",
        "tail_definition": "T_n=sum_(j>=n)c_j in [0,infinity]",
        "exact_outer_Abel_identity": "sum_j w_Z^j c_j=T_0+(w_Z-1)sum_(n>=1)w_Z^(n-1)T_n in [0,infinity], by Tonelli applied to w_Z^j=1+(w_Z-1)sum_(n=1)^j w_Z^(n-1)",
        "geometric_sufficient_interface": "c_j<=C*kappa^j and w_Z*kappa<1 imply sum_j w_Z^j c_j<=C/(1-w_Z*kappa)",
        "sharpness": "the geometric threshold w_Z*kappa<1 is sharp for c_j=C*kappa^j",
        "actual_decay_row": "NOT_CERTIFIED: the frozen estimate c_j<2395081816467609/880000 is uniform in j and supplies no kappa<1",
        "finite_unweighted_harmonic_separator": "take one immutable time-j event of mass/charge b_j=w_Z^(-j)/(j+1); sum_j b_j<infinity, every fixed-j anchor is finite, but sum_j w_Z^j b_j=sum_j 1/(j+1)=infinity",
        "separator_preserves_owner_semantics": "the events have different immutable time-j coordinates, so owner minimisation does not merge them",
        "separator_rows": rows,
        "separator_rows_sha256": digest(rows),
        "all_time_weighted_complement_anchor": "NOT_CERTIFIED",
        "deduplicated_all_time_positive_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_CANONICAL_ALL_TIME_REGISTRY_EXACT_IFF_AND_SHARP_SEPARATOR",
    }


def all_time_clearance_frontier() -> dict[str, Any]:
    c = constants()
    return {
        "same_law": "for each insertion j use the actual nu_j|A_col; outer assembly uses the time-labelled direct sum and never substitutes parent-W or collision-SRB law",
        "local_variables": "Y_j=w_Z^r_(K), Z_col,j=integral 2^(K+1)dnu_j, Phi(t)=t^q_col with q_col=1/alpha_opt",
        "q_col_decimal": str(c["q_col"]),
        "outer_power_Orlicz_iff": "sum_j w_Z^j Z_col,j<infinity iff sum_j w_Z^j integral Phi(Y_j)dnu_j<infinity, from the Round61 pointwise two-sided bound and Tonelli",
        "outer_clock_Abel_identity": "sum_j w_Z^j integral Y_j dnu_j=sum_j w_Z^j[w_Z^r_0 nu_j(A_col)+(w_Z-1)sum_(k in S)w_Z^r_k nu_j{K>k}] in [0,infinity]",
        "active_set": "S={k:r_(k+1)=r_k+1}",
        "local_perfect_separator": "on each j take A_col full, K=0, R=infinity and all seven suffix bits true, with mass b_j=w_Z^(-j)/(j+1); all local clock/raw-Z/Orlicz costs are finite and sum_j b_j<infinity, while every outer w_Z^j ledger diverges harmonically",
        "logical_scope": "this is a standard-Borel positive model proving that local clearance, perfect suffix truth and finite unweighted assembly do not imply the required outer insertion decay; it is not a new billiard realization",
        "physical_active_Abel_bound": "NOT_CERTIFIED",
        "physical_raw_Z_col_bound": "NOT_CERTIFIED",
        "physical_power_Orlicz_bound": "NOT_CERTIFIED",
        "physical_outer_insertion_decay": "NOT_CERTIFIED",
        "status": "CERTIFIED_ALL_TIME_EXTENDED_IDENTITIES_WITHOUT_FINITE_RHS",
    }


def suffix_jordan_cemetery_frontier() -> dict[str, Any]:
    rows = harmonic_rows()
    return {
        "suffix_Borel_typing": "CERTIFIED_7_OF_7_PINNED_ROUND61",
        "suffix_universal_values": "2_TRUE_5_OPEN",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "five_open_bits": ["L_input", "L_C24", "L_operator", "L_output", "L_horizon"],
        "weighted_Jordan_identity": "for nonnegative Borel integrands phi_j, sum_j w_Z^j integral phi_j d(mu_j^++mu_j^-)=sum_j w_Z^j integral phi_j d|J_j|+2 sum_j w_Z^j integral phi_j d(mu_j^+ wedge mu_j^-), in [0,infinity]",
        "variation_separator": "with b_j=w_Z^(-j)/(j+1), mu_j^+=b_j delta_0 and mu_j^-=b_j delta_1, unweighted total positive mass is finite but the weighted variation series is 2 sum_j 1/(j+1)=infinity",
        "common_mode_separator": "with b_j=w_Z^(-j)/(j+1), mu_j^+=mu_j^-=b_j delta_0, J_j=0 and unweighted mass is finite but the weighted common-mode series is sum_j 1/(j+1)=infinity",
        "orientation_type_guard": "Round61 C_bad,j forward/reverse RN densities are not identified with the Round54 Jordan marginals or their same charge",
        "separator_rows": rows,
        "separator_rows_sha256": digest(rows),
        "all_time_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "all_time_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "all_time_orientation_to_Jordan_join": "NOT_CERTIFIED",
        "strong_positive_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_ALL_TIME_JORDAN_SPLIT_AND_INDEPENDENT_SEPARATORS",
    }


def pinned_obstructions() -> dict[str, Any]:
    c = constants()
    return {
        "Round52_null_survivor_face_tower": "PINNED: collision survivor mass may decay as rho^p while a collision-null face retains trace mass one; fixed-j owner finiteness yields no kappa<1 recurrence",
        "Holder_threshold": "even if trace mass rho^p were supplied, an L^q owner charge with q<=2 gives kappa=rho^(1-1/q)>=sqrt(rho)>2rho/(1+rho)=w_Z^(-1)",
        "w_Z_decimal": str(c["w"]),
        "required_new_interface": "a genuine same-owner trace/coarea recurrence with weighted all-insertion decay, or q>2 plus trace-survivor decay, or a separately typed legal cancellation theorem",
        "no_repeat_guard": "fixed-j RN finiteness, collision-volume recurrence, and signed OT cancellation are each insufficient",
        "status": "PINNED_NO_SHORTCUT",
    }


def technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-21",
        "sources_checked": ["arXiv:2604.19671v2", "arXiv:2606.19621v2"],
        "finding": "no checked official source supplies same-owner all-insertion trace decay, a physical clearance Abel/raw-Z bound, universal five-bit suffix truth, Jordan/common-mode decay or strong positive cemetery",
        "survival_guard": "arXiv:2604.19671v2 starts with standard families and uses survival-mass normalisation; it does not control the singular owner trace or its time-labelled complement charge",
        "transport_guard": "arXiv:2606.19621v2 does not turn inter-sign cancellation into positive weighted variation/common-mode moments",
        "external_dependency_imported": False,
        "status": "CHECKED_NO_DIRECT_GATE5_IMPORT",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "source_endpoint_grazing_null_on_fixed_j_regular_owner_law": "CERTIFIED",
        "global_A_col_complement_nullity": "NOT_CERTIFIED",
        "canonical_minimal_all_time_time_labelled_registry_implementation": "CERTIFIED",
        "cross_j_owner_deduplication": "CERTIFIED_ILLEGAL",
        "all_time_weighted_complement_anchor": "NOT_CERTIFIED",
        "outer_clock_Abel_identity": "CERTIFIED_EXTENDED_IDENTITY",
        "outer_raw_Z_power_Orlicz_iff": "CERTIFIED_EXACT_IFF",
        "physical_active_Abel_raw_Z_Orlicz_finite": "NOT_CERTIFIED",
        "all_seven_suffix_predicates_Borel": "CERTIFIED_7_OF_7",
        "physical_all_seven_suffix_bits_true": "NOT_CERTIFIED_2_TRUE_5_OPEN",
        "physical_R_at_least_r_K": "NOT_CERTIFIED",
        "all_time_exact_Jordan_split": "CERTIFIED_EXTENDED_IDENTITY",
        "all_time_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "all_time_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "complete_positive_F10": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "F14_F15_F17_F18": "NOT_CERTIFIED",
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
            "Round61_aggregate_artifact_sha256": dict(ROUND61_AGGREGATE_PINS),
            "old_artifacts_modified": False,
            "parameter_scope": "base s=0 actual fixed-insertion owner/coarea law; all-time statements are exact direct-sum interfaces or logical separators, not a new physical decay theorem",
            "claim_type": "source-grazing null subtrace, canonical time-labelled all-insertion registry, exact outer Abel/Orlicz/Jordan interfaces, and sharp no-decay separators",
        },
        "source_trace_strata": source_trace_strata(),
        "all_time_owner_registry": all_time_owner_registry(),
        "all_time_clearance_frontier": all_time_clearance_frontier(),
        "suffix_Jordan_cemetery_frontier": suffix_jordan_cemetery_frontier(),
        "pinned_obstructions": pinned_obstructions(),
        "latest_technology_audit": technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "fixed-j regular-owner source endpoint-grazing null subtrace",
                "canonical time-labelled all-insertion standard-Borel registry and exact weighted complement criterion",
                "outer weighted active-Abel and raw-Z/power-Orlicz exact identities",
                "outer weighted Jordan/common-mode identity and finite-unweighted harmonic separators",
            ],
            "reason_no_new_field_credit": "remaining complement strata, actual all-insertion decay, physical Abel/raw-Z/Orlicz finiteness, five suffix values, orientation-to-Jordan charge join and strong cemetery remain open",
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
        "Round61_aggregate_artifact_sha256": dict(ROUND61_AGGREGATE_PINS),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def render_manifest(verifier: Path) -> bytes:
    return (json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round62_all_time_owner_trace_decay_frontier_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        args.write_manifest.write_bytes(render_manifest(args.verifier))
        print(f"wrote {args.write_manifest}")
        return 0
    s = build_result()["strict_nonpromotion"]
    print("SOURCE_GRAZING_NULL:", s["source_endpoint_grazing_null_on_fixed_j_regular_owner_law"])
    print("ALL_TIME_COMPLEMENT:", s["all_time_weighted_complement_anchor"])
    print("GATE5_MATURITY:", s["Gate5_maturity"])
    print("CM2:", s["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
