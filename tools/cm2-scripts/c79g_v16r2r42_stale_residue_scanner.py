#!/usr/bin/env python3
"""Read-only stale-residue scanner for a generated C79g r42 candidate.

This scanner is intentionally independent of the r42 builder and of the
publication path.  It reads the generated exact8 members, parses JSON and
source ASTs in memory, and emits one JSON report on stdout.  It never imports
candidate source, writes a receipt, changes permissions, creates a manifest,
or touches runtime/authority state.

The historical contract/audit JSONs deliberately contain many old rejection
witnesses.  Consequently this is not a blind whole-file ``r34``/``r39`` grep:
old labels are rejected only in the active bundle/active top-level metadata
surfaces.  Historical/rejection witness subtrees remain reportable data.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterable

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = os.environ.get("CM2_STALE_SCAN_TAG", "v16r2r42")
PREV = os.environ.get("CM2_STALE_SCAN_PREV", "v16r2r41")

# These are the only generated members examined by this scanner.  Manifest,
# outer, runtime, and credit are intentionally outside its scope.
TARGETS: dict[str, tuple[str, str]] = {
    "anchor": (f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json", "json"),
    "schema": (f"{BASE}_schema_{TAG}.json", "json"),
    "contract": (f"{BASE}_contract_{TAG}.json", "json"),
    "producer": (f"{BASE}_{TAG}_semantic_source.py", "source"),
    "consumer": (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{TAG}_semantic_source.py", "source"),
    "transition": (
        f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json", "json"),
    "audit": (f"{BASE}_static_audit_{TAG}.json", "json"),
    "launcher": (f"{BASE}_cold_launch_{TAG}_semantic_source.py", "source"),
}

# A stale r9 description/template label was the r41 blocker.  Keep this
# deliberately narrow so normal historical ``r9`` rejection witnesses do not
# cause a false rejection.
SCHEMA_DESCRIPTION_RESIDUE = re.compile(
    r"(?:\bv16r2r?9\b|\br9\b|\b r9\b|template|source[-_ ]template)",
    re.IGNORECASE,
)

# Old active path/tag tokens requested by the owner.  They are allowed in
# explicitly historical/rejection witness branches, but not in active bundle
# metadata or source active constants.
OLD_ACTIVE_TOKENS = ("v16r2r34", "v16r2r39", "v16r2r40")
OLD_SHORT_TOKENS = ("r34", "r39", "r40")
HISTORICAL_KEY_WORDS = (
    "histor", "rejection", "supersession", "predecessor", "published",
    "incident", "witness", "inherited", "v14", "v10", "v11", "v12",
    "v13", "prior", "previous", "old", "template_input",
)

# JSON nodes that describe the current candidate, rather than inherited
# history.  Matching is intentionally key-based and recursive under the
# current bundle roots.
ACTIVE_ROOT_KEYS = {
    "v16r2_bundle", "audited_v16r2_bundle", "successor_v16r2_static_bundle",
    "schema_and_constructor_closure", "final_audit_acceptance",
    "sealed_exec_and_no_producer_static_proof", "exact_publication_paths",
    "post_source_static_trust_receipts", "active_bundle", "active_paths",
    "active_metadata", "current_bundle", "current_paths",
}
ACTIVE_KEY_RE = re.compile(
    r"(?:^|_)(?:active|current|successor|candidate|source|consumer|producer|"
    r"launcher|cold|exact8|exact10|bundle|receipt|transition|audit|schema|"
    r"namespace|path|tag|pin_state)(?:$|_)", re.IGNORECASE)

# Source constants with active meaning.  Historical implementation constants
# (V14/V9/etc.) are intentionally not considered active by this scanner.
ACTIVE_SOURCE_NAME_RE = re.compile(
    r"(?:^|_)(?:ACTIVE|CURRENT|BASE|TAG|PREV|SELF|LAUNCHER|V16_TO_V16R2|"
    r"COLD_EXACT8|EXACT8|EXACT10|SOURCE_BASENAME)(?:$|_)")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    """Read one regular file while checking held fd and pathname identity."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short-read:{path}")
        return raw
    finally:
        os.close(fd)


def path_text(path: tuple[str, ...]) -> str:
    return "/".join(path) or "$"


def is_historical_path(path: tuple[str, ...]) -> bool:
    lowered = "_".join(path).lower()
    return any(word in lowered for word in HISTORICAL_KEY_WORDS)


