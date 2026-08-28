#!/usr/bin/env python3
"""Round306B1AF4 source-free normalized-support symbolic kernel.

This file is a deterministic symbolic foundation only.  It defines a small
tagged AST, exact rational and rational-interval operations, explicit Source-G
formula builders, macro lowering, and *shape* validators for future proof
payloads.  It is not a data constructor, does not read any upstream artifact,
and mints no theorem, support, representation, transition, or CM2 credit.

Only ``--print-kernel-contract`` and ``--self-test`` are public modes.  With no
arguments the program is silent.  Candidate, production, and unknown modes are
silently refused before any path inspection, file open, temporary creation,
write, or output operation.
"""

from __future__ import annotations

import builtins
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from math import isqrt
import json
import os
import re
import sys
import tempfile
from typing import Any, Callable, Iterable, Mapping, NoReturn, Sequence
from unittest import mock


class KernelError(ValueError):
    """Fail-closed symbolic-kernel validation error."""


class KernelRefusal(RuntimeError):
    """A deliberately unavailable candidate or production operation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise KernelError(label)


SCHEMA = "cm2.round306b1af4.source-g-normalized-support-symbolic-kernel.v1"
STATUS = "SOURCE_FREE_EXACT_SYMBOLIC_FOUNDATION__ZERO_THEOREM_CREDIT"
REFUSAL = (
    "Round306B1AF4 is not a data constructor; candidate and production modes "
    "are unavailable before filesystem or output boundaries"
)
SCALAR = "SCALAR"
PREDICATE = "PREDICATE"
TRUTH_VALUES = ("FALSE", "TRUE", "UNKNOWN")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,127}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/+\-]{0,511}$")
MAX_AST_DEPTH = 256
MAX_AST_NODES = 200_000
MAX_RATIONAL_BITS = 4096
MAX_SQRT_BITS = 256

BASELINE_OPERATORS = (
    "CONST_Q",
    "VAR",
    "NEG",
    "ADD",
    "SUB",
    "MUL",
    "DIV_NONZERO",
    "SQUARE",
    "SQRT_POSITIVE",
    "EQ_ZERO",
    "LT_ZERO",
    "GT_ZERO",
    "AND",
    "OR_DISJOINT",
    "RESTRICT",
)

MACRO_IDS = (
    "OPEN_RATIONAL_BOX",
    "STRICT_SIGN_CELL",
    "FINITE_DISJOINT_UNION",
    "BOUNDARY_RESTRICTION",
    "CHART_PULLBACK",
    "TPS_DOMAIN",
    "SOURCE_G_FIRST_HIT_MAP",
    "WALL_ENDPOINT_FACTOR",
    "OUTGOING_DIAGONAL_FACTOR",
    "IMPLICIT_REGULAR_GRAPH",
    "SHEET_MEMBER_EQUIVALENCE",
    "BOUNDARY_TRACE_INCIDENCE",
    "HALF_OPEN_BOUNDARY_ASSIGNMENT",
)

PROOF_KERNEL_IDS = (
    "EXACT_RATIONAL_AST_NORMALIZATION_V2",
    "DIRECTED_RATIONAL_INTERVAL_SIGN_V1",
    "POSITIVE_SQRT_INTERVAL_V1",
    "PREDICATE_CELL_EQUIVALENCE_V1",
    "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1",
    "DEPENDENT_INCIDENCE_RESTRICTION_V1",
    "FINITE_HALF_OPEN_SUPPORT_UNION_V1",
    "ARTIFICIAL_FACE_REGLUE_V1",
    "FIXED_SIGN_T2PS_PULLBACK_V1",
    "REPRESENTATION_OWNER_BACKBINDING_V1",
    "SHEET_MEMBER_EQUIVALENCE_V1",
    "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1",
    "SOURCE_LINEAGE_EXHAUSTION_V1",
)


def _wire(value: Any) -> Any:
    """Convert supported exact objects to a JSON-only deterministic value."""
    if isinstance(value, Fraction):
        return {"denominator": value.denominator, "numerator": value.numerator}
    if isinstance(value, RationalInterval):
        return value.to_wire()
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, Mapping):
        need(all(isinstance(key, str) for key in value), "JSON object keys are strings")
        return {key: _wire(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_wire(item) for item in value]
    raise KernelError("unsupported canonical JSON value:" + type(value).__name__)


def canonical_json(value: Any) -> str:
    return json.dumps(
        _wire(value),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("ascii")).hexdigest()


def as_fraction(value: Any, label: str = "rational") -> Fraction:
    """Parse an exact rational; binary floats are intentionally forbidden."""
    if isinstance(value, bool) or isinstance(value, float):
        raise KernelError(label + " must be exact rational")
    if isinstance(value, Fraction):
        result = value
    elif isinstance(value, int):
        result = Fraction(value, 1)
    elif isinstance(value, Mapping):
        need(set(value) == {"numerator", "denominator"}, label + " wire keys")
        numerator = value["numerator"]
        denominator = value["denominator"]
        need(
            isinstance(numerator, int) and not isinstance(numerator, bool),
            label + " numerator",
        )
        need(
            isinstance(denominator, int)
            and not isinstance(denominator, bool)
            and denominator != 0,
            label + " denominator",
        )
        result = Fraction(numerator, denominator)
    elif isinstance(value, tuple) and len(value) == 2:
        numerator, denominator = value
        need(
            isinstance(numerator, int)
            and not isinstance(numerator, bool)
            and isinstance(denominator, int)
            and not isinstance(denominator, bool)
            and denominator != 0,
            label + " tuple",
        )
        result = Fraction(numerator, denominator)
    else:
        raise KernelError(label + " must be int, Fraction, pair, or rational wire")
    need(
        result.numerator.bit_length() <= MAX_RATIONAL_BITS
        and result.denominator.bit_length() <= MAX_RATIONAL_BITS,
        label + " bit bound",
    )
    return result


def rational_wire(value: Any) -> dict[str, int]:
    q = as_fraction(value)
    return {"denominator": q.denominator, "numerator": q.numerator}


@dataclass(frozen=True)
class RationalInterval:
    """Closed exact rational interval with outward operations."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        lo = as_fraction(self.lower, "interval lower")
        hi = as_fraction(self.upper, "interval upper")
        need(lo <= hi, "interval lower <= upper")
        object.__setattr__(self, "lower", lo)
        object.__setattr__(self, "upper", hi)

    @classmethod
    def point(cls, value: Any) -> "RationalInterval":
        q = as_fraction(value)
        return cls(q, q)

    @classmethod
    def from_wire(cls, value: Any) -> "RationalInterval":
        need(isinstance(value, Mapping), "interval object")
        need(set(value) == {"lower", "upper"}, "interval wire keys")
        return cls(
            as_fraction(value["lower"], "interval lower"),
            as_fraction(value["upper"], "interval upper"),
        )

    def to_wire(self) -> dict[str, dict[str, int]]:
        return {
            "lower": rational_wire(self.lower),
            "upper": rational_wire(self.upper),
        }

    def __neg__(self) -> "RationalInterval":
        return RationalInterval(-self.upper, -self.lower)

    def add(self, other: "RationalInterval") -> "RationalInterval":
        return RationalInterval(self.lower + other.lower, self.upper + other.upper)

    def sub(self, other: "RationalInterval") -> "RationalInterval":
        return self.add(-other)

    def mul(self, other: "RationalInterval") -> "RationalInterval":
        products = (
            self.lower * other.lower,
            self.lower * other.upper,
            self.upper * other.lower,
            self.upper * other.upper,
        )
        return RationalInterval(min(products), max(products))

    def square(self) -> "RationalInterval":
        endpoint_squares = (self.lower * self.lower, self.upper * self.upper)
        lower = Fraction(0) if self.lower <= 0 <= self.upper else min(endpoint_squares)
        return RationalInterval(lower, max(endpoint_squares))

    def reciprocal_nonzero(self) -> "RationalInterval":
        need(not (self.lower <= 0 <= self.upper), "division interval excludes zero")
        values = (Fraction(1, self.lower), Fraction(1, self.upper))
        return RationalInterval(min(values), max(values))

    def div_nonzero(self, other: "RationalInterval") -> "RationalInterval":
        return self.mul(other.reciprocal_nonzero())


def _sqrt_floor_scaled(value: Fraction, bits: int) -> Fraction:
    need(value >= 0, "sqrt lower radicand nonnegative")
    scale = 1 << bits
    quotient = (value.numerator * scale * scale) // value.denominator
    return Fraction(isqrt(quotient), scale)


def _sqrt_ceil_scaled(value: Fraction, bits: int) -> Fraction:
    lower = _sqrt_floor_scaled(value, bits)
    if lower * lower == value:
        return lower
    return lower + Fraction(1, 1 << bits)


def positive_sqrt_bounds(
    interval: RationalInterval,
    precision_bits: int = 64,
) -> RationalInterval:
    """Conservative rational bounds for the positive square-root branch."""
    need(
        isinstance(precision_bits, int)
        and not isinstance(precision_bits, bool)
        and 1 <= precision_bits <= MAX_SQRT_BITS,
        "sqrt precision bits",
    )
    need(interval.lower > 0, "SQRT_POSITIVE interval is strictly positive")
    result = RationalInterval(
        _sqrt_floor_scaled(interval.lower, precision_bits),
        _sqrt_ceil_scaled(interval.upper, precision_bits),
    )
    need(result.lower * result.lower <= interval.lower, "sqrt lower outward")
    need(result.upper * result.upper >= interval.upper, "sqrt upper outward")
    return result


def _node(op: str, **fields: Any) -> dict[str, Any]:
    return {"op": op, **fields}


def const_q(value: Any) -> dict[str, Any]:
    return _node("CONST_Q", value=rational_wire(value))


def var(name: str) -> dict[str, Any]:
    need(isinstance(name, str) and bool(NAME.fullmatch(name)), "variable name")
    return _node("VAR", name=name)


def neg(arg: Any) -> dict[str, Any]:
    return _node("NEG", arg=arg)


def add(*args: Any) -> dict[str, Any]:
    return _node("ADD", args=list(args))


def sub(left: Any, right: Any) -> dict[str, Any]:
    return _node("SUB", left=left, right=right)


def mul(*args: Any) -> dict[str, Any]:
    return _node("MUL", args=list(args))


def div_nonzero(left: Any, right: Any) -> dict[str, Any]:
    return _node("DIV_NONZERO", left=left, right=right)


def square(arg: Any) -> dict[str, Any]:
    return _node("SQUARE", arg=arg)


def sqrt_positive(arg: Any) -> dict[str, Any]:
    return _node("SQRT_POSITIVE", arg=arg)


def eq_zero(arg: Any) -> dict[str, Any]:
    return _node("EQ_ZERO", arg=arg)


def lt_zero(arg: Any) -> dict[str, Any]:
    return _node("LT_ZERO", arg=arg)


def gt_zero(arg: Any) -> dict[str, Any]:
    return _node("GT_ZERO", arg=arg)


def and_pred(*args: Any) -> dict[str, Any]:
    return _node("AND", args=list(args))


def or_disjoint(*args: Any) -> dict[str, Any]:
    return _node("OR_DISJOINT", args=list(args))


def restrict(predicate: Any, domain: Any) -> dict[str, Any]:
    return _node("RESTRICT", predicate=predicate, domain=domain)


