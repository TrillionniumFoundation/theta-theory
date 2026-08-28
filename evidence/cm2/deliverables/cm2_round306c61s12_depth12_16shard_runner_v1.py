#!/usr/bin/env python3
"""C61s12 deterministic 16-shard continuation of C58s2 residual leaves.

Modes:
  --inventory       freeze the canonical 2,599-row assignment inventory
  --shard N         evaluate one no-replace shard and freeze ledger + receipt

The aggregate is deliberately a separate step.  No partial shard result has
formal, whole-parent, or D02 credit.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
OUT = SELF.parent
sys.path.insert(0, str(OUT))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41  # noqa: E402


BASE = "cm2_round306c61s12_depth12_16shard"
SCHEMA = "cm2.round306c61s12.depth12-16shard.v1"
SHARD_COUNT = 16
ADDITIONAL_DEPTH = 6
CONTRACT = OUT / "cm2_round306c61s12_independent_contract_v1.json"
C58_BASE = "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement"
C58_RESULT = OUT / (C58_BASE + "_result_v1.json")
C58_LEAVES = OUT / (C58_BASE + "_leaf_ledger_v1.jsonl.gz")
C58_MANIFEST = OUT / (C58_BASE + "_manifest_v1.sha256")
C58_VERIFY = OUT / (C58_BASE + "_independent_verification_v1.json")
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

INVENTORY = OUT / (BASE + "_assignment_inventory_v1.jsonl.gz")
INVENTORY_RESULT = OUT / (BASE + "_assignment_result_v1.json")

PIN = {
    "contract_file": "7f7efeb0a060fea143c9f6a00b4722f2cc87632bff631feb598c434ca969a418",
    "contract_object": "68c6e8a0899c66056724ea29c42949100b2fc6a625865867fd30aacc16d36f7d",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C58_manifest_file": "4cde1af23dbdbcfe4859e971ec698b553664ddaf79c4756e9fd64e59027edc12",
    "C58_verify_file": "054f219baae59fd713fb91718c683e09a660f135aeec0c347cf66465c42a0a89",
    "C58_verify_object": "6a2a44da030eabf43ace42d28c55001e61a6c6e4f0de66a09cbfe65eafdf337a",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key:" + key)
            answer[key] = value
        return answer
    value = json.loads(path.read_text(), object_pairs_hook=hook)
    need(type(value) is dict, "JSON object:" + path.name)
    return value


def validate_object(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    need(file_sha(path) == file_pin, "file pin:" + path.name)
    value = strict_json(path)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object pin:" + path.name)
    return value


def assignment_preimage(ordinal: int, path: str) -> bytes:
    need(type(ordinal) is int and ordinal >= 0, "assignment ordinal")
    need(type(path) is str and bool(path) and set(path) <= {"0", "1"}, "assignment path")
    return canonical({"path": path, "source_handoff_ordinal": ordinal})


def shard_id(ordinal: int, path: str) -> tuple[int, str]:
    claim = hashlib.sha256(assignment_preimage(ordinal, path)).hexdigest()
    return int(claim, 16) % SHARD_COUNT, claim


def closed_rows(path: Path, descriptor: dict[str, Any], pin: str) -> list[dict[str, Any]]:
    need(file_sha(path) == descriptor["sha256"] == pin, "ledger pin:" + path.name)
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            body = copy.deepcopy(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
            sequence.update((claim + "\n").encode("ascii"))
            answer.append(row)
    need(len(answer) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    return answer


class Writer:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> "Writer":
        need(not self.path.exists(), "no-replace:" + self.path.name)
        self.raw = self.path.open("xb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> dict[str, Any]:
        claim = digest(row)
        closed = {**row, "row_sha256": claim}
        self.stream.write(canonical(closed) + b"\n")
        self.sequence.update((claim + "\n").encode("ascii"))
        self.count += 1
        return closed

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order, "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    contract = validate_object(CONTRACT, PIN["contract_file"], PIN["contract_object"])
    need(contract["assignment"]["preimage"] == {
        "encoding": "UTF-8", "ensure_ascii": False, "json_separators": [",", ":"],
        "keys_lexicographically_sorted": True,
        "schema": {"path": "JSON string", "source_handoff_ordinal": "integer"},
        "trailing_newline": False,
    } and contract["assignment"]["shard_id_formula"] ==
         "int(SHA256(preimage),16)%16", "final assignment contract")
    result = validate_object(C58_RESULT, PIN["C58_result_file"], PIN["C58_result_object"])
    need(file_sha(C58_MANIFEST) == PIN["C58_manifest_file"], "C58 manifest pin")
    verification = validate_object(C58_VERIFY, PIN["C58_verify_file"], PIN["C58_verify_object"])
    need(verification["status"].startswith("PASS_COLD_NO_C58_PRODUCER_EXACT_NUMERIC_REPLAY"),
         "C58 independent verification status")
    leaves = closed_rows(C58_LEAVES, result["ledgers"]["leaves"], PIN["C58_leaf_file"])
    selected = [row for row in leaves if row["disposition"] == "COLLISION2_HANDOFF"]
    need(len(selected) == 2599 and all(row["collision2_handoff"]["next_collision_index"] == 2
                                      for row in selected), "2599 exact C58 residual inputs")
    return result, selected


def make_inventory() -> dict[str, Any]:
    _result, selected = inputs()
    writer = Writer(INVENTORY, "SOURCE_HANDOFF_ORDINAL_THEN_PATH")
    counts = [0] * SHARD_COUNT
    preimage_sequence = hashlib.sha256()
    seen: set[tuple[int, str]] = set()
    with writer:
        for source in selected:
            ordinal = source["source_handoff_ordinal"]
            path = source["path"]
            key = (ordinal, path)
            need(key not in seen, "assignment key unique")
            seen.add(key)
            shard, preimage_sha = shard_id(ordinal, path)
            counts[shard] += 1
            preimage_sequence.update((preimage_sha + "\n").encode("ascii"))
            writer.write({
                "schema": SCHEMA + ".assignment-row",
                "assignment_preimage_schema": {
                    "encoding": "UTF-8", "ensure_ascii": False,
                    "json_separators": [",", ":"], "keys_lexicographically_sorted": True,
                    "schema": {"path": "JSON string", "source_handoff_ordinal": "integer"},
                    "trailing_newline": False,
                },
                "assignment_preimage_sha256": preimage_sha,
                "source_handoff_ordinal": ordinal, "path": path, "shard_id": shard,
                "C58_leaf_row_sha256": source["row_sha256"],
                "C58_handoff_object_sha256": source["collision2_handoff"]["handoff_object_sha256"],
                "pair_index": source["pair_index"],
                "parent_volume_fraction": source["parent_volume_fraction"],
                "assignment_credit": 0, "D02_gate_credit": 0,
            })
    need(len(seen) == 2599 and sum(counts) == 2599 and all(counts), "assignment total/nonempty shards")
    value: dict[str, Any] = {
        "schema": SCHEMA + ".assignment-result",
        "status": "FROZEN_COMPLETE_MUTUALLY_EXCLUSIVE_2599_TO_16_CANONICAL_JSON_ASSIGNMENT",
        "independent_contract": {"file_sha256": PIN["contract_file"],
                                 "object_sha256": PIN["contract_object"]},
        "C58_source": {"result_object_sha256": PIN["C58_result_object"],
                       "manifest_sha256": PIN["C58_manifest_file"],
                       "verification_object_sha256": PIN["C58_verify_object"]},
        "assignment_preimage_schema": {
            "encoding": "UTF-8", "ensure_ascii": False,
            "json_separators": [",", ":"], "keys_lexicographically_sorted": True,
            "schema": {"path": "JSON string", "source_handoff_ordinal": "integer"},
            "trailing_newline": False,
        },
        "assignment_formula": "int(SHA256(preimage),16)%16",
        "inventory": writer.descriptor(),
        "input_count": 2599, "shard_count": SHARD_COUNT,
        "per_shard_input_counts": {str(index): count for index, count in enumerate(counts)},
        "ordered_preimage_sha256_line_sequence_sha256": preimage_sequence.hexdigest(),
        "assignment_complete": True, "assignment_mutually_exclusive": True,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    need(not INVENTORY_RESULT.exists(), "inventory result no-replace")
    INVENTORY_RESULT.write_bytes(canonical(value) + b"\n")
    return value


def inventory_rows() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    value = strict_json(INVENTORY_RESULT)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and digest(body) == claim, "inventory result closure")
    rows = closed_rows(INVENTORY, value["inventory"], value["inventory"]["sha256"])
    need(len(rows) == 2599, "inventory row count")
    return value, rows


def run_shard(shard: int) -> dict[str, Any]:
    need(0 <= shard < SHARD_COUNT, "shard range")
    _c58, sources = inputs()
    inventory_result, inventory = inventory_rows()
    by_hash = {row["row_sha256"]: row for row in sources}
    assigned = [row for row in inventory if row["shard_id"] == shard]
    need(len(assigned) == inventory_result["per_shard_input_counts"][str(shard)], "shard inventory count")

    context = c41.load_context(C40, None, formal=False)
    need(context["result"]["object_sha256"] == PIN["C40_object"], "C40 context object")
    c41.install_complete_immutable_cache()
    config = c41.decode_worker_config(context["config"])
    c40_rows = c41.c38.read_ledger(C40, context["result"]["ledgers"]["routed_leaf_cells"])
    c40_index = {row["row_sha256"]: (ordinal, row) for ordinal, row in enumerate(c40_rows)}

    ledger_path = OUT / (BASE + f"_shard_{shard:02d}_leaf_ledger_v1.jsonl.gz")
    receipt_path = OUT / (BASE + f"_shard_{shard:02d}_receipt_v1.json")
    need(not ledger_path.exists() and not receipt_path.exists(), "shard no-replace targets")
    writer = Writer(ledger_path, "ASSIGNMENT_ROW_ORDER_THEN_PATH")
    route_count = 0
    output_counts = {"STRICT_TERMINAL": 0, "COLLISION3_READY": 0, "COLLISION2_HANDOFF": 0}
    raw_census: dict[str, int] = {}
    assignment_sequence = hashlib.sha256()
    source_summaries: list[dict[str, Any]] = []
    with writer:
        for assignment in assigned:
            source = by_hash[assignment["C58_leaf_row_sha256"]]
            need(source["source_handoff_ordinal"] == assignment["source_handoff_ordinal"] and
                 source["path"] == assignment["path"], "assignment/source binding")
            expected_shard, preimage_sha = shard_id(source["source_handoff_ordinal"], source["path"])
            need(expected_shard == shard and preimage_sha == assignment["assignment_preimage_sha256"],
                 "canonical assignment replay")
            assignment_sequence.update((preimage_sha + "\n").encode("ascii"))
            c40_ordinal, c40_source = c40_index[source["C40_source_row_sha256"]]
            task = c41.task_for_row(c40_ordinal, c40_source, context)
            stack: list[tuple[str, int, Fraction]] = [
                (source["path"], 0, Fraction(source["parent_volume_fraction"]))
            ]
            final: list[dict[str, Any]] = []
            while stack:
                path, depth, volume = stack.pop()
                route = c41.route_at_path(task, path, config)
                route_count += 1
                family = c41.disposition_family(route["classification"])
                if family == "RESIDUAL_OUTER" and depth < ADDITIONAL_DEPTH:
                    stack.append((path + "1", depth + 1, volume / 2))
                    stack.append((path + "0", depth + 1, volume / 2))
                    continue
                if family == "TERMINAL_EXCLUDED":
                    disposition = "STRICT_TERMINAL"; next_collision = None
                elif family == "COLLISION3_READY":
                    disposition = "COLLISION3_READY"; next_collision = 3
                else:
                    disposition = "COLLISION2_HANDOFF"; next_collision = 2
                raw_census[route["classification"]] = raw_census.get(route["classification"], 0) + 1
                output_counts[disposition] += 1
                exact_box = c41.box_payload(route["box"])
                reflected_box = c41.reflected_box(task["c38_source"]["representative_origin_key"], route["box"])
                continuation: dict[str, Any] | None = None
                if next_collision is not None:
                    continuation = {
                        "next_collision_index": next_collision,
                        "prior_C58_leaf_row_sha256": source["row_sha256"],
                        "prior_C58_handoff_object_sha256": source["collision2_handoff"]["handoff_object_sha256"],
                        "collision1_history_row_sha256": source["collision2_handoff"]["collision1_history_row_sha256"],
                        "collision1_original_owner": source["collision2_handoff"]["collision1_original_owner"],
                        "collision1_event_order": source["collision2_handoff"]["collision1_event_order"],
                        "exact_representative_box": exact_box, "exact_reflected_box": reflected_box,
                        "route_classification": route["classification"], "route_witness": route["witness"],
                        "route_method": route["route_method"], "continuation_credit": 0,
                    }
                    continuation["continuation_object_sha256"] = digest(continuation)
                final.append(writer.write({
                    "schema": SCHEMA + ".shard-leaf-row", "shard_id": shard,
                    "assignment_preimage_sha256": preimage_sha,
                    "source_handoff_ordinal": source["source_handoff_ordinal"],
                    "source_C58_leaf_row_sha256": source["row_sha256"],
                    "source_path": source["path"], "path": path,
                    "additional_depth_from_C58": depth,
                    "pair_index": source["pair_index"], "parent_volume_fraction": str(volume),
                    "exact_representative_box": exact_box, "exact_reflected_box": reflected_box,
                    "route_classification": route["classification"], "route_witness": route["witness"],
                    "route_method": route["route_method"], "disposition": disposition,
                    "continuation": continuation, "local_terminal_credit": 1 if disposition == "STRICT_TERMINAL" else 0,
                    "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
                }))
            paths = [row["path"] for row in final]
            ordered = sorted(paths, key=lambda value: (len(value), value))
            need(all(not later.startswith(first) for index, first in enumerate(ordered)
                     for later in ordered[index + 1:]), "source prefix-free")
            need(sum(Fraction(row["parent_volume_fraction"]) for row in final) ==
                 Fraction(source["parent_volume_fraction"]), "source Kraft")
            source_summaries.append({
                "assignment_preimage_sha256": preimage_sha,
                "source_C58_leaf_row_sha256": source["row_sha256"],
                "source_output_row_count": len(final),
                "source_output_row_hash_line_sequence_sha256": hashlib.sha256(
                    "".join(row["row_sha256"] + "\n" for row in final).encode("ascii")).hexdigest(),
                "source_Kraft_conservation": source["parent_volume_fraction"],
                "source_prefix_free": True,
            })
    receipt: dict[str, Any] = {
        "schema": SCHEMA + ".shard-receipt", "status": "PASS_COMPLETE_NO_REPLACE_SHARD",
        "shard_id": shard, "shard_count": SHARD_COUNT,
        "assignment_contract_file_sha256": PIN["contract_file"],
        "assignment_contract_object_sha256": PIN["contract_object"],
        "assignment_result_object_sha256": inventory_result["object_sha256"],
        "assignment_inventory_sha256": inventory_result["inventory"]["sha256"],
        "assignment_preimage_schema": inventory_result["assignment_preimage_schema"],
        "assignment_formula": inventory_result["assignment_formula"],
        "assigned_input_count": len(assigned),
        "ordered_assignment_preimage_sha256_line_sequence_sha256": assignment_sequence.hexdigest(),
        "input_assignment_rows": source_summaries,
        "route_evaluation_count": route_count, "output_disposition_census": output_counts,
        "raw_classification_census": dict(sorted(raw_census.items())),
        "output_ledger": writer.descriptor(),
        "shard_complete": True, "partial_statistics_are_formal_credit": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    receipt["object_sha256"] = digest(receipt)
    receipt_path.write_bytes(canonical(receipt) + b"\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inventory", action="store_true")
    group.add_argument("--shard", type=int)
    args = parser.parse_args()
    try:
        value = make_inventory() if args.inventory else run_shard(args.shard)
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, ValueError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
