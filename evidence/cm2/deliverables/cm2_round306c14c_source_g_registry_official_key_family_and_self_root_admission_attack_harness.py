#!/usr/bin/env python3
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
PREFIX = "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission"
ADMISSIONS = PREFIX + "_new_exact_sheet_admission_ledger.jsonl.gz"
FAMILIES = PREFIX + "_old_outer_envelope_family_disposition_ledger.jsonl.gz"
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
    plain = hashlib.sha256()
    count = 0
    with gzip.open(candidate / filename, "rb") as source, \
            gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                          fileobj=output, mtime=0) as target:
        for line in source:
            row = json.loads(line)
            if count == 0:
                mutate(row)
                close_row(row)
            wire = canonical(row) + b"\n"
            target.write(wire)
            plain.update(wire)
            count += 1
    compressed = output.getvalue()
    (candidate / filename).write_bytes(compressed)
    result = json.loads((candidate / RESULT).read_bytes())
    result[descriptor_key].update({
        "row_count": count,
        "size": len(compressed),
        "sha256": hashlib.sha256(compressed).hexdigest(),
        "uncompressed_sha256": plain.hexdigest(),
    })
    close_result(result)
    (candidate / RESULT).write_bytes(canonical(result))


def admission_mutation(kind: str) -> Callable[[dict[str, Any]], None]:
    def mutate(row: dict[str, Any]) -> None:
        if kind == "registry":
            row["registry_member_admission_credit"] = 0
        elif kind == "official-key":
            row["official_key_binding_credit"] = 0
        elif kind == "root-inheritance":
            row["old_root_or_component_inheritance_credit"] = 1
        elif kind == "component":
            row["fresh_component_assignment_credit"] = 1
        elif kind == "edge":
            row["DSU_edge_or_union_authorized"] = True
        else:
            raise AssertionError(kind)
    return mutate


def family_mutation(kind: str) -> Callable[[dict[str, Any]], None]:
    def mutate(row: dict[str, Any]) -> None:
        if kind == "family":
            row["old_family_after"] = "UNRESOLVED"
        elif kind == "delete":
            row["old_member_retained"] = False
            row["member_deletion_or_invalidation_credit"] = 1
        else:
            raise AssertionError(kind)
    return mutate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    source = Path(args.candidate_dir).resolve()
    attacks = [
        ("member-census", "result", None),
        ("old-family-unresolved", "family", family_mutation("family")),
        ("old-member-deletion", "family", family_mutation("delete")),
        ("registry-admission-revoked", "admission", admission_mutation("registry")),
        ("official-key-binding-revoked", "admission", admission_mutation("official-key")),
        ("old-root-inheritance", "admission", admission_mutation("root-inheritance")),
        ("premature-component", "admission", admission_mutation("component")),
        ("premature-edge", "admission", admission_mutation("edge")),
    ]
    outcomes = []
    for name, target, mutation in attacks:
        with tempfile.TemporaryDirectory(prefix="c14c-attack-") as tmp:
            candidate = Path(tmp)
            for filename in (ADMISSIONS, FAMILIES, RESULT):
                shutil.copy2(source / filename, candidate / filename)
            if target == "result":
                result = json.loads((candidate / RESULT).read_bytes())
                result["formal_member_and_family_census"]["member_count"] = 502203
                close_result(result)
                (candidate / RESULT).write_bytes(canonical(result))
            elif target == "family":
                rewrite(candidate, FAMILIES, "old_outer_envelope_family_disposition_ledger", mutation)
            else:
                rewrite(candidate, ADMISSIONS, "new_exact_sheet_admission_ledger", mutation)
            process = subprocess.run(
                ["python3", "-I", "-B", str(VERIFIER), "--candidate-dir", str(candidate)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            rejected = process.returncode != 0
            outcomes.append({"attack": name, "rejected": rejected})
            if not rejected:
                raise RuntimeError("attack accepted:" + name)
    print(json.dumps({"status": "PASS_8_OF_8_COHERENT_ATTACKS_REJECTED",
                      "outcomes": outcomes}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
