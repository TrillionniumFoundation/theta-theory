#!/usr/bin/env python3
"""Coherent-corruption rejection suite for the candidate-only C30d lane.

The pinned independent verifier captures its C30c 78-state authority and
reconstructs its R184/R215/C30a mathematical reference exactly once.  Every
attack below rewrites canonical JSON, row hashes, gzip
bytes, ledger descriptors, and the result hash wherever those objects are in
the attacked dependency chain.  Acceptance is forbidden, and rejection must
be the verifier's ``Reject`` with the attack's declared reason prefix.
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
PREFIX = "cm2_round306c30d_source_w_multi_delta_whole_origin_exclusion"
VERIFIER = PREFIX + "_independent_verifier.py"
VERIFIER_SHA256 = (
    "faf778dcf6fb6e3f29c02dec20c545b3e72d4fd2e0453ba01fff81f5935ddbed"
)
PRODUCER = PREFIX + "_producer.py"
C30A_PRODUCER = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_producer.py"
)
C30B_PRODUCER = (
    "cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_producer.py"
)
C30C_PRODUCER = (
    "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_producer.py"
)
CELL_LEDGER = PREFIX + "_multi_delta_cell_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
RUNTIME_ATTESTATION = "cm2_round306c30b_python_flint_runtime_attestation.json"
EXPECTED_FILES = {
    RUNTIME_ATTESTATION,
    CELL_LEDGER,
    ATOMIC_OWNER_LEDGER,
    ORIGIN_LEDGER,
    RESULT,
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
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


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
    with gzip.open(path, "rb") as stream:
        rows = [json.loads(line) for line in stream]
    if not rows or not all(type(row) is dict for row in rows):
        raise RuntimeError("expected nonempty object ledger:" + path.name)
    return rows


def write_result(target: Path, result: dict[str, Any]) -> None:
    (target / RESULT).write_bytes(wire(close_result(result)))


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


def candidate_state(
    target: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    return (
        read_object(target / RESULT),
        read_rows(target / CELL_LEDGER),
        read_rows(target / ORIGIN_LEDGER),
    )


def copy_candidate(source: Path, target: Path) -> None:
    for filename in sorted(EXPECTED_FILES):
        shutil.copyfile(source / filename, target / filename)


def producer_modules_absent() -> bool:
    forbidden_files = (PRODUCER, C30A_PRODUCER, C30B_PRODUCER, C30C_PRODUCER)
    forbidden = {filename[:-3] for filename in forbidden_files}
    forbidden_paths = {(ROOT / filename).resolve() for filename in forbidden_files}
    for name, module in tuple(sys.modules.items()):
        if name in forbidden or any(
            name.endswith("." + item) for item in forbidden
        ):
            return False
        filename = getattr(module, "__file__", None)
        if filename is not None:
            try:
                if Path(filename).resolve() in forbidden_paths:
                    return False
            except (OSError, TypeError, ValueError):
                return False
    return True


def load_pinned_verifier() -> ModuleType:
    path = (ROOT / VERIFIER).resolve(strict=True)
    status = path.lstat()
    if (
        not stat.S_ISREG(status.st_mode)
        or path.is_symlink()
        or status.st_nlink != 1
        or file_hash(path) != VERIFIER_SHA256
        or not producer_modules_absent()
    ):
        raise RuntimeError("pinned verifier identity / producer independence")
    module_name = "_cm2_round306c30d_pinned_independent_verifier"
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
    if not producer_modules_absent():
        raise RuntimeError("producer imported while loading verifier")
    return module


def assert_baseline_shape(candidate: Path) -> None:
    status = candidate.lstat()
    if (
        not stat.S_ISDIR(status.st_mode)
        or candidate.is_symlink()
        or {path.name for path in candidate.iterdir()} != EXPECTED_FILES
    ):
        raise RuntimeError("baseline exact regular five-file candidate")


def assert_coherent_envelope(target: Path) -> None:
    """Check cryptographic/canonical closure without endorsing semantics."""
    result, cells, origins = candidate_state(target)
    atomic_owners = read_rows(target / ATOMIC_OWNER_LEDGER)
    if wire(result) != (target / RESULT).read_bytes():
        raise RuntimeError("attack result is not canonical")
    result_body = dict(result)
    claimed_result = result_body.pop("result_sha256", None)
    if claimed_result != digest(result_body):
        raise RuntimeError("attack result is not self-closed")
    for filename, rows, key in (
        (CELL_LEDGER, cells, "multi_Delta_cell_candidate"),
        (
            ATOMIC_OWNER_LEDGER,
            atomic_owners,
            "atomic_half_open_owner_candidate",
        ),
        (ORIGIN_LEDGER, origins, "whole_origin_exclusion_candidate"),
    ):
        for row in rows:
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            if claimed != digest(body):
                raise RuntimeError("attack row is not self-closed:" + filename)
        facts = result["ledgers"][key]
        sequence = hashlib.sha256()
        for row in rows:
            sequence.update(bytes.fromhex(row["row_sha256"]))
        observed = {
            "filename": filename,
            "row_count": len(rows),
            "size": (target / filename).stat().st_size,
            "sha256": file_hash(target / filename),
            "row_sequence_sha256": sequence.hexdigest(),
        }
        for fact, value in observed.items():
            if facts.get(fact) != value:
                raise RuntimeError("attack ledger is not coherently rebound:" + fact)


def cascade_cell_change(
    target: Path,
    result: dict[str, Any],
    cells: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    changed_ordinal: int,
) -> None:
    changed = cells[changed_ordinal]
    origin_key = changed["origin_key"]
    matching = [row for row in cells if row["origin_key"] == origin_key]
    positions = [
        ordinal for ordinal, row in enumerate(origins)
        if row["origin_key"] == origin_key
    ]
    if len(positions) != 1:
        raise RuntimeError("unique attacked origin")
    position = positions[0]
    origin = copy.deepcopy(origins[position])
    origin["Round306C30D_multi_Delta_cell_rows_sha256"] = digest(matching)
    origins[position] = close_row(origin)
    rebind_ledger(
        target,
        result,
        CELL_LEDGER,
        "multi_Delta_cell_candidate",
        cells,
    )
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_exclusion_candidate",
        origins,
    )
    write_result(target, result)


def mutate_universal_contact_deep_reclosure(target: Path) -> None:
    result, cells, origins = candidate_state(target)
    row = copy.deepcopy(cells[0])
    audit = row["frozen_owner_contact_audit"]
    audit["unique_strict_contact_chart"] = "W"
    audit["outgoing_chart_mismatch_on_every_possible_near_contact"] = False
    target_rows = row["exhaustive_possible_first_target_rows"]
    target_rows[-1]["strict_outgoing_chart"] = "W"
    row["exhaustive_possible_first_target_rows_sha256"] = digest(target_rows)
    cells[0] = close_row(row)
    cascade_cell_change(target, result, cells, origins, 0)


def mutate_target_tie_theorem_deep_reclosure(target: Path) -> None:
    result, cells, origins = candidate_state(target)
    row = copy.deepcopy(cells[0])
    theorem = row["closed_enclosure_exclusion_theorem_candidate"]
    theorem["first_target_tie_bookkeeping_owner_rule"] = (
        "FORGED_LEXICOGRAPHIC_GREATEST_TARGET_ID"
    )
    row["closed_enclosure_exclusion_theorem_candidate_sha256"] = digest(theorem)
    cells[0] = close_row(row)
    cascade_cell_change(target, result, cells, origins, 0)


def mutate_owner_3d_2d_1d_0d_deep_reclosure(target: Path) -> None:
    result, _cells, origins = candidate_state(target)
    atomic_owners = read_rows(target / ATOMIC_OWNER_LEDGER)
    attacked = copy.deepcopy(atomic_owners[0])
    attacked["owner_selection_rule"] = (
        "FORGED_LEXICOGRAPHIC_MAX_CONTAINING_LEAF"
    )
    atomic_owners[0] = close_row(attacked)
    origin_key = attacked["origin_key"]
    slice_rows = [
        row for row in atomic_owners if row["origin_key"] == origin_key
    ]
    positions = [
        ordinal for ordinal, row in enumerate(origins)
        if row["origin_key"] == origin_key
    ]
    if len(positions) != 1:
        raise RuntimeError("unique atomic-owner attacked origin")
    origin = copy.deepcopy(origins[positions[0]])
    summary = origin["materialized_atomic_half_open_owner_ledger_slice"]
    summary["rows_sha256"] = digest(slice_rows)
    summary["row_sha256_sequence_sha256"] = digest([
        row["row_sha256"] for row in slice_rows
    ])
    origin["materialized_atomic_half_open_owner_ledger_slice_sha256"] = digest(
        summary
    )
    origins[positions[0]] = close_row(origin)
    rebind_ledger(
        target,
        result,
        ATOMIC_OWNER_LEDGER,
        "atomic_half_open_owner_candidate",
        atomic_owners,
    )
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_exclusion_candidate",
        origins,
    )
    write_result(target, result)


def mutate_whole_origin_reclassification(target: Path) -> None:
    result, _cells, origins = candidate_state(target)
    row = copy.deepcopy(origins[0])
    row["whole_origin_disposition_candidate"] = "RESOLVED_MIXED"
    row["whole_original_physical_origin_excluded_candidate"] = False
    theorem = row["whole_origin_exclusion_theorem_candidate"]
    theorem["whole_original_physical_origin_excluded"] = False
    row["whole_origin_exclusion_theorem_candidate_sha256"] = digest(theorem)
    origins[0] = close_row(row)
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_exclusion_candidate",
        origins,
    )
    write_result(target, result)


def mutate_child_volume_credit(target: Path) -> None:
    result, _cells, origins = candidate_state(target)
    row = copy.deepcopy(origins[0])
    row["child_count_or_volume_used_as_whole_origin_credit"] = True
    origins[0] = close_row(row)
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_exclusion_candidate",
        origins,
    )
    write_result(target, result)


def mutate_formal_credit(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    result["formal_credit"]["whole_source_W_origin_exclusions"] = 20
    write_result(target, result)


def mutate_d02(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    result["strict_nonpromotion"]["D02"] = "CLEARED"
    write_result(target, result)


def mutate_cm2(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    result["strict_nonpromotion"]["CM2"] = "GO"
    write_result(target, result)


def mutate_input_pin(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    result["input_pins"][0]["sha256"] = "0" * 64
    write_result(target, result)


def mutate_ledger_order_contract(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    result["ledgers"]["multi_Delta_cell_candidate"]["order"] = (
        "FORGED_REVERSE_CELL_KEY"
    )
    write_result(target, result)


def mutate_cell_row_order(target: Path) -> None:
    result, cells, _origins = candidate_state(target)
    cells[0], cells[1] = cells[1], cells[0]
    rebind_ledger(
        target,
        result,
        CELL_LEDGER,
        "multi_Delta_cell_candidate",
        cells,
    )
    write_result(target, result)


def mutate_origin_row_order(target: Path) -> None:
    result, _cells, origins = candidate_state(target)
    origins[0], origins[1] = origins[1], origins[0]
    rebind_ledger(
        target,
        result,
        ORIGIN_LEDGER,
        "whole_origin_exclusion_candidate",
        origins,
    )
    write_result(target, result)


def mutate_phantom_ledger(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    phantom = copy.deepcopy(result["ledgers"]["multi_Delta_cell_candidate"])
    phantom["filename"] = "phantom_multi_delta_credit.jsonl.gz"
    result["ledgers"]["phantom_credit"] = phantom
    write_result(target, result)


def mutate_transition(target: Path) -> None:
    result, _cells, _origins = candidate_state(target)
    transition = result[
        "proposed_source_W_transition_if_C30d_is_independently_sealed"
    ]
    transition["candidate_credits"]["whole_origin_exclusion"] = 21
    transition["after"]["excluded"] = 74_767
    transition["after"]["conservative_live"] = 2_065
    transition["after"]["remaining"] = 57
    transition["conservation_identity"] = "74767+2065=76832"
    write_result(target, result)


@dataclass(frozen=True)
class Attack:
    name: str
    mutate: Callable[[Path], None]
    expected_reason_prefix: str


def assert_rejected(
    verifier: ModuleType,
    reference: Any,
    target: Path,
    expected_reason_prefix: str,
) -> tuple[str, str]:
    try:
        verifier.verify_candidate_dir(target, reference)
    except BaseException as error:
        exception = type(error).__name__
        reason = str(error)
        if (
            type(error) is not verifier.Reject
            or not reason.startswith(expected_reason_prefix)
        ):
            raise RuntimeError(
                "corruption rejected for unexpected type/reason:"
                + exception + ":" + reason
            ) from error
        return exception, reason
    raise RuntimeError("coherently reclosed corruption accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True, type=Path)
    arguments = parser.parse_args()
    if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
        raise RuntimeError("run with the pinned interpreter using -I -B")
    candidate = Path(os.path.abspath(os.fspath(arguments.candidate_dir)))
    assert_baseline_shape(candidate)

    verifier = load_pinned_verifier()
    reference = verifier.reconstruct_reference()
    baseline = verifier.verify_candidate_dir(candidate, reference)
    if not (
        baseline["status"].startswith("PASS_INDEPENDENT_CANDIDATE_C30D__")
        and baseline["formal_credit"] == verifier.RESULT_ZERO_FORMAL
        and baseline["manifest_authorized"] is False
        and baseline["candidate_producer_imported_or_executed"] is False
    ):
        raise RuntimeError("baseline did not independently verify at zero credit")

    attacks = (
        Attack(
            "universal-W-contact-deep-reclosure",
            mutate_universal_contact_deep_reclosure,
            "C30d independent universal-target cell:",
        ),
        Attack(
            "target-tie-owner-theorem-deep-reclosure",
            mutate_target_tie_theorem_deep_reclosure,
            "C30d independent universal-target cell:",
        ),
        Attack(
            "whole-origin-3D-2D-1D-0D-owner-deep-reclosure",
            mutate_owner_3d_2d_1d_0d_deep_reclosure,
            "C30d independent materialized atomic owner row:",
        ),
        Attack(
            "whole-origin-EXCLUDED-reclassification",
            mutate_whole_origin_reclassification,
            "C30d independent whole-origin EXCLUDED row:",
        ),
        Attack(
            "child-or-volume-as-whole-origin-credit",
            mutate_child_volume_credit,
            "C30d child/volume credit boundary",
        ),
        Attack(
            "formal-credit-injection",
            mutate_formal_credit,
            "C30d zero formal credit boundary",
        ),
        Attack(
            "D02-illegal-clear",
            mutate_d02,
            "C30d strict nonpromotion boundary",
        ),
        Attack(
            "CM2-illegal-GO",
            mutate_cm2,
            "C30d strict nonpromotion boundary",
        ),
        Attack(
            "input-pin-retarget",
            mutate_input_pin,
            "C30d exact input pins",
        ),
        Attack(
            "ledger-order-contract",
            mutate_ledger_order_contract,
            "C30d ledger descriptor:",
        ),
        Attack(
            "multi-Delta-cell-row-order-reclosure",
            mutate_cell_row_order,
            "C30d candidate canonical row order/census",
        ),
        Attack(
            "whole-origin-row-order-reclosure",
            mutate_origin_row_order,
            "C30d candidate canonical row order/census",
        ),
        Attack(
            "phantom-ledger-field",
            mutate_phantom_ledger,
            "C30d exact candidate-only result",
        ),
        Attack(
            "forged-source-W-transition",
            mutate_transition,
            "C30d exact candidate-only result",
        ),
    )

    rejected: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30d-rejection-suite-") as raw:
        base_dir = Path(raw)
        for ordinal, attack in enumerate(attacks):
            target = base_dir / f"{ordinal:02d}-{attack.name}"
            target.mkdir()
            copy_candidate(candidate, target)
            attack.mutate(target)
            assert_coherent_envelope(target)
            exception, reason = assert_rejected(
                verifier,
                reference,
                target,
                attack.expected_reason_prefix,
            )
            rejected.append({
                "attack": attack.name,
                "exception": exception,
                "reason": reason,
            })

    if not producer_modules_absent():
        raise RuntimeError("producer imported or executed during harness")
    print(wire({
        "schema": (
            "cm2.round306c30d.source-w-multi-delta."
            "coherent-corruption-rejection-suite.v2"
        ),
        "status": "PASS_14_OF_14_COHERENT_CORRUPTIONS_REJECTED",
        "pinned_verifier_sha256": VERIFIER_SHA256,
        "baseline_status": baseline["status"],
        "reference_reconstruction_count": 1,
        "attack_count": len(attacks),
        "all_attack_envelopes_canonically_and_cryptographically_reclosed": True,
        "expected_exception": "Reject",
        "expected_reason_prefixes_enforced": True,
        "formal_credit": verifier.RESULT_ZERO_FORMAL,
        "manifest_authorized": False,
        "producer_imported_or_executed": False,
        "rejected": rejected,
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
