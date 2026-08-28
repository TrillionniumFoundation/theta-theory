#!/usr/bin/env python3
"""Run eight coherently reclosed attacks against the C14b verifier."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).parent
PREFIX = "cm2_round306c14b_source_g_exact_partial_sheet_rematerialization_and_member_delta"
SHEETS = PREFIX + "_exact_sheet_member_ledger.jsonl.gz"
DISPOSITIONS = PREFIX + "_outer_envelope_disposition_ledger.jsonl.gz"
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
            mutate: Callable[[dict[str, Any]], None]) -> None:
    output = io.BytesIO()
    plain_hash = hashlib.sha256()
    ordered_hash = hashlib.sha256()
    ordered_hash.update(b"[")
    plain_size = 0
    count = 0
    with gzip.open(candidate / filename, "rb") as source, \
            gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                          fileobj=output, mtime=0) as target:
        for line in source:
            row = json.loads(line)
            if count == 0:
                mutate(row)
                close_row(row)
            wire = canonical(row)
            jsonl = wire + b"\n"
            target.write(jsonl)
            plain_hash.update(jsonl)
            plain_size += len(jsonl)
            if count:
                ordered_hash.update(b",")
            ordered_hash.update(wire)
            count += 1
    ordered_hash.update(b"]")
    compressed = output.getvalue()
    (candidate / filename).write_bytes(compressed)
    result = json.loads((candidate / RESULT).read_bytes())
    result[descriptor_key].update({
        "row_count": count,
        "compressed_size": len(compressed),
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "uncompressed_size": plain_size,
        "uncompressed_sha256": plain_hash.hexdigest(),
        "ordered_rows_sha256": ordered_hash.hexdigest(),
    })
    close_result(result)
    (candidate / RESULT).write_bytes(canonical(result))


def sheet_mutation(kind: str) -> Callable[[dict[str, Any]], None]:
    def mutate(row: dict[str, Any]) -> None:
        if kind == "natural-key":
            row["new_exact_sheet_natural_key"][0] = "UNTYPED_SHEET"
        elif kind == "projection":
            cert = row["graph_to_new_sheet_set_equality_certificate"]
            cert["projection_is_bijection"] = False
            core = dict(cert)
            core.pop("certificate_sha256", None)
            cert["certificate_sha256"] = obj(core)
        elif kind == "registry-admission":
            row["registry_member_admission_credit"] = 1
        elif kind == "root-inheritance":
            row["base_root_or_component_inheritance_credit"] = 1
        else:
            raise AssertionError(kind)
    return mutate


def disposition_mutation(kind: str) -> Callable[[dict[str, Any]], None]:
    def mutate(row: dict[str, Any]) -> None:
        if kind == "family":
            row["old_member_family_after"] = "NON_GRAPH"
            row["old_member_reclassification_credit"] = 1
        elif kind == "invalidate":
            row["old_outer_envelope_physical_member_retained"] = False
            row["old_member_deletion_or_invalidation_credit"] = 1
        elif kind == "edge-transfer":
            row["old_component_or_edge_transfer_to_new_member_credit"] = 1
            row["DSU_edge_or_union_authorized"] = True
        else:
            raise AssertionError(kind)
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    attacks = [
        ("conditional-member-census", "result", None),
        ("natural-key-domain", "sheet", sheet_mutation("natural-key")),
        ("projection-bijection", "sheet", sheet_mutation("projection")),
        ("registry-admission", "sheet", sheet_mutation("registry-admission")),
        ("root-component-inheritance", "sheet", sheet_mutation("root-inheritance")),
        ("family-reclassification", "disposition", disposition_mutation("family")),
        ("old-member-invalidation", "disposition", disposition_mutation("invalidate")),
        ("old-edge-transfer", "disposition", disposition_mutation("edge-transfer")),
    ]
    outcomes = []
    for name, target, mutation in attacks:
        with tempfile.TemporaryDirectory(prefix="c14b-attack-") as tmp:
            candidate = Path(tmp)
            for filename in (SHEETS, DISPOSITIONS, RESULT):
                shutil.copy2(source / filename, candidate / filename)
            if target == "result":
                result = json.loads((candidate / RESULT).read_bytes())
                result["census"]["candidate_member_count_if_admitted"] = 502203
                close_result(result)
                (candidate / RESULT).write_bytes(canonical(result))
            elif target == "sheet":
                rewrite(candidate, SHEETS, "exact_sheet_member_ledger", mutation)
            else:
                rewrite(candidate, DISPOSITIONS, "outer_envelope_disposition_ledger", mutation)
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
