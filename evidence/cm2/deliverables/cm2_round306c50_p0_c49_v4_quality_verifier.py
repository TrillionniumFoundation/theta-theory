#!/usr/bin/env python3
"""Read-only C49 v4 quality and evidence-boundary verifier.

This program deliberately does not import any C49 producer.  It verifies
source bytes, companion hashes, AST-level implementation boundaries, the v3
supersession record, the v4 split/runtime checks, and the canonical-status
boundary.  It is not a numeric implementation and cannot satisfy the P0
no-producer-import independent numeric verifier gate.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
DELIVERABLES = SELF.parent

V2 = DELIVERABLES / "cm2_round306c49_d02b_pure_advance_one_collision_v2.py"
V3 = DELIVERABLES / "cm2_round306c49_d02b_pure_advance_one_collision_v3.py"
V4 = DELIVERABLES / "cm2_round306c49_d02b_pure_advance_one_collision_v4.py"
V3_SUPERSESSION = (
    DELIVERABLES
    / "cm2_round306c49_d02b_v2_adversarial_rejection_and_v3_supersession_report.md"
)
CANONICAL = DELIVERABLES / "CM2_LATEST_STATUS.md"

EXPECTED_HASHES = {
    "cm2_round306c49_d02b_pure_advance_one_collision_v2.py":
        "25d87f0ae27b7946ab9f55dbe8a5f50c353eb9f05dd4a6e50810d92e438700df",
    "cm2_round306c49_d02b_pure_advance_one_collision_v3.py":
        "2f603c17f634ac1d5dca9763235f41e7a0259e0b384daa7d7c95cea63704a705",
    "cm2_round306c49_d02b_pure_advance_one_collision_v4.py":
        "80bb67a46ae4f8a10195aa6b1b17f539708eafc83be4b39bc7724624fd64295f",
    "cm2_round306c49_d02b_pure_advance_one_collision_independent_auditor_v2.py":
        "8d9a4beb46d384a69a902549d35ced1f4f584d392343402857d24966b0844ae0",
    "cm2_round306c49_d02b_pure_advance_one_collision_structural_replay_auditor_v3.py":
        "d5328cb30bc7bb9670af745d4d485cf9582b882089352c0ca47b14fdb3af30e0",
    "cm2_round306c49_d02b_pure_advance_one_collision_verification_v2.json":
        "711e41740329800f53a22c5b48f1f2f880ba92f6c44a6a7bf18f6ddba6160615",
    "cm2_round306c49_d02b_pure_advance_one_collision_structural_replay_verification_v3.json":
        "c02066ea6fc6459e50cd21e174d594b31a79722e5cecc967399317cf410902d8",
    "cm2_round306c49_d02b_pure_advance_one_collision_report_v2.md":
        "8b4859d2d863e7117c93e5857375800c00fb993fe595d8b561aae3b783802f07",
    "cm2_round306c49_d02b_pure_advance_one_collision_report_v3.md":
        "4176ba5ab06198efeeb66de1b65159f4e67e50de430fbd9920f2623dbc4ab9a9",
    "cm2_round306c49_d02b_v2_adversarial_rejection_and_v3_supersession_report.md":
        "34683da958bcc6b6ef43de233bdd0eaf8f536d8286d635aa27beb1b0b804ac22",
    "CM2_LATEST_STATUS.md":
        "c4d77168b85070ab20c20d64c26d0c0cfcf0b9e3d0ef0acd2fad3006d08e9be9",
}

COMPANION_FILES = (
    "cm2_round306c49_d02b_pure_advance_one_collision_v2.py",
    "cm2_round306c49_d02b_pure_advance_one_collision_v3.py",
    "cm2_round306c49_d02b_pure_advance_one_collision_independent_auditor_v2.py",
    "cm2_round306c49_d02b_pure_advance_one_collision_structural_replay_auditor_v3.py",
    "cm2_round306c49_d02b_pure_advance_one_collision_verification_v2.json",
    "cm2_round306c49_d02b_pure_advance_one_collision_structural_replay_verification_v3.json",
    "cm2_round306c49_d02b_pure_advance_one_collision_report_v2.md",
    "cm2_round306c49_d02b_pure_advance_one_collision_report_v3.md",
    "cm2_round306c49_d02b_v2_adversarial_rejection_and_v3_supersession_report.md",
)

REQUIRED_V4_DEPENDENCY_CALLS = (
    "v3.local_numeric_context",
    "v3.numeric_step",
    "v3.simple_numeric_inputs",
    "v2.sensitivity_split",
    "v2.split_box",
    "v2.atlas_box",
    "v2.public_box",
)

RECORDED_EXECUTIONS = {
    "producer_self_test": {
        "repeat_count": 2,
        "status": "PASS_15_OF_15_EXECUTED_TESTS",
        "object_sha256":
            "d11ae806d90053a939133c8e1c1fb52580cfcb82c05c2a3a5456110ea8ff0762",
        "review_run_elapsed": "0:02:04.68",
        "review_run_maxrss_kb": 664848,
    },
    "pair9_full_regression": {
        "repeat_count": 2,
        "status": "PASS_PAIR9_COLLISION_3_4_5_ZERO_CREDIT",
        "object_sha256":
            "9a39a43907651235a216977a097615aad098be10989617088a6295043857fb17",
        "review_run_elapsed": "0:03:03.58",
        "review_run_maxrss_kb": 1616940,
        "collision_indices": [3, 4, 5],
        "prior_numeric_replay": True,
        "split_decision_replay": True,
    },
    "post_patch_directed_checks": {
        "selected_child_bit_outside_enum_rejected": True,
        "selected_child_bit_reason":
            "v4 current refinement split 0 selected child bit enum",
        "non_384_bit_runtime_rejected": True,
        "runtime_reason": "v4 Arb runtime pin",
    },
}


class VerificationError(RuntimeError):
    """A read-only quality assertion failed."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise VerificationError(label)


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
    need("object_sha256" not in answer, "object hash absent before close")
    answer["object_sha256"] = digest(answer)
    return answer


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return None if parent is None else parent + "." + node.attr
    return None


