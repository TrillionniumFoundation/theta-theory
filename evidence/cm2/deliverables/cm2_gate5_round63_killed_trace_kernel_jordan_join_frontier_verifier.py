#!/usr/bin/env python3
"""Fail-closed verifier for the Round-63 Gate-5 frontier leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round63_killed_trace_kernel_jordan_join_frontier_cert as cert


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(path: Path, base: Path = HERE) -> bool:
    return path.is_file() and not path.is_symlink() and path.resolve().parent == base.resolve()


def strict_load(path: Path) -> dict[str, Any]:
    if not safe(path):
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


EXPECTED_PROVENANCE = {
    "dependency_sha256": dict(cert.DEPENDENCIES),
    "Round62_artifact_sha256": dict(cert.ROUND62_PINS),
    "old_artifacts_modified": False,
    "parameter_scope": "base s=0 actual fixed-j owner laws; all-time kernel theorem is exact conditional and separators are logical positive models, not a new billiard realization",
    "claim_type": "killed trace-kernel drift interface, actual fixed-j orientation-cost Jordan join, and complement zero/small-gap frontier",
}


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        if result["provenance"] != EXPECTED_PROVENANCE:
            errors.append("provenance")
        expected_sections = {
            "killed_trace_kernel_frontier": cert.killed_trace_kernel_frontier(),
            "fixed_j_orientation_cost_Jordan": cert.fixed_j_orientation_cost_jordan(),
            "complement_strata_frontier": cert.complement_strata_frontier(),
            "suffix_clearance_frontier": cert.suffix_clearance_frontier(),
            "latest_technology_audit": cert.technology_audit(),
            "Gate5_maturity_update": cert.maturity_update(),
            "strict_nonpromotion": cert.strict_nonpromotion(),
        }
        for key, expected in expected_sections.items():
            if result[key] != expected:
                errors.append(key)

        kernel = result["killed_trace_kernel_frontier"]
        if "disjoint_union" not in kernel["time_labelled_carrier"] or "never quotients" not in kernel["time_labelled_carrier"]:
            errors.append("time-label guard")
        if "Lambda_(j+1)<=Lambda_j K_j" not in kernel["positive_law"]:
            errors.append("positive recurrence")
        if "w_Z*kappa<1" not in kernel["weighted_conclusion"] or "1-w_Z*kappa" not in kernel["weighted_conclusion"]:
            errors.append("weighted conclusion")
        if kernel["replay_rows_sha256"] != cert.digest(kernel["replay_rows"]):
            errors.append("kernel rows digest")
        expected_rows = cert.killed_kernel_rows()
        if kernel["replay_rows"] != expected_rows:
            errors.append("kernel rows")
        ratios = [Q(row["ratio"]) for row in kernel["replay_rows"]]
        if not (ratios[0] < 1 and ratios[1] == 1 and ratios[2] > 1):
            errors.append("sharp threshold replay")
        for row in kernel["replay_rows"]:
            ratio = Q(row["ratio"])
            n = row["N"]
            partial = sum((ratio**j for j in range(n + 1)), Q(0))
            if Q(row["partial_sum"]) != partial or row["finite_geometric_criterion"] is not (ratio < 1):
                errors.append("geometric partial replay")
                break
        for key in ("actual_K_j", "actual_V_j", "actual_kappa_below_threshold"):
            if kernel[key] != "NOT_CERTIFIED":
                errors.append(f"kernel promotion {key}")

        jordan = result["fixed_j_orientation_cost_Jordan"]
        if Q(jordan["forward_strict_upper"]) + Q(jordan["reverse_strict_upper"]) != Q(jordan["bidirectional_strict_upper"]):
            errors.append("F10 rational sum")
        if jordan["exact_sum_check"] is not True or "|J_j^cost|+2" not in jordan["lattice_identity"]:
            errors.append("cost Jordan identity")
        if Q(jordan["common_mode_strict_upper"]) != min(cert.FORWARD_F10, cert.REVERSE_F10):
            errors.append("common mode bound")
        if "not identified" not in jordan["type_guard"]:
            errors.append("Jordan type guard")
        if jordan["fixed_j_orientation_cost_Jordan_join"] != "CERTIFIED":
            errors.append("fixed-j Jordan")
        for key in ("Round54_physical_signed_flux_alignment", "all_time_weighted_cost_variation", "all_time_weighted_cost_common_mode", "all_time_weighted_complement"):
            if jordan[key] != "NOT_CERTIFIED":
                errors.append(f"Jordan promotion {key}")

        comp = result["complement_strata_frontier"]
        if comp["rows_sha256"] != cert.digest(comp["rows"]):
            errors.append("complement rows digest")
        if comp["rows"][0]["orientation_F10_cost"] != "CERTIFIED_ZERO_FIXED_J" or "<<nu_j" not in comp["rows"][0]["proof"]:
            errors.append("grazing zero cost")
        if "iff" not in comp["exact_cut_criterion"] or "lim_" not in comp["accumulation_criterion"]:
            errors.append("cut/acc interface")
        for key in ("global_A_col_coverage", "remaining_complement_all_time_charge", "strong_pre_regularization_cemetery"):
            if comp[key] != "NOT_CERTIFIED":
                errors.append(f"complement promotion {key}")

        suffix = result["suffix_clearance_frontier"]
        if suffix["universal_values"] != "2_TRUE_5_OPEN" or len(suffix["five_open_bits"]) != 5:
            errors.append("suffix values")
        if "disjoint_union" not in suffix["first_failure_cells"]:
            errors.append("first-failure partition")
        if suffix["physical_R_at_least_r_K"] != "NOT_CERTIFIED":
            errors.append("R promotion")

        tech = result["latest_technology_audit"]
        if tech["external_dependency_imported"] is not False or len(tech["official_sources_checked"]) != 4:
            errors.append("technology scope")

        maturity = result["Gate5_maturity_update"]
        if maturity["current_global_maturity"] != "10/18" or maturity["complete_18_field_operator_block_count"] != 0 or maturity["new_global_field_completed"] is not None:
            errors.append("maturity")
        strict = result["strict_nonpromotion"]
        if strict["Gate5"] != "NOT_CERTIFIED" or strict["CM2"] != "NO-GO_FOR_CLAIM" or strict["complete_composite_gates"] != "0/5":
            errors.append("strict verdict")
        if strict["fixed_j_orientation_cost_Jordan_join"] != "CERTIFIED" or strict["all_time_weighted_variation_common_complement"] != "NOT_CERTIFIED":
            errors.append("typed Jordan verdict")

        with localcontext() as ctx:
            ctx.prec = 100
            rho = (Decimal(111718729) / Decimal(111718750)) ** cert.BLOCK_DEPTH
            w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
            threshold = Decimal(1) / w
            if not (Decimal(1) < w < Decimal("1.001")):
                errors.append("w replay")
            if str(w) != kernel["w_Z_decimal"] or str(threshold) != kernel["kappa_threshold_decimal"]:
                errors.append("threshold decimal")
            if not rho.sqrt() > threshold:
                errors.append("Round52 Holder guard")

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
        if manifest["certificate_sha256"] != sha(HERE / "cm2_gate5_round63_killed_trace_kernel_jordan_join_frontier_cert.py"):
            errors.append("certificate hash")
        if manifest["verifier_sha256"] != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("dependency map")
        if manifest["Round62_artifact_sha256"] != cert.ROUND62_PINS:
            errors.append("Round62 pins")
        for name, expected in {**cert.DEPENDENCIES, **cert.ROUND62_PINS}.items():
            path = HERE / name
            if not safe(path) or sha(path) != expected:
                errors.append(f"pinned artifact {name}")
        if manifest["verdict"] != manifest["result"]["strict_nonpromotion"]:
            errors.append("verdict copy")
    except (KeyError, TypeError) as exc:
        errors.append(f"malformed manifest: {exc}")
    return errors


def replay_errors(manifest: dict[str, Any]) -> list[str]:
    errors = integrity_errors(manifest)
    try:
        cert.validate_dependencies()
        errors.extend(direct_errors(manifest["result"]))
        rebuilt = cert.build_manifest(Path(__file__).resolve())
        if manifest != rebuilt:
            errors.append("deterministic manifest replay")
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
    malformed = {
        "duplicate": '{"x":1,"x":2}\n',
        "nan": '{"x":NaN}\n',
        "infinity": '{"x":Infinity}\n',
        "negative_infinity": '{"x":-Infinity}\n',
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for label, payload in malformed.items():
            path = root / f"{label}.json"
            path.write_text(payload, encoding="utf-8")
            try:
                json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object, parse_constant=cert.reject_json_constant)
                failures.append(f"strict JSON {label}")
            except ValueError:
                pass
    return len(paths) + len(malformed), failures


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
    verdict = manifest["verdict"]
    print("VERIFY: PASS")
    print("FIXED_J_COST_JORDAN:", verdict["fixed_j_orientation_cost_Jordan_join"])
    print("ACTUAL_ALL_TIME_DRIFT:", verdict["actual_same_owner_all_time_recurrence"])
    print("GATE5_MATURITY:", verdict["Gate5_maturity"])
    print("CM2:", verdict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
