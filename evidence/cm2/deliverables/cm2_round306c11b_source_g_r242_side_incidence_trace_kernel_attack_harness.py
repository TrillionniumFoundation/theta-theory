#!/usr/bin/env python3
"""Coherent mutation attacks for the independent C11b verifier."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable


PREFIX = "cm2_round306c11b_source_g_r242_side_incidence_trace_kernel"
RESULT = PREFIX + "_result.json"
INTERFACES = PREFIX + "_interface_kernel_ledger.jsonl.gz"
RELATIONS = PREFIX + "_relation_theorem_ledger.jsonl.gz"
ROOT = Path(__file__).parent
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def object_sha(value: Any) -> str:
    return sha(canonical(value))


def load_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def close_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = object_sha(row)


def store_rows(path: Path, rows: list[dict[str, Any]], descriptor: dict[str, Any]) -> None:
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    wire = gzip.compress(plain, compresslevel=9, mtime=0)
    path.write_bytes(wire)
    descriptor.update({
        "row_count": len(rows),
        "compressed_size": len(wire),
        "compressed_sha256": sha(wire),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": sha(plain),
        "ordered_row_ids_sha256": object_sha([row["row_id"] for row in rows]),
        "ordered_row_hashes_sha256": object_sha([row["row_sha256"] for row in rows]),
        "ordered_rows_sha256": object_sha(rows),
    })


def rewrite_result(path: Path, result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = object_sha(result)
    path.write_bytes(canonical(result))


def relation_mutator(change: Callable[[list[dict[str, Any]]], None]) -> Callable[[Path, dict[str, Any]], None]:
    def mutate(directory: Path, result: dict[str, Any]) -> None:
        path = directory / RELATIONS
        rows = load_rows(path)
        change(rows)
        store_rows(path, rows, result["relation_theorem_ledger"])
    return mutate


def interface_mutator(change: Callable[[list[dict[str, Any]]], None]) -> Callable[[Path, dict[str, Any]], None]:
    def mutate(directory: Path, result: dict[str, Any]) -> None:
        path = directory / INTERFACES
        rows = load_rows(path)
        change(rows)
        store_rows(path, rows, result["interface_kernel_ledger"])
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()

    def change_ref(rows: list[dict[str, Any]], field: str) -> None:
        rows[0][field]["row_sha256"] = "0" * 64
        close_row(rows[0])

    attacks: list[tuple[str, Callable[[Path, dict[str, Any]], None]]] = [
        ("relation-routing-ref", relation_mutator(lambda rows: change_ref(rows, "C11_routing_disposition_ref"))),
        ("relation-support-ref", relation_mutator(lambda rows: change_ref(rows, "C10_exact_support_ref"))),
        ("relation-interface-ref", relation_mutator(lambda rows: change_ref(rows, "interface_kernel_ref"))),
        ("common-boundary-ast", relation_mutator(lambda rows: (rows[0].__setitem__("common_boundary_graph_ast", {"op": "RATIONAL_CONSTANT", "value": "0"}), rows[0]["ast_sha256"].__setitem__("common_boundary_graph_ast", object_sha(rows[0]["common_boundary_graph_ast"])), close_row(rows[0])))),
        ("erase-local-incidence", relation_mutator(lambda rows: (rows[0].__setitem__("local_graph_side_physical_incidence_proved", False), close_row(rows[0])))),
        ("forge-downstream-credit", relation_mutator(lambda rows: (rows[0]["formal_credit"].__setitem__("B1A", 1), close_row(rows[0])))),
        ("duplicate-routing-subject", relation_mutator(lambda rows: (rows[1].__setitem__("graph_id", rows[0]["graph_id"]), rows[1].__setitem__("side_role", rows[0]["side_role"]), rows[1].__setitem__("side_member_id", rows[0]["side_member_id"]), close_row(rows[1])))),
        ("drop-interface-edge-kind", interface_mutator(lambda rows: (rows[0].__setitem__("edge_kind_exhaustion", rows[0]["edge_kind_exhaustion"][:-1]), close_row(rows[0])))),
    ]
    rejected = []
    with tempfile.TemporaryDirectory(prefix="c11b-attacks.") as base:
        for ordinal, (name, mutate) in enumerate(attacks):
            directory = Path(base) / f"{ordinal:02d}-{name}"
            directory.mkdir()
            for filename in (RESULT, INTERFACES, RELATIONS):
                shutil.copy2(source / filename, directory / filename)
            result_path = directory / RESULT
            result = json.loads(result_path.read_bytes())
            mutate(directory, result)
            rewrite_result(result_path, result)
            run = subprocess.run([sys.executable, "-I", "-B", str(VERIFIER), "--candidate-dir", str(directory)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if run.returncode == 0:
                raise RuntimeError("attack accepted:" + name)
            rejected.append(name)
    print(json.dumps({"status": "PASS_C11B_COHERENT_ATTACKS", "rejected": len(rejected), "attacks": rejected}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
