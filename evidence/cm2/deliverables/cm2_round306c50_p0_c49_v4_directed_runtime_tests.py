#!/usr/bin/env python3
"""Directed runtime quality checks for the exact patched C49 v4 source.

This test imports and executes v4.  It is same-implementation behavioral
evidence, not a no-producer-import independent numeric implementation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent
if str(DELIVERABLES) not in sys.path:
    sys.path.insert(0, str(DELIVERABLES))

from flint import ctx
import cm2_round306c49_d02b_pure_advance_one_collision_v4 as producer


EXPECTED_V4_SHA256 = (
    "80bb67a46ae4f8a10195aa6b1b17f539708eafc83be4b39bc7724624fd64295f"
)


class TestFailure(RuntimeError):
    """A directed quality expectation failed."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise TestFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "hash absent before close")
    answer["object_sha256"] = digest(answer)
    return answer


def rejected(action: Callable[[], Any]) -> dict[str, Any]:
    try:
        action()
    except producer.Rejected as exc:
        return {"rejected": True, "exception": type(exc).__name__, "reason": str(exc)}
    return {"rejected": False, "exception": None, "reason": None}


def run_directed() -> dict[str, Any]:
    source_sha = file_sha(Path(producer.__file__).absolute())
    need(source_sha == EXPECTED_V4_SHA256, "exact patched v4 source")
    _source, inputs = producer.pair9_inputs()
    original, history = copy.deepcopy(inputs[0])
    tree = producer.adaptive_advance(original, history, 1, 16)
    right = next(
        row for row in tree["leaves"]
        if row["adaptive_suffix"].endswith("1")
    )
    forged = copy.deepcopy(right["step"]["original_box"])
    split_row = forged["refinement_decision_chain"][-1]
    split_row.pop("object_sha256")
    split_row["selected_child_bit"] = "NOT_A_BIT"
    split_row["object_sha256"] = producer.digest(split_row)
    child_bit_result = rejected(
        lambda: producer.advance_one_collision(forged, history)
    )
    need(child_bit_result == {
        "rejected": True,
        "exception": "Rejected",
        "reason": "v4 current refinement split 0 selected child bit enum",
    }, "selected child bit directed rejection")

    prior_precision = ctx.prec
    try:
        ctx.prec = 128
        precision_result = rejected(
            lambda: producer.advance_one_collision(original, history)
        )
    finally:
        ctx.prec = prior_precision
    need(precision_result == {
        "rejected": True,
        "exception": "Rejected",
        "reason": "v4 Arb runtime pin",
    }, "runtime precision directed rejection")

    return close_object({
        "schema": "cm2.round306c50.p0.c49-v4-directed-runtime-tests.v1",
        "status": "PASS_2_OF_2_DIRECTED_RUNTIME_QUALITY_CHECKS",
        "v4_source_sha256": source_sha,
        "selected_child_bit_check": child_bit_result,
        "runtime_precision_check": precision_result,
        "producer_imported": True,
        "independent_numeric_implementation": False,
        "classification": "NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION",
        "formal_credit": 0,
        "D02_credit": 0,
        "writes_performed": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-self-test", action="store_true")
    parser.add_argument("--include-regression", action="store_true")
    args = parser.parse_args()
    try:
        result = run_directed()
        if args.include_self_test:
            value = producer.self_test()
            result["producer_self_test"] = {
                "status": value["status"],
                "object_sha256": value["object_sha256"],
            }
        if args.include_regression:
            value = producer.build_regression()
            result["pair9_full_regression"] = {
                "status": value["status"],
                "object_sha256": value["object_sha256"],
                "collision_indices_observed": value["collision_indices_observed"],
                "prior_numeric_replay":
                    value["every_prior_step_full_numeric_body_replayed"],
                "split_decision_replay":
                    value["every_split_decision_preimage_replayed"],
                "formal_credit": value["formal_credit"],
                "D02_credit": value["D02_credit"],
            }
        if args.include_self_test or args.include_regression:
            result.pop("object_sha256")
            result = close_object(result)
    except (TestFailure, producer.Rejected, RuntimeError, OSError, ValueError,
            KeyError, StopIteration) as exc:
        result = close_object({
            "schema": "cm2.round306c50.p0.c49-v4-directed-runtime-tests.v1.rejection",
            "status": "REJECTED_DIRECTED_RUNTIME_QUALITY_CHECKS",
            "reason": str(exc),
            "producer_imported": True,
            "independent_numeric_implementation": False,
            "classification": "NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION",
            "formal_credit": 0,
            "D02_credit": 0,
            "writes_performed": False,
        })
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 2
    sys.stdout.buffer.write(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
