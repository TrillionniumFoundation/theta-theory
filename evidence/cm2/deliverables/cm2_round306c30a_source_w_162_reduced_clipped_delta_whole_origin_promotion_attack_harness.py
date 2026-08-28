#!/usr/bin/env python3
from __future__ import annotations

import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


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
                out.write(wire(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return (
        hashlib.sha256(path.read_bytes()).hexdigest(),
        sequence.hexdigest(),
        path.stat().st_size,
    )


def rebind_ledger(
    result: dict[str, Any],
    target: Path,
    filename: str,
    ledger_key: str,
    rows: list[dict[str, Any]],
) -> None:
    sha, sequence, size = write_rows(target / filename, rows)
    descriptor = result["ledgers"][ledger_key]
    descriptor["sha256"] = sha
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


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    base = json.loads((candidate / RESULT).read_bytes())
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
            ].__setitem__("remaining", 89),
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
    ]
    rejected: list[str] = []
    for name, mutate in attacks:
        with tempfile.TemporaryDirectory(prefix="c30a-attack-") as raw:
            target = Path(raw)
            for filename in (CELL, ORIGIN, HELD, RESULT):
                shutil.copyfile(candidate / filename, target / filename)
            forged = copy.deepcopy(base)
            mutate(forged, target)
            (target / RESULT).write_bytes(wire(close_result(forged)))
            run = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-B",
                    str(VERIFIER),
                    "--candidate-dir",
                    str(target),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if run.returncode == 0:
                raise RuntimeError("accepted coherent attack:" + name)
            rejected.append(name)
    print(wire({
        "status": "PASS_9_OF_9_COHERENT_ATTACKS_REJECTED",
        "rejected": rejected,
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
