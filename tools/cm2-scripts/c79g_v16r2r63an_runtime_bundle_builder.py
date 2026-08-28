#!/usr/bin/env python3
"""Construct the append-only r63an declared/physical path successor.

r63am closed the live binding-equalities shape, but its serialized witnesses
still exposed the fresh physical r63am publication names where the frozen
v16r2/r57 schema requires the stable declared names.  This wrapper keeps the
r63am recipe and every byte of its rejection history immutable.  It patches
only the in-memory constructor immediately before each affected object is
hashed; runtime filesystem constants, held descriptors, and rename targets
remain round-scoped r63an paths.
"""
from __future__ import annotations

import builtins
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63am_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "567368c63495e4e4fc8d5c56eab10d41058c0eeb0a30fd3e13d3ce16fa0e3cae"
MARKER = "_R63AN_DECLARED_PHYSICAL_PROJECTION_APPLIED_"


def _contract_patch() -> str:
    """Source inserted into the base constructor before contract closure."""
    return '''    # _R63AN_DECLARED_PHYSICAL_PROJECTION_APPLIED_
    _r63an_paths = contract_value.get("exact_publication_paths")
    if not isinstance(_r63an_paths, dict):
        raise RuntimeError("r63an exact-publication path object missing")
    _r63an_paths.update({
        "candidate_A": ".cm2-runtime/c79g-v16r2-candidate-a-" + CHECKPOINT,
        "candidate_B": ".cm2-runtime/c79g-v16r2-candidate-b-" + CHECKPOINT,
        "verification_A": ".cm2-runtime/c79g-v16r2-verification-a-" + CHECKPOINT,
        "verification_B": ".cm2-runtime/c79g-v16r2-verification-b-" + CHECKPOINT,
        "committed_completion": ".cm2-runtime/c79g-v16r2-committed-completion-" + CHECKPOINT,
        "v16r2_rejection_namespace": ".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT,
        "v16r2_later_rejection": ".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT + "/rejection.json",
        "candidate_staging_path_template":
            ".cm2-runtime/.c79g-v16r2-candidate-stage-{a|b}-" + CHECKPOINT,
        "candidate_staging_prefix": ".cm2-runtime/.c79g-v16r2-candidate-stage-{a|b}-",
        "verification_staging_path_template":
            ".cm2-runtime/.c79g-v16r2-verification-stage-{a|b}-" + CHECKPOINT,
        "verification_staging_prefix": ".cm2-runtime/.c79g-v16r2-verification-stage-{a|b}-",
        "completion_staging_path": ".cm2-runtime/.c79g-v16r2-completion-stage-" + CHECKPOINT,
        "completion_staging_prefix": ".cm2-runtime/.c79g-v16r2-completion-stage-",
        "authority_seal": ".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-" + CHECKPOINT + ".seal",
        "authority_staging_path":
            ".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-" + CHECKPOINT + ".seal",
        "authority_staging_prefix": ".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-",
    })
    _r63an_no_later = contract_value.get("no_later_rejection_protocol")
    if not isinstance(_r63an_no_later, dict):
        raise RuntimeError("r63an no-later-rejection protocol missing")
    _r63an_no_later.update({
        "deterministic_target_exact_path":
            ".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT + "/rejection.json",
        "namespace_exact_path": ".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT,
    })
    _r63an_completion = contract_value.get("completion_protocol")
    if not isinstance(_r63an_completion, dict):
        raise RuntimeError("r63an completion protocol missing")
    _r63an_completion["completion_member_order"] = [
        "cm2_round306c79g_true_global_no_producer_consumer_completion_verification_copy_v16r2.json",
        "cm2_round306c79g_true_global_no_producer_consumer_pre_outer_completion_receipt_v16r2.json",
        "cm2_round306c79g_true_global_no_producer_consumer_one_global_manifest_v16r2.sha256",
        "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r57.json",
    ]
'''


