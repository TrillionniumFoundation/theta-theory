#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
CELL = PREFIX + "_cell_ledger.jsonl.gz"
ORIGIN = PREFIX + "_whole_origin_ledger.jsonl.gz"
HELD = PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
VERIFIER = ROOT / (PREFIX + "_independent_verifier.py")

# This harness is an add-on to the sealed C30a package.  Pin both the
# independent verifier and the exact baseline candidate so a later source or
# artifact change cannot silently weaken or redirect the attack.
PINNED_VERIFIER_SHA256 = (
    "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c"
)
PINNED_BASELINE_SHA256 = {
    CELL: "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    ORIGIN: "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
    HELD: "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    RESULT: "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
}

ATTACK_NAME = "held_origins_to_promoted_full_reclosure_252_to_90"
ATTACK_LAYER = (
    "WHOLE_ORIGIN_3D_2D_1D_0D_OWNERSHIP_AND_SOURCE_W_GLOBAL_LEDGER"
)
ATTACK_REASON = (
    "The two pinned held rows each retain four positive-measure MIXED "
    "outgoing-H terminals. Moving them into the promotion ledger and "
    "re-closing every row, ledger descriptor, theorem digest, census, "
    "conservation identity, and result digest cannot establish exhaustive "
    "half-open whole-origin exclusion."
)
HELD_CHARTS = {
    "W:N:04.00.10101011": "W:N",
    "W:S:H.04.00.10101011": "W:S:H",
}


