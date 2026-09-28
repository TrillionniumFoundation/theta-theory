#!/usr/bin/env python3
"""Focused A2 v37 source guards and finite diagnostics.

This script does not build TeX, audit every active input, or certify a theorem.
It preserves the v36 referee diagnostics byte-for-byte and invokes their six
finite families. Additional guards concern the actual E2 edit and a finite
SE(2) tree-propagation example. Exceptions remain active with python -O.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import re
from pathlib import Path

import numpy as np
import scipy

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parents[1]
SOURCE_COMMIT = "b0c21cd799bbe4d96bab4a7e1e369d5d7152b294"
REVIEW_SCRIPT = ROOT / "reviews/a2-v36-external-harsh-top4-2026-09-13/diagnostics.py"
REVIEW_SHA256 = "b0794bb7ddbe26503898c56df07b1fdf3fa37d2a230196804ce2b01f670e93bc"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_guards() -> dict:
    main = (PAPER / "main.tex").read_text(encoding="utf-8")
    old_main = (PAPER / "history/v36/main.tex").read_text(encoding="utf-8")
    chapter_path = PAPER / "article/23f_single_offset_law_inverse_v26.tex"
    chapter = chapter_path.read_text(encoding="utf-8")
    old_chapter = (PAPER / "history/v36/article/23f_single_offset_law_inverse_v26.tex").read_text(encoding="utf-8")
    require(git_blob(PAPER / "history/v36/main.tex") == "8b53acb0785b3b918d129216f172ee3dd73512bc", "Wrong v36 main baseline")
    require(git_blob(PAPER / "history/v36/article/23f_single_offset_law_inverse_v26.tex") == "35f538eea4415951d1572cd9db76fdff429afa0a", "Wrong v36 inverse baseline")
    require(main.replace("revision 37", "revision 36") == old_main, "Main changed beyond its two version identifiers")
    require(git_blob(chapter_path) == "63ed36efd417cd23e6f869952627719de00e6ef7", "Inverse chapter differs from the tested source")
    require(git_blob(PAPER / "article/99_auxiliary_compendium_v19.tex") == "a596f344cd660eeaacc8e4e3eb21a0cb39610a9e", "Auxiliary input wrapper changed")
    require(git_blob(PAPER / "article/23d_rank_two_lattice_recovery_v24.tex") == "5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c", "Full periodic theorem source changed")
    labels = re.compile(r"\\label\{([^}]+)\}")
    require(labels.findall(chapter) == labels.findall(old_chapter), "Inverse labels deleted, reordered, or added")
    section = chapter.split(r"\label{thm:v26-single-offset-global}", 1)[1]
    statement, proof = section.split(r"\end{theorem}", 1)
    item3 = statement.split(r"\item", 3)[3]
    flat = " ".join(item3.split())
    require("rooted signature-rigid spanning tree reaching every obstacle orbit" in flat, "Missing all-orbit tree condition")
    require("based at one channel frame" in flat, "Missing common cycle base frame")
    require(r"\ref{thm:v24-uncalibrated-periodic-rigidity}" in item3, "Missing full-table theorem reference")
    require(r"\ref{thm:v24-lattice-gram-recovery}" not in item3, "Lattice-only theorem still supplies whole-table hypotheses")
    for token in [r"\ref{thm:v24-lattice-gram-recovery}", r"L=VM^{-1}", r"M^{-T}V^TVM^{-1}", "every obstacle orbit", "existence and admissibility", r"\ref{thm:v24-uncalibrated-periodic-rigidity}"]:
        require(token in proof, "Missing proof dependency: " + token)
    inputs = re.findall(r"\\input\{([^}]+)\}", main)
    auxiliary = (PAPER / "article/99_auxiliary_compendium_v19.tex").read_text(encoding="utf-8")
    return {"main_changes_version_only": True, "direct_main_inputs_preserved": len(inputs),
            "auxiliary_wrapper_inputs_preserved": len(re.findall(r"\\input\{([^}]+)\}", auxiliary)),
            "inverse_labels_preserved": len(labels.findall(chapter)),
            "E2_statement_and_proof_guards": "PASS",
            "scope": "These counts compare entry/wrapper text; they are not a recursive input-availability or compilation check."}


def motion(angle: float, x: float, y: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, x], [s, c, y], [0., 0., 1.]])


def propagate(root_motion: np.ndarray, edges: list[tuple[str, str, np.ndarray]], nodes: set[str]) -> dict[str, np.ndarray]:
    placements = {"root": root_motion}
    remaining = list(edges)
    while remaining:
        next_edges = []
        for parent, child, transition in remaining:
            if parent not in placements:
                next_edges.append((parent, child, transition))
                continue
            require(child not in placements, "Input is not a rooted tree")
            placements[child] = placements[parent] @ transition
        require(len(next_edges) < len(remaining), "Disconnected tree")
        remaining = next_edges
    require(set(placements) == nodes, "Tree does not reach every declared obstacle orbit")
    return placements


def tree_example() -> dict:
    truth = {"root": np.eye(3), "a": motion(.2, 1.4, -.1),
             "b": motion(-.3, -.4, 2.1), "c": motion(.7, 3.2, 1.9)}
    pairs = [("a", "c"), ("root", "b"), ("root", "a")]
    edges = [(p, c, np.linalg.inv(truth[p]) @ truth[c]) for p, c in pairs]
    found = propagate(np.eye(3), edges, set(truth))
    gauge = motion(.4, 5., -2.)
    shifted = propagate(gauge, edges, set(truth))
    error = max(float(np.max(np.abs(found[k] - truth[k]))) for k in truth)
    gauge_error = max(float(np.max(np.abs(shifted[k] - gauge @ truth[k]))) for k in truth)
    require(max(error, gauge_error) < 1e-12, "Finite tree placement/gauge check failed")
    rejected = False
    try:
        propagate(np.eye(3), edges, set(truth) | {"unreached"})
    except RuntimeError:
        rejected = True
    require(rejected, "An unmeasured orbit was silently accepted")
    return {"obstacle_orbits": 4, "tree_edges": 3, "max_placement_error": error,
            "max_common_gauge_error": gauge_error, "unreached_orbit_rejected": rejected,
            "scope": "Finite SE(2) composition check, not analytic signature rigidity or billiard realizability."}


def main() -> None:
    require(hashlib.sha256(REVIEW_SCRIPT.read_bytes()).hexdigest() == REVIEW_SHA256, "Referee diagnostic source changed")
    spec = importlib.util.spec_from_file_location("a2_v36_referee_diagnostics", REVIEW_SCRIPT)
    require(spec is not None and spec.loader is not None, "Could not load pinned diagnostics")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    checks = {"source_guards": source_guards(), "rooted_tree_propagation": tree_example()}
    for name in ["density_inverse", "jet_algebra", "finite_halfline_envelope", "lattice_and_reflection", "moving_ceiling_layer", "alternative_mean"]:
        checks[name] = getattr(module, name)()
    result = {"status": "PASS", "tested_manuscript_source_commit": SOURCE_COMMIT,
              "scope": "Focused source guards, one finite tree example and six re-executed referee diagnostic families; not a full native-build or theorem certificate.",
              "complete_main_built_by_this_script": False,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "inherited_diagnostic_sha256": REVIEW_SHA256,
              "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "checks": checks}
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
