#!/usr/bin/env python3
"""Independent verifier for the Round-57 unshifted first-return frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "cm2_gate4_round57_unshifted_first_return_frontier_cert.py"
MANIFEST_PATH = (
    HERE
    / "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
)
RESULT_SCHEMA = "cm2.gate4.round57-unshifted-first-return-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"

EXPECTED_DEPENDENCIES = {
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json": (
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414"
    ),
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json": (
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8"
    ),
}

C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_LENGTH = Q(1, 2) / C_P
AVOIDANCE_CYCLE = 1001
AVOIDANCE_HORIZON = 1002


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def no_nonfinite(token: str) -> None:
    raise ValueError(f"non-finite token: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=no_nonfinite)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file() or MANIFEST_PATH.is_symlink():
        raise ValueError("manifest path")
    value = strict_load_text(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def dependency_check(data: dict[str, Any]) -> None:
    if data["dependencies"] != EXPECTED_DEPENDENCIES:
        raise ValueError("dependency registry drift")
    provenance = data["result"]["provenance"]
    if provenance["dependency_sha256"] != EXPECTED_DEPENDENCIES:
        raise ValueError("provenance dependency drift")
    for name, expected in EXPECTED_DEPENDENCIES.items():
        if len(expected) != 64:
            raise ValueError(f"dependency not frozen: {name}")
        path = HERE / name
        if (
            not path.is_file()
            or path.is_symlink()
            or path.resolve().parent != HERE
            or sha256_path(path) != expected
        ):
            raise ValueError(f"dependency integrity: {name}")


def integrity_check(data: dict[str, Any]) -> None:
    if set(data) != {
        "certificate_sha256",
        "dependencies",
        "result",
        "schema",
        "verdict",
        "verifier_sha256",
    }:
        raise ValueError("top-level shape")
    if data["schema"] != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if not CERT_PATH.is_file() or CERT_PATH.is_symlink():
        raise ValueError("certificate path")
    if data["certificate_sha256"] != sha256_path(CERT_PATH):
        raise ValueError("certificate digest")
    if data["verifier_sha256"] != sha256_path(Path(__file__).resolve()):
        raise ValueError("verifier digest")
    dependency_check(data)
    result = data["result"]
    if result["schema"] != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay = copy.deepcopy(result)
    observed = replay.pop("internal_replay_digest")
    if observed != digest(replay):
        raise ValueError("internal replay digest")
    if data["verdict"] != result["strict_nonpromotion"]:
        raise ValueError("verdict mirror")


def expected_recovery_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r in range(7):
        state = "C24" if r % 2 == 0 else "outside_C24"
        z = 2 * C_P if state == "C24" else Q(1)
        rows.append(
            {
                "extra_recovery_r": r,
                "total_time_n_plus_r": 2 + r,
                "landing_state": state,
                "landing_normalized_Z": qstr(z),
                "landing_is_proper": z < C_P,
                "is_C24_first_return": r == 0,
                "all_three_first_return_C24_and_proper": False,
            }
        )
    return rows


def expected_direct_sum_rows() -> list[dict[str, Any]]:
    return [
        {
            "construction": "selected_forward_only",
            "forward_weight": "1",
            "reverse_weight": "0",
            "total_mass_over_h": "1",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "1",
            "ambient_object": "one tagged proper reference view",
        },
        {
            "construction": "unweighted_tagged_direct_sum",
            "forward_weight": "1",
            "reverse_weight": "1",
            "total_mass_over_h": "2",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "2",
            "ambient_object": "double charge unless explicitly renormalized",
        },
        {
            "construction": "half_weighted_tagged_direct_sum",
            "forward_weight": "1/2",
            "reverse_weight": "1/2",
            "total_mass_over_h": "1",
            "raw_graph_mass_over_h_after_inverse_endpoint_maps": "1",
            "ambient_object": "artificial disjoint-union reference, not collision space",
        },
    ]


def expected_avoidance_rows() -> list[dict[str, Any]]:
    return [
        {
            "collision_time_j": j,
            "cycle_state": j % AVOIDANCE_CYCLE,
            "in_C24": j % AVOIDANCE_CYCLE == 0,
            "is_terminal_time": j == AVOIDANCE_HORIZON,
        }
        for j in (0, 1, 2, 1000, 1001, 1002)
    ]


def semantic_replay(data: dict[str, Any]) -> None:
    result = data["result"]
    if set(result) != {
        "finite_Z_not_unshifted_proper",
        "internal_replay_digest",
        "intermediate_avoidance_frontier",
        "proper_reference_graph_lift",
        "provenance",
        "raw_common_first_return_typing",
        "recovery_clock_first_hit_obstruction",
        "schema",
        "strict_nonpromotion",
    }:
        raise ValueError("result shape")

    provenance = result["provenance"]
    if provenance != {
        "claim_type": "unshifted first-return typing, recovery no-go, proper reference graph lift, and killed-path frontier",
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "external_theorem_promoted": False,
        "old_artifacts_modified": False,
        "parameter_scope": "parameterwise for every fixed |s|<=1/400",
    }:
        raise ValueError("provenance")

    raw = result["raw_common_first_return_typing"]
    if raw["status"] != "CERTIFIED_BUT_UNPROPER":
        raise ValueError("raw graph status")
    if raw["unshifted_landing_proper"] != "NOT_CERTIFIED":
        raise ValueError("raw properness promotion")
    if "tau_cap(y,x)=n(y)" not in raw["Borel_stopping_time"]:
        raise ValueError("raw stopping time")
    if "1<=j<n" not in raw["first_hit_semantics"]:
        raise ValueError("raw first-hit semantics")
    if "(id,Q_cap)_#kappa_cap" not in raw["graph_measure_identity"]:
        raise ValueError("raw graph identity")
    if raw["source_finite_Z"].split()[0] != "CERTIFIED":
        raise ValueError("source finite Z")
    if raw["landing_finite_Z"].split()[0] != "CERTIFIED":
        raise ValueError("landing finite Z")
    if raw["typing_triplet"] != {
        "exact_same_ID_first_return_graph_tau_cap_equals_n": "CERTIFIED_BUT_UNPROPER",
        "source_and_landing_finite_Z": "CERTIFIED",
        "proper_landing_kernel": "NOT_CERTIFIED",
    }:
        raise ValueError("raw typing triplet")
    if "does not assert C24 avoidance" not in raw["non_equivalence_guard"]:
        raise ValueError("raw/postproperisation guard")

    finite = result["finite_Z_not_unshifted_proper"]
    if finite["status"] != "CERTIFIED_FINITE_Z_DOES_NOT_IMPLY_UNSHIFTED_PROPERNESS":
        raise ValueError("finite-Z theorem")
    if finite["ell"] != qstr(SHORT_LENGTH):
        raise ValueError("short length")
    if finite["finite_normalized_Z"] != qstr(2 * C_P):
        raise ValueError("short Z")
    if finite["threshold_C_p"] != qstr(C_P) or finite["finite_but_improper"] is not True:
        raise ValueError("short properness")
    if Q(1) / SHORT_LENGTH != 2 * C_P or not (2 * C_P > C_P > 1):
        raise ValueError("independent properness arithmetic")

    recovery = result["recovery_clock_first_hit_obstruction"]
    if recovery["status"] != "CERTIFIED_FIRST_HIT_POSTRECOVERY_NO_GO_AND_EXACT_TRILEMMA":
        raise ValueError("recovery theorem")
    if "never the first return" not in recovery["general_postclock_dichotomy"]:
        raise ValueError("postclock dichotomy")
    if "outside C_s" not in recovery["preclock_scope"]:
        raise ValueError("preclock scope")
    if "696*D_cap" not in recovery["D_cap_consequence"]:
        raise ValueError("Dcap typing")
    rows = recovery["two_state_separator"]["rows"]
    expected = expected_recovery_rows()
    if rows != expected or recovery["two_state_separator"]["rows_sha256"] != digest(expected):
        raise ValueError("recovery rows")
    if any(row["all_three_first_return_C24_and_proper"] for row in rows):
        raise ValueError("recovery trilemma")

    lift = result["proper_reference_graph_lift"]
    if lift["status"] != "CERTIFIED_ONCE_CHARGED_PROPER_REFERENCE_GRAPH_LIFT_NOT_PHYSICAL_KERNEL":
        raise ValueError("graph lift status")
    if lift["exact_graph_identity"] != "(X,Y)_#kappa_fw_star=(id,Q_cap)_#kappa_cap=Gamma_cap":
        raise ValueError("graph lift identity")
    if len(lift["not_a_physical_kernel"]) != 4:
        raise ValueError("graph lift guards")
    if not any("need not lie in C_s" in item for item in lift["not_a_physical_kernel"]):
        raise ValueError("graph lift collision-space guard")
    direct = expected_direct_sum_rows()
    if lift["direct_sum_rows"] != direct or lift["direct_sum_rows_sha256"] != digest(direct):
        raise ValueError("direct sum rows")
    if direct[1]["total_mass_over_h"] != "2" or direct[2]["ambient_object"].startswith("physical"):
        raise ValueError("direct sum independent replay")

    avoidance = result["intermediate_avoidance_frontier"]
    if avoidance["status"] != "CERTIFIED_RAW_RN_AVOIDANCE_AND_TERMINAL_VERSUS_KILLED_SEPARATOR__POSTRECOVERY_OPEN":
        raise ValueError("avoidance status")
    if not avoidance["original_excursion"].startswith("CERTIFIED"):
        raise ValueError("raw avoidance")
    if not avoidance["postproperisation_or_terminal_schedule"].startswith("NOT_CERTIFIED"):
        raise ValueError("post-recovery avoidance promotion")
    separator = avoidance["exact_separator"]
    if separator["core_mass"] != "1/1001<1/1000":
        raise ValueError("separator core mass")
    if separator["terminal_nonhit_mass"] != "1" or separator["all_intermediate_avoidance_mass"] != "0":
        raise ValueError("terminal/killed separation")
    rows2 = expected_avoidance_rows()
    if separator["rows"] != rows2 or separator["rows_sha256"] != digest(rows2):
        raise ValueError("avoidance rows")
    if not (Q(1, 1001) < Q(1, 1000)):
        raise ValueError("avoidance mass arithmetic")

    strict = result["strict_nonpromotion"]
    expected_strict = {
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE_PINNED_ROUND57",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE_PINNED_ROUND57",
        "physical_same_ID_unshifted_first_return_graph_tau_cap_equals_n": "CERTIFIED_BUT_UNPROPER",
        "physical_first_return_source_and_landing_finite_Z": "CERTIFIED",
        "original_R_n_intermediate_C_s_avoidance": "CERTIFIED",
        "proper_once_charged_reference_graph_lift": "CERTIFIED",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_during_added_recovery": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    if strict != expected_strict:
        raise ValueError("strict frontier")


def validate(data: dict[str, Any]) -> None:
    integrity_check(data)
    semantic_replay(data)


def assign_path(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load_manifest()
    mutations: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("dependencies", "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"), "0" * 64),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "external_theorem_promoted"), True),
        (("result", "raw_common_first_return_typing", "status"), "NOT_CERTIFIED"),
        (("result", "raw_common_first_return_typing", "unshifted_landing_proper"), "CERTIFIED"),
        (("result", "raw_common_first_return_typing", "Borel_stopping_time"), "tau=0"),
        (("result", "raw_common_first_return_typing", "first_hit_semantics"), "terminal only"),
        (("result", "raw_common_first_return_typing", "graph_measure_identity"), "surrogate"),
        (("result", "raw_common_first_return_typing", "source_finite_Z"), "NOT_CERTIFIED"),
        (("result", "raw_common_first_return_typing", "landing_finite_Z"), "NOT_CERTIFIED"),
        (("result", "raw_common_first_return_typing", "typing_triplet", "exact_same_ID_first_return_graph_tau_cap_equals_n"), "CERTIFIED"),
        (("result", "raw_common_first_return_typing", "typing_triplet", "source_and_landing_finite_Z"), "NOT_CERTIFIED"),
        (("result", "raw_common_first_return_typing", "typing_triplet", "proper_landing_kernel"), "CERTIFIED"),
        (("result", "raw_common_first_return_typing", "non_equivalence_guard"), "postproperisation avoidance certified"),
        (("result", "finite_Z_not_unshifted_proper", "ell"), "1"),
        (("result", "finite_Z_not_unshifted_proper", "finite_normalized_Z"), "1"),
        (("result", "finite_Z_not_unshifted_proper", "finite_but_improper"), False),
        (("result", "finite_Z_not_unshifted_proper", "status"), "CERTIFIED_PROPER"),
        (("result", "recovery_clock_first_hit_obstruction", "status"), "RECOVERY_IS_FIRST_RETURN"),
        (("result", "recovery_clock_first_hit_obstruction", "general_postclock_dichotomy"), "may be first"),
        (("result", "recovery_clock_first_hit_obstruction", "preclock_scope"), "still in C_s"),
        (("result", "recovery_clock_first_hit_obstruction", "D_cap_consequence"), "physical first return"),
        (("result", "recovery_clock_first_hit_obstruction", "two_state_separator", "rows", 0, "landing_is_proper"), True),
        (("result", "recovery_clock_first_hit_obstruction", "two_state_separator", "rows", 1, "landing_state"), "C24"),
        (("result", "recovery_clock_first_hit_obstruction", "two_state_separator", "rows", 2, "is_C24_first_return"), True),
        (("result", "recovery_clock_first_hit_obstruction", "two_state_separator", "rows", 3, "all_three_first_return_C24_and_proper"), True),
        (("result", "recovery_clock_first_hit_obstruction", "two_state_separator", "rows_sha256"), "0" * 64),
        (("result", "proper_reference_graph_lift", "status"), "CERTIFIED_PHYSICAL_KERNEL"),
        (("result", "proper_reference_graph_lift", "exact_graph_identity"), "(id,z)#law"),
        (("result", "proper_reference_graph_lift", "not_a_physical_kernel"), []),
        (("result", "proper_reference_graph_lift", "not_a_physical_kernel", 0), "z in C_s"),
        (("result", "proper_reference_graph_lift", "direct_sum_rows", 1, "total_mass_over_h"), "1"),
        (("result", "proper_reference_graph_lift", "direct_sum_rows", 2, "ambient_object"), "physical kernel"),
        (("result", "proper_reference_graph_lift", "direct_sum_rows_sha256"), "0" * 64),
        (("result", "intermediate_avoidance_frontier", "status"), "CERTIFIED_POSTRECOVERY"),
        (("result", "intermediate_avoidance_frontier", "original_excursion"), "NOT_CERTIFIED"),
        (("result", "intermediate_avoidance_frontier", "postproperisation_or_terminal_schedule"), "CERTIFIED"),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "core_mass"), "1/999"),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "terminal_nonhit_mass"), "0"),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "all_intermediate_avoidance_mass"), "1"),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "rows", 4, "in_C24"), False),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "rows", 5, "in_C24"), True),
        (("result", "intermediate_avoidance_frontier", "exact_separator", "rows_sha256"), "0" * 64),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_landing_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "intermediate_C24_avoidance_during_added_recovery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        (("verdict", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
    ]
    rejected = 0
    accepted: list[tuple[Any, ...]] = []
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        try:
            validate(candidate)
        except (OSError, ValueError, KeyError, TypeError):
            rejected += 1
        else:
            accepted.append(path)

    strict_cases = (
        '{"a":1,"a":2}',
        '{"a":NaN}',
        '{"a":Infinity}',
        '[1,2,3]',
    )
    for payload in strict_cases:
        try:
            parsed = strict_load_text(payload)
            if not isinstance(parsed, dict):
                raise ValueError("strict root")
        except ValueError:
            rejected += 1
    if accepted:
        raise ValueError(f"hostile mutations accepted: {accepted}")
    return rejected, len(mutations) + len(strict_cases)


def generator_replay(manifest_bytes: bytes) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT_PATH), "--manifest-json"],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ValueError(f"generator exit {proc.returncode}: {proc.stderr.decode(errors='replace')}")
    if proc.stdout != manifest_bytes:
        raise ValueError("generator reemit mismatch")


def encoded(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", type=Path)
    args = parser.parse_args()
    try:
        data = load_manifest()
        validate(data)
        if args.self_test:
            rejected, total = hostile_self_test()
            if rejected != total:
                raise ValueError(f"hostile rejection shortfall {rejected}/{total}")
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 0
        if args.replay:
            generator_replay(MANIFEST_PATH.read_bytes())
        if args.reemit is not None:
            target = args.reemit.resolve()
            if target.parent != HERE:
                raise ValueError("reemit outside deliverables")
            target.write_text(encoded(data), encoding="utf-8")
            print(f"REEMIT: {target}")
            return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(f"ROUND57_GATE4_UNSHIFTED_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.integrity_only or args.replay:
        print("ROUND57_GATE4_UNSHIFTED_INTEGRITY: PASS")
        print("FIRST_RETURN_TYPING_AND_RECOVERY_REPLAY: PASS")
        print("NO_GATE_PROMOTION: PASS")
        return 0

    strict = data["result"]["strict_nonpromotion"]
    print("RAW_FIRST_RETURN_GRAPH:", strict["physical_same_ID_unshifted_first_return_graph_tau_cap_equals_n"])
    print("PHYSICAL_PROPER_RETURN:", strict["physical_proper_same_ID_first_return_kernel"])
    print("POSTRECOVERY_AVOIDANCE:", strict["intermediate_C24_avoidance_during_added_recovery"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
