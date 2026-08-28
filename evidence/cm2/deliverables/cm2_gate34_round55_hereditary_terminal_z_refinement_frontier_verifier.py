#!/usr/bin/env python3
"""Independent verifier for the Round-55 hereditary terminal-Z leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT_PATH = (
    HERE / "cm2_gate34_round55_hereditary_terminal_z_refinement_frontier_cert.py"
)
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json"
)
EXPECTED_SCHEMA = (
    "cm2.gate34.round55-hereditary-terminal-z-refinement-frontier.v1.manifest.v1"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json": (
        "941929e86bdecd1d3fc8d935ed685b346ea2bedc3fba0c24bd949f5f88b66c2f"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
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
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_certificate_module() -> Any:
    spec = importlib.util.spec_from_file_location("round55_terminal_cert", CERT_PATH)
    require(spec is not None and spec.loader is not None, "certificate import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_json_tree(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, str, int)):
        return
    if isinstance(value, float):
        require(math.isfinite(value), f"non-finite float at {path}")
        raise RuntimeError(f"floating JSON number forbidden at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            check_json_tree(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str), f"non-string key at {path}")
            check_json_tree(item, f"{path}.{key}")
        return
    raise RuntimeError(f"unsupported JSON type at {path}: {type(value).__name__}")


def independent_replay(manifest: dict[str, Any]) -> None:
    require(
        set(manifest)
        == {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        },
        "top-level keys",
    )
    require(manifest["schema"] == EXPECTED_SCHEMA, "manifest schema")
    require(manifest["dependencies"] == EXPECTED_DEPENDENCIES, "dependency map")
    require(
        manifest["certificate_sha256"] == sha256_path(CERT_PATH),
        "certificate hash",
    )
    require(
        manifest["verifier_sha256"] == sha256_path(Path(__file__).resolve()),
        "verifier hash",
    )
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency safety: {name}")
        require(path.resolve().parent == HERE, f"dependency parent: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")

    result = manifest["result"]
    require(
        result["provenance"]["dependency_sha256"] == manifest["dependencies"],
        "provenance parity",
    )
    require(manifest["verdict"] == result["strict_nonpromotion"], "verdict parity")

    all_mass = result["all_mass_extra_cut_one_step_replay"]
    recomputed_z1 = Q(2000, 1999) * 49 * Q(900337, 901685) + 2
    require(
        recomputed_z1 == Q(18367592526, 360493663), "Z1 rational replay"
    )
    require(
        all_mass["all_mass_one_step_Z_multiplier_Z1"] == qstr(recomputed_z1),
        "Z1 manifest",
    )
    require(all_mass["all_mass_not_survivor_operator"] is True, "operator type")
    require(
        all_mass["status"] == "CERTIFIED_NUMERICAL_ALL_MASS_ONE_STEP_REPLAY",
        "all-mass status",
    )

    survivor = result["all_time_killed_survivor_Z_join"]
    expected_rows = []
    for j in range(5):
        expected_rows.append(
            {
                "residue_j": j,
                "bound": f"Z(F_(pL+{j}))<=Z1^{j}*z_p",
                "Z1_power": qstr(recomputed_z1**j),
            }
        )
    require(survivor["sample_residue_rows"] == expected_rows, "residue rows")
    require(
        survivor["sample_residue_rows_sha256"] == digest(expected_rows),
        "residue digest",
    )
    require(survivor["N_open_materialized"] is False, "N_open boundary")
    require(
        survivor["typing_joins"]["status"]
        == "CERTIFIED_SAME_ID_OPERATOR_AND_INITIAL_FAMILY_JOIN",
        "same-ID typing join",
    )
    require(
        survivor["typing_joins"]["C_s_equals_C24_mod_frozen_faces"].startswith(
            "Round27 identifies C_s"
        ),
        "C_s/C24 typing",
    )
    require(
        "m_base" in survivor["unweighted_block_resolvent"]
        and "m_0" not in survivor["unweighted_block_resolvent"],
        "dominating base mass typing",
    )
    require(
        survivor["explicit_block_symbols"]["rho"]
        == "(111718729/111718750)^9148<1",
        "block rho",
    )
    require(
        survivor["status"]
        == "CERTIFIED_PHYSICAL_ALL_COLLISION_SURVIVOR_Z_L1_FINITE_NONNUMERIC_N_OPEN",
        "survivor status",
    )

    terminal = result["two_orientation_coarse_terminal_Z_join"]
    require(terminal["Phi_pair_used"] is False, "Phi use")
    require(terminal["physical_cell_refinement_included"] is False, "refinement type")
    require(
        terminal["status"]
        == "CERTIFIED_TWO_ORIENTATION_COARSE_TERMINAL_Z_L1_FINITE_NONNUMERIC_N_OPEN",
        "terminal status",
    )

    gap = result["official_gap_cutpoint_density_audit"]
    require(gap["strict_ratio_comparison"] == "11/9>2000/1999", "gap ratio")
    require(gap["zero_density_debit_join"] == "REJECTED", "gap no-go")
    require(gap["same_ID_canonical_chop_repairs_entry_length"] is False, "gap chop")
    require(gap["moving_sequence_Growth_claimed"] is False, "stationary scope")

    refinement = result["physical_cell_refinement_frontier"]
    expected_growth_rows = []
    for n in (1, 2, 3, 5, 8):
        expected_growth_rows.append(
            {
                "path_depth_n": n,
                "all_ranks_B_i": 14,
                "additive_D1": f"2473984*{n}",
                "image_recut_product_model": f"2457600^{n}",
                "claim_physical_path_has_constant_rank": False,
            }
        )
    require(
        refinement["constant_rank_growth_rows"] == expected_growth_rows,
        "refinement rows",
    )
    require(
        refinement["constant_rank_growth_rows_sha256"]
        == digest(expected_growth_rows),
        "refinement row digest",
    )
    require(refinement["countermodel_asserted_physical"] is False, "countermodel scope")
    require(refinement["physical_J_pair"] == "NOT_CERTIFIED", "J_pair frontier")

    frontier = result["strict_nonpromotion"]
    require(
        frontier["Phi_pair_l1_needed_for_coarse_terminal_Z"]
        == "BYPASSED_BY_HEREDITARY_EVERY_COLLISION_KILLED_GROWTH",
        "bypass verdict",
    )
    require(frontier["Phi_pair_l1_itself"] == "NOT_CERTIFIED", "Phi nonpromotion")
    require(frontier["physical_J_pair"] == "NOT_CERTIFIED", "Jpair nonpromotion")
    require(frontier["Gate4"] == "NOT_CERTIFIED", "Gate4 nonpromotion")
    require(frontier["complete_composite_gates"] == "0/5", "gate count")
    require(frontier["CM2"] == "NO-GO_FOR_CLAIM", "CM2 nonpromotion")

    digest_copy = copy.deepcopy(result)
    embedded = digest_copy.pop("internal_replay_digest")
    require(embedded == digest(digest_copy), "internal replay digest")


def verify_object(manifest: Any) -> None:
    require(isinstance(manifest, dict), "manifest root")
    check_json_tree(manifest)
    independent_replay(manifest)
    module = load_certificate_module()
    expected = module.build_manifest(Path(__file__).resolve())
    require(canonical_json(manifest) == canonical_json(expected), "producer replay mismatch")


def verify_path(path: Path) -> dict[str, Any]:
    require(path.is_file(), "manifest missing")
    require(not path.is_symlink(), "manifest symlink")
    require(path.resolve().parent == HERE, "manifest outside deliverables")
    raw = path.read_text(encoding="utf-8")
    manifest = parse_json_text(raw)
    verify_object(manifest)
    expected_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    require(raw == expected_text, "manifest bytes are not canonical pretty JSON")
    return manifest


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def hostile_mutations(base: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    def changed(path: tuple[str, ...], replacement: Any) -> None:
        item = copy.deepcopy(base)
        set_path(item, path, replacement)
        mutations.append(item)

    changed(("schema",), EXPECTED_SCHEMA + ".promoted")
    changed(("certificate_sha256",), "0" * 64)
    changed(("verifier_sha256",), "f" * 64)
    item = copy.deepcopy(base)
    item["dependencies"].pop(next(iter(EXPECTED_DEPENDENCIES)))
    mutations.append(item)
    changed(
        ("dependencies", "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"),
        "1" * 64,
    )
    changed(
        ("result", "provenance", "old_artifacts_modified"), True
    )
    changed(
        ("result", "provenance", "parameter_scope"), "moving arbitrary sequence"
    )
    changed(
        ("result", "all_mass_extra_cut_one_step_replay", "all_mass_not_survivor_operator"),
        False,
    )
    changed(
        ("result", "all_mass_extra_cut_one_step_replay", "all_mass_one_step_Z_multiplier_Z1"),
        "1",
    )
    changed(
        ("result", "all_mass_extra_cut_one_step_replay", "status"),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "N_open_materialized"), True
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "typing_joins", "status"),
        "NOT_CERTIFIED",
    )
    changed(
        (
            "result",
            "all_time_killed_survivor_Z_join",
            "typing_joins",
            "C_s_equals_C24_mod_frozen_faces",
        ),
        "NOT_JOINED",
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "unweighted_block_resolvent"),
        "sum z<=constant*m_0",
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "normalisation_used"), True
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "sample_residue_rows_sha256"),
        "2" * 64,
    )
    changed(
        ("result", "all_time_killed_survivor_Z_join", "status"),
        "CERTIFIED_NUMERICAL_COLLISION_RATE",
    )
    changed(
        ("result", "two_orientation_coarse_terminal_Z_join", "Phi_pair_used"), True
    )
    changed(
        ("result", "two_orientation_coarse_terminal_Z_join", "physical_cell_refinement_included"),
        True,
    )
    changed(
        ("result", "two_orientation_coarse_terminal_Z_join", "status"),
        "CERTIFIED_PHYSICAL_J_PAIR",
    )
    changed(
        ("result", "official_gap_cutpoint_density_audit", "strict_ratio_comparison"),
        "11/9<2000/1999",
    )
    changed(
        ("result", "official_gap_cutpoint_density_audit", "zero_density_debit_join"),
        "CERTIFIED",
    )
    changed(
        ("result", "official_gap_cutpoint_density_audit", "same_ID_canonical_chop_repairs_entry_length"),
        True,
    )
    changed(
        ("result", "official_gap_cutpoint_density_audit", "moving_sequence_Growth_claimed"),
        True,
    )
    changed(
        ("result", "physical_cell_refinement_frontier", "global_integrability_of_K_mult_pair"),
        "CERTIFIED",
    )
    changed(
        ("result", "physical_cell_refinement_frontier", "countermodel_asserted_physical"),
        True,
    )
    changed(
        ("result", "physical_cell_refinement_frontier", "constant_rank_growth_rows_sha256"),
        "3" * 64,
    )
    changed(
        ("result", "physical_cell_refinement_frontier", "physical_J_pair"),
        "CERTIFIED",
    )
    changed(
        ("result", "physical_cell_refinement_frontier", "physical_I_D"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "Phi_pair_l1_itself"), "CERTIFIED"
    )
    changed(
        ("result", "strict_nonpromotion", "physical_J_pair"), "CERTIFIED"
    )
    changed(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "complete_composite_gates"), "1/5")
    changed(("result", "strict_nonpromotion", "CM2"), "GO")
    changed(("result", "internal_replay_digest"), "4" * 64)
    changed(("verdict", "Gate4"), "CERTIFIED")
    item = copy.deepcopy(base)
    item["unexpected"] = "field"
    mutations.append(item)
    return mutations


def run_self_test(base: dict[str, Any]) -> int:
    rejected = 0
    mutations = hostile_mutations(base)
    for index, item in enumerate(mutations):
        try:
            verify_object(item)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"hostile mutation accepted: {index}")

    raw_attacks = [
        '{"schema":"a","schema":"b"}',
        '{"x":NaN}',
        '{"x":Infinity}',
    ]
    for raw in raw_attacks:
        try:
            parse_json_text(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"hostile raw JSON accepted: {raw}")
    total = len(mutations) + len(raw_attacks)
    require(rejected == total, "self-test rejection count")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit-manifest", action="store_true")
    args = parser.parse_args()

    manifest = verify_path(args.manifest)
    if args.self_test:
        return run_self_test(manifest)
    if args.reemit_manifest:
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0
    print("AUDIT_MODE: PASS")
    print(
        "COARSE_TERMINAL_Z:",
        manifest["verdict"]["two_orientation_coarse_terminal_Z_l1"],
    )
    print("PHYSICAL_J_PAIR:", manifest["verdict"]["physical_J_pair"])
    print("GATE4:", manifest["verdict"]["Gate4"])
    print("CM2:", manifest["verdict"]["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    raise SystemExit(main())
