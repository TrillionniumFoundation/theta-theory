#!/usr/bin/env python3
"""Coherent-corruption suite for the append-only v2 C30e candidate.

The expensive independent mathematical reference is reconstructed once.  A
verified candidate is copied into a fresh temporary directory for each
attack; every affected row hash, gzip descriptor, ledger hash, and result hash
is coherently rebound before the pinned verifier is called.  Each attack must
raise only the documented fail-closed Reject reason family.

The candidate attack set now reaches the external 3D/2D/1D/0D owner ledger:
missing/duplicate atoms, owner rebinding, proof/disposition mutation,
cross-dimensional incidence corruption, geometry movement, slice-digest and
descriptor corruption.  Authority-path, TOCTOU and process-contract attacks
remain a mandatory release phase because they require the final C30d terminal and
controlled subprocess launchers; this development harness lists them
explicitly and never claims they have run.

This harness never imports the C30e producer, never mutates its input
candidate, and grants zero formal credit.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round306c30e_source_w_reduced_live_"
    "whole_origin_disposition_v2"
)
VERIFIER = PREFIX + "_independent_verifier.py"
VERIFIER_SHA256 = (
    "684c67e7a7a3927743a410a329b1476c77b1dded881b6cedea0ecdb767dabd87"
)
PRODUCER = PREFIX + "_producer.py"
H_CELL_LEDGER = PREFIX + "_h_cell_ledger.jsonl.gz"
LIVE_CELL_LEDGER = PREFIX + "_strict_live_cell_ledger.jsonl.gz"
ORIGIN_LEDGER = PREFIX + "_whole_origin_ledger.jsonl.gz"
ATOMIC_OWNER_LEDGER = PREFIX + "_atomic_half_open_owner_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"


class HarnessFailure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise HarnessFailure(label)


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def import_pinned_verifier() -> Any:
    path = ROOT / VERIFIER
    status = path.lstat()
    need(
        stat.S_ISREG(status.st_mode)
        and not path.is_symlink()
        and status.st_nlink == 1
        and file_hash(path) == VERIFIER_SHA256,
        "pinned C30e independent verifier",
    )
    need(PRODUCER[:-3] not in sys.modules, "C30e producer not preloaded")
    module_name = VERIFIER[:-3]
    need(module_name not in sys.modules, "C30e verifier not preloaded")
    specification = importlib.util.spec_from_file_location(module_name, path)
    need(
        specification is not None and specification.loader is not None,
        "C30e verifier import specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    try:
        specification.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    need(
        Path(module.__file__).resolve(strict=True) == path.resolve(strict=True)
        and file_hash(path) == VERIFIER_SHA256
        and PRODUCER[:-3] not in sys.modules,
        "imported C30e verifier identity/producer independence",
    )
    return module


verifier = import_pinned_verifier()
wire = verifier.wire
digest = verifier.digest


EXPECTED_FILES = {
    H_CELL_LEDGER,
    LIVE_CELL_LEDGER,
    ATOMIC_OWNER_LEDGER,
    ORIGIN_LEDGER,
    RESULT,
    verifier.base.RUNTIME_ATTESTATION,
}


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("row_sha256", None)
    return {**body, "row_sha256": digest(body)}


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("result_sha256", None)
    return {**body, "result_sha256": digest(body)}


def read_rows(path: Path) -> list[dict[str, Any]]:
    return verifier.canonical_rows(path)


def read_result(path: Path) -> dict[str, Any]:
    return verifier.strict_json(path)


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0
        ) as output:
            for row in rows:
                output.write(wire(row) + b"\n")


def write_result(path: Path, result: dict[str, Any]) -> None:
    path.write_bytes(wire(close_result(result)))


def descriptor_facts(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(rows),
        "size": path.stat().st_size,
        "sha256": file_hash(path),
        "row_sequence_sha256": sequence.hexdigest(),
    }


def refresh_descriptor(
    result: dict[str, Any],
    key: str,
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    descriptor = result["ledgers"][key]
    order = descriptor["order"]
    descriptor.clear()
    descriptor.update(descriptor_facts(path, rows))
    descriptor["order"] = order


def copy_candidate(source: Path, target: Path) -> None:
    need(
        {path.name for path in source.iterdir()} == EXPECTED_FILES,
        "baseline exact file set",
    )
    for filename in sorted(EXPECTED_FILES):
        shutil.copyfile(source / filename, target / filename)


def reclose_origin_change(
    target: Path,
    rows: list[dict[str, Any]],
    result: dict[str, Any],
) -> None:
    write_rows(target / ORIGIN_LEDGER, rows)
    refresh_descriptor(
        result,
        "whole_origin_disposition_candidate",
        target / ORIGIN_LEDGER,
        rows,
    )
    write_result(target / RESULT, result)


def attack_deep_h_atomic_reclosure(target: Path) -> None:
    h_rows = read_rows(target / H_CELL_LEDGER)
    origins = read_rows(target / ORIGIN_LEDGER)
    result = read_result(target / RESULT)
    row = copy.deepcopy(h_rows[0])
    audit = row["H_partition"]["terminal_exact_atomic_owner_audit"]
    audit["all_raw_1D_strata_exactly_reclosed"] = False
    row["H_partition"]["terminal_exact_atomic_owner_audit_sha256"] = digest(
        audit
    )
    h_rows[0] = close_row(row)
    write_rows(target / H_CELL_LEDGER, h_rows)
    refresh_descriptor(
        result,
        "outgoing_H_cell_candidate",
        target / H_CELL_LEDGER,
        h_rows,
    )

    origin = row["origin_key"]
    origin_ordinal = next(
        index for index, value in enumerate(origins)
        if value["origin_key"] == origin
    )
    origin_row = copy.deepcopy(origins[origin_ordinal])
    origin_h_rows = [
        value for value in h_rows if value["origin_key"] == origin
    ]
    origin_row["H_cell_rows_sha256"] = digest(origin_h_rows)
    origins[origin_ordinal] = close_row(origin_row)
    reclose_origin_change(target, origins, result)


def reclose_owner_ledger(
    target: Path,
    rows: list[dict[str, Any]],
    result: dict[str, Any],
) -> None:
    rows.sort(key=lambda row: row["ledger_order_key"])
    write_rows(target / ATOMIC_OWNER_LEDGER, rows)
    refresh_descriptor(
        result,
        "atomic_half_open_owner_candidate",
        target / ATOMIC_OWNER_LEDGER,
        rows,
    )
    write_result(target / RESULT, result)


def attack_missing_3d_leaf_atom(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    index = next(
        ordinal for ordinal, row in enumerate(rows)
        if row["ambient_dimension"] == 3
    )
    rows.pop(index)
    reclose_owner_ledger(target, rows, result)


def attack_duplicate_2d_atom(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    row = next(row for row in rows if row["ambient_dimension"] == 2)
    rows.append(copy.deepcopy(row))
    reclose_owner_ledger(target, rows, result)


def attack_2d_owner_rebinding(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    index = next(
        ordinal for ordinal, row in enumerate(rows)
        if row["ambient_dimension"] == 2
        and len(row["closed_containing_leaf_keys"]) > 1
    )
    row = copy.deepcopy(rows[index])
    old_owner = row["half_open_owner_leaf_key"]
    new_owner = next(
        key for key in row["closed_containing_leaf_keys"] if key != old_owner
    )
    for ordinal, incidence in enumerate(row["closed_incident_leaf_rows"]):
        item = copy.deepcopy(incidence)
        item["selected_by_half_open_owner"] = item["leaf_key"] == new_owner
        row["closed_incident_leaf_rows"][ordinal] = close_row(item)
        if item["leaf_key"] == new_owner:
            row["owner_proof_source"] = item["proof_source"]
            row["owner_disposition"] = item["leaf_disposition"]
    row["closed_incident_leaf_rows_sha256"] = digest(
        row["closed_incident_leaf_rows"]
    )
    row["half_open_owner_leaf_key"] = new_owner
    rows[index] = close_row(row)
    reclose_owner_ledger(target, rows, result)


def attack_1d_cross_dimension_incidence(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    index = next(
        ordinal for ordinal, row in enumerate(rows)
        if row["ambient_dimension"] == 1
    )
    row = copy.deepcopy(rows[index])
    row["incident_sources"] = row["incident_sources"][1:]
    row["incident_source_count"] = len(row["incident_sources"])
    row["cross_dimensional_source_incidence_complete"] = False
    rows[index] = close_row(row)
    reclose_owner_ledger(target, rows, result)


def attack_0d_geometry_move(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    index = next(
        ordinal for ordinal, row in enumerate(rows)
        if row["ambient_dimension"] == 0
    )
    row = copy.deepcopy(rows[index])
    axis = sorted(row["geometry"]["fixed"])[0]
    row["geometry"]["fixed"][axis] = str(
        verifier.Q(row["geometry"]["fixed"][axis]) + verifier.Q(1, 2**40)
    )
    row["geometry_sha256"] = digest(row["geometry"])
    row["ledger_order_key"] = (
        row["origin_key"] + "|3|" + row["geometry_sha256"]
    )
    rows[index] = close_row(row)
    reclose_owner_ledger(target, rows, result)


def attack_3d_proof_and_disposition(target: Path) -> None:
    rows = read_rows(target / ATOMIC_OWNER_LEDGER)
    result = read_result(target / RESULT)
    index = next(
        ordinal for ordinal, row in enumerate(rows)
        if row["ambient_dimension"] == 3
    )
    row = copy.deepcopy(rows[index])
    row["owner_proof_source"] = "FORGED_PROOF_SOURCE"
    row["owner_disposition"] = (
        "LIVE" if row["owner_disposition"] != "LIVE" else "EXCLUDED"
    )
    source = row["source_3D_leaf_row"]
    source["proof_source"] = row["owner_proof_source"]
    source["disposition"] = row["owner_disposition"]
    row["source_3D_leaf_row_sha256"] = digest(source)
    rows[index] = close_row(row)
    reclose_owner_ledger(target, rows, result)


def attack_origin_owner_slice_digest(target: Path) -> None:
    origins = read_rows(target / ORIGIN_LEDGER)
    result = read_result(target / RESULT)
    row = copy.deepcopy(origins[0])
    row["atomic_half_open_owner_ledger_slice"]["rows_sha256"] = "0" * 64
    origins[0] = close_row(row)
    reclose_origin_change(target, origins, result)


def attack_owner_descriptor_only(target: Path) -> None:
    result = read_result(target / RESULT)
    result["ledgers"]["atomic_half_open_owner_candidate"]["sha256"] = "0" * 64
    write_result(target / RESULT, result)


def attack_child_count_credit(target: Path) -> None:
    origins = read_rows(target / ORIGIN_LEDGER)
    result = read_result(target / RESULT)
    row = copy.deepcopy(origins[0])
    child_count = row["lineage_census"]["Round215_reduced_LIVE"]
    row["formal_credit"]["resolved_nonexcluded"] = child_count
    candidate_credit = row[
        "candidate_credit_if_all_dependencies_and_independent_checks_later_seal"
    ]
    candidate_credit["resolved_nonexcluded"] = child_count
    theorem = row["whole_origin_theorem_candidate"]
    theorem["child_count_sheet_count_or_volume_used_as_integer_credit"] = True
    row["whole_origin_theorem_candidate_sha256"] = digest(theorem)
    origins[0] = close_row(row)
    reclose_origin_change(target, origins, result)


def attack_volume_credit(target: Path) -> None:
    origins = read_rows(target / ORIGIN_LEDGER)
    result = read_result(target / RESULT)
    row = copy.deepcopy(origins[0])
    parent_volume = row["exact_volume_conservation"]["original_parent"]
    row["formal_credit"]["whole_source_W_origin_exclusion"] = parent_volume
    candidate_credit = row[
        "candidate_credit_if_all_dependencies_and_independent_checks_later_seal"
    ]
    candidate_credit["whole_source_W_origin_exclusion"] = parent_volume
    theorem = row["whole_origin_theorem_candidate"]
    theorem["child_count_sheet_count_or_volume_used_as_integer_credit"] = True
    row["whole_origin_theorem_candidate_sha256"] = digest(theorem)
    origins[0] = close_row(row)
    reclose_origin_change(target, origins, result)


def attack_d02_cm2_promotion(target: Path) -> None:
    result = read_result(target / RESULT)
    result["formal_credit"]["D02"] = 1
    result["formal_credit"]["CM2"] = 1
    result["strict_nonpromotion"]["D02"] = "UNBLOCKED"
    result["strict_nonpromotion"]["CM2"] = "CLAIM_AUTHORIZED"
    write_result(target / RESULT, result)


def attack_input_pin(target: Path) -> None:
    result = read_result(target / RESULT)
    result["input_pins"][0]["sha256"] = "0" * 64
    write_result(target / RESULT, result)


def attack_ledger_order(target: Path) -> None:
    rows = read_rows(target / H_CELL_LEDGER)
    result = read_result(target / RESULT)
    need(len(rows) >= 2, "H ledger reorder fixture")
    rows[0], rows[1] = rows[1], rows[0]
    write_rows(target / H_CELL_LEDGER, rows)
    refresh_descriptor(
        result,
        "outgoing_H_cell_candidate",
        target / H_CELL_LEDGER,
        rows,
    )
    write_result(target / RESULT, result)


def attack_absolute_predecessor_order(target: Path) -> None:
    result = read_result(target / RESULT)
    result["upstream_authority"]["C30d"]["authority_pins_sha256"] = "0" * 64
    delta = result["proposed_source_W_transition_if_C30e_terminal_replay_passes"]
    delta["before"]["remaining"] = 59
    delta["after"]["remaining"] = 57
    write_result(target / RESULT, result)


Attack = tuple[str, Callable[[Path], None], tuple[str, ...]]


ATTACKS: tuple[Attack, ...] = (
    (
        "deep_h_atomic_reclosure",
        attack_deep_h_atomic_reclosure,
        ("H row exact independent reconstruction:",),
    ),
    (
        "missing_3D_leaf_atom_reclosed_ledger",
        attack_missing_3d_leaf_atom,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "duplicate_2D_atom_reclosed_ledger",
        attack_duplicate_2d_atom,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "2D_half_open_owner_rebinding",
        attack_2d_owner_rebinding,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "1D_cross_dimension_incidence_removed",
        attack_1d_cross_dimension_incidence,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "0D_endpoint_moved",
        attack_0d_geometry_move,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "3D_proof_source_and_disposition_rebound",
        attack_3d_proof_and_disposition,
        ("atomic owner ledger exact independent reconstruction",),
    ),
    (
        "origin_owner_slice_digest_rebound",
        attack_origin_owner_slice_digest,
        ("whole-origin row exact independent reconstruction:",),
    ),
    (
        "owner_ledger_descriptor_only",
        attack_owner_descriptor_only,
        ("candidate result exact reconstruction",),
    ),
    (
        "child_count_as_credit",
        attack_child_count_credit,
        ("whole-origin row exact independent reconstruction:",),
    ),
    (
        "volume_as_credit",
        attack_volume_credit,
        ("whole-origin row exact independent reconstruction:",),
    ),
    (
        "D02_CM2_promotion",
        attack_d02_cm2_promotion,
        ("candidate result exact reconstruction",),
    ),
    (
        "input_pin_reclosure",
        attack_input_pin,
        ("candidate result exact reconstruction",),
    ),
    (
        "ledger_order_reclosure",
        attack_ledger_order,
        ("candidate ledger row count/order",),
    ),
    (
        "absolute_predecessor_order_binding",
        attack_absolute_predecessor_order,
        ("candidate result exact reconstruction",),
    ),
)


MANDATORY_RELEASE_ONLY_ATTACKS = (
    "C30d_adapter_source_SHA_substitution_or_unpinned_adapter",
    "C30d_dynamic_pins_SHA_substitution_or_wrong_chain_basename",
    "C30d_terminal_replay_or_chain_status_substitution",
    "C30d_root_or_payload_manifest_substitution_extra_or_missing_member",
    "C30d_outer_verifier_or_terminal_seal_substitution",
    "C30d_receipt_object_hash_closure_forgery",
    "C30d_fake_before_after_remaining_credit_or_nonexact_status",
    "C30d_terminal_member_symlink_hardlink_extra_member_or_atomic_replace",
    "C30d_authority_TOCTOU_during_adapter_and_independent_recapture",
    "candidate_member_hardlink_symlink_extra_member_or_atomic_replace",
    "producer_missing_seed_wrong_seed_extra_environment_or_python_I",
    "verifier_wrong_python_runtime_or_producer_import",
    "producer_wrong_hash_fingerprint_or_unsafe_sys_path",
    "dual_seed_candidate_or_stdout_byte_mismatch",
    "input_and_manifest_pre_post_SHA_stat_drift",
    "cold_replay_protected_root_write_or_historical_candidate_read",
)


def reason_allowed(reason: str, prefixes: tuple[str, ...]) -> bool:
    return any(reason == prefix or reason.startswith(prefix) for prefix in prefixes)


def run(
    candidate: Path,
    adapter_path: Path,
    adapter_sha256: str,
    chain_path: Path,
    pins_path: Path,
    pins_sha256: str,
) -> dict[str, Any]:
    candidate = Path(os.path.abspath(os.fspath(candidate)))
    status = candidate.lstat()
    need(
        stat.S_ISDIR(status.st_mode) and not candidate.is_symlink(),
        "baseline candidate regular directory",
    )
    reference = verifier.reconstruct_reference(
        adapter_path,
        adapter_sha256,
        chain_path,
        pins_path,
        pins_sha256,
    )
    baseline = verifier.verify_candidate_dir(candidate, reference)
    outcomes: list[dict[str, Any]] = []
    reject_types = (verifier.Reject, verifier.base.Reject)
    for name, mutate, allowed in ATTACKS:
        with tempfile.TemporaryDirectory(prefix="c30e-attack-") as temporary:
            target = Path(temporary) / "candidate"
            target.mkdir()
            copy_candidate(candidate, target)
            mutate(target)
            try:
                verifier.verify_candidate_dir(target, reference)
            except reject_types as error:
                reason = str(error)
                need(
                    reason_allowed(reason, allowed),
                    "unconstrained Reject reason:" + name + ":" + reason,
                )
                outcomes.append({
                    "attack": name,
                    "status": "REJECTED_AS_REQUIRED",
                    "reject_reason": reason,
                    "allowed_reason_prefixes": list(allowed),
                })
            except BaseException as error:
                raise HarnessFailure(
                    "non-Reject exception:" + name + ":" + type(error).__name__
                ) from error
            else:
                raise HarnessFailure("coherent attack accepted:" + name)
    need(
        len(outcomes) == len(ATTACKS)
        and all(row["status"] == "REJECTED_AS_REQUIRED" for row in outcomes)
        and PRODUCER[:-3] not in sys.modules,
        "all coherent C30e attacks rejected",
    )
    return {
        "schema": (
            "cm2.round306c30e.source-w-reduced-live."
            "coherent-attack-harness.candidate.v3"
        ),
        "status": "PASS_ALL_C30E_V2_COHERENT_ATTACKS_REJECTED",
        "baseline_candidate_result_sha256": baseline[
            "candidate_result_sha256"
        ],
        "verifier_sha256": VERIFIER_SHA256,
        "reference_reconstruction_count": 1,
        "attack_count": len(outcomes),
        "attacks": outcomes,
        "external_atomic_owner_ledger_attack_count": 8,
        "mandatory_release_only_attack_count": len(
            MANDATORY_RELEASE_ONLY_ATTACKS
        ),
        "mandatory_release_only_attacks_not_run_here": list(
            MANDATORY_RELEASE_ONLY_ATTACKS
        ),
        "release_ready": False,
        "candidate_producer_imported_or_executed": False,
        "original_candidate_mutated": False,
        "formal_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--predecessor-adapter", required=True, type=Path)
    parser.add_argument("--predecessor-adapter-sha256", required=True)
    parser.add_argument("--predecessor-chain-dir", required=True, type=Path)
    parser.add_argument("--predecessor-dynamic-pins", required=True, type=Path)
    parser.add_argument("--predecessor-dynamic-pins-sha256", required=True)
    arguments = parser.parse_args()
    try:
        output = run(
            arguments.candidate,
            arguments.predecessor_adapter,
            arguments.predecessor_adapter_sha256,
            arguments.predecessor_chain_dir,
            arguments.predecessor_dynamic_pins,
            arguments.predecessor_dynamic_pins_sha256,
        )
    except (
        HarnessFailure,
        verifier.Reject,
        verifier.base.Reject,
        KeyError,
        OSError,
        ValueError,
        TypeError,
        RuntimeError,
    ) as error:
        print("REJECT:" + str(error), file=sys.stderr)
        return 2
    print(wire(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
