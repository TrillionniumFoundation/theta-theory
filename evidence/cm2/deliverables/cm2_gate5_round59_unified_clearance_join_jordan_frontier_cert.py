#!/usr/bin/env python3
"""Round-59 Gate-5 unified clearance / operator-join / Jordan frontier.

This append-only leaf turns the Round-58 restricted clearance ledger into a
single physical extended clock by assigning Kbar=infinity on A_col^c.  Its
finite-truncation Abel identity simultaneously detects coverage and moment
finiteness, and its active-clock compression is an exact Dini criterion.

The leaf also audits the tempting Round-25 root-isolation coverage join,
factorises the Round-54/Round-42 operator join into independently typed bits,
and gives the exact positive-measure identity behind the missing Jordan
anchor moment.  No artificial collar density or signed cancellation is used
as a positive bound.
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
RESULT_SCHEMA = "cm2.gate5.round59-unified-clearance-join-jordan-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round59-unified-clearance-join-jordan-frontier-manifest-2026-07-20.json"

DEPENDENCIES = {
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91",
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4",
    "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json": "1a53a0bac41f6c0d6f8155c69b67daf31337b5f13578af9fb9f497d16277d6ad",
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json": "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5",
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b",
    "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json": "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590",
    "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json": "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    "cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json": "ff54ad55f1e065ccf390f83a83cc6135aa22f0cabc7753fd700b38e05af1701c",
    "cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json": "c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479",
    "cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json": "89d2bed9f93140637d6079d7b425ce44ed1541e2da59776a446f4bd0f428c0f3",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json": "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
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
    r25 = d["cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"]["result"]
    roots = r25["physical_branch_slope_and_root_grammar"]
    if roots["every_active_branch_has_at_most_one_isolated_root"] is not True or roots["stable_unstable_transversality_gap_strict_lower"] != "50/9":
        raise RuntimeError("Round25 isolated-root theorem")
    if r25["strict_scope_boundary"]["Gate5"] != "NOT_CERTIFIED":
        raise RuntimeError("Round25 Gate5 boundary")
    r42 = d["cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"]["result"]["numerical_C24_killed_Growth"]
    if r42["block_depth_n_star"] != BLOCK_DEPTH or r42["hereditary_under_positive_C24_killing"] is not True:
        raise RuntimeError("Round42 block")
    r50 = d["cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"]["result"]["global_owner_aware_boundary_ZB_kernel"]
    if r50["index_space_is_standard_Borel"] is not True or r50["finite_after_sum_over_all_depths"] != "NOT_CERTIFIED":
        raise RuntimeError("Round50 owner law")
    r51 = d["cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"]["result"]["common_dynamic_suffix_envelope"]
    if "all finite regular suffix branches" not in r51["regular_suffix_registry"]:
        raise RuntimeError("Round51 suffix registry")
    r52 = d["cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"]["result"]["fixed_insertion_same_ID_owner_tail_transfer"]
    if r52["sums_over_insertion_times"] is not False:
        raise RuntimeError("Round52 fixed-time guard")
    r53 = d["cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json"]["result"]["transverse_trace_standard_family_audit"]
    if "root atom" not in r53["typed_owner_law"]:
        raise RuntimeError("Round53 root law")
    r54 = d["cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"]["result"]["recordwise_owner_collar_E_Tr"]
    if r54["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED" or "homogeneity" not in r54["positive_clearance_predicate"]:
        raise RuntimeError("Round54 coverage frontier")
    if "word-cell" not in r54["same_ID_label"] or "K_word" not in r54["killed_word_intertwining"]:
        raise RuntimeError("Round54 label/intertwining")
    r55 = d["cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json"]["result"]["dyadic_debt_layer_delayed_recovery"]
    if r55["physical_Round54_to_Round42_same_operator_join"] != "NOT_CERTIFIED":
        raise RuntimeError("Round55 operator frontier")
    r56 = d["cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json"]["result"]["optimal_exact_gamma_recovery_clock"]
    if "ceil(beta*(k+1))" not in r56["exact_clock_definition"]:
        raise RuntimeError("Round56 clock")
    r57 = d["cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json"]["result"]
    if r57["exact_clearance_negative_moment_equivalence"]["physical_same_law_negative_moment"] != "NOT_CERTIFIED":
        raise RuntimeError("Round57 moment frontier")
    r58 = d["cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json"]["result"]
    if r58["strict_nonpromotion"]["physical_A_col_full_coverage"] != "NOT_CERTIFIED" or r58["strict_nonpromotion"]["physical_clearance_horizon_joint_law"] != "NOT_CERTIFIED":
        raise RuntimeError("Round58 frontier")
    if not Q(4999, 10000) < GAMMA < Q(1, 2) or not Q(1) < W_Z < Q(4, 3):
        raise RuntimeError("constant arithmetic")
    return d


def active_rows() -> list[dict[str, Any]]:
    beta = constants()["beta"]
    rows = []
    for j in (0, 1, 2, 4378, 4379, 4380, 4381, 4382, 8761, 10000):
        r0, r1 = clock(j, beta), clock(j + 1, beta)
        rows.append({"j": j, "r_j": r0, "r_j_plus_1": r1, "active": r1 == r0 + 1, "Delta_a_j": "(w_Z-1)*w_Z^r_j" if r1 == r0 + 1 else "0"})
    return rows


def unified_infinite_clock() -> dict[str, Any]:
    rows = active_rows()
    return {
        "extended_level": "Kbar(a)=K(a) on A_col and Kbar(a)=infinity on A_col^c; Kbar is Borel into N union {infinity}",
        "extended_weight": "a_k=w_Z^r_k for finite k and a_infinity=infinity",
        "extended_tail": "Fbar_j=nu{Kbar>j}=nu(A_col^c)+nu{a in A_col:K(a)>j}",
        "coverage_identity": "lim_(j->infinity)Fbar_j=nu(A_col^c), so A_col is full iff Fbar_j tends to zero",
        "finite_truncation": "M_N=integral a_(min(Kbar,N))dnu=a_0*nu(total)+sum_(j=0)^(N-1)(a_(j+1)-a_j)*Fbar_j",
        "monotone_limit": "Mbar=lim_N M_N=integral a_Kbar dnu in [0,infinity]",
        "unified_iff": "Mbar<infinity iff nu(A_col^c)=0 and integral_(A_col)w_Z^r_K dnu<infinity",
        "active_set": "S={j>=0:r_(j+1)=r_j+1}; since 0<beta<1 every increment is zero or one",
        "active_compression": "Mbar=a_0*nu(total)+(w_Z-1)*sum_(j in S)w_Z^r_j*Fbar_j",
        "exact_tail_criterion": "Mbar<infinity iff sum_(j in S)w_Z^r_j*Fbar_j<infinity; this single series already forces coverage",
        "exponential_comparison": "with alpha_opt=beta*log_2(w_Z), w_Z^r_j is within fixed positive factors of 2^(alpha_opt*j)",
        "physical_finiteness": "NOT_CERTIFIED",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_UNIFIED_COVERAGE_AND_CLOCK_ABEL_CRITERION",
    }


def dini_orlicz_frontier() -> dict[str, Any]:
    return {
        "critical_tail_family": "for p>0 and 0<c<=w_Z^r_0 set Fbar_j=c/[w_Z^r_j*(j+1)^p], Fbar_-1=1 and m_(j+1)=Fbar_j-Fbar_(j+1); monotonicity of r_j and (j+1)^p makes the masses nonnegative, and Fbar_j->0 gives a full-coverage probability law",
        "exact_Dini_reduction": "on active j, (a_(j+1)-a_j)Fbar_j=c*(w_Z-1)/(j+1)^p",
        "sharp_threshold": "the clock moment is finite iff p>1; p=1 is the critical harmonic divergence",
        "why_active_deletion_does_not_change_threshold": "#(S intersect [0,N))=r_N-r_0, hence S has asymptotic density beta>0",
        "pure_critical_envelope_insufficient": "Fbar_j<=c/w_Z^r_j and Fbar_j tends to zero do not imply finiteness; the p=1 law has full coverage but divergent moment",
        "all_polynomial_separator": "put m_n=1/[100*n*w_Z^r_n] for n>=1 and the remaining mass at K=0; full A_col, B=14 and every polynomial K moment are finite, but the clock moment contains (1/100)*sum 1/n=infinity",
        "separator_mass_guard": "alpha_opt>0.0012 gives sum_(n>=1)m_n<0.071<1, so the remaining K=0 mass is positive",
        "aligned_join_guard": "the separator may set every future join bit true and recovery capacity R>=r_K; even a perfect suffix join cannot replace the missing tail moment",
        "Orlicz_variable": "X=a_Kbar with value infinity on A_col^c",
        "exact_Orlicz_equivalence": "for this single finite owner law and extended nonnegative X, Mbar<infinity iff there exists increasing convex Phi:[0,infinity)->[0,infinity) with Phi(t)/t->infinity and integral Phi(X)dnu<infinity (de la Vallee-Poussin); this existence statement is not a uniform physical bound",
        "Orlicz_Abel_identity": "integral Phi(X)dnu=Phi(a_0)*nu(total)+sum_j[Phi(a_(j+1))-Phi(a_j)]Fbar_j",
        "physical_tail_or_Orlicz_bound": "NOT_CERTIFIED",
        "status": "CERTIFIED_SHARP_ACTIVE_DINI_AND_ORLICZ_FRONTIER",
    }


def round25_coverage_audit() -> dict[str, Any]:
    return {
        "tempting_join": "Round25 gives finitely many isolated physical boundary roots with slope gap >50/9 on each finite word/canonical unstable graph",
        "typing_mismatch": "Round50/54 owner tokens do not pin a Round25 component/root identifier, so exact same-root alignment is not frozen",
        "larger_Round54_distance_ledger": "d_other also sees every singularity, homogeneity, owner and hole boundary in the fixed word, not only Round25 physical boundary roots",
        "grazing_gap": "homogeneity strip boundaries can accumulate at a grazing owner root; collision-area nullity does not imply nullity for the singular owner-root trace law",
        "exact_complement_partition": "A_col^c={d_other=0}=N_coinc union N_acc, where N_coinc means the anchor lies on another registered boundary and N_acc means distinct other-boundary cuts accumulate at the anchor",
        "exact_nullity_ledger": "nu(A_col^c)=lim_(m->infinity)nu{d_other<2^-m}; full coverage is equivalent to this limit being zero",
        "ordinary_isolated_subregistry": "after an exact same-ID join, every root in a compact nongrazing chart, away from endpoints/coincidences and with locally finite full-word nonphysical cuts has d_other>0 pointwise; its owner-trace mass is not frozen",
        "sharp_compatible_separator": "logical frozen-field model only (not a claimed billiard realization): take one isolated transverse physical root and no other physical root, but nonphysical cut coordinates c=1/n^2 accumulating at it; all Round25 physical-root conclusions hold while d_other=0",
        "missing_for_full_coverage": [
            "Round25-to-Round50/54 immutable root-ID equality",
            "owner-trace nullity of grazing and endpoint roots",
            "local finiteness/separation for all nonphysical homogeneity/chart cuts",
        ],
        "A_col_full_coverage": "NOT_CERTIFIED",
        "status": "CERTIFIED_ROUND25_COVERAGE_NONJOIN_AND_GRAZING_SEPARATOR",
    }


def operator_join_frontier() -> dict[str, Any]:
    bits = [
        {"bit": "L_id", "meaning": "immutable restriction/owner/event/side/word-cell label retained", "frozen": "CERTIFIED_ROUND54"},
        {"bit": "L_word", "meaning": "one fixed-word collar has constant half-open killed/survivor bit and K_trace=Tr K_word E", "frozen": "CERTIFIED_ROUND54"},
        {"bit": "L_input", "meaning": "the labelled collar family is the exact Round42 canonical-family input domain", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_C24", "meaning": "all 9148 intermediate killed bits equal the Round42 C24 killing policy", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_operator", "meaning": "K_word over the block equals the corresponding positive restriction of O_s^9148", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_output", "meaning": "block output, density and IDs equal the next block input without unregistered recut/renormalisation", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_horizon", "meaning": "the actual owner record selects enough consecutive joined blocks", "frozen": "NOT_CERTIFIED"},
    ]
    return {
        "join_bits": bits,
        "join_bits_sha256": digest(bits),
        "block_join": "J_b=product of the seven Boolean join bits for block b",
        "recovery_capacity": "for a in A_col, R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1} in N union {infinity}",
        "Borel_future_schema": "if all seven bit predicates are Borel on the A_col owner subregistry then R is Borel there by countable initial-run tests",
        "compressed_policy": "on A_col recover iff R>=r_K and otherwise pay raw 2^(K+1) debt; assign infinite policy cost on A_col^c",
        "exact_policy_criterion": "nu(A_col^c)=0 and integral_(A_col)[1_{R>=r_K}C_rec*w_Z^r_K+1_{R<r_K}2^(K+1)]dnu<infinity; equivalently integral C_policy dnu<infinity when C_policy=infinity on A_col^c",
        "registry_guard": "Round51 catalogues all finite regular suffix branches, but does not select these seven equalities on the actual owner law",
        "scalar_guard": "equal scalar Growth constants on a disjoint tagged domain do not set L_input or L_operator to one",
        "physical_recovery_capacity": "NOT_CERTIFIED",
        "physical_Round54_Round42_join": "NOT_CERTIFIED",
        "status": "CERTIFIED_SEVEN_BIT_JOIN_AND_MINIMAL_RECOVERY_CAPACITY_SCHEMA",
    }


def jordan_anchor_frontier() -> dict[str, Any]:
    rows = [
        {"n": n, "mu_plus_mass": f"2^-{n}", "transport_distance": f"2^-{n}", "positive_charge": f"2^{2*n}", "cost_term": f"2^-{2*n}", "charge_term": f"2^{n}"}
        for n in (1, 2, 4, 8, 16)
    ]
    return {
        "measure_lattice": "for finite positive mu_plus,mu_minus let lambda=mu_plus wedge mu_minus and J=mu_plus-mu_minus",
        "exact_Jordan_identity": "mu_plus+mu_minus=abs(J)+2*lambda",
        "weighted_identity": "integral a dmu_plus+integral a dmu_minus=integral a dabs(J)+2*integral a dlambda for every nonnegative Borel a",
        "minimal_positive_iff": "positive F10/cemetery a-charge is finite iff both the weighted Jordan-variation moment and weighted common-mode lambda moment are finite",
        "why_signed_is_insufficient": "signed BL/OT control of J does not control either unbounded integral a dabs(J) or the invisible common mode lambda",
        "one_anchor_transport_theorem": "if integral a dmu_minus<infinity, integral c dpi<infinity and a(y_plus)<=C*a(y_minus)+L*c(y_plus,y_minus) on a coupling pi, then the mu_plus a-moment is finite",
        "anchor_plus_cost_not_enough": "without the pointwise charge/transport inequality, one finite marginal anchor plus finite transport cost still does not control the other marginal",
        "sharp_anchor_separator": "take mu_minus=delta_y0 with a(y0)=1 and couple mu_plus=sum_(n>=1)2^-n delta_xn to y0, with c(xn,y0)=2^-n and a(xn)=2^(2n); cost=sum 4^-n<infinity but integral a dmu_plus=sum 2^n=infinity",
        "zero_signed_separator": "when mu_plus=mu_minus, J=0 and abs(J)=0 while lambda=mu_plus may have infinite weighted moment",
        "rows": rows,
        "rows_sha256": digest(rows),
        "physical_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "physical_weighted_common_mode_anchor": "NOT_CERTIFIED",
        "positive_F10": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_JORDAN_COMMON_MODE_ANCHOR_IDENTITY",
    }


def technology_audit() -> dict[str, Any]:
    return {
        "query_date": "2026-07-20",
        "official_source": "export.arxiv.org API",
        "checked": [
            {"id": "2606.10155v1", "title": "Recent Progress in the Application of Transfer Operators to Dispersing Billiards"},
            {"id": "2606.19621v2", "title": "Regularity of the positional penalization function in inter-sign optimal transport on real measures", "updated": "2026-07-17T10:16:59Z"},
        ],
        "finding": "no source supplies the actual owner-clearance tail, A_col trace-nullity, the seven-bit Round54/Round42 join, or the two positive weighted anchors",
        "external_dependency_imported": False,
        "status": "CHECKED_NO_DIRECT_PHYSICAL_GATE5_INTERFACE",
    }


def strict_nonpromotion() -> dict[str, Any]:
    return {
        "unified_extended_Kbar_ledger": "CERTIFIED_BOREL_EXTENDED_VALUED",
        "unified_coverage_clock_Abel_criterion": "CERTIFIED_EXACT_IFF",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "physical_same_law_clock_moment_finite": "NOT_CERTIFIED",
        "physical_tail_or_Orlicz_bound": "NOT_CERTIFIED",
        "physical_recovery_capacity_R": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "physical_weighted_Jordan_variation_anchor": "NOT_CERTIFIED",
        "physical_weighted_common_mode_anchor": "NOT_CERTIFIED",
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
            "parameter_scope": "frozen fixed-|s|<=1/400 owner/collar chain; separators at s=0",
            "claim_type": "unified Kbar Abel/Dini/Orlicz criterion, Round25 coverage audit, seven-bit operator join, and positive Jordan-anchor boundary",
        },
        "unified_infinite_level_clearance_clock": unified_infinite_clock(),
        "sharp_active_Dini_Orlicz_frontier": dini_orlicz_frontier(),
        "Round25_to_A_col_coverage_audit": round25_coverage_audit(),
        "Round54_Round42_seven_bit_join_frontier": operator_join_frontier(),
        "positive_Jordan_anchor_frontier": jordan_anchor_frontier(),
        "latest_technology_audit": technology_audit(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "unified infinite-level Kbar coverage-plus-moment ledger",
                "active-clock exact Abel and critical Dini criterion",
                "Orlicz equivalent tail interface",
                "Round25 coverage nonjoin and grazing separator",
                "seven-bit block join and recovery-capacity schema",
                "exact Jordan/common-mode positive-anchor identity",
            ],
            "reason_no_new_field_credit": "physical unified-tail summability is NOT_CERTIFIED, coverage is not known, four operator bits and actual horizon remain absent, and finiteness of neither positive weighted anchor is certified",
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": strict_nonpromotion(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {"schema": MANIFEST_SCHEMA, "certificate_sha256": sha(Path(__file__).resolve()), "verifier_sha256": sha(verifier.resolve()), "dependencies": dict(DEPENDENCIES), "result": result, "verdict": result["strict_nonpromotion"]}


def render_manifest(verifier: Path) -> bytes:
    return (json.dumps(build_manifest(verifier), indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round59_unified_clearance_join_jordan_frontier_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        args.write_manifest.write_bytes(render_manifest(args.verifier))
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("UNIFIED_ABEL:", strict["unified_coverage_clock_Abel_criterion"])
    print("PHYSICAL_CLOCK_FINITE:", strict["physical_same_law_clock_moment_finite"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
