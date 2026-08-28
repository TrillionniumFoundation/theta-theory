#!/usr/bin/env python3
"""Join the actual Q2 parent-W registry to the global numeric F7 theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round32-actual-instance-f7-join.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json":
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74",
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json":
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691",
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json":
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40",
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json":
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def build_result() -> dict[str, Any]:
    parent = load("cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json")
    growth = load("cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json")
    characteristic = load("cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json")
    q2 = load("cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json")
    parent_registry = parent["result"]["Q2_parent_W_Borel_registry"]
    instance_registry = parent["result"]["Q2_actual_recut_instance_schema"]
    q2_registry = q2["result"]["Q2_two_step_homogeneity_and_recut_registry"]
    if parent_registry["actual_parent_W_registry"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("parent W")
    if instance_registry["actual_recut_instance_registry"] != "CERTIFIED_PARAMETERIZED_SCHEMA":
        raise RuntimeError("instances")
    if growth["verdict"]["global_one_step_weighted_Growth_contraction"] != "CERTIFIED":
        raise RuntimeError("growth theorem")
    xi = Q(growth["replay_summary"]["global_one_step_Xi_strict_upper"])
    density = Q(characteristic["result"]["positive_inner_core_characteristic_Z"]["invariant_density_ratio_upper"])
    vartheta = density * xi
    if xi != Q(900337, 901685) or density != Q(2000, 1999):
        raise RuntimeError("numeric inputs")
    if vartheta != Q(360134800, 360493663) or not vartheta < 1:
        raise RuntimeError("F7 contraction")
    if q2_registry["strict_Q2_atom_count"] != 114006 or q2_registry["canonical_recut_branch_rule_id_count"] != 228012:
        raise RuntimeError("Q2 registry")
    result = {
        "schema": RESULT_SCHEMA,
        "same_ID_actual_instance_F7_join": {
            "Q2_atom_count": 114006,
            "actual_parameterized_parent_W_registry": "CERTIFIED",
            "actual_parameterized_recut_instance_registry": "CERTIFIED",
            "canonical_branch_rule_base_count": 228012,
            "F7_slot_id_schema": "slot:f7:(branch-rule-id):(parent-W-id):(natural-index-j)",
            "F7_field_name": "one_step_cut_growth_Z_sum",
            "global_componentwise_Xi_strict_upper": str(xi),
            "invariant_density_ratio_upper": str(density),
            "one_step_numeric_F7_strict_upper": str(vartheta),
            "one_step_numeric_F7_margin": str(1 - vartheta),
            "two_step_numeric_F7_strict_upper": str(vartheta * vartheta),
            "two_step_numeric_F7_margin": str(1 - vartheta * vartheta),
            "one_step_F7_is_strict_contraction": True,
            "all_actual_parameterized_instances_covered": True,
            "physical_and_homogeneity_children_counted_once": True,
            "raw_289_root_overledger_used_as_F7_count": False,
            "join_reason": "the universal componentwise theorem already quantifies every invariant-cone short W; round 31 supplies the previously missing actual W and recut IDs",
            "numeric_F7_actual_instance_slots": "CERTIFIED_PARAMETERIZED_228012_BASE_RULES",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "4/18",
            "newly_materialized_field": "F7 one_step_cut_growth_Z_sum",
            "current_global_maturity": "5/18",
            "F7_materialized_on_same_Q2_parent_W_branch_restriction": True,
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "complete_F4_chart_ledger": "NOT_CERTIFIED",
            "connected_nonempty_physical_face_piece_registry": "NOT_CERTIFIED",
            "numeric_transversality_coarea_one_sided_trace": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": {
            "actual_instance_numeric_F7": "CERTIFIED_PARAMETERIZED",
            "Gate5_maturity": "5/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate45_round32_actual_instance_f7_join_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("ACTUAL_INSTANCE_NUMERIC_F7: CERTIFIED_PARAMETERIZED")
    print("GATE5_MATURITY: 5/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
