#!/usr/bin/env python3
from __future__ import annotations
import copy, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")

def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")

def close(v):
    import hashlib
    body = dict(v); body.pop("result_sha256", None); return {**body, "result_sha256": hashlib.sha256(canonical(body)).hexdigest()}

def main() -> int:
    candidate = Path(sys.argv[1]).resolve(); base = json.loads((candidate / RESULT).read_bytes())
    attacks = [
        ("member_census", lambda d: d["fresh_universe_census"].__setitem__("members", 502203)),
        ("root_census", lambda d: d["fresh_universe_census"].__setitem__("base_roots", 339035)),
        ("edge_census", lambda d: d["edge_application_census"].__setitem__("applied_edges", 484981)),
        ("rank_reduction", lambda d: d["edge_application_census"].__setitem__("forward_rank_reduction", 281159)),
        ("component_census", lambda d: d["fresh_DSU_census"].__setitem__("components", 57875)),
        ("cross_denominator", lambda d: d["fresh_DSU_census"].__setitem__("cross_component_pair_denominator", 125616475669)),
        ("old_component_credit", lambda d: d["strict_invalidation"].__setitem__("all_pre_C15_component_ids", "RETAINED")),
        ("pullback_pollution", lambda d: d["strict_nonpromotion"].__setitem__("representation_pullback", 1)),
    ]
    rejected = []
    for name, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c15-attack-") as raw:
            directory = Path(raw)
            for source in candidate.iterdir():
                if source.name != RESULT: os.symlink(source, directory / source.name)
            value = copy.deepcopy(base); mutate(value); (directory / RESULT).write_bytes(canonical(close(value)))
            run = subprocess.run([sys.executable, "-I", "-B", str(VERIFIER), "--candidate-dir", str(directory)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if run.returncode == 0: raise RuntimeError("attack accepted:" + name)
            rejected.append(name)
    print(json.dumps({"status":"PASS_8_OF_8_COHERENT_ATTACKS_REJECTED","rejected":rejected}, sort_keys=True, separators=(",", ":")))
    return 0

if __name__ == "__main__": raise SystemExit(main())
