#!/usr/bin/env python3
"""Run eight coherently reclosed attacks against the C14a verifier."""
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
PREFIX = "cm2_round306c14a_source_g_graph_sheet_equality_and_partial_rematerialization_frontier"
EQ = PREFIX + "_equality_ledger.jsonl.gz"
PART = PREFIX + "_partial_rematerialization_frontier.jsonl.gz"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def obj(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = obj(row)


def close_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = obj(result)


def rewrite(candidate: Path, filename: str, descriptor_key: str,
            mutate: Callable[[list[dict[str, Any]]], None]) -> None:
    with gzip.open(candidate / filename, "rt") as stream:
        rows = [json.loads(line) for line in stream]
    mutate(rows)
    for row in rows:
        close_row(row)
    plain = b"".join(canonical(row) + b"\n" for row in rows)
    wire = gzip.compress(plain, compresslevel=9, mtime=0)
    (candidate / filename).write_bytes(wire)
    result = json.loads((candidate / RESULT).read_bytes())
    result[descriptor_key].update({
        "compressed_size": len(wire),
        "compressed_sha256": hashlib.sha256(wire).hexdigest(),
        "uncompressed_size": len(plain),
        "uncompressed_sha256": hashlib.sha256(plain).hexdigest(),
        "ordered_rows_sha256": obj(rows),
    })
    close_result(result)
    (candidate / RESULT).write_bytes(canonical(result))


def equality_mutation(kind: str) -> Callable[[list[dict[str, Any]]], None]:
    def mutate(rows: list[dict[str, Any]]) -> None:
        row = rows[0]
        cert = row["graph_to_sheet_set_equality_certificate"]
        if kind == "projection":
            cert["projection_is_bijection"] = False
        elif kind == "sheet-support":
            cert["current_sheet_support_equals_exact_base"] = False
        elif kind == "equality-credit":
            row["graph_sheet_set_equality_credit"] = 0
        elif kind == "pullback":
            row["representation_pullback_credit"] = 1
        else:
            raise AssertionError(kind)
        if kind in {"projection", "sheet-support"}:
            core = dict(cert)
            core.pop("certificate_sha256", None)
            cert["certificate_sha256"] = obj(core)
    return mutate


def partial_mutation(kind: str) -> Callable[[list[dict[str, Any]]], None]:
    def mutate(rows: list[dict[str, Any]]) -> None:
        row = rows[0]
        if kind == "old-equality":
            row["old_graph_sheet_set_equality_credit"] = 1
        elif kind == "ast":
            interval = next(x for x in row["exact_partial_base_ast"]["args"]
                            if x.get("op") == "CLOSED_INTERVAL")
            interval["lower"] = "-999"
            row["exact_partial_base_ast_sha256"] = obj(row["exact_partial_base_ast"])
            row["proposed_exact_sheet_member_id"] = (
                "round306c14-exact-partial-sheet:"
                + obj([row["graph_id"], row["exact_partial_base_ast_sha256"]])
            )
        elif kind == "member-id":
            row["proposed_exact_sheet_member_id"] = "round306c14-exact-partial-sheet:" + "0" * 64
        else:
            raise AssertionError(kind)
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    attacks = [
        ("result-census", "result", None),
        ("projection", "equality", equality_mutation("projection")),
        ("sheet-support", "equality", equality_mutation("sheet-support")),
        ("equality-credit", "equality", equality_mutation("equality-credit")),
        ("pullback-nonpromotion", "equality", equality_mutation("pullback")),
        ("partial-old-equality", "partial", partial_mutation("old-equality")),
        ("partial-ast-reclosure", "partial", partial_mutation("ast")),
        ("partial-member-id", "partial", partial_mutation("member-id")),
    ]
    outcomes = []
    for name, target, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c14a-attack-") as tmp:
            candidate = Path(tmp)
            for filename in (EQ, PART, RESULT):
                shutil.copy2(source / filename, candidate / filename)
            if target == "result":
                result = json.loads((candidate / RESULT).read_bytes())
                result["census"]["set_equalities_proved"] = 831
                close_result(result)
                (candidate / RESULT).write_bytes(canonical(result))
            elif target == "equality":
                rewrite(candidate, EQ, "equality_ledger", mutate)
            else:
                rewrite(candidate, PART, "partial_rematerialization_frontier", mutate)
            process = subprocess.run(
                ["python", "-I", "-B", str(VERIFIER), "--candidate-dir", str(candidate)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            rejected = process.returncode != 0
            outcomes.append({"attack": name, "rejected": rejected})
            if not rejected:
                raise RuntimeError("attack accepted: " + name)
    print(json.dumps({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED",
                      "outcomes": outcomes}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
