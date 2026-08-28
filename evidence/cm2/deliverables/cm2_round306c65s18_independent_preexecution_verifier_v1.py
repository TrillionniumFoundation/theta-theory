#!/usr/bin/env python3
"""Independent, no-import verifier for the frozen C65s18 contract/assignment.

The C65 runner is consumed only as pinned inert bytes and parsed as AST.  This
program does not import or execute it and performs no runtime/canonical writes.
"""

from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import json
from pathlib import Path
import stat
from typing import Any, Callable


SELF = Path(__file__).resolve()
OUT = SELF.parent
BASE = "cm2_round306c65s18_depth18_64shard"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v1.json"
RUNNER = OUT / (BASE + "_runner_v1.py")
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C61_MANIFEST = OUT / "cm2_round306c61s12_depth12_16shard_manifest_v4.sha256"
C61_VERIFY = OUT / "cm2_round306c61s12_independent_postexecution_verification_v4.json"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
ASSIGNMENT = OUT / (BASE + "_assignment_result_v1.json")
INVENTORY = OUT / (BASE + "_assignment_inventory_v1.jsonl.gz")
VERIFY_OUT = OUT / "cm2_round306c65s18_independent_preexecution_verification_v1.json"
SELFTEST_OUT = OUT / "cm2_round306c65s18_independent_preexecution_self_test_v1.json"

PIN = {
    "contract_file": "466fd81803ac0aa2237ba2d021b96ccc4f71bde8d1e3fb850af7f5ddc752edd2",
    "contract_object": "4fce42b17d7d711512f22edf65549795f3b641689f1a7cb6fb168ae3a526c736",
    "runner_file": "d9e8dd6e2e9da54f770f69600d83f2a6ec2b6d748e8ab2e58a359dc39fe9bd7d",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_manifest_file": "4c18c510367fc15b801fb6eff7901ad94a8fd53e47a6b7868ee876b554393545",
    "C61_verify_file": "2dc773d0051cc9668cdf7752fb61ac09f495044f566972faa335fffc509e9fc7",
    "C61_verify_object": "066e03be0c41600f5fb5cc2c157fe6e7eb04d1060896dd1acc910b06aab30b24",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "assignment_file": "61ae974ac84a8c59a80e304fdb9a1b281534b6a74d41bfe38028a5ee4bb3a3f1",
    "assignment_object": "bc460d484a75627485148fbc92a5e1466814e7b8c3e6a2df60fe138b0ba1da73",
    "inventory_file": "53f47406f31b8a3ef72fad25fda1e0eb4b4b29c47ca76d3db641ff29893c7b5a",
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


def snapshot(path: Path) -> tuple[int, int, int, int, int, int]:
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and not path.is_symlink(),
         "regular non-symlink single-link input:" + path.name)
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns)


def strict_loads(raw: bytes) -> Any:
    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate JSON key:" + key)
            answer[key] = value
        return answer
    return json.loads(raw, object_pairs_hook=hook)


def read_regular(path: Path, pin: str) -> bytes:
    before = snapshot(path)
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin, "file pin:" + path.name)
    need(snapshot(path) == before, "TOCTOU file:" + path.name)
    return raw


