#!/usr/bin/env python3
"""Materialize all 10,660 INCLUDED_STRATUM_ATTACHMENTS candidates.

The selection and row semantics are delegated to the already-pinned fresh
stream subgate implementation.  A separately executed SQLite implementation
is required by the independent verifier; this producer does not treat its own
module lineage as independent evidence.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "deliverables"
STREAM = HERE / "cm2_c27_included_stratum_attachments_stream_probe.py"
STREAM_SHA256 = "f4e821830b610de5be82f6593dc4ab4fa1d4aa64462c47b75af642ae48023a00"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def load_stream():
    need(file_hash(STREAM) == STREAM_SHA256, "fresh stream source pin")
    spec = importlib.util.spec_from_file_location("cm2_included_fresh_stream", STREAM)
    need(spec is not None and spec.loader is not None, "stream module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_gzip(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for value in rows:
                packed.write(canonical(value) + b"\n")


def build(seed: int, output: Path) -> dict[str, Any]:
    need(type(seed) is int, "true integer seed")
    need(not output.exists(), "fresh output directory")
    stream = load_stream()

    # First run the published fresh implementation end to end.  This binds the
    # exact commitments that the row materialization below must reproduce.
    authority = stream.build(seed)
    need(authority["status"].startswith("PASS_ZERO_CREDIT__10660_INCLUDED")
         and authority["candidate_universe"]["candidate_count"] == 10_660
         and authority["formal_credit"] == 0, "fresh stream authority")

    c20d_rows: dict[str, dict[str, Any]] = {}
    c20d_census: Counter[str] = Counter()
    for ordinal, value in enumerate(stream.rows(HERE / stream.C20D)):
        need(value.get("ordinal") == ordinal, "C20D ordinal")
        stream.check_row(value, "C20D")
        representation = value["representation_id"]
        need(representation not in c20d_rows, "C20D representation unique")
        c20d_rows[representation] = value
        c20d_census[value["source_semantics"]] += 1
    need(len(c20d_rows) == 2_520
         and dict(c20d_census) == stream.C20D_SEMANTICS, "C20D census")

    selected: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]] = []
    selected_owners: set[str] = set()
    excluded: set[str] = set()
    c25_iter = stream.rows(HERE / stream.C25)
    c26_iter = stream.rows(HERE / stream.C26)
    for ordinal in range(stream.FULL_COUNTS[stream.C25]):
        c25 = next(c25_iter, None)
        c26 = next(c26_iter, None)
        need(c25 is not None and c26 is not None, "C25/C26 length")
        need(c25["representation_ordinal"] == ordinal
             and c26["handle_ordinal"] == ordinal, "C25/C26 ordinal")
        need(c25["representation_id"] == c26["representation_id"]
             and c25["owner_member_id"] == c26["owner_member_id"]
             and c25["fresh_component_id"] == c26["fresh_component_id"]
             and c25["representation_semantic_kind"]
                 == c26["representation_semantic_kind"]
             and c26["source_bindings"]["C25_representation_row_sha256"]
                 == c25["row_sha256"], "C25/C26 lockstep")
        kind = c25["representation_semantic_kind"]
        kernel = c25.get("source_bindings", {}).get("semantic_kernel")
        c20d = c20d_rows.get(c25["representation_id"]) if kernel == "C20D" else None
        if c20d is not None and c20d["source_semantics"] == "ADJACENT_POSITIVE_T_CONTINUATION":
            excluded.add(c25["representation_id"])
        if (kind not in stream.SELECTED_KINDS
                or (c20d is not None
                    and c20d["source_semantics"] not in stream.C20D_STRICT)):
            continue
        selected.append((c25, c26, c20d))
        selected_owners.add(c25["owner_member_id"])
    need(next(c25_iter, None) is None and next(c26_iter, None) is None,
         "C25/C26 exhaustion")
    need(len(selected) == 10_660 and len(excluded) == 276,
         "selected/excluded census")

    owners: dict[str, dict[str, Any]] = {}
    for ordinal, value in enumerate(stream.rows(HERE / stream.C15)):
        need(value["member_ordinal"] == ordinal, "C15 ordinal")
        member = value["registry_member_id"]
        if member in selected_owners:
            stream.check_row(value, "selected C15")
            need(member not in owners, "C15 owner unique")
            owners[member] = value
    need(set(owners) == selected_owners, "C15 owner cover")

    bodies = []
    for c25, c26, c20d in selected:
        body = stream.validate_triplet(owners[c25["owner_member_id"]],
                                       c25, c26, c20d)
        bodies.append(body)
    bodies.sort(key=lambda value: value["representation_id"])
    need(len({value["representation_id"] for value in bodies}) == 10_660,
         "candidate unique")

    ids = hashlib.sha256()
    semantic_sequence = hashlib.sha256()
    rows = []
    for ordinal, body in enumerate(bodies):
        semantic_sha = digest(body)
        ids.update(body["representation_id"].encode("ascii") + b"\n")
        semantic_sequence.update(bytes.fromhex(semantic_sha))
        normalized_body = {
            "schema": "cm2.c27-independent.included-stratum-attachment.materialized-candidate-row.v1",
            "ordinal": ordinal, "terminal": "INCLUDED_STRATUM_ATTACHMENTS",
            **body, "semantic_body_sha256": semantic_sha,
            "terminal_disposition":
                "UNIQUE_INCLUDED_STRATUM_ATTACHMENT__NOT_RETAINED_CONTINUATION",
            "retained_continuation_candidate": False,
            "source_W_transition_authorized": False,
        }
        rows.append({**normalized_body, "row_sha256": digest(normalized_body)})
    commitment = authority["candidate_universe"]
    need(ids.hexdigest() == commitment["candidate_representation_ids_sha256"]
         and semantic_sequence.hexdigest()
             == commitment["candidate_row_sequence_sha256"],
         "published commitment exact reproduction")

    output.mkdir(parents=True, exist_ok=False)
    ledger = output / "included_stratum_10660_materialized_candidates.jsonl.gz"
    write_gzip(ledger, rows)
    result_body = {
        "schema": "cm2.c27-independent.included-stratum-10660-candidate-materialization.result.v1",
        "status": "PASS_10660_INCLUDED_STRATUM_CANDIDATES_MATERIALIZED_FROM_FRESH_STREAM_AUTHORITY__ZERO_CREDIT",
        "candidate_count": 10_660, "excluded_retained_count": 276,
        "candidate_excluded_intersection_count": 0,
        "candidate_representation_ids_sha256": ids.hexdigest(),
        "semantic_body_sequence_sha256": semantic_sequence.hexdigest(),
        "ledger": {"filename": ledger.name, "file_sha256": file_hash(ledger),
                   "row_count": len(rows),
                   "row_sequence_sha256":
                       digest([value["row_sha256"] for value in rows])},
        "fresh_stream_authority": {
            "source_path": str(STREAM.relative_to(ROOT)),
            "source_sha256": STREAM_SHA256,
            "result_sha256": authority["result_sha256"],
            "published_candidate_commitment_exactly_reproduced": True,
        },
        "independent_sqlite_verification_required": True,
        "seed_declared_but_not_semantically_used": True,
        "old_C27_FAMILIES_imported_or_read": False,
        "old_transition_or_edge_ledger_used_as_candidate_universe": False,
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
        "strict_nonpromotion": {"C27": 0, "C28": 0, "C29": 0,
                                "CM2": "NO-GO_FOR_CLAIM"},
    }
    result = {**result_body, "result_sha256": digest(result_body)}
    (output / "result.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        result = build(args.seed, Path(args.output_dir))
    except (Reject, RuntimeError, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
