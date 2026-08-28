#!/usr/bin/env python3
"""Round-53 Gate-4 fractional-Z and common-return frontier.

This append-only leaf identifies the exact same-measure boundary quantity
which would close the Round-52 defect moment after the certified cell-level
retyping.  If

    J_pair = integral sum_c p_c(ell_fw,c^-1 + ell_rev,c^-1)

is finite on the once-charged cell law, then the strict cell-length tail is
bounded by ``T_m < 2^-m J_pair``.  Exact layer cake and the rational bracket
``exp(1/6)<13/11`` then give

    I_D < mass + 35/(99*2^309) J_pair.

A second, independent boundary quantity is required for the positive common
terminal survivor.  Finite integrated two-view common-refinement numerator
``J_cap`` yields a recordwise common two-proper-view carrier and an integrable
additional 696-block properisation envelope.  Neither physical J is supplied
by the current D1 moment or the fixed-insertion owner trace.  In particular,
the Round-36 face injection is not silently identified with the target
standard-family Z: it must first pass through the physical aggregate growth
recurrence and a terminal-extraction inequality.

The result is therefore a sharp conditional bridge, not a promotion of the
physical q, strong singular/current cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round53-fractional-z-common-return-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round53_fractional_z_common_return_frontier_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json": (
        "7ddecb544fa5a2b243882eaf2028159c22f8437fc3fbb49fda4eb487ab181798"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": (
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
}

EXP_LOWER = Q(7, 6)
EXP_UPPER = Q(13, 11)
DEFECT_OFFSET = 309
LINEAR_TAIL_COEFFICIENT = Q(35, 99 * 2**309)
CLOSED_A = Q(360134800, 360493663)
CLOSED_MARGIN = 1 - CLOSED_A
CLOSED_RESOLVENT = 1 / CLOSED_MARGIN
CLOSED_B = 2 * 10**90
C_P = Q(4 * 10**90 * 360493663, 358863)
HALF_BLOCK = 696
CLOCK_DENOMINATOR = 4176
COMMON_MASS_LOWER = Q(249, 250)
RETURN_TAIL_A = Q(550000, 147)
RETURN_TAIL_R = Q(111718729, 111718750)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    round52 = load(
        "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
    )["result"]
    cell = round52["cell_level_retyping_audit"]
    if not cell["Borel_and_once_charge"].startswith("CERTIFIED:"):
        raise RuntimeError("Round52 cell once-charge typing")
    if cell["cell_retyping_closes_I_D"] is not False:
        raise RuntimeError("Round52 cell defect frontier")
    terminal = round52["uniform_outer_majorant_terminal_join"]
    if Q(
        terminal[
            "same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"
        ]
    ) != COMMON_MASS_LOWER:
        raise RuntimeError("Round52 common terminal mass")
    if terminal["physical_collision_time_q_L6over5"] != "NOT_CERTIFIED":
        raise RuntimeError("Round52 physical q frontier")
    if round52["large_common_mass_geometric_nonpromotion"][
        "proper_same_ID_fw_rev_return_inferred"
    ] is not False:
        raise RuntimeError("Round52 common geometry frontier")
    separator = round52["large_common_mass_geometric_nonpromotion"]
    if separator["status"] != (
        "CERTIFIED_LARGE_COMMON_MASS_BOREL_TWO_VIEW_FIELDS_DO_NOT_IMPLY_PROPER_INTERSECTION"
    ):
        raise RuntimeError("Round52 interval separator status")
    if separator["same_ID_common_mass"] != "499/500":
        raise RuntimeError("Round52 interval separator common mass")
    if separator["common_boundary_numerator"] != (
        "sum_k mass(A_k)/length(A_k)=sum_k 1=infinity"
    ):
        raise RuntimeError("Round52 interval separator boundary")

    round51 = load(
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    )["result"]
    if round51["physical_two_proper_view_object_lemma"]["status"] != (
        "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM"
    ):
        raise RuntimeError("Round51 two-view law")
    if round51["full_clock_conditional_bridge"]["physical_I_D_certified"] is not False:
        raise RuntimeError("Round51 I_D frontier")
    if round51["intersection_and_gate_frontier"]["collision_time_q"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round51 q typing")

    round50 = load(
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    )["result"]
    grouping = round50["physical_Borel_whole_family_grouping"]
    if grouping["status"] != (
        "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J"
    ):
        raise RuntimeError("Round50 grouping")
    if grouping["uniform_J_over_mass_bound_claimed"] is not False:
        raise RuntimeError("Round50 global J frontier")
    if grouping["kernel_partition_identities_mod_null"] != [
        "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
        "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
    ]:
        raise RuntimeError("Round50 once-charge partitions")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if pair["forward_and_reverse_are_two_views_not_two_charges"] is not True:
        raise RuntimeError("Round35 once charge")
    if pair["common_physical_restriction_id"] != (
        "rn-restriction:(component-id):(source-parent-W-id):(image-recut-rank)"
    ):
        raise RuntimeError("Round35 restriction ID")
    if carrier["per_carrier_numeric_recovery_clock"][
        "physical_global_D_tail_or_moment"
    ] != "NOT_CERTIFIED":
        raise RuntimeError("Round35 recovery moment frontier")

    d1 = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if d1["global_physical_L6over5_moment"]["status"] != (
        "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT"
    ):
        raise RuntimeError("Round35 D1 moment")
    d1charge = d1["arbitrary_Rn_additive_rank_sum_charge"]
    if d1charge["full_C_fw_or_C_rev_cost"] is not False:
        raise RuntimeError("Round35 D1 scope")
    if d1charge["dominates_final_same_ID_q"] is not False:
        raise RuntimeError("Round35 D1 nonpromotion")

    round36 = load(
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    )["result"]
    recurrence = round36["aggregate_Z_new_face_recurrence"]
    if recurrence["recurrence"] != "Z_(n+1)<=a*Z_n+b*m_n+J_n":
        raise RuntimeError("Round36 recurrence")
    if recurrence["aggregate_family"] != (
        "one unnormalised same-ID standard-family representation of the whole physical survivor/return level, retaining branch labels"
    ):
        raise RuntimeError("Round36 unnormalised family type")
    if recurrence["exact_resolvent"] != qstr(CLOSED_RESOLVENT):
        raise RuntimeError("Round36 resolvent")
    if round36["strict_nonpromotion"][
        "abstract_recurrence_supplies_physical_J_bound"
    ] is not False:
        raise RuntimeError("Round36 physical forcing frontier")

    owner = load(
        "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"
    )["result"]
    fixed = owner["fixed_insertion_same_ID_owner_tail_transfer"]
    if fixed["status"] != (
        "CERTIFIED_FIXED_INSERTION_SAME_ID_OWNER_TAIL_TRANSFER_ONLY"
    ):
        raise RuntimeError("Round52 owner fixed-time scope")
    if fixed["sums_over_insertion_times"] is not False:
        raise RuntimeError("Round52 owner tower frontier")
    if owner["strict_nonpromotion"]["same_ID_full_ZB_one_step_recurrence"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round52 owner recurrence frontier")
    null_separator = owner["null_survivor_face_tower_countermodel"]
    if null_separator["status"] != (
        "CERTIFIED_NULL_SURVIVOR_FACE_TOWER_NONIMPLICATION"
    ):
        raise RuntimeError("Round52 null-survivor separator status")
    if null_separator["collision_mass"] != "mu(Q_p)=rho^p and mu(Gamma)=0":
        raise RuntimeError("Round52 null-survivor collision type")
    if null_separator["trace_mass"] != (
        "nu(Q_p)=nu(Gamma)=1 for every p"
    ):
        raise RuntimeError("Round52 null-survivor trace type")

    round28 = load(
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    )["result"]
    definitions = round28["weighted_tail_transfer_theorem"]["definitions"]
    if definitions["two_views_charge_policy"] != (
        "q=max(C_fw,C_rev,2)*m is charged once, never once per view"
    ):
        raise RuntimeError("Round28 q once-charge type")
    if definitions["scope"] != (
        "regular first-return components; cemetery strong charge is accounted separately"
    ):
        raise RuntimeError("Round28 cemetery type")
    ledger = round28["first_return_mass_ledger_join"]
    if ledger["normalized_survivor_mass_symbol"] != (
        "S_n=mu_s(Q_n)/mu_s(C_s)"
    ):
        raise RuntimeError("Round28 normalized survivor type")
    if ledger["normalized_first_return_level_mass_symbol"] != (
        "a_n=sum_k mbar_s,n,k=S_(n-1)-S_n"
    ):
        raise RuntimeError("Round28 level-index shift")
    if ledger["tail_prefactor_A"] != qstr(RETURN_TAIL_A):
        raise RuntimeError("Round28 return-tail prefactor")
    if ledger["tail_block_factor_r"] != qstr(RETURN_TAIL_R):
        raise RuntimeError("Round28 return-tail factor")


def safe_defect(M: int) -> int:
    if M < 0:
        raise ValueError("M must be nonnegative")
    return 0 if M <= 310 else M - DEFECT_OFFSET


def common_z_defect(z: Q) -> int:
    """696-block count making a two-view normalized Z upper z proper."""
    if z < 0:
        raise ValueError("z must be nonnegative")
    # Properness is strict (Z<C_p*mass).  Equality therefore pays a block;
    # this avoids silently turning the closed threshold into a non-strict one.
    if z < C_P:
        return 0
    d = 1
    while Q(1, 2**d) * z >= C_P / 2:
        d += 1
    return d


def cell_tail_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for M, mass_power in ((14, 3), (310, 7), (311, 11), (400, 20), (576, 24)):
        p = Q(1, 2**mass_power)
        ell_fw = Q(1, 2**M)
        ell_rev = Q(1, 2 ** max(0, M - 3))
        pair_z = p / ell_fw + p / ell_rev
        rows.append(
            {
                "M": M,
                "mass": qstr(p),
                "ell_fw": qstr(ell_fw),
                "ell_rev": qstr(ell_rev),
                "pair_boundary_contribution": qstr(pair_z),
                "safe_defect_Dbar": safe_defect(M),
                "event_at_m_equals_M_minus_1": M > 0,
                "strict_tail_bound_at_m_equals_M_minus_1": (
                    "p<2^(-(M-1))*p*(ell_fw^-1+ell_rev^-1)"
                    if M > 0
                    else "not_used"
                ),
            }
        )
    return rows


def fractional_cell_z_bridge() -> dict[str, Any]:
    # Pure-rational proof of exp(1/6)<13/11.  For k>=2,
    # k!>=2*3^(k-2), so the remaining exponential series is bounded by
    # (1/72)*sum_{j>=0}(1/18)^j=1/68.  The final cross-product gap is one.
    exp_tail_upper = Q(1, 72) / (1 - Q(1, 18))
    exp_series_upper = 1 + Q(1, 6) + exp_tail_upper
    assert exp_tail_upper == Q(1, 68)
    assert exp_series_upper == Q(241, 204)
    assert 13 * 204 - 241 * 11 == 1
    assert exp_series_upper < EXP_UPPER
    # Rational upper evaluation of the exact Round-52 layer-cake identity
    # under T_m <= J_pair*2^-m.
    head = (EXP_UPPER**2 - 1) / Q(2**310)
    tail = (EXP_UPPER - 1) / Q(2**309) * (
        (EXP_UPPER / 2) ** 2 / (1 - EXP_UPPER / 2)
    )
    coefficient = head + tail
    assert coefficient == LINEAR_TAIL_COEFFICIENT
    assert EXP_UPPER / 2 < 1
    rows = cell_tail_rows()
    return {
        "once_charged_cell_law": (
            "retain the Round35 natural-short-cell-k and image-recut-rank; each positive cell c carries one mass p_c and two orientation lengths ell_fw,c,ell_rev,c"
        ),
        "pair_boundary_numerator": (
            "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda"
        ),
        "cell_rank": (
            "M_c=ceil(log2(1/min(ell_fw,c,ell_rev,c)))_+"
        ),
        "strict_event_identity": (
            "for every integer m>=0, {M_c>m}={min(ell_fw,c,ell_rev,c)<2^-m}"
        ),
        "pair_union_typing": (
            "1/min(ell_fw,c,ell_rev,c)=max(ell_fw,c^-1,ell_rev,c^-1)<=ell_fw,c^-1+ell_rev,c^-1 on the identical once-charged cell"
        ),
        "same_measure_tail_bound": (
            "T_m=sum_{M_c>m}p_c < 2^-m*J_pair; the strict form follows from min(ell)<2^-m"
        ),
        "no_rounding_loss": True,
        "exp_one_sixth_rational_proof": (
            "for k>=2, k!>=2*3^(k-2), hence exp(1/6)<1+1/6+1/68=241/204<13/11; the last cross-product gap is 1"
        ),
        "quarter_tail_corollary": (
            "T_m<=J_pair*2^-floor(m/4), so the Round52 rational quarter-tail bridge applies with C_quarter=J_pair"
        ),
        "direct_linear_tail_layer_cake_bound": (
            "I_D<nu(X)+[35/(99*2^309)]*J_pair"
        ),
        "direct_linear_tail_coefficient": qstr(coefficient),
        "equivalent_coefficient_form": "(70/99)*2^-310",
        "coefficient_derivation": (
            "[(13/11)^2-1]2^-310 +(2/11)2^-309*sum_{d>=2}(13/22)^d = [35/99]2^-309"
        ),
        "physical_instantiation_hypothesis": "J_pair<infinity on the full physical arbitrary-R_n cell law",
        "physical_J_pair_certified": False,
        "physical_I_D_certified": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_SAME_MEASURE_CELL_Z_TO_DEFECT_MOMENT_BRIDGE__PHYSICAL_J_PAIR_OPEN",
    }


def l1_recurrence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    z = Q(7, 5)
    for n in range(8):
        mass = Q(1, 2 ** (n + 1))
        forcing = Q(1, 3 ** (n + 1))
        z_next = CLOSED_A * z + CLOSED_B * mass + forcing
        rows.append(
            {
                "n": n,
                "Z_n": qstr(z),
                "m_n": qstr(mass),
                "face_forcing_F_n": qstr(forcing),
                "equality_model_Z_next": qstr(z_next),
            }
        )
        z = z_next
    return rows


def aggregate_z_cross_gate_bridge() -> dict[str, Any]:
    rows = l1_recurrence_rows()
    assert CLOSED_MARGIN == Q(358863, 360493663)
    assert CLOSED_RESOLVENT == Q(360493663, 358863)
    assert 1 - RETURN_TAIL_R == Q(21, 111718750)
    return {
        "abstract_recurrence": "Z_(n+1)<=a*Z_n+b*m_n+F_n",
        "a": qstr(CLOSED_A),
        "b": str(CLOSED_B),
        "exact_l1_resolvent": qstr(CLOSED_RESOLVENT),
        "finite_partial_sum_identity": (
            "(1-a)*sum_{n=1}^{N-1}Z_n+Z_N <= a*Z_0+b*sum_{n=0}^{N-1}m_n+sum_{n=0}^{N-1}F_n"
        ),
        "l1_conclusion": (
            "if sum_n m_n and sum_n F_n are finite, then sum_{n>=1}Z_n <= [a*Z_0+b*sum_n m_n+sum_n F_n]/(1-a)"
        ),
        "collision_mass_term": (
            "conditional only: if a same-ID level/normalization theorem identifies the Round36 unnormalised m_n with mu_s(C_s)*S_n (or gives an explicit fixed index shift and domination by it), then the Round28 tail gives sum_n m_n<mu_s(C_s)*A*N_open/(1-r)<infinity"
        ),
        "round28_Qn_to_round36_mn_same_ID_normalization_join": "NOT_CERTIFIED",
        "return_tail_constants": {
            "A": qstr(RETURN_TAIL_A),
            "r": qstr(RETURN_TAIL_R),
            "one_minus_r": "21/111718750",
            "N_open": "one uniform finite theorem-supplied integer, not numeric",
        },
        "target_typing": (
            "J_pair is a terminal cell standard-family boundary numerator; Round36 J_n/Round52 Z_B are face injections (roots divided by parent-W length), not J_pair itself"
        ),
        "required_physical_join_1": (
            "a same-ID level-index and normalization theorem from Round28 S_n=mu_s(Q_n)/mu_s(C_s) to the Round36 unnormalised recurrence mass m_n"
        ),
        "required_physical_join_2": (
            "an all-insertion-time same-ID face-tower L1 bound for the full F_n, including cemetery"
        ),
        "required_physical_join_3": (
            "a terminal-extraction inequality on the same cell law which bounds J_pair by the evolved aggregate Z plus terminal face injection"
        ),
        "round28_tail_supplies_join_1_without_typing": False,
        "fixed_insertion_owner_tail_supplies_join_2": False,
        "abstract_growth_recurrence_supplies_join_3": False,
        "conditional_cross_gate_consequence": (
            "once all three joins are installed, the aggregate resolvent gives J_pair<infinity and the fractional cell-Z bridge closes physical I_D"
        ),
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_ABSTRACT_L1_RESOLVENT_TO_GATE4_DEFECT_BRIDGE__PHYSICAL_MASS_NORMALIZATION_FACE_TOWER_AND_EXTRACTION_OPEN",
    }


def common_defect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in (-1, 0, 1, 4, 12, 32):
        if k == -1:
            z = C_P / 2
            label = "C_p/2"
        else:
            z = C_P * 2**k
            label = f"2^{k}*C_p"
        d = common_z_defect(z)
        relation = Q(2**d) <= 4 * z / C_P if d else True
        rows.append(
            {
                "normalized_pair_Z": label,
                "extra_block_defect_D_cap": d,
                "extra_clock_696_D_cap": HALF_BLOCK * d,
                "two_power_relation": relation,
                "proper_after_closed_evolution": True,
            }
        )
    return rows


def common_refinement_z_bridge() -> dict[str, Any]:
    rows = common_defect_rows()
    assert Q(HALF_BLOCK, CLOCK_DENOMINATOR) == Q(1, 6)
    assert EXP_UPPER**4 < 2
    assert C_P > 4
    assert 2 * CLOSED_A.numerator**696 < CLOSED_A.denominator**696
    return {
        "common_raw_subkernel": (
            "the Round52 same-parent common terminal survivor, of mass h(y)>249p(y)/250, before any normalization"
        ),
        "two_orientation_common_boundary": (
            "J_cap(y)=J_cap,fw(y)+J_cap,rev(y), computed from regular connected components of the identical common raw restriction"
        ),
        "component_registry_hypothesis": (
            "both orientation decompositions of the common raw restriction are standard-Borel regular connected-component kernels with exact outer disintegration and no duplicate charge"
        ),
        "global_hypothesis": (
            "J_cap,total=integral J_cap(y)dlambda(y)<infinity"
        ),
        "normalized_pair_boundary": "z_cap(y)=J_cap(y)/h(y) on h(y)>0",
        "extra_defect": (
            "D_cap=0 if z_cap<C_p; otherwise the least d>=1 with 2^-d*z_cap<C_p/2 (equality z_cap=C_p is not declared proper)"
        ),
        "synchronized_two_view_properisation": (
            "after 696*D_cap closed iterates the two orientation-specific pushforwards each have Z<C_p*h; the common raw points remain once charged and the Round51 transport can select one proper reference law"
        ),
        "physical_kernel_typing_boundary": (
            "two proper orientation-specific pushforwards of one common raw restriction give a proper two-view reference carrier; they are not thereby one physical first-return kernel"
        ),
        "minimality_inequality": (
            "for D_cap>0, minimality gives 2^D_cap<=4*z_cap/C_p"
        ),
        "rational_quarter_power": (
            "exp(D_cap/6)<(13/11)^D_cap<(13/11)^3*2^(D_cap/4)"
        ),
        "integrated_extra_clock_bound": (
            "integral h*exp(D_cap/6) <= H +(2197/1331)*(4/C_p)^(1/4)*H^(3/4)*J_cap,total^(1/4), where H=integral h"
        ),
        "weaker_pure_rational_bound": (
            "the preceding right side is < H+(2197/1331)*H^(3/4)*J_cap,total^(1/4) because C_p>4"
        ),
        "what_this_would_certify": (
            "a proper same-ID common terminal-survivor two-view carrier and the moment of this one additional synchronized properisation clock"
        ),
        "what_this_does_not_certify": [
            "intermediate C24 avoidance or the physical first-return interpretation",
            "moments for later/repeated recovery clocks not represented by D_cap",
            "the Round28 physical collision-time q",
            "the strong singular/current cemetery",
        ],
        "physical_common_refinement_J_cap_certified": False,
        "physical_proper_same_ID_return_certified": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_CONDITIONAL_COMMON_REFINEMENT_Z_TO_TWO_VIEW_PROPERISATION_AND_CLOCK_MOMENT__PHYSICAL_J_CAP_OPEN",
    }


def separation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (18, 19, 20, 24):
        M = n * n
        d = safe_defect(M)
        rows.append(
            {
                "band_n": n,
                "band_mass": f"2^-{n}",
                "cell_count": f"2^{M}",
                "cell_length": f"2^-{M}",
                "pair_Z_lower": f"2^{M-n}",
                "fixed_D1_density": "D0",
                "Dbar": d,
                "defect_moment_rational_lower": qstr(Q(1, 2**n) * EXP_LOWER**d),
                "next_lower_term_ratio": qstr(Q(1, 2) * EXP_LOWER ** (2 * n + 1)),
            }
        )
    return rows


def exact_nonimplication_audit() -> dict[str, Any]:
    rows = separation_rows()
    return {
        "D1_does_not_supply_J_pair": (
            "the Round52 band model has fixed finite physical D1 density D0 and finite D1 L^(6/5) mass moment, while J_pair has band contribution at least 2^(n^2-n) and the defect moment diverges"
        ),
        "fixed_insertion_owner_tail_does_not_supply_J_pair": (
            "each individual insertion/return record has finite boundary charge in the band model, but there is no decay in insertion time and the all-time sum diverges"
        ),
        "finite_marginal_Z_does_not_supply_J_cap": (
            "the Round52 interval-translation separator has both marginal survivor families proper with finite normalized Z, common mass 499/500, and common-refinement J_cap=infinity"
        ),
        "finite_absolute_continuous_Z_does_not_supply_strong_cemetery": (
            "the Round52 nested-tube separator allows a collision-null never-return set with full trace mass; strong singular/current cemetery therefore remains an independent theorem"
        ),
        "logical_scope": (
            "these are field-level nonimplications, not claims that the physical billiard realizes the abstract separators"
        ),
        "physical_J_pair_or_J_cap_disproved": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_SEPARATION_OF_D1_FIXED_TIME_OWNER_MARGINAL_Z_AND_STRONG_CEMETERY_FROM_THE_TWO_TARGET_Z_QUANTITIES",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": (
                "inherits every fixed |s|<=1/400 and full regular arbitrary-R_n scope where the pinned dependencies apply"
            ),
            "claim_type": (
                "exact same-measure cell-Z defect bridge, aggregate-Z cross-gate resolvent, conditional common-refinement properisation clock, and strict nonpromotion audit"
            ),
            "external_theorem_promoted": False,
        },
        "fractional_cell_Z_to_defect_moment": fractional_cell_z_bridge(),
        "aggregate_Z_cross_gate_bridge": aggregate_z_cross_gate_bridge(),
        "common_refinement_Z_to_proper_return_clock": common_refinement_z_bridge(),
        "two_Z_and_cemetery_nonimplication_audit": exact_nonimplication_audit(),
        "compressed_physical_frontier": {
            "cell_level_once_charge_retyping": "CERTIFIED_IN_ROUND52",
            "exact_Tm_from_J_pair": "CERTIFIED_CONDITIONAL_BRIDGE",
            "exact_I_D_from_J_pair": "CERTIFIED_CONDITIONAL_BRIDGE",
            "physical_J_pair": "NOT_CERTIFIED",
            "physical_I_D": "NOT_CERTIFIED",
            "aggregate_Z_l1_resolvent": "CERTIFIED_ABSTRACTLY",
            "round28_Qn_to_round36_mn_same_ID_normalization_join": "NOT_CERTIFIED",
            "all_time_physical_face_forcing_and_terminal_extraction": "NOT_CERTIFIED",
            "uniform_common_terminal_survivor_mass_gt_249_over_250": "CERTIFIED_IN_ROUND52",
            "common_refinement_Z_clock_bridge": "CERTIFIED_CONDITIONAL_BRIDGE",
            "physical_common_refinement_J_cap": "NOT_CERTIFIED",
            "proper_same_ID_physical_return": "NOT_CERTIFIED",
            "parent_charged_postclock_ambient_max_envelope_L6over5": "CERTIFIED_IN_ROUND52",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonpromotion": {
            "same_measure_cell_Z_to_defect_bridge": "CERTIFIED_CONDITIONAL_THEOREM",
            "abstract_aggregate_Z_l1_resolvent": "CERTIFIED",
            "common_refinement_Z_to_extra_clock_bridge": "CERTIFIED_CONDITIONAL_THEOREM",
            "physical_J_pair": "NOT_CERTIFIED",
            "physical_defect_moment_I_D": "NOT_CERTIFIED",
            "round28_Qn_to_round36_mn_same_ID_normalization_join": "NOT_CERTIFIED",
            "physical_all_time_face_tower_and_terminal_extraction": "NOT_CERTIFIED",
            "physical_common_refinement_J_cap": "NOT_CERTIFIED",
            "proper_same_ID_geometric_return": "NOT_CERTIFIED",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("CELL_Z_TO_DEFECT:", strict["same_measure_cell_Z_to_defect_bridge"])
    print("PHYSICAL_J_PAIR:", strict["physical_J_pair"])
    print("COMMON_REFINEMENT_Z_CLOCK:", strict["common_refinement_Z_to_extra_clock_bridge"])
    print("PROPER_SAME_ID_RETURN:", strict["proper_same_ID_geometric_return"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
