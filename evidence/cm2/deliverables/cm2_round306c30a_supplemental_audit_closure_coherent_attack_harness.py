#!/usr/bin/env python3
"""Persistent, per-attack evidence harness for the C30a verifier.

This additive harness leaves the original C30a harness untouched.  It repeats
the original nine attacks, adds a fully reclosed held-to-promoted overclaim,
and retains each forged candidate plus raw verifier stdout, stderr, and exit
metadata.  It is intentionally expensive and is not run by the lightweight
supplemental preflight.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent
PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
CELL = PREFIX + "_cell_ledger.jsonl.gz"
ORIGIN = PREFIX + "_whole_origin_ledger.jsonl.gz"
HELD = PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
FILES = (CELL, ORIGIN, HELD, RESULT)
VERIFIER = DELIVERABLES / (PREFIX + "_independent_verifier.py")
VERIFIER_SHA256 = (
    "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c"
)
BASE_MANIFEST = DELIVERABLES / (PREFIX + "_manifest.sha256")
BASE_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
BASE_RESULT_FILE_SHA256 = (
    "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48"
)
BASE_RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)


class Reject(RuntimeError):
    """The harness or attacked verifier failed closed."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha256(wire(value))


def read_regular(path: Path, maximum: int = 512 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        "regular singleton:" + os.fspath(path),
    )
    raw = absolute.read_bytes()
    require(len(raw) == status.st_size, "stable read:" + os.fspath(path))
    return raw


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    complete = False
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            require(written > 0, "short output write:" + path.name)
            offset += written
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
        if not complete:
            try:
                path.unlink()
            except OSError:
                pass


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("result_sha256", None)
    return {**body, "result_sha256": digest(body)}


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("row_sha256", None)
    return {**body, "row_sha256": digest(body)}


def read_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        return [json.loads(line) for line in handle]


