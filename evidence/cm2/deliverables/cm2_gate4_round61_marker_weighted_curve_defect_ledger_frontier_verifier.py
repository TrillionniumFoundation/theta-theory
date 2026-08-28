#!/usr/bin/env python3
"""Independent verifier for the Round-61 Gate-4 curve/defect frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round61-marker-weighted-curve-defect-ledger-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-20.md"
CERT = HERE / "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "c5cb689594c28296c1834f96ba8dbba092c513f60cbaef61e7efbda921d16388"

DEPENDENCIES = {
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json":
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json":
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
}

BASELINE = {
    "cm2-sixtieth-direct-assault-2026-07-20.md":
        "ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212",
    "cm2-sixtieth-direct-assault-manifest-2026-07-20.sha256":
        "5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-assault-2026-07-20.md":
        "88f042ed434f6199123a5f164385572dabfcde0af13a8d6b9d7ca1385079d00f",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256":
        "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_cert.py":
        "4a5d914ce8fec6c259e8df49f6c9ce04cc17285adfd2fd06173270635982f1b7",
    "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_verifier.py":
        "c74c71809b8484c85eadc921a74e6fdc6c38e85179167f68226844f685267503",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_L = Q(2, 1) / (3 * C_P)
SHORT_H = SHORT_L / 2
SHORT_J = Q(1, 2)
SHORT_Z = Q(3, 2) * C_P
SHORT_MOMENT = 2 * SHORT_L

EXPECTED_FRONTIER = {
    "actual_landing_RN_marker": "CERTIFIED_PINNED_ROUND60",
    "actual_marker_weighted_cone_curve_lift": "CERTIFIED_EXACT",
    "physical_invariant_unstable_Rokhlin_and_stable_holonomy": "NOT_CERTIFIED",
    "seven_field_physical_landing_join": "1/7_COMPLETE__FIELDS_1_4_7_PARTIAL_ONLY",
    "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
    "positive_good_bad_weighted_graph_hybrid": "CERTIFIED_EXACT_IN_X_D_GRAPH_ONLY",
    "D_land_pays_weighted_graph_TV_defect": "CERTIFIED_EXACT",
    "D_land_pays_BV_or_strong_current_defect": "NOT_CERTIFIED__BV_DERIVATIVE_ROUTE_FALSE_BY_SMOOTH_SEPARATOR",
    "downstream_accepts_positive_graph_defect": "NOT_CERTIFIED",
    "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
    "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
    "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
    "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
    "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
    "strong_singular_current_cemetery": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


class DuplicateKeyError(ValueError):
    pass


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    d = 1
    while Q(1, 2**d) * z >= C_P / 2:
        d += 1
    return d


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file() or MANIFEST.is_symlink() or MANIFEST.resolve().parent != HERE:
        raise ValueError("manifest path")
    data = strict_json(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root")
    return data


def check_files() -> None:
    for mapping in (DEPENDENCIES, BASELINE):
        for name, expected in mapping.items():
            path = HERE / name
            if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
                raise ValueError(f"pinned path: {name}")
            if sha256_path(path) != expected:
                raise ValueError(f"pinned hash: {name}")
    for path in (CERT, VERIFIER, REPORT):
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise ValueError(f"artifact path: {path.name}")


def load_result(name: str) -> dict[str, Any]:
    data = strict_json((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("result"), dict):
        raise ValueError(f"dependency semantic root: {name}")
    return data["result"]


def replay_dependencies() -> None:
    r60 = load_result(
        "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json"
    )
    marker = r60["actual_landing_RN_marker_bridge"]
    if "0<=g_B<=1" not in marker["RN_marker"]:
        raise ValueError("Round60 marker")
    if r60["seven_field_materialization_audit"]["actual_complete_rows"] != "1/7":
        raise ValueError("Round60 field count")
    if "integral_B h*2^D_land" not in r60["good_bad_original_time_graph_split"]["bad_dyadic_moment"]:
        raise ValueError("Round60 bad moment")

    r35 = load_result(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )
    leaf = r35["collision_SRB_leaf_disintegration"]
    if leaf["conditional_density_wrt_dell"] != "cp/sqrt(17)":
        raise ValueError("Round35 leaf density")
    if leaf["integrating_leaf_weights_recovers_mu_s_restricted_to_component"] is not True:
        raise ValueError("Round35 physical recovery")
    if r35["arbitrary_Rn_parent_W_Borel_registry"]["inside_invariant_unstable_cone"] is not True:
        raise ValueError("Round35 cone")

    r56 = load_result(
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    )["paired_leafwise_reverse_replay"]
    if "mu_s|C_s exactly once" not in r56["induced_return_once_coverage"]:
        raise ValueError("Round56 once coverage")
    if "subinterval of the exact Round35 slope-four" not in r56["forward_terminal_exact_inclusion"]:
        raise ValueError("Round56 curve inclusion")

    r58 = load_result(
        "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json"
    )
    if "integral h(y)*2^D_land" not in r58["landing_bad_stratum_interface"]["dyadic_moment"]:
        raise ValueError("Round58 dyadic moment")

    r57 = load_result(
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    )["raw_common_first_return_typing"]
    if "notin C_s" not in r57["first_hit_semantics"] or "charged exactly once" not in r57["charge"]:
        raise ValueError("Round57 graph semantics")


def integrity_check(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_files()
    if data.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if data.get("dependencies") != DEPENDENCIES:
        raise ValueError("dependencies")
    if data.get("baseline_files") != BASELINE:
        raise ValueError("baseline")
    if data.get("certificate_sha256") != sha256_path(CERT):
        raise ValueError("certificate hash")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        raise ValueError("verifier hash")
    if data.get("report_sha256") != sha256_path(REPORT):
        raise ValueError("report hash")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        value = data.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(key)
    result = data.get("result")
    if not isinstance(result, dict):
        raise ValueError("result root")
    replay = dict(result)
    recorded = replay.pop("internal_replay_digest", None)
    if recorded != EXPECTED_RESULT_DIGEST or digest(replay) != recorded:
        raise ValueError("internal result digest")
    if data.get("verdict") != result.get("strict_nonpromotion"):
        raise ValueError("verdict alias")


def replay_graph_lattice(result: dict[str, Any]) -> None:
    section = result["weighted_graph_defect_lattice"]
    if section["status"] != "CERTIFIED_EXACT_POSITIVE_GOOD_BAD_HYBRID_IN_WEIGHTED_GRAPH_TV_LATTICE__DOWNSTREAM_STRONG_ACCEPTANCE_ABSENT":
        raise ValueError("graph status")
    atoms = section["sample_atoms"]
    if digest(atoms) != section["sample_atoms_sha256"] or len(atoms) != 3:
        raise ValueError("graph atom digest")
    mass = Q(0)
    weighted = Q(0)
    for row in atoms:
        m = Q(row["mass"])
        wm = Q(row["weighted_mass"])
        if wm != 2 ** int(row["D"]) * m:
            raise ValueError("graph atom weight")
        mass += m
        weighted += wm
    if mass != Q(53, 320) or qstr(mass) != section["sample_total_mass"]:
        raise ValueError("graph mass")
    if weighted != Q(7, 5) or qstr(weighted) != section["sample_weighted_norm"]:
        raise ValueError("graph norm")
    rows = section["five_interface_rows"]
    if len(rows) != 5 or digest(rows) != section["five_interface_rows_sha256"]:
        raise ValueError("graph interface rows")
    if section["graph_rows_complete"] != "4/5" or section["requested_strong_interface_rows_complete"] != "1/5_TAG_ROW_ONLY":
        raise ValueError("graph completion typing")
    if rows[4]["graph_lattice"] != "NOT_CERTIFIED":
        raise ValueError("downstream row")
    if "not the anisotropic" not in section["type_guard"]:
        raise ValueError("graph type guard")


def replay_smooth_separator(result: dict[str, Any]) -> None:
    section = result["smooth_Dland_vs_strong_separator"]
    rows = section["rows"]
    if len(rows) != 5 or digest(rows) != section["rows_sha256"]:
        raise ValueError("separator rows")
    if SHORT_Z != SHORT_J / SHORT_H or defect_depth(SHORT_Z) != 2:
        raise ValueError("separator threshold")
    frequencies = [1, 2, 17, 257, 4096]
    for row, frequency in zip(rows, frequencies):
        if row["frequency_N"] != frequency:
            raise ValueError("separator frequency")
        if Q(row["plaque_length_L"]) != SHORT_L:
            raise ValueError("separator L")
        if Q(row["mass_h"]) != SHORT_H or Q(row["minimal_boundary_J"]) != SHORT_J:
            raise ValueError("separator h/J")
        if Q(row["normalized_boundary_z"]) != SHORT_Z or row["D_land"] != 2:
            raise ValueError("separator z/D")
        if Q(row["weighted_D_moment"]) != SHORT_MOMENT:
            raise ValueError("separator moment")
        if row["BV_variation_of_marker"] != frequency:
            raise ValueError("separator BV")
    if section["status"] != "CERTIFIED_SMOOTH_SEPARATOR__D_LAND_MOMENT_DOES_NOT_CONTROL_BV_DERIVATIVE_TRACE":
        raise ValueError("separator status")
    if "does not purport to refute every possible anisotropic norm" not in section["conclusion"]:
        raise ValueError("separator scope guard")


def replay_semantics(result: dict[str, Any]) -> None:
    if result.get("schema") != RESULT_SCHEMA:
        raise ValueError("result schema")
    curve = result["actual_marker_weighted_curve_lift"]
    if curve["status"] != "CERTIFIED_EXACT_ACTUAL_MARKER_WEIGHTED_CONE_CURVE_MEASURE_LIFT__NOT_REGULAR_STANDARD_FAMILY_OR_PHYSICAL_ROKHLIN_HOLONOMY_PRODUCT":
        raise ValueError("curve status")
    if "not asserted to be a partition" not in curve["rokhlin_guard"]:
        raise ValueError("curve Rokhlin guard")
    if "not a stable-holonomy" not in curve["holonomy_guard"]:
        raise ValueError("curve holonomy guard")
    if "not claimed to remain a regular standard family" not in curve["field_effect"] or "no complete seven-field row" not in curve["field_effect"]:
        raise ValueError("curve field guard")
    if "Euclidean-arclength Jacobian" not in curve["landing_leaf_density"] or "not generally slope four" not in curve["landing_leaf_density"]:
        raise ValueError("curve landing metric/type")

    field = result["seven_field_materialization_audit"]
    if field["actual_complete_rows"] != "1/7" or field["partial_rows"] != [1, 4, 7]:
        raise ValueError("field count")
    if field["official_Gate2_fields_unchanged"] != "0/17":
        raise ValueError("Gate2 count")
    if digest(field["rows"]) != field["rows_sha256"]:
        raise ValueError("field rows")

    if result["strict_nonpromotion"] != EXPECTED_FRONTIER:
        raise ValueError("strict frontier")
    if result["latest_official_technology_audit"]["external_theorem_promoted"] is not False:
        raise ValueError("external theorem promotion")
    if "weighted L1" not in result["downstream_join_audit"]["physical_q"]:
        raise ValueError("q typing")
    replay_graph_lattice(result)
    replay_smooth_separator(result)


def deterministic_regeneration(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if proc.returncode != 0:
        raise ValueError(f"producer exit {proc.returncode}: {proc.stderr.strip()}")
    produced = strict_json(proc.stdout)
    if produced != data:
        raise ValueError("producer replay mismatch")
    if proc.stdout.encode("utf-8") != MANIFEST.read_bytes():
        raise ValueError("producer bytes mismatch")


def deep_scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    paths: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "internal_replay_digest":
                continue
            paths.extend(deep_scalar_paths(child, prefix + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(deep_scalar_paths(child, prefix + (index,)))
    else:
        paths.append(prefix)
    return paths


def mutate_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "__HOSTILE"
    if value is None:
        return "HOSTILE"
    return {"hostile": True}


def set_path(root: Any, path: tuple[Any, ...], value: Any) -> None:
    node = root
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


def self_test(data: dict[str, Any]) -> int:
    paths = deep_scalar_paths(data["result"])
    selected = paths[:120]
    rejected = 0
    for path in selected:
        mutant = copy.deepcopy(data)
        old = mutant["result"]
        node: Any = old
        for step in path:
            node = node[step]
        set_path(old, path, mutate_scalar(node))
        replay = dict(old)
        replay.pop("internal_replay_digest", None)
        old["internal_replay_digest"] = digest(replay)
        mutant["verdict"] = old["strict_nonpromotion"]
        try:
            integrity_check(mutant, files=False)
            replay_semantics(old)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
    if rejected != len(selected) or len(selected) < 100:
        raise ValueError(f"hostile mutations accepted: {rejected}/{len(selected)}")

    hostile_json = [
        '{"a":1,"a":2}',
        '{"x":NaN}',
        '{"x":Infinity}',
        '{"x":-Infinity}',
    ]
    json_rejected = 0
    for payload in hostile_json:
        try:
            strict_json(payload)
        except (ValueError, DuplicateKeyError):
            json_rejected += 1
    if json_rejected != len(hostile_json):
        raise ValueError("hostile JSON accepted")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{len(selected)}")
    print(f"HOSTILE_JSON_REJECTED: {json_rejected}/{len(hostile_json)}")
    return rejected + json_rejected


def reemit(path: Path, data: dict[str, Any]) -> None:
    deterministic_regeneration(data)
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if proc.returncode != 0:
        raise ValueError("reemit producer failure")
    path.write_bytes(proc.stdout)
    if path.read_bytes() != MANIFEST.read_bytes():
        raise ValueError("reemit bytes")


def run_audit(data: dict[str, Any], *, regenerate: bool = True) -> None:
    integrity_check(data)
    replay_dependencies()
    replay_semantics(data["result"])
    if regenerate:
        deterministic_regeneration(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        if args.audit:
            run_audit(data)
            print("AUDIT_MODE: PASS")
            return 0
        if args.self_test:
            run_audit(data)
            self_test(data)
            print("SELF_TEST: PASS")
            return 0
        if args.reemit is not None:
            run_audit(data, regenerate=False)
            reemit(args.reemit, data)
            print(f"REEMIT: {args.reemit}")
            return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, subprocess.SubprocessError) as exc:
        print(f"ROUND61_GATE4_CURVE_DEFECT_VERIFY_FAILURE: {exc}")
        return 1

    frontier = data["result"]["strict_nonpromotion"]
    print("CURVE_LIFT:", frontier["actual_marker_weighted_cone_curve_lift"])
    print("GRAPH_HYBRID:", frontier["positive_good_bad_weighted_graph_hybrid"])
    print("STRONG_DEFECT:", frontier["D_land_pays_BV_or_strong_current_defect"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
