#!/usr/bin/env python3
"""Read-only AST inspection helpers for the C79g v12 draft sources.

The script parses source text only.  It never imports or executes a protocol
module, and it does not write protocol or runtime surfaces.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any


def literal_key(node: ast.AST) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def inspect(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    compile(tree, str(path), "exec", dont_inherit=True)
    set_closures: list[dict[str, Any]] = []
    dict_literals: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [literal_key(key) if key is not None else "**EXPANSION"
                    for key in node.keys]
            dict_literals.append({
                "line": node.lineno,
                "direct_key_count": sum(key is not None for key in node.keys),
                "expansion_count": sum(key is None for key in node.keys),
                "keys": keys,
            })
        if not (isinstance(node, ast.Compare) and
                isinstance(node.left, ast.Call) and
                isinstance(node.left.func, ast.Name) and
                node.left.func.id == "set" and
                len(node.left.args) == 1 and
                isinstance(node.left.args[0], ast.Name) and
                len(node.comparators) == 1 and
                isinstance(node.comparators[0], ast.Set)):
            continue
        variable = node.left.args[0].id
        keys = [literal_key(item) for item in node.comparators[0].elts]
        set_closures.append({
            "line": node.lineno,
            "variable": variable,
            "key_count": len(keys),
            "keys": keys,
        })
    return {
        "path": str(path),
        "ast_parse_and_in_memory_compile": True,
        "set_closures": sorted(set_closures, key=lambda item: item["line"]),
        "dict_literals": sorted(dict_literals, key=lambda item: item["line"]),
        "module_functions": {
            node.name: {
                "line": node.lineno,
                "normalized_ast_sha256": hashlib.sha256(ast.dump(
                    node, annotate_fields=True,
                    include_attributes=False).encode("utf-8")).hexdigest(),
            }
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--variable")
    parser.add_argument("--dict-line", type=int)
    parser.add_argument("--function")
    args = parser.parse_args()
    result = inspect(args.path)
    if args.variable is not None:
        result["set_closures"] = [
            item for item in result["set_closures"]
            if item["variable"] == args.variable]
        result.pop("dict_literals")
        result.pop("module_functions")
    elif args.dict_line is not None:
        result["dict_literals"] = [
            item for item in result["dict_literals"]
            if item["line"] == args.dict_line]
        result.pop("set_closures")
        result.pop("module_functions")
    elif args.function is not None:
        functions = result.pop("module_functions")
        result["module_functions"] = {
            args.function: functions.get(args.function)}
        result.pop("set_closures")
        result.pop("dict_literals")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
