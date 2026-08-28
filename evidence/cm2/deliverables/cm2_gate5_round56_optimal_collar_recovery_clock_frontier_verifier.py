#!/usr/bin/env python3
"""Fail-closed verifier for the Round-56 optimal collar-clock leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round56_optimal_collar_recovery_clock_frontier_cert as cert


HERE = Path(__file__).resolve().parent
BLOCK_DEPTH = 9148
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_safe_local_regular_file(path: Path, base: Path = HERE) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    return path.resolve().parent == base.resolve()


def strict_load(path: Path, base: Path = HERE) -> dict[str, Any]:
    if not is_safe_local_regular_file(path, base):
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def independent_decimals() -> dict[str, Decimal]:
    with localcontext() as context:
        context.prec = 120
        gamma = (
            Decimal(2000)
            / Decimal(1999)
            * Decimal(1 + 48 * BLOCK_DEPTH)
            * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        )
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        weight = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha_old = weight.ln() / Decimal(2).ln()
        alpha_opt = beta * alpha_old
        alpha_sep = Decimal(12408) / Decimal(10**7)
        q_opt = (beta * weight.ln() - alpha_sep * Decimal(2).ln()).exp()
        q_old = (weight.ln() - alpha_sep * Decimal(2).ln()).exp()
        return {
            "gamma": +gamma,
            "rho": +rho,
            "weight": +weight,
            "beta": +beta,
            "alpha_old": +alpha_old,
            "alpha_opt": +alpha_opt,
            "q_opt_separator": +q_opt,
            "q_old_separator": +q_old,
        }


def independent_clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def expected_clock_rows() -> list[dict[str, Any]]:
    dec = independent_decimals()
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4380, 4381, 4382, 8762, 10000):
        r = independent_clock(k, dec["beta"])
        rows.append(
            {
                "level_k": k,
                "Round55_safe_blocks_k_plus_1": k + 1,
                "optimal_blocks_r_k": r,
                "saved_blocks": k + 1 - r,
                "minimality_test": (
                    "gamma^r_k*2^(k+1)<=1<gamma^(r_k-1)*2^(k+1)"
                ),
            }
        )
    return rows


def expected_horizon_rows() -> list[dict[str, Any]]:
    beta = independent_decimals()["beta"]
    rows: list[dict[str, Any]] = []
    for horizon in (0, 1, 4380, 4381, 8761, 10000):
        k_max = int(
            (Decimal(horizon) / beta - Decimal(1)).to_integral_value(
                rounding=ROUND_FLOOR
            )
        )
        rows.append(
            {
                "available_blocks_H": horizon,
                "largest_recovered_level_K_H": k_max,
                "recovered_level_count": max(0, k_max + 1),
                "definition": "K_H=floor(H/beta-1)",
            }
        )
    return rows


def expected_shell_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (2, 4, 8, 16, 64):
        epsilon = Q(1, n**3)
        finite = 2 * n * epsilon
        tail = Q(1, n**2) + epsilon
        rows.append(
            {
                "split_index_n": n,
                "epsilon": str(epsilon),
                "finite_boundary_cover_2n_epsilon": str(finite),
                "accumulating_tail_cover_n_minus_2_plus_epsilon": str(tail),
                "total_displayed_upper": str(finite + tail),
                "four_epsilon_two_thirds_upper": str(Q(4, n**2)),
            }
        )
    return rows


def expected_strict() -> dict[str, Any]:
    return {
        "Round55_k_plus_1_schedule_remains_valid": "CERTIFIED",
        "optimal_exact_gamma_recovery_clock": "CERTIFIED_CONDITIONAL",
        "optimal_clock_pointwise_minimality": "CERTIFIED",
        "strictly_improved_weak_clearance_threshold": "CERTIFIED",
        "optimal_geometric_threshold_sharpness": "CERTIFIED",
        "finite_horizon_mass_remainder": "CERTIFIED_CONDITIONAL",
        "finite_horizon_debt_control_for_alpha_le_1": (
            "FALSE_BY_CERTIFIED_GEOMETRIC_SEPARATOR"
        ),
        "abstract_inverse_square_shell_clearance_tail": "CERTIFIED_CONDITIONAL",
        "physical_same_law_bounded_trace_density": "NOT_CERTIFIED",
        "physical_uniform_full_word_boundary_complexity": "NOT_CERTIFIED",
        "physical_weak_clearance_moment": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_unbounded_compatible_suffix_schedule": "NOT_CERTIFIED",
        "physical_short_horizon_debt_ledger": "NOT_CERTIFIED",
        "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "physical_same_source_pair_rate": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
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


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        provenance = result["provenance"]
        if provenance["dependency_sha256"] != cert.DEPENDENCIES:
            errors.append("provenance dependencies")
        if provenance["old_artifacts_modified"] is not False:
            errors.append("append-only provenance")
        if any(
            token not in provenance["parameter_scope"]
            for token in ("fixed |s|<=1/400", "no moving-map sequence", "no", "physical trace tail")
        ):
            errors.append("parameter scope")
        if any(
            token not in provenance["claim_type"]
            for token in ("pointwise minimal", "sharp", "mass-versus-debt")
        ):
            errors.append("claim scope")

        dec = independent_decimals()
        if not Q(4999, 10000) < GAMMA < Q(1, 2):
            errors.append("exact gamma bracket")
        if not Q(1) < W_Z < Q(2):
            errors.append("exact weight window")
        beta_lower = Decimal(9997717578875635395) / Decimal(10**19)
        beta_upper = Decimal(9997717578875635396) / Decimal(10**19)
        old_lower = Decimal(12409395510954121) / Decimal(10**19)
        old_upper = Decimal(12409395510954122) / Decimal(10**19)
        opt_lower = Decimal(12406563164308641) / Decimal(10**19)
        opt_upper = Decimal(12406563164308642) / Decimal(10**19)
        if not beta_lower < dec["beta"] < beta_upper:
            errors.append("beta bracket arithmetic")
        if not old_lower < dec["alpha_old"] < old_upper:
            errors.append("old alpha bracket arithmetic")
        if not opt_lower < dec["alpha_opt"] < opt_upper:
            errors.append("optimal alpha bracket arithmetic")
        if not Decimal(0) < dec["beta"] < Decimal(1):
            errors.append("beta window")
        if not Decimal(0) < dec["alpha_opt"] < dec["alpha_old"]:
            errors.append("strict alpha improvement")
        if not dec["q_opt_separator"] < Decimal(1) < dec["q_old_separator"]:
            errors.append("separator ratios")

        clock = result["optimal_exact_gamma_recovery_clock"]
        if any(
            token not in clock["frozen_layer_recurrence"]
            for token in ("2^(k+1)*m_k", "gamma", "Z0", "m_(k,r)<=m_k")
        ):
            errors.append("frozen recurrence")
        if any(
            token not in clock["exact_clock_definition"]
            for token in ("min{r>=0", "ceil(beta*(k+1))", "log(1/gamma)")
        ):
            errors.append("clock definition")
        if clock["beta_strict_window"] != "0<beta<1 because 0<gamma<1/2":
            errors.append("beta strict window")
        if clock["beta_rational_bracket"] != (
            "9997717578875635395/10^19 < beta < "
            "9997717578875635396/10^19"
        ):
            errors.append("beta bracket text")
        if clock["beta_decimal_120_digit_audit"] != format(dec["beta"], "f"):
            errors.append("beta decimal replay")
        if clock["gamma_decimal_120_digit_audit"] != format(dec["gamma"], "f"):
            errors.append("gamma decimal replay")
        if clock["gamma_fraction_binary_sha256"] != cert.fraction_digest(GAMMA):
            errors.append("gamma digest")
        if "least integer clock" not in clock["pointwise_minimality"]:
            errors.append("clock minimality statement")
        if any(
            token not in clock["weighted_cost_minimality"]
            for token in ("every w>1", "s_k>=r_k", "levelwise")
        ):
            errors.append("weighted minimality")
        first_saved = int(
            (Decimal(1) / (Decimal(1) - dec["beta"])).to_integral_value(
                rounding=ROUND_CEILING
            )
            - 1
        )
        if first_saved != 4381 or clock["first_level_saving_a_block"] != 4381:
            errors.append("first saved block")
        if clock["first_saving_statement"] != (
            "r_k=k+1 for 0<=k<=4380, while r_4381=4381<4382"
        ):
            errors.append("first saving statement")
        clock_rows = expected_clock_rows()
        if clock["rows"] != clock_rows:
            errors.append("clock rows")
        if clock["rows_sha256"] != cert.digest(clock_rows):
            errors.append("clock rows digest")
        # Check minimality independently in logarithmic coordinates.  This
        # avoids constructing rational powers with hundreds of millions of bits.
        log_inv_gamma = -dec["gamma"].ln()
        log_two = Decimal(2).ln()
        for row in clock_rows:
            k = row["level_k"]
            r = row["optimal_blocks_r_k"]
            target = Decimal(k + 1) * log_two
            if Decimal(r) * log_inv_gamma < target:
                errors.append("clock upper inequality")
                break
            if r > 0 and not Decimal(r - 1) * log_inv_gamma < target:
                errors.append("clock predecessor inequality")
                break
        if clock["status"] != "CERTIFIED_POINTWISE_MINIMAL_EXACT_GAMMA_RECOVERY_CLOCK":
            errors.append("clock status")

        moment = result["sharp_optimal_clock_weighted_moment"]
        if any(
            token not in moment["iterated_recovery"]
            for token in ("gamma^r_k*2^(k+1)*m_k", "C_rec", "Z0/(1-gamma)")
        ):
            errors.append("iterated recovery")
        if moment["optimal_emission_ledger"] != (
            "sum_k w_Z^r_k*z_(k,r_k)<=C_rec*sum_k w_Z^r_k*m_k"
        ):
            errors.append("optimal ledger")
        if any(
            token not in moment["ceiling_comparison"]
            for token in ("w_Z^(beta*(k+1))", "w_Z^r_k", "beta*(k+1)+1")
        ):
            errors.append("ceiling comparison")
        if moment["geometric_tail_model"] != "m_k=C_m*2^(-alpha*k), k>=0":
            errors.append("geometric model")
        if any(
            token not in moment["sharp_geometric_criterion"]
            for token in ("iff", "w_Z^beta*2^(-alpha)<1", "alpha>alpha_opt")
        ):
            errors.append("sharp criterion")
        if moment["optimal_critical_exponent"] != (
            "alpha_opt=beta*log(w_Z)/log(2)"
        ):
            errors.append("optimal exponent")
        if moment["Round55_safe_critical_exponent"] != (
            "alpha_55=log(w_Z)/log(2)"
        ):
            errors.append("old exponent")
        if "beta*alpha_55<alpha_55" not in moment["strict_improvement"]:
            errors.append("strict improvement statement")
        if moment["alpha_opt_decimal_120_digit_audit"] != format(
            dec["alpha_opt"], "f"
        ):
            errors.append("optimal alpha decimal")
        if moment["alpha_55_decimal_120_digit_audit"] != format(
            dec["alpha_old"], "f"
        ):
            errors.append("old alpha decimal")
        separator = moment["strict_separator"]
        if separator["alpha"] != "1551/1250000":
            errors.append("separator alpha")
        if separator["ordering"] != "alpha_opt<alpha=0.0012408<alpha_55":
            errors.append("separator ordering")
        if separator["optimal_ratio_w_beta_2_minus_alpha"] != format(
            dec["q_opt_separator"], "f"
        ):
            errors.append("optimal separator ratio")
        if separator["Round55_ratio_w_2_minus_alpha"] != format(
            dec["q_old_separator"], "f"
        ):
            errors.append("old separator ratio")
        if "optimal clock ledger converges" not in separator["conclusion"]:
            errors.append("separator conclusion")
        if "nondecaying" not in moment["critical_equality_separator"]:
            errors.append("critical equality")
        if "iff alpha>1" not in moment["raw_debt_phase_boundary"]:
            errors.append("raw debt phase")
        if "alpha_opt<alpha<=1" not in moment["strict_delayed_only_region"]:
            errors.append("delayed-only region")
        if moment["status"] != (
            "CERTIFIED_SHARP_OPTIMAL_CLOCK_GEOMETRIC_MOMENT_THRESHOLD"
        ):
            errors.append("moment status")

        horizon = result["finite_horizon_prefix_remainder_frontier"]
        if any(
            token not in horizon["recovered_prefix"]
            for token in ("r_k<=H", "K_H=floor(H/beta-1)")
        ):
            errors.append("horizon prefix")
        horizon_rows = expected_horizon_rows()
        if horizon["rows"] != horizon_rows:
            errors.append("horizon rows")
        if horizon["rows_sha256"] != cert.digest(horizon_rows):
            errors.append("horizon digest")
        if "1-2^(-alpha)" not in horizon["conditional_mass_remainder"]:
            errors.append("mass remainder")
        if "O(2^(-alpha*H/beta))" not in horizon["mass_remainder_rate"]:
            errors.append("mass remainder rate")
        if "alpha>1" not in horizon["debt_remainder_for_alpha_gt_1"]:
            errors.append("strong debt remainder")
        if any(
            token not in horizon["finite_horizon_obstruction_for_alpha_le_1"]
            for token in ("0<alpha<=1", "every finite-H", "is infinite")
        ):
            errors.append("finite horizon obstruction")
        if "cannot be renamed" not in horizon["logical_boundary"]:
            errors.append("mass/debt boundary")
        for key in (
            "physical_unbounded_suffix_horizon",
            "physical_short_horizon_debt_ledger_in_weak_regime",
        ):
            if horizon[key] != "NOT_CERTIFIED":
                errors.append(f"horizon promotion: {key}")
        if horizon["status"] != (
            "CERTIFIED_CONDITIONAL_PREFIX_AND_MASS_REMAINDER_"
            "WITH_SHARP_FINITE_HORIZON_DEBT_OBSTRUCTION"
        ):
            errors.append("horizon status")

        shell = result["inverse_square_shell_clearance_route_audit"]
        if any(
            token not in shell["abstract_shell_model"]
            for token in ("c in [0,1]", "x_k=k^(-2)", "x_infinity=0")
        ):
            errors.append("shell model")
        if any(
            token not in shell["gap_scale"]
            for token in ("(2k+1)", "k^2*(k+1)^2", "Theta(k^-3)")
        ):
            errors.append("shell gap scale")
        if any(
            token not in shell["epsilon_neighbourhood_split"]
            for token in ("ceil(epsilon^(-1/3))", "2*N*epsilon", "N^(-2)+epsilon")
        ):
            errors.append("shell split")
        if "<=6*epsilon^(2/3)" not in shell["Lebesgue_tail_bound"]:
            errors.append("shell Lebesgue bound")
        if "6*D*epsilon^(2/3)" not in shell["bounded_density_consequence"]:
            errors.append("shell density consequence")
        if "D*(6+2J)" not in shell["finite_extra_boundaries"]:
            errors.append("extra boundaries")
        if "2/3>alpha_55>alpha_opt" not in shell[
            "clearance_exponent_comparison"
        ]:
            errors.append("shell exponent comparison")
        shell_rows = expected_shell_rows()
        if shell["sample_rows"] != shell_rows:
            errors.append("shell rows")
        if shell["sample_rows_sha256"] != cert.digest(shell_rows):
            errors.append("shell rows digest")
        for row in shell_rows:
            if Q(row["total_displayed_upper"]) > Q(
                row["four_epsilon_two_thirds_upper"]
            ):
                errors.append("shell row arithmetic")
                break
        binding = shell["physical_binding_audit"]
        if any(
            token not in binding["Round54_trace_law"]
            for token in ("arbitrary finite Borel", "no density")
        ):
            errors.append("physical trace-law blocker")
        if any(
            token not in binding["Round54_clearance_scope"]
            for token in ("singularity", "homogeneity", "owner", "hole")
        ):
            errors.append("physical clearance blocker")
        for key in (
            "missing_same_law_density",
            "missing_uniform_pullback_gap_comparison",
            "missing_uniform_extra_boundary_count_over_owner_records",
            "A_col_positive_or_full_mass",
        ):
            if binding[key] != "NOT_CERTIFIED":
                errors.append(f"shell physical promotion: {key}")
        if "cannot be bound" not in binding["conclusion"]:
            errors.append("shell binding conclusion")
        if shell["status"] != (
            "CERTIFIED_ABSTRACT_INVERSE_SQUARE_SHELL_TWO_THIRDS_TAIL_"
            "PHYSICAL_BINDING_NOT_CERTIFIED"
        ):
            errors.append("shell status")

        maturity = result["Gate5_maturity_update"]
        if maturity["previous_global_maturity"] != "10/18":
            errors.append("previous maturity")
        if maturity["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if len(maturity["newly_certified_sublayers"]) != 5:
            errors.append("sublayer ledger")
        if any(
            token not in maturity["reason_no_new_field_credit"]
            for token in ("physical weak clearance", "same-operator", "suffix", "post-recovery")
        ):
            errors.append("no-credit reason")
        if maturity["current_global_maturity"] != "10/18":
            errors.append("current maturity")
        if maturity["complete_18_field_operator_block_count"] != 0:
            errors.append("complete block promotion")
        if result["strict_nonpromotion"] != expected_strict():
            errors.append("strict nonpromotion")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"malformed result: {exc}")
    return errors


def dependency_integrity_errors(
    dependencies: dict[str, str] | None = None, base: Path = HERE
) -> list[str]:
    selected = cert.DEPENDENCIES if dependencies is None else dependencies
    errors: list[str] = []
    for name, expected_sha in selected.items():
        if Path(name).name != name:
            errors.append(f"unsafe dependency name: {name}")
            continue
        path = base / name
        if not is_safe_local_regular_file(path, base):
            errors.append(f"unsafe or missing dependency: {name}")
            continue
        if sha(path) != expected_sha:
            errors.append(f"dependency hash: {name}")
    return errors


def fast_integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }
    if set(manifest) != expected_keys:
        errors.append("manifest keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependencies")
    errors.extend(dependency_integrity_errors())
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result")
        return errors
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal replay digest")
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict")
    return errors


def verify_object(manifest: dict[str, Any], replay: bool = True) -> list[str]:
    errors = fast_integrity_errors(manifest)
    if not errors:
        errors.extend(direct_errors(manifest["result"]))
    if replay and not errors:
        try:
            replayed = cert.build_result()
        except Exception as exc:
            errors.append(f"dependency replay: {exc}")
        else:
            if manifest["result"] != replayed:
                errors.append("deterministic replay")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def hostile_paths() -> list[tuple[str, ...]]:
    paths: list[tuple[str, ...]] = [
        ("result", "schema"),
        ("result", "provenance", "dependency_sha256"),
        ("result", "provenance", "old_artifacts_modified"),
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "claim_type"),
    ]
    sections = {
        "optimal_exact_gamma_recovery_clock": (
            "frozen_layer_recurrence",
            "exact_clock_definition",
            "beta_strict_window",
            "beta_rational_bracket",
            "beta_decimal_120_digit_audit",
            "gamma_decimal_120_digit_audit",
            "gamma_fraction_binary_sha256",
            "pointwise_minimality",
            "weighted_cost_minimality",
            "first_level_saving_a_block",
            "first_saving_statement",
            "rows",
            "rows_sha256",
            "status",
        ),
        "sharp_optimal_clock_weighted_moment": (
            "iterated_recovery",
            "optimal_emission_ledger",
            "ceiling_comparison",
            "geometric_tail_model",
            "sharp_geometric_criterion",
            "optimal_critical_exponent",
            "Round55_safe_critical_exponent",
            "strict_improvement",
            "alpha_opt_rational_bracket",
            "alpha_55_rational_bracket",
            "alpha_opt_decimal_120_digit_audit",
            "alpha_55_decimal_120_digit_audit",
            "strict_separator",
            "critical_equality_separator",
            "raw_debt_phase_boundary",
            "strict_delayed_only_region",
            "status",
        ),
        "finite_horizon_prefix_remainder_frontier": (
            "recovered_prefix",
            "rows",
            "rows_sha256",
            "conditional_mass_remainder",
            "mass_remainder_rate",
            "debt_remainder_for_alpha_gt_1",
            "finite_horizon_obstruction_for_alpha_le_1",
            "logical_boundary",
            "physical_unbounded_suffix_horizon",
            "physical_short_horizon_debt_ledger_in_weak_regime",
            "status",
        ),
        "inverse_square_shell_clearance_route_audit": (
            "abstract_shell_model",
            "gap_scale",
            "epsilon_neighbourhood_split",
            "Lebesgue_tail_bound",
            "bounded_density_consequence",
            "finite_extra_boundaries",
            "clearance_exponent_comparison",
            "sample_rows",
            "sample_rows_sha256",
            "physical_binding_audit",
            "status",
        ),
        "Gate5_maturity_update": (
            "previous_global_maturity",
            "new_global_field_completed",
            "newly_certified_sublayers",
            "reason_no_new_field_credit",
            "current_global_maturity",
            "complete_18_field_operator_block_count",
        ),
    }
    for section, keys in sections.items():
        paths.extend(("result", section, key) for key in keys)
    paths.extend(("result", "strict_nonpromotion", key) for key in expected_strict())
    return paths


def replacement_for(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "CERTIFIED"
    if isinstance(value, dict):
        return {}
    if isinstance(value, list):
        return []
    return "HOSTILE_MUTATION"


def refresh_result_integrity(mutant: dict[str, Any]) -> None:
    result = mutant["result"]
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = cert.digest(payload)
    mutant["verdict"] = result["strict_nonpromotion"]


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    failures = 0
    total = 0
    for path in hostile_paths():
        total += 1
        mutant = copy.deepcopy(manifest)
        current: Any = mutant
        for key in path:
            current = current[key]
        set_path(mutant, path, replacement_for(current))
        refresh_result_integrity(mutant)
        if not verify_object(mutant, replay=True):
            failures += 1
    for key, replacement in (
        ("schema", "bad.schema"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("verdict", {}),
    ):
        total += 1
        mutant = copy.deepcopy(manifest)
        mutant[key] = replacement
        if not verify_object(mutant, replay=False):
            failures += 1
    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["unexpected_key"] = True
    if not verify_object(mutant, replay=False):
        failures += 1
    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not verify_object(mutant, replay=False):
        failures += 1
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        total += 1
        try:
            json.loads(
                payload,
                object_pairs_hook=cert.strict_object,
                parse_constant=cert.reject_json_constant,
            )
        except ValueError:
            pass
        else:
            failures += 1
    with tempfile.TemporaryDirectory(prefix="cm2-r56-g5-hostile-") as temp_name:
        base = Path(temp_name)
        real_manifest = base / "real-manifest.json"
        real_manifest.write_text("{}\n", encoding="utf-8")
        linked_manifest = base / "linked-manifest.json"
        linked_manifest.symlink_to(real_manifest.name)
        total += 1
        try:
            strict_load(linked_manifest, base=base)
        except RuntimeError:
            pass
        else:
            failures += 1

        dependency = base / "dependency.json"
        dependency.write_bytes(b"frozen dependency\n")
        valid = {dependency.name: sha(dependency)}
        total += 1
        if dependency_integrity_errors(valid, base=base):
            failures += 1

        total += 1
        if not dependency_integrity_errors({"missing.json": "0" * 64}, base=base):
            failures += 1

        total += 1
        if not dependency_integrity_errors(
            {dependency.name: "0" * 64}, base=base
        ):
            failures += 1

        linked_dependency = base / "linked-dependency.json"
        linked_dependency.symlink_to(dependency.name)
        total += 1
        if not dependency_integrity_errors(
            {linked_dependency.name: sha(dependency)}, base=base
        ):
            failures += 1

        total += 1
        if not dependency_integrity_errors(
            {"../outside.json": "0" * 64}, base=base
        ):
            failures += 1
    return total - failures, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--integrity-only", action="store_true")
    actions.add_argument("--replay", action="store_true")
    actions.add_argument("--self-test", action="store_true")
    actions.add_argument("--reemit", action="store_true")
    args = parser.parse_args()
    try:
        manifest = strict_load(args.manifest)
        manifest_path = args.manifest.resolve()
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    replay = args.replay or args.self_test or args.reemit or not args.integrity_only
    errors = verify_object(manifest, replay=replay)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    if args.self_test:
        passed, total = self_test(manifest)
        print(f"HOSTILE_SELF_TEST: {passed}/{total}")
        return 0 if passed == total else 1
    if args.reemit:
        emitted = cert.render_manifest(Path(__file__).resolve())
        if emitted != manifest_path.read_bytes():
            print("FAIL: reemitted manifest is not byte-identical")
            return 1
        print("REEMIT: BYTE_IDENTICAL")
        return 0
    if args.integrity_only:
        print("INTEGRITY_ONLY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    print("SAFE_MANIFEST: PASS")
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
