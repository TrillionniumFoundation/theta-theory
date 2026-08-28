#!/usr/bin/env python3
"""Coherent-corruption rejection harness for candidate-only C30f.

The untouched candidate must first pass the pinned independent verifier.
Every attack then recloses every directly dependent row, ledger descriptor,
origin digest, and result self-hash.  The harness requires the verifier's
typed rejection reason to equal the attack's exact expected reason.

Only temporary copies are mutated.  This harness imports the independent
verifier but never imports or executes the C30f producer, emits zero formal
credit, and creates no durable result, manifest, or sealed artifact.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30f_source_w_retained_physical_seam_"
    "whole_origin_exclusion"
)
CELL_LEDGER = PREFIX + "_target_cell_ledger.jsonl.gz"
SOURCE_STRATA_LEDGER = PREFIX + "_source_half_open_strata_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
EXPECTED_FILES = {CELL_LEDGER, SOURCE_STRATA_LEDGER, ORIGIN_LEDGER, RESULT}
VERIFIER = PREFIX + "_independent_verifier.py"
VERIFIER_SHA256 = (
    "4feacbc45dda6ec68a326e62603f3af41dfc7cc58ed036128d30d5e802bbdae3"
)
PRODUCER_MODULE_NAME = PREFIX + "_producer"


class HarnessFailure(RuntimeError):
    """The harness, rather than an attacked candidate, failed."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise HarnessFailure(label)


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
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = {
        key: item for key, item in value.items() if key != "row_sha256"
    }
    return {**body, "row_sha256": digest(body)}


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = {
        key: item for key, item in value.items() if key != "result_sha256"
    }
    return {**body, "result_sha256": digest(body)}


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes().decode("ascii"))
    require(type(value) is dict, "object JSON:" + path.name)
    return value


def read_rows(path: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="ascii", newline="") as stream:
        for line in stream:
            value = json.loads(line)
            require(type(value) is dict, "row JSON:" + path.name)
            output.append(value)
    require(bool(output), "nonempty ledger:" + path.name)
    return output


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(wire(close_result(result)))


def write_rows(
    path: Path,
    rows: list[dict[str, Any]],
    order: str,
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=9,
            fileobj=raw,
            mtime=0,
        ) as stream:
            for row in rows:
                closed = close_row(row)
                row.clear()
                row.update(closed)
                stream.write(wire(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "row_sequence_sha256": sequence.hexdigest(),
        "sha256": file_hash(path),
        "size": path.stat().st_size,
        "order": order,
    }


def copy_candidate(source: Path, target: Path) -> None:
    require(
        source.is_dir()
        and not source.is_symlink()
        and {path.name for path in source.iterdir()} == EXPECTED_FILES,
        "baseline candidate exact file set",
    )
    target.mkdir()
    for filename in EXPECTED_FILES:
        status = (source / filename).lstat()
        require(
            stat.S_ISREG(status.st_mode)
            and not (source / filename).is_symlink()
            and status.st_nlink == 1,
            "baseline regular singleton:" + filename,
        )
        shutil.copyfile(source / filename, target / filename)


def load_pinned_verifier() -> ModuleType:
    path = ROOT / VERIFIER
    status = path.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and file_hash(path) == VERIFIER_SHA256,
        "pinned C30f independent verifier",
    )
    module_name = VERIFIER[:-3]
    require(
        module_name not in sys.modules
        and PRODUCER_MODULE_NAME not in sys.modules,
        "verifier and producer not preloaded",
    )
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(
        specification is not None and specification.loader is not None,
        "verifier import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    require(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and file_hash(path) == VERIFIER_SHA256
        and PRODUCER_MODULE_NAME not in sys.modules,
        "imported verifier identity and inert producer",
    )
    return module


def baseline_state(candidate: Path) -> dict[str, str]:
    return {
        filename: file_hash(candidate / filename)
        for filename in sorted(EXPECTED_FILES)
    }


def cascade_origins(
    target: Path,
    origins: list[dict[str, Any]],
) -> None:
    result = read_object(target / RESULT)
    descriptor = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    result["ledgers"]["whole_origin_exclusion_candidate"] = descriptor
    write_result(target, result)


