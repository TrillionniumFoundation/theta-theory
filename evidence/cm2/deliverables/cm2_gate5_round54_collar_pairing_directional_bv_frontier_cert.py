#!/usr/bin/env python3
"""Round-54 Gate-5 collar-extension, signed-pairing and directional-BV frontier.

The certificate remains at the base parameter ``s=0``.  It installs a
stagewise trace extension/recovery Borel-kernel schema on the explicitly
collar-admissible part of the labelled finite-record owner law.  Its mass on
the physical owner law is unknown.  The extension has mass norm one,
satisfies ``Tr E = Id`` and the killed-word intertwining on that restriction,
but carries the new inverse one-sided-collar debt ``Z_col`` and is not
asserted to be uniformly proper.

It also records two exact alternatives to the positive full-rank route.
The hit-minus-miss current has a canonical bounded-Lipschitz transport bound
before absolute values; a rho-rate paired-image estimate would already close
the signed weighted sum.  Separately, divergence-free Eulerian insertions can
be reduced to order-zero measures on a directional-BV source subspace, after
which every suffix has TV multiplier one.  Neither the paired-image rate nor
the physical directional-BV source field is presently certified, so no F17,
Gate-3 MT_DQ, or complete Gate-5 field is promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round54-collar-pairing-directional-bv-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json": (
        "8cacd8daa582c522a175cca3f24c7da1cb10c47f860b20645a365b27678d4590"
    ),
    "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json": (
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46"
    ),
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json": (
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d"
    ),
    "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json": (
        "33e3fae4633b133ffcaeb7bd0e552629ecf8528b3648b93ce85d5420e141bef5"
    ),
    "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json": (
        "3415f8533865e9ed907df823c1453ee981f3f1f1d5e04333fc14a90ddb2884d0"
    ),
    "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json": (
        "9abdc07cb0618f4a81b8e5591d8de83da7cce2c6d6a82fa41c834dd46c28412c"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
}

SURVIVAL_R = Q(111718729, 111718750)
BLOCK_DEPTH = 9148
B0 = 14
C_FLUX = Q(8064, 5)


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

    r53 = loaded[
        "cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json"
    ]["result"]
    trace53 = r53["transverse_trace_standard_family_audit"]
    bridge53 = trace53["conditional_unit_loss_bridge"]
    if bridge53["recovery_identity"] != "Tr composed E = Id on the owner trace laws":
        raise RuntimeError("Round53 recovery identity")
    if bridge53["killed_block_survivor_intertwining"] != (
        "K_trace=Tr composed K_proper composed E"
    ):
        raise RuntimeError("Round53 killed bridge")
    if trace53["conditional_unit_loss_bridge_is_installed"] is not False:
        raise RuntimeError("Round53 conditional boundary")
    if r53["strict_nonpromotion"]["physical_F17_bulk_suffix_constant"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round53 F17 boundary")

    r50 = loaded[
        "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
    ]["result"]
    owner = r50["global_owner_aware_boundary_ZB_kernel"]
    if owner["active_regular_root_section"] != (
        "the Borel graph of the unique transverse rank-0 root on the parent W"
    ):
        raise RuntimeError("Round50 root section")
    if owner["index_space_is_standard_Borel"] is not True:
        raise RuntimeError("Round50 Borel registry")
    if owner["finite_on_every_fixed_finite_regular_record"] is not True:
        raise RuntimeError("Round50 finite record")

    r44 = loaded[
        "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json"
    ]["result"]
    suffix44 = r44["occurrence_suffix_two_trace_transport"]["suffix_transport"]
    occurrence44 = r44["occurrence_suffix_two_trace_transport"]
    if occurrence44["one_sign_global_positive_mass_upper"] != "8064/5":
        raise RuntimeError("Round44 positive flux mass")
    if occurrence44["signed_current_TV_upper"] != "16128/5":
        raise RuntimeError("Round44 signed flux TV")
    if occurrence44["rank_convention"] != "B>=14":
        raise RuntimeError("Round44 rank convention")
    if suffix44["signed_current_formula"] != (
        "J_(n,j,e)=sigma_e*(tau_hit-tau_miss)"
    ):
        raise RuntimeError("Round44 signed pair")
    if suffix44["constant_test_cancellation_preserved"] is not True:
        raise RuntimeError("Round44 constant cancellation")
    if suffix44["suffix_positive_pushforward_mass_constant"] != "1":
        raise RuntimeError("Round44 suffix mass")

    r43 = loaded[
        "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
    ]["result"]
    generator43 = r43["one_step_area_eulerian_generator"]
    if generator43["divergence"] != (
        "div_mu X_s=0 on every regular area-preserving branch"
    ):
        raise RuntimeError("Round43 divergence")
    current43 = r43["arbitrary_path_Duhamel_current"]
    if "-div_mu" not in current43["one_step_derivative"]:
        raise RuntimeError("Round43 current")

    r47 = loaded[
        "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json"
    ]["result"]
    sub47 = r47["finite_regular_path_two_trace_C1dual_F13_sublayer"]
    if sub47["finite_regular_path_two_trace_C1dual_intertwiner"] != "CERTIFIED":
        raise RuntimeError("Round47 trace dual")
    if sub47["complete_Duhamel_bulk_current_included"] is not False:
        raise RuntimeError("Round47 bulk boundary")

    g3 = loaded[
        "cm2-gate3-common-graph-current-carrier-frontier-manifest-2026-07-17.json"
    ]["result"]
    if g3["common_free_carrier"]["total_fixed_slot_count"] != 41508:
        raise RuntimeError("Gate3 slots")
    if g3["physical_bridge_frontier"]["bounded_physical_lift_quotient_pair"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Gate3 bridge boundary")

    growth = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]["aggregate_canonical_Z_resolvent"]
    if growth["mass_factor_rho"] != "(111718729/111718750)^9148":
        raise RuntimeError("Round42 rho")
    if growth["explicit_block_index_weight"] != "w_Z=(1+rho^(-1))/2":
        raise RuntimeError("Round42 weight")
    return loaded


def collar_extension_audit() -> dict[str, Any]:
    sample = [
        ("a0", Q(1, 2), Q(1, 2)),
        ("a1", Q(1, 4), Q(1, 8)),
        ("a2", Q(1, 8), Q(1, 64)),
        ("a3", Q(1, 8), Q(1, 4096)),
    ]
    rows = []
    z_col = Q(0)
    for label, mass, ell in sample:
        contribution = mass / ell
        z_col += contribution
        rows.append(
            {
                "owner_label": label,
                "trace_mass": qstr(mass),
                "dyadic_collar_length": qstr(ell),
                "constant_density": qstr(1 / ell),
                "collar_Z_contribution": qstr(contribution),
            }
        )
    if sum((mass for _, mass, _ in sample), Q(0)) != 1:
        raise RuntimeError("sample mass")
    if z_col != Q(523):
        raise RuntimeError("sample collar debt")
    return {
        "physical_scope": (
            "the collar-admissible labelled finite-record subregistry A_col={a:d_a>0}, "
            "away from corners, simultaneous events and boundary accumulations; the "
            "maps E_j and Tr_j are stage dependent"
        ),
        "same_ID_label": (
            "(restriction-id,time-j,physical-event-signature,primitive-key,"
            "connected-rank-0,side-label,word-cell)"
        ),
        "trace_law_typing": (
            "a finite Borel measure nu_j on the standard-Borel owner/root base; the "
            "base may be continuous and is not replaced by a countable atom list"
        ),
        "joint_labelled_carrier": (
            "Mtilde_j={(omega,x):omega in A_col, x in I_(omega,j)}; omega and the "
            "complete record label are retained through E_j, the fiberwise word "
            "operator and Tr_t, so overlapping physical collar images are not identified"
        ),
        "positive_clearance_predicate": (
            "after choosing the owned half-open side, d_a is the one-sided distance "
            "from the anchor root face to the next OTHER singularity, homogeneity, "
            "owner or hole boundary in the fixed word; the already-owned anchor face "
            "is excluded from this distance, and A_col retains exactly d_a>0"
        ),
        "canonical_Borel_selection": (
            "k(omega)=min{k>=0:2^(-k)<=min(1,d(omega))} and "
            "ell(omega)=2^(-(k(omega)+1))<d(omega); measurable integer minima on "
            "the standard-Borel base make ell Borel"
        ),
        "Borel_kernel_proof": (
            "in each countable chart/word label, the predicate that an anchored "
            "half-open dyadic collar (xi,xi+ell] or [xi-ell,xi) has no boundary contact "
            "except the designated anchor face and otherwise lies in one open fixed-word "
            "side cell is Borel; A_col is the countable union of these predicates, the "
            "least candidate is Borel, and pushing normalized Lebesgue through the "
            "registered collar chart is a Borel probability kernel"
        ),
        "anchored_half_open_geometry": (
            "I_(omega,j)=(xi_(omega,j),xi_(omega,j)+ell(omega)] on the plus side or "
            "[xi_(omega,j)-ell(omega),xi_(omega,j)) on the minus side; its closure may "
            "touch the selected root face only at xi, while the far endpoint is strict "
            "interior because ell<d"
        ),
        "source_stage_extension": (
            "E_j is the Borel Markov kernel from omega to {omega}xI_(omega,j), "
            "with fiber density ell(omega)^(-1)dH1 on A_col"
        ),
        "stage_recovery": (
            "using the selected one-sided branch value S_(j,t)^side(xi), Tr_t is the "
            "deterministic Borel kernel (omega,S_(j,t)x) maps to "
            "(omega,S_(j,t)^side(xi_(omega,j))); it collapses inside each retained "
            "label fiber to the mapped root, not to the source root"
        ),
        "mass_norms": "norm_mass(E)=norm_mass(Tr)=1 on measures restricted to A_col",
        "recovery_identity": (
            "Tr_j composed E_j = Id on the stage-j owner trace laws restricted to A_col"
        ),
        "killed_word_intertwining": (
            "K_trace_(j,t)=Tr_t composed K_word_(j,t) composed E_j because the whole "
            "anchored one-sided labelled collar fiber I_a,j has the same half-open "
            "killed-word bit as xi_a,j and K_word acts fiberwise without dropping omega"
        ),
        "no_internal_cut_or_mass_leak": (
            "apart from the designated anchor root face, I_a,j is selected inside one "
            "connected open side cell of the common refinement by every other "
            "singularity, homogeneity, owner and hole boundary in the fixed word; "
            "S_(j,t) is one regular diffeomorphic one-sided branch on the collar "
            "interior at every registered stage, half-open endpoints are owned once, "
            "and pushforward preserves its total mass"
        ),
        "zero_map_excluded": True,
        "extension_density_regularity": (
            "constant density on each collar, so the log-Holder regularity mark is zero"
        ),
        "standard_family_shape_debt": (
            "Z_col(E nu)=integral_(A_col) ell(omega)^(-1)dnu(omega) in [0,infinity]; "
            "a discrete disintegration is the corresponding sum_a p_a/ell_a, and "
            "finiteness is NOT_CERTIFIED"
        ),
        "full_rank_shape_debt": (
            "Z_col,B(E nu)=integral_(A_col)2^B(omega)/ell(omega)dnu(omega)"
        ),
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "sample_Z_col": qstr(z_col),
        "uniformly_proper_if": (
            "ell_a>=delta_proper for every retained a, with the required common "
            "orientation and atlas; this hypothesis is not currently available"
        ),
        "collar_admissible_stagewise_mass_E_Tr_schema_installed": True,
        "all_physical_owner_records_stagewise_E_Tr_installed": False,
        "nu_mass_of_A_col_positive_or_full": "NOT_CERTIFIED",
        "Round53_uniform_proper_bridge_installed": False,
        "why_not_the_Round53_genuine_bridge": (
            "each finite collar is a standard-curve probability, but an aggregate "
            "proper-family input needs at least finite Z_col=sum p_a/ell_a and the "
            "uniform/block properness hypotheses; neither is certified"
        ),
        "quantitative_trace_contraction_installed": False,
        "parent_Z_does_not_control_collar_Z_separator": {
            "law": (
                "for a_k with p_k=2^(-k), parent length 1, B=14 and "
                "ell_k=2^(-k^2), k>=1"
            ),
            "trace_mass": "sum_k 2^(-k)=1",
            "unranked_parent_inverse_length_debt": "sum_k p_k/1=1",
            "full_parent_owner_ZB_at_B14": (
                "sum_k 2^14*p_k/1=2^14=16384, finite"
            ),
            "collar_inverse_length_debt": (
                "sum_k 2^(k^2-k)=infinity because its terms do not tend to zero"
            ),
            "full_rank_collar_debt": (
                "sum_k 2^14*p_k/ell_k=2^14*infinity=infinity"
            ),
            "logical_conclusion": (
                "the Round50 parent-W owner Z_B cannot be renamed as the one-sided "
                "same-word collar debt without a new geometric comparison"
            ),
        },
        "grazing_homogeneity_accumulation_separator": {
            "model": (
                "one-sided coordinate c in (0,ell] with uniform probability dc/ell, "
                "cut into H_k=(ell/(k+1)^2,ell/k^2], k>=1, accumulating at c=0"
            ),
            "root": "xi=0, so d_xi=0 although the face root can be transverse",
            "uniform_collar_subdivision": (
                "length(H_k)=ell*(1/k^2-1/(k+1)^2), the shell masses telescope "
                "to one, and each inverse-length Z contribution equals 1/ell"
            ),
            "shape_debt": (
                "sum over the infinitely many nonempty shells of 1/ell=infinity"
            ),
            "physical_warning": (
                "moving-occurrence/grazing roots are not put in A_col merely because "
                "their rank-zero face intersection is transverse"
            ),
            "logical_conclusion": (
                "positive full-word clearance is an extra physical predicate, not a "
                "consequence of finite depth or transverse connected rank zero"
            ),
        },
        "first_missing_global_join": (
            "first prove that A_col carries the required positive/full trace mass, then "
            "an all-insertion-time same-ID integral bound on Z_col or a recovery theorem "
            "whose clock/debt is integrable on the owner law"
        ),
        "status": "CERTIFIED_A_COL_STAGEWISE_COLLAR_E_TR_WITH_UNCONTROLLED_SHAPE_DEBT",
    }


def signed_pairing_audit() -> dict[str, Any]:
    rho = SURVIVAL_R**BLOCK_DEPTH
    w_z = (1 + 1 / rho) / 2
    kappa = 1 / w_z
    if w_z * rho != (1 + rho) / 2 or not w_z * rho < 1:
        raise RuntimeError("signed weighted route")
    rows = []
    for distance in (Q(2), Q(1), Q(1, 16), Q(1, 1024)):
        rows.append(
            {
                "paired_distance": qstr(distance),
                "BL_difference_factor": qstr(min(Q(2), distance)),
                "physical_flux_BL_charge_upper": qstr(
                    C_FLUX * min(Q(2), distance)
                ),
            }
        )
    return {
        "pairing_scope": (
            "fiberwise on the disjoint marked union over immutable physical record, "
            "orientation/event and retained source-rank B; no product coupling is "
            "taken across different records or ranks"
        ),
        "physical_signed_pair": (
            "write the physical signed source flux as lambda_p=lambda_p^+-lambda_p^- "
            "from the Jordan decomposition of sigma_e; with the immutable hit and miss "
            "kernels H_p,M_p set mu_p^+=H_p*lambda_p^+ + M_p*lambda_p^- and "
            "mu_p^-=M_p*lambda_p^+ + H_p*lambda_p^-; then J_p=mu_p^+-mu_p^- "
            "and both positive marginals have equal mass m_p=abs(lambda_p)(source)"
        ),
        "physical_flux_typing": (
            "the coefficient is the actual physical sigma_e flux law frozen in Round44; "
            "2^B is only a positive occurrence-rank envelope and is not identified with "
            "sigma_e"
        ),
        "physical_positive_mass_upper": "m_p<=C_flux=8064/5",
        "coupling_kernel": (
            "in every fixed marked standard-Borel fiber define canonically pi_p=0 when "
            "m_p=0 and pi_p=(mu_p^+ tensor mu_p^-)/m_p when m_p>0; this normalized-"
            "product formula has marginals mu_p^+,mu_p^-, total mass m_p, and is a "
            "Borel kernel without any measurable-choice theorem"
        ),
        "constant_test": "J_p(1)=0",
        "test_norm": "norm(phi)_BL=max(norm_infinity(phi),Lip(phi))",
        "pointwise_bound": (
            "abs(phi(y+)-phi(y-))<=min(2,d(y+,y-))*norm(phi)_BL"
        ),
        "canonical_pair_charge": (
            "d_p(pi_p)=integral min(2,d(y+,y-))d pi_p(y+,y-)"
        ),
        "BL_dual_bound": "norm(J_p)_(BL*)<=d_p",
        "rows": rows,
        "rows_sha256": digest(rows),
        "weighted_resolvent_hypothesis": "d_p<=C_pair*delta_pair^p",
        "weighted_resolvent_condition": "w*delta_pair<1",
        "weighted_resolvent_bound": (
            "sum_p w^p norm(J_p)_(BL*)<=C_pair/(1-w*delta_pair)"
        ),
        "rho_rate_at_Round42_weight": {
            "weight": "w_Z=(1+rho^(-1))/2",
            "product": "w_Z*rho=(1+rho)/2<1",
            "denominator": "1-w_Z*rho=(1-rho)/2",
            "bound": "sum_p w_Z^p norm(J_p)_(BL*)<=2*C_pair/(1-rho)",
            "rho_fraction_binary_sha256": fraction_digest(rho),
            "kappa_fraction_binary_sha256": fraction_digest(kappa),
        },
        "physical_flux_distance_sufficient_condition": (
            "if pi_p is supported on d(y+,y-)<=A*delta_pair^p, then the Round44 "
            "mass bound gives d_p(pi_p)<=A*(8064/5)*delta_pair^p"
        ),
        "rank_envelope_conditional": (
            "alternatively, if only m_p<=C_sigma*2^B and support(pi_p) lies in "
            "d<=A*2^(-B)*delta_pair^p, then d_p<=A*C_sigma*delta_pair^p; this is "
            "an envelope hypothesis, never the equality sigma_e=2^B"
        ),
        "why_q_star_is_bypassed": (
            "the estimate pairs the signed images before absolute values; it is not "
            "Holder interpolation of the positive 2^B trace charge"
        ),
        "physical_pair_separation_rate": "NOT_CERTIFIED",
        "positive_F10_or_TV_face_tower_from_signed_pairing": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
        "logical_scope": (
            "a signed F13/F17/MT_DQ route only; constant cancellation alone gives no "
            "distance decay and cannot close positive F10 or cemetery mass"
        ),
        "status": "CERTIFIED_SIGNED_PAIR_BL_BOUND_AND_CONDITIONAL_RHO_WEIGHT_ROUTE",
    }


def directional_bv_order_reduction_audit() -> dict[str, Any]:
    rows = []
    for periods in (1, 4, 16, 64, 256):
        rows.append(
            {
                "triangle_wave_periods": periods,
                "L_infinity": "1",
                "directional_BV_variation": str(4 * periods),
                "variation_to_Linfinity_ratio": str(4 * periods),
            }
        )
    return {
        "coordinates": "collision area coordinates with flat mu=R*dr*dp on each component",
        "physical_generator": (
            "X_s=(partial_s F_s) composed F_s^(-1), div_mu X_s=0 on every regular branch"
        ),
        "directional_source_space": (
            "BV_X^tr(U) consists of h in L1(U) with finite signed directional "
            "derivative D_X h and a registered finite normal trace gamma_Xh on "
            "partial U satisfying the Gauss-Green identity"
        ),
        "directional_derivative_typing": (
            "D_X h is the divergence/current derivative relative to mu, characterized "
            "on compact interior tests by integral phi d(D_X h)=-integral h*X(phi)dmu"
        ),
        "compact_interior_identity": (
            "T_h=-D_X h as an order-zero signed measure, with D_X h typed relative to mu"
        ),
        "domain_identity": (
            "T_h=-D_X h+gamma_Xh, with gamma_Xh=(R*h*X dot n_U)H^1 when the "
            "classical trace exists for mu=R*dr*dp, and each physical boundary trace "
            "included exactly once"
        ),
        "source_cost": (
            "C_BVXtr(h;U)=TV(D_X h)+TV(gamma_Xh)"
        ),
        "order_zero_TV_bound": "TV(T_h)<=C_BVXtr(h;U)",
        "finite_regular_suffix": (
            "for every measurable regular suffix S, TV(S_*T_h)<=TV(T_h)"
        ),
        "suffix_multiplier_on_directional_BV_subcarrier": (
            "C_dyn=1 in the order-zero TV/C0-dual transport norm"
        ),
        "not_a_single_fixed_physical_dynamic_test_field": (
            "TV pushforward is a fixed measure norm, but no bounded identification with "
            "the required common physical B0/dynamic-Holder test field and its 18-field "
            "operator block is certified"
        ),
        "passes_quarter_threshold": Q(1) < Q(7961063, 7800000),
        "piecewise_constant_flat_density_sublayer": (
            "D_X h=0 in every persistent cell interior; only the explicitly assembled "
            "physical boundary flux remains"
        ),
        "Linfinity_nonimplication_separator": {
            "space": "U=[0,1]^2, X=e_1 and R=1 in this logical flat model",
            "law": "h_N is the continuous triangle wave with N periods and range [-1,1]",
            "rows": rows,
            "rows_sha256": digest(rows),
            "conclusion": (
                "norm_infinity(h_N)=1 while TV(D_X h_N)=4N, so the existing "
                "c_X*norm_infinity source charge does not control the order-reduced cost"
            ),
        },
        "physical_all_input_directional_BV_bound": "NOT_CERTIFIED",
        "same_ID_boundary_flux_join_for_order_reduction": "NOT_CERTIFIED",
        "complete_physical_F17": "NOT_CERTIFIED",
        "precise_gain": (
            "the missing suffix derivative product is removed on the BV_X^tr subcarrier; "
            "the first missing quantity moves to a source directional-variation, normal-"
            "trace and boundary-assembly bound, naturally adjacent to F14"
        ),
        "status": "CERTIFIED_DIRECTIONAL_BV_ORDER_REDUCTION_WITH_SUFFIX_CONSTANT_ONE",
    }


def gate3_conditional_join() -> dict[str, Any]:
    conditions = [
        "bind every parameterized moving physical boundary graph/component and owner ID to one of the 41508 fixed graph slots",
        "lift the physical B2 input into a uniformly bounded directional-BV_X^tr payload",
        "assemble duplicate/artificial domain-flux traces before total variation",
        "prove bounded inclusion of the bulk order-zero measure and the boundary graph-slot family in physical B0",
        "prove common-atlas moving-limit convergence and the growing-depth no-|s|^-1 tail",
        "complete the remaining 17 operator fields on one recovered physical block",
    ]
    return {
        "new_typed_payload": (
            "split the order-reduced current: the bulk order-zero measure -D_X h and "
            "the immutable parameterized physical boundary graph flux gamma_Xh are "
            "sent to distinct summands of X0_hat"
        ),
        "free_carrier_match": (
            "the bulk -D_X h belongs to the (C^{1,alpha}(N))* summand, while only the "
            "parameterized boundary graph fluxes belong to l1(Omega_<=2;M(I)); no "
            "bulk measure is counted as one of the 41508 graph slots"
        ),
        "bulk_destination": "-D_X h -> (C^{1,alpha}(N))*",
        "boundary_destination": (
            "parameterized gamma_Xh graph fluxes -> l1(Omega_<=2;M(I)), with 41508 slots"
        ),
        "bulk_graph_slot_conflation_excluded": True,
        "finite_record_distribution_identity": "CERTIFIED_CONDITIONAL_ON_THE_LISTED_TYPING",
        "conditions": conditions,
        "conditions_sha256": digest(conditions),
        "physical_Rs_directional_BV_lift": "NOT_CERTIFIED",
        "physical_Qs_order_zero_quotient": "NOT_CERTIFIED",
        "intertwining_Qs_Phat_Rs": "NOT_CERTIFIED",
        "dynamic_branch_record_MT_DQ": "NOT_CERTIFIED",
        "automatic_promotion_from_order_reduction": False,
        "status": "CERTIFIED_SHARPER_DIRECTIONAL_BV_CONDITIONAL_GATE3_JOIN_ONLY",
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
                "one labelled finite regular owner record at a time; global sums over "
                "all insertion times and arbitrarily small collars remain fail closed"
            ),
            "claim_type": (
                "recordwise legal collar E/Tr, signed paired-image BL bound, and "
                "directional-BV order reduction"
            ),
        },
        "recordwise_owner_collar_E_Tr": collar_extension_audit(),
        "signed_hit_miss_pairing_resolvent": signed_pairing_audit(),
        "directional_BV_F17_order_reduction": directional_bv_order_reduction_audit(),
        "Gate3_directional_BV_conditional_join": gate3_conditional_join(),
        "latest_technology_audit": {
            "official_query_date": "2026-07-20",
            "official_versions_checked": [
                "2606.10155v1",
                "2604.19671v2",
                "2604.25881v1",
                "2502.07765v2",
            ],
            "official_source_archive_sha256_replayed_from_Round53": {
                "2606.10155v1": "d568ad1351593e1d33d7855079583dd28d3c1ff6a26f673ca01ebc2784c132a6",
                "2502.07765v2": "a703115d1c2b943b82303a9f9f5d728ff819f2fa86365e663c8c2419ff02f60f",
            },
            "newer_direct_trace_contraction_or_vector_current_theorem_found": False,
            "relevant_existing_mechanisms": (
                "small/sparse-hole cone recovery, stable-curve anisotropic norms, "
                "standard-family Growth, and projective cones"
            ),
            "why_not_imported": (
                "the sources do not supply the same-ID one-sided collar debt, paired "
                "hit/miss image separation, or a numeric BV_X-to-physical block bound"
            ),
            "status": "CHECKED_NO_DIRECT_TYPED_UPGRADE",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "collar-admissible stage-dependent mass-isometric same-ID collar E_j/Tr_j with exact killed-word intertwining",
                "one-sided collar inverse-length debt and parent-Z nonimplication separator",
                "signed hit-minus-miss BL pairing and conditional rho-weight resolvent",
                "directional-BV order reduction with suffix TV multiplier one",
                "sharper directional-BV conditional join to the Gate3 free carrier",
            ],
            "reason_no_new_field_credit": (
                "there is no global collar-debt bound or trace contraction, no physical "
                "paired-image rate, and no all-input directional-BV/source-to-physical join"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "collar_admissible_stagewise_mass_same_ID_collar_Ej_Trj": "CERTIFIED",
            "all_physical_owner_recordwise_Ej_Trj": "NOT_CERTIFIED",
            "positive_or_full_owner_trace_mass_of_A_col": "NOT_CERTIFIED",
            "A_col_killed_word_intertwining": "CERTIFIED",
            "Round53_uniformly_proper_trace_extension_bridge": "NOT_CERTIFIED",
            "global_owner_collar_Z_integrability": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "fixed_weight_q_above_critical_owner_moment": "NOT_CERTIFIED",
            "signed_pair_BL_bound": "CERTIFIED",
            "physical_paired_image_rho_rate": "NOT_CERTIFIED",
            "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
            "positive_F10_face_tower_from_signed_pairing": "NOT_CERTIFIED",
            "directional_BV_order_reduction_suffix_constant_one": "CERTIFIED_SUBCARRIER",
            "physical_all_input_directional_BV_source_bound": "NOT_CERTIFIED",
            "physical_F17_bulk_suffix_constant": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate5_round54_collar_pairing_directional_bv_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print(
        "A_COL_EJ_TRJ:",
        strict["collar_admissible_stagewise_mass_same_ID_collar_Ej_Trj"],
    )
    print("GLOBAL_TRACE_CONTRACTION:", strict["quantitative_trace_survivor_contraction"])
    print("BVX_SUBCARRIER:", strict["directional_BV_order_reduction_suffix_constant_one"])
    print("PHYSICAL_F17:", strict["physical_F17_bulk_suffix_constant"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
