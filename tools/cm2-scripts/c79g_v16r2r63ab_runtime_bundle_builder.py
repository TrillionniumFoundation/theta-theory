#!/usr/bin/env python3
"""Construct the append-only r63ab successor with the live 74-key registry.

The r63aa recipe is retained as an immutable witness.  This thin wrapper
patches the next in-memory recipe before it writes anything: it adds the two
frozen incident-authority fields required by the consumer, aligns all three
source validators to the resulting 66+7+1 registry shape, and updates the
static-audit evidence that those validators consume.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63aa_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "dd672709f7030d16a6b4f3c8ca1a03189e43c6e366d60e5354e8fa173f92e561"


def _replacement_code(target: str, label: str,
                     replacements: list[tuple[str, str, int]]) -> str:
    """Return source statements which apply exact, counted replacements."""
    nl = chr(10)
    out = [f"    {label}_replacements = ["]
    for old, new, count in replacements:
        out.append(f"        ({old!r}, {new!r}, {count}),")
    out.extend([
        "    ]",
        f"    for old, new, count in {label}_replacements:",
        f"        if {target}.count(old) != count:",
        f'            raise RuntimeError("r63ab {label} replacement anchor drift")',
        f"        {target} = {target}.replace(old, new, count)",
    ])
    return nl.join(out) + nl


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63aa builder template hash drift")
    text = raw.decode("utf-8").replace("r63aa", "r63ab")
    nl = chr(10)

    # The aa producer has the aggregate history field but is still short two
    # members relative to the consumer's closed registry schema.  Insert the
    # fields immediately before that aggregate so ordering remains stable.
    producer_anchor = (
        '        "append_only_history_unique_file_identity_count":\n'
        '            V16R2_TERMINAL_UNIQUE_LIVE_IDENTITY_COUNT,\n')
    producer_value = (
        '        "frozen_predecessor_incident_source_exact10_held_fd_bytes_read_only": True,\n'
        '        "frozen_predecessor_incident_sources_used_only_for_noncredit_regression_authority": True,\n'
        + producer_anchor)
    producer_patch = (
        "    r63ab_registry_anchor = " + repr(producer_anchor) + nl
        + "    r63ab_registry_value = " + repr(producer_value) + nl
        + "    if producer_text.count(r63ab_registry_anchor) != 1:" + nl
        + '        raise RuntimeError("r63ab producer registry-field anchor not unique")' + nl
        + "    producer_text = producer_text.replace(" + nl
        + "        r63ab_registry_anchor, r63ab_registry_value, 1)" + nl
        + _replacement_code(
            "producer_text", "producer_shapes", [
                ('"producerSourceRegistry": 75', '"producerSourceRegistry": 74', 1),
            ])
    )

    # The consumer's static audit predicate must agree with the producer's
    # renamed ten-incident execution-proof descriptors and the 74-key shape.
    consumer_patch = _replacement_code(
        "consumer_text", "consumer_live", [
            ('"producerSourceRegistry": 75', '"producerSourceRegistry": 74', 1),
            ('get("explicit_key_count") == 67', 'get("explicit_key_count") == 66', 1),
            ('get("explicit_unique_key_count") == 67', 'get("explicit_unique_key_count") == 66', 1),
            ('get("computed_closed_registry_key_count") == 75', 'get("computed_closed_registry_key_count") == 74', 1),
            ('get("explicit_key_guard_literals") == [67]', 'get("explicit_key_guard_literals") == [66]', 1),
            ('             "held_producer_independent_computed_shape") == 75',
             '             "held_producer_independent_computed_shape") == 74', 1),
            ('get("producer_independent_closed_key_count") == 75', 'get("producer_independent_closed_key_count") == 74', 1),
            ('get("audit_declared_producerSourceRegistry") == 75', 'get("audit_declared_producerSourceRegistry") == 74', 1),
            ('set(values) == {75}', 'set(values) == {74}', 1),
            ('get("expected_closed_key_count") == 75', 'get("expected_closed_key_count") == 74', 1),
            ('get("actual_closed_registry_shape") == 75', 'get("actual_closed_registry_shape") == 74', 1),
            ('exact75', 'exact74', 2),
            ('twelve_v14_inherited_authority_inputs_inherited_as_held_fds',
             'ten_incident_authority_inputs_inherited_as_held_fds', 1),
            ('twelve_v14_inherited_authority_held_fds_path_identity_mount_and_hash_revalidated',
             'ten_incident_held_fds_path_identity_mount_and_hash_revalidated', 1),
        ])

    # The launcher has two source-construction passes.  Apply the live shape
    # repair before each encode; the historical V14 incident literals remain
    # untouched because every replacement below is a narrow live-site anchor.
    launcher_patch = _replacement_code(
        "launcher_text", "launcher_live", [
            ("'producerSourceRegistry': 75", "'producerSourceRegistry': 74", 1),
            ('explicit67 + execution-proof7 + object closure1 structurally',
             'explicit66 + execution-proof7 + object closure1 structurally', 1),
            ('len(explicit_keys) == len(set(explicit_keys)) == 67',
             'len(explicit_keys) == len(set(explicit_keys)) == 66', 1),
            ('current v16r2 registry explicit67 plus exact execution-proof7',
             'current v16r2 registry explicit66 plus exact execution-proof7', 1),
            ('need(shape == 75,', 'need(shape == 74,', 1),
            ('current v16r2 producerSourceRegistry exact explicit67 plus execution-proof7 plus enclosing-object1 equals 75',
             'current v16r2 producerSourceRegistry exact explicit66 plus execution-proof7 plus enclosing-object1 equals 74', 1),
            ("runtime_registry_evidence.get('actual_closed_registry_shape') == 75",
             "runtime_registry_evidence.get('actual_closed_registry_shape') == 74", 1),
            ("producer_registry.get('explicit_key_count') == 67",
             "producer_registry.get('explicit_key_count') == 66", 1),
            ("producer_registry.get('computed_closed_registry_key_count') == 75",
             "producer_registry.get('computed_closed_registry_key_count') == 74", 1),
            ("launcher_registry.get('explicit_key_guard_literals') == [67]",
             "launcher_registry.get('explicit_key_guard_literals') == [66]", 1),
            ("launcher_registry.get('held_producer_independent_computed_shape') == 75",
             "launcher_registry.get('held_producer_independent_computed_shape') == 74", 1),
            ("registry_consensus.get('producer_independent_closed_key_count') == 75",
             "registry_consensus.get('producer_independent_closed_key_count') == 74", 1),
            ("registry_consensus.get('audit_declared_producerSourceRegistry') == 75",
             "registry_consensus.get('audit_declared_producerSourceRegistry') == 74", 1),
            ("registry_consensus.get('expected_closed_key_count') == 75",
             "registry_consensus.get('expected_closed_key_count') == 74", 1),
            ("computed_registry_shape == expected_shapes['producerSourceRegistry'] == 75",
             "computed_registry_shape == expected_shapes['producerSourceRegistry'] == 74", 1),
        ])

    # The persisted audit is consumed by all three surfaces.  Change only the
    # live registry-evidence subtree and the output-shape census, then let the
    # immutable recipe recompute its object/hash closure.
    audit_patch = (
        "    r63ab_evidence = audit[\"dual_independent_static_checkers\"][\"actual_runtime_registry_shape_evidence\"]" + nl
        + "    r63ab_producer_census = r63ab_evidence[\"producer_source_registry_census\"]" + nl
        + "    r63ab_launcher_census = r63ab_evidence[\"launcher_runtime_registry_helper_census\"]" + nl
        + "    r63ab_consensus = r63ab_evidence[\"runtime_registry_shape_consensus\"]" + nl
        + "    r63ab_producer_census[\"explicit_key_count\"] = 66" + nl
        + "    r63ab_producer_census[\"explicit_unique_key_count\"] = 66" + nl
        + "    r63ab_producer_census[\"computed_closed_registry_key_count\"] = 74" + nl
        + "    r63ab_producer_census[\"execution_proof_keys\"] = [" + nl
        + '        "producer_exec_fd_is_fresh_sealed_memfd",' + nl
        + '        "producer_exec_fd_distinct_from_installed_source_fd",' + nl
        + '        "producer_exec_memfd_required_seals_valid",' + nl
        + '        "producer_exec_bytes_equal_installed_source_bytes",' + nl
        + '        "producer_exec_and_installed_source_terminal_replayed",' + nl
        + '        "ten_incident_authority_inputs_inherited_as_held_fds",' + nl
        + '        "ten_incident_held_fds_path_identity_mount_and_hash_revalidated",' + nl
        + "    ]" + nl
        + "    r63ab_launcher_census[\"explicit_key_guard_literals\"] = [66]" + nl
        + "    r63ab_launcher_census[\"held_producer_independent_computed_shape\"] = 74" + nl
        + "    r63ab_consensus[\"producer_independent_closed_key_count\"] = 74" + nl
        + "    r63ab_consensus[\"audit_declared_producerSourceRegistry\"] = 74" + nl
        + "    r63ab_consensus[\"expected_closed_key_count\"] = 74" + nl
        + "    r63ab_consensus[\"source_declared_producerSourceRegistry_values\"] = {" + nl
        + '        "producer": [74], "consumer": [74], "launcher": [74]}' + nl
        + "    r63ab_evidence[\"actual_closed_registry_shape\"] = 74" + nl
        + "    audit[\"schema_and_constructor_closure\"][\"output_shape_key_counts\"][\"producerSourceRegistry\"] = 74" + nl
    )

    # aa's loader already carries its producer repair into the x/base recipe.
    # Extend that same in-memory loader with the successor repairs.  This
    # keeps all writes append-only and guarantees the generated bytes are
    # rebuilt from the frozen r62 inputs rather than edited in place.
    extra_loader_code = (
        "    r63ab_producer_needle = " + repr(
            '    producer_raw = producer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ab_producer_needle) != 1:" + nl
        + '        raise RuntimeError("r63ab producer insertion anchor drift")' + nl
        + "    text = text.replace(r63ab_producer_needle, " + repr(producer_patch) + "+ r63ab_producer_needle, 1)" + nl
        + "    r63ab_consumer_needle = " + repr(
            '    consumer_raw = consumer_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ab_consumer_needle) != 1:" + nl
        + '        raise RuntimeError("r63ab consumer insertion anchor drift")' + nl
        + "    text = text.replace(r63ab_consumer_needle, " + repr(consumer_patch) + "+ r63ab_consumer_needle, 1)" + nl
        + "    r63ab_launcher_needle = " + repr(
            '    launcher_raw = launcher_text.encode("utf-8")\n') + nl
        + "    if text.count(r63ab_launcher_needle) != 2:" + nl
        + '        raise RuntimeError("r63ab launcher insertion anchor drift")' + nl
        + "    text = text.replace(r63ab_launcher_needle, " + repr(launcher_patch) + "+ r63ab_launcher_needle)" + nl
        + "    r63ab_audit_needle = " + repr(
            '    audit = close_object(audit)\n') + nl
        + "    if text.count(r63ab_audit_needle) != 2:" + nl
        + '        raise RuntimeError("r63ab audit insertion anchor drift")' + nl
        + "    text = text.replace(r63ab_audit_needle, " + repr(audit_patch) + "+ r63ab_audit_needle, 1)" + nl
    )

    loader_anchor = (
        '        "+ producer_needle, 1)" + nl\n'
        '    )')
    loader_replacement = (
        '        "+ producer_needle, 1)" + nl\n'
        '        + ' + repr(extra_loader_code) + '\n'
        '    )')
    if text.count(loader_anchor) != 1:
        raise RuntimeError("r63ab builder-loader injection anchor drift")
    text = text.replace(loader_anchor, loader_replacement, 1)
    ns = {
        "__name__": "_c79g_r63ab_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ab_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