def write_rows(path: Path, rows: list[dict[str, Any]]) -> tuple[str, str, int]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for row in rows:
                encoded = wire(row)
                out.write(encoded + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return sha256(path.read_bytes()), sequence.hexdigest(), path.stat().st_size


def rebind_ledger(
    result: dict[str, Any],
    target: Path,
    filename: str,
    ledger_key: str,
    rows: list[dict[str, Any]],
) -> None:
    file_sha, sequence, size = write_rows(target / filename, rows)
    descriptor = result["ledgers"][ledger_key]
    descriptor["sha256"] = file_sha
    descriptor["row_sequence_sha256"] = sequence
    descriptor["size"] = size
    descriptor["row_count"] = len(rows)


def attack_cell_reclosure(result: dict[str, Any], target: Path) -> None:
    rows = read_rows(target / CELL)
    row = copy.deepcopy(rows[0])
    old_disposition = row["disposition"]
    row["whole_closed_cell_excluded"] = False
    row["disposition"] = "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED"
    row["formal_credit"]["whole_closed_cell_exclusion"] = 0
    row["partition"][
        "closed_box_and_all_owned_faces_edges_vertices_excluded"
    ] = False
    row["partition"][
        "all_graph_face_edge_corner_strata_inherit_the_graph_disposition"
    ] = False
    row["partition_sha256"] = digest(row["partition"])
    rows[0] = close_row(row)
    result["cell_census"]["excluded"] -= 1
    result["cell_census"]["residual"] += 1
    result["cell_census"]["by_disposition"][old_disposition] -= 1
    result["cell_census"]["by_disposition"][
        "RESIDUAL_NEGATIVE_OPEN_SIDE_NOT_EXCLUDED"
    ] += 1
    result["formal_credit"]["reduced_clipped_whole_cell_exclusions"] -= 1
    rebind_ledger(result, target, CELL, "reduced_clipped_cell", rows)


def attack_origin_reclosure(result: dict[str, Any], target: Path) -> None:
    rows = read_rows(target / ORIGIN)
    row = copy.deepcopy(rows[0])
    row["whole_origin_integer_credit"] = 0
    row["whole_original_physical_origin_excluded"] = False
    row["formal_credit"]["whole_source_W_origin_exclusion"] = 0
    rows[0] = close_row(row)
    result["formal_credit"]["whole_source_W_origin_exclusions"] -= 1
    result["source_W_ledger_transition"]["new_whole_origin_exclusion_credit"] -= 1
    result["source_W_ledger_transition"]["after"]["excluded"] -= 1
    result["source_W_ledger_transition"]["after"]["conservative_live"] += 1
    result["source_W_ledger_transition"]["after"]["remaining"] += 1
    result["source_W_ledger_transition"]["after"]["remaining_partition"][
        "mixed_active_nonseam"
    ] += 1
    result["source_W_ledger_transition"]["after"]["remaining_partition"][
        "total"
    ] += 1
    result["strict_nonpromotion"]["D02"] = (
        "BLOCKED_BY_93_REMAINING_SOURCE_W_ORIGINS"
    )
    rebind_ledger(result, target, ORIGIN, "whole_origin_promotion", rows)


def attack_origin_order(result: dict[str, Any], target: Path) -> None:
    rows = read_rows(target / ORIGIN)
    rows[0], rows[1] = rows[1], rows[0]
    rebind_ledger(result, target, ORIGIN, "whole_origin_promotion", rows)


def attack_held_to_promoted_full_reclosure(
    result: dict[str, Any], target: Path
) -> None:
    """Move both held keys into a fully rehashed 162/0, 252-to-90 forgery."""

    origins = read_rows(target / ORIGIN)
    held = read_rows(target / HELD)
    require(len(origins) == 160 and len(held) == 2,
            "held-to-promoted base cardinality")
    for held_row in held:
        held_key = held_row["origin_key"]
        chart = held_key.split(":", 2)[:2]
        source_chart = ":".join(chart)
        template = next(
            (row for row in origins if row["source_chart_id"] == source_chart),
            origins[0],
        )
        forged = copy.deepcopy(template)
        forged["origin_key"] = held_key
        forged["source_chart_id"] = source_chart
        forged["priority_ordinal"] = held_row["candidate_ordinal"]
        forged["whole_origin_integer_credit"] = 1
        forged["whole_original_physical_origin_excluded"] = True
        forged["formal_credit"]["whole_source_W_origin_exclusion"] = 1
        forged["whole_origin_theorem"]["whole_original_origin_excluded"] = True
        forged["whole_origin_theorem_sha256"] = digest(
            forged["whole_origin_theorem"]
        )
        origins.append(forged)
    origins.sort(key=lambda row: row["origin_key"])
    origins = [
        close_row({**row, "promotion_ordinal": ordinal})
        for ordinal, row in enumerate(origins)
    ]
    held = []
    rebind_ledger(result, target, ORIGIN, "whole_origin_promotion", origins)
    rebind_ledger(result, target, HELD, "inherited_H_obstruction_hold", held)

    promoted_keys = [row["origin_key"] for row in origins]
    held_keys: list[str] = []
    census = result["whole_origin_census"]
    census["Round306C30A_new_promoted"] = 162
    census["Round306C30A_inherited_H_held"] = 0
    census["Round306C30A_promoted_origin_keys_sha256"] = digest(promoted_keys)
    census["Round306C30A_inherited_H_held_origin_keys_sha256"] = digest(held_keys)
    census["still_open_active_strict_interior_origins"] = 34
    theorem = result["whole_origin_promotion_theorem"]
    theorem["whole_origins_with_complete_3D_2D_1D_0D_exclusion"] = 162
    theorem["whole_origins_held_by_inherited_positive_measure_H_side"] = 0
    theorem["kind"] = (
        "FORGED_SOURCE_W_162_CANDIDATE_REDUCED_CLIPPED_DELTA_"
        "162_WHOLE_ORIGIN_PROMOTION_AND_0_INHERITED_H_HOLD_THEOREM"
    )
    result["whole_origin_promotion_theorem_sha256"] = digest(theorem)
    result["formal_credit"]["whole_source_W_origin_exclusions"] = 162
    transition = result["source_W_ledger_transition"]
    transition["new_whole_origin_exclusion_credit"] = 162
    after = transition["after"]
    after["excluded"] = 74746
    after["conservative_live"] = 2086
    after["remaining"] = 90
    after["remaining_partition"]["mixed_active_nonseam"] = 34
    after["remaining_partition"]["total"] = 90
    transition["conservation_identity"] = "74746+2086=76832"
    result["strict_nonpromotion"]["D02"] = (
        "BLOCKED_BY_90_REMAINING_SOURCE_W_ORIGINS"
    )
    result["status"] = (
        "FORGED_162_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
        "0_INHERITED_H_OBSTRUCTIONS_HELD__SOURCE_W_252_TO_90"
    )
    result["required_next"] = (
        "CLOSE_12_OUTGOING_H_ORIGINS_THEN_2_FULL_DELTA_ORIGINS_"
        "THEN_20_MULTI_DELTA_ORIGINS_THEN_2_RETAINED_SEAMS_"
        "AND_54_COMPACT_Q_ORIGINS"
    )


def file_table(path: Path) -> list[dict[str, Any]]:
    return [
        {
            "filename": name,
            "sha256": sha256(read_regular(path / name)),
            "size": (path / name).stat().st_size,
        }
        for name in sorted(FILES)
    ]


def copy_candidate(source: Path, target: Path) -> None:
    target.mkdir()
    require(sorted(entry.name for entry in source.iterdir()) == sorted(FILES),
            "base candidate exact file set")
    for name in FILES:
        shutil.copyfile(source / name, target / name)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--evidence-dir", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        require(
            sys.flags.isolated == 1
            and sys.flags.dont_write_bytecode == 1
            and sys.dont_write_bytecode is True,
            "isolated harness runtime",
        )
        # Manifest-first: no candidate or verifier evidence is read above.
        require(sha256(read_regular(BASE_MANIFEST)) == BASE_MANIFEST_SHA256,
                "base manifest trust-root pin")
        require(sha256(read_regular(VERIFIER)) == VERIFIER_SHA256,
                "independent verifier pin")
        source = Path(arguments.candidate_dir).resolve(strict=True)
        require(source.is_dir() and source != DELIVERABLES,
                "candidate directory boundary")
        base_result_raw = read_regular(source / RESULT)
        base_result = json.loads(base_result_raw)
        require(
            sha256(base_result_raw) == BASE_RESULT_FILE_SHA256
            and base_result["result_sha256"] == BASE_RESULT_OBJECT_SHA256
            and base_result["source_W_ledger_transition"]["after"]["remaining"]
            == 92,
            "base result fixed 252-to-92",
        )
        evidence = Path(arguments.evidence_dir)
        evidence_absolute = Path(os.path.abspath(os.fspath(evidence)))
        require(
            not evidence_absolute.exists()
            and evidence_absolute.is_relative_to(WORKSPACE / ".cm2-runtime")
            and evidence_absolute != WORKSPACE / ".cm2-runtime",
            "fresh evidence directory inside .cm2-runtime",
        )
        evidence_absolute.mkdir(parents=True)

        attacks: list[
            tuple[str, Callable[[dict[str, Any], Path], None]]
        ] = [
            (
                "promoted_origin_count",
                lambda value, _target: value["whole_origin_census"].__setitem__(
                    "Round306C30A_new_promoted", 161
                ),
            ),
            (
                "remaining_origin_count",
                lambda value, _target: value["source_W_ledger_transition"][
                    "after"
                ].__setitem__("remaining", 90),
            ),
            (
                "D02_illegal_clear",
                lambda value, _target: value["strict_nonpromotion"].__setitem__(
                    "D02", "CLEARED"
                ),
            ),
            (
                "CM2_illegal_go",
                lambda value, _target: value["strict_nonpromotion"].__setitem__(
                    "CM2", "GO"
                ),
            ),
            (
                "child_volume_credit",
                lambda value, _target: value["whole_origin_promotion_theorem"].
                __setitem__("child_cell_or_volume_credit_used", True),
            ),
            (
                "input_pin_retarget",
                lambda value, _target: value["input_pins"][0].__setitem__(
                    "sha256", "0" * 64
                ),
            ),
            ("cell_ledger_full_reclosure", attack_cell_reclosure),
            ("origin_ledger_full_reclosure", attack_origin_reclosure),
            ("origin_order_full_reclosure", attack_origin_order),
            (
                "held_to_promoted_162_overclaim_full_reclosure",
                attack_held_to_promoted_full_reclosure,
            ),
        ]
        summary_rows: list[dict[str, Any]] = []
        for ordinal, (name, mutate) in enumerate(attacks):
            attack_dir = evidence_absolute / f"{ordinal:02d}_{name}"
            attack_dir.mkdir()
            target = attack_dir / "candidate"
            copy_candidate(source, target)
            before = file_table(target)
            forged = copy.deepcopy(base_result)
            mutate(forged, target)
            (target / RESULT).write_bytes(wire(close_result(forged)))
            after = file_table(target)
            descriptor = {
                "schema": "cm2.round306c30a.supplemental-coherent-attack.v1",
                "ordinal": ordinal,
                "name": name,
                "base_result_object_sha256": BASE_RESULT_OBJECT_SHA256,
                "before_file_table": before,
                "after_file_table": after,
            }
            write_exclusive(
                attack_dir / "attack_descriptor.json",
                wire(descriptor) + b"\n",
            )
            start = time.monotonic_ns()
            run = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    os.fspath(VERIFIER),
                    "--candidate-dir",
                    os.fspath(target),
                ],
                cwd=WORKSPACE,
                env={
                    "LANG": "C.UTF-8",
                    "LC_ALL": "C.UTF-8",
                    "PATH": "/usr/bin:/bin",
                    "TZ": "UTC",
                },
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            elapsed = time.monotonic_ns() - start
            write_exclusive(attack_dir / "verifier.stdout.raw", run.stdout)
            write_exclusive(attack_dir / "verifier.stderr.raw", run.stderr)
            exit_object = {
                "exit_code": run.returncode,
                "elapsed_monotonic_ns": elapsed,
                "stdout_sha256": sha256(run.stdout),
                "stdout_size": len(run.stdout),
                "stderr_sha256": sha256(run.stderr),
                "stderr_size": len(run.stderr),
            }
            write_exclusive(
                attack_dir / "verifier.exit.json", wire(exit_object) + b"\n"
            )
            require(run.returncode != 0, "accepted coherent attack:" + name)
            summary_rows.append({
                "ordinal": ordinal,
                "name": name,
                "rejected": True,
                "exit_code": run.returncode,
                "evidence_directory": attack_dir.relative_to(WORKSPACE).as_posix(),
                "after_file_table_sha256": digest(after),
            })
        summary = {
            "schema": "cm2.round306c30a.supplemental-coherent-attacks.v1",
            "status": "PASS_10_OF_10_COHERENT_ATTACKS_REJECTED",
            "base_manifest_sha256": BASE_MANIFEST_SHA256,
            "independent_verifier_sha256": VERIFIER_SHA256,
            "total": 10,
            "rejected": 10,
            "attacks": summary_rows,
        }
        summary["payload_sha256"] = digest(summary)
        write_exclusive(
            evidence_absolute / "attack_summary.json", wire(summary) + b"\n"
        )
        sys.stdout.buffer.write(wire(summary) + b"\n")
        sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_ATTACK_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
