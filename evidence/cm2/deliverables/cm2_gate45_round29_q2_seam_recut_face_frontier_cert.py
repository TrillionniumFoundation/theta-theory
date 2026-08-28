#!/usr/bin/env python3
"""Round-29 Q2 chart-seam refinement and recut/face instance frontier.

This append-only leaf replays the complete frozen time-two adaptive registry
with 384-bit Arb.  It then refines only the 5,280 strict Q2 boxes whose second
physical collision does not strictly exclude a target normal-chart seam.
The refinement is a finite, fair three-coordinate dyadic refinement and is
used only to enlarge the strict-single-chart subledger; a finite residual
tube is retained explicitly.

The leaf also audits the exact object-type frontier left by round 28.  The
228,012 canonical-recut objects are branch rules, not actual standard-curve
instances: no parent-W registry exists in the frozen dependencies, hence no
``(branch-rule,parent-W,j)`` curve-instance ID is manufactured.  Likewise a
physical carrier family is not a connected one-dimensional face piece.  On
every strict Q2-inner box the terminal C24 boundary is disjoint by inherited
whole-box strict outside tests, but this certified-empty terminal family is
not promoted to a complete physical face atlas or to F14--F18.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2_cert
import cm2_gate45_round28_q2_homogeneity_recut_cert as round28_q2


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round29-q2-seam-recut-face-frontier.v1"
MANIFEST_SCHEMA = "cm2.gate45.round29-q2-seam-recut-face-frontier.manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate45-round29-q2-seam-recut-face-frontier-manifest-2026-07-18.json"
MAX_EXTRA_SEAM_DEPTH = 6

DEPENDENCIES = {
    "cm2_gate45_round28_q2_homogeneity_recut_cert.py":
        "1acf1072caa22b676ed7f579cd2a909f06c6b8249396a7be4cdaa9c37997cf64",
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json":
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3",
    "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py":
        "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27",
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json":
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json":
        "120a3f1cba9f23cc4b2a9753491022f8143175810b19f1a9f9d8ee0214d66b60",
    "cm2_gate34_round26_q1_time2_frontier_cert.py":
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


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
    return str(value.numerator) if value.denominator == 1 else str(value)


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        if path.suffix == ".json":
            value = parse_json_text(path.read_text(encoding="utf-8"))
            require(isinstance(value, dict), f"dependency type: {name}")
            loaded[name] = value

    q2 = loaded[
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    ]
    registry = q2["result"]["Q2_two_step_homogeneity_and_recut_registry"]
    require(registry["strict_Q2_atom_count"] == 114006, "prior Q2 count")
    require(registry["canonical_recut_branch_rule_id_count"] == 228012, "rules")
    require(registry["actual_curve_recut_instance_id_count"] == 0, "instances")
    require(
        registry["time2_target_chart_seam_not_strictly_excluded_Q2_atom_count"]
        == 5280,
        "seam count",
    )

    faces = loaded[
        "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
    ]
    require(
        faces["result"]["R2_and_arbitrary_n_physical_face_ID_grammar_frontier"]
        ["R2_instantiated_face_component_id_count"] == 0,
        "connected face count",
    )
    require(
        faces["result"]["R2_and_arbitrary_n_physical_face_ID_grammar_frontier"]
        ["connected_rank_assignment_certified_on_instantiated_faces"] is False,
        "connected ranks",
    )

    components = loaded[
        "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
    ]
    require(
        components["verdict"]["Q2_inner_nonempty_depth2_adaptive_components"]
        == "CERTIFIED_114006",
        "Q2 components",
    )
    return loaded


def seam_child_id(parent_time2_atom_id: str, suffix: str, atom: Any) -> str:
    return "q2-chart-refinement:" + digest({
        "parent_time2_atom_id": parent_time2_atom_id,
        "additional_suffix": suffix,
        "box": {
            "t": [str(atom.t0), str(atom.t1)],
            "p": [str(atom.p0), str(atom.p1)],
            "s": [str(atom.s0), str(atom.s1)],
        },
    })


def refine_one_seam_atom(
    atom: Any,
    parent_time2_atom_id: str,
    parent_depth: int,
    cores: tuple[Any, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    stack = [atom]
    while stack:
        child = stack.pop()
        # The parent is already a strict Q2-inner whole box, so every child is
        # a physical Q2 subset.  Replaying core membership here would only
        # repeat an inherited strict separator.  We freshly replay both
        # collision owners because the requested chart is a target-owner
        # coordinate object, not an inherited source-box label.
        state = time2_cert.first_collision_outgoing(child)
        require(state is not None, "time1 owner inheritance")
        owner, status = round28_q2.owner_from_outgoing(child, state)
        require(status == "strict_unique_second_collision_owner", "owner inheritance")
        require(owner is not None, "Q2 owner state")
        chart = time2_cert.strict_chart(owner["normal_x"], owner["normal_y"])
        extra_depth = child.depth - parent_depth
        if chart is None and extra_depth < MAX_EXTRA_SEAM_DEPTH:
            left, right = time2_cert.step1.split_atom(child)
            stack.append(right)
            stack.append(left)
            continue
        suffix = child.path[len(atom.path):]
        mass = time2_cert.step1.base_mass(child)
        rows.append({
            "refined_atom_id": seam_child_id(parent_time2_atom_id, suffix, child),
            "parent_time2_atom_id": parent_time2_atom_id,
            "additional_suffix": suffix,
            "additional_depth": extra_depth,
            "time2_target_chart": (
                None if chart is None else f"{owner['selected_target_id'][0]}:{chart}"
            ),
            "classification": (
                "RESOLVED_STRICT_SINGLE_CHART"
                if chart is not None
                else "RESIDUAL_REPRESENTATION_SEAM_OUTER"
            ),
            "parameter_averaged_unnormalized_base_mass": qstr(mass),
            "physical_Q2_and_two_owner_inherited_and_replayed": True,
            "representation_seam_is_not_physical_cut": True,
        })
    rows.sort(key=lambda row: row["additional_suffix"])
    paths = [row["additional_suffix"] for row in rows]
    require(
        not any(right.startswith(left) for left, right in zip(paths, paths[1:])),
        "refinement prefix freedom",
    )
    require(
        sum(Q(row["parameter_averaged_unnormalized_base_mass"]) for row in rows)
        == time2_cert.step1.base_mass(atom),
        "seam parent mass",
    )
    return rows


def build_result() -> dict[str, Any]:
    load_dependencies()
    step1_manifest = time2_cert.load_step1_manifest()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "cores")
    q1_rows = [
        row
        for row in step1_manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    require(len(q1_rows) == 2868, "Q1 rows")
    q1_rows.sort(key=lambda row: row["atom_id"])

    terminal_count = 0
    q2_count = 0
    original_strict_chart_count = 0
    seam_parent_count = 0
    q2_mass = Q(0)
    seam_parent_mass = Q(0)
    refined_rows: list[dict[str, Any]] = []
    q2_ids: set[str] = set()

    for parent in q1_rows:
        stack = [time2_cert.atom_from_step1_row(parent, cores)]
        while stack:
            atom = stack.pop()
            classification, status, destination_id, state, owner = (
                round28_q2.classify_with_geometry(atom, cores)
            )
            if (
                classification == "UNRESOLVED_TIME2_OUTER"
                and atom.depth < time2_cert.MAX_TOTAL_BINARY_DEPTH
            ):
                left, right = time2_cert.step1.split_atom(atom)
                stack.append(right)
                stack.append(left)
                continue
            terminal_count += 1
            if classification != "SURVIVE_THROUGH_2_INNER":
                continue
            require(status == "strict_unique_second_collision_owner", "Q2 owner")
            require(destination_id is None and state is not None and owner is not None, "Q2 geometry")
            row = round28_q2.compact_terminal_row(
                parent,
                atom,
                classification,
                status,
                None,
                owner["selected_target_id"],
            )
            require(row["time2_atom_id"] not in q2_ids, "Q2 id")
            q2_ids.add(row["time2_atom_id"])
            q2_count += 1
            mass = time2_cert.step1.base_mass(atom)
            q2_mass += mass
            chart = time2_cert.strict_chart(owner["normal_x"], owner["normal_y"])
            if chart is not None:
                original_strict_chart_count += 1
                continue
            seam_parent_count += 1
            seam_parent_mass += mass
            refined_rows.extend(
                refine_one_seam_atom(atom, row["time2_atom_id"], atom.depth, cores)
            )

    require(terminal_count == 416994, "terminal count")
    require(q2_count == 114006, "Q2 count")
    require(original_strict_chart_count == 108726, "original strict charts")
    require(seam_parent_count == 5280, "seam parents")
    require(q2_mass == Q(5257799, 5120000000), "Q2 mass")

    class_hist = Counter(row["classification"] for row in refined_rows)
    depth_hist = Counter(row["additional_depth"] for row in refined_rows)
    chart_hist = Counter(
        row["time2_target_chart"] or "UNRESOLVED_REPRESENTATION_SEAM"
        for row in refined_rows
    )
    mass_hist: Counter[str] = Counter()
    for row in refined_rows:
        mass_hist[row["classification"]] += Q(
            row["parameter_averaged_unnormalized_base_mass"]
        )
    require(sum(mass_hist.values()) == seam_parent_mass, "global seam mass")
    require(class_hist["RESOLVED_STRICT_SINGLE_CHART"] > 0, "no seam progress")
    require(class_hist["RESIDUAL_REPRESENTATION_SEAM_OUTER"] > 0, "finite residual expected")
    require(
        mass_hist["RESIDUAL_REPRESENTATION_SEAM_OUTER"] < seam_parent_mass,
        "residual mass decreases",
    )

    refined_ids = [row["refined_atom_id"] for row in refined_rows]
    require(len(refined_ids) == len(set(refined_ids)), "refined ids")
    residual_count = class_hist["RESIDUAL_REPRESENTATION_SEAM_OUTER"]
    resolved_count = class_hist["RESOLVED_STRICT_SINGLE_CHART"]
    total_strict_chart_cells = original_strict_chart_count + resolved_count

    q2_terminal_face_pair_count = q2_count * 48
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "replay_engine": "fresh complete 384-bit Arb time-two recursion plus depth-6 fair seam refinement",
        },
        "Q2_time2_target_chart_seam_refinement": {
            "precision_bits": 384,
            "original_strict_Q2_atom_count": q2_count,
            "original_strict_single_chart_Q2_atom_count": original_strict_chart_count,
            "original_seam_frontier_parent_count": seam_parent_count,
            "original_seam_frontier_base_mass": qstr(seam_parent_mass),
            "maximum_additional_fair_dyadic_depth": MAX_EXTRA_SEAM_DEPTH,
            "refined_terminal_cell_count": len(refined_rows),
            "refined_classification_histogram": dict(sorted(class_hist.items())),
            "refined_additional_depth_histogram": {
                str(key): value for key, value in sorted(depth_hist.items())
            },
            "refined_target_chart_histogram": dict(sorted(chart_hist.items())),
            "resolved_strict_single_chart_child_count": resolved_count,
            "residual_representation_seam_outer_count": residual_count,
            "resolved_base_mass": qstr(mass_hist["RESOLVED_STRICT_SINGLE_CHART"]),
            "residual_base_mass": qstr(mass_hist["RESIDUAL_REPRESENTATION_SEAM_OUTER"]),
            "mass_identity_resolved_plus_residual_equals_original_seam_mass": True,
            "residual_mass_strictly_less_than_original_seam_mass": True,
            "original_plus_refined_strict_single_chart_cell_count": total_strict_chart_cells,
            "refined_cell_ids_sha256": digest(refined_ids),
            "refined_rows_sha256": digest(refined_rows),
            "representative_rows": refined_rows[:2] + refined_rows[-2:],
            "finite_refinement_claimed_as_complete_chart_atlas": False,
            "representation_seam_claimed_as_physical_cut": False,
        },
        "Q2_actual_parent_W_recut_instance_frontier": {
            "canonical_recut_branch_rule_count": 228012,
            "actual_parent_W_registry_count_in_frozen_dependencies": 0,
            "actual_curve_recut_instance_id_count": 0,
            "required_instance_key": "(branch-rule-id,parent-canonical-W-id,natural-index-j)",
            "branch_rule_retyped_as_actual_curve_instance": False,
            "first_real_blocker": "no materialized parent-canonical-W registry on the Q2 strong restriction",
            "F7_characteristic_Z_instance_charge_count": 0,
        },
        "Q2_terminal_C24_face_empty_family_ledger": {
            "strict_Q2_inner_atom_count": q2_count,
            "obstacle_compatible_terminal_core_face_family_count_per_atom": 48,
            "atom_terminal_face_family_pair_count": q2_terminal_face_pair_count,
            "nonempty_terminal_core_face_piece_count_on_strict_Q2_inner_atoms": 0,
            "justification": "whole-box strict outside of every compatible closed core rectangle gives one strict separator per core, hence disjointness from all four bounded core faces",
            "certified_empty_pair_count_is_connected_rank_assignment_count": False,
            "carrier_family_retyped_as_connected_face_piece": False,
            "artificial_dyadic_or_chart_seam_retyped_as_physical_face": False,
            "complete_Q2_physical_face_atlas": "NOT_CERTIFIED",
        },
        "Gate5_frontier": {
            "F4_strict_single_chart_subledger_enlarged": True,
            "F4_complete_Q2_chart_ledger": "NOT_CERTIFIED",
            "F7_materialized_actual_instance_slot_count": 0,
            "F14_through_F18_materialized_slot_count": 0,
            "numeric_transversality_coarea_one_sided_trace_on_nonempty_connected_faces": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
            "global_Gate5_maturity": "4/18_UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    seam = result["Q2_time2_target_chart_seam_refinement"]
    return {
        "Q2_finite_chart_seam_refinement": (
            f"CERTIFIED_{seam['refined_terminal_cell_count']}"
        ),
        "Q2_new_strict_single_chart_children": (
            f"CERTIFIED_{seam['resolved_strict_single_chart_child_count']}"
        ),
        "Q2_residual_representation_seam_outer": (
            f"CERTIFIED_{seam['residual_representation_seam_outer_count']}"
        ),
        "Q2_actual_curve_recut_instance_ids": 0,
        "Q2_connected_physical_face_piece_ids": 0,
        "Q2_F7_F14_F18": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round29_q2_seam_recut_face_frontier_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.manifest, args.verifier)
        print(f"WROTE: {args.manifest}")
        return 0
    result = build_result()
    seam = result["Q2_time2_target_chart_seam_refinement"]
    print(f"REFINED_TERMINAL_CELLS: {seam['refined_terminal_cell_count']}")
    print(f"NEW_STRICT_CHART_CHILDREN: {seam['resolved_strict_single_chart_child_count']}")
    print(f"RESIDUAL_SEAM_OUTER: {seam['residual_representation_seam_outer_count']}")
    print("ACTUAL_RECUT_INSTANCES: 0")
    print("F7_F14_F18: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, DuplicateKeyError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
