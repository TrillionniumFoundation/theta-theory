#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c27_source_g_corrected_transition_frontier_exhaustion_and_known_edge_recovery"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")
PYTHON = ROOT.parent / ".venv-cm2/bin/python"


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("result_sha256", None)
    return {**body, "result_sha256": hashlib.sha256(wire(body)).hexdigest()}


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    base = json.loads((candidate / RESULT).read_bytes())
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("frontier_total", lambda value: value["transition_candidate_census"].__setitem__("total", 487581)),
        ("known_edges", lambda value: value["formal_credit"].__setitem__("known_edge_recovery", 484981)),
        ("invalidated_nonedges", lambda value: value["formal_credit"].__setitem__("exact_nonedge_dispositions", 2599)),
        ("family_exhaustion", lambda value: value["formal_credit"].__setitem__("transition_family_exhaustion", 19)),
        ("transition_theorem", lambda value: value["formal_credit"].__setitem__("transition_theorem", 0)),
        ("pair_routing", lambda value: value["strict_nonpromotion"].__setitem__("pair_routing", 1)),
        ("maximality", lambda value: value["strict_nonpromotion"].__setitem__("maximality", 1)),
        ("CM2", lambda value: value["strict_nonpromotion"].__setitem__("CM2", "GO")),
    ]
    rejected: list[str] = []
    for name, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c27-attack-") as raw:
            target = Path(raw)
            for entry in candidate.iterdir():
                if entry.name != RESULT:
                    os.symlink(entry, target / entry.name)
            forged = copy.deepcopy(base)
            mutate(forged)
            (target / RESULT).write_bytes(wire(close(forged)))
            run = subprocess.run([str(PYTHON), "-I", "-B", str(VERIFIER), "--candidate-dir", str(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if run.returncode == 0:
                raise RuntimeError("accepted:" + name)
            rejected.append(name)
    print(wire({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED", "rejected": rejected}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