def _exact_keys(node: Mapping[str, Any], expected: set[str], label: str) -> None:
    need(set(node) == expected, label + " exact keys")


def infer_ast_type(node: Any) -> str:
    """Validate a primitive tagged AST and return SCALAR or PREDICATE."""
    seen = [0]

    def visit(value: Any, depth: int) -> str:
        need(depth <= MAX_AST_DEPTH, "AST depth bound")
        seen[0] += 1
        need(seen[0] <= MAX_AST_NODES, "AST node bound")
        need(isinstance(value, Mapping), "AST node object")
        op = value.get("op")
        need(isinstance(op, str) and op in BASELINE_OPERATORS, "known AST operator")
        if op == "CONST_Q":
            _exact_keys(value, {"op", "value"}, op)
            as_fraction(value["value"], "CONST_Q")
            return SCALAR
        if op == "VAR":
            _exact_keys(value, {"op", "name"}, op)
            need(
                isinstance(value["name"], str) and bool(NAME.fullmatch(value["name"])),
                "VAR name",
            )
            return SCALAR
        if op in {"NEG", "SQUARE", "SQRT_POSITIVE"}:
            _exact_keys(value, {"op", "arg"}, op)
            need(visit(value["arg"], depth + 1) == SCALAR, op + " scalar arg")
            if op == "SQRT_POSITIVE" and value["arg"].get("op") == "CONST_Q":
                need(as_fraction(value["arg"]["value"]) > 0, "constant SQRT_POSITIVE")
            return SCALAR
        if op in {"ADD", "MUL"}:
            _exact_keys(value, {"op", "args"}, op)
            args = value["args"]
            need(isinstance(args, list) and len(args) >= 2, op + " arity")
            need(all(visit(arg, depth + 1) == SCALAR for arg in args), op + " scalar args")
            return SCALAR
        if op in {"SUB", "DIV_NONZERO"}:
            _exact_keys(value, {"op", "left", "right"}, op)
            need(visit(value["left"], depth + 1) == SCALAR, op + " left scalar")
            need(visit(value["right"], depth + 1) == SCALAR, op + " right scalar")
            if op == "DIV_NONZERO" and value["right"].get("op") == "CONST_Q":
                need(as_fraction(value["right"]["value"]) != 0, "constant DIV_NONZERO")
            return SCALAR
        if op in {"EQ_ZERO", "LT_ZERO", "GT_ZERO"}:
            _exact_keys(value, {"op", "arg"}, op)
            need(visit(value["arg"], depth + 1) == SCALAR, op + " scalar arg")
            return PREDICATE
        if op in {"AND", "OR_DISJOINT"}:
            _exact_keys(value, {"op", "args"}, op)
            args = value["args"]
            need(isinstance(args, list) and len(args) >= 2, op + " arity")
            need(
                all(visit(arg, depth + 1) == PREDICATE for arg in args),
                op + " predicate args",
            )
            if op == "OR_DISJOINT":
                encodings = [canonical_json(arg) for arg in args]
                need(len(set(encodings)) == len(encodings), "OR_DISJOINT duplicate branch")
            return PREDICATE
        if op == "RESTRICT":
            _exact_keys(value, {"op", "predicate", "domain"}, op)
            need(visit(value["predicate"], depth + 1) == PREDICATE, "RESTRICT predicate")
            need(visit(value["domain"], depth + 1) == PREDICATE, "RESTRICT domain")
            return PREDICATE
        raise AssertionError("unreachable AST operator")

    return visit(node, 0)


def _const_value(node: Mapping[str, Any]) -> Fraction | None:
    if node.get("op") == "CONST_Q":
        return as_fraction(node["value"])
    return None


