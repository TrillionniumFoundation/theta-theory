#!/usr/bin/env python3
"""Independent verifier for the Round-63 Gate-2/4 saturation frontier."""

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
RESULT_SCHEMA = "cm2.gate24.round63-stable-saturation-holonomy-square-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round63-stable-saturation-holonomy-square-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
LEDGER = HERE / f"{PREFIX}-manifest-2026-07-21.sha256"
CERT = HERE / "cm2_gate24_round63_stable_saturation_holonomy_square_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "30585299c51f439d29724f32da1468014466f7c54cf4148115c6ff0aaaab8a72"

DEPENDENCIES = {
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json":
        "19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json":
        "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json":
        "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
}

BASELINE = {
    "cm2-sixty-second-direct-assault-2026-07-21.md":
        "873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f",
    "cm2-sixty-second-direct-assault-manifest-2026-07-21.sha256":
        "e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-assault-2026-07-21.md":
        "4acca86b074ce3f6792aa04625c9576d2affeacb0ad9d7cdeb09cabd08d45b00",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
    "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_cert.py":
        "12ef3cbaa17d727eeadb63fc6e1eb5a6256a38a7ebc35c8c159e5f951bdd4939",
    "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_verifier.py":
        "432c2b827e61a1d5db3bb5e5d2e8266c66abc25ccb3d341cc4d76257ed17ed0b",
    "cm2-round62-independent-core-frontier-audit-2026-07-21.md":
        "123f8ffc563e7d2b364f7caf565ac1a953ecc45123d1c483bc0f97b24c3cfeb4",
    "cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.sha256":
        "32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414",
    "cm2_round62_independent_core_frontier_audit_cert.py":
        "2d09eec99d4a32561f266702ad4e3e05bcf39b81f3b6c5a8d92e56d15b547c91",
    "cm2_round62_independent_core_frontier_audit_verifier.py":
        "893939d281c4bd3f6759b89e52a73c5057ff1fe64bc1117bad8875f38de1d804",
}

EXPECTED_STRICT = {
    "actual_tagged_first_return_branch_RN_covariance": "CERTIFIED_PINNED_ROUND62",
    "branch_holonomy_square_defect_identity": "CERTIFIED_EXACT",
    "exact_square_preserves_source_landing_defect_norm": "CERTIFIED_EXACT",
    "two_plaque_L1_stable_saturation_distance": "CERTIFIED_EXACT",
    "physical_invariant_product_rectangles": "NOT_CERTIFIED",
    "physical_stable_projection_and_two_sided_J_hol": "NOT_CERTIFIED",
    "actual_marker_zero_defect": "NOT_CERTIFIED",
    "holonomy_transport_m_squared_budget": "CERTIFIED_CONDITIONAL",
    "actual_FRthetaLmM_budget": "NOT_CERTIFIED",
    "fibrewise_FR_below_Cp_theta_L": "NOT_CERTIFIED",
    "tagged_graph_cylinder_normal_current": "CERTIFIED_PINNED_ROUND62",
    "physical_anisotropic_current_Piola_assembly": "NOT_CERTIFIED",
    "seven_field_landing_join": "1/7_COMPLETE__FIELDS_1_4_7_PARTIAL",
    "official_immutable_Gate2_fields": "0/17",
    "proper_physical_same_ID_first_return_kernel": "NOT_CERTIFIED",
    "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
    "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
    "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
    "strong_singular_current_cemetery": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}

