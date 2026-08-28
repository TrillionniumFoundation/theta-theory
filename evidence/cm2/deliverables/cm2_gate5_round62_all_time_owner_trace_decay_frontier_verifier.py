#!/usr/bin/env python3
"""Fail-closed verifier for the Round-62 Gate-5 frontier leaf."""

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

import cm2_gate5_round62_all_time_owner_trace_decay_frontier_cert as cert


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(path: Path, base: Path = HERE) -> bool:
    return path.is_file() and not path.is_symlink() and path.resolve().parent == base.resolve()


def strict_load(path: Path) -> dict[str, Any]:
    if not safe(path):
        raise RuntimeError("unsafe manifest")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object, parse_constant=cert.reject_json_constant)
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


EXPECTED_PROVENANCE = {
    "dependency_sha256": dict(cert.DEPENDENCIES),
    "Round61_aggregate_artifact_sha256": dict(cert.ROUND61_AGGREGATE_PINS),
    "old_artifacts_modified": False,
    "parameter_scope": "base s=0 actual fixed-insertion owner/coarea law; all-time statements are exact direct-sum interfaces or logical separators, not a new physical decay theorem",
    "claim_type": "source-grazing null subtrace, canonical time-labelled all-insertion registry, exact outer Abel/Orlicz/Jordan interfaces, and sharp no-decay separators",
}

