#!/usr/bin/env python3
"""Build a genuine append-only successor of the failed r62 cold publication.

The r62 sources and receipts are immutable witnesses.  This recipe only
constructs new bytes in memory first, then (with ``install``) writes a fresh
contract/source/transition/audit/manifest/outer chain with O_EXCL.  It keeps
the semantic schema and historical checkpoint unchanged: this is a physical
publication-repair successor, not a reinterpretation of r62 bytes.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import runpy
from pathlib import Path
from typing import Any

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

OLD = {
    "schema": f"{BASE}_schema_v16r2r62.json",
    "contract": f"{BASE}_contract_v16r2r62.json",
    "producer": f"{BASE}_v16r2r62_semantic_source.py",
    "consumer": f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r62_semantic_source.py",
    "transition": f"{BASE}_v16r2r61_to_v16r2r62_static_launch_transition_receipt_v1.json",
    "audit": f"{BASE}_static_audit_v16r2r62.json",
    "launcher": f"{BASE}_cold_launch_v16r2r62_semantic_source.py",
    "manifest": f"{BASE}_cold_launch_manifest_v16r2r62.sha256",
    "outer": f"{BASE}_cold_launch_outer_receipt_v16r2r62.json",
}
NEW = {
    # The schema is intentionally shared; changing it would create an
    # unrelated semantic version transition and is not needed for this fix.
    "schema": OLD["schema"],
    "contract": f"{BASE}_contract_v16r2r63w_repair.json",
    "producer": f"{BASE}_v16r2r63w_repair_semantic_source.py",
    "consumer": f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r63w_repair_semantic_source.py",
    "transition": f"{BASE}_v16r2r62_to_v16r2r63w_repair_static_launch_transition_receipt_v1.json",
    "audit": f"{BASE}_static_audit_v16r2r63w_repair.json",
    "launcher": f"{BASE}_cold_launch_v16r2r63w_repair_semantic_source.py",
    "manifest": f"{BASE}_cold_launch_manifest_v16r2r63w_runtime_repair.sha256",
    "outer": f"{BASE}_cold_launch_outer_receipt_v16r2r63w_runtime_repair.json",
    "receipt": f"{BASE}_v16r2r62_to_v16r2r63w_runtime_repair_successor_receipt_v1.json",
}

OLD_SHA = {
    "contract": "e5093fc90f063542f23c69dde6e0a674b885a5115893b668d755da81156fd4b7",
    "contract_obj": "83e8fa14f00b1d545d09c6aeecbc85cd77c6b66d79b6c00753f1c99ac9e823bd",
    "producer": "1c494a66668b7ee7f12a1d5eac25225a68f72d256303aa7114b939e57772659a",
    "consumer": "0e68a498f60d659f72247fc6a2a45ee7ee2503765c6b645d1e6ab46d6abc8f20",
    "transition": "23d328057145051a0e42d5b6c4d06350a5e2aab38c06a6a02049225b520b7357",
    "transition_obj": "62a5a5e4f2a788c440f74425b0e13865e031cf14352b7ba99ed7ef248dfc9cdc",
    "audit": "e1cf25ad75c9f7b99e375e03eee92581ac5108b35e51cabe993a77040dbe9601",
    "audit_obj": "a4b97b73352e4129c5b1954bce83886ecdd716b63a6c5b528cafa15979756207",
    "launcher": "d82461275e83ce720b1c18751b54de5611781db9992eae63e57091a4bf9230f0",
    "schema": "1a9c03d332a1c12a34f330b30acb77b13a8f315732fc0bc75be29d3b8c3e1577",
}
V14_PATH = f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
R62_ANCHOR = OUT / f"{BASE}_v16r2r62_active_predecessor_supersession_receipt_v1.json"
R62_ANCHOR_SHA = "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194"
R62_ANCHOR_OBJECT = "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6"

# r63s successfully created the first A/B candidate pair.  Those fixed
# checkpoint targets are now immutable O_EXCL evidence and therefore cannot
# be reused by this successor.  Keep the semantic checkpoint unchanged, but
# give the next runtime surface a fresh, round-specific target namespace.
RUNTIME_TARGET_PREFIX_OLD = "c79g-v16r2-"
RUNTIME_TARGET_PREFIX_NEW = "c79g-v16r2r63w-"


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def ordered_json(value: Any) -> bytes:
    """Serialize proof JSON while retaining its frozen insertion order."""
    return json.dumps(value, ensure_ascii=False, sort_keys=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_stable(path: Path, expected: str | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not os.path.isfile(path) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable immutable input: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, after.st_size) or len(raw) != before.st_size:
            raise RuntimeError(f"input identity drift: {path}")
        if expected is not None and digest(raw) != expected:
            raise RuntimeError(f"input hash drift: {path}")
        return raw
    finally:
        os.close(fd)


def load_json(path: Path, expected_file: str | None = None) -> dict[str, Any]:
    raw = read_stable(path, expected_file)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"object JSON required: {path}")
    claim = value.get("object_sha256")
    if isinstance(claim, str):
        body = dict(value); body.pop("object_sha256", None)
        if digest(canon(body)) != claim:
            raise RuntimeError(f"object closure drift: {path}")
    return value


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = digest(canon(body))
    return body


def walk_replace(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {k: walk_replace(v, replacements) for k, v in value.items()}
    if isinstance(value, list):
        return [walk_replace(v, replacements) for v in value]
    if isinstance(value, str):
        # Exact value replacement is deliberate: historical narrative text
        # and unrelated predecessor names must not be retagged.
        return replacements.get(value, value)
    return value


def walk_string_replace(value: Any, replacements: dict[str, str]) -> Any:
    """Replace hash strings without round-tripping through sorted JSON."""
    if isinstance(value, dict):
        return {key: walk_string_replace(item, replacements)
                for key, item in value.items()}
    if isinstance(value, list):
        return [walk_string_replace(item, replacements) for item in value]
    if isinstance(value, str):
        return replacements.get(value, value)
    return value


def retag_json_runtime_targets(value: Any) -> Any:
    """Retag live v16r2 publication paths while retaining JSON key order."""
    if isinstance(value, dict):
        return {key: retag_json_runtime_targets(item)
                for key, item in value.items()}
    if isinstance(value, list):
        return [retag_json_runtime_targets(item) for item in value]
    if isinstance(value, str):
        return value.replace(RUNTIME_TARGET_PREFIX_OLD,
                             RUNTIME_TARGET_PREFIX_NEW)
    return value


def repair_v3_exact10_names(value: Any) -> Any:
    """Repair only the live V3 frozen witness role labels.

    The inherited transition and audit use the historical short labels
    ``producer``/``consumer``.  The current executable helper expects the
    explicit roles ``build_only_producer``/``independent_consumer``.  Keep
    this scoped to the two V3 ``ordered_exact10`` containers; historical
    predecessor evidence elsewhere is immutable.
    """
    if not isinstance(value, dict):
        return value
    out = {key: repair_v3_exact10_names(item) for key, item in value.items()}
    for section_key in ("append_only_predecessor_v3_regression",
                        "predecessor_v3_exact10_regression"):
        section = out.get(section_key)
        if not isinstance(section, dict):
            continue
        rows = section.get("ordered_exact10")
        if not isinstance(rows, list) or len(rows) != 10:
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            if row.get("name") == "producer":
                row["name"] = "build_only_producer"
            elif row.get("name") == "consumer":
                row["name"] = "independent_consumer"
    return out


def _reorder_like(value: Any, template: Any) -> Any:
    if isinstance(value, dict):
        template_keys = list(template) if isinstance(template, dict) else []
        keys = [key for key in template_keys if key in value]
        keys.extend(key for key in value if key not in keys)
        return {
            key: _reorder_like(value[key],
                               template.get(key) if isinstance(template, dict) else None)
            for key in keys
        }
    if isinstance(value, list):
        template_items = template if isinstance(template, list) else []
        return [_reorder_like(item,
                              template_items[index] if index < len(template_items) else None)
                for index, item in enumerate(value)]
    return value


def restore_frozen_proof_orders(value: Any) -> Any:
    """Restore predecessor v5..v12 and witness key-order gates.

    The old publication's object hashes are key-order independent, but the
    live launcher intentionally checks several historical mappings in their
    original insertion order.  A sorted JSON rewrite therefore needs this
    explicit byte-shape repair in every new contract/transition/audit object.
    """
    ns = runpy.run_path(str(OUT / OLD["launcher"]))
    ns["configure_workspace_paths"](ROOT)
    templates: list[Any] = [
        ns[f"expected_v{version}_published_rejected_segment"]()
        for version in (5, 6, 7, 8, 9, 10, 11, 12)
    ]
    templates.extend([
        ns["V11_DUAL_VALIDATOR_DIVERGENCE_INCIDENT"],
        {key: None for key in ns["V10_COLON_PREFIX_WITNESS_KEY_ORDER"]},
        ns["V12_V5_REJECTION_SHAPE_INCIDENT"],
        {key: None for key in (
            "receipt_path", "receipt_file_sha256", "receipt_object_sha256",
            "receipt_schema", "receipt_status", "transition_kind",
            "v14_successor_contract",
        )},
    ])

    def visit(node: Any) -> Any:
        if isinstance(node, dict):
            for template in templates:
                if isinstance(template, dict) and set(node) == set(template):
                    walked = {key: visit(item) for key, item in node.items()}
                    return _reorder_like(walked, template)
            return {key: visit(item) for key, item in node.items()}
        if isinstance(node, list):
            return [visit(item) for item in node]
        return node

    return visit(value)


def restore_producer_v10_proof_orders(value: Any) -> Any:
    """Align V10 nested proof maps with the producer's frozen key order.

    The historical launcher serializes these two nested maps in a different
    insertion order than the producer's independent validator.  Their
    canonical object digests are identical, but the cold producer also gates
    the byte-level tuple order, so every successor publication must carry the
    producer order in contract, transition, and audit.
    """
    first_order = (
        "attempted", "producer_child_spawned", "candidate_write_started",
        "candidate_or_stage_created", "positive_runtime_surface_count",
        "aborted_by_regression_label_prefix_guard", "command", "orientation",
    )
    incident_order = (
        "schema", "incident_id", "evidence_source", "producer_source_path",
        "producer_source_file_sha256", "frozen_v9_launcher_path",
        "frozen_v9_launcher_file_sha256", "regression_function",
        "failure_label_without_colon_prefix", "colon_prefixed_failure_label_literal",
        "exact_unprefixed_failure_label_literal_count",
        "exact_colon_prefixed_failure_label_literal_count",
        "failure_label_suffix_match_count", "expanded_structural_dict_count",
        "expanded_structural_dict_exact_key_count", "validator_call_count",
        "equality_gate_count", "v9_launcher_hash_gate",
        "regression_guard_conjunct_count", "regression_guard_true_conjunct_count",
        "regression_guard_false_conjunct_count",
        "regression_guard_conjunct_truth_vector",
        "unique_false_conjunct_zero_based_index", "unique_false_conjunct_source_line",
        "authority_source", "raw_whole_tree_string_equality_is_authority",
        "authority_derived_from_AST_structure_and_exact_prefix_join",
        "hold_static_freeze_trust_call_source_line", "regression_call_inside_hold_source_line",
        "candidate_stage_creation_source_line", "hold_function_contains_mkdir_call",
        "failure_occurs_before_candidate_or_stage_creation", "first_command",
        "first_orientation", "producer_child_spawned", "candidate_write_started",
        "candidate_or_stage_created", "positive_runtime_surface_count",
        "inner_stderr_line", "outer_stderr_line", "required_successor_fix",
        "formal_global_closure_credit", "D02_unlock", "D02_started",
    )

    def reorder(node: Any, order: tuple[str, ...]) -> Any:
        if not isinstance(node, dict) or set(node) != set(order):
            return node
        return {key: node[key] for key in order}

    def visit(node: Any) -> Any:
        if isinstance(node, dict):
            out = {}
            for key, item in node.items():
                item = visit(item)
                if key == "first_runtime_attempt":
                    item = reorder(item, first_order)
                elif key == "regression_label_prefix_incident":
                    item = reorder(item, incident_order)
                out[key] = item
            return out
        if isinstance(node, list):
            return [visit(item) for item in node]
        return node

    return visit(value)


def json_path_replacements() -> dict[str, str]:
    """Include basename/split-literal forms used by frozen JSON/source recipes."""
    out = path_replacements()
    for role, old in OLD.items():
        new = NEW.get(role)
        if new is None or old == new:
            continue
        if old.endswith(('.py', '.json', '.sha256')):
            out[old] = new
        # A few source literals split immediately after the common prefix;
        # replace the suffix as well so byte-level self-path guards cannot
        # retain a stale basename.
        marker = f"{BASE}_"
        if old.startswith(marker):
            old_suffix = old[len(marker):]
            new_suffix = new[len(marker):]
            out[old_suffix] = new_suffix
    return out


def replace_source(raw: bytes, path_repl: dict[str, str], hash_repl: dict[str, str]) -> bytes:
    text = raw.decode("utf-8")
    # Replace basenames first (sources use both Path()/basename and full
    # workspace-relative literals).  Longest-first avoids prefix collisions.
    pairs: list[tuple[str, str]] = []
    for old, new in path_repl.items():
        pairs.append((old, new))
        if old.startswith("deliverables/") and new.startswith("deliverables/"):
            pairs.append((old[len("deliverables/"):], new[len("deliverables/"):]))
    for old, new in sorted(set(pairs), key=lambda p: len(p[0]), reverse=True):
        text = text.replace(old, new)
    # Also catch a path split across adjacent Python string literals (the
    # source bytes contain the suffix but not the reconstructed full basename).
    for old, new in sorted(json_path_replacements().items(), key=lambda p: len(p[0]), reverse=True):
        if old not in path_repl:
            text = text.replace(old, new)
    # Current pins are unique in the post-source sections.  Replacing these
    # exact 64-byte values updates all current contract/producer/consumer/
    # transition/audit references while leaving historical hashes untouched.
    for old, new in sorted(hash_repl.items(), key=lambda p: len(p[0]), reverse=True):
        text = text.replace(old, new)
    return text.encode("utf-8")


def retag_current_runtime_targets(text: str, label: str,
                                  launcher: bool = False) -> str:
    """Move only the live v16r2 target namespace to this append-only round.

    Historical v3..v12 paths and the ``c79g-v16r2-child-exec`` memfd label
    are evidence, not publication targets.  Producer/consumer sources contain
    only live target literals with this prefix, while the launcher also has a
    memfd name; hence the launcher uses the rejection-path-only replacement.
    """
    if launcher:
        old = "c79g-v16r2-rejections-"
        new = RUNTIME_TARGET_PREFIX_NEW + "rejections-"
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{label}: launcher runtime rejection target anchor count {count}")
        return text.replace(old, new, 1)
    count = text.count(RUNTIME_TARGET_PREFIX_OLD)
    if count == 0:
        raise RuntimeError(f"{label}: live runtime target namespace anchor missing")
    return text.replace(RUNTIME_TARGET_PREFIX_OLD,
                        RUNTIME_TARGET_PREFIX_NEW)


def compile_source(raw: bytes, label: str) -> None:
    try:
        tree = ast.parse(raw.decode("utf-8"), label, mode="exec")
        compile(tree, label, "exec")
    except Exception as exc:
        raise RuntimeError(f"{label} AST/compile failure: {exc}") from exc


def path_replacements() -> dict[str, str]:
    return {f"deliverables/{OLD[k]}": f"deliverables/{NEW[k]}"
            for k in OLD if k != "schema" and OLD[k] != NEW[k]}


def immutable_inputs() -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for role, name in OLD.items():
        expected = OLD_SHA.get(role)
        out[role] = read_stable(OUT / name, expected)
    # The active anchor is not part of exact8 but is a pinned live input.
    out["anchor"] = read_stable(R62_ANCHOR, R62_ANCHOR_SHA)
    anchor = json.loads(out["anchor"].decode("utf-8"))
    if anchor.get("object_sha256") != R62_ANCHOR_OBJECT:
        raise RuntimeError("r62 active anchor object pin drift")
    return out


def construct() -> tuple[dict[str, bytes], dict[str, Any]]:
    src = immutable_inputs()
    repl = path_replacements()

    # Contract is the first new node in the acyclic source graph.
    contract_value = load_json(OUT / OLD["contract"], OLD_SHA["contract"])
    contract_value = walk_replace(contract_value, json_path_replacements())
    contract_value = retag_json_runtime_targets(contract_value)
    contract_value = repair_v3_exact10_names(contract_value)
    # The frozen launcher contract shape is the canonical r63 repair shape:
    # v14 authority remains in the audit/inherited exact12 proof, while the
    # contract and transition omit the stale top-level v14 alias.
    contract_value.pop("published_then_officially_rejected_predecessor_v14", None)
    # The live launcher independently rebuilds the 126/124 identity census
    # and requires the same values to be persisted in the contract witness.
    # The r62 contract carried only the path/credit subset, so add the
    # missing immutable census fields to this successor before object close.
    bundle_value = contract_value.setdefault("v16r2_bundle", {})
    census = bundle_value.setdefault("cold_launch_outer_closure", {})
    census.update({
        "current_v16r2_exact10_plus_all_append_only_predecessors_unique_file_identity_count": 126,
        "v16r2_predecessor_unique_live_identity_count": 116,
        "v16r2_prepublication_unique_live_identity_count": 124,
        "v16r2_terminal_unique_live_identity_count": 126,
        "v16r2_terminal_group_vector": [10, 10, 10, 10, 10, 10, 10, 10, 10,
                                        10, 10, 7, 1, 3, 3, 1, 1],
        "all_126_file_identities_share_one_statx_mount": True,
    })
    contract_value = restore_frozen_proof_orders(contract_value)
    contract_value = restore_producer_v10_proof_orders(contract_value)
    contract_value = close_object(contract_value)
    contract_raw = ordered_json(contract_value) + b"\n"
    contract_sha = digest(contract_raw)
    contract_obj = contract_value["object_sha256"]

    # Producer has no self-hash cycle; it only binds the new contract and
    # physical source paths.
    producer_hash_repl = {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
    }
    producer_raw = replace_source(src["producer"], repl, producer_hash_repl)
    # The frozen r62 producer already inherits the twelve V14 authority
    # descriptors, but its aggregate identity census accidentally omitted the
    # published V14 exact10 and its later rejection (10 + 1 identities).
    # Repair that live census in the successor source before hashing it.  The
    # bytes remain immutable historical inputs; these are duplicate held-FD
    # views of the same 0444/nlink1 files, with no credit transfer.
    producer_text = producer_raw.decode("utf-8")
    producer_text = retag_current_runtime_targets(
        producer_text, NEW["producer"])
    producer_text = producer_text.replace(
        "make the predecessor census 105.  Current exact8 makes prepublication 113;\n"
        "    manifest plus outer-last make the terminal census 115.",
        "make the predecessor census 116.  Current exact8 makes prepublication 124;\n"
        "    manifest plus outer-last make the terminal census 126.")
    producer_text = producer_text.replace(
        '"append-only prior98/predecessor105/prepublication113/terminal115 "',
        '"append-only prior98/predecessor116/prepublication124/terminal126 "')
    old_v14_census_anchor = '''    need(len(v13_incident_guards) == 6 and
         len({guard.identity for guard in v13_incident_guards}) == 6 and
         [guard.file_sha256 for guard in v13_incident_guards] ==
             list(V13_INCIDENT_EXACT6_PINS.values()),
         "frozen v13 source-then-pyc exact6 held identity/hash order")
    current_cold_ten_guards = ['''
    new_v14_census_anchor = '''    need(len(v13_incident_guards) == 6 and
         len({guard.identity for guard in v13_incident_guards}) == 6 and
         [guard.file_sha256 for guard in v13_incident_guards] ==
             list(V13_INCIDENT_EXACT6_PINS.values()),
         "frozen v13 source-then-pyc exact6 held identity/hash order")
    v14_guards = [
        HeldPinnedInput(
            ROOT / relative_path,
            "frozen v14 published exact10:" + role,
            0o444, file_pin,
            self_guard.incident_fds.get(ROOT / relative_path))
        for role, relative_path, file_pin, _object_pin
        in V14_PUBLISHED_EXACT10_WITNESS
    ]
    need(len(v14_guards) == 10 and
         len({guard.identity for guard in v14_guards}) == 10 and
         len({guard.mount_id for guard in v14_guards}) == 1 and
         all(guard.mount_id == self_guard.mount_id
             for guard in v14_guards),
         "frozen v14 published exact10 held identities on one statx mount")
    v14_rejection_path = ROOT / V14_OFFICIAL_REJECTION_RELATIVE_PATH
    v14_rejection_guard = HeldPinnedInput(
        v14_rejection_path, "official v14 later rejection", 0o444,
        V14_OFFICIAL_REJECTION_FILE_PIN,
        self_guard.incident_fds.get(v14_rejection_path))
    need(v14_rejection_guard.mount_id == self_guard.mount_id and
         v14_rejection_guard.identity not in
             {guard.identity for guard in v14_guards},
         "official v14 rejection identity is distinct and on one mount")
    current_cold_ten_guards = ['''
    if producer_text.count(old_v14_census_anchor) != 1:
        raise RuntimeError("producer V14 census insertion anchor not unique")
    producer_text = producer_text.replace(
        old_v14_census_anchor, new_v14_census_anchor, 1)
    old_v14_census_lists = '''    predecessor_guards = [
        *prior_history_guards, *v13_incident_guards, v12_rejection_guard]
    current_exact8_guards = [self_guard, *by_path.values()]
    prepublication_guards = [*predecessor_guards, *current_exact8_guards]
    all_file_guards = [
        *current_cold_ten_guards,
        *v12_guards, *v11_guards, *v10_guards, *v9_guards, *v8_guards,
        *v7_guards, *v6_guards, *v5_guards, *v3_guards, *v4_guards,
        v3_rejection_guard,
        *v13_incident_guards[:3], *v13_incident_guards[3:],
        v12_rejection_guard,
    ]
    group_vector = [
        len(current_cold_ten_guards), len(v12_guards), len(v11_guards),
        len(v10_guards), len(v9_guards), len(v8_guards), len(v7_guards),
        len(v6_guards), len(v5_guards), len(v3_guards), len(v4_guards),
        1, len(v13_incident_guards[:3]), len(v13_incident_guards[3:]), 1,
    ]'''
    new_v14_census_lists = '''    predecessor_guards = [
        *prior_history_guards, *v13_incident_guards, v12_rejection_guard,
        *v14_guards, v14_rejection_guard]
    current_exact8_guards = [self_guard, *by_path.values()]
    prepublication_guards = [*predecessor_guards, *current_exact8_guards]
    all_file_guards = [
        *current_cold_ten_guards,
        *v14_guards,
        *v12_guards, *v11_guards, *v10_guards, *v9_guards, *v8_guards,
        *v7_guards, *v6_guards, *v5_guards, *v3_guards, *v4_guards,
        v3_rejection_guard,
        *v13_incident_guards[:3], *v13_incident_guards[3:],
        v12_rejection_guard, v14_rejection_guard,
    ]
    group_vector = [
        len(current_cold_ten_guards), len(v14_guards),
        len(v12_guards), len(v11_guards), len(v10_guards),
        len(v9_guards), len(v8_guards), len(v7_guards), len(v6_guards),
        len(v5_guards), len(v3_guards), len(v4_guards), 1,
        len(v13_incident_guards[:3]), len(v13_incident_guards[3:]), 1, 1,
    ]'''
    if producer_text.count(old_v14_census_lists) != 1:
        raise RuntimeError("producer V14 census list anchor not unique")
    producer_text = producer_text.replace(
        old_v14_census_lists, new_v14_census_lists, 1)
    old_v14_return_guards = '''            *v7_guards, *v6_guards, *v5_guards, *v3_guards,
            *v4_guards, v3_rejection_guard, *v13_incident_guards,
            v12_rejection_guard,
            v12_namespace_guard, v11_namespace_guard, v10_namespace_guard,'''
    new_v14_return_guards = '''            *v7_guards, *v6_guards, *v5_guards, *v3_guards,
            *v4_guards, v3_rejection_guard, *v13_incident_guards,
            v12_rejection_guard, *v14_guards, v14_rejection_guard,
            v12_namespace_guard, v11_namespace_guard, v10_namespace_guard,'''
    if producer_text.count(old_v14_return_guards) != 1:
        raise RuntimeError("producer V14 return-guard anchor not unique")
    producer_text = producer_text.replace(
        old_v14_return_guards, new_v14_return_guards, 1)
    # The live schema contains the descriptive JSON-Schema ``$comment``
    # keyword.  The inherited producer's hard-coded actual-keyword witness
    # predates that member, so bind the successor source to the same sorted
    # universe that the launcher and successor audit close over.
    old_producer_keywords = '''    actual_keywords = [
        "$defs", "$id", "$ref", "$schema", "additionalProperties",
        "const", "description", "items", "maxItems", "minItems",
        "minLength", "minimum", "pattern", "prefixItems", "properties",
        "required", "title", "type"]'''
    new_producer_keywords = '''    actual_keywords = [
        "$comment", "$defs", "$id", "$ref", "$schema",
        "additionalProperties", "const", "description", "items",
        "maxItems", "minItems", "minLength", "minimum", "pattern",
        "prefixItems", "properties", "required", "title", "type"]'''
    if producer_text.count(old_producer_keywords) != 1:
        raise RuntimeError("producer schema keyword witness anchor not unique")
    producer_text = producer_text.replace(
        old_producer_keywords, new_producer_keywords, 1)
    # Keep the canonical r59/r62 exact-30 transition shape.  The inherited
    # producer's later static-trust set still listed the rejected v14 alias;
    # remove only that transition conjunct while retaining v14 in the
    # contract/audit proofs.
    old_producer_transition_v14 = (
        '             "rejected_prepublication_v13_supersession_receipt",\n'
        '             "published_then_officially_rejected_predecessor_v14",\n'
        '             "successor_v16r2_static_bundle"')
    new_producer_transition_v14 = (
        '             "rejected_prepublication_v13_supersession_receipt",\n'
        '             "successor_v16r2_static_bundle"')
    if producer_text.count(old_producer_transition_v14) != 1:
        raise RuntimeError("producer transition v14 shape anchor not unique")
    producer_text = producer_text.replace(
        old_producer_transition_v14, new_producer_transition_v14, 1)
    # The successor contract follows the same 29-key HeldBundle shape.  Keep
    # the producer's audit v14 proof, but remove the stale contract-set alias
    # so its independent validator agrees with the live contract bytes.
    producer_contract_marker = "need(set(contract) == {"
    producer_contract_start = producer_text.find(producer_contract_marker)
    if producer_contract_start < 0:
        raise RuntimeError("producer contract shape marker missing")
    old_producer_contract_v14 = (
        '             "published_then_officially_rejected_predecessor_v12",\n'
        '             "published_then_officially_rejected_predecessor_v14",\n'
        '             "rejected_prepublication_v13_supersession_receipt",')
    new_producer_contract_v14 = (
        '             "published_then_officially_rejected_predecessor_v12",\n'
        '             "rejected_prepublication_v13_supersession_receipt",')
    producer_contract_pos = producer_text.find(
        old_producer_contract_v14, producer_contract_start)
    if producer_contract_pos < 0:
        raise RuntimeError("producer contract v14 shape anchor missing")
    producer_text = (producer_text[:producer_contract_pos] +
                     new_producer_contract_v14 +
                     producer_text[producer_contract_pos +
                                   len(old_producer_contract_v14):])
    # The successor audit's dual checker preserves the V14 supersession
    # receipt (the immutable producer still names the older V12 wording in
    # three validator literals).  Retag only those dual-checker literals;
    # historical V12 rejection proof fields remain untouched.
    producer_dual_replacements = {
        "pin_normalization_preserves_v12_rejection_and_all_historical_pins":
            "pin_normalization_preserves_v14_supersession_receipt_and_all_historical_pins",
        "PRESERVE_V12_REJECTION_AND_ALL_HISTORICAL_PINS_V1":
            "PRESERVE_V14_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1",
    }
    for old_dual, new_dual in producer_dual_replacements.items():
        count = producer_text.count(old_dual)
        if count != (2 if old_dual.startswith("pin_normalization_preserves_") else 1):
            raise RuntimeError("producer dual V12 normalization anchor count")
        producer_text = producer_text.replace(old_dual, new_dual)
    # The successor audit carries the runtime-registry shape witness as a
    # first-class dual-checker member.  Bind the producer's independent
    # top-level key census to that exact closed set; this is append-only and
    # does not alter any historical V14 proof members.
    old_producer_dual_keys = '''             "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection",
             "held_launcher_pin_normalized_ast_sha256",
         }, "final v16r2 static audit dual-checker exact8 closure")'''
    new_producer_dual_keys = '''             "final_launcher_must_reproduce_pin_normalized_ast_after_pin_injection",
             "held_launcher_pin_normalized_ast_sha256",
             "actual_runtime_registry_shape_evidence",
         }, "final v16r2 static audit dual-checker exact8 closure")'''
    if producer_text.count(old_producer_dual_keys) != 1:
        raise RuntimeError("producer dual runtime-registry evidence anchor not unique")
    producer_text = producer_text.replace(
        old_producer_dual_keys, new_producer_dual_keys, 1)
    # The V14 successor audit names the inherited authority proof by its
    # exact twelve-byte witness.  Retag the producer's sealed-proof keyset and
    # value check to that live spelling while preserving all historical V12
    # rejection fields elsewhere in the source.
    old_producer_sealed_v12 = (
        "consumer_frozen_predecessor_incident_exact10_bytes_read_only_noncredit_allowed")
    new_producer_sealed_v14 = (
        "consumer_v14_inherited_authority_exact12_bytes_read_only_noncredit_allowed")
    if producer_text.count(old_producer_sealed_v12) != 2:
        raise RuntimeError("producer sealed V12 authority anchor count")
    producer_text = producer_text.replace(
        old_producer_sealed_v12, new_producer_sealed_v14)
    producer_raw = producer_text.encode("utf-8")
    compile_source(producer_raw, NEW["producer"])
    producer_sha = digest(producer_raw)

    # Consumer fixes the r62 V14/active-anchor object-pin mix-up in addition to
    # rebinding the complete current source graph.
    consumer_raw = replace_source(src["consumer"], repl, {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
        OLD_SHA["producer"]: producer_sha,
    })
    old_bug = ("verify_object(\n"
               "            v14_supersession, \"live active predecessor supersession anchor\",\n"
               "            ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN)")
    new_bug = ("verify_object(\n"
               "            v14_supersession, \"live active predecessor supersession anchor\",\n"
               "            V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN)")
    if old_bug not in consumer_raw.decode("utf-8"):
        raise RuntimeError("r62 V14 object-pin bug pattern not found")
    consumer_text = consumer_raw.decode("utf-8").replace(old_bug, new_bug, 1)
    consumer_text = retag_current_runtime_targets(
        consumer_text, NEW["consumer"])
    # The frozen launcher and producer define the executable
    # PIN_NORMALIZED_AST_ALGORITHM with the short V14 supersession-receipt
    # spelling.  The inherited consumer validator carried a longer
    # descriptive alias, which rejects the otherwise matching audit during
    # the first B-side replay.  Retag only that validator literal; the audit
    # remains bound to the launcher's canonical constant.
    old_consumer_algorithm = (
        '             "PRESERVE_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_"\n'
        '             "RECEIPT_AND_ALL_HISTORICAL_PINS_V1" and')
    new_consumer_algorithm = (
        '             "PRESERVE_V14_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1" and')
    if consumer_text.count(old_consumer_algorithm) != 1:
        raise RuntimeError("consumer V14 algorithm spelling anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_algorithm, new_consumer_algorithm, 1)
    # The live launcher recursively reports ``$comment`` as a schema keyword;
    # the inherited consumer's frozen expected list omitted it.  Keep the
    # audit/launcher universe authoritative and repair only this exact list.
    old_consumer_actual_keywords = '''    actual_keywords = [
        "$defs", "$id", "$ref", "$schema", "additionalProperties",
        "const", "description", "items", "maxItems", "minItems",
        "minLength", "minimum", "pattern", "prefixItems", "properties",
        "required", "title", "type"]'''
    new_consumer_actual_keywords = '''    actual_keywords = [
        "$comment", "$defs", "$id", "$ref", "$schema",
        "additionalProperties", "const", "description", "items",
        "maxItems", "minItems", "minLength", "minimum", "pattern",
        "prefixItems", "properties", "required", "title", "type"]'''
    if consumer_text.count(old_consumer_actual_keywords) != 1:
        raise RuntimeError("consumer actual schema keyword universe anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_actual_keywords, new_consumer_actual_keywords, 1)
    # The recursive strict-bool checker treats bare container truthiness as
    # unsafe. Preserve the exact rejection semantics while making this
    # predicate an explicit boolean comparison in the successor source.
    old_consumer_bool = "need(set(rejection) and len(rejection) == 52 and"
    new_consumer_bool = "need(len(rejection) > 0 and len(rejection) == 52 and"
    if consumer_text.count(old_consumer_bool) != 1:
        raise RuntimeError("consumer strict-bool rejection anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_bool, new_consumer_bool, 1)
    old_consumer_transition_v14 = (
        '             "rejected_prepublication_v13_supersession_receipt",\n'
        '             "published_then_officially_rejected_predecessor_v14",\n'
        '             "successor_v16r2_static_bundle"')
    new_consumer_transition_v14 = (
        '             "rejected_prepublication_v13_supersession_receipt",\n'
        '             "successor_v16r2_static_bundle"')
    if consumer_text.count(old_consumer_transition_v14) != 1:
        raise RuntimeError("consumer transition v14 shape anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_transition_v14, new_consumer_transition_v14, 1)
    if consumer_text.count(
            "         isinstance(transition_v14, dict) and\n") != 1:
        raise RuntimeError("consumer transition v14 type gate anchor not unique")
    consumer_text = consumer_text.replace(
        "         isinstance(transition_v14, dict) and\n", "", 1)
    old_consumer_transition_compare = (
        "         transition_v13 ==\n"
        "             expected_rejected_prepublication_v13_supersession_receipt() and\n"
        "         transition_v14 == expected_published_then_rejected_v14_summary(),")
    new_consumer_transition_compare = (
        "         transition_v13 ==\n"
        "             expected_rejected_prepublication_v13_supersession_receipt(),")
    if consumer_text.count(old_consumer_transition_compare) != 1:
        raise RuntimeError("consumer transition v14 comparison anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_transition_compare, new_consumer_transition_compare, 1)
    old_consumer_transition_return = (
        "            transition_v13 ==\n"
        "                expected_rejected_prepublication_v13_supersession_receipt() and\n"
        "            transition_v14 == expected_published_then_rejected_v14_summary(),")
    new_consumer_transition_return = (
        "            transition_v13 ==\n"
        "                expected_rejected_prepublication_v13_supersession_receipt(),")
    if consumer_text.count(old_consumer_transition_return) != 1:
        raise RuntimeError("consumer transition v14 return anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_transition_return, new_consumer_transition_return, 1)
    old_consumer_v14_consensus = (
        '            contract.get(\n'
        '                "published_then_officially_rejected_predecessor_v14") ==\n'
        '            transition_v14 == audit_v14 ==\n'
        '                expected_published_then_rejected_v14_summary(),')
    new_consumer_v14_consensus = (
        '            audit_v14 == expected_published_then_rejected_v14_summary(),')
    if consumer_text.count(old_consumer_v14_consensus) != 1:
        raise RuntimeError("consumer contract/audit v14 consensus anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_v14_consensus, new_consumer_v14_consensus, 1)
    # Match the canonical 29-key successor contract: v14 remains an audit /
    # inherited-authority proof, not a duplicate contract top-level member.
    consumer_contract_marker = "need(set(contract) == {"
    consumer_contract_start = consumer_text.find(consumer_contract_marker)
    if consumer_contract_start < 0:
        raise RuntimeError("consumer contract shape marker missing")
    old_consumer_contract_v14 = (
        '             "published_then_officially_rejected_predecessor_v12",\n'
        '             "rejected_prepublication_v13_supersession_receipt",\n'
        '             "published_then_officially_rejected_predecessor_v14",')
    new_consumer_contract_v14 = (
        '             "published_then_officially_rejected_predecessor_v12",\n'
        '             "rejected_prepublication_v13_supersession_receipt",')
    consumer_contract_pos = consumer_text.find(
        old_consumer_contract_v14, consumer_contract_start)
    if consumer_contract_pos < 0:
        raise RuntimeError("consumer contract v14 shape anchor missing")
    consumer_text = (consumer_text[:consumer_contract_pos] +
                     new_consumer_contract_v14 +
                     consumer_text[consumer_contract_pos +
                                   len(old_consumer_contract_v14):])
    old_consumer_contract_v14_binding = (
        '    published_v14 = contract.get(\n'
        '        "published_then_officially_rejected_predecessor_v14")\n')
    if consumer_text.count(old_consumer_contract_v14_binding) != 1:
        raise RuntimeError("consumer contract v14 binding anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_contract_v14_binding, "", 1)
    old_consumer_contract_v14_check = (
        '         rejected_v13 ==\n'
        '             expected_rejected_prepublication_v13_supersession_receipt() and\n'
        '         published_v14 == expected_published_then_rejected_v14_summary() and\n')
    new_consumer_contract_v14_check = (
        '         rejected_v13 ==\n'
        '             expected_rejected_prepublication_v13_supersession_receipt() and\n')
    if consumer_text.count(old_consumer_contract_v14_check) != 1:
        raise RuntimeError("consumer contract v14 check anchor not unique")
    consumer_text = consumer_text.replace(
        old_consumer_contract_v14_check, new_consumer_contract_v14_check, 1)
    consumer_raw = consumer_text.encode("utf-8")
    compile_source(consumer_raw, NEW["consumer"])
    consumer_sha = digest(consumer_raw)

    # Transition and audit are closed JSON objects whose current path/hash
    # references form the post-source trust chain.
    transition = load_json(OUT / OLD["transition"], OLD_SHA["transition"])
    transition = walk_replace(transition, json_path_replacements())
    transition = retag_json_runtime_targets(transition)
    transition = repair_v3_exact10_names(transition)
    transition = walk_string_replace(transition, {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
        OLD_SHA["producer"]: producer_sha,
        OLD_SHA["consumer"]: consumer_sha,
    })
    # The inherited r62 transition describes a pre-pin draft and consequently
    # leaves this one core-finalization witness false.  In this successor the
    # contract/producer/consumer/transition pins are closed before the
    # transition object is sealed; the later launcher/manifest/outer gates
    # intentionally remain false until their own stages run.
    finalization_gates = transition.get("finalization_gates")
    if not isinstance(finalization_gates, dict):
        raise RuntimeError("transition finalization gate object missing")
    if finalization_gates.get("final_core_pins_installed_before_object_closure") is not False:
        raise RuntimeError("unexpected inherited transition core-finalization value")
    finalization_gates["final_core_pins_installed_before_object_closure"] = True
    transition = restore_frozen_proof_orders(transition)
    transition = restore_producer_v10_proof_orders(transition)
    transition = close_object(transition)
    transition_raw = ordered_json(transition) + b"\n"
    transition_sha = digest(transition_raw)
    transition_obj = transition["object_sha256"]

    audit = load_json(OUT / OLD["audit"], OLD_SHA["audit"])
    audit = walk_replace(audit, json_path_replacements())
    audit = retag_json_runtime_targets(audit)
    audit = repair_v3_exact10_names(audit)
    audit = walk_string_replace(audit, {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
        OLD_SHA["producer"]: producer_sha,
        OLD_SHA["consumer"]: consumer_sha,
        OLD_SHA["transition"]: transition_sha,
        OLD_SHA["transition_obj"]: transition_obj,
    })
    # The inherited V4 audit witness used the previous successor label
    # ``v15`` for the closed-schema regression check.  The live v16r2
    # producer validates the same historical fact under its current
    # successor label; rename in place so insertion order is preserved.
    audit_key_replacements = {
        "same_defects_absent_from_v15": "same_defects_absent_from_v16r2",
        "v15_closed_object_required_property_mismatch_count":
            "v16r2_closed_object_required_property_mismatch_count",
    }
    def rename_audit_keys(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                audit_key_replacements.get(key, key): rename_audit_keys(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [rename_audit_keys(item) for item in value]
        return value
    audit = rename_audit_keys(audit)
    # The historical static audit omitted the descriptive ``$comment``
    # keyword even though it is present in the closed schema.  The live
    # launcher compares this census against its own recursive schema walk;
    # repair the value before closing the successor object.
    audit_ns = runpy.run_path(str(OUT / OLD["launcher"]))
    audit_ns["configure_workspace_paths"](ROOT)
    schema_value = json.loads(src["schema"].decode("utf-8"))
    audit_closure = audit.get("schema_and_constructor_closure")
    if isinstance(audit_closure, dict):
        actual_schema_keywords = sorted(
            audit_ns["schema_keyword_universe"](schema_value))
        audit_closure["actual_schema_keyword_universe"] = actual_schema_keywords
        audit_closure["actual_schema_keyword_universe_sha256"] = digest(
            canon(actual_schema_keywords))
    audit = restore_frozen_proof_orders(audit)
    audit = restore_producer_v10_proof_orders(audit)
    audit = close_object(audit)
    audit_raw = ordered_json(audit) + b"\n"
    audit_sha = digest(audit_raw)
    audit_obj = audit["object_sha256"]

    # Launcher has no self-hash cycle.  Path/hash substitution updates its
    # BASE7 table and all current exact8/outer reconstruction literals.
    launcher_raw = replace_source(src["launcher"], repl, {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
        OLD_SHA["producer"]: producer_sha,
        OLD_SHA["consumer"]: consumer_sha,
        OLD_SHA["transition"]: transition_sha,
        OLD_SHA["transition_obj"]: transition_obj,
        OLD_SHA["audit"]: audit_sha,
        OLD_SHA["audit_obj"]: audit_obj,
    })
    # The frozen r62 launcher accidentally validates the v13 prepublication
    # summary against the v14 receipt object.  The v14 receipt is the first
    # exact8 member, but the v13 summary is derived from the inherited v13
    # supersession receipt held by the constructor.  Pass that held object
    # explicitly into the final-audit gate so the runtime and static paths
    # use the same authority.  This is a source-level repair; the immutable
    # r62 launcher remains untouched and is still retained as evidence.
    launcher_text = launcher_raw.decode("utf-8")
    launcher_text = retag_current_runtime_targets(
        launcher_text, NEW["launcher"], launcher=True)
    old_signature = (
        "predecessor_v12: 'HeldV12PredecessorExact10', "
        "launcher_source_raw: bytes) -> None:")
    new_signature = (
        "predecessor_v12: 'HeldV12PredecessorExact10', "
        "v13_supersession: Mapping[str, Any], launcher_source_raw: bytes) -> None:")
    if launcher_text.count(old_signature) != 1:
        raise RuntimeError("launcher v13-audit signature anchor not unique")
    launcher_text = launcher_text.replace(old_signature, new_signature, 1)
    old_v13_call = (
        "validate_v13_supersession_summary(audit.get('rejected_prepublication_v13_supersession_receipt'), "
        "base_objects[V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT], "
        "'final static audit v13 prepublication rejection')")
    new_v13_call = (
        "validate_v13_supersession_summary(audit.get('rejected_prepublication_v13_supersession_receipt'), "
        "v13_supersession, 'final static audit v13 prepublication rejection')")
    if launcher_text.count(old_v13_call) != 1:
        raise RuntimeError("launcher v13-audit receipt call anchor not unique")
    launcher_text = launcher_text.replace(old_v13_call, new_v13_call, 1)
    old_final_call = "self.predecessor_v12, self.by_path[SELF].raw)"
    new_final_call = "self.predecessor_v12, v13_supersession, self.by_path[SELF].raw)"
    old_bool_gate = (
        "need(exact_vector and exact_partition and one_mount and "
        "distinct_descriptors and current_first_is_receipt,")
    new_bool_gate = (
        "need(exact_vector is True and exact_partition is True and "
        "one_mount is True and distinct_descriptors is True and "
        "current_first_is_receipt is True,")
    if launcher_text.count(old_bool_gate) != 1:
        raise RuntimeError("launcher strict-bool identity gate anchor not unique")
    launcher_text = launcher_text.replace(old_bool_gate, new_bool_gate, 1)
    if launcher_text.count(old_final_call) != 1:
        raise RuntimeError("launcher final-audit call anchor not unique")
    launcher_text = launcher_text.replace(old_final_call, new_final_call, 1)
    launcher_raw = launcher_text.encode("utf-8")
    compile_source(launcher_raw, NEW["launcher"])
    launcher_sha = digest(launcher_raw)

    # The launcher repair changes executable AST, so the inherited r62 audit's
    # pin-normalized digest and A/B callsite census are no longer authoritative.
    # Recompute those witnesses from the exact in-memory successor bytes before
    # closing the audit object.  The checker deliberately labels rows by the
    # stable role names (producer/consumer/launcher), which keeps the census
    # independent of the physical round filename.
    launcher_ns: dict[str, Any] = {
        "__name__": "_c79g_generated_launcher_metrics",
        "__file__": NEW["launcher"],
    }
    exec(compile(launcher_raw, NEW["launcher"], "exec"),
         launcher_ns, launcher_ns)
    normalized_launcher = launcher_ns[
        "pin_normalized_launcher_ast_sha256"](
            launcher_raw, "generated r63 successor launcher")
    checker_ns = runpy.run_path(
        str(ROOT / "scripts/c79g_v15_checker_census.py"),
        run_name="_c79g_checker_census_metrics")
    ordered_sources = [
        ("producer", producer_raw),
        ("consumer", consumer_raw),
        ("launcher", launcher_raw),
    ]
    rows_a, kinds_a, arity_a = checker_ns[
        "callsite_census_parent_map"](ordered_sources)
    rows_b, kinds_b, arity_b = checker_ns[
        "callsite_census_visitor"](ordered_sources)
    if rows_a != rows_b or kinds_a != kinds_b or arity_a or arity_b:
        raise RuntimeError("successor dual callsite census mismatch")
    common_digest = digest(checker_ns["canonical"](rows_b))
    common_count = len(rows_b)
    common_kinds = {
        kind: kinds_b.get(kind, 0)
        for kind in checker_ns["CALLSITE_KINDS"]
    }
    dual = audit.get("dual_independent_static_checkers")
    if not isinstance(dual, dict):
        raise RuntimeError("successor static audit checker object missing")
    checker_a = dual.get("checker_A")
    checker_b = dual.get("checker_B")
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction")
    if not all(isinstance(item, dict)
               for item in (checker_a, checker_b, checker_c)):
        raise RuntimeError("successor static audit checker objects malformed")
    for checker in (checker_a, checker_b):
        inputs = checker.get("input_sha256")
        if not isinstance(inputs, dict):
            raise RuntimeError("successor static audit checker inputs missing")
        inputs["launcher_template"] = normalized_launcher
        checker["pin_normalized_launcher_ast_sha256"] = normalized_launcher
    checker_a["wider_local_callsite_census_row_count"] = common_count
    checker_a["wider_local_callsite_census_sha256"] = common_digest
    checker_b["common_ordered_callsite_row_count"] = common_count
    checker_b["common_ordered_callsite_census_sha256"] = common_digest
    checker_c.update({
        "pin_normalized_launcher_ast_sha256": normalized_launcher,
        "common_ordered_callsite_row_count": common_count,
        "common_ordered_callsite_census_sha256": common_digest,
        "common_callsite_kind_census": common_kinds,
    })
    # The r62 audit persisted a descriptive algorithm label that does not
    # equal the launcher's frozen live constant.  Bind the successor witness
    # to the exact executable constant instead of carrying that stale text.
    dual["pin_normalized_ast_algorithm"] = launcher_ns[
        "PIN_NORMALIZED_AST_ALGORITHM"]
    dual["held_launcher_pin_normalized_ast_sha256"] = normalized_launcher
    audit = close_object(audit)
    audit_raw = ordered_json(audit) + b"\n"
    audit_sha = digest(audit_raw)
    audit_obj = audit["object_sha256"]

    # Rebind the launcher to the newly closed audit hash.  Pin normalization
    # must remain stable across this final injection; otherwise fail closed.
    launcher_raw = replace_source(src["launcher"], repl, {
        OLD_SHA["contract"]: contract_sha,
        OLD_SHA["contract_obj"]: contract_obj,
        OLD_SHA["producer"]: producer_sha,
        OLD_SHA["consumer"]: consumer_sha,
        OLD_SHA["transition"]: transition_sha,
        OLD_SHA["transition_obj"]: transition_obj,
        OLD_SHA["audit"]: audit_sha,
        OLD_SHA["audit_obj"]: audit_obj,
    })
    # Reapply the source-level v13 receipt fix to this second launcher pass.
    launcher_text = launcher_raw.decode("utf-8")
    launcher_text = retag_current_runtime_targets(
        launcher_text, NEW["launcher"], launcher=True)
    if launcher_text.count(old_signature) != 1:
        raise RuntimeError("launcher v13-audit signature lost on final pass")
    launcher_text = launcher_text.replace(old_signature, new_signature, 1)
    if launcher_text.count(old_v13_call) != 1:
        raise RuntimeError("launcher v13-audit call lost on final pass")
    launcher_text = launcher_text.replace(old_v13_call, new_v13_call, 1)
    if launcher_text.count(old_final_call) != 1:
        raise RuntimeError("launcher final-audit call lost on final pass")
    launcher_text = launcher_text.replace(old_final_call, new_final_call, 1)
    if launcher_text.count(old_bool_gate) != 1:
        raise RuntimeError("launcher strict-bool identity gate lost on final pass")
    launcher_text = launcher_text.replace(old_bool_gate, new_bool_gate, 1)
    launcher_raw = launcher_text.encode("utf-8")
    compile_source(launcher_raw, NEW["launcher"])
    if launcher_ns["pin_normalized_launcher_ast_sha256"](
            launcher_raw, "generated r63 successor launcher final") != \
            normalized_launcher:
        raise RuntimeError("successor launcher pin-normalized AST drift")
    launcher_sha = digest(launcher_raw)

    exact8 = [
        {"path": V14_PATH, "file_sha256": V14_SHA},
        {"path": f"deliverables/{NEW['schema']}", "file_sha256": OLD_SHA["schema"]},
        {"path": f"deliverables/{NEW['contract']}", "file_sha256": contract_sha},
        {"path": f"deliverables/{NEW['producer']}", "file_sha256": producer_sha},
        {"path": f"deliverables/{NEW['consumer']}", "file_sha256": consumer_sha},
        {"path": f"deliverables/{NEW['transition']}", "file_sha256": transition_sha},
        {"path": f"deliverables/{NEW['audit']}", "file_sha256": audit_sha},
        {"path": f"deliverables/{NEW['launcher']}", "file_sha256": launcher_sha},
    ]
    manifest_raw = b"".join((row["file_sha256"] + "  " + row["path"] + "\n").encode("ascii")
                            for row in exact8)
    manifest_sha = digest(manifest_raw)
    outer_body: dict[str, Any] = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2",
        "status": "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": exact8,
        "cold_launch_manifest": {"path": f"deliverables/{NEW['manifest']}",
                                 "file_sha256": manifest_sha,
                                 "ordered_entry_count": 8},
        "cold_launcher": {"path": f"deliverables/{NEW['launcher']}",
                          "file_sha256": launcher_sha},
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": ["EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
                                   "PYTHON3_ISOLATED_INTERPRETER",
                                   "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    }
    outer = close_object(outer_body)
    outer_raw = canon(outer) + b"\n"
    outer_sha = digest(outer_raw)
    # A new receipt is evidence of the successor construction, not runtime
    # authority.  It is intentionally written last by install().
    receipt_body: dict[str, Any] = {
        "schema": "cm2.c79g.v16r2r63.runtime-repair-successor.v1",
        "status": "PASS_APPEND_ONLY_R63_RUNTIME_REPAIR_BUNDLE__ZERO_CREDIT__RUNTIME_DEFERRED",
        "predecessor_namespace": "v16r2r62",
        "predecessor_anchor_path": str(R62_ANCHOR.relative_to(ROOT)),
        "predecessor_anchor_file_sha256": R62_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R62_ANCHOR_OBJECT,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": "v16r2r63_repair_physical_bundle",
        "exact8_ordered_entries": exact8,
        "manifest_path": f"deliverables/{NEW['manifest']}",
        "manifest_file_sha256": manifest_sha,
        "outer_path": f"deliverables/{NEW['outer']}",
        "outer_file_sha256": outer_sha,
        "outer_object_sha256": outer["object_sha256"],
        "r62_failed_publication_preserved": True,
        "r63_diagnostic_repair_preserved": True,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "overwrite_delete_or_reuse_allowed": False,
    }
    receipt = close_object(receipt_body)
    receipt_raw = canon(receipt) + b"\n"
    generated = {
        "contract": contract_raw, "producer": producer_raw,
        "consumer": consumer_raw, "transition": transition_raw,
        "audit": audit_raw, "launcher": launcher_raw,
        "manifest": manifest_raw, "outer": outer_raw,
        "receipt": receipt_raw,
        # Existing schema is an exact8 member and must remain immutable.
        "schema": src["schema"],
    }
    meta = {
        "sha256": {k: digest(v) for k, v in generated.items()},
        "object_sha256": {"contract": contract_obj, "transition": transition_obj,
                           "audit": audit_obj, "outer": outer["object_sha256"],
                           "receipt": receipt["object_sha256"]},
        "exact8": exact8,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    return generated, meta


def exclusive(path: Path, raw: bytes, mode: int = 0o444) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        off = 0
        while off < len(raw):
            n = os.write(fd, raw[off:])
            if n <= 0:
                raise RuntimeError(f"short write: {path}")
            off += n
        os.fsync(fd)
        os.fchmod(fd, mode)
        os.fsync(fd)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    st = os.stat(path, follow_symlinks=False)
    if st.st_nlink != 1 or (st.st_mode & 0o777) != mode:
        raise RuntimeError(f"output identity/mode drift: {path}")


def install(generated: dict[str, bytes]) -> None:
    targets = {
        "contract": OUT / NEW["contract"], "producer": OUT / NEW["producer"],
        "consumer": OUT / NEW["consumer"], "transition": OUT / NEW["transition"],
        "audit": OUT / NEW["audit"], "launcher": OUT / NEW["launcher"],
        "manifest": OUT / NEW["manifest"], "outer": OUT / NEW["outer"],
        "receipt": OUT / NEW["receipt"],
    }
    occupied = [str(p) for p in targets.values() if p.exists() or p.is_symlink()]
    if occupied:
        raise RuntimeError("successor target already exists; never overwrite: " + ",".join(occupied))
    # Source and JSON members are frozen before manifest; manifest before outer;
    # receipt records the complete publication and is last.
    for key in ("contract", "producer", "consumer", "transition", "audit", "launcher"):
        exclusive(targets[key], generated[key], 0o444)
    exclusive(targets["manifest"], generated["manifest"], 0o444)
    exclusive(targets["outer"], generated["outer"], 0o444)
    exclusive(targets["receipt"], generated["receipt"], 0o444)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("preflight", "install"), nargs="?", default="preflight")
    args = parser.parse_args(argv)
    try:
        generated, meta = construct()
        result = {"schema": "cm2.c79g.v16r2r63.runtime-repair-builder.v1",
                  "status": "PASS_R63_RUNTIME_REPAIR_PREFLIGHT__ZERO_CREDIT" if args.action == "preflight" else "PASS_R63_RUNTIME_REPAIR_BUNDLE_INSTALLED__ZERO_CREDIT",
                  "meta": meta, "install": args.action == "install"}
        if args.action == "install":
            install(generated)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": "cm2.c79g.v16r2r63.runtime-repair-builder.failure.v1",
                          "status": "FAIL_CLOSED_R63_RUNTIME_REPAIR_PREFLIGHT" if args.action == "preflight" else "FAIL_CLOSED_R63_RUNTIME_REPAIR_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
