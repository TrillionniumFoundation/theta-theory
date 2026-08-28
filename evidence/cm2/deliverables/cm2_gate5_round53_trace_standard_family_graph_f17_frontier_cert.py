#!/usr/bin/env python3
"""Round-53 Gate-5 trace/standard-family and graph-current frontier.

This append-only certificate keeps the physical scope at the base parameter
``s=0`` and the owner scope at one fixed insertion time ``j`` with registered
terminal depths ``n>j``.  It sharpens three interfaces left open in Round 52.

First, the owner face law obtained by selecting one transverse root on each
parent curve is not an unstable standard-family law.  An exact foliated-square
separator prevents direct reuse of collision-volume/standard-family Growth.

Second, trace-nullity of the never-return set is necessary but is not enough
for an exponentially weighted face tower.  A nested trace-null model has only
polynomial trace survival.  The exact conditional closure condition is
``w*delta**(1-1/q)<1`` on one common same-ID trace-survivor law.  At the frozen
Round-42 weight and ``delta=rho``, the critical exponent is just above two,
whereas the available ``4^-b`` incidence tail has critical moment exactly two.

Third, the physical source-side graph-current injection is installed with
constant one in the dual Lipschitz norm.  Piola preserves the boundary-trace
TV part but not the bulk vector part.  A determinant-one diagonal separator
shows that area preservation alone gives no finite common suffix multiplier.
No complete F10/F17/strong-F13 field or Gate-3 MT_DQ lift is promoted.
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
RESULT_SCHEMA = "cm2.gate5.round53-trace-standard-family-graph-f17-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": (
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b"
    ),
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": (
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46"
    ),
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": (
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16"
    ),
    "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json": (
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json": (
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c"
    ),
    "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json": (
        "1c4437a3c237739bacb823f0a9309626bea06b6f6562c1e268d589ed7debb7c5"
    ),
}

B0 = 14
COAREA_MASS = Q(8064, 5)
RANK_TAIL_COEFFICIENT = Q(9158592, 6875)
SURVIVAL_R = Q(111718729, 111718750)
BLOCK_DEPTH = 9148


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

    r52 = loaded[
        "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json"
    ]["result"]
    fixed = r52["fixed_insertion_same_ID_owner_tail_transfer"]
    if fixed["transfer_constant"] != "1" or "n>j" not in fixed["fixed_index"]:
        raise RuntimeError("Round52 fixed-j scope")
    if fixed["target_Borel_set_domination_after_distinct_suffixes"] is not False:
        raise RuntimeError("Round52 target-set boundary")
    if fixed["transferred_rank_tail"] != (
        "sum_a m_(j,a)^owner{B>b}<=(9158592/6875)*4^(-b), b>=14"
    ):
        raise RuntimeError("Round52 transferred rank tail")
    interpolation52 = r52["fixed_weight_Lq_interpolation_audit"]
    if interpolation52["available_raw_moment_range"] != (
        "q<2; q=3/2 is explicitly certified"
    ):
        raise RuntimeError("Round52 q=3/2 moment scope")
    if r52["strict_nonpromotion"]["trace_nullity_of_never_return_cemetery"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round52 trace frontier")

    r50 = loaded[
        "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    owner = r50["global_owner_aware_boundary_ZB_kernel"]
    if owner["active_regular_root_section"] != (
        "the Borel graph of the unique transverse rank-0 root on the parent W"
    ):
        raise RuntimeError("Round50 transverse root")
    if "time j<n" not in owner["global_index_space"]:
        raise RuntimeError("Round50 owner time scope")

    r39 = loaded[
        "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
    ]["result"]
    seed39 = r39["physical_rank_L3over2_derivation"]
    if seed39["rank_tail"] != (
        "m{B>b}<=(9158592/6875)*4^(-b) for every integer b>=14"
    ):
        raise RuntimeError("Round39 tail")

    r43 = loaded[
        "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
    ]["result"]
    bulk = r43["arbitrary_path_Duhamel_current"]
    if bulk["one_step_derivative"] != (
        "partial_s P_j,s h=-div_mu(X_j,s*P_j,s h)=-X_j,s dot grad(P_j,s h)"
    ):
        raise RuntimeError("Round43 bulk current")

    r44 = loaded[
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    ]["result"]
    suffix = r44["occurrence_suffix_two_trace_transport"]["suffix_transport"]
    if suffix["suffix_positive_pushforward_mass_constant"] != "1":
        raise RuntimeError("Round44 trace pushforward")

    block = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]["aggregate_canonical_Z_resolvent"]
    if block["mass_factor_rho"] != "(111718729/111718750)^9148":
        raise RuntimeError("Round42 rho")
    if block["explicit_block_index_weight"] != "w_Z=(1+rho^(-1))/2":
        raise RuntimeError("Round42 weight")

    g3 = loaded[
        "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json"
    ]["result"]
    if g3["common_free_carrier"]["common_free_graph_current_carrier"] != (
        "CERTIFIED"
    ):
        raise RuntimeError("Gate3 free carrier")
    if g3["common_free_carrier"]["total_fixed_slot_count"] != 41508:
        raise RuntimeError("Gate3 fixed slot count")
    if g3["physical_bridge_frontier"]["bounded_physical_lift_quotient_pair"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Gate3 lift boundary")

    r51 = loaded[
        "cm2-gate5-round51-face-sparse-zb-dynamic-envelope-frontier-manifest-2026-07-20.json"
    ]["result"]
    envelope = r51["common_dynamic_suffix_envelope"]
    if envelope["common_envelope_suffix_multiplier"] != "C_dyn=1":
        raise RuntimeError("Round51 envelope")
    if envelope["F17_dynamic_test_operator_cost"] != "NOT_CERTIFIED":
        raise RuntimeError("Round51 F17 boundary")
    return loaded


def transverse_trace_standard_family_audit() -> dict[str, Any]:
    rows = []
    for exponent in (0, 2, 6, 10):
        epsilon = Q(1, 1 << exponent)
        rows.append(
            {
                "epsilon": qstr(epsilon),
                "trace_mass_of_A_epsilon": "1",
                "uniform_proper_family_mass_of_A_epsilon": qstr(epsilon),
                "trace_to_family_mass_ratio": str(1 << exponent),
            }
        )
    return {
        "typed_owner_law": (
            "one transverse connected-rank-0 root xi(W) on each parent W, "
            "then integrate the root atom against the outer parent law lambda(W)"
        ),
        "separator_space": "X=[0,1]^2 with horizontal unstable parents W_y=[0,1]x{y}",
        "parent_law": "lambda=dy on y in [0,1]",
        "physical_face": "Gamma={0}x[0,1]",
        "root_section": "xi(W_y)=(0,y)",
        "owner_trace": "nu(A)=integral 1_A(xi(W_y))dy=H^1|Gamma(A)",
        "uniform_proper_family": (
            "sigma(A)=integral_y integral_(W_y) 1_A(x,y) dx dy; more generally "
            "proper leaf densities are non-atomic along W_y"
        ),
        "singular_set_test": "nu(Gamma)=1 while sigma(Gamma)=0",
        "tube_test": "A_epsilon=[0,epsilon]x[0,1]",
        "rows": rows,
        "rows_sha256": digest(rows),
        "finite_positive_domination_nu_by_sigma": False,
        "direct_Round42_collision_or_proper_family_minorisation_transfer": False,
        "owner_trace_is_an_unstable_standard_family_law": False,
        "logical_scope": (
            "measure-type separator only; it does not rule out a billiard-specific "
            "trace extension, transverse holonomy theorem or direct trace contraction"
        ),
        "minimal_missing_bridge": (
            "a same-ID trace-to-uniformly-proper-family extension with quantitative "
            "loss and survivor compatibility, or a direct quantitative contraction "
            "proved on the transverse owner-trace law itself"
        ),
        "conditional_unit_loss_bridge": {
            "trace_extension": (
                "E maps each same-ID owner trace law into the Round42 proper-family class"
            ),
            "trace_recovery": "Tr maps the extended law back to the same owner trace ID",
            "recovery_identity": "Tr composed E = Id on the owner trace laws",
            "positive_operator_norms": "norm(E)<=1 and norm(Tr)<=1",
            "killed_block_survivor_intertwining": (
                "K_trace=Tr composed K_proper composed E"
            ),
            "zero_extension_or_recovery_is_excluded": True,
            "conditional_conclusion": "kappa_trace<=rho<2rho/(1+rho)",
        },
        "conditional_unit_loss_bridge_is_installed": False,
        "status": "CERTIFIED_TRANSVERSE_TRACE_NOT_PROPER_STANDARD_FAMILY_SEPARATOR",
    }


def trace_nullity_and_weighted_closure_audit() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    w_z = (1 + 1 / rho) / 2
    kappa = 1 / w_z
    if not Q(1) < w_z < 1 / rho:
        raise RuntimeError("aggregate weight")
    rows = []
    for p in (0, 1, 4, 16):
        trace_mass = Q(1, p + 1)
        rows.append(
            {
                "block_index": p,
                "collision_survivor_mass": (
                    "1" if p == 0 else f"rho^{p}/{p + 1}"
                ),
                "trace_survivor_mass": qstr(trace_mass),
                "constant_rank": B0,
                "owner_charge": qstr((1 << B0) * trace_mass),
            }
        )
    if not rho > kappa**3:
        raise RuntimeError("q=3/2 fixed-weight obstruction")
    if not (1 + rho) ** 3 < 8 * rho:
        raise RuntimeError("q=3 fixed-weight safe point")
    with localcontext() as ctx:
        ctx.prec = 80
        drho = (Decimal(SURVIVAL_R.numerator) / Decimal(SURVIVAL_R.denominator)) ** BLOCK_DEPTH
        dkappa = 2 * drho / (1 + drho)
        critical = Decimal(1) / (Decimal(1) - dkappa.ln() / drho.ln())
        critical_decimal = format(critical, ".34f")
    return {
        "trace_nullity_separator": {
            "space": "X=[0,1]^2, mu=dx*dy, Gamma={0}x[0,1], nu=H^1|Gamma",
            "nested_survivors": "Q_p=[0,rho^p]x[0,1/(p+1)]",
            "collision_mass": "mu(Q_p)=rho^p/(p+1)<=rho^p",
            "trace_mass": "nu(Q_p)=1/(p+1)",
            "never_return_set": "intersection_p Q_p={(0,0)}",
            "collision_and_trace_nullity": "mu(intersection Q_p)=nu(intersection Q_p)=0",
            "rank": "B=14 on Gamma",
            "owner_charge": "b_p=2^14/(p+1)",
            "ordinary_forcing_majorant": "z_p=m_p=rho^p",
            "weighted_forcing": "sum_p w_Z^p*rho^p<infinity",
            "weighted_owner_charge": (
                "sum_p w_Z^p*2^14/(p+1)=infinity because its terms do not tend to zero"
            ),
            "recurrence_conclusion": (
                "for every fixed kappa<1 and finite A,C, b_(p+1)<=kappa*b_p+"
                "A*rho^p+C*rho^p eventually fails"
            ),
            "rows": rows,
            "rows_sha256": digest(rows),
            "trace_nullity_alone_implies_exponentially_weighted_face_tower": False,
            "status": "CERTIFIED_TRACE_NULLITY_WITHOUT_EXPONENTIAL_TOWER_SEPARATOR",
        },
        "sharp_conditional_holder_closure": {
            "required_common_measure_typing": (
                "one finite same-ID source trace law nu_0, nested survivor restrictions "
                "nu_p=1_(Q_p)*nu_0, and one retained rank mark g=2^B"
            ),
            "hypotheses": (
                "nu_0(Q_p)<=C_tr*delta^p and ||g||_(L^q(nu_0))<=M_q, q>1"
            ),
            "holder_bound": (
                "b_p=integral_(Q_p)g dnu_0<=M_q*C_tr^(1-1/q)*"
                "delta^(p*(1-1/q))"
            ),
            "weighted_sum_criterion": "w*delta^(1-1/q)<1",
            "fixed_weight": "w_Z=(1+rho^(-1))/2",
            "fixed_weight_factor": "kappa_*=1/w_Z=2rho/(1+rho)",
            "if_delta_equals_rho_critical_q_formula": (
                "q_*=1/(1-log(kappa_*)/log(rho))"
            ),
            "if_delta_equals_rho_critical_q_decimal": critical_decimal,
            "q_equals_two_fails_exactly": (
                "kappa_*<sqrt(rho), directly equivalent to (1-sqrt(rho))^2>0; "
                "after squaring, equivalent to (1-rho)^2>0"
            ),
            "q_equals_three_is_safe": (
                "rho^(2/3)<kappa_*; equivalently (1+rho)^3<8rho, true for this rho"
            ),
            "q_equals_three_halves_fixed_weight_delta_threshold": (
                "delta<kappa_*^3=(2rho/(1+rho))^3"
            ),
            "delta_equals_rho_fails_q_three_halves": True,
            "kappa_fraction_binary_sha256": fraction_digest(kappa),
            "weaker_weight_for_q_three_halves_delta_rho": (
                "w_face=(1+rho^(-1/3))/2; then w_face*rho^(1/3)="
                "(1+rho^(1/3))/2<1 and w_face*rho<1"
            ),
            "weaker_weight_route_is_unconditional": False,
            "critical_equality_shell_extremizer": {
                "shells": (
                    "Q_p=disjoint_union_(r>=p)S_r with nu_0(S_r)="
                    "(1-delta)*delta^r, hence nu_0(Q_p)=delta^p"
                ),
                "mark": (
                    "g|S_r=delta^(-r/q)/(r+1)^a, a=(q+1)/(2q), "
                    "and g_tilde=2^max(14,ceil(log2(g))); for all sufficiently "
                    "large r, g<=g_tilde<2g, while finitely many initial shells "
                    "do not affect convergence or divergence"
                ),
                "Lq_check": (
                    "integral g^q dnu_0 is comparable to sum_(r>=0)"
                    "(r+1)^(-(q+1)/2)<infinity"
                ),
                "tail_charge": (
                    "b_p is comparable to delta^(p*(1-1/q))/(p+1)^a"
                ),
                "critical_weight_failure": (
                    "if w*delta^(1-1/q)=1 then sum_p w^p*b_p is comparable "
                    "to sum_p (p+1)^(-a)=infinity because 1/q<a<1"
                ),
                "strict_inequality_is_sharp_for_this_information": True,
            },
            "status": "CERTIFIED_SHARP_CONDITIONAL_TRACE_HOLDER_WEIGHT_REGION",
        },
    }


def raw_rank_criticality_audit() -> dict[str, Any]:
    scale = 4 * RANK_TAIL_COEFFICIENT * Q(1, 4**B0)
    if not Q(0) < scale < COAREA_MASS:
        raise RuntimeError("saturating measure scale")
    rows = []
    for k in (0, 1, 4, 16):
        atom_mass = scale * Q(3, 4 ** (k + 1))
        rows.append(
            {
                "rank": B0 + k,
                "atom_mass": qstr(atom_mass),
                "tail_after_this_rank": (
                    f"(9158592/6875)*4^(-{B0 + k})"
                ),
                "2^(2B)_atom_contribution": qstr(
                    atom_mass * (1 << (2 * (B0 + k)))
                ),
            }
        )
    return {
        "separator_law": (
            "on atoms B=14+k, k>=0, put mass s*(3/4)*4^(-k), "
            "s=4*(9158592/6875)*4^(-14)"
        ),
        "total_mass": qstr(scale),
        "total_mass_below_raw_coarea_upper": True,
        "tail_identity": (
            "m{B>14+k}=(9158592/6875)*4^(-(14+k)) for every k>=0"
        ),
        "moment_ratio": (
            "successive contributions to integral 2^(qB) have ratio 2^q/4"
        ),
        "finite_moment_range": "q<2",
        "critical_and_supercritical_moments": "integral 2^(qB)=infinity for q>=2",
        "owner_selection": "identity owner operation; no additional grazing sparsity",
        "rows": rows,
        "rows_sha256": digest(rows),
        "logical_conclusion": (
            "the certified 4^-b tail cannot imply the q>q_*>2 moment needed at "
            "the fixed Round42 weight; extra owner sparsity or signed geometry is essential"
        ),
        "does_not_assert_actual_owner_law_saturates_the_tail": True,
        "status": "CERTIFIED_RAW_TAIL_Q_EQUALS_TWO_CRITICAL_SEPARATOR",
    }


def graph_current_f17_audit() -> dict[str, Any]:
    rows = []
    for scale in (1, 16, 256, 4096, 65536):
        rows.append(
            {
                "L": scale,
                "source_domain": f"[0,1/{scale}]x[0,1]",
                "target_domain": f"[0,1]x[0,1/{scale}]",
                "area_preserving_suffix": f"S_L=diag({scale},1/{scale})",
                "source_vector": "K=e_1",
                "source_L1_bulk_cost": qstr(Q(1, scale)),
                "Piola_target_vector": f"K'={scale}*e_1",
                "target_L1_bulk_cost": "1",
                "unit_physical_test": "phi(y)=y_1",
                "target_pairing": "1",
                "required_multiplier_lower": str(scale),
            }
        )
    return {
        "source_current": "T_(K,B)(phi)=integral_U K dot grad(phi)dm+B(phi)",
        "physical_test_norm": "norm(phi)_Lip=max(norm_infinity(phi),norm_infinity(grad phi))",
        "bulk_injection": "norm(T_(K,0))_(Lip*)<=norm(K)_L1",
        "trace_injection": "norm(T_(0,B))_(Lip*)<=TV(B)",
        "combined_source_graph_injection_constant": "1",
        "source_graph_injection_status": "CERTIFIED",
        "area_preserving_suffix_identity": (
            "S_*T_(K,B)=T_(Piola_S K,S_*B), Piola_S K(Sx)=DS(x)K(x)"
        ),
        "boundary_trace_TV_suffix_constant": "1",
        "bulk_vector_suffix_bound": (
            "norm(Piola_S K)_L1=integral_U |DS(x)K(x)|dm(x)"
        ),
        "determinant_one_separator": {
            "rows": rows,
            "rows_sha256": digest(rows),
            "conclusion": (
                "det(DS)=1 and Piola flux naturality do not bound the bulk graph-current "
                "pushforward in a common physical Lipschitz-dual norm"
            ),
        },
        "generic_Hdiv_or_L1_graph_space_has_uniform_area_preserving_suffix_constant": False,
        "precise_missing_billiard_input": (
            "a common anisotropic current norm with bounded physical observable inclusion "
            "and either a directional Piola estimate on the actual Eulerian generators "
            "or a quotient/coboundary cancellation before taking the norm"
        ),
        "required_F17_threshold": "C_dyn<7961063/7800000 (quarter route)",
        "physical_F17_suffix_constant": "NOT_CERTIFIED",
        "complete_strong_F13_intertwiner": "NOT_CERTIFIED",
        "status": "CERTIFIED_SOURCE_GRAPH_INJECTION_AND_BULK_PIOLA_SEPARATOR",
    }


def gate3_conditional_bridge() -> dict[str, Any]:
    return {
        "available_join": (
            "the Gate3 fixed 41508-slot free graph-current carrier and the Gate5 "
            "source representation T_(K,B)=-div(K)+B have compatible bulk/trace typing"
        ),
        "conditional_use": (
            "a future physical vector-current F17 norm could supply part of the bounded "
            "Q_s:X0_hat->B0_physical quotient and R_s:B2_physical->X2_hat lift"
        ),
        "conditions_still_required": [
            "same physical branch/component and owner IDs for every moving Gate3 slot",
            "artificial and duplicate traces assembled before absolute values",
            "uniform moving-test convergence on the component-indexed atlas",
            "bounded physical observable inclusion and the F17 suffix constant",
            "all 18 operator fields on one common recovered block",
            "cemetery and growing-depth no-|s|^-1 current tail",
        ],
        "conditions_sha256": digest(
            [
                "same physical branch/component and owner IDs for every moving Gate3 slot",
                "artificial and duplicate traces assembled before absolute values",
                "uniform moving-test convergence on the component-indexed atlas",
                "bounded physical observable inclusion and the F17 suffix constant",
                "all 18 operator fields on one common recovered block",
                "cemetery and growing-depth no-|s|^-1 current tail",
            ]
        ),
        "physical_Qs_Rs_lift_quotient": "NOT_CERTIFIED",
        "dynamic_branch_record_MT_DQ": "NOT_CERTIFIED",
        "automatic_promotion_from_source_graph_injection": False,
        "status": "CERTIFIED_TYPED_CONDITIONAL_BRIDGE_ONLY",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base parameter s=0",
            "owner_scope": (
                "each fixed insertion time j, registered finite regular arbitrary-R_n "
                "records with n>j, source-rank marked; no common-target Borel domination"
            ),
            "claim_type": (
                "trace-to-standard-family measure typing, sharp trace-survivor/weight "
                "threshold, raw q=2 criticality, and vector-current source/Piola audit"
            ),
        },
        "transverse_trace_standard_family_audit": (
            transverse_trace_standard_family_audit()
        ),
        "trace_nullity_and_weighted_closure_audit": (
            trace_nullity_and_weighted_closure_audit()
        ),
        "raw_rank_moment_criticality_audit": raw_rank_criticality_audit(),
        "physical_graph_current_F17_audit": graph_current_f17_audit(),
        "Gate3_common_graph_conditional_bridge": gate3_conditional_bridge(),
        "latest_technology_audit": {
            "official_versions_checked_2026_07_20": [
                "2606.10155v1",
                "2502.07765v2",
            ],
            "official_source_archive_sha256": {
                "2606.10155v1": "d568ad1351593e1d33d7855079583dd28d3c1ff6a26f673ca01ebc2784c132a6",
                "2502.07765v2": "a703115d1c2b943b82303a9f9f5d728ff819f2fa86365e663c8c2419ff02f60f",
            },
            "relevant_mechanisms": (
                "stable-curve/projective cones and sequential collision-volume transfer laws"
            ),
            "singular_transverse_owner_trace_injection_found": False,
            "vector_current_Hdiv_F17_with_numeric_suffix_constant_found": False,
            "status": "CHECKED_NO_DIRECT_TYPED_UPGRADE",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "transverse owner-trace is not a proper unstable standard-family law",
                "trace-nullity alone does not imply an exponentially weighted face tower",
                "sharp conditional trace Holder/weight admissible region",
                "raw 4^-b tail has exact q=2 critical separator",
                "physical graph-current source injection constant one",
                "boundary TV Piola constant one and bulk Piola unbounded separator",
                "typed conditional bridge to the Gate3 common free graph carrier",
            ],
            "reason_no_new_field_credit": (
                "no physical trace-to-proper extension or trace contraction is installed, "
                "the fixed-weight owner moment is unavailable, and the bulk current lacks "
                "a common physical anisotropic suffix bound"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "fixed_insertion_same_ID_owner_tail_transfer": "CERTIFIED_PREVIOUSLY",
            "owner_trace_is_proper_standard_family": "NOT_CERTIFIED",
            "trace_to_proper_standard_family_injection": "NOT_CERTIFIED",
            "trace_nullity_of_never_return_cemetery": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "fixed_weight_q_above_critical_owner_moment": "NOT_CERTIFIED",
            "unconditional_weak_weight_face_resolvent": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "physical_graph_current_source_injection": "CERTIFIED",
            "physical_F17_bulk_suffix_constant": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3_Qs_Rs_physical_lift_quotient": "NOT_CERTIFIED",
            "Gate3_MT_DQ": "NOT_CERTIFIED",
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


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(
            HERE
            / "cm2_gate5_round53_trace_standard_family_graph_f17_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("TRACE_TO_PROPER:", strict["trace_to_proper_standard_family_injection"])
    print("TRACE_CONTRACTION:", strict["quantitative_trace_survivor_contraction"])
    print("SOURCE_GRAPH:", strict["physical_graph_current_source_injection"])
    print("F17_SUFFIX:", strict["physical_F17_bulk_suffix_constant"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
