#!/usr/bin/env python3
"""Recompute every authoritative v5 trace after attacks, before postcheck."""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Any

_DELIVERABLES_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _DELIVERABLES_BOOTSTRAP not in sys.path:
    sys.path.insert(0, _DELIVERABLES_BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common
import cm2_round306c30a_supplemental_audit_closure_v5_trace_lib as traces


sys.dont_write_bytecode = True


def _manifest_stdout() -> bytes:
    cap = common.capture(common.BASE_MANIFEST_REL)
    common.require(cap.raw is not None, "base manifest retained")
    rows = common.parse_manifest(cap.raw, "base manifest")
    return b"".join(name.encode("ascii") + b": OK\n" for name in rows)


def _validate_verifier(root: Path, seed: str) -> dict[str, Any]:
    analyzer = common.load_analyzer()
    pre = common.validate_stage(root, "55_verifier_manifest_pre_seed" + seed)
    stage_name = traces.VERIFIER_STAGES[seed]
    verifier = common.validate_stage(root, stage_name)
    post = common.validate_stage(root, "65_verifier_manifest_post_seed" + seed)
    expected_manifest_stdout = _manifest_stdout()
    common.require(
        pre["stdout"].raw == expected_manifest_stdout
        and post["stdout"].raw == expected_manifest_stdout
        and pre["stderr"].size == 0
        and post["stderr"].size == 0,
        "verifier manifest pre/post exact checks:" + seed,
    )
    common.require(verifier["stdout"].raw is not None, "verifier stdout retained")
    value = common.strict_json(verifier["stdout"].raw, stage_name + " stdout")
    common.require(
        value == analyzer.FIXED_STDOUT_OBJECT,
        "independent verifier fixed result:" + seed,
    )
    analysis = traces.analyze_role(
        root,
        kind="verifier",
        seed=seed,
        source="v5-trace-auditor:verifier:seed" + seed,
    )
    return {
        "manifest_pre_exit_sha256": pre["receipt_capture"].sha256,
        "verifier_exit_sha256": verifier["receipt_capture"].sha256,
        "manifest_post_exit_sha256": post["receipt_capture"].sha256,
        "analysis": analysis,
        "analysis_sha256": common.sha256(common.canonical(analysis)),
    }


def _validate_attacks(root: Path) -> dict[str, Any]:
    stage = common.validate_stage(root, "70_attacks")
    common.require(
        stage["stdout"].raw is not None and stage["stderr"].size == 0,
        "attack harness raw streams",
    )
    stdout = common.strict_json(stage["stdout"].raw, "attack harness stdout")
    summary_cap = common.capture(root / "attacks" / "attack_summary.json")
    common.require(summary_cap.raw is not None, "attack summary retained")
    summary = common.strict_json(summary_cap.raw, "attack summary")
    common.validate_closed(summary, "attack summary")
    common.require(
        stdout == summary
        and stdout.get("schema")
        == "cm2.round306c30a.supplemental-coherent-attacks.v1"
        and stdout.get("status") == "PASS_10_OF_10_COHERENT_ATTACKS_REJECTED"
        and stdout.get("total") == stdout.get("rejected") == 10
        and stdout.get("base_manifest_sha256") == common.BASE_MANIFEST_SHA256,
        "ten coherent attacks summary",
    )
    rows = stdout.get("attacks")
    common.require(type(rows) is list and len(rows) == 10, "attack row census")
    attack_root = root / "attacks"
    expected_top = {"attack_summary.json"}
    expected_top.update(
        f"{ordinal:02d}_{name}"
        for ordinal, name in enumerate(common.ATTACK_NAMES)
    )
    actual_top: set[str] = set()
    for entry in os.scandir(attack_root):
        common.require(not entry.is_symlink(), "attack top-level no symlink")
        common.require(
            entry.is_file(follow_symlinks=False)
            or entry.is_dir(follow_symlinks=False),
            "attack top-level regular kind",
        )
        actual_top.add(entry.name)
    common.require(actual_top == expected_top, "attack exact top-level map")
    evidence: list[dict[str, Any]] = []
    for ordinal, name in enumerate(common.ATTACK_NAMES):
        row = rows[ordinal]
        directory = root / "attacks" / f"{ordinal:02d}_{name}"
        descriptor_cap = common.capture(directory / "attack_descriptor.json")
        exit_cap = common.capture(directory / "verifier.exit.json")
        stdout_cap = common.capture(directory / "verifier.stdout.raw")
        stderr_cap = common.capture(directory / "verifier.stderr.raw")
        directory_entries: dict[str, str] = {}
        for entry in os.scandir(directory):
            common.require(not entry.is_symlink(), "attack directory no symlink")
            if entry.is_file(follow_symlinks=False):
                directory_entries[entry.name] = "file"
            elif entry.is_dir(follow_symlinks=False):
                directory_entries[entry.name] = "directory"
            else:
                raise common.Reject("attack directory special entry")
        common.require(
            directory_entries == {
                "attack_descriptor.json": "file",
                "candidate": "directory",
                "verifier.exit.json": "file",
                "verifier.stderr.raw": "file",
                "verifier.stdout.raw": "file",
            },
            "attack exact evidence map:" + name,
        )
        common.require(
            descriptor_cap.raw is not None and exit_cap.raw is not None,
            "attack retained descriptor/exit",
        )
        descriptor = common.strict_json(
            descriptor_cap.raw, "attack descriptor:" + name
        )
        exit_object = common.strict_json(exit_cap.raw, "attack exit:" + name)
        common.require(
            row.get("ordinal") == ordinal
            and row.get("name") == name
            and row.get("rejected") is True
            and row.get("exit_code") == 1
            and descriptor.get("ordinal") == ordinal
            and descriptor.get("name") == name
            and exit_object.get("exit_code") == 1
            and exit_object.get("stdout_sha256") == stdout_cap.sha256
            and exit_object.get("stdout_size") == stdout_cap.size
            and exit_object.get("stderr_sha256") == stderr_cap.sha256
            and exit_object.get("stderr_size") == stderr_cap.size
            and stdout_cap.size == 0
            and stderr_cap.size > 0,
            "coherent attack independently rejected:" + name,
        )
        candidate = directory / "candidate"
        status = candidate.lstat()
        common.require(
            stat.S_ISDIR(status.st_mode) and not candidate.is_symlink(),
            "attack candidate directory:" + name,
        )
        actual: set[str] = set()
        after_table: list[dict[str, Any]] = []
        for entry in os.scandir(candidate):
            common.require(
                entry.is_file(follow_symlinks=False) and not entry.is_symlink(),
                "attack candidate regular singleton:" + name,
            )
            cap = common.capture(candidate / entry.name, retain=False)
            actual.add(entry.name)
            after_table.append({
                "filename": entry.name, "sha256": cap.sha256, "size": cap.size,
            })
        common.require(actual == set(common.OUTPUT_NAMES),
                       "attack candidate exact map:" + name)
        after_table.sort(key=lambda row: row["filename"])
        before_table = descriptor.get("before_file_table")
        common.require(
            type(before_table) is list
            and len(before_table) == len(common.OUTPUT_NAMES)
            and {row.get("filename"): row.get("sha256") for row in before_table}
            == common.OUTPUT_HASHES
            and descriptor.get("after_file_table") == after_table
            and row.get("after_file_table_sha256")
            == common.sha256(common.canonical(after_table)),
            "attack descriptor/full candidate byte binding:" + name,
        )
        evidence.append({
            "ordinal": ordinal,
            "name": name,
            "descriptor_sha256": descriptor_cap.sha256,
            "verifier_exit_sha256": exit_cap.sha256,
        })
    return {
        "stage_exit_sha256": stage["receipt_capture"].sha256,
        "summary_sha256": summary_cap.sha256,
        "attacks": evidence,
    }


def build(root: Path) -> dict[str, Any]:
    common.validate_base_manifest()
    analyzer = common.load_analyzer()
    comparator_stage = common.validate_stage(root, "50_comparator")
    common.require(comparator_stage["stdout"].raw is not None,
                   "comparator stdout retained")
    comparator = common.strict_json(
        comparator_stage["stdout"].raw, "v5 comparator stdout"
    )
    common.validate_closed(comparator, "v5 comparator stdout")
    common.require(
        comparator.get("status") == (
            "PASS_REAL_DUAL_SEED_SAME_INVOCATION_EVIDENCE__"
            "KERNEL_NETWORK_NONE__ZERO_ADDITIONAL_CREDIT"
        ),
        "v5 comparator PASS",
    )
    producer_rows: dict[str, Any] = {}
    for seed in common.SEEDS:
        recomputed = traces.analyze_role(
            root,
            kind="producer",
            seed=seed,
            source="v5-trace-auditor:producer:seed" + seed,
        )
        embedded = comparator["seeds"][seed]["trace_analysis"]
        common.require(
            embedded.get("contract_source")
            == "v5-comparator:producer:seed" + seed
            and recomputed.get("contract_source")
            == "v5-trace-auditor:producer:seed" + seed
            and embedded.get("analyzer_result_sha256")
            == common.sha256(common.canonical(embedded.get("result")))
            and embedded.get("contract_sha256")
            == common.sha256(analyzer.canonical_bytes(embedded.get("contract")))
            and embedded.get("result", {}).get("contract", {}).get("sha256")
            == embedded.get("contract_sha256")
            and embedded.get("cold_facts_sha256")
            == common.sha256(common.canonical(embedded.get("cold_facts")))
            and comparator["seeds"][seed].get("trace_analysis_sha256")
            == common.sha256(common.canonical(embedded))
            and traces.normalize_result(embedded["result"])
            == traces.normalize_result(recomputed["result"])
            and embedded.get("normalized_analyzer_result_sha256")
            == recomputed.get("normalized_analyzer_result_sha256")
            and embedded.get("cold_facts") == recomputed.get("cold_facts"),
            "comparator/recomputed analyzer equality modulo pinned provenance:"
            + seed,
        )
        producer_rows[seed] = recomputed
    verifier_rows = {seed: _validate_verifier(root, seed) for seed in common.SEEDS}
    attacks = _validate_attacks(root)
    body = {
        "schema": "cm2.round306c30a.supplemental-full-trace-aggregate.v5",
        "status": (
            "PASS_FOUR_FULL_TRACES_RECOMPUTED__TEN_ATTACKS_REJECTED__"
            "KERNEL_NETWORK_NONE"
        ),
        "run_root": common.workspace_rel(root),
        "comparator_exit_sha256": comparator_stage["receipt_capture"].sha256,
        "comparator_stdout_sha256": comparator_stage["stdout"].sha256,
        "producer_traces": producer_rows,
        "verifier_traces": verifier_rows,
        "attacks": attacks,
        "conclusion": common.fixed_conclusion(),
    }
    return common.close_object(body)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--run-root", required=True)
    return value


def main() -> int:
    try:
        result = build(common.run_root(parser().parse_args().run_root))
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_V5_TRACE_AUDIT_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(common.canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