def validate_object(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    value = strict_loads(read_regular(path, file_pin))
    need(type(value) is dict, "JSON object:" + path.name)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object closure:" + path.name)
    return value


def rows(path: Path, descriptor: dict[str, Any], pin: str) -> list[dict[str, Any]]:
    raw = read_regular(path, pin)
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.GzipFile(fileobj=__import__("io").BytesIO(raw), mode="rb") as stream:
        for line in stream:
            row = strict_loads(line)
            need(type(row) is dict, "ledger row object:" + path.name)
            body = copy.deepcopy(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
            sequence.update((claim + "\n").encode("ascii"))
            answer.append(row)
    need(len(answer) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    return answer


def preimage(row_sha: str, pair_index: int, path: str) -> bytes:
    need(type(row_sha) is str and len(row_sha) == 64 and
         set(row_sha) <= set("0123456789abcdef"), "assignment row SHA")
    need(type(pair_index) is int and pair_index >= 0, "assignment pair")
    need(type(path) is str and bool(path) and set(path) <= {"0", "1"}, "assignment path")
    return canonical({"C61_aggregate_leaf_row_sha256": row_sha,
                      "pair_index": pair_index, "path": path})


def shard_claim(row_sha: str, pair_index: int, path: str) -> tuple[int, str]:
    claim = hashlib.sha256(preimage(row_sha, pair_index, path)).hexdigest()
    return int(claim, 16) % 64, claim


def ast_audit(raw: bytes) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8"), filename=RUNNER.name)
    constants: dict[str, Any] = {}
    forbidden = {"unlink", "rename", "replace", "rmdir", "removedirs", "rmtree",
                 "system", "popen", "run", "Popen", "check_call", "check_output"}
    seen_forbidden: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                constants[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
        if isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else (
                node.func.id if isinstance(node.func, ast.Name) else "")
            if name in forbidden:
                seen_forbidden.append(name)
    need(constants.get("SHARD_COUNT") == 64 and constants.get("ADDITIONAL_DEPTH") == 6,
         "runner AST shard/depth constants")
    need(constants.get("BASE") == BASE, "runner AST base")
    need(not seen_forbidden, "runner AST destructive/process calls:" + repr(seen_forbidden))
    return {"parsed": True, "shard_count": 64, "additional_depth": 6,
            "forbidden_destructive_or_process_calls": seen_forbidden}


def verify() -> dict[str, Any]:
    contract = validate_object(CONTRACT, PIN["contract_file"], PIN["contract_object"])
    runner_raw = read_regular(RUNNER, PIN["runner_file"])
    runner_ast = ast_audit(runner_raw)
    need(contract["assignment"]["source_input_count"] == 20879 and
         contract["assignment"]["modulus"] == 64 and
         contract["assignment"]["shard_ids_exactly"] == list(range(64)) and
         contract["assignment"]["shard_id_formula"] == "int(SHA256(preimage),16)%64",
         "contract assignment boundary")
    need(contract["refinement"]["additional_binary_depth"] == 6 and
         contract["formal_credit"] == contract["whole_parent_credit"] ==
         contract["D02_gate_credit"] == 0, "contract refinement/credit boundary")

    c61_result = validate_object(C61_RESULT, PIN["C61_result_file"], PIN["C61_result_object"])
    read_regular(C61_MANIFEST, PIN["C61_manifest_file"])
    c61_verify = validate_object(C61_VERIFY, PIN["C61_verify_file"], PIN["C61_verify_object"])
    need(c61_verify["status"].startswith("PASS_INDEPENDENT_V4_ONLY_COMPLETE_16_SHARD_AGGREGATE"),
         "C61 audit status")
    c61_rows = rows(C61_LEAVES, c61_result["ledgers"]["aggregate_leaves"], PIN["C61_leaf_file"])
    selected = [row for row in c61_rows if row["disposition"] == "COLLISION2_HANDOFF"]
    need(len(selected) == 20879 and len({row["row_sha256"] for row in selected}) == 20879,
         "exact unique C61 residual set")
    need(all(row["continuation"]["next_collision_index"] == 2 for row in selected),
         "C61 C2 continuation index")

    c58_result = validate_object(C58_RESULT, PIN["C58_result_file"], PIN["C58_result_object"])
    c58_rows = rows(C58_LEAVES, c58_result["ledgers"]["leaves"], PIN["C58_leaf_file"])
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_by_hash) == len(c58_rows), "unique C58 identities")

    assignment = validate_object(ASSIGNMENT, PIN["assignment_file"], PIN["assignment_object"])
    need(assignment["runner_file_sha256"] == PIN["runner_file"] and
         assignment["independent_contract"]["object_sha256"] == PIN["contract_object"],
         "assignment contract/runner binding")
    inventory = rows(INVENTORY, assignment["inventory"], PIN["inventory_file"])
    need(len(inventory) == len(selected) == 20879, "assignment inventory count")
    counts = [0] * 64
    ordered_claims = hashlib.sha256()
    inventory_keys: set[tuple[str, int, str]] = set()
    for source, assigned in zip(selected, inventory, strict=True):
        source_sha = source["row_sha256"]
        pair = source["pair_index"]
        path = source["path"]
        expected_shard, claim = shard_claim(source_sha, pair, path)
        key = (source_sha, pair, path)
        need(key not in inventory_keys, "duplicate assignment key")
        inventory_keys.add(key)
        need(assigned["C61_aggregate_leaf_row_sha256"] == source_sha and
             assigned["pair_index"] == pair and assigned["path"] == path and
             assigned["C61_source_shard_row_sha256"] == source["source_shard_row_sha256"] and
             assigned["C61_continuation_object_sha256"] ==
             source["continuation"]["continuation_object_sha256"] and
             assigned["source_C58_leaf_row_sha256"] == source["source_C58_leaf_row_sha256"] and
             assigned["assignment_preimage_sha256"] == claim and
             assigned["shard_id"] == expected_shard,
             "exact assignment row replay")
        need(assigned["assignment_credit"] == assigned["formal_credit"] ==
             assigned["whole_parent_credit"] == assigned["D02_gate_credit"] == 0,
             "assignment row zero credit")
        c58 = c58_by_hash[source["source_C58_leaf_row_sha256"]]
        need(c58["disposition"] == "COLLISION2_HANDOFF" and
             c58["source_handoff_ordinal"] == source["source_handoff_ordinal"] and
             c58["path"] == source["source_path"] and path.startswith(c58["path"]) and
             c58["pair_index"] == pair and
             source["continuation"]["prior_C58_leaf_row_sha256"] == c58["row_sha256"] and
             source["continuation"]["prior_C58_handoff_object_sha256"] ==
             c58["collision2_handoff"]["handoff_object_sha256"],
             "exact C61/C58 lineage")
        counts[expected_shard] += 1
        ordered_claims.update((claim + "\n").encode("ascii"))
    need(len(inventory_keys) == 20879 and all(counts) and sum(counts) == 20879,
         "complete mutually exclusive nonempty assignment")
    need(assignment["per_shard_input_counts"] ==
         {str(index): value for index, value in enumerate(counts)} and
         assignment["ordered_preimage_sha256_line_sequence_sha256"] ==
         ordered_claims.hexdigest() and assignment["assignment_complete"] is True and
         assignment["assignment_mutually_exclusive"] is True,
         "assignment aggregate replay")
    need(assignment["formal_credit"] == assignment["whole_parent_credit"] ==
         assignment["D02_gate_credit"] == 0 and
         assignment["runtime_canonical_pointer_or_seal_writes"] is False,
         "assignment zero-credit/no-runtime boundary")

    value: dict[str, Any] = {
        "schema": "cm2.round306c65s18.independent-preexecution-verifier.v1.verification",
        "status": "PASS_INDEPENDENT_NO_RUNNER_IMPORT__FROZEN_CONTRACT_AND_20879_TO_64_ASSIGNMENT__ZERO_CREDIT",
        "contract": {"file_sha256": PIN["contract_file"],
                     "object_sha256": PIN["contract_object"]},
        "runner": {"file_sha256": PIN["runner_file"], "consumed_as_inert_bytes": True,
                   "imported": False, "executed": False, "AST_audit": runner_ast},
        "source": {"C61_result_object_sha256": PIN["C61_result_object"],
                   "C61_leaf_ledger_sha256": PIN["C61_leaf_file"],
                   "C61_verification_object_sha256": PIN["C61_verify_object"],
                   "C58_result_object_sha256": PIN["C58_result_object"],
                   "C58_leaf_ledger_sha256": PIN["C58_leaf_file"]},
        "assignment": {"result_file_sha256": PIN["assignment_file"],
                       "result_object_sha256": PIN["assignment_object"],
                       "inventory_sha256": PIN["inventory_file"],
                       "input_count": 20879, "shard_count": 64,
                       "per_shard_input_counts": {str(i): n for i, n in enumerate(counts)},
                       "minimum_shard_input_count": min(counts),
                       "maximum_shard_input_count": max(counts),
                       "complete": True, "mutually_exclusive": True,
                       "stable_source_identity_and_path_bound": True},
        "partial_shards_are_an_aggregate": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    return value


def expect_fail(label: str, action: Callable[[], Any], results: list[dict[str, Any]]) -> None:
    try:
        action()
    except (FailClosed, ValueError, TypeError):
        results.append({"name": label, "status": "PASS_FAIL_CLOSED"})
        return
    raise FailClosed("hostile test accepted:" + label)


def self_test() -> dict[str, Any]:
    baseline = verify()
    results: list[dict[str, Any]] = []

    def passed(name: str, condition: bool) -> None:
        need(condition, "self-test:" + name)
        results.append({"name": name, "status": "PASS"})

    sample_sha = "0" * 64
    sample = preimage(sample_sha, 31, "0101")
    passed("canonical_exact_bytes", sample ==
           b'{"C61_aggregate_leaf_row_sha256":"0000000000000000000000000000000000000000000000000000000000000000","pair_index":31,"path":"0101"}')
    passed("canonical_no_newline", not sample.endswith(b"\n"))
    passed("canonical_utf8", sample.decode("utf-8").startswith("{"))
    passed("canonical_sorted_keys", sample.index(b"C61_") < sample.index(b"pair_index") < sample.index(b"path"))
    passed("assignment_deterministic", shard_claim(sample_sha, 31, "0101") ==
           shard_claim(sample_sha, 31, "0101"))
    passed("row_identity_changes_claim", shard_claim("1" + "0" * 63, 31, "0101")[1] !=
           shard_claim(sample_sha, 31, "0101")[1])
    passed("pair_changes_claim", shard_claim(sample_sha, 32, "0101")[1] !=
           shard_claim(sample_sha, 31, "0101")[1])
    passed("path_changes_claim", shard_claim(sample_sha, 31, "0100")[1] !=
           shard_claim(sample_sha, 31, "0101")[1])
    passed("shard_range", 0 <= shard_claim(sample_sha, 31, "0101")[0] < 64)
    expect_fail("uppercase_row_sha", lambda: preimage("A" * 64, 31, "0"), results)
    expect_fail("short_row_sha", lambda: preimage("0" * 63, 31, "0"), results)
    expect_fail("negative_pair", lambda: preimage(sample_sha, -1, "0"), results)
    expect_fail("boolean_pair", lambda: preimage(sample_sha, True, "0"), results)
    expect_fail("empty_path", lambda: preimage(sample_sha, 31, ""), results)
    expect_fail("nonbinary_path", lambda: preimage(sample_sha, 31, "012"), results)
    expect_fail("duplicate_json_key", lambda: strict_loads(b'{"a":1,"a":2}'), results)
    passed("baseline_object_closes", baseline["object_sha256"] ==
           digest({k: v for k, v in baseline.items() if k != "object_sha256"}))
    passed("source_count", baseline["assignment"]["input_count"] == 20879)
    passed("shard_count", baseline["assignment"]["shard_count"] == 64)
    passed("minimum_count", baseline["assignment"]["minimum_shard_input_count"] == 284)
    passed("maximum_count", baseline["assignment"]["maximum_shard_input_count"] == 357)
    passed("count_sum", sum(baseline["assignment"]["per_shard_input_counts"].values()) == 20879)
    passed("all_shards_nonempty", all(baseline["assignment"]["per_shard_input_counts"].values()))
    passed("assignment_complete", baseline["assignment"]["complete"] is True)
    passed("assignment_mutually_exclusive", baseline["assignment"]["mutually_exclusive"] is True)
    passed("stable_identity_path_bound", baseline["assignment"]["stable_source_identity_and_path_bound"] is True)
    passed("runner_not_imported", baseline["runner"]["imported"] is False)
    passed("runner_not_executed", baseline["runner"]["executed"] is False)
    passed("runner_AST_parsed", baseline["runner"]["AST_audit"]["parsed"] is True)
    passed("runner_no_forbidden_calls", not baseline["runner"]["AST_audit"]["forbidden_destructive_or_process_calls"])
    passed("partial_not_aggregate", baseline["partial_shards_are_an_aggregate"] is False)
    passed("formal_credit_zero", baseline["formal_credit"] == 0)
    passed("whole_parent_credit_zero", baseline["whole_parent_credit"] == 0)
    passed("D02_gate_credit_zero", baseline["D02_gate_credit"] == 0)
    passed("no_runtime_writes", baseline["runtime_canonical_pointer_or_seal_writes"] is False)
    passed("contract_pin", baseline["contract"]["object_sha256"] == PIN["contract_object"])
    passed("runner_pin", baseline["runner"]["file_sha256"] == PIN["runner_file"])
    passed("assignment_pin", baseline["assignment"]["result_object_sha256"] == PIN["assignment_object"])
    passed("C61_audit_pin", baseline["source"]["C61_verification_object_sha256"] == PIN["C61_verify_object"])
    passed("C58_source_pin", baseline["source"]["C58_result_object_sha256"] == PIN["C58_result_object"])
    need(len(results) == 40, "exactly 40 self-tests")
    value: dict[str, Any] = {
        "schema": "cm2.round306c65s18.independent-preexecution-verifier.v1.self-test",
        "status": "PASS_40_OF_40_HOSTILE_AND_INVARIANT_TESTS",
        "verification_object_sha256": baseline["object_sha256"],
        "tests": results, "passed": 40, "failed": 0,
        "runner_imported": False, "runner_executed": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    }
    value["object_sha256"] = digest(value)
    return value


def publish(path: Path, value: dict[str, Any]) -> None:
    need(not path.exists() and not path.is_symlink(), "no-replace:" + path.name)
    path.write_bytes(canonical(value) + b"\n")
    snapshot(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        target = VERIFY_OUT if args.verify else SELFTEST_OUT
        publish(target, value)
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (FailClosed, KeyError, TypeError, ValueError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
