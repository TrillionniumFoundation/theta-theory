#!/usr/bin/env python3
"""Bounded coherent-corruption rejection suite for the C30b certificate.

The pinned independent verifier is imported exactly once and its expensive
upstream reference is reconstructed exactly once.  Attacks that fail before
the mathematical row loop use the full candidate entry point.  Attacks aimed
at the whole-origin or result layers call the exact validation function used
by that entry point, with all earlier candidate bytes left at their pinned
valid values.  This avoids needlessly replaying all 688 H cells for every
result-field mutation while testing the same fail-close predicates.
"""

from __future__ import annotations

import argparse
import copy
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
PREFIX = "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition"
VERIFIER_NAME = PREFIX + "_independent_verifier.py"
VERIFIER_PATH = ROOT / VERIFIER_NAME
VERIFIER_SHA256 = (
    "1776137520b1add49a218e6ccce680aaffdafc195c99ef7992c1a5ee31694b66"
)
RUNTIME = "cm2_round306c30b_python_flint_runtime_attestation.json"
H_LEDGER = PREFIX + "_h_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
EXPECTED_FILES = {RUNTIME, H_LEDGER, ORIGIN_LEDGER, RESULT}
EXPECTED_BASELINE_SHA256 = {
    RUNTIME: "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df",
    H_LEDGER: "4259fdaadfe1b5e1c0b7b315ef71fdae245bb3bbc45c5f814c4d4b7a670e8672",
    ORIGIN_LEDGER: "19edfece87d4f95e3e25a62d508654918c03ec879f574ab01854bde5bee4c6c9",
    RESULT: "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b",
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
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def close_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop(field, None)
    return {**body, field: digest(body)}


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    return close_object(value, "row_sha256")


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    return close_object(value, "result_sha256")


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    if type(value) is not dict:
        raise RuntimeError("expected JSON object:" + path.name)
    return value


def read_rows(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        values = [json.loads(line) for line in handle]
    if not values or not all(type(value) is dict for value in values):
        raise RuntimeError("expected nonempty JSONL object ledger:" + path.name)
    return values


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(wire(close_result(result)) + b"\n")


def write_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0
        ) as output:
            for row in rows:
                output.write(wire(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


def rebind_ledger(
    target: Path,
    result: dict[str, Any],
    filename: str,
    descriptor_key: str,
    rows: list[dict[str, Any]],
) -> None:
    facts = write_rows(target / filename, rows)
    descriptor = result["ledgers"][descriptor_key]
    for key, value in facts.items():
        descriptor[key] = value


def copy_candidate(source: Path, target: Path) -> None:
    for filename in sorted(EXPECTED_FILES):
        shutil.copyfile(source / filename, target / filename)


def assert_pinned_baseline(candidate: Path) -> None:
    status = candidate.lstat()
    if not stat.S_ISDIR(status.st_mode) or candidate.is_symlink():
        raise RuntimeError("baseline is not a regular directory")
    if {path.name for path in candidate.iterdir()} != EXPECTED_FILES:
        raise RuntimeError("baseline exact file set")
    observed = {
        filename: file_hash(candidate / filename)
        for filename in sorted(EXPECTED_FILES)
    }
    if observed != EXPECTED_BASELINE_SHA256:
        raise RuntimeError("baseline four-file SHA-256 identity")


def load_pinned_verifier() -> ModuleType:
    path = VERIFIER_PATH.resolve(strict=True)
    status = path.lstat()
    if (
        not stat.S_ISREG(status.st_mode)
        or path.is_symlink()
        or status.st_nlink != 1
        or file_hash(path) != VERIFIER_SHA256
    ):
        raise RuntimeError("pinned verifier source identity")
    module_name = "_cm2_round306c30b_pinned_independent_verifier"
    if module_name in sys.modules:
        raise RuntimeError("verifier already imported")
    specification = importlib.util.spec_from_file_location(module_name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError("verifier import specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def candidate_state(
    target: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    return (
        read_object(target / RESULT),
        read_rows(target / H_LEDGER),
        read_rows(target / ORIGIN_LEDGER),
    )


def cascade_h_change(
    target: Path,
    result: dict[str, Any],
    h_rows: list[dict[str, Any]],
    origin_rows: list[dict[str, Any]],
    changed_h_ordinal: int,
) -> None:
    changed = h_rows[changed_h_ordinal]
    origin_key = changed["origin_key"]
    if (
        changed["source_kind"]
        == "ROUND180_INHERITED_SAME_SIGN_DELTA_FOLLOWUP_H"
    ):
        raise RuntimeError("attack fixture must avoid followup-H cascade")
    matching_h = [row for row in h_rows if row["origin_key"] == origin_key]
    matching_origin = [
        ordinal
        for ordinal, row in enumerate(origin_rows)
        if row["origin_key"] == origin_key
    ]
    if len(matching_origin) != 1:
        raise RuntimeError("unique attacked origin")
    origin_ordinal = matching_origin[0]
    origin = copy.deepcopy(origin_rows[origin_ordinal])
    origin["H_cell_rows_sha256"] = digest(matching_h)
    aggregation = origin["lineage_composition_evidence"][
        "materialized_H_strata_owner_aggregation"
    ]
    aggregation["terminal_exact_atomic_audit_list_sha256"] = digest([
        row["H_partition"]["terminal_exact_atomic_owner_audit"]
        for row in matching_h
    ])
    origin_rows[origin_ordinal] = close_row(origin)
    rebind_ledger(
        target, result, H_LEDGER, "outgoing_H_cell", h_rows
    )
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_disposition",
        origin_rows,
    )
    write_result(target, result)


def mutate_runtime_attestation(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    attestation = read_object(target / RUNTIME)
    attestation["offline"] = False
    body = {
        key: value
        for key, value in attestation.items()
        if key != "attestation_payload_sha256"
    }
    attestation["attestation_payload_sha256"] = digest(body)
    raw = wire(attestation) + b"\n"
    (target / RUNTIME).write_bytes(raw)
    result["runtime_attestation"].update({
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "attestation_payload_sha256": attestation[
            "attestation_payload_sha256"
        ],
    })
    write_result(target, result)


def mutate_h_provenance(target: Path) -> None:
    result, h_rows, origin_rows = candidate_state(target)
    row = copy.deepcopy(h_rows[0])
    if "C30a_held_row_sha256" not in row["source_binding"]:
        raise RuntimeError("expected held-H provenance fixture")
    row["source_binding"]["C30a_held_row_sha256"] = "0" * 64
    h_rows[0] = close_row(row)
    cascade_h_change(target, result, h_rows, origin_rows, 0)


def mutate_h_atomic_owner(target: Path) -> None:
    result, h_rows, origin_rows = candidate_state(target)
    row = copy.deepcopy(h_rows[0])
    partition = row["H_partition"]
    audit = partition["terminal_exact_atomic_owner_audit"]
    audit["atomic_owner_selection_rule"] = (
        "FORGED_LEXICOGRAPHIC_MAX_CONTAINING_LEAF"
    )
    audit["atomic_2D_owner_rows_sha256"] = "f" * 64
    partition["terminal_exact_atomic_owner_audit_sha256"] = digest(audit)
    h_rows[0] = close_row(row)
    cascade_h_change(target, result, h_rows, origin_rows, 0)


def mutate_origin_order(target: Path) -> None:
    result, _h_rows, origin_rows = candidate_state(target)
    origin_rows[0], origin_rows[1] = origin_rows[1], origin_rows[0]
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_disposition",
        origin_rows,
    )
    write_result(target, result)


def mutate_origin_disposition(target: Path) -> None:
    result, _h_rows, origin_rows = candidate_state(target)
    row = copy.deepcopy(origin_rows[0])
    if row["whole_origin_disposition"] != "RESOLVED_MIXED":
        raise RuntimeError("expected mixed-origin fixture")
    row["whole_origin_disposition"] = "EXCLUDED"
    row["whole_original_physical_origin_excluded"] = True
    row["whole_origin_exclusion_credit"] = 1
    row["resolved_nonexcluded_credit"] = 0
    row["positive_measure_LIVE_witness_count"] = 0
    row["positive_measure_LIVE_witnesses_sha256"] = digest([])
    row["lexicographic_first_positive_measure_LIVE_witness"] = (
        "NOT_APPLICABLE_EXCLUDED"
    )
    row["formal_credit"]["whole_source_W_origin_exclusion"] = 1
    theorem = row["whole_origin_theorem"]
    theorem["whole_original_physical_origin_excluded"] = True
    row["whole_origin_theorem_sha256"] = digest(theorem)
    origin_rows[0] = close_row(row)

    excluded = sorted(
        value["origin_key"]
        for value in origin_rows
        if value["whole_origin_disposition"] == "EXCLUDED"
    )
    mixed = sorted(
        value["origin_key"]
        for value in origin_rows
        if value["whole_origin_disposition"] == "RESOLVED_MIXED"
    )
    census = result["whole_origin_census"]
    census.update({
        "excluded": len(excluded),
        "resolved_mixed": len(mixed),
        "excluded_origin_keys_sha256": digest(excluded),
        "resolved_mixed_origin_keys_sha256": digest(mixed),
    })
    result["formal_credit"]["whole_source_W_origin_exclusions"] = 3
    transition = result["source_W_ledger_transition"]
    transition["credits"].update({
        "whole_origin_exclusion": 3,
        "resolved_nonexcluded": 9,
    })
    transition["after"].update({
        "excluded": 74747,
        "conservative_live": 2085,
        "resolved_nonexcluded": 2005,
    })
    transition["conservation_identity"] = "74747+2085=76832"
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_disposition",
        origin_rows,
    )
    write_result(target, result)


def mutate_origin_atomic_reclosure(target: Path) -> None:
    result, _h_rows, origin_rows = candidate_state(target)
    row = copy.deepcopy(origin_rows[0])
    audit = row["lineage_composition_evidence"][
        "disposition_aware_half_open_owner_audit"
    ]
    audit["atomic_owner_selection_rule"] = (
        "FORGED_LEXICOGRAPHIC_MAX_CONTAINING_LEAF"
    )
    audit["raw_2D_stratum_reclosure_rows_sha256"] = "e" * 64
    origin_rows[0] = close_row(row)
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_disposition",
        origin_rows,
    )
    write_result(target, result)


def mutate_descriptor_order(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    result["ledgers"]["outgoing_H_cell"]["order"] = (
        "FORGED_REVERSE_H_CELL_KEY"
    )
    write_result(target, result)


def mutate_phantom_ledger(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    phantom = copy.deepcopy(result["ledgers"]["outgoing_H_cell"])
    phantom["filename"] = "phantom_ledger.jsonl.gz"
    result["ledgers"]["phantom"] = phantom
    write_result(target, result)


def mutate_input_pin(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    result["input_pins"][0]["sha256"] = "0" * 64
    write_result(target, result)


def mutate_transition(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    transition = result["source_W_ledger_transition"]
    transition["credits"].update({
        "resolved_origin_disposition": 13,
        "resolved_nonexcluded": 11,
    })
    transition["after"].update({
        "remaining": 79,
        "resolved_nonexcluded": 2007,
    })
    transition["after"]["remaining_partition"]["compact_q"] = 53
    result["formal_credit"][
        "resolved_source_W_origin_dispositions"
    ] = 13
    result["strict_nonpromotion"]["D02"] = (
        "BLOCKED_BY_79_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE"
    )
    write_result(target, result)


def mutate_d02(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    result["strict_nonpromotion"]["D02"] = "CLEARED"
    write_result(target, result)


def mutate_cm2(target: Path) -> None:
    result, _h_rows, _origin_rows = candidate_state(target)
    result["strict_nonpromotion"]["CM2"] = "GO"
    write_result(target, result)


def mutate_child_volume_credit(target: Path) -> None:
    result, _h_rows, origin_rows = candidate_state(target)
    row = copy.deepcopy(origin_rows[0])
    row["strict_nonpromotion"]["child_or_volume_as_integer_credit"] = 1
    origin_rows[0] = close_row(row)
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_disposition",
        origin_rows,
    )
    write_result(target, result)


@dataclass(frozen=True)
class Attack:
    name: str
    layer: str
    mutate: Callable[[Path], None]
    expected_reason_prefix: str


def full_validator(
    verifier: ModuleType, reference: Any, target: Path
) -> None:
    verifier.verify_candidate_dir(target, reference)


def origin_validator(
    verifier: ModuleType, reference: Any, target: Path
) -> None:
    h_rows = verifier.canonical_rows(target / H_LEDGER)
    origin_rows = verifier.canonical_rows(target / ORIGIN_LEDGER)
    row = origin_rows[0]
    origin_key = row["origin_key"]
    matching_h = [
        value for value in h_rows if value["origin_key"] == origin_key
    ]
    ordinal = list(verifier.EXPECTED_KEYS).index(origin_key)
    verifier.validate_origin_row(
        row,
        ordinal,
        reference.compositions[origin_key],
        matching_h,
        reference.registry[origin_key],
    )


def result_validator(
    verifier: ModuleType, reference: Any, target: Path
) -> None:
    result = verifier.strict_json(target / RESULT)
    h_rows = verifier.canonical_rows(target / H_LEDGER)
    origin_rows = verifier.canonical_rows(target / ORIGIN_LEDGER)
    pins = [
        {"filename": filename, "sha256": sha256}
        for filename, sha256 in reference.pins
    ]
    verifier.validate_result(
        result, target, h_rows, origin_rows, pins, reference.lanes,
    )


def assert_rejected(
    verifier: ModuleType,
    reference: Any,
    target: Path,
    layer: str,
    expected_reason_prefix: str,
) -> tuple[str, str]:
    validators = {
        "full": full_validator,
        "whole-origin": origin_validator,
        "result": result_validator,
    }
    validator = validators[layer]
    accepted = False
    try:
        validator(verifier, reference, target)
        accepted = True
    except (verifier.Reject, KeyError, OSError, ValueError, TypeError) as error:
        exception = type(error).__name__
        reason = str(error)
        if exception != "Reject" or not reason.startswith(expected_reason_prefix):
            raise RuntimeError(
                "corruption rejected for an unexpected reason:"
                + exception + ":" + reason
            ) from error
        return exception, reason
    if accepted:
        raise RuntimeError("coherent corruption accepted")
    raise RuntimeError("unreachable rejection state")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    arguments = parser.parse_args()
    if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
        raise RuntimeError("run with the pinned interpreter using -I -B")
    candidate = Path(os.path.abspath(os.fspath(arguments.candidate_dir)))
    assert_pinned_baseline(candidate)

    verifier = load_pinned_verifier()
    reference = verifier.reconstruct_reference()
    baseline = verifier.verify_candidate_dir(candidate, reference)
    if not (
        baseline["status"].startswith("PASS_INDEPENDENT_C30B__")
        and baseline["candidate_result_sha256"]
        == "7abf8da628eb35b20ed27b032dc55ea29e9944530d2d5a6a64993a995f1ad85e"
    ):
        raise RuntimeError("pinned baseline did not independently verify")
    attacks = (
        Attack(
            "runtime-attestation-self-reclosure", "full",
            mutate_runtime_attestation,
            "candidate runtime attestation byte identity",
        ),
        Attack(
            "H-source-provenance-rebind", "full", mutate_h_provenance,
            "H candidate source binding:",
        ),
        Attack(
            "H-atomic-owner-deep-reclosure", "full", mutate_h_atomic_owner,
            "H independent partition:",
        ),
        Attack(
            "whole-origin-ledger-order-reclosure", "full",
            mutate_origin_order, "candidate row count and canonical order",
        ),
        Attack(
            "whole-origin-disposition-reclassification",
            "whole-origin",
            mutate_origin_disposition,
            "whole-origin row:",
        ),
        Attack(
            "whole-origin-3D-2D-1D-0D-deep-reclosure",
            "whole-origin",
            mutate_origin_atomic_reclosure,
            "independent exact 3D/2D/1D/0D owner reclosure:",
        ),
        Attack(
            "ledger-descriptor-order", "result", mutate_descriptor_order,
            "ledger order contract:",
        ),
        Attack(
            "phantom-ledger-field", "result", mutate_phantom_ledger,
            "result schema",
        ),
        Attack(
            "input-pin-retarget", "result", mutate_input_pin,
            "result schema",
        ),
        Attack(
            "source-W-transition-80-to-79", "result", mutate_transition,
            "source-W 92 to 80 transition",
        ),
        Attack(
            "D02-illegal-clear", "result", mutate_d02,
            "formal credit / composite fail-close",
        ),
        Attack(
            "CM2-illegal-GO", "result", mutate_cm2,
            "formal credit / composite fail-close",
        ),
        Attack(
            "child-volume-as-integer-credit", "whole-origin",
            mutate_child_volume_credit, "whole-origin row:",
        ),
    )

    rejected: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30b-rejection-suite-") as raw:
        base = Path(raw)
        for ordinal, attack in enumerate(attacks):
            target = base / f"{ordinal:02d}-{attack.name}"
            target.mkdir()
            copy_candidate(candidate, target)
            attack.mutate(target)
            exception, reason = assert_rejected(
                verifier, reference, target, attack.layer,
                attack.expected_reason_prefix,
            )
            rejected.append({
                "attack": attack.name,
                "validation_layer": attack.layer,
                "exception": exception,
                "reason": reason,
            })

    print(wire({
        "schema": "cm2.round306c30b.coherent-corruption-rejection-suite.v1",
        "status": "PASS_13_OF_13_COHERENT_CORRUPTIONS_REJECTED",
        "pinned_verifier_sha256": VERIFIER_SHA256,
        "baseline_validation": (
            "PINNED_FOUR_FILE_BYTE_IDENTITY_AND_FULL_INDEPENDENT_PASS"
        ),
        "baseline_status": baseline["status"],
        "reference_reconstruction_count": 1,
        "attack_count": len(attacks),
        "expected_exception": "Reject",
        "expected_reason_prefixes_enforced": True,
        "rejected": rejected,
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
