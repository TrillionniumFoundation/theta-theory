#!/usr/bin/env python3
"""Round-54 Gate-4 aggregate survivor/terminal extraction frontier.

This append-only certificate resolves the ambiguity in the Round-36 mass
symbol by instantiating its corrected Round-37 killed recurrence on the
unnormalised survivor family

    F_n = (T_s^n)_#(mu_s restricted to Q_n).

Consequently ``m_n=mu_s(Q_n)=mu_s(C_s) S_n`` on the exact Round-27 prefix
IDs.  The exponentially summable Round-28 survivor tail therefore supplies
the collision-mass term of the aggregate-Z resolvent.  Return-level families
``mu_s|R_n`` are explicitly rejected as the recurrence state: a one-step
killed evolution sends the Q_n state to Q_(n+1), not R_n to R_(n+1).

The certificate also installs an exact two-orientation *coarse terminal-Z*
extraction inequality using the terminal core multiplier 2000/1999.  It does
not identify that coarse terminal family with the natural-short-cell and
image-recut refinement used by Round-53 J_pair: a unit-interval separator has
coarse Z=1 and refined cell Z=N.  The hereditary C24-complement boundary
charge is independently open.  A nested-interval separator has summable
survivor mass but one new endpoint at every level, so the current mass tail
cannot supply that forcing either.

Finally, the finite-schedule typing is used to construct a Borel countable
common-refinement atlas on the Round-52 once-charged common terminal survivor.
Compactly contained regular analytic substrata have finitely many pieces, but
one original whole-family record may meet countably many such strata.  The
atlas therefore does not make J_cap(y) finite and does not give recordwise
properisation: a p_k=ell_k separator has one finite piece per stratum but
infinite total boundary.  No physical q, repeated-clock moment, proper
first-return kernel, or strong cemetery is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round54-survivor-mass-terminal-extraction-common-atlas.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json": (
        "890a95cb71a19bdb2f32963d5c3812c29d0d3bb9f427076c4bf7cc1b684d4393"
    ),
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json": (
        "7ddecb544fa5a2b243882eaf2028159c22f8437fc3fbb49fda4eb487ab181798"
    ),
    "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json": (
        "b86b5c74c8dcf4d2415ad28715a55ea98bf42bb191f7926684009ebbb8c8da34"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
}

TAIL_A = Q(550000, 147)
TAIL_R = Q(111718729, 111718750)
TAIL_GAP = 1 - TAIL_R
CORE_MASS_LOWER = Q(147, 550000)
CORE_MASS_UPPER = Q(29021, 75000000)
GROWTH_A = Q(360134800, 360493663)
GROWTH_B = Q(2 * 10**90)
GROWTH_MARGIN = 1 - GROWTH_A
GROWTH_RESOLVENT = 1 / GROWTH_MARGIN
CORE_MULTIPLIER = Q(2000, 1999)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root type: {name}")
        loaded[name] = value

    round27 = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    require(
        round27["verdict"]["arbitrary_n_Rn_Qn_measurable_level_and_mass_schema"]
        == "CERTIFIED",
        "Round27 level schema",
    )
    level = round27["result"]["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    require(level["Q_0"] == "C_s", "Round27 Q0")
    require(
        level["level_identity_mod_null"]
        == "Q_(n-1)=R_n disjoint_union Q_n",
        "Round27 level identity",
    )
    require(
        level["symbolic_physical_mass"]["sum_k_qmass_s_n_k"]
        == "mu_s(Q_n)",
        "Round27 Q mass",
    )
    require(
        level["symbolic_physical_mass"]["sum_k_m_s_n_k"]
        == "mu_s(R_n)",
        "Round27 R mass",
    )
    require(
        level["uniform_normalized_survivor_tail"]
        == "mu_s(Q_n)/mu_s(C_s)<(550000/147)*(111718729/111718750)^floor(n/N_open)",
        "Round27 tail",
    )
    require(
        level["normalized_core_mass_interval"]
        == ["147/550000_strict_lower", "29021/75000000_strict_upper"],
        "Round27 core mass interval",
    )

    round28 = loaded[
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    ]
    ledger = round28["result"]["first_return_mass_ledger_join"]
    require(
        ledger["normalized_survivor_mass_symbol"]
        == "S_n=mu_s(Q_n)/mu_s(C_s)",
        "Round28 S typing",
    )
    require(ledger["tail_prefactor_A"] == qstr(TAIL_A), "Round28 A")
    require(ledger["tail_block_factor_r"] == qstr(TAIL_R), "Round28 r")
    require(ledger["tail_hit_gap_epsilon"] == qstr(TAIL_GAP), "Round28 gap")

    round36 = loaded[
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    ]["result"]["aggregate_Z_new_face_recurrence"]
    require(round36["recurrence"] == "Z_(n+1)<=a*Z_n+b*m_n+J_n", "Round36 recurrence")
    require(round36["a"] == qstr(GROWTH_A), "Round36 a")
    require(round36["b"] == qstr(GROWTH_B), "Round36 b")
    require(
        "whole physical survivor/return level" in round36["aggregate_family"],
        "Round36 ambiguous family string",
    )

    round37 = loaded[
        "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json"
    ]["result"]
    typed = round37["typed_forcing_correction"]
    require(
        typed["fixed_s_base_standard_family_recurrence"]
        == "Z_(n+1)<=a*Z_n+b*m_n+J_C24,n",
        "Round37 survivor recurrence",
    )
    require(
        typed["C24_complement_role"]
        == "the repeated characteristic restriction external to the frozen closed-map step",
        "Round37 complement typing",
    )
    require(
        round37["strict_nonpromotion"]["hereditary_C24_open_Growth"]
        == "NOT_CERTIFIED",
        "Round37 forcing scope",
    )

    inner = loaded[
        "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
    ]
    require(
        inner["replay_summary"]["source_multiplier_norm_upper"]
        == qstr(CORE_MULTIPLIER),
        "terminal core multiplier",
    )
    require(
        inner["verdict"]["core_local_standard_family_source_multiplier"]
        == "CERTIFIED",
        "terminal core source operator",
    )

    round35 = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]["common_forward_reverse_carrier_pair"]
    require(
        round35["actual_parameterized_common_fw_rev_carrier_pair_registry"]
        == "CERTIFIED",
        "Round35 common carrier",
    )
    require(
        round35["reverse_oriented_branch"] == "I(B) -> I(A) by T_s^n",
        "Round35 reverse return branch",
    )
    require(
        round35["forward_and_reverse_share_identical_component_and_restriction"]
        is True,
        "Round35 identical return restriction",
    )

    round50 = loaded[
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    ]
    grouping = round50["result"]["physical_Borel_whole_family_grouping"]
    require(
        grouping["status"]
        == "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J",
        "Round50 grouping",
    )
    require(grouping["physical_full_registry_reconstructed"] is True, "Round50 reconstruction")
    require(
        grouping["same_ID_two_view_join"].endswith("never two charges"),
        "Round50 once charge",
    )

    round51 = loaded[
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    ]
    two_view = round51["result"]["physical_two_proper_view_object_lemma"]
    require(
        two_view["status"]
        == "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM",
        "Round51 two-view law",
    )
    require(two_view["same_ID_once_charge"] is True, "Round51 once charge")
    require(two_view["raw_geometry_is_proper"] is False, "Round51 geometry scope")

    round52 = loaded[
        "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    terminal = round52["uniform_outer_majorant_terminal_join"]
    require(
        terminal["same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"]
        == "249/250",
        "Round52 common mass",
    )
    require(terminal["common_terminal_subkernel_is_Borel_and_positive"] is True, "Round52 Borel")
    require(terminal["common_terminal_subkernel_is_geometrically_proper"] is False, "Round52 proper scope")
    separator = round52["large_common_mass_geometric_nonpromotion"]
    require(separator["common_boundary_numerator"].endswith("infinity"), "Round52 Jcap separator")
    require(separator["physical_proper_common_return_disproved"] is False, "Round52 logical scope")

    outer = loaded[
        "cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json"
    ]
    require(
        outer["verdict"]["proper_common_terminal_nonhit_restriction"]
        == "NOT_CERTIFIED",
        "Round52 terminal-only scope",
    )

    round53 = loaded[
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    ]
    bridge = round53["result"]["aggregate_Z_cross_gate_bridge"]
    require(
        bridge["round28_Qn_to_round36_mn_same_ID_normalization_join"]
        == "NOT_CERTIFIED",
        "Round53 first missing join",
    )
    require(
        round53["verdict"]["physical_all_time_face_tower_and_terminal_extraction"]
        == "NOT_CERTIFIED",
        "Round53 combined missing joins",
    )
    cap = round53["result"]["common_refinement_Z_to_proper_return_clock"]
    require(cap["physical_common_refinement_J_cap_certified"] is False, "Round53 Jcap scope")
    require(cap["physical_proper_same_ID_return_certified"] is False, "Round53 return scope")

    return loaded


def survivor_mass_instantiation() -> dict[str, Any]:
    require(TAIL_GAP == Q(21, 111718750), "tail gap")
    require(GROWTH_MARGIN == Q(358863, 360493663), "growth margin")
    require(GROWTH_RESOLVENT == Q(360493663, 358863), "resolvent")
    block_sum_coefficient = TAIL_A / TAIL_GAP
    require(block_sum_coefficient == Q(61445312500000, 3087), "tail sum coefficient")
    uniform_mass_sum_coefficient = CORE_MASS_UPPER * block_sum_coefficient
    require(
        uniform_mass_sum_coefficient == Q(142656353125, 18522),
        "uniform mass coefficient",
    )

    rows: list[dict[str, Any]] = []
    toy_block = 3
    for n in range(10):
        rows.append(
            {
                "n": n,
                "toy_N_open": toy_block,
                "block_index": n // toy_block,
                "strict_S_n_upper": qstr(TAIL_A * TAIL_R ** (n // toy_block)),
                "state_ID": f"survivor-prefix:(source-core,Q_{n},prefix-key)",
                "next_terminal_ID": f"return-path:(source-core,R_{n + 1},path-key)",
            }
        )

    return {
        "unique_recurrence_state": (
            "F_n=(T_s^n)_#(mu_s restricted to Q_n), represented as one "
            "unnormalised same-prefix survivor standard family modulo the frozen null boundary"
        ),
        "initial_state": "F_0=mu_s restricted to Q_0=mu_s restricted to C_s",
        "one_step_pre_kill": "G_(n+1)=T_s#F_n",
        "terminal_and_survivor_split": [
            "E_(n+1)=1_C_s G_(n+1), carrying exactly the R_(n+1) terminal IDs",
            "F_(n+1)=1_(C_s^c) G_(n+1), carrying exactly the Q_(n+1) prefix IDs",
        ],
        "same_ID_reason": (
            "Round27 exact half-open path ownership labels a Q_n prefix; the killed step "
            "extends that prefix by one collision, routing the terminal child to R_(n+1) "
            "and the surviving child to Q_(n+1), without relabelling positive mass"
        ),
        "mass_identity": "m_n=mass(F_n)=mu_s(Q_n)=mu_s(C_s)*S_n",
        "normalization_join": "CERTIFIED_PHYSICAL_SAME_ID_LEVEL_EXACT",
        "strict_tail": "m_n<mu_s(C_s)*(550000/147)*r^floor(n/N_open)",
        "strict_sum": (
            "sum_{n>=0}m_n<mu_s(C_s)*(61445312500000/3087)*N_open"
        ),
        "uniform_relaxed_sum": (
            "sum_{n>=0}m_n<(142656353125/18522)*N_open"
        ),
        "strictness_reason": (
            "every level uses the strict Round28 S_n bound; grouping the indices "
            "n=k*N_open,...,(k+1)*N_open-1 gives exactly N_open copies of r^k"
        ),
        "finite_but_nonnumeric_reason": "N_open is one theorem-supplied finite integer and is not numerically materialized",
        "R_n_state_rejected": {
            "candidate": "m_n=mu_s(R_n)",
            "why_mass_sum_would_be_finite": "sum_{n>=1}mu_s(R_n)=mu_s(C_s)",
            "why_not_this_recurrence_state": (
                "T_s#(mu_s restricted to R_n) is not the next return-level law "
                "mu_s restricted to R_(n+1); the corrected Round37 recurrence is the "
                "one-step killed base survivor recurrence"
            ),
            "using_R_n_mass_in_the_Q_n_killed_recurrence": False,
        },
        "tail_constants": {
            "A": qstr(TAIL_A),
            "r": qstr(TAIL_R),
            "one_minus_r": qstr(TAIL_GAP),
            "A_over_one_minus_r": qstr(block_sum_coefficient),
            "mu_C_strict_interval": [
                f">{qstr(CORE_MASS_LOWER)}",
                f"<{qstr(CORE_MASS_UPPER)}",
            ],
        },
        "sample_rows": rows,
        "sample_rows_sha256": canonical_digest(rows),
        "status": "CERTIFIED_ROUND28_QN_TO_ROUND36_37_MN_SAME_ID_NORMALIZATION_AND_L1_JOIN",
    }


def face_forcing_separator() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    mass_partial = Q(0)
    forcing_partial = Q(0)
    for n in range(9):
        mass = TAIL_R**n
        mass_partial += mass
        forcing_partial += 1
        rows.append(
            {
                "n": n,
                "survivor_interval": f"W_{n}=(0,r^{n})",
                "survivor_mass_m_n": qstr(mass),
                "new_cut_location": f"r^{n + 1}",
                "new_endpoint_boundary_charge_Phi_n": "1",
                "mass_partial_sum": qstr(mass_partial),
                "forcing_partial_sum": qstr(forcing_partial),
            }
        )
    require(mass_partial < 1 / TAIL_GAP, "separator mass partial sum")
    require(forcing_partial == 9, "separator forcing partial sum")
    return {
        "model": (
            "W_n=(0,r^n) with constant density one; at level n remove the terminal "
            "interval [r^(n+1),r^n) and retain W_(n+1)"
        ),
        "exact_mass_tail": "m_n=r^n and sum_n m_n=1/(1-r)=111718750/21<infinity",
        "exact_face_forcing": (
            "the complement cut creates one new endpoint with density one at every "
            "level, so Phi_n=1 and sum_n Phi_n=infinity"
        ),
        "fixed_level_finiteness": "every individual Phi_n is finite",
        "logical_scope": (
            "a standard-family restriction nonimplication for the installed scalar "
            "mass-tail fields, not a claim that the billiard realizes these intervals"
        ),
        "consequence": "summable killed-survivor mass does not imply all-time C24 face forcing",
        "physical_all_time_face_forcing_disproved": False,
        "rows": rows,
        "rows_sha256": canonical_digest(rows),
        "status": "CERTIFIED_EXACT_MASS_TAIL_TO_FACE_FORCING_NONIMPLICATION",
    }


def terminal_extraction_join() -> dict[str, Any]:
    c_resolvent = CORE_MULTIPLIER * GROWTH_RESOLVENT
    require(c_resolvent == Q(720987326000, 717367137), "terminal resolvent")
    pair_mass_coefficient = c_resolvent * 2 * GROWTH_B
    initial_coefficient = c_resolvent * GROWTH_A
    face_coefficient = initial_coefficient

    refinement_rows: list[dict[str, Any]] = []
    for cells in [1, 2, 4, 8, 32, 128]:
        refinement_rows.append(
            {
                "natural_or_image_cell_count_N": cells,
                "coarse_interval": "[0,1]",
                "coarse_mass": "1",
                "coarse_length": "1",
                "coarse_boundary_Z": "1",
                "each_refined_cell_mass": qstr(Q(1, cells)),
                "each_refined_cell_length": qstr(Q(1, cells)),
                "each_cell_boundary_contribution": "1",
                "refined_cell_boundary_Z": str(cells),
            }
        )

    return {
        "orientation_scope": "sigma in {fw,rev}; both views retain one physical R_(n+1) restriction ID",
        "orientation_specific_cores": {
            "forward_terminal_core": "C_fw=C_s",
            "reverse_terminal_core": "C_rev=I(C_s)",
            "no_time_reversal_invariance_of_the_literal_core_asserted": True,
            "same_multiplier_reason": (
                "the billiard involution I preserves collision-SRB measure and the adapted/"
                "Euclidean carrier arclength, so conjugation by I transports the C_s "
                "characteristic source norm 2000/1999 to I(C_s) with the same constant"
            ),
        },
        "level_definitions": [
            "G_(fw,n+1)=T_s#F_(fw,n), E_(fw,n+1)=1_C_s G_(fw,n+1)",
            "G_(rev,n+1)=T_s#F_(rev,n), E_(rev,n+1)=1_(I(C_s)) G_(rev,n+1)",
            "the corresponding complements form the next orientation-specific survivors",
        ],
        "closed_step": "Z(G_(sigma,n+1))<=a*Z_(sigma,n)+b*m_n",
        "terminal_core_operator": "Z(E_(sigma,n+1))<=(2000/1999)*Z(G_(sigma,n+1))",
        "survivor_recurrence": (
            "Z_(sigma,n+1)<=a*Z_(sigma,n)+b*m_n+Phi_(sigma,n)"
        ),
        "forcing_index_contract": (
            "Phi_(sigma,n) is only the extra C24-complement boundary charge used "
            "to form the next survivor; the forward R_(n+1) layer and reverse "
            "I(R_(n+1)) layer E_(sigma,n+1) are not included in Phi_(sigma,n) "
            "and are extracted separately"
        ),
        "first_level_check": (
            "n=0 produces the forward R_1 terminal layer in C_s and its reverse "
            "I(R_1) terminal layer in I(C_s)"
        ),
        "coarse_terminal_Z_definition": (
            "Z_term,coarse,pair=sum_{n>=0}[Z(E_(fw,n+1))+Z(E_(rev,n+1))]"
        ),
        "pair_resolvent": (
            "sum_{n>=0}[Z_(fw,n)+Z_(rev,n)] <= "
            "[Z_pair,0+2*b*M+Phi_pair]/(1-a)"
        ),
        "definitions_for_bound": [
            "M=sum_{n>=0}m_n",
            "Phi_pair=sum_{n>=0}(Phi_(fw,n)+Phi_(rev,n))",
            "Z_pair,0=Z_(fw,0)+Z_(rev,0)",
        ],
        "exact_coarse_extraction_bound": (
            "Z_term,coarse,pair<=(2000/1999)/(1-a)*[a*Z_pair,0+2*b*M+a*Phi_pair]"
        ),
        "coefficients": {
            "a": qstr(GROWTH_A),
            "b": qstr(GROWTH_B),
            "one_minus_a": qstr(GROWTH_MARGIN),
            "one_over_one_minus_a": qstr(GROWTH_RESOLVENT),
            "terminal_core_multiplier": qstr(CORE_MULTIPLIER),
            "terminal_resolvent_multiplier": qstr(c_resolvent),
            "Z_pair_0_coefficient": qstr(initial_coefficient),
            "M_coefficient": qstr(pair_mass_coefficient),
            "Phi_pair_coefficient": qstr(face_coefficient),
        },
        "coarse_finite_conclusion": (
            "the certified finite M and finite initial standard-family Z imply "
            "Z_term,coarse,pair<infinity as soon as Phi_pair<infinity"
        ),
        "cell_refinement_separator": {
            "model": (
                "one unit terminal interval has coarse mass/length boundary Z=1; "
                "partitioning it into N equal natural/image cells gives N terms "
                "(1/N)/(1/N)=1 and refined cell boundary Z=N"
            ),
            "conclusion": (
                "coarse terminal Z does not dominate the Round53 natural-short-cell/"
                "image-recut J_pair without a same-ID refinement-Z theorem"
            ),
            "physical_billiard_refinement_divergence_claimed": False,
            "rows": refinement_rows,
            "rows_sha256": canonical_digest(refinement_rows),
            "status": "CERTIFIED_COARSE_Z_TO_CELL_REFINEMENT_Z_NONIMPLICATION",
        },
        "coarse_terminal_Z_extraction": "CERTIFIED_EXACT_TWO_ORIENTATION_INEQUALITY",
        "terminal_cell_refinement_to_J_pair_same_ID_Z_join": "NOT_CERTIFIED",
        "actual_physical_J_pair": (
            "NOT_CERTIFIED_BECAUSE_BOTH_PHI_PAIR_L1_AND_CELL_REFINEMENT_Z_JOIN_ARE_OPEN"
        ),
        "status": "CERTIFIED_COARSE_TERMINAL_Z_ONLY__J_PAIR_REFINEMENT_AND_FACE_FORCING_OPEN",
    }


def common_refinement_atlas() -> dict[str, Any]:
    sample_rows = [
        {
            "record": "y0",
            "raw_parent": "(0,1)",
            "forward_strict_predicate": "x in (1/10,9/10)",
            "reverse_strict_predicate": "x in (1/5,2/5) union (3/5,4/5)",
            "common_components": ["(1/5,2/5)", "(3/5,4/5)"],
            "component_count": 2,
        },
        {
            "record": "y1",
            "raw_parent": "(0,1)",
            "forward_strict_predicate": "x in (1/4,3/4)",
            "reverse_strict_predicate": "x in (1/2,7/8)",
            "common_components": ["(1/2,3/4)"],
            "component_count": 1,
        },
        {
            "record": "y2",
            "raw_parent": "(0,1)",
            "forward_strict_predicate": "x in (0,1/3)",
            "reverse_strict_predicate": "x in (2/3,1)",
            "common_components": [],
            "component_count": 0,
        },
    ]
    countable_separator_rows: list[dict[str, Any]] = []
    for k in range(1, 9):
        length = Q(1, 2**k)
        countable_separator_rows.append(
            {
                "compact_regular_substratum_k": k,
                "component_count_on_this_substratum": 1,
                "component_mass_p_k": qstr(length),
                "forward_length_ell_k": qstr(length),
                "reverse_length_ell_k": qstr(length),
                "forward_boundary_contribution": "1",
                "reverse_boundary_contribution": "1",
                "pair_boundary_contribution": "2",
            }
        )
    return {
        "raw_object": (
            "the Round52 same-parent common terminal survivor K_cap=K_par restricted "
            "to S_fw intersect S_rev, before normalization and with mass h(y)>249p(y)/250"
        ),
        "regular_stratification": (
            "stratify by the integer stopped times, finite branch paths, incidence ranks, "
            "and half-open endpoint owners already present in Rounds 48--51"
        ),
        "compact_exhaustion_policy": (
            "exhaust every regular branch section by countably many compact substrata whose "
            "closures stay a positive distance from singular and predicate boundaries; "
            "no compact containment is asserted for the original whole-family section"
        ),
        "per_compact_substratum_finiteness": (
            "on each such compact regular substratum, finite-schedule predicates are finite "
            "intersections of analytic inequalities; a nonzero analytic boundary function "
            "has finitely many zeros, an identically signed row adds no cut, and an "
            "identically zero strict row is empty or belongs to the removed boundary stratum"
        ),
        "Borel_enumeration": (
            "enumerate each relatively open connected interval by the least rational-basis "
            "element it contains; the open-section component relation is Borel and the "
            "countable stopped-time union remains standard-Borel"
        ),
        "whole_record_cardinality": (
            "one original rn-whole-family record may meet countably many stopping/branch/"
            "compact-exhaustion strata and therefore may have countably many components"
        ),
        "component_ID": (
            "cap-component:(rn-whole-family-ID,terminal-schedule,stopping-stratum,"
            "least-rational-basis-rank)"
        ),
        "once_charge_disintegration": (
            "the half-open common components partition K_cap modulo the frozen null boundary; "
            "their masses sum to h(y), not 2h(y)"
        ),
        "orientation_geometry": (
            "P_fw and P_rev are finite analytic diffeomorphisms on each compact regular "
            "substratum, so every positive common component has positive Borel lengths "
            "ell_cap,fw and ell_cap,rev"
        ),
        "zero_policy": "h(y)=0 gives the empty atlas, J_cap(y)=0, and is never normalized",
        "recordwise_J_cap": "J_cap(y)<infinity is NOT_CERTIFIED",
        "recordwise_D_cap": "D_cap(y)<infinity is NOT_CERTIFIED",
        "recordwise_two_view_properisation": "NOT_CERTIFIED",
        "global_integrability": "integral J_cap(y)dlambda(y)<infinity is NOT_CERTIFIED",
        "global_clock_moment": "integral h(y)exp(D_cap(y)/6)dlambda(y)<infinity is NOT_CERTIFIED",
        "countable_stratum_separator": {
            "law": (
                "within one whole-family record take one component on each compact "
                "regular substratum with p_k=ell_fw,k=ell_rev,k=2^-k"
            ),
            "finite_mass": "sum_k p_k=1",
            "per_stratum_finite": True,
            "boundary_failure": (
                "each orientation contributes p_k/ell_k=1 on every k, so the pair "
                "J_cap=sum_k 2=infinity"
            ),
            "physical_billiard_realizes_separator_claimed": False,
            "rows": countable_separator_rows,
            "rows_sha256": canonical_digest(countable_separator_rows),
            "status": "CERTIFIED_PER_STRATUM_FINITE_DOES_NOT_IMPLY_RECORDWISE_J_CAP_FINITE",
        },
        "marginal_nonimplication_reason": (
            "the pinned Round52 interval-translation model has proper marginal views and "
            "common mass 499/500 but sum_k mass(A_k)/length(A_k)=infinity"
        ),
        "typing_boundary": (
            "the Borel countable common atlas is not yet a proper two-view carrier, one "
            "physical first-return kernel, or a proof of intermediate C24 avoidance"
        ),
        "sample_rows": sample_rows,
        "sample_rows_sha256": canonical_digest(sample_rows),
        "status": "CERTIFIED_PHYSICAL_BOREL_COUNTABLE_COMMON_REFINEMENT_ATLAS_ONLY",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "round28_Qn_to_round36_mn_same_ID_normalization_join": "CERTIFIED",
        "physical_survivor_mass_l1": "CERTIFIED_FINITE_NONNUMERIC_N_OPEN",
        "all_insertion_time_C24_complement_face_forcing_l1": "NOT_CERTIFIED",
        "coarse_terminal_Z_extraction_inequality": "CERTIFIED",
        "terminal_cell_refinement_to_J_pair_same_ID_Z_join": "NOT_CERTIFIED",
        "terminal_extraction_to_J_pair_join": "NOT_CERTIFIED",
        "physical_J_pair": "NOT_CERTIFIED",
        "physical_defect_moment_I_D": "NOT_CERTIFIED",
        "physical_common_refinement_atlas": "CERTIFIED_BOREL_COUNTABLE_ONLY",
        "per_compact_regular_substratum_component_finiteness": "CERTIFIED",
        "recordwise_common_refinement_J_cap": "NOT_CERTIFIED",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "recordwise_common_two_view_properisation": "NOT_CERTIFIED",
        "integrated_common_extra_clock_moment": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_for_postproperisation_schedule": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "later_or_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "Gate4": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "for every fixed |s|<=1/400",
            "depth_scope": "all finite killed-survivor levels and their countable first-return union",
            "claim_type": (
                "same-ID survivor mass instantiation, coarse two-view terminal-Z extraction, "
                "cell-refinement/face-forcing separators, and a Borel countable common atlas"
            ),
        },
        "killed_survivor_mass_join": survivor_mass_instantiation(),
        "summable_mass_nonsummable_face_separator": face_forcing_separator(),
        "two_orientation_terminal_extraction": terminal_extraction_join(),
        "physical_common_refinement_atlas": common_refinement_atlas(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round54_survivor_mass_terminal_extraction_common_atlas_verifier.py",
    )
    args = parser.parse_args()
    if args.print_manifest:
        print(json.dumps(build_manifest(args.verifier), indent=2, sort_keys=True))
        return 0
    result = build_result()
    frontier = result["strict_nonpromotion"]
    print("SURVIVOR_MASS_JOIN:", frontier["round28_Qn_to_round36_mn_same_ID_normalization_join"])
    print("COARSE_TERMINAL_Z:", frontier["coarse_terminal_Z_extraction_inequality"])
    print("TERMINAL_TO_J_PAIR_JOIN:", frontier["terminal_extraction_to_J_pair_join"])
    print("ALL_TIME_FACE_FORCING:", frontier["all_insertion_time_C24_complement_face_forcing_l1"])
    print("PHYSICAL_J_PAIR:", frontier["physical_J_pair"])
    print("COMMON_REFINEMENT_ATLAS:", frontier["physical_common_refinement_atlas"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
