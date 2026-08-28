#!/usr/bin/env python3
"""Coherent candidate-corruption harness for append-only C30f v2.

The pinned no-import verifier first accepts the untouched candidate.  Each
attack mutates only a temporary copy and recloses the affected row, gzip
ledger, descriptor, origin dependency and result object where applicable.
This is a candidate harness, not release authority or a terminal seal.
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
    "whole_origin_exclusion_v2"
)
CELL_LEDGER = PREFIX + "_target_cell_ledger.jsonl.gz"
SOURCE_STRATA_LEDGER = PREFIX + "_source_half_open_strata_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
EXPECTED_FILES = {CELL_LEDGER, SOURCE_STRATA_LEDGER, ORIGIN_LEDGER, RESULT}
VERIFIER_SOURCE = PREFIX + "_independent_verifier.py"
VERIFIER_SOURCE_SHA256 = (
    "0266e52dfb451ec0bae90e7c7ba22b4a5384624dc11ef33e105fca2b7d770b53"
)
PRODUCER_MODULE_NAME = PREFIX + "_producer"

CONTROLLED_HASH_SEEDS = frozenset({"30630071", "30630929"})
CONTROLLED_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
}
HASH_SEED_SENTINEL = "CM2_C30F_HASH_SEED_SENTINEL_v2"
HASH_FINGERPRINTS = {
    "30630071": -3949014500883849868,
    "30630929": 276388808340754406,
}
INITIAL_SAFE_SYS_PATH = tuple(sys.path)


class HarnessFailure(RuntimeError):
    """A failure of the harness rather than an attacked candidate."""


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


def validate_runtime() -> None:
    environment = dict(os.environ)
    seed = environment.pop("PYTHONHASHSEED", None)
    require(
        bool(
            sys.flags.isolated == 0
            and sys.flags.ignore_environment == 0
            and sys.flags.safe_path is True
            and sys.flags.no_user_site == 1
            and sys.flags.dont_write_bytecode == 1
            and sys.flags.hash_randomization == 1
        ),
        "C30F_ATTACKS_REQUIRES_ENV_I_AND_PYTHON_P_S_B",
    )
    require(
        bool(
            seed in CONTROLLED_HASH_SEEDS
            and environment == CONTROLLED_ENVIRONMENT
            and hash(HASH_SEED_SENTINEL) == HASH_FINGERPRINTS[seed]
            and "" not in INITIAL_SAFE_SYS_PATH
            and os.fspath(ROOT) not in INITIAL_SAFE_SYS_PATH
        ),
        "C30F_ATTACKS_CONTROLLED_ENVIRONMENT",
    )


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = {key: item for key, item in value.items() if key != "row_sha256"}
    return {**body, "row_sha256": digest(body)}


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = {key: item for key, item in value.items() if key != "result_sha256"}
    return {**body, "result_sha256": digest(body)}


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes().decode("ascii"))
    require(type(value) is dict, "object:" + path.name)
    return value


def read_rows(path: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    with gzip.open(path, "rt", encoding="ascii", newline="") as stream:
        for line in stream:
            value = json.loads(line)
            require(type(value) is dict, "row:" + path.name)
            output.append(value)
    require(bool(output), "nonempty-ledger:" + path.name)
    return output


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(wire(close_result(result)))


def write_rows(
    path: Path, rows: list[dict[str, Any]], order: str
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", compresslevel=9, fileobj=raw, mtime=0
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


def unbound_row(value: dict[str, Any]) -> dict[str, Any]:
    body = {
        key: item for key, item in value.items()
        if key not in {"row_sha256", "c30e_terminal_predecessor"}
    }
    return {**body, "row_sha256": digest(body)}


def copy_candidate(source: Path, target: Path) -> None:
    require(
        bool(
            source.is_dir()
            and not source.is_symlink()
            and {path.name for path in source.iterdir()} == EXPECTED_FILES
        ),
        "baseline exact file set",
    )
    target.mkdir()
    for filename in EXPECTED_FILES:
        path = source / filename
        status = path.lstat()
        require(
            bool(stat.S_ISREG(status.st_mode) and not path.is_symlink()
                 and status.st_nlink == 1),
            "baseline regular singleton:" + filename,
        )
        shutil.copyfile(path, target / filename)


def state(candidate: Path) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for filename in sorted(EXPECTED_FILES):
        path = candidate / filename
        status = path.lstat()
        output[filename] = {
            "sha256": file_hash(path),
            "mode": status.st_mode,
            "nlink": status.st_nlink,
            "symlink": path.is_symlink(),
        }
    return output


def load_verifier() -> ModuleType:
    path = ROOT / VERIFIER_SOURCE
    status = path.lstat()
    require(
        bool(
            stat.S_ISREG(status.st_mode)
            and not path.is_symlink()
            and status.st_nlink == 1
            and file_hash(path) == VERIFIER_SOURCE_SHA256
        ),
        "pinned C30f v2 verifier",
    )
    module_name = VERIFIER_SOURCE[:-3]
    require(
        bool(module_name not in sys.modules and PRODUCER_MODULE_NAME not in sys.modules),
        "verifier and producer not preloaded",
    )
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(bool(specification is not None and specification.loader is not None),
            "verifier import specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    require(
        bool(
            Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
            and file_hash(path) == VERIFIER_SOURCE_SHA256
            and PRODUCER_MODULE_NAME not in sys.modules
        ),
        "verifier identity and inert producer",
    )
    return module


def cascade_origins(target: Path, origins: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    result["ledgers"]["whole_origin_exclusion_candidate"] = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    write_result(target, result)


def cascade_cells(target: Path, cells: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGIN_LEDGER)
    result["ledgers"]["target_cell_candidate"] = write_rows(
        target / CELL_LEDGER,
        cells,
        "LEXICOGRAPHIC_ROUND180_FINAL_CELL_KEY",
    )
    for origin in origins:
        values = [
            unbound_row(row) for row in cells
            if row["origin_key"] == origin["origin_key"]
        ]
        origin["target_cell_rows_sha256"] = digest(values)
    result["ledgers"]["whole_origin_exclusion_candidate"] = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    write_result(target, result)


def cascade_strata(target: Path, strata: list[dict[str, Any]]) -> None:
    result = read_object(target / RESULT)
    origins = read_rows(target / ORIGIN_LEDGER)
    result["ledgers"]["source_half_open_strata_candidate"] = write_rows(
        target / SOURCE_STRATA_LEDGER,
        strata,
        "LEXICOGRAPHIC_ORIGIN_KEY_THEN_SOURCE_STRATUM_ID",
    )
    for origin in origins:
        values = [
            unbound_row(row) for row in strata
            if row["origin_key"] == origin["origin_key"]
        ]
        origin["source_half_open_strata_row_count"] = len(values)
        origin["source_half_open_strata_rows_sha256"] = digest(values)
        theorem = origin["source_half_open_atomic_theorem"]
        theorem["source_strata_rows_sha256"] = digest(values)
        origin["source_half_open_atomic_theorem_sha256"] = digest(theorem)
    result["ledgers"]["whole_origin_exclusion_candidate"] = write_rows(
        target / ORIGIN_LEDGER,
        origins,
        "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
    )
    write_result(target, result)


def mutate_cell_partition(target: Path) -> None:
    rows = read_rows(target / CELL_LEDGER)
    row = next(item for item in rows if item["source_kind"]
               == "SEALED_C30A_REDUCED_CLIPPED_KERNEL_REPLAY")
    row["partition"]["closed_box_and_all_owned_faces_edges_vertices_excluded"] = False
    row["partition"]["all_graph_face_edge_corner_strata_inherit_the_graph_disposition"] = False
    cascade_cells(target, rows)


def mutate_source_owner(target: Path) -> None:
    rows = read_rows(target / SOURCE_STRATA_LEDGER)
    row = next(item for item in rows if item["ambient_dimension"] == 0)
    row["dyadic_owner_proof_source"] = "COHERENT_ATTACK_REBINDS_OWNER"
    cascade_strata(target, rows)


def mutate_origin_disposition(target: Path) -> None:
    rows = read_rows(target / ORIGIN_LEDGER)
    rows[0]["whole_origin_disposition_candidate"] = "RESOLVED_MIXED"
    cascade_origins(target, rows)


def mutate_row_authority(target: Path) -> None:
    rows = read_rows(target / CELL_LEDGER)
    rows[0]["c30e_terminal_predecessor"]["binding_sha256"] = "f" * 64
    cascade_cells(target, rows)


def mutate_result_authority(target: Path) -> None:
    result = read_object(target / RESULT)
    result["c30e_terminal_authority"]["binding_sha256"] = "e" * 64
    write_result(target, result)


def mutate_before_56(target: Path) -> None:
    result = read_object(target / RESULT)
    result["source_W_handoff_candidate"]["before"]["remaining"] = 55
    write_result(target, result)


def mutate_after_54(target: Path) -> None:
    result = read_object(target / RESULT)
    result["source_W_handoff_candidate"]["after_if_later_terminal_release_passes"]["remaining"] = 53
    write_result(target, result)


def mutate_status_prefix(target: Path) -> None:
    result = read_object(target / RESULT)
    result["status"] += "__PREFIX_CONFUSION_ATTACK"
    write_result(target, result)


def mutate_d02_credit(target: Path) -> None:
    result = read_object(target / RESULT)
    result["formal_credit"]["D02"] = 1
    write_result(target, result)


def mutate_cm2_credit(target: Path) -> None:
    result = read_object(target / RESULT)
    result["formal_credit"]["CM2"] = 1
    result["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    write_result(target, result)


def mutate_origin_credit(target: Path) -> None:
    rows = read_rows(target / ORIGIN_LEDGER)
    rows[0]["formal_credit"]["whole_source_W_origin_exclusion"] = 1
    cascade_origins(target, rows)


def mutate_child_volume_credit(target: Path) -> None:
    rows = read_rows(target / ORIGIN_LEDGER)
    rows[0]["exact_rational_enclosure_volume_conservation"][
        "algebraic_source_substrata_volume_used_as_credit"
    ] = True
    rows[0]["formal_credit"]["resolved_source_W_origin_disposition"] = 1
    cascade_origins(target, rows)


def mutate_extra_member(target: Path) -> None:
    (target / "UNAUTHORIZED.extra").write_bytes(b"attack")


def mutate_result_symlink(target: Path) -> None:
    source = target.parent / (target.name + ".symlink-source")
    shutil.copyfile(target / RESULT, source)
    (target / RESULT).unlink()
    (target / RESULT).symlink_to(source)


def mutate_result_hardlink(target: Path) -> None:
    source = target.parent / (target.name + ".hardlink-source")
    shutil.copyfile(target / RESULT, source)
    (target / RESULT).unlink()
    os.link(source, target / RESULT)


def mutate_gzip_truncate(target: Path) -> None:
    path = target / SOURCE_STRATA_LEDGER
    raw = path.read_bytes()
    path.write_bytes(raw[:-17])


@dataclass(frozen=True)
class Attack:
    name: str
    reason: str
    mutate: Callable[[Path], None]


ATTACKS = (
    Attack("deep_cell_partition_reclosure", "TARGET_CELL_RECONSTRUCTION_MISMATCH", mutate_cell_partition),
    Attack("deep_source_owner_reclosure", "SOURCE_STRATA_RECONSTRUCTION_MISMATCH", mutate_source_owner),
    Attack("whole_origin_disposition_reclosure", "ORIGIN_RECONSTRUCTION_MISMATCH", mutate_origin_disposition),
    Attack("row_predecessor_binding_reclosure", "TARGET_CELL_RECONSTRUCTION_MISMATCH", mutate_row_authority),
    Attack("result_predecessor_authority_reclosure", "PREDECESSOR_AUTHORITY_MISMATCH", mutate_result_authority),
    Attack("fake_before_56_reclosure", "RESULT_RECONSTRUCTION_MISMATCH", mutate_before_56),
    Attack("fake_after_54_reclosure", "RESULT_RECONSTRUCTION_MISMATCH", mutate_after_54),
    Attack("status_prefix_confusion", "RESULT_RECONSTRUCTION_MISMATCH", mutate_status_prefix),
    Attack("D02_credit_mint", "ZERO_FORMAL_CREDIT_REQUIRED", mutate_d02_credit),
    Attack("CM2_credit_mint", "ZERO_FORMAL_CREDIT_REQUIRED", mutate_cm2_credit),
    Attack("origin_credit_mint", "ZERO_FORMAL_CREDIT_REQUIRED", mutate_origin_credit),
    Attack("algebraic_volume_credit_mint", "ZERO_FORMAL_CREDIT_REQUIRED", mutate_child_volume_credit),
    Attack("extra_candidate_member", "CANDIDATE_FORMAT_VIOLATION", mutate_extra_member),
    Attack("result_symlink", "CANDIDATE_FORMAT_VIOLATION", mutate_result_symlink),
    Attack("result_hardlink", "CANDIDATE_FORMAT_VIOLATION", mutate_result_hardlink),
    Attack("gzip_truncation", "CANDIDATE_FORMAT_VIOLATION", mutate_gzip_truncate),
)


def exact_reject(
    verifier: ModuleType,
    candidate: Path,
    authority: dict[str, Any],
    reference: dict[str, Any],
    attack: Attack,
) -> str:
    try:
        verifier.verify_candidate_dir(candidate, authority, reference)
    except verifier.VerificationFailure as error:
        require(
            error.reason == attack.reason,
            "wrong rejection:" + attack.name + ":" + error.reason,
        )
        return error.reason
    except BaseException as error:
        raise HarnessFailure("untyped rejection:" + attack.name + ":" + repr(error)) from error
    raise HarnessFailure("attack accepted:" + attack.name)


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    validate_runtime()
    verifier = load_verifier()
    verifier.validate_runtime()
    authority = verifier.capture_c30e_authority(
        arguments.predecessor_adapter,
        arguments.predecessor_adapter_sha256,
        arguments.predecessor_chain_dir,
        arguments.predecessor_pins,
        arguments.predecessor_pins_sha256,
    )
    reference = verifier.reconstruct_reference(authority)
    candidate = Path(os.path.abspath(os.fspath(arguments.candidate_dir)))
    baseline = verifier.verify_candidate_dir(candidate, authority, reference)
    before = state(candidate)
    outcomes: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30f-v2-attacks-") as name:
        root = Path(name)
        for ordinal, attack in enumerate(ATTACKS):
            mutated = root / f"{ordinal:02d}-{attack.name}"
            copy_candidate(candidate, mutated)
            attack.mutate(mutated)
            reason = exact_reject(verifier, mutated, authority, reference, attack)
            outcomes.append({
                "attack": attack.name,
                "expected_reject_reason": attack.reason,
                "actual_reject_reason": reason,
            })
    require(
        bool(state(candidate) == before and PRODUCER_MODULE_NAME not in sys.modules),
        "baseline immutable and producer inert",
    )
    body = {
        "schema": "cm2.round306c30f.retained-physical-seam.coherent-attack-harness.report.v2",
        "status": "PASS_ALL_C30F_V2_COHERENT_CANDIDATE_ATTACKS_REJECTED__ZERO_FORMAL_CREDIT",
        "baseline_result_sha256": baseline["candidate_result_sha256"],
        "baseline_file_facts": before,
        "c30e_authority_binding_sha256": authority["binding_sha256"],
        "attack_count": len(outcomes),
        "attacks": outcomes,
        "producer_imported_or_executed": False,
        "formal_credit": {
            "attack_successes": 0,
            "target_cell_dispositions": 0,
            "source_strata_dispositions": 0,
            "whole_origin_exclusions": 0,
            "D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0,
        },
        "artifacts_written": 0,
        "manifest_authorized": False,
        "terminal_authorized": False,
    }
    return {**body, "report_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    parser.add_argument("--predecessor-adapter", required=True, type=Path)
    parser.add_argument("--predecessor-adapter-sha256", required=True)
    parser.add_argument("--predecessor-chain-dir", required=True, type=Path)
    parser.add_argument("--predecessor-pins", required=True, type=Path)
    parser.add_argument("--predecessor-pins-sha256", required=True)
    arguments = parser.parse_args()
    try:
        report = run(arguments)
    except HarnessFailure as error:
        os.write(2, wire({"status": "REJECT", "reason": "HARNESS_FAILURE", "detail": str(error)}))
        return 1
    except BaseException as error:
        reason = "PREDECESSOR_OR_RUNTIME_REJECT"
        if type(error).__name__ == "VerificationFailure":
            reason = getattr(error, "reason", reason)
        os.write(2, wire({
            "status": "REJECT",
            "reason": reason,
            "detail": str(error),
            "formal_credit": {"D02": 0, "D03": 0, "D04": 0, "Gate5": 0, "CM2": 0},
        }))
        return 2
    os.write(1, wire(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
