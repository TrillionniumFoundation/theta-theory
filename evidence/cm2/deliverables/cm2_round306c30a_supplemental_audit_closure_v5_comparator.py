#!/usr/bin/env python3
"""Real-invocation dual-seed comparator for C30a supplemental P0-B v5."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

_DELIVERABLES_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _DELIVERABLES_BOOTSTRAP not in sys.path:
    sys.path.insert(0, _DELIVERABLES_BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common
import cm2_round306c30a_supplemental_audit_closure_v5_trace_lib as traces


sys.dont_write_bytecode = True

HASH_PROBES = {
    "30630071": 8841297538927089933,
    "30630929": 889641737497572634,
}


def build(root: Path) -> dict[str, Any]:
    common.validate_base_manifest()
    legacy = common.load_legacy_checker()
    stdout_bytes: list[bytes] = []
    stderr_bytes: list[bytes] = []
    candidate_tables: list[dict[str, str]] = []
    seed_rows: dict[str, Any] = {}
    for seed in common.SEEDS:
        stage_name = traces.PRODUCER_STAGES[seed]
        stage = common.validate_stage(root, stage_name)
        common.require(stage["stdout"].raw is not None, "producer stdout retained")
        common.require(stage["stderr"].raw is not None, "producer stderr retained")
        stdout_object = common.strict_json(
            stage["stdout"].raw, stage_name + " stdout"
        )
        common.require(
            stdout_object == {
                "result_sha256": legacy.RESULT_OBJECT_SHA256,
                "status": (
                    "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
                    "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
                    "160_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
                    "2_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
                ),
            }
            and stage["stderr"].raw.count(b"\n") == 50,
            "producer fixed conclusion and diagnostics:" + seed,
        )
        provenance_cap = common.capture(traces.provenance_path(root, seed))
        common.require(provenance_cap.raw is not None, "provenance retained")
        provenance = common.strict_json(
            provenance_cap.raw, "producer provenance:" + seed
        )
        common.validate_closed(provenance, "producer provenance:" + seed)
        expected_candidate = common.workspace_rel(traces.candidate_dir(root, seed))
        expected_pycache = common.workspace_rel(root / "pycache" / ("seed" + seed))
        common.require(
            provenance.get("schema")
            == "cm2.round306c30a.controlled-hash-seed-replay.v1"
            and provenance.get("seed") == seed
            and provenance.get("candidate_relpath") == expected_candidate
            and provenance.get("pycache_prefix_relpath") == expected_pycache
            and provenance.get("environment") == {
                "HOME": "/nonexistent",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "PATH": "/usr/bin:/bin",
                "PYTHONHASHSEED": seed,
                "PYTHONPYCACHEPREFIX": os.fspath(
                    common.WORKSPACE / expected_pycache
                ),
                "TZ": "UTC",
            }
            and provenance.get("expected_output_names")
            == list(common.OUTPUT_NAMES)
            and provenance.get("hash_probe_text")
            == "CM2-C30a-controlled-hash-seed-v1"
            and provenance.get("hash_probe_value") == HASH_PROBES[seed]
            and provenance.get("producer") == {
                "changed_byte_offset": 36078,
                "compiled_filename": (
                    "deliverables/" + common.BASE_PREFIX + "_producer.py"
                ),
                "path": "deliverables/" + common.BASE_PREFIX + "_producer.py",
                "sha256": (
                    "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee"
                    "15a6846dc91714"
                ),
                "transform": "ONE_BYTE_ISOLATED_GUARD_1_TO_0",
                "transformed_sha256": (
                    "6105ad2e3aeffbd2a27063a7e9b56cdadaeb22e8e96f8daf987"
                    "f0a5763ac923e"
                ),
            }
            and provenance.get("python") == {
                "cache_tag": "cpython-312",
                "dont_write_bytecode": 1,
                "hash_algorithm": "siphash13",
                "hash_randomization": 1,
                "hash_width": 64,
                "ignore_environment": 0,
                "isolated": 0,
                "no_user_site": 1,
                "safe_path": True,
                "version": "3.12.3",
            }
            and provenance.get("status")
            == "PREFLIGHT_PASS_REPLAY_NOT_YET_COMPLETE",
            "true seed provenance:" + seed,
        )
        candidates = traces.exact_candidate(root, seed)
        table = {name: candidates[name].sha256 for name in common.OUTPUT_NAMES}
        candidate_tables.append(table)
        stdout_bytes.append(stage["stdout"].raw)
        stderr_bytes.append(stage["stderr"].raw)
        analysis = traces.analyze_role(
            root,
            kind="producer",
            seed=seed,
            source="v5-comparator:producer:seed" + seed,
        )
        seed_rows[seed] = {
            "stage_exit_sha256": stage["receipt_capture"].sha256,
            "provenance_sha256": provenance_cap.sha256,
            "candidate_members": table,
            "trace_analysis": analysis,
            "trace_analysis_sha256": common.sha256(common.canonical(analysis)),
        }
    common.require(
        stdout_bytes[0] == stdout_bytes[1]
        and stderr_bytes[0] == stderr_bytes[1]
        and candidate_tables[0] == candidate_tables[1] == common.OUTPUT_HASHES,
        "two-seed byte identity against formal seal",
    )
    body = {
        "schema": "cm2.round306c30a.supplemental-dual-seed-comparator.v5",
        "status": (
            "PASS_REAL_DUAL_SEED_SAME_INVOCATION_EVIDENCE__"
            "KERNEL_NETWORK_NONE__ZERO_ADDITIONAL_CREDIT"
        ),
        "run_root": common.workspace_rel(root),
        "base_manifest_sha256": common.BASE_MANIFEST_SHA256,
        "seeds": seed_rows,
        "comparisons": {
            "producer_stdout_bytes_identical": True,
            "producer_stderr_bytes_identical": True,
            "candidate_files_seed1_equal_seed2": True,
            "candidate_files_both_equal_formal_seal": True,
            "candidate_member_count_each": len(common.OUTPUT_NAMES),
        },
        "conclusion": common.fixed_conclusion(),
    }
    return common.close_object(body)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--run-root", required=True)
    return value


def main() -> int:
    try:
        root = common.run_root(parser().parse_args().run_root)
        result = build(root)
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_V5_COMPARATOR_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(common.canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