def _producer_patch() -> str:
    """Project only the candidate-install descriptor in producer output."""
    return '''    _r63an_producer_replacements = [
        ("\\\".cm2-runtime/.c79g-v16r2r63an-candidate-stage-{a|b}-\\\" + UPSTREAM_CHECKPOINT_OBJECT_PIN",
         "\\\".cm2-runtime/.c79g-v16r2-candidate-stage-{a|b}-\\\" + UPSTREAM_CHECKPOINT_OBJECT_PIN"),
        ("str(CANDIDATE_A.relative_to(ROOT))",
         '".cm2-runtime/c79g-v16r2-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN'),
        ("str(CANDIDATE_B.relative_to(ROOT))",
         '".cm2-runtime/c79g-v16r2-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN'),
    ]
    for _r63an_old, _r63an_new in _r63an_producer_replacements:
        if producer_text.count(_r63an_old) != 1:
            raise RuntimeError("r63an producer declared-path anchor drift")
        producer_text = producer_text.replace(_r63an_old, _r63an_new, 1)
'''


def _consumer_declared_block() -> str:
    return '''DECLARED_CANDIDATE_A = ".cm2-runtime/c79g-v16r2-candidate-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_CANDIDATE_B = ".cm2-runtime/c79g-v16r2-candidate-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_VERIFICATION_A = ".cm2-runtime/c79g-v16r2-verification-a-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_VERIFICATION_B = ".cm2-runtime/c79g-v16r2-verification-b-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_COMMITTED_COMPLETION = ".cm2-runtime/c79g-v16r2-committed-completion-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_REJECTION_NAMESPACE = ".cm2-runtime/c79g-v16r2-rejections-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_LATER_REJECTION = DECLARED_REJECTION_NAMESPACE + "/rejection.json"
DECLARED_CANDIDATE_STAGE_TEMPLATE = ".cm2-runtime/.c79g-v16r2-candidate-stage-{a|b}-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_VERIFICATION_STAGE_TEMPLATE = ".cm2-runtime/.c79g-v16r2-verification-stage-{a|b}-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_COMPLETION_STAGE = ".cm2-runtime/.c79g-v16r2-completion-stage-" + UPSTREAM_CHECKPOINT_OBJECT_PIN
DECLARED_PRODUCER_PATH = "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v16r2r57_semantic_source.py"
DECLARED_CONSUMER_PATH = "deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r57_semantic_source.py"
DECLARED_INDEPENDENT_CONSUMER_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r57.independent-consumer-proof"
DECLARED_STANDALONE_OUTER_SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r57.standalone-final-outer"
DECLARED_COMPLETION_MEMBERS = (
    "cm2_round306c79g_true_global_no_producer_consumer_completion_verification_copy_v16r2.json",
    "cm2_round306c79g_true_global_no_producer_consumer_pre_outer_completion_receipt_v16r2.json",
    "cm2_round306c79g_true_global_no_producer_consumer_one_global_manifest_v16r2.sha256",
    "cm2_round306c79g_true_global_no_producer_consumer_cold_launch_outer_receipt_v16r2r57.json",
)
'''


