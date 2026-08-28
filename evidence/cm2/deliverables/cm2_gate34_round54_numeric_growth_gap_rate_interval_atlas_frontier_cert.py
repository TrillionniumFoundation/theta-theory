#!/usr/bin/env python3
"""Round-54 Gate-4 numerical Growth/gap-rate and interval-atlas frontier.

This certificate makes one genuinely numerical *conditional* advance toward
the five-row SYZ clock left by Round 53.  It does *not* identify the number
696 with the SYZ constant ``c_p``.  Instead it combines

* the physical one-step square-root image-length bound,
* the frozen standard-family Z recurrence, and
* the official rank-R magnet-gap recovery formula

to obtain the candidate exponential envelope

    lambda_bar = 9997/10000.

This envelope is certified only after a same-ID join places the official
magnet-gap density ``checkrho|V`` in the registered numerical density cone.
That join is not available, so the official five-row ``lambda`` remains
unfilled together with zeta0, S, R and C.

It also freezes a metric-safe executable schema for a future rational
parameter-interval crossing atlas.  No physical atlas rows are fabricated.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round54-numeric-growth-gap-rate-interval-atlas-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round54-numeric-growth-gap-rate-interval-atlas-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-round53-effective-clock-relative-atlas-frontier-manifest-2026-07-20.json": (
        "83c74e9b547e94844645fc8465f4bb9b36ce6723bbf68ab841b191b763e93302"
    ),
    "cm2_gate34_round53_effective_clock_relative_atlas_frontier_cert.py": (
        "65a1f102ea2e4f5c7b4ddecf37f5f08baf334e0311e5338ad7fbd9d997d02deb"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2_gate34_round42_numeric_c24_growth_block_cert.py": (
        "29e2be94c1e57368860bed03f37454ee3724791182eb697493625db5ed095d27"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py": (
        "01e32ca209818f4077443a7692622c4202ab7f1066e2f95802185e2be7a2cc9a"
    ),
    "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json": (
        "4e0c8216892afe9ce0c19e22b9ecc5742f21e9e4512d949b88325e1ee1ff70d5"
    ),
    "cm2_gate4_numeric_growth_leaves_frontier_cert.py": (
        "52effe0b62a8e90dc03b85247f59fc7c96b6b680e9684d506ff59745f8bc0669"
    ),
    "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json": (
        "4248c215821ba6e23eb78c64158b1301e1b33d964fb0cd024e4b8e4427247b21"
    ),
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json": (
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18"
    ),
}

ARXIV_SOURCE_HASHES = {
    "1210.0011v4_archive": "b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5",
    "1210.0011v4_Moving_final.tex": "921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44",
    "2104.06947v3_archive_gzip": "bb1486f08014e5d2d9ed6d9a80c541d13cb4334299d4767cf073271dfe99e33a",
    "2104.06947v3_cones-revision2.tex": "c0de4f5682c8a3a13b7a85fb46af712cd44945740cd8ad767424c10eb97d3150",
    "2604.25881v1_archive": "bd03bb220ca4456e65a511669b76a903f2a1dba6629de70935490664104ce5b4",
    "2604.25881v1_billiard-mme-arXiv-v1.tex": "b8f79a99f5f98648f91848cd7b4e489846f4512d6ed35ebd042229da3c89ee94",
    "2502.07765v2_archive": "a703115d1c2b943b82303a9f9f5d728ff819f2fa86365e663c8c2419ff02f60f",
    "2502.07765v2_sequential-revision1.tex": "1e4dfee91d2c7e2fc418b9a9b298be0afe78e9547a7729eaecadf88f73991951",
}

DENSITY_RATIO = Q(2000, 1999)
GROWTH_A = Q(360134800, 360493663)
GROWTH_MARGIN = 1 - GROWTH_A
DELTA_STAR = Q(1, 10**90)
ADDITIVE_B = Q(2, 1) / DELTA_STAR
GROWTH_STATIONARY_A = ADDITIVE_B / GROWTH_MARGIN
LAMBDA = Q(180337, 144000)
HAT_C = Q(20, 3807)
L0_UPPER = Q(68)
C_LEN = Q(5962448355, 5191)
C_E = C_LEN**2
HALF_LIFE = 696
RECOVERY_RANK_SLOPE = 1 + HALF_LIFE
LAMBDA_BAR = Q(9997, 10000)
FAILED_DECIMAL_PREDECESSOR = Q(2499, 2500)
ETA_THRESHOLD = Q(43008, 14285703575)
EUCLIDEAN_TO_ADAPTED_RELATIVE = Q(20, 3807)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
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


def checked_text(name: str, tokens: tuple[str, ...]) -> str:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe text dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"text dependency hash: {name}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise RuntimeError(f"missing dependency token {name}: {token}")
    return text


def validate_dependencies() -> None:
    prior = load_json(
        "cm2-gate34-round53-effective-clock-relative-atlas-frontier-manifest-2026-07-20.json"
    )
    gap = prior["result"]["coupling_gap_five_row_decomposition"]
    rows = gap["remaining_atomic_rows"]
    if [row["id"] for row in rows] != ["zeta0", "S", "R", "C", "lambda"]:
        raise RuntimeError("Round53 five rows")
    if any(row["value"] is not None for row in rows):
        raise RuntimeError("Round53 numerical frontier")
    checked_text(
        "cm2_gate34_round53_effective_clock_relative_atlas_frontier_cert.py",
        (
            "n_p <= 696*317 = 220632",
            "eta_s^* >= 43008/14285703575",
            "the post-coupling gap law starts with arbitrarily short rank gaps",
        ),
    )

    block = load_json(
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    )["result"]["physical_branch_length_pullback"]
    if Q(block["holder_constant_C_len"]) != C_LEN:
        raise RuntimeError("Round42 C_len")
    if block["numeric_length_holder"] != "CERTIFIED":
        raise RuntimeError("Round42 length status")
    checked_text(
        "cm2_gate34_round42_numeric_c24_growth_block_cert.py",
        (
            "length_E(T_s W)<",
            "sqrt(length_E(W))",
            "uniform_scope",
        ),
    )

    growth = load_json(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if Q(growth["density_ratio"]) != DENSITY_RATIO:
        raise RuntimeError("density ratio")
    if Q(growth["vartheta_p"]) != GROWTH_A:
        raise RuntimeError("Growth a")
    if growth["A1"] != 1005:
        raise RuntimeError("Growth recovery block")
    checked_text(
        "cm2_gate4_numeric_invariant_family_growth_recovery_frontier_cert.py",
        (
            "Z_*(T F)<=vartheta_p*Z_*(F)+2e90*mass(F)",
            "euclidean_SYZ_form",
            "Z_n^E/mass<=(C_p/2)*(1+a^n Z_0^E/mass)",
            "recovery_block = 1005",
            "assert contraction**recovery_block <= Q(1, 2)",
        ),
    )

    leaves = load_json(
        "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if Q(leaves["Lambda"]) != LAMBDA or Q(leaves["c_hat"]) != HAT_C:
        raise RuntimeError("hyperbolic leaves")
    checked_text(
        "cm2_gate4_numeric_growth_leaves_frontier_cert.py",
        (
            '"maximum_homogeneous_unstable_curve_length_strict_upper": "68"',
            '"numeric_C_metric_C_cone_L0_C_s_leaves": "CERTIFIED"',
        ),
    )
    if L0_UPPER != 68:
        raise RuntimeError("L0 upper")

    gauge = load_json(
        "cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json"
    )["result"]
    if gauge["instance_specific_fixed_gauge"]["uniform_numeric_m_s"] != "1":
        raise RuntimeError("Round51 gauge")
    if gauge["uniform_standard_family_bump_minorisation"][
        "uniform_SYZ_dynamic_density_bridge"
    ]["global_adapted_u_curve_length_strict_upper"] != "40":
        raise RuntimeError("Round51 adapted length")

    threshold = load_json(
        "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json"
    )["result"]["exact_remaining_cover_thresholds"]
    if Q(threshold["incidence_safe_required_direct_C24_fraction"]) != Q(
        2688, 893303125
    ):
        raise RuntimeError("Round49 beta threshold")
    if Q(threshold["direct_C24_hit_gap"]) != Q(21, 111718750):
        raise RuntimeError("Round49 hit gap")


def numerical_growth_constants() -> dict[str, Any]:
    # Iterating l_{j+1}<C_len sqrt(l_j) gives
    # l_n<C_len^(2-2^(1-n))*l_0^(2^-n)<C_len^2*l_0^(2^-n).
    assert C_LEN > 1
    assert C_E < 2**41
    assert LAMBDA**2 < 2
    assert GROWTH_A**HALF_LIFE < Q(1, 2)

    endpoint_conversion = (
        Q(27, 5) * Q(141, 2) * DENSITY_RATIO
    )
    euclidean_length_coefficient = (
        Q(141, 2) / DELTA_STAR
        + Q(141, 4) * GROWTH_STATIONARY_A
    )
    c_gr = endpoint_conversion * euclidean_length_coefficient
    assert c_gr == Q(
        64566981624654 * 10**92,
        239122379,
    )

    proof_rows = [
        {
            "step": 1,
            "claim": "C_e=C_len^2 is a safe official square-root-growth constant",
            "formula": "ell_E(T^n W)<C_len^(2-2^(1-n))*ell_E(W)^(2^-n)<C_len^2*ell_E(W)^(2^-n)",
        },
        {
            "step": 2,
            "claim": "artificial endpoints only enlarge the true endpoint event",
            "formula": "{r_true,n<epsilon} subset {r_artificial,n<epsilon}",
        },
        {
            "step": 3,
            "claim": "endpoint mass is controlled by adapted boundary Z with both metric conversions paid",
            "formula": "m_E{r_artificial,n<epsilon}<=(27/5)*(141/2)*R_rho*epsilon*Z_n^*",
        },
        {
            "step": 4,
            "claim": "initial equal delta-star subdivision and Z recurrence",
            "formula": "Z_0^*<=1+(141/2)*ell_E(W)/delta_star; Z_n^*<=a^n*Z_0^*+[B/(1-a)]*ell_*(W), ell_*(W)<=(141/4)ell_E(W)",
        },
        {
            "step": 5,
            "claim": "frozen fixed-map numerical Growth lemma",
            "formula": "m_W{r_W,n<epsilon}<=C_gr*(a^n+ell_E(W))*epsilon",
        },
    ]
    return {
        "C_len": qstr(C_LEN),
        "safe_frozen_fixed_map_C_e": qstr(C_E),
        "C_e_strict_power_two_upper": "2^41",
        "Growth_vartheta": qstr(GROWTH_A),
        "Growth_additive_B": qstr(ADDITIVE_B),
        "Growth_stationary_additive_B_over_one_minus_a": qstr(
            GROWTH_STATIONARY_A
        ),
        "Euclidean_endpoint_conversion_prefactor": qstr(endpoint_conversion),
        "Euclidean_length_coefficient": qstr(euclidean_length_coefficient),
        "numeric_C_gr": qstr(c_gr),
        "numeric_Growth_lemma": (
            "m_W{r_W,n<epsilon}<=C_gr*(a^n+ell_E(W))*epsilon"
        ),
        "scope": (
            "frozen stationary physical maps T_sigma, |sigma|<=1/400, with the registered canonical artificial subdivision; not the full moving-configuration SYZ class"
        ),
        "proof_rows": proof_rows,
        "proof_rows_sha256": digest(proof_rows),
        "status": "CERTIFIED_NUMERIC_FROZEN_FIXED_MAP_GROWTH_LEMMA",
    }


def dyadic_gap_builder(
    G: int,
    W: int,
    Cgpp: Q,
    zeta: Q,
    density_intercept: int,
    base_clock: int = 0,
) -> dict[str, Any]:
    """Conditional exact builder; sample inputs are never physical claims.

    ``density_intercept`` is a rank-independent clock debit supplied by the
    missing same-ID density join.  It must absorb both the regularisation
    time and any certified entry-Z inflation before the numerical Euclidean
    SYZ recurrence may be applied to ``checkrho|V``.
    """
    if not isinstance(G, int) or not isinstance(W, int) or G < 0 or W < 0:
        raise ValueError("G,W must be nonnegative integers")
    if Cgpp <= 0:
        raise ValueError("C_g'' must be positive")
    if not Q(0) < zeta < Q(1):
        raise ValueError("zeta must lie in (0,1)")
    if not isinstance(density_intercept, int) or density_intercept < 0:
        raise ValueError("density intercept must be a nonnegative integer")
    if not isinstance(base_clock, int) or base_clock < 0:
        raise ValueError("base clock must be a nonnegative integer")
    K = 82 + 2 * G + 2 * W
    offset = HALF_LIFE * K - 1 + density_intercept
    full_offset = max(offset, base_clock)
    multiplier = max(Q(1), Cgpp)
    extra = 0
    while multiplier * LAMBDA_BAR**extra >= 1 - zeta:
        extra += 1
    assert multiplier * LAMBDA_BAR**extra < 1 - zeta
    if extra:
        assert multiplier * LAMBDA_BAR ** (extra - 1) >= 1 - zeta
    r = full_offset + extra
    return {
        "G": G,
        "W": W,
        "C_g_double_prime": qstr(Cgpp),
        "zeta": qstr(zeta),
        "same_magnet_density_join_assumed": True,
        "rank_independent_density_recovery_intercept": density_intercept,
        "base_clock_for_rank_zero_top_and_excess": base_clock,
        "K": K,
        "rank_R_recovery_time_strict_upper": (
            f"697*R+{offset}"
        ),
        "envelope_prefactor_C_bar": (
            f"max(1,{qstr(Cgpp)})*(9997/10000)^(-{full_offset})"
        ),
        "least_extra_blocks_after_offset": extra,
        "least_gap_only_r_with_C_bar_lambda_bar_pow_r_lt_one_minus_zeta": r,
    }


def numerical_gap_rate() -> dict[str, Any]:
    assert C_E < 2**41
    assert C_E**2 < 2**82
    assert LAMBDA**2 < 2
    assert GROWTH_A**HALF_LIFE < Q(1, 2)
    assert LAMBDA_BAR**RECOVERY_RANK_SLOPE > 1 / LAMBDA
    assert FAILED_DECIMAL_PREDECESSOR**RECOVERY_RANK_SLOPE <= 1 / LAMBDA

    sample = dyadic_gap_builder(1, 1, Q(1), Q(1, 4), 0, 0)
    return {
        "official_rank_R_input": (
            "for R>=1: Z_(R-1)/mass<=C_e^2*c_g^(-2)*abs(W_tilde)^(-2)*Lambda^(2R); rank zero is assigned to r_base"
        ),
        "official_Euclidean_SYZ_recurrence": (
            "Z_n^E/mass<=(C_p^E/2)*(1+a^n*Z_0^E/mass)"
        ),
        "Euclidean_properness_test": "a^N*(Z_0^E/mass)<1",
        "conditional_recovery_derivation": (
            "after the same-ID density join, apply the pinned Euclidean recurrence to checkrho|V; the dyadic rank input gives Z_0^E/mass<2^(82+2G+2W+R), and a^696<1/2 makes a^N*(Z_0^E/mass)<1 after 696(82+2G+2W+R) recurrence steps"
        ),
        "same_magnet_checkrho_density_join": "NOT_CERTIFIED",
        "why_the_join_is_required": (
            "the official gap carrier checkrho|V has not been identified, with the same ID, with the registered adapted-density cone of ratio at most 2000/1999; only on that cone is the pinned Euclidean SYZ recurrence numerical"
        ),
        "conditional_dyadic_inputs": (
            "c_g>=2^(-G), abs(W_tilde)>=2^(-W), G,W nonnegative integers, plus a same-ID density join supplying a rank-independent total clock debit I_density"
        ),
        "dyadic_initial_Z_exponent": "K+R with K=82+2G+2W",
        "Growth_half_life": HALF_LIFE,
        "Growth_half_life_check": "a^696<1/2",
        "rank_R_recovery_clock": (
            "conditional on the density join: (R-1)+I_density+696*(82+2G+2W+R)=697R+696(82+2G+2W)-1+I_density"
        ),
        "density_recovery_is_rank_independent_intercept": True,
        "recovery_rank_slope": RECOVERY_RANK_SLOPE,
        "exact_algebraic_tail_base": "Lambda^(-1/697)",
        "conditional_candidate_lambda_bar": qstr(LAMBDA_BAR),
        "lambda_bar_exact_check": (
            "(9997/10000)^697>144000/180337=Lambda^(-1)"
        ),
        "decimal_grid_predecessor": qstr(FAILED_DECIMAL_PREDECESSOR),
        "decimal_grid_predecessor_fails": (
            "(2499/2500)^697<=144000/180337"
        ),
        "bad_gap_mass_envelope": (
            "conditional on the same-ID density join: mass(nonproper part at m)<=C_bar*(9997/10000)^m, with C_bar=max(1,C_g'')*(9997/10000)^(-max[696(82+2G+2W)-1+I_density,r_base]); I_density is rank independent and r_base covers rank-zero, top and excess pieces"
        ),
        "proper_part_reparameterisation": (
            "after the independently finite rank-zero/top/excess recovery time, choose r with C_bar*lambda_bar^r<1-zeta; exactly as in SYZ Lemma proper_part, add a suitable portion of already proper mass so the bad part has exact mass C_bar*lambda_bar^m"
        ),
        "official_lambda_equality_claimed": False,
        "safe_replacement_rate_row_status": (
            "CERTIFIED_CONDITIONAL_ON_SAME_MAGNET_DENSITY_JOIN"
        ),
        "official_five_row_lambda_status": "NOT_CERTIFIED",
        "numeric_C_bar": None,
        "numeric_r": None,
        "why_C_bar_and_r_remain_open": (
            "no same-ID checkrho density join or its rank-independent intercept, numerical same-magnet c_g lower, W_tilde length lower, C_g'' upper, zeta lower, or rank-zero/top/excess recovery clock is registered"
        ),
        "arithmetic_sample_not_physical": sample,
    }


def atomized_gap_prefactor() -> dict[str, Any]:
    c_gr = Q(64566981624654 * 10**92, 239122379)
    # Official Cantor/gap proof gives
    # C'_g <= C_gr*tildeC*(1+L0)/(1-Lambda^-1),
    # C_g <= (bar b+11/10)C'_g with bar b<=hat c,
    # and C_g'' <= R_rho*C_g for a density-ratio R_rho curve.
    k_g = (
        DENSITY_RATIO
        * (HAT_C + Q(11, 10))
        * c_gr
        * (1 + L0_UPPER)
        / (1 - 1 / LAMBDA)
    )
    assert k_g == Q(
        2537103957434907110652 * 10**94,
        2481327254508611,
    )
    rows = [
        {
            "id": "tildeC_stable_length",
            "needed": "numeric T>=tildeC in r^s>=tildeC^(-1) inf_n Lambda^n r_(W,n)",
            "value": None,
        },
        {
            "id": "c_g_rank_growth",
            "needed": "numeric G with c_g>=2^-G for the same magnet gap rank",
            "value": None,
        },
        {
            "id": "W_tilde_length",
            "needed": "numeric W with abs(W_tilde)>=2^-W for the same magnet",
            "value": None,
        },
        {
            "id": "same_magnet_density_join",
            "needed": "same-ID identify official checkrho|V with the registered density-ratio <=2000/1999 cone and supply a rank-independent density-recovery intercept",
            "value": None,
        },
        {
            "id": "top_excess_recovery",
            "needed": "numeric rank-zero-gap/top-density/excess-piece properisation clock r_base",
            "value": None,
        },
    ]
    return {
        "numeric_C_gr": qstr(c_gr),
        "maximum_homogeneous_unstable_curve_length_L0_strict_upper": qstr(
            L0_UPPER
        ),
        "official_Cantor_tail_atomisation": (
            "C_g_prime<=C_gr*T*69/(1-Lambda^-1) when tildeC<=T"
        ),
        "official_gap_tail_atomisation": (
            "C_g<=(hat_c+11/10)*C_g_prime because bar_b<=hat_c"
        ),
        "density_conversion": (
            "C_g_double_prime<=(2000/1999)*C_g after the same-magnet density-carrier join"
        ),
        "fully_numeric_multiplier_K_g": qstr(k_g),
        "conditional_prefactor": "C_g_double_prime<=K_g*T",
        "remaining_rows": rows,
        "remaining_rows_sha256": digest(rows),
        "numeric_C_g_double_prime": None,
        "status": "CERTIFIED_EXACT_ATOMISATION__PHYSICAL_INPUT_ROWS_OPEN",
    }


def atlas_eta_lower(
    metric_mode: str, width: Q, jacobian: Q, depth: int, max_source_length: Q
) -> Q:
    if metric_mode not in {"adapted", "euclidean"}:
        raise ValueError("metric mode")
    if width <= 0 or jacobian < 1 or max_source_length <= 0:
        raise ValueError("atlas positive rows")
    if not isinstance(depth, int) or depth < 0:
        raise ValueError("atlas depth")
    factor = Q(1) if metric_mode == "adapted" else EUCLIDEAN_TO_ADAPTED_RELATIVE
    return factor * width / (jacobian**depth * max_source_length)


def interval_atlas_builder() -> dict[str, Any]:
    adapted_sample = atlas_eta_lower(
        "adapted", ETA_THRESHOLD, Q(1), 1, Q(1)
    )
    euclidean_sample_width = ETA_THRESHOLD / EUCLIDEAN_TO_ADAPTED_RELATIVE
    euclidean_sample = atlas_eta_lower(
        "euclidean", euclidean_sample_width, Q(1), 1, Q(1)
    )
    assert adapted_sample == ETA_THRESHOLD
    assert euclidean_sample == ETA_THRESHOLD

    required_rows = [
        "closed rational parameter interval I_j; intervals cover [-1/400,1/400]",
        "same enlarged sufficient-cover target ID inside direct C24",
        "finite source-curve chart cells covering every Euclidean-selected abs(V)>=delta_rect curve",
        "one physical branch word and iterate N_j on every cell",
        "strict singularity/homogeneity clearance throughout I_j and the curve cell",
        "strict target stable-side crossing inequalities with positive transverse width",
        "either all-adapted (w_j,J_j,L_j) or all-Euclidean (w_j,J_j,L_j) length data",
        "rational per-step derivative/distortion upper J_j, hence N_j-step upper J_j^N_j, and source-length upper L_j",
        "parameter persistence verified on the entire interval, not only at its midpoint",
    ]
    return {
        "physical_rows_materialized": 0,
        "parameter_interval_rows_materialized": 0,
        "required_rows": required_rows,
        "required_rows_sha256": digest(required_rows),
        "adapted_mode_formula": "eta_j>=w_j/(J_j^N_j*L_j)",
        "Euclidean_mode_formula": (
            "eta_j^*>=(20/3807)*w_j/(J_j^N_j*L_j)"
        ),
        "why_20_over_3807": (
            "relative line-element conversion=(5/27)/(141/4); it converts both target/source Euclidean relative lengths to adapted relative length"
        ),
        "mixed_metric_rows_accepted": False,
        "uniform_eta_builder": (
            "eta_uniform=min_j eta_j only after exact interval and curve-cell cover checks"
        ),
        "J_j_semantics": (
            "J_j is a per-step derivative/distortion upper on the registered branch cell; J_j^N_j is the certified N_j-step product upper"
        ),
        "safe_target": qstr(ETA_THRESHOLD),
        "conditional_success_test": (
            "eta_uniform>=43008/14285703575"
        ),
        "arithmetic_samples_not_physical": {
            "adapted_exact_threshold": qstr(adapted_sample),
            "Euclidean_sample_width": qstr(euclidean_sample_width),
            "Euclidean_exact_threshold_after_conversion": qstr(euclidean_sample),
        },
        "numeric_uniform_eta_sigma_star": None,
        "numeric_H_cover": None,
        "numeric_beta": None,
        "status": "CERTIFIED_EXECUTABLE_CONDITIONAL_SCHEMA__NO_PHYSICAL_ROWS",
    }


def latest_technology_audit() -> dict[str, Any]:
    rows = [
        {
            "paper": "1210.0011v4",
            "finding": (
                "official Lemmas gap_proper/proper_part expose the rank slope and lambda=Lambda^(-1/c_p) mechanism; their C_e,c_g,C_g'',W_tilde and top constants are not numerical"
            ),
        },
        {
            "paper": "2104.06947v3",
            "finding": (
                "projective cones expose many formulas, but proper crossing still chooses mixing times n_i^* existentially and obtains the uniform block through a qualitative finite compact cover"
            ),
        },
        {
            "paper": "2604.25881v1",
            "finding": (
                "target-sensitive sufficient rectangles remain qualitative; no branch-width, clearance, derivative or parameter-interval registry is published"
            ),
        },
        {
            "paper": "2502.07765v2",
            "finding": (
                "the complex-cone application continues to import existential finite mixing/cone-diameter constants and supplies no pilot interval atlas"
            ),
        },
    ]
    return {
        "metadata_checked_on": "2026-07-20",
        "official_versions": [
            "1210.0011v4",
            "2104.06947v3",
            "2604.25881v1",
            "2502.07765v2",
        ],
        "source_hashes": ARXIV_SOURCE_HASHES,
        "rows": rows,
        "rows_sha256": digest(rows),
        "new_direct_numeric_magnet_or_interval_atlas_theorem_found": False,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "claim_type": (
                "numeric frozen-map Growth lemma, same-density-join-conditional magnet-gap exponential candidate, exact remaining prefactor atomisation, and metric-safe conditional interval-atlas builder"
            ),
            "parameter_scope": "stationary T_sigma for each |sigma|<=1/400",
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
        },
        "new_numeric_growth_lemma": numerical_growth_constants(),
        "conditional_numeric_gap_rate_candidate": numerical_gap_rate(),
        "gap_prefactor_atomisation": atomized_gap_prefactor(),
        "rational_parameter_interval_atlas_builder": interval_atlas_builder(),
        "latest_technology_audit": latest_technology_audit(),
        "corrected_round53_five_row_frontier": {
            "zeta0": None,
            "S": None,
            "R": None,
            "C": None,
            "lambda": None,
            "lambda_conditional_candidate_if_same_magnet_density_join": qstr(
                LAMBDA_BAR
            ),
            "numeric_Delta_upper": None,
            "numeric_H_bump": None,
            "numeric_H_out": None,
            "numeric_eta_sigma_star": None,
            "numeric_H_cover": None,
            "numeric_beta": None,
        },
        "strict_type_separators": {
            "half_life_696_renamed_SYZ_c_p": False,
            "official_lambda_equality_claimed": False,
            "conditional_candidate_written_into_official_lambda_row": False,
            "checkrho_density_join_assumed_unconditionally": False,
            "endpoint_collision_rank_tail_renamed_magnet_gap_rank_tail": False,
            "whole_family_hit_renamed_crossing": False,
            "fixed_sigma_crossing_renamed_parameter_uniform_atlas": False,
            "Euclidean_width_used_without_20_over_3807_conversion": False,
        },
        "strict_nonpromotion": {
            "numeric_safe_gap_rate_base": "NOT_CERTIFIED",
            "conditional_gap_rate_candidate": (
                "CERTIFIED_CONDITIONAL_ON_SAME_MAGNET_DENSITY_JOIN"
            ),
            "same_magnet_density_join": "NOT_CERTIFIED",
            "numeric_gap_prefactor_C": "NOT_CERTIFIED",
            "numeric_gap_or_top_recovery_R": "NOT_CERTIFIED",
            "numeric_zeta0_and_mixing_S": "NOT_CERTIFIED",
            "numeric_Delta_H_bump_H_out": "NOT_CERTIFIED",
            "numeric_uniform_eta_H_cover_beta": "NOT_CERTIFIED",
            "proper_same_ID_return_q_strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = dict(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def manifest() -> dict[str, Any]:
    verifier = HERE / "cm2_gate34_round54_numeric_growth_gap_rate_interval_atlas_frontier_verifier.py"
    if not verifier.is_file():
        raise RuntimeError("missing verifier")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def write_manifest(path: Path) -> None:
    path.write_text(
        json.dumps(manifest(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-manifest", type=Path)
    parser.add_argument("--print-result", action="store_true")
    args = parser.parse_args()
    if args.emit_manifest is not None:
        write_manifest(args.emit_manifest)
        print(f"WROTE {args.emit_manifest}")
        return 0
    if args.print_result:
        print(json.dumps(build_result(), indent=2, sort_keys=True))
        return 0
    print(
        "ROUND54_GATE4_GAP_RATE_CANDIDATE: "
        "CERTIFIED_CONDITIONAL_ON_SAME_MAGNET_DENSITY_JOIN"
    )
    print("ROUND54_GATE4_OFFICIAL_FIVE_ROW_LAMBDA: NOT_CERTIFIED")
    print("ROUND54_GATE4_NUMERIC_C_DELTA_H_COVER: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
