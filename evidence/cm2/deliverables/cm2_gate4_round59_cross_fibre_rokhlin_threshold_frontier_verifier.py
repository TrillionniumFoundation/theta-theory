#!/usr/bin/env python3
"""Independent verifier for the Round-59 Gate-4 Rokhlin frontier."""

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
CERT_PATH = HERE / "cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_cert.py"
MANIFEST_PATH = HERE / "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json"
REPORT_PATH = HERE / "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-assault-2026-07-20.md"
RESULT_SCHEMA = "cm2.gate4.round59-cross-fibre-rokhlin-threshold-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"

EXPECTED_DEPENDENCIES = {
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json":
        "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json":
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
H = Q(999, 1000)
N = C_P.numerator // C_P.denominator + 1
TEST_BOUND = Q(7_833_600_000, 1999)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


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
    data = strict_load_text(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root")
    return data


def expected_separator_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for m in (2, 10, 1000):
        eps = Q(1, m * N)
        j = 1 + Q(1, m) - Q(1, m * N)
        moment = H * (1 + Q(3, m * N))
        rows.append(
            {
                "m": m,
                "bad_outer_weight": qstr(eps),
                "bad_common_mass": qstr(eps * H),
                "aggregate_J_land_min": qstr(j),
                "aggregate_H": qstr(H),
                "aggregate_normalized_Z": qstr(j / H),
                "aggregate_D_land_dyadic_moment": qstr(moment),
                "good_D_land": 0,
                "bad_D_land": 2,
                "bad_fibre_is_proper": False,
            }
        )
    return rows


def expected_seven_rows() -> list[dict[str, Any]]:
    return [
        {"field": 1, "name": "physical product-rectangle cover of common landing", "actual": "NOT_CERTIFIED"},
        {"field": 2, "name": "stable projection and two-sided Borel holonomy Jacobian", "actual": "NOT_CERTIFIED"},
        {"field": 3, "name": "full-span or quantitatively bounded common fragmentation", "actual": "NOT_CERTIFIED"},
        {"field": 4, "name": "same-measure unstable conditionals with density/log distortion", "actual": "NOT_CERTIFIED"},
        {"field": 5, "name": "physical boundary charge strictly below C_p", "actual": "NOT_CERTIFIED_CONDITIONAL_FORMULA_ONLY"},
        {"field": 6, "name": "Borel branch inverse retaining n/path/ID/owner", "actual": "CERTIFIED_ROUND59"},
        {"field": 7, "name": "strong restriction and assembly", "actual": "NOT_CERTIFIED_WEAK_GRAPH_ASSEMBLY_ONLY"},
    ]


def expected_frontier() -> dict[str, Any]:
    return {
        "physical_J_land_min_total": "CERTIFIED_FINITE_PINNED_ROUND58",
        "physical_D_land_full_dyadic_moment": "CERTIFIED_FINITE_PINNED_ROUND58",
        "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
        "aggregate_to_fibrewise_implication": "CERTIFIED_FALSE_BY_POSITIVE_BAD_FIBRE_SEPARATOR",
        "tagged_Borel_first_return_branch_inverse": "CERTIFIED",
        "weak_same_graph_Rokhlin_reconditioning": "CERTIFIED",
        "seven_field_physical_landing_join": "1/7_ACTUAL_STRONG_JOIN_NOT_CERTIFIED",
        "quantitative_product_rectangle_bridge": "CERTIFIED_CONDITIONAL",
        "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_proper_landing": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def integrity_check(data: dict[str, Any]) -> None:
    if set(data) != {
        "certificate_sha256", "dependencies", "report_sha256", "result",
        "schema", "verdict", "verifier_sha256",
    }:
        raise ValueError("top-level shape")
    if data["schema"] != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if data["dependencies"] != EXPECTED_DEPENDENCIES:
        raise ValueError("dependency registry")
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        if (
            len(expected) != 64 or not path.is_file() or path.is_symlink()
            or path.resolve().parent != HERE or sha256_path(path) != expected
        ):
            raise ValueError(f"dependency integrity: {name}")
    if not CERT_PATH.is_file() or CERT_PATH.is_symlink():
        raise ValueError("certificate path")
    if data["certificate_sha256"] != sha256_path(CERT_PATH):
        raise ValueError("certificate digest")
    if data["verifier_sha256"] != sha256_path(Path(__file__).resolve()):
        raise ValueError("verifier digest")
    if not REPORT_PATH.is_file() or REPORT_PATH.is_symlink():
        raise ValueError("report path")
    if data["report_sha256"] != sha256_path(REPORT_PATH):
        raise ValueError("report digest")
    result = data["result"]
    if result["schema"] != RESULT_SCHEMA:
        raise ValueError("result schema")
    replay = copy.deepcopy(result)
    observed = replay.pop("internal_replay_digest")
    if observed != digest(replay):
        raise ValueError("internal replay digest")
    if data["verdict"] != result["strict_nonpromotion"]:
        raise ValueError("verdict mirror")


def semantic_replay(data: dict[str, Any]) -> None:
    result = data["result"]
    if set(result) != {
        "aggregate_to_fibrewise_separator", "internal_replay_digest",
        "latest_technical_literature_audit", "pinned_round58_audit",
        "provenance", "quantitative_product_rectangle_bridge",
        "same_graph_rokhlin_reconditioning", "schema",
        "seven_field_materialization_audit", "strict_nonpromotion",
    }:
        raise ValueError("result shape")
    provenance = result["provenance"]
    if provenance["dependency_sha256"] != EXPECTED_DEPENDENCIES:
        raise ValueError("provenance dependencies")
    if provenance["old_artifacts_modified"] is not False:
        raise ValueError("append-only guard")
    if provenance["external_theorem_promoted"] is not False:
        raise ValueError("external theorem promotion")

    pinned = result["pinned_round58_audit"]
    if pinned["status"] != "CERTIFIED_PINNED_ROUND58_TYPE_AUDIT":
        raise ValueError("pinned audit")
    if "iff" not in pinned["Round58_exact_iff"]:
        raise ValueError("pinned iff")
    if "conditional join" not in pinned["Round58_seven_field_join"]:
        raise ValueError("pinned seven fields")

    separator = result["aggregate_to_fibrewise_separator"]
    if separator["status"] != "CERTIFIED_AGGREGATE_AND_DLAND_DYADIC_MOMENT_DO_NOT_IMPLY_FIBREWISE_PROPERNESS":
        raise ValueError("separator status")
    if separator["N"] != str(N):
        raise ValueError("separator N")
    if separator["good_z"] != qstr(Q(1) / H):
        raise ValueError("good z")
    if separator["bad_z"] != qstr(Q(N) / H):
        raise ValueError("bad z")
    rows = expected_separator_rows()
    if separator["rows"] != rows or separator["rows_sha256"] != digest(rows):
        raise ValueError("separator rows")
    if not (Q(N - 1) <= C_P < Q(N)):
        raise ValueError("ceiling replay")
    if not (Q(1) / H < C_P < Q(N) / H < 2 * C_P):
        raise ValueError("fibre threshold replay")
    if not (Q(2) / H < C_P):
        raise ValueError("Dcap replay")
    for m in (2, 10, 1000):
        eps = Q(1, m * N)
        j = (1 - eps) + eps * N
        if not (eps * H > 0 and j / H < C_P):
            raise ValueError("positive bad/global proper replay")
    if "do not imply" not in separator["strict_conclusion"]:
        raise ValueError("separator conclusion")

    graph = result["same_graph_rokhlin_reconditioning"]
    if graph["status"] != "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE":
        raise ValueError("graph theorem status")
    if "Lusin-Souslin" not in graph["Borel_inverse_theorem"]:
        raise ValueError("Borel inverse")
    if graph["quotient_law"] != "eta=(q o pr_landing)_#Gamma_cap on U":
        raise ValueError("quotient law")
    if (
        "defined eta-almost everywhere" not in graph["disintegration_identity"]
        or "not division by the singleton mass" not in graph["disintegration_identity"]
    ):
        raise ValueError("measure-typed disintegration")
    if (
        "eta-almost every u" not in graph["conditional_support"]
        or "Gamma_u-almost surely" not in graph["conditional_support"]
        or "not pointwise" not in graph["conditional_support"]
    ):
        raise ValueError("conditional graph support")
    if (
        "same graph measure" not in graph["measure_charge"]
        or "once-charge bookkeeping at measure level" not in graph["measure_charge"]
        or "no pointwise" not in graph["measure_charge"]
    ):
        raise ValueError("measure charge")
    if (
        "Gamma_u-almost surely" not in graph["endpoint_and_tag_typing"]
        or "eta-almost every u" not in graph["endpoint_and_tag_typing"]
    ):
        raise ValueError("endpoint/tag typing")
    if "eta-null quotient set are arbitrary" not in graph["null_set_policy"]:
        raise ValueError("null-set policy")
    if "not yet" not in graph["what_is_not_certified"]:
        raise ValueError("weak/strong guard")

    bridge = result["quantitative_product_rectangle_bridge"]
    if bridge["status"] != "CERTIFIED_CONDITIONAL_QUANTITATIVE_PRODUCT_RECTANGLE_TO_PROPER_LANDING_THEOREM":
        raise ValueError("bridge status")
    if "z_u<=F*R/(theta*L)" not in bridge["boundary_proof"]:
        raise ValueError("bridge proof")
    if bridge["strict_sufficient_inequality"] != "F(u)*R(u)<C_p*theta(u)*L(u) almost everywhere":
        raise ValueError("bridge inequality")
    arithmetic = bridge["arithmetic_only_replay"]
    if arithmetic != {
        "F": 153, "R": "2000/1999", "theta": "1/2", "L": "1/12800",
        "F_R_over_theta_L": qstr(TEST_BOUND), "strictly_below_C_p": True,
    }:
        raise ValueError("bridge arithmetic row")
    if not (TEST_BOUND == Q(153) * Q(2000, 1999) / (Q(1, 2) * Q(1, 12800)) < C_P):
        raise ValueError("bridge independent arithmetic")
    if "not physically joinable" not in bridge["misaligned_field_guard"]:
        raise ValueError("misaligned guard")

    audit = result["seven_field_materialization_audit"]
    seven = expected_seven_rows()
    if audit["rows"] != seven or audit["rows_sha256"] != digest(seven):
        raise ValueError("seven-field rows")
    if audit["actual_complete_rows"] != "1/7":
        raise ValueError("seven-field count")
    if audit["official_Gate2_fields_unchanged"] != "0/17":
        raise ValueError("Gate2 no-promotion")

    literature = result["latest_technical_literature_audit"]
    if literature["status"] != "AUDITED_MME_LOCAL_PRODUCT_THEOREM_NOT_A_CM2_LANDING_PROPERISATION":
        raise ValueError("literature status")
    if literature["external_theorem_promoted"] is not False:
        raise ValueError("literature promotion")
    if len(literature["official_sources"]) != 2:
        raise ValueError("literature sources")
    if "not the pinned Liouville/SRB" not in literature["MME_type_audit"]:
        raise ValueError("MME type guard")

    if result["strict_nonpromotion"] != expected_frontier():
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
        (("report_sha256",), "0" * 64),
        (("dependencies", next(iter(EXPECTED_DEPENDENCIES))), "0" * 64),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "external_theorem_promoted"), True),
        (("result", "pinned_round58_audit", "status"), "NOT_CERTIFIED"),
        (("result", "pinned_round58_audit", "Round58_exact_iff"), "finite only"),
        (("result", "pinned_round58_audit", "Round58_seven_field_join"), "closed"),
        (("result", "aggregate_to_fibrewise_separator", "status"), "CERTIFIED_PROPER"),
        (("result", "aggregate_to_fibrewise_separator", "N"), "1"),
        (("result", "aggregate_to_fibrewise_separator", "good_z"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "bad_z"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "m"), 3),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "bad_outer_weight"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "bad_common_mass"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "aggregate_J_land_min"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "aggregate_H"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "aggregate_normalized_Z"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "aggregate_D_land_dyadic_moment"), "0"),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "bad_D_land"), 0),
        (("result", "aggregate_to_fibrewise_separator", "rows", 0, "bad_fibre_is_proper"), True),
        (("result", "aggregate_to_fibrewise_separator", "rows_sha256"), "0" * 64),
        (("result", "aggregate_to_fibrewise_separator", "strict_conclusion"), "implies"),
        (("result", "same_graph_rokhlin_reconditioning", "status"), "NOT_CERTIFIED"),
        (("result", "same_graph_rokhlin_reconditioning", "Borel_inverse_theorem"), "nonmeasurable"),
        (("result", "same_graph_rokhlin_reconditioning", "quotient_law"), "eta({u})"),
        (("result", "same_graph_rokhlin_reconditioning", "disintegration_identity"), "divide by eta({u})"),
        (("result", "same_graph_rokhlin_reconditioning", "conditional_support"), "pointwise all u"),
        (("result", "same_graph_rokhlin_reconditioning", "measure_charge"), "pointwise no deletion"),
        (("result", "same_graph_rokhlin_reconditioning", "endpoint_and_tag_typing"), "pointwise endpoints"),
        (("result", "same_graph_rokhlin_reconditioning", "null_set_policy"), "all null representatives canonical"),
        (("result", "same_graph_rokhlin_reconditioning", "what_is_not_certified"), "everything certified"),
        (("result", "quantitative_product_rectangle_bridge", "status"), "CERTIFIED_PHYSICAL"),
        (("result", "quantitative_product_rectangle_bridge", "boundary_proof"), "z=0"),
        (("result", "quantitative_product_rectangle_bridge", "strict_sufficient_inequality"), "F finite"),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "F"), 1),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "R"), "1"),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "theta"), "1"),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "L"), "1"),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "F_R_over_theta_L"), "0"),
        (("result", "quantitative_product_rectangle_bridge", "arithmetic_only_replay", "strictly_below_C_p"), False),
        (("result", "quantitative_product_rectangle_bridge", "misaligned_field_guard"), "physically joined"),
        (("result", "seven_field_materialization_audit", "status"), "CLOSED"),
        (("result", "seven_field_materialization_audit", "rows", 0, "actual"), "CERTIFIED"),
        (("result", "seven_field_materialization_audit", "rows", 5, "actual"), "NOT_CERTIFIED"),
        (("result", "seven_field_materialization_audit", "rows", 6, "actual"), "CERTIFIED"),
        (("result", "seven_field_materialization_audit", "rows_sha256"), "0" * 64),
        (("result", "seven_field_materialization_audit", "actual_complete_rows"), "7/7"),
        (("result", "seven_field_materialization_audit", "official_Gate2_fields_unchanged"), "17/17"),
        (("result", "latest_technical_literature_audit", "status"), "THEOREM_FOUND"),
        (("result", "latest_technical_literature_audit", "external_theorem_promoted"), True),
        (("result", "latest_technical_literature_audit", "official_sources"), []),
        (("result", "latest_technical_literature_audit", "MME_type_audit"), "same SRB law"),
        (("result", "strict_nonpromotion", "fibrewise_J_land_min_below_Cp_h"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "aggregate_to_fibrewise_implication"), "CERTIFIED_TRUE"),
        (("result", "strict_nonpromotion", "tagged_Borel_first_return_branch_inverse"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "weak_same_graph_Rokhlin_reconditioning"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "seven_field_physical_landing_join"), "7/7"),
        (("result", "strict_nonpromotion", "quantitative_product_rectangle_bridge"), "CERTIFIED_UNCONDITIONAL"),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_landing_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "intermediate_C24_avoidance_after_proper_landing"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        (("verdict", "Gate4"), "CERTIFIED"),
    ]
    rejected = 0
    accepted: list[tuple[Any, ...]] = []
    for path, value in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        try:
            validate(candidate)
        except (OSError, ValueError, RuntimeError, KeyError, TypeError):
            rejected += 1
        else:
            accepted.append(path)
    strict_cases = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '[1,2,3]')
    for payload in strict_cases:
        try:
            value = strict_load_text(payload)
            if not isinstance(value, dict):
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
        print(f"ROUND59_GATE4_ROKHLIN_VERIFIER_FAILURE: {exc}", file=sys.stderr)
        return 1

    if args.integrity_only or args.replay:
        print("ROUND59_GATE4_ROKHLIN_INTEGRITY: PASS")
        print("AGGREGATE_SEPARATOR_AND_PRODUCT_BRIDGE_REPLAY: PASS")
        print("NO_GATE_PROMOTION: PASS")
        return 0

    strict = data["result"]["strict_nonpromotion"]
    print("BRANCH_INVERSE:", strict["tagged_Borel_first_return_branch_inverse"])
    print("SEVEN_FIELD_JOIN:", strict["seven_field_physical_landing_join"])
    print("PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