def _consumer_patch() -> str:
    """Project schema-facing consumer serializers while retaining physical IO."""
    block = _consumer_declared_block()
    # Replacements are source-level expressions, not runtime filesystem edits.
    replacements = [
        ('str(CANDIDATE_A.relative_to(ROOT))', 'DECLARED_CANDIDATE_A', 4),
        ('str(CANDIDATE_B.relative_to(ROOT))', 'DECLARED_CANDIDATE_B', 4),
        ('str(VERIFICATION_A.relative_to(ROOT))', 'DECLARED_VERIFICATION_A', 3),
        ('str(VERIFICATION_B.relative_to(ROOT))', 'DECLARED_VERIFICATION_B', 3),
        ('str(COMMITTED_COMPLETION.relative_to(ROOT))', 'DECLARED_COMMITTED_COMPLETION', 3),
        ('str(REJECTION_NAMESPACE.relative_to(ROOT))', 'DECLARED_REJECTION_NAMESPACE', 4),
        ('str(LATER_REJECTION.relative_to(ROOT))', 'DECLARED_LATER_REJECTION', 4),
        ('".cm2-runtime/.c79g-v16r2r63an-candidate-stage-{a|b}-" + UPSTREAM_CHECKPOINT_OBJECT_PIN', 'DECLARED_CANDIDATE_STAGE_TEMPLATE', 1),
        ('".cm2-runtime/.c79g-v16r2r63an-candidate-stage-{a|b}-" +\n            UPSTREAM_CHECKPOINT_OBJECT_PIN', 'DECLARED_CANDIDATE_STAGE_TEMPLATE', 1),
        ('".cm2-runtime/.c79g-v16r2r63an-verification-stage-{a|b}-" +\n            UPSTREAM_CHECKPOINT_OBJECT_PIN', 'DECLARED_VERIFICATION_STAGE_TEMPLATE', 1),
        ('str(COMPLETION_STAGE.relative_to(ROOT))', 'DECLARED_COMPLETION_STAGE', 1),
        ('str(stage.relative_to(ROOT))', 'DECLARED_COMPLETION_STAGE', 1),
        ('list(COMPLETION_MEMBERS)', 'list(DECLARED_COMPLETION_MEMBERS)', 1),
        ('SCHEMA + ".independent-consumer-proof"', 'DECLARED_INDEPENDENT_CONSUMER_SCHEMA', 1),
        ('SCHEMA + ".standalone-final-outer"', 'DECLARED_STANDALONE_OUTER_SCHEMA', 1),
        ('"path": str(PRODUCER_SOURCE.relative_to(ROOT)),', '"path": DECLARED_PRODUCER_PATH,', 1),
        ('"path": str(SELF.relative_to(ROOT)),', '"path": DECLARED_CONSUMER_PATH,', 1),
        ('consumer_proof.get("consumer_SELF_identity", {}).get("path") ==\n             str(SELF.relative_to(ROOT))', 'consumer_proof.get("consumer_SELF_identity", {}).get("path") ==\n             DECLARED_CONSUMER_PATH', 1),
    ]
    lines = [
        '    _r63an_decl_anchor = "AUTHORITY_SEAL_SCHEMA ="',
        '    if consumer_text.count(_r63an_decl_anchor) != 1:',
        '        raise RuntimeError("r63an consumer declaration anchor drift")',
        f'    _r63an_decl_block = {block!r}',
        '    _r63an_decl_pos = consumer_text.index(_r63an_decl_anchor)',
        '    consumer_text = (consumer_text[:_r63an_decl_pos] +',
        '                     _r63an_decl_block +',
        '                     consumer_text[_r63an_decl_pos:])',
        '    _r63an_consumer_replacements = [',
    ]
    for old, new, count in replacements:
        lines.append(f'        ({old!r}, {new!r}, {count}),')
    lines.extend([
        '    ]',
        '    for _r63an_old, _r63an_new, _r63an_count in _r63an_consumer_replacements:',
        '        if consumer_text.count(_r63an_old) != _r63an_count:',
        '            raise RuntimeError("r63an consumer declared-path anchor drift")',
        '        consumer_text = consumer_text.replace(_r63an_old, _r63an_new, _r63an_count)',
        '    _r63an_stage_old = \'    recorded_stage = rooted(install_proof["staging_path"])\\n\'',
        '    _r63an_stage_new = (',
        '        \'    _r63an_recorded_stage = install_proof["staging_path"]\\n\'',
        '        \'    need(_r63an_recorded_stage == DECLARED_COMPLETION_STAGE,\\n\'',
        '        \'         "committed completion records declared generic completion stage")\\n\'',
        '        \'    recorded_stage = COMPLETION_STAGE\\n\'',
        '    )',
        '    if consumer_text.count(_r63an_stage_old) != 1:',
        '        raise RuntimeError("r63an completion-stage resolver anchor drift")',
        '    consumer_text = consumer_text.replace(_r63an_stage_old, _r63an_stage_new, 1)',
    ])
    return "\n".join(lines) + "\n"


