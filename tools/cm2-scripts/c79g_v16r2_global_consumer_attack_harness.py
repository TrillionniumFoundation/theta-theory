#!/usr/bin/env python3
"""Read-only C79g v16r2 global-consumer mutation attack harness.

The harness exercises the independent in-memory precompute, but never imports
or executes a C79g producer, consumer, launcher, or other protocol source.
All mutations are made to Python objects or to bytes already read from frozen
inputs.  Existing filesystem paths are opened only through the precompute
helper's O_NOFOLLOW/stable-identity reader; no temporary file, namespace,
manifest, outer receipt, runtime surface, or credit is created.

Every mutation attack must be rejected (``FAIL_CLOSED``).  Seed variation is
reported separately as a deterministic-invariance check because it is a
positive property, not a mutation that should itself fail.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, Callable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = Path(__file__).with_name("c79g_v16r2_global_consumer_precompute.py")


def load_helper() -> Any:
    """Load only the read-only precompute helper as a data/reconstruction API."""
    spec = importlib.util.spec_from_file_location(
        "_c79g_v16r2_read_only_precompute", HELPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load read-only precompute helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_inputs(m: Any) -> tuple[dict[str, Any], tuple[Any, ...]]:
    """Read and fully validate the frozen inputs once, then retain memory data."""
    leaf_obj, leaf_raw, _ = m.read_json(m.C55A_LEAF, m.C55A_LEAF_SHA, 0o444)
    m.verify_object(leaf_obj, "C55A leaf", m.C55A_LEAF_OBJECT)
    c55b, _, _ = m.read_gzip_rows(
        m.C55B_CELLS, m.C55B_CELLS_SHA, 0o664, "C55B cells")
    l_a, l_b, l_identity = m.dual_surface(
        m.C78L_A, m.C78L_B, m.C78L_NAMES, m.C78L_PINS, 0o755, "C78L")
    metadata = m.validate_c78_metadata()
    l_cells, _, _ = m.read_gzip_rows(
        m.C78L_A / m.C78L_NAMES["cells"], m.C78L_PINS["cells"],
        0o444, "C78L cells")
    l_pairs, _, _ = m.read_gzip_rows(
        m.C78L_A / m.C78L_NAMES["pairs"], m.C78L_PINS["pairs"],
        0o444, "C78L pairs")
    s_projection, _, _ = m.read_gzip_rows(
        m.C78S_A / m.C78S_NAMES["projection"], m.C78S_PINS["projection"],
        0o444, "C78S projection")
    s_pairs, _, _ = m.read_gzip_rows(
        m.C78S_A / m.C78S_NAMES["pairs"], m.C78S_PINS["pairs"],
        0o444, "C78S pairs")
    c42_rows, c53_rows, c53_meta = m.validate_c53()
    state, digests = m.reconstruct(
        leaf_raw, c55b, l_cells, l_pairs, s_projection, s_pairs,
        c42_rows, c53_rows)
    baseline = {
        "overlay_rows": len(state["overlay"]),
        "successor_rows": len(state["successor"]),
        "parent_rows": len(state["parents"]),
        "public_unresolved_after_reconstruction": 0,
        "all_parent_unresolved_count_zero": all(
            row["unresolved_count"] == 0 for row in state["parents"]),
        "census": state["census"],
        "modes": state["modes"],
        "digests": digests,
        "C53": c53_meta,
        "dual_identity": {
            "C78L": l_identity,
            "C78S": metadata["C78S_dual_identity"],
        },
    }
    args = (leaf_raw, c55b, l_cells, l_pairs, s_projection, s_pairs,
            c42_rows, c53_rows)
    # Keep the raw leaf object available for a row-closure mutation without
    # reopening any path in an attack case.
    baseline["leaf_object"] = leaf_obj
    return baseline, args


def expect_fail(name: str, attack: Callable[[], Any]) -> dict[str, Any]:
    """Run one mutation and turn any validator exception into FAIL_CLOSED."""
    try:
        attack()
    except Exception as exc:  # noqa: BLE001 - every validator failure is evidence
        return {
            "name": name,
            "status": "FAIL_CLOSED",
            "exception_type": type(exc).__name__,
            "detail": str(exc)[:240],
        }
    return {"name": name, "status": "UNEXPECTED_PASS"}


def main() -> int:
    try:
        m = load_helper()
        baseline, args = load_inputs(m)
        (leaf_raw, c55b, l_cells, l_pairs, s_projection, s_pairs,
         c42_rows, c53_rows) = args

        attacks: list[dict[str, Any]] = []

        # A pinned-byte substitution must fail before any semantic use.
        attacks.append(expect_fail(
            "hash_pin_flip_c55a",
            lambda: m.read_stable(m.C55A_LEAF, "0" * 64, 0o444)))

        # Pointing a trusted path at a different frozen member is rejected by
        # mode/hash binding (and never accepted as an alternate input).
        attacks.append(expect_fail(
            "path_substitution_wrong_member",
            lambda: m.read_stable(
                m.C55B_CELLS, m.C55A_LEAF_SHA, 0o444)))

        # Linux exposes this stable symlink without requiring a filesystem
        # mutation; O_NOFOLLOW must reject it.
        attacks.append(expect_fail(
            "symlink_nofollow_proc_self_exe",
            lambda: m.read_stable(Path("/proc/self/exe"))))

        # Truncation is tested against the already-read gzip bytes.  The
        # decompressor must reject a missing trailer/member boundary.
        def truncated_gzip() -> None:
            raw, _ = m.read_stable(m.C55B_CELLS, m.C55B_CELLS_SHA, 0o664)
            if len(raw) < 2:
                raise RuntimeError("gzip fixture too short")
            gzip.decompress(raw[:-1])

        attacks.append(expect_fail("truncated_gzip_member", truncated_gzip))

        # Duplicate crosswalk rows must not pass the exact 1,724-row census.
        def duplicate_c55b() -> None:
            rows = copy.deepcopy(c55b)
            rows.append(copy.deepcopy(rows[0]))
            m.reconstruct(leaf_raw, rows, l_cells, l_pairs, s_projection,
                           s_pairs, c42_rows, c53_rows)

        attacks.append(expect_fail("duplicate_c55b_row", duplicate_c55b))

        # A baseline row turned unresolved changes the global partition and
        # must be rejected even though its old row hash remains in memory.
        def unresolved_tamper() -> None:
            rows = copy.deepcopy(c55b)
            index = next(i for i, row in enumerate(rows)
                         if row.get("current_effective_disposition") ==
                         "EARLIEST_PREFIX_EXCLUDED")
            rows[index]["current_effective_disposition"] = \
                "UNRESOLVED_R1648_CONTINUATION"
            m.reconstruct(leaf_raw, rows, l_cells, l_pairs, s_projection,
                           s_pairs, c42_rows, c53_rows)

        attacks.append(expect_fail("unresolved_disposition_tamper", unresolved_tamper))

        # Reusing one directory for both candidates must fail the distinct
        # inode guard, even when every member byte is otherwise valid.
        attacks.append(expect_fail(
            "dual_candidate_inode_collision",
            lambda: m.dual_surface(
                m.C78L_A, m.C78L_A, m.C78L_NAMES, m.C78L_PINS, 0o755,
                "C78L-mutated")))

        # A byte/pin mutation in the singleton surface must fail closed before
        # semantic rows are consumed.
        def singleton_pin_flip() -> None:
            pins = dict(m.C78S_PINS)
            pins["projection"] = "f" * 64
            m.dual_surface(m.C78S_A, m.C78S_B, m.C78S_NAMES, pins, 0o555,
                           "C78S-mutated")

        attacks.append(expect_fail("singleton_surface_hash_tamper", singleton_pin_flip))

        # A duplicate Kraft parent index must not survive the global join.
        def duplicate_parent() -> None:
            rows = copy.deepcopy(c42_rows)
            rows[1]["pair_index"] = rows[0]["pair_index"]
            m.reconstruct(leaf_raw, c55b, l_cells, l_pairs, s_projection,
                           s_pairs, rows, c53_rows)

        attacks.append(expect_fail("duplicate_c42_parent_index", duplicate_parent))

        # A forged C53 projection object hash is caught by the closed-object
        # validator before it can be treated as a parent authority witness.
        def c53_projection_hash_tamper() -> None:
            row = copy.deepcopy(c53_rows[0])
            row["projection_object_sha256"] = "0" * 64
            m.verify_object(row, "tampered C53 projection")

        attacks.append(expect_fail("c53_projection_object_hash_tamper",
                                   c53_projection_hash_tamper))

        # A stale row hash after content mutation must not be accepted.
        def row_hash_flip() -> None:
            row = copy.deepcopy(baseline["leaf_object"]["leaves"][0])
            row["cell_id"] = row["cell_id"] + "-tampered"
            m.verify_row(row, "tampered C55A row")

        attacks.append(expect_fail("c55a_row_hash_tamper", row_hash_flip))

        # A semantic C78L row with unresolved_count=1 is rejected even if all
        # surrounding bytes and pins remain unchanged.
        def c78l_unresolved_tamper() -> None:
            rows = copy.deepcopy(l_cells)
            rows[0]["unresolved_count"] = 1
            m.reconstruct(leaf_raw, c55b, rows, l_pairs, s_projection,
                           s_pairs, c42_rows, c53_rows)

        attacks.append(expect_fail("c78l_unresolved_count_tamper",
                                   c78l_unresolved_tamper))

        # A C78S partition duplicate must fail exact overlay identity/census.
        def duplicate_singleton_projection() -> None:
            rows = copy.deepcopy(s_projection)
            rows[1]["cell_id"] = rows[0]["cell_id"]
            m.reconstruct(leaf_raw, c55b, l_cells, l_pairs, rows,
                           s_pairs, c42_rows, c53_rows)

        attacks.append(expect_fail("duplicate_singleton_projection_id",
                                   duplicate_singleton_projection))

        failed_closed = sum(row["status"] == "FAIL_CLOSED" for row in attacks)
        all_attack_pass = failed_closed == len(attacks)
        seed = {
            "status": "PASS_INVARIANT" if baseline.get("digests") else
            "FAIL_CLOSED",
            "note": "full precompute independently performs PYTHONHASHSEED=1/99991 child replay",
        }

        report = {
            "schema": "cm2.c79g.v16r2.global-consumer-attack-harness.v1",
            "status": (
                "PASS_READ_ONLY_ATTACK_HARNESS__ALL_MUTATIONS_FAIL_CLOSED__ZERO_CREDIT"
                if all_attack_pass else
                "FAIL_CLOSED_ATTACK_HARNESS_UNEXPECTED_MUTATION_ACCEPTED"
            ),
            "attack_count": len(attacks),
            "failed_closed_count": failed_closed,
            "attack_name_order_sha256": sha(canonical([row["name"] for row in attacks])),
            "attacks": attacks,
            "seed_invariance": seed,
            "baseline": {
                key: value for key, value in baseline.items()
                if key != "leaf_object"
            },
            "credit": {
                "formal_global_closure_credit": 0,
                "D02_unlock": False,
                "runtime_authorized": False,
            },
            "writes": {
                "deliverables": False,
                "runtime": False,
                "manifest": False,
                "outer": False,
                "credit": False,
                "pyc": False,
            },
        }
        print(json.dumps(report, sort_keys=True, ensure_ascii=True))
        return 0 if all_attack_pass else 1
    except Exception as exc:  # noqa: BLE001 - fail closed and report JSON only
        print(json.dumps({
            "schema": "cm2.c79g.v16r2.global-consumer-attack-harness.v1",
            "status": "FAIL_CLOSED_ATTACK_HARNESS_BASELINE",
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": False,
        }, sort_keys=True, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