def cascade_cells(
    target: Path,
    cells: list[dict[str, Any]],
) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGIN_LEDGER)
    cell_descriptor = write_rows(
        target / CELL_LEDGER,
        cells,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    for origin in origins:
        values = [
            row for row in cells
            if row["origin_key"] == origin["origin_key"]
        ]
        origin["target_cell_rows_sha256"] = digest(values)
        closed = close_row(origin)
        origin.clear()
        origin.update(closed)
    origin_descriptor = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    result["ledgers"]["target_cell_candidate"] = cell_descriptor
    result["ledgers"]["whole_origin_exclusion_candidate"] = origin_descriptor
    write_result(target, result)


def cascade_source_strata(
    target: Path,
    strata: list[dict[str, Any]],
) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGIN_LEDGER)
    source_descriptor = write_rows(
        target / SOURCE_STRATA_LEDGER,
        strata,
        "LEXICOGRAPHIC_ORIGIN_KEY_THEN_SOURCE_STRATUM_ID",
    )
    for origin in origins:
        values = [
            row for row in strata
            if row["origin_key"] == origin["origin_key"]
        ]
        origin["source_half_open_strata_row_count"] = len(values)
        origin["source_half_open_strata_rows_sha256"] = digest(values)
        theorem = origin["source_half_open_atomic_theorem"]
        theorem["source_strata_rows_sha256"] = digest(values)
        origin["source_half_open_atomic_theorem_sha256"] = digest(theorem)
        closed = close_row(origin)
        origin.clear()
        origin.update(closed)
    origin_descriptor = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    result["ledgers"][
        "source_half_open_strata_candidate"
    ] = source_descriptor
    result["ledgers"]["whole_origin_exclusion_candidate"] = origin_descriptor
    write_result(target, result)


def mutate_deep_clipped_partition_reclosure(target: Path) -> None:
    cells = read_rows(target / CELL_LEDGER)
    row = next(
        value for value in cells
        if value["source_kind"]
        == "SEALED_C30A_REDUCED_CLIPPED_KERNEL_REPLAY"
    )
    row["partition"][
        "closed_box_and_all_owned_faces_edges_vertices_excluded"
    ] = False
    row["partition"][
        "all_graph_face_edge_corner_strata_inherit_the_graph_disposition"
    ] = False
    cascade_cells(target, cells)


def mutate_deep_source_owner_reclosure(target: Path) -> None:
    strata = read_rows(target / SOURCE_STRATA_LEDGER)
    row = next(
        value for value in strata
        if value["ambient_dimension"] == 0
    )
    row["dyadic_owner_proof_source"] = (
        "COHERENT_ATTACK_REBINDS_THE_CLOSED_OWNER"
    )
    cascade_source_strata(target, strata)


def mutate_child_stratum_credit(target: Path) -> None:
    result = read_object(target / RESULT)
    theorem = result["candidate_theorem"]
    theorem["child_stratum_count_or_volume_used_as_integer_credit"] = True
    result["candidate_theorem_sha256"] = digest(theorem)
    result["formal_credit"]["target_cell_dispositions"] = 288
    result["formal_credit"]["source_half_open_stratum_dispositions"] = 994
    write_result(target, result)


def mutate_algebraic_volume_credit(target: Path) -> None:
    origins = read_rows(target / ORIGIN_LEDGER)
    origin = origins[0]
    origin["exact_rational_enclosure_volume_conservation"][
        "algebraic_source_substrata_volume_used_as_credit"
    ] = True
    origin["formal_credit"]["resolved_source_W_origin_disposition"] = 1
    origin["formal_credit"]["whole_source_W_origin_exclusion"] = 1
    closed = close_row(origin)
    origin.clear()
    origin.update(closed)
    cascade_origins(target, origins)


def mutate_d02_promotion(target: Path) -> None:
    result = read_object(target / RESULT)
    result["formal_credit"]["D02"] = 1
    result["strict_nonpromotion"]["D02"] = "CLEARED_BY_C30F_ATTACK"
    write_result(target, result)


def mutate_cm2_promotion(target: Path) -> None:
    result = read_object(target / RESULT)
    result["formal_credit"]["CM2"] = 1
    result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    write_result(target, result)


def mutate_input_pin(target: Path) -> None:
    result = read_object(target / RESULT)
    result["input_pins"][0]["sha256"] = "f" * 64
    write_result(target, result)


def mutate_conditional_order(target: Path) -> None:
    result = read_object(target / RESULT)
    dependencies = result["unsealed_upstream_dependencies"]
    lane = next(
        key for key in sorted(dependencies)
        if key.startswith("C30")
    )
    dependencies[lane]["dependency_kind"] = (
        "COHERENT_ATTACK_CONSUMES_UNSEALED_MATHEMATICAL_INPUT"
    )
    dependencies[lane]["result_or_ledger_consumed"] = True
    write_result(target, result)


@dataclass(frozen=True)
class Attack:
    name: str
    expected_reason: str
    mutate: Callable[[Path], None]


