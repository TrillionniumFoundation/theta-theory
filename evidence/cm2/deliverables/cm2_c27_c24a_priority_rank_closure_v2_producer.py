#!/usr/bin/env python3
"""Append-only closure-correct v2 publication of the independent priority/rank audit.

The v1 generator formed a Counter with integer multiplicity keys.  Its first
hash sorted those keys numerically, while JSON parsing converts them to
strings and later verification sorts lexicographically.  This v2 publisher
executes the pinned v1 generator in a fresh directory, explicitly normalizes
all multiplicity keys to strings before publication, and creates a
seed-separated but semantically stable, self-verifying result object.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT / ".cm2-runtime/audit/read-only-c24a-positive-priority-and-c27r1d-rank-audit.py"
V1_SHA256 = "4366d815589d5669d1778605e3bab07429c85c249ed4aa9e0dc1bc4cbf0c9661"
LEDGERS = {
    "C24A_9408_positive_pair_priority_disposition.jsonl.gz":
        "6a59b0822c8a27eb5f44609cd5edd33038dadf17aa8fe7841d2c7277c8c5ec95",
    "C24A_596_cross_positive_member_to_component_edge.jsonl.gz":
        "0f3924d4a9f0b029d4c82879ec453bb280232c13d870ac28157b5a20dd5585c8",
    "C24A_cross_positive_unique_component_edges.jsonl.gz":
        "d922bbf6d8f487df1e826271b0d65d2d9765432f6d4a02919fe1157b94c117ef",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def build(out: Path, seed: int) -> dict[str, Any]:
    need(file_sha(V1) == V1_SHA256, "pinned v1 producer source")
    need(not out.exists(), "fresh output directory")
    spec = importlib.util.spec_from_file_location("cm2_c24a_priority_rank_v1_pinned", V1)
    need(spec is not None and spec.loader is not None, "v1 module spec")
    module = importlib.util.module_from_spec(spec)
    old_argv = sys.argv
    captured = io.StringIO()
    try:
        spec.loader.exec_module(module)
        sys.argv = [str(V1), "--out-dir", str(out)]
        with redirect_stdout(captured):
            status = module.main()
    finally:
        sys.argv = old_argv
    need(status == 0, "v1 fresh generation")
    for filename, expected in LEDGERS.items():
        need(file_sha(out / filename) == expected, "v1 deterministic ledger:" + filename)

    result_path = out / "result.json"
    result = json.loads(result_path.read_bytes())
    need(result["status"]
         == "PASS_EXACT_SET_INTERSECTIONS_AND_PROVISIONAL_RANK_DIAGNOSTIC_ZERO_CREDIT",
         "v1 result status")
    old_claim = result.pop("result_sha256")
    census = result["cross_current_C15_component"]["member_pair_multiplicity_census"]
    need(all(str(int(key)) == key for key in census), "parsed multiplicity string keys")
    result["cross_current_C15_component"]["member_pair_multiplicity_census"] = {
        str(key): census[key] for key in sorted(census, key=lambda item: int(item))
    }
    result["schema"] = "cm2.audit.c24a-positive-priority-and-c27r1d-rank-diagnostic.v2"
    result["status"] = (
        "PASS_EXACT_SET_INTERSECTIONS_AND_PROVISIONAL_RANK_DIAGNOSTIC_"
        "CLOSURE_VALID_V2_ZERO_CREDIT"
    )
    result["invocation_seed"] = seed
    result["v1_closure_repair"] = {
        "pinned_v1_producer_sha256": V1_SHA256,
        "v1_claimed_result_sha256": old_claim,
        "cause": "INTEGER_COUNTER_KEYS_NORMALIZED_TO_STRINGS_BEFORE_RESULT_HASH",
        "ledger_payload_changed": False,
        "formal_credit": 0,
    }
    result["semantic_projection_sha256"] = digest({
        key: value for key, value in result.items() if key != "invocation_seed"
    })
    result["result_sha256"] = digest(result)
    result_path.write_bytes(canonical(result) + b"\n")

    reread = json.loads(result_path.read_bytes())
    claimed = reread.pop("result_sha256")
    need(claimed == digest(reread), "v2 result closure")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = build(Path(args.out_dir), args.seed)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "semantic_projection_sha256": result["semantic_projection_sha256"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