def wire(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("row_sha256", None)
    return {**body, "row_sha256": digest(body)}


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("result_sha256", None)
    return {**body, "result_sha256": digest(body)}


def read_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        return [json.loads(line) for line in handle]


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for row in rows:
                out.write(wire(row) + b"\n")


def ledger_descriptor(
    path: Path,
    rows: list[dict[str, Any]],
    order: str,
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def promoted_forgery(
    template: dict[str, Any],
    held: dict[str, Any],
) -> dict[str, Any]:
    """Launder a held key through a cloned, internally closed proof row."""
    forged = copy.deepcopy(template)
    forged["origin_key"] = held["origin_key"]
    forged["source_chart_id"] = HELD_CHARTS[held["origin_key"]]
    forged["priority_ordinal"] = held["candidate_ordinal"]
    forged["Round176_preclosed_frontier_count"] = sum(
        held["Round176_preclosed_kind_census"].values()
    )
    forged["Round176_residual_root_count"] = held[
        "Round176_residual_root_count"
    ]
    forged["Round180_inherited_terminal_count"] = sum(
        held["Round180_terminal_disposition_census"].values()
    )
    forged["Round180_final_cell_count"] = held[
        "Round180_final_residual_count"
    ]
    forged["whole_original_physical_origin_excluded"] = True
    forged["whole_origin_integer_credit"] = 1
    forged["formal_credit"]["whole_source_W_origin_exclusion"] = 1
    forged["whole_origin_theorem"]["whole_original_origin_excluded"] = True
    forged["whole_origin_theorem_sha256"] = digest(
        forged["whole_origin_theorem"]
    )
    return close_row(forged)


def build_attack(candidate: Path, target: Path) -> dict[str, Any]:
    for filename in (CELL, ORIGIN, HELD, RESULT):
        shutil.copyfile(candidate / filename, target / filename)

    result = json.loads((target / RESULT).read_bytes())
    origin_rows = read_rows(target / ORIGIN)
    held_rows = read_rows(target / HELD)
    require(len(origin_rows) == 160, "baseline promoted row count")
    require(len(held_rows) == 2, "baseline held row count")
    require(
        {row["origin_key"] for row in held_rows} == set(HELD_CHARTS),
        "baseline held origin identities",
    )
    require(
        all(
            row["Round180_nonexcluded_terminal_count"] == 4
            and row["Round180_terminal_disposition_census"].get("MIXED") == 4
            and not row["whole_original_physical_origin_excluded"]
            and row["whole_origin_integer_credit"] == 0
            for row in held_rows
        ),
        "baseline positive-measure held evidence",
    )

    template = origin_rows[0]
    origin_rows.extend(
        promoted_forgery(template, held) for held in held_rows
    )
    origin_rows.sort(key=lambda row: row["origin_key"])
    for ordinal, row in enumerate(origin_rows):
        row["promotion_ordinal"] = ordinal
        origin_rows[ordinal] = close_row(row)
    held_rows = []

    write_rows(target / ORIGIN, origin_rows)
    write_rows(target / HELD, held_rows)
    result["ledgers"]["whole_origin_promotion"] = ledger_descriptor(
        target / ORIGIN,
        origin_rows,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    result["ledgers"]["inherited_H_obstruction_hold"] = ledger_descriptor(
        target / HELD,
        held_rows,
        "LEXICOGRAPHIC_HELD_SOURCE_W_ORIGIN_KEY",
    )

    promoted_keys = [row["origin_key"] for row in origin_rows]
    census = result["whole_origin_census"]
    census["Round306C30A_new_promoted"] = 162
    census["Round306C30A_inherited_H_held"] = 0
    census["Round306C30A_promoted_origin_keys_sha256"] = digest(promoted_keys)
    census["Round306C30A_inherited_H_held_origin_keys_sha256"] = digest([])
    census["still_open_active_strict_interior_origins"] = 34

    transition = result["source_W_ledger_transition"]
    transition["new_whole_origin_exclusion_credit"] = 162
    transition["after"]["excluded"] = 74_746
    transition["after"]["conservative_live"] = 2_086
    transition["after"]["remaining"] = 90
    transition["after"]["remaining_partition"]["mixed_active_nonseam"] = 34
    transition["after"]["remaining_partition"]["total"] = 90
    transition["conservation_identity"] = "74746+2086=76832"

    result["formal_credit"]["whole_source_W_origin_exclusions"] = 162
    theorem = result["whole_origin_promotion_theorem"]
    theorem["kind"] = (
        "SOURCE_W_162_CANDIDATE_REDUCED_CLIPPED_DELTA_162_WHOLE_"
        "ORIGIN_PROMOTION_AND_0_INHERITED_H_HOLD_THEOREM"
    )
    theorem["whole_origins_with_complete_3D_2D_1D_0D_exclusion"] = 162
    theorem["whole_origins_held_by_inherited_positive_measure_H_side"] = 0
    result["whole_origin_promotion_theorem_sha256"] = digest(theorem)
    result["status"] = (
        "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
        "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
        "162_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
        "0_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
    )
    result["strict_nonpromotion"]["D02"] = (
        "BLOCKED_BY_90_REMAINING_SOURCE_W_ORIGINS"
    )
    result["required_next"] = (
        "CLOSE_10_OUTGOING_H_ORIGINS_THEN_2_FULL_DELTA_ORIGINS_THEN_"
        "20_MULTI_DELTA_ORIGINS_THEN_2_REDUCED_LIVE_ORIGINS_THEN_2_"
        "RETAINED_SEAMS_AND_54_COMPACT_Q_ORIGINS"
    )
    result = close_result(result)
    (target / RESULT).write_bytes(wire(result))
    assert_full_reclosure(target, result, origin_rows, held_rows)
    return result


def assert_full_reclosure(
    target: Path,
    result: dict[str, Any],
    origin_rows: list[dict[str, Any]],
    held_rows: list[dict[str, Any]],
) -> None:
    require(len(origin_rows) == 162 and not held_rows, "attack 162/0 split")
    require(
        [row["origin_key"] for row in origin_rows]
        == sorted(row["origin_key"] for row in origin_rows),
        "attack origin order",
    )
    require(
        [row["promotion_ordinal"] for row in origin_rows] == list(range(162)),
        "attack promotion ordinals",
    )
    for row in origin_rows:
        body = dict(row)
        claimed = body.pop("row_sha256")
        require(claimed == digest(body), "attack origin row closure")
    for key, path, rows, order in (
        (
            "whole_origin_promotion",
            target / ORIGIN,
            origin_rows,
            "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        ),
        (
            "inherited_H_obstruction_hold",
            target / HELD,
            held_rows,
            "LEXICOGRAPHIC_HELD_SOURCE_W_ORIGIN_KEY",
        ),
    ):
        require(
            result["ledgers"][key] == ledger_descriptor(path, rows, order),
            "attack ledger descriptor closure:" + key,
        )
    body = dict(result)
    claimed = body.pop("result_sha256")
    require(claimed == digest(body), "attack result closure")
    transition = result["source_W_ledger_transition"]
    require(
        transition["before"]["remaining"] == 252
        and transition["after"]["remaining"] == 90
        and transition["new_whole_origin_exclusion_credit"] == 162
        and transition["after"]["excluded"]
        + transition["after"]["conservative_live"]
        == transition["after"]["total"]
        == 76_832
        and transition["after"]["remaining_partition"]["total"] == 90,
        "attack global 252-to-90 reclosure",
    )
    require(
        result["whole_origin_promotion_theorem_sha256"]
        == digest(result["whole_origin_promotion_theorem"]),
        "attack theorem closure",
    )
    require(
        result["whole_origin_census"][
            "Round306C30A_promoted_origin_keys_sha256"
        ] == digest([row["origin_key"] for row in origin_rows])
        and result["whole_origin_census"][
            "Round306C30A_inherited_H_held_origin_keys_sha256"
        ] == digest([]),
        "attack origin-key set closure",
    )


def validate_pins(candidate: Path) -> None:
    require(
        VERIFIER.is_file()
        and file_hash(VERIFIER) == PINNED_VERIFIER_SHA256,
        "independent verifier source pin mismatch",
    )
    require(candidate.is_dir(), "candidate directory missing")
    for filename, expected in PINNED_BASELINE_SHA256.items():
        path = candidate / filename
        require(
            path.is_file() and file_hash(path) == expected,
            "baseline artifact pin mismatch:" + filename,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    arguments = parser.parse_args()
    candidate = arguments.candidate_dir.resolve()
    validate_pins(candidate)

    with tempfile.TemporaryDirectory(prefix="c30a-supplemental-attack-") as raw:
        target = Path(raw)
        forged = build_attack(candidate, target)
        run = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                str(VERIFIER),
                "--candidate-dir",
                str(target),
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(
            run.returncode != 0,
            "independent verifier accepted coherent held-to-promoted attack",
        )
        stderr_text = run.stderr.decode("utf-8", errors="replace")
        stderr_lines = [line for line in stderr_text.splitlines() if line]
        require(bool(stderr_lines), "independent verifier rejection reason missing")
        rejection_last_line = stderr_lines[-1]
        require(
            rejection_last_line == "Reject: static theorem/result boundary"
            or rejection_last_line.startswith("RuntimeError:")
            or rejection_last_line.startswith("ValueError:")
            or rejection_last_line.startswith("AssertionError:"),
            "unexpected independent verifier rejection type:"
            + rejection_last_line,
        )
        attack = {
            "name": ATTACK_NAME,
            "layer": ATTACK_LAYER,
            "reason": ATTACK_REASON,
            "status": "REJECTED",
            "verifier_returncode": run.returncode,
            "verifier_stdout_sha256": hashlib.sha256(run.stdout).hexdigest(),
            "verifier_stderr_sha256": hashlib.sha256(run.stderr).hexdigest(),
            "verifier_rejection_last_line": rejection_last_line,
            "forged_result_sha256": forged["result_sha256"],
            "forged_transition": "252_TO_90",
            "forged_promoted_held_split": "162_TO_0",
            "cryptographic_reclosure_checked_before_verification": True,
        }

    print(wire({
        "status": "PASS_1_OF_1_SUPPLEMENTAL_COHERENT_ATTACK_REJECTED",
        "pinned_independent_verifier_sha256": PINNED_VERIFIER_SHA256,
        "attacks": [attack],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
