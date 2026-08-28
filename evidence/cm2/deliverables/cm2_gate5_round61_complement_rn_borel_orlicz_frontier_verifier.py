#!/usr/bin/env python3
"""Fail-closed verifier for the Round-61 Gate-5 frontier leaf."""

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

import cm2_gate5_round61_complement_rn_borel_orlicz_frontier_cert as cert


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
        ctx.prec = 140
        gamma = Decimal(2000) / Decimal(1999) * Decimal(1 + 48 * BLOCK_DEPTH) * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * w.ln() / Decimal(2).ln()
        q_col = Decimal(1) / alpha
        return {"gamma": +gamma, "rho": +rho, "w": +w, "beta": +beta, "alpha": +alpha, "q_col": +q_col}


def independent_clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


EXPECTED_PROVENANCE = {
    "dependency_sha256": dict(cert.DEPENDENCIES),
    "Round60_aggregate_artifact_sha256": dict(cert.ROUND60_AGGREGATE_PINS),
    "old_artifacts_modified": False,
    "parameter_scope": "base s=0 for the actual fixed-insertion owner/F10 law; |s|<=1/400 only for the already-declared suffix code schema",
    "claim_type": "actual fixed-j owner-complement RN anchors, common standard-Borel suffix code maps, exact fixed-j hybrid typing, and same-law raw-collar power-Orlicz equivalence",
}
EXPECTED_OWNER = cert.owner_complement_rn_anchor()
EXPECTED_ORLICZ = cert.power_orlicz_frontier()
EXPECTED_SUFFIX = cert.suffix_code_materialisation()
EXPECTED_HYBRID = cert.fixed_j_hybrid()
EXPECTED_JORDAN = cert.jordan_and_all_time_frontier()
EXPECTED_TECH = cert.technology_audit()
EXPECTED_MATURITY = {
    "previous_global_maturity": "10/18",
    "new_global_field_completed": None,
    "newly_certified_sublayers": [
        "actual fixed-insertion Round52-to-Round54 owner-law pushforward and A_col-complement Borel submeasure",
        "same-law L1 RN densities for fixed-insertion forward/reverse/bidirectional positive F10 costs",
        "fixed-insertion charge-preserving labelled complement cemetery pushforward",
        "common standard-Borel input/kernel/output codes making all seven suffix predicates and R Borel",
        "exact fixed-insertion hybrid with a finite complement term",
        "same-owner-law raw-collar and explicit power-Orlicz exact equivalence",
    ],
    "reason_no_new_field_credit": "the complement trace value/nullity, both collar integrals, active Abel/raw-Z/Orlicz finiteness, five universal suffix values, R>=r_K, all-insertion decay, Jordan joins and strong cemetery remain open",
    "current_global_maturity": "10/18",
    "complete_18_field_operator_block_count": 0,
}
EXPECTED_STRICT = cert.strict_nonpromotion()


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        if result["provenance"] != EXPECTED_PROVENANCE:
            errors.append("provenance")

        owner = result["actual_owner_complement_RN_anchor"]
        if owner != EXPECTED_OWNER:
            errors.append("owner RN section")
        if "m_j^own" not in owner["fixed_insertion_scope"] or "no sum over j" not in owner["fixed_insertion_scope"]:
            errors.append("fixed insertion scope")
        if "nu_j=(q_j)_#m_j^own" not in owner["actual_owner_law_construction"]:
            errors.append("actual owner pushforward")
        if "same actual pushforward" not in owner["same_law_guard"]:
            errors.append("same-law guard")
        if "N_cut disjoint_union N_acc" not in owner["bad_set_partition"]:
            errors.append("bad partition")
        if "d xi_j^bi/dnu_j" not in owner["RN_costs"] or "L1(nu_j^bad)" not in owner["mass_anchor"]:
            errors.append("RN/L1 construction")
        bounds = owner["L1_bounds"]
        if Q(bounds["mass_strict_upper"]) != cert.COAREA_MASS or Q(bounds["forward_F10_strict_upper"]) != cert.FORWARD_F10 or Q(bounds["reverse_F10_strict_upper"]) != cert.REVERSE_F10 or Q(bounds["bidirectional_F10_strict_upper"]) != cert.BIDIRECTIONAL_F10:
            errors.append("RN constants")
        if cert.FORWARD_F10 + cert.REVERSE_F10 != cert.BIDIRECTIONAL_F10:
            errors.append("F10 arithmetic")
        if owner["signature_rows_sha256"] != cert.digest(owner["signature_rows"]):
            errors.append("signature digest")
        for key in ("fixed_insertion_same_law_positive_complement_mass_anchor", "fixed_insertion_same_law_positive_complement_F10_anchor"):
            if owner[key] != "CERTIFIED":
                errors.append(key)
        if owner["fixed_insertion_labelled_cemetery_pushforward"] != "CERTIFIED_CHARGE_PRESERVING":
            errors.append("cemetery pushforward")
        if "continuous endpoint/root" not in owner["cemetery_pushforward"] or "fixed-j marked mass" not in owner["cemetery_pushforward"] or "not a strong trace" not in owner["cemetery_scope_guard"]:
            errors.append("continuous cemetery label/scope")
        for key in ("physical_trace_value_or_nullity", "physical_A_col_full_coverage", "all_insertion_time_positive_complement_anchor", "strong_cemetery"):
            if owner[key] != "NOT_CERTIFIED":
                errors.append(f"owner promotion {key}")

        c = independent_constants()
        if not Decimal("0.4999") < c["gamma"] < Decimal("0.5"):
            errors.append("gamma")
        if not Decimal("0.0012406563164308641") < c["alpha"] < Decimal("0.0012406563164308642"):
            errors.append("alpha")
        if not Decimal(800) < c["q_col"] < Decimal(810):
            errors.append("q_col")
        orlicz = result["same_law_power_Orlicz_frontier"]
        if orlicz != EXPECTED_ORLICZ:
            errors.append("Orlicz section")
        for row in orlicz["rows"]:
            k = row["K"]
            r = independent_clock(k, c["beta"])
            y = c["w"] ** r
            phi = y ** c["q_col"]
            raw = Decimal(2) ** (k + 1)
            if row["r_K"] != r or not raw <= phi < (c["w"] ** c["q_col"]) * raw:
                errors.append("Orlicz pointwise bound")
                break
        if orlicz["rows_sha256"] != cert.digest(orlicz["rows"]):
            errors.append("Orlicz digest")
        if "same actual nu_j" not in orlicz["same_law_scope"] or orlicz["explicit_physical_power_Orlicz_criterion"] != "CERTIFIED_EXACT_SAME_LAW_IFF":
            errors.append("Orlicz same-law typing")
        for key in ("physical_active_Abel_series_finite", "physical_raw_Z_col_finite", "physical_power_Orlicz_bound"):
            if orlicz[key] != "NOT_CERTIFIED":
                errors.append(f"Orlicz promotion {key}")

        suffix = result["seven_bit_common_Borel_code_materialisation"]
        if suffix != EXPECTED_SUFFIX:
            errors.append("suffix section")
        bits = suffix["bit_rows"]
        names = ["L_id", "L_word", "L_input", "L_C24", "L_operator", "L_output", "L_horizon"]
        if [row["bit"] for row in bits] != names or any(row["Borel"] != "CERTIFIED" for row in bits):
            errors.append("seven Borel bits")
        if [row["universal_value"] for row in bits].count("NOT_CERTIFIED") != 5:
            errors.append("five open values")
        if suffix["unconditional_Borel_predicate_count"] != 7 or suffix["conditional_Borel_predicate_count"] != 0:
            errors.append("Borel counts")
        for token in ("standard Borel", "countable algebra D_m", "SubProb(X)"):
            blob = suffix["actual_record_space"] + suffix["state_and_kernel_spaces"] + suffix["countable_separating_generator"]
            if token not in blob:
                errors.append(f"code space {token}")
        if "rather than a countable atom list" not in suffix["state_and_kernel_spaces"] or "injective" not in suffix["countable_separating_generator"] or "equivalent to kernel equality" not in suffix["countable_separating_generator"]:
            errors.append("separating generator injectivity")
        if "sentinel" not in suffix["input_code_map"] or "sentinel" not in suffix["next_input_code_map"]:
            errors.append("total code maps")
        if suffix["bit_rows_sha256"] != cert.digest(bits):
            errors.append("bit digest")
        for sample in suffix["sample_rows"]:
            seq = sample["J_bits"]
            expected: int | str = "infinity" if all(seq) else seq.index(0)
            if sample["R"] != expected:
                errors.append("R samples")
                break
        if suffix["sample_rows_sha256"] != cert.digest(suffix["sample_rows"]):
            errors.append("R digest")
        if suffix["Borel_recovery_capacity_R_on_A_col"] != "CERTIFIED" or suffix["physical_R_at_least_r_K"] != "NOT_CERTIFIED":
            errors.append("R typing/value")

        hybrid = result["fixed_insertion_positive_hybrid"]
        if hybrid != EXPECTED_HYBRID:
            errors.append("hybrid section")
        for token in ("1_Acol", "R>=r_K", "R<r_K", "A_col^c", "C_bad,j^bi"):
            if token not in hybrid["policy"]:
                errors.append(f"hybrid policy {token}")
        if hybrid["complement_term"] != "CERTIFIED_FINITE_AT_FIXED_J" or hybrid["full_fixed_j_policy_finite"] != "NOT_CERTIFIED" or hybrid["all_insertion_assembly"].startswith("NOT_CERTIFIED") is not True:
            errors.append("hybrid strict boundary")

        jordan = result["Jordan_and_all_time_positive_frontier"]
        if jordan != EXPECTED_JORDAN:
            errors.append("Jordan section")
        if "are not Round54 Jordan" not in jordan["type_guard"] or "iff both" not in jordan["all_time_exact_criterion"]:
            errors.append("Jordan type/criterion")
        if jordan["rows_sha256"] != cert.digest(jordan["rows"]):
            errors.append("Jordan digest")
        for key in ("fixed_insertion_weighted_Jordan_variation_anchor", "fixed_insertion_weighted_common_mode_anchor", "all_time_weighted_Jordan_variation_anchor", "all_time_weighted_common_mode_anchor", "all_time_weighted_complement_anchor", "complete_positive_F10", "strong_cemetery"):
            if jordan[key] != "NOT_CERTIFIED":
                errors.append(f"Jordan promotion {key}")

        tech = result["latest_technology_audit"]
        if tech != EXPECTED_TECH or tech["external_dependency_imported"] is not False:
            errors.append("technology audit")
        if result["Gate5_maturity_update"] != EXPECTED_MATURITY:
            errors.append("maturity update")
        if result["strict_nonpromotion"] != EXPECTED_STRICT:
            errors.append("strict frontier")
        core = copy.deepcopy(result)
        claimed = core.pop("internal_replay_digest")
        if claimed != cert.digest(core):
            errors.append("internal digest")
    except (KeyError, IndexError, TypeError, ValueError, ArithmeticError) as exc:
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
        if manifest["dependencies"] != cert.DEPENDENCIES or manifest["Round60_aggregate_artifact_sha256"] != cert.ROUND60_AGGREGATE_PINS:
            errors.append("dependency declarations")
        for name, expected in {**cert.DEPENDENCIES, **cert.ROUND60_AGGREGATE_PINS}.items():
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


