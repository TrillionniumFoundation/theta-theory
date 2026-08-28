#!/usr/bin/env python3
"""Read-only independent attack-census audit for the C79g r11 draft.

This utility deliberately treats the r11 consumer and the older global
consumer harness as inert bytes.  It parses source with :mod:`ast` and
:mod:`tokenize`, but never imports, compiles, executes, or rewrites either
candidate.  The output is a zero-credit diagnostic report on stdout.  In
particular it does not create a manifest, outer receipt, runtime namespace,
``__pycache__`` entry, or authority/credit object.

The r11 consumer's ``make_attack_cases`` factory has three kinds of entries:
literal labels in loops/``extend`` lists, three direct helper calls, and a
dynamic 16-name ``V11_INCIDENT_ATTACK_NAMES`` tuple.  Checker A reconstructs
the factory from the AST; checker B independently scans string tokens in the
factory and inserts the dynamic tuple at its extension site.  Agreement is
reported only when both ordered lists (and their category census) are equal.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tokenize
from typing import Any, Iterable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
R11_CONSUMER = OUT / (
    BASE +
    "_independent_verifier_assembler_authority_consumer_v16r2r11_semantic_source.py"
)
LEGACY_HARNESS = ROOT / "scripts/c79g_v16r2_global_consumer_attack_harness.py"
EXPECTED_COUNT = 137
EXPECTED_PIN = "90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d"

# The factory's literal labels use these families.  Restricting extraction to
# this set avoids counting unrelated historical strings in the same source.
FAMILIES = frozenset({
    "overlay", "successor", "parent", "result", "credit", "authority",
    "publication", "registry", "C78l", "C78s", "gzip", "v11incident",
})

ROUTE_BY_FAMILY = {
    "overlay": "ROW_CLOSURE_THEN_INDEPENDENT_EXACT_RECONSTRUCTION",
    "successor": "ROW_CLOSURE_THEN_INDEPENDENT_EXACT_RECONSTRUCTION",
    "parent": "ROW_CLOSURE_THEN_INDEPENDENT_EXACT_RECONSTRUCTION",
    "result": "CANDIDATE_METADATA_PRODUCTION_VALIDATOR",
    "credit": "CANDIDATE_METADATA_PRODUCTION_VALIDATOR",
    "registry": "CANDIDATE_METADATA_PRODUCTION_VALIDATOR",
    "authority": "PINNED_AUTHORITY_PRODUCTION_SEMANTIC_VALIDATOR",
    "C78l": "PINNED_AUTHORITY_PRODUCTION_SEMANTIC_VALIDATOR",
    "C78s": "PINNED_AUTHORITY_PRODUCTION_SEMANTIC_VALIDATOR",
    "publication": "MANIFEST_OUTER_OBJECT_CHAIN_PRODUCTION_VALIDATOR",
    "gzip": "STRICT_SINGLE_MEMBER_GZIP_PRODUCTION_VALIDATOR",
    "v11incident": "INHERITED_HELD_FD_AND_EXACT_PER_CLAUSE_WITNESS_PRODUCTION_VALIDATOR",
}


class CensusError(RuntimeError):
    """A fail-closed diagnostic error (never an authority decision)."""


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def line_sequence_sha256(values: Iterable[str]) -> str:
    return sha(b"".join((value + "\n").encode("ascii") for value in values))


def stable(path: Path) -> bytes:
    """Read one regular nlink=1 file with a no-follow identity check."""
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise CensusError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise CensusError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise CensusError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def family_label(value: Any) -> bool:
    return (isinstance(value, str) and ":" in value and
            value.split(":", 1)[0] in FAMILIES)


def find_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node  # type: ignore[return-value]
    raise CensusError(f"function not found: {name}")


def v11_names(tree: ast.Module) -> tuple[str, ...]:
    for node in tree.body:
        targets: list[ast.expr]
        value: ast.expr | None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign):
            targets, value = [node.target], node.value
        else:
            continue
        if any(isinstance(target, ast.Name) and
               target.id == "V11_INCIDENT_ATTACK_NAMES" for target in targets):
            if not isinstance(value, (ast.Tuple, ast.List)):
                raise CensusError("V11_INCIDENT_ATTACK_NAMES is not a literal tuple")
            result = tuple(
                element.value for element in value.elts
                if isinstance(element, ast.Constant) and family_label(element.value)
            )
            if len(result) != len(value.elts) or len(set(result)) != len(result):
                raise CensusError("V11 incident tuple is not a unique literal list")
            return result
    raise CensusError("V11_INCIDENT_ATTACK_NAMES assignment not found")


def dynamic_extension_line(factory: ast.FunctionDef) -> int:
    for node in ast.walk(factory):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "extend" and node.args
                and isinstance(node.args[0], ast.List)
                and any(isinstance(element, ast.Tuple) and element.elts and
                        isinstance(element.elts[0], ast.Subscript) and
                        isinstance(element.elts[0].value, ast.Name) and
                        element.elts[0].value.id == "V11_INCIDENT_ATTACK_NAMES"
                        for element in node.args[0].elts)):
            return node.lineno
    raise CensusError("dynamic V11 attack extension not found")


def ast_enumeration(tree: ast.Module) -> list[str]:
    """Checker A: reconstruct labels from AST containers and helper calls."""
    factory = find_function(tree, "make_attack_cases")
    dynamic = v11_names(tree)
    dynamic_line = dynamic_extension_line(factory)
    entries: list[tuple[int, int, int, str]] = []
    serial = 0

    # Literal labels in loop tuples and ``cases.extend([...])`` lists.
    for node in ast.walk(factory):
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple):
            for element in node.iter.elts:
                if (isinstance(element, ast.Tuple) and element.elts and
                        isinstance(element.elts[0], ast.Constant) and
                        family_label(element.elts[0].value)):
                    serial += 1
                    first = element.elts[0]
                    entries.append((first.lineno, first.col_offset, serial,
                                    first.value))
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "extend" and node.args
                and isinstance(node.args[0], ast.List)):
            for element in node.args[0].elts:
                if not (isinstance(element, ast.Tuple) and element.elts):
                    continue
                first = element.elts[0]
                if isinstance(first, ast.Constant) and family_label(first.value):
                    serial += 1
                    entries.append((first.lineno, first.col_offset, serial,
                                    first.value))
                elif (isinstance(first, ast.Subscript) and
                      isinstance(first.value, ast.Name) and
                      first.value.id == "V11_INCIDENT_ATTACK_NAMES" and
                      isinstance(first.slice, ast.Constant) and
                      isinstance(first.slice.value, int)):
                    index = first.slice.value
                    try:
                        label = dynamic[index]
                    except IndexError as exc:
                        raise CensusError("V11 dynamic index out of range") from exc
                    serial += 1
                    # Use the extension call's line so all dynamic entries
                    # sort immediately after the preceding gzip literals.
                    entries.append((dynamic_line, first.col_offset, serial, label))

    # Three direct helper calls are not inside a tuple/list container.
    for node in ast.walk(factory):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in {"row_case", "object_case", "authority_case"}
                and node.args and isinstance(node.args[0], ast.Constant)
                and family_label(node.args[0].value)):
            # Calls used as the body of a loop are already represented by the
            # loop's tuple labels; only a direct Expr call is a new case.
            parent_is_loop = False
            for parent in ast.walk(factory):
                if isinstance(parent, ast.For) and any(
                        child is node for child in ast.walk(parent.body[0])):
                    parent_is_loop = True
                    break
            if parent_is_loop:
                continue
            serial += 1
            first = node.args[0]
            entries.append((first.lineno, first.col_offset, serial,
                            first.value))

    entries.sort(key=lambda row: (row[0], row[1], row[2]))
    labels = [row[3] for row in entries]
    if len(labels) != EXPECTED_COUNT or len(set(labels)) != EXPECTED_COUNT:
        raise CensusError(f"AST enumeration count/uniqueness {len(labels)}/"
                          f"{len(set(labels))}, expected {EXPECTED_COUNT}")
    return labels


def token_enumeration(raw: bytes, tree: ast.Module) -> list[str]:
    """Checker B: scan string tokens in the factory, then expand V11 names."""
    factory = find_function(tree, "make_attack_cases")
    dynamic = v11_names(tree)
    dynamic_line = dynamic_extension_line(factory)
    # ``end_lineno`` exists for every FunctionDef on supported Python 3.
    start, end = factory.lineno, factory.end_lineno or factory.lineno
    text = raw.decode("utf-8")
    tokens: list[tuple[int, int, str]] = []
    for token in tokenize.generate_tokens(iter(text.splitlines(True)).__next__):
        if token.type == tokenize.STRING:
            try:
                value = ast.literal_eval(token.string)
            except Exception:
                continue
            if start <= token.start[0] <= end and family_label(value):
                tokens.append((token.start[0], token.start[1], value))
    # Dynamic tuple labels are declared outside the factory and therefore do
    # not appear in the token slice; insert them at the extension site.
    labels: list[tuple[int, int, int, str]] = []
    serial = 0
    for line, col, value in tokens:
        serial += 1
        labels.append((line, col, serial, value))
    # The extension is after all literal gzip labels in the r11 source.  Keep
    # this ordering rule explicit rather than relying on source line trivia.
    serial += 1
    labels.extend((dynamic_line, 10 + index, serial + index, value)
                  for index, value in enumerate(dynamic))
    labels.sort(key=lambda row: (row[0], row[1], row[2]))
    result = [row[3] for row in labels]
    if len(result) != EXPECTED_COUNT or len(set(result)) != EXPECTED_COUNT:
        raise CensusError(f"token enumeration count/uniqueness {len(result)}/"
                          f"{len(set(result))}, expected {EXPECTED_COUNT}")
    return result


def legacy_harness_names(raw: bytes) -> list[str]:
    tree = ast.parse(raw.decode("utf-8"), filename=str(LEGACY_HARNESS))
    main = find_function(tree, "main")
    result: list[str] = []
    for node in ast.walk(main):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "expect_fail" and node.args and
                isinstance(node.args[0], ast.Constant) and
                isinstance(node.args[0].value, str)):
            result.append(node.args[0].value)
    if len(result) != 13 or len(set(result)) != 13:
        raise CensusError(f"legacy harness enumeration {len(result)}/"
                          f"{len(set(result))}, expected 13")
    return result


def category_counts(labels: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(label.split(":", 1)[0] for label in labels).items()))


def route_counts(labels: Iterable[str]) -> dict[str, int]:
    routes = Counter()
    for label in labels:
        family = label.split(":", 1)[0]
        if family not in ROUTE_BY_FAMILY:
            raise CensusError(f"unrouted attack family: {family}")
        routes[ROUTE_BY_FAMILY[family]] += 1
    return dict(sorted(routes.items()))


def source_pin(tree: ast.Module) -> str | None:
    for node in tree.body:
        targets: list[ast.expr]
        value: ast.expr | None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign):
            targets, value = [node.target], node.value
        else:
            continue
        if any(isinstance(target, ast.Name) and target.id == "ATTACK_NAME_ORDER_PIN"
               for target in targets):
            try:
                parsed = ast.literal_eval(value)
            except Exception:
                return None
            return parsed if isinstance(parsed, str) else None
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumer", type=Path, default=R11_CONSUMER)
    parser.add_argument("--harness", type=Path, default=LEGACY_HARNESS)
    args = parser.parse_args(argv)
    report: dict[str, Any] = {
        "schema": "cm2.c79g.v16r2r11.read-only-attack-census.v1",
        "status": "FAIL_CLOSED_ATTACK_CENSUS_DIAGNOSTIC",
        "read_only": True,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "manifest_or_outer_created": False,
        "runtime_surface_created": False,
        "pyc_created_by_audit": False,
        # This tool proves only the source-level definition/order.  It never
        # invokes ``run_attacks``; the r11 static audit's runtime execution
        # census therefore remains 0/137 and cannot receive credit here.
        "enumeration_only": True,
        "attack_execution_observed": False,
        "r11_static_audit_execution_census": {
            "observed": 0,
            "required": EXPECTED_COUNT,
            "blocker": "cold runtime attack execution remains deferred",
        },
    }
    try:
        consumer_raw = stable(args.consumer)
        harness_raw = stable(args.harness)
        consumer_tree = ast.parse(consumer_raw.decode("utf-8"), filename=str(args.consumer))
        # In-memory compile is intentionally omitted: this is a lexical/AST
        # audit and must not create or authorize an executable artifact.
        ast_labels = ast_enumeration(consumer_tree)
        token_labels = token_enumeration(consumer_raw, consumer_tree)
        harness_labels = legacy_harness_names(harness_raw)
        ast_hash = line_sequence_sha256(ast_labels)
        token_hash = line_sequence_sha256(token_labels)
        harness_hash = sha(canonical(harness_labels))
        expected_pin = source_pin(consumer_tree)
        factory = find_function(consumer_tree, "make_attack_cases")
        dynamic = v11_names(consumer_tree)
        report.update({
            "status": "PASS_INDEPENDENT_R11_ATTACK_CENSUS_137_OF_137__ZERO_CREDIT",
            "consumer_path": str(args.consumer.relative_to(ROOT)),
            "consumer_file_sha256": sha(consumer_raw),
            "legacy_harness_path": str(args.harness.relative_to(ROOT)),
            "legacy_harness_file_sha256": sha(harness_raw),
            "checker_A_ast": {
                "algorithm": "AST_FACTORY_CONTAINER_AND_HELPER_ENUMERATION_A_V1",
                "count": len(ast_labels),
                "ordered_name_sha256": ast_hash,
                "category_counts": category_counts(ast_labels),
                "validator_route_counts": route_counts(ast_labels),
            },
            "checker_B_tokens": {
                "algorithm": "TOKEN_STRING_LITERAL_AND_DYNAMIC_TUPLE_ENUMERATION_B_V1",
                "count": len(token_labels),
                "ordered_name_sha256": token_hash,
                "category_counts": category_counts(token_labels),
                "validator_route_counts": route_counts(token_labels),
            },
            "checker_consensus": {
                "ordered_names_equal": ast_labels == token_labels,
                "ordered_name_sha256_equal": ast_hash == token_hash,
                "category_counts_equal": category_counts(ast_labels) == category_counts(token_labels),
                "validator_route_counts_equal": route_counts(ast_labels) == route_counts(token_labels),
            },
            "r11_contract_requirement": {
                "required_count": EXPECTED_COUNT,
                "required_ordered_name_sha256": EXPECTED_PIN,
                "source_declared_attack_name_order_pin": expected_pin,
                "count_matches": len(ast_labels) == EXPECTED_COUNT,
                "pin_matches": ast_hash == EXPECTED_PIN == expected_pin,
            },
            "r11_attack_factory": {
                "function": "make_attack_cases",
                "source_line_start": factory.lineno,
                "source_line_end": factory.end_lineno,
                "dynamic_v11_tuple_count": len(dynamic),
            },
            "legacy_13_case_harness": {
                "count": len(harness_labels),
                "ordered_name_sha256": harness_hash,
                "category_counts": category_counts(harness_labels),
                "missing_vs_r11_count": EXPECTED_COUNT - len(harness_labels),
                "order_pin_matches_r11": harness_hash == EXPECTED_PIN,
                "names_overlap_r11": len(set(harness_labels) & set(ast_labels)),
                "names": harness_labels,
            },
            "r11_attack_names": ast_labels,
        })
        # The diagnostic is successful only if both independent enumerators
        # agree and the source's formal pin is the 137-name line-sequence pin.
        report["audit_pass"] = bool(
            ast_labels == token_labels and ast_hash == token_hash == EXPECTED_PIN == expected_pin
            and len(harness_labels) == 13
        )
        if not report["audit_pass"]:
            report["status"] = "FAIL_CLOSED_ATTACK_CENSUS_MISMATCH__ZERO_CREDIT"
    except Exception as exc:  # pragma: no cover - fail-closed diagnostic path
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)
        report["audit_pass"] = False
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report.get("audit_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
