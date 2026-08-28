#!/usr/bin/env python3
"""Read-only active-path/anchor audit for the v16r2 semantic retry chain.

This audit never imports or executes a candidate source, never writes a report,
and never opens an existing namespace for writing.  It selects the highest
complete ``v16r2rN_semantic_source`` triplet currently present, checks its
immediate append-only predecessor, and emits one canonical JSON object on
stdout.  A candidate can therefore be syntactically valid and still fail
closed when its active graph, receipt generation, static bundle, or credit
boundary is not closed.

Run with ``python3 -I -B scripts/cm2_v16r2r_active_anchor_audit_v1.py``.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

BASE_PREFIX = "cm2_round306c79g_true_global_no_producer_consumer_"
C53_HEAD_REL = (
    ".cm2-runtime/cm2-global-authority-heads/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
)
C53_CLAIM_REL = (
    ".cm2-runtime/cm2-global-successor-claims/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim"
)
C53_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
V16_REJECTION_REL = (
    ".cm2-runtime/c79g-v16-rejections-"
    "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b/rejection.json"
)
V16_SUPERSESSION_REL = (
    BASE_PREFIX + "v16_semantic_rejection_supersession_receipt_v1.json"
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_without_object(value: Any) -> bytes:
    if isinstance(value, dict):
        value = {k: v for k, v in value.items() if k != "object_sha256"}
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def read_stable(root: Path, rel: str) -> tuple[bytes, dict[str, Any]]:
    path = root / rel
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not a regular nlink=1 file: {rel}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev, after.st_ino, after.st_size
        ) or (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"identity drift: {rel}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {rel}")
        return raw, {
            "path": rel,
            "sha256": sha(raw),
            "bytes": len(raw),
            "mode": format(stat.S_IMODE(before.st_mode), "04o"),
            "nlink": before.st_nlink,
        }
    finally:
        os.close(fd)


def read_json(root: Path, rel: str) -> tuple[Any, dict[str, Any]]:
    raw, meta = read_stable(root, rel)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise ValueError(f"duplicate key {key} in {rel}")
            out[key] = value
        return out

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs), meta


def lstat_present(root: Path, rel: str) -> bool:
    try:
        os.lstat(root / rel)
        return True
    except (FileNotFoundError, OSError):
        return False


def resolve_rel(root: Path, value: str | None) -> str | None:
    """Resolve a source/receipt path without importing candidate code.

    Older source candidates spell ``OUT / "name"`` and therefore expose only
    a basename in the AST audit; newer templates may expose a deliverables
    relative path.  Accept both spellings, but never accept an ambiguous path
    that does not resolve to one regular file.
    """
    if not isinstance(value, str) or not value:
        return None
    candidates = [value]
    if not value.startswith("deliverables/") and not value.startswith(".cm2-runtime/"):
        candidates.extend([f"deliverables/{value}", f".cm2-runtime/{value}"])
    for rel in candidates:
        if lstat_present(root, rel):
            return rel
    return candidates[0]


def source_triplets(root: Path) -> tuple[int, dict[str, str]] | None:
    """Return highest complete retry number and role->relative path."""
    candidates: dict[int, dict[str, str]] = {}
    out = root / "deliverables"
    if not out.is_dir():
        return None
    patterns = {
        "producer": re.compile(
            rf"^{re.escape(BASE_PREFIX)}v16r2r(\d+)_semantic_source\.py$"
        ),
        "consumer": re.compile(
            rf"^{re.escape(BASE_PREFIX)}independent_verifier_assembler_authority_consumer_v16r2r(\d+)_semantic_source\.py$"
        ),
        "launcher": re.compile(
            rf"^{re.escape(BASE_PREFIX)}cold_launch_v16r2r(\d+)_semantic_source\.py$"
        ),
    }
    for path in out.iterdir():
        if not path.is_file():
            continue
        for role, pattern in patterns.items():
            match = pattern.match(path.name)
            if match:
                number = int(match.group(1))
                candidates.setdefault(number, {})[role] = (
                    f"deliverables/{path.name}"
                )
    complete = [number for number, roles in candidates.items() if len(roles) == 3]
    if not complete:
        return None
    number = max(complete)
    return number, candidates[number]


def string_assignment(tree: ast.AST, name: str) -> str | None:
    value: str | None = None
    for node in ast.walk(tree):
        target: ast.expr | None = None
        rhs: ast.expr | None = None
        if isinstance(node, ast.Assign) and node.targets:
            target, rhs = node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign):
            target, rhs = node.target, node.value
        if isinstance(target, ast.Name) and target.id == name and rhs is not None:
            try:
                parsed = ast.literal_eval(rhs)
            except Exception:
                continue
            if isinstance(parsed, str):
                value = parsed
    return value


def bool_assignment(tree: ast.AST, name: str) -> bool | None:
    value: bool | None = None
    for node in ast.walk(tree):
        target: ast.expr | None = None
        rhs: ast.expr | None = None
        if isinstance(node, ast.Assign) and node.targets:
            target, rhs = node.targets[0], node.value
        elif isinstance(node, ast.AnnAssign):
            target, rhs = node.target, node.value
        if isinstance(target, ast.Name) and target.id == name and rhs is not None:
            try:
                parsed = ast.literal_eval(rhs)
            except Exception:
                continue
            if isinstance(parsed, bool):
                value = parsed
    return value


def text_assignment(raw: bytes, name: str) -> str | None:
    text = raw.decode("utf-8", errors="strict")
    # Path-valued assignments are intentionally extracted lexically.  This
    # avoids importing Path expressions and does not rewrite or execute code.
    patterns = [
        rf"(?m)^\s*{re.escape(name)}\s*=\s*OUT\s*/\s*[\"']([^\"']+)[\"']",
        rf"(?m)^\s*{re.escape(name)}\s*=\s*[\"']([^\"']+)[\"']",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def source_constants(raw: bytes, path: str) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8"), filename=path)
    values: dict[str, Any] = {"ast_pass": True}
    for name in (
        "ACTIVE_SUCCESSOR_NAMESPACE", "SCHEMA", "BASE", "SOURCE_BASENAME",
        "CHECKPOINT", "CHECKPOINT_OBJECT_PIN",
    ):
        values[name] = string_assignment(tree, name) or text_assignment(raw, name)
    for name in ("FORMAL_GLOBAL_CLOSURE_CREDIT", "D02_UNLOCK", "FINAL_BASE7_PINS_INSTALLED",
                 "FINAL_CURRENT_V16R2_PINS_INSTALLED", "FINAL_V16R2_CORE_PINS_INSTALLED"):
        values[name] = bool_assignment(tree, name)
    for name in ("ACTIVE_PREDECESSOR_SUPERSESSION", "ACTIVE_REJECTED_RETRY_SUPERSESSION"):
        values[name] = text_assignment(raw, name)
    return values


def check(rows: list[dict[str, Any]], number: int, name: str, passed: bool,
          observed: Any = None, expected: Any = None, blocker: str | None = None) -> None:
    row: dict[str, Any] = {"id": number, "name": name, "passed": bool(passed)}
    if observed is not None:
        row["observed"] = observed
    if expected is not None:
        row["expected"] = expected
    if blocker is not None:
        row["blocker"] = blocker
    rows.append(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    rows: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {}
    try:
        selected = source_triplets(root)
        check(rows, 1, "complete_retry_triplet_present", selected is not None,
              observed=selected[0] if selected else None,
              blocker="Need producer, consumer, and launcher in one fresh namespace.")
        if selected is None:
            raise RuntimeError("no complete v16r2rN source triplet")
        number, paths = selected
        namespace = f"v16r2r{number}_semantic_source"
        predecessor_namespace = f"v16r2r{number - 1}_semantic_source"
        if number == 3:
            predecessor_rel = (
                f"deliverables/{BASE_PREFIX}v16r2r2_to_v16r2r3_"
                "semantic_source_rejection_supersession_receipt_v1.json"
            )
        else:
            predecessor_rel = (
                f"deliverables/{BASE_PREFIX}v16r2r{number - 1}_to_v16r2r{number}_"
                "semantic_source_rejection_supersession_receipt_v1.json"
            )
        rejection_rel = (
            f"deliverables/{BASE_PREFIX}v16r2r{number}_semantic_source_"
            "rejection_receipt_v1.json"
        )
        evidence.update({
            "retry_number": number,
            "namespace": namespace,
            "predecessor_namespace": predecessor_namespace,
            "source_paths": paths,
            "expected_predecessor_receipt": predecessor_rel,
            "expected_rejection_receipt": rejection_rel,
        })

        raws: dict[str, bytes] = {}
        metas: dict[str, dict[str, Any]] = {}
        trees: dict[str, ast.AST] = {}
        constants: dict[str, dict[str, Any]] = {}
        ast_ok = True
        for role, rel in paths.items():
            raw, meta = read_stable(root, rel)
            raws[role], metas[role] = raw, meta
            try:
                trees[role] = ast.parse(raw.decode("utf-8"), filename=rel)
                constants[role] = source_constants(raw, rel)
            except Exception as exc:
                ast_ok = False
                constants[role] = {"ast_pass": False, "error": str(exc)}
        evidence["sources"] = metas
        evidence["constants"] = constants

        check(rows, 2, "source_regular_nlink1", all(
            meta.get("mode") in {"0664", "0644", "0444"} and meta.get("nlink") == 1
            for meta in metas.values()
        ), observed=metas)
        check(rows, 3, "ast_compile_all_three_sources", ast_ok, blocker="Never execute a source that fails AST parsing.")

        active_paths = {role: constants[role].get("ACTIVE_PREDECESSOR_SUPERSESSION") for role in paths}
        active_names = {role: constants[role].get("ACTIVE_SUCCESSOR_NAMESPACE") for role in paths}
        retry_paths = {role: constants[role].get("ACTIVE_REJECTED_RETRY_SUPERSESSION") for role in paths}
        active_value = next((value for value in active_paths.values() if value), None)
        active_rel = resolve_rel(root, active_value)
        active_doc: Any = None
        active_meta: dict[str, Any] = {}
        if active_rel and lstat_present(root, active_rel):
            try:
                active_doc, active_meta = read_json(root, active_rel)
            except Exception as exc:
                active_meta = {"error": str(exc)}
        # A fresh retry may use a small immutable active-anchor receipt.  The
        # anchor is acceptable only when it names and pins the immediately
        # preceding retry supersession; it must not hide a skipped predecessor.
        anchor_mode = isinstance(active_doc, dict) and str(active_doc.get("schema", "")).endswith("active-predecessor-supersession.v1")
        anchor_underlying_rel = active_doc.get("predecessor_supersession_path") if anchor_mode else None
        anchor_underlying_rel = resolve_rel(root, anchor_underlying_rel)
        anchor_underlying_doc: Any = None
        if anchor_underlying_rel and lstat_present(root, anchor_underlying_rel):
            try:
                anchor_underlying_doc, _ = read_json(root, anchor_underlying_rel)
            except Exception:
                anchor_underlying_doc = None
        predecessor_doc: Any = anchor_underlying_doc if anchor_mode else active_doc
        predecessor_meta = active_meta
        evidence["predecessor_receipt"] = {
            "active_path": active_meta,
            "active_anchor": anchor_mode,
            "underlying_path": anchor_underlying_rel,
        }
        active_path_ok = all(
            value == Path(predecessor_rel).name for value in active_paths.values()
        )
        if anchor_mode:
            active_path_ok = all(value == Path(active_rel or "").name for value in active_paths.values()) and anchor_underlying_rel == predecessor_rel
        check(rows, 4, "active_predecessor_is_immediate_receipt", active_path_ok,
              observed={"source": active_paths, "active_resolved": active_rel, "underlying": anchor_underlying_rel},
              expected=predecessor_rel,
              blocker="A wrapper anchor is allowed only when it pins the immediately preceding supersession.")

        predecessor_file_sha = predecessor_meta.get("sha256")
        predecessor_obj_sha = active_doc.get("object_sha256") if isinstance(active_doc, dict) else None
        check(rows, 5, "predecessor_file_sha_available", bool(predecessor_file_sha),
              observed=predecessor_file_sha, blocker="The exact predecessor bytes must be pinned before freeze.")
        check(rows, 6, "predecessor_object_sha_available", bool(predecessor_obj_sha),
              observed=predecessor_obj_sha, blocker="The predecessor object pin must be carried into the transition.")
        pred_ns_obs = active_doc.get("predecessor_namespace") if isinstance(active_doc, dict) else None
        succ_ns_obs = active_doc.get("successor_namespace") if isinstance(active_doc, dict) else None
        check(rows, 7, "predecessor_namespace_exact", pred_ns_obs == predecessor_namespace,
              observed=pred_ns_obs, expected=predecessor_namespace)
        normalized_source_names = {str(value).replace("-", "_") for value in active_names.values() if value}
        allowed_namespace_aliases = {namespace, namespace.replace("_semantic_source", "_semantic_regeneration")}
        check(rows, 8, "successor_namespace_exact", normalized_source_names and normalized_source_names.issubset(allowed_namespace_aliases) and succ_ns_obs == namespace,
              observed={"source": active_names, "receipt": succ_ns_obs}, expected=namespace,
              blocker="Any human-readable retry alias must normalize to a documented immutable namespace.")

        graph_fields = ("ACTIVE_PREDECESSOR_SUPERSESSION", "ACTIVE_SUCCESSOR_NAMESPACE",
                        "ACTIVE_REJECTED_RETRY_SUPERSESSION", "BASE")
        graph_values = {
            tuple(c.get(field) for field in graph_fields)
            for c in constants.values() if c.get("ast_pass")
        }
        check(rows, 9, "source_constants_consistent", len(graph_values) == 1,
              observed={role: {field: c.get(field) for field in graph_fields}
                        for role, c in constants.items()},
              blocker="Producer/consumer/launcher must share one active graph.")
        expected_basenames = {Path(rel).name for rel in paths.values()}
        source_basenames = {c.get("SOURCE_BASENAME") for c in constants.values()}
        declared_basenames = {value for value in source_basenames if isinstance(value, str)}
        check(rows, 10, "source_basename_and_self_shape", bool(declared_basenames) and declared_basenames.issubset(expected_basenames),
              observed={"declared": sorted(declared_basenames), "actual": sorted(expected_basenames)})
        schema_values = {c.get("SCHEMA") for c in constants.values()
                         if isinstance(c.get("SCHEMA"), str) and not c.get("SCHEMA", "").endswith(".json")}
        base_values = {c.get("BASE") for c in constants.values() if isinstance(c.get("BASE"), str)}
        check(rows, 11, "schema_and_base_constants_consistent", len(base_values) == 1 and len(schema_values) <= 1,
              observed={role: (c.get("SCHEMA"), c.get("BASE")) for role, c in constants.items()},
              blocker="A retry cannot silently mix v16r2 and rN base/schema identifiers.")

        checkpoint_values = {
            role: (
                c.get("CHECKPOINT") or c.get("CHECKPOINT_OBJECT_PIN"),
                c.get("CHECKPOINT_OBJECT_PIN"),
            )
            for role, c in constants.items()
        }
        pairs = [pair for pair in checkpoint_values.values() if pair != (None, None)]
        successor_pin = v16_effective = None
        # The launcher deliberately carries two different pins: CHECKPOINT is
        # the held C53 upstream object and CHECKPOINT_OBJECT_PIN is the v16
        # rejection-derived successor object.  Producer/consumer may expose
        # only the successor object pin.
        check(rows, 12, "checkpoint_constants_consistent", bool(pairs) and len({pair[1] for pair in pairs}) == 1 and
              pairs[0][1] is not None and all(
                  pair[0] in {pair[1], C53_CHECKPOINT} for pair in pairs
              ), observed=checkpoint_values,
              expected={"upstream": C53_CHECKPOINT, "successor": "v16 rejection effective pin"},
              blocker="Permit only the explicit upstream-C53/successor-object dual-pin convention.")

        v16_doc: Any = None
        if lstat_present(root, V16_REJECTION_REL):
            try:
                v16_doc, _ = read_json(root, V16_REJECTION_REL)
            except Exception:
                pass
        v16_effective = v16_doc.get("effective_checkpoint_object_sha256") if isinstance(v16_doc, dict) else None
        launcher_pair = checkpoint_values.get("launcher", (None, None))
        check(rows, 13, "checkpoint_links_to_v16_rejection", launcher_pair[1] == v16_effective and bool(v16_effective) and
              launcher_pair[0] in {C53_CHECKPOINT, v16_effective},
              observed={"launcher": launcher_pair[0], "v16_effective": v16_effective},
              blocker="The derived dd9… pin is valid only when linked to the frozen v16 rejection and upstream C53.")

        c53_ok = False
        try:
            _, head_meta = read_stable(root, C53_HEAD_REL)
            claim, _ = read_json(root, C53_CLAIM_REL)
            c53_ok = head_meta.get("nlink") == 1 and (
                claim.get("effective_checkpoint_object_sha256") == C53_CHECKPOINT
                or claim.get("post_seal_effective_checkpoint_object_sha256") == C53_CHECKPOINT
            )
        except Exception:
            c53_ok = False
        check(rows, 14, "c53_upstream_chain_present", c53_ok, expected=C53_CHECKPOINT,
              blocker="A derived successor checkpoint is not authority without the C53 upstream pin.")
        retry_path_ok = all(value == Path(predecessor_rel).name for value in retry_paths.values())
        if anchor_mode:
            retry_path_ok = all(value == Path(active_rel or "").name for value in retry_paths.values()) and anchor_underlying_rel == predecessor_rel
        check(rows, 15, "retry_supersession_path_is_immediate", retry_path_ok,
              observed={"source": retry_paths, "active_resolved": active_rel, "underlying": anchor_underlying_rel},
              expected=predecessor_rel)

        receipt_doc = predecessor_doc
        schema_value = receipt_doc.get("schema") if isinstance(receipt_doc, dict) else ""
        check(rows, 16, "receipt_namespace_pair_closed", pred_ns_obs == predecessor_namespace and succ_ns_obs == namespace,
              observed={"predecessor": pred_ns_obs, "successor": succ_ns_obs})
        expected_schema_token = f"v16r2r{number - 1}-to-v16r2r{number}"
        check(rows, 17, "receipt_schema_generation_closed", expected_schema_token in str(schema_value) and "v16r2-to-v16r2r2" not in str(schema_value),
              observed=schema_value, expected=expected_schema_token)
        status_value = receipt_doc.get("status") if isinstance(receipt_doc, dict) else ""
        check(rows, 18, "receipt_status_generation_closed", bool(status_value) and "R2R2_ONLY" not in str(status_value) and str(number) in str(status_value),
              observed=status_value, blocker="A stale R2R2_ONLY status cannot authorize a later retry.")

        pred_rejection_path = receipt_doc.get("predecessor_rejection_path") if isinstance(receipt_doc, dict) else None
        pred_rejection_sha_ok = False
        pred_rejection_obj_ok = False
        if isinstance(pred_rejection_path, str) and lstat_present(root, pred_rejection_path):
            try:
                pred_raw, pred_meta = read_stable(root, pred_rejection_path)
                pred_rejection_sha_ok = pred_meta["sha256"] == receipt_doc.get("predecessor_rejection_file_sha256")
                pred_doc = json.loads(pred_raw.decode("utf-8"))
                pred_rejection_obj_ok = pred_doc.get("object_sha256") == receipt_doc.get("predecessor_rejection_object_sha256")
            except Exception:
                pass
        check(rows, 19, "predecessor_rejection_file_object_pins", pred_rejection_sha_ok and pred_rejection_obj_ok,
              observed={"file": pred_rejection_sha_ok, "object": pred_rejection_obj_ok})
        receipt_object_ok = isinstance(receipt_doc, dict) and receipt_doc.get("object_sha256") == sha(canonical_without_object(receipt_doc))
        active_object_ok = isinstance(active_doc, dict) and active_doc.get("object_sha256") == sha(canonical_without_object(active_doc))
        check(rows, 20, "supersession_receipt_object_hash", receipt_object_ok,
              observed={"active_anchor": active_object_ok, "underlying": receipt_doc.get("object_sha256") if isinstance(receipt_doc, dict) else None})
        check(rows, 21, "zero_credit_runtime_boundary", active_object_ok and isinstance(active_doc, dict) and active_doc.get("formal_global_closure_credit") == 0 and active_doc.get("D02_unlock") is False and active_doc.get("runtime_authorized") is False and isinstance(receipt_doc, dict) and receipt_doc.get("formal_global_closure_credit") == 0 and receipt_doc.get("D02_unlock") is False and receipt_doc.get("runtime_authorized") is False)

        # A retry-specific static bundle is required before any cold freeze.  It
        # is deliberately not inferred from the old v16r2 bundle.
        bundle_suffix = f"v16r2r{number}"
        bundle_paths = {
            "schema": f"deliverables/{BASE_PREFIX}schema_{bundle_suffix}.json",
            "contract": f"deliverables/{BASE_PREFIX}contract_{bundle_suffix}.json",
            "transition": f"deliverables/{BASE_PREFIX}v16r2r{number - 1}_to_v16r2r{number}_static_launch_transition_receipt_v1.json",
            "audit": f"deliverables/{BASE_PREFIX}static_audit_{bundle_suffix}.json",
        }
        bundle_docs: dict[str, Any] = {}
        bundle_meta: dict[str, Any] = {}
        for role, rel in bundle_paths.items():
            if lstat_present(root, rel):
                try:
                    doc, meta = read_json(root, rel)
                    bundle_docs[role], bundle_meta[role] = doc, meta
                except Exception as exc:
                    bundle_meta[role] = {"error": str(exc)}
        evidence["retry_bundle"] = bundle_meta
        schema_doc = bundle_docs.get("schema", {})
        check(rows, 22, "retry_schema_closed_shape", len(bundle_docs) == 4 and len(schema_doc.get("$defs", {})) == 46 and sum(
            1 for _ in re.finditer(r'\"\\$ref\"', json.dumps(schema_doc))
        ) == 242, observed={"bundle_files": sorted(bundle_docs), "defs": len(schema_doc.get("$defs", {}))})
        check(rows, 23, "retry_schema_refs_resolve", bool(bundle_docs.get("schema")) and schema_doc.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and all(
            isinstance(value, dict) for value in schema_doc.get("$defs", {}).values()
        ), blocker="Use a freshly pinned schema; an old v16r2 schema cannot stand in for a retry bundle.")

        contract = bundle_docs.get("contract", {})
        transition = bundle_docs.get("transition", {})
        audit = bundle_docs.get("audit", {})
        check(rows, 24, "retry_contract_exact_keys_and_real_pins", bool(contract) and len(contract) >= 30 and "UNPINNED" not in json.dumps(contract),
              blocker="Contract must have exact closed shape and real byte pins.")
        check(rows, 25, "retry_transition_exact_keys_and_real_pins", bool(transition) and len(transition) >= 31 and "UNPINNED" not in json.dumps(transition),
              blocker="Transition must carry exact successor/predecessor and byte pins.")
        audit_text = json.dumps(audit)
        check(rows, 26, "retry_static_audit_authoritative_status", bool(audit) and "PASS_DUAL_STATIC" in str(audit.get("status", "")) and "STAGING" not in audit_text,
              blocker="Staging audit cannot be treated as authority.")
        dual = audit.get("dual_independent_static_checkers", {}) if isinstance(audit, dict) else {}
        check(rows, 27, "independent_checker_a_b_zero_fail", dual.get("checker_A", {}).get("status") not in {None, "NOT_RUN_SOURCE_TEMPLATE_ONLY"} and dual.get("checker_B", {}).get("status") not in {None, "NOT_RUN_SOURCE_TEMPLATE_ONLY"} and dual.get("checker_A", {}).get("failed_static_check_count") == 0 and dual.get("checker_B", {}).get("failed_static_check_count") == 0)
        check(rows, 28, "callsite_and_pin_consensus", dual.get("all_common_callsite_censuses_equal") is True and dual.get("all_pin_normalizers_equal") is True)
        attacks = audit.get("coherent_attack_static_census", {}) if isinstance(audit, dict) else {}
        check(rows, 29, "coherent_attacks_137_of_137", attacks.get("exact_unique_ordered_attack_count_observed") == 137 and attacks.get("exact_unique_ordered_attack_count_required") == 137 and attacks.get("all_fail_closed") is True)
        check(rows, 30, "semantic_review_and_final_source", audit.get("source_semantic_review") is True and audit.get("final_static_acceptance") is True if isinstance(audit, dict) else False)
        check(rows, 31, "exact8_order_and_manifest_position", audit.get("exact8_order") == ["predecessor", "schema", "contract", "producer", "consumer", "transition", "audit", "launcher"] and audit.get("manifest_position") == 9 if isinstance(audit, dict) else False)

        manifest_rel = f"deliverables/{BASE_PREFIX}cold_launch_manifest_{bundle_suffix}.sha256"
        outer_rel = f"deliverables/{BASE_PREFIX}cold_launch_outer_receipt_{bundle_suffix}.json"
        check(rows, 32, "manifest_outer_frozen_for_authority", lstat_present(root, manifest_rel) and lstat_present(root, outer_rel),
              observed={"manifest": lstat_present(root, manifest_rel), "outer": lstat_present(root, outer_rel)},
              blocker="These must remain absent during staging and appear only after all hard gates pass.")
        frozen_targets = list(paths.values()) + list(bundle_paths.values()) + [predecessor_rel, manifest_rel, outer_rel]
        frozen_meta: dict[str, Any] = {}
        for rel in frozen_targets:
            if lstat_present(root, rel):
                try:
                    _, meta = read_stable(root, rel); frozen_meta[rel] = meta
                except Exception as exc:
                    frozen_meta[rel] = {"error": str(exc)}
        check(rows, 33, "frozen_bytes_mode_nlink_terminal_replay", bool(frozen_meta) and all(
            item.get("nlink") == 1 and item.get("mode") == "0444" for item in frozen_meta.values()
        ), observed=frozen_meta, blocker="Final freeze requires immutable 0444/nlink1 bytes plus independent replay.")
        candidate_credit = any(
            c.get("FORMAL_GLOBAL_CLOSURE_CREDIT") == 1 or c.get("D02_UNLOCK") is True
            for c in constants.values()
        )
        check(rows, 34, "credit_boundary_only_positive_wrapper", not candidate_credit and isinstance(audit, dict) and audit.get("formal_global_closure_credit", 0) == 0,
              observed={"source_positive_literal": candidate_credit, "audit_credit": audit.get("formal_global_closure_credit", 0) if isinstance(audit, dict) else None},
              blocker="All source/static staging remains zero-credit; only an independent cold positive wrapper may mint credit.")

        failed = [row for row in rows if not row["passed"]]
        report = {
            "schema": "cm2.c79g.v16r2r.active-anchor-audit.v1",
            "status": "PASS_AUTHORITY_PRECONDITIONS" if not failed else "FAIL_CLOSED_ACTIVE_ANCHOR_OR_STATIC_BUNDLE",
            "retry": evidence,
            "check_count": len(rows),
            "failed_check_count": len(failed),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "checks": rows,
        }
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0 if not failed else 1
    except Exception as exc:
        report = {
            "schema": "cm2.c79g.v16r2r.active-anchor-audit.failure.v1",
            "status": "FAIL_CLOSED_ACTIVE_ANCHOR_AUDIT",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "check_count": len(rows),
            "failed_check_count": len(rows),
            "checks": rows,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
