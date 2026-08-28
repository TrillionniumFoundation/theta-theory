#!/usr/bin/env python3
"""Run eight coherent mutations against the independent C12a verifier."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).parent
PREFIX = "cm2_round306c12a_source_g_rerouted_shared_side_kernel"
LEDGER = PREFIX + "_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = object_sha(row)


def close_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = object_sha(result)


def rewrite_ledger(directory: Path, mutate: Callable[[list[dict[str, Any]]], None]) -> None:
    ledger = directory / LEDGER
    with gzip.open(ledger, "rt") as stream:
        rows = [json.loads(line) for line in stream]
    mutate(rows)
    for row in rows:
        close_row(row)
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    wire = gzip.compress(plain, compresslevel=9, mtime=0)
    ledger.write_bytes(wire)
    result_path = directory / RESULT
    result = json.loads(result_path.read_bytes())
    descriptor = result["kernel_ledger"]
    descriptor.update({
        "compressed_size": len(wire),
        "compressed_sha256": hashlib.sha256(wire).hexdigest(),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "ordered_rows_sha256": object_sha(rows),
    })
    close_result(result)
    result_path.write_bytes(canonical(result))


def mutate_result(directory: Path) -> None:
    path = directory / RESULT
    result = json.loads(path.read_bytes())
    result["scoped_credit"]["one_sided_trace"] = 9
    close_result(result)
    path.write_bytes(canonical(result))


def row_mutator(kind: str) -> Callable[[list[dict[str, Any]]], None]:
    def mutate(rows: list[dict[str, Any]]) -> None:
        row = rows[0]
        if kind == "closure":
            row["closure_incidence_certificate"]["closure_incidence_complete"] = False
        elif kind == "direction":
            row["one_sided_trace_certificate"]["charts"][0]["direction"] *= -1
        elif kind == "branch":
            row["partition_branch_to_side_member_equivalence_certificate"]["side_member_exact_support_equivalence_proved"] = False
        elif kind == "downstream":
            row["strict_nonpromotion"]["representation_pullback"] = 1
        elif kind == "side_ast":
            row["exact_side_stratum_ast"]["args"][1]["op"] = "LT"
            row["exact_side_stratum_ast_sha256"] = object_sha(row["exact_side_stratum_ast"])
        elif kind == "geometry":
            row["R248_side_member_identity"]["support_geometry_taken_from_R248"] = True
        elif kind == "credit":
            row["scoped_credit"]["local_graph_side_physical_incidence"] = 0
        else:
            raise AssertionError(kind)
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    attacks: list[tuple[str, Callable[[Path], None]]] = [("result-credit", mutate_result)]
    attacks.extend((name, lambda directory, n=name: rewrite_ledger(directory, row_mutator(n))) for name in ("closure", "direction", "branch", "downstream", "side_ast", "geometry", "credit"))
    outcomes = []
    for name, attack in attacks:
        with tempfile.TemporaryDirectory(prefix="c12a-attack-") as temporary:
            target = Path(temporary)
            shutil.copy2(source / LEDGER, target / LEDGER)
            shutil.copy2(source / RESULT, target / RESULT)
            attack(target)
            completed = subprocess.run(
                ["python", "-I", "-B", str(VERIFIER), "--candidate-dir", str(target)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            rejected = completed.returncode != 0
            outcomes.append({"attack": name, "rejected": rejected})
            if not rejected:
                raise RuntimeError("attack accepted:" + name)
    print(json.dumps({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED", "outcomes": outcomes}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
