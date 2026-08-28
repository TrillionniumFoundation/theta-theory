#!/usr/bin/env python3
"""Fail-closed verifier for the Round-59 Gate-5 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round59_unified_clearance_join_jordan_frontier_cert as cert


HERE = Path(__file__).resolve().parent
BLOCK_DEPTH = 9148


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(path: Path, base: Path = HERE) -> bool:
    return path.is_file() and not path.is_symlink() and path.resolve().parent == base.resolve()


def strict_load(path: Path, base: Path = HERE) -> dict[str, Any]:
    if not safe(path, base):
        raise RuntimeError("unsafe manifest")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object, parse_constant=cert.reject_json_constant)
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def independent_constants() -> dict[str, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 120
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK_DEPTH) * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * w.ln() / Decimal(2).ln()
        return {"gamma": +gamma, "rho": +rho, "w": +w, "beta": +beta, "alpha": +alpha}


def independent_clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def expected_active_rows() -> list[dict[str, Any]]:
    beta = independent_constants()["beta"]
    rows = []
    for j in (0, 1, 2, 4378, 4379, 4380, 4381, 4382, 8761, 10000):
        r0, r1 = independent_clock(j, beta), independent_clock(j + 1, beta)
        rows.append({"j": j, "r_j": r0, "r_j_plus_1": r1, "active": r1 == r0 + 1, "Delta_a_j": "(w_Z-1)*w_Z^r_j" if r1 == r0 + 1 else "0"})
    return rows


def expected_join_bits() -> list[dict[str, Any]]:
    return [
        {"bit": "L_id", "meaning": "immutable restriction/owner/event/side/word-cell label retained", "frozen": "CERTIFIED_ROUND54"},
        {"bit": "L_word", "meaning": "one fixed-word collar has constant half-open killed/survivor bit and K_trace=Tr K_word E", "frozen": "CERTIFIED_ROUND54"},
        {"bit": "L_input", "meaning": "the labelled collar family is the exact Round42 canonical-family input domain", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_C24", "meaning": "all 9148 intermediate killed bits equal the Round42 C24 killing policy", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_operator", "meaning": "K_word over the block equals the corresponding positive restriction of O_s^9148", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_output", "meaning": "block output, density and IDs equal the next block input without unregistered recut/renormalisation", "frozen": "NOT_CERTIFIED"},
        {"bit": "L_horizon", "meaning": "the actual owner record selects enough consecutive joined blocks", "frozen": "NOT_CERTIFIED"},
    ]


def expected_jordan_rows() -> list[dict[str, Any]]:
    return [
        {"n": n, "mu_plus_mass": f"2^-{n}", "transport_distance": f"2^-{n}", "positive_charge": f"2^{2*n}", "cost_term": f"2^-{2*n}", "charge_term": f"2^{n}"}
        for n in (1, 2, 4, 8, 16)
    ]


def expected_strict() -> dict[str, Any]:
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


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        p = result["provenance"]
        if p["dependency_sha256"] != cert.DEPENDENCIES:
            errors.append("dependency provenance")
        if p["old_artifacts_modified"] is not False:
            errors.append("append-only")
        if "fixed-|s|<=1/400" not in p["parameter_scope"] or "s=0" not in p["parameter_scope"]:
            errors.append("parameter scope")
        if any(x not in p["claim_type"] for x in ("Kbar", "Round25", "seven-bit", "Jordan")):
            errors.append("claim type")

        c = independent_constants()
        if not Decimal("0.4999") < c["gamma"] < Decimal("0.5"):
            errors.append("gamma")
        if not Decimal("1") < c["w"] < Decimal("1.001"):
            errors.append("weight")
        if not Decimal("0.0012406563164308641") < c["alpha"] < Decimal("0.0012406563164308642"):
            errors.append("alpha")

        u = result["unified_infinite_level_clearance_clock"]
        for token in ("Kbar(a)=K(a)", "Kbar(a)=infinity", "Borel"):
            if token not in u["extended_level"]:
                errors.append("extended level")
                break
        if u["extended_weight"] != "a_k=w_Z^r_k for finite k and a_infinity=infinity":
            errors.append("extended weight")
        if "nu(A_col^c)+" not in u["extended_tail"]:
            errors.append("extended tail")
        if "lim_(j->infinity)Fbar_j=nu(A_col^c)" not in u["coverage_identity"]:
            errors.append("coverage identity")
        for token in ("M_N=", "min(Kbar,N)", "sum_(j=0)^(N-1)"):
            if token not in u["finite_truncation"]:
                errors.append("finite truncation")
                break
        if "lim_N M_N" not in u["monotone_limit"]:
            errors.append("monotone limit")
        if all(token in u["unified_iff"] for token in ("iff", "nu(A_col^c)=0", "w_Z^r_K")) is False:
            errors.append("unified iff")
        if u["active_set"] != "S={j>=0:r_(j+1)=r_j+1}; since 0<beta<1 every increment is zero or one":
            errors.append("active set")
        if "(w_Z-1)*sum_(j in S)w_Z^r_j*Fbar_j" not in u["active_compression"]:
            errors.append("active compression")
        if "single series already forces coverage" not in u["exact_tail_criterion"]:
            errors.append("tail iff")
        if "2^(alpha_opt*j)" not in u["exponential_comparison"]:
            errors.append("exponential comparison")
        rows = expected_active_rows()
        if u["rows"] != rows or u["rows_sha256"] != cert.digest(rows):
            errors.append("active rows")
        if u["physical_finiteness"] != "NOT_CERTIFIED" or u["status"] != "CERTIFIED_UNIFIED_COVERAGE_AND_CLOCK_ABEL_CRITERION":
            errors.append("unified status")

        # Independent finite-truncation Abel replay, including an infinity atom.
        weights = [Q(2), Q(3), Q(3), Q(5), Q(7), Q(7), Q(11)]
        atoms = [(0, Q(1, 10)), (2, Q(2, 10)), (5, Q(3, 10)), (None, Q(4, 10))]
        for N in range(1, 7):
            lhs = sum(weights[N if k is None else min(k, N)] * m for k, m in atoms)
            rhs = weights[0] * sum(m for _, m in atoms)
            for j in range(N):
                tail = sum(m for k, m in atoms if k is None or k > j)
                rhs += (weights[j + 1] - weights[j]) * tail
            if lhs != rhs:
                errors.append("finite Abel replay")
                break
        beta = c["beta"]
        N = 20000
        active_count = sum(independent_clock(j + 1, beta) == independent_clock(j, beta) + 1 for j in range(N))
        if active_count != independent_clock(N, beta) - independent_clock(0, beta):
            errors.append("active density telescoping")

        d = result["sharp_active_Dini_Orlicz_frontier"]
        for token in ("0<c<=w_Z^r_0", "nonnegative", "full-coverage"):
            if token not in d["critical_tail_family"]:
                errors.append("critical family")
                break
        if "c*(w_Z-1)/(j+1)^p" not in d["exact_Dini_reduction"]:
            errors.append("Dini reduction")
        if "iff p>1" not in d["sharp_threshold"] or "p=1" not in d["sharp_threshold"]:
            errors.append("Dini threshold")
        if "asymptotic density beta>0" not in d["why_active_deletion_does_not_change_threshold"]:
            errors.append("active density")
        if "p=1" not in d["pure_critical_envelope_insufficient"]:
            errors.append("critical separator")
        for token in ("1/[100*n*w_Z^r_n]", "B=14", "polynomial", "sum 1/n=infinity"):
            if token not in d["all_polynomial_separator"]:
                errors.append("polynomial separator")
                break
        if "<0.071<1" not in d["separator_mass_guard"]:
            errors.append("mass guard")
        if "R>=r_K" not in d["aligned_join_guard"]:
            errors.append("aligned join guard")
        for token in ("single finite owner law", "convex Phi", "de la Vallee-Poussin", "not a uniform"):
            if token not in d["exact_Orlicz_equivalence"]:
                errors.append("Orlicz equivalence")
                break
        if "Phi(a_(j+1))-Phi(a_j)" not in d["Orlicz_Abel_identity"]:
            errors.append("Orlicz Abel")
        if d["physical_tail_or_Orlicz_bound"] != "NOT_CERTIFIED" or d["status"] != "CERTIFIED_SHARP_ACTIVE_DINI_AND_ORLICZ_FRONTIER":
            errors.append("Dini status")

        r25 = result["Round25_to_A_col_coverage_audit"]
        if "slope gap >50/9" not in r25["tempting_join"]:
            errors.append("Round25 theorem")
        if "do not pin" not in r25["typing_mismatch"]:
            errors.append("root-ID mismatch")
        if "every singularity, homogeneity, owner and hole" not in r25["larger_Round54_distance_ledger"]:
            errors.append("distance ledger")
        if "singular owner-root trace" not in r25["grazing_gap"]:
            errors.append("grazing trace")
        if "N_coinc union N_acc" not in r25["exact_complement_partition"]:
            errors.append("complement partition")
        if "lim_(m->infinity)" not in r25["exact_nullity_ledger"]:
            errors.append("nullity ledger")
        if "owner-trace mass is not frozen" not in r25["ordinary_isolated_subregistry"]:
            errors.append("ordinary subregistry")
        for token in ("logical frozen-field model only", "not a claimed billiard realization", "c=1/n^2", "d_other=0"):
            if token not in r25["sharp_compatible_separator"]:
                errors.append("coverage separator")
                break
        if len(r25["missing_for_full_coverage"]) != 3 or r25["A_col_full_coverage"] != "NOT_CERTIFIED":
            errors.append("coverage missing")
        if r25["status"] != "CERTIFIED_ROUND25_COVERAGE_NONJOIN_AND_GRAZING_SEPARATOR":
            errors.append("coverage status")

        join = result["Round54_Round42_seven_bit_join_frontier"]
        bits = expected_join_bits()
        if join["join_bits"] != bits or join["join_bits_sha256"] != cert.digest(bits):
            errors.append("join bits")
        if [b["frozen"] for b in bits].count("CERTIFIED_ROUND54") != 2 or [b["frozen"] for b in bits].count("NOT_CERTIFIED") != 5:
            errors.append("join bit count")
        if join["block_join"] != "J_b=product of the seven Boolean join bits for block b":
            errors.append("block join")
        if "sup{q>=0" not in join["recovery_capacity"]:
            errors.append("recovery capacity")
        if "countable initial-run" not in join["Borel_future_schema"]:
            errors.append("R Borel")
        if "on A_col recover iff R>=r_K" not in join["compressed_policy"] or "infinite policy cost on A_col^c" not in join["compressed_policy"]:
            errors.append("compressed policy")
        for token in ("nu(A_col^c)=0", "integral_(A_col)", "R>=r_K", "C_rec*w_Z^r_K", "R<r_K", "2^(K+1)", "C_policy=infinity on A_col^c"):
            if token not in join["exact_policy_criterion"]:
                errors.append("policy criterion")
                break
        if "does not select" not in join["registry_guard"] or "disjoint tagged domain" not in join["scalar_guard"]:
            errors.append("join guards")
        if join["physical_recovery_capacity"] != "NOT_CERTIFIED" or join["physical_Round54_Round42_join"] != "NOT_CERTIFIED":
            errors.append("join frontier")
        if join["status"] != "CERTIFIED_SEVEN_BIT_JOIN_AND_MINIMAL_RECOVERY_CAPACITY_SCHEMA":
            errors.append("join status")

        j = result["positive_Jordan_anchor_frontier"]
        if "lambda=mu_plus wedge mu_minus" not in j["measure_lattice"]:
            errors.append("measure lattice")
        if j["exact_Jordan_identity"] != "mu_plus+mu_minus=abs(J)+2*lambda":
            errors.append("Jordan identity")
        if "integral a dabs(J)+2*integral a dlambda" not in j["weighted_identity"]:
            errors.append("weighted identity")
        if "iff both" not in j["minimal_positive_iff"]:
            errors.append("positive iff")
        if "invisible common mode" not in j["why_signed_is_insufficient"]:
            errors.append("common mode")
        if any(token not in j["one_anchor_transport_theorem"] for token in ("integral a dmu_minus", "integral c dpi<infinity", "a(y_plus)<=", "coupling pi")):
            errors.append("anchor theorem")
        if "pointwise charge/transport inequality" not in j["anchor_plus_cost_not_enough"]:
            errors.append("anchor guard")
        for token in ("mu_minus=delta_y0", "cost=sum 4^-n<infinity", "sum 2^n=infinity"):
            if token not in j["sharp_anchor_separator"]:
                errors.append("anchor separator")
                break
        if "mu_plus=mu_minus" not in j["zero_signed_separator"]:
            errors.append("zero separator")
        jr = expected_jordan_rows()
        if j["rows"] != jr or j["rows_sha256"] != cert.digest(jr):
            errors.append("Jordan rows")
        for key in ("physical_weighted_Jordan_variation_anchor", "physical_weighted_common_mode_anchor", "positive_F10", "strong_cemetery"):
            if j[key] != "NOT_CERTIFIED":
                errors.append(f"Jordan frontier {key}")
        if j["status"] != "CERTIFIED_EXACT_JORDAN_COMMON_MODE_ANCHOR_IDENTITY":
            errors.append("Jordan status")
        # Independent atomic measure-lattice replay.
        plus = [Q(3), Q(1), Q(5), Q(0)]
        minus = [Q(1), Q(4), Q(2), Q(2)]
        charge = [Q(2), Q(3), Q(5), Q(7)]
        lam = [min(x, y) for x, y in zip(plus, minus)]
        lhs = sum(a * (x + y) for a, x, y in zip(charge, plus, minus))
        rhs = sum(a * (abs(x - y) + 2 * z) for a, x, y, z in zip(charge, plus, minus, lam))
        if lhs != rhs:
            errors.append("Jordan arithmetic")

        tech = result["latest_technology_audit"]
        if tech["query_date"] != "2026-07-20" or tech["official_source"] != "export.arxiv.org API":
            errors.append("tech provenance")
        if [x["id"] for x in tech["checked"]] != ["2606.10155v1", "2606.19621v2"]:
            errors.append("tech records")
        if "owner-clearance tail" not in tech["finding"] or tech["external_dependency_imported"] is not False:
            errors.append("tech finding")
        if tech["status"] != "CHECKED_NO_DIRECT_PHYSICAL_GATE5_INTERFACE":
            errors.append("tech status")

        m = result["Gate5_maturity_update"]
        if m["previous_global_maturity"] != "10/18" or m["current_global_maturity"] != "10/18" or m["new_global_field_completed"] is not None:
            errors.append("maturity")
        if len(m["newly_certified_sublayers"]) != 6 or m["complete_18_field_operator_block_count"] != 0:
            errors.append("maturity sublayers")
        for token in ("NOT_CERTIFIED", "coverage", "operator bits", "anchor"):
            if token not in m["reason_no_new_field_credit"]:
                errors.append("maturity reason")
                break
        if result["strict_nonpromotion"] != expected_strict():
            errors.append("strict frontier")
        replay = copy.deepcopy(result)
        claimed = replay.pop("internal_replay_digest")
        if claimed != cert.digest(replay):
            errors.append("internal digest")
    except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
        errors.append(f"malformed result: {exc}")
    return errors


def integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if manifest["schema"] != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if manifest["certificate_sha256"] != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest["verifier_sha256"] != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("dependencies")
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not safe(path) or sha(path) != expected:
                errors.append(f"dependency {name}")
        if manifest["verdict"] != manifest["result"]["strict_nonpromotion"]:
            errors.append("verdict")
        errors.extend(direct_errors(manifest["result"]))
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"malformed manifest: {exc}")
    return errors


def replay_errors(manifest: dict[str, Any]) -> list[str]:
    errors = integrity_errors(manifest)
    try:
        if manifest["result"] != cert.build_result():
            errors.append("deterministic result replay")
    except Exception as exc:
        errors.append(f"replay exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    node: Any = value
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement


def redigest(result: dict[str, Any]) -> None:
    core = copy.deepcopy(result)
    core.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = cert.digest(core)


def semantic_mutations() -> list[tuple[tuple[str, ...], Any]]:
    return [
        (("schema",), "bad"),
        (("provenance", "dependency_sha256"), {}),
        (("provenance", "old_artifacts_modified"), True),
        (("provenance", "parameter_scope"), "global"),
        (("provenance", "claim_type"), "promotion"),
        (("unified_infinite_level_clearance_clock", "extended_level"), "K finite"),
        (("unified_infinite_level_clearance_clock", "extended_weight"), "a=1"),
        (("unified_infinite_level_clearance_clock", "extended_tail"), "F=0"),
        (("unified_infinite_level_clearance_clock", "coverage_identity"), "automatic"),
        (("unified_infinite_level_clearance_clock", "finite_truncation"), "false"),
        (("unified_infinite_level_clearance_clock", "monotone_limit"), "finite"),
        (("unified_infinite_level_clearance_clock", "unified_iff"), "coverage only"),
        (("unified_infinite_level_clearance_clock", "active_set"), "all j"),
        (("unified_infinite_level_clearance_clock", "active_compression"), "no increment"),
        (("unified_infinite_level_clearance_clock", "exact_tail_criterion"), "pointwise"),
        (("unified_infinite_level_clearance_clock", "exponential_comparison"), "polynomial"),
        (("unified_infinite_level_clearance_clock", "physical_finiteness"), "CERTIFIED"),
        (("unified_infinite_level_clearance_clock", "rows"), []),
        (("unified_infinite_level_clearance_clock", "rows_sha256"), "0" * 64),
        (("unified_infinite_level_clearance_clock", "status"), "PROMOTED"),
        (("sharp_active_Dini_Orlicz_frontier", "critical_tail_family"), "signed"),
        (("sharp_active_Dini_Orlicz_frontier", "exact_Dini_reduction"), "zero"),
        (("sharp_active_Dini_Orlicz_frontier", "sharp_threshold"), "p>0"),
        (("sharp_active_Dini_Orlicz_frontier", "why_active_deletion_does_not_change_threshold"), "density zero"),
        (("sharp_active_Dini_Orlicz_frontier", "pure_critical_envelope_insufficient"), "sufficient"),
        (("sharp_active_Dini_Orlicz_frontier", "all_polynomial_separator"), "finite clock"),
        (("sharp_active_Dini_Orlicz_frontier", "separator_mass_guard"), "mass>1"),
        (("sharp_active_Dini_Orlicz_frontier", "aligned_join_guard"), "join pays tail"),
        (("sharp_active_Dini_Orlicz_frontier", "exact_Orlicz_equivalence"), "uniform theorem"),
        (("sharp_active_Dini_Orlicz_frontier", "Orlicz_Abel_identity"), "false"),
        (("sharp_active_Dini_Orlicz_frontier", "physical_tail_or_Orlicz_bound"), "CERTIFIED"),
        (("sharp_active_Dini_Orlicz_frontier", "status"), "PROMOTED"),
        (("Round25_to_A_col_coverage_audit", "tempting_join"), "none"),
        (("Round25_to_A_col_coverage_audit", "typing_mismatch"), "same ID"),
        (("Round25_to_A_col_coverage_audit", "larger_Round54_distance_ledger"), "physical only"),
        (("Round25_to_A_col_coverage_audit", "grazing_gap"), "area null implies trace null"),
        (("Round25_to_A_col_coverage_audit", "exact_complement_partition"), "empty"),
        (("Round25_to_A_col_coverage_audit", "exact_nullity_ledger"), "zero"),
        (("Round25_to_A_col_coverage_audit", "ordinary_isolated_subregistry"), "full mass"),
        (("Round25_to_A_col_coverage_audit", "sharp_compatible_separator"), "physical example"),
        (("Round25_to_A_col_coverage_audit", "missing_for_full_coverage"), []),
        (("Round25_to_A_col_coverage_audit", "A_col_full_coverage"), "CERTIFIED"),
        (("Round25_to_A_col_coverage_audit", "status"), "PROMOTED"),
        (("Round54_Round42_seven_bit_join_frontier", "join_bits"), []),
        (("Round54_Round42_seven_bit_join_frontier", "join_bits_sha256"), "0" * 64),
        (("Round54_Round42_seven_bit_join_frontier", "block_join"), "J=1"),
        (("Round54_Round42_seven_bit_join_frontier", "recovery_capacity"), "infinity"),
        (("Round54_Round42_seven_bit_join_frontier", "Borel_future_schema"), "automatic"),
        (("Round54_Round42_seven_bit_join_frontier", "compressed_policy"), "recover always"),
        (("Round54_Round42_seven_bit_join_frontier", "exact_policy_criterion"), "signed"),
        (("Round54_Round42_seven_bit_join_frontier", "registry_guard"), "registry selects"),
        (("Round54_Round42_seven_bit_join_frontier", "scalar_guard"), "constants compose"),
        (("Round54_Round42_seven_bit_join_frontier", "physical_recovery_capacity"), "CERTIFIED"),
        (("Round54_Round42_seven_bit_join_frontier", "physical_Round54_Round42_join"), "CERTIFIED"),
        (("Round54_Round42_seven_bit_join_frontier", "status"), "PROMOTED"),
        (("positive_Jordan_anchor_frontier", "measure_lattice"), "none"),
        (("positive_Jordan_anchor_frontier", "exact_Jordan_identity"), "mu+=J"),
        (("positive_Jordan_anchor_frontier", "weighted_identity"), "signed"),
        (("positive_Jordan_anchor_frontier", "minimal_positive_iff"), "one anchor"),
        (("positive_Jordan_anchor_frontier", "why_signed_is_insufficient"), "sufficient"),
        (("positive_Jordan_anchor_frontier", "one_anchor_transport_theorem"), "no coupling"),
        (("positive_Jordan_anchor_frontier", "anchor_plus_cost_not_enough"), "enough"),
        (("positive_Jordan_anchor_frontier", "sharp_anchor_separator"), "finite charge"),
        (("positive_Jordan_anchor_frontier", "zero_signed_separator"), "J nonzero"),
        (("positive_Jordan_anchor_frontier", "rows"), []),
        (("positive_Jordan_anchor_frontier", "rows_sha256"), "0" * 64),
        (("positive_Jordan_anchor_frontier", "physical_weighted_Jordan_variation_anchor"), "CERTIFIED"),
        (("positive_Jordan_anchor_frontier", "physical_weighted_common_mode_anchor"), "CERTIFIED"),
        (("positive_Jordan_anchor_frontier", "positive_F10"), "CERTIFIED"),
        (("positive_Jordan_anchor_frontier", "strong_cemetery"), "CERTIFIED"),
        (("positive_Jordan_anchor_frontier", "status"), "PROMOTED"),
        (("latest_technology_audit", "query_date"), "2020"),
        (("latest_technology_audit", "official_source"), "blog"),
        (("latest_technology_audit", "checked"), []),
        (("latest_technology_audit", "finding"), "direct theorem"),
        (("latest_technology_audit", "external_dependency_imported"), True),
        (("latest_technology_audit", "status"), "IMPORTED"),
        (("Gate5_maturity_update", "previous_global_maturity"), "18/18"),
        (("Gate5_maturity_update", "new_global_field_completed"), "F10"),
        (("Gate5_maturity_update", "newly_certified_sublayers"), []),
        (("Gate5_maturity_update", "reason_no_new_field_credit"), "complete"),
        (("Gate5_maturity_update", "current_global_maturity"), "11/18"),
        (("Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("strict_nonpromotion", "physical_A_col_full_coverage"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_same_law_clock_moment_finite"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_Round54_to_Round42_same_operator_join"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_weighted_common_mode_anchor"), "CERTIFIED"),
        (("strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate5_maturity"), "18/18"),
        (("strict_nonpromotion", "complete_18_field_operator_block_count"), 1),
        (("strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("strict_nonpromotion", "CM2"), "GO"),
    ]


def run_self_test() -> tuple[int, list[str]]:
    base = cert.build_result()
    tests = semantic_mutations()
    failures: list[str] = []
    for i, (path, replacement) in enumerate(tests):
        mutated = copy.deepcopy(base)
        set_path(mutated, path, replacement)
        redigest(mutated)
        if not direct_errors(mutated):
            failures.append(f"semantic mutation {i}: {'/'.join(path)}")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        duplicate = root / "dup.json"
        nonfinite = root / "nan.json"
        duplicate.write_text('{"x":1,"x":2}\n', encoding="utf-8")
        nonfinite.write_text('{"x":NaN}\n', encoding="utf-8")
        for label, path in (("duplicate", duplicate), ("nonfinite", nonfinite)):
            try:
                json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object, parse_constant=cert.reject_json_constant)
                failures.append(f"strict JSON {label}")
            except ValueError:
                pass
    return len(tests) + 2, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--integrity-only", action="store_true")
    group.add_argument("--replay", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    if args.self_test:
        total, failures = run_self_test()
        if failures:
            print("HOSTILE_MUTATIONS: FAIL")
            print("\n".join(failures))
            return 1
        print(f"HOSTILE_MUTATIONS: {total}/{total} rejected")
        return 0
    if args.reemit:
        try:
            args.reemit.write_bytes(cert.render_manifest(Path(__file__).resolve()))
        except Exception as exc:
            print(f"REEMIT: FAIL: {exc}")
            return 1
        print(f"REEMIT: wrote {args.reemit}")
        return 0
    try:
        manifest = strict_load(args.manifest)
    except Exception as exc:
        print(f"LOAD: FAIL: {exc}")
        return 1
    errors = replay_errors(manifest) if args.replay else integrity_errors(manifest)
    if errors:
        print("VERIFY: FAIL")
        print("\n".join(errors))
        return 1
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    s = manifest["verdict"]
    print("VERIFY: PASS")
    print("UNIFIED_ABEL:", s["unified_coverage_clock_Abel_criterion"])
    print("PHYSICAL_CLOCK_FINITE:", s["physical_same_law_clock_moment_finite"])
    print("GATE5_MATURITY:", s["Gate5_maturity"])
    print("CM2:", s["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