def _launcher_patch() -> str:
    """Project launcher-only child and native rejection receipt paths."""
    return '''    _r63an_launcher_replacements = [
        ("str(V16R2_REJECTION_NAMESPACE.relative_to(ROOT))",
         '".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT'),
        ("str(V16R2_LATER_REJECTION.relative_to(ROOT))",
         '".cm2-runtime/c79g-v16r2-rejections-" + CHECKPOINT + "/rejection.json"'),
        ("str(CONSUMER.relative_to(ROOT))",
         '"deliverables/cm2_round306c79g_true_global_no_producer_consumer_independent_verifier_assembler_authority_consumer_v16r2r57_semantic_source.py"'),
    ]
    for _r63an_old, _r63an_new in _r63an_launcher_replacements:
        if launcher_text.count(_r63an_old) != 1:
            raise RuntimeError("r63an launcher declared-path anchor drift")
        launcher_text = launcher_text.replace(_r63an_old, _r63an_new, 1)
'''


def _patch_base_source(source_text: str) -> str:
    if MARKER in source_text:
        return source_text
    if "def construct() -> tuple[dict[str, bytes], dict[str, Any]]:" not in source_text:
        return source_text
    # These anchors are unique in the actual base constructor and absent from
    # the nested wrapper source literals.
    close_anchor = "    contract_value = close_object(contract_value)\n"
    producer_anchor = '    producer_raw = producer_text.encode("utf-8")\n'
    consumer_anchor = '    consumer_raw = consumer_text.encode("utf-8")\n'
    launcher_anchor = '    launcher_raw = launcher_text.encode("utf-8")\n'
    if source_text.count(close_anchor) != 1:
        return source_text
    if source_text.count(producer_anchor) != 1:
        raise RuntimeError("r63an producer anchor drift")
    if source_text.count(consumer_anchor) != 1:
        raise RuntimeError("r63an consumer anchor drift")
    if source_text.count(launcher_anchor) != 2:
        raise RuntimeError("r63an launcher anchor drift")
    source_text = source_text.replace(close_anchor, _contract_patch() + close_anchor, 1)
    source_text = source_text.replace(producer_anchor, _producer_patch() + producer_anchor, 1)
    source_text = source_text.replace(consumer_anchor, _consumer_patch() + consumer_anchor, 1)
    source_text = source_text.replace(launcher_anchor, _launcher_patch() + launcher_anchor)
    return source_text


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63am builder template hash drift")
    text = raw.decode("utf-8").replace("r63am", "r63an")
    real_compile = builtins.compile

    def patched_compile(source, filename, mode, *args, **kwargs):
        source_is_bytes = isinstance(source, (bytes, bytearray))
        if source_is_bytes:
            source_text = bytes(source).decode("utf-8")
        elif isinstance(source, str):
            source_text = source
        else:
            return real_compile(source, filename, mode, *args, **kwargs)
        if MARKER not in source_text:
            source_text = _patch_base_source(source_text)
            if source_text != source:
                source = source_text.encode("utf-8") if source_is_bytes else source_text
        return real_compile(source, filename, mode, *args, **kwargs)

    builtins.compile = patched_compile
    try:
        ns = {
            "__name__": "_c79g_r63an_builder_template",
            "__file__": str(ROOT / "scripts/c79g_v16r2r63an_runtime_bundle_builder.py"),
        }
        exec(real_compile(text, str(TEMPLATE), "exec"), ns, ns)
        return int(ns["main"](sys.argv[1:] if argv is None else argv))
    finally:
        builtins.compile = real_compile


if __name__ == "__main__":
    raise SystemExit(main())