EXPECTED_MATURITY = {
    "previous_global_maturity": "10/18",
    "new_global_field_completed": None,
    "newly_certified_sublayers": [
        "fixed-j regular-owner source endpoint-grazing null subtrace",
        "canonical time-labelled all-insertion standard-Borel registry and exact weighted complement criterion",
        "outer weighted active-Abel and raw-Z/power-Orlicz exact identities",
        "outer weighted Jordan/common-mode identity and finite-unweighted harmonic separators",
    ],
    "reason_no_new_field_credit": "remaining complement strata, actual all-insertion decay, physical Abel/raw-Z/Orlicz finiteness, five suffix values, orientation-to-Jordan charge join and strong cemetery remain open",
    "current_global_maturity": "10/18",
    "complete_18_field_operator_block_count": 0,
}


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        if result["provenance"] != EXPECTED_PROVENANCE:
            errors.append("provenance")
        sections = {
            "source_trace_strata": cert.source_trace_strata(),
            "all_time_owner_registry": cert.all_time_owner_registry(),
            "all_time_clearance_frontier": cert.all_time_clearance_frontier(),
            "suffix_Jordan_cemetery_frontier": cert.suffix_jordan_cemetery_frontier(),
            "pinned_obstructions": cert.pinned_obstructions(),
            "latest_technology_audit": cert.technology_audit(),
        }
        for key, expected in sections.items():
            if result[key] != expected:
                errors.append(key)

        trace = result["source_trace_strata"]
        if trace["source_grazing_nullity"] != "CERTIFIED_ON_EVERY_FIXED_J_REGULAR_OWNER_LAW":
            errors.append("grazing nullity")
        if "{eta=0}" not in trace["rows"][0]["proof"] or "4^(-b)" not in trace["rows"][0]["proof"]:
            errors.append("grazing tail proof")
        if trace["rows_sha256"] != cert.digest(trace["rows"]):
            errors.append("trace digest")
        for key in ("physical_A_col_full_coverage", "global_complement_trace_nullity", "strong_cemetery_for_removed_strata"):
            if trace[key] != "NOT_CERTIFIED":
                errors.append(f"trace promotion {key}")

        reg = result["all_time_owner_registry"]
        if "equivalent immutable insertion coordinate" not in reg["legal_owner_rule"] or reg["cross_j_deduplication"] != "CERTIFIED_ILLEGAL_FOR_THE_FROZEN_OPERATOR_IDENTITY":
            errors.append("time-label owner guard")
        if "iff sum_j w_Z^j c_j<infinity" not in reg["exact_finiteness_criterion"]:
            errors.append("outer criterion")
        if "T_0+(w_Z-1)" not in reg["exact_outer_Abel_identity"] or "Tonelli" not in reg["exact_outer_Abel_identity"]:
            errors.append("outer Abel")
        if reg["separator_rows_sha256"] != cert.digest(reg["separator_rows"]):
            errors.append("registry separator digest")
        for row in reg["separator_rows"]:
            n = row["N"]
            h = sum((Q(1, j + 1) for j in range(n + 1)), Q(0))
            if Q(row["weighted_partial_sum"]) != h or row["strictly_increasing"] is not True:
                errors.append("harmonic replay")
                break
        if reg["all_time_weighted_complement_anchor"] != "NOT_CERTIFIED" or reg["deduplicated_all_time_positive_cemetery"] != "NOT_CERTIFIED":
            errors.append("registry promotion")

        clear = result["all_time_clearance_frontier"]
        if "sum_j w_Z^j Z_col,j<infinity iff" not in clear["outer_power_Orlicz_iff"]:
            errors.append("outer Orlicz iff")
        if "sum_(k in S)" not in clear["outer_clock_Abel_identity"] or "all seven suffix bits true" not in clear["local_perfect_separator"]:
            errors.append("outer clock/perfect separator")
        for key in ("physical_active_Abel_bound", "physical_raw_Z_col_bound", "physical_power_Orlicz_bound", "physical_outer_insertion_decay"):
            if clear[key] != "NOT_CERTIFIED":
                errors.append(f"clearance promotion {key}")

        jordan = result["suffix_Jordan_cemetery_frontier"]
        if jordan["suffix_universal_values"] != "2_TRUE_5_OPEN" or len(jordan["five_open_bits"]) != 5:
            errors.append("suffix values")
        if "d|J_j|+2" not in jordan["weighted_Jordan_identity"]:
            errors.append("Jordan identity")
        if "sum_j 1/(j+1)=infinity" not in jordan["variation_separator"] or "J_j=0" not in jordan["common_mode_separator"]:
            errors.append("Jordan separators")
        if jordan["separator_rows_sha256"] != cert.digest(jordan["separator_rows"]):
            errors.append("Jordan digest")
        for key in ("physical_R_at_least_r_K", "all_time_weighted_Jordan_variation_anchor", "all_time_weighted_common_mode_anchor", "all_time_orientation_to_Jordan_join", "strong_positive_cemetery"):
            if jordan[key] != "NOT_CERTIFIED":
                errors.append(f"Jordan promotion {key}")

        with localcontext() as ctx:
            ctx.prec = 100
            rho = (Decimal(111718729) / Decimal(111718750)) ** cert.BLOCK_DEPTH
            w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
            threshold = Decimal(2) * rho / (Decimal(1) + rho)
            if not Decimal(1) < w < Decimal("1.001"):
                errors.append("w replay")
            if not rho.sqrt() > threshold:
                errors.append("Holder obstruction replay")

        if result["latest_technology_audit"]["external_dependency_imported"] is not False:
            errors.append("technology import")
        if result["Gate5_maturity_update"] != EXPECTED_MATURITY:
            errors.append("maturity")
        if result["strict_nonpromotion"] != cert.strict_nonpromotion():
            errors.append("strict nonpromotion")
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
        if manifest["certificate_sha256"] != sha(HERE / "cm2_gate5_round62_all_time_owner_trace_decay_frontier_cert.py"):
            errors.append("certificate hash")
        if manifest["verifier_sha256"] != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("dependency map")
        if manifest["Round61_aggregate_artifact_sha256"] != cert.ROUND61_AGGREGATE_PINS:
            errors.append("aggregate pins")
        for name, expected in {**cert.DEPENDENCIES, **cert.ROUND61_AGGREGATE_PINS}.items():
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
    print("SOURCE_GRAZING_NULL:", s["source_endpoint_grazing_null_on_fixed_j_regular_owner_law"])
    print("ALL_TIME_COMPLEMENT:", s["all_time_weighted_complement_anchor"])
    print("GATE5_MATURITY:", s["Gate5_maturity"])
    print("CM2:", s["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