def function(tree: ast.Module, name: str) -> ast.FunctionDef:
    rows = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    need(len(rows) == 1, "exact function: " + name)
    return rows[0]


def function_calls(node: ast.AST) -> set[str]:
    return {
        name
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
        and (name := dotted_name(child.func)) is not None
    }


def imports(tree: ast.Module) -> set[str]:
    rows: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            rows.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            rows.add(node.module)
    return rows


def has_selected_child_enum_check(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if not isinstance(child, ast.Compare) or len(child.ops) != 1:
            continue
        if not isinstance(child.ops[0], ast.In) or len(child.comparators) != 1:
            continue
        left = child.left
        if not (
            isinstance(left, ast.Subscript)
            and isinstance(left.slice, ast.Constant)
            and left.slice.value == "selected_child_bit"
        ):
            continue
        comparator = child.comparators[0]
        if isinstance(comparator, (ast.Set, ast.Tuple, ast.List)):
            values = {
                element.value
                for element in comparator.elts
                if isinstance(element, ast.Constant)
            }
            if values == {"0", "1"}:
                return True
    return False


def companion_check(filename: str) -> dict[str, Any]:
    target = DELIVERABLES / filename
    companion = DELIVERABLES / (filename + ".sha256")
    need(target.is_file() and companion.is_file(), "companion files: " + filename)
    tokens = companion.read_text(encoding="ascii").strip().split()
    need(len(tokens) == 2, "companion syntax: " + filename)
    observed = file_sha(target)
    expected = EXPECTED_HASHES[filename]
    need(tokens == [expected, filename], "companion content: " + filename)
    need(observed == expected, "companion digest: " + filename)
    return {"filename": filename, "sha256": observed, "status": "OK"}


def verify() -> dict[str, Any]:
    observed_hashes = {
        filename: file_sha(DELIVERABLES / filename)
        for filename in EXPECTED_HASHES
    }
    need(observed_hashes == EXPECTED_HASHES, "all pinned source/evidence bytes")

    companion_results = [companion_check(name) for name in COMPANION_FILES]
    canonical_tokens = (
        DELIVERABLES / "CM2_LATEST_STATUS.sha256"
    ).read_text(encoding="ascii").strip().split()
    need(canonical_tokens == [
        EXPECTED_HASHES["CM2_LATEST_STATUS.md"], "CM2_LATEST_STATUS.md"
    ], "canonical companion content")

    v3_report = V3_SUPERSESSION.read_text(encoding="utf-8")
    need("V2 REJECTED AS PURE/FAIL-CLOSED" in v3_report, "v2 rejection record")
    need("V3 SUPERSEDES V2 FOR DIAGNOSTIC USE" in v3_report,
         "v3 supersession record")
    need("ZERO FORMAL CREDIT" in v3_report, "v3 zero-credit record")

    v4_source = V4.read_text(encoding="utf-8")
    v4_tree = ast.parse(v4_source, filename=str(V4))
    v4_imports = imports(v4_tree)
    producer_imports = sorted(
        name for name in v4_imports
        if name.startswith("cm2_round306c49_d02b_pure_advance_one_collision_v")
    )
    need(producer_imports == [
        "cm2_round306c49_d02b_pure_advance_one_collision_v2",
        "cm2_round306c49_d02b_pure_advance_one_collision_v3",
    ], "v4 direct producer dependencies")
    calls = {
        name
        for node in ast.walk(v4_tree)
        if isinstance(node, ast.Call)
        and (name := dotted_name(node.func)) is not None
    }
    dependency_calls = sorted(set(REQUIRED_V4_DEPENDENCY_CALLS) & calls)
    need(dependency_calls == sorted(REQUIRED_V4_DEPENDENCY_CALLS),
         "v4 reused numeric/box implementation calls")

    split_verifier = function(v4_tree, "verify_split_chain")
    need(has_selected_child_enum_check(split_verifier),
         "selected child bit exact enum validation")
    split_calls = function_calls(split_verifier)
    need({"numeric_step", "numeric_split_decision", "v2.split_box"} <= split_calls,
         "split numeric decision replay calls")

    runtime_pin = function(v4_tree, "verify_numeric_authority_pins")
    runtime_text = ast.get_source_segment(v4_source, runtime_pin) or ""
    need("flint.__version__" in runtime_text and "ctx.prec == 384" in runtime_text,
         "runtime/version/precision pin")
    for public_name in ("advance_one_collision", "adaptive_advance"):
        need("verify_numeric_authority_pins" in function_calls(
            function(v4_tree, public_name)
        ), "public runtime pin: " + public_name)

    self_tree = ast.parse(SELF.read_text(encoding="utf-8"), filename=str(SELF))
    verifier_producer_imports = sorted(
        name for name in imports(self_tree) if name.startswith("cm2_")
    )
    need(not verifier_producer_imports, "quality verifier imports no producer")

    canonical_text = CANONICAL.read_text(encoding="utf-8")
    timestamp_match = re.search(r"As of: `([^`]+)`", canonical_text)
    need(timestamp_match is not None, "canonical timestamp")
    canonical_mentions_c49 = bool(re.search(r"(?:306c49|\bC49\b)", canonical_text,
                                             flags=re.IGNORECASE))
    need(not canonical_mentions_c49, "canonical excludes uninstalled C49")

    v4_adjacent_release_files = sorted(
        path.name for path in DELIVERABLES.glob(
            "cm2_round306c49_d02b_pure_advance_one_collision_*v4*"
        )
        if path != V4
    )
    need(not v4_adjacent_release_files, "no pre-existing v4 release companions")

    result = {
        "schema": "cm2.round306c50.p0.c49-v4-quality-review.v1",
        "status": "PASS_READ_ONLY_QUALITY_REVIEW_WITH_BLOCKING_INDEPENDENCE_GAP",
        "review_scope": "STATIC_FILE_AND_RECORDED_RUNTIME_BEHAVIOR",
        "v4_source_sha256": observed_hashes[V4.name],
        "p0_source_byte_pin_recorded": True,
        "standalone_c49_v4_release_bundle_present": False,
        "v4_adjacent_release_files": v4_adjacent_release_files,
        "v2_rejection_record_present": True,
        "v3_diagnostic_supersession_record_present": True,
        "legacy_companion_checks": companion_results,
        "file_consistency": {
            "current_v4_source_matches_p0_pin": True,
            "legacy_companion_count": len(companion_results),
            "legacy_companions_all_ok": True,
            "canonical_companion_ok": True,
            "concurrent_replacement_or_short_read_matrix_executed": False,
            "filesystem_fault_suite_present": False,
            "classification":
                "HASH_CONSISTENCY_PASS_EXTENDED_FILE_FAULT_MATRIX_NOT_RUN",
        },
        "canonical": {
            "sha256": observed_hashes[CANONICAL.name],
            "companion_ok": True,
            "as_of": timestamp_match.group(1),
            "mentions_C49_or_v4": canonical_mentions_c49,
            "touched_by_review": False,
        },
        "v4_implementation_boundary": {
            "direct_producer_imports": producer_imports,
            "reused_numeric_and_box_calls": dependency_calls,
            "producer_import_free": False,
            "independent_numeric_implementation": False,
            "classification": "NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION",
        },
        "split_replay": {
            "numeric_parent_and_decision_replay_present": True,
            "selected_child_bit_enum_check_present": True,
            "post_patch_directed_rejection_passed": True,
        },
        "public_runtime_pin": {
            "version_and_384_bit_check_present": True,
            "advance_one_collision_checked": True,
            "adaptive_advance_checked": True,
            "post_patch_directed_rejection_passed": True,
        },
        "recorded_executions": copy.deepcopy(RECORDED_EXECUTIONS),
        "pre_patch_observations_retained": {
            "superseded_source_sha256":
                "c4457b66dc1fdf05848011db2e5eb5369a2f90cb57b5b3b2fb99f5026b8bf860",
            "non_enum_child_bit_was_accepted_object_sha256":
                "f1d0cf6e29513cdda5ca7ca8e7874bebec0526baab826b37794d609490611644",
            "384_bit_object_sha256":
                "6ceacf1d5eb7d2cca4b169a4a40466a9b5e919602c96eb955b4debbc27340d1d",
            "128_bit_object_sha256":
                "545361becf0fb89e8dae17393895ede431a814bee47778bd2386fdb06c10eae7",
            "disposition": "SUPERSEDED_PRE_PATCH_QUALITY_EVIDENCE_ONLY",
        },
        "quality_verifier_imports_producer": False,
        "quality_verifier_is_numeric_implementation": False,
        "quality_verifier_classification": "NOT_INDEPENDENT_NUMERIC_IMPLEMENTATION",
        "P0_no_producer_import_independent_numeric_verifier_gate":
            "FAIL_NOT_IMPLEMENTED",
        "missing_global_oracles": [
            "GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE",
            "GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE",
        ],
        "formal_credit": 0,
        "D02_credit": 0,
        "authority_pointer_touched": False,
        "canonical_status_touched": False,
        "writes_performed": False,
    }
    return close_object(result)


def main() -> int:
    try:
        result = verify()
    except (VerificationError, OSError, UnicodeError, SyntaxError, ValueError,
            KeyError) as exc:
        result = close_object({
            "schema": "cm2.round306c50.p0.c49-v4-quality-review.v1.rejection",
            "status": "REJECTED_READ_ONLY_QUALITY_REVIEW",
            "reason": str(exc),
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
