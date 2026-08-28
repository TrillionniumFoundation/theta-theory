#!/usr/bin/env python3
"""Fail-closed verifier for the independent CM2 Round-60 core audit."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERT = HERE / "cm2_round60_independent_core_frontier_audit_cert.py"
REPORT = HERE / "cm2-round60-independent-core-frontier-audit-2026-07-20.md"
MANIFEST = HERE / "cm2-round60-independent-core-frontier-audit-manifest-2026-07-20.json"
SCHEMA = "cm2.round60-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = SCHEMA + ".manifest.v1"

EXPECTED_PINS = {
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json":
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.sha256":
        "ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json":
        "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256":
        "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
}

LEAF_SCRIPTS = [
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_cert.py",
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_verifier.py",
    "cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_cert.py",
    "cm2_gate5_round60_owner_trace_suffix_positive_anchor_frontier_verifier.py",
    "cm2_gate123_round60_combined_gauge_stable_strong_operator_frontier_cert.py",
    "cm2_gate123_round60_combined_gauge_stable_strong_operator_frontier_verifier.py",
]


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite constant: {token}")


def strict_load_text(text: str) -> dict[str, Any]:
    value = json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise ValueError("JSON root")
    return value


def load(path: Path = MANIFEST) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise ValueError("manifest path")
    return strict_load_text(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def resolve_ledger_target(raw_name: str) -> Path:
    item = Path(raw_name)
    if item.is_absolute() or ".." in item.parts:
        raise ValueError("unsafe ledger name")
    path = ROOT / item if item.parts[:1] == ("deliverables",) else HERE / item
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise ValueError(f"ledger target: {raw_name}")
    return path


def replay_leaf_ledgers() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for name in EXPECTED_PINS:
        if not name.endswith(".sha256"):
            continue
        sidecar = HERE / name
        leaf_rows = []
        for line in sidecar.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            fields = line.split(maxsplit=1)
            if len(fields) != 2 or len(fields[0]) != 64:
                raise ValueError("leaf ledger syntax")
            path = resolve_ledger_target(fields[1].strip())
            if sha(path) != fields[0]:
                raise ValueError("leaf ledger digest")
            leaf_rows.append({"name": path.name, "sha256": fields[0]})
        if len(leaf_rows) != 4:
            raise ValueError("leaf ledger row count")
        rows.extend(leaf_rows)
    if len(rows) != 12 or len({row["name"] for row in rows}) != 12:
        raise ValueError("leaf ledger total")
    return rows


def stale_round60_files() -> list[str]:
    stale: list[str] = []
    cache = HERE / "__pycache__"
    if cache.is_dir():
        stale.extend(str(path.relative_to(HERE)) for path in cache.iterdir()
                     if path.is_file() and "round60" in path.name.lower())
    bad_suffixes = {".tmp", ".temp", ".bak", ".orig", ".rej", ".new"}
    for path in HERE.iterdir():
        if not path.is_file() or "round60" not in path.name.lower():
            continue
        if path.suffix.lower() in bad_suffixes or path.name.endswith("~"):
            stale.append(path.name)
    return sorted(stale)


EXPECTED_MAIN = {
    "syntax": "6/6",
    "older_dependency_and_artifact_pins": "26/26",
    "frozen_manifest_and_ledger_pins": "6/6",
    "leaf_ledger_artifact_rows": "12/12",
    "integrity": "3/3", "replay": "3/3", "reemit": "3/3",
    "hostile_and_strict_JSON_rejected": "516/516",
    "default_cert_verifier_exit_2": "6/6",
}
EXPECTED_INDEPENDENT = {
    "syntax": "2/2", "frozen_manifest_and_ledger_pins": "6/6",
    "leaf_ledger_artifact_rows": "12/12",
    "integrity": "1/1", "replay": "1/1", "reemit": "1/1",
    "hostile_and_strict_JSON_rejected": "80/80",
    "default_cert_verifier_exit_2": "2/2", "SHA_ledger_rows": "4/4",
}
EXPECTED_COMBINED = {
    "syntax": "8/8", "dependency_and_artifact_pins": "32/32",
    "integrity": "4/4", "replay": "4/4", "reemit": "4/4",
    "hostile_and_strict_JSON_rejected": "596/596",
    "SHA_ledger_rows": "16/16", "default_cert_verifier_exit_2": "8/8",
    "Round60_stale_or_temp_files": 0,
}
EXPECTED_VERDICT = {
    "Gate1": "NOT_CERTIFIED", "Gate2": "NOT_CERTIFIED",
    "Gate2_immutable_fields": "0/17", "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED", "Gate5": "NOT_CERTIFIED",
    "Gate5_maturity": "10/18", "complete_18_field_blocks": 0,
    "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
    "audit": "PASS_NO_CLAIMED_SCOPE_BLOCKER",
}


def semantics(result: dict[str, Any]) -> None:
    expected_keys = {
        "schema", "provenance", "frozen_leaf_artifact_audit",
        "gate4_independent_audit", "gate5_independent_audit",
        "gate123_independent_audit", "technology_type_audit",
        "main_leaf_acceptance_matrix", "independent_leaf_acceptance_matrix",
        "four_leaf_acceptance_matrix", "strict_verdict", "internal_replay_digest",
    }
    if set(result) != expected_keys or result["schema"] != SCHEMA:
        raise ValueError("result schema/shape")
    provenance = result["provenance"]
    if provenance["frozen_pins"] != EXPECTED_PINS or provenance["old_artifacts_modified"] is not False or provenance["external_theorem_promoted"] is not False:
        raise ValueError("provenance")
    if "explicitly conditional" not in provenance["pre_freeze_type_correction"]:
        raise ValueError("type correction")
    frozen = result["frozen_leaf_artifact_audit"]
    if frozen["manifest_and_ledger_pins"] != "6/6" or frozen["main_leaf_dependency_and_artifact_pins"] != "26/26" or frozen["leaf_ledger_rows_status"] != "12/12":
        raise ValueError("frozen matrix")
    actual_rows = replay_leaf_ledgers()
    if frozen["leaf_ledger_rows"] != actual_rows:
        raise ValueError("frozen ledger rows")

    g4 = result["gate4_independent_audit"]
    if g4["status"] != "PASS" or g4["RN_domination"] != "CERTIFIED_ON_ONE_INDUCED_PHYSICAL_LAW" or g4["field4"] != "PARTIAL_ONLY" or g4["seven_field_join"] != "1/7":
        raise ValueError("Gate4 core")
    if g4["short_separator_D_land"] != 2 or g4["fragmented_separator_D_land"] != 2 or g4["good_source_properness"] != "NOT_CERTIFIED" or g4["bad_part_is_free_cemetery"] is not False or g4["proper_full_kernel"] != "NOT_CERTIFIED":
        raise ValueError("Gate4 guards")
    cp = Q(4 * 10**90 * 360493663, 358863)
    if Q(g4["short_separator_z"]) != Q(3, 2) * cp:
        raise ValueError("Gate4 short arithmetic")
    if not cp < Q(g4["fragmented_separator_z"]) < 2 * cp:
        raise ValueError("Gate4 fragmented arithmetic")

    g5 = result["gate5_independent_audit"]
    conditional = "CERTIFIED_CONDITIONAL_EXACT_IFF_ON_ANY_SUPPLIED_BOREL_R_AND_NONNEGATIVE_C_BAD"
    if g5["status"] != "PASS_AFTER_CONDITIONAL_HYBRID_TYPE_CORRECTION" or g5["owner_projection"] != "EXACT_BOREL_R50_TO_R54" or g5["A_col_coverage"] != "NOT_CERTIFIED":
        raise ValueError("Gate5 core")
    if g5["suffix_Borel_predicates"] != "4_UNCONDITIONAL_3_CONDITIONAL" or g5["suffix_universal_values"] != "2_TRUE_5_OPEN" or g5["R"] != "CONDITIONAL_SCHEMA_ON_A_col":
        raise ValueError("Gate5 suffix")
    if g5["hybrid_iff"] != conditional or g5["physical_hybrid_finiteness"] != "NOT_CERTIFIED" or g5["orientation_is_Jordan_identification"] is not False or g5["weighted_Jordan_anchors"] != "NOT_CERTIFIED":
        raise ValueError("Gate5 hybrid/Jordan")
    if Q(g5["F10_sum"]) != Q(2395081816467609, 880000) or g5["maturity"] != "10/18" or g5["blocks"] != 0:
        raise ValueError("Gate5 arithmetic/status")

    g123 = result["gate123_independent_audit"]
    if g123["status"] != "PASS" or Q(g123["gauge_budget"]) != Q(216800000000000000000000, 1071) or g123["gauge_budget_physical"] != "NOT_CERTIFIED":
        raise ValueError("Gate123 gauge")
    if g123["root_grid"] != "3264/3264" or g123["atom_budget_identity"] != "161*5+25=830" or g123["clock_pays_raw_enumeration"] is not False or g123["CAD_closed_form"] != "D_r=2^(4*2^r-1)":
        raise ValueError("Gate123 replay")
    if g123["strong_RQ_Piola_MT_DQ"] != "NOT_CERTIFIED":
        raise ValueError("Gate123 strong status")

    tech = result["technology_type_audit"]
    if tech["status"] != "PASS_NO_EXTERNAL_PROMOTION" or tech["external_theorem_promoted"] is not False or not all(tech[key] for key in (
        "small_hole_standard_families_do_not_supply_actual_landing_or_strong_RQ",
        "CAD_sources_do_not_pay_depth_integrated_boundary_complexity",
        "inter_sign_transport_does_not_pay_positive_Jordan_common_mode",
    )):
        raise ValueError("technology typing")
    if result["main_leaf_acceptance_matrix"] != EXPECTED_MAIN or result["independent_leaf_acceptance_matrix"] != EXPECTED_INDEPENDENT or result["four_leaf_acceptance_matrix"] != EXPECTED_COMBINED:
        raise ValueError("acceptance matrix")
    if result["strict_verdict"] != EXPECTED_VERDICT:
        raise ValueError("strict verdict")


def validate(data: dict[str, Any], *, check_files: bool = True, check_stale: bool = True) -> None:
    if set(data) != {"schema", "dependencies", "certificate_sha256", "verifier_sha256", "report_sha256", "result", "verdict"}:
        raise ValueError("manifest shape")
    if data["schema"] != MANIFEST_SCHEMA or data["dependencies"] != EXPECTED_PINS:
        raise ValueError("manifest schema/dependencies")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        value = data[key]
        if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ValueError(f"artifact digest syntax: {key}")
    if check_files:
        for name, expected in EXPECTED_PINS.items():
            path = HERE / name
            if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE or sha(path) != expected:
                raise ValueError(f"frozen pin: {name}")
        if data["certificate_sha256"] != sha(CERT) or data["verifier_sha256"] != sha(Path(__file__).resolve()) or data["report_sha256"] != sha(REPORT):
            raise ValueError("audit artifact hash")
    replay = copy.deepcopy(data["result"])
    observed = replay.pop("internal_replay_digest")
    if observed != digest(replay):
        raise ValueError("result digest")
    semantics(data["result"])
    if data["verdict"] != data["result"]["strict_verdict"]:
        raise ValueError("verdict mirror")
    if check_stale:
        stale = stale_round60_files()
        if stale:
            raise ValueError(f"Round60 stale/temp: {stale}")


def run(args: list[str], expected: int = 0) -> subprocess.CompletedProcess[bytes]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, *args], cwd=ROOT, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != expected:
        raise ValueError(
            f"subprocess exit {proc.returncode}!={expected}: {' '.join(args)}\n"
            + proc.stdout.decode(errors="replace") + proc.stderr.decode(errors="replace")
        )
    return proc


def syntax_replay() -> None:
    for name in LEAF_SCRIPTS + [CERT.name, Path(__file__).name]:
        path = HERE / name
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def leaf_acceptance_replay() -> None:
    syntax_replay()
    g4_cert, g4_ver, g5_cert, g5_ver, g123_cert, g123_ver = [str(HERE / name) for name in LEAF_SCRIPTS]

    g4_manifest = HERE / "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json"
    proc = run([g4_cert, "--manifest-json"])
    if proc.stdout != g4_manifest.read_bytes():
        raise ValueError("Gate4 producer replay")
    for flag in ("--integrity-only", "--replay", "--self-test", "--reemit", "--check-defaults"):
        run([g4_ver, flag])

    run([g5_cert, "--summary"])
    for flag in ("--integrity-only", "--replay", "--self-test"):
        run([g5_ver, flag])
    with tempfile.TemporaryDirectory(prefix="cm2-r60-audit-g5-") as temp_dir:
        target = Path(temp_dir) / "manifest.json"
        run([g5_ver, "--reemit", str(target)])
        g5_manifest = HERE / "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
        if target.read_bytes() != g5_manifest.read_bytes():
            raise ValueError("Gate5 reemit")

    run([g123_cert, "--audit"])
    for flag in ("--integrity-only", "--replay", "--self-test", "--reemit"):
        run([g123_ver, flag])

    for script in (g4_cert, g4_ver, g5_cert, g5_ver, g123_cert, g123_ver):
        run([script], expected=2)


def generator_replay() -> None:
    proc = run([str(CERT), "--manifest-json"])
    if proc.stdout != MANIFEST.read_bytes():
        raise ValueError("audit generator replay")


def default_exit_replay() -> None:
    run([str(CERT)], expected=2)
    run([str(Path(__file__).resolve()), "--default-child"], expected=2)


PathKey = str | int


def scalar_paths(value: Any, prefix: tuple[PathKey, ...] = ()) -> list[tuple[PathKey, ...]]:
    out: list[tuple[PathKey, ...]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            out.extend(scalar_paths(value[key], prefix + (key,)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.extend(scalar_paths(item, prefix + (index,)))
    else:
        out.append(prefix)
    return out


def get_path(value: Any, path: tuple[PathKey, ...]) -> Any:
    cursor = value
    for key in path:
        cursor = cursor[key]
    return cursor


def set_path(value: Any, path: tuple[PathKey, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def mutate(value: Any) -> Any:
    if value is None:
        return "MUTATED_NONE"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__MUTATED"
    raise TypeError(type(value))


def hostile() -> tuple[int, int]:
    original = load()
    paths = scalar_paths(original)
    if len(paths) < 76:
        raise ValueError("hostile leaf supply")
    rejected = 0
    for path in paths[:76]:
        candidate = copy.deepcopy(original)
        set_path(candidate, path, mutate(get_path(candidate, path)))
        try:
            validate(candidate, check_files=False, check_stale=False)
        except (ValueError, KeyError, TypeError, IndexError, ArithmeticError):
            rejected += 1
    malformed = ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '[1,2]')
    for payload in malformed:
        try:
            strict_load_text(payload)
        except (ValueError, json.JSONDecodeError):
            rejected += 1
    return rejected, 80


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    parser.add_argument("--default-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        data = load()
        validate(data)
        if args.default_child:
            print("INDEPENDENT_AUDIT:", data["verdict"]["audit"])
            return 2
        if args.replay:
            generator_replay()
            leaf_acceptance_replay()
            default_exit_replay()
            print("ROUND60_INDEPENDENT_REPLAY: PASS")
            return 0
        if args.self_test:
            rejected, total = hostile()
            if rejected != total:
                raise ValueError(f"hostile shortfall: {rejected}/{total}")
            print(f"HOSTILE_AND_STRICT_JSON_REJECTED: {rejected}/{total}")
            return 0
        if args.reemit is not None:
            generated = run([str(CERT), "--manifest-json"]).stdout
            if generated != MANIFEST.read_bytes():
                raise ValueError("reemit generator drift")
            args.reemit.write_bytes(generated)
            print(f"REEMIT: {args.reemit}")
            return 0
        if args.integrity_only:
            print("ROUND60_INDEPENDENT_INTEGRITY: PASS")
            return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, ArithmeticError) as exc:
        print(f"ROUND60_INDEPENDENT_AUDIT_VERIFY_FAILURE: {exc}", file=sys.stderr)
        return 1
    verdict = data["verdict"]
    print("INDEPENDENT_AUDIT:", verdict["audit"])
    print("COMPOSITE_GATES:", verdict["complete_composite_gates"])
    print("CM2:", verdict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
