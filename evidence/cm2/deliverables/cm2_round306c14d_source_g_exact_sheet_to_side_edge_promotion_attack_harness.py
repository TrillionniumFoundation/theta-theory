#!/usr/bin/env python3
from __future__ import annotations

import argparse, gzip, hashlib, io, json, shutil, subprocess, tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).parent
PREFIX = "cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion"
EDGES = PREFIX + "_edge_promotion_ledger.jsonl.gz"
NEGATIVE = PREFIX + "_negative_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")


def canonical(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def obj(v: Any) -> str: return hashlib.sha256(canonical(v)).hexdigest()


def close_row(r: dict[str, Any]) -> None:
    r.pop("row_sha256", None); r["row_sha256"] = obj(r)


def close_result(r: dict[str, Any]) -> None:
    r.pop("result_sha256", None); r["result_sha256"] = obj(r)


def rewrite(candidate: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    out = io.BytesIO(); plain = hashlib.sha256(); count = 0
    with gzip.open(candidate / EDGES, "rb") as source, \
            gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=out, mtime=0) as target:
        for line in source:
            row = json.loads(line)
            if count == 0: mutate(row); close_row(row)
            wire = canonical(row) + b"\n"; target.write(wire); plain.update(wire); count += 1
    compressed = out.getvalue(); (candidate / EDGES).write_bytes(compressed)
    result = json.loads((candidate / RESULT).read_bytes())
    result["edge_promotion_ledger"].update({"row_count": count, "size": len(compressed),
        "sha256": hashlib.sha256(compressed).hexdigest(), "uncompressed_sha256": plain.hexdigest()})
    close_result(result); (candidate / RESULT).write_bytes(canonical(result))


def mutation(kind: str) -> Callable[[dict[str, Any]], None]:
    def change(row: dict[str, Any]) -> None:
        if kind == "edge-credit": row["edge_promotion_credit"] = 0
        elif kind == "negative": row["negative_disposition_required"] = True
        elif kind == "equality": row["composition_certificate"]["graph_equals_new_exact_sheet"] = False
        elif kind == "closure": row["composition_certificate"]["graph_in_relative_closure_of_side"] = False
        elif kind == "trace": row["composition_certificate"]["one_sided_trace_to_graph"] = False
        elif kind == "dsu": row["fresh_DSU_application_credit"] = 1
        elif kind == "union": row["DSU_union_or_component_credit"] = 1
        else: raise AssertionError(kind)
    return change


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--candidate-dir", required=True); a = p.parse_args()
    source = Path(a.candidate_dir).resolve()
    attacks = [("edge-census", None), ("edge-credit", mutation("edge-credit")),
               ("negative-disposition", mutation("negative")),
               ("graph-sheet-equality", mutation("equality")),
               ("graph-side-closure", mutation("closure")),
               ("one-sided-trace", mutation("trace")),
               ("premature-dsu-application", mutation("dsu")),
               ("premature-union", mutation("union"))]
    outcomes = []
    for name, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c14d-attack-") as tmp:
            candidate = Path(tmp)
            for f in (EDGES, NEGATIVE, RESULT): shutil.copy2(source / f, candidate / f)
            if mutate is None:
                result = json.loads((candidate / RESULT).read_bytes())
                result["formal_edge_authority_census"]["promoted_edges"] = 8863
                close_result(result); (candidate / RESULT).write_bytes(canonical(result))
            else: rewrite(candidate, mutate)
            proc = subprocess.run(["python3", "-I", "-B", str(VERIFIER), "--candidate-dir", str(candidate)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            rejected = proc.returncode != 0; outcomes.append({"attack": name, "rejected": rejected})
            if not rejected: raise RuntimeError("attack accepted:" + name)
    print(json.dumps({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED", "outcomes": outcomes},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__": raise SystemExit(main())
