#!/usr/bin/env python3
"""Independent verifier for the Round-62 Gate-4/2 branch/current frontier."""

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
RESULT_SCHEMA = "cm2.gate42.round62-branch-covariance-graph-cylinder-current-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
CERT = HERE / "cm2_gate42_round62_branch_covariance_graph_cylinder_current_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_RESULT_DIGEST = "4bb5f0da16de9a35d50d9ef6088e8035e7402c70055648e2de8cb592a61dae96"

DEPENDENCIES = {
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
}

BASELINE = {
    "cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-assault-2026-07-20.md":
        "e99800b998a2fc547229a6b2a93dd84433634af76c691ef65c37b9024fc0d45c",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.sha256":
        "a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2",
    "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_cert.py":
        "0edb32c9572cbf3dc7ba4ef500a0ec011c379c19f42cc581c0e095176dc20f82",
    "cm2_gate4_round61_marker_weighted_curve_defect_ledger_frontier_verifier.py":
        "0dfa89b59db7567b871219878011a77db177f857af9daab92665a927a486a23a",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-assault-2026-07-20.md":
        "94d943e25c3f43a909f0ec691fe86f43848f41228da5378fa16a94405654dea6",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
}

EXPECTED_STRICT = {
    "actual_first_return_branch_RN_covariance": "CERTIFIED_EXACT",
    "physical_stable_holonomy_marker_covariance": "NOT_CERTIFIED",
    "holonomy_defect_isometry_cocycle_interface": "CERTIFIED_EXACT",
    "physical_invariant_product_quotient_and_J_hol": "NOT_CERTIFIED",
    "fibrewise_FR_below_Cp_theta_L": "NOT_CERTIFIED",
    "tagged_graph_cylinder_normal_current": "CERTIFIED_EXACT",
    "D_land_pays_cylinder_current_norms": "CERTIFIED_EXACT",
    "physical_anisotropic_current_Piola_recipient": "NOT_CERTIFIED",
    "downstream_accepts_positive_bad_current": "NOT_CERTIFIED",
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
    for path in (CERT, VERIFIER, REPORT):
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise ValueError(f"artifact path: {path.name}")


def replay_dependencies() -> None:
    gate4 = load_dependency(
        "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json"
    )
    if gate4["seven_field_materialization_audit"]["actual_complete_rows"] != "1/7":
        raise ValueError("Round61 Gate4 fields")
    graph = gate4["weighted_graph_defect_lattice"]
    if graph["sample_total_mass"] != "53/320" or graph["sample_weighted_norm"] != "7/5":
        raise ValueError("Round61 graph atoms")
    if "a=g_B after transport" not in gate4["actual_marker_weighted_curve_lift"]["source_marker"]:
        raise ValueError("Round61 source marker")

    gate123 = load_dependency(
        "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json"
    )
    gate2 = gate123["gate2"]
    if gate2["marker_holonomy_compatibility"]["status"] != "CERTIFIED_EXACT_MARKER_HOLONOMY_INTERFACE":
        raise ValueError("Round61 holonomy interface")
    physical = gate2["physical_boundary"]
    if physical["landing_join"] != "1/7" or physical["official_immutable_gate2_fields"] != "0/17":
        raise ValueError("Round61 Gate2 boundary")
    if physical["physical_marker_covariance_equation"] != "NOT_CERTIFIED":
        raise ValueError("Round61 physical covariance")


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


def replay_branch(result: dict[str, Any]) -> None:
    section = result["actual_branch_RN_covariance"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("branch replay digest")
    mu_u = [Q(x) for x in replay["mu_U"]]
    marker = [Q(x) for x in replay["source_marker_a"]]
    image = replay["H_image"]
    mu_v = [Q(0)] * 3
    kappa_v = [Q(0)] * 3
    for i, j in enumerate(image):
        mu_v[j] += mu_u[i]
        kappa_v[j] += mu_u[i] * marker[i]
    marker_v = [k / m for k, m in zip(kappa_v, mu_v)]
    inverse = [image.index(j) for j in range(3)]
    transported = [marker[inverse[j]] for j in range(3)]
    if marker_v != transported:
        raise ValueError("branch covariance")
    if [str(x) for x in marker_v] != replay["landing_marker_g_B"]:
        raise ValueError("branch marker rows")
    if section["status"] != "CERTIFIED_EXACT_ACTUAL_TAGGED_FIRST_RETURN_BRANCH_RN_COVARIANCE__NOT_STABLE_HOLONOMY_COVARIANCE":
        raise ValueError("branch status")
    if "no extra J_ell H" not in section["jacobian_guard"]:
        raise ValueError("branch Jacobian guard")


def replay_holonomy(result: dict[str, Any]) -> None:
    section = result["stable_holonomy_marker_defect"]
    replay = section["finite_replay"]
    if digest(replay) != section["finite_replay_sha256"]:
        raise ValueError("holonomy replay digest")
    mu = [Q(x) for x in replay["reference_law_each_fibre"]]
    g_u = [Q(x) for x in replay["g_u"]]
    g_v = [Q(x) for x in replay["g_v"]]
    g_w = [Q(x) for x in replay["g_w"]]
    uv = [v - u for u, v in zip(g_u, g_v)]
    vw = [w - v for v, w in zip(g_v, g_w)]
    uw = [w - u for u, w in zip(g_u, g_w)]
    if uw != [a + b for a, b in zip(uv, vw)]:
        raise ValueError("defect cocycle")
    l1 = lambda values: sum((m * abs(x) for m, x in zip(mu, values)), Q(0))
    if (l1(uv), l1(vw), l1(uw)) != (Q(1, 6), Q(1, 6), Q(1, 3)):
        raise ValueError("defect norms")
    if section["status"] != "CERTIFIED_EXACT_POSITIVE_L1_ISOMETRY_AND_MARKER_DEFECT_COCYCLE_INTERFACE__PHYSICAL_HOLONOMY_ABSENT":
        raise ValueError("holonomy status")


def replay_current(result: dict[str, Any]) -> None:
    section = result["tagged_graph_cylinder_current"]
    replay = section["replay"]
    if digest(replay) != section["replay_sha256"]:
        raise ValueError("current replay digest")
    total = Q(0)
    weighted = Q(0)
    for row in replay["atoms"]:
        mass = Q(row["mass"])
        weight = Q(row["weight"])
        if weight != 2 ** int(row["D_land"]):
            raise ValueError("current weight")
        if Q(row["weighted_mass"]) != mass * weight:
            raise ValueError("current weighted atom")
        if Q(row["recovered_mass"]) != mass:
            raise ValueError("current recovery")
        total += mass
        weighted += mass * weight
    if total != Q(53, 320) or weighted != Q(7, 5):
        raise ValueError("current totals")
    if Q(replay["ordinary_boundary_mass"]) != 2 * total:
        raise ValueError("ordinary boundary")
    if Q(replay["weighted_boundary_mass"]) != 2 * weighted:
        raise ValueError("weighted boundary")
    if "weighted current traces are w*nu, not nu" not in section["weighted_charge_guard"]:
        raise ValueError("weighted charge guard")
    rows = section["five_interface_rows"]
    if digest(rows) != section["five_interface_rows_sha256"] or len(rows) != 5:
        raise ValueError("current interface rows")
    if section["cylinder_rows_complete"] != "4/5" or rows[-1]["cylinder_current"] != "NOT_CERTIFIED":
        raise ValueError("current completion")
    if section["status"] != "CERTIFIED_EXACT_ENDPOINT_TRACED_NORMAL_METRIC_CURRENT_ON_TAGGED_GRAPH_CYLINDER__DOWNSTREAM_PHYSICAL_ACCEPTANCE_ABSENT":
        raise ValueError("current status")


def replay_semantics(result: dict[str, Any]) -> None:
    if result.get("schema") != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay_branch(result)
    replay_holonomy(result)
    replay_current(result)
    separator = result["graph_to_physical_current_type_separator"]
    if separator["status"] != "CERTIFIED_TYPE_SEPARATOR__GRAPH_CYLINDER_CURRENT_DOES_NOT_PROMOTE_TO_PHYSICAL_CURRENT":
        raise ValueError("separator status")
    fields = result["seven_field_materialization_audit"]
    if fields["complete_rows"] != "1/7" or fields["partial_rows"] != [1, 4, 7]:
        raise ValueError("field count")
    if fields["official_immutable_Gate2_fields"] != "0/17" or digest(fields["rows"]) != fields["rows_sha256"]:
        raise ValueError("field rows")
    if result["strict_nonpromotion"] != EXPECTED_STRICT:
        raise ValueError("strict frontier")
    if result["latest_official_technology_audit"]["external_theorem_promoted"] is not False:
        raise ValueError("external promotion")
    if "ordinary collision-SRB" not in result["downstream_typing"]["cemetery"]:
        raise ValueError("cemetery typing")


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
    if produced != data or proc.stdout.encode("utf-8") != MANIFEST.read_bytes():
        raise ValueError("producer replay mismatch")


def deep_scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    paths: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "internal_replay_digest":
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
    paths = deep_scalar_paths(data["result"])[:180]
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
            replay_semantics(result)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
    if len(paths) < 140 or rejected != len(paths):
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


def run_audit(data: dict[str, Any], *, regenerate: bool = True) -> None:
    integrity_check(data)
    replay_dependencies()
    replay_semantics(data["result"])
    if regenerate:
        deterministic_regeneration(data)


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
        print(f"ROUND62_GATE42_BRANCH_CURRENT_VERIFY_FAILURE: {exc}")
        return 1

    frontier = data["result"]["strict_nonpromotion"]
    print("BRANCH_RN_COVARIANCE:", frontier["actual_first_return_branch_RN_covariance"])
    print("GRAPH_CYLINDER_CURRENT:", frontier["tagged_graph_cylinder_normal_current"])
    print("PHYSICAL_CURRENT:", frontier["physical_anisotropic_current_Piola_recipient"])
    print("GATE2:", frontier["Gate2"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