PathKey = str | int


def leaf_paths(value: Any, prefix: tuple[PathKey, ...] = ()) -> list[tuple[PathKey, ...]]:
    out: list[tuple[PathKey, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "internal_replay_digest":
                continue
            out.extend(leaf_paths(child, prefix + (key,)))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            out.extend(leaf_paths(child, prefix + (i,)))
    else:
        out.append(prefix)
    return out


def get_path(value: Any, path: tuple[PathKey, ...]) -> Any:
    node = value
    for key in path:
        node = node[key]
    return node


def set_path(value: Any, path: tuple[PathKey, ...], replacement: Any) -> None:
    node = value
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement


def hostile_replacement(value: Any) -> Any:
    if value is None:
        return "MUTATED_NONE"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__MUTATED"
    raise TypeError(type(value))


def redigest(result: dict[str, Any]) -> None:
    core = copy.deepcopy(result)
    core.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = cert.digest(core)


def run_self_test() -> tuple[int, list[str]]:
    base = cert.build_result()
    paths = leaf_paths(base)
    failures: list[str] = []
    for i, path in enumerate(paths):
        mutated = copy.deepcopy(base)
        set_path(mutated, path, hostile_replacement(get_path(mutated, path)))
        redigest(mutated)
        if not direct_errors(mutated):
            failures.append(f"semantic mutation {i}: {'/'.join(map(str, path))}")
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
    return len(paths) + 2, failures


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
    print("FIXED_J_COMPLEMENT_F10:", s["fixed_insertion_same_law_positive_complement_F10_anchor"])
    print("SUFFIX_BOREL:", s["all_seven_suffix_predicates_Borel"])
    print("ORLICZ_CRITERION:", s["explicit_same_law_power_Orlicz_criterion"])
    print("GATE5_MATURITY:", s["Gate5_maturity"])
    print("CM2:", s["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