CP = Q(4 * 10**90 * 360493663, 358863)


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
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"non-finite JSON: {token}")),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file() or MANIFEST.is_symlink() or MANIFEST.resolve().parent != HERE:
        raise ValueError("manifest path")
    data = strict_json(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root")
    return data


def load_dependency(name: str) -> dict[str, Any]:
    data = strict_json((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("result"), dict):
        raise ValueError(f"dependency result: {name}")
    return data["result"]


def check_files() -> None:
    for mapping in (DEPENDENCIES, BASELINE):
        for name, expected in mapping.items():
            path = HERE / name
            if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
                raise ValueError(f"pinned path: {name}")
            if sha256_path(path) != expected:
                raise ValueError(f"pinned hash: {name}")
    for path in (CERT, VERIFIER, REPORT, MANIFEST):
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise ValueError(f"artifact path: {path.name}")


def replay_dependencies() -> None:
    r62 = load_dependency(
        "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json"
    )
    if r62["actual_branch_RN_covariance"]["status"] != (
        "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE"
    ):
        raise ValueError("Round62 branch covariance")
    if r62["seven_field_materialization_audit"]["complete_rows"] != "1/7":
        raise ValueError("Round62 landing fields")
    if r62["strict_nonpromotion"]["official_immutable_Gate2_fields"] != "0/17":
        raise ValueError("Round62 Gate2 fields")

    audit = load_dependency("cm2-round62-independent-core-frontier-audit-manifest-2026-07-21.json")
    final = audit["strict_final_state"]
    if final["audit_verdict"] != "PASS_AFTER_RED_TEAM_CORRECTIONS" or final["CM2"] != "NO-GO_FOR_CLAIM":
        raise ValueError("Round62 audit verdict")

    r61 = load_dependency("cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json")
    fields61 = r61["seven_field_materialization_audit"]
    if fields61["actual_complete_rows"] != "1/7" or fields61["partial_rows"] != [1, 4, 7]:
        raise ValueError("Round61 fields")

    r60 = load_dependency("cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json")
    if r60["actual_landing_RN_marker_bridge"]["status"] != "CERTIFIED_ACTUAL_RN_MARKER_AND_CONDITIONAL_SAME_MEASURE_BAYES_FORMULA__FIELD4_PARTIAL_ONLY":
        raise ValueError("Round60 marker")
    if r60["perfect_product_fields_1_to_4_nonimplication"]["status"] != "CERTIFIED_FIELDS_1_TO_4_QUALITATIVELY_PERFECT_DO_NOT_IMPLY_PHYSICAL_BOUNDARY_THRESHOLD":
        raise ValueError("Round60 separators")

    r59 = load_dependency("cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json")
    bridge = r59["quantitative_product_rectangle_bridge"]
    if bridge["strict_sufficient_inequality"] != "F(u)*R(u)<C_p*theta(u)*L(u) almost everywhere":
        raise ValueError("Round59 bridge")


def integrity_check(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_files()
    if data.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if data.get("dependencies") != DEPENDENCIES or data.get("baseline_files") != BASELINE:
        raise ValueError("pins")
    if data.get("certificate_sha256") != sha256_path(CERT):
        raise ValueError("certificate hash")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        raise ValueError("verifier hash")
    if data.get("report_sha256") != sha256_path(REPORT):
        raise ValueError("report hash")
    result = data.get("result")
    if not isinstance(result, dict):
        raise ValueError("result root")
    replay = dict(result)
    recorded = replay.pop("internal_replay_digest", None)
    if recorded != EXPECTED_RESULT_DIGEST or digest(replay) != recorded:
        raise ValueError("result digest")
    if data.get("verdict") != result.get("strict_nonpromotion"):
        raise ValueError("verdict alias")


def dynamic(values: list[Q], image: list[int]) -> list[Q]:
    inverse = [image.index(j) for j in range(len(image))]
    return [values[inverse[j]] for j in range(len(image))]


def l1_uniform(values: list[Q]) -> Q:
    return sum((abs(x) for x in values), Q(0)) / len(values)


def replay_square(result: dict[str, Any]) -> None:
    section = result["branch_holonomy_square"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("square digest")
    image = replay["dynamic_branch_image"]
    a_u = [Q(x) for x in replay["source_marker_a_u"]]
    a_v = [Q(x) for x in replay["source_marker_a_v"]]
    g_u = dynamic(a_u, image)
    g_v = dynamic(a_v, image)
    ds = [v - u for u, v in zip(a_u, a_v)]
    dl = [v - u for u, v in zip(g_u, g_v)]
    if dl != dynamic(ds, image):
        raise ValueError("square identity")
    if l1_uniform(ds) != Q(1, 6) or l1_uniform(dl) != Q(1, 6):
        raise ValueError("square norm")
    if replay["landing_marker_g_u"] != [str(x) for x in g_u] or replay["landing_marker_g_v"] != [str(x) for x in g_v]:
        raise ValueError("square rows")
    if section["status"] != "CERTIFIED_EXACT_BRANCH_HOLONOMY_SQUARE_DEFECT_IDENTITY__PHYSICAL_HOLONOMY_AND_ZERO_DEFECT_ABSENT":
        raise ValueError("square status")


def replay_saturation(result: dict[str, Any]) -> None:
    section = result["two_plaque_stable_saturation"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("saturation digest")
    if Q(replay["L1_marker_defect"]) != Q(1, 6) or Q(replay["delta_sat"]) != Q(1, 12):
        raise ValueError("saturation values")
    if section["exact_formula"] != "delta_sat=1/2||g_v-Pg_u||_L1(mu_v) for two plaques of outer weight 1/2 and a positive L1 isometry P":
        raise ValueError("saturation formula")
    if "conditional expectation is not asserted" not in section["L1_guard"]:
        raise ValueError("L1 guard")


def replay_transport(result: dict[str, Any]) -> None:
    section = result["quantitative_holonomy_transport"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("transport digest")
    F, R = Q(replay["F_u"]), Q(replay["R_u"])
    theta, length = Q(replay["theta_u"]), Q(replay["L_u"])
    m, M = Q(replay["metric_derivative_lower_m"]), Q(replay["metric_derivative_upper_M"])
    bound = F * R * M / (m * m * theta * length)
    if bound != Q(72) or Q(replay["target_z_upper"]) != bound or not bound < CP:
        raise ValueError("transport bound")
    if section["m_squared_audit"] != "one factor m pays retained-span contraction and one factor m pays the 1/lambda density-ratio conversion":
        raise ValueError("m squared")
    if section["status"] != "CERTIFIED_CONDITIONAL_EXACT_HOLONOMY_TRANSPORT_BUDGET_WITH_M_SQUARED_COST__ACTUAL_INPUTS_ABSENT":
        raise ValueError("transport status")


def replay_separators(result: dict[str, Any]) -> None:
    section = result["zero_defect_quantitative_separators"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("separator digest")
    short = replay["short_span"]
    if Q(short["z"]) != 2 * CP or not Q(short["z"]) > CP:
        raise ValueError("short separator")
    frag = replay["fragmentation"]
    N = CP.numerator // CP.denominator + 1
    if Q(frag["J"]) != N or Q(frag["h"]) != Q(1, 2) or Q(frag["z"]) != 2 * N:
        raise ValueError("fragment separator")
    if not Q(frag["z"]) > CP:
        raise ValueError("fragment threshold")
    if "delta_sat=0" not in section["common_hypotheses"]:
        raise ValueError("zero defect guard")


def replay_frontier(result: dict[str, Any]) -> None:
    if result.get("schema") != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay_square(result)
    replay_saturation(result)
    replay_transport(result)
    replay_separators(result)
    fields = result["seven_field_materialization_audit"]
    if fields["complete_rows"] != "1/7" or fields["partial_rows"] != [1, 4, 7]:
        raise ValueError("field counts")
    if fields["official_immutable_Gate2_fields"] != "0/17" or len(fields["rows"]) != 7:
        raise ValueError("Gate2/landing rows")
    if digest(fields["rows"]) != fields["rows_sha256"]:
        raise ValueError("field digest")
    if result["strict_nonpromotion"] != EXPECTED_STRICT:
        raise ValueError("strict frontier")
    if result["provenance"]["external_theorem_promoted"] is not False:
        raise ValueError("external theorem promotion")


def deterministic_regeneration(data: dict[str, Any]) -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json", "--verifier", str(VERIFIER)],
        cwd=HERE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if proc.returncode != 0:
        raise ValueError(f"producer regeneration: {proc.stderr.decode('utf-8', 'replace')}")
    if proc.stdout != MANIFEST.read_bytes():
        raise ValueError("producer regeneration bytes")
    regenerated = strict_json(proc.stdout.decode("utf-8"))
    if regenerated != data:
        raise ValueError("producer regeneration object")


def check_sidecar() -> None:
    if not LEDGER.is_file() or LEDGER.is_symlink() or LEDGER.resolve().parent != HERE:
        raise ValueError("SHA sidecar path")
    rows = [line.split() for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 4:
        raise ValueError("SHA sidecar rows")
    expected_names = {REPORT.name, MANIFEST.name, CERT.name, VERIFIER.name}
    if {parts[-1] for parts in rows} != expected_names:
        raise ValueError("SHA sidecar names")
    for parts in rows:
        if len(parts) != 2 or sha256_path(HERE / parts[1]) != parts[0]:
            raise ValueError(f"SHA sidecar mismatch: {parts[-1]}")


def deep_scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    out: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            if key == "internal_replay_digest":
                continue
            out.extend(deep_scalar_paths(value[key], prefix + (key,)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.extend(deep_scalar_paths(item, prefix + (index,)))
    else:
        out.append(prefix)
    return out


def mutate_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
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
    paths = deep_scalar_paths(data["result"])[:240]
    rejected = 0
    for path in paths:
        mutant = copy.deepcopy(data)
        result = mutant["result"]
        node: Any = result
        for step in path:
            node = node[step]
        set_path(result, path, mutate_scalar(node))
        replay = dict(result)
        replay.pop("internal_replay_digest", None)
        result["internal_replay_digest"] = digest(replay)
        mutant["verdict"] = result["strict_nonpromotion"]
        try:
            integrity_check(mutant, files=False)
            replay_frontier(result)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
    if len(paths) < 180 or rejected != len(paths):
        raise ValueError(f"hostile mutations accepted: {rejected}/{len(paths)}")

    hostile_json = ['{"a":1,"a":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}']
    json_rejected = 0
    for payload in hostile_json:
        try:
            strict_json(payload)
        except (ValueError, DuplicateKeyError):
            json_rejected += 1
    if json_rejected != len(hostile_json):
        raise ValueError("hostile JSON accepted")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{len(paths)}")
    print(f"HOSTILE_JSON_REJECTED: {json_rejected}/{len(hostile_json)}")
    return rejected + json_rejected


def run_audit(data: dict[str, Any], *, regenerate: bool = True, sidecar: bool = True) -> None:
    integrity_check(data)
    replay_dependencies()
    replay_frontier(data["result"])
    if regenerate:
        deterministic_regeneration(data)
    if sidecar:
        check_sidecar()


def reemit(path: Path, data: dict[str, Any]) -> None:
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
        print(f"ROUND63_GATE24_SATURATION_SQUARE_VERIFY_FAILURE: {exc}")
        return 1

    frontier = data["result"]["strict_nonpromotion"]
    print("SQUARE_DEFECT:", frontier["branch_holonomy_square_defect_identity"])
    print("STABLE_SATURATION_DISTANCE:", frontier["two_plaque_L1_stable_saturation_distance"])
    print("PHYSICAL_HOLONOMY:", frontier["physical_stable_projection_and_two_sided_J_hol"])
    print("GATE2:", frontier["Gate2"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
