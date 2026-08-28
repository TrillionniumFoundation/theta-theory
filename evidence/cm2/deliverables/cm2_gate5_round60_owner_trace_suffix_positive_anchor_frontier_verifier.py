#!/usr/bin/env python3
"""Fail-closed verifier for the Round-60 Gate-5 frontier leaf."""

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

import cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_cert as cert


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


EXPECTED_PROVENANCE = {
    "dependency_sha256": dict(cert.DEPENDENCIES),
    "old_artifacts_modified": False,
    "parameter_scope": "Round25/50 root audit at s=0; Round42/54 suffix schema for fixed |s|<=1/400; fixed-insertion positive anchors at s=0",
    "claim_type": "exact owner-token crosswalk, owner-trace coverage frontier, active-Abel audit, seven suffix predicate definitions with conditional R on A_col, and fixed-insertion orientation-positive anchors",
}
EXPECTED_CROSSWALK = cert.owner_crosswalk_frontier()
EXPECTED_ABEL = cert.active_abel_audit()
EXPECTED_SUFFIX = cert.suffix_predicate_materialisation()
EXPECTED_HYBRID = cert.hybrid_complement_policy()
EXPECTED_ANCHORS = cert.fixed_time_positive_anchors()
EXPECTED_TECH = cert.technology_audit()
EXPECTED_MATURITY = {
    "previous_global_maturity": "10/18",
    "new_global_field_completed": None,
    "newly_certified_sublayers": [
        "exact Round50-to-Round54 owner-token Borel projection",
        "exact owner-trace bad-set/nullity interface",
        "raw collar Z domination of the optimal clock moment",
        "five previously missing suffix predicate definitions with an exact three-code-map Borel frontier",
        "conditional Borel recovery-capacity construction on A_col",
        "conditional exact A_col-collar plus A_col-complement positive-anchor hybrid iff for supplied Borel R and measurable nonnegative C_bad",
        "fixed-insertion orientation-positive rank/F10 anchors and the exact Jordan-marginal type nonjoin",
    ],
    "reason_no_new_field_credit": "neither pure A_col coverage nor the alternative A_col-complement positive anchor is certified; the active Abel/Orlicz bound is absent; three suffix code maps and every missing universal value remain open; and the fixed-insertion orientation ledgers are not pinned to the weighted Jordan marginals",
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

        cross = result["owner_root_crosswalk_and_coverage_frontier"]
        if cross != EXPECTED_CROSSWALK:
            errors.append("crosswalk section")
        rows = cross["token_rows"]
        if len(rows) != 7 or [r["position"] for r in rows] != list(range(7)):
            errors.append("token positions")
        if any(r["action"] != "retain" for r in rows[:6]) or rows[6]["action"] != "forget_under_pi_50":
            errors.append("token projection")
        if cross["token_rows_sha256"] != cert.digest(rows):
            errors.append("token digest")
        if cross["Round50_to_Round54_same_ID_crosswalk"] != "CERTIFIED_EXACT_BOREL_PROJECTION":
            errors.append("crosswalk status")
        if cross["Round25_to_Round50_exact_root_ID_crosswalk"] != "NOT_MATERIALIZED":
            errors.append("Round25 guard")
        if "N_cut union N_acc" not in cross["regular_bad_partition"] or "nu(N_cut union N_acc)" not in cross["exact_trace_criterion"]:
            errors.append("bad trace partition")
        if cross["physical_A_col_full_coverage"] != "NOT_CERTIFIED":
            errors.append("coverage promotion")

        c = independent_constants()
        if not Decimal("0.4999") < c["gamma"] < Decimal("0.5"):
            errors.append("gamma")
        if not Decimal("1") < c["w"] < Decimal("1.001"):
            errors.append("w_Z")
        if not Decimal("0.0012406563164308641") < c["alpha"] < Decimal("0.0012406563164308642"):
            errors.append("alpha")
        abel = result["active_Abel_Orlicz_physical_audit"]
        if abel != EXPECTED_ABEL:
            errors.append("Abel section")
        beta = c["beta"]
        expected_levels = (0, 1, 2, 16, 4381, 10000)
        if [r["K"] for r in abel["rows"]] != list(expected_levels):
            errors.append("Abel rows levels")
        for row in abel["rows"]:
            k = row["K"]
            r = independent_clock(k, beta)
            if row["r_K"] != r or not c["w"] ** r < Decimal(2) ** (k + 1):
                errors.append("raw collar domination")
                break
        if abel["rows_sha256"] != cert.digest(abel["rows"]):
            errors.append("Abel rows digest")
        if abel["physical_active_Abel_series_finite"] != "NOT_CERTIFIED" or abel["physical_Orlicz_bound"] != "NOT_CERTIFIED":
            errors.append("Abel promotion")

        suffix = result["seven_bit_suffix_Borel_materialisation"]
        if suffix != EXPECTED_SUFFIX:
            errors.append("suffix section")
        bits = suffix["bit_rows"]
        if [b["bit"] for b in bits] != ["L_id", "L_word", "L_input", "L_C24", "L_operator", "L_output", "L_horizon"]:
            errors.append("suffix bit names")
        if any(b["definition_materialized"] is not True for b in bits):
            errors.append("suffix materialisation")
        if [b["universal_value_on_A_col"] for b in bits].count("NOT_CERTIFIED") != 5:
            errors.append("suffix universal values")
        if suffix["bit_rows_sha256"] != cert.digest(bits):
            errors.append("suffix bit digest")
        for sample in suffix["sample_rows"]:
            seq = sample["J_bits"]
            expected_r: int | str = "infinity" if all(seq) else seq.index(0)
            if sample["R"] != expected_r:
                errors.append("R sample")
                break
        if suffix["sample_rows_sha256"] != cert.digest(suffix["sample_rows"]):
            errors.append("R sample digest")
        if [b["Borel_on_frozen_registry"] for b in bits].count("CERTIFIED") != 4:
            errors.append("suffix Borel count")
        if suffix["unconditional_Borel_predicate_count"] != 4 or suffix["conditional_Borel_predicate_count"] != 3:
            errors.append("suffix Borel typing")
        if suffix["Borel_recovery_capacity_R_on_A_col"] != "CONDITIONAL_SCHEMA":
            errors.append("conditional Borel R")
        if suffix["physical_R_at_least_r_K"] != "NOT_CERTIFIED" or suffix["physical_Round54_Round42_operator_join"] != "NOT_CERTIFIED":
            errors.append("physical suffix promotion")
        if "C_policy=infinity on A_col^c" not in suffix["policy_guard"] or "only after testing" not in suffix["policy_guard"]:
            errors.append("policy registry guard")

        hybrid = result["A_col_complement_positive_hybrid_policy"]
        if hybrid != EXPECTED_HYBRID:
            errors.append("hybrid section")
        if len(hybrid["signature_rows"]) != 5 or hybrid["signature_rows_sha256"] != cert.digest(hybrid["signature_rows"]):
            errors.append("hybrid signature rows")
        for token in ("1_Acol", "R>=r_K", "R<r_K", "1_(A_col^c)*C_bad"):
            if token not in hybrid["hybrid_policy_definition"]:
                errors.append("hybrid policy")
                break
        if any(token not in hybrid["exact_positive_iff"] for token in ("recovered-long", "short/misaligned", "A_col^c direct")) or "collision-area nullity" not in hybrid["trace_typing_guard"]:
            errors.append("hybrid iff/typing")
        if len(hybrid["conditional_hypotheses"]) != 2 or "Borel on A_col" not in hybrid["conditional_hypotheses"][0] or "measurable nonnegative" not in hybrid["conditional_hypotheses"][1]:
            errors.append("hybrid conditional hypotheses")
        if hybrid["status"] != "CERTIFIED_CONDITIONAL_EXACT_IFF_ON_ANY_SUPPLIED_BOREL_R_AND_NONNEGATIVE_C_BAD":
            errors.append("hybrid conditional status")
        if hybrid["physical_A_col_complement_positive_anchor"] != "NOT_CERTIFIED" or hybrid["physical_hybrid_policy_finite"] != "NOT_CERTIFIED":
            errors.append("hybrid promotion")

        anchors = result["fixed_insertion_positive_anchor_and_global_frontier"]
        if anchors != EXPECTED_ANCHORS:
            errors.append("anchor section")
        if cert.FORWARD_F10 + cert.REVERSE_F10 != cert.BIDIRECTIONAL_F10:
            errors.append("F10 sum")
        if Q(anchors["rows"][0]["positive_upper"]) != cert.RANK_MOMENT:
            errors.append("orientation rank anchor")
        if Q(anchors["rows"][3]["positive_upper"]) != cert.BIDIRECTIONAL_F10:
            errors.append("F10 anchor")
        if anchors["rows_sha256"] != cert.digest(anchors["rows"]) or anchors["separator_rows_sha256"] != cert.digest(anchors["separator_rows"]):
            errors.append("anchor row digest")
        for key in ("fixed_insertion_orientation_positive_rank_anchor", "fixed_insertion_orientation_positive_F10_anchor", "fixed_marked_unweighted_Jordan_marginal_anchor"):
            if anchors[key] != "CERTIFIED":
                errors.append(f"fixed anchor {key}")
        for key in ("fixed_insertion_weighted_Jordan_variation_anchor", "fixed_insertion_weighted_common_mode_anchor", "global_weighted_Jordan_variation_anchor", "global_weighted_common_mode_anchor", "complete_positive_F10", "strong_cemetery"):
            if anchors[key] != "NOT_CERTIFIED":
                errors.append(f"global anchor {key}")

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
    print("R50_R54_CROSSWALK:", s["Round50_Round54_exact_owner_token_crosswalk"])
    print("A_COL_COVERAGE:", s["physical_A_col_full_coverage"])
    print("BOREL_R_ON_A_COL:", s["Borel_recovery_capacity_R_on_A_col"])
    print("FIXED_INSERTION_ORIENTATION_F10:", s["fixed_insertion_orientation_positive_F10_anchor"])
    print("GATE5_MATURITY:", s["Gate5_maturity"])
    print("CM2:", s["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
