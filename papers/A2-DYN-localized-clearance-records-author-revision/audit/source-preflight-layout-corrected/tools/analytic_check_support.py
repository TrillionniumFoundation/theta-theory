#!/usr/bin/env python3
"""Deterministic exact-check infrastructure; this is not a billiard proof engine."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from fractions import Fraction


ANCHOR_COMMIT = "03d651b8709d28d90aa435fc12d608ad9c945e23"
ANCHOR_ARTICLE_TREE = "3010c90e2363dfe1808101a3e992eb02643c28f1"
INHERITED_SHA256 = {
    "model.tex": "7ca3c885023e7e08e62e0aa16696336840b4b0ac271f9d5b105c4aba88406bb8",
    "inputs.tex": "0ec763b02ce9954fa5cbc7f63c020dd90a49d7d4406decb8a6d41c37b59090a4",
    "core/260_optical_jacobi_and_endpoint_trace_completion.tex": "2276a56b3f759ef96e8109d54f181f60b94ebf2ac9d04ef8b6a26ffe1f0453fc",
    "core/288_grazing_uniform_endpoint_localization.tex": "c4d9d73027361b9f202287c50582894747169cbe8b9f875404da6b86c91678f8",
    "core/315_full_physical_singular_multiplier.tex": "07f849b3cf160e0a99248594d49ae24bee0f39986a163f6f2bc33cd18ad5da14",
    "core/323_complete_physical_roof_variation.tex": "36eae03703168ed37d571a94bd8faf35398415163eaeb49d3b2d73c5b44bbdd8",
    "core/324_canonical_collision_boundary_budgets.tex": "9098b3bbca1bc336e9a1c9fe7050a0933e6b64b24fad3d9487bfe69e461cc59e",
    "core/325_exact_records_and_marked_roof_fourier.tex": "ebb0f60e0b5ca0d9d5233e1bc26c895ed59a00a51ae0d8285591228da57216c6",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def find_source(root: Path, relative: str) -> Path:
    alternatives = [root / relative, root / "inherited" / relative]
    if "/" not in relative:
        alternatives.extend([root / "core" / relative, root / "inherited" / "core" / relative])
    for candidate in alternatives:
        if candidate.is_file():
            return candidate
    raise RuntimeError("Required source was not found: " + relative)


def source_bindings(root: Path, native: list[str], program: Path) -> dict:
    sources = {}
    for relative, expected in INHERITED_SHA256.items():
        path = find_source(root, relative)
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if observed != expected:
            raise RuntimeError("Inherited source bytes changed: " + relative)
        sources[relative] = {
            "sha256": observed,
            "git_blob": git_blob(data),
            "bytes": len(data),
            "scope": "unchanged inherited input",
        }
    for relative in native:
        data = find_source(root, relative).read_bytes()
        sources[relative] = {
            "sha256": sha256_bytes(data),
            "git_blob": git_blob(data),
            "bytes": len(data),
            "scope": "new native proof bound to this execution",
        }
    for path in (program, Path(__file__).resolve()):
        data = path.read_bytes()
        sources[path.name] = {
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "scope": "executed exact checker",
        }
    return {
        "predecessor_commit": ANCHOR_COMMIT,
        "predecessor_article_tree": ANCHOR_ARTICLE_TREE,
        "sources": sources,
    }


class Audit:
    def __init__(self) -> None:
        self.groups: dict[str, int] = {}
        self.details: dict[str, object] = {}

    def check(self, group: str, condition: bool, context: object = None) -> None:
        if not condition:
            raise RuntimeError("Exact check failed: " + group + "; " + repr(context))
        self.groups[group] = self.groups.get(group, 0) + 1

    def detail(self, name: str, value: object) -> None:
        self.details[name] = value


def command_arguments(program: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", action="store_true", help="Include exact constants and scope-qualified check descriptions.")
    parser.add_argument("--source-root", type=Path, default=None, help="Article root containing core/, or reconstruction packet root.")
    parser.add_argument("--output", type=Path, default=None, help="Also save the identical deterministic JSON output here.")
    args = parser.parse_args()
    if args.source_root is None:
        here = program.parent
        args.source_root = here if (here / "330_all_label_physical_roof_variation.tex").is_file() else here.parent
    args.source_root = args.source_root.resolve()
    return args


def emit_result(args: argparse.Namespace, program: Path, native: list[str], audit: Audit, scope: list[str]) -> None:
    result = {
        "status": "pass",
        "program": program.name,
        "arithmetic": "exact rational and finite symbolic identities; no floating-point decisions",
        "total_checks": sum(audit.groups.values()),
        "groups": dict(sorted(audit.groups.items())),
        "scope": scope,
        "source_binding": source_bindings(args.source_root, native, program),
    }
    if args.details:
        result["details"] = audit.details
    rendered = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


def polynomial_value(coefficients: list[Fraction], x: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * x + coefficient
    return result


def derivative(coefficients: list[Fraction], order: int = 1) -> list[Fraction]:
    answer = coefficients[:]
    for _ in range(order):
        answer = [i * answer[i] for i in range(1, len(answer))] or [Fraction(0)]
    return answer


def integral(coefficients: list[Fraction], left: Fraction, right: Fraction) -> Fraction:
    antiderivative = [Fraction(0)] + [c / (i + 1) for i, c in enumerate(coefficients)]
    return polynomial_value(antiderivative, right) - polynomial_value(antiderivative, left)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
