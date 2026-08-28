#!/usr/bin/env python3
"""C65s18 deterministic 64-shard continuation of C61s12 C2 residuals.

Modes:
  --contract-check  replay the frozen source/contract boundary without writes
  --inventory       freeze the canonical 20,879-row assignment inventory
  --shard N         evaluate one no-replace shard and freeze ledger + receipt

Every partial artifact is deliberately zero-credit.  A later, separately
audited aggregate is required before any whole-parent conclusion is possible.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import stat
import sys
from typing import Any


SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
OUT = SELF.parent
sys.path.insert(0, str(OUT))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41  # noqa: E402


BASE = "cm2_round306c65s18_depth18_64shard_v2"
SCHEMA = "cm2.round306c65s18.depth18-64shard.v2"
SHARD_COUNT = 64
ADDITIONAL_DEPTH = 6
ASSIGNMENT_DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
C61_BASE = "cm2_round306c61s12_depth12_16shard"
C61_RESULT = OUT / (C61_BASE + "_aggregate_result_v4.json")
C61_LEAVES = OUT / (C61_BASE + "_aggregate_leaf_ledger_v4.jsonl.gz")
C61_MANIFEST = OUT / (C61_BASE + "_manifest_v4.sha256")
C61_VERIFY = OUT / "cm2_round306c61s12_independent_postexecution_verification_v4.json"
C61_SELFTEST = OUT / "cm2_round306c61s12_independent_postexecution_self_test_v4.json"
C58_BASE = "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement"
C58_RESULT = OUT / (C58_BASE + "_result_v1.json")
C58_LEAVES = OUT / (C58_BASE + "_leaf_ledger_v1.jsonl.gz")
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

INVENTORY = OUT / (BASE + "_assignment_inventory_v1.jsonl.gz")
INVENTORY_RESULT = OUT / (BASE + "_assignment_result_v1.json")

PIN = {
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_manifest_file": "4c18c510367fc15b801fb6eff7901ad94a8fd53e47a6b7868ee876b554393545",
    "C61_verify_file": "2dc773d0051cc9668cdf7752fb61ac09f495044f566972faa335fffc509e9fc7",
    "C61_verify_object": "066e03be0c41600f5fb5cc2c157fe6e7eb04d1060896dd1acc910b06aab30b24",
    "C61_selftest_file": "b5a6ad21006d690637c797e7459363f2d6d8e55ad3abd5c112e817de5f915f32",
    "C61_selftest_object": "77a6091d60a883826fc4f9e8786128ae6dd9e79bcfc7d8662b9da1ed0262339e",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
}

ASSIGNMENT_PREIMAGE_SCHEMA = {
    "encoding": "UTF-8",
    "ensure_ascii": False,
    "allow_nan": False,
    "json_separators": [",", ":"],
    "keys_lexicographically_sorted": True,
    "schema": {
        "assignment_domain": "exact literal cm2.round306c65s18.depth18-64shard.v2.assignment",
        "path": "exact 21-bit source path",
        "source_C61_aggregate_leaf_row_sha256": "64 lowercase hexadecimal characters",
    },
    "trailing_newline": False,
    "BOM": False,
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


def snapshot(path: Path) -> tuple[int, int, int, int, int, int, int]:
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and not path.is_symlink(),
         "regular non-symlink single-link input:" + path.name)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def exclusive_json(path: Path, value: dict[str, Any]) -> None:
    need(not path.is_symlink(), "no symlink output:" + path.name)
    flags = __import__("os").O_WRONLY | __import__("os").O_CREAT | __import__("os").O_EXCL
    flags |= getattr(__import__("os"), "O_NOFOLLOW", 0)
    descriptor = __import__("os").open(path, flags, 0o644)
    try:
        with __import__("os").fdopen(descriptor, "wb") as stream:
            stream.write(canonical(value) + b"\n")
            stream.flush()
            __import__("os").fsync(stream.fileno())
    except BaseException:
        raise
    snapshot(path)


def strict_json(path: Path) -> dict[str, Any]:
    before = snapshot(path)

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key:" + key)
            answer[key] = value
        return answer

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)
    need(snapshot(path) == before, "TOCTOU JSON input:" + path.name)
    need(type(value) is dict, "JSON object:" + path.name)
    return value


def validate_object(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    before = snapshot(path)
    need(file_sha(path) == file_pin, "file pin:" + path.name)
    value = strict_json(path)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object pin:" + path.name)
    need(snapshot(path) == before, "TOCTOU object input:" + path.name)
    return value


def assignment_preimage(row_sha: str, path: str) -> bytes:
    need(type(row_sha) is str and len(row_sha) == 64 and
         set(row_sha) <= set("0123456789abcdef"), "assignment C61 row SHA")
    need(type(path) is str and len(path) == 21 and set(path) <= {"0", "1"},
         "assignment exact 21-bit path")
    return canonical({"assignment_domain": ASSIGNMENT_DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": row_sha})


def shard_id(row_sha: str, path: str) -> tuple[int, str]:
    claim = hashlib.sha256(assignment_preimage(row_sha, path)).hexdigest()
    return int(claim, 16) % SHARD_COUNT, claim


def closed_rows(path: Path, descriptor: dict[str, Any], pin: str) -> list[dict[str, Any]]:
    before = snapshot(path)
    need(file_sha(path) == descriptor["sha256"] == pin, "ledger pin:" + path.name)
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            need(type(row) is dict, "ledger row object:" + path.name)
            body = copy.deepcopy(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
            sequence.update((claim + "\n").encode("ascii"))
            answer.append(row)
    need(len(answer) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    need(snapshot(path) == before, "TOCTOU ledger input:" + path.name)
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
        need(not self.path.exists() and not self.path.is_symlink(), "no-replace:" + self.path.name)
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
        snapshot(self.path)

    def descriptor(self) -> dict[str, Any]:
        snapshot(self.path)
        return {"filename": self.path.name, "order": self.order, "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def inputs() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    contract = validate_object(CONTRACT, PIN["contract_file"], PIN["contract_object"])
    need(contract["assignment"]["preimage"] == ASSIGNMENT_PREIMAGE_SCHEMA and
         contract["assignment"]["shard_id_formula"] ==
         "int(SHA256(preimage),16)%64" and
         contract["assignment"]["shard_ids_exactly"] == list(range(64)),
         "final assignment contract")
    need(contract["refinement"]["additional_binary_depth"] == ADDITIONAL_DEPTH and
         contract["formal_credit"] == contract["whole_parent_credit"] ==
         contract["D02_gate_credit"] == 0, "contract depth and zero-credit boundary")

    result = validate_object(C61_RESULT, PIN["C61_result_file"], PIN["C61_result_object"])
    before_manifest = snapshot(C61_MANIFEST)
    need(file_sha(C61_MANIFEST) == PIN["C61_manifest_file"], "C61 final manifest pin")
    need(snapshot(C61_MANIFEST) == before_manifest, "TOCTOU C61 manifest")
    verification = validate_object(C61_VERIFY, PIN["C61_verify_file"], PIN["C61_verify_object"])
    need(verification["status"].startswith("PASS_INDEPENDENT_V4_ONLY_COMPLETE_16_SHARD_AGGREGATE"),
         "C61 independent verification status")
    selftest = validate_object(C61_SELFTEST, PIN["C61_selftest_file"], PIN["C61_selftest_object"])
    need(selftest["status"] ==
         "PASS_40_OF_40_FROZEN_SCHEMA_ASSIGNMENT_V4_AGGREGATE_TOCTOU_AND_COHERENT_HOSTILE_TESTS",
         "C61 independent self-test status")
    leaves = closed_rows(C61_LEAVES, result["ledgers"]["aggregate_leaves"], PIN["C61_leaf_file"])
    selected = [row for row in leaves if row["disposition"] == "COLLISION2_HANDOFF"]
    need(len(selected) == contract["assignment"]["source_input_count"] == 20879 and
         all(row["continuation"]["next_collision_index"] == 2 for row in selected),
         "20879 exact C61 C2 residual inputs")
    source_sequence = hashlib.sha256()
    continuation_sequence = hashlib.sha256()
    for row in selected:
        source_sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        continuation_sequence.update(
            (row["continuation"]["continuation_object_sha256"] + "\n").encode("ascii"))
    need(source_sequence.hexdigest() ==
         contract["selection"]["filtered_source_row_sha256_line_sequence_sha256"] ==
         "8645ce3a101089526a12b04b9687449769202fc50f6073adf12e0cd11a5595a3" and
         continuation_sequence.hexdigest() ==
         contract["selection"]["filtered_continuation_object_sha256_line_sequence_sha256"] ==
         "0403c8cd4c1c9b4c6b73b43408baf4bb42b10d34a4a55d9098182cb56f6faaca",
         "frozen filtered C61 residual sequences")
    need(all(row["schema"] == contract["selection"]["predicate"]["schema"] and
             row["additional_depth_from_C58"] == 6 and len(row["path"]) == 21 and
             set(row["path"]) <= {"0", "1"} and
             row["parent_volume_fraction"] == "1/2097152" and
             row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == row["local_terminal_credit"] ==
             row["continuation"]["continuation_credit"] == 0 for row in selected),
         "exact C61 residual selection predicate")
    need(len({row["row_sha256"] for row in selected}) == len(selected),
         "C61 selected row identities unique")

    c58_result = validate_object(C58_RESULT, PIN["C58_result_file"], PIN["C58_result_object"])
    c58_rows = closed_rows(C58_LEAVES, c58_result["ledgers"]["leaves"], PIN["C58_leaf_file"])
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_by_hash) == len(c58_rows), "C58 row identities unique")
    for row in selected:
        source = c58_by_hash.get(row["source_C58_leaf_row_sha256"])
        need(source is not None and source["disposition"] == "COLLISION2_HANDOFF",
             "C61 to exact C58 C2 source binding")
        need(row["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
             row["source_path"] == source["path"] and row["path"].startswith(source["path"]) and
             row["pair_index"] == source["pair_index"], "C61/C58 source identity fields")
        need(row["continuation"]["prior_C58_leaf_row_sha256"] == source["row_sha256"] and
             row["continuation"]["prior_C58_handoff_object_sha256"] ==
             source["collision2_handoff"]["handoff_object_sha256"],
             "C61 continuation to C58 handoff binding")
    return result, selected, c58_rows


def contract_check() -> dict[str, Any]:
    _result, selected, _c58 = inputs()
    return {
        "schema": SCHEMA + ".contract-check",
        "status": "PASS_FROZEN_CONTRACT_AND_20879_EXACT_C61_RESIDUAL_INPUTS__ZERO_CREDIT",
        "input_count": len(selected), "shard_count": SHARD_COUNT,
        "additional_binary_depth": ADDITIONAL_DEPTH,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }


def make_inventory() -> dict[str, Any]:
    _result, selected, _c58 = inputs()
    writer = Writer(INVENTORY, "C61_AGGREGATE_LEDGER_ORDER")
    counts = [0] * SHARD_COUNT
    preimage_sequence = hashlib.sha256()
    seen: set[tuple[str, int, str]] = set()
    with writer:
        for source in selected:
            row_sha = source["row_sha256"]
            pair_index = source["pair_index"]
            path = source["path"]
            key = (row_sha, pair_index, path)
            need(key not in seen, "assignment key unique")
            seen.add(key)
            shard, preimage_sha = shard_id(row_sha, path)
            counts[shard] += 1
            preimage_sequence.update((preimage_sha + "\n").encode("ascii"))
            writer.write({
                "schema": SCHEMA + ".assignment-row",
                "assignment_preimage_sha256": preimage_sha,
                "source_C61_aggregate_leaf_row_sha256": row_sha,
                "source_C61_source_shard_row_sha256": source["source_shard_row_sha256"],
                "source_C61_continuation_object_sha256": source["continuation"]["continuation_object_sha256"],
                "source_C58_leaf_row_sha256": source["source_C58_leaf_row_sha256"],
                "source_handoff_ordinal": source["source_handoff_ordinal"],
                "source_path": source["source_path"], "path": path,
                "pair_index": pair_index, "shard_id": shard,
                "parent_volume_fraction": source["parent_volume_fraction"],
                "source_C61_disposition": source["disposition"],
                "source_C61_next_collision_index": source["continuation"]["next_collision_index"],
                "assignment_credit": 0, "formal_credit": 0,
                "whole_parent_credit": 0, "D02_gate_credit": 0,
            })
    need(len(seen) == 20879 and sum(counts) == 20879 and all(counts),
         "assignment total/nonempty shards")
    value: dict[str, Any] = {
        "schema": SCHEMA + ".assignment-result",
        "status": "FROZEN_V2_COMPLETE_MUTUALLY_EXCLUSIVE_20879_TO_64_CANONICAL_JSON_ASSIGNMENT",
        "runner_file_sha256": file_sha(SELF),
        "independent_contract": {"file_sha256": PIN["contract_file"],
                                 "object_sha256": PIN["contract_object"]},
        "C61_source": {"aggregate_result_object_sha256": PIN["C61_result_object"],
                       "aggregate_leaf_ledger_sha256": PIN["C61_leaf_file"],
                       "manifest_sha256": PIN["C61_manifest_file"],
                       "verification_object_sha256": PIN["C61_verify_object"]},
        "assignment_preimage_schema": ASSIGNMENT_PREIMAGE_SCHEMA,
        "assignment_domain": ASSIGNMENT_DOMAIN,
        "assignment_formula": "int(SHA256(preimage),16)%64",
        "inventory": writer.descriptor(),
        "input_count": 20879, "shard_count": SHARD_COUNT,
        "per_shard_input_counts": {str(index): count for index, count in enumerate(counts)},
        "ordered_preimage_sha256_line_sequence_sha256": preimage_sequence.hexdigest(),
        "assignment_complete": True, "assignment_mutually_exclusive": True,
        "partial_statistics_are_formal_credit": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    exclusive_json(INVENTORY_RESULT, value)
    return value


def inventory_rows() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    value = strict_json(INVENTORY_RESULT)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and digest(body) == claim, "inventory result closure")
    need(value["runner_file_sha256"] == file_sha(SELF), "inventory runner pin")
    rows = closed_rows(INVENTORY, value["inventory"], value["inventory"]["sha256"])
    need(len(rows) == 20879 and value["assignment_complete"] is True and
         value["assignment_mutually_exclusive"] is True, "inventory completeness")
    return value, rows


def run_shard(shard: int) -> dict[str, Any]:
    need(type(shard) is int and 0 <= shard < SHARD_COUNT, "shard range")
    _c61, sources, c58_rows = inputs()
    inventory_result, inventory = inventory_rows()
    by_hash = {row["row_sha256"]: row for row in sources}
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    assigned = [row for row in inventory if row["shard_id"] == shard]
    need(len(assigned) == inventory_result["per_shard_input_counts"][str(shard)],
         "shard inventory count")

    context = c41.load_context(C40, None, formal=False)
    need(context["result"]["object_sha256"] == PIN["C40_object"], "C40 context object")
    c41.install_complete_immutable_cache()
    config = c41.decode_worker_config(context["config"])
    c40_rows = c41.c38.read_ledger(C40, context["result"]["ledgers"]["routed_leaf_cells"])
    c40_index = {row["row_sha256"]: (ordinal, row) for ordinal, row in enumerate(c40_rows)}

    ledger_path = OUT / (BASE + f"_shard_{shard:02d}_leaf_ledger_v1.jsonl.gz")
    receipt_path = OUT / (BASE + f"_shard_{shard:02d}_receipt_v1.json")
    need(not ledger_path.exists() and not ledger_path.is_symlink() and
         not receipt_path.exists() and not receipt_path.is_symlink(),
         "shard no-replace targets")
    writer = Writer(ledger_path, "ASSIGNMENT_INVENTORY_ORDER_THEN_PATH")
    route_count = 0
    output_counts = {"STRICT_TERMINAL": 0, "COLLISION3_READY": 0, "COLLISION2_HANDOFF": 0}
    raw_census: dict[str, int] = {}
    assignment_sequence = hashlib.sha256()
    source_summaries: list[dict[str, Any]] = []
    with writer:
        for assignment in assigned:
            source = by_hash[assignment["source_C61_aggregate_leaf_row_sha256"]]
            need(source["row_sha256"] == assignment["source_C61_aggregate_leaf_row_sha256"] and
                 source["source_shard_row_sha256"] == assignment["source_C61_source_shard_row_sha256"] and
                 source["continuation"]["continuation_object_sha256"] ==
                 assignment["source_C61_continuation_object_sha256"] and
                 source["pair_index"] == assignment["pair_index"] and
                 source["path"] == assignment["path"], "assignment/C61 source binding")
            expected_shard, preimage_sha = shard_id(source["row_sha256"], source["path"])
            need(expected_shard == shard and preimage_sha == assignment["assignment_preimage_sha256"],
                 "canonical assignment replay")
            assignment_sequence.update((preimage_sha + "\n").encode("ascii"))

            c58_source = c58_by_hash[source["source_C58_leaf_row_sha256"]]
            need(c58_source["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
                 c58_source["path"] == source["source_path"] and
                 c58_source["pair_index"] == source["pair_index"],
                 "C61 to C58 source binding")
            c40_ordinal, c40_source = c40_index[c58_source["C40_source_row_sha256"]]
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
                    disposition = "STRICT_TERMINAL"
                    next_collision = None
                elif family == "COLLISION3_READY":
                    disposition = "COLLISION3_READY"
                    next_collision = 3
                else:
                    disposition = "COLLISION2_HANDOFF"
                    next_collision = 2
                raw_census[route["classification"]] = raw_census.get(route["classification"], 0) + 1
                output_counts[disposition] += 1
                exact_box = c41.box_payload(route["box"])
                reflected_box = c41.reflected_box(
                    task["c38_source"]["representative_origin_key"], route["box"])
                continuation: dict[str, Any] | None = None
                if next_collision is not None:
                    continuation = {
                        "next_collision_index": next_collision,
                        "prior_C61_aggregate_leaf_row_sha256": source["row_sha256"],
                        "prior_C61_shard_row_sha256": source["source_shard_row_sha256"],
                        "prior_C61_continuation_object_sha256":
                            source["continuation"]["continuation_object_sha256"],
                        "prior_C58_leaf_row_sha256": c58_source["row_sha256"],
                        "prior_C58_handoff_object_sha256":
                            c58_source["collision2_handoff"]["handoff_object_sha256"],
                        "collision1_history_row_sha256":
                            source["continuation"]["collision1_history_row_sha256"],
                        "collision1_original_owner": source["continuation"]["collision1_original_owner"],
                        "collision1_event_order": source["continuation"]["collision1_event_order"],
                        "exact_representative_box": exact_box,
                        "exact_reflected_box": reflected_box,
                        "route_classification": route["classification"],
                        "route_witness": route["witness"],
                        "route_method": route["route_method"],
                        "continuation_credit": 0,
                    }
                    continuation["continuation_object_sha256"] = digest(continuation)
                final.append(writer.write({
                    "schema": SCHEMA + ".shard-leaf-row", "shard_id": shard,
                    "assignment_preimage_sha256": preimage_sha,
                    "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
                    "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
                    "source_C58_leaf_row_sha256": c58_source["row_sha256"],
                    "source_handoff_ordinal": source["source_handoff_ordinal"],
                    "C58_source_path": source["source_path"], "source_path": source["path"],
                    "path": path, "additional_depth_from_C61": depth,
                    "nominal_additional_depth_from_C58":
                        source["additional_depth_from_C58"] + depth,
                    "pair_index": source["pair_index"], "parent_volume_fraction": str(volume),
                    "exact_representative_box": exact_box, "exact_reflected_box": reflected_box,
                    "route_classification": route["classification"], "route_witness": route["witness"],
                    "route_method": route["route_method"], "disposition": disposition,
                    "continuation": continuation,
                    "local_terminal_credit": 1 if disposition == "STRICT_TERMINAL" else 0,
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
                "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
                "source_output_row_count": len(final),
                "source_output_row_hash_line_sequence_sha256": hashlib.sha256(
                    "".join(row["row_sha256"] + "\n" for row in final).encode("ascii")).hexdigest(),
                "source_Kraft_conservation": source["parent_volume_fraction"],
                "source_prefix_free": True,
            })
    receipt: dict[str, Any] = {
        "schema": SCHEMA + ".shard-receipt",
        "status": "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT",
        "runner_file_sha256": file_sha(SELF),
        "shard_id": shard, "shard_count": SHARD_COUNT,
        "additional_binary_depth": ADDITIONAL_DEPTH,
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
    exclusive_json(receipt_path, receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--contract-check", action="store_true")
    group.add_argument("--inventory", action="store_true")
    group.add_argument("--shard", type=int)
    args = parser.parse_args()
    try:
        if args.contract_check:
            value = contract_check()
        elif args.inventory:
            value = make_inventory()
        else:
            value = run_shard(args.shard)
        print(json.dumps({"status": value["status"],
                          "object_sha256": value.get("object_sha256")},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, TypeError, ValueError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