def _perfect_rational_sqrt(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return Fraction(numerator, denominator)
    return None


def normalize_ast(node: Any) -> dict[str, Any]:
    """Deterministically normalize a validated primitive AST."""
    infer_ast_type(node)

    def norm(value: Mapping[str, Any]) -> dict[str, Any]:
        op = value["op"]
        if op == "CONST_Q":
            return const_q(as_fraction(value["value"]))
        if op == "VAR":
            return var(value["name"])
        if op == "NEG":
            arg = norm(value["arg"])
            constant = _const_value(arg)
            if constant is not None:
                return const_q(-constant)
            if arg["op"] == "NEG":
                return arg["arg"]
            return neg(arg)
        if op in {"ADD", "MUL"}:
            flattened: list[dict[str, Any]] = []
            for raw_arg in value["args"]:
                arg = norm(raw_arg)
                if arg["op"] == op:
                    flattened.extend(arg["args"])
                else:
                    flattened.append(arg)
            constants: list[Fraction] = []
            symbolic: list[dict[str, Any]] = []
            for arg in flattened:
                constant = _const_value(arg)
                if constant is None:
                    symbolic.append(arg)
                else:
                    constants.append(constant)
            if op == "ADD":
                total = sum(constants, Fraction(0))
                if total or not symbolic:
                    symbolic.append(const_q(total))
            else:
                product = Fraction(1)
                for constant in constants:
                    product *= constant
                if product == 0:
                    return const_q(0)
                if product != 1 or not symbolic:
                    symbolic.append(const_q(product))
            symbolic.sort(key=canonical_json)
            if len(symbolic) == 1:
                return symbolic[0]
            return _node(op, args=symbolic)
        if op == "SUB":
            left = norm(value["left"])
            right = norm(value["right"])
            left_q = _const_value(left)
            right_q = _const_value(right)
            if left_q is not None and right_q is not None:
                return const_q(left_q - right_q)
            if right_q == 0:
                return left
            return sub(left, right)
        if op == "DIV_NONZERO":
            left = norm(value["left"])
            right = norm(value["right"])
            left_q = _const_value(left)
            right_q = _const_value(right)
            if right_q == 0:
                raise KernelError("constant DIV_NONZERO")
            if left_q is not None and right_q is not None:
                return const_q(left_q / right_q)
            if left_q == 0:
                return const_q(0)
            if right_q == 1:
                return left
            return div_nonzero(left, right)
        if op == "SQUARE":
            arg = norm(value["arg"])
            constant = _const_value(arg)
            if constant is not None:
                return const_q(constant * constant)
            if arg["op"] == "NEG":
                arg = arg["arg"]
            return square(arg)
        if op == "SQRT_POSITIVE":
            arg = norm(value["arg"])
            constant = _const_value(arg)
            if constant is not None:
                need(constant > 0, "constant SQRT_POSITIVE")
                exact = _perfect_rational_sqrt(constant)
                if exact is not None:
                    return const_q(exact)
            return sqrt_positive(arg)
        if op in {"EQ_ZERO", "LT_ZERO", "GT_ZERO"}:
            return _node(op, arg=norm(value["arg"]))
        if op in {"AND", "OR_DISJOINT"}:
            flattened_predicates: list[dict[str, Any]] = []
            for raw_arg in value["args"]:
                arg = norm(raw_arg)
                if arg["op"] == op:
                    flattened_predicates.extend(arg["args"])
                else:
                    flattened_predicates.append(arg)
            keyed = sorted(
                ((canonical_json(arg), arg) for arg in flattened_predicates),
                key=lambda pair: pair[0],
            )
            if op == "AND":
                unique: list[dict[str, Any]] = []
                previous: str | None = None
                for encoding, arg in keyed:
                    if encoding != previous:
                        unique.append(arg)
                    previous = encoding
                if len(unique) == 1:
                    return unique[0]
                return and_pred(*unique)
            need(
                len({encoding for encoding, _arg in keyed}) == len(keyed),
                "OR_DISJOINT duplicate normalized branch",
            )
            return or_disjoint(*(arg for _encoding, arg in keyed))
        if op == "RESTRICT":
            return restrict(norm(value["predicate"]), norm(value["domain"]))
        raise AssertionError("unreachable normalize operator")

    result = norm(node)
    infer_ast_type(result)
    return result


def ast_hash(node: Any) -> str:
    return canonical_hash(normalize_ast(node))


def _truth_not(value: str) -> str:
    return {"FALSE": "TRUE", "TRUE": "FALSE", "UNKNOWN": "UNKNOWN"}[value]


def _truth_and(values: Iterable[str]) -> str:
    materialized = tuple(values)
    if "FALSE" in materialized:
        return "FALSE"
    if all(value == "TRUE" for value in materialized):
        return "TRUE"
    return "UNKNOWN"


def _truth_or(values: Iterable[str]) -> str:
    materialized = tuple(values)
    if "TRUE" in materialized:
        return "TRUE"
    if all(value == "FALSE" for value in materialized):
        return "FALSE"
    return "UNKNOWN"


def evaluate_interval(
    node: Any,
    variables: Mapping[str, RationalInterval],
    sqrt_precision_bits: int = 64,
) -> RationalInterval | str:
    """Evaluate a primitive AST with exact outward rational intervals."""
    ast = normalize_ast(node)
    environment: dict[str, RationalInterval] = {}
    for name, interval in variables.items():
        need(isinstance(name, str) and bool(NAME.fullmatch(name)), "interval variable name")
        need(isinstance(interval, RationalInterval), "interval environment value")
        environment[name] = interval

    def scalar(value: Mapping[str, Any]) -> RationalInterval:
        op = value["op"]
        if op == "CONST_Q":
            return RationalInterval.point(as_fraction(value["value"]))
        if op == "VAR":
            need(value["name"] in environment, "bound interval variable:" + value["name"])
            return environment[value["name"]]
        if op == "NEG":
            return -scalar(value["arg"])
        if op == "ADD":
            result = RationalInterval.point(0)
            for arg in value["args"]:
                result = result.add(scalar(arg))
            return result
        if op == "SUB":
            return scalar(value["left"]).sub(scalar(value["right"]))
        if op == "MUL":
            result = RationalInterval.point(1)
            for arg in value["args"]:
                result = result.mul(scalar(arg))
            return result
        if op == "DIV_NONZERO":
            return scalar(value["left"]).div_nonzero(scalar(value["right"]))
        if op == "SQUARE":
            return scalar(value["arg"]).square()
        if op == "SQRT_POSITIVE":
            return positive_sqrt_bounds(scalar(value["arg"]), sqrt_precision_bits)
        raise KernelError("predicate used as scalar interval")

    def predicate(value: Mapping[str, Any]) -> str:
        op = value["op"]
        if op in {"EQ_ZERO", "LT_ZERO", "GT_ZERO"}:
            interval = scalar(value["arg"])
            if op == "EQ_ZERO":
                if interval.lower == interval.upper == 0:
                    return "TRUE"
                if interval.upper < 0 or interval.lower > 0:
                    return "FALSE"
                return "UNKNOWN"
            if op == "LT_ZERO":
                if interval.upper < 0:
                    return "TRUE"
                if interval.lower >= 0:
                    return "FALSE"
                return "UNKNOWN"
            if interval.lower > 0:
                return "TRUE"
            if interval.upper <= 0:
                return "FALSE"
            return "UNKNOWN"
        if op == "AND":
            return _truth_and(predicate(arg) for arg in value["args"])
        if op == "OR_DISJOINT":
            return _truth_or(predicate(arg) for arg in value["args"])
        if op == "RESTRICT":
            return _truth_and((predicate(value["predicate"]), predicate(value["domain"])))
        raise KernelError("scalar used as interval predicate")

    return scalar(ast) if infer_ast_type(ast) == SCALAR else predicate(ast)


def substitute_ast(node: Any, substitutions: Mapping[str, Any]) -> dict[str, Any]:
    """Capture-free scalar-variable substitution in this binder-free AST."""
    ast = normalize_ast(node)
    replacements: dict[str, dict[str, Any]] = {}
    for name, expression in substitutions.items():
        need(isinstance(name, str) and bool(NAME.fullmatch(name)), "substitution name")
        normalized = normalize_ast(expression)
        need(infer_ast_type(normalized) == SCALAR, "substitution scalar expression")
        replacements[name] = normalized

    def replace(value: Mapping[str, Any]) -> dict[str, Any]:
        op = value["op"]
        if op == "VAR" and value["name"] in replacements:
            return deepcopy(replacements[value["name"]])
        if op in {"CONST_Q", "VAR"}:
            return dict(value)
        if op in {"NEG", "SQUARE", "SQRT_POSITIVE", "EQ_ZERO", "LT_ZERO", "GT_ZERO"}:
            return _node(op, arg=replace(value["arg"]))
        if op in {"ADD", "MUL", "AND", "OR_DISJOINT"}:
            return _node(op, args=[replace(arg) for arg in value["args"]])
        if op in {"SUB", "DIV_NONZERO"}:
            return _node(op, left=replace(value["left"]), right=replace(value["right"]))
        if op == "RESTRICT":
            return restrict(replace(value["predicate"]), replace(value["domain"]))
        raise AssertionError("unreachable substitution operator")

    return normalize_ast(replace(ast))


def _macro(name: str, **fields: Any) -> dict[str, Any]:
    need(name in MACRO_IDS, "known macro")
    return {"macro": name, **fields}


def OPEN_RATIONAL_BOX(bounds: Mapping[str, tuple[Any, Any]]) -> dict[str, Any]:
    need(isinstance(bounds, Mapping) and bool(bounds), "OPEN_RATIONAL_BOX bounds")
    rows: list[dict[str, Any]] = []
    for name in sorted(bounds):
        need(isinstance(name, str) and bool(NAME.fullmatch(name)), "box variable")
        pair = bounds[name]
        need(isinstance(pair, tuple) and len(pair) == 2, "box bound pair")
        lower = as_fraction(pair[0], "box lower")
        upper = as_fraction(pair[1], "box upper")
        need(lower < upper, "open box lower < upper")
        rows.append({"lower": rational_wire(lower), "upper": rational_wire(upper), "variable": name})
    return _macro("OPEN_RATIONAL_BOX", bounds=rows)


def STRICT_SIGN_CELL(factors: Sequence[tuple[Any, int]]) -> dict[str, Any]:
    need(isinstance(factors, Sequence) and not isinstance(factors, (str, bytes)), "sign factors")
    need(len(factors) >= 1, "STRICT_SIGN_CELL nonempty")
    rows: list[dict[str, Any]] = []
    for expression, sign in factors:
        need(sign in (-1, 1) and not isinstance(sign, bool), "strict sign is +/-1")
        normalized = normalize_ast(expression)
        need(infer_ast_type(normalized) == SCALAR, "strict sign scalar")
        rows.append({"factor": normalized, "sign": sign})
    return _macro("STRICT_SIGN_CELL", factors=rows)


def FINITE_DISJOINT_UNION(cells: Sequence[Any]) -> dict[str, Any]:
    need(isinstance(cells, Sequence) and not isinstance(cells, (str, bytes)), "union cells")
    need(len(cells) >= 2, "FINITE_DISJOINT_UNION arity")
    normalized = [normalize_ast(cell) for cell in cells]
    need(all(infer_ast_type(cell) == PREDICATE for cell in normalized), "union predicates")
    return _macro("FINITE_DISJOINT_UNION", cells=normalized)


def BOUNDARY_RESTRICTION(support: Any, boundary: Any) -> dict[str, Any]:
    return _macro(
        "BOUNDARY_RESTRICTION",
        boundary=normalize_ast(boundary),
        support=normalize_ast(support),
    )


def CHART_PULLBACK(predicate: Any, substitutions: Mapping[str, Any]) -> dict[str, Any]:
    normalized = normalize_ast(predicate)
    need(infer_ast_type(normalized) == PREDICATE, "pullback predicate")
    need(isinstance(substitutions, Mapping) and bool(substitutions), "pullback substitutions")
    rows: list[dict[str, Any]] = []
    for name in sorted(substitutions):
        replacement = normalize_ast(substitutions[name])
        need(infer_ast_type(replacement) == SCALAR, "pullback scalar substitution")
        rows.append({"expression": replacement, "variable": name})
    return _macro("CHART_PULLBACK", predicate=normalized, substitutions=rows)


def TPS_DOMAIN(
    t_bounds: tuple[Any, Any],
    p_bounds: tuple[Any, Any],
    s_bounds: tuple[Any, Any],
) -> dict[str, Any]:
    return _macro(
        "TPS_DOMAIN",
        p_bounds=[rational_wire(p_bounds[0]), rational_wire(p_bounds[1])],
        s_bounds=[rational_wire(s_bounds[0]), rational_wire(s_bounds[1])],
        t_bounds=[rational_wire(t_bounds[0]), rational_wire(t_bounds[1])],
    )


def SOURCE_G_FIRST_HIT_MAP(
    chart: str,
    target_kind: str,
    target_ix: Any,
    target_iy: Any,
    target_radius: Any,
    *,
    t: Any | None = None,
    p: Any | None = None,
    s: Any | None = None,
) -> dict[str, Any]:
    need(chart in {"E", "W", "N", "S"}, "Source-G chart")
    need(target_kind in {"G", "W"}, "Source-G target kind")
    ix = as_fraction(target_ix, "target ix")
    iy = as_fraction(target_iy, "target iy")
    radius = as_fraction(target_radius, "target radius")
    need(radius > 0, "target radius positive")
    t_ast = normalize_ast(var("t") if t is None else t)
    p_ast = normalize_ast(var("p") if p is None else p)
    s_ast = normalize_ast(var("s") if s is None else s)
    need(
        all(infer_ast_type(ast) == SCALAR for ast in (t_ast, p_ast, s_ast)),
        "Source-G scalar coordinates",
    )
    return _macro(
        "SOURCE_G_FIRST_HIT_MAP",
        chart=chart,
        p=p_ast,
        s=s_ast,
        t=t_ast,
        target_ix=rational_wire(ix),
        target_iy=rational_wire(iy),
        target_kind=target_kind,
        target_radius=rational_wire(radius),
    )


def WALL_ENDPOINT_FACTOR(point_coordinate: Any, wall_coordinate: Any) -> dict[str, Any]:
    point = normalize_ast(point_coordinate)
    wall = normalize_ast(wall_coordinate)
    need(infer_ast_type(point) == infer_ast_type(wall) == SCALAR, "wall scalar coordinates")
    return _macro("WALL_ENDPOINT_FACTOR", point=point, wall=wall)


def OUTGOING_DIAGONAL_FACTOR(vx: Any, vy: Any, branch: str = "PSI") -> dict[str, Any]:
    need(branch in {"H_PLUS", "H_MINUS", "PSI"}, "outgoing diagonal branch")
    x = normalize_ast(vx)
    y = normalize_ast(vy)
    need(infer_ast_type(x) == infer_ast_type(y) == SCALAR, "outgoing scalar components")
    return _macro("OUTGOING_DIAGONAL_FACTOR", branch=branch, vx=x, vy=y)


def IMPLICIT_REGULAR_GRAPH(
    domain: Any,
    equation: Any,
    graph_variable: str,
    base_variables: Sequence[str],
) -> dict[str, Any]:
    domain_ast = normalize_ast(domain)
    equation_ast = normalize_ast(equation)
    need(infer_ast_type(domain_ast) == PREDICATE, "graph domain predicate")
    need(infer_ast_type(equation_ast) == SCALAR, "graph equation scalar")
    need(isinstance(graph_variable, str) and bool(NAME.fullmatch(graph_variable)), "graph variable")
    need(
        isinstance(base_variables, Sequence)
        and not isinstance(base_variables, (str, bytes))
        and len(base_variables) >= 1
        and all(isinstance(name, str) and bool(NAME.fullmatch(name)) for name in base_variables),
        "base variables",
    )
    need(graph_variable not in base_variables, "graph variable is not base variable")
    need(len(set(base_variables)) == len(base_variables), "distinct base variables")
    return _macro(
        "IMPLICIT_REGULAR_GRAPH",
        base_variables=list(base_variables),
        domain=domain_ast,
        equation=equation_ast,
        graph_variable=graph_variable,
    )


def SHEET_MEMBER_EQUIVALENCE(graph_support: Any, member_support: Any) -> dict[str, Any]:
    graph = normalize_ast(graph_support)
    member = normalize_ast(member_support)
    need(infer_ast_type(graph) == infer_ast_type(member) == PREDICATE, "sheet equivalence predicates")
    return _macro("SHEET_MEMBER_EQUIVALENCE", graph_support=graph, member_support=member)


def BOUNDARY_TRACE_INCIDENCE(
    graph_support: Any,
    side_support: Any,
    boundary: Any,
) -> dict[str, Any]:
    graph = normalize_ast(graph_support)
    side = normalize_ast(side_support)
    boundary_ast = normalize_ast(boundary)
    need(
        all(infer_ast_type(item) == PREDICATE for item in (graph, side, boundary_ast)),
        "boundary trace predicates",
    )
    return _macro(
        "BOUNDARY_TRACE_INCIDENCE",
        boundary=boundary_ast,
        graph_support=graph,
        side_support=side,
    )


def HALF_OPEN_BOUNDARY_ASSIGNMENT(interior: Any, owned_boundary: Any) -> dict[str, Any]:
    interior_ast = normalize_ast(interior)
    boundary_ast = normalize_ast(owned_boundary)
    need(
        infer_ast_type(interior_ast) == infer_ast_type(boundary_ast) == PREDICATE,
        "half-open predicates",
    )
    return _macro(
        "HALF_OPEN_BOUNDARY_ASSIGNMENT",
        interior=interior_ast,
        owned_boundary=boundary_ast,
    )


def _macro_exact(value: Mapping[str, Any], fields: set[str], macro_id: str) -> None:
    need(set(value) == {"macro", *fields}, macro_id + " exact keys")
    need(value.get("macro") == macro_id, macro_id + " tag")


def _pred_and(items: Sequence[dict[str, Any]]) -> dict[str, Any]:
    need(bool(items), "predicate conjunction nonempty")
    return items[0] if len(items) == 1 else normalize_ast(and_pred(*items))


def lower_macro(value: Any) -> dict[str, Any]:
    """Lower a named macro to primitive ASTs or a zero-credit obligation frame."""
    need(isinstance(value, Mapping), "macro object")
    macro_id = value.get("macro")
    need(isinstance(macro_id, str) and macro_id in MACRO_IDS, "known macro tag")
    if macro_id == "OPEN_RATIONAL_BOX":
        _macro_exact(value, {"bounds"}, macro_id)
        bounds = value["bounds"]
        need(isinstance(bounds, list) and bool(bounds), "box bound rows")
        predicates: list[dict[str, Any]] = []
        names: list[str] = []
        for row in bounds:
            need(isinstance(row, Mapping), "box bound row")
            _exact_keys(row, {"lower", "upper", "variable"}, "box bound row")
            name = row["variable"]
            need(isinstance(name, str) and bool(NAME.fullmatch(name)), "box bound variable")
            lo = as_fraction(row["lower"], "box lower")
            hi = as_fraction(row["upper"], "box upper")
            need(lo < hi, "box lower < upper")
            names.append(name)
            coordinate = var(name)
            predicates.extend((lt_zero(sub(const_q(lo), coordinate)), lt_zero(sub(coordinate, const_q(hi)))))
        need(names == sorted(names) and len(set(names)) == len(names), "canonical box variables")
        return _pred_and([normalize_ast(item) for item in predicates])
    if macro_id == "STRICT_SIGN_CELL":
        _macro_exact(value, {"factors"}, macro_id)
        rows = value["factors"]
        need(isinstance(rows, list) and bool(rows), "sign factor rows")
        predicates = []
        for row in rows:
            need(isinstance(row, Mapping), "sign factor row")
            _exact_keys(row, {"factor", "sign"}, "sign factor row")
            factor = normalize_ast(row["factor"])
            need(infer_ast_type(factor) == SCALAR, "sign factor scalar")
            need(row["sign"] in (-1, 1) and not isinstance(row["sign"], bool), "factor sign")
            predicates.append(gt_zero(factor) if row["sign"] == 1 else lt_zero(factor))
        return _pred_and([normalize_ast(item) for item in predicates])
    if macro_id == "FINITE_DISJOINT_UNION":
        _macro_exact(value, {"cells"}, macro_id)
        cells = value["cells"]
        need(isinstance(cells, list) and len(cells) >= 2, "finite union cells")
        return normalize_ast(or_disjoint(*(normalize_ast(cell) for cell in cells)))
    if macro_id == "BOUNDARY_RESTRICTION":
        _macro_exact(value, {"boundary", "support"}, macro_id)
        boundary = normalize_ast(value["boundary"])
        support = normalize_ast(value["support"])
        need(infer_ast_type(boundary) == infer_ast_type(support) == PREDICATE, "boundary restriction")
        return normalize_ast(restrict(support, boundary))
    if macro_id == "CHART_PULLBACK":
        _macro_exact(value, {"predicate", "substitutions"}, macro_id)
        predicate = normalize_ast(value["predicate"])
        need(infer_ast_type(predicate) == PREDICATE, "pullback predicate")
        rows = value["substitutions"]
        need(isinstance(rows, list) and bool(rows), "pullback rows")
        replacements: dict[str, Any] = {}
        for row in rows:
            need(isinstance(row, Mapping), "pullback row")
            _exact_keys(row, {"expression", "variable"}, "pullback row")
            name = row["variable"]
            need(isinstance(name, str) and bool(NAME.fullmatch(name)), "pullback variable")
            need(name not in replacements, "unique pullback variable")
            replacements[name] = row["expression"]
        need(list(replacements) == sorted(replacements), "canonical pullback order")
        return substitute_ast(predicate, replacements)
    if macro_id == "TPS_DOMAIN":
        _macro_exact(value, {"p_bounds", "s_bounds", "t_bounds"}, macro_id)
        parsed: dict[str, tuple[Fraction, Fraction]] = {}
        for name in ("t", "p", "s"):
            pair = value[name + "_bounds"]
            need(isinstance(pair, list) and len(pair) == 2, "TPS bound pair")
            parsed[name] = (as_fraction(pair[0]), as_fraction(pair[1]))
        return lower_macro(OPEN_RATIONAL_BOX(parsed))
    if macro_id == "SOURCE_G_FIRST_HIT_MAP":
        _macro_exact(
            value,
            {"chart", "p", "s", "t", "target_ix", "target_iy", "target_kind", "target_radius"},
            macro_id,
        )
        chart = value["chart"]
        target_kind = value["target_kind"]
        need(chart in {"E", "W", "N", "S"}, "Source-G chart")
        need(target_kind in {"G", "W"}, "Source-G target kind")
        t_ast = normalize_ast(value["t"])
        p_ast = normalize_ast(value["p"])
        s_ast = normalize_ast(value["s"])
        need(
            all(infer_ast_type(item) == SCALAR for item in (t_ast, p_ast, s_ast)),
            "Source-G coordinates",
        )
        ix = as_fraction(value["target_ix"], "target ix")
        iy = as_fraction(value["target_iy"], "target iy")
        radius_q = as_fraction(value["target_radius"], "target radius")
        need(radius_q > 0, "target radius positive")
        one = const_q(1)
        rn = normalize_ast(sqrt_positive(sub(one, square(t_ast))))
        rp = normalize_ast(sqrt_positive(sub(one, square(p_ast))))
        if chart == "E":
            nx, ny = rn, t_ast
        elif chart == "W":
            nx, ny = normalize_ast(neg(rn)), t_ast
        elif chart == "N":
            nx, ny = t_ast, rn
        else:
            nx, ny = t_ast, normalize_ast(neg(rn))
        ux = normalize_ast(sub(mul(rp, nx), mul(p_ast, ny)))
        uy = normalize_ast(add(mul(rp, ny), mul(p_ast, nx)))
        qx = normalize_ast(mul(const_q(Fraction(9, 25)), nx))
        qy = normalize_ast(mul(const_q(Fraction(9, 25)), ny))
        if target_kind == "G":
            cx = const_q(ix)
            cy = const_q(iy)
        else:
            cx = normalize_ast(add(const_q(ix + Fraction(1, 2)), s_ast))
            cy = const_q(iy + Fraction(1, 2))
        dx = normalize_ast(sub(cx, qx))
        dy = normalize_ast(sub(cy, qy))
        z = normalize_ast(add(neg(mul(uy, dx)), mul(ux, dy)))
        radius = const_q(radius_q)
        delta = normalize_ast(sub(square(radius), square(z)))
        sqrt_delta = normalize_ast(sqrt_positive(delta))
        vx = normalize_ast(
            div_nonzero(add(neg(mul(sqrt_delta, ux)), mul(z, uy)), radius)
        )
        vy = normalize_ast(
            div_nonzero(sub(neg(mul(sqrt_delta, uy)), mul(z, ux)), radius)
        )
        hit_x = normalize_ast(add(cx, mul(radius, vx)))
        hit_y = normalize_ast(add(cy, mul(radius, vy)))
        h_plus = normalize_ast(add(vx, vy))
        h_minus = normalize_ast(sub(vx, vy))
        psi = normalize_ast(sub(square(vx), square(vy)))
        fields = {
            "center_x": cx,
            "center_y": cy,
            "delta": delta,
            "h_minus": h_minus,
            "h_plus": h_plus,
            "hit_x": hit_x,
            "hit_y": hit_y,
            "normal_x": nx,
            "normal_y": ny,
            "psi": psi,
            "q_x": qx,
            "q_y": qy,
            "radius": radius,
            "rn": rn,
            "rp": rp,
            "sqrt_delta": sqrt_delta,
            "tangent_x": ux,
            "tangent_y": uy,
            "transverse_z": z,
            "v_x": vx,
            "v_y": vy,
        }
        need(all(infer_ast_type(item) == SCALAR for item in fields.values()), "formula scalar map")
        return {
            "chart": chart,
            "fields": fields,
            "lowered_kind": "SOURCE_G_SCALAR_MAP",
            "target_kind": target_kind,
            "theorem_credit": 0,
        }
    if macro_id == "WALL_ENDPOINT_FACTOR":
        _macro_exact(value, {"point", "wall"}, macro_id)
        point = normalize_ast(value["point"])
        wall = normalize_ast(value["wall"])
        need(infer_ast_type(point) == infer_ast_type(wall) == SCALAR, "wall factor scalars")
        return normalize_ast(sub(point, wall))
    if macro_id == "OUTGOING_DIAGONAL_FACTOR":
        _macro_exact(value, {"branch", "vx", "vy"}, macro_id)
        branch = value["branch"]
        need(branch in {"H_PLUS", "H_MINUS", "PSI"}, "diagonal branch")
        vx = normalize_ast(value["vx"])
        vy = normalize_ast(value["vy"])
        need(infer_ast_type(vx) == infer_ast_type(vy) == SCALAR, "diagonal components")
        if branch == "H_PLUS":
            return normalize_ast(add(vx, vy))
        if branch == "H_MINUS":
            return normalize_ast(sub(vx, vy))
        return normalize_ast(sub(square(vx), square(vy)))
    if macro_id == "IMPLICIT_REGULAR_GRAPH":
        _macro_exact(value, {"base_variables", "domain", "equation", "graph_variable"}, macro_id)
        domain = normalize_ast(value["domain"])
        equation = normalize_ast(value["equation"])
        need(infer_ast_type(domain) == PREDICATE, "graph domain")
        need(infer_ast_type(equation) == SCALAR, "graph equation")
        graph_variable = value["graph_variable"]
        base_variables = value["base_variables"]
        need(isinstance(graph_variable, str) and bool(NAME.fullmatch(graph_variable)), "graph variable")
        need(
            isinstance(base_variables, list)
            and bool(base_variables)
            and len(set(base_variables)) == len(base_variables)
            and all(isinstance(name, str) and bool(NAME.fullmatch(name)) for name in base_variables),
            "graph base variables",
        )
        need(graph_variable not in base_variables, "graph/base separation")
        return {
            "base_variables": list(base_variables),
            "equation": equation,
            "graph_variable": graph_variable,
            "lowered_kind": "IMPLICIT_REGULAR_GRAPH_FRAME",
            "support": normalize_ast(restrict(eq_zero(equation), domain)),
            "theorem_credit": 0,
        }
    if macro_id == "SHEET_MEMBER_EQUIVALENCE":
        _macro_exact(value, {"graph_support", "member_support"}, macro_id)
        graph = normalize_ast(value["graph_support"])
        member = normalize_ast(value["member_support"])
        need(infer_ast_type(graph) == infer_ast_type(member) == PREDICATE, "sheet equivalence")
        return {
            "left_support": graph,
            "lowered_kind": "BIDIRECTIONAL_SET_EQUALITY_OBLIGATION",
            "right_support": member,
            "theorem_credit": 0,
        }
    if macro_id == "BOUNDARY_TRACE_INCIDENCE":
        _macro_exact(value, {"boundary", "graph_support", "side_support"}, macro_id)
        boundary = normalize_ast(value["boundary"])
        graph = normalize_ast(value["graph_support"])
        side = normalize_ast(value["side_support"])
        need(
            all(infer_ast_type(item) == PREDICATE for item in (boundary, graph, side)),
            "boundary incidence predicates",
        )
        return {
            "boundary": boundary,
            "graph_trace": normalize_ast(restrict(graph, boundary)),
            "lowered_kind": "PHYSICAL_BOUNDARY_TRACE_OBLIGATION",
            "side_trace": normalize_ast(restrict(side, boundary)),
            "theorem_credit": 0,
        }
    if macro_id == "HALF_OPEN_BOUNDARY_ASSIGNMENT":
        _macro_exact(value, {"interior", "owned_boundary"}, macro_id)
        interior = normalize_ast(value["interior"])
        owned = normalize_ast(value["owned_boundary"])
        need(infer_ast_type(interior) == infer_ast_type(owned) == PREDICATE, "half-open predicates")
        return normalize_ast(or_disjoint(interior, owned))
    raise AssertionError("unreachable macro")


def fixed_sign_t2ps(sigma: int, u: Any) -> dict[str, Any]:
    """Exact fixed-sign T2PS pullback t = sigma * sqrt(u)."""
    need(sigma in (-1, 1) and not isinstance(sigma, bool), "T2PS sigma")
    u_ast = normalize_ast(u)
    need(infer_ast_type(u_ast) == SCALAR, "T2PS u scalar")
    return normalize_ast(mul(const_q(sigma), sqrt_positive(u_ast)))


def source_g_formula_map(
    chart: str,
    target_kind: str,
    target_ix: Any,
    target_iy: Any,
    target_radius: Any,
) -> dict[str, Any]:
    """Convenience constructor followed by deterministic macro lowering."""
    return lower_macro(
        SOURCE_G_FIRST_HIT_MAP(chart, target_kind, target_ix, target_iy, target_radius)
    )


# These are wire-shape declarations, not proof implementations.  A future
# independent verifier must interpret and discharge the evidence.
PROOF_KERNEL_SHAPES: dict[str, dict[str, dict[str, str]]] = {
    "EXACT_RATIONAL_AST_NORMALIZATION_V2": {
        "premises": {"input_ast": "ANY_AST"},
        "evidence": {"normalization_rule_ids": "STR_LIST"},
        "conclusion": {"normalized_ast": "ANY_AST", "normalized_sha256": "SHA256"},
    },
    "DIRECTED_RATIONAL_INTERVAL_SIGN_V1": {
        "premises": {"scalar_ast": "SCALAR_AST", "variable_intervals": "INTERVAL_MAP"},
        "evidence": {
            "precision_bits": "SQRT_BITS",
            "rounding_mode": "LITERAL:OUTWARD_EXACT_RATIONAL",
            "subdivision_path": "STR_LIST",
        },
        "conclusion": {"interval": "INTERVAL", "sign": "SIGN"},
    },
    "POSITIVE_SQRT_INTERVAL_V1": {
        "premises": {"radicand_interval": "INTERVAL"},
        "evidence": {
            "method": "LITERAL:INTEGER_SQUARE_BRACKETING",
            "precision_bits": "SQRT_BITS",
        },
        "conclusion": {"sqrt_interval": "INTERVAL"},
    },
    "PREDICATE_CELL_EQUIVALENCE_V1": {
        "premises": {
            "domain": "PREDICATE_AST",
            "left_predicate": "PREDICATE_AST",
            "right_predicate": "PREDICATE_AST",
        },
        "evidence": {
            "cell_ids": "STR_LIST",
            "forward_certificate_ids": "STR_LIST",
            "reverse_certificate_ids": "STR_LIST",
        },
        "conclusion": {"equivalence_claim": "BOOL_TRUE"},
    },
    "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1": {
        "premises": {
            "derivative_ast": "SCALAR_AST",
            "domain": "PREDICATE_AST",
            "equation_ast": "SCALAR_AST",
        },
        "evidence": {
            "base_variables": "STR_LIST",
            "derivative_sign": "STRICT_SIGN",
            "face_signs": "STR_MAP",
            "graph_variable": "STR",
            "interval_cell_ids": "STR_LIST",
        },
        "conclusion": {"existence_claim": "BOOL_TRUE", "uniqueness_claim": "BOOL_TRUE"},
    },
    "DEPENDENT_INCIDENCE_RESTRICTION_V1": {
        "premises": {
            "boundary": "PREDICATE_AST",
            "dependent_support": "PREDICATE_AST",
            "root_support": "PREDICATE_AST",
        },
        "evidence": {
            "orientation": "ORIENTATION",
            "restriction_ast": "PREDICATE_AST",
            "trace_certificate_ids": "STR_LIST",
        },
        "conclusion": {"exact_restriction_claim": "BOOL_TRUE"},
    },
    "FINITE_HALF_OPEN_SUPPORT_UNION_V1": {
        "premises": {"pieces": "PREDICATE_LIST"},
        "evidence": {
            "owner_rule_ids": "STR_LIST",
            "pairwise_disjoint_certificate_ids": "STR_LIST",
            "piece_ids": "STR_LIST",
        },
        "conclusion": {"complete_claim": "BOOL_TRUE", "support": "PREDICATE_AST"},
    },
    "ARTIFICIAL_FACE_REGLUE_V1": {
        "premises": {
            "common_face": "PREDICATE_AST",
            "left_cell": "PREDICATE_AST",
            "right_cell": "PREDICATE_AST",
        },
        "evidence": {
            "left_trace_sha256": "SHA256",
            "owner_rule_id": "STR",
            "right_trace_sha256": "SHA256",
        },
        "conclusion": {"no_duplicate_claim": "BOOL_TRUE", "reglued_support": "PREDICATE_AST"},
    },
    "FIXED_SIGN_T2PS_PULLBACK_V1": {
        "premises": {"sigma": "SIGMA", "t_ast": "SCALAR_AST", "u_ast": "SCALAR_AST"},
        "evidence": {
            "substitution_variable": "STR",
            "u_positive_certificate_id": "STR",
        },
        "conclusion": {"pullback_predicate": "PREDICATE_AST"},
    },
    "REPRESENTATION_OWNER_BACKBINDING_V1": {
        "premises": {
            "member_support": "PREDICATE_AST",
            "representation_support": "PREDICATE_AST",
        },
        "evidence": {
            "member_id": "STR",
            "owner_id": "STR",
            "representation_id": "STR",
            "source_join_id": "STR",
        },
        "conclusion": {"supports_equal_claim": "BOOL_TRUE"},
    },
    "SHEET_MEMBER_EQUIVALENCE_V1": {
        "premises": {"graph_support": "PREDICATE_AST", "sheet_support": "PREDICATE_AST"},
        "evidence": {
            "forward_certificate_ids": "STR_LIST",
            "graph_id": "STR",
            "member_id": "STR",
            "reverse_certificate_ids": "STR_LIST",
        },
        "conclusion": {"sets_equal_claim": "BOOL_TRUE"},
    },
    "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1": {
        "premises": {
            "boundary": "PREDICATE_AST",
            "graph_support": "PREDICATE_AST",
            "side_support": "PREDICATE_AST",
        },
        "evidence": {
            "incidence_id": "STR",
            "orientation": "ORIENTATION",
            "trace_certificate_ids": "STR_LIST",
        },
        "conclusion": {"exact_physical_incidence_claim": "BOOL_TRUE"},
    },
    "SOURCE_LINEAGE_EXHAUSTION_V1": {
        "premises": {
            "join_ids": "STR_LIST",
            "member_ids": "STR_LIST",
            "source_ids": "STR_LIST",
        },
        "evidence": {
            "exhaustiveness_sha256": "SHA256",
            "join_count": "NONNEG_INT",
            "member_count": "NONNEG_INT",
            "source_count": "NONNEG_INT",
        },
        "conclusion": {
            "duplicate_count": "ZERO",
            "missing_count": "ZERO",
            "orphan_count": "ZERO",
        },
    },
}


def _interval_from_value(value: Any, label: str) -> RationalInterval:
    if isinstance(value, RationalInterval):
        return value
    try:
        return RationalInterval.from_wire(value)
    except KernelError as error:
        raise KernelError(label + ":" + str(error)) from error


def _check_shape(kind: str, value: Any, label: str) -> None:
    if kind == "ANY_AST":
        infer_ast_type(value)
        return
    if kind == "SCALAR_AST":
        need(infer_ast_type(value) == SCALAR, label + " scalar AST")
        return
    if kind == "PREDICATE_AST":
        need(infer_ast_type(value) == PREDICATE, label + " predicate AST")
        return
    if kind == "PREDICATE_LIST":
        need(isinstance(value, list) and len(value) >= 2, label + " predicate list")
        need(all(infer_ast_type(item) == PREDICATE for item in value), label + " predicate items")
        return
    if kind == "INTERVAL":
        _interval_from_value(value, label)
        return
    if kind == "INTERVAL_MAP":
        need(isinstance(value, Mapping), label + " interval map")
        need(all(isinstance(key, str) and bool(NAME.fullmatch(key)) for key in value), label + " names")
        for key, interval in value.items():
            _interval_from_value(interval, label + "." + key)
        return
    if kind == "STR":
        need(isinstance(value, str) and bool(IDENTIFIER.fullmatch(value)), label + " identifier")
        return
    if kind == "STR_LIST":
        need(
            isinstance(value, list)
            and bool(value)
            and all(isinstance(item, str) and bool(IDENTIFIER.fullmatch(item)) for item in value),
            label + " identifier list",
        )
        need(len(set(value)) == len(value), label + " distinct identifiers")
        return
    if kind == "STR_MAP":
        need(
            isinstance(value, Mapping)
            and bool(value)
            and all(
                isinstance(key, str)
                and bool(IDENTIFIER.fullmatch(key))
                and isinstance(item, str)
                and bool(IDENTIFIER.fullmatch(item))
                for key, item in value.items()
            ),
            label + " identifier map",
        )
        return
    if kind == "SHA256":
        need(isinstance(value, str) and bool(HEX64.fullmatch(value)), label + " SHA256")
        return
    if kind == "SQRT_BITS":
        need(
            isinstance(value, int)
            and not isinstance(value, bool)
            and 1 <= value <= MAX_SQRT_BITS,
            label + " sqrt bits",
        )
        return
    if kind == "NONNEG_INT":
        need(isinstance(value, int) and not isinstance(value, bool) and value >= 0, label + " nonnegative")
        return
    if kind == "ZERO":
        need(value == 0 and not isinstance(value, bool), label + " zero")
        return
    if kind == "BOOL_TRUE":
        need(value is True, label + " true assertion shape")
        return
    if kind == "SIGN":
        need(value in {"NEGATIVE", "ZERO", "POSITIVE", "UNRESOLVED"}, label + " sign")
        return
    if kind == "STRICT_SIGN":
        need(value in {"NEGATIVE", "POSITIVE"}, label + " strict sign")
        return
    if kind == "SIGMA":
        need(value in (-1, 1) and not isinstance(value, bool), label + " sigma")
        return
    if kind == "ORIENTATION":
        need(
            value in {"INWARD", "OUTWARD", "OWNER", "SHADOW", "BIDIRECTIONAL"},
            label + " orientation",
        )
        return
    if kind.startswith("LITERAL:"):
        need(value == kind.split(":", 1)[1], label + " literal")
        return
    raise AssertionError("unknown proof shape kind:" + kind)


def _exact_section(
    section: Any,
    shape: Mapping[str, str],
    label: str,
) -> Mapping[str, Any]:
    need(isinstance(section, Mapping), label + " object")
    need(set(section) == set(shape), label + " exact keys")
    for field, kind in shape.items():
        _check_shape(kind, section[field], label + "." + field)
    return section


def _interval_sign(interval: RationalInterval) -> str:
    if interval.upper < 0:
        return "NEGATIVE"
    if interval.lower > 0:
        return "POSITIVE"
    if interval.lower == interval.upper == 0:
        return "ZERO"
    return "UNRESOLVED"


def validate_proof_payload(payload: Any) -> dict[str, Any]:
    """Validate syntax/type/evidence shape; never validate a theorem."""
    need(isinstance(payload, Mapping), "proof payload object")
    need(
        set(payload) == {"claim_id", "conclusion", "evidence", "kernel_id", "premises", "theorem_credit"},
        "proof payload exact keys",
    )
    kernel_id = payload["kernel_id"]
    need(isinstance(kernel_id, str) and kernel_id in PROOF_KERNEL_IDS, "proof kernel ID")
    need(
        isinstance(payload["claim_id"], str)
        and bool(IDENTIFIER.fullmatch(payload["claim_id"])),
        "claim ID",
    )
    need(payload["theorem_credit"] == 0 and not isinstance(payload["theorem_credit"], bool), "zero theorem credit")
    shape = PROOF_KERNEL_SHAPES[kernel_id]
    premises = _exact_section(payload["premises"], shape["premises"], "premises")
    evidence = _exact_section(payload["evidence"], shape["evidence"], "evidence")
    conclusion = _exact_section(payload["conclusion"], shape["conclusion"], "conclusion")

    # The following checks are exact symbolic recomputations or bookkeeping
    # consistency only.  None discharges the mathematical evidence strings.
    if kernel_id == "EXACT_RATIONAL_AST_NORMALIZATION_V2":
        normalized = normalize_ast(premises["input_ast"])
        need(canonical_json(normalized) == canonical_json(conclusion["normalized_ast"]), "normalization result")
        need(ast_hash(normalized) == conclusion["normalized_sha256"], "normalization digest")
    elif kernel_id == "DIRECTED_RATIONAL_INTERVAL_SIGN_V1":
        environment = {
            name: _interval_from_value(interval, "variable interval")
            for name, interval in premises["variable_intervals"].items()
        }
        computed = evaluate_interval(
            premises["scalar_ast"],
            environment,
            evidence["precision_bits"],
        )
        need(isinstance(computed, RationalInterval), "directed interval scalar result")
        claimed = _interval_from_value(conclusion["interval"], "claimed interval")
        need(computed == claimed, "directed interval exact result")
        need(_interval_sign(computed) == conclusion["sign"], "directed interval sign")
    elif kernel_id == "POSITIVE_SQRT_INTERVAL_V1":
        radicand = _interval_from_value(premises["radicand_interval"], "sqrt radicand")
        computed = positive_sqrt_bounds(radicand, evidence["precision_bits"])
        claimed = _interval_from_value(conclusion["sqrt_interval"], "sqrt conclusion")
        need(computed == claimed, "positive sqrt exact bounds")
    elif kernel_id == "FINITE_HALF_OPEN_SUPPORT_UNION_V1":
        pieces = [normalize_ast(item) for item in premises["pieces"]]
        need(len(evidence["piece_ids"]) == len(pieces), "piece ID count")
        computed_support = normalize_ast(or_disjoint(*pieces))
        need(canonical_json(computed_support) == canonical_json(normalize_ast(conclusion["support"])), "union support")
    elif kernel_id == "ARTIFICIAL_FACE_REGLUE_V1":
        computed_support = normalize_ast(
            or_disjoint(premises["left_cell"], premises["right_cell"])
        )
        need(
            canonical_json(computed_support)
            == canonical_json(normalize_ast(conclusion["reglued_support"])),
            "reglued support syntax",
        )
    elif kernel_id == "FIXED_SIGN_T2PS_PULLBACK_V1":
        expected_t = fixed_sign_t2ps(premises["sigma"], premises["u_ast"])
        need(canonical_json(expected_t) == canonical_json(normalize_ast(premises["t_ast"])), "fixed-sign t")
    elif kernel_id == "SOURCE_LINEAGE_EXHAUSTION_V1":
        need(evidence["source_count"] == len(premises["source_ids"]), "source count")
        need(evidence["join_count"] == len(premises["join_ids"]), "join count")
        need(evidence["member_count"] == len(premises["member_ids"]), "member count")

    summary = {
        "claim_id": payload["claim_id"],
        "kernel_id": kernel_id,
        "payload_sha256": canonical_hash(payload),
        "status": "VALID_SYNTAX_TYPE_AND_EVIDENCE_SHAPE_ONLY",
        "theorem_credit": 0,
    }
    return {**summary, "validation_sha256": canonical_hash(summary)}


def _formula_commitments() -> dict[str, Any]:
    g_map = source_g_formula_map("E", "G", 0, 0, Fraction(1, 4))
    w_map = source_g_formula_map("N", "W", -1, 2, Fraction(1, 3))
    return {
        "chart_normal_cases": {
            "E": ["sqrt(1-t^2)", "t"],
            "N": ["t", "sqrt(1-t^2)"],
            "S": ["t", "-sqrt(1-t^2)"],
            "W": ["-sqrt(1-t^2)", "t"],
        },
        "explicit_formula_strings": {
            "Delta": "r^2-z^2",
            "G_center": "(ix,iy)",
            "H_minus": "vx-vy",
            "H_plus": "vx+vy",
            "W_center": "(ix+1/2+s,iy+1/2)",
            "hit": "c+r*v",
            "normal_radius": "rn=sqrt(1-t^2)",
            "outgoing_vx": "(-sqrt(Delta)*ux+z*uy)/r",
            "outgoing_vy": "(-sqrt(Delta)*uy-z*ux)/r",
            "psi": "vx^2-vy^2",
            "q": "(9/25)*n",
            "tangent": "u=(rp*nx-p*ny,rp*ny+p*nx)",
            "tangent_radius": "rp=sqrt(1-p^2)",
            "transverse": "z=-uy*(cx-qx)+ux*(cy-qy)",
        },
        "fixed_sign_T2PS": "t=sigma*sqrt(u), sigma in {-1,+1}",
        "g_formula_field_names": sorted(g_map["fields"]),
        "g_formula_map_sha256": canonical_hash(g_map),
        "w_formula_field_names": sorted(w_map["fields"]),
        "w_formula_map_sha256": canonical_hash(w_map),
    }


def _kernel_body() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "scope": {
            "data_constructor": False,
            "imports_or_executes_upstream_code": False,
            "opens_upstream_data": False,
            "source_free": True,
            "symbolic_foundation_only": True,
        },
        "public_modes": {
            "default": "SILENT_SUCCESS_NO_OUTPUT",
            "print": "--print-kernel-contract",
            "self_test": "--self-test",
            "all_other_modes": "SILENT_REFUSAL_BEFORE_FILESYSTEM_OR_OUTPUT",
        },
        "type_system": {
            "primitive_sorts": [SCALAR, PREDICATE],
            "operator_field_is_discriminating_tag": True,
            "exact_node_keys_required": True,
            "binary_float_rejected": True,
            "maximum_depth": MAX_AST_DEPTH,
            "maximum_nodes": MAX_AST_NODES,
            "maximum_rational_bits": MAX_RATIONAL_BITS,
        },
        "normalization": {
            "kernel_id": "EXACT_RATIONAL_AST_NORMALIZATION_V2",
            "canonical_JSON": "ASCII_SORTED_KEYS_NO_WHITESPACE_NO_NAN",
            "hash": "SHA256_CANONICAL_JSON",
            "rational_reduction": "fractions.Fraction canonical numerator/positive denominator",
            "ADD_MUL": "recursive flatten, exact constant fold, identity removal, canonical child sort",
            "NEG_SQUARE": "exact fold and canonical involution/sign removal",
            "AND": "recursive flatten, canonical sort, idempotent duplicate removal",
            "OR_DISJOINT": "recursive flatten, canonical sort, duplicate rejection",
            "SUB_DIV_NONZERO_SQRT_POSITIVE": "exact safe folds only; otherwise preserved",
        },
        "rational_interval_arithmetic": {
            "closed_intervals": True,
            "exact_operations": ["NEG", "ADD", "SUB", "MUL", "DIV_NONZERO", "SQUARE"],
            "division_requires_interval_exclude_zero": True,
            "positive_sqrt_requires_strictly_positive_lower_bound": True,
            "sqrt_bound_method": "integer square bracketing on a 2^precision_bits grid",
            "sqrt_precision_bits_range": [1, MAX_SQRT_BITS],
            "outward_guarantees": ["lower^2<=radicand.lower", "upper^2>=radicand.upper"],
            "truth_lattice": list(TRUTH_VALUES),
        },
        "baseline_operators": list(BASELINE_OPERATORS),
        "macro_contract": {
            "macro_ids": list(MACRO_IDS),
            "macro_nodes_are_not_primitive_AST": True,
            "all_macros_require_explicit_lowering": True,
            "AST_lowering": [
                "OPEN_RATIONAL_BOX",
                "STRICT_SIGN_CELL",
                "FINITE_DISJOINT_UNION",
                "BOUNDARY_RESTRICTION",
                "CHART_PULLBACK",
                "TPS_DOMAIN",
                "WALL_ENDPOINT_FACTOR",
                "OUTGOING_DIAGONAL_FACTOR",
                "HALF_OPEN_BOUNDARY_ASSIGNMENT",
            ],
            "frame_or_map_lowering": [
                "SOURCE_G_FIRST_HIT_MAP",
                "IMPLICIT_REGULAR_GRAPH",
                "SHEET_MEMBER_EQUIVALENCE",
                "BOUNDARY_TRACE_INCIDENCE",
            ],
            "relation_frames_are_obligations_not_boolean_proofs": True,
        },
        "source_g_formula_commitments": _formula_commitments(),
        "proof_payload_contract": {
            "kernel_ids": list(PROOF_KERNEL_IDS),
            "shapes": PROOF_KERNEL_SHAPES,
            "validator_scope": "SYNTAX_TYPE_EXACT_RECOMPUTATION_AND_EVIDENCE_SHAPE_ONLY",
            "evidence_strings_are_not_mathematical_proofs": True,
            "producer_independence_not_claimed_by_this_file": True,
        },
        "security_boundary": {
            "allowed_imports": "PYTHON_STDLIB_ONLY",
            "candidate_mode": False,
            "production_mode": False,
            "refusal_before": [
                "path_lstat",
                "os_open",
                "builtin_open",
                "temporary_creation",
                "filesystem_write",
                "stdout",
                "stderr",
            ],
        },
        "formal_credit": {
            "feature_definition": 0,
            "full_support": 0,
            "representation_cover": 0,
            "theorem": 0,
            "transition": 0,
            "pair_routing": 0,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "emission_accounting": {
            "upstream_files_opened": 0,
            "candidate_files_created": 0,
            "production_files_created": 0,
            "support_rows_emitted": 0,
            "theorem_credit_minted": 0,
        },
    }


def validate_kernel_contract(document: Any) -> None:
    need(isinstance(document, Mapping), "kernel contract object")
    need(set(document) == set(_kernel_body()) | {"kernel_digest"}, "kernel contract exact keys")
    expected = _kernel_body()
    actual_body = {key: document[key] for key in expected}
    need(canonical_json(actual_body) == canonical_json(expected), "frozen kernel contract body")
    need(
        isinstance(document["kernel_digest"], str)
        and bool(HEX64.fullmatch(document["kernel_digest"])),
        "kernel digest shape",
    )
    need(document["kernel_digest"] == canonical_hash(actual_body), "kernel digest")


def kernel_contract() -> dict[str, Any]:
    body = _kernel_body()
    document = {**body, "kernel_digest": canonical_hash(body)}
    validate_kernel_contract(document)
    return document


def _proof_payload(
    kernel_id: str,
    premises: Mapping[str, Any],
    evidence: Mapping[str, Any],
    conclusion: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "claim_id": "selftest." + kernel_id.lower(),
        "conclusion": dict(conclusion),
        "evidence": dict(evidence),
        "kernel_id": kernel_id,
        "premises": dict(premises),
        "theorem_credit": 0,
    }


def _sample_proof_payloads() -> dict[str, dict[str, Any]]:
    x = var("x")
    u = var("u")
    left = normalize_ast(lt_zero(x))
    right = normalize_ast(gt_zero(x))
    domain = normalize_ast(gt_zero(add(x, const_q(1))))
    boundary = normalize_ast(eq_zero(x))
    union = normalize_ast(or_disjoint(left, right))
    input_ast = add(x, const_q(0))
    normalized = normalize_ast(input_ast)
    interval_expression = normalize_ast(add(x, const_q(1)))
    variable_intervals = {"x": RationalInterval(Fraction(1), Fraction(2)).to_wire()}
    interval_result = evaluate_interval(
        interval_expression,
        {"x": RationalInterval(Fraction(1), Fraction(2))},
        32,
    )
    assert isinstance(interval_result, RationalInterval)
    radicand = RationalInterval(Fraction(1), Fraction(4))
    sqrt_result = positive_sqrt_bounds(radicand, 32)
    fixed_t = fixed_sign_t2ps(-1, u)
    hash_a = "a" * 64
    hash_b = "b" * 64
    payloads = {
        "EXACT_RATIONAL_AST_NORMALIZATION_V2": _proof_payload(
            "EXACT_RATIONAL_AST_NORMALIZATION_V2",
            {"input_ast": input_ast},
            {"normalization_rule_ids": ["ADD_CONSTANT_FOLD", "ADD_IDENTITY_REMOVE"]},
            {"normalized_ast": normalized, "normalized_sha256": ast_hash(normalized)},
        ),
        "DIRECTED_RATIONAL_INTERVAL_SIGN_V1": _proof_payload(
            "DIRECTED_RATIONAL_INTERVAL_SIGN_V1",
            {"scalar_ast": interval_expression, "variable_intervals": variable_intervals},
            {
                "precision_bits": 32,
                "rounding_mode": "OUTWARD_EXACT_RATIONAL",
                "subdivision_path": ["ROOT_CELL"],
            },
            {"interval": interval_result.to_wire(), "sign": "POSITIVE"},
        ),
        "POSITIVE_SQRT_INTERVAL_V1": _proof_payload(
            "POSITIVE_SQRT_INTERVAL_V1",
            {"radicand_interval": radicand.to_wire()},
            {"method": "INTEGER_SQUARE_BRACKETING", "precision_bits": 32},
            {"sqrt_interval": sqrt_result.to_wire()},
        ),
        "PREDICATE_CELL_EQUIVALENCE_V1": _proof_payload(
            "PREDICATE_CELL_EQUIVALENCE_V1",
            {"domain": domain, "left_predicate": left, "right_predicate": right},
            {
                "cell_ids": ["CELL_0"],
                "forward_certificate_ids": ["FORWARD_0"],
                "reverse_certificate_ids": ["REVERSE_0"],
            },
            {"equivalence_claim": True},
        ),
        "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1": _proof_payload(
            "MONOTONE_GRAPH_EXISTENCE_UNIQUENESS_V1",
            {"derivative_ast": const_q(1), "domain": domain, "equation_ast": x},
            {
                "base_variables": ["p", "s"],
                "derivative_sign": "POSITIVE",
                "face_signs": {"T_LO": "NEGATIVE", "T_HI": "POSITIVE"},
                "graph_variable": "t",
                "interval_cell_ids": ["CELL_0"],
            },
            {"existence_claim": True, "uniqueness_claim": True},
        ),
        "DEPENDENT_INCIDENCE_RESTRICTION_V1": _proof_payload(
            "DEPENDENT_INCIDENCE_RESTRICTION_V1",
            {"boundary": boundary, "dependent_support": left, "root_support": domain},
            {
                "orientation": "OWNER",
                "restriction_ast": normalize_ast(restrict(domain, boundary)),
                "trace_certificate_ids": ["TRACE_0"],
            },
            {"exact_restriction_claim": True},
        ),
        "FINITE_HALF_OPEN_SUPPORT_UNION_V1": _proof_payload(
            "FINITE_HALF_OPEN_SUPPORT_UNION_V1",
            {"pieces": [left, right]},
            {
                "owner_rule_ids": ["OWNER_0", "OWNER_1"],
                "pairwise_disjoint_certificate_ids": ["DISJOINT_0_1"],
                "piece_ids": ["PIECE_0", "PIECE_1"],
            },
            {"complete_claim": True, "support": union},
        ),
        "ARTIFICIAL_FACE_REGLUE_V1": _proof_payload(
            "ARTIFICIAL_FACE_REGLUE_V1",
            {"common_face": boundary, "left_cell": left, "right_cell": right},
            {
                "left_trace_sha256": hash_a,
                "owner_rule_id": "LEFT_OWNER",
                "right_trace_sha256": hash_b,
            },
            {"no_duplicate_claim": True, "reglued_support": union},
        ),
        "FIXED_SIGN_T2PS_PULLBACK_V1": _proof_payload(
            "FIXED_SIGN_T2PS_PULLBACK_V1",
            {"sigma": -1, "t_ast": fixed_t, "u_ast": u},
            {"substitution_variable": "t", "u_positive_certificate_id": "U_POSITIVE_0"},
            {"pullback_predicate": normalize_ast(gt_zero(u))},
        ),
        "REPRESENTATION_OWNER_BACKBINDING_V1": _proof_payload(
            "REPRESENTATION_OWNER_BACKBINDING_V1",
            {"member_support": domain, "representation_support": domain},
            {
                "member_id": "MEMBER_0",
                "owner_id": "OWNER_0",
                "representation_id": "REP_0",
                "source_join_id": "JOIN_0",
            },
            {"supports_equal_claim": True},
        ),
        "SHEET_MEMBER_EQUIVALENCE_V1": _proof_payload(
            "SHEET_MEMBER_EQUIVALENCE_V1",
            {"graph_support": domain, "sheet_support": domain},
            {
                "forward_certificate_ids": ["FORWARD_0"],
                "graph_id": "GRAPH_0",
                "member_id": "MEMBER_0",
                "reverse_certificate_ids": ["REVERSE_0"],
            },
            {"sets_equal_claim": True},
        ),
        "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1": _proof_payload(
            "BOUNDARY_TRACE_PHYSICAL_INCIDENCE_V1",
            {"boundary": boundary, "graph_support": domain, "side_support": left},
            {
                "incidence_id": "INCIDENCE_0",
                "orientation": "SHADOW",
                "trace_certificate_ids": ["TRACE_0"],
            },
            {"exact_physical_incidence_claim": True},
        ),
        "SOURCE_LINEAGE_EXHAUSTION_V1": _proof_payload(
            "SOURCE_LINEAGE_EXHAUSTION_V1",
            {"join_ids": ["JOIN_0"], "member_ids": ["MEMBER_0"], "source_ids": ["SOURCE_0"]},
            {
                "exhaustiveness_sha256": hash_a,
                "join_count": 1,
                "member_count": 1,
                "source_count": 1,
            },
            {"duplicate_count": 0, "missing_count": 0, "orphan_count": 0},
        ),
    }
    need(tuple(payloads) == PROOF_KERNEL_IDS, "sample payload kernel order")
    return payloads


def _positive_ast_and_macro_tests() -> int:
    count = 0
    x = var("x")
    y = var("y")
    normalized_sum = normalize_ast(add(const_q(2), x, add(y, const_q(-2))))
    need(normalized_sum["op"] == "ADD" and len(normalized_sum["args"]) == 2, "ADD normalization")
    count += 1
    normalized_product = normalize_ast(mul(const_q(2), x, const_q(Fraction(1, 2))))
    need(canonical_json(normalized_product) == canonical_json(x), "MUL normalization")
    count += 1
    need(as_fraction(normalize_ast(div_nonzero(const_q(3), const_q(4)))["value"]) == Fraction(3, 4), "DIV fold")
    count += 1
    need(as_fraction(normalize_ast(sqrt_positive(const_q(Fraction(9, 16))))["value"]) == Fraction(3, 4), "sqrt exact fold")
    count += 1
    need(ast_hash(add(x, const_q(0))) == ast_hash(x), "normalization hash")
    count += 1
    interval = RationalInterval(Fraction(-2), Fraction(3)).square()
    need(interval == RationalInterval(Fraction(0), Fraction(9)), "interval square")
    count += 1
    quotient = RationalInterval(Fraction(2), Fraction(4)).div_nonzero(
        RationalInterval(Fraction(1), Fraction(2))
    )
    need(quotient == RationalInterval(Fraction(1), Fraction(4)), "interval division")
    count += 1
    sqrt_interval = positive_sqrt_bounds(RationalInterval(Fraction(2), Fraction(3)), 24)
    need(sqrt_interval.lower * sqrt_interval.lower <= 2, "irrational sqrt lower")
    need(sqrt_interval.upper * sqrt_interval.upper >= 3, "irrational sqrt upper")
    count += 1
    sign = evaluate_interval(
        gt_zero(sub(x, const_q(1))),
        {"x": RationalInterval(Fraction(2), Fraction(3))},
    )
    need(sign == "TRUE", "interval predicate")
    count += 1

    box = OPEN_RATIONAL_BOX({"x": (0, 2), "y": (-1, 1)})
    box_ast = lower_macro(box)
    need(infer_ast_type(box_ast) == PREDICATE, "box lowering")
    count += 1
    sign_cell = lower_macro(STRICT_SIGN_CELL(((x, 1), (y, -1))))
    need(infer_ast_type(sign_cell) == PREDICATE, "sign cell lowering")
    count += 1
    left = normalize_ast(lt_zero(x))
    right = normalize_ast(gt_zero(x))
    union = lower_macro(FINITE_DISJOINT_UNION((left, right)))
    need(union["op"] == "OR_DISJOINT", "union lowering")
    count += 1
    boundary = normalize_ast(eq_zero(y))
    need(
        lower_macro(BOUNDARY_RESTRICTION(left, boundary))["op"] == "RESTRICT",
        "boundary lowering",
    )
    count += 1
    pullback = lower_macro(CHART_PULLBACK(gt_zero(x), {"x": add(y, const_q(1))}))
    need(infer_ast_type(pullback) == PREDICATE, "pullback lowering")
    count += 1
    tps = lower_macro(TPS_DOMAIN((-1, 1), (-1, 1), (0, 1)))
    need(infer_ast_type(tps) == PREDICATE, "TPS lowering")
    count += 1
    formula = source_g_formula_map("E", "G", 0, 0, Fraction(1, 4))
    need(formula["lowered_kind"] == "SOURCE_G_SCALAR_MAP", "formula lowering")
    need(
        canonical_json(formula["fields"]["psi"])
        == canonical_json(
            normalize_ast(
                sub(square(formula["fields"]["v_x"]), square(formula["fields"]["v_y"]))
            )
        ),
        "psi formula",
    )
    count += 1
    point_environment = {
        "p": RationalInterval.point(0),
        "s": RationalInterval.point(0),
        "t": RationalInterval.point(0),
    }
    expected_point_values = {
        "delta": Fraction(1, 16),
        "hit_x": Fraction(-1, 4),
        "hit_y": Fraction(0),
        "normal_x": Fraction(1),
        "normal_y": Fraction(0),
        "psi": Fraction(1),
        "q_x": Fraction(9, 25),
        "q_y": Fraction(0),
        "rn": Fraction(1),
        "rp": Fraction(1),
        "tangent_x": Fraction(1),
        "tangent_y": Fraction(0),
        "transverse_z": Fraction(0),
        "v_x": Fraction(-1),
        "v_y": Fraction(0),
    }
    for field, expected in expected_point_values.items():
        actual = evaluate_interval(formula["fields"][field], point_environment)
        need(actual == RationalInterval.point(expected), "formula point evaluation:" + field)
    count += 1
    wall_factor = lower_macro(WALL_ENDPOINT_FACTOR(formula["fields"]["hit_x"], const_q(0)))
    need(infer_ast_type(wall_factor) == SCALAR, "wall factor lowering")
    count += 1
    diagonal = lower_macro(
        OUTGOING_DIAGONAL_FACTOR(formula["fields"]["v_x"], formula["fields"]["v_y"], "PSI")
    )
    need(canonical_json(diagonal) == canonical_json(formula["fields"]["psi"]), "diagonal psi")
    count += 1
    graph = lower_macro(IMPLICIT_REGULAR_GRAPH(tps, diagonal, "t", ("p", "s")))
    need(graph["lowered_kind"] == "IMPLICIT_REGULAR_GRAPH_FRAME", "graph frame")
    count += 1
    sheet = lower_macro(SHEET_MEMBER_EQUIVALENCE(graph["support"], graph["support"]))
    need(sheet["theorem_credit"] == 0, "sheet obligation zero credit")
    count += 1
    incidence = lower_macro(BOUNDARY_TRACE_INCIDENCE(graph["support"], left, boundary))
    need(incidence["theorem_credit"] == 0, "incidence obligation zero credit")
    count += 1
    half_open = lower_macro(HALF_OPEN_BOUNDARY_ASSIGNMENT(left, boundary))
    need(half_open["op"] == "OR_DISJOINT", "half-open lowering")
    count += 1
    need(infer_ast_type(fixed_sign_t2ps(-1, var("u"))) == SCALAR, "fixed-sign T2PS")
    count += 1
    for chart in ("E", "W", "N", "S"):
        for target_kind in ("G", "W"):
            sample = source_g_formula_map(chart, target_kind, 1, -2, Fraction(1, 5))
            need(len(sample["fields"]) == 21, "formula field count")
            count += 1
    return count


def _positive_proof_payload_tests() -> int:
    payloads = _sample_proof_payloads()
    for kernel_id, payload in payloads.items():
        result = validate_proof_payload(payload)
        need(result["kernel_id"] == kernel_id, "proof payload validation kernel")
        need(result["theorem_credit"] == 0, "proof payload zero credit")
    return len(payloads)


def _expect_kernel_error(action: Callable[[], Any]) -> bool:
    try:
        action()
    except KernelError:
        return True
    return False


def _semantic_mutation_suite() -> tuple[int, int]:
    payloads = _sample_proof_payloads()

    def mutated(kernel_id: str, action: Callable[[dict[str, Any]], None]) -> Callable[[], Any]:
        def run() -> Any:
            payload = deepcopy(payloads[kernel_id])
            action(payload)
            return validate_proof_payload(payload)
        return run

    bad_contract = kernel_contract()
    bad_contract["formal_credit"]["theorem"] = 1
    actions: list[Callable[[], Any]] = [
        lambda: infer_ast_type({"op": "UNKNOWN"}),
        lambda: infer_ast_type({"op": "CONST_Q", "value": rational_wire(1), "extra": 0}),
        lambda: infer_ast_type({"op": "CONST_Q", "value": {"numerator": 1, "denominator": 0}}),
        lambda: infer_ast_type({"op": "VAR", "name": "bad name"}),
        lambda: infer_ast_type(neg(gt_zero(var("x")))),
        lambda: infer_ast_type(add(var("x"))),
        lambda: infer_ast_type(add(var("x"), gt_zero(var("x")))),
        lambda: infer_ast_type(div_nonzero(var("x"), const_q(0))),
        lambda: infer_ast_type(sqrt_positive(const_q(0))),
        lambda: infer_ast_type(and_pred(gt_zero(var("x")), var("x"))),
        lambda: infer_ast_type(or_disjoint(gt_zero(var("x")), gt_zero(var("x")))),
        lambda: infer_ast_type(restrict(gt_zero(var("x")), var("x"))),
        lambda: RationalInterval(Fraction(2), Fraction(1)),
        lambda: RationalInterval(Fraction(-1), Fraction(1)).reciprocal_nonzero(),
        lambda: positive_sqrt_bounds(RationalInterval(Fraction(0), Fraction(1)), 32),
        lambda: positive_sqrt_bounds(RationalInterval(Fraction(1), Fraction(2)), 0),
        lambda: SOURCE_G_FIRST_HIT_MAP("Q", "G", 0, 0, 1),
        lambda: SOURCE_G_FIRST_HIT_MAP("E", "Q", 0, 0, 1),
        lambda: SOURCE_G_FIRST_HIT_MAP("E", "G", 0, 0, 0),
        lambda: OUTGOING_DIAGONAL_FACTOR(var("x"), var("y"), "UNKNOWN"),
        lambda: IMPLICIT_REGULAR_GRAPH(var("x"), var("y"), "t", ("p", "s")),
        lambda: lower_macro(TPS_DOMAIN((1, -1), (-1, 1), (0, 1))),
        lambda: validate_proof_payload({}),
        mutated("EXACT_RATIONAL_AST_NORMALIZATION_V2", lambda p: p.__setitem__("kernel_id", "UNKNOWN")),
        mutated("EXACT_RATIONAL_AST_NORMALIZATION_V2", lambda p: p.__setitem__("theorem_credit", 1)),
        mutated("EXACT_RATIONAL_AST_NORMALIZATION_V2", lambda p: p["evidence"].pop("normalization_rule_ids")),
        mutated("EXACT_RATIONAL_AST_NORMALIZATION_V2", lambda p: p["conclusion"].__setitem__("normalized_ast", const_q(7))),
        mutated("EXACT_RATIONAL_AST_NORMALIZATION_V2", lambda p: p["conclusion"].__setitem__("normalized_sha256", "0" * 64)),
        mutated("DIRECTED_RATIONAL_INTERVAL_SIGN_V1", lambda p: p["conclusion"].__setitem__("sign", "NEGATIVE")),
        mutated(
            "DIRECTED_RATIONAL_INTERVAL_SIGN_V1",
            lambda p: p["conclusion"].__setitem__(
                "interval", RationalInterval(Fraction(0), Fraction(1)).to_wire()
            ),
        ),
        mutated("POSITIVE_SQRT_INTERVAL_V1", lambda p: p["evidence"].__setitem__("precision_bits", 0)),
        mutated(
            "POSITIVE_SQRT_INTERVAL_V1",
            lambda p: p["conclusion"].__setitem__(
                "sqrt_interval", RationalInterval(Fraction(1), Fraction(1)).to_wire()
            ),
        ),
        mutated("FIXED_SIGN_T2PS_PULLBACK_V1", lambda p: p["premises"].__setitem__("t_ast", var("t"))),
        mutated("FINITE_HALF_OPEN_SUPPORT_UNION_V1", lambda p: p["evidence"].__setitem__("piece_ids", ["ONE"])),
        mutated("SOURCE_LINEAGE_EXHAUSTION_V1", lambda p: p["evidence"].__setitem__("source_count", 2)),
        mutated("SOURCE_LINEAGE_EXHAUSTION_V1", lambda p: p["conclusion"].__setitem__("missing_count", 1)),
        lambda: validate_kernel_contract(bad_contract),
    ]
    rejected = sum(_expect_kernel_error(action) for action in actions)
    return rejected, len(actions)


def refuse_candidate_or_production(_mode: str, _target: Any = None) -> NoReturn:
    raise KernelRefusal(REFUSAL)


def _refusal_boundary_probe() -> dict[str, Any]:
    calls = {
        "builtin_open": 0,
        "lstat": 0,
        "os_open": 0,
        "os_write": 0,
        "stderr": 0,
        "stdout": 0,
        "temp": 0,
    }

    def touched(name: str) -> Callable[..., Any]:
        def inner(*_args: Any, **_kwargs: Any) -> Any:
            calls[name] += 1
            raise AssertionError("refusal boundary crossed:" + name)
        return inner

    with (
        mock.patch.object(os, "lstat", side_effect=touched("lstat")),
        mock.patch.object(os, "open", side_effect=touched("os_open")),
        mock.patch.object(os, "write", side_effect=touched("os_write")),
        mock.patch.object(builtins, "open", side_effect=touched("builtin_open")),
        mock.patch.object(tempfile, "TemporaryFile", side_effect=touched("temp")),
        mock.patch.object(tempfile, "NamedTemporaryFile", side_effect=touched("temp")),
        mock.patch.object(sys.stdout, "write", side_effect=touched("stdout")),
        mock.patch.object(sys.stderr, "write", side_effect=touched("stderr")),
    ):
        refused = 0
        for mode in ("candidate", "production", "unknown"):
            try:
                refuse_candidate_or_production(mode, "/forbidden")
            except KernelRefusal as error:
                refused += int(str(error) == REFUSAL)
        refusal_argv = (
            ["--candidate", "/forbidden"],
            ["--candidate-dir", "/forbidden"],
            ["--production", "/forbidden"],
            ["--unknown"],
            ["--print-kernel-contract", "extra"],
            ["--self-test", "--candidate"],
        )
        return_codes = [cli(list(argv)) for argv in refusal_argv]
        default_code = cli([])
    need(refused == 3, "direct refusal count")
    need(all(code == 1 for code in return_codes), "CLI refusal return codes")
    need(default_code == 0, "default silent success")
    need(all(value == 0 for value in calls.values()), "pre-filesystem and pre-output refusal")
    return {
        "default_return_code": default_code,
        "direct_modes_refused": refused,
        "refusal_cli_cases": len(return_codes),
        "refusal_return_codes": return_codes,
        **calls,
    }


def self_test() -> dict[str, Any]:
    contract = kernel_contract()
    positive_ast_macro = _positive_ast_and_macro_tests()
    positive_payloads = _positive_proof_payload_tests()
    rejected, mutation_count = _semantic_mutation_suite()
    need(rejected == mutation_count, "all semantic mutations rejected")
    boundary = _refusal_boundary_probe()
    summary = {
        "schema": SCHEMA + ".self-test.v1",
        "status": "PASS_SOURCE_FREE_SYMBOLIC_KERNEL_LIGHTWEIGHT_SELF_TEST",
        "kernel_digest": contract["kernel_digest"],
        "positive_ast_interval_macro_tests": positive_ast_macro,
        "positive_proof_payload_tests": positive_payloads,
        "proof_kernel_id_count": len(PROOF_KERNEL_IDS),
        "semantic_mutations_rejected": rejected,
        "semantic_mutation_count": mutation_count,
        "refusal_boundary_probe": boundary,
        "upstream_modules_imported_or_executed": 0,
        "upstream_data_files_opened": 0,
        "candidate_or_production_files_written": 0,
        "theorem_credit": 0,
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**summary, "self_test_sha256": canonical_hash(summary)}


def cli(argv: Sequence[str] | None = None) -> int:
    """Minimal silent fail-closed CLI; no parser writes usage on refusals."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        return 0
    if arguments == ["--print-kernel-contract"]:
        print(canonical_json(kernel_contract()))
        return 0
    if arguments == ["--self-test"]:
        print(canonical_json(self_test()))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(cli())
