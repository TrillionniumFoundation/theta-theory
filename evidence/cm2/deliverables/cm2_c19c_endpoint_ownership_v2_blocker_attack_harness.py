#!/usr/bin/env python3
"""Coherent mutation attacks for the C19C endpoint-bit blocker package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_c19c_endpoint_ownership_v2"
RESULT = PREFIX + "_blocker_result.json"
LEDGER = PREFIX + "_unrecoverable_rows.jsonl.gz"
VERIFIER = HERE / (PREFIX + "_blocker_independent_verifier.py")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def objsha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def resign(value: dict[str, Any]) -> None:
    value.pop("result_sha256", None)
    value["result_sha256"] = objsha(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--attack-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    attack_root = Path(args.attack_dir).resolve()
    attack_root.mkdir(parents=True, exist_ok=True)
    base = json.loads((source / RESULT).read_bytes())

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("status_promoted", lambda d: d.__setitem__("status", "PASS")),
        ("zero_seed", lambda d: d.__setitem__("execution_seed", 0)),
        ("row_census_minus_one", lambda d: d["census"].__setitem__("C19C_half_open_rational_box_rows", 33_343)),
        ("requested_slots_minus_one", lambda d: d["census"].__setitem__("requested_endpoint_ownership_bit_slots", 200_063)),
        ("forge_one_materialized_bit", lambda d: d["census"].__setitem__("materialized_endpoint_ownership_bit_slots", 1)),
        ("forge_one_recovered_vector", lambda d: d["census"].__setitem__("fully_recoverable_six_bit_vectors", 1)),
        ("delete_one_countermodel_row", lambda d: d["census"].__setitem__("rows_with_a_constructive_final_t_split_nonidentifiability_witness", 33_343)),
        ("input_pin_flip", lambda d: d["input_pins"].__setitem__(next(iter(d["input_pins"])), "0" * 64)),
        ("ledger_row_count_minus_one", lambda d: d["ledger"].__setitem__("row_count", 33_343)),
        ("ledger_sha_flip", lambda d: d["ledger"].__setitem__("sha256", "0" * 64)),
        ("ledger_size_plus_one", lambda d: d["ledger"].__setitem__("size", d["ledger"]["size"] + 1)),
        ("ledger_sequence_flip", lambda d: d["ledger"].__setitem__("row_sequence_sha256", "0" * 64)),
    ]

    outcomes = []
    for ordinal, (label, mutate) in enumerate(mutations):
        case = attack_root / f"{ordinal:02d}-{label}"
        if case.exists():
            shutil.rmtree(case)
        case.mkdir()
        os.link(source / LEDGER, case / LEDGER)
        candidate = deepcopy(base)
        mutate(candidate)
        resign(candidate)
        (case / RESULT).write_bytes(canonical(candidate))
        process = subprocess.run(
            [sys.executable, "-I", "-B", str(VERIFIER), "--candidate-dir", str(case)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        rejected = process.returncode != 0
        if not rejected:
            raise RuntimeError("attack accepted:" + label)
        outcomes.append({
            "ordinal": ordinal,
            "label": label,
            "coherently_resigned_result": True,
            "rejected": True,
            "returncode": process.returncode,
            "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
        })

    body = {
        "schema": "cm2.c19c-endpoint-ownership-v2.blocker-attacks.v1",
        "status": "PASS_ALL_COHERENT_MUTATIONS_REJECTED",
        "attack_count": len(outcomes),
        "rejected_count": len(outcomes),
        "all_rejected": True,
        "attacks": outcomes,
        "formal_credit": 0,
    }
    result = {**body, "result_sha256": objsha(body)}
    raw = canonical(result)
    Path(args.output).resolve().write_bytes(raw)
    print(raw.decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
