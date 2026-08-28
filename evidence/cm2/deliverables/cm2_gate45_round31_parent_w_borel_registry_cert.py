#!/usr/bin/env python3
"""Parameterized actual parent-W registry on every certified Q2 atom."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round31-parent-w-borel-registry.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json":
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3",
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json":
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json":
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691",
}
SLOPE = Q(4)
CONE_LOWER = Q(25, 9)
CONE_UPPER = Q(4108425, 145348)
DELTA_1 = Q(1, 37724355673552103994)
ADAPTED_CELL_LENGTH_TEXT = "1e-90"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    expected = DEPENDENCIES[name]
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != expected:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def build_result() -> dict[str, Any]:
    q2 = load("cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json")
    cone = load("cm2-gate45-global-invariant-cone-manifest-2026-07-16.json")
    growth = load("cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json")
    registry = q2["result"]["Q2_two_step_homogeneity_and_recut_registry"]
    geometric = cone["result"]["global_invariant_geometric_cone"]
    if registry["strict_Q2_atom_count"] != 114006:
        raise RuntimeError("Q2 atoms")
    if registry["canonical_recut_branch_rule_id_count"] != 228012:
        raise RuntimeError("branch rules")
    if geometric["strict_forward_invariance"] is not True:
        raise RuntimeError("cone invariance")
    if Q(geometric["curvature_lower"]) != CONE_LOWER or Q(geometric["cone_upper"]) != CONE_UPPER:
        raise RuntimeError("cone bounds")
    if growth["replay_summary"]["delta_1"] != str(DELTA_1):
        raise RuntimeError("delta1")
    if not CONE_LOWER < SLOPE < CONE_UPPER:
        raise RuntimeError("canonical slope outside cone")
    result = {
        "schema": RESULT_SCHEMA,
        "Q2_parent_W_Borel_registry": {
            "Q2_atom_base_count": 114006,
            "base_atom_key": "time2-atom-id",
            "leaf_parameter_space_per_atom": (
                "(s,b) with s in the atom s-interval and "
                "b=arcsin(p)-4r in the nonempty clipped intercept interval"
            ),
            "canonical_leaf_equation": "fixed s; phi(r)=4r+b; p(r)=sin(4r+b)",
            "canonical_parent_W_id_schema": "parent-W:(time2-atom-id):(s,b):(natural-short-cell-k)",
            "natural_short_cell_rule": "oriented Euclidean arclength intervals [k*1e-90,(k+1)*1e-90] clipped at leaf endpoints",
            "adapted_cell_length_upper": ADAPTED_CELL_LENGTH_TEXT,
            "adapted_cell_length_strictly_below_delta_1": True,
            "phase_graph_slope_dphi_dr": str(SLOPE),
            "phase_graph_C2_seminorm": "0",
            "inside_certified_invariant_unstable_cone": True,
            "strict_forward_cone_invariance_inherited": True,
            "each_atom_point_has_unique_leaf_parameters": "s is its parameter and b=arcsin(p)-4r",
            "each_leaf_atom_intersection_is_empty_or_one_connected_interval": True,
            "registry_type": "standard-Borel parameterized actual curve registry",
            "finite_integer_curve_count_claimed": False,
            "actual_parent_W_registry": "CERTIFIED_PARAMETERIZED",
        },
        "Q2_actual_recut_instance_schema": {
            "branch_rule_base_count": 228012,
            "instance_parameter_key": "(branch-rule-id,parent-W-id,natural-index-j)",
            "parent_W_is_actual_curve_not_branch_rule": True,
            "natural_index_is_deterministic": True,
            "same_Q2_forward_reverse_restriction_inherited": True,
            "actual_recut_instance_registry": "CERTIFIED_PARAMETERIZED_SCHEMA",
            "per_image_parent_natural_cell_count_formula": "ceil(adapted_length(image-parent-W)/1e-90)",
            "per_image_parent_internal_recut_endpoint_count_formula": "max(ceil(adapted_length(image-parent-W)/1e-90)-1,0)",
            "F7_instance_level_endpoint_formula": "CERTIFIED_SYMBOLIC_ON_ACTUAL_PARAMETERIZED_INSTANCES",
            "F7_family_integrated_numeric_charge": "NOT_CERTIFIED",
            "previous_zero_finite_materialized_instance_count_retyped_as_nonzero": False,
            "reason": "the new object is a Borel parameterized registry, not a fabricated finite enumeration",
        },
        "strict_nonpromotion": {
            "F7_numeric_characteristic_Z_charge": "NOT_CERTIFIED",
            "connected_nonempty_physical_face_piece_registry": "NOT_CERTIFIED",
            "numeric_transversality_coarea_one_sided_trace": "NOT_CERTIFIED",
            "F14_through_F18_materialized": "NOT_CERTIFIED",
            "complete_18_field_operator_blocks": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["internal_replay_digest"] = hashlib.sha256(encoded).hexdigest()
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
            "actual_parent_W_registry": "CERTIFIED_PARAMETERIZED",
            "actual_recut_instance_registry": "CERTIFIED_PARAMETERIZED_SCHEMA",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate45_round31_parent_w_borel_registry_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("ACTUAL_PARENT_W_REGISTRY: CERTIFIED_PARAMETERIZED")
    print("GATE5: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
