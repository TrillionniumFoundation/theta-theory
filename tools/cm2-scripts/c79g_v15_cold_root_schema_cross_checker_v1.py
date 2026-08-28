#!/usr/bin/env python3
"""Read-only v15 cold-root/schema cross checker.

This checker never imports or executes the v15 launcher.  It parses the
frozen/current launcher as data, extracts the ``cold_root`` proof constructor,
and compares that constructor with ``$defs.coldLaunchProof`` in the closed
schema.  It also checks the two-level 124/126 identity census source gates and
requires the unpublished v15 manifest, outer, runtime, and bytecode surfaces
to remain absent.

The only supported command is::

    python3 -I -B scripts/c79g_v15_cold_root_schema_cross_checker_v1.py \
        /absolute/workspace PREFLIGHT

stdout is exactly one canonical JSON line.  A failed check returns nonzero.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Mapping


SCHEMA_ID = "cm2.c79g.v15.cold-root-schema-cross-checker.v1"
PASS_STATUS = "PASS_C79G_V15_COLD_ROOT_SCHEMA_CROSS_CHECK__PREFLIGHT_READ_ONLY"
FAIL_STATUS = "FAIL_C79G_V15_COLD_ROOT_SCHEMA_CROSS_CHECK__PUBLISH_NOT_AUTHORIZED"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
LAUNCHER_REL = Path("deliverables") / (BASE + "_cold_launch_v15.py")
SCHEMA_REL = Path("deliverables") / (BASE + "_schema_v15.json")
MANIFEST_REL = Path("deliverables") / (BASE + "_cold_launch_manifest_v15.sha256")
OUTER_REL = Path("deliverables") / (BASE + "_cold_launch_outer_receipt_v15.json")
CLAIM_REL = Path(".cm2-runtime") / ".c79g-v15-publish-guard.transaction-claim-v1"

EXPECTED_PREPUBLICATION_IDENTITY_COUNT = 124
EXPECTED_TERMINAL_IDENTITY_COUNT = 126
EXPECTED_TERMINAL_GROUP_LENGTHS = (
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    7, 1, 3, 3, 1, 1,
)
EXPECTED_IDENTITY_PROOF_KEY = (
    "all_current_and_historical_124_identities_globally_unique_on_one_statx_mount"
)
EXPECTED_FIRST_MEMBER_KEY = (
    "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt"
)
EXPECTED_COUNT_KEY = "current_v15_and_all_predecessor_unique_file_identity_count"


class CheckFailure(Exception):
    pass


class DuplicateKey(CheckFailure):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey("duplicate JSON key:" + key)
        result[key] = value
    return result


def reject_json_constant(token: str) -> Any:
    raise CheckFailure("non-finite JSON token:" + token)


def strict_json(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CheckFailure("schema is not UTF-8") from exc
    try:
        return json.loads(
            text, object_pairs_hook=strict_object_pairs,
            parse_constant=reject_json_constant,
        )
    except (json.JSONDecodeError, DuplicateKey) as exc:
        raise CheckFailure("strict schema JSON rejected:" + str(exc)) from exc


def held_read(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CheckFailure(label + ":open failed:" + str(exc)) from exc
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise CheckFailure(label + ":not regular nlink1")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        identity = (before.st_dev, before.st_ino)
        if identity != (after.st_dev, after.st_ino) or identity != (named.st_dev, named.st_ino):
            raise CheckFailure(label + ":held/named identity drift")
        fingerprint_before = (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        )
        fingerprint_after = (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        )
        fingerprint_named = (
            named.st_dev, named.st_ino, named.st_mode, named.st_nlink,
            named.st_size, named.st_mtime_ns, named.st_ctime_ns,
        )
        if fingerprint_before != fingerprint_after or fingerprint_before != fingerprint_named:
            raise CheckFailure(label + ":held/path fingerprint drift")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise CheckFailure(label + ":short read")
        return raw, {
            "file_sha256": sha256(raw),
            "mode": format(stat.S_IMODE(before.st_mode), "04o"),
            "nlink": before.st_nlink,
            "size": before.st_size,
        }
    finally:
        os.close(fd)


def single_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    found = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == name]
    if len(found) != 1 or not isinstance(found[0], ast.FunctionDef):
        raise CheckFailure("expected one direct function:" + name)
    return found[0]


def literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def literal_int(node: ast.AST | None) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    return None


def direct_named_assignment(scope: ast.AST, name: str) -> ast.AST:
    matches: list[ast.AST] = []
    body = getattr(scope, "body", [])
    for statement in body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name
                   for target in statement.targets):
                matches.append(statement.value)
        elif isinstance(statement, ast.AnnAssign) and \
                isinstance(statement.target, ast.Name) and statement.target.id == name:
            matches.append(statement.value)
    if len(matches) != 1:
        raise CheckFailure("expected one direct assignment:" + name)
    return matches[0]


def dict_entries(node: ast.AST, label: str) -> tuple[dict[str, ast.AST], list[ast.AST]]:
    if not isinstance(node, ast.Dict):
        raise CheckFailure(label + ":not a dict constructor")
    entries: dict[str, ast.AST] = {}
    unpacks: list[ast.AST] = []
    for key_node, value_node in zip(node.keys, node.values):
        if key_node is None:
            unpacks.append(value_node)
            continue
        key = literal_string(key_node)
        if key is None:
            raise CheckFailure(label + ":non-literal key")
        if key in entries:
            raise CheckFailure(label + ":duplicate literal key:" + key)
        entries[key] = value_node
    return entries, unpacks


def chronology_keys(tree: ast.Module) -> set[str]:
    function = single_function(tree, "cold_publication_chronology")
    returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    if len(returns) != 1:
        raise CheckFailure("chronology requires exactly one return")
    entries, unpacks = dict_entries(returns[0].value, "chronology return")
    if unpacks or len(entries) != 6:
        raise CheckFailure("chronology return must be closed exact6")
    return set(entries)


def proof_constructor(tree: ast.Module) -> tuple[dict[str, ast.AST], dict[str, Any]]:
    function = single_function(tree, "cold_root")
    proof_node = direct_named_assignment(function, "proof")
    direct, unpacks = dict_entries(proof_node, "cold_root proof")
    if len(unpacks) != 1 or not isinstance(unpacks[0], ast.Attribute) or \
            not isinstance(unpacks[0].value, ast.Name) or \
            unpacks[0].value.id != "bundle" or unpacks[0].attr != "chronology":
        raise CheckFailure("cold_root proof must have sole **bundle.chronology expansion")
    chrono = chronology_keys(tree)
    overlap = set(direct) & chrono
    if overlap:
        raise CheckFailure("proof/chronology duplicate keys:" + ",".join(sorted(overlap)))
    expanded = dict(direct)
    for key in chrono:
        expanded[key] = ast.Name(id="__chronology_runtime_true__", ctx=ast.Load())

    root_node = direct_named_assignment(function, "root")
    if not isinstance(root_node, ast.Call) or not isinstance(root_node.func, ast.Name) or \
            root_node.func.id != "close_object" or len(root_node.args) != 1:
        raise CheckFailure("cold_root root must be close_object(exact dict)")
    root_entries, root_unpacks = dict_entries(root_node.args[0], "cold_root root")
    if root_unpacks:
        raise CheckFailure("cold_root root constructor must not unpack")
    proof_ref = root_entries.get("cold_launch_proof")
    if not isinstance(proof_ref, ast.Name) or proof_ref.id != "proof":
        raise CheckFailure("returned root does not bind cold_launch_proof to proof")

    returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.Tuple) or \
            len(returns[0].value.elts) != 2 or \
            not isinstance(returns[0].value.elts[0], ast.Name) or \
            returns[0].value.elts[0].id != "root":
        raise CheckFailure("cold_root must return (root, inner) once")

    statements = list(function.body)
    return_index = next(index for index, statement in enumerate(statements)
                        if statement is returns[0])
    validator_indexes = [
        index for index, statement in enumerate(statements)
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and
        isinstance(statement.value.func, ast.Name) and statement.value.func.id == "validate_schema" and
        statement.value.args and isinstance(statement.value.args[0], ast.Name) and
        statement.value.args[0].id == "root"
    ]
    if len(validator_indexes) != 1 or validator_indexes[0] >= return_index:
        raise CheckFailure("root schema validation must occur exactly once before return")

    return expanded, {
        "direct_key_count": len(direct),
        "chronology_expansion_key_count": len(chrono),
        "expanded_key_count": len(expanded),
        "root_constructor_key_count": len(root_entries),
        "root_schema_validation_before_return": True,
        "return_shape": ["root", "inner"],
    }


def module_literal_bindings(tree: ast.Module) -> dict[str, Any]:
    """Resolve only side-effect-free scalar/container module constants."""
    result: dict[str, Any] = {}
    pending: list[tuple[str, ast.AST]] = []
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and \
                isinstance(statement.targets[0], ast.Name):
            pending.append((statement.targets[0].id, statement.value))
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            pending.append((statement.target.id, statement.value))
    changed = True
    while changed:
        changed = False
        remainder: list[tuple[str, ast.AST]] = []
        for name, node in pending:
            try:
                result[name] = static_value(node, result)
            except CheckFailure:
                remainder.append((name, node))
            else:
                changed = True
        pending = remainder
    return result


def static_value(node: ast.AST, bindings: Mapping[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (str, int, bool, type(None))):
            return node.value
        raise CheckFailure("unsupported constant")
    if isinstance(node, ast.Name):
        if node.id in bindings:
            return bindings[node.id]
        raise CheckFailure("unresolved name:" + node.id)
    if isinstance(node, ast.List):
        return [static_value(item, bindings) for item in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(static_value(item, bindings) for item in node.elts)
    if isinstance(node, ast.Set):
        return {static_value(item, bindings) for item in node.elts}
    if isinstance(node, ast.Dict):
        result: dict[str, Any] = {}
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:
                unpacked = static_value(value_node, bindings)
                if not isinstance(unpacked, Mapping):
                    raise CheckFailure("non-mapping static dict unpack")
                for key, value in unpacked.items():
                    if key in result:
                        raise CheckFailure("duplicate static dict key:" + str(key))
                    result[str(key)] = value
            else:
                key = static_value(key_node, bindings)
                if not isinstance(key, str) or key in result:
                    raise CheckFailure("invalid static dict key")
                result[key] = static_value(value_node, bindings)
        return result
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = static_value(node.operand, bindings)
        if isinstance(value, int) and not isinstance(value, bool):
            return -value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = static_value(node.left, bindings)
        right = static_value(node.right, bindings)
        if isinstance(left, (str, tuple, list)) and isinstance(right, type(left)):
            return left + right
    raise CheckFailure("expression is runtime-dependent:" + type(node).__name__)


def compare_schema_and_proof(
        schema: Mapping[str, Any], proof: Mapping[str, ast.AST],
        bindings: Mapping[str, Any]) -> dict[str, Any]:
    definitions = schema.get("$defs")
    if not isinstance(definitions, Mapping):
        raise CheckFailure("schema missing $defs")
    surface = definitions.get("coldLaunchProof")
    if not isinstance(surface, Mapping):
        raise CheckFailure("schema missing $defs.coldLaunchProof")
    if surface.get("type") != "object" or surface.get("additionalProperties") is not False:
        raise CheckFailure("coldLaunchProof must be closed object")
    required = surface.get("required")
    properties = surface.get("properties")
    if not isinstance(required, list) or not all(isinstance(key, str) for key in required):
        raise CheckFailure("coldLaunchProof required is not string list")
    if len(required) != len(set(required)):
        raise CheckFailure("coldLaunchProof required contains duplicates")
    if not isinstance(properties, Mapping) or not all(isinstance(key, str) for key in properties):
        raise CheckFailure("coldLaunchProof properties is not mapping")
    required_set = set(required)
    property_set = set(properties)
    proof_set = set(proof)
    if required_set != property_set or required_set != proof_set:
        raise CheckFailure(canonical({
            "schema_required_minus_proof": sorted(required_set - proof_set),
            "proof_minus_schema_required": sorted(proof_set - required_set),
            "properties_minus_required": sorted(property_set - required_set),
            "required_minus_properties": sorted(required_set - property_set),
        }).decode("utf-8"))

    statically_compared: list[str] = []
    dynamically_schema_enforced: list[str] = []
    mismatches: dict[str, Any] = {}
    const_keys = [key for key, value in properties.items()
                  if isinstance(value, Mapping) and "const" in value]
    for key in const_keys:
        expected = properties[key]["const"]
        try:
            actual = static_value(proof[key], bindings)
        except CheckFailure:
            dynamically_schema_enforced.append(key)
            continue
        if isinstance(actual, tuple):
            actual = list(actual)
        if actual != expected:
            mismatches[key] = {"launcher_static": actual, "schema_const": expected}
        else:
            statically_compared.append(key)
    if mismatches:
        raise CheckFailure("schema const mismatch:" + canonical(mismatches).decode("utf-8"))

    for key, expected in (
        (EXPECTED_IDENTITY_PROOF_KEY, True),
        (EXPECTED_FIRST_MEMBER_KEY, True),
        (EXPECTED_COUNT_KEY, EXPECTED_PREPUBLICATION_IDENTITY_COUNT),
    ):
        if key not in properties or not isinstance(properties[key], Mapping) or \
                properties[key].get("const") != expected:
            raise CheckFailure("critical schema const mismatch:" + key)
        if key not in proof:
            raise CheckFailure("critical proof key absent:" + key)
    expected_census_subscripts = {
        EXPECTED_IDENTITY_PROOF_KEY:
            "all_current_and_historical_124_identities_globally_unique_"
            "on_one_statx_mount",
        EXPECTED_COUNT_KEY: "v15_prepublication_unique_live_identity_count",
        EXPECTED_FIRST_MEMBER_KEY:
            "current_exact8_first_member_is_v14_registry_shape_drift_"
            "supersession_receipt",
    }
    for proof_key, census_key in expected_census_subscripts.items():
        expression = proof[proof_key]
        if not isinstance(expression, ast.Subscript) or \
                not isinstance(expression.value, ast.Name) or \
                expression.value.id != "live_global_identity_census" or \
                literal_string(expression.slice) != census_key:
            raise CheckFailure(
                "critical proof is not exact live census subscript:" + proof_key)

    return {
        "additionalProperties": False,
        "required_key_count": len(required_set),
        "property_key_count": len(property_set),
        "proof_key_count": len(proof_set),
        "required_properties_proof_keysets_equal": True,
        "schema_const_key_count": len(const_keys),
        "statically_evaluated_const_key_count": len(statically_compared),
        "runtime_dependent_const_key_count": len(dynamically_schema_enforced),
        "all_statically_evaluable_consts_equal": True,
        "runtime_dependent_consts_closed_by_pre_return_schema_validation": True,
        "critical_identity_consts_equal": True,
        "critical_live_census_subscript_shapes_closed": True,
    }


def source_segment(raw: bytes, node: ast.AST) -> str:
    text = raw.decode("utf-8")
    segment = ast.get_source_segment(text, node)
    if segment is None:
        raise CheckFailure("unable to recover AST source segment")
    return segment


def need_call_segments(raw: bytes, tree: ast.Module) -> list[str]:
    result: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                node.func.id == "need" and node.args:
            result.append(source_segment(raw, node.args[0]))
    return result


def identity_census_source_audit(raw: bytes, tree: ast.Module) -> dict[str, Any]:
    segments = need_call_segments(raw, tree)
    prepublication = [segment for segment in segments
                      if str(EXPECTED_PREPUBLICATION_IDENTITY_COUNT) in segment and
                      ("prepublication" in segment or "unique_live_identity_count" in segment)]
    if not prepublication:
        raise CheckFailure("missing prepublication124 source gate")

    held_bundle = [node for node in tree.body
                   if isinstance(node, ast.ClassDef) and node.name == "HeldBundle"]
    if len(held_bundle) != 1:
        raise CheckFailure("expected one HeldBundle class")
    census_method = single_function_in_class(
        held_bundle[0], "_global_identity_census")
    census_source = source_segment(raw, census_method)
    required_census_tokens = (
        "len(predecessor_identities) == 116",
        "len(prepublication_identities) == 124",
        "len(terminal_identities) == 126",
        "len(owned_v14_identities) == 11",
        "current_exact8_identities.isdisjoint(predecessor_identities)",
        "v14_supersession.identity not in owned_v14_identities",
        "pairwise_disjoint",
        "distinct_descriptors",
        "one_mount",
    )
    for token in required_census_tokens:
        if token not in census_source:
            raise CheckFailure("global census missing mechanical token:" + token)

    group_guard_assignments = [
        node.value for node in ast.walk(census_method)
        if isinstance(node, ast.Assign) and
        any(isinstance(target, ast.Name) and target.id == "group_guards"
            for target in node.targets)
    ]
    if len(group_guard_assignments) != 1 or \
            not isinstance(group_guard_assignments[0], ast.List):
        raise CheckFailure("expected one literal HeldBundle group_guards list")
    group_list = group_guard_assignments[0]
    if len(group_list.elts) != len(EXPECTED_TERMINAL_GROUP_LENGTHS):
        raise CheckFailure("terminal identity group expression count is not exact17")
    group_source = [source_segment(raw, item) for item in group_list.elts]
    v14_groups = [item for item in group_source if "v14" in item.lower()]
    if len(v14_groups) != 2 or \
            not any("exact10" in item.lower() for item in v14_groups) or \
            not any("rejection" in item.lower() for item in v14_groups):
        raise CheckFailure(
            "identity_groups must split v14 exact10 and official rejection")

    identity_group_assignments = [
        node.value for node in ast.walk(census_method)
        if isinstance(node, ast.Assign) and
        any(isinstance(target, ast.Name) and target.id == "identity_groups"
            for target in node.targets)
    ]
    if len(identity_group_assignments) != 1 or \
            not isinstance(identity_group_assignments[0], ast.ListComp):
        raise CheckFailure("identity_groups must be one mechanical list comprehension")
    identity_comp = identity_group_assignments[0]
    if len(identity_comp.generators) != 1 or identity_comp.generators[0].ifs or \
            not isinstance(identity_comp.elt, ast.SetComp):
        raise CheckFailure("identity_groups comprehension shape is not closed")

    vector = list(EXPECTED_TERMINAL_GROUP_LENGTHS)
    compact_census = "".join(census_source.split())
    if str(vector).replace(" ", "") not in compact_census:
        raise CheckFailure("terminal126 group lengths are not exact frozen vector")

    exact12_function = single_function_in_class(
        held_bundle[0], "_hold_v14_inherited_authority_exact12")
    combined_source = source_segment(raw, exact12_function) + "\n" + \
        source_segment(raw, census_method)
    for token in (
        "V14_INHERITED_AUTHORITY_EXACT12", "12",
        "guards[-1] is self.files[0]", "isdisjoint",
    ):
        if token not in combined_source:
            raise CheckFailure("v14 exact12/census missing source token:" + token)

    return {
        "prepublication_unique_live_identity_count": EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "terminal_unique_live_identity_count": EXPECTED_TERMINAL_IDENTITY_COUNT,
        "terminal_identity_group_count": len(group_list.elts),
        "terminal_identity_group_lengths": list(EXPECTED_TERMINAL_GROUP_LENGTHS),
        "terminal_all_groups_pairwise_disjoint_gate": True,
        "v14_exact12_receipt_reused_as_current_first_member": True,
        "v14_exact12_extra11_cross_disjoint_gate": True,
    }


def single_function_in_class(cls: ast.ClassDef, name: str) -> ast.FunctionDef:
    found = [node for node in cls.body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise CheckFailure("expected one method:" + cls.name + "." + name)
    return found[0]


def duplicate_literal_dict_keys(tree: ast.Module) -> list[dict[str, Any]]:
    duplicates: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[Any] = set()
        for key_node in node.keys:
            if not isinstance(key_node, ast.Constant) or \
                    not isinstance(key_node.value, (str, int, bool, type(None))):
                continue
            key = key_node.value
            if key in seen:
                duplicates.append({"line": key_node.lineno, "key": key})
            seen.add(key)
    return duplicates


def absent_surface_snapshot(root: Path) -> dict[str, Any]:
    exact_paths = [MANIFEST_REL, OUTER_REL, CLAIM_REL]
    present_exact = [str(path) for path in exact_paths if os.path.lexists(root / path)]

    runtime_hits: list[str] = []
    runtime = root / ".cm2-runtime"
    if runtime.exists():
        for directory, names, files in os.walk(runtime, followlinks=False):
            for name in [*names, *files]:
                relative = (Path(directory) / name).relative_to(root)
                if "c79g-v15" in name.lower():
                    runtime_hits.append(str(relative))

    pyc_hits: list[str] = []
    for top_relative in (Path("deliverables"), Path("scripts")):
        top = root / top_relative
        if not top.exists():
            continue
        for directory, _, files in os.walk(top, followlinks=False):
            for name in files:
                if name.endswith(".pyc") and "v15" in name.lower():
                    pyc_hits.append(str((Path(directory) / name).relative_to(root)))

    return {
        "manifest_absent": not os.path.lexists(root / MANIFEST_REL),
        "outer_absent": not os.path.lexists(root / OUTER_REL),
        "transaction_claim_absent": not os.path.lexists(root / CLAIM_REL),
        "present_exact_paths": sorted(present_exact),
        "v15_runtime_surface_paths": sorted(set(runtime_hits)),
        "v15_pyc_paths": sorted(set(pyc_hits)),
    }


def audit(root: Path) -> tuple[dict[str, Any], bool]:
    checks: list[dict[str, Any]] = []

    def record(name: str, operation: Any, detailer: Any = None) -> Any:
        try:
            detail = operation()
        except BaseException as exc:
            checks.append({"name": name, "pass": False,
                           "detail": type(exc).__name__ + ":" + str(exc)})
            return None
        rendered = detailer(detail) if detailer is not None else detail
        checks.append({"name": name, "pass": True, "detail": rendered})
        return detail

    launcher_read = record(
        "held_read_launcher",
        lambda: held_read(root / LAUNCHER_REL, "launcher"),
        lambda value: value[1],
    )
    schema_read = record(
        "held_read_schema",
        lambda: held_read(root / SCHEMA_REL, "schema"),
        lambda value: value[1],
    )
    if launcher_read is None or schema_read is None:
        report = finish_report(checks, {}, {})
        return report, False
    launcher_raw, launcher_stat = launcher_read
    schema_raw, schema_stat = schema_read

    def parse_launcher() -> ast.Module:
        tree = ast.parse(launcher_raw, filename=str(LAUNCHER_REL), mode="exec")
        compile(tree, str(LAUNCHER_REL), "exec", dont_inherit=True, optimize=0)
        return tree

    tree = record(
        "launcher_AST_and_in_memory_compile", parse_launcher,
        lambda value: {"AST_node_count": sum(1 for _ in ast.walk(value))},
    )
    schema = record(
        "strict_schema_JSON", lambda: strict_json(schema_raw),
        lambda value: {
            "top_level_key_count": len(value) if isinstance(value, Mapping) else -1,
            "coldLaunchProof_present": isinstance(value, Mapping) and
                isinstance(value.get("$defs"), Mapping) and
                "coldLaunchProof" in value["$defs"],
        },
    )
    if tree is None or schema is None or not isinstance(tree, ast.Module) or \
            not isinstance(schema, Mapping):
        report = finish_report(checks, launcher_stat, schema_stat)
        return report, False

    record(
        "launcher_no_duplicate_literal_dict_keys",
        lambda: require_empty(duplicate_literal_dict_keys(tree),
                              "duplicate literal dict keys"),
    )
    constructed = record(
        "cold_root_returned_proof_constructor",
        lambda: proof_constructor(tree),
        lambda value: value[1],
    )
    if constructed is not None:
        proof, constructor_detail = constructed
        bindings = module_literal_bindings(tree)
        record(
            "closed_schema_required_properties_consts_match_proof",
            lambda: compare_schema_and_proof(schema, proof, bindings),
        )
    record(
        "terminal126_prepublication124_v14_exact12_extra11_source_gates",
        lambda: identity_census_source_audit(launcher_raw, tree),
    )

    before_absence = record(
        "manifest_outer_runtime_pyc_absent_before",
        lambda: require_absent(absent_surface_snapshot(root)),
    )
    launcher_again = record(
        "launcher_bytes_stable_after_review",
        lambda: require_same_file(root / LAUNCHER_REL, launcher_raw, launcher_stat),
    )
    schema_again = record(
        "schema_bytes_stable_after_review",
        lambda: require_same_file(root / SCHEMA_REL, schema_raw, schema_stat),
    )
    after_absence = record(
        "manifest_outer_runtime_pyc_absent_after",
        lambda: require_absent(absent_surface_snapshot(root)),
    )
    record(
        "read_only_surface_snapshot_stable",
        lambda: require_equal(before_absence, after_absence,
                              "absence snapshot drift"),
    )
    _ = launcher_again, schema_again

    report = finish_report(checks, launcher_stat, schema_stat)
    return report, report["failed_check_count"] == 0


def require_empty(value: list[Any], label: str) -> dict[str, Any]:
    if value:
        raise CheckFailure(label + ":" + canonical(value).decode("utf-8"))
    return {"count": 0}


def require_absent(value: Mapping[str, Any]) -> dict[str, Any]:
    if value.get("present_exact_paths") or value.get("v15_runtime_surface_paths") or \
            value.get("v15_pyc_paths") or not value.get("manifest_absent") or \
            not value.get("outer_absent") or not value.get("transaction_claim_absent"):
        raise CheckFailure("publication/runtime/pyc contamination:" +
                           canonical(value).decode("utf-8"))
    return dict(value)


def require_same_file(
        path: Path, expected_raw: bytes, expected_stat: Mapping[str, Any]) -> dict[str, Any]:
    raw, current_stat = held_read(path, str(path))
    if raw != expected_raw or current_stat != expected_stat:
        raise CheckFailure("reviewed file drift:" + str(path))
    return current_stat


def require_equal(left: Any, right: Any, label: str) -> dict[str, Any]:
    if left != right:
        raise CheckFailure(label)
    return {"equal": True}


def finish_report(
        checks: list[dict[str, Any]], launcher_stat: Mapping[str, Any],
        schema_stat: Mapping[str, Any]) -> dict[str, Any]:
    failed = [item["name"] for item in checks if item["pass"] is not True]
    return {
        "schema": SCHEMA_ID,
        "status": PASS_STATUS if not failed else FAIL_STATUS,
        "mode": "PREFLIGHT",
        "read_only": True,
        "protocol_executed": False,
        "pyc_generation_allowed": False,
        "expected_prepublication_unique_live_identity_count":
            EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "expected_terminal_unique_live_identity_count":
            EXPECTED_TERMINAL_IDENTITY_COUNT,
        "launcher": dict(launcher_stat),
        "closed_schema": dict(schema_stat),
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": checks,
    }


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[2] != "PREFLIGHT":
        report = {
            "schema": SCHEMA_ID,
            "status": FAIL_STATUS,
            "mode": "INVALID_CLI",
            "read_only": True,
            "protocol_executed": False,
            "pyc_generation_allowed": False,
            "failed_check_count": 1,
            "failed_checks": ["exact_CLI"],
        }
        sys.stdout.buffer.write(canonical(report) + b"\n")
        return 2
    root = Path(sys.argv[1])
    if not root.is_absolute() or not root.is_dir():
        report = {
            "schema": SCHEMA_ID,
            "status": FAIL_STATUS,
            "mode": "PREFLIGHT",
            "read_only": True,
            "protocol_executed": False,
            "pyc_generation_allowed": False,
            "failed_check_count": 1,
            "failed_checks": ["absolute_workspace_root"],
        }
        sys.stdout.buffer.write(canonical(report) + b"\n")
        return 2
    report, passed = audit(root)
    sys.stdout.buffer.write(canonical(report) + b"\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