ATTACKS = (
    Attack(
        "deep_clipped_partition_reclosure",
        "TARGET_CELL_RECONSTRUCTION_MISMATCH",
        mutate_deep_clipped_partition_reclosure,
    ),
    Attack(
        "deep_source_owner_reclosure",
        "SOURCE_STRATA_RECONSTRUCTION_MISMATCH",
        mutate_deep_source_owner_reclosure,
    ),
    Attack(
        "child_stratum_credit_mint",
        "CHILD_OR_VOLUME_CREDIT_VIOLATION",
        mutate_child_stratum_credit,
    ),
    Attack(
        "algebraic_source_volume_credit_mint",
        "CHILD_OR_VOLUME_CREDIT_VIOLATION",
        mutate_algebraic_volume_credit,
    ),
    Attack(
        "D02_promotion",
        "D02_NONPROMOTION_VIOLATION",
        mutate_d02_promotion,
    ),
    Attack(
        "CM2_promotion",
        "CM2_NONPROMOTION_VIOLATION",
        mutate_cm2_promotion,
    ),
    Attack(
        "input_pin_rewrite",
        "INPUT_PIN_CONTRACT_MISMATCH",
        mutate_input_pin,
    ),
    Attack(
        "conditional_predecessor_order_consumption",
        "CONDITIONAL_ORDER_CONTRACT_MISMATCH",
        mutate_conditional_order,
    ),
)


def assert_exact_rejection(
    verifier: ModuleType,
    candidate: Path,
    reference: Any,
    attack: Attack,
) -> str:
    try:
        verifier.verify_candidate_dir(candidate, reference)
    except verifier.VerificationFailure as error:
        require(
            error.reason == attack.expected_reason,
            "wrong Reject reason:"
            + attack.name
            + ":expected="
            + attack.expected_reason
            + ":actual="
            + error.reason,
        )
        return error.reason
    except BaseException as error:
        raise HarnessFailure(
            "untyped rejection:" + attack.name + ":" + repr(error)
        ) from error
    raise HarnessFailure("attack accepted:" + attack.name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    arguments = parser.parse_args()
    require(
        sys.flags.isolated == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True,
        "run with the pinned interpreter using -I -B",
    )
    candidate = Path(
        os.path.abspath(os.fspath(arguments.candidate_dir))
    )
    verifier = load_pinned_verifier()
    reference = verifier.reconstruct_reference()
    baseline = verifier.verify_candidate_dir(candidate, reference)
    require(
        baseline["formal_credit"] == {
            "verified_target_cell_dispositions": 0,
            "verified_source_atomic_strata": 0,
            "verified_whole_origin_exclusions": 0,
            "D02": 0,
            "CM2": 0,
        }
        and baseline["artifacts_written"] == 0,
        "zero-credit read-only baseline",
    )
    before = baseline_state(candidate)
    outcomes: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30f-attacks-") as temporary:
        root = Path(temporary)
        for ordinal, attack in enumerate(ATTACKS):
            mutated = root / f"{ordinal:02d}-{attack.name}"
            copy_candidate(candidate, mutated)
            attack.mutate(mutated)
            require(
                baseline_state(mutated) != before,
                "attack changes candidate:" + attack.name,
            )
            reason = assert_exact_rejection(
                verifier,
                mutated,
                reference,
                attack,
            )
            outcomes.append({
                "attack": attack.name,
                "expected_reject_reason": attack.expected_reason,
                "actual_reject_reason": reason,
            })
            shutil.rmtree(mutated)
    require(
        baseline_state(candidate) == before
        and PRODUCER_MODULE_NAME not in sys.modules,
        "baseline immutable and producer inert",
    )
    body = {
        "schema": (
            "cm2.round306c30f.retained-physical-seam."
            "coherent-attack-harness.report.v1"
        ),
        "status": (
            "PASS_ALL_C30F_COHERENT_ATTACKS_REJECTED_WITH_EXACT_REASONS__"
            "ZERO_FORMAL_CREDIT"
        ),
        "baseline_result_sha256": baseline["candidate_result_sha256"],
        "baseline_file_sha256": before,
        "attack_count": len(outcomes),
        "attacks": outcomes,
        "producer_imported_or_executed": False,
        "formal_credit": {
            "attack_successes": 0,
            "target_cell_dispositions": 0,
            "source_strata_dispositions": 0,
            "whole_origin_exclusions": 0,
            "D02": 0,
            "CM2": 0,
        },
        "artifacts_written": 0,
        "manifest_authorized": False,
    }
    print(wire({**body, "report_sha256": digest(body)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
