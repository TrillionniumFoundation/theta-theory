#!/usr/bin/env python3
"""Fail-closed verifier for the round-36 compact-germ F10 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import cm2_gate5_round36_compact_germ_f10_frontier_cert as cert


def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in rows:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load(path)
        if set(manifest) != {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        }:
            errors.append("top-level keys")
        if manifest.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("schema")
        if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        expected = cert.build_result()
        if manifest.get("result") != expected:
            errors.append("result")
        if manifest.get("verdict") != expected["strict_nonpromotion"]:
            errors.append("verdict")

        result = manifest["result"]
        universe = result["compact_regular_face_germ_universe"]
        if tuple(universe["physical_face_kinds"]) != cert.FACE_KINDS:
            errors.append("face kinds")
        if universe["every_regular_noncorner_face_point_has_a_closure_contained_compact_germ"] is not True:
            errors.append("germ coverage")
        if universe["instantiated_compact_germ_rows"] != 0:
            errors.append("materialized germs")

        theorem = result["analytic_coarea_C1_compactness_theorem"]
        if theorem["log_density_not_required_at_zeros"] is not True:
            errors.append("zero density policy")
        if theorem["carrier_C2_is_not_retyped_as_density_regularity"] is not True:
            errors.append("type safety")

        search = result["canonical_dyadic_radius_and_F10_search"]
        if search["radius_search_terminates_for_every_compact_regular_germ"] is not True:
            errors.append("radius termination")
        if search["bound_search_terminates_for_every_compact_regular_germ"] is not True:
            errors.append("bound termination")
        if search["canonical_finite_integer_F10_value_exists_for_each_germ"] is not True:
            errors.append("finite F10")
        if search["uniform_radius_or_integer_over_all_germs"] != "NOT_ASSERTED":
            errors.append("uniformity")
        if search["weighted_sum_of_N_F10_over_faces_or_components"] != "NOT_CERTIFIED":
            errors.append("summability")
        if search["materialized_N_F10_values"] != 0:
            errors.append("numeric materialization")

        matrix = result["five_face_kind_compact_germ_F10_matrix"]
        if set(matrix) != set(cert.FACE_KINDS) or len(matrix) != len(cert.FACE_KINDS):
            errors.append("matrix kinds")
        if matrix["source_core_clipping_face"]["compact_germ_F10"] != (
            "CERTIFIED_LEVEL_ZERO_STATIONARY_CURRENT"
        ):
            errors.append("source core")
        for kind in cert.FACE_KINDS:
            if matrix[kind]["global_F10"] != "NOT_CERTIFIED":
                errors.append(f"global F10: {kind}")

        scope = result["strict_nonpromotion"]
        if scope["compact_regular_germ_F10_finite_search_schema"] != "CERTIFIED":
            errors.append("schema verdict")
        if scope["pointwise_compact_germ_schema_is_complete_global_F10_field"] is not False:
            errors.append("global field nonpromotion")
        if scope["global_rank_path_F10_Lp_or_weighted_sum"] != "NOT_CERTIFIED":
            errors.append("weighted F10")
        if scope["complete_F10_all_face_coarea_regular_atlas"] != "NOT_CERTIFIED":
            errors.append("complete F10")
        if scope["Gate5_maturity"] != "7/18_UNCHANGED":
            errors.append("maturity")
        if scope["complete_18_field_operator_block_count"] != 0:
            errors.append("blocks")
        if scope["Gate5"] != "NOT_CERTIFIED":
            errors.append("Gate5")
        if scope["CM2"] != "NO-GO_FOR_CLAIM":
            errors.append("CM2")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def self_test(path: Path) -> tuple[int, int]:
    source = load(path)
    mutations: list[dict[str, Any]] = []

    direct_edits = [
        (
            "compact_regular_face_germ_universe",
            "instantiated_compact_germ_rows",
            1,
        ),
        (
            "compact_regular_face_germ_universe",
            "every_regular_noncorner_face_point_has_a_closure_contained_compact_germ",
            False,
        ),
        (
            "analytic_coarea_C1_compactness_theorem",
            "carrier_C2_is_not_retyped_as_density_regularity",
            False,
        ),
        (
            "canonical_dyadic_radius_and_F10_search",
            "radius_search_terminates_for_every_compact_regular_germ",
            False,
        ),
        (
            "canonical_dyadic_radius_and_F10_search",
            "bound_search_terminates_for_every_compact_regular_germ",
            False,
        ),
        (
            "canonical_dyadic_radius_and_F10_search",
            "uniform_radius_or_integer_over_all_germs",
            "CERTIFIED",
        ),
        (
            "canonical_dyadic_radius_and_F10_search",
            "weighted_sum_of_N_F10_over_faces_or_components",
            "CERTIFIED",
        ),
        (
            "canonical_dyadic_radius_and_F10_search",
            "materialized_N_F10_values",
            1,
        ),
    ]
    for section, key, value in direct_edits:
        mutation = copy.deepcopy(source)
        mutation["result"][section][key] = value
        mutations.append(mutation)

    mutation = copy.deepcopy(source)
    mutation["result"]["compact_regular_face_germ_universe"][
        "physical_face_kinds"
    ].pop()
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_compact_germ_F10_matrix"][
        "terminal_core_preimage_face"
    ]["global_F10"] = "CERTIFIED"
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["result"]["five_face_kind_compact_germ_F10_matrix"][
        "source_core_clipping_face"
    ]["compact_germ_F10"] = "CERTIFIED_POSITIVE_CURRENT"
    mutations.append(mutation)

    strict_edits = [
        ("pointwise_compact_germ_schema_is_complete_global_F10_field", True),
        ("global_rank_path_F10_Lp_or_weighted_sum", "CERTIFIED"),
        ("complete_F10_all_face_coarea_regular_atlas", "CERTIFIED"),
        ("Gate5_maturity", "8/18"),
        ("complete_18_field_operator_block_count", 1),
        ("Gate5", "CERTIFIED"),
        ("CM2", "CERTIFIED"),
    ]
    for key, value in strict_edits:
        mutation = copy.deepcopy(source)
        mutation["result"]["strict_nonpromotion"][key] = value
        mutation["verdict"][key] = value
        mutations.append(mutation)

    mutation = copy.deepcopy(source)
    mutation["certificate_sha256"] = "0" * 64
    mutations.append(mutation)
    mutation = copy.deepcopy(source)
    mutation["dependencies"] = {}
    mutations.append(mutation)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            target = Path(directory) / f"mutation-{index}.json"
            target.write_text(json.dumps(mutation), encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("COMPLETE_GLOBAL_F10_FIELD: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
