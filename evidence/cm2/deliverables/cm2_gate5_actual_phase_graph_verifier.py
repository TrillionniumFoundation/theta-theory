#!/usr/bin/env python3
"""Replay and fail-closed verifier for the actual Gate-5 phase graphs."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import cm2_gate5_actual_phase_graph_cert as cert
import cm2_gate5_transfer_audit as transfer_audit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"

PREDECESSOR_REPLAYS = (
    (
        "cm2_fixed_section_geometry_cert.py",
        ("fixed-section two-disk geometry: CERTIFIED",),
    ),
    (
        "cm2_fixed_section_impact_cert.py",
        (
            "fixed-section clean impact chart: EXACT POLYNOMIAL IDENTITIES CERTIFIED",
            "explicit cylinder: POSITIVE-MASS FIRST-HIT BOUNDS CERTIFIED",
        ),
    ),
    (
        "cm2_fixed_section_qnl_cert.py",
        (
            "fixed-section gray--white normal cycle: CERTIFIED",
            "fixed-section horizontal gray--gray cycle: CERTIFIED",
        ),
    ),
    (
        "cm2_common_one_return_tube_cert.py",
        (
            "COMMON_ONE_RETURN_TUBE: CERTIFIED",
            "physical_word=G(0,0)->W(0,0)->G(0,0)",
            "transparent_wall_crossings=0",
        ),
    ),
    (
        "cm2_fixed_section_common_vertex_cert.py",
        (
            "ORBIT_ROOT: CERTIFIED",
            "PHYSICAL_WORD: CERTIFIED",
            "TRIVIALIZED_MATRIX_NONDEGENERACY: CERTIFIED",
        ),
    ),
)

REQUIRED_GLOBAL = (
    "complete_return_word_manifest",
    "return_block_dq",
    "operator_wiener_aperiodicity_for_fixed_to_full_route",
    "phase_test_norm_lift",
    "gate5_certified",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def strongly_connected(graph: dict[str, Any]) -> bool:
    states = graph["states"]
    edges = graph["edges"]

    def reached(start: str, *, reverse: bool) -> set[str]:
        seen = {start}
        pending = [start]
        while pending:
            current = pending.pop()
            for edge in edges:
                source = edge["target"] if reverse else edge["source"]
                target = edge["source"] if reverse else edge["target"]
                if source == current and target not in seen:
                    seen.add(target)
                    pending.append(target)
        return seen

    return all(
        reached(state, reverse=False) == set(states)
        and reached(state, reverse=True) == set(states)
        for state in states
    )


def replay_predecessors() -> None:
    for filename, required_lines in PREDECESSOR_REPLAYS:
        run = subprocess.run(
            [sys.executable, str(HERE / filename)],
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
        assert run.returncode == 0, (filename, run.returncode, run.stderr)
        for line in required_lines:
            assert line in run.stdout, (filename, line)


def verify(data: dict[str, Any], *, require_global: bool, replay: bool) -> None:
    assert data["schema"] == "cm2.gate5.actual-phase-graph.v1"
    for item in data["provenance"]:
        path = ROOT / item["path"]
        assert path.is_file(), path
        assert sha256(path) == item["sha256"], path

    # Bind the phase audit to the corrected Gate-3 frontier without using an
    # empty raw endpoint descriptor as a physical phase edge.
    corrected = data["corrected_gate3_boundary"]
    assert corrected == {
        "retracted_pre_forward_time_descriptor_count": 320,
        "retracted_apparent_transition_vertex_count": 16,
        "corrected_physical_transition_vertex_count": 0,
        "physical_transition_vertex_orbit_count": 0,
        "nonphysical_tau_three_collar_count": 4,
        "phase_edges_derived_from_these_descriptors": 0,
    }

    fresh = cert.certify()
    for key in (
        "model",
        "sections",
        "physical_first_hit_witnesses",
        "phase_graphs",
        "logical_scope",
        "completion",
    ):
        assert data[key] == fresh[key]

    graphs = data["phase_graphs"]
    for graph_name, gcd_name in (
        ("height_two_Mstar_support_graph", "height_two_weighted_cycle_gcd"),
        ("standard_N_physical_spanning_graph", "standard_N_component_cycle_gcd"),
    ):
        graph = graphs[graph_name]
        assert strongly_connected(graph)
        failures: list[str] = []
        assert transfer_audit.weighted_cycle_gcd(graph, failures) == 1
        assert not failures
        assert graphs[gcd_name] == 1

    assert data["logical_scope"][
        "direct_standard_N_route_needs_separate_phase_tower"
    ] is False
    assert data["logical_scope"][
        "operator_Dz_unit_circle_invertibility_from_this_graph_alone"
    ] is False
    assert data["route_audit"] == {
        "preferred_route": "direct_standard_N",
        "preferred_route_uses_separate_phase_tower": False,
        "phase_graph_role": (
            "removes the component period-two obstruction only for the optional "
            "fixed-to-full common-refinement route"
        ),
        "component_gcd_one_is_operator_wiener_theorem": False,
    }

    if replay:
        replay_predecessors()

    if require_global:
        completion = data["completion"]
        for key in REQUIRED_GLOBAL:
            assert completion[key] is True


def self_test(data: dict[str, Any]) -> None:
    verify(data, require_global=False, replay=True)

    bad = copy.deepcopy(data)
    bad["phase_graphs"]["standard_N_physical_spanning_graph"]["edges"] = [
        edge
        for edge in bad["phase_graphs"]["standard_N_physical_spanning_graph"]["edges"]
        if not (edge["source"] == "G" and edge["target"] == "G")
    ]
    try:
        verify(bad, require_global=False, replay=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("self-loop deletion was accepted")

    bad = copy.deepcopy(data)
    bad["corrected_gate3_boundary"][
        "corrected_physical_transition_vertex_count"
    ] = 16
    try:
        verify(bad, require_global=False, replay=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("retracted Gate-3 vertices were accepted")

    bad = copy.deepcopy(data)
    bad["logical_scope"][
        "operator_Dz_unit_circle_invertibility_from_this_graph_alone"
    ] = True
    try:
        verify(bad, require_global=False, replay=False)
    except AssertionError:
        pass
    else:  # pragma: no cover
        raise AssertionError("component-to-operator promotion was accepted")
    print("MANIFEST_VERIFIER_SELF_TEST: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--replay-predecessors",
        action="store_true",
        help="also rerun all pinned physical predecessor certificates",
    )
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.self_test:
        self_test(data)
        return
    try:
        verify(
            data,
            require_global=True,
            replay=args.replay_predecessors,
        )
    except AssertionError:
        verify(data, require_global=False, replay=False)
        print("ACTUAL_COMPONENT_PHASE_GRAPH: CERTIFIED")
        print("COMPLETE_FIXED_TO_FULL_OPERATOR_PHASE_TRANSFER: NOT_CERTIFIED")
        raise SystemExit(2)
    print("COMPLETE_FIXED_TO_FULL_OPERATOR_PHASE_TRANSFER: CERTIFIED")


if __name__ == "__main__":
    main()