def old_token_hits(text: str) -> list[str]:
    lower = text.lower()
    hits: list[str] = []
    for token in OLD_ACTIVE_TOKENS:
        if token in lower:
            hits.append(token)
    # Catch short labels only as standalone words; this avoids matching the
    # ``r42`` portion of the target tag or unrelated hexadecimal data.
    for token in OLD_SHORT_TOKENS:
        if re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", lower):
            hits.append(token)
    return sorted(set(hits))


def iter_nodes(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_nodes(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_nodes(child, path + (str(index),))


def active_json_strings(value: Any) -> Iterable[tuple[tuple[str, ...], str]]:
    """Yield strings under active bundle roots or active-looking keys."""
    def walk(node: Any, path: tuple[str, ...], active: bool) -> Iterable[tuple[tuple[str, ...], str]]:
        if isinstance(node, str):
            if active:
                yield path, node
            return
        if isinstance(node, dict):
            for key, child in node.items():
                key_s = str(key)
                child_active = active or key_s in ACTIVE_ROOT_KEYS or bool(ACTIVE_KEY_RE.search(key_s))
                yield from walk(child, path + (key_s,), child_active)
            return
        if isinstance(node, list):
            for index, child in enumerate(node):
                yield from walk(child, path + (str(index),), active)
    yield from walk(value, (), False)


def find_template_flags(value: Any, root: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path, node in iter_nodes(value, root):
        if path and path[-1].lower() == "source_template_only":
            if node is True or (isinstance(node, str) and node.strip().lower() == "true"):
                findings.append({"kind": "source_template_only_true",
                                 "path": path_text(path), "value": node})
    return findings


def ast_literal(node: ast.AST) -> Any:
    """Best-effort literal extraction; non-literals are represented as None."""
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def source_active_assignments(
    tree: ast.Module, text: str
) -> dict[str, list[tuple[int, Any, str]]]:
    """Return active module assignments plus their source expressions.

    ``ast.literal_eval`` cannot evaluate expressions such as ``OUT /
    "...r42..."``.  Keeping the source segment alongside the literal value
    lets the scanner inspect Path/f-string expressions without importing or
    executing candidate source.
    """
    values: dict[str, list[tuple[int, Any, str]]] = {}
    for node in tree.body:
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
            value = ast_literal(node.value)
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = ast_literal(node.value) if node.value is not None else None
        else:
            continue
        names = [t.id for t in targets if isinstance(t, ast.Name)]
        segment = ast.get_source_segment(text, node.value) or ""
        for name in names:
            if ACTIVE_SOURCE_NAME_RE.search(name):
                values.setdefault(name, []).append((getattr(node, "lineno", 0), value, segment))
    return values


def literal_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            if isinstance(key, str):
                yield key
            yield from literal_strings(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from literal_strings(child)


def assignment_resolves_fragment(
    assignments: dict[str, list[tuple[int, Any, str]]],
    name: str,
    fragment: str,
    seen: set[str] | None = None,
) -> bool:
    """Resolve a small, non-executing Name reference graph.

    Launcher/consumer sources commonly define ``SELF = OUT /
    SOURCE_BASENAME``.  Literal-only inspection sees no tag in ``SELF`` even
    though the referenced top-level basename is current.  Parse only the
    expression's Name nodes and recursively inspect already-collected module
    assignments; never import or evaluate the candidate.
    """
    if seen is None:
        seen = set()
    if name in seen:
        return False
    seen.add(name)
    rows = assignments.get(name, [])
    for _line, value, segment in rows:
        texts = list(literal_strings(value))
        if segment:
            texts.append(segment)
        if fragment in texts or any(fragment in text for text in texts):
            return True
        if segment:
            try:
                expr = ast.parse(segment, mode="eval")
            except SyntaxError:
                expr = None
            if expr is not None:
                for node in ast.walk(expr):
                    if isinstance(node, ast.Name) and node.id in assignments:
                        if assignment_resolves_fragment(assignments, node.id,
                                                        fragment, seen):
                            return True
    return False


def source_template_flag_nodes(tree: ast.AST) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        # Dict entries such as {"source_template_only": True}.
        if isinstance(node, ast.Dict):
            for key, val in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "source_template_only":
                    literal = ast_literal(val)
                    if literal is True or (isinstance(literal, str) and literal.lower() == "true"):
                        findings.append({"kind": "source_template_only_true",
                                         "line": getattr(node, "lineno", 0),
                                         "value": literal})
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id.lower() == "source_template_only":
                    literal = ast_literal(node.value)
                    if literal is True or (isinstance(literal, str) and literal.lower() == "true"):
                        findings.append({"kind": "source_template_only_true",
                                         "line": getattr(node, "lineno", 0),
                                         "name": target.id, "value": literal})
    return findings


def add_check(checks: list[dict[str, Any]], name: str, passed: bool,
              detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)


def scan() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    loaded_json: dict[str, Any] = {}
    loaded_source: dict[str, tuple[str, ast.Module]] = {}

    # 1. Resolve and read all generated members first.  Missing members are a
    # hard fail, but the report remains machine-readable and side-effect-free.
    for role, (name, kind) in TARGETS.items():
        path = OUT / name
        exists = path.is_file()
        add_check(checks, f"member_present:{role}", exists,
                  {"path": str(path.relative_to(ROOT)), "kind": kind})
        if not exists:
            continue
        try:
            raw = stable(path)
            if kind == "json":
                loaded_json[role] = json.loads(raw.decode("utf-8"))
            else:
                text = raw.decode("utf-8")
                tree = ast.parse(text, filename=str(path), mode="exec")
                compile(tree, str(path), "exec")
                loaded_source[role] = (text, tree)
        except Exception as exc:
            findings.append({"kind": "parse_or_stable_read_error", "role": role,
                             "path": str(path.relative_to(ROOT)),
                             "error": f"{type(exc).__name__}: {exc}"})

    # 2. The schema description is a dedicated hard gate.  This catches the
    # exact r41 failure while allowing historical r9 strings elsewhere.
    schema = loaded_json.get("schema")
    description = schema.get("description") if isinstance(schema, dict) else None
    desc_hits = SCHEMA_DESCRIPTION_RESIDUE.findall(description or "") if isinstance(description, str) else ["<missing>"]
    add_check(checks, "schema_description_has_no_r9_or_template_residue",
              isinstance(description, str) and not desc_hits,
              {"description": description, "hits": sorted(set(desc_hits))})
    if desc_hits:
        findings.append({"kind": "schema_description_residue", "hits": sorted(set(desc_hits)),
                         "description": description})

    # 3. source_template_only=true is forbidden anywhere in generated JSON,
    # and in executable source ASTs (including nested receipt literals).
    json_template_findings: list[dict[str, Any]] = []
    for role, value in loaded_json.items():
        for item in find_template_flags(value):
            item = dict(item); item["role"] = role; json_template_findings.append(item)
    source_template_findings: list[dict[str, Any]] = []
    for role, (_text, tree) in loaded_source.items():
        for item in source_template_flag_nodes(tree):
            item = dict(item); item["role"] = role; source_template_findings.append(item)
    findings.extend(json_template_findings); findings.extend(source_template_findings)
    add_check(checks, "no_source_template_only_true",
              not json_template_findings and not source_template_findings,
              {"json_findings": json_template_findings,
               "source_findings": source_template_findings})

    # 4. Current JSON metadata must identify r42.  We inspect active roots and
    # top-level identity fields only, leaving inherited historical witnesses
    # untouched.
    active_old: list[dict[str, Any]] = []
    active_missing_tag: list[dict[str, Any]] = []
    for role, value in loaded_json.items():
        if not isinstance(value, dict):
            continue
        # Top-level identity fields are always active, regardless of their
        # names.  Nested active roots/keys are yielded by active_json_strings.
        candidates: list[tuple[tuple[str, ...], str]] = []
        for key, child in value.items():
            if isinstance(child, str):
                candidates.append(((str(key),), child))
        candidates.extend(active_json_strings(value))
        seen: set[tuple[tuple[str, ...], str]] = set()
        for path, text in candidates:
            if (path, text) in seen:
                continue
            seen.add((path, text))
            hits = old_token_hits(text)
            if not hits:
                continue
            if is_historical_path(path):
                continue
            active_old.append({"role": role, "path": path_text(path),
                               "hits": hits, "value": text[:600]})
        # Current identity fields that are present must contain target tag;
        # fields explicitly describing predecessor/history are excluded.
        for key in ("schema", "$id", "$comment", "title", "pin_state",
                    "bundle_version", "successor_namespace", "status"):
            if key in value and isinstance(value[key], str) and key not in ("status",):
                if TAG.lower() not in value[key].lower() and key in {"$id", "$comment", "bundle_version", "successor_namespace", "pin_state"}:
                    active_missing_tag.append({"role": role, "path": key,
                                               "value": value[key][:600]})
    findings.extend({"kind": "old_active_json_path", **item} for item in active_old)
    add_check(checks, "active_json_metadata_has_no_r34_r39_r40",
              not active_old, {"findings": active_old})
    add_check(checks, "active_json_identity_mentions_target_tag",
              not active_missing_tag, {"findings": active_missing_tag})

    # 5. Source top-level active metadata: inspect only module-level active
    # assignments, then explicitly validate the target/edge constants.
    source_old: list[dict[str, Any]] = []
    source_missing_tag: list[dict[str, Any]] = []
    for role, (_text, tree) in loaded_source.items():
        assignments = source_active_assignments(tree, _text)
        for name, rows in assignments.items():
            for line, value, segment in rows:
                literals = list(literal_strings(value))
                if segment:
                    literals.append(segment)
                for literal in literals:
                    hits = old_token_hits(literal)
                    if hits and not any(word in name.lower() for word in HISTORICAL_KEY_WORDS):
                        source_old.append({"role": role, "name": name, "line": line,
                                           "hits": hits, "value": literal[:600]})
        expected_fragments = {
            "ACTIVE_SUCCESSOR_NAMESPACE": TAG + "_semantic_source",
            "ACTIVE_SUCCESSOR_NAMESPACE_TAG": TAG + "-semantic-regeneration",
            "ACTIVE_PREDECESSOR_SUPERSESSION": TAG,
            "ACTIVE_REJECTED_RETRY_SUPERSESSION": TAG,
            "V16_TO_V16R2_TRANSITION": f"{PREV}_to_{TAG}",
            "LAUNCHER_RELATIVE": TAG,
            "SELF": TAG,
            "SOURCE_BASENAME": TAG,
        }
        for name, fragment in expected_fragments.items():
            rows = assignments.get(name, [])
            # Some active constants are role-specific (for example
            # ``LAUNCHER_RELATIVE`` exists only in the launcher).  Absence is
            # not a residue; when a role defines the name, however, its
            # expression must carry the current edge/tag.
            if not rows:
                continue
            if not assignment_resolves_fragment(assignments, name, fragment):
                literals = [s for _line, val, segment in rows
                            for s in (*literal_strings(val), segment)]
                source_missing_tag.append({"role": role, "name": name,
                                           "expected_fragment": fragment,
                                           "observed": literals[:6]})
    findings.extend({"kind": "old_active_source_path", **item} for item in source_old)
    add_check(checks, "source_top_level_active_metadata_has_no_r34_r39_r40",
              not source_old, {"findings": source_old})
    # Only launcher necessarily has all launcher constants; producer/consumer
    # may intentionally omit launcher-only fields.  Enforce each required
    # field on the role where it exists, and require core identity on all.
    core_missing = [row for row in source_missing_tag
                    if row["name"] in {"ACTIVE_SUCCESSOR_NAMESPACE",
                                       "ACTIVE_SUCCESSOR_NAMESPACE_TAG"}]
    add_check(checks, "source_top_level_active_identity_mentions_target_tag",
              not core_missing, {"findings": core_missing})
    edge_missing = [row for row in source_missing_tag
                    if row["name"] not in {"ACTIVE_SUCCESSOR_NAMESPACE",
                                            "ACTIVE_SUCCESSOR_NAMESPACE_TAG"}]
    add_check(checks, "source_top_level_active_edge_paths_are_current",
              not edge_missing, {"findings": edge_missing})

    failed = [row["name"] for row in checks if not row["passed"]]
    out: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.stale-residue-scan.v1",
        "status": (f"PASS_{TAG.upper()}_NO_STALE_ACTIVE_RESIDUE_READ_ONLY"
                   if not failed else
                   f"FAIL_CLOSED_{TAG.upper()}_STALE_ACTIVE_RESIDUE"),
        "read_only": True,
        "writes_performed": False,
        "target_tag": TAG,
        "predecessor_tag": PREV,
        "target_members": {role: name for role, (name, _kind) in TARGETS.items()},
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": checks,
        "findings": findings,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    out["object_sha256"] = sha(canonical(out))
    return out


def main() -> int:
    try:
        report = scan()
    except Exception as exc:  # Keep fail-closed output machine-readable.
        report = {
            "schema": f"cm2.c79g.{TAG}.stale-residue-scan.v1",
            "status": f"FAIL_CLOSED_{TAG.upper()}_STALE_SCAN_EXCEPTION",
            "read_only": True,
            "writes_performed": False,
            "target_tag": TAG,
            "predecessor_tag": PREV,
            "check_count": 0,
            "failed_check_count": 1,
            "failed_checks": ["scanner_exception"],
            "checks": [],
            "findings": [{"kind": "scanner_exception",
                          "error": f"{type(exc).__name__}: {exc}"}],
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }
        report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report.get("failed_check_count") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
